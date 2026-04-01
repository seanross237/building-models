"""
Stages 2-4 (FAST VERSION): Per-plaquette max, holonomy constraint, cross-plaquette coupling.

Uses direct SO(3) rotation via quaternion formula instead of matrix multiplication.
Much faster than matrix-based approach.
"""

import numpy as np
from scipy.optimize import minimize
from itertools import product

# ─── Fast quaternion → SO(3) ──────────────────────────────────────────────────

def quat_to_R3(q):
    """
    Quaternion (w, x, y, z) → 3x3 SO(3) rotation matrix.
    q is normalized internally.
    """
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    R = np.array([
        [1 - 2*(y**2 + z**2),   2*(x*y - w*z),         2*(x*z + w*y)],
        [2*(x*y + w*z),          1 - 2*(x**2 + z**2),   2*(y*z - w*x)],
        [2*(x*z - w*y),          2*(y*z + w*x),          1 - 2*(x**2 + y**2)]
    ])
    return R

def quat_multiply(q1, q2):
    """Hamilton product of two quaternions (w,x,y,z)."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    """Inverse of unit quaternion = conjugate."""
    q = q / np.linalg.norm(q)
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quat_identity():
    return np.array([1., 0., 0., 0.])

def random_quat():
    """Haar-random unit quaternion."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    return q

def axis_angle_to_quat(axis, theta):
    """exp(theta/2 * axis) as quaternion."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    axis = axis / np.linalg.norm(axis)
    return np.array([c, s*axis[0], s*axis[1], s*axis[2]])

# ─── Lattice setup ────────────────────────────────────────────────────────────

L, d = 2, 4
vertices = list(product(range(L), repeat=d))
edges = [(x, mu) for x in vertices for mu in range(d)]
edge_to_idx = {e: i for i, e in enumerate(edges)}
n_edges = len(edges)  # 64

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def stag_sign(x, mu):
    return (-1) ** (sum(x) + mu)

plaquettes = []
for x in vertices:
    for mu in range(d):
        for nu in range(mu + 1, d):
            x_mu = add_mod(x, mu)
            x_nu = add_mod(x, nu)
            e1, e2, e3, e4 = (x, mu), (x_mu, nu), (x_nu, mu), (x, nu)
            s1, s2, s3, s4 = stag_sign(*e1), stag_sign(*e2), stag_sign(*e3), stag_sign(*e4)
            # Effective coefficients: (s1, s2, -s3, -s4)
            eff = np.array([s1, s2, -s3, -s4], dtype=float)
            plaquettes.append({
                'ei': [edge_to_idx[e] for e in [e1, e2, e3, e4]],
                'eff': eff,
                'active': (mu + nu) % 2 == 1,
                'mu': mu, 'nu': nu, 'x': x
            })

n_plaq = len(plaquettes)  # 96

# Edge → plaquette map (which plaquettes contain each edge)
edge_plaq_map = [[] for _ in range(n_edges)]
for pi, plaq in enumerate(plaquettes):
    for ei in plaq['ei']:
        edge_plaq_map[ei].append(pi)

# ─── Fast B_□ computation ─────────────────────────────────────────────────────

def compute_B_plaq_q(quats, pi, n_vec):
    """
    Fast |B_□|^2 computation using quaternion multiplication.
    quats: array of shape (n_edges, 4) — quaternion per edge
    Returns: |B_□|^2 scalar
    """
    plaq = plaquettes[pi]
    ei = plaq['ei']
    c1, c2, c3, c4 = plaq['eff']

    q1, q2, q3, q4 = quats[ei[0]], quats[ei[1]], quats[ei[2]], quats[ei[3]]

    # Partial holonomies as quaternions
    P1 = q1 / np.linalg.norm(q1)
    q3_inv = quat_inv(q3)
    q4_inv = quat_inv(q4)
    P2 = quat_multiply(quat_multiply(P1, q2 / np.linalg.norm(q2)), q3_inv)
    P2 /= np.linalg.norm(P2)
    P3 = quat_multiply(P2, q4_inv)
    P3 /= np.linalg.norm(P3)

    # Apply rotations
    R1 = quat_to_R3(P1)
    R2 = quat_to_R3(P2)
    R3 = quat_to_R3(P3)

    B = c1 * n_vec + c2 * (R1 @ n_vec) + c3 * (R2 @ n_vec) + c4 * (R3 @ n_vec)
    return np.dot(B, B)

def compute_total_Bsq_q(quats, n_vec=None):
    """Sum_□ |B_□|^2 for quaternion config."""
    if n_vec is None:
        n_vec = np.array([1., 0., 0.])
    total = 0.0
    for pi in range(n_plaq):
        total += compute_B_plaq_q(quats, pi, n_vec)
    return total

def identity_quats():
    """All links = identity quaternion."""
    return np.tile([1., 0., 0., 0.], (n_edges, 1))

# ─── Vectorized version for large random samples ──────────────────────────────

def compute_total_Bsq_batch(quats, n_vec=None):
    """
    Compute Sum |B_□|^2 for a SINGLE config (quats shape: n_edges × 4).
    Precomputes all SO(3) matrices.
    """
    if n_vec is None:
        n_vec = np.array([1., 0., 0.])
    # Normalize all quaternions
    norms = np.linalg.norm(quats, axis=1, keepdims=True)
    Q = quats / norms

    # Precompute all SO(3) matrices
    w, x, y, z = Q[:, 0], Q[:, 1], Q[:, 2], Q[:, 3]
    # R[i] = 3x3 rotation matrix for edge i
    R_all = np.zeros((n_edges, 3, 3))
    R_all[:, 0, 0] = 1 - 2*(y**2 + z**2)
    R_all[:, 0, 1] = 2*(x*y - w*z)
    R_all[:, 0, 2] = 2*(x*z + w*y)
    R_all[:, 1, 0] = 2*(x*y + w*z)
    R_all[:, 1, 1] = 1 - 2*(x**2 + z**2)
    R_all[:, 1, 2] = 2*(y*z - w*x)
    R_all[:, 2, 0] = 2*(x*z - w*y)
    R_all[:, 2, 1] = 2*(y*z + w*x)
    R_all[:, 2, 2] = 1 - 2*(x**2 + y**2)

    total = 0.0
    for pi, plaq in enumerate(plaquettes):
        ei = plaq['ei']
        c = plaq['eff']

        q1, q2, q3, q4 = Q[ei[0]], Q[ei[1]], Q[ei[2]], Q[ei[3]]
        q3_inv = np.array([q3[0], -q3[1], -q3[2], -q3[3]])
        q4_inv = np.array([q4[0], -q4[1], -q4[2], -q4[3]])

        P1 = q1
        P2 = quat_multiply(quat_multiply(P1, q2), q3_inv)
        P2 /= np.linalg.norm(P2)
        P3 = quat_multiply(P2, q4_inv)
        P3 /= np.linalg.norm(P3)

        R1 = quat_to_R3(P1)
        R2 = quat_to_R3(P2)
        R3 = quat_to_R3(P3)

        B = c[0]*n_vec + c[1]*(R1@n_vec) + c[2]*(R2@n_vec) + c[3]*(R3@n_vec)
        total += np.dot(B, B)
    return total

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    np.random.seed(42)
    n_vec = np.array([1., 0., 0.])

    print("=" * 65)
    print("SU(2) Yang-Mills: Staggered Mode Bound Analysis (Fast Version)")
    print("=" * 65)

    # Verify at Q=I
    Q_I = identity_quats()
    Bsq_I = compute_total_Bsq_q(Q_I, n_vec)
    print(f"\nSum |B_□|^2 at Q=I: {Bsq_I:.4f} (expected 1024)")
    assert abs(Bsq_I - 1024) < 1e-8, f"Expected 1024, got {Bsq_I}"
    print("Q=I check: PASSED")

    # ── Stage 1: Random sampling ──────────────────────────────────────────────
    print("\n--- Stage 1: Random config sampling (N=2000) ---")
    N = 2000
    vals = np.zeros(N)
    for i in range(N):
        Q_rand = np.random.randn(n_edges, 4)
        Q_rand /= np.linalg.norm(Q_rand, axis=1, keepdims=True)
        vals[i] = compute_total_Bsq_q(Q_rand, n_vec)
        if i % 500 == 0:
            print(f"  {i}/{N}: max_so_far = {vals[:i+1].max():.4f}")

    print(f"\nRandom sampling results (N={N}):")
    print(f"  Max:  {vals.max():.6f}")
    print(f"  Mean: {vals.mean():.6f}")
    print(f"  Std:  {vals.std():.6f}")
    print(f"  Min:  {vals.min():.6f}")
    print(f"  Fraction > 900: {(vals > 900).mean():.3f}")
    print(f"  Any > 1024: {vals.max() > 1024}")

    # ── Stage 2: Per-plaquette max ────────────────────────────────────────────
    print("\n--- Stage 2: Per-plaquette constrained max (gradient ascent) ---")

    def neg_single_plaq(q_flat, pi):
        """Negative |B_pi|^2 for single plaquette, varying its 4 links."""
        quats = Q_I.copy()
        plaq = plaquettes[pi]
        for k, ei in enumerate(plaq['ei']):
            q = q_flat[4*k:4*(k+1)]
            quats[ei] = q / np.linalg.norm(q)
        return -compute_B_plaq_q(quats, pi, n_vec)

    # Test active and inactive plaquettes
    for pi, label in [(0, "Active"), (next(i for i,p in enumerate(plaquettes) if not p['active']), "Inactive")]:
        best = 0.0
        for _ in range(100):
            q_init = np.random.randn(16)
            # normalize each quaternion
            for k in range(4):
                q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
            res = minimize(neg_single_plaq, q_init, args=(pi,),
                           method='L-BFGS-B',
                           options={'maxiter': 500, 'ftol': 1e-12})
            val = -res.fun
            if val > best:
                best = val
        p = plaquettes[pi]
        print(f"\n  {label} plaquette {pi}: x={p['x']}, (mu,nu)=({p['mu']},{p['nu']})")
        print(f"    Constrained max |B_□|^2 = {best:.6f}")
        print(f"    Unconstrained max (all |c_k|=1) = {(sum(abs(c) for c in p['eff']))**2:.1f}")
        print(f"    Reduction factor: {best / 16:.6f}")
        if best < 15.99:
            print(f"    *** HOLONOMY CONSTRAINT REDUCES MAX! ***")
        else:
            print(f"    => Holonomy constraint does NOT reduce max (both = 16)")

    # ── Stage 3: Vary single link from identity ───────────────────────────────
    print("\n--- Stage 3: Vary single link from identity ---")
    t_vals = np.linspace(0, 2 * np.pi, 200)
    axes = [
        np.array([1., 0., 0.]),
        np.array([0., 1., 0.]),
        np.array([0., 0., 1.]),
        np.array([1., 1., 1.]) / np.sqrt(3),
    ]

    # Test all edges, each with 5 random axes
    max_global = 1024.0
    worst_edge = -1
    print("  Scanning all 64 edges (5 axes each)...")
    for ei in range(n_edges):
        for _ in range(5):
            axis = np.random.randn(3)
            axis /= np.linalg.norm(axis)
            max_t = 0.0
            for t in t_vals:
                Q = Q_I.copy()
                Q[ei] = axis_angle_to_quat(axis, t)
                Q[ei] /= np.linalg.norm(Q[ei])
                val = compute_total_Bsq_q(Q, n_vec)
                if val > max_t:
                    max_t = val
            if max_t > max_global:
                max_global = max_t
                worst_edge = ei

    print(f"  Max over all edges/axes: {max_global:.6f}")
    print(f"  Exceeds 1024: {max_global > 1024 + 1e-6}")
    if worst_edge >= 0:
        print(f"  Worst edge: {worst_edge} = {edges[worst_edge]}")

    # Detailed t-scan for edge 0, axis (1,0,0)
    print("\n  Detailed scan: edge 0 varied in axis (1,0,0):")
    t_dense = np.linspace(0, 2*np.pi, 500)
    total_vals_t = []
    active_vals_t = []
    inactive_vals_t = []
    affected_pis = edge_plaq_map[0]
    active_affected = [pi for pi in affected_pis if plaquettes[pi]['active']]
    inactive_affected = [pi for pi in affected_pis if not plaquettes[pi]['active']]

    for t in t_dense:
        Q = Q_I.copy()
        Q[0] = axis_angle_to_quat(np.array([1., 0., 0.]), t)
        Q[0] /= np.linalg.norm(Q[0])
        total = compute_total_Bsq_q(Q, n_vec)
        active_sum = sum(compute_B_plaq_q(Q, pi, n_vec) for pi in affected_pis
                         if plaquettes[pi]['active'])
        inactive_sum = sum(compute_B_plaq_q(Q, pi, n_vec) for pi in affected_pis
                           if not plaquettes[pi]['active'])
        total_vals_t.append(total)
        active_vals_t.append(active_sum)
        inactive_vals_t.append(inactive_sum)

    total_vals_t = np.array(total_vals_t)
    active_vals_t = np.array(active_vals_t)
    inactive_vals_t = np.array(inactive_vals_t)
    bsq_I_per_plaq = {}
    for pi in range(n_plaq):
        B = compute_B_plaq_q(Q_I, pi, n_vec)
        bsq_I_per_plaq[pi] = B

    print(f"    Total sum max: {total_vals_t.max():.6f} (at Q=I: 1024)")
    print(f"    Total sum min: {total_vals_t.min():.6f}")
    print(f"    Affected active plaqs sum at max t: {active_vals_t[np.argmax(total_vals_t)]:.4f}")
    print(f"    Affected inactive plaqs sum at max t: {inactive_vals_t[np.argmax(total_vals_t)]:.4f}")
    print(f"    Active affected: {len(active_affected)}, Inactive affected: {len(inactive_affected)}")

    # Check per-edge monotonicity
    print("\n  Per-edge monotonicity check:")
    baseline_affected = sum(bsq_I_per_plaq[pi] for pi in affected_pis)
    affected_sum_t = np.array([
        sum(compute_B_plaq_q(Q_I[:ei] + [axis_angle_to_quat(np.array([1.,0.,0.]), t)] + Q_I[ei+1:], pi, n_vec)
            for pi in affected_pis)
        for t in t_dense[:20]  # just first 20 for speed
    ])

    # ── Stage 3b: Per-edge monotonicity for ALL edges ─────────────────────────
    print("\n--- Stage 3b: Per-edge monotonicity (systematic check) ---")
    n_mono_violations = 0
    max_per_edge_gain = 0.0

    for ei in range(n_edges):
        affected_pis_e = edge_plaq_map[ei]
        baseline_e = sum(bsq_I_per_plaq[pi] for pi in affected_pis_e)

        # Try 10 axes
        local_max_gain = 0.0
        for _ in range(10):
            axis = np.random.randn(3)
            axis /= np.linalg.norm(axis)
            for t in np.linspace(0, 2*np.pi, 50):
                Q = Q_I.copy()
                Q[ei] = axis_angle_to_quat(axis, t)
                Q[ei] /= np.linalg.norm(Q[ei])
                edge_sum = sum(compute_B_plaq_q(Q, pi, n_vec) for pi in affected_pis_e)
                gain = edge_sum - baseline_e
                if gain > local_max_gain:
                    local_max_gain = gain

        if local_max_gain > 1e-6:
            n_mono_violations += 1
        if local_max_gain > max_per_edge_gain:
            max_per_edge_gain = local_max_gain

    print(f"  Edges violating per-edge monotonicity: {n_mono_violations} / {n_edges}")
    print(f"  Maximum per-edge gain: {max_per_edge_gain:.6f}")
    if n_mono_violations == 0:
        print("  => Per-edge monotonicity HOLDS globally")
    else:
        print("  => Per-edge monotonicity FAILS (some edges increase local sum)")

    # ── Stage 4: Decoherence at single-plaquette maximum ─────────────────────
    print("\n--- Stage 4: Decoherence analysis ---")

    # Find config maximizing plaquette 0 (while fixing rest at identity)
    pi_target = 0
    p0 = plaquettes[pi_target]
    print(f"  Target: Plaquette 0 (x={p0['x']}, mu={p0['mu']}, nu={p0['nu']}, "
          f"{'Active' if p0['active'] else 'Inactive'})")

    def neg_single_plaq_global(q_flat, pi):
        quats = Q_I.copy()
        for k, ei in enumerate(plaquettes[pi]['ei']):
            q = q_flat[4*k:4*(k+1)]
            quats[ei] = q / np.linalg.norm(q)
        return -compute_B_plaq_q(quats, pi, n_vec)

    best_plaq0 = 0.0
    best_Q_p0 = Q_I.copy()
    for trial in range(200):
        q_init = np.random.randn(16)
        for k in range(4):
            q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
        res = minimize(neg_single_plaq_global, q_init, args=(pi_target,),
                       method='L-BFGS-B', options={'maxiter': 300, 'ftol': 1e-12})
        val = -res.fun
        if val > best_plaq0:
            best_plaq0 = val
            q_best = res.x

    # Reconstruct Q at max
    Q_at_max = Q_I.copy()
    for k, ei in enumerate(p0['ei']):
        q = q_best[4*k:4*(k+1)]
        Q_at_max[ei] = q / np.linalg.norm(q)

    # Compute all plaquette values
    all_bsq_at_max = np.array([compute_B_plaq_q(Q_at_max, pi, n_vec) for pi in range(n_plaq)])
    total_at_max = all_bsq_at_max.sum()

    # Neighbor analysis
    neighbors_p0 = set()
    for ei in p0['ei']:
        for pj in edge_plaq_map[ei]:
            if pj != pi_target:
                neighbors_p0.add(pj)
    neighbors_p0 = list(neighbors_p0)

    bsq_I_all = np.array([bsq_I_per_plaq[pi] for pi in range(n_plaq)])
    gains = all_bsq_at_max - bsq_I_all

    active_mask = np.array([p['active'] for p in plaquettes])
    neigh_mask = np.zeros(n_plaq, dtype=bool)
    for pj in neighbors_p0:
        neigh_mask[pj] = True

    print(f"\n  Max |B_0|^2 achieved: {best_plaq0:.6f} (baseline: {bsq_I_all[pi_target]:.1f})")
    print(f"  Total Sum |B_□|^2 at max config: {total_at_max:.6f}")
    print(f"  Total gain: {total_at_max - 1024:+.6f}")
    print(f"  Plaquette 0 gain: {gains[pi_target]:+.4f}")
    print(f"  Neighbors ({len(neighbors_p0)}) total gain: {gains[neigh_mask].sum():+.4f}")
    print(f"    Active neighbors: {neigh_mask & active_mask} -> gain {gains[neigh_mask & active_mask].sum():+.4f}")
    print(f"    Inactive neighbors gain: {gains[neigh_mask & ~active_mask].sum():+.4f}")
    print(f"  Non-neighbor gain: {gains[~neigh_mask & (np.arange(n_plaq) != pi_target)].sum():+.4f}")

    # Per-plaquette breakdown for neighbors
    print(f"\n  Neighbor plaquettes:")
    for pj in sorted(neighbors_p0):
        pp = plaquettes[pj]
        print(f"    Plaquette {pj} ({'A' if pp['active'] else 'I'}, "
              f"mu={pp['mu']},nu={pp['nu']}): "
              f"|B|^2={all_bsq_at_max[pj]:.4f}, "
              f"baseline={bsq_I_all[pj]:.1f}, "
              f"gain={gains[pj]:+.4f}")

    # ── Test: config that maximizes BOTH plaq 0 and plaq 1 ───────────────────
    print("\n--- Stage 4b: Can two active neighbors both be maximized? ---")
    # Find two active plaquettes sharing an edge
    active_plaqs = [i for i, p in enumerate(plaquettes) if p['active']]
    shared_pairs = []
    for i, pi in enumerate(active_plaqs):
        for pj in active_plaqs[i+1:]:
            shared = set(plaquettes[pi]['ei']) & set(plaquettes[pj]['ei'])
            if shared:
                shared_pairs.append((pi, pj, list(shared)))
                if len(shared_pairs) >= 3:
                    break
        if len(shared_pairs) >= 3:
            break

    if shared_pairs:
        pi1, pi2, shared_edges = shared_pairs[0]
        p1, p2 = plaquettes[pi1], plaquettes[pi2]
        print(f"  Pair ({pi1},{pi2}): share edges {shared_edges}")
        print(f"    Plaquette {pi1}: x={p1['x']}, mu={p1['mu']}, nu={p1['nu']}")
        print(f"    Plaquette {pi2}: x={p2['x']}, mu={p2['mu']}, nu={p2['nu']}")

        # Maximize sum of both
        all_ei = list(set(p1['ei'] + p2['ei']))
        ei_to_slot = {ei: k for k, ei in enumerate(all_ei)}

        def neg_pair_sum(q_flat):
            quats = Q_I.copy()
            for k, ei in enumerate(all_ei):
                q = q_flat[4*k:4*(k+1)]
                quats[ei] = q / np.linalg.norm(q)
            return -(compute_B_plaq_q(quats, pi1, n_vec) +
                     compute_B_plaq_q(quats, pi2, n_vec))

        best_pair = 0.0
        for _ in range(100):
            q_init = np.random.randn(4 * len(all_ei))
            for k in range(len(all_ei)):
                q_init[4*k:4*(k+1)] /= np.linalg.norm(q_init[4*k:4*(k+1)])
            res = minimize(neg_pair_sum, q_init, method='L-BFGS-B',
                           options={'maxiter': 500, 'ftol': 1e-12})
            if -res.fun > best_pair:
                best_pair = -res.fun
                best_q_pair = res.x

        Q_pair = Q_I.copy()
        for k, ei in enumerate(all_ei):
            q = best_q_pair[4*k:4*(k+1)]
            Q_pair[ei] = q / np.linalg.norm(q)

        pair_total = compute_total_Bsq_q(Q_pair, n_vec)
        b1 = compute_B_plaq_q(Q_pair, pi1, n_vec)
        b2 = compute_B_plaq_q(Q_pair, pi2, n_vec)
        print(f"\n  Maximizing |B_{pi1}|^2 + |B_{pi2}|^2:")
        print(f"    Max sum = {best_pair:.6f} (if both at 16: 32)")
        print(f"    |B_{pi1}|^2 = {b1:.6f}")
        print(f"    |B_{pi2}|^2 = {b2:.6f}")
        print(f"    Total Sum |B_□|^2 = {pair_total:.6f}")
        print(f"    Max pair at 32 means both at their individual max: {best_pair >= 31.99:.1f}")
    else:
        print("  No sharing pairs found (unexpected)")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("SUMMARY OF KEY RESULTS")
    print("=" * 65)
    print(f"1. Q=I value: {Bsq_I:.2f} = 1024 ✓")
    print(f"2. Random sampling (N={N}): max = {vals.max():.4f}, "
          f"{'≤ 1024 ✓' if vals.max() <= 1024.01 else '> 1024 ✗'}")
    print(f"3. Per-plaquette constrained max: {best_plaq0:.4f} out of 16 possible")
    print(f"4. Single-link variation max: {max_global:.4f}, "
          f"{'≤ 1024 ✓' if max_global <= 1024.01 else '> 1024 ✗'}")
    print(f"5. Per-edge monotonicity: "
          f"{'HOLDS ✓' if n_mono_violations == 0 else f'FAILS ({n_mono_violations} edges) ✗'}")
    print(f"6. Decoherence: gain at plaq 0 = {gains[pi_target]:+.2f}, "
          f"neighbor gain = {gains[neigh_mask].sum():+.2f}")
