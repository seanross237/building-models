"""
Decompose sum_S = 2*sum VCBL(U,W,-I,...) + sum remainder
Check if the remainder can be proved >= 0 via the constraint.
Also try other M choices per plaquette.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh
from scipy.optimize import minimize

np.random.seed(42)
I3 = np.eye(3)

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return np.eye(3)
    k = v / theta
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def f(R, p):
    return p @ (I3 - R) @ p

P = np.zeros((12, 9))
P[0:3, 0:3] = I3; P[3:6, 3:6] = I3; P[6:9, 6:9] = I3
P[9:12, 0:3] = -I3; P[9:12, 3:6] = -I3; P[9:12, 6:9] = -I3

# ============================================================
# Step 1: Compute the remainder R = sum_S - 2*sum VCBL(-I)
# ============================================================
print("=" * 70)
print("Step 1: VCBL(-I) remainder per plaquette")
print("=" * 70)

# For a single plaquette (mu,nu):
# S = 2f(U,p) + 2f(W,q) - 2p^T(2I - D^T - RDR)q
# 2*VCBL(-I) = 2f(U,p) + 2f(W,q) - 2p^T(I-U)(I-W^T)q
#
# remainder = S - 2*VCBL(-I) = -2p^T[(2I-D^T-RDR) - (I-U)(I-W^T)]q
# = 2p^T[(I-U)(I-W^T) - (2I-D^T-RDR)]q
#
# Let C = (I-U)(I-W^T) - (2I-D^T-RDR)
# = I - W^T - U + UW^T - 2I + D^T + RDR
# = -I + D^T - U - W^T + UW^T + RDR
#
# Using W^T = R_nu D^T, U = R_mu D, D^T = U^T R_mu, RDR = U R_nu^T:
# C = -I + U^T R_mu - R_mu D - R_nu D^T + R_mu D R_nu D^T + U R_nu^T
#
# Hmm, let me also try:
# D^T = D^{-1} for D in SO(3)
# U^T = D^T R_mu^T
# W = D R_nu^T, so W^T = R_nu D^T

def compute_C(R_mu, R_nu, D_mn):
    U = R_mu @ D_mn
    W = D_mn @ R_nu.T
    RDR = R_mu @ D_mn @ R_nu.T
    IU = I3 - U
    IWT = I3 - W.T
    cross_mat = 2*I3 - D_mn.T - RDR
    C = IU @ IWT - cross_mat
    return C

# Test: at R=I, C should be 0
C_RI = compute_C(I3, I3, special_ortho_group.rvs(3))
print(f"C at R=I: ||C|| = {np.linalg.norm(C_RI):.2e}")  # Should be 0!

# Hmm, at R_mu = R_nu = I:
# U = D, W = D, RDR = D
# (I-D)(I-D^T) = 2I - D - D^T
# 2I - D^T - D = 2I - D^T - D
# C = (2I - D - D^T) - (2I - D^T - D) = 0. ✓

# For general R:
for trial in range(5):
    R_mu = special_ortho_group.rvs(3)
    R_nu = special_ortho_group.rvs(3)
    D_mn = special_ortho_group.rvs(3)
    C = compute_C(R_mu, R_nu, D_mn)
    print(f"Trial {trial}: ||C|| = {np.linalg.norm(C):.4f}, eigs(Sym(C)) = {np.linalg.eigvalsh((C+C.T)/2)}")

# ============================================================
# Step 2: Build remainder as 12x12 matrix, project to 9x9
# ============================================================
print("\n" + "=" * 70)
print("Step 2: Remainder matrix analysis")
print("=" * 70)

def build_remainder_12(R, D_dict):
    """Build 12x12 matrix for the remainder = sum_S - 2*sum VCBL(-I)."""
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            C = compute_C(R[mu], R[nu], D_dict[(mu,nu)])
            # remainder per plaquette = 2 p^T C q
            # In 12x12 matrix: 2*C goes to (mu,nu) block, 2*C^T to (nu,mu) block
            # But wait: the quadratic form T^T M T has T_mu^T M_{mu,nu} T_nu + T_nu^T M_{nu,mu} T_mu
            # = T_mu^T [M_{mu,nu} + M_{nu,mu}^T] T_nu
            # We need this = 2 T_mu^T C T_nu, so M_{mu,nu} = C and M_{nu,mu} = C^T works
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += C
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += C.T
    return (M + M.T) / 2

# Check: is the remainder PSD on V?
rem_violations = 0
for _ in range(1000):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)

    M_rem = build_remainder_12(R, D_dict)
    M9_rem = P.T @ M_rem @ P
    M9_rem = (M9_rem + M9_rem.T)/2
    me = eigvalsh(M9_rem)[0]
    if me < -1e-10:
        rem_violations += 1

print(f"Remainder PSD on V: {rem_violations}/1000 violations")

# Optimize for min eigenvalue of remainder
def min_eig_remainder(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}
    idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu, nu)] = so3_from_vec(params[idx:idx+3])
            idx += 3
    M_rem = build_remainder_12(R, D_dict)
    M9 = P.T @ M_rem @ P
    return eigvalsh((M9 + M9.T)/2)[0]

best_rem = float('inf')
bestp_rem = None
for _ in range(3000):
    p = np.random.randn(30) * np.pi
    v = min_eig_remainder(p)
    if v < best_rem:
        best_rem = v
        bestp_rem = p.copy()

res_rem = minimize(min_eig_remainder, bestp_rem, method='Nelder-Mead',
                   options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Remainder min eigenvalue: {res_rem.fun:.8f}")

# ============================================================
# Step 3: Simplify C algebraically
# ============================================================
print("\n" + "=" * 70)
print("Step 3: Algebraic simplification of C")
print("=" * 70)

# C = (I-U)(I-W^T) - (2I - D^T - RDR)
# = I - R_nu D^T - R_mu D + R_mu D R_nu D^T - 2I + D^T + R_mu D R_nu^T
# = -I + (I-R_nu)D^T - R_mu D + R_mu D R_nu D^T + R_mu D R_nu^T
# = -I + (I-R_nu)D^T + R_mu D(-I + R_nu D^T + R_nu^T)
# = -I + (I-R_nu)D^T + R_mu D R_nu(D^T + R_nu^{-1} R_nu^T ... hmm

# Let me try: factor out (I-R_mu) and (I-R_nu)
# C = -I + D^T - R_nu D^T + R_mu D R_nu^T - R_mu D + R_mu D R_nu D^T
# = (D^T - I) + R_nu(D R_mu D)^T ... no

# Actually let me try to write C in terms of (I-R_mu) and (I-R_nu).
# C has the property C = 0 when R_mu = R_nu = I.
# So C should be expressible in terms of I-R_mu and I-R_nu.

# C = I - R_nu D^T - R_mu D + R_mu D R_nu D^T - 2I + D^T + R_mu D R_nu^T
# Group terms:
# = (D^T - R_nu D^T) + (R_mu D R_nu^T - R_mu D) + (R_mu D R_nu D^T - 2I + I)
# Hmm still messy. Let me try substitution R_mu = I + E_mu, R_nu = I + F_nu

# Actually, let me try:
# C = (I-R_nu)D^T + R_mu D(R_nu^T - I) + R_mu D R_nu D^T - I
# = (I-R_nu)D^T - R_mu D(I - R_nu^T) + R_mu D R_nu D^T - I
# Note: R_nu D^T for SO(3): (R_nu D^T)^T = D R_nu^T
# R_mu D R_nu D^T = U R_nu D^T = U(R_nu D^T)

# Let me just verify the formula differently
# C = (I-U)(I-W^T) - (2I - D^T - U R_nu^T)
# = I - (I-R_nu D^T) - (R_mu D) + R_mu D (R_nu D^T) - 2I + D^T + R_mu D R_nu^T
# Simplify: = I - I + R_nu D^T - R_mu D + R_mu D R_nu D^T - 2I + D^T + R_mu D R_nu^T
# Wait I already did this. Let me go more slowly.
# C = -I + R_nu D^T + D^T - R_mu D + R_mu D R_nu D^T + R_mu D R_nu^T

# Factor: (1 + R_nu)D^T + R_mu D(R_nu D^T + R_nu^T - I) - I
# Hmm. Let me try a direct substitution to see the structure.

# C = (I-R_nu)D^T + R_mu D (R_nu^T - I) + (R_mu D R_nu D^T - I)
# Check: at R_mu = R_nu = I:
# (I-I)D^T + D(I-I) + (D D^T - I) = 0 + 0 + (I - I) = 0 ✓

# So C = (I-R_nu)D^T - R_mu D(I-R_nu^T) + (R_mu D R_nu D^T - I)
# The third term: R_mu D R_nu D^T = U(D^T R_mu^T)^T wait...
# R_mu D R_nu D^T. At R_mu = I: D R_nu D^T. At R_nu = I: R_mu. So this is like a "twisted product".

# Let me verify the formula above:
R_mu = special_ortho_group.rvs(3)
R_nu = special_ortho_group.rvs(3)
D_mn = special_ortho_group.rvs(3)

C_direct = compute_C(R_mu, R_nu, D_mn)
C_alt = (I3 - R_nu) @ D_mn.T - R_mu @ D_mn @ (I3 - R_nu.T) + (R_mu @ D_mn @ R_nu @ D_mn.T - I3)
print(f"C formula check: {np.allclose(C_direct, C_alt)}")

# The third term R_mu D R_nu D^T is interesting. It's the product of two "conjugated" rotations.
# Note that D R_nu D^T is R_nu rotated by D (conjugation in SO(3)).
# So R_mu D R_nu D^T = R_mu * (D R_nu D^T) = product of R_mu with D-conjugate of R_nu.

# For the third term: R_mu * conj_D(R_nu) - I = (I - R_mu^{-1}) + R_mu^{-1}(R_mu conj_D(R_nu) - I)
# ... still messy.

# ============================================================
# Step 4: Try SUM_S with different VCBL M choices
# ============================================================
print("\n" + "=" * 70)
print("Step 4: Try M = -R_mu^T R_nu for VCBL")
print("=" * 70)

# S_{mu,nu} = 2f(U,p) + 2f(W,q) - 2p^T X q where X = 2I - D^T - RDR
# 2*VCBL(U,W,M,p,q) = 2f(U,p) + 2f(W,q) + 2p^T(I-U)M(I-W^T)q
#
# S = 2*VCBL(U,W,M,...) iff (I-U)M(I-W^T) = -X = D^T + RDR - 2I
#
# Try M = -R_mu^T (note ||R_mu^T||_op = 1, so VCBL valid with this M):
# (I-U)(-R_mu^T)(I-W^T) = -(I-R_mu D)R_mu^T(I-R_nu D^T)
# = -(R_mu^T - D)(I - R_nu D^T)
# wait: (I-R_mu D)R_mu^T = R_mu^T - R_mu D R_mu^T
# hmm: D R_mu^T is not D in general.

# Let me just compute this numerically for the target equation
for trial in range(5):
    R_mu = special_ortho_group.rvs(3)
    R_nu = special_ortho_group.rvs(3)
    D_mn = special_ortho_group.rvs(3)
    U = R_mu @ D_mn
    W = D_mn @ R_nu.T
    RDR = R_mu @ D_mn @ R_nu.T

    target = D_mn.T + RDR - 2*I3

    # Try various M choices
    for M_choice, M_name in [(-I3, "-I"), (-R_mu.T, "-R_mu^T"), (-R_nu, "-R_nu"), (R_mu.T @ R_nu, "R_mu^T R_nu"), (-D_mn, "-D")]:
        achieved = (I3 - U) @ M_choice @ (I3 - W.T)
        error = np.linalg.norm(achieved - target)
        if trial == 0:
            print(f"  M = {M_name}: error = {error:.4f}")

# ============================================================
# Step 5: Think about sum_S differently — use the S_{mu,nu} per-plaquette expression
# ============================================================
print("\n" + "=" * 70)
print("Step 5: Per-plaquette S as a combined f-term")
print("=" * 70)

# From E002: S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T C_{mu,nu} T_nu
# where the C in E002 is: C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-RDR)
# So the cross term -2 T_mu^T [(I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-RDR)] T_nu

# And total_gap = sum S_{mu,nu} over plaquettes
# = sum [2f(U,T_mu) + 2f(W,T_nu)] - 2 sum T_mu^T C T_nu
# = f_same - 2 sum T_mu^T [(I-R_mu) + (I-R_nu^T)] T_nu - 2 sum T_mu^T [(I-D^T) + (I-RDR)] T_nu

# The sum-to-zero trick gives:
# -2 sum T_mu^T [(I-R_mu) + (I-R_nu^T)] T_nu = 2 sum_mu f(R_mu, T_mu) >= 0  [PROVED]

# So total_gap = 2 sum_mu f(R_mu, T_mu) + sum_S
# where sum_S uses the (I-D^T) + (I-RDR) cross terms.

# Now within sum_S:
# sum_S = f_same - 2 sum T_mu^T [(I-D^T) + (I-RDR)] T_nu
# = sum [2f(U,T_mu) + 2f(W,T_nu)] + sum [2 T_mu^T (D^T + RDR - 2I) T_nu]

# Can we apply the sum-to-zero trick AGAIN to the D^T and RDR terms?
# sum_{mu<nu} T_mu^T D^T_{mu,nu} T_nu — this involves different D for each pair, so
# the trick sum T_mu^T T_nu = -||T||^2/2 doesn't directly apply to the D-dependent part.

# But what if we split: D^T = I + (D^T - I)?
# sum T_mu^T D^T T_nu = sum T_mu^T T_nu + sum T_mu^T (D^T - I) T_nu
# = -||T||^2/2 + sum T_mu^T (D^T - I) T_nu
#
# Similarly for RDR:
# sum T_mu^T RDR T_nu = sum T_mu^T T_nu + sum T_mu^T (RDR - I) T_nu
# = -||T||^2/2 + sum T_mu^T (RDR - I) T_nu

# So sum_S = f_same + 2*(-||T||^2/2 + sum (D^T-I)) + 2*(-||T||^2/2 + sum (RDR-I)) - 4*(-||T||^2/2)
# Wait let me recompute.
# sum_S = f_same + 2 sum T_mu^T (D^T + RDR - 2I) T_nu
# = f_same + 2 sum T_mu^T D^T T_nu + 2 sum T_mu^T RDR T_nu - 4 sum T_mu^T T_nu
# = f_same + 2(-||T||^2/2 + delta_D) + 2(-||T||^2/2 + delta_RDR) - 4(-||T||^2/2)
# = f_same + (-||T||^2 + 2*delta_D) + (-||T||^2 + 2*delta_RDR) + 2||T||^2
# = f_same + 2*delta_D + 2*delta_RDR
# where delta_D = sum T_mu^T (D^T-I) T_nu and delta_RDR = sum T_mu^T (RDR-I) T_nu

# Verify:
R = [special_ortho_group.rvs(3) for _ in range(4)]
D = {}
for mu in range(4):
    for nu in range(mu+1, 4):
        D[(mu,nu)] = special_ortho_group.rvs(3)
T = [np.random.randn(3) for _ in range(3)]
T.append(-T[0]-T[1]-T[2])
nsq = sum(t@t for t in T)

f_same = sum(2*f(R[mu]@D[(mu,nu)], T[mu]) + 2*f(D[(mu,nu)]@R[nu].T, T[nu])
             for mu in range(4) for nu in range(mu+1, 4))
delta_D = sum(T[mu] @ (D[(mu,nu)].T - I3) @ T[nu] for mu in range(4) for nu in range(mu+1, 4))
delta_RDR = sum(T[mu] @ (R[mu]@D[(mu,nu)]@R[nu].T - I3) @ T[nu] for mu in range(4) for nu in range(mu+1, 4))

sumS_direct = f_same + 2*sum(T[mu] @ (D[(mu,nu)].T + R[mu]@D[(mu,nu)]@R[nu].T - 2*I3) @ T[nu]
                              for mu in range(4) for nu in range(mu+1, 4))
sumS_formula = f_same + 2*delta_D + 2*delta_RDR
print(f"sum_S direct: {sumS_direct:.8f}")
print(f"f_same + 2*delta_D + 2*delta_RDR: {sumS_formula:.8f}")
print(f"Match: {abs(sumS_direct - sumS_formula) < 1e-8}")

# ============================================================
# Step 6: Individual VCBL bounds
# ============================================================
print("\n" + "=" * 70)
print("Step 6: Can VCBL absorb the full cross term?")
print("=" * 70)

# Per plaquette: VCBL(U,W,M,p,q) = f(U,p) + f(W,q) + p^T(I-U)M(I-W^T)q
# With M=-I: VCBL(-I) = f(U,p) + f(W,q) - p^T(I-U)(I-W^T)q
# = f(U,p) + f(W,q) - (I-U^T)p . (I-W^T)q (dot product of defect vectors)
# = ||a||^2/2 + ||b||^2/2 - a.b (where a=(I-U^T)p, b=(I-W^T)q)
# = (||a|| - ||b||)^2/2 + ||a|| ||b|| - a.b >= 0 since a.b <= ||a|| ||b||.

# So 2*VCBL(-I) = ||a||^2 + ||b||^2 - 2a.b = ||a-b||^2 >= 0!

# Beautiful! So 2*VCBL(U,W,-I,p,q) = ||(I-U^T)p - (I-W^T)q||^2 >= 0

# And sum_S = sum ||(I-U^T)T_mu - (I-W^T)T_nu||^2 + sum_remainder

# Let me verify:
for trial in range(3):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D[(mu,nu)] = special_ortho_group.rvs(3)
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    sum_sq = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U = R[mu] @ D[(mu,nu)]
            W = D[(mu,nu)] @ R[nu].T
            a = (I3 - U.T) @ T[mu]
            b = (I3 - W.T) @ T[nu]
            sum_sq += np.linalg.norm(a - b)**2

    # 2*sum VCBL(-I)
    sum_vcbl = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U = R[mu] @ D[(mu,nu)]
            W = D[(mu,nu)] @ R[nu].T
            sum_vcbl += 2*(f(U, T[mu]) + f(W, T[nu]) - T[mu] @ (I3-U) @ (-I3) @ (I3 - W.T) @ T[nu])

    print(f"sum ||a-b||^2 = {sum_sq:.6f}, 2*sum VCBL(-I) = {sum_vcbl:.6f}, match: {abs(sum_sq-sum_vcbl)<1e-8}")

# ============================================================
# Step 7: Remainder = sum_S - sum ||a-b||^2
# ============================================================
print("\n" + "=" * 70)
print("Step 7: Remainder = sum_S - sum ||a-b||^2 analysis")
print("=" * 70)

# remainder = sum_S - sum ||a-b||^2
# Per plaquette: r_{mu,nu} = 2T_mu^T C T_nu where C is computed above
# This is a PURE cross term (no diagonal contribution)!

# Build the remainder 12x12 matrix (only off-diagonal blocks)
def build_remainder_12(R, D_dict):
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            C = compute_C(R[mu], R[nu], D_dict[(mu,nu)])
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += C
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += C.T
    return (M + M.T) / 2

# Test: is the remainder >= 0 on V?
rem_min = float('inf')
for _ in range(500):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)
    M_rem = build_remainder_12(R, D_dict)
    M9 = P.T @ M_rem @ P; M9 = (M9+M9.T)/2
    me = eigvalsh(M9)[0]
    rem_min = min(rem_min, me)

print(f"Remainder min eigenvalue (random): {rem_min:.6f}")

# ============================================================
# Step 8: Alternative decomposition — VCBL with M = -D^T or other choices
# ============================================================
print("\n" + "=" * 70)
print("Step 8: Alternative VCBL decompositions")
print("=" * 70)

# Try different M for each plaquette and check remainder
# Key constraint: ||M||_op <= 1 for VCBL to hold
# Candidates: -I, -D^T, -R_mu^T, -R_nu, D^T R_mu^T R_nu = (R_nu^T R_mu D)^T

# For each plaquette, find the M that minimizes the remainder
# The VCBL cross term is p^T(I-U)M(I-W^T)q
# S cross term is -p^T(2I - D^T - RDR)q
# So we need (I-U)M(I-W^T) closest to -(2I - D^T - RDR) = D^T + RDR - 2I
# subject to ||M||_op <= 1

# The optimal M minimizes || (I-U)M(I-W^T) - target ||_F
# This is a constrained optimization. For fixed (I-U), (I-W^T) (rank 2 each),
# the product (I-U)M(I-W^T) lives in a rank-2 image space.

# Simpler approach: just check sum_S >= 0 directly using per-plaquette VCBL
# with the BEST M per plaquette (optimized).

# Actually, the most promising insight from Step 6:
# 2*VCBL(-I) = ||a - b||^2 where a = (I-U^T)T_mu, b = (I-W^T)T_nu
# This means sum 2*VCBL(-I) = sum ||(I-U^T)T_mu - (I-W^T)T_nu||^2
# = sum ||a_{mu,nu}||^2 where a_{mu,nu} = defect(U,T_mu) - defect(W,T_nu)

# And sum_S = sum ||a_{mu,nu}||^2 + remainder

# The remainder is off-diagonal only. Let me see if the constraint makes it >= 0.

# CRITICAL TEST: remainder with constraint optimization
best_rem2 = float('inf')
bestp2 = None
for _ in range(3000):
    p = np.random.randn(30) * np.pi
    R_t = [so3_from_vec(p[3*i:3*(i+1)]) for i in range(4)]
    D_t = {}; idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_t[(mu,nu)] = so3_from_vec(p[idx:idx+3]); idx += 3
    M_rem = build_remainder_12(R_t, D_t)
    M9 = P.T @ M_rem @ P; M9 = (M9+M9.T)/2
    me = eigvalsh(M9)[0]
    if me < best_rem2:
        best_rem2 = me
        bestp2 = p.copy()

def min_eig_rem(params):
    R_t = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_t = {}; idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_t[(mu,nu)] = so3_from_vec(params[idx:idx+3]); idx += 3
    M_rem = build_remainder_12(R_t, D_t)
    M9 = P.T @ M_rem @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

res_rem2 = minimize(min_eig_rem, bestp2, method='Nelder-Mead',
                    options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Remainder optimized min eig: {res_rem2.fun:.8f}")

if res_rem2.fun < -0.01:
    print("REMAINDER IS NOT PSD ON V — need a different decomposition")
else:
    print("REMAINDER APPEARS PSD ON V — proof strategy:")
    print("  sum_S = sum ||(I-U^T)T_mu - (I-W^T)T_nu||^2 + remainder")
    print("  Both terms >= 0 on V, so sum_S >= 0!")
