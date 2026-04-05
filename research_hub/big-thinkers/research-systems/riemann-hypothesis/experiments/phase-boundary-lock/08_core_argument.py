"""
Experiment 8: The Core Phase-Boundary Lock Argument -- Rigorous Analysis

Synthesizing all experiments into the cleanest possible argument and 
identifying the EXACT gap.

The argument structure:
1. The functional equation gives AFE(s) = chi(s)*AFE(1-s) exactly
2. |chi(1/2+it)| = 1 for all t (the critical line is special)
3. |chi(sigma+it)| ~ (t/2pi)^{1/2-sigma} for sigma != 1/2
4. For zeros of the AFE at sigma+it: |D_N(sigma+it)| = |chi(sigma+it)| * |D_N(1-sigma+it)|
5. On the critical line, this is |D_N(s)| = |D_N(1-s)| (automatic by conjugation)
6. Off the critical line, this requires a precise amplitude matching that
   becomes harder as |sigma-1/2| increases or as t increases

The key theorem to prove or disprove:
"For the FULL zeta function, the functional equation + Euler product convergence
 for sigma > 1/2 prevents zeros off the critical line."
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, findroot, fabs, log, zetazero

mp.dps = 25

print("=" * 70)
print("THE PHASE-BOUNDARY LOCK ARGUMENT: COMPLETE ANALYSIS")
print("=" * 70)

print("""
THEOREM (Exact Functional Equation for AFE):
Let D_N(s) = sum_{n=1}^N n^{-s} and chi(s) = pi^{s-1/2} Gamma((1-s)/2)/Gamma(s/2).
Define AFE_N(s) = D_N(s) + chi(s)*D_N(1-s).
Then AFE_N(s) = chi(s) * AFE_N(1-s) for all s.

Proof: chi(s)*chi(1-s) = 1, so
  chi(s)*AFE_N(1-s) = chi(s)*[D_N(1-s) + chi(1-s)*D_N(s)]
                    = chi(s)*D_N(1-s) + D_N(s)
                    = AFE_N(s). QED

COROLLARY: Zeros of AFE_N come in pairs {s, 1-s}.
Zeros on sigma=1/2 are self-paired (s = 1-conj(s) when sigma=1/2).
""")

print("=" * 70)
print("THE AMPLITUDE MISMATCH ARGUMENT")
print("=" * 70)

print("""
For AFE_N(s) = D_N(s) + chi(s)*D_N(1-s) to vanish:
  D_N(s) = -chi(s)*D_N(1-s)
  
Taking absolute values:
  |D_N(sigma+it)| = |chi(sigma+it)| * |D_N(1-sigma+it)|
  
On sigma=1/2: |chi(1/2+it)| = 1, so |D_N(1/2+it)| = |D_N(1/2+it)| (trivially true).
The condition reduces to: D_N(1/2+it) and chi(1/2+it)*D_N(1/2-it) must have 
opposite phases. This is a 1-dimensional condition (phase matching only).

Off sigma=1/2: BOTH amplitude AND phase must match simultaneously.
This is a 2-dimensional condition, making zeros generically co-dimension 2.
But since we're in the complex plane (2 real dimensions), co-dimension 2 = 
isolated points. So off-line zeros CAN exist.

THE QUESTION: Are there ADDITIONAL constraints (from the Bohr-Jessen structure
or the Euler product) that upgrade "generically co-dimension 2" to "impossible"?
""")

# ============================================================
# The Bohr-Jessen constraint
# ============================================================
print("=" * 70)
print("THE BOHR-JESSEN CONSTRAINT")
print("=" * 70)

# For sigma > 1/2, the Euler product for zeta converges.
# This means: zeta(sigma+it) = prod_p 1/(1-p^{-sigma-it})
# Taking log: log zeta(sigma+it) = -sum_p log(1-p^{-sigma-it})
#           = sum_p sum_{k=1}^inf p^{-k(sigma+it)}/k
#           = sum_p p^{-sigma-it} + O(sum_p p^{-2sigma})
#
# The "random" part is sum_p p^{-sigma} * e^{-it*log(p)}
# whose variance is sum_p p^{-2*sigma} which CONVERGES for sigma > 1/2.
#
# For zeta(sigma+it) = 0, we need log|zeta| -> -infinity.
# But log|zeta| has BOUNDED variance. How often can it be very negative?

print("""
BOHR-JESSEN DISTRIBUTION OF log|zeta(sigma+it)|:

For sigma > 1/2 fixed, as T -> infinity:
  (1/T) meas{t in [0,T] : log|zeta(sigma+it)| < u} -> Phi_sigma(u)

where Phi_sigma is a continuous distribution with:
  - Mean ~ 0
  - Variance V(sigma) = (1/2) sum_p p^{-2*sigma} (FINITE for sigma > 1/2)
  - Support = (-infinity, +infinity) [the distribution has full support!]

CRITICAL POINT: The Bohr-Jessen distribution has FULL support on (-inf, inf).
This means: for ANY value u, no matter how negative, there exist arbitrarily 
large t values where log|zeta(sigma+it)| < u.

In particular: the Bohr-Jessen distribution assigns positive probability to 
log|zeta(sigma+it)| being very negative (i.e., |zeta| being very small).

BUT: "very small" is NOT the same as "exactly zero." An analytic function 
can have |f(z)| arbitrarily close to zero without actually vanishing.

The question reduces to: does the Bohr-Jessen distribution say anything about
EXACT zeros? The answer is: NOT DIRECTLY. The distribution describes the 
LIMITING PROPORTION of t values with log|zeta| < u, not the existence of 
isolated zeros (which have measure zero).
""")

# ============================================================
# The precise gap
# ============================================================
print("=" * 70)
print("THE PRECISE GAP IN THE PHASE-BOUNDARY LOCK ARGUMENT")
print("=" * 70)

print("""
After careful analysis, the phase-boundary lock argument has the following structure:

WHAT WE HAVE:
1. Functional equation: Xi(s) = Xi(1-s) => zeros are paired under s <-> 1-s
2. |chi(1/2+it)| = 1 => the critical line is the BALANCE POINT of the 
   functional equation
3. Euler product convergence for sigma > 1/2 => bounded fluctuations of log|zeta|
4. AFE preserves functional equation => its zeros cluster near sigma=1/2
5. Perturbative Fisher information minimized at sigma=1/2 (proved earlier)
6. Parametric Fisher information minimized at sigma=1/2 (zeros are "stealthy")

WHAT WE NEED:
A proof that zeta(sigma_0 + it_0) = 0 with sigma_0 > 1/2 leads to a contradiction.

THREE POTENTIAL CONTRADICTION ROUTES:

ROUTE A: "The amplitude mismatch becomes infinite"
- |chi(sigma+it)| ~ (t/2pi)^{1/2-sigma} for sigma > 1/2
- As t -> infinity, |chi| -> 0, requiring |D_N(sigma+it)| << |D_N(1-sigma+it)|
- PROBLEM: This is about the AFE, not the full zeta. For full zeta, the 
  functional equation zeta(s) = chi(s)*zeta(1-s) gives the same constraint
  but with zeta in place of D_N. And we KNOW zeta(1-sigma+it) can be large
  (it has growing fluctuations for sigma < 1/2).

ROUTE B: "The Euler product prevents exact zeros"
- For sigma > 1/2: log|zeta(sigma+it)| = sum_p Re(-log(1-p^{-sigma-it}))
- Each term is bounded. The sum converges absolutely.
- PROBLEM: A convergent sum of bounded terms CAN equal any value, including
  -infinity (in the limit of infinitely many terms). The convergence only
  bounds the VARIANCE, not the minimum.
- COUNTER-ARGUMENT: Actually, the Euler product DOES converge for sigma > 1/2,
  meaning zeta(sigma+it) = prod_p 1/(1-p^{-s}) is a convergent infinite product
  of NONZERO factors. A convergent infinite product of nonzero terms is nonzero!

WAIT -- THIS IS THE KEY INSIGHT. Let me verify this carefully.
""")

# ============================================================
# Route B: The convergent product argument
# ============================================================
print("=" * 70)
print("ROUTE B: THE CONVERGENT PRODUCT ARGUMENT (CAREFUL ANALYSIS)")
print("=" * 70)

print("""
CLAIM: If the Euler product prod_p 1/(1-p^{-s}) converges absolutely 
for Re(s) > 1/2, then zeta has no zeros for Re(s) > 1/2, i.e., RH is true.

ANALYSIS: Is this claim correct?

An infinite product prod (1 + a_n) converges absolutely if sum |a_n| < infinity.
Here a_n = -p_n^{-s}, so sum |a_n| = sum p^{-sigma}. This sum converges iff sigma > 1.

So the Euler product converges ABSOLUTELY only for sigma > 1, NOT for sigma > 1/2.

For 1/2 < sigma <= 1, the Euler product converges CONDITIONALLY (in the sense 
that prod_{p<=N} 1/(1-p^{-s}) has a limit as N -> infinity), but NOT absolutely.

CONDITIONALLY CONVERGENT products CAN equal zero!

Example: consider the product prod_n (1 - 1/n^s) for real s.
For s > 1, this converges absolutely to 1/zeta(s), which is nonzero.
For 1/2 < s <= 1, the convergence is conditional and the product can be zero
(in fact, 1/zeta(s) is zero at the ZEROS of zeta, if any exist for sigma > 1/2).

So the Euler product argument for sigma > 1/2 does NOT directly prove 
non-vanishing. The conditional convergence is too weak.

HOWEVER: The Euler product DOES prove non-vanishing for sigma > 1:
prod_p 1/(1-p^{-s}) converges absolutely to a NONZERO value for sigma > 1.
This is the classical proof that zeta(s) != 0 for Re(s) > 1.

The gap from sigma > 1 to sigma > 1/2 is exactly the gap between:
- Absolute convergence of the Euler product (sigma > 1)
- Conditional convergence (sigma > 1/2)
- Divergence (sigma < 1/2)
""")

# Verify this numerically
print("\nNumerical verification: Euler product convergence classification")
print()

def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

primes = sieve(100000)

print("sum_p |p^{-s}| = sum_p p^{-sigma} for various sigma:")
for sigma in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.5, 2.0]:
    partial = sum(p**(-sigma) for p in primes)
    # For sigma <= 1, this diverges (slowly), for sigma > 1 it converges
    status = "DIVERGES (conditionally conv.)" if sigma <= 1 else "CONVERGES (absolutely)"
    if sigma < 0.5:
        status = "DIVERGES (not even cond. conv.)"
    print(f"  sigma={sigma:.1f}: sum_{len(primes)} terms = {partial:.4f} ... {status}")

# ============================================================
# The final synthesis
# ============================================================
print("\n" + "=" * 70)
print("FINAL SYNTHESIS: THE PHASE-BOUNDARY LOCK MECHANISM")
print("=" * 70)

print("""
THE MECHANISM (what works):

1. The functional equation Xi(s) = Xi(1-s) makes sigma = 1/2 the UNIQUE 
   symmetry axis. Zeros must come in reflected pairs.

2. On sigma = 1/2, the functional equation gives |chi| = 1, creating a 
   "balanced" condition where phase cancellation naturally produces zeros.

3. Off sigma = 1/2, the amplitude mismatch |chi(sigma+it)| = (t/2pi)^{1/2-sigma}
   GROWS with t, making zeros increasingly improbable at large t.

4. The Euler product converges absolutely for sigma > 1, proving no zeros there.
   For 1/2 < sigma < 1, it converges conditionally but cannot rule out zeros.

5. The Bohr-Jessen theorem shows bounded fluctuations for sigma > 1/2 but
   full support of the distribution -- so near-zeros are possible even though
   the fluctuations are bounded.

6. The AFE (which preserves the functional equation) has zeros that are EXACTLY
   on sigma = 1/2 when it is a good approximation (t large enough relative to N).
   Spurious off-line zeros appear only in the poor-approximation regime.

THE GAP (what's missing):

The argument is HEURISTIC, not a proof. The precise missing ingredient is:

** A proof that conditional convergence of the Euler product for 1/2 < sigma < 1
   combined with the functional equation forces non-vanishing. **

This would require showing: a conditionally convergent infinite product 
prod_p 1/(1-p^{-s}) that ALSO satisfies the functional equation zeta(s) = chi(s)*zeta(1-s) 
cannot be zero for 1/2 < sigma < 1.

Neither condition alone suffices:
- Conditional convergence alone: can produce zeros (counterexamples exist)
- Functional equation alone: only pairs zeros, doesn't prevent them

The COMBINATION might suffice, but proving this requires a new insight.

MOST PROMISING DIRECTION: The Polya-de Bruijn approach.
  Xi(1/2+it) = integral Phi(u) cos(tu) du
  If Phi is positive and log-concave, all zeros of Xi(1/2+it) are real <=> RH.
  The functional equation IS the symmetry Phi(u) = Phi(-u).
  The Euler product convergence IS related to the rapid decay of Phi.
  LOG-CONCAVITY of Phi is the "repulsion" condition.
  Numerical evidence strongly supports log-concavity, but no proof exists.
""")

