#!/usr/bin/env python3
"""
THE CIRCULARITY ANALYSIS

This script demonstrates precisely where the martingale approach becomes circular.

Core question: can we bound |M(x)| = O(x^{1/2+eps}) using the martingale structure
WITHOUT already assuming something equivalent to RH?

The answer is: NO, and here's exactly why.

The martingale decomposition M(x) = x + Sum_p D_p is valid.
The Burkholder-Davis-Gundy inequality gives:
  E[|Sum D_p|^2] <= C * Sum E[D_p^2]

If we could show Sum D_p^2 = O(x^{1+eps}), we'd get |M(x)| = O(x^{1/2+eps}).
But Sum D_p^2 is NOT O(x) -- it's dominated by the contribution of p=2,
which gives D_2 ~ -3x/4 (since processing p=2 changes the sum from x to x/4).

The issue: D_p is NOT small for small primes. D_2 alone is O(x), so the
"martingale variance" is O(x^2), not O(x). The martingale bound gives
|M(x)| = O(x), which is trivial.

However, there's a subtlety: the CONDITIONAL variance (conditioning on
previous primes) might be much smaller than the unconditional variance.
This is what we investigate here.

The key theoretical question: can we show that the "effective variance"
(properly defined) is O(x)?
"""

import numpy as np

def compute_mobius(limit):
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

def demonstrate_circularity(x):
    """
    Show that the martingale approach is circular for the deterministic M(x).

    The point: for RANDOM multiplicative f, the martingale bound works because
    we can bound E[D_p^2] using PROBABILISTIC tools (independence of f(p)).

    For the DETERMINISTIC mu, D_p is a fixed number, not random.
    We can't take expectations over it.

    The "martingale" is with respect to the prime filtration G_k.
    But for a fixed x, the "random variable" is N uniform on {1,...,x},
    and M(x) = x * E[mu(N)] is deterministic.

    The decomposition M(x) = Sum_p D_p is just an algebraic identity.
    It's the INCLUSION-EXCLUSION principle applied prime by prime.
    """
    print(f"\n{'='*60}")
    print(f"CIRCULARITY ANALYSIS for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)
    M_x = int(np.sum(mu[1:x+1].astype(np.int64)))

    # The prime-by-prime decomposition is really just:
    # M(x) = Sum_{n=1}^x mu(n)
    #       = Sum_{n=1}^x prod_{p|n} (-1) * 1_{n squarefree}
    #
    # This is the Euler product evaluated at x:
    # M(x) = x * prod_p (1 - 1/p) * correction_terms
    #
    # The "correction_terms" are what make this hard.

    # Euler product prediction: M(x) ~ x * prod_{p<=x} (1 - 1/p) = x/ln(x) * e^{-gamma}
    # But wait, prod_p (1-1/p) = 0 (it diverges to zero).
    # The right formula: Sum_{n<=x} mu(n)/n = product terms + error

    # Actually: M(x) is related to 1/zeta(1) which is 0 (pole at s=1).
    # More precisely: M(x)/x -> 0 (prime number theorem equivalent).

    # The key identity we're using:
    # Processing prime p changes the partial sum by:
    # D_p = -2 * (sum of current partial_mu at multiples of p not div by p^2)
    #        + (zeroing out multiples of p^2)

    # For p = 2:
    # Before processing 2: partial sum = x (all 1's)
    # After processing 2: even numbers flip sign (-1), p^2=4 multiples become 0
    # D_2 = -floor(x/2) - floor(x/4) approximately = -3x/4

    # So |D_2| ~ 3x/4. This single innovation is O(x).
    # The BDG inequality gives |M - x| <= C * sqrt(Sum D_p^2) >= C * |D_2| ~ 3x/4
    # This is USELESS.

    # Can we do better by using conditional variance?
    # In the random model, Var(D_p | G_{p-1}) is what we'd bound.
    # But for the deterministic mu, D_p is a fixed number.
    # There's no randomness to take variance over.

    # THE FUNDAMENTAL ISSUE:
    # The martingale is over the "which prime is next" dimension.
    # But we process ALL primes -- there's no randomness in the filtration.
    # The only way to introduce randomness is:
    #   (a) Replace mu with random f (Harper's approach)
    #   (b) Average over x (Matomaki-Radziwill approach)
    #   (c) Use the uniform-N framework (Denjoy's heuristic)

    # Option (c) makes M(x) = x * E[mu(N)] deterministic.
    # Options (a) and (b) are what the experts actually use.

    # Let's quantify the "distance from random" for actual mu.

    # Sieve primes
    is_prime = np.ones(x + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(x**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    primes = np.where(is_prime)[0]

    # Compute innovations
    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0

    innovations = []
    for p in primes:
        p2 = p * p
        if p2 <= x:
            partial_mu[p2::p2] = 0.0
        for n in range(p, x + 1, p):
            if n % p2 != 0:
                partial_mu[n] *= -1
        current_sum = np.sum(partial_mu[1:x+1])
        D_p = current_sum - (x if len(innovations) == 0 else x + sum(innovations))
        innovations.append(current_sum - (x + sum(innovations[:-1]) if innovations else x))

    # Recompute more carefully
    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0
    prev_sum = float(x)
    innovations = []

    for p in primes:
        p2 = p * p
        if p2 <= x:
            partial_mu[p2::p2] = 0.0
        for n in range(p, x + 1, p):
            if n % p2 != 0:
                partial_mu[n] *= -1
        current_sum = np.sum(partial_mu[1:x+1])
        innovations.append(current_sum - prev_sum)
        prev_sum = current_sum

    innovations = np.array(innovations)

    print(f"\n  ALGEBRAIC DECOMPOSITION (not probabilistic!):")
    print(f"  M(x) = x + Sum D_p = {x} + ({np.sum(innovations):.0f}) = {x + np.sum(innovations):.0f}")
    print(f"  Actual M(x) = {M_x}")

    # The crucial comparison: how does the ACTUAL M(x) compare to what
    # would be "typical" if the innovations were random?

    # For random f, D_p would have mean 0 and variance ~ (prev_sum/p)^2
    # The actual D_p has a specific sign.

    # If we compute the "energy" Sum D_p^2 and compare to M(x)^2:
    energy = np.sum(innovations**2)
    print(f"\n  Innovation energy Sum D_p^2 = {energy:.0f}")
    print(f"  M(x)^2 = {M_x**2}")
    print(f"  If innovations were i.i.d. mean-0, E[M^2] = Sum D_p^2 = {energy:.0f}")
    print(f"  Actual M(x)^2 / Sum D_p^2 = {M_x**2 / energy:.8f}")

    # This ratio is MUCH less than 1, showing massive cancellation.
    # The innovations are NOT independent -- they cancel.
    # This cancellation IS the content of RH.

    print(f"\n  THE CIRCULARITY:")
    print(f"  - The algebraic decomposition M = x + Sum D_p is exact.")
    print(f"  - |D_2| = {abs(innovations[0]):.0f} = O(x).")
    print(f"  - Naive bound: |M| <= |x| + Sum |D_p| = {x + np.sum(np.abs(innovations)):.0f}.")
    print(f"  - This gives |M| = O(x), which is trivial.")
    print(f"  - To get |M| = O(sqrt(x)), we need Sum D_p to cancel x.")
    print(f"  - Proving this cancellation IS the Riemann Hypothesis.")
    print(f"  - The martingale framework doesn't help because:")
    print(f"    (a) D_p are deterministic, not random")
    print(f"    (b) The 'randomness' must come from elsewhere")
    print(f"    (c) Harper's trick: replace mu with random f, but then")
    print(f"        results only apply to RANDOM f, not actual mu")

    # But there IS a non-circular path (maybe):
    print(f"\n  POSSIBLE NON-CIRCULAR APPROACHES:")
    print(f"  1. Show mu is 'generic' among multiplicative functions")
    print(f"     (i.e., mu doesn't have special structure that causes")
    print(f"     larger-than-random cancellation failure)")
    print(f"  2. Use Matomaki-Radziwill to show cancellation in most")
    print(f"     short intervals, then bootstrap to full interval")
    print(f"  3. Show the innovations D_p satisfy a 'pseudorandomness'")
    print(f"     condition that implies cancellation (Sarnak's program)")

    return innovations

def alternative_filtration(x):
    """
    Try a different filtration: instead of processing primes in order,
    process them from LARGEST to SMALLEST.

    This changes the innovation structure but not the final result.
    The question: is one ordering better for bounding |M(x)|?
    """
    print(f"\n{'='*60}")
    print(f"ALTERNATIVE FILTRATION (large primes first) for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)
    M_x = int(np.sum(mu[1:x+1].astype(np.int64)))

    is_prime = np.ones(x + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(x**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    primes = np.where(is_prime)[0][::-1]  # REVERSE order

    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0
    prev_sum = float(x)
    innovations_rev = []

    for p in primes:
        p2 = p * p
        if p2 <= x:
            partial_mu[p2::p2] = 0.0
        for n in range(p, x + 1, p):
            if n % p2 != 0:
                partial_mu[n] *= -1
        current_sum = np.sum(partial_mu[1:x+1])
        innovations_rev.append(current_sum - prev_sum)
        prev_sum = current_sum

    innovations_rev = np.array(innovations_rev)

    print(f"  Processing primes from {primes[0]} down to {primes[-1]}")
    print(f"  Final sum: {prev_sum:.0f}, true M(x) = {M_x}")

    # First few innovations (from largest primes)
    print(f"\n  First 10 innovations (from largest primes):")
    for i in range(min(10, len(innovations_rev))):
        p = primes[i]
        D = innovations_rev[i]
        print(f"    p={p:>5d}: D_p = {D:>8.0f}")

    # Last few innovations (from smallest primes)
    print(f"\n  Last 5 innovations (from smallest primes):")
    for i in range(max(0, len(innovations_rev)-5), len(innovations_rev)):
        p = primes[i]
        D = innovations_rev[i]
        print(f"    p={p:>5d}: D_p = {D:>10.0f}")

    energy_rev = np.sum(innovations_rev**2)
    print(f"\n  Energy Sum D_p^2 (reverse) = {energy_rev:.0f}")
    print(f"  Note: energy depends on ordering! (not a martingale property)")

    # For large primes p > sqrt(x), each prime affects at most 1 number (p itself)
    # and at most floor(x/p) numbers. The innovation is at most 2*floor(x/p).
    # Sum over large primes: Sum_{p > sqrt(x)} (2x/p)^2 ~ 4x^2 * Sum_{p>sqrt(x)} 1/p^2
    # This is ~ 4x^2 / sqrt(x) ~ 4x^{3/2}, which is better than the forward ordering.

    large_prime_energy = np.sum(innovations_rev[:len(primes[primes > int(np.sqrt(x))])]**2)
    small_prime_energy = energy_rev - large_prime_energy
    n_large = len(primes[primes > int(np.sqrt(x))])
    n_small = len(primes) - n_large

    print(f"\n  Large primes (p > sqrt(x)={int(np.sqrt(x))}): {n_large} primes, "
          f"energy = {large_prime_energy:.0f}")
    print(f"  Small primes (p <= sqrt(x)): {n_small} primes, "
          f"energy = {small_prime_energy:.0f}")

def main():
    for x in [1000, 10000, 100000]:
        demonstrate_circularity(x)

    for x in [1000, 10000]:
        alternative_filtration(x)

if __name__ == "__main__":
    main()
