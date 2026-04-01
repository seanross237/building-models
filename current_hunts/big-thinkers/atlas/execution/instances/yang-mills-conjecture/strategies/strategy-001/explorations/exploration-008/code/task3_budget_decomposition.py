"""
Task 3: Per-plaquette budget analysis and proof decomposition.

KEY IDENTITY: For T with Sum_mu T_mu = 0:
  16||T||^2 = 4 * Sum_{mu<nu} |T_mu - T_nu|^2

So the "gap" 16||T||^2 - F_x(T) = Sum_{mu<nu} [4|T_mu - T_nu|^2 - |B_{mu,nu}|^2]

The budget per plaquette is 4|T_mu - T_nu|^2.
The cost per plaquette is |B_{mu,nu}|^2.

At Q=I: cost = budget exactly (since B = 2(T_mu - T_nu)).

Question: Does the per-plaquette budget hold for each plaquette separately?
Or do we need to group plaquettes (as in E006)?
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

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def compute_plaquette_B(R, D, T, mu, nu):
    """Compute B for plaquette (mu,nu): (I + R_mu D) T_mu - R_mu(I + D R_nu^T) T_nu"""
    S = np.eye(3) + R[mu] @ D[(mu,nu)]
    Tmat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
    return S @ T[mu] - Tmat @ T[nu]

def random_constrained_T():
    """Random T with Sum_mu T_mu = 0."""
    T = np.random.randn(4, 3)
    T[3] = -(T[0] + T[1] + T[2])
    return T

# ============================================================
# Part A: Verify the budget identity 16||T||^2 = 4 Sum |T_mu - T_nu|^2
# ============================================================
print("=" * 70)
print("PART A: Verify budget identity")
print("=" * 70)

max_err = 0
for _ in range(10000):
    T = random_constrained_T()
    norm2 = np.sum(T**2)
    budget_sum = sum(np.sum((T[mu] - T[nu])**2) for mu, nu in PLANES)
    err = abs(16 * norm2 - 4 * budget_sum)
    max_err = max(max_err, err)

print(f"  Max |16||T||^2 - 4*Sum|T_mu-T_nu|^2|: {max_err:.2e}")
print(f"  Identity VERIFIED: {max_err < 1e-10}")

# ============================================================
# Part B: Per-plaquette budget test — does |B|^2 <= 4|T_mu - T_nu|^2?
# ============================================================
print("\n" + "=" * 70)
print("PART B: Per-plaquette budget test")
print("=" * 70)

N_tests = 5000
per_plaq_violations = 0
max_per_plaq_ratio = 0
violation_plaquettes = {}

for trial in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    for mu, nu in PLANES:
        B = compute_plaquette_B(R, D, T, mu, nu)
        cost = np.dot(B, B)
        budget = 4 * np.sum((T[mu] - T[nu])**2)

        if budget > 1e-12:
            ratio = cost / budget
            max_per_plaq_ratio = max(max_per_plaq_ratio, ratio)
            if ratio > 1 + 1e-10:
                per_plaq_violations += 1
                key = (mu, nu)
                violation_plaquettes[key] = violation_plaquettes.get(key, 0) + 1

print(f"  Max |B|^2 / (4|T_mu-T_nu|^2): {max_per_plaq_ratio:.6f}")
print(f"  Per-plaquette violations: {per_plaq_violations}")
if per_plaq_violations > 0:
    print(f"  Violations by plaquette: {violation_plaquettes}")

# ============================================================
# Part C: If per-plaquette fails, try PAIRS of plaquettes
# ============================================================
print("\n" + "=" * 70)
print("PART C: E006-style analysis for general T")
print("=" * 70)

# In E006, the proof used f(R, n) = n^T(I-R)n >= 0
# and the key was the decomposition of 16||T||^2 - F_x into sums of f-terms.
#
# For general T, define:
#   f(R, p) = p^T(I-R)p for any vector p (not just unit n)
#   Still >= 0 since (I-R)_sym is PSD for R in SO(3)
#
# Let's see if 16||T||^2 - F_x can be written as a sum of f-terms.

# First, compute 16||T||^2 - F_x(T) as a function of (R, D, T)
# and try to match it against sums of f(rotation, vector)-type terms.

def f_vec(R, p):
    """f(R, p) = p^T (I - R) p >= 0 for R in SO(3), p in R^3."""
    return np.dot(p, p) - np.dot(p, R @ p)

# Test: is f_vec always >= 0?
min_f = float('inf')
for _ in range(10000):
    R = random_so3()
    p = np.random.randn(3)
    min_f = min(min_f, f_vec(R, p))
print(f"  Min f(R, p) over 10K tests: {min_f:.6f} (should be >= 0)")

# Now let's expand |B|^2 in terms of f-functions.
# B = (I + U)T_mu - R_mu(I+W)T_nu where U = R_mu D, W = D R_nu^T
#
# |B|^2 = |T_mu + U T_mu - R_mu T_nu - R_mu W T_nu|^2
#
# Let me define:
#   p = T_mu - T_nu (the "difference" direction)
#   Then T_mu = p + T_nu (roughly)
# But this doesn't have a clean structure.
#
# Instead, let's directly compute 4|T_mu - T_nu|^2 - |B|^2 and see its structure.

print("\nExpanding 4|T_mu - T_nu|^2 - |B|^2 for a single plaquette:")

# At Q = slightly perturbed identity
R = [so3_exp(0.1 * np.random.randn(3)) for _ in range(d)]
D = {p: so3_exp(0.1 * np.random.randn(3)) for p in PLANES}
T = random_constrained_T()

mu, nu = 0, 1
B = compute_plaquette_B(R, D, T, mu, nu)
cost = np.dot(B, B)
budget = 4 * np.sum((T[mu] - T[nu])**2)
print(f"  4|T_mu-T_nu|^2 = {budget:.4f}, |B|^2 = {cost:.4f}, gap = {budget-cost:.4f}")

# ============================================================
# Part D: Algebraic expansion — the GENERAL combined bound
# ============================================================
print("\n" + "=" * 70)
print("PART D: Generalized combined bound (E006 Step 4 for general T)")
print("=" * 70)

# In E006 for uniform color (T_mu = s_mu n), the key identity was:
#   f(A,n) + f(B,n) + f(AD,n) + f(DB^T,n) - f(D,n) - f(ADB^T,n)
#   = n^T(I-A)D(I-B^T)n + f(A,n) + f(B,n) >= 0
#
# For general T (different vectors per direction), the analogous identity involves
# CROSS-TERMS between T_mu and T_nu.
#
# Let's compute 4|p|^2 - |B|^2 where p = T_mu - T_nu and B = S T_mu - Tmat T_nu
# in terms of f-functions of T_mu and T_nu separately.

# Direct algebraic expansion:
# B = (I+U)T_mu - R_mu(I+W)T_nu
# |B|^2 = |T_mu + UT_mu - R_mu T_nu - R_mu W T_nu|^2
#
# 4|T_mu - T_nu|^2 = 4|T_mu|^2 + 4|T_nu|^2 - 8 T_mu . T_nu
#
# Let's compute the gap G = 4|T_mu-T_nu|^2 - |B|^2

def compute_gap_single_plaq(R, D, T, mu, nu):
    """Compute 4|T_mu-T_nu|^2 - |B_{mu,nu}|^2."""
    B = compute_plaquette_B(R, D, T, mu, nu)
    return 4 * np.sum((T[mu] - T[nu])**2) - np.dot(B, B)

# What about the TOTAL gap: Sum_{mu<nu} gap_{mu,nu} = 16||T||^2 - F_x?
# This should always be >= 0 (if the bound holds).

print("\nTotal gap analysis:")
N_tests = 5000
min_total_gap = float('inf')
gap_by_plaq_stats = {p: [] for p in PLANES}

for trial in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    gaps = {}
    for p in PLANES:
        gaps[p] = compute_gap_single_plaq(R, D, T, p[0], p[1])
        gap_by_plaq_stats[p].append(gaps[p])

    total_gap = sum(gaps.values())
    min_total_gap = min(min_total_gap, total_gap)

print(f"  Min total gap (16||T||^2 - F_x): {min_total_gap:.6f} (need >= 0)")

# Print per-plaquette gap statistics
print("\n  Per-plaquette gap statistics:")
for p in PLANES:
    vals = np.array(gap_by_plaq_stats[p])
    print(f"    ({p[0]},{p[1]}): min = {vals.min():.4f}, max = {vals.max():.4f}, "
          f"mean = {vals.mean():.4f}, frac < 0 = {np.mean(vals < 0):.4f}")

# ============================================================
# Part E: Classify plaquettes by active/inactive for general T
# ============================================================
print("\n" + "=" * 70)
print("PART E: Active/inactive classification for general T")
print("=" * 70)

# In E006 with s_mu = (-1)^mu: active plaquettes have (mu+nu) odd,
# inactive have (mu+nu) even. Active always have gap >= 0.
#
# For general T, does this classification still work?
# The "active" classification came from the sign structure a*b being positive/negative.
# For general T, there's no sign structure — the classification might depend on T.
#
# Let's check: at the adversarial maximum, which plaquettes have negative gap?

print("\nAdversarial analysis of per-plaquette gaps:")

for trial in range(10):
    # Adversarial: gradient ascent on F_x / ||T||^2
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    step_size = 0.02
    best_ratio = 0

    for iteration in range(200):
        # Find worst T for current (R, D)
        # This is the max eigenvalue direction of M_12 constrained
        M12 = np.zeros((12, 12))
        for mu, nu in PLANES:
            S = np.eye(3) + R[mu] @ D[(mu,nu)]
            Tm = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
            M12[3*mu:3*(mu+1), 3*mu:3*(mu+1)] += S.T @ S
            M12[3*nu:3*(nu+1), 3*nu:3*(nu+1)] += Tm.T @ Tm
            M12[3*mu:3*(mu+1), 3*nu:3*(nu+1)] -= S.T @ Tm
            M12[3*nu:3*(nu+1), 3*mu:3*(mu+1)] -= Tm.T @ S

        # Constrained eigenproblem
        V = np.zeros((12, 9))
        idx = 0
        for i in range(3):
            for a in range(3):
                v = np.zeros(12)
                v[3*i + a] = 1.0
                v[9 + a] = -1.0
                V[:, idx] = v
                idx += 1
        Q_orth, _ = np.linalg.qr(V)
        V_orth = Q_orth[:, :9]
        M_r = V_orth.T @ M12 @ V_orth
        eigs, vecs = np.linalg.eigh(M_r)

        top_12d = V_orth @ vecs[:, -1]
        T_star = top_12d.reshape(4, 3)
        T_norm2 = np.sum(T_star**2)
        ratio = eigs[-1] / T_norm2 * np.sum(T_star**2)  # this is just eigs[-1] since V_orth is orthonormal

        # Gradient ascent on R, D
        eps = 1e-5
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = R.copy(); R_p[mu] = so3_exp(omega) @ R[mu]
                M12_p = np.zeros((12, 12))
                for m, n in PLANES:
                    S = np.eye(3) + R_p[m] @ D[(m,n)]
                    Tm = R_p[m] + R_p[m] @ D[(m,n)] @ R_p[n].T
                    M12_p[3*m:3*(m+1), 3*m:3*(m+1)] += S.T @ S
                    M12_p[3*n:3*(n+1), 3*n:3*(n+1)] += Tm.T @ Tm
                    M12_p[3*m:3*(m+1), 3*n:3*(n+1)] -= S.T @ Tm
                    M12_p[3*n:3*(n+1), 3*m:3*(m+1)] -= Tm.T @ S
                M_r_p = V_orth.T @ M12_p @ V_orth
                eig_p = np.linalg.eigvalsh(M_r_p)[-1]
                g = (eig_p - eigs[-1]) / eps
                R[mu] = so3_exp(step_size * g * np.eye(3)[k]) @ R[mu]

        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D); D_p[p] = so3_exp(omega) @ D[p]
                M12_p = np.zeros((12, 12))
                for m, n in PLANES:
                    S = np.eye(3) + R[m] @ D_p[(m,n)]
                    Tm = R[m] + R[m] @ D_p[(m,n)] @ R[n].T
                    M12_p[3*m:3*(m+1), 3*m:3*(m+1)] += S.T @ S
                    M12_p[3*n:3*(n+1), 3*n:3*(n+1)] += Tm.T @ Tm
                    M12_p[3*m:3*(m+1), 3*n:3*(n+1)] -= S.T @ Tm
                    M12_p[3*n:3*(n+1), 3*m:3*(m+1)] -= Tm.T @ S
                M_r_p = V_orth.T @ M12_p @ V_orth
                eig_p = np.linalg.eigvalsh(M_r_p)[-1]
                g = (eig_p - eigs[-1]) / eps
                D[p] = so3_exp(step_size * g * np.eye(3)[k]) @ D[p]

        if iteration > 0 and iteration % 50 == 0:
            step_size *= 0.7

    # At convergence, analyze per-plaquette gaps with worst T
    gaps = {}
    for p in PLANES:
        gaps[p] = compute_gap_single_plaq(R, D, T_star, p[0], p[1])

    total = sum(gaps.values())
    neg_plaqs = [p for p in PLANES if gaps[p] < -1e-6]

    # Check T_star rank
    sv = np.linalg.svd(T_star, compute_uv=False)
    rank1_frac = sv[0]**2 / np.sum(sv**2)

    print(f"\n  Trial {trial}: max_eig = {eigs[-1]:.6f}, total_gap = {total:.6f}")
    print(f"    T rank-1 fraction = {rank1_frac:.4f}")
    print(f"    Per-plaquette gaps: ", end="")
    for p in PLANES:
        sign = "+" if gaps[p] >= 0 else "-"
        print(f"({p[0]},{p[1]}):{gaps[p]:+.3f}{sign} ", end="")
    print()
    if neg_plaqs:
        print(f"    Negative gap plaquettes: {neg_plaqs}")

# ============================================================
# Part F: Try the E006 factorization for general vectors
# ============================================================
print("\n" + "=" * 70)
print("PART F: E006 factorization identity for general vectors")
print("=" * 70)

# The E006 identity: for A, B, D in SO(3) and unit n:
#   f(A,n) + f(B,n) + f(AD,n) + f(DB^T,n) - f(D,n) - f(ADB^T,n)
#   = n^T(I-A)D(I-B^T)n + f(A,n) + f(B,n)
#
# Generalize: for DIFFERENT vectors p, q:
#   f(A,p) + f(B,q) + f(AD,p) + f(DB^T,q) - f(D,p?) - f(ADB^T,q?)
#   = ???
#
# This doesn't directly generalize because the original used the SAME n everywhere.
#
# NEW APPROACH: Work with vectors.
# For each plaquette, the "gap" is:
#   4|T_mu - T_nu|^2 - |B|^2
# where B = (I+U)T_mu - R_mu(I+W)T_nu
#
# Let p = T_mu, q = T_nu.
#
# 4|p-q|^2 - |(I+U)p - R(I+W)q|^2
# = 4(|p|^2 + |q|^2 - 2p.q) - [(2|p|^2 + p^T(U+U^T)p) + (2|q|^2 + q^T(W+W^T)q)
#   - 2p^T(I+U^T)R(I+W)q]
# where U = R_mu D, W = D R_nu^T, R = R_mu
#
# = 2|p|^2 + 2|q|^2 - 8p.q - p^T(U+U^T)p - q^T(W+W^T)q + 2p^T(I+U^T)R(I+W)q
# = 2|p|^2 - p^T(U+U^T)p + 2|q|^2 - q^T(W+W^T)q - 8p.q + 2p^T(I+U^T)R(I+W)q

# Note: 2|p|^2 - p^T(U+U^T)p = p^T(2I - U - U^T)p = 2f(U,p)
# Similarly: 2|q|^2 - q^T(W+W^T)q = 2f(W,q)
# Actually: f(U,p) = p^T(I-U)p, so 2f(U,p) = p^T(2I - U - U^T)p? No.
# 2f(U,p) = 2p^T(I-U)p = 2|p|^2 - 2p^TUp. But p^T(U+U^T)p = 2p^TUp (real part).
# Hmm, p^TUp is NOT equal to p^TU^Tp in general (since U is not symmetric).
# But p^T(U+U^T)p = p^TUp + p^TU^Tp = 2 Re(p^TUp). And f(U,p) = |p|^2 - p^TUp.
# So 2|p|^2 - p^T(U+U^T)p = 2|p|^2 - 2 Re(p^TUp) = 2 Re(f(U,p)).
# But f(U,p) = |p|^2 - p^TUp which is already real (since p^TUp = sum p_i (Up)_i is real).
# Wait, no: p^TUp is a scalar, and for a real matrix U, p^TUp = sum_{i,j} p_i U_{ij} p_j.
# For U = R_mu D (a rotation), p^TUp is real. And p^TU^Tp = p^TUp (just the transpose of a scalar = same scalar)?
# No! p^TU^Tp = (Up)^Tp = sum_i (Up)_i p_i = p^TUp. So yes, p^TUp = p^TU^Tp.
# Therefore p^T(U+U^T)p = 2p^TUp.
# So 2|p|^2 - p^T(U+U^T)p = 2(|p|^2 - p^TUp) = 2f(U,p). ✓

# So the gap for one plaquette is:
# 4|p-q|^2 - |B|^2 = 2f(U,p) + 2f(W,q) - 8p.q + 2p^T(I + U^T)R(I + W)q
#
# where (I+U^T)R(I+W) = (I + D^T R^T)R(I + DR_nu^T) = (R + D^T)(I + DR_nu^T)
# = R + RDR_nu^T + D^T + D^TDR_nu^T = R + RDR_nu^T + D^T + R_nu^T

# So the cross term is 2p^T(R + RDR_nu^T + D^T + R_nu^T)q

# Let me verify this numerically:
max_err = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    mu, nu = 0, 1
    p = T[mu]; q = T[nu]
    U = R[mu] @ D[(mu,nu)]
    W = D[(mu,nu)] @ R[nu].T

    # Direct
    B = compute_plaquette_B(R, D, T, mu, nu)
    gap_direct = 4 * np.sum((p-q)**2) - np.dot(B, B)

    # Formula
    fU = np.dot(p, p) - np.dot(p, U @ p)
    fW = np.dot(q, q) - np.dot(q, W @ q)
    cross_mat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T + D[(mu,nu)].T + R[nu].T
    cross = 2 * np.dot(p, cross_mat @ q)
    gap_formula = 2*fU + 2*fW - 8*np.dot(p, q) + cross

    err = abs(gap_direct - gap_formula)
    max_err = max(max_err, err)

print(f"  Gap formula verification error: {max_err:.2e}")

# Simplify: cross = 2p^T(R_mu + R_mu D R_nu^T + D^T + R_nu^T)q
# = 2p^T R_mu q + 2p^T R_mu D R_nu^T q + 2p^T D^T q + 2p^T R_nu^T q
#
# Note: 2p^T R_mu q = 2p.q - 2(p.q - p^T R_mu q) = 2p.q - 2*(something related to f)
# Actually, p^T R_mu q is not an f-function (f involves the same vector twice).
#
# Hmm, the cross terms involve different vectors p and q. This is the fundamental
# difficulty — f(R, p) = p^T(I-R)p only handles same-vector quadratics.
#
# Let me try a DIFFERENT decomposition. Instead of per-plaquette, try per-pair.

# ============================================================
# Part G: Check if 16||T||^2 - F_x decomposes into f-terms with MIXED vectors
# ============================================================
print("\n" + "=" * 70)
print("PART G: Looking for a clean decomposition of 16||T||^2 - F_x")
print("=" * 70)

# Let me directly compute 16||T||^2 - F_x and try to express it as a sum of
# p^T (I - R_k) p_k terms for various (R_k, p_k) pairs, ALL non-negative.

# Strategy: write 16||T||^2 - F_x in terms of the individual rotation parameters
# and try to factor.

# For UNIFORM color T_mu = s_mu * n (E006 result):
# 16|s|^2|n|^2 - F_x = 2*[group_02(n) + group_13(n) + active(n)] where each >= 0.
#
# The groups use f(R, n), f(RD, n), etc. — all with the SAME vector n.
#
# For GENERAL T, the analogous might use f(R, T_mu), f(R, T_nu), etc.
# But cross terms between T_mu and T_nu arise from plaquettes where both appear.
#
# KEY IDEA: What if the cross terms cancel when summed over all plaquettes?
#
# At each vertex, each direction mu appears in (d-1)=3 plaquettes.
# The cross term for plaquette (mu,nu) involves p^T [some rotation] q.
# Summing over plaquettes might yield a pattern.

# Let me compute the FULL expression 16||T||^2 - F_x and categorize all terms.

for trial_idx in range(3):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    # Direct computation
    F_x = 0
    for mu, nu in PLANES:
        B = compute_plaquette_B(R, D, T, mu, nu)
        F_x += np.dot(B, B)

    gap = 16 * np.sum(T**2) - F_x

    # Decompose into f-terms (same vector)
    f_same_total = 0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        fU = f_vec(U, T[mu])
        fW = f_vec(W, T[nu])
        f_same_total += 2*fU + 2*fW

    # Cross terms
    cross_total = 0
    for mu, nu in PLANES:
        p, q = T[mu], T[nu]
        cross_mat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T + D[(mu,nu)].T + R[nu].T
        cross_total += 2 * np.dot(p, cross_mat @ q) - 8 * np.dot(p, q)

    # Verify: gap = f_same_total + cross_total
    err = abs(gap - f_same_total - cross_total)
    print(f"\n  Trial {trial_idx}: gap = {gap:.4f}, f_same = {f_same_total:.4f}, "
          f"cross = {cross_total:.4f}, err = {err:.2e}")
    print(f"    f_same >= 0: {f_same_total >= -1e-10}, cross sign: {'pos' if cross_total > 0 else 'neg'}")

# ============================================================
# Part H: Analyze the cross term more carefully
# ============================================================
print("\n" + "=" * 70)
print("PART H: Structure of the cross term Sum_{mu<nu} [...]")
print("=" * 70)

# The cross term for plaquette (mu,nu) is:
#   2 T_mu^T (R_mu + R_mu D R_nu^T + D^T + R_nu^T) T_nu - 8 T_mu . T_nu
# = 2 T_mu^T (R_mu + D^T - 4I + R_nu^T + R_mu D R_nu^T) T_nu + (8 T_mu.T_nu - 8 T_mu.T_nu)
# Wait, let me redo: the total cross coefficient for T_mu^T ... T_nu per plaquette is:
#   2 T_mu^T (R_mu + R_mu D R_nu^T + D^T + R_nu^T - 4I) T_nu

# Define: C_{mu,nu} = R_mu + R_mu D_{mu,nu} R_nu^T + D_{mu,nu}^T + R_nu^T - 4I
# The cross term per plaquette = 2 T_mu^T C_{mu,nu} T_nu

# At Q=I: C = I + I + I + I - 4I = 0. So cross term = 0 at identity.
# The cross term is the "perturbation" that appears when Q != I.

# Let's check what happens when we SUM all cross terms.
# Total cross = 2 Sum_{mu<nu} T_mu^T C_{mu,nu} T_nu
# = T_vec^T [off-diagonal blocks of 2C] T_vec where C is a 12x12 matrix
# with C[mu,nu] block = C_{mu,nu}

# For the gap to be >= 0, we need: f_same_total + cross_total >= 0,
# i.e., the cross terms cannot dominate the f-same terms.

# Can we bound |cross_total| <= f_same_total?
# This would be a generalized Cauchy-Schwarz.

max_cross_to_fsame = 0
N_tests = 10000
for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    f_same = 0
    cross = 0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        f_same += 2*f_vec(U, T[mu]) + 2*f_vec(W, T[nu])

        p, q = T[mu], T[nu]
        cross_mat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T + D[(mu,nu)].T + R[nu].T - 4*np.eye(3)
        cross += 2 * np.dot(p, cross_mat @ q)

    if f_same > 1e-12:
        ratio = -cross / f_same  # negative cross means it helps, positive means it hurts
        max_cross_to_fsame = max(max_cross_to_fsame, ratio)

print(f"  Max (-cross / f_same): {max_cross_to_fsame:.6f} (need <= 1 for bound to hold)")
print(f"  Bound via f_same + cross >= 0 holds: {max_cross_to_fsame <= 1 + 1e-10}")

# Also check: is f_same ALWAYS >= |cross|? (stronger condition)
print(f"\n  f_same always >= |cross|: {max_cross_to_fsame <= 1 + 1e-10}")

print("\nDone with Task 3.")
