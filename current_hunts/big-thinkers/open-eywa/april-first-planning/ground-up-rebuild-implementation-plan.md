# Ground-Up Rebuild Implementation Plan

## Purpose

This document describes what will be built in the ground-up rebuild of Open-Eywa.

It is a build plan, not an implementation. The goal is to make the next construction phase deliberate, contract-first, and test-led rather than improvised.

This rebuild should optimize for:

- a hard node-first core
- strong offline reliability before live model runs
- easy future extension
- easy A/B testing
- minimum downstream churn when the system evolves

## Build Principles

The rebuild should follow these rules:

- build from the canonical node contract outward
- make correctness a code responsibility, not a model responsibility
- prefer small closed protocols and open extension points
- make the node the primary truth boundary
- make the node the primary measurement boundary
- design offline simulation before live inference
- preserve inspectability for both humans and future agents

## What Will Be Built

The rebuild will produce:

- a minimal contract-first node model
- a node validator that can prove whether a node is valid against the contract
- a small lifecycle engine for legal node transitions
- a clean event and metrics schema
- a simulated runtime interface for offline orchestration testing
- a contract test suite
- a scenario test suite
- a rebuilt orchestrator that operates against the contract
- a rebuilt tool layer with strict boundaries
- a rebuilt runtime layer for real agent runs
- a small live canary layer for later integration checks

It will not begin by rebuilding the whole previous prototype.

The first target is a trustworthy engine, not a feature-complete engine.

## Build Order

The rebuild should proceed in this order:

1. lock the contract-adjacent core
2. define the observability contract
3. define the simulation seam
4. build contract tests
5. build scenario tests
6. rebuild the orchestrator core
7. rebuild the tool layer
8. rebuild the runtime layer
9. add tiny live canaries
10. only then add richer mission behavior and polish

## Phase 0: Lock The Foundation Inputs

### Goal

Make sure the rebuild starts from stable source documents instead of shifting ideas.

### Inputs To Treat As Source Of Truth

- `april-first-planning/canonical-node-contract-spec.md`
- `BUILDING-PRINCIPLES.md`
- `OPEN-EYWA-GOAL-AND-OVERVIEW.md`

### Deliverables

- this plan
- one agreed canonical node contract
- one agreed immediate rebuild direction

### Done Means

- we are no longer debating the basic node-first direction
- future implementation work can point to a single contract doc

## Phase 1: Build The Contract Kernel

### Goal

Create the smallest code layer that understands what a node is before any real orchestration exists.

### What Will Be Built

- node path helpers
- node creation helpers
- node validation helpers
- canonical file presence checks
- canonical status parsing and validation
- terminal outcome validation
- failure reason validation
- invariant checks

### Key Behaviors

- create a new valid empty node on disk
- validate an existing node and explain what is invalid
- distinguish contract violations from normal nonterminal state

### Why This Comes First

Everything else depends on a trustworthy definition of:

- what a node contains
- what a valid node looks like
- what files and states mean

### Done Means

- we can create a valid node from code
- we can validate a node from code
- we can explain node invalidity in a structured way

## Phase 2: Define The Event And Metrics Contract

### Goal

Define the logging and measurement layer before building the engine that writes it.

### What Will Be Built

- event types for node lifecycle changes
- event types for run lifecycle changes
- event types for tool calls
- usage record schema
- cost record schema
- run summary schema
- mission summary schema

### Minimum Questions The Schema Must Answer

- what happened
- when did it happen
- on which node did it happen
- which role or run did it involve
- what changed
- what did it cost
- why did the node terminate the way it did

### Design Rule

The schema should be stable enough that:

- tests can assert against it
- visualizations can depend on it
- A/B analysis can depend on it

### Done Means

- the project has a canonical event vocabulary
- the project has a canonical usage and cost vocabulary
- future code can emit structured logs instead of ad hoc text

## Phase 3: Define The Simulation Seam

### Goal

Make it possible to test orchestration correctness without calling real models.

### What Will Be Built

- a runtime interface that the orchestrator talks to
- a simulated runtime implementation of that interface
- scenario fixture format for scripted agent behaviors
- deterministic run outputs for offline tests

### Simulated Behaviors To Support

- successful artifact creation
- missing required artifact
- malformed artifact
- wrong control file
- repeated no-op behavior
- loop behavior
- timeout behavior
- crash behavior
- escalation behavior
- stale-file behavior
- background computation start and completion

### Design Rule

The orchestrator should not care whether it is talking to:

- a simulated runtime
- a live runtime

That seam is essential.

### Done Means

- offline tests can drive the real orchestrator through fake agent behavior
- no OpenRouter calls are needed to test correctness

## Phase 4: Build The Contract Test Suite

### Goal

Prove the contract kernel is correct in small deterministic tests.

### What Will Be Built

- tests for valid node shape
- tests for invalid node shape
- tests for task source rules
- tests for status validation
- tests for terminal outcome validation
- tests for failure reason validation
- tests for invariant enforcement
- tests for stale control file handling
- tests for agent write boundary enforcement

### Design Rule

These tests should be:

- fast
- deterministic
- easy to extend

### Done Means

- small contract violations are caught immediately
- the rebuild has a reliable fast-test base

## Phase 5: Build The Scenario Test Suite

### Goal

Prove the orchestrator and runtime contract behave correctly across realistic multi-step flows.

### What Will Be Built

- success scenarios
- escalation scenarios
- failure scenarios
- waiting computation scenarios
- replanning scenarios
- cancellation scenarios
- bad-model-behavior scenarios

### Example Scenario Families

- planner writes `plan.md` and exits cleanly
- planner exits cleanly without `plan.md`
- worker loops and never produces `final-output.md`
- evaluator writes an invalid `next-action-after-child-report`
- synthesizer writes `final-output.md` but misses required artifacts
- stale `next-action-after-child-report` exists before a new run
- background job starts, node waits, result arrives, node resumes

### Done Means

- the system can be stress-tested offline
- every real bug found later can become a permanent regression scenario

## Phase 6: Rebuild The Orchestrator Core

### Goal

Build the smallest orchestrator that can drive nodes through legal contract-compliant progress.

### What Will Be Built

- node lifecycle transition engine
- precondition checks for each transition
- spawn/resume decision logic
- control-file consumption logic
- stale-control-file cleanup logic
- child-node creation logic
- background wait/resume handling
- mission-level event writing

### Design Rule

The orchestrator should only make decisions from durable on-disk truth plus validated control files.

It should not depend on:

- process optimism
- agent self-reporting
- implicit stale state

### Done Means

- the orchestrator can advance a mission correctly under simulated runtime conditions
- illegal transitions are rejected
- terminal states are only written when validated

## Phase 7: Rebuild The Tool Layer

### Goal

Build a strict capability layer that enforces machine-side safety and node boundaries.

### What Will Be Built

- file read and write tools with scoped boundaries
- editing helpers for node-local artifacts
- safe shell execution boundaries
- background job lifecycle tools
- math execution tools for Python, Sage, and Lean
- tool logging hooks

### Design Rule

Tools should enforce:

- node-local write boundaries
- orchestrator-owned file protection
- bounded execution
- reproducible artifacts

### Done Means

- tools are no longer soft assumptions
- the machine layer can enforce the rules even if the model is messy

## Phase 8: Rebuild The Runtime Layer

### Goal

Reintroduce real agent execution only after the contract and test foundation is strong.

### What Will Be Built

- runtime context assembly
- role-to-artifact success enforcement
- tool loop integration
- usage and cost aggregation
- run-record creation
- failure classification for runtime exits

### Design Rule

The runtime should be replaceable.

The node contract should stay stable whether the runtime is:

- simulated
- OpenRouter-backed
- replaced later

### Done Means

- a real agent run can happen without weakening the contract rules
- process exit alone never drives node success
- run history remains inspectable

## Phase 9: Add Tiny Live Canaries

### Goal

Reintroduce real model calls as a thin integration check, not as the main way to discover system flaws.

### What Will Be Built

- one or two tiny mission canaries
- one or two tiny role-level canaries
- cost-capped live test commands
- high-level run summaries

### Design Rule

Live tests should answer:

- does the runtime-model seam still work
- do logs and cost accounting still work

They should not be the main source of truth for correctness.

### Done Means

- real calls can be exercised cheaply
- failures found live are rare and high-signal

## Phase 10: Add Richer Features Only After The Core Is Solid

### Goal

Avoid rebuilding complexity before the foundation proves itself.

### Features To Delay Until After Core Reliability

- richer visualization
- more elaborate mission UX
- more advanced prompt tuning
- broader agent role expansion
- parallel execution
- generalized workflow layer
- sophisticated A/B orchestration

### Why

These are valuable, but they should sit on top of a hard, tested core.

## Immediate File-Level Build Plan

The first likely rebuild files are:

- `system/orchestrator/node_contract.py`
- `system/orchestrator/node_validator.py`
- `system/orchestrator/node_lifecycle.py`
- `system/orchestrator/event_schema.py`
- `system/runtime/runtime_interface.py`
- `validation-suite/contract-tests/`
- `validation-suite/scenario-tests/`

This is not a promise about exact filenames forever. It is the current likely starting shape.

## What Will Not Be Reused Blindly From The Prototype

The archived prototype should be used as:

- reference code
- source of pitfalls
- source of regression cases

It should not be treated as code to copy forward wholesale.

Areas to be especially cautious about copying directly:

- lifecycle/status assumptions
- orchestration routing assumptions
- runtime success criteria
- logging layout
- validation structure

## Acceptance Standard For The Rebuild

Before Open-Eywa returns to real live usage, the rebuilt core should satisfy all of the following:

- node contract is implemented in code
- node validation is reliable and test-covered
- offline contract tests pass cleanly
- offline scenario tests pass cleanly
- orchestrator correctness is proven mostly offline
- runtime success depends on artifacts, not process optimism
- logs and metrics are structured and reconstructable
- tiny live canaries run cleanly and cheaply

## Next Step After This Plan

The next build step should be:

- implement the contract kernel first

That means starting with the minimal node model, validator, and lifecycle logic before touching full orchestration or live runtime behavior.
