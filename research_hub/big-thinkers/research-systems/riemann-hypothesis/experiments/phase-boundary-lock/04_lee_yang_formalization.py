"""
Experiment 4: Lee-Yang Analogy Formalized

In the Ising model:
- Z(z) = sum_S e^{-beta H(S)} is a polynomial in z = e^{-2*beta*h}
- The Lee-Yang theorem: Z(z) = z^N * Z(1/z) (reflection symmetry on unit circle)
  + all interactions are repulsive (ferromagnetic)
  => ALL zeros of Z lie on |z| = 1

For the Riemann zeta:
- Xi(s) = Xi(1-s) (reflection symmetry across sigma = 1/2)
- What plays the role of "repulsive interactions"?
- Can the Bohr-Jessen convergence serve as the "repulsion"?

We investigate the EXACT structural parallel and identify what's needed.
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, log, sqrt, exp, fabs, zetazero, atan2

mp.dps = 25

# ============================================================
# Part 1: The Ising-Zeta Dictionary
# ============================================================
print("=" * 70)
print("PART 1: The Ising-Zeta Structural Dictionary")
print("=" * 70)

print("""
ISING MODEL                          RIEMANN ZETA
============                          =============
Variable: z = e^{-2*beta*h}          Variable: w = p^{-(s-1/2)} for each prime p
Unit circle: |z| = 1                  Critical line: Re(s) = 1/2 (i.e., |w| = 1)
Z(z) = sum_{configs} z^{n_+}         Xi(s) = Xi(1-s) completed zeta
Z(z) = z^N * Z(1/z)                  Xi(s) = Xi(1-s)  (after z -> w substitution)

PROOF INGREDIENTS:
(1) Polynomial in z                   Xi is NOT polynomial (infinite product)
(2) Z(z) = z^N * Z(1/z)              Xi(s) = Xi(1-s)  ✓ HAVE THIS
(3) All coefficients positive          Euler product factors: 1/(1-p^{-s})
(4) Repulsive (ferromagnetic)          ??? NEED TO IDENTIFY THIS

The Lee-Yang proof works by showing:
  If z_0 is a zero with |z_0| > 1, then z_0^{-1} is also a zero (by symmetry)
  AND: the coefficients being positive + repulsive means |Z(z)| cannot vanish
  for |z| > 1 by a counting/winding number argument.

For zeta, the analogous statement would be:
  If sigma_0 + it_0 is a zero with sigma_0 > 1/2, then (1-sigma_0) + it_0 is also (by FE)
  AND: some "positivity/repulsion" condition prevents |Xi| from vanishing for sigma > 1/2.
""")

# ============================================================
# Part 2: The Euler Product as "Repulsion"
# ============================================================
print("=" * 70)
print("PART 2: Can the Euler Product Convergence Serve as 'Repulsion'?")
print("=" * 70)

print("""
In the Lee-Yang theorem, the key "repulsion" condition is that the partition
function Z(z) can be written as a product of terms, each of which contributes
zeros on |z| = 1. Specifically, for the Ising model with N spins:

Z(z) = product_{i=1}^N (z + a_i) where |a_i| = 1

The zeros of each factor lie on |z| = 1, and a product of such terms has
ALL zeros on |z| = 1.

For zeta, the Euler product gives:
zeta(s) = product_p 1/(1 - p^{-s})

Each factor 1/(1-p^{-s}) has NO zeros (only poles). The zeros of zeta
emerge as a COLLECTIVE effect of infinitely many factors.

This is fundamentally different from Lee-Yang:
- Lee-Yang: each factor contributes zeros on the circle
- Zeta: no finite sub-product has ANY zeros; zeros emerge only in the limit

The Euler product convergence for sigma > 1/2 does NOT directly play the
role of "repulsion" because:
- Convergence means |zeta(sigma+it)| is bounded away from 0 and infinity
  ON AVERAGE (Bohr-Jessen)
- But it doesn't prevent INDIVIDUAL points where |zeta| = 0
- The measure of the set where |zeta| < epsilon is positive for any epsilon > 0
""")

# ============================================================
# Part 3: The Winding Number Approach
# ============================================================
print("=" * 70)
print("PART 3: Winding Number / Argument Principle Analysis")
print("=" * 70)

# The argument principle: for a rectangle [sigma_1, sigma_2] x [0, T],
# the number of zeros = (1/2*pi) * change in arg(zeta(s)) around the boundary
#
# For sigma > 1/2: the Euler product converges, so arg(zeta(sigma+it)) 
# has bounded variation.
# The functional equation forces: arg(zeta(sigma+it)) + arg(chi(sigma+it)) + arg(zeta(1-sigma+it)) 
# to be consistent.

# Let's compute the winding number of zeta along vertical lines
print("\nWinding number of zeta(sigma + it) as t goes from 0 to T:")
print("N(sigma, T) = (1/pi) * [arg(zeta(sigma+iT)) - arg(zeta(sigma+i))]")

for T in [50, 100]:
    print(f"\nT = {T}:")
    print(f"  {'sigma':>6} | {'Wind. number':>14} | {'Expected zeros':>15}")
    print("  " + "-" * 42)
    
    for sigma in [0.50, 0.55, 0.60, 0.70, 0.80, 1.00]:
        # Compute arg change along vertical line
        N_pts = 2000
        t_vals = np.linspace(1, T, N_pts)
        phases = []
        for t in t_vals:
            s = mpc(sigma, t)
            z = zeta(s)
            phases.append(float(atan2(z.imag, z.real)))
        
        # Unwrap phase
        phases = np.unwrap(phases)
        winding = (phases[-1] - phases[0]) / np.pi
        
        # Expected zeros (on sigma = 1/2) in [0, T]:
        # N(T) ~ (T/2*pi)*log(T/(2*pi*e)) (Riemann-von Mangoldt formula)
        expected = T / (2*np.pi) * np.log(T / (2*np.pi*np.e))
        
        print(f"  {sigma:>6.2f} | {winding:>14.2f} | {expected:>15.2f}")

# ============================================================
# Part 4: What Would Make Lee-Yang Work for Zeta?
# ============================================================
print("\n" + "=" * 70)
print("PART 4: What Additional Ingredient Would Make Lee-Yang Work?")
print("=" * 70)

print("""
ANALYSIS OF THE GAP:

The Lee-Yang theorem has THREE ingredients:
(1) Symmetry: Z(z) = z^N * Z(1/z)   [We have Xi(s) = Xi(1-s)]
(2) Polynomial structure                [We do NOT have this - infinite product]
(3) Repulsive interactions              [We do NOT have this]

Existing generalizations:

A. NEWMAN'S GENERALIZATION (1974):
   Works for functions of the form f(z) = integral K(t) z^t dt
   where K is a positive measure with certain regularity.
   Xi(1/2+it) = integral Phi(u) cos(tu) du fits this form!
   BUT: Newman's theorem requires the kernel Phi to satisfy 
   specific conditions (non-negative, log-concave).
   Phi IS non-negative (Polya's criterion), and numerical evidence 
   supports log-concavity.
   THIS IS THE CLOSEST TO A WORKING LEE-YANG PROOF.

B. BORCEA-BRANDEN (2009):
   Extends Lee-Yang to infinite-dimensional settings using 
   "stability preserving" operators.
   The zeta function can potentially be seen as the result of 
   applying a stability-preserving operator to a stable function.
   BUT: showing the operator preserves stability requires controlling 
   the infinite product, which circles back to RH.

C. DE BRUIJN-NEWMAN (2020):
   The heat flow H_t(z) = integral e^{tu^2} Phi(u) cos(zu) du
   Lambda >= 0 (proved by Rodgers-Tao)
   RH iff Lambda = 0
   The heat flow IS a stability-preserving operation (adding e^{tu^2} 
   makes the kernel "more log-concave"), so for t > 0, H_t has all real zeros.
   Lambda = 0 means the unperturbed kernel Phi ALREADY has all real zeros.

D. OUR PROPOSED INGREDIENT: "PHASE-BOUNDARY LOCK"
   The Euler product converges for sigma > 1/2 (Bohr-Jessen)
   PLUS Xi(s) = Xi(1-s) (functional equation)
   QUESTION: Is convergence of the Euler product the RIGHT analog of "repulsion"?

   ARGUMENT:
   - In Lee-Yang, repulsion => each spin feels a "force" toward the real axis
   - In the primon gas, Euler product convergence => log|zeta| has BOUNDED 
     fluctuations for sigma > 1/2
   - Bounded fluctuations mean zeros CANNOT form in the convergent region
     ... except they CAN! The measure of {t : |zeta(sigma+it)| < eps} is positive
     for any eps. Convergence only means this measure is SMALL, not zero.
   
   THE PRECISE GAP: We need ZERO measure, not just SMALL measure, for the 
   zero set. And the zero set of an analytic function IS measure zero. But we 
   need NO zeros at all for sigma > 1/2.
""")

# ============================================================
# Part 5: Numerical test of the "repulsion" hypothesis
# ============================================================
print("=" * 70)
print("PART 5: Testing the 'Repulsion' Hypothesis Numerically")
print("=" * 70)

# For the truncated Euler product Z_N(s), at what rate does 
# min_{t in [0,T]} |Z_N(sigma+it)| decrease with N?
# If it stays bounded away from 0 for sigma > 1/2 but approaches 0 
# for sigma = 1/2, that would support the phase-boundary-lock idea.

print("\nmin |Z_N(sigma+it)| for t in [10, 50], various N and sigma:")
print(f"\n{'N':>6} | {'sigma=0.50':>12} | {'sigma=0.55':>12} | {'sigma=0.60':>12} | {'sigma=0.70':>12} | {'sigma=0.80':>12}")
print("-" * 72)

def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

primes_list = sieve(10000)

for N in [10, 50, 100, 500, 1000]:
    ps = [p for p in primes_list if p <= N]
    
    row = [N]
    for sigma in [0.50, 0.55, 0.60, 0.70, 0.80]:
        min_val = float('inf')
        t_vals = np.linspace(10, 50, 500)
        for t in t_vals:
            s = mpc(sigma, t)
            # Z_N(s) = prod_{p<=N} 1/(1 - p^{-s})
            log_z = sum(float(-log(fabs(1 - mpf(p)**(-s)))) for p in ps)
            z_mag = np.exp(log_z)
            if z_mag < min_val:
                min_val = z_mag
        row.append(min_val)
    
    print(f"{row[0]:>6} | {row[1]:>12.6f} | {row[2]:>12.6f} | {row[3]:>12.6f} | {row[4]:>12.6f} | {row[5]:>12.6f}")

print("""
INTERPRETATION:
If min|Z_N| stays bounded away from 0 for sigma > 1/2 as N grows,
the Euler product has an "inherent repulsion" from zero in that region.
If min|Z_N| -> 0 for sigma = 1/2 (and below), zeros can nucleate there.
""")

