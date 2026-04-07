# 07 — Relation to the Current Super-Eywa Codebase

## The short version

Buddy-Eywa is an additive evolution of super-eywa, not a rewrite. The current codebase already has most of the primitives needed — they just need to be generalized and rewired. The hard changes are localized to the engine; the contracts, storage, executor, and grading infrastructure barely need to move.

## Overlap with existing primitives

### Recursion is already there

`eywa-system/runtime/eywa_runtime/engine.py`'s `_execute_node` is already a recursive function that materializes children and runs them. Buddy-Eywa's `expand_node` and `expand_subgraph` are a generalization of that — the recursion pattern stays the same, just extended to handle a small DAG of slots instead of just "one parent and its immediate helpers."

### Routing primitive is already there

The current `node_output` contract has `outgoing_packets` with `target_type` and `target_ref`. That's the primitive we need for routing — it already supports pointing an output at an arbitrary target. Buddy-Eywa's "edges between slots" reuses this exact field; the engine just needs to resolve slot labels to actual node IDs at materialization time and set `target_ref` accordingly.

### Per-child variable overrides are already there

The current `delegate` authored response has `helpers[].variable_overrides`, and the engine merges them into the child's resolved variables. Buddy-Eywa's "per-slot variable overrides" uses the exact same mechanism — just authored by Buddy as part of `slot_fills` rather than by a parent node choosing to delegate.

### Contracts stay mostly the same

- **`run_packet`** — unchanged. The run still starts with a task, run-level variables, and a root node pointer.
- **`node_packet`** — barely changes. One new field (`inputs_from_labels` → resolved `inputs_from_node_ids`), one new field (`artifact_refs`), one optional addition (`host_context_ref` for Buddy-loop hosts).
- **`node_record`** — barely changes. Same fields for input, variables, state, results, prompt, logging. One addition: `subgraph_instance_id` so records can be grouped by their containing instance.
- **`node_output`** — unchanged. Outgoing packets already handle arbitrary routing.
- **`final_output`** — unchanged.

### Storage layout stays mostly the same

```
run_dir/
  run_packet.json                     (unchanged)
  run_summary.json                    (unchanged)
  final-output.json                   (unchanged)
  nodes/                              (unchanged; each node still has its own folder)
    node_xxx/
      node_packet.json
      node_record.json
      events.jsonl
      edges.json
  events/run-events.jsonl             (unchanged)
  derived/                            (unchanged)
  replay/                             (unchanged)
  artifacts/                          (NEW)
    manifest.json
    art_0001_plan.md
    art_0001_plan.metadata.json
    ...
  subgraphs/                          (NEW)
    subgraph_instance_xxx/
      spec_resolved.json              (the materialized subgraph spec)
      type_content_hash.txt
      edges.json                      (the DAG edges for this instance)
      terminal_output.json
```

All existing directories stay; two new ones (`artifacts/` and `subgraphs/`) get added.

## What actually has to change

### 1. New contract: `subgraph_spec`

A new contract file in `eywa-system/contracts/` describing subgraph type specs and their materialized instances. Defines the schema for library files.

### 2. New contract: `artifact_record`

A new contract file describing artifact metadata schema. Defines the manifest layout.

### 3. Buddy's authored response schema

`pick_subgraph` becomes a new value for `orchestration_decision` in the authored response schema (alongside the existing `execute_locally`, `delegate`, `transmute`, `review`, `report_problem`). The structure:

```json
{
  "schema_name": "eywa_node_response",
  "schema_version": "v2",
  "orchestration_decision": "pick_subgraph",
  "turn_decision": "pick_subgraph" | "done",
  "chosen_subgraph_type": "delegate_fanout_synthesize",
  "slot_fills": {
    "worker_1": { "instructions": "...", "variable_overrides": {}, "artifact_refs": [] },
    "worker_2": { "instructions": "...", "variable_overrides": {}, "artifact_refs": [] },
    ...
  },
  "final_answer": null   // populated when turn_decision is "done"
}
```

This adds to the existing schema without breaking it.

### 4. Worker's authored response — radical simplification

Workers get their own schema variant, `buddy_eywa_worker_response`, that has no orchestration decisions. Just output, summary, artifacts_created, fail_fast. See `04-workers-slots.md`.

### 5. Engine refactor — split `_execute_node`

Split the current `_execute_node` into two functions:

- **`expand_node(node_spec, ctx)`** — entry point for any node. Checks the node's buddy policy. If `buddy: always`, starts a Buddy loop. Otherwise, executes as a single-turn worker.
- **`expand_subgraph(type, slot_fills, ctx)`** — materializes a subgraph instance from a type + fills, topologically orders its slots, runs them in order, routes outputs along the DAG edges, returns the terminal slot's output.

These two functions call each other recursively. The current `_execute_node`'s multi-turn loop goes away; the authored-response parsing, node-record writing, and replay-step recording all migrate into `expand_node` (for single-turn) or into the Buddy loop (for hosts).

### 6. Engine addition — the Buddy loop driver

A new function that runs a host node: repeatedly prompts Buddy, interprets the pick/done decision, calls `expand_subgraph` for picks, accumulates state, terminates on done or budget exhaustion. This is the new recursion driver at every host.

### 7. Engine addition — topological scheduler

For slots with `inputs_from` edges, the engine needs to run them in topological order and gate execution until all `inputs_from` slots have produced outputs. Simple implementation: maintain a "ready queue" of slots whose inputs are all satisfied, pop one at a time, run it, update readiness. For v1 this can be sequential; parallelism is a later optimization.

### 8. Engine addition — artifact store

New module `eywa_runtime/artifacts.py` that handles: creating artifacts on worker completion, loading referenced artifacts into worker prompts, maintaining the manifest.

### 9. Prompt assembly changes

`prompting.py` gets two new builders:

- `build_buddy_turn_prompt(host_context, accumulated_state, artifact_inventory, library_summary)` — the strategic prompt for a Buddy turn
- `build_worker_prompt(slot_spec, slot_fill, upstream_inputs, referenced_artifacts)` — the simplified tactical prompt

The current `build_turn_prompt` stays around during the coexistence period, used by legacy paths.

### 10. Executor stays mostly the same

`executor.py`'s `OpenRouterLiveExecutor` and `DeterministicLocalExecutor` don't need to change much. They still generate text given a prompt and parse an authored response. The parsing branches on the new schema versions, but the underlying generate-and-parse pipeline is the same.

### 11. Validation and correctness

New validators:
- Subgraph type spec validation (no cycles, all `inputs_from` resolve to valid labels, terminal is a real slot)
- Subgraph instance validation (consistent with its type, all slots present)
- Artifact manifest validation (all content_refs exist, supersedes chains are consistent)

These live alongside the existing validators in `data-system/correctness-suite/`.

### 12. Tests

New golden-run tests for:
- 1-slot `just_execute` subgraph running to completion
- Multi-slot `delegate_fanout_synthesize` with 3 workers and a synthesizer
- Buddy multi-turn loop with 2 different subgraph picks
- Nested case: host → slot with `buddy: always` → inner Buddy loop
- Fail-fast: worker signals termination, Buddy pivots on next turn
- Artifacts: worker creates one, next slot reads it, next turn's Buddy sees summary

## What does NOT have to change

- Grading infrastructure (`data-system/grading/`)
- OpenRouter client (`openrouter_client.py`)
- Supabase sync
- Run history storage format (the per-run directory layout)
- Validation of existing contracts that aren't being replaced
- Most of the story view / timeline generation (needs DAG awareness but the basic structure is the same)
- Budget policy and depth limits (the mechanism exists; new limits are just additional variables)

## Handling the existing run-history data

**Recommendation: skip the write-time backfill. Use a read-time adapter.**

The Plan subagent flagged that a write-time backfill script (rewriting old runs into the new format) is risky — it entrenches the new model before it's been validated and is one-way. A better approach:

1. Leave all existing run-history data untouched.
2. Build a small read-time adapter that, when the Scientist wants to study historical data, presents old runs through a compatible view: each old node becomes a virtual 1-slot subgraph instance, the prompt_family becomes a `_legacy_` subgraph type, the `delegate` actions become virtual `delegate_fanout_synthesize` instances retroactively.
3. Scientist can then query across old and new runs uniformly through the adapter, but the truth on disk is unchanged.

If it turns out the new format is working well and all new runs are using it, you can consider a proper migration much later — but only after the new bones have been proven stable.

## Coexistence period

During the worktree development, both old and new paths can live side by side:

- Current `_execute_node` keeps working for the old authored-response schema
- New `expand_node` / `expand_subgraph` / Buddy loop runs for runs that set `runtime_mode: buddy_eywa_v1` in their run-level variables
- Grading bench can run both modes and compare scores
- Once the new mode's scores match or beat the old mode, the old path can be retired

This is a safer landing strategy than a hard cutover. It also means the new implementation can be developed incrementally — land contracts first, then the library, then the Buddy role, then the engine refactor, each piece validated on its own before the next.
