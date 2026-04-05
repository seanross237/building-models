# Parallel Execution

## Problem
V1 runs all steps sequentially, even when the plan marks steps as independent. This wastes time when multiple steps have no dependencies on each other and could run concurrently.

## Design
Independent steps within a plan run concurrently. The plan already tracks dependency metadata per step (`Dependencies: none | step N, step M` and `Independent: yes | no`). The orchestrator uses this to determine which steps can be spawned simultaneously.

When a planner's status is `approved` or `executing`, the orchestrator identifies all steps whose dependencies are satisfied (all listed dependency steps are `complete`) and spawns them in parallel. Each gets its own child node directory and agent session.

## Key Considerations
- The parent's evaluation phase becomes more complex: it may receive multiple child completions between poll cycles and needs to evaluate them together.
- Replanning must cancel all in-flight children, not just the next unstarted one.
- Resource limits may be needed to prevent spawning too many concurrent agents (e.g., max 3 parallel children per node).
- Orchestrator logging must clearly track which children are running simultaneously for post-run analysis.
