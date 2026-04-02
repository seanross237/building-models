"""
Matrix Domination Test: Is H(I) - H(Q) positive semidefinite?
=============================================================

Tests the strong matrix inequality H(I) >= H(Q) for random SU(2) link
configurations Q on a lattice with Wilson action.

H(Q) = HessS(Q) is the full Hessian of the Wilson action at configuration Q.

The Hessian is computed analytically using the product-of-exponentials formula,
verified against finite differences in prior work (yang-mills-validation S002-E002).

Lattice: L=2, d-dimensional hypercubic torus, SU(2) gauge group.
Tests d=2, d=3, d=4.

Author: Sean (via Claude)
Date: 2026-03-29
"""

import numpy as np
from scipy.linalg import expm, eigvalsh
import sys
import time

np.random.seed(42)

# ============================================================================
# SU(2) Lie algebra utilities
# ============================================================================

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T_gen = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)


def su2_from_vec(v):
    """Map R^3 vector to su(2) element: v -> sum v_a T_a."""
    return sum(vi * ti for vi, ti in zip(v, T_gen))


def su2_to_vec(X):
    """Map su(2) element to R^3 vector using trace inner product."""
    return np.array([-2.0 * np.trace(t @ X).real for t in T_gen])


def Ad(Q, v_mat):
    """Adjoint action: Ad_Q(v) = Q v Q^dag."""
    return Q @ v_mat @ Q.conj().T


def re_tr(M):
    """Real part of trace."""
    return np.trace(M).real


def random_SU2():
    """Haar-random SU(2) element via Gaussian quaternion."""
    a = np.random.randn(4)
    a /= np.linalg.norm(a)
    return (a[0] * I2 + 1j * (a[1] * sigma[0] + a[2] * sigma[1] + a[3] * sigma[2]))


# ============================================================================
# Lattice geometry
# ============================================================================

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.Nsites = L ** d
        self.Nlinks = d * self.Nsites
        self.Ndof = 3 * self.Nlinks
        self.plaquettes = self._build_plaquettes()
        self.Nplaq = len(self.plaquettes)

    def site_index(self, x):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (x[i] % self.L)
        return idx

    def site_coords(self, idx):
        x = []
        r = idx
        for i in range(self.d):
            x.append(r % self.L)
            r //= self.L
        return list(reversed(x))

    def link_index(self, x, mu):
        return mu * self.Nsites + self.site_index(x)

    def neighbor(self, x, mu, direction=1):
        y = list(x)
        y[mu] = (y[mu] + direction) % self.L
        return y

    def _build_plaquettes(self):
        plaquettes = []
        for s in range(self.Nsites):
            x = self.site_coords(s)
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    e1 = self.link_index(x, mu)
                    e2 = self.link_index(self.neighbor(x, mu), nu)
                    e3 = self.link_index(self.neighbor(x, nu), mu)
                    e4 = self.link_index(x, nu)
                    plaquettes.append((e1, e2, e3, e4))
        return plaquettes


# ============================================================================
# Hessian computation (analytical, verified formula)
# ============================================================================

def build_hessian(lat, Q, beta=1.0):
    """
    Build the full Hessian of the Wilson action S = -(beta/2) sum_P Re Tr(U_P)
    at configuration Q, using the product-of-exponentials expansion.

    Under left perturbation Q_k -> exp(t*v_k) Q_k, the plaquette is:
      U_P(t) = prod_k exp(t * s_k * Ad_{P_k}(v_{e_k})) * U_P

    where s_k = +1 for forward edges, -1 for backward edges, and
    P_k is the path-ordered product from the first edge to edge k.

    The second derivative gives the Hessian entries:
      H[3*e_k+a, 3*e_l+b] from plaquette contributions.

    For k=l (same exponential, same edge position in plaquette):
      (1/2)(Re Tr(w_{k,a} w_{k,b} U) + Re Tr(w_{k,b} w_{k,a} U))
    For k<l (different positions):
      Re Tr(w_{k,a} w_{l,b} U)
    For k>l:
      Re Tr(w_{l,b} w_{k,a} U)

    Multiplied by -(beta/2).
    """
    Ndof = lat.Ndof
    H = np.zeros((Ndof, Ndof))

    for (e1, e2, e3, e4) in lat.plaquettes:
        # Plaquette holonomy: U = Q[e1] Q[e2] Q[e3]^dag Q[e4]^dag
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T

        # Parallel transport operators for each edge position
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ Q[e3].conj().T

        edges = [e1, e2, e3, e4]
        signs = [1, 1, -1, -1]
        Ad_ops = [I2, P2, P3, U]

        # Precompute all w_{k,a} = s_k * Ad_{P_k}(T_a)
        wka = np.zeros((4, 3, 2, 2), dtype=complex)
        for k in range(4):
            for a in range(3):
                wka[k, a] = signs[k] * Ad(Ad_ops[k], T_gen[a])

        # Build Hessian contributions from this plaquette
        for k in range(4):
            for a in range(3):
                i = 3 * edges[k] + a
                for l in range(4):
                    for b in range(3):
                        j = 3 * edges[l] + b

                        if k == l:
                            val = 0.5 * (re_tr(wka[k, a] @ wka[k, b] @ U) +
                                         re_tr(wka[k, b] @ wka[k, a] @ U))
                        elif k < l:
                            val = re_tr(wka[k, a] @ wka[l, b] @ U)
                        else:
                            val = re_tr(wka[l, b] @ wka[k, a] @ U)

                        H[i, j] += -(beta / 2) * val

    # Symmetrize (numerical precision)
    H = (H + H.T) / 2
    return H


def wilson_action(lat, Q, beta=1.0):
    """Compute Wilson action S = -(beta/2) sum_P Re Tr(U_P)."""
    S = 0.0
    for (e1, e2, e3, e4) in lat.plaquettes:
        U = Q[e1] @ Q[e2] @ Q[e3].conj().T @ Q[e4].conj().T
        S -= (beta / 2) * re_tr(U)
    return S


def build_hessian_fd(lat, Q, beta=1.0, h=1e-4):
    """Finite-difference Hessian for verification."""
    Ndof = lat.Ndof
    Nlinks = lat.Nlinks
    H = np.zeros((Ndof, Ndof))
    S0 = wilson_action(lat, Q, beta)

    # Diagonal entries
    for i in range(Ndof):
        li, ci = divmod(i, 3)
        old = Q[li].copy()
        Q[li] = expm(h * T_gen[ci]) @ old
        Sp = wilson_action(lat, Q, beta)
        Q[li] = expm(-h * T_gen[ci]) @ old
        Sm = wilson_action(lat, Q, beta)
        Q[li] = old
        H[i, i] = (Sp - 2 * S0 + Sm) / h ** 2

    # Off-diagonal entries
    for i in range(Ndof):
        li, ci = divmod(i, 3)
        for j in range(i + 1, Ndof):
            lj, cj = divmod(j, 3)
            old_i, old_j = Q[li].copy(), Q[lj].copy()

            Q[li] = expm(h * T_gen[ci]) @ old_i
            Q[lj] = expm(h * T_gen[cj]) @ old_j
            Spp = wilson_action(lat, Q, beta)
            Q[lj] = expm(-h * T_gen[cj]) @ old_j
            Spm = wilson_action(lat, Q, beta)
            Q[lj] = old_j
            Q[li] = old_i

            Q[li] = expm(-h * T_gen[ci]) @ old_i
            Q[lj] = expm(h * T_gen[cj]) @ old_j
            Smp = wilson_action(lat, Q, beta)
            Q[lj] = expm(-h * T_gen[cj]) @ old_j
            Smm = wilson_action(lat, Q, beta)
            Q[lj] = old_j
            Q[li] = old_i

            H[i, j] = (Spp - Spm - Smp + Smm) / (4 * h ** 2)
            H[j, i] = H[i, j]

    return H


def make_identity_config(lat):
    """Create flat connection (all links = I)."""
    Q = np.zeros((lat.Nlinks, 2, 2), dtype=complex)
    for i in range(lat.Nlinks):
        Q[i] = I2.copy()
    return Q


def make_random_config(lat):
    """Create random SU(2) configuration (Haar measure on each link)."""
    Q = np.zeros((lat.Nlinks, 2, 2), dtype=complex)
    for i in range(lat.Nlinks):
        Q[i] = random_SU2()
    return Q


# ============================================================================
# Sanity checks
# ============================================================================

def run_sanity_checks(lat, beta=1.0):
    """Verify Hessian at Q=I matches known exact values."""
    print("=" * 70)
    print(f"SANITY CHECKS: L={lat.L}, d={lat.d}, beta={beta}")
    print(f"  Sites={lat.Nsites}, Links={lat.Nlinks}, DOF={lat.Ndof}, Plaquettes={lat.Nplaq}")
    print("=" * 70)

    Q_I = make_identity_config(lat)
    H_I = build_hessian(lat, Q_I, beta)

    eigs_I = eigvalsh(H_I)[::-1]  # Descending

    # Expected: lambda_max = 2*d*beta for d-dim, N=2
    # (from the Fourier analysis: at Q=I, the max eigenvalue of H is 2*d*beta)
    # Actually from the formula: H_norm = d/(4*(d-1)*N^2) where N=2
    # lambda_max / (total normalization factor) = H_norm
    # The normalization factor for SZZ is 8*(d-1)*N*beta = 8*(d-1)*2*beta
    # So lambda_max = H_norm * 8*(d-1)*2*beta = d/(4*(d-1)*4) * 16*(d-1)*beta = 2*d*beta
    # Wait, let me recalculate from the library entry:
    # H_norm_max(I) = d / (4*(d-1)*N^2) for N=2:
    # lambda_max = H_norm * 8*(d-1)*N*beta = [d/(4*(d-1)*4)] * 8*(d-1)*2*beta
    #            = d * 16*(d-1)*beta / (16*(d-1))
    #            = d * beta  ... that doesn't match either
    #
    # From the Fourier entry: "λ_max = 4β, H_norm = 4β/48β = 1/12 exactly" for d=4
    # So lambda_max(H_I) = 4*beta for d=4.
    # More generally: lambda_max = 2*d*beta (verified at d=4: 2*4*1 = 8... no that's 4)
    # Actually the entry says: K_curl has eigenvalue 4d at k=(pi,...,pi)
    # The Hessian at Q=I is (beta/2N) * K_curl where K_curl is the curl operator
    # Wait: HessS(v,v)|_{Q=I} = (beta/(2N)) sum |omega|^2
    # The operator form: H_I = (beta/(2N)) * K_curl
    # lambda_max(K_curl) = 4d  (proven)
    # lambda_max(H_I) = (beta/(2N)) * 4d = 4d*beta/(2*2) = d*beta for N=2
    # For d=4, N=2: lambda_max = 4*beta = 4.0 ✓
    # H_norm = lambda_max / (8*(d-1)*N*beta) = d*beta / (16*(d-1)*beta) = d/(16*(d-1))
    # For d=4: 4/48 = 1/12 ✓
    expected_lmax = lat.d * beta  # For N=2

    print(f"\n  Eigenvalue spectrum of H(I):")
    print(f"    lambda_max = {eigs_I[0]:.8f}")
    print(f"    lambda_min = {eigs_I[-1]:.8f}")
    print(f"    Expected lambda_max = {expected_lmax:.8f}")
    print(f"    Ratio: {eigs_I[0]/expected_lmax:.8f}")
    print(f"    Match: {'YES' if abs(eigs_I[0] - expected_lmax) < 1e-6 else 'NO -- PROBLEM!'}")

    # H_norm check
    norm_factor = 8 * (lat.d - 1) * 2 * beta  # 8*(d-1)*N*beta for N=2
    H_norm = eigs_I[0] / norm_factor
    expected_Hnorm = lat.d / (16 * (lat.d - 1))  # d/(4*(d-1)*N^2) with N=2
    print(f"\n    H_norm(I) = {H_norm:.8f}")
    print(f"    Expected  = {expected_Hnorm:.8f}")
    print(f"    Match: {'YES' if abs(H_norm - expected_Hnorm) < 1e-6 else 'NO -- PROBLEM!'}")

    # Finite-difference verification for d=2 (small enough)
    if lat.d == 2:
        print("\n  Finite-difference verification (d=2 only):")
        H_fd = build_hessian_fd(lat, Q_I, beta, h=1e-4)
        diff = np.max(np.abs(H_I - H_fd))
        print(f"    |H_analytical - H_FD| = {diff:.2e}")
        print(f"    Match: {'YES' if diff < 1e-4 else 'NO -- PROBLEM!'}")

    # Also verify for one random Q
    Q_rand = make_random_config(lat)
    H_rand = build_hessian(lat, Q_rand, beta)
    eigs_rand = eigvalsh(H_rand)[::-1]
    print(f"\n  One random Q check:")
    print(f"    lambda_max(H(Q)) = {eigs_rand[0]:.8f}")
    print(f"    lambda_max(H(I)) = {eigs_I[0]:.8f}")
    print(f"    lambda_max(H(Q)) < lambda_max(H(I))? {eigs_rand[0] < eigs_I[0] + 1e-10}")

    if lat.d == 2:
        H_rand_fd = build_hessian_fd(lat, Q_rand, beta, h=1e-4)
        diff_rand = np.max(np.abs(H_rand - H_rand_fd))
        print(f"    |H_analytical - H_FD| at random Q = {diff_rand:.2e}")
        print(f"    FD match: {'YES' if diff_rand < 1e-4 else 'NO -- PROBLEM!'}")

    return H_I, eigs_I


# ============================================================================
# Matrix domination test
# ============================================================================

def run_matrix_domination_test(lat, H_I, N_samples=1000, beta=1.0):
    """
    Test whether H(I) - H(Q) >= 0 (PSD) for N_samples random Q.

    Returns detailed statistics.
    """
    print("\n" + "=" * 70)
    print(f"MATRIX DOMINATION TEST: L={lat.L}, d={lat.d}, N_samples={N_samples}")
    print("=" * 70)

    min_eigenvalues = []
    max_eigenvalues = []
    psd_violations = 0
    worst_violation = 0.0
    worst_violation_idx = -1
    worst_Q = None

    t0 = time.time()

    for trial in range(N_samples):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)

        diff = H_I - H_Q
        eigs_diff = eigvalsh(diff)

        min_eig = eigs_diff[0]  # Smallest eigenvalue
        max_eig = eigs_diff[-1]  # Largest eigenvalue

        min_eigenvalues.append(min_eig)
        max_eigenvalues.append(max_eig)

        if min_eig < -1e-10:  # Allow small numerical tolerance
            psd_violations += 1
            if min_eig < worst_violation:
                worst_violation = min_eig
                worst_violation_idx = trial
                worst_Q = Q.copy()

        if (trial + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (trial + 1) / elapsed
            eta = (N_samples - trial - 1) / rate
            print(f"  [{trial+1}/{N_samples}] violations={psd_violations}, "
                  f"min_eig_so_far={min(min_eigenvalues):.6f}, "
                  f"elapsed={elapsed:.1f}s, ETA={eta:.1f}s")

    elapsed = time.time() - t0
    min_eigenvalues = np.array(min_eigenvalues)
    max_eigenvalues = np.array(max_eigenvalues)

    print(f"\n  Completed in {elapsed:.1f}s ({N_samples/elapsed:.1f} configs/sec)")
    print(f"\n  RESULT: PSD violations = {psd_violations}/{N_samples}")
    print(f"\n  Statistics of min eigenvalue of H(I) - H(Q):")
    print(f"    Min:    {min_eigenvalues.min():.8f}")
    print(f"    Max:    {min_eigenvalues.max():.8f}")
    print(f"    Mean:   {min_eigenvalues.mean():.8f}")
    print(f"    Median: {np.median(min_eigenvalues):.8f}")
    print(f"    Std:    {min_eigenvalues.std():.8f}")
    print(f"\n  Statistics of max eigenvalue of H(I) - H(Q):")
    print(f"    Min:    {max_eigenvalues.min():.8f}")
    print(f"    Max:    {max_eigenvalues.max():.8f}")
    print(f"    Mean:   {max_eigenvalues.mean():.8f}")

    if psd_violations > 0:
        print(f"\n  *** COUNTEREXAMPLE FOUND ***")
        print(f"    Worst violation: min eigenvalue = {worst_violation:.8f}")
        print(f"    At trial index: {worst_violation_idx}")
    else:
        print(f"\n  *** H(I) >= H(Q) HOLDS for all {N_samples} samples ***")

    # Distribution: histogram bins for the min eigenvalue
    print(f"\n  Distribution of min_eig(H(I) - H(Q)):")
    percentiles = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]
    for p in percentiles:
        val = np.percentile(min_eigenvalues, p)
        print(f"    {p:3d}th percentile: {val:.6f}")

    return {
        'psd_violations': psd_violations,
        'min_eigenvalues': min_eigenvalues,
        'max_eigenvalues': max_eigenvalues,
        'worst_violation': worst_violation,
        'worst_Q': worst_Q,
    }


# ============================================================================
# Also test majorization (weaker than PSD domination)
# ============================================================================

def check_majorization(eigs_I_sorted, eigs_Q_sorted):
    """
    Check if eigs_I majorizes eigs_Q.
    Both should be sorted in DESCENDING order.

    Majorization: for all m=1,...,n:
        sum_{k=1}^m eigs_I[k] >= sum_{k=1}^m eigs_Q[k]
    AND
        sum_{k=1}^n eigs_I[k] = sum_{k=1}^n eigs_Q[k] (trace equality)

    We check the partial sums inequality (the trace won't be equal in general
    since these are different matrices).
    """
    n = len(eigs_I_sorted)
    cum_I = np.cumsum(eigs_I_sorted)
    cum_Q = np.cumsum(eigs_Q_sorted)
    violations = np.where(cum_Q > cum_I + 1e-10)[0]
    return len(violations) == 0, violations


def run_majorization_test(lat, H_I, N_samples=100, beta=1.0):
    """Test weak majorization: sorted eigenvalues partial sums."""
    print("\n" + "=" * 70)
    print(f"MAJORIZATION TEST: L={lat.L}, d={lat.d}, N_samples={N_samples}")
    print("=" * 70)

    eigs_I = eigvalsh(H_I)[::-1]  # Descending

    violations = 0
    for trial in range(N_samples):
        Q = make_random_config(lat)
        H_Q = build_hessian(lat, Q, beta)
        eigs_Q = eigvalsh(H_Q)[::-1]

        holds, bad_indices = check_majorization(eigs_I, eigs_Q)
        if not holds:
            violations += 1
            if violations <= 3:
                print(f"  Majorization violation at trial {trial}:")
                print(f"    First failing index m={bad_indices[0]}")
                cum_I = np.cumsum(eigs_I)
                cum_Q = np.cumsum(eigs_Q)
                m = bad_indices[0]
                print(f"    sum_I[1:m] = {cum_I[m]:.6f}, sum_Q[1:m] = {cum_Q[m]:.6f}")
                print(f"    Gap: {cum_I[m] - cum_Q[m]:.6f}")

    print(f"\n  RESULT: Majorization violations = {violations}/{N_samples}")
    if violations == 0:
        print(f"  *** Majorization HOLDS for all {N_samples} samples ***")

    return violations


# ============================================================================
# Main
# ============================================================================

def main():
    beta = 1.0

    # -------------------------------------------------------
    # Test d=2 (smallest, fastest — good for validation)
    # -------------------------------------------------------
    print("\n" + "#" * 70)
    print("# DIMENSION d=2")
    print("#" * 70)
    lat2 = Lattice(L=2, d=2)
    H_I_2, eigs_I_2 = run_sanity_checks(lat2, beta)
    results_2 = run_matrix_domination_test(lat2, H_I_2, N_samples=1000, beta=beta)
    run_majorization_test(lat2, H_I_2, N_samples=200, beta=beta)

    # -------------------------------------------------------
    # Test d=3
    # -------------------------------------------------------
    print("\n\n" + "#" * 70)
    print("# DIMENSION d=3")
    print("#" * 70)
    lat3 = Lattice(L=2, d=3)
    H_I_3, eigs_I_3 = run_sanity_checks(lat3, beta)
    results_3 = run_matrix_domination_test(lat3, H_I_3, N_samples=1000, beta=beta)
    run_majorization_test(lat3, H_I_3, N_samples=200, beta=beta)

    # -------------------------------------------------------
    # Test d=4 (main target — 192 DOF, slower)
    # -------------------------------------------------------
    print("\n\n" + "#" * 70)
    print("# DIMENSION d=4")
    print("#" * 70)
    lat4 = Lattice(L=2, d=4)
    H_I_4, eigs_I_4 = run_sanity_checks(lat4, beta)
    # Fewer samples for d=4 due to cost (192x192 Hessian)
    results_4 = run_matrix_domination_test(lat4, H_I_4, N_samples=500, beta=beta)
    run_majorization_test(lat4, H_I_4, N_samples=100, beta=beta)

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------
    print("\n\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    for d_val, res in [(2, results_2), (3, results_3), (4, results_4)]:
        status = "HOLDS" if res['psd_violations'] == 0 else f"FAILS ({res['psd_violations']} violations)"
        print(f"  d={d_val}: H(I) >= H(Q) PSD: {status}")
        print(f"         min_eig range: [{res['min_eigenvalues'].min():.6f}, {res['min_eigenvalues'].max():.6f}]")
        print(f"         mean min_eig: {res['min_eigenvalues'].mean():.6f}")


if __name__ == "__main__":
    main()
