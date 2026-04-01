"""
Stage 2: Advanced approaches to proving sum_S >= 0.

Since per-pair polarization bounds fail, we try:
1. Symmetric-part-only bound (ignore antisymmetric)
2. Schur complement on 3x3 block structure
3. Direct algebraic decomposition into PSD summands
4. SOS search via Cholesky pattern analysis
"""
import numpy as np
from scipy.optimize import minimize as sp_minimize
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

P = np.zeros((12, 9))
for i in range(3):
    P[3*i:3*i+3, 3*i:3*i+3] = I3
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

def build_M9(R, D):
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    return (M9 + M9.T) / 2

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return I3.copy()
    k = v / theta
    K = skew(k)
    return I3 + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

# ============================================================
# APPROACH 1: Decompose M9 = M9(I) + Delta_sym_9 + Delta_anti_9
# Check if M9(I) + Delta_sym_9 >= 0 (i.e., antisymmetric HELPS)
# ============================================================
print("=" * 60)
print("APPROACH 1: Is M9(I) + sym_delta_9 always PSD?")
print("=" * 60)

def build_delta_sym_matrix(R, D):
    """Build the 9x9 matrix corresponding to sum of symmetric parts of delta."""
    M_delta_sym = np.zeros((12, 12))
    for mu, nu in PAIRS:
        E = I3 - D[(mu,nu)]
        E_sym = (E + E.T) / 2

        # u_{mu,nu} = R_mu^T T_mu - T_nu → extraction matrices
        # The contribution to M12 from 2 u^T E_sym v:
        # u = A_mu T_mu + A_nu T_nu where A_mu = R_mu^T (in mu block), A_nu = -I (in nu block)
        # v = B_mu T_mu + B_nu T_nu where B_mu = I (in mu block), B_nu = -R_nu^T (in nu block)
        # 2 u^T E_sym v contributes to M12:
        # (mu,mu): 2 R_mu E_sym I = 2 R_mu E_sym
        # (mu,nu): 2 R_mu E_sym (-R_nu^T) = -2 R_mu E_sym R_nu^T
        # (nu,mu): 2 (-I) E_sym I = -2 E_sym
        # (nu,nu): 2 (-I) E_sym (-R_nu^T) = 2 E_sym R_nu^T

        # Actually: 2 u^T E_sym v = 2 (sum_i A_i T_i)^T E_sym (sum_j B_j T_j)
        # Contribution to block (i,j) of M12: 2 A_i^T E_sym B_j
        # Wait, need symmetrization: the bilinear form should be symmetrized as a matrix

        # 2 u^T E_sym v is NOT symmetric in T unless we symmetrize.
        # The 12x12 matrix Q for this term is: Q[i,j] = A_i^T E_sym B_j
        # then 2 T^T Q T is what we add to M12.

        # But for the 9x9, we need to project. Let me just compute M9(D) - M9(I) directly.
        pass

    # Simpler approach: compute M9_full and M9_at_I, then decompose.
    return None

# Let me instead just compute the symmetric and antisymmetric contributions
def delta_sym_anti(R, D, T):
    """Compute symmetric and antisymmetric parts of delta."""
    ds = 0.0
    da = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        E = I3 - D[(mu,nu)]
        E_sym = (E + E.T) / 2
        E_anti = (E - E.T) / 2
        ds += 2 * u @ E_sym @ v
        da += 2 * u @ E_anti @ v
    return ds, da

# Compute M9 decomposition as matrices
def build_delta9_parts(R, D):
    """Build M9(D) - M9(I) and split into sym/anti contribution matrices."""
    D_I = {p: I3 for p in PAIRS}
    M9_full = build_M9(R, D)
    M9_I = build_M9(R, D_I)
    Delta9 = M9_full - M9_I

    # Build symmetric-delta matrix by replacing each D with (D+D^T)/2
    # This is NOT the same as the symmetric part of Delta9.
    # Instead, build M12 using E_sym in place of E.
    M12_sym = np.zeros((12, 12))
    M12_anti = np.zeros((12, 12))

    for mu, nu in PAIRS:
        E = I3 - D[(mu,nu)]
        E_sym = (E + E.T) / 2
        E_anti = (E - E.T) / 2

        R_mu_T = R[mu].T
        R_nu_T = R[nu].T

        # 2 u^T E v where u = R_mu^T T_mu - T_nu, v = T_mu - R_nu^T T_nu
        # = 2 (R_mu^T T_mu - T_nu)^T E (T_mu - R_nu^T T_nu)
        # Expand into 4 terms, each contributing to a block of M12
        # Term 1: 2 T_mu^T R_mu E T_mu → block (mu, mu)
        # Term 2: -2 T_mu^T R_mu E R_nu^T T_nu → block (mu, nu)
        # Term 3: -2 T_nu^T E T_mu → block (nu, mu)
        # Term 4: 2 T_nu^T E R_nu^T T_nu → block (nu, nu)

        # For the 12x12 matrix, the contribution of 2u^T E v to block (i,j):
        for E_part, M12_part in [(E_sym, M12_sym), (E_anti, M12_anti)]:
            M12_part[3*mu:3*mu+3, 3*mu:3*mu+3] += 2 * R_mu_T @ E_part  # not symmetric!
            M12_part[3*mu:3*mu+3, 3*nu:3*nu+3] += -2 * R_mu_T @ E_part @ R_nu_T
            M12_part[3*nu:3*nu+3, 3*mu:3*mu+3] += -2 * E_part
            M12_part[3*nu:3*nu+3, 3*nu:3*nu+3] += 2 * E_part @ R_nu_T

    Delta9_sym = P.T @ M12_sym @ P
    Delta9_anti = P.T @ M12_anti @ P

    # Verify: Delta9_sym + Delta9_anti should equal Delta9
    Delta9_check = Delta9_sym + Delta9_anti

    return M9_I, Delta9_sym, Delta9_anti, Delta9, Delta9_check

# Quick verification
R = {mu: random_SO3() for mu in range(4)}
D = {p: random_SO3() for p in PAIRS}

M9_I, D9s, D9a, D9, D9c = build_delta9_parts(R, D)
print(f"  Delta9 reconstruction error: {np.max(np.abs(D9 - D9c)):.2e}")

# Test: is M9(I) + Delta9_sym always PSD?
min_eig_sym = float('inf')
neg_count = 0
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    M9_I, D9s, D9a, D9, _ = build_delta9_parts(R, D)

    # M9(I) + symmetrized delta
    M_sym = M9_I + D9s
    M_sym = (M_sym + M_sym.T) / 2
    eig = np.linalg.eigvalsh(M_sym)[0]
    min_eig_sym = min(min_eig_sym, eig)
    if eig < -1e-8:
        neg_count += 1

print(f"\n  M9(I) + Delta9_sym (from E_sym):")
print(f"  Min eigenvalue: {min_eig_sym:.6f}")
print(f"  Negative count: {neg_count}/2000")

if neg_count == 0:
    print(f"  *** SYMMETRIC PART ALONE GIVES PSD! Anti part helps but not needed ***")
else:
    print(f"  Sym-only matrix can go negative → antisymmetric part IS needed")

# ============================================================
# APPROACH 2: Try M9 = sum of PSD matrices algebraically
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 2: Identify PSD components of M9")
print("=" * 60)

# M9 = sum_{mu<nu} [plaquette contribution]
# Each plaquette (mu,nu) contributes to 4 blocks of M12.
# After projection to V, each contributes a 9x9 matrix.

def plaquette_M9(R, D, mu, nu):
    """9x9 contribution from single plaquette (mu,nu)."""
    M12 = np.zeros((12, 12))
    U = R[mu] @ D[(mu,nu)]
    W = D[(mu,nu)] @ R[nu].T
    RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
    M12[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*I3 - U - U.T
    M12[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*I3 - W - W.T
    cross = D[(mu,nu)].T + RDR - 2*I3
    M12[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
    M12[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    M9 = P.T @ M12 @ P
    return (M9 + M9.T) / 2

# Check: which groupings of plaquettes give PSD?
print("  Testing plaquette groupings:")

# Opposite face pairs: {(0,1),(2,3)}, {(0,2),(1,3)}, {(0,3),(1,2)}
opp = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]

for trial in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    for gname, (p1, p2) in zip(['01+23', '02+13', '03+12'], opp):
        M = plaquette_M9(R, D, *p1) + plaquette_M9(R, D, *p2)
        eig = np.linalg.eigvalsh(M)[0]
        if trial == 0:
            print(f"    {gname}: min eig = {eig:.4f}")

# Test all 3 opposite pairs summed
min_opp = [float('inf')] * 3
neg_opp = [0] * 3
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    for idx, (p1, p2) in enumerate(opp):
        M = plaquette_M9(R, D, *p1) + plaquette_M9(R, D, *p2)
        eig = np.linalg.eigvalsh(M)[0]
        min_opp[idx] = min(min_opp[idx], eig)
        if eig < -1e-8:
            neg_opp[idx] += 1

print(f"\n  Opposite-face pairings (2000 trials):")
for idx, (name, (p1, p2)) in enumerate(zip(['01+23', '02+13', '03+12'], opp)):
    print(f"    {name}: min eig = {min_opp[idx]:.4f}, negative = {neg_opp[idx]}/2000")

# ============================================================
# APPROACH 3: Vertex grouping
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 3: Group by vertex — 4 vertices, each in 3 faces")
print("=" * 60)

# Each vertex mu is in 3 plaquettes. Group the 6 plaquettes by vertex:
# vertex 0: (0,1), (0,2), (0,3) — 3 plaquettes
# But each plaquette is shared between 2 vertices.

# Alternative: "star" decomposition
# star_mu = sum of plaquettes containing mu (each counted 1/2)
# Then M9 = sum_mu star_mu

# Or simpler: M9 = (1/2) sum_mu [sum of plaquettes containing mu]

# Check: is the star of a single vertex PSD?
min_star = [float('inf')] * 4
neg_star = [0] * 4
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    for mu_star in range(4):
        M = np.zeros((9, 9))
        for m, n in PAIRS:
            if m == mu_star or n == mu_star:
                M += plaquette_M9(R, D, m, n)
        eig = np.linalg.eigvalsh(M)[0]
        min_star[mu_star] = min(min_star[mu_star], eig)
        if eig < -1e-8:
            neg_star[mu_star] += 1

print(f"  Vertex star (3 plaquettes each), 2000 trials:")
for mu_star in range(4):
    print(f"    star({mu_star}): min eig = {min_star[mu_star]:.4f}, neg = {neg_star[mu_star]}/2000")

# ============================================================
# APPROACH 4: VCBL decomposition + remainder analysis
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 4: VCBL decomposition of M9")
print("=" * 60)

# sum ||a_mn - b_mn||^2 is manifestly >= 0 where:
# a = (I-U^T)T_mu, b = (I-W^T)T_nu
#
# As a matrix: M9_VCBL = P^T [sum outer products] P
# And M9 = M9_VCBL + M9_remainder
#
# Is M9_remainder PSD? Or NSD? Or indefinite?

def build_VCBL_M12(R, D):
    """Build 12x12 matrix for sum ||(I-U^T)T_mu - (I-W^T)T_nu||^2."""
    M = np.zeros((12, 12))
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        # a = (I-U^T)T_mu → linear map from T_mu: L_a = I-U^T acting on block mu
        # b = (I-W^T)T_nu → linear map from T_nu: L_b = I-W^T acting on block nu
        # ||a-b||^2 = T^T [L_a -L_b]^T [L_a -L_b] T
        L_a = I3 - U.T  # 3x3
        L_b = I3 - W.T  # 3x3
        # Block (mu,mu): L_a^T L_a
        M[3*mu:3*mu+3, 3*mu:3*mu+3] += L_a.T @ L_a
        # Block (nu,nu): L_b^T L_b
        M[3*nu:3*nu+3, 3*nu:3*nu+3] += L_b.T @ L_b
        # Block (mu,nu): -L_a^T L_b
        M[3*mu:3*mu+3, 3*nu:3*nu+3] += -L_a.T @ L_b
        # Block (nu,mu): -L_b^T L_a
        M[3*nu:3*nu+3, 3*mu:3*mu+3] += -L_b.T @ L_a
    return M

min_rem = float('inf')
neg_rem = 0
min_vcbl_eig = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    M12_full = build_M12(R, D)
    M12_vcbl = build_VCBL_M12(R, D)
    M12_rem = M12_full - M12_vcbl

    M9_rem = P.T @ M12_rem @ P
    M9_rem = (M9_rem + M9_rem.T) / 2

    M9_vcbl = P.T @ M12_vcbl @ P
    M9_vcbl = (M9_vcbl + M9_vcbl.T) / 2

    eig_rem = np.linalg.eigvalsh(M9_rem)[0]
    eig_vcbl = np.linalg.eigvalsh(M9_vcbl)[0]
    min_rem = min(min_rem, eig_rem)
    min_vcbl_eig = min(min_vcbl_eig, eig_vcbl)
    if eig_rem < -1e-8:
        neg_rem += 1

print(f"  M9 = M9_VCBL + M9_remainder")
print(f"  M9_VCBL: always PSD (by construction), min eig = {min_vcbl_eig:.4f}")
print(f"  M9_remainder: min eig = {min_rem:.4f}, negative = {neg_rem}/2000")

# ============================================================
# APPROACH 5: Direct Cholesky pattern analysis
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 5: Cholesky decomposition pattern analysis")
print("=" * 60)

# For PSD M9, compute Cholesky L and study structure
# Look at rank, sparsity, patterns in L

chol_ranks = []
for trial in range(200):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}

    M9 = build_M9(R, D)
    eigs = np.linalg.eigvalsh(M9)
    rank = np.sum(eigs > 1e-8)
    chol_ranks.append(rank)

print(f"  Rank of M9: min={min(chol_ranks)}, max={max(chol_ranks)}, "
      f"mode={max(set(chol_ranks), key=chol_ranks.count)}")

# For a single case, show the Cholesky structure
R = {mu: random_SO3() for mu in range(4)}
D = {p: random_SO3() for p in PAIRS}
M9 = build_M9(R, D)
eigs = np.linalg.eigvalsh(M9)
print(f"  Eigenvalues of sample M9: {np.sort(eigs)}")

# Check the null space structure at D=I
D_I = {p: I3 for p in PAIRS}
M9_I = build_M9(R, D_I)
eigs_I = np.linalg.eigvalsh(M9_I)
print(f"  Eigenvalues of M9(I): {np.sort(eigs_I)}")

# ============================================================
# APPROACH 6: Can we write M9 = sum_k c_k(D) * N_k(R)?
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 6: Separated R-D structure")
print("=" * 60)

# At D=I: M9(I) = baseline matrix (PSD, depends on R only)
# For general D: M9(D) = M9(I) + sum Delta contributions
# Each Delta involves BOTH R and D linearly.
# M9 entries are linear in D entries (since (I-D) is linear in D).

# So: M9(R, D) = M9(R, I) + sum_{(mu,nu)} L_{mu,nu}(R, D_{mu,nu})
# where L is linear in D_{mu,nu}.

# For fixed R, M9 is an AFFINE function of (D entries).
# So M9 is a "matrix pencil" in the D variables.

# For M9 >= 0 for all D in SO(3)^6, this is a robust semidefiniteness condition.

# Check: is M9 CONVEX in D? (We know it's not from E004, but let's double-check)
# M9 is AFFINE in D (linear + constant) → it IS convex (and concave) in D.
# So M9 >= 0 for all D iff M9 >= 0 at EXTREME POINTS of SO(3)^6.

# Wait! If M9 is affine in D_{mu,nu}, then along any line segment in D-space:
# M9(tD1 + (1-t)D2) = t M9(D1) + (1-t) M9(D2)
# This means: if M9(D1) >= 0 and M9(D2) >= 0, then M9(tD1+(1-t)D2) >= 0.

# BUT: D is constrained to SO(3), not all of R^{3x3}. The convex hull of SO(3)
# is {M : ||M||_op <= 1} (matrices with operator norm <= 1).

# So: M9 >= 0 for all D in SO(3)^6 iff M9 >= 0 for all D in co(SO(3))^6
# (convex hull) iff M9 >= 0 at extreme points of co(SO(3))^6.
# The extreme points of co(SO(3)) include SO(3) and also reflections O(3)?

# Actually, for 3x3 real matrices: the convex hull of SO(3) is the unit ball
# in operator norm. Extreme points are SO(3) itself.

# So M9 is affine in D, and D ranges over SO(3) (compact).
# min of min_eig(M9) over D is achieved at some boundary point of the D-space.

# KEY INSIGHT: Since M9 is LINEAR in each D_{mu,nu}, the minimum of min_eig
# over all D ∈ SO(3)^6 is achieved when each D is at an "extreme configuration"
# of SO(3) for the given direction.

# Actually, for a linear function of D, the minimum over the convex hull of
# SO(3) equals the minimum over SO(3) itself (since SO(3) is the extreme
# point set). And since M9 is affine (linear) in each D_{mu,nu}:
# The minimum over D in SO(3)^6 = minimum over D in co(SO(3))^6
# And by the extreme point theorem, it's achieved at a vertex.

# But co(SO(3)) = {M : ||M|| <= 1} for operator norm. Its extreme points are
# the orthogonal matrices O(3). Hmm, actually I need to be more careful about
# this.

# Let me just verify: is M9 linear in D?
R_test = {mu: random_SO3() for mu in range(4)}
D1 = {p: random_SO3() for p in PAIRS}
D2 = {p: random_SO3() for p in PAIRS}
t = 0.37

D_mix = {p: t*D1[p] + (1-t)*D2[p] for p in PAIRS}
M9_1 = build_M9(R_test, D1)
M9_2 = build_M9(R_test, D2)
M9_mix = build_M9(R_test, D_mix)
M9_interp = t * M9_1 + (1-t) * M9_2

err = np.max(np.abs(M9_mix - M9_interp))
print(f"  M9 linearity in D check: max error = {err:.2e}")
print(f"  (Should be ~0 if M9 is affine in D)")

if err < 1e-10:
    print(f"  *** CONFIRMED: M9 is AFFINE in D ***")
    print(f"  This means: M9 >= 0 on SO(3)^6 iff M9 >= 0 on convex hull of SO(3)^6")
    print(f"  The convex hull of SO(3) is the set of contractions (op norm <= 1)")

    # Test at D = 0 (zero matrix — inside convex hull of SO(3))
    D_zero = {p: np.zeros((3,3)) for p in PAIRS}
    M9_0 = build_M9(R_test, D_zero)
    eig_0 = np.linalg.eigvalsh(M9_0)
    print(f"\n  At D=0: min eig = {eig_0[0]:.4f}")

    # Test at D = -I (inside convex hull? det(-I) = -1, so -I in O(3) but not SO(3))
    # ||{-I}|| = 1, so -I is in the convex hull of SO(3)
    D_neg = {p: -I3 for p in PAIRS}
    M9_neg = build_M9(R_test, D_neg)
    eig_neg = np.linalg.eigvalsh(M9_neg)
    print(f"  At D=-I: min eig = {eig_neg[0]:.4f}")

    # The MINIMUM of min_eig over D in {||D|| <= 1} is what we need.
    # Since M9 is affine in D, the min_eig is a concave function of D
    # (min of affine functions). So its minimum over a convex set is at a
    # boundary point.

    # For D = alpha * I: M9(alpha I) = M9(I) + (alpha-1) * [M9(I) - M9(0)]
    # At alpha = 0: M9(0). At alpha = 1: M9(I). At alpha = -1: M9(-I).
    print(f"\n  M9 along D = alpha*I line:")
    for alpha in [-1, -0.5, 0, 0.5, 1]:
        D_a = {p: alpha * I3 for p in PAIRS}
        M9_a = build_M9(R_test, D_a)
        eig_a = np.linalg.eigvalsh(M9_a)[0]
        print(f"    alpha={alpha:5.1f}: min eig = {eig_a:.4f}")

# ============================================================
# APPROACH 7: Since M9 is affine in D, minimize over the
# UNCONSTRAINED D (operator norm constraint only)
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 7: M9 >= 0 over contractions?")
print("=" * 60)

# For fixed R, T (unit vector in the null eigenvector direction):
# f(D) = T^T M9(R, D) T is affine in D.
# Minimize f(D) over {D : ||D_p|| <= 1 for each pair p}.

# Since f is affine in D and D ranges over a product of unit balls,
# the minimum is achieved at D_p = argmin_{||D|| <= 1} contribution_p.
# Each plaquette contributes independently to the affine function.

# For a single plaquette (mu,nu), the contribution to M9 that depends on D is:
# 2 u^T (I-D) v (linear in D)
# The D-dependent part is -2 u^T D v (linear in D).
# For a FIXED direction in T-space, this becomes -2 u^T D v where u,v are fixed vectors.
# Minimizing -2 u^T D v over ||D|| <= 1: minimum = -2 ||u|| ||v|| (when D = -v u^T / (||u|| ||v||))

# So the minimum of sum_S over ALL contractions (not just SO(3)):
# min_contraction sum_S >= baseline - 2 sum_{mu<nu} ||u|| ||v||
# (by choosing worst-case D for each pair independently)

neg_contraction = 0
min_contraction = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    T = random_T_in_V()

    # Baseline
    bl = 6 * sum(f(R[mu], T[mu]) for mu in range(4))
    s = sum(R[mu].T @ T[mu] for mu in range(4))
    bl += np.dot(s, s)

    # Add f(D=I) contributions (the u^T(I-I)v = 0 at D=I) — but we're at D=I base
    # Actually we need the D-independent part plus the worst D contribution

    # From M9(D) = M9(I) + linear_in_D
    # The D-dependent part per pair: 2 u^T (-D) v → minimize over ||D|| <= 1 → -2||u||*||v||
    # But also the diagonal terms have D-dependence:
    # Actually let me just compute sum_S at worst-case D analytically.

    # sum_S(R, D, T) = baseline + sum 2 u^T (I-D) v
    # = baseline + sum 2(u^T u - u^T D v) ... wait, that's wrong
    # = baseline + sum 2[u^T v - u^T D v]

    # Actually: 2 u^T (I-D) v = 2(u·v) - 2(u^T D v)
    # So: sum_S = baseline + sum [2u·v - 2 u^T D v]
    # = baseline + sum 2u·v - 2 sum u^T D v

    # Wait, but the baseline is sum_S at D=I, which already includes the u^T(I-I)v = 0 terms.
    # So sum_S = baseline + sum 2u^T(I-D)v = baseline + sum 2u·v - 2 sum u^T D v...
    # No: at D=I, sum delta = 0. At general D:
    # sum_S(D) = sum_S(I) + sum 2u^T(I-D)v = baseline + sum [-2 u^T D v + 2u^T v - 2u^T v]
    # Hmm, this is getting confused. Let me just be direct.

    # Delta = sum 2 u^T (I-D) v = sum [2u·v - 2 u^T D v]
    # At D=I: Delta = 0 → sum 2u·v = sum 2 u^T I v → consistent.

    # For contraction D: minimize over ||D_p|| <= 1 independently:
    # minimize -2 u_p^T D_p v_p → min = -2 ||u_p|| * ||v_p||

    # So min delta over contractions = sum [2 u_p · v_p - 2 ||u_p|| * ||v_p||]
    #                                = sum 2[u_p · v_p - ||u_p|| * ||v_p||]
    #                                >= sum 2[-||u_p||*||v_p|| - ||u_p||*||v_p||]
    #                                = -4 sum ||u_p|| * ||v_p||
    # But actually u_p · v_p can be computed exactly.

    worst_delta = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        # Best D for this pair: D_opt = -v u^T / (||v|| ||u||) if ||u||, ||v|| > 0
        # giving -2 u^T D v = -2 u^T * (-vu^T/(||v||||u||)) * v = 2 ||u|| * (u^T v / (||u|| ||v||)) * ||v||
        # Wait, that's not right. Let me recompute.
        # -2 u^T D v: want to minimize over ||D|| <= 1.
        # -2 u^T D v = -2 Tr(D^T (vu^T)) (since u^T D v = Tr(v u^T D^T)... hmm)
        # Actually u^T D v = sum_{ij} u_i D_{ij} v_j = Tr(D^T u v^T)... no.
        # u^T D v = sum_i u_i (D v)_i = sum_{ij} u_i D_{ij} v_j
        # = Tr(u^T D v)... it's a scalar. In matrix terms: = vec(D)^T vec(u v^T)
        # Maximize u^T D v over ||D||_op <= 1: max = sigma_max of u v^T = ||u|| ||v||
        # (since u v^T has rank 1 with singular value ||u|| ||v||)
        # So minimize -u^T D v over ||D||_op <= 1: min = -||u|| ||v||

        # So the worst delta per pair: 2 u·v + 2*(-||u||*||v||)
        # = 2(u·v - ||u|| ||v||) <= 0
        worst_delta += 2*(np.dot(u, v) - np.linalg.norm(u)*np.linalg.norm(v))

    val = bl + worst_delta
    min_contraction = min(min_contraction, val)
    if val < -1e-8:
        neg_contraction += 1

print(f"  min(baseline + worst_delta over contractions): {min_contraction:.4f}")
print(f"  Negative: {neg_contraction}/2000")
if neg_contraction > 0:
    print(f"  *** M9 is NOT PSD over all contractions — SO(3) structure IS needed ***")
else:
    print(f"  *** M9 >= 0 even over contractions → SO(3) not needed, proof is easier ***")

# ============================================================
# APPROACH 8: Since M9 is affine, check D=-I extreme
# ============================================================
print("\n" + "=" * 60)
print("APPROACH 8: M9 at D = -I (worst extreme of convex hull)")
print("=" * 60)

neg_at_neg_I = 0
min_at_neg_I = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: -I3 for p in PAIRS}
    M9 = build_M9(R, D)
    eig = np.linalg.eigvalsh(M9)[0]
    min_at_neg_I = min(min_at_neg_I, eig)
    if eig < -1e-8:
        neg_at_neg_I += 1

print(f"  M9 at D = -I for all pairs:")
print(f"  Min eigenvalue: {min_at_neg_I:.4f}")
print(f"  Negative: {neg_at_neg_I}/2000")

# D = rotation by pi around random axis (this IS in SO(3))
neg_at_pi = 0
min_at_pi = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    # D = rotation by pi (eigenvalues 1, -1, -1)
    D = {}
    for p in PAIRS:
        n = np.random.randn(3)
        n /= np.linalg.norm(n)
        D[p] = 2*np.outer(n, n) - I3  # rotation by pi around n
    M9 = build_M9(R, D)
    eig = np.linalg.eigvalsh(M9)[0]
    min_at_pi = min(min_at_pi, eig)
    if eig < -1e-8:
        neg_at_pi += 1

print(f"\n  M9 at D = rotation by pi:")
print(f"  Min eigenvalue: {min_at_pi:.4f}")
print(f"  Negative: {neg_at_pi}/2000")
