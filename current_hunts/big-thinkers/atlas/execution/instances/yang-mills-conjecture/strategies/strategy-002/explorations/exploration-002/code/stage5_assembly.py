"""
Stage 5: Assembly of the proof strategy and verification of key lemma.

Summary of what we've established:

ALGEBRAIC IDENTITIES (verified numerically):
  total_gap = 16||T||^2 - F_x(Q,T)
            = f_same + cross
            = f_same + 2*sum_mu f(R_mu, T_mu) + cross_D + cross_RDR
            = 2*sum_mu f(R_mu, T_mu) + sum_S

where sum_S = sum_{mu<nu} S_{mu,nu} and
  S_{mu,nu} = 2f(U_munu, T_mu) + 2f(W_munu, T_nu)
              - 2 T_mu^T (I-D^T_{munu}) T_nu
              - 2 T_mu^T (I-R_mu D_{munu} R_nu^T) T_nu

PROVED:
  P1. 2*sum_mu f(R_mu, T_mu) >= 0  [trivially, each f >= 0]
  P2. Vector CBL: p^T(I-A)D(I-B^T)q + f(A,p) + f(B,q) >= 0  [by C-S + AM-GM]
  P3. Per-plaquette VCB_S >= 0 [from vector CBL with D_inner=I]

NUMERICALLY VERIFIED:
  N1. sum_S >= 0 (100K tests, min = 2.63)
  N2. total_gap >= 0 (no violations in 200K+ tests)

KEY REMAINING LEMMA:
  Prove sum_S = sum_{mu<nu} S_{mu,nu} >= 0 for all T in V, all Q.

This exploration focuses on:
1. Verifying the complete proof structure assembles correctly
2. Checking if sum_S = 0 occurs (would identify saturation configs)
3. Testing a candidate algebraic proof of sum_S >= 0
4. Summarizing the proof gap
"""

import numpy as np

np.random.seed(999)
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

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def f_vec(R, p):
    return float(p @ p - p @ R @ p)

def compute_S(R, D_mat, T, mu, nu):
    p, q = T[mu], T[nu]
    U = R[mu] @ D_mat[(mu, nu)]
    W = D_mat[(mu, nu)] @ R[nu].T
    return (2*f_vec(U, p) + 2*f_vec(W, q)
            - 2 * float(p @ (np.eye(3) - D_mat[(mu,nu)].T) @ q)
            - 2 * float(p @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ q))

def build_M12(R, D):
    M = np.zeros((12, 12))
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu, nu)]
        S = np.eye(3) + U
        Tmat = R[mu] + U @ R[nu].T
        M[3*mu:3*(mu+1), 3*mu:3*(mu+1)] += S.T @ S
        M[3*nu:3*(nu+1), 3*nu:3*(nu+1)] += Tmat.T @ Tmat
        M[3*mu:3*(mu+1), 3*nu:3*(nu+1)] -= S.T @ Tmat
        M[3*nu:3*(nu+1), 3*mu:3*(mu+1)] -= Tmat.T @ S
    return M

def make_projector():
    V = np.zeros((12, 9))
    idx = 0
    for mu in range(3):
        for a in range(3):
            v = np.zeros(12)
            v[3*mu + a] = 1.0
            v[3*3 + a] = -1.0
            V[:, idx] = v
            idx += 1
    Q_mat, _ = np.linalg.qr(V)
    return Q_mat[:, :9]

P_V = make_projector()

# ============================================================
# ASSEMBLY 1: Verify the complete decomposition identity
# ============================================================
print("=" * 70)
print("ASSEMBLY 1: Complete decomposition identity")
print("  total_gap = 2*sum_mu f(R_mu,T_mu) + sum_S")
print("=" * 70)

max_err = 0
for _ in range(50000):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    # Direct total_gap
    M = build_M12(R, D_mat)
    vec_T = T.flatten()
    total_gap_direct = 16 * np.sum(T**2) - float(vec_T @ M @ vec_T)

    # Decomposed
    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    sum_S = sum(compute_S(R, D_mat, T, mu, nu) for mu, nu in PLANES)
    total_gap_decomp = term1 + sum_S

    max_err = max(max_err, abs(total_gap_direct - total_gap_decomp))

print(f"  Max error in decomposition: {max_err:.2e}")
print(f"  Identity VERIFIED: {max_err < 1e-9}")

# ============================================================
# ASSEMBLY 2: Both parts always >= 0
# ============================================================
print("\n" + "=" * 70)
print("ASSEMBLY 2: Verify term1 >= 0 and sum_S >= 0 simultaneously")
print("=" * 70)

N_tests = 200000
min_term1 = float('inf')
min_sum_S = float('inf')
min_total = float('inf')
term1_viol = sum_S_viol = total_viol = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    sum_S = sum(compute_S(R, D_mat, T, mu, nu) for mu, nu in PLANES)
    total = term1 + sum_S

    min_term1 = min(min_term1, term1)
    min_sum_S = min(min_sum_S, sum_S)
    min_total = min(min_total, total)
    if term1 < -1e-10: term1_viol += 1
    if sum_S < -1e-10: sum_S_viol += 1
    if total < -1e-10: total_viol += 1

print(f"  N tests: {N_tests}")
print(f"  Min term1 = 2*sum f(R_mu,T_mu): {min_term1:.6f}, violations: {term1_viol}")
print(f"  Min sum_S: {min_sum_S:.6f}, violations: {sum_S_viol}")
print(f"  Min total_gap = term1 + sum_S: {min_total:.6f}, violations: {total_viol}")
print(f"\n  PROOF STRATEGY VIABLE: {term1_viol == 0 and sum_S_viol == 0}")
print(f"  (Missing piece: algebraic proof that sum_S >= 0)")

# ============================================================
# ASSEMBLY 3: Adversarial test for sum_S
# ============================================================
print("\n" + "=" * 70)
print("ASSEMBLY 3: Adversarial minimization of sum_S")
print("  Q: What is the minimum value of sum_S achievable?")
print("  (If it can reach 0, the bound is tight. If min >> 0, there's slack.)")
print("=" * 70)

def compute_sum_S_and_term1(R, D_mat, T):
    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    sum_S = sum(compute_S(R, D_mat, T, mu, nu) for mu, nu in PLANES)
    return term1, sum_S

N_adversarial = 30
best_sum_S = float('inf')

for trial in range(N_adversarial):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    step = 0.02

    for iteration in range(200):
        # Find worst T = top eigenvector of M12 restricted to V
        M = build_M12(R, D_mat)
        M9 = P_V.T @ M @ P_V
        eigs, vecs = np.linalg.eigh(M9)
        T = (P_V @ vecs[:, -1]).reshape(4, 3)

        # Compute sum_S for this T
        t1, sS = compute_sum_S_and_term1(R, D_mat, T)
        if sS < best_sum_S:
            best_sum_S = sS

        # Gradient descent on sum_S (try to minimize it)
        eps = 1e-5
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = list(R); R_p[mu] = so3_exp(omega) @ R[mu]
                _, sS_p = compute_sum_S_and_term1(R_p, D_mat, T)
                g = (sS_p - sS) / eps
                R[mu] = so3_exp(-step * g * np.eye(3)[k]) @ R[mu]

        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D_mat); D_p[p] = so3_exp(omega) @ D_mat[p]
                _, sS_p = compute_sum_S_and_term1(R, D_p, T)
                g = (sS_p - sS) / eps
                D_mat[p] = so3_exp(-step * g * np.eye(3)[k]) @ D_mat[p]

        if iteration % 50 == 49:
            step *= 0.8

    if (trial + 1) % 10 == 0:
        print(f"  Trial {trial+1}/30, best min sum_S = {best_sum_S:.6f}")

print(f"\n  BEST adversarial min sum_S = {best_sum_S:.6f}")
print(f"  min sum_S > 0: {best_sum_S > -1e-10}")
print(f"  Gap from 0: {best_sum_S:.4f} (smaller gap = harder to prove bound)")

# ============================================================
# ASSEMBLY 4: Structure of sum_S at adversarial minimum
# ============================================================
print("\n" + "=" * 70)
print("ASSEMBLY 4: Uniform color case — exact formula for sum_S")
print("  For T_mu = s_mu * n: S_{mu,nu} = 2 * s_mu * s_nu * n^T(I-R_mu)D(I-R_nu^T)n")
print("  sum_S = 2 * sum_{mu<nu} s_mu*s_nu * n^T(I-R_mu)D_munu(I-R_nu^T)n")
print("=" * 70)

N_tests = 10000
min_sum_S_uniform = float('inf')
sum_S_uniform_viol = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    n = np.random.randn(3)
    # Random s in V = {s: sum s_mu = 0}
    s = np.random.randn(4)
    s -= s.mean()
    T = np.outer(s, n)  # T[mu] = s_mu * n

    sum_S = sum(compute_S(R, D_mat, T, mu, nu) for mu, nu in PLANES)
    min_sum_S_uniform = min(min_sum_S_uniform, sum_S)
    if sum_S < -1e-10:
        sum_S_uniform_viol += 1

print(f"  Min sum_S (uniform color): {min_sum_S_uniform:.6f}, violations: {sum_S_uniform_viol}")
print(f"  For uniform color, sum_S = 2*sum_munu s_mu*s_nu * n^T(I-R_mu)D(I-R_nu^T)n")
print(f"  This is >= 0 by the E006 CBL proof (for the specific staggered pattern s)")

# Check: for s = staggered = (1,-1,1,-1)/2, each term s_mu*s_nu has definite sign
s_stag = np.array([1, -1, 1, -1]) / 2
print(f"\n  Staggered s pattern: s_mu*s_nu products:")
for mu, nu in PLANES:
    print(f"    ({mu},{nu}): s_mu*s_nu = {s_stag[mu]*s_stag[nu]:+.4f}")

# ============================================================
# ASSEMBLY 5: Candidate algebraic proof of sum_S >= 0
# ============================================================
print("\n" + "=" * 70)
print("ASSEMBLY 5: Candidate algebraic proof attempt for sum_S >= 0")
print("  Apply vector CBL to paired plaquettes")
print("=" * 70)

# IDEA: Group the 6 plaquettes into 3 pairs:
# Pair A: (0,1) and (2,3)  [μ+ν = odd pairs]
# Pair B: (0,2) and (1,3)  [μ+ν = even pairs]
# Pair C: (0,3) and (1,2)
#
# For each pair, try to apply a 2-plaquette vector CBL.
# S_{mu,nu} + S_{mu',nu'} >= 0 for each pair?

PAIRS = [[(0,1),(2,3)], [(0,2),(1,3)], [(0,3),(1,2)]]

N_tests = 50000
for i, pair in enumerate(PAIRS):
    (mu1,nu1), (mu2,nu2) = pair
    min_pair_S = float('inf')
    pair_viol = 0

    for _ in range(N_tests):
        R = [random_so3() for _ in range(d)]
        D_mat = {p: random_so3() for p in PLANES}
        T = np.random.randn(4, 3)
        T -= T.mean(axis=0)

        S1 = compute_S(R, D_mat, T, mu1, nu1)
        S2 = compute_S(R, D_mat, T, mu2, nu2)
        pair_sum = S1 + S2

        min_pair_S = min(min_pair_S, pair_sum)
        if pair_sum < -1e-10:
            pair_viol += 1

    print(f"  Pair {i}: {pair}: min S_pair = {min_pair_S:.4f}, violations: {pair_viol}")

# Also check all 6 together
print(f"\n  Sum over ALL 6: min sum_S = {min_sum_S:.6f}")

# ============================================================
# ASSEMBLY 6: Apply scalar CBL to each plaquette in sum_S
# ============================================================
print("\n" + "=" * 70)
print("ASSEMBLY 6: Try scalar CBL on per-plaquette S_{mu,nu}")
print("  For uniform n: S = 2*n^T(I-R_mu)D(I-R_nu^T)n")
print("  CBL says: n^T(I-R_mu)D(I-R_nu^T)n >= -(f(R_mu,n) + f(R_nu,n))")
print("  So: 2*sum S >= -2 * 3 * sum f(R_mu,n) = -6 * sum f(R_mu,n)")
print("  total_gap (uniform) = term1 + sum_S >= 2*sum f - 6*sum f = -4*sum f")
print("  This bound is NEGATIVE — not sufficient!")
print("  The E006 proof needed MORE STRUCTURE (grouping by sign pattern)")
print("=" * 70)

# For GENERAL T, we need sum_S >= 0 without sign-pattern information.
# Key challenge: no sign structure for D-terms.

# OBSERVATION: For uniform color with ALL s_mu = 1 (would violate sum=0):
# sum_S = sum_{mu<nu} 2*1*1*n^T(I-R_mu)D(I-R_nu^T)n
# But Sigma s_mu = 0 means NOT all s_mu = 1.
# For general s with Sigma s_mu = 0: some s products are positive, some negative.

# BOUND via vector CBL for each plaquette:
# S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu
# = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T (2I - D^T - R_mu D R_nu^T) T_nu

# By vector CBL with A=U, B=W^T (note B^T = W), D_inner=I:
# VCB_S = T_mu^T(I-U)I(I-W^T)T_nu + f(U,T_mu) + f(W^T,T_nu) >= 0

# Note: (I-U)(I-W^T) = I - W^T - U + UW^T

# S - VCB_S = f(U,T_mu) + f(W,T_nu) - 2T_mu^T(2I-D^T-R_mu D R_nu^T)T_nu - T_mu^T(I-U)(I-W^T)T_nu

# For this sum Sigma(S - VCB_S) to help, we need to identify it as a known positive quantity.

# CLAIM: sum_{mu<nu} (S - VCB_S) = 2*Sigma_mu f(R_mu, T_mu)
# Let's check this numerically.

print("\nCheck: sum(S - VCB_S) = 2*sum f(R_mu, T_mu)?")
max_err_claim = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    sum_correction = 0
    for mu, nu in PLANES:
        p, q = T[mu], T[nu]
        U = R[mu] @ D_mat[(mu,nu)]
        W = D_mat[(mu,nu)] @ R[nu].T
        S = compute_S(R, D_mat, T, mu, nu)
        VCB_S = float(p @ (np.eye(3)-U) @ (np.eye(3)-W.T) @ q) + f_vec(U, p) + f_vec(W, q)
        sum_correction += S - VCB_S

    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    max_err_claim = max(max_err_claim, abs(sum_correction - term1))

print(f"  Max error in claim: {max_err_claim:.2e}")
if max_err_claim < 1e-8:
    print(f"  CLAIM HOLDS! sum(S - VCB_S) = 2*sum f(R_mu, T_mu) [VERIFIED]")
    print(f"  PROOF COMPLETE!")
    print(f"  sum_S = sum VCB_S + 2*sum f(R_mu)")
    print(f"        = [sum of vector CBL terms, each >= 0] + [2*sum f, >= 0]")
    print(f"        >= 0")
    print(f"  total_gap = 2*sum f(R_mu) + sum_S = 2*sum f(R_mu) + sum VCB_S + 2*sum f(R_mu)")
    print(f"            = 4*sum f(R_mu) + sum VCB_S >= 0")
else:
    print(f"  Claim does NOT hold exactly (error = {max_err_claim:.2e})")
    # Check if there's a simple relationship
    print(f"  Need to look for a different algebraic identity")

print("\n=== STAGE 5 COMPLETE ===")
