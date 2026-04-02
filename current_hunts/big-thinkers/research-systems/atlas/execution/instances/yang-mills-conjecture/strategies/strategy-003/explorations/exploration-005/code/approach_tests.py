"""
Test all 6 proof approaches for the decoherence lemma ||C(Q)|| <= 2(d+1).
Each approach is tested numerically for d=4, L=2 with 100 random configs.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, flat_config, random_config,
    plaquette_holonomy, isigma, get_link, su2_to_quat, adjoint_so3,
    cross_product_matrix, color_kernel_direct, color_kernel_formula,
    compute_hessian_decomposed
)

def compute_C_and_blocks(lat, Q, beta=1.0, N=2):
    """Compute cross-term C and per-edge-pair G blocks, plus per-plaquette data."""
    ne = lat.nedges
    dim = 3 * ne
    C = np.zeros((dim, dim))

    # Per-plaquette, per-pair data
    plaq_pair_data = []  # list of (ep,eq, sp,sq, F_block, beta0, beta_vec, R_M)

    for pidx, plaq in enumerate(lat.plaquettes):
        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ get_link(Q, *edges_list[k])
                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ get_link(Q, *edges_list[k])
                R = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R = R @ get_link(Q, *edges_list[k])

                # F_{ab} = Re Tr(L iσ_a mid iσ_b R) = Re Tr(iσ_a mid iσ_b (R L))
                M_ctx = mid
                N_ctx = R @ L
                W = M_ctx @ N_ctx
                beta0, beta_vec = su2_to_quat(W)
                R_M = adjoint_so3(M_ctx)

                F_block = np.zeros((3, 3))
                for a in range(3):
                    for b in range(3):
                        F_block[a, b] = np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R)
                        )

                contrib = -(beta/N) * sp * sq * F_block
                for a in range(3):
                    for b in range(3):
                        C[3*ep+a, 3*eq+b] += contrib[a, b]
                        C[3*eq+b, 3*ep+a] += contrib[a, b]

                plaq_pair_data.append({
                    'ep': ep, 'eq': eq, 'sp': sp, 'sq': sq,
                    'F': F_block, 'beta0': beta0, 'beta_vec': beta_vec,
                    'R_M': R_M, 'contrib': contrib
                })

    return C, plaq_pair_data

def compute_A_total(lat):
    """Compute the spatial adjacency A_total (|E| x |E|) at flat."""
    ne = lat.nedges
    A = np.zeros((ne, ne))
    for plaq in lat.plaquettes:
        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]
                A[ep, eq] += sp * sq
                A[eq, ep] += sp * sq
    return A

def approach1_tensor_bound(C, A_total, plaq_data, ne):
    """Approach 1: Tensor product norm bound.
    Try: ||C|| <= ||Sigma A_i|| * max ||F_i|| = ||A_total|| * 2? No, this uses PSD structure.

    Modified: decompose A_total = A+ - A- and bound each.
    """
    # A_total eigendecomposition
    evals_A = np.linalg.eigvalsh(A_total)
    norm_A = max(abs(evals_A[0]), abs(evals_A[-1]))

    # Since each F has ||F|| = 2, the naive bound is:
    # Each plaquette contributes C_sq = sum of rank-1 spatial ⊗ F^{pq}
    # ||C|| <= sum_sq ||C_sq|| ... but this overcounts edges

    # The bound ||C|| <= 2 * ||A_total|| follows IF all color kernels are scalar multiples
    # of the same contraction (as at flat). For general Q, we bound:
    # ||C|| <= ||abs(A_total)|| * 2 where abs takes entrywise absolute values
    A_abs = np.abs(A_total)
    evals_abs = np.linalg.eigvalsh(A_abs)
    bound = max(abs(evals_abs))

    return bound, norm_A

def approach2_kronecker_bound(C, A_total, plaq_data, ne):
    """Approach 2: For v = (r_e * n_e), bound v^T C v using ||F|| <= 2.

    |v^T C v| = |sum_{ef} r_e r_f n_e^T G_{ef} n_f|
              <= sum_{ef} |r_e r_f| * ||G_{ef}||
              = r^T M r  where M_{ef} = ||G_{ef}||
    So ||C|| <= ||M||.
    """
    # Compute G blocks
    G = {}
    for d in plaq_data:
        key = (d['ep'], d['eq'])
        rkey = (d['eq'], d['ep'])
        if key not in G:
            G[key] = np.zeros((3,3))
        G[key] += d['contrib']

    # Compute ||G_{ef}|| matrix
    M = np.zeros((ne, ne))
    for (e, f), block in G.items():
        M[e, f] = np.linalg.norm(block, ord=2)
        M[f, e] = np.linalg.norm(block.T, ord=2)  # G_{fe} = G_{ef}^T

    evals_M = np.linalg.eigvalsh(M)
    bound = max(abs(evals_M[0]), abs(evals_M[-1]))
    return bound

def approach3_cauchy_schwarz_misalignment(C, plaq_data, ne, d):
    """Approach 3: Cauchy-Schwarz with color misalignment.

    For aligned color (all n_e = n), the quadratic form becomes:
    v^T C v = r^T B(n) r  where B(n)_{ef} = n^T G_{ef} n

    Bound: max_n ||B(n)|| (scan over directions n)
    """
    # Compute G blocks
    G = {}
    for dat in plaq_data:
        key = (dat['ep'], dat['eq'])
        if key not in G:
            G[key] = np.zeros((3,3))
        G[key] += dat['contrib']

    # Scan over color directions
    max_norm = 0
    rng = np.random.default_rng(42)
    for _ in range(200):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)

        B = np.zeros((ne, ne))
        for (e, f), block in G.items():
            B[e, f] = n @ block @ n
            B[f, e] = n @ block.T @ n

        evals_B = np.linalg.eigvalsh(B)
        norm_B = max(abs(evals_B[0]), abs(evals_B[-1]))
        max_norm = max(max_norm, norm_B)

    return max_norm

def approach4_per_plaquette(C, lat, Q, d):
    """Approach 4: Per-plaquette bound.

    ||C|| = ||sum_sq C_sq|| <= sum_sq ||C_sq||
    But each edge appears in 2(d-1) plaquettes, so this overcounts.

    Better: use edge-disjoint grouping or Gershgorin-like argument.
    """
    ne = lat.nedges

    # Compute per-plaquette cross-term contribution
    plaq_norms = []
    for pidx, plaq in enumerate(lat.plaquettes):
        # Build the 12x12 (4 edges x 3 colors) sub-matrix
        edges_list = plaq
        edge_indices = [e for e, s in edges_list]

        C_plaq = np.zeros((12, 12))
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ get_link(Q, *edges_list[k])
                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ get_link(Q, *edges_list[k])
                R_mat = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R_mat = R_mat @ get_link(Q, *edges_list[k])

                for a in range(3):
                    for b in range(3):
                        val = -0.5 * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R_mat)
                        )
                        C_plaq[3*p_idx+a, 3*q_idx+b] += val
                        C_plaq[3*q_idx+b, 3*p_idx+a] += val

        evals = np.linalg.eigvalsh(C_plaq)
        plaq_norms.append(max(abs(evals[0]), abs(evals[-1])))

    # Triangle inequality bound
    triangle_bound = sum(plaq_norms)

    # Average per plaquette: each edge is in 2(d-1) plaquettes
    # So the "diluted" bound is: max_e sum_{sq containing e} ||C_sq|| / 2(d-1)
    # ... this isn't quite right. Return the triangle bound.

    return triangle_bound, np.max(plaq_norms), np.mean(plaq_norms)

def approach5_variational_perturbation(lat, d, n_perturbations=50):
    """Approach 5: Show flat is global max of ||C||.

    1. Compute ||C_flat|| = 2(d+1)
    2. Perturb flat by eps * random and check ||C(Q+eps)|| < ||C_flat||
    3. Compute the 2nd derivative numerically
    """
    Q_flat = flat_config(lat)
    D_flat, C_flat = compute_hessian_decomposed(lat, Q_flat)
    evals_flat = np.linalg.eigvalsh(C_flat)
    norm_flat = max(abs(evals_flat[0]), abs(evals_flat[-1]))

    results = {'norm_flat': norm_flat, 'perturbations': []}
    rng = np.random.default_rng(42)

    for trial in range(n_perturbations):
        # Random perturbation direction
        epsilons = [0.01, 0.05, 0.1, 0.3, 0.5, 1.0]
        trial_data = []

        # Generate random tangent vectors
        w = [rng.normal(size=3) for _ in range(lat.nedges)]

        for eps in epsilons:
            Q_pert = []
            for e in range(lat.nedges):
                # exp(eps * w_e . isigma)
                theta = np.linalg.norm(w[e]) * eps
                if theta < 1e-14:
                    Q_pert.append(np.eye(2, dtype=complex))
                else:
                    wn = w[e] / np.linalg.norm(w[e])
                    W = sum(wn[a] * isigma[a] for a in range(3))
                    Q_pert.append(np.cos(theta) * np.eye(2, dtype=complex) +
                                  np.sin(theta) / (np.linalg.norm(w[e]) * eps) * eps * sum(w[e][a] * isigma[a] for a in range(3)))

            # Simpler: just use the exponential map
            Q_pert2 = []
            for e in range(lat.nedges):
                wvec = eps * w[e]
                theta = np.linalg.norm(wvec)
                if theta < 1e-14:
                    Q_pert2.append(np.eye(2, dtype=complex))
                else:
                    W = sum(wvec[a] * isigma[a] for a in range(3))
                    Q_pert2.append(np.cos(theta)*np.eye(2, dtype=complex) + (np.sin(theta)/theta)*W)

            D_p, C_p = compute_hessian_decomposed(lat, Q_pert2)
            evals_p = np.linalg.eigvalsh(C_p)
            norm_p = max(abs(evals_p[0]), abs(evals_p[-1]))
            trial_data.append((eps, norm_p))

        results['perturbations'].append(trial_data)

    return results

def approach6_schur_product(C, A_total, plaq_data, ne):
    """Approach 6: Schur product bound.

    At flat: C = A_total ⊗ I_3, and the quadratic form with aligned colors
    gives A_total ∘ N where N_{ef} = n_e . n_f is a correlation matrix.

    Schur product theorem: ||A ∘ N|| <= ||A|| for correlation matrix N.
    So at flat, max over n_e is ||A_total||.

    At general Q: B_{ef}^(n) = n_e^T G_{ef} n_f.
    Is B a Schur product of anything nice?
    """
    # Compute G blocks
    G = {}
    for dat in plaq_data:
        key = (dat['ep'], dat['eq'])
        if key not in G:
            G[key] = np.zeros((3,3))
        G[key] += dat['contrib']

    # For aligned color (all same n):
    # B_{ef}(n) = n^T G_{ef} n
    # At flat: G_{ef} = c_{ef} I, so B = A_total (independent of n)
    # At general Q: G_{ef} not proportional to I

    # Compute max over misaligned colors using the full eigenvector
    actual_evals = np.linalg.eigvalsh(C)
    actual_norm = max(abs(actual_evals[0]), abs(actual_evals[-1]))

    # Compute aligned-color norm (max over n of ||B(n)||)
    aligned_norm = approach3_cauchy_schwarz_misalignment(C, plaq_data, ne, 4)

    return actual_norm, aligned_norm


def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    print(f"Lattice: d={d}, L={L}, nedges={ne}, nplaq={lat.nplaq}")

    A_total = compute_A_total(lat)
    evals_A = np.linalg.eigvalsh(A_total)
    print(f"||A_total|| = {max(abs(evals_A[0]), abs(evals_A[-1])):.4f}")
    print(f"Expected 2(d+1) = {2*(d+1)}")
    print(f"A_total eigenvalues: min={evals_A[0]:.4f}, max={evals_A[-1]:.4f}")

    target = 2 * (d + 1)
    rng = np.random.default_rng(42)
    n_configs = 50

    # Arrays to collect results
    actual_norms = []
    a1_bounds = []
    a2_bounds = []
    a3_bounds = []
    a4_bounds_tri = []
    a4_bounds_max = []
    beta0_stats = []

    print(f"\n{'='*80}")
    print(f"Testing {n_configs} random configs. Target bound: {target}")
    print(f"{'='*80}")

    for trial in range(n_configs):
        Q = random_config(lat, rng)
        C, plaq_data = compute_C_and_blocks(lat, Q)
        evals_C = np.linalg.eigvalsh(C)
        actual_norm = max(abs(evals_C[0]), abs(evals_C[-1]))
        actual_norms.append(actual_norm)

        # Collect beta0 stats
        beta0s = [abs(d['beta0']) for d in plaq_data]
        beta0_stats.append(np.mean(beta0s))

        # Approach 1
        b1, norm_A = approach1_tensor_bound(C, A_total, plaq_data, ne)
        a1_bounds.append(b1)

        # Approach 2
        b2 = approach2_kronecker_bound(C, A_total, plaq_data, ne)
        a2_bounds.append(b2)

        # Approach 3 (expensive — reduce scan for survey)
        G = {}
        for dat in plaq_data:
            key = (dat['ep'], dat['eq'])
            if key not in G:
                G[key] = np.zeros((3,3))
            G[key] += dat['contrib']

        # Quick aligned norm (just axis-aligned)
        max_aligned = 0
        for ax in range(3):
            n = np.zeros(3); n[ax] = 1
            B = np.zeros((ne, ne))
            for (e, f), block in G.items():
                B[e, f] = n @ block @ n
                B[f, e] = n @ block.T @ n
            ev = np.linalg.eigvalsh(B)
            max_aligned = max(max_aligned, max(abs(ev[0]), abs(ev[-1])))
        a3_bounds.append(max_aligned)

        if trial < 3:
            print(f"\nConfig {trial}: ||C|| = {actual_norm:.4f}, mean|β₀| = {np.mean(beta0s):.4f}")
            print(f"  A1 (|A_total| bound): {b1:.4f}")
            print(f"  A2 (||G_ef|| bound): {b2:.4f}")
            print(f"  A3 (aligned color): {max_aligned:.4f}")

    print(f"\n{'='*80}")
    print("SUMMARY OVER {n_configs} CONFIGS")
    print(f"{'='*80}")
    print(f"Target: ||C|| <= {target}")
    print(f"Actual ||C||: max = {max(actual_norms):.4f}, mean = {np.mean(actual_norms):.4f}")
    print(f"Violations (||C|| > {target}): {sum(1 for x in actual_norms if x > target + 0.01)}")
    print()

    print("Approach 1 (|A_total| entrywise abs bound):")
    print(f"  Max bound: {max(a1_bounds):.4f} (tight iff <= {target})")
    a1_norm = max(a1_bounds)
    print(f"  {'WORKS' if a1_norm <= target + 0.01 else 'TOO LOOSE'}: gives ||C|| <= {a1_norm:.4f}")
    print()

    print("Approach 2 (per-block norm bound ||G_ef||):")
    print(f"  Max bound: {max(a2_bounds):.4f}")
    print(f"  {'WORKS' if max(a2_bounds) <= target + 0.01 else 'TOO LOOSE'}")
    print()

    print("Approach 3 (aligned color max over axes):")
    print(f"  Max bound: {max(a3_bounds):.4f}")
    print(f"  {'WORKS' if max(a3_bounds) <= target + 0.01 else 'TOO LOOSE'}")
    print()

    print(f"Mean |β₀| across configs: {np.mean(beta0_stats):.4f}")
    print(f"  (At flat: |β₀| = 1.0; lower means more decoherence)")

    # =========================================================================
    # Approach 5: Variational (perturbation around flat)
    # =========================================================================
    print(f"\n{'='*80}")
    print("APPROACH 5: Perturbation around flat")
    print(f"{'='*80}")

    results = approach5_variational_perturbation(lat, d, n_perturbations=30)
    print(f"||C_flat|| = {results['norm_flat']:.6f}")

    # Check: is ||C|| < ||C_flat|| for ALL perturbations?
    all_decrease = True
    max_norm_any = results['norm_flat']
    for trial_data in results['perturbations']:
        for eps, norm_p in trial_data:
            if norm_p > results['norm_flat'] + 1e-10:
                all_decrease = False
                max_norm_any = max(max_norm_any, norm_p)

    print(f"All perturbations decrease ||C||: {all_decrease}")
    if not all_decrease:
        print(f"  Max ||C|| found: {max_norm_any:.6f}")

    # Compute 2nd derivative numerically from the eps=0.01 data
    print("\nSecond derivative d²||C||/dε² at flat:")
    second_derivs = []
    for trial_data in results['perturbations'][:10]:
        # Use eps=0.01 and eps=0.05
        eps1, n1 = trial_data[0]  # 0.01
        eps2, n2 = trial_data[1]  # 0.05
        # ||C(eps)|| ≈ ||C_flat|| + (eps²/2) * d²||C||/deps²
        # d2 ≈ 2 * (||C(eps)|| - ||C_flat||) / eps²
        d2_1 = 2 * (n1 - results['norm_flat']) / eps1**2
        d2_2 = 2 * (n2 - results['norm_flat']) / eps2**2
        second_derivs.append(d2_1)

    print(f"  Values (from eps=0.01): {[f'{x:.2f}' for x in second_derivs]}")
    print(f"  All negative: {all(x < 0 for x in second_derivs)}")
    print(f"  Mean: {np.mean(second_derivs):.4f}")

    # =========================================================================
    # Approach 4: Per-plaquette (on a few configs)
    # =========================================================================
    print(f"\n{'='*80}")
    print("APPROACH 4: Per-plaquette bound")
    print(f"{'='*80}")

    for trial in range(5):
        Q = random_config(lat, rng)
        tri, maxp, meanp = approach4_per_plaquette(None, lat, Q, d)
        _, C_check = compute_hessian_decomposed(lat, Q)
        ev = np.linalg.eigvalsh(C_check)
        actual = max(abs(ev[0]), abs(ev[-1]))
        print(f"Config {trial}: ||C||={actual:.2f}, triangle={tri:.2f}, max_plaq={maxp:.2f}, mean_plaq={meanp:.2f}")

    # =========================================================================
    # Approach 6: Full vs aligned norm comparison
    # =========================================================================
    print(f"\n{'='*80}")
    print("APPROACH 6: Full norm vs aligned-color norm")
    print(f"{'='*80}")

    for trial in range(10):
        Q = random_config(lat, rng)
        C, plaq_data = compute_C_and_blocks(lat, Q)
        full_norm, aligned_norm = approach6_schur_product(C, A_total, plaq_data, ne)
        print(f"Config {trial}: full_norm={full_norm:.4f}, aligned={aligned_norm:.4f}, ratio={full_norm/aligned_norm:.4f}")

if __name__ == "__main__":
    main()
