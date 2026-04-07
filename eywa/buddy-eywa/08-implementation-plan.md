# 08 — Implementation Plan

## Guiding rules for the build

1. **Ship in a worktree** — branch off `main`, keep the current super-eywa runtime untouched until the new mode is proven.
2. **Modifications from the Plan subagent eval apply**:
   - Slots are strictly single-turn. No intra-slot multi-turn behavior. Any multi-turn need is expressed via `buddy: always` + nested Buddy loop.
   - Seed the library with 2 types only (`just_execute`, `delegate_fanout_synthesize`). Resist shipping more on day one.
   - Skip the write-time backfill. Use a read-time adapter for historical data if needed.
   - Defer the Scientist. Build the data collection first; invent the offline learner only after real type-level data exists.
   - Subgraph type specs are content-hashed; every instance records the hash for precise grouping.
3. **Land the data shapes before the logic** — contracts first, loader/validator second, engine last. This lets the shapes get reviewed before they're depended on.
4. **Every chunk should leave the system runnable**, even if the new path isn't fully wired up yet. Hide new mode behind a `runtime_mode` variable during the build.

## Chunks in build order

### Chunk 1 — Contracts

**Deliverables:**
- `eywa-system/contracts/subgraph-type-contract.md` — describes the subgraph type spec schema (slots, edges, terminal, per-slot buddy policy, variables)
- `eywa-system/contracts/subgraph-instance-contract.md` — describes the materialized instance (type hash, resolved slot IDs, edges, terminal output)
- `eywa-system/contracts/artifact-record-contract.md` — describes the artifact metadata schema
- Extension to `node-authored-response-contract.md` to describe the new `pick_subgraph` decision for Buddy and the simplified worker response schema

**Acceptance:** contracts review cleanly, JSON examples validate against the schemas, no code yet. Sean reads the contracts and signs off on the shapes.

### Chunk 2 — Type library scaffolding

**Deliverables:**
- New directory `eywa-system/variables/subgraph-types/` with:
  - `just_execute.json` — full spec
  - `delegate_fanout_synthesize.json` — full spec
  - `README.md` — explains the directory, the type format, how the library grows
- `eywa-system/runtime/eywa_runtime/subgraph_library.py` — loader that reads the directory and returns a dict of typed specs
- `eywa-system/runtime/eywa_runtime/subgraph_validation.py` — validator that checks a spec for DAG validity (no cycles, all `inputs_from` resolve, terminal is a real slot, single connected component)
- Unit tests for both

**Acceptance:** both seed types load and validate. A deliberately broken spec (cycle, missing terminal, bad edge) is rejected with a clear error.

### Chunk 3 — Buddy role prompt assembly

**Deliverables:**
- `build_buddy_turn_prompt` function in `prompting.py` that takes `(host_context, accumulated_state, artifact_inventory, library)` and produces a complete prompt for Buddy
- `build_worker_prompt` function that takes `(slot_spec, slot_fill, upstream_inputs, referenced_artifacts)` and produces a complete prompt for a worker
- New prompt profile file for the Buddy role
- Tests: golden snapshots of assembled prompts for a few scenarios

**Acceptance:** given a hand-constructed host context and a library of 2 types, `build_buddy_turn_prompt` produces a readable, task-appropriate strategic prompt with the library rendered as choices.

### Chunk 4 — Authored response parsing

**Deliverables:**
- Extension to `authored_response.py` to parse Buddy's `pick_subgraph` decisions (including `turn_decision: done` and the `slot_fills` structure)
- New parser for `buddy_eywa_worker_response` with its radically simpler schema
- Validation: Buddy's chosen type must exist in the library, slot_fills must cover every slot in the chosen type, the final_answer field is only present when turn_decision is done
- Tests covering happy paths and malformed responses

**Acceptance:** valid Buddy and worker responses parse cleanly, invalid ones produce specific error messages for the engine to recover from.

### Chunk 5 — Engine refactor, part 1 — `expand_node` and single-turn worker path

**Deliverables:**
- New function `expand_node(node_spec, ctx)` in `engine.py` that handles single-turn worker execution using the new worker response schema
- Small `RunContext` dataclass passed through recursive calls (run_id, depth, artifact_store, subgraph_instance_id, etc.)
- Legacy `_execute_node` stays intact; `expand_node` is added alongside it
- The existing engine entry point dispatches on `runtime_mode`: legacy or buddy_eywa_v1
- Tests: a trivial 1-slot `just_execute` subgraph runs end-to-end through the new path

**Acceptance:** running a simple task with `runtime_mode: buddy_eywa_v1` produces a valid run directory where a single worker ran, produced output, and the run terminated cleanly.

### Chunk 6 — Engine refactor, part 2 — `expand_subgraph` with topo scheduler

**Deliverables:**
- New function `expand_subgraph(type, slot_fills, ctx)` in `engine.py`
- Materializer that assigns slot IDs, builds the subgraph instance record, writes the spec and edges to disk under `run_dir/subgraphs/`
- Topological scheduler: sequential for v1, parallel-safe structure so parallelism is a later optimization not a rewrite
- Input gating: a slot doesn't run until all its `inputs_from` sources have produced outputs
- Routing: after a slot runs, its output gets attached to any downstream slots waiting on it
- Tests: a 4-slot `delegate_fanout_synthesize` runs cleanly with 3 workers feeding a synthesizer

**Acceptance:** running a task that uses `delegate_fanout_synthesize` produces a valid run where 3 workers ran (in sequence for v1), their outputs flowed into the synthesizer, and the synthesizer's output is the subgraph's terminal.

### Chunk 7 — Buddy loop driver

**Deliverables:**
- New function `run_host(host_spec, ctx)` that drives the Buddy loop: repeatedly calls Buddy, interprets pick/done, calls `expand_subgraph` for picks, accumulates state, enforces budget, terminates on done or exhaustion
- Host records: each host gets a record on disk describing its loop of Buddy turns and the subgraph instances produced
- `max_buddy_turns_per_host` and related budget variables wired through
- Tests: a host that needs 2 Buddy turns (first a `delegate_fanout_synthesize`, then a `just_execute`) runs cleanly

**Acceptance:** a task that requires multiple strategic decisions produces a run where Buddy picked 2 different subgraphs in sequence and the second picked was informed by the first's terminal output.

### Chunk 8 — Recursion via nesting

**Deliverables:**
- When `expand_subgraph` encounters a slot with `buddy: always`, it calls `run_host` for that slot instead of executing it as a single-turn worker
- Nested host records linked to their parent subgraph instance
- Nesting depth tracking and `max_host_depth` enforcement
- Tests: a subgraph with one slot marked `buddy: always` runs an inner Buddy loop at depth 1, produces a terminal output, and that output flows back up as the slot's output

**Acceptance:** nested runs produce a legible record tree on disk where each host's loop is visible and their outputs compose cleanly.

### Chunk 9 — Fail-fast escape hatch

**Deliverables:**
- Worker response schema already supports `fail_fast: { triggered, reason }` (from Chunk 4)
- Engine logic: when a worker's response has `fail_fast.triggered == true`, the containing subgraph instance terminates immediately with that worker's output as the terminal
- Remaining slots in the subgraph are not run (v1: they're simply skipped; no cancellation of in-flight work because v1 is sequential)
- The fail-fast status is surfaced in the host's accumulated state so Buddy can see it on the next turn
- Tests: a subgraph where one of the workers fail-fasts terminates early, and the next Buddy turn sees the fail-fast in context

**Acceptance:** a worker that raises a fail-fast signal causes its containing subgraph to bail out cleanly, and Buddy gets to see the failure and decide what to do next.

### Chunk 10 — Artifact store

**Deliverables:**
- New module `eywa_runtime/artifacts.py`
- Artifact creation on worker completion: the engine processes `artifacts_created`, writes content + metadata + updates manifest
- Artifact loading for worker prompts: when a slot's `artifact_refs` is non-empty, the engine loads each artifact's content into the worker's user prompt
- Manifest management: one `manifest.json` per run, updated atomically when artifacts are added
- Buddy-turn prompts include the artifact inventory block
- Tests: a worker creates an artifact, the next slot reads it by reference, the next Buddy turn sees the summary in its inventory

**Acceptance:** artifacts flow end-to-end: created by a worker, consumed by a downstream worker, summarized for Buddy.

### Chunk 11 — Learning surface recording

**Deliverables:**
- On every Buddy turn, append a row to `run_dir/derived/buddy-turns.jsonl` (and aggregate across runs to `data-system/laboratory/buddy-turns/`)
- On every slot execution, append a row to `run_dir/derived/slot-executions.jsonl` (and aggregate to `data-system/laboratory/slot-executions/`)
- On every artifact reference, append a row to `run_dir/derived/artifact-usages.jsonl`
- Rich context in each row: prompt snapshots, prior state summaries, full variable sets, downstream placeholder fields for grading scores to be filled in later
- Supabase sync extension: the three new tables get synced alongside the existing derived views

**Acceptance:** a completed bench run leaves behind three populated learning-surface files that an offline analysis script can load and query.

### Chunk 12 — Grading bench integration

**Deliverables:**
- Grading bench runs `runtime_mode: buddy_eywa_v1` alongside `runtime_mode: legacy` for the same question set
- Results are compared and recorded
- No changes to the grading scoring logic itself — just a new mode to run

**Acceptance:** a single `run_clean_benchmark_v1.py` invocation can run both modes and produce comparable scores.

### Chunk 13 — DAG-aware story view

**Deliverables:**
- Extension to `story.py` and `timeline.md` generation to handle DAG-shaped runs
- Render nested Buddy loops legibly
- Show subgraph instances as boxes with their slots and edges
- Still text/markdown for v1; a richer visualizer can come later

**Acceptance:** a nested multi-turn run produces a human-readable story doc that a reader can follow without pulling up the raw JSON.

### Chunk 14 — Cleanup and hardening

**Deliverables:**
- Remove dead code from the coexistence period if ready
- Document the finalized runtime mode switch
- Add CLI flags for `run_live_batch_v1.py` to pick the runtime mode
- Error messages polished

**Acceptance:** a reader coming to the codebase fresh can follow the new path cleanly, and the legacy path is either retired or clearly marked as deprecated.

## Order-of-operations notes

- Chunks 1, 2, 3 can happen in parallel if multiple people are working, but should all land before Chunks 4+ depend on them.
- Chunks 5 and 6 together are the heart of the engine refactor. Budget the most implementation time for these.
- Chunk 8 (nesting) should not be rushed — nested recursion is where subtle bugs hide. Do it after 5, 6, and 7 are all stable.
- Chunks 9 (fail-fast) and 10 (artifacts) are independent of each other and can happen in either order.
- Chunk 11 (learning surfaces) should land as early as possible in the build, even with mostly empty rows, so that later chunks automatically populate it as they come online.

## Worktree setup

```
git worktree add ../super-eywa-buddy worktree-branch
cd ../super-eywa-buddy
```

All buddy-eywa work happens in the worktree. Main stays stable. Periodically merge main into the worktree to stay current with grading/runtime fixes. When the worktree is ready to replace main, cut a PR with the final state.

## Out of scope for v1

These are deliberately deferred:

- True mid-flight cancellation (workers 2 and 3 still finish even if worker 1 fail-fasts)
- Parallel slot execution within a subgraph (the topo scheduler runs sequentially in v1)
- Automated subgraph type generation or learned Buddy policies
- Tool-based artifact reads (content is inlined into worker prompts in v1)
- Rich DAG visualizer (markdown story view is enough for v1)
- Scientist as an offline agent; Scientist is a human-run analysis function in v1

Each of these is a clean v2 feature that doesn't require re-architecting the bones.
