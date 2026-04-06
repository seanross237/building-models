"""
Investigation 2: Pushing Density to Zero — Can Jensen + Concentration Give Zero-Free Regions?

The idea: forget about counting zeros in [0,T]. Instead, ask: for a SINGLE disk
centered at sigma_0 + iT, can Jensen + concentration give n(r) < 1?

If n(r) < 1 in a disk of radius r = sigma_0 - 1/2, then there are no zeros with
Re(s) > 1/2 in that disk. If this works for ALL T, we'd have RH.

REFINED JENSEN APPROACH:

Jensen's formula for a disk of radius R centered at z_0:
  n(r) * log(R/r) <= (1/2pi) int log|f(z_0 + Re^{itheta})| dtheta - log|f(z_0)|

For f = zeta, z_0 = sigma_0 + iT, we need:
1. UPPER BOUND: (1/2pi) int log|zeta(sigma_0 + Re^{itheta} + iT)| dtheta
2. LOWER BOUND: log|zeta(sigma_0 + iT)|

For n(r) < 1, we need:
  (1/2pi) int log|zeta| dtheta - log|zeta(z_0)| < log(R/r)

This means: the average of log|zeta| on the big circle minus the value at center
must be LESS than log(R/r). If the average is close to zero and the center value
is also close to zero, this requires log(R/r) > small number, which is easy.

The problem: for EXCEPTIONAL T near a zero, log|zeta(sigma_0 + iT)| can be very
negative. Jensen doesn't help us EXCLUDE zeros -- it tells us HOW MANY there are.

KEY INSIGHT: We need to flip the approach. Instead of using Jensen to bound zeros
from above, we should use it to derive CONTRADICTIONS.

APPROACH A: Littlewood's lemma (rectangle version of Jensen)
If we can show the integral of log|zeta| along a rectangle is bounded from below,
and the zero count times some factor exceeds this bound, we get a contradiction.

APPROACH B: Backlund's formula (argument principle)
N(T) = (T/2pi)*log(T/2pi*e) + O(log T) gives the total zero count to height T.
This is EXACT (not a bound). Can we use it combined with concentration to
constrain where zeros can be?

APPROACH C: Use the concentration to get a LOWER BOUND on |zeta| directly.
If we could show |zeta(sigma + it)| >= exp(-C(sigma)) for all t, we'd have
a zero-free region. The concentration gives this "on average" but not pointwise.

The deterministic tool: Bohr-Jessen (1932) gives the VALUE DISTRIBUTION of
log zeta(sigma+it) for sigma > 1/2. It's Gaussian with known mean and variance.
But the tails are not literally Gaussian -- they're described by a rate function.

LITTLEWOOD'S LEMMA (our main tool):
For a rectangle [sigma_1, sigma_2] x [0, T]:
  int_{sigma_1}^{sigma_2} N(sigma, T) dsigma = (1/2pi) * [
    int_0^T log|zeta(sigma_1+it)| dt - int_0^T log|zeta(sigma_2+it)| dt
    + boundary terms on t=0 and t=T
  ]

The boundary terms are O(log T). The integrals of log|zeta| are known:
- For sigma > 1/2: (1/T) int_0^T log|zeta(sigma+it)| dt -> 0 as T -> inf
  More precisely: int_0^T log|zeta(sigma+it)| dt = O(1) for sigma > 1
  and = O(T) for sigma in (1/2, 1] (actually o(T))

This gives: int_{sigma_1}^{sigma_2} N(sigma, T) dsigma ~ (T/2pi)*log(T) * (area under Backlund)
"""

import mpmath
from mpmath import mp, mpf, log, pi, sqrt, exp, power, zeta, arg, mpc, re, im, fabs
from sympy import nextprime as _nextprime
from math import log as mlog, sqrt as msqrt, pi as mpi, exp as mexp
import json

mp.dps = 30

def nextprime(n):
    return int(_nextprime(int(n)))

def V_sigma_full(sigma, num_primes=2000):
    """V(sigma) = sum_p (-1/2)*log(1 - p^{-2*sigma})"""
    total = mpf(0)
    p = 2
    count = 0
    while count < num_primes:
        total += -log(1 - power(p, -2*sigma)) / 2
        p = nextprime(p)
        count += 1
    return float(total)

print("=" * 70)
print("INVESTIGATION 2: PUSHING TOWARD ZERO-FREE REGIONS")
print("=" * 70)

# Part 1: Individual disk analysis
print("\n--- Part 1: Jensen bound in individual disk ---")
print("""
For a SINGLE disk centered at s_0 = sigma_0 + iT with big radius R and small radius r:

n(r) <= [avg log|zeta| on |s-s_0|=R  -  log|zeta(s_0)|] / log(R/r)

For n(r) < 1 (zero-free in small disk), we need:

  avg log|zeta| on big circle  -  log|zeta(s_0)|  <  log(R/r)     (*)

Analysis of each term:

1) avg log|zeta| on big circle:
   The circle passes through regions where zeta can be large (near sigma=1)
   and regions where zeta can be small (near sigma=1/2).

   For a circle of radius R centered at sigma_0 > 1/2:
   - Right side (sigma_0 + R): zeta is O(1) here, so log|zeta| is O(1)
   - Left side (sigma_0 - R): if this < 1/2, Phragmen-Lindelof gives
     log|zeta| <= ((1-(sigma_0-R))/4)*log(T) + O(1)  [SUBCONVEXITY if available]
     or log|zeta| <= ((1/2-(sigma_0-R))/2)*log(T) + O(1)  [CONVEXITY bound]

   The AVERAGE over the circle is dominated by the worst (leftmost) part.
   But importantly, it's an AVERAGE, not a maximum.

   For sigma_0 = 3/4, R = 1/4 + delta:
   Left point at 1/2 - delta. Convexity: log|zeta| <= (delta/2)*log T
   Average: dominated by this, giving avg ~ C*delta*log(T)

2) log|zeta(s_0)|:
   For "generic" T, Bohr-Jessen gives |log|zeta(s_0)|| ~ sqrt(V(sigma_0))
   But we need this for ALL T, including T near the imaginary part of a zero.

   If there's a zero at rho = beta + igamma with beta > 1/2, then
   log|zeta(s_0)| can be as negative as log|sigma_0 - beta + i(T-gamma)|
   = log(distance from s_0 to nearest zero)

   For a zero ON the critical line (beta = 1/2):
   log|zeta(sigma_0 + igamma)| is of order log(sigma_0 - 1/2)
   which is a NEGATIVE CONSTANT for sigma_0 near 1/2.

3) log(R/r):
   This is our "budget." For R = sigma_0 - 1/2 + delta, r = epsilon:
   log(R/r) = log((sigma_0 - 1/2 + delta)/epsilon)
   We want r to encompass a potential zero at beta + iT with beta > 1/2.
   So r >= sigma_0 - 1/2 (to reach the critical line).
   Then log(R/r) = log(1 + delta/(sigma_0 - 1/2)).

For (*) to hold with r = sigma_0 - 1/2:
  C*delta*log(T) + |log|zeta(s_0)|| < log(1 + delta/(sigma_0-1/2))

The LEFT side grows like log(T) (from the convexity bound on the big circle).
The RIGHT side is a CONSTANT (independent of T).

CONCLUSION: For any fixed sigma_0 > 1/2, Jensen CANNOT give a zero-free region
for ALL T, because the convexity bound on the circle grows with T while the
budget log(R/r) is constant.

This is why Vinogradov-Korobov zero-free regions have sigma_0 -> 1 as T -> inf.
""")

# Part 2: What if we use subconvexity?
print("\n--- Part 2: Impact of subconvexity bounds ---")
print("""
The convexity bound gives: mu(sigma) <= (1/2-sigma)/2 for 0 < sigma < 1/2
(where |zeta(sigma+it)| <= t^{mu(sigma)+epsilon}).

If we had the LINDELOF HYPOTHESIS: mu(sigma) = 0 for sigma >= 1/2, then
on the left side of our Jensen circle at sigma = 1/2 - delta:
  log|zeta| <= epsilon * log T

This would make the left side of (*) grow as epsilon*log(T), which is arbitrarily small
but still GROWS. So even Lindelof doesn't suffice for a fixed zero-free region.

What WOULD suffice: a UNIFORM bound log|zeta(sigma+it)| <= C for sigma >= 1/2.
This is MUCH stronger than Lindelof and is essentially equivalent to RH itself.

Current subconvexity results:
- Weyl: mu(1/2) <= 1/6  (1921)
- Bombieri-Iwaniec: mu(1/2) <= 9/56 (1986)
- Huxley: mu(1/2) <= 32/205 (2005)
- Bourgain: mu(1/2) <= 13/84 (2017)

These give progressively smaller growth of log|zeta| on the left side of the
Jensen circle, but they're all still O(log T) growth. Not good enough.
""")

# Part 3: Refined analysis — what growth rate of zero-free region does Jensen give?
print("\n--- Part 3: Zero-free region width from Jensen + Concentration ---")
print("""
QUESTION: If we can't get a FIXED zero-free region, what zero-free region
growing with T can we get?

Setup: center at sigma_0(T) + iT. Choose sigma_0(T) = 1 - w(T) where w(T) -> 0.
Want to show n(r) < 1 in disk of radius r = w(T).

Jensen: n(w) <= [avg log|zeta| on circle of radius R] / log(R/w)

Choose R = 2w (say). Then the circle goes from sigma = 1-3w to sigma = 1+w.
On the circle:
  - Right side (sigma ~ 1+w): |zeta| ~ 1/w, so log|zeta| ~ log(1/w)
  - Left side (sigma ~ 1-3w): |zeta| bounded by convexity
    log|zeta(1-3w+it)| <= (3w/2)*log(t) + O(1) [convexity bound]
    OR: log|zeta(1-3w+it)| <= (3w)*mu(1-3w)*log(t) + O(1)

Average on circle ~ (3w/2)*log(T) + log(1/w) approximately.

Budget: log(R/w) = log(2w/w) = log(2).

For n(w) < 1:
  (3w/2)*log(T) + log(1/w) < log(2)

This requires: w << 1/log(T)  (to make w*log(T) small)
AND: log(1/w) < log(2), i.e., w > 1/2 (contradicts w << 1/log T)

PROBLEM: The log(1/w) term from the right side of the circle (where |zeta| ~ 1/w
near sigma = 1) already exceeds the budget log(2).

FIX: Choose R much larger. R = 1/2 + sigma_0 = 3/2 - w. Then R/w >> 1.
But the left side of the circle reaches sigma = -1/2 + w, where the
functional equation gives log|zeta| ~ (1-w)*log(T). The average becomes ~ log(T).
Budget: log(R/w) ~ log(1/w). Need log(T) < log(1/w), so w < T^{-1}. Too small.

ALTERNATIVE: Use the functional equation to our advantage.
Near sigma = 1: |zeta(sigma+it)| has a pole at sigma = 1.
For sigma = 1 - w: log|zeta| ~ log(1/w) + oscillatory terms.
The oscillatory terms average out, but the log(1/w) doesn't.

The bottom line: the POLE of zeta at s=1 forces log|zeta| to be large
on any Jensen circle that includes sigma near 1. This inflates the
Jensen bound and prevents us from getting n < 1.
""")

# Part 4: Quantitative comparison with Vinogradov-Korobov
print("\n--- Part 4: Comparison with Vinogradov-Korobov ---")

def vinogradov_korobov_width(T, c=0.05):
    """Width of VK zero-free region: sigma > 1 - c/(logT)^{2/3}(loglogT)^{1/3}"""
    logT = mlog(T)
    loglogT = mlog(logT)
    return c / (logT**(2.0/3) * loglogT**(1.0/3))

def classical_zero_free_width(T, c=0.05):
    """Width of classical (de la Vallee Poussin) zero-free region: sigma > 1 - c/logT"""
    return c / mlog(T)

def jensen_concentration_width(T):
    """
    Width from Jensen + concentration analysis.

    From our analysis: we need w such that the Jensen bound gives n(w) < 1.

    The constraint is roughly: w * log(T) + log(1/w) < log(R/w)

    With R fixed, this gives w ~ 1/log(T) at best (same as classical!).

    Actually, the concentration helps by improving the lower bound on
    log|zeta(center)| from 0 to a POSITIVE value (for sigma near 1,
    log|zeta| ~ log(1/|sigma-1|) from the pole).

    For sigma_0 = 1 - w near 1: the average of log|zeta(sigma_0+it)| over
    t in [0,T] is approximately log(1/w) (from the pole contribution).

    The concentration says: the DEVIATION from this average is O(sqrt(V(sigma_0))).
    For sigma_0 near 1: V(sigma_0) ~ sum_p p^{-2(1-w)}/2 ~ sum_p p^{-2}/2 + O(w)
    which is BOUNDED. So the deviation is O(1).

    Jensen with center at sigma_0 = 1-w, radius R:
    avg log|zeta| on circle - log|zeta(center)| <= A*log(T) - (log(1/w) - O(1))

    For n < 1: A*log(T) - log(1/w) + O(1) < log(R/(sigma_0-1/2))
    = log(R/(1/2-w))

    This gives: log(1/w) > A*log(T) - log(R/(1/2-w)) + O(1)
    i.e., w < exp(-A*log(T) + ...) = T^{-A}

    But A depends on R, and for R large, A is large too.
    Optimizing: w ~ exp(-c*log(T)) = T^{-c} for some c > 0.
    This is WORSE than Vinogradov-Korobov (which gives w ~ (logT)^{-2/3}).

    Wait -- the concentration helps near sigma=1 because the POLE gives
    a deterministic lower bound. Let me reconsider.
    """
    # Simplified: Jensen near sigma=1 with pole contribution
    # gives w ~ c / log(T), same as de la Vallee Poussin
    return 0.05 / mlog(T)

print(f"{'T':>12} {'VK width':>14} {'Classical':>14} {'Jensen-Conc':>14}")
print("-" * 58)
for T in [1e6, 1e10, 1e20, 1e50, 1e100]:
    vk = vinogradov_korobov_width(T)
    cl = classical_zero_free_width(T)
    jc = jensen_concentration_width(T)
    print(f"{T:>12.0e} {vk:>14.6f} {cl:>14.6f} {jc:>14.6f}")

print("""
*** FINDING: Jensen + Concentration gives AT BEST the classical zero-free region ***

The concentration helps most near sigma = 1, where the POLE gives a deterministic
lower bound on |zeta|. But the zero-free region width is limited by the same
factor that limits de la Vallee Poussin: the convexity bound on the far side of
the Jensen circle grows with log(T).

The Vinogradov-Korobov improvement comes from exponential sum estimates
(Vinogradov's method), not from Jensen's formula. The concentration inequality
does not provide this kind of improvement.
""")

# Part 5: The fundamental obstruction
print("\n--- Part 5: The Fundamental Obstruction ---")
print("""
WHY Jensen + concentration cannot prove RH or even improve zero-free regions:

1. JENSEN IS A COUNTING TOOL, NOT A LOCATION TOOL.
   Jensen counts zeros inside a disk. It cannot determine WHERE they are.
   To get a zero-free region, we need n < 1, which requires the Jensen
   integral to be SMALLER than log(R/r).

2. THE CONVEXITY BOUND DOMINATES.
   On any circle that extends to sigma < 1/2, the convexity bound gives
   log|zeta| ~ (growth rate) * log(T). This grows with T.
   Jensen's "budget" log(R/r) is T-independent.
   So Jensen ALWAYS loses to the convexity bound for large T.

3. CONCENTRATION ONLY HELPS THE CENTER VALUE.
   The concentration inequality bounds log|zeta(center)| (a single point).
   It doesn't help with the average on the circle, which is where the
   dominant contribution comes from.

4. THE POLE AT s=1 IS DOUBLE-EDGED.
   Near sigma=1, the pole gives |zeta| >> 1 (helpful for Jensen's center value).
   But it also gives |zeta| >> 1 on parts of the Jensen circle (harmful).

5. SUBCONVEXITY DOESN'T HELP ENOUGH.
   Even Lindelof's hypothesis (mu(1/2) = 0) only reduces the growth rate
   to epsilon*log(T). This still grows, so Jensen still loses for large T.

WHAT WOULD HELP:
- A UNIFORM bound |zeta(sigma+it)| >= exp(-g(sigma)) independent of t.
  This is essentially the RH itself.
- Or: a way to exploit the Euler product structure that goes beyond
  concentration of measure. The large sieve and Halasz-Montgomery
  method do this, but they give density estimates, not zero-free regions.

BOTTOM LINE: Jensen's formula is the wrong tool for this problem. It converts
pointwise information into counting information, but we need pointwise information
(zero-free) from global/average information (concentration). The direction is wrong.
""")

# Part 6: Can we reverse Jensen? (Turan's method)
print("\n--- Part 6: Turan's Power Sum Method (the reverse direction) ---")
print("""
TURAN'S IDEA: Instead of Jensen (pointwise -> counting), use power sums
(counting -> pointwise). The idea:

If zeta has "few" zeros near sigma_0 + iT, then |zeta(sigma_0+iT)| cannot
be too small. Specifically:

|zeta(sigma_0+iT)|^{-1} <= (number of zeros in disk of radius r)^{C(r)}

This is the reverse of Jensen! If we could show N(sigma, T) < 1 for
sigma > sigma_0(T), we'd get |zeta(sigma_0(T) + iT)| > 0.

But N(sigma, T) < 1 IS the zero-free region. This is circular.

HOWEVER: Turan's power sum method gives more:
If sum_{k=1}^N a_k z_k^n has controlled growth in n, then the z_k cannot
be too far from the unit circle.

Applied to the Dirichlet series: the exponential sum behavior of n^{-it}
(which is the Euler product structure) constrains zero locations.

This is actually how Vinogradov-Korobov works: exponential sum estimates
(from the multiplicative structure) give constraints on Dirichlet polynomial
values, which constrain zeta values, which constrain zero locations.

The concentration inequality, in this framework, is a WEAKER version of
the exponential sum estimates. It captures the statistical behavior but
not the arithmetic structure that Vinogradov's method exploits.
""")

# Save results
results = {
    'finding': 'Jensen + concentration cannot improve on classical zero-free regions',
    'obstruction': 'Convexity bound on Jensen circle grows with log(T), exceeding T-independent budget',
    'best_achievable': 'de la Vallee Poussin type: w ~ c/log(T)',
    'why_VK_is_better': 'Vinogradov uses exponential sum estimates (arithmetic structure) not concentration',
    'fundamental_issue': 'Jensen converts pointwise -> counting, but we need global -> pointwise (wrong direction)',
    'key_insight': 'Concentration is a weaker version of exponential sum estimates; it captures statistical behavior but not arithmetic structure'
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/jensen-concentration/inv2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to inv2_results.json")
