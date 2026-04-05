"""
Stage 1: Setup and Verification for Maximal Tree Gauge Decomposition
Yang-Mills Hessian bound on L=2, d=4 hypercubic torus with SU(2).

Lattice: (Z/2Z)^4, vertices=16, edges=64, plaquettes=96.
SU(2) represented as 2x2 unitary matrices with det=1.
Lie algebra su(2) basis: sigma_a / (2i) where sigma_a are Pauli matrices.
We use |A|^2 = -2 Tr(A^2) (SZZ convention).
"""

import numpy as np
from scipy import linalg
import itertools

np.random.seed(42)

# =============================================================================
# SU(2) Utilities
# =============================================================================

# Pauli matrices
sigma = np.array([
    [[0, 1], [1, 0]],       # sigma_1
    [[0, -1j], [1j, 0]],    # sigma_2
    [[1, 0], [0, -1]],      # sigma_3
], dtype=complex)

# su(2) basis: T_a = sigma_a / (2i) = -i sigma_a / 2
# We use the convention that v in R^3 represents the Lie algebra element sum_a v_a T_a
# |A|^2 = -2 Tr(A^2) for A in su(2)
# For A = sum v_a T_a: |A|^2 = -2 Tr(sum v_a v_b T_a T_b) = sum v_a^2 (since -2Tr(T_a T_b) = delta_ab)

def random_su2():
    """Generate a random SU(2) element using quaternion parametrization."""
    v = np.random.randn(4)
    v = v / np.linalg.norm(v)
    # q = a + b*i*sigma_1 + c*i*sigma_2 + d*i*sigma_3
    # U = v[0]*I + i*(v[1]*sigma_1 + v[2]*sigma_2 + v[3]*sigma_3)
    U = v[0] * np.eye(2, dtype=complex) + 1j * sum(v[k+1] * sigma[k] for k in range(3))
    return U

def su2_adj(U, X):
    """Adjoint action: Ad_U(X) = U X U^dagger, for X in su(2) (as 2x2 matrix)."""
    return U @ X @ U.conj().T

def lie_to_matrix(v):
    """Convert R^3 vector to su(2) matrix: X = sum_a v_a T_a = -i/2 sum v_a sigma_a."""
    return -0.5j * sum(v[a] * sigma[a] for a in range(3))

def matrix_to_lie(X):
    """Convert su(2) matrix to R^3 vector. T_a = -i sigma_a / 2, so v_a = -2 Tr(T_a^dag X) = Tr(i sigma_a X)."""
    # v_a = -2 Tr(T_a X) ... but T_a = -i sigma_a/2, so -2 Tr(T_a X) = i Tr(sigma_a X)
    # Actually: |A|^2 = -2Tr(A^2), and for A = sum v_a T_a, -2Tr(T_a T_b) = delta_ab/2 * 2 = delta_ab... let me be careful.
    # T_a = -i sigma_a / 2
    # Tr(T_a T_b) = Tr((-i sigma_a/2)(-i sigma_b/2)) = -1/4 Tr(sigma_a sigma_b) = -1/4 * 2 delta_ab = -delta_ab/2
    # So -2 Tr(T_a T_b) = delta_ab. Good, so our basis is orthonormal under |.|^2 = -2Tr(.^2)
    # To extract: v_a = -2 Tr(T_a^T X) where T_a^T means the transpose in the inner product
    # Since -2Tr(T_a T_b) = delta_ab, we have v_a = -2 Tr(T_a X)
    # T_a = -i sigma_a / 2, so -2 Tr(T_a X) = -2 Tr(-i sigma_a/2 X) = i Tr(sigma_a X)
    v = np.zeros(3)
    for a in range(3):
        v[a] = (1j * np.trace(sigma[a] @ X)).real
    return v

def ad_action_matrix(U):
    """
    Compute the 3x3 matrix representing Ad_U in the T_a basis.
    (Ad_U)_{ab} = -2 Tr(T_a U T_b U^dag)
    """
    R = np.zeros((3, 3))
    Ud = U.conj().T
    for a in range(3):
        for b in range(3):
            Ta = -0.5j * sigma[a]
            Tb = -0.5j * sigma[b]
            R[a, b] = (-2 * np.trace(Ta @ U @ Tb @ Ud)).real
    return R

# Verify: Ad_I should be identity
assert np.allclose(ad_action_matrix(np.eye(2, dtype=complex)), np.eye(3))

# Verify: random SU(2) should give SO(3) matrix
U_test = random_su2()
R_test = ad_action_matrix(U_test)
assert np.allclose(R_test @ R_test.T, np.eye(3), atol=1e-10)
assert np.allclose(np.linalg.det(R_test), 1.0, atol=1e-10)

print("SU(2) utilities verified.")

# =============================================================================
# Lattice Setup: (Z/LZ)^d
# =============================================================================

L = 2
d = 4
N_vertices = L**d      # 16
N_edges = d * L**d      # 64
N_plaquettes = d*(d-1)//2 * L**d  # 96

print(f"L={L}, d={d}: {N_vertices} vertices, {N_edges} edges, {N_plaquettes} plaquettes")

def vertex_index(x):
    """Convert d-tuple (mod L) to vertex index."""
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def index_to_vertex(idx):
    """Convert vertex index to d-tuple."""
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return tuple(reversed(x))

# Verify bijection
for v in range(N_vertices):
    assert vertex_index(index_to_vertex(v)) == v

# Edge indexing: edge (x, mu) goes from vertex x to vertex x + e_mu
# Edge index = mu * L^d + vertex_index(x)
def edge_index(x, mu):
    """Edge from x in direction mu."""
    return mu * N_vertices + vertex_index(x)

def edge_endpoints(e):
    """Return (start_vertex, end_vertex, mu) for edge e."""
    mu = e // N_vertices
    v_start = e % N_vertices
    x = list(index_to_vertex(v_start))
    x_end = list(x)
    x_end[mu] = (x_end[mu] + 1) % L
    v_end = vertex_index(x_end)
    return v_start, v_end, mu

# Plaquette setup
# A plaquette at vertex x in the (mu, nu) plane (mu < nu) has 4 edges:
# e1: (x, mu) forward
# e2: (x+e_mu, nu) forward
# e3: (x+e_nu, mu) forward (traversed backward = from x+e_mu+e_nu to x+e_nu)
# e4: (x, nu) forward (traversed backward = from x+e_nu to x)
# Holonomy: U_sq = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}

plaquettes = []  # List of (e1, e2, e3, e4) edge indices
for v in range(N_vertices):
    x = list(index_to_vertex(v))
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = edge_index(x, mu)
            x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
            e2 = edge_index(x_mu, nu)
            x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L
            e3 = edge_index(x_nu, mu)
            x4 = list(x)
            e4 = edge_index(x4, nu)
            plaquettes.append((e1, e2, e3, e4))

assert len(plaquettes) == N_plaquettes
print(f"Constructed {N_plaquettes} plaquettes.")

# =============================================================================
# Maximal Spanning Tree
# =============================================================================

# Build adjacency for the torus graph using BFS to find a spanning tree
from collections import deque

def find_spanning_tree():
    """Find a maximal spanning tree of the torus using BFS."""
    visited = set()
    tree_edges = set()  # Set of edge indices
    queue = deque([0])  # Start from vertex 0
    visited.add(0)

    while queue:
        v = queue.popleft()
        x = list(index_to_vertex(v))
        for mu in range(d):
            # Forward edge from v
            x_next = list(x)
            x_next[mu] = (x_next[mu] + 1) % L
            v_next = vertex_index(x_next)
            if v_next not in visited:
                visited.add(v_next)
                e = edge_index(x, mu)
                tree_edges.add(e)
                queue.append(v_next)
            # Backward edge to v
            x_prev = list(x)
            x_prev[mu] = (x_prev[mu] - 1) % L
            v_prev = vertex_index(x_prev)
            if v_prev not in visited:
                visited.add(v_prev)
                # The edge from x_prev in direction mu
                e = edge_index(x_prev, mu)
                tree_edges.add(e)
                queue.append(v_prev)

    return tree_edges

tree_edges = find_spanning_tree()
non_tree_edges = set(range(N_edges)) - tree_edges

print(f"Tree edges: {len(tree_edges)} (expected {N_vertices - 1} = {N_vertices - 1})")
print(f"Non-tree edges: {len(non_tree_edges)} (expected {N_edges - N_vertices + 1} = {N_edges - N_vertices + 1})")
assert len(tree_edges) == N_vertices - 1
assert len(non_tree_edges) == N_edges - N_vertices + 1

# =============================================================================
# Gauge Transformation to Maximal Tree Gauge
# =============================================================================

def find_tree_path(tree_edges_set, target_vertex):
    """Find path from vertex 0 to target_vertex using only tree edges.
    Returns list of (edge_index, direction) where direction is +1 (forward) or -1 (backward)."""
    if target_vertex == 0:
        return []

    # BFS on the tree
    parent = {0: None}
    queue = deque([0])

    while queue:
        v = queue.popleft()
        if v == target_vertex:
            break
        x = list(index_to_vertex(v))
        for mu in range(d):
            # Forward: edge (x, mu)
            e = edge_index(x, mu)
            x_next = list(x); x_next[mu] = (x_next[mu] + 1) % L
            v_next = vertex_index(x_next)
            if e in tree_edges_set and v_next not in parent:
                parent[v_next] = (v, e, +1)
                queue.append(v_next)
            # Backward: edge (x_prev, mu) where x_prev[mu]+1 = x[mu]
            x_prev = list(x); x_prev[mu] = (x_prev[mu] - 1) % L
            e_back = edge_index(x_prev, mu)
            v_prev = vertex_index(x_prev)
            if e_back in tree_edges_set and v_prev not in parent:
                parent[v_prev] = (v, e_back, -1)
                queue.append(v_prev)

    # Reconstruct path
    path = []
    v = target_vertex
    while parent[v] is not None:
        prev_v, e, direction = parent[v]
        path.append((e, direction))
        v = prev_v
    path.reverse()
    return path

def compute_gauge_transforms(Q, tree_edges_set):
    """
    Compute gauge transformations G[v] for each vertex such that
    G[v_start] Q_e G[v_end]^{-1} = I for all tree edges e.

    Convention: gauge-transformed link Q'_e = G[start(e)] Q_e G[end(e)]^{-1}
    We set G[0] = I and determine G[v] from the tree.
    """
    G = [None] * N_vertices
    G[0] = np.eye(2, dtype=complex)

    for v in range(1, N_vertices):
        path = find_tree_path(tree_edges_set, v)
        # The holonomy along the path from 0 to v:
        # For forward edge e: contributes Q_e
        # For backward edge e: contributes Q_e^{-1}
        # G[v] must satisfy: for tree edge from a to b, G[a] Q_e G[b]^{-1} = I => G[b] = Q_e^{-1} G[a]... wait
        # Actually: Q'_e = G[start] Q_e G[end]^dag = I => G[end] = Q_e G[start]... no.
        # G[start] Q_e G[end]^{-1} = I => G[end] = G[start] Q_e
        # So walking from 0 to v along tree:
        # G[v] = G[0] * (product of Q along path)
        hol = np.eye(2, dtype=complex)
        for (e, direction) in path:
            if direction == +1:
                hol = hol @ Q[e]
            else:
                hol = hol @ Q[e].conj().T
        G[v] = hol

    return G

def gauge_transform(Q, G):
    """Apply gauge transformation: Q'_e = G[start(e)] Q_e G[end(e)]^{-1}."""
    Q_new = [None] * N_edges
    for e in range(N_edges):
        v_start, v_end, mu = edge_endpoints(e)
        Q_new[e] = G[v_start] @ Q[e] @ G[v_end].conj().T
    return Q_new

# =============================================================================
# B_square formula and M(Q) operator
# =============================================================================

def compute_B_sq(Q, sq_idx, v_vec):
    """
    Compute B_sq(Q, v) for plaquette sq_idx.

    v_vec is a vector of length N_edges * 3 (3 Lie algebra components per edge).

    B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

    Returns a 3-vector (the Lie algebra result).
    """
    e1, e2, e3, e4 = plaquettes[sq_idx]

    v1 = v_vec[3*e1:3*e1+3]
    v2 = v_vec[3*e2:3*e2+3]
    v3 = v_vec[3*e3:3*e3+3]
    v4 = v_vec[3*e4:3*e4+3]

    R1 = ad_action_matrix(Q[e1])

    P12 = Q[e1] @ Q[e2]
    P123inv = Q[e1] @ Q[e2] @ Q[e3].conj().T
    R123inv = ad_action_matrix(P123inv)

    U_sq = P123inv @ Q[e4].conj().T
    R_sq = ad_action_matrix(U_sq)

    result = v1 + R1 @ v2 - R123inv @ v3 - R_sq @ v4
    return result

def compute_M_matrix(Q):
    """
    Compute the full M(Q) matrix of size (N_edges*3) x (N_edges*3).
    M(Q) = sum_sq B_sq^T B_sq (Gram operator).
    """
    dim = N_edges * 3
    M = np.zeros((dim, dim))

    for sq_idx in range(N_plaquettes):
        # Build the linear map v -> B_sq(Q, v)
        # B_sq maps R^{N_edges*3} -> R^3
        B = np.zeros((3, dim))
        for j in range(dim):
            e_j = np.zeros(dim)
            e_j[j] = 1.0
            B[:, j] = compute_B_sq(Q, sq_idx, e_j)
        M += B.T @ B

    return M

# Faster version: precompute B matrices
def compute_M_matrix_fast(Q):
    """
    Compute M(Q) more efficiently using precomputed adjoint matrices.
    """
    dim = N_edges * 3
    M = np.zeros((dim, dim))

    for sq_idx in range(N_plaquettes):
        e1, e2, e3, e4 = plaquettes[sq_idx]

        # Precompute adjoint matrices
        R1 = ad_action_matrix(Q[e1])
        P123inv = Q[e1] @ Q[e2] @ Q[e3].conj().T
        R123inv = ad_action_matrix(P123inv)
        U_sq = P123inv @ Q[e4].conj().T
        R_sq = ad_action_matrix(U_sq)

        # B_sq(v) = I*v_{e1} + R1*v_{e2} - R123inv*v_{e3} - R_sq*v_{e4}
        # B is 3 x dim matrix, only nonzero in columns for e1,e2,e3,e4 (each 3 cols)
        # M += B^T B

        # Edges and their coefficient matrices (3x3 blocks)
        edges = [e1, e2, e3, e4]
        coeffs = [np.eye(3), R1, -R123inv, -R_sq]

        for i, (ei, Ci) in enumerate(zip(edges, coeffs)):
            for j, (ej, Cj) in enumerate(zip(edges, coeffs)):
                # Contribution: Ci^T Cj added to block (ei, ej)
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ci.T @ Cj

    return M

# =============================================================================
# Staggered mode subspace P
# =============================================================================

def staggered_modes():
    """
    Compute the 9-dimensional staggered mode subspace.
    v_{x,mu,a} = (-1)^{|x|+mu} delta_{a,b} for each (mu_0, b) pair.
    Wait -- the modes are: for each color a=0,1,2:
    v^a_{e} where e = edge(x, mu): v^a_{x,mu,b} = (-1)^{sum(x)+mu} delta_{a,b}

    Actually, re-reading: "staggered modes v_{x,mu} = (-1)^{|x|+mu} e_a for a=1,2,3"
    So there are 3 modes (one per color), and they're 9-dimensional total...
    wait, 3 colors but 4 directions. Let me think again.

    The top eigenspace of M(I) is 9-dimensional. The modes are:
    For each mu=0,...,3 and a=0,1,2, but that would be 12... unless there's a constraint.

    Actually for d=4, M(I) has eigenvalue 4d=16 with multiplicity... let me just compute M(I) and find it.
    """
    pass

# Actually, let's just compute M(I) and find the top eigenspace directly.
print("\nComputing M(I)...")
Q_identity = [np.eye(2, dtype=complex)] * N_edges
M_I = compute_M_matrix_fast(Q_identity)
print(f"M(I) shape: {M_I.shape}")
print(f"M(I) symmetric: {np.allclose(M_I, M_I.T)}")

eigenvalues_I, eigenvectors_I = np.linalg.eigh(M_I)
print(f"Top 15 eigenvalues of M(I): {eigenvalues_I[-15:]}")
print(f"Max eigenvalue of M(I): {eigenvalues_I[-1]:.6f} (expected 4d={4*d})")

# Find the top eigenspace (eigenvalue = 16)
top_mask = np.abs(eigenvalues_I - 4*d) < 1e-6
top_multiplicity = np.sum(top_mask)
print(f"Top eigenvalue multiplicity: {top_multiplicity}")

# P is the projector onto the top eigenspace
P = eigenvectors_I[:, top_mask]  # dim x multiplicity matrix
print(f"P shape: {P.shape} (should be {N_edges*3} x {top_multiplicity})")

# Verify staggered mode structure
# For edge e = (x, mu): the staggered mode has v_{x,mu,a} = (-1)^{sum(x)+mu}
# Let's check
stag_modes = np.zeros((N_edges * 3, 3 * d))  # 3 colors x 4 directions = 12 modes
mode_idx = 0
for mu in range(d):
    for a in range(3):
        v = np.zeros(N_edges * 3)
        for vert in range(N_vertices):
            x = index_to_vertex(vert)
            e = edge_index(list(x), mu)
            sign = (-1) ** (sum(x) + mu)
            v[3*e + a] = sign
        # Normalize
        v = v / np.linalg.norm(v)
        stag_modes[:, mode_idx] = v
        mode_idx += 1

# Check which of these are in the top eigenspace
print("\nStaggered mode M(I) eigenvalue check:")
for k in range(12):
    Mv = M_I @ stag_modes[:, k]
    lam = np.dot(stag_modes[:, k], Mv)
    print(f"  Mode {k} (mu={k//3}, a={k%3}): eigenvalue = {lam:.6f}")

# The top eigenspace might be a subset; let's see which modes have eigenvalue 16
stag_in_top = []
for k in range(12):
    Mv = M_I @ stag_modes[:, k]
    lam = np.dot(stag_modes[:, k], Mv)
    if abs(lam - 16) < 0.1:
        stag_in_top.append(k)

print(f"\nStaggered modes in top eigenspace: {stag_in_top} ({len(stag_in_top)} modes)")

# =============================================================================
# Stage 1: Verification with random configs
# =============================================================================

print("\n" + "="*80)
print("Stage 1: Random configuration verification")
print("="*80)

results = []

for trial in range(20):
    # Generate random SU(2) config
    Q = [random_su2() for _ in range(N_edges)]

    # Compute M(Q) before gauge fixing
    M_Q = compute_M_matrix_fast(Q)
    eigs_Q = np.linalg.eigvalsh(M_Q)
    lambda_max_before = eigs_Q[-1]

    # Compute P^T R(Q) P before gauge fixing
    R_Q = M_Q - M_I
    PtRP_before = P.T @ R_Q @ P
    eigs_PtRP_before = np.linalg.eigvalsh(PtRP_before)
    max_PtRP_before = eigs_PtRP_before[-1]

    # Gauge transform to maximal tree gauge
    G = compute_gauge_transforms(Q, tree_edges)
    Q_tree = gauge_transform(Q, G)

    # Verify tree edges are identity
    tree_ok = all(np.allclose(Q_tree[e], np.eye(2, dtype=complex), atol=1e-10) for e in tree_edges)

    # Compute M(Q) after gauge fixing
    M_Q_tree = compute_M_matrix_fast(Q_tree)
    eigs_Q_tree = np.linalg.eigvalsh(M_Q_tree)
    lambda_max_after = eigs_Q_tree[-1]

    # Compute P^T R(Q) P after gauge fixing
    R_Q_tree = M_Q_tree - M_I
    PtRP_after = P.T @ R_Q_tree @ P
    eigs_PtRP_after = np.linalg.eigvalsh(PtRP_after)
    max_PtRP_after = eigs_PtRP_after[-1]

    # Weitzenbock: W(Q) = sum_sq (1 - Re Tr(U_sq)/2)... actually need to compute it
    W = 0.0
    for sq_idx in range(N_plaquettes):
        e1, e2, e3, e4 = plaquettes[sq_idx]
        U_sq = Q_tree[e1] @ Q_tree[e2] @ Q_tree[e3].conj().T @ Q_tree[e4].conj().T
        W += (1 - np.trace(U_sq).real / 2)

    results.append({
        'id': trial,
        'lambda_max_before': lambda_max_before,
        'lambda_max_after': lambda_max_after,
        'max_PtRP_before': max_PtRP_before,
        'max_PtRP_after': max_PtRP_after,
        'tree_ok': tree_ok,
        'gauge_covariant': abs(lambda_max_before - lambda_max_after) < 1e-6,
        'PtRP_le_0': max_PtRP_after < 1e-10,
        'W': W,
    })

    if trial < 3 or trial == 19:
        print(f"\nConfig {trial}:")
        print(f"  Tree links = I: {tree_ok}")
        print(f"  lambda_max before: {lambda_max_before:.8f}, after: {lambda_max_after:.8f}, diff: {abs(lambda_max_before - lambda_max_after):.2e}")
        print(f"  max eig(P^T R P) before: {max_PtRP_before:.8f}, after: {max_PtRP_after:.8f}")
        print(f"  P^T R P <= 0: {max_PtRP_after < 1e-10}")
        print(f"  W(Q) = {W:.6f}")

print("\n\nSummary of 20 configs:")
all_tree_ok = all(r['tree_ok'] for r in results)
all_gauge_cov = all(r['gauge_covariant'] for r in results)
all_PtRP_neg = all(r['PtRP_le_0'] for r in results)
print(f"  All tree links = I: {all_tree_ok}")
print(f"  Gauge covariance (lambda_max preserved): {all_gauge_cov}")
print(f"  P^T R P <= 0 for all: {all_PtRP_neg}")
print(f"  lambda_max range: [{min(r['lambda_max_after'] for r in results):.4f}, {max(r['lambda_max_after'] for r in results):.4f}]")
print(f"  max eig(P^T R P) range: [{min(r['max_PtRP_after'] for r in results):.6f}, {max(r['max_PtRP_after'] for r in results):.6f}]")

# Print verification table
print("\n\nVerification Table:")
print(f"{'ID':>4} {'λ_max(M(Q))':>14} {'max eig(P^TR P)':>18} {'W(Q)':>10} {'Tree OK':>8} {'Gauge Cov':>10} {'P^TRP≤0':>8}")
print("-" * 85)
for r in results:
    print(f"{r['id']:>4} {r['lambda_max_after']:>14.6f} {r['max_PtRP_after']:>18.8f} {r['W']:>10.4f} {str(r['tree_ok']):>8} {str(r['gauge_covariant']):>10} {str(r['PtRP_le_0']):>8}")
