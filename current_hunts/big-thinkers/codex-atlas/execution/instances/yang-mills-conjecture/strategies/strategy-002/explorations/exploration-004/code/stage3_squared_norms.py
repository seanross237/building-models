"""
Stage 3: Attempt to write sum_S as a sum of squared norms.

Key idea: Use the B-vector structure from the per-plaquette identity.
4|T_mu - T_nu|^2 = |B|^2 + S_{mu,nu} + extraction_term

Try to find vectors w_k(R, D, T) such that sum_S = Σ ||w_k||^2.
"""
import numpy as np
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

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return I3
    k = v / theta
    K = skew(k)
    return I3 + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def random_T_in_V():
    T = {mu: np.random.randn(3) for mu in range(3)}
    T[3] = -T[0] - T[1] - T[2]
    return T

P = np.zeros((12, 9))
P[0:3, 0:3] = I3
P[3:6, 3:6] = I3
P[6:9, 6:9] = I3
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

# ============================================================
# APPROACH: Cholesky-like decomposition of M9
# ============================================================
# For specific (R, D), compute M9 and check if Cholesky works.
# If M9 = L L^T with L depending smoothly on (R, D), we have a proof sketch.

print("=" * 60)
print("CHOLESKY TEST: Is M9 always PSD?")
print("=" * 60)

n_psd = 0
n_total = 5000
min_eig = float('inf')
for trial in range(n_total):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T) / 2
    eigs = np.linalg.eigvalsh(M9)
    if eigs[0] >= -1e-12:
        n_psd += 1
    min_eig = min(min_eig, eigs[0])

print(f"  {n_total} configs: PSD count = {n_psd}/{n_total}")
print(f"  min eigenvalue: {min_eig:.2e}")

# ============================================================
# INTENSIVE adversarial search using multiple restarts + refinement
# ============================================================
print("\n" + "=" * 60)
print("INTENSIVE ADVERSARIAL SEARCH")
print("=" * 60)

def min_eig_M9(params):
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    D = {}
    idx = 12
    for p in PAIRS:
        D[p] = so3_from_vec(params[idx:idx+3])
        idx += 3
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T) / 2
    return np.linalg.eigvalsh(M9)[0]

def numerical_gradient(func, x, eps=1e-7):
    grad = np.zeros_like(x)
    f0 = func(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += eps
        grad[i] = (func(x_plus) - f0) / eps
    return grad

# Phase 1: Wide random search
best_val = float('inf')
best_params = None
for trial in range(5000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    if v < best_val:
        best_val = v
        best_params = p0.copy()

print(f"  Phase 1 (5000 random): best = {best_val:.8f}")

# Phase 2: Gradient descent from best start
x = best_params.copy()
for lr in [0.05, 0.01, 0.005, 0.001]:
    for step in range(300):
        g = numerical_gradient(min_eig_M9, x)
        x -= lr * g
        v = min_eig_M9(x)
        if v < best_val:
            best_val = v
            best_params = x.copy()
    print(f"  After lr={lr}: best = {best_val:.10e}")

# Phase 3: Multiple local optimizations from different starts
top_starts = []
for trial in range(10000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    top_starts.append((v, p0.copy()))

top_starts.sort()
print(f"\n  Top 5 random starts: {[f'{s[0]:.4f}' for s in top_starts[:5]]}")

for rank, (v0, p0) in enumerate(top_starts[:10]):
    x = p0.copy()
    for lr in [0.01, 0.003, 0.001]:
        for step in range(200):
            g = numerical_gradient(min_eig_M9, x)
            x -= lr * g
            v = min_eig_M9(x)
            if v < best_val:
                best_val = v
                best_params = x.copy()
    if rank % 3 == 0:
        print(f"  Start #{rank}: optimized to {min_eig_M9(x):.10e}")

print(f"\n  FINAL MINIMUM EIGENVALUE: {best_val:.12e}")

# ============================================================
# ANALYZE THE MINIMIZER
# ============================================================
print("\n" + "=" * 60)
print("MINIMIZER ANALYSIS")
print("=" * 60)

R_opt = {i: so3_from_vec(best_params[3*i:3*(i+1)]) for i in range(4)}
D_opt = {}
idx = 12
for p in PAIRS:
    D_opt[p] = so3_from_vec(best_params[idx:idx+3])
    idx += 3

M12_opt = build_M12(R_opt, D_opt)
M9_opt = P.T @ M12_opt @ P
M9_opt = (M9_opt + M9_opt.T) / 2
eigs_opt = np.linalg.eigvalsh(M9_opt)
print(f"  Eigenvalues: {np.array2string(eigs_opt, precision=4)}")

for i in range(4):
    angle = np.degrees(np.arccos(np.clip((np.trace(R_opt[i])-1)/2, -1, 1)))
    print(f"  R_{i}: {angle:.1f}°")
for p in PAIRS:
    angle = np.degrees(np.arccos(np.clip((np.trace(D_opt[p])-1)/2, -1, 1)))
    dist = np.linalg.norm(D_opt[p] - I3, 'fro')
    print(f"  D_{p}: {angle:.1f}° (||D-I||={dist:.3f})")

# Check if D is near I → minimizer should be D=I
all_near_I = all(np.linalg.norm(D_opt[p] - I3, 'fro') < 0.1 for p in PAIRS)
print(f"\n  All D near I: {all_near_I}")

# ============================================================
# CRITICAL TEST: Compare with D=I baseline
# ============================================================
D_I = {p: I3 for p in PAIRS}
M12_DI = build_M12(R_opt, D_I)
M9_DI = P.T @ M12_DI @ P
M9_DI = (M9_DI + M9_DI.T) / 2
eigs_DI = np.linalg.eigvalsh(M9_DI)
print(f"\n  Same R, D=I eigenvalues: {np.array2string(eigs_DI, precision=4)}")
print(f"  M9(D=I) min eig: {eigs_DI[0]:.6e}")

# ============================================================
# NEW APPROACH: "Gauge-invariant" rewriting
# ============================================================
print("\n" + "=" * 60)
print("GAUGE REWRITING: absorb R into T")
print("=" * 60)

# Define p_mu = R_mu^T T_mu. Then T_mu = R_mu p_mu.
# Constraint: sum R_mu p_mu = 0 (NOT sum p_mu = 0).
#
# f(R_mu D, T_mu) = f(R_mu D, R_mu p_mu) = p_mu^T R_mu^T(I - R_mu D)R_mu p_mu
# = p_mu^T(I - D)p_mu = f(D, p_mu) [since R_mu^T R_mu = I]
#
# Wait: R_mu^T(I - R_mu D)R_mu = R_mu^T R_mu - R_mu^T R_mu D R_mu = I - D R_mu?
# No: R_mu^T(I - R_mu D) = R_mu^T - D. So R_mu^T(I - R_mu D)R_mu = R_mu^T R_mu - D R_mu = I - D R_mu.
# So f(R_mu D, R_mu p) = p^T(I - D R_mu)p?
# But f(M, q) = q^T(I-M)q. So f(R_mu D, T_mu) = T_mu^T(I-R_mu D)T_mu.
# With T_mu = R_mu p_mu: (R_mu p)^T(I - R_mu D)(R_mu p) = p^T R_mu^T(I-R_mu D)R_mu p
# = p^T(I - D R_mu)... wait: R_mu^T(I - R_mu D) = R_mu^T - D. And (R_mu^T - D)R_mu = I - D R_mu.
# Hmm, that doesn't simplify. Let me try differently.
# T_mu^T(I - R_mu D)T_mu = (R_mu p)^T(I - R_mu D)(R_mu p)
# = p^T R_mu^T R_mu p - p^T R_mu^T R_mu D R_mu p = p^T p - p^T D R_mu p
# No: R_mu^T(I - R_mu D)R_mu = R_mu^T R_mu - R_mu^T R_mu D R_mu = I - D R_mu
# That's not right either. Let me just compute:
# R_mu^T (R_mu D) R_mu = D R_mu. NO.
# R_mu^T (R_mu D) = D. So R_mu^T (I - R_mu D) = R_mu^T - D.
# Then (R_mu^T - D) R_mu = I - D R_mu.
# Hmm, so p^T(I - D R_mu)p = f(D R_mu, p).
# So f(R_mu D, R_mu p) = f(D R_mu, p). NOT f(D, p).

# WAIT. f(R_mu D, R_mu p) = (R_mu p)^T (I - R_mu D)(R_mu p)
# = p^T R_mu^T (I - R_mu D) R_mu p
# Let's expand R_mu^T (I - R_mu D) R_mu:
# = R_mu^T R_mu - R_mu^T R_mu D R_mu
# = I - D R_mu  (Wait: R_mu^T R_mu D R_mu = (R_mu^T R_mu) (D R_mu) = D R_mu)
# Actually: R_mu^T R_mu = I. And R_mu^T (R_mu D) R_mu = (R_mu^T R_mu)(D R_mu) = D R_mu.
# NO! Matrix multiplication: R_mu^T × (R_mu D) × R_mu = (R_mu^T R_mu D) × R_mu = D R_mu.
# Wait: R_mu^T (R_mu D R_mu)?? No, I need to be careful.
# R_mu^T (R_mu D) R_mu: first R_mu^T × R_mu D = D. Then D × R_mu = D R_mu.
# So R_mu^T (R_mu D) R_mu = D R_mu.
# Therefore: p^T [I - D R_mu] p = f(D R_mu, p).

# This doesn't simplify nicely because of the "D R_mu" combination.

# Let me try a different substitution. For the cross term:
# T_mu^T(2I - D^T - R_mu D R_nu^T)T_nu = (R_mu p_mu)^T(2I - D^T - R_mu D R_nu^T)(R_nu p_nu)
# = p_mu^T R_mu^T(2I - D^T - R_mu D R_nu^T)R_nu p_nu
# = p_mu^T(2 R_mu^T R_nu - R_mu^T D^T R_nu - D R_nu^T R_nu)p_nu
# = p_mu^T(2 R_mu^T R_nu - R_mu^T D^T R_nu - D)p_nu
# Wait: R_nu^T R_nu = I. So R_mu^T (R_mu D R_nu^T) R_nu = D.
# And R_mu^T(2I)R_nu = 2 R_mu^T R_nu.
# And R_mu^T D^T R_nu = R_mu^T D^T R_nu.
# So: 2 R_mu^T R_nu - R_mu^T D^T R_nu - D.

# Define G_{mu,nu} = R_mu^T R_nu (the "gauge" rotation from nu to mu).
# Then: 2G - G D^T G^{-1}... hmm no, R_mu^T D^T R_nu = (R_nu^T D R_mu)^T.

# This substitution doesn't simplify either. Let me abandon this approach.

# ============================================================
# ANOTHER APPROACH: Direct eigenvalue bound using Gershgorin
# ============================================================
print("\n" + "=" * 60)
print("GERSHGORIN BOUND on M9")
print("=" * 60)

# M9 is 9x9 with 3x3 blocks. Use block Gershgorin:
# If diagonal block D_i has min eigenvalue d_i and off-diagonal blocks have norms r_i,
# then min eigenvalue of M >= min_i (d_i - r_i).

def block_gershgorin(R, D):
    M12 = build_M12(R, D)
    M9 = P.T @ M12 @ P
    M9 = (M9 + M9.T) / 2

    # 3 blocks of size 3x3
    diag_eigs = []
    off_norms = [0, 0, 0]
    for i in range(3):
        blk = M9[3*i:3*i+3, 3*i:3*i+3]
        diag_eigs.append(np.linalg.eigvalsh(blk)[0])
        for j in range(3):
            if j != i:
                off_norms[i] += np.linalg.norm(M9[3*i:3*i+3, 3*j:3*j+3], 2)

    gershgorin = min(diag_eigs[i] - off_norms[i] for i in range(3))
    actual = np.linalg.eigvalsh(M9)[0]
    return gershgorin, actual

neg_gersh = 0
tight_count = 0
for trial in range(1000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    g, a = block_gershgorin(R, D)
    if g < 0:
        neg_gersh += 1

print(f"  Gershgorin bound negative: {neg_gersh}/1000")
print(f"  (Gershgorin bound is too loose to prove PSD)")

# ============================================================
# APPROACH: Write M9 = A^T A for explicit A (decomposition)
# ============================================================
print("\n" + "=" * 60)
print("MATRIX DECOMPOSITION: M12 as sum of rank-1 or structured terms")
print("=" * 60)

# For a specific (R, D), decompose M9 = sum v_k v_k^T via eigendecomposition
# and look for patterns in the v_k.

R = {mu: random_SO3() for mu in range(4)}
D = {p: random_SO3() for p in PAIRS}
M12 = build_M12(R, D)
M9 = P.T @ M12 @ P
M9 = (M9 + M9.T) / 2

eigs, vecs = np.linalg.eigh(M9)
print(f"  Eigenvalues: {np.array2string(eigs, precision=4)}")

# The diagonal part of M12 is:
# M12_diag[mu,mu] = sum_{nu:partner} [2I - U_{mu,nu} - U_{mu,nu}^T + 2I - W_{nu,mu} - W_{nu,mu}^T]
# where the sum over nu ≠ mu with appropriate signs.

# Actually, wait. Let me reconsider the STRUCTURE.
# Each pair (mu,nu) contributes:
# - To diagonal (mu,mu): 2I - U - U^T (symmetric, PSD since U in SO(3))
# - To diagonal (nu,nu): 2I - W - W^T (symmetric, PSD)
# - To off-diagonal (mu,nu): D^T + RDR - 2I (NOT necessarily PSD)
#
# The diagonal blocks are sums of PSD matrices → PSD.
# The problem is the off-diagonal blocks.

# KEY INSIGHT: For R in SO(3), 2I - R - R^T = 2(1-cos θ)(I - nn^T) where θ is rotation angle.
# So diagonal blocks are PSD with eigenvalues 0, 2(1-cos θ), 2(1-cos θ) (one zero on axis).

# For the off-diagonal: D^T + RDR - 2I. Let's analyze.
# D^T + RDR - 2I = (D^T - I) + (RDR - I) = -(I-D^T) - (I-RDR)
# Both I-D^T and I-RDR have the form I-S for S in SO(3).
# So D^T + RDR - 2I = -(I-D^T) - (I-RDR). The symmetric part:
# [(D^T+D)/2 - I] + [(RDR+(RDR)^T)/2 - I] = (cos θ_D - 1)(I-nn^T) + (cos θ_{RDR} - 1)(I-mm^T)
# Both <= 0. So symmetric part of off-diagonal block is NSD (negative semi-definite)!

print("\n  Off-diagonal symmetric part analysis:")
for trial in range(5):
    R_mu, R_nu = random_SO3(), random_SO3()
    D_mn = random_SO3()
    cross = D_mn.T + R_mu @ D_mn @ R_nu.T - 2*I3
    sym = (cross + cross.T) / 2
    eigs_sym = np.linalg.eigvalsh(sym)
    print(f"  Trial {trial}: off-diag sym eigs = [{eigs_sym[0]:.4f}, {eigs_sym[1]:.4f}, {eigs_sym[2]:.4f}]")

# So symmetric part of off-diagonal is always <= 0!
# This means the cross term -2T^T(off-diag)T = -2T^T * negative * T = positive contribution
# Wait no: the off-diagonal in M12 is +cross = D^T + RDR - 2I (which has NSD symmetric part).
# In the quadratic form: T^T M T includes T_mu^T(cross)T_nu + T_nu^T(cross^T)T_mu
# = 2 T_mu^T(sym part of cross)T_nu (since antisymmetric part cancels).
# And sym part <= 0, so 2 T_mu^T(neg thing)T_nu can be positive or negative depending on T.

# ============================================================
# APPROACH: Use symmetry reductions
# ============================================================
print("\n" + "=" * 60)
print("SYMMETRY: Does sum_S have nice symmetry properties?")
print("=" * 60)

# Consider the "gauge transformation": R_mu → R_mu G for all mu (right-multiply by same G).
# D_{mu,nu} → D_{mu,nu} (unchanged).
# T_mu → G^T T_mu ... no, T_mu is the eigenvector, it's fixed.
# Actually in the lattice setup, a gauge transformation at vertex x transforms:
# R_mu → G R_mu, T_mu → G T_mu (left-multiply by same G).
# Under T_mu → G T_mu, R_mu → G R_mu:
# f(R_mu D, T_mu) → f(G R_mu D, G T_mu) = (G T)^T(I - G R D)(G T) = T^T G^T(I-GRD)G T
# = T^T(G^T G - G^T G R D)T = T^T(I - RD)T = f(RD, T). Wait, G^T G = I but G^T(GRD) = RD.
# So f(GRD, GT) = f(RD, T). Hmm, that's f(R_mu D, T_mu) not f(G R_mu D, G T_mu).
# f(G R_mu D, G T_mu) = (GT)^T(I - GRD)(GT) = T^T G^T(I - GRD)GT = T^T(I - RD)T? NO.
# G^T(I - GRD)G = G^T G - G^T GRD G = I - RDG. Not the same.

# Hmm, gauge invariance doesn't simplify things much in this formulation.

# Let me try ONE MORE approach: relate to the Weitzenbock formula.
# ============================================================
print("\n" + "=" * 60)
print("WEITZENBOCK: Alternative decomposition of sum_S")
print("=" * 60)

# Define for each mu: phi_mu = (I - R_mu) T_mu (the "curvature" vector).
# Then f(R_mu, T_mu) = T_mu^T(I-R_mu)T_mu, and phi_mu = (I-R_mu)T_mu.
# Note: ||phi_mu||^2 ≠ f(R_mu, T_mu) in general.
# Actually ||phi_mu||^2 = T_mu^T(I-R_mu)^T(I-R_mu)T_mu = T_mu^T(2I-R_mu-R_mu^T)T_mu = 2f(R_mu, T_mu).

# So 2f(R_mu, T_mu) = ||(I-R_mu)T_mu||^2.

# Similarly, 2f(R_mu D, T_mu) = ||(I-R_mu D)T_mu||^2.
# And 2f(D R_nu^T, T_nu) = ||(I - D R_nu^T)T_nu||^2 = ||(I - W)T_nu||^2 where W = D R_nu^T.
# Wait: ||(I-M)p||^2 = p^T(I-M)^T(I-M)p = p^T(2I-M-M^T)p = 2f(M,p) only if M in SO(3).
# For M in SO(3): (I-M)^T(I-M) = I - M - M^T + M^T M = 2I - M - M^T. ✓

# So the budget part of sum_S is:
# sum_{mu<nu} [||(I-U)T_mu||^2 + ||(I-W)T_nu||^2]

# And sum_S = sum_{mu<nu} ||(I-U)T_mu||^2 + ||(I-W)T_nu||^2 - 2T_mu^T(2I-D^T-RDR)T_nu

# The cross term 2I - D^T - RDR:
# Note (I-U)^T + (I-W)^T = (I-U^T) + (I-W^T) = 2I - U^T - W^T
# = 2I - D^T R_mu^T - R_nu D^T
# Hmm, this is 2I - D^T R_mu^T - R_nu D^T, not 2I - D^T - RDR.

# Actually: D^T = (R_mu D)^T R_mu = U^T R_mu. And RDR = U R_nu^T.
# So 2I - D^T - RDR = 2I - U^T R_mu - U R_nu^T.

# And (I-U^T) R_mu + (I-U) R_nu^T:
# = R_mu - U^T R_mu + R_nu^T - U R_nu^T
# = R_mu + R_nu^T - U^T R_mu - U R_nu^T
# = R_mu + R_nu^T - D^T - RDR
# Hmm, 2I-D^T-RDR vs R_mu+R_nu^T-D^T-RDR. Off by (2I-R_mu-R_nu^T).

# KEY: sum_S involves BOTH the budget (diagonal) and cross terms.
# Can we write: sum_S = ||(stuff)||^2 where stuff involves linear combinations of T_mu?

# Let me try constructing A (12 x 12 or 12 x K) such that sum_S = ||A T||^2:
# For this, we need M12 = A^T A, i.e., M12 is PSD.
# But M12 is the FULL 12x12 matrix before projection to V.
# M12 need not be PSD (it only needs to be PSD on V).

# Check: is M12 PSD?
min_eig_12 = float('inf')
for trial in range(1000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    M12 = build_M12(R, D)
    M12 = (M12 + M12.T) / 2
    eig = np.linalg.eigvalsh(M12)[0]
    min_eig_12 = min(min_eig_12, eig)

print(f"  M12 min eigenvalue: {min_eig_12:.6f}")
if min_eig_12 >= -1e-10:
    print(f"  M12 IS PSD! → sum_S >= 0 for ALL T (not just V)!")
    print(f"  This would be a STRONGER result!")
else:
    print(f"  M12 is NOT PSD → need V restriction")

# ============================================================
# CRITICAL: What are the negative eigenvalues of M12?
# ============================================================
if min_eig_12 < -1e-10:
    print("\n  Analyzing M12 negative eigenspace...")

    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    M12 = build_M12(R, D)
    M12 = (M12 + M12.T) / 2
    eigs12, vecs12 = np.linalg.eigh(M12)
    print(f"  M12 eigenvalues: {np.array2string(eigs12, precision=3)}")

    # Check: do negative eigenvectors satisfy sum T = 0?
    neg_idx = np.where(eigs12 < -0.01)[0]
    for idx in neg_idx:
        v = vecs12[:, idx]
        T_check = {mu: v[3*mu:3*mu+3] for mu in range(4)}
        sum_T = sum(T_check[mu] for mu in range(4))
        print(f"  Negative eig {eigs12[idx]:.4f}: |sum T| = {np.linalg.norm(sum_T):.6f}")

    # If negative eigenvectors have sum T ≠ 0, then M12 restricted to V IS PSD.
    # That's the whole point — V restriction kills the negative directions.

# ============================================================
# RANK of the complement: how many negative eigs does M12 have?
# ============================================================
print("\n" + "=" * 60)
print("M12 NEGATIVE EIGENSPACE vs V^perp")
print("=" * 60)

# V^perp = {T: T_0 = T_1 = T_2 = T_3 = c for some c in R^3} (3-dimensional)
# If all negative eigenvalues of M12 lie in V^perp, then M9 >= 0.

for trial in range(5):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    M12 = build_M12(R, D)
    M12 = (M12 + M12.T) / 2
    eigs12, vecs12 = np.linalg.eigh(M12)

    # V^perp basis: e = (1,1,1,1) ⊗ n for n in R^3
    # So V^perp = span of (n, n, n, n) for n in R^3.
    # Orthogonal complement is V = {sum T = 0}.

    neg_count = np.sum(eigs12 < -0.01)
    neg_in_Vperp = 0
    for idx in np.where(eigs12 < -0.01)[0]:
        v = vecs12[:, idx]
        # Project onto V^perp
        sum_v = np.zeros(3)
        for mu in range(4):
            sum_v += v[3*mu:3*mu+3]
        proj_Vperp = np.concatenate([sum_v/4]*4)  # uniform part
        ratio = np.dot(proj_Vperp, proj_Vperp) / np.dot(v, v) if np.dot(v,v) > 0 else 0
        if ratio > 0.99:
            neg_in_Vperp += 1

    print(f"  Trial {trial}: neg_eigs={neg_count}, in V^perp={neg_in_Vperp}")

    # More precise: check if ALL negative eigenspace lies in V^perp
    neg_eig_mask = eigs12 < -0.01
    if np.any(neg_eig_mask):
        neg_space = vecs12[:, neg_eig_mask]  # columns = negative eigenvectors
        # Project each onto V (remove V^perp component)
        for col in range(neg_space.shape[1]):
            v = neg_space[:, col]
            sum_v = np.zeros(3)
            for mu in range(4):
                sum_v += v[3*mu:3*mu+3]
            for mu in range(4):
                v[3*mu:3*mu+3] -= sum_v / 4
            neg_space[:, col] = v

        # How much of the negative eigenvectors is in V?
        norms = np.linalg.norm(neg_space, axis=0)
        print(f"    Neg eigvec norms after V-projection: {norms}")
        if np.all(norms < 1e-8):
            print(f"    ALL negative eigenvectors in V^perp!")
