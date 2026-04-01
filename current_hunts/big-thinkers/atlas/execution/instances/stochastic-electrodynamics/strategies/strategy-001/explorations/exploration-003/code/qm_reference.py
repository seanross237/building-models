"""
QM Reference Values for Anharmonic Oscillator V(x) = 0.5*x^2 + beta*x^4

Uses matrix diagonalization in the harmonic oscillator basis.
Natural units: hbar=1, m=1, omega_0=1

Matrix elements of x in harmonic oscillator basis:
  <n|x|m> = sqrt(n/2)*delta_{n,m+1} + sqrt((n+1)/2)*delta_{n,m-1}
  x = (a + a†) / sqrt(2)
  x^2 = (a^2 + 2*a†a + 1 + (a†)^2) / 2
  x^4 computed numerically via x^4 = (x^2)^2
"""

import numpy as np
from scipy.linalg import eigh
import json

def build_x_matrix(N):
    """Build x matrix in harmonic oscillator basis."""
    x = np.zeros((N, N))
    for n in range(N-1):
        val = np.sqrt((n+1)/2.0)
        x[n, n+1] = val
        x[n+1, n] = val
    return x

def build_hamiltonian(beta, N):
    """Build H = -0.5*d^2/dx^2 + 0.5*x^2 + beta*x^4 in HO basis."""
    # Diagonal: H_0 = n + 0.5
    H0 = np.diag(np.arange(N) + 0.5)

    # x matrix
    x = build_x_matrix(N)

    # x^2 matrix
    x2 = x @ x

    # x^4 matrix
    x4 = x2 @ x2

    H = H0 + beta * x4
    return H, x, x2, x4

def compute_qm_values(beta_list, N=80):
    """Compute QM ground state energy and position statistics for each beta."""
    results = {}

    for beta in beta_list:
        H, x, x2, x4 = build_hamiltonian(beta, N)

        # Diagonalize (only need lowest eigenvalues)
        # eigh returns eigenvalues in ascending order
        eigvals, eigvecs = eigh(H)

        E0 = eigvals[0]
        psi0 = eigvecs[:, 0]  # ground state coefficients in HO basis

        # Expectation values
        # <x> = 0 by symmetry (parity)
        # <x^2> = psi0^T @ x2 @ psi0
        var_x = psi0 @ (x2 @ psi0)  # = <x^2> since <x>=0

        # <x^4>
        x4_exp = psi0 @ (x4 @ psi0)

        # Potential energy <V> = 0.5*<x^2> + beta*<x^4>
        PE = 0.5 * var_x + beta * x4_exp

        # Perturbation theory (valid for small beta):
        # E0 = 0.5 + 0.75*beta - 2.625*beta^2 + O(beta^3)
        E0_PT = 0.5 + 0.75*beta - 2.625*beta**2

        # For var_x, perturbation theory:
        # var_x = <x^2> = 0.5 + delta at O(beta)
        # <x^2> = 0.5 + correction
        # First-order: correction = sum_{n!=0} |<n|x^4|0>| / (E0-En) * x^2 matrix elements
        # We compute this numerically below

        results[beta] = {
            'E0': float(E0),
            'E0_PT': float(E0_PT),
            'var_x': float(var_x),
            'x4_exp': float(x4_exp),
            'PE': float(PE),
            'psi0_coeffs': psi0.tolist()  # for wavefunction computation
        }

        print(f"beta={beta:.3f}: E0={E0:.6f} (PT: {E0_PT:.6f}), "
              f"var_x={var_x:.6f}, <x^4>={x4_exp:.6f}, PE={PE:.6f}")

    return results

def compute_qm_wavefunction(psi0_coeffs, x_grid):
    """Compute QM wavefunction on a spatial grid from HO expansion coefficients."""
    from scipy.special import hermite
    from math import factorial

    N = len(psi0_coeffs)
    psi_x = np.zeros_like(x_grid, dtype=float)

    for n, cn in enumerate(psi0_coeffs):
        # HO eigenfunction: psi_n(x) = (2^n n! sqrt(pi))^{-1/2} H_n(x) exp(-x^2/2)
        Hn = hermite(n)
        norm = 1.0 / np.sqrt(2**n * factorial(n) * np.sqrt(np.pi))
        psi_n = norm * Hn(x_grid) * np.exp(-x_grid**2 / 2)
        psi_x += cn * psi_n

    return psi_x

if __name__ == '__main__':
    beta_list = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

    print("="*70)
    print("QM Reference Values — Anharmonic Oscillator V(x) = 0.5*x^2 + beta*x^4")
    print("N_max = 80, hbar=1, m=1, omega_0=1")
    print("="*70)
    print()

    # Run with N=80
    print("--- N_max = 80 ---")
    results_80 = compute_qm_values(beta_list, N=80)

    print()
    print("--- Convergence check: N_max = 50 ---")
    results_50 = compute_qm_values(beta_list, N=50)

    print()
    print("--- Convergence check ---")
    print(f"{'beta':>6} | {'E0(N=80)':>12} | {'E0(N=50)':>12} | {'diff':>12}")
    print("-"*50)
    for beta in beta_list:
        diff = results_80[beta]['E0'] - results_50[beta]['E0']
        print(f"{beta:6.3f} | {results_80[beta]['E0']:12.8f} | {results_50[beta]['E0']:12.8f} | {diff:12.2e}")

    print()
    print("--- Summary Table ---")
    print(f"{'beta':>6} | {'E0':>12} | {'E0_PT':>12} | {'var_x':>12} | {'<x^4>':>12} | {'PE':>12}")
    print("-"*75)
    for beta in beta_list:
        r = results_80[beta]
        print(f"{beta:6.3f} | {r['E0']:12.8f} | {r['E0_PT']:12.8f} | "
              f"{r['var_x']:12.8f} | {r['x4_exp']:12.8f} | {r['PE']:12.8f}")

    # Save results
    import os
    save_path = os.path.join(os.path.dirname(__file__), 'qm_reference_results.json')
    # Remove psi0 coefficients for cleaner save
    save_results = {}
    for beta, r in results_80.items():
        save_results[str(beta)] = {k: v for k, v in r.items() if k != 'psi0_coeffs'}

    with open(save_path, 'w') as f:
        json.dump(save_results, f, indent=2)
    print(f"\nResults saved to {save_path}")
