# Exploration 009 — Summary

## Outcome: ARTIFACT

The λ_n^zeta/λ_n^GUE crossover ratio from E007/E008 is a **truncation artifact**, not a genuine structural signal.

## Key Evidence

Matched ratio at n=500 across K=N levels:

| K=N | Ratio | Significance |
|-----|-------|-------------|
| 500 | 0.888 | -22.3σ below 1 |
| 1000 | 0.898 | -16.9σ below 1 |
| 2000 | 0.952 | -7.3σ below 1 |
| 3000 | 1.004 | +0.5σ above 1 |
| 5000 | 1.090 | +9.7σ above 1 |

The ratio is **monotonically increasing** with K=N and crosses 1.0 between K=N=2000 and 3000. At K=N=5000, zeta is 9% ABOVE GUE, not below. The crossover point (n where ratio first drops below 1) disappears entirely at K=N ≥ 3000.

## Root Cause

The linear scaling of GUE eigenvalues to [t_1, t_K] introduces a systematic density mismatch. As the range widens with K, the semicircle distribution concentrates GUE eigenvalues at large t (small contributions), while zeta zeros have logarithmically growing density across the entire range. This causes GUE λ_n to stagnate/decrease at small n while zeta λ_n increases monotonically.

## Verification Scorecard

- **[COMPUTED]: 7** — All zeta/GUE values at 5 K-levels, ratio table, trend analysis
- **[VERIFIED]: 0**
- **[CONJECTURED]: 0**

## Final Verdict

The novel claim (E007: "λ_n^zeta/λ_n^GUE < 1 for n > 272, ratio ≈ 0.949") does NOT survive. It is valid only at K=N=2000 and reverses at larger K=N. **The comparison method itself is flawed** — the linear-scaling GUE does not provide a K-independent baseline.

## Further Work

If pursuing zeta-GUE comparison, the scaling method needs fundamental revision: either use unfolded zeros with unit mean spacing (standard in RMT), or match the local density profile of zeros rather than linearly rescaling.
