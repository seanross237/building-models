# Exploration 001: Adversarial Stress Test of λ_max Inequality

## Mission Context

We are validating a claimed mass gap proof for lattice SU(2) Yang-Mills at β < 1/6 (an 8× improvement over SZZ's β < 1/48). The proof uses the Bakry-Émery framework: a spectral gap exists if the Hessian of the Wilson action is bounded. The proof chain goes:

1. SZZ Bakry-Émery theorem → spectral gap if HessS bounded ✓
2. HessS(v,v) = (β/(2N)) Σ|B□(Q,v)|² ← **THIS IS THE GAP** (not an identity for Q ≠ I)
3. CS bound: |B□|² ≤ 4Σ|v_e|² ✓
4. Link counting: 2(d-1) plaquettes/link ✓
5. Combine: HessS ≤ 4(d-1)β/N · |v|² → threshold β < N²/(8(d-1)) ✓

The formula in Step 2 is exact at Q = I (flat connections) but NOT exact for generic Q. We need to determine if the inequality λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) holds for ALL Q, which would rescue the proof chain.

## Critical Background: M(Q) vs H(Q)

**The B² formula gives M(Q) = Σ B□ᵀ B□ (the "covariant curl squared operator"). The actual Hessian of the Wilson action is H(Q) = M(Q) - C(Q), where C(Q) involves curvature correction terms from second derivatives of the exponential map.**

- At Q = I: C(I) = 0, so H(I) = M(I), and the formula is exact.
- At generic Q: C(Q) ≠ 0, and C(Q) is NOT positive semi-definite.
- Per-plaquette, H_actual(v,v) can EXCEED H_formula(v,v) by up to ~2× for specific v directions.
- Despite this, λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all ~200 previously tested Q.

**Your job is to determine whether this λ_max inequality holds robustly, or whether it can be broken by adversarial search.**

## Specific Goal

Build both Hessian matrices for SU(2) on L=2 lattice in d=4, and stress-test the ratio r(Q) = λ_max(H_actual(Q)) / λ_max(H_formula(Q)).

### Stage 1: Build and Verify at Q = I

1. Implement the Wilson action S(Q) = -(β/N) Σ_□ Re Tr(U_□) for SU(2) with β = 1.0, N = 2.
2. Build H_actual(Q) using **central finite differences** (step h = 1e-4). The Hessian is a (dE × dim(su(2))) × (dE × dim(su(2))) matrix where dE = number of directed links and dim(su(2)) = 3. For L=2, d=4: there are L^d × d = 16 × 4 = 64 links, so the Hessian is 192 × 192.
   - Perturb link e in color direction a: Q_e → exp(ε · T_a) · Q_e (LEFT perturbation, SZZ convention)
   - T_a = iσ_a/2 (su(2) basis, orthonormal under ⟨X,Y⟩ = -2 Tr(XY))
   - H_actual[(e,a),(f,b)] = ∂²S/∂ε_a^e ∂ε_b^f using central differences
3. Build H_formula(Q) = (β/(2N)) × M(Q) where M(Q) = Σ_□ B□ᵀ B□.
   - **LEFT B□ formula (CRITICAL — use exactly this):**
     B□(Q,v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) - Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) - Ad_{U□}(v_{e₄})
   - where U□ = Q_{e₁}Q_{e₂}Q_{e₃}⁻¹Q_{e₄}⁻¹ is the plaquette holonomy
   - Ad_Q(v) = QvQ⁻¹ for SU(2) (adjoint action, NOT fundamental Qv)
   - For each plaquette □ with edges e₁,e₂,e₃,e₄ (e₃,e₄ traversed backward):
     - P₁ = I (identity — no transport for e₁)
     - P₂ = Q_{e₁}
     - P₃ = Q_{e₁}Q_{e₂}Q_{e₃}⁻¹ (note: includes Q_{e₃}⁻¹)
     - P₄ = U□ = Q_{e₁}Q_{e₂}Q_{e₃}⁻¹Q_{e₄}⁻¹
   - Then B□(v) = v₁ + P₂v₂P₂⁻¹ - P₃v₃P₃⁻¹ - P₄v₄P₄⁻¹
4. **Sanity check at Q = I:**
   - Both matrices should be identical
   - λ_max should be 4β = 4.0 (for β = 1.0)
   - If this fails, STOP and debug before proceeding

### Stage 2: Compare at Random Configurations (50+ configs)

For 50 random SU(2) configurations (Haar-random on each link):
1. Compute H_actual(Q) and H_formula(Q) using numpy.linalg.eigvalsh (exact eigendecomposition, NOT ARPACK)
2. Compute r(Q) = λ_max(H_actual(Q)) / λ_max(H_formula(Q))
3. Record: r(Q), λ_max(H_actual), λ_max(H_formula), ||C(Q)||_op = ||H_formula - H_actual||_op
4. Report statistics: mean(r), max(r), min(r), std(r)
5. **If any r(Q) > 1.0**: STOP — the inequality fails. Report the configuration.
6. Also: for the top eigenvector v_max of H_actual, compute H_actual(v_max,v_max)/H_formula(v_max,v_max). This tests whether the top eigenvector of H_actual "sees" C(Q).

### Stage 3: Adversarial Gradient Ascent (20 starts)

Maximize r(Q) = λ_max(H_actual(Q)) / λ_max(H_formula(Q)) over Q:
1. Start from 20 independent random SU(2) configurations
2. Use gradient ascent: for each link e and color a, compute ∂r/∂Q by finite differences (perturb Q_e → exp(δ·T_a)·Q_e, recompute r, use forward differences with δ = 1e-3)
3. Take gradient steps with small step size (η = 0.01 initially, adaptive)
4. After each step, project back to SU(2) (Q → Q/det(Q)^{1/2} or use the exponential map)
5. Run for 200+ steps per start, or until r converges
6. Record the best r found across all starts and the configuration that achieves it
7. **If any r > 1.0**: STOP — the inequality fails.
8. Also try Nelder-Mead optimization on r (parameterize Q by 3 × 64 = 192 angles, one per link×color)

### Stage 4: Characterize the Gap

Report:
1. The maximum r(Q) found (the "closest approach" to violation)
2. The gap: 1 - max(r) = safety margin for a proof
3. How does max(r) scale with configuration type? (near-identity, near-abelian, random Haar, worst-case)
4. The spectrum of C(Q) = H_formula - H_actual for the worst-case Q. How many positive eigenvalues? What's their magnitude?
5. Does the top eigenvector of H_actual align with positive or negative eigenspace of C(Q)?

## Success Criteria

- **PASS (inequality holds):** max r(Q) < 1.0 after all tests, with gap > 0.01
- **FAIL (inequality broken):** any r(Q) > 1.0 found
- **MARGINAL:** max r(Q) very close to 1.0 (gap < 0.01) — needs larger search

## Failure Criteria

- If Stage 1 sanity check fails (λ_max ≠ 4.0 at Q=I), there's a bug — report and debug
- If gradient ascent doesn't converge, report the trajectory

## Conventions

- SU(2): N = 2, generators T_a = iσ_a/2 for a = 1,2,3
- Inner product: ⟨X,Y⟩ = -2 Tr(XY), so |T_a|² = 1
- Wilson action: S(Q) = -(β/N) Σ_□ Re Tr(U_□) = -(β/2) Σ_□ Re Tr(U_□) for N=2
- LEFT perturbation: Q → exp(ε·v)·Q
- Lattice: L=2 hypercubic torus with periodic boundary conditions, d=4

## What to Write

Write your REPORT.md incrementally — after each stage, write what you found. Include:
- Code (all Python, in `code/` directory)
- Tables of results
- The maximum r(Q) found and the configuration achieving it
- Your assessment: does the inequality hold?

Write REPORT-SUMMARY.md when done (≤30 lines).
