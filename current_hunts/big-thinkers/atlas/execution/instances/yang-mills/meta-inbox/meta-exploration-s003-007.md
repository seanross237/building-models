# Meta-Learning Note: Strategy-003 Exploration 007

**Strategy:** 003, Phase 2
**Explorer type:** Standard
**Task:** Prove M(Q) ≼ M(I) via pure gauge orbit + convexity argument

## What Worked Well

- The explorer correctly identified that the goal target (M(Q) ≼ M(I)) was wrong and stated this prominently.
- Independent confirmation of E005's finding adds confidence.
- New analytical result (Δ = 14(cosε − 1) ≤ 0 for single-link excitation) was a genuine proof.
- Identified algebraic invariant B_□ B_□^T = 4I₃ and Haar average E[M(Q)] = 2(d-1)I.
- Stayed focused and productive despite the false goal statement.

## What Didn't Work

- The goal asked to prove something FALSE. This wasted exploration budget. A quick numerical check at the start (5 lines of Python) would have caught this immediately.
- The explorer spent significant effort on Approaches B/C/D for M(Q) ≼ M(I) before confirming it's false.

## Lessons

1. **Always start proof explorations with a numerical sanity check**: Before attempting to prove X, compute X for 5-10 examples. If X fails, it's false — pivot immediately. The GOAL.md should say "First: compute eigenvalues of M(Q) - M(I) for 3 random Q. If any are positive, the full operator inequality is false."

2. **Structural constants are easy wins**: The Haar average E[M(Q)] = 2(d-1)I was computed in ~10 lines of code. Always include "compute the Haar average" as a quick sub-task in spectral bound explorations.

3. **"Useful failure" is genuinely useful**: This exploration confirmed falseness, found new algebraic invariants (B_□ B_□^T = 4I₃), and proved an analytical result for single-link excitations. Even when the main goal fails, secondary results can be valuable.

## Key Findings for Future Strategizers

1. **B_□ B_□^T = 4I₃ per plaquette** (algebraic invariant): Each plaquette contributes exactly 4×(3×3 identity) in color space regardless of Q. This constrains how M(Q) can deviate from M(I).

2. **Haar average E[M(Q)] = 2(d-1)I = 6I**: Far below max of 16. The inequality has enormous average-case slack (average/max = 6/16 = 37.5%). The interesting question is why the maximum remains exactly 16.

3. **Correct target**: λ_max(M(Q)) ≤ 4d (NOT M(Q) ≼ M(I)).
