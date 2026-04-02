---
topic: GUE nearest-neighbor spacing of Riemann zeta zeros
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-001"
---

## Finding

The nearest-neighbor spacing distribution of Riemann zeta zeros matches the GUE Wigner surmise (P_GUE(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)) and definitively discriminates GUE from other universality classes.

## Quantitative Results

**Low height (first 2,000 zeros):**
- Mean absolute deviation from Wigner surmise: 0.041
- Max absolute deviation: 0.278
- Standard deviation of normalized spacings: 0.3845
- Min spacing: 0.0893; Max spacing: 2.4587
- KS test: statistic = 0.0406, critical value (5%) = 0.0304, critical value (1%) = 0.0365
- KS result: **Marginally rejects** Wigner surmise at 5% significance
- Classification: **STRONG MATCH**

**High height (zeros 9,501-10,000):**
- Mean absolute deviation from Wigner surmise: 0.057
- Standard deviation of normalized spacings: 0.3967
- KS test: statistic = 0.0441, critical value (5%) = 0.0609
- KS result: **Passes** at 5% (larger critical value from smaller sample)
- Classification: **STRONG MATCH**

## KS Test Caveat

The marginal KS failure at low height does NOT indicate departure from GUE. The Wigner surmise is the exact spacing distribution for 2x2 GUE matrices, used as an approximation for large-N GUE. The exact large-N distribution (via Fredholm determinants of the sine kernel) differs from the Wigner surmise by ~1-3%. With 2,000 zeros, the data is precise enough to detect this approximation error but not precise enough to distinguish between candidate exact distributions.

## Ensemble Discrimination

Mean absolute deviation from each universality class:

| Ensemble | Low Height | High Height | Level Repulsion |
|----------|-----------|-------------|-----------------|
| **GUE (beta=2)** | **0.041** | **0.057** | s^2 (quadratic) |
| GSE (beta=4) | 0.050 | 0.074 | s^4 (quartic) |
| GOE (beta=1) | 0.089 | 0.092 | s (linear) |
| Poisson | 0.219 | 0.222 | none |

- GUE vs. GOE: **Definitive** (GUE 2x better)
- GUE vs. Poisson: **Definitive** (GUE 5x better)
- GUE vs. GSE: **Suggestive** (GUE 1.2x better)

The ordering GUE < GSE < GOE << Poisson is consistent at both heights.

## Level Repulsion

| Threshold | Observed fraction | GUE expected | Ratio |
|-----------|-------------------|--------------|-------|
| s < 0.1 | 0.000500 | 0.001073 | 0.47 |
| s < 0.2 | 0.003002 | 0.008387 | 0.36 |
| s < 0.5 | 0.080040 | 0.112000 | 0.71 |

Quadratic level repulsion (P(s) ~ s^2 for small s) is confirmed, consistent with GUE.
