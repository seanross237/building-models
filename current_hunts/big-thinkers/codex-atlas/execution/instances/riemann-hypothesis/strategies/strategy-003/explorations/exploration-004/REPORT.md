# Exploration 004: N²/p Scaling Universality for Gauss Sum Matrices

## Goal

Test whether the Gauss sum matrix H_{jk} = Λ(|j-k|+1) × exp(2πijk/p) has a universal N²/p scaling law for its peak Brody β. Specifically: does N²/p_opt ≈ 275 hold for N ∈ {250, 500, 1000}?

---

## Task 1: Replicate N=500 Baseline

**Status:** COMPLETE — PASS

### Methodology Discovery

[CHECKED] The S002 target values (β=1.154 at p=809 etc.) were measured using the **Wigner interpolated** distribution P(s;β) = A s^β exp(-B s²), NOT the Brody distribution. This matters: the two distributions give systematically different β for the same data. The S002 methodology:
1. Degree-15 polynomial unfolding with eigenvalue normalization
2. Histogram-based least-squares fit (50 bins, s_max=4) to Wigner interpolated
3. No tail trimming

### Method Comparison (6 methods tested)

| Method | p=499 | p=809 | p=997 | Total |err| |
|--------|-------|-------|-------|------------|
| **Wigner Hist (no trim)** | 0.743 | **1.154** | **1.092** | **0.033** |
| Wigner MLE (no trim) | 0.694 | 1.041 | 0.946 | 0.341 |
| Brody MLE (no trim) | 0.776 | 1.010 | 0.959 | 0.278 |

[CHECKED] Wigner Hist (no trim) reproduces S002 targets to total error < 0.04.

### Baseline Results

| p | N²/p | β_W (Wigner) | β_B (Brody) | S002 target |
|---|------|-------------|-------------|-------------|
| 499 | 501.0 | 0.743 | 0.776 | 0.776 |
| 809 | 309.0 | **1.154** | 1.010 | **1.154** |
| 997 | 250.8 | **1.092** | 0.959 | **1.092** |

Pass criteria: β_W(p=809) = 1.154 ∈ [1.05, 1.25] ✓, β_W(p=499) = 0.743 ∈ [0.70, 0.85] ✓

Code: `code/task1_baseline_v3.py`

---

## Task 2: N=250 Sweep

**Status:** COMPLETE

Tested 26 primes spanning N²/p from 25 to 2717.

### Full Results (sorted by N²/p)

| p | N²/p | β_W | β_B | Notes |
|---|------|-----|-----|-------|
| 2503 | 25.0 | 0.599 | 0.700 | |
| 619 | 101.0 | 0.883 | 0.937 | |
| 503 | 124.3 | 0.715 | 0.898 | |
| 449 | 139.2 | 0.887 | 0.934 | |
| 397 | 157.4 | 0.842 | 0.858 | |
| 353 | 177.1 | 1.137 | 0.966 | Local high |
| 313 | 199.7 | 0.849 | 0.898 | |
| 293 | 213.3 | 0.704 | 0.769 | |
| 281 | 222.4 | 0.843 | 0.767 | |
| **277** | **225.6** | **1.318** | **1.137** | **PEAK** |
| 271 | 230.6 | 0.940 | 1.002 | |
| 263 | 237.6 | 1.087 | 1.033 | |
| 257 | 243.2 | 0.598 | 0.694 | Near p≈N |
| **251** | **249.0** | **0.080** | **0.347** | **p≈N ANOMALY** |
| 241 | 259.3 | 0.900 | 0.842 | |
| 239 | 261.5 | 0.896 | 0.919 | |
| 233 | 268.2 | 0.888 | 0.854 | |
| 223 | 280.3 | 0.603 | 0.803 | |
| 211 | 296.2 | 1.112 | 1.079 | Secondary high |
| 199 | 314.1 | 0.778 | 0.830 | |
| 179 | 349.2 | 0.632 | 0.744 | |
| 167 | 374.3 | 0.880 | 0.950 | |
| 149 | 419.5 | 0.952 | 0.997 | |
| 127 | 492.1 | 0.724 | 0.814 | |
| 61 | 1024.6 | 0.868 | 0.850 | |
| 23 | 2717.4 | 0.599 | 0.396 | |

[COMPUTED] **Peak: p=277, N²/p=225.6, β_W=1.318**

### Critical Observation: Extreme Scatter at N=250

The Wigner histogram fit with only ~249 spacings is highly unstable. Point-to-point variations of 0.3-0.5 between adjacent primes are common (e.g., p=277 → 1.318, p=281 → 0.843). The "peak" is determined primarily by noise rather than a smooth underlying curve. The p≈N anomaly at p=251 (β_W=0.080) confirms the resonance effect but makes it hard to determine the true peak position.

Code: `code/task2_n250_sweep.py`, `code/refine_sweeps.py`

---

## Task 3: N=1000 Sweep

**Status:** COMPLETE

Tested 19 primes spanning N²/p from 100 to 500.

### Full Results (sorted by N²/p)

| p | N²/p | β_W | β_B | Notes |
|---|------|-----|-----|-------|
| 9973 | 100.3 | 0.839 | 0.893 | |
| **4999** | **200.0** | **1.019** | **0.921** | **Wigner peak** |
| 4507 | 221.9 | 0.802 | 0.851 | |
| 4007 | 249.6 | 0.896 | 0.919 | |
| 3989 | 250.7 | 0.966 | 0.874 | |
| 3803 | 263.0 | 0.742 | 0.768 | |
| 3709 | 269.6 | 0.807 | 0.909 | |
| 3613 | 276.8 | 0.877 | 0.863 | |
| 3571 | 280.0 | 0.846 | 0.902 | |
| 3517 | 284.3 | 0.932 | 0.895 | |
| 3461 | 288.9 | 0.970 | 0.971 | Brody peak |
| **3407** | **293.5** | **1.012** | **0.949** | Secondary high |
| 3299 | 303.1 | 0.895 | 0.851 | |
| 3229 | 309.7 | 0.995 | 0.959 | N²/p≈310, matches N=500 |
| 3137 | 318.8 | 0.865 | 0.862 | |
| 3079 | 324.8 | 0.904 | 0.902 | |
| 2999 | 333.4 | 0.792 | 0.848 | |
| 2753 | 363.2 | 0.853 | 0.873 | |
| 1999 | 500.3 | 0.818 | 0.847 | |

[COMPUTED] **Wigner peak: p=4999, N²/p=200.0, β_W=1.019**
[COMPUTED] **Secondary high: p=3407, N²/p=293.5, β_W=1.012**
[COMPUTED] **Brody peak: p=3461, N²/p=288.9, β_B=0.971**

### Key Observation: Two Competing Peaks for N=1000

The N=1000 data shows two roughly equal β_W highs:
1. p=4999, N²/p=200.0, β_W=1.019
2. p=3407, N²/p=293.5, β_W=1.012

These are essentially tied within noise. The Brody MLE (more stable statistically) peaks near N²/p≈290-310 (p=3461: β_B=0.971), which is consistent with the N=500 peak location (N²/p=309).

Code: `code/task3_n1000_sweep.py`, `code/refine_sweeps.py`

---

## Task 4: Universality Assessment

### Summary Table

| N | p_opt (Wigner) | N²/p_opt | β_W_max | p_opt (Brody) | N²/p_opt (Brody) | β_B_max |
|---|----------------|----------|---------|---------------|-------------------|---------|
| 250 | 277 | 225.6 | 1.318 | 277 | 225.6 | 1.137 |
| 500 | 809 | 309.0 | 1.154 | 809 | 309.0 | 1.010 |
| 1000 | 4999 | 200.0 | 1.019 | 3461 | 288.9 | 0.971 |

### Is N²/p_opt ≈ 275 Universal?

**[COMPUTED] NO — the hypothesis is NOT supported by the data.**

The peak N²/p values across the three matrix sizes are:

| N | N²/p_opt (Wigner) | Ratio to 275 |
|---|-------------------|-------------|
| 250 | 225.6 | 0.82 |
| 500 | 309.0 | 1.12 |
| 1000 | 200.0 | 0.73 |

The values span a range of 200–309, with no convergence toward 275 or any other constant. The spread (ratio 0.73 to 1.12) represents a factor of 1.5× variation, far too large for a "universal" constant.

### Why the Scaling Law Fails

**1. Insufficient statistics at small N.** With N eigenvalues there are only ~N spacings. For N=250 that's ~249 spacings in a 50-bin histogram — fewer than 5 spacings per bin on average. The Wigner histogram fit is dominated by binning noise, producing point-to-point scatter of ΔβW ≈ 0.3–0.5 between adjacent primes.

**2. The p≈N resonance contaminates the peak region.** At p≈N, the matrix exhibits a dramatic anomalous collapse (β→0). For N=250, this anomaly at p=251 affects the entire N²/p≈240–260 region, distorting the landscape near the hypothesized peak at 275.

**3. The Brody MLE tells a more consistent story.** The Brody MLE, which is statistically more robust than histogram fitting, gives Brody-peak positions that are more consistent across N:
- N=250: β_B peak at p=277, N²/p=225.6
- N=500: β_B peak at p=809, N²/p=309.0
- N=1000: β_B peak at p=3461, N²/p=288.9

The N=500 and N=1000 Brody peaks (N²/p≈289–309) are mutually consistent, but N=250 remains an outlier, likely because 249 spacings are insufficient.

**4. Peak β_max is NOT increasing with N.** If there were a universal scaling, we'd expect β_max to either stabilize or increase with N. Instead:
- N=250: β_W=1.318 (unreliable due to noise)
- N=500: β_W=1.154 (well-determined)
- N=1000: β_W=1.019 (moderate confidence)

The *decrease* of β_max with increasing N is the opposite of what a convergent scaling law would predict. This strongly suggests that the N=500 peak of β_W=1.154 benefited from favorable noise, and the true signal is weaker.

### Verdict

[COMPUTED] The N²/p ≈ 275 universal scaling hypothesis is **REJECTED**. The evidence shows:

1. **Peak location is not universal** — N²/p_opt ranges from 200 to 309 across the three N values tested.
2. **Peak height decreases with N** — β_max goes from 1.32 → 1.15 → 1.02, suggesting the signal is noise-dominated.
3. **The fitting method matters** — Wigner histogram and Brody MLE give different peak locations and heights, indicating the "peak" is not a robust feature of the spacing distribution.
4. **A weaker claim is partially supported** — the Brody MLE peaks for N=500 and N=1000 are both near N²/p≈290–310, consistent with each other but not with 275 and not with N=250.

### What Would Be Needed to Salvage the Hypothesis

- **Much larger N** (N=5000 or N=10000) to get sufficient statistics for reliable fitting
- **Ensemble averaging** — multiple independent realizations per (N,p) point to reduce variance
- **Finer p-grid** — 50+ primes per N value in the candidate peak region
- **Robust fitting** — bootstrap confidence intervals on β to distinguish signal from noise
