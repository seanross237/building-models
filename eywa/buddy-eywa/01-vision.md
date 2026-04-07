# 01 — Vision

## The north star

Super-Eywa's original north star was: a machine whose behavior is increasingly learnable through explicit variables, and whose structure is increasingly improvable through behavior-preserving changes to the bones.

Buddy-Eywa pushes that further by separating **strategic decisions** from **tactical execution** so cleanly that each becomes its own learning surface, and by expressing workflows as **composable, reusable subgraph types** that grow into a catalog over time.

## The core reframe

> A subgraph is the biggest chunk of work we're willing to commit to autonomously before Buddy reconsults his accumulated wisdom.

This single sentence is the load-bearing idea.

- **Buddy** is the one who owns the meta-knowledge of what has worked historically. He sets the checkpoints.
- **A subgraph** is the bounded burst of autonomy between checkpoints.
- **Workers (slots)** inside a subgraph do their one assigned job and produce their output. They never choose what comes next.
- All adaptation, pivoting, re-planning, and strategic reconsideration happens at **Buddy turn boundaries**, not inside subgraphs.

This reframe resolves a tension that earlier drafts of this design had: if you allow adaptation inside a subgraph (via multi-turn slots or reactive supervisors), you end up with two control planes — one inside subgraphs and one wrapping them. By pushing all adaptation out to Buddy checkpoints, you get exactly one control plane. It nests recursively via `buddy: always` on individual slots, but every level uses the same primitive.

## Key concept definitions

**Buddy** — a meta-agent role. A normal node whose prompt family is `pick_subgraph`. Runs in a multi-turn loop at any host node. Each turn, Buddy looks at the task plus accumulated context and either picks a subgraph type to run next or declares "done, here's the answer." Buddy is strategic, not tactical. Buddy never executes task work directly.

**Worker (or slot)** — a node that executes one assignment, in one turn, producing one output. Workers never choose what comes next. The only thing they can do besides produce their output is author a fail-fast signal when it becomes clear their assignment is broken.

**Host node** — any node whose execution is managed by a Buddy loop. The root of a run is always a host node. Any slot inside a subgraph that has `buddy: always` also becomes a host.

**Subgraph type** — a named, reusable, fully-fixed bundle for a small graph of worker slots, living as a file in the type library. Defines: labeled slots, a templated `meta_prompt` per slot, edges (`inputs_from`), a terminal slot, per-slot variable defaults, and per-slot `buddy` policy (`never`/`always`/`inherit`).

**Subgraph instance** — the live, materialized version of a subgraph type, created when Buddy picks that type, populates the runtime's `context_bindings` for any buddy-bound template variables the type's meta prompts reference, and optionally adds per-slot `variable_overrides`. Gets a unique ID, lives under the run directory, records its own execution trace.

**Slot** — one labeled position in a subgraph type. Becomes a worker node when the type is instantiated. Can have its own variable overrides and a `buddy` policy.

**Scientist** — an offline agent that experiments with run history and grading bench scores. Invents new subgraph types, refines existing ones, retires bad variants. Works in the laboratory, not the runtime.

**Laboratory** — the folder / system where run history and the subgraph type library live together, alongside tooling the Scientist uses to study past runs and propose new types.

**Artifact** — a piece of content (file, document, code, data) that's too large or too structural to pass through Buddy's context window. Lives in a per-run artifact store. Workers create and read artifacts by ID; Buddy sees only summary cards.

## The two (really three) learning surfaces

The separation of strategic from tactical gives the Scientist independent learning surfaces:

1. **Buddy-turn table** — one row per Buddy decision, answering "what subgraph types work best in what contexts?"
2. **Slot-execution table** — one row per worker execution, answering "what prompt profiles, models, and variables work best for what kinds of assignments?"
3. **Artifact-usage table** — one row per artifact use, answering "what kinds of artifacts produced by which slots are most valuable to which downstream slots?"

Each surface has its own sample size, signal-to-noise ratio, and time scale. Separating them means each can be optimized independently without interference.

## What success looks like

- A run is legible as a tree of Buddy loops, each loop a sequence of DAG subgraph runs, each DAG a set of single-turn workers.
- The subgraph type library starts with 2 entries and grows organically from observed high-scoring patterns in the run history.
- Buddy's decisions and worker executions accumulate as structured tables the Scientist can study and improve over time.
- Adding new workflow patterns is a matter of the Scientist dropping a new JSON file in the library, not writing new runtime code.
- Old super-eywa prompt families (`execute`, `transmute`, `delegate`, `review`) are expressible as entries in the new library, so no expressive power is lost.
