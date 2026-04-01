# Exploration 006 — Summary

## Goal
Verify whether M(Q) ≼ M(I) holds as a full operator inequality for SU(2) Yang-Mills d=4. Prove analytically that pure gauge Q gives M(Q) = M(I) up to isometry.

## What was tried

1. **Full operator inequality test:** Built M(Q) and D(Q) = M(Q) - M(I) for 50 diverse configurations on L=2; computed all 192 eigenvalues of D(Q).
2. **Pure gauge isometry:** Proved analytically and verified numerically (10 configs, agreement to 1e-14) that M(Q_pure) = Ad_G^T M(I) Ad_G.
3. **λ_max check:** Verified λ_max(M(Q)) ≤ 4d for 95 configurations (zero violations).
4. **Top eigenspace projection:** Computed the 9×9 matrix P^T R(Q) P for 42 configs.
5. **Gradient ascent:** Ran ascent on both λ_max(M) and λ_max(P^T R P).
6. **Abelian decomposition:** Analyzed the block structure of R(Q) for diagonal configs.
7. **Trace analysis:** Proved Tr(M(Q)) = Tr(M(I)) analytically; checked Tr(M²) dependence on Q.

## Outcome: CRITICAL FINDING + KEY REFORMULATION

**M(Q) ≼ M(I) is FALSE.** Every non-trivial Q has ~96 positive eigenvalues in D(Q) (of 192 total). This includes pure gauge configs (D has eigenvalues ±12 with trace 0). This is structural: Tr(R(Q)) = 0 forces positive and negative eigenvalues.

**However: P^T R(Q) P ≼ 0 for ALL 42 tested Q.** The projection of R(Q) onto the 9-dimensional top eigenspace of K_curl is always non-positive semidefinite. This is the correct reformulation: proving P^T R(Q) P ≼ 0 implies λ_max(M(Q)) ≤ 4d.

## Verification scorecard
- **VERIFIED:** 3 (M(I)=K_curl, pure gauge isometry + conjugation formula, trace conservation)
- **COMPUTED:** 7 (M≼M(I) false, λ_max ≤ 4d, P^T R P ≼ 0, gradient ascent ×2, abelian block structure, Tr(M²) varies)
- **CONJECTURED:** 1 (characterization: λ_max=4d iff invariant color direction exists)

## Key takeaway

**The correct inequality is NOT R(Q) ≼ 0 but P^T R(Q) P ≼ 0** (9×9 matrix inequality on the top eigenspace of K_curl). This holds for all 42 tested configs and withstands gradient ascent. Pure gauge gives M(Q) isospectral with M(I) via the gauge isometry Ad_G^T M(I) Ad_G = M(Q).

## Proof gaps identified

1. **P^T R(Q) P ≼ 0 not yet proved analytically.** The 9×9 matrix involves computing how adjoint transports rotate the staggered-mode color direction. The key: staggered modes have v_{x,μ} = (-1)^{|x|+μ} n for fixed color n ∈ su(2), and the B_□ formula at such v involves Ad_P(n) for various partial holonomies P. Bounding the resulting sum requires controlling the "decoherence" of n under different Ad rotations.

2. **Abelian saturation:** For abelian Q, one eigenvalue of P^T R P is exactly 0 (the invariant τ₃ direction). Any proof must accommodate this boundary case.

## Unexpected findings

1. **Tr(M(Q)) = Tr(M(I)) for ALL Q** — each transport matrix is orthogonal, so the trace is a topological invariant. This forces R(Q) to be trace-free, explaining the half-positive-half-negative eigenvalue structure.

2. **Tr(M²) is NOT conserved** — it drops from 11520 at Q=I to ~10380 at random Haar (9.9% reduction). This means non-trivial Q makes the eigenvalue distribution more uniform (less peaked at 4d).

3. **Gradient ascent on P^T R P stays at -8 to -11** — even when directly optimizing, the top eigenspace projection is strongly negative, suggesting a substantial gap between the achievable maximum and 0.

## Computations identified

1. **Analytical bound on v^T R(Q) v for v in the staggered-mode eigenspace** — requires explicit computation of how B_□(Q, fn) depends on Q for staggered spatial mode f and color direction n.

2. **SU(2)-specific analysis of the 9×9 P^T R P** — the top eigenspace has color ⊗ spatial structure (3 × 3 = 9). The color part is rotated by Ad, the spatial part is fixed. This decomposition might simplify the bound.

3. **Per-plaquette contribution to P^T R P** — decompose the 9×9 matrix into plaquette-by-plaquette contributions and bound each one separately.
