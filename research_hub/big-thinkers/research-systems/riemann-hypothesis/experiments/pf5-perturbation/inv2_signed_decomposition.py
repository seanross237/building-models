"""
Investigation 2: Signed Toeplitz minor decomposition.

Decompose D5 into contributions from individual theta-function terms.
The 5x5 Toeplitz matrix T5 with entries K(u0 + (i-j)*h) can be written as:
  T5 = T5(f1) + T5(f2) + cross terms

where T5(fn) uses only the n-th term of the theta sum.

Since det is not linear in the matrix entries, we use:
  K = f1 + f2 + f3 + ...

and the Toeplitz matrix entries become sums of the individual fn evaluations.
The determinant of a sum of matrices is complex, but we can track how D5
changes as we add terms.

Key questions:
1. How does D5 change as we include f1, f1+f2, f1+f2+f3, ...?
2. Which term's inclusion makes D5 most negative vs. positive?
3. Can we identify the specific cross-terms responsible for D5 < 0?
"""

from mpmath import mp, mpf, matrix, det, pi, exp
import time
import json

mp.dps = 60

def phi_term(n, u):
    """Single term f_n(u) of the Polya kernel."""
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def K_partial(u, terms):
    """Partial kernel using only specified terms."""
    u_abs = abs(mpf(u))
    return sum(phi_term(n, u_abs) for n in terms)

def toeplitz_matrix(kfunc, u0, h, r):
    """Build the r x r Toeplitz matrix."""
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return M

def toeplitz_det(kfunc, u0, h, r):
    """r x r Toeplitz determinant."""
    return det(toeplitz_matrix(kfunc, u0, h, r))

def main():
    print("=" * 70)
    print("Investigation 2: Signed Toeplitz Minor Decomposition")
    print("=" * 70)

    configs = [
        (0.001, 0.05, "worst |D5|/D4"),
        (0.01, 0.05, "paper counterexample"),
        (0.001, 0.01, "small h"),
        (0.02, 0.05, "near boundary"),
        (0.03, 0.035, "edge of failure region"),
    ]

    results = {}

    # Part 1: D5 as terms are accumulated
    print("\n--- Part 1: Cumulative D5 as theta terms are added ---")
    for u0, h, label in configs:
        print(f"\n  Config ({u0}, {h}) - {label}:")
        print(f"    {'Terms':>10} {'D4':>14} {'D5':>14} {'D5/D4':>14}")

        cum_results = []
        for max_n in [1, 2, 3, 4, 5, 10, 50]:
            terms = list(range(1, max_n + 1))
            kfunc = lambda u, t=terms: K_partial(u, t)
            d4 = toeplitz_det(kfunc, u0, h, 4)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            ratio = float(d5/d4) if d4 != 0 else float('inf')
            s4 = "+" if d4 > 0 else "-"
            s5 = "+" if d5 > 0 else "-"
            print(f"    f1..f{max_n:>3}: {float(d4):>14.4e}[{s4}] {float(d5):>14.4e}[{s5}] {ratio:>14.4e}")
            cum_results.append({
                'max_n': max_n,
                'D4': float(d4),
                'D5': float(d5),
                'ratio': ratio
            })

        results[f"({u0},{h})_cumulative"] = cum_results

    # Part 2: Incremental contributions
    print("\n--- Part 2: Incremental D5 change from each new term ---")
    for u0, h, label in configs[:3]:
        print(f"\n  Config ({u0}, {h}) - {label}:")
        prev_d5 = None
        for max_n in range(1, 11):
            terms = list(range(1, max_n + 1))
            kfunc = lambda u, t=terms: K_partial(u, t)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            if prev_d5 is not None:
                delta = float(d5 - prev_d5)
                print(f"    Adding f{max_n}: delta_D5 = {delta:>14.4e}, D5 = {float(d5):>14.4e}")
            else:
                print(f"    f1 alone:  D5 = {float(d5):>14.4e}")
            prev_d5 = d5

    # Part 3: The role of f1 vs f2 in the Toeplitz MATRIX (not just determinant)
    print("\n--- Part 3: Matrix-level analysis at (0.01, 0.05) ---")
    u0, h = 0.01, 0.05

    # Build Toeplitz matrices for f1 alone and f2 alone
    T_f1 = toeplitz_matrix(lambda u: K_partial(u, [1]), u0, h, 5)
    T_f2 = toeplitz_matrix(lambda u: K_partial(u, [2]), u0, h, 5)
    T_full = toeplitz_matrix(lambda u: K_partial(u, range(1, 51)), u0, h, 5)

    print("  Toeplitz matrix from f1 only (5x5):")
    for i in range(5):
        row = [float(T_f1[i,j]) for j in range(5)]
        print(f"    [{', '.join(f'{v:>12.6e}' for v in row)}]")

    print("\n  Toeplitz matrix from f2 only (5x5):")
    for i in range(5):
        row = [float(T_f2[i,j]) for j in range(5)]
        print(f"    [{', '.join(f'{v:>12.6e}' for v in row)}]")

    print("\n  Ratio T_f2/T_f1 (element-wise):")
    for i in range(5):
        row = [float(T_f2[i,j]/T_f1[i,j]) if T_f1[i,j] != 0 else float('inf') for j in range(5)]
        print(f"    [{', '.join(f'{v:>12.6e}' for v in row)}]")

    # Part 4: Eigenvalue analysis of the Toeplitz matrices
    print("\n--- Part 4: Eigenvalue analysis ---")
    # Use numpy for eigenvalues since mpmath doesn't have a direct eigensolver
    # Convert to float arrays
    import numpy as np

    T_f1_np = np.array([[float(T_f1[i,j]) for j in range(5)] for i in range(5)])
    T_full_np = np.array([[float(T_full[i,j]) for j in range(5)] for i in range(5)])

    eigs_f1 = np.linalg.eigvalsh(T_f1_np)
    eigs_full = np.linalg.eigvalsh(T_full_np)

    print(f"  Eigenvalues of T5(f1):   {eigs_f1}")
    print(f"  Eigenvalues of T5(full): {eigs_full}")
    print(f"  det(T5(f1)):   {np.prod(eigs_f1):.6e}")
    print(f"  det(T5(full)): {np.prod(eigs_full):.6e}")
    print(f"  Min eigenvalue of T5(f1):   {min(eigs_f1):.6e}")
    print(f"  Min eigenvalue of T5(full): {min(eigs_full):.6e}")

    # Part 5: The "effective perturbation" — how f2 shifts eigenvalues
    print("\n--- Part 5: How f2 shifts the spectrum ---")
    T_f2_np = np.array([[float(T_f2[i,j]) for j in range(5)] for i in range(5)])
    eigs_f2 = np.linalg.eigvalsh(T_f2_np)
    print(f"  Eigenvalues of T5(f2): {eigs_f2}")
    print(f"  Frobenius norm of T5(f2): {np.linalg.norm(T_f2_np, 'fro'):.6e}")
    print(f"  Frobenius norm of T5(f1): {np.linalg.norm(T_f1_np, 'fro'):.6e}")
    print(f"  Relative perturbation: {np.linalg.norm(T_f2_np, 'fro') / np.linalg.norm(T_f1_np, 'fro'):.6e}")

    # Part 6: Check which cofactor of D5 is responsible for negativity
    print("\n--- Part 6: Cofactor analysis of D5 ---")
    T = T_full
    # D5 = sum_j (-1)^j T[0,j] * M[0,j] where M[0,j] is the (0,j) minor
    print("  Laplace expansion along first row:")
    total = mpf(0)
    for j in range(5):
        # Build (4x4) minor by deleting row 0 and column j
        minor = matrix(4, 4)
        for ii in range(4):
            col_idx = 0
            for jj in range(5):
                if jj == j:
                    continue
                minor[ii, col_idx] = T[ii+1, jj]
                col_idx += 1
        cofactor = (-1)**j * T[0, j] * det(minor)
        total += cofactor
        print(f"    j={j}: (-1)^{j} * T[0,{j}] * M[0,{j}] = {float(cofactor):>14.6e}")
    print(f"    Sum = {float(total):>14.6e}")
    print(f"    D5  = {float(det(T)):>14.6e}")

    # Save
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf5-perturbation/inv2_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")

if __name__ == "__main__":
    main()
