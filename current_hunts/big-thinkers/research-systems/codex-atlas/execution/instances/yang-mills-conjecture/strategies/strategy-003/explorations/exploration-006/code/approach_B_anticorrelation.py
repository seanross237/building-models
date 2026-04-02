"""
Approach B: D/C Anti-Correlation Bound
Test whether |D_min(Q)| + ||C(Q)||_op ≤ 4d for all Q.

The D+C decomposition failed because ||C|| alone can exceed 2(d+1).
But the combined bound |D| + ||C|| ≤ 4d may hold due to anti-correlation:
when ||C|| is large, |D| is small (and vice versa).

This script:
1. Random survey: 1000+ configs, compute |D_min| + ||C||_op
2. Structured configs (anti-instanton, near-saddle, etc.)
3. Gradient ascent on |D_min| + ||C||_op
4. Detailed analysis of the tradeoff curve
"""

import numpy as np
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, su2_exp, project_su2,
    flat_config, random_config, anti_instanton_config,
    compute_hessian, compute_hessian_decomposed,
    plaquette_holonomy, isigma
)

def analyze_config(lat, Q, beta=1.0, N=2):
    """Compute D_min, D_max, ||C||_op, |λ(H)|_max for a config."""
    D, C = compute_hessian_decomposed(lat, Q, beta, N)
    evals_C = np.linalg.eigvalsh(C)
    C_norm = max(abs(evals_C[0]), abs(evals_C[-1]))
    D_min = np.min(D)
    D_max = np.max(D)

    H = np.diag(D) + C
    evals_H = np.linalg.eigvalsh(H)
    lam_min = evals_H[0]
    lam_max = evals_H[-1]

    return {
        'D_min': D_min, 'D_max': D_max,
        'C_norm': C_norm,
        'lam_min': lam_min, 'lam_max': lam_max,
        'D_range': D_max - D_min,
        'abs_D_min': abs(D_min),
        'abs_D_max': abs(D_max),
        'sum_pos': D_max + C_norm,  # for λ_max bound
        'sum_neg': abs(D_min) + C_norm,  # for |λ_min| bound
    }

def gradient_ascent_combined(lat, Q_init, n_iters=200, lr=0.015, target='sum_neg'):
    """Gradient ascent on |D_min| + ||C|| (target='sum_neg')
    or on D_max + ||C|| (target='sum_pos') or on |λ_max| directly."""
    ne = lat.nedges
    Q = [q.copy() for q in Q_init]
    best_val = -np.inf
    best_Q = None
    trajectory = []

    for it in range(n_iters):
        info = analyze_config(lat, Q)
        if target == 'sum_neg':
            val = info['sum_neg']
        elif target == 'sum_pos':
            val = info['sum_pos']
        elif target == 'lam_max':
            val = info['lam_max']
        elif target == 'abs_lam_min':
            val = abs(info['lam_min'])
        else:
            val = info['sum_neg']

        trajectory.append(val)
        if val > best_val:
            best_val = val
            best_Q = [q.copy() for q in Q]

        # Finite-difference gradient
        eps = 1e-4
        grad = np.zeros((ne, 3))
        for e in range(ne):
            for a in range(3):
                w = np.zeros(3)
                w[a] = eps
                Q_plus = [q.copy() for q in Q]
                Q_plus[e] = su2_exp(w) @ Q[e]
                info_plus = analyze_config(lat, Q_plus)
                if target == 'sum_neg':
                    val_plus = info_plus['sum_neg']
                elif target == 'sum_pos':
                    val_plus = info_plus['sum_pos']
                elif target == 'lam_max':
                    val_plus = info_plus['lam_max']
                elif target == 'abs_lam_min':
                    val_plus = abs(info_plus['lam_min'])
                else:
                    val_plus = info_plus['sum_neg']
                grad[e, a] = (val_plus - val) / eps

        gnorm = np.linalg.norm(grad)
        if gnorm < 1e-8:
            break

        effective_lr = min(lr, 0.5 / gnorm) if gnorm > lr / 0.5 else lr
        for e in range(ne):
            Q[e] = su2_exp(effective_lr * grad[e]) @ Q[e]
            Q[e] = project_su2(Q[e])

        if it % 50 == 0:
            print(f"    iter {it}: val={val:.6f} |D_min|={info['abs_D_min']:.3f} "
                  f"||C||={info['C_norm']:.3f} gnorm={gnorm:.2e}")

    return best_val, best_Q, trajectory


def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    bound_4d = 4 * d  # = 16

    print(f"{'='*70}")
    print(f"APPROACH B: D/C ANTI-CORRELATION BOUND")
    print(f"d={d}, L={L}, nedges={ne}, target bound = 4d = {bound_4d}")
    print(f"{'='*70}")

    # ==================================================================
    # PHASE 1: RANDOM SURVEY (1000 configs)
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 1: RANDOM SURVEY (1000 configs)")
    print(f"{'='*60}")

    rng = np.random.default_rng(42)
    results = []
    t0 = time.time()

    for trial in range(1000):
        Q = random_config(lat, rng)
        info = analyze_config(lat, Q)
        results.append(info)

    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.1f}s")

    sum_negs = [r['sum_neg'] for r in results]
    sum_poss = [r['sum_pos'] for r in results]
    lam_maxs = [r['lam_max'] for r in results]
    abs_lam_mins = [abs(r['lam_min']) for r in results]
    C_norms = [r['C_norm'] for r in results]
    D_mins = [r['D_min'] for r in results]

    print(f"\n|D_min| + ||C||  (controls |λ_min|):")
    print(f"  max = {max(sum_negs):.6f}  (bound = {bound_4d})")
    print(f"  mean = {np.mean(sum_negs):.4f}")
    print(f"  violations of 4d: {sum(1 for x in sum_negs if x > bound_4d)}")

    print(f"\nD_max + ||C||  (controls λ_max):")
    print(f"  max = {max(sum_poss):.6f}  (bound = {bound_4d})")
    print(f"  mean = {np.mean(sum_poss):.4f}")
    print(f"  violations of 4d: {sum(1 for x in sum_poss if x > bound_4d)}")

    print(f"\nActual λ_max:")
    print(f"  max = {max(lam_maxs):.6f}")
    print(f"  violations of 4d: {sum(1 for x in lam_maxs if x > bound_4d + 0.01)}")

    print(f"\nActual |λ_min|:")
    print(f"  max = {max(abs_lam_mins):.6f}")
    print(f"  violations of 4d: {sum(1 for x in abs_lam_mins if x > bound_4d + 0.01)}")

    print(f"\n||C|| alone:")
    print(f"  max = {max(C_norms):.6f}")
    print(f"  mean = {np.mean(C_norms):.4f}")

    print(f"\nD_min (most negative self-term):")
    print(f"  min = {min(D_mins):.6f}")
    print(f"  mean = {np.mean(D_mins):.4f}")

    # Slack analysis
    slacks_neg = [bound_4d - x for x in sum_negs]
    slacks_pos = [bound_4d - x for x in sum_poss]
    print(f"\nSlack (4d - sum):")
    print(f"  neg: min={min(slacks_neg):.4f}, mean={np.mean(slacks_neg):.4f}")
    print(f"  pos: min={min(slacks_pos):.4f}, mean={np.mean(slacks_pos):.4f}")

    # ==================================================================
    # PHASE 2: STRUCTURED CONFIGS
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 2: STRUCTURED CONFIGS")
    print(f"{'='*60}")

    structured = []

    # Flat
    Q = flat_config(lat)
    info = analyze_config(lat, Q)
    structured.append(('flat', info))

    # Anti-instanton
    Q = anti_instanton_config(lat)
    info = analyze_config(lat, Q)
    structured.append(('anti-instanton', info))

    # Near saddle: checkerboard I/iσ
    for ax in range(3):
        Q = []
        for mu in range(d):
            for site in lat.sites:
                if sum(site) % 2 == 0:
                    Q.append(np.eye(2, dtype=complex))
                else:
                    Q.append(isigma[ax].copy())
        info = analyze_config(lat, Q)
        structured.append((f'checker-I/iσ{ax}', info))

    # Uniform rotations at various angles
    for theta in [np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, np.pi]:
        w = np.zeros(3); w[2] = theta
        Q_e = su2_exp(w)
        Q = [Q_e.copy() for _ in range(ne)]
        info = analyze_config(lat, Q)
        structured.append((f'uniform-θ={theta:.3f}', info))

    # Per-direction non-commuting
    axes_list = [[0,1,2,0], [0,1,0,1]]
    for axes in axes_list:
        for theta in [np.pi/4, np.pi/2, np.pi]:
            Q = []
            for mu in range(d):
                w = np.zeros(3); w[axes[mu]] = theta
                Q_mu = su2_exp(w)
                for _ in range(lat.nsites):
                    Q.append(Q_mu.copy())
            info = analyze_config(lat, Q)
            structured.append((f'perdir-{axes}-θ={theta:.2f}', info))

    print(f"{'config':40s} {'|D_min|':>8s} {'||C||':>8s} {'sum':>8s} {'λ_max':>8s} {'|λ_min|':>8s} {'slack':>8s}")
    print("-" * 100)
    max_sum = 0
    for name, info in structured:
        s = info['sum_neg']
        max_sum = max(max_sum, s)
        slack = bound_4d - max(s, info['sum_pos'])
        print(f"{name:40s} {info['abs_D_min']:8.4f} {info['C_norm']:8.4f} "
              f"{s:8.4f} {info['lam_max']:8.4f} {abs(info['lam_min']):8.4f} {slack:8.4f}")

    # Also check sum_pos
    for name, info in structured:
        if info['sum_pos'] > bound_4d:
            print(f"*** VIOLATION (pos) at {name}: D_max+||C|| = {info['sum_pos']:.6f} > {bound_4d}")
        if info['sum_neg'] > bound_4d:
            print(f"*** VIOLATION (neg) at {name}: |D_min|+||C|| = {info['sum_neg']:.6f} > {bound_4d}")

    # ==================================================================
    # PHASE 3: GRADIENT ASCENT on |D_min| + ||C||
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 3: GRADIENT ASCENT on |D_min| + ||C||")
    print(f"{'='*60}")

    rng2 = np.random.default_rng(12345)
    best_global = 0
    best_global_info = None

    starts = [
        ('random-1', random_config(lat, rng2)),
        ('random-2', random_config(lat, rng2)),
        ('random-3', random_config(lat, rng2)),
        ('random-4', random_config(lat, rng2)),
        ('random-5', random_config(lat, rng2)),
        ('flat', flat_config(lat)),
        ('anti-inst', anti_instanton_config(lat)),
    ]

    # Add perturbed anti-instanton starts
    for i in range(3):
        Q_ai = anti_instanton_config(lat)
        Q_pert = [su2_exp(0.3 * rng2.normal(size=3)) @ q for q in Q_ai]
        Q_pert = [project_su2(q) for q in Q_pert]
        starts.append((f'pert-anti-inst-{i}', Q_pert))

    for name, Q_init in starts:
        print(f"\n  Start: {name}")
        info_init = analyze_config(lat, Q_init)
        print(f"    initial: |D_min|+||C|| = {info_init['sum_neg']:.4f}")

        best_val, best_Q, traj = gradient_ascent_combined(
            lat, Q_init, n_iters=150, lr=0.015, target='sum_neg'
        )
        info_final = analyze_config(lat, best_Q)
        print(f"    FINAL: |D_min|+||C|| = {best_val:.6f}, "
              f"|D_min|={info_final['abs_D_min']:.3f}, ||C||={info_final['C_norm']:.3f}")
        print(f"    Actual: λ_max={info_final['lam_max']:.4f}, λ_min={info_final['lam_min']:.4f}")

        if best_val > best_global:
            best_global = best_val
            best_global_info = info_final
            print(f"    *** NEW GLOBAL BEST ***")

    # Also try maximizing sum_pos
    print(f"\n  --- Now maximizing D_max + ||C|| ---")
    for name, Q_init in starts[:5]:
        print(f"\n  Start: {name}")
        best_val, best_Q, traj = gradient_ascent_combined(
            lat, Q_init, n_iters=150, lr=0.015, target='sum_pos'
        )
        info_final = analyze_config(lat, best_Q)
        print(f"    FINAL: D_max+||C|| = {best_val:.6f}, "
              f"D_max={info_final['D_max']:.3f}, ||C||={info_final['C_norm']:.3f}")
        if best_val > best_global:
            best_global = best_val
            best_global_info = info_final

    # ==================================================================
    # PHASE 4: TRADEOFF CURVE
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 4: D/C TRADEOFF CURVE")
    print(f"{'='*60}")

    # Collect (|D_min|, ||C||) pairs from all data
    pairs = [(r['abs_D_min'], r['C_norm']) for r in results]
    # Add structured
    for name, info in structured:
        pairs.append((info['abs_D_min'], info['C_norm']))

    # Compute convex hull of tradeoff
    abs_d_vals = [p[0] for p in pairs]
    c_vals = [p[1] for p in pairs]

    print(f"Tradeoff extremes:")
    print(f"  max |D_min|: {max(abs_d_vals):.4f} (with ||C||={c_vals[np.argmax(abs_d_vals)]:.4f})")
    print(f"  max ||C||:   {max(c_vals):.4f} (with |D_min|={abs_d_vals[np.argmax(c_vals)]:.4f})")

    # Check: does |D_min| + ||C|| ≤ 4d define a half-plane that contains all points?
    violations = [(d_val, c_val) for d_val, c_val in pairs if d_val + c_val > bound_4d + 0.01]
    print(f"\nViolations of |D_min| + ||C|| ≤ {bound_4d}: {len(violations)}")
    if violations:
        worst = max(violations, key=lambda p: p[0]+p[1])
        print(f"  Worst: |D_min|={worst[0]:.4f}, ||C||={worst[1]:.4f}, sum={worst[0]+worst[1]:.4f}")

    # Also check linear combinations: α|D_min| + (1-α)||C|| ≤ f(α)
    print(f"\nTighter bound search:")
    print(f"  Trying |D_min| + ||C|| ≤ K:")
    K_vals = [bound_4d, bound_4d - 0.5, bound_4d - 1.0, bound_4d - 1.5, bound_4d - 2.0]
    for K in K_vals:
        n_viol = sum(1 for d_v, c_v in pairs if d_v + c_v > K + 0.001)
        print(f"    K = {K:.1f}: {n_viol} violations")

    # ==================================================================
    # PHASE 5: DIMENSION SCAN
    # ==================================================================
    print(f"\n{'='*60}")
    print("PHASE 5: DIMENSION SCAN")
    print(f"{'='*60}")

    for dd in [2, 3, 4]:
        lat_d = Lattice(dd, 2)
        rng_d = np.random.default_rng(42)
        bound_dd = 4 * dd
        max_sum_neg = 0
        max_sum_pos = 0
        max_lam = 0
        max_abs_lam_min = 0

        for trial in range(500):
            Q = random_config(lat_d, rng_d)
            info = analyze_config(lat_d, Q)
            max_sum_neg = max(max_sum_neg, info['sum_neg'])
            max_sum_pos = max(max_sum_pos, info['sum_pos'])
            max_lam = max(max_lam, info['lam_max'])
            max_abs_lam_min = max(max_abs_lam_min, abs(info['lam_min']))

        print(f"d={dd}: bound=4d={bound_dd}")
        print(f"  max |D_min|+||C|| = {max_sum_neg:.4f} (ratio={max_sum_neg/bound_dd:.4f})")
        print(f"  max D_max+||C||   = {max_sum_pos:.4f} (ratio={max_sum_pos/bound_dd:.4f})")
        print(f"  max λ_max         = {max_lam:.4f} (ratio={max_lam/bound_dd:.4f})")
        print(f"  max |λ_min|       = {max_abs_lam_min:.4f} (ratio={max_abs_lam_min/bound_dd:.4f})")

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print(f"\n{'='*70}")
    print("APPROACH B SUMMARY")
    print(f"{'='*70}")
    print(f"Best |D_min| + ||C|| found: {best_global:.6f}")
    print(f"Bound 4d = {bound_4d}")
    print(f"Slack: {bound_4d - best_global:.4f}")
    holds = best_global < bound_4d + 0.01
    print(f"|D_min| + ||C|| ≤ 4d: {'HOLDS (no violations)' if holds else 'VIOLATED'}")

    if best_global_info:
        print(f"\nExtremal config: |D_min|={best_global_info['abs_D_min']:.4f}, "
              f"||C||={best_global_info['C_norm']:.4f}")
        print(f"  λ_max={best_global_info['lam_max']:.4f}, λ_min={best_global_info['lam_min']:.4f}")

    return best_global < bound_4d + 0.01


if __name__ == "__main__":
    main()
