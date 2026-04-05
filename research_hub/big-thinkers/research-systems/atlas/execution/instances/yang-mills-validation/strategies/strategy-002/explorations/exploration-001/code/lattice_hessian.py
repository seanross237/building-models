"""
Lattice SU(2) Yang-Mills: Hessian computation and λ_max inequality stress test.

Conventions:
- SU(2), N=2, generators T_a = i σ_a / 2 for a=1,2,3
- Inner product: <X,Y> = -2 Tr(X Y), so |T_a|² = 1
- Wilson action: S(Q) = -(β/N) Σ_□ Re Tr(U_□) = -(β/2) Σ_□ Re Tr(U_□)
- LEFT perturbation: Q → exp(ε v) Q
- Adjoint action: Ad_Q(v) = Q v Q⁻¹
- L=2 hypercubic torus, d=4, periodic BC
"""

import numpy as np
from numpy.linalg import eigvalsh, norm, det
from scipy.linalg import expm
import sys
import time

# ===================== SU(2) Basics =====================

# Pauli matrices
sigma = np.array([
    [[0, 1], [1, 0]],       # σ₁
    [[0, -1j], [1j, 0]],    # σ₂
    [[1, 0], [0, -1]],      # σ₃
], dtype=complex)

# su(2) generators: T_a = i σ_a / 2
T = np.array([1j * sigma[a] / 2 for a in range(3)])

# Check: -2 Tr(T_a T_b) = δ_ab
for a in range(3):
    for b in range(3):
        val = -2 * np.trace(T[a] @ T[b])
        expected = 1.0 if a == b else 0.0
        assert abs(val - expected) < 1e-14, f"Inner product check failed: <T_{a},T_{b}> = {val}"

def su2_exp(v):
    """Exponential map: v ∈ R³ → exp(Σ v_a T_a) ∈ SU(2)."""
    X = sum(v[a] * T[a] for a in range(3))
    return expm(X)

def project_su2(U):
    """Project a 2×2 matrix to SU(2) via U → U / sqrt(det(U))."""
    d = det(U)
    U = U / np.sqrt(d)
    # Enforce unitarity
    U = (U + np.linalg.inv(U).conj().T) / 2
    d = det(U)
    U = U / np.sqrt(d)
    return U

def haar_random_su2():
    """Sample Haar-random SU(2) element."""
    # Use quaternion parameterization
    x = np.random.randn(4)
    x = x / norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ], dtype=complex)

def adjoint_action(Q, v_coeffs):
    """
    Adjoint action Ad_Q(v) = Q v Q⁻¹ where v = Σ v_a T_a.
    Returns the coefficients of the result in the T_a basis.
    """
    v_mat = sum(v_coeffs[a] * T[a] for a in range(3))
    Qinv = np.linalg.inv(Q)
    result_mat = Q @ v_mat @ Qinv
    # Project onto T_a basis: v_a = -2 Tr(T_a · result)
    result_coeffs = np.zeros(3)
    for a in range(3):
        result_coeffs[a] = -2 * np.trace(T[a] @ result_mat).real
    return result_coeffs

def adjoint_matrix(Q):
    """
    3×3 matrix R such that Ad_Q(v) = R v (in T_a coefficients).
    R_ab = -2 Tr(T_a Q T_b Q⁻¹)
    """
    Qinv = np.linalg.inv(Q)
    R = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            R[a, b] = -2 * np.trace(T[a] @ Q @ T[b] @ Qinv).real
    return R


# ===================== Lattice Setup =====================

class Lattice:
    """L^d periodic hypercubic lattice."""

    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_links = self.n_sites * d  # directed links (one per site per direction)
        self.n_dof = self.n_links * 3    # total degrees of freedom

        # Site coordinates: site index → (x₀, x₁, ..., x_{d-1})
        self.coords = np.array(np.unravel_index(
            np.arange(self.n_sites), [L]*d
        )).T  # shape (n_sites, d)

        # Site index from coordinates
        self._coord_to_idx = {}
        for i in range(self.n_sites):
            self._coord_to_idx[tuple(self.coords[i])] = i

    def site_index(self, coords):
        """Convert coordinates (with periodic BC) to site index."""
        c = tuple(c % self.L for c in coords)
        return self._coord_to_idx[c]

    def neighbor(self, site, mu):
        """Site index of neighbor of site in direction mu."""
        c = list(self.coords[site])
        c[mu] = (c[mu] + 1) % self.L
        return self.site_index(c)

    def neighbor_back(self, site, mu):
        """Site index of neighbor of site in direction -mu."""
        c = list(self.coords[site])
        c[mu] = (c[mu] - 1) % self.L
        return self.site_index(c)

    def link_index(self, site, mu):
        """Index of the link starting at site in direction mu."""
        return site * self.d + mu

    def plaquettes(self):
        """
        Enumerate all plaquettes. Each plaquette is in the (mu, nu) plane
        with mu < nu, starting at each site.

        Returns list of plaquettes, each is a list of (link_idx, is_forward).
        A plaquette U_□ = U_{e₁} U_{e₂} U_{e₃}⁻¹ U_{e₄}⁻¹ where:
        - e₁: site x, direction mu (forward)
        - e₂: site x+μ̂, direction nu (forward)
        - e₃: site x+ν̂, direction mu (forward, traversed backward → U⁻¹)
        - e₄: site x, direction nu (forward, traversed backward → U⁻¹)
        """
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.neighbor(x, mu)
                    x_nu = self.neighbor(x, nu)

                    e1 = self.link_index(x, mu)       # x → x+μ̂
                    e2 = self.link_index(x_mu, nu)     # x+μ̂ → x+μ̂+ν̂
                    e3 = self.link_index(x_nu, mu)     # x+ν̂ → x+ν̂+μ̂ (traversed backward)
                    e4 = self.link_index(x, nu)        # x → x+ν̂ (traversed backward)

                    plaq_list.append({
                        'edges': [e1, e2, e3, e4],
                        'forward': [True, True, False, False],
                        'site': x,
                        'mu': mu,
                        'nu': nu
                    })
        return plaq_list


# ===================== Wilson Action =====================

def wilson_action(Q, lattice, beta):
    """
    S(Q) = -(β/2) Σ_□ Re Tr(U_□)
    where U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹

    Q: array of shape (n_links, 2, 2), SU(2) matrices on each link
    """
    S = 0.0
    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']
        U_plaq = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])
        S -= (beta / 2) * np.trace(U_plaq).real
    return S


# ===================== Finite-Difference Hessian =====================

def compute_hessian_fd(Q, lattice, beta, h=1e-4):
    """
    Compute the Hessian of S(Q) using central finite differences.

    Perturbation: Q_e → exp(ε T_a) Q_e (LEFT perturbation)

    H[(e,a), (f,b)] = ∂²S / ∂ε_a^e ∂ε_b^f

    Using central differences:
    - Diagonal: (S(+h) - 2S(0) + S(-h)) / h²
    - Off-diagonal: (S(+h,+h) - S(+h,-h) - S(-h,+h) + S(-h,-h)) / (4h²)
    """
    n = lattice.n_dof
    H = np.zeros((n, n))
    S0 = wilson_action(Q, lattice, beta)

    def perturb(Q_orig, link_idx, color_idx, eps):
        """Return perturbed configuration: Q_e → exp(eps * T_a) Q_e"""
        Q_new = Q_orig.copy()
        v = np.zeros(3)
        v[color_idx] = eps
        Q_new[link_idx] = su2_exp(v) @ Q_orig[link_idx]
        return Q_new

    # Pre-compute single perturbations for efficiency
    S_plus = np.zeros(n)
    S_minus = np.zeros(n)

    for i in range(n):
        e_i = i // 3
        a_i = i % 3
        Q_plus = perturb(Q, e_i, a_i, h)
        Q_minus = perturb(Q, e_i, a_i, -h)
        S_plus[i] = wilson_action(Q_plus, lattice, beta)
        S_minus[i] = wilson_action(Q_minus, lattice, beta)

    # Diagonal elements
    for i in range(n):
        H[i, i] = (S_plus[i] - 2*S0 + S_minus[i]) / h**2

    # Off-diagonal elements (only upper triangle, then symmetrize)
    for i in range(n):
        e_i = i // 3
        a_i = i % 3
        for j in range(i+1, n):
            e_j = j // 3
            a_j = j % 3

            # S(+h_i, +h_j)
            Q_pp = perturb(Q, e_i, a_i, h)
            Q_pp = perturb(Q_pp, e_j, a_j, h)
            S_pp = wilson_action(Q_pp, lattice, beta)

            # S(+h_i, -h_j)
            Q_pm = perturb(Q, e_i, a_i, h)
            Q_pm = perturb(Q_pm, e_j, a_j, -h)
            S_pm = wilson_action(Q_pm, lattice, beta)

            # S(-h_i, +h_j)
            Q_mp = perturb(Q, e_i, a_i, -h)
            Q_mp = perturb(Q_mp, e_j, a_j, h)
            S_mp = wilson_action(Q_mp, lattice, beta)

            # S(-h_i, -h_j)
            Q_mm = perturb(Q, e_i, a_i, -h)
            Q_mm = perturb(Q_mm, e_j, a_j, -h)
            S_mm = wilson_action(Q_mm, lattice, beta)

            H[i, j] = (S_pp - S_pm - S_mp + S_mm) / (4 * h**2)
            H[j, i] = H[i, j]

    return H


# ===================== B² Formula Hessian =====================

def compute_hessian_formula(Q, lattice, beta):
    """
    Compute H_formula = (β/(2N)) Σ_□ B□ᵀ B□

    For each plaquette with edges e₁,e₂,e₃,e₄ (e₃,e₄ backward):
    B□(v) = v₁ + Ad_{P₂}(v₂) - Ad_{P₃}(v₃) - Ad_{P₄}(v₄)

    where:
    P₁ = I
    P₂ = Q_{e₁}
    P₃ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹
    P₄ = U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹

    B□ is a linear map from R^{n_dof} → R³ (su(2) valued).
    B□ᵀ B□ is the contribution from this plaquette to M(Q).
    """
    N = 2  # SU(2)
    n = lattice.n_dof
    M = np.zeros((n, n))

    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']

        # Compute transport operators
        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3])
        P4 = Q[e1] @ Q[e2] @ np.linalg.inv(Q[e3]) @ np.linalg.inv(Q[e4])

        # Adjoint representation matrices (3×3)
        R2 = adjoint_matrix(P2)   # Ad_{P₂}
        R3 = adjoint_matrix(P3)   # Ad_{P₃}
        R4 = adjoint_matrix(P4)   # Ad_{P₄}

        # B□ is a 3 × n_dof matrix
        # B□(v)_a = Σ_{f,b} B_mat[a, f*3+b] * v_{f,b}
        # Only edges e1,e2,e3,e4 contribute
        B_mat = np.zeros((3, n))

        # e₁: coefficient is I (identity 3×3)
        for a in range(3):
            B_mat[a, e1*3 + a] += 1.0

        # e₂: coefficient is +R₂ (adjoint of P₂)
        for a in range(3):
            for b in range(3):
                B_mat[a, e2*3 + b] += R2[a, b]

        # e₃: coefficient is -R₃ (adjoint of P₃, but edge traversed backward)
        for a in range(3):
            for b in range(3):
                B_mat[a, e3*3 + b] -= R3[a, b]

        # e₄: coefficient is -R₄ (adjoint of P₄, edge traversed backward)
        for a in range(3):
            for b in range(3):
                B_mat[a, e4*3 + b] -= R4[a, b]

        # Contribution to M: B□ᵀ B□
        M += B_mat.T @ B_mat

    # H_formula = (β/(2N)) M
    H_formula = (beta / (2 * N)) * M
    return H_formula


# ===================== Main Routines =====================

def stage1_identity_check(lattice, beta=1.0):
    """Stage 1: Verify both Hessians match at Q = I."""
    print("=" * 60)
    print("STAGE 1: Identity Configuration Check")
    print("=" * 60)

    n_links = lattice.n_links
    Q = np.array([np.eye(2, dtype=complex) for _ in range(n_links)])

    # Wilson action at identity
    S0 = wilson_action(Q, lattice, beta)
    n_plaq = len(lattice.plaquettes())
    S_expected = -(beta/2) * n_plaq * 2  # Tr(I₂) = 2
    print(f"S(I) = {S0:.6f}, expected = {S_expected:.6f}, diff = {abs(S0 - S_expected):.2e}")

    print("\nComputing H_actual (finite differences)...")
    t0 = time.time()
    H_actual = compute_hessian_fd(Q, lattice, beta, h=1e-4)
    t1 = time.time()
    print(f"  Done in {t1-t0:.1f}s")

    print("Computing H_formula (B² formula)...")
    t0 = time.time()
    H_formula = compute_hessian_formula(Q, lattice, beta)
    t1 = time.time()
    print(f"  Done in {t1-t0:.1f}s")

    # Check symmetry
    asym_actual = norm(H_actual - H_actual.T)
    asym_formula = norm(H_formula - H_formula.T)
    print(f"\nSymmetry check:")
    print(f"  ||H_actual - H_actual^T|| = {asym_actual:.2e}")
    print(f"  ||H_formula - H_formula^T|| = {asym_formula:.2e}")

    # Symmetrize for safety
    H_actual = (H_actual + H_actual.T) / 2
    H_formula = (H_formula + H_formula.T) / 2

    # Compare matrices
    diff = norm(H_actual - H_formula)
    rel_diff = diff / max(norm(H_actual), 1e-15)
    print(f"\n||H_actual - H_formula|| = {diff:.2e}")
    print(f"Relative difference = {rel_diff:.2e}")

    # Eigenvalues
    eigs_actual = eigvalsh(H_actual)
    eigs_formula = eigvalsh(H_formula)

    lmax_actual = eigs_actual[-1]
    lmax_formula = eigs_formula[-1]

    print(f"\nλ_max(H_actual) = {lmax_actual:.6f}")
    print(f"λ_max(H_formula) = {lmax_formula:.6f}")
    print(f"Expected λ_max = {4*beta:.6f}")
    print(f"Diff from expected: actual={abs(lmax_actual - 4*beta):.2e}, formula={abs(lmax_formula - 4*beta):.2e}")

    # Eigenvalue comparison
    print(f"\nTop 10 eigenvalues:")
    print(f"{'H_actual':>15s} {'H_formula':>15s} {'diff':>15s}")
    for i in range(-1, -11, -1):
        print(f"{eigs_actual[i]:15.8f} {eigs_formula[i]:15.8f} {abs(eigs_actual[i]-eigs_formula[i]):15.2e}")

    # Check r
    r = lmax_actual / lmax_formula if lmax_formula > 0 else float('inf')
    print(f"\nr = λ_max(H_actual) / λ_max(H_formula) = {r:.10f}")

    passed = abs(r - 1.0) < 0.01 and rel_diff < 0.01
    print(f"\nStage 1 {'PASSED' if passed else 'FAILED'}")

    return passed, {
        'H_actual': H_actual,
        'H_formula': H_formula,
        'lmax_actual': lmax_actual,
        'lmax_formula': lmax_formula,
        'r': r,
        'diff': diff,
        'rel_diff': rel_diff
    }


def compute_ratio(Q, lattice, beta, h=1e-4):
    """Compute r(Q) = λ_max(H_actual) / λ_max(H_formula)."""
    H_actual = compute_hessian_fd(Q, lattice, beta, h)
    H_formula = compute_hessian_formula(Q, lattice, beta)

    H_actual = (H_actual + H_actual.T) / 2
    H_formula = (H_formula + H_formula.T) / 2

    eigs_actual = eigvalsh(H_actual)
    eigs_formula = eigvalsh(H_formula)

    lmax_actual = eigs_actual[-1]
    lmax_formula = eigs_formula[-1]

    r = lmax_actual / lmax_formula if lmax_formula > 1e-15 else float('inf')

    # C(Q) = H_formula - H_actual
    C = H_formula - H_actual
    eigs_C = eigvalsh(C)

    return {
        'r': r,
        'lmax_actual': lmax_actual,
        'lmax_formula': lmax_formula,
        'C_norm': norm(C, 2),  # operator norm
        'C_min_eig': eigs_C[0],
        'C_max_eig': eigs_C[-1],
        'H_actual': H_actual,
        'H_formula': H_formula,
    }


def random_su2_config(lattice):
    """Generate Haar-random SU(2) on all links."""
    return np.array([haar_random_su2() for _ in range(lattice.n_links)])


def stage2_random_configs(lattice, beta=1.0, n_configs=50):
    """Stage 2: Test r(Q) on random configurations."""
    print("\n" + "=" * 60)
    print(f"STAGE 2: Random Configurations ({n_configs} configs)")
    print("=" * 60)

    results = []
    worst_r = -1
    worst_config = None

    for i in range(n_configs):
        Q = random_su2_config(lattice)
        t0 = time.time()
        res = compute_ratio(Q, lattice, beta)
        t1 = time.time()

        results.append(res)

        if res['r'] > worst_r:
            worst_r = res['r']
            worst_config = Q.copy()
            worst_res = res

        print(f"  Config {i+1:3d}: r = {res['r']:.8f}, λ_act = {res['lmax_actual']:.6f}, "
              f"λ_form = {res['lmax_formula']:.6f}, ||C||_op = {res['C_norm']:.6f} "
              f"({t1-t0:.1f}s)")

        if res['r'] > 1.0:
            print(f"\n  *** VIOLATION FOUND: r = {res['r']:.10f} > 1.0 ***")
            return results, worst_config, worst_res

    rs = [r['r'] for r in results]
    print(f"\nStatistics:")
    print(f"  mean(r) = {np.mean(rs):.8f}")
    print(f"  max(r)  = {np.max(rs):.8f}")
    print(f"  min(r)  = {np.min(rs):.8f}")
    print(f"  std(r)  = {np.std(rs):.8f}")
    print(f"  gap     = {1 - np.max(rs):.8f}")

    return results, worst_config, worst_res


if __name__ == '__main__':
    # Use smaller lattice first for speed: L=2, d=2 for debugging, then L=2, d=4
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, default=1)
    parser.add_argument('--L', type=int, default=2)
    parser.add_argument('--d', type=int, default=4)
    parser.add_argument('--beta', type=float, default=1.0)
    parser.add_argument('--n_configs', type=int, default=50)
    args = parser.parse_args()

    print(f"Lattice: L={args.L}, d={args.d}")
    lat = Lattice(args.L, args.d)
    print(f"Sites: {lat.n_sites}, Links: {lat.n_links}, DOF: {lat.n_dof}")
    print(f"Plaquettes: {len(lat.plaquettes())}")
    print(f"β = {args.beta}")

    if args.stage == 1:
        passed, info = stage1_identity_check(lat, args.beta)
        if not passed:
            print("\nStage 1 FAILED. Stopping.")
            sys.exit(1)

    elif args.stage == 2:
        results, worst_Q, worst_res = stage2_random_configs(lat, args.beta, args.n_configs)
