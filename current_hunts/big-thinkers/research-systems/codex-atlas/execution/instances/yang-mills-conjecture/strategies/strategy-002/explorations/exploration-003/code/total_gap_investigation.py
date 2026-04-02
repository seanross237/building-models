"""
Investigate: Even though LEMMA_D alone can be negative,
does sum_S = LEMMA_D + LEMMA_RDR remain >= 0?
Does the total gap remain >= 0?
And: optimize directly to find minimum of each.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh
from scipy.optimize import minimize
import time

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

def compute_lemma_D(T, R, D):
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            val += f(R[mu] @ Dmn, T[mu]) + f(Dmn @ R[nu].T, T[nu])
            val -= 2.0 * T[mu] @ (np.eye(3) - Dmn.T) @ T[nu]
    return val

def compute_lemma_RDR(T, R, D):
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            RDR = R[mu] @ Dmn @ R[nu].T
            val += f(R[mu] @ Dmn, T[mu]) + f(Dmn @ R[nu].T, T[nu])
            val -= 2.0 * T[mu] @ (np.eye(3) - RDR) @ T[nu]
    return val

def build_matrix_12(R, D_dict, mode='D'):
    """Build 12x12 matrix for LEMMA_D or LEMMA_RDR."""
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            block_mm = np.eye(3) - R[mu] @ Dmn
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += block_mm
            block_nn = np.eye(3) - Dmn @ R[nu].T
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += block_nn

            if mode == 'D':
                cross_block = -(np.eye(3) - Dmn.T)
            else:  # RDR
                cross_block = -(np.eye(3) - R[mu] @ Dmn @ R[nu].T)
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross_block
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross_block.T
    return (M + M.T) / 2

def build_sumS_matrix_12(R, D_dict):
    """Build 12x12 matrix for sum_S = LEMMA_D + LEMMA_RDR."""
    return build_matrix_12(R, D_dict, 'D') + build_matrix_12(R, D_dict, 'RDR')

def build_total_gap_matrix_12(R, D_dict):
    """Build 12x12 matrix for total_gap = 2*sum f(R_mu, T_mu) + sum_S."""
    M = build_sumS_matrix_12(R, D_dict)
    # Add 2*sum_mu f(R_mu, T_mu) = 2 * sum_mu T_mu^T (I - R_mu) T_mu
    for mu in range(4):
        M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2 * (np.eye(3) - R[mu])
    return (M + M.T) / 2

P = np.zeros((12, 9))
P[0:3, 0:3] = np.eye(3)
P[3:6, 3:6] = np.eye(3)
P[6:9, 6:9] = np.eye(3)
P[9:12, 0:3] = -np.eye(3)
P[9:12, 3:6] = -np.eye(3)
P[9:12, 6:9] = -np.eye(3)

def project(M12):
    M9 = P.T @ M12 @ P
    return (M9 + M9.T) / 2

def params_to_config(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}
    idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu, nu)] = so3_from_vec(params[idx:idx+3])
            idx += 3
    return R, D_dict

# ============================================================
# TEST 1: sum_S adversarial optimization
# ============================================================
print("=" * 70)
print("Adversarial optimization: sum_S = LEMMA_D + LEMMA_RDR")
print("=" * 70)

def min_eig_sumS(params):
    R, D_dict = params_to_config(params)
    M12 = build_sumS_matrix_12(R, D_dict)
    M9 = project(M12)
    return eigvalsh(M9)[0]

best_sumS = float('inf')
best_sumS_params = None
for _ in range(5000):
    p = np.random.randn(30) * np.pi
    v = min_eig_sumS(p)
    if v < best_sumS:
        best_sumS = v
        best_sumS_params = p.copy()

print(f"Random search: min eig(sum_S) = {best_sumS:.6f}")

result_sumS = minimize(min_eig_sumS, best_sumS_params, method='Nelder-Mead',
                       options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Optimized: min eig(sum_S) = {result_sumS.fun:.8f}")

# ============================================================
# TEST 2: total_gap adversarial optimization
# ============================================================
print("\n" + "=" * 70)
print("Adversarial optimization: total_gap = 2*sum_f(R,T) + sum_S")
print("=" * 70)

def min_eig_total(params):
    R, D_dict = params_to_config(params)
    M12 = build_total_gap_matrix_12(R, D_dict)
    M9 = project(M12)
    return eigvalsh(M9)[0]

best_total = float('inf')
best_total_params = None
for _ in range(5000):
    p = np.random.randn(30) * np.pi
    v = min_eig_total(p)
    if v < best_total:
        best_total = v
        best_total_params = p.copy()

print(f"Random search: min eig(total_gap) = {best_total:.6f}")

result_total = minimize(min_eig_total, best_total_params, method='Nelder-Mead',
                        options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Optimized: min eig(total_gap) = {result_total.fun:.8f}")

# ============================================================
# TEST 3: LEMMA_RDR adversarial optimization
# ============================================================
print("\n" + "=" * 70)
print("Adversarial optimization: LEMMA_RDR")
print("=" * 70)

def min_eig_RDR(params):
    R, D_dict = params_to_config(params)
    M12 = build_matrix_12(R, D_dict, 'RDR')
    M9 = project(M12)
    return eigvalsh(M9)[0]

best_RDR = float('inf')
best_RDR_params = None
for _ in range(5000):
    p = np.random.randn(30) * np.pi
    v = min_eig_RDR(p)
    if v < best_RDR:
        best_RDR = v
        best_RDR_params = p.copy()

print(f"Random search: min eig(LEMMA_RDR) = {best_RDR:.6f}")

result_RDR = minimize(min_eig_RDR, best_RDR_params, method='Nelder-Mead',
                      options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Optimized: min eig(LEMMA_RDR) = {result_RDR.fun:.8f}")

# ============================================================
# TEST 4: At the LEMMA_D counterexample, check sum_S and total_gap
# ============================================================
print("\n" + "=" * 70)
print("At LEMMA_D counterexample: check sum_S and total_gap")
print("=" * 70)

def min_eig_D(params):
    R, D_dict = params_to_config(params)
    M12 = build_matrix_12(R, D_dict, 'D')
    M9 = project(M12)
    return eigvalsh(M9)[0]

# Find the LEMMA_D counterexample again
best_D = float('inf')
best_D_params = None
for _ in range(3000):
    p = np.random.randn(30) * np.pi
    v = min_eig_D(p)
    if v < best_D:
        best_D = v
        best_D_params = p.copy()

result_D = minimize(min_eig_D, best_D_params, method='Nelder-Mead',
                    options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"LEMMA_D min eig: {result_D.fun:.8f}")

# At this config, compute sum_S and total_gap
R_ce, D_ce = params_to_config(result_D.x)

M_D = project(build_matrix_12(R_ce, D_ce, 'D'))
M_RDR = project(build_matrix_12(R_ce, D_ce, 'RDR'))
M_sumS = project(build_sumS_matrix_12(R_ce, D_ce))
M_total = project(build_total_gap_matrix_12(R_ce, D_ce))

print(f"At LEMMA_D counterexample:")
print(f"  min eig(LEMMA_D) = {eigvalsh(M_D)[0]:.6f}")
print(f"  min eig(LEMMA_RDR) = {eigvalsh(M_RDR)[0]:.6f}")
print(f"  min eig(sum_S) = {eigvalsh(M_sumS)[0]:.6f}")
print(f"  min eig(total_gap) = {eigvalsh(M_total)[0]:.6f}")
print(f"  All eigs(sum_S): {eigvalsh(M_sumS)}")

# ============================================================
# TEST 5: Deeper search for sum_S violation
# ============================================================
print("\n" + "=" * 70)
print("Deeper adversarial search for sum_S violation")
print("=" * 70)

# Use multiple restarts with better search
best_sumS_deep = float('inf')
best_sumS_deep_params = None
t0 = time.time()

for trial in range(50):
    # Start from random
    p0 = np.random.randn(30) * np.pi
    # Quick local search
    res = minimize(min_eig_sumS, p0, method='Nelder-Mead',
                   options={'maxiter': 10000, 'xatol': 1e-8, 'fatol': 1e-10})
    if res.fun < best_sumS_deep:
        best_sumS_deep = res.fun
        best_sumS_deep_params = res.x.copy()

# Refine the best
res_deep = minimize(min_eig_sumS, best_sumS_deep_params, method='Nelder-Mead',
                    options={'maxiter': 100000, 'xatol': 1e-12, 'fatol': 1e-14})
print(f"Deep search (50 restarts): min eig(sum_S) = {res_deep.fun:.8f}")
print(f"Time: {time.time()-t0:.1f}s")

# Also try starting from the LEMMA_D counterexample
res_from_D = minimize(min_eig_sumS, result_D.x, method='Nelder-Mead',
                      options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"From LEMMA_D counterexample: min eig(sum_S) = {res_from_D.fun:.8f}")

# ============================================================
# TEST 6: Deeper search for total_gap violation
# ============================================================
print("\n" + "=" * 70)
print("Deeper adversarial search for total_gap violation")
print("=" * 70)

best_total_deep = float('inf')
best_total_deep_params = None

for trial in range(50):
    p0 = np.random.randn(30) * np.pi
    res = minimize(min_eig_total, p0, method='Nelder-Mead',
                   options={'maxiter': 10000, 'xatol': 1e-8, 'fatol': 1e-10})
    if res.fun < best_total_deep:
        best_total_deep = res.fun
        best_total_deep_params = res.x.copy()

res_deep_total = minimize(min_eig_total, best_total_deep_params, method='Nelder-Mead',
                          options={'maxiter': 100000, 'xatol': 1e-12, 'fatol': 1e-14})
print(f"Deep search (50 restarts): min eig(total_gap) = {res_deep_total.fun:.8f}")

# ============================================================
# TEST 7: Characterize the relationship between LEMMA_D and LEMMA_RDR
# ============================================================
print("\n" + "=" * 70)
print("Correlation between LEMMA_D and LEMMA_RDR min eigenvalues")
print("=" * 70)

D_eigs = []
RDR_eigs = []
for _ in range(500):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = special_ortho_group.rvs(3)

    M_D = project(build_matrix_12(R, D_dict, 'D'))
    M_RDR = project(build_matrix_12(R, D_dict, 'RDR'))
    D_eigs.append(eigvalsh(M_D)[0])
    RDR_eigs.append(eigvalsh(M_RDR)[0])

D_eigs = np.array(D_eigs)
RDR_eigs = np.array(RDR_eigs)
corr = np.corrcoef(D_eigs, RDR_eigs)[0,1]
print(f"Correlation between min eigenvalues: {corr:.4f}")
print(f"min LEMMA_D eigenvalue (random): {D_eigs.min():.6f}")
print(f"min LEMMA_RDR eigenvalue (random): {RDR_eigs.min():.6f}")
print(f"min(D + RDR) eigenvalue (random): {(D_eigs + RDR_eigs).min():.6f}")
