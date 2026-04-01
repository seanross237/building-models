"""
Final targeted adversarial search for max r(Q).
Focus on the most promising directions:
1. Nelder-Mead on per-direction parameterization (12 params, d=4)
2. One-link perturbation sweep (optimize angle of single link from identity)
3. Two-link perturbation (pairs of links)
4. Final d=4 hill climbing (more steps, bigger perturbations)
"""
import numpy as np
from numpy.linalg import eigvalsh, norm, eigh
from scipy.optimize import minimize, minimize_scalar
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

def pr(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def nelder_mead_per_direction():
    """12-parameter optimization: one SU(2) element per lattice direction."""
    pr("=" * 60)
    pr("Nelder-Mead per-direction (12 params, d=4)")
    pr("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r = 0

    for trial in range(8):
        np.random.seed(300 + trial)

        def neg_r(params):
            p = params.reshape(4, 3)
            Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
            for e in range(lat.n_links):
                Q[e] = su2_exp(p[e % lat.d])
            return -compute_r(Q, lat, beta)

        x0 = np.random.randn(12) * (0.3 if trial < 4 else 1.5)
        result = minimize(neg_r, x0, method='Nelder-Mead',
                         options={'maxfev': 300, 'xatol': 1e-4, 'fatol': 1e-6})
        r = -result.fun
        pr(f"  Trial {trial+1}: r = {r:.8f} (evals={result.nfev})")
        best_r = max(best_r, r)

    pr(f"\nBest r (NM per-dir) = {best_r:.10f}, gap = {1-best_r:.10f}")
    return best_r


def one_link_angle_sweep():
    """Optimize the angle of a single link perturbation from identity."""
    pr("\n" + "=" * 60)
    pr("One-link angle sweep (d=4)")
    pr("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r = 0

    # For each of the 3 color directions, optimize the angle
    for axis in range(3):
        def neg_r_angle(angle):
            Q = np.array([I2.copy() for _ in range(lat.n_links)])
            v = np.zeros(3); v[axis] = angle
            Q[0] = su2_exp(v)
            return -compute_r(Q, lat, beta)

        # Bracket search
        result = minimize_scalar(neg_r_angle, bounds=(0.01, np.pi), method='bounded',
                                options={'xatol': 1e-3, 'maxiter': 30})
        r = -result.fun
        pr(f"  Axis {axis}: best angle = {result.x:.4f}, r = {r:.8f}")
        best_r = max(best_r, r)

    # Now try optimizing which link and the full 3D angle
    pr("\n  Optimizing link + angle jointly:")
    for link_idx in [0, 1, 4, 16, 32]:  # Sample different links
        def neg_r_3d(v):
            Q = np.array([I2.copy() for _ in range(lat.n_links)])
            Q[link_idx] = su2_exp(v)
            return -compute_r(Q, lat, beta)

        x0 = np.array([np.pi/2, 0, 0])
        result = minimize(neg_r_3d, x0, method='Nelder-Mead',
                         options={'maxfev': 100, 'xatol': 1e-3})
        r = -result.fun
        pr(f"  Link {link_idx}: r = {r:.8f}")
        best_r = max(best_r, r)

    pr(f"\nBest r (one-link) = {best_r:.10f}, gap = {1-best_r:.10f}")
    return best_r


def two_link_perturbation():
    """Perturb two links from identity, optimize angles."""
    pr("\n" + "=" * 60)
    pr("Two-link perturbation (d=4)")
    pr("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r = 0

    # Try pairs of links that share a plaquette (neighboring)
    link_pairs = [(0, 1), (0, 4), (0, lat.n_links-1)]
    # Also try pairs that are far apart
    link_pairs += [(0, 32), (0, 48), (16, 48)]

    for e1, e2 in link_pairs:
        def neg_r_6d(params):
            Q = np.array([I2.copy() for _ in range(lat.n_links)])
            Q[e1] = su2_exp(params[:3])
            Q[e2] = su2_exp(params[3:])
            return -compute_r(Q, lat, beta)

        x0 = np.array([np.pi/2, 0, 0, 0, np.pi/2, 0])
        result = minimize(neg_r_6d, x0, method='Nelder-Mead',
                         options={'maxfev': 200, 'xatol': 1e-3})
        r = -result.fun
        pr(f"  Links ({e1},{e2}): r = {r:.8f} (evals={result.nfev})")
        best_r = max(best_r, r)

    pr(f"\nBest r (two-link) = {best_r:.10f}, gap = {1-best_r:.10f}")
    return best_r


def hill_climbing_final():
    """Hill climbing with larger perturbations and mixed strategies."""
    pr("\n" + "=" * 60)
    pr("Hill Climbing d=4 (3 starts × 300 steps, mixed)")
    pr("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r_global = 0

    np.random.seed(555)
    for start in range(3):
        Q = random_su2_config(lat.n_links)
        r = compute_r(Q, lat, beta)
        pr(f"  Start {start+1}: initial r={r:.8f}")

        for step in range(300):
            # Mix strategies: single link, multi-link, and direction-aligned
            strategy = np.random.choice(['single', 'multi', 'direction'], p=[0.5, 0.3, 0.2])

            Q_trial = Q.copy()
            if strategy == 'single':
                e = np.random.randint(lat.n_links)
                v = 0.4 * np.random.randn(3)
                Q_trial[e] = su2_exp(v) @ Q[e]
                Q_trial[e] = project_su2(Q_trial[e])
            elif strategy == 'multi':
                n_perturb = np.random.randint(2, 8)
                for _ in range(n_perturb):
                    e = np.random.randint(lat.n_links)
                    v = 0.2 * np.random.randn(3)
                    Q_trial[e] = su2_exp(v) @ Q[e]
                    Q_trial[e] = project_su2(Q_trial[e])
            else:  # direction
                mu = np.random.randint(lat.d)
                v = 0.3 * np.random.randn(3)
                for e in range(lat.n_links):
                    if e % lat.d == mu:
                        Q_trial[e] = su2_exp(v) @ Q[e]
                        Q_trial[e] = project_su2(Q_trial[e])

            r_trial = compute_r(Q_trial, lat, beta)
            if r_trial > r:
                Q, r = Q_trial, r_trial

            if step % 100 == 0:
                pr(f"    Step {step}: r={r:.8f}")

        pr(f"  Start {start+1} best: r={r:.8f}")
        best_r_global = max(best_r_global, r)

    pr(f"\nHill climbing best: r = {best_r_global:.10f}, gap = {1-best_r_global:.10f}")
    return best_r_global


if __name__ == '__main__':
    t0 = time.time()

    r1 = nelder_mead_per_direction()
    r2 = one_link_angle_sweep()
    r3 = two_link_perturbation()
    r4 = hill_climbing_final()

    overall = max(r1, r2, r3, r4)
    pr("\n" + "=" * 60)
    pr("FINAL ADVERSARIAL SUMMARY")
    pr("=" * 60)
    pr(f"  NM per-direction: r = {r1:.10f}")
    pr(f"  One-link opt:     r = {r2:.10f}")
    pr(f"  Two-link opt:     r = {r3:.10f}")
    pr(f"  Hill climbing:    r = {r4:.10f}")
    pr(f"\n  Overall max r = {overall:.10f}")
    pr(f"  Overall gap   = {1 - overall:.10f}")
    pr(f"  Total time: {time.time()-t0:.0f}s")
    pr(f"\n  VERDICT: {'INEQUALITY HOLDS (PASS)' if overall < 1.001 else 'VIOLATION (FAIL)'}")
