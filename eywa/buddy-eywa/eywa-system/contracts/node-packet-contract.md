# Node Packet Contract

## Purpose

The `node_packet` is the frozen starting package for one node run.

It preserves exactly what that node was given when it started.

It should be created before node execution begins and then treated as immutable.

## Required Fields

- `contract_name`
  - always `node_packet`
- `contract_version`
  - starting at `v1`
- `run_id`
- `node_id`
- `created_at_utc`
- `creation_parent_node_id`
- `input`
- `variable_resolution`
- `node_setup`

## Field Details

### `input`

The `input` object preserves the node's assignment package.

Required fields:

- `instructions`
- `provided_context_refs`
- `attachment_refs`

### `variable_resolution`

This preserves how the node's variables were resolved.

Required fields:

- `run_level_defaults`
- `node_level_overrides`
- `resolved_variables`

The most important field is `resolved_variables`.

That is the full behavior-shaping variable set the node actually ran with.

### `node_setup`

This preserves node-specific setup facts.

Required fields:

- `created_by_action_type`
- `notes`

## Example Shape

```json
{
  "contract_name": "node_packet",
  "contract_version": "v1",
  "run_id": "run_2026_04_04_001",
  "node_id": "node_root",
  "created_at_utc": "2026-04-04T12:00:00Z",
  "creation_parent_node_id": null,
  "input": {
    "instructions": "Build me feature X.",
    "provided_context_refs": [],
    "attachment_refs": []
  },
  "variable_resolution": {
    "run_level_defaults": {
      "model": "gpt-5.4",
      "context_policy": "minimal"
    },
    "node_level_overrides": {},
    "resolved_variables": {
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
      },
      "routing_policy": "return_to_creator"
    }
  },
  "node_setup": {
    "created_by_action_type": null,
    "notes": []
  }
}
```

## Notes

- `creation_parent_node_id` is about origin, not output destination
- routing behavior belongs in resolved variables, not in a separate hard-coded field
- the node packet preserves variable-selected prompt behavior, but not the rendered turn prompt itself
- this packet should be enough to understand the node in isolation

## Planned Buddy-Eywa Extensions

These fields are not yet part of the contract. They will land in later sections of the buddy-eywa build:

- **`input.artifact_refs`** (added in Section 5 — engine part 1) — list of artifact IDs the engine loads into the worker's prompt at materialization time
- **`node_setup.subgraph_instance_id`** (added in Section 6 — engine part 2) — the subgraph instance this node belongs to, so records can be grouped by instance
- **`node_setup.inputs_from`** (added in Section 6 — engine part 2) — resolved upstream slot node IDs whose outputs feed into this node's input, derived from the subgraph type's edges
