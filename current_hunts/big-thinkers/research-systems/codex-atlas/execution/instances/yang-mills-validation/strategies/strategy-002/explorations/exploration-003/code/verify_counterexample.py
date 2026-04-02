"""
CRITICAL VERIFICATION: At d=3, one-hot perturbations appear to INCREASE λ_max
above the flat connection value. If confirmed, flat connections are NOT global
maximizers of λ_max(H_actual).

Verify with multiple finite-difference step sizes to rule out numerical artifact.
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *


def verify_one_hot(L, d, beta, link_idx=0, color_idx=0, angles=None, h_values=None):
    """Verify λ_max for one-hot perturbations at various angles and h values."""
    if angles is None:
        angles = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, np.pi/2, np.pi]
    if h_values is None:
        h_values = [1e-3, 5e-4, 1e-4, 5e-5]

    lat = Lattice(L, d)
    Q_I = identity_config(lat)

    print(f"Lattice: L={L}, d={d}, DOF={lat.n_dof}")
    print(f"One-hot perturbation: link {link_idx}, color {color_idx}")
    print()

    # Compute reference λ_max(I) at each h
    print("Reference λ_max(I) at various h:")
    lmax_I = {}
    for h in h_values:
        H_I = compute_hessian_fd(Q_I, lat, beta, h=h)
        H_I = (H_I + H_I.T) / 2
        lmax_I[h] = eigvalsh(H_I)[-1]
        print(f"  h = {h:.0e}: λ_max(I) = {lmax_I[h]:.12f}")

    # Now compute λ_max at each angle and h
    print(f"\n{'angle':>8s}", end="")
    for h in h_values:
        print(f" {'h='+str(h):>16s}", end="")
    print(f" {'consistent?':>12s}")
    print("-" * (8 + 17 * len(h_values) + 12))

    for angle in angles:
        Q = identity_config(lat)
        if angle != 0.0:
            v = np.zeros(3)
            v[color_idx] = angle
            Q[link_idx] = su2_exp(v) @ Q[link_idx]

        lmax_vals = []
        for h in h_values:
            H = compute_hessian_fd(Q, lat, beta, h=h)
            H = (H + H.T) / 2
            lmax = eigvalsh(H)[-1]
            lmax_vals.append(lmax)

        # Check consistency: are all values within 0.001 of each other?
        spread = max(lmax_vals) - min(lmax_vals)
        consistent = spread < 0.001

        print(f"{angle:8.4f}", end="")
        for lmax in lmax_vals:
            print(f" {lmax:16.10f}", end="")
        print(f" {'YES' if consistent else 'SPREAD='+str(spread)[:6]:>12s}")

    # Gap analysis: use smallest h for best accuracy
    h_best = min(h_values)
    print(f"\nGap analysis (using h = {h_best:.0e}):")
    print(f"{'angle':>8s} {'λ_max(Q)':>14s} {'λ_max(I)':>14s} {'gap':>12s} {'Q>I?':>6s}")
    print("-" * 60)

    for angle in angles:
        Q = identity_config(lat)
        if angle != 0.0:
            v = np.zeros(3)
            v[color_idx] = angle
            Q[link_idx] = su2_exp(v) @ Q[link_idx]

        H = compute_hessian_fd(Q, lat, beta, h=h_best)
        H = (H + H.T) / 2
        lmax = eigvalsh(H)[-1]
        gap = lmax_I[h_best] - lmax
        exceeds = lmax > lmax_I[h_best] + 1e-8

        print(f"{angle:8.4f} {lmax:14.10f} {lmax_I[h_best]:14.10f} {gap:12.2e} "
              f"{'YES!' if exceeds else 'no':>6s}")


def verify_with_formula_hessian(L, d, beta, angle=0.5, link_idx=0, color_idx=0):
    """Also check H_formula at the same config, to see if the B² formula
    also has the same issue."""
    lat = Lattice(L, d)

    print(f"\n{'='*60}")
    print(f"FORMULA HESSIAN CHECK: d={d}, angle={angle}")
    print(f"{'='*60}")

    Q_I = identity_config(lat)
    Q_pert = identity_config(lat)
    v = np.zeros(3); v[color_idx] = angle
    Q_pert[link_idx] = su2_exp(v) @ Q_pert[link_idx]

    h = 5e-5
    H_actual_I = compute_hessian_fd(Q_I, lat, beta, h=h)
    H_actual_I = (H_actual_I + H_actual_I.T) / 2
    H_actual_Q = compute_hessian_fd(Q_pert, lat, beta, h=h)
    H_actual_Q = (H_actual_Q + H_actual_Q.T) / 2

    H_formula_I = compute_hessian_formula(Q_I, lat, beta)
    H_formula_Q = compute_hessian_formula(Q_pert, lat, beta)

    lmax_actual_I = eigvalsh(H_actual_I)[-1]
    lmax_actual_Q = eigvalsh(H_actual_Q)[-1]
    lmax_formula_I = eigvalsh(H_formula_I)[-1]
    lmax_formula_Q = eigvalsh(H_formula_Q)[-1]

    print(f"λ_max(H_actual(I))  = {lmax_actual_I:.10f}")
    print(f"λ_max(H_actual(Q))  = {lmax_actual_Q:.10f}")
    print(f"λ_max(H_formula(I)) = {lmax_formula_I:.10f}")
    print(f"λ_max(H_formula(Q)) = {lmax_formula_Q:.10f}")
    print(f"")
    print(f"Gap actual:  λ(I) - λ(Q) = {lmax_actual_I - lmax_actual_Q:.10f}")
    print(f"Gap formula: λ(I) - λ(Q) = {lmax_formula_I - lmax_formula_Q:.10f}")
    print(f"r(Q) = λ_actual(Q) / λ_formula(Q) = {lmax_actual_Q / lmax_formula_Q:.10f}")
    print(f"r(I) = λ_actual(I) / λ_formula(I) = {lmax_actual_I / lmax_formula_I:.10f}")


def main():
    beta = 1.0

    # ===== d=2 (baseline) =====
    print("#" * 70)
    print("# d=2, L=2 (baseline — should show all gaps > 0)")
    print("#" * 70)
    verify_one_hot(2, 2, beta, h_values=[1e-3, 5e-4, 1e-4, 5e-5])

    # ===== d=3 (potential counterexample) =====
    print("\n\n" + "#" * 70)
    print("# d=3, L=2 (POTENTIAL COUNTEREXAMPLE)")
    print("#" * 70)
    verify_one_hot(2, 3, beta, h_values=[1e-3, 5e-4, 1e-4, 5e-5])

    # Also check link 0 color 1, link 1 color 0, etc.
    print("\n--- Other link/color combinations at d=3 ---")
    for link in [0, 1, 5]:
        for color in [0, 1, 2]:
            lat = Lattice(2, 3)
            Q_I = identity_config(lat)
            Q_pert = identity_config(lat)
            v = np.zeros(3); v[color] = 0.5
            Q_pert[link] = su2_exp(v) @ Q_pert[link]

            h = 5e-5
            H_I = compute_hessian_fd(Q_I, lat, beta, h=h)
            H_I = (H_I + H_I.T) / 2
            H_Q = compute_hessian_fd(Q_pert, lat, beta, h=h)
            H_Q = (H_Q + H_Q.T) / 2

            lmax_I = eigvalsh(H_I)[-1]
            lmax_Q = eigvalsh(H_Q)[-1]
            gap = lmax_I - lmax_Q

            print(f"  link={link}, color={color}: λ_max(I)={lmax_I:.8f}, "
                  f"λ_max(Q)={lmax_Q:.8f}, gap={gap:.6f} "
                  f"{'<< EXCEEDS' if gap < -1e-4 else ''}")

    # Formula hessian comparison
    verify_with_formula_hessian(2, 3, beta, angle=0.5)

    # ===== d=4 =====
    print("\n\n" + "#" * 70)
    print("# d=4, L=2 (TARGET DIMENSION)")
    print("#" * 70)
    verify_one_hot(2, 4, beta,
                   angles=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0],
                   h_values=[1e-4, 5e-5])


if __name__ == '__main__':
    main()
