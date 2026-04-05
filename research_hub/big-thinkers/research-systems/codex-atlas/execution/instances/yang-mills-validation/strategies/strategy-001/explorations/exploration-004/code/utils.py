"""
Shared utilities for Yang-Mills H_norm exploration.
LEFT perturbation convention: Q_e -> exp(t*v_e) @ Q_e
P3 = Q1 @ Q2 @ Q3.conj().T  (includes Q3 inverse)
"""
import numpy as np
from itertools import product as iproduct
import scipy.sparse.linalg as spla
import scipy.linalg as la

# SU(2) generators (anti-Hermitian: tau_a = i*sigma_a/2)
sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = np.array([[0, 1], [1, 0]])
sigma[1] = np.array([[0, -1j], [1j, 0]])
sigma[2] = np.array([[1, 0], [0, -1]])
tau = np.array([1j * sigma[a] / 2 for a in range(3)])  # shape (3,2,2)


def site_index(x, L):
    idx = 0
    for i, xi in enumerate(x):
        idx += (int(xi) % L) * (L ** i)
    return idx


def shift(x, mu, L, sign=1):
    xnew = list(x)
    xnew[mu] = (xnew[mu] + sign) % L
    return tuple(xnew)


def link_index(x, mu, L, d):
    return site_index(x, L) * d + mu


def build_plaquette_list(L, d):
    """Build list of plaquettes. Each plaquette is 4 (link_idx, sign) pairs."""
    plaquettes = []
    for x in iproduct(range(L), repeat=d):
        for mu in range(d):
            for nu in range(mu + 1, d):
                links = [
                    (link_index(x, mu, L, d), +1),
                    (link_index(shift(x, mu, L), nu, L, d), +1),
                    (link_index(shift(x, nu, L), mu, L, d), -1),
                    (link_index(x, nu, L, d), -1),
                ]
                plaquettes.append(links)
    return plaquettes


def build_plaquette_list_by_link(plaq_list, n_links):
    """For each link, list of (plaquette, position_in_plaq) pairs."""
    by_link = [[] for _ in range(n_links)]
    for pi, plaq in enumerate(plaq_list):
        for pos, (link_idx, sign) in enumerate(plaq):
            by_link[link_idx].append((pi, pos))
    return by_link


def adjoint_rep(g):
    """Adjoint representation: R[c,a] = -2 Re Tr(tau_c g tau_a g.dag)"""
    R = np.zeros((3, 3))
    for a in range(3):
        for c in range(3):
            R[c, a] = -2.0 * np.real(np.trace(tau[c] @ g @ tau[a] @ g.conj().T))
    return R


def su2_exp(M):
    """Matrix exponential for 2x2 anti-Hermitian matrix (su(2) element)."""
    theta_sq = -2.0 * np.real(np.trace(M @ M))
    if theta_sq < 1e-20:
        return np.eye(2, dtype=complex) + M + M @ M / 2.0 + M @ M @ M / 6.0
    theta = np.sqrt(theta_sq)
    return np.cos(theta / 2.0) * np.eye(2, dtype=complex) + (2.0 / theta) * np.sin(theta / 2.0) * M


def random_su2():
    """Random Haar-distributed SU(2) element."""
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return (a[0] * np.eye(2, dtype=complex)
            + 1j * a[1] * sigma[0]
            + 1j * a[2] * sigma[1]
            + 1j * a[3] * sigma[2])


def wilson_action(U, plaq_list, beta, N):
    """S = -(beta/N) sum_plaq Re Tr(U_plaq)"""
    S = 0.0
    for plaq in plaq_list:
        e1, s1 = plaq[0]; e2, s2 = plaq[1]; e3, s3 = plaq[2]; e4, s4 = plaq[3]
        U_plaq = U[e1] @ U[e2] @ U[e3].conj().T @ U[e4].conj().T
        S += np.real(np.trace(U_plaq))
    return -beta / N * S


def compute_partial_holonomies(U1, U2, U3, U4, N):
    """Compute LEFT partial holonomies for a plaquette."""
    P1 = np.eye(N, dtype=complex)
    P2 = U1.copy()
    P3 = U1 @ U2 @ U3.conj().T          # includes Q3 inverse
    P4 = P3 @ U4.conj().T               # = U_plaq
    return P1, P2, P3, P4


def hessian_matvec(v_flat, U, plaq_list, beta, N, n_links, n_gen):
    """Compute H @ v without forming H explicitly (matrix-free)."""
    prefactor = beta / (2.0 * N)
    result = np.zeros(n_links * n_gen, dtype=float)
    r = result.reshape(n_links, n_gen)
    v = v_flat.reshape(n_links, n_gen)

    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs = [plaq[k][1] for k in range(4)]
        Us = [U[e_idx[k]] for k in range(4)]
        P1, P2, P3, P4 = compute_partial_holonomies(Us[0], Us[1], Us[2], Us[3], N)
        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                r[e_idx[ie]] += block @ v[e_idx[je]]
    return result


def build_hessian_LEFT(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """Build full Hessian matrix using LEFT B_square formula."""
    H = np.zeros((n_dof, n_dof))
    prefactor = beta / (2.0 * N)

    for plaq in plaq_list:
        e_idx = [plaq[k][0] for k in range(4)]
        signs = [plaq[k][1] for k in range(4)]
        Us = [U[e_idx[k]] for k in range(4)]
        P1, P2, P3, P4 = compute_partial_holonomies(Us[0], Us[1], Us[2], Us[3], N)
        Rs = [adjoint_rep(P) for P in [P1, P2, P3, P4]]

        for ie in range(4):
            for je in range(4):
                block = prefactor * signs[ie] * signs[je] * Rs[ie].T @ Rs[je]
                ei, ej = e_idx[ie], e_idx[je]
                H[ei * n_gen:(ei + 1) * n_gen, ej * n_gen:(ej + 1) * n_gen] += block
    return H


def lambda_max_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """Compute lambda_max using dense Hessian (for small lattices)."""
    H = build_hessian_LEFT(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    evals = la.eigvalsh(H)
    return np.max(evals)


def lambda_max_sparse(U, plaq_list, beta, N, n_links, n_gen, tol=1e-8, maxiter=1000):
    """Compute lambda_max using matrix-free ARPACK eigsh."""
    n_dof = n_links * n_gen

    def matvec(v):
        return hessian_matvec(v, U, plaq_list, beta, N, n_links, n_gen)

    A = spla.LinearOperator((n_dof, n_dof), matvec=matvec, dtype=float)
    try:
        vals, vecs = spla.eigsh(A, k=1, which='LM', tol=tol, maxiter=maxiter)
        return float(vals[0]), vecs[:, 0]
    except spla.ArpackNoConvergence as e:
        if len(e.eigenvalues) > 0:
            return float(np.max(e.eigenvalues)), e.eigenvectors[:, 0]
        raise


def lambda_max_and_vec_dense(U, plaq_list, beta, N, n_dof, n_links, n_gen):
    """Return (lambda_max, eigenvector) using dense Hessian."""
    H = build_hessian_LEFT(U, plaq_list, beta, N, n_dof, n_links, n_gen)
    evals, evecs = la.eigh(H)
    idx = np.argmax(evals)
    return evals[idx], evecs[:, idx]


def h_norm(lmax, beta, d=4, N=2):
    """H_norm = lambda_max / (4 * d * (N^2-1) * beta) ... but use 48 as prior work."""
    # From prior work: H_norm = lambda_max / (48 * beta) for d=4, N=2
    # At Q=I: lambda_max = 4*beta => H_norm = 4/(48) = 1/12
    return lmax / (48.0 * beta)


def gibbs_sample(U, plaq_list, beta, N, n_links, n_steps=1000):
    """Run Metropolis updates to sample from Gibbs measure."""
    U = U.copy()
    S = wilson_action(U, plaq_list, beta, N)
    accepted = 0
    for _ in range(n_steps):
        e = np.random.randint(n_links)
        U_new = random_su2()
        U_tmp = U.copy()
        U_tmp[e] = U_new
        S_new = wilson_action(U_tmp, plaq_list, beta, N)
        dS = S_new - S
        if np.random.rand() < np.exp(-dS):
            U[e] = U_new
            S = S_new
            accepted += 1
    return U, accepted / n_steps
