"""
Investigation 1: Quantify the tension between almost-periodicity and concentration.

Key questions:
1. For P_N(sigma+it), how dense are the almost-periods?
2. If zeta(sigma_0+it_0) = 0, how many near-zeros does almost-periodicity force?
3. How many near-zeros does concentration allow?
4. Do these conflict?
"""

import mpmath
import numpy as np
from collections import defaultdict

mpmath.mp.dps = 30

def primes_up_to(N):
    """Sieve of Eratosthenes."""
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]

def euler_product_truncated(sigma, t, N):
    """Compute P_N(sigma + it) = prod_{p <= N} (1 - p^{-sigma-it})^{-1}."""
    s = mpmath.mpc(sigma, t)
    result = mpmath.mpc(1, 0)
    for p in primes_up_to(N):
        result *= 1 / (1 - mpmath.power(p, -s))
    return result

def variance_V(sigma, N_primes=97):
    """
    Compute V(sigma) = sum_{p <= N} (1/2) * p^{-2*sigma}.
    Leading term of Var[log|1 - p^{-sigma-it}|].
    """
    V = 0.0
    for p in primes_up_to(N_primes):
        V += 0.5 * float(p) ** (-2 * sigma)
    return V

# ============================================================
# Part A: Almost-period density for truncated Euler products
# ============================================================

print("=" * 70)
print("INVESTIGATION 1: ALMOST-PERIODICITY vs CONCENTRATION")
print("=" * 70)

print("\n--- Part A: Almost-period structure ---\n")

# For P_N(sigma+it), the frequencies are {log(p) : p <= N}
# An epsilon-almost-period tau satisfies:
#   |P_N(sigma+i(t+tau)) - P_N(sigma+it)| < epsilon for ALL t
#
# By Kronecker's approximation, such tau exist iff we can find tau
# such that tau * log(p) is close to an integer multiple of 2*pi
# for each prime p <= N simultaneously.
#
# The density of epsilon-almost-periods is related to the simultaneous
# Diophantine approximation of {log(2)/2pi, log(3)/2pi, log(5)/2pi, ...}

# For a single frequency omega, epsilon-almost-periods of e^{i*omega*t}
# have density ~1/(epsilon period), i.e., gaps bounded by ~2*pi/(omega * epsilon).
# For k independent frequencies, the gap grows exponentially in k.

for N in [10, 30, 100]:
    ps = primes_up_to(N)
    k = len(ps)
    freqs = [np.log(p) for p in ps]

    # The key quantity: how does the Euler product P_N vary as a function of t?
    # |P_N(sigma+i(t+tau)) / P_N(sigma+it)| = prod_p |1 - p^{-sigma-i(t+tau)}|^{-1} / |1 - p^{-sigma-it}|^{-1}
    # = prod_p |1 - p^{-sigma-it}| / |1 - p^{-sigma-i(t+tau)}|

    # For the ratio to be close to 1, we need each factor close to 1,
    # which requires p^{-i*tau} close to 1 for each p, i.e.,
    # tau * log(p) close to 0 mod 2*pi.

    # Effective dimension of the torus: number of primes
    # Gap between consecutive almost-periods: roughly (2*pi/epsilon)^k / Volume
    # where Volume ~ (2*pi)^k (torus volume)

    # More precisely, for multiplicative epsilon-closeness in each factor:
    # we need |tau * log(p) mod 2*pi| < delta_p for each p
    # where delta_p depends on sigma and the target epsilon

    print(f"N = {N}: k = {k} primes, frequencies = log(p) for p in {ps[:5]}...")

    # For sigma = 0.7, compute how sensitive P_N is to a shift tau
    sigma = 0.7
    t0 = 100.0
    P0 = euler_product_truncated(sigma, t0, N)

    # Scan for approximate periods
    n_scan = 10000
    tau_vals = np.linspace(0.1, 1000.0, n_scan)
    ratios = []
    for tau in tau_vals:
        Ptau = euler_product_truncated(sigma, t0 + tau, N)
        ratio = abs(float(abs(Ptau)) / float(abs(P0)) - 1.0)
        ratios.append(ratio)
    ratios = np.array(ratios)

    # Count epsilon-close returns
    for eps in [0.1, 0.01]:
        count = np.sum(ratios < eps)
        print(f"  sigma={sigma}, eps={eps}: {count}/{n_scan} points in [0,1000] have |P_N(t+tau)/P_N(t) - 1| < eps")
        if count > 0:
            close_indices = np.where(ratios < eps)[0]
            gaps = np.diff(tau_vals[close_indices])
            if len(gaps) > 0:
                print(f"    Mean gap between returns: {np.mean(gaps):.2f}, Max gap: {np.max(gaps):.2f}")
    print()

# ============================================================
# Part B: Concentration bounds on near-zeros
# ============================================================

print("\n--- Part B: Concentration bounds on near-zeros ---\n")

for sigma in [0.6, 0.7, 0.8, 0.9]:
    V = variance_V(sigma, 997)  # primes up to 997

    print(f"sigma = {sigma}:")
    print(f"  V(sigma) = {V:.6f}")
    print(f"  For |zeta| < epsilon:")
    for eps_exp in [1, 2, 5, 10]:
        eps = 10**(-eps_exp)
        M = -np.log(eps)  # log|zeta| < -M means |zeta| < eps
        # Actually log|zeta| concentrates around its mean ~ 0 for large t
        # P(log|zeta| < -M) <= exp(-M^2 / 2V)
        log_prob = -M**2 / (2 * V)
        # Expected number in [0,T] with T = 10^6
        T = 1e6
        expected_count = T * np.exp(log_prob) if log_prob > -500 else 0
        print(f"    eps=10^{-eps_exp}: P(|zeta|<eps) <= exp({log_prob:.1f}), expected in [0,10^6]: {expected_count:.2e}")
    print()

# ============================================================
# Part C: The crucial tension calculation
# ============================================================

print("\n--- Part C: Tension between almost-periodicity and concentration ---\n")

# Suppose zeta(sigma_0 + it_0) = 0 for some sigma_0 > 1/2.
#
# Step 1: P_N(sigma_0 + it_0) must be close to 0 for large N.
# Specifically, P_N -> zeta, so |P_N(sigma_0+it_0)| -> 0.
#
# Step 2: P_N is almost-periodic. So for any delta > 0, the set
# {tau : |P_N(sigma_0+i(t_0+tau))| < delta}
# is relatively dense (gaps bounded by some L(N, delta)).
#
# BUT: P_N is NOT almost-periodic uniformly in N!
# As N -> infinity, the almost-period length L(N, epsilon) -> infinity.
# The truncated product P_N has pi(N) frequencies, so the almost-period
# structure becomes increasingly complicated.
#
# The real question: does L(N, epsilon) grow faster or slower than
# the spacing between near-zeros allowed by concentration?

print("Almost-period length L(N,eps) vs concentration spacing:")
print()

for sigma_0 in [0.6, 0.7, 0.8]:
    V = variance_V(sigma_0, 997)
    print(f"sigma_0 = {sigma_0}, V(sigma_0) = {V:.4f}:")

    for log_eps in [-1, -2, -5]:
        eps = 10**(log_eps)
        M = -np.log(eps)

        # Concentration: expected gap between epsilon-near-zeros of zeta
        # is ~ 1 / P(|zeta| < eps) ~ exp(M^2 / (2V))
        conc_gap = np.exp(M**2 / (2 * V))

        # Almost-periodicity of P_N: for N primes, the gap between
        # epsilon-almost-periods is roughly:
        # L(N, eps) ~ prod_{p<=N} (2*pi / arcsin(eps/C_p))
        # where C_p = |1/(1-p^{-sigma})|
        #
        # A rough estimate: for the RATIO |P_N(t+tau)/P_N(t)| to be within
        # epsilon of 1, we need EACH factor within ~eps/pi(N) of 1.
        # The gap for a single factor (1-p^{-s})^{-1} is ~2*pi/(log(p) * eps_per_factor).
        # The joint gap is roughly the product.

        # Let's be more careful. The almost-period for a product of k terms
        # in general grows as the product of individual almost-periods
        # (since the frequencies are linearly independent over Q by
        # the transcendence of log primes).

        # For P_N with N such that pi(N) primes:
        # Individual factor: period-like structure has gap ~ 2*pi/log(p)
        # For near-periodicity with tolerance delta in each factor:
        # gap ~ 2*pi / (log(p) * delta)
        # If we want overall tolerance epsilon, and there are k factors,
        # each factor needs tolerance ~ epsilon/k (by triangle inequality in log space)

        # For 10, 30, 100 primes:
        for N_val, k_val in [(30, 10), (100, 25), (1000, 168)]:
            ps = primes_up_to(N_val)
            k = len(ps)
            delta_per_factor = eps / k  # rough

            # Gap for simultaneous approximation: by Minkowski/pigeonhole,
            # there exist almost-periods in every interval of length
            # L ~ (2*pi)^k / (prod_{p<=N} delta_per_factor * log(p))
            # But we want the SMALLEST such period, not just existence.

            # A more practical estimate: by the equidistribution/Kronecker
            # theorem, simultaneous epsilon-approximation occurs with density
            # ~ (2*delta_per_factor / (2*pi))^k in the sequence (tau*log(p)/2pi mod 1)
            # So the gap is ~ (pi/delta_per_factor)^k

            # Work in log space to avoid overflow
            log_period_gap = k * np.log(np.pi / delta_per_factor)
            log_conc_gap = M**2 / (2 * V)

            print(f"  eps=10^{log_eps}, N={N_val} (k={k}):")
            print(f"    log(Concentration gap): {log_conc_gap:.1f}")
            print(f"    log(Almost-period gap): {log_period_gap:.1f}")
            if log_period_gap < log_conc_gap:
                print(f"    --> Almost-periods MORE FREQUENT than concentration allows: POTENTIAL TENSION")
            else:
                print(f"    --> Almost-periods LESS FREQUENT: no tension (AP gap exceeds concentration gap)")
        print()
    print()

# ============================================================
# Part D: The refined argument -- does the tension survive?
# ============================================================

print("\n--- Part D: Does the tension survive careful analysis? ---\n")

# The issue: as N grows, P_N gets closer to zeta, but the
# almost-period gap L(N, epsilon) also grows dramatically.
# The question is whether, at the SPECIFIC N where P_N first
# approximates zeta well enough to "see" the zero, the
# almost-periodicity still forces enough near-zeros to
# contradict concentration.

# For P_N to approximate zeta within epsilon at height t:
# Error = |zeta(sigma+it) - P_N(sigma+it)|
# For sigma > 1/2, the error is bounded by sum_{p > N} p^{-sigma} * (secondary terms)
# Roughly: |error| ~ N^{1-2*sigma} / (2*sigma - 1) (from prime number theorem)

print("Required N for P_N to approximate zeta within epsilon at sigma:")
print()

for sigma in [0.6, 0.7, 0.8]:
    for log_eps in [-1, -2, -5]:
        eps = 10**(log_eps)
        # N^{1-2*sigma} / (2*sigma - 1) ~ eps
        # N ~ (eps * (2*sigma - 1))^{1/(1-2*sigma)}
        exponent = 1.0 / (2*sigma - 1)
        N_required = (eps * (2*sigma - 1)) ** (-exponent)
        k_required = N_required / np.log(N_required) if N_required > 2 else 1  # pi(N) ~ N/log(N)

        # At this N, the almost-period gap
        delta_per_factor = eps / max(k_required, 1)
        if delta_per_factor > 0 and delta_per_factor < np.pi:
            ap_gap_log = k_required * np.log(np.pi / delta_per_factor)
        else:
            ap_gap_log = float('inf')

        # Concentration gap
        V = variance_V(sigma, 997)
        M = -np.log(eps)
        conc_gap_log = M**2 / (2 * V)

        print(f"  sigma={sigma}, eps=10^{log_eps}:")
        print(f"    N_required ~ {N_required:.1e}, k ~ {k_required:.1e}")
        print(f"    AP gap (log): {ap_gap_log:.1f}")
        print(f"    Concentration gap (log): {conc_gap_log:.1f}")
        if ap_gap_log < conc_gap_log:
            print(f"    ==> TENSION: AP forces near-zeros more often than concentration allows")
        else:
            print(f"    ==> NO TENSION: AP gap dominates")
    print()

# ============================================================
# Part E: The key insight -- what happens as epsilon -> 0?
# ============================================================

print("\n--- Part E: Asymptotic analysis as epsilon -> 0 ---\n")

# For a genuine zero: epsilon -> 0, meaning M = -log(epsilon) -> infinity
#
# Concentration gap: exp(M^2 / (2V)) -- grows as exp(M^2)
#
# For the almost-periodicity gap at the required N:
# N_required ~ epsilon^{-1/(2sigma-1)} = exp(M/(2sigma-1))
# k ~ N/log(N) ~ exp(M/(2sigma-1)) / (M/(2sigma-1))
# delta_per_factor ~ epsilon/k = exp(-M) / k
#
# AP gap ~ (pi/delta_per_factor)^k ~ (pi * k * exp(M))^k
# log(AP gap) ~ k * (M + log(k) + log(pi))
# ~ exp(M/(2sigma-1)) * M / (M/(2sigma-1))  (dropping log terms)
# = (2sigma-1) * exp(M/(2sigma-1))
#
# So log(AP gap) ~ exp(M/(2sigma-1)) -- grows EXPONENTIALLY in M
# log(Concentration gap) ~ M^2 -- grows QUADRATICALLY in M
#
# For large M: exp(M/(2sigma-1)) >> M^2
#
# Therefore: the AP gap ALWAYS DOMINATES for large enough M.
# The almost-periodicity argument CANNOT produce a contradiction
# because as we demand closer and closer to zero, the truncated
# Euler product needs more primes, and the almost-period gap
# grows exponentially -- far faster than the concentration bound.

for sigma in [0.6, 0.7, 0.8]:
    print(f"sigma = {sigma}:")
    print(f"  Concentration gap growth: exp(M^2 / {2*variance_V(sigma,997):.3f})")
    print(f"  AP gap growth: exp(exp(M / {2*sigma-1:.1f}))")
    print(f"  For large M, AP gap >> concentration gap: NO CONTRADICTION")
    print(f"  The almost-periodicity becomes too weak as the approximation demand increases.")
    print()

print("\n" + "=" * 70)
print("CONCLUSION OF INVESTIGATION 1")
print("=" * 70)
print("""
The naive almost-periodicity vs concentration tension does NOT yield
a contradiction that excludes off-line zeros. The reason:

1. For P_N to approximate zeta within epsilon, we need N ~ epsilon^{-1/(2sigma-1)}.
2. At that N, the almost-period gap is ~ exp(exponential in M) where M = -log(epsilon).
3. The concentration gap is ~ exp(M^2).
4. Exponential growth beats quadratic: AP gap >> concentration gap for large M.

In other words: as we demand the truncated product to be closer to zero
(to approach an actual zero of zeta), the number of primes needed grows,
and the almost-periodicity becomes so weak (periods so long) that it
cannot force enough near-zeros to contradict concentration.

This is PRECISELY analogous to the fact that an individual Gaussian
random variable has P(X < -M) = exp(-M^2/2), but a sum of N independent
variables has the SAME tail behavior (by CLT, with variance growing as N).
The "almost-periodicity" is like the lattice structure of independent
variables -- it creates correlations, but the tail probability adapts.

KEY INSIGHT: The tension IS real for FIXED N (finite truncation), but
dissolves as N -> infinity because the almost-periodicity degrades
faster than the concentration sharpens.

HOWEVER: There may be a more subtle argument using the RATE at which
almost-periodicity degrades. If the Euler product convergence rate
and the almost-period degradation rate are precisely calibrated
(as they must be, by the functional equation), there might be a
window where the tension persists. This requires Investigation 2.
""")
