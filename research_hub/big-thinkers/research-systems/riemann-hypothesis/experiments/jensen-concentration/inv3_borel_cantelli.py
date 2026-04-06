"""
Investigation 3: The Borel-Cantelli Approach

Can we use the concentration inequality + Borel-Cantelli to show that zeros
with Re > sigma_0 are FINITELY MANY?

Framework:
- For each integer T, define A_T = {zeta has a zero with Re > sigma_0, T < Im < T+1}
- If sum_T P(A_T) < infinity, Borel-Cantelli says only finitely many A_T occur
- This would mean: for T > T_0, no zeros with Re > sigma_0 in [T, T+1]
- Combined with numerical verification below T_0, this proves RH for Re > sigma_0

The key question: what is P(A_T)?

SUBTLETY #1: A_T is NOT a probabilistic event.
Zeta is a deterministic function. "P(A_T)" must be interpreted as:
- The proportion of T-values in [1, X] for which A_T occurs (as X -> inf)
- Or: the probability in the Bohr-Jessen random model

In the Bohr-Jessen model:
- Replace n^{-it} by n^{-X_t} where X_t are random
- The distribution of log zeta(sigma + iX_t) is approximately Gaussian
- with mean 0 and variance V(sigma)

SUBTLETY #2: "P(zeta has a zero)" is not the same as "P(zeta is small at a point)".
A zero requires |zeta(sigma+it)| = 0 for SOME sigma > sigma_0, not just one fixed point.

Strategy:
1. Cover [sigma_0, 1] x [T, T+1] with a grid of spacing delta.
2. P(A_T) <= sum over grid points P(|zeta(grid point)| < C*delta)
3. Use concentration to bound each P(|zeta| < C*delta)
4. Sum the grid contributions
5. Sum over T and check convergence
"""

import mpmath
from mpmath import mp, mpf, log, pi, sqrt, exp, power
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
print("INVESTIGATION 3: BOREL-CANTELLI APPROACH")
print("=" * 70)

# Part 1: Concentration-based bound on P(|zeta| < epsilon)
print("\n--- Part 1: P(|zeta(sigma+it)| < epsilon) from Concentration ---")
print("""
The Bohr-Jessen distribution of log|zeta(sigma+it)| for sigma > 1/2:

As T -> inf, the distribution of log|zeta(sigma+it)| for t in [0,T]
converges to a distribution with:
  - Mean: mu(sigma) = -sum_p log|1 - p^{-sigma}| ≈ 0 for sigma >> 1/2
    More precisely: mu(sigma) = sum_p [-log(1-p^{-2sigma})/2 + O(p^{-3sigma})]
    (from the real part of log(1-p^{-s})^{-1} averaged over t)
  - Variance: V(sigma) = sum_p p^{-2sigma}/2 + higher terms

The tail bound from concentration:
  P(log|zeta(sigma+it)| < -M) <= exp(-M^2 / (2*V(sigma)))

For |zeta| < epsilon: log|zeta| < log(epsilon), so M = -log(epsilon) = log(1/epsilon).
  P(|zeta(sigma+it)| < epsilon) <= exp(-log(1/epsilon)^2 / (2*V(sigma)))
                                  = epsilon^{log(1/epsilon) / (2*V(sigma))}

For small epsilon, this is VERY small (super-polynomial in 1/epsilon).

BUT: This is for a FIXED point sigma + it.
For a ZERO, we need |zeta| = 0 at SOME point, not a fixed point.
""")

# Compute P(|zeta| < epsilon) for various sigma and epsilon
print("\nP(|zeta(sigma+it)| < epsilon) upper bound from concentration:")
print(f"{'sigma':>6} {'epsilon':>10} {'V(sigma)':>10} {'P bound':>14} {'log10(P)':>10}")
print("-" * 55)

for sigma in [0.6, 0.7, 0.8, 0.9]:
    V = V_sigma_full(sigma, 2000)
    for eps_exp in [-1, -2, -5, -10]:
        eps = 10**eps_exp
        M = -mlog(eps)
        log_P = -M**2 / (2*V)
        log10_P = log_P / mlog(10)
        print(f"{sigma:>6.1f} {eps:>10.0e} {V:>10.4f} {mexp(log_P):>14.6e} {log10_P:>10.1f}")
    print()

# Part 2: Grid covering argument
print("\n--- Part 2: Grid Covering for P(A_T) ---")
print("""
To bound P(A_T) = P(zeta has zero with Re > sigma_0 in [T, T+1]):

Step 1: Discretize. Cover [sigma_0, 1-delta] x [T, T+delta] with grid spacing delta.
  Number of grid points: N_grid = (1-sigma_0)/delta * (1/delta) = (1-sigma_0)/delta^2

Step 2: If zeta has a zero at beta+igamma, then |zeta(grid point)| < C*delta
  for the nearest grid point. (This uses Lipschitz continuity of zeta;
  |zeta'(s)| <= C*T^{mu+epsilon} in the critical strip, so
  |zeta(s) - zeta(s')| <= C*T^{mu+epsilon}*|s-s'| <= C*T^{mu+epsilon}*delta)

  For a ZERO at s', the nearest grid point s has:
  |zeta(s)| = |zeta(s) - zeta(s')| <= C*T^{mu+epsilon}*delta

  So P(A_T) <= N_grid * max_{s in grid} P(|zeta(s)| < C*T^{mu}*delta)

Step 3: Use concentration:
  P(|zeta(s)| < C*T^{mu}*delta) <= exp(-log(1/(C*T^{mu}*delta))^2 / (2*V(sigma)))

Step 4: Optimize delta.
  P(A_T) <= (1-sigma_0)/delta^2 * exp(-log(1/(C*T^{mu}*delta))^2 / (2*V(sigma_0)))

  Let u = log(1/(C*T^{mu}*delta)) = log(1/C) - mu*log(T) - log(delta)
  = -mu*log(T) + log(1/delta) + O(1)

  For delta = T^{-a}: u = -mu*log(T) + a*log(T) + O(1) = (a-mu)*log(T)
  N_grid = (1-sigma_0) * T^{2a}

  P(A_T) <= (1-sigma_0) * T^{2a} * exp(-(a-mu)^2 * log(T)^2 / (2*V(sigma_0)))
           = (1-sigma_0) * T^{2a} * T^{-(a-mu)^2 * log(T) / (2*V(sigma_0))}

  Wait -- let me redo this. With u = (a-mu)*log(T):
  exp(-u^2/(2V)) = exp(-(a-mu)^2 * (log T)^2 / (2V))

  This is SUPER-EXPONENTIALLY small in log(T)! It decays like exp(-C*(log T)^2).
  The grid factor T^{2a} = exp(2a*log T) is only exponential in log(T).

  So for log(T) large enough: exp(-C*(log T)^2) << T^{-2a-2}

  This means: sum_T P(A_T) < infinity for ANY sigma_0 > 1/2!

  THIS WOULD PROVE RH (for a random model)!

  But wait -- there's a catch...
""")

# Part 3: Compute the bound explicitly
print("\n--- Part 3: Explicit Computation ---")
print(f"{'sigma_0':>8} {'T':>10} {'delta':>10} {'N_grid':>10} {'P(single)':>14} {'P(A_T)':>14} {'Sum conv?':>10}")
print("-" * 85)

for sigma_0 in [0.51, 0.55, 0.6, 0.7, 0.8]:
    V = V_sigma_full(sigma_0, 2000)
    mu = 0.16  # Bourgain's bound mu(1/2) <= 13/84 ~ 0.155

    convergent = True
    for T_exp in [4, 6, 10, 20, 50]:
        T = 10**T_exp
        log_T = mlog(T)

        # Choose delta = T^{-a} with a = 1 (say)
        a = 1.0
        delta = T**(-a)
        N_grid = int((1-sigma_0) / delta**2) + 1

        # The nearest grid point argument
        # |zeta(grid)| < C * T^mu * delta
        C_lip = 1.0
        eps_eff = C_lip * T**mu * delta  # = T^{mu-a}
        if eps_eff >= 1:
            P_single = 1.0
        else:
            M_eff = -mlog(eps_eff)  # = (a-mu)*log(T)
            log_P_single = -M_eff**2 / (2*V)
            P_single = mexp(max(log_P_single, -700))  # avoid underflow

        P_AT = min(1.0, N_grid * P_single)

        # Check if sum converges: need P(A_T) * T to be summable
        # P(A_T) needs to decay faster than 1/T^{1+epsilon}
        if T_exp >= 10:
            if P_AT > 0 and P_AT < 1e-300:
                sum_conv = "YES (easily)"
            elif P_AT == 0:
                sum_conv = "YES (=0)"
            elif P_AT < T**(-2):
                sum_conv = "YES"
            else:
                sum_conv = "NO"
                convergent = False
        else:
            sum_conv = "-"

        print(f"{sigma_0:>8.2f} {T:>10.0e} {delta:>10.2e} {N_grid:>10.0e} {P_single:>14.4e} {P_AT:>14.4e} {sum_conv:>10}")
    print()

# Part 4: The fatal catch
print("\n--- Part 4: THE FATAL CATCH ---")
print("""
The computation above gives P(A_T) ~ exp(-C * (log T)^2), which is summable.
This would prove RH if the probabilistic model were exact.

BUT: The Bohr-Jessen model is NOT exact. The errors come from:

1. FINITE PRIME APPROXIMATION.
   The random model replaces {t*log(p) mod 2*pi}_p with independent uniform
   random variables. This is accurate in the LIMIT T -> infinity (by Kronecker's
   theorem / equidistribution), but the ERROR in this approximation is:

   |P_actual(|zeta| < eps) - P_model(|zeta| < eps)| <= ???

   The best known bounds (Montgomery-Vaughan, Goldston-Gonek) give:
   Error <= C * (log T)^{-A} for some A > 0

   This is a POWER of log T decay, not a super-exponential decay.

2. THE TAIL ISSUE.
   Our concentration bound gives GAUSSIAN tails: exp(-M^2/(2V)).
   The Bohr-Jessen limit theorem says the tails ARE approximately Gaussian.
   But the approximation error in the Gaussian approximation is:

   |P(log|zeta| < -M) - Phi(-M/sqrt(V))| <= C/M  (Berry-Esseen type bound)

   For M ~ (log T), this error is ~ C/(log T), which is BIGGER than the
   main term exp(-C*(log T)^2) that we're trying to use!

   In other words: the Gaussian approximation is good for M = O(sqrt(V)),
   but we're using it for M = O(log T) >> sqrt(V). The approximation
   breaks down precisely where we need it.

3. THE CONTINUITY/LIPSCHITZ ISSUE.
   We used |zeta(s) - zeta(s')| <= C*T^mu*|s-s'|. The constant C here
   depends on the maximum of |zeta'| in the region, which can be large
   near zeros. If there IS a zero nearby, the Lipschitz bound is tight;
   if not, it's wasteful. This is circular reasoning.

4. THE JOINT DISTRIBUTION ISSUE.
   We used a UNION BOUND over grid points: P(A_T) <= sum P(|zeta(s_i)| < eps).
   This ignores CORRELATIONS between nearby points. The Bohr-Jessen model
   gives the marginal distribution at each point, but the joint distribution
   (needed for the union bound to be useful) requires more:

   P(|zeta(s_1)| < eps AND |zeta(s_2)| < eps) << P(|zeta(s_1)| < eps)^2

   This correlation structure is where the Euler product plays a role,
   but quantifying it is exactly the hard problem.

CONCLUSION: The Borel-Cantelli approach fails because:
(a) The probabilistic model is only accurate to polynomial-in-log(T) precision.
(b) We need super-exponential-in-log(T) precision for the sum to converge.
(c) The gap between (a) and (b) is exactly where the difficulty lies.
""")

# Part 5: What precision would we need?
print("\n--- Part 5: Required vs Available Precision ---")
print("""
For the sum P(A_T) to converge, we need P(A_T) < T^{-1-epsilon} for large T.

From the random model: P(A_T) ~ exp(-C*(log T)^2), which is << T^{-1-epsilon}.

Available precision of the random model approximation:
  |P_actual - P_model| <= C * (log T)^{-A}  [best known]

For the Borel-Cantelli argument:
  P_actual(A_T) <= P_model(A_T) + |P_actual - P_model|
                 <= exp(-C*(log T)^2) + C*(log T)^{-A}
                 ~ C*(log T)^{-A}  [the error dominates!]

We need: C*(log T)^{-A} < T^{-1-epsilon} = exp(-(1+epsilon)*log T)
  i.e., (log T)^{-A} < exp(-(1+epsilon)*log T)
  i.e., A*log(log T) > (1+epsilon)*log T
  i.e., A > (1+epsilon)*log T / log(log T)

This requires A to GROW with T. But A is a FIXED constant in the
approximation theorem. So this NEVER holds for large T.

ALTERNATIVE: Could we improve the approximation precision?

The Bohr-Jessen theorem gives the limit as T -> inf. The rate of convergence
is controlled by the equidistribution of {t*log p mod 2pi}.

By Baker's theorem (transcendental number theory), log(p1)/log(p2) is
irrational for distinct primes p1, p2, and the equidistribution rate is:

  Discrepancy(t*log p1, ..., t*log p_k mod 2pi) <= C_k / T

for the first k primes. The constant C_k GROWS with k (exponentially in k).

For the Euler product with k primes:
  P_k(|zeta_k| < eps) is computed EXACTLY from the k-fold uniform distribution.
  The error from truncating at k primes: O(p_{k+1}^{-sigma})

  For sigma > 1/2: p_{k+1}^{-sigma} ~ (k*log k)^{-sigma} ~ k^{-sigma}
  For this to be < T^{-1}: k > T^{1/sigma}

  With k primes, the equidistribution error is ~ C_k / T.
  We need C_k / T < T^{-1-epsilon}, so C_k < T^{-epsilon}.
  But C_k ~ exp(c*k), so we need k < (epsilon/c)*log T.

  CONFLICT: truncation requires k > T^{1/sigma}, equidistribution requires k < C*log T.
  For T large, T^{1/sigma} >> C*log T. IMPOSSIBLE.

This quantifies why the random model approach cannot work:
the number of primes needed for the truncation approximation
grows polynomially in T, but the equidistribution can only
handle logarithmically many primes.
""")

# Part 6: Salvage — what CAN Borel-Cantelli give?
print("\n--- Part 6: What CAN Borel-Cantelli Give? ---")
print("""
Even though Borel-Cantelli can't prove RH, it CAN give:

1. DENSITY-ONE RESULT (already known):
   For sigma > 1/2, "almost all" zeros have Re < sigma in a density sense.
   This is weaker than RH but follows from concentration.

   Specifically: N(sigma, T) / N(1/2, T) -> 0 as T -> inf for sigma > 1/2.
   This is the density hypothesis, which follows from Ingham's density estimate.

2. CONDITIONAL RESULTS:
   IF the random model approximation could be improved to
   |P_actual - P_model| <= exp(-c*(log T)^2)  (super-exponential precision),
   THEN Borel-Cantelli would give RH.

   This would require a version of the equidistribution theorem with
   exponentially good error terms for exponentially many "frequencies."
   Such a result would be a major breakthrough in its own right.

3. RH FOR RANDOM EULER PRODUCTS:
   In the Bohr-Jessen random model, the "random zeta function"
   zeta_random(s) = prod_p (1 - p^{-sigma} * e^{-i*theta_p})^{-1}
   (with theta_p independent uniform) almost surely has no zeros for sigma > 1/2.

   This IS a theorem (Bohr-Jessen 1932, plus Selberg CLT for the variance).
   Our concentration argument is essentially a reproof of this.

   The gap: "almost surely" in the RANDOM model does not imply "surely"
   for the SPECIFIC deterministic function zeta.

HONEST ASSESSMENT: The Borel-Cantelli approach is a dead end for proving RH.
It works in the random model (where it's already known) and fails for the
deterministic function (where we need it). The failure is fundamental:
the approximation precision available is polynomial in log T, but
super-exponential precision is needed.
""")

# Save results
results = {
    'finding': 'Borel-Cantelli fails due to model approximation precision gap',
    'random_model_bound': 'P(A_T) ~ exp(-C*(log T)^2) — super-exponentially small',
    'approximation_error': '|P_actual - P_model| ~ (log T)^{-A} — polynomial in log T',
    'gap': 'Need super-exponential precision, only have polynomial precision',
    'root_cause': 'Truncation needs T^{1/sigma} primes, equidistribution handles only O(log T) primes',
    'salvage': 'RH for random Euler products (already known), density-one result (already known)',
    'verdict': 'Dead end for proving RH'
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/jensen-concentration/inv3_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to inv3_results.json")
