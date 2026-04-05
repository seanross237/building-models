# Canonical Node Contract Spec

## Purpose

This is the landed node contract for Open-Eywa's current foundation phase.

It is intended to be:

- concrete enough to audit code against
- concrete enough to build offline simulation tests around
- narrow enough to stay stable through many future agent and system changes

This is a node-first contract. It does not define a full workflow system.

## Core Rule

Open-Eywa should be:

- stable at the node level
- flexible at the agent level
- hard at the protocol level

The practical rule is:

- code owns correctness
- models provide bounded judgment and content

A model may lower quality, but it must not be able to break correctness.

## 1. What A Node Is

A node is a bounded unit of work with a durable on-disk contract.

A node is the stable unit of:

- truth
- inspection
- measurement
- recovery

A node is not:

- one agent
- one model session
- one prompt
- one fixed recipe forever

A node persists across agent runs, prompt changes, model changes, and future experiments.

## 2. What A Node Must Contain

Every valid node has these top-level subdirectories:

```text
<node>/
├── input/
├── output/
├── for-orchestrator/
├── system/
└── children/
```

These directories are part of the contract and are created together.

## 3. Canonical Files

### Task Source

Every node must have exactly one task source:

- `input/goal.md`
- `input/parent-instructions.md`

Meaning:

- `goal.md`
  Canonical task source for a root node.
- `parent-instructions.md`
  Canonical task source for a child node.

### Prepared Context And Knowledge

Optional or role-dependent context may exist in `input/`, including:

- `input/retrieved_relevant_knowledge_from_library.md`
- `input/context.md`
- `input/instructions-<role>.md`

The orchestrator is responsible for assembling critical context. The system should prefer prepared context over making models discover important files on their own.

### Canonical Output Artifacts

- `output/plan.md`
- `output/review.md`
- `output/final-output.md`
- `output/state.md`
- `output/escalation.md`

Meaning:

- `plan.md`
  Planning artifact.
- `review.md`
  Review artifact.
- `final-output.md`
  Main success artifact.
- `state.md`
  Node-local summary or continuation state. Useful but not authoritative.
- `escalation.md`
  Explicit statement that the node cannot safely continue under current assumptions.

Additional output files are allowed, but they are not part of the core contract unless explicitly added later.

### Orchestrator Control Files

- `for-orchestrator/agent-mode`
- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/next-action-after-child-report`
- `for-orchestrator/terminal-outcome`
- `for-orchestrator/failure-reason`
- `for-orchestrator/WAITING_FOR_COMPUTATION`
- `for-orchestrator/computation_result`

Meaning:

- `agent-mode`
  The current or next agent responsibility for the node.
- `this-nodes-current-status`
  The authoritative lifecycle status for the node.
- `next-action-after-child-report`
  Ephemeral parent-routing decision after receiving a child report.
- `terminal-outcome`
  The explicit terminal outcome when the node finishes successfully or is cancelled.
- `failure-reason`
  The explicit reason when the node fails.
- `WAITING_FOR_COMPUTATION`
  Marker that background computation is in progress.
- `computation_result`
  Marker that background computation finished and produced a result to inspect.

### Machine-Room Files

The `system/` directory is where run history and internal artifacts live. Common entries include:

- `system/runs/`
- `system/artifacts/`
- `system/jobs/`
- `system/agent-loop.jsonl`
- `system/tool-log.jsonl`
- `system/usage-summary.json`

The exact internal layout may evolve, but measurement and reconstruction must remain possible from disk.

## 4. Lifecycle Model

The node lifecycle should stay small and closed.

### Authoritative Status Values

- `pending`
- `active`
- `waiting_on_computation`
- `finished`
- `failed`

Meaning:

- `pending`
  Node exists and has a task source, but no active progress has started.
- `active`
  The node is currently advancing through one of its working stages.
- `waiting_on_computation`
  The node is blocked on an external or background computation result.
- `finished`
  The node reached an explicit terminal outcome.
- `failed`
  The node could not satisfy its contract safely or recoverably.

### Terminal Outcomes

When `this-nodes-current-status` is `finished`, `for-orchestrator/terminal-outcome` must exist and contain one of:

- `completed`
- `escalated`
- `cancelled`

Meaning:

- `completed`
  The node satisfied its terminal artifact contract.
- `escalated`
  The node explicitly handed the decision back upward.
- `cancelled`
  The node was invalidated by parent or orchestrator control.

### Failure Reason

When `this-nodes-current-status` is `failed`, `for-orchestrator/failure-reason` must exist.

Failure reasons are an open vocabulary. They should be specific enough to support debugging, analytics, and retry policy.

### Agent Mode

`for-orchestrator/agent-mode` carries the current or next role for the node, for example:

- `librarian`
- `planner`
- `plan-reviewer`
- `plan-decider`
- `worker`
- `mid-plan-evaluator`
- `synthesizer`

This role list is intentionally open. The lifecycle contract must not depend on freezing the current role set forever.

## 5. Legal Status Transitions

Legal transitions are:

- `pending -> active`
- `pending -> finished`
- `pending -> failed`
- `active -> waiting_on_computation`
- `active -> finished`
- `active -> failed`
- `waiting_on_computation -> active`
- `waiting_on_computation -> finished`
- `waiting_on_computation -> failed`

Additional rules:

- `pending -> finished` should normally mean immediate cancellation or deliberate short-circuiting by orchestrator policy.
- `waiting_on_computation -> finished` is only legal if the terminal artifact contract can be validated without another active agent run.
- `finished` is terminal.
- `failed` is terminal.

No other transitions are legal.

## 6. Node Invariants

The following should always hold for a valid node:

- the node has exactly one authoritative status
- the node has exactly one task source
- process exit never counts as success by itself
- correctness is determined by validated files plus status, not by model confidence
- stale control files must not silently drive fresh transitions
- important node state must be reconstructable from disk
- the node remains inspectable after success, escalation, cancellation, or failure
- no single agent run becomes the durable source of truth

Additional invariants:

- if status is `finished`, `terminal-outcome` exists
- if outcome is `completed`, `output/final-output.md` exists
- if outcome is `escalated`, `output/escalation.md` exists
- if status is `failed`, `failure-reason` exists
- at most one agent run is active per node at a time
- children are created by the orchestrator, not by agents

## 7. Agent Run Contract

An agent run is a temporary attempt to advance a node.

It is not the durable unit of truth. It is a contributor to node truth.

### Spawn Preconditions

Before spawning an agent run:

- the node must be in a status that allows work
- the node must have a task source on disk
- the orchestrator must have written or assembled required context
- no competing active run may still control the node

### Allowed Reads

An agent run may read:

- files inside its current node
- approved prompt files
- approved library files
- explicitly prepared parent or child context when needed

The preferred pattern is prepared context, not filesystem spelunking.

### Allowed Writes

An agent run may write only inside its own node directory, including:

- canonical artifacts in `input/` or `output/` when its role allows them
- machine-room artifacts in `system/`
- `for-orchestrator/next-action-after-child-report` when its role allows it
- computation marker files only through the background-job tool path

An agent run must never directly write:

- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/terminal-outcome`
- `for-orchestrator/failure-reason`
- sibling node truth files
- parent node truth files
- child node truth files

### Run Success Rule

An agent run is successful only if it leaves behind the required artifacts for its role.

Stopping, timing out, sounding finished, or returning a polite message is not enough.

## 8. Current V1 Role-To-Artifact Contract

This section is role-specific and may evolve later. It is the current v1 contract.

### `librarian`

Required success artifact:

- `input/retrieved_relevant_knowledge_from_library.md`

### `planner`

Required success artifact:

- `output/plan.md`

Allowed terminal alternative:

- `output/escalation.md`

### `plan-reviewer`

Required success artifact:

- `output/review.md`

### `plan-decider`

Required success artifact:

- revised or approved `output/plan.md`

Allowed terminal alternative:

- `output/escalation.md`

### `worker`

Required success artifact:

- `output/final-output.md`

Expected companion artifact:

- `output/state.md`

Allowed terminal alternative:

- `output/escalation.md`

### `mid-plan-evaluator`

Required success artifact:

- `for-orchestrator/next-action-after-child-report`

Allowed decision values:

- `continue`
- `replan`
- `escalate`

Expected companion artifact:

- `output/state.md`

### `synthesizer`

Required success artifact:

- `output/final-output.md`

Expected companion artifact:

- `output/state.md`

## 9. Hard In Code Versus Soft In Models

### Hard In Code

Code must own:

- lifecycle transitions
- artifact validation
- terminal outcome validation
- failure recording
- path and tool boundaries
- duplicate-run prevention
- retry and timeout policy
- stale-control-file cleanup
- background wait and resume semantics
- logging and measurement schemas

### Soft In Models

Models may vary on:

- wording
- explanation style
- plan shape
- review style
- synthesis style
- bounded task approach within allowed rules

These are quality variables, not correctness variables.

## 10. Observability And A/B Testability

The node is the primary measurement and experiment boundary.

Each node should make it possible to reconstruct:

- what task it had
- what status transitions occurred
- which runs happened
- what artifacts were written
- what tools were used
- what tokens and cost were consumed
- how it terminated

Each run under `system/runs/` should be independently inspectable and append-only. At minimum, a run record should capture:

- role
- model
- prompt or variant identifier
- start and finish time
- token usage
- cost
- exit reason
- artifacts produced

Future experiments should be able to vary:

- agent type
- prompt variant
- tool profile
- model assignment
- context assembly policy
- retry policy
- routing thresholds

without changing what a node fundamentally means.

## 11. What Is Intentionally Flexible

The following are intentionally left flexible:

- the role set
- prompt templates
- model assignments
- tool profiles
- retry heuristics
- routing heuristics
- experiment variants
- internal `system/` file layout beyond what is needed for reconstruction

These should be able to change without changing the node contract itself.

## 12. Node-Only Pressure Points

This is a node-first contract, but there are places where a later node-plus-workflow design could differ.

The main pressure points are:

- multiple sequential agent types inside one node
- parallel agent execution inside one node
- reusable repair loops
- reusable verification chains
- reusable approval or synthesis recipes

For now, those stay inside the node-first framing. If they become too implicit or too repetitive, that is the moment to consider adding a workflow layer above this contract rather than replacing the node as the foundation.

## 13. Immediate Use Of This Spec

This spec should now be used for:

- auditing the current Open-Eywa implementation
- identifying where the current system is still too soft
- designing offline simulation and regression tests around node behavior

That is the next step after this document.
