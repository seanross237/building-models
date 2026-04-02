"""Compute GUE Li coefficients at N=500, 1000, 3000, 5000 with matched scaling.
Each N-level uses N GUE eigenvalues scaled to [t_1, t_K] where K=N zeros are used.
Results saved individually per K level so partial progress is preserved.
"""
import numpy as np
import time
import json
import sys

def compute_lambda_gue_vec(t_values, n_val):
    """Vectorized GUE Li coefficient (float64 precision)."""
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

# Load zeros
zeros_5k = np.load('../exploration-008/t_zeros_5k.npy')
n_test = [100, 200, 300, 400, 500]

# Configuration: K -> number of trials
K_config = {
    500: 50,
    1000: 50,
    3000: 30,
    5000: 15,
}

all_results = {}

for K, N_trials in K_config.items():
    zeros_K = zeros_5k[:K]
    t_min_K, t_max_K = float(zeros_K[0]), float(zeros_K[-1])

    gue_results = {n: [] for n in n_test}
    print(f"\n{'='*60}")
    print(f"Computing GUE at K=N={K}, {N_trials} trials, range=[{t_min_K:.2f}, {t_max_K:.2f}]")
    print(f"{'='*60}", flush=True)

    t0_total = time.time()
    for trial in range(N_trials):
        rng = np.random.RandomState(trial + 999)
        evals = gen_gue_scaled(K, t_min_K, t_max_K, rng)
        for n in n_test:
            gue_results[n].append(compute_lambda_gue_vec(evals, n))
        if (trial + 1) % 10 == 0 or trial == 0:
            elapsed = time.time() - t0_total
            eta = elapsed / (trial + 1) * (N_trials - trial - 1)
            print(f"  Trial {trial+1}/{N_trials} done ({elapsed:.1f}s elapsed, ~{eta:.0f}s remaining)", flush=True)

    total_time = time.time() - t0_total
    print(f"  Completed K={K} in {total_time:.1f}s")

    # Compute statistics
    means = {}
    stds = {}
    stderrs = {}
    for n in n_test:
        arr = np.array(gue_results[n])
        means[n] = float(np.mean(arr))
        stds[n] = float(np.std(arr, ddof=1))
        stderrs[n] = stds[n] / np.sqrt(N_trials)

    # Save per-K results
    np.savez(f'gue_matched_K{K}.npz',
             n_values=n_test,
             means=[means[n] for n in n_test],
             stds=[stds[n] for n in n_test],
             stderrs=[stderrs[n] for n in n_test],
             N_GUE=K,
             N_REALIZATIONS=N_trials,
             all_trials={str(n): gue_results[n] for n in n_test})

    all_results[K] = {'means': means, 'stds': stds, 'stderrs': stderrs, 'N_trials': N_trials}

    # Print results for this K
    print(f"\n  Results for K=N={K}:")
    print(f"  {'n':>5} {'GUE mean':>12} {'GUE std':>10} {'GUE stderr':>10}")
    for n in n_test:
        print(f"  {n:>5} {means[n]:>12.4f} {stds[n]:>10.4f} {stderrs[n]:>10.4f}")
    sys.stdout.flush()

# Final summary
print(f"\n{'='*60}")
print(f"GUE COMPUTATION COMPLETE — SUMMARY")
print(f"{'='*60}")
print(f"\nGUE mean at n=500 across K=N levels:")
for K in sorted(all_results.keys()):
    r = all_results[K]
    print(f"  K=N={K:>5}: λ_500^GUE = {r['means'][500]:.4f} ± {r['stds'][500]:.4f} ({r['N_trials']} trials)")
