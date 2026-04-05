# File Hierarchies For Review

## Repo Root

```text
super-eywa/
  AGENTS.md
  CLAUDE.md
  high-level-north-star.md
  detailed-target-state.md
  current-state.md
  eywa-system/
  data-system/
  sticky-notes/
  mission-runs/
  archive/
  the-do-queue/
```

## Eywa Runtime

```text
eywa-system/runtime/
  README.md
  run_v1.py
  eywa_runtime/
    __init__.py
    contracts.py
    defaults.py
    engine.py
    executor.py
    ids.py
    openrouter_client.py
    prompting.py
    secrets.py
    storage.py
    story.py
    validation.py
  tests/
    test_runtime.py
    test_validation.py
```

## Grading Area

```text
data-system/grading/
  README.md
  all-test-questions.md
  run_test_question_v1.py
  run_live_batch_v1.py
  test-questions/
    ... question files ...
  question-types/
    atlas-derived/
    architecture-derived/
    coding/
  grading_methods/
    README.md
    simple_grade_v1.py
  tests/
    test_simple_grade_v1.py
  runs/
    live-batch-v1-summary.json
    architecture-derived-B4-hensel-lifting-verification/
    architecture-derived-B5-combinatorial-probability-random-chords/
    architecture-derived-B6-binary-representation-minimization/
    architecture-derived-B10-mean-field-lattice-gas-occupancy/
    architecture-derived-B11-board-game-rule-chaining/
  benchmarks/
    README.md
```

## Sample Stored Run

Example:

- `data-system/run-history/architecture-derived-B11-board-game-rule-chaining__main__run_2026_04_04_134739/`

```text
run/
  run_packet.json
  run_summary.json
  events/
    run-events.jsonl
  derived/
    simple-run-row.json
    timeline.json
    timeline.md
  nodes/
    node_root/
      node_packet.json
      node_record.json
      events.jsonl
      edges.json
    node_root_helper_01/
      ...
    node_root_helper_02/
      ...
    node_root_helper_02_helper_01/
      ...
    node_root_helper_02_helper_02/
      ...
  replay/
    node_root/
      raw-model.json
      prompt-snapshot.json
      tool-transcript.jsonl
    node_root_helper_01/
      ...
    node_root_helper_02/
      ...
    node_root_helper_02_helper_01/
      ...
    node_root_helper_02_helper_02/
      ...
```
