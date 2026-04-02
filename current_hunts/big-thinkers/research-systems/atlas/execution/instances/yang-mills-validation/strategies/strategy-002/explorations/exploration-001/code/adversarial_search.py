"""
Adversarial search for configurations maximizing r(Q) = λ_max(H_actual)/λ_max(H_formula).

Strategies:
1. Full gradient ascent on d=2 (very fast)
2. Structured adversarial configurations on d=4
3. Nelder-Mead on low-dimensional parameterizations of d=4
4. Coordinate-wise hill climbing on d=4
"""

import numpy as np
from numpy.linalg import eigvalsh, norm, eigh
from scipy.optimize import minimize
import sys
import time

# Import from fast_hessian
sys.path.insert(0, '.')
from fast_hessian import (
    Lattice, su2_exp, haar_random_su2, project_su2,
    adjoint_matrix, T, I2, sigma,
    compute_hessian_fd, compute_hessian_formula,
    compute_ratio_data, wilson_action,
    random_su2_config, near_identity_config, near_abelian_config,
)


def compute_r(Q, lattice, beta, h=1e-4):
    """Compute just r(Q), returning a float."""
    H_a = compute_hessian_fd(Q, lattice, beta, h)
    H_f = compute_hessian_formula(Q, lattice, beta)
    H_a = (H_a + H_a.T) / 2
    H_f = (H_f + H_f.T) / 2
    la = eigvalsh(H_a)[-1]
    lf = eigvalsh(H_f)[-1]
    return la / lf if lf > 1e-15 else float('inf')


# ===================== Strategy 1: Gradient Ascent on d=2 =====================

def gradient_ascent_d2(beta=1.0, n_starts=20, n_steps=300, eta=0.05, delta=5e-3):
    """Full gradient ascent on L=2, d=2 lattice (DOF=24, very fast)."""
    print("=" * 60)
    print("STRATEGY 1: Gradient Ascent on d=2 (L=2)")
    print("=" * 60)

    lat = Lattice(2, 2)
    best_r_global = -1
    best_Q_global = None

    for start in range(n_starts):
        Q = random_su2_config(lat.n_links)
        r_current = compute_r(Q, lat, beta)
        best_r_run = r_current

        for step in range(n_steps):
            grad = np.zeros(lat.n_dof)
            for i in range(lat.n_dof):
                e = i // 3
                a = i % 3
                v = np.zeros(3)
                v[a] = delta
                Q_pert = Q.copy()
                Q_pert[e] = su2_exp(v) @ Q[e]
                r_pert = compute_r(Q_pert, lat, beta)
                grad[i] = (r_pert - r_current) / delta

            grad_norm = norm(grad)
            if grad_norm < 1e-8:
                break

            # Take gradient step
            for i in range(lat.n_dof):
                e = i // 3
                a = i % 3
                v = np.zeros(3)
                v[a] = eta * grad[i]
                Q[e] = su2_exp(v) @ Q[e]
                Q[e] = project_su2(Q[e])

            r_new = compute_r(Q, lat, beta)
            if r_new > best_r_run:
                best_r_run = r_new

            r_current = r_new

            if step % 50 == 0:
                print(f"  Start {start+1}, step {step}: r = {r_current:.8f}, |∇r| = {grad_norm:.6f}")

            if r_current > 1.0:
                print(f"  *** VIOLATION: r = {r_current:.10f} ***")
                break

        print(f"  Start {start+1} best: r = {best_r_run:.8f}")
        if best_r_run > best_r_global:
            best_r_global = best_r_run
            best_Q_global = Q.copy()

    print(f"\nGlobal best r (d=2) = {best_r_global:.10f}")
    print(f"Gap = {1 - best_r_global:.10f}")
    return best_r_global, best_Q_global


# ===================== Strategy 2: Structured Adversarial Configs d=4 =====================

def structured_adversarial_d4(beta=1.0):
    """Try structured configurations designed to be adversarial on d=4."""
    print("\n" + "=" * 60)
    print("STRATEGY 2: Structured Adversarial Configs (d=4)")
    print("=" * 60)

    lat = Lattice(2, 4)
    results = []

    configs = []

    # Type 1: All links the same (maximally symmetric)
    for _ in range(10):
        Q_base = haar_random_su2()
        Q = np.array([Q_base.copy() for _ in range(lat.n_links)])
        configs.append(("uniform", Q))

    # Type 2: Near-identity (small fluctuations)
    for scale in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0]:
        Q = near_identity_config(lat.n_links, scale)
        configs.append((f"near-id(s={scale})", Q))

    # Type 3: Near-abelian (all rotations around T₃)
    for _ in range(5):
        Q = near_abelian_config(lat.n_links)
        configs.append(("abelian", Q))

    # Type 4: Maximally non-abelian — alternating between σ₁ and σ₂ rotations
    for angle in [np.pi/4, np.pi/2, np.pi, 3*np.pi/2]:
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            axis = e % 3  # cycle through T₁, T₂, T₃
            v = np.zeros(3)
            v[axis] = angle
            Q[e] = su2_exp(v)
        configs.append((f"cyclic-axis(θ={angle:.2f})", Q))

    # Type 5: π rotations (Q = exp(πT_a), maximal curvature)
    for a in range(3):
        v = np.zeros(3)
        v[a] = np.pi
        Q_base = su2_exp(v)
        Q = np.array([Q_base.copy() for _ in range(lat.n_links)])
        configs.append((f"pi-rotation(a={a})", Q))

    # Type 6: Checkerboard — alternating identity and a fixed rotation
    Q_rot = haar_random_su2()
    Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
    for e in range(lat.n_links):
        site = e // lat.d
        if sum(lat.coords[site]) % 2 == 0:
            Q[e] = I2.copy()
        else:
            Q[e] = Q_rot.copy()
    configs.append(("checkerboard", Q))

    # Type 7: Random with one extremely non-flat plaquette
    for _ in range(5):
        Q = np.array([I2.copy() for _ in range(lat.n_links)])
        # Pick one plaquette and make it have holonomy = -I
        plaq = lat.plaquettes()[0]
        e1 = plaq['edges'][0]
        Q[e1] = su2_exp(np.array([np.pi, 0, 0]))
        configs.append(("one-hot-pi", Q))

    # Type 8: Correlated per direction
    for _ in range(5):
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        dir_Q = [haar_random_su2() for _ in range(lat.d)]
        for e in range(lat.n_links):
            mu = e % lat.d
            Q[e] = dir_Q[mu].copy()
        configs.append(("per-direction", Q))

    # Run all
    best_r = -1
    best_label = ""
    for label, Q in configs:
        t0 = time.time()
        r = compute_r(Q, lat, beta)
        dt = time.time() - t0
        results.append((label, r))
        status = "*** VIOLATION ***" if r > 1.0 else ""
        print(f"  {label:30s}: r = {r:.8f} ({dt:.1f}s) {status}")
        if r > best_r:
            best_r = r
            best_label = label

    print(f"\nBest structured adversarial: r = {best_r:.8f} ({best_label})")
    return results, best_r


# ===================== Strategy 3: Nelder-Mead on parameterized Q =====================

def nelder_mead_per_direction(beta=1.0, d=4):
    """Parameterize Q by per-direction SU(2) (4d×3 = 12 params for d=4)."""
    print("\n" + "=" * 60)
    print(f"STRATEGY 3a: Nelder-Mead per-direction (d={d})")
    print("=" * 60)

    lat = Lattice(2, d)

    def params_to_Q(params):
        """params: shape (d, 3) → Q on all links."""
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            mu = e % lat.d
            Q[e] = su2_exp(params[mu])
        return Q

    def neg_r(flat_params):
        params = flat_params.reshape(lat.d, 3)
        Q = params_to_Q(params)
        return -compute_r(Q, lat, beta)

    best_r = -1
    n_evals = [0]

    def callback(xk):
        nonlocal best_r
        r = -neg_r(xk)
        n_evals[0] += 1
        if r > best_r:
            best_r = r
            if n_evals[0] % 10 == 0:
                print(f"  Eval {n_evals[0]}: best r = {best_r:.8f}")

    for trial in range(5):
        x0 = np.random.randn(lat.d * 3) * 2.0
        print(f"  Trial {trial+1}...")
        result = minimize(neg_r, x0, method='Nelder-Mead',
                         options={'maxfev': 200, 'xatol': 1e-4, 'fatol': 1e-6})
        r_val = -result.fun
        print(f"  Trial {trial+1}: r = {r_val:.8f} (evals={result.nfev})")
        if r_val > best_r:
            best_r = r_val

    print(f"\nBest r (per-direction NM) = {best_r:.8f}")
    return best_r


def nelder_mead_uniform(beta=1.0, d=4):
    """Parameterize Q by a single SU(2) for all links (3 params)."""
    print("\n" + "=" * 60)
    print(f"STRATEGY 3b: Nelder-Mead uniform (d={d})")
    print("=" * 60)

    lat = Lattice(2, d)

    def neg_r(params):
        Q_base = su2_exp(params)
        Q = np.array([Q_base.copy() for _ in range(lat.n_links)])
        return -compute_r(Q, lat, beta)

    best_r = -1
    for trial in range(10):
        x0 = np.random.randn(3) * np.pi
        result = minimize(neg_r, x0, method='Nelder-Mead',
                         options={'maxfev': 100, 'xatol': 1e-4, 'fatol': 1e-6})
        r_val = -result.fun
        print(f"  Trial {trial+1}: r = {r_val:.8f}")
        if r_val > best_r:
            best_r = r_val

    print(f"\nBest r (uniform NM) = {best_r:.8f}")
    return best_r


def nelder_mead_per_site(beta=1.0, d=4):
    """Parameterize Q by per-site SU(2) (16 sites × 3 = 48 params)."""
    print("\n" + "=" * 60)
    print(f"STRATEGY 3c: Nelder-Mead per-site (d={d})")
    print("=" * 60)

    lat = Lattice(2, d)

    def params_to_Q(params):
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            site = e // lat.d
            Q[e] = su2_exp(params[site])
        return Q

    def neg_r(flat_params):
        params = flat_params.reshape(lat.n_sites, 3)
        Q = params_to_Q(params)
        return -compute_r(Q, lat, beta)

    best_r = -1
    for trial in range(3):
        x0 = np.random.randn(lat.n_sites * 3) * 2.0
        print(f"  Trial {trial+1}...")
        result = minimize(neg_r, x0, method='Powell',
                         options={'maxfev': 500, 'xtol': 1e-4, 'ftol': 1e-6})
        r_val = -result.fun
        print(f"  Trial {trial+1}: r = {r_val:.8f} (evals={result.nfev})")
        if r_val > best_r:
            best_r = r_val

    print(f"\nBest r (per-site Powell) = {best_r:.8f}")
    return best_r


# ===================== Strategy 4: Hill Climbing on d=4 =====================

def hill_climbing_d4(beta=1.0, n_starts=5, n_steps=100, step_size=0.3):
    """Random perturbation hill climbing on full d=4 config space."""
    print("\n" + "=" * 60)
    print(f"STRATEGY 4: Hill Climbing on d=4 ({n_starts} starts, {n_steps} steps)")
    print("=" * 60)

    lat = Lattice(2, 4)
    best_r_global = -1

    for start in range(n_starts):
        Q = random_su2_config(lat.n_links)
        r_current = compute_r(Q, lat, beta)
        print(f"  Start {start+1}: initial r = {r_current:.8f}")

        for step in range(n_steps):
            # Randomly perturb one link
            e = np.random.randint(lat.n_links)
            v = step_size * np.random.randn(3)
            Q_trial = Q.copy()
            Q_trial[e] = su2_exp(v) @ Q[e]
            Q_trial[e] = project_su2(Q_trial[e])

            r_trial = compute_r(Q_trial, lat, beta)

            if r_trial > r_current:
                Q = Q_trial
                r_current = r_trial

            if step % 25 == 0:
                print(f"    Step {step}: r = {r_current:.8f}")

            if r_current > 1.0:
                print(f"    *** VIOLATION: r = {r_current:.10f} ***")
                break

        print(f"  Start {start+1} best: r = {r_current:.8f}")
        if r_current > best_r_global:
            best_r_global = r_current

    print(f"\nGlobal best r (hill climbing d=4) = {best_r_global:.10f}")
    return best_r_global


# ===================== Strategy 5: Gradient Ascent on d=4 =====================

def gradient_ascent_d4(beta=1.0, n_starts=3, n_steps=30, eta=0.02, delta=5e-3):
    """Gradient ascent on d=4 — expensive but definitive."""
    print("\n" + "=" * 60)
    print(f"STRATEGY 5: Gradient Ascent on d=4 ({n_starts} starts, {n_steps} steps)")
    print("=" * 60)

    lat = Lattice(2, 4)
    best_r_global = -1

    for start in range(n_starts):
        Q = random_su2_config(lat.n_links)
        r_current = compute_r(Q, lat, beta)
        print(f"\n  Start {start+1}: initial r = {r_current:.8f}")
        t_start = time.time()

        for step in range(n_steps):
            t_step = time.time()
            # Compute gradient via forward differences
            grad = np.zeros((lat.n_links, 3))
            for e in range(lat.n_links):
                for a in range(3):
                    v = np.zeros(3)
                    v[a] = delta
                    Q_pert = Q.copy()
                    Q_pert[e] = su2_exp(v) @ Q[e]
                    r_pert = compute_r(Q_pert, lat, beta)
                    grad[e, a] = (r_pert - r_current) / delta

            grad_norm = norm(grad)
            if grad_norm < 1e-8:
                print(f"    Gradient vanished at step {step}")
                break

            # Take step
            for e in range(lat.n_links):
                v = eta * grad[e]
                Q[e] = su2_exp(v) @ Q[e]
                Q[e] = project_su2(Q[e])

            r_new = compute_r(Q, lat, beta)
            dt = time.time() - t_step
            print(f"    Step {step}: r = {r_new:.8f}, |∇r| = {grad_norm:.6f} ({dt:.1f}s)")

            r_current = r_new
            if r_current > 1.0:
                print(f"    *** VIOLATION: r = {r_current:.10f} ***")
                break

        elapsed = time.time() - t_start
        print(f"  Start {start+1} final: r = {r_current:.8f} ({elapsed:.0f}s)")
        if r_current > best_r_global:
            best_r_global = r_current

    print(f"\nGlobal best r (gradient ascent d=4) = {best_r_global:.10f}")
    return best_r_global


# ===================== Main =====================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', type=int, default=0, help='0=all, 1-5=specific')
    args = parser.parse_args()

    np.random.seed(42)
    beta = 1.0

    if args.strategy == 0 or args.strategy == 1:
        r1, Q1 = gradient_ascent_d2(beta, n_starts=10, n_steps=200, eta=0.05, delta=5e-3)

    if args.strategy == 0 or args.strategy == 2:
        res2, r2 = structured_adversarial_d4(beta)

    if args.strategy == 0 or args.strategy == 3:
        r3a = nelder_mead_uniform(beta)
        r3b = nelder_mead_per_direction(beta)

    if args.strategy == 0 or args.strategy == 4:
        r4 = hill_climbing_d4(beta, n_starts=5, n_steps=200, step_size=0.3)

    if args.strategy == 0 or args.strategy == 5:
        r5 = gradient_ascent_d4(beta, n_starts=2, n_steps=20, eta=0.02)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_rs = []
    if args.strategy in [0, 1]:
        print(f"  Gradient ascent d=2: r = {r1:.8f}")
        all_rs.append(r1)
    if args.strategy in [0, 2]:
        print(f"  Structured d=4: r = {r2:.8f}")
        all_rs.append(r2)
    if args.strategy in [0, 3]:
        print(f"  NM uniform d=4: r = {r3a:.8f}")
        print(f"  NM per-dir d=4: r = {r3b:.8f}")
        all_rs.extend([r3a, r3b])
    if args.strategy in [0, 4]:
        print(f"  Hill climbing d=4: r = {r4:.8f}")
        all_rs.append(r4)
    if args.strategy in [0, 5]:
        print(f"  Gradient ascent d=4: r = {r5:.8f}")
        all_rs.append(r5)
    if all_rs:
        print(f"\n  Overall max r = {max(all_rs):.10f}")
        print(f"  Gap = {1 - max(all_rs):.10f}")
