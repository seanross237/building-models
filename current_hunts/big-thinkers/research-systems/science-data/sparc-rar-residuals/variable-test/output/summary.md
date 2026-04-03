# Variable Test Summary

- Galaxies used: 163 (Q = 1 or 2)
- Radial points used: 3269
- Surface-brightness split: median `SBeff = 81.81 Lsun/pc^2`
- Gas-fraction split: median `fgas = 0.463`

## Scatter ranking

| Variable | Scatter (dex) | Notes |
|---|---:|---|
| `g_bar` | 0.1794 | Baseline acceleration variable. |
| `Sigma_bar` | 0.1794 | Approximate disk surface density from V_bar^2 / (2 pi G r). |
| `Phi_bar` | 0.2368 | Potential depth relative to the outermost SPARC point. |
| `|dg_bar/dr|` | 0.2952 | Magnitude of the radial acceleration gradient. |

## Main takeaways

- `g_bar` is the tightest empirical variable in this SPARC implementation at 0.1794 dex.
- `Sigma_bar` ties exactly with `g_bar` because the requested approximation `Sigma = V_bar^2 / (2 pi G r)` is algebraically proportional to `g_bar = V_bar^2 / r`.
- `Phi_bar` is visibly looser, and `|dg_bar/dr|` is the loosest of the four.
- Because `corr(g_bar, Sigma_bar) = 1.000`, SPARC cannot distinguish acceleration from this approximate surface-density proxy.

## Correlation matrix

| Variable | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |
|---|---:|---:|---:|---:|
| `g_bar` | 1.0000 | 0.9074 | 1.0000 | 0.8861 |
| `Phi_bar` | 0.9074 | 1.0000 | 0.9074 | 0.7459 |
| `Sigma_bar` | 1.0000 | 0.9074 | 1.0000 | 0.8861 |
| `|dg_bar/dr|` | 0.8861 | 0.7459 | 0.8861 | 1.0000 |

## Most diagnostic galaxies

| Galaxy | Score | Main tension |
|---|---:|---|
| NGC6789 | 0.3004 | `Phi_bar vs |dg_bar/dr|` |
| UGC07232 | 0.3001 | `Phi_bar vs |dg_bar/dr|` |
| UGC04483 | 0.2511 | `Phi_bar vs |dg_bar/dr|` |
| CamB | 0.2462 | `Phi_bar vs |dg_bar/dr|` |
| UGC07577 | 0.2325 | `Phi_bar vs |dg_bar/dr|` |
| UGCA444 | 0.2146 | `Phi_bar vs |dg_bar/dr|` |
| NGC0289 | 0.2040 | `Phi_bar vs |dg_bar/dr|` |
| NGC4214 | 0.1991 | `Phi_bar vs |dg_bar/dr|` |
| UGC01230 | 0.1987 | `Phi_bar vs |dg_bar/dr|` |
| UGC02885 | 0.1980 | `Phi_bar vs |dg_bar/dr|` |

## Subpopulation winners

- mass >= 1e10 Msun: g_bar=0.1384, Sigma_bar=0.1384, Phi_bar=0.2007, |dg_bar/dr|=0.2104
- mass < 1e10 Msun: Sigma_bar=0.2201, g_bar=0.2201, Phi_bar=0.2735, |dg_bar/dr|=0.2980
- high surface brightness: g_bar=0.1541, Sigma_bar=0.1541, Phi_bar=0.2134, |dg_bar/dr|=0.2361
- low surface brightness: Sigma_bar=0.2174, g_bar=0.2174, Phi_bar=0.2569, |dg_bar/dr|=0.2828
- gas-rich: g_bar=0.2079, Sigma_bar=0.2079, Phi_bar=0.2619, |dg_bar/dr|=0.2698
- star-dominated: g_bar=0.1605, Sigma_bar=0.1605, Phi_bar=0.2143, |dg_bar/dr|=0.2492

## Caveats

- `Phi_bar` is a relative potential depth anchored to the outermost measured SPARC radius, so it is a practical proxy rather than an absolute potential.
- `|dg_bar/dr|` uses the magnitude of the numerical gradient because a signed gradient mixes rising and falling parts of the curve and is not directly comparable in log space.
- If surface density is computed from full photometric profiles instead of the requested approximation, the exact `g_bar`-`Sigma_bar` degeneracy could be broken.
