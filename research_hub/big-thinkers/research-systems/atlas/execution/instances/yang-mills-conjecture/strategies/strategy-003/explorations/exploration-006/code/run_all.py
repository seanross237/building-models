"""
Unified runner for all three approaches. Optimized for speed.
Runs B (anti-correlation), C (concavity), A (per-plaquette) in sequence.
"""

import numpy as np
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, su2_exp, project_su2,
    flat_config, random_config, anti_instanton_config,
    compute_hessian, compute_hessian_decomposed,
    compute_per_plaquette_hessian,
    plaquette_holonomy, isigma, get_link
)

def analyze_config(lat, Q, beta=1.0, N=2):
    """Compute D_min, D_max, ||C||, |λ(H)|_max."""
    D, C = compute_hessian_decomposed(lat, Q, beta, N)
    evals_C = np.linalg.eigvalsh(C)
    C_norm = max(abs(evals_C[0]), abs(evals_C[-1]))
    H = np.diag(D) + C
    evals_H = np.linalg.eigvalsh(H)
    return {
        'D_min': np.min(D), 'D_max': np.max(D),
        'C_norm': C_norm,
        'lam_min': evals_H[0], 'lam_max': evals_H[-1],
        'abs_D_min': abs(np.min(D)), 'abs_D_max': abs(np.max(D)),
        'sum_neg': abs(np.min(D)) + C_norm,
        'sum_pos': np.max(D) + C_norm,
    }

def su2_log(U):
    cos_theta = np.clip(np.real(np.trace(U)) / 2.0, -1, 1)
    theta = np.arccos(cos_theta)
    if abs(theta) < 1e-12:
        return np.zeros(3)
    U_tl = U - cos_theta * np.eye(2, dtype=complex)
    w = np.zeros(3)
    for a in range(3):
        w[a] = np.real(np.trace((-isigma[a]) @ U_tl)) / (2.0 * np.sin(theta)) * theta
    return w

def geodesic_interpolation(Q1, Q2, t):
    Q_t = []
    for e in range(len(Q1)):
        Delta = su2_inv(Q1[e]) @ Q2[e]
        w = su2_log(Delta)
        Q_t.append(Q1[e] @ su2_exp(t * w))
    return Q_t

def lambda_max_H(lat, Q):
    H = compute_hessian(lat, Q)
    return np.max(np.linalg.eigvalsh(H))

# ======================================================================
# APPROACH B: D/C ANTI-CORRELATION
# ======================================================================
def run_approach_B(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    print(f"\n{'='*70}")
    print(f"APPROACH B: D/C ANTI-CORRELATION BOUND (d={d}, bound=4d={bound})")
    print(f"{'='*70}")

    # Phase 1: Random survey
    print(f"\n--- Phase 1: Random survey (1000 configs) ---")
    t0 = time.time()
    results = []
    for _ in range(1000):
        Q = random_config(lat, rng)
        info = analyze_config(lat, Q)
        results.append(info)
    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.1f}s")

    sum_negs = [r['sum_neg'] for r in results]
    sum_poss = [r['sum_pos'] for r in results]
    max_sum_neg = max(sum_negs)
    max_sum_pos = max(sum_poss)

    print(f"|D_min|+||C||: max={max_sum_neg:.6f}, mean={np.mean(sum_negs):.4f}, violations(>{bound})={sum(1 for x in sum_negs if x > bound)}")
    print(f"D_max+||C||:   max={max_sum_pos:.6f}, mean={np.mean(sum_poss):.4f}, violations(>{bound})={sum(1 for x in sum_poss if x > bound)}")
    print(f"λ_max:  max={max(r['lam_max'] for r in results):.6f}")
    print(f"|λ_min|: max={max(abs(r['lam_min']) for r in results):.6f}")

    # Phase 2: Structured configs
    print(f"\n--- Phase 2: Structured configs ---")
    structured = [
        ('flat', flat_config(lat)),
        ('anti-instanton', anti_instanton_config(lat)),
    ]
    # Checkerboard I/iσ
    for ax in range(3):
        Q = []
        for mu in range(d):
            for site in lat.sites:
                if sum(site) % 2 == 0:
                    Q.append(np.eye(2, dtype=complex))
                else:
                    Q.append(isigma[ax].copy())
        structured.append((f'checker-I/iσ{ax}', Q))

    # Uniform rotations
    for theta in [np.pi/4, np.pi/2, 2*np.pi/3, np.pi]:
        w = np.zeros(3); w[2] = theta
        Q_e = su2_exp(w)
        structured.append((f'uniform-θ={theta:.3f}', [Q_e.copy() for _ in range(ne)]))

    # Per-direction non-commuting
    for axes in [[0,1,2,0], [0,1,0,1]]:
        for theta in [np.pi/2, np.pi]:
            Q = []
            for mu in range(d):
                w = np.zeros(3); w[axes[mu]] = theta
                Q_mu = su2_exp(w)
                for _ in range(lat.nsites):
                    Q.append(Q_mu.copy())
            structured.append((f'perdir-{axes}-θ={theta:.2f}', Q))

    print(f"{'config':35s} {'|D_min|':>8s} {'||C||':>8s} {'sum_neg':>8s} {'sum_pos':>8s} {'λ_max':>8s} {'|λ_min|':>8s}")
    print("-" * 95)
    for name, Q in structured:
        info = analyze_config(lat, Q)
        print(f"{name:35s} {info['abs_D_min']:8.4f} {info['C_norm']:8.4f} "
              f"{info['sum_neg']:8.4f} {info['sum_pos']:8.4f} {info['lam_max']:8.4f} {abs(info['lam_min']):8.4f}")
        max_sum_neg = max(max_sum_neg, info['sum_neg'])
        max_sum_pos = max(max_sum_pos, info['sum_pos'])

    # Phase 3: Targeted gradient ascent — maximize |D_min|+||C|| via random coordinate ascent
    print(f"\n--- Phase 3: Stochastic gradient ascent on |D_min|+||C|| ---")
    rng2 = np.random.default_rng(12345)
    best_global_sum = max_sum_neg

    starts = [
        ('random', random_config(lat, rng2)),
        ('random2', random_config(lat, rng2)),
        ('random3', random_config(lat, rng2)),
        ('anti-inst', anti_instanton_config(lat)),
    ]
    # Perturbed anti-instanton
    Q_ai = anti_instanton_config(lat)
    starts.append(('pert-AI', [su2_exp(0.3*rng2.normal(size=3)) @ q for q in Q_ai]))
    starts.append(('pert-AI2', [su2_exp(0.5*rng2.normal(size=3)) @ q for q in Q_ai]))

    for name, Q_init in starts:
        Q = [q.copy() for q in Q_init]
        info0 = analyze_config(lat, Q)
        best_val = info0['sum_neg']
        best_Q = [q.copy() for q in Q]

        # Stochastic coordinate ascent
        for it in range(300):
            Q_trial = [q.copy() for q in Q]
            n_perturb = max(1, ne // 4)
            edges = rng2.choice(ne, n_perturb, replace=False)
            lr = 0.03 / (1 + it/200)
            for e in edges:
                Q_trial[e] = su2_exp(lr * rng2.normal(size=3)) @ Q_trial[e]
                Q_trial[e] = project_su2(Q_trial[e])

            info_trial = analyze_config(lat, Q_trial)
            if info_trial['sum_neg'] > best_val:
                Q = Q_trial
                best_val = info_trial['sum_neg']
                best_Q = [q.copy() for q in Q]

            if it % 100 == 0:
                info_curr = analyze_config(lat, Q)
                print(f"  {name} iter {it}: |D_min|+||C||={info_curr['sum_neg']:.4f}")

        info_final = analyze_config(lat, best_Q)
        print(f"  {name} FINAL: |D_min|+||C||={best_val:.6f}, "
              f"|D_min|={info_final['abs_D_min']:.3f}, ||C||={info_final['C_norm']:.3f}, "
              f"λ_max={info_final['lam_max']:.4f}, λ_min={info_final['lam_min']:.4f}")

        if best_val > best_global_sum:
            best_global_sum = best_val
            print(f"  *** NEW GLOBAL BEST ***")

    # Also try maximizing sum_pos
    print(f"\n--- Phase 3b: Maximize D_max + ||C|| ---")
    for name, Q_init in starts[:3]:
        Q = [q.copy() for q in Q_init]
        best_val = analyze_config(lat, Q)['sum_pos']

        for it in range(300):
            Q_trial = [q.copy() for q in Q]
            n_perturb = max(1, ne // 4)
            edges = rng2.choice(ne, n_perturb, replace=False)
            lr = 0.03 / (1 + it/200)
            for e in edges:
                Q_trial[e] = su2_exp(lr * rng2.normal(size=3)) @ Q_trial[e]
                Q_trial[e] = project_su2(Q_trial[e])

            info_trial = analyze_config(lat, Q_trial)
            if info_trial['sum_pos'] > best_val:
                Q = Q_trial
                best_val = info_trial['sum_pos']

        info_f = analyze_config(lat, Q)
        print(f"  {name}: D_max+||C||={best_val:.6f}, D_max={info_f['D_max']:.3f}, "
              f"||C||={info_f['C_norm']:.3f}")
        if best_val > best_global_sum:
            best_global_sum = best_val

    # Phase 4: Tradeoff analysis
    print(f"\n--- Phase 4: Tradeoff curve ---")
    pairs = [(r['abs_D_min'], r['C_norm']) for r in results]
    for name, Q in structured:
        info = analyze_config(lat, Q)
        pairs.append((info['abs_D_min'], info['C_norm']))

    abs_d_vals = [p[0] for p in pairs]
    c_vals = [p[1] for p in pairs]
    print(f"max |D_min| = {max(abs_d_vals):.4f} (with ||C||={c_vals[np.argmax(abs_d_vals)]:.4f})")
    print(f"max ||C||   = {max(c_vals):.4f} (with |D_min|={abs_d_vals[np.argmax(c_vals)]:.4f})")

    for K in [bound, bound-0.5, bound-1, bound-2, bound-3]:
        n_viol = sum(1 for d_v, c_v in pairs if d_v + c_v > K + 0.001)
        print(f"  |D_min|+||C|| ≤ {K:.1f}: {n_viol} violations")

    # Phase 5: Dimension scan
    print(f"\n--- Phase 5: Dimension scan ---")
    for dd in [2, 3, 4]:
        lat_d = Lattice(dd, 2)
        rng_d = np.random.default_rng(42)
        bd = 4*dd
        max_sn = 0
        max_sp = 0
        for _ in range(300):
            Q = random_config(lat_d, rng_d)
            info = analyze_config(lat_d, Q)
            max_sn = max(max_sn, info['sum_neg'])
            max_sp = max(max_sp, info['sum_pos'])
        print(f"d={dd}: max |D_min|+||C||={max_sn:.4f}/{bd}, max D_max+||C||={max_sp:.4f}/{bd}")

    # Summary
    print(f"\n--- APPROACH B RESULT ---")
    holds = best_global_sum < bound + 0.01
    print(f"Best |D_min|+||C|| found: {best_global_sum:.6f}")
    print(f"Bound 4d = {bound}, slack = {bound - best_global_sum:.4f}")
    print(f"|D_min|+||C|| ≤ 4d: {'HOLDS' if holds else 'VIOLATED'}")
    return holds, best_global_sum, results


# ======================================================================
# APPROACH C: CONCAVITY / LOCAL MAXIMUM
# ======================================================================
def run_approach_C(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    print(f"\n{'='*70}")
    print(f"APPROACH C: CONCAVITY / LOCAL MAXIMUM (d={d}, bound=4d={bound})")
    print(f"{'='*70}")

    # Test 1: Midpoint concavity
    print(f"\n--- Test 1: Midpoint concavity of λ_max along geodesics ---")
    n_geodesics = 100
    max_viol = -np.inf
    n_violated = 0
    violations = []

    for trial in range(n_geodesics):
        Q1 = random_config(lat, rng)
        Q2 = random_config(lat, rng)

        t_vals = np.linspace(0, 1, 9)
        f_vals = [lambda_max_H(lat, geodesic_interpolation(Q1, Q2, t)) for t in t_vals]
        f0, f1 = f_vals[0], f_vals[-1]

        for i, t in enumerate(t_vals):
            linear = (1-t)*f0 + t*f1
            viol = linear - f_vals[i]
            if viol > max_viol:
                max_viol = viol
            if viol > 1e-6:
                n_violated += 1
                violations.append(viol)
                break  # One violation per geodesic is enough

        if trial % 25 == 0:
            print(f"  trial {trial}: max_viol={max_viol:.6e}, violated={n_violated}/{trial+1}")

    concavity_holds = n_violated == 0
    print(f"\nRandom-random: {n_violated}/{n_geodesics} geodesics violate concavity")
    print(f"Max violation: {max_viol:.6e}")

    if not concavity_holds:
        print("*** λ_max is NOT concave on SU(2)^E ***")
        if violations:
            print(f"Violation magnitudes: min={min(violations):.6e}, max={max(violations):.6e}")

    # Flat-to-random geodesics
    print(f"\n--- Geodesics from flat ---")
    Q_flat = flat_config(lat)
    max_viol_flat = -np.inf
    n_viol_flat = 0

    for trial in range(50):
        Q2 = random_config(lat, rng)
        t_vals = np.linspace(0, 1, 11)
        f_vals = [lambda_max_H(lat, geodesic_interpolation(Q_flat, Q2, t)) for t in t_vals]
        f0, f1 = f_vals[0], f_vals[-1]
        for i, t in enumerate(t_vals):
            viol = (1-t)*f0 + t*f1 - f_vals[i]
            max_viol_flat = max(max_viol_flat, viol)
            if viol > 1e-6:
                n_viol_flat += 1
                break

    print(f"Flat-random: {n_viol_flat}/50 violated, max_viol={max_viol_flat:.6e}")

    # Test 2: Gradient ascent on λ_max
    print(f"\n--- Test 2: Gradient ascent on λ_max ---")
    rng2 = np.random.default_rng(123)

    convergence_results = []
    starts = []
    for i in range(8):
        starts.append((f'random-{i}', random_config(lat, rng2)))
    starts.append(('anti-inst', anti_instanton_config(lat)))
    Q_ai = anti_instanton_config(lat)
    starts.append(('pert-AI', [su2_exp(0.5*rng2.normal(size=3)) @ q for q in Q_ai]))

    for name, Q_init in starts:
        Q = [q.copy() for q in Q_init]
        best_lmax = lambda_max_H(lat, Q)

        # Stochastic ascent
        for it in range(200):
            Q_trial = [q.copy() for q in Q]
            n_perturb = max(1, ne // 4)
            edges = rng2.choice(ne, n_perturb, replace=False)
            lr = 0.03 / (1 + it/150)
            for e in edges:
                Q_trial[e] = su2_exp(lr * rng2.normal(size=3)) @ Q_trial[e]
                Q_trial[e] = project_su2(Q_trial[e])

            lmax_trial = lambda_max_H(lat, Q_trial)
            if lmax_trial > best_lmax:
                Q = Q_trial
                best_lmax = lmax_trial

        # Check if near flat
        max_dist = max(min(np.linalg.norm(q - np.eye(2, dtype=complex)),
                          np.linalg.norm(q + np.eye(2, dtype=complex))) for q in Q)
        near_flat = max_dist < 0.5
        print(f"  {name:15s}: λ_max={best_lmax:.6f}, near_flat={near_flat} (dist={max_dist:.3f})")
        convergence_results.append({'name': name, 'lmax': best_lmax, 'near_flat': near_flat, 'dist': max_dist})

    # Test 3: Second derivative at various points
    print(f"\n--- Test 3: Second derivative of λ_max ---")
    for cname, Q0 in [('flat', flat_config(lat)), ('anti-inst', anti_instanton_config(lat))]:
        lam0 = lambda_max_H(lat, Q0)
        d2_vals = []
        eps = 0.02
        for _ in range(20):
            dw = [rng.normal(size=3) for _ in range(ne)]
            norm = np.sqrt(sum(np.linalg.norm(w)**2 for w in dw))
            dw = [w/norm for w in dw]
            f_m = lambda_max_H(lat, [su2_exp(-eps*w) @ q for w, q in zip(dw, Q0)])
            f_p = lambda_max_H(lat, [su2_exp(eps*w) @ q for w, q in zip(dw, Q0)])
            d2_vals.append((f_p - 2*lam0 + f_m) / eps**2)
        d2 = np.array(d2_vals)
        print(f"  {cname}: λ_max={lam0:.4f}, d²/dε²: min={d2.min():.4f}, max={d2.max():.4f}, all_neg={np.all(d2 < 0)}")

    # Summary
    print(f"\n--- APPROACH C RESULT ---")
    print(f"Concavity: {'HOLDS' if concavity_holds else 'FAILS'}")
    all_converge = all(r['lmax'] > bound - 1 for r in convergence_results)
    print(f"Gradient ascent → flat: all converge to λ_max≈{bound}? {all_converge}")
    return concavity_holds, convergence_results


# ======================================================================
# APPROACH A: PER-PLAQUETTE
# ======================================================================
def run_approach_A(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    print(f"\n{'='*70}")
    print(f"APPROACH A: PER-PLAQUETTE HESSIAN BOUND (d={d}, bound=4d={bound})")
    print(f"{'='*70}")

    # Phase 1: Flat
    print(f"\n--- Phase 1: Flat config ---")
    Q = flat_config(lat)
    norms = []
    for pidx in range(lat.nplaq):
        H_p = compute_per_plaquette_hessian(lat, Q, pidx)
        ev = np.linalg.eigvalsh(H_p)
        norms.append(max(abs(ev[0]), abs(ev[-1])))
    print(f"||H_□|| at flat: min={min(norms):.4f}, max={max(norms):.4f}")

    # Verify decomposition
    H_full = compute_hessian(lat, Q)
    H_sum = sum(compute_per_plaquette_hessian(lat, Q, pidx) for pidx in range(lat.nplaq))
    print(f"||H - Σ H_□|| = {np.max(np.abs(H_full - H_sum)):.2e}")

    # Phase 2: Random survey
    print(f"\n--- Phase 2: Random survey (500 configs) ---")
    max_plaq_norm = 0
    n_viol_4 = 0
    all_max_norms = []
    t0 = time.time()

    for trial in range(500):
        Q = random_config(lat, rng)
        norms = []
        for pidx in range(lat.nplaq):
            H_p = compute_per_plaquette_hessian(lat, Q, pidx)
            ev = np.linalg.eigvalsh(H_p)
            norms.append(max(abs(ev[0]), abs(ev[-1])))
        mn = max(norms)
        all_max_norms.append(mn)
        if mn > 4.001:
            n_viol_4 += 1
        max_plaq_norm = max(max_plaq_norm, mn)
        if trial % 100 == 0:
            print(f"  trial {trial}: max_so_far={max_plaq_norm:.6f}")

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s")
    print(f"max ||H_□|| = {max_plaq_norm:.6f}")
    print(f"||H_□|| > 4: {n_viol_4}/500 configs")

    # Phase 3: Anti-instanton
    print(f"\n--- Phase 3: Anti-instanton ---")
    Q = anti_instanton_config(lat)
    norms = []
    for pidx in range(lat.nplaq):
        H_p = compute_per_plaquette_hessian(lat, Q, pidx)
        ev = np.linalg.eigvalsh(H_p)
        norms.append(max(abs(ev[0]), abs(ev[-1])))
    print(f"Anti-instanton: max ||H_□|| = {max(norms):.6f}, mean = {np.mean(norms):.4f}")
    max_plaq_norm = max(max_plaq_norm, max(norms))

    # Phase 4: Graph coloring for aggregation
    print(f"\n--- Phase 4: Graph coloring ---")
    colors = [-1] * lat.nplaq
    n_colors = 0
    for pidx in range(lat.nplaq):
        edges_p = set(e for (e, s) in lat.plaquettes[pidx])
        neighbor_colors = set()
        for e in edges_p:
            for pidx2 in lat.edge_plaquettes[e]:
                if pidx2 != pidx and colors[pidx2] >= 0:
                    neighbor_colors.add(colors[pidx2])
        c = 0
        while c in neighbor_colors:
            c += 1
        colors[pidx] = c
        n_colors = max(n_colors, c + 1)

    print(f"Greedy coloring: {n_colors} colors")
    print(f"If ||H_□|| ≤ 4: triangle bound gives ||H|| ≤ {n_colors}×4 = {n_colors*4}")
    print(f"Target: 4d = {bound}")

    # But the per-plaquette-to-full-Hessian bound is actually:
    # λ_max(H) = λ_max(Σ H_□) ≤ Σ λ_max(H_□)
    # and λ_max(H_□) = max eigenvalue of H_□ (as full-dim matrix, so it's the norm).
    # We need a better aggregation!
    #
    # Better: for independent (non-overlapping) plaquettes in one color class,
    # H_{class} = Σ_{□ in class} H_□ and these act on disjoint supports,
    # so ||H_{class}|| = max_{□ in class} ||H_□|| ≤ 4.
    # Then ||H|| ≤ Σ_{classes} ||H_{class}|| ≤ n_colors × 4.

    # Check: within each color class, are plaquettes edge-disjoint?
    all_disjoint = True
    for c in range(n_colors):
        class_pidxs = [i for i in range(lat.nplaq) if colors[i] == c]
        all_edges = []
        for pidx in class_pidxs:
            all_edges.extend([e for (e, s) in lat.plaquettes[pidx]])
        from collections import Counter
        counts = Counter(all_edges)
        max_c = max(counts.values()) if counts else 0
        if max_c > 1:
            all_disjoint = False
        print(f"  Color {c}: {len(class_pidxs)} plaquettes, edge-disjoint? {max_c <= 1}")

    if all_disjoint:
        print(f"\nAll color classes are edge-disjoint!")
        print(f"=> ||H|| ≤ {n_colors} × max||H_□|| ≤ {n_colors} × {max_plaq_norm:.4f} = {n_colors*max_plaq_norm:.4f}")
    else:
        print(f"\nColor classes NOT edge-disjoint — norm bound requires more care")

    # Summary
    print(f"\n--- APPROACH A RESULT ---")
    per_plaq_holds = max_plaq_norm < 4.001
    print(f"Per-plaquette ||H_□|| ≤ 4: {'HOLDS' if per_plaq_holds else 'FAILS'} (max={max_plaq_norm:.6f})")
    if per_plaq_holds and all_disjoint and n_colors <= d:
        print(f"Aggregation: {n_colors} colors (≤ d={d}) + edge-disjoint => ||H|| ≤ {n_colors*4} = {bound}")
        print(f"*** PROOF STRATEGY VIABLE ***")
    else:
        if not per_plaq_holds:
            print(f"Per-plaquette bound fails — cannot use this approach")
        elif n_colors > d:
            print(f"Need {n_colors} colors > d={d} — aggregation too loose")
    return per_plaq_holds, n_colors, max_plaq_norm


# ======================================================================
# MAIN
# ======================================================================
if __name__ == "__main__":
    t_start = time.time()

    holds_B, best_sum_B, results_B = run_approach_B()
    holds_C, conv_C = run_approach_C()
    holds_A, n_colors_A, max_norm_A = run_approach_A()

    total = time.time() - t_start

    print(f"\n{'='*70}")
    print(f"FINAL SUMMARY (total time: {total:.1f}s)")
    print(f"{'='*70}")
    print(f"Approach B (anti-correlation): |D_min|+||C|| ≤ 4d {'HOLDS' if holds_B else 'FAILS'} (best={best_sum_B:.4f}/16)")
    print(f"Approach C (concavity):        λ_max concave? {'YES' if holds_C else 'NO'}")
    all_near = all(r['lmax'] > 15.0 for r in conv_C)
    print(f"  Gradient ascent → flat? {all_near}")
    print(f"Approach A (per-plaquette):     ||H_□|| ≤ 4? {'YES' if holds_A else 'NO'} (max={max_norm_A:.4f})")
    print(f"  Coloring: {n_colors_A} colors needed (need ≤ d=4)")
