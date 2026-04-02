"""
Task 6: Check L-dependence.

Critical question: On L=2, cross-links may wrap around and coincide with base links.
On L>=3, they're independent. Does the proof handle both cases?

Build the lattice for L=2 and L=3, d=4. Verify:
1. Whether D_{mu,nu} parameters are truly independent of R_mu on each lattice
2. lambda_max(M(Q)) <= 16 for random configs on L=3
3. Per-vertex F_x <= 64 on L=3
"""

import numpy as np

np.random.seed(31415)

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def build_lattice(L, d=4):
    """Build d-dimensional hypercubic torus of side L."""
    N_vertices = L**d

    def vertex_index(coords):
        idx = 0
        for i in range(d):
            idx = idx * L + (coords[i] % L)
        return idx

    def index_to_coords(idx):
        coords = []
        for i in range(d):
            coords.append(idx % L)
            idx //= L
        return tuple(reversed(coords))

    vertices = [index_to_coords(i) for i in range(N_vertices)]

    # Edge index: (vertex_idx, direction) -> edge_idx
    edge_idx = {}
    for x_idx in range(N_vertices):
        for mu in range(d):
            edge_idx[(x_idx, mu)] = x_idx * d + mu

    N_edges = N_vertices * d

    # Plaquettes
    plaquettes = []
    for x_idx in range(N_vertices):
        x = vertices[x_idx]
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
                x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L

                e1 = edge_idx[(x_idx, mu)]
                e2 = edge_idx[(vertex_index(tuple(x_mu)), nu)]
                e3 = edge_idx[(vertex_index(tuple(x_nu)), mu)]
                e4 = edge_idx[(x_idx, nu)]

                plaquettes.append((e1, e2, e3, e4, x_idx, mu, nu))

    return vertices, edge_idx, N_vertices, N_edges, plaquettes, index_to_coords

def compute_B_sq(Q, p, n, vertices, d, L):
    """Compute B_sq for plaquette p with staggered mode amplitude n."""
    e1, e2, e3, e4, x_idx, mu, nu = p
    x = vertices[x_idx]

    Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
    U_sq = Q1 @ Q2 @ Q3.T @ Q4.T

    # Staggered signs
    s1 = (-1) ** (sum(x) + mu)
    x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
    s2 = (-1) ** (sum(x_mu) + nu)
    x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L
    s3 = (-1) ** (sum(x_nu) + mu)
    s4 = (-1) ** (sum(x) + nu)

    B = s1*n + s2*(Q1 @ n) - s3*(Q1 @ Q2 @ Q3.T @ n) - s4*(U_sq @ n)
    return B

def compute_full_M(Q, vertices, edge_idx, N_vertices, N_edges, plaquettes, d, L):
    """Build full M(Q) matrix."""
    N_dim = N_edges * 3
    M = np.zeros((N_dim, N_dim))

    for plaq in plaquettes:
        e1, e2, e3, e4 = plaq[0], plaq[1], plaq[2], plaq[3]
        Q1, Q2, Q3, Q4 = Q[e1], Q[e2], Q[e3], Q[e4]
        U_sq = Q1 @ Q2 @ Q3.T @ Q4.T

        blocks = {
            e1: np.eye(3),
            e2: Q1.copy(),
            e3: -(Q1 @ Q2 @ Q3.T),
            e4: -U_sq.copy()
        }

        edge_list = [e1, e2, e3, e4]
        for ei in edge_list:
            Bi = blocks[ei]
            for ej in edge_list:
                Bj = blocks[ej]
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Bi.T @ Bj

    return M

# ============================================================
# Part A: L=2 edge sharing analysis
# ============================================================

print("=" * 70)
print("TASK 6A: Edge sharing on L=2 torus")
print("=" * 70)

L = 2; d = 4
verts, eidx, NV, NE, plaqs, idx2c = build_lattice(L, d)
print(f"L={L}: {NV} vertices, {NE} edges, {len(plaqs)} plaquettes")

# For vertex x=0, plaquette (0,1):
# e1 = (0, 0), e2 = (x+e_0, 1), e3 = (x+e_1, 0), e4 = (0, 1)
# On L=2: x+e_0 = (1,0,0,0), x+e_1 = (0,1,0,0)
# e2 goes from (1,0,0,0) in direction 1
# e3 goes from (0,1,0,0) in direction 0

# For vertex x=(1,0,0,0), plaquette (0,1):
# e1' = ((1,0,0,0), 0), e2' = ((0,0,0,0), 1) = e4 above!, e3' = ((1,1,0,0), 0), e4' = ((1,0,0,0), 1) = e2 from above!

print("\nEdge sharing between vertex 0 and vertex 1 plaquettes:")
x0 = (0,0,0,0)
x1 = (1,0,0,0)

def vertex_index(coords, L=2, d=4):
    idx = 0
    for i in range(d):
        idx = idx * L + (coords[i] % L)
    return idx

for mu, nu in [(0,1)]:
    x0_mu = list(x0); x0_mu[mu] = (x0_mu[mu]+1)%L
    x0_nu = list(x0); x0_nu[nu] = (x0_nu[nu]+1)%L
    e1_0 = eidx[(vertex_index(x0), mu)]
    e2_0 = eidx[(vertex_index(tuple(x0_mu)), nu)]
    e3_0 = eidx[(vertex_index(tuple(x0_nu)), mu)]
    e4_0 = eidx[(vertex_index(x0), nu)]
    print(f"  Vertex {x0}, plane ({mu},{nu}): edges {e1_0}, {e2_0}, {e3_0}, {e4_0}")

    x1_mu = list(x1); x1_mu[mu] = (x1_mu[mu]+1)%L
    x1_nu = list(x1); x1_nu[nu] = (x1_nu[nu]+1)%L
    e1_1 = eidx[(vertex_index(x1), mu)]
    e2_1 = eidx[(vertex_index(tuple(x1_mu)), nu)]
    e3_1 = eidx[(vertex_index(tuple(x1_nu)), mu)]
    e4_1 = eidx[(vertex_index(x1), nu)]
    print(f"  Vertex {x1}, plane ({mu},{nu}): edges {e1_1}, {e2_1}, {e3_1}, {e4_1}")

    shared = set([e1_0,e2_0,e3_0,e4_0]) & set([e1_1,e2_1,e3_1,e4_1])
    print(f"  Shared edges: {shared}")

# On L=2, adjacent vertices share edges. This means the "cross-link" D_{mu,nu}
# at one vertex involves the "base link" R_nu at the adjacent vertex.
# The proof bounds lambda_max(M_total) <= 64 for ARBITRARY R_mu, D_{mu,nu} in SO(3).
# On the actual lattice, the rotations at different vertices are coupled.
# But since the bound is universal (works for ALL rotation choices), the coupling
# doesn't matter — each vertex's bound holds independently.

print("\nThe per-vertex bound is UNIVERSAL (valid for all SO(3) configurations),")
print("so edge sharing between vertices doesn't affect the proof.")

# ============================================================
# Part B: L=3 full matrix check
# ============================================================

print("\n" + "=" * 70)
print("TASK 6B: L=3, d=4 lattice (full matrix)")
print("=" * 70)

L = 3; d = 4
verts3, eidx3, NV3, NE3, plaqs3, idx2c3 = build_lattice(L, d)
print(f"L={L}: {NV3} vertices, {NE3} edges, {len(plaqs3)} plaquettes")
print(f"Full matrix size: {NE3*3} x {NE3*3}")

# Full matrix is 324x324, feasible but slow. Let me use the staggered mode approach.

def staggered_M(Q, vertices, plaquettes, d, L, NE):
    """Compute the 3x3 matrix M_stag restricted to staggered modes."""
    M = np.zeros((3, 3))
    for p in plaquettes:
        A_p = np.zeros((3, 3))
        for j in range(3):
            ej = np.zeros(3); ej[j] = 1.0
            A_p[:, j] = compute_B_sq(Q, p, ej, vertices, d, L)
        M += A_p.T @ A_p
    return M

# |v|^2 for staggered mode = NE (each edge contributes |n|^2 = 1)

N_test = 50
max_stag_rq = 0
for trial in range(N_test):
    Q = [random_so3() for _ in range(NE3)]
    M_s = staggered_M(Q, verts3, plaqs3, d, L, NE3)
    eigs = np.linalg.eigvalsh(M_s)
    rq = eigs[-1] / NE3  # Rayleigh quotient = eigenvalue / |v|^2
    max_stag_rq = max(max_stag_rq, rq)
    if trial < 5:
        print(f"  Trial {trial}: M_stag eigenvalues = {np.sort(eigs)}, Rayleigh = {rq:.6f}")

print(f"\n  Max staggered Rayleigh quotient over {N_test} trials: {max_stag_rq:.6f} (bound: 16)")

# Per-vertex F_x check on L=3
print("\n--- Per-vertex F_x bound on L=3 ---")
max_F_ratio = 0
for trial in range(20):
    Q = [random_so3() for _ in range(NE3)]
    n = np.random.randn(3); n /= np.linalg.norm(n)

    for x_idx in range(NV3):
        F_x = 0.0
        for p in plaqs3:
            if p[4] == x_idx:  # base vertex
                B = compute_B_sq(Q, p, n, verts3, d, L)
                F_x += np.dot(B, B)
        ratio = F_x / 64.0
        max_F_ratio = max(max_F_ratio, ratio)

print(f"  Max F_x / 64 over 20 trials x {NV3} vertices: {max_F_ratio:.6f}")
print(f"  Violations: {'YES' if max_F_ratio > 1 + 1e-10 else 'NONE'}")

# ============================================================
# Part C: L=3 full matrix eigenvalue check (smaller sample)
# ============================================================

print("\n--- L=3 full matrix eigenvalue check ---")
# 324x324 matrix, should be ok for a few configs

for trial in range(5):
    Q = [random_so3() for _ in range(NE3)]
    M_full = compute_full_M(Q, verts3, eidx3, NV3, NE3, plaqs3, d, L)
    eigs = np.linalg.eigvalsh(M_full)
    print(f"  Trial {trial}: lambda_max = {eigs[-1]:.6f} (bound: 16)")

# Identity config for L=3
Q_id = [np.eye(3)] * NE3
M_full_id = compute_full_M(Q_id, verts3, eidx3, NV3, NE3, plaqs3, d, L)
eigs_id = np.linalg.eigvalsh(M_full_id)
print(f"\n  Identity: lambda_max = {eigs_id[-1]:.6f}")
print(f"  Distinct eigenvalues: {np.unique(np.round(eigs_id, 4))}")
for ue in np.unique(np.round(eigs_id, 4)):
    count = np.sum(np.abs(eigs_id - ue) < 0.01)
    print(f"    {ue:.4f}: multiplicity {count}")

print("\nDone.")
