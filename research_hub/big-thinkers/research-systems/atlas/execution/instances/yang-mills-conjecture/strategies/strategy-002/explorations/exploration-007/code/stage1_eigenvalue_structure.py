"""
Stage 1: Full eigenvalue structure characterization of M(Q) on L=2, d=4.
Stage 4: Operator norm bound on R(Q) = M(Q) - M(I) restricted to non-staggered subspace.

Key question: Is lambda_max(R|_{non-stag}) <= 4? If so, then
  lambda_max(M(Q)|_{non-stag}) <= 12 + 4 = 16.
"""
import numpy as np
from scipy.linalg import expm
import itertools
import time

np.random.seed(42)

# ============================================================
# LATTICE SETUP: L=2, d=4
# ============================================================
L = 2
d = 4
N_vertices = L**d  # 16
N_edges = d * N_vertices  # 64
N_dim = 3 * N_edges  # 192

def vertex_index(x):
    idx = 0
    for i in range(d):
        idx = idx * L + (x[i] % L)
    return idx

def all_vertices():
    return list(itertools.product(range(L), repeat=d))

def edge_index(x, mu):
    vi = vertex_index(x)
    return vi * d + mu

def neighbor(x, mu, direction=1):
    y = list(x)
    y[mu] = (y[mu] + direction) % L
    return tuple(y)

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def generate_random_gauge():
    Q = {}
    for x in all_vertices():
        for mu in range(d):
            Q[(x, mu)] = random_so3()
    return Q

def holonomy(Q, x, mu, nu):
    x_plus_mu = neighbor(x, mu)
    x_plus_nu = neighbor(x, nu)
    return Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T @ Q[(x, nu)].T

def build_full_M(Q):
    """Build full 192x192 M(Q) = sum_plaq B_plaq^T B_plaq."""
    M = np.zeros((N_dim, N_dim))
    for x in all_vertices():
        for mu in range(d):
            for nu in range(mu+1, d):
                x_plus_mu = neighbor(x, mu)
                x_plus_nu = neighbor(x, nu)

                G1 = np.eye(3)
                G2 = Q[(x, mu)]
                G3 = -(Q[(x, mu)] @ Q[(x_plus_mu, nu)] @ Q[(x_plus_nu, mu)].T)
                G4 = -holonomy(Q, x, mu, nu)

                e1 = (x, mu); e2 = (x_plus_mu, nu)
                e3 = (x_plus_nu, mu); e4 = (x, nu)

                idx1 = 3 * edge_index(e1[0], e1[1])
                idx2 = 3 * edge_index(e2[0], e2[1])
                idx3 = 3 * edge_index(e3[0], e3[1])
                idx4 = 3 * edge_index(e4[0], e4[1])

                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        M[ia:ia+3, ib:ib+3] += Ga.T @ Gb
    return M

def build_staggered_basis():
    """9D staggered subspace: v_{x,mu} = (-1)^{|x|+mu} T_mu, sum T_mu = 0."""
    basis = []
    for a, b in [(0,1), (1,2), (2,3)]:
        for j in range(3):
            T = np.zeros((4, 3))
            T[a, j] = 1.0
            T[b, j] = -1.0
            v = np.zeros(N_dim)
            for x in all_vertices():
                sx = sum(x) % 2
                for mu in range(d):
                    sign = (-1)**(sx + mu)
                    ei = edge_index(x, mu)
                    v[3*ei:3*ei+3] = sign * T[mu]
            basis.append(v)
    P = np.column_stack(basis)
    Q_orth, R = np.linalg.qr(P)
    return Q_orth

def build_momentum_eigenspaces(M_I):
    """Decompose the Q=I eigenspaces by eigenvalue."""
    eigvals, eigvecs = np.linalg.eigh(M_I)

    # Group by eigenvalue
    spaces = {}
    for i in range(N_dim):
        ev = round(eigvals[i])
        if ev not in spaces:
            spaces[ev] = []
        spaces[ev].append(eigvecs[:, i])

    # Convert to orthonormal bases
    projectors = {}
    for ev, vecs in spaces.items():
        P = np.column_stack(vecs)
        projectors[ev] = P

    return projectors

# ============================================================
# Stage 1: Q=I baseline
# ============================================================
print("=" * 70)
print("STAGE 1: EIGENVALUE STRUCTURE CHARACTERIZATION")
print("=" * 70)

# Build M(I)
Q_identity = {}
for x in all_vertices():
    for mu in range(d):
        Q_identity[(x, mu)] = np.eye(3)

M_I = build_full_M(Q_identity)
eigvals_I = np.linalg.eigvalsh(M_I)
eigvals_I_sorted = np.sort(eigvals_I)

print(f"\nM(I) eigenvalue range: [{eigvals_I_sorted[0]:.4f}, {eigvals_I_sorted[-1]:.4f}]")

# Count multiplicities at Q=I
unique_eigs = {}
for ev in eigvals_I_sorted:
    key = round(ev)
    unique_eigs[key] = unique_eigs.get(key, 0) + 1

print("M(I) eigenvalue structure:")
for ev in sorted(unique_eigs.keys()):
    print(f"  {ev:3d} (x{unique_eigs[ev]})")

# Build momentum eigenspace projectors
projectors = build_momentum_eigenspaces(M_I)

# Build staggered basis
P_stag = build_staggered_basis()
P_perp = np.eye(N_dim) - P_stag @ P_stag.T  # projector onto non-stag

# Build non-staggered complement basis
eigvals_full, eigvecs_full = np.linalg.eigh(P_perp)
# Take eigenvectors with eigenvalue ~1
non_stag_indices = np.where(eigvals_full > 0.5)[0]
P_ns_basis = eigvecs_full[:, non_stag_indices]  # 183 columns
print(f"\nNon-staggered subspace dimension: {len(non_stag_indices)} (should be 183)")

# ============================================================
# Stage 1 & 4 combined: Random Q analysis
# ============================================================
print(f"\n{'='*70}")
print("STAGES 1+4: RANDOM Q ANALYSIS (300 configs)")
print("="*70)

N_configs = 300
max_lmax_full = 0
max_lmax_nonstag = 0
max_R_nonstag = 0  # max eigenvalue of R|_{non-stag}
max_lmax_nonstag_direct = 0

# Track momentum sector composition of top eigenvector
top_vec_compositions = []
all_full_lmax = []
all_nonstag_lmax = []
all_R_nonstag_max = []
all_stag_lmax = []

t0 = time.time()

for trial in range(N_configs):
    Q = generate_random_gauge()
    M = build_full_M(Q)
    R = M - M_I  # perturbation matrix

    # Full eigendecomposition
    eigvals, eigvecs = np.linalg.eigh(M)
    lmax = eigvals[-1]
    max_lmax_full = max(max_lmax_full, lmax)
    all_full_lmax.append(lmax)

    # Staggered eigenvalue
    M_stag = P_stag.T @ M @ P_stag  # 9x9
    stag_eigs = np.linalg.eigvalsh(M_stag)
    all_stag_lmax.append(stag_eigs[-1])

    # Non-staggered: restrict M to complement
    M_ns = P_ns_basis.T @ M @ P_ns_basis  # 183x183
    ns_eigs = np.linalg.eigvalsh(M_ns)
    ns_lmax = ns_eigs[-1]
    max_lmax_nonstag = max(max_lmax_nonstag, ns_lmax)
    all_nonstag_lmax.append(ns_lmax)

    # R restricted to non-stag
    R_ns = P_ns_basis.T @ R @ P_ns_basis  # 183x183
    R_ns_eigs = np.linalg.eigvalsh(R_ns)
    R_ns_max = R_ns_eigs[-1]
    max_R_nonstag = max(max_R_nonstag, R_ns_max)
    all_R_nonstag_max.append(R_ns_max)

    # Momentum sector decomposition of top eigenvector
    top_vec = eigvecs[:, -1]
    composition = {}
    for ev, P_ev in projectors.items():
        proj = P_ev @ (P_ev.T @ top_vec)
        weight = np.linalg.norm(proj)**2
        composition[ev] = weight
    top_vec_compositions.append(composition)

    if trial < 10 or trial % 50 == 49:
        print(f"  Config {trial:3d}: lmax_full={lmax:.4f}, lmax_nonstag={ns_lmax:.4f}, "
              f"R_nonstag_max={R_ns_max:.4f}, stag_max={stag_eigs[-1]:.4f}")

dt = time.time() - t0
print(f"\n  Time: {dt:.1f}s for {N_configs} configs")

# ============================================================
# Summary statistics
# ============================================================
print(f"\n{'='*70}")
print("SUMMARY STATISTICS")
print("="*70)

all_full_lmax = np.array(all_full_lmax)
all_nonstag_lmax = np.array(all_nonstag_lmax)
all_R_nonstag_max = np.array(all_R_nonstag_max)
all_stag_lmax = np.array(all_stag_lmax)

print(f"\nFull lambda_max:")
print(f"  max = {all_full_lmax.max():.6f}")
print(f"  mean = {all_full_lmax.mean():.4f}")
print(f"  std = {all_full_lmax.std():.4f}")
print(f"  violations (>16): {np.sum(all_full_lmax > 16 + 1e-10)}")

print(f"\nNon-staggered lambda_max (should be <= 16):")
print(f"  max = {all_nonstag_lmax.max():.6f}")
print(f"  mean = {all_nonstag_lmax.mean():.4f}")
print(f"  std = {all_nonstag_lmax.std():.4f}")
print(f"  violations (>16): {np.sum(all_nonstag_lmax > 16 + 1e-10)}")

print(f"\nR|_nonstag max eigenvalue (KEY: should be <= 4):")
print(f"  max = {all_R_nonstag_max.max():.6f}")
print(f"  mean = {all_R_nonstag_max.mean():.4f}")
print(f"  std = {all_R_nonstag_max.std():.4f}")
print(f"  violations (>4): {np.sum(all_R_nonstag_max > 4 + 1e-10)}")

print(f"\nStaggered lambda_max (proved <= 16):")
print(f"  max = {all_stag_lmax.max():.6f}")
print(f"  mean = {all_stag_lmax.mean():.4f}")

# Momentum composition of top eigenvector
print(f"\n{'='*70}")
print("TOP EIGENVECTOR MOMENTUM COMPOSITION (first 20 configs)")
print("="*70)
for i in range(min(20, len(top_vec_compositions))):
    comp = top_vec_compositions[i]
    parts = [f"{ev}:{comp[ev]:.3f}" for ev in sorted(comp.keys()) if comp[ev] > 0.01]
    print(f"  Config {i:3d}: lmax={all_full_lmax[i]:.4f}  composition: {', '.join(parts)}")

# Which Q=I sector does the top eigenvector come from?
print(f"\n{'='*70}")
print("DOMINANT MOMENTUM SECTOR OF TOP EIGENVECTOR")
print("="*70)
sector_counts = {ev: 0 for ev in projectors}
for comp in top_vec_compositions:
    dominant = max(comp, key=comp.get)
    sector_counts[dominant] += 1
for ev in sorted(sector_counts.keys()):
    print(f"  Sector {ev:3d}: {sector_counts[ev]}/{N_configs} ({100*sector_counts[ev]/N_configs:.1f}%)")

# ============================================================
# Adversarial check: try to maximize R|_{non-stag}
# ============================================================
print(f"\n{'='*70}")
print("ADVERSARIAL: EXTREME GAUGE CONFIGS")
print("="*70)

# Try gauge configs that maximize non-staggered eigenvalues
# Strategy: use gauge fields close to a rotation by pi
max_extreme_R = 0
max_extreme_ns = 0

for trial in range(100):
    # Random angle near pi
    angle = np.pi * (0.8 + 0.4 * np.random.rand())
    axis = np.random.randn(3)
    axis /= np.linalg.norm(axis)
    K = angle * np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    g = expm(K)

    Q = {}
    for x in all_vertices():
        for mu in range(d):
            # All links = same near-pi rotation
            perturbation = np.random.randn(3) * 0.1
            Kp = np.array([[0, -perturbation[2], perturbation[1]],
                           [perturbation[2], 0, -perturbation[0]],
                           [-perturbation[1], perturbation[0], 0]])
            Q[(x, mu)] = g @ expm(Kp)

    M = build_full_M(Q)
    R = M - M_I

    M_ns = P_ns_basis.T @ M @ P_ns_basis
    R_ns = P_ns_basis.T @ R @ P_ns_basis

    ns_eigs = np.linalg.eigvalsh(M_ns)
    R_ns_eigs = np.linalg.eigvalsh(R_ns)

    max_extreme_ns = max(max_extreme_ns, ns_eigs[-1])
    max_extreme_R = max(max_extreme_R, R_ns_eigs[-1])

print(f"  Extreme non-stag lambda_max: {max_extreme_ns:.6f}")
print(f"  Extreme R|_nonstag max: {max_extreme_R:.6f}")
print(f"  Violations (ns > 16): {'YES' if max_extreme_ns > 16 + 1e-10 else 'NONE'}")
print(f"  Violations (R > 4): {'YES' if max_extreme_R > 4 + 1e-10 else 'NONE'}")

# ============================================================
# More adversarial: uniform gauge config (all links = same g)
# ============================================================
print(f"\n{'='*70}")
print("ADVERSARIAL: UNIFORM GAUGE CONFIGS (all links same)")
print("="*70)

max_uniform_ns = 0
max_uniform_R = 0
best_angle = 0

for trial in range(200):
    angle = np.pi * np.random.rand()
    axis = np.random.randn(3)
    axis /= np.linalg.norm(axis)
    K = angle * np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    g = expm(K)

    Q = {}
    for x in all_vertices():
        for mu in range(d):
            Q[(x, mu)] = g.copy()

    M = build_full_M(Q)
    R = M - M_I

    M_ns = P_ns_basis.T @ M @ P_ns_basis
    R_ns = P_ns_basis.T @ R @ P_ns_basis

    ns_eigs = np.linalg.eigvalsh(M_ns)
    R_ns_eigs = np.linalg.eigvalsh(R_ns)

    if ns_eigs[-1] > max_uniform_ns:
        max_uniform_ns = ns_eigs[-1]
        max_uniform_R = R_ns_eigs[-1]
        best_angle = angle

        eigvals_full = np.linalg.eigvalsh(M)
        print(f"  New max at angle={angle:.4f}: ns_max={ns_eigs[-1]:.6f}, "
              f"R_max={R_ns_eigs[-1]:.6f}, full_max={eigvals_full[-1]:.6f}")

print(f"\n  Best uniform: ns_max={max_uniform_ns:.6f}, R_max={max_uniform_R:.6f}, angle={best_angle:.4f}")

# ============================================================
# Final verdict
# ============================================================
print(f"\n{'='*70}")
print("FINAL STAGE 1+4 VERDICT")
print("="*70)

overall_R_max = max(max_R_nonstag, max_extreme_R, max_uniform_R)
overall_ns_max = max(max_lmax_nonstag, max_extreme_ns, max_uniform_ns)

print(f"  Overall max R|_nonstag eigenvalue: {overall_R_max:.6f}")
print(f"  Overall max non-stag lambda_max: {overall_ns_max:.6f}")
print(f"  Bound R|_nonstag <= 4: {'HOLDS' if overall_R_max <= 4 + 1e-10 else 'FAILS'}")
print(f"  Bound non-stag <= 16: {'HOLDS' if overall_ns_max <= 16 + 1e-10 else 'FAILS'}")
print(f"  Gap to 16: {16 - overall_ns_max:.4f}")
print(f"  Gap to 4 for R: {4 - overall_R_max:.4f}")
