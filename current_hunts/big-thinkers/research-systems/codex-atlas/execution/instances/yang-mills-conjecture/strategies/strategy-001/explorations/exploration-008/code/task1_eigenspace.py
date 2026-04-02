"""
Task 1: Characterize the full 9D top eigenspace of M(I) and test
whether lambda_max(M(Q)) <= 16 for all directions in P.

Key definitions:
- L=2, d=4, SU(2) gauge group (adjoint = SO(3))
- M(Q) is a 192x192 matrix: v^T M(Q) v = sum_plaquettes |B_sq(Q,v)|^2
- At Q=I, the top eigenvalue is 16 with multiplicity 9
- The 9D eigenspace P consists of modes v_{x,mu} = (-1)^{|x|} s_mu e_a
  where s perp (1,1,1,1) and e_a is a color basis vector
"""

import numpy as np
from itertools import product

np.random.seed(42)

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

edge_index = {}
for x_idx in range(N_vertices):
    for mu in range(d):
        edge_index[(x_idx, mu)] = x_idx * d + mu

# Plaquettes: (e1, e2, e3, e4, x_idx, mu, nu)
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

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def compute_full_M(Q_edges):
    M = np.zeros((N_dim, N_dim))
    for plaq in plaquettes:
        e1, e2, e3, e4, x_idx, mu, nu = plaq
        Q1, Q2, Q3, Q4 = Q_edges[e1], Q_edges[e2], Q_edges[e3], Q_edges[e4]
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
# Part A: Build and verify the 9D eigenspace at Q=I
# ============================================================

print("=" * 70)
print("PART A: Eigenspace of M(I)")
print("=" * 70)

Q_id = [np.eye(3)] * N_edges
M_id = compute_full_M(Q_id)

eigs_id, vecs_id = np.linalg.eigh(M_id)
print(f"Distinct eigenvalues (rounded to 2 decimals):")
unique_eigs = np.unique(np.round(eigs_id, 2))
for ue in unique_eigs:
    count = np.sum(np.abs(eigs_id - ue) < 0.01)
    print(f"  {ue:.4f}: multiplicity {count}")

# Top eigenspace: eigenvalue = 16
top_mask = np.abs(eigs_id - 16.0) < 0.01
top_count = np.sum(top_mask)
print(f"\nTop eigenspace dimension: {top_count} (should be 9)")

# Extract basis of top eigenspace
P_basis = vecs_id[:, top_mask]  # 192 x 9

# ============================================================
# Part B: Verify our analytical basis matches
# ============================================================

print("\n" + "=" * 70)
print("PART B: Verify analytical basis for P")
print("=" * 70)

# Spatial modes perpendicular to (1,1,1,1)/2
# s1 = (1,-1,0,0)/sqrt(2), s2 = (1,1,-2,0)/sqrt(6), s3 = (1,1,1,-3)/sqrt(12)
s_modes = np.array([
    [1, -1, 0, 0],
    [1, 1, -2, 0],
    [1, 1, 1, -3]
], dtype=float)
for i in range(3):
    s_modes[i] /= np.linalg.norm(s_modes[i])

color_basis = np.eye(3)

# Build 9 basis vectors of P analytically
P_analytical = np.zeros((N_dim, 9))
idx = 0
for s_i in range(3):
    s = s_modes[s_i]
    for a in range(3):
        e_a = color_basis[a]
        v = np.zeros(N_dim)
        for x_idx in range(N_vertices):
            x = vertices[x_idx]
            sign_x = (-1) ** sum(x)
            for mu in range(d):
                e = edge_index[(x_idx, mu)]
                v[3*e : 3*e+3] = sign_x * s[mu] * e_a
        P_analytical[:, idx] = v
        idx += 1

# Verify these are eigenvectors of M(I) with eigenvalue 16
print("Checking analytical basis vectors are eigenvectors with eigenvalue 16:")
for j in range(9):
    v = P_analytical[:, j]
    Mv = M_id @ v
    ratio = np.dot(Mv, v) / np.dot(v, v)
    residual = np.linalg.norm(Mv - 16 * v)
    print(f"  v[{j}]: Rayleigh quotient = {ratio:.6f}, |Mv - 16v| = {residual:.2e}")

# Verify analytical basis spans the same space as numerical top eigenspace
# Project P_analytical columns onto numerical P_basis
overlaps = P_analytical.T @ P_basis  # 9x9
sing_vals = np.linalg.svd(overlaps, compute_uv=False)
print(f"\nSingular values of overlap matrix: {np.sort(sing_vals)[::-1]}")
print(f"All > 0.1 (i.e., spans same space): {np.all(sing_vals > 0.1)}")

# Also check: is the uniform-color staggered mode IN the eigenspace?
# v_{x,mu} = (-1)^{|x|+mu} n = (-1)^{|x|} (-1)^mu n
# s_mu = (-1)^mu = (1, -1, 1, -1)
s_stag = np.array([1, -1, 1, -1], dtype=float)
# Check: s_stag perp (1,1,1,1)?
print(f"\ns_stag = {s_stag}")
print(f"s_stag . (1,1,1,1) = {np.dot(s_stag, np.ones(4))}")
# Express s_stag in terms of s1, s2, s3
s_stag_norm = s_stag / np.linalg.norm(s_stag)
coeffs = s_modes @ s_stag_norm
print(f"s_stag/|s_stag| in s-basis: {coeffs}")
print(f"Reconstruction: {coeffs @ s_modes} (should be {s_stag_norm})")

# ============================================================
# Part C: Test v^T M(Q) v <= 16|v|^2 for general modes in P
# ============================================================

print("\n" + "=" * 70)
print("PART C: Test Rayleigh quotient for general modes in P")
print("=" * 70)

N_tests = 200
max_rayleigh = 0
violations = 0

# Test for each analytical basis vector AND random superpositions
for trial in range(N_tests):
    Q_rand = [random_so3() for _ in range(N_edges)]
    M_full = compute_full_M(Q_rand)

    # Test all 9 basis vectors
    for j in range(9):
        v = P_analytical[:, j]
        rq = v @ M_full @ v / np.dot(v, v)
        max_rayleigh = max(max_rayleigh, rq)
        if rq > 16 + 1e-10:
            violations += 1

    # Test 10 random superpositions in the 9D space
    for _ in range(10):
        alpha = np.random.randn(9)
        alpha /= np.linalg.norm(alpha)
        w = P_analytical @ alpha
        rq = w @ M_full @ w / np.dot(w, w)
        max_rayleigh = max(max_rayleigh, rq)
        if rq > 16 + 1e-10:
            violations += 1

    if trial < 5:
        # Print restricted eigenvalues
        M_restricted = P_analytical.T @ M_full @ P_analytical
        eigs_r = np.linalg.eigvalsh(M_restricted)
        norm_mat = P_analytical.T @ P_analytical
        gen_eigs = np.linalg.eigvalsh(np.linalg.solve(norm_mat, M_restricted))
        print(f"  Trial {trial}: max generalized eigenvalue = {gen_eigs[-1]:.6f}")

print(f"\nResults over {N_tests} configs x (9 basis + 10 random) directions:")
print(f"  Max Rayleigh quotient: {max_rayleigh:.6f}")
print(f"  Violations (> 16): {violations}")

# ============================================================
# Part D: Compute restricted 9x9 matrix and its max eigenvalue
# ============================================================

print("\n" + "=" * 70)
print("PART D: Max eigenvalue of restricted matrix P^T M(Q) P / gram matrix")
print("=" * 70)

# Orthonormalize P_analytical first
P_orth, _ = np.linalg.qr(P_analytical)
P_orth = P_orth[:, :9]  # 192 x 9, orthonormal

# Verify orthonormality
gram = P_orth.T @ P_orth
print(f"Gram matrix diagonal: {np.diag(gram)[:3]} (should be 1)")
print(f"Max off-diagonal: {np.max(np.abs(gram - np.eye(9))):.2e}")

max_restricted_eig = 0
min_restricted_eig = float('inf')
max_R_eig = -float('inf')

for trial in range(500):
    Q_rand = [random_so3() for _ in range(N_edges)]
    M_full = compute_full_M(Q_rand)

    # Restricted matrix
    M_r = P_orth.T @ M_full @ P_orth  # 9x9
    eigs_r = np.linalg.eigvalsh(M_r)

    max_restricted_eig = max(max_restricted_eig, eigs_r[-1])
    min_restricted_eig = min(min_restricted_eig, eigs_r[0])

    # R(Q) = M(Q) - M(I), restricted to P
    R_r = M_r - 16 * np.eye(9)
    eigs_R = np.linalg.eigvalsh(R_r)
    max_R_eig = max(max_R_eig, eigs_R[-1])

    if trial < 5:
        print(f"  Trial {trial}: restricted eigs range [{eigs_r[0]:.4f}, {eigs_r[-1]:.4f}], "
              f"max R_restricted eig = {eigs_R[-1]:.6f}")

print(f"\nResults over 500 configs:")
print(f"  Max eigenvalue of P^T M(Q) P: {max_restricted_eig:.6f} (need <= 16)")
print(f"  Min eigenvalue of P^T M(Q) P: {min_restricted_eig:.6f}")
print(f"  Max eigenvalue of P^T R(Q) P: {max_R_eig:.6f} (need <= 0)")
print(f"  Bound holds: {max_restricted_eig <= 16 + 1e-10}")

# ============================================================
# Part E: Adversarial gradient ascent on lambda_max(P^T M(Q) P)
# ============================================================

print("\n" + "=" * 70)
print("PART E: Adversarial gradient ascent on max eigenvalue in P")
print("=" * 70)

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

N_adversarial = 50
best_overall = -float('inf')

for trial in range(N_adversarial):
    Q = [random_so3() for _ in range(N_edges)]

    step_size = 0.01
    for iteration in range(200):
        M_full = compute_full_M(Q)
        M_r = P_orth.T @ M_full @ P_orth
        eigs_r, vecs_r = np.linalg.eigh(M_r)
        current = eigs_r[-1]

        if current > best_overall:
            best_overall = current

        # Top eigenvector in full space
        top_vec_9 = vecs_r[:, -1]
        top_vec_full = P_orth @ top_vec_9

        # Numerical gradient: perturb each link
        grad = []
        for e in range(N_edges):
            g_e = np.zeros(3)
            for k in range(3):
                omega = np.zeros(3)
                omega[k] = 1e-5
                Q_pert = Q.copy()
                Q_pert[e] = so3_exp(omega) @ Q[e]
                M_pert = compute_full_M(Q_pert)
                M_r_pert = P_orth.T @ M_pert @ P_orth
                eig_pert = np.linalg.eigvalsh(M_r_pert)[-1]
                g_e[k] = (eig_pert - current) / 1e-5
            grad.append(g_e)

        # Update
        for e in range(N_edges):
            Q[e] = so3_exp(step_size * grad[e]) @ Q[e]

        if iteration % 50 == 0:
            grad_norm = np.sqrt(sum(np.dot(g, g) for g in grad))
            if trial < 3:
                print(f"  Trial {trial}, iter {iteration}: lambda_max_P = {current:.6f}, grad_norm = {grad_norm:.6f}")

        # Adaptive step
        if iteration > 0 and iteration % 50 == 0:
            step_size *= 0.7

    if trial < 10 or current > 16 - 0.01:
        print(f"  Trial {trial} final: lambda_max_P = {current:.6f}")

print(f"\nBest adversarial lambda_max in P: {best_overall:.6f}")
print(f"Bound holds under adversarial attack: {best_overall <= 16 + 1e-10}")

print("\nDone with Task 1.")
