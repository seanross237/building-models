"""
Stages 2-4 (VECTORIZED): Fully numpy-vectorized computation.
Key optimization: n = e1 = (1,0,0), so R*n = first column of R(q).
All 96 plaquettes computed simultaneously as numpy arrays.
"""

import numpy as np
from scipy.optimize import minimize
from itertools import product

# ─── Fast quaternion operations (batch) ────────────────────────────────────

def quat_mul_batch(q1, q2):
    """Batch quaternion multiply. Inputs shape (..., 4). Returns (..., 4)."""
    w1,x1,y1,z1 = q1[...,0], q1[...,1], q1[...,2], q1[...,3]
    w2,x2,y2,z2 = q2[...,0], q2[...,1], q2[...,2], q2[...,3]
    return np.stack([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ], axis=-1)

def quat_conj_batch(q):
    """Quaternion conjugate (= inverse for unit quaternions). Shape (..., 4)."""
    c = q.copy(); c[..., 1:] *= -1; return c

def quat_normalize(q):
    """Normalize quaternion(s). Shape (..., 4)."""
    return q / np.linalg.norm(q, axis=-1, keepdims=True)

def rotate_n_by_q(q, n):
    """
    Apply rotation corresponding to unit quaternion q to vector n.
    q shape: (..., 4)  (w,x,y,z); n shape: (3,)
    Returns: (..., 3)
    Formula: R*n = (2w^2-1)*n + 2(q_v·n)*q_v + 2w*(q_v×n)
    """
    w = q[..., 0]      # (...,)
    qv = q[..., 1:]    # (..., 3)
    qdotn = np.einsum('...i,i->...', qv, n)     # (...,)
    qcrossn = np.cross(qv, n)                    # (..., 3)
    return ((2*w**2 - 1)[..., np.newaxis] * n[np.newaxis, :]
            + 2 * qdotn[..., np.newaxis] * qv
            + 2 * w[..., np.newaxis] * qcrossn)

# ─── Lattice setup ────────────────────────────────────────────────────────────

L, d = 2, 4
vertices = list(product(range(L), repeat=d))
edges = [(x, mu) for x in vertices for mu in range(d)]
edge_to_idx = {e: i for i, e in enumerate(edges)}
n_edges = len(edges)  # 64

def add_mod(x, mu):
    y = list(x); y[mu] = (y[mu] + 1) % L; return tuple(y)

def stag_sign(x, mu): return (-1) ** (sum(x) + mu)

plaq_list = []
for x in vertices:
    for mu in range(d):
        for nu in range(mu + 1, d):
            xm, xn = add_mod(x, mu), add_mod(x, nu)
            e1,e2,e3,e4 = (x,mu),(xm,nu),(xn,mu),(x,nu)
            s1,s2,s3,s4 = stag_sign(*e1),stag_sign(*e2),stag_sign(*e3),stag_sign(*e4)
            plaq_list.append({
                'ei': [edge_to_idx[e] for e in [e1,e2,e3,e4]],
                'eff': (float(s1), float(s2), float(-s3), float(-s4)),
                'active': (mu+nu)%2==1, 'x': x, 'mu': mu, 'nu': nu
            })

n_plaq = len(plaq_list)  # 96
EI = np.array([p['ei'] for p in plaq_list], dtype=np.int32)   # (96, 4)
EFF = np.array([p['eff'] for p in plaq_list])                  # (96, 4)
ACTIVE = np.array([p['active'] for p in plaq_list])           # (96,) bool

edge_plaq_map = [[] for _ in range(n_edges)]
for pi, plaq in enumerate(plaq_list):
    for ei in plaq['ei']:
        edge_plaq_map[ei].append(pi)

# ─── Vectorized B_sq computation ──────────────────────────────────────────────

def compute_Bsq_all(quats, n_vec=None):
    """
    Compute |B_□|^2 for all 96 plaquettes. Returns shape (96,).
    quats: shape (n_edges, 4) — will be normalized internally.
    """
    if n_vec is None: n_vec = np.array([1., 0., 0.])
    quats = quat_normalize(quats)
    q1 = quats[EI[:,0]]; q2 = quats[EI[:,1]]
    q3 = quats[EI[:,2]]; q4 = quats[EI[:,3]]
    P1 = q1
    P2 = quat_normalize(quat_mul_batch(quat_mul_batch(q1, q2), quat_conj_batch(q3)))
    P3 = quat_normalize(quat_mul_batch(P2, quat_conj_batch(q4)))
    R1n = rotate_n_by_q(P1, n_vec)
    R2n = rotate_n_by_q(P2, n_vec)
    R3n = rotate_n_by_q(P3, n_vec)
    B = (EFF[:,0:1]*n_vec + EFF[:,1:2]*R1n + EFF[:,2:3]*R2n + EFF[:,3:4]*R3n)
    return (B*B).sum(axis=1)

def compute_total_Bsq_vec(quats, n_vec=None):
    return compute_Bsq_all(quats, n_vec).sum()

def identity_quats():
    q = np.zeros((n_edges, 4)); q[:, 0] = 1.0; return q

def random_quats():
    q = np.random.randn(n_edges, 4)
    return q / np.linalg.norm(q, axis=1, keepdims=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    np.random.seed(42)
    n_vec = np.array([1., 0., 0.])
    Q_I = identity_quats()

    print("=" * 65)
    print("SU(2) Yang-Mills: Staggered Mode Bound (Vectorized)")
    print("=" * 65)

    # ── Verify at Q=I ─────────────────────────────────────────────────────────
    bsq_I_all = compute_Bsq_all(Q_I, n_vec)
    Bsq_I = bsq_I_all.sum()
    print(f"\nSum |B_□|^2 at Q=I: {Bsq_I:.6f} (expected 1024)")
    assert abs(Bsq_I - 1024) < 1e-8
    print(f"  Active (64): each = {bsq_I_all[ACTIVE].mean():.2f}")
    print(f"  Inactive (32): each = {bsq_I_all[~ACTIVE].mean():.2f}")

    # ── Stage 1: Random sampling ──────────────────────────────────────────────
    print("\n--- Stage 1: Random config sampling (N=5000) ---")
    N = 5000
    vals = np.array([compute_total_Bsq_vec(random_quats(), n_vec) for _ in range(N)])
    print(f"  Max:  {vals.max():.6f}  [Conjecture bound: 1024]")
    print(f"  Mean: {vals.mean():.6f}")
    print(f"  Std:  {vals.std():.6f}")
    print(f"  Min:  {vals.min():.6f}")
    print(f"  Fraction > 900: {(vals > 900).mean():.4f}")
    print(f"  Any > 1024: {vals.max() > 1024 + 1e-6}")

    # ── Stage 2: Per-plaquette max via gradient ascent ────────────────────────
    print("\n--- Stage 2: Per-plaquette constrained max (gradient ascent) ---")

    def neg_single_plaq(q_flat, pi):
        """Negative |B_pi|^2 varying the 4 edges of plaquette pi."""
        Q = Q_I.copy()
        for k, ei in enumerate(plaq_list[pi]['ei']):
            q = q_flat[4*k:4*(k+1)]
            Q[ei] = q / max(np.linalg.norm(q), 1e-10)
        return -compute_Bsq_all(Q, n_vec)[pi]

    constrained_maxima = {}
    for pi, label in [(0, "Active"), (next(i for i,p in enumerate(plaq_list) if not p['active']), "Inactive")]:
        best = 0.0
        for trial in range(80):
            q_init = np.random.randn(16)
            for k in range(4): q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
            res = minimize(neg_single_plaq, q_init, args=(pi,), method='L-BFGS-B',
                           options={'maxiter': 300, 'ftol': 1e-12})
            if -res.fun > best: best = -res.fun
        p = plaq_list[pi]
        print(f"\n  {label} plaquette {pi}: "
              f"x={p['x']}, (mu,nu)=({p['mu']},{p['nu']}), eff={p['eff']}")
        print(f"    Constrained max |B_□|^2 = {best:.6f}")
        print(f"    Unconstrained max (4 free SO(3)) = 16.0")
        print(f"    Holonomy constraint reduces max: {best < 15.99}")
        constrained_maxima[label] = best

    # ── Stage 3: Vary single link + per-edge monotonicity ────────────────────
    print("\n--- Stage 3+3b: Single-link variation and per-edge monotonicity ---")
    t_vals = np.linspace(0, 2*np.pi, 100)
    global_max_total = 1024.0
    per_edge_violations = 0
    max_per_edge_gain = 0.0
    worst_edge_info = None

    for ei in range(n_edges):
        ep = edge_plaq_map[ei]
        baseline_ep = bsq_I_all[ep].sum()
        edge_local_max = baseline_ep
        global_best_for_edge = 1024.0

        for trial in range(5):
            axis = np.random.randn(3); axis /= np.linalg.norm(axis)
            for t in t_vals:
                Q = Q_I.copy()
                c, s = np.cos(t/2), np.sin(t/2)
                Q[ei] = np.array([c, s*axis[0], s*axis[1], s*axis[2]])
                Bsq = compute_Bsq_all(Q, n_vec)
                total = Bsq.sum()
                ep_sum = Bsq[ep].sum()
                if total > global_max_total: global_max_total = total
                if ep_sum > edge_local_max:
                    edge_local_max = ep_sum
                    if ep_sum - baseline_ep > max_per_edge_gain:
                        max_per_edge_gain = ep_sum - baseline_ep
                        worst_edge_info = (ei, axis.copy(), t, ep_sum, baseline_ep)

        if edge_local_max > baseline_ep + 1e-6:
            per_edge_violations += 1

    print(f"  Global max total Sum |B_□|^2 (all edges, 5 axes each): {global_max_total:.6f}")
    print(f"  Exceeds 1024: {global_max_total > 1024 + 1e-6}")
    print(f"  Per-edge monotonicity violations: {per_edge_violations}/{n_edges}")
    print(f"  Max per-edge gain over baseline: {max_per_edge_gain:.6f}")
    if per_edge_violations == 0:
        print("  => Per-edge monotonicity: HOLDS")
    else:
        print("  => Per-edge monotonicity: FAILS")
        if worst_edge_info:
            ei_w, ax_w, t_w, ep_sum_w, base_w = worst_edge_info
            print(f"  Worst: edge {ei_w}={edges[ei_w]}, gain={ep_sum_w-base_w:.4f}")

    # ── Detailed t-scan for edge 0, axis=(1,0,0) ─────────────────────────────
    print("\n--- Stage 3c: Detailed breakdown for edge 0, axis=(1,0,0) ---")
    t_dense = np.linspace(0, 2*np.pi, 500)
    ep0 = edge_plaq_map[0]
    active_ep0 = [pi for pi in ep0 if plaq_list[pi]['active']]
    inactive_ep0 = [pi for pi in ep0 if not plaq_list[pi]['active']]
    print(f"  Edge 0 = {edges[0]}, in {len(ep0)} plaquettes "
          f"({len(active_ep0)} active, {len(inactive_ep0)} inactive)")

    totals_e0 = np.zeros(len(t_dense))
    for ti, t in enumerate(t_dense):
        Q = Q_I.copy()
        c, s = np.cos(t/2), np.sin(t/2)
        Q[0] = np.array([c, s, 0., 0.])
        totals_e0[ti] = compute_total_Bsq_vec(Q, n_vec)

    t_max_idx = np.argmax(totals_e0)
    t_max = t_dense[t_max_idx]
    print(f"  Total sum: max={totals_e0.max():.6f} (at t={t_max:.4f}), "
          f"min={totals_e0.min():.6f}")

    Q_t = Q_I.copy()
    c, s = np.cos(t_max/2), np.sin(t_max/2)
    Q_t[0] = np.array([c, s, 0., 0.])
    Bsq_t = compute_Bsq_all(Q_t, n_vec)
    print(f"  At t_max, affected plaquettes:")
    for pi in ep0:
        pp = plaq_list[pi]
        print(f"    Plaq {pi} ({'A' if pp['active'] else 'I'}, "
              f"mu={pp['mu']},nu={pp['nu']}): "
              f"val={Bsq_t[pi]:.4f}, baseline={bsq_I_all[pi]:.1f}, "
              f"gain={Bsq_t[pi]-bsq_I_all[pi]:+.4f}")
    print(f"  Total active plaquette gain: {(Bsq_t[ACTIVE] - bsq_I_all[ACTIVE]).sum():+.4f}")
    print(f"  Total inactive plaquette gain: {(Bsq_t[~ACTIVE] - bsq_I_all[~ACTIVE]).sum():+.4f}")
    print(f"  Net total gain: {Bsq_t.sum() - 1024:+.4f}")

    # ── Stage 4: Decoherence — maximize plaquette 0 ──────────────────────────
    print("\n--- Stage 4: Decoherence at single-plaquette maximum ---")

    def neg_plaq0(q_flat):
        Q = Q_I.copy()
        for k, ei in enumerate(plaq_list[0]['ei']):
            q = q_flat[4*k:4*(k+1)]
            Q[ei] = q / max(np.linalg.norm(q), 1e-10)
        return -compute_Bsq_all(Q, n_vec)[0]

    best_p0 = 0.0; best_q_p0 = None
    for _ in range(150):
        q_init = np.random.randn(16)
        for k in range(4): q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
        res = minimize(neg_plaq0, q_init, method='L-BFGS-B',
                       options={'maxiter': 400, 'ftol': 1e-13})
        if -res.fun > best_p0: best_p0 = -res.fun; best_q_p0 = res.x

    Q_p0 = Q_I.copy()
    for k, ei in enumerate(plaq_list[0]['ei']):
        q = best_q_p0[4*k:4*(k+1)]; Q_p0[ei] = q / np.linalg.norm(q)

    Bsq_p0 = compute_Bsq_all(Q_p0, n_vec)
    gains_p0 = Bsq_p0 - bsq_I_all
    neighbors_0 = set()
    for ei in plaq_list[0]['ei']:
        for pj in edge_plaq_map[ei]:
            if pj != 0: neighbors_0.add(pj)
    neighbors_0 = sorted(neighbors_0)
    neigh_mask = np.zeros(n_plaq, dtype=bool)
    for pj in neighbors_0: neigh_mask[pj] = True

    print(f"\n  Plaquette 0: x={plaq_list[0]['x']}, "
          f"(mu,nu)=({plaq_list[0]['mu']},{plaq_list[0]['nu']}), Active")
    print(f"  Max |B_0|^2 = {best_p0:.6f} (possible max: 16)")
    print(f"  Total Sum |B_□|^2 at this config: {Bsq_p0.sum():.6f}")
    print(f"  Net change from Q=I: {Bsq_p0.sum() - 1024:+.6f}")
    print(f"  Gain breakdown:")
    print(f"    Plaquette 0 (target): {gains_p0[0]:+.4f}")
    print(f"    {len(neighbors_0)} neighbors: {gains_p0[neigh_mask].sum():+.4f}")
    print(f"      Active neighbors: {gains_p0[neigh_mask & ACTIVE].sum():+.4f}")
    print(f"      Inactive neighbors: {gains_p0[neigh_mask & ~ACTIVE].sum():+.4f}")
    other_mask = ~neigh_mask; other_mask[0] = False
    print(f"    Other plaquettes: {gains_p0[other_mask].sum():+.4f}")

    print(f"\n  Neighbor details:")
    for pj in neighbors_0:
        pp = plaq_list[pj]
        print(f"    Plaq {pj} ({'A' if pp['active'] else 'I'}, "
              f"mu={pp['mu']},nu={pp['nu']}): "
              f"val={Bsq_p0[pj]:.4f}, base={bsq_I_all[pj]:.1f}, "
              f"gain={gains_p0[pj]:+.4f}")

    # ── Stage 4b: Two-plaquette competition ────────────────────────────────────
    print("\n--- Stage 4b: Two-plaquette competition ---")
    # Find active pair sharing an edge
    active_pis = [i for i,p in enumerate(plaq_list) if p['active']]
    pair = None
    for pi1 in active_pis[:15]:
        for pi2 in active_pis:
            if pi2 <= pi1: continue
            shared = set(plaq_list[pi1]['ei']) & set(plaq_list[pi2]['ei'])
            if shared:
                pair = (pi1, pi2, list(shared)); break
        if pair: break

    if pair:
        pi1, pi2, sh = pair
        all_ei = list(set(plaq_list[pi1]['ei'] + plaq_list[pi2]['ei']))
        print(f"  Pair ({pi1},{pi2}) sharing edges {sh}")

        def neg_pair(q_flat):
            Q = Q_I.copy()
            for k, ei in enumerate(all_ei):
                q = q_flat[4*k:4*(k+1)]
                Q[ei] = q / max(np.linalg.norm(q), 1e-10)
            Bsq = compute_Bsq_all(Q, n_vec)
            return -(Bsq[pi1] + Bsq[pi2])

        best_pr = 0.0; best_q_pr = None
        for _ in range(100):
            q_init = np.random.randn(4*len(all_ei))
            for k in range(len(all_ei)):
                q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
            res = minimize(neg_pair, q_init, method='L-BFGS-B',
                           options={'maxiter': 400, 'ftol': 1e-13})
            if -res.fun > best_pr: best_pr = -res.fun; best_q_pr = res.x

        Q_pr = Q_I.copy()
        for k, ei in enumerate(all_ei):
            q = best_q_pr[4*k:4*(k+1)]; Q_pr[ei] = q / np.linalg.norm(q)
        Bsq_pr = compute_Bsq_all(Q_pr, n_vec)
        print(f"  Max |B_{pi1}|^2 + |B_{pi2}|^2 = {best_pr:.6f} (max possible: 32)")
        print(f"  Individual: |B_{pi1}|^2 = {Bsq_pr[pi1]:.6f}, |B_{pi2}|^2 = {Bsq_pr[pi2]:.6f}")
        print(f"  Total sum |B_□|^2 = {Bsq_pr.sum():.6f}")
        print(f"  Reduction from 32 (both at max): {32 - best_pr:.6f}")

    # ── Stage 4c: Active/inactive gain correlation (random) ───────────────────
    print("\n--- Stage 4c: Active vs inactive gain correlation ---")
    N_c = 2000
    ag = np.zeros(N_c); ig = np.zeros(N_c)
    for i in range(N_c):
        Bsq = compute_Bsq_all(random_quats(), n_vec)
        ag[i] = Bsq[ACTIVE].sum() - bsq_I_all[ACTIVE].sum()
        ig[i] = Bsq[~ACTIVE].sum()  # baseline inactive = 0
    tg = ag + ig

    print(f"  Active gain:   mean={ag.mean():.2f}, std={ag.std():.2f}, "
          f"max={ag.max():.2f}, min={ag.min():.2f}")
    print(f"  Inactive gain: mean={ig.mean():.2f}, std={ig.std():.2f}, "
          f"max={ig.max():.2f}, min={ig.min():.2f}")
    print(f"  Total gain:    mean={tg.mean():.2f}, std={tg.std():.2f}, "
          f"max={tg.max():.2f}")
    print(f"  Corr(active_gain, inactive_gain): {np.corrcoef(ag, ig)[0,1]:.6f}")
    print(f"  Active gains always <= 0: {(ag <= 1e-6).all()}")
    print(f"  Inactive gains always >= 0: {(ig >= -1e-6).all()}")
    print(f"  |Active_gain| always >= Inactive_gain (total <= 0): {(tg <= 1e-6).all()}")

    # For configs where inactive gain is large, how big is active loss?
    high_ig = ig > ig.mean() + ig.std()
    if high_ig.sum() > 0:
        print(f"  When inactive gain > mean+std ({high_ig.sum()} configs):")
        print(f"    Active gain: mean={ag[high_ig].mean():.2f}")
        print(f"    Total gain: mean={tg[high_ig].mean():.2f}, max={tg[high_ig].max():.2f}")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("FINAL SUMMARY")
    print("=" * 65)
    print(f"[VERIFIED] Q=I: Sum |B_□|^2 = 1024.0 = 4d × |v|^2")
    print(f"[COMPUTED] Random sampling (N={N}): max = {vals.max():.4f}, "
          f"{'≤ 1024 ✓' if vals.max() <= 1024.01 else '> 1024 ✗'}")
    print(f"[COMPUTED] Active per-plaquette constrained max = {constrained_maxima.get('Active', '?'):.4f}")
    print(f"           (unconstrained max = 16; holonomy does NOT reduce it)")
    print(f"[COMPUTED] Inactive per-plaquette constrained max = {constrained_maxima.get('Inactive', '?'):.4f}")
    print(f"[COMPUTED] Single-link variation: max = {global_max_total:.4f}, "
          f"{'≤ 1024 ✓' if global_max_total <= 1024.01 else '> 1024 ✗'}")
    print(f"[COMPUTED] Per-edge monotonicity: "
          f"{'HOLDS ✓' if per_edge_violations == 0 else f'FAILS ({per_edge_violations} violations) ✗'}, "
          f"max gain = {max_per_edge_gain:.4f}")
    print(f"[COMPUTED] Active gains always ≤ 0: {(ag <= 1e-6).all()}")
    print(f"[COMPUTED] Inactive gains always ≥ 0: {(ig >= -1e-6).all()}")
    print(f"[COMPUTED] Total (active+inactive) always ≤ 0: {(tg <= 1e-6).all()}")
    print(f"[COMPUTED] Two-plaquette max (sharing edge): {best_pr:.4f} vs 32 possible")
