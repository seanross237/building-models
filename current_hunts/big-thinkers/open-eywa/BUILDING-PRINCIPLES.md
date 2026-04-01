# Open-Eywa Building Principles

This is the main doc future agents should read before making meaningful Open-Eywa changes.

Use it to understand:

- the architectural values to preserve
- the trust boundary to respect
- the practical change discipline to follow

Related docs:

- `OPEN-EYWA-GOAL-AND-OVERVIEW.md`
  - the north star
- `OPEN-EYWA-IMPLEMENTATION-DETAILS.md`
  - how the current system works
- `april-first-planning/canonical-node-contract-spec.md`
  - the detailed node contract

## Core Idea

Open-Eywa should be a simple, sturdy, node-first system that is easy to build upon, easy to measure, easy to A/B test, and able to improve over time without collapsing into hidden complexity.

## Current Foundation Shape

The current foundation is:

- node-first
- contract-first
- simulation-first before live model testing
- file-based and inspectable
- compartmentalized
- designed for future experimentation and comparison

## Principles

### 1. Node-First

The node is the stable unit of work, truth, inspection, measurement, and recovery.

Agents may change. Models may change. Prompts may change. Tools may change.

The node should remain the durable unit the rest of the system can rely on.

### 2. Code Owns Protocol

Models should contribute bounded intelligence inside a hard structure.

Code should own:

- protocol
- correctness
- state transitions
- artifact validation
- boundaries
- recovery logic
- logging and measurement

This is the core trust boundary:

- models do judgment
- code does protocol

### 3. Simulation Before Spend

The system should be exerciseable offline before live API usage.

If important orchestration behavior cannot be simulated and tested, it is probably not solid enough yet.

### 4. Contracts Before Cleverness

Explicit contracts are better than hidden conventions.

Prefer:

- named files
- closed state meanings
- explicit seams
- validated artifacts
- small clear modules

over behavior that only works because prompts or agents happen to behave well.

### 5. Human Inspectability Matters

A human should be able to look at the files on disk and understand what happened.

Open-Eywa should remain visible, legible, and reconstructable from its artifacts and events.

### 6. Compartmentalize Aggressively

Keep parts easy to change without forcing large downstream rewrites.

Prefer small modules and narrow seams over large multipurpose files.

When complexity grows, extract rather than pile on.

### 7. Design For A/B Testing

The system should make experiments easier, not harder.

Preserve:

- stable node boundaries
- stable run boundaries
- explicit variant recording
- append-only event history
- prepared inputs through explicit seams

Do not hide behavior in places that make variants hard to compare later.

### 8. Events Are Facts, Metrics Are Views

Raw events should record what happened.

Metrics and summaries should be derived from those facts.

Do not blur the two.

### 9. Prepared Context Beats Filesystem Guessing

Whenever possible, agents should be given prepared context packets instead of needing to discover system structure by wandering the filesystem.

That makes runs more reliable, more testable, and easier to compare.

### 10. Naming Should Be Explicit

Names should help humans understand the system quickly.

Prefer names that reveal purpose over names that are short but vague.

### 11. Build For Iteration

Open-Eywa is meant to be iterated on repeatedly.

Changes should leave the system easier to extend, easier to evaluate, and easier for future agents to understand.

### 12. Every Failure Should Teach The System

When a real failure is discovered, it should become:

- a clearer contract
- a better guardrail
- a test
- or all three

The system should get stronger as it is used.

## Trust Boundary

If something matters for correctness, it should live on the hard side of the system.

Code should own and enforce:

- legal node states
- legal state transitions
- required artifacts
- path and tool boundaries
- recovery and cancellation rules
- event logging
- usage and cost recording
- retry behavior
- prepared context assembly
- mission and node summaries

Models may contribute:

- planning
- evaluation
- synthesis
- bounded reasoning
- tool choice inside allowed boundaries
- human-readable writing

Models should not be trusted to:

- decide what counts as done
- decide what file paths are valid
- discover protocol rules from prose alone
- maintain orchestrator state correctly
- avoid stale files automatically
- emit valid control values reliably without code checks

## Practical Change Rules

When changing Open-Eywa:

1. identify the kind of change
   - contract
   - orchestration behavior
   - runtime or tool behavior
   - event or summary behavior
   - internal refactor
2. keep stable what should remain stable
   - node meaning
   - runtime seam
   - event meaning
   - tool boundaries
3. make the smallest compartmentalized change possible
4. update or add offline validation coverage
5. run the validation suite
6. update docs if behavior, philosophy, or implementation shape changed

## What Must Trigger Test Updates

Update tests when you change:

- node statuses
- node control files
- terminal outcome semantics
- event names or required payload fields
- runtime request or result shapes
- tool behavior or tool boundaries
- recovery, cancellation, waiting, or progression behavior
- mission summary meaning

## Preferred Validation Shape

Use contract tests for:

- hard validity rules
- required files
- legal transitions
- tool boundaries
- schema validity

Use scenario tests for:

- parent and child progression
- evaluator decisions
- waiting and resume behavior
- recovery and retry flows
- mission-level behavior
- runtime and tool interactions

If a bug is found in a real or simulated run, add a regression test for it.

## Architectural Guardrails

Do not bypass:

- the node contract
- the runtime seam
- offline exerciseability for important orchestration behavior

Prefer adding small modules over growing one large file.

Current pressure points to watch:

- `system/orchestrator/orchestrator_progression.py`
- `system/orchestrator/event_schema.py`
- `system/orchestrator/node_preparation.py`
- `system/orchestrator/mission_driver.py`

If a change makes one of these much more complex, extract first.

## Validation Commands

Run these after meaningful system changes:

```bash
python3 -m unittest discover -s validation-suite/contract-tests -p 'test_*.py'
python3 -m unittest discover -s validation-suite/scenario-tests -p 'test_*.py'
python3 -m py_compile $(find system -name '*.py' | sort)
```

## Growth Directions

These are major long-term areas of growth:

- plan creation, evaluation, and execution
- efficient knowledge retrieval / acquisition
- system for self experimenting with strong feedback loops
- an efficient plan simulation system

## Practical Builder Heuristic

When making a change, ask:

- does this keep the node as the durable center of truth?
- does this make the system more or less inspectable?
- does this keep protocol on the hard side of the trust boundary?
- does this preserve offline testability?
- does this keep future A/B testing easier?
- does this keep the change localized?
- did I update the right tests and docs?

If the answer to several of those is no, the change is probably moving in the wrong direction.
