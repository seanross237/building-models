# Node Authored Response Contract

## Purpose

The `node_authored_response` is the JSON object the model must return on every node turn.

It is the protocol boundary between:

- model-authored orchestration judgment
- runtime-authored graph realization

The runtime validates this object before it creates helper nodes, packets, edges, or final node outputs.

## Required Fields

- `schema_name`
  - always `eywa_node_response`
- `schema_version`
  - starting at `v1`
- `orchestration_decision`

## Allowed `orchestration_decision` Values

- `execute_locally`
- `delegate`
- `report_problem`

## Common Optional Fields

- `decision_notes`
  - short explanation of why the node chose this decision

## `execute_locally` Shape

Required extra fields:

- `response`
  - the node's real answer/result text

Optional extra fields:

- `result_type`

Example:

```json
{
  "schema_name": "eywa_node_response",
  "schema_version": "v1",
  "orchestration_decision": "execute_locally",
  "decision_notes": "The task is narrow enough to complete directly.",
  "result_type": "answer",
  "response": "FINAL_ANSWER: 42\nJUSTIFICATION: concise proof"
}
```

## `delegate` Shape

Required extra fields:

- `helpers`
  - non-empty list of helper specs

Optional extra fields:

- `synthesis_brief`

Each helper spec may include:

- `label`
- `instructions`
- `variable_overrides`

Example:

```json
{
  "schema_name": "eywa_node_response",
  "schema_version": "v1",
  "orchestration_decision": "delegate",
  "decision_notes": "The task separates into derivation and verification.",
  "helpers": [
    {
      "label": "derivation",
      "instructions": "Derive the relevant equation carefully.",
      "variable_overrides": {}
    },
    {
      "label": "verification",
      "instructions": "Check the candidate answer and edge cases.",
      "variable_overrides": {
        "verification_policy": "strict"
      }
    }
  ],
  "synthesis_brief": "Combine the helper outputs into one final answer."
}
```

## `report_problem` Shape

Required extra fields:

- `response`
  - explanation of why the node cannot proceed responsibly

Example:

```json
{
  "schema_name": "eywa_node_response",
  "schema_version": "v1",
  "orchestration_decision": "report_problem",
  "decision_notes": "The task requires external facts not present in context.",
  "response": "I cannot verify the requested claim from the information available."
}
```

## Notes

- this object must be valid JSON only, with no surrounding prose
- turn-level runtime policy may restrict which decisions are allowed on a given call
- helper count and depth are additionally constrained by runtime budget policy
- benchmark-specific answer formatting belongs inside `response`, not outside the Eywa JSON envelope
