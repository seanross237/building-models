"""
Approach C: Concavity / Local Maximum Argument
Test whether λ_max(H(Q)) is concave on SU(2)^E (along geodesics),
and whether flat connections are the unique global max.

Two sub-tests:
1. Midpoint concavity: λ_max(H(Q_mid)) ≥ (λ_max(H(Q1)) + λ_max(H(Q2)))/2
   along geodesics Q(t) on SU(2)^E.
2. Gradient ascent on λ_max: do ALL starts converge to flat?

If λ_max is concave and flat is a local max (proved in E003), then flat is global max.
"""

import numpy as np
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, su2_exp, project_su2,
    flat_config, random_config, anti_instanton_config,
    compute_hessian, isigma
)

def su2_log(U):
    """Lie algebra element w such that exp(Σ w_a iσ_a) = U.
    Returns 3-vector w."""
    # U = cos(θ)I + i sin(θ)(n·σ) = cos(θ)I + sin(θ)(n·(iσ))
    cos_theta = np.real(np.trace(U)) / 2.0
    cos_theta = np.clip(cos_theta, -1, 1)
    theta = np.arccos(cos_theta)

    if abs(theta) < 1e-12:
        return np.zeros(3)

    # Extract axis: U - cos(θ)I = sin(θ) Σ n_a iσ_a
    # Tr(iσ_a^† (U - cos(θ)I)) = sin(θ) n_a * Tr(iσ_a^† iσ_a) = -2 sin(θ) n_a
    # So n_a = -Tr((-iσ_a)(U - cos(θ)I)) / (2 sin(θ))
    w = np.zeros(3)
    U_traceless = U - cos_theta * np.eye(2, dtype=complex)
    for a in range(3):
        w[a] = np.real(np.trace((-isigma[a]) @ U_traceless)) / (2.0 * np.sin(theta)) * theta
        # w_a = θ * n_a

    return w

def geodesic_interpolation(Q1, Q2, t):
    """Geodesic interpolation on SU(2)^E: Q(t) = Q1_e · exp(t · log(Q1_e^{-1} Q2_e))."""
    ne = len(Q1)
    Q_t = []
    for e in range(ne):
        Delta = su2_inv(Q1[e]) @ Q2[e]
        w = su2_log(Delta)
        Q_t.append(Q1[e] @ su2_exp(t * w))
    return Q_t

def lambda_max_H(lat, Q, beta=1.0, N=2):
    """Compute λ_max of H(Q)."""
    H = compute_hessian(lat, Q, beta, N)
    return np.max(np.linalg.eigvalsh(H))

def lambda_min_H(lat, Q, beta=1.0, N=2):
    """Compute λ_min of H(Q)."""
    H = compute_hessian(lat, Q, beta, N)
    return np.min(np.linalg.eigvalsh(H))

def test_midpoint_concavity(lat, Q1, Q2, n_points=11):
    """Test concavity along geodesic from Q1 to Q2.
    Concavity means: f(t) ≥ (1-t)f(0) + t f(1) for all t in [0,1].
    Returns max violation (positive = violated, negative = holds).
    """
    t_vals = np.linspace(0, 1, n_points)
    f_vals = []
    for t in t_vals:
        Q_t = geodesic_interpolation(Q1, Q2, t)
        f_vals.append(lambda_max_H(lat, Q_t))

    f0 = f_vals[0]
    f1 = f_vals[-1]

    max_violation = -np.inf
    for i, t in enumerate(t_vals):
        linear = (1 - t) * f0 + t * f1
        # Concavity: f(t) ≥ linear
        violation = linear - f_vals[i]  # positive = concavity violated
        max_violation = max(max_violation, violation)

    return max_violation, t_vals, f_vals

def gradient_ascent_lambda_max(lat, Q_init, n_iters=200, lr=0.015):
    """Gradient ascent on λ_max(H(Q)). If all starts converge to flat, that's evidence."""
    ne = lat.nedges
    Q = [q.copy() for q in Q_init]
    trajectory = []
    best_val = -np.inf
    best_Q = None

    for it in range(n_iters):
        H = compute_hessian(lat, Q)
        evals, evecs = np.linalg.eigh(H)
        lam_max = evals[-1]
        v_max = evecs[:, -1]
        trajectory.append(lam_max)

        if lam_max > best_val:
            best_val = lam_max
            best_Q = [q.copy() for q in Q]

        # Gradient via finite differences of Rayleigh quotient v^T H v
        eps = 1e-4
        grad = np.zeros((ne, 3))
        for e in range(ne):
            for a in range(3):
                w = np.zeros(3); w[a] = eps
                Q_plus = [q.copy() for q in Q]
                Q_plus[e] = su2_exp(w) @ Q[e]
                H_plus = compute_hessian(lat, Q_plus)
                rq_plus = v_max @ H_plus @ v_max
                rq_0 = lam_max
                grad[e, a] = (rq_plus - rq_0) / eps

        gnorm = np.linalg.norm(grad)
        if gnorm < 1e-8:
            break

        effective_lr = min(lr, 0.5 / gnorm) if gnorm > lr / 0.5 else lr
        for e in range(ne):
            Q[e] = su2_exp(effective_lr * grad[e]) @ Q[e]
            Q[e] = project_su2(Q[e])

        if it % 50 == 0:
            print(f"    iter {it}: λ_max={lam_max:.6f}, |grad|={gnorm:.2e}")

    return best_val, best_Q, trajectory

def check_near_flat(Q, tol=0.1):
    """Check if Q is close to a flat config (all links ≈ ±I)."""
    max_dist = 0
    for q in Q:
        # Distance to identity
        d_I = np.linalg.norm(q - np.eye(2, dtype=complex))
        d_mI = np.linalg.norm(q + np.eye(2, dtype=complex))
        max_dist = max(max_dist, min(d_I, d_mI))
    return max_dist < tol, max_dist


def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d

    print(f"{'='*70}")
    print(f"APPROACH C: CONCAVITY / LOCAL MAXIMUM ARGUMENT")
    print(f"d={d}, L={L}, bound=4d={bound}")
    print(f"{'='*70}")

    rng = np.random.default_rng(42)

    # ==================================================================
    # TEST 1: MIDPOINT CONCAVITY
    # ==================================================================
    print(f"\n{'='*60}")
    print("TEST 1: MIDPOINT CONCAVITY of λ_max along geodesics")
    print(f"{'='*60}")

    n_geodesics = 200
    max_viol = -np.inf
    n_violated = 0
    violations = []

    for trial in range(n_geodesics):
        Q1 = random_config(lat, rng)
        Q2 = random_config(lat, rng)
        viol, t_vals, f_vals = test_midpoint_concavity(lat, Q1, Q2, n_points=11)
        if viol > 1e-6:
            n_violated += 1
            violations.append(viol)
        max_viol = max(max_viol, viol)

        if trial % 50 == 0:
            print(f"  trial {trial}: max_violation_so_far={max_viol:.6e}, "
                  f"n_violated={n_violated}/{trial+1}")

    print(f"\nResults: {n_geodesics} geodesics tested")
    print(f"  Max violation: {max_viol:.6e}")
    print(f"  Concavity violations: {n_violated}/{n_geodesics}")
    concavity_holds = n_violated == 0

    if n_violated > 0:
        print(f"  *** CONCAVITY FAILS ***")
        print(f"  Violation magnitudes: min={min(violations):.6e}, max={max(violations):.6e}, "
              f"mean={np.mean(violations):.6e}")
    else:
        print(f"  Concavity holds for all tested geodesics!")

    # Test with geodesics from/to flat
    print(f"\n  --- Geodesics involving flat ---")
    Q_flat = flat_config(lat)
    max_viol_flat = -np.inf
    n_viol_flat = 0

    for trial in range(100):
        Q2 = random_config(lat, rng)
        viol, t_vals, f_vals = test_midpoint_concavity(lat, Q_flat, Q2, n_points=21)
        if viol > 1e-6:
            n_viol_flat += 1
        max_viol_flat = max(max_viol_flat, viol)

    print(f"  Flat-to-random: max_viol={max_viol_flat:.6e}, violated={n_viol_flat}/100")

    # Test with geodesics from/to anti-instanton
    print(f"\n  --- Geodesics involving anti-instanton ---")
    Q_ai = anti_instanton_config(lat)
    max_viol_ai = -np.inf
    n_viol_ai = 0

    for trial in range(50):
        Q2 = random_config(lat, rng)
        viol, t_vals, f_vals = test_midpoint_concavity(lat, Q_ai, Q2, n_points=11)
        if viol > 1e-6:
            n_viol_ai += 1
        max_viol_ai = max(max_viol_ai, viol)

    print(f"  Anti-inst-to-random: max_viol={max_viol_ai:.6e}, violated={n_viol_ai}/50")

    # ==================================================================
    # TEST 2: GRADIENT ASCENT on λ_max → does it converge to flat?
    # ==================================================================
    print(f"\n{'='*60}")
    print("TEST 2: GRADIENT ASCENT on λ_max → convergence to flat?")
    print(f"{'='*60}")

    convergence_results = []

    starts = []
    for i in range(10):
        starts.append((f'random-{i}', random_config(lat, rng)))
    starts.append(('anti-instanton', anti_instanton_config(lat)))
    # Perturbed anti-instanton
    Q_ai = anti_instanton_config(lat)
    starts.append(('pert-anti-inst', [su2_exp(0.5*rng.normal(size=3)) @ q for q in Q_ai]))

    for name, Q_init in starts:
        print(f"\n  Start: {name}")
        init_lmax = lambda_max_H(lat, Q_init)
        print(f"    initial λ_max = {init_lmax:.4f}")

        best_val, best_Q, traj = gradient_ascent_lambda_max(
            lat, Q_init, n_iters=200, lr=0.015
        )
        near_flat, dist = check_near_flat(best_Q, tol=0.5)
        final_lmax = lambda_max_H(lat, best_Q)

        print(f"    final λ_max = {final_lmax:.6f}")
        print(f"    near flat? {near_flat} (max_dist={dist:.4f})")
        print(f"    ratio final/4d = {final_lmax/bound:.4f}")

        convergence_results.append({
            'name': name, 'init_lmax': init_lmax,
            'final_lmax': final_lmax, 'near_flat': near_flat, 'dist': dist
        })

    # ==================================================================
    # TEST 3: SECOND DERIVATIVE (Hessian of λ_max) check
    # ==================================================================
    print(f"\n{'='*60}")
    print("TEST 3: SECOND DERIVATIVE of λ_max at various configs")
    print(f"{'='*60}")

    # At flat, E003 showed d²λ_max/dε² < 0 for all directions.
    # Check at other critical points.
    configs_to_check = [
        ('flat', flat_config(lat)),
        ('anti-instanton', anti_instanton_config(lat)),
    ]

    for name, Q0 in configs_to_check:
        lam0 = lambda_max_H(lat, Q0)
        print(f"\n  Config: {name}, λ_max = {lam0:.6f}")

        # Sample random perturbation directions
        n_dirs = 30
        d2_vals = []
        eps = 0.02
        for _ in range(n_dirs):
            # Random direction in Lie algebra
            dw = [rng.normal(size=3) for _ in range(ne)]
            # Normalize
            norm = np.sqrt(sum(np.linalg.norm(w)**2 for w in dw))
            dw = [w / norm for w in dw]

            # f(ε) = λ_max(Q0 · exp(ε·dw))
            f_minus = lambda_max_H(lat, [su2_exp(-eps * w) @ q for w, q in zip(dw, Q0)])
            f_plus = lambda_max_H(lat, [su2_exp(eps * w) @ q for w, q in zip(dw, Q0)])
            d2 = (f_plus - 2*lam0 + f_minus) / eps**2
            d2_vals.append(d2)

        d2_arr = np.array(d2_vals)
        print(f"    d²λ_max/dε²: min={d2_arr.min():.4f}, max={d2_arr.max():.4f}, "
              f"mean={d2_arr.mean():.4f}")
        n_pos = np.sum(d2_arr > 0)
        print(f"    Positive (convex/saddle): {n_pos}/{n_dirs}")
        if name == 'flat':
            print(f"    All negative → local max? {np.all(d2_arr < 0)}")

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print(f"\n{'='*70}")
    print("APPROACH C SUMMARY")
    print(f"{'='*70}")

    print(f"\nMidpoint concavity test:")
    print(f"  Random-random: {n_violated}/{n_geodesics} violations (max={max_viol:.2e})")
    print(f"  Flat-random:   {n_viol_flat}/100 violations (max={max_viol_flat:.2e})")
    print(f"  AI-random:     {n_viol_ai}/50 violations (max={max_viol_ai:.2e})")

    print(f"\nGradient ascent convergence:")
    all_converge = all(r['final_lmax'] > bound - 0.5 and r['near_flat'] for r in convergence_results)
    for r in convergence_results:
        print(f"  {r['name']:20s}: λ_max={r['final_lmax']:.4f}, near_flat={r['near_flat']}, "
              f"dist={r['dist']:.4f}")

    return concavity_holds


if __name__ == "__main__":
    main()
