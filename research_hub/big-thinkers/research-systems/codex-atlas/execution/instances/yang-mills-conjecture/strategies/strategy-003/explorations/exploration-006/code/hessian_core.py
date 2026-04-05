"""
Core Hessian computation for lattice SU(2) Yang-Mills.
Consolidated from E002-E005 with all needed functions.

Key formulas:
- Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□)
- Cross-terms: H[(ep,a),(eq,b)] = -(β/N) sp sq Re Tr(L·iσa·mid·iσb·R)
- Color kernel F_{ab}(M,N) = Re Tr(iσa·M·iσb·N) = -2(β₀I+[β⃗×])R_M
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

def su2_exp(w_vec):
    """exp(Σ w_a iσ_a) for SU(2)."""
    theta = np.linalg.norm(w_vec)
    if theta < 1e-14:
        return np.eye(2, dtype=complex)
    W = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * W

def project_su2(M):
    """Project to SU(2) via polar decomposition."""
    U, s, Vh = np.linalg.svd(M)
    P = U @ Vh
    if np.real(np.linalg.det(P)) < 0:
        P = -P
    d = np.linalg.det(P)
    P /= np.sqrt(d)
    return P

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
                    s1 = self.shift(site, mu)
                    e2 = self.edge_index(s1, nu)
                    s2 = self.shift(site, nu)
                    e3 = self.edge_index(s2, mu)
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

def compute_hessian(lat, Q, beta=1.0, N=2):
    """Compute the full Hessian matrix H = D + C."""
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
                        H[3*ep+a, 3*eq+b] += val
                        H[3*eq+b, 3*ep+a] += val
    return H

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

def compute_per_plaquette_hessian(lat, Q, pidx, beta=1.0, N=2):
    """Compute the Hessian contribution H_□ from a single plaquette.
    Returns a sparse representation: dict of (row, col) -> value."""
    plaq = lat.plaquettes[pidx]
    ne = lat.nedges
    dim = 3 * ne
    H_plaq = np.zeros((dim, dim))

    U_plaq = plaquette_holonomy(Q, plaq)
    re_tr = np.real(np.trace(U_plaq))

    # Self-terms
    for (e, s) in plaq:
        for a in range(3):
            H_plaq[3*e+a, 3*e+a] += (beta/N) * re_tr

    # Cross-terms
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
                    H_plaq[3*ep+a, 3*eq+b] += val
                    H_plaq[3*eq+b, 3*ep+a] += val
    return H_plaq

def random_config(lat, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    return [random_su2(rng) for _ in range(lat.nedges)]

def flat_config(lat):
    return [np.eye(2, dtype=complex) for _ in range(lat.nedges)]

def anti_instanton_config(lat):
    """Anti-instanton: Q_mu = iσ_{mu mod 3}. Gives Re Tr(U_□) = -2."""
    Q = []
    for mu in range(lat.d):
        for _ in range(lat.nsites):
            Q.append(isigma[mu % 3].copy())
    return Q
