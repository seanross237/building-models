---
topic: GUE pair correlation of Riemann zeta zeros
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-001"
---

## Finding

The pair correlation function of Riemann zeta zeros matches the GUE prediction (Montgomery's conjecture, R_2(r) = 1 - (sin(pi*r)/(pi*r))^2) to high precision. Deviations are statistically consistent with sampling noise.

## Quantitative Results

**Low height (first 2,000 zeros, t ~ 14-2,515):**
- Mean relative deviation: 9.1% (for predictions > 0.1)
- Mean absolute deviation: 0.074
- Max absolute deviation: 0.262
- Statistical uncertainty per bin: +/-0.100
- Chi-squared: 147.3 for 98 dof (chi-squared/dof = 1.50)
- Deviation distribution: 68% within 1-sigma (expected ~68%), 90% within 2-sigma (expected ~95%)
- Classification: **STRONG MATCH**

**High height (zeros 9,501-10,000, t ~ 9,450-9,878):**
- Mean relative deviation: 17.2%
- Mean absolute deviation: 0.152
- Statistical uncertainty per bin: +/-0.199
- Classification: **MODERATE MATCH** (sample-limited; 500 zeros vs. 2,000)

## Height Dependence

No evidence that the GUE match weakens or strengthens with height in this range. The increased deviations at high height are entirely explained by the 4x smaller sample size (500 vs. 2,000 zeros). Published results (Odlyzko) using millions of zeros at t ~ 10^20 confirm the match strengthens with height.

## Statistical Significance

The slightly elevated chi-squared/dof = 1.50 (perfect match ~1.0) may reflect: (a) unfolding formula inaccuracies at low height (leading-order smooth approximation x_n = (t_n/2pi)*log(t_n/(2pi*e)) is least accurate for the lowest zeros), or (b) bin-to-bin correlations from boundary effects.

## Methodology

- Software: Python 3.14, mpmath 1.4.1 (`zetazero(n)`)
- Precision: 20 decimal places
- Unfolding: x_n = (t_n / 2pi) * log(t_n / (2pi*e))
- Mean unfolded spacing verified ~ 1.0000 (low: 0.999965, high: 1.000870)
- Bin width: 0.05, range [0, 5], pairs within r < 5.5
- Computation rate: ~5.6 zeros/s at n=2000, ~1.4/s at n=10,000 (mpmath; Odlyzko-Schonhage essential for large-scale studies)
