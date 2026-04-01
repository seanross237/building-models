---
topic: BMO/L^inf ratio ~0.27 — Kozono-Taniuchi criterion 4x tighter than standard L^inf blowup criterion
confidence: provisional
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-007, adversarial review exploration-008"
---

## Overview

The BMO (Bounded Mean Oscillation) norm of vorticity is consistently ~0.25-0.27 of the L^inf norm across Re=100-5000 for Taylor-Green vortex. This means the Kozono-Taniuchi blowup criterion (using ||omega||_{BMO} instead of ||omega||_{L^inf}) is **~4x tighter**. The ratio appears Re-stable across the tested range, but "universality" is not established (see Adversarial Caveats).

---

## BMO Computation Method

BMO norm = sup_B (1/|B|) int_B |f - f_B| dx, supremum over all balls B in T^3.

Computed by sampling balls at 5 radii (L/4, L/8, L/16, L/32, L/64, L=2*pi) with 150 random centers per radius, on every 5th diagnostic snapshot. Maximum mean oscillation across all balls. [COMPUTED]

---

## Results

| Re | ||omega||_{L^inf} mean | ||omega||_{BMO} mean | BMO/L^inf ratio |
|---|---|---|---|
| 100 | 2.53 | 0.617 | 0.250 |
| 500 | 6.07 | 1.646 | 0.272 |
| 1000 | 6.85 | 1.794 | 0.268 |
| 5000 | 7.65 | 1.933 | 0.265 |

Ratio stabilizes at **~0.27** for Re >= 500. [COMPUTED]

---

## Time Evolution (Re=1000)

| Time | ||omega||_{L^inf} | ||omega||_{BMO} | BMO/L^inf |
|---|---|---|---|
| 0.05 | 2.00 | 0.370 | 0.185 |
| 0.84 | 1.68 | 0.327 | 0.194 |
| 1.67 | 1.53 | 0.417 | 0.272 |
| 2.52 | 2.53 | 0.890 | 0.352 |
| 3.37 | 5.12 | 1.348 | 0.263 |
| 4.21 | 14.23 | 3.518 | 0.247 |
| 5.00 | 17.46 | 4.678 | 0.268 |

After initial transient, ratio stabilizes around 0.25-0.27. [COMPUTED]

---

## Key Findings

1. **Re-stable ratio (0.25-0.27 across Re=100-5000)** — a non-trivial finding suggesting universal BMO/L^inf structure in NS vorticity fields.

2. **BMO norm peaks at intermediate radii (L/8 to L/16)** — vorticity has greatest relative oscillation at intermediate scales, consistent with vortex filament structure.

3. **The BMO advantage compounds with BKM** — the Kozono-Taniuchi criterion uses BMO instead of L^inf in the BKM-type framework, potentially giving another 3-4x tightening beyond BKM's ~80x advantage (with theoretical constants). However, the 4x improvement is modest.

## Adversarial Caveats (E008)

1. **BMO computed by ball sampling, not exactly.** 150 random ball centers at 5 radii is a Monte Carlo approximation that **underestimates** the true BMO norm (~8% statistical error per radius). The 0.27 ratio is a lower bound on the true ratio.
2. **Single IC only (TGV).** Anti-parallel tubes (adversarially optimal for VS slack) might give a different BMO/L^inf ratio due to more concentrated vorticity. Not tested.
3. **Re range too narrow for "universality" claim.** Re=100-5000 spans laminar-to-transitional only. Fully turbulent flows (Re~10^5) with multi-scale coherent structures might show different ratios.
4. **Only 4 Re values.** Insufficient statistical support for a "universal" claim. The Re-stability may reflect limited structural variety in TGV specifically.
5. **Kozono-Taniuchi (2000)** shows L^inf strictly contains BMO, meaning for flows with very intermittent vorticity (extreme peaks surrounded by near-zero regions), BMO/L^inf could be much smaller than 0.27.

**Verdict (E008): INCONCLUSIVE.** The measurement is real but methodological limitations prevent claiming universality. [NOVEL — no published measurement of this ratio for NS flows was found]
