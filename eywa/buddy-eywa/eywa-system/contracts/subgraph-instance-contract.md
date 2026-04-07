# Subgraph Instance Contract

## Purpose

A `subgraph_instance` is the live, materialized form of a `subgraph_type`.

It is created when Buddy picks a type at a turn and the engine renders the type's per-slot meta prompts using Buddy's `context_bindings` and runtime auto-bound variables, then assigns node IDs. The instance records which type was used (by name and content hash), the exact context bindings Buddy authored, the rendered prompts each slot's worker actually saw, the resulting DAG edges, the assigned node IDs, and the terminal output reference once the instance finishes.

## Relationship to `subgraph_type`

Every instance references its originating type via `type_name`, `type_version`, and `type_content_hash`. The content hash is the load-bearing identity field — it pins the exact spec the instance was materialized from regardless of any later changes to the library file. Because the type's content hash captures the full bundle (shape + meta prompts + variable defaults), two instances with the same `type_content_hash` and the same task + state produce literally identical `rendered_prompt` values at every slot.

## Required Fields

- `contract_name`
  - always `subgraph_instance`
- `contract_version`
  - starting at `v1`
- `subgraph_instance_id`
- `run_id`
- `parent_host_node_id`
- `buddy_turn_number`
- `type_name`
- `type_version`
- `type_content_hash`
- `context_bindings`
- `slots_resolved`
- `edges`
- `terminal_slot_label`
- `terminal_output_ref`
- `status`
- `created_at_utc`
- `completed_at_utc`

## Field Details

### `subgraph_instance_id`

Unique ID for this instance. See the ID generation section below.

### `parent_host_node_id`

The host node whose Buddy loop spawned this instance.

The root host is the run's root node. Nested hosts spawn their own instances within their own Buddy loops.

### `buddy_turn_number`

Which turn at the parent host produced this instance.

This lets instances be ordered within a host's loop without needing to reconstruct turn order from timestamps.

### `type_name`, `type_version`, `type_content_hash`

The originating subgraph type's name, version, and SHA-256 hex digest of its canonical spec JSON.

`type_content_hash` is the grouping key for learning analyses across runs.

### `context_bindings`

Object. The exact buddy-bound template variable bindings Buddy authored on his `pick_subgraph` response for this instance, copied verbatim.

Each entry is keyed by template variable name and has a `binding_type` plus the type-specific extra fields (see [`buddy-node-authored-response-contract.md`](./buddy-node-authored-response-contract.md) for the full shape).

Empty object `{}` when the chosen type declares no buddy-bound variables.

This field is preserved on the instance so any later replay or analysis can reconstruct exactly what Buddy bound — independently of any changes to the run's artifact manifest after the fact.

### `slots_resolved`

Object keyed by slot label with one entry per slot in the referenced type.

Required fields on each entry:

- `node_id`
  - the node ID assigned to this slot when `buddy_policy` is `"never"`
  - the nested host node ID when `buddy_policy` is `"always"`
- `rendered_prompt`
  - the runtime-rendered meta prompt for this slot after all template variable substitution
  - this is the exact prompt text the worker saw, captured for replay and learning analysis
  - non-empty string
  - written by the runtime at materialization time (and may grow incrementally for slots whose `meta_prompt` references upstream `{inputs.<slot_label>.output}` — those substitutions happen once the upstream slot has produced output, not at instance creation time)
- `variable_overrides`
  - per-slot overrides Buddy authored for this instance
  - empty object if none
- `buddy_policy`
  - the resolved buddy policy for this slot
  - one of `"never"` or `"always"` (`"inherit"` is resolved at materialization time and never appears here)

### `edges`

List of `{from_slot_label, to_slot_label}` pairs derived from the type's `inputs_from`.

Present so the DAG is explicit in the record without needing to re-parse the type spec.

### `terminal_slot_label`

The label of the terminal slot, copied from the type for convenience.

### `terminal_output_ref`

Reference to the terminal slot's output (node ID or similar) once the instance completes.

`null` until the terminal slot has produced output.

### `status`

One of:

- `created`
- `running`
- `completed`
- `failed_fail_fast`
- `budget_exhausted`
- `system_error`

### `created_at_utc`, `completed_at_utc`

ISO timestamps. `completed_at_utc` is `null` until the instance reaches a terminal status.

## Subgraph Instance ID Generation

Format: `sg_inst_<shorthash>_<runid>_<counter>`

- `shorthash` — first 8 hex chars of `type_content_hash`
- `runid` — the run ID this instance belongs to
- `counter` — monotonic integer scoped to the run, incremented per instance

This gives IDs that are deterministic enough for replay and unique enough for debugging.

## On Disk

The instance lives at `run_dir/subgraphs/<subgraph_instance_id>/`.

Files inside:

- `instance.json` — this contract (the full record)
- `spec_resolved.json` — snapshot of the type spec as loaded, with any variable resolution applied
- `type_content_hash.txt` — the bare content hash for quick greppability
- `edges.json` — the DAG edges for this instance (redundant with `instance.json:edges` but convenient for tools that just want the graph)
- `terminal_output.json` — the terminal slot's output (written on completion)

## Example Shape

```json
{
  "contract_name": "subgraph_instance",
  "contract_version": "v1",
  "subgraph_instance_id": "sg_inst_a1b2c3d4_run_2026_04_07_001_3",
  "run_id": "run_2026_04_07_001",
  "parent_host_node_id": "node_root",
  "buddy_turn_number": 2,
  "type_name": "delegate_fanout_synthesize",
  "type_version": "v1",
  "type_content_hash": "a1b2c3d4e5f607182930415263748596a7b8c9d0e1f2031425364758697a8b9c",
  "context_bindings": {},
  "slots_resolved": {
    "worker_1": {
      "node_id": "node_root__t2__sg3__worker_1",
      "rendered_prompt": "You are worker 1 in a three-way fan-out. Your task:\n\nWrite a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today.\n\nHandle the first independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "variable_overrides": {},
      "buddy_policy": "never"
    },
    "worker_2": {
      "node_id": "node_root__t2__sg3__worker_2",
      "rendered_prompt": "You are worker 2 in a three-way fan-out. Your task:\n\nWrite a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today.\n\nHandle the second independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "variable_overrides": {},
      "buddy_policy": "never"
    },
    "worker_3": {
      "node_id": "node_root__t2__sg3__worker_3",
      "rendered_prompt": "You are worker 3 in a three-way fan-out. Your task:\n\nWrite a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today.\n\nHandle the third independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "variable_overrides": {
        "model": "gpt-5.4",
        "context_policy": "expanded"
      },
      "buddy_policy": "never"
    },
    "synthesizer": {
      "node_id": "node_root__t2__sg3__synthesizer",
      "rendered_prompt": "You are the synthesizer. Your task:\n\nWrite a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today.\n\nThree workers handled independent pieces of this task in parallel. Combine their outputs into one coherent final answer. Do not duplicate the workers' work or critique their approach — integrate.\n\nWorker 1 output:\n<rendered once worker_1 completes>\n\nWorker 2 output:\n<rendered once worker_2 completes>\n\nWorker 3 output:\n<rendered once worker_3 completes>",
      "variable_overrides": {},
      "buddy_policy": "never"
    }
  },
  "edges": [
    {"from_slot_label": "worker_1", "to_slot_label": "synthesizer"},
    {"from_slot_label": "worker_2", "to_slot_label": "synthesizer"},
    {"from_slot_label": "worker_3", "to_slot_label": "synthesizer"}
  ],
  "terminal_slot_label": "synthesizer",
  "terminal_output_ref": null,
  "status": "running",
  "created_at_utc": "2026-04-07T15:42:00Z",
  "completed_at_utc": null
}
```

## Validation Rules

- Every key in `slots_resolved` must match a slot label in the referenced subgraph type (verified by content hash)
- `terminal_slot_label` must be a key in `slots_resolved`
- `edges` must be consistent with the type's `inputs_from`
- `parent_host_node_id` must be a valid node ID (not enforced by this contract, but noted)
- `buddy_policy` on every resolved slot must be `"never"` or `"always"` — `"inherit"` is resolved at materialization time and is not a valid stored value here
- Every buddy-bound variable declared by the referenced subgraph type (via `buddy_bound_variables`, or computed by parsing meta prompts if that field is omitted) must have a matching entry in `context_bindings` keyed by name
- Every entry in `context_bindings` must have a valid `binding_type` and the required extra fields for that type, per [`buddy-node-authored-response-contract.md`](./buddy-node-authored-response-contract.md)
- `rendered_prompt` must be present as a non-empty string on every slot in `slots_resolved` (the runtime is responsible for populating it; for slots whose meta prompt references `{inputs.<slot_label>.output}`, the placeholder is allowed to remain unsubstituted until the upstream slot completes, but the field itself must always be present)

## Notes

- the instance is the atomic unit of Buddy's strategic decisions — one Buddy turn produces exactly one instance (unless the turn is `done`)
- `type_content_hash` is the grouping key for learning analyses; two instances with the same hash used the same spec
- `rendered_prompt` is the single source of truth for what each worker actually saw. The slot-execution learning surface groups by `(type_content_hash, slot_label)` for cross-run analysis and reads `rendered_prompt` for the per-row prompt detail. Anything that wants to attribute a worker outcome to its prompt reads this field.
- `context_bindings` is preserved verbatim alongside `rendered_prompt` so the link from "what Buddy bound" to "what the worker saw" is recoverable from a single record
- `failed_fail_fast` status means a worker slot authored a fail-fast signal that terminated the instance early
- `edges` is intentionally denormalized so tooling can read the DAG without re-loading the type file
