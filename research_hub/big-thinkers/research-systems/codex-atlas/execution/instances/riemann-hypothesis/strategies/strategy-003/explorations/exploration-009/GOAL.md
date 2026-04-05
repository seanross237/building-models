# Exploration 009: λ_n Ratio Convergence — Decisive Novel Claim Test

## CRITICAL: Confirm Working Directory First

**BEFORE ANYTHING ELSE:** Run `pwd` and `ls`.

Your working directory MUST be:
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-009/`

If not, run:
```bash
cd /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-009/
```
Then verify with `pwd`. Do not proceed until confirmed.

---

## Mission Context

This is the DECISIVE exploration for this strategy's main novel claim.

**The novel claim (E007):** λ_n^zeta/λ_n^GUE < 1 for n>272, ratio ≈ 0.949 at n=500. No prior literature compares these (novelty score 4/5).

**E008 complication:** The ratio at K=N=2000 is confirmed (7.3σ, 100 realizations). BUT the ratio is truncation-sensitive: it's only valid when N_GUE = K_zeros = same number. When K=4500 zeros were compared to N=2000 GUE (unfair), ratio = 1.005 > 1. The K=N=5000 matched test never completed.

**Your ONLY task:** Compute the matched ratio at multiple K=N levels and determine the TREND.

---

## The One Question to Answer

**Is the ratio λ_n^zeta(K) / λ_n^GUE(N=K) at n=500 converging toward 1 (artifact) or stabilizing at a constant < 1 (genuine signal) as K=N increases?**

---

## Data and Code Already Available — USE THESE

**All critical data in:**
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-008/`

Files to load (do NOT recompute):
```python
import numpy as np

# All 5000 zeros (the full dataset you need)
zeros_5k = np.load('../exploration-008/t_zeros_5k.npy')
# Verify: zeros_5k[0] ≈ 14.135, zeros_5k[4999] ≈ 5447

# Zeta Li coefficients ALREADY COMPUTED for K=2000 and K=5000
# Load from E008's cached files
import numpy as np
data_2k = np.load('../exploration-008/li_zeta_2k.npz')
data_5k = np.load('../exploration-008/li_zeta_5k.npz')
# Keys should include 'lambda_values' or similar — check with print(data_2k.files)

# GUE at N=2000 (100 trials) — already computed
gue_2k = np.load('../exploration-008/gue_li_N2000_100trials.npz')
# Check keys with print(gue_2k.files)

# Extend matched_comparison.py (already exists at ../exploration-008/code/matched_comparison.py)
```

**IMPORTANT:** Read `../exploration-008/code/matched_comparison.py` to understand the existing approach. You will EXTEND it, not rewrite it.

---

## Tasks

### Task 0: Setup (write to REPORT.md immediately)

1. Run `pwd` — confirm exploration-009
2. List files in `../exploration-008/`
3. Load the cached files and print their keys + shapes:
   - `t_zeros_5k.npy` — confirm 5000 zeros, print first and last
   - `li_zeta_2k.npz` and `li_zeta_5k.npz` — print file keys
   - `gue_li_N2000_100trials.npz` — print file keys

**Write Task 0 to REPORT.md NOW. Then proceed.**

### Task 1: Extract Cached Values

From the E008 files, extract the λ_n^zeta values at n=100, 200, 300, 400, 500 for:
- K=2000 zeros (from li_zeta_2k.npz)
- K=5000 zeros (from li_zeta_5k.npz)

And from gue_li_N2000_100trials.npz, extract:
- λ_n^GUE mean and std at n=100, 200, 300, 400, 500 for N=2000

If the cached files don't have exactly these values, load them and compute from the stored data. Worst case: recompute zeta λ_n from zeros_5k at the needed n values (should take <10 min total at 25-digit precision).

**Produce this table before moving to Task 2:**

| K zeros | n=100 | n=200 | n=300 | n=400 | n=500 |
|---------|-------|-------|-------|-------|-------|
| K=2000 | ? | ? | ? | ? | ? |
| K=5000 | ? | ? | ? | ? | ? |

**Write Task 1 to REPORT.md NOW. Then proceed.**

### Task 2: Compute GUE at New K=N Levels

You need GUE λ_n for the missing levels. Use this code:

```python
from mpmath import mp, mpc
import numpy as np

mp.dps = 15  # 15 digits sufficient for GUE (eigenvalues are float64)

def compute_lambda_gue_vec(t_values, n_val):
    """Vectorized GUE Li coefficient."""
    t = np.array(t_values, dtype=np.float64)
    denom = 0.25 + t**2
    real_part = 1 - 0.5/denom
    imag_part = t/denom
    z = real_part + 1j * imag_part
    z_n = z ** n_val
    return np.sum(2.0 - 2.0 * np.real(z_n))

def gen_gue_scaled(N, t_min, t_max, rng):
    """Generate GUE eigenvalues scaled to [t_min, t_max]."""
    A = (rng.randn(N, N) + 1j * rng.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    evals = np.linalg.eigvalsh(H)
    ev_min, ev_max = evals.min(), evals.max()
    return t_min + (evals - ev_min) / (ev_max - ev_min) * (t_max - t_min)

zeros_5k = np.load('../exploration-008/t_zeros_5k.npy')
n_test = [100, 200, 300, 400, 500]

# Load K=2000 GUE (already have 100 trials)
# Just load from gue_li_N2000_100trials.npz

# Compute for:
# K=N=500 (fast: use 50 trials)
# K=N=1000 (use 50 trials)
# K=N=3000 (use 30 trials — ~3 min)
# K=N=5000 (use 15 trials — ~10 min)

K_values_to_compute = [500, 1000, 3000, 5000]

for K in K_values_to_compute:
    zeros_K = zeros_5k[:K]  # First K zeros
    t_min_K, t_max_K = zeros_K[0], zeros_K[-1]
    N_trials = 50 if K <= 1000 else (30 if K == 3000 else 15)

    gue_results = {n: [] for n in n_test}
    print(f"Computing K=N={K}, {N_trials} trials...", flush=True)
    import time; t0 = time.time()
    for trial in range(N_trials):
        rng = np.random.RandomState(trial + 999)
        evals = gen_gue_scaled(K, t_min_K, t_max_K, rng)
        for n in n_test:
            gue_results[n].append(compute_lambda_gue_vec(evals, n))
    print(f"  Done in {time.time()-t0:.1f}s", flush=True)

    # Save results
    out_means = {n: np.mean(gue_results[n]) for n in n_test}
    out_stds = {n: np.std(gue_results[n], ddof=1) for n in n_test}
    np.savez(f'gue_matched_K{K}.npz', means=list(out_means.values()),
             stds=list(out_stds.values()), n_values=n_test)

    # Print immediately (write to REPORT.md after each K)
    print(f"\nK=N={K} results at n=500: GUE mean={out_means[500]:.2f} ± {out_stds[500]:.2f}")
```

**CRITICAL: Write results to REPORT.md after EACH K level, before computing the next one. Do not batch.**

**Timeout hints:**
- K=500, K=1000: should complete in <5 min total
- K=3000: ~3-5 min
- K=5000: ~10-15 min total — if this times out after 10 min, save partial results and proceed

**Write Task 2 to REPORT.md NOW after each K computation. Then proceed.**

### Task 3: Build the Trend Table and Verdict

Assemble all results into the final convergence table:

| K=N | λ_500^zeta | λ_500^GUE (mean ± std) | Ratio | Crossover n |
|-----|-----------|------------------------|-------|-------------|
| 500 | ? | ? ± ? | ? | ? |
| 1000 | ? | ? ± ? | ? | ? |
| 2000 | 881.43 | 929.10 ± 6.09 | 0.949 | ~272 |
| 3000 | ? | ? ± ? | ? | ? |
| 5000 | 935.20 | ? ± ? | ? | ? |

**Critical analysis:**
1. Plot (in text): is the ratio at n=500 INCREASING toward 1 as K=N grows, or STABLE/DECREASING?
2. What is the slope? If ratio goes 0.949 → 0.95x → 0.96x → ... → 1.0, that's an artifact. If 0.949 → 0.948 → 0.946 → ..., that's a stable signal.
3. Is the crossover point (where ratio first < 1) also moving? If crossover moves to larger n as K=N increases, that's an artifact indicator.

**Verdict:**
- **CONFIRMED**: Ratio at K=N=5000 still < 0.96, stable across K=N levels → genuine signal
- **ARTIFACT**: Ratio at K=N=5000 approaches 1.0 (within 2σ of 1.0) → truncation artifact
- **INCONCLUSIVE**: Too few data points or large variance to determine trend

**Write Task 3 to REPORT.md NOW. Then write REPORT-SUMMARY.md.**

---

## REPORT-SUMMARY.md Format

Write 150-200 words covering:
1. Outcome (CONFIRMED / ARTIFACT / INCONCLUSIVE)
2. Ratio trend table (2-3 key K=N levels)
3. Statistical significance at K=N=5000 (or largest tested)
4. Final verdict on the novel claim
5. What would be needed for definitive confirmation if inconclusive

---

## Success / Failure Criteria

**SUCCESS:** Ratio at K=N=5000 is still ≤ 0.96 at n=500 and trend is stable or decreasing. Novel claim confirmed — the crossover is a genuine structural property, not a truncation artifact.

**PARTIAL:** Ratio at K=N=5000 is 0.97-0.99 — signal present but weaker. Novel claim survives with qualification: "at finite K=N, zeta Li coefficients are systematically below GUE by 1-3%."

**FAILURE:** Ratio at K=N=5000 is ≥ 0.99 or within 2σ of 1.0 — truncation artifact. The novel claim does NOT survive. This is a valid negative result.

**INCONCLUSIVE:** K=N=5000 computation timed out and we only have K=N≤3000 — report what we have and note the limitation.

---

## Scope Warnings

- **DO NOT replicate E008** — it's already done. Just load the cached files.
- **DO NOT recompute zeta λ_n** — use the cached li_zeta_5k.npz values.
- **ONE GOAL ONLY**: the matched ratio convergence table. Nothing else.
- **scipy.optimize BROKEN** — don't try to use it
- **If K=N=5000 computation is too slow**: run 10 trials (not 15) and use that
- **Write after EACH K level** — the strategizer monitors REPORT.md line count

---

## Key Background Values (VERIFIED by E008)

| Source | Value | Verified? |
|--------|-------|-----------|
| λ_100^zeta (K=2000 zeros) | 114.18 | [VERIFIED] |
| λ_200^zeta (K=2000 zeros) | 288.97 | [VERIFIED] |
| λ_500^zeta (K=2000 zeros) | 881.43 | [VERIFIED] |
| λ_500^zeta (K=5000 zeros) | 935.20 | [COMPUTED] |
| λ_500^GUE (N=2000, 100 trials) | 929.10 ± 6.09 | [COMPUTED] |
| Ratio at K=N=2000, n=500 | 0.949 | [COMPUTED] |
| Significance at K=N=2000, n=500 | 7.3σ | [COMPUTED] |
| Crossover point (K=N=2000) | n≈272 | [COMPUTED] |
