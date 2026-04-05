#!/usr/bin/env python3
"""Task 1 v2: Replicate N=500 Baseline with polynomial unfolding."""

import numpy as np
from scipy.special import gamma
from scipy.optimize import minimize
from sympy import isprime, factorint
import time

def von_mangoldt(n):
    """Compute von Mangoldt function Lambda(n)."""
    if n <= 0 or n == 1:
        return 0.0
    factors = factorint(n)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        return float(np.log(p))
    return 0.0

def build_gauss_sum_matrix(N, p):
    """Build Hermitianized Gauss sum matrix (1-INDEXED)."""
    vm_values = np.array([von_mangoldt(n) for n in range(1, N+1)])
    H = np.zeros((N, N), dtype=complex)
    for j in range(1, N+1):
        for k in range(1, N+1):
            amplitude = vm_values[abs(j-k)]
            phase = np.exp(2 * np.pi * 1j * j * k / p)
            H[j-1, k-1] = amplitude * phase
    H = (H + H.conj().T) / 2
    return H

def compute_spacings_simple(eigenvalues, trim_fraction=0.05):
    """Simple unfolding: divide by mean spacing."""
    eigs = np.sort(np.real(eigenvalues))
    n = len(eigs)
    trim = int(n * trim_fraction)
    eigs = eigs[trim:n-trim]
    spacings = np.diff(eigs)
    mean_spacing = np.mean(spacings)
    if mean_spacing > 0:
        spacings = spacings / mean_spacing
    spacings = spacings[spacings > 1e-10]
    return spacings

def compute_spacings_poly(eigenvalues, trim_fraction=0.05, poly_degree=6):
    """Polynomial unfolding: fit smooth staircase, then compute spacings."""
    eigs = np.sort(np.real(eigenvalues))
    n = len(eigs)
    trim = int(n * trim_fraction)
    eigs_trimmed = eigs[trim:n-trim]

    # Staircase function: N(E_i) = i+1 for sorted eigenvalues
    staircase = np.arange(1, len(eigs_trimmed) + 1, dtype=float)

    # Fit polynomial to staircase
    coeffs = np.polyfit(eigs_trimmed, staircase, poly_degree)
    N_smooth = np.polyval(coeffs, eigs_trimmed)

    # Unfolded spacings
    spacings = np.diff(N_smooth)
    spacings = spacings[spacings > 1e-10]
    return spacings

def brody_neg_log_likelihood(params, spacings):
    """Negative log-likelihood for Brody distribution."""
    beta = params[0]
    if beta <= 0 or beta >= 3:
        return 1e10
    b = gamma((beta + 2) / (beta + 1)) ** (beta + 1)
    pdf = (1 + beta) * b * spacings**beta * np.exp(-b * spacings**(beta + 1))
    pdf = np.clip(pdf, 1e-300, None)
    return -np.sum(np.log(pdf))

def fit_brody(spacings):
    """Fit Brody parameter beta using MLE with Nelder-Mead."""
    result = minimize(brody_neg_log_likelihood, x0=[1.0], args=(spacings,),
                      method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-8, 'maxiter': 10000})
    return result.x[0]

def main():
    N = 500
    p_values = [499, 809, 997]
    targets = {499: 0.776, 809: 1.154, 997: 1.092}

    print(f"=== Task 1 v2: N={N} Baseline with Different Unfolding Methods ===\n")

    for p in p_values:
        t0 = time.time()
        print(f"--- p={p}, N^2/p = {N**2/p:.1f} ---")

        H = build_gauss_sum_matrix(N, p)
        eigs = np.linalg.eigvalsh(H)
        t1 = time.time()
        print(f"  Matrix + eigenvalues: {t1-t0:.1f}s")

        # Test different unfolding methods
        for method_name, method_func in [
            ("simple (mean)", lambda e: compute_spacings_simple(e, 0.05)),
            ("poly deg=5", lambda e: compute_spacings_poly(e, 0.05, 5)),
            ("poly deg=7", lambda e: compute_spacings_poly(e, 0.05, 7)),
            ("poly deg=9", lambda e: compute_spacings_poly(e, 0.05, 9)),
            ("simple trim=0.10", lambda e: compute_spacings_simple(e, 0.10)),
            ("poly deg=7 trim=0.10", lambda e: compute_spacings_poly(e, 0.10, 7)),
        ]:
            spacings = method_func(eigs)
            beta = fit_brody(spacings)
            target = targets[p]
            diff = beta - target
            print(f"  {method_name:25s}: beta = {beta:.4f}  (target {target:.3f}, diff {diff:+.3f})")

        print()

    print("Target criterion: beta(p=809) in [1.05, 1.25]")

if __name__ == "__main__":
    main()
