# Exploration 008 — Summary

## Goal
Close Gap 1 from the adversarial review: prove the eigenvalue bound lambda_max(M(Q)) <= 16 for the FULL 9-dimensional top eigenspace P, not just the 3D uniform-color staggered subspace.

## What Was Tried
1. Built the 12x12 per-vertex matrix M_12 and its restriction to the 9D constraint space V = {T : Sum_mu T_mu = 0}
2. Ran 110K+ random configs and 350+ adversarial gradient ascent trials
3. Decomposed the gap as f_same + cross and analyzed the structure
4. Attempted algebraic proof via extending E006's combined bound lemma
5. Tested uniform-color modes with all spatial patterns s

## Outcome: PARTIAL SUCCESS (Strong numerical verification, no algebraic proof)

**The bound holds with 0 violations across all tests.** Best adversarial eigenvalue: 15.997 (below 16). The constraint Sum_mu T_mu = 0 is essential (unconstrained eigenvalue reaches ~21).

**Gap decomposition discovered:** 16||T||^2 - F_x = f_same + cross where f_same >= 0 always. The harmful cross term never exceeds 8.2% of f_same — enormous safety margin. This is the structure a proof must exploit.

**Algebraic proof NOT achieved.** The E006 proof structure does not directly generalize because: (1) trace identity fails for general spatial patterns, (2) base-link budget is insufficient for some configurations, (3) cross-color coupling creates off-diagonal terms not present in the uniform-color case.

## Verification Scorecard
- **VERIFIED:** 3 (budget identity, per-plaquette expansion, M_12 at identity)
- **COMPUTED:** 8 (all numerical tests — zero violations)
- **CONJECTURED:** 2 (algebraic proof structure)

## Key Takeaway
Gap 1 is numerically closed but algebraically open. The per-vertex 12x12 formulation and the gap = f_same + cross decomposition provide the precise framework for a future proof. The bound holds with enormous margin (harmful cross < 8.2% of f_same), suggesting the proof exists but requires a technique beyond the per-plaquette combined bound lemma used in E006.

## Proof Gaps Identified
- Need to prove: max(harmful_cross / f_same) < 1 for all SO(3) rotations and constrained T
- The constraint Sum_mu T_mu = 0 is essential and must be used in any proof
- A matrix-valued extension of the E006 combined bound lemma would suffice

## Unexpected Findings
- The maximizing T is NOT always rank-1 (uniform-color). Min rank-1 fraction = 0.56 at adversarial maxima. This means no simple reduction to the proven uniform-color case exists.
- The cross term is strongly ASYMMETRIC: it mostly helps the gap (up to 3.7x f_same) and rarely hurts (< 8.2% of f_same). This asymmetry is the key structural fact.
- The E006 trace identity (Tr = constant) FAILS for general spatial patterns. The proof cannot rely on trace arguments.

## Computations Identified for Future Work
1. SDP/SOS formulation: express M_12|_V <= 16I as a semidefinite program and check if the dual certificate can be computed symbolically
2. Lean formalization of the budget identity and per-plaquette expansion (these are algebraic and should formalize cleanly)
3. Systematic search for a Cauchy-Schwarz or AM-GM chain that bounds the cross term by f_same
4. Check if the bound lambda_max(M_12|_V) <= 16 holds for ALL compact Lie groups (not just SU(2)), which might suggest a representation-theoretic proof
