"""
Part B Complete: Gauss Prime Sweep + Fine Sweep + .npz output
Exploration 005, Strategy 002, Riemann Hypothesis

Runs:
1. Main sweep: p = 97, 251, 499, 997, 9973, 99991
2. Fine sweep near optimal: p near 500-2000 (where β peaks)
3. Saves all eigenvalues and results as .npz
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

def analyze_prime(N, mgv, p):
    """Full analysis for a single prime p."""
    H = build_c3_gauss(N, mgv, p)
    evals = eigh(H, eigvals_only=True)
    spacings = compute_spacings(evals)

    beta_w, beta_err = fit_wigner_interpolated(spacings)
    beta_b = fit_brody(spacings)
    chi2_gue = compute_chi2_reduced(spacings, wigner_gue)
    chi2_goe = compute_chi2_reduced(spacings, wigner_goe)
    ks_gue = compute_ks(spacings, wigner_gue)
    ks_goe = compute_ks(spacings, wigner_goe)
    best_fit = "GUE" if ks_gue < ks_goe else "GOE"

    return {
        "p": int(p),
        "N": N,
        "beta_wigner": float(beta_w) if np.isfinite(beta_w) else None,
        "beta_wigner_err": float(beta_err) if np.isfinite(beta_err) else None,
        "beta_brody": float(beta_b) if np.isfinite(beta_b) else None,
        "chi2_gue": float(chi2_gue) if np.isfinite(chi2_gue) else None,
        "chi2_goe": float(chi2_goe) if np.isfinite(chi2_goe) else None,
        "ks_gue": float(ks_gue),
        "ks_goe": float(ks_goe),
        "best_fit": best_fit,
        "log_p": float(np.log(p)),
        "N2_over_p": float(N**2 / p),
        "eigenvalues": evals,
        "spacings": spacings,
    }

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    N = 500
    print(f"Precomputing Von Mangoldt up to {2*N+1}...")
    mgv = precompute_mangoldt(2 * N + 1)

    # ─── Phase 1: Main sweep ────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("PHASE 1: Main Prime Sweep")
    print("="*70)

    main_primes = [97, 251, 499, 997, 9973, 99991]
    main_results = {}
    main_eigenvalues = {}

    for p in main_primes:
        t0 = time.time()
        print(f"\np={p} (N²/p={N**2/p:.1f})...", end=" ", flush=True)
        r = analyze_prime(N, mgv, p)
        elapsed = time.time() - t0
        bw = r['beta_wigner']
        bw_s = f"{bw:.3f}" if bw is not None else "NaN"
        print(f"β_W={bw_s}, β_B={r['beta_brody']:.3f}, {r['best_fit']} ({elapsed:.1f}s)")
        main_eigenvalues[p] = r.pop('eigenvalues')
        r.pop('spacings')
        main_results[p] = r

    # ─── Phase 2: Fine sweep (primes 500-5000) ──────────────────────────────────
    print("\n" + "="*70)
    print("PHASE 2: Fine Sweep (primes in [500, 5000])")
    print("="*70)

    # Generate primes in range using simple sieve
    def sieve_primes(lo, hi):
        """Simple sieve for primes in [lo, hi]."""
        is_prime = [True] * (hi + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(hi**0.5) + 1):
            if is_prime[i]:
                for j in range(i*i, hi + 1, i):
                    is_prime[j] = False
        return [p for p in range(max(lo, 2), hi + 1) if is_prime[p]]

    # Select a sparse set of primes: every ~50th prime in range
    all_primes_range = sieve_primes(500, 5000)
    # Pick ~25 evenly spaced primes
    step = max(1, len(all_primes_range) // 25)
    fine_primes = all_primes_range[::step]
    # Also include p=809 (previous max), and some near multiples of N
    extra_primes = [503, 509, 521, 601, 701, 809, 853, 907, 1009, 1301, 1801, 1999, 2503, 3001, 4001, 4999]
    # Filter to actual primes
    extra_set = set()
    for p in extra_primes:
        if p in set(all_primes_range):
            extra_set.add(p)
    fine_primes = sorted(set(fine_primes) | extra_set)

    fine_results = {}
    for p in fine_primes:
        t0 = time.time()
        r = analyze_prime(N, mgv, p)
        elapsed = time.time() - t0
        bw = r['beta_wigner']
        bw_s = f"{bw:.3f}" if bw is not None else "NaN"
        print(f"  p={p:>5d} (N²/p={N**2/p:>7.1f}) β_W={bw_s} ({elapsed:.1f}s)")
        r.pop('eigenvalues')
        r.pop('spacings')
        fine_results[p] = r

    # ─── Phase 3: Summary ────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("SUMMARY TABLE: Main Sweep")
    print("="*70)
    print(f"{'p':>8} {'log(p)':>7} {'N²/p':>8} {'β_W':>8} {'β_B':>7} {'χ²_GUE':>8} {'χ²_GOE':>8} {'Best':>6}")
    print("-"*70)
    for p in main_primes:
        r = main_results[p]
        bw = r['beta_wigner']
        bw_s = f"{bw:.3f}" if bw is not None else "  NaN"
        bb = r['beta_brody']
        bb_s = f"{bb:.3f}" if bb is not None else " NaN"
        print(f"{p:>8} {r['log_p']:>7.3f} {r['N2_over_p']:>8.1f} {bw_s:>8} {bb_s:>7} "
              f"{r['chi2_gue']:>8.3f} {r['chi2_goe']:>8.3f} {r['best_fit']:>6}")

    print(f"\n{'='*70}")
    print("FINE SWEEP — β_Wigner vs p")
    print(f"{'='*70}")
    print(f"{'p':>6} {'N²/p':>8} {'β_W':>8}")
    print("-"*30)

    all_fine_betas = []
    all_fine_primes = []
    for p in sorted(fine_results.keys()):
        r = fine_results[p]
        bw = r['beta_wigner']
        if bw is not None and np.isfinite(bw):
            print(f"{p:>6} {r['N2_over_p']:>8.1f} {bw:>8.3f}")
            all_fine_betas.append(bw)
            all_fine_primes.append(p)

    # Find maximum
    if all_fine_betas:
        max_idx = np.argmax(all_fine_betas)
        print(f"\nFine sweep max β = {all_fine_betas[max_idx]:.3f} at p = {all_fine_primes[max_idx]}")

    # ─── Combine all results and find global max ──────────────────────────────
    all_results = {}
    all_results.update(main_results)
    all_results.update(fine_results)

    all_betas = []
    all_ps = []
    for p, r in sorted(all_results.items()):
        bw = r['beta_wigner']
        if bw is not None and np.isfinite(bw):
            all_betas.append(bw)
            all_ps.append(p)

    all_betas = np.array(all_betas)
    all_ps = np.array(all_ps)
    global_max_idx = np.argmax(all_betas)
    print(f"\nGLOBAL MAXIMUM β = {all_betas[global_max_idx]:.3f} at p = {all_ps[global_max_idx]}")

    # Trend analysis: β vs log(p)
    log_ps = np.log(all_ps)
    # Exclude very small p and very large p for trend
    mask_trend = (all_ps >= 500) & (all_ps <= 5000)
    if mask_trend.sum() >= 3:
        coeffs = np.polyfit(log_ps[mask_trend], all_betas[mask_trend], 1)
        print(f"\nLinear trend (p in [500,5000]): β = {coeffs[0]:.4f} × log(p) + {coeffs[1]:.4f}")
        if abs(coeffs[0]) > 1e-5:
            lp_at_2 = (2.0 - coeffs[1]) / coeffs[0]
            if lp_at_2 > 0:
                print(f"Extrapolated β→2 at p ≈ {np.exp(lp_at_2):.2e}")
            else:
                print("Extrapolation to β=2 gives negative log(p) — trend is AWAY from GUE")

    # Full range trend
    mask_all = np.isfinite(all_betas)
    if mask_all.sum() >= 3:
        coeffs_full = np.polyfit(log_ps[mask_all], all_betas[mask_all], 1)
        print(f"Full range trend: β = {coeffs_full[0]:.4f} × log(p) + {coeffs_full[1]:.4f}")

    # ─── Save everything ─────────────────────────────────────────────────────────
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # Save main results JSON
    output_json = {
        "main_sweep": {str(p): {k: v for k, v in r.items()} for p, r in main_results.items()},
        "fine_sweep": {str(p): {k: v for k, v in r.items()} for p, r in fine_results.items()},
        "global_max_beta": float(all_betas[global_max_idx]),
        "global_max_p": int(all_ps[global_max_idx]),
    }
    with open(os.path.join(out_dir, "part_b_complete_results.json"), "w") as f:
        json.dump(output_json, f, indent=2)

    # Save .npz with eigenvalues for main primes
    eig_dict = {f"evals_p{p}": main_eigenvalues[p] for p in main_primes}
    eig_dict["primes"] = np.array(main_primes)
    np.savez(os.path.join(out_dir, "part_b_data.npz"), **eig_dict)

    # Save fine sweep β values as .npz for plotting
    np.savez(os.path.join(out_dir, "part_b_fine_data.npz"),
             primes=np.array(all_ps),
             betas=all_betas,
             log_primes=log_ps)

    print(f"\nSaved: part_b_complete_results.json, part_b_data.npz, part_b_fine_data.npz")
    return all_results

if __name__ == "__main__":
    results = main()
