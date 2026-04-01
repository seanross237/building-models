---
topic: Gaussian effective Ladyzhenskaya constant scales as Re^{-3/8} for Kolmogorov spectra
confidence: verified
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-006"
---

## Overview

For fields with many random-phase Fourier modes, the Central Limit Theorem gives a Gaussian pointwise distribution. In this regime, the effective Ladyzhenskaya constant has an explicit formula depending only on the energy spectrum, with a clean Re^{-3/8} scaling for Kolmogorov turbulence.

**This is a TYPICAL-case property, not a worst-case bound.** NS solutions have phase correlations (intermittency) that create enhanced L⁴ concentration above Gaussian. See `spectral-ladyzhenskaya-negative-result.md` for why this cannot be used as a proof bound.

---

## Analytical Formula

**Gaussian regime (CLT):**

||f||_{L⁴} = 3^{1/4} ||f||_{L²}

giving the effective constant:

C_{L,eff} = 3^{1/4} × (Σ|f̂_k|²)^{3/8} / (Σ|k|²|f̂_k|²)^{3/8}

[COMPUTED — verified numerically at multiple spectral profiles and resolutions]

---

## Kolmogorov Spectrum: Asymptotic Formula

For |û_k|² ~ k^{-11/3} exp(-c(k/k_d)^{4/3}) with k_d = Re^{3/4}:

**C_{L,eff} ≈ 1.707 × Re^{-3/8}**

Derivation: In the large-Re limit, ||f||² → 6π (IR-dominated), ||∇f||² → 3π × Re (UV-dominated). [COMPUTED]

### Numerical Verification

| Re | C_{L,eff} (Gaussian) | C_{L,eff}/C_L | Slack reduction (4th power) |
|----|---------------------|---------------|----------------------------|
| 100 | 0.284 | 0.452 | 24× |
| 1,000 | 0.125 | 0.199 | 632× |
| 10,000 | 0.054 | 0.085 | 18,878× |
| 100,000 | 0.023 | 0.036 | 586,261× |

Asymptotic formula accuracy: 6.7% at Re=100, 2.1% at Re=1000, 0.2% at Re=100,000. [COMPUTED]

---

## Comparison to Measured NS Values

The GOAL.md reports measured C_eff ≈ 0.147 at Re~1000, vs. Gaussian prediction of 0.125. The phases add ~18% to concentration above Gaussian (intermittency). This confirms the Gaussian formula is a reasonable estimate for typical NS flows but NOT a bound. [COMPUTED]

---

## Band-Limited Numerical Results

Fields with Fourier support in |k| ∈ [k₀/2, 2k₀], 300 random-phase samples on T³ (N=32):

| k₀ | Modes | Mean C_eff | Analytical Gaussian | Error |
|----|-------|-----------|-------------------|-------|
| 2  | 256   | 0.569     | 0.560             | 2%    |
| 4  | 2082  | 0.335     | 0.333             | 1%    |
| 8  | 16823 | 0.198     | 0.198             | 0.0%  |

CLT accuracy improves with mode count. Verified at N=48 for k₀=4 (identical results). [COMPUTED, CHECKED]

---

## Slack Assessment

The Ladyzhenskaya inequality contributes 63% of the log-slack in the vortex stretching bound (total slack 158-237×). If the Gaussian C_{L,eff} were a valid bound at Re=1000, total slack would drop from ~200× to ~3.4×. At Re=10,000 it would drop below 1×, which is impossible — confirming the Gaussian approximation is too aggressive to serve as a bound. [COMPUTED]
