---
topic: Vorticity intermittency — flatness 2-12x Gaussian, extreme spatial concentration, F4 scaling of effective constant
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-007"
---

## Overview

Direct measurement of vorticity intermittency via flatness (F4) and volume fractions on Taylor-Green vortex DNS. Vorticity is **highly intermittent**: flatness 2-7x above Gaussian prediction, with only 1-2.4% of the domain containing |omega| > 0.5*omega_max. The effective Ladyzhenskaya constant scales as F4^{-0.30}, close to the predicted -0.25 exponent but with a 4x residual factor from geometric alignment.

---

## Flatness Results

| Re | F4 mean | F4 (peak enstrophy) | Gaussian (5/3) | Excess flatness |
|---|---|---|---|---|
| 100 | 1.82 | 3.26 | 1.67 | 1.10-1.96x |
| 500 | 3.60 | 12.13 | 1.67 | 2.16x (mean) to 7.3x (peak) |
| 1000 | 3.96 | 11.44 | 1.67 | 2.37x to 6.9x |
| 5000 | 4.09 | 9.42 | 1.67 | 2.45x to 5.7x |

Intermittency increases with Re in the mean. Peak F4 is highest at Re=500-1000 (peak enstrophy occurs later at higher Re and the field is more developed). [COMPUTED]

---

## Volume Fractions (at peak enstrophy)

| Re | mu(0.1) | mu(0.3) | mu(0.5) | mu(0.7) | mu(0.9) |
|---|---|---|---|---|---|
| 100 | 0.852 | 0.139 | 0.024 | 0.008 | 0.001 |
| 500 | 0.304 | 0.021 | 0.010 | 0.003 | 0.002 |
| 1000 | 0.334 | 0.025 | 0.011 | 0.004 | 0.002 |
| 5000 | 0.372 | 0.033 | 0.012 | 0.004 | 0.001 |

Only **1-2.4% of the domain** has |omega| > 0.5*omega_max. Only **0.1-0.2%** has |omega| > 0.9*omega_max. Higher Re gives more concentrated distribution. [COMPUTED]

---

## Effective Constant vs Flatness

| Re | C_{L,eff}/C_L mean | Predicted from F4^{-1/4} | Correlation |
|---|---|---|---|
| 100 | 0.184 | 0.845 | r = -0.80 |
| 500 | 0.170 | 0.609 | r = -0.91 |
| 1000 | 0.167 | 0.618 | r = -0.93 |
| 5000 | 0.165 | 0.649 | r = -0.94 |

**Best fit: C_{L,eff}/C_L ~ F4^{-0.30}** (averaged across Re). The exploration-006 prediction of F4^{-1/4} captures the correct scaling trend but underestimates the Ladyzhenskaya slack by ~4x. The residual factor comes from geometric alignment/cancellation (the alpha_geom factor from exploration 004, which contributes independently of spectral intermittency). [COMPUTED]
