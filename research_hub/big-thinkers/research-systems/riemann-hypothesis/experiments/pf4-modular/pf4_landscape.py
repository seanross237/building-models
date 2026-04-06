"""
Compute PF4 and PF5 Toeplitz minors of the de Bruijn-Newman kernel
across a grid of (u0, h) values, to map the landscape of positivity/negativity.

The Polya kernel:
  Phi(u) = sum_{n=1}^{N} [2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}] * e^{-pi*n^2*e^{4u}}

K(u) = Phi(|u|) for all u.
"""

import numpy as np
from mpmath import mp, mpf, matrix, det, pi, exp, fac
import json
import time

# Set high precision
mp.dps = 50  # 50 decimal places

def phi_term(n, u):
    """Single term f_n(u) of the Polya kernel."""
    n = mpf(n)
    u = mpf(u)
    e4u = exp(4*u)
    e5u = exp(5*u)
    e9u = exp(9*u)
    return (2*pi**2*n**4*e9u - 3*pi*n**2*e5u) * exp(-pi*n**2*e4u)

def phi(u, N=50):
    """Polya kernel Phi(u) = sum_{n=1}^{N} f_n(u)."""
    u = mpf(u)
    return sum(phi_term(n, u) for n in range(1, N+1))

def K(u, N=50):
    """de Bruijn-Newman kernel K(u) = Phi(|u|)."""
    return phi(abs(mpf(u)), N)

def toeplitz_minor(u0, h, r, N=50):
    """
    Compute the r x r Toeplitz minor D_r(u0, h).
    Matrix entries: M[i,j] = K(u0 + (i-j)*h) for i,j = 0,...,r-1
    """
    u0 = mpf(u0)
    h = mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = K(u0 + (i-j)*h, N)
    return det(M)

def scan_pf_landscape(u0_values, h_values, max_order=5, N=50):
    """Scan PF minors across (u0, h) grid."""
    results = []
    total = len(u0_values) * len(h_values)
    count = 0

    for u0 in u0_values:
        for h in h_values:
            count += 1
            if count % 10 == 0:
                print(f"  Progress: {count}/{total}")

            row = {'u0': float(u0), 'h': float(h)}
            for r in range(2, max_order+1):
                try:
                    d = toeplitz_minor(u0, h, r, N)
                    row[f'D{r}'] = float(d)
                    row[f'D{r}_sign'] = 1 if d > 0 else (-1 if d < 0 else 0)
                except Exception as e:
                    row[f'D{r}'] = None
                    row[f'D{r}_sign'] = None
            results.append(row)

    return results

def main():
    print("=" * 60)
    print("PF4/PF5 Landscape of the de Bruijn-Newman Kernel")
    print("=" * 60)

    # First: reproduce the paper's counterexample
    print("\n--- Reproducing paper counterexample (u0=0.01, h=0.05) ---")
    for r in range(2, 6):
        t0 = time.time()
        d = toeplitz_minor(0.01, 0.05, r)
        t1 = time.time()
        print(f"  D_{r}(0.01, 0.05) = {d}  [{t1-t0:.1f}s]")

    # Second: scan near the paper's critical region
    print("\n--- Scanning near u0=0, varying h ---")
    u0_near_zero = [0.001, 0.005, 0.01, 0.02, 0.03, 0.031, 0.032, 0.04, 0.05, 0.1, 0.2, 0.5, 1.0]
    h_values = [0.01, 0.02, 0.05, 0.1, 0.2]

    print(f"\nGrid: {len(u0_near_zero)} u0 values x {len(h_values)} h values = {len(u0_near_zero)*len(h_values)} points")
    results = scan_pf_landscape(u0_near_zero, h_values, max_order=5)

    # Print results table
    print("\n--- Results ---")
    print(f"{'u0':>8} {'h':>6} {'D2':>14} {'D3':>14} {'D4':>14} {'D5':>14}")
    print("-" * 80)
    for row in results:
        d2 = f"{row['D2']:.6e}" if row['D2'] is not None else "N/A"
        d3 = f"{row['D3']:.6e}" if row['D3'] is not None else "N/A"
        d4 = f"{row['D4']:.6e}" if row['D4'] is not None else "N/A"
        d5 = f"{row['D5']:.6e}" if row['D5'] is not None else "N/A"
        sign5 = "+" if row.get('D5_sign') == 1 else ("-" if row.get('D5_sign') == -1 else "?")
        print(f"{row['u0']:>8.4f} {row['h']:>6.3f} {d2:>14} {d3:>14} {d4:>14} {d5:>14} [{sign5}]")

    # Count PF5 failures
    failures = [r for r in results if r.get('D5_sign') == -1]
    print(f"\nPF5 failures: {len(failures)} out of {len(results)} configurations")
    for f in failures:
        print(f"  u0={f['u0']:.4f}, h={f['h']:.3f}: D5={f['D5']:.6e}")

    # Check PF4: any failures?
    pf4_failures = [r for r in results if r.get('D4_sign') == -1]
    print(f"\nPF4 failures: {len(pf4_failures)} out of {len(results)} configurations")

    # Third: compute the ratio |D5|/D4 where D5 < 0
    print("\n--- PF5 deficit ratios |D5|/D4 ---")
    for f in failures:
        if f['D4'] is not None and f['D4'] > 0 and f['D5'] is not None:
            ratio = abs(f['D5']) / f['D4']
            print(f"  u0={f['u0']:.4f}, h={f['h']:.3f}: |D5|/D4 = {ratio:.6e}")

    # Save results
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf4-modular/pf_landscape_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")

    # Fourth: scan larger u0 values to confirm PF4 holds far from origin
    print("\n--- Large u0 scan (PF4 only, should all be positive) ---")
    large_u0 = [1.0, 2.0, 3.0, 5.0]
    for u0 in large_u0:
        for h in [0.1, 0.5, 1.0]:
            d4 = toeplitz_minor(u0, h, 4)
            sign = "+" if d4 > 0 else "-"
            print(f"  D4({u0}, {h}) = {float(d4):.6e} [{sign}]")

    return results

if __name__ == "__main__":
    results = main()
