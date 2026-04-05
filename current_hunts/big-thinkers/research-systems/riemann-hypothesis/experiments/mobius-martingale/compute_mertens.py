#!/usr/bin/env python3
"""
Compute the Mertens function M(x) and related statistics.
Investigates the near-martingale structure of the Mobius function.
"""

import numpy as np
import time

def compute_mobius_sieve(limit):
    """Compute μ(n) for n = 1, ..., limit using a sieve."""
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0

    # Sieve of Eratosthenes style
    is_prime_factor_count = np.zeros(limit + 1, dtype=np.int8)
    has_square_factor = np.zeros(limit + 1, dtype=bool)

    for p in range(2, limit + 1):
        if is_prime_factor_count[p] == 0:  # p is prime
            # Mark all multiples of p
            for multiple in range(p, limit + 1, p):
                is_prime_factor_count[multiple] += 1
            # Mark all multiples of p² as having square factor
            p2 = p * p
            if p2 <= limit:
                for multiple in range(p2, limit + 1, p2):
                    has_square_factor[multiple] = True

    # μ(n) = 0 if n has a square factor
    # μ(n) = (-1)^k if n has k distinct prime factors
    for n in range(1, limit + 1):
        if has_square_factor[n]:
            mu[n] = 0
        else:
            mu[n] = (-1) ** is_prime_factor_count[n]

    return mu

def compute_mobius_fast(limit):
    """Faster sieve for μ(n) using numpy vectorization where possible."""
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0

    # Track number of prime factors and square factors
    smallest_prime = np.zeros(limit + 1, dtype=np.int64)

    for p in range(2, int(limit**0.5) + 1):
        if smallest_prime[p] == 0:  # p is prime
            # Mark composites
            smallest_prime[p*p::p][smallest_prime[p*p::p] == 0] = p
    # Remaining unmarked numbers > 1 are prime
    for n in range(2, limit + 1):
        if smallest_prime[n] == 0:
            smallest_prime[n] = n

    # Actually, let's use a simpler direct sieve
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0

    # For each prime p, multiply mu[kp] by -1 and set mu[kp²] = 0
    sieve = np.ones(limit + 1, dtype=bool)  # is_prime sieve
    sieve[0] = sieve[1] = False

    for p in range(2, limit + 1):
        if not sieve[p]:
            continue
        # p is prime
        # Mark composites for prime sieve
        if p * p <= limit:
            sieve[p*p::p] = False

        # For Mobius: multiply by -1 for each prime factor
        mu[p::p] *= -1

        # Set to 0 for square factors
        p2 = p * p
        if p2 <= limit:
            mu[p2::p2] = 0

    return mu

def main():
    LIMIT = 10_000_000  # 10^7

    print(f"Computing μ(n) for n = 1 to {LIMIT:,}...")
    t0 = time.time()
    mu = compute_mobius_fast(LIMIT)
    t1 = time.time()
    print(f"  Done in {t1-t0:.2f}s")

    # Compute Mertens function
    print("Computing M(x) = cumulative sum of μ...")
    M = np.cumsum(mu)

    # Basic statistics
    x_vals = np.arange(1, LIMIT + 1)
    sqrt_x = np.sqrt(x_vals)
    normalized = M[1:] / sqrt_x  # M(x)/√x

    print(f"\n=== Mertens Function Statistics (up to {LIMIT:,}) ===")
    print(f"M({LIMIT:,}) = {M[LIMIT]}")
    print(f"max |M(x)| = {np.max(np.abs(M[1:]))}")
    print(f"max |M(x)|/√x = {np.max(np.abs(normalized)):.6f}")
    print(f"argmax |M(x)|/√x at x = {np.argmax(np.abs(normalized)) + 1}")

    # Values at powers of 10
    print(f"\n=== M(x) at powers of 10 ===")
    for k in range(1, 8):
        x = 10**k
        if x <= LIMIT:
            print(f"  M(10^{k}) = {M[x]:>8d},  M/√x = {M[x]/np.sqrt(x):>8.4f}")

    # Distribution of μ
    print(f"\n=== Distribution of μ(n) for n ≤ {LIMIT:,} ===")
    for val in [-1, 0, 1]:
        count = np.sum(mu[1:LIMIT+1] == val)
        print(f"  μ(n) = {val:>2d}: {count:>8,} ({100*count/LIMIT:.2f}%)")

    # Check: density of squarefree numbers should be 6/π² ≈ 0.6079
    squarefree_count = np.sum(mu[1:LIMIT+1] != 0)
    print(f"  Squarefree density: {squarefree_count/LIMIT:.6f} (theory: {6/np.pi**2:.6f})")

    # Normalized Mertens function: check if M(x)/√x stays bounded
    print(f"\n=== Extrema of M(x)/√x ===")
    print(f"  max M(x)/√x = {np.max(normalized):.6f}")
    print(f"  min M(x)/√x = {np.min(normalized):.6f}")

    # Check at various scales
    print(f"\n=== max|M(x)|/√x over intervals ===")
    for k in range(2, 8):
        lo = 10**(k-1)
        hi = min(10**k, LIMIT)
        seg = np.abs(normalized[lo-1:hi])
        print(f"  [{10**(k-1):>10,}, {hi:>10,}]: max|M|/√x = {np.max(seg):.6f}")

    # Variance analysis: Var(M(x)) vs x
    print(f"\n=== Variance Analysis ===")
    # For a random walk, Var(S_n) = n * Var(step)
    # For M(x), if μ were i.i.d., Var(M(x)) = x * Var(μ(n))
    # Var(μ(n)) = E[μ(n)²] - E[μ(n)]² ≈ 6/π² (since μ² = 1 iff squarefree)
    var_step = 6 / np.pi**2
    print(f"  Var(μ(n)) = E[μ²] ≈ {var_step:.6f} (squarefree density)")
    print(f"  If i.i.d.: std(M(x)) ≈ √(x·{var_step:.4f}) = {np.sqrt(var_step):.4f}·√x")

    # Empirical: compute M(x)² at sample points and compare to x
    sample_points = [10**k for k in range(3, 8) if 10**k <= LIMIT]
    print(f"\n  Empirical M(x)²/x vs theory ({var_step:.4f}):")
    for x in sample_points:
        empirical = M[x]**2 / x
        print(f"    x = {x:>10,}: M(x)²/x = {empirical:.4f} (M(x) = {M[x]})")

    # Auto-correlation analysis
    print(f"\n=== Auto-correlation of μ(n) ===")
    mu_centered = mu[1:100001].astype(np.float64)  # use first 100k
    N_ac = len(mu_centered)
    mu_centered = mu_centered - np.mean(mu_centered)
    var0 = np.var(mu_centered)

    print(f"  Lag  | Autocorrelation")
    for lag in [1, 2, 3, 5, 6, 10, 12, 30]:
        if lag < N_ac:
            corr = np.mean(mu_centered[:N_ac-lag] * mu_centered[lag:]) / var0
            print(f"  {lag:>4d} | {corr:>10.6f}")

    # Save key data for plotting
    save_data = {
        'M_at_powers': {10**k: int(M[10**k]) for k in range(1, 8) if 10**k <= LIMIT},
        'max_normalized': float(np.max(np.abs(normalized))),
        'squarefree_density': float(squarefree_count / LIMIT),
    }
    print(f"\n=== Key data for findings ===")
    for k, v in save_data.items():
        print(f"  {k}: {v}")

    # Detailed: M(x)/√x at many points for trend analysis
    print(f"\n=== M(x)/x^(1/2+ε) boundedness check ===")
    for eps in [0, 0.01, 0.05, 0.1]:
        max_ratio = np.max(np.abs(M[1:]) / (x_vals ** (0.5 + eps)))
        print(f"  ε = {eps:.2f}: max |M(x)|/x^(0.5+ε) = {max_ratio:.6f}")

    return mu, M

if __name__ == "__main__":
    mu, M = main()
