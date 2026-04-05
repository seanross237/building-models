---
topic: Require baseline-adjusted significance for trend detection
category: goal-design
date: 2026-03-27
source: "stochastic-electrodynamics strategy-001 meta-exploration-006"
---

## Lesson

When exploring whether a quantity changes as a function of a parameter β (or any control variable), require the report to compute **baseline-adjusted significance** — not just raw comparison to the reference value. Raw comparison overstates trend significance by ignoring the offset that exists even at β=0.

## The Problem

In SED E003, the significance at β=0.01 was reported as 5.4σ — computed as (var_x_SED − var_x_QM) / σ. This is accurate for the question "does SED differ from QM at β=0.01?" But for the question "does the SED-QM gap *grow* with β?" (i.e., is there an O(β) failure?), the correct significance is:

- Adjusted excess = [SED-QM at β=0.01] − [SED-QM at β=0] = 0.0275
- Combined std: √(σ_01² + σ_0²) = 0.0108
- True O(β) trend significance: **~2.5σ** (not 5.4σ)

The 5.4σ is not wrong, but it answers the wrong question.

## Template Language for Goals

Include in goal: "For each β value, report both: (a) raw significance vs. QM reference, and (b) baseline-adjusted significance = [excess(β) − excess(β=0)] / √(σ(β)² + σ(0)²). This separately tests the absolute discrepancy and the β-dependent trend."

## When to Apply

- Any exploration measuring how a quantity changes with a control parameter (β, coupling, temperature)
- Especially when there is a known β=0 (or control=0) offset that exists even in the baseline

## When NOT to Apply

- When the β=0 baseline is zero by construction (no offset to subtract)
- When the question IS about absolute discrepancy, not trend (then raw significance is correct)

## Note

At large β (β ≥ 0.1 in the SED case), the trend significance and raw significance converge because the β-dependent effect dwarfs the baseline offset. The correction matters primarily at small β where both effects are comparable.
