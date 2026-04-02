"""
Part 1: Perturbation Theory at Q = I

Strategy:
- Phase A: d=2, L=2 (24×24 Hessian, fast) — full analysis
- Phase B: d=4, L=2 (192×192 Hessian, slower) — targeted verification

At Q = I:
- H_actual(I) = H_formula(I) = lattice curl-curl operator
- λ_max = 2d·β/(d-1)... actually λ_max = 4β for d=4, let's compute it
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import (Lattice, identity_config, su2_exp, wilson_action,
                          compute_hessian_fd, compute_lmax_and_evecs,
                          compute_lmax_actual, perturb_config, random_su2_config,
                          haar_random_su2, apply_gauge_transform)


def run_perturbation_analysis(L, d, beta, n_directions=20, label=""):
    """Full perturbation analysis for given lattice parameters."""
    np.random.seed(42)
    lat = Lattice(L, d)
    n_links = lat.n_links
    n_dof = lat.n_dof
    n_plaq = len(lat.plaquettes())

    print(f"\n{'='*70}")
    print(f"PERTURBATION ANALYSIS: L={L}, d={d}, β={beta} {label}")
    print(f"Links: {n_links}, DOF: {n_dof}, Plaquettes: {n_plaq}")
    print(f"{'='*70}")

    Q_I = identity_config(lat)

    # Step 1: Eigenstructure at identity
    print("\n--- Step 1: Eigenstructure at Q = I ---")
    t0 = time.time()
    H_I = compute_hessian_fd(Q_I, lat, beta)
    H_I = (H_I + H_I.T) / 2
    t1 = time.time()
    print(f"Hessian computed in {t1-t0:.2f}s")

    evals_I, evecs_I = eigh(H_I)
    lmax_I = evals_I[-1]
    print(f"λ_max(H(I)) = {lmax_I:.10f}")

    # Degeneracy
    tol = 0.005
    deg_mask = evals_I > (lmax_I - tol)
    degeneracy = np.sum(deg_mask)
    print(f"Degeneracy of top eigenvalue: {degeneracy}")

    # Print spectrum summary
    unique_evals = []
    current_val = evals_I[0]
    current_count = 1
    for i in range(1, len(evals_I)):
        if abs(evals_I[i] - current_val) < 0.005:
            current_count += 1
        else:
            unique_evals.append((current_val, current_count))
            current_val = evals_I[i]
            current_count = 1
    unique_evals.append((current_val, current_count))

    print(f"\nSpectrum (grouped, tol=0.005):")
    for val, count in unique_evals:
        print(f"  λ = {val:10.6f} (degeneracy {count})")

    top_evecs = evecs_I[:, deg_mask]  # shape (n_dof, degeneracy)

    # Step 2: Line scans + perturbation analysis
    print(f"\n--- Step 2: Line Scans ({n_directions} directions) ---")

    # Sparse t values for efficiency
    t_values = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]

    dt_first = 0.001  # for dH/dt finite difference

    all_results = []

    print(f"\n{'Dir':>4s} {'Δ_max':>10s} {'d²λ/dt²':>10s} {'c=gap/t²':>10s}", end="")
    for t in t_values[1:]:
        print(f" {'λ('+str(t)+')':>12s}", end="")
    print(f" {'monotone':>8s}")
    print("-" * (44 + 13 * len(t_values[1:])))

    for idx in range(n_directions):
        delta_Q = np.random.randn(n_links, 3)
        delta_Q = delta_Q / np.sqrt(np.sum(delta_Q**2))

        lmax_at_t = {}
        lmax_at_t[0.0] = lmax_I

        for t in t_values[1:]:
            Q_t = perturb_config(Q_I, delta_Q, t)
            lmax_at_t[t] = compute_lmax_actual(Q_t, lat, beta)

        # First-order: Δ matrix
        Q_plus = perturb_config(Q_I, delta_Q, dt_first)
        Q_minus = perturb_config(Q_I, delta_Q, -dt_first)
        H_plus = compute_hessian_fd(Q_plus, lat, beta)
        H_minus = compute_hessian_fd(Q_minus, lat, beta)
        H_plus = (H_plus + H_plus.T) / 2
        H_minus = (H_minus + H_minus.T) / 2

        dH_dt = (H_plus - H_minus) / (2 * dt_first)
        Delta = top_evecs.T @ dH_dt @ top_evecs
        Delta_eigs = eigvalsh(Delta)

        # Second-order
        lmax_plus = eigvalsh(H_plus)[-1]
        lmax_minus = eigvalsh(H_minus)[-1]
        d2l_dt2 = (lmax_plus + lmax_minus - 2*lmax_I) / dt_first**2

        # Quadratic fit c from t=0.01 data
        gap_001 = lmax_I - lmax_at_t[0.01]
        c_est = gap_001 / (0.01**2) if gap_001 > 0 else 0.0

        # Monotone check
        lvals = [lmax_at_t[t] for t in t_values]
        monotone = all(lvals[i] >= lvals[i+1] - 1e-6 for i in range(len(lvals)-1))

        res = {
            'lmax_at_t': lmax_at_t,
            'Delta_eigs': Delta_eigs,
            'd2l_dt2': d2l_dt2,
            'c_est': c_est,
            'monotone': monotone,
        }
        all_results.append(res)

        print(f"{idx+1:4d} {Delta_eigs[-1]:10.4f} {d2l_dt2:10.2f} {c_est:10.4f}", end="")
        for t in t_values[1:]:
            print(f" {lmax_at_t[t]:12.8f}", end="")
        print(f" {'YES' if monotone else 'NO':>8s}")

    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: L={L}, d={d}")
    print(f"{'='*70}")

    fo = np.array([r['Delta_eigs'][-1] for r in all_results])
    so = np.array([r['d2l_dt2'] for r in all_results])
    cs = np.array([r['c_est'] for r in all_results])

    print(f"\nFirst-order max(Δ_ij eigenvalue):")
    print(f"  range: [{fo.min():.6f}, {fo.max():.6f}]")
    print(f"  |max|: {np.abs(fo).max():.6f}")
    print(f"  VERDICT: {'VANISHES' if np.abs(fo).max() < 0.5 else 'NON-ZERO'}")

    print(f"\nSecond-order d²λ/dt²:")
    print(f"  range: [{so.min():.4f}, {so.max():.4f}]")
    print(f"  mean:  {so.mean():.4f}")
    print(f"  VERDICT: {'ALL NEGATIVE (local max)' if np.all(so < 0) else 'SOME POSITIVE (not local max!)'}")

    print(f"\nQuadratic coefficient c (gap ≈ c·t²):")
    print(f"  range: [{cs.min():.4f}, {cs.max():.4f}]")
    print(f"  mean:  {cs.mean():.4f}")

    n_mono = sum(r['monotone'] for r in all_results)
    print(f"\nMonotone decrease: {n_mono}/{n_directions}")

    return all_results, evals_I, evecs_I, lmax_I


def main():
    print("=" * 70)
    print("PART 1: PERTURBATION THEORY AT Q = I")
    print("=" * 70)

    # Phase A: d=2 (fast, comprehensive)
    print("\n\n" + "#" * 70)
    print("# PHASE A: d=2, L=2 (fast lattice)")
    print("#" * 70)
    results_d2, evals_d2, evecs_d2, lmax_d2 = run_perturbation_analysis(
        L=2, d=2, beta=1.0, n_directions=20, label="(Phase A)"
    )

    # Phase B: d=4 (target lattice, fewer directions)
    print("\n\n" + "#" * 70)
    print("# PHASE B: d=4, L=2 (target lattice)")
    print("#" * 70)
    results_d4, evals_d4, evecs_d4, lmax_d4 = run_perturbation_analysis(
        L=2, d=4, beta=1.0, n_directions=5, label="(Phase B)"
    )

    print("\n\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)
    print(f"d=2: λ_max(I) = {lmax_d2:.10f}")
    print(f"d=4: λ_max(I) = {lmax_d4:.10f}")
    print(f"d=2: First order vanishes: {np.abs(np.array([r['Delta_eigs'][-1] for r in results_d2])).max() < 0.5}")
    print(f"d=4: First order vanishes: {np.abs(np.array([r['Delta_eigs'][-1] for r in results_d4])).max() < 0.5}")
    print(f"d=2: All d²λ/dt² < 0: {np.all(np.array([r['d2l_dt2'] for r in results_d2]) < 0)}")
    print(f"d=4: All d²λ/dt² < 0: {np.all(np.array([r['d2l_dt2'] for r in results_d4]) < 0)}")


if __name__ == '__main__':
    main()
