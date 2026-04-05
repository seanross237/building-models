"""
Direct analysis of sum_S as a quadratic form.

Key insight: sum_S = 0 at Q=I and appears >= 0 everywhere.
Can we find a matrix decomposition that proves sum_S >= 0?

Strategy: Write the 12x12 matrix for sum_S and find conditions under which
its projection to V is PSD.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh
from scipy.optimize import minimize

np.random.seed(42)
I3 = np.eye(3)
I12 = np.eye(12)

P = np.zeros((12, 9))
P[0:3, 0:3] = I3; P[3:6, 3:6] = I3; P[6:9, 6:9] = I3
P[9:12, 0:3] = -I3; P[9:12, 3:6] = -I3; P[9:12, 6:9] = -I3

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return np.eye(3)
    k = v / theta
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def f(R, p):
    return p @ (I3 - R) @ p

# ============================================================
# Approach A: Gram matrix decomposition
# ============================================================
print("=" * 70)
print("Approach A: Try to write sum_S matrix as a Gram matrix G^T G")
print("=" * 70)

# sum_S 12x12 matrix:
# Diagonal (mu,mu) = 2*sum_{nu partner} [I - Sym(R_mu D)] + 2*sum_{nu partner} [I - Sym(D R_nu^T)]
#   (where Sym(A) is the symmetric part used in quadratic form, but since T^T A T = T^T Sym(A) T,
#    the effective diagonal is sum of (2I - R_mu D - D^T R_mu^T)/2 etc.)
#
# Actually the raw sum_S matrix has the FULL (non-symmetrized) matrices, then we
# symmetrize the 12x12 at the end.

def build_sumS_12(R, D_dict):
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            U = R[mu] @ Dmn
            W = Dmn @ R[nu].T
            RDR = R[mu] @ Dmn @ R[nu].T

            # Budget: 2f(U,T_mu) + 2f(W,T_nu)
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*(I3 - U)
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*(I3 - W)

            # Cross: -2T_mu^T(2I - D^T - RDR)T_nu
            cross = Dmn.T + RDR - 2*I3  # negative of cross matrix
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    return (M + M.T) / 2

# ============================================================
# Approach B: Factor sum_S as sum of ||v_k||^2 terms
# ============================================================
print("\n" + "=" * 70)
print("Approach B: Try explicit vector decomposition")
print("=" * 70)

# For each plaquette (mu,nu), define defect vectors:
# a_{mu,nu} = (I - U_{mu,nu}^T) T_mu  [lives in R^3]
# b_{mu,nu} = (I - W_{mu,nu}^T) T_nu  [lives in R^3]
#
# Note: ||a||^2 = 2f(U,T_mu), ||b||^2 = 2f(W,T_nu)
#
# sum ||a||^2 + sum ||b||^2 = f_same (the budget)
#
# Now sum_S = f_same + 2*sum T_mu^T(D^T + RDR - 2I)T_nu
# = sum(||a||^2 + ||b||^2) + 2*sum T_mu^T(D^T + RDR - 2I)T_nu
#
# Using D^T = U^T R_mu and RDR = U R_nu^T:
# T_mu^T D^T T_nu = T_mu^T U^T R_mu T_nu = (U T_mu)·(R_mu T_nu)
# = (T_mu - (I-U)T_mu)·(R_mu T_nu) = T_mu·R_mu T_nu - ((I-U)T_mu)·(R_mu T_nu)
#
# Let a' = (I-U)T_mu [note: a = (I-U^T)T_mu and ||a||=||a'|| for U in SO(3)]
# Then T_mu^T D^T T_nu = T_mu^T R_mu^T ... wait

# Actually: T_mu^T U^T R_mu T_nu
# and U = R_mu D, so U^T R_mu = D^T R_mu^T R_mu = D^T.
# So T_mu^T U^T R_mu T_nu = T_mu^T D^T T_nu. Circular.

# Let me try a completely different approach.
# ============================================================
# Approach C: Express sum_S in terms of "color-rotated" vectors
# ============================================================
print("\n" + "=" * 70)
print("Approach C: Color-rotated vectors")
print("=" * 70)

# Define S_mu = R_mu T_mu for each mu.
# Then f(R_mu, T_mu) = T_mu^T(I-R_mu)T_mu = |T_mu|^2 - T_mu^T R_mu T_mu
#                    = |T_mu|^2 - S_mu · T_mu
# And the various products:
# T_mu^T R_mu D T_mu = S_mu^T D T_mu = S_mu · (D T_mu)
# T_mu^T R_mu D R_nu^T T_nu = S_mu^T D R_nu^T T_nu = S_mu · (D R_nu^T T_nu) = S_mu · (W T_nu)

# Hmm. Let's also define:
# e_mu = D_{mu,nu} T_mu  (D-rotated T_mu)
# Then T_mu^T D^T T_nu = e_mu · T_nu   ... but D depends on (mu,nu), not just mu.

# With 6 different D matrices, we can't simplify to per-vertex quantities.

# ============================================================
# Approach D: Second-order expansion around Q = I
# ============================================================
print("\n" + "=" * 70)
print("Approach D: Taylor expansion of sum_S around Q = I")
print("=" * 70)

# Parameterize: R_mu = exp(epsilon r_mu), D_{mu,nu} = exp(epsilon d_{mu,nu})
# where r_mu and d_{mu,nu} are 3x3 antisymmetric matrices.
# At first order in epsilon: R_mu ≈ I + epsilon r_mu, D ≈ I + epsilon d_{mu,nu}

# U = R_mu D ≈ I + epsilon(r_mu + d_{mu,nu})
# W = D R_nu^T ≈ I + epsilon(d_{mu,nu} - r_nu)
# RDR = R_mu D R_nu^T ≈ I + epsilon(r_mu + d_{mu,nu} - r_nu)

# f(U,T_mu) ≈ T_mu^T(-epsilon(r+d))T_mu = -epsilon T_mu^T(r+d)T_mu
# Wait, f(U,T) = T^T(I-U)T ≈ T^T(-epsilon(r+d))T for the first-order part.
# For a skew-symmetric r, T^T r T = 0 (skew quad form vanishes).
# So f(U,T) starts at O(epsilon^2).

# At order epsilon^2: U ≈ I + epsilon(r+d) + epsilon^2(r+d)^2/2
# f(U,T) ≈ T^T(-(r+d) epsilon - (r+d)^2 epsilon^2/2)T
# Since T^T(r+d)T = 0 (skew), f(U,T) ≈ -epsilon^2/2 * T^T(r+d)^2 T
# For skew A, -A^2 is PSD, so f(U,T) >= 0 as expected.

# Cross terms at O(epsilon^2):
# 2I - D^T - RDR ≈ 2I - (I-epsilon d + epsilon^2 d^T d/2) - (I + epsilon(r-r'+d) + epsilon^2(...)/2)
# ≈ -epsilon(d^T + r + d - r') + O(epsilon^2)
# Wait, d^T = -d for skew d, so D^T ≈ I - epsilon d + epsilon^2 d^2/2
# And RDR ≈ I + epsilon(r+d-r') + epsilon^2(...)

# 2I - D^T - RDR ≈ 2I - I + epsilon d - I - epsilon(r+d-r') + O(eps^2)
# = epsilon(d - r - d + r') = epsilon(r' - r)
# = epsilon(r_nu - r_mu)

# So cross term: T_mu^T * epsilon(r_nu - r_mu) * T_nu

# But r_mu is skew-symmetric, so T_mu^T r_nu T_nu is not necessarily 0
# (it's skew in different coordinates).

# sum_S at O(epsilon^2):
# Budget = sum 2f(U,T) + 2f(W,T) ≈ 2*sum [-epsilon^2/2 T^T(r+d)^2 T + ...]
# = epsilon^2 * sum [-T_mu^T(r_mu + d_{mu,nu})^2 T_mu - T_nu^T(d_{mu,nu} - r_nu)^2 T_nu]
# Cross = 2*sum T_mu^T * epsilon(r_nu - r_mu) * T_nu

# The cross term is O(epsilon) while budget is O(epsilon^2).
# But wait, T_mu^T(r_nu - r_mu)T_nu — if r_mu, r_nu are skew, this is real (not zero).
# So cross term IS O(epsilon), which means sum_S ~ O(epsilon) to leading order.

# Let's check: sum_{mu<nu} T_mu^T(r_nu - r_mu)T_nu
# = sum_{mu<nu} T_mu^T r_nu T_nu - sum_{mu<nu} T_mu^T r_mu T_nu
# = sum_nu r_nu . (sum_{mu<nu} T_mu) . T_nu - sum_mu r_mu . T_mu . (sum_{nu>mu} T_nu)
# Using sum-to-zero: sum_{mu: mu<nu} T_mu = -(T_nu + sum_{mu>nu} T_mu) = -T_nu - sum_{mu>nu} T_mu

# Hmm, this is getting complicated. Let me just verify numerically.

epsilon = 0.01
r = [np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]) for v in [np.random.randn(3) for _ in range(4)]]
d_vecs = [np.random.randn(3) for _ in range(6)]
d = [np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]) for v in d_vecs]

from scipy.linalg import expm

R = [expm(epsilon * r[mu]) for mu in range(4)]
D_dict = {}
idx = 0
for mu in range(4):
    for nu in range(mu+1, 4):
        D_dict[(mu,nu)] = expm(epsilon * d[idx])
        idx += 1

T = [np.random.randn(3) for _ in range(3)]
T.append(-T[0]-T[1]-T[2])

M12 = build_sumS_12(R, D_dict)
M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
eigs = eigvalsh(M9)
nsq = sum(t@t for t in T)

# sum_S value
sumS = sum(t) if (t := [T[mu] @ M12[3*mu:3*mu+3, 3*nu:3*nu+3] @ T[nu] for mu in range(4) for nu in range(4)]) else 0
# Actually just compute it directly
tvec = np.concatenate(T)
sumS = tvec @ M12 @ tvec

print(f"epsilon = {epsilon}")
print(f"sum_S = {sumS:.8f}")
print(f"sum_S / epsilon^2 = {sumS/epsilon**2:.4f}")
print(f"sum_S / epsilon = {sumS/epsilon:.4f}")
print(f"min eig(M9) = {eigs[0]:.8f}")

# Try different epsilons to see scaling
for eps in [0.001, 0.01, 0.1, 0.5, 1.0]:
    R = [expm(eps * r[mu]) for mu in range(4)]
    D_dict = {}; idx = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = expm(eps * d[idx]); idx += 1
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    me = eigvalsh(M9)[0]
    print(f"  eps={eps:.3f}: min_eig={me:.6f}, min_eig/eps^2={me/eps**2:.4f}")

# ============================================================
# Approach E: Combinatorial structure using plaquette pairs
# ============================================================
print("\n" + "=" * 70)
print("Approach E: Group plaquettes into complementary pairs")
print("=" * 70)

# The 6 plaquettes pair into 3 complementary pairs:
# Group A: (0,1) + (2,3) — disjoint indices
# Group B: (0,2) + (1,3)
# Group C: (0,3) + (1,2)
#
# For each group, the two plaquettes have disjoint first indices and disjoint second indices.
# With T_3 = -T_0 - T_1 - T_2, the indices overlap through T_3.

# For group A: sum_S contribution from (0,1) and (2,3):
# S_{01} + S_{23}
# The cross terms involve T_0^T(...)T_1 and T_2^T(...)T_3
# With T_3 = -T_0-T_1-T_2: T_2^T(...)T_3 = -T_2^T(...)T_0 - T_2^T(...)T_1 - T_2^T(...)T_2
# So the group A cross terms couple ALL T_0, T_1, T_2.

# Check: does each group contribute non-negatively?
violations_per_group = {g: 0 for g in ['A', 'B', 'C']}
groups = {
    'A': [(0,1), (2,3)],
    'B': [(0,2), (1,3)],
    'C': [(0,3), (1,2)]
}

for _ in range(5000):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    for gname, pairs in groups.items():
        val = 0
        for mu, nu in pairs:
            Dmn = D_dict[(mu,nu)]
            U = R[mu] @ Dmn; W = Dmn @ R[nu].T; RDR = R[mu] @ Dmn @ R[nu].T
            val += 2*f(U, T[mu]) + 2*f(W, T[nu])
            val -= 2*T[mu] @ (2*I3 - Dmn.T - RDR) @ T[nu]
        if val < -1e-10:
            violations_per_group[gname] += 1

print("Per-group violations (5000 tests):")
for g in ['A', 'B', 'C']:
    print(f"  Group {g}: {violations_per_group[g]}/5000")

# ============================================================
# Approach F: Explicit factorization attempt
# ============================================================
print("\n" + "=" * 70)
print("Approach F: Check if sum_S = sum_i ||v_i(T)||^2 for some linear v_i")
print("=" * 70)

# If M_9(Q) is PSD, it has a Cholesky decomposition M_9 = L L^T.
# Each row of L gives a linear functional v_i, and M_9 = sum v_i v_i^T.
# The question: is there a UNIVERSAL choice of v_i (independent of Q)?
# Answer: almost certainly no (because the matrix structure varies with Q).
# But the Cholesky WORKS for each fixed Q (since M_9 is PSD).

# Let me verify by computing Cholesky for many Q:
cholesky_failures = 0
for _ in range(1000):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    try:
        L = np.linalg.cholesky(M9 + 1e-14*np.eye(9))  # Small regularization
    except np.linalg.LinAlgError:
        cholesky_failures += 1

print(f"Cholesky failures (with 1e-14 regularization): {cholesky_failures}/1000")

# ============================================================
# Approach G: Write sum_S using the 6 defect vectors a_{mu,nu}, b_{mu,nu}
# ============================================================
print("\n" + "=" * 70)
print("Approach G: Defect vector representation")
print("=" * 70)

# a_{mu,nu} = (I-U^T)T_mu (3D vector)
# b_{mu,nu} = (I-W^T)T_nu (3D vector)
# For each plaquette, we have 2 defect vectors. Total: 12 vectors in R^3.
#
# Budget = sum(||a||^2 + ||b||^2)
# Cross per plaquette = 2 T_mu^T (D^T + RDR - 2I) T_nu
#
# Can we express the cross in terms of a, b, and additional defect-like vectors?
#
# T_mu^T D^T T_nu = T_mu^T U^T R_mu T_nu
# = (U T_mu)^T (R_mu T_nu)
# Let c_mu = R_mu T_mu = T_mu + (R_mu - I)T_mu. Then R_mu T_nu is similar but with nu.
# (U T_mu) = (R_mu D T_mu) and R_mu T_nu are both "rotated T" vectors.
#
# T_mu^T RDR T_nu = T_mu^T U R_nu^T T_nu = (U^T T_mu)^T (R_nu^T T_nu)
# Hmm, these are inner products of rotated T vectors.

# Key insight: define for each (mu,nu):
#   p_{mu,nu} = R_mu T_nu  (3D vector, R_mu applied to T_nu)
# Then:
#   T_mu^T D^T T_nu = T_mu^T U^T R_mu T_nu = (R_mu D T_mu) · (R_mu T_nu)
#   = (U T_mu) · p_{mu,nu}   [where p_{mu,nu} = R_mu T_nu]

# Also U T_mu = T_mu - (I-U)T_mu. And (I-U)T_mu = R_mu(I-D)T_mu ... hmm.

# Actually (I-U)T_mu = (I-R_mu D)T_mu and (I-U^T)T_mu are related:
# ||(I-U)T_mu||^2 = ||(I-U^T)T_mu||^2 = 2f(U,T_mu)  (verified earlier)

# This approach is getting too complex for a clean proof. Let me try something simpler.

# ============================================================
# Approach H: Prove sum_S >= 0 via VCBL applied to appropriately PAIRED vectors
# ============================================================
print("\n" + "=" * 70)
print("Approach H: VCBL on combined (sum-constrained) vectors")
print("=" * 70)

# The sum-to-zero trick for the (I-R) terms used:
# sum_{mu<nu} T_mu^T(I-R_mu)T_nu = -1/2 sum_mu T_mu^T(I-R_mu)(sum_{nu!=mu} T_nu)
# = -1/2 sum_mu T_mu^T(I-R_mu)(-T_mu) = 1/2 sum f(R_mu, T_mu)
#
# Can we do something similar for the D-dependent terms?
# sum_{mu<nu} T_mu^T (I-D^T_{mu,nu}) T_nu
# This is NOT the same as sum_{mu<nu} T_mu^T A_mu T_nu for a per-vertex A_mu.
# The matrix D depends on the PAIR (mu,nu), not just one index.
# So the sum-to-zero trick doesn't directly apply.

# HOWEVER, if all D_{mu,nu} were the SAME D, then:
# sum T_mu^T(I-D^T)T_nu = (I-D^T) . sum_{mu<nu} T_mu^T T_nu * ... no
# sum T_mu^T(I-D^T)T_nu = ... this would factor as (sum T_mu)^T(I-D^T)(sum T_nu) type thing? No.

# For a single D: sum_{mu<nu} T_mu^T(I-D^T)T_nu = (I-D^T) * (-||T||^2/2) using sum T = 0
# Wait: T_mu^T(I-D^T)T_nu includes (I-D^T) as a MATRIX, not scalar.
# sum_{mu<nu} T_mu^T (I-D^T) T_nu = Tr[(I-D^T) * sum_{mu<nu} T_nu T_mu^T]

# sum_{mu<nu} T_nu T_mu^T = (1/2)[(sum T_mu)(sum T_nu)^T - sum T_mu T_mu^T]
# = (1/2)[0 - sum T_mu T_mu^T] = -1/2 * (T outer sum)
# Hmm, sum_{mu<nu} T_nu T_mu^T is the off-diagonal outer product sum.
# (sum T_mu)(sum T_mu)^T = sum_mu T_mu T_mu^T + 2*sum_{mu<nu} T_mu T_nu^T
# 0 = sum T_mu T_mu^T + 2*sum_{mu<nu} T_mu T_nu^T (using symmetry in swap)
# Wait: sum_{mu,nu} T_mu T_nu^T = sum_mu T_mu T_mu^T + sum_{mu!=nu} T_mu T_nu^T
# And sum_{mu!=nu} T_mu T_nu^T = sum_{mu<nu} (T_mu T_nu^T + T_nu T_mu^T)

# Let S_T = sum_mu T_mu T_mu^T (3x3 PSD matrix)
# Then 0 = (sum T_mu)(sum T_mu)^T = S_T + sum_{mu!=nu} T_mu T_nu^T
# So sum_{mu!=nu} T_mu T_nu^T = -S_T
# sum_{mu<nu} (T_mu T_nu^T + T_nu T_mu^T) = -S_T
# sum_{mu<nu} T_mu T_nu^T = (-S_T - sum_{mu<nu}(T_mu T_nu^T - T_nu T_mu^T))/2 + ...
# Actually: sum_{mu<nu} T_mu T_nu^T + sum_{mu<nu} T_nu T_mu^T = -S_T
# These aren't individually determined.

# For our purposes:
# sum_{mu<nu} T_mu^T (I-D) T_nu (single D for all pairs)
# = sum_{mu<nu} Tr[(I-D) T_nu T_mu^T]
# ... let me just check: if all D the same:
# sum_{mu<nu} T_mu^T (I-D^T) T_nu = Tr[(I-D^T)^T sum_{mu<nu} T_mu T_nu^T]? NO.
# T_mu^T A T_nu = Tr[A T_nu T_mu^T], so
# sum_{mu<nu} T_mu^T (I-D^T) T_nu = Tr[(I-D^T) sum_{mu<nu} T_nu T_mu^T]

# And sum_{mu<nu} T_nu T_mu^T is just the sum of rank-1 matrices T_nu T_mu^T for mu<nu.
# We know sum_{mu<nu} (T_mu T_nu^T + T_nu T_mu^T) = -S_T.

# For single D: sum T_mu^T(I-D^T)T_nu = Tr[(I-D^T) * (-S_T - sum_{mu<nu} T_nu T_mu^T)/2 + ...]
# This is getting circular. Let me just compute it numerically.

D_single = special_ortho_group.rvs(3)
T = [np.random.randn(3) for _ in range(3)]
T.append(-T[0]-T[1]-T[2])
S_T = sum(np.outer(T[mu], T[mu]) for mu in range(4))

cross_single = sum(T[mu] @ (I3 - D_single.T) @ T[nu] for mu in range(4) for nu in range(mu+1, 4))
# Compare with Tr[(I-D^T) sum T_nu T_mu^T] for mu<nu
sum_outer = sum(np.outer(T[nu], T[mu]) for mu in range(4) for nu in range(mu+1, 4))
cross_trace = np.trace((I3 - D_single.T) @ sum_outer)
print(f"Cross (single D): {cross_single:.6f}")
print(f"Via trace: {cross_trace:.6f}")
print(f"S_T = sum T T^T:\n{S_T}")
print(f"sum_{mu<nu} T_nu T_mu^T:\n{sum_outer}")

# Also compute: sum_{mu<nu} T_mu^T T_nu (scalar)
scalar_cross = sum(T[mu] @ T[nu] for mu in range(4) for nu in range(mu+1, 4))
print(f"\nsum T_mu.T_nu = {scalar_cross:.6f}")
nsq = sum(t@t for t in T)
print(f"-||T||^2/2 = {-nsq/2:.6f}")
print(f"Match: {abs(scalar_cross + nsq/2) < 1e-10}")

# So for scalar (D=I): sum T_mu^T(I-I)T_nu = 0. And for D=I in the matrix sense:
# sum T_mu^T(I-I^T)T_nu = 0. Both trivial.

# The KEY difficulty: with 6 different D matrices, we can't use sum-to-zero to simplify.
# But maybe we can bound the D-dependent terms using the budget.

# ============================================================
# Approach I: Direct SDP relaxation
# ============================================================
print("\n" + "=" * 70)
print("Approach I: SDP-style bound — ratio test")
print("=" * 70)

# For sum_S >= 0, we need: budget >= -cross for all Q and T.
# budget = sum 2f(U,T_mu) + 2f(W,T_nu) >= 0
# cross = 2 sum T_mu^T(D^T + RDR - 2I)T_nu  (can be positive or negative)
#
# When cross <= 0 (harmful), we need budget >= |cross|.
#
# Worst case ratio = max |cross| / budget when cross < 0.
# If this ratio < 1 always, we're done.

max_ratio = 0
for _ in range(10000):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    budget = sum(2*f(R[mu]@D_dict[(mu,nu)], T[mu]) + 2*f(D_dict[(mu,nu)]@R[nu].T, T[nu])
                 for mu in range(4) for nu in range(mu+1, 4))
    cross = 2*sum(T[mu] @ (D_dict[(mu,nu)].T + R[mu]@D_dict[(mu,nu)]@R[nu].T - 2*I3) @ T[nu]
                  for mu in range(4) for nu in range(mu+1, 4))

    if cross < -1e-10 and budget > 1e-10:
        ratio = abs(cross) / budget
        max_ratio = max(max_ratio, ratio)

print(f"Max |harmful cross|/budget ratio: {max_ratio:.4f}")
print(f"Ratio < 1? {max_ratio < 1}")

# Also do adversarial optimization of the ratio
def neg_ratio(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}; idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = so3_from_vec(params[idx:idx+3]); idx += 3

    # Also need to optimize over T — use the worst T for this Q
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

# We already know this gives ~0, but let me verify the ratio interpretation:
# sum_S >= 0 iff budget + cross >= 0 iff budget >= -cross (when cross < 0)
# iff |cross|/budget <= 1 (when cross < 0 and budget > 0)
# But budget could be 0 when cross is also 0 (at Q=I).

print("\nVerified: sum_S min eigenvalue ~ 0 (see earlier tests)")
print("This means max |cross|/budget ratio -> 1 in the limit")
