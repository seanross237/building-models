# Open-Eywa Trust Boundary

## Purpose

This document defines what Open-Eywa code must guarantee and what models are only allowed to propose.

The main rule is:

- models do judgment
- code does protocol

Open-Eywa should move toward minimum reliance on models having predictable outputs.

## Hard Responsibilities: Code Must Guarantee These

The codebase should own and enforce:

- legal node states
- legal state transitions
- required files for each role
- exact conditions for success, failure, escalation, and completion
- spawn and respawn rules
- one-active-run-at-a-time rules
- stale-file cleanup rules
- file path boundaries
- tool permissions
- context assembly
- event logging
- usage and cost accounting
- retry limits
- zombie detection
- background job lifecycle
- mission-level summaries

If these behaviors matter for correctness, they should not depend on model obedience.

## Soft Responsibilities: Models May Contribute These

Models are still useful for:

- deciding how to decompose a task
- deciding how to phrase a plan
- deciding how to phrase a review
- deciding how to synthesize multiple results
- writing human-readable notes
- carrying out bounded reasoning inside a node
- choosing among allowed tools inside a constrained task

These are quality-sensitive tasks, but they should not define protocol correctness.

## What Models Must Not Be Trusted To Do

The system should not rely on models to:

- decide what counts as done
- decide whether a node is complete
- decide whether a file path is valid
- discover protocol rules from prose alone
- remember where critical files live
- maintain correct orchestrator state
- avoid stale files automatically
- avoid duplicate actions automatically
- produce valid decision values reliably
- keep retrying forever in a useful way

Where possible, code should narrow these freedoms or remove them entirely.

## Trust Boundary By Layer

### Orchestrator

The orchestrator should be treated as authoritative for:

- mission bootstrap
- status transitions
- child creation
- review / decision / evaluation / synthesis routing
- background wait and resume
- terminal mission outcome

### Runtime

The runtime should be authoritative for:

- loading prompts and instructions
- assembling model context
- exposing only allowed tools
- validating artifacts before accepting a turn as done
- recording loop history and usage
- detecting no-progress and malformed-response conditions

### Tools

The tool layer should be authoritative for:

- read and write boundaries
- command timeouts
- structured results
- command logging
- background job metadata

### Models

Models should be treated as bounded contributors inside these controlled interfaces, not as trusted controllers of the system.

## Design Consequences

This trust boundary implies that Open-Eywa should move toward:

- typed tools over generic filesystem spelunking
- prepared context packets over open-ended file discovery
- strict output validation over optimistic completion
- narrow allowed decisions over free-form protocol text
- offline simulation for reliability testing
- regression fixtures for every discovered failure mode

## Practical Rule

When deciding whether something belongs in code or in prompts, ask:

If the model behaved unexpectedly here, could the system still remain correct and inspectable?

If the answer is no, that behavior belongs on the hard side of the boundary and should be enforced by code.
