"""
Stage 3: Analyze the critical manifold where lambda_max = 64 and develop proof.

KEY FINDING from Stage 2b: adversarial ascent always converges to lambda_max = 64.
This suggests a mathematical identity or tight inequality.

PLAN:
1. At critical configs, analyze the per-plaquette decomposition
2. Check if active plaquettes are saturated and inactive are zero
3. Develop the proof based on the observed structure
"""

import numpy as np
from itertools import product as iproduct

np.random.seed(999)

# SO(3) utilities
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

planes = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]
sigmas = {(mu,nu): (-1)**(mu+nu+1) for mu,nu in planes}

def compute_M_total(R, D):
    M = np.zeros((3, 3))
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        A = a * S + b * T
        M += A.T @ A
    return M

def compute_B_vectors(R, D, n):
    """Compute all 6 B vectors for the given n."""
    Bs = {}
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        B = (a * S + b * T) @ n
        Bs[(mu,nu)] = B
    return Bs

def adversarial_ascent_detailed(n_steps=500, lr=0.02):
    """Gradient ascent on lambda_max, return final config."""
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}

    for step in range(n_steps):
        M = compute_M_total(R, D)
        eigs, vecs = np.linalg.eigh(M)
        lam = eigs[2]
        n_star = vecs[:, 2]

        # Gradient ascent via finite differences
        eps = 1e-5
        for mu_r in range(4):
            for j in range(3):
                omega = np.zeros(3)
                omega[j] = eps
                R_p = [r.copy() for r in R]
                R_p[mu_r] = R[mu_r] @ so3_exp(omega)
                M_p = compute_M_total(R_p, D)
                dlam = (np.linalg.eigvalsh(M_p)[2] - lam) / eps
                R[mu_r] = R[mu_r] @ so3_exp(lr * dlam * np.eye(3)[j])

        for i, (mu, nu) in enumerate(planes):
            for j in range(3):
                omega = np.zeros(3)
                omega[j] = eps
                D_p = {k: v.copy() for k, v in D.items()}
                D_p[(mu,nu)] = D[(mu,nu)] @ so3_exp(omega)
                M_p = compute_M_total(R, D_p)
                dlam = (np.linalg.eigvalsh(M_p)[2] - lam) / eps
                D[(mu,nu)] = D[(mu,nu)] @ so3_exp(lr * dlam * np.eye(3)[j])

    return R, D

# ============================================================
# Analyze critical configs where lambda_max = 64
# ============================================================

print("=" * 70)
print("ANALYZE CRITICAL CONFIGS WHERE lambda_max = 64")
print("=" * 70)

for trial in range(10):
    R, D = adversarial_ascent_detailed(n_steps=300, lr=0.02)
    M = compute_M_total(R, D)
    eigs, vecs = np.linalg.eigh(M)
    n_star = vecs[:, 2]

    print(f"\n--- Trial {trial} ---")
    print(f"lambda_max = {eigs[2]:.8f}")
    print(f"n* = [{n_star[0]:.4f}, {n_star[1]:.4f}, {n_star[2]:.4f}]")

    # Per-plaquette decomposition at n*
    Bs = compute_B_vectors(R, D, n_star)
    total = 0.0
    for mu, nu in planes:
        B = Bs[(mu,nu)]
        bsq = np.dot(B, B)
        total += bsq
        typ = "A" if sigmas[(mu,nu)] == 1 else "I"
        print(f"  ({mu},{nu}) [{typ}]: |B|^2 = {bsq:.6f}, B = [{B[0]:.3f}, {B[1]:.3f}, {B[2]:.3f}]")
    print(f"  Total F_x(n*) = {total:.6f}")

    # Check: are all B vectors parallel to n*?
    print("  B directions (angle with n*):")
    for mu, nu in planes:
        B = Bs[(mu,nu)]
        bnorm = np.linalg.norm(B)
        if bnorm > 0.01:
            cos_angle = abs(np.dot(B, n_star)) / bnorm
            print(f"    ({mu},{nu}): |cos(angle)| = {cos_angle:.6f}, |B| = {bnorm:.4f}")

# ============================================================
# Key structural check: at lambda_max=64, are all B parallel to n*?
# ============================================================

print("\n" + "=" * 70)
print("STRUCTURE CHECK: Parallelism at lambda_max = 64")
print("=" * 70)

# If lambda_max(M) = 64 and the eigenvector is n*, then M n* = 64 n*.
# M = sum A^T A, so sum A^T B_k = 64 n* where B_k = A_k n*.
# This doesn't require B_k parallel to n*, but let's check.

n_parallel_check = 50
all_parallel = True
max_perp_frac = 0.0

for trial in range(n_parallel_check):
    R, D = adversarial_ascent_detailed(n_steps=200, lr=0.02)
    M = compute_M_total(R, D)
    eigs, vecs = np.linalg.eigh(M)
    n_star = vecs[:, 2]

    Bs = compute_B_vectors(R, D, n_star)
    for mu, nu in planes:
        B = Bs[(mu,nu)]
        bnorm = np.linalg.norm(B)
        if bnorm > 0.01:
            perp = B - np.dot(B, n_star) * n_star
            perp_frac = np.linalg.norm(perp) / bnorm
            max_perp_frac = max(max_perp_frac, perp_frac)
            if perp_frac > 0.01:
                all_parallel = False

print(f"Max perpendicular fraction: {max_perp_frac:.6f}")
print(f"All B parallel to n* at critical? {'YES' if max_perp_frac < 0.01 else 'NO'}")

# ============================================================
# If B's are parallel to n*, then decomposition simplifies
# ============================================================

print("\n" + "=" * 70)
print("PARALLEL DECOMPOSITION: B_k = alpha_k * n*")
print("=" * 70)

# If all B are parallel to n*, then |B_k|^2 = alpha_k^2 and F_x = sum alpha_k^2 = 64.
# And each B = A_k n* = alpha_k n*, so A_k n* = alpha_k n* (n* is an eigenvector of EACH A_k with eigenvalue alpha_k)

# Check: is n* simultaneously an eigenvector of all A_k?
for trial in range(5):
    R, D = adversarial_ascent_detailed(n_steps=300, lr=0.02)
    M = compute_M_total(R, D)
    eigs, vecs = np.linalg.eigh(M)
    n_star = vecs[:, 2]

    print(f"\n--- Trial {trial} ---")
    sum_alpha_sq = 0.0
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        A = a * S + b * T

        An = A @ n_star
        alpha = np.dot(An, n_star)
        perp = An - alpha * n_star
        perp_norm = np.linalg.norm(perp)

        sigma = sigmas[(mu,nu)]
        typ = "A" if sigma == 1 else "I"
        print(f"  ({mu},{nu}) [{typ}]: alpha = {alpha:.4f}, |A n* - alpha n*| = {perp_norm:.6f}, alpha^2 = {alpha**2:.4f}")
        sum_alpha_sq += alpha**2

    print(f"  Sum alpha^2 = {sum_alpha_sq:.6f}")

# ============================================================
# Critical insight: If n* is eigenvalue of each A_k,
# then alpha_k are eigenvalues and sum alpha_k^2 = 64.
# Per-plaquette: |alpha_k| <= 4 (since |B_k| <= 4).
# So sum <= 4 * sum |alpha_k| with each |alpha_k| <= 4.
# But sum alpha_k^2 = 64 with 6 terms each <= 16.
# ============================================================

print("\n" + "=" * 70)
print("DIRECT PROOF APPROACH: Parallelogram + Active/Inactive Pairing")
print("=" * 70)

# Test the direct approach: for ANY (R, D, n), decompose as:
# F_x = sum_active |B|^2 + sum_inactive |B|^2
# For active: B_active = X + Y, so |B|^2 = |X+Y|^2
# For inactive: B_inactive = X' - Y', so |B|^2 = |X'-Y'|^2
# Use: |X+Y|^2 + |X-Y|^2 = 2|X|^2 + 2|Y|^2 (parallelogram)

# The key is: can we bound sum_active + sum_inactive using the structure?
# Active (4 plaquettes): each |B| <= 4, so sum <= 64
# But we also need sum_inactive = F_x - sum_active
# If sum_active + sum_inactive <= 64, then F_x <= 64.

# Actually, let's compute: at what configs does sum_active approach 64?
print("\nActive plaquette saturation analysis:")
print("  For 3000 random configs:")

max_active_sum = 0.0
active_sums = []
inactive_sums = []

for _ in range(3000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    n = np.array([1.0, 0.0, 0.0])  # Fixed direction

    active_sum = 0.0
    inactive_sum = 0.0
    for mu, nu in planes:
        a = (-1)**mu
        b = (-1)**(nu+1)
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        B = (a * S + b * T) @ n
        bsq = np.dot(B, B)
        if sigmas[(mu,nu)] == 1:
            active_sum += bsq
        else:
            inactive_sum += bsq

    active_sums.append(active_sum)
    inactive_sums.append(inactive_sum)
    max_active_sum = max(max_active_sum, active_sum)

print(f"  Active sum: min={min(active_sums):.4f}, max={max(active_sums):.4f}, mean={np.mean(active_sums):.4f}")
print(f"  Inactive sum: min={min(inactive_sums):.4f}, max={max(inactive_sums):.4f}, mean={np.mean(inactive_sums):.4f}")
print(f"  Total (A+I): max={max(a+i for a,i in zip(active_sums,inactive_sums)):.4f}")

# Test: active + inactive decomposition at adversarial max
print("\n  At adversarial maxima (over n*):")
for trial in range(10):
    R, D = adversarial_ascent_detailed(n_steps=200, lr=0.02)
    M = compute_M_total(R, D)
    eigs, vecs = np.linalg.eigh(M)
    n_star = vecs[:, 2]

    active_s = 0.0
    inactive_s = 0.0
    for mu, nu in planes:
        a = (-1)**mu; b = (-1)**(nu+1)
        B = (a*(np.eye(3) + R[mu]@D[(mu,nu)]) + b*(R[mu] + R[mu]@D[(mu,nu)]@R[nu].T)) @ n_star
        bsq = np.dot(B, B)
        if sigmas[(mu,nu)] == 1:
            active_s += bsq
        else:
            inactive_s += bsq

    print(f"    Trial {trial}: active={active_s:.4f}, inactive={inactive_s:.4f}, total={active_s+inactive_s:.4f}")

# ============================================================
# Test the REAL proof approach: sum = sum_active + sum_inactive
# At the critical manifold (lambda_max=64), the active sum saturates
# to 64 and inactive sum is 0.
# AWAY from the critical manifold, F_x < 64.
# ============================================================

print("\n" + "=" * 70)
print("PARALLELOGRAM IDENTITY APPROACH")
print("=" * 70)

# For each plaquette (mu, nu):
# B = a(n + p) + b R_mu(n + q)
# where p = R_mu D n, q = D R_nu^T n
#
# For active (sigma=ab=+1, a=b): B = a[(n+p) + R_mu(n+q)]
# For inactive (sigma=ab=-1, a=-b): B = a[(n+p) - R_mu(n+q)]
#
# DEFINE for each plaquette:
# X = n + R_mu D n      (vector on R^3, norm <= 2)
# Y = R_mu(n + D R_nu^T n) (vector on R^3, norm <= 2)
#
# Active: |B|^2 = |X+Y|^2
# Inactive: |B|^2 = |X-Y|^2
#
# By parallelogram: |X+Y|^2 + |X-Y|^2 = 2|X|^2 + 2|Y|^2 <= 2*4 + 2*4 = 16
# So |B_active|^2 + [inactive complement] <= 16 for each plaquette.
#
# But there are 4 active and 2 inactive plaquettes.
# If we could pair each inactive with an active, we'd get 2 pairs contributing <= 16 each,
# plus 2 unpaired active contributing <= 16 each: total <= 64.
#
# But the pairing requires same X, Y — which doesn't hold generically.
# HOWEVER: we can use a different approach!

# For each ACTIVE plaquette: |B_active|^2 = |X+Y|^2 <= (|X| + |Y|)^2 <= 16  (per plaquette)
# For each INACTIVE plaquette: |B_inactive|^2 = |X-Y|^2

# Total active <= 4 * 16 = 64. Question: total inactive adds how much?

# KEY IDENTITY: For each plaquette,
# |B_active|^2 + |B_inactive_complement|^2 = 2|X|^2 + 2|Y|^2
# where B_inactive_complement is the "same plaquette but with opposite sign"

# For the actual inactive plaquettes (0,2) and (1,3), their "complements" would be
# active versions with the same X, Y. But these are DIFFERENT plaquettes.

# Let me instead try: write the sum using the X, Y variables directly.

print("Computing X, Y decomposition for all configs...")

n_test = 2000
Fx_values = []
para_bounds = []

for trial in range(n_test):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    n = np.array([1.0, 0.0, 0.0])

    Fx = 0.0
    para_sum = 0.0  # sum of 2|X|^2 + 2|Y|^2 over all plaquettes

    for mu, nu in planes:
        X = n + R[mu] @ D[(mu,nu)] @ n
        Y = R[mu] @ (n + D[(mu,nu)] @ R[nu].T @ n)
        sigma = sigmas[(mu,nu)]

        Bsq = np.dot(X+sigma*Y, X+sigma*Y)  # |X + sigma*Y|^2
        Fx += Bsq

        para = 2*np.dot(X,X) + 2*np.dot(Y,Y)
        para_sum += para

    Fx_values.append(Fx)
    para_bounds.append(para_sum)

print(f"F_x stats: min={min(Fx_values):.4f}, max={max(Fx_values):.4f}, mean={np.mean(Fx_values):.4f}")
print(f"Para bound sum (2|X|^2+2|Y|^2): min={min(para_bounds):.4f}, max={max(para_bounds):.4f}")
print(f"Gap (para - Fx): min={(min(p-f for p,f in zip(para_bounds,Fx_values))):.4f}")

# The parallelogram sum is the sum of ALL |B|^2 if each plaquette contributed its PAIR.
# Para_sum = sum_all (|X+Y|^2 + |X-Y|^2) = 2 * sum |X|^2 + 2 * sum |Y|^2

# So F_x = Para_sum - sum_complement
# where sum_complement = sum_active |X-Y|^2 + sum_inactive |X+Y|^2

# This means: F_x = Para_sum - sum_complement <= Para_sum
# And Para_sum itself is bounded...

# But more useful: F_x = sum_active |X+Y|^2 + sum_inactive |X-Y|^2
# And sum_active |X+Y|^2 <= sum_active 16 = 64

# So F_x <= 64 + sum_inactive |X-Y|^2

# Hmm, that's the wrong direction. We need inactive to help, not hurt.

# KEY: The parallelogram identity gives:
# sum_active |X+Y|^2 = sum_active [2|X|^2 + 2|Y|^2 - |X-Y|^2]
# sum_inactive |X-Y|^2 = sum_inactive [2|X|^2 + 2|Y|^2 - |X+Y|^2]

# F_x = sum_active [2|X|^2 + 2|Y|^2 - |X-Y|^2] + sum_inactive [2|X|^2 + 2|Y|^2 - |X+Y|^2]
# = 2 sum_all (|X|^2 + |Y|^2) - sum_active |X-Y|^2 - sum_inactive |X+Y|^2

# Let P = 2 sum_all (|X|^2 + |Y|^2) >= F_x
# Let Q = sum_active |X-Y|^2 + sum_inactive |X+Y|^2 >= 0
# F_x = P - Q

# We want F_x <= 64, i.e., P - Q <= 64, i.e., Q >= P - 64.

# At Q=I: P = 2*6*8 = 96, Q = 4*0 + 2*16 = 32, F_x = 96 - 32 = 64. ✓

# For general Q: we need Q >= P - 64.

# Let me compute P and Q for the random configs:
print("\n\nP and Q analysis:")
Ps = []
Qs = []
for trial in range(n_test):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    n = np.array([1.0, 0.0, 0.0])

    P = 0.0
    Q = 0.0
    Fx = 0.0
    for mu, nu in planes:
        X = n + R[mu] @ D[(mu,nu)] @ n
        Y = R[mu] @ (n + D[(mu,nu)] @ R[nu].T @ n)
        sigma = sigmas[(mu,nu)]

        xsq = np.dot(X, X)
        ysq = np.dot(Y, Y)
        P += 2*(xsq + ysq)

        Bsq = np.dot(X + sigma*Y, X + sigma*Y)
        Fx += Bsq

        # Complementary
        Bcomp = np.dot(X - sigma*Y, X - sigma*Y)
        Q += Bcomp

    Ps.append(P)
    Qs.append(Q)

print(f"P stats: min={min(Ps):.2f}, max={max(Ps):.2f}, mean={np.mean(Ps):.2f}")
print(f"Q stats: min={min(Qs):.2f}, max={max(Qs):.2f}, mean={np.mean(Qs):.2f}")
print(f"P-Q stats (=Fx): max={max(p-q for p,q in zip(Ps,Qs)):.4f}")
print(f"Q - (P-64) stats: min={min(q-(p-64) for p,q in zip(Ps,Qs)):.4f}")

# Q >= P - 64 is equivalent to F_x <= 64.
# So the question is: is Q >= P - 64 always?

# Now Q = sum_active |X-Y|^2 + sum_inactive |X+Y|^2
# and P = sum_all 2(|X|^2 + |Y|^2)
#
# Q >= P - 64
# sum_active |X-Y|^2 + sum_inactive |X+Y|^2 >= sum_all 2(|X|^2+|Y|^2) - 64
#
# Using |X+Y|^2 = 2|X|^2 + 2|Y|^2 - |X-Y|^2 and |X-Y|^2 = 2|X|^2 + 2|Y|^2 - |X+Y|^2:
#
# Q = sum_active (2|X|^2 + 2|Y|^2 - |X+Y|^2) + sum_inactive (2|X|^2 + 2|Y|^2 - |X-Y|^2)
# = 2 sum_all (|X|^2 + |Y|^2) - sum_active |X+Y|^2 - sum_inactive |X-Y|^2
# = P - Fx
#
# So Q = P - F_x, and Q >= P - 64 iff F_x <= 64. Circular!

print("\n\nCircularity confirmed: Q = P - F_x is a tautology.")
print("Need a different approach.")

# ============================================================
# NEW APPROACH: Direct bound via |X+Y|^2 sharing
# ============================================================

print("\n" + "=" * 70)
print("NEW APPROACH: Shared vector analysis")
print("=" * 70)

# Each |B|^2 involves X_{mu,nu} = n + R_mu D_{mu,nu} n and Y_{mu,nu} = R_mu(n + D_{mu,nu} R_nu^T n)
#
# Key: Y_{mu,nu} = R_mu(n + q_{mu,nu}) where q = D R_nu^T n is a unit vector.
# So Y = R_mu n + R_mu q = v_mu + R_mu q
#
# X = n + R_mu D n = n + p_{mu,nu}
#
# For active: |B|^2 = |n + p + v_mu + R_mu q|^2 = |(n + v_mu) + (p + R_mu q)|^2
#
# where n + v_mu = n + R_mu n (depends only on base link mu, shared among plaquettes)
# and p + R_mu q = R_mu(D n + q) = R_mu(D n + D R_nu^T n) = R_mu D(n + R_nu^T n)
#
# So for active: B_active = a * [(n + R_mu n) + R_mu D(n + R_nu^T n)]
# |B_active|^2 = |(n + R_mu n) + R_mu D(n + R_nu^T n)|^2
# = |n + R_mu n|^2 + |n + R_nu^T n|^2 + 2<n + R_mu n, R_mu D(n + R_nu^T n)>
#
# First term: |n + R_mu n|^2 = 2(1 + <n, R_mu n>) = 2(1+p_mu)
# Second term: |R_mu D(n + R_nu^T n)| = |n + R_nu^T n| since R_mu D is orthogonal.
# So |R_mu D(n + R_nu^T n)|^2 = 2(1 + <n, R_nu^T n>) = 2(1+p_nu)
#
# Cross term: <n+R_mu n, R_mu D(n + R_nu^T n)>
# = <n, R_mu D n> + <n, R_mu D R_nu^T n> + <R_mu n, R_mu D n> + <R_mu n, R_mu D R_nu^T n>
# = d_{mu,nu} + f_{mu,nu} + <n, D n> + <n, D R_nu^T n>
# = d + f + e + d'

# For ACTIVE: |B|^2 = 2(1+p_mu) + 2(1+p_nu) + 2(d + f + e + d')
# = 4 + 2p_mu + 2p_nu + 2d + 2f + 2e + 2d'

# For INACTIVE: |B|^2 = 2(1+p_mu) + 2(1+p_nu) - 2(d + f + e + d')
# = 4 + 2p_mu + 2p_nu - 2d - 2f - 2e - 2d'

# So F_x = sum (4 + 2p_mu + 2p_nu) + sum sigma * 2(d + f + e + d')
#
# First sum = 24 + 2*3*(p_0+p_1+p_2+p_3) = 24 + 6*sum(p)
# Second sum = 2 * sum sigma * (d + f + e + d')

# Now: sigma(d + f + e + d') for each plaquette.
# The question is: is sum sigma * (d + f + e + d') <= 20?
# (Since F_x = 24 + 6*sum(p) + 2*sum(sigma*(d+f+e+d')) and sum(p) <= 4,
#  F_x <= 24 + 24 + 2*X = 48 + 2X. Need X <= 8.)

# Wait, sum(p) = sum_{mu} <n, R_mu n>, each in [-1,1], sum in [-4,4].
# 24 + 6*sum(p) ranges from 0 to 48.

# And we need 48 + 2*sum(sigma*(d+f+e+d')) <= 64, i.e., sum(...) <= 8.

# But at Q=I: sum(p) = 4, d=1, f=1, e=1, d'=1 for all plaquettes.
# sum(sigma*(d+f+e+d')) = 4*sum_active(4) + (-1)*sum_inactive(4)... wait
# sum sigma * (d+f+e+d') at Q=I:
# Active: sigma=+1, each contributes 4. Sum = 4*4 = 16.
# Inactive: sigma=-1, each contributes -4. Sum = 2*(-4) = -8.
# Total = 16 - 8 = 8. And 48 + 2*8 = 64. ✓

# So the bound reduces to: sum sigma * (d + f + e + d') <= (64 - 24 - 6*sum(p))/2 = 20 - 3*sum(p)

# Hmm, that still involves sum(p). Let me think differently.

# The total formula is:
# F_x = 24 + 6*sum(p) + 2*sum(sigma*(d+f+e+d'))
# = 24 + 6S + 2T where S = sum p_mu, T = sum sigma*(d+f+e+d')

# We need 24 + 6S + 2T <= 64, i.e., 3S + T <= 20.

# At Q=I: S=4, T=8. 3*4+8 = 20. Tight!
# So the bound 3S + T <= 20 is tight at Q=I.

# Can we prove 3S + T <= 20 for all (R, D)?

# Let me verify numerically:
print("Testing 3S + T <= 20:")
max_3ST = -np.inf
for _ in range(5000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    n = np.array([1.0, 0.0, 0.0])

    S = sum(n @ R[mu] @ n for mu in range(4))

    T = 0.0
    for mu, nu in planes:
        sigma = sigmas[(mu,nu)]
        d = n @ R[mu] @ D[(mu,nu)] @ n
        f = n @ R[mu] @ D[(mu,nu)] @ R[nu].T @ n
        e = n @ D[(mu,nu)] @ n
        dp = n @ D[(mu,nu)] @ R[nu].T @ n
        T += sigma * (d + f + e + dp)

    val = 3*S + T
    max_3ST = max(max_3ST, val)

print(f"  Max 3S + T over 5000 trials: {max_3ST:.6f}")
print(f"  Bound: <= 20.0")
print(f"  RESULT: {'PASS' if max_3ST < 20 + 1e-8 else 'FAIL'}")

# This is with fixed n = e_1. But we need it for all n.
# Test with random n:
print("\nWith random n:")
max_3ST_rn = -np.inf
for _ in range(5000):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    n = np.random.randn(3)
    n /= np.linalg.norm(n)

    S = sum(n @ R[mu] @ n for mu in range(4))

    T = 0.0
    for mu, nu in planes:
        sigma = sigmas[(mu,nu)]
        d = n @ R[mu] @ D[(mu,nu)] @ n
        f = n @ R[mu] @ D[(mu,nu)] @ R[nu].T @ n
        e = n @ D[(mu,nu)] @ n
        dp = n @ D[(mu,nu)] @ R[nu].T @ n
        T += sigma * (d + f + e + dp)

    val = 3*S + T
    max_3ST_rn = max(max_3ST_rn, val)

print(f"  Max 3S + T over 5000 trials: {max_3ST_rn:.6f}")
print(f"  RESULT: {'PASS' if max_3ST_rn < 20 + 1e-8 else 'FAIL'}")

print("\nDone with Stage 3 — proof analysis.")
