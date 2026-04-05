"""
Pure gauge isometry verification + correct inequality check.

Key finding from Step 1: M(Q) ≼ M(I) is FALSE. D(Q) = M(Q) - M(I) has many positive eigenvalues.

But: λ_max(M(Q)) ≤ λ_max(M(I)) = 4d is the correct target.

This script verifies:
1. Pure gauge M(Q) is isospectral with M(I) (same eigenvalues)
2. λ_max(M(Q)) ≤ 4d for all Q
3. For non-pure-gauge Q, λ_max(M(Q)) < 4d strictly
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

def ad_matrix(U, basis):
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

# ====================== Build M(Q) ======================

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
        R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis)
        R4 = -ad_matrix(U_plaq, basis)

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M

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

def gen_pure_gauge(lat):
    """Pure gauge: Q_e = g_{s(e)} g_{t(e)}^{-1}."""
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    g = [random_su2() for _ in range(lat.n_sites)]
    for x in range(lat.n_sites):
        for mu in range(lat.d):
            e = lat.edge_index(x, mu)
            y = lat.shifted_site(x, mu)
            Q[e] = g[x] @ np.conj(g[y]).T
    return Q, g

def gen_near_identity(lat, eps):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = su2_near_identity(eps)
    return Q

# ====================== Build Ad_g block-diagonal ======================

def build_Ad_g_matrix(lat, g, basis):
    """Build the block-diagonal matrix Ad_g: v_{x,μ,a} -> (Ad_{g_x})_{ab} v_{x,μ,b}."""
    dim = lat.dim
    dim_su = lat.dim_su
    Ad = np.zeros((dim, dim))

    for x in range(lat.n_sites):
        R = ad_matrix(g[x], basis)
        for mu in range(lat.d):
            e = lat.edge_index(x, mu)
            Ad[dim_su*e:dim_su*e+dim_su, dim_su*e:dim_su*e+dim_su] = R

    return Ad

# ====================== Main ======================

def main():
    np.random.seed(42)
    basis = su2_basis()

    L = 2
    d = 4
    lat = Lattice(L, d)
    bound = 4 * d

    print(f"Lattice: L={L}, d={d}, dim={lat.dim}")
    print()

    # Reference: M(I) = K_curl
    Q_id = gen_identity(lat)
    M_I = build_M_operator(lat, Q_id, basis)
    eigs_I = np.sort(np.linalg.eigvalsh(M_I))

    print("="*70)
    print("PART 1: PURE GAUGE ISOMETRY VERIFICATION")
    print("="*70)
    print()
    print("Theory: For pure gauge Q_e = g_x g_y^{-1}, M(Q) = Ad_g^T M(I) Ad_g")
    print("=> M(Q) is isospectral with M(I) (same eigenvalues)")
    print("=> D(Q) = M(Q) - M(I) has trace 0 and is NOT ≼ 0 in general")
    print()

    for trial in range(10):
        Q_pg, g = gen_pure_gauge(lat)
        M_Q = build_M_operator(lat, Q_pg, basis)
        eigs_Q = np.sort(np.linalg.eigvalsh(M_Q))

        # Check isospectrality
        eig_diff = np.max(np.abs(eigs_Q - eigs_I))

        # Check the conjugation formula: M(Q) = Ad_g^T M(I) Ad_g
        # where Ad_g acts as: v_{x,mu,a} -> (Ad_{g_x})_{ab} v_{x,mu,b}
        # But this isn't quite right. We need the INVERSE gauge transform:
        # v_{x,mu} -> Ad_{g_x^{-1}} v_{x,mu}
        # M(Q_pure) = Ad_{g^{-1}}^T M(I) Ad_{g^{-1}}
        #
        # Let's verify both forms
        Ad_g = build_Ad_g_matrix(lat, g, basis)
        ginv = [np.conj(g[x]).T for x in range(lat.n_sites)]
        Ad_ginv = build_Ad_g_matrix(lat, ginv, basis)

        # Check: Ad_g is orthogonal (since Ad_{SU(2)} ∈ SO(3))
        ortho_err = np.max(np.abs(Ad_g @ Ad_g.T - np.eye(lat.dim)))

        # Test: M(Q) = Ad_ginv^T M(I) Ad_ginv = Ad_g M(I) Ad_g^T ?
        # Ad_ginv = Ad_g^{-1} = Ad_g^T (since orthogonal)
        M_conj1 = Ad_ginv.T @ M_I @ Ad_ginv
        M_conj2 = Ad_g @ M_I @ Ad_g.T

        conj_err1 = np.max(np.abs(M_Q - M_conj1))
        conj_err2 = np.max(np.abs(M_Q - M_conj2))

        # D(Q) = M(Q) - M(I) spectrum
        D_Q = M_Q - M_I
        eigs_D = np.sort(np.linalg.eigvalsh(D_Q))

        print(f"  Pure gauge #{trial+1}:")
        print(f"    |eigs(M(Q)) - eigs(M(I))| = {eig_diff:.2e} (should be ~0)")
        print(f"    |M(Q) - Ad_ginv^T M(I) Ad_ginv| = {conj_err1:.2e}")
        print(f"    |M(Q) - Ad_g M(I) Ad_g^T|      = {conj_err2:.2e}")
        print(f"    Ad_g orthogonality error = {ortho_err:.2e}")
        print(f"    λ_max(M(Q)) = {eigs_Q[-1]:.10f} (should be 16)")
        print(f"    λ_max(D(Q)) = {eigs_D[-1]:.6f}, λ_min(D(Q)) = {eigs_D[0]:.6f}")
        print(f"    Tr(D(Q)) = {np.trace(D_Q):.2e} (should be 0)")
        print(f"    # positive eigs of D: {np.sum(eigs_D > 1e-10)}, # negative: {np.sum(eigs_D < -1e-10)}")
        print()

    print()
    print("="*70)
    print("PART 2: λ_max(M(Q)) ≤ 4d FOR ALL Q")
    print("="*70)
    print()
    print("This is the CORRECT inequality (not the full operator inequality).")
    print()

    configs = []

    # Pure gauge
    for i in range(5):
        Q_pg, _ = gen_pure_gauge(lat)
        configs.append((f"Pure gauge #{i+1}", Q_pg))

    # Random Haar
    for i in range(20):
        configs.append((f"Random Haar #{i+1}", gen_random_haar(lat)))

    # Near-identity
    for eps in [0.01, 0.1, 0.5, 1.0, 2.0]:
        for i in range(3):
            configs.append((f"Near-I ε={eps} #{i+1}", gen_near_identity(lat, eps)))

    # Diagonal/abelian
    for i in range(5):
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            theta = np.random.uniform(0, 2*np.pi)
            Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])
        configs.append((f"Abelian #{i+1}", Q))

    print(f"Testing {len(configs)} configurations:")
    print()
    header = f"{'Config':<25s} {'λ_max(M)':<14s} {'gap to 4d':<14s} {'Status':<10s}"
    print(header)
    print("-" * len(header))

    all_pass = True
    max_ratio = 0.0
    for name, Q in configs:
        M_Q = build_M_operator(lat, Q, basis)
        eigs = np.linalg.eigvalsh(M_Q)
        lam_max = eigs[-1]
        gap = bound - lam_max
        ratio = lam_max / bound

        if lam_max > bound + 1e-8:
            status = "VIOLATION!"
            all_pass = False
        elif abs(gap) < 1e-6:
            status = "= 4d"
        else:
            status = f"< 4d"

        max_ratio = max(max_ratio, ratio)
        print(f"{name:<25s} {lam_max:<14.8f} {gap:<14.8f} {status:<10s}")

    print()
    if all_pass:
        print(f"*** ALL {len(configs)} PASS: λ_max(M(Q)) ≤ 4d ***")
        print(f"    Max ratio λ_max/4d = {max_ratio:.10f}")
    else:
        print("*** VIOLATIONS FOUND ***")

    print()
    print("="*70)
    print("PART 3: CHARACTERIZE WHICH Q ACHIEVE λ_max = 4d")
    print("="*70)
    print()
    print("Check: λ_max(M(Q)) = 4d iff Q is pure gauge (all plaquette holonomies = I)")
    print()

    # For each config, compute plaquette holonomy
    for name, Q in configs[:10]:  # First 10
        M_Q = build_M_operator(lat, Q, basis)
        lam_max = np.linalg.eigvalsh(M_Q)[-1]

        # Compute max plaquette deviation from I
        max_hol_dev = 0.0
        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T
            dev = np.linalg.norm(U_plaq - np.eye(2))
            max_hol_dev = max(max_hol_dev, dev)

        is_pure_gauge = max_hol_dev < 1e-8
        gap = bound - lam_max
        print(f"  {name:<25s}: λ_max={lam_max:.8f}, gap={gap:.8f}, max_hol_dev={max_hol_dev:.6f}, pure_gauge={is_pure_gauge}")


if __name__ == '__main__':
    main()
