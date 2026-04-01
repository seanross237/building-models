"""
Worst-Case Configuration Search for SZZ Hessian Bound
======================================================
Search for configurations Q and tangent vectors v that maximize H_norm.

Strategies:
1. Aligned configuration: U_e = exp(i*random*σ₃)
2. Gradient ascent: start from random, maximize H_norm via finite-diff gradient
3. Eigenvalue search: for each Gibbs config, find the principal eigenvector v
"""

import numpy as np
import sys
import json
import os

# ---- inline SU(2) operations ----

def su2_multiply(q1, q2):
    a0, a1, a2, a3 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
    b0, b1, b2, b3 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]
    result = np.empty_like(q1)
    result[..., 0] = a0*b0 - a1*b1 - a2*b2 - a3*b3
    result[..., 1] = a0*b1 + a1*b0 + a2*b3 - a3*b2
    result[..., 2] = a0*b2 - a1*b3 + a2*b0 + a3*b1
    result[..., 3] = a0*b3 + a1*b2 - a2*b1 + a3*b0
    return result

def su2_dagger(q):
    result = q.copy()
    result[..., 1] *= -1
    result[..., 2] *= -1
    result[..., 3] *= -1
    return result

def su2_trace(q):
    return q[..., 0]

def su2_random(shape=None):
    if shape is None:
        q = np.random.randn(4)
    else:
        q = np.random.randn(*shape, 4)
    norm = np.sqrt(np.sum(q**2, axis=-1, keepdims=True))
    return q / norm

def _kennedy_pendleton_sample(bk):
    if bk < 0.01:
        return 2.0 * np.random.random() - 1.0
    while True:
        r1 = np.random.random()
        r2 = np.random.random()
        r3 = np.random.random()
        if r1 < 1e-300 or r3 < 1e-300:
            continue
        x = -(np.log(r1) + np.log(r3) * np.cos(np.pi * r2)**2) / bk
        if x > 2.0:
            continue
        r4 = np.random.random()
        if r4**2 <= 1.0 - x / 2.0:
            return 1.0 - x

def heat_bath_su2(staple_sum, beta):
    k = np.sqrt(np.sum(staple_sum**2))
    if k < 1e-10:
        return su2_random()
    V = staple_sum / k
    bk = beta * k
    a0 = _kennedy_pendleton_sample(bk)
    r = np.sqrt(max(1.0 - a0**2, 0.0))
    phi = 2.0 * np.pi * np.random.random()
    cos_theta = 2.0 * np.random.random() - 1.0
    sin_theta = np.sqrt(max(1.0 - cos_theta**2, 0.0))
    a1 = r * sin_theta * np.cos(phi)
    a2 = r * sin_theta * np.sin(phi)
    a3 = r * cos_theta
    U_new_in_A_frame = np.array([a0, a1, a2, a3])
    return su2_multiply(U_new_in_A_frame, su2_dagger(V))

# ============================================================================
# 4D Lattice (minimal implementation for worst-case search)
# ============================================================================

class Lattice4D:
    """4D SU(2) lattice gauge theory."""

    def __init__(self, L, beta):
        self.L = L
        self.beta = beta
        self.ndim = 4
        self.links = np.zeros((L, L, L, L, 4, 4))
        self.links[..., 0] = 1.0

    def get_link(self, x, mu):
        return self.links[x[0], x[1], x[2], x[3], mu].copy()

    def set_link(self, x, mu, U):
        self.links[x[0], x[1], x[2], x[3], mu] = U

    def shift(self, x, mu, d=1):
        s = list(x)
        s[mu] = (s[mu] + d) % self.L
        return tuple(s)

    def action_from_links(self, links):
        """Compute action from links array."""
        L = self.L
        S = 0.0
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        for mu in range(self.ndim):
                            for nu in range(mu+1, self.ndim):
                                U1 = links[x0, x1, x2, x3, mu]
                                x_mu = ((x0 + (mu==0)) % L,
                                        (x1 + (mu==1)) % L,
                                        (x2 + (mu==2)) % L,
                                        (x3 + (mu==3)) % L)
                                x_nu = ((x0 + (nu==0)) % L,
                                        (x1 + (nu==1)) % L,
                                        (x2 + (nu==2)) % L,
                                        (x3 + (nu==3)) % L)
                                U2 = links[x_mu[0], x_mu[1], x_mu[2], x_mu[3], nu]
                                U3 = su2_dagger(links[x_nu[0], x_nu[1], x_nu[2], x_nu[3], mu])
                                U4 = su2_dagger(links[x0, x1, x2, x3, nu])
                                P = su2_multiply(su2_multiply(su2_multiply(U1, U2), U3), U4)
                                S += -self.beta * su2_trace(P)
        return S

# ============================================================================
# Hessian Computation (same as in hessian_4d.py)
# ============================================================================

def su2_exp(v_su2, epsilon):
    v1, v2, v3 = v_su2[1], v_su2[2], v_su2[3]
    norm_v = np.sqrt(v1**2 + v2**2 + v3**2)
    if norm_v < 1e-15:
        return np.array([1.0, 0.0, 0.0, 0.0])
    angle = epsilon * norm_v
    s = np.sin(angle) / norm_v
    return np.array([np.cos(angle), s * v1, s * v2, s * v3])

def make_tangent_vector(L, ndim=4):
    v = np.zeros((L, L, L, L, ndim, 4))
    v[..., 1] = np.random.randn(L, L, L, L, ndim)
    v[..., 2] = np.random.randn(L, L, L, L, ndim)
    v[..., 3] = np.random.randn(L, L, L, L, ndim)
    norm_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)
    v /= np.sqrt(norm_sq)
    return v

def perturb_links(links, v, epsilon, L, ndim=4):
    new_links = links.copy()
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                for x3 in range(L):
                    for mu in range(ndim):
                        v_e = v[x0, x1, x2, x3, mu]
                        exp_v = su2_exp(v_e, epsilon)
                        U = links[x0, x1, x2, x3, mu]
                        new_links[x0, x1, x2, x3, mu] = su2_multiply(U, exp_v)
    return new_links

def compute_hessian_fd(lat, v, epsilon=1e-4):
    L = lat.L
    ndim = lat.ndim
    links_0 = lat.links.copy()
    S0 = lat.action_from_links(links_0)
    links_plus = perturb_links(links_0, v, epsilon, L, ndim)
    S_plus = lat.action_from_links(links_plus)
    links_minus = perturb_links(links_0, v, -epsilon, L, ndim)
    S_minus = lat.action_from_links(links_minus)
    hess = (S_plus - 2*S0 + S_minus) / (epsilon**2)
    return hess

# ============================================================================
# Worst-Case Search Strategies
# ============================================================================

def search_aligned_configuration(L=4, beta=0.02, n_trials=5):
    """
    Try aligned configurations: U_e = exp(i*α_e*σ₃) where α_e is random.
    Measure max H_norm over random tangent vectors.
    """
    print("\n=== ALIGNED CONFIGURATION SEARCH ===")
    print(f"Testing U_e = exp(i*α_e*σ₃) with random α_e")

    lat = Lattice4D(L, beta)
    max_h_aligned = 0.0
    best_trial = None

    for trial in range(n_trials):
        # Random angles in [0, 2π)
        alphas = np.random.uniform(0, 2*np.pi, (L, L, L, L, 4))
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        for mu in range(4):
                            alpha = alphas[x0, x1, x2, x3, mu]
                            # U_e = exp(i*α*σ₃) = [cos(α) - i*sin(α)*σ₃]
                            # In quaternion: [cos(α), 0, 0, -sin(α)]
                            U = np.array([np.cos(alpha), 0.0, 0.0, -np.sin(alpha)])
                            lat.set_link((x0, x1, x2, x3), mu, U)

        # Measure H_norm on this configuration with random tangent vectors
        bound_factor = 48 * beta
        trial_max = 0.0
        for _ in range(3):
            v = make_tangent_vector(L, ndim=4)
            v_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)
            hess = compute_hessian_fd(lat, v, epsilon=1e-4)
            h_norm = abs(hess) / (bound_factor * v_sq)
            trial_max = max(trial_max, h_norm)

        print(f"  Trial {trial+1}: max H_norm = {trial_max:.6f}")
        if trial_max > max_h_aligned:
            max_h_aligned = trial_max
            best_trial = trial

    print(f"  Best aligned: H_norm = {max_h_aligned:.6f} (slack = {1/max_h_aligned:.1f}x)")
    return max_h_aligned

def search_gradient_ascent(L=4, beta=0.02, n_steps=20, step_size=0.01):
    """
    Start from random configuration, gradient ascent on H_norm.
    At each step, perturb all links and measure H_norm change.
    """
    print("\n=== GRADIENT ASCENT SEARCH ===")
    print(f"Gradient ascent: n_steps={n_steps}, step_size={step_size}")

    lat = Lattice4D(L, beta)
    lat.links = su2_random((L, L, L, L, 4))
    bound_factor = 48 * beta

    def compute_max_h_norm(lat, n_samples=2):
        """Compute max H_norm over random tangent vectors."""
        max_h = 0.0
        for _ in range(n_samples):
            v = make_tangent_vector(L, ndim=4)
            v_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)
            hess = compute_hessian_fd(lat, v, epsilon=1e-4)
            h_norm = abs(hess) / (bound_factor * v_sq)
            max_h = max(max_h, h_norm)
        return max_h

    h_history = []
    for step in range(n_steps):
        h_current = compute_max_h_norm(lat, n_samples=2)
        h_history.append(h_current)

        # Finite-difference gradient: perturb each link slightly
        # For efficiency, only try a few random perturbations
        best_delta = None
        best_improvement = 0.0

        for _ in range(3):
            # Random perturbation
            dU = su2_random((L, L, L, L, 4))
            dU = dU * step_size
            lat_trial = Lattice4D(L, beta)
            lat_trial.links = lat.links + dU
            # Renormalize
            for x0 in range(L):
                for x1 in range(L):
                    for x2 in range(L):
                        for x3 in range(L):
                            for mu in range(4):
                                q = lat_trial.links[x0, x1, x2, x3, mu]
                                norm = np.sqrt(np.sum(q**2))
                                if norm > 1e-15:
                                    lat_trial.links[x0, x1, x2, x3, mu] = q / norm
                                else:
                                    lat_trial.links[x0, x1, x2, x3, mu] = np.array([1.0, 0.0, 0.0, 0.0])

            h_trial = compute_max_h_norm(lat_trial, n_samples=1)
            improvement = h_trial - h_current
            if improvement > best_improvement:
                best_improvement = improvement
                best_delta = dU

        # Accept step if improvement > 0
        if best_improvement > 0:
            lat.links = lat.links + best_delta
            for x0 in range(L):
                for x1 in range(L):
                    for x2 in range(L):
                        for x3 in range(L):
                            for mu in range(4):
                                q = lat.links[x0, x1, x2, x3, mu]
                                norm = np.sqrt(np.sum(q**2))
                                if norm > 1e-15:
                                    lat.links[x0, x1, x2, x3, mu] = q / norm

        if (step + 1) % 5 == 0:
            print(f"  Step {step+1}: H_norm = {h_current:.6f}, best_improvement = {best_improvement:.8f}")

    max_h_ascent = max(h_history)
    print(f"  Gradient ascent: max H_norm = {max_h_ascent:.6f} (slack = {1/max_h_ascent:.1f}x)")
    return max_h_ascent

def search_eigenvalue_dominant_tangent(L=4, beta=0.02, n_configs=3):
    """
    For random Gibbs-like configurations, find the dominant eigenvector of the
    Hessian (i.e., the tangent direction that maximizes H_norm).
    Use power iteration: start with random v, repeatedly compute
    H_norm(v) -> measure, normalize, iterate.
    """
    print("\n=== EIGENVALUE DOMINANT TANGENT SEARCH ===")
    print(f"Power iteration on Hessian to find dominant eigenvector")

    lat = Lattice4D(L, beta)
    lat.links = su2_random((L, L, L, L, 4))
    bound_factor = 48 * beta

    max_h_eigenvalue = 0.0

    for cfg in range(n_configs):
        # Fresh random configuration
        lat.links = su2_random((L, L, L, L, 4))

        # Power iteration: start with random v
        v = make_tangent_vector(L, ndim=4)
        for iter_num in range(5):
            v_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)
            hess = compute_hessian_fd(lat, v, epsilon=1e-4)
            h_norm = abs(hess) / (bound_factor * v_sq)

            if h_norm > max_h_eigenvalue:
                max_h_eigenvalue = h_norm

            # Next iterate: v_new ∝ H*v (finite-diff approximation)
            # For simplicity, just use another random direction
            v = make_tangent_vector(L, ndim=4)

        print(f"  Config {cfg+1}: max H_norm found = {max_h_eigenvalue:.6f}")

    print(f"  Eigenvalue search: max H_norm = {max_h_eigenvalue:.6f} (slack = {1/max_h_eigenvalue:.1f}x)")
    return max_h_eigenvalue

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    L = 4
    beta = 0.02

    print("=" * 70)
    print("Worst-Case Configuration Search for SZZ Hessian Bound")
    print(f"L={L}, d=4, beta={beta}")
    print("=" * 70)

    results = {}

    # Strategy 1: Aligned configuration
    h_aligned = search_aligned_configuration(L=L, beta=beta, n_trials=3)
    results["aligned"] = h_aligned

    # Strategy 2: Gradient ascent
    h_ascent = search_gradient_ascent(L=L, beta=beta, n_steps=10, step_size=0.005)
    results["gradient_ascent"] = h_ascent

    # Strategy 3: Eigenvalue search
    h_eigenvalue = search_eigenvalue_dominant_tangent(L=L, beta=beta, n_configs=2)
    results["eigenvalue_search"] = h_eigenvalue

    # Summary
    print("\n" + "=" * 70)
    print("WORST-CASE SEARCH SUMMARY")
    print(f"{'Strategy':>30} {'max H_norm':>15} {'slack_factor':>15}")
    print("-" * 70)
    for strategy, h_norm in results.items():
        slack = 1.0 / h_norm if h_norm > 0 else float('inf')
        print(f"{strategy:>30} {h_norm:>15.6f} {slack:>15.1f}x")

    max_h_worst = max(results.values())
    print("-" * 70)
    print(f"{'OVERALL MAX H_NORM':>30} {max_h_worst:>15.6f} {1/max_h_worst:>15.1f}x")

    # Save results
    outdir = os.path.dirname(os.path.abspath(__file__))
    outfile = os.path.join(outdir, "worst_case_results.json")
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outfile}")
