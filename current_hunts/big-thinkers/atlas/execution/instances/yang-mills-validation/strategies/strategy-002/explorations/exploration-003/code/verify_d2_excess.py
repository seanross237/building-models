"""
Verify: does λ_max(H_actual) exceed 2.0 at d=2 for non-flat configs?
If the random walk found λ > 2.0, we need to verify with multiple h values.
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *


def random_walk_with_verification(lat, beta, n_steps=200, step_size=0.1, n_candidates=10):
    """Random walk ascent that saves the best config for verification."""
    Q_I = identity_config(lat)
    Q = random_su2_config(lat)
    lmax = compute_lmax_actual(Q, lat, beta, h=1e-4)
    best_Q = Q.copy()
    best_lmax = lmax

    for step in range(n_steps):
        improved = False
        for _ in range(n_candidates):
            dQ = np.random.randn(lat.n_links, 3)
            dQ = dQ / np.sqrt(np.sum(dQ**2)) * step_size

            Q_trial = Q.copy()
            for e in range(lat.n_links):
                Q_trial[e] = su2_exp(dQ[e]) @ Q[e]
                Q_trial[e] = project_su2(Q_trial[e])

            lmax_trial = compute_lmax_actual(Q_trial, lat, beta, h=1e-4)

            if lmax_trial > best_lmax:
                best_lmax = lmax_trial
                best_Q = Q_trial.copy()

            if lmax_trial > lmax:
                Q = Q_trial
                lmax = lmax_trial
                improved = True

        if not improved:
            step_size *= 0.8

        if step % 50 == 0:
            print(f"  Step {step:4d}: current λ = {lmax:.8f}, best = {best_lmax:.8f}")

    return best_Q, best_lmax


def main():
    beta = 1.0
    np.random.seed(42)

    for d in [2, 3]:
        print(f"\n{'='*70}")
        print(f"VERIFICATION: d={d}, L=2")
        print(f"{'='*70}")

        lat = Lattice(2, d)
        Q_I = identity_config(lat)

        # Reference at multiple h values
        print("Reference λ_max(I):")
        for h in [1e-3, 5e-4, 1e-4, 5e-5]:
            H = compute_hessian_fd(Q_I, lat, beta, h=h)
            H = (H + H.T) / 2
            lmax = eigvalsh(H)[-1]
            print(f"  h={h:.0e}: λ_max = {lmax:.12f}")

        # Find best config via random walk
        print("\nRunning random walk ascent (3 starts)...")
        best_Q_overall = None
        best_lmax_overall = 0

        for i in range(3):
            np.random.seed(42 + i * 100)
            Q_best, lmax_best = random_walk_with_verification(lat, beta, n_steps=200)
            if lmax_best > best_lmax_overall:
                best_lmax_overall = lmax_best
                best_Q_overall = Q_best.copy()
            print(f"  Start {i+1}: best λ = {lmax_best:.10f}")

        # Verify the best config with multiple h values
        print(f"\nBest found: λ = {best_lmax_overall:.10f}")
        print("Verifying with multiple h values:")
        for h in [1e-3, 5e-4, 1e-4, 5e-5, 2e-5]:
            H = compute_hessian_fd(best_Q_overall, lat, beta, h=h)
            H = (H + H.T) / 2
            lmax = eigvalsh(H)[-1]

            # Also compute reference at this h
            H_I = compute_hessian_fd(Q_I, lat, beta, h=h)
            H_I = (H_I + H_I.T) / 2
            lmax_I = eigvalsh(H_I)[-1]

            gap = lmax_I - lmax
            print(f"  h={h:.0e}: λ(best)={lmax:.10f}, λ(I)={lmax_I:.10f}, gap={gap:.8f} {'EXCEEDS' if gap < 0 else 'ok'}")

        # Check flatness
        flat_dev = 0.0
        for plaq in lat.plaquettes():
            e1, e2, e3, e4 = plaq['edges']
            U = best_Q_overall[e1] @ best_Q_overall[e2] @ np.linalg.inv(best_Q_overall[e3]) @ np.linalg.inv(best_Q_overall[e4])
            flat_dev = max(flat_dev, norm(U - np.eye(2)))
        print(f"  Max plaquette deviation: {flat_dev:.6f}")


if __name__ == '__main__':
    main()
