# Task

## Goal

Rank plausible high-level research routes toward the Navier-Stokes existence and smoothness problem under a tight exploratory budget.

## Success Criteria

- Build a structured belief state for the problem.
- Generate multiple plausible route families.
- Score the routes by expected success, information gain, option value, cost, and risk.
- Run at least 3 planning cycles.
- Keep a human-readable record of the run inside this folder.
- Produce a final favored route and brief justification.

## Constraints

- Tight budget: only a few cycles of exploration.
- Do not attempt a proof.
- Focus on route identification, ranking, and replanning.
- Keep the record self-contained.
- Do not modify anything outside this run folder.

## Assumptions

- The problem is treated as a research-planning target, not a direct theorem-proving task.
- The best route is likely to be one that produces sharp intermediate milestones and strong pruning power.
- Existing mathematical knowledge is summarized at a high level; the run does not depend on external citations.

## Candidate Route Families Considered

1. `criticality-and-concentration`
2. `partial-regularity-and-epsilon-bootstrapping`
3. `frequency-cascade-and-structure-rules`
4. `barrier-and-morrey-control`

## Working Hypothesis

The highest-value route under budget is the one that most quickly converts the global regularity question into a smaller family of sharply testable subclaims.
