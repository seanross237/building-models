"""
CRITICAL FINDING: f_1 alone is NOT PF_infinity as a function of u!

f_1(u) = [2*pi^2*e^{9u} - 3*pi*e^{5u}] * e^{-pi*e^{4u}}

This is NOT a simple Gaussian. Let's analyze its properties carefully.
It IS a PF_infinity function? Let's check.

A function g(x) is PF_infinity if:
  1. g(x) >= 0 for all x, AND
  2. All Toeplitz minors det[g(x_i - x_j)] >= 0

For g(x) = e^{-alpha*x^2}, this holds (Gaussian is PF_infinity).
For g(x) = e^{-alpha*cosh(x)}, this is NOT obviously PF_infinity.

f_1(u) involves e^{-pi*e^{4u}}, which is NOT a Gaussian in u.
Under the substitution t = e^{4u}, we get functions of t that might be
PF_infinity in t, but the composition with u -> e^{4u} does not preserve PF.

Let's understand WHY f_1 has negative Toeplitz minors and why the sum
f_1 + f_2 + ... can have POSITIVE minors.
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, log, sqrt
import time

mp.dps = 50

def f_n(n, u):
    """Single term f_n(u) of the Polya kernel."""
    n = mpf(n)
    u = mpf(u)
    e4u = exp(4*u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*e4u)

def phi(u, N=50):
    return sum(f_n(n, u) for n in range(1, N+1))

def K_fn(u, n):
    """Kernel from a single term: K_n(u) = f_n(|u|)."""
    return f_n(n, abs(mpf(u)))

def K_full(u, N=50):
    return phi(abs(mpf(u)), N)

def toeplitz_det_func(kfunc, u0, h, r):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)

def main():
    print("=" * 70)
    print("f_1 Analysis: Why f_1 alone is NOT PF_infinity")
    print("=" * 70)

    # Part 1: Check f_1 positivity
    print("\n--- Part 1: Is f_1(u) >= 0 for all u >= 0? ---")
    print("  f_1(u) = [2*pi^2*e^{9u} - 3*pi*e^{5u}] * e^{-pi*e^{4u}}")
    print("  The bracket 2*pi^2*e^{9u} - 3*pi*e^{5u} = pi*e^{5u}*(2*pi*e^{4u} - 3)")
    print("  This is zero when e^{4u} = 3/(2*pi), i.e. u = (1/4)*ln(3/(2*pi))")
    u_zero = float(log(3/(2*pi)) / 4)
    print(f"  u_zero = {u_zero:.6f}")
    print(f"  Since 3/(2*pi) = {3/(2*np.pi):.6f} < 1, u_zero < 0.")
    print(f"  So for u >= 0: f_1(u) > 0. Good.")

    # Check a few values
    for u in [0, 0.01, 0.1, 0.5, 1.0, 2.0]:
        print(f"  f_1({u}) = {float(f_n(1, u)):.6e}")

    # Part 2: The Toeplitz structure of f_1
    print("\n--- Part 2: Toeplitz minors of K_1(u) = f_1(|u|) ---")
    configs = [(0.01, 0.05), (0.01, 0.01), (0.01, 0.1), (0.1, 0.1), (0.2, 0.2)]
    for u0, h in configs:
        kfunc = lambda u: K_fn(u, 1)
        d2 = toeplitz_det_func(kfunc, u0, h, 2)
        d3 = toeplitz_det_func(kfunc, u0, h, 3)
        d4 = toeplitz_det_func(kfunc, u0, h, 4)
        d5 = toeplitz_det_func(kfunc, u0, h, 5)
        s2 = "+" if d2 > 0 else "-"
        s3 = "+" if d3 > 0 else "-"
        s4 = "+" if d4 > 0 else "-"
        s5 = "+" if d5 > 0 else "-"
        print(f"  (u0={u0}, h={h}): D2={float(d2):.3e}[{s2}] D3={float(d3):.3e}[{s3}] D4={float(d4):.3e}[{s4}] D5={float(d5):.3e}[{s5}]")

    # Part 3: Why is f_1 not PF_infinity?
    print("\n--- Part 3: Understanding why f_1 is NOT PF_infinity ---")
    print("""
  f_1(u) = [2*pi^2*e^{9u} - 3*pi*e^{5u}] * e^{-pi*e^{4u}}

  Write t = e^u. Then:
    f_1(u) = [2*pi^2*t^9 - 3*pi*t^5] * e^{-pi*t^4}
           = pi*t^5*(2*pi*t^4 - 3) * e^{-pi*t^4}

  Under the substitution s = t^4 = e^{4u}:
    f_1 ~ s^{5/4} * (2*pi*s - 3) * e^{-pi*s}

  This is NOT a PF_infinity function of u because:
  1. e^{-pi*e^{4u}} is NOT a Gaussian in u (it's a Gaussian in e^{4u})
  2. The composition of a PF_infinity function with a convex function
     is NOT generally PF_infinity
  3. The polynomial prefactor pi*t^5*(2*pi*t^4 - 3) adds non-monotone
     behavior that further breaks total positivity

  The key insight: f_1 IS PF_infinity as a function of t = e^u
  (up to a Gaussian factor), but NOT as a function of u itself.
  The coordinate transformation u -> e^u is convex, and convex
  reparametrizations do NOT preserve total positivity.
""")

    # Part 4: The REAL story - adding f_2 HELPS
    print("--- Part 4: Why adding f_2 to f_1 can increase PF order ---")
    print("  At (u0=0.01, h=0.05):")

    for n_max in [1, 2, 3, 5, 50]:
        kfunc = lambda u, nm=n_max: sum(K_fn(u, n) for n in range(1, nm+1))
        d2 = toeplitz_det_func(kfunc, 0.01, 0.05, 2)
        d3 = toeplitz_det_func(kfunc, 0.01, 0.05, 3)
        d4 = toeplitz_det_func(kfunc, 0.01, 0.05, 4)
        d5 = toeplitz_det_func(kfunc, 0.01, 0.05, 5)
        signs = "".join(["+" if d > 0 else "-" for d in [d2, d3, d4, d5]])
        print(f"  N={n_max:>2}: D2={float(d2):>12.4e} D3={float(d3):>12.4e} D4={float(d4):>12.4e} D5={float(d5):>12.4e}  signs={signs}")

    print("""
  CRITICAL OBSERVATION:
  - f_1 alone: D4 < 0, D5 < 0 (NOT PF_4)
  - f_1 + f_2: D4 > 0, D5 < 0 (PF_4 but not PF_5)
  - Full sum:  D4 > 0, D5 < 0 (PF_4 but not PF_5)

  The theta-function sum IMPROVES the total positivity order!
  Individual terms are NOT PF_infinity in the u-variable.
  The SUM has HIGHER PF order than individual terms.

  This is the OPPOSITE of the naive expectation that sums decrease PF order.
  The theta-function structure CONSTRUCTIVELY INTERFERES to boost PF order.
""")

    # Part 5: At what u0 does f_1 become PF_4?
    print("--- Part 5: Where does f_1 alone become PF_4? ---")
    for u0 in [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3]:
        kfunc = lambda u: K_fn(u, 1)
        d4 = toeplitz_det_func(kfunc, u0, 0.05, 4)
        sign = "+" if d4 > 0 else "-"
        print(f"  D4(f_1, u0={u0}, h=0.05) = {float(d4):.6e} [{sign}]")

    # Part 6: The modular correction
    print("\n--- Part 6: The 'modular correction' from f_2 ---")
    print("  The sum Phi = f_1 + f_2 + f_3 + ... is constrained by the")
    print("  Jacobi theta function identity. The correction terms f_n, n>=2,")
    print("  are not arbitrary but follow from the modular symmetry.")
    print("  This modular symmetry is EXACTLY what boosts the PF order from <4 to >=4.")
    print("")

    # Compute the fractional contribution of f_2 to D4 at the critical region
    print("  Fractional contribution of f_2 to D4:")
    for u0 in [0.001, 0.01, 0.02, 0.03]:
        d4_f1 = toeplitz_det_func(lambda u: K_fn(u, 1), u0, 0.05, 4)
        d4_f12 = toeplitz_det_func(lambda u: K_fn(u, 1) + K_fn(u, 2), u0, 0.05, 4)
        d4_all = toeplitz_det_func(lambda u: K_full(u), u0, 0.05, 4)
        # The "f_2 correction" to D4
        delta_d4 = d4_f12 - d4_f1
        print(f"  u0={u0:.3f}: D4(f1)={float(d4_f1):.4e}, D4(f1+f2)={float(d4_f12):.4e}, correction={float(delta_d4):.4e}")
        print(f"           ratio D4(full)/|D4(f1)| = {float(d4_all/abs(d4_f1)):.4f}")

    return

if __name__ == "__main__":
    main()
