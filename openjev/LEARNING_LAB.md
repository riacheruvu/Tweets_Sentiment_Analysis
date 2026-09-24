# Learning lab: from embeddings to typed decisions

Use this companion alongside the original notebook and report. The goal is to understand a change in method, not to assume a newer model wins.

## 1. Observe the new interface

Run the sample rows from `examples/tweets.csv`. For one tweet, compare the predicted label with all six probabilities. The probabilities describe the model's choice distribution for that request; the separate confidence value summarizes how concentrated that distribution is.

Try a tricky example such as sarcasm, mixed praise and criticism, or a tweet that only mentions a self-driving car without expressing an opinion. Write down where the three-label setup loses nuance.

## 2. Compare the assumptions

The historical project builds representations from word embeddings and trains a CNN with labeled data. This companion asks a pretrained OpenJev model to choose among descriptions at request time. The original labels use a five-level sentiment scale plus `not_relevant`; this project expresses those as descriptive options. The historical model learns from a task dataset; the OpenJev path depends on the option descriptions, pretrained knowledge, and service model. Neither method is guaranteed to handle the domain or labels correctly.

## 3. Design a fair comparison

1. Reserve a held-out set of tweets with human-reviewed labels.
2. Run the historical model and OpenJev on exactly those same texts.
3. Map both systems to the same label definitions before scoring.
4. Report macro-F1 and the per-class precision/recall, along with the number of examples per class.
5. Review disagreements manually, especially neutral and mixed-sentiment examples.
6. Keep OpenJev confidence separate from measured accuracy. If desired, assess calibration by grouping predictions into confidence ranges and comparing each range's confidence with its observed accuracy.

The sample CSV is illustrative only. It is too small and not independently labeled, so it cannot support performance claims.

## 4. Experiments

- Change the class descriptions in `sentiment.py`. Which ambiguous tweets change labels?
- Add a second typed question, such as whether the tweet concerns safety. Inspect that answer independently of sentiment.
- Point the client at a local server with `OPENJEV_BASE_URL` and compare the same request against a hosted endpoint.
- Add a human-reviewed gold-label column to a copy of the dataset, then build an evaluation script that calculates macro-F1 and a confusion matrix.

## Discussion

- Which failure modes came from the label definitions, the model, or the data?
- Did high confidence correspond to correct predictions on your reviewed examples?
- What information did the embedding/CNN workflow make visible that the API-based workflow hides (and vice versa)?
- What would need to be true before you would use either system to make a consequential decision?
