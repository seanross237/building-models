#!/usr/bin/env python3
"""
Compute Li's criterion coefficients λ_n for the Riemann Hypothesis.

λ_n = Σ_ρ [1 − (1 − 1/ρ)^n] summed over ALL non-trivial zeros ρ.

Uses mpmath at 50-digit precision with the first 2000 zero pairs (4000 zeros total).
Pre-computes all zeros first, then iterates over n values.
"""

import time
import os
import pickle
import numpy as np
from mpmath import mp, mpf, mpc, zetazero, log, pi, euler, fsum, re as mpre, im as mpim

mp.dps = 50  # 50 decimal digits of precision

WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.dirname(os.path.abspath(__file__))

NUM_ZEROS = 2000
MAX_N = 500

def precompute_zeros(num_zeros=NUM_ZEROS):
    """Pre-compute all zeta zeros. Returns list of zeros in upper half plane."""
    cache_file = os.path.join(CODE_DIR, 'zeros_cache.pkl')

    # Check for cached zeros
    if os.path.exists(cache_file):
        print(f"Loading cached zeros from {cache_file}")
        with open(cache_file, 'rb') as f:
            zeros = pickle.load(f)
        if len(zeros) >= num_zeros:
            print(f"Loaded {len(zeros)} cached zeros")
            return zeros[:num_zeros]
        else:
            print(f"Cache has only {len(zeros)} zeros, need {num_zeros}. Recomputing...")

    print(f"Pre-computing {num_zeros} zeta zeros at {mp.dps}-digit precision...")
    zeros = []
    t0 = time.time()

    for k in range(1, num_zeros + 1):
        rho = zetazero(k)
        zeros.append(rho)
        if k % 100 == 0:
            elapsed = time.time() - t0
            rate = k / elapsed
            eta = (num_zeros - k) / rate
            print(f"  Zero {k}/{num_zeros}: ρ = 0.5 + {float(mpim(rho)):.6f}i  "
                  f"[{elapsed:.1f}s elapsed, ETA {eta:.0f}s, rate {rate:.1f}/s]")

    elapsed = time.time() - t0
    print(f"Done computing {num_zeros} zeros in {elapsed:.1f}s")

    # Cache the zeros
    with open(cache_file, 'wb') as f:
        pickle.dump(zeros, f)
    print(f"Cached zeros to {cache_file}")

    return zeros


def compute_lambda_n(n, zeros):
    """
    Compute λ_n = Σ_ρ [1 − (1 − 1/ρ)^n] over all zeros and their conjugates.

    Each zero ρ = 1/2 + i*t in the upper half plane has a conjugate ρ̄ = 1/2 - i*t.
    Both contribute to the sum.
    """
    terms = []
    for rho in zeros:
        # Contribution from ρ (upper half plane)
        term_rho = 1 - (1 - 1/rho)**n
        # Contribution from ρ̄ = conjugate (lower half plane)
        rho_bar = rho.conjugate()
        term_rho_bar = 1 - (1 - 1/rho_bar)**n
        terms.append(term_rho + term_rho_bar)

    # Use fsum for accurate summation
    result = fsum(terms)
    return result


def compute_all_lambdas(max_n, zeros):
    """Compute λ_n for n=1 to max_n using pre-computed zeros."""
    lambdas = {}
    t0 = time.time()

    for n in range(1, max_n + 1):
        lam = compute_lambda_n(n, zeros)
        lambdas[n] = lam

        # Sanity: λ_n should be real (imaginary part from numerical noise)
        real_part = float(mpre(lam))
        imag_part = float(mpim(lam))

        if n <= 20 or n % 50 == 0 or n == max_n:
            elapsed = time.time() - t0
            print(f"  λ_{n} = {float(mpre(lam)):.15f} (imag: {imag_part:.2e})  [{elapsed:.1f}s]")

        # CRITICAL CHECK: λ_n must be positive for RH
        if real_part < 0:
            print(f"\n!!! CRITICAL: λ_{n} = {real_part} < 0 !!!")
            print(f"!!! This would FALSIFY the Riemann Hypothesis !!!")
            print(f"!!! Double-check this value immediately !!!\n")

    return lambdas


def save_results(lambdas, zeros):
    """Save computed values to npz file."""
    # Convert to numpy arrays for storage
    n_values = sorted(lambdas.keys())
    lambda_real = np.array([float(mpre(lambdas[n])) for n in n_values])
    lambda_imag = np.array([float(mpim(lambdas[n])) for n in n_values])

    # Also save zero imaginary parts for reference
    zero_imag_parts = np.array([float(mpim(z)) for z in zeros])

    npz_file = os.path.join(CODE_DIR, 'li_coefficients.npz')
    np.savez(npz_file,
             n_values=np.array(n_values),
             lambda_real=lambda_real,
             lambda_imag=lambda_imag,
             zero_imag_parts=zero_imag_parts,
             num_zeros=NUM_ZEROS,
             precision=mp.dps)
    print(f"Saved results to {npz_file}")
    return npz_file


def expected_lambda_1():
    """Compute expected λ_1 from Bombieri-Lagarias formula."""
    # λ_1 = 1 + γ/2 - log(2) - (1/2)*log(π)
    # = log(4π)/2 + γ/2 - 1 - log(2)  ... let me compute it directly
    # Actually: λ_1 = Σ_ρ 1/ρ (for all non-trivial zeros)
    # Known value: λ_1 = 1 + γ/2 - log(2) - (1/2)*log(π) ≈ 0.0231...
    # Let me just compute it from the known formula
    val = 1 + euler/2 - log(2) - log(pi)/2
    return val


if __name__ == '__main__':
    print("=" * 70)
    print("Li's Criterion Coefficient Computation")
    print(f"Precision: {mp.dps} digits, Zeros: {NUM_ZEROS} pairs ({2*NUM_ZEROS} total)")
    print("=" * 70)

    # Step 1: Pre-compute zeros
    print("\n--- Step 1: Pre-computing zeta zeros ---")
    zeros = precompute_zeros()

    # Save zeros immediately
    zero_imag = np.array([float(mpim(z)) for z in zeros])
    np.savez(os.path.join(CODE_DIR, 'zeros.npz'),
             zero_imag_parts=zero_imag, num_zeros=NUM_ZEROS)
    print(f"First 5 zeros (imag parts): {zero_imag[:5]}")
    print(f"Last zero (imag part): {zero_imag[-1]:.6f}")

    # Step 2: Sanity check λ_1
    print("\n--- Step 2: Sanity check λ_1 ---")
    expected = expected_lambda_1()
    print(f"Expected λ_1 (Bombieri-Lagarias): {float(expected):.15f}")

    # Step 3: Compute all λ_n
    print(f"\n--- Step 3: Computing λ_n for n=1 to {MAX_N} ---")
    t_start = time.time()
    lambdas = compute_all_lambdas(MAX_N, zeros)
    t_total = time.time() - t_start
    print(f"\nTotal computation time for λ_n: {t_total:.1f}s")

    # Verify λ_1
    computed_l1 = float(mpre(lambdas[1]))
    expected_l1 = float(expected)
    print(f"\nλ_1 computed: {computed_l1:.15f}")
    print(f"λ_1 expected: {expected_l1:.15f}")
    print(f"Difference:   {abs(computed_l1 - expected_l1):.2e}")

    # Check all positive
    all_positive = all(float(mpre(lambdas[n])) > 0 for n in lambdas)
    min_lambda = min(float(mpre(lambdas[n])) for n in lambdas)
    min_n = min(lambdas.keys(), key=lambda n: float(mpre(lambdas[n])))
    print(f"\nAll λ_n > 0: {all_positive}")
    print(f"Minimum λ_n: λ_{min_n} = {min_lambda:.15f}")

    # Save
    print("\n--- Step 4: Saving results ---")
    save_results(lambdas, zeros)

    # Print summary table
    print("\n--- Summary Table (selected values) ---")
    print(f"{'n':>5} | {'λ_n':>25} | {'Positive?':>10}")
    print("-" * 50)
    for n in [1, 2, 3, 4, 5, 10, 20, 50, 100, 200, 300, 400, 500]:
        if n in lambdas:
            val = float(mpre(lambdas[n]))
            print(f"{n:>5} | {val:>25.15f} | {'YES' if val > 0 else '*** NO ***':>10}")

    print("\n=== DONE ===")
