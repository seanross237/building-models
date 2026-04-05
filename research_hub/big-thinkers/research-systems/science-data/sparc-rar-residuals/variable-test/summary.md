# SPARC Variable-Control Analysis

- Galaxies used: 163 with `Q = 1` or `2`
- Radial points used: 3269
- Model: cubic spline in log-log space with quantile knots; low-order polynomial fallback for small subsets
- Mass split: `Mbar = 1e10 Msun`
- Surface-brightness split: median `SBeff = 81.81 Lsun/pc^2`
- Gas-fraction split: median `fgas = 0.467`

## Scatter Ranking

| Rank | Variable | Scatter (dex) | Points | Notes |
|---:|---|---:|---:|---|
| 1 | `Sigma_bar` | 0.1795 | 3269 | Surface-density proxy proportional to g_bar. |
| 1 | `g_bar` | 0.1795 | 3269 | Standard baryonic acceleration. |
| 2 | `Phi_bar` | 0.2368 | 3106 | Relative baryonic potential depth from the outermost measured radius. |
| 3 | `|dg_bar/dr|` | 0.2954 | 3269 | Magnitude of the finite-difference acceleration gradient. |

## Main Result

- Best relation: **Sigma_bar / g_bar** at **0.1795 dex**.
- `Sigma_bar` is algebraically proportional to `g_bar`, so the two are expected to tie to numerical precision in log space.
- `Phi_bar` is the next-tightest candidate, and `|dg_bar/dr|` is the loosest of the four.

## Candidate Correlation Matrix

| Variable | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |
|---|---:|---:|---:|---:|
| `g_bar` | 1.0000 | 0.9074 | 1.0000 | 0.8861 |
| `Phi_bar` | 0.9074 | 1.0000 | 0.9074 | 0.7459 |
| `Sigma_bar` | 1.0000 | 0.9074 | 1.0000 | 0.8861 |
| `|dg_bar/dr|` | 0.8861 | 0.7459 | 0.8861 | 1.0000 |

## Diagnostic Galaxies

| Galaxy | Diagnostic score | Strongest rank tension | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |
|---|---:|---|---:|---:|---:|---:|
| NGC6789 | 0.3004 | Phi_bar vs |dg_bar/dr| | 0.580 | 0.068 | 0.580 | 0.907 |
| UGC07232 | 0.3001 | Phi_bar vs |dg_bar/dr| | 0.617 | 0.086 | 0.617 | 0.920 |
| UGC04483 | 0.2511 | Phi_bar vs |dg_bar/dr| | 0.296 | 0.012 | 0.296 | 0.716 |
| CamB | 0.2462 | Phi_bar vs |dg_bar/dr| | 0.210 | 0.019 | 0.210 | 0.685 |
| UGC07577 | 0.2325 | Phi_bar vs |dg_bar/dr| | 0.056 | 0.006 | 0.056 | 0.574 |
| UGCA444 | 0.2146 | Phi_bar vs |dg_bar/dr| | 0.130 | 0.025 | 0.130 | 0.580 |
| NGC0289 | 0.2040 | Phi_bar vs |dg_bar/dr| | 0.426 | 0.673 | 0.426 | 0.099 |
| NGC4214 | 0.1991 | Phi_bar vs |dg_bar/dr| | 0.500 | 0.247 | 0.500 | 0.809 |
| UGC01230 | 0.1987 | Phi_bar vs |dg_bar/dr| | 0.333 | 0.605 | 0.333 | 0.043 |
| UGC02885 | 0.1980 | Phi_bar vs |dg_bar/dr| | 0.642 | 0.840 | 0.642 | 0.290 |

## Subgroup Winners

- mass >= 1e10 Msun: winner **g_bar / Sigma_bar**; g_bar=0.1387, Sigma_bar=0.1387, Phi_bar=0.2008, |dg_bar/dr|=0.2108
- mass < 1e10 Msun: winner **g_bar / Sigma_bar**; Sigma_bar=0.2201, g_bar=0.2201, Phi_bar=0.2739, |dg_bar/dr|=0.2992
- high surface brightness (SBeff >= 81.81): winner **g_bar / Sigma_bar**; g_bar=0.1544, Sigma_bar=0.1544, Phi_bar=0.2136, |dg_bar/dr|=0.2365
- low surface brightness (SBeff < 81.81): winner **g_bar / Sigma_bar**; g_bar=0.2178, Sigma_bar=0.2178, Phi_bar=0.2576, |dg_bar/dr|=0.2828
- gas-rich (fgas >= 0.467): winner **g_bar / Sigma_bar**; g_bar=0.2085, Sigma_bar=0.2085, Phi_bar=0.2609, |dg_bar/dr|=0.2690
- star-dominated (fgas < 0.467): winner **g_bar / Sigma_bar**; g_bar=0.1577, Sigma_bar=0.1577, Phi_bar=0.2147, |dg_bar/dr|=0.2435

## Subgroup Conclusion

- The winner does not change across the requested subgroup splits; `g_bar` and `Sigma_bar` remain tied for best scatter in every case.

## Notes

- `Phi_bar` is defined as the outward integral of `g_bar = V_bar^2 / r` from each radius to the outermost measured SPARC radius, so the outermost point is zero by construction and is excluded from log fits.
- `|dg_bar/dr|` uses the magnitude of the finite-difference derivative so it can be fit in log space.
- The mass split uses a fixed `M/L = 0.5` proxy on the total 3.6 micron luminosity plus helium-corrected HI mass, which keeps the analysis within the two requested SPARC tables.
