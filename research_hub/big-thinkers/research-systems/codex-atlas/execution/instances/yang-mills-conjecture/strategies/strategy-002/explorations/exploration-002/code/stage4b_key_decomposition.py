"""
Stage 4b: Deep investigation of the key decomposition found in TEST 7.

KEY FINDING: total_gap = 2*sum_mu f(R_mu, T_mu) + [f_same + cross_D + cross_RDR]
Both parts are individually >= 0 (numerically).

This suggests the PROOF STRUCTURE:
  total_gap = [non-negative term 1] + [non-negative term 2] >= 0

Term 1: 2 * sum_mu f(R_mu, T_mu)  -- trivially >= 0

Term 2: f_same + cross_D + cross_RDR  -- needs proof
  where:
  f_same = 2 sum_{mu<nu} [f(U_{mu,nu}, T_mu) + f(W_{mu,nu}, T_nu)]
  cross_D = sum_{mu<nu} (-2) T_mu^T (I-D^T_{mu,nu}) T_nu
  cross_RDR = sum_{mu<nu} (-2) T_mu^T (I-R_mu D_{mu,nu} R_nu^T) T_nu

Let S_{mu,nu} = f_sub_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu
Then Term 2 = sum_{mu<nu} S_{mu,nu}

KEY QUESTIONS:
1. Is S_{mu,nu} >= 0 per plaquette? (Would make Term 2 trivially >= 0)
2. If not, is sum S_{mu,nu} >= 0 via cancellation? Why?
3. Can we apply the Vector CBL to get S_{mu,nu} >= VCB - correction?
4. Is there an algebraic identity for S_{mu,nu}?
"""

import numpy as np

np.random.seed(789)
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
    return float(p @ p - p @ R @ p)

def compute_S(R, D_mat, T, mu, nu):
    """S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu"""
    p, q = T[mu], T[nu]
    U = R[mu] @ D_mat[(mu, nu)]
    W = D_mat[(mu, nu)] @ R[nu].T
    return (2*f_vec(U, p) + 2*f_vec(W, q)
            - 2 * float(p @ (np.eye(3) - D_mat[(mu,nu)].T) @ q)
            - 2 * float(p @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ q))

# ============================================================
# TEST A: Is S_{mu,nu} >= 0 per plaquette?
# ============================================================
print("=" * 70)
print("TEST A: Per-plaquette S_{mu,nu} >= 0?")
print("=" * 70)

N_tests = 100000
min_S = float('inf')
S_violations = 0
sum_S_violations = 0
min_sum_S = float('inf')

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)  # constraint

    sum_S = 0
    for mu, nu in PLANES:
        S = compute_S(R, D_mat, T, mu, nu)
        sum_S += S
        if S < min_S:
            min_S = S
        if S < -1e-10:
            S_violations += 1

    if sum_S < min_sum_S:
        min_sum_S = sum_S
    if sum_S < -1e-10:
        sum_S_violations += 1

print(f"  N tests: {N_tests} (Q,T) pairs, {N_tests*6} plaquette evaluations")
print(f"  Min S per plaquette: {min_S:.6f}")
print(f"  S per-plaquette violations: {S_violations}")
print(f"  Min sum_S: {min_sum_S:.6f}")
print(f"  sum_S violations: {sum_S_violations}")
print(f"  S >= 0 per plaquette: {S_violations == 0}")
print(f"  sum_S >= 0: {sum_S_violations == 0}")

# ============================================================
# TEST B: Algebraic identity for S_{mu,nu}
# ============================================================
print("\n" + "=" * 70)
print("TEST B: Algebraic identity for S_{mu,nu}")
print("  Claim: S = 2f(U,p) + 2f(W,q) - 2p^T(I-D^T)q - 2p^T(I-R_mu D R_nu^T)q")
print("  Try to write as (sum of) vector CBL terms")
print("=" * 70)

# For uniform color (p = q = n):
# S = 2f(U,n) + 2f(W,n) - 2n^T(I-D^T)n - 2n^T(I-R_mu D R_nu^T)n
# = 2f(U) + 2f(W) - 2f(D) - 2f(R_mu D R_nu^T)
# Using scalar CBL: f(U)+f(W)-f(D)-f(R_mu D R_nu^T) = n^T(I-R_mu)D(I-R_nu^T)n
# So S(p=q=n) = 2[n^T(I-R_mu)D(I-R_nu^T)n]

# Verify this for uniform color:
max_err_uniform = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    n = np.random.randn(3)
    T = np.array([n, n, n, -3*n])  # sum = 0
    T *= np.random.randn()  # scale

    mu, nu = 0, 1  # one plaquette
    S = compute_S(R, D_mat, T, mu, nu)
    # Formula for uniform (T_mu = a*n, T_nu = b*n):
    a, b = T[mu] @ n / (n @ n) if (n @ n) > 1e-12 else 1, T[nu] @ n / (n @ n) if (n @ n) > 1e-12 else 1
    # Actually just check for T_mu = T_nu = n
    p = n; q = n
    S2 = compute_S(R, D_mat, np.vstack([n, n, n, -3*n]), mu, nu)  # same as above
    formula = 2 * float(p @ (np.eye(3)-R[mu]) @ D_mat[(mu,nu)] @ (np.eye(3)-R[nu].T) @ q)
    max_err_uniform = max(max_err_uniform, abs(S2 - formula))

print(f"  Uniform color: S = 2*n^T(I-R_mu)D(I-R_nu^T)n, max error = {max_err_uniform:.2e}")
print(f"  Uniform identity holds: {max_err_uniform < 1e-10}")

# For general (p, q):
# S = 2f(U,p) + 2f(W,q) - 2p^T(I-D^T)q - 2p^T(I-R_mu D R_nu^T)q
# Let's try: does S = p^T A p + q^T B q + p^T C q where A, B, C can be identified?

# Expanding:
# S = 2(p^T p - p^T U p) + 2(q^T q - q^T W q)
#     - 2(p^T q - p^T D^T q)
#     - 2(p^T q - p^T R_mu D R_nu^T q)
# = 2p^T p - 2p^T U p + 2q^T q - 2q^T W q - 4p^T q + 2p^T D^T q + 2p^T R_mu D R_nu^T q
# = 2p^T(I-U)p + 2q^T(I-W)q - 4p^T q + 2p^T(D^T + R_mu D R_nu^T)q

# The 6x6 symmetric matrix form z = [p;q]:
# S = z^T M_S z where M_S = [[2(I-U)_sym, -(2I - D^T - R_mu D R_nu^T)];
#                             [-(2I - D - (R_mu D R_nu^T)^T), 2(I-W)_sym]]

# For S to be >= 0 per plaquette, M_S must be PSD.
# The Schur complement criterion: M_S >= 0 iff
#   2(I-W)_sym >= 0  [TRUE always]
#   2(I-U)_sym - (2I - D^T - R_mu D R_nu^T) * (2(I-W)_sym)^{-1} * (2I - D - (R_mu D R_nu^T)^T) >= 0

# Let's check: what is the minimum eigenvalue of M_S numerically?
print("\n  Checking M_S eigenvalues (is M_S >= 0?)...")
N_tests_eig = 10000
min_eig_MS = float('inf')
neg_eig_count = 0

for _ in range(N_tests_eig):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}

    mu, nu = 0, 1
    U = R[mu] @ D_mat[(mu, nu)]
    W = D_mat[(mu, nu)] @ R[nu].T
    Uprod = R[mu] @ D_mat[(mu, nu)] @ R[nu].T  # R_mu D R_nu^T

    # Symmetric part
    A_sym = 2 * (np.eye(3) - (U + U.T)/2)
    D_sym = 2 * (np.eye(3) - (W + W.T)/2)
    B = -(2*np.eye(3) - D_mat[(mu,nu)].T - Uprod)  # upper right block
    C = B.T  # lower left block

    M_S = np.block([[A_sym, B], [C, D_sym]])
    eigs = np.linalg.eigvalsh(M_S)
    min_eig_MS = min(min_eig_MS, eigs[0])
    if eigs[0] < -1e-10:
        neg_eig_count += 1

print(f"  Min eigenvalue of M_S: {min_eig_MS:.6f}")
print(f"  Configurations with neg eigenvalue: {neg_eig_count}/{N_tests_eig}")
print(f"  M_S PSD always: {neg_eig_count == 0}")

# ============================================================
# TEST C: Apply Vector CBL to S_{mu,nu}
# ============================================================
print("\n" + "=" * 70)
print("TEST C: Vector CBL analysis for S_{mu,nu}")
print("  S = 2f(U,p) + 2f(W,q) - 4p^T q + 2p^T(D^T + R_mu D R_nu^T)q")
print("  Candidate VCB for S: p^T(I-U)(I-W)q + f(U,p) + f(W,q)")
print("  Note: (I-U)(I-W) = I - W - U + UW")
print("  Does S >= candidate VCB?")
print("=" * 70)

# Try: S = [p^T(I-U)D(I-W^T)q + f(U,p) + f(W,q)] + [correction]
# correction = S - VCB

N_tests = 50000
min_VCB_S = float('inf')
VCB_S_violations = 0
min_correction_S = float('inf')
correction_S_violations = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        D_mn = D_mat[(mu, nu)]

        S = compute_S(R, D_mat, T, mu, nu)

        # Try VCB with A=U, B=W^T (so B^T=W), D_inner=I:
        # p^T(I-U)I(I-W)q + f(U,p) + f(W^T,q)
        # = p^T(I-U)(I-W)q + f(U,p) + f(W^T,q)
        # Note: f(W^T, q) = q^T(I-W^T)q = f(W,q)? No: f(W^T,q)=q^T(I-W^T)q, f(W,q)=q^T(I-W)q.
        # They differ. And the VCB uses B in f(B,q), not B^T. Here B = W^T, so f(B,q) = f(W^T,q) = f(W,q)?
        # Actually: for rotation W: f(W,q) = q^T(I-W)q and f(W^T,q) = q^T(I-W^T)q.
        # These are equal iff q^T W q = q^T W^T q, which holds since both equal q^T W q
        # (scalar transposition). Wait: q^T W^T q = (q^T W^T q)^T = q W q^T... no.
        # For real scalars: q^T W q is a 1x1 matrix = q^T W^T q (since (q^T W q)^T = q^T W^T q, and 1x1 matrix = its transpose).
        # So f(W, q) = f(W^T, q) always! Great.

        # VCB: p^T(I-U)I(I-W)q + f(U,p) + f(W^T,q) = p^T(I-U)(I-W)q + f(U,p) + f(W,q)
        VCB_S = float(p @ (np.eye(3)-U) @ (np.eye(3)-W) @ q) + f_vec(U, p) + f_vec(W, q)

        correction_S = S - VCB_S

        min_VCB_S = min(min_VCB_S, VCB_S)
        min_correction_S = min(min_correction_S, correction_S)
        if VCB_S < -1e-10:
            VCB_S_violations += 1
        if correction_S < -1e-10:
            correction_S_violations += 1

print(f"  VCB_S = p^T(I-U)(I-W)q + f(U,p) + f(W,q):")
print(f"    Min: {min_VCB_S:.8f}, violations: {VCB_S_violations}")
print(f"  correction_S = S - VCB_S:")
print(f"    Min: {min_correction_S:.6f}, violations: {correction_S_violations}")
print(f"  VCB_S is itself a vector CBL (D_inner=I): {VCB_S_violations == 0}")
print(f"  S >= VCB_S (correction_S >= 0): {correction_S_violations == 0}")

# ============================================================
# TEST D: Direct algebraic derivation of S
# ============================================================
print("\n" + "=" * 70)
print("TEST D: Derive S algebraically and look for vector CBL structure")
print("  S = 2p^T(I-U)p + 2q^T(I-W)q - 4p^T q + 2p^T(D^T + UW/U...)q")
print("  Let me compute VCB with A=U, B=W, D_inner=I and check")
print("  VCB(U, W, I) = p^T(I-U)I(I-W^T)q + f(U,p) + f(W,q)")
print("                = p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)")
print("=" * 70)

# VCB_check:
# p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)
# = p^T q - p^T W^T q - p^T U q + p^T U W^T q + p^T(I-U)p + q^T(I-W)q
#
# S: = 2p^T(I-U)p + 2q^T(I-W)q - 4p^T q + 2p^T D^T q + 2p^T R_mu D R_nu^T q
#
# correction_S = S - VCB_check:
# = 2p^T(I-U)p + 2q^T(I-W)q - 4p^T q + 2p^T D^T q + 2p^T R_mu D R_nu^T q
#   - [p^T(I-U)(I-W^T)q + p^T(I-U)p + q^T(I-W)q]
# = p^T(I-U)p + q^T(I-W)q - 4p^T q + 2p^T D^T q + 2p^T R_mu D R_nu^T q - p^T(I-U)(I-W^T)q
#
# Note: (I-U)(I-W^T) = I - W^T - U + UW^T
# p^T(I-U)(I-W^T)q = p^T q - p^T W^T q - p^T U q + p^T U W^T q
#
# correction_S = p^T(I-U)p + q^T(I-W)q - 4p^T q + 2p^T D^T q + 2p^T R_mu D R_nu^T q
#                - p^T q + p^T W^T q + p^T U q - p^T U W^T q
# = p^T(I-U)p + q^T(I-W)q + p^T(W^T + U - UW^T + 2D^T + 2R_mu D R_nu^T - 5I)q
#
# At Q=I: U=W=D=I, R_mu=R_nu=I
# = p^T 0 p + q^T 0 q + p^T(I+I-I+2I+2I-5I)q = 0 + p^T 0 q = 0. ✓

# Let's check if correction_S = f(something, p) + something or another VCB
N_tests = 50000
min_corr2 = float('inf')
corr2_violations = 0
for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T

        S = compute_S(R, D_mat, T, mu, nu)
        VCB_S = float(p @ (np.eye(3)-U) @ (np.eye(3)-W.T) @ q) + f_vec(U, p) + f_vec(W, q)
        corr = S - VCB_S

        min_corr2 = min(min_corr2, corr)
        if corr < -1e-10:
            corr2_violations += 1

print(f"  VCB(U, W^T, I) = p^T(I-U)(I-W^T^T)q + f(U,p) + f(W,q) -- wait, (I-W^T)^T = (I-W)")
print(f"  Let me use VCB(A=U, B=W, D=I) = p^T(I-U)(I-(W)^T)q + f(U,p) + f(W,q)")
print(f"  = p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)")
print(f"  Min correction S - VCB: {min_corr2:.6f}, violations: {corr2_violations}")

# ============================================================
# TEST E: Total sum approach — use sum_S >= 0 for proof
# ============================================================
print("\n" + "=" * 70)
print("TEST E: Sum of S over all plaquettes for constrained T")
print("  sum S = total_gap - 2*sum_mu f(R_mu, T_mu)")
print("  Both parts >= 0 — numerical verification")
print("=" * 70)

N_tests = 30000
min_sum_S = float('inf')
min_term1 = float('inf')
min_total = float('inf')
sum_S_viol = 0
term1_viol = 0
total_gap_viol = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    sum_S = sum(compute_S(R, D_mat, T, mu, nu) for mu, nu in PLANES)
    total_gap = term1 + sum_S

    min_sum_S = min(min_sum_S, sum_S)
    min_term1 = min(min_term1, term1)
    min_total = min(min_total, total_gap)
    if sum_S < -1e-10: sum_S_viol += 1
    if term1 < -1e-10: term1_viol += 1
    if total_gap < -1e-10: total_gap_viol += 1

print(f"  N tests: {N_tests}")
print(f"  Min term1 = 2*sum f(R_mu, T_mu): {min_term1:.6f}, violations: {term1_viol}")
print(f"  Min sum_S: {min_sum_S:.6f}, violations: {sum_S_viol}")
print(f"  Min total_gap = term1 + sum_S: {min_total:.6f}, violations: {total_gap_viol}")
print(f"\n  PROOF STRATEGY VIABLE: {term1_viol == 0 and sum_S_viol == 0}")

# ============================================================
# TEST F: Analyze sum_S algebraically
# ============================================================
print("\n" + "=" * 70)
print("TEST F: Algebraic structure of sum_S")
print("  sum_S = sum_{mu<nu} [2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu]")
print("  Note: -2T_mu^T(I-D^T)T_nu = 2T_nu^T(I-D)T_mu [by transposing scalar]")
print("        -2T_mu^T(I-R_mu D R_nu^T)T_nu = 2T_nu^T(I-R_nu D^T R_mu^T)T_mu [by transposing]")
print("  Symmetrize: combine (mu,nu) with (nu,mu) terms?")
print("=" * 70)

# Note: in our sum, (mu,nu) is ordered with mu < nu.
# The cross-link D_{mu,nu} goes from direction mu to nu.
# There's no separate D_{nu,mu} in the problem (only one cross-link per pair).

# But: -2T_mu^T(I-D^T)T_nu = 2T_nu^T D^T T_mu - 2T_nu^T T_mu = 2T_nu^T(D^T-I)T_mu = -2T_nu^T(I-D^T)T_mu
# Wait: -2T_mu^T(I-D^T)T_nu = transpose: -2T_nu^T(I-D)T_mu
#
# So: sum_{mu<nu} [-2T_mu^T(I-D^T)T_nu] = sum_{mu<nu} [-2T_nu^T(I-D)T_mu]
# This is the same sum just with T_mu and T_nu swapped (and D vs D^T).

# Can we apply the same "sum to zero" trick for D-terms?
# For D_{mu,nu}, the sum involves a different D for each (mu,nu) pair.
# Unlike R_mu which appears in multiple plaquettes, D_{mu,nu} appears ONLY in plaquette (mu,nu).
# So the "sum to zero" trick doesn't apply.

# Let's try a DIFFERENT approach: apply vector CBL directly to sum_S.
# VCB_sum = sum_{mu<nu} VCB_{mu,nu}(U, W, I) = sum_plaq [p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)]
# We showed: sum_S >= 0 and VCB_S >= 0 per plaquette.
# Is sum_S >= VCB_sum? (If yes, proof by VCB_sum >= 0)
# Is VCB_sum <= sum_S? (If no, different approach needed)

N_tests = 10000
min_sum_S2 = float('inf')
min_VCB_sum = float('inf')
min_diff2 = float('inf')
diff2_viol = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    sum_S = 0
    VCB_sum = 0
    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T

        S = compute_S(R, D_mat, T, mu, nu)
        VCB_S = float(p @ (np.eye(3)-U) @ (np.eye(3)-W.T) @ q) + f_vec(U, p) + f_vec(W, q)

        sum_S += S
        VCB_sum += VCB_S

    min_sum_S2 = min(min_sum_S2, sum_S)
    min_VCB_sum = min(min_VCB_sum, VCB_sum)
    min_diff2 = min(min_diff2, sum_S - VCB_sum)
    if sum_S - VCB_sum < -1e-10:
        diff2_viol += 1

print(f"  Min sum_S: {min_sum_S2:.6f}")
print(f"  Min VCB_sum: {min_VCB_sum:.6f}")
print(f"  Min (sum_S - VCB_sum): {min_diff2:.4f}")
print(f"  sum_S >= VCB_sum: {diff2_viol == 0}")

# ============================================================
# TEST G: Check per-plaquette S using the vector CBL with D_inner=D
# ============================================================
print("\n" + "=" * 70)
print("TEST G: Per-plaquette S vs VCB with D_inner = D_{mu,nu}")
print("  Try: VCB_D = p^T(I-U)D(I-W^T^T)q + f(U,p) + f(W,q)")
print("     = p^T(I-U)D(I-W^T)q + f(U,p) + f(W,q)")
print("  Note: W^T = R_nu D^T, so (I-W^T) = I - R_nu D^T")
print("=" * 70)

# VCB_D = p^T(I-R_mu D)D(I-R_nu D^T)q + f(R_mu D, p) + f(D R_nu^T, q)
# Let A' = R_mu D = U, B' = R_nu D^T [note: B'^T = D^T R_nu^T = W^T], D' = D_{mu,nu}
# Then p^T(I-A')D'(I-B'^T)q = p^T(I-U)D(I-R_nu D^T^T)q = p^T(I-U)D(I-D R_nu^T)q
# Hmm: B'^T = D^T R_nu^T ≠ D R_nu^T... Let me redo.
#
# Actually: D R_nu^T = W. So let B' = W^T = R_nu D^T. Then B'^T = (R_nu D^T)^T = D R_nu^T = W.
# And VCB(A=U, B=W^T, D=D): p^T(I-U)D(I-B'^T)q + f(U,p) + f(W^T,q)
# = p^T(I-U)D(I-W)q + f(U,p) + f(W,q)  [since f(W^T,q) = f(W,q)]
# = p^T(I-R_mu D)D_{mn}(I-D_{mn}R_nu^T)q + f(R_mu D, p) + f(D R_nu^T, q)

N_tests = 50000
min_VCB_D = float('inf')
VCB_D_viol = 0
min_corr_D = float('inf')
corr_D_viol = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        D_mn = D_mat[(mu, nu)]

        S = compute_S(R, D_mat, T, mu, nu)
        # VCB with A=U, B=W^T, D_inner=D:
        # p^T(I-U)D(I-W)q + f(U,p) + f(W^T,q) = p^T(I-U)D_mn(I-W)q + f(U,p) + f(W,q)
        VCB_D = float(p @ (np.eye(3)-U) @ D_mn @ (np.eye(3)-W) @ q) + f_vec(U, p) + f_vec(W, q)
        corr_D = S - VCB_D

        min_VCB_D = min(min_VCB_D, VCB_D)
        min_corr_D = min(min_corr_D, corr_D)
        if VCB_D < -1e-10:
            VCB_D_viol += 1
        if corr_D < -1e-10:
            corr_D_viol += 1

print(f"  VCB_D = p^T(I-U)D(I-W)q + f(U,p) + f(W,q):")
print(f"    Min: {min_VCB_D:.8f}, violations: {VCB_D_viol}")
print(f"  Correction S - VCB_D:")
print(f"    Min: {min_corr_D:.6f}, violations: {corr_D_viol}")
print(f"  S >= VCB_D: {corr_D_viol == 0}")

# ============================================================
# TEST H: Algebraic identity for S using CBL
# ============================================================
print("\n" + "=" * 70)
print("TEST H: Direct algebraic check — S = VCB_D + extra")
print("  VCB_D = p^T(I-U)D(I-W)q + f(U,p) + f(W,q)")
print("  S - VCB_D = ?")
print("=" * 70)

# S = 2f(U,p) + 2f(W,q) - 2p^T(I-D^T)q - 2p^T(I-R_mu D R_nu^T)q
# VCB_D = p^T(I-U)D(I-W)q + f(U,p) + f(W,q)
#       = p^T Dq - p^T DWq - p^T UDq + p^T UDWq + f(U,p) + f(W,q)
# where D = D_{mu,nu}, W = D R_nu^T, U = R_mu D
# DW = D * D R_nu^T = D^2 R_nu^T  [NOT a simple rotation unless D=I]
# UD = R_mu D * D = R_mu D^2
# UDW = R_mu D^2 * D R_nu^T = R_mu D^3 R_nu^T

# This doesn't simplify nicely. Let me try numerically what S - VCB_D equals.

R = [random_so3() for _ in range(d)]
D_mat = {p: random_so3() for p in PLANES}
T = np.random.randn(4, 3)
T -= T.mean(axis=0)

mu, nu = 0, 1
p = T[mu]; q = T[nu]
U = R[mu] @ D_mat[(mu,nu)]
W = D_mat[(mu,nu)] @ R[nu].T
D_mn = D_mat[(mu,nu)]
Uprod = R[mu] @ D_mn @ R[nu].T  # R_mu D R_nu^T

S = compute_S(R, D_mat, T, mu, nu)
VCB_D = float(p @ (np.eye(3)-U) @ D_mn @ (np.eye(3)-W) @ q) + f_vec(U, p) + f_vec(W, q)
diff_SD = S - VCB_D

print(f"\n  Sample: S = {S:.4f}, VCB_D = {VCB_D:.4f}, diff = {diff_SD:.4f}")

# S - VCB_D = 2f(U,p) + 2f(W,q) - 2p^T(I-D^T)q - 2p^T(I-Uprod)q
#             - [p^T(I-U)D(I-W)q + f(U,p) + f(W,q)]
# = f(U,p) + f(W,q) - 2p^T(I-D^T)q - 2p^T(I-Uprod)q - p^T(I-U)D(I-W)q

# Let me try to see if diff is another VCB-type term
# diff = f(U,p) + f(W,q) - 2p^T(2I - D^T - Uprod)q - p^T(I-U)D(I-W)q

# Try: diff = VCB3 where VCB3 = p^T M3 q + f(A3,p) + f(B3,q) for some A3, B3, M3?
# If f(U,p) = f(A3,p) and f(W,q) = f(B3,q), then A3 = U, B3 = W, and
# M3 = (I-A3)D3(I-B3^T) for some D3, and we need:
# p^T M3 q = -2p^T(2I-D^T-Uprod)q - p^T(I-U)D(I-W)q

# The LHS p^T(I-U)D3(I-W^T)q = p^T M3 q where D3 to be determined.
# Setting M3 = -2(2I-D^T-Uprod) - (I-U)D(I-W):
# = -(4I - 2D^T - 2Uprod) - (D - DW - UD + UDW)
# At Q=I: -(4I-2I-2I) - (I-I-I+I) = 0 - 0 = 0. ✓

print("\n  Structure of S - VCB_D:")
for trial in range(5):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    p = np.random.randn(3)
    q = np.random.randn(3)
    mu, nu = 0, 1
    U = R[mu] @ D_mat[(mu,nu)]
    W = D_mat[(mu,nu)] @ R[nu].T
    D_mn = D_mat[(mu,nu)]

    S_val = (2*f_vec(U, p) + 2*f_vec(W, q)
             - 2*float(p @ (np.eye(3)-D_mn.T) @ q)
             - 2*float(p @ (np.eye(3) - R[mu] @ D_mn @ R[nu].T) @ q))

    VCB_D_val = float(p @ (np.eye(3)-U) @ D_mn @ (np.eye(3)-W) @ q) + f_vec(U, p) + f_vec(W, q)
    diff_val = S_val - VCB_D_val
    print(f"  Trial {trial}: S={S_val:.4f}, VCB_D={VCB_D_val:.4f}, diff={diff_val:.4f}")

print("\n=== STAGE 4b COMPLETE ===")
