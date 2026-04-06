# Variables

This folder is for the Eywa variable surface.

It should hold the variable schema, variable family definitions, and later the resolved-variable machinery that Eywa nodes run with.

The current runtime expects the variable surface to control:

- which prompt family a node runs under
- which exact prompt text is injected for that node
- which prompt family and prompt text a node uses on child-review turns
- which child prompt family and child prompt text are inherited by downstream nodes
- which additional instruction prompt profiles are layered on top
- how many helper nodes and authored decision turns are allowed
- how nodes recover from invalid authored JSON

Current v1 files:

- `default-run-level-variables.json`
- `variable-schema-v1.md`
- `prompt-profiles/`

Prompt profile note:

- prompt families and selected prompt text are now the main orchestration-prompt surface
- the runtime still uses in-code prompt profile text from `eywa-system/runtime/eywa_runtime/prompting.py` for supplemental guidance
- the markdown files in `prompt-profiles/` are the human-readable mirrors of those supplemental profiles and should be kept aligned
