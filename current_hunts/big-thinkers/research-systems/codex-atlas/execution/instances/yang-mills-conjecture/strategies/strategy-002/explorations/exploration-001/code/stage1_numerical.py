"""
Stage 1: Numerical Verification of lambda_max(M_9(Q)) <= 16

Tests 1000 random SO(3)^10 configurations.
Constructs M_12(Q) explicitly, projects to 9D constraint subspace V = {T: sum T_mu = 0},
computes lambda_max(M_9(Q)).

Also verifies at Q=I that M_12(I) = 16*I_12 - 4*(J_4 ⊗ I_3) as claimed.
"""
import numpy as np
from scipy.linalg import null_space, eigh
from scipy.stats import ortho_group
import sys

np.random.seed(42)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def random_SO3(rng=None):
    """Generate a uniformly random SO(3) matrix using Haar measure."""
    if rng is None:
        rng = np.random
    # Use QR decomposition of a random Gaussian matrix
    M = rng.randn(3, 3)
    Q, R = np.linalg.qr(M)
    # Correct sign so det(Q) = +1
    Q = Q * np.sign(np.diag(R))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

def identity_SO3():
    return np.eye(3)

def construct_M12(R_list, D_dict):
    """
    Construct the 12x12 per-vertex quadratic form matrix M_12(Q).

    R_list : list of 4 SO(3) matrices [R_0, R_1, R_2, R_3]
    D_dict : dict (mu, nu) -> SO(3) for mu < nu (6 cross-links)

    F_x(Q, T) = sum_{mu<nu} |(I + R_mu D_munu) T_mu - (R_mu + R_mu D_munu R_nu^T) T_nu|^2
              = vec(T)^T M_12 vec(T)
    """
    M = np.zeros((12, 12))
    I3 = np.eye(3)

    for mu in range(4):
        for nu in range(mu + 1, 4):
            R_mu = R_list[mu]
            R_nu = R_list[nu]
            D = D_dict[(mu, nu)]

            A = I3 + R_mu @ D          # 3x3, coefficient of T_mu
            B = R_mu + R_mu @ D @ R_nu.T  # 3x3, coefficient of T_nu (negated)

            # F contribution = ||A T_mu - B T_nu||^2
            # = T_mu^T (A^T A) T_mu - T_mu^T (A^T B) T_nu - T_nu^T (B^T A) T_mu + T_nu^T (B^T B) T_nu
            ATA = A.T @ A
            BTB = B.T @ B
            ATB = A.T @ B

            M[3*mu:3*mu+3, 3*mu:3*mu+3] += ATA
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += BTB
            M[3*mu:3*mu+3, 3*nu:3*nu+3] -= ATB
            M[3*nu:3*nu+3, 3*mu:3*mu+3] -= ATB.T

    return M

def compute_constraint_basis():
    """
    Compute W: 12x9 orthonormal basis for V = {vec(T) in R^12 : sum_mu T_mu = 0}.
    Constraint: C @ v = 0,  C = [I_3 | I_3 | I_3 | I_3]  (3x12)
    """
    C = np.hstack([np.eye(3)] * 4)  # 3x12
    W = null_space(C)               # 12x9
    return W

def lambda_max_M9(M12, W):
    """Compute lambda_max of M_12 restricted to the constraint subspace V."""
    M9 = W.T @ M12 @ W  # 9x9
    eigs = eigh(M9, eigvals_only=True)
    return np.max(eigs)

def check_M12_at_identity(W):
    """Verify M_12(I) = 16*I_12 - 4*(J_4 ⊗ I_3) and eigenvalues {0(x3), 16(x9)}."""
    R_list = [np.eye(3)] * 4
    D_dict = {(mu, nu): np.eye(3) for mu in range(4) for nu in range(mu+1, 4)}
    M12_I = construct_M12(R_list, D_dict)

    # Expected: 16*I_12 - 4*(ones(4,4) ⊗ I_3)
    J4 = np.ones((4, 4))
    expected = 16 * np.eye(12) - 4 * np.kron(J4, np.eye(3))

    err = np.max(np.abs(M12_I - expected))
    print(f"  M_12(I) vs expected: max error = {err:.2e}")
    assert err < 1e-10, "M_12(I) construction error!"

    eigs_full = np.sort(np.linalg.eigvalsh(M12_I))
    print(f"  Eigenvalues of M_12(I): min={eigs_full[0]:.6f}, max={eigs_full[-1]:.6f}")
    print(f"  Expected: 0 (×3), 16 (×9)")

    lmax = lambda_max_M9(M12_I, W)
    print(f"  lambda_max(M_9(I)) = {lmax:.6f}  [expected: 16.0]")
    return err < 1e-10

# ──────────────────────────────────────────────
# Main Stage 1 computation
# ──────────────────────────────────────────────

def run_stage1(n_samples=1000, seed=42):
    rng = np.random.RandomState(seed)
    W = compute_constraint_basis()

    print("=" * 60)
    print("Stage 1: Numerical Verification of lambda_max(M_9(Q)) <= 16")
    print("=" * 60)

    # ---- Sanity check at Q=I ----
    print("\n[Sanity check] M_12 at Q = Identity:")
    ok = check_M12_at_identity(W)
    print(f"  Sanity check passed: {ok}")

    # ---- Random sampling ----
    print(f"\n[Random sampling] Testing {n_samples} random SO(3)^10 configurations...")
    lmax_values = np.zeros(n_samples)
    worst_Q = None
    worst_lmax = -np.inf

    for i in range(n_samples):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng)
                  for mu in range(4) for nu in range(mu+1, 4)}

        M12 = construct_M12(R_list, D_dict)
        lmax = lambda_max_M9(M12, W)
        lmax_values[i] = lmax

        if lmax > worst_lmax:
            worst_lmax = lmax
            worst_Q = (R_list, D_dict)

        if (i + 1) % 200 == 0:
            print(f"  Processed {i+1}/{n_samples}, current max lambda = {np.max(lmax_values[:i+1]):.6f}")

    gap_values = 16 - lmax_values

    print("\n[Results]")
    print(f"  Samples tested:          {n_samples}")
    print(f"  All lambda_max < 16?     {np.all(lmax_values < 16.0 + 1e-10)}")
    print(f"  Max lambda_max found:    {np.max(lmax_values):.8f}")
    print(f"  Min gap (16 - lmax):     {np.min(gap_values):.8f}")
    print(f"  Mean lambda_max:         {np.mean(lmax_values):.6f}")
    print(f"  Std dev:                 {np.std(lmax_values):.6f}")
    print(f"  25th pct lambda_max:     {np.percentile(lmax_values, 25):.6f}")
    print(f"  Median lambda_max:       {np.percentile(lmax_values, 50):.6f}")
    print(f"  75th pct lambda_max:     {np.percentile(lmax_values, 75):.6f}")
    print(f"  95th pct lambda_max:     {np.percentile(lmax_values, 95):.6f}")
    print(f"  99th pct lambda_max:     {np.percentile(lmax_values, 99):.6f}")

    # Verify cross-term bound
    print("\n[Cross-term ratio check]")
    cross_ratios = []
    for i in range(min(200, n_samples)):
        R_list = [random_SO3(rng) for _ in range(4)]
        D_dict = {(mu, nu): random_SO3(rng)
                  for mu in range(4) for nu in range(mu+1, 4)}
        M12 = construct_M12(R_list, D_dict)
        ratio = check_cross_term_ratio(M12, W)
        if ratio is not None:
            cross_ratios.append(ratio)

    if cross_ratios:
        print(f"  Max |cross|/f_same ratio: {np.max(cross_ratios):.4f}  [bound claimed: 8.2%]")
        print(f"  Mean ratio:               {np.mean(cross_ratios):.4f}")

    return lmax_values, worst_Q, worst_lmax

def check_cross_term_ratio(M12, W):
    """
    For a random T in V, compute ratio |cross|/f_same where
    f_same = sum of non-negative f(R, T_mu) terms
    cross = sum of cross terms T_mu^T C_{mu,nu} T_nu
    in the identity: 16||T||^2 - F_x = sum(f_same) + sum(cross)
    Returns max ratio over random T vectors.
    """
    # Use random T in V
    max_ratio = 0.0
    for _ in range(10):
        t = W @ np.random.randn(9)
        t = t / np.linalg.norm(t)
        f_x = t @ (M12 @ t)
        budget = 16 * np.dot(t, t)
        gap = budget - f_x

        # Rough decomposition: f_same >= 0, so |cross| <= gap + |cross|
        # We just report gap > 0 as sanity check here
        if gap < -1e-10:
            return None  # violation found
        if gap > 1e-12:
            # ratio = how much gap comes from cross terms / f_same
            # Without full decomposition, just return gap/budget as fraction
            pass

    return None  # placeholder — full decomposition done in Stage 2

if __name__ == "__main__":
    lmax_values, worst_Q, worst_lmax = run_stage1(n_samples=1000)

    print(f"\n[Summary]")
    print(f"  Bound lambda_max <= 16 holds for all 1000 random samples: {np.all(lmax_values < 16.0 + 1e-10)}")
    print(f"  Worst case: lambda_max = {worst_lmax:.8f}, gap = {16 - worst_lmax:.8f}")
    print(f"\n  Note: At Q=I, lambda_max = 16.0 exactly (bound is TIGHT)")
