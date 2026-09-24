---
name: openjev-decision-lab
description: Build a small OpenJev-compatible typed-decision demo from a real task, with an explicit label map and a grounded evaluation plan. Use for fixed-choice classification, ordinal scoring, or yes/no decisions; use a generative model when the task needs free-form text.
---

# OpenJev Decision Lab

Turn a concrete decision task into a small, understandable OpenJev-compatible example and explain what its outputs do and do not establish.

## Shape the decision

- Start from the user's actual task and inspect the input fields and labels before choosing a schema.
- Use `choice` for mutually exclusive categories, `score` for an ordered scale, and `noul` for a yes/no judgment. Keep the question narrow and the option descriptions distinct.
- Preserve meaningful source classes, including `other`, `not_relevant`, or abstention when the task needs them. Do not silently collapse a nuanced scale into generic positive/negative/neutral labels.
- Keep option keys stable and code-friendly. Explain any mapping between source labels and API options.

## Build the smallest useful demo

- Use the service endpoint and request contract configured by the project. OpenJev-compatible services can differ in model names, hosting, authentication, and limits; check the chosen provider's current docs.
- Keep credentials in environment variables. Never write API keys into source, output files, or example commands.
- Prefer a short command-line or notebook path that shows one input, the typed answer, all relevant probabilities, and confidence. Make examples clearly illustrative unless they were actually run.
- If processing a file, preserve its original columns, add predictions in new columns, and include a small row limit so the first run is easy to inspect.
- Make external data submission explicit. Do not send private or sensitive records to a hosted service unless the user authorized that destination.

## Teach and evaluate

- Explain the request/response path in plain language: state in, typed question, option probabilities out, application logic next.
- Separate schema validity from answer quality. Restricting output to declared options avoids malformed labels; it does not guarantee the chosen answer is true.
- Treat confidence as a model signal, not accuracy. Do not claim calibration unless it was measured against appropriate labeled examples.
- For evaluation, use a human-reviewed holdout set shared by the new approach and any baseline. Report class counts and per-class metrics (such as precision/recall and macro-F1); inspect disagreements and label ambiguity.
- Distinguish the decision-model/API contribution from a full application. The service returns decisions; application code still defines thresholds, fallbacks, and actions.

For this repository's historical example, read [`openjev/CONCEPTS.md`](../../../openjev/CONCEPTS.md) when adapting the tweet task or discussing its original six classes. The original notebook and annotated dataset are at the repository root.

## Be precise about Jev and OpenJev

TypeSafe's Jev and independently developed OpenJev implementations share a typed-decision API pattern, but they are not the same model, service, weights, or training method. Name the exact endpoint/model used in code and in performance claims. Do not imply endorsement or affiliation.
