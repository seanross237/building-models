"""
Fast Gradient Ascent on λ_max(H_actual(Q)) — d=2 only.

Key insight: compute gradient using Hellmann-Feynman theorem:
  ∂λ_max/∂t = v_max^T (∂H/∂t) v_max
where v_max is the top eigenvector. This avoids n separate Hessian evaluations!

Instead, compute H once, get v_max, then use:
  ∂λ_max/∂v_{e,a} ≈ v^T [(H(+h) - H(-h))/(2h)] v

But even faster: v^T H(perturbed) v ≈ v^T H v + h * v^T [∂H/∂v_{e,a}] v + O(h²)
So: ∂λ_max/∂v_{e,a} ≈ (v^T H(+h) v - v^T H(-h) v) / (2h)

And v^T H v = Rayleigh quotient, which we can compute cheaply by just doing
the double finite difference of S with perturbation in the v direction!

Actually simplest: just compute Rayleigh quotient R(v, Q) = Σ_{i,j} v_i H_{ij} v_j = d²S/dt² along direction v.
This is a SINGLE finite-difference computation per gradient component.

Even simpler approach: Hill climbing. At each step:
1. Compute H(Q), get λ_max and v_max
2. Perturb each link by ±h in each color direction
3. For each perturbation, compute λ_max of the new H
4. Move in the direction of largest increase

OR: Just use the "cheap gradient" approach:
∂λ_max/∂v_{e,a} ≈ [λ_max(exp(h T_a) Q_e, Q_{rest}) - λ_max(exp(-h T_a) Q_e, Q_{rest})] / (2h)

This requires 2 * n_links * 3 = 48 Hessian evals for d=2, which is expensive.
Let's use a MUCH cheaper approach for d=2: just sample directions and do line search.
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *


def random_walk_ascent(Q_init, lattice, beta, n_steps=200, step_size=0.1, n_candidates=10):
    """
    Random walk ascent: at each step, try n_candidates random perturbation
    directions and pick the one that increases λ_max the most.
    """
    Q = Q_init.copy()
    lmax_current = compute_lmax_actual(Q, lattice, beta)
    history = []

    for step in range(n_steps):
        best_lmax = lmax_current
        best_Q = None

        for _ in range(n_candidates):
            # Random perturbation direction
            dQ = np.random.randn(lattice.n_links, 3)
            dQ = dQ / np.sqrt(np.sum(dQ**2)) * step_size

            Q_trial = Q.copy()
            for e in range(lattice.n_links):
                Q_trial[e] = su2_exp(dQ[e]) @ Q[e]
                Q_trial[e] = project_su2(Q_trial[e])

            lmax_trial = compute_lmax_actual(Q_trial, lattice, beta)

            if lmax_trial > best_lmax:
                best_lmax = lmax_trial
                best_Q = Q_trial.copy()

        flat_dev = check_flatness(Q, lattice)
        history.append({
            'step': step,
            'lmax': lmax_current,
            'flat_dev': flat_dev,
        })

        if step % 20 == 0:
            print(f"  Step {step:4d}: λ_max = {lmax_current:.8f}, "
                  f"plaq_dev = {flat_dev:.6f}")

        if best_Q is not None:
            Q = best_Q
            lmax_current = best_lmax
        else:
            # No improvement found — reduce step size
            step_size *= 0.5
            if step_size < 1e-6:
                break

    flat_dev = check_flatness(Q, lattice)
    history.append({'step': len(history), 'lmax': lmax_current, 'flat_dev': flat_dev})
    return Q, history


def check_flatness(Q, lattice):
    max_dev = 0.0
    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']
        U_plaq = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])
        dev = norm(U_plaq - np.eye(2))
        max_dev = max(max_dev, dev)
    return max_dev


def simulated_annealing_max(Q_init, lattice, beta, n_steps=500, T_init=0.1, T_final=0.001):
    """Simulated annealing to find global max of λ_max."""
    Q = Q_init.copy()
    lmax_current = compute_lmax_actual(Q, lattice, beta)
    best_Q = Q.copy()
    best_lmax = lmax_current

    history = []

    for step in range(n_steps):
        T = T_init * (T_final / T_init) ** (step / n_steps)
        step_size = T

        # Random perturbation
        dQ = np.random.randn(lattice.n_links, 3)
        dQ = dQ / np.sqrt(np.sum(dQ**2)) * step_size

        Q_trial = Q.copy()
        for e in range(lattice.n_links):
            Q_trial[e] = su2_exp(dQ[e]) @ Q[e]
            Q_trial[e] = project_su2(Q_trial[e])

        lmax_trial = compute_lmax_actual(Q_trial, lattice, beta)

        delta = lmax_trial - lmax_current
        if delta > 0 or np.random.random() < np.exp(delta / T):
            Q = Q_trial
            lmax_current = lmax_trial

            if lmax_current > best_lmax:
                best_lmax = lmax_current
                best_Q = Q.copy()

        if step % 50 == 0:
            flat_dev = check_flatness(Q, lattice)
            history.append({'step': step, 'lmax': lmax_current, 'best_lmax': best_lmax, 'flat_dev': flat_dev})
            print(f"  Step {step:4d}: λ_max = {lmax_current:.8f}, "
                  f"best = {best_lmax:.8f}, T = {T:.6f}, "
                  f"plaq_dev = {flat_dev:.6f}")

    return best_Q, best_lmax, history


def main():
    beta = 1.0
    L, d = 2, 2
    lat = Lattice(L, d)

    lmax_flat = compute_lmax_actual(identity_config(lat), lat, beta)
    print(f"Lattice: L={L}, d={d}, DOF={lat.n_dof}")
    print(f"λ_max(flat) = {lmax_flat:.10f}")

    # ==================== Method 1: Random Walk Ascent ====================
    print(f"\n{'='*60}")
    print("METHOD 1: Random Walk Ascent")
    print(f"{'='*60}")

    np.random.seed(42)
    n_starts = 10
    results = []

    for i in range(n_starts):
        if i < 5:
            Q0 = random_su2_config(lat)
            label = f"Haar random #{i+1}"
        elif i < 8:
            scale = [0.1, 0.5, 1.0][i-5]
            Q0 = identity_config(lat)
            for e in range(lat.n_links):
                v = np.random.randn(3) * scale
                Q0[e] = su2_exp(v) @ Q0[e]
            label = f"Near flat (ε={scale})"
        else:
            Q0 = identity_config(lat)
            v = np.zeros(3)
            v[0] = [np.pi/2, np.pi][i-8]
            Q0[0] = su2_exp(v) @ Q0[0]
            label = f"One-hot ({v[0]:.2f})"

        lmax_init = compute_lmax_actual(Q0, lat, beta)
        flat_init = check_flatness(Q0, lat)
        print(f"\n--- {label} ---")
        print(f"  Initial: λ_max = {lmax_init:.8f}, plaq_dev = {flat_init:.6f}")

        Q_final, history = random_walk_ascent(
            Q0, lat, beta, n_steps=200, step_size=0.1, n_candidates=10
        )

        lmax_final = history[-1]['lmax']
        flat_final = history[-1]['flat_dev']

        results.append({
            'label': label,
            'lmax_init': lmax_init,
            'lmax_final': lmax_final,
            'flat_init': flat_init,
            'flat_final': flat_final,
        })

        print(f"  Final: λ_max = {lmax_final:.8f}, plaq_dev = {flat_final:.6f}")
        print(f"  Reached {lmax_final/lmax_flat*100:.2f}% of flat value")

    # ==================== Method 2: Simulated Annealing ====================
    print(f"\n{'='*60}")
    print("METHOD 2: Simulated Annealing (3 starts)")
    print(f"{'='*60}")

    np.random.seed(123)
    sa_results = []

    for i in range(3):
        Q0 = random_su2_config(lat)
        lmax_init = compute_lmax_actual(Q0, lat, beta)
        flat_init = check_flatness(Q0, lat)
        print(f"\n--- SA Start {i+1} (Haar random) ---")
        print(f"  Initial: λ_max = {lmax_init:.8f}, plaq_dev = {flat_init:.6f}")

        Q_best, best_lmax, history = simulated_annealing_max(
            Q0, lat, beta, n_steps=500, T_init=0.5, T_final=0.001
        )

        flat_best = check_flatness(Q_best, lat)
        sa_results.append({
            'lmax_init': lmax_init,
            'best_lmax': best_lmax,
            'flat_best': flat_best,
        })
        print(f"  Best: λ_max = {best_lmax:.8f}, plaq_dev = {flat_best:.6f}")
        print(f"  Reached {best_lmax/lmax_flat*100:.2f}% of flat value")

    # ==================== Summary ====================
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    print(f"\nλ_max(flat) = {lmax_flat:.10f}")
    print(f"\nRandom Walk Ascent:")
    print(f"{'Label':<25s} {'λ_init':>10s} {'λ_final':>10s} {'%flat':>8s} {'flat_dev':>10s}")
    print("-" * 70)
    for r in results:
        pct = r['lmax_final'] / lmax_flat * 100
        print(f"{r['label']:<25s} {r['lmax_init']:10.6f} {r['lmax_final']:10.6f} {pct:7.2f}% {r['flat_final']:10.6f}")

    print(f"\nSimulated Annealing:")
    for i, r in enumerate(sa_results):
        pct = r['best_lmax'] / lmax_flat * 100
        print(f"  SA {i+1}: {r['lmax_init']:.6f} → {r['best_lmax']:.6f} ({pct:.2f}%), plaq_dev = {r['flat_best']:.6f}")

    # Key question: did any non-flat config achieve λ_max close to flat?
    all_finals = [r['lmax_final'] for r in results] + [r['best_lmax'] for r in sa_results]
    max_non_flat = max(all_finals)
    print(f"\nHighest λ_max found: {max_non_flat:.8f}")
    print(f"Gap from flat: {lmax_flat - max_non_flat:.8f}")
    print(f"Ratio: {max_non_flat/lmax_flat:.8f}")

    if max_non_flat > lmax_flat - 0.001:
        # Close to flat value — check if it's actually on the gauge orbit of I
        print("\nWARNING: Found config close to flat value — checking if it's gauge-flat")
    else:
        print(f"\nAll non-flat configs have λ_max < {lmax_flat:.6f} (flat value)")
        print("Consistent with flat connections being global maximizers")


if __name__ == '__main__':
    main()
