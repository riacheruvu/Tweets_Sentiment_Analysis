# A 2019 tweet project, revisited in 2026

In 2019, one of my first deep learning courses had me asking whether I could recognize opinions about self-driving cars in tweets. I cleaned up the text, tried Word2Vec and GloVe, and trained a Keras CNN. It was one of those projects where the whole pipeline felt exciting because I could see each piece learning.

I recently reopened that work to try a different idea: what changes when the model is asked for a typed decision instead of being trained as a task-specific classifier?

This repo keeps both versions together. The original notebook, report, slides, and dataset are still here. The 2026 version uses TypeSafe's Jev through OpenRouter. I’m treating this as a learning experiment, not a claim that the newer approach is automatically better.

## Try the 2026 version

You’ll need Python 3.10+ and an OpenRouter API key. Jev requests are billed to your OpenRouter account. Set the key in the terminal you plan to run the demo from; it only stays set for that terminal session.

In PowerShell on Windows:

```powershell
$secureKey = Read-Host "OpenRouter API key (input is hidden)" -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new("", $secureKey).Password
Set-Location jev
python sentiment.py --text "I love the idea of a self-driving car, but I would not trust it on an icy road."
Remove-Item Env:OPENROUTER_API_KEY
Remove-Variable secureKey
```

In macOS/Linux bash or zsh:

```bash
export OPENROUTER_API_KEY="your-api-key"
cd jev
python sentiment.py --text "I love the idea of a self-driving car, but I would not trust it on an icy road."
```

You’ll get one of six labels, the probabilities for all six choices, and Jev's confidence. Try a happy tweet, a skeptical one, and something unrelated. Seeing how the probabilities move is part of the fun.

Want to try a few rows from the tiny sample file?

```bash
python sentiment.py --input examples/tweets.csv --limit 3 --output results.csv
```

The CSV is just for exploring the workflow; it is not evaluation data. Start with a small limit before sending any bigger dataset, since each non-empty row makes a billed API request.

## What changed between versions?

The 2019 CNN learns from labeled tweets and word embeddings. The 2026 Jev version sends a tweet as state, asks a typed six-way question, and gets back a choice with probabilities. The labels keep the original broad shape: five sentiment levels plus `not_relevant`.

I find the interface shift interesting. The application defines the choices, Jev returns a structured judgment, and the rest of the code decides what to do with it. That’s different from parsing a paragraph—but a tidy response is not automatically a right response. Confidence is not accuracy, so a fair comparison still needs the same human-reviewed examples and labels for both approaches.

## Try the agent skill

There’s a small project skill at [`.agents/skills/jev-decision-lab/SKILL.md`](.agents/skills/jev-decision-lab/SKILL.md). It helps an agent turn a fixed-choice, yes/no, or scoring task into a Jev schema and a sensible evaluation plan.

Open this repo in an agent that supports project skills, then try:

> Use `$jev-decision-lab` to classify the three toy app reviews in `jev/SKILL_DEMO.md` as `bug`, `feature_request`, or `praise`. Keep the labels distinct, show the Jev question schema, and suggest a small human-reviewed evaluation plan. Don’t call the API.

I included a [skill demo prompt and walkthrough](jev/SKILL_DEMO.md) so it’s clear what to ask and what a useful answer should cover.

## A few useful places to look

- [`CaseStudyinSentimentAnalysis.ipynb`](CaseStudyinSentimentAnalysis.ipynb) — the 2019 notebook.
- [`jev/sentiment.py`](jev/sentiment.py) — the small Python client for Jev through OpenRouter.
- [`jev/LEARNING_LAB.md`](jev/LEARNING_LAB.md) — experiments and comparison ideas.
- [`jev/README.md`](jev/README.md) — setup and CSV instructions.

The API client uses Python's standard library and OpenRouter's Decisions API with `typesafe/jev-1.13`. For the API shape and current Jev access details, see [OpenRouter's Jev guide](https://openrouter.ai/blog/tutorials/how-to-use-jev/).
