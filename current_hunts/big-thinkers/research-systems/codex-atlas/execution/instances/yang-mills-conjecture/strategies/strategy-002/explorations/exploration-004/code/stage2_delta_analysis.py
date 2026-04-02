"""
Stage 2: Analyze Delta_S and attempt full proof of sum_S >= 0.

We have: sum_S = baseline + delta_total
baseline = 6*sum f(R,T) + |sum R^T T|^2 >= 0
delta_total = sum_{mu<nu} 2*(R_mu^T T_mu - T_nu)^T (I-D) (T_mu - R_nu^T T_nu)
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

def random_T_in_V():
    T = {mu: np.random.randn(3) for mu in range(3)}
    T[3] = -T[0] - T[1] - T[2]
    return T

def compute_sum_S(R, D, T):
    total = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        total += 2*f(U, T[mu]) + 2*f(W, T[nu])
        total -= 2*T[mu] @ (2*I3 - D[(mu,nu)].T - RDR) @ T[nu]
    return total

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

# ============================================================
# TEST 1: Budget vs Cross ratio
# ============================================================
print("=" * 60)
print("BUDGET vs CROSS: can cross exceed budget?")
print("=" * 60)

max_ratio = 0
for trial in range(10000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    budget = 0.0
    cross_val = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        budget += 2*f(U, T[mu]) + 2*f(W, T[nu])
        C = 2*I3 - D[(mu,nu)].T - RDR
        cross_val += 2*T[mu] @ C @ T[nu]

    if budget > 1e-10:
        ratio = cross_val / budget
        max_ratio = max(max_ratio, ratio)

print(f"  max (cross / budget): {max_ratio:.6f}")

# ============================================================
# TEST 2: Convexity in D (Hessian check)
# ============================================================
print("\n" + "=" * 60)
print("CONVEXITY in D: Hessian at D=I and random D")
print("=" * 60)

def eval_hessian_along_geodesic(R, T, D_base, A_vecs, eps=1e-5):
    """Second derivative of sum_S along geodesic in D-space."""
    vals = []
    for t in [-2*eps, -eps, 0, eps, 2*eps]:
        D_t = {}
        for p in PAIRS:
            theta = np.linalg.norm(A_vecs[p])
            if theta > 1e-15:
                k = A_vecs[p] / theta
                K = skew(k)
                D_t[p] = D_base[p] @ (I3 + np.sin(t*theta)*K + (1-np.cos(t*theta))*(K@K))
            else:
                D_t[p] = D_base[p].copy()
        vals.append(compute_sum_S(R, D_t, T))
    return (-vals[0] + 16*vals[1] - 30*vals[2] + 16*vals[3] - vals[4]) / (12*eps**2)

# Hessian at D=I
R = {mu: random_SO3() for mu in range(4)}
T = random_T_in_V()
D_I = {p: I3.copy() for p in PAIRS}

neg_count_DI = 0
min_h_DI = float('inf')
for _ in range(200):
    A = {p: np.random.randn(3) for p in PAIRS}
    # Normalize so sum of squared norms = 1
    total_norm = np.sqrt(sum(np.dot(A[p], A[p]) for p in PAIRS))
    if total_norm > 1e-10:
        A = {p: A[p] / total_norm for p in PAIRS}
    h = eval_hessian_along_geodesic(R, T, D_I, A)
    min_h_DI = min(min_h_DI, h)
    if h < -1e-4:
        neg_count_DI += 1

print(f"  At D=I (fixed R, T):")
print(f"  min Hessian: {min_h_DI:.6f}, negative count: {neg_count_DI}/200")

# Hessian at random D
neg_at_random = 0
min_h_rand = float('inf')
for trial in range(100):
    R = {mu: random_SO3() for mu in range(4)}
    T = random_T_in_V()
    D_base = {p: random_SO3() for p in PAIRS}

    A = {p: np.random.randn(3) for p in PAIRS}
    total_norm = np.sqrt(sum(np.dot(A[p], A[p]) for p in PAIRS))
    if total_norm > 1e-10:
        A = {p: A[p] / total_norm for p in PAIRS}
    h = eval_hessian_along_geodesic(R, T, D_base, A)
    min_h_rand = min(min_h_rand, h)
    if h < -1e-4:
        neg_at_random += 1

print(f"\n  At random D:")
print(f"  min Hessian: {min_h_rand:.6f}, negative count: {neg_at_random}/100")

# ============================================================
# TEST 3: Adversarial minimum eigenvalue search
# ============================================================
print("\n" + "=" * 60)
print("ADVERSARIAL: min eigenvalue of 9x9 sum_S matrix")
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

from scipy.optimize import minimize as sp_minimize

best_val = float('inf')
best_params = None
for trial in range(500):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    if v < best_val:
        best_val = v
        best_params = p0.copy()

print(f"  After 500 random starts: best min_eig = {best_val:.6f}")

# Refine
res = sp_minimize(min_eig_M9, best_params, method='Nelder-Mead',
                  options={'maxiter': 500000, 'xatol': 1e-14, 'fatol': 1e-15})
print(f"  After Nelder-Mead: min_eig = {res.fun:.10e}")

# ============================================================
# TEST 4: Structure of the Delta_S bilinear form
# ============================================================
print("\n" + "=" * 60)
print("STRUCTURE: Delta_S bilinear form analysis")
print("=" * 60)

# Delta_S_{mu,nu} = 2 u^T E v where u = R_mu^T T_mu - T_nu, v = T_mu - R_nu^T T_nu, E = I-D
# Note: u^T E v = u^T (E_sym) v + u^T (E_skew) v
# E_sym = (I - (D+D^T)/2), E_skew = (D^T - D)/2

# For D = exp(theta * K) with K skew:
# E = I - D ≈ -theta*K + theta^2/2 * K^2 + ...
# E_sym ≈ theta^2/2 * (K^2 + (K^2)^T)/2 ... hmm K^2 is already symmetric for skew K
# Actually for K skew: K^T = -K, K^2 is symmetric (K^2)^T = (K^T)^2 = K^2.
# E = I - exp(theta K) ≈ -theta K + theta^2/2 K^2 + ...
# E_sym = (E + E^T)/2 ≈ theta^2/2 K^2 + ... (the -theta K cancels)
# Actually: (I-D + I-D^T)/2 = I - (D+D^T)/2

# For D in SO(3): D+D^T = 2 cos(theta)I + 2(1-cos(theta)) nn^T - 0 (the antisymmetric part cancels)
# Wait, D = I cos(theta) + (1-cos(theta)) nn^T + sin(theta) K_n
# D+D^T = 2 cos(theta)I + 2(1-cos(theta)) nn^T
# So I - (D+D^T)/2 = (1-cos(theta))(I - nn^T) which is PSD!

# So E_sym is PSD! The symmetric part of I-D is always PSD for D in SO(3).
# E_skew = (D^T - D)/2 = -sin(theta) K_n

# Key: u^T E v = u^T E_sym v + u^T E_skew v
# The first part can be bounded since E_sym is PSD.
# The second part involves the skew part.

# For the proof, consider: u^T E_sym v <= ||E_sym^{1/2} u|| ||E_sym^{1/2} v|| (C-S)
# and |u^T E_skew v| <= ||E_skew|| ||u|| ||v||

# Let's check: what fraction of Delta_S comes from E_sym vs E_skew?
sym_frac = []
for trial in range(1000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    delta_sym = 0.0
    delta_skew = 0.0
    for mu, nu in PAIRS:
        E = I3 - D[(mu,nu)]
        E_sym = (E + E.T) / 2
        E_skew = (E - E.T) / 2
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        delta_sym += 2 * u @ E_sym @ v
        delta_skew += 2 * u @ E_skew @ v

    if abs(delta_sym + delta_skew) > 1e-10:
        sym_frac.append(delta_sym / (delta_sym + delta_skew))

print(f"  Symmetric fraction of Delta_S: mean={np.mean(sym_frac):.4f}, "
      f"std={np.std(sym_frac):.4f}")

# ============================================================
# TEST 5: Alternative decomposition — rewrite sum_S entirely
# ============================================================
print("\n" + "=" * 60)
print("ALTERNATIVE: Rewrite sum_S using (I-D) = E_sym + E_skew")
print("=" * 60)

# sum_S = baseline + sum_{mu<nu} 2 u^T E v
# = baseline + sum 2 u^T E_sym v + sum 2 u^T E_skew v
#
# Since E_sym = (1-cos theta)(I - nn^T) is PSD, the symmetric part is well-behaved.
# The skew part: E_skew = -sin(theta) K_n, and u^T K_n v = n · (u × v).
#
# So sum_skew = sum_{mu<nu} 2 * (-sin theta_{mu,nu}) * n_{mu,nu} · (u_{mu,nu} × v_{mu,nu})
# This involves cross products! It can be positive or negative.

# Let's check: does the baseline always dominate the skew part?
max_skew_ratio = 0
for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    baseline = 6*sum(f(R[mu], T[mu]) for mu in range(4))
    sum_vec = sum(R[mu].T @ T[mu] for mu in range(4))
    baseline += np.dot(sum_vec, sum_vec)

    delta_total = 0.0
    for mu, nu in PAIRS:
        E = I3 - D[(mu,nu)]
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        delta_total += 2 * u @ E @ v

    if baseline > 1e-10 and delta_total < 0:
        ratio = -delta_total / baseline
        max_skew_ratio = max(max_skew_ratio, ratio)

print(f"  max |negative delta| / baseline: {max_skew_ratio:.6f}")
print(f"  If < 1, then sum_S >= 0 is guaranteed by baseline dominance")

# ============================================================
# TEST 6: Can we prove sum_S >= 0 via a different decomposition?
# ============================================================
print("\n" + "=" * 60)
print("NEW DECOMPOSITION: Try writing sum_S as sum of |...|^2")
print("=" * 60)

# From the per-plaquette identity:
# 4|T_mu - T_nu|^2 - |B|^2 = S_{mu,nu}
# where B = (I + U)T_mu - R_mu(I + W)T_nu
#
# So S_{mu,nu} = 4|T_mu - T_nu|^2 - |(I+U)T_mu - R_mu(I+W)T_nu|^2
#
# Let A_mn = (I+U)/2, C_mn = R_mu(I+W)/2. Then:
# S_{mu,nu} = 4|T_mu - T_nu|^2 - 4|A T_mu - C T_nu|^2
# = 4[(T_mu - T_nu)^T(T_mu - T_nu) - (A T_mu - C T_nu)^T(A T_mu - C T_nu)]
# = 4[|T_mu|^2 - 2T_mu·T_nu + |T_nu|^2 - |A T_mu|^2 + 2(AT_mu)·(CT_nu) - |C T_nu|^2]
# = 4[|T_mu|^2(1 - |A|^2_{T_mu}) + |T_nu|^2(1 - |C|^2_{T_nu}) - 2T_mu·T_nu + 2(AT_mu)·(CT_nu)]
# where |A|^2_{T_mu} means T_mu^T A^T A T_mu / |T_mu|^2.

# The matrices A, C involve (I+rotation)/2. For rotation by angle theta:
# I + R = 2cos(theta/2)^2 I + 2(1-cos(theta)) nn^T + sin(theta) K_n ... hmm complex.
# Let me just check: is |A T_mu|^2 <= |T_mu|^2?
# A = (I+U)/2 where U in SO(3). Singular values of (I+U)/2?
# For U with eigenvalues e^{i*alpha}, e^{-i*alpha}, 1:
# (I+U)/2 has eigenvalues (1+e^{i*alpha})/2 = cos(alpha/2) e^{i*alpha/2}, etc.
# |singular values| = |cos(alpha/2)| and 1. So max singular value = 1, min = |cos(alpha/2)|.
# So ||(I+U)/2|| <= 1, meaning |A T_mu|^2 <= |T_mu|^2. Good.

# But more importantly, can we write sum_S = sum |something|^2?

# From 4|T_mu-T_nu|^2 - |B|^2, using the polarization:
# |a|^2 - |b|^2 = |a+b|/2 * |a-b|/2 ... no, that's for scalars.
# In vectors: |a|^2 - |b|^2 where a = 2(T_mu - T_nu), b = (I+U)T_mu - R_mu(I+W)T_nu

# Actually |a|^2 - |b|^2 = (a+b)·(a-b) for vectors too (just inner product).
# a - b = 2(T_mu - T_nu) - (I+U)T_mu + R_mu(I+W)T_nu
#       = (2I - I - U)T_mu + (-2I + R_mu + R_mu W)T_nu
#       = (I - U)T_mu + (R_mu + R_mu W - 2I)T_nu
#       = (I - U)T_mu + (R_mu(I + W) - 2I)T_nu

# a + b = 2(T_mu - T_nu) + (I+U)T_mu - R_mu(I+W)T_nu
#       = (3I + U - ... wait, wrong
#       = (2I + I + U)T_mu + (-2I - R_mu(I+W))T_nu
#       = (3I + U)T_mu - (2I + R_mu + R_mu W)T_nu

# This doesn't factor nicely. Let me try something else entirely.

# ============================================================
# CRITICAL INSIGHT TEST: Does sum_S factor as a sum of VCBL terms?
# ============================================================
print("\n" + "=" * 60)
print("VCBL DECOMPOSITION: sum_S as global VCBL")
print("=" * 60)

# At R=I: sum_S = 2*sum VCBL(D, D, -I, T_mu, T_nu) [KNOWN]
# For general R: try sum_S = 2*sum VCBL(U, W, M, T_mu, T_nu)
# where M = -I (same as R=I case).
#
# 2*VCBL(U, W, -I, p, q) = 2f(U,p) + 2f(W,q) - 2 p^T(I-U)(I-W^T)q
# S_{mu,nu} = 2f(U,p) + 2f(W,q) - 2p^T(2I - D^T - RDR)q
#
# Difference: S - 2*VCBL(-I) = -2p^T[(2I-D^T-RDR) - (I-U)(I-W^T)]q
# = -2p^T[2I-D^T-RDR - I + U + W^T - UW^T]q
# (I-U)(I-W^T) = I - U - W^T + UW^T
# 2I-D^T-RDR = 2I - U^T R_mu - U R_nu^T

# So diff = (2I - U^T R_mu - U R_nu^T) - (I - U - W^T + UW^T)
# = I - U^T R_mu - U R_nu^T + U + W^T - UW^T
# = I + U - U^T R_mu - U R_nu^T + W^T - UW^T
# Now W = D R_nu^T so W^T = R_nu D^T. And U = R_mu D.
# UW^T = R_mu D R_nu D^T.
# U R_nu^T = R_mu D R_nu^T = RDR.
# U^T R_mu = D^T R_mu^T R_mu = D^T.
# So diff = I + R_mu D - D^T - RDR + R_nu D^T - R_mu D R_nu D^T

# Let me verify numerically:
for trial in range(5):
    R_mu, R_nu = random_SO3(), random_SO3()
    D_mn = random_SO3()
    U = R_mu @ D_mn; W = D_mn @ R_nu.T
    p, q = np.random.randn(3), np.random.randn(3)

    S_val = 2*f(U, p) + 2*f(W, q) - 2*p @ (2*I3 - D_mn.T - R_mu @ D_mn @ R_nu.T) @ q
    vcbl_val = 2*f(U, p) + 2*f(W, q) - 2*p @ (I3 - U) @ (I3 - W.T) @ q
    remainder = S_val - vcbl_val

    diff_mat = (2*I3 - D_mn.T - R_mu @ D_mn @ R_nu.T) - (I3 - U - W.T + U @ W.T)
    remainder_check = -2 * p @ diff_mat @ q

    print(f"  Trial {trial}: S={S_val:.4f}, 2*VCBL(-I)={vcbl_val:.4f}, "
          f"diff={remainder:.4f}, check={remainder_check:.6f}, match={abs(remainder - remainder_check) < 1e-10}")

# So S = 2*VCBL(U,W,-I,...) + remainder
# where remainder = -2 p^T Phi q, Phi = diff_mat

print("\n  Analyzing remainder matrix Phi...")
for trial in range(10):
    R_mu, R_nu = random_SO3(), random_SO3()
    D_mn = random_SO3()
    U = R_mu @ D_mn; W = D_mn @ R_nu.T

    Phi = (2*I3 - D_mn.T - R_mu @ D_mn @ R_nu.T) - (I3 - U - W.T + U @ W.T)
    eigs_sym = np.linalg.eigvalsh((Phi + Phi.T)/2)
    print(f"  Phi sym eigs: [{eigs_sym[0]:.4f}, {eigs_sym[1]:.4f}, {eigs_sym[2]:.4f}]")

# ============================================================
# DIRECT APPROACH: Build 12x12 matrix as sum of outer products
# ============================================================
print("\n" + "=" * 60)
print("DIRECT: Can we write M12 = sum of PSD terms?")
print("=" * 60)

# sum_S = sum_{mu<nu} [||a||^2 + ||b||^2 - 2 T_mu^T C T_nu]
# where a = (I-U^T)T_mu, b = (I-W^T)T_nu
# ||a||^2 + ||b||^2 = diagonal terms
# -2 T^T C T = cross terms
#
# VCBL(-I) gives: ||a||^2 + ||b||^2 - 2 a·b = ||a - b||^2
# so 2*VCBL(-I) per pair = ||(I-U^T)T_mu - (I-W^T)T_nu||^2

# Let me verify:
R_mu, R_nu = random_SO3(), random_SO3()
D_mn = random_SO3()
U = R_mu @ D_mn; W = D_mn @ R_nu.T
T_mu, T_nu = np.random.randn(3), np.random.randn(3)

a = (I3 - U.T) @ T_mu
b = (I3 - W.T) @ T_nu
vcbl_neg1 = np.dot(a-b, a-b)  # ||a-b||^2
vcbl_formula = 2*f(U, T_mu) + 2*f(W, T_nu) - 2*a @ b
print(f"  ||a-b||^2 = {vcbl_neg1:.6f}")
print(f"  2f(U)+2f(W)-2a·b = {vcbl_formula:.6f}")
print(f"  -2a·b = {-2*a@b:.6f}")
print(f"  -2 T^T (I-U)(I-W^T) T = {-2*T_mu @ (I3-U) @ (I3-W.T) @ T_nu:.6f}")
# Check: a·b = [(I-U^T)T_mu]·[(I-W^T)T_nu] = T_mu^T(I-U)(I-W^T)T_nu
print(f"  Match: {abs(-2*a@b - (-2*T_mu @ (I3-U) @ (I3-W.T) @ T_nu)):.2e}")

# So VCBL(-I) per pair = ||a-b||^2 = ||(I-U^T)T_mu - (I-W^T)T_nu||^2
# And S_{mu,nu} = ||a-b||^2 + remainder

# Total: sum_S = sum ||a_{mu,nu} - b_{mu,nu}||^2 + sum remainder
# If sum remainder >= 0, done.

# Let me check the sign of sum remainder:
print("\n  Sum remainder = sum_S - sum ||a-b||^2:")
for trial in range(10):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    sum_S_val = compute_sum_S(R, D, T)
    sum_norm_sq = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        a = (I3 - U.T) @ T[mu]
        b = (I3 - W.T) @ T[nu]
        sum_norm_sq += np.dot(a-b, a-b)

    remainder = sum_S_val - sum_norm_sq
    print(f"  sum_S={sum_S_val:8.3f}, sum||a-b||^2={sum_norm_sq:8.3f}, "
          f"remainder={remainder:8.3f}")

# If remainder can be negative, we need a different decomposition.

# ============================================================
# KEY ATTEMPT: Direct algebraic proof via Cauchy-Schwarz
# ============================================================
print("\n" + "=" * 60)
print("SUM_S AS SCHUR COMPLEMENT or BLOCK MATRIX")
print("=" * 60)

# Write T = (T_0, T_1, T_2, T_3) ∈ R^12 with constraint T_3 = -T_0-T_1-T_2.
# sum_S = T^T M T where M is 12x12.
# Claim: M|_V >= 0, i.e., the projected M9 = P^T M P is PSD.

# For any R, D, compute the eigenvalues of M9 and try to find an algebraic
# proof that they're non-negative.

# Hint from the structure: at D=I, M9 is manifestly PSD (from Stage 1).
# At general D, can we write M9(D) = M9(I) + Delta where Delta has
# controlled eigenvalues?

# Check: how negative can the smallest eigenvalue of Delta_M9 get?
neg_delta_eigs = []
for trial in range(1000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    D_I_dict = {p: I3 for p in PAIRS}

    M12_D = build_M12(R, D)
    M12_I = build_M12(R, D_I_dict)
    Delta = M12_D - M12_I
    Delta9 = P.T @ Delta @ P
    Delta9 = (Delta9 + Delta9.T) / 2

    M9_I = P.T @ M12_I @ P
    M9_I = (M9_I + M9_I.T) / 2

    eig_delta = np.linalg.eigvalsh(Delta9)
    eig_base = np.linalg.eigvalsh(M9_I)

    neg_delta_eigs.append(eig_delta[0])

neg_delta_eigs = np.array(neg_delta_eigs)
print(f"  min eig of Delta_M9: {np.min(neg_delta_eigs):.4f}")
print(f"  mean: {np.mean(neg_delta_eigs):.4f}")
print(f"  Delta CAN be negative (as expected)")
print(f"  But baseline M9(I) compensates")
