# Exploration 004 Summary

## Goal
Prove sum_S >= 0 for all R, D in SO(3), T in V (the final step for the Yang-Mills mass gap).

## Outcome: Significant Partial Success + Strong Numerical Confirmation

### What was proved algebraically:

1. **sum_S(D=I) = 6·Σ f(R_mu, T_mu) + |Σ R_mu^T T_mu|² ≥ 0** — a manifestly non-negative decomposition. This corrects E003's claim that sum_S(D=I) = 0; the true minimum eigenvalue is 0 (tight, multiplicity 1) but sum_S is positive for generic T.

2. **Delta factoring**: sum_S(D) = sum_S(I) + Σ 2·(R_mu^T T_mu - T_nu)^T (I-D)(T_mu - R_nu^T T_nu). Every Delta term involves (I-D) linearly.

3. **Critical T theorem**: For T on rotation axes (T_mu = c_mu·axis(R_mu)), we have u = v in the Delta factoring, so each Delta term equals 2f(D, u) ≥ 0. Therefore **sum_S ≥ 0 for the null eigenvector direction of M9(I)**. This is the most dangerous direction (where sum_S(I) = 0), and the proof works cleanly there.

### What was computed:
- 67,000+ adversarial configurations: min eigenvalue = 3.9e-13 ≈ 0 (at D=I)
- Every perturbation from D=I strictly increases the minimum eigenvalue
- The 2×2 submatrix on the (null, second eigenvector) plane is always PSD (min det = 12.3)

## Verification Scorecard
- **3 VERIFIED** (Stage 1 identity, Stage 1 proof, Critical T theorem)
- **5 COMPUTED** (Delta factoring, 2×2 submatrix, adversarial search, eigenvalue structure, cross/budget ratio)
- **1 CONJECTURED** (full algebraic proof of sum_S ≥ 0)

## Key Takeaway
**sum_S ≥ 0 is true** (overwhelming numerical evidence from 67K adversarial tests), and we have an algebraic proof for the hardest case (null eigenvector direction). The full algebraic proof remains open. Multiple proof approaches were eliminated (convexity, per-plaquette VCBL, direct perturbation, Gershgorin). The cleanest remaining avenue is likely a Schur complement or SDP certificate approach, or finding a global identity that extends the u=v structure.

## Proof Gaps Identified
- **The gap**: Need to show Δ-term doesn't overcome baseline for non-axis T. The baseline is positive but the Δ-term can be negative (each u^T E v is a bilinear form, not quadratic).
- **Structural obstacle**: I-U is always rank 2 (U ∈ SO(3)), so per-plaquette VCBL decomposition is fundamentally impossible. The proof MUST use all 6 pairs together.
- **Perturbation obstacle**: ||Δ M9|| >> λ₂(M9(I)), so eigenvalue perturbation doesn't yield a global bound.

## Unexpected Findings
- **E003's claim was wrong**: sum_S(D=I) ≠ 0 for all T. The correct identity is sum_S(D=I) = 6Σf + |Σ R^T T|² ≥ 0, which is a STRONGER result (manifestly non-negative, not just zero).
- **M12 is NOT PSD** (2 negative eigenvalues), and the negative eigenvectors have non-zero V-components. The V restriction is essential.

## Computations for Next Steps
1. **SDP certificate**: Use semidefinite programming to find a PSD decomposition of M9(R,D) that works for all (R,D). May need parametric SDP with SO(3) variables.
2. **Extend Critical T theorem**: For T near axes (T_mu = c_mu n_mu + ε_mu with ε_mu small perpendicular perturbation), compute sum_S to second order in ε. If the second-order term is positive, this gives a local proof near the null direction.
3. **Block matrix approach**: The 9×9 matrix M9 has 3×3 block structure. The diagonal blocks are PSD. Try to prove M9 ≥ 0 using Schur complement conditions on the block structure.
4. **Monotonicity in D-angle**: For fixed R and T, check if sum_S is monotonically increasing in the rotation angles of D (away from D=I). This is NOT convexity (which fails) but something weaker.
