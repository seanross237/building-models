"""
Investigate the connection between PF_k of the kernel and Jensen polynomial
hyperbolicity of degree d.

Key question: Is PF_4 of the kernel EQUIVALENT to Jensen polynomials of
degree <= 3 being hyperbolic for all shifts n?

The connection goes through the Taylor coefficients. If Phi has Taylor
expansion Phi(u) = sum gamma_k * u^k / k!, then the Toeplitz minor
D_r(0, h) / h^{r(r-1)} involves the gamma_k in a specific way related
to Hankel determinants.

Specifically, for the h -> 0 limit:
  C_r(u0) = lim_{h->0} D_r(u0, h) / h^{r(r-1)}
is a polynomial in the derivatives K'(u0), K''(u0), etc.

For u0=0: C_r(0) involves K^(k)(0) = Phi^(k)(0) for k = 0, ..., 2(r-1).
The connection to Jensen polynomials goes through these derivatives.

Jensen polynomial: J_{d,n}(X) = sum_{j=0}^d C(d,j) * gamma_{n+j} * X^j
where gamma_k = Phi^(2k)(0) / (2k)! (even derivatives only, since Phi is related to xi).

Turan inequality (order 2): gamma_k^2 - gamma_{k-1}*gamma_{k+1} >= 0
  This is equivalent to PF_2 (log-concavity) of the sequence {gamma_k}.

Higher-order Turan: det[gamma_{n+i+j}]_{i,j=0}^{d-1} >= 0 for all n.
  These are Hankel determinants of the sequence {gamma_k}.

KEY INSIGHT: The Toeplitz minors of K(x-y) and the Hankel determinants
of the Taylor coefficients are RELATED but NOT identical.
- Toeplitz: det[K(x_i - x_j)]
- Hankel: det[gamma_{i+j}]

For a kernel K(u) = sum gamma_k * u^{2k} / (2k)! (even function),
the Toeplitz minor at (u0=0, small h) reduces to a Hankel-type determinant
of the gamma_k.

Let's compute both and compare.
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, diff, fac, power
import time

mp.dps = 80

def phi(u, N=50):
    """Polya kernel Phi(u)."""
    u = mpf(u)
    result = mpf(0)
    for n in range(1, N+1):
        n_mpf = mpf(n)
        e4u = exp(4*u)
        e5u = exp(5*u)
        e9u = exp(9*u)
        result += (2*pi**2*n_mpf**4*e9u - 3*pi*n_mpf**2*e5u) * exp(-pi*n_mpf**2*e4u)
    return result

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def phi_derivatives(u0, max_order=10, N=50):
    """Compute Phi^(k)(u0) for k = 0, ..., max_order using numerical differentiation."""
    u0 = mpf(u0)
    derivs = []
    for k in range(max_order + 1):
        d = diff(lambda u: phi(u, N), u0, k)
        derivs.append(d)
    return derivs

def hankel_det(gamma, n, d):
    """
    Compute the (d+1) x (d+1) Hankel determinant:
    det[gamma_{n+i+j}]_{i,j=0}^{d}
    """
    M = matrix(d+1, d+1)
    for i in range(d+1):
        for j in range(d+1):
            idx = n + i + j
            if idx < len(gamma):
                M[i,j] = gamma[idx]
            else:
                M[i,j] = 0  # Truncation
    return det(M)

def toeplitz_det_matrix(u0, h, r, N=50):
    """r x r Toeplitz determinant."""
    u0 = mpf(u0)
    h = mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = K(u0 + (i-j)*h, N)
    return det(M)

def main():
    print("=" * 70)
    print("Jensen Polynomial / PF_k Connection Investigation")
    print("=" * 70)

    # Part 1: Compute Taylor coefficients of Phi at u=0
    print("\n--- Part 1: Taylor coefficients of Phi at u=0 ---")
    print("  Computing derivatives Phi^(k)(0) for k = 0, ..., 12...")

    t0 = time.time()
    derivs = phi_derivatives(0, max_order=12)
    t1 = time.time()
    print(f"  Done in {t1-t0:.1f}s")

    # The Taylor coefficients: gamma_k = Phi^(k)(0) / k!
    print("\n  Taylor coefficients gamma_k = Phi^(k)(0) / k!:")
    gamma = []
    for k in range(len(derivs)):
        gk = derivs[k] / fac(k)
        gamma.append(gk)
        print(f"    gamma_{k} = {float(gk):.15e}  (Phi^({k})(0) = {float(derivs[k]):.6e})")

    # Part 2: Check Turan inequalities
    print("\n--- Part 2: Turan inequalities (Hankel determinants) ---")

    # Order 2 (standard Turan): gamma_k^2 - gamma_{k-1}*gamma_{k+1} >= 0
    print("\n  Order 2 Turan inequalities (gamma_k^2 - gamma_{k-1}*gamma_{k+1}):")
    for k in range(1, len(gamma)-1):
        turan2 = gamma[k]**2 - gamma[k-1]*gamma[k+1]
        sign = "+" if turan2 > 0 else ("-" if turan2 < 0 else "0")
        print(f"    k={k}: {float(turan2):.6e} [{sign}]")

    # Order 3 Hankel: 3x3 Hankel determinants
    print("\n  Order 3 Hankel determinants det[gamma_{n+i+j}]_{i,j=0}^2:")
    for n in range(len(gamma)-4):
        h3 = hankel_det(gamma, n, 2)
        sign = "+" if h3 > 0 else ("-" if h3 < 0 else "0")
        print(f"    n={n}: {float(h3):.6e} [{sign}]")

    # Order 4 Hankel: 4x4 Hankel determinants
    print("\n  Order 4 Hankel determinants det[gamma_{n+i+j}]_{i,j=0}^3:")
    for n in range(len(gamma)-6):
        h4 = hankel_det(gamma, n, 3)
        sign = "+" if h4 > 0 else ("-" if h4 < 0 else "0")
        print(f"    n={n}: {float(h4):.6e} [{sign}]")

    # Order 5 Hankel: 5x5 Hankel determinants
    print("\n  Order 5 Hankel determinants det[gamma_{n+i+j}]_{i,j=0}^4:")
    for n in range(max(0, len(gamma)-8)):
        h5 = hankel_det(gamma, n, 4)
        sign = "+" if h5 > 0 else ("-" if h5 < 0 else "0")
        print(f"    n={n}: {float(h5):.6e} [{sign}]")

    # Part 3: Compare Toeplitz C_r(0) with Hankel determinants
    print("\n--- Part 3: Comparing Toeplitz C_r(0) with Hankel determinants ---")
    print("  Computing C_r(0) = D_r(0, h)/h^{r(r-1)} at small h...")

    h_test = mpf('0.0001')
    for r in range(2, 6):
        dr = toeplitz_det_matrix(0, h_test, r)
        cr = dr / h_test**(r*(r-1))
        print(f"\n  r={r}: C_{r}(0) = {float(cr):.10e}")

        # Compare with Hankel
        if r == 2:
            # C_2(0) should be related to gamma_0^2 - gamma_1^2 or similar
            print(f"    gamma_0^2 = {float(gamma[0]**2):.10e}")
            print(f"    gamma_0*gamma_2 = {float(gamma[0]*gamma[2]):.10e}")
            h2_val = gamma[0]**2 - gamma[0]*gamma[2]  # Not quite right...
            # Actually C_2 = K(0)^2 - K(h)^2, and in the limit:
            # K(h) = K(0) + K''(0)*h^2/2 + ...
            # D_2 = K(0)^2 - K(h)^2 ~ -K(0)*K''(0)*h^2 + ...
            # So C_2 = -K(0)*K''(0) (since r(r-1)=2)
            expected_c2 = -phi(0) * derivs[2] / 2  # Not quite...
            # Actually for an even function K(u) = K(-u):
            # D_2(0, h) = K(0)^2 - K(h)^2 = K(0)^2 - K(h)*K(-h) = K(0)^2 - K(h)^2
            # = [K(0) - K(h)][K(0) + K(h)]
            # ~ [-K''(0)*h^2/2 + ...] * [2K(0) + K''(0)*h^2/2 + ...]
            # ~ -K''(0)*K(0)*h^2 + O(h^4)
            # So C_2 = -K''(0)*K(0)
            # But K''(0) = Phi''(0) (since K(u) = Phi(|u|), K''(0) = Phi''(0))
            # Wait: K(u) = Phi(|u|), so K'(0+) = Phi'(0) but K is even...
            # Actually K(u) = Phi(|u|) is even, so K'(0)=0, K''(0) = Phi''(0)
            val = -phi(0) * derivs[2]
            print(f"    -Phi(0)*Phi''(0) = {float(val):.10e}")
            print(f"    Ratio C_2 / (-Phi(0)*Phi''(0)) = {float(cr/val):.6f}")

    # Part 4: The key theoretical question
    print("\n--- Part 4: Theoretical Analysis ---")
    print("""
  KEY INSIGHT:

  The relationship between PF_k of the kernel K and Hankel positivity
  of the Taylor coefficients is NOT a simple equivalence. Here's why:

  PF_k: det[K(x_i - x_j)]_{i,j=1}^k >= 0 for ALL ordered x_1 < ... < x_k
  Hankel: det[gamma_{n+i+j}]_{i,j=0}^{k-1} >= 0 for ALL n >= 0

  The Toeplitz condition involves K evaluated at ARBITRARY point
  configurations, while the Hankel condition involves the Taylor
  coefficients evaluated at specific shifts n.

  In the h -> 0 limit around u0=0, the Toeplitz minor D_k(0, h)/h^{k(k-1)}
  equals a SPECIFIC polynomial in the gamma_k, which is NOT the same as
  the Hankel determinant.

  However, there IS a connection through the Schoenberg/Karlin theory:
  - PF_infinity of K iff K is in the Polya frequency class
  - K in PF class iff its bilateral Laplace transform is 1/q(s) with q
    in the Laguerre-Polya class
  - q in L-P class iff ALL Hankel determinants of q's Taylor coefficients
    are non-negative
  - This is also equivalent to ALL Jensen polynomials being hyperbolic

  So: PF_infinity <=> ALL Hankel positive <=> ALL Jensen hyperbolic

  For FINITE k: PF_k is STRONGER than Hankel-k-positive because PF_k
  requires positivity for ALL point configurations, not just the specific
  ones arising from the Taylor expansion.

  THEREFORE: PF_4 globally => Hankel-4-positive => degree-3 Jensen
  polynomials are hyperbolic.

  The CONVERSE is false: Hankel-4-positive does NOT imply PF_4.

  Since Csordas-Norfolk-Varga (1986) proved degree-3 Jensen hyperbolicity,
  they proved Hankel-4-positive. But this does NOT prove PF_4.

  PF_4 is a STRICTLY STRONGER condition than what CNV proved.
""")

    # Part 5: What does PF_4 BUY us that Hankel-4 doesn't?
    print("\n--- Part 5: What does PF_4 give beyond Hankel-4? ---")
    print("""
  PF_4 implies that the kernel K is "4th-order positive" in a POINTWISE
  sense -- for ANY 4 points, not just those arising from Taylor expansion.

  In particular, PF_4 constrains the GLOBAL shape of K in ways that
  Hankel conditions on Taylor coefficients do not. The Taylor coefficients
  are LOCAL information (behavior near u=0), while PF_4 is GLOBAL.

  This is significant because:
  1. The zeros of the Fourier transform (the zeta zeros) are determined
     by the GLOBAL behavior of K.
  2. Hankel conditions on Taylor coefficients control behavior near the
     origin but say nothing about large u.
  3. PF_4 constrains the entire profile of K(u) for all u.

  So PF_4 is genuinely new information beyond what CNV proved, and could
  potentially constrain the zero set of the Fourier transform.
""")

    # Part 6: Compute the xi-function Taylor coefficients
    print("\n--- Part 6: Xi-function connection ---")
    print("  The xi-function has Taylor expansion:")
    print("    xi(1/2 + it) = sum_{k=0}^{inf} (-1)^k * a_{2k} * t^{2k}")
    print("  where a_{2k} = gamma_k / (2k)!")
    print("  and xi(s) = (1/2) integral_{-inf}^{inf} Phi(u) * e^{isu} du")
    print("  (Fourier relationship)")
    print("")
    print("  The Fourier transform relates kernel Taylor coefficients gamma_k")
    print("  to xi-function Taylor coefficients in a DUAL way:")
    print("    xi^(2k)(1/2) = (-1)^k * integral Phi(u) * u^{2k} du")
    print("    (moments of Phi)")
    print("")
    print("  PF_k conditions on K constrain these moments.")

    return gamma, derivs

if __name__ == "__main__":
    gamma, derivs = main()
