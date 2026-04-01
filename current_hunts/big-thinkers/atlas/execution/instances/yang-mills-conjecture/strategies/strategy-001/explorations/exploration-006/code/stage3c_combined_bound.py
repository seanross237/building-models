"""
Stage 3c: The combined bound - using base-link terms to absorb inactive negatives.

The individual lemmas (subadditivity, inactive net) FAIL. But the full
expression has extra slack from base links and active cross-links.

For each inactive plaquette (0,2), the relevant terms in 64I-M are:
  +f(R_0) + f(R_2)  (base links)
  +f(R_0 D) + f(D R_2^T) - f(D) - f(R_0 D R_2^T)  (inactive plaquette)

TEST: Is f(R_0) + f(R_2) + f(R_0 D) + f(D R_2^T) - f(D) - f(R_0 D R_2^T) >= 0 ?
"""

import numpy as np

np.random.seed(42)

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

def f_scalar(R, n):
    return 1 - n @ R @ n

# ============================================================
# Test 1: Combined base + inactive bound
# ============================================================

print("=" * 70)
print("TEST 1: f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) >= 0 ?")
print("=" * 70)

violations = 0
min_val = float('inf')
for _ in range(2000000):
    A = random_so3()
    D = random_so3()
    B = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    val = (f_scalar(A, n) + f_scalar(B, n)
         + f_scalar(A @ D, n) + f_scalar(D @ B.T, n)
         - f_scalar(D, n) - f_scalar(A @ D @ B.T, n))
    min_val = min(min_val, val)
    if val < -1e-10:
        violations += 1

print(f"  2,000,000 tests: violations = {violations}, min = {min_val:.6f}")

# ============================================================
# Test 1b: Adversarial search
# ============================================================

print("\n  Adversarial search:")
min_adv = float('inf')
for trial in range(30):
    params = np.random.randn(12) * 2  # [n(3), A(3), D(3), B(3)]
    lr = 0.01
    best = 10

    for step in range(500):
        n = params[:3]; n /= np.linalg.norm(n)
        A = so3_exp(params[3:6])
        D = so3_exp(params[6:9])
        B = so3_exp(params[9:12])

        val = (f_scalar(A, n) + f_scalar(B, n)
             + f_scalar(A @ D, n) + f_scalar(D @ B.T, n)
             - f_scalar(D, n) - f_scalar(A @ D @ B.T, n))
        best = min(best, val)

        grad = np.zeros(12)
        eps = 1e-6
        for i in range(12):
            pp = params.copy(); pp[i] += eps
            nn = pp[:3]; nn /= np.linalg.norm(nn)
            Ap = so3_exp(pp[3:6])
            Dp = so3_exp(pp[6:9])
            Bp = so3_exp(pp[9:12])
            vp = (f_scalar(Ap, nn) + f_scalar(Bp, nn)
                + f_scalar(Ap @ Dp, nn) + f_scalar(Dp @ Bp.T, nn)
                - f_scalar(Dp, nn) - f_scalar(Ap @ Dp @ Bp.T, nn))
            grad[i] = (vp - val) / eps

        params -= lr * grad  # minimize
        params[:3] /= np.linalg.norm(params[:3])

    min_adv = min(min_adv, best)
    if trial < 10 or best < 0.1:
        print(f"    Trial {trial}: min = {best:.8f}")

print(f"\n  Min adversarial: {min_adv:.8f}")
print(f"  Combined bound holds: {min_adv >= -1e-6}")

# ============================================================
# Test 2: What if we don't have the full base link surplus?
# ============================================================

print("\n" + "=" * 70)
print("TEST 2: Checking weaker condition without base terms")
print("f(AD) + f(DB^T) - f(D) - f(ADB^T) >= 0 ?")
print("(This is the inactive net WITHOUT base link help)")
print("=" * 70)

# We already know this fails. Just confirm the max violation size.
max_neg = 0
for _ in range(100000):
    A = random_so3()
    D = random_so3()
    B = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    val = (f_scalar(A @ D, n) + f_scalar(D @ B.T, n)
         - f_scalar(D, n) - f_scalar(A @ D @ B.T, n))
    if val < 0:
        max_neg = max(max_neg, -val)

print(f"  Max negative value of inactive net: {max_neg:.6f}")
print(f"  (This much needs to be absorbed by base link terms)")

# ============================================================
# Test 3: What's the tightest the combined bound can be?
# ============================================================

print("\n" + "=" * 70)
print("TEST 3: Structure at the tightest combined bound")
print("=" * 70)

# Find configs where the combined bound is near 0
near_zero = []
for trial in range(30):
    params = np.random.randn(12) * 2
    lr = 0.01
    best_val = 10
    best_params = params.copy()

    for step in range(500):
        n = params[:3]; n /= np.linalg.norm(n)
        A = so3_exp(params[3:6])
        D = so3_exp(params[6:9])
        B = so3_exp(params[9:12])

        val = (f_scalar(A, n) + f_scalar(B, n)
             + f_scalar(A @ D, n) + f_scalar(D @ B.T, n)
             - f_scalar(D, n) - f_scalar(A @ D @ B.T, n))

        if val < best_val:
            best_val = val
            best_params = params.copy()

        grad = np.zeros(12)
        eps = 1e-6
        for i in range(12):
            pp = params.copy(); pp[i] += eps
            nn = pp[:3]; nn /= np.linalg.norm(nn)
            Ap = so3_exp(pp[3:6])
            Dp = so3_exp(pp[6:9])
            Bp = so3_exp(pp[9:12])
            vp = (f_scalar(Ap, nn) + f_scalar(Bp, nn)
                + f_scalar(Ap @ Dp, nn) + f_scalar(Dp @ Bp.T, nn)
                - f_scalar(Dp, nn) - f_scalar(Ap @ Dp @ Bp.T, nn))
            grad[i] = (vp - val) / eps

        params -= lr * grad
        params[:3] /= np.linalg.norm(params[:3])

    near_zero.append((best_val, best_params))

# Analyze the tightest cases
near_zero.sort(key=lambda x: x[0])
for i, (val, params) in enumerate(near_zero[:5]):
    n = params[:3]; n /= np.linalg.norm(n)
    A = so3_exp(params[3:6])
    D = so3_exp(params[6:9])
    B = so3_exp(params[9:12])

    fA = f_scalar(A, n)
    fB = f_scalar(B, n)
    fD = f_scalar(D, n)
    fAD = f_scalar(A @ D, n)
    fDBt = f_scalar(D @ B.T, n)
    fADBt = f_scalar(A @ D @ B.T, n)

    print(f"\n  Case {i}: combined = {val:.6f}")
    print(f"    f(A) = {fA:.4f}, f(B) = {fB:.4f}")
    print(f"    f(AD) = {fAD:.4f}, f(DB^T) = {fDBt:.4f}")
    print(f"    f(D) = {fD:.4f}, f(ADB^T) = {fADBt:.4f}")
    print(f"    Inactive net = {fAD + fDBt - fD - fADBt:.4f}")
    print(f"    Base surplus = {fA + fB:.4f}")

    # Rotation angles
    for name, R in [("A", A), ("D", D), ("B", B), ("AD", A@D), ("DB^T", D@B.T), ("ADB^T", A@D@B.T)]:
        tr = np.clip((np.trace(R)-1)/2, -1, 1)
        angle = np.arccos(tr) * 180 / np.pi
        print(f"    angle({name}) = {angle:.1f}°")

# ============================================================
# Test 4: PROVE the combined bound via Three Vectors Lemma
# ============================================================

print("\n" + "=" * 70)
print("TEST 4: Proving the combined bound algebraically")
print("=" * 70)

# f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T)
#
# Using Three Vectors Lemma: f(ADB^T) <= 4f(AD) + 4f(B)
# So: -f(ADB^T) >= -4f(AD) - 4f(B)
#
# Combined >= f(A) + f(B) + f(AD) + f(DB^T) - f(D) - 4f(AD) - 4f(B)
#           = f(A) - 3f(B) - 3f(AD) + f(DB^T) - f(D)
#
# This can be negative. Not helpful with coefficient 4.

# Try: f(ADB^T) = f(A (DB^T)) <= 4f(A) + 4f(DB^T)
# Combined >= f(A) + f(B) + f(AD) + f(DB^T) - f(D) - 4f(A) - 4f(DB^T)
#           = -3f(A) + f(B) + f(AD) - 3f(DB^T) - f(D)
# Also not helpful.

# The coefficient 4 from Three Vectors Lemma is too large.
# Let me check: is the coefficient 4 tight?

print("Tightness of Three Vectors Lemma coefficient:")
max_ratio = 0
for _ in range(500000):
    A = random_so3()
    B = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    fAB = f_scalar(A @ B, n)
    fA = f_scalar(A, n)
    fB = f_scalar(B, n)

    if fA + fB > 1e-10:
        ratio = fAB / (fA + fB)
        max_ratio = max(max_ratio, ratio)

print(f"  max(f(AB) / (f(A)+f(B))) = {max_ratio:.6f}")
print(f"  Three Vectors Lemma gives coefficient 4")
print(f"  Tight coefficient for subadditivity: {max_ratio:.4f}")

# ============================================================
# Test 5: Alternative approach - direct quadratic form
# ============================================================

print("\n" + "=" * 70)
print("TEST 5: Direct approach for inactive plaquette bound")
print("=" * 70)

# Let's express the combined bound in terms of unit vectors.
# Set a = A^T n, b = Bn, d = Dn (unit vectors)
# p = D^T n (another unit vector; note f(D) uses p.n while f(D^T) uses d.n)
#
# f(A) = 1 - n.a
# f(B) = 1 - n.b (since f(B) = 1 - n^T B n, and n^T B n = n.(Bn) = n.b?
#         Wait: n^T B n = (B^T n).n. Let me denote b' = B^T n = B^{-1} n.
#         Then f(B) = 1 - b'.n.)
# Hmm, this notation is getting confusing. Let me use:
# f(R, n) = 1 - n^T R n = 1 - (R^T n) . n

# For R^T n: if R is rotation by theta about u,
# R^T n = cos(theta) n + (1-cos(theta))(n.u)u - sin(theta)(u x n)
# And (R^T n).n = cos(theta) + (1-cos(theta))(n.u)^2 = n^T R n. So f is symmetric.

# Let's use explicit coordinates. Fix n = e_3.
# Then f(R) = 1 - R_{33}.

# For A parameterized by angles, D by angles, B by angles:
# f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T)
# = (1 - A_{33}) + (1 - B_{33}) + (1 - (AD)_{33}) + (1 - (DB^T)_{33}) - (1 - D_{33}) - (1 - (ADB^T)_{33})
# = 4 - A_{33} - B_{33} - (AD)_{33} - (DB^T)_{33} + D_{33} + (ADB^T)_{33} - 1
# = 3 + D_{33} + (ADB^T)_{33} - A_{33} - B_{33} - (AD)_{33} - (DB^T)_{33}

# Hmm, this doesn't simplify obviously.

# Let me try a very different approach. Instead of proving term-by-term,
# maybe I can show the full 64I - M >= 0 by a different decomposition.

# Key idea: Try to decompose 64I - M as a SUM OF SQUARES.
# This would give a direct proof.

# For the D=I case, we showed:
# 64I - M = 2 * [4*sum f(R_mu) + sum_active f(R_mu R_nu^T) - sum_inactive f(R_mu R_nu^T)]
# >= 2 * sum_active f(R_mu R_nu^T) >= 0

# For general D, can we find a similar SOS decomposition?

# Let me compute 64I - M for many configs and examine its eigenvalues
print("Eigenvalues of 64I - M for random configs:")

PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]

def compute_M_total(R, D):
    M = np.zeros((3, 3))
    for mu, nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        A = a * S + b * T
        M += A.T @ A
    return M

min_eig_gap = float('inf')
for _ in range(10000):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    M = compute_M_total(R, D)
    gap_matrix = 64 * np.eye(3) - M
    eigs = np.linalg.eigvalsh(gap_matrix)
    min_eig = eigs[0]
    min_eig_gap = min(min_eig_gap, min_eig)

print(f"  Min eigenvalue of (64I - M) over 10000 configs: {min_eig_gap:.6f}")
print(f"  All non-negative: {min_eig_gap >= -1e-10}")

# ============================================================
# Test 6: Complete budget analysis
# ============================================================

print("\n" + "=" * 70)
print("TEST 6: Complete budget - how much each group contributes")
print("=" * 70)

# For the eigenvector n_max of M, compute each group's contribution to 64-lambda_max

def so3_log(R):
    tr = np.clip((np.trace(R) - 1) / 2, -1, 1)
    angle = np.arccos(tr)
    if angle < 1e-10:
        return np.zeros(3)
    axis = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]]) / (2*np.sin(angle))
    return angle * axis

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

def gradient_lmax(params, eps=1e-6):
    R, D = unflatten(params)
    M0 = compute_M_total(R, D)
    lam0 = np.linalg.eigvalsh(M0)[2]
    grad = np.zeros_like(params)
    for i in range(len(params)):
        p_plus = params.copy()
        p_plus[i] += eps
        R_p, D_p = unflatten(p_plus)
        M_p = compute_M_total(R_p, D_p)
        grad[i] = (np.linalg.eigvalsh(M_p)[2] - lam0) / eps
    return grad

# Run a few adversarial and analyze
print("Budget analysis at adversarial maxima:")
for trial in range(5):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    params = flatten(R, D)

    for step in range(500):
        grad = gradient_lmax(params)
        lr = 0.05 if step < 200 else (0.02 if step < 350 else 0.005)
        params += lr * grad

    R, D = unflatten(params)
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)
    n = np.linalg.eigh(M)[1][:, 2]

    print(f"\n  Trial {trial}: lambda_max = {eigs[2]:.6f}")

    # Base link contribution to gap
    base = sum(f_scalar(R[mu], n) for mu in range(4))

    # Active cross-link contribution
    active_total = 0
    ACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu)%2 == 1]
    for mu, nu in ACTIVE:
        active_total += (f_scalar(R[mu] @ D[(mu,nu)], n)
                       + f_scalar(D[(mu,nu)], n)
                       + f_scalar(R[mu] @ D[(mu,nu)] @ R[nu].T, n)
                       + f_scalar(D[(mu,nu)] @ R[nu].T, n))

    # Inactive net contribution
    INACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu)%2 == 0]
    inactive_net = 0
    for mu, nu in INACTIVE:
        inactive_net += (f_scalar(R[mu] @ D[(mu,nu)], n)
                       + f_scalar(D[(mu,nu)] @ R[nu].T, n)
                       - f_scalar(D[(mu,nu)], n)
                       - f_scalar(R[mu] @ D[(mu,nu)] @ R[nu].T, n))

    total = 2 * (base + active_total + inactive_net)
    print(f"    Base: {base:.4f}, Active: {active_total:.4f}, Inactive net: {inactive_net:.4f}")
    print(f"    Total (= 64 - lambda_max): {total:.4f} vs gap {64-eigs[2]:.4f}")

print("\n" + "=" * 70)
print("TEST 7: Trying to tighten the Three Vectors bound with structure")
print("=" * 70)

# The Three Vectors Lemma gives f(AB) <= 4f(A) + 4f(B).
# But in our setting, the rotations A, B satisfy ADDITIONAL constraints
# (they share base links across plaquettes).
#
# For a tighter bound: if A and B share the same rotation axis:
# f(AB) = f(A) + f(B) - 2*stuff  (potentially tighter)
#
# More importantly, the OVERALL bound works even if individual terms don't.
# This suggests the proof needs to use the FULL structure, not plaquette-by-plaquette.

# Let me check: what fraction of the positive budget does the base link provide?
# And what fraction does the inactive net consume?

print("Budget fractions at adversarial maxima:")
for trial in range(20):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    params = flatten(R, D)

    for step in range(500):
        grad = gradient_lmax(params)
        lr = 0.05 if step < 200 else (0.02 if step < 350 else 0.005)
        params += lr * grad

    R, D = unflatten(params)
    M = compute_M_total(R, D)
    eigs = np.linalg.eigvalsh(M)
    n = np.linalg.eigh(M)[1][:, 2]

    base = sum(f_scalar(R[mu], n) for mu in range(4))

    active_total = 0
    for mu, nu in ACTIVE:
        active_total += (f_scalar(R[mu] @ D[(mu,nu)], n)
                       + f_scalar(D[(mu,nu)], n)
                       + f_scalar(R[mu] @ D[(mu,nu)] @ R[nu].T, n)
                       + f_scalar(D[(mu,nu)] @ R[nu].T, n))

    inactive_net = 0
    for mu, nu in INACTIVE:
        inactive_net += (f_scalar(R[mu] @ D[(mu,nu)], n)
                       + f_scalar(D[(mu,nu)] @ R[nu].T, n)
                       - f_scalar(D[(mu,nu)], n)
                       - f_scalar(R[mu] @ D[(mu,nu)] @ R[nu].T, n))

    print(f"  Trial {trial}: base={base:.4f}, active={active_total:.4f}, "
          f"inact_net={inactive_net:.4f}, sum={base+active_total+inactive_net:.4f}")

print("\nDone with Stage 3c.")
