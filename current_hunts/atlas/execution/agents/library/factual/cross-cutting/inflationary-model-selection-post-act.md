---
topic: cross-cutting
confidence: provisional
date: 2026-03-24
source: exploration-004-ns-tension-analysis (strategy-002)
---

# Inflationary Model Selection After ACT DR6 and DESI

## Context

If n_s = 0.974 ± 0.002 is confirmed by CMB-S4, the inflationary model landscape narrows dramatically. Most models naturally predicting n_s ≈ 0.974 have **no known UV completion** — posing a challenge for quantum gravity programs.

## Models Favored by n_s ≈ 0.974

1. **Monomial potentials V(φ) ∝ φ^(2/3)** (axion monodromy): n_s ≈ 0.972-0.977 for N = 50-60. Excellent fit. Formula: n_s = 1 − (p+2)/(2N), so for p = 2/3, N = 57: n_s ≈ 0.977.
2. **R² + R³ corrected Starobinsky**: δ₃ ~ −10⁻⁴ gives n_s ≈ 0.974 (arXiv: 2505.10305)
3. **RG-improved Starobinsky** (AS-type corrections): Running of R² coupling pushes n_s upward. **Note**: within QG+F specifically, the direct RG running of R² is negligible (Δn_s ~ 10⁻¹⁴; see `quadratic-gravity-fakeon/ns-tension-resolution-paths.md`); the effective shift requires either AS-specific non-perturbative effects or the R³ correction from six-derivative gravity.
4. **Natural inflation variants**: Decay constant f ~ 5-10 M_Pl
5. **Smooth hybrid inflation**: Fits ACT data (arXiv: 2506.15965)
6. **α-attractor GUP models**: Modified by generalized uncertainty principle (arXiv: 2506.10547)

## Models Disfavored (>3σ if n_s = 0.974 confirmed)

- **Pure Starobinsky R² inflation**: n_s ≈ 0.967 for N = 60
- **Pure Higgs inflation**: Similar predictions to Starobinsky
- **Standard α-attractor E-models** (α = 1): n_s = 0.958-0.963
- **Standard α-attractor T-models**: n_s = 0.956-0.961
- Any model predicting n_s < 0.968

## The UV Completion Challenge

**Key observation**: Most models naturally predicting n_s ≈ 0.974 are NOT connected to UV-complete quantum gravity theories. Monomial potentials (φ^(2/3)) are simple phenomenological models with no known UV completion. The challenge is finding a UV-complete theory that naturally predicts this value.

The exceptions are:
- RG-improved Starobinsky (connected to AS; QG+F's perturbative RG running is negligible — the shift requires non-perturbative AS effects or the six-derivative extension)
- Six-derivative gravity (super-renormalizable, naturally includes R³ at tree level — the leading candidate for UV-complete resolution)

This makes the QG+F resolution paths (see `quadratic-gravity-fakeon/ns-tension-resolution-paths.md`) especially important: they would connect a UV-complete theory to the observed n_s.

## Spectral Index Running

ACT DR6: dn_s/d ln k = 0.0062 ± 0.0052 (consistent with zero, positive central value). In QG+F, Anselmi (JCAP 2021) predicts small nonzero running from quantum gravity corrections not suppressed by slow-roll parameters. However, the magnitude (|dn_s/d ln k| ~ 10⁻³) is too small to explain Δn_s ~ 0.007 over accessible scales.

## Assessment

The n_s tension, if real, preferentially selects theories with corrections to the Starobinsky potential. Among UV-complete candidates, only QG+F (via RG improvement or six-derivative extension) and asymptotic safety (via RG-improved inflation) currently offer natural explanations. This makes the n_s measurement a powerful discriminator for quantum gravity programs — more powerful than r alone.

Sources: arXiv: 2512.10613, arXiv: 2510.18656, arXiv: 2505.10305, arXiv: 2506.15965, arXiv: 2506.10547, arXiv: 2509.04832, arXiv: 2007.15023
