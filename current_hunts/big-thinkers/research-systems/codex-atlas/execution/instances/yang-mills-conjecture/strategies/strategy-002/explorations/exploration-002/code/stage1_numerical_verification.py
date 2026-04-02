"""
Stage 1: Numerical Verification of Gap Decomposition for General T.

Gap = 16||T||^2 - F_x = f_same + cross
- f_same = 2 sum_{mu<nu} [f(U_munu, T_mu) + f(W_munu, T_nu)]  >= 0 always
- cross = -2 sum_{mu<nu} T_mu^T C_munu T_nu  (can be positive or negative)
- C_munu = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-R_mu D R_nu^T)

Verified formula: 4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U, T_mu) + 2f(W, T_nu) - 2 T_mu^T C T_nu

Task: 200 Q configs, 20 T each + gradient-optimized T.
Report max |cross|/f_same when cross < 0.
"""

import numpy as np

np.random.seed(42)
d = 4
PLANES = [(mu, nu) for mu in range(d) for nu in range(mu+1, d)]

# ============================================================
# Core functions
# ============================================================

def random_so3():
    """Random SO(3) matrix via quaternion."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_exp(omega):
    """Exponential map for so(3) -> SO(3)."""
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def random_constrained_T():
    """Random T in R^{4x3} with sum_mu T_mu = 0."""
    T = np.random.randn(4, 3)
    mean = T.mean(axis=0)
    T -= mean  # project: now sum_mu T_mu = 0
    return T

def make_projector():
    """Construct 12x9 orthogonal projector onto V = {T : sum_mu T_mu = 0}."""
    # Basis: e_{mu,a} - e_{3,a} for mu=0,1,2, a=0,1,2 (9 vectors)
    V = np.zeros((12, 9))
    idx = 0
    for mu in range(3):
        for a in range(3):
            v = np.zeros(12)
            v[3*mu + a] = 1.0
            v[3*3 + a] = -1.0
            V[:, idx] = v
            idx += 1
    Q, _ = np.linalg.qr(V)
    return Q[:, :9]  # orthonormal basis for V

def compute_B(R, D, T, mu, nu):
    """B = (I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu"""
    U = R[mu] @ D[(mu, nu)]
    S = np.eye(3) + U
    Tmat = R[mu] + U @ R[nu].T
    return S @ T[mu] - Tmat @ T[nu]

def compute_F_x(R, D, T):
    """F_x = sum_{mu<nu} |B_{mu,nu}|^2"""
    total = 0.0
    for mu, nu in PLANES:
        B = compute_B(R, D, T, mu, nu)
        total += np.dot(B, B)
    return total

def f_vec(R, p):
    """f(R, p) = p^T (I - R) p >= 0 for R in SO(3)."""
    return np.dot(p, p) - np.dot(p, R @ p)

def compute_gap_decomposition(R, D, T):
    """Decompose gap = 16||T||^2 - F_x into f_same + cross."""
    F_x = compute_F_x(R, D, T)
    norm2 = np.sum(T**2)
    gap = 16 * norm2 - F_x

    f_same = 0.0
    cross = 0.0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu, nu)]
        W = D[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D[(mu,nu)].T) + (np.eye(3) - R[mu] @ D[(mu,nu)] @ R[nu].T)

        f_same += 2 * f_vec(U, T[mu]) + 2 * f_vec(W, T[nu])
        cross += -2 * T[mu] @ C @ T[nu]

    return gap, f_same, cross, F_x

def build_M12(R, D):
    """Build 12x12 matrix M_12 such that F_x = vec(T)^T M12 vec(T)."""
    M = np.zeros((12, 12))
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu, nu)]
        S = np.eye(3) + U  # coefficient of T_mu in B
        Tmat = R[mu] + U @ R[nu].T  # coefficient of T_nu in B
        # B = S T_mu - Tmat T_nu
        # |B|^2 = T_mu^T S^T S T_mu - 2 T_mu^T S^T Tmat T_nu + T_nu^T Tmat^T Tmat T_nu
        M[3*mu:3*(mu+1), 3*mu:3*(mu+1)] += S.T @ S
        M[3*nu:3*(nu+1), 3*nu:3*(nu+1)] += Tmat.T @ Tmat
        M[3*mu:3*(mu+1), 3*nu:3*(nu+1)] -= S.T @ Tmat
        M[3*nu:3*(nu+1), 3*mu:3*(mu+1)] -= Tmat.T @ S
    return M

def compute_lambda_max_constrained(R, D, P_V):
    """Compute max eigenvalue of M_12 restricted to V = {T: sum T_mu = 0}."""
    M = build_M12(R, D)
    M_r = P_V.T @ M @ P_V
    eigs = np.linalg.eigvalsh(M_r)
    return eigs[-1]

def gradient_ascent_T(R, D, P_V, n_steps=100):
    """Find T in V maximizing F_x / ||T||^2 by eigenvalue computation."""
    M = build_M12(R, D)
    M_r = P_V.T @ M @ P_V
    eigs, vecs = np.linalg.eigh(M_r)
    # Max eigenvalue direction
    v = P_V @ vecs[:, -1]
    T = v.reshape(4, 3)
    return T, eigs[-1]

# ============================================================
# STAGE 1A: Basic statistical tests
# ============================================================
print("=" * 70)
print("STAGE 1A: Basic Numerical Verification (200 Q, 20 T each)")
print("=" * 70)

P_V = make_projector()

N_Q = 200
N_T_per_Q = 20
N_T_adversarial = 1  # via eigenvalue

all_gaps = []
all_f_same = []
all_cross = []
all_lambda_max = []
all_cross_to_fsame_neg = []  # |cross|/f_same when cross < 0

gap_violations = 0
f_same_violations = 0

for q_idx in range(N_Q):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    # Random T tests
    for t_idx in range(N_T_per_Q):
        T = random_constrained_T()
        gap, f_same, cross, F_x = compute_gap_decomposition(R, D, T)

        all_gaps.append(gap)
        all_f_same.append(f_same)
        all_cross.append(cross)

        if gap < -1e-10:
            gap_violations += 1
        if f_same < -1e-10:
            f_same_violations += 1
        if cross < -1e-10 and f_same > 1e-10:
            all_cross_to_fsame_neg.append(abs(cross) / f_same)

    # Adversarial T via eigenvalue
    T_adv, lam = gradient_ascent_T(R, D, P_V)
    all_lambda_max.append(lam)

    # Verify gap decomposition for adversarial T
    gap, f_same, cross, F_x = compute_gap_decomposition(R, D, T_adv)
    if cross < -1e-10 and f_same > 1e-10:
        all_cross_to_fsame_neg.append(abs(cross) / f_same)

print(f"\n--- Random T Statistics ({N_Q} Q × {N_T_per_Q} T = {N_Q*N_T_per_Q} tests) ---")
print(f"  Gap violations (gap < 0): {gap_violations}")
print(f"  f_same violations (f_same < 0): {f_same_violations}")
print(f"  Min gap: {min(all_gaps):.6f}")
print(f"  Max gap: {max(all_gaps):.6f}")
print(f"  Mean gap: {np.mean(all_gaps):.4f}")
print(f"  Min f_same: {min(all_f_same):.6f}")
print(f"  Max cross (positive): {max(all_cross):.4f}")
print(f"  Min cross (negative): {min(all_cross):.4f}")

print(f"\n--- Cross-to-f_same Ratio (when cross < 0) ---")
if all_cross_to_fsame_neg:
    print(f"  N samples with cross < 0: {len(all_cross_to_fsame_neg)}")
    print(f"  Max |cross|/f_same: {max(all_cross_to_fsame_neg):.6f} (need < 1)")
    print(f"  Mean |cross|/f_same: {np.mean(all_cross_to_fsame_neg):.6f}")
    print(f"  Fraction > 0.082: {np.mean(np.array(all_cross_to_fsame_neg) > 0.082):.4f}")
else:
    print("  No samples with cross < 0 found")

print(f"\n--- Adversarial Lambda_max ({N_Q} Q configs) ---")
print(f"  Max lambda_max (constrained): {max(all_lambda_max):.6f}")
print(f"  Min lambda_max: {min(all_lambda_max):.6f}")
print(f"  Mean lambda_max: {np.mean(all_lambda_max):.4f}")
print(f"  Fraction above 15: {np.mean(np.array(all_lambda_max) > 15):.4f}")
print(f"  Fraction above 15.5: {np.mean(np.array(all_lambda_max) > 15.5):.4f}")

# ============================================================
# STAGE 1B: Gradient optimization for adversarial Q
# ============================================================
print("\n" + "=" * 70)
print("STAGE 1B: Gradient Optimization of Q (Adversarial Attack)")
print("=" * 70)

N_adversarial = 50
best_lam = 0.0
best_Q_record = None

for trial in range(N_adversarial):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    step = 0.03

    prev_lam = 0
    for iteration in range(300):
        lam = compute_lambda_max_constrained(R, D, P_V)

        if lam > best_lam:
            best_lam = lam
            best_Q_record = (iteration, trial, lam)

        # Gradient w.r.t. R[mu]
        eps = 1e-5
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = list(R); R_p[mu] = so3_exp(omega) @ R[mu]
                lam_p = compute_lambda_max_constrained(R_p, D, P_V)
                g = (lam_p - lam) / eps
                R[mu] = so3_exp(step * g * np.eye(3)[k]) @ R[mu]

        # Gradient w.r.t. D[p]
        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D); D_p[p] = so3_exp(omega) @ D[p]
                lam_p = compute_lambda_max_constrained(R, D_p, P_V)
                g = (lam_p - lam) / eps
                D[p] = so3_exp(step * g * np.eye(3)[k]) @ D[p]

        if iteration % 100 == 99:
            step *= 0.7

    if (trial + 1) % 10 == 0:
        print(f"  Trial {trial+1}/50, current best lambda_max = {best_lam:.6f}")

print(f"\n  BEST adversarial lambda_max = {best_lam:.6f} (need < 16)")
print(f"  Gap from 16: {16 - best_lam:.6f}")

# ============================================================
# STAGE 1C: Gradient optimization of T for fixed Q
# ============================================================
print("\n" + "=" * 70)
print("STAGE 1C: Maximize |cross|/f_same over T (fixed Q adversarial)")
print("=" * 70)

N_Q_cross = 100
max_cross_ratio_overall = 0.0

for q_idx in range(N_Q_cross):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    # Try many T
    best_ratio = 0
    for _ in range(200):
        T = random_constrained_T()
        gap, f_same, cross, F_x = compute_gap_decomposition(R, D, T)
        if cross < -1e-10 and f_same > 1e-10:
            ratio = abs(cross) / f_same
            if ratio > best_ratio:
                best_ratio = ratio

    # Gradient ascent on |cross|/f_same over T in V
    # Use 5 random restarts
    for restart in range(5):
        T = random_constrained_T()
        T = T / np.linalg.norm(T) if np.linalg.norm(T) > 1e-12 else T
        step_T = 0.05

        for _ in range(100):
            gap, f_same, cross, F_x = compute_gap_decomposition(R, D, T)
            if cross < 0 and f_same > 1e-12:
                ratio = abs(cross) / f_same
                if ratio > best_ratio:
                    best_ratio = ratio

            # Gradient via finite differences
            eps = 1e-5
            grad_T = np.zeros_like(T)
            for mu_g in range(4):
                for a_g in range(3):
                    T_p = T.copy(); T_p[mu_g, a_g] += eps
                    T_p -= T_p.mean(axis=0)  # maintain constraint
                    _, fs_p, cr_p, _ = compute_gap_decomposition(R, D, T_p)

                    if cross < 0 and f_same > 1e-12 and fs_p > 1e-12:
                        # Objective: |cross| / f_same (maximize when cross < 0)
                        obj_p = abs(cr_p) / fs_p if cr_p < 0 else 0
                        obj_c = abs(cross) / f_same if cross < 0 else 0
                        grad_T[mu_g, a_g] = (obj_p - obj_c) / eps

            T = T + step_T * grad_T
            T -= T.mean(axis=0)  # maintain constraint
            n = np.linalg.norm(T)
            if n > 1e-12:
                T /= n

    if best_ratio > max_cross_ratio_overall:
        max_cross_ratio_overall = best_ratio

    if (q_idx + 1) % 25 == 0:
        print(f"  Q {q_idx+1}/100, running max |cross|/f_same = {max_cross_ratio_overall:.6f}")

print(f"\n  MAX |cross|/f_same across all tests = {max_cross_ratio_overall:.6f}")
print(f"  Previous bound (E008): 0.082")
print(f"  Gap from 1: {1 - max_cross_ratio_overall:.4f}")

# ============================================================
# STAGE 1D: Verify expansion identity
# ============================================================
print("\n" + "=" * 70)
print("STAGE 1D: Verify per-plaquette expansion identity")
print("=" * 70)
# Verify: 4|T_mu-T_nu|^2 - |B|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C T_nu

max_err = 0
for _ in range(50000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    for mu, nu in PLANES:
        B = compute_B(R, D, T, mu, nu)
        lhs = 4 * np.sum((T[mu] - T[nu])**2) - np.dot(B, B)

        U = R[mu] @ D[(mu, nu)]
        W = D[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D[(mu,nu)].T) + (np.eye(3) - R[mu] @ D[(mu,nu)] @ R[nu].T)

        rhs = 2*f_vec(U, T[mu]) + 2*f_vec(W, T[nu]) - 2 * T[mu] @ C @ T[nu]

        err = abs(lhs - rhs)
        max_err = max(max_err, err)

print(f"  Max identity error: {max_err:.2e} (need < 1e-10)")
print(f"  Identity VERIFIED: {max_err < 1e-10}")

print("\n=== STAGE 1 COMPLETE ===")
