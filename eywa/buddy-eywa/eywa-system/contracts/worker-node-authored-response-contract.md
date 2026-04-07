# Worker Node Authored Response Contract

## Purpose

The `worker_node_authored_response` is the JSON object a worker must return after executing its one assigned job.

It is the protocol boundary between:

- a worker's tactical execution
- the runtime's recording machinery

Workers produce their one output and stop. There is no orchestration decision branching here. Workers never choose what happens next, never propose follow-up work, and never decide whether they should be replaced or extended. Strategy is Buddy's job, exclusively.

The single escape hatch is `fail_fast`: a worker may signal that its assignment is broken or its approach cannot succeed as specified. That terminates the containing subgraph instance early and surfaces the failure to Buddy on the next turn, where Buddy decides what to do about it.

## Required Fields

- `schema_name`
  - always `worker_node_authored_response`
- `schema_version`
  - starting at `v1`
- `output`
  - the worker's actual result content
  - structured object or string, task-appropriate
  - non-empty
- `output_summary`
  - one-line description of the output
  - used in Buddy's per-turn inventory view and in the slot-execution learning surface
  - non-empty

## Common Optional Fields

- `result_type`
  - free-form short tag classifying the output (e.g., `summary | plan | code | data | finding | answer | critique | ...`)
  - loose classification only — not enforced against an enum
- `artifacts_created`
  - list of new artifact entries the worker wants the runtime to persist
  - empty list (or omitted) if the worker produced no artifacts
- `fail_fast`
  - object describing whether the worker is raising the fail-fast signal
  - omitted is equivalent to `{ "triggered": false }`

## `artifacts_created` Entry Shape

Each entry:

- `title`
  - required
  - short human-readable name (e.g., "Plan for task X")
- `type`
  - required
  - one of the allowed `artifact_record` types (see [`artifact-record-contract.md`](./artifact-record-contract.md))
- `content`
  - required
  - the raw content the runtime will write to disk
- `summary`
  - required
  - one-line hook for the artifact inventory view Buddy reads on the next turn
- `supersedes`
  - optional
  - the `artifact_id` of a prior version this replaces
  - if non-null, that prior `artifact_id` must exist in the run's artifact manifest at write time
  - omitted or `null` means this is a brand-new artifact

The runtime assigns `artifact_id`, `created_by_node_id`, `version`, `content_ref`, and `content_size_bytes` when it persists each entry as an `artifact_record` sidecar. Workers do not author those fields.

## `fail_fast` Shape

When present:

- `triggered`
  - required boolean
  - `false` is equivalent to omitting `fail_fast` entirely
  - `true` raises the signal and terminates the containing subgraph instance early
- `reason`
  - required non-empty string when `triggered` is `true`
  - explains why the assignment cannot be completed
  - must NOT propose alternatives or suggest follow-up work — strategy is Buddy's

## Example Shapes

### Success

```json
{
  "schema_name": "worker_node_authored_response",
  "schema_version": "v1",
  "output": "Timeline of the Riemann hypothesis from 1859 to 1900:\n- 1859: Riemann publishes the original paper...\n- 1896: Hadamard and de la Vallee Poussin prove the prime number theorem...\n[full timeline]",
  "output_summary": "1859-1900 Riemann hypothesis timeline with 7 key entries.",
  "result_type": "finding",
  "artifacts_created": [
    {
      "title": "Riemann hypothesis 1859-1900 timeline",
      "type": "text_markdown",
      "content": "# Riemann Hypothesis Timeline (1859-1900)\n\n- **1859**: Riemann publishes...\n[full markdown]",
      "summary": "1859-1900 Riemann hypothesis timeline with 7 key entries."
    }
  ],
  "fail_fast": {
    "triggered": false,
    "reason": null
  }
}
```

### Fail-fast

```json
{
  "schema_name": "worker_node_authored_response",
  "schema_version": "v1",
  "output": "The assignment asks me to extract numerical results from the attached dataset, but the referenced artifact art_0002 is a free-text interview transcript with no numerical content. I cannot extract numbers that do not exist.",
  "output_summary": "Assignment is incompatible with the referenced artifact's content type.",
  "fail_fast": {
    "triggered": true,
    "reason": "Referenced artifact art_0002 is a text transcript, not a dataset. The assignment to extract numerical results cannot be completed against this input."
  }
}
```

## Validation Rules

- the object must be valid JSON only, with no surrounding prose
- `output` and `output_summary` are both required and must be non-empty
- if `artifacts_created` is present, every entry must include a non-empty `title`, `type`, `content`, and `summary`
- each entry's `type` must be one of the allowed values listed in [`artifact-record-contract.md`](./artifact-record-contract.md)
- if an entry's `supersedes` is non-null, that prior `artifact_id` must exist in the run's artifact manifest at write time
- `fail_fast.triggered` must be a boolean; if `true`, `fail_fast.reason` must be a non-empty string
- there are NO orchestration decision fields anywhere in this schema — no `delegate`, no `transmute`, no `execute_locally`, no `chosen_subgraph_type`, no `slot_fills`, no `turn_decision`, no `helpers`, no `synthesis_brief`, no `message_for_next_agent`, no `next_node_overrides`. Workers do not decide what comes next.

## Relationship to Other Contracts

- `artifacts_created` entries are persisted by the runtime as [`artifact-record-contract.md`](./artifact-record-contract.md) sidecars. The runtime fills in the runtime-owned fields (`artifact_id`, `created_by_node_id`, `version`, `content_ref`, `content_size_bytes`) when it writes each entry to disk and updates the run's artifact manifest.
- `fail_fast.triggered == true` causes the containing subgraph instance to terminate early with `status: failed_fail_fast` (see [`subgraph-instance-contract.md`](./subgraph-instance-contract.md)). Buddy sees that status in his accumulated state on the next turn.
- the worker's authored response is preserved on the worker's `node_record` (see [`node-record-contract.md`](./node-record-contract.md)) like any other authored output, alongside its prompt packet, metrics, and replay reference.

## Notes

- this schema is deliberately minimal. Every field that exists is load-bearing. There is no orchestration decision branching, no `allowed_decisions` restriction, no "agent chooses" mode, no synthesis brief, no helper specs
- workers do not author `synthesis_brief`, `helpers`, or any other strategic field. If a slot needs multi-turn behavior, it is marked `buddy: always` in the subgraph type and becomes its own host with its own Buddy loop — the worker schema never grows multi-turn awareness
- `fail_fast` is the one escape hatch and must not be abused for "soft" problems. Use it only when the assignment itself is broken or the approach genuinely cannot succeed as specified. Disagreement with the instructions, partial difficulty, or a desire to try a different angle are not fail-fast cases — they are `output` content that Buddy can read and react to on the next turn
- benchmark-specific answer formatting belongs inside `output`, not outside the JSON envelope
- the radical simplicity of this schema versus super-eywa's mixed-role authored response is the point. The two-contract split (Buddy vs worker) is what makes the strategic and tactical signals separable in the learning surfaces
