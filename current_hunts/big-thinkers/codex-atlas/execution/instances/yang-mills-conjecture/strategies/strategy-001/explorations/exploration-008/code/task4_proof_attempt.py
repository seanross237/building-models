"""
Task 4: PROOF ATTEMPT for the full 9D bound.

Strategy: Show that for ALL T with Sum_mu T_mu = 0 and ALL R, D in SO(3):

  16||T||^2 - F_x(T) >= 0

APPROACH: Extend E006 combined bound to general T using Cauchy-Schwarz.

KEY INSIGHT: The gap decomposes as:
  gap = f_same + cross
where f_same >= 0 always and |cross| is bounded by Cauchy-Schwarz applied
to the PSD matrices (I-R).

If we can show |cross| <= f_same, the proof is complete.
"""

import numpy as np

np.random.seed(42)
d = 4
PLANES = [(mu, nu) for mu in range(d) for nu in range(mu+1, d)]

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_exp(omega):
    angle = np.linalg.norm(omega)
    if angle < 1e-14:
        return np.eye(3)
    axis = omega / angle
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

def f_vec(R, p):
    """f(R, p) = p^T (I - R) p >= 0 for R in SO(3)."""
    return np.dot(p, p) - np.dot(p, R @ p)

def compute_B(R, D, T, mu, nu):
    S = np.eye(3) + R[mu] @ D[(mu,nu)]
    Tmat = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
    return S @ T[mu] - Tmat @ T[nu]

def random_constrained_T():
    T = np.random.randn(4, 3)
    T[3] = -(T[0] + T[1] + T[2])
    return T

# ============================================================
# PART A: Cauchy-Schwarz bound on cross terms
# ============================================================
print("=" * 70)
print("PART A: Cauchy-Schwarz bound on individual cross terms")
print("=" * 70)

# For a PSD matrix P = I - R (symmetric part is PSD for R in SO(3)):
# |T_mu^T P T_nu| <= sqrt(T_mu^T P T_mu) * sqrt(T_nu^T P T_nu)
#                  = sqrt(f(R, T_mu)) * sqrt(f(R, T_nu))
#
# But we need to be careful: (I-R) is NOT PSD in general for R in SO(3).
# Its symmetric part (I-R+R^T-I)/2... wait, (I-R) has symmetric part (2I-R-R^T)/2 = I - (R+R^T)/2.
# For R in SO(3) with eigenvalues 1, e^{itheta}, e^{-itheta}:
# (R+R^T)/2 has eigenvalues 1, cos(theta), cos(theta).
# So I - (R+R^T)/2 has eigenvalues 0, 1-cos(theta), 1-cos(theta). All >= 0. PSD!
#
# But (I-R) also has a skew-symmetric part: -(R-R^T)/2.
# T_mu^T (I-R) T_nu = T_mu^T [(I-R)_sym + (I-R)_skew] T_nu
# = T_mu^T (I-R)_sym T_nu + T_mu^T (I-R)_skew T_nu
#
# The PSD part gives |T_mu^T P_sym T_nu| <= sqrt(f(P_sym,T_mu)) sqrt(f(P_sym,T_nu))
# = sqrt(f(R,T_mu)) sqrt(f(R,T_nu)) since f(R,p) = p^T P_sym p.
#
# But the skew part T_mu^T Q T_nu (Q skew) satisfies |Q T_nu| = |Q_skew T_nu|
# bounded by ||Q_skew|| |T_nu|. The operator norm of Q_skew is sin(theta).

# More precisely: for unit n, |(I-R)n|^2 = 2 - 2 cos(angle(R,n))... hmm, let me compute directly.

# For R in SO(3) with rotation angle theta about axis k:
# (I-R)p = p - Rp. |(I-R)p|^2 = 2|p|^2 - 2 p^T R p = 2f(R,p).
# So |(I-R)p| = sqrt(2 f(R,p)).

# Cauchy-Schwarz: |p^T (I-R) q| = |(I-R^T)p . q| = |(I-R)^T p . q|
# = |((I-R)p) . q| <= |(I-R)p| |q| = sqrt(2f(R,p)) |q|
#
# But also: |p^T (I-R) q| <= |p| |(I-R)q| = |p| sqrt(2f(R,q))
#
# Tighter: |p^T (I-R) q| <= |(I-R)p| |(I-R)q| / ... no, that's not right.
#
# Actually, (I-R) is NOT symmetric, so p^T(I-R)q != q^T(I-R)p in general.
# We have: p^T(I-R)q = p.q - p^T R q.
# And: |p^T R q| <= |p||q| (since R is orthogonal).
# So |p^T(I-R)q| <= |p.q| + |p^T R q| <= 2|p||q|. (very weak)
#
# Better: |p^T(I-R)q| = |((I-R^T)p)^T q| <= |(I-R^T)p| |q| = sqrt(2f(R,p)) |q|.
# (using |x^T y| <= |x||y| and |(I-R^T)p|^2 = 2f(R^T,p) = 2f(R,p))

# For the SYMMETRIC part specifically:
# p^T [(I-R) + (I-R)^T]/2 q = p^T [I - (R+R^T)/2] q
# This IS a PSD quadratic form, so:
# |p^T P_sym q| <= sqrt(p^T P_sym p) sqrt(q^T P_sym q) = sqrt(f(R,p)) sqrt(f(R,q))
# where f(R,p) = p^T P_sym p.

# For the SKEW part:
# p^T [(I-R) - (I-R)^T]/2 q = p^T [-(R-R^T)/2] q = p^T Q q (Q skew)
# |p^T Q q| <= ||Q|| |p||q| = sin(theta) |p||q|

# So total: |p^T(I-R)q| <= sqrt(f(R,p)f(R,q)) + sin(theta)|p||q|

# The sin(theta) term involves the rotation angle, not just the f-values.
# This makes a clean Cauchy-Schwarz bound harder.

# HOWEVER: for the TOTAL cross term, the skew parts might cancel!
# Let's check.

print("\nChecking if skew parts of cross terms cancel in the sum:")

max_skew_fraction = 0
N_tests = 10000
for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    cross_total = 0
    sym_total = 0
    skew_total = 0

    for mu, nu in PLANES:
        for Rot in [R[mu], R[nu].T, D[(mu,nu)].T, (R[mu] @ D[(mu,nu)] @ R[nu].T)]:
            P = np.eye(3) - Rot
            P_sym = (P + P.T) / 2
            P_skew = (P - P.T) / 2
            c_sym = np.dot(T[mu], P_sym @ T[nu])
            c_skew = np.dot(T[mu], P_skew @ T[nu])
            sym_total += c_sym
            skew_total += c_skew
            cross_total += c_sym + c_skew

    if abs(cross_total) > 1e-12:
        skew_frac = abs(skew_total) / abs(cross_total) if abs(cross_total) > 1e-12 else 0
        max_skew_fraction = max(max_skew_fraction, abs(skew_total) / (abs(sym_total) + 1e-15))

print(f"  Max |skew_total|/|sym_total|: {max_skew_fraction:.6f}")

# ============================================================
# PART B: Tighter bound using ONLY symmetric part + AM-GM
# ============================================================
print("\n" + "=" * 70)
print("PART B: Bound using symmetric Cauchy-Schwarz")
print("=" * 70)

# For the symmetric part: |p^T P_sym q| <= sqrt(f(R,p)) sqrt(f(R,q))
# For the skew part: |p^T P_skew q| <= sin(theta) |p| |q| <= sqrt(2f(R,p)) |q|... hmm
#
# Actually, let me try to bound the FULL cross term directly:
#
# |p^T(I-R)q| = |p.q - p^T R q|
#
# For unit vectors: p.q = cos(angle_pq), p^T R q = ... depends on R.
#
# Better approach: |(I-R)q|^2 = 2f(R,q). So:
# |p^T(I-R)q| <= |p| |(I-R)q| = |p| sqrt(2 f(R,q))
#
# And: |p^T(I-R)q| = |q^T(I-R^T)p| <= |q| sqrt(2 f(R^T,p)) = |q| sqrt(2 f(R,p))
#
# Taking geometric mean: |p^T(I-R)q| <= sqrt(|p| sqrt(2f(R,q)) * |q| sqrt(2f(R,p)))
# = (2)^{1/2} (|p||q| f(R,p) f(R,q))^{1/4}... this is getting messy.
#
# Let me try a DIRECT numerical test: is the cross term bounded by a simple
# multiple of f_same for ALL configurations?

print("\nDirect test: |cross| / f_same ratio over adversarial configs:")

def compute_gap_parts(R, D, T):
    """Compute f_same and cross for given config."""
    f_same = 0
    cross = 0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        W = D[(mu,nu)] @ R[nu].T
        f_same += 2 * f_vec(U, T[mu]) + 2 * f_vec(W, T[nu])

        # Cross term
        for Rot in [R[mu], R[nu].T, D[(mu,nu)].T, R[mu] @ D[(mu,nu)] @ R[nu].T]:
            cross -= 2 * np.dot(T[mu], (np.eye(3) - Rot) @ T[nu])

    return f_same, cross

# Adversarial gradient ascent to MAXIMIZE |cross|/f_same
best_ratio = 0
N_adversarial = 50

for trial in range(N_adversarial):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}
    T = random_constrained_T()
    T_norm = np.sqrt(np.sum(T**2))
    T = T / T_norm  # normalize

    step_size = 0.01
    for iteration in range(300):
        f_same, cross = compute_gap_parts(R, D, T)
        gap = f_same + cross

        if f_same > 1e-12:
            ratio = -cross / f_same
            if ratio > best_ratio:
                best_ratio = ratio

        # Gradient: maximize (-cross/f_same) wrt R, D
        # Approximate: maximize -cross (since f_same changes slowly)
        eps = 1e-5

        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = R.copy(); R_p[mu] = so3_exp(omega) @ R[mu]
                _, cross_p = compute_gap_parts(R_p, D, T)
                g = -(cross_p - cross) / eps  # gradient of -cross
                R[mu] = so3_exp(step_size * g * np.eye(3)[k]) @ R[mu]

        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D); D_p[p] = so3_exp(omega) @ D[p]
                _, cross_p = compute_gap_parts(R, D_p, T)
                g = -(cross_p - cross) / eps
                D[p] = so3_exp(step_size * g * np.eye(3)[k]) @ D[p]

        # Also optimize T (within constraint space)
        for mu in range(3):  # optimize T_0, T_1, T_2 (T_3 is determined)
            for a in range(3):
                T_p = T.copy(); T_p[mu, a] += eps; T_p[3] = -(T_p[0]+T_p[1]+T_p[2])
                T_p /= np.sqrt(np.sum(T_p**2))  # renormalize
                _, cross_p = compute_gap_parts(R, D, T_p)
                f_p, _ = compute_gap_parts(R, D, T_p)
                if f_p > 1e-12:
                    ratio_p = -cross_p / f_p
                else:
                    ratio_p = 0
                g = (ratio_p - (-cross/f_same)) / eps
                T[mu, a] += step_size * g
                T[3] = -(T[0]+T[1]+T[2])
                T /= np.sqrt(np.sum(T**2))

        if iteration > 0 and iteration % 100 == 0:
            step_size *= 0.5

    f_same, cross = compute_gap_parts(R, D, T)
    if f_same > 1e-12:
        final_ratio = -cross / f_same
    else:
        final_ratio = 0

    if trial < 10 or final_ratio > 0.5:
        print(f"  Trial {trial}: -cross/f_same = {final_ratio:.6f}, gap = {f_same+cross:.6f}")

print(f"\n  BEST adversarial ratio |cross|/f_same: {best_ratio:.6f}")
print(f"  Bound gap >= (1 - {best_ratio:.4f}) * f_same >= 0: {best_ratio < 1}")

# ============================================================
# PART C: E006 combined bound for UNIFORM COLOR with general s
# ============================================================
print("\n" + "=" * 70)
print("PART C: E006-style proof for uniform-color modes with general s")
print("=" * 70)

# For uniform-color T_mu = s_mu * n, check if the E006 proof extends.
# The per-plaquette gap for unit n is:
# g_{mu,nu} = 2 s_mu^2 f(U) + 2 s_nu^2 f(V)
#           - 2 s_mu s_nu [f(R_mu) + f(R_nu) + f(D) + f(H)]
#           + share of base-link budget

# At the GLOBAL level:
# G = 2 Sigma [s_mu^2 f(U) + s_nu^2 f(V)] + Sigma s_mu^2 f(R_mu)
#   - 2 Sigma s_mu s_nu [f(D) + f(H)]

# Using the combined bound: for each (mu,nu):
# f(D) + f(H) = f(U) + f(V) - X  where X = n^T(I-R_mu)D(I-R_nu^T)n
# and |X| <= 2 sqrt(f(R_mu) f(R_nu))

# Substituting:
# G = 2 Sigma [(s_mu-s_nu)^2 f(U)] + extra + Sigma s_mu^2 f(R_mu) + 2 Sigma s_mu s_nu X

# Wait, let me be more careful.
# G = 2 Sigma [s_mu^2 f(U) + s_nu^2 f(V) - s_mu s_nu (f(U)+f(V)-X)]
#   + Sigma s_mu^2 f(R_mu)
# = 2 Sigma [(s_mu^2-s_mu s_nu) f(U) + (s_nu^2-s_mu s_nu) f(V)]
#   + 2 Sigma s_mu s_nu X + Sigma s_mu^2 f(R_mu)
# = 2 Sigma [s_mu(s_mu-s_nu) f(U) + s_nu(s_nu-s_mu) f(V)]
#   + 2 Sigma s_mu s_nu X + Sigma s_mu^2 f(R_mu)
# = 2 Sigma (s_mu-s_nu) [s_mu f(U) - s_nu f(V)]
#   + 2 Sigma s_mu s_nu X + Sigma s_mu^2 f(R_mu)

# The first term: 2(s_mu-s_nu)[s_mu f(U) - s_nu f(V)].
# If s_mu = s_nu: this is 0, and f(U), f(V) don't help.
# The second term: 2 s_mu s_nu X where |X| <= 2 sqrt(r_mu r_nu).
# The third term: s_mu^2 f(R_mu) >= 0.

# For hard plaquettes (s_mu s_nu > 0): 2 s_mu s_nu X can be as negative as
# -4 s_mu s_nu sqrt(r_mu r_nu). Need base-link budget to cover this.

# By AM-GM: 4 s_mu s_nu sqrt(r_mu r_nu) <= 2(s_mu^2 r_nu + s_nu^2 r_mu)
# (using 2ab <= a^2 + b^2 with a = s_mu sqrt(r_nu), b = s_nu sqrt(r_mu))

# Wait: 4 s_mu s_nu sqrt(r_mu r_nu) = 4 s_mu s_nu sqrt(r_mu) sqrt(r_nu)
# <= 2(s_mu^2 r_nu + s_nu^2 r_mu)  by AM-GM (since 2xy <= x^2 + y^2 with x = s_mu sqrt(r_nu), y = s_nu sqrt(r_mu))
# Actually: 2 * s_mu sqrt(r_nu) * s_nu sqrt(r_mu) <= s_mu^2 r_nu + s_nu^2 r_mu
# So 4 s_mu s_nu sqrt(r_mu r_nu) = 2 * [2 s_mu s_nu sqrt(r_mu r_nu)]
# = 2 * [s_mu sqrt(r_nu) * s_nu sqrt(r_mu) + s_mu sqrt(r_nu) * s_nu sqrt(r_mu)]
# Hmm, 4xy = 2(2xy) <= 2(x^2+y^2)? No, 2xy <= x^2+y^2, so 4xy <= 2(x^2+y^2).

# So: the worst X contribution per hard plaquette is -4 s_mu s_nu sqrt(r_mu r_nu)
# and this is bounded by 2(s_mu^2 r_nu + s_nu^2 r_mu).

# Total negative from X: sum over all hard plaquettes of 2(s_mu^2 r_nu + s_nu^2 r_mu)
# This needs to be <= total base-link budget = sum_mu s_mu^2 r_mu

# Let's check: total X absorption = sum_{hard} 2(s_mu^2 r_nu + s_nu^2 r_mu)
# vs base-link budget = sum_mu s_mu^2 r_mu

# This depends on the number and weights of hard plaquettes.

# NUMERICAL CHECK: Is the base-link budget SUFFICIENT for all s?

print("Testing if base-link budget covers worst-case X terms:")

N_tests = 10000
budget_sufficient = 0
for trial in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    # Random s perp (1,1,1,1)
    s = np.random.randn(4)
    s -= np.mean(s)  # project perp to (1,1,1,1)
    if np.linalg.norm(s) < 1e-8: continue
    s /= np.linalg.norm(s)

    n = np.random.randn(3); n /= np.linalg.norm(n)

    r = np.array([f_vec(R[mu], n) for mu in range(d)])

    # Base link budget
    base_budget = np.sum(s**2 * r)

    # Worst-case X absorption (using AM-GM bound)
    x_absorption = 0
    for mu, nu in PLANES:
        if s[mu] * s[nu] > 0:  # hard plaquette
            x_absorption += 2 * (s[mu]**2 * r[nu] + s[nu]**2 * r[mu])

    # Also need to account for the first term in G
    first_term = 0
    for mu, nu in PLANES:
        U = R[mu] @ D[(mu,nu)]
        V = D[(mu,nu)] @ R[nu].T
        fU = f_vec(U, n)
        fV = f_vec(V, n)
        first_term += 2 * (s[mu]-s[nu]) * (s[mu]*fU - s[nu]*fV)

    # G = first_term + 2 Sigma s_mu s_nu X + base_budget
    # Worst case: first_term could be positive or negative
    # X contribution: >= -x_absorption (from AM-GM)
    # So G >= first_term - x_absorption + base_budget

    if base_budget >= x_absorption:
        budget_sufficient += 1

print(f"  Base-link budget sufficient: {budget_sufficient}/{N_tests} "
      f"({100*budget_sufficient/N_tests:.1f}%)")

# Now check the FULL gap (including first_term)
print("\nFull gap analysis for uniform-color modes with general s:")
N_tests = 50000
min_gap = float('inf')
max_ratio_per_s = 0

for trial in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    s = np.random.randn(4)
    s -= np.mean(s)
    if np.linalg.norm(s) < 1e-8: continue

    n = np.random.randn(3); n /= np.linalg.norm(n)

    # Compute F_x for T = s*n
    F_x = 0
    for mu, nu in PLANES:
        B = (np.eye(3) + R[mu] @ D[(mu,nu)]) @ (s[mu] * n) - \
            (R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T) @ (s[nu] * n)
        F_x += np.dot(B, B)

    norm2 = np.sum(s**2)
    gap = 16 * norm2 - F_x
    min_gap = min(min_gap, gap)

    ratio = F_x / (16 * norm2)
    max_ratio_per_s = max(max_ratio_per_s, ratio)

    if gap < 0:
        print(f"  *** VIOLATION at trial {trial}: gap = {gap:.6f}")

print(f"  Min gap over {N_tests} tests: {min_gap:.6f} (need >= 0)")
print(f"  Max F_x / (16|s|^2): {max_ratio_per_s:.6f} (need <= 1)")

# ============================================================
# PART D: Definitive adversarial test for general T on M_12
# ============================================================
print("\n" + "=" * 70)
print("PART D: Definitive adversarial test on constrained M_12")
print("=" * 70)

def compute_M12_max_constrained(R, D):
    M12 = np.zeros((12, 12))
    for mu, nu in PLANES:
        S = np.eye(3) + R[mu] @ D[(mu,nu)]
        T = R[mu] + R[mu] @ D[(mu,nu)] @ R[nu].T
        M12[3*mu:3*(mu+1), 3*mu:3*(mu+1)] += S.T @ S
        M12[3*nu:3*(nu+1), 3*nu:3*(nu+1)] += T.T @ T
        M12[3*mu:3*(mu+1), 3*nu:3*(nu+1)] -= S.T @ T
        M12[3*nu:3*(nu+1), 3*mu:3*(mu+1)] -= T.T @ S

    V = np.zeros((12, 9))
    idx = 0
    for i in range(3):
        for a in range(3):
            v = np.zeros(12)
            v[3*i + a] = 1.0
            v[9 + a] = -1.0
            V[:, idx] = v
            idx += 1
    Q_orth, _ = np.linalg.qr(V)
    V_orth = Q_orth[:, :9]
    M_r = V_orth.T @ M12 @ V_orth
    return np.linalg.eigvalsh(M_r)[-1], V_orth, M_r

# More aggressive adversarial search
N_trials = 200
best_eig = 0
converged_values = []

for trial in range(N_trials):
    R = [random_so3() for _ in range(d)]
    D = {p: random_so3() for p in PLANES}

    step_size = 0.03
    for iteration in range(500):
        current, V_orth, M_r = compute_M12_max_constrained(R, D)
        if current > best_eig:
            best_eig = current

        # Gradient
        eps = 1e-5
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = R.copy(); R_p[mu] = so3_exp(omega) @ R[mu]
                e_p, _, _ = compute_M12_max_constrained(R_p, D)
                g = (e_p - current) / eps
                R[mu] = so3_exp(step_size * g * np.eye(3)[k]) @ R[mu]

        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D); D_p[p] = so3_exp(omega) @ D[p]
                e_p, _, _ = compute_M12_max_constrained(R, D_p)
                g = (e_p - current) / eps
                D[p] = so3_exp(step_size * g * np.eye(3)[k]) @ D[p]

        if iteration > 0 and iteration % 100 == 0:
            step_size *= 0.5

    final_eig, _, _ = compute_M12_max_constrained(R, D)
    converged_values.append(final_eig)

    if trial < 10 or final_eig > 15.99:
        print(f"  Trial {trial}: final constrained max eigenvalue = {final_eig:.6f}")

converged_values = np.array(converged_values)
print(f"\nResults over {N_trials} adversarial trials:")
print(f"  Best constrained eigenvalue: {best_eig:.8f}")
print(f"  Mean converged value: {np.mean(converged_values):.6f}")
print(f"  Std: {np.std(converged_values):.6f}")
print(f"  Fraction > 15.99: {np.mean(converged_values > 15.99):.4f}")
print(f"  Fraction > 16.00: {np.mean(converged_values > 16.0):.4f}")
print(f"  BOUND HOLDS: {best_eig <= 16 + 1e-10}")

# ============================================================
# PART E: At the adversarial maximum, what does the gap look like?
# ============================================================
print("\n" + "=" * 70)
print("PART E: Gap structure at adversarial maximum")
print("=" * 70)

# Start from identity and perturb slightly
for trial in range(20):
    # Start closer to identity (where gap is smallest)
    R = [so3_exp(0.3 * np.random.randn(3)) for _ in range(d)]
    D = {p: so3_exp(0.3 * np.random.randn(3)) for p in PLANES}

    step_size = 0.02
    for iteration in range(800):
        current, V_orth, M_r = compute_M12_max_constrained(R, D)

        eps = 1e-5
        for mu in range(d):
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                R_p = R.copy(); R_p[mu] = so3_exp(omega) @ R[mu]
                e_p, _, _ = compute_M12_max_constrained(R_p, D)
                g = (e_p - current) / eps
                R[mu] = so3_exp(step_size * g * np.eye(3)[k]) @ R[mu]

        for p in PLANES:
            for k in range(3):
                omega = np.zeros(3); omega[k] = eps
                D_p = dict(D); D_p[p] = so3_exp(omega) @ D[p]
                e_p, _, _ = compute_M12_max_constrained(R, D_p)
                g = (e_p - current) / eps
                D[p] = so3_exp(step_size * g * np.eye(3)[k]) @ D[p]

        if iteration > 0 and iteration % 200 == 0:
            step_size *= 0.5

    final_eig, V_orth, M_r = compute_M12_max_constrained(R, D)

    # Extract top eigenvector
    eigs, vecs = np.linalg.eigh(M_r)
    top_9d = vecs[:, -1]
    top_12d = V_orth @ top_9d
    T_star = top_12d.reshape(4, 3)

    # Check constraint
    constraint_err = np.linalg.norm(T_star[0]+T_star[1]+T_star[2]+T_star[3])

    # Gap decomposition
    f_same, cross = compute_gap_parts(R, D, T_star)
    gap = 16 * np.sum(T_star**2) - sum(np.dot(compute_B(R, D, T_star, mu, nu),
                                                compute_B(R, D, T_star, mu, nu))
                                        for mu, nu in PLANES)

    # Rank
    sv = np.linalg.svd(T_star, compute_uv=False)
    rank1 = sv[0]**2 / np.sum(sv**2)

    # Check if close to identity
    dist_from_id = sum(np.linalg.norm(R[mu] - np.eye(3), 'fro') for mu in range(d))
    dist_from_id += sum(np.linalg.norm(D[p] - np.eye(3), 'fro') for p in PLANES)

    if trial < 20:
        print(f"  Trial {trial}: eig = {final_eig:.6f}, gap = {gap:.6f}, "
              f"f_same = {f_same:.4f}, cross = {cross:.4f}, "
              f"rank1 = {rank1:.3f}, dist_from_I = {dist_from_id:.3f}")

print("\nDone with Task 4.")
