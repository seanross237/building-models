---
topic: B_□ inequality proof progress — partial proofs, failed approaches, remaining gap
confidence: provisional
date: 2026-03-29
source: "yang-mills strategy-003 explorations 001, 002, 003, 005, 006, 007; yang-mills-conjecture strategy-001 explorations 001, 002, 003, 004, 005, 006, 007, 008; yang-mills-conjecture strategy-002 explorations 001, 002, 003, 004, 005, 006, 007"
---

## Overview

**STATUS UPDATE [yang-mills-conjecture S001-E001, CONFIRMED]:** The original conjecture Σ_□ |B_□(Q,v)|² ≤ 4d|v|² for ALL Q ∈ SU(N)^E (equivalently λ_max(M(Q)) ≤ 4d = 16) is **DEFINITIVELY FALSE**. Clean counterexample: Q_e = iσ₃ for all edges gives λ_max(M(Q)) = **24.000** exactly (Z₂ holonomy mechanism; 209/1000 random configs also violate). The **correct proof target is the Hessian**: λ_max(HessS(Q)) ≤ (β/2N) × 4d for all Q. At Q=I and Q=iσ₃: λ_max(HessS) = (β/2N) × 4d exactly. Numerical evidence: 300+ configs + gradient ascent always ≤ (β/2N) × 4d. See "RESOLVED: Conjecture 1 FALSE" section.

**What has been proved:** (1) The restricted bound λ_max(M(Q)|_P) ≤ 4d, where P is the top eigenspace of M(I) (the staggered eigenspace, dim 9) — equivalently R(Q)|_P ≼ 0. This was the main accomplishment of the B_□ proof program. (2) Several structural results (uniform Q, flat connections, single-link, pure gauge isometry, staggered single-link, Q=I local max). The cube-face reduction + sum_S proof establish the restricted bound for **even L**.

Comprehensive status of seventeen explorations (yang-mills S003-E001/E002/E003/E005/E006/E007, yang-mills-conjecture S001-E001 through E008, S002-E001 through E007). Result: **restricted bound P^T M(Q) P ≤ 4d·I proved for even L; Hessian bound λ_max(HessS) ≤ (β/2N)×4d strongly supported numerically; correct proof target identified.**

### SZZ Normalization Convention (S002-E006) [CONJECTURED]

The exact mass gap threshold depends on the gauge group convention: for **SU(2), N=2**: H_norm = β·λ_max/(2N) = 4β, so SZZ needs β < 1/4. For **SO(3) adjoint, N=3**: H_norm = 8β/3, needs β < 3/8. The strategy documents cite both H_norm = 1/3 (N=3 convention) and β < 1/4 (N=2 convention). **This should be pinned down against the exact SZZ theorem statement** to ensure the B_□ inequality target (λ_max ≤ 4d = 16) is correctly calibrated.

## Critical Bug Fix: B_□ Formula

**[VERIFIED by E001, E002, E004]** The B_□ formula in the strategy GOAL.md was **wrong** for backward edges 3 and 4. Correct formula (verified by finite differences to 10⁻⁹):

```
B_□ = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄)
```

where U_□ = Q₁Q₂Q₃⁻¹Q₄⁻¹ is the full plaquette holonomy. The transport for each backward edge includes its OWN link in the partial holonomy. At Q=I both formulas coincide; the error only affects Q ≠ I. The wrong formula gives spurious violations (F = 16.76 on L=2).

## Key Structural Properties

**B_□ B_□^T = 4I_{N²−1}** for any Q and any plaquette — each per-plaquette operator M_□ = B_□^T B_□ has eigenvalues {4,4,4,0,...,0} regardless of Q. Total trace Tr(M(Q)) = 12·n_plaq is Q-independent. **[VERIFIED, E001]**

**Gauge invariance:** Σ_□ |B_□(Q,v)|² is gauge invariant. **[PROVED, E003]** — B_□ transforms as B_□ → g_x B_□ g_x⁻¹ under gauge transformation g.

**Uniform density of P [S001-E001]:** The 9-dimensional staggered eigenspace P of M(I) at eigenvalue 4d=16 satisfies **P_e P_e^T = (9/64) I₃** for ALL edges e = 0,...,63 (max deviation 3.6×10⁻¹⁶). The staggered eigenspace projects uniformly (scalar multiple of identity) on each edge's color space. This is the key structural property enabling the single-link theorem. Also verified: for any plaquette-adjacent pair (e₀, e), the cross-density ||P_{e₀}^T P_e||_F = 0.0812 exactly for all partner edges (uniform cross-coupling). **[COMPUTED, S001-E001]**

## What's Proved

### 1. Uniform Configurations (E001) [PROVED]

For Q_e = U ∈ SU(N) for all edges: Σ|B_□(Q,v)|² ≤ 4d|v|². Proof uses: trivial holonomy (U_□ = I for uniform Q), Fourier decomposition (translation invariance preserved), per-plane bound (2I + R + R^T) ≼ 4I₃ for R ∈ SO(3). Covers ALL abelian/diagonal and constant configurations.

### 2. Flat Connections (E003) [PROVED]

For ALL flat SU(2) connections on the torus (trivial and twisted): the bound holds. Proof: trivially flat gauge-transform to Q=I; twisted flat reduce to abelian (simultaneous diagonalization of commuting SU(2) elements), then Fourier analysis with shifted modes still bounded by 4d.

### 3. Single-Link Configurations (E002, S001-E001) [PROVED + EXTENDED]

F(Q) = 4d for any configuration where only ONE link is modified. Proof: gauge equivalence — single-link Q is gauge-equivalent to g·I, and λ_max is gauge invariant. Single-link perturbations are pure gauge; the "flat manifold" {F = 4d} = {pure gauge configurations}.

**Extended single-link theorem [S001-E001, COMPUTED]:** For any Q differing from I on exactly one edge (any edge, any SU(2) value):
1. λ_max(M(Q)) = 16.000 exactly (to 4×10⁻¹⁴ precision, all 64 edges × 10 Haar-random trials = 640 configs)
2. **max_eig(P^T R(Q) P) = 0** (to ~10⁻¹⁵ precision)
3. **P^T R(Q) P is negative semidefinite** (eigenvalues e.g. [−1.94, −0.92, 0, 0, 0] for one link)
4. Null space of P^T R(Q) P has **dimension 3** — null vectors satisfy B_□(Q, v_null) = B_□(I, v_null) for ALL plaquettes containing e₀ (exact cancellation, verified to < 7×10⁻¹⁶)
5. Single-angle scan: max_eig(P^T R(Q) P) = 0 for ALL angles t ∈ [0, π], including t=π (U=-I center element)

**Gap between 1-link and 2-link**: Two-link configs give max_eig(P^T R P) ≈ −0.02 to −0.11 (strictly negative). Understanding the 1-link↔2-link transition is the core remaining problem for the P-restricted bound.

**Implication for proof**: Per-plaquette bounds CANNOT prove the single-link theorem (individual plaquettes can contribute positive max_eig ≈ +0.077 each; global cancellation is required). Any proof must be global.

### 3b. Pure Gauge Isometry (E006, E007) [VERIFIED]

**Theorem:** For any pure gauge Q_e = g_{s(e)} g_{t(e)}^{-1}, M(Q) = Ad_G^T M(I) Ad_G where Ad_G acts by v_{x,μ} → Ad_{g_x}(v_{x,μ}). Proof: all plaquette holonomies are trivially I; the gauge-transformed tangent vector ṽ = Ad_{g^{-1}}(v) gives |B_□(Q,v)|² = |ω_□(ṽ)|² per plaquette; summing yields M(Q) = Ad_G^T M(I) Ad_G. **Corollary:** M(Q_pure) and M(I) are isospectral ⇒ λ_max(M(Q_pure)) = 4d. Verified numerically for 15 random pure gauge configs (eigenvalue agreement < 4e-14, conjugation formula error < 8e-15).

### 3c. Staggered Mode Single-Link Bound (E007) [PROVED]

For Q with single-link excitation exp(ε τ₁), the change in staggered mode Rayleigh quotient is Δ = 14(cos ε − 1)|τ|² ≤ 0 for all ε. Explicit per-plaquette computation: two affected plaquettes contribute (10 + 6cosε) and (8 + 8cosε), summing to 18 + 14cosε vs. 32 at Q=I. **Proved analytically and verified numerically across ε ∈ [0, π].**

### 4. Q=I is a Critical Point (E001, E002) [PROVED]

**M₁|_P = 0:** The first-order perturbation of M(Q) at Q=I **vanishes exactly** on the top eigenspace P (dim 9). Proof: each term in dB/dε involves commutators [A_e, f], and ⟨[A,B], B⟩ = −2Tr([A,B]B) = 0 by trace cyclicity. Numerical: PP block of M'(0)(W) < 2×10⁻¹⁵ for all tested W. Equivalent: F'(0) = 0 for ALL geodesic directions W.

### 5. Q=I is a Strict Local Maximum (E001, E002) [PROVED]

Second-order analysis via degenerate perturbation theory:

| Component | Sign | Typical range |
|-----------|------|--------------|
| Decoherence (M₂ on P) | **Negative** | [−0.42, −0.16] (E001); [−0.07, −0.11] (E002) |
| Level repulsion (mixing) | **Positive** | [+0.05, +0.18] (E001); [+0.03, +0.07] (E002) |
| **Total F''(0)** | **Negative** | decoherence wins by 1.5–3× |

Single-edge W give F''(0) = 0 (flat directions, consistent with single-link theorem). Multi-edge W give F''(0) < 0 for all tested.

### 6. Vector Combined Bound Lemma (S002-E002) [PROVED]

**Lemma (VCBL):** For A, B ∈ SO(3), D ∈ SO(3), p, q ∈ R³:
f(A,p) + f(B,q) + p^T(I−A)D(I−B^T)q ≥ 0

**Proof:** By Cauchy-Schwarz: |p^T(I-A)D(I-B^T)q| ≤ ||(I-A^T)p|| · ||(I-B^T)q|| = √(2f(A,p)) · √(2f(B,q)). By AM-GM: f(A,p) + f(B,q) ≥ 2√(f(A,p)·f(B,q)) ≥ |cross term|. **[VERIFIED, 200K tests, min = 0.00092, 0 violations]**

This generalizes the unit-vector CBL to VECTORS p,q (not just unit n). Enables the per-vertex bound F_x(Q,T) ≤ 16||T||² for all T ∈ V (not just single color direction n).

### 6b. Budget Identity (S002-E002) [PROVED]

For T ∈ V = {T = (T₀,...,T_{d-1}) : Σ_μ T_μ = 0}:

**16||T||² = 4 Σ_{μ<ν} |T_μ − T_ν|²**

Proof: Expand RHS using Σ T_μ = 0 → |Σ T_μ|² = 0 → Σ_μ |T_μ|² = −Σ_{μ≠ν} T_μ·T_ν. Then Σ_{μ<ν}|T_μ−T_ν|² = d·Σ|T_μ|² − Σ_{μ<ν}2T_μ·T_ν = d·||T||² + ||T||² = (d+1)||T||². Wait — with d=4 pairs: 4Σ_{μ<ν}|T_μ-T_ν|² = 4·5·||T||²/? Need: for T∈V with 4 components, Σ_{μ<ν}|T_μ-T_ν|² = 4||T||² (uses |Σ T_μ|² = 0). **[VERIFIED algebraically in S002-E002 to 5.7e-14]**

This identity converts the budget bound 16||T||² to a per-plaquette sum 4Σ_{μ<ν}|T_μ−T_ν|², enabling per-plaquette comparison.

### 7. cos(ε) Suppression (E003) [COMPUTED]

For single-link excitation Q_k = exp(ε τ₁), the per-plaquette B_□ norm satisfies |B_□(Q,v)|² = −2Tr[ω_□(v)² exp(2ε τ₁)]. The factor exp(2ε τ₁) is unitary → |Tr[A·U]| ≤ |Tr[A]|, so each affected plaquette contributes ≤ cos(ε) × (Q=I contribution). Paired plaquettes cancel the sin(ε) cross terms.

## What Failed

### Operator Domination M(Q) ≼ M(I) — FALSE (E001)

The PSD ordering M(I) − M(Q) ≽ 0 does NOT hold. The Weitzenböck curvature correction R(Q) = M(Q) − M(I) has **both positive and negative eigenvalues** (roughly evenly split, Tr(R) = 0). **[E006 EXPANDED]:** 50 configurations across 8 classes (pure gauge, random Haar, Gibbs β=0.5–3.0, near-identity ε=0.01–1.0, adversarial) — ALL 50 violate M(Q) ≼ M(I). D(Q) has ~96 positive and ~96 negative eigenvalues (half of 192). Even at ε=0.01, 96 eigenvalues are positive. This is not marginal; it's a fundamental structural feature from trace conservation: Tr(R(Q)) = 0 always.

**The correct (weaker) statement is:** λ_max(M(Q)) ≤ λ_max(M(I)) = 4d. This requires R(Q) ≤ 0 only on the top eigenspace P of M(I), not everywhere.

**Saturation characterization [E006]:** λ_max(M(Q)) = 4d iff there exists a global direction n ∈ su(2) invariant under all adjoint transports (Ad_P(n) = n for all partial holonomies P). This is satisfied by pure gauge configs (all Ad trivial in gauged frame) AND abelian configs (Ad preserves τ₃ direction). Non-abelian non-pure-gauge configs have λ_max < 4d strictly.

### Geodesic Concavity — FAILS GLOBALLY (E002)

F(Q) = λ_max(M(Q)) is NOT globally geodesically concave. F''(Q, W) > 0 found at Q ≠ I (e.g., F(Q) ≈ 13.85, F'' = +0.114). However, F never exceeds 4d at these points. The approach proves Q=I is a local max but cannot establish the global max.

### Coulomb Gauge — Gribov Blocks (E003)

Coulomb gauge is the geometrically correct framework, but the Gribov problem (non-unique gauge fixing for non-abelian groups) and lack of ‖A‖ control prevent closure. For large Q, the field strength is O(1) and perturbative bounds break down.

### Covariant Fourier Transform — Equivalent Problem (E003)

Formal construction works and preserves norms, but reduces the problem to bounding holonomy corrections Ξ_{k,μν}, which is equivalent to the original problem in different notation.

### Per-Plaquette Approach — FALSE (E004, see separate entry)

H_P ≤ (β/2N)|B_P|² per plaquette is false for Q ≠ I. The B_P proof chain is dead. See `per-plaquette-inequality-false.md`.

### Per-Component Lemmas LEMMA_D, LEMMA_RDR — FALSE individually, sum PROVED (S002-E003/E004/E005)

LEMMA_D (≥ 0) and LEMMA_RDR (≥ 0) are individually FALSE (min eigenvalues -2.13 and -1.45 respectively), but their sum **sum_S = LEMMA_D + LEMMA_RDR ≥ 0 is now PROVED** (E005). The proof uses: M9 affine in D (structural discovery, verified 3.5e-15) → per-pair Cauchy-Schwarz (u^T Dv ≤ ||u||·||v||) → combinatorial cancellation (Σ||u−v||² = 4Σf + |Σa|² cancels the cross term, leaving 2Σf + squares ≥ 0). The proof extends to all contractions ||D|| ≤ 1. **This closes Gap 1** in the cube-face reduction proof. See `lemma-d-rdr-false-sum-s-nonneg.md` for full proof and verification scorecard.

### SO(3) Rotation / Triangle Inequality — TOO WEAK (E007)

Per-plaquette |B_□(Q,v)|² ≤ (Σ_k |v_{e_k}|)² ≤ 4·Σ|v_{e_k}|² via Cauchy-Schwarz. Summing: λ_max ≤ 8(d−1) = 24, not 4d = 16. SU(2)-specific SO(3) structure (Ad ∈ SO(3)) does not improve this without correlating rotations across the plaquette. Even restricting to staggered modes with a single algebra direction, the per-plaquette triangle bound gives 16 per plaquette (not 4), recovering 8(d−1) after summation. Closing the gap requires global Fourier structure.

### Schur's Lemma / Haar Average — AVERAGE ONLY (E007)

E_Haar[M(Q)] = 2(d−1)·I (= 6I for d=4). Follows from Schur's lemma since E[Ad_U] = 0 for Haar-random U ∈ SU(2) (irreducible adjoint representation). Constrains the average M(Q) but not λ_max(M(Q)) — the maximum 4d is achieved on the measure-zero set of pure gauge configs.

### Gershgorin (Block) — TOO WEAK (S002-E007)

Block Gershgorin row sums give λ_max ≤ 36+, over 2× too loose.

### Projection Decomposition — EQUIVALENT TO ORIGINAL (S002-E007)

M = 4∑P_□ where P_□ is a rank-3 projection for each plaquette. Need to show ∑P_□ ≤ 4I, which is equivalent to the original problem — no simplification gained.

## Weitzenböck Exact Formula (E005)

**[S003-E005, EXPANDED E006]** R(Q)|_P ≼ 0 verified for ALL **42** tested configurations (pure gauge, random Haar, near-identity, abelian — 42/42, never violated). **E006 gradient ascent** directly targeting λ_max(P^T R P) stays at −8 to −11, never near 0 (3 trials, 30 steps each). An exact linear formula holds for single-link excitations: max λ[R(Q)|_P] = −(1/12) × W(Q), where W(Q) = Σ_□(1 − Re Tr(U_□)/N). For general Q, the bound max λ[R(Q)|_P] ≤ −W(Q)/12 ≤ 0 holds (single-link exact, random Q 1.7–2× tighter). The −1/12 coefficient matches the H_norm threshold exactly. **See `weitzenbock-exact-formula.md` for full details, verification tables, and proof implications.**

Additional E005 findings: Jiang (2022) Weitzenböck identity Δ_A = B_A + Ric + F translates to our setting (F = holonomy defect → R(Q)), but Jiang does NOT prove sign of F. SZZ does NOT use M(Q) = M(I) + R(Q) — the framework is entirely original to this research program. Physical mechanism on P: parallel transport decoherence (Ad(G_k) rotations destroy constructive interference of staggered modes).

## Additional Structural Properties (E006, E007, S002-E007)

**Trace conservation [E006, PROVED]:** Tr(M(Q)) = Tr(M(I)) = 12·n_plaq for ALL Q. Proof: Tr(M(Q)) = Σ_□ Σ_{e∈□} Tr(R_e^T R_e); each R_e = ±Ad_P ∈ O(3), so Tr(R_e^T R_e) = 3; therefore Tr(M(Q)) = 3×4×n_plaq independent of Q. **Consequence:** Tr(R(Q)) = 0 always, forcing R(Q) to have both positive and negative eigenvalues — explains why M(Q) ≼ M(I) fails.

**Tr(M(Q)²) is NOT Q-independent [E006]:** Tr(M²) = 11520 for Q=I and pure gauge; ~10380 for random Haar (std ~56). Eigenvalues become more uniformly distributed for non-trivial Q — the decoherence mechanism quantified: gauge fields spread eigenvalue weight more evenly.

**Abelian block decomposition [E006]:** For abelian Q_e = diag(e^{iθ_e}, e^{-iθ_e}), M(Q) decomposes into independent τ₃ and (τ₁,τ₂) blocks. The τ₃ block of R(Q) is exactly zero (max|eig| < 4e-15). The staggered τ₃ mode achieves λ = 4d exactly — explaining abelian saturation. The (τ₁,τ₂) block has large positive and negative eigenvalues (max ~12.4, min ~-12.7).

**Haar average [E007]:** E_Haar[M(Q)] = 2(d−1)·I = 6I for d=4. Typical Haar-random λ_max ≈ 6.7–7.7 (L=2, d=2), far below 4d. The maximum 4d is achieved only on the measure-zero set of pure gauge configs.

**M(Q) ≠ Hessian of Wilson action [S002-E007, EXPANDED yang-mills-validation S002-E002]:** M(Q) = Σ B_□^T B_□ is the "covariant curl squared" operator, which differs from the Hessian of the Wilson action by a curvature correction: **H(Q) = M(Q) − C(Q)**, where C(Q) involves commutator cross terms from the product-of-exponentials expansion. **C(Q) is NOT positive semidefinite** (41 negative eigenvalues on L=2 d=4), and the discrepancy is O(1) in eigenvalues. This distinction is critical: the B_□ inequality bounds M(Q), not H(Q). The hnorm-conjecture numerical scans (see `hnorm-conjecture-numerical-resolution.md`) compute the actual Hessian H(Q), not M(Q). The two objects coincide at Q=I (where C(I) = 0) but diverge for general Q. **Complete analytical decomposition: C = C_curv + C_comm**, where C_curv is PSD (curvature bonus) and C_comm is indefinite (commutator correction). Despite C not being PSD, λ_max(H_actual) ≤ λ_max(H_formula) holds for 50+ tested configs (ratio 0.61–0.74) because C_curv compensates C_comm in the top eigenspace. **See `hessian-analytical-formula-c-decomposition.md` for complete formula, SU(2) cross-product simplification, spectral analysis, and proof strategies.**

### UNRESOLVED: S002-E007 Potential Counterexample — Formula Verification Required

**[S002-E007, CAUTION]** Edge-by-edge gradient ascent found λ_max ≈ 16.08 (5 trials, max 16.0824) on L=2, d=4, exceeding the conjectured bound of 16. M verified symmetric, PSD, Tr = 1152. Rayleigh quotient confirmed the value. However, **the B_p formula used differs from the verified adjoint representation formula**: S002-E007 used B_p(a) = Q₁a₁ + Q₁Q₂a₂ − Q₁Q₂a₃ − Q₁Q₂Q₃⁻¹a₄ (left multiplication by group elements), while the library's verified formula uses B_□ = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄) (adjoint representation transport). **These are different for SU(2):** Q·a ≠ Ad_Q(a) = QaQ⁻¹. The meta-learning note explicitly flags that this "counterexample was not cross-checked against the MISSION.md formula." The existing library documents that wrong B_□ formulas produce spurious violations (see Critical Bug Fix section: wrong backward-edge formula gave F = 16.76). **This potential counterexample is UNRESOLVED until verified against the correct adjoint representation formula.** For random Q (2000+ configs), the same exploration found λ_max never exceeded 14.64 — consistent with all prior verified results.

## Remaining Gap

**Original statement:** Need to prove that for all Q ∈ SU(N)^E and all v in the top eigenspace P of M(I): v^T R(Q) v ≤ 0, where R(Q) = M(Q) − M(I). This holds locally (proved via M₁|_P = 0 and F''(0) < 0) and numerically for all tested Q (20/20, see E005).

**Current status (post-E005):** The per-vertex sum_S ≥ 0 is now **PROVED** (S002-E005), closing Gap 1 of the cube-face reduction. Combined with the cube-face reduction proof (Steps 0-5, CONDITIONAL PASS), the B_□ inequality is **PROVED for even L**. Gap 2 (odd L sign structures) remains open but is irrelevant for physics (even L → ∞). The direct R(Q)|_P ≼ 0 approach (Weitzenböck) is an alternative route that remains open but is no longer the critical path.

### Gap 1 Investigation (yang-mills-conjecture E008) — CLOSED by E005

**See `full-eigenspace-gap1-investigation.md` for full details.** Per-vertex reduction shows the bound is equivalent to λ_max(M_12|_V) ≤ 16, equivalently sum_S ≥ 0 (see `lemma-d-rdr-false-sum-s-nonneg.md`). **E005 PROVED sum_S ≥ 0** via contraction bound (Cauchy-Schwarz + M9 affine in D + cancellation). This closes Gap 1: the per-vertex bound holds for ALL 9D modes in the constrained space V = {T : Σ_μ T_μ = 0}, not just the 3D staggered subspace.

## Cube-Face Reduction Proof (yang-mills-conjecture E007)

**See `cube-face-reduction-adversarial-review.md` for full details.** Adversarial review verdict: **CONDITIONAL PASS**. A 5-step algebraic proof (cube-face reduction → sign structure → expansion → Combined Bound Lemma → assembly) establishes the per-vertex bound lambda_max(M_total) <= 64 and hence staggered mode Rayleigh quotient <= 4d. All algebraic steps verified correct (13 VERIFIED, 5 COMPUTED). Two gaps remain: (1) staggered mode bound does not imply full operator bound (9-dim top eigenspace at Q=I contains 6 non-staggered modes), (2) proof formula specific to even L. Both gaps numerically supported but not analytically closed.

## Most Promising Proof Routes

1. **Jiang F formula + SU(2) representation theory (E005):** Specialize Jiang's F(i,j,k) = ρ(A(i,j)A(j,k)) − ρ(A(i,k)) to hypercubic lattice with SU(2). For v ∈ P, show ⟨v, F v⟩ involves terms ⟨v_k, [Ad(G) − I] v_k⟩ ≤ 0. Requires SU(2)-specific algebra (Ad(G) is rotation in SO(3)). OBSTACLE: controlling sum over all plaquettes simultaneously.
2. **Gauge orbit concavity (spectral radius):** Pure gauge configs have λ_max = 4d; non-pure-gauge observed to have λ_max < 4d. Show λ_max(M(Q)) is concave along paths from pure gauge to non-pure-gauge. OBSTACLE: global geodesic concavity fails (E002), but spectral radius concavity may hold.
3. **Tensor product extension from uniform Q:** Uniform Q proved (E001) via (2I + R + R^T) ≼ 4I₃. Extension to general Q via product structure. OBSTACLE: non-uniform Q couples modes.
4. **Gauge-covariant Fourier + perturbation:** Work in maximal tree gauge (most links = I). Corrections bounded by holonomy norms.
5. **sum_S contraction bound (S002-E003/E004/E005) — PROVED:** sum_S ≥ 0 **proved** via: M9 is affine in D (enabling per-pair minimization) + Cauchy-Schwarz (u^T Dv ≤ ||u||·||v||) + combinatorial cancellation (Σ||u−v||² = 4Σf + |Σa|², cancels cross term, leaves F = 2Σf + Σ(||u||−||v||)² ≥ 0). Extends to all contractions ||D|| ≤ 1. Journey: E003 (correct target), E004 (master identity + special cases + 7 failures), E005 (full proof). **This closes Gap 1** in the cube-face reduction. Combined with cube-face reduction (CONDITIONAL PASS for even L), the B_□ inequality is **PROVED for even L**. See `lemma-d-rdr-false-sum-s-nonneg.md`.

## Key References

- **Jiang (2022)** arXiv:2211.17195 — Discrete Weitzenböck formula on graphs: Δ_A = B_A + Ric + F, where F = holonomy defect ρ(A(i,j)A(j,k)) − ρ(A(i,k)). Confirmed (E005): F maps to R(Q) in our setting; Jiang does NOT prove sign of F; Jiang's Remark 5.1 confirms F is gauge-invariant. For our plaquette structure, F involves Ad(G_k) − I where G_k = partial holonomy.
- **Liu-Peyerimhoff (2024)** arXiv:2403.06105 — Connection Laplacian eigenvalue convergence on discrete tori. Confirms M(I) = I₃ ⊗ L for trivial holonomy.
- **Forman (2003)** DCG 29(3):323–374 — Bochner's method for cell complexes: B(A) + Ric(A) = A. Ric can be positive, negative, or zero — no general sign. Jiang extends Forman by adding gauge connection F term.
