"""
Fix B6: M9 is affine in D (for D in SO(3)).
The key identity: |B|^2 = |p|^2 + |v|^2 + 2*p^T*R_mu*D*v
where p = T_mu - R_mu*T_nu, v = T_mu - R_nu^T*T_nu
This is LINEAR in D, making F_x AFFINE in each D_{mu,nu}.
"""
import numpy as np
from scipy.linalg import expm

np.random.seed(42)

def random_so3():
    v = np.random.randn(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return expm(K)

def random_T_in_V():
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)
    return T

def test_affine_identity(n_trials=2000):
    """Test that |B|^2 = |p|^2 + |v|^2 + 2*p^T*R*D*v for D in SO(3)."""
    print("=== B6: Affine Identity Test ===")
    max_err = 0
    for _ in range(n_trials):
        R_mu = random_so3()
        R_nu = random_so3()
        D = random_so3()
        T = random_T_in_V()
        mu, nu = 0, 1

        T_mu = T[mu]
        T_nu = T[nu]

        # Direct computation of |B|^2
        A = np.eye(3) + R_mu @ D
        B_mat = R_mu + R_mu @ D @ R_nu.T
        B_vec = A @ T_mu - B_mat @ T_nu
        B_sq_direct = np.dot(B_vec, B_vec)

        # Affine formula
        p = T_mu - R_mu @ T_nu
        v = T_mu - R_nu.T @ T_nu
        B_sq_affine = np.dot(p, p) + np.dot(v, v) + 2 * p @ (R_mu @ D @ v)

        err = abs(B_sq_direct - B_sq_affine)
        max_err = max(max_err, err)

    print(f"  Max |direct - affine|: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def test_affine_sum(n_trials=1000):
    """Test the full F_x is affine in each D_{mu,nu} by verifying the identity on F_x."""
    print("\n=== B6: Full F_x Affine Test ===")
    max_err = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        T = random_T_in_V()

        F_x = 0
        F_x_affine = 0
        D_dict = {}
        for mu in range(4):
            for nu in range(mu+1, 4):
                D = random_so3()
                D_dict[(mu,nu)] = D

                # Direct
                A = np.eye(3) + R[mu] @ D
                B_mat = R[mu] + R[mu] @ D @ R[nu].T
                B_vec = A @ T[mu] - B_mat @ T[nu]
                F_x += np.dot(B_vec, B_vec)

                # Affine
                p = T[mu] - R[mu] @ T[nu]
                v = T[mu] - R[nu].T @ T[nu]
                F_x_affine += np.dot(p, p) + np.dot(v, v) + 2 * p @ (R[mu] @ D @ v)

        err = abs(F_x - F_x_affine)
        max_err = max(max_err, err)

    print(f"  Max |direct - affine|: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

def test_affine_via_linearity(n_trials=1000):
    """Directly verify F(alpha*D1 + (1-alpha)*D2) = alpha*F(D1) + (1-alpha)*F(D2)
    using the affine formula (which is valid for any D, not just SO(3)).
    """
    print("\n=== B6: Affine Linearity Interpolation Test ===")
    max_err = 0
    for _ in range(n_trials):
        R = [random_so3() for _ in range(4)]
        T = random_T_in_V()
        target_pair = (0, 1)

        D1 = random_so3()
        D2 = random_so3()
        alpha = np.random.rand()

        # Compute F using AFFINE formula for each D
        def F_affine(D_target):
            total = 0
            for mu in range(4):
                for nu in range(mu+1, 4):
                    D = D_target if (mu,nu) == target_pair else np.eye(3)
                    p = T[mu] - R[mu] @ T[nu]
                    v = T[mu] - R[nu].T @ T[nu]
                    total += np.dot(p, p) + np.dot(v, v) + 2 * p @ (R[mu] @ D @ v)
            return total

        F1 = F_affine(D1)
        F2 = F_affine(D2)
        F_mix = F_affine(alpha * D1 + (1 - alpha) * D2)
        expected = alpha * F1 + (1 - alpha) * F2

        err = abs(F_mix - expected)
        max_err = max(max_err, err)

    print(f"  Max interpolation error: {max_err:.2e} (should be < 1e-10)")
    print(f"  Status: {'VERIFIED' if max_err < 1e-10 else 'FAILED'}")
    return max_err < 1e-10

if __name__ == "__main__":
    r1 = test_affine_identity()
    r2 = test_affine_sum()
    r3 = test_affine_via_linearity()
    print(f"\nOverall B6: {'VERIFIED' if r1 and r2 and r3 else 'FAILED'}")
