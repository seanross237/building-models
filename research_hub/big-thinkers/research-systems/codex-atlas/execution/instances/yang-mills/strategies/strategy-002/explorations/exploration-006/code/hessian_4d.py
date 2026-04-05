"""
Hessian Sharpness Check for SZZ Lemma 4.1 — 4D Lattice
========================================================
Measure H_normalized = |HessS(v,v)| / (8(d-1)N*beta*|v|^2)
for SU(2) lattice Yang-Mills on a 4^4 lattice (4D).

SZZ Lemma 4.1: |HessS(v,v)| <= 8(d-1)*N*beta * |v|^2
In 4D: bound = 8*3*2*beta = 48*beta

Compare with E005 3D results:
  3D (d=3): bound = 8*2*2*beta = 32*beta, max H_norm ≈ 0.02-0.08
  4D (d=4): bound = 8*3*2*beta = 48*beta, max H_norm = ?
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
    """(1/2) Re Tr U = q[0]"""
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
# 4D Lattice (L^4, d=4, ndim=4)
# ============================================================================

class Lattice4D:
    """4D SU(2) lattice gauge theory."""

    def __init__(self, L, beta):
        self.L = L
        self.beta = beta
        self.ndim = 4
        # links[x0, x1, x2, x3, mu, 4]
        self.links = np.zeros((L, L, L, L, 4, 4))
        self.links[..., 0] = 1.0  # cold start (identity)

    def hot_start(self):
        self.links = su2_random((self.L, self.L, self.L, self.L, 4))

    def get_link(self, x, mu):
        """x = (x0, x1, x2, x3), mu in [0,3]"""
        return self.links[x[0], x[1], x[2], x[3], mu].copy()

    def set_link(self, x, mu, U):
        self.links[x[0], x[1], x[2], x[3], mu] = U

    def shift(self, x, mu, d=1):
        """Shift position x by d in direction mu (periodic)."""
        s = list(x)
        s[mu] = (s[mu] + d) % self.L
        return tuple(s)

    def staple_sum(self, x, mu):
        """Sum of staples for link U_mu(x)."""
        A = np.zeros(4)
        for nu in range(self.ndim):
            if nu == mu:
                continue
            x_mu = self.shift(x, mu)
            x_nu = self.shift(x, nu)
            x_mu_mnu = self.shift(x_mu, nu, -1)
            x_mnu = self.shift(x, nu, -1)

            # Forward staple
            U1 = self.get_link(x_mu, nu)
            U2 = su2_dagger(self.get_link(x_nu, mu))
            U3 = su2_dagger(self.get_link(x, nu))
            fwd = su2_multiply(su2_multiply(U1, U2), U3)

            # Backward staple
            U4 = su2_dagger(self.get_link(x_mu_mnu, nu))
            U5 = su2_dagger(self.get_link(x_mnu, mu))
            U6 = self.get_link(x_mnu, nu)
            bwd = su2_multiply(su2_multiply(U4, U5), U6)

            A = A + fwd + bwd
        return A

    def sweep_heatbath(self):
        L = self.L
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        x = (x0, x1, x2, x3)
                        for mu in range(self.ndim):
                            A = self.staple_sum(x, mu)
                            U_new = heat_bath_su2(A, self.beta)
                            self.set_link(x, mu, U_new)

    def wilson_action(self):
        """S = -beta * sum_plaq (1/2) Re Tr(U_P). Returns scalar."""
        L = self.L
        S = 0.0
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        x = (x0, x1, x2, x3)
                        for mu in range(self.ndim):
                            for nu in range(mu+1, self.ndim):
                                x_mu = self.shift(x, mu)
                                x_nu = self.shift(x, nu)
                                U1 = self.get_link(x, mu)
                                U2 = self.get_link(x_mu, nu)
                                U3 = su2_dagger(self.get_link(x_nu, mu))
                                U4 = su2_dagger(self.get_link(x, nu))
                                P = su2_multiply(su2_multiply(su2_multiply(U1, U2), U3), U4)
                                S += -self.beta * su2_trace(P)
        return S

    def action_from_links(self, links):
        """Compute action from a given links array."""
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

    def average_plaquette(self):
        L = self.L
        total = 0.0
        count = 0
        for x0 in range(L):
            for x1 in range(L):
                for x2 in range(L):
                    for x3 in range(L):
                        x = (x0, x1, x2, x3)
                        for mu in range(self.ndim):
                            for nu in range(mu+1, self.ndim):
                                x_mu = self.shift(x, mu)
                                x_nu = self.shift(x, nu)
                                U1 = self.get_link(x, mu)
                                U2 = self.get_link(x_mu, nu)
                                U3 = su2_dagger(self.get_link(x_nu, mu))
                                U4 = su2_dagger(self.get_link(x, nu))
                                P = su2_multiply(su2_multiply(su2_multiply(U1, U2), U3), U4)
                                total += su2_trace(P)
                                count += 1
        return total / count

# ============================================================================
# Hessian Measurement
# ============================================================================

def su2_exp(v_su2, epsilon):
    """
    Compute exp(epsilon * v) for v in su(2).
    v is stored as (0, v1, v2, v3) — pure imaginary quaternion.
    """
    v1, v2, v3 = v_su2[1], v_su2[2], v_su2[3]
    norm_v = np.sqrt(v1**2 + v2**2 + v3**2)
    if norm_v < 1e-15:
        return np.array([1.0, 0.0, 0.0, 0.0])
    angle = epsilon * norm_v
    s = np.sin(angle) / norm_v
    return np.array([np.cos(angle), s * v1, s * v2, s * v3])

def make_tangent_vector(L, ndim=4):
    """
    Generate a random unit tangent vector for all links on the 4D lattice.
    Returns array of shape (L, L, L, L, ndim, 4) where [0] component = 0.
    Normalized so |v|^2 = sum_e |v_e|^2 = 1.
    """
    v = np.zeros((L, L, L, L, ndim, 4))
    v[..., 1] = np.random.randn(L, L, L, L, ndim)
    v[..., 2] = np.random.randn(L, L, L, L, ndim)
    v[..., 3] = np.random.randn(L, L, L, L, ndim)
    norm_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)
    v /= np.sqrt(norm_sq)
    return v

def perturb_links(links, v, epsilon, L, ndim=4):
    """
    Compute Q * exp(epsilon * v) for each link, return new links array.
    """
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
    """
    Finite-difference Hessian: HessS(v,v) ≈ [S(Q exp(ε v)) - 2S(Q) + S(Q exp(-ε v))] / ε²
    """
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

def measure_hessian_normalized_4d(L, beta, n_therm, n_configs, n_tangent, epsilon=1e-4, seed=None):
    """
    Measure H_normalized = |HessS(v,v)| / (8(d-1)*N*beta * |v|^2) on 4D lattice.

    In 4D: d=4, so (d-1)=3, N=2
    bound_factor = 8 * 3 * 2 * beta = 48 * beta
    """
    if seed is not None:
        np.random.seed(seed)

    ndim = 4
    N = 2
    d = 4
    # SZZ bound: 8(d-1)*N*beta = 8*3*2*beta = 48*beta
    bound_factor = 8 * (d - 1) * N * beta

    lat = Lattice4D(L, beta)
    lat.hot_start()

    print(f"  Thermalizing ({n_therm} sweeps)...", flush=True)
    for sweep in range(n_therm):
        lat.sweep_heatbath()
        if (sweep + 1) % 100 == 0:
            avg_p = lat.average_plaquette()
            print(f"    sweep {sweep+1}: avg_plaquette = {avg_p:.6f}", flush=True)

    all_h = []
    plaq_values = []

    print(f"  Measuring {n_configs} configs x {n_tangent} tangent vectors...", flush=True)
    for cfg in range(n_configs):
        # Do sweeps between measurements
        for _ in range(10):
            lat.sweep_heatbath()

        avg_p = lat.average_plaquette()
        plaq_values.append(avg_p)

        for t in range(n_tangent):
            v = make_tangent_vector(L, ndim)
            v_sq = np.sum(v[..., 1]**2 + v[..., 2]**2 + v[..., 3]**2)

            hess = compute_hessian_fd(lat, v, epsilon)

            if bound_factor > 1e-15:
                h_norm = abs(hess) / (bound_factor * v_sq)
            else:
                h_norm = 0.0

            all_h.append(h_norm)

        print(f"  Config {cfg+1}/{n_configs}: avg_plaq={avg_p:.5f}, "
              f"last h_norm={all_h[-1]:.4f}", flush=True)

    all_h = np.array(all_h)
    return {
        "beta": beta,
        "mean": float(np.mean(all_h)),
        "std": float(np.std(all_h)),
        "max": float(np.max(all_h)),
        "min": float(np.min(all_h)),
        "median": float(np.median(all_h)),
        "avg_plaq": float(np.mean(plaq_values)),
        "bound_factor": bound_factor,
        "n_values": len(all_h),
        "all_h": all_h.tolist()
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    L = 4
    N = 2
    d = 4
    epsilon = 1e-4
    n_therm = 500
    n_configs = 10
    n_tangent = 5

    beta_values = [0.02, 0.1, 0.5, 1.0]

    print("=" * 70)
    print("SZZ Lemma 4.1 Hessian Sharpness Check — 4D Lattice")
    print(f"L={L}, N={N}, d={d}, epsilon={epsilon}")
    print(f"n_therm={n_therm}, n_configs={n_configs}, n_tangent={n_tangent}")
    print(f"SZZ bound factor: 8*(d-1)*N*beta = 8*{d-1}*{N}*beta = {8*(d-1)*N}*beta")
    print("=" * 70)

    results = []

    for beta in beta_values:
        print(f"\n{'='*50}")
        print(f"beta = {beta}")
        bound_factor = 8 * (d - 1) * N * beta
        print(f"  SZZ bound: 8(d-1)N*beta = {bound_factor:.4f}")
        print(f"  SZZ threshold (d=4): beta < 1/48 = {1/48:.4f}")

        res = measure_hessian_normalized_4d(
            L=L,
            beta=beta,
            n_therm=n_therm,
            n_configs=n_configs,
            n_tangent=n_tangent,
            epsilon=epsilon,
            seed=42 + beta_values.index(beta)
        )

        results.append(res)

        print(f"\n  RESULT for beta={beta}:")
        print(f"    mean(H_norm) = {res['mean']:.4f}")
        print(f"    std(H_norm)  = {res['std']:.4f}")
        print(f"    max(H_norm)  = {res['max']:.4f}")
        print(f"    min(H_norm)  = {res['min']:.4f}")
        print(f"    avg_plaq     = {res['avg_plaq']:.5f}")
        print(f"    n_samples    = {res['n_values']}")

    print("\n" + "="*70)
    print("SUMMARY TABLE — 4D LATTICE")
    print(f"{'beta':>8} {'mean':>10} {'std':>10} {'max':>10} {'avg_plaq':>10} {'slack_factor'}")
    print("-"*70)
    for res in results:
        beta = res['beta']
        slack = 1.0 / res['max'] if res['max'] > 0 else float('inf')
        print(f"{beta:>8.3f} {res['mean']:>10.4f} {res['std']:>10.4f} {res['max']:>10.4f} "
              f"{res['avg_plaq']:>10.5f}  {slack:>10.1f}x")

    # Save results
    outdir = os.path.dirname(os.path.abspath(__file__))
    outfile = os.path.join(outdir, "results_4d.json")
    save_results = []
    for res in results:
        r = {k: v for k, v in res.items() if k != 'all_h'}
        save_results.append(r)

    with open(outfile, 'w') as f:
        json.dump(save_results, f, indent=2)
    print(f"\nResults saved to {outfile}")
