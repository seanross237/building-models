#!/usr/bin/env python3
"""Refinement: add more primes near peaks for N=250 and N=1000."""
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
from scipy.special import gamma
import time, json

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
            vals[n] = np.log(n)
        elif temp == 1:
            vals[n] = np.log(found_prime)
    return vals

def build_gauss_matrix(N, p, mgv):
    i_idx, j_idx = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    diff_abs = np.abs(i_idx - j_idx)
    amp = mgv[diff_abs + 1]
    jk = (i_idx + 1).astype(np.float64) * (j_idx + 1).astype(np.float64)
    phases = 2 * np.pi * jk / p
    H = amp * np.exp(1j * phases)
    H = (H + H.conj().T) / 2
    return H

def unfold_eigenvalues(evals):
    evals_sorted = np.sort(evals)
    n = len(evals_sorted)
    cum = np.arange(1, n + 1, dtype=float)
    x_norm = (evals_sorted - evals_sorted.mean()) / (evals_sorted.std() + 1e-10)
    poly_coeffs = np.polyfit(x_norm, cum, deg=15)
    smooth_cum = np.polyval(poly_coeffs, x_norm)
    return smooth_cum

def compute_spacings(evals):
    unfolded = unfold_eigenvalues(evals)
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    return spacings / spacings.mean()

def wigner_interpolated_pdf(s, beta):
    g1 = gamma((beta + 1) / 2)
    g2 = gamma((beta + 2) / 2)
    B = (g2 / g1) ** 2
    A = 2 * (g2 ** (beta + 1)) / (g1 ** (beta + 2))
    return A * s**beta * np.exp(-B * s**2)

def fit_wigner_hist(spacings, n_bins=50):
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
        except:
            return 1e10
    result = minimize(residuals, x0=[1.0], method='Nelder-Mead',
                      options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

def fit_brody(spacings):
    def neg_ll(params):
        beta = params[0]
        if beta <= 0 or beta >= 3:
            return 1e10
        b = gamma((beta + 2) / (beta + 1)) ** (beta + 1)
        pdf = (1 + beta) * b * spacings**beta * np.exp(-b * spacings**(beta + 1))
        pdf = np.clip(pdf, 1e-300, None)
        return -np.sum(np.log(pdf))
    result = minimize(neg_ll, x0=[1.0], method='Nelder-Mead',
                      options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

def sweep(N, primes, mgv):
    results = []
    for p in primes:
        t0 = time.time()
        H = build_gauss_matrix(N, p, mgv)
        eigs = eigh(H, eigvals_only=True)
        spacings = compute_spacings(eigs)
        bw = fit_wigner_hist(spacings)
        bb = fit_brody(spacings)
        dt = time.time() - t0
        n2p = N**2 / p
        results.append({'p': p, 'N2_over_p': n2p, 'beta_W': bw, 'beta_B': bb})
        print(f"  N={N} p={p:>5} N2/p={n2p:>7.1f} beta_W={bw:.4f} beta_B={bb:.4f} ({dt:.1f}s)")
    return results

def main():
    # N=250: refine around peak (p=271, N^2/p=231) and fill gaps
    # Need primes between 199 and 313 (N^2/p ~ 200-314)
    primes_250_refine = [211, 233, 239, 241, 257, 263, 277, 281, 293]
    # Also add some far-from-N primes for baseline shape
    primes_250_far = [149, 167, 179, 353, 397, 449, 503]

    # N=1000: refine around peak (p=3229, N^2/p=310) and add flanks
    primes_1000_refine = [2753, 2999, 3079, 3137, 3299, 3407, 3461, 3517, 3613, 3709, 3803, 4007, 4507, 4999]

    print("=== N=250 REFINEMENT ===")
    mgv250 = precompute_mangoldt(2 * 250 + 1)
    r250 = sweep(250, primes_250_refine + primes_250_far, mgv250)

    print("\n=== N=1000 REFINEMENT ===")
    mgv1000 = precompute_mangoldt(2 * 1000 + 1)
    r1000 = sweep(1000, primes_1000_refine, mgv1000)

    # Merge with original results
    import json
    with open('task2_n250_results.json') as f:
        orig250 = json.load(f)
    with open('task3_n1000_results.json') as f:
        orig1000 = json.load(f)

    all250 = orig250['results'] + r250
    all1000 = orig1000['results'] + r1000

    # Sort by N^2/p
    all250.sort(key=lambda x: x['N2_over_p'])
    all1000.sort(key=lambda x: x['N2_over_p'])

    print("\n=== FULL N=250 TABLE (sorted by N^2/p) ===")
    print(f"{'p':>6} {'N2/p':>8} {'beta_W':>8} {'beta_B':>8}")
    print("-" * 36)
    for r in all250:
        marker = " <-- PEAK" if r['beta_W'] == max(x['beta_W'] for x in all250) else ""
        marker2 = " <-- p~N ANOMALY" if abs(r['p'] - 250) < 5 else ""
        print(f"{r['p']:>6} {r['N2_over_p']:>8.1f} {r['beta_W']:>8.4f} {r['beta_B']:>8.4f}{marker}{marker2}")

    peak250 = max(all250, key=lambda x: x['beta_W'])
    print(f"\nN=250 PEAK: p={peak250['p']}, N^2/p={peak250['N2_over_p']:.1f}, beta_W={peak250['beta_W']:.4f}")

    print("\n=== FULL N=1000 TABLE (sorted by N^2/p) ===")
    print(f"{'p':>6} {'N2/p':>8} {'beta_W':>8} {'beta_B':>8}")
    print("-" * 36)
    for r in all1000:
        marker = " <-- PEAK" if r['beta_W'] == max(x['beta_W'] for x in all1000) else ""
        print(f"{r['p']:>6} {r['N2_over_p']:>8.1f} {r['beta_W']:>8.4f} {r['beta_B']:>8.4f}{marker}")

    peak1000 = max(all1000, key=lambda x: x['beta_W'])
    print(f"\nN=1000 PEAK: p={peak1000['p']}, N^2/p={peak1000['N2_over_p']:.1f}, beta_W={peak1000['beta_W']:.4f}")

    # Universality comparison
    print("\n\n=== UNIVERSALITY COMPARISON ===")
    print(f"{'N':>6} {'p_opt':>8} {'N2/p_opt':>10} {'beta_max':>10}")
    print("-" * 40)
    print(f"{'250':>6} {peak250['p']:>8} {peak250['N2_over_p']:>10.1f} {peak250['beta_W']:>10.4f}")
    print(f"{'500':>6} {'809':>8} {'309.0':>10} {'1.1543':>10}")
    print(f"{'1000':>6} {peak1000['p']:>8} {peak1000['N2_over_p']:>10.1f} {peak1000['beta_W']:>10.4f}")

    target_ratio = 275
    print(f"\nHypothesized universal N^2/p_opt ≈ {target_ratio}")
    print(f"  N=250:  N^2/p_opt = {peak250['N2_over_p']:.1f}  (ratio to 275: {peak250['N2_over_p']/target_ratio:.2f})")
    print(f"  N=500:  N^2/p_opt = 309.0  (ratio to 275: {309.0/target_ratio:.2f})")
    print(f"  N=1000: N^2/p_opt = {peak1000['N2_over_p']:.1f}  (ratio to 275: {peak1000['N2_over_p']/target_ratio:.2f})")

    # Save merged results
    with open('all_results_merged.json', 'w') as f:
        json.dump({
            'N250': {'results': all250, 'peak': peak250},
            'N500': {'results': [
                {'p': 499, 'N2_over_p': 501.0, 'beta_W': 0.7434, 'beta_B': 0.7762},
                {'p': 809, 'N2_over_p': 309.0, 'beta_W': 1.1543, 'beta_B': 1.0099},
                {'p': 997, 'N2_over_p': 250.8, 'beta_W': 1.0921, 'beta_B': 0.9587},
            ], 'peak': {'p': 809, 'N2_over_p': 309.0, 'beta_W': 1.1543, 'beta_B': 1.0099}},
            'N1000': {'results': all1000, 'peak': peak1000},
        }, f, indent=2)
    print("\nSaved all_results_merged.json")

if __name__ == "__main__":
    main()
