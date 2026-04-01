---
topic: C1 random-phase von Mangoldt matrix — 10-constraint RMT scorecard
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-002 exploration-001 (initial), exploration-005 (corrected), exploration-007 (adversarial review), exploration-009 (C1 rigidity retraction)"
---

## Summary

The C1 construction (von Mangoldt Hankel matrix with random complex phases) was evaluated against the 10-point RMT constraint catalog for the hypothetical Riemann operator. **Corrected scorecard (S002-E005): 3 PASS, 4 PARTIAL, 2 NOT COMPUTED, 1 N/A.** The matrix demonstrates GUE-class statistics by spacing distribution and pair correlation, but exhibits anomalously strong spectral rigidity (Δ₃ ≈ 50% of GUE) and sub-quadratic level repulsion (β ≈ 1.18 from 5-realization average).

**Matrix:** H_{jk} = Λ(|j-k|+1) × e^{iφ_{jk}}, φ_{jk} i.i.d. Uniform[0, 2π]. N = 500, 5 independent matrices, ~2494 total spacings.

## Corrected Constraint Scorecard (S002-E005)

| # | Constraint | Score | Value |
|---|---|---|---|
| 1 | β level repulsion | **PARTIAL** | β_Wigner = 1.18 ± 0.22 (5-realization avg); target β=2 |
| 2 | Pair correlation vs Montgomery | **PASS** ✓ | MRD = 7.9% [COMPUTED, bug fixed] |
| 3 | NN spacing vs Wigner surmise | **PASS** ✓ | KS_GUE = 0.042 < 0.05; χ²_GUE = 7.98 [COMPUTED] |
| 4 | Spectral form factor | **PASS** | GUE best fit (from S002-E001, not re-run) |
| 5 | Quadratic level repulsion β ≈ 2 | **PARTIAL** | β = 1.18 from log-log slope (5-realization avg) |
| 6 | Number variance Σ²(L) | **PARTIAL** | Σ²(1)=0.39, Σ²(5)=0.60; suppressed vs Poisson but below GUE |
| 7 | Spectral rigidity Δ₃ | **PARTIAL** | Saturation ≈ 0.285, ~50% of GUE (L=25–50 avg) [COMPUTED, bug fixed] |
| 8 | Form factor plateau | **NOT COMPUTED** | Requires multi-matrix average |
| 9 | Higher-order correlations | **NOT COMPUTED** | Out of scope |
| 10 | Universality class | **N/A** | Complex Hermitian structure → GUE class by construction |

**Scorecard: 3 PASS, 4 PARTIAL, 2 NOT COMPUTED, 1 N/A**

*Improvement over S002-E001: Pair correlation upgraded NOT COMPUTED→PASS (normalization bug fixed); Δ₃ upgraded NOT COMPUTED→PARTIAL (integral formula bug fixed); β downgraded PASS→PARTIAL (single-realization 1.675 was outlier; 5-realization avg = 1.18).*

## Key Quantitative Details

### Pair Correlation R₂(r) [Corrected]

Method: Pairwise separations in unfolded spectrum, dr=0.05, normalized to R₂→1 for large r. Averaged over 5 realizations.

| r | R₂_computed | R₂_Montgomery |
|---|-------------|---------------|
| 0.5 | 0.512 | 0.554 |
| 1.0 | 1.104 | 0.999 |
| 1.5 | 0.968 | 0.954 |
| 2.0 | 0.840 | 1.000 |
| 3.0 | 1.128 | 1.000 |

**MRD [0.5, 4.0] = 7.9%** — well within GUE behavior. (Prior S002-E001 MRD = 0.996 was meaningless due to normalization bug.)

### Spectral Rigidity Δ₃(L) [Corrected]

Method: Dyson-Mehta integral (piecewise constant staircase, minimized over linear fit), averaged over 200 windows per L value.

| L | Δ₃(L) C1 | GUE prediction | Ratio C1/GUE |
|---|-----------|----------------|--------------|
| 15 | 0.221 | 0.495 | 0.45 |
| 30 | 0.274 | 0.566 | 0.48 |
| 50 | 0.313 | 0.617 | 0.51 |

**Saturation (L=25–50 avg): 0.285** — approximately 50% of GUE Δ₃, but significantly ABOVE the actual zeta zeros' value of 0.156 ± 0.005. C1 is anomalously rigid relative to GUE (from the von Mangoldt Hankel structure) but NOT as rigid as the actual Riemann zeros.

### Level Repulsion β

- **S002-E005 (5 fresh realizations):** β_Wigner = 1.182 ± 0.219 — **PARTIAL** (target: 2.0)
- **S002-E001 (original run, likely single realization effectively):** β_Wigner = 1.675 ± 0.085
- **Explanation:** Large realization-to-realization variability; the KS-based fit (KS_GUE = 0.042 < 0.05) is more reliable than the log-log β estimate. C1 is GUE-class by KS criterion but sub-quadratic by β estimate.

## Interpretation

C1 is clearly GUE-class by the discrete KS test on spacing distributions (KS=0.042, passes) and pair correlation (MRD=7.9%), but shows:

1. **Anomalous rigidity:** Δ₃ ≈ 50% of GUE prediction — the von Mangoldt amplitude profile forces extra long-range spectral order beyond GUE. This is LESS rigid than the actual Riemann zeros (0.156), so C1 is intermediate between GUE and the actual spectrum.

2. **Sub-quadratic level repulsion:** β ≈ 1.18 (5-realization avg) indicates the phase structure doesn't fully reproduce the quadratic repulsion of GUE. The von Mangoldt envelope likely softens the local repulsion.

3. **Number variance suppressed:** Σ²(L) ≈ 0.39–0.60 is systematically below GUE theory (~0.88 for GUE), reflecting the same extra-rigidity effect.

**Bottom line:** C1 passes 3 of 4 testable short-range statistics (pair correlation, spacing KS, form factor) but fails the key long-range and level-repulsion targets. The random-phase construction reaches toward GUE but remains intermediate between GOE and true GUE.

## Adversarial Review of Pair Correlation Claim (S002-E007)

A dedicated adversarial exploration (S002-E007) attacked the "PASS" verdict on pair correlation (constraint #2). Three independent tests were run: null matrix comparison, realization stability over 20 realizations, and a severity table.

### Null Matrix Comparison

| Matrix | MRD (5 realizations pooled) | β_Wigner | Passes ≤10% threshold |
|---|---|---|---|
| C1 (Von Mangoldt Hankel + random phases) | 7.9% | 1.18 ± 0.22 | YES |
| GUE control (random complex Gaussian) | 7.8% | 1.50 | YES |
| Flat-amplitude random phase | 6.8% | 1.45 | YES (better than C1) |
| Flat-amplitude Toeplitz (random per-lag phase) | 9.0% | 0.45 | YES (barely; GOE class) |

**Verdict:** Pair correlation ≤10% MRD is a generic property of GUE-class matrices, not specific to C1's arithmetic construction. The Von Mangoldt amplitude is NOT necessary — flat amplitudes achieve equal or better MRD.

### Realization Stability (20 C1 Realizations)

- Mean MRD across 20 individual N=500 matrices: **15.5% ± 1.9%**
- Range: 12.1%–19.1%. **Pass rate: 0/20.**
- The "7.9%" from S002-E005 was computed by averaging 5 R₂(r) curves together before computing MRD — a noise-reduction technique that artificially lowers MRD by ~√5. Per-realization MRD is ~15.5%.
- With all 20 realizations pooled (10,000 eigenvalues), MRD = 3.7% — but this is from sample size, not arithmetic structure.

### Revised Assessment of Constraint #2

The pair correlation "PASS" (7.9% MRD) is conditional on 5-realization averaging:
- **PASS in a qualified sense:** The C1 construction is GUE-class; when averaged over 5+ realizations it achieves ≤10% MRD. This is a real and true statement.
- **NOT ESTABLISHED as arithmetic-specific:** Any GUE-class Hermitian matrix (including pure random GUE) achieves the same or better score. The Von Mangoldt amplitude contributes nothing.
- **NOT ESTABLISHED as per-realization:** Individual C1 matrices at N=500 fail 100% of the time.

**The 10% MRD criterion at N=500 with 5-realization averaging cannot discriminate GUE from GOE** — a GOE-class Toeplitz matrix (β=0.45) also passes at 9.0%.

### Severity Assessment (Adversarial)

| Attack | Severity | Verdict |
|---|---|---|
| Von Mangoldt amplitude unnecessary | SERIOUS | ESTABLISHED |
| 7.9% MRD not stable per-realization (mean 15.5%, 0/20 pass) | SERIOUS | ESTABLISHED |
| Test cannot distinguish GOE from GUE at this N/sample size | SERIOUS | ESTABLISHED |
| GUE class ≠ Riemann-like (β=1.18 vs 2.0, Δ₃=0.285 vs 0.156) | MODERATE | ESTABLISHED |
| Random phases drive GUE class, not arithmetic structure | SERIOUS | ESTABLISHED |

### Restated Claim (Honest Version)

**Original:** "C1 satisfies Montgomery's pair correlation formula at 7.9% MRD."
**Restated:** "C1 is GUE-class. When pair correlation is averaged over 5+ realizations (~2500+ eigenvalues), it satisfies Montgomery's formula at ~8–10% MRD. This is generic to any GUE-class Hermitian matrix and does not require the Von Mangoldt amplitude."

**Status: SUPPORTED (not ESTABLISHED).** The claim is true but not novel; any GUE-class matrix makes it true. *Confirmed: S002-E007.*

---

## E009 Update: C1 Rigidity Claim Retracted (S002-E009)

A flat-amplitude control experiment (E009) directly tested whether Von Mangoldt amplitude structure is responsible for C1's intermediate Δ₃. Result: **it is not.** The C1 anomalous rigidity claim is retracted.

### E009 Comparison Table

| Ensemble | Δ₃_sat | ±std |
|---|---|---|
| H_flat (flat amplitude, random phases) | 0.256 | ±0.010 |
| C1 (Von Mangoldt + random phases) | **0.243** | ±0.017 |
| GUE_control | 0.227 | ±0.010 |
| Riemann zeta zeros | 0.155 | — |

H_flat vs. C1 difference = 0.013, combined uncertainty = 0.020. **< 1σ — not distinguishable.**

### Constraint #7 (Spectral Rigidity Δ₃) — Revised

**Corrected status: NOT MEANINGFUL as a discriminating test.**

The prior Δ₃_sat = 0.285 (E005) and the "50% of GUE" interpretation were compared against the **infinite-N GUE theory** value (~0.566). The correct comparison at finite N=500 uses the **finite-size GUE value** (~0.22–0.26). Against the correct baseline, C1's Δ₃_sat = 0.243 is entirely generic GUE-class behavior.

The "anomalous rigidity" observation was an artifact of using the wrong GUE reference (infinite-N theory instead of finite-size simulation). The Von Mangoldt amplitude plays no role in the spectral rigidity at N=500.

The prior Δ₃_sat = 0.285 (E005) is within 2.5σ of the E009 corrected C1 value (0.243 ± 0.017) — consistent with sampling variation across independent realization sets.

### Updated Summary (post-E009)

**Revised scorecard: 3 PASS, 3 PARTIAL, 2 NOT COMPUTED, 1 N/A, 1 NOT MEANINGFUL**

Constraint #7 (spectral rigidity) is reclassified as NOT MEANINGFUL: C1's Δ₃_sat is indistinguishable from H_flat and GUE_control at N=500. The key gap (zeta zeros at 0.155 vs. all N=500 ensembles at 0.23–0.26) is a finite-size GUE property, not a C1-specific feature.

---

## Prior S002-E001 Scorecard (for reference)

The original S002-E001 scorecard (4 PASS, 2 PARTIAL, 2 NOT COMPUTED, 2 N/A) had bugs in constraints 2 and 7. The "4 PASS" result was therefore overstated; pair correlation and Δ₃ were not computed correctly. The S002-E005 corrected scorecard supersedes the E001 numbers.
