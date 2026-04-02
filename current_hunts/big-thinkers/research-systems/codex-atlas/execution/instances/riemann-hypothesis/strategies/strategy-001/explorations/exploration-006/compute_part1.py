"""
Part 1: Von Mangoldt Toeplitz Matrix Construction and Eigenvalue Analysis
Part 2: Statistical Analysis of Eigenvalues (GUE/GOE/Poisson comparison)
"""
import numpy as np
from sympy import isprime, factorint
import time
import json

# ---- Arithmetic functions ----

def von_mangoldt(n):
    """Lambda(n) = ln(p) if n = p^k for some prime p and k>=1, else 0."""
    if n <= 0:
        return 0.0
    if n == 1:
        return 0.0
    factors = factorint(n)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        return float(np.log(p))
    return 0.0

# Precompute von Mangoldt values up to N_max
N_max = 1001
print(f"Precomputing von Mangoldt function for n=1..{N_max}...")
t0 = time.time()
Lambda = np.array([von_mangoldt(n) for n in range(N_max + 1)])  # Lambda[0] unused
print(f"  Done in {time.time()-t0:.2f}s")

# ---- Part 1: Construct Toeplitz matrices and compute eigenvalues ----

def build_toeplitz(a_func_values, N, diag_val=0.0):
    """Build symmetric Toeplitz matrix T where T_{ij} = a(|i-j|+1) for i!=j, T_{ii} = diag_val."""
    # a_func_values[k] = a(k) for k >= 0
    T = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                T[i, j] = diag_val
            else:
                T[i, j] = a_func_values[abs(i - j) + 1]
    return T

# But building with loops is slow for N=1000. Use vectorized approach.
def build_toeplitz_fast(a_values, N, diag_val=0.0):
    """Build symmetric Toeplitz matrix using scipy."""
    from scipy.linalg import toeplitz
    # First row: T[0,j] = a(|0-j|+1) for j!=0, T[0,0] = diag_val
    first_row = np.zeros(N)
    first_row[0] = diag_val
    for j in range(1, N):
        first_row[j] = a_values[j + 1]  # a(|0-j|+1) = a(j+1) ... wait
    # T_{ij} = a(|i-j|+1). For i=0: T_{0,j} = a(j+1) for j>=1
    # Actually: T_{0,0} = diag_val, T_{0,1} = a(2), T_{0,2} = a(3), ..., T_{0,N-1} = a(N)
    first_row[0] = diag_val
    for j in range(1, N):
        first_row[j] = a_values[j + 1]
    # Wait, let me re-check. T_{ij} = a(|i-j|+1).
    # For i=0, j=0: |0-0|+1 = 1, but we set diagonal separately.
    # For i=0, j=1: |0-1|+1 = 2, so a(2)
    # For i=0, j=2: |0-2|+1 = 3, so a(3)
    # OK so first_row[j] = a(j+1) for j>=1. That means we need a up to N+1.
    # But Lambda is precomputed up to N_max+1, so for N=1000, we need a(1001) which is fine.

    T = toeplitz(first_row)
    return T

results = {}

for N in [200, 500, 1000]:
    print(f"\n=== Von Mangoldt Toeplitz, N={N} ===")
    t0 = time.time()

    # Build matrix
    T = build_toeplitz_fast(Lambda, N, diag_val=0.0)
    t_build = time.time() - t0
    print(f"  Matrix built in {t_build:.2f}s")

    # Compute eigenvalues
    t0 = time.time()
    eigs = np.linalg.eigvalsh(T)
    t_eig = time.time() - t0
    print(f"  Eigenvalues computed in {t_eig:.2f}s")

    # Basic statistics
    eig_min, eig_max = eigs[0], eigs[-1]
    eig_mean = np.mean(eigs)
    eig_std = np.std(eigs)
    eig_median = np.median(eigs)

    print(f"  Range: [{eig_min:.4f}, {eig_max:.4f}]")
    print(f"  Mean: {eig_mean:.4f}, Median: {eig_median:.4f}")
    print(f"  Std: {eig_std:.4f}")

    # Density near zero
    near_zero = np.sum(np.abs(eigs) < eig_std * 0.1)
    print(f"  Eigenvalues within 10% of std from zero: {near_zero} ({100*near_zero/N:.1f}%)")

    # Store results
    results[N] = {
        'range': [float(eig_min), float(eig_max)],
        'mean': float(eig_mean),
        'median': float(eig_median),
        'std': float(eig_std),
        'near_zero_count': int(near_zero),
        'near_zero_pct': float(100*near_zero/N),
    }

    # Save eigenvalues for later analysis
    np.save(f'/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006/eigs_vM_N{N}.npy', eigs)

# Also with diagonal = ln(2*pi)
print("\n=== Von Mangoldt Toeplitz with diag=ln(2π), N=500 ===")
T_diag = build_toeplitz_fast(Lambda, 500, diag_val=np.log(2*np.pi))
eigs_diag = np.linalg.eigvalsh(T_diag)
print(f"  Range: [{eigs_diag[0]:.4f}, {eigs_diag[-1]:.4f}]")
print(f"  Mean: {np.mean(eigs_diag):.4f}, Std: {np.std(eigs_diag):.4f}")

# Histogram of eigenvalue density for N=1000
eigs_1000 = np.load(f'/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006/eigs_vM_N1000.npy')

print("\n=== Eigenvalue Density Histogram (N=1000) ===")
hist, bin_edges = np.histogram(eigs_1000, bins=50)
for i in range(len(hist)):
    center = (bin_edges[i] + bin_edges[i+1]) / 2
    if hist[i] > 0:
        print(f"  [{center:8.2f}]: {'#' * min(hist[i], 80)} ({hist[i]})")

# Summary
print("\n=== PART 1 SUMMARY ===")
for N in [200, 500, 1000]:
    r = results[N]
    print(f"N={N}: range=[{r['range'][0]:.2f}, {r['range'][1]:.2f}], mean={r['mean']:.2f}, std={r['std']:.2f}, near_zero={r['near_zero_pct']:.1f}%")

# Save results
with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006/results_part1.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nPart 1 complete.")
