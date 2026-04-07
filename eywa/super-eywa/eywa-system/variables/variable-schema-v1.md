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
- `prompt_family`
- `selected_prompt_text`
- `base_header_prompt`
- `review_prompt_family`
- `review_selected_prompt_text`
- `review_base_header_prompt`
- `child_prompt_family`
- `child_selected_prompt_text`
- `child_base_header_prompt`
- `submission_contract_type`
- `submission_entry_file`
- `terminal_result_destination`
- `child_terminal_result_destination`
- `injected_prompt_profile`
- `additional_instruction_prompt_profiles`
- `context_policy`
- `workflow_structure`
- `verification_policy`
- `tool_policy`
- `json_response_policy`
- `orchestration_policy`
- `budget_policy`
- `routing_policy`
- `recovery_policy`

## Notes

- this is a starting schema, not the final variable taxonomy
- the runtime currently uses only a subset of these fields in behavior
- `runtime_provider` currently supports `deterministic` and `openrouter`
- `budget_policy.max_depth` is hard-capped to `3` in runtime code to prevent runaway recursion
- `budget_policy.max_turns_per_node` limits how many authored decision turns one node may take before runtime stops it
- `prompt_family` now controls the main orchestration-prompt family for a node
- supported prompt families now include `execute`, `delegate`, `transmute`, `review`, `none`, and `agent_chooses`
- `selected_prompt_text` is the actual prompt text injected before the question when explicitly set
- `base_header_prompt` is an optional fixed header injected before the selected prompt and currently defaults to blank
- `review_*` variables let a node switch prompt behavior on a later child-review turn without changing the first-turn prompt
- `child_prompt_family` and related child prompt variables let parent-created nodes inherit a different prompt setup
- `submission_contract_type` lets execute turns switch from plain-text answer submission to a stricter artifact submission contract such as a single Python file
- `submission_entry_file` names the primary artifact expected by that contract, such as `main.py`
- `terminal_result_destination` controls whether a node's terminal answer goes to its creator or to the run's canonical `final_output` artifact
- `child_terminal_result_destination` lets parent-created nodes inherit a different terminal destination
- `injected_prompt_profile` is now legacy support for older prompt-profile experiments
- node-authored responses are now expected to be JSON with an always-present `orchestration_decision`
- preserving the full resolved variable set still matters even before each field is deeply used
