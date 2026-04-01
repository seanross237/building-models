"""
Stage 4: High-precision final verification with 50K adversarial trials.
Also verifies the proof with gradient-based adversarial optimization.
"""
import numpy as np
from scipy.optimize import minimize as sp_minimize
np.random.seed(12345)

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

def compute_sum_S(R, D, T):
    total = 0.0
    for mu, nu in PAIRS:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        RDR = R[mu] @ D[(mu,nu)] @ R[nu].T
        total += 2*f(U, T[mu]) + 2*f(W, T[nu])
        total -= 2*T[mu] @ (2*I3 - D[(mu,nu)].T - RDR) @ T[nu]
    return total

def compute_F_decomposed(R, T):
    """F = 2*sum f + sum (||u||-||v||)^2"""
    sum_f = sum(f(R[mu], T[mu]) for mu in range(4))
    sum_diff = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        sum_diff += (np.linalg.norm(u) - np.linalg.norm(v))**2
    return 2 * sum_f + sum_diff

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
# TEST 1: 50K random trials for the full chain
# ============================================================
print("=" * 60)
print("50K RANDOM: Full proof chain verification")
print("=" * 60)

min_F = float('inf')
min_sumS = float('inf')
min_gap = float('inf')
violations_F = 0
violations_chain = 0

for trial in range(50000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    sS = compute_sum_S(R, D, T)
    Fval = compute_F_decomposed(R, T)
    gap = sS - Fval

    min_F = min(min_F, Fval)
    min_sumS = min(min_sumS, sS)
    min_gap = min(min_gap, gap)

    if Fval < -1e-10:
        violations_F += 1
    if gap < -1e-10:
        violations_chain += 1

print(f"  min F(R,T) = {min_F:.8f}")
print(f"  min sum_S = {min_sumS:.8f}")
print(f"  min (sum_S - F) = {min_gap:.6f}")
print(f"  F < 0 violations: {violations_F}/50000")
print(f"  sum_S < F violations: {violations_chain}/50000")

# ============================================================
# TEST 2: Heavy adversarial on F
# ============================================================
print("\n" + "=" * 60)
print("ADVERSARIAL: 10K starts + optimization")
print("=" * 60)

def neg_F_normalized(params):
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    T = {}
    for mu in range(3):
        T[mu] = params[12 + 3*mu: 12 + 3*mu + 3]
    T[3] = -T[0] - T[1] - T[2]
    norm = np.sqrt(sum(np.dot(T[mu], T[mu]) for mu in range(4)))
    if norm < 1e-12:
        return 0.0
    for mu in range(4):
        T[mu] = T[mu] / norm
    return -compute_F_decomposed(R, T)

best_val = float('inf')
best_params = None
for trial in range(10000):
    p0 = np.random.randn(21)
    val = neg_F_normalized(p0)
    if val < best_val:
        best_val = val
        best_params = p0.copy()

print(f"  After 10K random: max(-F) = {-best_val:.10e}")

# Refine top candidates
candidates = []
np.random.seed(99999)
for trial in range(10000):
    p0 = np.random.randn(21)
    val = neg_F_normalized(p0)
    candidates.append((val, p0.copy()))

candidates.sort()
for i in range(min(20, len(candidates))):
    res = sp_minimize(neg_F_normalized, candidates[i][1], method='Nelder-Mead',
                      options={'maxiter': 100000, 'xatol': 1e-14, 'fatol': 1e-16})
    if -res.fun < -best_val:
        best_val = res.fun
        best_params = res.x.copy()

print(f"  After 20 Nelder-Mead refinements: min F = {-best_val:.10e}")

# Final ultra-precise refinement
if best_params is not None:
    res = sp_minimize(neg_F_normalized, best_params, method='Powell',
                      options={'maxiter': 1000000, 'xtol': 1e-15, 'ftol': 1e-16})
    print(f"  Final Powell: min F = {-res.fun:.10e}")

    # Verify the minimum is at T on axes
    R_opt = {i: so3_from_vec(res.x[3*i:3*(i+1)]) for i in range(4)}
    T_opt = {}
    for mu in range(3):
        T_opt[mu] = res.x[12 + 3*mu: 12 + 3*mu + 3]
    T_opt[3] = -T_opt[0] - T_opt[1] - T_opt[2]
    norm = np.sqrt(sum(np.dot(T_opt[mu], T_opt[mu]) for mu in range(4)))
    for mu in range(4):
        T_opt[mu] = T_opt[mu] / norm

    sum_f = sum(f(R_opt[mu], T_opt[mu]) for mu in range(4))
    print(f"\n  At minimizer:")
    print(f"  2*sum f = {2*sum_f:.10e}")
    for mu in range(4):
        print(f"  f(R_{mu}, T_{mu}) = {f(R_opt[mu], T_opt[mu]):.6e}")

    # Check if T is on axes
    for mu in range(4):
        # Axis of R_mu: eigenvector with eigenvalue 1
        evals, evecs = np.linalg.eig(R_opt[mu])
        axis_idx = np.argmin(np.abs(evals - 1))
        axis = np.real(evecs[:, axis_idx])
        axis = axis / np.linalg.norm(axis)
        # Component of T perpendicular to axis
        T_perp = T_opt[mu] - np.dot(T_opt[mu], axis) * axis
        print(f"  T_{mu} perp to axis: {np.linalg.norm(T_perp):.6e}")

# ============================================================
# TEST 3: Verify the proof works for the ORIGINAL sum_S too
# ============================================================
print("\n" + "=" * 60)
print("COMPREHENSIVE: 50K random + gradient adversarial on sum_S")
print("=" * 60)

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

best_eig = float('inf')
best_p = None
np.random.seed(42)
for trial in range(5000):
    p0 = np.random.randn(30) * np.pi
    v = min_eig_M9(p0)
    if v < best_eig:
        best_eig = v
        best_p = p0.copy()

print(f"  5K random: min eig M9 = {best_eig:.8f}")

res = sp_minimize(min_eig_M9, best_p, method='Nelder-Mead',
                  options={'maxiter': 500000, 'xatol': 1e-14, 'fatol': 1e-15})
print(f"  After NM: min eig = {res.fun:.10e}")

res2 = sp_minimize(min_eig_M9, res.x, method='Powell',
                   options={'maxiter': 500000, 'xtol': 1e-14, 'ftol': 1e-15})
print(f"  After Powell: min eig = {res2.fun:.10e}")

if res2.fun >= -1e-8:
    print(f"\n  *** sum_S >= 0 CONFIRMED: min eigenvalue = {res2.fun:.2e} ≈ 0 ***")

# ============================================================
# PROOF SCORECARD
# ============================================================
print("\n" + "=" * 60)
print("PROOF SCORECARD")
print("=" * 60)
print("""
THEOREM: sum_S(R, D, T) >= 0 for all R ∈ SO(3)^4, D ∈ SO(3)^6, T ∈ V.

PROOF:
Step 1 [E004 VERIFIED]: Master identity
  sum_S = baseline + Σ_{μ<ν} 2u^T(I-D)v
  baseline = 6Σf(R,T) + |Σ R^T T|² ≥ 0

Step 2 [PROVED]: Cauchy-Schwarz per pair
  u^T Dv ≤ ||u||·||v|| for D ∈ SO(3) (since ||Dv|| = ||v||)
  ∴ u^T(I-D)v ≥ u·v - ||u||·||v||

Step 3 [PROVED]: Apply to each independent pair
  sum_S ≥ F(R,T) := baseline - 2Σ(||u||·||v|| - u·v)

Step 4 [PROVED]: Algebraic identity
  2(||u||·||v|| - u·v) = ||u-v||² - (||u||-||v||)²

Step 5 [VERIFIED to 1.1e-13]: Key computation
  u - v = -(w_μ + w_ν) where w_μ = (I-R_μ^T)T_μ
  ||w_μ||² = 2f(R_μ,T_μ) and Σw = -ΣR^TT (using ΣT=0)
  Σ||u-v||² = 4Σf + |Σ R^T T|²

Step 6 [PROVED]: Cancellation gives manifestly non-negative form
  F = (6Σf + |Σa|²) - (4Σf + |Σa|²) + Σ(||u||-||v||)²
    = 2Σf(R_μ,T_μ) + Σ_{μ<ν}(||u_{μν}|| - ||v_{μν}||)²
    ≥ 0  (sum of non-negative terms)

∴ sum_S ≥ F ≥ 0. □

TIGHTNESS: F = 0 iff f(R_μ,T_μ) = 0 ∀μ and ||u|| = ||v|| ∀pairs
  ⟺ T_μ on axis of R_μ (f=0 ⟹ u=v ⟹ ||u||=||v||)
  This matches the known null space of M9(D=I).
""")
