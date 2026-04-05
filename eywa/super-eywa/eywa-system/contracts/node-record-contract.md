# Node Record Contract

## Purpose

The `node_record` is the canonical preserved record of a node run.

It is the clean, readable core record that later analysis should start from.

## Required Fields

- `contract_name`
  - always `node_record`
- `contract_version`
  - starting at `v1`
- `run_id`
- `node_id`
- `state`
- `final_action_type`
- `input`
- `variables`
- `orchestration`
- `prompt`
- `results`
- `logging`
- `replay_ref`

## Field Details

### `state`

For v1, the core lifecycle state values should be:

- `created`
- `running`
- `completed`
- `system_error`

These are runtime lifecycle states, not semantic success/problem labels.

The semantic outcome of the node should be visible in:

- `results`
- `final_action_type`

### `final_action_type`

This preserves the final human-facing action label for the node run.

For v1, it should be one of:

- `local_attempt`
- `local_replan`
- `recruit_help`
- `report_success`
- `report_problem`

### `input`

This should preserve the same input object that appeared in the `node_packet`.

### `variables`

This should preserve the node's fully resolved variables.

In the current runtime this includes fields such as:

- `injected_prompt_profile`
- `additional_instruction_prompt_profiles`
- `json_response_policy`
- `orchestration_policy`
- `budget_policy`

### `prompt`

This should preserve the actual prepared prompt packet the node was given.

Required fields:

- `rendered_prompt_text`
- `prompt_artifact_refs`

### `orchestration`

This preserves the decision summary for the node across its authored turns.

Required fields:

- `turn_count`
- `initial_decision`
- `final_decision`
- `decision_notes`
- `helper_count`

Allowed decision values for v1:

- `execute_locally`
- `delegate`
- `report_problem`

### `results`

This should preserve the authored results from the node output.

### `logging`

This should be the umbrella category for:

- `metrics`
- `events_ref`
- `edges_ref`

#### `metrics`

For v1, metrics should preserve fields such as:

- `input_tokens`
- `output_tokens`
- `total_tokens`
- `cost_usd`
- `wall_time_ms`

### `replay_ref`

This should point to the heavier replay material for the node run.

That replay material stays separate so the core node record remains readable.

## Example Shape

```json
{
  "contract_name": "node_record",
  "contract_version": "v1",
  "run_id": "run_2026_04_04_001",
  "node_id": "node_root",
  "state": "completed",
  "final_action_type": "report_success",
  "input": {
    "instructions": "Build me feature X.",
    "provided_context_refs": [],
    "attachment_refs": []
  },
  "variables": {
    "model": "gpt-5.4",
    "injected_prompt_profile": "agent_orchestration_basic_instruction_prompt",
    "additional_instruction_prompt_profiles": [
      "double_check_reasoning_prompt"
    ],
    "context_policy": "minimal",
    "workflow_structure": "sequential_parent_review",
    "verification_policy": "light",
    "json_response_policy": "strict_required",
    "orchestration_policy": "agent_decides",
    "routing_policy": "return_to_creator"
  },
  "orchestration": {
    "turn_count": 2,
    "initial_decision": "delegate",
    "final_decision": "execute_locally",
    "decision_notes": "Child results were sufficient to finish locally.",
    "helper_count": 2
  },
  "prompt": {
    "rendered_prompt_text": "You are working on feature X...",
    "prompt_artifact_refs": []
  },
  "results": [
    {
      "result_type": "plan",
      "content": "Split feature X into backend, frontend, and validation work.",
      "attachment_refs": []
    }
  ],
  "logging": {
    "metrics": {
      "input_tokens": 1200,
      "output_tokens": 220,
      "total_tokens": 1420,
      "cost_usd": 0.012,
      "wall_time_ms": 18000
    },
    "events_ref": "events.jsonl",
    "edges_ref": "edges.json"
  },
  "replay_ref": "replay/run-001/node-root/"
}
```

## Notes

- the node record is the main readable truth
- replay stays linked but separate and should preserve raw authored JSON turns
- this shape should be easy for both humans and derived tables to consume
