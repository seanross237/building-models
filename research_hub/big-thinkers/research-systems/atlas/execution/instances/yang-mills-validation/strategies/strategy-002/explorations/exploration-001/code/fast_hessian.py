"""
Optimized Hessian computation for SU(2) lattice Yang-Mills.

Key optimizations:
1. Pre-compute plaquette neighborhoods per link
2. Only recompute affected plaquettes in FD evaluation
3. Skip zero off-diagonal blocks (links not sharing a plaquette)
4. Vectorized plaquette trace computation
"""

import numpy as np
from numpy.linalg import eigvalsh, norm, det, inv
from scipy.linalg import expm
import sys
import time

# ===================== SU(2) Basics =====================

sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)

T = np.array([1j * sigma[a] / 2 for a in range(3)])

I2 = np.eye(2, dtype=complex)

def su2_exp(v):
    """Efficient SU(2) exponential: exp(v_a T_a) using Rodrigues."""
    theta = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if theta < 1e-15:
        return I2.copy()
    X = sum(v[a] * T[a] for a in range(3))
    return np.cos(theta/2) * I2 + (np.sin(theta/2) / (theta/2)) * X

def haar_random_su2():
    x = np.random.randn(4)
    x = x / norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ], dtype=complex)

def project_su2(U):
    """Project to SU(2)."""
    d = det(U)
    U = U / np.sqrt(d)
    return U

def adjoint_matrix(Q):
    """3×3 matrix R_ab = -2 Re Tr(T_a Q T_b Q^{-1})."""
    Qinv = inv(Q)
    R = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            R[a, b] = -2 * np.trace(T[a] @ Q @ T[b] @ Qinv).real
    return R


# ===================== Lattice =====================

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

        # Build plaquette list
        self._plaquettes = self._build_plaquettes()
        self.n_plaq = len(self._plaquettes)

        # Build link → plaquette map
        self._link_to_plaq = [[] for _ in range(self.n_links)]
        for p_idx, plaq in enumerate(self._plaquettes):
            for e in plaq['edges']:
                self._link_to_plaq[e].append(p_idx)

        # Build link pair → shared plaquettes
        self._shared_plaq = {}
        for e in range(self.n_links):
            for p_idx in self._link_to_plaq[e]:
                for f in self._plaquettes[p_idx]['edges']:
                    if f != e:
                        key = (min(e, f), max(e, f))
                        if key not in self._shared_plaq:
                            self._shared_plaq[key] = set()
                        self._shared_plaq[key].add(p_idx)

        # Build neighbors: links that share at least one plaquette
        self._link_neighbors = [set() for _ in range(self.n_links)]
        for e in range(self.n_links):
            for p_idx in self._link_to_plaq[e]:
                for f in self._plaquettes[p_idx]['edges']:
                    if f != e:
                        self._link_neighbors[e].add(f)

    def site_index(self, coords):
        c = tuple(c % self.L for c in coords)
        return self._coord_to_idx[c]

    def neighbor(self, site, mu):
        c = list(self.coords[site])
        c[mu] = (c[mu] + 1) % self.L
        return self.site_index(c)

    def link_index(self, site, mu):
        return site * self.d + mu

    def _build_plaquettes(self):
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
                    })
        return plaq_list

    def plaquettes(self):
        return self._plaquettes


# ===================== Plaquette Traces =====================

def compute_plaq_traces(Q, lattice):
    """Compute Re Tr(U_□) for all plaquettes."""
    traces = np.zeros(lattice.n_plaq)
    for p_idx, plaq in enumerate(lattice.plaquettes()):
        e1, e2, e3, e4 = plaq['edges']
        U = Q[e1] @ Q[e2] @ inv(Q[e3]) @ inv(Q[e4])
        traces[p_idx] = np.trace(U).real
    return traces

def compute_single_plaq_trace(Q, plaq):
    """Compute Re Tr(U_□) for one plaquette."""
    e1, e2, e3, e4 = plaq['edges']
    U = Q[e1] @ Q[e2] @ inv(Q[e3]) @ inv(Q[e4])
    return np.trace(U).real


# ===================== Wilson Action =====================

def wilson_action_from_traces(traces, beta):
    return -(beta / 2) * np.sum(traces)

def wilson_action(Q, lattice, beta):
    traces = compute_plaq_traces(Q, lattice)
    return wilson_action_from_traces(traces, beta)


# ===================== Fast FD Hessian =====================

def compute_hessian_fd(Q, lattice, beta, h=1e-4):
    """
    Compute Hessian using central finite differences with locality optimization.
    Only compute entries for link pairs sharing a plaquette.
    """
    n = lattice.n_dof
    H = np.zeros((n, n))

    # Base plaquette traces
    base_traces = compute_plaq_traces(Q, lattice)
    S0 = wilson_action_from_traces(base_traces, beta)

    def perturbed_action(link_idx, color_idx, eps, base_traces):
        """Compute action with one link perturbed, only recomputing affected plaquettes."""
        v = np.zeros(3)
        v[color_idx] = eps
        Q_new_link = su2_exp(v) @ Q[link_idx]

        # Only recompute affected plaquettes
        new_traces = base_traces.copy()
        for p_idx in lattice._link_to_plaq[link_idx]:
            plaq = lattice.plaquettes()[p_idx]
            e1, e2, e3, e4 = plaq['edges']
            # Replace the link with the perturbed version
            Qs = [None] * 4
            edges = [e1, e2, e3, e4]
            for k, e in enumerate(edges):
                if e == link_idx:
                    Qs[k] = Q_new_link
                else:
                    Qs[k] = Q[e]
            U = Qs[0] @ Qs[1] @ inv(Qs[2]) @ inv(Qs[3])
            new_traces[p_idx] = np.trace(U).real
        return wilson_action_from_traces(new_traces, beta)

    def double_perturbed_action(link_i, color_i, eps_i, link_j, color_j, eps_j, base_traces):
        """Compute action with two links perturbed."""
        v_i = np.zeros(3)
        v_i[color_i] = eps_i
        Q_new_i = su2_exp(v_i) @ Q[link_i]

        v_j = np.zeros(3)
        v_j[color_j] = eps_j
        Q_new_j = su2_exp(v_j) @ Q[link_j]

        # Affected plaquettes: union of both links' plaquettes
        affected = set(lattice._link_to_plaq[link_i]) | set(lattice._link_to_plaq[link_j])
        new_traces = base_traces.copy()
        for p_idx in affected:
            plaq = lattice.plaquettes()[p_idx]
            edges = plaq['edges']
            Qs = []
            for e in edges:
                if e == link_i:
                    Qs.append(Q_new_i)
                elif e == link_j:
                    Qs.append(Q_new_j)
                else:
                    Qs.append(Q[e])
            U = Qs[0] @ Qs[1] @ inv(Qs[2]) @ inv(Qs[3])
            new_traces[p_idx] = np.trace(U).real
        return wilson_action_from_traces(new_traces, beta)

    # Pre-compute single perturbations for diagonal elements
    S_plus = np.zeros(n)
    S_minus = np.zeros(n)

    for i in range(n):
        e_i = i // 3
        a_i = i % 3
        S_plus[i] = perturbed_action(e_i, a_i, h, base_traces)
        S_minus[i] = perturbed_action(e_i, a_i, -h, base_traces)

    # Diagonal elements
    for i in range(n):
        H[i, i] = (S_plus[i] - 2*S0 + S_minus[i]) / h**2

    # Off-diagonal: only for link pairs that share a plaquette
    for e_i in range(lattice.n_links):
        for e_j in lattice._link_neighbors[e_i]:
            if e_j <= e_i:
                continue  # Only upper triangle
            for a_i in range(3):
                i = e_i * 3 + a_i
                for a_j in range(3):
                    j = e_j * 3 + a_j
                    S_pp = double_perturbed_action(e_i, a_i, h, e_j, a_j, h, base_traces)
                    S_pm = double_perturbed_action(e_i, a_i, h, e_j, a_j, -h, base_traces)
                    S_mp = double_perturbed_action(e_i, a_i, -h, e_j, a_j, h, base_traces)
                    S_mm = double_perturbed_action(e_i, a_i, -h, e_j, a_j, -h, base_traces)
                    H[i, j] = (S_pp - S_pm - S_mp + S_mm) / (4 * h**2)
                    H[j, i] = H[i, j]

        # Same-link off-diagonal (different color directions on the same link)
        for a_i in range(3):
            i = e_i * 3 + a_i
            for a_j in range(a_i+1, 3):
                j = e_i * 3 + a_j
                S_pp = double_perturbed_action(e_i, a_i, h, e_i, a_j, h, base_traces)
                S_pm = double_perturbed_action(e_i, a_i, h, e_i, a_j, -h, base_traces)
                S_mp = double_perturbed_action(e_i, a_i, -h, e_i, a_j, h, base_traces)
                S_mm = double_perturbed_action(e_i, a_i, -h, e_i, a_j, -h, base_traces)
                H[i, j] = (S_pp - S_pm - S_mp + S_mm) / (4 * h**2)
                H[j, i] = H[i, j]

    return H


# ===================== B² Formula Hessian =====================

def compute_hessian_formula(Q, lattice, beta):
    """H_formula = (β/(2N)) Σ_□ B□ᵀ B□, using LEFT B□ with adjoint representation."""
    N = 2
    n = lattice.n_dof
    M = np.zeros((n, n))

    for plaq in lattice.plaquettes():
        e1, e2, e3, e4 = plaq['edges']

        P2 = Q[e1].copy()
        P3 = Q[e1] @ Q[e2] @ inv(Q[e3])
        P4 = Q[e1] @ Q[e2] @ inv(Q[e3]) @ inv(Q[e4])

        R2 = adjoint_matrix(P2)
        R3 = adjoint_matrix(P3)
        R4 = adjoint_matrix(P4)

        B_mat = np.zeros((3, n))

        # e₁: +I
        B_mat[:, e1*3:e1*3+3] += np.eye(3)
        # e₂: +R₂
        B_mat[:, e2*3:e2*3+3] += R2
        # e₃: -R₃
        B_mat[:, e3*3:e3*3+3] -= R3
        # e₄: -R₄
        B_mat[:, e4*3:e4*3+3] -= R4

        M += B_mat.T @ B_mat

    return (beta / (2 * N)) * M


# ===================== Main Analysis =====================

def compute_ratio_data(Q, lattice, beta, h=1e-4):
    """Compute r(Q) and associated data."""
    H_actual = compute_hessian_fd(Q, lattice, beta, h)
    H_formula = compute_hessian_formula(Q, lattice, beta)

    H_actual = (H_actual + H_actual.T) / 2
    H_formula = (H_formula + H_formula.T) / 2

    eigs_actual = eigvalsh(H_actual)
    eigs_formula = eigvalsh(H_formula)

    lmax_actual = eigs_actual[-1]
    lmax_formula = eigs_formula[-1]

    r = lmax_actual / lmax_formula if lmax_formula > 1e-15 else float('inf')

    C = H_formula - H_actual
    eigs_C = eigvalsh(C)

    # Top eigenvector of H_actual
    from numpy.linalg import eigh
    _, vecs_actual = eigh(H_actual)
    v_max = vecs_actual[:, -1]

    # H_actual(v_max, v_max) and H_formula(v_max, v_max)
    ha_vmax = v_max @ H_actual @ v_max
    hf_vmax = v_max @ H_formula @ v_max
    r_vmax = ha_vmax / hf_vmax if abs(hf_vmax) > 1e-15 else float('inf')

    return {
        'r': r,
        'lmax_actual': lmax_actual,
        'lmax_formula': lmax_formula,
        'C_norm': np.max(np.abs(eigs_C)),  # operator norm = max |eigenvalue|
        'C_min_eig': eigs_C[0],
        'C_max_eig': eigs_C[-1],
        'C_n_positive': np.sum(eigs_C > 1e-10),
        'C_n_negative': np.sum(eigs_C < -1e-10),
        'r_vmax': r_vmax,
        'H_actual': H_actual,
        'H_formula': H_formula,
        'eigs_actual': eigs_actual,
        'eigs_formula': eigs_formula,
        'eigs_C': eigs_C,
    }


def random_su2_config(n_links):
    return np.array([haar_random_su2() for _ in range(n_links)])


def near_identity_config(n_links, scale=0.1):
    """Generate near-identity configuration: Q_e = exp(scale * random * T_a)."""
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for e in range(n_links):
        v = scale * np.random.randn(3)
        Q[e] = su2_exp(v)
    return Q


def near_abelian_config(n_links):
    """Generate near-abelian config: Q_e = exp(θ_e T_3) (all rotations around same axis)."""
    Q = np.zeros((n_links, 2, 2), dtype=complex)
    for e in range(n_links):
        theta = np.random.uniform(0, 2*np.pi)
        v = np.array([0, 0, theta])
        Q[e] = su2_exp(v)
    return Q


# ===================== Stage 1 =====================

def stage1(lattice, beta):
    print("=" * 60)
    print("STAGE 1: Identity Configuration Check")
    print(f"L={lattice.L}, d={lattice.d}, β={beta}")
    print(f"Links={lattice.n_links}, DOF={lattice.n_dof}, Plaquettes={lattice.n_plaq}")
    print("=" * 60)

    Q = np.array([I2.copy() for _ in range(lattice.n_links)])

    S0 = wilson_action(Q, lattice, beta)
    S_expected = -(beta/2) * lattice.n_plaq * 2
    print(f"S(I) = {S0:.6f}, expected = {S_expected:.6f}")

    t0 = time.time()
    H_actual = compute_hessian_fd(Q, lattice, beta)
    t_fd = time.time() - t0
    print(f"H_actual computed in {t_fd:.1f}s")

    t0 = time.time()
    H_formula = compute_hessian_formula(Q, lattice, beta)
    t_bf = time.time() - t0
    print(f"H_formula computed in {t_bf:.1f}s")

    H_actual = (H_actual + H_actual.T) / 2
    H_formula = (H_formula + H_formula.T) / 2

    diff = norm(H_actual - H_formula)
    rel_diff = diff / max(norm(H_actual), 1e-15)
    print(f"\n||H_actual - H_formula|| = {diff:.2e}")
    print(f"Relative difference = {rel_diff:.2e}")

    eigs_actual = eigvalsh(H_actual)
    eigs_formula = eigvalsh(H_formula)

    lmax_a = eigs_actual[-1]
    lmax_f = eigs_formula[-1]

    print(f"\nλ_max(H_actual) = {lmax_a:.8f}")
    print(f"λ_max(H_formula) = {lmax_f:.8f}")

    r = lmax_a / lmax_f
    print(f"r = {r:.10f}")

    # Unique eigenvalues
    unique_a = np.unique(np.round(eigs_actual, 4))
    unique_f = np.unique(np.round(eigs_formula, 4))
    print(f"\nUnique eigenvalues (H_actual, rounded to 4dp): {unique_a}")
    print(f"Unique eigenvalues (H_formula, rounded to 4dp): {unique_f}")

    passed = rel_diff < 0.01 and abs(r - 1.0) < 0.01
    print(f"\nStage 1 {'PASSED' if passed else 'FAILED'}")

    return passed, {
        'lmax_actual': lmax_a,
        'lmax_formula': lmax_f,
        'r': r,
        'diff': diff,
        'rel_diff': rel_diff,
        'eigs_actual': eigs_actual,
        'eigs_formula': eigs_formula,
        't_fd': t_fd,
        't_bf': t_bf,
    }


# ===================== Stage 2 =====================

def stage2(lattice, beta, n_configs=50):
    print("\n" + "=" * 60)
    print(f"STAGE 2: Random Configurations ({n_configs} configs)")
    print("=" * 60)

    results = []
    worst_r = -1
    worst_Q = None

    for i in range(n_configs):
        Q = random_su2_config(lattice.n_links)
        t0 = time.time()
        res = compute_ratio_data(Q, lattice, beta)
        dt = time.time() - t0

        results.append(res)
        if res['r'] > worst_r:
            worst_r = res['r']
            worst_Q = Q.copy()

        status = "*** VIOLATION ***" if res['r'] > 1.0 else ""
        print(f"  [{i+1:3d}/{n_configs}] r={res['r']:.8f}  λ_a={res['lmax_actual']:.4f}  "
              f"λ_f={res['lmax_formula']:.4f}  ||C||={res['C_norm']:.4f}  "
              f"r_vmax={res['r_vmax']:.6f}  ({dt:.1f}s) {status}")

        if res['r'] > 1.0:
            print(f"\n*** INEQUALITY VIOLATED: r = {res['r']:.10f} ***")
            break

    rs = np.array([r['r'] for r in results])
    print(f"\nStatistics over {len(results)} configs:")
    print(f"  mean(r)  = {np.mean(rs):.8f}")
    print(f"  max(r)   = {np.max(rs):.8f}")
    print(f"  min(r)   = {np.min(rs):.8f}")
    print(f"  std(r)   = {np.std(rs):.8f}")
    print(f"  gap      = {1 - np.max(rs):.8f}")

    # Also report r_vmax stats
    rvs = np.array([r['r_vmax'] for r in results])
    print(f"  mean(r_vmax) = {np.mean(rvs):.8f}")
    print(f"  max(r_vmax)  = {np.max(rvs):.8f}")

    return results, worst_Q


# ===================== Stage 3: Gradient Ascent =====================

def gradient_ascent_r(lattice, beta, n_starts=20, n_steps=200, eta=0.01, delta=1e-3, h_fd=1e-4):
    """Maximize r(Q) = λ_max(H_actual) / λ_max(H_formula) via gradient ascent on Q."""
    print("\n" + "=" * 60)
    print(f"STAGE 3: Adversarial Gradient Ascent ({n_starts} starts, {n_steps} steps)")
    print("=" * 60)

    best_r_global = -1
    best_Q_global = None

    for start in range(n_starts):
        Q = random_su2_config(lattice.n_links)
        res = compute_ratio_data(Q, lattice, beta, h_fd)
        r_current = res['r']
        print(f"\n  Start {start+1}: initial r = {r_current:.8f}")

        best_r_run = r_current
        stall_count = 0

        for step in range(n_steps):
            # Compute gradient of r w.r.t. each link/color
            grad = np.zeros((lattice.n_links, 3))

            for e in range(lattice.n_links):
                for a in range(3):
                    v = np.zeros(3)
                    v[a] = delta
                    Q_pert = Q.copy()
                    Q_pert[e] = su2_exp(v) @ Q[e]

                    res_pert = compute_ratio_data(Q_pert, lattice, beta, h_fd)
                    grad[e, a] = (res_pert['r'] - r_current) / delta

            # Gradient step
            grad_norm = norm(grad)
            if grad_norm < 1e-10:
                print(f"    Step {step}: gradient vanished, stopping")
                break

            # Adaptive step size
            effective_eta = eta
            for e in range(lattice.n_links):
                v = effective_eta * grad[e]
                Q[e] = su2_exp(v) @ Q[e]
                # Project back to SU(2)
                Q[e] = project_su2(Q[e])

            res = compute_ratio_data(Q, lattice, beta, h_fd)
            r_new = res['r']

            if r_new > best_r_run:
                best_r_run = r_new
                stall_count = 0
            else:
                stall_count += 1

            if step % 20 == 0 or r_new > 1.0:
                print(f"    Step {step}: r = {r_new:.8f}, |∇r| = {grad_norm:.6f}")

            r_current = r_new

            if r_new > 1.0:
                print(f"    *** VIOLATION at step {step}: r = {r_new:.10f} ***")
                break

            if stall_count > 30:
                print(f"    Stalled at step {step}, r = {r_current:.8f}")
                break

        print(f"  Start {start+1} best r = {best_r_run:.8f}")

        if best_r_run > best_r_global:
            best_r_global = best_r_run
            best_Q_global = Q.copy()

    print(f"\nGlobal best r = {best_r_global:.10f}")
    print(f"Gap = {1 - best_r_global:.10f}")

    return best_r_global, best_Q_global


# ===================== Main =====================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, default=1)
    parser.add_argument('--L', type=int, default=2)
    parser.add_argument('--d', type=int, default=4)
    parser.add_argument('--beta', type=float, default=1.0)
    parser.add_argument('--n_configs', type=int, default=50)
    parser.add_argument('--n_starts', type=int, default=20)
    parser.add_argument('--n_steps', type=int, default=200)
    args = parser.parse_args()

    lat = Lattice(args.L, args.d)
    print(f"Lattice: L={args.L}, d={args.d}")
    print(f"Sites={lat.n_sites}, Links={lat.n_links}, DOF={lat.n_dof}, Plaquettes={lat.n_plaq}")

    if args.stage == 1:
        passed, info = stage1(lat, args.beta)
    elif args.stage == 2:
        results, worst_Q = stage2(lat, args.beta, args.n_configs)
    elif args.stage == 3:
        best_r, best_Q = gradient_ascent_r(lat, args.beta, args.n_starts, args.n_steps)
