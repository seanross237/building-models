"""
THE MODULAR BOOST PHENOMENON

Key discovery: Individual terms f_n are NOT PF_infinity as functions of u.
The theta-function sum CONSTRUCTIVELY INTERFERES to produce higher PF order.

f_1 alone:  signs = ++-- (PF_3 at best, at u0=0.01, h=0.05)
f_1 + f_2:  signs = +++- (PF_4)
Full Phi:   signs = +++- (PF_4 but not PF_5)

This means: the modular structure of the theta function is ESSENTIAL to PF_4.
It's not that individual terms are "nice" and we need to prove the sum preserves
it. Rather, the individual terms are "bad" and the theta sum FIXES them.

This is deeply connected to the modular transformation. Let's investigate
whether this boost pattern -- where adding more theta terms improves PF order --
could potentially reach PF_5 with some modification.

Also: at what configurations does f_1 become PF_4? Only when u0 is large enough.
The modular correction from f_2 is ESSENTIAL near u0 = 0.
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp
import time

mp.dps = 50

def f_n(n, u):
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def K_partial(u, n_max):
    u_abs = abs(mpf(u))
    return sum(f_n(n, u_abs) for n in range(1, n_max+1))

def toeplitz_det(kfunc, u0, h, r):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)

def main():
    print("=" * 70)
    print("THE MODULAR BOOST: How theta-function structure raises PF order")
    print("=" * 70)

    # Part 1: Track the PF order as we add terms, for several configs
    print("\n--- Part 1: PF order evolution as terms are added ---")

    configs = [
        (0.001, 0.01, "tiny h"),
        (0.001, 0.05, "near origin, moderate h"),
        (0.01, 0.05, "paper counterexample"),
        (0.02, 0.05, "slightly shifted"),
        (0.03, 0.05, "near threshold"),
        (0.05, 0.1, "larger scale"),
    ]

    for u0, h, label in configs:
        print(f"\n  Config (u0={u0}, h={h}): {label}")
        for N in [1, 2, 3, 5]:
            kfunc = lambda u, nm=N: K_partial(u, nm)
            signs = []
            for r in range(2, 7):
                try:
                    d = toeplitz_det(kfunc, u0, h, r)
                    signs.append("+" if d > 0 else ("-" if d < 0 else "0"))
                except:
                    signs.append("?")
            pf_order = 1
            for s in signs:
                if s == "+":
                    pf_order += 1
                else:
                    break
            print(f"    N={N}: D2..D6 signs = {''.join(signs)}  (PF_{pf_order})")

    # Part 2: The boost at (0.01, 0.05) in detail
    print("\n--- Part 2: Detailed boost at (u0=0.01, h=0.05) ---")
    u0, h = 0.01, 0.05
    print(f"  {'N':>3} {'D2':>14} {'D3':>14} {'D4':>14} {'D5':>14}")
    for N in range(1, 11):
        kfunc = lambda u, nm=N: K_partial(u, nm)
        d2 = toeplitz_det(kfunc, u0, h, 2)
        d3 = toeplitz_det(kfunc, u0, h, 3)
        d4 = toeplitz_det(kfunc, u0, h, 4)
        d5 = toeplitz_det(kfunc, u0, h, 5)
        print(f"  {N:>3} {float(d2):>14.6e} {float(d3):>14.6e} {float(d4):>14.6e} {float(d5):>14.6e}")

    # Part 3: Could a "weighted" theta sum achieve PF_5?
    print("\n--- Part 3: Can modifying the theta sum restore PF_5? ---")
    print("  Testing: alpha*f_1 + beta*f_2 with varying alpha, beta")
    print("  Normal theta sum: alpha=1, beta=1")
    print("  At (u0=0.01, h=0.05):")

    for alpha, beta in [(1, 0), (1, 0.5), (1, 1), (1, 1.5), (1, 2), (1, 3), (0.5, 1), (2, 1)]:
        kfunc = lambda u, a=alpha, b=beta: a*f_n(1, abs(mpf(u))) + b*f_n(2, abs(mpf(u)))
        d4 = toeplitz_det(kfunc, 0.01, 0.05, 4)
        d5 = toeplitz_det(kfunc, 0.01, 0.05, 5)
        s4 = "+" if d4 > 0 else "-"
        s5 = "+" if d5 > 0 else "-"
        print(f"  alpha={alpha}, beta={beta}: D4={float(d4):>12.4e}[{s4}] D5={float(d5):>12.4e}[{s5}]")

    # Part 4: The magical balance
    print("\n--- Part 4: The magical balance of the theta sum ---")
    print("""
  Key finding: At (u0=0.01, h=0.05), the theta sum coefficients
  (all = 1, as dictated by theta_3) produce:
    D4 = +3.83e-06 (positive, PF_4 holds)
    D5 = -1.85e-09 (negative, PF_5 fails)

  But f_1 alone has D4 = -8.06e-07 (negative!).
  The correction from f_2 is +4.63e-06, which overwhelms the D4(f_1) contribution.

  This means: the RELATIVE WEIGHT of f_2 vs f_1 in the theta sum is
  CRUCIAL for PF_4. If f_2 were smaller (or weighted differently),
  PF_4 would fail.

  The theta function identity CONSTRAINS these relative weights.
  The Jacobi theta_3 function is:
    theta_3(0, q) = 1 + 2*sum_{n=1}^{inf} q^{n^2}

  For our kernel with q = e^{-pi*e^{4u}}, each f_n gets weight 1.
  The modular transformation tau -> -1/tau constrains the relationship
  between terms in a way that (apparently) ensures PF_4 globally.
""")

    # Part 5: Investigate whether there's a simple explanation
    print("--- Part 5: Log-concavity of f_1 vs the full sum ---")
    print("  Check: is f_1(|u|) log-concave? (PF_2)")

    # Compute log(f_1(u)) and check second derivative
    for u0_test in [0.01, 0.05, 0.1]:
        eps = mpf('0.001')
        logf1_minus = mp.log(f_n(1, mpf(u0_test) - eps))
        logf1_center = mp.log(f_n(1, mpf(u0_test)))
        logf1_plus = mp.log(f_n(1, mpf(u0_test) + eps))
        d2_logf1 = (logf1_plus - 2*logf1_center + logf1_minus) / eps**2
        print(f"  u0={u0_test}: d^2/du^2 log(f_1) = {float(d2_logf1):.6f} ({'concave' if d2_logf1 < 0 else 'CONVEX'})")

        logphi_minus = mp.log(sum(f_n(n, mpf(u0_test) - eps) for n in range(1, 51)))
        logphi_center = mp.log(sum(f_n(n, mpf(u0_test)) for n in range(1, 51)))
        logphi_plus = mp.log(sum(f_n(n, mpf(u0_test) + eps) for n in range(1, 51)))
        d2_logphi = (logphi_plus - 2*logphi_center + logphi_minus) / eps**2
        print(f"           d^2/du^2 log(Phi) = {float(d2_logphi):.6f} ({'concave' if d2_logphi < 0 else 'CONVEX'})")

    # Part 6: Can we prove PF_4 by bounding the correction?
    print("\n--- Part 6: Strategy for proving PF_4 globally ---")
    print("""
  Strategy outline:
  1. For u0 > 0.02 (approximately): f_1 alone has D_4 > 0.
     The correction from f_2, ..., f_N is small (exponentially decreasing).
     PF_4 follows from a perturbation argument.

  2. For u0 near 0: f_1 alone has D_4 < 0.
     We NEED the f_2 correction. The proof would require showing
     that the theta-sum correction is always large enough to flip
     D_4 to positive.

  The difficulty is in case 2. The correction from f_2 involves
  a determinantal expansion with cross-terms between f_1 and f_2.
  Bounding these requires understanding the MATRIX structure, not
  just the scalar values.

  A possible approach: use the Cauchy-Binet formula to decompose
  D_4(sum f_n) into sums of products of minors of individual f_n.
""")

    return

if __name__ == "__main__":
    main()
