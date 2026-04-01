"""
Task 1: Numerical verification of max lambda[P^T R(Q) P] <= -W(Q)/12
for 200+ diverse SU(2) gauge configurations on L=2, d=4 lattice.

Tests:
- 50 random Haar
- 50 Gibbs samples (beta = 0.5, 1.0, 2.0, 4.0)
- 20 near-identity (eps = 0.01, 0.1, 0.5, 1.0, 2.0, pi)
- 20 pure gauge
- 20 abelian (diagonal)
- 40 adversarial (gradient ascent on max_eig / W)
"""

import numpy as np
import sys
import time


def expm_su2(A):
    """Matrix exponential for 2x2 anti-hermitian matrix (su(2) algebra).
    exp(A) where A = i*theta*(n.sigma)/2, using exact formula for SU(2).
    Also works for general small matrices via Pade approximation fallback.
    """
    # For 2x2: use Cayley-Hamilton
    # A^2 = (tr(A^2)/2) * I for traceless A
    # exp(A) = cos(theta)*I + (sin(theta)/theta)*A
    # where theta^2 = -det(A) = -tr(A^2)/2
    tr_A2 = np.trace(A @ A)
    theta_sq = -tr_A2 / 2.0

    if abs(theta_sq) < 1e-30:
        return np.eye(2, dtype=complex) + A + 0.5 * A @ A

    if theta_sq.real >= 0:
        theta = np.sqrt(theta_sq.real)
        return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * A
    else:
        # Imaginary theta (shouldn't happen for su(2) but be safe)
        theta = np.sqrt(-theta_sq.real)
        return np.cosh(theta) * np.eye(2, dtype=complex) + (np.sinh(theta) / theta) * A

np.random.seed(42)

# ============================================================
# Lattice and SU(2) infrastructure
# ============================================================

class Lattice:
    def __init__(self, L, d):
        self.L, self.d = L, d
        self.n_sites = L**d
        self.n_edges = d * self.n_sites
        self.n_plaq = d*(d-1)//2 * self.n_sites
        self.dim_su = 3
        self.dim = self.dim_su * self.n_edges
        self._plaq_cache = None

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
        if self._plaq_cache is not None:
            return self._plaq_cache
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
        self._plaq_cache = plaq_list
        return plaq_list


def su2_basis():
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]


def adjoint_action(U, A):
    return U @ A @ np.conj(U).T


def su2_to_vec(A, basis):
    return np.array([-2 * np.trace(b @ A).real for b in basis])


def ad_matrix(U, basis):
    dim_su = len(basis)
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R


def random_su2():
    """Generate random SU(2) matrix via Haar measure."""
    # Use quaternion parameterization
    x = np.random.randn(4)
    x /= np.linalg.norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ], dtype=complex)


def su2_from_algebra(vec):
    """exp(vec[0]*tau1 + vec[1]*tau2 + vec[2]*tau3)"""
    basis = su2_basis()
    A = sum(v * b for v, b in zip(vec, basis))
    return expm_su2(A)


# ============================================================
# Build M(Q) and K_curl
# ============================================================

def build_M_operator(lat, Q, basis):
    dim_su = lat.dim_su
    M = np.zeros((lat.dim, lat.dim))

    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        Q1 = Q[e1]
        Q12 = Q1 @ Q[e2]
        Q123inv = Q12 @ np.conj(Q[e3]).T
        U_plaq = Q123inv @ np.conj(Q[e4]).T

        R1 = np.eye(dim_su)
        R2 = ad_matrix(Q1, basis)
        R3 = -ad_matrix(Q123inv, basis)
        R4 = -ad_matrix(U_plaq, basis)

        edges_and_R = [(e1, R1), (e2, R2), (e3, R3), (e4, R4)]

        for (ei, Ri) in edges_and_R:
            for (ej, Rj) in edges_and_R:
                block = Ri.T @ Rj
                M[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += block

    return M


def build_K_curl(lat):
    dim_su = lat.dim_su
    K = np.zeros((lat.dim, lat.dim))
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        signs = {e1: +1, e2: +1, e3: -1, e4: -1}
        edges = [e1, e2, e3, e4]
        for ei in edges:
            for ej in edges:
                si, sj = signs[ei], signs[ej]
                K[dim_su*ei:dim_su*ei+dim_su, dim_su*ej:dim_su*ej+dim_su] += si * sj * np.eye(dim_su)
    return K


# ============================================================
# Wilson action
# ============================================================

def compute_wilson_action(lat, Q):
    """W(Q) = sum_plaq (1 - Re Tr(U_plaq) / N) where N=2 for SU(2)."""
    N = 2
    W = 0.0
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        U_plaq = Q[e1] @ Q[e2] @ np.conj(Q[e3]).T @ np.conj(Q[e4]).T
        W += 1.0 - np.trace(U_plaq).real / N
    return W


def compute_plaquette_holonomies(lat, Q):
    """Return list of plaquette holonomies U_plaq."""
    holonomies = []
    for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
        U_plaq = Q[e1] @ Q[e2] @ np.conj(Q[e3]).T @ np.conj(Q[e4]).T
        holonomies.append(U_plaq)
    return holonomies


# ============================================================
# Configuration generators
# ============================================================

def gen_identity(lat):
    return np.array([np.eye(2, dtype=complex) for _ in range(lat.n_edges)])


def gen_random_haar(lat):
    return np.array([random_su2() for _ in range(lat.n_edges)])


def gen_pure_gauge(lat):
    """Pure gauge: Q_e = g_x g_{x+mu}^{-1}"""
    g = [random_su2() for _ in range(lat.n_sites)]
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for x in range(lat.n_sites):
        for mu in range(lat.d):
            x_mu = lat.shifted_site(x, mu)
            e = lat.edge_index(x, mu)
            Q[e] = g[x] @ np.conj(g[x_mu]).T
    return Q


def gen_near_identity(lat, eps):
    """Q_e = exp(eps * random_su2_algebra)"""
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    basis = su2_basis()
    for e in range(lat.n_edges):
        vec = np.random.randn(3) * eps
        A = sum(v * b for v, b in zip(vec, basis))
        Q[e] = expm_su2(A)
    return Q


def gen_abelian(lat):
    """Abelian (diagonal) config: Q_e = diag(e^{i*theta}, e^{-i*theta})"""
    Q = np.zeros((lat.n_edges, 2, 2), dtype=complex)
    for e in range(lat.n_edges):
        theta = np.random.uniform(0, 2*np.pi)
        Q[e] = np.array([[np.exp(1j*theta), 0], [0, np.exp(-1j*theta)]])
    return Q


def gen_gibbs(lat, beta, n_sweeps=50):
    """Simple Metropolis-Hastings for Wilson action at inverse coupling beta.
    S = -(beta/N) sum_plaq Re Tr(U_plaq)
    """
    Q = gen_random_haar(lat)
    N_gauge = 2
    basis = su2_basis()

    for sweep in range(n_sweeps):
        for e in range(lat.n_edges):
            # Propose new link
            delta = np.random.randn(3) * 0.5
            A = sum(v * b for v, b in zip(delta, basis))
            Q_new = expm_su2(A) @ Q[e]

            # Compute action change (only plaquettes touching edge e)
            dS = 0.0
            for (e1, e2, e3, e4, x, mu, nu) in lat.plaquettes():
                if e in (e1, e2, e3, e4):
                    # Old plaquette
                    U_old = Q[e1] @ Q[e2] @ np.conj(Q[e3]).T @ np.conj(Q[e4]).T
                    # New plaquette
                    Q_temp = Q.copy()
                    Q_temp[e] = Q_new
                    U_new = Q_temp[e1] @ Q_temp[e2] @ np.conj(Q_temp[e3]).T @ np.conj(Q_temp[e4]).T
                    dS += -(beta/N_gauge) * (np.trace(U_new).real - np.trace(U_old).real)

            # Accept/reject
            if dS < 0 or np.random.rand() < np.exp(-dS):
                Q[e] = Q_new

    return Q


# ============================================================
# Core analysis function
# ============================================================

def analyze_config(lat, Q, K_curl, P, basis, label=""):
    """Compute max_eig, min_eig of P^T R(Q) P, Wilson action W(Q), and ratios."""
    M_Q = build_M_operator(lat, Q, basis)
    R_Q = M_Q - K_curl

    PRP = P.T @ R_Q @ P  # 9x9 matrix
    eigs_PRP = np.linalg.eigvalsh(PRP)

    max_eig = eigs_PRP[-1]
    min_eig = eigs_PRP[0]

    W_Q = compute_wilson_action(lat, Q)

    lam_max_MQ = np.linalg.eigvalsh(M_Q)[-1]

    # Ratios (handle W=0 case)
    if W_Q > 1e-12:
        ratio_max = max_eig / (-W_Q / 12.0)
        ratio_min = min_eig / (-W_Q / 3.0)
    else:
        ratio_max = 0.0 if abs(max_eig) < 1e-10 else float('inf')
        ratio_min = 0.0 if abs(min_eig) < 1e-10 else float('inf')

    return {
        'label': label,
        'max_eig': max_eig,
        'min_eig': min_eig,
        'W_Q': W_Q,
        'neg_W_over_12': -W_Q / 12.0,
        'neg_W_over_3': -W_Q / 3.0,
        'ratio_max': ratio_max,
        'ratio_min': ratio_min,
        'lam_max_MQ': lam_max_MQ,
        'all_eigs': eigs_PRP,
        'violation_max': max_eig > 1e-10,  # strict positivity = violation
        'violation_bound': max_eig > -W_Q/12.0 + 1e-10  # exceeds bound
    }


# ============================================================
# Main
# ============================================================

def main():
    t0 = time.time()

    L, d = 2, 4
    lat = Lattice(L, d)
    basis = su2_basis()

    print(f"Lattice: L={L}, d={d}")
    print(f"Sites: {lat.n_sites}, Edges: {lat.n_edges}, Plaquettes: {lat.n_plaq}")
    print(f"M dimension: {lat.dim}x{lat.dim}")
    print()

    # Build reference operator
    K_curl = build_K_curl(lat)
    eigs_K, vecs_K = np.linalg.eigh(K_curl)

    print(f"K_curl eigenvalues: {np.unique(np.round(eigs_K, 6))}")
    print(f"lambda_max(K_curl) = {eigs_K[-1]:.10f}")

    # Top eigenspace P (eigenvalue = 16, multiplicity = 9)
    top_mask = np.abs(eigs_K - 16.0) < 1e-8
    P = vecs_K[:, top_mask]
    print(f"Top eigenspace dimension: {P.shape[1]} (expected 9)")
    assert P.shape[1] == 9, f"Expected 9 top eigenvectors, got {P.shape[1]}"

    # Verify M(I) = K_curl
    Q_id = gen_identity(lat)
    M_I = build_M_operator(lat, Q_id, basis)
    diff_MK = np.max(np.abs(M_I - K_curl))
    print(f"|M(I) - K_curl| = {diff_MK:.2e}")
    print()

    results = []

    # ----- 1. Random Haar (50) -----
    print("=== Random Haar (50 configs) ===")
    for i in range(50):
        Q = gen_random_haar(lat)
        r = analyze_config(lat, Q, K_curl, P, basis, f"Haar-{i}")
        results.append(r)
        if (i+1) % 10 == 0:
            print(f"  {i+1}/50 done")

    # ----- 2. Gibbs samples (50: 12-13 each for beta=0.5, 1.0, 2.0, 4.0) -----
    print("=== Gibbs samples (50 configs) ===")
    betas = [0.5, 1.0, 2.0, 4.0]
    for beta in betas:
        n_per = 13 if beta == 0.5 else (13 if beta == 1.0 else (12 if beta == 2.0 else 12))
        for i in range(n_per):
            Q = gen_gibbs(lat, beta, n_sweeps=30)
            r = analyze_config(lat, Q, K_curl, P, basis, f"Gibbs-b{beta}-{i}")
            results.append(r)
        print(f"  beta={beta}: {n_per} configs done")

    # ----- 3. Near-identity (20: ~3-4 each for eps = 0.01, 0.1, 0.5, 1.0, 2.0, pi) -----
    print("=== Near-identity (20 configs) ===")
    epsilons = [0.01, 0.1, 0.5, 1.0, 2.0, np.pi]
    for eps in epsilons:
        n_per = 4 if eps in [0.01, 0.1, 0.5] else 3 if eps == 1.0 else 3
        for i in range(n_per):
            Q = gen_near_identity(lat, eps)
            r = analyze_config(lat, Q, K_curl, P, basis, f"NearI-eps{eps:.3f}-{i}")
            results.append(r)
        print(f"  eps={eps:.3f}: {n_per} configs done")

    # ----- 4. Pure gauge (20) -----
    print("=== Pure gauge (20 configs) ===")
    for i in range(20):
        Q = gen_pure_gauge(lat)
        r = analyze_config(lat, Q, K_curl, P, basis, f"PureGauge-{i}")
        results.append(r)
        if (i+1) % 10 == 0:
            print(f"  {i+1}/20 done")

    # ----- 5. Abelian (20) -----
    print("=== Abelian (20 configs) ===")
    for i in range(20):
        Q = gen_abelian(lat)
        r = analyze_config(lat, Q, K_curl, P, basis, f"Abelian-{i}")
        results.append(r)
        if (i+1) % 10 == 0:
            print(f"  {i+1}/20 done")

    # ----- 6. Adversarial: gradient ascent on ratio max_eig / (-W/12) (40) -----
    print("=== Adversarial (40 configs) ===")
    for i in range(40):
        # Start from random Haar
        Q = gen_random_haar(lat)
        best_ratio = -np.inf
        best_Q = Q.copy()

        for step in range(20):
            # Try random perturbation and keep if ratio increases
            e_perturb = np.random.randint(lat.n_edges)
            delta = np.random.randn(3) * 0.3
            A = sum(v * b for v, b in zip(delta, basis))
            Q_trial = Q.copy()
            Q_trial[e_perturb] = expm_su2(A) @ Q[e_perturb]

            M_trial = build_M_operator(lat, Q_trial, basis)
            R_trial = M_trial - K_curl
            PRP_trial = P.T @ R_trial @ P
            max_eig_trial = np.linalg.eigvalsh(PRP_trial)[-1]
            W_trial = compute_wilson_action(lat, Q_trial)

            if W_trial > 1e-10:
                ratio_trial = max_eig_trial / (-W_trial / 12.0)
            else:
                ratio_trial = 0.0

            if ratio_trial > best_ratio:
                best_ratio = ratio_trial
                best_Q = Q_trial.copy()
                Q = Q_trial

        r = analyze_config(lat, best_Q, K_curl, P, basis, f"Adversarial-{i}")
        results.append(r)
        if (i+1) % 10 == 0:
            print(f"  {i+1}/40 done")

    # ============================================================
    # Summary statistics
    # ============================================================
    print("\n" + "="*80)
    print("SUMMARY OF ALL RESULTS")
    print("="*80)

    total = len(results)
    n_violations_psd = sum(1 for r in results if r['violation_max'])
    n_violations_bound = sum(1 for r in results if r['violation_bound'])

    print(f"\nTotal configs tested: {total}")
    print(f"Violations of max_eig <= 0: {n_violations_psd} / {total}")
    print(f"Violations of max_eig <= -W/12: {n_violations_bound} / {total}")

    # Group by type
    groups = {}
    for r in results:
        prefix = r['label'].split('-')[0]
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(r)

    print(f"\n{'Group':<15} {'Count':>5} {'max_eig range':>25} {'W range':>25} {'ratio_max range':>25} {'viol':>5}")
    print("-"*105)
    for grp, rs in groups.items():
        max_eigs = [r['max_eig'] for r in rs]
        Ws = [r['W_Q'] for r in rs]
        ratios = [r['ratio_max'] for r in rs if abs(r['ratio_max']) < 1e10]
        viols = sum(1 for r in rs if r['violation_bound'])

        me_str = f"[{min(max_eigs):.6f}, {max(max_eigs):.6f}]"
        w_str = f"[{min(Ws):.6f}, {max(Ws):.6f}]"
        if ratios:
            r_str = f"[{min(ratios):.6f}, {max(ratios):.6f}]"
        else:
            r_str = "N/A (W=0)"

        print(f"{grp:<15} {len(rs):>5} {me_str:>25} {w_str:>25} {r_str:>25} {viols:>5}")

    # Detailed table for a subset
    print("\n\n=== DETAILED SAMPLE (first 5 of each group) ===")
    print(f"{'Label':<25} {'max_eig':>12} {'-W/12':>12} {'ratio':>10} {'min_eig':>12} {'-W/3':>12} {'ratio_min':>10} {'W':>10}")
    print("-"*115)
    for grp, rs in groups.items():
        for r in rs[:5]:
            print(f"{r['label']:<25} {r['max_eig']:>12.6f} {r['neg_W_over_12']:>12.6f} {r['ratio_max']:>10.6f} {r['min_eig']:>12.6f} {r['neg_W_over_3']:>12.6f} {r['ratio_min']:>10.6f} {r['W_Q']:>10.4f}")
        print()

    # Check for exact equality pattern
    print("\n=== EQUALITY CHECK: Is max_eig EXACTLY -W/12? ===")
    print("(Looking at ratio_max distribution)")
    nonzero_ratios = [r['ratio_max'] for r in results if r['W_Q'] > 1e-10 and abs(r['ratio_max']) < 1e10]
    if nonzero_ratios:
        print(f"  Mean ratio_max: {np.mean(nonzero_ratios):.8f}")
        print(f"  Std ratio_max:  {np.std(nonzero_ratios):.8f}")
        print(f"  Min ratio_max:  {min(nonzero_ratios):.8f}")
        print(f"  Max ratio_max:  {max(nonzero_ratios):.8f}")
        print(f"  Median ratio_max: {np.median(nonzero_ratios):.8f}")

    # Check min eigenvalue pattern
    print("\n=== MIN EIGENVALUE CHECK: Is min_eig = -W/3? ===")
    nonzero_ratios_min = [r['ratio_min'] for r in results if r['W_Q'] > 1e-10 and abs(r['ratio_min']) < 1e10]
    if nonzero_ratios_min:
        print(f"  Mean ratio_min: {np.mean(nonzero_ratios_min):.8f}")
        print(f"  Std ratio_min:  {np.std(nonzero_ratios_min):.8f}")
        print(f"  Min ratio_min:  {min(nonzero_ratios_min):.8f}")
        print(f"  Max ratio_min:  {max(nonzero_ratios_min):.8f}")
        print(f"  Median ratio_min: {np.median(nonzero_ratios_min):.8f}")

    # Eigenvalue structure of the 9x9 P^T R P
    print("\n=== EIGENVALUE STRUCTURE of P^T R(Q) P ===")
    print("(Number of distinct eigenvalues, multiplicities)")
    for grp, rs in groups.items():
        r = rs[0]
        eigs = r['all_eigs']
        rounded = np.round(eigs, 6)
        unique, counts = np.unique(rounded, return_counts=True)
        eig_str = ", ".join(f"{v:.4f} (x{c})" for v, c in zip(unique, counts))
        print(f"  {r['label']}: {eig_str}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")

    # Save detailed results for later analysis
    with open("results_detailed.txt", "w") as f:
        f.write(f"label,max_eig,min_eig,W_Q,neg_W_12,neg_W_3,ratio_max,ratio_min,lam_max_MQ\n")
        for r in results:
            f.write(f"{r['label']},{r['max_eig']:.10f},{r['min_eig']:.10f},{r['W_Q']:.10f},{r['neg_W_over_12']:.10f},{r['neg_W_over_3']:.10f},{r['ratio_max']:.10f},{r['ratio_min']:.10f},{r['lam_max_MQ']:.10f}\n")
    print("\nDetailed results saved to results_detailed.txt")


if __name__ == "__main__":
    main()
