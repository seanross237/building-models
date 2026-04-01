---
topic: Spectral form factor K(τ) confirms GUE universality class
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-002"
---

## Finding

The spectral form factor K(τ) of the first 2,000 Riemann zeta zeros matches the GUE random matrix prediction to within 1–4%, confirming GUE universality through Fourier-space statistics independent of pair correlation and spacing distribution.

## Method

K(τ) = (1/N) |Σ exp(2πiτx_n)|². Ensemble averaging over 16 overlapping blocks of 400 zeros with local re-unfolding. Compared against same procedure on GUE simulation eigenvalues (6 blocks of 400).

## Results

| Region | Quantity | Zeta | GUE sim | GUE theory |
|--------|----------|-----:|--------:|-----------:|
| Ramp (0.1 < τ < 0.8) | Slope | **1.010** | 1.021 | 1.000 |
| Plateau (1.3 < τ < 2.5) | Mean | **1.043** | 1.044 | 1.000 |
| Plateau | Std | 0.077 | 0.146 | 0.000 |

- **Ramp slope = 1.010** — within 1% of GUE prediction K(τ) = τ. Confirms level repulsion at all short-range scales.
- **Plateau mean = 1.043 ± 0.077** — within 4.3% of unity. Ramp-to-plateau transition occurs near τ ≈ 1 as predicted.
- Zeta and GUE simulation form factors are essentially indistinguishable in both shape and magnitude.

## Significance

The form factor is the Fourier transform of the two-point correlation function. Its GUE match, combined with the Berry saturation seen in number variance and spectral rigidity, confirms Berry's (1985) predicted pattern: the form factor is modified only at very small τ (below block resolution), while the main ramp-plateau structure remains intact. Short-range correlations are GUE; long-range correlations show additional rigidity from prime periodic orbits.

The ramp structure (K(τ) ∝ τ for τ < 1) specifically indicates time-reversal symmetry breaking, consistent with the Riemann operator having no anti-unitary symmetry (GUE, β = 2 ensemble).
