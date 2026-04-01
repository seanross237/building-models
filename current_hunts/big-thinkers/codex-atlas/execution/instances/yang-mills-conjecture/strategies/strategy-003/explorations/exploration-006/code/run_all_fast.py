"""
Unified runner using fast Hessian. All three approaches: B, C, A.
"""

import numpy as np
import sys, os, time
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, su2_exp, su2_inv, project_su2,
    flat_config, random_config, anti_instanton_config, isigma
)
from fast_hessian import (
    compute_hessian_fast as compute_hessian,
    compute_hessian_decomposed_fast as compute_hessian_decomposed,
    compute_per_plaquette_hessian_fast as compute_per_plaquette_hessian,
)

OUT = "/tmp/e006_results.txt"
f_out = open(OUT, "w", buffering=1)  # line-buffered

def log(msg=""):
    print(msg, flush=True)
    f_out.write(msg + "\n")

def analyze(lat, Q):
    D, C = compute_hessian_decomposed(lat, Q)
    evals_C = np.linalg.eigvalsh(C)
    C_norm = max(abs(evals_C[0]), abs(evals_C[-1]))
    H = np.diag(D) + C
    evals_H = np.linalg.eigvalsh(H)
    return {
        'D_min': np.min(D), 'D_max': np.max(D),
        'C_norm': C_norm,
        'lam_min': evals_H[0], 'lam_max': evals_H[-1],
        'abs_D_min': abs(np.min(D)),
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

def geodesic_interp(Q1, Q2, t):
    return [Q1[e] @ su2_exp(t * su2_log(su2_inv(Q1[e]) @ Q2[e])) for e in range(len(Q1))]

def lambda_max_H(lat, Q):
    return np.max(np.linalg.eigvalsh(compute_hessian(lat, Q)))


# ======================================================================
def run_B(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    log(f"\n{'='*70}")
    log(f"APPROACH B: D/C ANTI-CORRELATION (d={d}, bound=4d={bound})")
    log(f"{'='*70}")

    # Phase 1: Random survey
    log(f"\n--- Phase 1: Random survey (500 configs) ---")
    t0 = time.time()
    results = []
    for i in range(500):
        Q = random_config(lat, rng)
        info = analyze(lat, Q)
        results.append(info)
        if i % 100 == 0:
            log(f"  {i}/500...")
    elapsed = time.time() - t0
    log(f"Done in {elapsed:.1f}s")

    sum_negs = [r['sum_neg'] for r in results]
    sum_poss = [r['sum_pos'] for r in results]
    max_sn = max(sum_negs)
    max_sp = max(sum_poss)

    log(f"|D_min|+||C||: max={max_sn:.6f}, mean={np.mean(sum_negs):.4f}")
    log(f"D_max+||C||:   max={max_sp:.6f}, mean={np.mean(sum_poss):.4f}")
    log(f"Violations (>{bound}): neg={sum(1 for x in sum_negs if x > bound)}, pos={sum(1 for x in sum_poss if x > bound)}")
    log(f"λ_max: max={max(r['lam_max'] for r in results):.6f}")
    log(f"|λ_min|: max={max(abs(r['lam_min']) for r in results):.6f}")

    # Slack analysis
    for K in [bound, bound-1, bound-2, bound-3, bound-4]:
        n_viol = sum(1 for x in sum_negs if x > K + 0.001)
        log(f"  |D_min|+||C|| ≤ {K:.0f}: {n_viol}/500 violations")

    # Phase 2: Structured
    log(f"\n--- Phase 2: Structured configs ---")
    structured = [
        ('flat', flat_config(lat)),
        ('anti-instanton', anti_instanton_config(lat)),
    ]
    for ax in range(3):
        Q = []
        for mu in range(d):
            for site in lat.sites:
                if sum(site) % 2 == 0:
                    Q.append(np.eye(2, dtype=complex))
                else:
                    Q.append(isigma[ax].copy())
        structured.append((f'checker-I/iσ{ax}', Q))

    for theta in [np.pi/4, np.pi/2, 2*np.pi/3, np.pi]:
        w = np.zeros(3); w[2] = theta
        Qe = su2_exp(w)
        structured.append((f'uniform-θ={theta:.3f}', [Qe.copy() for _ in range(ne)]))

    for axes in [[0,1,2,0], [0,1,0,1]]:
        for theta in [np.pi/2, np.pi]:
            Q = []
            for mu in range(d):
                w = np.zeros(3); w[axes[mu]] = theta
                Qmu = su2_exp(w)
                for _ in range(lat.nsites):
                    Q.append(Qmu.copy())
            structured.append((f'perdir-{axes}-θ={theta:.2f}', Q))

    log(f"{'config':35s} {'|D_min|':>8s} {'||C||':>8s} {'sum_neg':>8s} {'sum_pos':>8s} {'λ_max':>8s} {'|λ_min|':>8s}")
    log("-" * 95)
    for name, Q in structured:
        info = analyze(lat, Q)
        log(f"{name:35s} {info['abs_D_min']:8.4f} {info['C_norm']:8.4f} "
              f"{info['sum_neg']:8.4f} {info['sum_pos']:8.4f} {info['lam_max']:8.4f} {abs(info['lam_min']):8.4f}")
        max_sn = max(max_sn, info['sum_neg'])
        max_sp = max(max_sp, info['sum_pos'])

    # Phase 3: Stochastic ascent on |D_min|+||C||
    log(f"\n--- Phase 3: Stochastic ascent on |D_min|+||C|| ---")
    rng2 = np.random.default_rng(12345)
    best_global = max(max_sn, max_sp)

    starts = [
        ('random', random_config(lat, rng2)),
        ('random2', random_config(lat, rng2)),
        ('random3', random_config(lat, rng2)),
        ('anti-inst', anti_instanton_config(lat)),
    ]
    Q_ai = anti_instanton_config(lat)
    starts.append(('pert-AI', [su2_exp(0.3*rng2.normal(size=3)) @ q for q in Q_ai]))
    starts.append(('pert-AI2', [su2_exp(0.5*rng2.normal(size=3)) @ q for q in Q_ai]))

    for target in ['sum_neg', 'sum_pos']:
        log(f"\n  Target: {target}")
        for name, Q_init in starts:
            Q = [q.copy() for q in Q_init]
            best_val = analyze(lat, Q)[target]

            for it in range(300):
                Q_trial = [q.copy() for q in Q]
                n_p = max(1, ne // 4)
                edges = rng2.choice(ne, n_p, replace=False)
                lr = 0.04 / (1 + it/150)
                for e in edges:
                    Q_trial[e] = su2_exp(lr * rng2.normal(size=3)) @ Q_trial[e]
                    Q_trial[e] = project_su2(Q_trial[e])
                trial_val = analyze(lat, Q_trial)[target]
                if trial_val > best_val:
                    Q = Q_trial
                    best_val = trial_val

            info_f = analyze(lat, Q)
            log(f"    {name:12s}: {target}={best_val:.6f}, "
                  f"|D_min|={info_f['abs_D_min']:.3f}, ||C||={info_f['C_norm']:.3f}, "
                  f"λ_max={info_f['lam_max']:.4f}, |λ_min|={abs(info_f['lam_min']):.4f}")
            best_global = max(best_global, best_val)

    # Phase 4: Dimension scan
    log(f"\n--- Phase 4: Dimension scan ---")
    for dd in [2, 3, 4]:
        lat_d = Lattice(dd, 2)
        rng_d = np.random.default_rng(42)
        bd = 4*dd
        max_sn_d = 0; max_sp_d = 0
        for _ in range(200):
            Q = random_config(lat_d, rng_d)
            info = analyze(lat_d, Q)
            max_sn_d = max(max_sn_d, info['sum_neg'])
            max_sp_d = max(max_sp_d, info['sum_pos'])
        log(f"  d={dd}: max|D_min|+||C||={max_sn_d:.4f}/{bd}, maxD_max+||C||={max_sp_d:.4f}/{bd}")

    log(f"\n--- APPROACH B RESULT ---")
    holds = best_global < bound + 0.01
    log(f"Best combined sum found: {best_global:.6f}")
    log(f"Bound 4d = {bound}, slack = {bound - best_global:.4f}")
    log(f"|D|+||C|| ≤ 4d: {'HOLDS' if holds else 'VIOLATED'}")
    return holds, best_global, results


# ======================================================================
def run_C(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    log(f"\n{'='*70}")
    log(f"APPROACH C: CONCAVITY / LOCAL MAXIMUM (d={d}, bound=4d={bound})")
    log(f"{'='*70}")

    # Test 1: Midpoint concavity
    log(f"\n--- Test 1: Midpoint concavity (100 geodesics) ---")
    max_viol = -np.inf
    n_violated = 0

    for trial in range(100):
        Q1 = random_config(lat, rng)
        Q2 = random_config(lat, rng)
        t_vals = np.linspace(0, 1, 9)
        f_vals = [lambda_max_H(lat, geodesic_interp(Q1, Q2, t)) for t in t_vals]
        f0, f1 = f_vals[0], f_vals[-1]
        for i, t in enumerate(t_vals):
            viol = (1-t)*f0 + t*f1 - f_vals[i]
            if viol > max_viol:
                max_viol = viol
            if viol > 1e-6:
                n_violated += 1
                break
        if trial % 25 == 0:
            log(f"  trial {trial}: max_viol={max_viol:.6e}, violated={n_violated}/{trial+1}")

    concavity_holds = n_violated == 0
    log(f"Random-random: {n_violated}/100 violate concavity (max_viol={max_viol:.6e})")

    # Flat-to-random
    log(f"\n--- Geodesics from flat ---")
    Q_flat = flat_config(lat)
    mv_flat = -np.inf; nv_flat = 0
    for trial in range(50):
        Q2 = random_config(lat, rng)
        t_vals = np.linspace(0, 1, 11)
        f_vals = [lambda_max_H(lat, geodesic_interp(Q_flat, Q2, t)) for t in t_vals]
        f0, f1 = f_vals[0], f_vals[-1]
        for i, t in enumerate(t_vals):
            viol = (1-t)*f0 + t*f1 - f_vals[i]
            mv_flat = max(mv_flat, viol)
            if viol > 1e-6:
                nv_flat += 1; break
    log(f"Flat-random: {nv_flat}/50 violated (max_viol={mv_flat:.6e})")

    # Test 2: Gradient ascent on λ_max
    log(f"\n--- Test 2: Stochastic ascent on λ_max ---")
    rng2 = np.random.default_rng(123)
    conv_results = []

    starts = [(f'random-{i}', random_config(lat, rng2)) for i in range(8)]
    starts.append(('anti-inst', anti_instanton_config(lat)))
    Q_ai = anti_instanton_config(lat)
    starts.append(('pert-AI', [su2_exp(0.5*rng2.normal(size=3)) @ q for q in Q_ai]))

    for name, Q_init in starts:
        Q = [q.copy() for q in Q_init]
        best_lmax = lambda_max_H(lat, Q)
        for it in range(200):
            Q_trial = [q.copy() for q in Q]
            n_p = max(1, ne // 4)
            edges = rng2.choice(ne, n_p, replace=False)
            lr = 0.04 / (1 + it/150)
            for e in edges:
                Q_trial[e] = su2_exp(lr * rng2.normal(size=3)) @ Q_trial[e]
                Q_trial[e] = project_su2(Q_trial[e])
            lmax_t = lambda_max_H(lat, Q_trial)
            if lmax_t > best_lmax:
                Q = Q_trial; best_lmax = lmax_t

        max_dist = max(min(np.linalg.norm(q - np.eye(2, dtype=complex)),
                          np.linalg.norm(q + np.eye(2, dtype=complex))) for q in Q)
        near_flat = max_dist < 0.5
        log(f"  {name:15s}: λ_max={best_lmax:.6f}, near_flat={near_flat} (dist={max_dist:.3f})")
        conv_results.append({'name': name, 'lmax': best_lmax, 'near_flat': near_flat})

    # Test 3: Second derivative
    log(f"\n--- Test 3: d²λ_max/dε² ---")
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
        log(f"  {cname}: λ_max={lam0:.4f}, d²: min={d2.min():.4f}, max={d2.max():.4f}, all_neg={np.all(d2<0)}")

    log(f"\n--- APPROACH C RESULT ---")
    log(f"Concavity: {'HOLDS' if concavity_holds else 'FAILS'}")
    all_near = all(r['lmax'] > bound - 1 for r in conv_results)
    log(f"All converge to near-flat (λ_max>{bound-1})? {all_near}")
    return concavity_holds, conv_results


# ======================================================================
def run_A(d=4, L=2):
    lat = Lattice(d, L)
    ne = lat.nedges
    bound = 4 * d
    rng = np.random.default_rng(42)

    log(f"\n{'='*70}")
    log(f"APPROACH A: PER-PLAQUETTE HESSIAN (d={d}, bound=4d={bound})")
    log(f"{'='*70}")

    # Phase 1: Flat
    log(f"\n--- Phase 1: Flat ---")
    Q = flat_config(lat)
    norms = []
    for pidx in range(lat.nplaq):
        H_p = compute_per_plaquette_hessian(lat, Q, pidx)
        ev = np.linalg.eigvalsh(H_p)
        norms.append(max(abs(ev[0]), abs(ev[-1])))
    log(f"||H_□|| at flat: min={min(norms):.4f}, max={max(norms):.4f}")

    # Verify sum
    H_full = compute_hessian(lat, Q)
    H_sum = sum(compute_per_plaquette_hessian(lat, Q, pidx) for pidx in range(lat.nplaq))
    log(f"||H - Σ H_□|| = {np.max(np.abs(H_full - H_sum)):.2e}")

    # Phase 2: Random survey
    log(f"\n--- Phase 2: Random survey (200 configs) ---")
    max_pn = 0; n_viol = 0
    t0 = time.time()
    for trial in range(200):
        Q = random_config(lat, rng)
        mx = 0
        for pidx in range(lat.nplaq):
            H_p = compute_per_plaquette_hessian(lat, Q, pidx)
            ev = np.linalg.eigvalsh(H_p)
            mx = max(mx, max(abs(ev[0]), abs(ev[-1])))
        if mx > 4.001: n_viol += 1
        max_pn = max(max_pn, mx)
        if trial % 50 == 0:
            log(f"  trial {trial}: max_so_far={max_pn:.6f}")
    log(f"Done in {time.time()-t0:.1f}s. max||H_□||={max_pn:.6f}, violations(>4)={n_viol}/200")

    # Phase 3: Structured
    log(f"\n--- Phase 3: Structured ---")
    Q_ai = anti_instanton_config(lat)
    norms_ai = []
    for pidx in range(lat.nplaq):
        H_p = compute_per_plaquette_hessian(lat, Q_ai, pidx)
        ev = np.linalg.eigvalsh(H_p)
        norms_ai.append(max(abs(ev[0]), abs(ev[-1])))
    log(f"Anti-instanton: max||H_□||={max(norms_ai):.6f}, mean={np.mean(norms_ai):.4f}")
    max_pn = max(max_pn, max(norms_ai))

    # Phase 4: Graph coloring
    log(f"\n--- Phase 4: Graph coloring ---")
    colors = [-1] * lat.nplaq
    n_colors = 0
    for pidx in range(lat.nplaq):
        edges_p = set(e for (e, s) in lat.plaquettes[pidx])
        nbr_colors = set()
        for e in edges_p:
            for pidx2 in lat.edge_plaquettes[e]:
                if pidx2 != pidx and colors[pidx2] >= 0:
                    nbr_colors.add(colors[pidx2])
        c = 0
        while c in nbr_colors: c += 1
        colors[pidx] = c
        n_colors = max(n_colors, c + 1)

    log(f"Greedy coloring: {n_colors} colors")
    all_disjoint = True
    for c in range(n_colors):
        cls = [i for i in range(lat.nplaq) if colors[i] == c]
        all_e = []
        for pidx in cls:
            all_e.extend([e for (e, s) in lat.plaquettes[pidx]])
        cnts = Counter(all_e)
        mx_c = max(cnts.values()) if cnts else 0
        if mx_c > 1: all_disjoint = False
        log(f"  Color {c}: {len(cls)} plaquettes, max edge overlap={mx_c}")

    log(f"\n--- APPROACH A RESULT ---")
    pp_holds = max_pn < 4.001
    log(f"||H_□|| ≤ 4: {'YES' if pp_holds else 'NO'} (max={max_pn:.6f})")
    log(f"Coloring: {n_colors} colors, edge-disjoint={all_disjoint}")
    if pp_holds and all_disjoint and n_colors <= d:
        log(f"*** PROOF VIABLE: ||H|| ≤ {n_colors}×4 = {n_colors*4} ≤ 4d={bound} ***")
    elif pp_holds and n_colors > d:
        log(f"Per-plaquette holds but need {n_colors} > d={d} colors — too many")
    elif not pp_holds:
        log(f"Per-plaquette bound FAILS")
    return pp_holds, n_colors, max_pn


# ======================================================================
if __name__ == "__main__":
    t_start = time.time()

    holds_B, best_B, res_B = run_B()
    holds_C, conv_C = run_C()
    holds_A, ncol_A, maxn_A = run_A()

    total = time.time() - t_start

    log(f"\n{'='*70}")
    log(f"FINAL SUMMARY (total: {total:.0f}s)")
    log(f"{'='*70}")
    log(f"B (anti-correlation): |D|+||C|| ≤ 4d {'HOLDS' if holds_B else 'FAILS'} (best={best_B:.4f}/16)")
    log(f"C (concavity):        {'HOLDS' if holds_C else 'FAILS'}")
    all_conv = all(r['lmax'] > 15.0 for r in conv_C)
    log(f"  Gradient ascent → flat? {all_conv}")
    log(f"A (per-plaquette):    ||H_□||≤4 {'YES' if holds_A else 'NO'} (max={maxn_A:.4f}), coloring={ncol_A}")

    f_out.close()
    log(f"\nResults saved to {OUT}")
