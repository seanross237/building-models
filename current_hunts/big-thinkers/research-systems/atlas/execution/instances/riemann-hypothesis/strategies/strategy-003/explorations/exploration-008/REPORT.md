# Exploration 008: Validate λ_n^zeta / λ_n^GUE Crossover — Novel Claim Confirmation

## Goal
Validate the E002 finding that λ_n^zeta / λ_n^GUE < 1 for n > ~272, using 5000 zeros and larger GUE matrices. Determine if this is a real signal or a finite-sample artifact.

**The central question:** When we match N_GUE = K_zeros at every scale (K = 500, 1000, 2000, 3000, 5000), does the ratio λ_n^zeta / λ_n^GUE at n=500 stay below 1, or does it converge to 1?

---

## Task 0: Setup and Zero Computation [COMPUTED]

**Working directory confirmed:** exploration-008

### Data Recovered from Prior Run:
- 5000 zeros computed, range: t₁ = 14.1347 to t₅₀₀₀ = 5447.8620
- Saved as `t_zeros_5k.npy` (5000 values) and `t_zeros_2k.npy` (first 2000)
- Li coefficients λ_n with 2000 zeros: saved in `li_zeta_2k.npz`
- Li coefficients λ_n with 5000 zeros: saved in `li_zeta_5k.npz`
- GUE Li coefficients at N=2000, 100 trials: saved in `gue_li_N2000_100trials.npz`

All data from the prior partial run is intact and usable.

---

## Task 1: Replicate E002 λ_n^zeta with 2000 zeros [VERIFIED]

Prior run confirmed: recomputed Li coefficients λ_n using the same 2000 zeros at 25-digit precision.

### Replication Table [VERIFIED]

| n | E008 recompute | E002 stored value | Match? |
|---|---------------|-------------------|--------|
| 1 | 0.0227 | 0.0227 | ✓ exact |
| 10 | 2.2351 | 2.2351 | ✓ exact |
| 50 | 42.4253 | (not reported) | — |
| 100 | 114.1806 | 114.1806 | ✓ exact |
| 200 | 288.9650 | 288.9650 | ✓ exact |
| 300 | 479.9058 | 479.9058 | ✓ exact |
| 400 | 677.5864 | 677.5864 | ✓ exact |
| 500 | 881.4252 | 881.4252 | ✓ exact |

**All values match E002's actual stored data to machine precision. Replication successful.** [VERIFIED]

**NOTE:** The GOAL.md stated λ_100^zeta = 59.72, which is incorrect — E002's actual stored value is 114.18. This appears to be a transcription error in the strategizer's context. Other reference values are correct.

### E002 Ratio Data (from stored files) [CHECKED]

| n | λ_n^zeta | λ_n^GUE (mean ± std) | Ratio |
|---|---------|----------------------|-------|
| 100 | 114.18 | 103.30 ± 0.53 | 1.105 |
| 200 | 288.97 | 279.39 ± 2.13 | 1.034 |
| 272 | — | — | 0.9997 (first < 1) |
| 300 | 479.91 | 482.57 ± 2.41 | 0.994 |
| 400 | 677.59 | 701.64 ± 3.23 | 0.966 |
| 500 | 881.43 | 929.10 ± 2.68 | 0.949 |

**Crossover confirmed at n ≈ 272 with the original E002 data.**

---

## Task 2: λ_n^zeta Convergence with Number of Zeros [COMPUTED]

### Convergence Study

Li coefficients using varying numbers of zeros:

| K zeros | λ_100 | λ_300 | λ_500 |
|---------|-------|-------|-------|
| 500 | 107.12 | 416.66 | 707.36 |
| 1000 | 111.41 | 455.01 | 812.56 |
| 1500 | 113.18 | 470.91 | 856.50 |
| 2000 | 114.18 | 479.91 | 881.43 |
| 3000 | 115.30 | 489.99 | 909.39 |
| 4500 | 116.15 | 497.63 | 930.60 |
| 5000 | 116.34 | 499.29 | 935.20 |

**Relative change from K=2000 to K=5000:** [COMPUTED]
- λ_100: +1.9%
- λ_300: +4.0%
- λ_500: +6.1%
- λ_1000: +11.4%

**The sum is NOT converged at 2000 zeros for large n.** Each block of ~1000 additional zeros adds ~2% to λ_500. This slow convergence is critical — it means the comparison to GUE is only valid when N_GUE = K_zeros exactly, using the same range.

---

## Task 3: GUE Li Coefficients — N=2000, 100 Realizations [COMPUTED]

Prior run computed GUE Li coefficients with N=2000, 100 realizations (20× more than E002's 5 trials).

### Results (N=2000, 100 realizations) [COMPUTED]

| n | λ_n^zeta | λ_n^GUE (mean) | GUE std | Ratio | (ζ−GUE)/σ |
|---|---------|---------------|---------|-------|-----------|
| 1 | 0.0227 | 0.0203 | 0.0019 | 1.114 | +1.2σ |
| 10 | 2.2351 | 2.0039 | 0.1837 | 1.115 | +1.3σ |
| 50 | 42.4253 | 37.5028 | 2.8231 | 1.131 | +1.7σ |
| 100 | 114.1806 | 103.0155 | 3.4719 | 1.108 | +3.2σ |
| 200 | 288.9650 | 277.5537 | 4.8095 | 1.041 | +2.4σ |
| 300 | 479.9058 | 480.0973 | 5.5736 | 1.000 | −0.03σ |
| 400 | 677.5864 | 699.6748 | 5.7322 | 0.968 | −3.9σ |
| 500 | 881.4252 | 925.6231 | 6.0855 | 0.952 | −7.3σ |

### Key Findings (N=K=2000):
1. **Crossover at n ≈ 300 confirmed** — ratio ≈ 1.000 right at n=300 [COMPUTED]
2. **Ratio at n=500 = 0.952** — matches E002's 0.949 closely [COMPUTED]
3. **Significance: 7.3σ below 1 at n=500** — NOT statistical noise [COMPUTED]
4. **For small n, zeta EXCEEDS GUE** by ~10-13% [COMPUTED]

### N-Dependence Study [COMPUTED]

GUE λ_n vs matrix dimension N (50 trials each, all scaled to [t₁, t₂₀₀₀]):

| N | λ_100^GUE | λ_500^GUE | Ratio at n=500 |
|---|----------|----------|---------------|
| 500 | 26.96 | 235.23 | 3.75 |
| 1000 | 52.67 | 465.43 | 1.89 |
| 2000 | 103.32 | 925.78 | 0.952 |
| 3000 | 153.28 | 1385.16 | 0.636 |

**GUE λ_n scales roughly linearly with N** — the comparison is only meaningful when N_GUE = K_zeros.

---

## Task 4: DEFINITIVE TEST — Matched N=K Comparison [COMPUTING]

**This is the critical test.** For each K = 500, 1000, 2000, 3000, 5000:
- Compute λ_n^zeta with exactly K zeros
- Compute λ_n^GUE with N=K GUE eigenvalues, scaled to [t₁, t_K]
- Report the ratio

If the ratio at n=500 is stable across K → the crossover is REAL.
If the ratio moves toward 1.0 as K increases → the crossover is an ARTIFACT.

**Results: PENDING (computing with code/definitive_matched_test.py)**

---
