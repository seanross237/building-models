---
topic: SU(3) H_norm extension — H_norm(I) = 1/27 and general N formula d/(4(d-1)N²)
confidence: verified
date: 2026-03-29
source: "yang-mills-validation exploration-005"
---

## Overview

Extension of the H_norm analysis from SU(2) to SU(3) reveals H_norm(I) = 1/27 for SU(3) d=4 — tighter than the predicted 1/18. The correct general formula is H_norm(I) = d/(4(d−1)N²), which has **N² in the denominator, not N**. Verified for 120+ random SU(3) configurations with zero violations.

## Key Result: H_norm(I) = 1/27 for SU(3) `[VERIFIED]`

At Q=I on L=2, d=4, SU(3):
- λ_max = 8β/3 = 2.66667 (difference from analytic: 5.77×10⁻¹⁵)
- H_norm(I) = 2.6667 / (72.0) = 1/27 = 0.037037

Eigenvalue spectrum: λ = 2.667 (×24), 2.000 (×96), 1.333 (×144), 0.667 (×96), 0 (×152).

## General N Formula `[VERIFIED for N=2,3]`

```
H_norm(I) = d / (4(d−1)N²)
```

| N | d | H_norm(I) | H_norm_CS | Ratio |
|---|---|-----------|-----------|-------|
| 2 | 4 | 1/12 = 0.0833 | 1/8 = 0.125 | 2/3 |
| 3 | 4 | 1/27 = 0.0370 | 1/18 = 0.0556 | 2/3 |
| N | 4 | 1/(3N²) | 1/(2N²) | 2/3 |

The ratio H_norm(I)/H_norm_CS = d/(2(d−1)) = 2/3 for d=4, independent of N.

## Numerical Evidence for H_norm ≤ 1/27 `[COMPUTED]`

120+ SU(3) random configurations (Haar measure): max H_norm = 0.03303 < 1/27.
10 adversarial configurations (including gradient ascent): max H_norm = 1/27 (flat only).
Gradient ascent from random Q converged to 0.03612, did not reach 1/27.

**Pattern:** All flat connections achieve H_norm = 1/27 exactly. All non-flat configs strictly below.

## Improved Thresholds for SU(3)

| Method | N=2, d=4 | N=3, d=4 |
|--------|----------|----------|
| SZZ Lemma 4.1 | β < 1/48 | β < 1/48 |
| CS bound (rigorous) | β < 1/6 | β < 3/8 |
| Conjectured tight | β < 1/4 | β < 9/16 |

## Correction: GOAL.md Formula Error

The validation goal predicted H_norm ≤ 1/18 for SU(3) (using N). The actual tight value is 1/27 (using N²). The N² scaling arises from: (1) the HessS prefactor β/(2N), and (2) the Bakry-Émery Ricci curvature N/2. Both factors involve N, so the threshold goes as N²/(8(d−1)).
