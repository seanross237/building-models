# High-Importance Plan Tournament

## Problem
For critical plans (high importance tier), a single reviewer may miss weaknesses or be biased toward a particular approach. The current medium-tier review (plan -> single reviewer -> decider) doesn't provide enough diversity of perspective for plans where getting it wrong is costly.

## Design
Generate 5 candidate plans, each from a separate planner agent given the same goal. Each plan gets a dedicated critic agent. Each critique gets a judge agent evaluating whether the critique is valid. A final decider sees all 5 plans + 5 critiques + 5 judgments and picks the best plan or synthesizes from multiple.

### Flow
1. Spawn 5 planner agents with the same goal (can run in parallel)
2. Collect 5 candidate plans
3. Spawn 5 critic agents, one per plan (can run in parallel)
4. Collect 5 critiques
5. Spawn 5 judge agents, one per critique (can run in parallel)
6. Collect 5 judgments
7. Spawn final decider with all 15 artifacts

### Orchestrator Impact
This needs its own sub-state-machine within the orchestrator. New statuses might include: `generating_candidates`, `critiquing`, `judging`, `final_decision`. The node's status file tracks which phase the tournament is in.

## Key Considerations
- Token cost: 5 planners + 5 critics + 5 judges + 1 decider = 16 agent spawns per plan. Only justified for genuinely high-stakes decisions.
- Determining the importance tier threshold: what score or condition triggers the tournament vs. medium review.
- The parallel phases (steps 1, 3, 5) benefit heavily from the parallel execution expansion.
