"""
Compute the ACTUAL Hessian of the Yang-Mills action on L=4, d=4, SU(2),
and verify H_norm ≤ 1/12 even for configurations that violate the B_□ bound.

The Hessian of S = -(β/N) Σ Re Tr(U_□) is:

  HessS(v,v) = -(β/N) Σ_□ [ Re Tr(B_□(v)² U_□) + Re Tr(D_□(v) U_□) ]

where B_□ is the first-order variation (covariant curl) and D_□ are diagonal
(second-order) terms from varying the same link twice.

Actually, the exact Hessian for lattice gauge theory at a general configuration Q:

For the action S(Q) = -(β/N) Σ_□ Re Tr(U_□(Q)):

d²S/dt² |_{t=0} for Q → Q e^{tv} involves:
  - First-order contribution squared: ~ Tr(B² U)
  - Second-order contribution: ~ Tr(v² terms ... U)

The per-plaquette Hessian for tangent vectors v, w is:

  H_□(v,w) = -(β/N) Re Tr( (dU_□/dv)(dU_□/dw) U_□^{-1} + d²U_□/dv dw ) × U_□^{-1} ...

This gets complicated. Let me use the correct formula.

For a plaquette U_□ = P₁ P₂ P₃ P₄ where P_i are link variables (or their inverses),
the variation Q_e → Q_e exp(t v_e) gives:

dU_□/dt = Σ_i (Ã_i) U_□

where Ã_i is the adjoint-transported tangent at the i-th position.

So d²U_□/dt² = (Σ_i Ã_i)² U_□ + Σ_i (dÃ_i/dt) U_□

The second term (dÃ_i/dt) comes from the fact that Ã_i depends on the link variables
being varied. When we vary link e, and Ã_i involves Ad_{...Q_e...}(v_f), the
variation hits the adjoint transport AND the tangent vector.

For the QUADRATIC form (all variations in the same direction v):
d²S/dt² = -(β/N) Σ_□ Re Tr[ d²U_□/dt² · U_□^{-1} ]

d²U_□/dt² = (Σ_i Ã_i)² U_□ + Σ_{edges e in □} [second-order variation terms from e] U_□

The key point: for a SINGLE link e appearing once in plaquette □, the second-order
variation from varying Q_e → Q_e exp(tv_e) gives a term v_e² in the appropriate
position. But this is a NEGATIVE definite contribution to the Hessian (it involves
-Re Tr(v² U) which is non-positive for U near identity).

The SIMPLIFIED approach (following E008): the Hessian at configuration Q is

HessS(v,v) = (β/N) Σ_□ [ Re Tr(B_□(v)² U_□) - Σ_{e∈□} Re Tr(v_e² U_□^{(e)}) ]

where U_□^{(e)} is the plaquette holonomy "as seen from edge e" (suitably transported).

Actually, let me take a step back and just compute numerically. We can compute the
Hessian by FINITE DIFFERENCES: perturb Q along direction v, compute S(Q exp(tv)),
and take the second derivative numerically.

This is the most reliable approach for verification.
"""

import numpy as np
import time

# --- SU(2) utilities (same as before) ---

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct = np.cos(theta / 2)
    st = np.sin(theta / 2)
    return np.array([
        [ct + 1j*st*n[2], st*(1j*n[0] + n[1])],
        [st*(1j*n[0] - n[1]), ct - 1j*st*n[2]]
    ])

def su2_near_identity(eps):
    coeffs = np.random.randn(3)
    coeffs /= np.linalg.norm(coeffs)
    coeffs *= eps
    return su2_exp(coeffs)

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]

def su2_to_vec(A, basis):
    return np.array([-2 * np.trace(b @ A).real for b in basis])

# --- Lattice ---

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        for i in range(self.d - 1, -1, -1):
            coords.append(idx % self.L)
            idx //= self.L
        return list(reversed(coords))

    def edge_index(self, site_idx, mu):
        return site_idx * self.d + mu

    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)

    def plaquettes(self):
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu)
                    x_nu = self.shifted_site(x, nu)
                    e1 = self.edge_index(x, mu)
                    e2 = self.edge_index(x_mu, nu)
                    e3 = self.edge_index(x_nu, mu)
                    e4 = self.edge_index(x, nu)
                    plaq_list.append((e1, e2, e3, e4, x, mu, nu))
        return plaq_list


def compute_action(Q, lat):
    """
    Compute S(Q) = -(1/N) Σ_□ Re Tr(U_□)
    (without β factor, which is applied outside)
    """
    N = 2
    S = 0.0
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        U_plaq = Q[e1] @ Q[e2] @ np.conj(Q[e3]).T @ np.conj(Q[e4]).T
        S -= (1.0/N) * np.trace(U_plaq).real
    return S


def perturb_config(Q, v_flat, t, basis, lat):
    """
    Perturb Q → Q exp(t v): Q_e → exp(t v_e) Q_e
    v_flat: flat vector of tangent components
    """
    dim_su = 3
    Q_new = np.copy(Q)
    for e in range(lat.n_edges):
        # v_e in su(2)
        coeffs = v_flat[dim_su*e:dim_su*e+dim_su]
        A = sum(c * T for c, T in zip(coeffs, basis))
        # exp(tA) Q_e  -- A is anti-Hermitian
        exp_tA = su2_exp(t * coeffs)  # this uses the vector form
        Q_new[e] = exp_tA @ Q[e]
    return Q_new


def hessian_finite_diff(Q, v_flat, lat, basis, h=1e-5):
    """
    Compute d²S/dt²|_{t=0} for Q → Q exp(tv) via finite differences.
    Uses 5-point stencil for accuracy.
    """
    S0 = compute_action(Q, lat)
    Sp = compute_action(perturb_config(Q, v_flat, h, basis, lat), lat)
    Sm = compute_action(perturb_config(Q, v_flat, -h, basis, lat), lat)
    Sp2 = compute_action(perturb_config(Q, v_flat, 2*h, basis, lat), lat)
    Sm2 = compute_action(perturb_config(Q, v_flat, -2*h, basis, lat), lat)

    # 5-point stencil: f'' ≈ (-f(2h) + 16f(h) - 30f(0) + 16f(-h) - f(-2h)) / (12h²)
    d2S = (-Sp2 + 16*Sp - 30*S0 + 16*Sm - Sm2) / (12 * h**2)
    return d2S


def build_hessian_matrix_fd(Q, lat, basis, h=1e-4):
    """
    Build the full Hessian matrix by finite differences.
    H_{ij} = d²S / dv_i dv_j

    For efficiency, use: H_{ij} = (S(v_i+h, v_j+h) - S(v_i+h) - S(v_j+h) + S(0)) / h²
    But this requires O(n²) evaluations. For n=3072 this is ~10M evaluations = too slow.

    Instead, compute H v for specific vectors v using finite differences,
    and use the Lanczos method to find the top eigenvalue.
    """
    pass  # Use power iteration instead


def power_iteration_hessian(Q, lat, basis, n_iter=100, h=1e-5):
    """
    Find the maximum eigenvalue of the Hessian using power iteration.

    Hv ≈ (gradient(Q + hv) - gradient(Q - hv)) / (2h)

    But computing gradient is also expensive. Use instead:
    Hv·w = d²S/dt ds for Q → Q exp(tv + sw)

    Actually, let's just use the Rayleigh quotient:
    R(v) = v^T H v / v^T v = d²S/dt² / |v|²

    And do random search over directions to find the max.
    """
    dim = 3 * lat.n_edges
    best_ratio = -np.inf
    best_v = None

    # Try random directions
    for i in range(n_iter):
        v = np.random.randn(dim)
        v /= np.linalg.norm(v)

        d2S = hessian_finite_diff(Q, v, lat, basis, h=h)
        ratio = d2S  # since |v|=1

        if ratio > best_ratio:
            best_ratio = ratio
            best_v = v.copy()

    return best_ratio, best_v


def run_hessian_check():
    """
    Check H_norm on L=4 for configurations that violate the B_□ bound.

    H_norm = HessS(v,v) / (8(d-1)Nβ|v|²) should be ≤ 1/12.

    Actually, HessS = β × d²S_0/dt² where S_0 = -(1/N)ΣReTr(U_□).

    So H_norm = β × d²S_0/dt² / (8(d-1)Nβ|v|²) = d²S_0/dt² / (8(d-1)N|v|²)

    For SU(2) (N=2), d=4: denominator = 8 × 3 × 2 = 48.
    H_norm = d²S_0/(48|v|²)

    If H_norm ≤ 1/12, then d²S_0/|v|² ≤ 48/12 = 4.

    Wait, let's be more careful. From E008:

    H_norm = max_v HessS(v,v) / (8(d-1)Nβ|v|²)

    The Bakry-Emery condition is K_S > 0 where:
    K_S = 1 - 4β × N × H_norm × something...

    Let me just compute the raw Hessian eigenvalue and the B_□ eigenvalue
    for the same configurations, to see if the Hessian is indeed smaller.
    """

    L = 4
    d = 4
    N = 2
    lat = Lattice(L, d)
    basis = su2_basis()
    dim = 3 * lat.n_edges  # 3072

    print(f"L={L}, d={d}, N={N}, dim={dim}")
    print(f"Checking Hessian vs B_□ bound for violating configurations\n")

    # First, on a smaller lattice L=2 as sanity check
    for L_test in [2, 4]:
        lat_test = Lattice(L_test, d)
        dim_test = 3 * lat_test.n_edges
        print(f"\n{'='*60}")
        print(f"L={L_test}: dim={dim_test}")

        for config_name, config_seed in [('Q=I', None), ('Random Haar', 12345), ('Random Haar 2', 99999)]:
            if config_seed is not None:
                np.random.seed(config_seed)

            Q = np.zeros((lat_test.n_edges, 2, 2), dtype=complex)
            if config_name == 'Q=I':
                for e in range(lat_test.n_edges):
                    Q[e] = np.eye(2)
            else:
                for e in range(lat_test.n_edges):
                    Q[e] = random_su2()

            # Compute B_□ max eigenvalue (via direct computation for large L)
            # For efficiency, just compute Rayleigh quotient on random vectors
            # and on the specific "staggered mode" for Q=I

            n_trial = 200
            best_B_ratio = 0.0
            best_H_ratio = 0.0

            for trial in range(n_trial):
                if config_name == 'Q=I' and trial == 0:
                    # Use staggered mode
                    v = np.zeros(dim_test)
                    for x in range(lat_test.n_sites):
                        coords = lat_test.site_coords(x)
                        for mu in range(d):
                            e = lat_test.edge_index(x, mu)
                            sign = (-1)**(sum(coords) + mu)
                            v[3*e] = sign  # first su(2) component
                    v /= np.linalg.norm(v)
                else:
                    v = np.random.randn(dim_test)
                    v /= np.linalg.norm(v)

                # B_□ quadratic form: ∑_□ |B_□(Q,v)|²
                B_sum_sq = 0.0
                for (e1, e2, e3, e4, x, mu, nu) in lat_test.plaquettes():
                    Q1 = Q[e1]
                    Q12 = Q1 @ Q[e2]
                    Q123inv = Q12 @ np.conj(Q[e3]).T

                    # Reconstruct v_e as su(2) elements
                    v1 = sum(v[3*e1+a] * basis[a] for a in range(3))
                    v2 = sum(v[3*e2+a] * basis[a] for a in range(3))
                    v3 = sum(v[3*e3+a] * basis[a] for a in range(3))
                    v4 = sum(v[3*e4+a] * basis[a] for a in range(3))

                    A1 = v1
                    A2 = adjoint_action(Q1, v2)
                    A3 = -adjoint_action(Q12, v3)
                    A4 = -adjoint_action(Q123inv, v4)

                    B = A1 + A2 + A3 + A4
                    B_sq = -2 * np.trace(B @ B).real
                    B_sum_sq += B_sq

                B_ratio = B_sum_sq / (4 * d)  # should be ≤ 1 if |v|=1
                if B_ratio > best_B_ratio:
                    best_B_ratio = B_ratio

                # Hessian via finite differences
                d2S = hessian_finite_diff(Q, v, lat_test, basis, h=1e-5)
                # H_norm = d2S / (8(d-1)N) for β=1, |v|=1
                # But actually d2S = d²S_0/dt² where S_0 = -(1/N)ΣReTr
                # The actual HessS = β × d2S
                # We want: max d2S over unit v. Then H_norm = max_d2S / (8(d-1)N)
                H_ratio = d2S / (4 * d)  # compare with B_□ scale
                if d2S > best_H_ratio:
                    best_H_ratio = d2S

            H_norm = best_H_ratio / (8 * (d-1) * N)

            print(f"\n  {config_name} (seed={config_seed}):")
            print(f"    B_□ max ratio (over {n_trial} random v): {best_B_ratio:.6f} (bound: 1.0)")
            print(f"    Hessian d²S max (over {n_trial} random v): {best_H_ratio:.6f}")
            print(f"    H_norm estimate: {H_norm:.6f} (bound: {1/12:.6f})")

            if L_test == 2:
                break  # Only do Q=I for L=2 sanity check on timing


if __name__ == '__main__':
    run_hessian_check()
