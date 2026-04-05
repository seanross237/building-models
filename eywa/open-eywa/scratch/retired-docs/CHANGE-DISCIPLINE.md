# Open-Eywa Change Discipline

This guide is for any future agent or human changing the rebuilt `Open-Eywa` system.

The goal is simple:

- keep the architecture simple
- keep changes compartmentalized
- keep the offline simulation model in sync with the real system
- make future A/B testing and iteration safer, not harder

## Non-Negotiables

- Do not bypass the node contract.
- Do not bypass the runtime seam.
- Do not add orchestration behavior that cannot be exercised offline.
- Do not treat implementation as complete until the relevant validation coverage is updated.

## Current Source Of Truth

For the current rebuild, use these docs first:

- `BUILDING-PRINCIPLES.md`
- `GROUND-UP-REBUILD.md`
- `april-first-planning/canonical-node-contract-spec.md`
- `TRUST-BOUNDARY.md`
- `CANONICAL-CONTRACTS.md`
- this file

If behavior changes materially, update the relevant docs, especially `OPEN-EYWA-GOAL-AND-OVERVIEW.md` when the high-level story changes.

## Required Change Loop

When changing the system:

1. identify what kind of change it is
   - contract change
   - orchestration behavior change
   - runtime/tool behavior change
   - logging/event/summary change
   - pure internal refactor
2. decide what must stay stable
   - node meaning
   - runtime seam
   - event meaning
   - tool boundaries
3. make the smallest compartmentalized code change possible
4. update or add validation coverage
5. run the validation suite
6. update docs if the behavior or contract changed

## What Must Trigger Test Updates

Update tests when you change:

- node statuses
- node control files
- terminal outcome semantics
- event names or required payload fields
- runtime request/result shape
- tool behavior or tool boundaries
- recovery, cancellation, waiting, or progression behavior
- mission summary meaning

## What Test Coverage Should Look Like

### Contract tests

Use contract tests when the change affects hard rules:

- valid node structure
- valid transitions
- required files
- allowed tool boundaries
- recovery/cancellation rules
- schema validity

### Scenario tests

Use scenario tests when the change affects system behavior:

- parent/child progression
- evaluator decisions
- waiting and resume
- recovery and retry flows
- mission-level behavior
- runtime/tool interactions

### Regression rule

If a bug is found in a run, add a regression test for it.

Prefer:

- a scenario fixture if it is about runtime/orchestration behavior
- a contract test if it is about a hard validity rule

## Architecture Guardrails

Prefer adding small modules over growing one large file.

Right now the main pressure points are:

- `system/orchestrator/orchestrator_progression.py`
- `system/orchestrator/event_schema.py`
- `system/orchestrator/node_preparation.py`
- `system/orchestrator/mission_driver.py`

If a change makes one of these files significantly more complex, strongly consider extraction first.

## A/B Testability Rule

Changes should preserve or improve:

- explicit `model` and `variant` recording
- append-only raw event history
- stable mission/node/run boundaries
- prepared inputs through the runtime seam

Do not add hidden behavior that makes variants harder to compare later.

## Validation Commands

Run these after meaningful system changes:

```bash
python3 -m unittest discover -s validation-suite/contract-tests -p 'test_*.py'
python3 -m unittest discover -s validation-suite/scenario-tests -p 'test_*.py'
python3 -m py_compile $(find system -name '*.py' | sort)
```

## Fast Rule Of Thumb

Before declaring a change done, ask:

- Did I change a contract?
- Did I change runtime behavior?
- Did I add or update the right offline test?
- Did I keep the change localized?
- Would another agent understand this change from the files on disk?

If the answer to any of those is no, the change is probably not finished yet.
