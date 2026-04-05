# MOND / RAR Interpolating-Function Fits

- Sample: 163 galaxies and 3269 radial points after the Q=1/2 cut.
- Best-fit a0: 9.5675e-11 m s^-2.
- Winning model: generalized exponential (generalized_exponential).
- Winning transition width: 2.91 decades from slope 0.55 to 0.95.

## BIC Ranking

| Rank | Model | a0 [m s^-2] | Scatter [dex] | Intrinsic scatter [dex] | Chi^2 | BIC | ΔBIC | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | generalized exponential | 9.5675e-11 | 0.1808 | 0.1315 | 3577.7 | -2901.8 | 0.0 | Free sharpness n; n=1 recovers the McGaugh exponential RAR. |
| 2 | simple MOND | 1.0952e-10 | 0.1812 | 0.1319 | 3576.7 | -2894.4 | 7.4 | Exact equivalent of the Bekenstein toy / simple mu(x)=x/(1+x) law. |
| 3 | RAR exponential | 1.1219e-10 | 0.1813 | 0.1319 | 3574.9 | -2892.7 | 9.1 | McGaugh et al. exponential RAR; exact n=1 case of the generalized exponential family. |
| 4 | standard MOND | 1.5565e-10 | 0.1866 | 0.1395 | 3537.0 | -2620.1 | 281.6 | Canonical mu(x)=x/sqrt(1+x^2) form written in nu(y) form. |

## Deep-MOND Fit

- Cut: g_bar < 0.1 a0 = 9.5675e-12 m s^-2.
- Points used: 1147 across 119 galaxies.
- Slope: 0.683 ± 0.073 (bootstrap 1σ).
- Intercept: -2.879 ± 0.827.

## Interpretation

The canonical simple and McGaugh RAR forms are close in BIC, but the generalized exponential wins by allowing a broader transition than the fixed n=1 curve.
The standard MOND interpolating function is strongly disfavored relative to the other three by BIC.
The low-acceleration cut g_bar < 0.1 a0 still reaches into the turnover region, so the fitted slope stays steeper than the asymptotic 1/2 limit.
