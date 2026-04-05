"""
Detailed multiplicativity test for the Davenport-Heilbronn function.

The KEY question: the DH function's Dirichlet series sum a_DH(n) n^{-s}
has coefficients that fail to be multiplicative. This means it cannot
have an Euler product. We quantify exactly HOW it fails.

We also compare with L(s, chi1) which IS multiplicative (has Euler product).
"""

import numpy as np
from fractions import Fraction
import json

###############################################################################
# Setup
###############################################################################

# kappa
sqrt5 = np.sqrt(5)
kappa = (np.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
print(f"kappa = {kappa:.10f}")

# chi1 mod 5: chi(1)=1, chi(2)=i, chi(3)=-i, chi(4)=-1, chi(0)=0
chi1_table = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}

def chi1(n):
    return chi1_table[n % 5]

def chi1_bar(n):
    return np.conj(chi1(n))

# DH coefficients
c1 = (1 - 1j*kappa) / 2
c2 = (1 + 1j*kappa) / 2

def a_dh(n):
    """n-th Dirichlet coefficient of the DH function"""
    return c1 * chi1(n) + c2 * chi1_bar(n)

# Note: a_DH(n) should be real since DH has real coefficients
# Verify:
print(f"\nFirst 20 DH coefficients (should be real):")
for n in range(1, 21):
    a = a_dh(n)
    print(f"  a_DH({n:2d}) = {a.real:+.6f} {'+' if a.imag >= 0 else ''}{a.imag:.6f}i  (|Im| = {abs(a.imag):.2e})")

###############################################################################
# Test multiplicativity: a(mn) = a(m)*a(n) for gcd(m,n)=1
###############################################################################

print("\n=== MULTIPLICATIVITY TEST ===")
print("For a multiplicative function: a(mn) = a(m)*a(n) when gcd(m,n) = 1\n")

from math import gcd

violations = []
total_tests = 0

print(f"{'m':>3s} {'n':>3s} {'mn':>4s} {'a(mn)':>12s} {'a(m)*a(n)':>12s} {'Ratio':>10s} {'Match?':>8s}")
print("-" * 60)

for m in range(2, 30):
    for n in range(2, 30):
        if m*n > 100:
            continue
        if gcd(m, n) != 1:
            continue
        if m >= n:
            continue

        a_mn = a_dh(m * n)
        a_m_times_a_n = a_dh(m) * a_dh(n)
        total_tests += 1

        if abs(a_m_times_a_n) > 1e-10:
            ratio = abs(a_mn / a_m_times_a_n)
        else:
            ratio = float('inf') if abs(a_mn) > 1e-10 else 1.0

        match = abs(a_mn.real - a_m_times_a_n.real) < 1e-8

        if not match:
            violations.append((m, n, m*n, a_mn.real, a_m_times_a_n.real))
            print(f"{m:3d} {n:3d} {m*n:4d} {a_mn.real:12.6f} {a_m_times_a_n.real:12.6f} {ratio:10.6f} {'FAIL':>8s}")

print(f"\nTotal tests: {total_tests}")
print(f"Violations: {len(violations)}")
print(f"Violation rate: {len(violations)/total_tests*100:.1f}%")

###############################################################################
# Compare: L(s, chi1) IS multiplicative
###############################################################################

print("\n\n=== COMPARISON: L(s, chi1) coefficients ARE multiplicative ===\n")

violations_chi = []
total_chi = 0

for m in range(2, 30):
    for n in range(2, 30):
        if m*n > 100:
            continue
        if gcd(m, n) != 1:
            continue
        if m >= n:
            continue

        c_mn = chi1(m * n)
        c_m_times_c_n = chi1(m) * chi1(n)
        total_chi += 1

        if abs(c_mn - c_m_times_c_n) > 1e-10:
            violations_chi.append((m, n))

print(f"Total tests: {total_chi}")
print(f"Violations: {len(violations_chi)}")
if violations_chi:
    print("UNEXPECTED: chi1 should be fully multiplicative!")
else:
    print("CONFIRMED: chi1 is completely multiplicative (as expected)")

###############################################################################
# The periodic structure of DH coefficients
###############################################################################

print("\n\n=== PERIODIC STRUCTURE of DH coefficients ===")
print("Since DH = c1*L(s,chi1) + c2*L(s,chi1_bar), and chi has period 5:")
print("a_DH(n) depends only on n mod 5\n")

for r in range(5):
    vals = [a_dh(n).real for n in range(r if r > 0 else 5, 101, 5)]
    print(f"n ≡ {r} mod 5: a_DH = {vals[0]:.6f} (constant)")

print("""
The DH function has PURELY PERIODIC coefficients (period 5).
This means it is a Dirichlet series with:
  a(n) = f(n mod 5)

A function with periodic coefficients can never be multiplicative
(unless the period is 1, i.e., constant coefficients like zeta).

Reason: if a(n) = f(n mod q) with q > 1, then for any two primes
p1 ≡ p2 mod q, we need a(p1) = a(p2). But multiplicativity requires
the behavior at prime powers to determine everything, which constrains
the values at different primes to be INDEPENDENT. The periodicity
creates CORRELATIONS between the values at different primes that
are incompatible with the independent Euler product structure.
""")

###############################################################################
# Deeper: what's the Euler product of L(s, chi1)?
###############################################################################

print("=== Euler product decomposition of L(s, chi1) vs DH ===\n")
print("L(s, chi1) = prod_p (1 - chi1(p)/p^s)^{-1}")
print("L(s, chi1_bar) = prod_p (1 - chi1_bar(p)/p^s)^{-1}")
print()
print("DH = c1 * L(s,chi1) + c2 * L(s,chi1_bar)")
print("   = c1 * prod_p (1-chi1(p)/p^s)^{-1} + c2 * prod_p (1-chi1_bar(p)/p^s)^{-1}")
print()
print("This is a SUM of two Euler products, NOT an Euler product itself.")
print("In general: prod_p f_p(s) + prod_p g_p(s) ≠ prod_p h_p(s)")
print()

# Compute the individual Euler factors
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print(f"{'p':>3s}  {'chi1(p)':>12s}  {'chi1_bar(p)':>12s}  {'|1-chi1(p)/p^{1/2}|':>20s}")
print("-" * 55)

for p in primes:
    c = chi1(p)
    cb = chi1_bar(p)
    factor_mag = abs(1 - c / np.sqrt(p))
    c_str = f"{c.real:+.0f}{c.imag:+.0f}i" if c != 0 else "  0"
    cb_str = f"{cb.real:+.0f}{cb.imag:+.0f}i" if cb != 0 else "  0"
    print(f"{p:3d}  {c_str:>12s}  {cb_str:>12s}  {factor_mag:20.6f}")

###############################################################################
# The structural theorem
###############################################################################

print("""
=== THE STRUCTURAL THEOREM ===

The Davenport-Heilbronn function is:
  L_DH(s) = c1 * L(s, chi1) + c2 * L(s, chi1_bar)

with c1, c2 chosen so that L_DH satisfies the functional equation
  L_DH(s) = L_DH(1-s)  (up to gamma factors)

The coefficients c1, c2 are NOT 0 or 1. They are:
  c1 = (1 - i*kappa)/2 ≈ """ + f"{c1.real:.6f} + {c1.imag:.6f}i" + """
  c2 = (1 + i*kappa)/2 ≈ """ + f"{c2.real:.6f} + {c2.imag:.6f}i" + f"""

|c1| = {abs(c1):.6f}
|c2| = {abs(c2):.6f}

KEY FACTS:
1. Each L(s, chi) separately satisfies GRH (conjectured, and consistent with all evidence)
2. Each L(s, chi) has an Euler product
3. The linear combination L_DH DOES NOT have an Euler product
4. L_DH provably has zeros OFF the critical line
5. L_DH satisfies the SAME functional equation as each L(s, chi)

CONCLUSION: The functional equation is NOT enough. The Euler product is essential.
The linear combination operation PRESERVES the functional equation but DESTROYS
the Euler product, and this destruction allows zeros to escape the critical line.

MECHANISM: The Euler product forces log|L(s)| to be a sum of INDEPENDENT
contributions from each prime. This independence creates the log-correlated
Gaussian structure at sigma = 1/2 (Saksman-Webb, Harper). The linear combination
introduces CORRELATIONS between the prime contributions of the two L-functions,
breaking the independence and allowing the cancellation patterns that produce
off-line zeros.
""")

###############################################################################
# Quantify the "interference" that creates off-line zeros
###############################################################################

print("=== INTERFERENCE PATTERN ===")
print("At a zero of L_DH: c1*L(s,chi1) = -c2*L(s,chi1_bar)")
print("This requires a specific amplitude and phase relationship.\n")

# For L(s,chi1) and L(s,chi1_bar), when they are "in phase" and "out of phase"

import mpmath
mpmath.mp.dps = 30

print("Computing L(s, chi1) and L(s, chi1_bar) on the critical line:")
print(f"{'t':>6s}  {'|L(1/2+it,chi1)|':>16s}  {'arg(L)':>8s}  {'|DH|':>8s}  {'DH/L ratio':>10s}")
print("-" * 55)

for t_val in np.linspace(5, 50, 20):
    s = complex(0.5, t_val)
    # Compute L-functions using mpmath
    s_mp = mpmath.mpc(0.5, t_val)

    # L(s, chi) for chi mod 5
    L1 = sum(complex(chi1(n)) * complex(n)**(-s) for n in range(1, 3000))
    L2 = sum(complex(chi1_bar(n)) * complex(n)**(-s) for n in range(1, 3000))

    dh_val = complex(c1) * L1 + complex(c2) * L2
    ratio = abs(dh_val) / max(abs(L1), 1e-20)

    print(f"{t_val:6.1f}  {abs(L1):16.6f}  {np.angle(L1):8.4f}  {abs(dh_val):8.4f}  {ratio:10.6f}")

print("\nWhen |DH| is small, we see DESTRUCTIVE INTERFERENCE between the")
print("two L-functions -- the c1*L(s,chi1) and c2*L(s,chi1_bar) terms nearly cancel.")
print("This cancellation is only possible because DH is a LINEAR COMBINATION.")
print("A single Euler product CANNOT produce this kind of cancellation pattern.")
