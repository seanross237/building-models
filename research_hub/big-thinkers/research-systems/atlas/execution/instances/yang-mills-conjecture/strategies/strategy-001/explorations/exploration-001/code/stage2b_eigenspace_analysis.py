"""
Stage 2b: Detailed analysis of the 9-dimensional top eigenspace of M(I)
and the structure of P^T R(Q) P.

Key question: What are the explicit eigenvectors in the top eigenspace?
From Stage 2, we know they all have Fourier momentum k=(1,1,1,1),
meaning v_{x,mu,a} = (-1)^{sum(x)} * c_{mu,a}.

The eigenvalue 16 subspace has dimension 9 = 3 colors * 3 direction modes.
We need to find the 3 independent direction modes.
"""

import numpy as np
from collections import defaultdict

np.random.seed(42)

# Lattice setup (same as before)
sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)

L = 2; d = 4
N_vertices = L**d; N_edges = d * L**d; N_plaquettes = d*(d-1)//2 * L**d

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

Q_I = [np.eye(2, dtype=complex)] * N_edges
M_I = compute_M_matrix_fast(Q_I)
eigenvalues_I, eigenvectors_I = np.linalg.eigh(M_I)
top_mask = np.abs(eigenvalues_I - 16.0) < 1e-6
P = eigenvectors_I[:, top_mask]

# =============================================================================
# Part 1: Explicit construction of top eigenspace
# =============================================================================

print("="*80)
print("Part 1: Explicit top eigenspace construction")
print("="*80)

# At k=(1,1,1,1), the mode has form: v_{x,mu,a} = (-1)^{sum(x)} * c_mu * delta_{a,a0}
# For each color a0, we have 4 modes (one per direction mu).
# M(I) restricted to these 4 modes is a 4x4 matrix.

# Let's compute this 4x4 matrix for color a=0
print("\nM(I) restricted to k=(1,1,1,1) staggered modes, per color:")

for a0 in range(1):  # Color-independent, so just do a=0
    modes_4d = []
    for mu in range(d):
        v = np.zeros(N_edges * 3)
        for vert in range(N_vertices):
            x = index_to_vertex(vert)
            phase = (-1) ** sum(x)
            e = edge_index(list(x), mu)
            v[3*e + a0] = phase
        v = v / np.linalg.norm(v)
        modes_4d.append(v)

    V4 = np.column_stack(modes_4d)
    M_4x4 = V4.T @ M_I @ V4
    print(f"\n  Color a={a0}:")
    print(f"  4x4 matrix:")
    for i in range(4):
        print(f"    [{', '.join(f'{M_4x4[i,j]:8.4f}' for j in range(4))}]")

    eigvals4, eigvecs4 = np.linalg.eigh(M_4x4)
    print(f"  Eigenvalues: {eigvals4}")
    print(f"  Eigenvectors (columns):")
    for i in range(4):
        print(f"    [{', '.join(f'{eigvecs4[i,j]:8.4f}' for j in range(4))}]")

    # The eigenvalue-16 subspace
    mask16 = np.abs(eigvals4 - 16) < 0.01
    n16 = np.sum(mask16)
    print(f"  Eigenvalue 16 has multiplicity {n16} in this 4d subspace")
    V16 = eigvecs4[:, mask16]
    print(f"  Direction vectors in 16-eigenspace:")
    for col in range(V16.shape[1]):
        print(f"    c = {V16[:, col]}")

    # The kernel eigenspace
    mask0 = np.abs(eigvals4) < 0.01
    n0 = np.sum(mask0)
    print(f"  Eigenvalue ~0 has multiplicity {n0} in this 4d subspace")

# =============================================================================
# Part 2: Why 3 not 4? What's the constraint?
# =============================================================================

print("\n" + "="*80)
print("Part 2: Why dimension 3 (not 4) per color?")
print("="*80)

# The 4x4 matrix is 12*I - 4*J where J is the all-ones matrix.
# eigenvalues: 12 - 4*4 = -4 for c=(1,1,1,1)/2, and 12 for c perp (1,1,1,1)... no
# Actually J has eigenvalue 4 on (1,1,1,1)/2 and 0 on orthogonal complement.
# So M_4x4 = 12I - 4J has eigenvalue 12 - 4*4 = -4 on (1,1,1,1), and 12 on complement.
# But we got eigenvalues 0 and 16. Let me reconsider.
# Hmm, the matrix entries are 12 on diagonal and -4 off-diagonal.
# That's 16*I - 4*J. So eigenvalues: 16-4*4=0 on (1,1,1,1)/2, and 16-0=16 on complement.
# Yes: M_4x4 = 16*I - 4*J. The 4x4 all-ones matrix J has eigenvalue 4 on (1,1,1,1)/2
# and 0 on its complement.

print("  M_4x4 = 16*I - 4*J (where J is the all-ones matrix)")
print("  Eigenvalue 16 on {c : sum(c) = 0} (3d subspace)")
print("  Eigenvalue 0 on (1,1,1,1) direction")
print()

# The (1,1,1,1) direction gives eigenvalue 0 (kernel of M(I))
# This makes sense: v_{x,mu,a} = (-1)^{sum(x)} * const for all mu is a gauge mode
# because B_sq(I, v) = v_e1 + v_e2 - v_e3 - v_e4 = 0 when v is constant on the edges
# of the plaquette... actually with staggering it's alternating. Let me think.

print("  Physical interpretation:")
print("  The (1,1,1,1) direction mode v_{x,mu,a} = (-1)^{sum(x)} * delta_a")
print("  has all 4 direction coefficients equal, so B_sq = c*(1+1-1-1) on L=2 torus")
print("  This is in the kernel of M(I), confirmed by eigenvalue 0.")
print()
print("  The top eigenspace requires sum(c_mu) = 0, i.e., 'transverse' staggered modes.")
print("  Dimension: 3 per color x 3 colors = 9 total.")

# =============================================================================
# Part 3: Explicit orthonormal basis for P
# =============================================================================

print("\n" + "="*80)
print("Part 3: Explicit orthonormal basis for P")
print("="*80)

# Direction basis: 3 orthonormal vectors in R^4 perpendicular to (1,1,1,1)
e_dir = np.array([
    [1, -1, 0, 0],
    [1, 1, -2, 0],
    [1, 1, 1, -3],
], dtype=float)
# Gram-Schmidt
for i in range(3):
    for j in range(i):
        e_dir[i] -= np.dot(e_dir[i], e_dir[j]) * e_dir[j]
    e_dir[i] /= np.linalg.norm(e_dir[i])

print("Direction basis (orthogonal to (1,1,1,1)):")
for i in range(3):
    print(f"  d_{i} = {e_dir[i]}")

# Full P basis: 9 vectors, indexed by (direction_idx, color_idx)
P_explicit = np.zeros((N_edges * 3, 9))
for dir_idx in range(3):
    for col_idx in range(3):
        v = np.zeros(N_edges * 3)
        for vert in range(N_vertices):
            x = index_to_vertex(vert)
            phase = (-1) ** sum(x)
            for mu in range(d):
                e = edge_index(list(x), mu)
                v[3*e + col_idx] = phase * e_dir[dir_idx][mu]
        v = v / np.linalg.norm(v)
        P_explicit[:, 3 * dir_idx + col_idx] = v

# Verify these are eigenvectors of M(I) with eigenvalue 16
print("\nVerification:")
for k in range(9):
    Mv = M_I @ P_explicit[:, k]
    lam = P_explicit[:, k] @ Mv
    print(f"  Mode {k} (dir={k//3}, col={k%3}): eigenvalue = {lam:.6f}")

# Check that P_explicit spans the same space as P
# Project P onto P_explicit's column space
PP = P_explicit.T @ P_explicit
print(f"\nP_explicit^T P_explicit (should be identity): max off-diag = {np.max(np.abs(PP - np.eye(9))):.2e}")

overlap = P.T @ P_explicit
# The singular values should all be 1
svds = np.linalg.svd(overlap, compute_uv=False)
print(f"Singular values of P^T P_explicit: {svds}")
print(f"All close to 1: {np.allclose(svds, 1.0, atol=1e-6)}")

# =============================================================================
# Part 4: P^T R(Q) P in explicit basis has BLOCK STRUCTURE
# =============================================================================

print("\n" + "="*80)
print("Part 4: Block structure of P^T R(Q) P")
print("="*80)

# P is 192 x 9 with basis vectors indexed by (dir_idx, col_idx)
# Since M(Q) has SU(2) color structure, and our basis vectors are color-pure,
# P^T R(Q) P might have a block structure.

# For SU(2): Ad_Q is a 3x3 SO(3) matrix acting on colors.
# The staggered modes mix colors only through Ad_Q.
# So P^T M(Q) P should decompose as:
# [P^T M(Q) P]_{(d_i, a), (d_j, b)} = sum_sq F^{sq}_{d_i, d_j} * [Ad matrices]_{a,b}

# Let's test: is P^T R(Q) P = D tensor R_3x3 for some direction matrix D and color matrix R?

def random_su2():
    v = np.random.randn(4)
    v = v / np.linalg.norm(v)
    return v[0] * np.eye(2, dtype=complex) + 1j * sum(v[k+1] * sigma[k] for k in range(3))

from collections import deque
def find_spanning_tree():
    visited = set(); tree_edges = set(); queue = deque([0]); visited.add(0)
    while queue:
        v = queue.popleft(); x = list(index_to_vertex(v))
        for mu in range(d):
            x_next = list(x); x_next[mu] = (x_next[mu] + 1) % L
            v_next = vertex_index(x_next)
            if v_next not in visited:
                visited.add(v_next); tree_edges.add(edge_index(x, mu)); queue.append(v_next)
            x_prev = list(x); x_prev[mu] = (x_prev[mu] - 1) % L
            v_prev = vertex_index(x_prev)
            if v_prev not in visited:
                visited.add(v_prev); tree_edges.add(edge_index(x_prev, mu)); queue.append(v_prev)
    return tree_edges

tree_edges = find_spanning_tree()
non_tree_edges = sorted(set(range(N_edges)) - tree_edges)

# Generate test config
Q_test = [np.eye(2, dtype=complex)] * N_edges
for e in non_tree_edges:
    Q_test[e] = random_su2()

M_Q = compute_M_matrix_fast(Q_test)
R_Q = M_Q - M_I

# Compute P^T R P using explicit basis
PtRP_expl = P_explicit.T @ R_Q @ P_explicit
print("P^T R(Q) P in explicit (dir x color) basis:")
print("  Shape:", PtRP_expl.shape)

# Examine block structure: rows/cols indexed by (dir, color)
# If tensor product: PtRP[3*i+a, 3*j+b] = D[i,j] * C[a,b]
print("\n  Full 9x9 matrix:")
for i in range(9):
    row = [f"{PtRP_expl[i,j]:8.4f}" for j in range(9)]
    print(f"    [{', '.join(row)}]")

# Check if it's a tensor product D_3x3 tensor C_3x3
# Extract 3x3 blocks
print("\n  3x3 direction blocks (each block is color x color):")
for di in range(3):
    for dj in range(3):
        block = PtRP_expl[3*di:3*di+3, 3*dj:3*dj+3]
        print(f"    Block ({di},{dj}): [{block[0,0]:8.4f} {block[0,1]:8.4f} {block[0,2]:8.4f}]")
        print(f"                   [{block[1,0]:8.4f} {block[1,1]:8.4f} {block[1,2]:8.4f}]")
        print(f"                   [{block[2,0]:8.4f} {block[2,1]:8.4f} {block[2,2]:8.4f}]")

# Check if all direction blocks are proportional to the same color matrix
block_00 = PtRP_expl[0:3, 0:3]
print("\n  Checking if blocks are proportional to block(0,0):")
for di in range(3):
    for dj in range(3):
        block = PtRP_expl[3*di:3*di+3, 3*dj:3*dj+3]
        if np.linalg.norm(block_00) > 1e-10:
            # Try to find scalar c such that block = c * block_00
            ratios = block / (block_00 + 1e-20)
            if np.std(ratios[np.abs(block_00) > 0.01]) < 0.1:
                c = np.mean(ratios[np.abs(block_00) > 0.01])
                print(f"    Block ({di},{dj}) ~ {c:.4f} * Block(0,0), residual = {np.linalg.norm(block - c * block_00):.6f}")
            else:
                print(f"    Block ({di},{dj}): NOT proportional to Block(0,0)")

# Alternative: check if PtRP = D kron C
# Use SVD of the reshaped matrix
PtRP_reshaped = PtRP_expl.reshape(3, 3, 3, 3)
# Flatten to (3*3, 3*3) in direction x color ordering
PtRP_flat = PtRP_reshaped.transpose(0, 2, 1, 3).reshape(9, 9)
# If it were D kron C, then PtRP_flat would have rank 1 when viewed as (9,9)
# Actually, let's do it differently. Reshape PtRP as (3,3) x (3,3):
# M_{(i,a),(j,b)} -> T_{(i,j),(a,b)}
T = np.zeros((9, 9))
for i in range(3):
    for j in range(3):
        for a in range(3):
            for b in range(3):
                T[3*i+j, 3*a+b] = PtRP_expl[3*i+a, 3*j+b]

svd_T = np.linalg.svd(T, compute_uv=False)
print(f"\n  SVD of reshaped tensor (should be rank-1 if tensor product): {svd_T}")
rank_ratio = svd_T[1] / svd_T[0] if svd_T[0] > 1e-10 else 0
print(f"  Rank-1 test: sigma_2/sigma_1 = {rank_ratio:.6f}")
if rank_ratio < 0.01:
    print("  >> TENSOR PRODUCT STRUCTURE CONFIRMED!")
else:
    print(f"  >> NOT a pure tensor product (ratio = {rank_ratio:.4f})")

# =============================================================================
# Part 5: Statistics of the color structure
# =============================================================================

print("\n" + "="*80)
print("Part 5: Color structure across multiple configs")
print("="*80)

# For each config, compute the 3x3 color block of P^T R P restricted to dir_0
# If it's always proportional to the same matrix, the color structure is universal
color_blocks = []
for trial in range(20):
    Q_t = [np.eye(2, dtype=complex)] * N_edges
    for e in non_tree_edges:
        Q_t[e] = random_su2()
    M_Qt = compute_M_matrix_fast(Q_t)
    R_Qt = M_Qt - M_I
    PtRP_t = P_explicit.T @ R_Qt @ P_explicit

    # Extract the color block for direction pair (0,0)
    block = PtRP_t[0:3, 0:3]
    # Normalize
    norm = np.linalg.norm(block)
    if norm > 1e-10:
        color_blocks.append(block / norm)

    if trial < 3:
        print(f"  Config {trial}, block(0,0):")
        for row in range(3):
            print(f"    [{block[row,0]:8.5f} {block[row,1]:8.5f} {block[row,2]:8.5f}]")

        # Eigenvalues of this color block
        eigs_c = np.linalg.eigvalsh(block)
        print(f"    Eigenvalues: {eigs_c}")

# Check if color blocks are all proportional to same matrix
if len(color_blocks) >= 2:
    ref = color_blocks[0]
    print("\n  Similarity of normalized color blocks to first config:")
    for i, cb in enumerate(color_blocks):
        diff = np.linalg.norm(cb - ref)
        diff_neg = np.linalg.norm(cb + ref)
        print(f"    Config {i}: |diff| = {min(diff, diff_neg):.6f}")
