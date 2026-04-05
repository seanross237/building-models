# Runtime

This folder is for the Eywa runtime implementation.

The runtime is now a small Python stdlib scaffold aligned with:

- `../high-level-north-star.md`
- `../detailed-target-state.md`

## Current Entry Point

- `run_v1.py`

## How To Run

From repo root:

```bash
python3 eywa-system/runtime/run_v1.py --task "Design the backend and build the frontend and validate the feature."
```

Live provider example:

```bash
python3 eywa-system/runtime/run_v1.py \
  --task "For each n, let k(n) be the number of ones in the binary representation of 2023*n. Find the minimum k(n)." \
  --runtime-provider openrouter \
  --model openai/gpt-4.1-mini
```

This writes a run under:

- `data-system/run-history/`

## How To Test

```bash
python3 -m unittest discover -s eywa-system/runtime/tests -p 'test_*.py'
```

Grading-layer tests:

```bash
python3 -m unittest discover -s data-system/grading/tests -p 'test_*.py'
```

## Notes

- v1 supports both:
  - deterministic local execution
  - live OpenRouter execution
- depth is hard-capped to `3` in runtime code
- node-authored responses are now JSON-only and must include `orchestration_decision`
- agents now decide orchestration intent; runtime validates that intent and realizes legal packets, edges, and records
- the default prompt profile is `agent_orchestration_basic_instruction_prompt`
- additional instruction prompt profiles can be layered through run variables
- live provider request/response payloads are written into replay
