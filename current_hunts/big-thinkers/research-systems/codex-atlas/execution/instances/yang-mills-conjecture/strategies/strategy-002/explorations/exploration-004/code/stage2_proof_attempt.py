"""
Stage 2: Core proof attempt for sum_S >= 0.

Key findings from analysis:
1. Convexity in D FAILS (Hessian negative)
2. cross/budget ratio bounded at ~0.29 (promising!)
3. Per-plaquette VCBL fails but sum always recovers

Strategy: Prove sum_S >= 0 by showing cross <= budget for the TOTAL.
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

def random_T_in_V():
    T = {mu: np.random.randn(3) for mu in range(3)}
    T[3] = -T[0] - T[1] - T[2]
    return T

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

# ============================================================
# Manual Nelder-Mead for adversarial eigenvalue search
# ============================================================
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

print("=" * 60)
print("ADVERSARIAL: min eigenvalue search (manual optimization)")
print("=" * 60)

# Random search phase
best_val = float('inf')
best_params = None
for trial in range(2000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    if v < best_val:
        best_val = v
        best_params = p0.copy()
        if trial % 200 == 0:
            print(f"  trial {trial}: best = {best_val:.8f}")

print(f"  After 2000 random starts: best = {best_val:.10f}")

# Simple gradient descent with numerical gradient
def numerical_gradient(func, x, eps=1e-7):
    grad = np.zeros_like(x)
    f0 = func(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += eps
        grad[i] = (func(x_plus) - f0) / eps
    return grad

x = best_params.copy()
lr = 0.01
for step in range(500):
    g = numerical_gradient(min_eig_M9, x)
    x -= lr * g
    v = min_eig_M9(x)
    if v < best_val:
        best_val = v
        best_params = x.copy()
    if step % 100 == 0:
        print(f"  GD step {step}: val = {v:.10f}, best = {best_val:.10f}")

print(f"  FINAL min eigenvalue: {best_val:.12e}")

# ============================================================
# DETAILED EIGENVALUE ANALYSIS at minimizer
# ============================================================
print("\n" + "=" * 60)
print("MINIMIZER ANALYSIS")
print("=" * 60)

R_opt = {i: so3_from_vec(best_params[3*i:3*(i+1)]) for i in range(4)}
D_opt = {}
idx = 12
for p in PAIRS:
    D_opt[p] = so3_from_vec(best_params[idx:idx+3])
    idx += 3

M12_opt = build_M12(R_opt, D_opt)
M9_opt = P.T @ M12_opt @ P
M9_opt = (M9_opt + M9_opt.T) / 2
eigs_opt = np.linalg.eigvalsh(M9_opt)
print(f"  Eigenvalues of M9 at minimizer:")
print(f"  {eigs_opt}")

for i in range(4):
    angle = np.degrees(np.arccos(np.clip((np.trace(R_opt[i])-1)/2, -1, 1)))
    print(f"  R_{i} angle: {angle:.2f}°")
for p in PAIRS:
    angle = np.degrees(np.arccos(np.clip((np.trace(D_opt[p])-1)/2, -1, 1)))
    print(f"  D_{p} angle: {angle:.2f}°")

# Check: are all D near I?
print(f"\n  D distances from I:")
for p in PAIRS:
    dist = np.linalg.norm(D_opt[p] - I3, 'fro')
    print(f"  D_{p}: ||D-I||_F = {dist:.4f}")

# ============================================================
# CROSS / BUDGET RATIO: exhaustive adversarial search
# ============================================================
print("\n" + "=" * 60)
print("CROSS/BUDGET RATIO: adversarial search")
print("=" * 60)

# For the 9x9 matrix, write M9 = B9 - C9 where B9 is the budget (diagonal) part
# and C9 is the cross part. If B9 >= C9 as matrices (i.e., B9 - C9 >= 0), done.

def build_budget_cross_M12(R, D):
    """Build budget and cross parts separately."""
    B = np.zeros((12, 12))
    C = np.zeros((12, 12))
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        B[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*I3 - U - U.T
        B[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*I3 - W - W.T
        # The cross block: -(2I - D^T - RDR) appears as off-diagonal
        # sum_S cross = -2T^T(2I-D^T-RDR)T = cross contribution
        # In matrix form: off-diag block = D^T + RDR - 2I (I add this to M)
        # So the "negative" part is -(D^T + RDR - 2I) = 2I - D^T - RDR
        neg_cross = 2*I3 - D[(mu,nu)].T - RDR
        C[3*mu:3*mu+3, 3*nu:3*nu+3] += neg_cross
        C[3*nu:3*nu+3, 3*mu:3*mu+3] += neg_cross.T
    return B, C

# M = B - C. We want M >= 0 on V.
# Sufficient: B >= C on V, i.e., T^T B T >= T^T C T for all T in V.
# On V: t^T (P^T B P) t >= t^T (P^T C P) t, i.e., B9 >= C9.

# Check: is P^T C P always <= P^T B P?
max_ratio_eig = 0
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    B12, C12 = build_budget_cross_M12(R, D)
    B9 = P.T @ B12 @ P; B9 = (B9+B9.T)/2
    C9 = P.T @ C12 @ P; C9 = (C9+C9.T)/2

    # Generalized eigenvalue: C9 v = lambda B9 v
    # If max lambda < 1, then B9 > C9.
    eigs_B = np.linalg.eigvalsh(B9)
    if eigs_B[0] > 1e-10:  # B9 is PD
        # max eigenvalue of B9^{-1} C9
        eigs_gen = np.linalg.eigvalsh(np.linalg.solve(B9, C9))
        max_ratio_eig = max(max_ratio_eig, eigs_gen[-1])

print(f"  max generalized eigenvalue (C9 vs B9): {max_ratio_eig:.6f}")
if max_ratio_eig < 1:
    print(f"  *** B9 > C9 for all tested configs! ***")
    print(f"  This means sum_budget > sum_cross as matrices.")
else:
    print(f"  B9 >= C9 FAILS for some configs")

# But B9 might not be PD. Check:
min_eig_B = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    B12, _ = build_budget_cross_M12(R, D)
    B9 = P.T @ B12 @ P; B9 = (B9+B9.T)/2
    min_eig_B = min(min_eig_B, np.linalg.eigvalsh(B9)[0])

print(f"\n  min eigenvalue of B9: {min_eig_B:.6f}")
if min_eig_B < 1e-10:
    print(f"  B9 can be singular → generalized eigenvalue approach may not work directly")

# ============================================================
# ATTEMPT: Write sum_S = sum_VCBL + non-negative remainder
# ============================================================
print("\n" + "=" * 60)
print("VCBL DECOMPOSITION: sum_S = sum ||a-b||^2 + remainder")
print("=" * 60)

# 2*VCBL(U,W,-I,p,q) = ||a||^2 + ||b||^2 - 2a·b = ||a-b||^2
# where a = (I-U^T)p, b = (I-W^T)q
# S_{mu,nu} = ||a||^2 + ||b||^2 - 2p^T(2I-D^T-RDR)q

# remainder per pair = -2p^T[(2I-D^T-RDR) - (I-U)(I-W^T)]q
# = -2p^T Phi q where Phi = (2I-D^T-RDR) - (I-U-W^T+UW^T)
# = -2p^T [I - D^T - RDR + U + W^T - UW^T] q

# Let me compute and simplify Phi algebraically.
# Phi = I - D^T - RDR + U + W^T - UW^T
# = I - D^T - R_mu D R_nu^T + R_mu D + R_nu D^T - R_mu D R_nu D^T
# = I + R_mu D - D^T - R_mu D R_nu^T + R_nu D^T - R_mu D R_nu D^T
# Factor: group terms with R_mu D:
# = I + R_mu D(I - R_nu^T - R_nu D^T) + (R_nu - I) D^T
# Hmm, not clean. Let me try:
# = (I - D^T)(I - R_nu) + R_mu D(I - R_nu D^T)
# Check: (I-D^T)(I-R_nu) = I - R_nu - D^T + D^T R_nu
#         R_mu D(I - R_nu D^T) = R_mu D - R_mu D R_nu D^T
# Sum: I - R_nu - D^T + D^T R_nu + R_mu D - R_mu D R_nu D^T
# Compare with Phi: I + R_mu D - D^T - R_mu D R_nu^T + R_nu D^T - R_mu D R_nu D^T
# Not matching (R_nu vs R_nu D^T, etc.)

# Let me try numerical verification:
print("  Checking Phi structure...")
for trial in range(5):
    R_mu, R_nu = random_SO3(), random_SO3()
    D_mn = random_SO3()
    U = R_mu @ D_mn; W = D_mn @ R_nu.T; RDR = R_mu @ D_mn @ R_nu.T

    Phi = I3 - D_mn.T - RDR + U + W.T - U @ W.T
    # = I - D^T - R_mu D R_nu^T + R_mu D + R_nu D^T - R_mu D R_nu D^T

    # Try: Phi = (I - D^T + R_mu D)(I - R_nu D^T)?
    # (I - D^T + R_mu D)(I - R_nu D^T) = I - R_nu D^T - D^T + D^T R_nu D^T + R_mu D - R_mu D R_nu D^T
    test1 = (I3 - D_mn.T + R_mu @ D_mn) @ (I3 - R_nu @ D_mn.T)
    print(f"  Trial {trial}: ||Phi - test1|| = {np.linalg.norm(Phi - test1):.2e}")

    # Try: Phi = (R_mu - D^{-1})(D - R_nu^T)?
    test2 = (R_mu - np.linalg.inv(D_mn)) @ (D_mn - R_nu.T)
    print(f"           ||Phi - test2|| = {np.linalg.norm(Phi - test2):.2e}")

    # Try: Phi = (R_mu D - I)(I - D^T R_nu)?
    # wait, D^T = D^{-1}
    test3 = (R_mu @ D_mn - I3) @ (I3 - D_mn.T @ R_nu)
    # = (U - I)(I - D^{-1} R_nu)
    print(f"           ||Phi - (U-I)(I-D^T R_nu)|| = {np.linalg.norm(Phi - test3):.2e}")

    # Try other factorizations:
    # Phi = A B where A, B involve R_mu, R_nu, D
    # (R_mu D - D^T)(I - R_nu)?
    test4 = (R_mu @ D_mn - D_mn.T) @ (I3 - R_nu)
    print(f"           ||Phi - (U-D^T)(I-R_nu)|| = {np.linalg.norm(Phi - test4):.2e}")

    # (I + R_mu D)(I - R_nu D^T) - (I - D^T)(I - R_nu) ... combine?
    # Actually let me try:
    # Phi = (I-D^T)(I-R_nu) + (R_mu D)(I-R_nu D^T)
    test5 = (I3 - D_mn.T) @ (I3 - R_nu) + (R_mu @ D_mn) @ (I3 - R_nu @ D_mn.T)
    # = I - R_nu - D^T + D^T R_nu + R_mu D - R_mu D R_nu D^T
    print(f"           ||Phi - [(I-D^T)(I-R_nu) + U(I-R_nu D^T)]|| = {np.linalg.norm(Phi - test5):.2e}")

print("\n  Checking more factorizations...")
# Let me try the factorization (I + U - 2D^T)(I - R_nu) or similar
for trial in range(3):
    R_mu, R_nu = random_SO3(), random_SO3()
    D_mn = random_SO3()
    U = R_mu @ D_mn; W = D_mn @ R_nu.T; RDR = R_mu @ D_mn @ R_nu.T

    Phi = I3 - D_mn.T - RDR + U + W.T - U @ W.T

    # The successful factorization from above:
    # Phi = (I - D^T + U)(I - R_nu D^T)
    # But wait, test1 showed this does NOT match Phi.
    # Let me re-check: I get test1 = I - R_nu D^T - D^T + D^T R_nu D^T + U - U R_nu D^T
    # And Phi = I - D^T - RDR + U + R_nu D^T - U R_nu D^T
    #         = I - D^T - U R_nu^T + U + R_nu D^T - U R_nu D^T
    # These are different: test1 has -R_nu D^T + D^T R_nu D^T while Phi has +R_nu D^T - U R_nu^T

    # Let me try: Phi = (I - D^{-1})(D - R_nu^T) + (R_mu - D^{-1})(D R_nu^T - R_nu^T)?
    # Getting complicated. Let me focus on the sign instead.

    # For the PROOF we need: sum remainder = -2 sum p^T Phi q >= 0 when summed over pairs
    # with T in V. Or at least: sum_VCBL(-I) + sum_remainder = sum_S >= 0.

    # Since sum_VCBL(-I) >= 0 (each term is ||a-b||^2 >= 0), if sum remainder >= 0 we're done.
    # Check:
    R_test = {mu: random_SO3() for mu in range(4)}
    D_test = {p: random_SO3() for p in PAIRS}
    T_test = random_T_in_V()

    sum_vcbl = 0
    sum_rem = 0
    for mu, nu in PAIRS:
        U_t = R_test[mu] @ D_test[(mu,nu)]
        W_t = D_test[(mu,nu)] @ R_test[nu].T
        a = (I3 - U_t.T) @ T_test[mu]
        b = (I3 - W_t.T) @ T_test[nu]
        sum_vcbl += np.dot(a-b, a-b)

        Phi_t = (I3 - D_test[(mu,nu)].T - R_test[mu] @ D_test[(mu,nu)] @ R_test[nu].T
                 + U_t + W_t.T - U_t @ W_t.T)
        sum_rem += -2 * T_test[mu] @ Phi_t @ T_test[nu]

    print(f"  trial {trial}: VCBL={sum_vcbl:.3f}, rem={sum_rem:.3f}, total={sum_vcbl+sum_rem:.3f}")

# ============================================================
# CRITICAL: Sign of remainder across many trials
# ============================================================
print("\n" + "=" * 60)
print("REMAINDER SIGN: can it be negative?")
print("=" * 60)

min_rem = float('inf')
pos_count = 0
neg_count = 0
for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    sum_rem = 0.0
    for mu, nu in PAIRS:
        U_t = R[mu] @ D[(mu,nu)]
        W_t = D[(mu,nu)] @ R[nu].T
        Phi_t = (I3 - D[(mu,nu)].T - R[mu] @ D[(mu,nu)] @ R[nu].T
                 + U_t + W_t.T - U_t @ W_t.T)
        sum_rem += -2 * T[mu] @ Phi_t @ T[nu]

    if sum_rem >= 0:
        pos_count += 1
    else:
        neg_count += 1
        min_rem = min(min_rem, sum_rem)

print(f"  5000 trials: positive={pos_count}, negative={neg_count}")
if neg_count > 0:
    print(f"  min remainder: {min_rem:.4f}")
    print(f"  Remainder CAN be negative → VCBL(-I) alone doesn't prove sum_S >= 0")
else:
    print(f"  REMAINDER IS ALWAYS NON-NEGATIVE → sum_S >= sum_VCBL(-I) >= 0 → PROOF!")

# ============================================================
# FULL SUM CHECK: sum_S >= 0 verified
# ============================================================
print("\n" + "=" * 60)
print("FULL sum_S >= 0: 10000 random configs")
print("=" * 60)

min_sum_S = float('inf')
for trial in range(10000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()
    val = compute_sum_S(R, D, T)
    min_sum_S = min(min_sum_S, val)

print(f"  min sum_S over 10000 random: {min_sum_S:.6f}")

# ============================================================
# STAGE 4: RANK-1 T REDUCTION
# ============================================================
print("\n" + "=" * 60)
print("RANK-1 T: T_mu = s_mu * n, sum s_mu = 0")
print("=" * 60)

# For T_mu = s_mu * n with sum s = 0:
# sum_S = sum_{mu<nu} [2 s_mu^2 f(U, n) + 2 s_nu^2 f(W, n) - 2 s_mu s_nu n^T(2I-D^T-RDR)n]
# = n^T [sum_{mu<nu} 2 s_mu^2 (I-U)_sym + 2 s_nu^2 (I-W)_sym - 2 s_mu s_nu (2I-D^T-RDR)_sym] n
# This is a 3x3 matrix in n → PSD iff eigenvalues >= 0.

# For rank-1 T, sum_S >= 0 iff the 3x3 matrix is PSD for all s in V_s = {sum s=0} and all R, D.

min_eig_rank1 = float('inf')
for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    # Random s with sum = 0
    s = np.random.randn(3)
    s = np.append(s, -np.sum(s))

    # Build 3x3 matrix
    M3 = np.zeros((3,3))
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T

        M3 += s[mu]**2 * (2*I3 - U - U.T)
        M3 += s[nu]**2 * (2*I3 - W - W.T)
        C_sym = (D[(mu,nu)].T + D[(mu,nu)] + RDR + RDR.T) / 2 - 2*I3
        M3 += 2 * s[mu] * s[nu] * C_sym  # note: cross enters with + sign

    eigs = np.linalg.eigvalsh(M3)
    min_eig_rank1 = min(min_eig_rank1, eigs[0])

print(f"  min eigenvalue of 3x3 (rank-1 T): {min_eig_rank1:.8f}")

# ============================================================
# KEY STRUCTURAL ANALYSIS: At the minimizer (D=I), what's the structure?
# ============================================================
print("\n" + "=" * 60)
print("MINIMIZER STRUCTURE: eigenspace analysis at D=I")
print("=" * 60)

R_test = {mu: random_SO3() for mu in range(4)}
D_I = {p: I3 for p in PAIRS}
M12_I = build_M12(R_test, D_I)
M9_I = P.T @ M12_I @ P
M9_I = (M9_I + M9_I.T) / 2
eigs_I, vecs_I = np.linalg.eigh(M9_I)
print(f"  Eigenvalues at D=I: {eigs_I}")
print(f"  Number of zero eigenvalues: {np.sum(np.abs(eigs_I) < 1e-10)}")

# Get the null eigenvector(s)
null_idx = np.where(np.abs(eigs_I) < 1e-10)[0]
if len(null_idx) > 0:
    for idx in null_idx:
        v = vecs_I[:, idx]
        # Reconstruct T from v: t = (T_0, T_1, T_2), T_3 = -T_0-T_1-T_2
        T_null = {}
        for mu in range(3):
            T_null[mu] = v[3*mu:3*mu+3]
        T_null[3] = -T_null[0] - T_null[1] - T_null[2]

        # Check: is T_mu on axis of R_mu?
        for mu in range(4):
            if np.linalg.norm(T_null[mu]) > 1e-10:
                cosang = abs(np.dot(T_null[mu], np.real(np.linalg.eig(R_test[mu])[1][:,
                    np.argmin(np.abs(np.linalg.eig(R_test[mu])[0] - 1))]))) / np.linalg.norm(T_null[mu])
                print(f"    T_{mu} alignment with axis(R_{mu}): cos = {cosang:.6f}")
            else:
                print(f"    T_{mu} = 0")
