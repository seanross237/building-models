"""
Investigate sum_S = LEMMA_D + LEMMA_RDR algebraically.

sum_S = sum_{mu<nu} [2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu)
                      - 2 T_mu^T(I - D^T)T_nu
                      - 2 T_mu^T(I - R_mu D R_nu^T)T_nu]

The budget (f terms) appear twice (once from each lemma).
The cross terms are -(I-D^T) and -(I-R_mu D R_nu^T).

Key: (I-D^T) + (I-R_mu D R_nu^T) = 2I - D^T - R_mu D R_nu^T

So sum_S = sum_{mu<nu} [2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(2I - D^T - R_mu D R_nu^T)T_nu]

where U = R_mu D, W = D R_nu^T.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh
from scipy.optimize import minimize

np.random.seed(42)

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return np.eye(3)
    k = v / theta
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def f(R, p):
    return p @ (np.eye(3) - R) @ p

I3 = np.eye(3)

# ============================================================
# Step 1: Write sum_S explicitly and verify
# ============================================================
print("=" * 70)
print("Step 1: Verify sum_S algebraic form")
print("=" * 70)

def compute_sumS_direct(T, R, D):
    """Direct computation of sum_S."""
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            U = R[mu] @ Dmn
            W = Dmn @ R[nu].T
            RDR = R[mu] @ Dmn @ R[nu].T
            val += 2*f(U, T[mu]) + 2*f(W, T[nu])
            val -= 2 * T[mu] @ (I3 - Dmn.T) @ T[nu]
            val -= 2 * T[mu] @ (I3 - RDR) @ T[nu]
    return val

def compute_sumS_combined_cross(T, R, D):
    """sum_S with combined cross term."""
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            U = R[mu] @ Dmn
            W = Dmn @ R[nu].T
            RDR = R[mu] @ Dmn @ R[nu].T
            budget = 2*f(U, T[mu]) + 2*f(W, T[nu])
            # Combined cross: 2I - D^T - R_mu D R_nu^T
            cross = 2 * T[mu] @ (2*I3 - Dmn.T - RDR) @ T[nu]
            val += budget - cross
    return val

# Test
R = [special_ortho_group.rvs(3) for _ in range(4)]
D = {}
for mu in range(4):
    for nu in range(mu+1, 4):
        D[(mu,nu)] = special_ortho_group.rvs(3)
T = [np.random.randn(3) for _ in range(3)]
T.append(-T[0]-T[1]-T[2])

s1 = compute_sumS_direct(T, R, D)
s2 = compute_sumS_combined_cross(T, R, D)
print(f"Direct: {s1:.10f}")
print(f"Combined: {s2:.10f}")
print(f"Match: {abs(s1-s2) < 1e-10}")

# ============================================================
# Step 2: Rewrite sum_S using the identity f(M,p) = |p|^2 - p^T M p
# ============================================================
print("\n" + "=" * 70)
print("Step 2: Expand sum_S")
print("=" * 70)

# f(U,T_mu) = |T_mu|^2 - T_mu^T U T_mu = |T_mu|^2 - T_mu^T R_mu D T_mu
# f(W,T_nu) = |T_nu|^2 - T_nu^T W T_nu = |T_nu|^2 - T_nu^T D R_nu^T T_nu

# Budget = 2*sum_{mu<nu} [|T_mu|^2 + |T_nu|^2 - T_mu^T U T_mu - T_nu^T W T_nu]
#        = 2*[3||T||^2 - sum_{mu<nu} (T_mu^T R_mu D T_mu + T_nu^T D R_nu^T T_nu)]

# Cross = 2*sum_{mu<nu} T_mu^T (2I - D^T - R_mu D R_nu^T) T_nu
#        = 4*sum_{mu<nu} T_mu^T T_nu - 2*sum_{mu<nu} T_mu^T D^T T_nu - 2*sum_{mu<nu} T_mu^T R_mu D R_nu^T T_nu
#        = 4*(-||T||^2/2) - 2*sum D_cross - 2*sum RDR_cross
#        = -2||T||^2 - 2*sum D_cross - 2*sum RDR_cross

# So sum_S = budget - cross
#          = 6||T||^2 - 2*rot_budget + 2||T||^2 + 2*sum D_cross + 2*sum RDR_cross
#          = 8||T||^2 - 2*rot_budget + 2*sum D_cross + 2*sum RDR_cross

nsq = sum(t@t for t in T)
rot_budget = sum(
    T[mu] @ R[mu] @ D[(mu,nu)] @ T[mu] + T[nu] @ D[(mu,nu)] @ R[nu].T @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
D_cross = sum(T[mu] @ D[(mu,nu)].T @ T[nu] for mu in range(4) for nu in range(mu+1, 4))
RDR_cross = sum(T[mu] @ R[mu] @ D[(mu,nu)] @ R[nu].T @ T[nu] for mu in range(4) for nu in range(mu+1, 4))

sumS_formula = 8*nsq - 2*rot_budget + 2*D_cross + 2*RDR_cross
print(f"sum_S formula: 8||T||^2 - 2*rot + 2*D_cross + 2*RDR_cross")
print(f"= {8*nsq:.4f} - {2*rot_budget:.4f} + {2*D_cross:.4f} + {2*RDR_cross:.4f} = {sumS_formula:.4f}")
print(f"Direct: {s1:.4f}")
print(f"Match: {abs(sumS_formula - s1) < 1e-8}")

# ============================================================
# Step 3: Factor sum_S differently using VCBL structure
# ============================================================
print("\n" + "=" * 70)
print("Step 3: VCBL-based decomposition of sum_S")
print("=" * 70)

# For each plaquette (mu,nu), define:
# a_{mu,nu} = (I - U^T)T_mu = (I - D^T R_mu^T)T_mu   [note: ||a||^2 = 2f(U,T_mu)]
# b_{mu,nu} = (I - W^T)T_nu = (I - R_nu D^T)T_nu     [note: ||b||^2 = 2f(W,T_nu)]
#
# VCBL says: ||a||^2/2 + ||b||^2/2 + a^T M b >= 0 for ANY M in SO(3)
# i.e., f(U,T_mu) + f(W,T_nu) >= -a^T M b >= -||a||*||b||
#
# The cross term in sum_S involves:
# T_mu^T (D^T + R_mu D R_nu^T) T_nu - 2 T_mu^T T_nu
#
# Can we express T_mu^T D^T T_nu in terms of a and b?
# a = T_mu - D^T R_mu^T T_mu, b = T_nu - R_nu D^T T_nu
# T_mu = a + D^T R_mu^T T_mu, T_nu = b + R_nu D^T T_nu
#
# T_mu^T D^T T_nu = (a + D^T R_mu^T T_mu)^T D^T (b + R_nu D^T T_nu)
# This is getting complicated. Let's try a different approach.

# ============================================================
# Step 4: Write sum_S as a sum of VCBL-type terms plus remainder
# ============================================================
print("\n" + "=" * 70)
print("Step 4: sum_S = 2*sum VCBL + remainder?")
print("=" * 70)

# Each plaquette S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(2I - D^T - RDR)T_nu
#
# Compare with 2*VCBL(U,W,M,T_mu,T_nu) = 2[f(U,T_mu) + f(W,T_nu) + T_mu^T(I-U)M(I-W^T)T_nu]
# = 2f(U,T_mu) + 2f(W,T_nu) + 2T_mu^T(I-U)M(I-W^T)T_nu
#
# So S_{mu,nu} = 2*VCBL(U,W,M,...) - 2T_mu^T(I-U)M(I-W^T)T_nu - 2T_mu^T(2I - D^T - RDR)T_nu
# = 2*VCBL(U,W,M,...) - 2T_mu^T[(I-U)M(I-W^T) + 2I - D^T - RDR]T_nu
#
# The remainder vanishes if (I-U)M(I-W^T) = -(2I - D^T - RDR) for some M.
# Let's check if this can work with a specific M.
#
# (I-U)(I-W^T) = (I-R_mu D)(I - R_nu D^T)
# = I - R_nu D^T - R_mu D + R_mu D D^T R_nu^{-1}   wait D in SO(3) so D D^T = I
# = I - R_nu D^T - R_mu D + R_mu R_nu^{-1}    wait R_nu^T = R_nu^{-1}
# Actually D^T = D^{-1} since D in SO(3), so D D^T = I.
# And R_nu^T = R_nu^{-1}.
#
# (I-U)(I-W^T) = I - R_nu D^T - R_mu D + R_mu D D^T R_nu^T ... wait
#
# U = R_mu D, W = D R_nu^T
# (I-U) = I - R_mu D
# (I-W^T) = I - (D R_nu^T)^T = I - R_nu D^T
# (I-U)(I-W^T) = (I - R_mu D)(I - R_nu D^T)
# = I - R_nu D^T - R_mu D + R_mu D R_nu D^T
#
# Hmm, the last term is R_mu D R_nu D^T, not R_mu D R_nu^T.
#
# Compare with what we need: -(2I - D^T - RDR) = D^T + R_mu D R_nu^T - 2I
#
# So we need: (I-U)(I-W^T) + correction = D^T + R_mu D R_nu^T - 2I
# (I - R_nu D^T - R_mu D + R_mu D R_nu D^T) + correction = D^T + R_mu D R_nu^T - 2I
# correction = D^T + R_mu D R_nu^T - 2I - I + R_nu D^T + R_mu D - R_mu D R_nu D^T
# = D^T + R_nu D^T - 3I + R_mu D + R_mu D R_nu^T - R_mu D R_nu D^T
# Messy. Let me just check M=I numerically.

def compute_VCBL(U, W, M, p, q):
    return f(U, p) + f(W, q) + p @ (I3 - U) @ M @ (I3 - W.T) @ q

def S_per_plaquette(T_mu, T_nu, R_mu, R_nu, D_mn):
    U = R_mu @ D_mn
    W = D_mn @ R_nu.T
    RDR = R_mu @ D_mn @ R_nu.T
    return 2*f(U, T_mu) + 2*f(W, T_nu) - 2*T_mu @ (2*I3 - D_mn.T - RDR) @ T_nu

# With M=I: VCBL = f(U,p) + f(W,q) + p^T(I-U)(I-W^T)q
# S = 2*VCBL_I + remainder, where remainder = S - 2*VCBL_I
for trial in range(5):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D[(mu,nu)] = special_ortho_group.rvs(3)
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    sumS = 0
    sum_VCBL = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U = R[mu] @ D[(mu,nu)]
            W = D[(mu,nu)] @ R[nu].T
            s = S_per_plaquette(T[mu], T[nu], R[mu], R[nu], D[(mu,nu)])
            v_I = compute_VCBL(U, W, I3, T[mu], T[nu])
            sumS += s
            sum_VCBL += v_I

    print(f"Trial {trial}: sum_S = {sumS:.4f}, 2*sum_VCBL(M=I) = {2*sum_VCBL:.4f}, remainder = {sumS - 2*sum_VCBL:.4f}")

# ============================================================
# Step 5: Can we decompose S_{mu,nu} as 2*VCBL(U,W,M,...) with suitable M?
# ============================================================
print("\n" + "=" * 70)
print("Step 5: Find M such that S_{mu,nu} = 2*VCBL(U,W,M,...)")
print("=" * 70)

# S = 2f(U,p) + 2f(W,q) - 2p^T(2I - D^T - RDR)q
# 2*VCBL = 2f(U,p) + 2f(W,q) + 2p^T(I-U)M(I-W^T)q
# S = 2*VCBL iff (I-U)M(I-W^T) = -(2I - D^T - RDR) = D^T + RDR - 2I

# Check: is (I-U)(I-W^T) = D^T + RDR - 2I for some special case?
# At R=I: U = D, W = D, so (I-D)(I-D^T) = I - D - D^T + I = 2I - D - D^T
# And D^T + D - 2I = -(2I - D - D^T) = -(I-D)(I-D^T)
# So at R=I: need (I-D)M(I-D^T) = -(I-D)(I-D^T)
# => M = -I (if I-D is invertible)

# Check: does VCBL hold with M = -I? VCBL requires ||M|| <= 1 for the CS bound,
# but -I has ||M|| = 1. Actually VCBL was proved for M in SO(3).
# -I is in O(3) but not SO(3) (det = -1).

# Actually, let me re-read the VCBL proof. It says:
# f(A,p) + f(B,q) + p^T(I-A)D(I-B^T)q >= 0 for all A,B,D in SO(3)
# The proof uses |p^T(I-A)D(I-B^T)q| <= ||a|| ||b|| where a=(I-A^T)p, b=(I-B^T)q
# and AM-GM: ||a||^2/2 + ||b||^2/2 >= ||a|| ||b|| >= |cross term|

# So the bound is: budget >= |cross|. This uses ||D|| = 1 (operator norm).
# -I also has ||M|| = 1. But -I is not in SO(3).
# The proof works for ANY M with ||M|| <= 1, not just SO(3)!

print("VCBL works for any M with ||M||_op <= 1, not just SO(3)!")
print("So M = -I is valid for VCBL.")

# At R=I: S = 2*VCBL(D, D, -I, ...) provided VCBL with M=-I holds
# Let's check: VCBL(D, D, -I, p, q) = f(D,p) + f(D,q) + p^T(I-D)(-I)(I-D^T)q
# = f(D,p) + f(D,q) - p^T(I-D)(I-D^T)q
# = f(D,p) + f(D,q) - ||(I-D^T)p||*... no wait, this is just the value.
# ||(I-D^T)p||^2 = 2f(D,p)

# At R=I, S = 2f(D,p) + 2f(D,q) - 2p^T(2I - D^T - D)q
# = 2f(D,p) + 2f(D,q) - 4p^T(I - (D+D^T)/2)q
# Note f(D,p) = p^T(I-D)p and (D+D^T)/2 is symmetric part.
# p^T(I - (D+D^T)/2)q is the symmetric bilinear form associated with f_sym.

# And 2*VCBL(D,D,-I,p,q) = 2f(D,p) + 2f(D,q) - 2p^T(I-D)(I-D^T)q
# = 2f(D,p) + 2f(D,q) - 2p^T(2I - D - D^T)q  [since (I-D)(I-D^T) = 2I-D-D^T for D in SO(3)]
# = 2f(D,p) + 2f(D,q) - 4p^T(I - (D+D^T)/2)q

# So at R=I: S = 2*VCBL(D,D,-I,p,q)! Great!
# And VCBL(D,D,-I,p,q) >= 0 since ||-I||_op = 1.

# Let's verify:
R_I = [I3]*4
for trial in range(5):
    D = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D[(mu,nu)] = special_ortho_group.rvs(3)
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    sumS = sum(S_per_plaquette(T[mu], T[nu], R_I[mu], R_I[nu], D[(mu,nu)])
               for mu in range(4) for nu in range(mu+1, 4))
    sum_VCBL_neg = sum(
        2*compute_VCBL(D[(mu,nu)], D[(mu,nu)], -I3, T[mu], T[nu])
        for mu in range(4) for nu in range(mu+1, 4)
    )
    print(f"R=I: sum_S = {sumS:.6f}, 2*sum_VCBL(D,D,-I) = {sum_VCBL_neg:.6f}, match = {abs(sumS - sum_VCBL_neg) < 1e-8}")

# ============================================================
# Step 6: General R case — find M(R_mu, R_nu, D) such that S = 2*VCBL(U,W,M,...)
# ============================================================
print("\n" + "=" * 70)
print("Step 6: General case — find M for each plaquette")
print("=" * 70)

# S_{mu,nu} = 2*VCBL(U,W,M,...) requires:
# (I-U)M(I-W^T) = D^T + RDR - 2I
#
# Where U = R_mu D, W = D R_nu^T.
# (I-U)^{-1} exists when U != I (i.e., R_mu D != I).
# When it exists: M = (I-U)^{-1} (D^T + RDR - 2I) (I-W^T)^{-1}

# Let's compute M for random configs and check its operator norm.

for trial in range(10):
    R_mu = special_ortho_group.rvs(3)
    R_nu = special_ortho_group.rvs(3)
    Dmn = special_ortho_group.rvs(3)

    U = R_mu @ Dmn
    W = Dmn @ R_nu.T
    RDR = R_mu @ Dmn @ R_nu.T

    IU = I3 - U
    IW_T = I3 - W.T  # = I - R_nu D^T

    target = Dmn.T + RDR - 2*I3

    # Check invertibility
    det_IU = np.linalg.det(IU)
    det_IWT = np.linalg.det(IW_T)

    if abs(det_IU) > 0.01 and abs(det_IWT) > 0.01:
        M = np.linalg.solve(IU, target) @ np.linalg.inv(IW_T)
        op_norm = np.linalg.norm(M, 2)  # operator 2-norm
        # Check
        check = IU @ M @ IW_T
        print(f"Trial {trial}: ||M||_op = {op_norm:.4f}, check error = {np.linalg.norm(check - target):.2e}")
    else:
        print(f"Trial {trial}: singular (det(I-U)={det_IU:.4f})")

# ============================================================
# Step 7: Algebraic identity for the cross term
# ============================================================
print("\n" + "=" * 70)
print("Step 7: Algebraic identity for combined cross term")
print("=" * 70)

# Combined cross: 2I - D^T - R_mu D R_nu^T
# = (I - D^T) + (I - R_mu D R_nu^T)
#
# Note: I - D^T = (I - U^T)(I - ...) ... complex
#
# Alternative: use the identity
# I - D^T = I - (R_mu^T U)^T = I - U^T R_mu = (I - U^T) + U^T(I - R_mu)
# Similarly: I - RDR = I - U R_nu^T = (I - U) + U(I - R_nu^T)
#   wait: RDR = R_mu D R_nu^T = U R_nu^T.
#   So I - RDR = I - U R_nu^T
#
# Combined: (I - D^T) + (I - RDR) = (I - U^T R_mu) + (I - U R_nu^T)
# = 2I - U^T R_mu - U R_nu^T

# Verify:
R_mu = special_ortho_group.rvs(3)
R_nu = special_ortho_group.rvs(3)
Dmn = special_ortho_group.rvs(3)
U = R_mu @ Dmn

lhs = (I3 - Dmn.T) + (I3 - R_mu @ Dmn @ R_nu.T)
rhs = 2*I3 - U.T @ R_mu - U @ R_nu.T
print(f"Identity check: (I-D^T) + (I-RDR) = 2I - U^T R_mu - U R_nu^T")
print(f"  Error: {np.linalg.norm(lhs - rhs):.2e}")

# D^T = D^{-1} = (R_mu^{-1} U)^{-1} = U^{-1} R_mu = U^T R_mu (since U in SO(3))
# So I - D^T = I - U^T R_mu ✓

# And RDR = U R_nu^T, so I - RDR = I - U R_nu^T ✓

# So combined cross = 2I - U^T R_mu - U R_nu^T

# Now can we write this in terms of (I-U) and (I-U^T)?
# 2I - U^T R_mu - U R_nu^T
# = (I - U^T R_mu) + (I - U R_nu^T)
# = (I - U^T)(R_mu) + U^T(I - R_mu) + (I-U)(R_nu^T) + U(I-R_nu^T)
# Hmm, this doesn't simplify nicely.

# Actually: U^T R_mu = D^T R_mu^T R_mu = D^T (since R in SO(3))
# Wait, U = R_mu D, so U^T = D^T R_mu^T, and U^T R_mu = D^T R_mu^T R_mu = D^T.
# Similarly U R_nu^T = R_mu D R_nu^T = RDR.
# So we're just back to D^T + RDR.

# Let me try a different decomposition. For the per-plaquette sum_S term:
# S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(2I - D^T - RDR)T_nu
#
# Use D^T = U^T R_mu and RDR = U W^T (since U W^T = R_mu D D^{-1} R_nu^T? No.)
# W = D R_nu^T, so U W^T = R_mu D (D R_nu^T)^T = R_mu D R_nu D^T. Not = RDR in general.

# Actually: RDR = R_mu D R_nu^T, and U = R_mu D, so RDR = U R_nu^T. Let me check:
check = np.allclose(R_mu @ Dmn @ R_nu.T, U @ R_nu.T)
print(f"RDR = U R_nu^T: {check}")

# And D^T = U^T R_mu:
check2 = np.allclose(Dmn.T, U.T @ R_mu)
print(f"D^T = U^T R_mu: {check2}")

# ============================================================
# Step 8: Per-plaquette sum_S as f-terms + structured cross
# ============================================================
print("\n" + "=" * 70)
print("Step 8: sum_S in terms of (I-U) and (I-W) vectors")
print("=" * 70)

# Let a = (I-U^T)T_mu, b = (I-W^T)T_nu.
# Then ||a||^2 = 2f(U,T_mu), ||b||^2 = 2f(W,T_nu).
#
# budget = ||a||^2 + ||b||^2
#
# Now the cross term T_mu^T(D^T + RDR)T_nu:
# T_mu^T D^T T_nu = T_mu^T U^T R_mu T_nu
# = (U T_mu)^T R_mu T_nu
# = (T_mu - (I-U)T_mu)^T R_mu T_nu
# = T_mu^T R_mu T_nu - ((I-U)T_mu)^T R_mu T_nu
#
# Hmm, this doesn't use a and b nicely. Let me try:
# a = (I-U^T)T_mu => T_mu = (I-U^T)^{-1} a (when invertible)
# Not helpful either.

# Let me try a DIFFERENT approach entirely.
# ============================================================
# Step 9: sum_S as a quadratic form — DIRECT DECOMPOSITION
# ============================================================
print("\n" + "=" * 70)
print("Step 9: Direct matrix decomposition of sum_S")
print("=" * 70)

# Build the sum_S matrix and try to decompose it as a sum of PSD terms.
# The 12x12 matrix has:
# Diagonal block (mu,mu): from budget terms 2(I-U_{mu,nu}) + 2(I-W_{nu,mu}) summed over partners
# Off-diagonal (mu,nu): -(2I - D^T - RDR) = D^T + RDR - 2I

# Let's build and analyze the off-diagonal structure.
R = [special_ortho_group.rvs(3) for _ in range(4)]
D = {}
for mu in range(4):
    for nu in range(mu+1, 4):
        D[(mu,nu)] = special_ortho_group.rvs(3)

# Off-diagonal block for sum_S: D^T + R_mu D R_nu^T - 2I
# This is the NEGATIVE of (2I - D^T - RDR)
for mu in range(4):
    for nu in range(mu+1, 4):
        off_diag = D[(mu,nu)].T + R[mu] @ D[(mu,nu)] @ R[nu].T - 2*I3
        eigs_od = np.linalg.eigvalsh((off_diag + off_diag.T)/2)
        print(f"Off-diag ({mu},{nu}): eigenvalues of symm part = [{eigs_od[0]:.3f}, {eigs_od[1]:.3f}, {eigs_od[2]:.3f}]")

# Note: D^T + RDR - 2I. When D=I and R=I: 2I - 2I = 0 (at Q=I).
# When D is large angle: off-diagonal has eigenvalues near -3 (max negative).

# ============================================================
# Step 10: Characteristic polynomial approach -- when is sum_S min eig = 0?
# ============================================================
print("\n" + "=" * 70)
print("Step 10: When is sum_S min eigenvalue = 0? (Characterize minimizer)")
print("=" * 70)

P = np.zeros((12, 9))
P[0:3, 0:3] = I3
P[3:6, 3:6] = I3
P[6:9, 6:9] = I3
P[9:12, 0:3] = -I3
P[9:12, 3:6] = -I3
P[9:12, 6:9] = -I3

def build_sumS_12(R, D_dict):
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            U = R[mu] @ Dmn
            W = Dmn @ R[nu].T
            RDR = R[mu] @ Dmn @ R[nu].T
            # Diagonal
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*(I3 - U)
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*(I3 - W)
            # Off-diagonal
            cross = Dmn.T + RDR - 2*I3
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    return (M + M.T) / 2

# Find the sum_S minimizer
def min_eig_sumS(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}
    idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu, nu)] = so3_from_vec(params[idx:idx+3])
            idx += 3
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T)/2
    return eigvalsh(M9)[0]

best = float('inf')
bestp = None
for _ in range(5000):
    p = np.random.randn(30) * np.pi
    v = min_eig_sumS(p)
    if v < best:
        best = v
        bestp = p.copy()

res = minimize(min_eig_sumS, bestp, method='Nelder-Mead',
               options={'maxiter': 100000, 'xatol': 1e-12, 'fatol': 1e-14})
print(f"sum_S min eigenvalue: {res.fun:.10f}")

# Extract config at minimizer
R_min = [so3_from_vec(res.x[3*i:3*(i+1)]) for i in range(4)]
D_min = {}
idx = 12
for mu in range(4):
    for nu in range(mu+1, 4):
        D_min[(mu,nu)] = so3_from_vec(res.x[idx:idx+3])
        idx += 3

print("\nAt sum_S minimizer:")
for mu in range(4):
    angle = np.arccos(np.clip((np.trace(R_min[mu])-1)/2, -1, 1))
    print(f"  R_{mu} angle: {np.degrees(angle):.2f}°")
for mu in range(4):
    for nu in range(mu+1, 4):
        angle = np.arccos(np.clip((np.trace(D_min[(mu,nu)])-1)/2, -1, 1))
        print(f"  D_{mu}{nu} angle: {np.degrees(angle):.2f}°")

M12_min = build_sumS_12(R_min, D_min)
M9_min = P.T @ M12_min @ P
M9_min = (M9_min + M9_min.T)/2
eigs_min = eigvalsh(M9_min)
print(f"Eigenvalues: {eigs_min}")
print(f"Multiplicity of ~0 eigenvalue: {sum(abs(e) < 0.01 for e in eigs_min)}")
