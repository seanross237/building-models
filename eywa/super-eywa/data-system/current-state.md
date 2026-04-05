# Data System — Current State

Current state right now:

- the data-system target docs are filled in
- the grading area has been organized into a cleaner structure
- the first implementation-facing folders exist
- the first v1 run-history layout doc exists
- a first preserved run-history implementation now exists
- a first correctness validator now exists
- a first grading-bank runner now exists
- a first live baseline/main grading batch now exists

Current folders:

- `grading/`
- `run-history/`
- `derived-views/`
- `correctness-suite/`

Current correctness utility:

- `correctness-suite/validate_run_v1.py`

Current grading utilities:

- `grading/run_test_question_v1.py`
- `grading/run_live_batch_v1.py`

The current phase is:

- refine the preserved run-history implementation
- keep correctness and grading separate from the start
- grow correctness beyond layout validation into richer run checks
- evolve grading-bank cases from summary markdown into richer runnable packets
