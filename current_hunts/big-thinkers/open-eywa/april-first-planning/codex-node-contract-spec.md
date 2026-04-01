# Codex Node Contract Spec

## Purpose

This document defines a concrete node contract for Open-Eywa's current node-first direction.

It is intended to be:

- concrete enough to audit code against
- concrete enough to design offline tests around
- narrow enough to remain stable through many future iterations

This is a node-first spec, not a general workflow engine spec.

## Core Rule

Open-Eywa should be:

- stable at the node level
- flexible at the agent level
- hard at the protocol level

The practical rule is:

- code owns correctness
- models provide bounded judgment and content

A model may lower output quality, but it must not be able to break correctness.

## 1. What A Node Is

A node is a bounded unit of work with a durable on-disk contract.

A node is the smallest unit that should be:

- inspectable by a human
- validated by code
- measurable across runs
- recoverable after failure
- stable even as agents, prompts, and models change

A node is not one agent, one prompt, or one model session. It is the persistent work container whose truth can be checked on disk.

## 2. What A Node Owns

A node owns:

- its task or goal
- its current status
- its canonical inputs
- its canonical outputs
- its orchestrator control files
- its logs and usage records
- its child relationships
- its execution history on disk

The key principle is:

the node owns truth, not the agent.

## 3. Required Node Shape

Every node must contain these subdirectories:

```text
<node>/
├── input/
├── output/
├── for-orchestrator/
├── system/
└── children/
```

These five directories are part of the node contract.

### Directory Roles

- `input/`
  Human-readable task inputs and prepared context for the node.
- `output/`
  Human-readable results and state artifacts produced for the node.
- `for-orchestrator/`
  Machine-consumable control files used by the orchestrator.
- `system/`
  Machine-room logs, artifacts, run history, and job bookkeeping.
- `children/`
  Child nodes, each of which must obey the same node contract recursively.

## 4. Canonical Files

These files are part of the current v1 node contract.

### Task Source

At least one of these must exist:

- `input/goal.md`
- `input/parent-instructions.md`

Meaning:

- `input/goal.md`
  Root task statement for a root node.
- `input/parent-instructions.md`
  Task statement handed down to a child node.

Every node must have a clear task source on disk.

### Context And Knowledge

- `input/retrieved_relevant_knowledge_from_library.md`

Meaning:

- retrieved or fallback knowledge relevant to the node

### Main Output Artifacts

- `output/plan.md`
- `output/review.md`
- `output/final-output.md`
- `output/state.md`
- `output/escalation.md`

Meaning:

- `plan.md`
  Planning artifact for a planning pass
- `review.md`
  Review artifact for a review pass
- `final-output.md`
  Main success artifact for execution or synthesis
- `state.md`
  Serializable node-local state summary
- `escalation.md`
  Explicit declaration that the node cannot safely continue

### Orchestrator Control Files

- `for-orchestrator/agent-mode`
- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/eval-decision`
- `for-orchestrator/WAITING_FOR_COMPUTATION`
- `for-orchestrator/computation_result`

Meaning:

- `agent-mode`
  The expected current or next role/mode for the node
- `this-nodes-current-status`
  The authoritative node status
- `eval-decision`
  A machine-consumable evaluator or synthesizer decision
- `WAITING_FOR_COMPUTATION`
  Marker that the node is waiting on a background job
- `computation_result`
  Marker that the background job has completed

### Machine-Room Files

Examples under `system/`:

- `agent-loop.jsonl`
- `usage-summary.json`
- `tool-log.jsonl`
- `jobs/`
- `artifacts/`

These are important for observability, but the main truth contract should remain centered on `input/`, `output/`, and `for-orchestrator/`.

## 5. Node Invariants

The following should always hold for a valid node:

- a node has exactly one authoritative current status
- a node has a task source on disk
- a node remains inspectable after success, failure, or escalation
- process exit never counts as success by itself
- correctness is determined by files plus status, not by model confidence
- stale control files must not silently drive fresh transitions
- important node state must be reconstructable from disk
- no single agent run becomes the durable source of truth

## 6. Canonical Status Model

Current canonical statuses:

- `pending`
- `retrieving`
- `running`
- `needs_review`
- `reviewing`
- `needs_decision`
- `deciding`
- `approved`
- `executing`
- `evaluating`
- `waiting_comp`
- `complete`
- `escalated`
- `cancelled`
- `failed`

### Status Meanings

- `pending`
  Node exists and is ready to begin.
- `retrieving`
  Retrieval is the active responsibility.
- `running`
  A direct contributor such as planner or worker is active.
- `needs_review`
  A reviewable plan exists and review has not yet started.
- `reviewing`
  Plan review is active.
- `needs_decision`
  Review is complete and a plan decision is needed.
- `deciding`
  Plan decision is active.
- `approved`
  A plan is approved and execution may begin.
- `executing`
  Child work is the active mechanism of progress.
- `evaluating`
  The node is deciding what to do after child progress or completion.
- `waiting_comp`
  The node is waiting on a background computation.
- `complete`
  The node has satisfied its completion contract.
- `escalated`
  The node has explicitly escalated.
- `cancelled`
  The node was invalidated by parent-level replanning or cancellation.
- `failed`
  The node could not satisfy its contract safely or recoverably.

## 7. Legal Status Transitions

The legal transitions for the current node-first design are:

- `pending -> retrieving`
- `retrieving -> running`
- `retrieving -> failed`
- `running -> needs_review`
- `running -> approved`
- `running -> complete`
- `running -> escalated`
- `running -> waiting_comp`
- `running -> failed`
- `needs_review -> reviewing`
- `reviewing -> needs_decision`
- `reviewing -> failed`
- `needs_decision -> deciding`
- `deciding -> approved`
- `deciding -> escalated`
- `deciding -> failed`
- `approved -> executing`
- `approved -> failed`
- `executing -> evaluating`
- `executing -> failed`
- `evaluating -> executing`
- `evaluating -> approved`
- `evaluating -> complete`
- `evaluating -> escalated`
- `evaluating -> failed`
- `waiting_comp -> running`
- `waiting_comp -> failed`
- `* -> cancelled`
  only when a parent or orchestrator invalidates the node

No other transitions should be considered legal.

## 8. Completion, Failure, Escalation, Cancellation

### Completion

A node is `complete` only when:

- its terminal artifact contract is satisfied
- the required files exist
- the orchestrator can validate them

Completion is a file-and-state fact, not a model feeling.

### Failure

A node is `failed` when:

- it could not satisfy its contract safely
- retry or recovery rules were exhausted
- the failure remains inspectable on disk

### Escalation

A node is `escalated` when:

- it cannot safely continue under current assumptions
- a higher-level decision is required
- the escalation is explicit and inspectable

### Cancellation

A node is `cancelled` when:

- a parent or orchestrator has invalidated it
- it should no longer be treated as an active path of progress

## 9. Agent Run Contract

An agent run is a temporary attempt to advance a node.

### Preconditions For Spawn

Before spawning an agent run:

- the node must be in a status that expects that run
- the task source must exist
- the orchestrator must have written the required instruction/context files
- no competing active run may still control the node

### Allowed Reads

An agent run may read:

- files inside its current node
- approved prompt files
- approved library files
- explicitly prepared parent or child context when the role requires it

The design should increasingly prefer prepared context over asking models to discover critical files on their own.

### Allowed Writes

An agent run may write:

- canonical truth files inside its own node
- machine-room artifacts inside its own node `system/`
- allowed control files such as `for-orchestrator/eval-decision` when its role permits that

An agent run must not directly mutate:

- sibling node truth files
- parent node truth files
- child node truth files
- orchestrator-owned status files

### Success Rule

An agent run is successful only if it leaves behind the required artifacts for its role or phase.

Stopping, timing out, or sounding finished is not enough.

## 10. Current V1 Role-To-Artifact Contract

This is the current v1 role contract inside the node-first design.

### `librarian`

Required success artifact:

- `input/retrieved_relevant_knowledge_from_library.md`

### `planner`

Required success artifact:

- `output/plan.md`

Allowed terminal alternative:

- `output/escalation.md`

### `worker`

Required success artifact:

- `output/final-output.md`

Expected companion artifact:

- `output/state.md`

Allowed terminal alternative:

- `output/escalation.md`

### `plan-reviewer`

Required success artifact:

- `output/review.md`

### `plan-decider`

Required success artifact:

- approved `output/plan.md`

Expected companion artifact:

- `output/state.md`

Allowed terminal alternative:

- `output/escalation.md`

### `mid-plan-evaluator`

Required success artifact:

- `for-orchestrator/eval-decision`

Allowed decision values:

- `continue`
- `replan`
- `escalate`

Expected companion artifact:

- `output/state.md`

### `synthesizer`

Required success artifacts:

- `output/final-output.md`
- `for-orchestrator/eval-decision`

Required decision value:

- `synthesize`

Expected companion artifact:

- `output/state.md`

## 11. Hard In Code Versus Soft In Models

### Hard In Code

Code must own:

- valid state transitions
- required artifacts
- completion checks
- escalation semantics
- path boundaries
- tool boundaries
- duplicate-run prevention
- retry limits
- stale-file cleanup
- logging and metrics schemas
- measurement hooks
- background wait/resume semantics

### Soft In Models

Models may vary on:

- wording
- synthesis style
- planning style
- explanatory detail
- bounded task strategy inside allowed rules

These are quality variables, not correctness variables.

## 12. Observability And A/B Testability

Every node should remain measurable and inspectable.

At minimum, the system should make it possible to reconstruct:

- what task the node had
- what status transitions happened
- which agent runs occurred
- what files were written
- what tools were used
- what tokens and cost were consumed
- how the node terminated

The node should be the main experiment boundary.

That means future experiments should be able to vary:

- agent type
- prompt variant
- tool profile
- context assembly policy
- retry policy
- recovery behavior
- routing thresholds

while keeping the meaning of the node fixed.

## 13. Intentional Flexibility

This spec intentionally leaves these things flexible:

- which agent roles exist in the future
- which models are assigned to which roles
- which prompts are used
- which tool profiles are assigned
- which experiment variants are active
- whether future verification or repair roles are added

Those things should be able to change without changing what a node fundamentally is.

## 14. Node-Only Versus Workflow Pressure Points

This is a node-first spec, but there are places where a future node-plus-workflow design could differ.

The main pressure points are:

- multiple sequential agent types inside one node
- parallel agent execution inside one node
- reusable repair loops
- reusable verification chains
- reusable approval or synthesis recipes

For now, these should be handled inside the node-first framing.

If they become too implicit or too repetitive, that is the moment to explicitly revisit whether a workflow layer is warranted.

## 15. Immediate Use

This spec should now be used for:

- auditing the current Open-Eywa implementation
- identifying where the current system is still too soft
- designing offline simulation and regression tests around node behavior

That is the next step after this document.
