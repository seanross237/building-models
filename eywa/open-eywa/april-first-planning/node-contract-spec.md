# Node Contract Spec

## Purpose

This document defines the concrete node contract for Open-Eywa's node-first foundation.

It is meant to be stricter than the earlier philosophy docs. This is the first spec that should be usable for:

- code audit
- offline simulation design
- regression testing
- future refactors

The goal is to make the node the durable unit of truth, correctness, measurement, and inspection.

## Scope

This spec is intentionally node-first.

It does **not** try to introduce a general workflow layer yet. If later design choices differ between a pure node-first system and a node-plus-workflow system, we should flag those moments explicitly. For now, this spec stays node-focused and treats workflow concerns as future pressure points, not core primitives.

## Core Rule

Open-Eywa should be:

- stable at the node level
- flexible at the agent level
- hard at the protocol level

The main protocol rule is:

- models do judgment
- code does protocol

A model may lower quality, but it must not be able to break correctness.

## 1. What A Node Is

A node is a bounded unit of work with a durable on-disk contract.

A node is the smallest unit that should be:

- inspectable by a human
- validated by code
- measured across runs
- replayable after failure
- stable even as agents, prompts, and models change

A node is **not**:

- one agent
- one model session
- one prompt
- one fixed recipe forever

A node **is**:

- one persistent work container whose truth can be checked on disk

## 2. What A Node Owns

A node owns:

- its task or goal
- its current status
- its artifact contract
- its readable inputs
- its readable outputs
- its orchestrator control files
- its logs and usage records
- its child relationships
- its execution history on disk

The key rule is:

the node owns truth, not the agent.

Agents may help produce node truth, but the node is where truth lives, is checked, and is compared across runs.

## 3. Required Node Shape

A valid node directory should contain these subdirectories:

- `input/`
- `output/`
- `for-orchestrator/`
- `system/`
- `children/`

The node root itself should not be the primary place for truth files. Truth should live in the stable subdirectories above.

## 4. Canonical Files And Their Meaning

### Task Source Files

At least one of these must exist:

- `input/goal.md`
- `input/parent-instructions.md`

Meaning:

- `input/goal.md`
  The canonical root-level task statement for a mission root node.
- `input/parent-instructions.md`
  The canonical task statement handed to a child node or derived subnode.

Every node must have a clear task source on disk.

### Context And Knowledge Files

- `input/retrieved_relevant_knowledge_from_library.md`
  Retrieved or fallback knowledge relevant to the node.

This file may be brief, but if retrieval is part of the active protocol, the file must exist before retrieval is considered complete.

### Main Output Files

- `output/plan.md`
  The plan artifact for a planning pass.
- `output/review.md`
  The review artifact for a plan-review pass.
- `output/final-output.md`
  The main success artifact for a completed execution or synthesis.
- `output/state.md`
  A serializable summary of current node-local state.
- `output/escalation.md`
  An explicit declaration that the node cannot safely continue under current assumptions.

### Orchestrator Control Files

- `for-orchestrator/agent-mode`
  The current or next role/mode expected for this node.
- `for-orchestrator/this-nodes-current-status`
  The current node status.
- `for-orchestrator/eval-decision`
  A machine-consumable control decision for evaluation/synthesis stages.
- `for-orchestrator/WAITING_FOR_COMPUTATION`
  Marker that the node is waiting on a background computation.
- `for-orchestrator/computation_result`
  Marker that the background computation produced a result.

### Machine-Room Files

Common examples under `system/`:

- `active-run.json`
- `agent-loop.jsonl`
- `usage-summary.json`
- `tool-log.jsonl`
- `jobs/`
- `artifacts/`

These files are important for debugging and measurement, but the main truth contract should remain centered on `input/`, `output/`, and `for-orchestrator/`.

## 5. Node Invariants

These invariants should always hold:

- a node has exactly one authoritative current status
- a node has a clear task source on disk
- a node remains inspectable after success, failure, or escalation
- process exit never counts as success by itself
- correctness is determined by files plus status, not by model confidence
- no agent run is allowed to become the durable source of truth
- important node state must be reconstructable from disk
- protocol files must have stable meaning across runs

## 6. Canonical Node Statuses

The current canonical status vocabulary for Open-Eywa v1 is:

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
  Node exists and has a task source, but no active run has started.
- `retrieving`
  Retrieval is the active responsibility for the node.
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
  A plan is approved and the node is ready to create or resume child execution.
- `executing`
  Child work is the active mechanism of progress for this node.
- `evaluating`
  The node is deciding what to do after child progress or completion.
- `waiting_comp`
  The node is waiting for a background computation result.
- `complete`
  The node has satisfied its completion contract.
- `escalated`
  The node has explicitly escalated and requires higher-level handling.
- `cancelled`
  The node was invalidated by parent-level replanning or cancellation.
- `failed`
  The node could not satisfy its contract safely or recoverably.

## 7. Legal Status Transitions

### Standard Transitions

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

### Forced Cancellation Rule

Any nonterminal descendant node may be forced to:

- `* -> cancelled`

when a parent invalidates that node through replanning or cancellation.

### Status Contract Rule

A transition is legal only if:

- the source status matches
- the destination status is allowed from that source
- the file-level preconditions for the destination status are satisfied

## 8. File-Level Preconditions For Important States

### Entering `running`

Requires:

- a task source file exists
- if retrieval is part of the active protocol, `input/retrieved_relevant_knowledge_from_library.md` exists

### Entering `needs_review`

Requires:

- `output/plan.md` exists
- the plan requires review under current routing rules

### Entering `approved`

Requires:

- an approved plan exists, or the current planning policy allows direct approval

### Entering `executing`

Requires:

- the node has an approved plan or equivalent execution basis

### Entering `complete`

Requires:

- the node has satisfied its terminal artifact contract
- no stale control file is incorrectly driving completion

Completion must never be inferred from process exit alone.

### Entering `escalated`

Requires:

- `output/escalation.md` exists or an equivalent explicit escalation artifact exists

## 9. Agent Run Contract

An agent run is a temporary attempt to advance a node.

### Preconditions

Before spawning an agent run:

- the node must be in a status that expects that run
- the task source must exist
- the orchestrator must have written any required instruction/context files
- no competing active run may still control the node

### Allowed Reads

An agent run may read:

- its current node files
- approved library and prompt files
- approved mission-level context files
- explicitly permitted child or parent artifacts when the role requires them

The system should increasingly prefer prepared context over requiring the model to discover critical files on its own.

### Allowed Writes

An agent run may write:

- canonical node artifacts inside the current node
- machine-room artifacts inside the current node `system/`

An agent run must not directly mutate:

- sibling node truth files
- parent node truth files
- child node truth files

Exception:

- runtime and orchestrator code may append mission-level logs as part of the platform, but models themselves should not be treated as writers of shared global truth.

### Agent Run Success Rule

An agent run is successful only if it leaves behind the required artifacts for its role or phase.

Stopping, timing out, or sounding finished is not enough.

## 10. Current V1 Role-To-Artifact Contract

This section is role-specific and may evolve later, but it is the current v1 contract.

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

## 11. Completion, Failure, Escalation, And Cancellation

### Completion

A node is `complete` only when:

- its terminal artifact contract is satisfied
- the required files exist
- the orchestrator can validate them

Completion is a file-and-state fact, not a model feeling.

### Failure

A node is `failed` when:

- it could not satisfy the contract safely
- recovery or retry rules were exhausted
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

## 12. Hard Guarantees Versus Soft Variation

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

## 13. Observability Contract

Every node should remain measurable and inspectable.

At minimum, the system should make it possible to reconstruct:

- what task the node had
- what status transitions happened
- which agent runs occurred
- what files were written
- what tools were used
- what tokens and cost were consumed
- how the node terminated

This is necessary for reliability work and for future A/B testing.

## 14. A/B Testability Contract

The node should be the primary experiment boundary.

That means future experiments should be able to vary:

- agent type
- prompt variant
- tool profile
- context assembly policy
- retry policy
- recovery behavior
- routing thresholds

while keeping the meaning of the node fixed.

If experiment variants change the meaning of a node, comparison quality breaks.

## 15. Current Workflow Pressure Points

This spec is intentionally node-first, but there are places where a node-plus-workflow design could eventually diverge.

The main pressure points are:

- multiple sequential agent types inside one node
- parallel agent execution inside one node
- reusable repair loops
- reusable verification chains
- reusable approval/synthesis recipes

For now, we should keep these inside the node-first framing.

If later these patterns become too implicit, that is the moment to explicitly revisit whether a workflow layer is warranted.

## 16. Immediate Use Of This Spec

This spec should now be used for:

- auditing the current Open-Eywa implementation
- identifying where the current system is still too soft
- designing offline simulation and regression tests around node behavior

That is the next step after this document.
