# 02 — Subgraph Types

## What a subgraph type is

A subgraph type is a **named, reusable, fully-fixed bundle**: a DAG shape, a templated meta prompt for every slot, and per-slot variable defaults. It lives as one file in the type library. The library entry is the whole bundle, not just the shape — Buddy picks it as a unit and the runtime renders the meta prompts into worker prompts at materialization time.

Subgraph types are to Buddy-Eywa what prompt profiles are to current super-eywa: a library of named, variable-driven behaviors that get selected and parameterized at runtime rather than hard-coded into the engine.

## Where the library lives

```
eywa-system/variables/subgraph-types/
  just_execute.json
  delegate_fanout_synthesize.json
  plan_3review_consolidate.json    (added later)
  research_then_execute_then_consolidate.json    (added later)
  ...
```

One file per type. Simple loader, simple validator.

## What a type contains

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

Fields explained:

- **contract_name / contract_version** — envelope tags identifying this file as a `subgraph_type` document; used by the loader and validator
- **name** — library-unique identifier
- **version** — version string (types are immutable; variants are new files or `_v2` suffixes)
- **description** — human- and agent-readable summary of when this type is appropriate; Buddy reads this when choosing which type to pick
- **buddy_bound_variables** — optional list of buddy-bound template variable names this type's meta prompts reference. If omitted, the runtime auto-computes the list by scanning the meta prompts. Empty list means the type needs nothing from Buddy beyond the pick itself.
- **slots** — labeled positions in the graph, keyed by label
  - **role** — short human-readable label for what this slot is for. Used for display, debugging, and grouping in learning surfaces. Not the prompt — the prompt lives in `meta_prompt`.
  - **meta_prompt** — the templated system prompt for this slot. Non-empty string. May contain template variables that the runtime substitutes at materialization time. This is what gets rendered into the worker's actual prompt.
  - **buddy** — policy for whether this slot becomes its own host with its own Buddy loop: `never`, `always`, or `inherit`
  - **inputs_from** — list of upstream slot labels whose outputs feed into this slot (defines the DAG edges). Absent means the slot has no upstream.
  - **variables** — per-slot variable defaults (model, prompt profile, budget, etc.); merged with run-level defaults and Buddy's per-instance overrides at materialization time
- **terminal** — which slot's output is the subgraph instance's final result

### Template variables in meta prompts

A meta prompt can contain template variables that the runtime substitutes when it materializes the instance. Two flavors exist:

- **Auto-bound variables** resolve from runtime context with no help from Buddy: `{task.text}` (the run's task text), `{inputs.<slot_label>.output}` (an upstream slot's output, valid only when that slot is in the current slot's `inputs_from`), and `{prior_turns[N].terminal_output}` (a previous host turn's terminal output).
- **Buddy-bound variables** are any other `{name}` token. The Scientist writes templates like `"Revise the {plan} based on the {review}"`; on each turn Buddy decides what artifact, literal, or prior-turn output `{plan}` and `{review}` resolve to via `context_bindings` on his authored response.

`subgraph-type-contract.md` is the source of truth for the full variable list, the auto-bound-first resolution rule, and the escape syntax for literal curly braces.

## What a type does NOT contain

- No task-specific content authored per turn — the runtime substitutes task text and upstream outputs via template variables at materialization time
- No Buddy-authored per-slot instructions — under Option 3 that mode is gone; per-slot instruction text lives in the bundle as `meta_prompt`
- No node IDs (labels only — IDs assigned at materialization)
- No actual model outputs
- No runtime state

## Option 3 commitment

Library entries are fully-fixed bundles. Buddy never improvises per-slot instructions on the fly. He picks a type by name, binds any context variables its meta prompts reference, and optionally overrides per-slot variables — that's it.

Why we made this trade:

- **Reproducibility.** The same `type_content_hash` plus the same task plus the same bindings produce literally identical rendered prompts at every slot. That is the load-bearing property the learning surfaces depend on.
- **Clean attribution.** When a row in the buddy-turn table outscores another, we can point at the bundle that was picked instead of disentangling Buddy's authoring choices from the shape.
- **Clean A/B testing.** Two bundle variants can be benched against each other directly. Editing one slot's meta prompt produces a new file with a new hash and a new row in the table.
- **A clearer Scientist role.** Iterating on prompt wording is the Scientist's job: publish a new bundle as a new file, bench it against the old one, keep the winner.

The cost: novel adaptive behavior must be crystallized as a new bundle before Buddy can use it. Buddy cannot author a one-off instruction to handle an unprecedented situation. If the library doesn't yet contain the right pattern, the Scientist authors one. (A future `just_execute` variant with a `{buddy_free_instruction}` literal binding could restore open-ended per-turn instruction authoring for novel cases — not in the seed library, added by the Scientist if and when it's worth the loss of attribution cleanliness.)

## The seeded library (day one)

Only two types ship on day one:

### `just_execute`

The trivial case — one worker, no edges, no nesting. Buddy picks this when the next step is narrow enough to answer in a single shot.

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

Replaces the current `execute_locally` prompt family.

### `delegate_fanout_synthesize`

The classic fan-out — three parallel workers, one synthesizer. Buddy picks this when the next step separates cleanly into independent subtasks.

See the full example above.

Replaces the current `delegate` prompt family.

## Why only two

Between these two, Buddy can compose essentially any workflow as a sequence of turns:
- "Plan, then execute" → two `just_execute` turns
- "Research in parallel then execute" → `delegate_fanout_synthesize` followed by `just_execute`
- "Plan, delegate, consolidate" → `just_execute` then `delegate_fanout_synthesize` then (optionally) `just_execute`
- "Plan, execute steps sequentially, re-evaluate after each" → one `just_execute` per step, interleaved with Buddy's reconsideration

Every richer pattern is expressible as a Buddy composition of these two primitives. You lose nothing expressively by starting small — you just force the complexity into Buddy's sequencing instead of into the type library. The Plan subagent's critique of this direction specifically called out that shipping too many types on day one creates folklore the Scientist then has to unlearn, so starting with two is the conservative play.

## How the library grows

The library grows from **observed recurring patterns** in the run history, not from upfront guesses:

- Run data accumulates with grading scores.
- Scientist clusters runs by task type and studies Buddy's turn sequences alongside the per-slot rendered prompts those turns produced.
- When a particular pattern — a specific shape with specific meta prompts and specific variable defaults — recurs in high-scoring runs, Scientist crystallizes the whole bundle as a new library file.
- The new bundle gets its own content hash and becomes a new option Buddy can pick by name.
- Grading bench compares the new bundle directly against older variants — no need to disentangle Buddy's authoring from the shape, because there is no Buddy authoring inside the bundle.
- Winners stay; losers are archived in a graveyard folder with notes on why they underperformed.

## Type versioning

Types are immutable. A "modification" is always a new file, because changing the `meta_prompt` on any slot — or any other part of the bundle — produces a new content hash. Two variants might differ in meta prompt wording, in slot shape, or in variable defaults; all three are equally valid axes for Scientist experimentation. For example:

- `delegate_fanout_synthesize_v1.json`
- `delegate_fanout_synthesize_v2.json` (e.g., adds a light review slot between workers and synthesizer, or rewords the synthesizer's meta prompt)

Both coexist in the library. Scientist compares them on the bench. The loser gets moved to a graveyard subfolder but is not deleted — its history is valuable.

## Content-addressed type identity

Following the Plan subagent's recommendation: every subgraph instance records a **content hash of the type spec** it was materialized from. Under Option 3 the hash captures the full bundle — shape, every slot's `meta_prompt` text, the optional `buddy_bound_variables` list, and per-slot variable defaults. Editing a single character in any meta prompt produces a new hash.

That is exactly the property the learning surfaces rely on: `chosen_type_content_hash` is a reproducible grouping key. Two types with different names but identical content hashes are structurally equivalent, and two differently-named types that converge to the same spec get automatically recognized as equivalent.

## DAG-only — no loops

Subgraph types are strictly acyclic. There are no back-edges, no iteration, no loop budgets inside a type. If a workflow needs to iterate (e.g., "plan, review, revise, repeat until satisfied"), that iteration is expressed at the Buddy loop level — Buddy picks the review subgraph, sees the result, picks it again with revised bindings, and so on — not inside a single subgraph type. This keeps each subgraph type a clean, finite DAG that always terminates and is trivial to validate.

## Variants as experiments

The primary unit of Scientist experimentation is the bundle variant. The axes the Scientist can vary, each producing a new file with a new content hash:

- **Meta prompt wording** on any given slot
- **Per-slot variable defaults** — model, prompt profile, budget, context policy
- **Slot shape** — adding or removing slots, changing `inputs_from` edges, moving the terminal
- **Buddy policy** on individual slots (`never` vs `always` vs `inherit`)

Each axis produces new bundles with new content hashes. Scientist compares them on the bench. Over time, winners accumulate and the library converges on empirically justified patterns.
