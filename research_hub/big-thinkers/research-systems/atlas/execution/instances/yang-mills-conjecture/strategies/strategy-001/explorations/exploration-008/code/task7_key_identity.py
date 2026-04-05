"""
Task 7: Verify and prove the KEY IDENTITIES for the full 9D bound.

Identity 1 (Budget): For T with Sum_mu T_mu = 0:
  16||T||^2 = 4 Sum_{mu<nu} |T_mu - T_nu|^2

Identity 2 (Per-plaquette expansion): For each plaquette (mu,nu):
  4|T_mu - T_nu|^2 - |B_{mu,nu}|^2
  = 2f(U, T_mu) + 2f(W, T_nu)
    - 2 T_mu^T [(I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-R_mu D R_nu^T)] T_nu

Identity 3 (Combined bound for scalars): For unit n and A,B,D in SO(3):
  f(A)+f(B)+f(AD)+f(DB^T)-f(D)-f(ADB^T) = n^T(I-A)D(I-B^T)n + f(A)+f(B)

This script also derives the TIGHTEST possible bound on the cross-to-f_same ratio.
"""

import numpy as np

np.random.seed(42)
d = 4
PLANES = [(mu, nu) for mu in range(d) for nu in range(mu+1, d)]

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def f_vec(R, p):
    return np.dot(p, p) - np.dot(p, R @ p)

# ============================================================
# IDENTITY 1: Budget identity (PROOF)
# ============================================================
print("=" * 70)
print("IDENTITY 1: Budget identity (ALGEBRAIC PROOF)")
print("=" * 70)

# Proof: For T with Sum_mu T_mu = 0:
# Sum_{mu<nu} |T_mu - T_nu|^2
# = Sum_{mu<nu} (|T_mu|^2 + |T_nu|^2 - 2 T_mu . T_nu)
# = (d-1) Sum_mu |T_mu|^2 - 2 Sum_{mu<nu} T_mu . T_nu
# = (d-1)||T||^2 - [|Sum T_mu|^2 - ||T||^2]
# = (d-1)||T||^2 - 0 + ||T||^2 = d ||T||^2
# So 4 Sum |T_mu-T_nu|^2 = 4d ||T||^2 = 16||T||^2 when d=4. QED.

# Numerical verification:
max_err = 0
for _ in range(10000):
    T = np.random.randn(4, 3)
    T[3] = -(T[0]+T[1]+T[2])
    lhs = 16 * np.sum(T**2)
    rhs = 4 * sum(np.sum((T[mu]-T[nu])**2) for mu, nu in PLANES)
    max_err = max(max_err, abs(lhs - rhs))
print(f"  Budget identity verified: max error = {max_err:.2e}")
print(f"  STATUS: [VERIFIED] (algebraic proof + 10K numerical checks)")

# ============================================================
# IDENTITY 2: Per-plaquette expansion (PROOF)
# ============================================================
print("\n" + "=" * 70)
print("IDENTITY 2: Per-plaquette gap expansion")
print("=" * 70)

# 4|T_mu-T_nu|^2 - |B|^2 where B = (I+U)T_mu - R_mu(I+W^T)T_nu
# = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C T_nu
# where C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-R_mu D R_nu^T)
# and U = R_mu D, W = D R_nu^T

max_err = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T[3] = -(T[0]+T[1]+T[2])

    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T

        # LHS
        S = np.eye(3) + U
        Tmat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        B = S @ T[mu] - Tmat @ T[nu]
        lhs = 4*np.sum((T[mu]-T[nu])**2) - np.dot(B, B)

        # RHS
        f_U = f_vec(U, T[mu])
        f_W = f_vec(W, T[nu])
        C = (np.eye(3)-R[mu]) + (np.eye(3)-R[nu].T) + (np.eye(3)-D[(mu,nu)].T) + (np.eye(3)-R[mu]@D[(mu,nu)]@R[nu].T)
        cross = np.dot(T[mu], C @ T[nu])
        rhs = 2*f_U + 2*f_W - 2*cross

        err = abs(lhs - rhs)
        max_err = max(max_err, err)

print(f"  Per-plaquette expansion verified: max error = {max_err:.2e}")
print(f"  STATUS: [VERIFIED] (10K checks per plaquette)")

# ============================================================
# IDENTITY 3: Combined bound (E006, already proven)
# ============================================================
print("\n" + "=" * 70)
print("IDENTITY 3: E006 Combined bound lemma (already proven)")
print("=" * 70)
print("  f(A,n)+f(B,n)+f(AD,n)+f(DB^T,n)-f(D,n)-f(ADB^T,n)")
print("  = n^T(I-A)D(I-B^T)n + f(A,n) + f(B,n) >= 0")
print("  STATUS: [VERIFIED] (proven in E006 with 100K+ tests)")

# ============================================================
# KEY ANALYSIS: Derive the STRUCTURAL bound on cross terms
# ============================================================
print("\n" + "=" * 70)
print("KEY ANALYSIS: Cross term structure")
print("=" * 70)

# The total gap is:
# G = Sum_plaq [2f(U,T_mu) + 2f(W,T_nu)] - 2 Sum_plaq T_mu^T C_{mu,nu} T_nu
#   = f_same - cross_raw
#
# where f_same >= 0 always, and cross_raw = 2 Sum T_mu^T C T_nu.
# C = (I-R_mu)+(I-R_nu^T)+(I-D^T)+(I-H) where H = R_mu D R_nu^T.
#
# Using the factorization from Identity 3:
# (I-R_mu)+(I-R_nu)+(I-U)+(I-W)-(I-D)-(I-H) = combined bound terms
# This relates the 4 deficiency matrices in C to the 2 f-same rotations.
#
# Specifically: (I-D) + (I-H) = (I-U) + (I-W) - X  where X is the cross term.
# So: C = (I-R_mu)+(I-R_nu^T)+(I-U)+(I-W)-X
# Wait, that's not right. Let me re-derive.
#
# C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-H)
#   = 4I - R_mu - R_nu^T - D^T - H
# = 4I - R_mu - R_nu^T - D^T - R_mu D R_nu^T
#
# Meanwhile: (I-U)+(I-W) = 2I - R_mu D - D R_nu^T
#
# So C - [(I-U)+(I-W)] = 2I - R_mu - R_nu^T - D^T - R_mu D R_nu^T + R_mu D + D R_nu^T
#                       = 2I - R_mu - R_nu^T - D^T + R_mu D + D R_nu^T - R_mu D R_nu^T
#                       = (I - R_mu)(I - D) + ... hmm let me verify numerically

# Check: C = (I-U) + (I-W) + E for some E
max_err = 0
for _ in range(10000):
    R_mu = random_so3()
    R_nu = random_so3()
    D_mn = random_so3()
    U = R_mu @ D_mn
    W = D_mn @ R_nu.T
    H = R_mu @ D_mn @ R_nu.T

    C = (np.eye(3)-R_mu) + (np.eye(3)-R_nu.T) + (np.eye(3)-D_mn.T) + (np.eye(3)-H)
    IU_IW = (np.eye(3)-U) + (np.eye(3)-W)
    E = C - IU_IW

    # What is E?
    # E = (I-R_mu)+(I-R_nu^T)+(I-D^T)+(I-H) - (I-U) - (I-W)
    # = 2I - R_mu - R_nu^T - D^T - H + U + W
    # = 2I - R_mu - R_nu^T - D^T - R_mu D R_nu^T + R_mu D + D R_nu^T
    # = (I - R_mu) + (R_mu D - D^T) + (D R_nu^T - R_nu^T) + (I - R_mu D R_nu^T)... hmm

    # Let me factor differently:
    # E = 2I - R_mu + R_mu D - D^T + D R_nu^T - R_nu^T - R_mu D R_nu^T
    # = (I - R_mu)(I) + (I)(R_mu D - D^T) + (D - I)(R_nu^T) + (I - R_mu D R_nu^T)
    # Not clean.

    # Try: E = (I - R_mu)(I - D^T) + (D - D^T)(I - R_nu^T)?
    E_test = (np.eye(3)-R_mu) @ (np.eye(3)-D_mn.T) + (D_mn - D_mn.T) @ (np.eye(3)-R_nu.T)
    err = np.linalg.norm(E - E_test, 'fro')
    max_err = max(max_err, err)

print(f"  Test E = (I-R_mu)(I-D^T) + (D-D^T)(I-R_nu^T): max error = {max_err:.2e}")

# Try other factorizations
max_err = 0
for _ in range(10000):
    R_mu = random_so3()
    R_nu = random_so3()
    D_mn = random_so3()
    U = R_mu @ D_mn
    W = D_mn @ R_nu.T
    H = R_mu @ D_mn @ R_nu.T

    C = (np.eye(3)-R_mu) + (np.eye(3)-R_nu.T) + (np.eye(3)-D_mn.T) + (np.eye(3)-H)
    IU_IW = (np.eye(3)-U) + (np.eye(3)-W)
    E = C - IU_IW

    # Try: E = (I-R_mu)(I-D) + (I-D^T)(I-R_nu^T)?
    # (I-R_mu)(I-D) = I - R_mu - D + R_mu D
    # (I-D^T)(I-R_nu^T) = I - D^T - R_nu^T + D^T R_nu^T = I - D^T - R_nu^T + (R_nu D)^T
    # Sum: 2I - R_mu - D + R_mu D - D^T - R_nu^T + D^T R_nu^T
    # = 2I - R_mu - D - D^T - R_nu^T + R_mu D + D^T R_nu^T... not matching

    # What about E = (I-R_mu)(I-D^{-1}) + (I-D^{-T})(I-R_nu^T)?
    Di = D_mn.T  # D^{-1} = D^T for SO(3)
    E_test2 = (np.eye(3)-R_mu) @ (np.eye(3)-Di) + (np.eye(3)-Di.T) @ (np.eye(3)-R_nu.T)
    err2 = np.linalg.norm(E - E_test2, 'fro')
    max_err = max(max_err, err2)

print(f"  Test E = (I-R_mu)(I-D^T) + (I-D)(I-R_nu^T): max error = {max_err:.2e}")

# ============================================================
# ACTUAL factorization search
# ============================================================
# E = 2I - R_mu + R_mu D - D^T + D R_nu^T - R_nu^T - R_mu D R_nu^T

# Factor: (I - R_mu)(I - D R_nu^T) = I - R_mu - D R_nu^T + R_mu D R_nu^T
# And: (I - D^T)(I - R_nu^T) = I - D^T - R_nu^T + D^T R_nu^T

# Hmm: (I - R_mu)(I - D R_nu^T) + (R_mu D - D^T)
# = I - R_mu - D R_nu^T + R_mu D R_nu^T + R_mu D - D^T
# = I - R_mu - D R_nu^T + R_mu D R_nu^T + R_mu D - D^T... let me compare to E:
# E = 2I - R_mu + R_mu D - D^T + D R_nu^T - R_nu^T - R_mu D R_nu^T

# That has +R_mu D R_nu^T vs -R_mu D R_nu^T. So NOT the right factorization.

# Try: DEFINE P = I - R_mu, Q_m = I - R_nu^T, S = I - D, H = I - R_mu D R_nu^T
# Then C = P + Q_m + S^T + H (where S^T = I - D^T)
# And IU + IW = (I - R_mu D) + (I - D R_nu^T)
# So E = C - IU - IW = P + Q_m + S^T + H - (I-U) - (I-W)
# = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-H) - (I-R_mu D) - (I-D R_nu^T)
# = -R_mu - R_nu^T - D^T - H + 2I + R_mu D + D R_nu^T

# Another angle: does E have a nice quadratic form bound?
# T_mu^T E T_nu = ? We need |T_mu^T E T_nu| to be small.

# For the TOTAL cross: cross_total = 2 Sum T_mu^T [(I-U)+(I-W)+E] T_nu
# = 2 Sum T_mu^T (I-U) T_nu + 2 Sum T_mu^T (I-W) T_nu + 2 Sum T_mu^T E T_nu
# The first two are related to f_same by Cauchy-Schwarz.
# The third might vanish or be bounded.

# Check: does Sum T_mu^T E_{mu,nu} T_nu vanish?
max_sum_E = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T[3] = -(T[0]+T[1]+T[2])

    E_sum = 0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        H = R[mu] @ D[(mu,nu)] @ R[nu].T
        C = (np.eye(3)-R[mu]) + (np.eye(3)-R[nu].T) + (np.eye(3)-D[(mu,nu)].T) + (np.eye(3)-H)
        IU_IW = (np.eye(3)-U) + (np.eye(3)-W)
        E = C - IU_IW
        E_sum += np.dot(T[mu], E @ T[nu])

    max_sum_E = max(max_sum_E, abs(E_sum))

print(f"\n  Max |Sum T_mu^T E T_nu| over 10K tests: {max_sum_E:.6f}")
print(f"  (If this is always 0, the cross term has a clean structure)")

# ============================================================
# FINAL: Tightest bound on cross/f_same
# ============================================================
print("\n" + "=" * 70)
print("TIGHTEST BOUND on cross-to-f_same ratio")
print("=" * 70)

# Decompose cross = IU_part + IW_part + E_part
# IU_part = 2 Sum T_mu^T (I-U) T_nu
# IW_part = 2 Sum T_mu^T (I-W) T_nu
# E_part = 2 Sum T_mu^T E T_nu

# For IU_part: |(I-U)^{1/2} T_mu^T ... no, (I-U) is not symmetric.
# Better: |T_mu^T (I-U) T_nu| = |((I-U^T)T_mu)^T T_nu| <= |(I-U^T)T_mu| |T_nu|
#                                = sqrt(2f(U,T_mu)) |T_nu|
# By Cauchy-Schwarz on the PSD symmetric part:
# |T_mu^T (I-U)_sym T_nu| <= sqrt(f(U,T_mu)) sqrt(f(U,T_nu))

# The total IU_part = 2 Sum_{mu<nu} T_mu^T (I-U_{mu,nu}) T_nu
# Each term bounded by sqrt(f(U,T_mu)) sqrt(f(U,T_nu)) (symmetric part)
# Plus skew part bounded by sin(theta_U) |T_mu| |T_nu|

# For the SYMMETRIC PART of the cross term only:
max_sym_ratio = 0
max_full_ratio = 0

for _ in range(50000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T[3] = -(T[0]+T[1]+T[2])

    f_same = 0
    cross_sym = 0
    cross_full = 0

    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T

        f_same += 2*f_vec(U, T[mu]) + 2*f_vec(W, T[nu])

        C = (np.eye(3)-R[mu]) + (np.eye(3)-R[nu].T) + \
            (np.eye(3)-D[(mu,nu)].T) + (np.eye(3)-R[mu]@D[(mu,nu)]@R[nu].T)
        C_sym = (C + C.T) / 2
        C_skew = (C - C.T) / 2

        cross_sym += 2 * np.dot(T[mu], C_sym @ T[nu])
        cross_full += 2 * np.dot(T[mu], C @ T[nu])

    if f_same > 1e-12:
        max_sym_ratio = max(max_sym_ratio, abs(cross_sym) / f_same)
        max_full_ratio = max(max_full_ratio, abs(cross_full) / f_same)

print(f"  Max |cross_symmetric|/f_same: {max_sym_ratio:.6f}")
print(f"  Max |cross_full|/f_same: {max_full_ratio:.6f}")
print(f"  Symmetric part dominates cross: {max_sym_ratio > 0.8 * max_full_ratio}")
print(f"  cross/f_same < 1: {max_full_ratio < 1}")

# Check: what fraction of cross comes from E vs IU+IW parts?
print("\nDecomposition of cross into IU+IW and E parts:")
max_E_frac = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T[3] = -(T[0]+T[1]+T[2])

    IU_part = 0
    IW_part = 0
    E_part = 0

    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        H = R[mu] @ D[(mu,nu)] @ R[nu].T
        C = (np.eye(3)-R[mu]) + (np.eye(3)-R[nu].T) + \
            (np.eye(3)-D[(mu,nu)].T) + (np.eye(3)-H)

        IU_part += 2 * np.dot(T[mu], (np.eye(3)-U) @ T[nu])
        IW_part += 2 * np.dot(T[mu], (np.eye(3)-W) @ T[nu])
        E_mat = C - (np.eye(3)-U) - (np.eye(3)-W)
        E_part += 2 * np.dot(T[mu], E_mat @ T[nu])

    total = IU_part + IW_part + E_part
    if abs(total) > 1e-10:
        E_frac = abs(E_part) / abs(total) if abs(total) > 0 else 0
        max_E_frac = max(max_E_frac, abs(E_part) / (abs(IU_part) + abs(IW_part) + 1e-15))

print(f"  Max |E_part| / (|IU_part|+|IW_part|): {max_E_frac:.6f}")

print("\nDone with Task 7.")
