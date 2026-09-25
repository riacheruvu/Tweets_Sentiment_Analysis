# The 2026 version: tweet sentiment with Jev

This is the newer half of the project. The other half is my 2019 CNN notebook, still in the repository root. I wanted to keep the original work visible and try the same question with a different model interface.

The Python script sends a tweet to TypeSafe's Jev through OpenRouter, asks a six-way typed question, and prints the chosen label with probabilities. It uses the original broad label shape: sentiment ratings 1–5 plus `not_relevant`.

## Setup

You’ll need Python 3.10+ and an OpenRouter API key. If you’re new, [create an OpenRouter account](https://openrouter.ai/), add credits if needed from [Settings → Credits](https://openrouter.ai/settings/credits), then create a key in [Settings → Keys](https://openrouter.ai/settings/keys). A per-key spending limit is a useful guardrail. Jev calls are billed to the account associated with your key; no separate TypeSafe account is needed.

In PowerShell:

```powershell
$secureKey = Read-Host "OpenRouter API key (input is hidden)" -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new("", $secureKey).Password
```

In macOS/Linux bash or zsh:

```bash
export OPENROUTER_API_KEY="your-api-key"
```

Keep the key in your terminal environment. Don’t put it in the script, a notebook, or a commit.

## Try a tweet

```bash
python sentiment.py --text "I love the idea of a self-driving car, but I would not trust it on an icy road."
```

Then try an excited tweet, a neutral observation, and an unrelated one. The CLI prints the selected label, all six probabilities, confidence, model, and usage details. This is a live demo, so the answer can change. These examples are here to explore the interface; they aren’t benchmark results.

## Try a few CSV rows

```bash
python sentiment.py --input examples/tweets.csv --limit 3 --output results.csv
```

The output keeps the input columns and adds `jev_sentiment`, `jev_confidence`, and one probability column per label. Each non-empty row makes a separately billed request, so the limit is a nice way to start small. The sample CSV is hand-written and not evaluation data.

## What I’m comparing

The 2019 model learns from labeled examples. This 2026 version asks pretrained Jev to choose among options at request time. That makes for an interesting comparison, but the task setup and assumptions differ. For a fair evaluation, run both on the same human-reviewed examples and compare per-class precision/recall and macro-F1. A confident answer can still be wrong.

For the request walkthrough and experiments, see [`CONCEPTS.md`](CONCEPTS.md) and [`LEARNING_LAB.md`](LEARNING_LAB.md). For a quick example of the reusable agent skill, see [`SKILL_DEMO.md`](SKILL_DEMO.md). The [Medium article draft](ARTICLE_DRAFT.md) uses the PNGs in `images/`; the included image script can regenerate them with Pillow, but the sentiment client itself needs no extra packages.

The client calls OpenRouter's Decisions API using `typesafe/jev-1.13`. See [OpenRouter's Jev guide](https://openrouter.ai/blog/tutorials/how-to-use-jev/) for the request shape and current access details.
