"""
FOCUSED decoherence proof attempt.

Strategy: extract G blocks directly from verified Hessian, then analyze.

Key results to establish:
1. F = -2(β₀I + [β⃗×])R with SVs (2, 2, 2|β₀|) — VERIFIED
2. Per-plaquette decoherence: ||C_□(Q)|| ≤ ||C_□(flat)|| = 3 — TEST
3. Flat is global max of ||C|| — gradient ascent
4. Aligned-color Schur bound — prove
5. Misalignment factor bound — investigate
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hessian_core import (
    Lattice, random_su2, su2_inv, flat_config, random_config,
    isigma, get_link, compute_hessian_decomposed, su2_to_quat,
    adjoint_so3, cross_product_matrix
)

def su2_exp(w_vec):
    theta = np.linalg.norm(w_vec)
    if theta < 1e-14:
        return np.eye(2, dtype=complex)
    W = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta) / theta) * W

def project_su2(M):
    U, s, Vh = np.linalg.svd(M)
    P = U @ Vh
    if np.real(np.linalg.det(P)) < 0:
        P = -P
    P /= np.sqrt(np.linalg.det(P))
    return P

def extract_G_blocks(C, ne):
    """Extract 3x3 blocks G[e,f] from the full C matrix."""
    G = np.zeros((ne, ne, 3, 3))
    for e in range(ne):
        for f in range(ne):
            G[e, f] = C[3*e:3*e+3, 3*f:3*f+3]
    return G

def aligned_norm(G, ne, n_samples=500):
    """Max over unit n of ||B(n)|| where B_ef = n^T G_ef n."""
    rng = np.random.default_rng(42)
    max_norm = 0
    for _ in range(n_samples):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        B = np.zeros((ne, ne))
        for e in range(ne):
            for f in range(ne):
                B[e, f] = n @ G[e, f] @ n
        ev = np.linalg.eigvalsh(B)
        max_norm = max(max_norm, max(abs(ev[0]), abs(ev[-1])))
    return max_norm

def per_plaquette_cross_term(lat, Q):
    """Compute per-plaquette cross-term 12x12 matrix and its norm."""
    norms = []
    for pidx, plaq in enumerate(lat.plaquettes):
        edges_list = plaq
        C_plaq = np.zeros((12, 12))
        for p_idx in range(4):
            for q_idx in range(p_idx + 1, 4):
                ep_slot, sp = p_idx, edges_list[p_idx][1]
                eq_slot, sq = q_idx, edges_list[q_idx][1]

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
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R_mat))
                        C_plaq[3*ep_slot+a, 3*eq_slot+b] += val
                        C_plaq[3*eq_slot+b, 3*ep_slot+a] += val

        ev = np.linalg.eigvalsh(C_plaq)
        norms.append(max(abs(ev[0]), abs(ev[-1])))
    return norms

def per_plaquette_proof(lat, n_configs=200):
    """Test if ||C_□(Q)|| ≤ ||C_□(flat)|| for all Q and all □."""
    rng = np.random.default_rng(42)

    # Flat norms
    Q_flat = flat_config(lat)
    flat_norms = per_plaquette_cross_term(lat, Q_flat)
    flat_max = max(flat_norms)
    print(f"Flat per-plaquette: max={flat_max:.6f}, all={flat_norms[0]:.6f} (all same)")

    # Random configs
    violations = 0
    max_gen = 0
    for trial in range(n_configs):
        Q = random_config(lat, rng)
        gen_norms = per_plaquette_cross_term(lat, Q)
        max_gen = max(max_gen, max(gen_norms))
        for i, (g, f) in enumerate(zip(gen_norms, flat_norms)):
            if g > f + 1e-10:
                violations += 1

    print(f"Over {n_configs} configs: max per-plaq norm = {max_gen:.6f}")
    print(f"Violations (gen > flat): {violations}/{n_configs * lat.nplaq}")
    return violations == 0

def prove_per_plaquette_decoherence():
    """
    PROVE: For a single plaquette with 4 edges and signs (+1,+1,-1,-1),
    the cross-term 12×12 matrix has ||C_□(Q)|| ≤ ||C_□(flat)|| = 3.

    This is the 12×12 matrix with block structure:
    C_□ = Σ_{p<q} s_p s_q E_{pq}^sym ⊗ (-(1/2) F^{pq})

    At flat: F^{pq} = -2I for all pairs, so:
    C_□^flat = Σ_{p<q} s_p s_q E_{pq}^sym ⊗ I = (ss^T - I_4) ⊗ I_3

    Eigenvalues of ss^T - I_4 = {3, -1, -1, -1} (since s = [1,1,-1,-1])
    So ||C_□^flat|| = 3.

    For general Q: each F^{pq} has ||F^{pq}|| = 2 and SVs (2, 2, 2|β₀|).
    The contribution -(1/2)F = P_k R_k is a contraction with ||·|| ≤ 1.

    Can we show ||C_□(Q)|| ≤ 3?
    """
    print("\n=== PER-PLAQUETTE DECOHERENCE PROOF ATTEMPT ===")

    # The 12×12 matrix for a single plaquette with 4 SU(2) links
    rng = np.random.default_rng(42)

    max_norm = 0
    for trial in range(10000):
        # Random 4 SU(2) links for the plaquette
        Q = [random_su2(rng) for _ in range(4)]
        signs = [+1, +1, -1, -1]

        C_plaq = np.zeros((12, 12))
        for p in range(4):
            for q in range(p+1, 4):
                sp, sq = signs[p], signs[q]

                # Compute L, mid, R for this pair
                L = np.eye(2, dtype=complex)
                for k in range(p+1):
                    if signs[k] == +1:
                        L = L @ Q[k]
                    else:
                        L = L @ su2_inv(Q[k])

                mid = np.eye(2, dtype=complex)
                for k in range(p+1, q):
                    if signs[k] == +1:
                        mid = mid @ Q[k]
                    else:
                        mid = mid @ su2_inv(Q[k])

                R = np.eye(2, dtype=complex)
                for k in range(q+1, 4):
                    if signs[k] == +1:
                        R = R @ Q[k]
                    else:
                        R = R @ su2_inv(Q[k])

                for a in range(3):
                    for b in range(3):
                        val = -0.5 * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R))
                        C_plaq[3*p+a, 3*q+b] += val
                        C_plaq[3*q+b, 3*p+a] += val

        ev = np.linalg.eigvalsh(C_plaq)
        norm = max(abs(ev[0]), abs(ev[-1]))
        max_norm = max(max_norm, norm)

    print(f"Over 10000 random 4-link configs: max ||C_□|| = {max_norm:.6f}")
    print(f"Flat value: 3.000000")
    print(f"Per-plaquette decoherence holds: {max_norm <= 3.0 + 1e-6}")

    # Also try gradient ascent on single plaquette
    print("\nGradient ascent on single plaquette ||C_□||:")
    for start in range(10):
        Q = [random_su2(rng) for _ in range(4)]
        signs = [+1, +1, -1, -1]

        for _ in range(500):
            Q_best = [q.copy() for q in Q]
            norm_best = 0

            # Compute current norm
            C_plaq = np.zeros((12, 12))
            for p in range(4):
                for q in range(p+1, 4):
                    sp, sq = signs[p], signs[q]
                    L = np.eye(2, dtype=complex)
                    for k in range(p+1):
                        L = L @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                    mid = np.eye(2, dtype=complex)
                    for k in range(p+1, q):
                        mid = mid @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                    R = np.eye(2, dtype=complex)
                    for k in range(q+1, 4):
                        R = R @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                    for a in range(3):
                        for b in range(3):
                            val = -0.5 * sp * sq * np.real(
                                np.trace(L @ isigma[a] @ mid @ isigma[b] @ R))
                            C_plaq[3*p+a, 3*q+b] += val
                            C_plaq[3*q+b, 3*p+a] += val

            ev = np.linalg.eigvalsh(C_plaq)
            norm_curr = max(abs(ev[0]), abs(ev[-1]))

            # Random perturbation
            e_pert = rng.integers(4)
            w = 0.03 * rng.normal(size=3)
            Q_trial = [q.copy() for q in Q]
            Q_trial[e_pert] = su2_exp(w) @ Q[e_pert]
            Q_trial[e_pert] = project_su2(Q_trial[e_pert])

            C_trial = np.zeros((12, 12))
            for p in range(4):
                for q in range(p+1, 4):
                    sp, sq = signs[p], signs[q]
                    L = np.eye(2, dtype=complex)
                    for k in range(p+1):
                        L = L @ (Q_trial[k] if signs[k] == +1 else su2_inv(Q_trial[k]))
                    mid = np.eye(2, dtype=complex)
                    for k in range(p+1, q):
                        mid = mid @ (Q_trial[k] if signs[k] == +1 else su2_inv(Q_trial[k]))
                    R = np.eye(2, dtype=complex)
                    for k in range(q+1, 4):
                        R = R @ (Q_trial[k] if signs[k] == +1 else su2_inv(Q_trial[k]))
                    for a in range(3):
                        for b in range(3):
                            val = -0.5 * sp * sq * np.real(
                                np.trace(L @ isigma[a] @ mid @ isigma[b] @ R))
                            C_trial[3*p+a, 3*q+b] += val
                            C_trial[3*q+b, 3*p+a] += val

            ev_trial = np.linalg.eigvalsh(C_trial)
            norm_trial = max(abs(ev_trial[0]), abs(ev_trial[-1]))
            if norm_trial > norm_curr:
                Q = Q_trial

        # Final norm
        C_plaq = np.zeros((12, 12))
        for p in range(4):
            for q in range(p+1, 4):
                sp, sq = signs[p], signs[q]
                L = np.eye(2, dtype=complex)
                for k in range(p+1):
                    L = L @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                mid = np.eye(2, dtype=complex)
                for k in range(p+1, q):
                    mid = mid @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                R = np.eye(2, dtype=complex)
                for k in range(q+1, 4):
                    R = R @ (Q[k] if signs[k] == +1 else su2_inv(Q[k]))
                for a in range(3):
                    for b in range(3):
                        val = -0.5 * sp * sq * np.real(
                            np.trace(L @ isigma[a] @ mid @ isigma[b] @ R))
                        C_plaq[3*p+a, 3*q+b] += val
                        C_plaq[3*q+b, 3*p+a] += val
        ev = np.linalg.eigvalsh(C_plaq)
        final_norm = max(abs(ev[0]), abs(ev[-1]))
        print(f"  Start {start}: final ||C_□|| = {final_norm:.6f}")

def main():
    d = 4
    L = 2
    lat = Lattice(d, L)
    ne = lat.nedges
    target = 2 * (d + 1)

    print(f"{'='*70}")
    print(f"DECOHERENCE LEMMA PROOF — d={d}, L={L}, target={target}")
    print(f"{'='*70}")

    # =====================================================================
    # 1. Per-plaquette decoherence
    # =====================================================================
    print("\n--- 1. Per-plaquette decoherence on full lattice ---")
    per_plaq_ok = per_plaquette_proof(lat, n_configs=200)
    if per_plaq_ok:
        print("RESULT: Per-plaquette decoherence HOLDS for all tested configs!")

    # =====================================================================
    # 2. Per-plaquette proof (isolated plaquette)
    # =====================================================================
    prove_per_plaquette_decoherence()

    # =====================================================================
    # 3. Full lattice: aligned color norm
    # =====================================================================
    print(f"\n{'='*70}")
    print("ALIGNED COLOR NORM ANALYSIS")
    print(f"{'='*70}")

    rng = np.random.default_rng(42)
    Q_flat = flat_config(lat)
    D_flat, C_flat = compute_hessian_decomposed(lat, Q_flat)
    G_flat = extract_G_blocks(C_flat, ne)
    an_flat = aligned_norm(G_flat, ne)
    print(f"Flat aligned norm: {an_flat:.4f} (expected: {target})")

    max_an = 0
    max_fn = 0
    for trial in range(100):
        Q = random_config(lat, rng)
        D, C = compute_hessian_decomposed(lat, Q)
        G = extract_G_blocks(C, ne)

        ev = np.linalg.eigvalsh(C)
        fn = max(abs(ev[0]), abs(ev[-1]))
        an = aligned_norm(G, ne, n_samples=200)

        max_fn = max(max_fn, fn)
        max_an = max(max_an, an)

    print(f"\n100 random configs:")
    print(f"  Max full norm: {max_fn:.4f}")
    print(f"  Max aligned norm: {max_an:.4f}")
    print(f"  Target: {target}")
    print(f"  Full norm ≤ target: {max_fn <= target + 0.01}")
    print(f"  Aligned ≤ target: {max_an <= target + 0.01}")

    # =====================================================================
    # 4. Full norm vs aligned norm correlation
    # =====================================================================
    print(f"\n{'='*70}")
    print("FULL vs ALIGNED NORM: CORRELATION")
    print(f"{'='*70}")

    aligned_list = []
    full_list = []
    for trial in range(50):
        Q = random_config(lat, rng)
        D, C = compute_hessian_decomposed(lat, Q)
        G = extract_G_blocks(C, ne)

        ev = np.linalg.eigvalsh(C)
        fn = max(abs(ev[0]), abs(ev[-1]))
        an = aligned_norm(G, ne, n_samples=100)

        aligned_list.append(an)
        full_list.append(fn)

    aligned_arr = np.array(aligned_list)
    full_arr = np.array(full_list)
    ratios = full_arr / aligned_arr

    print(f"Aligned norms: min={aligned_arr.min():.3f}, max={aligned_arr.max():.3f}, "
          f"mean={aligned_arr.mean():.3f}")
    print(f"Full norms:    min={full_arr.min():.3f}, max={full_arr.max():.3f}, "
          f"mean={full_arr.mean():.3f}")
    print(f"Ratios full/aligned: min={ratios.min():.3f}, max={ratios.max():.3f}, "
          f"mean={ratios.mean():.3f}")
    print(f"\nKey bound: full ≤ aligned × ratio_max = {aligned_arr.max():.3f} × "
          f"{ratios.max():.3f} = {aligned_arr.max() * ratios.max():.3f}")
    print(f"Alternative: max(full) = {full_arr.max():.3f} vs target = {target}")

    # =====================================================================
    # 5. Near-flat analysis
    # =====================================================================
    print(f"\n{'='*70}")
    print("NEAR-FLAT ANALYSIS: how ||C|| depends on perturbation size")
    print(f"{'='*70}")

    for eps in [0.01, 0.03, 0.1, 0.3, 0.5, 1.0, 2.0, 3.0]:
        norms = []
        for trial in range(50):
            Q = [su2_exp(eps * rng.normal(size=3)) for _ in range(ne)]
            D, C = compute_hessian_decomposed(lat, Q)
            ev = np.linalg.eigvalsh(C)
            norms.append(max(abs(ev[0]), abs(ev[-1])))
        print(f"eps={eps:.2f}: mean||C||={np.mean(norms):.4f}, "
              f"max={max(norms):.4f}, min={min(norms):.4f}")

if __name__ == "__main__":
    main()
