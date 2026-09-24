# A tiny demo for the Jev Decision Lab skill

The project skill helps an agent design a typed Jev task. This walkthrough is for trying the skill itself; it does not call Jev or use an API key.

## Try this prompt

Open the repository in an agent that can load project skills and ask:

> Use `$jev-decision-lab` to adapt this project to classify these app reviews as `bug`, `feature_request`, or `praise`. Keep the three labels distinct. Show the Jev question schema, a short Python request sketch, and an evaluation plan for a small human-reviewed sample. Don’t call the API.

For example, the toy reviews could be:

- “The save button closes the screen but my changes disappear.”
- “I’d love a dark mode option.”
- “This is much easier to use than the old app.”

## What a useful skill response should include

1. A `choice` question whose criteria define `bug`, `feature_request`, and `praise` clearly.
2. A state containing the review text, and an instruction that asks for its primary intent.
3. A note that the schema makes the output structured but does not guarantee a correct label.
4. An evaluation plan using reviews labeled by a person, with class counts and per-class precision/recall or macro-F1.
5. A reminder that a live request needs `OPENROUTER_API_KEY` and is billed through OpenRouter.

The important part is the design conversation: are the labels distinct enough, is there a missing `other` class, and what evidence would tell us whether the classifier is useful? The skill should surface those decisions before anyone spends money on a larger batch.
