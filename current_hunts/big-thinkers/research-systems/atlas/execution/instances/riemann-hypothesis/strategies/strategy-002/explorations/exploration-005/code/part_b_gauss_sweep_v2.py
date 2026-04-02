"""
Part B v2: Gauss Prime Sweep — Corrected β via Wigner-interpolated fit
Uses the SAME fitting method as exploration-001 (fit_wigner_interpolated)
and degree-15 polynomial unfolding for consistency.

Primes: 97 (control), 251, 499, 997, 9973, 99991
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import curve_fit, minimize_scalar
from scipy.special import gamma
import json
import os
import time

np.random.seed(99)

# ─── Von Mangoldt ──────────────────────────────────────────────────────────────

def precompute_mangoldt_sieve(max_n):
    vals = np.zeros(max_n + 1)
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(max_n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    for p in range(2, max_n + 1):
        if is_prime[p]:
            log_p = np.log(p)
            pk = p
            while pk <= max_n:
                vals[pk] = log_p
                pk *= p
    return vals

# ─── Matrix construction ───────────────────────────────────────────────────────

def build_gauss_hankel(N, p, mangoldt_vals):
    """H_{jk} = Λ(|j-k|+1) × exp(2πi jk/p), then symmetrized."""
    j_idx = np.arange(N, dtype=float)
    k_idx = np.arange(N, dtype=float)
    jj, kk = np.meshgrid(j_idx, k_idx, indexing='ij')
    diffs = np.abs(jj - kk).astype(int) + 1
    amps = mangoldt_vals[diffs]
    phases = 2.0 * np.pi * jj * kk / p
    H = amps * np.exp(1j * phases)
    H = (H + H.conj().T) / 2.0
    return H

# ─── Unfolding (degree-15, matching S002-E001) ─────────────────────────────────

def unfold_eigenvalues(evals):
    """Degree-15 polynomial unfolding, same as S002-E001."""
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

# ─── Wigner-like distributions ─────────────────────────────────────────────────

def wigner_gue(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_goe(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)

def wigner_interpolated(s, beta):
    """P(s; β) = A s^β exp(-B s²) normalized so mean = 1."""
    g1 = gamma((beta + 1) / 2)
    g2 = gamma((beta + 2) / 2)
    B = (g2 / g1)**2
    A = 2 * (g2**(beta + 1)) / (g1**(beta + 2))
    return A * s**beta * np.exp(-B * s**2)

# ─── Fitting (same as S002-E001) ──────────────────────────────────────────────

def fit_wigner_interpolated(spacings, n_bins=50):
    """Fit full Wigner-like interpolation P(s) = A s^β exp(-B s²) to spacings."""
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
            model,
            centers[mask], hist[mask],
            p0=[1.0],
            bounds=([0.0], [4.0]),
            maxfev=10000
        )
        beta = popt[0]
        beta_err = np.sqrt(np.diag(pcov))[0] if pcov is not None else np.nan
        return float(beta), float(beta_err)
    except Exception:
        return np.nan, np.nan

def fit_brody(spacings):
    """Brody distribution MLE."""
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
    ks = np.max(np.abs(empirical_cdf - theo_cdf_at_sp))
    return float(ks)

def fit_beta_logslope(spacings):
    """Simple log-log slope (for comparison)."""
    s_max = 0.5
    bins = np.linspace(0, s_max, 20)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = (hist > 0) & (centers > 1e-8)
    if mask.sum() < 4:
        return np.nan
    coeffs = np.polyfit(np.log(centers[mask]), np.log(hist[mask]), 1)
    return float(coeffs[0])

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    N = 500

    print(f"Precomputing Von Mangoldt up to {2*N+2}...")
    mangoldt_vals = precompute_mangoldt_sieve(2 * N + 2)

    primes_to_test = [97, 251, 499, 997, 9973, 99991]

    results_table = {}

    for p in primes_to_test:
        print(f"\n{'='*55}")
        print(f"p = {p}, N = {N}")
        t0 = time.time()

        H = build_gauss_hankel(N, p, mangoldt_vals)
        evals = eigh(H, eigvals_only=True)
        spacings = compute_spacings(evals)
        print(f"  Built + diagonalized in {time.time()-t0:.1f}s, n_spacings={len(spacings)}")
        print(f"  spacing range: [{spacings.min():.3f}, {spacings.max():.3f}], mean={spacings.mean():.3f}")

        beta_w, beta_err = fit_wigner_interpolated(spacings)
        beta_b = fit_brody(spacings)
        beta_ls = fit_beta_logslope(spacings)
        chi2_gue = compute_chi2_reduced(spacings, wigner_gue)
        chi2_goe = compute_chi2_reduced(spacings, wigner_goe)
        ks_gue = compute_ks(spacings, wigner_gue)
        ks_goe = compute_ks(spacings, wigner_goe)
        best_fit = "GUE" if ks_gue < ks_goe else "GOE"

        bw_s = f"{beta_w:.3f}" if beta_w == beta_w else "NaN"
        be_s = f"{beta_err:.3f}" if beta_err == beta_err else "NaN"
        print(f"  β_Wigner (full fit) = {bw_s} ± {be_s}")
        print(f"  β_Brody  (MLE)      = {beta_b:.3f}")
        print(f"  β_logslope (0,0.5)  = {beta_ls:.3f}")
        print(f"  χ²_GUE = {chi2_gue:.3f}, χ²_GOE = {chi2_goe:.3f}")
        print(f"  KS_GUE = {ks_gue:.3f}, KS_GOE = {ks_goe:.3f}")
        print(f"  Best fit: {best_fit}")

        results_table[p] = {
            "p": p,
            "N": N,
            "beta_wigner_fullfit": beta_w,
            "beta_wigner_err": beta_err,
            "beta_brody": beta_b,
            "beta_logslope": beta_ls,
            "chi2_gue": chi2_gue,
            "chi2_goe": chi2_goe,
            "ks_gue": ks_gue,
            "ks_goe": ks_goe,
            "best_fit": best_fit,
            "log_p": float(np.log(p)),
            "n_spacings": len(spacings)
        }

    # ─── Summary Table ──────────────────────────────────────────────────────────
    print("\n\n" + "="*80)
    print("GAUSS PRIME SWEEP — β vs log(p) SUMMARY TABLE (v2: Wigner-interp fit)")
    print("="*80)
    print(f"{'p':>8} {'log(p)':>7} {'β_W (full)':>11} {'β_Brody':>8} {'χ²_GUE':>8} {'χ²_GOE':>8} {'Best':>6}")
    print("-"*80)
    for p in primes_to_test:
        r = results_table[p]
        bw_s = f"{r['beta_wigner_fullfit']:.3f}" if r['beta_wigner_fullfit'] is not None and r['beta_wigner_fullfit'] == r['beta_wigner_fullfit'] else "  NaN"
        print(f"{p:>8} {r['log_p']:>7.3f} {bw_s:>11} {r['beta_brody']:>8.3f} "
              f"{r['chi2_gue']:>8.3f} {r['chi2_goe']:>8.3f} {r['best_fit']:>6}")

    # Known from S002-E001 for comparison
    print("\nKnown from S002-E001:")
    print("  p= 97: β_W=0.880, β_B=0.930, χ²_GUE=10.896, best=GOE")
    print("  p=997: β_W=1.092, β_B=0.959, χ²_GUE=5.027, best=GOE")

    # ─── Trend analysis ─────────────────────────────────────────────────────────
    print("\n--- Trend Analysis: β_Wigner (full fit) vs log(p) ---")
    log_p_vals = np.array([results_table[p]['log_p'] for p in primes_to_test])
    beta_vals = np.array([results_table[p]['beta_wigner_fullfit'] for p in primes_to_test])
    valid = np.array([b == b and b is not None for b in beta_vals])  # not NaN

    slope, intercept, p_at_beta2 = np.nan, np.nan, np.nan
    if valid.sum() >= 3:
        lp_valid = log_p_vals[valid]
        bv_valid = beta_vals[valid]
        # Exclude p ≈ N anomaly (p=499) from trend line if β is anomalously low
        exclude_anomaly = (bv_valid < 0.4)  # p=499 tends to be anomalously low
        if not exclude_anomaly.all():
            lp_fit = lp_valid[~exclude_anomaly]
            bv_fit = bv_valid[~exclude_anomaly]
            coeffs = np.polyfit(lp_fit, bv_fit, 1)
            slope, intercept = coeffs
            print(f"  Linear fit (excluding p≈N anomaly): β = {slope:.4f} × log(p) + {intercept:.4f}")
        else:
            coeffs = np.polyfit(lp_valid, bv_valid, 1)
            slope, intercept = coeffs
            print(f"  Linear fit (all primes): β = {slope:.4f} × log(p) + {intercept:.4f}")

        if abs(slope) > 1e-6:
            log_p_at_beta2 = (2.0 - intercept) / slope
            p_at_beta2 = np.exp(log_p_at_beta2)
            if p_at_beta2 < 1e15:
                print(f"  β → 2 at log(p) = {log_p_at_beta2:.1f}, p ≈ {p_at_beta2:.2e}")
            else:
                print(f"  β → 2 at p ≈ {p_at_beta2:.2e} (very large)")
        else:
            print("  Trend too flat to extrapolate to β=2")

        # Plateau test
        large_p = [p for p in primes_to_test if p >= 9973]
        betas_large = [results_table[p]['beta_wigner_fullfit'] for p in large_p
                       if results_table[p]['beta_wigner_fullfit'] == results_table[p]['beta_wigner_fullfit']]
        if len(betas_large) >= 2:
            print(f"\n  Plateau check (p ≥ 9973): β = {betas_large}")
            plateau_range = max(betas_large) - min(betas_large)
            print(f"  Range = {plateau_range:.4f}")
            if plateau_range < 0.05:
                print("  → PLATEAU (β not growing for large p)")
            else:
                print("  → Still varying")
    else:
        print("  Insufficient data for trend analysis")

    # ─── Save ────────────────────────────────────────────────────────────────────
    output = {
        "version": "v2_wigner_interp_fit",
        "results": {str(p): {k: (float(v) if isinstance(v, (float, np.floating)) and v == v else
                               (None if v != v else v))
                              for k, v in results_table[p].items()}
                    for p in primes_to_test},
        "trend": {
            "slope": float(slope) if slope == slope else None,
            "intercept": float(intercept) if intercept == intercept else None,
            "p_at_beta2": float(p_at_beta2) if p_at_beta2 == p_at_beta2 and p_at_beta2 < 1e20 else None
        },
        "known_from_s002_e001": {
            "97": {"beta_wigner": 0.880, "beta_brody": 0.930, "chi2_gue": 10.896, "best": "GOE"},
            "997": {"beta_wigner": 1.092, "beta_brody": 0.959, "chi2_gue": 5.027, "best": "GOE"}
        }
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "part_b_results_v2.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")

    return output

if __name__ == "__main__":
    results = main()
