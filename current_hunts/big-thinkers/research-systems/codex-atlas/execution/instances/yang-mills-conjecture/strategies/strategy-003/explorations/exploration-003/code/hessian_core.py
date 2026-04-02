"""
Core Hessian computation for lattice SU(2) Yang-Mills.
Provides: lattice setup, plaquette enumeration, Hessian assembly, eigenvalue computation.

Based on the verified formula from E002:
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
        """Edge from site in direction mu."""
        return mu * self.nsites + self.site_index[site]

    def _build_plaquettes(self):
        """Build all plaquettes. Each is (e1,s1, e2,s2, e3,s3, e4,s4)
        where e_i is edge index and s_i is sign (+1 forward, -1 backward)."""
        self.plaquettes = []
        self.edge_plaquettes = {}  # edge -> list of plaquettes containing it

        for site in self.sites:
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    # Plaquette: site->mu, site+mu->nu, site+nu->mu (backward), site->nu (backward)
                    e1 = self.edge_index(site, mu)
                    s1_site = self.shift(site, mu)
                    e2 = self.edge_index(s1_site, nu)
                    s2_site = self.shift(site, nu)
                    e3 = self.edge_index(s2_site, mu)  # backward
                    e4 = self.edge_index(site, nu)      # backward

                    plaq = [(e1, +1), (e2, +1), (e3, -1), (e4, -1)]
                    self.plaquettes.append(plaq)

                    for (e, s) in plaq:
                        if e not in self.edge_plaquettes:
                            self.edge_plaquettes[e] = []
                        self.edge_plaquettes[e].append(len(self.plaquettes) - 1)

        self.nplaq = len(self.plaquettes)

def plaquette_holonomy(Q, plaq):
    """Compute holonomy U_box = Q1 Q2 Q3^{-1} Q4^{-1}."""
    U = np.eye(2, dtype=complex)
    for (e, s) in plaq:
        if s == +1:
            U = U @ Q[e]
        else:
            U = U @ su2_inv(Q[e])
    return U

def compute_hessian(lat, Q, beta=1.0, N=2):
    """Compute the full Hessian matrix of the Wilson action.

    Returns: (3*nedges) x (3*nedges) symmetric matrix.
    Index (e,a) maps to 3*e + a.
    """
    ne = lat.nedges
    dim = 3 * ne
    H = np.zeros((dim, dim))

    for pidx, plaq in enumerate(lat.plaquettes):
        U_plaq = plaquette_holonomy(Q, plaq)
        re_tr = np.real(np.trace(U_plaq))

        # Self-terms: for each edge in the plaquette
        for (e, s) in plaq:
            for a in range(3):
                H[3*e+a, 3*e+a] += (beta/N) * re_tr

        # Cross-terms: for each pair of slots (p < q) in the plaquette
        edges_list = [(e, s) for (e, s) in plaq]

        for p_idx in range(4):
            for q_idx in range(p_idx+1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                # Compute L_p, mid_{pq}, R_q
                # L_p = product of Q's for slots 0..p (inclusive)
                # R_q = product of Q's for slots q+1..3
                # mid = product of Q's for slots p+1..q-1

                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    ek, sk = edges_list[k]
                    L = L @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    ek, sk = edges_list[k]
                    mid = mid @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

                R = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    ek, sk = edges_list[k]
                    R = R @ (Q[ek] if sk == +1 else su2_inv(Q[ek]))

                for a in range(3):
                    for b in range(3):
                        val = -(beta/N) * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                        )
                        H[3*ep+a, 3*eq+b] += val
                        H[3*eq+b, 3*ep+a] += val

    return H

def compute_gershgorin_bounds(H):
    """Compute Gershgorin upper bound for each row."""
    n = H.shape[0]
    bounds = np.zeros(n)
    for i in range(n):
        bounds[i] = H[i,i] + np.sum(np.abs(H[i,:])) - np.abs(H[i,i])
    return bounds

def random_config(lat, rng=None):
    """Generate random SU(2) config."""
    if rng is None:
        rng = np.random.default_rng()
    return [random_su2(rng) for _ in range(lat.nedges)]

def flat_config(lat):
    """Flat config: all links = I."""
    return [np.eye(2, dtype=complex) for _ in range(lat.nedges)]

def flat_config_z2(lat):
    """Z2 flat config: all links = i*sigma_3."""
    return [1j * sigma[2] for _ in range(lat.nedges)]

def action_value(lat, Q, beta=1.0, N=2):
    """Wilson action value."""
    S = 0.0
    for plaq in lat.plaquettes:
        U = plaquette_holonomy(Q, plaq)
        S -= (beta/N) * np.real(np.trace(U))
    return S

if __name__ == "__main__":
    # Quick test: verify Hessian at flat config
    lat = Lattice(2, 2)
    Q = flat_config(lat)
    H = compute_hessian(lat, Q)
    evals = np.linalg.eigvalsh(H)
    print(f"d=2, L=2: flat config, max eigenvalue = {evals[-1]:.6f}")
    print(f"  Expected: 4d = {4*2} (in isigma basis)")
    print(f"  Min eigenvalue = {evals[0]:.6f}")
    print(f"  Symmetric: {np.allclose(H, H.T)}")

    lat4 = Lattice(4, 2)
    Q4 = flat_config(lat4)
    H4 = compute_hessian(lat4, Q4)
    evals4 = np.linalg.eigvalsh(H4)
    print(f"\nd=4, L=2: flat config, max eigenvalue = {evals4[-1]:.6f}")
    print(f"  Expected: 4d = {4*4}")
