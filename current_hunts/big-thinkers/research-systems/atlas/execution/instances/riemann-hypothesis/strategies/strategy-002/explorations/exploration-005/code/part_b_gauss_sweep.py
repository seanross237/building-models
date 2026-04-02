"""
Part B: Gauss Prime Sweep — β vs log(p) trend
Exploration 005, Strategy 002, Riemann Hypothesis

Tests H_{jk} = Λ(|j-k|+1) × exp(2πi jk/p) for primes p = 251, 499, 997, 9973, 99991
Also tests p = 97 (reconfirm S002-E001 result).

For each prime: computes β_Wigner, χ²_GUE, χ²_GOE, best fit.
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import curve_fit
import json
import os
import time

np.random.seed(99)

# ─── Von Mangoldt precomputation ───────────────────────────────────────────────

def precompute_mangoldt_sieve(max_n):
    """Fast sieve for Von Mangoldt values."""
    vals = np.zeros(max_n + 1)
    # Sieve of Eratosthenes approach
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(max_n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False

    log_p_cache = {}
    for p in range(2, max_n + 1):
        if is_prime[p]:
            log_p_cache[p] = np.log(p)
            pk = p
            while pk <= max_n:
                vals[pk] = log_p_cache[p]
                pk *= p
    return vals

# ─── Gauss Matrix Construction ─────────────────────────────────────────────────

def build_gauss_hankel(N, p, mangoldt_vals):
    """
    Build N×N Gauss sum Hermitian matrix:
    H_{jk} = Λ(|j-k|+1) × exp(2πi jk/p)
    (1-indexed: j,k from 1..N → use 0-indexed internally)

    Then symmetrize: H = (H + H†)/2
    """
    j_idx = np.arange(N, dtype=float)
    k_idx = np.arange(N, dtype=float)
    jj, kk = np.meshgrid(j_idx, k_idx, indexing='ij')

    # Von Mangoldt amplitude
    diffs = np.abs(jj - kk).astype(int) + 1
    amps = mangoldt_vals[diffs]

    # Gauss phases
    phases = 2.0 * np.pi * jj * kk / p
    H = amps * np.exp(1j * phases)

    # Symmetrize
    H = (H + H.conj().T) / 2.0
    return H

# ─── Unfolding ─────────────────────────────────────────────────────────────────

def unfold_eigenvalues(evals, deg=7):
    """Polynomial unfolding, mean spacing = 1."""
    evals_sorted = np.sort(evals)
    N = len(evals_sorted)
    cum = np.arange(1, N + 1, dtype=float)
    x_min, x_max = evals_sorted[0], evals_sorted[-1]
    x_norm = (evals_sorted - x_min) / (x_max - x_min + 1e-15) * 2 - 1
    try:
        coeffs = np.polyfit(x_norm, cum, deg=deg)
        unfolded = np.polyval(coeffs, x_norm)
    except Exception:
        unfolded = cum
    sp = np.diff(unfolded)
    ms = sp.mean()
    if ms > 0:
        unfolded = unfolded / ms
    return unfolded

def get_spacings(evals):
    """Get normalized spacings from eigenvalues."""
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    spacings = spacings / spacings.mean()
    return spacings[spacings > 0]

# ─── Statistics ────────────────────────────────────────────────────────────────

def fit_beta(spacings):
    """Fit level repulsion exponent β from small-s log-log slope."""
    s_max = 0.5
    bins = np.linspace(0, s_max, 20)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = (hist > 0) & (centers > 1e-8)
    if mask.sum() < 4:
        return np.nan
    log_c = np.log(centers[mask])
    log_h = np.log(hist[mask])
    coeffs = np.polyfit(log_c, log_h, 1)
    return float(coeffs[0])

def fit_beta_brody(spacings):
    """Fit Brody distribution parameter β_B (interpolates Poisson to GUE)."""
    # Brody: P(s) = (1+β) × α × s^β × exp(-α s^{1+β})
    # where α = [Γ((β+2)/(β+1))]^{β+1}
    from scipy.special import gamma
    from scipy.optimize import minimize_scalar

    def neg_log_likelihood(beta_b):
        if beta_b < 0 or beta_b > 3:
            return 1e10
        alpha = gamma((beta_b + 2) / (beta_b + 1)) ** (beta_b + 1)
        log_pdf = (np.log(1 + beta_b) + np.log(alpha) +
                   beta_b * np.log(spacings + 1e-15) -
                   alpha * spacings**(1 + beta_b))
        return -np.sum(log_pdf)

    result = minimize_scalar(neg_log_likelihood, bounds=(0.0, 2.5), method='bounded')
    return float(result.x)

def wigner_gue(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_goe(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def chi2_reduced(spacings, model_fn, n_bins=20):
    """Reduced chi² of spacing histogram vs theoretical distribution."""
    bins = np.linspace(0, 4.0, n_bins + 1)
    obs, _ = np.histogram(spacings, bins=bins, density=False)
    centers = (bins[:-1] + bins[1:]) / 2
    dr = bins[1] - bins[0]
    expected = model_fn(centers) * dr * len(spacings)
    mask = expected > 3
    if mask.sum() < 3:
        return np.inf
    chi2_val = np.sum((obs[mask] - expected[mask])**2 / expected[mask])
    return float(chi2_val / mask.sum())

# ─── Main: Part B computation ──────────────────────────────────────────────────

def main():
    N = 500

    print(f"Precomputing Von Mangoldt up to {2*N+2}...")
    mangoldt_vals = precompute_mangoldt_sieve(2 * N + 2)

    # Prime list to test
    # From goal: p = 251, 499, 997, 9973, 99991
    # Also include p = 97 (from S002-E001) and p = 499 (near N=500)
    primes_to_test = [97, 251, 499, 997, 9973, 99991]

    # Known results from S002-E001:
    known = {
        97: {"beta_wigner": 0.88, "chi2_gue": 10.9, "chi2_goe": 1.47, "best_fit": "GOE"},
        997: {"beta_wigner": 1.09, "chi2_gue": 5.0, "chi2_goe": 0.64, "best_fit": "GOE"},
    }

    results_table = {}

    for p in primes_to_test:
        print(f"\n{'='*50}")
        print(f"Computing Gauss matrix for p = {p}, N = {N}...")
        t0 = time.time()

        # Average over 3 realizations (Gauss matrix is deterministic, so we only need 1!)
        # Actually the Gauss matrix is fully deterministic (no randomness), so 1 suffices.
        H = build_gauss_hankel(N, p, mangoldt_vals)
        print(f"  Matrix built in {time.time()-t0:.1f}s")

        t1 = time.time()
        evals = eigh(H, eigvals_only=True)
        print(f"  Diagonalization in {time.time()-t1:.1f}s")

        spacings = get_spacings(evals)
        print(f"  Spacings: {len(spacings)} values, mean = {spacings.mean():.3f}")

        beta_w = fit_beta(spacings)
        beta_b = fit_beta_brody(spacings)
        chi2_g = chi2_reduced(spacings, wigner_gue)
        chi2_o = chi2_reduced(spacings, wigner_goe)
        best_fit = "GUE" if chi2_g < chi2_o else "GOE"

        print(f"  β_Wigner = {beta_w:.3f}")
        print(f"  β_Brody  = {beta_b:.3f}")
        print(f"  χ²_GUE   = {chi2_g:.3f}")
        print(f"  χ²_GOE   = {chi2_o:.3f}")
        print(f"  Best fit: {best_fit}")

        results_table[p] = {
            "p": p,
            "N": N,
            "beta_wigner": beta_w,
            "beta_brody": beta_b,
            "chi2_gue": chi2_g,
            "chi2_goe": chi2_o,
            "best_fit": best_fit,
            "log_p": float(np.log(p))
        }

        # Mark known results
        if p in known:
            print(f"  (Known from S002-E001: β={known[p]['beta_wigner']}, {known[p]['best_fit']})")

    # ─── Print summary table ────────────────────────────────────────────────────
    print("\n\n" + "="*75)
    print("GAUSS PRIME SWEEP RESULTS TABLE")
    print("="*75)
    print(f"{'p':>8} {'log(p)':>7} {'β_Wigner':>9} {'β_Brody':>8} {'χ²_GUE':>8} {'χ²_GOE':>8} {'Best':>6}")
    print("-"*75)
    for p in primes_to_test:
        r = results_table[p]
        print(f"{p:>8} {r['log_p']:>7.3f} {r['beta_wigner']:>9.3f} {r['beta_brody']:>8.3f} "
              f"{r['chi2_gue']:>8.3f} {r['chi2_goe']:>8.3f} {r['best_fit']:>6}")

    # ─── Trend analysis ─────────────────────────────────────────────────────────
    print("\n--- Trend Analysis: β vs log(p) ---")
    log_p_vals = [results_table[p]['log_p'] for p in primes_to_test]
    beta_vals = [results_table[p]['beta_wigner'] for p in primes_to_test]
    log_p_arr = np.array(log_p_vals)
    beta_arr = np.array(beta_vals)

    # Remove NaN
    valid = ~np.isnan(beta_arr)
    if valid.sum() >= 3:
        coeffs = np.polyfit(log_p_arr[valid], beta_arr[valid], 1)
        slope, intercept = coeffs
        print(f"  Linear fit: β = {slope:.4f} × log(p) + {intercept:.4f}")

        # Extrapolate to β = 2
        if abs(slope) > 1e-8:
            log_p_at_beta2 = (2.0 - intercept) / slope
            p_at_beta2 = np.exp(log_p_at_beta2)
            print(f"  β → 2 at log(p) = {log_p_at_beta2:.2f}, i.e., p ≈ {p_at_beta2:.0f}")
        else:
            print("  β trend too flat — cannot extrapolate to β=2")

        # Check if plateau
        beta_large = [results_table[p]['beta_wigner'] for p in primes_to_test if p >= 9973 and not np.isnan(results_table[p]['beta_wigner'])]
        if len(beta_large) >= 2:
            plateau_range = max(beta_large) - min(beta_large)
            print(f"  Plateau test (p ≥ 9973): β range = {plateau_range:.4f}")
            if plateau_range < 0.1:
                print("  → PLATEAU detected (β not increasing for large p)")
            else:
                print("  → Still increasing")
    else:
        slope, intercept = np.nan, np.nan
        p_at_beta2 = np.nan
        print("  Insufficient valid data for trend fit")

    # ─── Save results ────────────────────────────────────────────────────────────
    output = {
        "results": {str(p): results_table[p] for p in primes_to_test},
        "trend": {
            "slope": float(slope) if not np.isnan(slope) else None,
            "intercept": float(intercept) if not np.isnan(intercept) else None,
            "p_at_beta2": float(p_at_beta2) if not np.isnan(p_at_beta2) else None
        },
        "known_from_s002_e001": known
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "part_b_results.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return output

if __name__ == "__main__":
    results = main()
