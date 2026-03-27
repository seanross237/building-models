# Riemann Hypothesis — Factual Library

Statistical properties of non-trivial Riemann zeta zeros and their connection to random matrix theory (GUE). Computational verification of the Montgomery-Odlyzko law, Berry's spectral saturation prediction, and constraints on the hypothetical Riemann operator. 5 findings.

## Short-Range Statistics (GUE Confirmation)

- **gue-pair-correlation.md** — Pair correlation of first 2,000 zeta zeros matches Montgomery's conjecture to 9.1% mean relative deviation (STRONG MATCH); deviations consistent with noise (68% within 1sigma, chi-squared/dof = 1.50); no height dependence detected.
- **gue-nearest-neighbor-spacing.md** — Nearest-neighbor spacing matches GUE Wigner surmise to 4.1% mean absolute deviation (STRONG MATCH); ensemble discrimination: GUE definitively beats GOE (2x) and Poisson (5x), suggestively beats GSE (1.2x); KS marginal failure reflects Wigner surmise approximation, not departure from GUE.
- **spectral-form-factor-gue.md** — Spectral form factor K(τ) matches GUE: ramp slope = 1.010 (1% of GUE), plateau mean = 1.043 ± 0.077 (4.3% of GUE). Confirms GUE universality class through Fourier-space statistics; indistinguishable from GUE simulation.

## Long-Range Statistics (Berry Saturation)

- **berry-saturation-confirmed.md** — Berry's (1985) saturation prediction definitively confirmed: number variance Σ²(L) saturates at ~0.3–0.5 for L > 2 (growth rate 12× below GUE sim, 34× below GUE theory); spectral rigidity Δ₃(L) saturates at 0.156 for L > 15 (constant to L=100). Zeta zeros are 30–50% more rigid than finite-size GUE at large scales. Caused by prime periodic orbits.

## Operator Constraints

- **riemann-operator-constraints.md** — GUE statistics imply the hypothetical Riemann operator must act on a complex Hilbert space, break time-reversal symmetry, and exhibit quadratic level repulsion; definitively rules out Poisson, GOE, disfavors GSE. Long-range statistics add: classical dynamics must be chaotic, shortest periodic orbit periods ~ log p, super-rigidity beyond GUE at large scales.
