# Super-Eywa V1 Presentation Brief

## Purpose

This brief is for the presentation about the first runnable and live-tested Super-Eywa v1.

The deck should explain:

- what was built
- how it works
- how to run it
- how a run unfolds step by step
- how data is stored
- what the live test runs showed
- what judgment calls were made
- what questions remain
- what recommendations came out of the first live pass

## Required Inputs

- `high-level-north-star.md`
- `detailed-target-state.md`
- `current-state.md`
- `eywa-system/current-state.md`
- `data-system/current-state.md`
- `eywa-system/runtime/README.md`
- `data-system/grading/README.md`
- `sticky-notes/daily-journals/2026-04-04/live-run-results-summary.md`
- `sticky-notes/daily-journals/2026-04-04/file-hierarchies-for-review.md`
- `sticky-notes/daily-journals/2026-04-04/build-journal.md`
- `sticky-notes/daily-journals/2026-04-04/implementation-questions-and-judgment-calls.md`
- `sticky-notes/daily-journals/2026-04-04/v1-handoff.md`

## Must Show

- file hierarchies
- run-history storage layout
- single-node path
- delegated path
- baseline vs main run results
- where the grading-bank runner lives
- where replay artifacts live
- how the data ended up being stored

## Live Batch Facts

- model: `openai/gpt-4.1-mini`
- runtime provider: `openrouter`
- baseline mode: `max_depth = 0`
- main mode: `max_depth = 3`
- main runs completed: `5`
- baseline runs completed: `5`

## Headline Results

- `B6` was a clean single-node success in both baseline and main mode.
- `B11` was a clean delegated success in main mode.
- `B4` and `B10` showed that delegation is structurally working before it is reliably improving answer quality.
- The question bank is only partly runnable right now.

## Presentation Tone

- dark themed
- sparse
- visual
- background images
- more “system briefing” than “dense technical report”

## Useful Paths

- first live smoke run:
  - `data-system/run-history/run_live_smoke_single_01/`
- live batch summary:
  - `data-system/grading/runs/live-batch-v1-summary.json`
- run-history root:
  - `data-system/run-history/`
- grading run records:
  - `data-system/grading/runs/`
