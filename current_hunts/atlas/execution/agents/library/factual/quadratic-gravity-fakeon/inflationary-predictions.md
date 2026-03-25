---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-003-quadratic-gravity-fakeon-validation
---

# Inflationary Predictions: Tensor-to-Scalar Ratio and CMB Tests

## Mechanism

The R² term in the quadratic gravity action naturally generates **Starobinsky inflation**. The scalar mode (mass M₀) plays the role of the inflaton. The addition of the C² term with the fakeon prescription modifies the predictions compared to pure Starobinsky.

## Tensor-to-Scalar Ratio

The key quantitative prediction of the theory:

    4/3 < N² r < 12

where N is the number of e-foldings (standard range N = 50-60).

| Scenario | r range |
|----------|---------|
| Standard Starobinsky (no fakeon) | r = 12/N² ≈ 0.003-0.005 |
| With fakeon (lower bound) | r > 4/(3N²) ≈ 0.0004-0.0005 |
| With fakeon (upper bound) | r < 12/N² ≈ 0.003-0.005 |
| **Combined prediction** | **0.0004 ≲ r ≲ 0.0035** |

The fakeon widens the prediction range compared to pure Starobinsky — the lower bound drops by nearly an order of magnitude.

Source: Anselmi (2020), JHEP 07, 211; Anselmi (2022), Symmetry 14(3), 521

## Scalar Spectral Index (n_s) — The Emerging Tension

### QG+F Prediction

The scalar spectral index is determined by the **R² term alone**, not the C² (fakeon) term. The prediction is essentially the Starobinsky value:

- Standard approximation: n_s ≃ 1 − 2/N
- Refined formula (arXiv: 2504.20757): n_s ≃ 1 − 2/(N★ − ¾ ln(2/N★))
- For N = 60: n_s ≈ 0.9667
- For N = 55: n_s ≈ 0.9636

**The fakeon (C² term) does NOT significantly shift n_s.** From Anselmi, Bianchi & Piva (JHEP 2020, arXiv: 2005.10293): the fakeon primarily modifies the **tensor** sector (r), not the scalar sector (n_s). The C² fakeon affects tensor perturbations and their ratio to scalars, but the scalar power spectrum is dominated by the R² inflaton dynamics. The fakeon decoupling limit is singular (cannot simply take m_χ → ∞), but the scalar spectral index remains close to the Starobinsky prediction.

### Current Status

- CMB alone (combined SPA): n_s = 0.9693 ± 0.0029 — barely 1σ above QG+F prediction
- CMB + DESI BAO: n_s = 0.9737 ± 0.0025 — 2.3σ above QG+F prediction
- See `cross-cutting/cmb-spectral-index-tension.md` for full observational picture

**QG+F's parameter space CANNOT accommodate n_s ≈ 0.974 without modification**: f₀ is fixed by the amplitude A_s, f₂ affects r but not n_s, and n_s is essentially fixed at the Starobinsky value for given N★. This is a falsifiable prediction. If confirmed, modification is needed — see `ns-tension-resolution-paths.md`.

### Fakeon Mass Constraint

- m_χ > m_φ/4 (fakeon must be heavier than 1/4 of inflaton mass)

## Full CMB Predictions Catalog

### Running of the Spectral Index: α_s = dn_s/d ln k

- **Pure Starobinsky:** α_s = -2/N² ≈ -6.6 × 10⁻⁴ (N=55)
- **QG+F:** α_s ≃ -(1/2)(n_s - 1)² ≈ -6.5 × 10⁻⁴. C² corrections enter at O(α³) ≈ 10⁻⁶, well below any foreseeable measurement.
- **Six-derivative:** α_s ≈ -8 × 10⁻⁴ (slightly larger)
- **Current data:** -0.0045 ± 0.0067 (consistent with all)

### Running of the Running: β_s = dα_s/d ln k

- **Pure Starobinsky / QG+F:** β_s ≈ 4/N³ + O(α⁴) ≈ 2.4 × 10⁻⁵ (N=55). Indistinguishable from Starobinsky. Not yet constrained.

### Tensor Spectral Tilt: n_T

- **Pure Starobinsky / QG+F:** n_T ≈ -r/8 (consistency relation preserved to leading order)
- **QG+F first correction** (Anselmi 2021, JCAP 01, 048): r + 8n_T = O(α²) ≈ 10⁻⁴. Distinctive QG+F prediction but far below foreseeable measurement precision.
- **Six-derivative:** C□C modifies tensor propagator, but consistency relation violation remains tiny.

### Non-Gaussianity: f_NL

- **QG+F:** f_NL ~ O(α/N) ~ 10⁻⁴. Fakeon enters only through loop corrections to scalar bispectrum, suppressed by α ~ 1/115. Unmeasurably small.
- **Current:** f_NL^local = -0.9 ± 5.1 (Planck). CMB-S4 would have achieved σ(f_NL) ~ 1, both far above QG+F prediction.

### Isocurvature Modes

- **Standard QG+F:** None. Single-field R² inflation produces only adiabatic perturbations.
- **Multi-field QG+F (φ² + R²+C²):** Scalar mixing affects only subleading corrections (Anselmi et al. 2021, arXiv:2105.05864).
- **Current bound:** < 0.038 (95% CL)

### Spectral Features from the Fakeon Sector

- **QG+F:** The fakeon produces NO spectral features at leading order — contributes only through virtual corrections that modify amplitude and tilt smoothly. No oscillatory features, bumps, or steps.
- **IHO/DQFT (Sravan Kumar):** Claims parity-odd oscillations in tensor power spectrum at large scales — the one observable that could distinguish IHO from fakeon. See `iho-ghost-interpretation.md`.

### Summary Predictions Table

| Observable | Pure Starobinsky | QG+F (4-deriv) | QG+F (6-deriv) | Current Data |
|-----------|-----------------|----------------|----------------|--------------|
| n_s | 1 - 2/N ≈ 0.964 | ≈ 0.964-0.967 | **≈ 0.974** | 0.9682 ± 0.0032 |
| r | 12/N² ≈ 0.004 | 0.0004-0.004 | **≈ 0.0045** | < 0.034 (95%) |
| α_s | -2/N² ≈ -6.6×10⁻⁴ | ≈ -6.6×10⁻⁴ | ≈ -8×10⁻⁴ | -0.0045 ± 0.0067 |
| β_s | 4/N³ ≈ 2.4×10⁻⁵ | ≈ 2.4×10⁻⁵ | ~ 10⁻⁵ | Not constrained |
| n_T | -r/8 ≈ -5×10⁻⁴ | ≈ -r/8 + O(10⁻⁴) | ≈ -r/8 | Not measured |
| f_NL | ~ 10⁻⁴ | ~ 10⁻⁴ | ~ 10⁻⁴ | -0.9 ± 5.1 |
| Isocurvature | None | None | None | < 0.038 (95%) |
| Parity features | None | None | None | ~2-3σ anomaly |

**Key conclusion:** Beyond n_s and r, all other QG+F CMB observables are indistinguishable from pure Starobinsky at any foreseeable experimental precision. The C² corrections enter at O(1/115), making them tiny.

## Additional Notes

- **Running from quantum gravity:** Anselmi (JCAP 2021, arXiv: 2007.15023) showed QG+F predicts small nonzero running dn_s/d ln k from quantum gravity corrections not suppressed by slow-roll parameters. Magnitude ~10⁻³. Furthermore, the direct RG running of the R² coupling during inflation gives Δn_s ~ 10⁻¹⁴ — **completely negligible** (see `ns-tension-resolution-paths.md` for the definitive calculation).
- Current observational bound: r < 0.036 (BICEP/Keck 2021, 95% CL) — the theory is comfortably within this

## Experimental Testability

This is a **concrete, falsifiable prediction** within reach of near-future experiments:

| Experiment | Sensitivity | Status | Probe Range |
|------------|------------|--------|-------------|
| **LiteBIRD** (JAXA) | σ(r) < 10⁻³ | Launch 2032, results ~2036-2037 | Upper half of prediction |
| **SO enhanced** (6 SATs) | σ(r) ~ 0.001 | ~2034 | Discrimination window |
| ~~CMB-S4~~ | ~~σ(r) ≤ 5 × 10⁻⁴~~ | **CANCELLED July 2025** | ~~Nearly entire prediction range~~ |

**Falsification criterion:** If LiteBIRD or CMB-S4 measure r < 0.0004 or r > 0.0035, the theory (with standard single-field inflation) is ruled out.

## Significance

QG+F makes **two sharp, falsifiable inflationary predictions**:

1. **r in [0.0004, 0.0035]**: Testable by LiteBIRD/CMB-S4 within the next decade.
2. **n_s ≈ 0.967 (for N = 60)**: Already in 2.3σ tension with CMB+DESI data (n_s ≈ 0.974). SO + LiteBIRD will be definitive by ~2034-2037 (CMB-S4 cancelled July 2025).

The n_s prediction is arguably MORE constraining than r, because the current data already shows tension. If n_s ≈ 0.974 is confirmed, QG+F requires modification to the R² sector (see `ns-tension-resolution-paths.md`). If the RG running of f₀² naturally produces the right shift, this would be a triumph for the theory. If not, the six-derivative extension becomes necessary (see `six-derivative-extension.md`).

Sources: Anselmi (2020), JHEP 07, 211; Anselmi (2022), Symmetry 14(3), 521; Anselmi, Bianchi & Piva (2020), JHEP; Anselmi (2021), JCAP; arXiv: 2504.20757; BICEP/Keck (2021); LiteBIRD collaboration; CMB-S4 collaboration
