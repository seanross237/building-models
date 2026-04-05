"""
Exploration 006: Detailed eigenvector analysis for all d.
Key insight: max eigenvectors at Q=I have the form v_{x,mu} = c_mu * (-1)^|x|
with c satisfying sum_mu c_mu = 0.
"""

import numpy as np
from itertools import product

def get_sites(d, L=2):
    return list(product(range(L), repeat=d))

def site_to_idx(x, L=2):
    idx = 0
    for xi in x:
        idx = idx * L + xi
    return idx

def link_idx(x, mu, d, L=2):
    return site_to_idx(x, L) * d + mu

def shift_site(x, mu, L=2):
    x = list(x)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

def build_M_identity(d, L=2):
    """Build geometric Hessian M(I) = sum_plaq b_plaq b_plaq^T"""
    sites = get_sites(d, L)
    n_links = d * (L**d)
    M = np.zeros((n_links, n_links))
    for x in sites:
        for mu in range(d):
            for nu in range(mu+1, d):
                x_mu = shift_site(x, mu, L)
                x_nu = shift_site(x, nu, L)
                b = np.zeros(n_links)
                b[link_idx(x,    mu, d, L)] += 1.0
                b[link_idx(x_mu, nu, d, L)] += 1.0
                b[link_idx(x_nu, mu, d, L)] -= 1.0
                b[link_idx(x,    nu, d, L)] -= 1.0
                M += np.outer(b, b)
    return M

def rayleigh_quotient(M, v):
    """Compute Rayleigh quotient v^T M v / v^T v"""
    return np.dot(v, M @ v) / np.dot(v, v)

def analyze_half_staggered_mode(d, L=2, c_vec=None):
    """
    Test the mode v_{x,mu} = c_mu * (-1)^|x|.
    If c_vec is None, use the max eigenvec.
    Returns (rayleigh_quotient, is_eigvec).
    """
    sites = get_sites(d, L)
    n_links = d * (L**d)
    M = build_M_identity(d, L)

    if c_vec is None:
        # Use c = (d-1, -1, -1, ..., -1) which has sum = 0
        c_vec = np.array([-1.0] * d)
        c_vec[0] = d - 1.0

    # Normalize c_vec check
    c_sum = sum(c_vec)
    print(f"  c = {c_vec}, sum(c) = {c_sum:.6f}")

    v = np.zeros(n_links)
    for x in sites:
        x_sum = sum(x)
        sign = (-1)**x_sum
        for mu in range(d):
            v[link_idx(x, mu, d, L)] = c_vec[mu] * sign

    rq = rayleigh_quotient(M, v)
    Mv = M @ v
    residual = Mv - rq * v
    is_eigvec = np.linalg.norm(residual) / np.linalg.norm(v) < 1e-8

    return rq, is_eigvec

def analytical_formula(d, c_vec):
    """
    Analytical Rayleigh quotient for v_{x,mu} = c_mu * (-1)^|x|.
    Q(c) = 4 * sum_{mu<nu} (c_mu - c_nu)^2 / sum_mu c_mu^2
    = 4 * [d * sum c_mu^2 - (sum c_mu)^2] / sum c_mu^2
    = 4 * [d - (sum c_mu)^2 / sum c_mu^2]
    """
    c_vec = np.array(c_vec)
    c_sum = sum(c_vec)
    c_sq = sum(c_vec**2)
    return 4 * (d - c_sum**2 / c_sq)

def main():
    L = 2

    print("="*70)
    print("ANALYTICAL FORMULA DERIVATION")
    print("="*70)
    print()
    print("For modes v_{x,mu} = c_mu * (-1)^|x|:")
    print()
    print("B_plaq = c_mu*(-1)^|x| + c_nu*(-1)^|x+mu| - c_mu*(-1)^|x+nu| - c_nu*(-1)^|x|")
    print("       = c_mu*(-1)^|x| - c_nu*(-1)^|x| + c_mu*(-1)^|x| - c_nu*(-1)^|x|")
    print("       [since |x+mu_hat| = |x|+1 for L=2, so (-1)^|x+mu_hat| = -(-1)^|x|]")
    print("       = (-1)^|x| * [c_mu - c_nu - (-c_mu) - c_nu]")
    print("       = (-1)^|x| * 2(c_mu - c_nu)")
    print()
    print("|B_plaq|^2 = 4(c_mu - c_nu)^2")
    print()
    print("Rayleigh Q = 4 * [sum_{mu<nu} (c_mu-c_nu)^2] / [sum_mu c_mu^2]")
    print("           = 4 * [d*|c|^2 - (c.1)^2] / |c|^2")
    print("           = 4 * [d - (c.1)^2/|c|^2]")
    print()
    print("Maximum Q when c orthogonal to 1: Q_max = 4d")
    print("For staggered mode c_mu = (-1)^mu:")
    print("  sum c_mu = sum_{mu=0}^{d-1} (-1)^mu = (1-(-1)^d)/2")
    print("  For even d: sum=0, Q=4d")
    print("  For odd d: sum=1, Q = 4*(d - 1/d) = 4(d^2-1)/d")

    print()
    print("="*70)
    print("VERIFICATION BY DIMENSION")
    print("="*70)

    for d in [3, 4, 5, 6]:
        print(f"\nd = {d}:")
        M = build_M_identity(d, L)

        # Staggered mode c_mu = (-1)^mu
        c_stag = np.array([(-1)**mu for mu in range(d)], dtype=float)
        c_sum_stag = sum(c_stag)
        Q_stag_analytical = analytical_formula(d, c_stag)
        Q_stag_numerical, is_eig_stag = analyze_half_staggered_mode(d, L, c_stag)
        print(f"  Staggered c = {c_stag}, sum = {c_sum_stag}")
        print(f"  Q_stag (analytical) = 4(d^2-1)/d = {4*(d**2-1)/d:.6f}")
        print(f"  Q_stag (formula)    = {Q_stag_analytical:.6f}")
        print(f"  Q_stag (numerical)  = {Q_stag_numerical:.6f}")
        print(f"  Is eigenvector: {is_eig_stag}")

        # Optimal mode: c orthogonal to 1, e.g. c = (d-1, -1, -1, ..., -1)
        c_opt = np.array([-1.0] * d)
        c_opt[0] = float(d - 1)
        Q_opt_analytical = analytical_formula(d, c_opt)
        Q_opt_numerical, is_eig_opt = analyze_half_staggered_mode(d, L, c_opt)
        print(f"  Optimal c = {c_opt}, sum = {sum(c_opt):.6f}")
        print(f"  Q_opt (analytical)  = 4d = {4*d}")
        print(f"  Q_opt (formula)     = {Q_opt_analytical:.6f}")
        print(f"  Q_opt (numerical)   = {Q_opt_numerical:.6f}")
        print(f"  Is eigenvector: {is_eig_opt}")

        # H eigenvalues
        beta = 1.0
        N = 2
        print(f"  lambda_max(H) = (beta/(2N)) * 4d = {(beta/(2*N))*4*d:.4f}*beta")
        print(f"  lambda_stag(H) = (beta/(2N)) * 4(d^2-1)/d = {(beta/(2*N))*4*(d**2-1)/d:.4f}*beta")
        print(f"  H_norm = d/(16*(d-1)) = {d/(16*(d-1)):.8f}")

    print()
    print("="*70)
    print("EIGENVALUE STRUCTURE SUMMARY")
    print("="*70)
    print()
    print("On L=2 torus, the Hessian M(I) eigenmodes at Q=I are:")
    print("  v_{x,mu} = c_mu * f(x)  where f(x) = product_{nu in S} (-1)^{x_nu}")
    print()
    print("The 'all-high' modes have f(x) = (-1)^{sum x_i} = (-1)^|x|.")
    print("Rayleigh Q = 4 * [d - (c.1)^2/|c|^2]")
    print("Maximum Q = 4d, achieved when c is orthogonal to (1,...,1).")
    print("This has multiplicity d-1 (rank d directions minus the longitudinal zero mode).")
    print()

    for d in [3, 4, 5, 6]:
        eigvals = np.linalg.eigvalsh(build_M_identity(d, L))
        lmax = max(eigvals)
        from math import ceil, floor
        print(f"d={d}: lambda_max={lmax:.1f} = 4d={4*d}, multiplicity={np.sum(eigvals > lmax-0.01)}")

    print()
    print("="*70)
    print("ODD vs EVEN d ANOMALY EXPLANATION")
    print("="*70)
    print()
    print("The 'staggered mode' v_{x,mu} = (-1)^{|x|+mu} = (-1)^|x| * (-1)^mu")
    print("has direction vector c_mu = (-1)^mu.")
    print()
    print("sum_{mu=0}^{d-1} c_mu = sum_{mu=0}^{d-1} (-1)^mu")
    print("  = (1 + (-1)^d * (-1)) / (1 - (-1)) ... hmm let me just list:")
    for d in range(3, 7):
        c_sum = sum((-1)**mu for mu in range(d))
        print(f"  d={d}: sum = {c_sum} ({'=0: achieves max' if c_sum==0 else '!=0: below max'})")

    print()
    print("CONCLUSION: Staggered mode achieves lambda_max iff d is EVEN.")
    print("For odd d, lambda_max is achieved by modes c with sum c_mu = 0,")
    print("e.g. c = (d-1, -1, ..., -1) or any vector in span{e_mu - e_nu}.")

    print()
    print("="*70)
    print("H_NORM FORMULA")
    print("="*70)
    print()
    print("H_norm = lambda_max(H) / (8*(d-1)*N*beta)")
    print("       = (beta/(2N))*4d / (8*(d-1)*N*beta)")
    print("       = 4d / (16*(d-1)*N^2)")
    print("       = d / (4*(d-1)*N^2)")
    print()
    print("For N=2: H_norm = d / (16*(d-1))")
    for d in [3, 4, 5, 6]:
        N = 2
        print(f"  d={d}: H_norm = {d/(16*(d-1)):.8f} = {d}/{16*(d-1)}")

    print()
    print("CS threshold: beta < N^2/(8*(d-1)) = 1/(2*(d-1)) for N=2")
    for d in [3, 4, 5, 6]:
        print(f"  d={d}: beta < 1/{2*(d-1)} = {1/(2*(d-1)):.6f}")

    print()
    print("="*70)
    print("TRIANGLE INEQUALITY PROOF GENERALIZATION")
    print("="*70)
    print()
    print("The Cauchy-Schwarz step at Q != I:")
    print("|B_plaq(v)|^2 = |Ad_{P1}v1 + Ad_{P3}v2 - Ad_{P3}v3 - Ad_{P4}v4|^2")
    print("              <= (|v1| + |v2| + |v3| + |v4|)^2 [by CS, since Ad is isometry]")
    print("              <= 4(|v1|^2 + |v2|^2 + |v3|^2 + |v4|^2) [by CS]")
    print()
    print("Each link appears in 2(d-1) plaquettes.")
    print("Sum_plaq |B_plaq(v)|^2 <= 4*2(d-1)*|v|^2 = 8(d-1)|v|^2")
    print()
    print("HessS(v,v) = (beta/(2N)) * Sum_plaq |B_plaq(v)|^2")
    print("           <= (beta/(2N)) * 8(d-1) * |v|^2")
    print("           = 4(d-1)beta/N * |v|^2")
    print()
    print("K_S > 0 requires HessS < (N/2)|v|^2 [Bochner condition]")
    print("So: 4(d-1)beta/N < N/2 => beta < N^2 / (8(d-1))")
    print()
    for d in [3, 4, 5, 6]:
        N = 2
        thresh = N**2 / (8*(d-1))
        print(f"  d={d}: beta < N^2/(8*(d-1)) = 4/{8*(d-1)} = {thresh:.6f} = 1/{int(1/thresh)}")
    print()
    print("This is dimension-INDEPENDENT in structure, dimension-DEPENDENT in threshold.")
    print("The proof works for all d >= 2.")
    print()

    # Final: show that actual H_norm(I) is strictly below the CS threshold
    print("="*70)
    print("TIGHTNESS CHECK: H_norm(I) vs 1/(8(d-1)N^2)")
    print("="*70)
    print()
    print("H_norm_actual = d/(16(d-1)) = d/(4N^2(d-1))")
    print("H_norm_CS_bound = CS/(8(d-1)N*beta / (8(d-1)N*beta)) = 1/2 (relative to full CS)")
    print("More precisely: lambda_max(H) = d*beta vs CS_bound = 4(d-1)*beta/N = 2(d-1)*beta")
    print("Ratio = d / (2(d-1)) -> 1/2 as d->inf")
    print()
    for d in [3, 4, 5, 6]:
        lmax = d  # lambda_max(H) = d*beta for N=2
        cs_bound = 4*(d-1)*1.0/2  # 4(d-1)*beta/N
        ratio = lmax / cs_bound
        print(f"  d={d}: lambda_max={d}*beta, CS_bound={2*(d-1)}*beta, ratio={ratio:.4f}")

if __name__ == '__main__':
    main()
