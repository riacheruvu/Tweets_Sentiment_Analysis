# Learning lab: from embeddings to typed decisions

Use this companion alongside the original notebook and report. The goal is to understand a change in method, not to assume a newer model wins.

## 1. Observe the new interface

Run the sample rows from `examples/tweets.csv`. For one tweet, compare the predicted label with all six probabilities. Jev's probabilities describe the model's distribution across the options; confidence summarizes how concentrated that distribution is.

Try sarcasm, mixed praise and criticism, or a tweet that only mentions a self-driving car without expressing an opinion. Write down where the labels lose nuance.

## 2. Compare the assumptions

The historical project builds representations from word embeddings and trains a CNN with labeled data. This 2026 companion asks pretrained Jev to choose among descriptions at request time. The original labels use a five-level sentiment scale plus `not_relevant`; this project expresses those as descriptive options. The historical model learns from the task dataset; Jev depends on the option descriptions, its pretrained model, and a hosted API. Neither method is guaranteed to handle the domain or labels correctly.

## 3. Design a fair comparison

1. Reserve a held-out set of tweets with human-reviewed labels.
2. Run the historical CNN and Jev on the same texts.
3. Map both systems to the same label definitions before scoring.
4. Report macro-F1 and per-class precision/recall, along with the example count per class.
5. Review disagreements manually, especially neutral and mixed-sentiment examples.
6. Keep Jev confidence separate from measured accuracy. If desired, assess calibration by grouping predictions into confidence ranges and comparing each range's confidence with observed accuracy.

The sample CSV is illustrative only. It is too small and not independently labeled, so it cannot support performance claims.

## 4. Experiments

- Change the class descriptions in `sentiment.py`. Which ambiguous tweets change labels?
- Add a second typed question, such as whether the tweet concerns safety. Inspect that answer independently of sentiment.
- Save Jev's outputs for a human-reviewed sample, then replay different confidence thresholds without paying for another inference call.
- Add a gold-label column to a copy of the dataset and calculate macro-F1 and a confusion matrix.

## Discussion

- Which failure modes came from label definitions, the model, or the data?
- Did high confidence correspond to correct predictions on the reviewed examples?
- What information did the embedding/CNN workflow make visible that the API-based workflow hides, and vice versa?
- What would need to be true before you used either system for a consequential decision?
