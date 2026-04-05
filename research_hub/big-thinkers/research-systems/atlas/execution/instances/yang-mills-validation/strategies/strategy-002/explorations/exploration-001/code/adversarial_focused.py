"""
Focused adversarial search — combining the most effective strategies.
1. Gradient ascent on d=2 (fast, thorough)
2. Hill climbing on d=4 starting from near-identity configs (where r is closest to 1)
3. Nelder-Mead on full d=4 with per-link parameterization
"""
import numpy as np
from numpy.linalg import eigvalsh, norm, eigh
from scipy.optimize import minimize
import sys
import time

sys.path.insert(0, '.')
from fast_hessian import (
    Lattice, su2_exp, haar_random_su2, project_su2,
    T, I2, compute_hessian_fd, compute_hessian_formula,
    compute_ratio_data, random_su2_config,
)

def compute_r(Q, lattice, beta, h=1e-4):
    H_a = compute_hessian_fd(Q, lattice, beta, h)
    H_f = compute_hessian_formula(Q, lattice, beta)
    H_a = (H_a + H_a.T) / 2
    H_f = (H_f + H_f.T) / 2
    la = eigvalsh(H_a)[-1]
    lf = eigvalsh(H_f)[-1]
    return la / lf if lf > 1e-15 else float('inf')


# ===================== Part 1: d=2 Gradient Ascent =====================

def d2_gradient_ascent():
    print("=" * 60)
    print("Part 1: Gradient Ascent d=2 (L=2, DOF=24)")
    print("=" * 60)

    lat = Lattice(2, 2)
    beta = 1.0
    best_r_overall = -1

    # 10 starts from random
    for start in range(10):
        Q = random_su2_config(lat.n_links)
        r = compute_r(Q, lat, beta)
        best_r = r

        for step in range(200):
            delta = 5e-3
            eta = 0.05
            grad = np.zeros(lat.n_dof)

            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = delta
                Q_p = Q.copy()
                Q_p[e] = su2_exp(v) @ Q[e]
                r_p = compute_r(Q_p, lat, beta)
                grad[i] = (r_p - r) / delta

            gn = norm(grad)
            if gn < 1e-8:
                break

            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = eta * grad[i]
                Q[e] = su2_exp(v) @ Q[e]
                Q[e] = project_su2(Q[e])

            r = compute_r(Q, lat, beta)
            best_r = max(best_r, r)

            if step % 50 == 0:
                print(f"  Start {start+1}, step {step}: r={r:.8f} |∇|={gn:.4f}")

        print(f"  Start {start+1} final: r={best_r:.8f}")
        best_r_overall = max(best_r_overall, best_r)

    # 5 starts from near-identity (where r is close to 1)
    print("\n  Near-identity starts:")
    for start in range(5):
        scale = 0.01
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            Q[e] = su2_exp(scale * np.random.randn(3))
        r = compute_r(Q, lat, beta)
        best_r = r

        for step in range(200):
            delta = 2e-3
            eta = 0.01
            grad = np.zeros(lat.n_dof)

            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = delta
                Q_p = Q.copy()
                Q_p[e] = su2_exp(v) @ Q[e]
                r_p = compute_r(Q_p, lat, beta)
                grad[i] = (r_p - r) / delta

            gn = norm(grad)
            if gn < 1e-8:
                break

            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = eta * grad[i]
                Q[e] = su2_exp(v) @ Q[e]
                Q[e] = project_su2(Q[e])

            r = compute_r(Q, lat, beta)
            best_r = max(best_r, r)

            if step % 50 == 0:
                print(f"  NI start {start+1}, step {step}: r={r:.8f} |∇|={gn:.4f}")

        print(f"  NI start {start+1} final: r={best_r:.8f}")
        best_r_overall = max(best_r_overall, best_r)

    print(f"\n  d=2 overall best: r = {best_r_overall:.10f}, gap = {1-best_r_overall:.10f}")
    return best_r_overall


# ===================== Part 2: d=4 Hill Climbing from Near-Identity =====================

def d4_near_id_hill_climbing():
    print("\n" + "=" * 60)
    print("Part 2: Hill Climbing d=4 from Near-Identity Configs")
    print("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r_overall = -1

    for trial, scale in enumerate([0.005, 0.01, 0.02, 0.05]):
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        np.random.seed(42 + trial)
        for e in range(lat.n_links):
            Q[e] = su2_exp(scale * np.random.randn(3))
        r = compute_r(Q, lat, beta)
        print(f"\n  Scale={scale}: initial r={r:.8f}")
        best_r = r

        for step in range(150):
            # Random perturbation of one link
            e = np.random.randint(lat.n_links)
            step_size = 0.01 * (1 + np.random.rand())  # keep perturbations small near identity
            v = step_size * np.random.randn(3)
            Q_trial = Q.copy()
            Q_trial[e] = su2_exp(v) @ Q[e]
            Q_trial[e] = project_su2(Q_trial[e])

            r_trial = compute_r(Q_trial, lat, beta)

            if r_trial > r:
                Q = Q_trial
                r = r_trial
                if r > best_r:
                    best_r = r

            if step % 50 == 0:
                print(f"    Step {step}: r={r:.8f}")

        print(f"  Scale={scale} final: r={best_r:.8f}")
        best_r_overall = max(best_r_overall, best_r)

    print(f"\n  d=4 NI hill climbing best: r = {best_r_overall:.10f}, gap = {1-best_r_overall:.10f}")
    return best_r_overall


# ===================== Part 3: d=4 Nelder-Mead Full Parameterization =====================

def d4_nelder_mead_full():
    print("\n" + "=" * 60)
    print("Part 3: Nelder-Mead d=4 Full Parameterization (192 params)")
    print("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0

    call_count = [0]
    best_r = [0]

    def neg_r(flat_params):
        call_count[0] += 1
        params = flat_params.reshape(lat.n_links, 3)
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            Q[e] = su2_exp(params[e])
        r = compute_r(Q, lat, beta)
        if r > best_r[0]:
            best_r[0] = r
        if call_count[0] % 50 == 0:
            print(f"    Eval {call_count[0]}: best r = {best_r[0]:.8f}")
        return -r

    # Start from small perturbation around identity
    for trial in range(3):
        scale = 0.02
        x0 = scale * np.random.randn(lat.n_links * 3)
        call_count[0] = 0
        best_r[0] = 0
        print(f"\n  Trial {trial+1} (initial scale={scale})...")
        result = minimize(neg_r, x0, method='Powell',
                         options={'maxfev': 300, 'xtol': 1e-4, 'ftol': 1e-6})
        print(f"  Trial {trial+1}: r = {-result.fun:.8f} (evals={result.nfev})")

    print(f"\n  NM full best: r = {best_r[0]:.10f}, gap = {1-best_r[0]:.10f}")
    return best_r[0]


# ===================== Part 4: Characterize Worst Case =====================

def characterize_worst_case():
    print("\n" + "=" * 60)
    print("Part 4: Detailed Characterization")
    print("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0

    # The worst non-flat case from Stage 2 was around r=0.66 for Haar random.
    # Near-identity at scale=0.01 gives r ≈ 0.9999.
    # Let's find the sweet spot that maximizes r among genuinely non-flat configs.

    print("\nSweep of near-identity scales (5 samples each):")
    print(f"{'scale':>8s} {'mean(r)':>12s} {'max(r)':>12s} {'gap':>12s}")

    best_r_all = 0
    for scale in [0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1]:
        rs = []
        for _ in range(5):
            Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
            for e in range(lat.n_links):
                Q[e] = su2_exp(scale * np.random.randn(3))
            r = compute_r(Q, lat, beta)
            rs.append(r)
        mean_r = np.mean(rs)
        max_r = np.max(rs)
        best_r_all = max(best_r_all, max_r)
        print(f"  {scale:8.4f} {mean_r:12.10f} {max_r:12.10f} {1-max_r:12.10f}")

    # Detailed analysis of the worst-case config (near identity, small scale)
    print("\n\nDetailed analysis of near-identity worst case:")
    np.random.seed(777)
    scale = 0.01
    Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
    for e in range(lat.n_links):
        Q[e] = su2_exp(scale * np.random.randn(3))

    res = compute_ratio_data(Q, lat, beta)
    print(f"r = {res['r']:.10f}")
    print(f"λ_max(H_actual) = {res['lmax_actual']:.10f}")
    print(f"λ_max(H_formula) = {res['lmax_formula']:.10f}")
    print(f"||C||_op = {res['C_norm']:.10f}")
    print(f"C eigenvalue range: [{res['C_min_eig']:.6f}, {res['C_max_eig']:.6f}]")
    print(f"C positive eigenvalues: {res['C_n_positive']}")
    print(f"C negative eigenvalues: {res['C_n_negative']}")

    # Alignment analysis
    _, vecs = eigh(res['H_actual'])
    v_top = vecs[:, -1]

    C = res['H_formula'] - res['H_actual']
    cv = v_top @ C @ v_top
    ha_v = v_top @ res['H_actual'] @ v_top
    hf_v = v_top @ res['H_formula'] @ v_top

    print(f"\nTop eigenvector analysis:")
    print(f"v_top^T H_actual v_top = {ha_v:.10f}")
    print(f"v_top^T H_formula v_top = {hf_v:.10f}")
    print(f"v_top^T C v_top = {cv:.10f}")
    print(f"r_vmax = H_actual/H_formula on v_top = {ha_v/hf_v:.10f}")


if __name__ == '__main__':
    r1 = d2_gradient_ascent()
    r2 = d4_near_id_hill_climbing()
    r3 = d4_nelder_mead_full()
    characterize_worst_case()

    print("\n" + "=" * 60)
    print("GRAND SUMMARY")
    print("=" * 60)
    print(f"  d=2 gradient ascent:     r = {r1:.10f}, gap = {1-r1:.10f}")
    print(f"  d=4 NI hill climbing:    r = {r2:.10f}, gap = {1-r2:.10f}")
    print(f"  d=4 NM full:             r = {r3:.10f}, gap = {1-r3:.10f}")
    overall = max(r1, r2, r3)
    print(f"\n  Overall max r = {overall:.10f}")
    print(f"  Overall gap   = {1-overall:.10f}")
    print(f"\n  VERDICT: {'PASS — inequality holds' if overall < 1.001 else 'FAIL'}")
