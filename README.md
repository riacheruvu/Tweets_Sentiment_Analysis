# Tweet sentiment analysis: original study and OpenJev extension

This repository began as a study of opinions about self-driving cars in tweets, using Word2Vec, GloVe, and a Keras convolutional neural network. The original notebook, report, slides, and annotated dataset remain at the repository root.

## Try the OpenJev extension

The `openjev/` directory adds an educational, zero-shot classification path using [OpenJev](https://github.com/razorback16/openjev), an independent open-source implementation of a typed System One decision API. It sends the tweet text and asks OpenJev to choose among six classes aligned with the original dataset: sentiment levels 1–5 and `not_relevant`.

See [`openjev/README.md`](openjev/README.md) for setup, API credentials, single-tweet and CSV commands, and important comparison caveats. The original CSV's `text` column is used by default. Try `--limit 20` before processing the full file because each non-empty row produces a separate API request.

## Educational comparison

The original CNN path learns from labeled examples and word embeddings. The OpenJev path applies a pretrained model at request time and returns probabilities for typed choices. The extension is a new-tech companion, not a claim that the newer approach performs better or exactly reproduces the original study. Compare both on the same human-reviewed held-out examples, and treat OpenJev confidence as distinct from measured accuracy.

See [`openjev/LEARNING_LAB.md`](openjev/LEARNING_LAB.md) for guided exercises and a comparison plan.
