---
topic: Full 9D eigenspace bound (Gap 1) — per-vertex reduction, gap decomposition, numerical evidence, PROVED by E005
confidence: verified
date: 2026-03-29
source: "yang-mills-conjecture strategy exploration-008; yang-mills-conjecture strategy-002 exploration-005"
---

## Overview

Dedicated investigation of Gap 1 from the cube-face reduction adversarial review (see `cube-face-reduction-adversarial-review.md`): proving that λ_max(M(Q)) ≤ 16 for ALL directions in the 9-dimensional top eigenspace P of M(I), not just the 3D uniform-color staggered subspace. **E008 characterized the problem** (110K+ tests, 0 violations, gap decomposition). **S002-E005 PROVED the bound**: sum_S ≥ 0 via contraction bound (M9 affine in D + Cauchy-Schwarz + cancellation). See `lemma-d-rdr-false-sum-s-nonneg.md` for the full proof. Gap 1 is **CLOSED**.

## The 9D Eigenspace P

At Q = I, M(I) has eigenvalue 16 with multiplicity 9. The eigenspace P is spanned by:

  v^{(s,a)}_{x,μ} = (−1)^{|x|} s_μ e_a

where s ⊥ (1,1,1,1) in ℝ⁴ (3 spatial DOF) and e_a is a color basis vector in ℝ³ (3 color DOF). A general element w ∈ P has w_{x,μ} = (−1)^{|x|} T_μ where T = (T_0, T_1, T_2, T_3) is a 4×3 matrix with **constraint Σ_μ T_μ = 0** (a 3-vector equation giving 9 DOF).

## Per-Vertex Reduction [VERIFIED]

**Key reduction:** The bound v^T M(Q) v ≤ 16|v|² for v ∈ P is EQUIVALENT to the per-vertex bound:

  **F_x(T, Q_local) ≤ 16 ‖T‖_F²   for all T with Σ_μ T_μ = 0**

where F_x = Σ_{μ<ν} |(I + R_μ D_{μ,ν}) T_μ − (R_μ + R_μ D_{μ,ν} R_ν^T) T_ν|² is the per-vertex B-field squared, and ‖T‖_F² = Σ_μ |T_μ|².

This is a 12×12 eigenvalue problem: λ_max(M_12|_V) ≤ 16 where M_12 is the per-vertex Hessian restricted to the 9D constraint space V = {T : Σ_μ T_μ = 0}.

### M_12 at Q=I [VERIFIED]
- M_12(I) = 16 I_12 − 4 (J_4 ⊗ I_3) where J_4 is the 4×4 all-ones matrix
- Eigenvalues: {0 (mult. 3), 16 (mult. 9)}
- On V: all eigenvalues equal 16 (maximum, tight)
- On complement (1,1,1,1)⊗ℝ³: eigenvalue 0

## The Constraint Is ESSENTIAL [COMPUTED]

Unconstrained M_12 has max eigenvalue **~21** (up to 20.885 in random tests). The constraint Σ_μ T_μ = 0 is what forces λ_max ≤ 16. Any proof MUST use this constraint centrally.

## Numerical Evidence — Zero Violations

| Test type | N configs | Max λ_max (constrained) | Max λ_max (unconstrained) |
|-----------|-----------|------------------------|--------------------------|
| Random configs | 10,000 | **15.525** | 20.885 |
| Adversarial gradient ascent (100×300 iter) | 100 | **15.997** | 17.878 |
| Adversarial gradient ascent (200×1000 iter) | 200 | **15.769** | — |
| Uniform-color random | 50,000 | ratio 0.901 of 16 | — |
| Extreme-rotation configs | 10,000 | — (all below 16) | — |
| Direct F_x/‖T‖² bound | 5,000 | 12.46 | — |

**0 violations across 110K+ random + 350+ adversarial trials.** Best adversarial eigenvalue: 15.997 (Task 2C); 15.769 (Task 4D, longer optimization).

## Maximizer Is NOT Always Rank-1 [COMPUTED]

The constrained maximizer is **not always rank-1** (i.e., not always uniform-color). Rank-1 fraction at adversarial maxima ranges from 0.56 to 0.99 (mean 0.90). **Implication: Cannot reduce to the uniform-color case. Need full 9D proof.**

## Gap Decomposition: f_same + cross [VERIFIED]

### Budget Identity [PROVED]

**For T with Σ_μ T_μ = 0:  16 ‖T‖² = 4 Σ_{μ<ν} |T_μ − T_ν|²**

Proof: Σ_{μ<ν} |T_μ − T_ν|² = (d−1)‖T‖² − 2 Σ_{μ<ν} T_μ · T_ν = (d−1)‖T‖² + ‖T‖² = d‖T‖² = 4‖T‖² (using |Σ T_μ|² = 0). So 4 × 4‖T‖² = 16‖T‖². ∎

### Per-Plaquette Expansion Identity [VERIFIED]

4|T_μ − T_ν|² − |B_{μ,ν}|² = 2 f(U_{μ,ν}, T_μ) + 2 f(W_{μ,ν}, T_ν) − 2 T_μ^T C_{μ,ν} T_ν

where f(R, p) = p^T(I − R)p ≥ 0 for R ∈ SO(3), p ∈ ℝ³; U_{μ,ν} = R_μ D_{μ,ν}; W_{μ,ν} = D_{μ,ν} R_ν^T; C_{μ,ν} = (I−R_μ) + (I−R_ν^T) + (I−D_{μ,ν}^T) + (I−R_μ D_{μ,ν} R_ν^T). Verified to < 2e-13.

### Total Gap Structure [VERIFIED]

Summing over plaquettes: **gap = f_same + cross** where:
- **f_same = 2 Σ [f(U, T_μ) + f(W, T_ν)] ≥ 0** (always non-negative)
- **cross = −2 Σ T_μ^T C_{μ,ν} T_ν** (can be positive or negative)

### Cross Term Dominated by f_same [COMPUTED — KEY RESULT]

When cross is **negative** (hurts the gap): max |cross|/f_same = **0.082** (8.2%)
When cross is **positive** (helps the gap): up to 3.7× f_same

The cross is strongly **asymmetric** — it mostly helps. **Gap ≥ 0.918 × f_same ≥ 0** in all tested configurations.

At adversarial maxima: gap ranges from 2.2 to 6.4 (always positive); f_same > 0 always; cross typically small (|cross| < 2).

## Per-Plaquette Budget Fails [COMPUTED]

Max |B|² / (4|T_μ − T_ν|²) = **195.6** — individual plaquettes can vastly overspend their budget. About 5–21% of plaquettes exceed budget. ALL 6 plaquette types can have negative gap. **Cross-plaquette cancellation is needed** (same situation as E006 for staggered modes).

## Why Algebraic Proof Is Hard [CONJECTURED]

1. **Trace identity fails for general s**: Unlike E006 where Tr(M_total) = 64 independently of Q, for general s the trace varies by factor ~3
2. **Active/inactive classification depends on s**: The sign pattern s_μ s_ν determines which plaquettes are "hard"
3. **Base-link budget insufficient for some s patterns**: Balanced patterns like (1,1,−1,−1) share budget across multiple "hard" plaquettes
4. **Cross-color coupling**: For rank > 1 modes, B-field mixes color directions, introducing cross terms absent in uniform-color analysis
5. **Constraint is essential**: The unconstrained M_12 has eigenvalue up to ~21, so proof MUST use Σ_μ T_μ = 0

## Proof Strategy — RESOLVED by S002-E005

**E005 proved sum_S ≥ 0** via a completely different approach than the gap decomposition investigated here. Rather than bounding harmful cross < f_same, E005 discovered that M9 is affine in D (enabling per-pair independent minimization), then used Cauchy-Schwarz to get sum_S ≥ F = 2Σf + Σ(||u||−||v||)² ≥ 0. The proof is elementary but required the structural insight about affinity. See `lemma-d-rdr-false-sum-s-nonneg.md` for the full proof.

**Historical note:** The approaches investigated here (harmful cross < f_same, SDP/SOS, concavity, CBL extension) were all superseded by the E005 contraction bound. The gap decomposition framework remains valid and was instrumental in building intuition (especially the 8.2% ratio showing the bound has enormous margin).

## Verification Scorecard
- **VERIFIED:** 3 (budget identity with algebraic proof, per-plaquette expansion to 2e-13, M_12 at Q=I)
- **COMPUTED:** 8 (random tests, adversarial tests ×2, gap structure, uniform-color tests, extreme rotations, maximizer rank structure, cross-term ratio, trace identity failure)
- **CONJECTURED:** 2 (algebraic proof difficulty analysis, f_same domination bound)

## Relationship to Other Entries

- **`cube-face-reduction-adversarial-review.md`** — This investigation directly addresses Gap 1 identified there (staggered mode ≠ full operator bound)
- **`b-square-inequality-proof-progress.md`** — Part of the B_□ inequality proof program; adds the per-vertex reduction and gap decomposition framework
- **`weitzenbock-exact-formula.md`** — The Weitzenböck R(Q)|_P ≤ 0 approach is an alternative to the gap decomposition; both target the same bound from different angles
