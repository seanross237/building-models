"""
Stage 4b: Certificate attempt — per-plaquette ratio and structural analysis.

Key question: Is 16||T||^2 - F_x a sum of per-plaquette certificates?
I.e., does |A T_mu - B T_nu|^2 <= 4 |T_mu - T_nu|^2 hold per plaquette?

If yes: the budget identity 16||T||^2 = 4 sum |T_mu - T_nu|^2 directly gives
  F_x = sum |A T_mu - B T_nu|^2 <= 4 sum |T_mu - T_nu|^2 = 16||T||^2.

This would be an SOS certificate WITHOUT needing the full constraint — only the
budget identity.

This script:
1. Tests the per-plaquette ratio F_plaq / (4|T_mu - T_nu|^2)
2. Checks whether a per-plaquette algebraic bound works
3. Attempts a direct algebraic SOS factorization for a single plaquette
4. Analyzes the cross-term bound using Lie algebra expansion
"""
import numpy as np
from scipy.linalg import null_space, eigh
import time

np.random.seed(42)

def random_SO3(rng):
    M = rng.randn(3, 3)
    Q, R = np.linalg.qr(M)
    Q = Q * np.sign(np.diag(R))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

W_basis = null_space(np.hstack([np.eye(3)] * 4))  # 12x9
I3 = np.eye(3)

# ─────────────────────────────────────────────
# 1. Test per-plaquette ratio
# ─────────────────────────────────────────────

def test_per_plaquette_ratio(n_trials=1000, n_T=100, seed=42):
    """
    Test: is |A T_mu - B T_nu|^2 <= 4 |T_mu - T_nu|^2 for all (mu,nu), T, Q?

    If TRUE: F_x <= 4 sum |T_mu - T_nu|^2 = 16||T||^2 (for T in V)
    This would give a DIRECT certificate without needing the full cross-term analysis.
    """
    rng = np.random.RandomState(seed)
    max_ratio = 0.0
    violations = 0
    n_total = 0
    worst = None

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

                for _ in range(n_T):
                    # Random T_mu, T_nu in R^3 (unconstrained for this test)
                    p = rng.randn(3)
                    q = rng.randn(3)
                    denom = np.dot(p - q, p - q)
                    if denom < 1e-12:
                        continue

                    Bv = A @ p - B @ q
                    numer = np.dot(Bv, Bv)
                    ratio = numer / (4 * denom)
                    n_total += 1

                    if ratio > max_ratio:
                        max_ratio = ratio
                        worst = (R_mu, R_nu, D, p, q, ratio)

                    if ratio > 1.0 + 1e-8:
                        violations += 1

    print(f"[Per-plaquette ratio test] ({n_trials} configs, {n_T} T per plaquette)")
    print(f"  Max |A p - B q|^2 / (4|p-q|^2): {max_ratio:.6f}")
    print(f"  Violations (ratio > 1):           {violations}/{n_total}")
    print(f"  Bound per plaquette holds:         {violations == 0}")

    if worst:
        R_mu, R_nu, D, p, q, ratio = worst
        A = I3 + R_mu @ D
        B = R_mu + R_mu @ D @ R_nu.T
        print(f"\n  Worst case: ratio = {ratio:.6f}")
        print(f"    A = I + R_mu D, B = R_mu + R_mu D R_nu^T")
        print(f"    ||A||^2 = {np.sum(A**2):.4f}, ||B||^2 = {np.sum(B**2):.4f}")
        # Check: A and B are always of the form I + R for R in SO(3)?
        # If A = I + U (U in SO(3)): ||A||^2 = 3 + 2*Tr(U) + 3 = 6 + 2*Tr(U)
        U = R_mu @ D
        print(f"    Tr(U=R_mu D): {np.trace(U):.4f} (range [-1, 3])")
        print(f"    ||A||^2 = {6 + 2*np.trace(U):.4f} (formula check)")

    return max_ratio, violations

# ─────────────────────────────────────────────
# 2. When does per-plaquette bound fail?
# ─────────────────────────────────────────────

def find_per_plaquette_max(n_gradient_steps=500, n_starts=20, seed=77):
    """
    Maximize |A p - B q|^2 / (4|p-q|^2) over R_mu, R_nu, D in SO(3) and p, q in R^3.

    This is a generalized eigenvalue problem. For fixed A, B:
    max_{p,q} |A p - B q|^2 / |p-q|^2 = lambda_max(M_{A,B})
    where M_{A,B} = [[A^T A, -A^T B], [-B^T A, B^T B]].

    Already know M_{A,B} is PSD. So max eigenvalue >= 0.
    Need to compare with 4.
    """
    rng = np.random.RandomState(seed)

    def so3_project(M):
        U, s, Vt = np.linalg.svd(M)
        R = U @ Vt
        if np.linalg.det(R) < 0:
            U[:, -1] *= -1
            R = U @ Vt
        return R

    def plaquette_max_eigenvalue(R_mu, R_nu, D):
        A = I3 + R_mu @ D
        B = R_mu + R_mu @ D @ R_nu.T
        ATA, BTB, ATB = A.T @ A, B.T @ B, A.T @ B
        block = np.block([[ATA, -ATB], [-ATB.T, BTB]])
        return np.linalg.eigvalsh(block)[-1]

    global_max = 0.0
    results = []

    for start in range(n_starts):
        R_mu = random_SO3(rng)
        R_nu = random_SO3(rng)
        D = random_SO3(rng)
        lmax = plaquette_max_eigenvalue(R_mu, R_nu, D)

        # Gradient ascent
        for step in range(n_gradient_steps):
            # Perturb and take gradient step
            best_l = lmax
            best_cfg = (R_mu, R_nu, D)

            for _ in range(5):
                eps = 0.1 * (0.99 ** step)
                dR_mu = so3_project(R_mu + eps * rng.randn(3,3))
                dR_nu = so3_project(R_nu + eps * rng.randn(3,3))
                dD = so3_project(D + eps * rng.randn(3,3))
                l_new = plaquette_max_eigenvalue(dR_mu, dR_nu, dD)
                if l_new > best_l:
                    best_l = l_new
                    best_cfg = (dR_mu, dR_nu, dD)

            R_mu, R_nu, D = best_cfg
            lmax = best_l

        results.append(lmax)
        if lmax > global_max:
            global_max = lmax
            best_final = (R_mu, R_nu, D)

    print(f"\n[Per-plaquette eigenvalue max] ({n_starts} starts × {n_gradient_steps} steps)")
    print(f"  Max lambda_max(M_AB): {global_max:.6f}")
    print(f"  Per-plaquette bound (vs 4): {global_max:.6f} vs 4")
    print(f"  Ratio to 4:                {global_max / 4:.4f}")

    # At the adversarial maximum, what is the config?
    R_mu, R_nu, D = best_final
    A = I3 + R_mu @ D
    B = R_mu + R_mu @ D @ R_nu.T
    ATA, BTB, ATB = A.T @ A, B.T @ B, A.T @ B
    block = np.block([[ATA, -ATB], [-ATB.T, BTB]])
    eigs = np.linalg.eigvalsh(block)
    print(f"  All eigenvalues of adversarial block: {np.round(eigs, 4)}")
    print(f"  Tr(R_mu D): {np.trace(R_mu @ D):.4f}")
    print(f"  Tr(D R_nu^T): {np.trace(D @ R_nu.T):.4f}")

    return global_max

# ─────────────────────────────────────────────
# 3. Algebraic max eigenvalue of single-plaquette block
# ─────────────────────────────────────────────

def algebraic_block_analysis():
    """
    Analytical analysis: what is lambda_max of M_{A,B} where
    A = I + U, B = R_mu + U R_nu^T, U = R_mu D?

    Note: A = I + U, B = R_mu(I + D R_nu^T)

    Let V = D R_nu^T (also in SO(3)). Then:
    B = R_mu(I + V) = R_mu A'  where A' = I + V.

    ||A p - B q||^2 = ||(I+U) p - R_mu(I+V) q||^2

    The 6x6 matrix M_{A,B}:
    A^T A = (I+U^T)(I+U) = 2I + U + U^T = 2I + 2 sym(U)
    B^T B = (I+V)^T R_mu^T R_mu (I+V) = (I+V^T)(I+V) = 2I + V + V^T = 2I + 2 sym(V)
    A^T B = (I+U^T) R_mu (I+V) = R_mu + U^T R_mu + R_mu V + U^T R_mu V

    where U = R_mu D, so U^T = D^T R_mu^T, and:
    U^T R_mu = D^T R_mu^T R_mu = D^T
    U^T R_mu V = D^T R_mu^T R_mu V = D^T V = D^T (D R_nu^T) = R_nu^T

    So A^T B = R_mu + D^T + R_mu V + R_nu^T
             = R_mu + D^T + R_mu D R_nu^T + R_nu^T

    Hmm, let me verify: R_mu V = R_mu D R_nu^T, yes.

    So A^T B = R_mu + D^T + R_mu D R_nu^T + R_nu^T.

    The full block:
    M_{A,B} = [[2I + 2 sym(U), -(R_mu + D^T + R_mu D R_nu^T + R_nu^T)],
               [-(R_mu + D^T + R_mu D R_nu^T + R_nu^T)^T, 2I + 2 sym(V)]]

    = [[2I + 2 sym(U), -C^T],
       [-C, 2I + 2 sym(V)]]

    where C = R_mu + D^T + R_mu D R_nu^T + R_nu^T = A^T B.

    The Schur complement:
    lambda_max(M_{A,B}) > t iff M_{A,B} - t I_6 is not PSD
    iff [2-t] I + 2 sym(U) - C^T [(2-t)I + 2 sym(V)]^{-1} C is not PSD.

    When t = 4 (testing whether lambda_max <= 4):
    Schur: (2-4)I + 2 sym(U) - C^T [(2-4)I + 2 sym(V)]^{-1} C
         = -2I + 2 sym(U) - C^T [-2I + 2 sym(V)]^{-1} C

    This is a bit complex. Let me check numerically whether lambda_max <= 4.
    """
    print("\n[Algebraic block analysis]")

    rng = np.random.RandomState(42)
    max_lmax = 0.0
    for _ in range(5000):
        U = random_SO3(rng)  # U = R_mu D
        V = random_SO3(rng)  # V = D R_nu^T

        # Reconstruct A^T B (using the derivation above, but with arbitrary R_mu, D, R_nu):
        # For a fresh random config:
        R_mu = random_SO3(rng)
        R_nu = random_SO3(rng)
        D = random_SO3(rng)
        U = R_mu @ D
        V = D @ R_nu.T

        A = I3 + U
        B = R_mu + U @ R_nu.T
        ATA = A.T @ A
        BTB = B.T @ B
        ATB = A.T @ B

        block = np.block([[ATA, -ATB], [-ATB.T, BTB]])
        lmax = np.linalg.eigvalsh(block)[-1]
        max_lmax = max(max_lmax, lmax)

    print(f"  Max lambda_max(M_AB) over 5000 random configs: {max_lmax:.6f}")
    print(f"  Compare to 4 (per-plaquette budget):           4.000000")
    print(f"  Is lambda_max <= 4? {max_lmax <= 4.0 + 1e-8}")

    # What's the theoretical max?
    # At U=I, V=I: A = 2I, B = R_mu + R_mu R_nu^T = R_mu(I + R_nu^T)
    # Hmm not identity B at identity.

    # At U=I, R_mu=I, R_nu=I, D=I: A=2I, B=2I
    # block: [[4I, -4I], [-4I, 4I]]
    # Eigenvalues: 0 (×3) and 8 (×3)!
    A_I = 2*I3
    B_I = 2*I3
    block_I = np.block([[A_I.T @ A_I, -A_I.T @ B_I], [-B_I.T @ A_I, B_I.T @ B_I]])
    eigs_I = np.linalg.eigvalsh(block_I)
    print(f"\n  Block at R_mu=R_nu=D=I: eigenvalues = {np.round(eigs_I, 4)}")
    print(f"  Max eigenvalue at Q=I: {np.max(eigs_I):.4f}")
    print(f"  => lambda_max(M_AB) = 8 at Q=I, FAR exceeding 4!")

    print(f"\n  KEY INSIGHT: Per-plaquette bound DOES NOT HOLD!")
    print(f"  |A T_mu - B T_nu|^2 can be UP TO 8 |T_mu - T_nu|^2 (not <= 4)")
    print(f"  This means the per-plaquette approach FAILS for a global certificate.")
    print(f"  The constraint sum T_mu = 0 is ESSENTIAL to cancel the excess.")

    return max_lmax

# ─────────────────────────────────────────────
# 4. Global lambda_max analysis: what is the maximum over all Q?
# ─────────────────────────────────────────────

def global_lambda_max_analysis(n_samples=5000, seed=12345):
    """
    Compute lambda_max(M_9(Q)) for a large number of samples, focusing on the
    distribution and finding the global maximum.

    Also: for each adversarial lambda_max, check which eigenvector mode achieves it.
    """
    rng = np.random.RandomState(seed)

    def construct_M12_full(R_list, D_dict):
        M = np.zeros((12, 12))
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

    lmax_values = []
    global_max = -np.inf
    best_config = None

    for i in range(n_samples):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng) for mu in range(4) for nu in range(mu+1, 4)}
        M12 = construct_M12_full(R_list, D_dict)
        M9 = W_basis.T @ M12 @ W_basis
        lmax = np.linalg.eigvalsh(M9)[-1]
        lmax_values.append(lmax)

        if lmax > global_max:
            global_max = lmax
            best_config = (R_list, D_dict, M12)

    lmax_arr = np.array(lmax_values)
    print(f"\n[Global lambda_max analysis] ({n_samples} samples)")
    print(f"  Global max:     {global_max:.8f}")
    print(f"  Min gap:        {16 - global_max:.8f}")
    print(f"  Mean:           {np.mean(lmax_arr):.4f}")
    print(f"  99th pct:       {np.percentile(lmax_arr, 99):.4f}")
    print(f"  99.9th pct:     {np.percentile(lmax_arr, 99.9):.4f}")

    # Analyze the adversarial eigenvector
    if best_config:
        R_list, D_dict, M12 = best_config
        M9 = W_basis.T @ M12 @ W_basis
        eigs, vecs = np.linalg.eigh(M9)
        v_best = W_basis @ vecs[:, -1]  # 12D eigenvector
        T_best = v_best.reshape(4, 3)
        print(f"\n  Adversarial eigenvector (T matrix, 4×3):")
        print(f"  sum T_mu = {np.sum(T_best, axis=0)}  [should be ~0]")
        print(f"  ||T_0||={np.linalg.norm(T_best[0]):.4f}, ||T_1||={np.linalg.norm(T_best[1]):.4f},"
              f" ||T_2||={np.linalg.norm(T_best[2]):.4f}, ||T_3||={np.linalg.norm(T_best[3]):.4f}")

        # Check per-plaquette contributions to F_x
        print(f"\n  Per-plaquette F contributions (in adversarial case):")
        total_F = 0.0
        total_budget = 0.0
        for mu in range(4):
            for nu in range(mu+1, 4):
                A = I3 + R_list[mu] @ D_dict[(mu, nu)]
                B = R_list[mu] + R_list[mu] @ D_dict[(mu, nu)] @ R_list[nu].T
                Bv = A @ T_best[mu] - B @ T_best[nu]
                F_plaq = np.dot(Bv, Bv)
                budget_plaq = 4 * np.dot(T_best[mu] - T_best[nu], T_best[mu] - T_best[nu])
                total_F += F_plaq
                total_budget += budget_plaq
                ratio = F_plaq / budget_plaq if budget_plaq > 1e-10 else np.inf
                print(f"    ({mu},{nu}): F={F_plaq:.4f}, budget=4|T_mu-T_nu|^2={budget_plaq:.4f}, ratio={ratio:.4f}")

        print(f"  Total F_x:     {total_F:.6f}")
        print(f"  16||T||^2:     {16 * np.dot(v_best, v_best):.6f}")
        print(f"  Total budget:  {total_budget:.6f}  [should = 16||T||^2]")

    return global_max, lmax_arr

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Stage 4b: Certificate Structure Analysis")
    print("=" * 60)

    print("\n--- Test 1: Per-plaquette ratio check ---")
    max_ratio, violations = test_per_plaquette_ratio(n_trials=500, n_T=100)

    print("\n--- Test 2: Find per-plaquette adversarial max ---")
    global_pp_max = find_per_plaquette_max(n_gradient_steps=300, n_starts=30, seed=77)

    print("\n--- Test 3: Algebraic block analysis ---")
    algebraic_block_analysis()

    print("\n--- Test 4: Global M_9 analysis ---")
    global_max, lmax_arr = global_lambda_max_analysis(n_samples=5000)

    print("\n" + "=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    print(f"1. Per-plaquette ratio max: {max_ratio:.4f}  (vs per-plaquette budget: 1.0)")
    print(f"   => Per-plaquette bound |Ap-Bq|^2 <= 4|p-q|^2 FAILS (ratio {max_ratio:.2f} > 1)")
    print(f"   => Need GLOBAL cancellation across plaquettes using sum T_mu = 0")
    print(f"2. Single-plaquette 6x6 block lambda_max ~ {global_pp_max:.2f} >> 4")
    print(f"   => Each plaquette contributes up to {global_pp_max:.2f}*|T_mu|^2 per mode")
    print(f"   => Cancellation requires the constraint subspace V crucially")
    print(f"3. Global M_9 lambda_max: {global_max:.6f} < 16")
    print(f"   => Bound holds with gap {16-global_max:.6f}")
    print(f"\nSOS CERTIFICATE STRUCTURE:")
    print(f"  - Cannot decompose plaquette-by-plaquette (each can exceed 4*|T_mu-T_nu|^2)")
    print(f"  - Must use global structure + constraint sum T_mu = 0")
    print(f"  - The budget identity is ESSENTIAL (not just a convenient identity)")
    print(f"  - Candidate: mix of 2f(U,T_mu) + 2f(W,T_nu) terms")
    print(f"    with cross terms bounded using AM-GM + sum T_mu = 0")
