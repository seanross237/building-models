#!/usr/bin/env python3
"""
Step 1: Establish the GUE baseline from actual Riemann zeta zeros.

Computes:
  - First ~10,000 nontrivial zeros using mpmath
  - Normalized nearest-neighbor spacings
  - KS test against GUE Wigner surmise
  - KS test against Poisson
  - Saves results for comparison with CA experiments
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad
import mpmath
import json
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# GUE Wigner surmise distribution
# ============================================================

def wigner_surmise_pdf(s):
    """GUE nearest-neighbor spacing: P(s) = (32/pi^2) s^2 exp(-4s^2/pi)"""
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf(s):
    """CDF of the Wigner surmise (GUE), computed via numerical integration."""
    if np.isscalar(s):
        val, _ = quad(wigner_surmise_pdf, 0, s)
        return val
    return np.array([quad(wigner_surmise_pdf, 0, si)[0] for si in s])

class WignerSurmise:
    """scipy-compatible distribution wrapper for KS tests."""
    def cdf(self, x):
        return wigner_surmise_cdf(x)

# ============================================================
# Compute Riemann zeta zeros
# ============================================================

def compute_zeta_zeros(n_zeros=10000):
    """Compute first n nontrivial zeros of the Riemann zeta function."""
    print(f"Computing first {n_zeros} Riemann zeta zeros using mpmath...")
    mpmath.mp.dps = 25  # 25 decimal places - sufficient for spacing stats

    zeros = []
    t0 = time.time()

    for k in range(1, n_zeros + 1):
        z = float(mpmath.im(mpmath.zetazero(k)))
        zeros.append(z)
        if k % 1000 == 0:
            elapsed = time.time() - t0
            print(f"  Computed {k}/{n_zeros} zeros ({elapsed:.1f}s elapsed, last zero: {z:.6f})")

    elapsed = time.time() - t0
    print(f"  Done. {n_zeros} zeros computed in {elapsed:.1f}s")
    return np.array(zeros)

def normalize_spacings(zeros):
    """
    Compute normalized nearest-neighbor spacings.

    The mean spacing at height T is approximately 2*pi / log(T/(2*pi)).
    We normalize so that the mean spacing is 1 (unfolding).
    """
    spacings = np.diff(zeros)

    # Local unfolding: normalize each spacing by the local mean density
    # The density of zeros at height t is approximately (1/(2*pi)) * log(t/(2*pi))
    midpoints = (zeros[:-1] + zeros[1:]) / 2
    local_density = (1.0 / (2 * np.pi)) * np.log(midpoints / (2 * np.pi))

    # Normalized spacing = raw spacing * local density
    normalized = spacings * local_density

    return normalized

# ============================================================
# Statistical tests
# ============================================================

def ks_test_gue(spacings):
    """KS test of spacings against GUE Wigner surmise."""
    # Build empirical CDF values at each data point
    sorted_s = np.sort(spacings)
    n = len(sorted_s)

    # Compute Wigner CDF at each point
    wigner_cdf_vals = wigner_surmise_cdf(sorted_s)

    # Empirical CDF
    ecdf = np.arange(1, n + 1) / n
    ecdf_minus = np.arange(0, n) / n

    # KS statistic
    d_plus = np.max(ecdf - wigner_cdf_vals)
    d_minus = np.max(wigner_cdf_vals - ecdf_minus)
    ks_stat = max(d_plus, d_minus)

    # Approximate p-value using Kolmogorov distribution
    # For large n, sqrt(n) * D converges to the Kolmogorov distribution
    p_value = stats.ksone.sf(ks_stat, n) * 2  # two-sided
    p_value = min(p_value, 1.0)

    return ks_stat, p_value

def ks_test_poisson(spacings):
    """KS test of spacings against exponential (Poisson process) distribution."""
    # Poisson nearest-neighbor: P(s) = exp(-s), mean = 1
    result = stats.kstest(spacings, 'expon', args=(0, 1))
    return result.statistic, result.pvalue

# ============================================================
# Main
# ============================================================

def main():
    # Compute zeros (start with fewer if this is too slow, then scale up)
    # Try 2000 first for speed, then expand
    N_ZEROS = 2000

    zeros = compute_zeta_zeros(N_ZEROS)

    # Save raw zeros
    np.save(os.path.join(OUTPUT_DIR, 'zeta_zeros.npy'), zeros)

    # Compute normalized spacings
    spacings = normalize_spacings(zeros)
    np.save(os.path.join(OUTPUT_DIR, 'zeta_spacings.npy'), spacings)

    print(f"\n=== Spacing Statistics ===")
    print(f"Number of spacings: {len(spacings)}")
    print(f"Mean spacing (should be ~1): {np.mean(spacings):.6f}")
    print(f"Std of spacings: {np.std(spacings):.6f}")
    print(f"Min spacing: {np.min(spacings):.6f}")
    print(f"Max spacing: {np.max(spacings):.6f}")

    # KS test against GUE
    print(f"\n=== KS Tests ===")
    ks_gue, p_gue = ks_test_gue(spacings)
    print(f"KS test vs GUE Wigner surmise: D = {ks_gue:.6f}, p = {p_gue:.6f}")

    # KS test against Poisson
    ks_poisson, p_poisson = ks_test_poisson(spacings)
    print(f"KS test vs Poisson (exp): D = {ks_poisson:.6f}, p = {p_poisson:.6f}")

    # Compute histogram for later comparison
    bins = np.linspace(0, 4, 81)
    hist, bin_edges = np.histogram(spacings, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Theoretical GUE values at bin centers
    gue_theoretical = wigner_surmise_pdf(bin_centers)

    # Theoretical Poisson values
    poisson_theoretical = np.exp(-bin_centers)

    print(f"\n=== Histogram Comparison (selected bins) ===")
    print(f"{'s':>6s} | {'Data':>8s} | {'GUE':>8s} | {'Poisson':>8s}")
    print("-" * 40)
    for i in range(0, len(bin_centers), 4):
        print(f"{bin_centers[i]:6.2f} | {hist[i]:8.4f} | {gue_theoretical[i]:8.4f} | {poisson_theoretical[i]:8.4f}")

    # Save results
    results = {
        'n_zeros': N_ZEROS,
        'n_spacings': len(spacings),
        'mean_spacing': float(np.mean(spacings)),
        'std_spacing': float(np.std(spacings)),
        'ks_gue_statistic': float(ks_gue),
        'ks_gue_pvalue': float(p_gue),
        'ks_poisson_statistic': float(ks_poisson),
        'ks_poisson_pvalue': float(p_poisson),
        'histogram_bins': bin_centers.tolist(),
        'histogram_values': hist.tolist(),
        'gue_theoretical': gue_theoretical.tolist(),
        'poisson_theoretical': poisson_theoretical.tolist(),
    }

    with open(os.path.join(OUTPUT_DIR, 'gue_baseline_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {OUTPUT_DIR}/gue_baseline_results.json")

    return results

if __name__ == '__main__':
    main()
