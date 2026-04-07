# Subgraph Type Contract

## Purpose

A `subgraph_type` is a named, reusable, fully-fixed bundle: a DAG shape, a per-slot meta prompt for every slot, and per-slot variable defaults.

It lives as one file in the type library and is picked by Buddy at runtime. Buddy's only authoring job at pick time is naming the type and binding any context variables the type's meta prompts reference. Buddy does NOT write per-slot task-specific instructions — those live in the bundle as templated meta prompts and are rendered by the runtime when the engine materializes a `subgraph_instance`.

Subgraph types are content-addressable, versionable, and immutable. A modification to an existing type is always a new file with a bumped version or a variant suffix. Two runs that pick the same `type_content_hash` and see the same task + state produce literally identical rendered prompts at every slot — that is the load-bearing property the learning surfaces depend on.

## Required Fields

- `contract_name`
  - always `subgraph_type`
- `contract_version`
  - starting at `v1`
- `name`
- `version`
- `description`
- `slots`
- `terminal`

## Optional Fields

- `buddy_bound_variables`
  - list of buddy-bound template variable names this type expects Buddy to resolve via `context_bindings`
  - convenience for Buddy (so he knows what to bind without parsing every meta prompt) and for validation
  - if omitted, the runtime auto-computes the list by scanning every slot's `meta_prompt` for variables that do not match an auto-bound pattern
  - if present, the runtime validates that every listed variable is actually referenced somewhere in the type's meta prompts and that no buddy-bound variable referenced in the prompts is missing from the list

## Field Details

### `name`

Library-unique identifier for the type (e.g., `just_execute`, `delegate_fanout_synthesize`).

### `version`

Version string for the type itself (e.g., `v1`).

Types are immutable. A modification is a new file with a bumped version or a variant suffix, not an in-place edit.

### `description`

Human- and agent-readable summary of when this type is appropriate.

Buddy reads this when choosing which type to pick for the next turn.

### `slots`

Object keyed by slot label. Each entry describes one labeled position in the DAG.

Required fields on each slot:

- `role`
  - short human-readable label for what this slot is for
  - used for display, debugging, and grouping in learning surfaces
  - NOT the prompt — the prompt lives in `meta_prompt`
  - kept required so the Scientist always provides a recognizable label per slot
- `meta_prompt`
  - the full templated system prompt for this slot
  - non-empty string
  - may contain zero or more template variables (see "Template Variables" below)
  - this is what the runtime renders into the worker's prompt at materialization time, after substituting all referenced variables
- `buddy`
  - one of `"never"`, `"always"`, or `"inherit"`
  - policy for whether this slot becomes its own host with its own Buddy loop

Optional fields on each slot:

- `inputs_from`
  - list of upstream slot label strings whose outputs feed into this slot
  - absence means the slot has no upstream and runs with only its rendered meta prompt as input
- `variables`
  - per-slot variable defaults (e.g., model, prompt profile, budget)
  - merged with run-level defaults and Buddy's per-instance overrides at materialization time

### `terminal`

The slot label whose output becomes the subgraph instance's terminal output.

## DAG Validity Rules

- Every `inputs_from` entry must resolve to a slot label that exists in this type's `slots`
- No cycles — the directed graph induced by `inputs_from` must be acyclic
- `terminal` must be a slot label that exists in `slots`
- Every non-terminal slot must have a path to the terminal slot following the `inputs_from` edges (a single connected component with the terminal slot as sink)
- Valid `buddy` values are exactly `"never"`, `"always"`, or `"inherit"`
- Every slot's `meta_prompt` must be a non-empty string
- Every template variable referenced in any slot's `meta_prompt` must be either:
  - an auto-bound variable matching one of the patterns listed in "Template Variables", OR
  - a buddy-bound variable name (any other `{name}` token); if `buddy_bound_variables` is provided, the variable must appear in that list

## Template Variables

Meta prompts contain template variables that the runtime substitutes at materialization time. This is how a fully-fixed library entry produces task-specific prompts without Buddy authoring any per-slot instruction text.

### Syntax

A template variable is `{name}` or `{namespace.field}` or `{namespace[index].field}` for structured references. The runtime parses curly-brace tokens and resolves each one to a string. Literal curly braces in a prompt body must be escaped as `{{` and `}}`.

### Auto-bound variables

These resolve automatically from runtime context. Buddy provides nothing for them. The runtime recognizes the following exact patterns:

- `{task.text}` — the run's raw task text from `run_packet.task.raw_task_text`
- `{inputs.<slot_label>.output}` — the full output of the upstream slot named `<slot_label>`. Valid only when `<slot_label>` appears in the current slot's `inputs_from`. Invalid otherwise.
- `{inputs.<slot_label>.summary}` — the summary of the upstream slot's output. Same validity rule.
- `{prior_turns[N].terminal_output}` — the terminal output of host turn `N` at the current host (0-indexed). Must reference a turn that has already completed at materialization time.
- `{prior_turns[N].summary}` — the summary of prior turn `N`'s terminal output. Same validity rule.

### Buddy-bound variables

Any `{name}` token in a meta prompt that does NOT match one of the auto-bound patterns above is a buddy-bound variable. The Scientist writes semantically meaningful templates like `"Revise the {plan} based on the {review}"`, and Buddy decides on each turn what artifacts (or literals, or prior-turn outputs) "the plan" and "the review" point at.

Buddy provides values via the `context_bindings` field on his authored response (see [`buddy-node-authored-response-contract.md`](./buddy-node-authored-response-contract.md)).

### Resolution rule

When the runtime encounters a `{name}` token in a meta prompt, it tries to match the auto-bound patterns first. If the token matches any auto-bound pattern, it is resolved from runtime context. Otherwise it is treated as a buddy-bound variable and looked up in the instance's `context_bindings` map.

This means: a buddy-bound variable can never shadow an auto-bound name. If the Scientist wants a buddy-bound variable, they must pick a name that does not collide with any auto-bound pattern (e.g., do not name a buddy-bound variable `task` and try to use `{task.text}` for it).

### Validation at materialization time

- Every buddy-bound variable referenced in any of the chosen type's slots' meta prompts must have a matching entry in `context_bindings`.
- Every auto-bound variable referenced must resolve against actual runtime state (the upstream slot exists in `inputs_from`, the prior turn exists, etc.).
- If `buddy_bound_variables` is provided on the type, the set of buddy-bound variables actually referenced must equal the declared set.
- Bindings present in `context_bindings` but not referenced in any meta prompt are a warning, not an error — the runtime ignores them.

## Content Hashing

Every subgraph instance records the content hash of the type spec it was materialized from. This gives the Scientist a precise grouping key across runs, even as the library evolves.

Algorithm:

1. Canonicalize the spec JSON — keys sorted at every nesting level, whitespace normalized, no trailing commas. The canonical form MUST include every field of the spec, including each slot's `meta_prompt` and the optional `buddy_bound_variables` list. The full bundle (shape + meta prompts + variable defaults) is what the hash captures.
2. Hash the canonical bytes with SHA-256.
3. The resulting hex digest is the content hash.

Two types with different names but identical content hashes are structurally equivalent — same shape, same meta prompts, same defaults. Two types with identical names but different content hashes are treated as different type versions. Editing a single character in any meta prompt produces a new content hash, which is exactly the property the learning surfaces rely on for clean attribution.

## On Disk

Specs live at `eywa-system/variables/subgraph-types/<name>.json`. One file per type.

The loader and validator land in Step 2 of Section 2 of the build.

## Example Shape

### `just_execute`

```json
{
  "contract_name": "subgraph_type",
  "contract_version": "v1",
  "name": "just_execute",
  "version": "v1",
  "description": "One worker, one shot. Buddy picks this when the next step is narrow enough to answer in a single pass with no decomposition.",
  "buddy_bound_variables": [],
  "slots": {
    "worker": {
      "role": "produce the requested output",
      "meta_prompt": "You are the sole worker for this task. Your task:\n\n{task.text}\n\nProduce the requested output directly. Do not propose follow-up work or alternative approaches — return only the result.",
      "buddy": "never",
      "variables": {}
    }
  },
  "terminal": "worker"
}
```

### `delegate_fanout_synthesize`

```json
{
  "contract_name": "subgraph_type",
  "contract_version": "v1",
  "name": "delegate_fanout_synthesize",
  "version": "v1",
  "description": "Fan out a task into three parallel workers, then synthesize their outputs into one answer. Good for tasks that separate cleanly into independent subtasks.",
  "buddy_bound_variables": [],
  "slots": {
    "worker_1": {
      "role": "handle the first independent piece of the task",
      "meta_prompt": "You are worker 1 in a three-way fan-out. Your task:\n\n{task.text}\n\nHandle the first independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "buddy": "never",
      "variables": {}
    },
    "worker_2": {
      "role": "handle the second independent piece of the task",
      "meta_prompt": "You are worker 2 in a three-way fan-out. Your task:\n\n{task.text}\n\nHandle the second independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "buddy": "never",
      "variables": {}
    },
    "worker_3": {
      "role": "handle the third independent piece of the task",
      "meta_prompt": "You are worker 3 in a three-way fan-out. Your task:\n\n{task.text}\n\nHandle the third independent piece of this task. Return a compact bullet-point summary of your findings or output. Do not attempt to cover the other two pieces — other workers handle those.",
      "buddy": "never",
      "variables": {}
    },
    "synthesizer": {
      "role": "combine the worker outputs into one coherent final answer",
      "meta_prompt": "You are the synthesizer. Your task:\n\n{task.text}\n\nThree workers handled independent pieces of this task in parallel. Combine their outputs into one coherent final answer. Do not duplicate the workers' work or critique their approach — integrate.\n\nWorker 1 output:\n{inputs.worker_1.output}\n\nWorker 2 output:\n{inputs.worker_2.output}\n\nWorker 3 output:\n{inputs.worker_3.output}",
      "buddy": "never",
      "inputs_from": ["worker_1", "worker_2", "worker_3"],
      "variables": {}
    }
  },
  "terminal": "synthesizer"
}
```

## Notes

- types are immutable; variants are new files, never in-place edits
- content-addressed identity is what makes learning analyses stable across library evolution
- under Option 3, Buddy authors no per-slot instruction text. The bundle (shape + meta prompts + variable defaults) is the whole thing. Iteration on prompt wording is the Scientist's job: publish a new bundle as a new file with a new hash, then bench the two against each other
- novel adaptive behavior must be crystallized by the Scientist as a new library entry. Buddy cannot improvise instruction text on a turn; if a desired behavior does not yet exist in the library, the Scientist authors it
- `variables` defaults follow a three-layer merge at materialization time: run-level ← type's per-slot ← Buddy's per-instance overrides (latest wins). This merge ordering lives with the runtime, not with the contract.
- a type carries no task-specific content, no node IDs, and no runtime state — only the workflow pattern, the templated meta prompts, and the variable defaults
