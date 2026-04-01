---
topic: N²/p universal scaling hypothesis REJECTED — peak varies 200–309 across matrix sizes
confidence: verified
date: 2026-03-28
source: "riemann-hypothesis strategy-003 exploration-004"
---

## Finding

The hypothesis that Gauss sum matrices H_{jk} = Λ(|j-k|+1) × exp(2πijk/p) have a **universal** N²/p scaling law for peak Brody β (with N²/p_opt ≈ 275) is **REJECTED** by multi-N testing.

### Summary Table

| N | p_opt (Wigner) | N²/p_opt | β_W_max | p_opt (Brody) | N²/p_opt (Brody) | β_B_max |
|---|----------------|----------|---------|---------------|-------------------|---------|
| 250 | 277 | 225.6 | 1.318 | 277 | 225.6 | 1.137 |
| 500 | 809 | 309.0 | 1.154 | 809 | 309.0 | 1.010 |
| 1000 | 4999 | 200.0 | 1.019 | 3461 | 288.9 | 0.971 |

### Why the Hypothesis Fails

1. **Peak location not universal:** N²/p_opt (Wigner) ranges from 200 to 309 — a factor 1.5× variation. No convergence toward 275 or any other constant.

2. **Peak β_max decreases with N:** β_W_max = 1.318 → 1.154 → 1.019 for N = 250, 500, 1000. The *decrease* of the signal with increasing N is the opposite of what a convergent scaling law predicts. Strongly suggests the N=500 peak of β_W=1.154 benefited from favorable noise.

3. **Fitting method matters:** Wigner histogram and Brody MLE give different peak locations and heights. The "peak" is not a robust feature of the spacing distribution. N=1000 Wigner peak is at N²/p=200 but Brody peak is at N²/p=289 — the methods don't agree.

4. **Insufficient statistics at small N:** With N eigenvalues there are only ~N spacings. For N=250, that's ~249 spacings in a 50-bin histogram — fewer than 5 spacings per bin. Point-to-point scatter of Δβ_W ≈ 0.3–0.5 between adjacent primes dominates the signal.

5. **p≈N resonance contaminates peak region:** At p≈N the matrix exhibits a dramatic β→0 anomaly (β_W=0.080 at p=251 for N=250). This distorts the entire N²/p ≈ 240–260 region near the hypothesized peak.

### Weaker Claim Partially Supported

The Brody MLE (statistically more robust than histogram fitting) gives somewhat consistent peak positions for N=500 and N=1000: N²/p ≈ 289–309. N=250 (N²/p=225.6) remains an outlier due to insufficient statistics. The defensible claim is: "for N ≥ 500, the Brody MLE peak appears near N²/p ≈ 290–310," but this is weaker than the universal constant hypothesis.

### Methodology Discovery: Wigner vs. Brody Fitting

[CHECKED] The S002 target values (β=1.154 at p=809 etc.) were measured using the **Wigner interpolated** distribution P(s;β) = A s^β exp(-B s²), NOT the Brody distribution. Six methods were tested against S002 targets; the Wigner histogram (no trim, 50 bins, s_max=4) with degree-15 polynomial unfolding reproduced S002 targets to total error < 0.04. This method identification was essential for valid cross-N comparison.

### What Would Be Needed to Salvage the Hypothesis

- Much larger N (N=5000+) for sufficient statistics
- Ensemble averaging — multiple independent realizations per (N,p) point
- Finer p-grid (50+ primes per N in the candidate peak region)
- Bootstrap confidence intervals on β to distinguish signal from noise

### Implications

The N²/p ≈ 250–310 observation from S002-E005 (N=500 only) remains **SUPPORTED as an empirical observation for N=500** — no prior literature documents this for the Gauss sum matrix class. But the word "universal" (N-independent) is **REJECTED**. The original novelty verdict should be qualified: "empirically observed for N=500; multi-N universality not supported."
