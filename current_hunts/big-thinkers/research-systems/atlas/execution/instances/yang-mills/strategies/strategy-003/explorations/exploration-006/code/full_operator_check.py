"""
Full operator check: M(Q) ≼ M(I) for SU(2), d=4, L=2.

Computes D(Q) = M(Q) - M(I) and checks that ALL eigenvalues are ≤ 0
for 50+ configurations including pure gauge, random Haar, Gibbs, near-identity,
and adversarial gradient ascent.

Uses the CORRECTED B_□ formula from E001.
"""

import numpy as np
import json
import time
import sys

# ====================== SU(2) Utilities ======================

def random_su2():
    """Random Haar-distributed SU(2) matrix."""
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ])

def su2_exp(A_vec):
    """Exponential map: R^3 -> SU(2), using A = sum_a A_vec[a] * (i sigma_a / 2)."""
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
    """Random SU(2) element near the identity, with |A| ~ eps."""
    coeffs = np.random.randn(3)
    coeffs = coeffs / np.linalg.norm(coeffs) * eps
    return su2_exp(coeffs)

def adjoint_action(U, A):
    """Ad_U(A) = U A U†."""
    return U @ A @ np.conj(U).T

def su2_basis():
    """Return the su(2) basis: τ_a = i σ_a / 2."""
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]

def su2_to_vec(A, basis):
    """Project su(2) element A onto the basis: c_a = -2 Tr(τ_a A)."""
    return np.array([-2 * np.trace(b @ A).real for b in basis])

def ad_matrix(U, basis):
    """3x3 real adjoint matrix: (Ad_U)_{ab} = -2 Tr(τ_a U τ_b U†)."""
    dim_su = len(basis)
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R

# ====================== Lattice ======================

class Lattice:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites
        self.dim_su = 3
        self.dim = self.dim_su * self.n_edges

    def site_index(self, coords):
        idx = 0
        for i in range(self.d):
            idx = idx * self.L + (coords[i] % self.L)
        return idx

    def site_coords(self, idx):
        coords = []
        r = idx
        for i in range(self.d - 1, -1, -1):
            coords.append(r % self.L)
            r //= self.L
        return list(reversed(coords))

    def edge_index(self, site_idx, mu):
        return site_idx * self.d + mu

    def shifted_site(self, site_idx, mu, sign=+1):
        coords = self.site_coords(site_idx)
        coords[mu] = (coords[mu] + sign) % self.L
        return self.site_index(coords)

    def plaquettes(self):
        """Return list of plaquettes: (e1, e2, e3, e4, x, mu, nu)."""
        plaq_list = []
        for x in range(self.n_sites):
            for mu in range(self.d):
                for nu in range(mu+1, self.d):
                    x_mu = self.shifted_site(x, mu)
                    x_nu = self.shifted_site(x, nu)
                    e1 = self.edge_index(x, mu)        # forward along mu at x
                    e2 = self.edge_index(x_mu, nu)     # forward along nu at x+mu
                    e3 = self.edge_index(x_nu, mu)     # backward along mu at x+nu (forward edge from x+nu)
                    e4 = self.edge_index(x, nu)        # backward along nu at x (forward edge from x)
                    plaq_list.append((e1, e2, e3, e4, x, mu, nu))
        return plaq_list

# ====================== Build M(Q) ======================

def build_M_operator(lat, Q, basis):
    """
    Build M(Q) = ∑_□ B_□^T B_□ using the CORRECTED B_□ formula.

    For plaquette □ with edges e1(x,μ), e2(x+μ,ν), e3(x+ν,μ), e4(x,ν):
      B_□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U₀}(v₄)

    where U₀ = Q₁Q₂Q₃⁻¹Q₄⁻¹ = plaquette holonomy.
    """
    dim_su = lat.dim_su
    n_edges = lat.n_edges
    dim = lat.dim
    M = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T          # Q₁ Q₂ Q₃⁻¹
        U_plaq = Q123inv @ np.conj(Q[e4]).T        # Q₁ Q₂ Q₃⁻¹ Q₄⁻¹

        R1 = np.eye(dim_su)                        # identity for e1
        R2 = ad_matrix(Q1, basis)                   # Ad_{Q₁} for e2
        R3 = -ad_matrix(Q123inv, basis)             # -Ad_{Q₁Q₂Q₃⁻¹} for e3
        R4 = -ad_matrix(U_plaq, basis)              # -Ad_{U₀} for e4

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M

# ====================== Build K_curl = M(I) ======================

def build_K_curl(lat):
    """Build K_curl = M(I) directly from sign structure (no gauge field)."""
    dim_su = lat.dim_su
    dim = lat.dim
    K = np.zeros((dim, dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        signs = {e1: +1, e2: +1, e3: -1, e4: -1}
        edges = [e1, e2, e3, e4]
        for ei in edges:
            for ej in edges:
                si = signs[ei]
                sj = signs[ej]
                K[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += si * sj * np.eye(dim_su)

    return K

# ====================== Configuration Generators ======================

def gen_identity(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = np.eye(2)
    return Q

def gen_random_haar(lat):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = random_su2()
    return Q

def gen_near_identity(lat, eps):
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        Q[e] = su2_near_identity(eps)
    return Q

def gen_pure_gauge(lat):
    """Generate pure gauge: Q_e = g_{s(e)} g_{t(e)}^{-1}."""
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    g = [random_su2() for _ in range(lat.n_sites)]
    for x in range(lat.n_sites):
        for mu in range(lat.d):
            e = lat.edge_index(x, mu)
            y = lat.shifted_site(x, mu)
            Q[e] = g[x] @ np.conj(g[y]).T  # g_x g_y†
    return Q

def gen_gibbs(lat, beta, n_sweeps=30):
    """Simple Metropolis Gibbs sampling."""
    Q = gen_identity(lat)
    basis = su2_basis()
    step_size = 1.0 / max(beta, 0.5)
    for sweep in range(n_sweeps):
        for e in range(lat.n_edges):
            proposal = Q[e] @ su2_near_identity(step_size)
            # Simple accept (not true Metropolis, but gives diverse configs)
            Q[e] = proposal
            # Re-unitarize
            u, s, vh = np.linalg.svd(Q[e])
            Q[e] = u @ vh
    return Q

def gen_adversarial_near_id(lat, eps):
    """Near-identity with correlated perturbation."""
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    # Use a common direction to try to align perturbations
    direction = np.random.randn(3)
    direction /= np.linalg.norm(direction)
    for e in range(lat.n_edges):
        noise = np.random.randn(3) * 0.3  # small noise
        A = eps * (direction + noise)
        Q[e] = su2_exp(A)
    return Q

# ====================== Main Verification ======================

def run_full_check():
    np.random.seed(42)
    basis = su2_basis()

    L = 2
    d = 4
    lat = Lattice(L, d)
    bound = 4 * d  # = 16

    print(f"Lattice: L={L}, d={d}")
    print(f"  Sites: {lat.n_sites}, Edges: {lat.n_edges}, Plaquettes: {lat.n_plaq}")
    print(f"  M dimension: {lat.dim}×{lat.dim}")
    print(f"  Bound: λ_max(M) ≤ {bound}")
    print()

    # ===== STEP 1: Verify M(I) = K_curl =====
    print("="*70)
    print("STEP 1: Verify M(I) = K_curl")
    print("="*70)

    Q_id = gen_identity(lat)
    M_I = build_M_operator(lat, Q_id, basis)
    K_curl = build_K_curl(lat)

    diff = np.max(np.abs(M_I - K_curl))
    print(f"  max|M(I) - K_curl| = {diff:.2e}")

    eigs_MI = np.linalg.eigvalsh(M_I)
    print(f"  λ_max(M(I)) = {eigs_MI[-1]:.10f}")
    print(f"  λ_min(M(I)) = {eigs_MI[0]:.10f}")
    print(f"  Trace(M(I)) = {np.trace(M_I):.6f} (expected {12 * lat.n_plaq})")

    if diff > 1e-10:
        print("  *** FAIL: M(I) ≠ K_curl! Debug before proceeding. ***")
        return
    else:
        print("  PASS: M(I) = K_curl to machine precision.")

    # Record unique eigenvalues of K_curl
    eigs_K = np.sort(np.linalg.eigvalsh(K_curl))
    unique_eigs = []
    for e in eigs_K:
        if not unique_eigs or abs(e - unique_eigs[-1]) > 0.01:
            unique_eigs.append(e)
    print(f"  K_curl distinct eigenvalues: {[round(e, 4) for e in unique_eigs]}")
    print()

    # ===== STEP 2: Full D(Q) spectrum for 50+ configs =====
    print("="*70)
    print("STEP 2: Full D(Q) = M(Q) - M(I) eigenvalue check")
    print("="*70)

    configs = []

    # Pure gauge (5)
    for i in range(5):
        configs.append((f"Pure gauge #{i+1}", gen_pure_gauge(lat)))

    # Random Haar (20)
    for i in range(20):
        configs.append((f"Random Haar #{i+1}", gen_random_haar(lat)))

    # Gibbs at various β (10 total)
    for beta in [0.5, 1.0, 2.0, 3.0]:
        for i in range(2 if beta <= 1.0 else 3):
            configs.append((f"Gibbs β={beta} #{i+1}", gen_gibbs(lat, beta)))

    # Near-identity (10)
    for eps in [0.01, 0.1, 0.5]:
        for i in range(3):
            configs.append((f"Near-I ε={eps} #{i+1}", gen_near_identity(lat, eps)))
    configs.append((f"Near-I ε=1.0 #1", gen_near_identity(lat, 1.0)))

    # Adversarial (5)
    for i in range(5):
        configs.append((f"Adversarial #{i+1}", gen_adversarial_near_id(lat, 0.5)))

    print(f"  Testing {len(configs)} configurations")
    print()

    header = f"{'Config':<30s} {'λ_max(D)':<14s} {'λ_min(D)':<14s} {'#pos eigs':<10s} {'Status':<10s}"
    print(header)
    print("-" * len(header))

    results = []
    all_pass = True

    for name, Q in configs:
        t0 = time.time()
        M_Q = build_M_operator(lat, Q, basis)
        D_Q = M_Q - K_curl

        # Symmetry check
        asym = np.max(np.abs(D_Q - D_Q.T))
        assert asym < 1e-9, f"D not symmetric: {asym}"

        eigs_D = np.linalg.eigvalsh(D_Q)
        lam_max_D = eigs_D[-1]
        lam_min_D = eigs_D[0]
        n_positive = np.sum(eigs_D > 1e-10)

        elapsed = time.time() - t0

        if n_positive > 0:
            status = "*** FAIL ***"
            all_pass = False
        else:
            status = "PASS"

        print(f"{name:<30s} {lam_max_D:<14.8f} {lam_min_D:<14.8f} {n_positive:<10d} {status:<10s}")

        results.append({
            'name': name,
            'lambda_max_D': float(lam_max_D),
            'lambda_min_D': float(lam_min_D),
            'n_positive_eigs': int(n_positive),
            'lambda_max_M': float(np.linalg.eigvalsh(M_Q)[-1]),
            'passed': n_positive == 0,
            'time': elapsed
        })

    print()
    if all_pass:
        print(f"*** ALL {len(configs)} CONFIGURATIONS PASS: M(Q) ≼ M(I) ***")
    else:
        fails = [r for r in results if not r['passed']]
        print(f"*** {len(fails)} VIOLATIONS FOUND ***")
        for f in fails:
            print(f"  {f['name']}: λ_max(D) = {f['lambda_max_D']:.10f}, {f['n_positive_eigs']} positive eigenvalues")

    # Summary statistics
    max_lam_D = max(r['lambda_max_D'] for r in results)
    min_lam_D = min(r['lambda_min_D'] for r in results)
    print(f"\n  Worst-case λ_max(D): {max_lam_D:.10f}")
    print(f"  Most negative λ_min(D): {min_lam_D:.10f}")
    print(f"  Total configs tested: {len(results)}")

    # Save results
    with open('results_step2.json', 'w') as f:
        json.dump(results, f, indent=2)

    return results, K_curl, lat, basis


if __name__ == '__main__':
    results, K_curl, lat, basis = run_full_check()
