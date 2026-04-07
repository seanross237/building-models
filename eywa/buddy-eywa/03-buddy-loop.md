# 03 — Buddy Loop

## What Buddy is

Buddy is a meta-agent role — a normal node whose prompt family is `pick_subgraph`. Buddy is not a new species of node in the bones; it's just a node with a specific, strategic role, run in a specific way (multi-turn, re-consulted between subgraph executions).

Buddy sits alongside any host node. The host node does no task work directly; instead, Buddy runs a multi-turn loop that decides what work happens in sequence until the host's goal is met.

## What Buddy decides

Per turn, Buddy decides exactly three things:

1. **Which subgraph type to pick, and which context bindings to supply** — name a fully-fixed bundle from the library and resolve every buddy-bound template variable its meta prompts reference. The bindings object is empty when the chosen type declares no buddy-bound variables.
2. **Per-slot variable overrides** (optional) — model, prompt profile, budget, tool access
3. **Whether to declare done** — at any turn, instead of picking a subgraph, Buddy can say "done, here's the final answer for this host" and the host terminates

Buddy never authors per-slot instructions. Per-slot prompts are templated `meta_prompt` strings crystallized in the bundle by the Scientist; the runtime renders them at materialization time using Buddy's `context_bindings` and the runtime's auto-bound variables (`{task.text}`, `{inputs.<slot>.output}`, `{prior_turns[N].terminal_output}`). See `02-subgraph-types.md` for the bundle model.

Under Option 3, Buddy's authoring surface is intentionally minimal: pick a type, bind any context variables the type requires, optionally override per-slot variables. That's it. The bundle owns everything else — shape, edges, prompt wording, defaults. This minimalism is the load-bearing learning property: every turn's decision decomposes cleanly into (which bundle + which bindings + which overrides), and the runtime guarantees reproducibility given those inputs. Iterating on prompt wording is the Scientist's job, not Buddy's.

Buddy does not:
- Invent new subgraph types (that's the Scientist's offline job)
- Author per-slot instructions — those live in the bundle's `meta_prompt` strings
- Execute any task work itself
- Decide routing — routing is baked into the chosen type's edges
- Author anything beyond one of the three things above

## The loop in pseudocode

```
function run_host(task, host_context):
    accumulated_state = { "task": task, "prior_turns": [] }
    for turn_number in 1..max_buddy_turns_per_host:
        buddy_decision = buddy.pick(accumulated_state)

        if buddy_decision.is_done:
            return buddy_decision.final_answer

        subgraph_instance = materialize(
            type = buddy_decision.chosen_type,
            context_bindings = buddy_decision.context_bindings,
            variable_overrides = buddy_decision.variable_overrides,
        )
        terminal_output = expand_subgraph(subgraph_instance)

        accumulated_state.prior_turns.append({
            "turn": turn_number,
            "chosen_type": buddy_decision.chosen_type,
            "context_bindings": buddy_decision.context_bindings,
            "terminal_output": terminal_output,
        })

    # Fell off the end of the budget — treat as terminal.
    return accumulated_state.prior_turns[-1].terminal_output
```

Buddy is re-prompted at the start of each turn with the current `accumulated_state`. Buddy sees everything that's happened so far at this host (which types ran, what they produced, any fail-fast signals, the current artifact inventory) and decides next move.

## What Buddy's prompt looks like conceptually

```
You are the Buddy for a host node working on the following task:

TASK:
{original task}

ARTIFACT INVENTORY:
- plan_v1 (markdown) "3-step plan: research A, implement B, test C"
- research_findings_v1 (json) "12 papers on topic X"

PRIOR TURNS AT THIS HOST:
Turn 1: chose `delegate_fanout_synthesize` with empty context_bindings.
        Terminal output: compiled findings (see research_findings_v1).
Turn 2: chose `just_execute` with empty context_bindings.
        Terminal output: worker 1 succeeded, produced initial implementation.

YOUR CHOICES THIS TURN:
- Pick a subgraph type from the library and bind any context variables it requires
- Declare done with a final answer

LIBRARY OF SUBGRAPH TYPES:
{list of available types with descriptions and their buddy_bound_variables}

OUTPUT (JSON):
{
  "schema_name": "buddy_node_authored_response",
  "schema_version": "v1",
  "turn_decision": "pick_subgraph" | "done",
  "chosen_subgraph_type": "<type name from the library>",
  "context_bindings": { ... },
  "variable_overrides": { ... },
  "decision_notes": "<short rationale>"
}
```

Buddy's prompt is strategic, not tactical. It focuses on "given this state, which bundle in the library is the right next move?" — not on actually doing the work, and not on writing per-slot prompt text.

## Pivots are free

Because Buddy is re-consulted every turn, pivoting happens naturally:

- Turn 1: chose approach A, result was disappointing
- Turn 2: Buddy sees the disappointing result, picks a different approach (pivot)
- Turn 3: new approach runs, maybe better

No new mechanism is needed. Pivoting is just "Buddy makes a different pick on the next turn based on what's in the accumulated state" — a different type, different bindings, or different overrides.

## Fail-fast — the one escape hatch

The single exception to "workers never decide what to do" is the **fail-fast signal**. A worker slot, while executing its assigned work, may author `terminate_subgraph_early` if it becomes clear its assignment is broken or the approach is fundamentally wrong.

When a worker fail-fasts:

1. The engine cancels remaining work in that subgraph (or in v1, lets it finish and ignores it — see `06-learning-surfaces.md` for the cost note)
2. The subgraph instance terminates with the fail-fast result as its terminal output
3. Buddy sees the fail-fast outcome in accumulated state on his next turn
4. Buddy decides what to do about it (pick a different bundle, possibly with different context bindings, re-plan, give up, etc.)

Fail-fast is not strategic. The worker doesn't propose an alternative or suggest what should happen next — it just raises a flag. Strategy is still Buddy's.

## Recursion via nesting

A slot inside a subgraph can have `buddy: always`, which makes that slot itself a host node with its own Buddy loop. When the engine reaches that slot, instead of running it as a single-turn worker, it instantiates a fresh Buddy for it and runs a nested loop. The slot's **rendered_prompt** — its `meta_prompt` after the runtime substitutes all template variables — becomes the nested host's task text.

The nested Buddy follows the exact same rules as the outer Buddy. It picks subgraphs, binds context, composes turns, declares done. When it declares done, the slot's "output" is whatever the nested Buddy produced as its final answer. That output then flows along the outer subgraph's edges like any other slot output.

This is the **one control plane**: Buddy loops, nesting arbitrarily deep, all using the same primitive.

```
Outer host (buddy depth 0)
├── Turn 1: runs subgraph of type T1
│   └── slot "worker_a" (buddy: never) → runs once, produces output
│   └── slot "synthesizer" (buddy: always)
│       │  → Inner host (buddy depth 1)
│       │  ├── Turn 1: runs subgraph of type T2
│       │  │   └── slot "subworker_a" (buddy: never) → runs once
│       │  │   └── slot "subworker_b" (buddy: never) → runs once
│       │  ├── Turn 2: runs subgraph of type T3
│       │  └── Turn 3: declares done, returns final answer
│       │  → Inner host output becomes outer slot's output
├── Turn 2: ... (more outer turns based on inner's result)
```

No new mechanism at any level. Just Buddy loops calling Buddy loops.

## Why multi-turn buddy does NOT create two control planes

A critique of earlier drafts of this direction was: "you have multi-turn execution inside slots AND a multi-turn Buddy loop wrapping them — that's two control planes." The fix, adopted in Buddy-Eywa, is: **slots are strictly single-turn**. A slot without a buddy executes once and produces one output. Any need for multi-turn behavior at a slot is expressed by giving that slot `buddy: always`, which turns it into a host with its own Buddy loop.

This gives exactly one control plane — the Buddy loop — applied recursively. There is no other multi-turn mechanism in the system. The old super-eywa pattern of "a node having multiple internal turns where it decides to delegate or execute" goes away entirely.

## Budget controls

Each host has:

- **`max_buddy_turns_per_host`** — hard cap on how many subgraph executions Buddy can chain together at one host
- **`max_host_depth`** — hard cap on nesting depth (how deep `buddy: always` can nest before the engine refuses)
- **`max_total_nodes_per_run`** — global cap to prevent pathological multiplicative blowups

These are variables like any other, set at run level and overridable per host. They're load-bearing for cost control because nested Buddy loops can multiply.

## What happens when Buddy runs out of turns

If Buddy's budget is exhausted before he declares done, the host terminates with the most recent turn's terminal output as its final answer, plus a "budget_exhausted" flag in the host's record. The outer layer (parent Buddy or the run's final output) sees this and can react. Scientist can study "how often does budget exhaustion happen and which task types trigger it?" as one of the tracked metrics.
