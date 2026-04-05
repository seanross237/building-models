# Variable Schema V1

## Purpose

This doc records the first concrete variable surface used by the Super-Eywa v1 runtime.

It is intentionally small.

## Run-Level Defaults

The default run-level variables currently live in:

- `default-run-level-variables.json`

## Current V1 Fields

- `model`
- `runtime_provider`
- `injected_prompt_profile`
- `context_policy`
- `workflow_structure`
- `verification_policy`
- `tool_policy`
- `budget_policy`
- `routing_policy`
- `recovery_policy`

## Notes

- this is a starting schema, not the final variable taxonomy
- the runtime currently uses only a subset of these fields in behavior
- `runtime_provider` currently supports `deterministic` and `openrouter`
- `budget_policy.max_depth` is hard-capped to `3` in runtime code to prevent runaway recursion
- preserving the full resolved variable set still matters even before each field is deeply used
