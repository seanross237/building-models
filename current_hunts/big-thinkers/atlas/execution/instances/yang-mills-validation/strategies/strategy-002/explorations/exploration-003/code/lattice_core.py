"""
Core lattice SU(2) Yang-Mills infrastructure for Exploration 003.
Adapted from E001 with optimizations for perturbation studies.

Conventions:
- SU(2), N=2, generators T_a = i σ_a / 2 for a=1,2,3
- Inner product: <X,Y> = -2 Tr(X Y), so |T_a|² = 1
- Wilson action: S(Q) = -(β/2) Σ_□ Re Tr(U_□)
- LEFT perturbation: Q → exp(ε v) Q
- L=2 hypercubic torus, d=4, periodic BC
"""

import numpy as np
from numpy.linalg import eigvalsh, eigh, norm, det
from scipy.linalg import expm
import time

# ===================== SU(2) Basics =====================

sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)

T = np.array([1j * sigma[a] / 2 for a in range(3)])

def su2_exp(v):
    """Exponential map: v ∈ R³ → exp(Σ v_a T_a) ∈ SU(2)."""
    X = sum(v[a] * T[a] for a in range(3))
    return expm(X)

def su2_exp_fast(v):
    """Fast exponential using Rodrigues formula for su(2)."""
    theta = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    X = sum(v[a] * T[a] for a in range(3))
    return np.eye(2, dtype=complex) * np.cos(theta/2) + (2*np.sin(theta/2)/theta) * X

def project_su2(U):
    """Project a 2×2 matrix to SU(2)."""
    d = det(U)
    U = U / np.sqrt(d)
    U = (U + np.linalg.inv(U).conj().T) / 2
    d = det(U)
    U = U / np.sqrt(d)
    return U

def haar_random_su2():
    """Sample Haar-random SU(2) element."""
    x = np.random.randn(4)
    x = x / norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ], dtype=complex)

def adjoint_matrix(Q):
    """3×3 adjoint representation matrix."""
    Qinv = np.linalg.inv(Q)
    R = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            R[a, b] = -2 * np.trace(T[a] @ Q @ T[b] @ Qinv).real
    return R


# ===================== Lattice Setup =====================

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_links = self.n_sites * d
        self.n_dof = self.n_links * 3

        self.coords = np.array(np.unravel_index(
            np.arange(self.n_sites), [L]*d
        )).T

        self._coord_to_idx = {}
        for i in range(self.n_sites):
            self._coord_to_idx[tuple(self.coords[i])] = i

        self._plaquettes = None

    def site_index(self, coords):
        c = tuple(c % self.L for c in coords)
        return self._coord_to_idx[c]

    def neighbor(self, site, mu):
        c = list(self.coords[site])
        c[mu] = (c[mu] + 1) % self.L
        return self.site_index(c)

    def neighbor_back(self, site, mu):
        c = list(self.coords[site])
        c[mu] = (c[mu] - 1) % self.L
        return self.site_index(c)

    def link_index(self, site, mu):
        return site * self.d + mu

    def plaquettes(self):
        if self._plaquettes is not None:
            return self._plaquettes
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.neighbor(x, mu)
                    x_nu = self.neighbor(x, nu)
                    e1 = self.link_index(x, mu)
                    e2 = self.link_index(x_mu, nu)
                    e3 = self.link_index(x_nu, mu)
                    e4 = self.link_index(x, nu)
                    plaq_list.append({
                        'edges': [e1, e2, e3, e4],
                        'site': x, 'mu': mu, 'nu': nu
                    })
        self._plaquettes = plaq_list
        return plaq_list


# ===================== Wilson Action =====================

def wilson_action(Q, lattice, beta):
    S = 0.0
    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']
        U_plaq = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])
        S -= (beta / 2) * np.trace(U_plaq).real
    return S


# ===================== Hessian Computations =====================

def compute_hessian_fd(Q, lattice, beta, h=1e-4):
    """Finite-difference Hessian (LEFT perturbation)."""
    n = lattice.n_dof
    H = np.zeros((n, n))
    S0 = wilson_action(Q, lattice, beta)

    def perturb(Q_orig, link_idx, color_idx, eps):
        Q_new = Q_orig.copy()
        v = np.zeros(3)
        v[color_idx] = eps
        Q_new[link_idx] = su2_exp(v) @ Q_orig[link_idx]
        return Q_new

    S_plus = np.zeros(n)
    S_minus = np.zeros(n)
    for i in range(n):
        e_i = i // 3
        a_i = i % 3
        S_plus[i] = wilson_action(perturb(Q, e_i, a_i, h), lattice, beta)
        S_minus[i] = wilson_action(perturb(Q, e_i, a_i, -h), lattice, beta)

    for i in range(n):
        H[i, i] = (S_plus[i] - 2*S0 + S_minus[i]) / h**2

    for i in range(n):
        e_i = i // 3
        a_i = i % 3
        for j in range(i+1, n):
            e_j = j // 3
            a_j = j % 3
            Q_pp = perturb(perturb(Q, e_i, a_i, h), e_j, a_j, h)
            Q_pm = perturb(perturb(Q, e_i, a_i, h), e_j, a_j, -h)
            Q_mp = perturb(perturb(Q, e_i, a_i, -h), e_j, a_j, h)
            Q_mm = perturb(perturb(Q, e_i, a_i, -h), e_j, a_j, -h)
            H[i, j] = (wilson_action(Q_pp, lattice, beta) - wilson_action(Q_pm, lattice, beta)
                       - wilson_action(Q_mp, lattice, beta) + wilson_action(Q_mm, lattice, beta)) / (4*h**2)
            H[j, i] = H[i, j]
    return H


def compute_hessian_formula(Q, lattice, beta):
    """B² formula Hessian."""
    N = 2
    n = lattice.n_dof
    M = np.zeros((n, n))

    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3])
        P4 = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])

        R2 = adjoint_matrix(P2)
        R3 = adjoint_matrix(P3)
        R4 = adjoint_matrix(P4)

        B_mat = np.zeros((3, n))
        for a in range(3):
            B_mat[a, e1*3 + a] += 1.0
        for a in range(3):
            for b in range(3):
                B_mat[a, e2*3 + b] += R2[a, b]
                B_mat[a, e3*3 + b] -= R3[a, b]
                B_mat[a, e4*3 + b] -= R4[a, b]

        M += B_mat.T @ B_mat

    return (beta / (2 * N)) * M


def compute_lmax_actual(Q, lattice, beta, h=1e-4):
    """Just compute λ_max(H_actual(Q))."""
    H = compute_hessian_fd(Q, lattice, beta, h)
    H = (H + H.T) / 2
    return eigvalsh(H)[-1]


def compute_lmax_and_evecs(Q, lattice, beta, h=1e-4, n_top=12):
    """Compute top eigenvalues and eigenvectors of H_actual."""
    H = compute_hessian_fd(Q, lattice, beta, h)
    H = (H + H.T) / 2
    evals, evecs = eigh(H)
    # Return top n_top
    return evals[-n_top:], evecs[:, -n_top:], H


def apply_gauge_transform(Q, lattice, g):
    """Apply gauge transformation: Q_{x,mu} -> g(x) Q_{x,mu} g(x+mu)^{-1}."""
    Q_new = Q.copy()
    for x in range(lattice.n_sites):
        for mu in range(lattice.d):
            y = lattice.neighbor(x, mu)
            link_idx = lattice.link_index(x, mu)
            Q_new[link_idx] = g[x] @ Q[link_idx] @ np.linalg.inv(g[y])
    return Q_new


def perturb_config(Q, delta_Q, t):
    """Perturb Q → exp(t * delta_Q_e) Q_e for each link e.
    delta_Q: array of shape (n_links, 3) giving su(2) coefficients.
    """
    Q_new = Q.copy()
    for e in range(len(Q)):
        v = t * delta_Q[e]
        Q_new[e] = su2_exp(v) @ Q[e]
    return Q_new


def random_su2_config(lattice):
    return np.array([haar_random_su2() for _ in range(lattice.n_links)])


def identity_config(lattice):
    return np.array([np.eye(2, dtype=complex) for _ in range(lattice.n_links)])
