"""
Check: Is P^T R(Q) P ≼ 0 where P is the top eigenspace of M(I)?

R(Q) = D(Q) = M(Q) - M(I) is NOT ≼ 0 in general.
But we only need λ_max(M(Q)) ≤ 4d, which is equivalent to:
  v^T R(Q) v ≤ 0 for all v in ker(M(I) - 4d·I)

The top eigenspace P of M(I) = K_curl at eigenvalue 4d has dimension 9
(from E004: multiplicity = 3(d-1) = 9 for SU(2) in d=4).

This script computes the 9×9 matrix P^T R(Q) P for many configs and checks
its eigenvalues.

Also: Abelian config analysis and D(Q) spectrum decomposition.
"""

import numpy as np
import json
import time

# ====================== SU(2) Utilities ======================

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct = np.cos(theta / 2)
    st = np.sin(theta / 2)
    return np.array([
        [ct + 1j*st*n[2], st*(1j*n[0] + n[1])],
        [st*(1j*n[0] - n[1]), ct - 1j*st*n[2]]
    ])

def su2_near_identity(eps):
    coeffs = np.random.randn(3)
    coeffs = coeffs / np.linalg.norm(coeffs) * eps
    return su2_exp(coeffs)

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]

def su2_to_vec(A, basis):
    return np.array([-2 * np.trace(b @ A).real for b in basis])

def ad_matrix_fn(U, basis):
    dim_su = len(basis)
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R

# ====================== Lattice ======================

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites
        self.dim_su = 3
        self.dim = self.dim_su * self.n_edges

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        r = idx
        for i in range(self.d - 1, -1, -1):
            coords.append(r % self.L)
            r //= self.L
        return list(reversed(coords))

    def edge_index(self, site_idx, mu):
        return site_idx * self.d + mu

    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)

    def plaquettes(self):
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu)
                    x_nu = self.shifted_site(x, nu)
                    e1 = self.edge_index(x, mu)
                    e2 = self.edge_index(x_mu, nu)
                    e3 = self.edge_index(x_nu, mu)
                    e4 = self.edge_index(x, nu)
                    plaq_list.append((e1, e2, e3, e4, x, mu, nu))
        return plaq_list

def build_M_operator(lat, Q, basis):
    dim_su = lat.dim_su
    dim = lat.dim
    M = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        R1 = np.eye(dim_su)
        R2 = ad_matrix_fn(Q1, basis)
        R3 = -ad_matrix_fn(Q123inv, basis)
        R4 = -ad_matrix_fn(U_plaq, basis)

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M

def build_K_curl(lat):
    dim_su = lat.dim_su
    dim = lat.dim
    K = np.zeros((dim, dim))
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        signs = {e1: +1, e2: +1, e3: -1, e4: -1}
        edges = [e1, e2, e3, e4]
        for ei in edges:
            for ej in edges:
                si = signs[ei]
                sj = signs[ej]
                K[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += si * sj * np.eye(dim_su)
    return K

# ====================== Config Generators ======================

def gen_identity(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = np.eye(2)
    return Q

def gen_random_haar(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = random_su2()
    return Q

def gen_near_identity(lat, eps):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = su2_near_identity(eps)
    return Q

def gen_pure_gauge(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    g = [random_su2() for _ in range(lat.n_sites)]
    for x in range(lat.n_sites):
        for mu in range(lat.d):
            e = lat.edge_index(x, mu)
            y = lat.shifted_site(x, mu)
            Q[e] = g[x] @ np.conj(g[y]).T
    return Q

def gen_abelian(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        theta = np.random.uniform(0, 2*np.pi)
        Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])
    return Q

# ====================== Main ======================

def main():
    np.random.seed(42)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)
    bound = 4 * d

    # Get K_curl and its top eigenspace
    K_curl = build_K_curl(lat)
    eigs_K, vecs_K = np.linalg.eigh(K_curl)

    # Top eigenspace: eigenvalue = 4d = 16
    tol = 1e-8
    top_mask = np.abs(eigs_K - bound) < tol
    n_top = np.sum(top_mask)
    P = vecs_K[:, top_mask]  # 192 × n_top

    print(f"K_curl top eigenspace: eigenvalue = {bound}, multiplicity = {n_top}")
    print(f"P shape: {P.shape}")
    print()

    # Verify: P^T K_curl P should be 4d * I
    PKP = P.T @ K_curl @ P
    diag_err = np.max(np.abs(PKP - bound * np.eye(n_top)))
    print(f"Verification: |P^T K_curl P - 16I| = {diag_err:.2e}")
    print()

    # ===== TOP EIGENSPACE PROJECTION =====
    print("="*70)
    print("TOP EIGENSPACE PROJECTION: P^T R(Q) P eigenvalues")
    print("="*70)
    print()
    print("If P^T R(Q) P ≼ 0 for all Q, then λ_max(M(Q)) ≤ 4d.")
    print("(This is necessary but not sufficient for λ_max ≤ 4d.)")
    print()

    configs = []

    # Pure gauge (5)
    for i in range(5):
        configs.append((f"Pure gauge #{i+1}", gen_pure_gauge(lat)))

    # Random Haar (20)
    for i in range(20):
        configs.append((f"Random Haar #{i+1}", gen_random_haar(lat)))

    # Near-identity
    for eps in [0.01, 0.1, 0.5, 1.0]:
        for i in range(3):
            configs.append((f"Near-I ε={eps} #{i+1}", gen_near_identity(lat, eps)))

    # Abelian
    for i in range(5):
        configs.append((f"Abelian #{i+1}", gen_abelian(lat)))

    print(f"Testing {len(configs)} configurations")
    print()

    header = f"{'Config':<25s} {'λ_max(P^T R P)':<16s} {'λ_min(P^T R P)':<16s} {'λ_max(M)':<12s} {'#pos':<6s} {'Status'}"
    print(header)
    print("-" * len(header))

    all_pass = True
    results = []

    for name, Q in configs:
        M_Q = build_M_operator(lat, Q, basis)
        R_Q = M_Q - K_curl

        # Project R onto top eigenspace
        PRP = P.T @ R_Q @ P  # n_top × n_top
        eigs_PRP = np.sort(np.linalg.eigvalsh(PRP))

        lam_max_PRP = eigs_PRP[-1]
        lam_min_PRP = eigs_PRP[0]
        n_pos = np.sum(eigs_PRP > 1e-10)
        lam_max_M = np.linalg.eigvalsh(M_Q)[-1]

        if lam_max_PRP > 1e-8:
            status = "*** POS ***"
            all_pass = False
        else:
            status = "≼ 0"

        print(f"{name:<25s} {lam_max_PRP:<16.10f} {lam_min_PRP:<16.10f} {lam_max_M:<12.6f} {n_pos:<6d} {status}")

        results.append({
            'name': name,
            'lam_max_PRP': float(lam_max_PRP),
            'lam_min_PRP': float(lam_min_PRP),
            'lam_max_M': float(lam_max_M),
            'n_pos_PRP': int(n_pos),
            'eigs_PRP': [float(e) for e in eigs_PRP],
        })

    print()
    if all_pass:
        print(f"*** ALL {len(configs)} CONFIGS: P^T R(Q) P ≼ 0 ***")
    else:
        fails = [r for r in results if r['lam_max_PRP'] > 1e-8]
        print(f"*** {len(fails)} CONFIGS WITH P^T R(Q) P > 0 ***")

    # ===== DETAILED EIGENVALUE ANALYSIS =====
    print()
    print("="*70)
    print("DETAILED P^T R(Q) P EIGENVALUES")
    print("="*70)
    print()

    for r in results[:10]:
        print(f"  {r['name']}:")
        print(f"    P^T R P eigenvalues: {[f'{e:.6f}' for e in r['eigs_PRP']]}")
        print()

    # ===== ABELIAN DECOMPOSITION =====
    print("="*70)
    print("ABELIAN CONFIG: τ₃ SECTOR vs τ₁τ₂ SECTOR")
    print("="*70)
    print()

    for trial in range(3):
        Q = gen_abelian(lat)
        M_Q = build_M_operator(lat, Q, basis)
        R_Q = M_Q - K_curl

        # Decompose into τ₃ and τ₁τ₂ blocks
        idx_3 = [3*e + 2 for e in range(lat.n_edges)]
        idx_12 = []
        for e in range(lat.n_edges):
            idx_12.extend([3*e, 3*e+1])

        # τ₃ block of R
        R_33 = R_Q[np.ix_(idx_3, idx_3)]
        eigs_R33 = np.linalg.eigvalsh(R_33)

        # τ₁τ₂ block of R
        R_12 = R_Q[np.ix_(idx_12, idx_12)]
        eigs_R12 = np.linalg.eigvalsh(R_12)

        # Cross-block
        R_cross = R_Q[np.ix_(idx_3, idx_12)]
        cross_max = np.max(np.abs(R_cross))

        # Full eigenvalues
        eigs_full = np.linalg.eigvalsh(R_Q)

        # M(Q) eigenvalues
        eigs_M = np.linalg.eigvalsh(M_Q)

        print(f"  Abelian #{trial+1}:")
        print(f"    τ₃ block: max|eig(R)| = {np.max(np.abs(eigs_R33)):.2e}, R is zero? {np.max(np.abs(R_33)) < 1e-10}")
        print(f"    τ₁τ₂ block: max eig(R) = {np.max(eigs_R12):.6f}, min = {np.min(eigs_R12):.6f}")
        print(f"    Cross-block: max|entry| = {cross_max:.2e}")
        print(f"    Full R: max = {np.max(eigs_full):.6f}, min = {np.min(eigs_full):.6f}")
        print(f"    λ_max(M) = {eigs_M[-1]:.10f}")
        print(f"    Tr(R) = {np.trace(R_Q):.2e}")
        print()

    # ===== TRACE ANALYSIS =====
    print("="*70)
    print("TRACE ANALYSIS: Tr(M(Q)) vs Tr(M(I))")
    print("="*70)
    print()
    print(f"Tr(M(I)) = {np.trace(K_curl):.4f} = 12 × {lat.n_plaq} plaquettes")
    print()

    for name, Q in configs[:15]:
        M_Q = build_M_operator(lat, Q, basis)
        tr_Q = np.trace(M_Q)
        tr_I = np.trace(K_curl)
        tr_diff = tr_Q - tr_I
        print(f"  {name:<25s}: Tr(M(Q)) = {tr_Q:.4f}, diff = {tr_diff:.4f}")

    print()
    print("Note: Tr(M(Q)) = ∑_□ ∑_{e∈□} Tr(R_e^T R_e) = ∑_□ ∑_{e∈□} 3 = 12 × n_plaq")
    print("So Tr(M(Q)) = Tr(M(I)) for all Q! (each R_e is orthogonal)")

if __name__ == '__main__':
    main()
