"""
Stage 3: Proof attempt for lambda_max(M_total) <= 64.

KEY REDUCTION (from Stage 2):
  M_total = c*I + P  where c + Tr(P) = 64 (algebraic identity).
  lambda_max(M) <= 64  iff  lambda_max(P) <= Tr(P)
                       iff  lambda_mid(P) + lambda_min(P) >= 0.

APPROACH:
1. Verify the trace identity algebraically
2. Adversarial search for tightest case of lambda_mid + lambda_min
3. Analyze the D=I case analytically
4. Attempt proof via the "pairing" of cross-term types
"""

import numpy as np
from itertools import combinations

np.random.seed(42)

# ============================================================
# SO(3) utilities
# ============================================================

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def so3_log(R):
    tr = np.clip((np.trace(R) - 1) / 2, -1, 1)
    angle = np.arccos(tr)
    if angle < 1e-10:
        return np.zeros(3)
    axis = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]]) / (2*np.sin(angle))
    return angle * axis

PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]
ACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu) % 2 == 1]
INACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu) % 2 == 0]

def compute_A(mu, nu, R, D):
    a = (-1)**mu
    b = (-1)**(nu+1)
    S = np.eye(3) + R[mu] @ D[(mu,nu)]
    T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
    return a * S + b * T

def compute_M_total(R, D):
    M = np.zeros((3, 3))
    for mu, nu in PLANES:
        A = compute_A(mu, nu, R, D)
        M += A.T @ A
    return M

def flatten(R, D):
    params = []
    for mu in range(4):
        params.extend(so3_log(R[mu]))
    for p in PLANES:
        params.extend(so3_log(D[p]))
    return np.array(params)

def unflatten(params):
    R = [so3_exp(params[3*i:3*i+3]) for i in range(4)]
    D = {p: so3_exp(params[12+3*i:12+3*i+3]) for i, p in enumerate(PLANES)}
    return R, D

# ============================================================
# Part 3a: PROVE the trace identity c + Tr(P) = 64
# ============================================================

print("=" * 70)
print("PART 3a: Algebraic verification of c + Tr(P) = 64")
print("=" * 70)

# The identity is: Sigma_k sigma_k = 20
# where we have 6 plaquettes, each with C(4,2)=6 cross terms = 36 terms total.
# Active plaquettes: 4, each with 6 positive terms = 24 positive
# Inactive plaquettes: 2, each with 2 positive and 4 negative = 4+(-8) = -4
# Total: 24 + (-4) = 20

# Let's verify by enumeration
total_sigma = 0
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    signs = [a, a, b, b]
    for i in range(4):
        for j in range(i+1, 4):
            sigma = signs[i] * signs[j]
            total_sigma += sigma

print(f"Sum of all sigma_k = {total_sigma}")
print(f"c + Tr(P) = 24 + 2*{total_sigma} = {24 + 2*total_sigma}")
print(f"This equals 64: {24 + 2*total_sigma == 64}")
print()

# Break down by plaquette
print("Per-plaquette sigma sums:")
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    signs = [a, a, b, b]
    plaq_sigma = sum(signs[i]*signs[j] for i in range(4) for j in range(i+1,4))
    ptype = "active" if (mu+nu)%2==1 else "inactive"
    print(f"  ({mu},{nu}) [{ptype}]: sum(sigma) = {plaq_sigma}  (a={a:+d}, b={b:+d})")

print(f"\nActive total: {sum(6 for _ in ACTIVE)} = {4*6}")
print(f"Inactive total: {sum(-2 for _ in INACTIVE)} = {2*(-2)}")
print(f"Grand total: {4*6 + 2*(-2)} = {24 - 4} = 20  ✓")

# ============================================================
# Part 3b: The D=I case - analytical formula
# ============================================================

print("\n" + "=" * 70)
print("PART 3b: Analytical formula for D=I case")
print("=" * 70)

# When D = I:
# Active (a=b=s): A = s(I + 2R_mu + R_mu R_nu^T)
# Inactive (a=-b): A = a(I - R_mu R_nu^T)
#
# So for D=I, the ONLY rotations that matter are R_mu and R_mu R_nu^T

# Test: compute M_total for D=I in two ways
print("Verifying D=I formula:")
for trial in range(10):
    R = [random_so3() for _ in range(4)]
    D_I = {p: np.eye(3) for p in PLANES}

    M_direct = compute_M_total(R, D_I)

    # Formula for D=I
    M_formula = np.zeros((3, 3))

    for mu, nu in ACTIVE:
        # A = s(I + 2R_mu + R_mu R_nu^T), s = ±1
        # A^T A = (I + 2R_mu + R_mu R_nu^T)^T (I + 2R_mu + R_mu R_nu^T)
        S = np.eye(3) + 2*R[mu] + R[mu] @ R[nu].T
        M_formula += S.T @ S

    for mu, nu in INACTIVE:
        # A = a(I - R_mu R_nu^T)
        # A^T A = (I - R_mu R_nu^T)^T (I - R_mu R_nu^T) = (I-R_nu R_mu^T)(I-R_mu R_nu^T)
        S = np.eye(3) - R[mu] @ R[nu].T
        M_formula += S.T @ S

    err = np.max(np.abs(M_direct - M_formula))
    if trial < 3:
        print(f"  Trial {trial}: max error = {err:.2e}")

# ============================================================
# Part 3c: The D=I active contribution
# ============================================================

print("\n" + "=" * 70)
print("PART 3c: Active contribution for D=I")
print("=" * 70)

# For one active plaquette with D=I:
# ||An||^2 = |n + 2R_mu n + R_mu R_nu^T n|^2
# = 1 + 4 + 1 + 4 n·R_mu n + 2 n·R_mu R_nu^T n + 4 (R_mu n)·(R_mu R_nu^T n)
# = 6 + 4 n^T R_mu n + 2 n^T R_mu R_nu^T n + 4 n^T R_nu^T n
# = 6 + 4 n^T R_mu n + 2 n^T R_mu R_nu^T n + 4 n^T R_nu n
#
# (Using: n^T R_mu^T R_mu R_nu^T n = n^T R_nu^T n since R_mu^T R_mu = I,
#  and (R_mu n)·(R_mu R_nu^T n) = n^T R_nu^T n)
#
# So ||An||^2 = 6 + 4(n^T R_mu n + n^T R_nu n) + 2 n^T R_mu R_nu^T n

# For one inactive plaquette with D=I:
# ||An||^2 = |(I - R_mu R_nu^T)n|^2 = 2 - 2 n^T R_mu R_nu^T n
# (Using n^T R_nu R_mu^T R_mu R_nu^T n = 1)

# Total F_x = sum over 4 active + 2 inactive:
# = 4*6 + 4*sum_{active} [4(n^T R_mu n + n^T R_nu n) + 2 n^T R_mu R_nu^T n]
#   + 2*sum_{inactive} [2 - 2 n^T R_mu R_nu^T n]
#
# Wait, I need to be more careful about which R_mu appears in which plaquette.

# Let me compute the coefficient of n^T R_mu n for each mu:
print("Computing coefficient structure for D=I case...")

# For D=I, the cross-term expansion:
# F_x = 24 + 2*sum_{k} sigma_k * n^T O_k n
#
# The 36 cross-term rotations simplify when D=I:
# For plaquette (mu,nu), the 4 "vectors" are:
# v1 = n, v2 = R_mu n, v3 = R_mu n, v4 = R_mu R_nu^T n
#
# Cross terms:
# (1,2): R_mu,  sigma * n^T R_mu n
# (1,3): R_mu,  sigma * n^T R_mu n
# (1,4): R_mu R_nu^T, sigma * n^T R_mu R_nu^T n
# (2,3): I,     sigma * 1
# (2,4): R_nu^T, sigma * n^T R_nu n
# (3,4): R_nu^T, sigma * n^T R_nu n

# Wait, (2,3): Q_2^T Q_3 = (R_mu D)^T R_mu = D^T = I when D=I. So O_{23} = I!
# And (2,4): (R_mu D)^T (R_mu D R_nu^T) = D^T D R_nu^T = R_nu^T when D=I.
# And (3,4): R_mu^T (R_mu D R_nu^T) = D R_nu^T = R_nu^T when D=I.

# So for D=I, cross terms per plaquette:
# (1,2) -> R_mu, sigma
# (1,3) -> R_mu, sigma
# (1,4) -> R_mu R_nu^T, sigma
# (2,3) -> I, sigma (constant!)
# (2,4) -> R_nu^T, sigma
# (3,4) -> R_nu^T, sigma

# This means each plaquette contributes:
# 2*sigma*(2 n^T R_mu n + 2 n^T R_nu n + n^T R_mu R_nu^T n + 1)

# Verify
for trial in range(5):
    R = [random_so3() for _ in range(4)]
    D_I = {p: np.eye(3) for p in PLANES}
    n = np.random.randn(3); n /= np.linalg.norm(n)

    # Direct
    M = compute_M_total(R, D_I)
    Fx_direct = n @ M @ n

    # Formula
    Fx_formula = 24.0
    for mu, nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        signs = [a, a, b, b]

        # sigma for each cross term pair
        pairs_sigmas = [
            (signs[0]*signs[1], R[mu]),               # (1,2) -> R_mu
            (signs[0]*signs[2], R[mu]),               # (1,3) -> R_mu
            (signs[0]*signs[3], R[mu] @ R[nu].T),    # (1,4) -> R_mu R_nu^T
            (signs[1]*signs[2], np.eye(3)),           # (2,3) -> I
            (signs[1]*signs[3], R[nu].T),             # (2,4) -> R_nu^T
            (signs[2]*signs[3], R[nu].T),             # (3,4) -> R_nu^T
        ]

        for sigma, O in pairs_sigmas:
            Fx_formula += 2 * sigma * (n @ O @ n)

    err = abs(Fx_direct - Fx_formula)
    if trial < 3:
        print(f"  Trial {trial}: error = {err:.2e}")

# ============================================================
# Part 3d: Simplified D=I formula
# ============================================================

print("\n" + "=" * 70)
print("PART 3d: Simplified D=I formula")
print("=" * 70)

# For D=I, collecting all cross terms, the coefficient of n^T R_mu n:
# R_mu appears in:
# - Type (1,2) and (1,3) of plaquettes where mu is the first index
# - NOT in Type (2,4) or (3,4) [those give R_nu]
#
# Plaquettes with mu as first index:
#   (mu, nu) for all nu > mu
#
# For each such plaquette, Types (1,2) and (1,3) each contribute sigma_12 and sigma_13.
# For active: sigma_12 = a^2 = 1, sigma_13 = ab = 1.
# For inactive: sigma_12 = a^2 = 1, sigma_13 = ab = -1.
#
# So n^T R_mu n coefficient from Type A (1,3) and Type (1,2):
#   sum over (mu,nu): (sigma_12 + sigma_13) = 2 for active, 0 for inactive

# Also, R_mu appears via n^T R_mu R_nu^T n terms (Type E = (1,4)):
# For each (mu, nu): sigma_14 = ab for active = 1, ab for inactive = -1.

# And R_nu appears via Type B (2,4) and (3,4):
# For each (mu, nu): sigma_24 and sigma_34.
# Active: both = 1. Inactive: sigma_24 = ab = -1, sigma_34 = b^2 = 1.

# Plus the constant term from Type D (2,3): sigma_23 = a^2 or ab.
# Active: a^2 = 1. Inactive: ab = -1.

# Let me compute the TOTAL F_x formula for D=I by collecting:

# F_x = 24 + 2*[constant terms] + 2*[R_mu terms] + 2*[R_nu terms] + 2*[R_mu R_nu^T terms]

# Constant terms (from (2,3) -> I):
const_sum = 0
for mu, nu in PLANES:
    a = (-1)**mu; b = (-1)**(nu+1)
    sigma_23 = a * b  # signs[1]*signs[2] = a*b
    const_sum += sigma_23

print(f"Constant term sum: {const_sum}")
# For active: ab = 1 (since a=b). 4 active: 4.
# For inactive: ab = -1. 2 inactive: -2.
# Total: 2. So constant contribution: 2*2 = 4.

# n^T R_mu n terms: coefficient for each mu
print("\nCoefficients of n^T R_mu n:")
for target_mu in range(4):
    coeff = 0
    for mu, nu in PLANES:
        a = (-1)**mu; b = (-1)**(nu+1)
        signs = [a, a, b, b]

        if mu == target_mu:
            # Types (1,2) and (1,3) give R_mu
            coeff += signs[0]*signs[1] + signs[0]*signs[2]

    # Also Type B appearances: R_nu^T where nu = target_mu
    for mu, nu in PLANES:
        a = (-1)**mu; b = (-1)**(nu+1)
        signs = [a, a, b, b]

        if nu == target_mu:
            # Types (2,4) and (3,4) give R_nu^T, and n^T R_nu^T n = n^T R_nu n
            coeff += signs[1]*signs[3] + signs[2]*signs[3]

    print(f"  R_{target_mu}: coeff = {coeff}")

# n^T R_mu R_nu^T n terms: coefficient for each (mu,nu) pair
print("\nCoefficients of n^T R_mu R_nu^T n:")
for mu, nu in PLANES:
    a = (-1)**mu; b = (-1)**(nu+1)
    signs = [a, a, b, b]
    coeff = signs[0] * signs[3]  # Type (1,4) -> R_mu R_nu^T
    ptype = "active" if (mu+nu)%2==1 else "inactive"
    print(f"  R_{mu} R_{nu}^T ({ptype}): coeff = {coeff}")

# So the complete D=I formula:
# F_x(n) = 24 + 2*2 + 2*sum_mu c_mu * n^T R_mu n + 2*sum_{mu<nu} d_{mu,nu} * n^T R_mu R_nu^T n

# Let me verify this formula
print("\nVerifying simplified D=I formula:")
for trial in range(10):
    R = [random_so3() for _ in range(4)]
    D_I = {p: np.eye(3) for p in PLANES}
    n = np.random.randn(3); n /= np.linalg.norm(n)

    Fx_direct = n @ compute_M_total(R, D_I) @ n

    # Simplified formula
    Fx_simp = 28.0  # 24 + 2*2

    # R_mu coefficients (computed above: all equal to 4)
    # Actually let me compute them:
    r_coeffs = {}
    for target_mu in range(4):
        coeff = 0
        for mu, nu in PLANES:
            a = (-1)**mu; b = (-1)**(nu+1)
            signs = [a, a, b, b]
            if mu == target_mu:
                coeff += signs[0]*signs[1] + signs[0]*signs[2]
            if nu == target_mu:
                coeff += signs[1]*signs[3] + signs[2]*signs[3]
        r_coeffs[target_mu] = coeff

    for mu in range(4):
        Fx_simp += 2 * r_coeffs[mu] * (n @ R[mu] @ n)

    # R_mu R_nu^T coefficients
    for mu, nu in PLANES:
        a = (-1)**mu; b = (-1)**(nu+1)
        signs = [a, a, b, b]
        d_coeff = signs[0] * signs[3]
        Fx_simp += 2 * d_coeff * (n @ R[mu] @ R[nu].T @ n)

    err = abs(Fx_direct - Fx_simp)
    if trial < 5:
        print(f"  Trial {trial}: error = {err:.2e}, Fx = {Fx_direct:.4f}")

# ============================================================
# Part 3e: Adversarial on -(lambda_mid + lambda_min) of P
# ============================================================

print("\n" + "=" * 70)
print("PART 3e: Adversarial minimization of lambda_mid(P) + lambda_min(P)")
print("=" * 70)

def compute_P_eigs(R, D):
    """Compute eigenvalues of P = M - c*I where c + Tr(P) = 64."""
    M = compute_M_total(R, D)
    eigs_M = np.sort(np.linalg.eigvalsh(M))
    tr_M = sum(eigs_M)
    c = (tr_M - 64) / 2  # Since tr_M = 2c + 64 (from the identity)
    # Wait: Tr(M) = 3c + Tr(P) and c + Tr(P) = 64, so Tr(P) = 64-c and Tr(M) = 3c + 64-c = 2c+64
    # So c = (Tr(M) - 64)/2
    eigs_P = eigs_M - c
    return eigs_P, c

# The key condition: eigs_P[0] + eigs_P[1] >= 0 (the two smallest eigenvalues of P)
# This is equivalent to: lambda_max(P) <= Tr(P) = 64-c

def objective_min_sum_low_eigs(params):
    """Minimize lambda_mid(P) + lambda_min(P). Want to show this is >= 0."""
    R, D = unflatten(params)
    eigs_P, c = compute_P_eigs(R, D)
    return eigs_P[0] + eigs_P[1]  # minimize this (want to show >= 0)

def gradient_min_sum(params, eps=1e-6):
    f0 = objective_min_sum_low_eigs(params)
    grad = np.zeros_like(params)
    for i in range(len(params)):
        p_plus = params.copy()
        p_plus[i] += eps
        grad[i] = (objective_min_sum_low_eigs(p_plus) - f0) / eps
    return grad

print("Adversarial: minimizing lambda_mid(P) + lambda_min(P)...")
min_sum = float('inf')
for trial in range(20):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    params = flatten(R, D)

    for step in range(400):
        grad = gradient_min_sum(params)
        lr = 0.03 if step < 200 else 0.01
        params -= lr * grad  # MINIMIZE (gradient descent)

    R, D = unflatten(params)
    eigs_P, c = compute_P_eigs(R, D)
    sum_low = eigs_P[0] + eigs_P[1]
    min_sum = min(min_sum, sum_low)

    eigs_M = np.linalg.eigvalsh(compute_M_total(R, D))
    print(f"  Trial {trial:2d}: lambda_mid(P)+lambda_min(P) = {sum_low:.6f}, "
          f"c = {c:.2f}, eigs_M = [{eigs_M[0]:.2f}, {eigs_M[1]:.2f}, {eigs_M[2]:.4f}]")

print(f"\nMinimum lambda_mid(P) + lambda_min(P) found: {min_sum:.6f}")
print(f"Condition >= 0: {'YES' if min_sum >= -1e-6 else 'NO'}")

# ============================================================
# Part 3f: D=I case - can we prove lambda_max <= 64 analytically?
# ============================================================

print("\n" + "=" * 70)
print("PART 3f: D=I case - detailed analysis")
print("=" * 70)

# For D=I, we have:
# F_x(n) = 28 + 2*sum_mu c_mu * n^T R_mu n + 2*sum_{mu<nu} d_{mu,nu} * n^T R_mu R_nu^T n
#
# We need to compute c_mu and d_{mu,nu} and verify F_x <= 64.

# Coefficients
c_mu = {}
for target_mu in range(4):
    coeff = 0
    for mu, nu in PLANES:
        a = (-1)**mu; b = (-1)**(nu+1)
        signs = [a, a, b, b]
        if mu == target_mu:
            coeff += signs[0]*signs[1] + signs[0]*signs[2]
        if nu == target_mu:
            coeff += signs[1]*signs[3] + signs[2]*signs[3]
    c_mu[target_mu] = coeff

d_munu = {}
for mu, nu in PLANES:
    a = (-1)**mu; b = (-1)**(nu+1)
    d_munu[(mu,nu)] = a * b  # signs[0]*signs[3] for D=I

print("D=I formula: F_x(n) = 28 + sum terms")
print(f"  Constant: 28 (= 24 + 4)")
print(f"  R_mu coefficients: {dict(c_mu)}")
print(f"  R_mu R_nu^T coefficients: {dict(d_munu)}")

# Note: at Q=I (all R_mu = I):
# F_x = 28 + 2*sum_mu c_mu + 2*sum d_{mu,nu}
# = 28 + 2*(4+4+4+4) + 2*(1-1+1+1-1+1)
# = 28 + 32 + 2*2 = 28 + 32 + 4 = 64 ✓

val_at_I = 28 + 2*sum(c_mu.values()) + 2*sum(d_munu.values())
print(f"\n  At Q=I: 28 + 2*{sum(c_mu.values())} + 2*{sum(d_munu.values())} = {val_at_I}")

# Now, the D=I case:
# F_x(n) = 28 + 2*4*sum_mu n^T R_mu n + 2*sum_{mu<nu} d_{mu,nu} n^T R_mu R_nu^T n

# Each n^T R_mu n = cos(theta_mu) + (1-cos(theta_mu))(n.u_mu)^2
# This ranges from cos(theta_mu) to 1.

# At Q=I: n^T R_mu n = 1 for all mu and n.
# n^T R_mu R_nu^T n ranges similarly.

# The question: can we show F_x <= 64 for D=I?

# For D=I, F_x = 28 + 8*sum_mu n^T R_mu n + 2*sum d_{mu,nu} n^T R_mu R_nu^T n

# 64 - F_x = 64 - 28 - 8*sum_mu n^T R_mu n - 2*sum d n^T R_mu R_nu^T n
# = 36 - 8*sum n^T R_mu n - 2*sum d n^T R_mu R_nu^T n

# At Q=I: 36 - 8*4 - 2*2 = 36 - 32 - 4 = 0 ✓

# Can we write 36 - 8*S - 2*T >= 0 where S = sum n^T R_mu n, T = sum d n^T R_mu R_nu^T n?

# S <= 4 (each n^T R_mu n <= 1, 4 terms)
# T <= |sum d| = |2| = 2 (at Q=I)

# But 36 - 8*4 - 2*2 = 0, so the bound is tight.

# Let me check: for generic R, is 8S + 2T <= 36?

print("\nD=I adversarial: maximize 8*S + 2*T")
max_val = 0
for _ in range(10000):
    R = [random_so3() for _ in range(4)]
    D_I = {p: np.eye(3) for p in PLANES}
    n = np.random.randn(3); n /= np.linalg.norm(n)

    S = sum(n @ R[mu] @ n for mu in range(4))
    T = sum(d_munu[(mu,nu)] * (n @ R[mu] @ R[nu].T @ n) for mu, nu in PLANES)
    val = 8*S + 2*T
    max_val = max(max_val, val)

print(f"  Max(8S + 2T) over 10000 random: {max_val:.4f} (need <= 36)")

# Adversarial with optimization
print("\nAdversarial gradient ascent on 8S + 2T:")

def compute_8S_2T(params_full):
    """params_full = [n(3), R_params(12)]"""
    n = params_full[:3]
    n = n / np.linalg.norm(n)
    R_params = params_full[3:]
    R = [so3_exp(R_params[3*i:3*i+3]) for i in range(4)]

    S = sum(n @ R[mu] @ n for mu in range(4))
    T = sum(d_munu[(mu,nu)] * (n @ R[mu] @ R[nu].T @ n) for mu, nu in PLANES)
    return 8*S + 2*T

max_8S2T = 0
for trial in range(20):
    n0 = np.random.randn(3); n0 /= np.linalg.norm(n0)
    R_params0 = np.random.randn(12) * 0.5
    params_full = np.concatenate([n0, R_params0])

    lr = 0.01
    best = 0
    for step in range(500):
        val0 = compute_8S_2T(params_full)
        best = max(best, val0)
        grad = np.zeros_like(params_full)
        eps = 1e-6
        for i in range(len(params_full)):
            pf = params_full.copy()
            pf[i] += eps
            grad[i] = (compute_8S_2T(pf) - val0) / eps
        params_full += lr * grad
        # Normalize n
        params_full[:3] /= np.linalg.norm(params_full[:3])

    max_8S2T = max(max_8S2T, best)
    if trial < 10 or best > 35:
        print(f"  Trial {trial}: max(8S+2T) = {best:.6f}")

print(f"\nMax adversarial 8S+2T: {max_8S2T:.6f} (need <= 36)")

# ============================================================
# Part 3g: Key insight for D=I proof
# ============================================================

print("\n" + "=" * 70)
print("PART 3g: Quadratic form analysis for D=I")
print("=" * 70)

# For D=I case, the M matrix is:
# M = 28*I + 8*sum_mu sym(R_mu) + 2*sum_{mu<nu} d_{mu,nu} sym(R_mu R_nu^T)
# where sym(O) = (O + O^T)/2

# sym(R) for rotation by theta about u:
# sym(R) = cos(theta)*I + (1-cos(theta))*uu^T

# So M = 28*I + 8*sum_mu [cos(theta_mu)*I + (1-cos(theta_mu))*u_mu u_mu^T]
#       + 2*sum d [cos(phi_{mu,nu})*I + (1-cos(phi_{mu,nu}))*w_{mu,nu} w_{mu,nu}^T]

# where phi_{mu,nu} = angle of R_mu R_nu^T, w_{mu,nu} = axis of R_mu R_nu^T.

# Let's compute the isotropic part c and anisotropy P for D=I:
# c = 28 + 8*sum cos(theta_mu) + 2*sum d cos(phi_{mu,nu})
# P = 8*sum (1-cos theta_mu) u_mu u_mu^T + 2*sum d (1-cos phi_{mu,nu}) w_{mu,nu} w_{mu,nu}^T

# c + Tr(P) = 28 + 8*sum cos theta_mu + 2*sum d cos phi_{mu,nu}
#            + 8*sum (1-cos theta_mu) + 2*sum d (1-cos phi_{mu,nu})
# = 28 + 8*4 + 2*sum d = 28 + 32 + 2*2 = 64 ✓

# Note: sum d_{mu,nu} = 1+(-1)+1+1+(-1)+1 = 2

print("D=I: c + Tr(P) = 28 + 8*4 + 2*2 = 64 ✓")

# For D=I, the negative contributions to P come from:
# d_{mu,nu} = -1 for (0,2) and (1,3) (inactive planes)
# These contribute: -2*(1-cos phi_{02})*w_{02} w_{02}^T - 2*(1-cos phi_{13})*w_{13} w_{13}^T

# The positive contributions come from:
# Base links: 8*sum_mu (1-cos theta_mu) u_mu u_mu^T  (always positive)
# Active composites: +2*(1-cos phi_{01})*w_{01} w_{01}^T + ... for 4 active planes

# The base links provide "uniform coverage" with weight 8*(1-cos theta_mu) per direction.
# The active composites provide additional positive weight.
# The inactive composites subtract weight.

# Key question: can the subtracted weight from inactive composites exceed the base+active positive?

# For each inactive plane, say (0,2):
# R_0 R_2^T has axis w_{02} and angle phi_{02}.
# The subtracted weight is 2*(1-cos phi_{02}).
# The base links R_0 and R_2 provide weight 8*(1-cos theta_0)*u_0 u_0^T + 8*(1-cos theta_2)*u_2 u_2^T

# If u_0, u_2, w_{02} are all aligned, the base links dominate:
# base weight along that direction: 8*(1-cos theta_0) + 8*(1-cos theta_2)
# inactive subtracted: 2*(1-cos phi_{02})

# By the triangle inequality for rotation angles: phi_{02} <= theta_0 + theta_2
# (angle of R_0 R_2^T <= angle of R_0 + angle of R_2)
# So 1-cos phi_{02} <= something...

# But this isn't quite right for angles > pi. Let me check the more precise bound.

# For SO(3): angle(AB) <= angle(A) + angle(B) (mod 2pi)
# and 1-cos is convex on [0, pi], so...

# Test numerically
print("\nTesting rotation angle inequality:")
for _ in range(10000):
    R0 = random_so3()
    R2 = random_so3()
    R02 = R0 @ R2.T
    theta0 = np.arccos(np.clip((np.trace(R0)-1)/2, -1, 1))
    theta2 = np.arccos(np.clip((np.trace(R2)-1)/2, -1, 1))
    phi02 = np.arccos(np.clip((np.trace(R02)-1)/2, -1, 1))

    # Check: 2(1-cos phi) <= 8(1-cos theta0) + 8(1-cos theta2)?
    # i.e., (1-cos phi) <= 4(1-cos theta0) + 4(1-cos theta2)
    lhs = 1 - np.cos(phi02)
    rhs = 4*(1-np.cos(theta0)) + 4*(1-np.cos(theta2))
    if lhs > rhs + 1e-10:
        print(f"  VIOLATION: {lhs:.6f} > {rhs:.6f}, theta0={theta0:.3f}, theta2={theta2:.3f}, phi02={phi02:.3f}")
        break
else:
    print("  No violations in 10000 tests")
    print("  Conjecture: (1-cos(angle(R0 R2^T))) <= 4(1-cos(angle(R0))) + 4(1-cos(angle(R2)))")

# Even if the axis directions differ, check: for any n,
# (1-cos phi)(n.w)^2 <= 4(1-cos theta0)(n.u0)^2 + 4(1-cos theta2)(n.u2)^2 ?

violations = 0
for _ in range(100000):
    R0 = random_so3()
    R2 = random_so3()
    R02 = R0 @ R2.T
    n = np.random.randn(3); n /= np.linalg.norm(n)

    # Symmetric parts
    sym_R0 = (R0 + R0.T) / 2
    sym_R2 = (R2 + R2.T) / 2
    sym_R02 = (R02 + R02.T) / 2

    # We want: n^T (I - sym_R02) n <= 4 * n^T (I - sym_R0) n + 4 * n^T (I - sym_R2) n
    lhs = n @ (np.eye(3) - sym_R02) @ n
    rhs = 4 * n @ (np.eye(3) - sym_R0) @ n + 4 * n @ (np.eye(3) - sym_R2) @ n
    if lhs > rhs + 1e-10:
        violations += 1
        if violations <= 3:
            print(f"  Direction violation: lhs={lhs:.6f} > rhs={rhs:.6f}")

if violations == 0:
    print(f"\n  No directional violations in 100000 tests!")
    print(f"  CONJECTURE: (I - sym(R0 R2^T)) <= 4(I - sym(R0)) + 4(I - sym(R2)) as quadratic forms")
else:
    print(f"\n  {violations} directional violations found out of 100000")

print("\nDone with Stage 3.")
