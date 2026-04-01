"""
Verify: is there really a negative eigenvalue for LEMMA_D's projected matrix?
If so, LEMMA_D is FALSE and we need to rethink.
If not, find the bug.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh

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

def compute_lemma_D_direct(T, R, D):
    """Direct computation of LEMMA_D."""
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            term1 = f(R[mu] @ Dmn, T[mu])
            term2 = f(Dmn @ R[nu].T, T[nu])
            cross = 2.0 * T[mu] @ (np.eye(3) - Dmn.T) @ T[nu]
            val += term1 + term2 - cross
    return val

def lemma_D_matrix_12(R, D_dict):
    """Build 12x12 matrix M for quadratic form T^T M T."""
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            # f(R_mu D, T_mu): diagonal block for mu
            block_mm = np.eye(3) - R[mu] @ Dmn
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += block_mm

            # f(D R_nu^T, T_nu): diagonal block for nu
            block_nn = np.eye(3) - Dmn @ R[nu].T
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += block_nn

            # -2 T_mu^T (I - D^T) T_nu: off-diagonal blocks
            # The factor of 2 in the expression: in quadratic form T^T M T,
            # cross contribution is T_mu^T M_{mu,nu} T_nu + T_nu^T M_{nu,mu} T_mu
            # = T_mu^T [M_{mu,nu} + M_{nu,mu}^T] T_nu
            # We want this to equal -2 T_mu^T (I - D^T) T_nu
            # So M_{mu,nu} + M_{nu,mu}^T = -2(I - D^T)
            # Setting M_{mu,nu} = -(I - D^T) and M_{nu,mu} = -(I - D) works.
            cross_block = -(np.eye(3) - Dmn.T)
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross_block
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross_block.T
    return (M + M.T) / 2

def project_to_V(M12):
    """Project to V = {sum T_mu = 0} using T_3 = -T_0 - T_1 - T_2."""
    P = np.zeros((12, 9))
    P[0:3, 0:3] = np.eye(3)
    P[3:6, 3:6] = np.eye(3)
    P[6:9, 6:9] = np.eye(3)
    P[9:12, 0:3] = -np.eye(3)
    P[9:12, 3:6] = -np.eye(3)
    P[9:12, 6:9] = -np.eye(3)
    M9 = P.T @ M12 @ P
    return (M9 + M9.T) / 2

# Reconstruct the optimizer's best config from minimizer_analysis
# Use the same random seed and re-run to find it
from scipy.optimize import minimize

def min_eig_from_params(params):
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

# Search for low eigenvalue config
np.random.seed(42)
best_min_eig = float('inf')
best_params = None
for trial in range(2000):
    params = np.random.randn(30) * np.pi
    me = min_eig_from_params(params)
    if me < best_min_eig:
        best_min_eig = me
        best_params = params.copy()

print(f"Random search: min eig = {best_min_eig:.6f}")

result = minimize(min_eig_from_params, best_params, method='Nelder-Mead',
                  options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
opt_params = result.x
print(f"Optimized: min eig = {result.fun:.8f}")

# Extract config
R_opt = [so3_from_vec(opt_params[3*i:3*(i+1)]) for i in range(4)]
D_opt = {}
idx = 12
for mu in range(4):
    for nu in range(mu+1, 4):
        D_opt[(mu, nu)] = so3_from_vec(opt_params[idx:idx+3])
        idx += 3

# Get the min eigenvector
M12 = lemma_D_matrix_12(R_opt, D_opt)
M9 = project_to_V(M12)
eigs, vecs = eigh(M9)
print(f"Eigenvalues: {eigs}")

# The min eigenvector in 9D = (T_0, T_1, T_2)
v = vecs[:, 0]
T_from_matrix = [v[0:3], v[3:6], v[6:9]]
T_from_matrix.append(-v[0:3] - v[3:6] - v[6:9])

# Compute LEMMA_D directly with this T
ld_direct = compute_lemma_D_direct(T_from_matrix, R_opt, D_opt)
ld_matrix = v @ M9 @ v

print(f"\nCRITICAL VERIFICATION:")
print(f"LEMMA_D via direct formula: {ld_direct:.10f}")
print(f"LEMMA_D via matrix: {ld_matrix:.10f}")
print(f"||T||^2 = {sum(t@t for t in T_from_matrix):.6f}")
print(f"||v||^2 = {v@v:.6f}")

# Double-check each term of LEMMA_D
print(f"\nPer-plaquette breakdown:")
for mu in range(4):
    for nu in range(mu+1, 4):
        Dmn = D_opt[(mu, nu)]
        T = T_from_matrix
        t1 = f(R_opt[mu] @ Dmn, T[mu])
        t2 = f(Dmn @ R_opt[nu].T, T[nu])
        cross = 2.0 * T[mu] @ (np.eye(3) - Dmn.T) @ T[nu]
        print(f"  ({mu},{nu}): f1={t1:.6f}, f2={t2:.6f}, cross={cross:.6f}, net={t1+t2-cross:.6f}")

# ============================================================
# CROSS CHECK: Verify the matrix formula is correct
# ============================================================
print("\n" + "=" * 70)
print("Cross-check: matrix vs direct computation for 100 random configs")
print("=" * 70)

max_discrepancy = 0
for _ in range(100):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)

    M12 = lemma_D_matrix_12(R, D_dict)
    M9 = project_to_V(M12)

    for _ in range(10):
        t = np.random.randn(9)
        T = [t[0:3], t[3:6], t[6:9]]
        T.append(-t[0:3] - t[3:6] - t[6:9])

        ld_direct = compute_lemma_D_direct(T, R, D_dict)
        ld_matrix = t @ M9 @ t

        disc = abs(ld_direct - ld_matrix)
        max_discrepancy = max(max_discrepancy, disc)

print(f"Max discrepancy between matrix and direct: {max_discrepancy:.2e}")

# ============================================================
# If matrix is correct and eigenvalue is negative, LEMMA_D is FALSE!
# Check if it's a numerical artifact by verifying with higher precision
# ============================================================
print("\n" + "=" * 70)
print("High-precision check at optimal config")
print("=" * 70)

# Verify R and D are actually SO(3)
for mu in range(4):
    R = R_opt[mu]
    print(f"R_{mu}: det={np.linalg.det(R):.10f}, ||R^T R - I|| = {np.linalg.norm(R.T@R - np.eye(3)):.2e}")
for mu in range(4):
    for nu in range(mu+1, 4):
        D = D_opt[(mu,nu)]
        print(f"D_{mu}{nu}: det={np.linalg.det(D):.10f}, ||D^T D - I|| = {np.linalg.norm(D.T@D - np.eye(3)):.2e}")

# Verify f >= 0 for each term
print("\nBudget terms (all should be >= 0):")
T = T_from_matrix
for mu in range(4):
    for nu in range(mu+1, 4):
        Dmn = D_opt[(mu, nu)]
        print(f"  f(R_{mu}D_{mu}{nu}, T_{mu}) = {f(R_opt[mu]@Dmn, T[mu]):.8f}")
        print(f"  f(D_{mu}{nu}R_{nu}^T, T_{nu}) = {f(Dmn@R_opt[nu].T, T[nu]):.8f}")

# Finally, check constraint
print(f"\nsum T_mu = {T[0] + T[1] + T[2] + T[3]}")
