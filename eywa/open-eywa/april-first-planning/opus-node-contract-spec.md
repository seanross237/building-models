# Open-Eywa Node Contract Spec

This is the concrete contract for what a node is, what it contains, what can happen to it, and what must always be true about it. It is written to be auditable against an implementation and testable offline.

---

## 1. What A Node Fundamentally Is

A node is a directory on disk that represents one bounded unit of work.

It is the stable unit of truth in Open-Eywa. A node persists across agent runs, model changes, prompt changes, and configuration changes. It is the thing you point at and ask: what was the goal, what happened, what was produced, how much did it cost, and is it done.

A node does not know what agent will work on it. It does not care what model is used, what prompt is written, or what tools are available. Those are supplied externally. The node only knows: here is my goal, here is my status, here are my artifacts.

A node can have children. Each child is a complete node with the same structure.

---

## 2. What A Node Must Contain

Every node has exactly five subdirectories:

```
<node>/
  input/             # what the node was given to work with
  output/            # what agents produced
  for-orchestrator/  # control state the orchestrator reads and writes
  system/            # run history, logs, internal bookkeeping
  children/          # child nodes (may be empty)
```

No other top-level entries. If a node directory exists, all five subdirectories exist. They are created together when the node is created.

---

## 3. Canonical Directories And Files

### input/

| File | Written by | Mutability | Purpose |
|---|---|---|---|
| `goal.md` | orchestrator | immutable | The task. Root nodes only. |
| `parent-instructions.md` | orchestrator | immutable | The task. Child nodes only. |
| `context.md` | orchestrator | immutable | Accumulated context from prior sibling steps. Optional. |
| `knowledge.md` | librarian agent | write-once | Library retrieval results. Written during retrieval phase. |
| `instructions-<role>.md` | orchestrator | regenerated per spawn | Assembled context and instructions for a specific agent run. |

A node must have exactly one of `goal.md` or `parent-instructions.md`.

### output/

| File | Written by | Purpose |
|---|---|---|
| `plan.md` | planner agent | The decomposition of the task into steps. |
| `review.md` | plan-reviewer agent | Critique of the plan. |
| `final-output.md` | worker or synthesizer agent | The terminal work product. Required for completion. |
| `state.md` | any agent | Running notes and breadcrumbs for later runs. Advisory only — the orchestrator never gates decisions on it. |
| `escalation.md` | any escalation-eligible agent | Explanation of why the node cannot continue. Required for escalation. |

Agents may write additional files into `output/`. Those files are not part of the contract but are not forbidden.

### for-orchestrator/

| File | Written by | Content |
|---|---|---|
| `status` | orchestrator only | Current status. One of the five legal values. |
| `phase` | orchestrator only | Current sub-phase of `running`. Informational — never used as a gate. |
| `outcome` | orchestrator only | Terminal outcome. Written when status becomes `done`. |
| `failure-reason` | orchestrator only | Why the node failed or timed out. Written at terminal transition. |
| `mode` | orchestrator | Which role should run on this node: `planner`, `worker`, etc. |
| `eval-decision` | evaluator or synthesizer agent | Routing decision. Consumed and deleted by the orchestrator after reading. |
| `cost.json` | orchestrator | Cost tracking. See cost section. |
| `waiting` | agent (via background job tool) | Marker: background computation in progress. |
| `computation-result` | background job script | Marker: background computation finished. |

`status` is the single most important file in the system. Only the orchestrator writes it. Every write is logged.

`eval-decision` is ephemeral. The orchestrator reads it, acts on it, and deletes it. If the file exists when a new evaluator is about to be spawned, the orchestrator deletes it first. Stale decision files must never drive fresh transitions.

### system/

```
system/
  runs/
    run-001/
      meta.json         # structured record of what happened in this run
      loop.jsonl        # per-turn agent loop log
      usage.json        # token and cost summary
      stdout.log
      stderr.log
    run-002/
      ...
  artifacts/            # generated scripts and intermediate files
  jobs/                 # background computation metadata
```

Run directories are numbered monotonically and never overwritten. Each is independently inspectable. Nothing in `system/` is read by agents.

### children/

```
children/
  step-01-<slug>/       # a complete node, same structure recursively
  step-02-<slug>/
```

Children are created by the orchestrator, never by agents. Each child is an independent node.

---

## 4. The Minimal Status Model

Five statuses. Closed enum. This never grows.

| Status | Meaning |
|---|---|
| `pending` | Created but no work has started. |
| `running` | Work is in progress. |
| `done` | Terminal. The node reached a conclusion. Check outcome for what kind. |
| `failed` | Terminal. The node could not complete and recovery was exhausted. Check failure reason. |
| `timed_out` | Terminal. An infrastructure-level timeout. Distinct from `failed` because retry strategy differs: timeouts are retried with the same input; failures are escalated or abandoned. |

When status is `running`, the orchestrator also writes a **phase** to indicate what is currently happening (retrieving, planning, reviewing, deciding, executing, evaluating, synthesizing, working, waiting for computation). Phase is informational and open — new phases can be added without changing the state machine. Phase is never used to gate orchestrator decisions.

When status is `done`, the orchestrator writes an **outcome**:

| Outcome | Meaning | Required artifact |
|---|---|---|
| `completed` | Produced the required output | `output/final-output.md` |
| `escalated` | Explicitly punted to parent | `output/escalation.md` |
| `cancelled` | Parent killed this node | none |

When status is `failed` or `timed_out`, the orchestrator writes a **failure reason**: `cost_cap_exceeded`, `max_retries_exceeded`, `zombie_detected`, `api_timeout`, or `no_artifacts_produced`. New reasons can be added as discovered.

---

## 5. Legal Status Transitions

```
pending  -> running
pending  -> done          (cancellation only)
pending  -> failed        (cost cap exceeded at creation)
running  -> done
running  -> failed
running  -> timed_out
```

No other transitions are legal. Terminal statuses have no outgoing transitions.

Every transition uses an expected-value check: the orchestrator reads the current status, confirms it matches what it expects, then writes the new value. If the current status has already changed, the write is silently skipped. Every successful transition is logged to the orchestrator event log.

---

## 6. Completion, Failure, Escalation, And Cancellation

### Completion

A node is complete when its status is `done`, its outcome is `completed`, and `output/final-output.md` exists on disk. The orchestrator validates this before writing the terminal status. Process exit alone is never sufficient. A model saying "I'm done" is never sufficient. The file must exist.

### Failure

A node has failed when its status is `failed` or `timed_out` and a failure reason file explains why. Failure is always orchestrator-driven. Agents do not fail themselves. They produce output, escalate, or crash. The orchestrator detects the condition and makes it explicit.

### Escalation

A node has escalated when its status is `done`, its outcome is `escalated`, and `output/escalation.md` exists. Escalation means: this node cannot complete its goal under current assumptions, and the parent needs to decide what to do. It is an explicit, inspectable terminal state.

### Cancellation

A node is cancelled when its status is `done` and its outcome is `cancelled`. This happens when a parent replans and the node is no longer needed. The orchestrator sets it directly. No agent is involved.

---

## 7. What An Agent Run Is

An agent run is a single process that temporarily works inside a node.

It reads the node's prepared context, uses allowed tools, writes artifacts into the node, and exits. It has no persistent identity. If the orchestrator needs more work, it spawns a fresh run that reconstructs context entirely from files on disk. There is no session continuity between runs.

A single node may see many runs over its lifetime — a librarian, then a planner, then a reviewer, then a decider, then evaluators and a synthesizer. At most one run is active at any time.

Each run produces a structured record under `system/runs/run-NNN/` with: the role it played, the model it used, when it started and finished, how many loop iterations it took, how many tokens it consumed, what it cost, what artifacts it produced, and why it exited. The run number increments monotonically and is never reused.

The run record also includes a `variant` field (currently empty). When A/B testing is implemented, this is where variant identifiers go.

---

## 8. What An Agent Run May Read And Write

### Read access

An agent may read any file inside the Open-Eywa repository. This is deliberately permissive — agents need context from the library, from prior sibling outputs (assembled by the orchestrator into `input/`), and from their own node's state.

### Write access

An agent may only write inside its own node directory:

| Location | Who may write |
|---|---|
| `input/knowledge.md` | librarian |
| `output/*` | any role (role-specific artifacts) |
| `for-orchestrator/eval-decision` | evaluator and synthesizer |
| `for-orchestrator/waiting` | any role, via background job tool |
| `system/artifacts/*` | any role (generated scripts) |
| `system/jobs/*` | any role, via background job tool |

### Hard boundaries

Agents must never write to:

- `for-orchestrator/status`, `phase`, `outcome`, `failure-reason`, `mode`, or `cost.json`
- Any file outside their own node directory
- Any location inside `children/`

These boundaries are enforced by the tool layer. They do not depend on the model choosing to comply.

---

## 9. What Must Be Hard In Code Vs. Soft In Model Behavior

### Hard: enforced in code, tested offline

| Rule | Why it must be hard |
|---|---|
| Status only transitions through the legal set | A wrong transition silently corrupts the node |
| Only the orchestrator writes status | An agent writing its own status makes correctness uncheckable |
| Completion requires the terminal artifact on disk | Process exit is not proof of success |
| Cost cap is a hard kill, no model consultation | Runaway cost is a production-level failure |
| One active run per node at a time | Concurrent runs corrupt shared files |
| Agents cannot write outside their node | Cross-node corruption is the worst silent failure |
| Stale eval-decision files are deleted before new evaluator spawns | Stale decisions driving fresh transitions is a silent corruption |
| Run records are append-only and monotonically numbered | Overwriting history destroys inspectability |
| Every status transition is logged | The log is how the node's history becomes recoverable |
| Cost is updated synchronously after every run exit | Cost must be current before the next decision |

### Soft: model judgment, quality-sensitive but not safety-critical

| Behavior | Why it can be soft |
|---|---|
| How a plan decomposes a task | Many valid decompositions exist |
| How a review critiques a plan | Quality matters, but it is a judgment call |
| How a worker reasons through a task | The contract is the output file, not the process |
| How a synthesizer combines child outputs | Judgment call |
| How an evaluator decides continue/replan/escalate | Judgment call — but the decision value is validated to be one of the legal strings |
| The wording and style of any markdown artifact | Artifacts are for humans; the protocol checks file existence, not prose quality |

The guiding test: if a model behaved unexpectedly here, could the system still remain correct and inspectable? If no, the behavior belongs on the hard side.

---

## 10. Invariants

These must hold for any valid node at any point in time. They are the foundation for offline tests.

### Status invariants

1. Every node has a `for-orchestrator/status` file containing exactly one of the five legal values.
2. A node with status `done` has a `for-orchestrator/outcome` file containing one of: `completed`, `escalated`, `cancelled`.
3. A node with status `failed` or `timed_out` has a `for-orchestrator/failure-reason` file.
4. A node with outcome `completed` has `output/final-output.md`.
5. A node with outcome `escalated` has `output/escalation.md`.
6. No node in a terminal status ever transitions again.

### Run invariants

7. At most one agent run is active per node at any time.
8. Run directories under `system/runs/` are monotonically numbered and never reused or overwritten.
9. Every completed run has a `meta.json` with all required fields.
10. `for-orchestrator/cost.json` is updated after every run exit, before the orchestrator takes any further action on that node.

### Tree invariants

11. Every node has exactly one of `input/goal.md` or `input/parent-instructions.md`.
12. Children are only created by the orchestrator.
13. A node's `children_usd` in `cost.json` equals the sum of its children's `total_usd`.

### Boundary invariants

14. Agents can only write inside their own node directory.
15. Agents never write to `for-orchestrator/status`, `phase`, `outcome`, `failure-reason`, `mode`, or `cost.json`.
16. Every status transition is logged to the orchestrator event log.

---

## 11. What Is Intentionally Left Flexible

These parts of the design are deliberately not locked down. They are the seams where future agents, future experiments, and future A/B tests can vary without breaking the contract.

### The phase list is open

New phases can be added by adding an enum value and setting it in the orchestrator at the right moment. The state machine does not change.

### The failure reason list is open

New reasons can be added as they are discovered. The state machine does not branch on reasons.

### The role set is open

Adding a new role requires: a system prompt, a row in the artifact requirements table, a config entry, and orchestrator routing logic. The status enum, the directory layout, and the validation functions do not change.

### Model, prompt, and tool selection are config

Which model runs which role, which prompt template is used, and which tools are enabled are all external to the node contract. They can be varied per-mission, per-node, or per-experiment without touching the contract.

### The variant field in run records is a placeholder for A/B testing

The node is the stable comparison boundary. The variant field tags what was different about a specific run. When experiments are implemented, this is the hook. The node contract does not need to change.

### Orchestrator decision logic is not part of the contract

How the orchestrator decides what to do next (the routing rules, the decision table, the tick function) is implementation. The contract defines what those decisions operate on. The orchestrator can be refactored freely as long as the invariants hold.

### Workflow sequencing is not part of the contract

The order in which roles run inside a node (retrieve -> plan -> review -> decide -> execute -> evaluate -> synthesize) is orchestrator logic, not a node rule. The contract says what each role must produce and what terminal states are legal.

> **Workflow boundary note:** If we later need reusable workflow recipes (e.g., "research nodes always do retrieval then planning then review"), that can be added as a layer above the node contract — a template that tells the orchestrator which roles to sequence. The node contract stays the same. The node remains the stable unit; the workflow becomes a configurable pattern that drives routing. This is a natural extension point but is not needed for v1.

### Parallel child execution is a future extension

This spec assumes sequential child execution. Parallel execution would change orchestrator routing but would not change the node directory structure, status model, or invariants.
