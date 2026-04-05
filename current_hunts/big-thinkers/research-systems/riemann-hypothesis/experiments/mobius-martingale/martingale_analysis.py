#!/usr/bin/env python3
"""
Martingale decomposition of M(x) through the prime-by-prime filtration.

For each prime p, we decompose the Mertens function into contributions from
divisibility by successive primes. This script:

1. Computes the "partial Mertens" function after accounting for first k primes
2. Computes the "innovation" (martingale difference) at each prime step
3. Verifies the variance decomposition
4. Tests the near-martingale property of the actual μ function
"""

import numpy as np
import time
from collections import defaultdict

def sieve_primes(limit):
    """Sieve of Eratosthenes."""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    return np.where(is_prime)[0]

def compute_mobius(limit):
    """Compute μ(n) for n = 1, ..., limit."""
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False

    for p in range(2, limit + 1):
        if not sieve[p]:
            continue
        if p * p <= limit:
            sieve[p*p::p] = False
        mu[p::p] *= -1
        p2 = p * p
        if p2 <= limit:
            mu[p2::p2] = 0
    return mu

def prime_filtration_analysis(x):
    """
    Analyze M(x) through the prime-by-prime filtration.

    For a uniform random N in {1,...,x}, define:
      G_k = sigma(1_{p_j | N} : j <= k)

    The "partial Mobius" after k primes is:
      E[mu(N) | G_k]

    And the sum M_k(x) = sum_{n=1}^x E[mu(n) | G_k]

    We compute this explicitly.
    """
    print(f"\n{'='*60}")
    print(f"PRIME FILTRATION ANALYSIS for x = {x:,}")
    print(f"{'='*60}")

    primes = sieve_primes(x)
    mu = compute_mobius(x)
    M_true = np.sum(mu[1:x+1])

    print(f"Number of primes up to {x}: {len(primes)}")
    print(f"True M({x}) = {M_true}")

    # For the prime-by-prime filtration, we work with the "partial Euler product"
    # idea. After accounting for primes p_1, ..., p_k, the contribution to M(x)
    # from numbers whose factorization involves only these primes is determined.

    # More precisely: define f_k(n) = product over p_j | n, j <= k, of (-1)
    # times the indicator that n is not divisible by p_j^2 for j <= k.
    # Then the "partial Mobius" considering only the first k primes.

    # The Euler product decomposition gives us:
    # M(x) = sum_{n<=x} mu(n) = sum_{n<=x} prod_{p|n} (-1) * 1_{n squarefree}

    # Let's track the partial product approach.
    # Start with all n having "tentative mu" = 1.
    # At each prime p, for multiples of p: multiply by -1.
    # For multiples of p^2: set to 0.
    # After processing all primes: we have the true mu.

    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0

    partial_sums = []  # M_k(x) after processing k primes
    innovations = []   # M_k(x) - M_{k-1}(x)

    prev_sum = np.sum(partial_mu[1:x+1])  # Before any prime: sum of 1's = x

    for idx, p in enumerate(primes):
        # Process prime p:
        # For multiples of p (not already zeroed by p^2): multiply by -1
        # For multiples of p^2: set to 0

        p2 = p * p

        # First, zero out multiples of p^2
        if p2 <= x:
            partial_mu[p2::p2] = 0.0

        # Then, for multiples of p (that aren't zero), multiply by -1
        partial_mu[p::p] *= -1  # This handles the sign flip
        # But wait, we zeroed p^2 multiples first, so their -1 flip is -1*0 = 0. Good.
        # Actually no — we zeroed them, then multiplied by -1, getting 0*(-1) = 0.
        # Hmm, but we want: zero them AND flip sign of p-multiples not divisible by p^2.

        # Let me redo this more carefully.
        # We need to be careful about order. Let's reset and do it properly.
        pass

    # Redo: build partial_mu step by step
    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0

    # After processing prime p, partial_mu[n] should be:
    # Product over primes q <= p of:
    #   (-1) if q | n and q^2 does not divide n
    #   0 if q^2 | n
    #   1 if q does not divide n

    prev_sum = float(x)  # sum of all 1's
    partial_sums = [prev_sum]
    innovations = []
    prime_labels = ['(none)']

    for idx, p in enumerate(primes):
        # For each n, we need to update partial_mu[n] based on divisibility by p.
        # If p^2 | n: partial_mu[n] = 0 (regardless of previous value)
        # If p | n but p^2 does not divide n: partial_mu[n] *= (-1)
        # If p does not divide n: no change

        p2 = p * p

        # Handle p^2 multiples first (set to zero)
        if p2 <= x:
            partial_mu[p2::p2] = 0.0

        # Handle p multiples (but not p^2 multiples) — multiply by -1
        # We need multiples of p that are NOT multiples of p^2
        for n in range(p, x + 1, p):
            if n % p2 != 0:
                partial_mu[n] *= -1
            # If n % p2 == 0, it's already zeroed

        current_sum = np.sum(partial_mu[1:x+1])
        innovation = current_sum - prev_sum

        partial_sums.append(current_sum)
        innovations.append(innovation)
        prime_labels.append(str(p))

        prev_sum = current_sum

        # Show first several and occasionally after
        if idx < 15 or (idx < 100 and idx % 10 == 0) or idx % 100 == 0:
            print(f"  After prime p_{idx+1}={p:>5d}: M_k = {current_sum:>10.0f}, "
                  f"innovation = {innovation:>10.0f}, "
                  f"|innovation|/√x = {abs(innovation)/np.sqrt(x):>8.4f}")

    final_sum = partial_sums[-1]
    print(f"\n  Final partial sum after all primes: {final_sum:.0f}")
    print(f"  True M({x}) = {M_true}")
    print(f"  Match: {abs(final_sum - M_true) < 1e-6}")

    # Variance decomposition
    innovations_arr = np.array(innovations)
    print(f"\n=== Innovation (Martingale Difference) Statistics ===")
    print(f"  Number of innovations: {len(innovations_arr)}")
    print(f"  Sum of innovations: {np.sum(innovations_arr):.0f} (should be {M_true - x})")
    print(f"  Sum of |innovations|: {np.sum(np.abs(innovations_arr)):.0f}")

    # If this were a true martingale, the variance of the sum would equal
    # the sum of the variances of the innovations.
    # Here we check: M(x) - x = sum of innovations
    # and |M(x) - x|^2 vs sum of innovation^2

    total_innovation_sq = np.sum(innovations_arr**2)
    print(f"  Sum of innovation^2: {total_innovation_sq:.2f}")
    print(f"  (M(x) - x)^2: {(M_true - x)**2}")
    print(f"  Ratio: {(M_true - x)**2 / total_innovation_sq:.6f}")

    # The ratio being much less than 1 means cancellations are happening
    # (innovations have different signs), as expected for a "random walk"

    # Innovation size by prime size
    print(f"\n=== Innovation Size by Prime ===")
    print(f"  Largest |innovation|: {np.max(np.abs(innovations_arr)):.0f} at prime {primes[np.argmax(np.abs(innovations_arr))]}")

    # Expected innovation size: for prime p, about x/p numbers are divisible by p.
    # Each such number flips sign, contributing ≈ 2 * (current partial mu value) to the innovation.
    # The net innovation should be ≈ -2 * (sum of partial_mu over multiples of p) ≈ -(2/p) * current partial sum
    # Actually this is more complex due to the p^2 zeroing.

    # Let's check: innovation(p) ≈ -2 * M_k(x) / p for small p?
    print(f"\n=== Innovation vs -2*M_prev/p (Testing Euler product structure) ===")
    for idx in range(min(15, len(primes))):
        p = primes[idx]
        predicted = -2 * partial_sums[idx] / p
        actual = innovations[idx]
        print(f"  p={p:>3d}: predicted = {predicted:>10.2f}, actual = {actual:>10.0f}, "
              f"ratio = {actual/predicted if abs(predicted) > 0.01 else float('nan'):>8.4f}")

    return partial_sums, innovations, primes

def second_moment_analysis(x):
    """
    Compute E[S(x)^2] for the random multiplicative function model.

    For random f with f(p) i.i.d. ±1:
    E[S(x)^2] = #{(n,m) <= x : n*m is a perfect square}
              = Sum_{d squarefree, d<=x} (#{k : dk^2 <= x})^2
              = Sum_{d squarefree, d<=x} floor(sqrt(x/d))^2
    """
    print(f"\n{'='*60}")
    print(f"SECOND MOMENT ANALYSIS for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)

    # Count squarefree numbers
    is_squarefree = (mu[1:x+1] != 0)
    squarefree_d = np.where(is_squarefree)[0] + 1  # +1 because of 0-indexing

    total = 0
    for d in squarefree_d:
        k_max = int(np.sqrt(x / d))
        total += k_max * k_max

    print(f"  E[S({x})²] = {total}")
    print(f"  x = {x}")
    print(f"  E[S({x})²] / x = {total/x:.6f}")
    print(f"  E[S({x})²] / (x * ln(x)) = {total/(x * np.log(x)):.6f}")
    print(f"  6/π² = {6/np.pi**2:.6f}")
    print(f"  sqrt(E[S²]) / sqrt(x) = {np.sqrt(total/x):.6f}")

    return total

def autocorrelation_structure(x):
    """
    Analyze the autocorrelation structure of μ(n).

    Compute Cov(μ(n), μ(n+h)) for various lags h.
    Also compute the "GCD correlation": how Cov(μ(n), μ(m)) depends on gcd(n,m).
    """
    print(f"\n{'='*60}")
    print(f"AUTOCORRELATION STRUCTURE for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)
    mu_float = mu[1:x+1].astype(np.float64)

    mean_mu = np.mean(mu_float)
    var_mu = np.var(mu_float)
    print(f"  E[μ] = {mean_mu:.8f} (theory: 0)")
    print(f"  Var(μ) = {var_mu:.8f} (theory: 6/π² = {6/np.pi**2:.8f})")

    # Lag autocorrelation
    print(f"\n  Lag autocorrelation Corr(μ(n), μ(n+h)):")
    print(f"  {'Lag':>6s} | {'Autocorr':>12s} | {'p-value proxy':>14s}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*14}")

    for h in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 60, 100]:
        if h >= x:
            break
        cov = np.mean(mu_float[:x-h] * mu_float[h:]) - mean_mu**2
        corr = cov / var_mu
        # Under null of independence, autocorr ~ N(0, 1/x)
        z_score = corr * np.sqrt(x)
        print(f"  {h:>6d} | {corr:>12.8f} | z = {z_score:>8.2f}")

    # GCD-based correlation
    print(f"\n  GCD-based correlation analysis (sample):")
    print(f"  For prime p, compute avg of mu(n)*mu(m) over pairs where p|gcd(n,m)")

    primes = sieve_primes(min(x, 100))
    for p in primes[:10]:
        # Get μ values at multiples of p
        multiples = mu_float[p-1::p]  # μ(p), μ(2p), μ(3p), ...
        n_mult = len(multiples)
        if n_mult < 2:
            continue
        mean_mult = np.mean(multiples)

        # Cross-correlation among multiples of p
        sum_sq = np.sum(multiples)**2 - np.sum(multiples**2)
        n_pairs = n_mult * (n_mult - 1)
        avg_product = sum_sq / n_pairs if n_pairs > 0 else 0

        print(f"    p={p:>3d}: #{p}-multiples = {n_mult:>6d}, "
              f"mean μ at multiples = {mean_mult:>8.5f}, "
              f"avg μ(n)μ(m) for p|gcd = {avg_product:>10.7f}")

    return

def conditional_expectation_test(x):
    """
    Test the near-martingale property: E[μ(n) | μ(1),...,μ(n-1)].

    If μ were a martingale difference sequence, E[μ(n)|past] = 0.
    We test how well this holds by checking if past μ values predict future ones.

    Specifically: can we predict μ(n) from the values of μ at divisors of n?
    """
    print(f"\n{'='*60}")
    print(f"CONDITIONAL EXPECTATION TEST for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)

    # Test 1: Does μ(n) depend on μ(n-1)?
    # For each value v of μ(n-1), compute E[μ(n) | μ(n-1) = v]
    print(f"\n  Test 1: E[μ(n) | μ(n-1) = v]")
    for v in [-1, 0, 1]:
        indices = np.where(mu[1:x] == v)[0]  # positions where μ = v
        if len(indices) == 0:
            continue
        next_vals = mu[indices + 2]  # μ at next position (indices is 0-based in mu[1:x])
        cond_mean = np.mean(next_vals)
        print(f"    μ(n-1) = {v:>2d}: E[μ(n)] = {cond_mean:>10.6f} "
              f"(sample size: {len(indices):,})")

    # Test 2: Does μ(n) depend on μ at divisors of n?
    # For n with a specific set of divisor μ-values, check E[μ(n)]
    print(f"\n  Test 2: E[μ(n) | μ(n/p) for p | n] (Mobius inversion structure)")
    print(f"  For even n: E[μ(n)] = {np.mean(mu[2:x+1:2]):.6f}")
    print(f"  For odd n:  E[μ(n)] = {np.mean(mu[1:x+1:2]):.6f}")
    print(f"  For 3|n:    E[μ(n)] = {np.mean(mu[3:x+1:3]):.6f}")
    print(f"  For 3∤n:    E[μ(n)] = {np.mean(mu[1:x+1][np.arange(x) % 3 != 2]):.6f}")

    # Test 3: Mobius at multiples of various primes
    print(f"\n  Test 3: Mean of μ at multiples of p (should be 0 by Euler product)")
    primes = sieve_primes(min(x, 200))
    for p in primes[:15]:
        mult_mu = mu[p::p]
        mean_val = np.mean(mult_mu[:x//p])
        std_err = np.std(mult_mu[:x//p]) / np.sqrt(x//p)
        print(f"    p={p:>3d}: E[μ] at p-multiples = {mean_val:>10.6f} ± {std_err:.6f}")

    # Test 4: Product structure — E[μ(n) | n ≡ 0 mod p, n ≡ 0 mod q]
    print(f"\n  Test 4: E[μ(n) | p|n AND q|n] for distinct primes p, q")
    for p, q in [(2,3), (2,5), (3,5), (2,7), (3,7), (5,7), (2,11), (2,13)]:
        pq = p * q
        mult_mu = mu[pq::pq][:x//(pq)]
        mean_val = np.mean(mult_mu) if len(mult_mu) > 0 else float('nan')
        print(f"    p={p}, q={q}: E[μ | pq|n] = {mean_val:>10.6f} "
              f"(sample: {len(mult_mu):,})")

def main():
    print("=" * 70)
    print("MARTINGALE ANALYSIS OF THE MOBIUS FUNCTION")
    print("=" * 70)

    # Run prime filtration analysis for manageable sizes
    for x in [1000, 10000, 100000]:
        prime_filtration_analysis(x)

    # Second moment analysis
    for x in [1000, 10000, 100000]:
        second_moment_analysis(x)

    # Autocorrelation
    autocorrelation_structure(1000000)

    # Conditional expectation
    conditional_expectation_test(1000000)

if __name__ == "__main__":
    main()
