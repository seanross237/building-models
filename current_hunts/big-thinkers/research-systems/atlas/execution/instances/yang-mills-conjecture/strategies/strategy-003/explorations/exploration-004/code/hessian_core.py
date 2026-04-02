"""
Core Hessian computation for lattice SU(2) Yang-Mills.
Copied from E003 with optimizations for adversarial search.

Formula (verified in E002):
- Self-terms: H[(e,a),(e,b)] = (beta/N) * delta_{ab} * sum_{box containing e} Re Tr(U_box)
- Cross-terms: H[(ep,a),(eq,b)] = -(beta/N) * sp * sq * Re Tr(Lp * i*sigma_a * mid_pq * i*sigma_b * Rq)
"""

import numpy as np
from itertools import product

# Pauli matrices
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
isigma = [1j * s for s in sigma]  # i*sigma_a basis of su(2)

def random_su2(rng=None):
    """Random SU(2) matrix from Haar measure."""
    if rng is None:
        rng = np.random.default_rng()
    v = rng.normal(size=4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*b, c + 1j*d], [-c + 1j*d, a - 1j*b]])

def su2_inv(U):
    return U.conj().T

def su2_exp(w_vec):
    """exp(sum w_a * i*sigma_a) for SU(2). w_vec is 3-vector."""
    theta = np.linalg.norm(w_vec)
    if theta < 1e-14:
        return np.eye(2, dtype=complex)
    w = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * w

class Lattice:
    """d-dimensional periodic lattice of size L."""
    def __init__(self, d, L):
        self.d = d
        self.L = L
        self.nsites = L**d
        self.nedges = d * self.nsites
        self.sites = list(product(range(L), repeat=d))
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
        self.edge_plaquettes = {}  # edge -> list of plaquette indices

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
    """Get Q_e if s=+1, Q_e^{-1} if s=-1."""
    return Q[e] if s == +1 else su2_inv(Q[e])

def plaquette_holonomy(Q, plaq):
    U = np.eye(2, dtype=complex)
    for (e, s) in plaq:
        U = U @ get_link(Q, e, s)
    return U

def compute_hessian(lat, Q, beta=1.0, N=2):
    """Compute the full Hessian matrix."""
    ne = lat.nedges
    dim = 3 * ne
    H = np.zeros((dim, dim))

    for pidx, plaq in enumerate(lat.plaquettes):
        U_plaq = plaquette_holonomy(Q, plaq)
        re_tr = np.real(np.trace(U_plaq))

        # Self-terms
        for (e, s) in plaq:
            for a in range(3):
                H[3*e+a, 3*e+a] += (beta/N) * re_tr

        # Cross-terms
        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                # L_p = product of slots 0..p
                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ get_link(Q, *edges_list[k])

                # mid = product of slots p+1..q-1
                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ get_link(Q, *edges_list[k])

                # R = product of slots q+1..3
                R = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R = R @ get_link(Q, *edges_list[k])

                for a in range(3):
                    for b in range(3):
                        val = -(beta/N) * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                        )
                        H[3*ep+a, 3*eq+b] += val
                        H[3*eq+b, 3*ep+a] += val

    return H

def compute_hessian_decomposed(lat, Q, beta=1.0, N=2):
    """Compute D (self-term diagonal) and C (cross-term) separately."""
    ne = lat.nedges
    dim = 3 * ne
    D = np.zeros(dim)  # diagonal
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

def action_value(lat, Q, beta=1.0, N=2):
    S = 0.0
    for plaq in lat.plaquettes:
        U = plaquette_holonomy(Q, plaq)
        S -= (beta/N) * np.real(np.trace(U))
    return S

def project_su2(M):
    """Project a 2x2 matrix to SU(2) via polar decomposition."""
    U, s, Vh = np.linalg.svd(M)
    P = U @ Vh
    if np.real(np.linalg.det(P)) < 0:
        P = -P
    # Ensure det = 1
    d = np.linalg.det(P)
    P /= np.sqrt(d)
    return P
