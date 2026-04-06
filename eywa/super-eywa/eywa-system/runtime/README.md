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
- prompt families now include `none`, `execute`, `transmute`, `delegate`, and `agent_chooses`
- `selected_prompt_text` is the main per-node prompt body when explicitly set
- `review_prompt_family` and `review_selected_prompt_text` can switch the same node into a different prompt mode once child results return
- `base_header_prompt` is an optional prefix and currently defaults to blank
- additional instruction prompt profiles can still be layered through run variables as supplemental guidance
- live provider request/response payloads are written into replay
