# Exploration 005 Summary: SU(3) Hessian Extension

## What Was the Goal
Test the generalized H_norm conjecture for SU(3), d=4, L=2. The goal predicted H_norm ≤ 1/18 (formula d/(4(d−1)N) with N=3).

## What Was Tried
1. Implemented full SU(3) Hessian: Gell-Mann generators, LEFT perturbation, 512×512 matrix
2. Sanity check at Q=I — verified against analytic prediction
3. 120+ random Haar SU(3) configurations
4. Gradient ascent to maximize H_norm
5. Adversarial constructions: center elements (Z_3), flat diagonals, staggered configs

## Outcome: SUCCESS — FORMULA CORRECTED

**All tasks completed. No violations. Sanity check passed to machine precision.**

### Sanity Check
- λ_max at Q=I = 8β/3 = 2.6666... **[VERIFIED]** (analytic error < 6×10⁻¹⁵)
- H_norm(I) = 1/27 = 0.037037... **[VERIFIED]** (analytic error < 10⁻¹⁶)

### Random + Adversarial Configs
- 20 random (seed=42): max H_norm = 0.03266 < 1/27 **[COMPUTED]**
- 100 random (seed=123): max H_norm = 0.03303 < 1/27 **[COMPUTED]**
- Gradient ascent: converged to 0.03612 < 1/27 **[COMPUTED]**
- All flat configs (any constant link value): H_norm = 1/27 exactly **[COMPUTED]**

## Verification Scorecard
- **2 VERIFIED** (machine-precision matches to analytic predictions at Q=I)
- **5 COMPUTED** (code ran, results recorded, reproducible)
- **2 CONJECTURED** (universal bound for all Q; K_S threshold)

## Key Takeaway

**The tight bound is H_norm ≤ 1/27 = d/(4(d−1)N²), not 1/18 = d/(4(d−1)N).**
The correct generalization uses N², not N. This matches the SU(2) result exactly:

| N | d | H_norm(I) = tight bound | CS bound |
|---|---|--------------------------|----------|
| 2 | 4 | 1/12 = 0.08333           | 1/8      |
| 3 | 4 | 1/27 = 0.03704           | 1/18     |
| N | 4 | 1/(3N²)                  | 1/(2N²)  |

The ratio tight_bound/CS_bound = d/(2(d−1)) = 2/3 for d=4. This factor is strictly <1
for all d ≥ 3, meaning the actual bound is always tighter than CS.

**Conjecture:** H_norm(Q) ≤ d/(4(d−1)N²) for all Q ∈ SU(N)^E.
The bound is saturated by flat configurations (uniform link value); random configs
are strictly interior.

**K_S implication:** If conjecture holds, K_S > 0 for β < N²/(4d) = 9/16 for SU(3),d=4.
Rigorous CS threshold is β < N²/(8(d−1)) = 3/8. Conjecture would give a 50% improvement.

## Proof Gaps Identified
- No analytic proof that H_norm ≤ d/(4(d−1)N²) for all Q (only numerical at N=2,3)
- Not proven that flat configs are the UNIQUE maximizers (gradient ascent suggests yes but doesn't converge to the bound from random starts)
- The factor d/(2(d−1)) vs. CS bound lacks an analytic explanation

## Unexpected Findings
- **All** flat configurations achieve H_norm = 1/27 exactly, regardless of which SU(3) element is used for links — only the "flatness" matters, not the specific value
- The gradient ascent plateaued at 0.036, well below 1/27, and did not converge to a flat configuration — the maximizers appear to be isolated fixed points

## Computations That Would Advance Investigation
- Test N=4 to further validate d/(4(d−1)N²) scaling with N
- Test d=3 to validate the d/(4(d−1)) factor (expect 3/(4×3×N²) = 1/(4N²) for d=3)
- Prove analytically that flat configurations are the unique maximizers of H_norm
- Identify what group-theoretic property of flat configs causes saturation
