# SPARC RAR Residual Correlation Summary

- Galaxies kept: 163 (quality flag 1 or 2)
- Radial points kept: 3269
- Point-level residual scatter: 0.1811 dex
- Mean of per-galaxy mean residuals: -0.0487 dex
- Scatter of per-galaxy mean residuals: 0.1707 dex

## Spearman Results

| Property | rho | p-value | Significant (p < 0.01) |
|---|---:|---:|---:|
| Maximum rotation velocity | +0.324 | 2.521e-05 | 1 |
| Quality flag | -0.309 | 5.924e-05 | 1 |
| Hubble type | -0.196 | 0.012 | 0 |
| Effective surface brightness | +0.176 | 0.02433 | 0 |
| Total baryonic mass | +0.149 | 0.05803 | 0 |
| Distance | +0.119 | 0.1305 | 0 |
| Disk scale length | +0.105 | 0.1803 | 0 |
| Gas fraction | -0.074 | 0.3502 | 0 |

## Interpretation

Significant correlations were found and need follow-up artifact checks:
- Maximum rotation velocity: rho = +0.324, p = 2.521e-05
- Quality flag: rho = -0.309, p = 5.924e-05

Under the requested Q<=2 cut, the only p<0.01 signals are Vmax and the SPARC quality flag.
The quality-flag trend is almost certainly non-physical because Q directly measures data reliability.
The Vmax trend is also likely non-physical: it disappears in the Q=1 subsample, survives only in Q=2 galaxies, and Vmax is strongly anti-correlated with the fractional velocity-error proxies.
No robust physical second-parameter signal is seen for gas fraction, distance, disk scale length, or total baryonic mass.

## Artifact Checks

| Check | Sample | rho | p-value |
|---|---|---:|---:|
| Residual vs Vmax (all Q<=2) | all | +0.324 | 2.521e-05 |
| Residual vs quality flag | all | -0.309 | 5.924e-05 |
| Residual vs mean fractional V error | all | -0.258 | 0.0008923 |
| Residual vs median fractional V error | all | -0.211 | 0.006776 |
| Residual vs number of RC points | all | +0.211 | 0.006846 |
| Vmax vs quality flag | all | -0.336 | 1.149e-05 |
| Vmax vs mean fractional V error | all | -0.588 | 1.517e-16 |
| Vmax vs median fractional V error | all | -0.595 | 5.34e-17 |
| Residual vs Vmax within Q=1 | Q=1 | +0.097 | 0.3404 |
| Residual vs Vmax within Q=2 | Q=2 | +0.521 | 1.039e-05 |
| Residual vs Vmax with Inc>30 deg | Inc>30 | +0.319 | 7.137e-05 |
| Residual vs Vmax with Inc>30 deg and Q=1 | Inc>30,Q=1 | +0.131 | 0.209 |
| Residual vs Vmax with Inc>30 deg and Q=2 | Inc>30,Q=2 | +0.518 | 4.335e-05 |

## Inclination > 30 deg Robustness

| Property | rho | p-value |
|---|---:|---:|
| Maximum rotation velocity | +0.319 | 7.137e-05 |
| Quality flag | -0.265 | 0.001099 |
| Hubble type | -0.208 | 0.01076 |
| Effective surface brightness | +0.201 | 0.01412 |
| Total baryonic mass | +0.164 | 0.04622 |
| Gas fraction | -0.112 | 0.1743 |
| Distance | +0.111 | 0.1785 |
| Disk scale length | +0.109 | 0.187 |
