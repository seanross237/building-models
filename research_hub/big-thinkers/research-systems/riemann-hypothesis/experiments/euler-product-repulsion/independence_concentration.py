"""
Prime Independence and Concentration Inequalities.

The Euler product makes log|zeta(sigma+it)| = sum_p Re(-log(1 - p^{-sigma-it}))
a sum of INDEPENDENT contributions. Independence is incredibly powerful:

1. Central limit theorems (Selberg's CLT)
2. Large deviation bounds (Cramer, Chernoff)
3. Concentration inequalities (Hoeffding, Bernstein)
4. PF properties via Schoenberg's theorem on convolutions

The DH function BREAKS independence because it's a linear combination.
We quantify the concentration inequality gap.
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 25

###############################################################################
# 1. Setup: the random model
###############################################################################

print("=== THE RANDOM MODEL ===\n")
print("""
Model: For each prime p, define X_p(t) = Re(-log(1 - p^{-1/2-it})).
As t ranges over [T, 2T], X_p behaves approximately as a random variable.

Key properties:
  E[X_p] ≈ 0  (for large p)
  Var(X_p) ≈ 1/(2p)  (leading term)
  The {X_p} are asymptotically independent (for distinct primes)

Then: log|zeta(1/2+it)| ≈ sum_p X_p(t)
  Var(sum) = sum_p Var(X_p) ≈ sum_p 1/(2p) ≈ (1/2) log log T  (Mertens' theorem)
  This is Selberg's central limit theorem.
""")

###############################################################################
# 2. Concentration for sums of independent vs dependent variables
###############################################################################

print("=== CONCENTRATION INEQUALITIES ===\n")

print("For INDEPENDENT random variables X_1, ..., X_n with |X_k| <= B_k:")
print("  Hoeffding: P(|sum X_k| > t) <= 2 exp(-2t^2 / sum B_k^2)")
print("  Bernstein: P(|sum X_k| > t) <= 2 exp(-t^2/(2(V + Bt/3)))")
print("  where V = sum Var(X_k) and B = max B_k")
print()
print("For DEPENDENT variables, only much weaker bounds hold (or none at all).")
print()

# Compute the Hoeffding/Bernstein parameters for zeta
primes = []
p = 2
while p < 10000:
    if all(p % d != 0 for d in range(2, int(p**0.5)+1)):
        primes.append(p)
    p += 1 if p == 2 else 2

def compute_prime_bounds(sigma, prime_list):
    """
    For X_p = Re(-log(1 - p^{-sigma-it})):
    |X_p| <= -log(1 - p^{-sigma}) ≈ p^{-sigma} for large p
    Var(X_p) ≈ 1/(2 * p^{2*sigma})
    """
    B_k_sq_sum = 0
    V_sum = 0
    B_max = 0

    for p in prime_list:
        B = -float(mpmath.log(1 - mpmath.power(p, -sigma)))
        var = 1.0 / (2 * p**(2*sigma))
        B_k_sq_sum += B**2
        V_sum += var
        B_max = max(B_max, B)

    return B_k_sq_sum, V_sum, B_max

print(f"{'sigma':>6s}  {'V=sum Var':>10s}  {'B_max':>8s}  {'sum B^2':>10s}  {'Hoeff bound for t=V':>20s}")
print("-" * 65)

for sigma in [0.50, 0.55, 0.60, 0.75, 1.00]:
    B2_sum, V, B_max = compute_prime_bounds(sigma, primes[:500])  # primes up to ~3500
    t_val = V  # asking: probability that sum exceeds its own variance
    hoeffding = 2 * np.exp(-2 * t_val**2 / B2_sum) if B2_sum > 0 else 0
    print(f"{sigma:6.2f}  {V:10.4f}  {B_max:8.4f}  {B2_sum:10.4f}  {hoeffding:20.6e}")

###############################################################################
# 3. The critical calculation: probability of "near-zero" events
###############################################################################

print("\n\n=== PROBABILITY OF NEAR-ZERO EVENTS ===\n")
print("""
For zeta to have a zero at sigma + it, we need |zeta(sigma+it)| = 0,
equivalently log|zeta(sigma+it)| = -infinity.

In the random model, log|zeta| ≈ sum X_p, and the probability that
a sum of independent random variables reaches -M satisfies:

  P(sum X_p < -M) <= exp(-M^2 / (2*V))  [sub-Gaussian bound]

where V = sum Var(X_p).

At sigma > 1/2: V is FINITE (converges). So the probability of
log|zeta| reaching -M decays exponentially in M^2.

At sigma = 1/2: V ~ (1/2) log log T -> infinity. The bound becomes
  P(sum X_p < -M) <= exp(-M^2 / (log log T))
which is compatible with zeros existing (you need M -> infinity but
the variance also grows).
""")

# Detailed calculation
print("Probability bounds for log|zeta(sigma+it)| < -M (for M = 10, 50, 100):\n")

print(f"{'sigma':>6s}  {'V(T=10^6)':>10s}  {'P(< -10)':>12s}  {'P(< -50)':>12s}  {'P(< -100)':>12s}")
print("-" * 60)

# Use all primes up to T for height T ~ 10^6
# sum 1/(2p) for p < T approximates (1/2) log log T
for sigma in [0.50, 0.51, 0.52, 0.55, 0.60, 0.75, 1.00]:
    if sigma == 0.50:
        # At sigma = 1/2, use Selberg's estimate
        V = 0.5 * np.log(np.log(1e6))  # ≈ 0.5 * 2.63 ≈ 1.31
    else:
        # At sigma > 1/2, sum converges
        V = sum(1.0 / (2 * p**(2*sigma)) for p in primes)

    p10 = np.exp(-10**2 / (2*V)) if V > 0 else 0
    p50 = np.exp(-50**2 / (2*V)) if V > 0 else 0
    p100 = np.exp(-100**2 / (2*V)) if V > 0 else 0

    print(f"{sigma:6.2f}  {V:10.4f}  {p10:12.4e}  {p50:12.4e}  {p100:12.4e}")

print("""
The probabilities at sigma > 1/2 are ABSURDLY small.
For sigma = 0.75: P(log|zeta| < -10) < 10^{-24}
This means in a range [0, T], the expected number of "near-zeros" (|zeta| < e^{-10}) is:
  T * P(< -10) ~ T * 10^{-24}
which is effectively zero for any computationally accessible T.

For a genuine zero (M -> infinity), the probability is zero.
This is the concentration inequality argument: INDEPENDENCE of the prime
contributions forces log|zeta| to concentrate around its mean at sigma > 1/2.
""")

###############################################################################
# 4. Why the DH function doesn't concentrate
###############################################################################

print("=== WHY DH DOESN'T CONCENTRATE ===\n")
print("""
The DH function L_DH(s) = c1*L(s,chi1) + c2*L(s,chi1_bar).

Even at sigma > 1/2, the two terms can CANCEL:
  |L_DH(s)| = |c1*L(s,chi1) + c2*L(s,chi1_bar)|

This is NOT a sum of independent terms -- it's a sum of TWO terms
(each of which is itself well-concentrated) but the two can have
OPPOSITE phases. The cancellation produces zeros.

The key difference:
- log|zeta(s)| = sum_p f_p(s)  [independent, concentrated]
- L_DH(s) = c1*prod_p g_p(s) + c2*prod_p h_p(s)  [two correlated products]

For L_DH, the two products can be of similar magnitude but opposite sign,
giving L_DH = 0. This happens when:
  c1*L(s,chi1) = -c2*L(s,chi1_bar)
  i.e., |L(s,chi1)/L(s,chi1_bar)| = |c2/c1| = 1  (since |c1| = |c2|)
  and arg(c1*L(s,chi1)) = arg(c2*L(s,chi1_bar)) + pi
""")

# Find actual near-zeros of DH off the critical line
print("Searching for near-zeros of DH off the critical line...\n")

def dh_fast(sigma, t, N=3000):
    """Fast DH computation"""
    s = complex(sigma, t)
    L1 = sum(complex(chi1_table[n%5]) * n**(-s) for n in range(1, N+1) if chi1_table[n%5] != 0)
    L2 = sum(complex(chi1_table[n%5]).conjugate() * n**(-s) for n in range(1, N+1) if chi1_table[n%5] != 0)
    c1_val = complex((1 - 1j*0.284079) / 2)
    c2_val = complex((1 + 1j*0.284079) / 2)
    return c1_val * L1 + c2_val * L2

chi1_table = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}

print(f"{'sigma':>6s}  {'t':>6s}  {'|DH|':>10s}  {'|L(chi1)|':>10s}  {'|L(chi1b)|':>10s}  {'phase diff':>10s}")
print("-" * 60)

near_zeros = []
for sigma in np.arange(0.55, 0.95, 0.05):
    for t in np.arange(1, 100, 0.5):
        s = complex(sigma, t)
        L1 = sum(complex(chi1_table[n%5]) * n**(-s) for n in range(1, 2000) if chi1_table[n%5] != 0)
        L2 = sum(complex(chi1_table[n%5]).conjugate() * n**(-s) for n in range(1, 2000) if chi1_table[n%5] != 0)
        c1_val = complex((1 - 1j*0.284079) / 2)
        c2_val = complex((1 + 1j*0.284079) / 2)
        dh = c1_val * L1 + c2_val * L2

        if abs(dh) < 0.3:
            term1 = c1_val * L1
            term2 = c2_val * L2
            phase_diff = np.angle(term1) - np.angle(term2)
            # Normalize to [-pi, pi]
            phase_diff = (phase_diff + np.pi) % (2*np.pi) - np.pi
            near_zeros.append((sigma, t, abs(dh)))
            print(f"{sigma:6.2f}  {t:6.1f}  {abs(dh):10.6f}  {abs(L1):10.6f}  {abs(L2):10.6f}  {phase_diff:10.4f}")

print(f"\nFound {len(near_zeros)} near-zeros off the critical line")

###############################################################################
# 5. Selberg class summary
###############################################################################

print("\n\n=== SELBERG CLASS AND GRH ===\n")
print("""
The Selberg class S consists of Dirichlet series F(s) = sum a_n n^{-s} with:
  (S1) Analytic continuation (Ramanujan bound: a_n = O(n^epsilon))
  (S2) Functional equation of standard type
  (S3) Euler product: F(s) = prod_p F_p(s) where F_p(s) = exp(sum_{k>=1} b_{p^k} p^{-ks})
       with b_{p^k} = O(p^{k*theta}) for some theta < 1/2
  (S4) Ramanujan conjecture on the coefficients

Grand Lindelof Hypothesis and GRH are expected for all F in S.

KEY RESULTS IN THE SELBERG CLASS:

1. Conrey-Ghosh (1993): Formalized the connection between the Selberg class and
   analytic properties. The degree d(F) = 2*sum N_j (where N_j are the gamma
   factors) is the key invariant.

2. Kaczorowski-Perelli (1999, 2002, 2011): Structure theorems for S.
   - d(F) = 0 => F = 1
   - d(F) = 1 => F = L(s, chi) for some primitive character chi (proved!)
   - d(F) in (0,1) => no such F exists
   - The classification for d(F) = 2 (which includes zeta^2 and L-functions
     of holomorphic newforms) is still open

3. The Degree Conjecture: Every F in S has integer degree.

4. Bombieri-Hejhal (1995): Under statistical independence hypotheses about
   the zeros of distinct L-functions in S, GRH follows. This is the closest
   to a conditional proof via the Euler product structure.

5. The Davenport-Heilbronn function is NOT in the Selberg class because it
   fails axiom (S3) -- no Euler product. Its degree would be 1 (same gamma
   factors as a degree-1 L-function), but without the Euler product it is
   not in S, and indeed violates GRH.

WHAT THE SELBERG CLASS TELLS US:
The Euler product axiom (S3) is not just a technicality -- it is the
DISTINGUISHING feature that separates functions satisfying GRH from those
that don't. Every other axiom (continuation, functional equation, Ramanujan
bound) is shared by DH. Only (S3) fails.
""")

###############################################################################
# 6. The convolution vs addition dichotomy
###############################################################################

print("=== THE CONVOLUTION VS ADDITION DICHOTOMY ===\n")
print("""
Here is the fundamental dichotomy:

EULER PRODUCT (convolution):
  zeta(s) = prod_p (1-p^{-s})^{-1}
  => log zeta(s) = sum_p f_p(s)        [additive in log space]
  => In kernel space: Phi = conv_p phi_p  [convolution of individual kernels]
  => Schoenberg's theorem: convolution preserves PF_infinity
  => Independence of prime contributions
  => Concentration inequalities prevent off-line zeros
  => Log-correlated Gaussian structure at sigma = 1/2

LINEAR COMBINATION (addition):
  L_DH(s) = c1 * L(s,chi1) + c2 * L(s,chi1_bar)
  => In kernel space: Phi_DH = c1 * Phi_1 + c2 * Phi_2  [weighted sum]
  => Addition does NOT preserve PF properties
  => The two terms can destructively interfere
  => No concentration inequalities (the two terms are maximally correlated)
  => Phase cancellation produces off-line zeros

The Euler product converts MULTIPLICATION of L-function values into
ADDITION of logarithmic contributions. This additive decomposition (in log space)
becomes CONVOLUTION in kernel space. Convolution preserves PF (Schoenberg).

The DH construction takes ADDITION in the original function space.
Addition does not become convolution anywhere -- it stays as addition.
Addition does not preserve PF properties.

This is the precise mechanism by which the Euler product prevents off-line zeros:
  PRODUCT -> LOG -> SUM (independent) -> CONVOLUTION (in kernel) -> PF preserved
vs
  SUM (dependent) -> ADDITION (in kernel) -> PF destroyed
""")

# Save results
results = {
    "near_zeros_off_line": [(float(s), float(t), float(v)) for s, t, v in near_zeros],
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/independence_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Results saved.")
