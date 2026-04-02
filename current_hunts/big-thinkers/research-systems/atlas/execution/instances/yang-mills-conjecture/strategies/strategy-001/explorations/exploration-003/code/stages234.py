"""
Stages 2-4: Per-plaquette max, holonomy constraint, cross-plaquette coupling, decoherence.

Lattice: (Z/2Z)^4, d=4. 16 vertices, 64 edges, 96 plaquettes.

B_□(Q, v) = v_{e1} + Ad(Q_{e1})(v_{e2}) - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(v_{e3}) - Ad(U_□)(v_{e4})
U_□ = Q_{e1}Q_{e2}Q_{e3}^{-1}Q_{e4}^{-1}

Staggered mode: v_{x,mu} = (-1)^{|x|+mu} * n, n = (1,0,0)

Conjecture: Sum_□ |B_□|^2 <= 1024 |n|^2 for all Q in SU(2)^64.
"""

import numpy as np
from scipy.optimize import minimize
from itertools import product
import sys

# ─── SU(2) / SO(3) utilities ─────────────────────────────────────────────────

def su2_from_axis_angle(v, theta):
    """SU(2) element exp(i*theta/2 * v.sigma) for unit vector v"""
    # = cos(theta/2) I + i*sin(theta/2) * v.sigma
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c + 1j * s * v[2], s * (1j * v[0] + v[1])],
                     [s * (1j * v[0] - v[1]), c - 1j * s * v[2]]])

def random_su2():
    """Haar-random SU(2) element"""
    # Uniform on 3-sphere = random unit quaternion
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    a, b, c, d = q
    return np.array([[a + 1j * d, 1j * b + c],
                     [1j * b - c, a - 1j * d]])

def su2_adjoint(Q, v):
    """Apply Ad(Q) to 3-vector v: returns SO(3)*v"""
    # V = i/2 * (v[0]*s1 + v[1]*s2 + v[2]*s3) in su(2)
    # W = Q V Q†
    # w_k = Re(Tr(-i s_k W))
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]])
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    sigmas = [s1, s2, s3]
    V = (1j / 2) * (v[0] * s1 + v[1] * s2 + v[2] * s3)
    W = Q @ V @ Q.conj().T
    return np.array([(-1j * np.trace(s @ W)).real for s in sigmas])

def su2_inv(Q):
    """SU(2) inverse = conjugate transpose"""
    return Q.conj().T

def quat_to_su2(q):
    """Quaternion (a,b,c,d) → SU(2) matrix (normalized)"""
    q = q / np.linalg.norm(q)
    a, b, c, d = q
    return np.array([[a + 1j * d, 1j * b + c],
                     [1j * b - c, a - 1j * d]])

# Verify adjoint: should give identity at Q=I
def test_adjoint():
    I2 = np.eye(2, dtype=complex)
    for v in [np.array([1.,0,0]), np.array([0,1.,0]), np.array([0,0,1.])]:
        res = su2_adjoint(I2, v)
        assert np.allclose(res, v), f"Adjoint test failed: {res} vs {v}"
    # Rotation by pi around z: should flip x and y
    Q_pi_z = su2_from_axis_angle(np.array([0,0,1.]), np.pi)
    v = np.array([1., 0, 0])
    res = su2_adjoint(Q_pi_z, v)
    assert np.allclose(res, [-1, 0, 0], atol=1e-10), f"Rotation test: {res}"
    print("Adjoint tests PASSED")

# ─── Lattice setup ────────────────────────────────────────────────────────────

L = 2
d = 4
n_vecs = np.array([[1., 0, 0]])  # canonical n

def staggered_sign(x, mu):
    return (-1) ** (sum(x) + mu)

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

vertices = list(product(range(L), repeat=d))
edges = [(x, mu) for x in vertices for mu in range(d)]
edge_to_idx = {e: i for i, e in enumerate(edges)}
n_edges = len(edges)  # 64

plaquettes = []
for x in vertices:
    for mu in range(d):
        for nu in range(mu + 1, d):
            x_mu = add_mod(x, mu)
            x_nu = add_mod(x, nu)
            e1, e2, e3, e4 = (x, mu), (x_mu, nu), (x_nu, mu), (x, nu)
            s1 = staggered_sign(x, mu)
            s2 = staggered_sign(x_mu, nu)
            s3 = staggered_sign(x_nu, mu)
            s4 = staggered_sign(x, nu)
            plaquettes.append({
                'edges': (e1, e2, e3, e4),
                'signs': (s1, s2, s3, s4),       # raw staggered signs
                'eff': (s1, s2, -s3, -s4),        # effective coefficients
                'x': x, 'mu': mu, 'nu': nu,
                'active': (mu + nu) % 2 == 1
            })

n_plaq = len(plaquettes)  # 96
assert n_plaq == 96

# Build edge-sharing map: for each edge, which plaquette indices contain it
edge_plaq_map = {e: [] for e in edges}
for pi, plaq in enumerate(plaquettes):
    for e in plaq['edges']:
        edge_plaq_map[e].append(pi)

# ─── B_□ computation ─────────────────────────────────────────────────────────

def compute_B_plaq(Q_arr, pi, n_vec=None):
    """Compute B_□ vector for plaquette pi given Q_arr (n_edges SU(2) matrices)."""
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    plaq = plaquettes[pi]
    e1, e2, e3, e4 = plaq['edges']
    c1, c2, c3, c4 = plaq['eff']

    i1 = edge_to_idx[e1]
    i2 = edge_to_idx[e2]
    i3 = edge_to_idx[e3]
    i4 = edge_to_idx[e4]

    Q1 = Q_arr[i1]
    Q2 = Q_arr[i2]
    Q3 = Q_arr[i3]
    Q4 = Q_arr[i4]

    # Partial holonomies
    P1 = Q1
    P2 = Q1 @ Q2 @ su2_inv(Q3)
    P3 = P2 @ su2_inv(Q4)  # = U_□

    B = (c1 * n_vec
         + c2 * su2_adjoint(P1, n_vec)
         + c3 * su2_adjoint(P2, n_vec)
         + c4 * su2_adjoint(P3, n_vec))
    return B

def compute_total_Bsq(Q_arr, n_vec=None):
    """Sum_□ |B_□|^2 over all plaquettes."""
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    total = 0.0
    for pi in range(n_plaq):
        B = compute_B_plaq(Q_arr, pi, n_vec)
        total += np.dot(B, B)
    return total

def make_identity_config():
    """All links = identity SU(2)"""
    return [np.eye(2, dtype=complex) for _ in edges]

# ─── Stage 2: Per-plaquette max with gradient ascent ────────────────────────

def single_plaq_Bsq_constrained(q_flat, plaq_idx, n_vec=None):
    """
    |B_□|^2 for a SINGLE plaquette parametrized by 4 quaternions q = [q1,q2,q3,q4]
    (each a unit quaternion in R^4, total 16 parameters).
    Returns NEGATIVE (for minimization).
    """
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    q_flat = np.array(q_flat)
    Q = [quat_to_su2(q_flat[4*i:4*i+4]) for i in range(4)]
    Q1, Q2, Q3, Q4 = Q
    P1 = Q1
    P2 = Q1 @ Q2 @ su2_inv(Q3)
    P3 = P2 @ su2_inv(Q4)
    plaq = plaquettes[plaq_idx]
    c1, c2, c3, c4 = plaq['eff']
    B = (c1 * n_vec
         + c2 * su2_adjoint(P1, n_vec)
         + c3 * su2_adjoint(P2, n_vec)
         + c4 * su2_adjoint(P3, n_vec))
    return -np.dot(B, B)  # negative for minimization

def maximize_single_plaq(plaq_idx, n_trials=200, n_vec=None):
    """Find max |B_□|^2 for a single plaquette via gradient ascent."""
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    best = 0.0
    best_q = None
    for _ in range(n_trials):
        # Random initial quaternions
        q0 = np.concatenate([np.random.randn(4) / np.linalg.norm(np.random.randn(4))
                              for _ in range(4)])
        # Re-normalize each quaternion
        q0_norm = q0.copy()
        for i in range(4):
            q0_norm[4*i:4*i+4] /= np.linalg.norm(q0_norm[4*i:4*i+4])

        res = minimize(single_plaq_Bsq_constrained, q0_norm,
                       args=(plaq_idx, n_vec),
                       method='L-BFGS-B',
                       options={'maxiter': 500, 'ftol': 1e-15, 'gtol': 1e-10})
        val = -res.fun
        if val > best:
            best = val
            best_q = res.x
    return best, best_q

def unconstrained_single_plaq_max(eff):
    """
    For 4 rotations R_k in SO(3) with effective coefficients c_k,
    max |sum c_k R_k n|^2 over all R_k in SO(3) independently.
    = (sum |c_k|)^2 = (1+1+1+1)^2 = 16.
    """
    return sum(abs(c) for c in eff) ** 2

# ─── Stage 3: Vary a single link ─────────────────────────────────────────────

def vary_single_link(edge_idx, X_hat, t_values, Q_base=None, n_vec=None):
    """
    Vary Q_{edge} = exp(i*t*X_hat) for t in t_values.
    Q_base: base configuration (default: identity for all links).
    Returns array of total Sum_□ |B_□|^2 for each t.
    """
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    if Q_base is None:
        Q_base = make_identity_config()

    results = []
    for t in t_values:
        Q = list(Q_base)  # copy
        # Q_{edge} = exp(i*t/2 * X_hat.sigma)
        Q[edge_idx] = su2_from_axis_angle(X_hat, t)
        total = compute_total_Bsq(Q, n_vec)
        results.append(total)
    return np.array(results)

def vary_single_link_plaq_contributions(edge_idx, X_hat, t_values, Q_base=None, n_vec=None):
    """
    Like vary_single_link, but returns contributions of each plaquette separately.
    Returns shape (len(t_values), n_plaq) array.
    """
    if n_vec is None:
        n_vec = np.array([1., 0, 0])
    if Q_base is None:
        Q_base = make_identity_config()

    results = np.zeros((len(t_values), n_plaq))
    for ti, t in enumerate(t_values):
        Q = list(Q_base)
        Q[edge_idx] = su2_from_axis_angle(X_hat, t)
        for pi in range(n_plaq):
            B = compute_B_plaq(Q, pi, n_vec)
            results[ti, pi] = np.dot(B, B)
    return results

# ─── Stage 4: Decoherence analysis ────────────────────────────────────────────

def neighbor_plaquettes(pi):
    """Find all plaquettes that share at least one edge with plaquette pi."""
    plaq = plaquettes[pi]
    neighbors = set()
    for e in plaq['edges']:
        for pj in edge_plaq_map[e]:
            if pj != pi:
                neighbors.add(pj)
    return list(neighbors)

# ──────────────────────────────────────────────────────────────────────────────
# MAIN COMPUTATIONS
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    np.random.seed(42)

    print("=" * 70)
    print("LATTICE YANG-MILLS: SU(2) REPRESENTATION THEORY BOUND")
    print("=" * 70)

    # Run adjoint tests
    test_adjoint()

    # ── Test at Q=I ──────────────────────────────────────────────────────────
    print("\n--- Verification at Q=I ---")
    Q_I = make_identity_config()
    Bsq_I = compute_total_Bsq(Q_I)
    print(f"Sum |B_□|^2 at Q=I = {Bsq_I:.6f}")
    print(f"Expected: 1024. Matches: {abs(Bsq_I - 1024) < 1e-9}")

    # ── Random config sampling ────────────────────────────────────────────────
    print("\n--- Stage 1: Random config sampling (N=1000) ---")
    N_random = 1000
    total_vals = np.zeros(N_random)
    for trial in range(N_random):
        Q_rand = [random_su2() for _ in edges]
        total_vals[trial] = compute_total_Bsq(Q_rand)

    print(f"Sum |B_□|^2 over {N_random} random configs:")
    print(f"  Max: {total_vals.max():.6f}")
    print(f"  Mean: {total_vals.mean():.6f}")
    print(f"  Std: {total_vals.std():.6f}")
    print(f"  Min: {total_vals.min():.6f}")
    print(f"  At Q=I (1024): {'YES' if abs(Bsq_I - 1024) < 1e-9 else 'NO'}")
    print(f"  Max > 1024? {total_vals.max() > 1024}")
    print(f"  Fraction > 900: {(total_vals > 900).mean():.3f}")

    # ── Stage 2: Per-plaquette max ────────────────────────────────────────────
    print("\n--- Stage 2: Per-plaquette max (holonomy-constrained) ---")

    # Test one active plaquette and one inactive
    active_idx = next(i for i, p in enumerate(plaquettes) if p['active'])
    inactive_idx = next(i for i, p in enumerate(plaquettes) if not p['active'])

    print(f"\nActive plaquette {active_idx}: x={plaquettes[active_idx]['x']}, "
          f"mu={plaquettes[active_idx]['mu']}, nu={plaquettes[active_idx]['nu']}")
    print(f"  eff_coeffs = {plaquettes[active_idx]['eff']}")
    print("  Maximizing |B_□|^2 over Q_{e1,e2,e3,e4} ∈ SU(2)...")
    max_active, _ = maximize_single_plaq(active_idx, n_trials=300)
    print(f"  Constrained max |B_□|^2 = {max_active:.6f}")
    unc_max = unconstrained_single_plaq_max(plaquettes[active_idx]['eff'])
    print(f"  Unconstrained max (independent SO(3)) = {unc_max:.6f}")
    print(f"  Reduction factor: {max_active / unc_max:.6f}")

    print(f"\nInactive plaquette {inactive_idx}: x={plaquettes[inactive_idx]['x']}, "
          f"mu={plaquettes[inactive_idx]['mu']}, nu={plaquettes[inactive_idx]['nu']}")
    print(f"  eff_coeffs = {plaquettes[inactive_idx]['eff']}")
    print("  Maximizing |B_□|^2 over Q_{e1,e2,e3,e4} ∈ SU(2)...")
    max_inactive, _ = maximize_single_plaq(inactive_idx, n_trials=300)
    print(f"  Constrained max |B_□|^2 = {max_inactive:.6f}")
    unc_max_i = unconstrained_single_plaq_max(plaquettes[inactive_idx]['eff'])
    print(f"  Unconstrained max (independent SO(3)) = {unc_max_i:.6f}")
    print(f"  Reduction factor: {max_inactive / unc_max_i:.6f}")

    # ── Stage 3: Vary single link from identity ───────────────────────────────
    print("\n--- Stage 3: Vary single link (edge 0) from identity ---")
    t_vals = np.linspace(0, 2 * np.pi, 200)
    edge_0 = 0  # First edge (x=(0,0,0,0), mu=0)
    affected = edge_plaq_map[edges[edge_0]]
    print(f"Edge 0: {edges[edge_0]}, appears in {len(affected)} plaquettes")

    # Try 3 random rotation directions
    directions = [
        np.array([1., 0, 0]),
        np.array([0., 1., 0]),
        np.array([0., 0., 1.]),
        np.array([1., 1., 0.]) / np.sqrt(2)
    ]
    print(f"\nVarying edge 0 in 4 rotation directions:")
    max_over_dirs = 1024.0
    for di, X_hat in enumerate(directions):
        vals = vary_single_link(edge_0, X_hat, t_vals)
        print(f"  Dir {di} = {X_hat}: max={vals.max():.6f}, "
              f"at t={t_vals[np.argmax(vals)]:.4f}, "
              f"min={vals.min():.6f}")
        if vals.max() > max_over_dirs:
            max_over_dirs = vals.max()

    # Try varying EVERY edge in random directions
    print("\nVarying each edge in 5 random directions:")
    global_max = 1024.0
    worst_edge = -1
    worst_dir = None
    for ei, e in enumerate(edges):
        edge_max = 0.0
        for _ in range(5):
            X_hat = np.random.randn(3)
            X_hat /= np.linalg.norm(X_hat)
            vals = vary_single_link(ei, X_hat, t_vals)
            if vals.max() > edge_max:
                edge_max = vals.max()
                worst_dir = X_hat.copy()
        if edge_max > global_max:
            global_max = edge_max
            worst_edge = ei
        if ei % 16 == 0:
            print(f"  Edge {ei}/{n_edges}: max so far = {edge_max:.6f}")

    print(f"\nGlobal max over all edges, directions: {global_max:.6f}")
    print(f"Exceeded 1024? {global_max > 1024}")
    if worst_edge >= 0:
        print(f"Worst edge: {worst_edge} = {edges[worst_edge]}")

    # ── Stage 3b: Detailed plaquette-by-plaquette for one link variation ──────
    print("\n--- Stage 3b: Plaquette-by-plaquette analysis for varying edge 0 ---")
    X_hat = np.array([1., 0, 0])
    t_fine = np.linspace(0, 2 * np.pi, 500)
    plaq_vals = vary_single_link_plaq_contributions(edge_0, X_hat, t_fine)

    # For each time step, find which plaquettes gain / lose
    bsq_at_I = np.array([np.dot(compute_B_plaq(Q_I, pi), compute_B_plaq(Q_I, pi))
                           for pi in range(n_plaq)])

    gains = plaq_vals - bsq_at_I[np.newaxis, :]  # shape (n_t, n_plaq)
    total_gains = gains.sum(axis=1)  # shape (n_t,)
    active_mask = np.array([p['active'] for p in plaquettes])
    inactive_mask = ~active_mask

    print(f"  Total gain (from Q=I baseline) max: {total_gains.max():.6f}")
    print(f"  Total gain min: {total_gains.min():.6f}")
    print(f"  Total gain at t=0: {total_gains[0]:.6f}")
    print(f"  Active plaquettes: {active_mask.sum()}")
    print(f"  Inactive plaquettes: {inactive_mask.sum()}")
    print(f"  Affected plaquettes: {len(affected)}")

    # At the peak t
    t_peak_idx = np.argmax(gains.sum(axis=1))
    t_peak = t_fine[t_peak_idx]
    print(f"\n  At peak t = {t_peak:.4f}:")
    print(f"    Total sum |B_□|^2 = {plaq_vals[t_peak_idx].sum():.6f}")
    print(f"    Active plaquettes sum: {plaq_vals[t_peak_idx][active_mask].sum():.6f}")
    print(f"    Inactive plaquettes sum: {plaq_vals[t_peak_idx][inactive_mask].sum():.6f}")
    print(f"    Gain from active: {gains[t_peak_idx][active_mask].sum():.6f}")
    print(f"    Gain from inactive: {gains[t_peak_idx][inactive_mask].sum():.6f}")

    # Show gain by type for affected plaquettes
    print(f"\n  Affected plaquettes and their gains at t_peak:")
    for pi in sorted(affected):
        p = plaquettes[pi]
        g = gains[t_peak_idx][pi]
        t = "Active" if p['active'] else "Inactive"
        print(f"    Plaquette {pi} ({t}, {p['mu']},{p['nu']}): gain = {g:+.4f}")

    # ── Stage 4: Decoherence — when one plaquette gains, do neighbors lose? ──
    print("\n--- Stage 4: Decoherence analysis ---")

    # Find the worst-case single-plaquette configuration
    print("Finding max |B_□|^2 for plaquette 0 (active) with random global config...")

    # Fix plaquette 0 near its maximum, then look at neighbor contributions
    # First, find a config that maximizes plaquette 0
    best_total = 0.0
    best_single = 0.0
    best_Q = None

    n_search = 500
    for trial in range(n_search):
        Q_rand = [random_su2() for _ in edges]
        B0 = compute_B_plaq(Q_rand, 0)
        val0 = np.dot(B0, B0)
        if val0 > best_single:
            best_single = val0
            best_Q = list(Q_rand)
            best_total = compute_total_Bsq(Q_rand)

    print(f"Best |B_□|^2 for plaquette 0 (over {n_search} random configs): {best_single:.6f}")
    print(f"  Total sum |B_□|^2 at that config: {best_total:.6f}")

    if best_Q is not None:
        # Plaquette 0 analysis
        neigh = neighbor_plaquettes(0)
        plaq0_active = plaquettes[0]['active']
        print(f"  Plaquette 0 type: {'Active' if plaq0_active else 'Inactive'}")
        print(f"  Number of neighbors: {len(neigh)}")

        # Contributions
        B0 = compute_B_plaq(best_Q, 0)
        neigh_total = sum(np.dot(compute_B_plaq(best_Q, pj), compute_B_plaq(best_Q, pj))
                         for pj in neigh)
        print(f"  |B_0|^2 = {np.dot(B0, B0):.6f}")
        print(f"  Sum |B_neighbor|^2 = {neigh_total:.6f}")
        print(f"  Baseline at Q=I: plaquette 0 = {bsq_at_I[0]:.4f}, "
              f"neighbors = {sum(bsq_at_I[j] for j in neigh):.4f}")
        print(f"  Gain at plaquette 0: {np.dot(B0,B0) - bsq_at_I[0]:+.4f}")
        print(f"  Gain at neighbors: {neigh_total - sum(bsq_at_I[j] for j in neigh):+.4f}")

    # Per-edge analysis: is Sum_e S_e(Q) <= S_e(I)?
    print("\n--- Stage 4b: Per-edge monotonicity test ---")
    print("For each edge, testing if varying from identity ONLY decreases the sum")
    print("(across all plaquettes containing that edge)...")

    violations = 0
    max_gain = 0.0
    worst_edge_idx = -1

    for ei, e in enumerate(edges):
        edge_plaqs = edge_plaq_map[e]
        baseline_e = sum(bsq_at_I[pi] for pi in edge_plaqs)

        # Try 20 random directions × t in [0, 2pi]
        local_max = baseline_e
        for _ in range(20):
            X_hat = np.random.randn(3)
            X_hat /= np.linalg.norm(X_hat)
            t_test = np.linspace(0, 2 * np.pi, 100)
            for t in t_test:
                Q = list(Q_I)
                Q[ei] = su2_from_axis_angle(X_hat, t)
                edge_sum = sum(np.dot(compute_B_plaq(Q, pi), compute_B_plaq(Q, pi))
                               for pi in edge_plaqs)
                if edge_sum > local_max:
                    local_max = edge_sum

        gain_e = local_max - baseline_e
        if gain_e > max_gain:
            max_gain = gain_e
            worst_edge_idx = ei
        if local_max > baseline_e + 1e-6:
            violations += 1

    print(f"  Edges tested: {n_edges}")
    print(f"  Violations of per-edge monotonicity: {violations}")
    print(f"  Maximum per-edge gain over baseline: {max_gain:.6f}")
    print(f"  Worst edge: {worst_edge_idx} = {edges[worst_edge_idx] if worst_edge_idx >= 0 else 'N/A'}")

    if violations > 0:
        print("  => Per-edge monotonicity FAILS (individual edge sums can increase)")
    else:
        print("  => Per-edge monotonicity HOLDS (no individual edge sum increased)")

    # ── Stage 4c: Compensation at maximal single plaquette ────────────────────
    print("\n--- Stage 4c: Compensation structure at single-plaquette maximum ---")

    # Gradient ascent to maximize one plaquette
    print("Maximizing plaquette 0 subject to rest of links at identity...")

    def plaq0_max_neg(q_flat):
        Q = list(Q_I)
        q_flat = np.array(q_flat)
        for i, e in enumerate(plaquettes[0]['edges']):
            qi = q_flat[4*i:4*i+4]
            Q[edge_to_idx[e]] = quat_to_su2(qi)
        B = compute_B_plaq(Q, 0)
        return -np.dot(B, B)

    q0 = np.array([1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0], dtype=float)
    best_val_plaq0 = 0.0
    best_Q_plaq0 = None

    for _ in range(100):
        q_init = np.concatenate([np.random.randn(4) for _ in range(4)])
        for i in range(4):
            q_init[4*i:4*i+4] /= np.linalg.norm(q_init[4*i:4*i+4])
        res = minimize(plaq0_max_neg, q_init, method='L-BFGS-B',
                       options={'maxiter': 1000, 'ftol': 1e-15})
        val = -res.fun
        if val > best_val_plaq0:
            best_val_plaq0 = val
            best_q = res.x

    # Reconstruct Q at maximum
    Q_max_plaq0 = list(Q_I)
    for i, e in enumerate(plaquettes[0]['edges']):
        Q_max_plaq0[edge_to_idx[e]] = quat_to_su2(best_q[4*i:4*i+4])

    B0_max = compute_B_plaq(Q_max_plaq0, 0)
    plaq0_val_max = np.dot(B0_max, B0_max)
    total_at_max = compute_total_Bsq(Q_max_plaq0)
    neigh0 = neighbor_plaquettes(0)
    neigh_vals = [np.dot(compute_B_plaq(Q_max_plaq0, pj), compute_B_plaq(Q_max_plaq0, pj))
                  for pj in neigh0]
    neigh_sum_max = sum(neigh_vals)
    other_sum_max = total_at_max - plaq0_val_max - neigh_sum_max

    print(f"  Max |B_0|^2 (plaquette 0 only) = {plaq0_val_max:.6f}")
    print(f"  Total Sum |B_□|^2 at that config = {total_at_max:.6f}")
    print(f"  Sum |B_neighbor|^2 = {neigh_sum_max:.6f}")
    print(f"  Sum |B_other|^2 = {other_sum_max:.6f}")
    print(f"  Gain at plaquette 0 = {plaq0_val_max - bsq_at_I[0]:+.4f}")
    print(f"  Gain at neighbors = {neigh_sum_max - sum(bsq_at_I[j] for j in neigh0):+.4f}")
    print(f"  Net total change = {total_at_max - 1024:+.4f}")
    print(f"  Conjecture holds at this config: {total_at_max <= 1024 + 1e-6}")

    print("\n  Active vs inactive breakdown at max:")
    neigh_active = [j for j in neigh0 if plaquettes[j]['active']]
    neigh_inactive = [j for j in neigh0 if not plaquettes[j]['active']]
    active_neigh_sum = sum(np.dot(compute_B_plaq(Q_max_plaq0, j), compute_B_plaq(Q_max_plaq0, j))
                           for j in neigh_active)
    inactive_neigh_sum = sum(np.dot(compute_B_plaq(Q_max_plaq0, j), compute_B_plaq(Q_max_plaq0, j))
                             for j in neigh_inactive)
    active_neigh_baseline = sum(bsq_at_I[j] for j in neigh_active)
    inactive_neigh_baseline = sum(bsq_at_I[j] for j in neigh_inactive)

    print(f"    Active neighbors ({len(neigh_active)}): "
          f"sum = {active_neigh_sum:.4f}, baseline = {active_neigh_baseline:.4f}, "
          f"gain = {active_neigh_sum - active_neigh_baseline:+.4f}")
    print(f"    Inactive neighbors ({len(neigh_inactive)}): "
          f"sum = {inactive_neigh_sum:.4f}, baseline = {inactive_neigh_baseline:.4f}, "
          f"gain = {inactive_neigh_sum - inactive_neigh_baseline:+.4f}")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Q=I value: {Bsq_I:.4f}")
    print(f"Max over {N_random} random configs: {total_vals.max():.4f}")
    print(f"Mean over random configs: {total_vals.mean():.4f}")
    print(f"Single-link variation max: {global_max:.4f}")
    print(f"Conjecture holds in random sampling: {total_vals.max() <= 1024 + 1e-6}")
