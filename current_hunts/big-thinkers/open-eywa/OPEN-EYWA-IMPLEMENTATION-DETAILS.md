# Open-Eywa Implementation Details

This document describes the **current actual implementation** of the rebuilt `Open-Eywa` system.

Use this doc when you want to understand how the offline engine works today, how the major modules connect, and what parts are already real versus still planned.

This is different from:

- `OPEN-EYWA-GOAL-AND-OVERVIEW.md`
  - north star and high-level direction
- `BUILDING-PRINCIPLES.md`
  - architectural values, trust boundary, and change discipline
- `april-first-planning/canonical-node-contract-spec.md`
  - hard node contract

## Current State

The current live rebuild is an **offline-first, simulation-backed implementation**.

That means:

- the orchestrator is real
- the node contract is real
- lifecycle and recovery controls are real
- event and summary recording are real
- the first safe file-tool layer is real
- the runtime seam is real
- the runtime used for confidence-building is currently the simulated runtime
- the fast adversarial sturdiness layer is real
- a tiny real OpenRouter runtime path is now real
- `stuff-for-agents/` is now materially used by the runtime prompt loader
- the live canary path has now completed both a single-node real run and a multi-step real tree run

The real OpenRouter runtime is still **minimal and not yet the main active path**, but the live seam is now proven enough to support careful canaries.

## Top-Level Shape

Important top-level areas:

```text
open-eywa/
├── OPEN-EYWA-GOAL-AND-OVERVIEW.md
├── BUILDING-PRINCIPLES.md
├── OPEN-EYWA-IMPLEMENTATION-DETAILS.md
├── AGENTS.md
├── CLAUDE.md
├── stuff-for-agents/
├── validation-suite/
└── system/
```

Main implementation code:

- `system/orchestrator/`
- `system/runtime/`
- `system/tools/`
- `stuff-for-agents/`
- `system/scripts/`

Main validation code:

- `validation-suite/contract-tests/`
- `validation-suite/adversarial-tests/`
- `validation-suite/scenario-tests/`

## Core Node Contract

The node is the durable unit of work and truth.

Current canonical node directories:

- `input/`
- `output/`
- `system/`
- `children/`

Current authoritative node record:

- `system/node.json`

Important implementation file:

- `system/orchestrator/node_contract.py`

That module provides:

- current status and terminal-outcome enums
- the `NodeLayout` path model
- node creation helpers
- path helpers for runs, summaries, node snapshots, and recovery folders

### Current statuses

- `pending`
- `active`
- `waiting_on_computation`
- `finished`
- `failed`

### Current terminal outcomes

- `completed`
- `escalated`
- `cancelled`

## Orchestrator Modules

### `node_contract.py`

Defines the durable node layout and path model.

### `node_record.py`

Defines the authoritative `system/node.json` schema helpers and read/write access layer.

The lifecycle block now carries a visible `retry_count` field so repeated attempts are inspectable in the live node state.

### `node_lifecycle.py`

Defines legal status transitions and enforces transition rules.

This is where the system ensures things like:

- completed nodes must have `output/final-output.md`
- escalated nodes must have `output/escalation.md`
- cancelled nodes must have a cancellation reason in `system/node.json`

### `node_validator.py`

Checks whether a node is valid against the current contract.

This is used both in tests and during orchestration safety checks.

### `event_schema.py`

Defines the raw append-only event vocabulary and event payload requirements.

Events are raw facts, not summaries.

### `event_writer.py`

Small append-only JSONL writer for events and records.

### `usage_schema.py`

Defines raw usage and cost record shapes.

### `summary_schema.py`

Defines derived summary shapes for:

- runs
- nodes
- missions

### `role_contracts.py`

Defines the current role-to-artifact expectations.

This is where the system knows, for example:

- `planner` must produce `output/plan.md`
- `worker` must produce `output/final-output.md`
- `mid-plan-evaluator` must set `control.next_action_after_child_report` in `system/node.json`

### `orchestrator_core.py`

Runs one role on one node through the runtime seam.

It is responsible for:

- validating the node before a run
- moving `pending -> active` when needed
- creating a run directory
- snapshotting `system/node.json` into the run directory
- preparing a runtime request
- calling the runtime
- persisting request/result/summary/usage files
- updating node usage and cost summaries
- applying runtime control/lifecycle updates back into `system/node.json`
- enforcing post-run contract outcomes

### `orchestrator_progression.py`

This is the multi-run node progression layer.

It currently handles:

- planner-first behavior for unplanned nodes
- plan parsing, including the strict `### Step ... / Goal:` planner format
- child node creation
- driving child nodes to stable states
- evaluator handoff after child results
- consuming `control.next_action_after_child_report` from `system/node.json`
- continue / replan / escalate behavior
- waiting-on-child behavior
- synthesizer triggering
- bounded automatic retries for contract-output failures (`missing_required_artifact` and `invalid_decision_value`)

Current automatic retry policy:

- retry happens in the progression layer, not inside the runtime client
- retry is limited to 3 automatic retries per node
- retries increment `lifecycle.retry_count` in `system/node.json`
- retries create `node_recovery_prepared` events and `system/recoveries/recovery-XXX/` snapshots
- when the retry limit is reached, the node stays failed

This is currently the main orchestration pressure point and should be watched carefully for creeping complexity.

### `mission_contract.py`

Defines the mission-level folder shape.

### `mission_driver.py`

Drives a whole mission tree from the mission root and produces mission-level events and summaries.

### `live_canary.py`

Small helper layer for tiny live canary missions.

It currently handles:

- default canary goal text
- default mission path creation under `missions/live-canaries/`
- mission bootstrap for a tiny canary
- root role selection for the canary

### `node_controls.py`

Small lifecycle-control layer for:

- recording computation results
- resuming waiting nodes when results exist
- cancelling nodes safely

### `node_recovery.py`

Small recovery layer for preparing a node for a fresh attempt.

It currently archives prior attempt state into:

- `system/recoveries/recovery-XXX/`

and resets the live node back to a clean `pending` state.

There are now two recovery shapes:

- fresh-attempt recovery
  - archives output, children, and the old node record, then resets progression state
- narrow retry recovery
  - snapshots the current output and node record, increments `retry_count`, and resets the lifecycle back to `pending` without wiping children or progression state

### `node_preparation.py`

Builds the prepared context packet for a run.

This is how the orchestrator currently gives the runtime a structured summary of:

- task source
- node state
- relevant artifacts
- progression state
- latest child report
- child summaries

The goal is to reduce filesystem spelunking and make runtime behavior easier to compare and test.

In the current planner/progression contract:

- child directory names come from step titles
- child `input/parent-instructions.md` comes from the step `Goal:` field when present
- child `input/context.md` is assembled from parent task, plan, state, and prior child results
- numbered and bulleted fallback plans are still supported for older simulated fixtures

## Runtime Modules

### `runtime_interface.py`

Defines the stable runtime seam.

Main types:

- `RuntimeRequest`
- `RuntimeResult`
- `RuntimeAdapter`

This seam is the boundary between orchestration and runtime implementation.

### `simulation_scenarios.py`

Defines the shape of scenario fixtures used by the simulated runtime.

### `simulated_runtime.py`

Implements the current offline runtime.

It:

- reads a scripted scenario fixture
- applies scenario actions to the current node
- can call the real file-tool layer
- emits tool events when tools are used
- returns a structured `RuntimeResult`

This is how the system is currently exercised end-to-end without live API calls.

### `prompt_loader.py`

Loads real prompt bundles from:

- `stuff-for-agents/`

This is the bridge between the human-facing prompt/library tree and the runtime seam.

Prompt loading is now also guarded by contract tests so prompt bundles do not silently drift back to legacy control-file names.

### `openrouter_client.py`

Small OpenRouter chat-completions client.

It currently handles:

- non-streaming chat completions
- auth headers
- optional generation stats lookup for cost

### `openrouter_runtime.py`

Implements the tiny real runtime path.

It currently:

- loads role prompts from `stuff-for-agents/`
- loads prepared context packets from the orchestrator
- sends non-streaming chat-completions requests to OpenRouter
- exposes the current safe file tools as tool calls
- loops through assistant tool calls until a terminal assistant response
- records usage and optional generation-derived cost

This path is meant to be small and testable first, not broad yet.

### `runtime_factory.py`

Small runtime-factory layer for the live canary path.

It currently provides:

- the default cheap model choice for canaries
- a default role-to-model map
- a thin constructor for the OpenRouter runtime using environment configuration, with repo-root `.env` fallback for `OPENROUTER_API_KEY`

## Tool Layer

### `system/tools/file_tools.py`

This is the first real tool layer.

Currently implemented tools:

- `read_file`
- `write_file`
- `edit_file`
- `glob`
- `grep`

Important properties:

- node-bounded
- deterministic
- safe to run offline
- usable through the runtime seam

Broader tools like shell/math/background jobs are still future work in the rebuild.

The tiny real OpenRouter runtime currently exposes only these file tools, even if some role prompts describe richer future toolsets.

## End-To-End Offline Flow

The current offline system works roughly like this:

1. create a mission and root node
2. mission driver calls node progression
3. node progression decides which role should run next
4. orchestrator core prepares a run directory and prepared context packet
5. orchestrator core sends a `RuntimeRequest` to the runtime seam
6. either:
   - simulated runtime executes a scripted scenario
   - or tiny real OpenRouter runtime loads prompts, uses file tools, and returns a result
7. the runtime may directly write files and/or call real file tools
8. orchestrator core validates the result against the role contract
9. progression decides what happens next
10. mission driver aggregates the final mission summary

## Tiny Live Canary Path

There is now a first tiny live canary entry point:

- `system/scripts/run_live_canary.py`

It:

- creates a mission under `missions/live-canaries/` by default
- uses the tiny OpenRouter runtime path
- defaults the root role to `worker` for minimal cost and complexity
- prints a compact JSON result summary at the end

This path has now been proven with:

- a real single-node `worker` canary
- a real multi-step tree canary using `planner`, `worker`, `mid-plan-evaluator`, and `synthesizer`

The default live canary model is currently:

- `openai/gpt-4.1-mini`

The real live run currently accepts `OPENROUTER_API_KEY` from either:

- the process environment
- the repo-root `.env` file

## Run Artifacts

For each run, the system currently writes under:

- `system/runs/run-XXX/`

Current per-run files include:

- `request.json`
- `prepared-node-context.json`
- `result.json`
- `summary.json`
- `usage.json`

## Event And Summary Model

The current design rule is:

- events are raw facts
- summaries are derived views

Node-level raw events live under:

- `system/events.jsonl`

Mission-level raw events live under:

- `system/mission-events.jsonl`

Derived mission summary currently lives at:

- `system/mission-summary.json`

## Validation Suite

The validation suite is already connected to the real rebuild architecture.

### Contract tests

Live under:

- `validation-suite/contract-tests/`

They verify:

- node validity rules
- lifecycle rules
- event/schema behavior
- file-tool behavior
- node preparation behavior

### Scenario tests

Live under:

- `validation-suite/scenario-tests/`

They verify:

- simulated runtime behavior
- single-run orchestrator behavior
- multi-run progression behavior
- mission-driver behavior
- waiting/resume behavior
- recovery/retry behavior
- tool-through-runtime behavior

### How tests connect to the implementation

The important point is:

- tests are not off to the side
- they drive the real orchestrator and runtime seam
- only the model/runtime behavior is simulated

So the current offline system is genuinely runnable end-to-end.

### Adversarial tests

Live under:

- `validation-suite/adversarial-tests/`

They are the compact fast weird-case layer.

They verify that the system fails explicitly and safely under high-value ugly cases like:

- malformed control values
- runtime failures
- tool boundary violations
- malformed plans
- explicit mission-drive failures

There is also a fast runner:

- `python3 system/scripts/run_fast_sturdiness_suite.py`

## What Is Already Real

Already real in the rebuild:

- node creation
- node validation
- lifecycle transitions
- run recording
- event recording
- usage/cost recording
- mission driving
- parent/child progression
- waiting / resume
- cancellation
- fresh-attempt recovery
- prepared context packets
- safe file tools
- offline runtime execution through the real seam
- prompt loading from `stuff-for-agents/`
- tiny real OpenRouter runtime execution through the real seam
- tiny live canary mission bootstrapping and runner path
- completed real single-node canary execution
- completed real multi-step tree canary execution

## What Is Not Yet The Main Live Path

Not yet fully built as the main live path:

- full tool-calling agent loop
- broader shell/math/background job tooling in the rebuild
- live canary workflow
- richer experiment management above the current `model` / `variant` fields

The real OpenRouter path now exists, but it is still intentionally narrow and not yet the default confidence path.

## Current Architectural Pressure Points

The places most likely to become complexity sinks if not watched:

- `system/orchestrator/orchestrator_progression.py`
- `system/orchestrator/event_schema.py`
- `system/orchestrator/node_preparation.py`
- `system/orchestrator/mission_driver.py`

Future changes should prefer small extra modules over making those files absorb everything.

## If You Change This System

Also update:

- `OPEN-EYWA-GOAL-AND-OVERVIEW.md` when the high-level story changes
- `BUILDING-PRINCIPLES.md` when the architectural philosophy or builder rules change
- this file when the actual implementation shape changes
