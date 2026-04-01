#!/usr/bin/env python3
"""Task 1 v3: Match S002 methodology exactly.

Key insight: S002 used Wigner interpolated fit P(s;β) = A s^β exp(-B s²),
NOT Brody distribution. Also degree-15 polynomial unfolding with eigenvalue normalization.
"""

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
from scipy.special import gamma
import time

# ─── Von Mangoldt ──────────────────────────────────────────────────────────────

def precompute_mangoldt(max_n):
    """Precompute von Mangoldt values."""
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
            vals[n] = np.log(n)
        elif temp == 1:
            vals[n] = np.log(found_prime)
    return vals

# ─── Matrix Construction ──────────────────────────────────────────────────────

def build_gauss_matrix(N, p, mgv):
    """Build H_{jk} = Lambda(|j-k|+1) * exp(2*pi*i * j*k / p), 1-indexed."""
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]

    # Phase: (i+1)*(j+1) is 1-indexed j*k
    jk = (i_idx + 1).astype(np.float64) * (j_idx + 1).astype(np.float64)
    phases = 2 * np.pi * jk / p
    H = amp * np.exp(1j * phases)

    # Hermitianize
    H = (H + H.conj().T) / 2
    return H

# ─── Unfolding (degree-15 polynomial, S002 style) ────────────────────────────

def unfold_eigenvalues(evals):
    """Polynomial unfolding matching S002-E001."""
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

def compute_spacings(evals, trim_fraction=0.05):
    """Compute normalized nearest-neighbor spacings with polynomial unfolding."""
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    spacings = spacings / spacings.mean()

    # Trim tails
    if trim_fraction > 0:
        n = len(spacings)
        trim = int(n * trim_fraction)
        if trim > 0:
            spacings = np.sort(spacings)
            spacings = spacings[trim:-trim] if trim < n//2 else spacings
            spacings = spacings / spacings.mean()  # Renormalize

    return spacings

# ─── Wigner Interpolated Fit (what S002 reported as "beta") ──────────────────

def wigner_interpolated_pdf(s, beta):
    """P(s; beta) = A * s^beta * exp(-B * s^2), properly normalized."""
    g1 = gamma((beta + 1) / 2)
    g2 = gamma((beta + 2) / 2)
    B = (g2 / g1) ** 2
    A = 2 * (g2 ** (beta + 1)) / (g1 ** (beta + 2))
    return A * s**beta * np.exp(-B * s**2)

def fit_wigner_interpolated_mle(spacings):
    """MLE fit for Wigner interpolated distribution."""
    def neg_log_likelihood(params):
        beta = params[0]
        if beta <= 0 or beta >= 4:
            return 1e10
        try:
            g1 = gamma((beta + 1) / 2)
            g2 = gamma((beta + 2) / 2)
            B = (g2 / g1) ** 2
            A = 2 * (g2 ** (beta + 1)) / (g1 ** (beta + 2))
            pdf = A * spacings**beta * np.exp(-B * spacings**2)
            pdf = np.clip(pdf, 1e-300, None)
            return -np.sum(np.log(pdf))
        except Exception:
            return 1e10

    result = minimize(neg_log_likelihood, x0=[1.0],
                      method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

def fit_wigner_interpolated_hist(spacings, n_bins=50):
    """Histogram-based least-squares fit (S002 method)."""
    s_max = 4.0
    bins = np.linspace(0, s_max, n_bins + 1)
    hist, edges = np.histogram(spacings, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = hist > 0

    if mask.sum() < 5:
        return np.nan

    def residuals(params):
        beta = params[0]
        if beta <= 0 or beta >= 4:
            return 1e10
        try:
            model = wigner_interpolated_pdf(centers[mask], beta)
            return np.sum((hist[mask] - model)**2)
        except Exception:
            return 1e10

    result = minimize(residuals, x0=[1.0],
                      method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

# ─── Brody Fit ───────────────────────────────────────────────────────────────

def fit_brody(spacings):
    """MLE fit for Brody distribution."""
    def neg_log_likelihood(params):
        beta = params[0]
        if beta <= 0 or beta >= 3:
            return 1e10
        b = gamma((beta + 2) / (beta + 1)) ** (beta + 1)
        pdf = (1 + beta) * b * spacings**beta * np.exp(-b * spacings**(beta + 1))
        pdf = np.clip(pdf, 1e-300, None)
        return -np.sum(np.log(pdf))

    result = minimize(neg_log_likelihood, x0=[1.0], args=(),
                      method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    N = 500
    p_values = [499, 809, 997]
    targets = {499: 0.776, 809: 1.154, 997: 1.092}

    print(f"=== Task 1 v3: N={N} Baseline with S002 Methodology ===")
    print(f"Matching: deg-15 poly unfolding, Wigner interpolated fit\n")

    mgv = precompute_mangoldt(2 * N + 1)

    results = {}

    for p in p_values:
        t0 = time.time()
        print(f"--- p={p}, N^2/p = {N**2/p:.1f} ---")

        H = build_gauss_matrix(N, p, mgv)
        eigs = eigh(H, eigvals_only=True)
        t1 = time.time()
        print(f"  Matrix + eigs: {t1-t0:.1f}s")

        # Compute spacings (no additional trimming, let unfolding handle it)
        spacings_notrim = compute_spacings(eigs, trim_fraction=0.0)
        spacings_trim05 = compute_spacings(eigs, trim_fraction=0.05)

        # Fit with different methods and trimming
        print(f"  Spacings (no trim): {len(spacings_notrim)}, (trim 5%): {len(spacings_trim05)}")

        beta_wigner_mle_notrim = fit_wigner_interpolated_mle(spacings_notrim)
        beta_wigner_hist_notrim = fit_wigner_interpolated_hist(spacings_notrim)
        beta_brody_notrim = fit_brody(spacings_notrim)

        beta_wigner_mle_trim = fit_wigner_interpolated_mle(spacings_trim05)
        beta_wigner_hist_trim = fit_wigner_interpolated_hist(spacings_trim05)
        beta_brody_trim = fit_brody(spacings_trim05)

        target = targets[p]

        print(f"  {'Method':35s} {'beta':>8} {'target':>8} {'diff':>8}")
        print(f"  {'-'*60}")
        for name, beta in [
            ("Wigner MLE (no trim)", beta_wigner_mle_notrim),
            ("Wigner Hist (no trim)", beta_wigner_hist_notrim),
            ("Brody MLE (no trim)", beta_brody_notrim),
            ("Wigner MLE (5% trim)", beta_wigner_mle_trim),
            ("Wigner Hist (5% trim)", beta_wigner_hist_trim),
            ("Brody MLE (5% trim)", beta_brody_trim),
        ]:
            diff = beta - target
            marker = " <-- MATCH" if abs(diff) < 0.05 else ""
            print(f"  {name:35s} {beta:8.4f} {target:8.3f} {diff:+8.3f}{marker}")

        results[p] = {
            'wigner_mle_notrim': beta_wigner_mle_notrim,
            'wigner_hist_notrim': beta_wigner_hist_notrim,
            'brody_notrim': beta_brody_notrim,
            'wigner_mle_trim': beta_wigner_mle_trim,
            'wigner_hist_trim': beta_wigner_hist_trim,
            'brody_trim': beta_brody_trim,
        }
        print()

    # Determine best method
    print("\n=== METHOD COMPARISON ===")
    methods = ['wigner_mle_notrim', 'wigner_hist_notrim', 'brody_notrim',
               'wigner_mle_trim', 'wigner_hist_trim', 'brody_trim']
    for method in methods:
        total_err = sum(abs(results[p][method] - targets[p]) for p in p_values)
        print(f"  {method:35s}: total |err| = {total_err:.3f}")

    # Check pass criterion for best-matching method
    print("\n=== PASS CRITERION CHECK (Wigner Hist, no trim) ===")
    beta_809 = results[809]['wigner_hist_notrim']
    beta_499 = results[499]['wigner_hist_notrim']
    print(f"  beta(p=809) = {beta_809:.4f}, in [1.05, 1.25]? {'PASS' if 1.05 <= beta_809 <= 1.25 else 'FAIL'}")
    print(f"  beta(p=499) = {beta_499:.4f}, in [0.70, 0.85]? {'PASS' if 0.70 <= beta_499 <= 0.85 else 'FAIL'}")

    # Save
    np.savez('baseline_N500.npz',
             p_values=p_values,
             results_dict=str(results),
             targets=str(targets))
    print("\nSaved to baseline_N500.npz")

if __name__ == "__main__":
    main()
