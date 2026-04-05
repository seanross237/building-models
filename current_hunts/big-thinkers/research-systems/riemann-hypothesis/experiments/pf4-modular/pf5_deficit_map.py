"""
Detailed map of the PF5 deficit boundary.
Where exactly does D5 change sign? What is the shape of the boundary in (u0, h) space?
Also: investigate the leading coefficient C5(u0) and find u0* more precisely.
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, diff, taylor, fac, log
import time
import json

mp.dps = 60

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
    """K(u) = Phi(|u|)."""
    return phi(abs(mpf(u)), N)

def toeplitz_det(u0, h, r, N=50):
    """r x r Toeplitz determinant."""
    u0 = mpf(u0)
    h = mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = K(u0 + (i-j)*h, N)
    return det(M)

def find_h_boundary(u0, r=5, h_low=0.001, h_high=0.5, tol=1e-12, N=50):
    """
    For fixed u0, find the critical h where D_r changes sign.
    Assumes D_r < 0 for small h and D_r > 0 for large h.
    """
    u0 = mpf(u0)
    d_low = toeplitz_det(u0, h_low, r, N)
    d_high = toeplitz_det(u0, h_high, r, N)

    if d_low >= 0:
        return None  # Already positive at small h
    if d_high < 0:
        return None  # Still negative at large h

    while h_high - h_low > tol:
        h_mid = (h_low + h_high) / 2
        d_mid = toeplitz_det(u0, h_mid, r, N)
        if d_mid < 0:
            h_low = h_mid
        else:
            h_high = h_mid

    return float((h_low + h_high) / 2)

def compute_C5_leading(u0, N=50):
    """
    Compute the leading coefficient C5(u0) = lim_{h->0} D5(u0,h) / h^{5*4}.
    We estimate this numerically by computing D5 at very small h and dividing by h^20.
    """
    u0 = mpf(u0)
    # Use several small h values and extrapolate
    results = []
    for h_exp in range(-4, -1):
        h = mpf(10)**h_exp
        d5 = toeplitz_det(u0, h, 5, N)
        c5_est = d5 / h**20
        results.append((float(h), float(c5_est)))
    return results

def main():
    print("=" * 60)
    print("PF5 Deficit Detailed Map")
    print("=" * 60)

    # Part 1: Find the h-boundary for several u0 values
    print("\n--- Part 1: Critical h where D5 changes sign ---")
    u0_values = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.031, 0.0315]

    boundaries = {}
    for u0 in u0_values:
        t0 = time.time()
        h_crit = find_h_boundary(u0, r=5, h_low=0.001, h_high=0.3, tol=1e-6)
        t1 = time.time()
        if h_crit is not None:
            boundaries[u0] = h_crit
            print(f"  u0={u0:.4f}: h_crit = {h_crit:.6f}  [{t1-t0:.1f}s]")
        else:
            print(f"  u0={u0:.4f}: No sign change found  [{t1-t0:.1f}s]")

    # Part 2: Estimate C5(u0) at several points to find u0*
    print("\n--- Part 2: Leading coefficient C5(u0) estimation ---")
    print("  (Estimating C5 = D5/h^20 at small h values)")

    u0_fine = [0.001, 0.005, 0.01, 0.02, 0.025, 0.03, 0.031, 0.0311, 0.0312, 0.0315, 0.032, 0.035, 0.04, 0.05]

    c5_estimates = {}
    for u0 in u0_fine:
        t0 = time.time()
        # Use h = 10^-3 for the estimate (small enough to be in leading-term regime)
        h = mpf('0.001')
        d5 = toeplitz_det(u0, h, 5)
        c5 = d5 / h**20
        t1 = time.time()
        c5_float = float(c5)
        c5_estimates[u0] = c5_float
        sign = "+" if c5 > 0 else "-"
        print(f"  u0={u0:.4f}: C5 ~ {c5_float:.6e} [{sign}]  [{t1-t0:.1f}s]")

    # Part 3: Bisect to find u0* more precisely
    print("\n--- Part 3: Bisecting for u0* where C5 changes sign ---")
    u0_low = mpf('0.031')
    u0_high = mpf('0.032')

    # Verify signs
    h_test = mpf('0.001')
    d5_low = toeplitz_det(u0_low, h_test, 5)
    d5_high = toeplitz_det(u0_high, h_test, 5)
    print(f"  D5 at u0={float(u0_low)}: {float(d5_low):.6e} ({'<0' if d5_low < 0 else '>0'})")
    print(f"  D5 at u0={float(u0_high)}: {float(d5_high):.6e} ({'<0' if d5_high < 0 else '>0'})")

    if d5_low < 0 and d5_high > 0:
        for _ in range(40):  # ~12 digits of precision
            u0_mid = (u0_low + u0_high) / 2
            d5_mid = toeplitz_det(u0_mid, h_test, 5)
            if d5_mid < 0:
                u0_low = u0_mid
            else:
                u0_high = u0_mid
        u0_star = float((u0_low + u0_high) / 2)
        print(f"\n  u0* = {u0_star:.15f}")
        print(f"  (Paper value: 0.031139763615...)")
    else:
        print("  Sign change not bracketed, adjusting...")
        # Try a finer grid
        for u0_try in [0.0310, 0.0311, 0.0312, 0.0313, 0.0314, 0.0315]:
            d5 = toeplitz_det(mpf(u0_try), h_test, 5)
            print(f"    u0={u0_try}: D5={float(d5):.6e}")

    # Part 4: Compute the "almost PF5" metric
    print("\n--- Part 4: The 'Almost PF5' Metric ---")
    print("  At the worst-case configuration (u0=0.001, h=0.05):")

    u0_worst = mpf('0.001')
    h_worst = mpf('0.05')

    d2 = toeplitz_det(u0_worst, h_worst, 2)
    d3 = toeplitz_det(u0_worst, h_worst, 3)
    d4 = toeplitz_det(u0_worst, h_worst, 4)
    d5 = toeplitz_det(u0_worst, h_worst, 5)

    print(f"  D2 = {float(d2):.10e}")
    print(f"  D3 = {float(d3):.10e}")
    print(f"  D4 = {float(d4):.10e}")
    print(f"  D5 = {float(d5):.10e}")
    print(f"  |D5|/D4 = {float(abs(d5)/d4):.10e}")
    print(f"  |D5|/D3 = {float(abs(d5)/d3):.10e}")
    print(f"  |D5|/D2 = {float(abs(d5)/d2):.10e}")

    # The decay pattern
    print(f"\n  Decay ratios:")
    print(f"  D3/D2 = {float(d3/d2):.6e}")
    print(f"  D4/D3 = {float(d4/d3):.6e}")
    print(f"  |D5|/D4 = {float(abs(d5)/d4):.6e}")
    print(f"  If PF5 held with the same ratio: D5_expected ~ D4 * (D4/D3) = {float(d4 * d4/d3):.6e}")
    print(f"  Actual |D5| / D5_expected = {float(abs(d5) / (d4 * d4/d3)):.6e}")

    # Save all results
    results = {
        'boundaries': boundaries,
        'c5_estimates': c5_estimates,
        'u0_star_estimate': u0_star if 'u0_star' in dir() else None,
    }
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf4-modular/pf5_deficit_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")

if __name__ == "__main__":
    main()
