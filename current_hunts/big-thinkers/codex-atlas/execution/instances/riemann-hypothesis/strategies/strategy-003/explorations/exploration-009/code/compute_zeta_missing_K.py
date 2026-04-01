"""Compute zeta Li coefficients at K=500, 1000, 3000 (missing from E008 cache)."""
import numpy as np
from mpmath import mp, mpc, re as mpre
import time

mp.dps = 25

def compute_lambda_zeta(n_val, zeros_imag):
    """Compute λ_n using zeros with imaginary parts in zeros_imag.
    λ_n = Σ_ρ [1 - (1 - 1/ρ)^n], summed over conjugate pairs:
    contribution = 2 - 2*Re[(1-1/ρ)^n]
    """
    total = mp.mpf(0)
    for t in zeros_imag:
        rho = mpc('0.5', str(t))
        power_val = (1 - 1/rho) ** n_val
        total += 2.0 - 2.0 * float(mpre(power_val))
    return float(total)

# Load zeros
zeros_5k = np.load('../exploration-008/t_zeros_5k.npy')
print(f"Loaded {len(zeros_5k)} zeros")

n_test = [100, 200, 300, 400, 500]
K_values = [500, 1000, 3000]

all_results = {}

for K in K_values:
    zeros_K = zeros_5k[:K]
    results = {}
    print(f"\n=== Computing zeta λ_n at K={K} (range [{zeros_K[0]:.2f}, {zeros_K[-1]:.2f}]) ===")
    t0_total = time.time()
    for n_val in n_test:
        t0 = time.time()
        lam = compute_lambda_zeta(n_val, zeros_K)
        elapsed = time.time() - t0
        results[n_val] = lam
        print(f"  λ_{n_val}^zeta (K={K}) = {lam:.6f}  [{elapsed:.1f}s]")
    total_time = time.time() - t0_total
    print(f"  Total time for K={K}: {total_time:.1f}s")
    all_results[K] = results

# Save results
for K in K_values:
    np.savez(f'zeta_li_K{K}.npz',
             n_values=n_test,
             lambda_values=[all_results[K][n] for n in n_test],
             K=K)
    print(f"\nSaved zeta_li_K{K}.npz")

# Print summary table
print(f"\n{'='*70}")
print(f"ZETA Li COEFFICIENTS SUMMARY")
print(f"{'='*70}")
print(f"{'n':>5}", end="")
for K in K_values:
    print(f"  {'K='+str(K):>12}", end="")
print()
for n in n_test:
    print(f"{n:>5}", end="")
    for K in K_values:
        print(f"  {all_results[K][n]:>12.4f}", end="")
    print()
