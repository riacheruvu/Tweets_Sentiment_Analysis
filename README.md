# Tweet sentiment analysis: original study and OpenJev extension

This repository began as a study of opinions about self-driving cars in tweets, using Word2Vec, GloVe, and a Keras convolutional neural network. The original notebook, report, slides, and annotated dataset remain at the repository root.

## Try the OpenJev extension

The `openjev/` directory adds an educational, zero-shot classification path using [OpenJev](https://github.com/razorback16/openjev), an independent open-source implementation of a typed System One decision API. It sends the tweet text and asks OpenJev to choose among six classes aligned with the original dataset: sentiment levels 1–5 and `not_relevant`.

See [`openjev/README.md`](openjev/README.md) for setup, API credentials, single-tweet and CSV commands, and important comparison caveats. The original CSV's `text` column is used by default. Try `--limit 20` before processing the full file because each non-empty row produces a separate API request.

For a quick “autonomous-car tweet vibe check,” put your OpenJev-compatible API key in `TYPESAFE_API_KEY`, then run:

```bash
cd openjev
python sentiment.py --text "I love the idea of a self-driving car, but I would not trust it on an icy road."
```

The CLI prints the chosen label and probabilities for all six options. Try a clearly positive, skeptical, factual, and off-topic message and compare how the probability distribution changes. The result is dynamic; the included examples are for exploration, not benchmark scores.

## Educational comparison

The original CNN path learns from labeled examples and word embeddings. The OpenJev path applies a pretrained model at request time and returns probabilities for typed choices. The extension is a new-tech companion, not a claim that the newer approach performs better or exactly reproduces the original study. Compare both on the same human-reviewed held-out examples, and treat OpenJev confidence as distinct from measured accuracy.

See [`openjev/LEARNING_LAB.md`](openjev/LEARNING_LAB.md) for guided exercises and a comparison plan.

## Reusable agent workflow

The repository also includes [`openjev-decision-lab`](.agents/skills/openjev-decision-lab/SKILL.md), a project skill for agents that need to turn a bounded classification, rating, or yes/no task into a typed-decision demo and a careful evaluation plan.
