#!/usr/bin/env python3
"""
Inverse Spectral Solver for the Hilbert-Polya Potential Sequence.

Given the first N nontrivial Riemann zeta zeros gamma_1, ..., gamma_N,
find V(x) on [0, L] such that the Schrodinger operator -u'' + V(x)u = lambda*u
with Dirichlet boundary conditions has eigenvalues lambda_n ~ gamma_n.

V(x) is parameterized using K Chebyshev polynomial modes.

Usage:
    python inverse_spectral_solver.py [N] [L] [K]

Requires Modal cloud compute for remote execution.
"""
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import differential_evolution, minimize


def eval_chebyshev(coeffs, x, L):
    """Evaluate Chebyshev expansion V(x) = sum c_k T_k(2x/L - 1) on [0, L]."""
    t = 2 * x / L - 1
    V = np.zeros_like(x, dtype=float)
    for k in range(len(coeffs)):
        V += coeffs[k] * np.cos(k * np.arccos(np.clip(t, -1, 1)))
    return V


def solve_schrodinger(V_coeffs, L, n_grid, n_eigs):
    """
    Solve -u'' + V(x)u = lambda*u on [0, L] with Dirichlet BCs.
    Returns the first n_eigs eigenvalues (sorted ascending).
    """
    K = len(V_coeffs)
    N = n_grid
    dx = L / (N + 1)
    x = np.linspace(dx, L - dx, N)  # interior grid points
    V = eval_chebyshev(V_coeffs, x, L)

    # Finite difference Hamiltonian: -d^2/dx^2 + V(x)
    diag_main = 2.0 / dx**2 + V
    diag_off = -1.0 / dx**2 * np.ones(N - 1)
    H = sparse.diags([diag_off, diag_main, diag_off], [-1, 0, 1], format='csc')

    try:
        n_req = min(n_eigs + 5, N - 2)
        eigs = eigsh(H, k=n_req, which='SM', return_eigenvectors=False)
        eigs = np.sort(eigs)
        return eigs[:n_eigs]
    except Exception:
        return None


def objective(V_coeffs, target_zeros, L, n_grid):
    """Sum of squared relative errors between eigenvalues and targets."""
    N_target = len(target_zeros)
    eigs = solve_schrodinger(V_coeffs, L, n_grid, N_target)
    if eigs is None or len(eigs) < N_target:
        return 1e10
    rel_errors = (eigs - target_zeros) / target_zeros
    return np.sum(rel_errors**2)


def solve_inverse_problem(target_zeros, L=10.0, K=None, n_grid=300,
                          warm_start=None, use_de=True):
    """
    Solve the inverse spectral problem: find V(x) whose eigenvalues
    match target_zeros.

    Parameters:
        target_zeros: array of N target eigenvalues
        L: domain length [0, L]
        K: number of Chebyshev modes (default: N + 5)
        n_grid: finite difference grid points
        warm_start: initial Chebyshev coefficients (or None)
        use_de: whether to use differential evolution (slow but more global)

    Returns:
        dict with coefficients, eigenvalues, errors, etc.
    """
    N = len(target_zeros)
    if K is None:
        K = N + 5

    # Initialize
    avg_shift = np.mean([target_zeros[i] - ((i+1)*np.pi/L)**2 for i in range(N)])
    x0 = np.zeros(K)
    x0[0] = avg_shift

    if warm_start is not None:
        min_k = min(len(warm_start), K)
        x0[:min_k] = np.array(warm_start)[:min_k]

    bounds = [(-300.0, 300.0)] * K

    # Phase 1: L-BFGS-B from warm start
    r1 = minimize(objective, x0, args=(target_zeros, L, n_grid),
                  method='L-BFGS-B', bounds=bounds,
                  options={'maxiter': 5000, 'ftol': 1e-15})

    best_x, best_loss = r1.x, r1.fun

    # Phase 2: Differential Evolution (optional)
    if use_de:
        center = r1.x
        bounds2 = [(c - 80, c + 80) for c in center]
        de = differential_evolution(
            objective, bounds2, args=(target_zeros, L, n_grid),
            maxiter=min(400, 150 + 8*N),
            popsize=min(20, 10 + K//3),
            seed=42, tol=1e-13, polish=False
        )
        if de.fun < best_loss:
            best_x, best_loss = de.x, de.fun

    # Phase 3: Final polish
    final = minimize(objective, best_x, args=(target_zeros, L, n_grid),
                     method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 5000, 'ftol': 1e-16})

    # Evaluate results
    fc = final.x
    fe = solve_schrodinger(fc, L, n_grid, N)

    if fe is not None and len(fe) >= N:
        rel_errors = ((fe - target_zeros) / target_zeros * 100).tolist()
        x_eval = np.linspace(0.01, L - 0.01, 500)
        V_eval = eval_chebyshev(fc, x_eval, L)

        return {
            "N": N, "L": L, "K": K,
            "loss": float(final.fun),
            "coefficients": fc.tolist(),
            "eigenvalues": fe.tolist(),
            "target_zeros": target_zeros.tolist(),
            "relative_errors_pct": rel_errors,
            "max_error_pct": float(max(abs(e) for e in rel_errors)),
            "mean_error_pct": float(np.mean(np.abs(rel_errors))),
            "V_x_values": x_eval.tolist(),
            "V_y_values": V_eval.tolist(),
        }
    return {"N": N, "error": "eigenvalue solve failed"}


if __name__ == "__main__":
    import sys, json

    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    L = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    K = int(sys.argv[3]) if len(sys.argv) > 3 else N + 5

    # Load zeta zeros
    import mpmath
    mpmath.mp.dps = 30
    zeros = np.array([float(mpmath.zetazero(n).imag) for n in range(1, N+1)])

    print(f"Solving inverse spectral problem: N={N}, L={L}, K={K}")
    result = solve_inverse_problem(zeros, L=L, K=K, use_de=True)

    if "error" in result:
        print(f"FAILED: {result['error']}")
    else:
        print(f"Loss: {result['loss']:.10f}")
        print(f"Max error: {result['max_error_pct']:.4f}%")
        print(f"Mean error: {result['mean_error_pct']:.4f}%")

        with open(f"result_N{N}_L{L}.json", "w") as f:
            json.dump(result, f, indent=2)
