"""Classify tweet sentiment with OpenJev's typed System One API."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


LABELS = {
    "very_negative": "Sentiment rating 1: strongly negative, skeptical, fearful, or opposed.",
    "negative": "Sentiment rating 2: somewhat negative, skeptical, or opposed.",
    "neutral": "Sentiment rating 3: factual, undecided, or without a clear positive or negative opinion.",
    "positive": "Sentiment rating 4: somewhat positive, interested, or supportive.",
    "very_positive": "Sentiment rating 5: strongly positive, excited, or supportive.",
    "not_relevant": "The tweet is outside the self-driving or autonomous vehicle topic, or is not about that technology.",
}
DEFAULT_BASE_URL = "https://api.codiv.ai"


class OpenJevError(RuntimeError):
    """Raised when the OpenJev request fails or has an unexpected response."""


def classify(text: str, *, base_url: str, api_key: str | None, timeout: float = 60) -> dict:
    """Return sentiment, per-label probabilities, and service confidence."""
    if not text.strip():
        raise ValueError("Tweet text must not be empty")

    payload = {
        "model": "openjev-latest",
        "state": text,
        "questions": {
            "sentiment": {
                "type": "choice",
                "instructions": "Classify the overall sentiment expressed in this tweet.",
                "criteria": LABELS,
            }
        },
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(
        f"{base_url.rstrip('/')}/v1/systemone",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise OpenJevError(f"OpenJev returned HTTP {error.code}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise OpenJevError(f"Could not reach OpenJev: {error}") from error
    except json.JSONDecodeError as error:
        raise OpenJevError("OpenJev returned invalid JSON") from error

    try:
        answer = body["answers"]["sentiment"]
        probabilities = answer["probabilities"]
        sentiment = answer["choice"]
        confidence = answer["confidence"]
    except (KeyError, TypeError) as error:
        raise OpenJevError(f"Unexpected OpenJev response: {body}") from error
    if sentiment not in LABELS:
        raise OpenJevError(f"OpenJev returned an unknown sentiment: {sentiment!r}")
    return {"sentiment": sentiment, "probabilities": probabilities, "confidence": confidence}


def analyze_csv(input_path: Path, output_path: Path, text_column: str, *, base_url: str, api_key: str | None, limit: int | None = None) -> int:
    """Classify each non-empty text row and write enriched rows to a CSV."""
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or text_column not in reader.fieldnames:
            raise ValueError(f"CSV must include a {text_column!r} column")
        fieldnames = list(reader.fieldnames) + [
            "openjev_sentiment", "openjev_confidence",
            *(f"probability_{label}" for label in LABELS),
        ]
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if limit is not None and len(rows) >= limit:
                break
            tweet = (row.get(text_column) or "").strip()
            if not tweet:
                row.update({"openjev_sentiment": "", "openjev_confidence": ""})
                row.update({f"probability_{label}": "" for label in LABELS})
            else:
                result = classify(tweet, base_url=base_url, api_key=api_key)
                row["openjev_sentiment"] = result["sentiment"]
                row["openjev_confidence"] = result["confidence"]
                for label in LABELS:
                    row[f"probability_{label}"] = result["probabilities"].get(label, "")
                print(f"Classified CSV row {line_number}: {result['sentiment']}", file=sys.stderr)
            rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify tweet sentiment with OpenJev.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="One tweet to classify")
    source.add_argument("--input", type=Path, help="Input CSV file")
    parser.add_argument("--text-column", default="text", help="CSV column containing text (default: text; matches the original dataset)")
    parser.add_argument("--output", type=Path, help="Output CSV (required with --input)")
    parser.add_argument("--limit", type=int, help="Classify at most this many CSV rows (useful for a small first run)")
    parser.add_argument("--base-url", default=os.environ.get("OPENJEV_BASE_URL", DEFAULT_BASE_URL))
    args = parser.parse_args()

    if args.input:
        if not args.output:
            parser.error("--output is required with --input")
        try:
            if args.limit is not None and args.limit < 1:
                raise ValueError("--limit must be a positive integer")
            count = analyze_csv(
                args.input, args.output, args.text_column,
                base_url=args.base_url, api_key=os.environ.get("TYPESAFE_API_KEY"), limit=args.limit,
            )
        except (OSError, ValueError, OpenJevError) as error:
            parser.error(str(error))
        print(f"Wrote {count} rows to {args.output}")
        return 0

    try:
        result = classify(args.text, base_url=args.base_url, api_key=os.environ.get("TYPESAFE_API_KEY"))
    except (ValueError, OpenJevError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
