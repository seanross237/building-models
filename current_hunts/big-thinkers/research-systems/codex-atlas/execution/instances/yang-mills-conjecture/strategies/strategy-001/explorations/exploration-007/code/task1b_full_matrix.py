"""
Task 1b: Build the FULL M(Q) matrix (192x192) and check its eigenvalues.

CRITICAL TEST: If lambda_max of the full M(Q) > 16 for some Q, then the proof
has a gap — it only bounds the staggered mode restriction, not the full matrix.

Convention: v is a vector in R^{192} = R^{64 edges * 3 components}.
v^T M(Q) v = sum_{plaquettes} |B_sq(Q,v)|^2

The staggered mode is v_e = (-1)^{|x|+mu} * n where e = (x, mu).
"""

import numpy as np
from itertools import product

np.random.seed(99999)

d = 4
L = 2
N_vertices = L**d  # 16
N_edges = N_vertices * d  # 64
N_dim = N_edges * 3  # 192

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

# Build edges
edge_index = {}  # (vertex_flat_idx, mu) -> edge_idx
for x_idx in range(N_vertices):
    for mu in range(d):
        edge_index[(x_idx, mu)] = x_idx * d + mu

# Plaquettes
plaquettes = []
for x_idx in range(N_vertices):
    x = vertices[x_idx]
    for mu in range(d):
        for nu in range(mu+1, d):
            x_mu = list(x); x_mu[mu] = (x_mu[mu] + 1) % L
            x_nu = list(x); x_nu[nu] = (x_nu[nu] + 1) % L

            e1 = edge_index[(x_idx, mu)]
            e2 = edge_index[(vertex_index(tuple(x_mu)), nu)]
            e3 = edge_index[(vertex_index(tuple(x_nu)), mu)]
            e4 = edge_index[(x_idx, nu)]

            plaquettes.append((e1, e2, e3, e4, x_idx, mu, nu))

print(f"N_vertices={N_vertices}, N_edges={N_edges}, N_plaquettes={len(plaquettes)}, N_dim={N_dim}")

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def compute_B_sq_vector(Q_edges, plaq, v_full):
    """
    Compute B_sq(Q,v) for a plaquette.

    B_sq = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

    v_full is length N_dim = 192. For edge e, v_e = v_full[3*e : 3*e+3].
    """
    e1, e2, e3, e4, x_idx, mu, nu = plaq

    v1 = v_full[3*e1 : 3*e1+3]
    v2 = v_full[3*e2 : 3*e2+3]
    v3 = v_full[3*e3 : 3*e3+3]
    v4 = v_full[3*e4 : 3*e4+3]

    Q1 = Q_edges[e1]
    Q2 = Q_edges[e2]
    Q3 = Q_edges[e3]
    Q4 = Q_edges[e4]

    U_sq = Q1 @ Q2 @ Q3.T @ Q4.T

    B = v1 + Q1 @ v2 - (Q1 @ Q2 @ Q3.T) @ v3 - U_sq @ v4
    return B

def compute_full_M(Q_edges):
    """
    Build the full N_dim x N_dim matrix M(Q) such that
    v^T M(Q) v = sum_p |B_sq(Q,v)|^2 for all v.

    We do this column-by-column: M[:,j] = sum_p B_sq(Q, e_j) * B_sq(Q, e_j) contributions.
    More precisely: M = sum_p A_p^T A_p where A_p is the 3 x N_dim matrix with A_p @ v = B_sq(Q,v).
    """
    M = np.zeros((N_dim, N_dim))

    for plaq in plaquettes:
        e1, e2, e3, e4, x_idx, mu, nu = plaq
        Q1 = Q_edges[e1]
        Q2 = Q_edges[e2]
        Q3 = Q_edges[e3]
        Q4 = Q_edges[e4]
        U_sq = Q1 @ Q2 @ Q3.T @ Q4.T

        # A_p is 3 x N_dim: A_p @ v = B_sq
        # Nonzero blocks: edges e1, e2, e3, e4
        # A_p[:, 3*e1:3*e1+3] = I
        # A_p[:, 3*e2:3*e2+3] = Q1
        # A_p[:, 3*e3:3*e3+3] = -(Q1 Q2 Q3^T)
        # A_p[:, 3*e4:3*e4+3] = -U_sq

        blocks = {
            e1: np.eye(3),
            e2: Q1.copy(),
            e3: -(Q1 @ Q2 @ Q3.T),
            e4: -U_sq.copy()
        }

        # M += A_p^T A_p. Only nonzero blocks: (ei, ej) pairs
        edge_list = [e1, e2, e3, e4]
        for i_idx, ei in enumerate(edge_list):
            Bi = blocks[ei]
            for j_idx, ej in enumerate(edge_list):
                Bj = blocks[ej]
                M[3*ei:3*ei+3, 3*ej:3*ej+3] += Bi.T @ Bj

    return M

def staggered_mode(n):
    """Build the staggered mode vector v in R^{N_dim} from n in R^3."""
    v = np.zeros(N_dim)
    for x_idx in range(N_vertices):
        x = vertices[x_idx]
        for mu in range(d):
            e = edge_index[(x_idx, mu)]
            sign = (-1) ** (sum(x) + mu)
            v[3*e : 3*e+3] = sign * n
    return v

# ============================================================
# Test 1: Identity configuration
# ============================================================

print("\n" + "=" * 70)
print("TEST 1: Full M(Q) at identity")
print("=" * 70)

Q_id = [np.eye(3)] * N_edges
M_full_id = compute_full_M(Q_id)
eigs_id = np.sort(np.linalg.eigvalsh(M_full_id))
print(f"  Top 10 eigenvalues: {eigs_id[-10:]}")
print(f"  Bottom 5 eigenvalues: {eigs_id[:5]}")
print(f"  lambda_max = {eigs_id[-1]:.6f}")
print(f"  Number of eigenvalues > 16 + 1e-10: {np.sum(eigs_id > 16 + 1e-10)}")

# Check staggered mode
n_test = np.array([1., 0., 0.])
v_stag = staggered_mode(n_test)
print(f"  |v_stag|^2 = {np.dot(v_stag, v_stag):.4f} (should be {N_edges}={N_edges})")
print(f"  v^T M v / |v|^2 = {v_stag @ M_full_id @ v_stag / np.dot(v_stag, v_stag):.6f}")

# ============================================================
# Test 2: Random configs - check full matrix eigenvalues
# ============================================================

print("\n" + "=" * 70)
print("TEST 2: Full M(Q) for random configs")
print("=" * 70)

N_tests = 200
max_full_lam = 0
full_violations = 0
stag_violations = 0

for trial in range(N_tests):
    Q_rand = [random_so3() for _ in range(N_edges)]
    M_full = compute_full_M(Q_rand)
    eigs = np.linalg.eigvalsh(M_full)
    lam_max = eigs[-1]
    max_full_lam = max(max_full_lam, lam_max)

    if lam_max > 16 + 1e-10:
        full_violations += 1

    # Also check staggered mode
    n = np.random.randn(3); n /= np.linalg.norm(n)
    v = staggered_mode(n)
    rayleigh = v @ M_full @ v / np.dot(v, v)
    if rayleigh > 16 + 1e-10:
        stag_violations += 1

    if trial < 5 or lam_max > 16:
        print(f"  Trial {trial}: lambda_max(full) = {lam_max:.6f}, "
              f"stag Rayleigh = {rayleigh:.6f}")

print(f"\n  Results over {N_tests} random configs:")
print(f"    Max lambda_max(full M): {max_full_lam:.6f}")
print(f"    Full matrix violations (> 16): {full_violations}")
print(f"    Staggered mode violations (> 16): {stag_violations}")

if full_violations > 0 and stag_violations == 0:
    print("\n  *** CRITICAL: Full matrix has eigenvalues > 16 but staggered mode doesn't!")
    print("  *** The proof only covers the staggered mode, not the full conjecture!")

# ============================================================
# Test 3: Find the top eigenvector - is it staggered?
# ============================================================

print("\n" + "=" * 70)
print("TEST 3: Nature of top eigenvector at identity")
print("=" * 70)

eigs_full, vecs_full = np.linalg.eigh(M_full_id)
top_vec = vecs_full[:, -1]

# Project onto staggered subspace
# Staggered subspace is spanned by staggered_mode(e1), staggered_mode(e2), staggered_mode(e3)
S = np.zeros((N_dim, 3))
for i in range(3):
    e = np.zeros(3); e[i] = 1.0
    S[:, i] = staggered_mode(e)
S_orth, _ = np.linalg.qr(S)  # orthonormalize

proj = S_orth @ (S_orth.T @ top_vec)
proj_norm = np.linalg.norm(proj)
print(f"  Top eigenvector projection onto staggered subspace: {proj_norm:.6f}")
print(f"  (1.0 = fully staggered, 0.0 = orthogonal to staggered)")

# Count eigenvalue multiplicities at identity
unique_eigs = np.unique(np.round(eigs_full, 4))
print(f"  Distinct eigenvalue values (rounded to 4 decimals): {unique_eigs}")
for ue in unique_eigs:
    count = np.sum(np.abs(eigs_full - ue) < 0.01)
    print(f"    {ue:.4f}: multiplicity {count}")

print("\nDone.")
