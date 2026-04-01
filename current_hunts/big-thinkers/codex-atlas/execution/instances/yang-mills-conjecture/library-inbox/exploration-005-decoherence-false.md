# Exploration 005: The Cross-Term Decoherence Lemma — Proof Attempt

## Goal
Prove ||C(Q)||_op ≤ 2(d+1) for all Q ∈ SU(2)^E (the "decoherence lemma"), which would complete the mass gap proof giving β < 1/(2d).

## Key Discovery: The Decoherence Lemma is FALSE for d ≥ 3

**[COMPUTED]** Adversarial gradient ascent on ||C(Q)|| found configurations exceeding 2(d+1):

| d | ||C_flat|| = 2(d+1) | Adversarial max ||C|| | Exceeds? |
|---|---------------------|----------------------|----------|
| 2 | 6.00 | 5.68 | **No** |
| 3 | 8.00 | 8.60 | **Yes** |
| 4 | 10.00 | 11.68 | **Yes** |

For d=4: the counterexample has ||C|| = 11.68, verified independently with SU(2) constraint errors < 10⁻¹⁵. The configuration is obtained by gradient-ascending from an anti-instanton (Q_μ = iσ_{a(μ)}) for ~2000 iterations.

At this counterexample: D_min = -1.40 (small!), λ_min(H) = -11.90 (< 4d = 16). The self-term nearly vanishes, allowing the cross-term to dominate.

## Discovery 1: Closed-Form SVD of the Color Kernel F

**[VERIFIED]** The 3×3 color kernel F_{ab}(M,N) = Re Tr(iσ_a M iσ_b N) has the exact form:

**F(M,N) = -2(β₀I₃ + [β⃗×]) R_M**

where:
- R_M ∈ SO(3) is the adjoint representation of M
- MN = β₀I + iβ⃗·σ⃗ (quaternion decomposition), β₀² + |β⃗|² = 1
- [β⃗×] is the 3×3 cross-product matrix

**Singular values: (2, 2, 2|β₀|)**

Verified to machine precision (error < 10⁻¹⁵) over 100 random (M,N) pairs. At flat (M=N=I): β₀=1, SVs=(2,2,2). At general Q: third SV drops to 2|β₀| < 2.

This formula reveals F decomposes as -2PR where P = β₀I+[β⃗×] has SVs (|β₀|, 1, 1) and R ∈ SO(3). The "deficient direction" of F is β⃗ (left space) and R^Tβ⃗ (right space).

## Discovery 2: Per-Plaquette Decoherence — PROVED

**[VERIFIED]** For a single plaquette □ with 4 edges, 6 cross-term pairs, each with ||B_{pq}|| ≤ 1:

**Theorem:** ||C_□(Q)||_op ≤ 3 = ||C_□(flat)|| for all Q ∈ SU(2)^4.

**Proof:** For unit v = (v₀,...,v₃) ∈ ℝ¹², with r_p = ||v_p||:

|v^T C_□ v| = |Σ_{p<q} 2 s_p s_q v_p^T B_{pq} v_q|
≤ Σ_{p<q} 2 ||B_{pq}|| r_p r_q ≤ Σ_{p<q} 2 r_p r_q
= (Σ r_p)² - Σ r_p² ≤ 4·Σr_p² - Σr_p² = 3||v||² = 3.   ∎

The Cauchy-Schwarz step uses (r₁+r₂+r₃+r₄)² ≤ 4(r₁²+r₂²+r₃²+r₄²). Equality at flat when r_p = 1/2 for all p and color directions n_p = s_p n.

Confirmed numerically: 0/19200 plaquettes across 200 random d=4 configs exceeded 3.0. Gradient ascent on isolated plaquettes converges to ≈ 3.0 (flat value).

## Discovery 3: Full Decoherence Proved for d = 2

**[VERIFIED]** Aggregating the per-plaquette bound to the full lattice:

|v^T C v| ≤ Σ_□ [(Σ_{p∈□} r_{ep})² - Σ_{p∈□} r²_{ep}]
= r^T(JJ^T)r - 2(d-1) ≤ ||JJ^T|| - 2(d-1) = ||A_struct||

where J is the unsigned edge-plaquette incidence matrix and A_struct is the unsigned edge-pair overlap.

||A_struct|| values: d=2: **6 = 2(d+1)** ✓, d=3: 12 > 8, d=4: 18 > 10.

**For d=2: ||C(Q)|| ≤ 6 = 2(d+1) for ALL Q.** Complete proof of the decoherence lemma.

For d ≥ 3: the bound is too loose because it loses inter-plaquette sign correlations. The gap ratio ||A_struct||/||A_total|| = 1.0 (d=2), 1.5 (d=3), 1.8 (d=4).

## Approach Results Summary

| # | Approach | Bound (d=4) | Tight? |
|---|---------|-------------|--------|
| 1 | Tensor product (|A_total|_abs) | 18 | No |
| 2 | Per-block norm ||G_ef|| | 15 | No |
| 3 | Aligned color (Schur product) | ≤ 5.0 aligned, ×1.8 misalignment | N/A |
| 4 | Per-plaquette triangle | 252 | No |
| 5 | Variational (perturbation) | Flat IS local max | Local only |
| **New** | Per-plaquette + lattice | 18 (= ||A_struct||) | d=2 only |

## Why the Lemma Fails: Anti-Correlation Breakdown

At the counterexample config (||C|| = 11.68 for d=4):
- D_min = -1.40 (self-term nearly zero)
- λ_min(H) = -11.90 (still < 4d = 16)

The mechanism: anti-instanton configs + gradient ascent pushes toward saddle points of the Wilson action where Re Tr(U_□) ≈ 0. At these points:
- D ≈ 0 (self-terms vanish since plaquette traces ≈ 0)
- ||C|| grows beyond 2(d+1) because the sign structure of C no longer matches the flat pattern
- But |D| + ||C|| remains < 4d because the C eigenvalue and D bias partially anti-correlate

The per-plaquette bound ||C_□|| ≤ 3 holds everywhere, but the AGGREGATION loses the inter-plaquette sign structure that keeps ||C|| bounded at flat.

## What Still Holds

**[COMPUTED]** Despite the decoherence lemma failing, the full Hessian bound appears valid:

| Config type | |D_min| | ||C|| | |D_min|+||C|| | |λ_min(H)| | < 4d? |
|-------------|---------|-------|--------------|-----------|-------|
| Flat | 6.00 | 10.00 | 16.00 | 16.00 | = 4d |
| Anti-inst (pure) | 6.00 | 8.65 | 14.65 | 14.18 | ✓ |
| Anti-inst (GD λ) | 5.60 | 9.83 | 15.43 | 14.73 | ✓ |
| GD on ||C|| | 1.40 | 11.68 | 13.08 | 11.90 | ✓ |

The D/C anti-correlation ensures |λ(H)| < 4d even when ||C|| > 2(d+1).

## Implications for the Mass Gap Proof

The β < 1/8 result **CANNOT** be obtained by bounding D and C separately. The path forward requires either:

1. **Bound the full Hessian directly**, using the D/C anti-correlation (e.g., show |λ(H)| ≤ 4d without decomposing)
2. **Use a different decomposition** of H that doesn't separate self/cross terms
3. **Prove the weaker bound** ||C|| ≤ K for some K with 2(d-1) + K ≤ 4d, i.e., K ≤ 2(d+1). But this IS the decoherence lemma, which fails.

Option 1 seems most promising: prove |λ(H)| ≤ 4d directly using the Wilson action structure.

## Code

- `code/hessian_core.py`: Hessian computation, F formula, SVD analysis
- `code/approach_tests.py`: All 6 approach tests
- `code/gradient_ascent_C_norm.py`: Gradient ascent on ||C||
- `code/decoherence_proof.py`: Per-plaquette proof, lattice aggregation, aligned norm
- `code/proof_attempt.py`: Schur product and contraction analysis
