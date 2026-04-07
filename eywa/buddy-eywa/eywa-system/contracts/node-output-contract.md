# Node Output Contract

## Purpose

The `node_output` is the structured runtime-compiled output of a node execution.

It is derived from the node-authored JSON response after runtime validation.

The node does not author `node_output` directly.

The runtime authors this object after it decides that the node-authored JSON was legal for the current turn.

## Required Fields

- `contract_name`
  - always `node_output`
- `contract_version`
  - starting at `v1`
- `run_id`
- `node_id`
- `action_type`
- `results`
- `outgoing_packets`

## Action Type

For v1, the allowed `action_type` values are:

- `local_attempt`
- `local_replan`
- `recruit_help`
- `report_success`
- `report_problem`

## Results

The `results` field is a list of compiled work-result objects.

Each result object should preserve:

- `result_type`
- `content`
- `attachment_refs`

Examples of `result_type`:

- `answer`
- `plan`
- `summary`
- `code_patch`
- `failure_explanation`

## Outgoing Packets

The `outgoing_packets` field is a list of structured packets to intended targets.

Each outgoing packet should preserve:

- `message_type`
- `target`
- `message`
- `attachment_refs`

### Allowed `message_type` Values For V1

- `helper_assignment`
- `work_result`
- `replan_message`
- `success_report`
- `problem_report`

### `target` Shape

For v1, the `target` object should preserve:

- `target_type`
- `target_ref`

Allowed `target_type` values for v1:

- `creating_parent`
- `existing_node`
- `new_helper`

## Example Shape

```json
{
  "contract_name": "node_output",
  "contract_version": "v1",
  "run_id": "run_2026_04_04_001",
  "node_id": "node_root",
  "action_type": "recruit_help",
  "results": [
    {
      "result_type": "plan",
      "content": "Split feature X into backend, frontend, and validation work.",
      "attachment_refs": []
    }
  ],
  "outgoing_packets": [
    {
      "message_type": "helper_assignment",
      "target": {
        "target_type": "new_helper",
        "target_ref": "helper_backend"
      },
      "message": "Implement the backend changes needed for feature X.",
      "attachment_refs": []
    },
    {
      "message_type": "helper_assignment",
      "target": {
        "target_type": "new_helper",
        "target_ref": "helper_frontend"
      },
      "message": "Implement the frontend changes needed for feature X.",
      "attachment_refs": []
    }
  ]
}
```

## Notes

- this is runtime-compiled output, not raw node-authored JSON
- the raw node-authored JSON belongs in replay and should match the worker-node or buddy-node authored response contracts
- metrics, events, and edges are derived by the system from execution and output handling

---

> *No buddy-eywa-specific additions planned for v1. This contract is reused as-is from the super-eywa shape.*
