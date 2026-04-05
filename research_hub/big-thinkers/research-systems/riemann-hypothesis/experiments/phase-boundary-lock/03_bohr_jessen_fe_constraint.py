"""
Experiment 3: Bohr-Jessen + Functional Equation Constraints

Key investigation: what constraints does the functional equation impose on 
WHERE zeros can nucleate, given the Bohr-Jessen fluctuation structure?

The Bohr-Jessen theorem: for fixed sigma > 1/2, as T -> infinity,
  (1/T) * meas{t in [0,T] : log|zeta(sigma+it)| < u} -> Phi_sigma(u)
where Phi_sigma is a smooth distribution.

The functional equation: |zeta(sigma+it)|^2 = |chi(sigma+it)|^2 * |zeta(1-sigma+it)|^2

This COUPLES the distribution at sigma with the distribution at 1-sigma.

We investigate:
1. The variance coupling: Var(log|zeta(sigma)|) vs Var(log|zeta(1-sigma)|)
2. The zero-nucleation constraint: can a zero at sigma_0 > 1/2 be consistent
   with the Bohr-Jessen distribution at sigma_0?
3. The "reflection gap" argument
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, log, sqrt, exp, fabs, zetazero, arg, loggamma

mp.dps = 25

def chi_func(s):
    """chi(s) = pi^{s-1/2} Gamma((1-s)/2) / Gamma(s/2)"""
    return pi**(s - mpf('0.5')) * gamma((1-s)/2) / gamma(s/2)

def log_chi_magnitude(sigma, t):
    """log|chi(sigma + it)|"""
    s = mpc(sigma, t)
    c = chi_func(s)
    return float(log(fabs(c)))

# ============================================================
# Part 1: The Variance Coupling
# ============================================================
print("=" * 70)
print("PART 1: Bohr-Jessen Variance at sigma vs 1-sigma")
print("=" * 70)

# The Bohr-Jessen variance of log|zeta(sigma+it)| is approximately
# V(sigma) = (1/2) sum_p p^{-2*sigma}
# For sigma < 1/2, this diverges.

# But the functional equation says:
# log|zeta(sigma+it)| = log|chi(sigma+it)| + log|zeta(1-sigma+it)|
# So Var(log|zeta(sigma)|) = Var(log|chi(sigma)|) + Var(log|zeta(1-sigma)|) + 2*Cov

# The key: log|chi(sigma+it)| is essentially deterministic (grows like (1/2-sigma)*log(t/2pi))
# and slowly varying. So the randomness of log|zeta(sigma+it)| is almost entirely
# from log|zeta(1-sigma+it)|.

print("\nBohr-Jessen variance V(sigma) = (1/2) sum_{p<=N} p^{-2*sigma}:")
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
# Extend with a sieve
def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

primes = sieve(100000)

def bj_variance(sigma, N_primes=None):
    ps = primes[:N_primes] if N_primes else primes
    return 0.5 * sum(p**(-2*sigma) for p in ps)

print(f"\n{'sigma':>8} | {'1-sigma':>8} | {'V(sigma)':>12} | {'V(1-sigma)':>12} | {'Ratio':>10}")
print("-" * 60)
for sigma in [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 0.95]:
    vs = bj_variance(sigma)
    vs_ref = bj_variance(1 - sigma)
    ratio = vs_ref / vs if vs > 0 else float('inf')
    print(f"{sigma:>8.2f} | {1-sigma:>8.2f} | {vs:>12.4f} | {vs_ref:>12.4f} | {ratio:>10.2f}")

# ============================================================
# Part 2: The log|chi| bridge
# ============================================================
print("\n" + "=" * 70)
print("PART 2: The log|chi| bridge between sigma and 1-sigma")
print("=" * 70)

# The functional equation: zeta(s) = chi(s) * zeta(1-s)
# So: log|zeta(sigma+it)| = log|chi(sigma+it)| + log|zeta(1-sigma+it)|
#
# If zeta(sigma_0 + it_0) = 0, then:
# 0 = -infinity = log|chi(sigma_0+it_0)| + log|zeta(1-sigma_0+it_0)|
# This means: log|zeta(1-sigma_0+it_0)| = -log|chi(sigma_0+it_0)|
#
# For sigma_0 > 1/2: log|chi(sigma_0+it_0)| < 0 (for large t_0)
# So: log|zeta(1-sigma_0+it_0)| = -log|chi(sigma_0+it_0)| > 0

print("\nlog|chi(sigma + it)| for various sigma and t:")
print(f"\n{'t':>8} | {'sigma=0.50':>12} | {'sigma=0.55':>12} | {'sigma=0.60':>12} | {'sigma=0.70':>12} | {'sigma=0.80':>12}")
print("-" * 72)
for t in [14.13, 25.01, 50.0, 100.0, 500.0, 1000.0]:
    vals = []
    for sigma in [0.50, 0.55, 0.60, 0.70, 0.80]:
        v = log_chi_magnitude(sigma, t)
        vals.append(v)
    print(f"{t:>8.1f} | {'  |  '.join(f'{v:>8.3f}' for v in vals)}")

# The Stirling approximation for |chi|:
# log|chi(sigma+it)| ≈ (1/2 - sigma) * log(t/(2*pi)) - pi*t/4 + ... 
# Wait, that's wrong. Let me compute more carefully.
# chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s)
# |chi(sigma+it)| ~ (t/(2*pi))^{1/2-sigma} for large t (Stirling)

print("\n\nStirling check: log|chi(sigma+it)| ≈ (1/2-sigma)*log(t/(2*pi))")
print(f"\n{'t':>8} | {'sigma':>6} | {'Exact':>10} | {'Stirling':>10} | {'Error':>8}")
print("-" * 52)
for t in [100.0, 500.0, 1000.0]:
    for sigma in [0.55, 0.60, 0.70, 0.80]:
        exact = log_chi_magnitude(sigma, t)
        stirling = (0.5 - sigma) * np.log(t / (2*np.pi))
        err = abs(exact - stirling)
        print(f"{t:>8.1f} | {sigma:>6.2f} | {exact:>10.4f} | {stirling:>10.4f} | {err:>8.4f}")

# ============================================================  
# Part 3: The zero-at-sigma_0 contradiction argument
# ============================================================
print("\n" + "=" * 70)
print("PART 3: The Zero-at-sigma_0 Contradiction Argument")
print("=" * 70)

# Suppose zeta(sigma_0 + it_0) = 0 with sigma_0 > 1/2.
# Then by the functional equation: zeta(1-sigma_0 + it_0) = zeta(sigma_0+it_0)/chi(sigma_0+it_0) = 0/chi = 0
# Wait -- that's wrong! The functional equation says:
# zeta(s) = chi(s) * zeta(1-s)
# If zeta(s) = 0 and chi(s) != 0, then zeta(1-s) = zeta(s)/chi(s) = 0/chi(s) = 0.
# Actually, chi(s) is never zero (it has poles but no zeros).
# So if zeta(sigma_0 + it_0) = 0 with sigma_0 > 1/2, then zeta(1-sigma_0 + it_0) must...
# 
# Wait. Let me be more careful. zeta(s) = chi(s) * zeta(1-s).
# If zeta(s) = 0, then chi(s) * zeta(1-s) = 0. Since chi(s) != 0 for s in the critical strip
# (chi has no zeros), we need zeta(1-s) = 0.
#
# So zeros ALWAYS come in pairs: if rho = sigma_0 + it_0 is a zero, so is 1 - conjugate(rho).
# Combined with the conjugate symmetry (zeta(s*) = zeta(s)*), if sigma_0 + it_0 is a zero,
# so are sigma_0 - it_0, (1-sigma_0) + it_0, (1-sigma_0) - it_0.
#
# This is ALWAYS true. The functional equation doesn't prevent off-line zeros; it just
# says they come in pairs.

print("\nFACT: The functional equation alone does NOT prevent off-line zeros.")
print("If rho = sigma_0 + it_0 is a zero with sigma_0 != 1/2, then")
print("(1-sigma_0) + it_0 is also a zero. Zeros come in reflected pairs.")
print("\nThe question is whether the COMBINATION of reflection + Bohr-Jessen prevents this.")

# ============================================================
# Part 4: The quantitative argument
# ============================================================
print("\n" + "=" * 70)
print("PART 4: Quantitative Constraints from Bohr-Jessen + Functional Equation")
print("=" * 70)

# For sigma > 1/2, the Bohr-Jessen distribution of log|zeta(sigma+it)| has:
# - Mean approximately sum_p p^{-sigma} (log p) / (p^sigma - 1)  -- actually this is E_beta
# - For the LOG, mean ≈ 0 (by symmetry of the distribution in the limit)
# - Variance V(sigma) = (1/2) sum_p p^{-2*sigma}
#
# The probability that |zeta(sigma+it)| < epsilon (i.e., near a zero) is:
# P(log|zeta| < log(epsilon)) ≈ Phi_sigma(log(epsilon))
#
# For the Bohr-Jessen distribution, the probability density at u = -infinity (log|zeta| -> -inf)
# is controlled by the entire tail of the distribution.
#
# KEY QUANTITY: How rare are near-zeros for the Euler product at sigma?

# Let's measure this empirically
print("\nEmpirical measurement: frequency of |zeta(sigma+it)| < threshold")
print("Sampling t in [10000, 20000] at 10000 points")

T_low, T_high = 10000, 20000
N_samples = 10000
t_vals = np.linspace(T_low, T_high, N_samples)

for sigma in [0.55, 0.60, 0.70, 0.80, 1.0]:
    vals = []
    for t in t_vals:
        s = mpc(sigma, t)
        z = zeta(s)
        vals.append(float(fabs(z)))
    vals = np.array(vals)
    
    print(f"\nsigma = {sigma:.2f}:")
    print(f"  mean |zeta| = {np.mean(vals):.4f}")
    print(f"  std  |zeta| = {np.std(vals):.4f}")
    print(f"  min  |zeta| = {np.min(vals):.6f}")
    for thresh in [0.1, 0.01, 0.001]:
        count = np.sum(vals < thresh)
        pct = 100.0 * count / N_samples
        print(f"  P(|zeta| < {thresh}) ≈ {pct:.3f}%")

print("\n" + "=" * 70)
print("PART 5: The reflection + fluctuation argument (the heart of the matter)")
print("=" * 70)

# Here's the key argument:
#
# CLAIM: A zero at sigma_0 > 1/2 requires "coordinated improbable behavior"
# at BOTH sigma_0 and 1-sigma_0 simultaneously.
#
# At sigma = sigma_0 > 1/2:
#   - The Euler product CONVERGES, so log|zeta(sigma_0+it)| has Gaussian-like
#     fluctuations with variance V(sigma_0) < infinity
#   - A zero means log|zeta| = -infinity, an event of probability ZERO 
#     in the Bohr-Jessen distribution for a GENERIC Euler product
#   - For the ACTUAL zeta function, zeros are possible because zeta is not
#     a generic Euler product -- it has the functional equation
#
# At sigma = 1-sigma_0 < 1/2:
#   - The functional equation FORCES a companion zero
#   - But at 1-sigma_0 < 1/2, the variance V(1-sigma_0) is LARGER (or infinite)
#   - So zeros are "easier" to produce there
#
# The question: does the variance asymmetry V(sigma_0) < V(1-sigma_0) create
# a contradiction?

print("\nThe variance asymmetry:")
print("For a zero pair at sigma_0 and 1-sigma_0:")
print(f"\n{'sigma_0':>8} | {'V(sigma_0)':>12} | {'V(1-sigma_0)':>14} | {'Asymmetry':>10}")
print("-" * 52)
for sigma0 in [0.51, 0.55, 0.60, 0.70, 0.80, 0.90]:
    v1 = bj_variance(sigma0)
    v2 = bj_variance(1 - sigma0)
    asym = v2 / v1
    print(f"{sigma0:>8.2f} | {v1:>12.4f} | {v2:>14.4f} | {asym:>10.2f}")

print("\nCRITICAL OBSERVATION:")
print("The variance asymmetry shows that at sigma_0 = 0.51, the fluctuations")
print("at 1-sigma_0 = 0.49 are only ~1.15x larger. The asymmetry grows with |sigma_0 - 0.5|.")
print("\nThis means: for sigma_0 NEAR 1/2 (like 0.5001), the functional equation")
print("imposes almost NO extra constraint. The zero at 0.4999 has essentially the")
print("same fluctuation environment as the zero at 0.5001.")
print("\nTHE GAP: The Bohr-Jessen + functional equation argument CANNOT rule out")
print("zeros very close to the critical line. It only constrains zeros FAR from 1/2.")

