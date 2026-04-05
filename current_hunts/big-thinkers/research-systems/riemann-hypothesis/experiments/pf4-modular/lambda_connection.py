"""
Investigate the connection between the PF5 deficit and the de Bruijn-Newman constant Lambda.

Key question: The Gaussian deformation K_t(u) = e^{tu^2} * Phi(|u|) generates a family
of kernels. At t = Lambda, the Fourier transform H_t has only real zeros (RH for H_t).
At t = 0, H_0 = Xi (the Riemann xi-function), and RH <=> Lambda <= 0.

The paper shows that PF5 fails at t=0 but is restored at configuration-dependent
thresholds lambda_5*. These are NOT Lambda, but they measure "how far from PF5"
the kernel is at each configuration.

Can we relate the PF5 deficit to Lambda?

Also: The deformation K_t(u) = e^{tu^2} * K(u). What happens to the PF order
as t varies from 0 upward?
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, sqrt
import time

mp.dps = 50

def phi(u, N=50):
    u = mpf(u)
    result = mpf(0)
    for n in range(1, N+1):
        n_mpf = mpf(n)
        result += (2*pi**2*n_mpf**4*exp(9*u) - 3*pi*n_mpf**2*exp(5*u)) * exp(-pi*n_mpf**2*exp(4*u))
    return result

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def K_t(u, t, N=50):
    """Gaussian-deformed kernel K_t(u) = e^{t*u^2} * Phi(|u|)."""
    u_mpf = mpf(u)
    t_mpf = mpf(t)
    return exp(t_mpf * u_mpf**2) * K(u, N)

def toeplitz_det_func(kfunc, u0, h, r):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)

def main():
    print("=" * 70)
    print("Connection to the de Bruijn-Newman Constant Lambda")
    print("=" * 70)

    # Part 1: PF order as function of t at the counterexample
    print("\n--- Part 1: PF order of K_t at (u0=0.01, h=0.05) ---")
    u0, h = 0.01, 0.05
    t_values = [0, 0.5, 1, 2, 5, 10, 11, 11.5, 12, 15, 20]

    print(f"  {'t':>6} {'D4':>14} {'D5':>14} {'D6':>14}")
    for t in t_values:
        kfunc = lambda u, tv=t: K_t(u, tv)
        d4 = toeplitz_det_func(kfunc, u0, h, 4)
        d5 = toeplitz_det_func(kfunc, u0, h, 5)
        d6 = toeplitz_det_func(kfunc, u0, h, 6)
        s4 = "+" if d4 > 0 else "-"
        s5 = "+" if d5 > 0 else "-"
        s6 = "+" if d6 > 0 else "-"
        print(f"  {t:>6.1f} {float(d4):>14.4e}[{s4}] {float(d5):>14.4e}[{s5}] {float(d6):>14.4e}[{s6}]")

    # Part 2: Find the t where D5 changes sign (lambda_5*)
    print("\n--- Part 2: Finding lambda_5* at (u0=0.01, h=0.05) ---")
    t_low, t_high = mpf(0), mpf(20)
    for _ in range(50):
        t_mid = (t_low + t_high) / 2
        kfunc = lambda u, tv=t_mid: K_t(u, float(tv))
        d5 = toeplitz_det_func(kfunc, u0, h, 5)
        if d5 < 0:
            t_low = t_mid
        else:
            t_high = t_mid
    lambda_5_star = float((t_low + t_high) / 2)
    print(f"  lambda_5* = {lambda_5_star:.6f}")
    print(f"  (Paper value: ~11.43)")

    # Part 3: lambda_5* at different configurations
    print("\n--- Part 3: lambda_5* at different configurations ---")
    configs = [
        (0.001, 0.01),
        (0.001, 0.05),
        (0.01, 0.01),
        (0.01, 0.05),
        (0.02, 0.05),
        (0.03, 0.02),
    ]

    for u0_test, h_test in configs:
        # Check if D5 is negative at t=0
        d5_0 = toeplitz_det_func(lambda u: K_t(u, 0), u0_test, h_test, 5)
        if d5_0 >= 0:
            print(f"  (u0={u0_test}, h={h_test}): D5(t=0) > 0, PF5 already holds")
            continue

        t_low, t_high = mpf(0), mpf(50)
        # First find an upper bound where D5 > 0
        d5_high = toeplitz_det_func(lambda u: K_t(u, float(t_high)), u0_test, h_test, 5)
        while d5_high < 0:
            t_high *= 2
            d5_high = toeplitz_det_func(lambda u: K_t(u, float(t_high)), u0_test, h_test, 5)

        for _ in range(40):
            t_mid = (t_low + t_high) / 2
            d5 = toeplitz_det_func(lambda u: K_t(u, float(t_mid)), u0_test, h_test, 5)
            if d5 < 0:
                t_low = t_mid
            else:
                t_high = t_mid
        lambda5 = float((t_low + t_high) / 2)
        print(f"  (u0={u0_test}, h={h_test}): lambda_5* = {lambda5:.4f}")

    # Part 4: The key conceptual analysis
    print("\n--- Part 4: Conceptual Analysis ---")
    print("""
  The de Bruijn-Newman constant Lambda is defined by:
    Lambda = inf{t : H_t has all real zeros}

  where H_t(x) = integral_{-inf}^{inf} e^{tu^2} * Phi(u) * cos(xu) du.

  Key facts:
  - Lambda >= 0 (Rodgers-Tao 2018)
  - Lambda <= 0.2 (Platt-Trudgian 2020)
  - RH <=> Lambda = 0

  The PF order of K_t controls a SUFFICIENT condition:
  - K_t in PF_infinity => H_t has all real zeros => t >= Lambda

  But we know:
  - K_0 is NOT PF_infinity (fails PF_5)
  - K_0 IS (apparently) PF_4

  The question is: does PF_4 + structure give ENOUGH for real zeros?

  IMPORTANT DISTINCTION:
  - PF_infinity => real zeros (Schoenberg's theorem)
  - PF_k for any finite k does NOT generically imply real zeros
  - The gap between PF_4 and PF_infinity is qualitative, not quantitative

  However, PF_4 of a SPECIFIC kernel (with modular structure) might
  constrain the zeros more than PF_4 of a generic kernel.

  THE KEY QUESTION: Is there a value t_crit such that:
  - K_t is PF_infinity for t > t_crit
  - K_t is PF_4 (but not PF_5) for 0 <= t < t_crit

  If so, what is t_crit? And is Lambda related to t_crit?
""")

    # Part 5: Check if K_t becomes PF_infinity for large t
    print("\n--- Part 5: Does K_t become PF_infinity for large t? ---")
    print("  Testing at (u0=0.01, h=0.05) for large t:")
    for t in [50, 100, 200, 500]:
        kfunc = lambda u, tv=t: K_t(u, tv)
        signs = []
        for r in range(2, 8):
            d = toeplitz_det_func(kfunc, u0, h, r)
            signs.append("+" if d > 0 else ("-" if d < 0 else "0"))
        print(f"  t={t}: D2..D7 signs = {''.join(signs)}")

    # Part 6: The "barely failing PF_5" observation
    print("\n--- Part 6: How close is the theta sum to PF_5? ---")
    print("  We showed that alpha=1, beta=1.5 restores PF_5 at (0.01, 0.05).")
    print("  The theta sum has alpha=beta=1. How much 'extra f_2' is needed?")
    print("")

    # Binary search for the minimum beta that restores PF5
    u0, h = 0.01, 0.05
    beta_low, beta_high = mpf(1), mpf(2)
    for _ in range(50):
        beta_mid = (beta_low + beta_high) / 2
        kfunc = lambda u, b=float(beta_mid): f_n_func(1, abs(mpf(u))) + b * f_n_func(2, abs(mpf(u))) + sum(f_n_func(n, abs(mpf(u))) for n in range(3, 51))
        # Simplified: just f_1 + beta*f_2
        kfunc2 = lambda u, b=float(beta_mid): phi_weighted(u, b)
        d5 = toeplitz_det_func(kfunc2, u0, h, 5)
        if d5 < 0:
            beta_low = beta_mid
        else:
            beta_high = beta_mid

    print(f"  Minimum beta (weight of f_2) for PF_5: {float((beta_low+beta_high)/2):.6f}")
    print(f"  Theta sum has beta = 1.0")
    print(f"  Shortfall: {float((beta_low+beta_high)/2 - 1):.6f} = {float(((beta_low+beta_high)/2 - 1)*100):.2f}%")

    return

def f_n_func(n, u):
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def phi_weighted(u, beta_2, N=50):
    """Phi with modified weight for the n=2 term."""
    u_abs = abs(mpf(u))
    result = f_n_func(1, u_abs)
    result += mpf(beta_2) * f_n_func(2, u_abs)
    for n in range(3, N+1):
        result += f_n_func(n, u_abs)
    return result

if __name__ == "__main__":
    main()
