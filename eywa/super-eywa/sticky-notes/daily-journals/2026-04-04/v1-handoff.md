# V1 Handoff

## Purpose

This doc is the review handoff for the autonomous Super-Eywa v1 build pass.

It will be updated with:

- what was built
- how to run it
- what was tested
- what still needs review

## Status

- Ready for review.

## Current Built Pieces

- deterministic Eywa v1 runtime
- live OpenRouter Eywa v1 runtime
- contract validators
- file-first run writer
- story/timeline generation
- variable defaults
- runtime unit tests
- grading parser/grader tests
- run validator in `data-system/correctness-suite/`
- grading-bank runner in `data-system/grading/run_test_question_v1.py`
- live baseline/main batch runner in `data-system/grading/run_live_batch_v1.py`
- one smoke run under `data-system/run-history/run_2026_04_04_smoke/`
- one live smoke run under `data-system/run-history/run_live_smoke_single_01/`
- one completed live grading batch under `data-system/grading/runs/live-batch-v1-summary.json`

## Current Commands

Deterministic run:

```bash
python3 eywa-system/runtime/run_v1.py --task "Design the backend and build the frontend and validate the feature."
```

Live run:

```bash
python3 eywa-system/runtime/run_v1.py \
  --task "For each n, let k(n) be the number of ones in the binary representation of 2023*n. Find the minimum k(n)." \
  --runtime-provider openrouter \
  --model openai/gpt-4.1-mini
```

Test:

```bash
python3 -m unittest discover -s eywa-system/runtime/tests -p 'test_*.py'
```

Grading tests:

```bash
python3 -m unittest discover -s data-system/grading/tests -p 'test_*.py'
```

Validate stored run:

```bash
python3 data-system/correctness-suite/validate_run_v1.py data-system/run-history/run_2026_04_04_smoke
```

Run one grading-bank question:

```bash
python3 data-system/grading/run_test_question_v1.py \
  --question-file data-system/grading/test-questions/architecture-derived-B6-binary-representation-minimization.md \
  --label baseline \
  --runtime-provider openrouter \
  --model openai/gpt-4.1-mini \
  --max-depth 0
```

Run the first live batch:

```bash
python3 data-system/grading/run_live_batch_v1.py \
  --runtime-provider openrouter \
  --model openai/gpt-4.1-mini
```

## What Was Tested

- syntax check with `python3 -m py_compile`
- unit tests with `python3 -m unittest discover -s eywa-system/runtime/tests -p 'test_*.py'`
- grading tests with `python3 -m unittest discover -s data-system/grading/tests -p 'test_*.py'`
- smoke run with `run_v1.py`
- stored-run validation against the smoke run
- live OpenRouter smoke run
- 5 baseline grading-bank live runs
- 5 main grading-bank live runs

## First Live Batch Snapshot

- main runs completed: `5`
- baseline runs completed: `5`
- clean single-node success:
  - `architecture-derived-B6-binary-representation-minimization`
- clean delegated success:
  - `architecture-derived-B11-board-game-rule-chaining`
- delegated but still wrong:
  - `architecture-derived-B4-hensel-lifting-verification`
  - `architecture-derived-B10-mean-field-lattice-gas-occupancy`
- summary artifact:
  - `data-system/grading/runs/live-batch-v1-summary.json`

## Presentation

- presentation folder:
  - `/Users/seanross/kingdom_of_god/home-base/presentation_hub/super-eywa-first-live-pass-2026-04-04/`
- main file:
  - `/Users/seanross/kingdom_of_god/home-base/presentation_hub/super-eywa-first-live-pass-2026-04-04/presentation.html`

## What Still Needs Review

- whether `final_action_type` is the right way to represent final node semantics
- whether the multi-step root-node behavior should stay hidden in replay or become more explicit in core records
- whether the deterministic executor’s decomposition heuristic is the right first default
- whether the current file layout is calm enough for long-term human browsing
- how grading-bank question files should evolve from summary cases to richer runnable packets
- whether delegation should stay code-driven or become more variable/model-driven
