"""
Find near-minimizers of LEMMA_D and understand their structure.
Also test Approach 3: constraint elimination algebra.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh
from scipy.optimize import minimize
import time

np.random.seed(42)

def random_SO3(n=1):
    return [special_ortho_group.rvs(3) for _ in range(n)]

def f(R, p):
    return p @ (np.eye(3) - R) @ p

def angle_of_SO3(R):
    """Rotation angle of SO(3) matrix."""
    cos_theta = (np.trace(R) - 1) / 2
    return np.arccos(np.clip(cos_theta, -1, 1))

def lemma_D_matrix_12(R, D_dict):
    """Build 12x12 matrix (before projection)."""
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            block_mm = np.eye(3) - R[mu] @ Dmn
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += block_mm
            block_nn = np.eye(3) - Dmn @ R[nu].T
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += block_nn
            cross_block = -(np.eye(3) - Dmn.T)
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross_block
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross_block.T
    return (M + M.T) / 2

def project_to_V(M12):
    """Project 12x12 to 9x9 on V = {sum T_mu = 0}."""
    P = np.zeros((12, 9))
    P[0:3, 0:3] = np.eye(3)
    P[3:6, 3:6] = np.eye(3)
    P[6:9, 6:9] = np.eye(3)
    P[9:12, 0:3] = -np.eye(3)
    P[9:12, 3:6] = -np.eye(3)
    P[9:12, 6:9] = -np.eye(3)
    M9 = P.T @ M12 @ P
    return (M9 + M9.T) / 2

# ============================================================
# Step 1: Find minimizer via gradient descent on SO(3)^10 parameters
# ============================================================
print("=" * 70)
print("Finding near-minimizers of LEMMA_D eigenvalue")
print("=" * 70)

def so3_from_vec(v):
    """Exponential map: R^3 -> SO(3)."""
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return np.eye(3)
    k = v / theta
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def min_eig_from_params(params):
    """Compute negative of min eigenvalue from 30-parameter vector."""
    # params: 4 R matrices (12 params) + 6 D matrices (18 params) = 30 total
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}
    idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu, nu)] = so3_from_vec(params[idx:idx+3])
            idx += 3

    M12 = lemma_D_matrix_12(R, D_dict)
    M9 = project_to_V(M12)
    return eigvalsh(M9)[0]

# Random search for low min-eigenvalue configs
best_min_eig = float('inf')
best_params = None
for trial in range(2000):
    params = np.random.randn(30) * np.pi
    me = min_eig_from_params(params)
    if me < best_min_eig:
        best_min_eig = me
        best_params = params.copy()

print(f"Random search best min eigenvalue: {best_min_eig:.6f}")

# Now optimize via Nelder-Mead to find actual minimizer
result = minimize(min_eig_from_params, best_params, method='Nelder-Mead',
                  options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
opt_min_eig = result.fun
opt_params = result.x
print(f"Optimized min eigenvalue: {opt_min_eig:.8f}")

# Extract the optimal R and D
R_opt = [so3_from_vec(opt_params[3*i:3*(i+1)]) for i in range(4)]
D_opt = {}
idx = 12
for mu in range(4):
    for nu in range(mu+1, 4):
        D_opt[(mu, nu)] = so3_from_vec(opt_params[idx:idx+3])
        idx += 3

print("\nOptimal R rotation angles:")
for mu in range(4):
    print(f"  R_{mu}: angle = {np.degrees(angle_of_SO3(R_opt[mu])):.2f}°")

print("\nOptimal D rotation angles:")
for mu in range(4):
    for nu in range(mu+1, 4):
        print(f"  D_{mu}{nu}: angle = {np.degrees(angle_of_SO3(D_opt[(mu,nu)])):.2f}°")

# Eigenstructure at optimum
M12_opt = lemma_D_matrix_12(R_opt, D_opt)
M9_opt = project_to_V(M12_opt)
eigs_opt, vecs_opt = eigh(M9_opt)
print(f"\nFull eigenvalues at optimizer: {eigs_opt}")
print(f"Min eigenvector (in T_0, T_1, T_2 coordinates):")
v = vecs_opt[:, 0]
print(f"  T_0 = [{v[0]:.4f}, {v[1]:.4f}, {v[2]:.4f}]")
print(f"  T_1 = [{v[3]:.4f}, {v[4]:.4f}, {v[5]:.4f}]")
print(f"  T_2 = [{v[6]:.4f}, {v[7]:.4f}, {v[8]:.4f}]")
T3 = -(v[0:3] + v[3:6] + v[6:9])
print(f"  T_3 = [{T3[0]:.4f}, {T3[1]:.4f}, {T3[2]:.4f}]")

# ============================================================
# Step 2: Check if minimizers have special structure (e.g. all D close to pi rotations)
# ============================================================
print("\n" + "=" * 70)
print("Near-minimizer structure analysis")
print("=" * 70)

# Run multiple optimizations from different starts
opt_results = []
for trial in range(20):
    params0 = np.random.randn(30) * np.pi
    # First find good start via random search
    best = float('inf')
    bestp = params0
    for _ in range(200):
        p = np.random.randn(30) * np.pi
        v = min_eig_from_params(p)
        if v < best:
            best = v
            bestp = p
    # Then optimize
    res = minimize(min_eig_from_params, bestp, method='Nelder-Mead',
                   options={'maxiter': 20000, 'xatol': 1e-8, 'fatol': 1e-10})
    opt_results.append((res.fun, res.x))
    if trial < 5 or res.fun < 0.05:
        R_t = [so3_from_vec(res.x[3*i:3*(i+1)]) for i in range(4)]
        D_t = {}
        idx = 12
        for mu in range(4):
            for nu in range(mu+1, 4):
                D_t[(mu, nu)] = so3_from_vec(res.x[idx:idx+3])
                idx += 3

        R_angles = [np.degrees(angle_of_SO3(R_t[mu])) for mu in range(4)]
        D_angles = [np.degrees(angle_of_SO3(D_t[k])) for k in D_t]
        print(f"Trial {trial}: min_eig = {res.fun:.6f}, R_angles = {[f'{a:.1f}' for a in R_angles]}, D_angles = {[f'{a:.1f}' for a in D_angles]}")

all_min_eigs = sorted([r[0] for r in opt_results])
print(f"\nAll min eigenvalues found: {[f'{x:.4f}' for x in all_min_eigs[:10]]}")
print(f"Global minimum found: {all_min_eigs[0]:.8f}")

# ============================================================
# Step 3: Approach 3 - Direct Constraint Manipulation
# ============================================================
print("\n" + "=" * 70)
print("Approach 3: Direct Constraint Algebra")
print("=" * 70)

# LEMMA_D = sum_{mu<nu} [f(R_mu D, T_mu) + f(D R_nu^T, T_nu) - 2 T_mu^T(I-D^T)T_nu]
#
# The cross term sum: sum_{mu<nu} T_mu^T(I-D_{mu,nu}^T) T_nu
# = sum_{mu<nu} T_mu^T T_nu - sum_{mu<nu} T_mu^T D_{mu,nu}^T T_nu
#
# Using sum T_mu = 0: sum_{mu<nu} T_mu^T T_nu = -||T||^2/2
#
# So cross term = -||T||^2/2 - sum_{mu<nu} T_mu^T D^T T_nu

# Let's verify this identity numerically
def verify_cross_identity():
    R, D_dict = random_SO3(4), {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = random_SO3(1)[0]
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0]-T[1]-T[2])

    cross_sum = sum(T[mu] @ (np.eye(3) - D_dict[(mu,nu)].T) @ T[nu]
                    for mu in range(4) for nu in range(mu+1, 4))
    nsq = sum(t@t for t in T)
    D_cross = sum(T[mu] @ D_dict[(mu,nu)].T @ T[nu]
                  for mu in range(4) for nu in range(mu+1, 4))

    print(f"cross_sum = {cross_sum:.8f}")
    print(f"-||T||^2/2 - D_cross = {-nsq/2 - D_cross:.8f}")
    print(f"Match: {abs(cross_sum - (-nsq/2 - D_cross)) < 1e-10}")

verify_cross_identity()

# So LEMMA_D = budget_terms - 2*(-||T||^2/2 - D_cross) = budget_terms + ||T||^2 + 2*D_cross
# where budget_terms = sum_{mu<nu} [f(R_mu D, T_mu) + f(D R_nu^T, T_nu)]
#       D_cross = sum_{mu<nu} T_mu^T D^T T_nu

# Verify this decomposition:
print("\nVerify LEMMA_D decomposition:")
R, D_dict = random_SO3(4), {}
for mu in range(4):
    for nu in range(mu+1, 4):
        D_dict[(mu,nu)] = random_SO3(1)[0]
T = [np.random.randn(3) for _ in range(3)]
T.append(-T[0]-T[1]-T[2])
nsq = sum(t@t for t in T)

budget = sum(f(R[mu] @ D_dict[(mu,nu)], T[mu]) + f(D_dict[(mu,nu)] @ R[nu].T, T[nu])
             for mu in range(4) for nu in range(mu+1, 4))
D_cross = sum(T[mu] @ D_dict[(mu,nu)].T @ T[nu]
              for mu in range(4) for nu in range(mu+1, 4))

lemma_D_direct = sum(
    f(R[mu] @ D_dict[(mu,nu)], T[mu]) + f(D_dict[(mu,nu)] @ R[nu].T, T[nu])
    - 2 * T[mu] @ (np.eye(3) - D_dict[(mu,nu)].T) @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
lemma_D_rewrite = budget + nsq + 2*D_cross

print(f"LEMMA_D direct = {lemma_D_direct:.8f}")
print(f"budget + ||T||^2 + 2*D_cross = {lemma_D_rewrite:.8f}")
print(f"Match: {abs(lemma_D_direct - lemma_D_rewrite) < 1e-10}")

# ============================================================
# Step 4: Decompose budget terms more carefully
# ============================================================
print("\n" + "=" * 70)
print("Budget term decomposition")
print("=" * 70)

# f(R_mu D, T_mu) = T_mu^T(I - R_mu D) T_mu = |T_mu|^2 - T_mu^T R_mu D T_mu
# Similarly f(D R_nu^T, T_nu) = |T_nu|^2 - T_nu^T D R_nu^T T_nu
#
# Sum of budget = sum_{mu<nu} [|T_mu|^2 + |T_nu|^2 - T_mu^T R_mu D T_mu - T_nu^T D R_nu^T T_nu]
# Each mu appears in 3 plaquettes. So sum of |T|^2 terms = 3*||T||^2
# Sum of R_mu D terms: for each (mu,nu), we get T_mu^T R_mu D_{mu,nu} T_mu and T_nu^T D_{mu,nu} R_nu^T T_nu

budget_decomp = 3*nsq - sum(
    T[mu] @ R[mu] @ D_dict[(mu,nu)] @ T[mu] + T[nu] @ D_dict[(mu,nu)] @ R[nu].T @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
print(f"Budget from formula: {budget:.8f}")
print(f"3||T||^2 - rotation terms: {budget_decomp:.8f}")
print(f"Match: {abs(budget - budget_decomp) < 1e-10}")

# So LEMMA_D = 3||T||^2 - rot_terms + ||T||^2 + 2*D_cross
#            = 4||T||^2 - rot_terms + 2*D_cross
# where rot_terms = sum_{mu<nu} [T_mu^T R_mu D T_mu + T_nu^T D R_nu^T T_nu]
# and D_cross = sum_{mu<nu} T_mu^T D^T T_nu

rot_terms = sum(
    T[mu] @ R[mu] @ D_dict[(mu,nu)] @ T[mu] + T[nu] @ D_dict[(mu,nu)] @ R[nu].T @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
lemma_D_v2 = 4*nsq - rot_terms + 2*D_cross
print(f"\nLEMMA_D = 4||T||^2 - rot_terms + 2*D_cross")
print(f"= {4*nsq:.4f} - {rot_terms:.4f} + {2*D_cross:.4f} = {lemma_D_v2:.4f}")
print(f"Direct: {lemma_D_direct:.4f}")
print(f"Match: {abs(lemma_D_v2 - lemma_D_direct) < 1e-10}")

# ============================================================
# Step 5: Separate R-dependent and D-dependent parts
# ============================================================
print("\n" + "=" * 70)
print("R-dependence analysis")
print("=" * 70)

# rot_terms = sum_{mu<nu} T_mu^T R_mu D T_mu + T_nu^T D R_nu^T T_nu
# The T_mu^T R_mu D T_mu term: for fixed D, this is a quadratic form in T_mu
# Note T_mu^T R_mu D T_mu = T_mu^T S(R_mu, D) T_mu where S = (R_mu D + D^T R_mu^T)/2
#
# For fixed mu, the term T_mu^T R_mu D T_mu summed over all nu > mu (3 terms) gives
# sum_{nu > mu} T_mu^T R_mu D_{mu,nu} T_mu
# Plus for nu < mu: T_mu appears as the second index in (nu,mu), giving
# T_mu^T D_{nu,mu} R_mu^T T_mu
#
# Wait, let me be more careful. Each (mu,nu) contributes T_mu^T R_mu D_{mu,nu} T_mu.
# So the sum over all (mu,nu) with mu<nu of T_mu^T R_mu D T_mu gives,
# for each mu, three terms: sum_{nu: nu>mu} T_mu^T R_mu D_{mu,nu} T_mu
# Similarly the T_nu^T D R_nu^T T_nu term: for each nu, sum_{mu: mu<nu} T_nu^T D_{mu,nu} R_nu^T T_nu

# So rot_terms = sum_mu [sum_{nu > mu} T_mu^T R_mu D_{mu,nu} T_mu + sum_{nu < mu} T_mu^T D_{nu,mu} R_mu^T T_mu]
# Can be written per-mu if needed.

# Let's check: at R_mu = I for all mu:
R_I = [np.eye(3) for _ in range(4)]
budget_RI = sum(f(D_dict[(mu,nu)], T[mu]) + f(D_dict[(mu,nu)], T[nu])
                for mu in range(4) for nu in range(mu+1, 4))
lemma_D_RI = sum(
    f(D_dict[(mu,nu)], T[mu]) + f(D_dict[(mu,nu)], T[nu])
    - 2 * T[mu] @ (np.eye(3) - D_dict[(mu,nu)].T) @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
print(f"LEMMA_D at R=I: {lemma_D_RI:.6f}")

# At R=I, the budget f(D,T_mu) + f(D,T_nu) already contains rotation info from D.
# The cross term is still T_mu^T(I-D^T)T_nu.

# ============================================================
# Step 6: Can we write LEMMA_D in terms of ||(I-D)T||^2 type terms?
# ============================================================
print("\n" + "=" * 70)
print("LEMMA_D in terms of ||(I-M)T||^2 norms")
print("=" * 70)

# Key identity: f(M,p) = p^T(I-M)p and ||(I-M)p||^2 = p^T(I-M)^T(I-M)p = 2f(M,p) for M in SO(3)
# because (I-M)^T(I-M) = I - M - M^T + I = 2I - M - M^T = 2(I - (M+M^T)/2)
# and f(M,p) = p^T(I-M)p = p^T p - p^T M p, while p^T(I-(M+M^T)/2)p = p^T p - p^T(M+M^T)/2 p
# These are NOT equal unless M is symmetric. So ||(I-M)p||^2 = 2f_sym(M,p) where f_sym uses (M+M^T)/2.
# Actually (I-M)^T(I-M) = 2I - M - M^T, and f(M,p) = p^T(I-M)p. So
# ||(I-M)p||^2 = 2|p|^2 - p^T(M+M^T)p = 2(|p|^2 - p^T[(M+M^T)/2]p)
# f(M,p) = |p|^2 - p^T M p
# So ||(I-M)p||^2 = 2f_sym(M,p) where f_sym(M,p) = p^T(I - (M+M^T)/2)p

# Let's verify: ||(I-M^T)p||^2 = 2f(M,p)? NO.
# ||(I-M^T)p||^2 = p^T(I-M)(I-M^T)p = p^T(2I - M - M^T)p = 2|p|^2 - p^T(M+M^T)p
# f(M,p) = |p|^2 - p^T M p
# So ||(I-M^T)p||^2 = 2f(M,p) iff |p|^2 - p^T M^T p = f(M,p) iff p^T M^T p = p^T M p
# which is true since p^T M^T p = (p^T M p)^T = p^T M p (scalar). YES!

# So ||(I-M^T)p||^2 = 2f(M,p). Let me verify:
M_test = random_SO3(1)[0]
p_test = np.random.randn(3)
norm_sq = np.linalg.norm((np.eye(3) - M_test.T) @ p_test)**2
f_val = f(M_test, p_test)
print(f"||(I-M^T)p||^2 = {norm_sq:.8f}, 2f(M,p) = {2*f_val:.8f}, match: {abs(norm_sq - 2*f_val) < 1e-10}")

# Good. So the budget terms:
# f(R_mu D, T_mu) = ||(I - D^T R_mu^T)T_mu||^2 / 2
# f(D R_nu^T, T_nu) = ||(I - R_nu D^T)T_nu||^2 / 2

# And the cross term uses T_mu^T(I-D^T)T_nu.
# By CS: |T_mu^T(I-D^T)T_nu| <= ||(I-D)T_mu|| * ||T_nu||   [standard CS]
#       also <= ||(I-D^T)^T T_mu|| * ||T_nu|| = ||(I-D)T_mu|| * ||T_nu||   hmm same thing

# But we have ||(I-D)T_mu||^2 = p^T(I-D)^T(I-D)p = 2f(D,p) (using the identity above...wait)
# ||(I-D)T_mu||^2 = T_mu^T(I-D)^T(I-D)T_mu = T_mu^T(2I - D - D^T)T_mu
# f(D,T_mu) = T_mu^T(I-D)T_mu

# And ||(I-D^T)T_mu||^2 = T_mu^T(I-D)(I-D^T)T_mu = T_mu^T(2I - D - D^T)T_mu = same!
# So ||(I-D)p||^2 = ||(I-D^T)p||^2 = 2f(D,p). Confirmed.

# ============================================================
# Step 7: Write LEMMA_D in matrix block form and analyze PSD structure
# ============================================================
print("\n" + "=" * 70)
print("Matrix block structure of LEMMA_D")
print("=" * 70)

# LEMMA_D 12x12 matrix has blocks M_{mu,mu} (diagonal) and M_{mu,nu} (off-diagonal)
# M_{mu,mu} = sum_{nu: nu partners mu} (I - R_mu D_{mu,nu})  [from budget terms]
# Wait, more carefully:

# For diagonal block (mu,mu):
# From budget: sum over nu paired with mu of (I - R_mu D_{mu,nu}) when mu < nu
#              + sum over nu paired with mu of (I - D_{nu,mu} R_mu^T) when nu < mu
# Cross terms don't contribute to diagonal.
# So M_{mu,mu} = sum_{nu > mu} (I - R_mu D_{mu,nu}) + sum_{nu < mu} (I - D_{nu,mu} R_mu^T)

# For off-diagonal (mu,nu) with mu < nu:
# From cross: -(I - D_{mu,nu}^T)
# So M_{mu,nu} = -(I - D_{mu,nu}^T) = D_{mu,nu}^T - I

# Verify this block structure:
M12 = lemma_D_matrix_12(R, D_dict)

# Check (0,1) block
block_01 = M12[0:3, 3:6]
expected_01 = D_dict[(0,1)].T - np.eye(3)
print(f"Block (0,1) match: {np.allclose(block_01, expected_01)}")

# Check (0,0) block
block_00 = M12[0:3, 0:3]
expected_00 = sum(np.eye(3) - R[0] @ D_dict[(0,nu)] for nu in range(1,4))
print(f"Block (0,0) match: {np.allclose(block_00, expected_00)}")

# Check (1,1) block
block_11 = M12[3:6, 3:6]
expected_11 = (np.eye(3) - D_dict[(0,1)] @ R[1].T) + sum(np.eye(3) - R[1] @ D_dict[(1,nu)] for nu in range(2,4))
print(f"Block (1,1) match: {np.allclose(block_11, expected_11)}")

# Check (3,3) block
block_33 = M12[9:12, 9:12]
expected_33 = sum(np.eye(3) - D_dict[(nu,3)] @ R[3].T for nu in range(3))
print(f"Block (3,3) match: {np.allclose(block_33, expected_33)}")

print("\nKey insight: off-diagonal blocks M_{mu,nu} = D_{mu,nu}^T - I")
print("These are INDEPENDENT of R! Only diagonal blocks depend on R.")

# ============================================================
# Step 8: What if we set R = I? Then LEMMA_D simplifies
# ============================================================
print("\n" + "=" * 70)
print("LEMMA_D at R = I: simplified form")
print("=" * 70)

# At R = I: M_{mu,mu} = sum_{nu partners} (I - D_{mu,nu})  [where D_{mu,nu} or D_{nu,mu}^T]
# Wait at R=I:
# From budget: f(I*D,T_mu) + f(D*I,T_nu) = f(D,T_mu) + f(D,T_nu)
# So M_{mu,mu} = sum of (I-D) or (I-D) depending on direction.
# For mu < nu: contribution I - D_{mu,nu} to block (mu,mu) and I - D_{mu,nu} to block (nu,nu)
# Cross term: -(I - D_{mu,nu}^T)

# So at R=I, diagonal block (mu,mu) = sum_{nu: nu>mu} (I-D_{mu,nu}) + sum_{nu: nu<mu} (I-D_{nu,mu})
# Off-diagonal (mu,nu) = D_{mu,nu}^T - I

# This is a cleaner form. Let's check if LEMMA_D(R=I) is PSD.
R_I = [np.eye(3) for _ in range(4)]
M12_I = lemma_D_matrix_12(R_I, D_dict)
M9_I = project_to_V(M12_I)
eigs_I = eigvalsh(M9_I)
print(f"LEMMA_D(R=I) eigenvalues: {eigs_I}")

# Now try to find minimizer with R=I
best_RI = float('inf')
best_RI_params = None
for _ in range(5000):
    D_params = np.random.randn(18) * np.pi
    D_dict_t = {}
    idx = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict_t[(mu,nu)] = so3_from_vec(D_params[idx:idx+3])
            idx += 3
    M12_t = lemma_D_matrix_12(R_I, D_dict_t)
    M9_t = project_to_V(M12_t)
    me = eigvalsh(M9_t)[0]
    if me < best_RI:
        best_RI = me
        best_RI_params = D_params.copy()

def min_eig_RI(params):
    D_dict_t = {}
    idx = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict_t[(mu,nu)] = so3_from_vec(params[idx:idx+3])
            idx += 3
    M12_t = lemma_D_matrix_12(R_I, D_dict_t)
    M9_t = project_to_V(M12_t)
    return eigvalsh(M9_t)[0]

result_RI = minimize(min_eig_RI, best_RI_params, method='Nelder-Mead',
                     options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"\nLEMMA_D(R=I) minimized eigenvalue: {result_RI.fun:.8f}")

# Extract optimal D angles
D_opt_RI = {}
idx = 0
for mu in range(4):
    for nu in range(mu+1, 4):
        D_opt_RI[(mu,nu)] = so3_from_vec(result_RI.x[idx:idx+3])
        idx += 3
        print(f"  D_{mu}{nu} angle: {np.degrees(angle_of_SO3(D_opt_RI[(mu,nu)])):.2f}°")
