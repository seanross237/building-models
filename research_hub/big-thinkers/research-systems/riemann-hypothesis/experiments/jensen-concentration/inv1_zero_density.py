"""
Investigation 1: Zero-Density Estimates from Euler Product Concentration

The plan:
1. Use Jensen's formula to relate average of log|zeta| on circles/rectangles
   to zero counts inside.
2. The Euler product concentration bounds the average of log|zeta(sigma+it)|
   from below for sigma > 1/2.
3. Classical convexity bounds control log|zeta| from above.
4. Combining gives zero-density estimates N(sigma, T).
5. Compare to Ingham, Huxley, Guth-Maynard.

Key formulas:
- Jensen: n(r, f) <= (1/2pi) integral_0^{2pi} log|f(Re^{itheta})| dtheta - log|f(0)|
  (for f analytic in disk |z| <= R, zeros at a_1,...,a_n with |a_k| < R)

  More precisely: sum log(R/|a_k|) = (1/2pi) int log|f(Re^{itheta})| dtheta - log|f(0)|

- For zeta, we work in rectangles. The argument principle version:
  N(sigma, T, T+H) = (1/2pi) * change in arg(zeta) around rectangle

- The key input: for sigma > 1/2, the Bohr-Jessen theorem gives
  (1/T) meas{t in [0,T] : log|zeta(sigma+it)| < -M} ~ Phi(-M/sqrt(V(sigma)))
  where Phi is the standard Gaussian CDF and V(sigma) = sum_p p^{-2sigma}/2.
"""

import mpmath
from mpmath import mp, mpf, log, pi, sqrt, exp, gamma, zeta, fsum, power
from sympy import nextprime as _nextprime
from math import log as math_log
import json

mp.dps = 30  # 30 decimal places

def nextprime(n):
    return int(_nextprime(int(n)))

def V_sigma(sigma, num_primes=10000):
    """Compute V(sigma) = sum_p p^{-2*sigma}/2 using first num_primes primes."""
    total = mpf(0)
    p = 2
    count = 0
    while count < num_primes:
        total += power(p, -2*sigma) / 2
        p = nextprime(p)
        count += 1
    return total

def V_sigma_full(sigma, num_primes=10000):
    """Full variance including higher-order terms:
    V(sigma) = sum_p sum_{k>=1} p^{-2k*sigma}/(2k)
    = sum_p (-1/2)*log(1 - p^{-2*sigma})
    """
    total = mpf(0)
    p = 2
    count = 0
    while count < num_primes:
        total += -log(1 - power(p, -2*sigma)) / 2
        p = nextprime(p)
        count += 1
    return total

print("=" * 70)
print("INVESTIGATION 1: ZERO-DENSITY ESTIMATES FROM CONCENTRATION")
print("=" * 70)

# Part 1: Compute V(sigma) for various sigma
print("\n--- Part 1: Variance V(sigma) ---")
print(f"{'sigma':>8} {'V_leading':>14} {'V_full':>14} {'ratio':>8}")
print("-" * 50)

sigmas = [0.51, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
V_values = {}

for s in sigmas:
    v_lead = V_sigma(s, 5000)
    v_full = V_sigma_full(s, 5000)
    ratio = v_full / v_lead
    V_values[s] = float(v_full)
    print(f"{s:>8.2f} {float(v_lead):>14.6f} {float(v_full):>14.6f} {float(ratio):>8.4f}")

# Part 2: Jensen's formula approach to zero-density
print("\n\n--- Part 2: Jensen's Formula Zero-Density Bound ---")
print("""
DERIVATION:

Consider a disk of radius R centered at s_0 = sigma_0 + iT.
Jensen's formula:
  sum_{|rho - s_0| < R} log(R/|rho - s_0|) = (1/2pi) int_0^{2pi} log|zeta(s_0 + Re^{itheta})| dtheta - log|zeta(s_0)|

Let n(r) = number of zeros in disk of radius r. Then n(r) * log(R/r) <= Jensen sum.

So: n(r) <= [avg log|zeta| on circle of radius R - log|zeta(s_0)|] / log(R/r)

The KEY INPUTS:

UPPER BOUND on avg log|zeta| on large circle:
  For sigma > 1/2: log|zeta(sigma+it)| <= (1/2)*log(t/(2*pi)) + O(1)  [convexity bound]
  For sigma < 0: functional equation gives log|zeta(sigma+it)| ~ (1/2-sigma)*log(t/(2*pi))

  On a circle of radius R centered at sigma_0 + iT:
  max log|zeta| on circle <= max((1/2)*log(T/(2pi)), (1/2-sigma_0+R)*log(T/(2pi)))

  The dominant contribution comes from the leftmost point of the circle:
  sigma_min = sigma_0 - R. If sigma_0 - R < 1/2:
    max log|zeta| ~ (1/2 - sigma_0 + R)*log(T)  [Phragmen-Lindelof]

LOWER BOUND on log|zeta(s_0)| from concentration:
  By Bohr-Jessen, for "most" T, log|zeta(sigma_0+iT)| is within O(sqrt(V(sigma_0))) of its mean.
  Mean of log|zeta(sigma_0+it)| = -sum_p Re[log(1-p^{-sigma_0-it})]
  For sigma_0 > 1/2, mean ~ -sum_p p^{-sigma_0}*cos(t*log p) which averages to 0.

  Actually: E[log|zeta(sigma+it)|] = -sum_p log|1-p^{-sigma}| for the random model.
  But in the actual function, the AVERAGE over t is:
  (1/T) int_0^T log|zeta(sigma+it)| dt -> 0 as T -> infinity (for sigma > 1/2)
  [This follows from the mean value theorem for Dirichlet series]

COMBINING via Jensen:
  n(r) <= [(1/2-sigma_0+R)*log(T) - log|zeta(sigma_0+iT)|] / log(R/r)

  For "most" T (outside a set of measure O(T * exp(-M^2/(2V(sigma_0))))):
  |log|zeta(sigma_0+iT)|| <= M * sqrt(V(sigma_0))

  So: n(r) <= [(1/2-sigma_0+R)*log(T) + M*sqrt(V(sigma_0))] / log(R/r)

  Choosing M = sqrt(2V(sigma_0)*log T) to make the exceptional set O(T * T^{-1}) = O(1):
  n(r) <= [(1/2-sigma_0+R)*log T + sqrt(2V(sigma_0))*sqrt(V(sigma_0)*log T)] / log(R/r)
       = [(1/2-sigma_0+R)*log T + sqrt(2)*V(sigma_0)*sqrt(log T)] / log(R/r)
""")

# Part 3: Explicit zero-density computation
print("\n--- Part 3: Explicit Zero-Density Bound N(sigma, T) ---")
print("""
STANDARD APPROACH (following Ingham's method with our concentration input):

N(sigma, T) = number of zeros rho = beta + i*gamma with beta > sigma, 0 < gamma < T.

Method: Cover [0, T] with intervals of length H. In each interval, use Jensen centered
at s_0 = sigma_1 + i*T_j (where sigma_1 > sigma) with radius R = sigma_1 - 1/2 + delta.

The zeros with beta > sigma that lie in [T_j, T_j + H] are in the Jensen disk if:
  R > sigma_1 - sigma = sigma_1 - sigma

Choose sigma_1 = (sigma + 1)/2 (midpoint), R = sigma_1 - 1/2 + 1/(log T).

Jensen bound per interval:
  n_j <= [(R - (sigma_1 - 1/2))*log T + C*sqrt(V(sigma_1)*log T)] / log(R/(sigma_1-sigma))
       ~ [log(T)/log(T) + C*sqrt(V(sigma_1)*log T)] / log(R/(sigma_1-sigma))

For the full strip: N(sigma, T) = sum_j n_j, with T/H intervals.
""")

# Numerical comparison
print("\n--- Part 4: Numerical Comparison with Classical Bounds ---\n")

def ingham_bound(sigma, T):
    """N(sigma,T) <= T^{3(1-sigma)/(2-sigma)+epsilon}"""
    if sigma >= 1 or sigma <= 0.5:
        return float('inf')
    exponent = 3*(1-sigma)/(2-sigma)
    return float(power(T, exponent))

def huxley_bound(sigma, T):
    """N(sigma,T) <= T^{12(1-sigma)/5+epsilon}"""
    if sigma >= 1 or sigma <= 0.5:
        return float('inf')
    exponent = 12*(1-sigma)/5
    return float(power(T, exponent))

def guth_maynard_bound(sigma, T):
    """N(sigma,T) <= T^{30(1-sigma)/13+epsilon} (for sigma near 3/4)"""
    if sigma >= 1 or sigma <= 0.5:
        return float('inf')
    exponent = 30*(1-sigma)/13
    return float(power(T, exponent))

def concentration_jensen_bound(sigma, T, V_dict):
    """
    Our concentration-based bound via Jensen's formula.

    Setup: center Jensen disk at sigma_1 + iT where sigma_1 = (sigma + 1)/2.
    R = sigma_1 - 1/2 + delta (big enough to reach left of sigma).
    r = sigma_1 - sigma (small radius containing the zeros we want to count).

    Jensen: n(r) <= [max log|zeta| on big circle - log|zeta(center)|] / log(R/r)

    Upper bound on circle: (R - (sigma_1 - 1/2)) * log(T) ≈ delta * log(T)
    [Actually: the leftmost point has sigma_1 - R < 1/2, giving
     mu(sigma_1 - R) * log T where mu is the convexity bound exponent]

    Lower bound at center: -C * sqrt(V(sigma_1) * log T) with probability 1 - 1/T

    Combining: n(r) <= [delta*log(T) + C*sqrt(V(sigma_1)*log(T))] / log(R/r)

    Over T/1 intervals: N(sigma, T) <= T * [delta*log(T) + C*sqrt(V(sigma_1)*log(T))] / log(R/r)
    """
    sigma_1 = (sigma + 1) / 2  # center sigma
    delta = 0.1  # overshoot past 1/2
    R = sigma_1 - 0.5 + delta
    r = sigma_1 - sigma

    if r <= 0 or R <= r:
        return float('inf')

    # V at center
    v_s1 = V_dict.get(round(sigma_1, 2))
    if v_s1 is None:
        # Interpolate
        v_s1 = float(V_sigma_full(mpf(sigma_1), 2000))

    # Upper bound from convexity: on leftmost point of circle, sigma_min = sigma_1 - R = 0.5 - delta
    # Phragmen-Lindelof: mu(sigma) = (1/2 - sigma)/2 for sigma < 0, and mu(sigma) <= (1-sigma)/2 for 0 < sigma < 1
    # At sigma_min = 0.5 - delta: mu = (1-(0.5-delta))/2 = (0.5+delta)/2
    sigma_min = sigma_1 - R  # = 0.5 - delta
    mu_upper = (1 - sigma_min) / 2  # convexity bound exponent

    log_T = math_log(T)
    upper_avg = mu_upper * log_T  # average on circle dominated by maximum

    # Lower bound at center from concentration
    C_conc = 2.0  # constant
    lower_center = -C_conc * (v_s1 * log_T)**0.5

    # Jensen gives count in one disk
    ratio = R / r
    n_per_disk = (upper_avg - lower_center) / math_log(ratio) if ratio > 1 else float('inf')

    # Number of disks needed to cover [0, T] (height coverage ~2*R each)
    n_disks = T / (2 * R)

    return float(n_per_disk * n_disks)

T_values = [1e4, 1e6, 1e8, 1e10]
sigma_values = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]

print(f"{'sigma':>6} {'T':>10} {'Ingham':>12} {'Huxley':>12} {'Guth-May':>12} {'Conc-Jensen':>14}")
print("-" * 70)

results_table = []
for s in sigma_values:
    for T in T_values:
        ib = ingham_bound(s, T)
        hb = huxley_bound(s, T)
        gm = guth_maynard_bound(s, T)
        cj = concentration_jensen_bound(s, T, V_values)

        row = {
            'sigma': s, 'T': T,
            'ingham': ib, 'huxley': hb, 'guth_maynard': gm, 'concentration': cj
        }
        results_table.append(row)

        print(f"{s:>6.2f} {T:>10.0e} {float(ib):>12.1f} {float(hb):>12.1f} {float(gm):>12.1f} {float(cj):>14.1f}")
    print()

# Part 5: The exponents
print("\n--- Part 5: Exponent Comparison ---")
print("""
Classical zero-density exponents: N(sigma, T) <= T^{A(sigma) + epsilon}

Ingham:      A(sigma) = 3(1-sigma)/(2-sigma)
Huxley:      A(sigma) = 12(1-sigma)/5
Guth-Maynard: A(sigma) = 30(1-sigma)/13

Our concentration-Jensen: What exponent does it give?

From the computation above:
N(sigma, T) ~ T * [C1 * log(T) + C2 * sqrt(V(sigma_1) * log(T))] / log(R/r)

The dominant term is T * log(T) / log(R/r).

Since R and r depend on sigma but not on T, we get:
A_conc(sigma) = 1  (!!!)

This is WORSE than all classical bounds (which have A(sigma) < 1 for sigma > 1/2).

The reason: Jensen's formula with just concentration gives a bound proportional to T
(one unit interval per zero potential). Classical methods use mean-value theorems
for Dirichlet polynomials that exploit MULTIPLICATIVE structure more efficiently.
""")

print(f"{'sigma':>6} {'A_Ingham':>10} {'A_Huxley':>10} {'A_GM':>10} {'A_conc':>10}")
print("-" * 50)
for s in sigma_values:
    a_ing = 3*(1-s)/(2-s)
    a_hux = 12*(1-s)/5
    a_gm = 30*(1-s)/13
    a_conc = 1.0  # our bound
    print(f"{s:>6.2f} {a_ing:>10.4f} {a_hux:>10.4f} {a_gm:>10.4f} {a_conc:>10.4f}")

print("""
\n*** CRITICAL FINDING ***

The concentration-Jensen approach gives exponent A(sigma) = 1 uniformly,
which is MUCH WORSE than all classical bounds. The reason is clear:

1. Jensen's formula bounds zeros in a DISK. To cover [0,T], we need ~T disks.
2. Each disk gets O(log T) zeros from Jensen, giving N = O(T * log T).
3. Classical methods use the MEAN VALUE THEOREM for Dirichlet polynomials:
   int_0^T |sum a(n) n^{-it}|^2 dt ~ T * sum |a(n)|^2
   This gives cancellation that Jensen alone cannot achieve.

The concentration inequality gives GAUSSIAN tails for log|zeta|, but this only
affects the log T factor, not the T factor. The T factor comes from covering
the full height, not from the concentration.

IMPLICATION: Naive Jensen + concentration CANNOT recover classical zero-density
estimates. The missing ingredient is the mean-value theorem / large sieve, which
exploits the multiplicative structure at a deeper level than just concentration.

However, there is a SUBTLETY we should investigate further: the concentration
inequality might be useful for INDIVIDUAL DISKS (giving a zero-free result
for specific T), even if it doesn't help with density estimates.
""")

# Save results
with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/jensen-concentration/inv1_results.json', 'w') as f:
    json.dump({
        'V_values': V_values,
        'density_table': results_table,
        'finding': 'Concentration + Jensen gives exponent 1, worse than all classical bounds',
        'reason': 'Jensen requires T disks to cover height T, concentration only helps with log factor'
    }, f, indent=2, default=str)

print("\nResults saved to inv1_results.json")
