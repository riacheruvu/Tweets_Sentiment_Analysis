# Tweet sentiment with OpenJev

An educational update to [Ria Cheruvu's original tweet sentiment analysis](https://github.com/riacheruvu/Tweets_Sentiment_Analysis). The original study explored Word2Vec, GloVe, and a Keras convolutional neural network for opinions about self-driving cars. This small companion project adds a modern, API-based baseline using OpenJev.

## What you will learn

- How to send the original six-way sentiment scheme as a typed `choice` question to an OpenJev-compatible System One endpoint.
- How sentiment labels and their probabilities differ from a generated explanation.
- Why confidence is not the same thing as accuracy, and why model outputs should be checked against labeled examples.
- How to run the same analysis over individual text or a CSV file.

OpenJev is an independent open-source project. This example uses its documented `/v1/systemone` API. The default endpoint below is the hosted Codiv endpoint; you can point `OPENJEV_BASE_URL` at your own OpenJev server instead.

## Setup

Requires Python 3.10+ and uses only the Python standard library.

PowerShell:

```powershell
$env:TYPESAFE_API_KEY = "your-api-key"
```

macOS/Linux:

```bash
export TYPESAFE_API_KEY="your-api-key"
```

For a local OpenJev server, set the base URL (without `/v1/systemone`):

```powershell
$env:OPENJEV_BASE_URL = "http://127.0.0.1:8080"
```

## Try one tweet

```bash
python sentiment.py --text "I love how safely the self-driving car handled that turn."
```

The result includes the selected label, probability for every label, and OpenJev's confidence score.

## Analyze a CSV

The CSV must have a header row. Select the text column with `--text-column`:

```bash
python sentiment.py --input examples/tweets.csv --output results.csv
```

Download the [original dataset CSV](https://raw.githubusercontent.com/riacheruvu/Tweets_Sentiment_Analysis/master/Twitter-sentiment-self-drive-DFE-dataset.csv) and pass its path directly; its tweet text field is named `text`, which is the CLI default. Start with a small sample before processing the full file, since each non-empty row makes a separate service request:

```bash
python sentiment.py --input path/to/Twitter-sentiment-self-drive-DFE-dataset.csv --limit 20 --output results.csv
```

The original `sentiment` labels are `1` to `5` plus `not_relevant`. OpenJev uses descriptive labels (`very_negative`, `negative`, `neutral`, `positive`, `very_positive`, `not_relevant`) corresponding to those six categories. The enriched output preserves the original columns and does not replace or reinterpret their annotations. Note that this project makes the label mapping explicit for teaching; review the original report and annotation instructions before treating it as an exact replication of the original experiment.

Each row is sent to the service separately; keep request volume and endpoint limits in mind. The output retains the input columns and adds `openjev_sentiment`, `openjev_confidence`, and one probability column per label.

## How it works

The client sends one `choice` question with six candidate outcomes matching the source data: ratings 1–5 and `not_relevant`. OpenJev scores those typed options and returns probabilities. It does not generate a free-form answer that the client has to parse.

This is zero-shot classification: no model is trained on the original labels in this project. That makes it useful for a quick comparison, but it is not automatically better than the original CNN. The class descriptions, domain, class balance, and label quality can all change performance. For an honest comparison, run both approaches on the same held-out, human-labeled tweets and report class-wise precision/recall or macro-F1. Treat confidence as the model's certainty distribution, not a promise that its answer is correct.

## Project map

- `sentiment.py` — API client and CSV/one-text command line interface.
- `examples/tweets.csv` — tiny, hand-written examples for trying the workflow (not evaluation data).
- Original notebook, report, slides, and dataset — available from the [source repository](https://github.com/riacheruvu/Tweets_Sentiment_Analysis).

## API details

The request uses `POST {OPENJEV_BASE_URL}/v1/systemone`, model `openjev-latest`, and a `choice` question. Set `TYPESAFE_API_KEY` for hosted endpoints. OpenJev's API is Jev-compatible, but OpenJev is independently developed and is not affiliated with TypeSafe AI.

## Further reading

- [Original sentiment analysis repository](https://github.com/riacheruvu/Tweets_Sentiment_Analysis)
- [OpenJev](https://github.com/razorback16/openjev)
- [OpenJev API and question types](https://github.com/razorback16/openjev#api)
