"""Classify tweet sentiment with TypeSafe Jev through OpenRouter."""

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
DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = "typesafe/jev-1.13"


class JevError(RuntimeError):
    """Raised when the Jev request fails or has an unexpected response."""


def classify(text: str, *, api_key: str | None = None, timeout: float = 60) -> dict:
    """Return Jev's selected sentiment, probabilities, and confidence."""
    if not text.strip():
        raise ValueError("Tweet text must not be empty")
    if not api_key:
        raise JevError("Set OPENROUTER_API_KEY before calling Jev.")

    payload = {
        "model": MODEL,
        "state": {"tweet": text},
        "questions": {
            "sentiment": {
                "type": "choice",
                "instructions": "Classify the overall sentiment expressed in `tweet` about self-driving or autonomous vehicles.",
                "criteria": LABELS,
            }
        },
    }
    request = Request(
        DECISIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise JevError(f"OpenRouter returned HTTP {error.code}: {detail}") from error
    except (URLError, TimeoutError) as error:
        raise JevError(f"Could not reach OpenRouter: {error}") from error
    except json.JSONDecodeError as error:
        raise JevError("OpenRouter returned invalid JSON") from error

    try:
        answer = body["answers"]["sentiment"]
        if answer["type"] != "choice":
            raise TypeError("sentiment answer was not a choice")
        probabilities = answer["probabilities"]
        sentiment = answer["choice"]
        confidence = answer["confidence"]
    except (KeyError, TypeError) as error:
        raise JevError(f"Unexpected Jev response: {body}") from error
    if sentiment not in LABELS:
        raise JevError(f"Jev returned an unknown sentiment: {sentiment!r}")
    return {
        "sentiment": sentiment,
        "probabilities": probabilities,
        "confidence": confidence,
        "model": body.get("model", MODEL),
        "usage": body.get("usage", {}),
    }


def analyze_csv(input_path: Path, output_path: Path, text_column: str, *, api_key: str | None, limit: int | None = None) -> int:
    """Classify each non-empty text row and write enriched rows to a CSV."""
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or text_column not in reader.fieldnames:
            raise ValueError(f"CSV must include a {text_column!r} column")
        fieldnames = list(reader.fieldnames) + [
            "jev_sentiment", "jev_confidence",
            *(f"probability_{label}" for label in LABELS),
        ]
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if limit is not None and len(rows) >= limit:
                break
            tweet = (row.get(text_column) or "").strip()
            if not tweet:
                row.update({"jev_sentiment": "", "jev_confidence": ""})
                row.update({f"probability_{label}": "" for label in LABELS})
            else:
                result = classify(tweet, api_key=api_key)
                row["jev_sentiment"] = result["sentiment"]
                row["jev_confidence"] = result["confidence"]
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
    parser = argparse.ArgumentParser(description="Classify tweet sentiment with Jev through OpenRouter.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="One tweet to classify")
    source.add_argument("--input", type=Path, help="Input CSV file")
    parser.add_argument("--text-column", default="text", help="CSV column containing text (default: text; matches the original dataset)")
    parser.add_argument("--output", type=Path, help="Output CSV (required with --input)")
    parser.add_argument("--limit", type=int, help="Classify at most this many CSV rows (useful for a small first run)")
    args = parser.parse_args()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if args.input:
        if not args.output:
            parser.error("--output is required with --input")
        try:
            if args.limit is not None and args.limit < 1:
                raise ValueError("--limit must be a positive integer")
            count = analyze_csv(args.input, args.output, args.text_column, api_key=api_key, limit=args.limit)
        except (OSError, ValueError, JevError) as error:
            parser.error(str(error))
        print(f"Wrote {count} rows to {args.output}")
        return 0

    try:
        result = classify(args.text, api_key=api_key)
    except (ValueError, JevError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
