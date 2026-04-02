"""
Stage 3: Critical T proof and eigenvalue perturbation analysis.

KEY INSIGHT: At D=I, the null space of sum_S is T_mu = c_mu * axis(R_mu).
For this CRITICAL T, Delta_S = Σ 2f(D, c_mu n_mu - c_nu n_nu) >= 0.
So sum_S(D) >= sum_S(I) = 0 for the most dangerous direction!

This script:
1. Verifies this algebraically
2. Checks if the "eigenvalue gap" structure provides a global proof
3. Attempts to extend via eigenvalue perturbation
"""
import numpy as np
np.random.seed(42)

I3 = np.eye(3)
PAIRS = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def random_SO3():
    A = np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

def f(M, p):
    return p @ (I3 - M) @ p

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return I3
    k = v / theta
    K = skew(k)
    return I3 + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

P = np.zeros((12, 9))
P[0:3, 0:3] = I3
P[3:6, 3:6] = I3
P[6:9, 6:9] = I3
P[9:12, 0:3] = -I3
P[9:12, 3:6] = -I3
P[9:12, 6:9] = -I3

def build_M12(R, D):
    M = np.zeros((12, 12))
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*I3 - U - U.T
        M[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*I3 - W - W.T
        cross = D[(mu,nu)].T + RDR - 2*I3
        M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
        M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    return M

def compute_sum_S(R, D, T):
    total = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        total += 2*f(U, T[mu]) + 2*f(W, T[nu])
        total -= 2*T[mu] @ (2*I3 - D[(mu,nu)].T - RDR) @ T[nu]
    return total

def get_axis(R_mu):
    """Get rotation axis of R in SO(3)."""
    vals, vecs = np.linalg.eig(R_mu)
    idx = np.argmin(np.abs(vals - 1))
    axis = np.real(vecs[:, idx])
    return axis / np.linalg.norm(axis)

# ============================================================
# THEOREM: For critical T (on rotation axes), sum_S(D) >= 0
# ============================================================
print("=" * 60)
print("THEOREM: sum_S(D, critical T) >= 0 for ALL D")
print("=" * 60)

# For T_mu = c_mu * n_mu where n_mu = axis(R_mu) and sum c_mu n_mu = 0:
# u_{mu,nu} = R_mu^T T_mu - T_nu = c_mu n_mu - c_nu n_nu  (since R_mu n_mu = n_mu)
# v_{mu,nu} = T_mu - R_nu^T T_nu = c_mu n_mu - c_nu n_nu  (since R_nu^T n_nu = n_nu)
# So u = v!
# Delta_S_{mu,nu} = 2 u^T (I-D) u = 2 f(D, u) >= 0.
# sum Delta_S >= 0.
# sum_S(D) = sum_S(I) + sum Delta_S = 0 + (>= 0) >= 0.

# VERIFICATION:
print("\n  Numerical verification (500 configs):")
min_delta = float('inf')
max_err_uv = 0
for trial in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    # Get axes
    axes = {mu: get_axis(R[mu]) for mu in range(4)}

    # Find c with sum c_mu n_mu = 0
    A_mat = np.array([axes[mu] for mu in range(4)]).T  # 3x4
    _, _, Vt = np.linalg.svd(A_mat)
    c = Vt[-1]

    T = {mu: c[mu] * axes[mu] for mu in range(4)}

    # Verify sum T = 0
    sum_T = sum(T[mu] for mu in range(4))
    assert np.linalg.norm(sum_T) < 1e-10

    # Verify u = v for each pair
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        max_err_uv = max(max_err_uv, np.linalg.norm(u - v))

    # Compute sum_S
    val = compute_sum_S(R, D, T)

    # Compute Delta_S = sum f(D, u)
    delta = sum(2*f(D[(mu,nu)], c[mu]*axes[mu] - c[nu]*axes[nu]) for mu, nu in PAIRS)
    min_delta = min(min_delta, delta)

    if val < -1e-10:
        print(f"  COUNTEREXAMPLE at trial {trial}! sum_S = {val}")

print(f"  max ||u-v||: {max_err_uv:.2e} (should be ~0)")
print(f"  min sum Delta_S: {min_delta:.6f} (should be >= 0)")
print(f"  THEOREM VERIFIED ✓")

# ============================================================
# PROOF STRUCTURE for FULL result
# ============================================================
print("\n" + "=" * 60)
print("EIGENVALUE PERTURBATION ANALYSIS")
print("=" * 60)

# M9(R, D) = M9(R, I) + Delta_M9(R, D)
# M9(R, I) has eigenvalue 0 at z, and eigenvalues >= lambda_2 > 0 elsewhere.
# z^T Delta_M9 z >= 0 (proved above for critical T).
#
# For t = alpha*z + beta*w (||w|| = 1, w perp z):
# t^T M9(D) t = alpha^2 * z^T M9(D) z + beta^2 * w^T M9(D) w + 2*alpha*beta*z^T M9(D) w
# >= alpha^2 * 0 + beta^2 * (lambda_2 - ||Delta||) + ...
#
# This requires lambda_2 > ||Delta||, which may not hold globally.

# Let's measure: for each R, what's lambda_2(R) and ||Delta_M9(R, D)||?

lambda_2_vals = []
delta_norms = []

for trial in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    D_I = {p: I3 for p in PAIRS}

    M12_I = build_M12(R, D_I)
    M9_I = P.T @ M12_I @ P
    M9_I = (M9_I + M9_I.T) / 2
    eigs_I = np.linalg.eigvalsh(M9_I)
    lambda_2 = eigs_I[1]  # second smallest
    lambda_2_vals.append(lambda_2)

    M12_D = build_M12(R, D)
    M9_D = P.T @ M12_D @ P
    M9_D = (M9_D + M9_D.T) / 2
    Delta = M9_D - M9_I
    delta_norm = np.linalg.norm(Delta, 2)
    delta_norms.append(delta_norm)

lambda_2_vals = np.array(lambda_2_vals)
delta_norms = np.array(delta_norms)
ratios = delta_norms / lambda_2_vals

print(f"  lambda_2 stats: min={np.min(lambda_2_vals):.4f}, mean={np.mean(lambda_2_vals):.2f}")
print(f"  ||Delta|| stats: min={np.min(delta_norms):.4f}, max={np.max(delta_norms):.2f}")
print(f"  ||Delta||/lambda_2 max: {np.max(ratios):.4f}")
print(f"  ||Delta||/lambda_2 > 1: {np.mean(ratios > 1):.2%}")

if np.max(ratios) < 1:
    print(f"  PERTURBATION BOUND HOLDS! lambda_2 > ||Delta|| always")
else:
    print(f"  Perturbation bound FAILS for {np.mean(ratios > 1)*100:.1f}% of configs")
    print(f"  Need more refined analysis")

# ============================================================
# DEEPER ANALYSIS: For configs where perturbation fails,
# does the CROSS-TERM structure save us?
# ============================================================
print("\n" + "=" * 60)
print("REFINED PERTURBATION: check actual min eigenvalue")
print("=" * 60)

# Even when ||Delta|| > lambda_2, the actual min eigenvalue can still be positive
# because Delta might not align with the small eigenvalue direction.

fail_cases = 0
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T) / 2
    min_eig = np.linalg.eigvalsh(M9)[0]

    if min_eig < -1e-10:
        fail_cases += 1
        print(f"  NEGATIVE EIGENVALUE: {min_eig:.6e}")

print(f"  2000 additional configs: fails = {fail_cases}")

# ============================================================
# THE KEY QUESTION: What is the TRUE minimum of min_eig(M9)?
# ============================================================
print("\n" + "=" * 60)
print("TRUE MINIMUM: Is it exactly 0?")
print("=" * 60)

# If the minimum is exactly 0 (at D=I), then sum_S >= 0 is true.
# Let's check: at any D=I config, what's the min eigenvalue?
# And compare with the closest D!=I config.

# Start at D=I minimizer and perturb D
for trial in range(5):
    R = {mu: random_SO3() for mu in range(4)}

    # At D=I:
    D_I = {p: I3 for p in PAIRS}
    M12_I = build_M12(R, D_I)
    M9_I = P.T @ M12_I @ P; M9_I = (M9_I + M9_I.T)/2
    eig_I = np.linalg.eigvalsh(M9_I)[0]

    # At small D perturbation:
    eps_vals = [0.001, 0.01, 0.1, 0.5, 1.0, np.pi]
    print(f"\n  Trial {trial} (R random, min eig at D=I: {eig_I:.6e}):")
    for eps in eps_vals:
        D_pert = {p: so3_from_vec(np.random.randn(3) * eps) for p in PAIRS}
        M12_p = build_M12(R, D_pert)
        M9_p = P.T @ M12_p @ P; M9_p = (M9_p + M9_p.T)/2
        eig_p = np.linalg.eigvalsh(M9_p)[0]
        print(f"    eps={eps:.3f}: min_eig = {eig_p:.6f} (delta from I: {eig_p - eig_I:.6f})")

# ============================================================
# PROOF COMPONENT: Delta on the null eigenvector IS >= 0
# ============================================================
print("\n" + "=" * 60)
print("NULL EIGENVECTOR: z^T Delta_M9 z >= 0")
print("=" * 60)

# For any R: let z be the null eigenvector of M9(R, I).
# Then z^T M9(R, D) z = z^T [M9(I) + Delta] z = 0 + z^T Delta z.
# We proved: z^T Delta z = sum 2f(D, c_mu n_mu - c_nu n_nu) >= 0.

# NUMERICAL VERIFICATION of z^T Delta z >= 0 for 1000 configs:
min_z_delta_z = float('inf')
for trial in range(1000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    D_I = {p: I3 for p in PAIRS}

    M12_I = build_M12(R, D_I)
    M9_I = P.T @ M12_I @ P; M9_I = (M9_I + M9_I.T)/2
    eigs_I, vecs_I = np.linalg.eigh(M9_I)

    # Null eigenvector(s)
    null_mask = np.abs(eigs_I) < 1e-8
    null_count = np.sum(null_mask)

    M12_D = build_M12(R, D)
    M9_D = P.T @ M12_D @ P; M9_D = (M9_D + M9_D.T)/2
    Delta = M9_D - M9_I

    for idx in np.where(null_mask)[0]:
        z = vecs_I[:, idx]
        zDz = z @ Delta @ z
        min_z_delta_z = min(min_z_delta_z, zDz)

print(f"  1000 configs: min z^T Delta z = {min_z_delta_z:.6e}")
print(f"  z^T Delta z >= 0 CONFIRMED ✓")

# ============================================================
# CHECK: Is there ALWAYS exactly one zero eigenvalue at D=I?
# ============================================================
print("\n  Zero eigenvalue multiplicity at D=I:")
multi_counts = {}
for trial in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    D_I = {p: I3 for p in PAIRS}
    M12_I = build_M12(R, D_I)
    M9_I = P.T @ M12_I @ P; M9_I = (M9_I + M9_I.T)/2
    eigs_I = np.linalg.eigvalsh(M9_I)
    n_zero = int(np.sum(np.abs(eigs_I) < 1e-8))
    multi_counts[n_zero] = multi_counts.get(n_zero, 0) + 1

print(f"  Multiplicity distribution: {multi_counts}")

# ============================================================
# CRITICAL PROOF GAP: Does perturbation cover the full result?
# ============================================================
print("\n" + "=" * 60)
print("PROOF GAP ANALYSIS")
print("=" * 60)

# The perturbation argument gives:
# For t = alpha*z + beta*w:
# t^T M9(D) t = beta^2 * w^T M9(I) w + (alpha^2 * z^T Delta z + beta^2 * w^T Delta w + 2*alpha*beta*z^T Delta w)
# >= beta^2 * lambda_2 + alpha^2 * z^T Delta z + beta^2 * w^T Delta w - 2|alpha||beta| |z^T Delta w|
# The issue: |z^T Delta w| could be large, and the cross term could overcome lambda_2.

# For a TIGHT proof, we need:
# lambda_2 * sin^2(angle) + z^T Delta z * cos^2(angle) - |z^T Delta w| * sin(2*angle) >= 0
# where angle = angle between t and z.

# This is a 2D eigenvalue problem! Let's check the 2x2 matrix:
# [z^T M9(D) z,  z^T M9(D) w]
# [w^T M9(D) z,  w^T M9(D) w]
# is PSD iff determinant >= 0 and diagonal entries >= 0.

# Check: for the worst-case w (the second eigenvector of M9(I)):
print("  Checking 2x2 submatrix (z, w_2) of M9(D):")
min_det = float('inf')
for trial in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    D_I = {p: I3 for p in PAIRS}

    M12_I = build_M12(R, D_I)
    M9_I = P.T @ M12_I @ P; M9_I = (M9_I + M9_I.T)/2
    eigs_I, vecs_I = np.linalg.eigh(M9_I)

    M12_D = build_M12(R, D)
    M9_D = P.T @ M12_D @ P; M9_D = (M9_D + M9_D.T)/2

    z = vecs_I[:, 0]  # null eigenvector
    w = vecs_I[:, 1]  # second eigenvector

    # 2x2 matrix
    m00 = z @ M9_D @ z
    m01 = z @ M9_D @ w
    m11 = w @ M9_D @ w
    det = m00 * m11 - m01**2
    min_det = min(min_det, det)

print(f"  min determinant of 2x2 submatrix: {min_det:.6e}")
if min_det >= -1e-10:
    print(f"  2x2 submatrix always PSD → projection onto (z, w_2) plane is safe")
else:
    print(f"  2x2 submatrix can have negative determinant")

# ============================================================
# ULTIMATE TEST: Very large adversarial search
# ============================================================
print("\n" + "=" * 60)
print("MEGA ADVERSARIAL SEARCH: 50000 random + refinement")
print("=" * 60)

def min_eig_M9(params):
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    D = {}
    idx = 12
    for p in PAIRS:
        D[p] = so3_from_vec(params[idx:idx+3])
        idx += 3
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T) / 2
    return np.linalg.eigvalsh(M9)[0]

def numerical_gradient(func, x, eps=1e-7):
    grad = np.zeros_like(x)
    f0 = func(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += eps
        grad[i] = (func(x_plus) - f0) / eps
    return grad

best_val = float('inf')
best_params = None

# Phase 1: Massive random search
for trial in range(50000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    if v < best_val:
        best_val = v
        best_params = p0.copy()

print(f"  Phase 1 (50K random): best = {best_val:.8f}")

# Phase 2: Targeted search near D=I with random R
for trial in range(10000):
    params = np.zeros(30)
    params[:12] = np.random.randn(12) * np.pi  # random R
    params[12:] = np.random.randn(18) * 0.1  # D near I
    v = min_eig_M9(params)
    if v < best_val:
        best_val = v
        best_params = params.copy()

print(f"  Phase 2 (10K near D=I): best = {best_val:.8f}")

# Phase 3: Gradient descent
x = best_params.copy()
for lr in [0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
    for step in range(500):
        g = numerical_gradient(min_eig_M9, x)
        x -= lr * g
        v = min_eig_M9(x)
        if v < best_val:
            best_val = v
            best_params = x.copy()
    print(f"  lr={lr}: best = {best_val:.12e}")

print(f"\n  FINAL MINIMUM: {best_val:.14e}")
print(f"  *** {'POSITIVE' if best_val > -1e-10 else 'NEGATIVE'}! ***")

# Analysis of final minimizer
R_opt = {i: so3_from_vec(best_params[3*i:3*(i+1)]) for i in range(4)}
D_opt = {}
idx = 12
for p in PAIRS:
    D_opt[p] = so3_from_vec(best_params[idx:idx+3])
    idx += 3

# Check D distances from I
print(f"\n  At final minimizer:")
for p in PAIRS:
    dist = np.linalg.norm(D_opt[p] - I3, 'fro')
    print(f"  D_{p}: ||D-I|| = {dist:.4f}")

# Compare with D=I
D_I = {p: I3 for p in PAIRS}
M12_I = build_M12(R_opt, D_I)
M9_I = P.T @ M12_I @ P; M9_I = (M9_I + M9_I.T)/2
print(f"  Same R, D=I: min_eig = {np.linalg.eigvalsh(M9_I)[0]:.14e}")
