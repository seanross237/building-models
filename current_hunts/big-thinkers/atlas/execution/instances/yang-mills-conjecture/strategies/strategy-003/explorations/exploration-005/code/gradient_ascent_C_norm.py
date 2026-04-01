"""
Gradient ascent on ||C(Q)||_op to find the global maximum.
If the maximum is at Q=flat, this provides strong evidence for the decoherence lemma.
Also computes the Schur product bound and misalignment analysis.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, flat_config, random_config,
    plaquette_holonomy, isigma, get_link, compute_hessian_decomposed
)

def compute_C_norm(lat, Q):
    """Compute ||C(Q)||_op (spectral norm of cross-term)."""
    D, C = compute_hessian_decomposed(lat, Q)
    evals = np.linalg.eigvalsh(C)
    return max(abs(evals[0]), abs(evals[-1])), C

def su2_exp(w_vec):
    """exp(w_1*iσ_1 + w_2*iσ_2 + w_3*iσ_3)"""
    theta = np.linalg.norm(w_vec)
    if theta < 1e-14:
        return np.eye(2, dtype=complex)
    W = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * W

def project_su2(M):
    """Project to SU(2) via polar decomposition."""
    U, s, Vh = np.linalg.svd(M)
    P = U @ Vh
    if np.real(np.linalg.det(P)) < 0:
        P = -P
    d = np.linalg.det(P)
    P /= np.sqrt(d)
    return P

def gradient_ascent_C_norm(lat, Q_init, n_iters=200, lr=0.01):
    """
    Gradient ascent on ||C(Q)|| using finite differences.
    Returns trajectory of ||C|| values and final Q.
    """
    ne = lat.nedges
    Q = [q.copy() for q in Q_init]
    trajectory = []

    for it in range(n_iters):
        norm0, C0 = compute_C_norm(lat, Q)
        trajectory.append(norm0)

        # Compute top eigenvector direction for Rayleigh quotient gradient
        evals, evecs = np.linalg.eigh(C0)
        if abs(evals[-1]) >= abs(evals[0]):
            top_eval = evals[-1]
            top_evec = evecs[:, -1]
        else:
            top_eval = evals[0]
            top_evec = evecs[:, 0]

        # Gradient via finite differences: d(v^T C v)/dw_{e,a}
        grad = np.zeros((ne, 3))
        eps = 1e-4
        for e in range(ne):
            for a in range(3):
                w = np.zeros(3)
                w[a] = eps
                Q_plus = [q.copy() for q in Q]
                Q_plus[e] = su2_exp(w) @ Q[e]

                _, C_plus = compute_C_norm(lat, Q_plus)
                # Use Rayleigh quotient at the top eigenvector
                rq_plus = top_evec @ C_plus @ top_evec
                rq_0 = top_evec @ C0 @ top_evec
                grad[e, a] = (rq_plus - rq_0) / eps

        # Gradient step: multiply each Q_e by exp(lr * grad_e)
        for e in range(ne):
            w = lr * grad[e]
            if top_eval < 0:
                w = -w  # For negative eigenvalues, we want more negative
            Q[e] = su2_exp(w) @ Q[e]
            Q[e] = project_su2(Q[e])

        if it % 50 == 0 or it == n_iters - 1:
            print(f"  iter {it}: ||C|| = {norm0:.6f}, |top_eval| = {abs(top_eval):.6f}")

    return trajectory, Q

def gradient_ascent_fast(lat, Q_init, n_iters=300, lr=0.02):
    """
    Faster gradient ascent using random coordinate descent.
    At each step, perturb a random subset of edges and accept if ||C|| increases.
    """
    ne = lat.nedges
    Q = [q.copy() for q in Q_init]
    rng = np.random.default_rng(123)

    norm0, _ = compute_C_norm(lat, Q)
    trajectory = [norm0]

    for it in range(n_iters):
        # Random perturbation
        Q_trial = [q.copy() for q in Q]
        n_perturb = max(1, ne // 4)
        edges_to_perturb = rng.choice(ne, n_perturb, replace=False)
        for e in edges_to_perturb:
            w = lr * rng.normal(size=3)
            Q_trial[e] = su2_exp(w) @ Q_trial[e]
            Q_trial[e] = project_su2(Q_trial[e])

        norm_trial, _ = compute_C_norm(lat, Q_trial)

        if norm_trial > norm0:
            Q = Q_trial
            norm0 = norm_trial

        trajectory.append(norm0)

        if it % 100 == 0:
            print(f"  iter {it}: ||C|| = {norm0:.6f}")

    return trajectory, Q

def schur_product_analysis(lat, Q):
    """
    Analyze the Schur product structure.

    For aligned colors (all n_e = n): B_{ef}(n) = n^T G_{ef} n
    At flat: B = A_total (independent of n) with ||B|| = 2(d+1)
    At general Q: B depends on n, and max_n ||B(n)|| < ||A_total||

    Also: ||C(Q)|| = max_n ||B(n)|| * (misalignment factor)
    """
    ne = lat.nedges
    D, C = compute_hessian_decomposed(lat, Q)

    # Actual norm
    evals_C = np.linalg.eigvalsh(C)
    full_norm = max(abs(evals_C[0]), abs(evals_C[-1]))

    # Extract G blocks
    G = np.zeros((ne, ne, 3, 3))
    for e in range(ne):
        for f in range(ne):
            if e != f:
                G[e, f] = C[3*e:3*e+3, 3*f:3*f+3]

    # Max aligned norm: max over n of ||B(n)||
    rng = np.random.default_rng(42)
    max_aligned = 0
    best_n = None
    for _ in range(500):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)

        B = np.zeros((ne, ne))
        for e in range(ne):
            for f in range(ne):
                if e != f:
                    B[e, f] = n @ G[e, f] @ n

        ev = np.linalg.eigvalsh(B)
        norm_B = max(abs(ev[0]), abs(ev[-1]))
        if norm_B > max_aligned:
            max_aligned = norm_B
            best_n = n.copy()

    # Misalignment factor
    misalign_factor = full_norm / max_aligned if max_aligned > 0 else float('inf')

    return full_norm, max_aligned, misalign_factor, best_n

def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    target = 2 * (d + 1)
    rng = np.random.default_rng(42)

    print(f"{'='*80}")
    print(f"GRADIENT ASCENT ON ||C(Q)|| — d={d}, L={L}")
    print(f"Target: ||C_flat|| = {target}")
    print(f"{'='*80}")

    # =========================================================================
    # 1. Gradient ascent from random starts
    # =========================================================================
    print("\n--- Fast gradient ascent from random starts ---")
    max_found = 0
    for start in range(20):
        Q = random_config(lat, rng)
        norm0, _ = compute_C_norm(lat, Q)
        print(f"\nStart {start}: initial ||C|| = {norm0:.4f}")

        traj, Q_final = gradient_ascent_fast(lat, Q, n_iters=500, lr=0.03)
        final_norm = traj[-1]
        max_found = max(max_found, final_norm)
        print(f"  Final ||C|| = {final_norm:.4f}")

    print(f"\n*** Max ||C|| found across all starts: {max_found:.6f}")
    print(f"*** Flat value: {target:.6f}")
    print(f"*** Exceeds flat: {max_found > target + 0.01}")

    # =========================================================================
    # 2. Gradient ascent from near-flat
    # =========================================================================
    print(f"\n{'='*80}")
    print("GRADIENT ASCENT FROM NEAR-FLAT")
    print(f"{'='*80}")

    for eps_init in [0.01, 0.05, 0.1, 0.3, 0.5]:
        Q_flat = flat_config(lat)
        # Small random perturbation
        w_list = [eps_init * rng.normal(size=3) for _ in range(ne)]
        Q = [su2_exp(w) @ q for w, q in zip(w_list, Q_flat)]
        Q = [project_su2(q) for q in Q]

        norm0, _ = compute_C_norm(lat, Q)
        traj, Q_final = gradient_ascent_fast(lat, Q, n_iters=500, lr=0.02)
        print(f"eps={eps_init}: init ||C||={norm0:.4f}, final ||C||={traj[-1]:.4f}")

    # =========================================================================
    # 3. Gradient ascent from anti-instanton (E004's extremal config)
    # =========================================================================
    print(f"\n{'='*80}")
    print("GRADIENT ASCENT FROM ANTI-INSTANTON")
    print(f"{'='*80}")

    # Anti-instanton: Q_mu = iσ_a(mu) with axes assignment (0,0,2,1)
    axes = [0, 0, 2, 1]
    Q_ai = flat_config(lat)
    for mu in range(d):
        for site_idx in range(lat.nsites):
            e = mu * lat.nsites + site_idx
            Q_ai[e] = isigma[axes[mu]]
    norm_ai, _ = compute_C_norm(lat, Q_ai)
    print(f"Anti-instanton initial ||C|| = {norm_ai:.4f}")

    traj, Q_final = gradient_ascent_fast(lat, Q_ai, n_iters=1000, lr=0.03)
    print(f"After gradient ascent: ||C|| = {traj[-1]:.4f}")

    # =========================================================================
    # 4. Schur product / misalignment analysis
    # =========================================================================
    print(f"\n{'='*80}")
    print("SCHUR PRODUCT / MISALIGNMENT ANALYSIS")
    print(f"{'='*80}")

    # Flat
    Q_flat = flat_config(lat)
    fn, an, mf, bn = schur_product_analysis(lat, Q_flat)
    print(f"FLAT: full={fn:.4f}, aligned={an:.4f}, misalign_factor={mf:.4f}")

    # Random configs
    misalign_factors = []
    aligned_norms = []
    full_norms = []
    for trial in range(30):
        Q = random_config(lat, rng)
        fn, an, mf, bn = schur_product_analysis(lat, Q)
        full_norms.append(fn)
        aligned_norms.append(an)
        misalign_factors.append(mf)

    print(f"\nRandom configs (30):")
    print(f"  Full norm: max={max(full_norms):.4f}, mean={np.mean(full_norms):.4f}")
    print(f"  Aligned norm: max={max(aligned_norms):.4f}, mean={np.mean(aligned_norms):.4f}")
    print(f"  Misalign factor: max={max(misalign_factors):.4f}, mean={np.mean(misalign_factors):.4f}")

    # Near-flat configs (should have high aligned norm)
    print(f"\nNear-flat configs (eps=0.1, 0.3, 0.5, 1.0):")
    for eps in [0.1, 0.3, 0.5, 1.0]:
        Q = [su2_exp(eps * rng.normal(size=3)) for _ in range(ne)]
        Q = [project_su2(q) for q in Q]
        fn, an, mf, bn = schur_product_analysis(lat, Q)
        print(f"  eps={eps}: full={fn:.4f}, aligned={an:.4f}, misalign={mf:.4f}, product={an*mf:.4f}")

    # =========================================================================
    # 5. Dimension scaling
    # =========================================================================
    print(f"\n{'='*80}")
    print("DIMENSION SCALING")
    print(f"{'='*80}")

    for dd in [2, 3, 4]:
        lat_d = Lattice(dd, 2)
        Q_f = flat_config(lat_d)
        norm_f, _ = compute_C_norm(lat_d, Q_f)

        max_rand = 0
        for _ in range(100):
            Q = random_config(lat_d, rng)
            n, _ = compute_C_norm(lat_d, Q)
            max_rand = max(max_rand, n)

        print(f"d={dd}: ||C_flat||={norm_f:.4f}, max_random={max_rand:.4f}, "
              f"target=2(d+1)={2*(dd+1)}, ratio={max_rand/norm_f:.4f}")

if __name__ == "__main__":
    main()
