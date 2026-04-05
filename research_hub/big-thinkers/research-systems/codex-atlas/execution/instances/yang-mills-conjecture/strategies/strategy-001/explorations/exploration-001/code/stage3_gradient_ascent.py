"""
Stage 3: Gradient ascent on P^T R(Q) P in maximal tree gauge
+ Detailed analysis of the decomposition structure
"""

import numpy as np
from collections import defaultdict

np.random.seed(42)

# =============================================================================
# Full lattice setup (self-contained)
# =============================================================================

sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)

L = 2
d = 4
N_vertices = L**d
N_edges = d * L**d
N_plaquettes = d*(d-1)//2 * L**d

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def index_to_vertex(idx):
    x = []
    for i in range(d):
        x.append(idx % L)
        idx //= L
    return tuple(reversed(x))

def edge_index(x, mu):
    return mu * N_vertices + vertex_index(x)

def edge_endpoints(e):
    mu = e // N_vertices
    v_start = e % N_vertices
    x = list(index_to_vertex(v_start))
    x_end = list(x)
    x_end[mu] = (x_end[mu] + 1) % L
    v_end = vertex_index(x_end)
    return v_start, v_end, mu

plaquettes = []
for v in range(N_vertices):
    x = list(index_to_vertex(v))
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = edge_index(x, mu)
            x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
            e2 = edge_index(x_mu, nu)
            x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L
            e3 = edge_index(x_nu, mu)
            e4 = edge_index(x, nu)
            plaquettes.append((e1, e2, e3, e4))

from collections import deque
def find_spanning_tree():
    visited = set()
    tree_edges = set()
    queue = deque([0])
    visited.add(0)
    while queue:
        v = queue.popleft()
        x = list(index_to_vertex(v))
        for mu in range(d):
            x_next = list(x); x_next[mu] = (x_next[mu] + 1) % L
            v_next = vertex_index(x_next)
            if v_next not in visited:
                visited.add(v_next)
                tree_edges.add(edge_index(x, mu))
                queue.append(v_next)
            x_prev = list(x); x_prev[mu] = (x_prev[mu] - 1) % L
            v_prev = vertex_index(x_prev)
            if v_prev not in visited:
                visited.add(v_prev)
                tree_edges.add(edge_index(x_prev, mu))
                queue.append(v_prev)
    return tree_edges

tree_edges = find_spanning_tree()
non_tree_edges = sorted(set(range(N_edges)) - tree_edges)
non_tree_set = set(non_tree_edges)

def random_su2():
    v = np.random.randn(4)
    v = v / np.linalg.norm(v)
    return v[0] * np.eye(2, dtype=complex) + 1j * sum(v[k+1] * sigma[k] for k in range(3))

def ad_action_matrix(U):
    R = np.zeros((3, 3))
    Ud = U.conj().T
    for a in range(3):
        for b in range(3):
            Ta = -0.5j * sigma[a]
            Tb = -0.5j * sigma[b]
            R[a, b] = (-2 * np.trace(Ta @ U @ Tb @ Ud)).real
    return R

def compute_M_matrix_fast(Q):
    dim = N_edges * 3
    M = np.zeros((dim, dim))
    for sq_idx in range(N_plaquettes):
        e1, e2, e3, e4 = plaquettes[sq_idx]
        R1 = ad_action_matrix(Q[e1])
        P123inv = Q[e1] @ Q[e2] @ Q[e3].conj().T
        R123inv = ad_action_matrix(P123inv)
        U_sq = P123inv @ Q[e4].conj().T
        R_sq = ad_action_matrix(U_sq)
        edges_list = [e1, e2, e3, e4]
        coeffs = [np.eye(3), R1, -R123inv, -R_sq]
        for i, (ei, Ci) in enumerate(zip(edges_list, coeffs)):
            for j, (ej, Cj) in enumerate(zip(edges_list, coeffs)):
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ci.T @ Cj
    return M

# Compute M(I) and P
Q_I = [np.eye(2, dtype=complex)] * N_edges
M_I = compute_M_matrix_fast(Q_I)
eigenvalues_I, eigenvectors_I = np.linalg.eigh(M_I)
top_mask = np.abs(eigenvalues_I - 16.0) < 1e-6
P = eigenvectors_I[:, top_mask]
print(f"P shape: {P.shape}")

# Classify plaquettes
plaq_by_ntree = defaultdict(list)
for sq_idx, (e1, e2, e3, e4) in enumerate(plaquettes):
    n_nontree = sum(1 for e in [e1, e2, e3, e4] if e in non_tree_set)
    plaq_by_ntree[n_nontree].append(sq_idx)

# =============================================================================
# Part 1: Gradient ascent on max eig(P^T R P) in tree gauge
# =============================================================================

print("="*80)
print("Part 1: Gradient ascent on max eigenvalue of P^T R P in tree gauge")
print("="*80)

def su2_exp(omega):
    """Exponential map: omega in R^3 -> SU(2)."""
    theta = np.linalg.norm(omega)
    if theta < 1e-12:
        return np.eye(2, dtype=complex)
    n = omega / theta
    return np.cos(theta) * np.eye(2, dtype=complex) + 1j * np.sin(theta) * sum(n[k] * sigma[k] for k in range(3))

def tree_gauge_config(params):
    """Build config from params: flattened array of 3*len(non_tree_edges) reals.
    Each non-tree edge gets 3 Lie algebra parameters via exp map."""
    Q = [np.eye(2, dtype=complex)] * N_edges
    for idx, e in enumerate(non_tree_edges):
        omega = params[3*idx:3*idx+3]
        Q[e] = su2_exp(omega)
    return Q

def objective(params):
    """Compute max eigenvalue of P^T R(Q) P in tree gauge."""
    Q = tree_gauge_config(params)
    M_Q = compute_M_matrix_fast(Q)
    R_Q = M_Q - M_I
    PtRP = P.T @ R_Q @ P
    eigs = np.linalg.eigvalsh(PtRP)
    return eigs[-1]  # max eigenvalue

def objective_and_gradient(params, delta=1e-5):
    """Compute objective and numerical gradient."""
    val = objective(params)
    grad = np.zeros_like(params)
    for i in range(len(params)):
        params_p = params.copy()
        params_p[i] += delta
        grad[i] = (objective(params_p) - val) / delta
    return val, grad

# Run gradient ascent from multiple starting points
n_params = 3 * len(non_tree_edges)  # 147
print(f"Number of parameters: {n_params}")

best_val = -np.inf
best_params = None

for trial in range(10):
    # Random starting point
    params = np.random.randn(n_params) * np.pi  # Full range of SU(2)

    lr = 0.1
    prev_val = -np.inf

    for step in range(100):
        val, grad = objective_and_gradient(params)

        if step % 20 == 0 or step == 99:
            print(f"  Trial {trial}, step {step}: max eig(P^T R P) = {val:.8f}, |grad| = {np.linalg.norm(grad):.6f}")

        # Gradient ascent
        params = params + lr * grad

        # Adaptive learning rate
        if val < prev_val:
            lr *= 0.5
        prev_val = val

    if val > best_val:
        best_val = val
        best_params = params.copy()

print(f"\nBest found: max eig(P^T R P) = {best_val:.8f}")

# More aggressive search: start from configs near identity
print("\n\nAggressive search near identity:")
for trial in range(5):
    params = np.random.randn(n_params) * 0.1  # Near identity
    lr = 0.05
    prev_val = -np.inf

    for step in range(200):
        val, grad = objective_and_gradient(params)

        if step % 50 == 0 or step == 199:
            print(f"  Trial {trial}, step {step}: max eig(P^T R P) = {val:.8f}, |grad| = {np.linalg.norm(grad):.6f}")

        params = params + lr * grad
        if val < prev_val:
            lr *= 0.7
        prev_val = val

    if val > best_val:
        best_val = val
        best_params = params.copy()

print(f"\nOverall best: max eig(P^T R P) = {best_val:.8f}")

# =============================================================================
# Part 2: Single-link extremal configs
# =============================================================================

print("\n" + "="*80)
print("Part 2: Single non-tree link extremal analysis")
print("="*80)

# Set only ONE non-tree link to non-identity, all others to I
# Find which single link gives the worst (least negative) P^T R P eigenvalue

for e_idx, e in enumerate(non_tree_edges[:15]):  # First 15
    worst_val = -np.inf
    for _ in range(50):
        Q = [np.eye(2, dtype=complex)] * N_edges
        Q[e] = random_su2()
        M_Q = compute_M_matrix_fast(Q)
        R_Q = M_Q - M_I
        PtRP = P.T @ R_Q @ P
        eig_max = np.linalg.eigvalsh(PtRP)[-1]
        if eig_max > worst_val:
            worst_val = eig_max
    # Also try Q[e] = -I (antipodal)
    Q = [np.eye(2, dtype=complex)] * N_edges
    Q[e] = -np.eye(2, dtype=complex)
    M_Q = compute_M_matrix_fast(Q)
    R_Q = M_Q - M_I
    PtRP = P.T @ R_Q @ P
    eig_antipodal = np.linalg.eigvalsh(PtRP)[-1]
    worst_val = max(worst_val, eig_antipodal)

    x_v = index_to_vertex(e % N_vertices)
    mu_v = e // N_vertices
    print(f"  Edge {e} (vertex {x_v}, dir {mu_v}): worst single-link eig = {worst_val:.8f}")

# =============================================================================
# Part 3: Check if per-plaquette-type negativity holds for many configs
# =============================================================================

print("\n" + "="*80)
print("Part 3: Per-plaquette-type P^T R_k P negativity check")
print("="*80)

n_configs = 50
violations_by_type = defaultdict(int)
max_eig_by_type = defaultdict(lambda: -np.inf)

for trial in range(n_configs):
    Q = [np.eye(2, dtype=complex)] * N_edges
    for e in non_tree_edges:
        Q[e] = random_su2()

    for k in sorted(plaq_by_ntree.keys()):
        PtRP_k = np.zeros((P.shape[1], P.shape[1]))
        for sq_idx in plaq_by_ntree[k]:
            e1, e2, e3, e4 = plaquettes[sq_idx]
            # Compute per-plaquette R contribution
            def build_B(QQ, sq_idx):
                e1, e2, e3, e4 = plaquettes[sq_idx]
                R1 = ad_action_matrix(QQ[e1])
                P123inv = QQ[e1] @ QQ[e2] @ QQ[e3].conj().T
                R123inv = ad_action_matrix(P123inv)
                U_sq = P123inv @ QQ[e4].conj().T
                R_sq = ad_action_matrix(U_sq)
                dim = N_edges * 3
                B = np.zeros((3, dim))
                edges_list = [e1, e2, e3, e4]
                coeffs = [np.eye(3), R1, -R123inv, -R_sq]
                for i, (ei, Ci) in enumerate(zip(edges_list, coeffs)):
                    B[:, 3*ei:3*ei+3] = Ci
                return B
            B_Q = build_B(Q, sq_idx)
            B_I = build_B(Q_I, sq_idx)
            R_plaq = B_Q.T @ B_Q - B_I.T @ B_I
            PtRP_k += P.T @ R_plaq @ P

        eig_max = np.linalg.eigvalsh(PtRP_k)[-1]
        if eig_max > 1e-10:
            violations_by_type[k] += 1
        if eig_max > max_eig_by_type[k]:
            max_eig_by_type[k] = eig_max

print(f"Tested {n_configs} random tree-gauge configs:")
for k in sorted(plaq_by_ntree.keys()):
    print(f"  {k}-nontree: violations = {violations_by_type[k]}/{n_configs}, max eig = {max_eig_by_type[k]:.8f}")

# =============================================================================
# Part 4: Check per-plaquette-GROUP negativity (by non-tree edge)
# =============================================================================

print("\n" + "="*80)
print("Part 4: Per-non-tree-edge star grouping")
print("="*80)

# Group plaquettes by which non-tree edge they share
edge_plaq_list = defaultdict(list)
for sq_idx, (e1, e2, e3, e4) in enumerate(plaquettes):
    for e in [e1, e2, e3, e4]:
        if e in non_tree_set:
            edge_plaq_list[e].append(sq_idx)

# For a single non-tree edge, compute the "star" contribution to P^T R P
# Check if each star contribution is independently <= 0
Q_test = [np.eye(2, dtype=complex)] * N_edges
for e in non_tree_edges:
    Q_test[e] = random_su2()

print("Star contributions (plaquettes sharing each non-tree edge):")
star_positive = 0
for e_idx, e in enumerate(non_tree_edges[:10]):
    PtRP_star = np.zeros((P.shape[1], P.shape[1]))
    for sq_idx in edge_plaq_list[e]:
        def build_B(QQ, sq_idx):
            e1, e2, e3, e4 = plaquettes[sq_idx]
            R1 = ad_action_matrix(QQ[e1])
            P123inv = QQ[e1] @ QQ[e2] @ QQ[e3].conj().T
            R123inv = ad_action_matrix(P123inv)
            U_sq = P123inv @ QQ[e4].conj().T
            R_sq = ad_action_matrix(U_sq)
            dim = N_edges * 3
            B = np.zeros((3, dim))
            edges_list = [e1, e2, e3, e4]
            coeffs = [np.eye(3), R1, -R123inv, -R_sq]
            for i, (ei, Ci) in enumerate(zip(edges_list, coeffs)):
                B[:, 3*ei:3*ei+3] = Ci
            return B
        B_Q = build_B(Q_test, sq_idx)
        B_I = build_B(Q_I, sq_idx)
        R_plaq = B_Q.T @ B_Q - B_I.T @ B_I
        PtRP_star += P.T @ R_plaq @ P

    eigs_star = np.linalg.eigvalsh(PtRP_star)
    x_v = index_to_vertex(e % N_vertices)
    mu_v = e // N_vertices
    print(f"  Edge {e} ({x_v}, dir {mu_v}): max eig = {eigs_star[-1]:.6f}, min eig = {eigs_star[0]:.6f}")
    if eigs_star[-1] > 1e-10:
        star_positive += 1

print(f"\nStars with positive eigenvalue: {star_positive}/{min(10, len(non_tree_edges))}")

# =============================================================================
# Part 5: Tight bound search -- specific adversarial configs
# =============================================================================

print("\n" + "="*80)
print("Part 5: Adversarial configs (all non-tree links equal)")
print("="*80)

# Try: all non-tree links set to the same SU(2) element
for _ in range(20):
    U = random_su2()
    Q = [np.eye(2, dtype=complex)] * N_edges
    for e in non_tree_edges:
        Q[e] = U
    M_Q = compute_M_matrix_fast(Q)
    R_Q = M_Q - M_I
    PtRP = P.T @ R_Q @ P
    eig_max = np.linalg.eigvalsh(PtRP)[-1]
    # Compute trace of plaquette holonomy
    W = 0
    for sq_idx in range(N_plaquettes):
        e1, e2, e3, e4 = plaquettes[sq_idx]
        U_sq = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        W += (1 - np.trace(U_sq).real / 2)
    print(f"  max eig(P^T R P) = {eig_max:.8f}, W = {W:.4f}")

# Try: antipodal (-I) on all non-tree links
print("\nAll non-tree = -I:")
Q = [np.eye(2, dtype=complex)] * N_edges
for e in non_tree_edges:
    Q[e] = -np.eye(2, dtype=complex)
M_Q = compute_M_matrix_fast(Q)
R_Q = M_Q - M_I
PtRP = P.T @ R_Q @ P
eig_max = np.linalg.eigvalsh(PtRP)[-1]
print(f"  max eig(P^T R P) = {eig_max:.8f}")
print(f"  lambda_max(M(Q)) = {np.linalg.eigvalsh(M_Q)[-1]:.8f}")

# Try: all non-tree = i*sigma_1
print("\nAll non-tree = i*sigma_1:")
Q = [np.eye(2, dtype=complex)] * N_edges
for e in non_tree_edges:
    Q[e] = 1j * sigma[0]
M_Q = compute_M_matrix_fast(Q)
R_Q = M_Q - M_I
PtRP = P.T @ R_Q @ P
eig_max = np.linalg.eigvalsh(PtRP)[-1]
print(f"  max eig(P^T R P) = {eig_max:.8f}")
print(f"  lambda_max(M(Q)) = {np.linalg.eigvalsh(M_Q)[-1]:.8f}")

# Try: all non-tree = exp(pi/2 * sigma_1)
print("\nAll non-tree = exp(i*pi/2 * T_1):")
Q = [np.eye(2, dtype=complex)] * N_edges
theta = np.pi/2
for e in non_tree_edges:
    Q[e] = su2_exp(np.array([theta, 0, 0]))
M_Q = compute_M_matrix_fast(Q)
R_Q = M_Q - M_I
PtRP = P.T @ R_Q @ P
eig_max = np.linalg.eigvalsh(PtRP)[-1]
print(f"  max eig(P^T R P) = {eig_max:.8f}")
print(f"  lambda_max(M(Q)) = {np.linalg.eigvalsh(M_Q)[-1]:.8f}")
