# Exploration 009: λ_n Ratio Convergence — Decisive Novel Claim Test

## Goal

Determine whether the λ_n^zeta/λ_n^GUE crossover ratio is a genuine signal or truncation artifact by computing the matched ratio at multiple K=N levels (500, 1000, 2000, 3000, 5000).

**The key question:** Is the ratio at n=500 converging toward 1 (artifact) or stabilizing below 1 (genuine signal) as K=N increases?

---

## Task 0: Setup and Data Verification

**Working directory confirmed:** `exploration-009/`

### Cached Files from E008

| File | Contents | Status |
|------|----------|--------|
| `t_zeros_5k.npy` | 5000 zeros, shape (5000,), range [14.134725, 5447.861998] | Loaded |
| `li_zeta_2k.npz` | λ_n^zeta at K=2000 for n=1,10,50,100,200,300,400,500 | Loaded |
| `li_zeta_5k.npz` | λ_n^zeta at K=2000 and K=5000 for n=100..1000 | Loaded |
| `gue_li_N2000_100trials.npz` | GUE λ_n at N=2000, 100 trials, n=1..500 | Loaded |

---

## Task 1: Zeta λ_n at All K Levels

Computed zeta Li coefficients from cached zeros at K=500, 1000, 3000 using mpmath at 25-digit precision (code: `code/compute_zeta_missing_K.py`). Combined with cached K=2000 and K=5000 from E008.

### Complete Zeta λ_n Table [COMPUTED]

| n | K=500 | K=1000 | K=2000 | K=3000 | K=5000 |
|---|-------|--------|--------|--------|--------|
| 100 | 107.120 | 111.409 | 114.181 | 115.302 | 116.335 |
| 200 | 260.773 | 277.887 | 288.965 | 293.448 | 297.583 |
| 300 | 416.657 | 455.012 | 479.906 | 489.988 | 499.288 |
| 400 | 565.602 | 633.410 | 677.586 | 695.498 | 712.027 |
| 500 | 707.363 | 812.559 | 881.425 | 909.388 | 935.203 |

**Observation:** Zeta λ_n grows monotonically with K at all n values — each additional zero contributes positively. Growth is sublinear and decelerating.

---

## Task 2: GUE at All K=N Levels

Computed GUE Li coefficients at N=500, 1000, 3000, 5000 using N×N GUE matrices with eigenvalues linearly scaled to [t_1, t_K] (code: `code/compute_gue_all_K.py`). Used K=N=2000 data from E008 cache (100 trials).

### K=N=500 (50 trials, 4.1s) [COMPUTED]

| n | GUE mean | GUE std |
|---|----------|---------|
| 100 | 117.530 | 3.373 |
| 200 | 292.732 | 4.450 |
| 300 | 472.992 | 3.955 |
| 400 | 642.844 | 4.479 |
| 500 | 796.245 | 3.991 |

### K=N=1000 (50 trials, 32.6s) [COMPUTED]

| n | GUE mean | GUE std |
|---|----------|---------|
| 100 | 112.502 | 3.284 |
| 200 | 293.861 | 4.217 |
| 300 | 494.975 | 4.711 |
| 400 | 700.644 | 5.721 |
| 500 | 904.720 | 5.465 |

### K=N=2000 (100 trials, from E008 cache) [COMPUTED]

| n | GUE mean | GUE std |
|---|----------|---------|
| 100 | 103.015 | 3.472 |
| 200 | 277.554 | 4.810 |
| 300 | 480.097 | 5.574 |
| 400 | 699.675 | 5.732 |
| 500 | 925.623 | 6.086 |

### K=N=3000 (30 trials, 528.7s) [COMPUTED]

| n | GUE mean | GUE std |
|---|----------|---------|
| 100 | 96.339 | 3.396 |
| 200 | 262.512 | 4.882 |
| 300 | 461.022 | 5.943 |
| 400 | 677.349 | 5.337 |
| 500 | 906.078 | 6.387 |

### K=N=5000 (15 trials, 1147.6s) [COMPUTED]

| n | GUE mean | GUE std |
|---|----------|---------|
| 100 | 86.704 | 4.040 |
| 200 | 240.113 | 5.534 |
| 300 | 426.257 | 6.680 |
| 400 | 634.636 | 7.935 |
| 500 | 858.186 | 7.918 |

### Critical Anomaly: GUE λ_n DECREASES with N at small n

| K=N | GUE λ_100 | Zeta λ_100 | GUE λ_500 | Zeta λ_500 |
|-----|-----------|------------|-----------|------------|
| 500 | 117.53 | 107.12 | 796.25 | 707.36 |
| 1000 | 112.50 | 111.41 | 904.72 | 812.56 |
| 2000 | 103.02 | 114.18 | 925.62 | 881.43 |
| 3000 | 96.34 | 115.30 | 906.08 | 909.39 |
| 5000 | 86.70 | 116.34 | 858.19 | 935.20 |

**GUE λ_100 drops from 117.5 to 86.7 as N goes from 500 to 5000, while zeta λ_100 grows from 107.1 to 116.3.** This divergent behavior is a clear diagnostic that the linear scaling method introduces systematic K-dependent bias.

---

## Task 3: Final Convergence Table and Verdict

### The Decisive Table: Ratio at n=500 [COMPUTED]

| K=N | λ_500^zeta | λ_500^GUE (mean ± std) | Ratio | (ζ-GUE)/σ |
|-----|-----------|------------------------|-------|-----------|
| 500 | 707.36 | 796.25 ± 3.99 | **0.888** | -22.3σ |
| 1000 | 812.56 | 904.72 ± 5.47 | **0.898** | -16.9σ |
| 2000 | 881.43 | 925.62 ± 6.09 | **0.952** | -7.3σ |
| 3000 | 909.39 | 906.08 ± 6.39 | **1.004** | +0.5σ |
| 5000 | 935.20 | 858.19 ± 7.92 | **1.090** | +9.7σ |

### Full Ratio Table (zeta/GUE) Across All n [COMPUTED]

| K=N | n=100 | n=200 | n=300 | n=400 | n=500 |
|-----|-------|-------|-------|-------|-------|
| 500 | 0.911 | 0.891 | 0.881 | 0.880 | 0.888 |
| 1000 | 0.990 | 0.946 | 0.919 | 0.904 | 0.898 |
| 2000 | 1.108 | 1.041 | 1.000 | 0.968 | 0.952 |
| 3000 | 1.197 | 1.118 | 1.063 | 1.027 | 1.004 |
| 5000 | 1.342 | 1.239 | 1.171 | 1.122 | 1.090 |

### Trend Analysis

**1. Ratio at n=500 is monotonically INCREASING:**
```
K=N:    500  → 1000 → 2000 → 3000 → 5000
Ratio: 0.888 → 0.898 → 0.952 → 1.004 → 1.090
```
The ratio crosses 1.0 between K=N=2000 and K=N=3000, and reaches 1.09 at K=N=5000. The trend is **accelerating away from 1.0** in the positive direction, not stabilizing below it.

**2. The crossover point DISAPPEARS at larger K=N:**
- K=N=500: All ratios < 1 (zeta below GUE at all tested n)
- K=N=1000: All ratios < 1
- K=N=2000: Crossover at n≈300 (ratio < 1 for n > 300)
- K=N=3000: All ratios > 1 (zeta ABOVE GUE at all tested n)
- K=N=5000: All ratios > 1, with large excess (9-34%)

**3. Root cause: broken GUE scaling.**
The linear scaling method maps N GUE eigenvalues (semicircle distribution) to the range [t_1, t_K]. As K=N grows:
- The range widens (811 → 5448), spreading the semicircle over a larger interval
- The semicircle concentrates eigenvalues near the center at large t, where each contributes ~2 to λ_n (oscillating phase)
- But the number of eigenvalues near small t (where contributions are largest at small n) does NOT grow proportionally
- Meanwhile, zeta zeros have logarithmically growing density, so their count near any fixed t does grow

This density mismatch causes GUE λ_n to saturate or decrease at small n while zeta λ_n monotonically increases. The ratio is therefore a smooth function of K that crosses 1.0 at some K-dependent point, not a structural property.

### Verdict: ARTIFACT [COMPUTED]

**The crossover ratio λ_n^zeta/λ_n^GUE < 1 is a truncation artifact.**

Evidence:
1. The ratio at n=500 crosses from < 1 to > 1 as K=N increases past ~2500
2. At K=N=5000, the ratio is 1.090 (9.7σ ABOVE 1, not below)
3. The crossover point itself vanishes at K=N ≥ 3000
4. The GUE comparison is not self-consistent: GUE λ_100 decreases with N (117 → 87) while zeta λ_100 increases (107 → 116)

**The novel claim from E007 (ratio ≈ 0.949 at n=500, crossover at n≈272) does NOT survive.** It is specific to the K=N=2000 comparison and reverses at larger K=N. This matches the artifact diagnosis from the GOAL: "If ratio goes 0.949 → 0.95x → 0.96x → ... → 1.0, that's an artifact."

---

## Artifacts

All code and data are in:
- `code/compute_zeta_missing_K.py` — Zeta Li coefficients at K=500, 1000, 3000
- `code/compute_gue_all_K.py` — GUE Li coefficients at N=500, 1000, 3000, 5000
- `zeta_li_K{500,1000,3000}.npz` — Saved zeta results
- `gue_matched_K{500,1000,3000,5000}.npz` — Saved GUE results
