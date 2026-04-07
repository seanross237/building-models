# Buddy Node Authored Response Contract

## Purpose

The `buddy_node_authored_response` is the JSON object Buddy must return on every turn at a host node.

It is the protocol boundary between:

- Buddy's strategic judgment
- the runtime's execution machinery

On each turn, Buddy authors exactly one of two things:

- a subgraph pick — naming a fully-fixed bundle from the library and binding any context variables that bundle's meta prompts reference
- a done declaration — handing back a final answer for the host

The runtime validates this object before materializing a `subgraph_instance` or terminating the host. Buddy never authors task work directly. Under Option 3, Buddy also never authors per-slot instruction text — those prompts live in the chosen subgraph type's meta prompts and are rendered by the runtime using Buddy's `context_bindings` and the runtime's auto-bound variables.

## Required Fields

- `schema_name`
  - always `buddy_node_authored_response`
- `schema_version`
  - starting at `v1`
- `turn_decision`

## Allowed `turn_decision` Values

- `pick_subgraph`
- `done`

There is no third value. Budget exhaustion is not Buddy's job to author — when Buddy's turn budget runs out without a `done`, the runtime authors a synthetic terminal state separately.

## Common Optional Fields

- `decision_notes`
  - short explanation of why Buddy made this choice
  - surfaced as a human-readable column in the buddy-turn learning surface
  - strongly encouraged for all turns, even though optional

## `pick_subgraph` Shape

Required extra fields:

- `chosen_subgraph_type`
  - the `name` of a subgraph type in the currently loaded library
  - must match a type that exists in the library at turn time
- `context_bindings`
  - object resolving every buddy-bound template variable referenced by the chosen type's meta prompts
  - exactly one entry per buddy-bound variable name; no missing bindings
  - empty object `{}` is required (and valid) when the chosen type declares no buddy-bound variables
  - per-entry shape documented in "context_bindings Shape" below

Optional extra fields:

- `variable_overrides`
  - map from slot label to a per-slot variable overrides object, e.g., `{"worker_1": {"model": "gpt-5.4"}}`
  - defaults to an empty object if omitted
  - merged with the type's per-slot defaults and any run-level defaults at materialization time (latest wins)
  - only slot labels that exist in the chosen type are valid keys; extra keys are an error

## `context_bindings` Shape

A flat per-instance map. Keys are buddy-bound template variable names (matching `{name}` tokens in the chosen type's slot meta prompts that do not match an auto-bound pattern). Values are typed binding objects.

Bindings are flat across the whole instance — every slot in the instance shares the same bindings. If two slots' meta prompts both reference `{plan}`, they resolve to the same binding.

### Per-entry shape

Every entry has a `binding_type` discriminator plus the extra fields required by that type.

Supported `binding_type` values for v1:

- `artifact`
  - additional field: `artifact_id` — must exist in the run's artifact manifest at turn time
  - the runtime substitutes the rendered content of the referenced artifact into the meta prompt at materialization time
- `literal`
  - additional field: `value` — plain string, substituted into the meta prompt verbatim
  - useful for small free-form fragments the type wants Buddy to author per-turn (e.g., a user-style note or a constraint)
- `prior_turn_output`
  - additional field: `turn_number` — integer, 0-indexed, must be a prior turn at the current host
  - the runtime substitutes the terminal output of that turn into the meta prompt at materialization time

These three are the entire v1 vocabulary. The runtime rejects any other `binding_type` value.

## Examples

### `pick_subgraph` — seed type with no buddy-bound variables

```json
{
  "schema_name": "buddy_node_authored_response",
  "schema_version": "v1",
  "turn_decision": "pick_subgraph",
  "decision_notes": "The task separates cleanly into three independent research angles plus a synthesis step. Upgrading worker_3's model since it has the heaviest historical period.",
  "chosen_subgraph_type": "delegate_fanout_synthesize",
  "context_bindings": {},
  "variable_overrides": {
    "worker_3": {
      "model": "gpt-5.4",
      "context_policy": "expanded"
    }
  }
}
```

### `pick_subgraph` — hypothetical future bundle with buddy-bound variables

This example illustrates the `context_bindings` shape on a bundle that takes Buddy-supplied references. The `revise_plan_given_review` type is hypothetical (not part of the seed library) and exists here only to show what the field looks like in practice — its meta prompts would reference `{plan}`, `{review}`, and `{focus_note}`.

```json
{
  "schema_name": "buddy_node_authored_response",
  "schema_version": "v1",
  "turn_decision": "pick_subgraph",
  "decision_notes": "Worker_2 just produced a critique of the original plan. Re-running the planner against that critique with an explicit focus on the edge case worker_2 flagged.",
  "chosen_subgraph_type": "revise_plan_given_review",
  "context_bindings": {
    "plan": {
      "binding_type": "artifact",
      "artifact_id": "art_0001"
    },
    "review": {
      "binding_type": "artifact",
      "artifact_id": "art_0003"
    },
    "focus_note": {
      "binding_type": "literal",
      "value": "Pay particular attention to the edge case where the input dataset is empty."
    },
    "prior_analysis": {
      "binding_type": "prior_turn_output",
      "turn_number": 2
    }
  },
  "variable_overrides": {}
}
```

### `done`

```json
{
  "schema_name": "buddy_node_authored_response",
  "schema_version": "v1",
  "turn_decision": "done",
  "decision_notes": "Two turns produced a researched draft and a glossary patch. The result satisfies the host task and further turns would only add polish.",
  "final_answer": "Quantum computing is a model of computation that uses quantum-mechanical phenomena... [full 600-word draft with glossary]",
  "final_answer_summary": "600-word general-audience blog post on quantum computing with an inline glossary."
}
```

## `done` Shape

Required extra fields:

- `final_answer`
  - the final answer for this host
  - structured object or string, task-appropriate

Optional extra fields:

- `final_answer_summary`
  - short one-line summary of the final answer
  - surfaced in the buddy-turn learning surface and in any parent host's accumulated state on the next turn

## Validation Rules

- the object must be valid JSON only, with no surrounding prose
- `turn_decision` must be exactly `"pick_subgraph"` or `"done"`
- when `turn_decision` is `"pick_subgraph"`:
  - `chosen_subgraph_type` must be present and must match the `name` of a subgraph type in the currently loaded library
  - `context_bindings` must be present (possibly an empty object)
  - every buddy-bound variable declared by the chosen subgraph type — whether listed explicitly in its `buddy_bound_variables` field or computed by parsing its slot meta prompts — must have a matching entry in `context_bindings`
  - every `context_bindings` entry must have a `binding_type` of `"artifact"`, `"literal"`, or `"prior_turn_output"` and must include the additional fields required for that type
  - for `binding_type: "artifact"`, the referenced `artifact_id` must exist in the run's artifact manifest at turn time
  - for `binding_type: "prior_turn_output"`, the referenced `turn_number` must be a non-negative integer pointing at a prior turn at the current host (not the current turn or a future turn)
  - extra entries in `context_bindings` that do not correspond to any buddy-bound variable in the chosen type are a warning, not an error — the runtime ignores them
  - `variable_overrides` is optional and defaults to an empty object; only slot labels defined in the chosen type are valid keys
  - `final_answer` and `final_answer_summary` must be absent
- when `turn_decision` is `"done"`:
  - `final_answer` must be present
  - `chosen_subgraph_type`, `context_bindings`, and `variable_overrides` must be absent
- workers do not have orchestration decisions of any kind — those live in the worker contract and are deliberately separate from this one

## Relationship to Other Contracts

- `chosen_subgraph_type` references a type in [`subgraph-type-contract.md`](./subgraph-type-contract.md). The named type must exist in the loaded library and be loadable; its content hash is captured separately by the runtime when the instance is materialized.
- `context_bindings` is resolved at materialization time. `artifact` bindings are looked up against [`artifact-record-contract.md`](./artifact-record-contract.md) sidecars in the run's artifact manifest. `literal` bindings substitute their `value` verbatim. `prior_turn_output` bindings resolve against the current host's prior turn records. The substituted text lands in the per-slot `rendered_prompt` field on the resulting [`subgraph-instance-contract.md`](./subgraph-instance-contract.md).
- `context_bindings` itself is preserved verbatim on the materialized instance's top-level `context_bindings` field, so the link from "what Buddy bound" to "what the worker saw" is recoverable.
- `variable_overrides` flows into `slots_resolved[<slot_label>].variable_overrides` on the materialized [`subgraph-instance-contract.md`](./subgraph-instance-contract.md).
- Buddy's authored response is preserved on the host node's `node_record` (see [`node-record-contract.md`](./node-record-contract.md)) like any other authored output, alongside its prompt packet, metrics, and replay reference.

## Notes

- this is the only authoring surface for strategic decisions in buddy-eywa — every strategic choice in the system flows through this contract
- under Option 3, Buddy's authoring surface is intentionally minimal: pick a type, bind any context variables the type requires, optionally override per-slot variables. Buddy never writes per-slot instruction text. Per-slot prompts are crystallized in the library by the Scientist as templated meta prompts on the type, and the runtime renders them.
- `variable_overrides` is optional and the simplest runs use none. It exists for the case where Buddy observes something at runtime that justifies deviating from the type's defaults — for example, upgrading the model on a slot that is about to handle a particularly hard piece of the task. It is NOT a way to inject new instruction content; instructions live in `meta_prompt` only.
- `decision_notes` is optional but strongly encouraged; it becomes the human-readable rationale column in the buddy-turn learning surface and is what later analysis uses to attribute outcomes to choices
- there is no orchestration decision branching here beyond `pick_subgraph` vs `done` — Buddy never authors `delegate`, `transmute`, `execute_locally`, or any other action verb. The execution shape is owned by the chosen subgraph type, not by Buddy
- routing inside an instance is owned by the chosen subgraph type's edges, not by anything Buddy authors here
- a `pick_subgraph` turn always produces exactly one `subgraph_instance`; a `done` turn produces zero
- benchmark-specific answer formatting belongs inside `final_answer`, not outside the JSON envelope
