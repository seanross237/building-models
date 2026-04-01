---
topic: BKM bound is tighter than Ladyzhenskaya for NS flows — ~80-226x advantage depending on constant choice
confidence: provisional
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-007, adversarial review exploration-008"
---

## Overview

The Beale-Kato-Majda (BKM) inequality bounds ||nabla u||_{L^inf} using pointwise vorticity information with only a logarithmic correction. Using an empirically calibrated constant (C_BKM ≈ 0.68), it achieves 1.05x slack — but this tightness is **partly an artifact of calibrating C to TGV data**. With the theoretical R^3 constant (C_BKM ≈ 0.24), the slack is ~3x, giving an advantage of **~80x** over Ladyzhenskaya (not 226x).

**Bottom line:** BKM is genuinely tighter than Ladyzhenskaya for NS flows, but the headline "226x advantage" is inflated. The real advantage is ~80x with theoretical constants. Additionally, the comparison is between different mathematical quantities (see Adversarial Review section).

## Adversarial Review (E008) — Key Corrections

### 1. Apples-to-Oranges Comparison (MOST SERIOUS)

BKM and Ladyzhenskaya bound **fundamentally different quantities**:
- **BKM slack** = ||nabla u||_{L^inf} / [C_BKM × ||omega||_{L^inf} × log_term] — a **pointwise supremum** comparison
- **Ladyzhenskaya VS slack** = [C_Lad × ||omega||^{3/2} × ||nabla omega||^{3/2}] / VS_actual — a **domain-integrated** quantity

A "226x advantage factor" comparing them is like comparing a ruler to a scale. BKM controls whether ||nabla u||_{L^inf} blows up; Ladyzhenskaya controls whether the volume-averaged vortex stretching becomes too large. No published paper makes this comparison.

### 2. BKM "1.05x Slack" Is Circular

The empirical C_BKM ≈ 0.68 was calibrated to TGV data (smallest value making the bound valid + 5% margin). The theoretical R^3 Biot-Savart kernel gives C ~ 3/(4pi) = 0.239. Ratio: 0.68/0.24 = 2.83x. With theoretical constant, BKM slack would be **~3x, not 1.05x**, and the advantage would be **~80x, not 226x**. The direction is correct but the headline number is misleading.

### 3. BKM Tightness Is Calderon-Zygmund Theory, Not NS-Specific

For any divergence-free field on T^3, CZ theory gives ||nabla u||_{L^inf} ~ ||omega||_{L^inf} × log(1 + ||omega||_{H^1}/||omega||_{L^2}). BKM near-tightness is a general mathematical fact about the Biot-Savart operator, not a special property of NS flows.

### 4. BKM Advantage Does Not Transfer to Regularity Theory

The reason Ladyzhenskaya seems "looser" is precisely because it works with weaker (L^2-based) norms that are easier to control analytically. BKM's tightness comes at the cost of needing L^inf control of vorticity — the very thing we don't know how to prove. The tighter bound is in a harder-to-use norm.

---

## Three-Bound Comparison

Three bounds for ||nabla u||_{L^inf} compared on Taylor-Green vortex DNS (N=48-64, Re=100-5000, T=5.0):

1. **Ladyzhenskaya chain (vortex stretching):** C_L^2 * ||omega||_{L^2}^{3/2} * ||nabla omega||_{L^2}^{3/2}. Minimum slack: **237x**.
2. **Agmon inequality:** C_Agmon * ||u||_{H^2}^{1/2} * ||u||_{H^3}^{1/2}. Minimum slack: **12.4x**.
3. **BKM inequality:** C_BKM * ||omega||_{L^inf} * (1 + log(1 + ||omega||_{H^1}/||omega||_{L^2})). Minimum slack: **1.05x**. [COMPUTED]

---

## BKM Constant Calibration

Empirically calibrated C_BKM (smallest value making bound valid at all timesteps + 5% safety margin):

| Re | max ratio (||grad u||_inf / (||omega||_inf * log_term)) | Calibrated C_BKM |
|---|---|---|
| 100 | 0.643 | 0.675 |
| 500 | 0.645 | 0.677 |
| 1000 | 0.646 | 0.679 |
| 5000 | 0.648 | 0.680 |

Theoretical R^3 Biot-Savart kernel gives C ~ 3/(4*pi) = 0.239. Empirical value is **~2.7x larger** — reasonable for periodic domain T^3 (additional contributions from periodic images). [COMPUTED]

---

## Key Results

| Re | Lad VS min slack | Agmon min slack | BKM min slack | BKM advantage (Lad/BKM) |
|---|---|---|---|---|
| 100 | 237.0 | 12.4 | 1.05 | 225.7 |
| 500 | 237.5 | 12.4 | 1.05 | 226.2 |
| 1000 | 237.5 | 12.4 | 1.05 | 226.2 |
| 5000 | 237.6 | 12.4 | 1.05 | 226.3 |

**Time-averaged comparison (BKM advantage grows with Re):**

| Re | BKM mean slack | BKM advantage (time-avg) |
|---|---|---|
| 100 | 1.67 | 221x |
| 500 | 1.98 | 342x |
| 1000 | 2.06 | 414x |
| 5000 | 2.13 | 535x |

[COMPUTED]

---

## Why BKM Is Tighter

BKM uses ||omega||_{L^inf} directly (pointwise vorticity information) with only a logarithmic correction (log term = 2.1-3.6 for smooth flows). For smooth flows, BKM is essentially ||grad u||_inf ~ ||omega||_inf. The Ladyzhenskaya chain loses from three independent sources:
- ~5-9x from Holder alignment/cancellation (exploration 004)
- ~31x from interpolation constant looseness (exploration 004)
- sqrt(2) from the symmetric factor

The minimum BKM slack is **Re-independent** (1.05 at all Re with empirical C), meaning the empirical C_BKM captures the actual ||nabla u||_inf vs ||omega||_inf * log(...) relationship to within 5%. With theoretical C, the 3x slack is also Re-independent. [COMPUTED]

---

## Implications

BKM is genuinely tighter than Ladyzhenskaya for tracking NS flow dynamics (~80x with theoretical constants). The intermittency analysis (see `conditional-vortex-stretching-bound.md`) explains WHY Ladyzhenskaya is loose (NS solutions are far from the optimizer). However, BKM tightness reflects CZ theory (general Biot-Savart property), while Ladyzhenskaya works with analytically controllable L^2 norms. The two criteria are complementary, not competing.

## Novelty Assessment (E008)

**PARTIALLY KNOWN.** The observation that BKM-type bounds are tighter than Ladyzhenskaya for typical flows is implicitly known (CZ theory gives sharp div-free bounds). The specific numerical quantification (~80-226x depending on constant choice) appears not to be in the literature, but the qualitative direction is expected from the theory.
