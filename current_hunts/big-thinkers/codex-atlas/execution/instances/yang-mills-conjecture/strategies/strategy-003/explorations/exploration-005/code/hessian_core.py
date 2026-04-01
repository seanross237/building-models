"""
Core Hessian computation for lattice SU(2) Yang-Mills.
Includes: lattice setup, Hessian assembly, cross-term C(Q) extraction,
and the NEW closed-form SVD formula for the color kernel F.

From E002-E004 (verified):
- Self-terms: H[(e,a),(e,b)] = (beta/N) * delta_{ab} * sum_{box} Re Tr(U_box)
- Cross-terms: H[(ep,a),(eq,b)] = -(beta/N)*sp*sq*Re Tr(L*iσa*mid*iσb*R)
"""

import numpy as np
from itertools import product as iterproduct

# Pauli matrices
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
isigma = [1j * s for s in sigma]

def random_su2(rng=None):
    if rng is None:
        rng = np.random.default_rng()
    v = rng.normal(size=4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

def su2_inv(U):
    return U.conj().T

def su2_to_quat(U):
    """Extract quaternion (w0, w1, w2, w3) from SU(2) matrix U = w0*I + i*(w1*s1+w2*s2+w3*s3)."""
    w0 = np.real(U[0,0] + U[1,1]) / 2
    w1 = np.imag(U[0,1] + U[1,0]) / 2
    w2 = np.real(U[0,1] - U[1,0]) / 2
    w3 = np.imag(U[0,0] - U[1,1]) / 2
    return w0, np.array([w1, w2, w3])

def adjoint_so3(U):
    """Compute the SO(3) adjoint representation of SU(2) element U.
    R_{ab} such that U (iσ_b) U^{-1} = sum_a R_{ab} (iσ_a).
    """
    R = np.zeros((3, 3))
    for b in range(3):
        rotated = U @ isigma[b] @ su2_inv(U)
        for a in range(3):
            R[a, b] = np.real(np.trace(rotated @ su2_inv(isigma[a]))) / 2
            # Tr(iσ_a * iσ_b) = -2 δ_{ab}, so coeff = Tr(rotated * (-iσ_a)) / 2
    # Cleaner: R[a,b] = -Re Tr(iσ_a * rotated) / 2? Let me use direct formula
    R2 = np.zeros((3, 3))
    for b in range(3):
        rotated = U @ isigma[b] @ su2_inv(U)
        for a in range(3):
            # rotated = sum_c R[c,b] iσ_c
            # Tr((-iσ_a) * rotated) = sum_c R[c,b] Tr(-iσ_a * iσ_c) = sum_c R[c,b] * 2δ_{ac} = 2 R[a,b]
            R2[a, b] = np.real(np.trace((-isigma[a]) @ rotated)) / 2
    return R2

def cross_product_matrix(v):
    """Return 3x3 antisymmetric matrix [v×] such that [v×]w = v × w."""
    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])

def color_kernel_direct(M, N):
    """Compute F_{ab}(M,N) = Re Tr(iσ_a * M * iσ_b * N) directly."""
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ M @ isigma[b] @ N))
    return F

def color_kernel_formula(M, N):
    """Compute F using the closed-form: F = -2(β₀I + [β⃗×]) R_M
    where MN = β₀I + iβ⃗·σ, R_M = adjoint SO(3) rep of M.
    """
    W = M @ N
    beta0, beta_vec = su2_to_quat(W)
    R_M = adjoint_so3(M)
    beta_cross = cross_product_matrix(beta_vec)
    P = beta0 * np.eye(3) + beta_cross
    return -2 * P @ R_M

class Lattice:
    def __init__(self, d, L):
        self.d = d
        self.L = L
        self.nsites = L**d
        self.nedges = d * self.nsites
        self.sites = list(iterproduct(range(L), repeat=d))
        self.site_index = {s: i for i, s in enumerate(self.sites)}
        self._build_plaquettes()

    def shift(self, site, mu, forward=True):
        s = list(site)
        s[mu] = (s[mu] + (1 if forward else -1)) % self.L
        return tuple(s)

    def edge_index(self, site, mu):
        return mu * self.nsites + self.site_index[site]

    def _build_plaquettes(self):
        self.plaquettes = []
        self.edge_plaquettes = {}
        for site in self.sites:
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    e1 = self.edge_index(site, mu)
                    s1_site = self.shift(site, mu)
                    e2 = self.edge_index(s1_site, nu)
                    s2_site = self.shift(site, nu)
                    e3 = self.edge_index(s2_site, mu)
                    e4 = self.edge_index(site, nu)
                    plaq = [(e1, +1), (e2, +1), (e3, -1), (e4, -1)]
                    self.plaquettes.append(plaq)
                    for (e, s) in plaq:
                        if e not in self.edge_plaquettes:
                            self.edge_plaquettes[e] = []
                        self.edge_plaquettes[e].append(len(self.plaquettes) - 1)
        self.nplaq = len(self.plaquettes)

def get_link(Q, e, s):
    return Q[e] if s == +1 else su2_inv(Q[e])

def plaquette_holonomy(Q, plaq):
    U = np.eye(2, dtype=complex)
    for (e, s) in plaq:
        U = U @ get_link(Q, e, s)
    return U

def compute_cross_term(lat, Q, beta=1.0, N=2):
    """Compute the cross-term matrix C(Q) and the 3x3 color blocks G_{ef}."""
    ne = lat.nedges
    dim = 3 * ne
    C = np.zeros((dim, dim))

    # Also store per-edge-pair color blocks
    G_blocks = {}  # (e1, e2) -> 3x3 matrix

    for pidx, plaq in enumerate(lat.plaquettes):
        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ get_link(Q, *edges_list[k])

                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ get_link(Q, *edges_list[k])

                R = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R = R @ get_link(Q, *edges_list[k])

                # F_{ab} = Re Tr(iσ_a * L * ... ) but the actual trace argument
                # as coded: Re Tr(L * iσ_a * mid * iσ_b * R)
                # = Re Tr(iσ_a * mid * iσ_b * R * L)  [cyclic]
                # So in my formula: M=mid, N=R*L

                F_block = np.zeros((3, 3))
                for a in range(3):
                    for b in range(3):
                        F_block[a, b] = np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                        )

                contrib = -(beta/N) * sp * sq * F_block

                key = (min(ep, eq), max(ep, eq))
                if key not in G_blocks:
                    G_blocks[key] = np.zeros((3, 3))

                for a in range(3):
                    for b in range(3):
                        C[3*ep+a, 3*eq+b] += contrib[a, b]
                        C[3*eq+b, 3*ep+a] += contrib[a, b]
                        if ep <= eq:
                            G_blocks[key][a, b] += contrib[a, b]
                        else:
                            G_blocks[key][b, a] += contrib[a, b]

    return C, G_blocks

def compute_hessian_decomposed(lat, Q, beta=1.0, N=2):
    """Compute D (diagonal) and C (cross-term) separately."""
    ne = lat.nedges
    dim = 3 * ne
    D = np.zeros(dim)
    C = np.zeros((dim, dim))

    for pidx, plaq in enumerate(lat.plaquettes):
        U_plaq = plaquette_holonomy(Q, plaq)
        re_tr = np.real(np.trace(U_plaq))
        for (e, s) in plaq:
            for a in range(3):
                D[3*e+a] += (beta/N) * re_tr

        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]
                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ get_link(Q, *edges_list[k])
                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ get_link(Q, *edges_list[k])
                R = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R = R @ get_link(Q, *edges_list[k])
                for a in range(3):
                    for b in range(3):
                        val = -(beta/N) * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                        )
                        C[3*ep+a, 3*eq+b] += val
                        C[3*eq+b, 3*ep+a] += val
    return D, C

def random_config(lat, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    return [random_su2(rng) for _ in range(lat.nedges)]

def flat_config(lat):
    return [np.eye(2, dtype=complex) for _ in range(lat.nedges)]

if __name__ == "__main__":
    # Verify the closed-form SVD formula
    print("=== Verifying F = -2(β₀I + [β⃗×])R_M formula ===")
    rng = np.random.default_rng(42)
    max_err = 0
    for trial in range(100):
        M = random_su2(rng)
        N = random_su2(rng)
        F_direct = color_kernel_direct(M, N)
        F_formula = color_kernel_formula(M, N)
        err = np.max(np.abs(F_direct - F_formula))
        max_err = max(max_err, err)
    print(f"Max error over 100 random (M,N) pairs: {max_err:.2e}")

    # Verify SVD structure
    print("\n=== SVD structure of F ===")
    for trial in range(5):
        M = random_su2(rng)
        N = random_su2(rng)
        F = color_kernel_direct(M, N)
        svs = np.linalg.svd(F, compute_uv=False)
        W = M @ N
        beta0, beta_vec = su2_to_quat(W)
        print(f"  SVs: {svs[0]:.4f}, {svs[1]:.4f}, {svs[2]:.4f} | "
              f"|β₀|={abs(beta0):.4f}, predicted SVs: 2, 2, {2*abs(beta0):.4f}")

    # Check flat config
    print("\n=== Flat config check ===")
    lat = Lattice(4, 2)
    Q = flat_config(lat)
    D, C = compute_hessian_decomposed(lat, Q)
    evals_C = np.linalg.eigvalsh(C)
    print(f"d=4, L=2: ||C_flat|| = {max(abs(evals_C[0]), abs(evals_C[-1])):.4f}")
    print(f"  Expected: 2(d+1) = {2*(4+1)}")
    print(f"  C eigenvalue range: [{evals_C[0]:.4f}, {evals_C[-1]:.4f}]")
