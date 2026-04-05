"""
Investigate the theta function structure of Phi and how it relates to PF order.

Key questions:
1. Each term f_n is individually PF_infinity. How much does f_1 dominate the
   Toeplitz minors?
2. Can we bound the cross-terms between f_1 and f_n (n>=2) to prove PF_4?
3. What is the "effective number of terms" at each u0 value?
4. Is the PF5 failure caused by the interference pattern of theta-function terms?
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp
import time

mp.dps = 50

def phi_term(n, u):
    """Single term f_n(u) of the Polya kernel."""
    n = mpf(n)
    u = mpf(u)
    e4u = exp(4*u)
    e5u = exp(5*u)
    e9u = exp(9*u)
    return (2*pi**2*n**4*e9u - 3*pi*n**2*e5u) * exp(-pi*n**2*e4u)

def phi(u, N=50):
    return sum(phi_term(n, u) for n in range(1, N+1))

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def K_partial(u, n_max):
    """K using only first n_max terms."""
    return sum(phi_term(n, abs(mpf(u))) for n in range(1, n_max+1))

def toeplitz_det_func(kernel_func, u0, h, r):
    """Toeplitz determinant using a given kernel function."""
    u0 = mpf(u0)
    h = mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kernel_func(u0 + (i-j)*h)
    return det(M)

def main():
    print("=" * 70)
    print("Theta Function Decomposition Analysis")
    print("=" * 70)

    # Part 1: Term magnitudes at the counterexample point
    print("\n--- Part 1: Term magnitudes at the counterexample ---")
    u0 = 0.01
    h = 0.05
    eval_points = [u0 + k*h for k in range(-4, 5)]

    print(f"  Evaluation points: {eval_points}")
    print(f"\n  Term contributions |f_n(u)| at key points:")
    print(f"  {'n':>3} {'f_n(0.01)':>16} {'f_n(0.21)':>16} {'ratio f2/f1':>16}")

    f1_vals = {}
    for u in eval_points:
        f1_vals[u] = float(phi_term(1, u))

    for n in range(1, 8):
        fn_01 = phi_term(n, 0.01)
        fn_21 = phi_term(n, 0.21)
        if n > 1:
            r1 = fn_01 / phi_term(1, 0.01)
            r2 = fn_21 / phi_term(1, 0.21)
            print(f"  {n:>3} {float(fn_01):>16.6e} {float(fn_21):>16.6e} {float(r1):>16.6e}")
        else:
            print(f"  {n:>3} {float(fn_01):>16.6e} {float(fn_21):>16.6e} {'---':>16}")

    # Part 2: How many terms needed for D4 and D5?
    print("\n--- Part 2: Toeplitz minors with truncated sums ---")
    print(f"  Configuration: u0={u0}, h={h}")

    for n_max in [1, 2, 3, 5, 10, 50]:
        kernel = lambda u, nm=n_max: K_partial(u, nm)
        d4 = toeplitz_det_func(kernel, u0, h, 4)
        d5 = toeplitz_det_func(kernel, u0, h, 5)
        sign4 = "+" if d4 > 0 else "-"
        sign5 = "+" if d5 > 0 else "-"
        print(f"  N={n_max:>2}: D4 = {float(d4):>14.6e} [{sign4}]  D5 = {float(d5):>14.6e} [{sign5}]")

    # Part 3: D5 for f_1 alone vs full kernel
    print("\n--- Part 3: f_1 alone is PF_infinity, so D5(f_1) >= 0 ---")
    kernel_f1 = lambda u: phi_term(1, abs(mpf(u)))
    d5_f1 = toeplitz_det_func(kernel_f1, u0, h, 5)
    d5_full = toeplitz_det_func(lambda u: K(u), u0, h, 5)
    print(f"  D5(f_1 only) = {float(d5_f1):.10e}")
    print(f"  D5(full)     = {float(d5_full):.10e}")
    print(f"  D5(full) - D5(f1) = {float(d5_full - d5_f1):.10e}")
    print(f"  Ratio: D5(full)/D5(f1) = {float(d5_full/d5_f1):.10e}")

    # Part 4: What does f_2 contribute?
    print("\n--- Part 4: Contribution of f_2 to D5 ---")
    kernel_f12 = lambda u: K_partial(u, 2)
    d5_f12 = toeplitz_det_func(kernel_f12, u0, h, 5)
    print(f"  D5(f1+f2) = {float(d5_f12):.10e}")
    print(f"  D5(f1)    = {float(d5_f1):.10e}")
    print(f"  D5(f1+f2) - D5(f1) = {float(d5_f12 - d5_f1):.10e}")
    print(f"  The perturbation from f_2 is: {float((d5_f12-d5_f1)/d5_f1*100):.4f}% of D5(f1)")

    # Part 5: For D4, same analysis
    print("\n--- Part 5: D4 decomposition ---")
    d4_f1 = toeplitz_det_func(kernel_f1, u0, h, 4)
    d4_f12 = toeplitz_det_func(kernel_f12, u0, h, 4)
    d4_full = toeplitz_det_func(lambda u: K(u), u0, h, 4)
    print(f"  D4(f1)      = {float(d4_f1):.10e}")
    print(f"  D4(f1+f2)   = {float(d4_f12):.10e}")
    print(f"  D4(full)    = {float(d4_full):.10e}")
    print(f"  D4(f1+f2)/D4(f1) = {float(d4_f12/d4_f1):.10f}")
    print(f"  D4(full)/D4(f1)  = {float(d4_full/d4_f1):.10f}")

    # Part 6: Scan over multiple configurations
    print("\n--- Part 6: PF5 sign for f_1 alone at various (u0, h) ---")
    print("  (f_1 alone is PF_infinity, so all D5 must be >= 0)")
    configs = [(0.001, 0.01), (0.001, 0.05), (0.01, 0.05), (0.03, 0.05),
               (0.05, 0.1), (0.1, 0.1), (0.2, 0.2)]
    for u0_test, h_test in configs:
        d5_single = toeplitz_det_func(kernel_f1, u0_test, h_test, 5)
        d5_all = toeplitz_det_func(lambda u: K(u), u0_test, h_test, 5)
        print(f"  u0={u0_test:.3f}, h={h_test:.2f}: D5(f1)={float(d5_single):.6e}  D5(all)={float(d5_all):.6e}  ratio={float(d5_all/d5_single):.6e}")

    # Part 7: At what u0 does f_2 become negligible for PF5?
    print("\n--- Part 7: f_2/f_1 ratio at various u0 ---")
    print("  (The ratio f_2(u)/f_1(u) controls when higher terms become negligible)")
    for u in [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
        f1 = phi_term(1, u)
        f2 = phi_term(2, u)
        if f1 != 0:
            ratio = f2/f1
            print(f"  u={u:.2f}: f_2/f_1 = {float(ratio):.10e}")
        else:
            print(f"  u={u:.2f}: f_1 = 0")

    return

if __name__ == "__main__":
    main()
