"""
Stage 1: Verify the polarization lower bound numerically.

Polarization identity for E = I-D (where D in SO(3)):
  u^T E v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)]

Since f(D,p) >= 0 for all p:
  u^T E v >= -(1/2)[f(D,u) + f(D,v)]

Therefore:
  sum_S >= baseline - sum_{mu<nu} [f(D_{mu,nu}, u_{mu,nu}) + f(D_{mu,nu}, v_{mu,nu})]

We verify this and check whether the RHS is always >= 0.
"""
import numpy as np
from scipy.optimize import minimize as sp_minimize
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
    """f(M,p) = p^T (I - M) p. For M in SO(3), f >= 0."""
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

def compute_baseline(R, T):
    """baseline = 6*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2"""
    b = 6.0 * sum(f(R[mu], T[mu]) for mu in range(4))
    s = sum(R[mu].T @ T[mu] for mu in range(4))
    b += np.dot(s, s)
    return b

def compute_correction(R, D, T):
    """correction = sum_{mu<nu} [f(D, u) + f(D, v)]"""
    corr = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        corr += f(D[(mu,nu)], u) + f(D[(mu,nu)], v)
    return corr

def compute_delta_total(R, D, T):
    """delta = sum_{mu<nu} 2 u^T (I-D) v"""
    delta = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        E = I3 - D[(mu,nu)]
        delta += 2.0 * u @ E @ v
    return delta

# ============================================================
# TEST 1: Verify polarization inequality holds
# ============================================================
print("=" * 60)
print("TEST 1: Polarization inequality verification")
print("  sum_S >= baseline - correction")
print("=" * 60)

violations = 0
min_gap = float('inf')
for trial in range(2000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    sS = compute_sum_S(R, D, T)
    bl = compute_baseline(R, T)
    corr = compute_correction(R, D, T)

    # Polarization says: delta >= -correction
    # So sum_S = baseline + delta >= baseline - correction
    gap = sS - (bl - corr)
    min_gap = min(min_gap, gap)
    if gap < -1e-10:
        violations += 1

print(f"  Trials: 2000")
print(f"  Violations: {violations}")
print(f"  Min gap (sum_S - polarization_LB): {min_gap:.6e}")
print(f"  [Should be >= 0 by construction]")

# ============================================================
# TEST 2: Is polarization LB = baseline - correction >= 0?
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: Is baseline - correction >= 0?")
print("  (If yes, proof is done!)")
print("=" * 60)

neg_count = 0
min_pol_lb = float('inf')
max_ratio = 0
ratio_samples = []

for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    bl = compute_baseline(R, T)
    corr = compute_correction(R, D, T)
    pol_lb = bl - corr

    min_pol_lb = min(min_pol_lb, pol_lb)
    if pol_lb < -1e-10:
        neg_count += 1

    if bl > 1e-10:
        ratio_samples.append(corr / bl)
        max_ratio = max(max_ratio, corr / bl)

print(f"  Trials: 5000")
print(f"  Negative count: {neg_count}")
print(f"  Min (baseline - correction): {min_pol_lb:.6f}")
print(f"  Max (correction/baseline): {max_ratio:.6f}")
print(f"  Mean(corr/baseline): {np.mean(ratio_samples):.4f}")
print(f"  Std(corr/baseline): {np.std(ratio_samples):.4f}")

if neg_count > 0:
    print(f"\n  *** POLARIZATION LB CAN GO NEGATIVE — proof via crude polarization FAILS ***")
    print(f"  Need tighter bound or different approach")
else:
    print(f"\n  *** POLARIZATION LB IS ALWAYS >= 0 — PROOF COMPLETE! ***")

# ============================================================
# TEST 3: Adversarial search for worst-case correction/baseline ratio
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: Adversarial search for max correction/baseline")
print("=" * 60)

def skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def so3_from_vec(v):
    theta = np.linalg.norm(v)
    if theta < 1e-15:
        return I3.copy()
    k = v / theta
    K = skew(k)
    return I3 + np.sin(theta)*K + (1-np.cos(theta))*(K@K)

def neg_ratio(params):
    """Minimize -(correction/baseline) to find worst case."""
    R = {i: so3_from_vec(params[3*i:3*(i+1)]) for i in range(4)}
    D = {}
    idx = 12
    for p in PAIRS:
        D[p] = so3_from_vec(params[idx:idx+3])
        idx += 3
    # T in V: parameterize T_0, T_1, T_2, T_3 = -sum
    T = {}
    t_idx = 30
    for mu in range(3):
        T[mu] = params[t_idx:t_idx+3]
        t_idx += 3
    T[3] = -T[0] - T[1] - T[2]

    bl = compute_baseline(R, T)
    if bl < 1e-12:
        return 0.0  # degenerate
    corr = compute_correction(R, D, T)
    return -corr / bl

best_ratio_val = 0
best_params = None
for trial in range(2000):
    p0 = np.random.randn(39)
    p0[30:] *= 2.0  # larger T
    val = -neg_ratio(p0)
    if val > best_ratio_val:
        best_ratio_val = val
        best_params = p0.copy()

print(f"  After 2000 random starts: best corr/baseline = {best_ratio_val:.6f}")

# Refine with Nelder-Mead
if best_params is not None:
    res = sp_minimize(neg_ratio, best_params, method='Nelder-Mead',
                      options={'maxiter': 200000, 'xatol': 1e-12, 'fatol': 1e-14})
    opt_ratio = -res.fun
    print(f"  After optimization: best corr/baseline = {opt_ratio:.8f}")

    if opt_ratio >= 1.0 - 1e-8:
        print(f"  *** RATIO CAN REACH 1.0 — polarization is TIGHT ***")
    elif opt_ratio < 1.0:
        print(f"  *** RATIO < 1.0 — polarization bound SUFFICES! ***")
        print(f"  Gap from 1.0: {1.0 - opt_ratio:.8f}")

# ============================================================
# TEST 4: Per-term analysis — which correction terms are largest?
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: Per-term analysis")
print("=" * 60)

# Decompose baseline into its two parts
for trial in range(10):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    diag_part = 6.0 * sum(f(R[mu], T[mu]) for mu in range(4))
    s = sum(R[mu].T @ T[mu] for mu in range(4))
    cross_part = np.dot(s, s)

    f_D_u_total = 0.0
    f_D_v_total = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        f_D_u_total += f(D[(mu,nu)], u)
        f_D_v_total += f(D[(mu,nu)], v)

    corr = f_D_u_total + f_D_v_total
    bl = diag_part + cross_part

    if trial < 5:
        print(f"  Trial {trial}: diag={diag_part:.3f}, cross={cross_part:.3f}, "
              f"f(D,u)={f_D_u_total:.3f}, f(D,v)={f_D_v_total:.3f}, "
              f"ratio={corr/bl:.4f}" if bl > 1e-10 else f"  Trial {trial}: degenerate")

# ============================================================
# TEST 5: Tighter bound via Cauchy-Schwarz on E_sym + E_anti
# ============================================================
print("\n" + "=" * 60)
print("TEST 5: Tighter bound — C-S on E_sym + spectral on E_anti")
print("=" * 60)

# u^T E v = u^T E_sym v + u^T E_anti v
# |u^T E_sym v| <= sqrt(f(D,u)) * sqrt(f(D,v))  [C-S for PSD form]
# |u^T E_anti v| <= |sin(theta)| * ||u|| * ||v||  [spectral bound]
# So: u^T E v >= -sqrt(f(D,u)*f(D,v)) - |sin(theta)| * ||u|| * ||v||

# Tighter correction:
# correction_CS = sum [2*sqrt(f(D,u)*f(D,v)) + 2*|sin theta| * ||u|| * ||v||]

def get_rotation_angle(D):
    """Get rotation angle of SO(3) matrix."""
    tr = np.clip((np.trace(D) - 1) / 2, -1, 1)
    return np.arccos(tr)

neg_count_cs = 0
min_cs_lb = float('inf')
for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    bl = compute_baseline(R, T)

    corr_cs = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        fu = f(D[(mu,nu)], u)
        fv = f(D[(mu,nu)], v)
        theta = get_rotation_angle(D[(mu,nu)])

        # C-S bound for symmetric part + spectral bound for antisymmetric
        corr_cs += 2*(np.sqrt(fu*fv) + abs(np.sin(theta)) * np.linalg.norm(u) * np.linalg.norm(v))

    cs_lb = bl - corr_cs
    min_cs_lb = min(min_cs_lb, cs_lb)
    if cs_lb < -1e-10:
        neg_count_cs += 1

print(f"  Trials: 5000")
print(f"  Negative count: {neg_count_cs}")
print(f"  Min (baseline - CS_correction): {min_cs_lb:.6f}")
if neg_count_cs > 0:
    print(f"  *** C-S + spectral bound also fails ***")
else:
    print(f"  *** C-S + spectral bound WORKS — proof via this route! ***")

# ============================================================
# TEST 6: Use ONLY Cauchy-Schwarz (no anti-symmetric bound)
# ============================================================
print("\n" + "=" * 60)
print("TEST 6: Pure C-S bound (ignoring antisymmetric part)")
print("=" * 60)

# Since u^T E v = u^T E_sym v + u^T E_anti v
# and E_anti is antisymmetric, u^T E_anti v = -v^T E_anti u
# But the SUM over mu<nu of u^T E_anti v may have structure.
#
# Alternative: just use polarization directly.
# u^T E v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)]
# Lower bound: >= -f(D,u)/2 - f(D,v)/2 (dropping the +f(D,u+v)/2 >= 0 term)
# Upper bound: <= f(D,u+v)/2 (dropping the -f(D,u)/2 - f(D,v)/2 <= 0 terms)
#
# But we can also use: u^T E v = f(D,u+v)/2 - f(D,u)/2 - f(D,v)/2
# This is EXACT, not a bound.
#
# So delta_total = sum 2 u^T E v = sum [f(D,u+v) - f(D,u) - f(D,v)]
# And sum_S = baseline + sum [f(D,u+v) - f(D,u) - f(D,v)]

# Wait, let me verify this. For symmetric forms, polarization is exact:
# x^T A y = (1/2)[(x+y)^T A (x+y) - x^T A x - y^T A y] ONLY if A is symmetric.
# But E = I-D is NOT symmetric!

# For general E: u^T E v = (1/2)[(u+v)^T E (u+v) - u^T E u - v^T E v]
# Since u^T E u = u^T E_sym u (the antisymmetric part vanishes in quadratic form)
# And (u+v)^T E (u+v) = (u+v)^T E_sym (u+v)
# So: u^T E v = (1/2)[(u+v)^T E_sym (u+v) - u^T E_sym u - v^T E_sym v] + u^T E_anti v
#            = u^T E_sym v + u^T E_anti v  (correctly decomposes)
#
# The polarization for the full E:
# (u+v)^T E (u+v) = u^T E u + v^T E v + u^T E v + v^T E u
# For general E: u^T E v + v^T E u = 2 u^T E_sym v
# So: u^T E_sym v = (1/2)[(u+v)^T E (u+v) - u^T E u - v^T E v]
#                 = (1/2)[f(D,u+v) - f(D,u) - f(D,v)]
# This is ONLY the symmetric part! The full u^T E v has an extra u^T E_anti v.

# So: u^T E v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)] + u^T E_anti v

# Let me verify numerically:
print("  Verifying decomposition...")
verify_ok = True
for trial in range(100):
    D_test = random_SO3()
    u_test = np.random.randn(3)
    v_test = np.random.randn(3)

    E_test = I3 - D_test
    E_sym = (E_test + E_test.T) / 2
    E_anti = (E_test - E_test.T) / 2

    lhs = u_test @ E_test @ v_test
    rhs = 0.5*(f(D_test, u_test + v_test) - f(D_test, u_test) - f(D_test, v_test)) + u_test @ E_anti @ v_test

    if abs(lhs - rhs) > 1e-10:
        verify_ok = False
        print(f"  MISMATCH: {lhs:.10f} vs {rhs:.10f}")

print(f"  Decomposition verified: {verify_ok}")

# Now: delta_total = sum 2 u^T E v = sum [f(D,u+v) - f(D,u) - f(D,v)] + sum 2 u^T E_anti v
#
# The first sum is "symmetric delta": >= -sum[f(D,u)+f(D,v)] (since f(D,u+v) >= 0)
# The second sum is "antisymmetric delta"
#
# Key question: does the antisymmetric delta HELP or HURT?

print("\n  Antisymmetric delta analysis:")
anti_helps = 0
anti_hurts = 0
for trial in range(5000):
    R = {mu: random_SO3() for mu in range(4)}
    D = {p: random_SO3() for p in PAIRS}
    T = random_T_in_V()

    delta_sym = 0.0
    delta_anti = 0.0
    for mu, nu in PAIRS:
        u = R[mu].T @ T[mu] - T[nu]
        v = T[mu] - R[nu].T @ T[nu]
        E = I3 - D[(mu,nu)]
        E_anti = (E - E.T) / 2

        delta_sym += f(D[(mu,nu)], u + v) - f(D[(mu,nu)], u) - f(D[(mu,nu)], v)
        delta_anti += 2 * u @ E_anti @ v

    if delta_anti > 1e-10:
        anti_helps += 1
    elif delta_anti < -1e-10:
        anti_hurts += 1

print(f"  Anti helps (positive): {anti_helps}/5000")
print(f"  Anti hurts (negative): {anti_hurts}/5000")
print(f"  Anti neutral: {5000 - anti_helps - anti_hurts}/5000")
print(f"  [If roughly 50/50, antisymmetric part is signed and averages out]")
