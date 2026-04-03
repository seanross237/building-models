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
- Claude CLI and Codex CLI runtime adapters are now real
- a provider-selectable runtime factory is now real
- `stuff-for-agents/` is now materially used by the runtime prompt loader
- the live canary path has now completed both a single-node real run and a multi-step real tree run

The live runtime supports three providers (`openrouter`, `claude`, `codex`) through the same seam. The orchestrator does not know or care which backend executed the work.

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
- `for-orchestrator/`
- `system/`
- `children/`

Important implementation file:

- `system/orchestrator/node_contract.py`

That module provides:

- current status and terminal-outcome enums
- the `NodeLayout` path model
- node creation helpers
- path helpers for runs, control files, summaries, and recovery folders

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

### `node_lifecycle.py`

Defines legal status transitions and enforces transition rules.

This is where the system ensures things like:

- completed nodes must have `output/final-output.md`
- escalated nodes must have `output/escalation.md`
- cancelled nodes must have `for-orchestrator/cancellation-reason`

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
- `mid-plan-evaluator` must produce `for-orchestrator/next-action-after-child-report`

### `orchestrator_core.py`

Runs one role on one node through the runtime seam.

It is responsible for:

- validating the node before a run
- moving `pending -> active` when needed
- creating a run directory
- preparing a runtime request
- calling the runtime
- persisting request/result/summary/usage files
- updating node usage and cost summaries
- enforcing post-run contract outcomes

### `orchestrator_progression.py`

This is the multi-run node progression layer.

It currently handles:

- planner-first behavior for unplanned nodes
- plan parsing, including the strict `### Step ... / Goal:` planner format
- child node creation
- driving child nodes to stable states
- evaluator handoff after child results
- consuming `next-action-after-child-report`
- continue / replan / escalate behavior
- waiting-on-child behavior
- synthesizer triggering

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

### `runtime_task_builder.py`

Builds a provider-neutral runtime task file from a prompt bundle and prepared context packets.

The task file is a markdown document written to the node directory that any CLI runtime can consume. It packages:

- role and run metadata
- system prompt and support documents
- prepared context packets
- role contract required artifact paths
- runtime note and instructions

### `cli_runtime_base.py`

Shared base class for CLI-backed runtime adapters (Claude CLI, Codex CLI).

It handles:

- prompt loading and task file assembly
- subprocess execution with timeout
- stdout/stderr capture to disk
- artifact scanning from `output/`
- `RuntimeResult` construction with honest subscription-mode usage accounting

### `claude_cli_runtime.py`

Claude CLI runtime adapter. Runs nodes via `claude -p` in non-interactive mode with:

- `--permission-mode bypassPermissions` for unattended execution
- `--allowedTools Read,Write,Edit,Glob,Grep` to match the OpenRouter tool boundary
- OAuth/keychain auth preserved so subscription credits work

### `codex_cli_runtime.py`

Codex CLI runtime adapter. Runs nodes via `codex exec` in non-interactive mode with:

- `--sandbox workspace-write` for controlled file access

### `runtime_factory.py`

Provider-selectable runtime factory for the live canary path.

It currently provides:

- `RuntimeProvider` type: `"openrouter" | "claude" | "codex"`
- `LiveRuntimeSettings` dataclass with provider-neutral settings
- `build_live_runtime()` builder that selects the correct backend
- the default model choice for canaries
- a default role-to-model map
- a legacy `build_openrouter_runtime_for_live_canary()` for backwards compatibility

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

There is now a tiny live canary entry point:

- `system/scripts/run_live_canary.py`

It:

- creates a mission under `missions/live-canaries/` by default
- selects a runtime provider via `--runtime-provider openrouter|claude|codex`
- defaults the root role to `worker` for minimal cost and complexity
- prints a compact JSON result summary at the end

The runtime provider controls which backend executes node roles:

- `openrouter` — API-backed via OpenRouter chat completions (requires `OPENROUTER_API_KEY`)
- `claude` — local Claude CLI via `claude -p` (uses monthly subscription credits)
- `codex` — local Codex CLI via `codex exec` (uses monthly subscription credits)

The same orchestrator, node contract, role contracts, and mission artifacts are used regardless of provider. Success is always determined by artifact validation after the run, not by provider-specific behavior.

CLI providers record honest usage metadata with `usage_unavailable: true` and `total_cost_usd: 0.0` since token counts and costs are not available from subscription-based CLI runs.

This path has been proven with:

- a real single-node `worker` canary
- a real multi-step tree canary using `planner`, `worker`, `mid-plan-evaluator`, and `synthesizer`

The default live canary model is currently:

- `openai/gpt-4.1-mini`

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
- Claude CLI runtime adapter via `claude -p`
- Codex CLI runtime adapter via `codex exec`
- provider-neutral runtime task builder
- provider-selectable runtime factory
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
