# April First Planning

## Purpose

This document captures the current plan for making Open-Eywa rock solid, easy to iterate on, and easy for future agents to understand and extend.

We should optimize for:

- simplicity of system design
- flexibility for many future iterations
- reliability under messy or adversarial conditions
- clear documentation for future humans and agents
- minimum downstream churn when code changes

## Core Principle

We want as much of the system as possible to be hard rather than soft.

In practice, that means moving toward minimum reliance on models having predictable outputs.

The guiding idea is:

- models do judgment
- code does protocol

So the code should own:

- state transitions
- required outputs
- valid decision values
- spawn rules
- stale state cleanup
- tool boundaries
- context assembly
- logging and metrics
- recovery rules

The models should mainly contribute:

- planning judgment
- synthesis judgment
- task reasoning
- human-readable content inside bounded tasks

## The Right Order

If our goal is the firmest possible foundation, the work should proceed in this order:

1. define the trust boundary
2. define the canonical contracts
3. do the adversarial review against those contracts
4. design the seams
5. design the test taxonomy and testing guide
6. build the simulated runtime and offline scenario tests
7. harden the deterministic core until the offline suite is strong
8. define the canonical event and metrics schema
9. write the overview docs from the contracts and tests
10. add live-model canaries last
11. enforce change-discipline rules going forward

The important change from the earlier version of this plan is:

we should not start with an adversarial review of the code alone.

We should first define what the system is trying to guarantee, then review the code against that target.

## Phase 1: Define The Trust Boundary

Before reviewing implementation details, define what the code must guarantee and what the model is merely proposing.

This phase should answer questions like:

- what parts of the system are allowed to rely on model judgment
- what parts must never rely on model obedience
- what parts of correctness belong entirely to code
- what kinds of model weirdness the system must tolerate safely

This phase is about deciding where trust stops.

## Phase 2: Define The Canonical Contracts

Next, define the hard contracts of the system.

These contracts should cover at least:

- role contracts
- status contracts
- file contracts
- tool contracts
- orchestration contracts
- logging and metrics contracts

Examples:

- what files each role must produce
- what values are allowed in decision files
- what conditions are required for a node to be considered complete
- what tools may read or write
- what state transitions are legal

This is the real foundation. The rest of the system should derive from these contracts.

## Phase 3: Do The Adversarial Review Against The Contracts

Once the trust boundary and contracts exist, do an adversarial review of the system design and code.

This should ask:

- what is more complicated than it needs to be
- what is brittle
- what is too tightly coupled
- what is too model-dependent
- what is hard for future agents to understand
- what is likely to cause cascading changes later

This should not just be a bug hunt. It should be a structural review with long-term iteration speed in mind.

## Phase 4: Design The Seams

Define the clean interfaces between the major parts of the system.

At minimum, that means the seam between:

- orchestrator
- runtime
- tool executor
- metrics and logging
- docs and tests

This phase should also define the simulated runtime as a first-class interface, not an afterthought.

## Phase 5: Design The Test Taxonomy And Testing Guide

Before rushing into fixes, design the testing structure properly.

This may start with a guide doc for the test suite, since we will probably be making many changes in the future and will want the testing approach documented thoroughly.

That guide should:

- list all the important joints in the system
- list the situations and corner cases for each joint
- explain how those cases should be tested
- rate those cases by how likely they are in practice

That likelihood rating matters because later we may want both:

- full, thorough testing
- fast testing loops

If some cases are extremely unlikely, we may decide they do not always need to run in the fast path.

## Phase 6: Build The Simulated Runtime And Offline Scenario Tests

Then build the tests and run them without actually calling OpenRouter.

The goal here is to make the system sturdy and efficient even before real models are involved.

The test suite should validate that no matter what model responses come back, the orchestration and runtime layers can handle them well.

This means simulating many possible model behaviors, including bad ones, so that the system is robust under:

- missing files
- malformed outputs
- wrong outputs
- repeated outputs
- loops
- process death
- stale state
- duplicate actions
- partial completion
- bad evaluator decisions
- bad synthesizer behavior
- tool misuse

We should fix the system as we learn from these tests, but also keep improving the test suite itself so that it becomes a reliable foundation.

## Phase 7: Harden The Deterministic Core

At this point, the focus is not on live-model behavior.

The focus is on making the deterministic engine boring, strict, and dependable.

This includes:

- valid state transitions only
- no duplicate spawns
- no silent completion
- no stale-file surprises
- no tool boundary leaks
- no hidden coupling between parts of the system

The test suite should not just exist. It should itself be dependable, maintainable, and easy to extend.

It should help prove that the system is:

- efficient
- sturdy
- predictable
- safe against unexpected model behavior

## Phase 8: Define The Event And Metrics Schema

Before building more dashboards, summaries, or visualizations, define the canonical shape of:

- event logs
- tool logs
- usage logs
- run summaries
- high-level metrics

When we do run models, we want excellent logging and tracking of everything that happens.

We should automatically track a rich metrics suite for every run, including at least:

- total runtime
- time spent in each stage
- tokens
- cost
- agents used
- which models were used for which roles
- how models responded
- whether they planned, executed, escalated, looped, or behaved unexpectedly
- which outputs were created
- which recoveries or retries happened
- any unexpected model behavior

We want both:

- deep low-level logs for detailed analysis
- high-level summaries that are clean and easy to inspect at the end of a run

## Phase 9: Write The Overview Docs From The Contracts And Tests

We want a detailed overview doc that explains:

- how the whole system works
- the major components
- the stages and states the system can be in
- a walkthrough of the lifecycle of a run
- links to the relevant tests for each stage or state

This should be downstream of the contracts and tests, not ahead of them.

That way, the docs and the tests reinforce each other.

## Phase 10: Add Models Back In Only After The Foundation Is Solid

After the system is working well offline, the tests run cleanly, and the test suite itself is solid, then we add real models back in and test with OpenRouter.

At that point, we should already trust the orchestration layer.

The live model phase should mostly be validating the model integration layer, not discovering basic system flaws.

## Phase 11: Enforce Change Discipline

We need a clear rule for the future:

any meaningful system change should require updating:

- the relevant tests
- the testing guide when needed
- the main overview doc when needed
- the metrics or event schema when needed

We want to build things in such a way that code changes require the minimum necessary downstream changes.

In practice, that means changes to code should ideally require only small, localized updates to:

- the testing suite
- the metric suite
- visualizations
- overview documentation

This should be an explicit design constraint as we continue building Open-Eywa.

## Foundation-First Roadmap

This is the first concrete roadmap to execute against.

### Milestone 1: Trust Boundary And Contracts

Deliverables:

- a trust-boundary doc
- a canonical contract doc
- a list of hard vs soft responsibilities
- a first pass at explicit success and failure conditions for every role

### Milestone 2: Adversarial Review And Simplification

Deliverables:

- an adversarial review doc of the current architecture
- a list of soft spots
- a list of simplifications
- a proposed target architecture with cleaner seams

### Milestone 3: Simulated Runtime And Test Taxonomy

Deliverables:

- a simulated runtime design
- a test taxonomy guide
- a list of key system joints and corner cases
- a likelihood ranking for those cases

### Milestone 4: Offline Reliability Suite

Deliverables:

- offline scenario tests that do not call OpenRouter
- regression fixtures for known failures
- clear pass/fail gates for deterministic behavior

### Milestone 5: Metrics, Docs, And Live Canaries

Deliverables:

- canonical event and metrics schemas
- overview docs tied to contracts and tests
- small live canary runs
- clean end-of-run summaries with high-level and low-level detail

## Immediate Next Step

Begin with Milestone 1.

The first concrete task should be to write down the trust boundary and the canonical contracts of Open-Eywa before doing more architectural review or more live model testing.
