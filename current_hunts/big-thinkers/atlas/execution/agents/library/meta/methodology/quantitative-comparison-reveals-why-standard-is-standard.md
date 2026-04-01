---
topic: Quantitative comparison of closed vs standard route reveals why the standard method is standard
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-exploration-006 meta"
---

## Lesson

When closing a direction (confirming a route doesn't improve over the standard method), compute the QUANTITATIVE gap between the closed route and the standard route. The magnitude and mechanism of the gap reveal why the standard method became standard, which is itself actionable information.

## Pattern

1. Standard method gives exponent X (e.g., beta = 4/3 via CZ).
2. Alternative method gives exponent Y (e.g., beta = 1 via IBP).
3. Compute the gap X - Y (= 1/3) and identify its mechanism (CZ consolidation of bilinear product enables Chebyshev extraction).
4. The gap mechanism tells you what the standard method is doing that alternatives cannot — which becomes a constraint on future improvement attempts.

## Example: S2-E006

- IBP gives beta = 1 (WORSE than CZ's 4/3 by exactly 1/3).
- The 1/3 gap = the CZ consolidation gain: mapping the bilinear product u^{below} * u^{above} into a single L^p function enables the Chebyshev level-set measure bound to contribute its 1/3 exponent.
- Without consolidation, two v-factors are bounded separately, and 1/2 + 1/2 = 1.

This quantitative comparison immediately shows that CZ consolidation is ESSENTIAL (not just convenient), and any future improvement attempt must either (a) find a different consolidation mechanism, or (b) work within the CZ framework.

## When to Apply

Every time a direction is closed with "doesn't improve beta" or similar, compute the quantitative shortfall and explain its mechanism. The explanation constrains future strategy.

## Distinction from Related Lessons

- **extract-precise-obstruction-from-failed-route:** Extracts what goes wrong in the failed route. This lesson compares the failed route TO the standard route and explains the standard route's advantage.
- **distinguish-constant-from-scaling-slack:** Classifies slack type. This lesson explains the mechanism that creates the gap between routes.
- **tool-independence-stronger-than-single-failure:** Concludes the barrier is structural. This lesson explains WHY the standard method is better (complementary to tool-independence).
