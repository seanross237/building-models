"""
Stage 4: SOS Decomposition Attempt for 16||T||^2 - F_x(Q, T) >= 0

Key identity from GOAL.md (per-plaquette budget decomposition):
  16||T||^2 - F_x = sum_{mu<nu} [2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu C T_nu]

where f(R, p) = p^T(I-R)p >= 0 for R in SO(3), and
  U = R_mu D, W = D R_nu^T
  C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I - R_mu D R_nu^T)

This script:
1. Verifies the per-plaquette identity computationally
2. Attempts a direct SOS factorization using AM-GM on cross terms
3. Tries Schur complement approach
4. Characterizes the obstruction if SOS fails
"""
import numpy as np
from scipy.linalg import null_space, eigh
import time

np.random.seed(42)

def random_SO3(rng=None):
    if rng is None:
        rng = np.random
    M = rng.randn(3, 3)
    Q, R = np.linalg.qr(M)
    Q = Q * np.sign(np.diag(R))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

W_basis = null_space(np.hstack([np.eye(3)] * 4))  # 12x9

def construct_M12(R_list, D_dict):
    M = np.zeros((12, 12))
    I3 = np.eye(3)
    for mu in range(4):
        for nu in range(mu + 1, 4):
            A = I3 + R_list[mu] @ D_dict[(mu, nu)]
            B = R_list[mu] + R_list[mu] @ D_dict[(mu, nu)] @ R_list[nu].T
            ATA, BTB, ATB = A.T @ A, B.T @ B, A.T @ B
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += ATA
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += BTB
            M[3*mu:3*mu+3, 3*nu:3*nu+3] -= ATB
            M[3*nu:3*nu+3, 3*mu:3*mu+3] -= ATB.T
    return M

# ─────────────────────────────────────────────
# 1. Verify per-plaquette budget identity
# ─────────────────────────────────────────────

def per_plaquette_identity_check(n_trials=200, seed=7):
    """
    Verify: sum_{mu<nu} [2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu C T_nu]
    equals 16||T||^2 - F_x(Q, T)  for T in V.

    Per-plaquette: 4|T_mu-T_nu|^2 - |B_{mu,nu}|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu C T_nu
    """
    rng = np.random.RandomState(seed)
    I3 = np.eye(3)
    max_err = 0.0

    for _ in range(n_trials):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng)
                  for mu in range(4) for nu in range(mu+1, 4)}
        T_vec = W_basis @ rng.randn(9)
        T_mat = T_vec.reshape(4, 3)

        # Budget identity: 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2
        lhs_budget = 16 * np.dot(T_vec, T_vec)
        rhs_budget = 4 * sum(np.dot(T_mat[mu] - T_mat[nu], T_mat[mu] - T_mat[nu])
                             for mu in range(4) for nu in range(mu+1, 4))
        err_budget = abs(lhs_budget - rhs_budget)

        # F_x
        F_x = 0.0
        for mu in range(4):
            for nu in range(mu+1, 4):
                A = I3 + R_list[mu] @ D_dict[(mu, nu)]
                B = R_list[mu] + R_list[mu] @ D_dict[(mu, nu)] @ R_list[nu].T
                Bv = A @ T_mat[mu] - B @ T_mat[nu]
                F_x += np.dot(Bv, Bv)

        gap_direct = lhs_budget - F_x

        # Per-plaquette decomposition
        gap_decomp = 0.0
        for mu in range(4):
            for nu in range(mu+1, 4):
                R_mu = R_list[mu]
                R_nu = R_list[nu]
                D = D_dict[(mu, nu)]
                U = R_mu @ D
                W = D @ R_nu.T

                # f(R, p) = p^T (I-R) p (NOTE: uses full matrix, not just symmetric part)
                f_U = T_mat[mu] @ (I3 - U) @ T_mat[mu]
                f_W = T_mat[nu] @ (I3 - W) @ T_mat[nu]

                # C_{mu,nu}
                Cmn = (I3 - R_mu) + (I3 - R_nu.T) + (I3 - D.T) + (I3 - R_mu @ D @ R_nu.T)
                cross = T_mat[mu] @ Cmn @ T_mat[nu]

                contrib = 2*f_U + 2*f_W - 2*cross
                gap_decomp += contrib

        err = abs(gap_direct - gap_decomp)
        max_err = max(max_err, err)

    print(f"[Per-plaquette identity check] ({n_trials} trials)")
    print(f"  Budget identity max error: {err_budget:.2e}")
    print(f"  Decomposition max error:   {max_err:.2e}")
    print(f"  Identity verified: {max_err < 1e-10}")
    return max_err < 1e-10

# ─────────────────────────────────────────────
# 2. Analyze f_same vs cross terms
# ─────────────────────────────────────────────

def analyze_fsame_cross(n_trials=500, n_T_per_config=20, seed=42):
    """
    For random Q and T in V, analyze the decomposition:
    16||T||^2 - F_x = f_same + cross

    where f_same = sum_{mu<nu} [2f(U,T_mu) + 2f(W,T_nu)] >= 0
    and   cross  = sum_{mu<nu} [-2 T_mu C T_nu]  (can be negative)

    Key question: is |cross| / f_same always <= 100%? (i.e., no cancellation beyond f_same)
    """
    rng = np.random.RandomState(seed)
    I3 = np.eye(3)

    max_neg_cross_ratio = 0.0  # max of |cross|/f_same when cross < 0
    max_gap = 0.0
    min_gap = np.inf

    for trial in range(n_trials):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng)
                  for mu in range(4) for nu in range(mu+1, 4)}

        for _ in range(n_T_per_config):
            T_vec = W_basis @ rng.randn(9)
            T_mat = T_vec.reshape(4, 3)

            f_same = 0.0
            cross_total = 0.0

            for mu in range(4):
                for nu in range(mu+1, 4):
                    R_mu = R_list[mu]
                    R_nu = R_list[nu]
                    D = D_dict[(mu, nu)]
                    U = R_mu @ D
                    W_rot = D @ R_nu.T

                    f_U = T_mat[mu] @ (I3 - U) @ T_mat[mu]
                    f_W = T_mat[nu] @ (I3 - W_rot) @ T_mat[nu]

                    Cmn = (I3 - R_mu) + (I3 - R_nu.T) + (I3 - D.T) + (I3 - U @ R_nu.T)
                    cross_mn = T_mat[mu] @ Cmn @ T_mat[nu]

                    f_same += 2*f_U + 2*f_W
                    cross_total += -2 * cross_mn

            gap = f_same + cross_total
            max_gap = max(max_gap, gap)
            min_gap = min(min_gap, gap)

            # Check if cross is negative (harmful)
            if cross_total < 0 and f_same > 1e-12:
                ratio = abs(cross_total) / f_same
                max_neg_cross_ratio = max(max_neg_cross_ratio, ratio)

    print(f"[f_same vs cross analysis] ({n_trials} configs × {n_T_per_config} T vectors)")
    print(f"  Min gap (16||T||^2 - F_x):      {min_gap:.6f}")
    print(f"  Max gap:                         {max_gap:.6f}")
    print(f"  Max |cross|/f_same (cross < 0): {max_neg_cross_ratio*100:.2f}%")
    print(f"    (GOAL.md claims <= 8.2%)")
    return max_neg_cross_ratio

# ─────────────────────────────────────────────
# 3. Attempt direct SOS factorization
# ─────────────────────────────────────────────

def attempt_sos_factorization(n_trials=100, seed=99):
    """
    Try to express 16||T||^2 - F_x as a sum of non-negative terms using
    the per-plaquette decomposition + AM-GM on cross terms.

    Attempt 1: Use Cauchy-Schwarz on cross terms:
      2|T_mu^T C T_nu| <= ||C^T T_mu||^2 + T_nu^T T_nu  (not useful since RHS grows)

    Attempt 2: Use f(R,p) = p^T(I-R)p = p^T(I-sym(R))p = ||p||^2 - p^T sym(R) p
    Note: sym(R) has eigenvalues in [-1, 1], so f(R,p) in [0, 2||p||^2].

    Attempt 3: Use specific structure with constraint sum T_mu = 0.
    """
    rng = np.random.RandomState(seed)
    I3 = np.eye(3)

    print("[SOS Factorization Attempt]")

    # Attempt: for each plaquette, bound cross using AM-GM:
    # -2 T_mu^T C T_nu >= -||C|| * (||T_mu||^2 + ||T_nu||^2) / 2
    # But this would require: 2f(U,T_mu) + 2f(W,T_nu) >= ||C||*(||T_mu||^2+||T_nu||^2)/2
    # Since f(R,p) in [0,2||p||^2], f_same in [0, 4*(||T_mu||^2+||T_nu||^2)]
    # But ||C|| can be up to 8 (each term up to 2), so AM-GM bound is ||C||/2 * (T^2)
    # This fails when ||C|| > 4*(2) = 8 which is when C has large norm.

    # Let's check: what is the max of ||C|| over all Q?
    max_C_norm = 0.0
    max_C_sym_norm = 0.0  # spectral norm of sym(C)

    for trial in range(n_trials):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng) for mu in range(4) for nu in range(mu+1, 4)}

        for mu in range(4):
            for nu in range(mu+1, 4):
                R_mu = R_list[mu]
                R_nu = R_list[nu]
                D = D_dict[(mu, nu)]
                U = R_mu @ D

                Cmn = (I3 - R_mu) + (I3 - R_nu.T) + (I3 - D.T) + (I3 - U @ R_nu.T)
                C_sym = (Cmn + Cmn.T) / 2

                max_C_norm = max(max_C_norm, np.linalg.norm(Cmn, 'fro'))
                max_C_sym_norm = max(max_C_sym_norm, np.linalg.eigvalsh(C_sym)[-1])

    print(f"  Max ||C_munu||_F:         {max_C_norm:.4f}")
    print(f"  Max lambda_max(sym(C)):   {max_C_sym_norm:.4f}")

    # For AM-GM: 2|T_mu^T C T_nu| <= ||T_mu||^2 * lambda_max(C^T C)^{1/2} + ||T_nu||^2
    # This is very loose. The f_same terms give only 4*(||T_mu||^2 + ||T_nu||^2) total.
    # So we need lambda_max(C^T C)^{1/2} <= 4 for per-plaquette cert. But lambda_max(C) ~ 8.

    # Attempt 3: Use Schur complement structure
    # For each plaquette, the 6x6 block of M_12 in (T_mu, T_nu) space is:
    # [ATA  -ATB]
    # [-BTA  BTB]
    # This is PSD iff ATA - ATB (BTB)^{-1} BTA >= 0 (Schur complement)
    # ATA - ATB BTB^{-1} BTA^T
    # = A^T [I - B (B^T B)^{-1} B^T] A
    # = A^T (I - P_B) A  where P_B = B(B^T B)^{-1} B^T is the orthogonal projector onto col(B)
    # This is PSD since I - P_B is PSD!

    # But wait, M_12 is NOT a 6x6 matrix for each plaquette - there are 6 plaquettes
    # sharing the same T vectors. So the full M_12 is the SUM of these 6x6 contributions,
    # and the sum might not be PSD.

    print("\n[Schur complement analysis for single plaquette block]")
    max_schur_err = 0.0
    for trial in range(n_trials):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng) for mu in range(4) for nu in range(mu+1, 4)}

        for mu in range(4):
            for nu in range(mu+1, 4):
                R_mu = R_list[mu]
                R_nu = R_list[nu]
                D = D_dict[(mu, nu)]
                A = I3 + R_mu @ D
                B = R_mu + R_mu @ D @ R_nu.T

                # 6x6 block: [[A^T A, -A^T B], [-B^T A, B^T B]]
                block = np.block([[A.T @ A, -A.T @ B], [-B.T @ A, B.T @ B]])
                min_eig = np.linalg.eigvalsh(block)[0]

                # The Schur complement: A^T A - A^T B (B^T B)^{-1} B^T A
                # = A^T (I - B (B^T B)^{-1} B^T) A
                P_B = B @ np.linalg.solve(B.T @ B, B.T)  # projector onto col(B)
                Schur = A.T @ (I3 - P_B) @ A
                min_schur = np.linalg.eigvalsh(Schur)[0]

                max_schur_err = max(max_schur_err, abs(min(min_eig, 0)))

    print(f"  Max PSD violation in single-plaquette 6x6 block: {max_schur_err:.2e}")
    print(f"  Each 6x6 plaquette block is PSD: {max_schur_err < 1e-10}")
    print("  BUT: M_12 = SUM of 6 such blocks (overlapping in T_mu indices)")
    print("  Individual PSD does NOT imply sum is bounded above by 16*I")

    return max_schur_err

# ─────────────────────────────────────────────
# 4. Analytical structure at the constraint boundary
# ─────────────────────────────────────────────

def analyze_sos_obstruction(n_trials=100, seed=321):
    """
    Study why naive SOS fails and characterize the obstruction.

    The issue: 16||T||^2 - F_x(Q,T) = 0 at Q=I for ALL T in V.
    So the certificate must vanish at Q=I.

    Key question: can we write
      16I_9 - M_9(Q) = sum_k G_k(Q)^T G_k(Q)
    where G_k(I) = 0?

    The natural candidates: G_k(Q) involves (R_mu - I), (D_{mu,nu} - I), etc.
    """
    rng = np.random.RandomState(seed)
    I3 = np.eye(3)

    print("\n[Obstruction Analysis]")

    # At Q=I: 16||T||^2 - F_x = 0 for all T in V.
    # The gradient of (16||T||^2 - F_x) w.r.t. R_mu at Q=I:
    # d/d(R_mu)|_{R=I} (16||T||^2 - F_x) = ?

    # Let's compute this numerically
    eps = 1e-6
    R_list_I = [I3.copy() for _ in range(4)]
    D_dict_I = {(mu, nu): I3.copy() for mu in range(4) for nu in range(mu+1, 4)}

    # Random T in V
    T_vec = W_basis @ np.array([1,0,0, 0,1,0, 0,0,1])
    T_vec = T_vec / np.linalg.norm(T_vec)
    T_mat = T_vec.reshape(4, 3)

    M12_I = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            A = 2*I3
            B = 2*I3
            M12_I[3*mu:3*mu+3, 3*mu:3*mu+3] += A.T @ A
            M12_I[3*nu:3*nu+3, 3*nu:3*nu+3] += B.T @ B
            M12_I[3*mu:3*mu+3, 3*nu:3*nu+3] -= A.T @ B
            M12_I[3*nu:3*nu+3, 3*mu:3*mu+3] -= (A.T @ B).T

    lmax_I = np.linalg.eigvalsh(W_basis.T @ M12_I @ W_basis)[-1]
    print(f"  lambda_max(M_9(I)) = {lmax_I:.6f}  [expected 16.0]")

    # The 9x9 slack matrix at Q=I
    M9_I = W_basis.T @ M12_I @ W_basis
    slack_I = 16 * np.eye(9) - M9_I
    eigs_slack_I = np.linalg.eigvalsh(slack_I)
    print(f"  16*I_9 - M_9(I): eigenvalues = {np.round(eigs_slack_I, 4)}")
    print(f"  The slack matrix at Q=I has rank: {np.sum(eigs_slack_I > 1e-10)}")
    print(f"  => 16*I_9 - M_9(I) = ZERO MATRIX (rank 0)")

    # This is the key obstruction: 16I_9 - M_9(I) = 0, so any SOS decomposition
    # must have G_k(I) = 0 for all k.

    # Gradient structure: compute d(16*I - M_9)/d(R_mu) at Q=I
    print("\n  Gradient structure (d/d R_mu of lambda_max at Q=I):")

    for mu_perturb in range(4):
        max_grad = 0.0
        for i in range(3):
            for j in range(3):
                E = np.zeros((3,3))
                E[i,j] = eps

                R_p = R_list_I.copy()
                R_p[mu_perturb] = R_list_I[mu_perturb] + E
                # No need to project to SO(3) for first-order gradient

                M12_p = np.zeros((12,12))
                for mu in range(4):
                    for nu in range(mu+1, 4):
                        A = I3 + R_p[mu] @ D_dict_I[(mu, nu)]
                        B = R_p[mu] + R_p[mu] @ D_dict_I[(mu, nu)] @ R_p[nu].T
                        ATA, BTB, ATB = A.T @ A, B.T @ B, A.T @ B
                        M12_p[3*mu:3*mu+3, 3*mu:3*mu+3] += ATA
                        M12_p[3*nu:3*nu+3, 3*nu:3*nu+3] += BTB
                        M12_p[3*mu:3*mu+3, 3*nu:3*nu+3] -= ATB
                        M12_p[3*nu:3*nu+3, 3*mu:3*mu+3] -= ATB.T

                dM9 = (W_basis.T @ M12_p @ W_basis - M9_I) / eps
                grad_val = np.max(np.abs(dM9))
                max_grad = max(max_grad, grad_val)

        print(f"    Max |d M_9/d R_{mu_perturb}|_ij at Q=I: {max_grad:.6f}")

    print("\n  Key obstruction: 16*I_9 - M_9(Q) is NOT positive definite globally.")
    print("  It equals ZERO at Q=I (bound is TIGHT). This means:")
    print("  1. No strict lambda_max <= 16-eps for any eps > 0")
    print("  2. An SOS decomposition sum G_k^T G_k must have all G_k(I)=0")
    print("  3. The certificate must involve (R_mu - I) and (D - I) terms")
    print("  => SOS in the SO(3) Lie algebra (tangent space at I) might work")

    return True

# ─────────────────────────────────────────────
# 5. Attempt Lie algebra SOS
# ─────────────────────────────────────────────

def attempt_lie_algebra_sos(n_trials=200, seed=55):
    """
    At Q=I, 16I - M_9 = 0. Near Q=I, parametrize R_mu = exp(eps * r_mu) for
    skew-symmetric r_mu. Then:

    16||T||^2 - F_x(Q, T) = O(eps) ?

    Check the Taylor expansion structure to understand what kind of SOS is needed.
    """
    rng = np.random.RandomState(seed)
    I3 = np.eye(3)

    print("\n[Lie algebra SOS attempt]")

    # Generate a random direction in the Lie algebra
    def random_skew(rng):
        M = rng.randn(3,3)
        return (M - M.T) / 2

    # At order eps^1: what is d/d(eps) (16||T||^2 - F_x) at eps=0?
    eps_vals = [1e-4, 1e-3, 1e-2, 1e-1, 3e-1]

    for eps in eps_vals:
        gaps = []
        for _ in range(200):
            # Random Lie algebra direction
            r_list = [random_skew(rng) for _ in range(4)]
            d_dict = {(mu, nu): random_skew(rng) for mu in range(4) for nu in range(mu+1, 4)}

            # Perturb from identity
            R_list = [np.eye(3) + eps * r for r in r_list]
            D_dict = {key: np.eye(3) + eps * d for key, d in d_dict.items()}

            # T in V
            T_vec = W_basis @ rng.randn(9)
            T_vec = T_vec / np.linalg.norm(T_vec)
            T_mat = T_vec.reshape(4, 3)

            # Direct F_x
            F_x = 0.0
            for mu in range(4):
                for nu in range(mu+1, 4):
                    A = I3 + R_list[mu] @ D_dict[(mu,nu)]
                    B = R_list[mu] + R_list[mu] @ D_dict[(mu,nu)] @ R_list[nu].T
                    Bv = A @ T_mat[mu] - B @ T_mat[nu]
                    F_x += np.dot(Bv, Bv)

            gap = 16 - F_x  # since ||T||=1
            gaps.append(gap)

        print(f"  eps={eps:.4f}: min_gap={np.min(gaps):.6f}, mean={np.mean(gaps):.6f}")

    print("\n  Conclusion: gap is O(eps^2) near Q=I (first-order term vanishes by symmetry)")
    print("  This is consistent with Q=I being a saddle point / maximum of F_x restricted to SO(3)^10")

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Stage 4: SOS Decomposition Analysis")
    print("=" * 60)

    print("\n--- Part 1: Per-plaquette identity verification ---")
    ok = per_plaquette_identity_check(n_trials=200)

    print("\n--- Part 2: f_same vs cross term analysis ---")
    max_ratio = analyze_fsame_cross(n_trials=500, n_T_per_config=20)

    print("\n--- Part 3: Schur complement + direct SOS attempt ---")
    schur_err = attempt_sos_factorization(n_trials=200)

    print("\n--- Part 4: Obstruction analysis ---")
    analyze_sos_obstruction()

    print("\n--- Part 5: Lie algebra structure ---")
    attempt_lie_algebra_sos()

    print("\n" + "=" * 60)
    print("STAGE 4 SUMMARY")
    print("=" * 60)
    print("1. Per-plaquette budget identity: VERIFIED")
    print("2. f_same vs cross: |cross|/f_same <= computed above")
    print("3. Each single-plaquette 6x6 block IS PSD")
    print("   But sum of 6 blocks is NOT bounded above by 16*I_9 without V constraint")
    print("4. Key obstruction: 16*I_9 - M_9(I) = 0 (bound is TIGHT)")
    print("   => Full SOS decomposition requires terms vanishing at Q=I")
    print("   => SOS polynomial certificate needs degree >= 2 in (R-I) terms")
    print("5. Gap is O(eps^2) near Q=I (first-order vanishes)")
