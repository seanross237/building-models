---
topic: Scope computational explorations to the minimum diagnostic test
category: goal-design
date: 2026-03-28
source: "riemann-hypothesis s003-meta-exploration-008"
---

## Lesson

For computationally intensive explorations, specify the MINIMUM computation needed to answer the question — not a broad validation mandate. When given a broad goal ("validate with 5000 zeros and N=300 GUE"), the explorer will run all available approaches (replication, truncation analysis, N-dependence, matched K=N test) instead of the one diagnostic test that would settle the question.

## Evidence

- **riemann-hypothesis strategy-003 exploration-008** — Goal was "validate λ_n^zeta/λ_n^GUE crossover with 5000 zeros + larger GUE." Explorer ran 4 separate computation paths: (1) full replication of E002 at 2000 zeros, (2) truncation analysis at multiple K values, (3) N-dependence study, (4) matched K=N test (incomplete at cutoff). Only paths 2 and 4 were needed. The replication was redundant (E002 already verified); the N-dependence was interesting but not the question. The primary comparison (K=N=5000) ran out of context before completing because earlier computations consumed context and wall-clock time.

## Better Goal Framing

Instead of: "Validate the crossover with 5000 zeros and N=300 GUE matrices"

Use: "Compute λ_n^zeta / λ_n^GUE at matched K=N=500, 1000, 2000, 3000, 5000 and tabulate the ratio at n=100, 300, 500. Extrapolate: does the ratio at n=500 converge to a value below 1 as K=N increases, or does it approach 1?"

The second framing specifies exactly what to compute and what question to answer — no room for scope expansion.

## When to Apply

Any exploration where:
1. A specific quantitative question needs answering (e.g., "does this ratio stay below 1?")
2. Multiple computational approaches exist but only one is diagnostic
3. Wall-clock time or context limits are binding constraints (especially Math Explorer sessions >45 min)

## Relationship to Other Lessons

Distinct from `one-task-per-exploration.md` (which is about not combining unrelated cognitive tasks). This lesson is about scoping WITHIN a single computational task: even when the explorer is working on one question, it will naturally expand to all available computational paths unless the goal restricts it to the diagnostic minimum.
