---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-005-ns-beta-functions-six-derivative (strategy-002), exploration-004-ns-tension-analysis (strategy-002)
---

# n_s Tension Resolution Paths for QG+F

## The Problem

QG+F predicts Starobinsky inflation via its R² term, giving n_s ≈ 0.967 for N = 60 e-folds. CMB + DESI data suggest n_s ≈ 0.974 ± 0.003 — a 2.3σ tension. The fakeon (C² term) **does not help**: it primarily modifies the tensor-to-scalar ratio r, not the scalar spectral index n_s. The scalar sector is determined by R², and QG+F has no free parameter to tune n_s independently of N★.

This is actually a **virtue** — QG+F makes a sharp, falsifiable prediction. But if n_s = 0.974 is confirmed, the theory requires modification.

## Path 1: RG Running of R² Coupling — RULED OUT

**Status: DEFINITIVELY INSUFFICIENT (Δn_s ~ 10⁻¹⁴)**

This was previously ranked as the most natural path and "the critical next calculation." That calculation has now been done (exploration-005). The result: **the RG running of the R² coupling is 12 orders of magnitude too small to resolve the n_s tension.**

### The Calculation

The R² coefficient θ = 1/(6f₀²) ≈ 1.8 × 10⁸ runs under the physical beta functions (see `physical-beta-functions.md`). For |ξ| >> |λ| (always true in QG+F):

    β_θ = (1/ξ²) × β_ξ ≈ −1/(576π²) ≈ −1.76 × 10⁻⁴ per unit of ln μ

During the observable part of inflation (7 e-folds, N ≈ 60 to N ≈ 53), the curvature scale changes by only Δ(ln μ) ~ O(10⁻²) because the Starobinsky potential is extremely flat on the plateau.

    Δθ/θ ≈ (−1.76 × 10⁻⁴) × O(10⁻²) / (1.8 × 10⁸) ≈ −10⁻¹⁴

**This is 12 orders of magnitude smaller than the needed Δn_s ~ 10⁻².**

### Why the Running Is So Tiny (Two Independent Reasons)

1. **The coupling θ ~ 10⁸ is enormous.** One-loop corrections scale as 1/(16π²) ~ 10⁻², so the fractional change is 10⁻²/10⁸ = 10⁻¹⁰ per unit of ln μ.
2. **The energy scale barely changes during observable inflation.** The Starobinsky potential is extremely flat, so μ changes by O(1%) across the observable window.

These combine to give O(10⁻¹⁴). This is a **robust** conclusion: it holds regardless of which beta functions (FT or physical) are used — the suppression comes from the hierarchy between the coupling value and the loop factor, not the specific beta function form.

### Cross-Checks

- **Coleman-Weinberg effective potential**: One-loop correction from the spin-2 sector gives δV/V ~ f₂⁴/f₀². The field-dependent part introduces additional suppression (H/M₂)² ~ 10⁻¹⁰, giving δn_s ~ 10⁻¹⁸.
- **Anselmi's cosmic RG flow** (arXiv:2007.15023): Corrections to n_s are Δn_s ~ (1 − n_s)² × (H²/M₂²). For M₂ >> H: Δn_s << 10⁻³.
- **Radiative corrections literature** (arXiv:2510.15137): Self-corrections (inflaton loops) give ΔV/V ~ H²/M_P² ~ 10⁻¹⁰ with "no observable impact on n_s and r." Scalar coupling corrections "never push n_s into the ACT range."

### What Could Change This?

Only coupling to specific **external matter content** (Yukawa coupling y ~ 4−6 × 10⁻⁴) can shift n_s into the ACT range via radiative corrections — but that's model-dependent, not intrinsic to QG+F. Non-perturbative effects are uncalculable but would need 12 orders of magnitude enhancement.

## Path 2: R³ Curvature Correction — THE RESOLUTION ✓

**Status: WORKS. One new parameter δ₃ ≈ −10⁻⁴ resolves the tension.**

### Modified Action

    f(R) = ½(R + R²/(6m²) + δ₃ R³/(36m⁴))

With δ₃ = −1.19 × 10⁻⁴ (arXiv:2505.10305):

| Parameter | Pure Starobinsky | With R³ (δ₃ = −1.19×10⁻⁴) |
|-----------|-----------------|---------------------------|
| n_s | ≈ 0.967 (N=55) | **≈ 0.974** |
| r | ≈ 0.003 | **≈ 0.0045** |

### Mechanism

Negative δ₃ makes the potential plateau slightly flatter at large field values, reducing |ηᵥ| and increasing n_s. Modified slow-roll parameters (y ≡ e^{−√(2/3)φ/M_P} << 1):

    εᵥ ≃ (4/3)y² − (2/3)δ₃
    ηᵥ ≃ −(4/3)y − (1/3)δ₃ y⁻¹

### Naturalness of δ₃ ~ 10⁻⁴

- **EFT perspective**: δ₃ ~ (m/Λ)² where Λ ~ 100m ≈ 3×10¹⁵ GeV — near the GUT scale, a natural hierarchy.
- **Loop-generated in QG+F**: δ₃ ~ f₀²/(16π²) ~ 10⁻¹⁰ — 6 orders too small. **The R³ term must be tree-level**, not loop-generated.
- **Six-derivative theory**: δ₃ is a free parameter whose smallness reflects the hierarchy between the scalaron mass and the higher-derivative scale.

### Literature Confirmation

- arXiv:2511.06640: Pure Starobinsky at 2σ boundary; R³ "removes tension across both datasets"
- arXiv:2504.20757: Pure Starobinsky: n_s ∈ [0.967, 0.972], "a mild tension appears to be emerging"

### Tachyonic Instability Caveat

For δ₃ < 0, the R³ term eventually causes f'(R) < 0 at very large R → tachyonic instability. But this occurs at **trans-Planckian** curvatures irrelevant for inflation. The full six-derivative theory (with stabilizing terms) addresses this in the UV.

See `six-derivative-extension.md` for the full six-derivative theory that naturally includes R³.

## Path 3: Matter Radiative Corrections (Model-Dependent)

Coupling the scalaron to matter fields generates radiative corrections (arXiv:2506.18077, arXiv:2510.15137):
- **Yukawa coupling** (y ~ 4 × 10⁻⁴): Flattens potential, increasing n_s. Implies T_RH ~ 2 × 10¹¹ GeV.
- **Higgs portal** (λ_φH ~ 0.05-0.14): Raises both n_s and r to 0.970-0.975.

Can resolve the tension but requires specific coupling values. Does not modify the gravitational sector.

## Path 4: Very High e-folds (Fine-Tuned)

Refined formula (arXiv:2504.20757): n_s ≃ 1 − 2/(N★ − ¾ ln(2/N★)). Even N = 66 only gives n_s ~ 0.970. Cannot reach 0.974.

## Priority Ranking (Revised)

1. **Path 2 (R³ correction)** — Works, one parameter, naturally arises in the six-derivative extension of QG+F. The **definitive resolution** if n_s ≈ 0.974 is confirmed.
2. **Path 3 (matter coupling)** — Works but model-dependent, less theoretically motivated.
3. **Path 4 (high e-folds)** — Fine-tuned, insufficient even optimistically.
4. ~~**Path 1 (RG running)**~~ — **RULED OUT** (Δn_s ~ 10⁻¹⁴, 12 orders too small).

## Distinguishing Predictions

| Scenario | n_s | r | Testable? |
|----------|-----|---|-----------|
| Pure QG+F | 0.964-0.967 | 0.003-0.005 | n_s already in 2.3σ tension |
| QG+F + RG running | 0.964-0.967 (unchanged) | 0.003-0.005 | Indistinguishable from pure QG+F |
| Six-derivative QG+F (R³) | **0.974 ± 0.003** | **0.004-0.005** | Yes: n_s discriminates; r slightly enhanced |

The cleanest discriminator: if n_s ≈ 0.974, the R³ correction is needed. If n_s ≈ 0.967, pure QG+F suffices.

## What This Means for QG+F

The finding that RG running cannot resolve the tension is actually **positive** for the program:
1. **Predictions are robust** — quantum corrections don't spoil the leading-order result
2. **The theory is predictive** — you can trust n_s ≈ 1 − 2/N
3. **If n_s ≈ 0.974 is confirmed**, it points to the six-derivative extension as the natural next order
4. **Narrative**: QG+F is the leading-order theory; the six-derivative extension is the next order in the curvature expansion, needed for precision cosmology

Sources: arXiv:2403.02397 (physical beta functions), arXiv:2505.10305 (R³ corrections), arXiv:2509.23329 (marginally deformed Starobinsky), arXiv:2504.20757 (refined formula), arXiv:2005.10293 (Anselmi-Bianchi-Piva), arXiv:2007.15023 (Anselmi cosmic RG), arXiv:2510.15137 (radiative corrections), arXiv:2511.06640 (subtle tension), arXiv:2506.18077 (matter corrections)
