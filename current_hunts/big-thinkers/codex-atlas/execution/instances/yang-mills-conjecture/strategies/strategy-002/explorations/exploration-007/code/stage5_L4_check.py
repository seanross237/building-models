"""
Stage 5: L=4 spot check. Build M(Q) for L=4 (much larger matrix: 3*4*4^4=3072 dimensional)
and verify lambda_max <= 16.

Also: L=3 check (3*4*3^4 = 972 dimensional).
"""
import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import eigsh
from scipy.sparse import lil_matrix
import itertools
import time

np.random.seed(99)

d = 4

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def build_M_for_L(L, Q_dict):
    """Build full M(Q) for given lattice size L."""
    N_vertices = L**d
    N_edges = d * N_vertices
    N_dim = 3 * N_edges

    def vertex_index(x):
        idx = 0
        for i in range(d):
            idx = idx * L + (x[i] % L)
        return idx

    def edge_index(x, mu):
        return vertex_index(x) * d + mu

    def neighbor(x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % L
        return tuple(y)

    vertices = list(itertools.product(range(L), repeat=d))

    # Use sparse matrix for efficiency
    M = lil_matrix((N_dim, N_dim))

    for x in vertices:
        for mu in range(d):
            for nu in range(mu+1, d):
                xmu = neighbor(x, mu)
                xnu = neighbor(x, nu)

                G1 = np.eye(3)
                G2 = Q_dict[(x, mu)]
                G3 = -(Q_dict[(x, mu)] @ Q_dict[(xmu, nu)] @ Q_dict[(xnu, mu)].T)
                U = Q_dict[(x, mu)] @ Q_dict[(xmu, nu)] @ Q_dict[(xnu, mu)].T @ Q_dict[(x, nu)].T
                G4 = -U

                idx1 = 3 * edge_index(x, mu)
                idx2 = 3 * edge_index(xmu, nu)
                idx3 = 3 * edge_index(xnu, mu)
                idx4 = 3 * edge_index(x, nu)

                edges = [(idx1, G1), (idx2, G2), (idx3, G3), (idx4, G4)]
                for (ia, Ga) in edges:
                    for (ib, Gb) in edges:
                        block = Ga.T @ Gb
                        for i in range(3):
                            for j in range(3):
                                M[ia+i, ib+j] += block[i, j]

    return M.tocsr(), N_dim

def generate_Q(L, mode="random"):
    """Generate gauge configuration."""
    vertices = list(itertools.product(range(L), repeat=d))
    Q = {}
    for x in vertices:
        for mu in range(d):
            if mode == "identity":
                Q[(x, mu)] = np.eye(3)
            elif mode == "random":
                Q[(x, mu)] = expm(skew(np.random.randn(3)))
            elif mode == "near_pi":
                angle = np.pi * (0.8 + 0.4 * np.random.rand())
                axis = np.random.randn(3)
                axis /= np.linalg.norm(axis)
                Q[(x, mu)] = expm(angle * skew(axis))
    return Q

# ============================================================
# L=3 check
# ============================================================
print("=" * 70)
print("L=3 CHECK (d=4, N_dim=972)")
print("=" * 70)

L = 3
t0 = time.time()

# Identity check
Q_id = generate_Q(L, "identity")
M_id, N = build_M_for_L(L, Q_id)
print(f"  N_dim = {N}")

# Top eigenvalues
eigs_id = eigsh(M_id.toarray(), k=20, which='LM', return_eigenvectors=False)
print(f"  M(I) top 10 eigenvalues: {sorted(eigs_id)[-10:][::-1]}")
print(f"  lambda_max = {max(eigs_id):.6f}")

# Expected: 4*sum sin^2(k*pi/(2*3)) for k in {0,1,2}
# Max when k=(2,2,2,2): 4*4*sin^2(pi/3) = 16*sin^2(60°) = 16*3/4 = 12
print(f"  Expected max (L=3): 4*4*sin^2(π/3) = {16*np.sin(np.pi/3)**2:.4f}")

# Random Q check
max_lmax_L3 = 0
for trial in range(20):
    Q = generate_Q(L, "random")
    M, _ = build_M_for_L(L, Q)
    eigs = eigsh(M.toarray(), k=5, which='LM', return_eigenvectors=False)
    lmax = max(eigs)
    max_lmax_L3 = max(max_lmax_L3, lmax)
    if trial < 5:
        print(f"  Random {trial}: lmax = {lmax:.6f}")

print(f"  Max lambda_max over 20 random (L=3): {max_lmax_L3:.6f}")
print(f"  Exceeds 16? {'YES' if max_lmax_L3 > 16 + 1e-8 else 'NO'}")
print(f"  Time: {time.time()-t0:.1f}s")

# ============================================================
# L=4 check
# ============================================================
print(f"\n{'='*70}")
print("L=4 CHECK (d=4, N_dim=3072)")
print("="*70)

L = 4
t0 = time.time()

# Identity check first
Q_id = generate_Q(L, "identity")
M_id, N = build_M_for_L(L, Q_id)
print(f"  N_dim = {N}")

# Use only sparse eigsh for top eigenvalues
eigs_id = eigsh(M_id, k=20, which='LM', return_eigenvectors=False)
print(f"  M(I) top eigenvalues: {sorted(eigs_id)[-5:][::-1]}")
print(f"  lambda_max = {max(eigs_id):.6f}")
# Expected max: 4*4*sin^2(π/2) = 16 (since L=4, k can reach (π,π,π,π))
print(f"  Expected: 16.000000")

# Random Q checks
max_lmax_L4 = 0
for trial in range(10):
    Q = generate_Q(L, "random")
    M, _ = build_M_for_L(L, Q)
    eigs = eigsh(M, k=5, which='LM', return_eigenvectors=False)
    lmax = max(eigs)
    max_lmax_L4 = max(max_lmax_L4, lmax)
    print(f"  Random {trial}: lmax = {lmax:.6f}")

print(f"\n  Max lambda_max over 10 random (L=4): {max_lmax_L4:.6f}")
print(f"  Exceeds 16? {'YES' if max_lmax_L4 > 16 + 1e-8 else 'NO'}")

# Near-pi adversarial
max_adv_L4 = 0
for trial in range(5):
    Q = generate_Q(L, "near_pi")
    M, _ = build_M_for_L(L, Q)
    eigs = eigsh(M, k=5, which='LM', return_eigenvectors=False)
    lmax = max(eigs)
    max_adv_L4 = max(max_adv_L4, lmax)
    print(f"  Near-π {trial}: lmax = {lmax:.6f}")

print(f"\n  Max lambda_max adversarial (L=4): {max_adv_L4:.6f}")
print(f"  Exceeds 16? {'YES' if max_adv_L4 > 16 + 1e-8 else 'NO'}")
print(f"  Time: {time.time()-t0:.1f}s")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("MULTI-SCALE SUMMARY")
print("="*70)
print(f"  L=3: max lambda_max = {max_lmax_L3:.6f} (M(I) max = {16*np.sin(np.pi/3)**2:.4f}, bound 16)")
print(f"  L=4: max lambda_max = {max(max_lmax_L4, max_adv_L4):.6f} (M(I) max = 16, bound 16)")
print(f"  All within bound? {'YES' if max(max_lmax_L3, max_lmax_L4, max_adv_L4) <= 16 + 1e-8 else 'NO'}")
