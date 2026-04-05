"""
Part B v3: Gauss Prime Sweep — 1-indexed construction matching S002-E001
Key fix: S002-E001 used ((i+1)*(j+1)) % p, NOT (i*j).

This uses the EXACT same:
  - Matrix construction: H_{jk} = Λ(|j-k|+1) × exp(2πi ((j+1)(k+1) mod p)/p)
  - Unfolding: degree-15 polynomial
  - Fitting: fit_wigner_interpolated (full range)
  - Multiple realizations: N_REP=3 (3 copies = 3×499 spacings)

Primes: 97 (control), 251, 499, 997, 9973, 99991
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import curve_fit, minimize_scalar
from scipy.special import gamma
import json
import os
import time

# ─── Von Mangoldt ──────────────────────────────────────────────────────────────

def precompute_mangoldt(max_n):
    """Match S002-E001 implementation exactly."""
    vals = np.zeros(max_n + 1)
    for n in range(2, max_n + 1):
        temp = n
        found_prime = None
        for p in range(2, int(n**0.5) + 1):
            if temp % p == 0:
                found_prime = p
                while temp % p == 0:
                    temp //= p
                break
        if found_prime is None:
            vals[n] = np.log(n)  # n is prime
        elif temp == 1:
            vals[n] = np.log(found_prime)  # n is prime power
    return vals

# ─── Gauss Matrix (1-indexed, matching S002-E001) ─────────────────────────────

def build_c3_gauss(N, mgv, p):
    """C3: H_{jk} = Λ(|j-k|+1) × exp(2πi ((j+1)(k+1) mod p)/p) — 1-indexed."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]

    # 1-indexed product modulo p
    jk_mod = ((i_idx + 1) * (j_idx + 1)) % p
    phases = 2 * np.pi * jk_mod / p
    H = amp * np.exp(1j * phases)
    np.fill_diagonal(H, float(np.real(mgv[1])))  # Λ(1) = 0
    H = (H + H.conj().T) / 2
    return H

# ─── Unfolding (degree-15 matching S002-E001) ──────────────────────────────────

def unfold_eigenvalues(evals):
    evals_sorted = np.sort(evals)
    n = len(evals_sorted)
    cum = np.arange(1, n + 1, dtype=float)
    x_norm = (evals_sorted - evals_sorted.mean()) / (evals_sorted.std() + 1e-10)
    try:
        poly_coeffs = np.polyfit(x_norm, cum, deg=15)
        smooth_cum = np.polyval(poly_coeffs, x_norm)
    except Exception:
        smooth_cum = cum
    return smooth_cum

def compute_spacings(evals):
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    return spacings / spacings.mean()

# ─── Spacing distributions and fitting ────────────────────────────────────────

def wigner_gue(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_goe(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def wigner_interpolated(s, beta):
    """P(s; β) = A s^β exp(-B s²), normalized."""
    g1 = gamma((beta + 1) / 2)
    g2 = gamma((beta + 2) / 2)
    B = (g2 / g1)**2
    A = 2 * (g2**(beta + 1)) / (g1**(beta + 2))
    return A * s**beta * np.exp(-B * s**2)

def fit_wigner_interpolated(spacings, n_bins=50):
    s_max = 4.0
    bins = np.linspace(0, s_max, n_bins + 1)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = hist > 0
    if mask.sum() < 5:
        return np.nan, np.nan
    def model(s, beta):
        try:
            return wigner_interpolated(s, beta)
        except Exception:
            return np.ones_like(s) * 1e-10
    try:
        popt, pcov = curve_fit(
            model, centers[mask], hist[mask],
            p0=[1.0], bounds=([0.0], [4.0]), maxfev=10000
        )
        return float(popt[0]), float(np.sqrt(np.diag(pcov))[0])
    except Exception:
        return np.nan, np.nan

def fit_brody(spacings):
    def neg_log_likelihood(beta):
        if beta <= 0 or beta > 3:
            return 1e10
        try:
            gval = gamma((beta + 2) / (beta + 1))
            b = gval**(beta + 1)
            log_probs = (np.log((beta + 1) * b) + beta * np.log(np.maximum(spacings, 1e-10))
                         - b * spacings**(beta + 1))
            return -np.sum(log_probs)
        except Exception:
            return 1e10
    result = minimize_scalar(neg_log_likelihood, bounds=(0.01, 3.0), method='bounded')
    return float(result.x) if result.success else np.nan

def compute_chi2_reduced(spacings, wigner_func, n_bins=30, s_max=4.0):
    bins = np.linspace(0, s_max, n_bins + 1)
    observed, edges = np.histogram(spacings, bins=bins, density=False)
    centers = (edges[:-1] + edges[1:]) / 2
    bin_width = bins[1] - bins[0]
    expected = wigner_func(centers) * bin_width * len(spacings)
    mask = expected > 0.5
    if mask.sum() < 5:
        return np.nan
    chi2_val = np.sum((observed[mask] - expected[mask])**2 / expected[mask])
    return float(chi2_val / mask.sum())

def compute_ks(spacings, wigner_func):
    s_eval = np.linspace(0, 5, 2000)
    ds = s_eval[1] - s_eval[0]
    pdf_vals = wigner_func(s_eval)
    cdf_vals = np.cumsum(pdf_vals) * ds
    cdf_vals /= cdf_vals[-1]
    sp_sorted = np.sort(spacings)
    n = len(sp_sorted)
    empirical_cdf = np.arange(1, n + 1) / n
    theo_cdf_at_sp = np.interp(sp_sorted, s_eval, cdf_vals)
    return float(np.max(np.abs(empirical_cdf - theo_cdf_at_sp)))

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    N = 500
    N_REP = 3  # match S002-E001 (3 copies for more spacings, but matrix is deterministic)

    print(f"Precomputing Von Mangoldt up to {2*N}...")
    mgv = precompute_mangoldt(2 * N + 1)

    primes_to_test = [97, 251, 499, 997, 9973, 99991]

    results_table = {}

    for p in primes_to_test:
        print(f"\n{'='*55}")
        print(f"p = {p}, N = {N}, N_REP = {N_REP} (1-indexed construction)")
        t0 = time.time()

        H = build_c3_gauss(N, mgv, p)
        evals = eigh(H, eigvals_only=True)

        # N_REP=3 means 3×499 spacings (same matrix = same eigenvalues, so trivially 3×)
        spacings_single = compute_spacings(evals)
        spacings = np.tile(spacings_single, N_REP)  # replicate to match S002-E001 data size

        print(f"  Built + diag in {time.time()-t0:.1f}s, n_spacings={len(spacings)}")
        print(f"  spacing range: [{spacings.min():.3f}, {spacings.max():.3f}], mean={spacings.mean():.3f}")

        beta_w, beta_err = fit_wigner_interpolated(spacings)
        beta_b = fit_brody(spacings)
        chi2_gue = compute_chi2_reduced(spacings, wigner_gue)
        chi2_goe = compute_chi2_reduced(spacings, wigner_goe)
        ks_gue = compute_ks(spacings, wigner_gue)
        ks_goe = compute_ks(spacings, wigner_goe)
        best_fit = "GUE" if ks_gue < ks_goe else "GOE"

        bw_s = f"{beta_w:.3f}" if beta_w == beta_w else "NaN"
        be_s = f"{beta_err:.3f}" if beta_err == beta_err else "NaN"
        print(f"  β_Wigner (full fit) = {bw_s} ± {be_s}")
        print(f"  β_Brody  (MLE)      = {beta_b:.3f}")
        print(f"  χ²_GUE = {chi2_gue:.3f}, χ²_GOE = {chi2_goe:.3f}")
        print(f"  KS_GUE = {ks_gue:.3f}, KS_GOE = {ks_goe:.3f}")
        print(f"  Best fit: {best_fit}")

        results_table[p] = {
            "p": p,
            "N": N,
            "beta_wigner": beta_w,
            "beta_wigner_err": beta_err,
            "beta_brody": beta_b,
            "chi2_gue": chi2_gue,
            "chi2_goe": chi2_goe,
            "ks_gue": ks_gue,
            "ks_goe": ks_goe,
            "best_fit": best_fit,
            "log_p": float(np.log(p)),
        }

    # ─── Summary Table ──────────────────────────────────────────────────────────
    print("\n\n" + "="*80)
    print("GAUSS PRIME SWEEP (v3: 1-indexed, matching S002-E001)")
    print("="*80)
    print(f"{'p':>8} {'log(p)':>7} {'β_W':>8} {'β_B':>7} {'χ²_GUE':>8} {'χ²_GOE':>8} {'Best':>6}")
    print("-"*80)
    for p in primes_to_test:
        r = results_table[p]
        bw_s = f"{r['beta_wigner']:.3f}" if r['beta_wigner'] == r['beta_wigner'] else "  NaN"
        print(f"{p:>8} {r['log_p']:>7.3f} {bw_s:>8} {r['beta_brody']:>7.3f} "
              f"{r['chi2_gue']:>8.3f} {r['chi2_goe']:>8.3f} {r['best_fit']:>6}")
    print("\nS002-E001 reference:")
    print("      97   4.575    0.880   0.930   10.896    1.499    GOE")
    print("     997   6.905    1.092   0.959    5.027    0.640    GOE")

    # ─── Trend Analysis ──────────────────────────────────────────────────────────
    print("\n--- Trend: β vs log(p) ---")
    log_p_arr = np.array([results_table[p]['log_p'] for p in primes_to_test])
    beta_arr = np.array([results_table[p]['beta_wigner'] for p in primes_to_test])
    valid = np.isfinite(beta_arr) & (beta_arr > 0)

    # Exclude p≈N anomaly from trend line
    no_anomaly = valid & (np.abs(log_p_arr - np.log(N)) > 0.5)

    slope, intercept = np.nan, np.nan
    if no_anomaly.sum() >= 3:
        coeffs = np.polyfit(log_p_arr[no_anomaly], beta_arr[no_anomaly], 1)
        slope, intercept = coeffs
        print(f"  Trend (excl. p≈N): β = {slope:.4f} × log(p) + {intercept:.4f}")
        if abs(slope) > 1e-5:
            lp_at_2 = (2.0 - intercept) / slope
            p_at_2 = np.exp(lp_at_2)
            print(f"  β→2 at p = {p_at_2:.2e}")
        else:
            print("  Slope ≈ 0: β does NOT trend toward 2")
    elif valid.sum() >= 3:
        coeffs = np.polyfit(log_p_arr[valid], beta_arr[valid], 1)
        slope, intercept = coeffs
        print(f"  Trend (all valid): β = {slope:.4f} × log(p) + {intercept:.4f}")
    else:
        print("  Insufficient data")

    # Max β across all primes
    valid_betas = beta_arr[valid]
    valid_primes = np.array(primes_to_test)[valid]
    if len(valid_betas) > 0:
        max_idx = np.argmax(valid_betas)
        print(f"\n  Maximum β = {valid_betas[max_idx]:.3f} at p = {valid_primes[max_idx]}")
        print(f"  β at large p (p=9973): {results_table[9973]['beta_wigner']:.3f}")
        print(f"  β at very large p (p=99991): {results_table[99991]['beta_wigner']:.3f}")

    # Anomaly check
    print(f"\n  p=499 (≈N) anomaly: β={results_table[499]['beta_wigner']:.3f} (expected ~0.8-1.0)")
    print(f"  p=99991 (>>N) behavior: β={results_table[99991]['beta_wigner']:.3f}")

    # ─── Save ────────────────────────────────────────────────────────────────────
    output = {
        "version": "v3_1indexed_s002e001_matching",
        "construction": "H_{jk} = Λ(|j-k|+1) × exp(2πi ((j+1)(k+1) mod p)/p), 1-indexed",
        "results": {str(p): {k: (float(v) if isinstance(v, (float, np.floating)) and np.isfinite(v) else None)
                              for k, v in results_table[p].items()}
                    for p in primes_to_test},
        "trend": {
            "slope": float(slope) if np.isfinite(slope) else None,
            "intercept": float(intercept) if np.isfinite(intercept) else None,
        },
        "known_from_s002_e001": {
            "97": {"beta_wigner": 0.880, "chi2_gue": 10.896, "best": "GOE"},
            "997": {"beta_wigner": 1.092, "chi2_gue": 5.027, "best": "GOE"}
        }
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "part_b_results_v3.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    return output

if __name__ == "__main__":
    results = main()
