"""
Part A: Check abelian configs — are they pure gauge? Do they saturate λ_max = 4d?
Part B: Gradient ascent on λ_max(D(Q)) to find the worst-case Q.
Part C: Detailed eigenvalue spectrum analysis of D(Q) for different config classes.
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

# ====================== PART A: Abelian config analysis ======================

def part_a():
    np.random.seed(42)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)
    K_curl = build_K_curl(lat)

    print("="*70)
    print("PART A: Abelian (diagonal) configs — are they pure gauge?")
    print("="*70)
    print()

    for trial in range(5):
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            theta = np.random.uniform(0, 2*np.pi)
            Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])

        M_Q = build_M_operator(lat, Q, basis)
        eigs_M = np.linalg.eigvalsh(M_Q)
        D_Q = M_Q - K_curl
        eigs_D = np.linalg.eigvalsh(D_Q)

        # Check plaquette holonomies
        max_hol_dev = 0.0
        all_abelian_hol = True
        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T
            dev = np.linalg.norm(U_plaq - np.eye(2))
            max_hol_dev = max(max_hol_dev, dev)
            # Check if holonomy is diagonal
            offdiag = abs(U_plaq[0,1]) + abs(U_plaq[1,0])
            if offdiag > 1e-10:
                all_abelian_hol = False

        is_pure_gauge = max_hol_dev < 1e-8

        # For abelian configs, check the σ₃ direction
        # v_{x,μ} = (-1)^{|x|+μ} τ₃ is an eigenvector if all holonomies fix τ₃
        # i.e., if Ad_{transport}(τ₃) = τ₃
        # For diagonal Q, Ad_Q preserves τ₃ and rotates τ₁,τ₂
        # So the staggered τ₃ mode should still be an eigenvector

        print(f"  Abelian #{trial+1}:")
        print(f"    λ_max(M) = {eigs_M[-1]:.10f}")
        print(f"    max plaq dev from I = {max_hol_dev:.6f}")
        print(f"    pure gauge? {is_pure_gauge}")
        print(f"    all holonomies abelian? {all_abelian_hol}")
        print(f"    λ_max(D) = {eigs_D[-1]:.6f}, λ_min(D) = {eigs_D[0]:.6f}")
        print(f"    # positive D eigs: {np.sum(eigs_D > 1e-10)}")

        # Check if staggered τ₃ mode is eigenvector
        v_stag = np.zeros(lat.dim)
        for x in range(lat.n_sites):
            coords = lat.site_coords(x)
            parity = sum(coords) % 2
            sign = (-1)**parity
            for mu in range(d):
                e = lat.edge_index(x, mu)
                color_sign = (-1)**mu
                # τ₃ direction = index 2 in su(2) basis
                v_stag[3*e + 2] = sign * color_sign

        v_stag /= np.linalg.norm(v_stag)
        Mv = M_Q @ v_stag
        rayleigh = v_stag @ Mv
        residual = np.linalg.norm(Mv - rayleigh * v_stag) / np.linalg.norm(Mv)
        print(f"    Staggered τ₃ Rayleigh quotient: {rayleigh:.10f}")
        print(f"    Eigenvector residual: {residual:.2e}")
        print()

    # Also check: for abelian configs, what eigenvalues of D(Q) look like
    print("  Key insight: For abelian Q, the τ₃ sector is UNCHANGED (Ad preserves τ₃)")
    print("  but the τ₁,τ₂ sector eigenvalues shift (Ad rotates them)")
    print("  So D(Q) has 0 eigenvalues in the τ₃ sector and ±something in τ₁,τ₂ sector")
    print()

    # Verify: decompose D into τ₃ and τ₁τ₂ blocks
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        theta = np.random.uniform(0, 2*np.pi)
        Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])

    M_Q = build_M_operator(lat, Q, basis)
    D_Q = M_Q - K_curl

    # Extract τ₃ block (color index = 2, every 3rd row/col starting at 2)
    idx_3 = [3*e + 2 for e in range(lat.n_edges)]
    D_33 = D_Q[np.ix_(idx_3, idx_3)]
    eigs_33 = np.linalg.eigvalsh(D_33)
    print(f"  τ₃ block of D: max|eig| = {np.max(np.abs(eigs_33)):.2e}")

    # Extract τ₁τ₂ block
    idx_12 = []
    for e in range(lat.n_edges):
        idx_12.extend([3*e, 3*e+1])
    D_12 = D_Q[np.ix_(idx_12, idx_12)]
    eigs_12 = np.linalg.eigvalsh(D_12)
    print(f"  τ₁τ₂ block of D: max eig = {np.max(eigs_12):.6f}, min eig = {np.min(eigs_12):.6f}")

    # Check cross-blocks
    D_cross = D_Q[np.ix_(idx_3, idx_12)]
    print(f"  Cross-block (τ₃ vs τ₁τ₂): max|entry| = {np.max(np.abs(D_cross)):.2e}")

# ====================== PART B: Gradient ascent on λ_max(M(Q)) ======================

def part_b():
    np.random.seed(123)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)
    bound = 4 * d

    print()
    print("="*70)
    print("PART B: Gradient ascent on λ_max(M(Q))")
    print("="*70)
    print()
    print("Goal: Find Q that maximizes λ_max(M(Q)). Should plateau at 4d = 16.")
    print()

    n_starts = 5
    n_steps = 100
    step_size = 0.01

    for start in range(n_starts):
        # Random starting config
        Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
        for e in range(lat.n_edges):
            Q[e] = su2_near_identity(1.0)

        print(f"  Start #{start+1}:")
        t0 = time.time()

        for step in range(n_steps):
            M_Q = build_M_operator(lat, Q, basis)
            eigs, vecs = np.linalg.eigh(M_Q)
            lam_max = eigs[-1]
            v_max = vecs[:, -1]

            if step % 20 == 0 or step == n_steps - 1:
                print(f"    Step {step:3d}: λ_max = {lam_max:.8f} (gap to 4d = {bound - lam_max:.8f})")

            # Compute gradient via finite differences
            delta = 1e-5
            for e in range(lat.n_edges):
                # Perturb along each su(2) direction
                best_dir = np.zeros(3)
                for a in range(3):
                    A_vec = np.zeros(3)
                    A_vec[a] = delta
                    Q_pert = Q.copy()
                    Q_pert[e] = su2_exp(A_vec) @ Q[e]
                    M_pert = build_M_operator(lat, Q_pert, basis)
                    lam_pert = v_max @ M_pert @ v_max  # Rayleigh quotient
                    grad_a = (lam_pert - lam_max) / delta
                    best_dir[a] = grad_a

                # Step in gradient direction
                if np.linalg.norm(best_dir) > 1e-10:
                    A_step = step_size * best_dir
                    Q[e] = su2_exp(A_step) @ Q[e]
                    # Re-unitarize
                    u, s, vh = np.linalg.svd(Q[e])
                    Q[e] = u @ vh

        elapsed = time.time() - t0
        M_final = build_M_operator(lat, Q, basis)
        lam_final = np.linalg.eigvalsh(M_final)[-1]

        # Check if final config is pure gauge
        max_hol_dev = 0.0
        for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
            Q1 = Q[e1]
            Q12 = Q1 @ Q[e2]
            Q123inv = Q12 @ np.conj(Q[e3]).T
            U_plaq = Q123inv @ np.conj(Q[e4]).T
            dev = np.linalg.norm(U_plaq - np.eye(2))
            max_hol_dev = max(max_hol_dev, dev)

        print(f"    Final: λ_max = {lam_final:.10f}, gap = {bound - lam_final:.10f}")
        print(f"    Max plaq deviation = {max_hol_dev:.6f}")
        print(f"    Elapsed: {elapsed:.1f}s")
        print()

# ====================== PART C: D(Q) eigenvalue spectrum analysis ======================

def part_c():
    np.random.seed(456)
    basis = su2_basis()
    L, d = 2, 4
    lat = Lattice(L, d)
    K_curl = build_K_curl(lat)

    print()
    print("="*70)
    print("PART C: Eigenvalue spectrum of D(Q) = M(Q) - M(I)")
    print("="*70)
    print()

    # For a few representative configs, show full eigenvalue spectrum of D(Q)
    configs = [
        ("Near-I ε=0.01", lambda: gen_near_id(lat, 0.01)),
        ("Near-I ε=0.1", lambda: gen_near_id(lat, 0.1)),
        ("Near-I ε=0.5", lambda: gen_near_id(lat, 0.5)),
        ("Random Haar", lambda: gen_haar(lat)),
    ]

    for name, gen in configs:
        Q = gen()
        M_Q = build_M_operator(lat, Q, basis)
        D_Q = M_Q - K_curl
        eigs_D = np.sort(np.linalg.eigvalsh(D_Q))
        eigs_M = np.sort(np.linalg.eigvalsh(M_Q))

        print(f"  {name}:")
        print(f"    D(Q) eigenvalues: min={eigs_D[0]:.6f}, max={eigs_D[-1]:.6f}")
        print(f"    D(Q) trace = {np.sum(eigs_D):.2e}")
        print(f"    # positive: {np.sum(eigs_D > 1e-10)}, # negative: {np.sum(eigs_D < -1e-10)}, # zero: {np.sum(np.abs(eigs_D) < 1e-10)}")
        print(f"    M(Q) λ_max = {eigs_M[-1]:.8f}")
        print(f"    M(I) λ_max = 16.0")
        print(f"    Gap: 16 - λ_max(M(Q)) = {16 - eigs_M[-1]:.8f}")

        # Show how the trace of D splits
        trace_D = np.trace(D_Q)
        trace_M_Q = np.trace(M_Q)
        trace_K = np.trace(K_curl)
        print(f"    Tr(M(Q)) = {trace_M_Q:.4f}, Tr(K_curl) = {trace_K:.4f}, Tr(D) = {trace_D:.4f}")
        print()

def gen_near_id(lat, eps):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = su2_near_identity(eps)
    return Q

def gen_haar(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = random_su2()
    return Q

# ====================== Main ======================

if __name__ == '__main__':
    part_a()
    part_c()
    part_b()
