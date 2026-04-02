# Exploration 001 Summary: Maximal Tree Gauge Decomposition

## Goal
Implement maximal tree gauge on L=2, d=4 SU(2) lattice, analyze P^T R(Q) P in tree gauge, classify cotree-link contributions, and assess whether this decomposition yields a tractable proof route for lambda_max(M(Q)) ≤ 16.

## What Was Tried
- Implemented M(Q) (192×192), B-field formula, BFS spanning tree gauge fixing, P (staggered eigenspace, 9-dim)
- Verified gauge covariance of eigenvalues, gauge-fix correctness
- Computed P^T R(Q) P for 25 random gauge-fixed configs + gradient ascent
- Analyzed single-link and two-link perturbations separately
- Investigated the algebraic structure of the staggered eigenspace P
- Ran plaquette-level decomposition of P^T R P

## Outcome: Key Results

**Verification scorecard: 0 proved, 12 computed, 0 verified (Lean), 0 conjectured**

### COMPUTED results:
1. lambda_max(M(I)) = 16, multiplicity 9. Gauge covariance holds (error < 3×10^{-14}).
2. P^T R(Q) P < 0 for all 25 random gauge-fixed configs (max eigenvalue: -6.6 to -8.7).
3. Gradient ascent best: -6.61 (never approaches 0).
4. **Single-link theorem**: For ANY Q differing from I on exactly one edge (all 64 edges × 10 trials = 640 tests), lambda_max(M(Q)) = 16.000000 exactly AND max_eig(P^T R(Q) P) = 0 exactly. The matrix P^T R(Q) P is negative semidefinite with a 3-dimensional null space.
5. Null vectors of P^T R(Q) P satisfy B_□(Q, v_null) = B_□(I, v_null) for all plaquettes affected by the perturbation (B-field invariance; error < 10^{-15}).
6. P_e P_e^T = (9/64) × I_3 for ALL 64 edges (uniform density of staggered eigenspace; error < 4×10^{-16}).
7. Two-link perturbations: max_eig ∈ [-0.02, -0.11] (strictly negative).
8. Per-plaquette Tr(P^T R_□ P) < 0 for all 96 plaquettes in all 3 random configs tested.

## Key Takeaway

**The single-link theorem is the main new finding.** It states: changing any one lattice link from I to an arbitrary U ∈ SU(2) leaves lambda_max(M(Q)) = 16 exactly — the bound is achieved but not violated. The matrix P^T R(Q) P becomes negative semidefinite (max_ev = 0, not just ≤ 0). The null space has a concrete characterization: vectors v in the staggered eigenspace whose B-fields at all affected plaquettes are unchanged.

This is backed by uniform algebraic properties: P_e P_e^T = (9/64) I_3 for all edges and uniform cross-coupling between plaquette-adjacent edges.

## Tractability Assessment: NOT YET TRACTABLE via tree gauge alone

The decomposition is informative but not sufficient:
- **Route A** (prove single-link semidefiniteness algebraically): MODERATE difficulty, a concrete sub-theorem with clear algebraic structure. Requires Fourier analysis on L=2 torus using the uniform density property.
- **Route B** (extend from single-link to all-link): LOW — no inductive structure found.
- Per-plaquette bounds fail: individual plaquettes can contribute positive eigenvalues; the bound requires global cancellation.

## Proof Gaps Identified

1. **Gap 1**: Algebraic proof that Σ_{□ ∋ e0} P^T [M_□(e0=U) - M_□(e0=I)] P ≤_psd 0 for all U ∈ SU(2), any e0. (Uniform density P_e P_e^T = c I_3 is the key ingredient.)
2. **Gap 2**: Understanding why multi-link configs give strict negativity (max_ev < 0) while single-link gives exact 0 — what is the transition mechanism?
3. **Gap 3**: No global proof route from the cotree decomposition; the bound appears to require understanding multi-link coherence.

## Unexpected Findings

- The staggered eigenspace has a "color-uniform" density at every edge (P_e P_e^T = c I_3), a property not previously noted in the goal description.
- The single-link theorem holds for ALL 64 edges (tree and cotree alike), not just cotree edges.
- U = -I (center element) gives exact Tr(P^T R P) = -4.875 = -9 × (13/24), suggesting exact algebraic structure.

## Computations Identified for Follow-Up

1. **Prove the single-link theorem algebraically** using the Fourier decomposition of M(I) and the su(2) adjoint orthogonality. This is the most tractable next step.
2. **Characterize the null space** of P^T R(Q) P at single-link configs: is it always the same 3-dim subspace (independent of U, or depending only on e0)?
3. **Test on larger lattices** (L=4, d=4): does the single-link theorem generalize, and does the uniform density P_e P_e^T = c I_3 still hold?
4. **Second-order analysis**: compute d²/dt² max_eig(P^T R(exp(tv))P)|_{t=0} to characterize the curvature at the Q=I saddle.
