"""
Part 2 & 3: Line scans and gauge orbit verification.

Focuses on d=2 for speed, with targeted d=4 checks.
"""

import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import (Lattice, identity_config, su2_exp, wilson_action,
                          compute_hessian_fd, compute_lmax_actual,
                          perturb_config, random_su2_config,
                          haar_random_su2, apply_gauge_transform)


def gauge_orbit_check(L, d, beta, n_gauge=10):
    """Verify all points on gauge orbit of identity give same λ_max."""
    print(f"\n{'='*60}")
    print(f"GAUGE ORBIT CHECK: L={L}, d={d}")
    print(f"{'='*60}")

    lat = Lattice(L, d)
    Q_I = identity_config(lat)

    lmax_I = compute_lmax_actual(Q_I, lat, beta)
    print(f"λ_max(I) = {lmax_I:.10f}")

    results = []
    for i in range(n_gauge):
        # Random gauge transformation
        g = np.array([haar_random_su2() for _ in range(lat.n_sites)])
        Q_gauge = apply_gauge_transform(Q_I, lat, g)

        # Verify it's still flat: all plaquettes should be I
        max_plaq_dev = 0.0
        for plaq in lat.plaquettes():
            e1, e2, e3, e4 = plaq['edges']
            U_plaq = Q_gauge[e1] @ Q_gauge[e2] @ np.linalg.inv(Q_gauge[e3]) @ np.linalg.inv(Q_gauge[e4])
            dev = norm(U_plaq - np.eye(2))
            max_plaq_dev = max(max_plaq_dev, dev)

        lmax_g = compute_lmax_actual(Q_gauge, lat, beta)
        diff = abs(lmax_g - lmax_I)
        results.append((lmax_g, diff, max_plaq_dev))
        print(f"  Gauge {i+1:2d}: λ_max = {lmax_g:.10f}, "
              f"Δ = {diff:.2e}, max plaq dev = {max_plaq_dev:.2e}")

    max_diff = max(r[1] for r in results)
    print(f"\nMax |Δλ_max| across gauge orbit: {max_diff:.2e}")
    print(f"VERDICT: {'PASS (gauge invariant)' if max_diff < 0.01 else 'FAIL'}")
    return results


def detailed_line_scan(L, d, beta, n_directions=20):
    """Detailed line scans with quadratic fitting."""
    print(f"\n{'='*60}")
    print(f"DETAILED LINE SCANS: L={L}, d={d}")
    print(f"{'='*60}")

    np.random.seed(123)
    lat = Lattice(L, d)
    Q_I = identity_config(lat)
    lmax_I = compute_lmax_actual(Q_I, lat, beta)

    t_fine = np.array([0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, np.pi])

    print(f"λ_max(I) = {lmax_I:.10f}")
    print(f"Testing {n_directions} random directions")
    print(f"t values: {list(t_fine)}")

    all_scans = []
    all_c_values = []

    for idx in range(n_directions):
        delta_Q = np.random.randn(lat.n_links, 3)
        delta_Q = delta_Q / np.sqrt(np.sum(delta_Q**2))

        lmax_vals = []
        for t in t_fine:
            if t == 0.0:
                lmax_vals.append(lmax_I)
            else:
                Q_t = perturb_config(Q_I, delta_Q, t)
                lmax_vals.append(compute_lmax_actual(Q_t, lat, beta))

        lmax_vals = np.array(lmax_vals)
        gaps = lmax_I - lmax_vals

        # Fit gap = c * t^2 using t ≤ 0.05
        mask = (t_fine > 0) & (t_fine <= 0.05)
        if np.sum(mask) > 0:
            t2 = t_fine[mask]**2
            g = gaps[mask]
            c_fit = np.sum(g * t2) / np.sum(t2**2)
        else:
            c_fit = np.nan

        all_scans.append((t_fine.copy(), lmax_vals.copy(), gaps.copy()))
        all_c_values.append(c_fit)

        # Check if λ_max(t) ≤ λ_max(0) for all t
        max_excess = (lmax_vals - lmax_I).max()

        print(f"  Dir {idx+1:2d}: c = {c_fit:8.4f}, "
              f"max_excess = {max_excess:.2e}, "
              f"λ_min_along_scan = {lmax_vals.min():.6f}")

    c_arr = np.array(all_c_values)
    print(f"\nQuadratic coefficient c (gap ≈ c·t²):")
    print(f"  range: [{c_arr.min():.6f}, {c_arr.max():.6f}]")
    print(f"  mean:  {c_arr.mean():.6f}")
    print(f"  std:   {c_arr.std():.6f}")
    print(f"  ALL POSITIVE: {np.all(c_arr > 0)}")

    # Check no direction ever exceeds λ_max(I)
    any_excess = False
    for scan in all_scans:
        if (scan[1] > lmax_I + 1e-6).any():
            any_excess = True
            break
    print(f"\nAny direction exceeds λ_max(I): {any_excess}")
    print(f"VERDICT: {'FLAT IS LOCAL MAX' if not any_excess and np.all(c_arr > 0) else 'NEEDS INVESTIGATION'}")

    return all_scans, all_c_values


def special_perturbation_scans(L, d, beta):
    """Test special structured perturbations, not just random."""
    print(f"\n{'='*60}")
    print(f"SPECIAL PERTURBATION SCANS: L={L}, d={d}")
    print(f"{'='*60}")

    lat = Lattice(L, d)
    Q_I = identity_config(lat)
    lmax_I = compute_lmax_actual(Q_I, lat, beta)
    print(f"λ_max(I) = {lmax_I:.10f}")

    t_vals = [0.0, 0.01, 0.05, 0.1, 0.5, 1.0, np.pi]

    perturbations = []

    # 1. Single-link perturbation (all su(2) directions)
    for a in range(3):
        dQ = np.zeros((lat.n_links, 3))
        dQ[0, a] = 1.0
        perturbations.append((f"single_link_0_T{a+1}", dQ))

    # 2. Uniform perturbation (same rotation on all links in direction mu)
    for mu in range(d):
        dQ = np.zeros((lat.n_links, 3))
        for x in range(lat.n_sites):
            link = lat.link_index(x, mu)
            dQ[link, 0] = 1.0 / np.sqrt(lat.n_sites)
        perturbations.append((f"uniform_dir_{mu}_T1", dQ))

    # 3. Staggered perturbation (alternating sign)
    dQ = np.zeros((lat.n_links, 3))
    for x in range(lat.n_sites):
        parity = sum(lat.coords[x]) % 2
        sign = 1 if parity == 0 else -1
        for mu in range(d):
            link = lat.link_index(x, mu)
            dQ[link, 0] = sign / np.sqrt(lat.n_links)
    perturbations.append(("staggered_T1", dQ))

    # 4. One-hot π rotation (worst case from E001)
    dQ = np.zeros((lat.n_links, 3))
    dQ[0, 0] = 1.0  # will scan up to t=π
    perturbations.append(("one_hot_pi_scan", dQ))

    print(f"\n{'Name':<30s}", end="")
    for t in t_vals:
        print(f" {'t='+str(t):>10s}", end="")
    print()
    print("-" * (30 + 11 * len(t_vals)))

    for name, dQ in perturbations:
        line = f"{name:<30s}"
        for t in t_vals:
            if t == 0.0:
                lv = lmax_I
            else:
                Q_t = perturb_config(Q_I, dQ, t)
                lv = compute_lmax_actual(Q_t, lat, beta)
            line += f" {lv:10.6f}"
        print(line)


def main():
    beta = 1.0

    # d=2 analysis (fast)
    print("\n" + "#"*70)
    print("# d=2, L=2")
    print("#"*70)
    gauge_orbit_check(2, 2, beta, n_gauge=5)
    detailed_line_scan(2, 2, beta, n_directions=20)
    special_perturbation_scans(2, 2, beta)

    # d=3 analysis (medium)
    print("\n" + "#"*70)
    print("# d=3, L=2")
    print("#"*70)
    gauge_orbit_check(2, 3, beta, n_gauge=5)
    detailed_line_scan(2, 3, beta, n_directions=10)

    # d=4 targeted (slow)
    print("\n" + "#"*70)
    print("# d=4, L=2")
    print("#"*70)
    gauge_orbit_check(2, 4, beta, n_gauge=3)
    detailed_line_scan(2, 4, beta, n_directions=3)


if __name__ == '__main__':
    main()
