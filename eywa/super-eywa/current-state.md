# Super-Eywa — Current State

Current state right now:

- the root target docs are filled in
- the Eywa target docs are filled in
- the data-system target docs are filled in
- the grading question bank has been reorganized cleanly
- the first implementation-facing folders have been scaffolded
- the first Eywa contract files have been defined
- the first v1 run-history layout doc has been defined
- a live OpenRouter runtime path now exists
- the first grading-bank runner now exists
- the first live baseline/main batch has been completed

What exists now:

- `eywa-system/`
  - target docs
  - initial folders for contracts, runtime, variables, and story view
  - concrete contract docs for run packet, node packet, node output, and node record
  - a deterministic Python v1 runtime
  - a live OpenRouter v1 runtime path
  - unit tests for runtime writing and validation
- `data-system/`
  - target docs
  - grading structure
  - initial folders for run history, derived views, and correctness suite
  - a v1 run-history layout doc
  - a first preserved run-history implementation
  - a first correctness validator for stored runs
  - a grading-bank runner
  - a live baseline/main batch summary

What does not exist yet:

- real database or derived-table pipeline
- dry-run correctness machinery

The current phase is:

- refine the live Eywa runtime implementation
- refine the grading-bank question packets and graders
- improve delegation quality beyond structural success
- grow correctness from layout validation toward real dry-run checks
