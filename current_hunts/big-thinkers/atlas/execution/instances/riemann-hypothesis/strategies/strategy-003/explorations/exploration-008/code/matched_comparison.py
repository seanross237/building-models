"""
DEFINITIVE TEST: Match N_GUE = K_zeros and scale to same range.

For each K in [2000, 3000, 4500]:
  - Compute λ_n^zeta using first K zeros
  - Compute λ_n^GUE using N=K GUE eigenvalues scaled to [t_1, t_K]
  - Compute ratio λ_n^zeta / λ_n^GUE

If the ratio is stable across K, the signal is real.
If the ratio moves toward 1 as K increases, it's a truncation artifact.
"""
import numpy as np
from mpmath import mp, mpc
import time

mp.dps = 25

# Load all available zeros
zeros_all = np.load('t_zeros_progress.npy')
print(f"Total zeros available: {len(zeros_all)}")

def compute_lambda_zeta(n_val, t_array):
    """High-precision Li coefficient computation."""
    total = 0.0
    for t in t_array:
        rho = mpc('0.5', str(t))
        power_val = (1 - 1/rho) ** n_val
        total += 2.0 - 2.0 * float(power_val.real)
    return total

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
    A = (rng.randn(N, N) + 1j * rng.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    evals = np.linalg.eigvalsh(H)
    ev_min, ev_max = evals.min(), evals.max()
    return t_min + (evals - ev_min) / (ev_max - ev_min) * (t_max - t_min)

# ============================================================
# Test with matched K
# ============================================================
K_values = [1000, 2000, 3000, 4500]
n_test = [100, 200, 300, 400, 500]
N_TRIALS = 30  # Use fewer trials since matrices are larger

print(f"\n{'='*70}")
print(f"MATCHED COMPARISON: N_GUE = K_zeros, same scaling range")
print(f"{'='*70}")

for K in K_values:
    if K > len(zeros_all):
        print(f"\nSkipping K={K}: only {len(zeros_all)} zeros available")
        continue

    zeros_K = zeros_all[:K]
    t_min_K = zeros_K[0]
    t_max_K = zeros_K[-1]

    print(f"\n--- K = {K}, range = [{t_min_K:.2f}, {t_max_K:.2f}] ---")

    # Compute zeta Li coefficients with K zeros
    zeta_lam = {}
    t0 = time.time()
    for n in n_test:
        zeta_lam[n] = compute_lambda_zeta(n, zeros_K)
    zeta_time = time.time() - t0
    print(f"  Zeta λ_n computed in {zeta_time:.1f}s")

    # Compute GUE Li coefficients with N=K, matched scaling
    gue_results = {n: [] for n in n_test}
    t0 = time.time()
    for trial in range(N_TRIALS):
        rng = np.random.RandomState(42 + trial)
        evals = gen_gue_scaled(K, t_min_K, t_max_K, rng)
        for n in n_test:
            lam = compute_lambda_gue_vec(evals, n)
            gue_results[n].append(lam)
    gue_time = time.time() - t0
    print(f"  GUE λ_n computed in {gue_time:.1f}s ({N_TRIALS} trials)")

    # Results
    print(f"\n  {'n':>5} {'λ^zeta':>12} {'λ^GUE mean':>12} {'GUE std':>10} {'Ratio':>10} {'(ζ-G)/σ':>10}")
    for n in n_test:
        gue_arr = np.array(gue_results[n])
        gue_mean = np.mean(gue_arr)
        gue_std = np.std(gue_arr, ddof=1)
        ratio = zeta_lam[n] / gue_mean
        nsig = (zeta_lam[n] - gue_mean) / gue_std if gue_std > 0 else 0
        print(f"  {n:>5} {zeta_lam[n]:>12.4f} {gue_mean:>12.4f} {gue_std:>10.4f} {ratio:>10.6f} {nsig:>10.2f}")

# ============================================================
# Summary: ratio at n=500 vs K
# ============================================================
print(f"\n{'='*70}")
print(f"SUMMARY: Is the crossover an artifact?")
print(f"{'='*70}")
print("If ratio at n=500 moves toward 1.0 as K increases → ARTIFACT")
print("If ratio at n=500 stays ~0.95 as K increases → REAL SIGNAL")

print("\n=== MATCHED COMPARISON COMPLETE ===")
