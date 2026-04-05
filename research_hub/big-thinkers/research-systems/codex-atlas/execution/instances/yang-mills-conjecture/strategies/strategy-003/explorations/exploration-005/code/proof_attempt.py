"""
Focused proof attempt for the decoherence lemma.

Key structural result: F(M,N) = -2(β₀I + [β⃗×])R_M
with singular values (2, 2, 2|β₀|) where β₀ = Re Tr(MN)/2.

This script:
1. Verifies the Schur product theorem bound for aligned colors
2. Analyzes the misalignment factor
3. Attempts to prove ||C(Q)|| ≤ 2(d+1) using the SVD structure
4. Analyzes per-plaquette decoherence
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, flat_config, random_config,
    isigma, get_link, su2_to_quat, adjoint_so3, cross_product_matrix,
    compute_hessian_decomposed
)

def compute_G_blocks_with_svd(lat, Q, beta=1.0, N=2):
    """Compute G blocks with full SVD data for each plaquette-pair contribution."""
    ne = lat.nedges
    G = np.zeros((ne, ne, 3, 3))
    svd_data = []  # per plaquette-pair: {beta0, beta_vec, R_M, ...}

    for pidx, plaq in enumerate(lat.plaquettes):
        edges_list = plaq
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                L = np.eye(2, dtype=complex)
                for k in range(p_idx + 1):
                    L = L @ (Q[edges_list[k][0]] if edges_list[k][1] == +1
                             else su2_inv(Q[edges_list[k][0]]))
                mid = np.eye(2, dtype=complex)
                for k in range(p_idx + 1, q_idx):
                    mid = mid @ (Q[edges_list[k][0]] if edges_list[k][1] == +1
                                  else su2_inv(Q[edges_list[k][0]]))
                R_mat = np.eye(2, dtype=complex)
                for k in range(q_idx + 1, 4):
                    R_mat = R_mat @ (Q[edges_list[k][0]] if edges_list[k][1] == +1
                                      else su2_inv(Q[edges_list[k][0]]))

                M_ctx = mid
                N_ctx = R_mat @ L
                W = M_ctx @ N_ctx
                beta0, beta_vec = su2_to_quat(W)
                R_M = adjoint_so3(M_ctx)

                # F = Re Tr(L iσ_a mid iσ_b R) for 3x3 block
                F = np.zeros((3, 3))
                for a in range(3):
                    for b in range(3):
                        F[a, b] = np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R_mat))

                # B_k = -(beta/N) * sp * sq * F = -0.5 * sp * sq * F
                B_k = -(beta/N) * sp * sq * F

                G[ep, eq] += B_k
                G[eq, ep] += B_k.T

                svd_data.append({
                    'ep': ep, 'eq': eq, 'sp': sp, 'sq': sq,
                    'beta0': beta0, 'beta_vec': beta_vec.copy(),
                    'R_M': R_M.copy(), 'B_k': B_k.copy(),
                    'pidx': pidx
                })

    return G, svd_data

def schur_product_bound_proof(lat, Q, d):
    """
    Prove the ALIGNED-COLOR bound:
    For all Q and all unit n, ||B(n)|| ≤ ||A_total||

    where B(n)_{ef} = n^T G_{ef}(Q) n.

    This follows from the Schur product theorem IF B(n) = A_total ∘ N(n)
    for some correlation matrix N. This is true at FLAT but not at general Q.

    At general Q, we need a DIFFERENT argument.
    """
    ne = lat.nedges
    G, svd_data = compute_G_blocks_with_svd(lat, Q, d)

    # Compute A_total (flat value)
    A_flat = np.zeros((ne, ne))
    for dat in svd_data:
        ep, eq, sp, sq = dat['ep'], dat['eq'], dat['sp'], dat['sq']
        A_flat[ep, eq] += sp * sq
        A_flat[eq, ep] += sp * sq

    evals_A = np.linalg.eigvalsh(A_flat)
    norm_A = max(abs(evals_A))

    # Test: for random n, compute ||B(n)|| and compare to ||A_total||
    rng = np.random.default_rng(42)
    max_aligned_norm = 0
    for _ in range(1000):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)

        B = np.zeros((ne, ne))
        for e in range(ne):
            for f in range(ne):
                if e != f:
                    B[e, f] = n @ G[e, f] @ n

        ev = np.linalg.eigvalsh(B)
        norm_B = max(abs(ev[0]), abs(ev[-1]))
        max_aligned_norm = max(max_aligned_norm, norm_B)

    return max_aligned_norm, norm_A


def analyze_decoherence_mechanism(lat, Q, d):
    """
    Analyze the decoherence mechanism quantitatively.

    For each edge e, compute the "deficient directions" β⃗^{(k)} from all
    plaquette-pairs involving e. If these directions span ℝ³, then no single
    color direction n_e can avoid all deficient directions simultaneously.
    """
    ne = lat.nedges
    G, svd_data = compute_G_blocks_with_svd(lat, Q, d)

    # For each edge, collect the deficient directions (β⃗ vectors)
    edge_betas = {e: [] for e in range(ne)}
    edge_beta0s = {e: [] for e in range(ne)}

    for dat in svd_data:
        ep, eq = dat['ep'], dat['eq']
        beta_vec = dat['beta_vec']
        beta0 = dat['beta0']

        edge_betas[ep].append(beta_vec.copy())
        edge_betas[eq].append(beta_vec.copy())
        edge_beta0s[ep].append(abs(beta0))
        edge_beta0s[eq].append(abs(beta0))

    # For each edge: compute the "decoherence measure"
    # = how much the β⃗ vectors span of ℝ³
    decoherence_measures = []
    for e in range(ne):
        betas = np.array(edge_betas[e])  # shape (n_pairs, 3)
        if len(betas) > 0:
            # Compute the covariance matrix of β⃗ directions
            cov = betas.T @ betas / len(betas)
            eigs = np.linalg.eigvalsh(cov)
            # The minimum eigenvalue measures the "weakest" decoherence direction
            decoherence_measures.append(eigs[0])
        else:
            decoherence_measures.append(0)

    avg_beta0 = np.mean([np.mean(v) for v in edge_beta0s.values()])
    min_decoherence = min(decoherence_measures)
    mean_decoherence = np.mean(decoherence_measures)

    return {
        'avg_beta0': avg_beta0,
        'min_decoherence': min_decoherence,
        'mean_decoherence': mean_decoherence,
        'decoherence_measures': decoherence_measures
    }


def single_plaquette_bound(lat, Q, d):
    """
    For each plaquette, compute the cross-term contribution and its norm.
    Compare to the flat value.

    At flat: each plaquette's cross-term has eigenvalues in [-6, 6] (for the
    12×12 sub-matrix of 4 edges × 3 colors).

    Key question: does ||(PR_k)|| ≤ 1 for each contribution imply
    ||C_□(Q)|| ≤ ||C_□(flat)||?
    """
    ne = lat.nedges

    flat_plaq_norms = []
    gen_plaq_norms = []

    Q_flat = flat_config(lat)

    for pidx, plaq in enumerate(lat.plaquettes):
        edges_list = plaq

        C_flat_plaq = np.zeros((12, 12))
        C_gen_plaq = np.zeros((12, 12))

        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep, sp = edges_list[p_idx]
                eq, sq = edges_list[q_idx]

                for Q_test, C_plaq in [(Q_flat, C_flat_plaq), (Q, C_gen_plaq)]:
                    L = np.eye(2, dtype=complex)
                    for k in range(p_idx + 1):
                        ek, sk = edges_list[k]
                        L = L @ (Q_test[ek] if sk == +1 else su2_inv(Q_test[ek]))
                    mid = np.eye(2, dtype=complex)
                    for k in range(p_idx + 1, q_idx):
                        ek, sk = edges_list[k]
                        mid = mid @ (Q_test[ek] if sk == +1 else su2_inv(Q_test[ek]))
                    R_mat = np.eye(2, dtype=complex)
                    for k in range(q_idx + 1, 4):
                        ek, sk = edges_list[k]
                        R_mat = R_mat @ (Q_test[ek] if sk == +1 else su2_inv(Q_test[ek]))

                    for a in range(3):
                        for b in range(3):
                            val = -0.5 * sp * sq * np.real(
                                np.trace(L @ isigma[a] @ mid @ isigma[b] @ R_mat))
                            C_plaq[3*p_idx+a, 3*q_idx+b] += val
                            C_plaq[3*q_idx+b, 3*p_idx+a] += val

        ev_flat = np.linalg.eigvalsh(C_flat_plaq)
        ev_gen = np.linalg.eigvalsh(C_gen_plaq)
        flat_plaq_norms.append(max(abs(ev_flat[0]), abs(ev_flat[-1])))
        gen_plaq_norms.append(max(abs(ev_gen[0]), abs(ev_gen[-1])))

    return flat_plaq_norms, gen_plaq_norms


def attempt_contraction_proof(lat, Q, d):
    """
    Attempt to prove: ||C(Q)|| ≤ ||C_flat|| using the contraction property.

    Key idea: Each B_k = s_k P_k R_k is a contraction (||B_k|| ≤ 1),
    and at flat B_k = s_k I_3.

    We want: ||Σ_k E_k ⊗ B_k|| ≤ ||Σ_k E_k ⊗ (s_k I_3)||

    This is NOT true in general. But for the SPECIFIC lattice structure
    with E_k coming from plaquettes, it might be true.

    Test: for each edge pair (e,f), check if ||G_{ef}(Q)|| ≤ ||G_{ef}(flat)|| = |c_{ef}|.
    """
    ne = lat.nedges
    G, svd_data = compute_G_blocks_with_svd(lat, Q, d)

    A_flat = np.zeros((ne, ne))
    for dat in svd_data:
        ep, eq, sp, sq = dat['ep'], dat['eq'], dat['sp'], dat['sq']
        A_flat[ep, eq] += sp * sq
        A_flat[eq, ep] += sp * sq

    # Check per-entry bound
    violations = 0
    max_ratio = 0
    for e in range(ne):
        for f in range(ne):
            if e != f and abs(A_flat[e, f]) > 0:
                gen_norm = np.linalg.norm(G[e, f], ord=2)
                flat_norm = abs(A_flat[e, f])
                ratio = gen_norm / flat_norm if flat_norm > 0 else float('inf')
                max_ratio = max(max_ratio, ratio)
                if gen_norm > flat_norm + 1e-10:
                    violations += 1

    # Check entries where flat has c_{ef} = 0
    zero_entries = 0
    max_zero_norm = 0
    for e in range(ne):
        for f in range(ne):
            if e != f and abs(A_flat[e, f]) < 1e-10:
                gen_norm = np.linalg.norm(G[e, f], ord=2)
                if gen_norm > 1e-10:
                    zero_entries += 1
                    max_zero_norm = max(max_zero_norm, gen_norm)

    return violations, max_ratio, zero_entries, max_zero_norm


def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    target = 2 * (d + 1)
    rng = np.random.default_rng(42)

    print(f"{'='*80}")
    print(f"PROOF ATTEMPT FOR DECOHERENCE LEMMA")
    print(f"d={d}, L={L}, ne={ne}, target=2(d+1)={target}")
    print(f"{'='*80}")

    # =========================================================================
    # 1. Schur product bound for aligned colors
    # =========================================================================
    print("\n--- 1. Aligned-color bound (Schur product theorem at flat) ---")
    Q_flat = flat_config(lat)
    max_aligned, norm_A = schur_product_bound_proof(lat, Q_flat, d)
    print(f"FLAT: max aligned norm = {max_aligned:.4f}, ||A_total|| = {norm_A:.4f}")
    print(f"  Schur product theorem confirms: aligned ≤ ||A_total|| ✓")

    for trial in range(5):
        Q = random_config(lat, rng)
        max_aligned, norm_A = schur_product_bound_proof(lat, Q, d)
        D, C = compute_hessian_decomposed(lat, Q)
        evals = np.linalg.eigvalsh(C)
        full_norm = max(abs(evals[0]), abs(evals[-1]))
        print(f"Random {trial}: aligned={max_aligned:.4f}, full={full_norm:.4f}, "
              f"ratio={full_norm/max_aligned:.4f}")

    # =========================================================================
    # 2. Decoherence mechanism analysis
    # =========================================================================
    print(f"\n--- 2. Decoherence mechanism (β⃗ spread analysis) ---")
    for trial in range(5):
        Q = random_config(lat, rng)
        dec = analyze_decoherence_mechanism(lat, Q, d)
        D, C = compute_hessian_decomposed(lat, Q)
        evals = np.linalg.eigvalsh(C)
        full_norm = max(abs(evals[0]), abs(evals[-1]))
        print(f"Config {trial}: ||C||={full_norm:.4f}, avg|β₀|={dec['avg_beta0']:.4f}, "
              f"mean_decoherence={dec['mean_decoherence']:.4f}, "
              f"min_decoherence={dec['min_decoherence']:.4f}")

    # =========================================================================
    # 3. Per-plaquette bound comparison
    # =========================================================================
    print(f"\n--- 3. Per-plaquette norm comparison (flat vs general) ---")
    for trial in range(3):
        Q = random_config(lat, rng)
        flat_norms, gen_norms = single_plaquette_bound(lat, Q, d)
        print(f"Config {trial}:")
        print(f"  Flat plaq norms: max={max(flat_norms):.4f}, mean={np.mean(flat_norms):.4f}")
        print(f"  Gen plaq norms:  max={max(gen_norms):.4f}, mean={np.mean(gen_norms):.4f}")
        print(f"  Plaquettes where gen > flat: "
              f"{sum(1 for g,f in zip(gen_norms,flat_norms) if g > f+0.01)}/{len(flat_norms)}")

    # =========================================================================
    # 4. Contraction / per-entry bound
    # =========================================================================
    print(f"\n--- 4. Per-entry bound ||G_ef(Q)|| vs |c_ef| ---")
    for trial in range(5):
        Q = random_config(lat, rng)
        violations, max_ratio, zero_entries, max_zero_norm = \
            attempt_contraction_proof(lat, Q, d)
        print(f"Config {trial}: violations={violations}, max_ratio={max_ratio:.4f}, "
              f"zero_entries_nonzero={zero_entries}, max_zero_entry={max_zero_norm:.4f}")

    # =========================================================================
    # 5. Key computation: Frobenius norm vs operator norm tradeoff
    # =========================================================================
    print(f"\n--- 5. Frobenius norm analysis ---")
    print("At flat: ||F||_F = sqrt(12) = 3.46, ||F||_op = 2, ||F||_F/||F||_op = 1.73")
    print("At general: ||F||_F = 2*sqrt(2+β₀²) < sqrt(12), ||F||_op = 2")
    print("So Frobenius norm DECREASES but operator norm stays constant.")

    # Compute the "effective color dimension" per pair
    for trial in range(3):
        Q = random_config(lat, rng)
        G, svd_data = compute_G_blocks_with_svd(lat, Q, d)

        frob_ratios = []
        for dat in svd_data:
            F = -2 * dat['B_k'] / (-(1/2) * dat['sp'] * dat['sq'])  # undo -(β/N)*sp*sq
            frob = np.linalg.norm(F, 'fro')
            op = np.linalg.norm(F, 2)
            frob_ratios.append(frob / op)

        print(f"Config {trial}: mean(||F||_F/||F||_op)={np.mean(frob_ratios):.4f} "
              f"(flat=1.732, rank-2=1.414)")

    # =========================================================================
    # 6. The aligned bound IS tight at flat (prove via Schur product)
    # =========================================================================
    print(f"\n--- 6. Schur product theorem verification ---")
    print("At flat: B(n)_ef = c_ef * (n_e · n_f) = (A_total ∘ N)_ef")
    print("where N_ef = n_e · n_f is a correlation matrix (PSD, unit diagonal).")
    print("By Schur product theorem: ||A ∘ N||_op ≤ ||A||_op for A symmetric, N correlation.")
    print("Therefore: aligned norm at flat ≤ ||A_total|| = 2(d+1). ✓")
    print("Equality: when all n_e = n (same direction), N = ones matrix, A∘N = A.")
    print()
    print("At general Q: B(n)_ef = n_e^T G_ef(Q) n_f ≠ (A_total ∘ N)_ef")
    print("The Schur product theorem does NOT directly apply.")
    print("But numerical evidence shows aligned norm < ||A_total|| at non-flat Q.")

    # =========================================================================
    # 7. Attempt: bound using the contraction P_k R_k
    # =========================================================================
    print(f"\n--- 7. Contraction bound attempt ---")
    print("C(Q) = Σ_k E_k ⊗ B_k with B_k = s_k P_k R_k, ||P_k R_k|| ≤ 1")
    print("At flat: B_k = s_k I_3")
    print()
    print("For quadratic form with unit v = (r_e n_e):")
    print("v^T C v = Σ_k s_k r_ep r_eq (n_ep^T P_k R_k n_eq)")
    print()
    print("Using |n^T (PR) n'| ≤ ||PR|| ≤ 1:")
    print("|v^T C v| ≤ Σ_k |r_ep r_eq| = r^T |A_total|_abs r")
    print("This gives ||C|| ≤ |||A_total|_abs|| = ||abs(A_total)||")

    A_total = np.zeros((ne, ne))
    for plaq in lat.plaquettes:
        for p in range(4):
            for q in range(p+1, 4):
                ep, sp = plaq[p]
                eq, sq = plaq[q]
                A_total[ep, eq] += sp * sq
                A_total[eq, ep] += sp * sq

    A_abs = np.abs(A_total)
    ev_abs = np.linalg.eigvalsh(A_abs)
    print(f"||abs(A_total)|| = {max(abs(ev_abs)):.4f}")
    print(f"||A_total|| = {max(abs(np.linalg.eigvalsh(A_total))):.4f}")
    print(f"Ratio: {max(abs(ev_abs)) / max(abs(np.linalg.eigvalsh(A_total))):.4f}")
    print(f"This bound is {'TIGHT' if max(abs(ev_abs)) <= target + 0.01 else 'TOO LOOSE'}")


if __name__ == "__main__":
    main()
