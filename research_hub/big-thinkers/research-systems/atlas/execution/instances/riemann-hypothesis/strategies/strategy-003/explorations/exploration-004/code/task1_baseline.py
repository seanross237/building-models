#!/usr/bin/env python3
"""Task 1: Replicate N=500 Baseline for Gauss Sum Matrix."""

import numpy as np
from scipy.special import gamma
from scipy.optimize import minimize
from sympy import isprime, factorint
import time
import sys

def von_mangoldt(n):
    """Compute von Mangoldt function Lambda(n).
    Lambda(n) = log(p) if n = p^k for some prime p and integer k >= 1, else 0.
    """
    if n <= 0:
        return 0.0
    if n == 1:
        return 0.0
    factors = factorint(n)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        return float(np.log(p))
    return 0.0

def build_gauss_sum_matrix(N, p):
    """Build Hermitianized Gauss sum matrix H_{jk} = Lambda(|j-k|+1) * exp(2*pi*i*j*k/p).
    Uses 1-INDEXED construction (critical for correct results).
    """
    # Precompute von Mangoldt values for all needed arguments
    # |j-k| ranges from 0 to N-1, so |j-k|+1 ranges from 1 to N
    vm_values = np.array([von_mangoldt(n) for n in range(1, N+1)])

    H = np.zeros((N, N), dtype=complex)
    for j in range(1, N+1):
        for k in range(1, N+1):
            amplitude = vm_values[abs(j-k)]  # vm_values[0] = Lambda(1) = 0, etc.
            phase = np.exp(2 * np.pi * 1j * j * k / p)
            H[j-1, k-1] = amplitude * phase

    # Hermitianize
    H = (H + H.conj().T) / 2
    return H

def compute_spacings(eigenvalues, trim_fraction=0.05):
    """Compute normalized nearest-neighbor spacings.
    Trim outliers from both tails, then unfold by dividing by mean spacing.
    """
    eigs = np.sort(np.real(eigenvalues))
    n = len(eigs)
    trim = int(n * trim_fraction)
    eigs = eigs[trim:n-trim]

    spacings = np.diff(eigs)
    mean_spacing = np.mean(spacings)
    if mean_spacing > 0:
        spacings = spacings / mean_spacing

    # Remove any zero or negative spacings
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
    beta_values = []

    print(f"=== Task 1: N={N} Baseline Replication ===")
    print(f"Testing p values: {p_values}")
    print()

    for p in p_values:
        t0 = time.time()
        print(f"--- p={p}, N^2/p = {N**2/p:.1f} ---")

        # Build matrix
        print(f"  Building {N}x{N} matrix...", end=" ", flush=True)
        H = build_gauss_sum_matrix(N, p)
        t1 = time.time()
        print(f"done ({t1-t0:.1f}s)")

        # Compute eigenvalues
        print(f"  Computing eigenvalues...", end=" ", flush=True)
        eigs = np.linalg.eigvalsh(H)
        t2 = time.time()
        print(f"done ({t2-t1:.1f}s)")

        # Compute spacings
        spacings = compute_spacings(eigs, trim_fraction=0.05)
        print(f"  Spacings: {len(spacings)} (after trimming)")

        # Fit Brody beta
        beta = fit_brody(spacings)
        beta_values.append(beta)
        t3 = time.time()
        print(f"  Brody beta = {beta:.4f}")
        print(f"  Total time: {t3-t0:.1f}s")
        print()

    # Report results
    print("=== RESULTS ===")
    print(f"{'p':>8} {'N^2/p':>8} {'beta':>8} {'target':>10}")
    print("-" * 40)
    targets = {499: 0.776, 809: 1.154, 997: 1.092}
    for p, beta in zip(p_values, beta_values):
        target = targets.get(p, '?')
        print(f"{p:>8} {N**2/p:>8.1f} {beta:>8.4f} {target:>10}")

    # Save results
    np.savez('baseline_N500.npz', p_values=p_values, beta_values=beta_values)
    print("\nSaved to baseline_N500.npz")

    # Verify pass criteria
    beta_809 = beta_values[1]  # p=809
    beta_499 = beta_values[0]  # p=499
    pass_809 = 1.05 <= beta_809 <= 1.25
    pass_499 = 0.70 <= beta_499 <= 0.85
    print(f"\nPASS criteria:")
    print(f"  beta(p=809) in [1.05, 1.25]: {beta_809:.4f} -> {'PASS' if pass_809 else 'FAIL'}")
    print(f"  beta(p=499) in [0.70, 0.85]: {beta_499:.4f} -> {'PASS' if pass_499 else 'FAIL'}")

    if pass_809 and pass_499:
        print("\n*** BASELINE VERIFIED ***")
    else:
        print("\n*** BASELINE FAILED — DEBUG NEEDED ***")

if __name__ == "__main__":
    main()
