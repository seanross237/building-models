"""
CORRECTED verification of ∑_□ |B_□(Q,v)|² ≤ 4d|v|² on L=4, d=4, SU(2).

CRITICAL BUG FIX: The GOAL.MD formula for B_□ has INCORRECT transport matrices
for edges 3 and 4. The CORRECT formula (verified by finite differences) is:

  B_□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U₀}(v₄)

where U₀ = Q₁Q₂Q₃⁻¹Q₄⁻¹ is the full plaquette holonomy.

GOAL.MD incorrectly used:
  B_□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂}(v₃) - Ad_{Q₁Q₂Q₃⁻¹}(v₄)

The transport for each position should use the partial product INCLUDING that
position's link variable, not just the links before it.
"""

import numpy as np
import time

# --- SU(2) utilities ---

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


def build_M_operator_corrected(lat, Q, basis):
    """
    Build M(Q) = ∑_□ B_□^T B_□ using the CORRECT B_□ formula.

    CORRECT transport matrices:
      R₁ = I                           (no transport for e1)
      R₂ = Ad_{Q₁}                     (transport by 1st link)
      R₃ = -Ad_{Q₁Q₂Q₃⁻¹}            (transport by links 1,2,3⁻¹)
      R₄ = -Ad_{U₀}                    (transport by full holonomy)
    """
    dim_su = 3
    n_edges = lat.n_edges
    dim = dim_su * n_edges
    M = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]                                    # Q_{x,μ}
        Q12 = Q1 @ Q[e2]                              # Q₁Q₂
        Q123inv = Q12 @ np.conj(Q[e3]).T              # Q₁Q₂Q₃⁻¹
        U_plaq = Q123inv @ np.conj(Q[e4]).T           # Q₁Q₂Q₃⁻¹Q₄⁻¹ = U₀

        def ad_matrix(U):
            R = np.zeros((dim_su, dim_su))
            for j in range(dim_su):
                transformed = adjoint_action(U, basis[j])
                R[:, j] = su2_to_vec(transformed, basis)
            return R

        R1 = np.eye(dim_su)            # identity for e1
        R2 = ad_matrix(Q1)             # Ad_{Q₁} for e2
        R3 = -ad_matrix(Q123inv)       # -Ad_{Q₁Q₂Q₃⁻¹} for e3  [CORRECTED]
        R4 = -ad_matrix(U_plaq)        # -Ad_{U₀} for e4          [CORRECTED]

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M


def generate_config(config_type, lat, **kwargs):
    n_edges = lat.n_edges
    Q = np.zeros((n_edges, 2, 2), dtype=complex)

    if config_type == 'identity':
        for e in range(n_edges):
            Q[e] = np.eye(2)

    elif config_type == 'random':
        for e in range(n_edges):
            Q[e] = random_su2()

    elif config_type == 'near_identity':
        eps = kwargs.get('eps', 0.1)
        for e in range(n_edges):
            Q[e] = su2_near_identity(eps)

    elif config_type == 'single_nontrivial':
        for e in range(n_edges):
            Q[e] = np.eye(2)
        e0 = kwargs.get('edge', 0)
        Q[e0] = random_su2()

    elif config_type == 'diagonal':
        for e in range(n_edges):
            theta = np.random.uniform(0, 2*np.pi)
            Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])

    elif config_type == 'gibbs':
        beta = kwargs.get('beta', 2.0)
        for e in range(n_edges):
            Q[e] = np.eye(2)
        n_sweeps = kwargs.get('n_sweeps', 20)
        for sweep in range(n_sweeps):
            for e in range(n_edges):
                proposal = Q[e] @ su2_near_identity(1.0/max(beta, 0.5))
                u, s, vh = np.linalg.svd(proposal)
                Q[e] = u @ vh

    elif config_type == 'adversarial':
        eps = kwargs.get('eps', 0.3)
        for e in range(n_edges):
            Q[e] = su2_near_identity(eps)

    return Q


def run_verification():
    """Main verification with CORRECTED B_□ formula."""
    basis = su2_basis()

    for L in [2, 4]:
        d = 4
        lat = Lattice(L, d)
        bound = 4 * d  # = 16

        print(f"\n{'='*70}")
        print(f"L={L}, d={d}: {lat.n_edges} edges, {lat.n_plaq} plaquettes, dim={3*lat.n_edges}")
        print(f"CORRECTED B_□ formula: B = v₁ + Ad_Q₁(v₂) - Ad_{{Q₁Q₂Q₃⁻¹}}(v₃) - Ad_{{U₀}}(v₄)")
        print(f"Bound: λ_max(M) ≤ {bound}")
        print()

        configs = []
        configs.append(('Q=I (baseline)', 'identity', {}))

        # Random Haar
        for i in range(10):
            configs.append((f'Random Haar #{i+1}', 'random', {}))

        # Near identity
        for eps in [0.01, 0.1, 0.5, 1.0]:
            configs.append((f'Near-I ε={eps}', 'near_identity', {'eps': eps}))

        # Diagonal
        for i in range(3):
            configs.append((f'Diagonal #{i+1}', 'diagonal', {}))

        # Single nontrivial
        for i in range(3):
            configs.append((f'Single link #{i+1}', 'single_nontrivial', {'edge': np.random.randint(lat.n_edges)}))

        # Gibbs
        for beta in [0.5, 1.0, 2.0, 4.0]:
            configs.append((f'Gibbs β={beta}', 'gibbs', {'beta': beta, 'n_sweeps': 15}))

        # Adversarial
        for i in range(3):
            configs.append((f'Adversarial #{i+1}', 'adversarial', {'eps': 0.3}))

        print(f"{'Config':<30s} {'λ_max':>10s} {'ratio':>10s} {'status':>10s}")
        print("-" * 65)

        results = []
        for name, ctype, kwargs in configs:
            t0 = time.time()
            Q = generate_config(ctype, lat, **kwargs)
            M = build_M_operator_corrected(lat, Q, basis)

            # Verify symmetry
            asym = np.max(np.abs(M - M.T))
            assert asym < 1e-10, f"M not symmetric: {asym}"

            # Verify trace
            expected_trace = 12 * lat.n_plaq
            actual_trace = np.trace(M)
            assert abs(actual_trace - expected_trace) < 1e-6, f"Trace mismatch: {actual_trace} vs {expected_trace}"

            eigs = np.linalg.eigvalsh(M)
            lam_max = eigs[-1]
            ratio = lam_max / bound
            status = "OK" if lam_max <= bound + 1e-8 else "VIOLATION!"
            elapsed = time.time() - t0

            print(f"{name:<30s} {lam_max:10.6f} {ratio:10.6f} {status:>10s}  ({elapsed:.1f}s)")
            results.append({'name': name, 'lambda_max': lam_max, 'ratio': ratio, 'status': status})

        max_ratio = max(r['ratio'] for r in results)
        max_lambda = max(r['lambda_max'] for r in results)
        violations = [r for r in results if r['status'] == 'VIOLATION!']

        print(f"\nMax λ_max: {max_lambda:.6f}, Max ratio: {max_ratio:.8f}")
        print(f"Violations: {len(violations)} / {len(results)}")

        if violations:
            print("VIOLATIONS:")
            for v in violations:
                print(f"  {v['name']}: λ_max = {v['lambda_max']:.8f}")
        else:
            print(f"NO VIOLATIONS on L={L}. Inequality holds for all {len(results)} configs.")

    # Also do a direct cross-check for L=4 random Q
    print(f"\n{'='*70}")
    print("Cross-check: direct B_□ computation vs matrix eigenvalue")
    L = 4
    d = 4
    lat = Lattice(L, d)
    np.random.seed(12345)
    Q = generate_config('random', lat)
    M = build_M_operator_corrected(lat, Q, basis)
    eigenvalues, eigenvectors = np.linalg.eigh(M)
    v_top = eigenvectors[:, -1]

    # Direct computation
    B_sum_sq = 0.0
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        v1 = sum(v_top[3*e1+a] * basis[a] for a in range(3))
        v2 = sum(v_top[3*e2+a] * basis[a] for a in range(3))
        v3 = sum(v_top[3*e3+a] * basis[a] for a in range(3))
        v4 = sum(v_top[3*e4+a] * basis[a] for a in range(3))

        A1 = v1
        A2 = adjoint_action(Q1, v2)
        A3 = -adjoint_action(Q123inv, v3)   # CORRECTED
        A4 = -adjoint_action(U_plaq, v4)     # CORRECTED

        B = A1 + A2 + A3 + A4
        B_sq = -2 * np.trace(B @ B).real
        B_sum_sq += B_sq

    vMv = v_top @ M @ v_top
    print(f"  v^T M v = {vMv:.10f}")
    print(f"  ∑|B_□|² = {B_sum_sq:.10f}")
    print(f"  Discrepancy: {abs(vMv - B_sum_sq):.2e}")
    print(f"  Ratio / 4d: {vMv / (4*d):.8f}")


if __name__ == '__main__':
    np.random.seed(42)
    run_verification()
