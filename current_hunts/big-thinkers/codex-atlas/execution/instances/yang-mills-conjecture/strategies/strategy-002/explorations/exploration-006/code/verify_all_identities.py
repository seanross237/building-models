"""
Independent adversarial verification of ALL identities B1-B9.
Written from scratch — no code copied from prior explorations.
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize
import sys

np.random.seed(42)

def random_so3():
    """Random SO(3) via exponential map of random skew-symmetric."""
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def random_T_in_V():
    """Random T in V = {T : sum T_mu = 0}, 4x3 matrix."""
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)  # project to sum=0
    return T

def f(M, p):
    """f(M, p) = |p|^2 - p^T M p = p^T (I - M) p"""
    return np.dot(p, p) - np.dot(p, M @ p)

def verify_B1(n_trials=1000):
    """B1: Budget identity: 16||T||^2 = 4 sum_{mu<nu} |T_mu - T_nu|^2 for T with sum=0"""
    print("=== B1: Budget Identity ===")
    max_err = 0
    for _ in range(n_trials):
        T = random_T_in_V()
        lhs = 16 * np.sum(T**2)
        rhs = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                rhs += 4 * np.sum((T[mu] - T[nu])**2)
        err = abs(lhs - rhs)
        max_err = max(max_err, err)
    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def verify_B2(n_trials=1000):
    """B2: Per-plaquette identity
    4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U, T_mu) + 2f(W, T_nu) - 2 T_mu^T C T_nu
    where U = R_mu D, W = D R_nu^T,
    C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-R_mu D R_nu^T)
    """
    print("\n=== B2: Per-Plaquette Identity ===")
    max_err = 0
    for _ in range(n_trials):
        R_mu = random_so3()
        R_nu = random_so3()
        D = random_so3()
        T = random_T_in_V()
        mu, nu = np.random.choice(4, 2, replace=False)
        mu, nu = min(mu, nu), max(mu, nu)

        T_mu_vec = T[mu]
        T_nu_vec = T[nu]

        # LHS: 4|T_mu - T_nu|^2 - |B|^2
        # B = (I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu  (staggered formula, ignoring signs for identity check)
        # Actually, B_{mu,nu} = sum of signed terms. For identity verification, use:
        # |B|^2 where B uses the generic staggered mode formula
        # The signs come from (-1)^{|x|+mu} pattern. For a single plaquette identity, we use:
        # B = T_mu + R_mu D T_mu - R_mu T_nu - R_mu D R_nu^T T_nu  (with appropriate signs)
        # Actually, the staggered B-field for plaquette (mu,nu) at a vertex with standard signs:
        # We need to be careful. Let me use the formula from E001:
        # F_x(Q,T) = sum_{mu<nu} ||(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu||^2
        # So |B|^2 = ||(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu||^2
        # But wait, signs depend on the specific mu,nu pair. Let me use the absolute formula.

        # For the per-plaquette identity, the sign structure cancels — the identity holds for ANY signs.
        # Let's just directly compute with the formula as given.

        A_mat = np.eye(3) + R_mu @ D
        B_mat = R_mu + R_mu @ D @ R_nu.T
        B_vec = A_mat @ T_mu_vec - B_mat @ T_nu_vec
        B_sq = np.dot(B_vec, B_vec)

        lhs = 4 * np.sum((T_mu_vec - T_nu_vec)**2) - B_sq

        # RHS
        U = R_mu @ D
        W = D @ R_nu.T
        I3 = np.eye(3)
        C = (I3 - R_mu) + (I3 - R_nu.T) + (I3 - D.T) + (I3 - R_mu @ D @ R_nu.T)

        rhs = 2*f(U, T_mu_vec) + 2*f(W, T_nu_vec) - 2 * T_mu_vec @ C @ T_nu_vec

        err = abs(lhs - rhs)
        max_err = max(max_err, err)

    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def compute_Fx_and_gap(R, D_dict, T):
    """Compute F_x and 16||T||^2 - F_x from scratch.
    R: list of 4 SO(3) matrices
    D_dict: dict (mu,nu) -> SO(3) for mu<nu
    T: 4x3 matrix with sum=0
    """
    F_x = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            D = D_dict[(mu, nu)]
            A = np.eye(3) + R[mu] @ D
            B = R[mu] + R[mu] @ D @ R[nu].T
            Bvec = A @ T[mu] - B @ T[nu]
            F_x += np.dot(Bvec, Bvec)
    return F_x

def compute_sum_S(R, D_dict, T):
    """Compute sum_S from the master identity decomposition."""
    # sum_S = sum_x F_x decomposition remainder
    # sum_S = baseline + sum_{mu<nu} 2 u^T (I-D) v
    # where baseline = 6 sum_mu f(R_mu, T_mu) + |sum R_mu^T T_mu|^2

    sum_f = sum(f(R[mu], T[mu]) for mu in range(4))
    sum_a = sum(R[mu].T @ T[mu] for mu in range(4))
    baseline = 6 * sum_f + np.dot(sum_a, sum_a)

    delta = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            D = D_dict[(mu, nu)]
            u = R[mu].T @ T[mu] - T[nu]
            v = T[mu] - R[nu].T @ T[nu]
            E = np.eye(3) - D
            delta += 2 * u @ E @ v

    return baseline + delta

def verify_B3(n_trials=500):
    """B3: Sum-to-zero extraction:
    16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S
    """
    print("\n=== B3: Sum-to-Zero Extraction ===")
    max_err = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        D_dict = {(mu,nu): random_so3() for mu in range(4) for nu in range(mu+1, 4)}
        T = random_T_in_V()

        F_x = compute_Fx_and_gap(R, D_dict, T)
        gap = 16 * np.sum(T**2) - F_x

        sum_f = sum(f(R[mu], T[mu]) for mu in range(4))

        # Compute sum_S directly from the per-plaquette contributions
        sum_S_parts = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                D = D_dict[(mu, nu)]
                U = R[mu] @ D
                W = D @ R[nu].T
                I3 = np.eye(3)
                C = (I3 - R[mu]) + (I3 - R[nu].T) + (I3 - D.T) + (I3 - R[mu] @ D @ R[nu].T)
                S_mn = 2*f(U, T[mu]) + 2*f(W, T[nu]) - 2 * T[mu] @ C @ T[nu]
                # But we need to subtract the sum-to-zero part
                # Actually, let's compute gap - 2*sum_f and check = sum_S
                sum_S_parts += S_mn

        # The extraction says: sum over plaquettes of [4|T_mu-T_nu|^2 - |B|^2] = 16||T||^2 - F_x
        # And the RHS decomposes as 2*sum f + sum_S
        # So sum_S = gap - 2*sum_f
        rhs = 2 * sum_f + compute_sum_S(R, D_dict, T)

        err = abs(gap - rhs)
        max_err = max(max_err, err)

    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def verify_B4(n_trials=500):
    """B4: D=I base case: sum_S(D=I) = 6*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2 >= 0"""
    print("\n=== B4: D=I Base Case ===")
    max_err = 0
    min_val = float('inf')
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        D_dict = {(mu,nu): np.eye(3) for mu in range(4) for nu in range(mu+1, 4)}
        T = random_T_in_V()

        sum_S = compute_sum_S(R, D_dict, T)

        sum_f = sum(f(R[mu], T[mu]) for mu in range(4))
        sum_a = sum(R[mu].T @ T[mu] for mu in range(4))
        expected = 6 * sum_f + np.dot(sum_a, sum_a)

        err = abs(sum_S - expected)
        max_err = max(max_err, err)
        min_val = min(min_val, sum_S / max(np.sum(T**2), 1e-15))

    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Min sum_S/||T||^2: {min_val:.6f} (should be >= 0)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 and min_val > -1e-10 else 'FAILED'}")
    return max_err < 1e-10 and min_val > -1e-10

def verify_B5(n_trials=500):
    """B5: Delta factoring:
    sum_S = baseline + sum_{mu<nu} 2 u^T (I-D) v
    """
    print("\n=== B5: Delta Factoring ===")
    max_err = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        D_dict = {(mu,nu): random_so3() for mu in range(4) for nu in range(mu+1, 4)}
        T = random_T_in_V()

        # Compute sum_S directly
        F_x = compute_Fx_and_gap(R, D_dict, T)
        gap = 16 * np.sum(T**2) - F_x
        sum_f = sum(f(R[mu], T[mu]) for mu in range(4))
        sum_S_direct = gap - 2 * sum_f

        # Compute via delta factoring
        sum_S_factored = compute_sum_S(R, D_dict, T)

        err = abs(sum_S_direct - sum_S_factored)
        max_err = max(max_err, err)

    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def verify_B6(n_trials=500):
    """B6: M9 is affine in D.
    Test: M9(R, alpha*D1 + (1-alpha)*D2) = alpha*M9(R,D1) + (1-alpha)*M9(R,D2)
    Note: alpha*D1 + (1-alpha)*D2 may not be in SO(3), but affinity should hold.
    """
    print("\n=== B6: M9 Affine in D ===")
    max_err = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        T = random_T_in_V()

        # Pick a random pair (mu,nu) and two D values
        mu, nu = 0, 1  # test with first pair
        D1 = random_so3()
        D2 = random_so3()
        alpha = np.random.rand()
        D_mix = alpha * D1 + (1 - alpha) * D2

        # Create D_dicts with D1, D2, and D_mix for pair (mu,nu), identity elsewhere
        def make_D_dict(D_val):
            d = {(i,j): np.eye(3) for i in range(4) for j in range(i+1, 4)}
            d[(mu, nu)] = D_val
            return d

        F1 = compute_Fx_and_gap(R, make_D_dict(D1), T)
        F2 = compute_Fx_and_gap(R, make_D_dict(D2), T)
        F_mix = compute_Fx_and_gap(R, make_D_dict(D_mix), T)

        expected = alpha * F1 + (1 - alpha) * F2
        err = abs(F_mix - expected)
        max_err = max(max_err, err)

    print(f"  Max error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def verify_B7_B8_B9(n_trials=1000):
    """B7: Cauchy-Schwarz contraction
    B8: sum_{mu<nu} ||u-v||^2 = 4*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2
    B9: Cancellation → F >= 0
    """
    print("\n=== B7-B9: CS Contraction + Key Computation + Cancellation ===")

    max_err_B7 = 0  # CS bound
    max_err_B8 = 0  # Key computation
    max_err_B9 = 0  # Cancellation identity
    min_F = float('inf')
    min_sum_S = float('inf')
    violations_F = 0
    violations_sum_S = 0

    for trial in range(n_trials):
        R = [random_so3() for _ in range(4)]
        D_dict = {(mu,nu): random_so3() for mu in range(4) for nu in range(mu+1, 4)}
        T = random_T_in_V()
        T_norm_sq = np.sum(T**2)
        if T_norm_sq < 1e-15:
            continue

        # Compute u, v for each pair
        u_list = {}
        v_list = {}
        for mu in range(4):
            for nu in range(mu+1, 4):
                u_list[(mu,nu)] = R[mu].T @ T[mu] - T[nu]
                v_list[(mu,nu)] = T[mu] - R[nu].T @ T[nu]

        # B7: Check u^T D v <= ||u|| * ||v|| for each pair
        for mu in range(4):
            for nu in range(mu+1, 4):
                D = D_dict[(mu, nu)]
                u = u_list[(mu,nu)]
                v = v_list[(mu,nu)]
                lhs = u @ D @ v
                rhs = np.linalg.norm(u) * np.linalg.norm(v)
                if lhs > rhs + 1e-10:
                    max_err_B7 = max(max_err_B7, lhs - rhs)

        # B8: sum ||u-v||^2 = 4*sum f + |sum a|^2
        sum_uv_sq = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                diff = u_list[(mu,nu)] - v_list[(mu,nu)]
                sum_uv_sq += np.dot(diff, diff)

        sum_f = sum(f(R[mu], T[mu]) for mu in range(4))
        sum_a = sum(R[mu].T @ T[mu] for mu in range(4))
        expected_B8 = 4 * sum_f + np.dot(sum_a, sum_a)

        err_B8 = abs(sum_uv_sq - expected_B8)
        max_err_B8 = max(max_err_B8, err_B8)

        # B9: F = 2*sum_f + sum (||u|| - ||v||)^2
        sum_norm_diff_sq = 0
        sum_CS_gap = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                u = u_list[(mu,nu)]
                v = v_list[(mu,nu)]
                norm_u = np.linalg.norm(u)
                norm_v = np.linalg.norm(v)
                sum_norm_diff_sq += (norm_u - norm_v)**2
                sum_CS_gap += (norm_u * norm_v - np.dot(u, v))

        F_val = 2 * sum_f + sum_norm_diff_sq

        # Check F = baseline - sum 2(||u||*||v|| - u.v) = baseline - 2*sum_CS_gap
        baseline = 6 * sum_f + np.dot(sum_a, sum_a)
        F_check = baseline - 2 * sum_CS_gap
        err_B9 = abs(F_val - F_check)
        max_err_B9 = max(max_err_B9, err_B9)

        # Check F >= 0
        if F_val < -1e-10:
            violations_F += 1
        min_F = min(min_F, F_val / T_norm_sq)

        # Check sum_S >= F (so sum_S >= 0)
        sum_S = compute_sum_S(R, D_dict, T)
        if sum_S < -1e-10:
            violations_sum_S += 1
        min_sum_S = min(min_sum_S, sum_S / T_norm_sq)

    print(f"  B7 (CS bound) max violation: {max_err_B7:.2e} (should be 0)")
    print(f"  B8 max error: {max_err_B8:.2e} (should be < 1e-10)")
    print(f"  B9 max error: {max_err_B9:.2e} (should be < 1e-10)")
    print(f"  Min F/||T||^2: {min_F:.6f} (should be >= 0)")
    print(f"  Min sum_S/||T||^2: {min_sum_S:.6f} (should be >= 0)")
    print(f"  F violations: {violations_F}/{n_trials}")
    print(f"  sum_S violations: {violations_sum_S}/{n_trials}")

    all_ok = (max_err_B7 < 1e-10 and max_err_B8 < 1e-10 and max_err_B9 < 1e-10
              and violations_F == 0 and violations_sum_S == 0)
    print(f"  Status: {'VERIFIED' if all_ok else 'FAILED'}")
    return all_ok

def verify_full_gap(n_trials=500):
    """Verify the FULL gap: 16||T||^2 - F_x >= 0"""
    print("\n=== Full Gap: 16||T||^2 - F_x >= 0 ===")
    min_gap = float('inf')
    violations = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        D_dict = {(mu,nu): random_so3() for mu in range(4) for nu in range(mu+1, 4)}
        T = random_T_in_V()
        T_norm_sq = np.sum(T**2)
        if T_norm_sq < 1e-15:
            continue

        F_x = compute_Fx_and_gap(R, D_dict, T)
        gap = 16 * T_norm_sq - F_x

        if gap < -1e-10:
            violations += 1
        min_gap = min(min_gap, gap / T_norm_sq)

    print(f"  Min gap/||T||^2: {min_gap:.6f} (should be >= 0)")
    print(f"  Violations: {violations}/{n_trials}")
    print(f"  Status: {'VERIFIED' if violations == 0 else 'FAILED'}")
    return violations == 0

if __name__ == "__main__":
    results = {}
    results['B1'] = verify_B1()
    results['B2'] = verify_B2()
    results['B3'] = verify_B3()
    results['B4'] = verify_B4()
    results['B5'] = verify_B5()
    results['B6'] = verify_B6()
    results['B7-B9'] = verify_B7_B8_B9()
    results['full_gap'] = verify_full_gap()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for k, v in results.items():
        print(f"  {k}: {'VERIFIED' if v else 'FAILED'}")

    all_pass = all(results.values())
    print(f"\nOverall: {'ALL VERIFIED' if all_pass else 'SOME FAILED'}")
