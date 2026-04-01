"""
Exploration 006: Hessian eigenspectrum at Q=I for d=3,4,5,6
Convention: LEFT perturbation, S = -(beta/N)*sum Re Tr(U_plaq), N=2

M(I) = sum_plaq b_plaq^T b_plaq
where b_plaq is the "discrete curl" indicator vector over links.

At Q=I, the SU(2) structure factors out and M(I) is a real n_links x n_links matrix.
HessS eigenvalues = (beta/(2N)) * M(I) eigenvalues.
"""

import numpy as np
from itertools import product

def get_sites(d, L=2):
    """Return list of all sites as tuples."""
    return list(product(range(L), repeat=d))

def site_to_idx(x, L=2):
    """Convert site tuple to integer index."""
    idx = 0
    for xi in x:
        idx = idx * L + xi
    return idx

def link_idx(x, mu, d, L=2):
    """Return global link index for link (x, mu)."""
    n_sites = L**d
    return site_to_idx(x, L) * d + mu

def shift_site(x, mu, L=2):
    """Shift site x by +1 in direction mu (periodic)."""
    x = list(x)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

def build_M_identity(d, L=2):
    """
    Build the geometric Hessian matrix M(I) = sum_plaq b_plaq b_plaq^T.
    At Q=I, left perturbation: B_plaq = v1 + v2 - v3 - v4
    where v1 = link (x, mu) [forward leg]
          v2 = link (x+mu, nu) [right leg]
          v3 = link (x+nu, mu) [back leg, reversed = -]
          v4 = link (x, nu) [left leg, reversed = -]

    Note: for left perturbation at Q=I:
    B_plaq(v)[a=color] = v_{x,mu}[a] + v_{x+mu,nu}[a] - v_{x+nu,mu}[a] - v_{x,nu}[a]

    The +/- signs: for LEFT perturbation B_plaq = v1+v2-v3-v4 in the orientation
    link1=(x,mu), link2=(x+mu,nu), link3=(x+nu,mu)^{-1}, link4=(x,nu)^{-1}
    """
    sites = get_sites(d, L)
    n_links = d * (L**d)

    M = np.zeros((n_links, n_links))

    for x in sites:
        for mu in range(d):
            for nu in range(mu+1, d):
                # Plaquette in (mu, nu) plane at x
                x_munu = x
                x_mu   = shift_site(x, mu, L)    # x + mu_hat
                x_nu   = shift_site(x, nu, L)    # x + nu_hat

                # Link indices in this plaquette
                # b_plaq = +link(x,mu) + link(x+mu,nu) - link(x+nu,mu) - link(x,nu)
                i1 = link_idx(x,    mu, d, L)   # +1
                i2 = link_idx(x_mu, nu, d, L)   # +1
                i3 = link_idx(x_nu, mu, d, L)   # -1
                i4 = link_idx(x,    nu, d, L)   # -1

                # b_plaq vector (coefficients for each link)
                b = np.zeros(n_links)
                b[i1] += 1.0
                b[i2] += 1.0
                b[i3] -= 1.0
                b[i4] -= 1.0

                M += np.outer(b, b)

    return M

def staggered_mode_eigenvalue(d, L=2):
    """
    Compute the Rayleigh quotient of the staggered mode v_{x,mu} = (-1)^(|x|+mu)
    for M(I).
    Returns the eigenvalue (if it's actually an eigenvector) or just the Rayleigh quotient.
    """
    sites = get_sites(d, L)
    n_links = d * (L**d)

    # Build staggered mode vector
    v = np.zeros(n_links)
    for x in sites:
        for mu in range(d):
            x_sum = sum(x)
            v[link_idx(x, mu, d, L)] = (-1)**(x_sum + mu)

    M = build_M_identity(d, L)
    Mv = M @ v
    rayleigh = np.dot(v, Mv) / np.dot(v, v)

    # Check if it's an eigenvector
    residual = Mv - rayleigh * v
    is_eigvec = np.linalg.norm(residual) / np.linalg.norm(v) < 1e-8

    return rayleigh, is_eigvec, v

def analyze_eigenvector(eigvec, d, L=2, threshold=0.01):
    """
    Analyze structure of an eigenvector.
    Returns dict with information about the pattern.
    """
    sites = get_sites(d, L)
    n_links = d * (L**d)

    # Normalize
    eigvec = eigvec / np.linalg.norm(eigvec) * np.sqrt(n_links)

    # Check component pattern
    components = {}
    for x in sites:
        for mu in range(d):
            idx = link_idx(x, mu, d, L)
            val = eigvec[idx]
            x_sum = sum(x)
            stag = (-1)**(x_sum + mu)
            components[(x, mu)] = {'val': val, 'stag': stag, 'x_sum': x_sum}

    # Check for direction-only dependence (v depends only on mu, not x)
    dir_mode = True
    dir_vals = {}
    for mu in range(d):
        mu_vals = [eigvec[link_idx(x, mu, d, L)] for x in sites]
        if np.std(mu_vals) > threshold * np.abs(np.mean(mu_vals)) + threshold:
            dir_mode = False
        dir_vals[mu] = np.mean(mu_vals)

    # Check for "half-staggered": v = f(mu) * (-1)^|x| (staggered in x but not mu)
    half_stag_check = []
    for mu in range(d):
        mu_vals = np.array([eigvec[link_idx(x, mu, d, L)] * (-1)**sum(x) for x in sites])
        half_stag_check.append(np.std(mu_vals))
    is_half_stag = all(s < threshold * 10 + 0.01 for s in half_stag_check)

    # Check for "mu-staggered": v = f(x) * (-1)^mu
    mu_stag_check = []
    for x in sites:
        x_vals = np.array([eigvec[link_idx(x, mu, d, L)] * (-1)**mu for mu in range(d)])
        mu_stag_check.append(np.std(x_vals))
    is_mu_stag = all(s < threshold * 10 + 0.01 for s in mu_stag_check)

    return {
        'is_dir_mode': dir_mode,
        'dir_vals': dir_vals,
        'is_half_stag': is_half_stag,
        'is_mu_stag': is_mu_stag,
        'half_stag_check': half_stag_check,
    }

def compute_dimension(d, L=2, beta=1.0, N=2):
    """
    Full computation for dimension d.
    Returns dict with all results.
    """
    print(f"\n{'='*60}")
    print(f"d = {d}, L = {L}, N = {N}")
    n_sites = L**d
    n_links = d * n_sites
    n_dof = n_links * (N**2 - 1)
    print(f"n_sites = {n_sites}, n_links = {n_links}, n_dof = {n_dof}")

    # Build M(I)
    M = build_M_identity(d, L)
    print(f"M(I) shape: {M.shape}")

    # Compute eigenspectrum
    eigvals, eigvecs = np.linalg.eigh(M)
    eigvals_sorted = sorted(eigvals, reverse=True)

    lambda_max_M = eigvals_sorted[0]
    lambda_max_H = (beta / (2*N)) * lambda_max_M

    # Sanity check: beta=1, so 4*beta = 4
    expected_H = 4 * beta * d / 4  # = beta*d for any d? No...
    # Actually expected from staggered mode: (beta/(2N)) * 16 * ceil(d/2)*floor(d/2) / d
    # Wait, need to recalculate. Expected lambda_max(M) for staggered mode:
    # = 16 * ceil(d/2) * floor(d/2) * L^d / (d * L^d)
    # No wait: for staggered mode |v|^2 = n_links = d*L^d
    # Sigma_plaq |B_plaq|^2 = 16 * (# plaquettes with different parity mu,nu) * L^d/L^d? No...

    # Correct calculation:
    # For each site x, for each plaquette (mu,nu) with mu<nu:
    # |B_plaq|^2 = 4*[(-1)^mu - (-1)^nu]^2 = 0 if mu,nu same parity, 16 if different
    # Number of (mu,nu) pairs with different parity = ceil(d/2)*floor(d/2)
    # Sum over all sites: L^d * ceil(d/2)*floor(d/2) plaquettes contribute 16 each
    # Total Sigma |B_plaq|^2 = 16 * L^d * ceil(d/2)*floor(d/2)
    # Rayleigh quotient = Total / |v|^2 = 16 * L^d * ceil(d/2)*floor(d/2) / (d * L^d)
    #                    = 16 * ceil(d/2)*floor(d/2) / d

    from math import ceil, floor
    stag_rayleigh_expected = 16 * ceil(d/2) * floor(d/2) / d

    # Compute actual staggered mode eigenvalue
    stag_rayleigh, is_eigvec, stag_v = staggered_mode_eigenvalue(d, L)

    print(f"\nEigenvalue analysis:")
    print(f"  lambda_max(M)           = {lambda_max_M:.6f}")
    print(f"  lambda_max(H) = beta*   {lambda_max_H:.6f}")
    print(f"  Expected 4*beta*d/4?    {beta*d:.6f} (staggered for d=4)")
    print(f"  Staggered Rayleigh      = {stag_rayleigh:.6f} (expected {stag_rayleigh_expected:.6f})")
    print(f"  Staggered is eigvec?    {is_eigvec}")

    # H_norm = lambda_max(H) / (8*(d-1)*N*beta)
    H_norm = lambda_max_H / (8 * (d-1) * N * beta)
    print(f"  H_norm = {H_norm:.8f}")

    # CS bound
    cs_bound_H = (beta / (2*N)) * 4 * 2 * (d-1)  # (beta/4) * 4 * 2*(d-1) for N=2
    cs_threshold_beta = N**2 / (8 * (d-1))  # beta < N^2/(8*(d-1)) for K_S > 0
    print(f"  CS bound on lambda_max(H): {cs_bound_H:.4f} * beta")
    print(f"  K_S>0 threshold: beta < {cs_threshold_beta:.6f} = {cs_threshold_beta}")

    # Print top eigenvalues
    print(f"\nTop 10 eigenvalues of M(I):")
    for i, lv in enumerate(eigvals_sorted[:10]):
        print(f"  [{i}] {lv:.6f}  -> H eigenvalue {(beta/(2*N))*lv:.6f}*beta")

    # Eigenvalue multiplicity analysis
    unique_eigs, counts = np.unique(np.round(eigvals, 4), return_counts=True)
    print(f"\nUnique eigenvalues of M(I) (rounded to 4 decimals):")
    for uv, c in sorted(zip(unique_eigs, counts), reverse=True)[:15]:
        print(f"  {uv:.4f} (multiplicity {c})")

    # Analyze eigenvector of max eigenvalue
    max_idx = np.argmax(eigvals)
    max_eigvec = eigvecs[:, max_idx]
    print(f"\nAnalyzing max eigenvector (lambda={eigvals[max_idx]:.4f}):")
    analysis = analyze_eigenvector(max_eigvec, d, L)
    print(f"  Is direction-only mode? {analysis['is_dir_mode']}")
    if analysis['is_dir_mode']:
        print(f"  Direction values: {analysis['dir_vals']}")
    print(f"  Is half-staggered (f(mu)*(-1)^|x|)? {analysis['is_half_stag']}")
    print(f"  Is mu-staggered (f(x)*(-1)^mu)? {analysis['is_mu_stag']}")

    # Compare max eigvec with staggered mode
    norm_max = max_eigvec / np.linalg.norm(max_eigvec)
    norm_stag = stag_v / np.linalg.norm(stag_v)
    overlap = abs(np.dot(norm_max, norm_stag))
    print(f"  Overlap with staggered mode: {overlap:.6f}")

    # For d=5: check "checker-board" modes - modes of the form v_{x,mu} = (-1)^x_nu for some fixed nu
    # These are "spatial direction" modes
    print(f"\nChecking special modes for d={d}:")
    for test_nu in range(d):
        v_test = np.zeros(n_links)
        for x in get_sites(d, L):
            for mu in range(d):
                v_test[link_idx(x, mu, d, L)] = (-1)**x[test_nu]
        Mv = M @ v_test
        rq = np.dot(v_test, Mv) / np.dot(v_test, v_test)
        print(f"  Mode v=(-1)^x[{test_nu}]: Rayleigh quotient = {rq:.6f} -> H = {(beta/(2*N))*rq:.6f}*beta")

    # "mu-checker" modes: v_{x,mu} = delta_{mu, nu0}
    print("\nChecking direction-selector modes v_{x,mu} = delta_mu_nu:")
    for nu0 in range(d):
        v_test = np.zeros(n_links)
        for x in get_sites(d, L):
            v_test[link_idx(x, nu0, d, L)] = 1.0
        Mv = M @ v_test
        rq = np.dot(v_test, Mv) / np.dot(v_test, v_test)
        print(f"  nu={nu0}: Rayleigh quotient = {rq:.6f} -> H = {(beta/(2*N))*rq:.6f}*beta")

    return {
        'd': d,
        'n_links': n_links,
        'n_dof': n_dof,
        'lambda_max_M': lambda_max_M,
        'lambda_max_H': lambda_max_H,
        'stag_rayleigh': stag_rayleigh,
        'stag_rayleigh_expected': stag_rayleigh_expected,
        'is_eigvec': is_eigvec,
        'H_norm': H_norm,
        'cs_bound_H': cs_bound_H,
        'cs_threshold_beta': cs_threshold_beta,
        'eigvals': eigvals,
    }

def main():
    print("EXPLORATION 006: d=5 Anomaly Resolution")
    print("Convention: LEFT perturbation, S = -(beta/N) Re Tr(U_plaq), N=2")
    print("M(I) = sum_plaq b_plaq b_plaq^T, HessS = (beta/(2N)) * M(I)")

    beta = 1.0
    N = 2
    L = 2

    results = {}
    for d in [3, 4, 5, 6]:
        results[d] = compute_dimension(d, L, beta, N)

    # Summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'d':>3} | {'n_links':>8} | {'lambda_max(M)':>14} | {'lambda_max(H)/beta':>18} | {'stag_eig/beta':>14} | {'H_norm':>8} | {'CS_thresh':>10}")
    print("-"*80)

    for d in [3, 4, 5, 6]:
        r = results[d]
        lmH = r['lambda_max_H']
        stag = r['stag_rayleigh'] * beta / (2*N)
        H_norm = r['H_norm']
        cs = r['cs_threshold_beta']
        cs_H = r['cs_bound_H']
        print(f"{d:>3} | {r['n_links']:>8} | {r['lambda_max_M']:>14.4f} | {lmH:>18.6f} | {stag:>14.6f} | {H_norm:>8.6f} | {cs:>10.6f}")

    print("\nFormulas:")
    print("  lambda_max(H) = (beta/(2N)) * lambda_max(M)")
    print("  H_norm = lambda_max(H) / (8*(d-1)*N*beta)")
    print("  CS threshold: beta < N^2/(8*(d-1)) = 1/(2*(d-1)) for N=2")

    print("\nChecking H_norm formula: H_norm(I) = ceil(d/2)*floor(d/2) / (N^2 * d * (d-1))?")
    from math import ceil, floor
    for d in [3, 4, 5, 6]:
        r = results[d]
        formula = ceil(d/2) * floor(d/2) / (N**2 * d * (d-1))
        print(f"  d={d}: formula={formula:.8f}, computed={r['H_norm']:.8f}, match={abs(formula - r['H_norm']) < 1e-6}")

    # Check if lambda_max(M) = 4d for all d
    print("\nChecking lambda_max(M) = 4d:")
    for d in [3, 4, 5, 6]:
        r = results[d]
        expected = 4 * d
        print(f"  d={d}: 4d={expected}, lambda_max={r['lambda_max_M']:.4f}, match={abs(r['lambda_max_M'] - expected) < 0.01}")

    # Detailed d=5 analysis
    print("\n" + "="*60)
    print("DETAILED d=5 ANALYSIS")
    print("="*60)
    r5 = results[5]
    d = 5
    L = 2
    M = build_M_identity(d, L)
    eigvals, eigvecs = np.linalg.eigh(M)

    # Find all eigenvectors near the maximum
    max_lam = eigvals.max()
    near_max = np.where(np.abs(eigvals - max_lam) < 0.01)[0]
    print(f"Degenerate eigenvectors at lambda_max={max_lam:.4f}: {len(near_max)}")

    # Print the structure of ALL distinct eigenvalues
    unique_eigs = np.unique(np.round(eigvals, 4))
    print(f"\nAll distinct eigenvalues of M(I) for d=5:")
    for uv in sorted(unique_eigs, reverse=True):
        mult = np.sum(np.abs(np.round(eigvals, 4) - uv) < 0.01)
        hval = (beta/(2*N)) * uv
        print(f"  {uv:.4f} (x{mult}) -> H eigenvalue = {hval:.4f}*beta")

    # Staggered mode analysis
    stag_rq, is_eig, stag_v = staggered_mode_eigenvalue(5, L)
    print(f"\nStaggered mode:")
    print(f"  Rayleigh quotient = {stag_rq:.6f}")
    print(f"  Is eigenvector: {is_eig}")
    print(f"  Expected from formula: {16*3*2/5:.6f} = 96/5 = 19.2")

    # Identify what eigenvectors look like at the maximum
    print(f"\nMax eigenvectors analysis (lambda={max_lam:.4f}):")
    for idx in near_max[:5]:
        ev = eigvecs[:, idx]
        ev_norm = ev / np.linalg.norm(ev)

        # Check spatial pattern: does it depend only on one direction?
        sites = list(product(range(2), repeat=5))
        n_links = 5 * 32

        print(f"\n  Eigvec at index {idx} (lambda={eigvals[idx]:.4f}):")

        # Show components
        components_by_site = {}
        for x in sites:
            components_by_site[x] = [ev_norm[link_idx(x, mu, 5, L)] for mu in range(5)]

        # Print a few representative sites
        for x in list(sites)[:4]:
            print(f"    x={x}: " + ", ".join(f"v_{mu}={components_by_site[x][mu]:+.4f}" for mu in range(5)))

    return results

if __name__ == '__main__':
    results = main()
