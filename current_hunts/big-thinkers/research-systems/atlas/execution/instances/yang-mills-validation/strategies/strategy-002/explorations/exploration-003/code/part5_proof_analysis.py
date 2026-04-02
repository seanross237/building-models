"""
Part 5: Toward a Rigorous Proof

Key analytical questions:
1. Can we decompose H_actual(Q) = H_actual(I) + D(Q) with D(Q) ≼ 0?
2. What is the structure of H_actual(I) - H_actual(Q)?
3. Can we bound λ_max(H_actual(Q)) ≤ λ_max(H_actual(I)) using:
   a. The Weitzenböck-type identity
   b. Concavity of λ_max in some parameterization
   c. A gauge-theoretic argument

Numerical investigation: compute D(Q) = H_actual(I) - H_actual(Q) for various Q
and check whether D(Q) ≽ 0 (i.e., all eigenvalues ≥ 0).
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *


def analyze_D_matrix(L, d, beta, n_configs=20):
    """
    For various Q, compute D(Q) = H_actual(I) - H_actual(Q).
    If D(Q) ≽ 0 for all Q, then H_actual(Q) ≼ H_actual(I) in the Loewner order,
    which implies λ_max(H_actual(Q)) ≤ λ_max(H_actual(I)).
    """
    lat = Lattice(L, d)
    Q_I = identity_config(lat)

    print(f"Lattice: L={L}, d={d}, DOF={lat.n_dof}")

    # Compute H at identity
    print("Computing H_actual(I)...")
    H_I = compute_hessian_fd(Q_I, lat, beta)
    H_I = (H_I + H_I.T) / 2
    lmax_I = eigvalsh(H_I)[-1]
    print(f"λ_max(I) = {lmax_I:.10f}")

    np.random.seed(42)

    print(f"\n{'Config':<25s} {'min(D)':>10s} {'max(D)':>10s} {'D≽0?':>6s} "
          f"{'λmax(Q)':>10s} {'gap':>10s}")
    print("-" * 80)

    results = []

    configs = []
    # Haar random
    for i in range(8):
        configs.append((f"Haar random {i+1}", random_su2_config(lat)))

    # Near flat
    for scale in [0.01, 0.05, 0.1, 0.5, 1.0]:
        Q = identity_config(lat)
        for e in range(lat.n_links):
            v = np.random.randn(3) * scale
            Q[e] = su2_exp(v) @ Q[e]
        configs.append((f"Near flat ε={scale}", Q))

    # One-hot perturbations
    for angle in [0.1, 0.5, np.pi/2, np.pi]:
        Q = identity_config(lat)
        v = np.zeros(3); v[0] = angle
        Q[0] = su2_exp(v) @ Q[0]
        configs.append((f"One-hot θ={angle:.2f}", Q))

    # Structured: all links same rotation
    for angle in [0.1, 0.5, 1.0]:
        Q = identity_config(lat)
        for e in range(lat.n_links):
            v = np.zeros(3); v[0] = angle
            Q[e] = su2_exp(v) @ Q[e]
        configs.append((f"Uniform θ={angle:.1f}", Q))

    for name, Q in configs:
        H_Q = compute_hessian_fd(Q, lat, beta)
        H_Q = (H_Q + H_Q.T) / 2
        D = H_I - H_Q

        D_eigs = eigvalsh(D)
        d_min = D_eigs[0]
        d_max = D_eigs[-1]
        psd = d_min >= -1e-6

        lmax_Q = eigvalsh(H_Q)[-1]
        gap = lmax_I - lmax_Q

        results.append({
            'name': name,
            'd_min': d_min,
            'd_max': d_max,
            'psd': psd,
            'lmax_Q': lmax_Q,
            'gap': gap,
        })

        print(f"{name:<25s} {d_min:10.6f} {d_max:10.6f} {'YES' if psd else 'NO':>6s} "
              f"{lmax_Q:10.6f} {gap:10.6f}")

    # Summary
    n_psd = sum(r['psd'] for r in results)
    n_total = len(results)
    all_gap_positive = all(r['gap'] > -1e-6 for r in results)

    print(f"\n{'='*60}")
    print(f"SUMMARY: D(Q) = H(I) - H(Q) Analysis")
    print(f"{'='*60}")
    print(f"D(Q) ≽ 0 (PSD): {n_psd}/{n_total}")
    print(f"λ_max(I) ≥ λ_max(Q) for all Q: {all_gap_positive}")

    if n_psd == n_total:
        print(f"\n*** D(Q) is PSD for ALL configs tested! ***")
        print(f"This means H_actual(Q) ≼ H_actual(I) in Loewner order.")
        print(f"If proved analytically, this gives: λ_max(H(Q)) ≤ λ_max(H(I)) = {lmax_I:.6f}")
    elif all_gap_positive and n_psd < n_total:
        print(f"\nD(Q) is NOT always PSD, but λ_max inequality still holds.")
        print(f"The Loewner order argument would be too strong — need a weaker argument.")

    return results


def investigate_D_structure(L, d, beta):
    """Deeper investigation of D(Q) for near-flat configs."""
    lat = Lattice(L, d)
    Q_I = identity_config(lat)

    H_I = compute_hessian_fd(Q_I, lat, beta)
    H_I = (H_I + H_I.T) / 2

    # For near-flat Q(ε) = exp(ε·δQ)·I, compute D(ε) = H(I) - H(Q(ε))
    # and check how D(ε) scales with ε
    print(f"\n{'='*60}")
    print(f"D(Q) SCALING ANALYSIS: L={L}, d={d}")
    print(f"{'='*60}")

    np.random.seed(77)
    delta_Q = np.random.randn(lat.n_links, 3)
    delta_Q = delta_Q / np.sqrt(np.sum(delta_Q**2))

    epsilons = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

    print(f"\n{'ε':>8s} {'min(D)/ε²':>12s} {'max(D)/ε²':>12s} {'D≽0?':>6s} "
          f"{'||D||/ε²':>12s} {'#neg eigs':>10s}")
    print("-" * 70)

    for eps in epsilons:
        Q_eps = perturb_config(Q_I, delta_Q, eps)
        H_eps = compute_hessian_fd(Q_eps, lat, beta)
        H_eps = (H_eps + H_eps.T) / 2
        D = H_I - H_eps

        D_eigs = eigvalsh(D)
        d_min = D_eigs[0]
        d_max = D_eigs[-1]
        D_norm = norm(D, 2)
        psd = d_min >= -1e-6
        n_neg = np.sum(D_eigs < -1e-8)

        print(f"{eps:8.4f} {d_min/eps**2:12.6f} {d_max/eps**2:12.6f} "
              f"{'YES' if psd else 'NO':>6s} {D_norm/eps**2:12.6f} {n_neg:10d}")

    return


def main():
    beta = 1.0

    # d=2 analysis
    print("#" * 70)
    print("# d=2, L=2")
    print("#" * 70)
    results_d2 = analyze_D_matrix(2, 2, beta)
    investigate_D_structure(2, 2, beta)

    # d=3 analysis (if fast enough)
    print("\n\n" + "#" * 70)
    print("# d=3, L=2")
    print("#" * 70)
    results_d3 = analyze_D_matrix(2, 3, beta, n_configs=10)


if __name__ == '__main__':
    main()
