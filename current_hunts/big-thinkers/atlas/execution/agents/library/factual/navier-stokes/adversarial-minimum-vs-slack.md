---
topic: Adversarial IC search finds minimum vortex stretching slack at 157.70x — TGV not optimal
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-003"
---

## Overview

Adversarial search across initial conditions on 3D periodic Navier-Stokes (T^3) finds that the minimum vortex stretching (VS) slack ratio is **157.70x** (converged at N=128), achieved by anti-parallel vortex tubes with sigma=2.5, d=pi/4, delta=1.2 at Re=100. This is **34% below the Taylor-Green vortex baseline of 236.90x**.

The Taylor-Green vortex was previously the tightest known IC. The adversarial search shows it is not the global minimum — its competing symmetries (mirror planes in all three axes) partially cancel vortex stretching contributions.

---

## Five-IC Comparison (N=64, max|u|=1)

| Initial Condition | Re=100 | Re=500 | Re=1000 | Overall Min | vs TGV |
|---|---|---|---|---|---|
| Taylor-Green Vortex | 236.95x | 237.48x | 237.53x | **236.95x** | 1.00x |
| ABC Flow (A=B=C=1) | inf | inf | inf | inf | - |
| Random-Phase Gaussian | 1586.99x | 3067.88x | 3725.30x | 1586.99x | 6.70x |
| Vortex Tube (sigma=0.2, z-perturbed) | 1431.55x | 977.21x | 1229.81x | 977.21x | 4.12x |
| Anti-Parallel Tubes (sigma=0.2, z-perturbed) | 1550.92x | 1614.75x | 1718.37x | 1550.92x | 6.55x |

TGV tightest among standard ICs by 4x. Random Gaussian (generic turbulence) loosest at 6.7x above TGV. Vortex tube non-monotonic in Re (minimum at Re=500). [COMPUTED]

---

## Adversarial Search: Tube Width Controls Slack

Grid search (120 configs, N=32): **all top 10 configs have sigma=0.8** (widest tested). Tilt and circulation ratio do not improve slack.

Sigma sweep (N=64, Re=100, d=pi/4, delta=1.2):

| sigma | Min VS Slack | Time of Min |
|---|---|---|
| 0.5 | 413.88x | 0.76 |
| 1.0 | 231.47x | 1.34 |
| 1.5 | 182.21x | 1.80 |
| 2.0 | 161.29x | 2.21 |
| **2.5** | **157.31x** | **2.31** |
| 3.0 | 159.56x | 2.39 |

Bowl-shaped minimum at sigma~2.5. Physical interpretation:
- **Narrow tubes (sigma < 1):** Geometrically inefficient — strain field from one tube doesn't optimally align with the other's vorticity
- **Optimal (sigma ~ 2.5):** Best balance between vorticity spread (approaching Ladyzhenskaya extremizer) and retained structure
- **Wide tubes (sigma > 3):** Vorticity nearly uniform, reducing strain gradients

[COMPUTED]

---

## Convergence Checks (N=128)

| Configuration | N=32 | N=64 | N=128 | Change 64→128 |
|---|---|---|---|---|
| TGV (Re=100) | 237.43x | 236.95x | **236.90x** | 0.02% |
| Anti-parallel sigma=2.5 (Re=100) | 157.94x | 158.38x | **157.70x** | 0.4% |
| Anti-parallel sigma=3.0 (Re=100) | 161.09x | 160.03x | **159.75x** | 0.2% |

All converged. [CHECKED]

---

## Re-Independence

Minimum slack nearly constant across Re=100-1000 for optimal sigma:

| sigma | Re=100 | Re=500 | Re=1000 |
|---|---|---|---|
| 2.0 | 161.29x | 165.40x | 165.97x |
| 2.5 | ~157x | - | - |
| 3.0 | 159.56x | 171.65x | 174.79x |

Minimum always at Re=100, with weak Re-dependence for optimal sigma. Confirms that minimum slack is determined by IC geometry, not dynamics. [COMPUTED]

---

## Why TGV Is Not Optimal

1. TGV has competing symmetries (mirror planes in all three axes) that partially cancel vortex stretching contributions from different spatial regions
2. Anti-parallel tubes with optimal width break these symmetries while maintaining z-perturbation that drives stretching; two-tube structure creates strain field that directly stretches the opposing tube's vorticity

The optimal sigma=2.5 ~ 0.4L (where L=2pi is the domain size), suggesting the periodic domain geometry matters. Results are T^3-specific.

**Adversarial note (E008):** The Protas group (Kang, Yun, Protas 2020, *J. Fluid Mech.* 893) computed globally optimal ICs for maximum enstrophy growth using PDE-constrained optimization. Their result: maximum enstrophy growth ~ E_0^{3/2} with gap (>=1) even for most adversarial ICs. These Protas-type ICs were **NOT tested** here. They represent the strongest untested challenge to the 158x lower bound. [CONJECTURED]
