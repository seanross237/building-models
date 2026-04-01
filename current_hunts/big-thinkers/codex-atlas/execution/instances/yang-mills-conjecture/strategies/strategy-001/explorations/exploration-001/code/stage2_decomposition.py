"""
Stage 2: Decomposition analysis for Maximal Tree Gauge
Investigate:
1. What the top eigenspace P of M(I) actually looks like
2. Classify plaquettes by number of non-tree links
3. Per-plaquette contributions to R(Q) in tree gauge
4. Algebraic structure of P^T R(Q) P
"""

import numpy as np
from collections import defaultdict
import itertools

np.random.seed(42)

# =============================================================================
# Copy lattice setup from stage1 (self-contained)
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

def edge_info(e):
    """Return (vertex_coords, direction_mu) for edge e."""
    mu = e // N_vertices
    v_start = e % N_vertices
    x = index_to_vertex(v_start)
    return x, mu

# Plaquettes
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

# Spanning tree
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
tree_edges_sorted = sorted(tree_edges)

print(f"Tree edges ({len(tree_edges_sorted)}): {tree_edges_sorted}")
print(f"Non-tree edges ({len(non_tree_edges)}): {non_tree_edges}")

# Print tree edge info
print("\nTree edge details:")
for e in tree_edges_sorted:
    x, mu = edge_info(e)
    vs, ve, _ = edge_endpoints(e)
    print(f"  Edge {e}: vertex {x} dir {mu} ({vs} -> {ve})")

# =============================================================================
# Part 1: Classify plaquettes by number of non-tree links
# =============================================================================

print("\n" + "="*80)
print("Part 1: Plaquette classification by non-tree link count")
print("="*80)

non_tree_set = set(non_tree_edges)
plaq_by_ntree = defaultdict(list)

for sq_idx, (e1, e2, e3, e4) in enumerate(plaquettes):
    n_nontree = sum(1 for e in [e1, e2, e3, e4] if e in non_tree_set)
    plaq_by_ntree[n_nontree].append(sq_idx)

print("\nDistribution of plaquettes by number of non-tree links:")
for k in sorted(plaq_by_ntree.keys()):
    print(f"  {k} non-tree links: {len(plaq_by_ntree[k])} plaquettes")
    if len(plaq_by_ntree[k]) <= 10:
        for sq_idx in plaq_by_ntree[k]:
            e1, e2, e3, e4 = plaquettes[sq_idx]
            nt_flags = ['*' if e in non_tree_set else '.' for e in [e1, e2, e3, e4]]
            x = index_to_vertex(e1 % N_vertices)
            mu_val = e1 // N_vertices
            nu_candidates = [e2 // N_vertices]  # direction of e2
            print(f"    sq {sq_idx}: edges ({e1},{e2},{e3},{e4}), non-tree pattern {''.join(nt_flags)}")

# =============================================================================
# Part 2: Investigate top eigenspace of M(I)
# =============================================================================

print("\n" + "="*80)
print("Part 2: Top eigenspace of M(I)")
print("="*80)

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
        edges = [e1, e2, e3, e4]
        coeffs = [np.eye(3), R1, -R123inv, -R_sq]
        for i, (ei, Ci) in enumerate(zip(edges, coeffs)):
            for j, (ej, Cj) in enumerate(zip(edges, coeffs)):
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Ci.T @ Cj
    return M

Q_I = [np.eye(2, dtype=complex)] * N_edges
M_I = compute_M_matrix_fast(Q_I)

eigenvalues_I, eigenvectors_I = np.linalg.eigh(M_I)

# Examine eigenvalue spectrum
unique_eigs = []
prev = None
for ev in sorted(eigenvalues_I):
    if prev is None or abs(ev - prev) > 0.01:
        unique_eigs.append((ev, 1))
    else:
        unique_eigs[-1] = (unique_eigs[-1][0], unique_eigs[-1][1] + 1)
    prev = ev

print("\nFull eigenvalue spectrum of M(I):")
for ev, mult in unique_eigs:
    print(f"  eigenvalue {ev:8.4f}, multiplicity {mult}")

# Top eigenspace
top_mask = np.abs(eigenvalues_I - 16.0) < 1e-6
P = eigenvectors_I[:, top_mask]
print(f"\nTop eigenspace P: {P.shape[1]} dimensions")

# Analyze the structure of top eigenvectors
# Each eigenvector is in R^{192} = R^{64*3}
# Let's see which edges have nonzero components

print("\nAnalyzing top eigenvector structure:")
for k in range(min(P.shape[1], 3)):
    v = P[:, k]
    print(f"\n  Eigenvector {k}:")
    # Find edges with significant amplitude
    for e in range(N_edges):
        amp = np.linalg.norm(v[3*e:3*e+3])
        if amp > 0.01:
            x, mu = edge_info(e)
            is_tree = "TREE" if e in tree_edges else "cotree"
            print(f"    Edge {e} (vertex {x}, dir {mu}, {is_tree}): components = {v[3*e:3*e+3]}, |amp| = {amp:.6f}")

# Let's try different staggered mode combinations
# The modes might be direction-mixed staggered modes
print("\n\nChecking direction-mixed staggered modes:")
# Mode: v_{x,mu,a} = (-1)^{|x|} * c_mu * delta_{a,a0}
# where c_mu are some direction-dependent signs

for a0 in range(3):
    # Try all 2^4 sign patterns for the 4 directions
    best_val = -np.inf
    best_signs = None
    for signs_bits in range(16):
        c = np.array([(signs_bits >> mu) & 1 for mu in range(d)]) * 2 - 1  # +1 or -1
        v = np.zeros(N_edges * 3)
        for vert in range(N_vertices):
            x = index_to_vertex(vert)
            sign_x = (-1) ** sum(x)
            for mu in range(d):
                e = edge_index(list(x), mu)
                v[3*e + a0] = sign_x * c[mu]
        v = v / np.linalg.norm(v)
        Mv = M_I @ v
        lam = v @ Mv
        if lam > best_val:
            best_val = lam
            best_signs = c.copy()
    print(f"  Color a={a0}: best eigenvalue = {best_val:.6f}, best signs = {best_signs}")

# Try also including (-1)^mu factor
print("\nChecking staggered modes with (-1)^mu factor:")
for a0 in range(3):
    for signs_bits in range(16):
        c = np.array([(signs_bits >> mu) & 1 for mu in range(d)]) * 2 - 1
        v = np.zeros(N_edges * 3)
        for vert in range(N_vertices):
            x = index_to_vertex(vert)
            for mu in range(d):
                e = edge_index(list(x), mu)
                sign = (-1) ** (sum(x) + mu)
                v[3*e + a0] = sign * c[mu]
        v = v / np.linalg.norm(v)
        Mv = M_I @ v
        lam = v @ Mv
        if abs(lam - 16.0) < 0.01:
            print(f"  FOUND! Color a={a0}, signs={c}: eigenvalue = {lam:.6f}")

# More general: try v_{x,mu,a} = phi(x) * psi(mu) * delta_{a,a0}
# where phi depends on x and psi depends on mu
# Actually, on the torus (Z/2Z)^4, the Fourier modes are (-1)^{k.x} for k in {0,1}^4
print("\n\nFourier analysis of top eigenvectors:")
for k_idx, k in enumerate(itertools.product([0, 1], repeat=d)):
    for mu in range(d):
        for a0 in range(3):
            v = np.zeros(N_edges * 3)
            for vert in range(N_vertices):
                x = index_to_vertex(vert)
                phase = (-1) ** sum(k[i] * x[i] for i in range(d))
                e = edge_index(list(x), mu)
                v[3*e + a0] = phase
            if np.linalg.norm(v) < 1e-10:
                continue
            v = v / np.linalg.norm(v)
            Mv = M_I @ v
            lam = v @ Mv
            if abs(lam - 16.0) < 0.1:
                print(f"  k={k}, mu={mu}, a={a0}: eigenvalue = {lam:.6f}")

# Try mixed-direction modes
print("\n\nMixed-direction Fourier modes at eigenvalue 16:")
# For each Fourier momentum k and color a, the mode might mix directions
for k in itertools.product([0, 1], repeat=d):
    for a0 in range(3):
        # Build 4 modes (one per direction) with this (k, a0)
        modes = []
        for mu in range(d):
            v = np.zeros(N_edges * 3)
            for vert in range(N_vertices):
                x = index_to_vertex(vert)
                phase = (-1) ** sum(k[i] * x[i] for i in range(d))
                e = edge_index(list(x), mu)
                v[3*e + a0] = phase
            if np.linalg.norm(v) > 1e-10:
                modes.append(v / np.linalg.norm(v))

        if len(modes) == 0:
            continue

        # Compute M(I) restricted to this subspace
        n_modes = len(modes)
        V = np.column_stack(modes)
        M_sub = V.T @ M_I @ V
        sub_eigs = np.linalg.eigvalsh(M_sub)
        if max(sub_eigs) > 15.9:
            sub_eigvals, sub_eigvecs = np.linalg.eigh(M_sub)
            for idx in range(n_modes):
                if abs(sub_eigvals[idx] - 16.0) < 0.1:
                    coeffs = sub_eigvecs[:, idx]
                    print(f"  k={k}, a={a0}: eigenvalue={sub_eigvals[idx]:.6f}, direction mix={coeffs}")

# =============================================================================
# Part 3: Per-plaquette contributions f_sq(Q) in tree gauge
# =============================================================================

print("\n" + "="*80)
print("Part 3: Per-plaquette contributions to R(Q) in tree gauge")
print("="*80)

def compute_per_plaquette_Bsq_norm(Q, sq_idx, v_vec):
    """Compute |B_sq(Q,v)|^2 for a single plaquette."""
    e1, e2, e3, e4 = plaquettes[sq_idx]
    v1 = v_vec[3*e1:3*e1+3]
    v2 = v_vec[3*e2:3*e2+3]
    v3 = v_vec[3*e3:3*e3+3]
    v4 = v_vec[3*e4:3*e4+3]

    R1 = ad_action_matrix(Q[e1])
    P123inv = Q[e1] @ Q[e2] @ Q[e3].conj().T
    R123inv = ad_action_matrix(P123inv)
    U_sq = P123inv @ Q[e4].conj().T
    R_sq = ad_action_matrix(U_sq)

    result = v1 + R1 @ v2 - R123inv @ v3 - R_sq @ v4
    return np.dot(result, result)

# Generate a random config in tree gauge
def random_tree_gauge_config():
    """Generate config with tree links = I, non-tree links random."""
    Q = [np.eye(2, dtype=complex)] * N_edges
    for e in non_tree_edges:
        Q[e] = random_su2()
    return Q

# Pick a top eigenvector
v_top = P[:, 0]  # First top eigenvector

# Compute per-plaquette f_sq = |B_sq(Q,v)|^2 - |B_sq(I,v)|^2 for a random config
Q_rand = random_tree_gauge_config()

f_sq_values = {}
for sq_idx in range(N_plaquettes):
    bsq_Q = compute_per_plaquette_Bsq_norm(Q_rand, sq_idx, v_top)
    bsq_I = compute_per_plaquette_Bsq_norm(Q_I, sq_idx, v_top)
    f_sq_values[sq_idx] = bsq_Q - bsq_I

# Summarize by plaquette type
print("\nPer-plaquette f_sq (= |B_sq(Q,v)|^2 - |B_sq(I,v)|^2) by non-tree count:")
for k in sorted(plaq_by_ntree.keys()):
    vals = [f_sq_values[sq] for sq in plaq_by_ntree[k]]
    if vals:
        print(f"\n  {k} non-tree links ({len(vals)} plaquettes):")
        print(f"    mean = {np.mean(vals):.6f}")
        print(f"    min  = {np.min(vals):.6f}")
        print(f"    max  = {np.max(vals):.6f}")
        print(f"    sum  = {np.sum(vals):.6f}")
        if len(vals) <= 10:
            for sq in plaq_by_ntree[k]:
                print(f"      sq {sq}: f_sq = {f_sq_values[sq]:.8f}")

total_f = sum(f_sq_values.values())
print(f"\nTotal sum of f_sq = {total_f:.8f}")
print(f"v^T R(Q) v = {v_top @ (compute_M_matrix_fast(Q_rand) - M_I) @ v_top:.8f}")

# =============================================================================
# Part 4: In tree gauge, examine which edges appear in plaquette B-formula
# =============================================================================

print("\n" + "="*80)
print("Part 4: Plaquette structure in tree gauge")
print("="*80)

print("\nFor plaquettes with 0 non-tree links (all tree edges):")
for sq_idx in plaq_by_ntree.get(0, []):
    e1, e2, e3, e4 = plaquettes[sq_idx]
    print(f"  sq {sq_idx}: edges ({e1},{e2},{e3},{e4}) -- all tree, so all = I")
    print(f"    B_sq(Q,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4} (independent of Q)")
    print(f"    f_sq = 0 always (B_sq same as at Q=I)")

print(f"\nFor plaquettes with 1 non-tree link:")
for sq_idx in plaq_by_ntree.get(1, [])[:5]:  # Show first 5
    e1, e2, e3, e4 = plaquettes[sq_idx]
    nt = [(i+1, e) for i, e in enumerate([e1,e2,e3,e4]) if e in non_tree_set]
    t = [(i+1, e) for i, e in enumerate([e1,e2,e3,e4]) if e not in non_tree_set]
    print(f"  sq {sq_idx}: edges ({e1},{e2},{e3},{e4})")
    print(f"    Non-tree: position {nt[0][0]}, edge {nt[0][1]}")
    print(f"    Tree (=I): positions {[x[0] for x in t]}")

print(f"\nFor plaquettes with 2 non-tree links:")
for sq_idx in plaq_by_ntree.get(2, [])[:5]:
    e1, e2, e3, e4 = plaquettes[sq_idx]
    nt = [(i+1, e) for i, e in enumerate([e1,e2,e3,e4]) if e in non_tree_set]
    print(f"  sq {sq_idx}: edges ({e1},{e2},{e3},{e4})")
    print(f"    Non-tree: positions {[(x[0], x[1]) for x in nt]}")

# Count which positions (1-4) the non-tree link appears in for 1-nontree plaquettes
if 1 in plaq_by_ntree:
    pos_count = defaultdict(int)
    for sq_idx in plaq_by_ntree[1]:
        e1, e2, e3, e4 = plaquettes[sq_idx]
        for i, e in enumerate([e1, e2, e3, e4]):
            if e in non_tree_set:
                pos_count[i+1] += 1
    print(f"\n1-nontree plaquettes: non-tree link position distribution: {dict(pos_count)}")

# =============================================================================
# Part 5: Algebraic form for 1-nontree plaquettes
# =============================================================================

print("\n" + "="*80)
print("Part 5: Algebraic simplification for 1-nontree plaquettes")
print("="*80)

# In tree gauge, all tree links = I. So Ad_{Q_e} = I for tree links.
# For a plaquette with edges (e1, e2, e3, e4) where only e_j is non-tree:
#
# Case: non-tree link at position 1 (e1):
#   B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1} * I * I}(v_{e3}) - Ad_{Q_{e1} * I * I * I}(v_{e4})
#   = v_{e1} + R(Q_{e1}) v_{e2} - R(Q_{e1}) v_{e3} - R(Q_{e1}) v_{e4}
#   (since Q_{e2}=I, Q_{e3}=I means P_{123inv} = Q_{e1}*I*I = Q_{e1}, U_sq = Q_{e1}*I = Q_{e1})
#   Wait, need to be more careful about the formula.
#
# B_sq formula: v_{e1} + Ad(Q_{e1}) v_{e2} - Ad(Q_{e1} Q_{e2} Q_{e3}^{-1}) v_{e3} - Ad(Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1}) v_{e4}

print("Algebraic forms for each position of the single non-tree link:")
print("(In tree gauge: tree links = I, so Ad_I = identity)")
print()

print("Position 1 (e1 = non-tree, e2,e3,e4 = tree = I):")
print("  Partial holonomies: Q_{e1}, Q_{e1}*I*I^{-1} = Q_{e1}, Q_{e1}*I*I^{-1}*I^{-1} = Q_{e1}")
print("  B_sq = v_{e1} + Ad(Q_{e1}) v_{e2} - Ad(Q_{e1}) v_{e3} - Ad(Q_{e1}) v_{e4}")
print("  B_sq(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4}")
print("  diff = (Ad(Q)-I)(v_{e2} - v_{e3} - v_{e4})")
print()

print("Position 2 (e2 = non-tree, e1,e3,e4 = tree = I):")
print("  Partial holonomies: I, I*Q_{e2}, I*Q_{e2}*I^{-1} = Q_{e2}, Q_{e2}*I^{-1} = Q_{e2}")
print("  B_sq = v_{e1} + Ad(I) v_{e2} - Ad(Q_{e2}) v_{e3} - Ad(Q_{e2}) v_{e4}")
print("  = v_{e1} + v_{e2} - Ad(Q_{e2}) v_{e3} - Ad(Q_{e2}) v_{e4}")
print("  B_sq(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4}")
print("  diff = -(Ad(Q_{e2})-I)(v_{e3} + v_{e4})")
print()

print("Position 3 (e3 = non-tree, e1,e2,e4 = tree = I):")
print("  Partial holonomies: I, I*I=I, I*I*Q_{e3}^{-1} = Q_{e3}^{-1}, Q_{e3}^{-1}*I^{-1} = Q_{e3}^{-1}")
print("  B_sq = v_{e1} + v_{e2} - Ad(Q_{e3}^{-1}) v_{e3} - Ad(Q_{e3}^{-1}) v_{e4}")
print("  B_sq(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4}")
print("  diff = -(Ad(Q_{e3}^{-1})-I)(v_{e3} + v_{e4})")
print()

print("Position 4 (e4 = non-tree, e1,e2,e3 = tree = I):")
print("  Partial holonomies: I, I, I, I*I*I*Q_{e4}^{-1} = Q_{e4}^{-1}")
print("  Actually: U_sq = I*I*I^{-1}*Q_{e4}^{-1} = Q_{e4}^{-1}")
print("  B_sq = v_{e1} + v_{e2} - v_{e3} - Ad(Q_{e4}^{-1}) v_{e4}")
print("  B_sq(I,v) = v_{e1} + v_{e2} - v_{e3} - v_{e4}")
print("  diff = -(Ad(Q_{e4}^{-1})-I) v_{e4}")

# =============================================================================
# Part 6: Verify the algebraic forms numerically
# =============================================================================

print("\n" + "="*80)
print("Part 6: Numerical verification of algebraic forms")
print("="*80)

def compute_Bsq_explicit(Q, sq_idx, v_vec):
    """Compute B_sq(Q,v) as a 3-vector."""
    e1, e2, e3, e4 = plaquettes[sq_idx]
    v1 = v_vec[3*e1:3*e1+3]
    v2 = v_vec[3*e2:3*e2+3]
    v3 = v_vec[3*e3:3*e3+3]
    v4 = v_vec[3*e4:3*e4+3]

    R1 = ad_action_matrix(Q[e1])
    P123inv = Q[e1] @ Q[e2] @ Q[e3].conj().T
    R123inv = ad_action_matrix(P123inv)
    U_sq = P123inv @ Q[e4].conj().T
    R_sq = ad_action_matrix(U_sq)

    return v1 + R1 @ v2 - R123inv @ v3 - R_sq @ v4

# Test with a specific 1-nontree plaquette
if 1 in plaq_by_ntree and len(plaq_by_ntree[1]) > 0:
    Q_test = random_tree_gauge_config()
    v_test = np.random.randn(N_edges * 3)

    for sq_idx in plaq_by_ntree[1][:4]:
        e1, e2, e3, e4 = plaquettes[sq_idx]
        edges = [e1, e2, e3, e4]

        # Find which position is non-tree
        nt_pos = [i for i in range(4) if edges[i] in non_tree_set][0]
        nt_edge = edges[nt_pos]

        # Compute B_sq numerically
        B_num = compute_Bsq_explicit(Q_test, sq_idx, v_test)
        B_I = compute_Bsq_explicit(Q_I, sq_idx, v_test)

        # Compute using simplified formula
        v1 = v_test[3*e1:3*e1+3]
        v2 = v_test[3*e2:3*e2+3]
        v3 = v_test[3*e3:3*e3+3]
        v4 = v_test[3*e4:3*e4+3]

        Q_nt = Q_test[nt_edge]
        R_nt = ad_action_matrix(Q_nt)
        R_nt_inv = ad_action_matrix(Q_nt.conj().T)
        dR = R_nt - np.eye(3)
        dR_inv = R_nt_inv - np.eye(3)

        if nt_pos == 0:
            B_simplified = B_I + dR @ (v2 - v3 - v4)
        elif nt_pos == 1:
            B_simplified = B_I - dR @ (v3 + v4)
        elif nt_pos == 2:
            B_simplified = B_I - dR_inv @ (v3 + v4)
        elif nt_pos == 3:
            B_simplified = B_I - dR_inv @ v4

        diff = np.linalg.norm(B_num - B_simplified)
        print(f"  sq {sq_idx} (nt_pos={nt_pos+1}): |B_num - B_simplified| = {diff:.2e}")

# =============================================================================
# Part 7: Non-tree edge frequency analysis
# =============================================================================

print("\n" + "="*80)
print("Part 7: Non-tree edge participation in plaquettes")
print("="*80)

# For each non-tree edge, how many plaquettes contain it?
edge_plaq_count = defaultdict(int)
edge_plaq_list = defaultdict(list)
for sq_idx, (e1, e2, e3, e4) in enumerate(plaquettes):
    for e in [e1, e2, e3, e4]:
        if e in non_tree_set:
            edge_plaq_count[e] += 1
            edge_plaq_list[e].append(sq_idx)

print("Non-tree edge participation count (# plaquettes containing each edge):")
count_distribution = defaultdict(int)
for e in non_tree_edges:
    count_distribution[edge_plaq_count[e]] += 1

for k in sorted(count_distribution.keys()):
    print(f"  {k} plaquettes: {count_distribution[k]} non-tree edges")

# Each edge in a d-dimensional torus appears in 2(d-1) plaquettes
print(f"\nExpected: each edge in 2(d-1) = {2*(d-1)} plaquettes")
for e in non_tree_edges[:5]:
    x, mu = edge_info(e)
    print(f"  Edge {e} (vertex {x}, dir {mu}): appears in {edge_plaq_count[e]} plaquettes")

# =============================================================================
# Part 8: Full P^T R(Q) P as sum of per-plaquette contributions
# =============================================================================

print("\n" + "="*80)
print("Part 8: P^T R(Q) P decomposition by plaquette type")
print("="*80)

# Compute P^T R(Q) P decomposed by plaquette non-tree count
Q_test2 = random_tree_gauge_config()
M_Q = compute_M_matrix_fast(Q_test2)
R_Q = M_Q - M_I
PtRP = P.T @ R_Q @ P
print(f"Full P^T R P eigenvalues: {np.sort(np.linalg.eigvalsh(PtRP))}")

# Now decompose M(Q) = sum_sq B_sq^T B_sq into plaquette contributions
# R_sq contribution = B_sq(Q)^T B_sq(Q) - B_sq(I)^T B_sq(I)
def compute_per_plaq_R_matrix(Q, sq_idx):
    """Compute the 192x192 contribution of plaquette sq_idx to R(Q)."""
    dim = N_edges * 3
    # Build B matrices
    e1, e2, e3, e4 = plaquettes[sq_idx]

    def build_B(QQ):
        R1 = ad_action_matrix(QQ[e1])
        P123inv = QQ[e1] @ QQ[e2] @ QQ[e3].conj().T
        R123inv = ad_action_matrix(P123inv)
        U_sq = P123inv @ QQ[e4].conj().T
        R_sq = ad_action_matrix(U_sq)
        edges = [e1, e2, e3, e4]
        coeffs = [np.eye(3), R1, -R123inv, -R_sq]
        B = np.zeros((3, dim))
        for i, (ei, Ci) in enumerate(zip(edges, coeffs)):
            B[:, 3*ei:3*ei+3] = Ci
        return B

    B_Q = build_B(Q)
    B_I = build_B(Q_I)
    return B_Q.T @ B_Q - B_I.T @ B_I

# Accumulate P^T R P by plaquette type
PtRP_by_type = {}
for k in sorted(plaq_by_ntree.keys()):
    PtRP_k = np.zeros((P.shape[1], P.shape[1]))
    for sq_idx in plaq_by_ntree[k]:
        R_sq = compute_per_plaq_R_matrix(Q_test2, sq_idx)
        PtRP_k += P.T @ R_sq @ P
    PtRP_by_type[k] = PtRP_k
    eigs_k = np.linalg.eigvalsh(PtRP_k)
    print(f"\n{k}-nontree plaquettes ({len(plaq_by_ntree[k])} plaqs):")
    print(f"  P^T R_k P eigenvalues: {np.sort(eigs_k)}")
    print(f"  max eigenvalue: {max(eigs_k):.8f}")
    print(f"  trace: {np.trace(PtRP_k):.8f}")

# Verify sum
PtRP_sum = sum(PtRP_by_type.values())
print(f"\nSum of all types vs full P^T R P: max diff = {np.max(np.abs(PtRP_sum - PtRP)):.2e}")
