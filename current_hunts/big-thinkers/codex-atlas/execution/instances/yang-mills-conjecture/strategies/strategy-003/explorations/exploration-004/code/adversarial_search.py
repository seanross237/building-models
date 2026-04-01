"""
Adversarial search for sup|lambda_min(HessS)| on d=4, L=2 lattice SU(2) Yang-Mills.

Key optimization: Hellmann-Feynman + local Rayleigh quotient update.
When perturbing Q_e, only 2(d-1)=6 plaquettes are affected.
We compute the change in v^T H v from just those plaquettes.
This is ~30x faster than recomputing the full Hessian per perturbation.
"""

import numpy as np
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import *


# ==================================================================
# FAST RAYLEIGH QUOTIENT CHANGE (core optimization)
# ==================================================================

def plaquette_rq(Q, plaq, v, beta=1.0, N=2):
    """
    Compute one plaquette's contribution to v^T H v.
    Returns scalar: self-term + cross-term contributions.
    """
    U = plaquette_holonomy(Q, plaq)
    re_tr = np.real(np.trace(U))

    result = 0.0
    edges_list = plaq

    # Self-terms: (β/N) re_tr Σ_{e in plaq} |v_e|²
    for (e, s) in plaq:
        for a in range(3):
            result += (beta/N) * re_tr * v[3*e+a]**2

    # Cross-terms
    for p_idx in range(4):
        for q_idx in range(p_idx + 1, 4):
            ep, sp = edges_list[p_idx]
            eq, sq = edges_list[q_idx]

            L = np.eye(2, dtype=complex)
            for k in range(p_idx + 1):
                L = L @ get_link(Q, *edges_list[k])
            mid = np.eye(2, dtype=complex)
            for k in range(p_idx + 1, q_idx):
                mid = mid @ get_link(Q, *edges_list[k])
            R = np.eye(2, dtype=complex)
            for k in range(q_idx + 1, 4):
                R = R @ get_link(Q, *edges_list[k])

            for a in range(3):
                for b in range(3):
                    val = -(beta/N) * sp * sq * np.real(
                        np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                    )
                    # H_{ep_a, eq_b} += val and H_{eq_b, ep_a} += val
                    # contribution to v^T H v: 2 * val * v_{ep,a} * v_{eq,b}
                    result += 2 * val * v[3*ep+a] * v[3*eq+b]

    return result


def fast_gradient(lat, Q, v, beta=1.0, N=2, eps=1e-5):
    """
    Compute gradient of λ_min ≈ v^T H v w.r.t. perturbations Q_e -> Q_e exp(ε iσ_a).
    Only recomputes affected plaquettes (6 per edge for d=4).
    """
    ne = lat.nedges
    grad = np.zeros((ne, 3))

    # Precompute old RQ contributions per plaquette
    old_rq = {}
    for pidx, plaq in enumerate(lat.plaquettes):
        old_rq[pidx] = plaquette_rq(Q, plaq, v, beta, N)

    for e in range(ne):
        pidxs = lat.edge_plaquettes.get(e, [])
        if not pidxs:
            continue

        for a in range(3):
            dw = np.zeros(3)
            dw[a] = eps

            # Build perturbed config (only edge e changes)
            Q_pert = list(Q)
            Q_pert[e] = Q[e] @ su2_exp(dw)

            delta = 0.0
            for pidx in pidxs:
                new_rq_val = plaquette_rq(Q_pert, lat.plaquettes[pidx], v, beta, N)
                delta += new_rq_val - old_rq[pidx]

            grad[e, a] = delta / eps

    return grad


def gradient_descent(lat, Q_init, n_iters=200, lr=0.02, beta=1.0, N=2, verbose=True):
    """Gradient descent to minimize λ_min."""
    Q = [q.copy() for q in Q_init]
    ne = lat.nedges
    best_lmin = 0.0
    best_Q = None
    history = []

    for step in range(n_iters):
        H = compute_hessian(lat, Q, beta, N)
        evals, evecs = np.linalg.eigh(H)
        lmin = evals[0]
        vmin = evecs[:, 0]

        history.append(lmin)
        if lmin < best_lmin:
            best_lmin = lmin
            best_Q = [q.copy() for q in Q]

        if verbose and step % 50 == 0:
            print(f"  Step {step:3d}: λ_min={lmin:.6f}, λ_max={evals[-1]:.6f}")

        # Fast gradient
        grad = fast_gradient(lat, Q, vmin, beta, N)

        grad_norm = np.linalg.norm(grad)
        if grad_norm < 1e-8:
            if verbose:
                print(f"  Converged at step {step}: |grad|={grad_norm:.2e}")
            break

        # Adaptive step size
        effective_lr = min(lr, 0.5 / grad_norm) if grad_norm > lr / 0.5 else lr

        for e in range(ne):
            Q[e] = Q[e] @ su2_exp(-effective_lr * grad[e])

        # Line search: if λ_min increased, halve step
        if step > 0 and len(history) >= 2 and history[-1] > history[-2] + 0.01:
            # Undo and retry with smaller step
            pass  # Keep it simple for now

    return best_lmin, best_Q, history


# ==================================================================
# STRUCTURED CONFIGURATIONS
# ==================================================================

def config_uniform_angle(lat, theta, axis=2):
    w = np.zeros(3); w[axis] = theta
    Q_e = su2_exp(w)
    return [Q_e.copy() for _ in range(lat.nedges)]

def config_per_direction(lat, thetas, axes):
    Q = []
    for mu in range(lat.d):
        w = np.zeros(3); w[axes[mu]] = thetas[mu]
        Q_mu = su2_exp(w)
        for _ in range(lat.nsites):
            Q.append(Q_mu.copy())
    return Q

def config_checkerboard(lat, Q_even, Q_odd):
    Q = []
    for mu in range(lat.d):
        for site in lat.sites:
            parity = sum(site) % 2
            Q.append(Q_even.copy() if parity == 0 else Q_odd.copy())
    return Q

def config_staggered_direction(lat, theta):
    """Links in direction mu get sign(-1)^{x_mu} * theta."""
    Q = []
    for mu in range(lat.d):
        for site in lat.sites:
            sign = (-1) ** site[mu]
            w = np.zeros(3); w[2] = sign * theta
            Q.append(su2_exp(w))
    return Q

def config_orthogonal_dirs(lat, theta):
    """Direction mu gets rotation in plane (mu mod 3)."""
    Q = []
    for mu in range(lat.d):
        w = np.zeros(3); w[mu % 3] = theta
        Q.append(su2_exp(w))
    # Replicate for each site
    Q_full = []
    for mu in range(lat.d):
        for _ in range(lat.nsites):
            Q_full.append(Q[mu].copy())
    return Q_full


# ==================================================================
# MAIN
# ==================================================================

def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    dim = 3 * ne
    beta = 1.0
    N = 2

    print(f"Lattice: d={d}, L={L}, nedges={ne}, dim={dim}")
    print(f"nplaquettes={lat.nplaq}, plaq/edge=2(d-1)={2*(d-1)}")

    # Benchmark
    rng = np.random.default_rng(42)
    Q_test = random_config(lat, rng)

    t0 = time.time()
    H = compute_hessian(lat, Q_test)
    t_hess = time.time() - t0

    evals, evecs = np.linalg.eigh(H)

    t0 = time.time()
    g = fast_gradient(lat, Q_test, evecs[:, 0])
    t_grad = time.time() - t0

    print(f"Hessian: {t_hess*1000:.1f}ms, Fast gradient: {t_grad*1000:.1f}ms")
    est_total = (t_hess + t_grad) * 200 * 20 / 60
    print(f"Est. total GD time (200 iter × 20 starts): {est_total:.1f} min\n")

    all_results = []  # (lambda_min, description)
    global_best_lmin = 0.0
    global_best_Q = None

    # ========================================
    # PHASE 1: RANDOM SURVEY (1000 configs)
    # ========================================
    print("=" * 60)
    print("PHASE 1: RANDOM SURVEY")
    print("=" * 60)

    rng = np.random.default_rng(12345)
    lmins = []
    lmaxs = []
    best_random_Q = None
    best_random_lmin = 0

    t0 = time.time()
    for trial in range(1000):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q, beta, N)
        ev = np.linalg.eigvalsh(H)
        lmins.append(ev[0])
        lmaxs.append(ev[-1])
        if ev[0] < best_random_lmin:
            best_random_lmin = ev[0]
            best_random_Q = [q.copy() for q in Q]

    print(f"1000 configs in {time.time()-t0:.1f}s")
    print(f"  λ_min: min={min(lmins):.6f}, mean={np.mean(lmins):.4f}, std={np.std(lmins):.4f}")
    print(f"  λ_max: max={max(lmaxs):.6f}, mean={np.mean(lmaxs):.4f}")
    print(f"  |λ_min|/2d = {abs(min(lmins))/(2*d):.4f}")
    print(f"  |λ_min|/4d = {abs(min(lmins))/(4*d):.4f}")

    # Histogram bins
    bins = np.linspace(-10, 0, 41)
    hist, _ = np.histogram(lmins, bins=bins)
    print(f"\n  λ_min distribution (tail):")
    for i in range(5):
        if hist[i] > 0:
            print(f"    [{bins[i]:.2f}, {bins[i+1]:.2f}): {hist[i]}")

    all_results.append((best_random_lmin, "random survey"))
    if best_random_lmin < global_best_lmin:
        global_best_lmin = best_random_lmin
        global_best_Q = best_random_Q

    # ========================================
    # PHASE 2: STRUCTURED CONFIGURATIONS
    # ========================================
    print("\n" + "=" * 60)
    print("PHASE 2: STRUCTURED CONFIGS")
    print("=" * 60)

    configs = []

    # Uniform angles
    for theta in np.linspace(0.1, np.pi, 20):
        for axis in range(3):
            configs.append((config_uniform_angle(lat, theta, axis),
                          f"uniform θ={theta:.2f} ax={axis}"))

    # Per-direction (non-commuting rotations)
    angle_sets = [
        ([np.pi/2]*4, [0,1,2,0]),
        ([np.pi/2]*4, [0,1,0,1]),
        ([np.pi/3]*4, [0,1,2,0]),
        ([np.pi/4]*4, [0,1,2,0]),
        ([np.pi/2, np.pi/3, np.pi/4, np.pi/6], [0,1,2,0]),
        ([np.pi]*4, [0,0,0,0]),
        ([np.pi/2, np.pi/2, np.pi/2, 0], [0,1,2,0]),
        ([np.pi/2, 0, np.pi/2, 0], [0,1,0,1]),
    ]
    for thetas, axes in angle_sets:
        configs.append((config_per_direction(lat, thetas, axes),
                       f"per-dir {[f'{t:.2f}' for t in thetas]},{axes}"))

    # Checkerboard patterns
    for angle_e, angle_o in [(np.pi/4, np.pi/2), (0, np.pi/2), (np.pi/3, 2*np.pi/3)]:
        for ax_e, ax_o in [(0,1), (0,2), (1,2)]:
            we = np.zeros(3); we[ax_e] = angle_e
            wo = np.zeros(3); wo[ax_o] = angle_o
            configs.append((config_checkerboard(lat, su2_exp(we), su2_exp(wo)),
                           f"checker θ=({angle_e:.2f},{angle_o:.2f}) ax=({ax_e},{ax_o})"))

    # Checkerboard with I / isigma
    for a in range(3):
        configs.append((config_checkerboard(lat, np.eye(2, dtype=complex), isigma[a]),
                       f"checker I/iσ_{a+1}"))

    # Staggered
    for theta in np.linspace(0.1, np.pi, 15):
        configs.append((config_staggered_direction(lat, theta),
                       f"staggered θ={theta:.2f}"))

    # Orthogonal directions
    for theta in np.linspace(0.1, np.pi, 15):
        configs.append((config_orthogonal_dirs(lat, theta),
                       f"ortho-dir θ={theta:.2f}"))

    # Anti-instanton attempt: mu -> isigma[mu%3]
    Q_ai = []
    for mu in range(d):
        for _ in range(lat.nsites):
            Q_ai.append(isigma[mu % 3].copy())
    configs.append((Q_ai, "anti-instanton"))

    # Large-angle random
    rng2 = np.random.default_rng(999)
    for trial in range(50):
        Q = []
        for e in range(ne):
            theta = np.pi * (0.3 + 0.7 * rng2.random())
            axis = rng2.normal(size=3)
            axis /= np.linalg.norm(axis)
            Q.append(su2_exp(theta * axis))
        configs.append((Q, f"large-angle-rand-{trial}"))

    best_struct_lmin = 0
    best_struct_Q = None
    best_struct_desc = ""

    for Q, desc in configs:
        try:
            H = compute_hessian(lat, Q, beta, N)
            ev = np.linalg.eigvalsh(H)
            lmin = ev[0]
            if lmin < best_struct_lmin:
                best_struct_lmin = lmin
                best_struct_Q = [q.copy() for q in Q]
                best_struct_desc = desc
                print(f"  NEW BEST: λ_min={lmin:.6f} [{desc}]")
            all_results.append((lmin, desc))
        except Exception as ex:
            pass

    print(f"\nBest structured: λ_min={best_struct_lmin:.6f} [{best_struct_desc}]")
    if best_struct_lmin < global_best_lmin:
        global_best_lmin = best_struct_lmin
        global_best_Q = best_struct_Q

    # ========================================
    # PHASE 3: GRADIENT DESCENT (20 starts)
    # ========================================
    print("\n" + "=" * 60)
    print("PHASE 3: GRADIENT DESCENT")
    print("=" * 60)

    rng3 = np.random.default_rng(54321)
    n_starts = 20
    n_iters_per_start = 200

    for start in range(n_starts):
        t0 = time.time()

        # Choose starting configuration
        if start < 12:
            Q_init = random_config(lat, rng3)
            desc = f"random-{start}"
        elif start == 12 and best_struct_Q is not None:
            Q_init = [q.copy() for q in best_struct_Q]
            desc = f"warm-struct"
        elif start == 13 and best_random_Q is not None:
            Q_init = [q.copy() for q in best_random_Q]
            desc = f"warm-random"
        elif start == 14 and global_best_Q is not None:
            # Perturb the current best slightly
            Q_init = [q.copy() for q in global_best_Q]
            for e in range(ne):
                Q_init[e] = Q_init[e] @ su2_exp(0.1 * rng3.normal(size=3))
            desc = "perturbed-best"
        else:
            # Large-angle random
            Q_init = []
            for e in range(ne):
                theta = np.pi * rng3.random()
                axis = rng3.normal(size=3)
                axis /= np.linalg.norm(axis)
                Q_init.append(su2_exp(theta * axis))
            desc = f"large-angle-{start}"

        best_lmin, best_Q, history = gradient_descent(
            lat, Q_init, n_iters=n_iters_per_start, lr=0.015,
            beta=beta, N=N, verbose=False
        )

        elapsed = time.time() - t0
        print(f"  Start {start+1:2d}/{n_starts} [{desc:20s}]: "
              f"λ_min={best_lmin:.6f} ({elapsed:.1f}s)", end="")

        all_results.append((best_lmin, f"GD-{desc}"))

        if best_lmin < global_best_lmin:
            global_best_lmin = best_lmin
            global_best_Q = [q.copy() for q in best_Q]
            print(" *** NEW BEST ***", end="")
        print()

    # ========================================
    # PHASE 4: REFINEMENT on best config
    # ========================================
    print("\n" + "=" * 60)
    print("PHASE 4: REFINEMENT (coordinate descent on best)")
    print("=" * 60)

    if global_best_Q is not None:
        Q = [q.copy() for q in global_best_Q]
        print(f"Starting from global best: λ_min={global_best_lmin:.6f}")

        # Multiple rounds of GD with smaller step size
        for refine in range(3):
            lr = 0.01 / (refine + 1)
            best_lmin, best_Q, _ = gradient_descent(
                lat, Q, n_iters=300, lr=lr, beta=beta, N=N, verbose=False
            )
            if best_lmin < global_best_lmin:
                global_best_lmin = best_lmin
                global_best_Q = [q.copy() for q in best_Q]
                Q = [q.copy() for q in best_Q]
                print(f"  Refine {refine+1}: λ_min={best_lmin:.6f} (lr={lr:.4f}) *** IMPROVED ***")
            else:
                Q = [q.copy() for q in best_Q]
                print(f"  Refine {refine+1}: λ_min={best_lmin:.6f} (lr={lr:.4f})")

        # Per-link coordinate descent
        print("\n  Per-link coordinate descent:")
        Q = [q.copy() for q in global_best_Q]
        for sweep in range(5):
            H = compute_hessian(lat, Q, beta, N)
            current_lmin = np.linalg.eigvalsh(H)[0]
            improved = False

            for e in range(ne):
                best_local_lmin = current_lmin
                best_dw = np.zeros(3)

                # Try several random perturbations
                for _ in range(50):
                    dw = 0.05 * np.random.randn(3) / (sweep + 1)
                    Q_try = list(Q)
                    Q_try[e] = Q[e] @ su2_exp(dw)
                    H_try = compute_hessian(lat, Q_try, beta, N)
                    lmin_try = np.linalg.eigvalsh(H_try)[0]

                    if lmin_try < best_local_lmin:
                        best_local_lmin = lmin_try
                        best_dw = dw.copy()

                if best_local_lmin < current_lmin - 1e-8:
                    Q[e] = Q[e] @ su2_exp(best_dw)
                    current_lmin = best_local_lmin
                    improved = True

            H = compute_hessian(lat, Q, beta, N)
            current_lmin = np.linalg.eigvalsh(H)[0]
            print(f"    Sweep {sweep+1}: λ_min={current_lmin:.6f}" +
                  (" (improved)" if improved else " (converged)"))

            if current_lmin < global_best_lmin:
                global_best_lmin = current_lmin
                global_best_Q = [q.copy() for q in Q]

            if not improved:
                break

    # ========================================
    # PHASE 5: DIMENSION SCAN (d=2,3,4,5)
    # ========================================
    print("\n" + "=" * 60)
    print("PHASE 5: DIMENSION SCAN")
    print("=" * 60)

    for dd in [2, 3, 4]:
        lat_d = Lattice(dd, 2)
        rng_d = np.random.default_rng(42)

        # Random survey
        best_lmin_d = 0
        for trial in range(500):
            Q = random_config(lat_d, rng_d)
            H = compute_hessian(lat_d, Q, 1.0, 2)
            ev = np.linalg.eigvalsh(H)
            best_lmin_d = min(best_lmin_d, ev[0])

        # Quick GD from 5 starts
        for _ in range(5):
            Q_init = random_config(lat_d, rng_d)
            bl, _, _ = gradient_descent(lat_d, Q_init, n_iters=100, lr=0.02, verbose=False)
            best_lmin_d = min(best_lmin_d, bl)

        print(f"  d={dd}: inf λ_min ≈ {best_lmin_d:.6f}, |λ_min|={abs(best_lmin_d):.4f}, "
              f"|λ_min|/2d={abs(best_lmin_d)/(2*dd):.4f}, |λ_min|/4d={abs(best_lmin_d)/(4*dd):.4f}")

    # ========================================
    # FINAL SUMMARY
    # ========================================
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print(f"\nGlobal best λ_min = {global_best_lmin:.6f}")
    abs_lmin = abs(global_best_lmin)
    print(f"|λ_min| = {abs_lmin:.6f}")
    print(f"|λ_min| / d  = {abs_lmin/d:.4f}")
    print(f"|λ_min| / 2d = {abs_lmin/(2*d):.4f}")
    print(f"|λ_min| / 4d = {abs_lmin/(4*d):.4f}")

    beta_threshold = 2.0 / abs_lmin if abs_lmin > 0 else float('inf')
    print(f"\nMass gap threshold: β < 2/{abs_lmin:.4f} = {beta_threshold:.6f}")
    print(f"  SZZ:           β < 1/12 = {1/12:.6f}")
    print(f"  λ_max=4d=16:   β < 1/8  = {1/8:.6f}")
    print(f"  |λ_min|≤2d=8:  β < 1/4  = {1/4:.6f}")

    # Determine which bound applies
    if abs_lmin <= 2*d + 0.01:
        print(f"\n  *** |λ_min| ≤ 2d = {2*d}: mass gap at β < 1/4 ACHIEVABLE ***")
    elif abs_lmin <= 4*d + 0.01:
        print(f"\n  |λ_min| ≤ 4d = {4*d}: mass gap at β < 1/8 (via current proof)")
    else:
        print(f"\n  WARNING: |λ_min| > 4d! Check computation.")

    # Save results
    if global_best_Q is not None:
        np.savez(os.path.join(os.path.dirname(__file__), 'best_config.npz'),
                 Q=np.array(global_best_Q),
                 lambda_min=global_best_lmin, d=d, L=L)
        print(f"\nBest config saved to code/best_config.npz")

    # Top results
    all_results.sort()
    print(f"\nTop 10 most negative λ_min:")
    for i, (lmin, desc) in enumerate(all_results[:10]):
        print(f"  {i+1}. λ_min={lmin:.6f} [{desc}]")

    return global_best_lmin, global_best_Q


if __name__ == "__main__":
    main()
