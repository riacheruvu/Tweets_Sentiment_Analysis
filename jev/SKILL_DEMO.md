# A tiny demo for the Jev Decision Lab skill

The project skill is intentionally reusable: it helps an agent design a typed Jev task, whether that task is sentiment, routing, scoring, or a yes/no check. This demo applies it to the sentiment project itself. It does not call Jev or use an API key.

## Try this prompt

Open the repository in an agent that can load project skills and ask:

> Use `$jev-decision-lab` to review the sentiment task in `jev/sentiment.py`. Keep the original six labels, check whether the descriptions make mixed opinions hard to classify, and show a small revised Jev question schema plus a second `noul` question for whether the tweet raises a safety concern. Include a fair evaluation plan for human-reviewed tweets. Don’t edit files or call the API.

You can use these two examples to focus the discussion:

- “I love the idea of a self-driving car, but I would not trust it on an icy road.”
- “The prototype completed another 100-mile test on public roads today.”

## What a useful skill response should include

1. The same six outcome keys as the project, with distinct explanations tied to the original 1–5 scale and `not_relevant` class.
2. A `choice` question for overall sentiment and a separate `noul` question for safety concerns.
3. A request sketch that puts the tweet in `state`, along with a note that the schema structures the answer but does not make it correct.
4. A human-reviewed holdout plan using the same tweets for the historical CNN and Jev, with per-class precision/recall or macro-F1.
5. A reminder that confidence is not accuracy and live requests need an OpenRouter key and are billed.

The project is still specifically about tweets on self-driving cars because that’s what the 2019 data and labels cover. The skill stays generic so the same workflow can help with another bounded task later. Calling the model on a different social-media domain would need fresh criteria and evaluation; the current demo does not establish that it generalizes.
