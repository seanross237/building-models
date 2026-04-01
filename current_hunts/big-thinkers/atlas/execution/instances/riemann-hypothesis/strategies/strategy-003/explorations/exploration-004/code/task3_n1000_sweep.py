#!/usr/bin/env python3
"""Task 3: N=1000 sweep over primes near N^2/p ~ 250-310."""
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

def main():
    N = 1000
    primes = [3229, 3571, 3989, 1999, 9973]
    mgv = precompute_mangoldt(2 * N + 1)

    print(f"=== N={N} SWEEP ===")
    print(f"{'p':>6} {'N2/p':>8} {'beta_W':>8} {'beta_B':>8} {'time':>8}")
    print("-" * 44)

    results = []
    for p in primes:
        t0 = time.time()
        print(f"Starting p={p} (N^2/p={N**2/p:.1f})...", flush=True)
        H = build_gauss_matrix(N, p, mgv)
        t1 = time.time()
        print(f"  Matrix built in {t1-t0:.1f}s, computing eigenvalues...", flush=True)
        eigs = eigh(H, eigvals_only=True)
        t2 = time.time()
        print(f"  Eigenvalues in {t2-t1:.1f}s, fitting...", flush=True)
        spacings = compute_spacings(eigs)
        bw = fit_wigner_hist(spacings)
        bb = fit_brody(spacings)
        dt = time.time() - t0
        n2p = N**2 / p
        results.append({'p': p, 'N2_over_p': n2p, 'beta_W': bw, 'beta_B': bb})
        print(f"{p:>6} {n2p:>8.1f} {bw:>8.4f} {bb:>8.4f} {dt:>7.1f}s")

    betas = [r['beta_W'] for r in results]
    peak_idx = np.argmax(betas)
    peak = results[peak_idx]
    print(f"\nPEAK: p={peak['p']}, N^2/p={peak['N2_over_p']:.1f}, beta_W={peak['beta_W']:.4f}")

    with open('task3_n1000_results.json', 'w') as f:
        json.dump({'N': N, 'results': results, 'peak': peak}, f, indent=2)
    print("Saved task3_n1000_results.json")

if __name__ == "__main__":
    main()
