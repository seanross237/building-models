"""
Numerical verification of LEMMA_D and LEMMA_RDR.
Tests: overall bounds, per-plaquette bounds, eigenvalue structure.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh
import time

np.random.seed(42)

def random_SO3(n=1):
    """Generate n random SO(3) matrices."""
    return [special_ortho_group.rvs(3) for _ in range(n)]

def f(R, p):
    """f(R,p) = p^T (I - R) p for R in SO(3), p in R^3."""
    return p @ (np.eye(3) - R) @ p

def random_T_constrained():
    """Generate random T = (T_0, T_1, T_2, T_3) with sum = 0, each T_mu in R^3."""
    T = [np.random.randn(3) for _ in range(3)]
    T.append(-T[0] - T[1] - T[2])
    return T

def compute_lemma_D(T, R, D):
    """
    LEMMA_D = sum_{mu<nu} [f(R_mu D_{mu,nu}, T_mu) + f(D_{mu,nu} R_nu^T, T_nu)
                           - 2 T_mu^T (I - D_{mu,nu}^T) T_nu]
    R: list of 4 SO(3) matrices (R_0,...,R_3)
    D: dict (mu,nu) -> SO(3) for mu<nu
    """
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            term1 = f(R[mu] @ Dmn, T[mu])
            term2 = f(Dmn @ R[nu].T, T[nu])
            cross = 2.0 * T[mu] @ (np.eye(3) - Dmn.T) @ T[nu]
            val += term1 + term2 - cross
    return val

def compute_lemma_RDR(T, R, D):
    """
    LEMMA_RDR = sum_{mu<nu} [f(R_mu D_{mu,nu}, T_mu) + f(D_{mu,nu} R_nu^T, T_nu)
                              - 2 T_mu^T (I - R_mu D_{mu,nu} R_nu^T) T_nu]
    """
    val = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D[(mu, nu)]
            RDR = R[mu] @ Dmn @ R[nu].T
            term1 = f(R[mu] @ Dmn, T[mu])
            term2 = f(Dmn @ R[nu].T, T[nu])
            cross = 2.0 * T[mu] @ (np.eye(3) - RDR) @ T[nu]
            val += term1 + term2 - cross
    return val

def per_plaquette_D(T, R, D, mu, nu):
    """Per-plaquette LEMMA_D value for a single (mu,nu)."""
    Dmn = D[(mu, nu)]
    term1 = f(R[mu] @ Dmn, T[mu])
    term2 = f(Dmn @ R[nu].T, T[nu])
    cross = 2.0 * T[mu] @ (np.eye(3) - Dmn.T) @ T[nu]
    return term1 + term2 - cross

def norm_sq_T(T):
    return sum(t @ t for t in T)

def random_Q():
    """Generate random gauge config: R_mu (4 matrices), D_{mu,nu} (6 matrices)."""
    R = random_SO3(4)
    D = {}
    for mu in range(4):
        for nu in range(mu+1, 4):
            D[(mu, nu)] = random_SO3(1)[0]
    return R, D

# ============================================================
# TEST 1: Verify LEMMA_D and LEMMA_RDR over 1000 random configs
# ============================================================
print("=" * 70)
print("TEST 1: LEMMA_D and LEMMA_RDR verification (1000 configs x 50 T)")
print("=" * 70)

n_configs = 1000
n_T = 50
min_D = float('inf')
min_RDR = float('inf')
min_D_normalized = float('inf')
min_RDR_normalized = float('inf')
violations_D = 0
violations_RDR = 0

t0 = time.time()
for _ in range(n_configs):
    R, D_dict = random_Q()
    for __ in range(n_T):
        T = random_T_constrained()
        nsq = norm_sq_T(T)

        ld = compute_lemma_D(T, R, D_dict)
        lr = compute_lemma_RDR(T, R, D_dict)

        min_D = min(min_D, ld)
        min_RDR = min(min_RDR, lr)
        if nsq > 1e-10:
            min_D_normalized = min(min_D_normalized, ld / nsq)
            min_RDR_normalized = min(min_RDR_normalized, lr / nsq)

        if ld < -1e-10:
            violations_D += 1
        if lr < -1e-10:
            violations_RDR += 1

elapsed = time.time() - t0
print(f"Time: {elapsed:.1f}s")
print(f"LEMMA_D:   violations={violations_D}, min={min_D:.6f}, min/||T||^2={min_D_normalized:.6f}")
print(f"LEMMA_RDR: violations={violations_RDR}, min={min_RDR:.6f}, min/||T||^2={min_RDR_normalized:.6f}")

# ============================================================
# TEST 2: Per-plaquette test for LEMMA_D
# ============================================================
print("\n" + "=" * 70)
print("TEST 2: Per-plaquette LEMMA_D (does each plaquette >= 0?)")
print("=" * 70)

n_configs2 = 2000
n_T2 = 20
pp_violations = 0
pp_min = float('inf')

for _ in range(n_configs2):
    R, D_dict = random_Q()
    for __ in range(n_T2):
        T = random_T_constrained()
        for mu in range(4):
            for nu in range(mu+1, 4):
                val = per_plaquette_D(T, R, D_dict, mu, nu)
                pp_min = min(pp_min, val)
                if val < -1e-10:
                    pp_violations += 1

print(f"Per-plaquette violations: {pp_violations} / {n_configs2 * n_T2 * 6}")
print(f"Per-plaquette minimum: {pp_min:.6f}")

# ============================================================
# TEST 3: LEMMA_D without sum-to-zero constraint (should violate)
# ============================================================
print("\n" + "=" * 70)
print("TEST 3: LEMMA_D WITHOUT sum-to-zero constraint")
print("=" * 70)

violations_no_constraint = 0
n_test3 = 5000
for _ in range(n_test3):
    R, D_dict = random_Q()
    T = [np.random.randn(3) for _ in range(4)]  # No constraint!
    ld = compute_lemma_D(T, R, D_dict)
    if ld < -1e-10:
        violations_no_constraint += 1

print(f"Without constraint: {violations_no_constraint}/{n_test3} violations")

# ============================================================
# TEST 4: Eigenvalue structure of LEMMA_D as quadratic form
# ============================================================
print("\n" + "=" * 70)
print("TEST 4: Eigenvalue structure of LEMMA_D quadratic form")
print("=" * 70)

def lemma_D_matrix(R, D_dict):
    """
    Build 12x12 matrix M such that LEMMA_D = T_vec^T M T_vec
    where T_vec = (T_0, T_1, T_2, T_3) in R^12.
    Then project onto V = {sum T_mu = 0} (9D subspace) via constraint elimination.
    """
    M = np.zeros((12, 12))

    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            # f(R_mu D, T_mu) = T_mu^T (I - R_mu D) T_mu
            block_mm = np.eye(3) - R[mu] @ Dmn
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += block_mm

            # f(D R_nu^T, T_nu) = T_nu^T (I - D R_nu^T) T_nu
            block_nn = np.eye(3) - Dmn @ R[nu].T
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += block_nn

            # -2 T_mu^T (I - D^T) T_nu cross term
            cross_block = -(np.eye(3) - Dmn.T)
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross_block
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross_block.T

    # Now project onto constraint subspace sum T_mu = 0
    # Use T_3 = -T_0 - T_1 - T_2, so T_vec = P @ t where t = (T_0, T_1, T_2)
    P = np.zeros((12, 9))
    P[0:3, 0:3] = np.eye(3)
    P[3:6, 3:6] = np.eye(3)
    P[6:9, 6:9] = np.eye(3)
    P[9:12, 0:3] = -np.eye(3)
    P[9:12, 3:6] = -np.eye(3)
    P[9:12, 6:9] = -np.eye(3)

    M_proj = P.T @ M @ P
    return (M_proj + M_proj.T) / 2  # Symmetrize

def lemma_RDR_matrix(R, D_dict):
    """Build 9x9 projected matrix for LEMMA_RDR."""
    M = np.zeros((12, 12))

    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            RDR = R[mu] @ Dmn @ R[nu].T

            block_mm = np.eye(3) - R[mu] @ Dmn
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += block_mm

            block_nn = np.eye(3) - Dmn @ R[nu].T
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += block_nn

            cross_block = -(np.eye(3) - RDR)
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross_block
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross_block.T

    P = np.zeros((12, 9))
    P[0:3, 0:3] = np.eye(3)
    P[3:6, 3:6] = np.eye(3)
    P[6:9, 6:9] = np.eye(3)
    P[9:12, 0:3] = -np.eye(3)
    P[9:12, 3:6] = -np.eye(3)
    P[9:12, 6:9] = -np.eye(3)

    M_proj = P.T @ M @ P
    return (M_proj + M_proj.T) / 2

n_eig_tests = 500
min_eig_D = float('inf')
min_eig_RDR = float('inf')
eig_D_list = []
eig_RDR_list = []

for _ in range(n_eig_tests):
    R, D_dict = random_Q()

    M_D = lemma_D_matrix(R, D_dict)
    eigs_D = eigvalsh(M_D)
    min_eig_D = min(min_eig_D, eigs_D[0])
    eig_D_list.append(eigs_D)

    M_RDR = lemma_RDR_matrix(R, D_dict)
    eigs_RDR = eigvalsh(M_RDR)
    min_eig_RDR = min(min_eig_RDR, eigs_RDR[0])
    eig_RDR_list.append(eigs_RDR)

eig_D_arr = np.array(eig_D_list)
eig_RDR_arr = np.array(eig_RDR_list)

print(f"LEMMA_D min eigenvalue (over {n_eig_tests} configs): {min_eig_D:.6f}")
print(f"LEMMA_RDR min eigenvalue (over {n_eig_tests} configs): {min_eig_RDR:.6f}")
print(f"\nLEMMA_D eigenvalue statistics (9 eigenvalues, sorted):")
print(f"  Min per position:  {eig_D_arr.min(axis=0)}")
print(f"  Mean per position: {eig_D_arr.mean(axis=0)}")
print(f"\nLEMMA_RDR eigenvalue statistics:")
print(f"  Min per position:  {eig_RDR_arr.min(axis=0)}")
print(f"  Mean per position: {eig_RDR_arr.mean(axis=0)}")

# ============================================================
# TEST 5: Special case D = I (all D matrices = identity)
# ============================================================
print("\n" + "=" * 70)
print("TEST 5: D = I special case")
print("=" * 70)

n_D_I = 500
min_D_I = float('inf')
min_RDR_I = float('inf')

for _ in range(n_D_I):
    R = random_SO3(4)
    D_dict_I = {(mu, nu): np.eye(3) for mu in range(4) for nu in range(mu+1, 4)}

    for __ in range(20):
        T = random_T_constrained()
        nsq = norm_sq_T(T)

        ld = compute_lemma_D(T, R, D_dict_I)
        lr = compute_lemma_RDR(T, R, D_dict_I)
        if nsq > 1e-10:
            min_D_I = min(min_D_I, ld / nsq)
            min_RDR_I = min(min_RDR_I, lr / nsq)

print(f"LEMMA_D(D=I)   min/||T||^2 = {min_D_I:.6f}")
print(f"LEMMA_RDR(D=I) min/||T||^2 = {min_RDR_I:.6f}")

# At D=I, LEMMA_D and LEMMA_RDR differ only in cross term
# LEMMA_D cross: T_mu^T(I - D^T)T_nu = T_mu^T(I-I)T_nu = 0
# LEMMA_RDR cross: T_mu^T(I - R_mu R_nu^T)T_nu
# So LEMMA_D(D=I) = sum f(R_mu, T_mu) + sum f(R_nu^T, T_nu) = 2 sum f(R_mu, T_mu)
# which is >= 0 trivially.

# Verify this:
R = random_SO3(4)
D_dict_I = {(mu, nu): np.eye(3) for mu in range(4) for nu in range(mu+1, 4)}
T = random_T_constrained()

ld_DI = compute_lemma_D(T, R, D_dict_I)
manual_sum = sum(f(R[mu], T[mu]) for mu in range(4))
# Each mu appears in 3 plaquettes as either first or second index
# f(R_mu I, T_mu) = f(R_mu, T_mu) and f(I R_nu^T, T_nu) = f(R_nu^T, T_nu) = f(R_nu, T_nu) [since f(R^T,p) = f(R,p)]
manual_sum2 = 0
for mu in range(4):
    for nu in range(mu+1, 4):
        manual_sum2 += f(R[mu], T[mu]) + f(R[nu].T, T[nu])
print(f"\nD=I verification: LEMMA_D = {ld_DI:.8f}, manual sum = {manual_sum2:.8f}")

# ============================================================
# TEST 6: Cauchy-Schwarz per-plaquette bound test
# ============================================================
print("\n" + "=" * 70)
print("TEST 6: Per-plaquette CS bound: budget >= 2|cross|?")
print("=" * 70)

cs_per_plaq_fails = 0
cs_total_fails = 0
n_cs = 5000
for _ in range(n_cs):
    R, D_dict = random_Q()
    T = random_T_constrained()

    budget_total = 0
    cross_total = 0
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            budget = f(R[mu] @ Dmn, T[mu]) + f(Dmn @ R[nu].T, T[nu])
            cross = 2 * abs(T[mu] @ (np.eye(3) - Dmn.T) @ T[nu])
            budget_total += budget
            cross_total += cross
            if budget < cross - 1e-10:
                cs_per_plaq_fails += 1

    if budget_total < cross_total - 1e-10:
        cs_total_fails += 1

print(f"Per-plaquette budget >= 2|cross|: fails = {cs_per_plaq_fails} / {n_cs * 6}")
print(f"Total budget >= total |cross|: fails = {cs_total_fails} / {n_cs}")

# ============================================================
# TEST 7: Sum_S = LEMMA_D + LEMMA_RDR
# ============================================================
print("\n" + "=" * 70)
print("TEST 7: sum_S = LEMMA_D + LEMMA_RDR")
print("=" * 70)

min_sum_S = float('inf')
min_sum_S_norm = float('inf')
for _ in range(2000):
    R, D_dict = random_Q()
    for __ in range(25):
        T = random_T_constrained()
        nsq = norm_sq_T(T)
        ld = compute_lemma_D(T, R, D_dict)
        lr = compute_lemma_RDR(T, R, D_dict)
        sS = ld + lr
        min_sum_S = min(min_sum_S, sS)
        if nsq > 1e-10:
            min_sum_S_norm = min(min_sum_S_norm, sS / nsq)

print(f"sum_S minimum: {min_sum_S:.6f}")
print(f"sum_S / ||T||^2 minimum: {min_sum_S_norm:.6f}")
