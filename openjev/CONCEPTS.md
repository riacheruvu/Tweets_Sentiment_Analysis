# What the OpenJev example is doing

This companion keeps the original question—what opinions do people express about self-driving cars?—but replaces a task-specific embedding/CNN pipeline with a call to an OpenJev-compatible decision API.

## Follow one request

1. `classify()` takes one tweet as `state`.
2. `LABELS` defines the six possible answers. The keys become the return values; the descriptions explain how the options map to the original dataset's 1–5 scale and `not_relevant` class.
3. The client sends one `choice` question to `POST /v1/systemone`.
4. OpenJev returns the selected option, probabilities for each option, and confidence. The Python code checks the response and prints it as JSON.

There is no generated paragraph to parse. The schema limits the answer to the choices in `LABELS`. That makes the output shape predictable; it does not make the classification automatically correct.

## Follow a CSV

`analyze_csv()` reads the chosen text column, calls `classify()` for each non-empty row, and writes a new CSV. It copies the original columns through unchanged and adds the selected class, confidence, and per-class probabilities. `--limit` makes it possible to try a few rows before sending a larger file.

## Questions to keep in mind

- The old annotation scale is not a generic positive/negative/neutral taxonomy. The six options retain its broad structure, but the descriptions are a teaching choice; review the original annotation rubric before claiming exact equivalence.
- A model's confidence is not measured accuracy. Compare predictions with human-reviewed examples before drawing performance conclusions.
- The API result is a zero-shot baseline. The original trained CNN and this pretrained decision service have different data, assumptions, and deployment costs.
- The sample tweets are invented for exploration. They are not labeled evaluation data.
