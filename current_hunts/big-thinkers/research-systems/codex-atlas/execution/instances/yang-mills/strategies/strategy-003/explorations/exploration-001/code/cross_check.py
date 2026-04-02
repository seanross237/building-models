"""
Cross-check: verify the M(Q) computation against direct B_□ evaluation.

For a specific random Q on L=2 (where E010 found no violations) and L=4
(where we found violations), compute ∑_□ |B_□(Q,v)|² TWO ways:
  1. Via the matrix: v^T M(Q) v
  2. Directly: loop over plaquettes, compute B_□ = Ã₁+Ã₂+Ã₃+Ã₄, sum |B_□|²

If they agree, the matrix construction is correct.
Also: verify B_□ B_□^T = 4I₃ for each plaquette.
Also: run L=2 to compare with E010 results.
"""

import numpy as np
import time

# --- SU(2) utilities ---

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
    coeffs /= np.linalg.norm(coeffs)
    coeffs *= eps
    return su2_exp(coeffs)

def adjoint_action(U, A):
    """Ad_U(A) = U A U† for U ∈ SU(2), A ∈ su(2)."""
    return U @ A @ np.conj(U).T

def su2_basis():
    """Orthonormal basis for su(2) under |A|² = -2Tr(A²)."""
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]

def su2_to_vec(A, basis):
    return np.array([-2 * np.trace(b @ A).real for b in basis])

def inner_product_su2(A, B):
    """-2 Re Tr(AB) for A, B ∈ su(2)."""
    return -2 * np.trace(A @ B).real

# --- Lattice ---

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        for i in range(self.d - 1, -1, -1):
            coords.append(idx % self.L)
            idx //= self.L
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


def compute_B_plaq_direct(Q, e1, e2, e3, e4, v_dict, basis):
    """
    Directly compute B_□ = Ã₁ + Ã₂ + Ã₃ + Ã₄ as an su(2) element.

    v_dict: maps edge index -> su(2) element (2x2 anti-Hermitian matrix)
    """
    Q1 = Q[e1]
    Q12 = Q1 @ Q[e2]
    Q123inv = Q12 @ np.conj(Q[e3]).T  # Q1 Q2 Q3^{-1}

    # Ã₁ = v_{e1} (no transport)
    A1 = v_dict[e1]

    # Ã₂ = Ad_{Q1}(v_{e2})
    A2 = adjoint_action(Q1, v_dict[e2])

    # Ã₃ = -Ad_{Q12}(v_{e3})
    A3 = -adjoint_action(Q12, v_dict[e3])

    # Ã₄ = -Ad_{Q123inv}(v_{e4})
    A4 = -adjoint_action(Q123inv, v_dict[e4])

    B = A1 + A2 + A3 + A4
    return B


def build_M_operator(lat, Q, basis):
    """Build M(Q) = ∑_□ B_□^T B_□."""
    dim_su = 3
    n_edges = lat.n_edges
    dim = dim_su * n_edges
    M = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T

        def ad_matrix(U):
            R = np.zeros((dim_su, dim_su))
            for j in range(dim_su):
                transformed = adjoint_action(U, basis[j])
                R[:, j] = su2_to_vec(transformed, basis)
            return R

        R1 = np.eye(dim_su)
        R2 = ad_matrix(Q1)
        R3 = -ad_matrix(Q12)
        R4 = -ad_matrix(Q123inv)

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M


def vec_to_su2_dict(v, n_edges, basis):
    """Convert flat vector to dict of su(2) elements."""
    dim_su = 3
    v_dict = {}
    for e in range(n_edges):
        coeffs = v[dim_su*e:dim_su*e+dim_su]
        A = sum(c * T for c, T in zip(coeffs, basis))
        v_dict[e] = A
    return v_dict


def run_checks():
    basis = su2_basis()

    for L_test in [2, 4]:
        d = 4
        lat = Lattice(L_test, d)
        print(f"\n{'='*60}")
        print(f"L={L_test}, d={d}: {lat.n_edges} edges, {lat.n_plaq} plaquettes, dim={3*lat.n_edges}")

        # Test 1: Q=I baseline
        print(f"\n--- Q=I ---")
        Q_id = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q_id[e] = np.eye(2)

        M_id = build_M_operator(lat, Q_id, basis)
        eigs_id = np.linalg.eigvalsh(M_id)
        print(f"  λ_max = {eigs_id[-1]:.10f}, expected {4*d}")
        print(f"  λ_min = {eigs_id[0]:.10f}")
        print(f"  Trace = {np.trace(M_id):.6f}, expected {12 * lat.n_plaq}")

        # Test 2: Random Q
        np.random.seed(12345)
        Q_rand = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q_rand[e] = random_su2()

        M_rand = build_M_operator(lat, Q_rand, basis)
        eigs_rand = np.linalg.eigvalsh(M_rand)
        print(f"\n--- Random Q (seed=12345) ---")
        print(f"  λ_max = {eigs_rand[-1]:.10f}, 4d={4*d}")
        print(f"  ratio = {eigs_rand[-1]/(4*d):.8f}")
        print(f"  Trace = {np.trace(M_rand):.6f}, expected {12 * lat.n_plaq}")

        # Verify B_□ B_□^T = 4I for a few plaquettes
        print(f"\n  Checking B_□ B_□^T = 4I₃ for first 5 plaquettes:")
        plaquettes = lat.plaquettes()
        for p_idx in range(min(5, len(plaquettes))):
            e1, e2, e3, e4, x, mu, nu = plaquettes[p_idx]
            Q1 = Q_rand[e1]
            Q12 = Q1 @ Q_rand[e2]
            Q123inv = Q12 @ np.conj(Q_rand[e3]).T

            def ad_matrix(U):
                R = np.zeros((3, 3))
                for j in range(3):
                    transformed = adjoint_action(U, basis[j])
                    R[:, j] = su2_to_vec(transformed, basis)
                return R

            R1 = np.eye(3)
            R2 = ad_matrix(Q1)
            R3 = -ad_matrix(Q12)
            R4 = -ad_matrix(Q123inv)

            # B_□ is 3 × (3*n_edges) but only 4 nonzero 3×3 blocks
            # B_□ B_□^T = ∑_i R_i R_i^T
            BBT = R1 @ R1.T + R2 @ R2.T + R3 @ R3.T + R4 @ R4.T
            err = np.max(np.abs(BBT - 4*np.eye(3)))
            print(f"    Plaquette {p_idx}: ||B B^T - 4I|| = {err:.2e}")

        # Cross-check: compute v^T M v vs ∑|B_□|² for top eigenvector
        print(f"\n  Cross-checking via direct B_□ computation:")
        eigenvalues, eigenvectors = np.linalg.eigh(M_rand)
        v_top = eigenvectors[:, -1]  # top eigenvector

        # Method 1: v^T M v
        vMv = v_top @ M_rand @ v_top

        # Method 2: direct computation
        v_dict = vec_to_su2_dict(v_top, lat.n_edges, basis)
        B_sum_sq = 0.0
        for (e1, e2, e3, e4, x, mu, nu) in plaquettes:
            B = compute_B_plaq_direct(Q_rand, e1, e2, e3, e4, v_dict, basis)
            # |B|² = -2 Tr(B²)
            B_sq = -2 * np.trace(B @ B).real
            B_sum_sq += B_sq

        v_norm_sq = np.dot(v_top, v_top)

        print(f"    v^T M v = {vMv:.10f}")
        print(f"    ∑|B_□|² = {B_sum_sq:.10f}")
        print(f"    |v|²    = {v_norm_sq:.10f}")
        print(f"    Ratio (matrix): {vMv / (4*d * v_norm_sq):.8f}")
        print(f"    Ratio (direct): {B_sum_sq / (4*d * v_norm_sq):.8f}")
        print(f"    Discrepancy: {abs(vMv - B_sum_sq):.2e}")

        if eigs_rand[-1] > 4*d + 1e-8:
            print(f"\n  *** VIOLATION detected: λ_max = {eigs_rand[-1]:.8f} > {4*d} ***")
            print(f"      This means ∑|B_□(Q,v)|² = {B_sum_sq:.6f} > {4*d * v_norm_sq:.6f} = 4d|v|²")
            print(f"      The B_□ inequality is FALSE for this Q!")
        else:
            print(f"\n  No violation: λ_max = {eigs_rand[-1]:.8f} ≤ {4*d}")


if __name__ == '__main__':
    run_checks()
