# What the Jev example is doing

This companion keeps the original question—what opinions do people express about self-driving cars?—and changes the method from a trained embedding/CNN pipeline to a call to TypeSafe's Jev decision model.

## Follow one request

1. `classify()` takes one tweet and puts it in a `state` object.
2. `LABELS` defines the six possible answers and explains how they map to the original labels.
3. The client sends one typed `choice` question to OpenRouter's Decisions API.
4. Jev returns a selected option, probabilities, and confidence. Python checks the answer and prints it as JSON.

There is no generated paragraph to parse. The schema limits the answer to the choices in `LABELS`. That makes the output shape predictable; it does not guarantee the classification is correct.

## Follow a CSV

`analyze_csv()` reads the chosen text column, calls Jev for each non-empty row, and writes a new CSV. It copies the original columns unchanged and adds the selected class, confidence, and per-class probabilities. `--limit` lets you try a few rows before sending a larger file.

## Questions to keep in mind

- The old annotation scale is not a generic positive/negative/neutral taxonomy. The six options retain its broad structure, but the descriptions are a teaching choice; review the original rubric before claiming exact equivalence.
- A model's confidence is not measured accuracy. Compare predictions with human-reviewed examples before drawing performance conclusions.
- The API result is a zero-shot baseline. The original trained CNN and Jev have different data, assumptions, and deployment costs.
- The sample tweets are invented for exploration. They are not labeled evaluation data.
- Tweets from the original dataset are sent to OpenRouter when analyzed. Don't send sensitive data, and remember that each row makes a separately billed request.
