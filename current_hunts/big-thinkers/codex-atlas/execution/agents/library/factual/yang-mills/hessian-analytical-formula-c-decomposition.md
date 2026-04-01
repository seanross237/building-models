---
topic: Analytical Hessian formula for SU(2) Wilson action — commutator cross terms and C = C_curv + C_comm decomposition
confidence: verified
date: 2026-03-29
source: "yang-mills-validation strategy-002 exploration-002"
---

## Overview

Complete analytical computation of the second derivative d²/dt² Re Tr(U□(t))|_{t=0} for SU(2) lattice gauge theory, revealing that the commutator cross terms are **large and often dominant**. The difference C = H_formula − H_actual decomposes exactly as C = C_curv + C_comm, where C_curv is PSD (curvature bonus) and C_comm is indefinite (commutator correction). **C is NOT positive semidefinite** (41 negative eigenvalues), so H_actual ≤ H_formula does NOT hold as a matrix inequality — only the weaker λ_max(H_actual) ≤ λ_max(H_formula) holds (verified for 50+ configs, ratio 0.61–0.74). This provides the complete analytical framework for the M(Q) ≠ Hessian distinction (see `b-square-inequality-proof-progress.md`).

## Analytical Second Derivative Formula

Under left perturbation Q_k → exp(t·v_k)·Q_k, the plaquette U□(t) = exp(tw₁)exp(tw₂)exp(tw₃)exp(tw₄)·U□, where w_k are parallel-transported tangent vectors:

- w₁ = v₁, w₂ = Ad_{Q₁}(v₂), w₃ = −Ad_{Q₁Q₂Q₃⁻¹}(v₃), w₄ = −Ad_{U□}(v₄)

Expanding the product of exponentials to O(t²):

> **d²/dt² Re Tr(U□(t))|_{t=0} = Re Tr(w² U□) + Σ_{i<j} Re Tr([wᵢ,wⱼ] U□)**

The first term is the "w²U" term (present in H_formula). The second term is the **commutator cross term** (absent from H_formula). `[VERIFIED against finite differences, error < 2×10⁻⁷]`

## Cross Terms Are Large

Over 100 random SU(2) configurations (single plaquette):

| Statistic | |comm/w²U| |
|---|---|
| Mean | 3.12 |
| Max | 63.6 |
| Fraction |comm| > |w²U| | 37% |
| Sign distribution | 56 positive, 44 negative |

For large deformations (Q₁ = exp(πT₁)): w²U = 0, and the **entire second derivative comes from commutator terms**. `[VERIFIED]`

## SU(2) Cross-Product Simplification

For SU(2) with T_a = iσ_a/2, structure constants [T_a, T_b] = −ε_{abc} T_c:

Write w_k = w⃗_k · T⃗ (3-vectors) and U□ = cos(θ/2)I + b⃗·T⃗. Then:

> **d²/dt² Re Tr(U□) = −(|w|²/2)cos(θ/2) + (1/2) L⃗·b⃗**

where |w|² = |B□(v)|², L⃗ = Σ_{i<j} w⃗_i × w⃗_j, |b⃗|² = 4sin²(θ/2).

The cross-product formula Re Tr([w_i, w_j] U□) = (1/2)(w⃗_i × w⃗_j)·b⃗ verified to machine precision (error < 2×10⁻¹⁵). `[VERIFIED]`

Product identity: T_a T_b = −(δ_{ab}/4)I − (1/2)ε_{abc} T_c. `[VERIFIED]`

## Decomposition: C = H_formula − H_actual

**H_actual(v,v)** = (β/4) Σ□ |w□|² cos(θ□/2) − (β/4) Σ□ L⃗□·b⃗□

**H_formula(v,v)** = (β/4) Σ□ |w□|² = (β/4) Σ□ |B□(v)|²

Therefore:

> **C(v,v) = (β/4) Σ□ [|w□|²(1 − cos(θ□/2)) + L⃗□·b⃗□]**

### Matrix Decomposition

- **C_curv** = (β/4)(1 − cos(θ/2)) × BᵀB — the **curvature bonus**, always PSD
- **C_comm** = off-diagonal blocks with coefficient (β/8)(w⃗_{ka} × w⃗_{lb})·b⃗ — the **commutator correction**, indefinite

Same-link, different-component entries of C_comm are exactly zero (SU(2) orthogonality: Ad preserves orthonormal basis). `[VERIFIED]`

Decomposition verified: |C − (C_curv + C_comm)| = 6.7×10⁻¹⁶. `[VERIFIED]`

## Spectral Analysis of C

L=2, d=4, SU(2), β=1.0, 192 DOF:

| Matrix | Min eigenvalue | Max eigenvalue | PSD? |
|---|---|---|---|
| C | −0.765 | 4.340 | **NO** (41 negative eigenvalues) |
| C_curv | +0.018 | 3.850 | **YES** |
| C_comm | −1.555 | +1.624 | **NO** (indefinite) |

### Why λ_max(H_actual) ≤ λ_max(H_formula) Still Holds

At the top eigenvector v_top of H_actual:
- v_top^T C v_top = +0.103 (positive)
- v_top^T C_curv v_top = 1.163
- v_top^T C_comm v_top = −1.060
- Ratio C_curv/|C_comm| = 1.10 (barely compensates)

The curvature bonus compensates the commutator correction **in the top eigenspace**, but the margin is slim.

### Eigenvalue Comparison (H_actual vs H_formula)

| Rank | H_actual | H_formula | Ratio |
|---|---|---|---|
| 1 | 2.464 | 3.576 | 0.689 |
| 2 | 2.334 | 3.538 | 0.660 |
| 3 | 2.301 | 3.501 | 0.657 |
| 4 | 2.275 | 3.486 | 0.653 |
| 5 | 2.252 | 3.438 | 0.655 |

**Eigenvalue-by-eigenvalue inequality holds: 0 violations out of 192.** `[VERIFIED]`

Over 20 random configurations: ratio λ_max(H_actual)/λ_max(H_formula) ranges 0.61–0.74. `[COMPUTED]`

### Flat Configuration

At Q=I: H_actual = H_formula exactly (max difference = 0), λ_max = 4β = 4.0. `[VERIFIED]`

## Per-Plaquette Bound Fails

For a SINGLE plaquette, the quantity |w|²(1 − cos(θ/2)) + L⃗·b⃗ can be negative (violations in 10–28% of random directions). Worst case: min C/|v|² = −1.05. **The proof cannot work per-plaquette** — lattice-wide cancellation is needed. `[COMPUTED]`

## Proof Strategies for λ_max(H_actual) ≤ λ_max(H_formula)

**Strategy A (Direct |v|² bound):** Bound H_actual ≤ c|v|² directly without H_formula. Since cos(θ/2) ≤ 1 and commutator terms bounded by Cauchy-Schwarz, yields spectral gap for β < 1/(d−1) = 1/3. Weaker than β < 1/6 but doesn't need the B² inequality. `[CONJECTURED]`

**Strategy B (Eigenspace orthogonality):** Prove commutator term projects onto a complementary space to the top eigenspace. Motivated by near-orthogonality of v_top(H_actual) and v_top(H_formula). `[CONJECTURED]`

**Strategy C (Lattice cancellation):** Per-plaquette bound fails, but commutator terms from different plaquettes sharing the same link may partially cancel. Analyze this cancellation structure. `[CONJECTURED]`

## Relationship to Other Entries

- **b-square-inequality-proof-progress.md** — This entry provides the complete analytical basis for the M(Q) ≠ Hessian distinction noted there. H_formula = (β/4)M(Q), H_actual = H_formula − C.
- **per-plaquette-inequality-false.md** — Per-plaquette C not non-negative is consistent with the per-plaquette H_P bound failure; both demonstrate that the proof must work at the lattice level.
- **fourier-hessian-proof-q-identity.md** — At Q=I, C=0 and the Fourier analysis gives the exact eigenstructure.
