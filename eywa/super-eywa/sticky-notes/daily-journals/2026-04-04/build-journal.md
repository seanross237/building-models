# 2026-04-04 Build Journal

## Purpose

This journal tracks the autonomous Super-Eywa v1 build pass.

It is the main running log for:

- implementation progress
- non-obvious decisions
- uncertainties encountered during build
- what was tested

## Build Log

### 1. Start

- Confirmed target docs and contracts exist.
- Confirmed `super-eywa` has no real runtime implementation yet.
- Chose a small Python stdlib implementation for v1 to keep setup simple and testable.
- Chose file-first storage under `data-system/run-history/` following `run-layout-v1.md`.
- Chose a deterministic local executor for v1 so the system is runnable without external model keys.

### 2. First Runtime Pass

- Implemented a deterministic Python runtime under `eywa-system/runtime/eywa_runtime/`.
- Added a CLI entry point at `eywa-system/runtime/run_v1.py`.
- Added contract validators for run packet, node packet, node output, and node record.
- Added file-first run writing under `data-system/run-history/`.
- Added a basic story/timeline generator.

### 3. Testing And Smoke Run

- Ran syntax check with `python3 -m py_compile`.
- Ran unit tests with `python3 -m unittest discover -s eywa-system/runtime/tests -p 'test_*.py'`.
- Ran a smoke test into `data-system/run-history/run_2026_04_04_smoke/`.
- Found one issue: the timeline was written before the final `run_completed` event.
- Fixed that ordering issue.

### 4. Correctness Validator

- Added `data-system/correctness-suite/validate_run_v1.py`.
- Added a validation helper in the runtime package.
- Added a unit test that validates a generated run directory.
- Ran the validator successfully against `run_2026_04_04_smoke`.

### 5. Review State

- Removed generated `__pycache__` directories to keep the tree clean.
- Left one smoke run on disk for review:
  - `data-system/run-history/run_2026_04_04_smoke/`
- Current state: v1 is runnable, tested, documented, and reviewable.

### 6. Next Scope Captured

- Added `live-model-runs-and-presentation-plan.md` to capture the next requested scope before continuing.
- This includes:
  - live-model integration
  - 5 successful real runs
  - baseline runs
  - depth cap 3
  - final presentation requirements

### 7. Live Provider Integration

- Added a live OpenRouter executor behind the same runtime seam as the deterministic executor.
- Added provider selection through run-level variables:
  - `runtime_provider`
  - `model`
- Added replay capture for:
  - raw request body
  - raw response body
  - provider usage details
- Added `.env` fallback loading so Super-Eywa can reuse the existing `../open-eywa/.env` key source.
- Kept deterministic mode working.

### 8. Live Runtime Fixes

- Found and fixed a usage-merging bug that would have double-counted tokens/cost if both chat-completion usage and generation stats were present.
- Enforced a hard recursion cap of `3` in runtime code even if higher values are requested.
- Widened the decomposition splitter to catch:
  - `and`
  - `;`
  - `Then`
  - bullet lists
  - numbered lists
- Found and fixed a second bug where the engine computed subtasks correctly but still failed to branch because it used a separate inconsistent decomposition gate.

### 9. Grading-Bank Runner

- Added a simple grading-bank runner:
  - `data-system/grading/run_test_question_v1.py`
- Added a small grading helper module:
  - `data-system/grading/grading_methods/simple_grade_v1.py`
- Added a batch runner for the first live evaluation pass:
  - `data-system/grading/run_live_batch_v1.py`
- Added grading parser/grader tests under:
  - `data-system/grading/tests/`

### 10. Live Runs Completed

- Completed `5` main live grading runs.
- Completed matching baseline runs for those same `5` questions.
- Confirmed:
  - at least one successful single-node live run
  - at least one successful delegated live run
- Stored the batch summary at:
  - `data-system/grading/runs/live-batch-v1-summary.json`

### 11. Current Review State

- Runtime tests pass.
- Grading tests pass.
- Live provider runs are working.
- The system now has:
  - deterministic runtime mode
  - live OpenRouter runtime mode
  - grading-bank runner
  - baseline/main batch runner
  - stored live run artifacts ready for presentation
