# Primer for Next Session — Starting the Buddy-Eywa Worktree Build

Copy and paste the "Primer message" block below into a fresh Claude session. It assumes Claude starts with no memory of the 2026-04-07 design conversation and needs to be brought up to speed before implementation begins.

---

## Primer message (copy-paste this)

Hey Claude. We're about to start building **Buddy-Eywa** in a new git worktree. Here's what you need to do to get ready:

1. **Read the design snapshot.** Everything we decided on 2026-04-07 is in `/Users/seanross/kingdom_of_god/home-base/eywa/buddy-eywa/`. Start with `README.md`, then read the numbered docs in order:
   - `01-vision.md` — north star and core concept definitions (Buddy, Worker, subgraph, host, slot, Scientist, laboratory, artifact)
   - `02-subgraph-types.md` — the type library, the seed types, why we only ship 2 on day one
   - `03-buddy-loop.md` — the multi-turn Buddy loop, fail-fast, recursion via nesting
   - `04-workers-slots.md` — the single-turn rule and clean division of labor
   - `05-artifacts.md` — the artifact store, two views, versioning
   - `06-learning-surfaces.md` — the three learning surfaces and their trajectory over time
   - `07-relation-to-current.md` — what overlaps with current super-eywa, what changes, what stays
   - `08-implementation-plan.md` — the 14-chunk build order — **this is the roadmap we'll follow**
   - `09-evaluation-and-open-questions.md` — the Plan subagent's eval and unresolved questions
   - `examples/` — three worked examples of the system in action

2. **Familiarize yourself with the current super-eywa codebase** before changing anything. Key files:
   - `/Users/seanross/kingdom_of_god/home-base/eywa/super-eywa/eywa-system/runtime/eywa_runtime/engine.py` — the current execution engine (you'll be splitting `_execute_node` into `expand_node` + `expand_subgraph`)
   - `/Users/seanross/kingdom_of_god/home-base/eywa/super-eywa/eywa-system/runtime/eywa_runtime/prompting.py` — current prompt families (mostly getting replaced; Buddy gets a new prompt builder, workers get a radically simpler one)
   - `/Users/seanross/kingdom_of_god/home-base/eywa/super-eywa/eywa-system/runtime/eywa_runtime/executor.py` — executors (mostly unchanged, just parse new response schemas)
   - `/Users/seanross/kingdom_of_god/home-base/eywa/super-eywa/eywa-system/contracts/` — contracts that get extended (node_packet, node_record, authored_response)

3. **The ground rules for this build** (from the Plan subagent eval, already baked into the design):
   - Slots are **strictly single-turn**. No intra-slot multi-turn behavior. Ever. Any multi-turn need = `buddy: always` + nested Buddy loop.
   - Seed the library with **2 types only**: `just_execute` and `delegate_fanout_synthesize`. Don't ship `plan_3review_consolidate` or other types on day one — they should emerge from the Scientist's analysis later.
   - **No write-time backfill** of old runs. A read-time adapter is the plan if we need historical compatibility.
   - **Defer the Scientist** — just record the data cleanly from day one. Offline learning happens later.
   - Subgraph type specs are **content-hashed** and every instance records the hash.
   - Everything must be **behind a `runtime_mode: buddy_eywa_v1` flag** so the legacy super-eywa path keeps working during coexistence.

4. **Set up the worktree.** We're going to build on a branch off main, in a separate worktree so super-eywa main stays stable:
   ```
   cd /Users/seanross/kingdom_of_god/home-base/eywa/super-eywa
   git worktree add ../super-eywa-buddy buddy-eywa-v1
   cd ../super-eywa-buddy
   ```
   (Confirm with me before running this — I want to pick the branch name.)

5. **The build order is in `08-implementation-plan.md`.** It's 14 chunks. Start with Chunk 1 (contracts). Don't try to jump ahead. Each chunk should leave the system runnable.

6. **Context about Sean's style** (important, won't be in memory since `CLAUDE.md` forbids memory writes):
   - Prefers short formatted responses with line breaks, not paragraphs.
   - Keep responses to ~15 lines unless more detail is genuinely necessary.
   - When making plan docs, they go in `convenience-docs/lil-plans/`.
   - Autonomous build notes go in `sticky-notes/daily-journals/YYYY-MM-DD/` (today: `sticky-notes/daily-journals/2026-04-07/` in whatever worktree you're working in).
   - Don't use `sticky-notes/open-questions/`, `sticky-notes/remember-for-later/`, or `the-do-queue/` for autonomous build notes unless explicitly asked.

7. **Once you've read through the buddy-eywa docs, confirm back to me** what your understanding is and what you think Chunk 1 should look like specifically. Then we'll set up the worktree and start.

Don't start writing code yet. First, read + confirm understanding + propose Chunk 1 specifics. Let's talk before we build.

---

## Notes to self (the current Claude, pre-compact)

- The design docs in this folder are the canonical source of truth for what we agreed on. If anything in a future conversation contradicts them, prefer the docs.
- The key insight is Sean's reframe: **"subgraph = the biggest chunk of work Buddy is willing to commit to autonomously before he reconsults his accumulated wisdom."** This is the load-bearing idea. Everything else (type library, single-turn slots, fail-fast, nested Buddies) is a consequence of trying to express that reframe cleanly.
- The Plan subagent's critique was adopted. The Codex subagent did not return a substantive response and can be rerun later if desired.
- We have not started any implementation. All decisions are paper-only. The worktree build is the next step.
- Sean has been disciplined about keeping me terse. Don't ramble in the first post-compact message. Read, confirm understanding, propose Chunk 1, wait for go-ahead.

---

## Chunk 1 quick reference (what you'll propose first)

Chunk 1 from `08-implementation-plan.md` is writing the contracts:

1. `eywa-system/contracts/subgraph-type-contract.md` — subgraph type spec schema
2. `eywa-system/contracts/subgraph-instance-contract.md` — materialized instance
3. `eywa-system/contracts/artifact-record-contract.md` — artifact metadata schema
4. Extension to `eywa-system/contracts/node-authored-response-contract.md` for the new Buddy `pick_subgraph` decision and the simplified worker response schema

These are all markdown docs, no code. Goal: Sean reads them, signs off on the shapes, and only then do we start writing the loader and validator in Chunk 2.

Every contract should include:
- Purpose
- Required and optional fields
- A concrete JSON example
- Validation rules
- Notes on how it relates to existing contracts

Keep them aligned stylistically with the existing contracts in `eywa-system/contracts/` (read one of them first to match the voice).
