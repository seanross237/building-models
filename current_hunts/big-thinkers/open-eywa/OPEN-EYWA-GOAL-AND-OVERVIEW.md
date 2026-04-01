# Open-Eywa Overview

## North Star

Open-Eywa is being built as a simple, sturdy, node-first agent system that is easy to build upon, easy to A/B test, and able to record what happens for evaluation.

It is designed to be iterated. We want automated iteration ability, with thorough testing to evaluate the system and its components. We are building a system that can grow and learn. We are moving toward a system that will grow in capacity over time, toward the end of being able to tackle any goal, large or small.

Code should own protocol and correctness. Models should contribute bounded intelligence inside that hard structure.

## Major Areas Of Growth

- plan creation, evaluation, and execution
- efficient knowledge retrieval / acquisition
- system for self experimenting with strong feedback loops
- an efficient plan simulation system

## Current Foundation

The rebuild is currently grounded in these principles:

- node-first
- contract-first
- simulation-first before live model testing
- file-based and human-inspectable
- compartmentalized and easy to change
- designed for future experimentation and comparison

The durable unit of the system is the node. Agents are temporary contributors inside a node. The node is where truth, status, outputs, recovery state, and measurement live.

## What Open-Eywa Is Trying To Be

Open-Eywa is not meant to be a fragile prompt bundle or a hidden agent cloud.

It is meant to be:

- a visible system
- a testable system
- a system that can improve itself over time
- a system whose parts can be swapped, compared, and evaluated
- a system that can grow in capability without losing structural clarity

## Current Architecture Shape

High-level layout:

```text
open-eywa/
├── OPEN-EYWA-GOAL-AND-OVERVIEW.md
├── BUILDING-PRINCIPLES.md
├── CLAUDE.md
├── AGENTS.md
├── stuff-for-agents/
├── missions/
├── validation-suite/
├── future-expansions/
├── viz/
└── system/
```

Core rebuild areas:

- `system/orchestrator/`
  - node contract, lifecycle, progression, mission driving, recovery, preparation
- `system/runtime/`
  - runtime seam, simulated runtime, and tiny real OpenRouter runtime path
- `system/tools/`
  - controlled local tool layer
- `validation-suite/`
  - contract tests, adversarial tests, and scenario tests

## Node Model

A node is a durable work container with explicit on-disk state.

Each node centers on:

- `input/`
- `output/`
- `for-orchestrator/`
- `system/`
- `children/`

The current closed node statuses are:

- `pending`
- `active`
- `waiting_on_computation`
- `finished`
- `failed`

Current terminal outcomes are:

- `completed`
- `escalated`
- `cancelled`

## Runtime Model

The orchestrator talks to a runtime through a stable runtime interface.

Right now:

- the real orchestrator runs
- the runtime seam is real
- the main confidence-building runtime is still the simulated runtime
- a tiny real OpenRouter runtime path now exists for initial integration work
- the system can already load real prompt bundles from `stuff-for-agents/`
- the live canary path has now completed both a real single-node run and a real multi-step tree run

This lets Open-Eywa stay offline-first while beginning to bridge toward real model execution.

There is now also a tiny live canary path for cheap real-runtime trials once an API key is present.

## Validation Model

Validation is a first-class part of the architecture.

There are three main layers:

- contract tests
  - hard rules and invariants
- adversarial tests
  - compact weird-case tests for fast sturdiness checks
- scenario tests
  - end-to-end orchestration behavior under simulated runtime conditions

The design goal is that meaningful system changes should either:

- keep tests unchanged because the contract stayed stable, or
- require focused test updates because the real behavior changed

The system also now has a one-command fast sturdiness loop for quick confidence checks during iteration:

```bash
python3 system/scripts/run_fast_sturdiness_suite.py
```

## Builder Guidance

Open-Eywa should be changed in a way that keeps the implementation, tests, docs, and runtime seam aligned.

The main builder guide for this is:

- `BUILDING-PRINCIPLES.md`

## Near-Term Direction

The current journey is:

1. finish making the offline system sturdy and easy to evolve
2. keep the fast validation loop strong as the system grows
3. expand the tiny real runtime path carefully and test it with cheap canaries

The point is not just to get something working. The point is to get something that can keep improving without collapsing into a brittle mess.
