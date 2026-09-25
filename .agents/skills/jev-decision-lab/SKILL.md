---
name: jev-decision-lab
description: Build a small, understandable demo using TypeSafe Jev through OpenRouter, with a grounded typed schema and evaluation plan. Use for fixed-choice classification, ordinal scoring, or yes/no decisions; use a generative model when the task needs free-form text.
---

# Jev Decision Lab

Turn a concrete decision task into a small example using TypeSafe's Jev model through OpenRouter, and explain what its outputs do and do not establish.

## Shape the decision

- Start from the user's actual task and inspect input fields and labels before choosing a schema.
- Use `choice` for mutually exclusive categories, `score` for an ordered scale, and `noul` for a yes/no judgment. Keep the question narrow and option descriptions distinct.
- Preserve meaningful source classes, including `other`, `not_relevant`, or abstention when needed. Do not silently collapse a nuanced scale into generic positive/negative/neutral labels.
- Keep option keys stable and code-friendly. Explain any mapping between source labels and API options.

## Build the smallest useful demo

- Use the OpenRouter Decisions API: `POST https://openrouter.ai/api/alpha/decisions`; name the model `typesafe/jev-1.13` unless the project explicitly chooses another supported Jev model.
- Keep credentials in `OPENROUTER_API_KEY`. Never write API keys into source, output files, or example commands.
- Prefer a short command-line or notebook path that shows one input, the typed answer, relevant probabilities, and confidence. Make examples clearly illustrative unless actually run.
- If processing a file, preserve original columns, add predictions in new columns, and include a small row limit so the first run is easy to inspect.
- Make external data submission explicit. Do not send private or sensitive records to a hosted service unless the user authorized that destination.

## Teach and evaluate

- Explain the request/response path plainly: state in, typed question, option probabilities out, application logic next.
- Separate schema validity from answer quality. Restricting output to declared options avoids malformed labels; it does not guarantee the selected answer is true.
- Treat confidence as a model signal, not accuracy. Do not claim calibration unless measured against appropriate labeled examples.
- Evaluate on a human-reviewed holdout set shared by Jev and any baseline. Report class counts and per-class metrics (such as precision/recall and macro-F1); inspect disagreements and label ambiguity.
- Distinguish the decision-model/API contribution from a full application. Jev returns decisions; application code still defines thresholds, fallbacks, and actions.

For this repository's historical example, read [`jev/CONCEPTS.md`](../../../jev/CONCEPTS.md) when adapting the tweet task or discussing its original six classes. The original notebook and annotated dataset are at the repository root.
To see the skill applied to this exact sentiment use case, follow [`jev/SKILL_DEMO.md`](../../../jev/SKILL_DEMO.md). Keep the skill general; keep dataset-specific labels and criteria in the project.

## Be precise about the model

Call this model TypeSafe's Jev and identify the `typesafe/jev-1.13` model ID. Do not call it OpenJev or imply that Jev is open source. Jev is accessed through OpenRouter and usage is billed to the account associated with the API key. Verify current provider documentation when model IDs or API contracts may have changed.
