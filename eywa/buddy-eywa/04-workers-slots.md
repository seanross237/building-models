# 04 — Workers and Slots

## The one-line rule

**Buddy chooses. Workers do.**

Buddy is strategic. Workers are tactical. Workers execute their one assigned job, produce their output, and stop. They never choose what comes next. Anything that looks like a strategic decision at runtime is a Buddy decision, not a worker decision.

## What a slot is

A slot is a labeled position in a subgraph type. When Buddy picks a type and the engine materializes it, each slot becomes one worker node in the run graph.

A slot has:

- A **label** — its name within the type (e.g., `worker_a`, `synthesizer`, `planner`)
- A **role** — a short human-readable label for what this slot is for. Used for display, debugging, and grouping in learning surfaces. Not the prompt — the prompt lives in `meta_prompt`.
- A **meta_prompt** — the full templated system prompt for this slot. Lives on the slot in the bundle. May contain template variables: auto-bound ones that the runtime resolves from runtime context (`{task.text}`, `{inputs.<slot_label>.output}`, `{prior_turns[N].terminal_output}`), or buddy-bound ones (any other `{name}` token) that Buddy resolves via `context_bindings`. See `02-subgraph-types.md` and `subgraph-type-contract.md` for the full spec.
- A **buddy policy** — `never` (single-turn worker), `always` (becomes its own host), or `inherit` (follows the outer policy)
- An **inputs_from list** — which other slots' outputs feed into it (absent means no upstream)
- **Variables** — default model, prompt profile, budget, tools, overridable at runtime

### From `meta_prompt` to `rendered_prompt`

When the engine materializes a subgraph instance, it walks every slot and renders the templated `meta_prompt` into the exact prompt text the worker will see. Auto-bound variables are resolved from runtime context (the run's task text, upstream slot outputs, prior host turns). Buddy-bound variables are resolved from the `context_bindings` object Buddy authored on his `pick_subgraph` response for this turn. The substituted text is written to `slots_resolved[label].rendered_prompt` on the instance record.

`rendered_prompt` is what the worker actually sees. Two instances with the same `type_content_hash` and the same task + state produce literally identical `rendered_prompt` values at every slot — that is the reproducibility property the learning surfaces depend on.

## What a worker authors per execution

A worker's authored response schema is **radically simpler** than current super-eywa's authored response. There are no orchestration decisions to choose between. There is no `delegate` vs `execute_locally` vs `transmute` vs `review` branching. A worker produces one output shape:

```json
{
  "schema_name": "buddy_eywa_worker_response",
  "schema_version": "v1",
  "output": "the worker's actual result content",
  "output_summary": "one-line description for Buddy's inventory view",
  "result_type": "optional tag: summary | plan | code | data | finding | ...",
  "artifacts_created": [
    { "title": "...", "type": "text_markdown", "content": "...", "summary": "..." }
  ],
  "fail_fast": {
    "triggered": false,
    "reason": null
  }
}
```

The only optional escape hatch is `fail_fast`, which a worker may set if the assignment can't be completed and the whole subgraph should bail early.

## What a worker's prompt looks like

Because the authored response is so much simpler, the worker's prompt is also much simpler than today's orchestration-heavy prompts. The worker sees the slot's `rendered_prompt` — the bundle's `meta_prompt` after the runtime has substituted every template variable — plus the output JSON schema. Nothing else. Buddy does not hand the worker a custom string at any point.

Concrete example: Buddy picks `delegate_fanout_synthesize` on a turn where the task text is "Write a 600-word general-audience summary of the historical context of the Riemann hypothesis from 1859 to today." The `worker_1` slot's meta prompt from the seed bundle contains a `{task.text}` token. After the runtime substitutes it, the worker sees:

```
[slot role: handle the first independent piece of the task]

You are worker 1 in a three-way fan-out. Your task:

Write a 600-word general-audience summary of the historical context of the
Riemann hypothesis from 1859 to today.

Handle the first independent piece of this task. Return a compact bullet-point
summary of your findings or output. Do not attempt to cover the other two
pieces — other workers handle those.

OUTPUT (JSON):
{
  "output": "...",
  "output_summary": "...",
  "result_type": "...",
  "artifacts_created": [...],
  "fail_fast": { "triggered": false }
}

You may set fail_fast.triggered to true if the assignment is broken or reveals
the approach cannot succeed. Do not suggest alternatives — just explain the
reason. Buddy decides what to do about it.
```

For the `synthesizer` slot, the same rendering step substitutes `{inputs.worker_1.output}`, `{inputs.worker_2.output}`, and `{inputs.worker_3.output}` incrementally, once each upstream slot has produced output. When a slot's meta prompt includes a buddy-bound variable whose `binding_type` is `"artifact"`, the runtime loads that artifact's content and substitutes it into the rendered prompt just like any other value — there is no separate "referenced artifacts" section, the bundle decides where artifact content lands.

Crucially, the worker's prompt does NOT include any of the orchestration decision machinery that currently lives in `eywa-system/runtime/eywa_runtime/prompting.py`. No JSON schemas for `delegate_example` or `transmute_example` or `review_example`. The worker has one job and one output shape.

## Single-turn rule

A slot with `buddy: never` executes **exactly once**. The engine materializes it, renders its meta prompt into `rendered_prompt`, runs the executor against that rendered prompt, parses the authored response, records the node, and moves on. There is no loop, no retry, no "decide what to do next" phase.

A slot with `buddy: always` does not execute as a worker at all. Instead, the engine spawns a Buddy for it and runs a nested Buddy loop, with the slot's `rendered_prompt` as the nested host's task text. When that inner loop terminates, its final answer becomes the slot's output. From the outer subgraph's perspective, the slot still produced one output — the multi-turn work happened inside a nested host, not inside the slot itself.

There is no third option. Slots are either single-turn workers or hosts-with-buddies.

## The division of labor, by example

Imagine the task: "Write a blog post about quantum computing for a general audience."

Buddy's decisions (strategic), turn by turn:

- **Turn 1.** Buddy reads the task and picks `delegate_fanout_synthesize`. The seed bundle declares no buddy-bound variables, so `context_bindings` is `{}`. Buddy might add a variable override (e.g., bump the synthesizer's model, or tighten its budget), but that's it — no per-slot instruction authoring. The runtime renders each slot's `meta_prompt` by substituting `{task.text}` with the blog post task text, so all three worker slots see the same task text and the same surrounding instructions; the synthesizer sees the same task text plus `{inputs.worker_N.output}` resolved once each upstream slot completes.
- **Turn 2.** The draft comes back as turn 1's terminal output. Buddy notices the draft uses several technical terms without definitions and wants a glossary appended. See the "escape hatch" discussion below — under Option 3 there's no clean way to say "append a glossary section to the draft" with only the two seed bundles, and this is where the seed library's limits show.
- **Turn 3 (or whenever satisfied).** Buddy declares done with the (possibly revised) draft as the final answer.

Worker executions (tactical):

- `worker_1`, `worker_2`, `worker_3` in turn 1: each reads its rendered prompt — the bundle's "handle the first / second / third independent piece" meta prompt with `{task.text}` substituted — and produces bullet-point output. Done.
- Synthesizer in turn 1: reads its rendered prompt with all three workers' outputs substituted in, produces the draft. Done.

Notice: none of the workers ever think about "should I delegate?" or "should I transmute?" or "should I call a reviewer?" They just do their one thing. All strategic decisions were Buddy's, made at turn boundaries.

### Being honest about the seed library

The seed `delegate_fanout_synthesize` bundle does not assign specific angles to its three workers — each meta prompt just says "handle the first / second / third independent piece." The workers differentiate in practice only because they're told to cover different pieces of the same task, and each picks its own angle. A richer bundle variant with specific researcher roles (e.g., `researcher_physics`, `researcher_applications`, `researcher_history` slots, each with its own meta prompt) would be a Scientist-published bundle Buddy could pick when those specific angles fit.

Turn 2 is the harder honesty. Under Option 3, "add a glossary section to this draft" has to come from one of:

- A dedicated bundle whose meta prompt says something like `"Add a glossary section to the following draft:\n\n{prior_turns[0].terminal_output}"`. Ideal — fully fixed, cleanly attributable — but not in the seed library.
- A `just_execute_with_buddy_instruction` bundle whose meta prompt contains a `{buddy_free_instruction}` buddy-bound variable (a literal binding Buddy fills in per turn), restoring open-ended per-turn instruction authoring. The "escape hatch" pattern flagged in `02-subgraph-types.md`'s Option 3 commitment section. Also not in the seed library.

Neither bundle exists on day one, so on day one Buddy cannot express "append a glossary" as a clean second turn. This is a real seed-library limitation, not a design mistake: novel adaptive behavior must be crystallized by the Scientist as a new bundle before Buddy can use it, and the seed library deliberately ships small.

## Why this makes learning cleaner

Current super-eywa mixes strategic and tactical signals in every authored response. When a node chose to `delegate`, was that a good strategic choice (yes, the task decomposed well) or a good tactical execution (yes, the subtasks were well-written)? The signal is tangled.

Buddy-Eywa separates them:

- **Strategic signal** — was Buddy's turn-by-turn pick (bundle + context bindings + optional variable overrides) the right sequence for this task? Studied via the buddy-turn table.
- **Tactical signal** — given a worker's `rendered_prompt` and its upstream inputs, was its output strong? Studied via the slot-execution table.

Each signal can be optimized independently. A tactical improvement (e.g., a better meta prompt on a specific slot, published as a new bundle variant with a new content hash) benefits every turn where Buddy picks that bundle, without touching Buddy's strategic layer. A strategic improvement (e.g., Buddy learns that for task class X, `delegate_fanout_synthesize` beats `just_execute`) works regardless of the specific meta prompts inside the bundles.

The slot-execution learning surface groups rows by `(type_content_hash, slot_label)`. Under Option 3 every execution of the same slot in the same bundle sees the same meta prompt after substitution (given the same task + state), so the attribution of outcome-to-prompt is crisp: a row's outcome is caused by exactly the rendered prompt that row captured, and every row in the group shares the same underlying `meta_prompt` template.

## What goes away from current super-eywa

The worker simplification means several things that currently exist in super-eywa become unnecessary:

- The `prompt_family` variable on regular nodes (only Buddy uses `pick_subgraph`)
- The `agent_orchestration_basic_instruction_prompt` profile
- The orchestration decision schema with its multiple branches
- The `allowed_decisions` logic in the engine that restricts which orchestration decisions a node can author based on its prompt family
- The multi-turn loop inside `_execute_node` that re-prompts a node after child results come back
- Any notion of per-slot instruction authoring at either the worker or the Buddy level — per-slot prompts live in the bundle as `meta_prompt` strings, rendered by the runtime, full stop

All of that complexity was doing double duty as both "run a node" and "decide what happens next." Buddy-Eywa splits those two jobs into two separate node types (worker and Buddy), and the worker gets the simple half — execute the rendered prompt, return the one output shape, stop.
