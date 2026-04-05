"""
Characterize the zero-set of sum_S: when does sum_S = 0?
Understanding this is key to finding the proof.
"""
import numpy as np
from scipy.stats import special_ortho_group
from scipy.linalg import eigvalsh, eigh, expm
from scipy.optimize import minimize

np.random.seed(42)
I3 = np.eye(3)

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

def build_sumS_12(R, D_dict):
    M = np.zeros((12, 12))
    for mu in range(4):
        for nu in range(mu+1, 4):
            Dmn = D_dict[(mu, nu)]
            U = R[mu] @ Dmn
            W = Dmn @ R[nu].T
            RDR = R[mu] @ Dmn @ R[nu].T
            M[3*mu:3*mu+3, 3*mu:3*mu+3] += 2*(I3 - U)
            M[3*nu:3*nu+3, 3*nu:3*nu+3] += 2*(I3 - W)
            cross = Dmn.T + RDR - 2*I3
            M[3*mu:3*mu+3, 3*nu:3*nu+3] += cross
            M[3*nu:3*nu+3, 3*mu:3*mu+3] += cross.T
    return (M + M.T) / 2

def angle_of(R):
    return np.degrees(np.arccos(np.clip((np.trace(R)-1)/2, -1, 1)))

# ============================================================
# Step 1: Does sum_S = 0 when all D = I? (for any R)
# ============================================================
print("=" * 70)
print("Step 1: sum_S at D = I for various R")
print("=" * 70)

for trial in range(10):
    R = [special_ortho_group.rvs(3) for _ in range(4)]
    D_dict = {(mu,nu): I3 for mu in range(4) for nu in range(mu+1, 4)}
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    eigs = eigvalsh(M9)
    print(f"D=I, R random: min_eig = {eigs[0]:.6f}, max_eig = {eigs[-1]:.4f}")

# At D=I:
# U = R_mu, W = R_nu^T
# Diagonal (mu,mu): 2*sum_{nu partner} (I - R_mu) + 2*sum_{nu partner} (I - R_nu^T)
# But each mu appears in 3 plaquettes (as first or second index).
# As first index (mu < nu): contributes 2(I - R_mu D) = 2(I - R_mu) [D=I]
# As second index (nu < mu): contributes 2(I - D R_mu^T) = 2(I - R_mu^T) [D=I]
# But f(R_mu,T) = f(R_mu^T,T) (since T^T(I-R)T = T^T(I-R^T)T for scalars)
# So each (I-R_mu) and (I-R_mu^T) contribute identically to the quadratic form.

# Off-diagonal at D=I: D^T + RDR - 2I = I + R_mu R_nu^T - 2I = R_mu R_nu^T - I = -(I - R_mu R_nu^T)

# So sum_S(D=I) has:
# diagonal: 2*3*(I - R_mu) symmetrized (3 partner plaquettes each)
# off-diag: -(I - R_mu R_nu^T) symmetrized

# This is a specific quadratic form that involves R_mu R_nu^T (relative rotations).

# ============================================================
# Step 2: Optimize sum_S with D=I constraint
# ============================================================
print("\n" + "=" * 70)
print("Step 2: Minimize sum_S with D = I")
print("=" * 70)

def min_eig_D_identity(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {(mu,nu): I3 for mu in range(4) for nu in range(mu+1, 4)}
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

best_DI = float('inf')
bestp_DI = None
for _ in range(3000):
    p = np.random.randn(12) * np.pi
    v = min_eig_D_identity(p)
    if v < best_DI:
        best_DI = v; bestp_DI = p.copy()

res_DI = minimize(min_eig_D_identity, bestp_DI, method='Nelder-Mead',
                  options={'maxiter': 50000, 'xatol': 1e-12, 'fatol': 1e-14})
print(f"sum_S(D=I) min eigenvalue: {res_DI.fun:.10f}")

R_opt_DI = [so3_from_vec(res_DI.x[3*i:3*(i+1)]) for i in range(4)]
for mu in range(4):
    print(f"  R_{mu} angle: {angle_of(R_opt_DI[mu]):.2f}°")

# ============================================================
# Step 3: Multiple zero-finding runs for sum_S
# ============================================================
print("\n" + "=" * 70)
print("Step 3: Find all near-zero configurations of sum_S")
print("=" * 70)

def min_eig_sumS(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {}; idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            D_dict[(mu,nu)] = so3_from_vec(params[idx:idx+3]); idx += 3
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

near_zeros = []
for trial in range(100):
    p0 = np.random.randn(30) * np.pi
    res = minimize(min_eig_sumS, p0, method='Nelder-Mead',
                   options={'maxiter': 20000, 'xatol': 1e-10, 'fatol': 1e-12})
    if abs(res.fun) < 0.01:
        R_t = [so3_from_vec(res.x[3*i:3*(i+1)]) for i in range(4)]
        D_t = {}; idx = 12
        for mu in range(4):
            for nu in range(mu+1, 4):
                D_t[(mu,nu)] = so3_from_vec(res.x[idx:idx+3]); idx += 3

        D_angles = [angle_of(D_t[k]) for k in sorted(D_t.keys())]
        near_zeros.append((res.fun, D_angles))

print(f"Found {len(near_zeros)} near-zero configs out of 100 tries")
# Show D angle patterns
for i, (val, d_ang) in enumerate(near_zeros[:15]):
    d_str = [f'{a:.1f}' for a in d_ang]
    near_zero_D = sum(1 for a in d_ang if a < 5)
    print(f"  Config {i}: min_eig={val:.6f}, D_angles={d_str}, #D≈I: {near_zero_D}")

# ============================================================
# Step 4: Check hypothesis: sum_S = 0 iff enough D = I
# ============================================================
print("\n" + "=" * 70)
print("Step 4: Does sum_S -> 0 require most D ≈ I?")
print("=" * 70)

# Check: if only SOME D = I, does sum_S still have zero?
# Try: set exactly 3 D's to I (a spanning tree of the complete graph K4)
# K4 has 6 edges. A spanning tree has 3 edges.
# Set D_{01}, D_{02}, D_{03} = I (star from vertex 0), optimize over D_{12}, D_{13}, D_{23} and R.

def min_eig_partial_DI(params):
    # params: 4 R (12 params) + 3 D (9 params) = 21
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {
        (0,1): I3, (0,2): I3, (0,3): I3,
        (1,2): so3_from_vec(params[12:15]),
        (1,3): so3_from_vec(params[15:18]),
        (2,3): so3_from_vec(params[18:21]),
    }
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

best_partial = float('inf')
bestp_partial = None
for _ in range(3000):
    p = np.random.randn(21) * np.pi
    v = min_eig_partial_DI(p)
    if v < best_partial:
        best_partial = v; bestp_partial = p.copy()

res_partial = minimize(min_eig_partial_DI, bestp_partial, method='Nelder-Mead',
                       options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"Star tree D=I: min_eig = {res_partial.fun:.8f}")

# Try: NO D = I, all free
# (This is the general case, already tested — min eig → 0)

# Try: exactly ONE D = I
def min_eig_one_DI(params):
    R = [so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)]
    D_dict = {(0,1): I3}  # Only D_01 = I
    idx = 12
    for mu in range(4):
        for nu in range(mu+1, 4):
            if (mu,nu) != (0,1):
                D_dict[(mu,nu)] = so3_from_vec(params[idx:idx+3])
                idx += 3
    M12 = build_sumS_12(R, D_dict)
    M9 = P.T @ M12 @ P; M9 = (M9+M9.T)/2
    return eigvalsh(M9)[0]

best_one = float('inf')
bestp_one = None
for _ in range(3000):
    p = np.random.randn(27) * np.pi
    v = min_eig_one_DI(p)
    if v < best_one:
        best_one = v; bestp_one = p.copy()

res_one = minimize(min_eig_one_DI, bestp_one, method='Nelder-Mead',
                   options={'maxiter': 50000, 'xatol': 1e-10, 'fatol': 1e-12})
print(f"One D=I: min_eig = {res_one.fun:.8f}")

# ============================================================
# Step 5: At the zero-set, what's the null eigenvector?
# ============================================================
print("\n" + "=" * 70)
print("Step 5: Null eigenvector at sum_S = 0")
print("=" * 70)

# Refine the best near-zero
best_all = float('inf')
bestp_all = None
for _ in range(5000):
    p = np.random.randn(30) * np.pi
    v = min_eig_sumS(p)
    if v < best_all:
        best_all = v; bestp_all = p.copy()
res_all = minimize(min_eig_sumS, bestp_all, method='Nelder-Mead',
                   options={'maxiter': 100000, 'xatol': 1e-14, 'fatol': 1e-16})

R_z = [so3_from_vec(res_all.x[3*i:3*(i+1)]) for i in range(4)]
D_z = {}; idx = 12
for mu in range(4):
    for nu in range(mu+1, 4):
        D_z[(mu,nu)] = so3_from_vec(res_all.x[idx:idx+3]); idx += 3

M12_z = build_sumS_12(R_z, D_z)
M9_z = P.T @ M12_z @ P; M9_z = (M9_z + M9_z.T)/2
eigs_z, vecs_z = eigh(M9_z)

print(f"Min eigenvalue: {eigs_z[0]:.10f}")
print(f"All eigenvalues: {eigs_z}")

v = vecs_z[:, 0]
T_0 = v[0:3]; T_1 = v[3:6]; T_2 = v[6:9]; T_3 = -(T_0+T_1+T_2)

print(f"\nNull eigenvector:")
print(f"  T_0 = {T_0}")
print(f"  T_1 = {T_1}")
print(f"  T_2 = {T_2}")
print(f"  T_3 = {T_3}")
print(f"  |T_0| = {np.linalg.norm(T_0):.4f}")
print(f"  |T_1| = {np.linalg.norm(T_1):.4f}")
print(f"  |T_2| = {np.linalg.norm(T_2):.4f}")
print(f"  |T_3| = {np.linalg.norm(T_3):.4f}")

# Per-plaquette breakdown at zero config
print(f"\nPer-plaquette sum_S at zero config:")
for mu in range(4):
    for nu in range(mu+1, 4):
        Dmn = D_z[(mu,nu)]
        U = R_z[mu] @ Dmn; W = Dmn @ R_z[nu].T; RDR = R_z[mu] @ Dmn @ R_z[nu].T
        T = [T_0, T_1, T_2, T_3]
        budget = 2*f(U, T[mu]) + 2*f(W, T[nu])
        cross = 2*T[mu] @ (2*I3 - Dmn.T - RDR) @ T[nu]
        print(f"  ({mu},{nu}): D_angle={angle_of(Dmn):.1f}°, budget={budget:.6f}, cross={cross:.6f}, net={budget-cross:.6f}")

# ============================================================
# Step 6: Check if total_gap (with 2*sum f(R,T)) is strictly > 0 at this config
# ============================================================
print("\n" + "=" * 70)
print("Step 6: Total gap at sum_S = 0 config")
print("=" * 70)

T = [T_0, T_1, T_2, T_3]
term1 = 2*sum(f(R_z[mu], T[mu]) for mu in range(4))
sumS_val = sum(
    2*f(R_z[mu]@D_z[(mu,nu)], T[mu]) + 2*f(D_z[(mu,nu)]@R_z[nu].T, T[nu])
    - 2*T[mu] @ (2*I3 - D_z[(mu,nu)].T - R_z[mu]@D_z[(mu,nu)]@R_z[nu].T) @ T[nu]
    for mu in range(4) for nu in range(mu+1, 4)
)
print(f"term1 (2*sum f(R,T)) = {term1:.8f}")
print(f"sum_S = {sumS_val:.8f}")
print(f"total_gap = {term1 + sumS_val:.8f}")
print(f"||T||^2 = {sum(t@t for t in T):.6f}")

# ============================================================
# Step 7: Key structural test — rewrite sum_S using product R_mu R_nu^T
# ============================================================
print("\n" + "=" * 70)
print("Step 7: sum_S in terms of relative rotations")
print("=" * 70)

# The cross matrix for each plaquette: D^T + RDR - 2I
# = D_{mu,nu}^{-1} + R_mu D_{mu,nu} R_nu^T - 2I
#
# If we define:
#   E_{mu,nu} = R_mu D_{mu,nu} (the full "east" link product)
#   N_{mu,nu} = D_{mu,nu} R_nu^T (the full "north" link product)
# Then:
#   D = E^{-1} R_mu = R_mu^{-1} E  →  D^{-1} = E^{-1} R_mu = R_mu^T E_{mu,nu}^T ... no
#   Actually D_{mu,nu} = R_mu^{-1} U_{mu,nu}, so D^{-1} = U^{-1} R_mu = (R_mu D)^{-1} R_mu = D^{-1}
#   D^T = D^{-1} for SO(3)
#   And RDR = R_mu D R_nu^T = U R_nu^T = E_{mu,nu} R_nu^T? No, U = R_mu D = E_{mu,nu}...
#   Wait U_{mu,nu} = R_mu D_{mu,nu}. So RDR = U_{mu,nu} R_nu^T.
#
# Cross = D^T + U R_nu^T - 2I
# = U^T R_mu + U R_nu^T - 2I   [since D^T = (R_mu^{-1} U)^T = U^T R_mu]
# = U^T R_mu + U R_nu^T - 2I

# This is interesting! The cross matrix only depends on U and R_mu, R_nu.
# And U = R_mu D.

# Let's verify:
R_mu = special_ortho_group.rvs(3); R_nu = special_ortho_group.rvs(3)
D_mn = special_ortho_group.rvs(3)
U = R_mu @ D_mn

cross1 = D_mn.T + R_mu @ D_mn @ R_nu.T - 2*I3
cross2 = U.T @ R_mu + U @ R_nu.T - 2*I3
print(f"Cross identity U^T R_mu + U R_nu^T - 2I: error = {np.linalg.norm(cross1 - cross2):.2e}")

# So the off-diagonal block (mu,nu) of sum_S is:
# U^T R_mu + U R_nu^T - 2I   (symmetric when transposed and indices swapped)

# And the diagonal block (mu,mu):
# sum over partners: 2(I-U_{mu,nu}) for nu>mu PLUS 2(I-W_{nu,mu}) for nu<mu
# = 2*sum_{nu>mu} (I - R_mu D_{mu,nu}) + 2*sum_{nu<mu} (I - D_{nu,mu} R_mu^T)

# Now: define for each vertex mu, the "dressed" rotations P_mu^{(nu)} = R_mu D_{mu,nu}
# These are 3 rotations per vertex (one for each partner plaquette).

# The sum_S matrix can be written in terms of these P's and the R's.
# But this doesn't obviously simplify.

# ============================================================
# Step 8: Try writing sum_S as ||AT||_F^2 for some matrix A
# ============================================================
print("\n" + "=" * 70)
print("Step 8: Frobenius norm representation")
print("=" * 70)

# sum_S = T_vec^T M_12 T_vec = Tr[T^T M_12 T] where T_vec = vec(T)
# If M_12 = A^T A for some matrix A, then sum_S = ||A T_vec||^2 >= 0.
#
# On the constraint subspace V: M_9 = P^T M_12 P = (AP)^T (AP) = L^T L where L = AP.
# So sum_S|_V = ||L t||^2 >= 0 where t is the 9D reduced vector.
#
# This is just the Cholesky/Gram decomposition — it exists IFF M_9 is PSD.
#
# We already checked Cholesky works for 1000 random Q. The question is whether
# there exists a Q where M_9 is NOT PSD.
#
# From our adversarial optimization: min eigenvalue → 0 but never negative.
# This strongly suggests M_9 is always PSD.

# Let me do ONE FINAL definitive test with many restarts and higher precision:
print("\nFinal definitive test: 200 restarts, high precision")
global_best = float('inf')
global_bestp = None
for trial in range(200):
    p0 = np.random.randn(30) * np.pi * 2
    res = minimize(min_eig_sumS, p0, method='Nelder-Mead',
                   options={'maxiter': 15000, 'xatol': 1e-10, 'fatol': 1e-12})
    if res.fun < global_best:
        global_best = res.fun
        global_bestp = res.x.copy()
        if res.fun < -0.001:
            print(f"  *** VIOLATION FOUND: min_eig = {res.fun:.8f} ***")
            break

res_final = minimize(min_eig_sumS, global_bestp, method='Nelder-Mead',
                     options={'maxiter': 200000, 'xatol': 1e-14, 'fatol': 1e-16})
print(f"FINAL: sum_S min eigenvalue = {res_final.fun:.12f}")

if res_final.fun > -1e-8:
    print("CONCLUSION: sum_S >= 0 holds (tight at 0)")
    print("Both LEMMA_D and LEMMA_RDR are individually false,")
    print("but their SUM is non-negative.")
else:
    print("CONCLUSION: sum_S < 0 found — conjecture may be in trouble!")
