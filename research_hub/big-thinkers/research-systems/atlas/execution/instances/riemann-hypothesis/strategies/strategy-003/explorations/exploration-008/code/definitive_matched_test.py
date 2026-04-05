"""
DEFINITIVE MATCHED TEST: λ_n^zeta(K zeros) vs λ_n^GUE(N=K, same range)

For each K in [500, 1000, 2000, 3000, 5000]:
  - Compute λ_n^zeta using first K zeros (high precision, mpmath)
  - Compute λ_n^GUE using N=K GUE eigenvalues scaled to [t_1, t_K]
  - Multiple GUE trials for statistics
  - Report ratio and significance

This is the definitive test for whether the crossover is real or a truncation artifact.
"""
import numpy as np
from mpmath import mp, mpc
import time
import sys
import json

mp.dps = 25

# Load all 5000 zeros
zeros_all = np.load('/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-008/t_zeros_5k.npy')
print(f"Total zeros available: {len(zeros_all)}")
print(f"Range: [{zeros_all[0]:.4f}, {zeros_all[-1]:.4f}]")

def compute_lambda_zeta_mp(n_val, t_array):
    """High-precision Li coefficient computation using mpmath."""
    total = mp.mpf(0)
    for t in t_array:
        rho = mpc('0.5', str(float(t)))
        power_val = (1 - 1/rho) ** n_val
        total += 2.0 - 2.0 * float(power_val.real)
    return float(total)

def compute_lambda_vectorized(t_values, n_val):
    """Vectorized Li coefficient (float64 precision) — fast for GUE."""
    t = np.array(t_values, dtype=np.float64)
    denom = 0.25 + t**2
    real_part = 1 - 0.5/denom   # Re(1 - 1/ρ)
    imag_part = t/denom          # Im(1 - 1/ρ)
    z = real_part + 1j * imag_part
    z_n = z ** n_val
    return np.sum(2.0 - 2.0 * np.real(z_n))

def gen_gue_scaled(N, t_min, t_max, rng):
    """Generate GUE(N) eigenvalues linearly scaled to [t_min, t_max]."""
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    evals = np.linalg.eigvalsh(H)
    ev_min, ev_max = evals.min(), evals.max()
    return t_min + (evals - ev_min) / (ev_max - ev_min) * (t_max - t_min)

# ============================================================
# First: verify vectorized vs mpmath agree for zeta zeros
# ============================================================
print("\n=== PRECISION CHECK: mpmath vs vectorized for zeta zeros ===")
zeros_test = zeros_all[:2000]
for n_val in [100, 300, 500]:
    mp_val = compute_lambda_zeta_mp(n_val, zeros_test[:200])  # small subset for speed
    vec_val = compute_lambda_vectorized(zeros_test[:200], n_val)
    rel_diff = abs(mp_val - vec_val) / abs(mp_val)
    print(f"  n={n_val}: mpmath={mp_val:.6f}, vectorized={vec_val:.6f}, rel_diff={rel_diff:.2e}")
    if rel_diff > 1e-6:
        print(f"  *** WARNING: precision issue at n={n_val}! Using mpmath for zeta. ***")

# ============================================================
# MATCHED COMPARISON
# ============================================================
K_values = [500, 1000, 2000, 3000, 5000]
n_test = [50, 100, 200, 300, 400, 500]

# Adaptive number of trials based on matrix size
def n_trials_for_K(K):
    if K <= 1000: return 100
    if K <= 2000: return 50
    if K <= 3000: return 30
    return 10  # 5000x5000 is expensive

all_results = {}

for K in K_values:
    if K > len(zeros_all):
        print(f"\nSkipping K={K}: only {len(zeros_all)} zeros available")
        continue

    zeros_K = zeros_all[:K]
    t_min_K = float(zeros_K[0])
    t_max_K = float(zeros_K[-1])
    n_trials = n_trials_for_K(K)

    print(f"\n{'='*70}")
    print(f"K = {K}, range = [{t_min_K:.2f}, {t_max_K:.2f}], {n_trials} GUE trials")
    print(f"{'='*70}")

    # Compute zeta Li coefficients with K zeros
    # For K <= 2000, use mpmath; for larger, use vectorized (check precision first)
    zeta_lam = {}
    t0 = time.time()

    if K <= 2000:
        print("  Computing ζ λ_n with mpmath (high precision)...")
        for n in n_test:
            zeta_lam[n] = compute_lambda_zeta_mp(n, zeros_K)
    else:
        # Check if vectorized is accurate enough
        # Test on subset with mpmath
        mp_check = compute_lambda_zeta_mp(500, zeros_K[:500])
        vec_check = compute_lambda_vectorized(zeros_K[:500], 500)
        rel = abs(mp_check - vec_check) / abs(mp_check)
        if rel < 1e-6:
            print(f"  Vectorized OK (rel_diff={rel:.2e}), using fast path...")
            for n in n_test:
                zeta_lam[n] = compute_lambda_vectorized(zeros_K, n)
        else:
            print(f"  Precision concern (rel_diff={rel:.2e}), using mpmath...")
            for n in n_test:
                zeta_lam[n] = compute_lambda_zeta_mp(n, zeros_K)

    zeta_time = time.time() - t0
    print(f"  ζ λ_n computed in {zeta_time:.1f}s")
    for n in n_test:
        print(f"    λ_{n}^ζ = {zeta_lam[n]:.4f}")

    # Compute GUE Li coefficients with N=K, matched scaling
    print(f"  Computing GUE λ_n (N={K}, {n_trials} trials)...")
    gue_results = {n: [] for n in n_test}
    t0 = time.time()

    for trial in range(n_trials):
        rng = np.random.RandomState(42 + trial)
        evals = gen_gue_scaled(K, t_min_K, t_max_K, rng)
        for n in n_test:
            lam = compute_lambda_vectorized(evals, n)
            gue_results[n].append(lam)

        if (trial + 1) % max(1, n_trials // 5) == 0:
            elapsed = time.time() - t0
            print(f"    Trial {trial+1}/{n_trials} [{elapsed:.1f}s]")

    gue_time = time.time() - t0
    print(f"  GUE computed in {gue_time:.1f}s")

    # Store and print results
    result_K = {}
    print(f"\n  {'n':>5} {'λ^ζ':>12} {'λ^GUE mean':>12} {'GUE std':>10} {'Ratio':>10} {'(ζ-G)/σ':>10}")
    for n in n_test:
        gue_arr = np.array(gue_results[n])
        gue_mean = float(np.mean(gue_arr))
        gue_std = float(np.std(gue_arr, ddof=1))
        gue_stderr = gue_std / np.sqrt(n_trials)
        ratio = zeta_lam[n] / gue_mean if gue_mean != 0 else float('nan')
        nsig = (zeta_lam[n] - gue_mean) / gue_std if gue_std > 0 else 0
        print(f"  {n:>5} {zeta_lam[n]:>12.4f} {gue_mean:>12.4f} {gue_std:>10.4f} {ratio:>10.6f} {nsig:>10.2f}")
        result_K[n] = {
            'zeta': zeta_lam[n],
            'gue_mean': gue_mean,
            'gue_std': gue_std,
            'gue_stderr': float(gue_stderr),
            'ratio': ratio,
            'n_sigma': float(nsig),
            'n_trials': n_trials
        }

    all_results[K] = result_K

# ============================================================
# SUMMARY TABLE: ratio at n=500 vs K
# ============================================================
print(f"\n{'='*70}")
print(f"SUMMARY: Ratio λ_n^ζ / λ_n^GUE at n=500 as function of K=N")
print(f"{'='*70}")
print(f"  {'K':>6} {'λ_500^ζ':>12} {'λ_500^GUE':>12} {'Ratio':>10} {'σ below 1':>10} {'Trials':>8}")
for K in K_values:
    if K in all_results and 500 in all_results[K]:
        r = all_results[K][500]
        sig_below = (1.0 - r['ratio']) / (r['gue_std'] / r['gue_mean']) if r['gue_mean'] != 0 else 0
        print(f"  {K:>6} {r['zeta']:>12.4f} {r['gue_mean']:>12.4f} {r['ratio']:>10.6f} {r['n_sigma']:>10.2f} {r['n_trials']:>8}")

print(f"\n{'='*70}")
print("VERDICT:")
print("If ratio is STABLE across K → signal is REAL")
print("If ratio moves toward 1.0 as K increases → ARTIFACT")
print(f"{'='*70}")

# Check trend
ratios_500 = []
K_list = []
for K in K_values:
    if K in all_results and 500 in all_results[K]:
        ratios_500.append(all_results[K][500]['ratio'])
        K_list.append(K)

if len(ratios_500) >= 3:
    # Simple linear regression of ratio vs K
    K_arr = np.array(K_list, dtype=float)
    r_arr = np.array(ratios_500)
    slope = np.polyfit(K_arr, r_arr, 1)[0]
    print(f"\nLinear trend: slope = {slope:.2e} per unit K")
    if slope > 0:
        print("  → Ratio INCREASES with K → crossover WEAKENS → likely ARTIFACT")
    else:
        print("  → Ratio DECREASES with K → crossover STRENGTHENS → likely REAL")

    # Extrapolate to K=inf? Not meaningful for linear, but show it
    print(f"\n  Ratio at K=500:  {ratios_500[0]:.6f}")
    print(f"  Ratio at K=5000: {ratios_500[-1]:.6f}")
    print(f"  Direction: {'toward 1' if abs(ratios_500[-1] - 1) < abs(ratios_500[0] - 1) else 'away from 1'}")

# Also show crossover n for each K
print(f"\n{'='*70}")
print(f"CROSSOVER ANALYSIS: At what n does ratio cross below 1?")
print(f"{'='*70}")
for K in K_values:
    if K not in all_results:
        continue
    crossover_n = None
    for n in sorted(all_results[K].keys()):
        if all_results[K][n]['ratio'] < 1.0:
            crossover_n = n
            break
    if crossover_n:
        print(f"  K={K}: crossover at n ≈ {crossover_n}")
    else:
        print(f"  K={K}: ratio NEVER drops below 1 (up to n=500)")

# Save all results
output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-008/matched_results.json'
# Convert to serializable format
save_results = {}
for K, data in all_results.items():
    save_results[str(K)] = {}
    for n, vals in data.items():
        save_results[str(K)][str(n)] = vals
with open(output_path, 'w') as f:
    json.dump(save_results, f, indent=2)
print(f"\nResults saved to {output_path}")

print("\n=== DEFINITIVE MATCHED TEST COMPLETE ===")
