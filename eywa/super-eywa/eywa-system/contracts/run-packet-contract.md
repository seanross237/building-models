# Run Packet Contract

## Purpose

The `run_packet` is the frozen starting package for a whole Eywa run.

It preserves the top-level assignment and run-level setup facts.

It should be created at run start and then treated as immutable.

## Required Fields

- `contract_name`
  - always `run_packet`
- `contract_version`
  - starting at `v1`
- `run_id`
- `created_at_utc`
- `root_node_id`
- `task`
- `run_level_variables`
- `top_level_context`
- `root_setup`

## Field Details

### `task`

The `task` object preserves the original top-level assignment.

Required fields:

- `raw_task_text`
- `task_source`
- `constraints`
- `success_criteria`
- `attachment_refs`

### `run_level_variables`

This object preserves the run-level variables that apply across the run unless overridden later.

It should store the resolved run-level values, not vague descriptions.

### `top_level_context`

This preserves any top-level context explicitly attached to the run.

Examples:

- top-level summaries
- files
- URLs
- operator notes

### `root_setup`

This preserves facts about how the root node was initialized.

Required fields:

- `root_input_summary`
- `notes`

## Example Shape

```json
{
  "contract_name": "run_packet",
  "contract_version": "v1",
  "run_id": "run_2026_04_04_001",
  "created_at_utc": "2026-04-04T12:00:00Z",
  "root_node_id": "node_root",
  "task": {
    "raw_task_text": "Build me feature X.",
    "task_source": "sean_direct_request",
    "constraints": [],
    "success_criteria": [],
    "attachment_refs": []
  },
  "run_level_variables": {
    "model": "gpt-5.4",
    "injected_prompt_profile": "agent_orchestration_basic_instruction_prompt",
    "additional_instruction_prompt_profiles": [],
    "context_policy": "minimal",
    "workflow_structure": "sequential_parent_review",
    "verification_policy": "light",
    "json_response_policy": "strict_required",
    "orchestration_policy": "agent_decides",
    "budget_policy": {
      "max_depth": 3,
      "max_helpers_per_node": 3,
      "max_turns_per_node": 4
    }
  },
  "top_level_context": {
    "context_refs": []
  },
  "root_setup": {
    "root_input_summary": "Direct top-level feature build request.",
    "notes": []
  }
}
```

## Notes

- the run packet is setup truth, not outcome truth
- scores do not belong here
- node-specific resolved variables do not belong here
- prompt-profile selection belongs here, but the actual rendered turn prompt belongs in node records and replay
