---
topic: sum_S proof program — individual lemmas FALSE, sum_S ≥ 0 PROVED via contraction bound (E005)
confidence: verified
date: 2026-03-29
source: "yang-mills-conjecture strategy-002 explorations 003, 004, 005"
---

## Overview

The individual per-component lemmas LEMMA_D (≥ 0) and LEMMA_RDR (≥ 0) are both **FALSE**, disproved by adversarial optimization (E003). However, their sum **sum_S = LEMMA_D + LEMMA_RDR ≥ 0** holds — and is now **PROVED** (E005). The proof is elementary (Cauchy-Schwarz + norm identities + combinatorial cancellation) but required a structural discovery: M9 is affine in D, enabling per-pair independent minimization. **This closes Gap 1 in the cube-face reduction proof** (see `cube-face-reduction-adversarial-review.md`, `full-eigenspace-gap1-investigation.md`). The proof extends to all contractions ||D|| ≤ 1, not just SO(3). Journey: E003 identified correct target → E004 proved special cases + established master identity → E005 proved the full result.

## Counterexamples to Individual Lemmas (E003)

**LEMMA_D is FALSE [VERIFIED]:** Min eigenvalue of the constrained 9×9 quadratic form = **-2.13**. Verification: (a) matrix formula and direct computation agree to 5.7e-14, (b) all R, D confirmed as SO(3) to machine precision, (c) T satisfies sum = 0 constraint, (d) 20 independent optimizations all converge to ≈ -2.13.

**LEMMA_RDR is FALSE [VERIFIED]:** Min eigenvalue = **-1.45**.

**Counterexample structure:** D₀₁, D₀₂, D₁₂ at ~128° while D₀₃, D₁₃, D₂₃ near identity. Per-plaquette budget ≈ 0.05 vs cross ≈ 1.16 for the "active" plaquettes.

**Why 200K random tests missed this:** Random uniform sampling on SO(3)^10 almost never hits the specific adversarial corner (30D parameter space). Adversarial optimization is essential for high-dimensional verification.

## D=I Base Case [VERIFIED + PROVED] (E004)

**CORRECTION of E003:** E003 claimed "sum_S(D=I) = 0 for all R, T." This is **FALSE**. Correct statement: sum_S(D=I) ≥ 0 with min eigenvalue = 0 (tight, multiplicity always 1).

### Identity [VERIFIED to 1.1e-13, 500 trials]

**sum_S(R, D=I, T) = 6·Σ_μ f(R_μ, T_μ) + |Σ_μ R_μ^T T_μ|²**

where f(R, p) = p^T(I − R)p ≥ 0 for R ∈ SO(3).

### Proof [VERIFIED]

At D=I: S_{μ,ν} = 2f(R_μ, T_μ) + 2f(R_ν, T_ν) − 2T_μ^T(I − R_μ R_ν^T)T_ν. **Diagonal terms:** Each μ in 3 pairs → sum = 6·Σ f(R_μ, T_μ). **Cross terms:** Using Σ T = 0, Σ_{μ<ν} T_μ·T_ν = −||T||²/2, and T_μ^T R_μ R_ν^T T_ν = (R_μ^T T_μ)·(R_ν^T T_ν), the cross sum = |Σ R_μ^T T_μ|². Both terms ≥ 0. **QED.** □

**Null space:** T_μ = c_μ·axis(R_μ) with Σ c_μ·axis(R_μ) = 0. Zero eigenvalue multiplicity = 1 (500/500 configs).

## Delta_S Factoring [VERIFIED to 7.1e-14] (E004)

**Δ S_{μ,ν} := S_{μ,ν}(D) − S_{μ,ν}(I) = 2·u_{μ,ν}^T · (I−D) · v_{μ,ν}**

where u_{μ,ν} = R_μ^T T_μ − T_ν, v_{μ,ν} = T_μ − R_ν^T T_ν.

### Master Identity [VERIFIED]

**sum_S(R, D, T) = [6·Σ f(R_μ, T_μ) + |Σ R^T T|²] + Σ_{μ<ν} 2·u^T · (I−D) · v**

= (baseline ≥ 0) + (Delta term, signed). This decomposition separates the problem: baseline is proved ≥ 0, and the Delta term is bilinear in (u, v).

## Critical T Theorem [VERIFIED + PROVED] (E004)

**Theorem:** For T on rotation axes (T_μ = c_μ·n_μ where n_μ = axis(R_μ), Σ c_μ n_μ = 0): **sum_S(R, D, T) ≥ 0 for ALL D ∈ SO(3)^6.**

**Proof:** For T on axes, R_μ^T T_μ = c_μ n_μ (since R_μ n_μ = n_μ). Therefore **u_{μ,ν} = v_{μ,ν} = c_μ n_μ − c_ν n_ν**. Each Delta term becomes 2·u^T(I−D)u = 2f(D, u) ≥ 0. So Σ ΔS ≥ 0, and sum_S(D) = sum_S(I) + Σ ΔS = (≥0) + (≥0) ≥ 0. **QED.** □

**Significance:** This proves sum_S ≥ 0 for the **MOST DANGEROUS T direction** — the null eigenvector of the 9×9 matrix at D=I. The "hardest" case (where baseline = 0) is exactly where u = v makes the bilinear Delta term become a quadratic form, which is trivially ≥ 0.

**Numerical confirmation:** max ||u−v|| = 1.2e-15 on axes (confirms u = v); min Σ ΔS = 0.87 > 0 over 500 configs; z^T ΔM9 z ≥ 2.95 over 1000 configs; 2×2 submatrix (z, w₂) of M9(D): min det = 12.3 > 0.

## Adversarial Verification of sum_S ≥ 0 (E003 + E004)

**[COMPUTED]** Combined evidence from E003 (200 Nelder-Mead) and E004 (50K random + gradient descent + targeted):
- **67K+ adversarial + random tests: min eigenvalue = 3.9e-13 ≈ 0** (tight at zero)
- Minimizer has D near I (||D−I|| ~ 0.1–0.25)
- Same R at D=I: min eigenvalue = 0 (as expected)
- **Every perturbation from D=I INCREASES min eigenvalue**
- All 5000 random + 2000 targeted + 10000 random: zero negative eigenvalues

**Zero-set structure [COMPUTED]:** sum_S = 0 iff D = I (for any R). The zero eigenvalue is R-independent. Even a single D = I suffices for a zero eigenvalue. The zero set is rich: every optimization (100/100 trials) converges to sum_S = 0, with diverse D-angle patterns.

**At the LEMMA_D counterexample**, sum_S = 1.28 — LEMMA_RDR compensates. Correlation between LEMMA_D and LEMMA_RDR min eigenvalues: 0.39.

## Approaches That Failed for Full Proof (E004)

| Approach | Result | Why it fails |
|----------|--------|--------------|
| Convexity in D | FAILS | Hessian negative at D=I and elsewhere |
| B9 ≥ C9 (budget ≥ cross as matrices) | FAILS | Generalized eigenvalue ratio = 2.36 |
| VCBL(−I) per-plaquette | FAILS | Remainder can reach −151 |
| Per-plaquette VCBL (any M) | IMPOSSIBLE | I−U rank 2, cross term outside range⊗range |
| Eigenvalue perturbation | FAILS | ||Δ||/λ₂ up to 12536 |
| Gershgorin block bound | FAILS | Always negative (too loose) |
| M12 PSD directly | FAILS | M12 has 2 negative eigs (need V restriction) |

**VCBL at R = I [VERIFIED]:** sum_S = 2·Σ VCBL(D,D,−I,...) ≥ 0 by Cauchy-Schwarz + AM-GM. At general R: VCBL remainder = −32 (far from PSD). Fundamental obstruction: per-plaquette cross is rank 3, VCBL product rank ≤ 2.

## Other Structural Properties (E003)

- **Random verification:** Per-plaquette bound fails (18,993/240K violations). Simple Cauchy-Schwarz insufficient (398/5000 failures).
- **Eigenvalue/matrix structure:** min_eig(sum_S) scales as O(ε²) near Q = I (coefficient ≈ 2.96). Positive Hessian at Q = I.
- **Budget/cross ratio:** max |harmful cross|/budget ≈ 0.28 for random Q,T (substantial margin).
- **Remaining structure (E004):** M12 NOT PSD (2 negative eigs), off-diagonal symmetric part of cross blocks always NSD, budget B9 min eigenvalue 0.63 (always PD), cross/budget scalar ratio bounded at 0.29.

## Approaches That Failed for Full Proof — Additional (E005)

| Approach | Result | Why it fails |
|----------|--------|--------------|
| Polarization identity | FAILS | u^T(I-D)v = symmetric part only; antisymmetric missing. 37% of trials negative. |
| C-S + spectral bound | FAILS | Even worse — 65% negative |
| Any per-pair independent bounding via polarization | IMPOSSIBLE | Correction/baseline ratio > 10 |

## M9 is Affine in D [VERIFIED to 3.5e-15] (E005)

**Key structural discovery:** M9(R, D) is an **affine function of D**. Since M9 is linear in D, and each D_{μ,ν} enters only its own pair's contribution, we can **minimize over each D independently**. The minimum of u^T(I−D)v over D ∈ SO(3) has a closed form via Cauchy-Schwarz.

Additional structural findings (E005):
- Opposite-face pairings not PSD (all negative)
- Vertex stars not PSD
- VCBL remainder deeply negative (−19.9)
- M9 rank is always 9 (full rank for D ≠ I)

## FULL PROOF of sum_S ≥ 0 [PROVED] (E005)

### Theorem
**sum_S(R, D, T) ≥ 0** for all R_μ ∈ SO(3)^4, D_{μ,ν} ∈ SO(3)^6, T ∈ V = {T : Σ T_μ = 0}.

### Proof

**Step 1** (Master Identity, E004 [VERIFIED to 7.1e-14]):
sum_S = baseline + Σ_{μ<ν} 2·u_{μ,ν}^T·(I − D_{μ,ν})·v_{μ,ν}
where baseline = 6·Σ f(R_μ, T_μ) + |Σ R_μ^T T_μ|² ≥ 0, u = R_μ^T T_μ − T_ν, v = T_μ − R_ν^T T_ν.

**Step 2** (Per-pair Cauchy-Schwarz [PROVED]):
For D ∈ SO(3): u^T D v ≤ ||u||·||v|| (Cauchy-Schwarz + orthogonality).
Therefore: u^T(I−D)v = u·v − u^T D v ≥ u·v − ||u||·||v||.

**Step 3** (Independent minimization [PROVED]):
Since D_{μ,ν} are independent (M9 affine in D), apply Step 2 to each pair:
sum_S ≥ F(R,T) := baseline − 2·Σ_{μ<ν}(||u||·||v|| − u·v)

**Step 4** (Algebraic identity [VERIFIED to 1.1e-14]):
2(||u||·||v|| − u·v) = ||u−v||² − (||u|| − ||v||)²

**Step 5** (Key computation [VERIFIED to 1.1e-13]):
Define w_μ = (I − R_μ^T)T_μ. Then: u − v = −(w_μ + w_ν), ||w_μ||² = 2·f(R_μ, T_μ), Σ w_μ = −Σ R_μ^T T_μ.
Therefore: Σ_{μ<ν} ||u−v||² = 4·Σf + |Σ R^T T|²

**Step 6** (Cancellation [PROVED]):
F = (6·Σf + |Σa|²) − (4·Σf + |Σa|²) + Σ(||u|| − ||v||)²
  = **2·Σ f(R_μ, T_μ) + Σ_{μ<ν}(||u_{μ,ν}|| − ||v_{μ,ν}||)² ≥ 0**

Both terms manifestly non-negative: f(R,T) ≥ 0 for R ∈ SO(3), and (·)² ≥ 0.
**∴ sum_S ≥ F ≥ 0.** □

### Tightness
F = 0 iff f(R_μ, T_μ) = 0 for all μ AND ||u|| = ||v|| for all pairs. On rotation axes: u = v (E004 Critical T Theorem), so ||u|| = ||v||. Matches the null space of M9(D=I): T_μ = c_μ·axis(R_μ) with Σ c_μ·axis(R_μ) = 0.

### Extension to All Contractions [VERIFIED: 0/2000 violations]
The proof actually shows sum_S ≥ 0 for **all contractions** ||D_{μ,ν}|| ≤ 1, not just SO(3). The SO(3) constraint enters only through ||Dv|| = ||v||; for contractions ||Dv|| ≤ ||v||, giving u^T Dv ≤ ||u||·||v||. Verified over 2000 random contraction matrices.

## E005 Verification Scorecard

| Step | Claim | Status | Evidence |
|------|-------|--------|----------|
| 1 | Master identity | [VERIFIED] | E004, 500 trials, err < 7.1e-14 |
| 2 | u^T Dv ≤ \|\|u\|\|·\|\|v\|\| | [PROVED] | Cauchy-Schwarz + orthogonality |
| 3 | Per-pair independence | [PROVED] | M9 affine in D (verified 3.5e-15) |
| 4 | Algebraic identity | [VERIFIED] | 1000 trials, err < 1.1e-14 |
| 5 | Σ\|\|u-v\|\|² = 4Σf + \|Σa\|² | [VERIFIED] | 2000 trials, err < 1.1e-13 |
| 6 | F = 2Σf + Σ(·)² | [VERIFIED] | 2000 trials, err < 1.4e-13 |
| — | F ≥ 0 | [VERIFIED] | 10K random + adversarial, min ≈ 0 |
| — | sum_S ≥ F | [VERIFIED] | 5000 trials, min gap = 6.1 |
| — | Full chain sum_S ≥ 0 | [VERIFIED] | 25K random + adversarial, 0 violations |

## Key Insights (E005)

1. **M9 affine in D** enables per-pair independent minimization — the structural discovery that unlocked the proof.
2. **Cauchy-Schwarz suffices** — no need for spectral bounds; the simple u^T Dv ≤ ||u||·||v|| is enough.
3. **Beautiful cancellation**: Σ||u-v||² = 4Σf + |Σa|² exactly cancels the |Σa|² cross term in the baseline, leaving 2Σf as the margin.
4. **The hardest case is easy**: At the null eigenvector (T on axes), u = v so the correction vanishes. The proof difficulty is entirely off-axis, where the baseline provides the margin.

## Proof Status (Updated E005) — COMPLETE

1. **D=I base case: PROVED** (E004). sum_S(D=I) = 6Σf + |ΣR^T T|² ≥ 0.
2. **Critical T (null direction): PROVED** (E004). u = v on rotation axes makes bilinear → quadratic.
3. **R=I: PROVED via VCBL** (E004). sum_S = 2·Σ VCBL ≥ 0.
4. **FULL PROOF: PROVED** (E005). Contraction bound via Cauchy-Schwarz + cancellation.
5. **Extension: PROVED** for all contractions ||D|| ≤ 1.
6. **Historical note:** 7 approaches failed (E004) before the affine structure was discovered. Proof cannot be per-plaquette, perturbative, or matrix-domination-based.
