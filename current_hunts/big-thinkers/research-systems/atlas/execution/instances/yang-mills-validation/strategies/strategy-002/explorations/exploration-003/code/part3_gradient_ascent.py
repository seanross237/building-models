"""
Part 4: Gradient Ascent on λ_max(H_actual(Q))

Starting from random non-flat configs, ascend on λ_max to check
whether all trajectories converge to flat connections (gauge orbit of I).

Uses numerical gradient: ∂λ_max/∂v_{e,a} ≈ (λ_max(exp(h T_a)Q_e) - λ_max(exp(-h T_a)Q_e)) / (2h)
"""

import numpy as np
from numpy.linalg import eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import (Lattice, identity_config, su2_exp, wilson_action,
                          compute_hessian_fd, compute_lmax_actual,
                          random_su2_config, haar_random_su2, project_su2)


def compute_lmax_gradient(Q, lattice, beta, h_grad=0.01, h_hess=1e-4):
    """
    Compute gradient of λ_max(H_actual(Q)) w.r.t. left perturbations.

    Returns grad: array of shape (n_links, 3)
    """
    n_links = lattice.n_links
    grad = np.zeros((n_links, 3))
    lmax_0 = compute_lmax_actual(Q, lattice, beta, h=h_hess)

    for e in range(n_links):
        for a in range(3):
            Q_plus = Q.copy()
            v = np.zeros(3)
            v[a] = h_grad
            Q_plus[e] = su2_exp(v) @ Q[e]

            Q_minus = Q.copy()
            v[a] = -h_grad
            Q_minus[e] = su2_exp(v) @ Q[e]

            lmax_plus = compute_lmax_actual(Q_plus, lattice, beta, h=h_hess)
            lmax_minus = compute_lmax_actual(Q_minus, lattice, beta, h=h_hess)

            grad[e, a] = (lmax_plus - lmax_minus) / (2 * h_grad)

    return grad, lmax_0


def gradient_ascent(Q_init, lattice, beta, lr=0.01, max_steps=50, tol=1e-6,
                    h_grad=0.01, h_hess=1e-4, verbose=True):
    """
    Gradient ascent on λ_max(H_actual(Q)).
    Updates: Q_e → exp(lr * grad_{e,a} T_a) Q_e
    """
    Q = Q_init.copy()
    history = []

    for step in range(max_steps):
        grad, lmax = compute_lmax_gradient(Q, lattice, beta, h_grad=h_grad, h_hess=h_hess)
        grad_norm = np.sqrt(np.sum(grad**2))

        # Check if near flat
        max_plaq_dev = check_flatness(Q, lattice)

        history.append({
            'step': step,
            'lmax': lmax,
            'grad_norm': grad_norm,
            'max_plaq_dev': max_plaq_dev,
        })

        if verbose:
            print(f"  Step {step:3d}: λ_max = {lmax:.8f}, "
                  f"|∇| = {grad_norm:.6f}, plaq_dev = {max_plaq_dev:.6f}")

        if grad_norm < tol:
            if verbose:
                print(f"  Converged (grad norm < {tol})")
            break

        # Update: Q_e → exp(lr * grad_e) Q_e
        for e in range(lattice.n_links):
            v = lr * grad[e]
            Q[e] = su2_exp(v) @ Q[e]
            # Re-project to SU(2) for numerical stability
            Q[e] = project_su2(Q[e])

    return Q, history


def check_flatness(Q, lattice):
    """Check how close Q is to a flat connection (all plaquettes = I)."""
    max_dev = 0.0
    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']
        U_plaq = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])
        dev = norm(U_plaq - np.eye(2))
        max_dev = max(max_dev, dev)
    return max_dev


def near_flat_config(lattice, scale=0.1):
    """Generate a near-flat config: Q_e = exp(scale * random_su2) · I."""
    n_links = lattice.n_links
    Q = np.array([np.eye(2, dtype=complex) for _ in range(n_links)])
    for e in range(n_links):
        v = np.random.randn(3) * scale
        Q[e] = su2_exp(v) @ Q[e]
    return Q


def main():
    beta = 1.0

    # ===================== d=2 (fast) =====================
    print("=" * 70)
    print("GRADIENT ASCENT: d=2, L=2")
    print("=" * 70)

    L, d = 2, 2
    lat = Lattice(L, d)
    print(f"Links: {lat.n_links}, DOF: {lat.n_dof}")

    lmax_flat = compute_lmax_actual(identity_config(lat), lat, beta)
    print(f"λ_max(flat) = {lmax_flat:.10f}")

    n_starts = 10
    np.random.seed(42)

    converged_to_flat = 0
    results = []

    for i in range(n_starts):
        print(f"\n--- Start {i+1}/{n_starts} ---")

        if i < 5:
            # Haar random
            Q0 = random_su2_config(lat)
            label = "Haar random"
        elif i < 8:
            # Near flat (various scales)
            scale = [0.1, 0.5, 1.0][i-5]
            Q0 = near_flat_config(lat, scale=scale)
            label = f"Near flat (scale={scale})"
        else:
            # Structured: one-hot perturbation
            Q0 = identity_config(lat)
            v = np.zeros(3)
            v[0] = [np.pi/2, np.pi][i-8]
            Q0[0] = su2_exp(v) @ Q0[0]
            label = f"One-hot ({v[0]:.2f})"

        lmax_init = compute_lmax_actual(Q0, lat, beta)
        flat_init = check_flatness(Q0, lat)
        print(f"  Config type: {label}")
        print(f"  Initial λ_max = {lmax_init:.8f}, plaq_dev = {flat_init:.6f}")

        Q_final, history = gradient_ascent(
            Q0, lat, beta, lr=0.02, max_steps=30,
            h_grad=0.01, h_hess=1e-4, verbose=True
        )

        lmax_final = history[-1]['lmax']
        flat_final = history[-1]['max_plaq_dev']

        is_flat = flat_final < 0.1
        if is_flat:
            converged_to_flat += 1

        results.append({
            'label': label,
            'lmax_init': lmax_init,
            'lmax_final': lmax_final,
            'flat_init': flat_init,
            'flat_final': flat_final,
            'is_flat': is_flat,
            'n_steps': len(history),
        })

        print(f"  Final: λ_max = {lmax_final:.8f}, "
              f"plaq_dev = {flat_final:.6f}, "
              f"converged_to_flat = {is_flat}")

    # Summary
    print(f"\n{'='*70}")
    print(f"GRADIENT ASCENT SUMMARY: d=2")
    print(f"{'='*70}")
    print(f"Converged to flat: {converged_to_flat}/{n_starts}")
    print(f"\n{'Label':<30s} {'λ_init':>10s} {'λ_final':>10s} {'flat_dev':>10s} {'→flat':>6s}")
    print("-" * 70)
    for r in results:
        print(f"{r['label']:<30s} {r['lmax_init']:10.6f} {r['lmax_final']:10.6f} "
              f"{r['flat_final']:10.6f} {'YES' if r['is_flat'] else 'NO':>6s}")

    # ===================== d=3 (medium) =====================
    print(f"\n\n{'='*70}")
    print(f"GRADIENT ASCENT: d=3, L=2")
    print(f"{'='*70}")

    L, d = 2, 3
    lat = Lattice(L, d)
    print(f"Links: {lat.n_links}, DOF: {lat.n_dof}")

    lmax_flat = compute_lmax_actual(identity_config(lat), lat, beta)
    print(f"λ_max(flat) = {lmax_flat:.10f}")

    np.random.seed(99)
    n_starts_3 = 5
    results_3 = []
    converged_3 = 0

    for i in range(n_starts_3):
        print(f"\n--- Start {i+1}/{n_starts_3} ---")
        if i < 3:
            Q0 = random_su2_config(lat)
            label = "Haar random"
        else:
            Q0 = near_flat_config(lat, scale=0.5)
            label = "Near flat (0.5)"

        lmax_init = compute_lmax_actual(Q0, lat, beta)
        flat_init = check_flatness(Q0, lat)
        print(f"  Config type: {label}")
        print(f"  Initial λ_max = {lmax_init:.8f}, plaq_dev = {flat_init:.6f}")

        Q_final, history = gradient_ascent(
            Q0, lat, beta, lr=0.02, max_steps=30,
            h_grad=0.01, h_hess=1e-4, verbose=True
        )

        lmax_final = history[-1]['lmax']
        flat_final = history[-1]['max_plaq_dev']
        is_flat = flat_final < 0.1
        if is_flat:
            converged_3 += 1

        results_3.append({
            'label': label,
            'lmax_init': lmax_init,
            'lmax_final': lmax_final,
            'flat_final': flat_final,
            'is_flat': is_flat,
        })

        print(f"  Final: λ_max = {lmax_final:.8f}, plaq_dev = {flat_final:.6f}")

    print(f"\nConverged to flat: {converged_3}/{n_starts_3}")


if __name__ == '__main__':
    main()
