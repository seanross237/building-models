---
topic: Require explicit trend tabulation when testing scaling/universality hypotheses
category: methodology
date: 2026-03-28
source: "riemann-hypothesis s003-meta-exploration-004"
---

## Lesson

When a goal tests a scaling law, universality claim, or monotone hypothesis, **explicitly require a table of the metric of interest at each parameter value and a direct test for monotone trend.** The clean tabulation is what makes a negative result decisive — "the claim seems wrong" is vague; "β_max = 1.32, 1.15, 1.02 for N = 250, 500, 1000 (decreasing, not increasing)" is a clean refutation.

## Evidence

- **riemann-hypothesis strategy-003 exploration-004** — The explorer tested whether N²/p_opt ≈ 275 is universal across N = 250, 500, 1000. The decisive finding was a 3-row summary table showing peak N²/p = 225.6, 309.0, 200.0 (no convergence) and peak β_W_max = 1.318, 1.154, 1.019 (decreasing, not stabilizing). This table alone refutes both the constant-ratio claim and the scaling-law premise. Without the table, the result would have been a fuzzy "results vary across N."

## Recommended Goal Instruction

> "Tabulate [metric] at each [parameter value]. If testing universality, compute the ratio to the hypothesized constant. If testing a scaling law, verify whether the metric is monotonically increasing/decreasing/stabilizing with [control parameter]."

## When to Apply

Any exploration testing a quantitative prediction of the form "X is constant across Y" or "X increases monotonically with Y." The trend table is the primary deliverable — it should be the FIRST table in the report, not buried in analysis.

## Relationship to Other Meta Entries

Complements `decisive-negative-pivot.md` (when to stop investigating) and `specify-computation-parameters.md` (what to specify). This entry is specifically about the **presentation format** that makes negative results clean and reusable: the trend table.
