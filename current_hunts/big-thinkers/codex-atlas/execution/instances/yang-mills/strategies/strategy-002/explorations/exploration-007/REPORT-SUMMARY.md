# Exploration 007 — Report Summary

## Goal

Adversarial review of the claim: "SZZ Lemma 4.1 is 29-138× loose numerically, implying the
Bakry-Émery condition K_S > 0 holds in 4D at β ≤ 0.5, far beyond SZZ's β < 1/48 threshold."

## What Was Tried

1. **Planted configuration analysis**: Computed H_norm for analytical (non-Gibbs) configurations including the identity config, single-link rotations, plaquette patterns, and structured tangent fields on the L=4, d=4 SU(2) lattice.
2. **Staggered tangent discovery**: Found that v_{x,μ} = (-1)^{|x|+μ} v₀ (alternating ±1 by site+direction parity) at the identity configuration achieves the maximum H_norm.
3. **β-independence verification**: Confirmed numerically for β = 0.01 through 5.0.
4. **Non-identity sweep**: Tested single-link rotations, all-link rotations, one-link = -I, Gibbs configs at multiple β values — none exceeded 1/12.
5. **Literature search**: Searched arXiv:2204.12737, arXiv:2509.04688, arXiv:2505.16585 and related papers for explicit Hessian max computations.

## Outcome: PARTIALLY CORRECT, SERIOUSLY OVERSTATED

The claim of "29-138× slack" is **true for Gibbs configurations** but **false for the worst-case**.

**Key finding:** The identity configuration (energy minimum of the action) with the staggered tangent field achieves H_norm = **1/12 ≈ 0.083** in both d=3 and d=4. This is:
- **14× higher** than what E006's adversarial search found (0.0057)
- **β-independent** — constant regardless of coupling
- Achievable at ANY β, not just small β

The E006 adversarial search missed this because it used gradient ascent from random starts and random aligned configs — none of which discover the structured staggered eigenmode at the identity.

## Key Takeaway

**The worst-case slack is 12×, not 138×.** If the identity+staggered maximum can be proved analytically, it would give:
```
K_S = N/2 - max_Hess = 1 - (1/12)×48β > 0  iff  β < 1/4
```
This is a 12× improvement over SZZ (β < 1/48) and 6× over CNS (β < 1/24).

But the **claim that K_S > 0 at β = 0.5 is WRONG**. At the identity with the staggered tangent:
```
K_S = 1 - (1/12)×48×0.5 = 1 - 2 = -1 < 0
```
The Bakry-Émery curvature fails at β = 0.5 (the method can at best extend to β < 1/4).

The confusing E006 measurement was: Gibbs-typical configurations at β = 0.5 give H_norm ≈ 0.020, so "effective K_S" ≈ 0.52 — but this is NOT the mathematical K_S, which requires the worst-case over ALL configurations, including the identity.

## Leads Worth Pursuing

1. **Prove max H_norm = 1/12 analytically**: The formula H_norm = ⌊d/2⌋⌈d/2⌉/(4d(d-1)) (= 1/12 in d=3,4) appears in no published paper. If provable, it yields a new Lemma replacing SZZ's Lemma 4.1 with a 12× tighter bound and threshold β < 1/4.
2. **Verify d-dependence**: In d=5: H_norm_max = 3/40 ≈ 0.075. Test numerically.
3. **Rigorous proof structure**: The staggered-mode saturation needs a formal proof. The calculation is clean — each of 4 (in d=4) active plane-pair types contributes 4β per plaquette coherently. This seems tractable as a formal Lemma.
4. **Why 1/3 of planes are inactive**: The same-parity planes (0,2) and (1,3) in d=4 contribute exactly 0 to the staggered-mode Hessian. This is a geometric identity from the sign cancellation σ₁+σ₂-σ₃-σ₄ = 0, which follows from the staggered pattern structure. This may connect to duality or lattice symmetry.

## Unexpected Finding

The staggered mode gives **identical H_norm = 1/12 in d=3 and d=4** — this appears to be a coincidence of the formula ⌊d/2⌋⌈d/2⌉/(4d(d-1)) = 1/12 for these two dimensions specifically. For d=5 and d=6 the formula gives 3/40 (different value). This dimensional coincidence may have a symmetry explanation.

More provocatively: the "worst-case" configuration is not adversarial at all — it's the **vacuum** (identity). This means any attempt to extend the SZZ Bakry-Émery proof must contend with the ordered phase. The staggered mode Hessian maximum at the vacuum state is the fundamental obstruction, not some rare adversarial configuration.

## Computations Identified

- **Prove max H_norm ≤ 1/12**: Show analytically that ∂²S/∂t² ≤ 4β per plaquette for the staggered mode, with 4 out of 6 plane-pairs active → total ≤ 4×L^d×4β, giving H_norm = 1/12. This is a ~30-line calculation exploiting the sign structure of the staggered pattern. Medium difficulty. Would directly yield β < 1/4 threshold.
- **Tight Bakry-Émery constant for identity config**: The exact maximum eigenvalue of the Hessian matrix at the identity is achievable by diagonalizing the Hessian. This would determine whether H_norm = 1/12 is also the maximum over ALL tangent vectors (not just the staggered one). Medium difficulty, requires ~100-line numerical linear algebra on the full 3×1024 × 3×1024 Hessian matrix.
