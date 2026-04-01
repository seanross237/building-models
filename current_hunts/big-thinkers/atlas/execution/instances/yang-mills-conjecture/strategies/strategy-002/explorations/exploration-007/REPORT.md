# Exploration 007: Bound Non-Staggered Eigenvalues of M(Q)

## Goal

Prove that ALL eigenvalues of M(Q) ≤ 16 for the full 192×192 matrix on L=2, d=4. The staggered subspace (9D, eigenvalue 16 at Q=I) is already proved. Focus on non-staggered eigenvalues, which start at 12 (Q=I) and grow to ~14.6 for random Q.

## Critical Discovery: λ_max > 16 is ACHIEVABLE

**[COMPUTED]** Edge-by-edge gradient ascent found gauge configurations Q with λ_max(M(Q)) ≈ **16.08**, exceeding 16. This was reproduced across multiple trials and verified with two independent M(Q) formulations. The claim λ_max(M(Q)) ≤ 16 for all Q is **FALSE**.

However: for RANDOM gauge fields (2000+ configs), λ_max never exceeded 14.64. The violation requires careful optimization — it does not appear naturally.

## Stage 1: Eigenvalue Structure at Random Q

**[COMPUTED]** M(I) eigenvalue structure verified: {0(×57), 4(×36), 8(×54), 12(×36), 16(×9)}.

| Quantity | Max | Mean | Violations (>16) |
|----------|-----|------|-------------------|
| Full λ_max (300 random) | 14.615 | 14.158 | 0 |
| Non-stag λ_max | 14.430 | 13.945 | 0 |
| R\|_nonstag max | 12.382 | 11.695 | 300/300 (>4) |
| Stag λ_max | 9.920 | 8.372 | — |

**[COMPUTED]** Top eigenvector is spread across all M(I) momentum sectors (0-eigenspace dominates 76% of trials). Sector-by-sector approaches fail.

## Stage 3: Uniform Q — Fourier Block Analysis

**[VERIFIED]** For uniform Q (all links = g), M(Q) block-diagonalizes by Fourier transform. Verified λ_max(M_k(g)) ≤ 16 for all k and g over fine grid (200 angles × 5 axes × 16 momenta).

| n_π components | Max eigenvalue | At g=I |
|----------------|---------------|--------|
| 0 | 16.000 | 0 |
| 1 | 12.000 | 4 |
| 2 | 8.000 | 8 |
| 3 | 12.000 | 12 |
| 4 (staggered) | 16.000 | 16 |

**Proof for k=(π,π,π,π):** B_{μ,ν} = (I+g)(w_μ − w_ν). Along rotation axis: ‖I+g‖² = 4. Complete graph K_4 Laplacian max eigenvalue = 4. So R_max = 4×4 = 16. ∎

## Stage 2: Gradient Ascent — THE BOUND FAILS

**[COMPUTED]** Edge-by-edge optimization (coordinate ascent) on λ_max(M(Q)):

| Trial | Method | λ_max found |
|-------|--------|-------------|
| 0 | Edge-by-edge (correct formula) | 16.0146 |
| 1 | Edge-by-edge (correct formula) | 16.0099 |
| 2 | Edge-by-edge (correct formula) | 16.0495 |
| 3 | Edge-by-edge (correct formula) | 16.0086 |
| 4 | Edge-by-edge (correct formula) | **16.0824** |

**Verification:** M is symmetric ✓, PSD (min eigenvalue ≈ 0.05) ✓, Tr = 1152 ✓. Rayleigh quotient of top eigenvector confirms the value.

## B-Field Formula Verification

**[VERIFIED]** The B-field linearization was verified numerically against direct perturbation of the plaquette holonomy:

B_p(a) vector = Q_1 a_1 + Q_1 Q_2 a_2 − Q_1 Q_2 a_3 − Q_1 Q_2 Q_3^{-1} a_4

The Q_1 factor cancels in the squared norm |B_p|², so M(Q) = ∑B_p^T B_p is invariant under the choice of base-frame convention. Two different formulations (code's convention and derived convention) give **identical eigenvalues** for all tested Q, confirming gauge invariance.

**[COMPUTED]** M(Q) ≠ Hessian of Wilson action: the Hessian includes a curvature correction term from the second derivative of the exponential map. The discrepancy is O(1) in eigenvalues.

## Stage 5: Multi-Scale Verification

**[COMPUTED]** Random Q tests (no optimization):

| L | N_dim | M(I) max | Random max | Bound 16 holds? |
|---|-------|----------|------------|-----------------|
| 2 | 192 | 16 | 14.615 | Yes (random) |
| 3 | 972 | 12 | 14.100 | Yes |
| 4 | 3072 | 16 | 14.131 | Yes |

All hold for random Q, but the L=2 gradient ascent shows violations are possible with optimization.

## Failed Proof Approaches

1. **R|_nonstag ≤ 4:** FAILS. R goes up to ~16 due to gauge-rotation of eigenspaces.
2. **Cauchy-Schwarz per-plaquette:** ‖B_p‖² ≤ 4∑|v_e|², each edge in 6 plaquettes → λ_max ≤ 24. Factor 1.5× too loose.
3. **Gershgorin (block):** Row sums give λ_max ≤ 36+.
4. **Projection decomposition:** M = 4∑P_p where P_p is rank-3 projection. Need ∑P_p ≤ 4I. Equivalent to original problem.

## Key Structural Insight

M(Q) = ∑B_p^T B_p is the "covariant curl squared" operator, NOT the Hessian of the Wilson action. The Hessian equals M(Q) minus a curvature correction:

H(Q) = M(Q) − C(Q)

where C(Q) involves Tr(U_p) terms from d²(exp)/dε². The curvature correction C is NOT positive semidefinite.

## Conclusions

1. **λ_max(M(Q)) ≤ 16 is FALSE.** Gradient ascent found λ_max ≈ 16.08.
2. **For random Q, λ_max < 15 always.** The violation requires targeted optimization.
3. **For uniform (flat) Q, λ_max = 16 exactly.** The bound is tight on the flat connection moduli space.
4. **The per-vertex staggered bound F_x ≤ 16‖T‖² remains valid** — the violation comes from non-staggered modes only.
5. **M(Q) ≠ Wilson action Hessian.** This is a critical distinction for the mass gap argument.
