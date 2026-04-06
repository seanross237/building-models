"""
Investigation 1: Fine-grained heat flow analysis for PF5 restoration.

Key question: At what SMALL t does PF5 get restored? Prior work found t ~ 11.4,
but that was at a specific configuration. We check:
1. D5(t) at t = 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0 across multiple configs
2. Whether there's monotonicity in D5 as a function of t
3. The derivative dD5/dt at t=0 (how fast does D5 improve with heat flow?)
4. Whether the heat flow e^{tu^2} preserves PF4 at small t

Also critically: we investigate the CORRECT heat flow. The de Bruijn-Newman
constant uses H_t(x) = integral e^{tu^2} Phi(u) cos(xu) du. The kernel of this
transform is K_t(u) = e^{tu^2} Phi(|u|). The question is whether PF properties
of K_t control zeros of H_t.
"""

from mpmath import mp, mpf, matrix, det, pi, exp, diff, log
import time
import json

mp.dps = 60  # 60 decimal digits

def phi_term(n, u):
    """Single term f_n(u) of the Polya kernel."""
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def phi(u, N=50):
    """Polya kernel Phi(u) = sum f_n(u)."""
    u = mpf(u)
    return sum(phi_term(n, u) for n in range(1, N+1))

def K(u, N=50):
    """K(u) = Phi(|u|)."""
    return phi(abs(mpf(u)), N)

def K_t(u, t, N=50):
    """Heat-deformed kernel K_t(u) = e^{tu^2} Phi(|u|)."""
    u_mpf = mpf(u)
    t_mpf = mpf(t)
    return exp(t_mpf * u_mpf**2) * K(u, N)

def toeplitz_det(kfunc, u0, h, r):
    """r x r Toeplitz determinant with kernel function kfunc."""
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)

def main():
    print("=" * 70)
    print("Investigation 1: Fine-Grained Heat Flow Analysis")
    print("=" * 70)

    configs = [
        (0.001, 0.01),
        (0.001, 0.05),
        (0.01, 0.01),
        (0.01, 0.05),
        (0.02, 0.03),
        (0.02, 0.05),
        (0.03, 0.02),
        (0.03, 0.035),
    ]

    # Fine grid of t values focused on small t
    t_values = [0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]

    results = {}

    # Part 1: D5(t) at fine t grid across configurations
    print("\n--- Part 1: D5(t) at fine t grid ---")
    print(f"{'config':>16} | " + " | ".join(f"t={t:.4f}" for t in t_values[:8]))

    for u0, h in configs:
        key = f"({u0},{h})"
        row = []
        for t in t_values:
            t0 = time.time()
            kfunc = lambda u, tv=mpf(t): K_t(u, tv)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            t1 = time.time()
            row.append(float(d5))
        results[key] = {'t_values': [float(t) for t in t_values], 'D5': row}

        # Print first 8 values
        signs = ["+" if v > 0 else "-" for v in row[:8]]
        print(f"  ({u0:.3f},{h:.3f}) | " + " | ".join(
            f"{row[i]:.2e}[{signs[i]}]" for i in range(min(8, len(row)))
        ))

    # Part 2: Also track D4(t) to see if PF4 is preserved
    print("\n--- Part 2: D4(t) — checking PF4 preservation ---")
    for u0, h in configs[:4]:
        key = f"({u0},{h})"
        print(f"\n  Config ({u0}, {h}):")
        for t in t_values:
            kfunc = lambda u, tv=mpf(t): K_t(u, tv)
            d4 = toeplitz_det(kfunc, u0, h, 4)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            s4 = "+" if d4 > 0 else "-"
            s5 = "+" if d5 > 0 else "-"
            print(f"    t={t:>8.4f}: D4={float(d4):>12.4e}[{s4}]  D5={float(d5):>12.4e}[{s5}]")
            results[key + f'_D4_t{t}'] = float(d4)

    # Part 3: Rate of change dD5/dt at t=0
    print("\n--- Part 3: Derivative dD5/dt at t=0 (finite differences) ---")
    for u0, h in configs:
        # D5 at t=0 and t=epsilon
        eps = mpf('0.0001')
        d5_0 = toeplitz_det(lambda u: K_t(u, 0), u0, h, 5)
        d5_eps = toeplitz_det(lambda u: K_t(u, eps), u0, h, 5)
        deriv = (d5_eps - d5_0) / eps
        print(f"  ({u0:.3f},{h:.3f}): D5(0) = {float(d5_0):>12.4e}, dD5/dt|_0 = {float(deriv):>12.4e}, ratio = {float(deriv/d5_0) if d5_0 != 0 else 'inf':>12.4e}")
        results[f"({u0},{h})_deriv"] = float(deriv)

    # Part 4: The critical question — does |D5| decrease monotonically with t?
    print("\n--- Part 4: Monotonicity check — is D5(t) monotonically increasing? ---")
    for u0, h in [(0.01, 0.05), (0.001, 0.05)]:
        print(f"\n  Config ({u0}, {h}):")
        t_fine = [mpf(k) / 100 for k in range(0, 201, 5)]  # t from 0 to 2.0 in steps of 0.05
        prev_d5 = None
        monotone = True
        for t in t_fine:
            d5 = toeplitz_det(lambda u, tv=t: K_t(u, tv), u0, h, 5)
            if prev_d5 is not None and d5 < prev_d5:
                monotone = False
            if float(t) in [0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]:
                print(f"    t={float(t):>5.2f}: D5 = {float(d5):>14.6e}")
            prev_d5 = d5
        print(f"    Monotonically increasing on [0, 2]: {monotone}")

    # Part 5: Find the MINIMUM t where D5 >= 0 via bisection at the worst config
    print("\n--- Part 5: Minimum t for D5 >= 0 at worst configs ---")
    for u0, h in [(0.001, 0.05), (0.01, 0.05), (0.001, 0.01)]:
        # First check if D5(t=0) < 0
        d5_0 = toeplitz_det(lambda u: K(u), u0, h, 5)
        if d5_0 >= 0:
            print(f"  ({u0}, {h}): D5 already >= 0 at t=0")
            continue

        # Find upper bound
        t_hi = mpf(20)
        d5_hi = toeplitz_det(lambda u: K_t(u, t_hi), u0, h, 5)
        while d5_hi < 0:
            t_hi *= 2
            d5_hi = toeplitz_det(lambda u: K_t(u, t_hi), u0, h, 5)

        # Bisect
        t_lo = mpf(0)
        for _ in range(60):
            t_mid = (t_lo + t_hi) / 2
            d5_mid = toeplitz_det(lambda u: K_t(u, t_mid), u0, h, 5)
            if d5_mid < 0:
                t_lo = t_mid
            else:
                t_hi = t_mid
        t_crit = float((t_lo + t_hi) / 2)
        print(f"  ({u0}, {h}): D5 crosses zero at t = {t_crit:.10f}")
        results[f"({u0},{h})_t_crit_D5"] = t_crit

    # Save results
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf5-perturbation/inv1_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")

if __name__ == "__main__":
    main()
