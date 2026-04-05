# Variables

This folder is for the Eywa variable surface.

It should hold the variable schema, variable family definitions, and later the resolved-variable machinery that Eywa nodes run with.

The current runtime expects the variable surface to control:

- which orchestration prompt profile is injected
- which additional instruction prompt profiles are layered on top
- how many helper nodes and authored decision turns are allowed
- how nodes recover from invalid authored JSON

Current v1 files:

- `default-run-level-variables.json`
- `variable-schema-v1.md`
- `prompt-profiles/`

Prompt profile note:

- the runtime currently uses in-code prompt profile text from `eywa-system/runtime/eywa_runtime/prompting.py`
- the markdown files in `prompt-profiles/` are the human-readable mirrors of those profiles and should be kept aligned
