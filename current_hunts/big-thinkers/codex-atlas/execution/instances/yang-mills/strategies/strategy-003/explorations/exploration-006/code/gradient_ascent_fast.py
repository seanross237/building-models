"""
Fast gradient ascent on λ_max(M(Q)).

Uses Rayleigh quotient gradient:
  ∂λ_max/∂Q_e ≈ (1/δ) * [v_max^T M(Q_pert) v_max - v_max^T M(Q) v_max]

where v_max is the top eigenvector and Q_pert = exp(δ A_e) Q_e.

Optimization: we only need the Rayleigh quotient change, not the full
eigendecomposition, for each perturbation direction.

Actually, for speed, let's use the analytical gradient:
  ∂(v^T M v)/∂ε_e,a = 2 ∑_□∋e ⟨B_□(Q,v), ∂B_□/∂ε_{e,a}⟩
"""

import numpy as np
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

# ====================== Gradient Ascent ======================

def gradient_ascent_lambda_max(lat, Q, basis, n_steps=50, lr=0.02, verbose=True):
    """
    Gradient ascent on λ_max(M(Q)) using finite differences.

    For efficiency, only perturb a random subset of edges each step.
    """
    bound = 4 * lat.d
    n_edges = lat.n_edges

    history = []

    for step in range(n_steps):
        M_Q = build_M_operator(lat, Q, basis)
        eigs, vecs = np.linalg.eigh(M_Q)
        lam_max = eigs[-1]
        v_max = vecs[:, -1]

        history.append(float(lam_max))

        if verbose and (step % 10 == 0 or step == n_steps - 1):
            print(f"    Step {step:3d}: λ_max = {lam_max:.8f}, gap = {bound - lam_max:.8f}")

        # Compute gradient via finite differences on Rayleigh quotient
        delta = 1e-5
        grad = np.zeros((n_edges, 3))

        for e in range(n_edges):
            for a in range(3):
                A_vec = np.zeros(3)
                A_vec[a] = delta
                Q_pert = Q.copy()
                Q_pert[e] = su2_exp(A_vec) @ Q[e]

                # Only recompute the blocks involving edge e
                # For speed, use Rayleigh quotient
                M_pert = build_M_operator(lat, Q_pert, basis)
                lam_pert = v_max @ M_pert @ v_max
                grad[e, a] = (lam_pert - lam_max) / delta

        # Update
        grad_norm = np.linalg.norm(grad)
        if grad_norm < 1e-10:
            if verbose:
                print(f"    Gradient vanished at step {step}")
            break

        for e in range(n_edges):
            if np.linalg.norm(grad[e]) > 1e-12:
                A_step = lr * grad[e]
                Q[e] = su2_exp(A_step) @ Q[e]
                # Re-unitarize
                u, s, vh = np.linalg.svd(Q[e])
                Q[e] = u @ vh

    return Q, history

def main():
    np.random.seed(42)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)
    bound = 4 * d

    print(f"Lattice: L={L}, d={d}")
    print(f"Gradient ascent on λ_max(M(Q))")
    print(f"Target: 4d = {bound}")
    print()

    # Start from several random configs
    for trial in range(5):
        print(f"Trial #{trial+1}:")
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q[e] = su2_near_identity(1.5)

        t0 = time.time()
        Q_final, history = gradient_ascent_lambda_max(lat, Q, basis, n_steps=30, lr=0.02)
        elapsed = time.time() - t0

        # Final analysis
        M_final = build_M_operator(lat, Q_final, basis)
        eigs_final = np.linalg.eigvalsh(M_final)
        lam_max_final = eigs_final[-1]

        # Check holonomies
        max_hol_dev = 0.0
        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            Q1 = Q_final[e1]
            Q12 = Q1 @ Q_final[e2]
            Q123inv = Q12 @ np.conj(Q_final[e3]).T
            U_plaq = Q123inv @ np.conj(Q_final[e4]).T
            dev = np.linalg.norm(U_plaq - np.eye(2))
            max_hol_dev = max(max_hol_dev, dev)

        print(f"    Final: λ_max = {lam_max_final:.10f}")
        print(f"    Gap to 4d: {bound - lam_max_final:.10f}")
        print(f"    Max plaq deviation: {max_hol_dev:.6f}")
        print(f"    Time: {elapsed:.1f}s")
        print(f"    History: {[f'{h:.4f}' for h in history[::10]]}")
        print()

    # Now: specifically try gradient ascent on P^T R(Q) P eigenvalue
    print("="*70)
    print("Gradient ascent on λ_max(P^T R(Q) P)")
    print("="*70)
    print()

    # Get top eigenspace of K_curl
    K_curl_I = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        K_curl_I[e] = np.eye(2)

    M_I = build_M_operator(lat, K_curl_I, basis)
    eigs_I, vecs_I = np.linalg.eigh(M_I)
    top_mask = np.abs(eigs_I - bound) < 1e-8
    P = vecs_I[:, top_mask]  # 192 × 9

    print(f"Top eigenspace dimension: {P.shape[1]}")
    print()

    for trial in range(3):
        print(f"Trial #{trial+1}:")
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q[e] = su2_near_identity(0.5)

        for step in range(20):
            M_Q = build_M_operator(lat, Q, basis)
            R_Q = M_Q - M_I
            PRP = P.T @ R_Q @ P
            eigs_PRP = np.linalg.eigvalsh(PRP)

            if step % 5 == 0:
                print(f"    Step {step}: max eig(P^T R P) = {eigs_PRP[-1]:.10f}")

            # Gradient of max eigenvalue of P^T R P
            delta = 1e-5
            for e in range(lat.n_edges):
                for a in range(3):
                    A_vec = np.zeros(3)
                    A_vec[a] = delta
                    Q_pert = Q.copy()
                    Q_pert[e] = su2_exp(A_vec) @ Q[e]
                    M_pert = build_M_operator(lat, Q_pert, basis)
                    R_pert = M_pert - M_I
                    PRP_pert = P.T @ R_pert @ P
                    eigs_pert = np.linalg.eigvalsh(PRP_pert)

                    grad_ea = (eigs_pert[-1] - eigs_PRP[-1]) / delta

                    if abs(grad_ea) > 1e-10:
                        A_step = np.zeros(3)
                        A_step[a] = 0.01 * grad_ea
                        Q[e] = su2_exp(A_step) @ Q[e]
                        u, s, vh = np.linalg.svd(Q[e])
                        Q[e] = u @ vh

        # Final
        M_Q = build_M_operator(lat, Q, basis)
        R_Q = M_Q - M_I
        PRP = P.T @ R_Q @ P
        eigs_PRP = np.linalg.eigvalsh(PRP)
        print(f"    Final: max eig(P^T R P) = {eigs_PRP[-1]:.10f}")
        print(f"    All P^T R P eigs: {[f'{e:.6f}' for e in eigs_PRP]}")
        print()

if __name__ == '__main__':
    main()
