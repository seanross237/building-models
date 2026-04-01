"""
Perturbation analysis: show that Q=I is a local maximum of λ_max(M(Q)).

For Q_e = exp(εA_e) near identity (A_e ∈ su(2)):
1. Compute δM = dM/dε|_{ε=0}
2. Check if ⟨v*, δM v*⟩ = 0 (critical point condition)
3. If yes, compute δ²M and check ⟨v*, δ²M v*⟩ ≤ 0 (local max)

where v* is the top eigenvector of M(I).

Also: check eigenvalue sensitivity numerically for various perturbation directions.
"""

import numpy as np
import time

# --- SU(2) utilities ---

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a+1j*b, c+1j*d], [-c+1j*d, a-1j*b]])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct, st = np.cos(theta/2), np.sin(theta/2)
    return np.array([[ct+1j*st*n[2], st*(1j*n[0]+n[1])],
                      [st*(1j*n[0]-n[1]), ct-1j*st*n[2]]])

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [1j*s1/2, 1j*s2/2, 1j*s3/2]

def su2_to_vec(A, basis):
    return np.array([-2*np.trace(b @ A).real for b in basis])

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
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
        for i in range(self.d-1, -1, -1):
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


def build_M_corrected(lat, Q, basis):
    """Build M(Q) with correct transport formula."""
    dim_su = 3
    dim = dim_su * lat.n_edges
    M = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        def ad_matrix(U):
            R = np.zeros((dim_su, dim_su))
            for j in range(dim_su):
                transformed = adjoint_action(U, basis[j])
                R[:, j] = su2_to_vec(transformed, basis)
            return R

        R1 = np.eye(dim_su)
        R2 = ad_matrix(Q1)
        R3 = -ad_matrix(Q123inv)
        R4 = -ad_matrix(U_plaq)

        for (ei, Ri) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
            for (ej, Rj) in [(e1,R1),(e2,R2),(e3,R3),(e4,R4)]:
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += Ri.T @ Rj

    return M


def analyze_perturbation():
    """Analyze eigenvalue sensitivity at Q=I."""
    L, d = 2, 4
    lat = Lattice(L, d)
    basis = su2_basis()
    dim = 3 * lat.n_edges
    bound = 4 * d

    print(f"L={L}, d={d}, dim={dim}")
    print(f"Perturbation analysis of λ_max(M(Q)) at Q=I\n")

    # Q=I baseline
    Q_id = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q_id[e] = np.eye(2)

    M_id = build_M_corrected(lat, Q_id, basis)
    eigs, vecs = np.linalg.eigh(M_id)
    lam_max_id = eigs[-1]
    print(f"λ_max(M(I)) = {lam_max_id:.10f}")
    print(f"Multiplicity of λ_max: {np.sum(np.abs(eigs - lam_max_id) < 1e-8)}")

    # Top eigenspace
    top_mask = np.abs(eigs - lam_max_id) < 1e-8
    top_vecs = vecs[:, top_mask]
    print(f"Top eigenspace dimension: {top_vecs.shape[1]}")

    # --- Numerical first derivative ---
    # For each single-link perturbation direction, compute λ_max(Q(ε))
    print(f"\n=== First derivative check (should be zero at Q=I) ===")

    n_test = 20
    epsilons = [1e-4, 1e-3, 1e-2, 0.1]

    # Test: perturb a single link in a single su(2) direction
    for trial in range(5):
        np.random.seed(trial)
        # Random perturbation direction: random A_e for each edge
        A_coeffs = np.random.randn(lat.n_edges, 3)
        A_coeffs /= np.linalg.norm(A_coeffs)  # Normalize

        lambdas = []
        for eps in [0] + epsilons + [-e for e in epsilons]:
            Q_pert = np.zeros((lat.n_edges, 2, 2), dtype=complex)
            for e in range(lat.n_edges):
                Q_pert[e] = su2_exp(eps * A_coeffs[e])

            M_pert = build_M_corrected(lat, Q_pert, basis)
            lam = np.linalg.eigvalsh(M_pert)[-1]
            lambdas.append((eps, lam))

        # Sort by epsilon
        lambdas.sort()
        print(f"\n  Trial {trial}: perturbation in random direction")
        for eps, lam in lambdas:
            delta = lam - lam_max_id
            print(f"    ε={eps:+.4f}: λ_max = {lam:.8f}, Δ = {delta:+.2e}")

    # --- Focused analysis: derivative and curvature ---
    print(f"\n=== Eigenvalue curvature (second derivative) ===")

    np.random.seed(42)
    for trial in range(5):
        A_coeffs = np.random.randn(lat.n_edges, 3)
        A_coeffs /= np.linalg.norm(A_coeffs)

        # 5-point stencil for second derivative
        h = 1e-3
        lam_vals = []
        for factor in [-2, -1, 0, 1, 2]:
            Q_pert = np.zeros((lat.n_edges, 2, 2), dtype=complex)
            for e in range(lat.n_edges):
                Q_pert[e] = su2_exp(factor * h * A_coeffs[e])

            M_pert = build_M_corrected(lat, Q_pert, basis)
            lam_vals.append(np.linalg.eigvalsh(M_pert)[-1])

        # Second derivative: (-f(2h) + 16f(h) - 30f(0) + 16f(-h) - f(-2h)) / (12h²)
        d2lam = (-lam_vals[0] + 16*lam_vals[1] - 30*lam_vals[2] + 16*lam_vals[3] - lam_vals[4]) / (12*h**2)
        # First derivative: (-f(2h) + 8f(h) - 8f(-h) + f(-2h)) / (12h)
        d1lam = (-lam_vals[0] + 8*lam_vals[1] - 8*lam_vals[3] + lam_vals[4]) / (12*h)

        print(f"  Trial {trial}: dλ/dε = {d1lam:+.6e}, d²λ/dε² = {d2lam:+.6f}")

    print(f"\n=== Single-edge perturbation ===")
    for e_test in range(min(10, lat.n_edges)):
        for a_test in range(3):
            A_coeffs = np.zeros((lat.n_edges, 3))
            A_coeffs[e_test, a_test] = 1.0

            h = 1e-3
            lam_vals = []
            for factor in [-2, -1, 0, 1, 2]:
                Q_pert = np.zeros((lat.n_edges, 2, 2), dtype=complex)
                for e in range(lat.n_edges):
                    if np.any(A_coeffs[e] != 0):
                        Q_pert[e] = su2_exp(factor * h * A_coeffs[e])
                    else:
                        Q_pert[e] = np.eye(2)

                M_pert = build_M_corrected(lat, Q_pert, basis)
                lam_vals.append(np.linalg.eigvalsh(M_pert)[-1])

            d2lam = (-lam_vals[0] + 16*lam_vals[1] - 30*lam_vals[2] + 16*lam_vals[3] - lam_vals[4]) / (12*h**2)
            d1lam = (-lam_vals[0] + 8*lam_vals[1] - 8*lam_vals[3] + lam_vals[4]) / (12*h)

            if abs(d1lam) > 1e-4 or d2lam > 1e-4:
                print(f"  Edge {e_test}, dir {a_test}: dλ/dε = {d1lam:+.6e}, d²λ/dε² = {d2lam:+.6f}")

    # Summary
    print(f"\n=== All single-edge second derivatives ===")
    d2_values = []
    for e_test in range(lat.n_edges):
        for a_test in range(3):
            A_coeffs = np.zeros((lat.n_edges, 3))
            A_coeffs[e_test, a_test] = 1.0

            h = 1e-3
            lam_vals = []
            for factor in [-1, 0, 1]:
                Q_pert = np.zeros((lat.n_edges, 2, 2), dtype=complex)
                for e in range(lat.n_edges):
                    if np.any(A_coeffs[e] != 0):
                        Q_pert[e] = su2_exp(factor * h * A_coeffs[e])
                    else:
                        Q_pert[e] = np.eye(2)

                M_pert = build_M_corrected(lat, Q_pert, basis)
                lam_vals.append(np.linalg.eigvalsh(M_pert)[-1])

            d2lam = (lam_vals[0] - 2*lam_vals[1] + lam_vals[2]) / h**2
            d2_values.append(d2lam)

    d2_values = np.array(d2_values)
    print(f"  Number of directions: {len(d2_values)}")
    print(f"  Max d²λ/dε²: {np.max(d2_values):.6f}")
    print(f"  Min d²λ/dε²: {np.min(d2_values):.6f}")
    print(f"  Mean d²λ/dε²: {np.mean(d2_values):.6f}")

    if np.max(d2_values) > 1e-4:
        print(f"  *** WARNING: Some directions have POSITIVE second derivative! ***")
        pos_idx = np.where(d2_values > 1e-4)[0]
        print(f"  Positive directions: {len(pos_idx)} out of {len(d2_values)}")
    else:
        print(f"  ALL second derivatives ≤ 0 → Q=I is a LOCAL MAXIMUM of λ_max")


if __name__ == '__main__':
    analyze_perturbation()
