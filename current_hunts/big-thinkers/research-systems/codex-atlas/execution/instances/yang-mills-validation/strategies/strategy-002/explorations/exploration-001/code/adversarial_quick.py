"""
Quick adversarial search — d=2 gradient ascent + d=4 hill climbing.
Runs with unbuffered output.
"""
import numpy as np
from numpy.linalg import eigvalsh, norm
import sys
import time

sys.path.insert(0, '.')
from fast_hessian import (
    Lattice, su2_exp, haar_random_su2, project_su2,
    T, I2, compute_hessian_fd, compute_hessian_formula,
    random_su2_config,
)

def compute_r(Q, lattice, beta, h=1e-4):
    H_a = compute_hessian_fd(Q, lattice, beta, h)
    H_f = compute_hessian_formula(Q, lattice, beta)
    H_a = (H_a + H_a.T) / 2
    H_f = (H_f + H_f.T) / 2
    la = eigvalsh(H_a)[-1]
    lf = eigvalsh(H_f)[-1]
    return la / lf if lf > 1e-15 else float('inf')


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def d2_gradient_ascent():
    flush_print("=" * 60)
    flush_print("d=2 Gradient Ascent (5 starts × 150 steps)")
    flush_print("=" * 60)

    lat = Lattice(2, 2)
    beta = 1.0
    best_r_global = -1

    np.random.seed(42)
    for start in range(5):
        Q = random_su2_config(lat.n_links)
        r = compute_r(Q, lat, beta)
        best_r = r

        for step in range(150):
            delta, eta = 5e-3, 0.05
            grad = np.zeros(lat.n_dof)
            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = delta
                Q_p = Q.copy(); Q_p[e] = su2_exp(v) @ Q[e]
                grad[i] = (compute_r(Q_p, lat, beta) - r) / delta

            gn = norm(grad)
            if gn < 1e-8: break

            for i in range(lat.n_dof):
                e, a = i // 3, i % 3
                v = np.zeros(3); v[a] = eta * grad[i]
                Q[e] = su2_exp(v) @ Q[e]; Q[e] = project_su2(Q[e])

            r = compute_r(Q, lat, beta)
            best_r = max(best_r, r)
            if step % 30 == 0:
                flush_print(f"  Start {start+1}, step {step}: r={r:.8f} |∇|={gn:.4f}")

        flush_print(f"  Start {start+1} best: r={best_r:.8f}")
        best_r_global = max(best_r_global, best_r)

    flush_print(f"\nd=2 global best: r = {best_r_global:.10f}, gap = {1-best_r_global:.10f}")
    return best_r_global


def d4_hill_climbing():
    flush_print("\n" + "=" * 60)
    flush_print("d=4 Hill Climbing (5 starts × 200 steps)")
    flush_print("=" * 60)

    lat = Lattice(2, 4)
    beta = 1.0
    best_r_global = -1

    np.random.seed(123)
    for start in range(5):
        Q = random_su2_config(lat.n_links)
        r = compute_r(Q, lat, beta)
        flush_print(f"  Start {start+1}: initial r={r:.8f}")
        best_r = r

        for step in range(200):
            e = np.random.randint(lat.n_links)
            v = 0.3 * np.random.randn(3)
            Q_t = Q.copy()
            Q_t[e] = su2_exp(v) @ Q[e]; Q_t[e] = project_su2(Q_t[e])
            r_t = compute_r(Q_t, lat, beta)
            if r_t > r:
                Q, r = Q_t, r_t
                best_r = max(best_r, r)
            if step % 50 == 0:
                flush_print(f"    Step {step}: r={r:.8f}")

        flush_print(f"  Start {start+1} best: r={best_r:.8f}")
        best_r_global = max(best_r_global, best_r)

    flush_print(f"\nd=4 HC global best: r = {best_r_global:.10f}, gap = {1-best_r_global:.10f}")
    return best_r_global


def d4_near_id_optimization():
    """Nelder-Mead on per-direction parameterization (12 params)."""
    flush_print("\n" + "=" * 60)
    flush_print("d=4 Nelder-Mead per-direction (12 params, 5 trials)")
    flush_print("=" * 60)

    from scipy.optimize import minimize

    lat = Lattice(2, 4)
    beta = 1.0
    best_r = -1

    for trial in range(5):
        np.random.seed(200 + trial)

        def neg_r(params):
            p = params.reshape(lat.d, 3)
            Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
            for e in range(lat.n_links):
                Q[e] = su2_exp(p[e % lat.d])
            return -compute_r(Q, lat, beta)

        x0 = np.random.randn(12) * 1.0
        result = minimize(neg_r, x0, method='Nelder-Mead', options={'maxfev': 200})
        r_val = -result.fun
        flush_print(f"  Trial {trial+1}: r = {r_val:.8f} (evals={result.nfev})")
        best_r = max(best_r, r_val)

    flush_print(f"\nNM per-dir best: r = {best_r:.10f}, gap = {1-best_r:.10f}")
    return best_r


if __name__ == '__main__':
    t0 = time.time()

    r1 = d2_gradient_ascent()
    r2 = d4_hill_climbing()
    r3 = d4_near_id_optimization()

    overall = max(r1, r2, r3)
    flush_print("\n" + "=" * 60)
    flush_print("GRAND SUMMARY")
    flush_print("=" * 60)
    flush_print(f"  d=2 gradient ascent: r = {r1:.10f}")
    flush_print(f"  d=4 hill climbing:   r = {r2:.10f}")
    flush_print(f"  d=4 NM per-dir:      r = {r3:.10f}")
    flush_print(f"\n  Overall max r = {overall:.10f}")
    flush_print(f"  Overall gap   = {1 - overall:.10f}")
    flush_print(f"  Total time: {time.time()-t0:.0f}s")
    flush_print(f"\n  VERDICT: {'PASS' if overall < 1.001 else 'FAIL'}")
