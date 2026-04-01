---
topic: Distinguish constant slack from scaling slack in iterative proof measurements
source: "vasseur-pressure s2-meta-exploration-002"
date: 2026-03-30
---

## Lesson

When measuring the "tightness" of an inequality in a De Giorgi or similar iterative proof, the key question is NOT "is there slack?" but "does the slack scale with the energy parameter U_{k-1}^{-delta}?" Constant multiplicative slack (ratio independent of k and U) only affects the constant C in the recurrence U_k <= C^k * U_{k-1}^beta — it does NOT improve the exponent beta. Only slack that grows as U_{k-1} shrinks (i.e., scales as U_{k-1}^{-delta} for some delta > 0) can improve beta.

## The Distinction

**Constant slack (affects C, not beta):** Measured inequality overestimates by a fixed factor (e.g., 3-5x) independent of the energy level U_{k-1} and the iteration depth k. Accumulates multiplicatively to C^K over K levels but does not change the convergence criterion.

**Scaling slack (affects beta):** Measured inequality overestimates by a factor that grows as U_{k-1} -> 0. In the De Giorgi context, this would mean |{v_{k-1} > 2^{-k}}| <= (something) * U_{k-1}^{5/3 + delta}, giving beta = 4/3 + delta/2.

## Operational Protocol

When designing tightness measurement explorations:
1. Measure the ratio (bound / actual) across multiple De Giorgi levels k
2. Check whether the ratio is constant, growing, or shrinking with k
3. If constant or shrinking: slack is non-transformative (affects C only)
4. ALSO check whether the ratio correlates with U_{k-1} — this is the decisive test for beta improvement
5. Make sure explorers understand this distinction BEFORE launching measurements

## Evidence

S2-E002: De Giorgi Chebyshev tightness ratios were ~3-5x across all ICs and k=1..8. Ratios decreased or stayed constant (TG: ~0.89^k; ABC: ~0.87^k). This was correctly interpreted as "constant slack, does not improve beta" — but the distinction should have been built into the exploration goal from the start.

E004: CZ tightness ratios for P_k^{21} similarly k-independent. Same conclusion.

Both confirmed constant slack. Neither measured U_{k-1}-dependence explicitly (would require DNS with different initial energy levels, holding structure constant).

## Complementary Entries

- Distinct from `test-improvability-before-pursuing-variations.md` (tests circularity of a proof step, not measurement interpretation)
- Distinct from `decomposition-audit-before-attacking-barrier.md` (identifies which step to attack, not how to interpret measurements)
- Complements `sufficient-ic-diversity-for-outliers.md` (IC diversity can reveal whether slack is flow-dependent, as S2-E002 showed with ABC p < 10/3)
