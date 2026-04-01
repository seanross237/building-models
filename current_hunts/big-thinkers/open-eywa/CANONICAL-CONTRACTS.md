# Open-Eywa Canonical Contracts

## Purpose

This document defines the first-pass hard contracts for Open-Eywa.

These contracts are the rules the system should enforce directly in code and cover explicitly in tests.

## 1. Role Contracts

### `librarian`

Required success artifact:

- `input/retrieved_relevant_knowledge_from_library.md`

Allowed terminal alternatives:

- none in normal operation

Contract:

- a node is not done retrieving until the retrieval file exists
- if nothing useful is found, the file should still be written with a plain note

### `planner`

Required success artifact:

- `output/plan.md`

Allowed terminal alternatives:

- `output/escalation.md`

Contract:

- planner success requires a valid plan artifact
- planner escalation is explicit and file-based

### `worker`

Required success artifact:

- `output/final-output.md`

Allowed terminal alternatives:

- `output/escalation.md`

Expected companion artifact:

- `output/state.md`

Contract:

- worker success requires final output
- worker failure to produce output must not silently count as completion

### `plan-reviewer`

Required success artifact:

- `output/review.md`

Contract:

- reviewer success requires review output

### `plan-decider`

Required success artifact:

- approved `output/plan.md`

Allowed terminal alternatives:

- `output/escalation.md`

Expected companion artifact:

- `output/state.md`

Contract:

- decider must either approve a plan in a machine-checkable way or escalate explicitly

### `mid-plan-evaluator`

Required success artifact:

- `for-orchestrator/eval-decision`

Allowed decision values:

- `continue`
- `replan`
- `escalate`

Expected companion artifact:

- `output/state.md`

Contract:

- evaluator success requires a valid decision value
- free-form prose is not enough unless code extracts a valid decision deterministically

### `synthesizer`

Required success artifacts:

- `output/final-output.md`
- `for-orchestrator/eval-decision`

Required decision value:

- `synthesize`

Expected companion artifact:

- `output/state.md`

Contract:

- synthesizer success requires a real final output plus the `synthesize` decision
- the node must not become complete merely because the process exited

## 2. Status Contracts

Legal statuses:

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

Contract:

- nodes may only move through legal transitions
- terminal states are authoritative
- a node must never become `complete` without the required artifacts for that role or phase

## 3. File Contracts

### Human-facing directories

- `input/`
- `output/`
- `for-orchestrator/`

### Machine-room directory

- `system/`

Contract:

- protocol files live in stable, well-known locations
- machine-room details should not leak into the human-facing contract unless intentional

### Important protocol files

- `input/goal.md`
- `input/parent-instructions.md`
- `input/retrieved_relevant_knowledge_from_library.md`
- `output/plan.md`
- `output/review.md`
- `output/final-output.md`
- `output/state.md`
- `output/escalation.md`
- `for-orchestrator/agent-mode`
- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/eval-decision`
- `for-orchestrator/WAITING_FOR_COMPUTATION`
- `for-orchestrator/computation_result`

Contract:

- these files should have stable meaning across the system
- stale protocol files must not silently drive fresh transitions

## 4. Tool Contracts

Contract:

- tools must return structured results
- tools must stay within approved read and write boundaries
- write operations must be bounded to the current node unless explicitly allowed
- shell execution must be logged and time-bounded
- background jobs must produce metadata under `system/jobs/`

The system should increasingly prefer typed tools over open-ended filesystem discovery for routine protocol actions.

## 5. Orchestration Contracts

Contract:

- only one active run should control a node at a time
- duplicate spawns for the same transition should not happen
- child creation should be idempotent
- evaluator decisions should be consumed and cleared safely
- stale decision files should not control fresh evaluations
- root mission completion should be based on validated artifacts, not process exit alone

## 6. Logging Contracts

Mission-level logs:

- `orchestrator.jsonl`
- `usage.jsonl`
- `tools.jsonl`

Per-node logs under `system/`:

- `agent-loop.jsonl`
- `usage-summary.json`
- `tool-log.jsonl`
- `jobs/`
- `artifacts/`

Contract:

- important state changes should be reconstructable from logs
- usage and cost should be attributable by node and role
- tool behavior should be inspectable after a run

## 7. Completion And Failure Contracts

Contract:

- process exit does not equal success
- role success is defined by artifacts, not by model stop reason
- failure should be explicit and inspectable
- escalation should be explicit and inspectable
- partial output should never silently count as full success

## 8. Testing Contracts

Contract:

- every hard contract should be tested offline
- every discovered real failure mode should become a regression test
- live model runs should validate integration, not basic orchestration correctness

## 9. Immediate Hardening Direction

These contracts suggest the next moves clearly:

- reduce free-form protocol behavior
- move more context assembly into code
- replace routine file discovery with typed tools or prepared context packets
- validate all role outputs strictly
- expand offline scenario coverage around known failure modes
