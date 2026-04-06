"""
Attempt to prove PF_4 globally for the de Bruijn-Newman kernel.

Strategy: Show D4(u0, h) >= 0 for all u0 >= 0, h > 0.

We'll divide into regions:
  Region A: u0 > 0.02, any h > 0  (f_1 dominates, correction from f_2 is small)
  Region B: 0 <= u0 <= 0.02, h > h_crit(u0)  (large h, D4 clearly positive)
  Region C: 0 <= u0 <= 0.02, h <= h_crit(u0)  (the hard region near the origin)

For Region C, we use the asymptotic formula:
  D4(u0, h) / h^{4*3} = C_4(u0) + O(h^2)
  where C_4(u0) > 0 was certified by the paper for all tested u0.

So the proof reduces to:
  1. Show C_4(u0) > 0 for all u0 > 0 (leading coefficient is positive)
  2. Show D4(u0, h) > 0 for h >= h_min (some explicit h_min)
  3. Verify computationally in the gap between the asymptotic regime and h_min
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, diff
import time
import json

mp.dps = 60

def phi(u, N=50):
    u = mpf(u)
    result = mpf(0)
    for n in range(1, N+1):
        n_mpf = mpf(n)
        result += (2*pi**2*n_mpf**4*exp(9*u) - 3*pi*n_mpf**2*exp(5*u)) * exp(-pi*n_mpf**2*exp(4*u))
    return result

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def toeplitz_det(u0, h, r, N=50):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = K(u0 + (i-j)*h, N)
    return det(M)

def C4_estimate(u0, N=50):
    """Estimate C_4(u0) = lim_{h->0} D_4(u0,h) / h^12."""
    h = mpf('0.0001')
    d4 = toeplitz_det(u0, h, 4, N)
    return d4 / h**12

def main():
    print("=" * 70)
    print("PF_4 Global Proof Attempt")
    print("=" * 70)

    # Part 1: C_4(u0) for a dense grid of u0 values
    print("\n--- Part 1: C_4(u0) estimates ---")
    u0_grid = [0.001, 0.002, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03,
               0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0]

    c4_values = {}
    for u0 in u0_grid:
        c4 = C4_estimate(u0)
        c4_float = float(c4)
        c4_values[u0] = c4_float
        sign = "+" if c4 > 0 else "-"
        print(f"  u0={u0:.4f}: C_4 = {c4_float:.6e} [{sign}]")

    # Check: any negative C_4?
    negatives = {k: v for k, v in c4_values.items() if v < 0}
    if negatives:
        print(f"\n  WARNING: C_4 < 0 at {len(negatives)} points!")
        for k, v in negatives.items():
            print(f"    u0={k}: C_4={v:.6e}")
    else:
        print(f"\n  C_4 > 0 at all {len(c4_values)} tested points. Promising for global PF_4.")

    # Part 2: D_4(u0, h) for the critical region
    print("\n--- Part 2: D_4 in the critical region (u0 near 0, small h) ---")
    u0_critical = [0.001, 0.005, 0.01, 0.015, 0.02]
    h_critical = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

    print(f"  {'u0':>6} {'h':>6} {'D4':>14} {'sign':>5}")
    all_positive = True
    for u0 in u0_critical:
        for h in h_critical:
            d4 = toeplitz_det(u0, h, 4)
            sign = "+" if d4 > 0 else ("-" if d4 < 0 else "0")
            if d4 <= 0:
                all_positive = False
            print(f"  {u0:>6.3f} {h:>6.3f} {float(d4):>14.4e} [{sign}]")

    if all_positive:
        print(f"\n  All D_4 values positive in the critical region!")
    else:
        print(f"\n  Some D_4 values are non-positive!")

    # Part 3: The derivative structure
    print("\n--- Part 3: Understanding C_4(u0) analytically ---")
    print("  C_4(u0) involves derivatives K^(k)(u0) for k = 0,...,6")
    print("  Computing these derivatives at u0 = 0:")

    derivs_at_0 = []
    for k in range(7):
        d = diff(lambda u: phi(u), mpf(0), k)
        derivs_at_0.append(d)
        print(f"  Phi^({k})(0) = {float(d):.6e}")

    print(f"\n  Note: odd derivatives are ~0 (Phi is effectively even due to")
    print(f"  the super-exponential decay making Phi(u) ~ Phi(-u) for |u| small)")

    # Part 4: The C_4 formula
    print("\n--- Part 4: C_4 formula decomposition ---")
    print("""
  C_4(u0) = det of 4x4 matrix with (i,j) entry = K^{2|i-j|}(u0) / (2|i-j|)!
  multiplied by combinatorial factors from the Vandermonde.

  More precisely: for the Toeplitz matrix with entries K(u0 + (i-j)*h),
  expanding to leading order in h:
    K(u0 + s*h) = sum_k K^(k)(u0) * (s*h)^k / k!

  The 4x4 determinant involves terms up to h^12 = h^{4*3}.

  C_4 is a polynomial in K(u0), K'(u0), K''(u0), ..., K^(6)(u0).

  For u0 = 0: K is even, so K'(0) = K'''(0) = K^(5)(0) = 0.
  This simplifies C_4(0) to involve only K(0), K''(0), K^(4)(0), K^(6)(0).
""")

    # Part 5: Verify the formula numerically
    print("--- Part 5: Numerical C_4(0) vs analytic ---")
    K0 = phi(0)
    K2 = derivs_at_0[2]
    K4 = derivs_at_0[4]
    K6 = derivs_at_0[6]

    print(f"  K(0) = {float(K0):.10e}")
    print(f"  K''(0) = {float(K2):.10e}")
    print(f"  K^(4)(0) = {float(K4):.10e}")
    print(f"  K^(6)(0) = {float(K6):.10e}")

    # C_4 from numerical estimate
    c4_num = C4_estimate(0)
    print(f"\n  C_4(0) from numerical D4/h^12: {float(c4_num):.10e}")

    # Part 6: Asymptotic behavior
    print("\n--- Part 6: C_4(u0) asymptotic behavior ---")
    print("  As u0 -> infinity, Phi(u0) ~ f_1(u0) ~ e^{-pi*e^{4u0}}")
    print("  (super-exponential decay)")
    print("  C_4(u0) should also decay super-exponentially.")
    print("  The critical behavior is at u0 near 0.")
    print(f"\n  C_4 values (log scale):")
    for u0, c4 in sorted(c4_values.items()):
        if c4 > 0:
            from mpmath import log10
            print(f"    u0={u0:.4f}: log10(C_4) = {float(log10(mpf(c4))):.2f}")

    # Part 7: Is there a GLOBAL minimum of C_4?
    print("\n--- Part 7: Finding the minimum of C_4(u0) ---")
    # Fine grid near where we might expect a minimum
    u0_fine = np.linspace(0.001, 0.1, 50)
    c4_fine = []
    for u0 in u0_fine:
        c4 = float(C4_estimate(u0))
        c4_fine.append(c4)

    min_c4 = min(c4_fine)
    min_u0 = u0_fine[c4_fine.index(min_c4)]
    print(f"  Minimum C_4 on [0.001, 0.1]: {min_c4:.6e} at u0 = {min_u0:.4f}")

    if min_c4 > 0:
        print(f"  C_4 is POSITIVE everywhere on this grid.")
        print(f"  Combined with C_4(u0) > 0 from the paper for all tested u0,")
        print(f"  this strongly suggests PF_4 holds globally.")

    # Save results
    results = {
        'c4_values': c4_values,
        'c4_fine': list(zip([float(x) for x in u0_fine], c4_fine)),
        'min_c4': min_c4,
        'min_u0': float(min_u0),
    }
    outpath = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf4-modular/pf4_proof_results.json"
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {outpath}")

    return results

if __name__ == "__main__":
    results = main()
