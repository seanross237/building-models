#!/usr/bin/env python3
"""
Rigorous variance decomposition of M(x) through the Euler product.

Key computation: the second moment E[S(x)^2] for random multiplicative functions,
and comparison with the actual M(x)^2.

This script investigates THE critical question: does the random multiplicative
function model accurately predict the variance of M(x)?

Key identity:
  E[S(x)^2] = Sum_{d squarefree, d<=x} floor(sqrt(x/d))^2

This grows like (6/pi^2) * x * ln(x), NOT like x.
So std(S(x)) ~ sqrt(x * ln(x)), not sqrt(x).

Wait -- this contradicts the heuristic! Let's compute carefully.

Actually: E[S(x)^2] = Sum_{n<=x} |mu(n)|  (for Rademacher)
No wait, that's E[|S(x)|^2] = Sum_{n<=x} E[f(n)^2] only if f(n) are uncorrelated.
But they're NOT uncorrelated for multiplicative f.

For Rademacher random multiplicative f:
E[f(n)f(m)] = 1 if n and m have the same squarefree part, 0 otherwise.
So E[S(x)^2] = Sum_{n,m<=x} E[f(n)f(m)] = Sum_{d sqfree} (#{k: dk^2 <= x})^2

Let's compute this and understand the growth rate.
"""

import numpy as np
import time

def compute_mobius(limit):
    """Compute mu(n) for n = 1, ..., limit."""
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

def second_moment_detailed(x):
    """
    Compute E[S(x)^2] = Sum_{d squarefree, d<=x} floor(sqrt(x/d))^2

    Break it down by the size of d to understand where the mass lives.
    """
    mu = compute_mobius(x)

    total = 0
    # Group by order of magnitude of d
    bins = {}

    for d in range(1, x + 1):
        if mu[d] == 0:
            continue  # d not squarefree
        k_max = int(np.sqrt(x / d))
        contrib = k_max * k_max
        total += contrib

        # Bin by log10(d)
        if d == 0:
            continue
        bin_key = int(np.log10(max(d, 1)))
        bins[bin_key] = bins.get(bin_key, 0) + contrib

    return total, bins

def euler_product_variance(x, num_primes=None):
    """
    Compute the predicted variance of M(x) from the Euler product decomposition.

    The Euler product for 1/zeta(s) = prod_p (1 - p^{-s}).

    For the variance of M(x), we use:
    Var(M(x)) = Sum_{n<=x} mu(n)^2 + 2*Sum_{n<m<=x} mu(n)*mu(m)
              = |{n<=x : n squarefree}| + 2*Sum_{n<m<=x} mu(n)*mu(m)

    The first term is ~ 6x/pi^2.
    The second term (cross-correlations) is M(x)^2 - Sum mu(n)^2.

    So this is circular! M(x)^2 = Var(M(x)) means we need to compute M(x) to get Var(M(x)).

    For the RANDOM model:
    E[S(x)^2] = Sum_{d sqfree} floor(sqrt(x/d))^2

    The key insight: this equals Sum_{n<=x} r(n) where r(n) = #{d sqfree, k : dk^2 = n}
    """
    # Just compute it directly
    mu = compute_mobius(x)

    # Sum of mu(n)^2 = number of squarefree integers up to x
    sum_mu_sq = np.sum(mu[1:x+1].astype(np.int64)**2)

    # M(x)
    M_x = np.sum(mu[1:x+1].astype(np.int64))

    # M(x)^2 decomposition
    print(f"\n  x = {x:,}")
    print(f"  M(x) = {M_x}")
    print(f"  M(x)^2 = {M_x**2}")
    print(f"  Sum mu(n)^2 (= #{'{'}sqfree{'}'}) = {sum_mu_sq}")
    print(f"  Cross-term = M(x)^2 - Sum mu^2 = {M_x**2 - sum_mu_sq}")
    print(f"  |Cross-term| / Sum mu^2 = {abs(M_x**2 - sum_mu_sq) / sum_mu_sq:.6f}")

    # For random model
    total, bins = second_moment_detailed(x)
    print(f"\n  E[S(x)^2] (random model) = {total}")
    print(f"  E[S(x)^2] / x = {total/x:.6f}")
    print(f"  E[S(x)^2] / (x * ln x) = {total/(x * np.log(x)):.6f}")
    print(f"  sqrt(E[S^2]) = {np.sqrt(total):.2f}")
    print(f"  sqrt(E[S^2]) / sqrt(x) = {np.sqrt(total/x):.6f}")

    # Contribution by d-size
    print(f"\n  Contribution to E[S^2] by size of d:")
    for k in sorted(bins.keys()):
        print(f"    d ~ 10^{k}: contribution = {bins[k]:>12,} ({100*bins[k]/total:.1f}%)")

    return M_x, sum_mu_sq, total

def innovation_variance_by_prime(x):
    """
    Compute the variance contribution of each prime to M(x).

    In the prime-by-prime martingale decomposition:
    M(x) = x + Sum_p D_p

    where D_p = change in partial Mertens when incorporating prime p.

    The key question: does Sum_p D_p^2 scale like x, x*log(x), or something else?
    And how does it compare to (M(x) - x)^2?
    """
    print(f"\n{'='*60}")
    print(f"INNOVATION VARIANCE BY PRIME for x = {x:,}")
    print(f"{'='*60}")

    mu = compute_mobius(x)
    M_x = int(np.sum(mu[1:x+1].astype(np.int64)))

    # Sieve for primes
    is_prime = np.ones(x + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(x**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    primes = np.where(is_prime)[0]

    # Build partial Mobius step by step
    partial_mu = np.ones(x + 1, dtype=np.float64)
    partial_mu[0] = 0.0

    innovation_sq_sum = 0
    innovation_abs_sum = 0
    cum_var_by_prime_size = {}  # prime size -> cumulative D_p^2

    prev_sum = float(x)

    for p in primes:
        p2 = p * p

        if p2 <= x:
            partial_mu[p2::p2] = 0.0

        for n in range(p, x + 1, p):
            if n % p2 != 0:
                partial_mu[n] *= -1

        current_sum = np.sum(partial_mu[1:x+1])
        D_p = current_sum - prev_sum

        innovation_sq_sum += D_p**2
        innovation_abs_sum += abs(D_p)

        # Bin by prime size
        if p > 0:
            bin_key = int(np.log10(max(p, 1)))
            cum_var_by_prime_size[bin_key] = cum_var_by_prime_size.get(bin_key, 0) + D_p**2

        prev_sum = current_sum

    print(f"\n  M(x) = {M_x}")
    print(f"  (M(x) - x)^2 = {(M_x - x)**2}")
    print(f"  Sum D_p^2 = {innovation_sq_sum:.0f}")
    print(f"  Sum |D_p| = {innovation_abs_sum:.0f}")
    print(f"  Sum D_p^2 / x = {innovation_sq_sum/x:.4f}")
    print(f"  Sum D_p^2 / (x * ln x) = {innovation_sq_sum/(x * np.log(x)):.4f}")

    # If Sum D_p^2 ~ C * x, then the martingale has variance ~x,
    # giving M(x) = O(sqrt(x)) on average.
    # If Sum D_p^2 ~ C * x * ln x, the martingale has larger variance.

    print(f"\n  Variance contribution by prime size:")
    total_var = max(innovation_sq_sum, 1)
    for k in sorted(cum_var_by_prime_size.keys()):
        print(f"    p ~ 10^{k}: Sum D_p^2 = {cum_var_by_prime_size[k]:>15,.0f} "
              f"({100*cum_var_by_prime_size[k]/total_var:.1f}%)")

    # Theoretical prediction: D_p^2 should be approximately (x/p)^2 * (something small)
    # Actually D_p approximately = -2 * S_{k-1} / p for small primes
    # and D_p = +/- 2 * (# of relevant squarefree multiples of p <= x) for larger primes

    # Compare to prediction from Euler product
    # The "naive" prediction: Var(D_p) ~ x * (1/p^2) * (6/pi^2)
    # (Each of x/p multiples of p contributes ~1/p to the variance)
    predicted_var_sum = x * sum(1.0/p**2 for p in primes)
    print(f"\n  Predicted Sum 1/p^2 * x = {predicted_var_sum:.2f}")
    print(f"  Sum 1/p^2 (over primes <= x) = {sum(1.0/p**2 for p in primes):.6f}")
    print(f"  Sum 1/p^2 (all primes) ~ P(2) - 1 = {0.4522474200:.6f}")
    print(f"  Ratio actual/predicted = {innovation_sq_sum/predicted_var_sum:.4f}")

    return innovation_sq_sum

def growth_rate_analysis():
    """
    Analyze how E[S(x)^2] grows with x.

    Theory predicts E[S(x)^2] ~ (6/pi^2) * x * ln(x) for random multiplicative functions.

    But wait -- let me re-derive this.

    E[S(x)^2] = Sum_{d sqfree, d<=x} floor(sqrt(x/d))^2

    Approximate: ~ Sum_{d sqfree, d<=x} x/d = x * Sum_{d sqfree, d<=x} 1/d

    Now Sum_{d sqfree, d<=x} 1/d = prod_{p<=x} (1 + 1/p) * correction

    No wait. The generating function for squarefree reciprocals:
    Sum_{d sqfree} 1/d^s = prod_p (1 + 1/p^s) = zeta(s)/zeta(2s)

    At s = 1: this diverges like zeta(1)/zeta(2) ~ ln(x) * (6/pi^2).
    Hmm, zeta(1) diverges. More precisely:

    Sum_{d sqfree, d<=x} 1/d ~ (6/pi^2) * (ln x + gamma + 2*sum_p ln(1-1/p^2) + ...)

    Actually the coefficient is different. Let me compute:

    Sum_{d sqfree, d<=x} 1/d = prod_{p<=x} (1 + 1/p) approximately
                                = exp(sum_p 1/p + O(1/p^2))
                                ~ exp(ln ln x + M + O(1/ln x))
                                = C * ln(x)

    where C = e^M * prod_p (1+1/p)*e^{-1/p} (Mertens' constant).

    Hmm this is getting complicated. Let me just compute numerically.
    """
    print(f"\n{'='*60}")
    print(f"GROWTH RATE ANALYSIS")
    print(f"{'='*60}")

    results = []
    for exp in range(2, 7):
        x = 10**exp
        mu = compute_mobius(x)

        # E[S(x)^2] for random model
        total = 0
        for d in range(1, x + 1):
            if mu[d] == 0:
                continue
            k_max = int(np.sqrt(x / d))
            total += k_max * k_max

        # M(x) for actual Mobius
        M_x = int(np.sum(mu[1:x+1].astype(np.int64)))

        results.append((x, total, M_x))
        print(f"  x = {x:>10,}: E[S^2] = {total:>15,}, E[S^2]/x = {total/x:>8.4f}, "
              f"E[S^2]/(x*ln x) = {total/(x*np.log(x)):>8.6f}, "
              f"M(x)^2/x = {M_x**2/x:>8.4f}")

    # Check growth rate
    print(f"\n  Growth rate check (ratio of consecutive E[S^2]/x):")
    for i in range(1, len(results)):
        x1, t1, _ = results[i-1]
        x2, t2, _ = results[i]
        ratio = (t2/x2) / (t1/x1)
        print(f"    {x1:>10,} -> {x2:>10,}: ratio = {ratio:.4f} "
              f"(expected if ~ ln(x): {np.log(x2)/np.log(x1):.4f})")

    # Key insight: E[S(x)^2] / (x * ln x) approaches a constant ~ 6/pi^2
    # This means std(S(x)) ~ sqrt(6/pi^2 * x * ln x) ~ 0.78 * sqrt(x * ln x)
    # This is BIGGER than sqrt(x) by a factor of sqrt(ln x)!
    #
    # But Harper showed E|S(x)| ~ sqrt(x) / (log log x)^{1/4}, which is LESS than sqrt(x).
    # How is this consistent?
    #
    # Answer: the SECOND moment and FIRST moment of |S(x)| have very different behaviors.
    # E[S(x)^2] ~ x * ln(x), but E|S(x)| ~ sqrt(x) / (log log x)^{1/4}.
    # This means the distribution is very heavy-tailed: rare large values dominate E[S^2].
    # S(x) is typically ~ sqrt(x) / (log log x)^{1/4}, but occasionally ~ sqrt(x * ln x).

    print(f"\n  KEY INSIGHT:")
    print(f"  E[S(x)^2] grows like x * ln(x), not x.")
    print(f"  But Harper showed E|S(x)| ~ sqrt(x) / (log log x)^(1/4)")
    print(f"  This means the distribution is heavy-tailed:")
    print(f"    - Typical |S(x)| ~ sqrt(x) / (log log x)^(1/4)")
    print(f"    - But rare large values ~ sqrt(x * ln x) dominate E[S^2]")
    print(f"  For the deterministic mu, we need: |M(x)| = O(x^(1/2+eps))")
    print(f"  The random model predicts this should hold with overwhelming probability")
    print(f"  (since even sqrt(x * ln x) = O(x^(1/2+eps)) for any eps > 0)")

def main():
    print("=" * 70)
    print("VARIANCE DECOMPOSITION OF M(x)")
    print("=" * 70)

    # Detailed variance analysis at specific points
    for x in [1000, 10000, 100000]:
        print(f"\n{'='*60}")
        print(f"DETAILED ANALYSIS at x = {x:,}")
        print(f"{'='*60}")
        euler_product_variance(x)

    # Innovation variance
    for x in [1000, 10000]:
        innovation_variance_by_prime(x)

    # Growth rate
    growth_rate_analysis()

if __name__ == "__main__":
    main()
