"""
Task 1: Independent re-implementation of the lattice and B_square formula.

Build d=4 hypercubic torus for L=2, compute M(Q) from scratch, verify lambda_max <= 16.
Also compute per-vertex F_x and verify F_x <= 64|n|^2.

Written from scratch — no code copied from E006.
"""

import numpy as np
from itertools import product

np.random.seed(12345)  # Different seed from E006

# ============================================================
# Part A: Build the d=4 hypercubic torus for L=2
# ============================================================

d = 4
L = 2
N_vertices = L**d  # 16

def vertex_index(coords):
    """Convert (x0,x1,x2,x3) to a flat index."""
    idx = 0
    for i in range(d):
        idx = idx * L + (coords[i] % L)
    return idx

def index_to_coords(idx):
    """Convert flat index back to coordinates."""
    coords = []
    for i in range(d):
        coords.append(idx % L)
        idx //= L
    return tuple(reversed(coords))

# All vertices
vertices = [index_to_coords(i) for i in range(N_vertices)]

# Build edges: (vertex_index, direction mu) -> edge_index
# Edge from vertex x in direction mu goes to x + e_mu
edges = {}
edge_list = []
for x_idx in range(N_vertices):
    x = vertices[x_idx]
    for mu in range(d):
        e_key = (x_idx, mu)
        edges[e_key] = len(edge_list)
        # target: x + e_mu (mod L)
        y = list(x)
        y[mu] = (y[mu] + 1) % L
        edge_list.append((x_idx, vertex_index(tuple(y)), mu))

N_edges = len(edge_list)
print(f"Vertices: {N_vertices}, Edges: {N_edges}")
assert N_edges == N_vertices * d  # 64

# Build plaquettes: for each vertex x, for each pair (mu, nu) with mu < nu,
# the plaquette is the cycle x -> x+mu -> x+mu+nu -> x+nu -> x
# Edges: e1 = (x, mu), e2 = (x+mu, nu), e3 = (x+nu, mu), e4 = (x, nu)
# Orientations: e1 forward, e2 forward, e3 backward, e4 backward

plaquettes = []
for x_idx in range(N_vertices):
    x = vertices[x_idx]
    for mu in range(d):
        for nu in range(mu+1, d):
            x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
            x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L

            e1 = edges[(x_idx, mu)]  # x -> x+mu
            e2 = edges[(vertex_index(tuple(x_mu)), nu)]  # x+mu -> x+mu+nu
            e3 = edges[(vertex_index(tuple(x_nu)), mu)]  # x+nu -> x+nu+mu (backward)
            e4 = edges[(x_idx, nu)]  # x -> x+nu (backward)

            plaquettes.append({
                'base': x_idx,
                'mu': mu, 'nu': nu,
                'e1': e1, 'e2': e2, 'e3': e3, 'e4': e4,
                'e1_fwd': True, 'e2_fwd': True, 'e3_fwd': False, 'e4_fwd': False
            })

N_plaquettes = len(plaquettes)
print(f"Plaquettes: {N_plaquettes}")
assert N_plaquettes == N_vertices * d*(d-1)//2  # 16 * 6 = 96

# ============================================================
# Part B: Check unique base vertex assignment
# ============================================================

base_counts = {}
for p in plaquettes:
    key = (p['e1'], p['e2'], p['e3'], p['e4'])
    if key in base_counts:
        print(f"  WARNING: Duplicate plaquette edges! {key}")
    base_counts[key] = p['base']

print(f"Unique plaquettes by edge set: {len(base_counts)} (should be {N_plaquettes})")

# ============================================================
# Part C: Random SO(3) generation and B_square formula
# ============================================================

def random_so3():
    """Generate random SO(3) via quaternion."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def Ad(Q, v):
    """Adjoint action: Ad_Q(v) = Q v for Q in SO(3), v in R^3 (= so(3))."""
    return Q @ v

def compute_holonomy(Q_edges, p):
    """Compute holonomy U_sq = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}."""
    U = Q_edges[p['e1']] @ Q_edges[p['e2']] @ Q_edges[p['e3']].T @ Q_edges[p['e4']].T
    return U

def staggered_sign(x_coords, mu):
    """
    Staggered mode sign: v_e = (-1)^{|x|+mu} * n where e = (x, mu).
    |x| = sum of coordinates of x.
    """
    return (-1) ** (sum(x_coords) + mu)

def compute_B_sq(Q_edges, p, n):
    """
    Compute B_sq(Q, v) for a plaquette p and staggered mode v with amplitude n.

    B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

    where v_e = sign(e) * n for the staggered mode.
    """
    Q1 = Q_edges[p['e1']]
    Q2 = Q_edges[p['e2']]
    Q3 = Q_edges[p['e3']]
    Q4 = Q_edges[p['e4']]
    U_sq = Q1 @ Q2 @ Q3.T @ Q4.T

    # Get the base vertex coords
    x = vertices[p['base']]

    # Staggered signs for each edge endpoint
    # e1 = (x, mu): sign = (-1)^(|x| + mu)
    s1 = staggered_sign(x, p['mu'])

    # e2 = (x+mu_hat, nu): sign = (-1)^(|x+mu_hat| + nu) = (-1)^(|x|+1+nu)
    x_mu = list(x); x_mu[p['mu']] = (x_mu[p['mu']] + 1) % L
    s2 = staggered_sign(tuple(x_mu), p['nu'])

    # e3 = (x+nu_hat, mu): sign = (-1)^(|x+nu_hat| + mu) = (-1)^(|x|+1+mu)
    x_nu = list(x); x_nu[p['nu']] = (x_nu[p['nu']] + 1) % L
    s3 = staggered_sign(tuple(x_nu), p['mu'])

    # e4 = (x, nu): sign = (-1)^(|x| + nu)
    s4 = staggered_sign(x, p['nu'])

    # B_sq formula
    v1 = s1 * n
    v2 = s2 * n
    v3 = s3 * n
    v4 = s4 * n

    B = v1 + Ad(Q1, v2) - Ad(Q1 @ Q2 @ Q3.T, v3) - Ad(U_sq, v4)

    return B

# ============================================================
# Part D: Compute global M(Q) and per-vertex F_x
# ============================================================

def compute_global_M(Q_edges):
    """Compute the full M(Q) matrix: sum over all plaquettes of B_sq B_sq^T."""
    # M(Q) is the matrix such that v^T M(Q) v = sum_p |B_sq(Q,v)|^2
    # For staggered mode v = (..., (-1)^{|x|+mu} n, ...), we have
    # v^T M(Q) v = sum_p |B_sq(Q,v)|^2 which is a quadratic form in n.
    #
    # Actually, M(Q) is L^d * d by L^d * d (big matrix).
    # But we only need its action on the staggered modes.
    # The staggered modes are spanned by v(n) = ((-1)^{|x|+mu} n_i)_{(x,mu),i}
    # which form a 3-dimensional subspace (parameterized by n in R^3).
    #
    # The restriction of M(Q) to this subspace is the 3x3 matrix M_stag(Q)
    # where n^T M_stag(Q) n = sum_p |B_sq(Q, v(n))|^2

    # Compute M_stag by computing B_sq for basis vectors n = e_i
    M_stag = np.zeros((3, 3))
    for i in range(3):
        n_i = np.zeros(3)
        n_i[i] = 1.0
        for j in range(3):
            n_j = np.zeros(3)
            n_j[j] = 1.0
            # M_stag[i,j] = sum_p B_sq(Q, v(e_i)) . B_sq(Q, v(e_j))
            # Use polarization: M[i,j] = 0.5 * ((e_i+e_j)^T M (e_i+e_j) - e_i^T M e_i - e_j^T M e_j)
            # But simpler: compute B_sq for each plaquette and accumulate
            pass

    # More efficiently: compute B for each plaquette as a function of n,
    # B(n) = M_p @ n for some 3x3 matrix M_p, then M_stag = sum_p M_p^T M_p

    M_stag = np.zeros((3, 3))
    for p in plaquettes:
        # B_sq is linear in n, so B_sq = A_p @ n for some 3x3 matrix A_p
        # Find A_p by applying to basis vectors
        A_p = np.zeros((3, 3))
        for j in range(3):
            e_j = np.zeros(3)
            e_j[j] = 1.0
            A_p[:, j] = compute_B_sq(Q_edges, p, e_j)
        M_stag += A_p.T @ A_p

    return M_stag

def compute_vertex_F(Q_edges, x_idx, n):
    """Compute F_x = sum_{mu<nu} |B_{(x,mu,nu)}(Q,v)|^2 for vertex x."""
    F = 0.0
    for p in plaquettes:
        if p['base'] == x_idx:
            B = compute_B_sq(Q_edges, p, n)
            F += np.dot(B, B)
    return F

# ============================================================
# Part E: Run tests
# ============================================================

print("\n" + "=" * 70)
print("TEST 1: Identity configuration")
print("=" * 70)

Q_identity = [np.eye(3)] * N_edges
M_id = compute_global_M(Q_identity)
print(f"  M_stag(I) eigenvalues: {np.sort(np.linalg.eigvalsh(M_id))}")
print(f"  Expected: all eigenvalues = some constant")
print(f"  Trace: {np.trace(M_id):.4f}")

# Also check per-vertex
n_test = np.array([1.0, 0.0, 0.0])
F_total = 0.0
for x_idx in range(N_vertices):
    F_x = compute_vertex_F(Q_identity, x_idx, n_test)
    F_total += F_x
    if x_idx < 4:
        print(f"  F_{x_idx} = {F_x:.4f}")
print(f"  Sum F_x = {F_total:.4f}")
print(f"  n^T M n = {n_test @ M_id @ n_test:.4f}")

print("\n" + "=" * 70)
print("TEST 2: Random configs - lambda_max of M_stag")
print("=" * 70)

N_tests = 1000
max_lam = 0
violations = 0
for trial in range(N_tests):
    Q_rand = [random_so3() for _ in range(N_edges)]
    M = compute_global_M(Q_rand)
    eigs = np.linalg.eigvalsh(M)
    lam_max = eigs[-1]
    max_lam = max(max_lam, lam_max)
    if lam_max > 16 + 1e-10:
        violations += 1
        print(f"  VIOLATION at trial {trial}: lambda_max = {lam_max:.6f}")

print(f"  Max lambda_max over {N_tests} trials: {max_lam:.6f}")
print(f"  Violations (> 16): {violations}")

print("\n" + "=" * 70)
print("TEST 3: Per-vertex F_x bound")
print("=" * 70)

max_F_ratio = 0
F_violations = 0
for trial in range(200):
    Q_rand = [random_so3() for _ in range(N_edges)]
    n = np.random.randn(3)
    n /= np.linalg.norm(n)

    for x_idx in range(N_vertices):
        F_x = compute_vertex_F(Q_rand, x_idx, n)
        ratio = F_x / 64.0  # should be <= |n|^2 = 1
        max_F_ratio = max(max_F_ratio, ratio)
        if ratio > 1 + 1e-10:
            F_violations += 1
            print(f"  VIOLATION: vertex {x_idx}, trial {trial}: F_x/64 = {ratio:.6f}")

print(f"  Max F_x / (64 * |n|^2) over 200 trials x 16 vertices: {max_F_ratio:.6f}")
print(f"  Violations: {F_violations}")

print("\n" + "=" * 70)
print("TEST 4: Verify Sum_x F_x = n^T M_stag n")
print("=" * 70)

max_err = 0
for trial in range(100):
    Q_rand = [random_so3() for _ in range(N_edges)]
    M = compute_global_M(Q_rand)
    n = np.random.randn(3)
    n /= np.linalg.norm(n)

    sum_F = sum(compute_vertex_F(Q_rand, x_idx, n) for x_idx in range(N_vertices))
    nMn = n @ M @ n
    err = abs(sum_F - nMn)
    max_err = max(max_err, err)

print(f"  Max |Sum_x F_x - n^T M n| over 100 trials: {max_err:.2e}")
print(f"  Identity VERIFIED: {max_err < 1e-10}")

print("\nDone.")
