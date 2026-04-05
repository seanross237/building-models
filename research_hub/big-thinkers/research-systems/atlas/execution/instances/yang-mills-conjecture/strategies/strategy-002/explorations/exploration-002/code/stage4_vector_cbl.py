"""
Stage 4: Vector Combined Bound Lemma

Key mathematical question: Can the CBL proof structure (factorization -> C-S -> AM-GM)
be extended from scalar (p=q=n) to general vector case (p, q in R^3)?

Vector CBL claim: For A, B in SO(3), D in SO(3), p, q in R^3:
  p^T(I-A)D(I-B^T)q + f(A,p) + f(B,q) >= 0

Proof sketch:
  LHS = p^T(I-A)D(I-B^T)q + p^T(I-A)p + q^T(I-B)q  [note: f(B,q) = q^T(I-B)q]
  |p^T(I-A)D(I-B^T)q| <= ||(I-A^T)p|| * ||(I-B^T)q||  [Cauchy-Schwarz + D orthogonal]
  = sqrt(2f(A,p)) * sqrt(2f(B,q))  [key identity ||(I-M^T)p||^2 = 2f(M,p)]
  <= f(A,p) + f(B,q)  [AM-GM]
  So the cross term is >= -(f(A,p) + f(B,q)), making LHS >= 0.

Then: verify whether the per-plaquette gap G_{mu,nu} can be written as
  G_{mu,nu} = [Vector CBL term] + correction
  and check if correction >= 0 always.

Also: explore whether G_{mu,nu} has the structure from the GOAL.md hint.
"""

import numpy as np

np.random.seed(456)
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

def f_vec(R, p):
    """f(R,p) = p^T(I-R)p >= 0 for R in SO(3)."""
    return float(p @ p - p @ R @ p)

def vcbl(A, B, D, p, q):
    """
    Vector CBL term: p^T(I-A)D(I-B^T)q + f(A,p) + f(B,q)
    Should always be >= 0 if the vector CBL holds.
    Note: f(B,q) = q^T(I-B)q (using B, not B^T)
    """
    cross = float(p @ (np.eye(3)-A) @ D @ (np.eye(3)-B.T) @ q)
    return cross + f_vec(A, p) + f_vec(B, q)

def random_constrained_T():
    T = np.random.randn(4, 3)
    T -= T.mean(axis=0)
    return T

# ============================================================
# TEST 0: Verify the key identity ||(I-M^T)p||^2 = 2f(M,p)
# ============================================================
print("=" * 70)
print("TEST 0: Key identity ||(I-M^T)p||^2 = 2f(M,p) for M in SO(3)")
print("=" * 70)

max_err = 0
for _ in range(100000):
    M = random_so3()
    p = np.random.randn(3)
    lhs = np.dot((np.eye(3) - M.T) @ p, (np.eye(3) - M.T) @ p)
    rhs = 2 * f_vec(M, p)
    max_err = max(max_err, abs(lhs - rhs))

print(f"  Max ||(I-M^T)p||^2 - 2f(M,p)|: {max_err:.2e}")
print(f"  Identity VERIFIED: {max_err < 1e-10}")

# ============================================================
# TEST 1: Vector CBL >= 0 for arbitrary A, B, D, p, q
# ============================================================
print("\n" + "=" * 70)
print("TEST 1: Vector CBL: p^T(I-A)D(I-B^T)q + f(A,p) + f(B,q) >= 0")
print("=" * 70)

N_tests = 200000
min_vcbl = float('inf')
violations = 0

for _ in range(N_tests):
    A = random_so3()
    B = random_so3()
    D = random_so3()
    p = np.random.randn(3)
    q = np.random.randn(3)

    val = vcbl(A, B, D, p, q)
    if val < min_vcbl:
        min_vcbl = val
    if val < -1e-10:
        violations += 1

print(f"  N tests: {N_tests}")
print(f"  Min value: {min_vcbl:.8f}")
print(f"  Violations (< -1e-10): {violations}")
print(f"  Vector CBL HOLDS: {min_vcbl >= -1e-10}")

# ============================================================
# TEST 2: Cauchy-Schwarz bound: |cross| <= 2*sqrt(f(A,p)*f(B,q))
# ============================================================
print("\n" + "=" * 70)
print("TEST 2: C-S bound: |cross term| <= 2*sqrt(f(A,p)*f(B,q))")
print("=" * 70)

max_ratio = 0
violations_cs = 0
for _ in range(100000):
    A = random_so3()
    B = random_so3()
    D = random_so3()
    p = np.random.randn(3)
    q = np.random.randn(3)

    cross = abs(float(p @ (np.eye(3)-A) @ D @ (np.eye(3)-B.T) @ q))
    bound = 2 * np.sqrt(f_vec(A, p) * f_vec(B, q))

    if cross > bound + 1e-10:
        violations_cs += 1
    if bound > 1e-12:
        ratio = cross / bound
        max_ratio = max(max_ratio, ratio)

print(f"  C-S violations: {violations_cs}")
print(f"  Max |cross| / bound: {max_ratio:.6f} (need <= 1)")
print(f"  C-S bound VERIFIED: {violations_cs == 0}")

# ============================================================
# TEST 3: Per-plaquette check: G_{mu,nu} = VCB + correction?
# ============================================================
print("\n" + "=" * 70)
print("TEST 3: Per-plaquette analysis")
print("  G_{mu,nu} = 2f(U,p) + 2f(W,q) - 2p^T C q")
print("  VCB = p^T(I-R_mu)D(I-R_nu)q + f(R_mu,p) + f(R_nu,q)")
print("  correction = G - VCB")
print("  Q: Is correction always >= 0?")
print("=" * 70)

N_tests = 50000
min_G = float('inf')
min_VCB = float('inf')
min_correction = float('inf')
G_violations = 0
VCB_violations = 0
correction_violations = 0
correction_data = []

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D_mat[(mu,nu)].T) + (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T)

        # Per-plaquette gap
        G = 2*f_vec(U, p) + 2*f_vec(W, q) - 2 * float(p @ C @ q)

        # Vector CBL with A=R_mu, B=R_nu, D=D_{mu,nu}
        VCB = float(p @ (np.eye(3) - R[mu]) @ D_mat[(mu,nu)] @ (np.eye(3) - R[nu]) @ q) + f_vec(R[mu], p) + f_vec(R[nu], q)

        correction = G - VCB

        min_G = min(min_G, G)
        min_VCB = min(min_VCB, VCB)
        min_correction = min(min_correction, correction)
        if G < -1e-10:
            G_violations += 1
        if VCB < -1e-10:
            VCB_violations += 1
        if correction < -1e-10:
            correction_violations += 1
        correction_data.append(correction)

print(f"  N (Q,T,plaquette) triples: {N_tests * len(PLANES)}")
print(f"  G per-plaquette violations (< 0): {G_violations}")
print(f"  VCB violations (< 0): {VCB_violations}")
print(f"  correction violations (< 0): {correction_violations}")
print(f"  Min G: {min_G:.4f}")
print(f"  Min VCB: {min_VCB:.8f}")
print(f"  Min correction: {min_correction:.4f}")
print(f"  Max correction: {max(correction_data):.4f}")
print(f"\n  Conclusion: VCB >= 0 always: {VCB_violations == 0}")
print(f"  Conclusion: per-plaquette G >= VCB (correction >= 0): {correction_violations == 0}")

# ============================================================
# TEST 4: Total gap vs sum of VCBs
# ============================================================
print("\n" + "=" * 70)
print("TEST 4: Total gap vs sum of per-plaquette VCBs")
print("  total_gap = sum_plaq G_{mu,nu}")
print("  sum_VCB = sum_plaq VCB_{mu,nu}")
print("  Q: Is total_gap >= sum_VCB always? (if so, sum_VCB >= 0 gives the proof)")
print("=" * 70)

def make_projector():
    V = np.zeros((12, 9))
    idx = 0
    for mu in range(3):
        for a in range(3):
            v = np.zeros(12)
            v[3*mu + a] = 1.0
            v[3*3 + a] = -1.0
            V[:, idx] = v
            idx += 1
    Q_mat, _ = np.linalg.qr(V)
    return Q_mat[:, :9]

P_V = make_projector()

N_tests = 20000
min_gap = float('inf')
min_sum_VCB = float('inf')
min_gap_minus_sum_VCB = float('inf')
gap_violations = 0
sum_VCB_violations = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    total_gap = 0
    sum_VCB = 0
    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D_mat[(mu,nu)].T) + (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T)

        G = 2*f_vec(U, p) + 2*f_vec(W, q) - 2 * float(p @ C @ q)
        VCB = float(p @ (np.eye(3) - R[mu]) @ D_mat[(mu,nu)] @ (np.eye(3) - R[nu]) @ q) + f_vec(R[mu], p) + f_vec(R[nu], q)

        total_gap += G
        sum_VCB += VCB

    norm2 = np.sum(T**2)
    total_gap_scaled = total_gap  # this is 16||T||^2 - F_x

    min_gap = min(min_gap, total_gap)
    min_sum_VCB = min(min_sum_VCB, sum_VCB)
    min_gap_minus_sum_VCB = min(min_gap_minus_sum_VCB, total_gap - sum_VCB)
    if total_gap < -1e-10:
        gap_violations += 1
    if sum_VCB < -1e-10:
        sum_VCB_violations += 1

print(f"  N tests: {N_tests}")
print(f"  total_gap violations (< 0): {gap_violations}")
print(f"  sum_VCB violations (< 0): {sum_VCB_violations}")
print(f"  Min total_gap: {min_gap:.6f}")
print(f"  Min sum_VCB: {min_sum_VCB:.6f}")
print(f"  Min (gap - sum_VCB): {min_gap_minus_sum_VCB:.4f}")

# ============================================================
# TEST 5: Algebraic identity — decompose sum_VCB
# ============================================================
print("\n" + "=" * 70)
print("TEST 5: Algebraic identity for sum_VCB")
print("  sum_VCB = sum_plaq [p^T(I-R_mu)D(I-R_nu)q + f(R_mu,p) + f(R_nu,q)]")
print("  Claim: sum_{mu<nu} [f(R_mu,T_mu) + f(R_nu,T_nu)] = 3 * sum_mu f(R_mu, T_mu)")
print("  (each direction appears in 3 plaquettes)")
print("=" * 70)

N_tests = 10000
max_err = 0
for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    T = random_constrained_T()

    # LHS: sum over plaquettes
    lhs = 0
    for mu, nu in PLANES:
        lhs += f_vec(R[mu], T[mu]) + f_vec(R[nu], T[nu])

    # RHS: 3 * sum_mu f(R_mu, T_mu)
    rhs = 3 * sum(f_vec(R[mu], T[mu]) for mu in range(4))

    max_err = max(max_err, abs(lhs - rhs))

print(f"  Max error: {max_err:.2e}")
print(f"  Identity holds: {max_err < 1e-10}")
print(f"\n  So sum_VCB = cross_part + 3 * sum_mu f(R_mu, T_mu)")
print(f"  where cross_part = sum_plaq p^T(I-R_mu)D(I-R_nu)q")

# ============================================================
# TEST 6: Key algebraic claim from Stage 3 partial result
# ============================================================
print("\n" + "=" * 70)
print("TEST 6: Verify key decomposition")
print("  cross = 2*sum_mu f(R_mu,T_mu) + cross_D + cross_RDR")
print("  where cross_D = sum_{mu<nu} (-2) T_mu^T (I-D^T) T_nu")
print("        cross_RDR = sum_{mu<nu} (-2) T_mu^T (I-R_mu D R_nu^T) T_nu")
print("=" * 70)

max_err = 0
for _ in range(10000):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    # Direct cross computation
    cross_direct = 0
    for mu, nu in PLANES:
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D_mat[(mu,nu)].T) + (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T)
        cross_direct += -2 * float(T[mu] @ C @ T[nu])

    # Decomposed
    term1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    term_D = sum(-2 * float(T[mu] @ (np.eye(3) - D_mat[(mu,nu)].T) @ T[nu]) for mu, nu in PLANES)
    term_RDR = sum(-2 * float(T[mu] @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ T[nu]) for mu, nu in PLANES)
    cross_decomp = term1 + term_D + term_RDR

    max_err = max(max_err, abs(cross_direct - cross_decomp))

print(f"  Max decomposition error: {max_err:.2e}")
print(f"  Decomposition VERIFIED: {max_err < 1e-10}")

# Now check signs of each component
print("\n  Sign statistics (from 1000 random (Q,T) pairs):")
term1_vals, term_D_vals, term_RDR_vals = [], [], []

for _ in range(1000):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()
    T = T / np.linalg.norm(T)  # normalize

    t1 = 2 * sum(f_vec(R[mu], T[mu]) for mu in range(4))
    tD = sum(-2 * float(T[mu] @ (np.eye(3) - D_mat[(mu,nu)].T) @ T[nu]) for mu, nu in PLANES)
    tRDR = sum(-2 * float(T[mu] @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ T[nu]) for mu, nu in PLANES)
    term1_vals.append(t1)
    term_D_vals.append(tD)
    term_RDR_vals.append(tRDR)

t1_arr = np.array(term1_vals)
tD_arr = np.array(term_D_vals)
tRDR_arr = np.array(term_RDR_vals)
print(f"  term1 = 2*sum f(R_mu): min={t1_arr.min():.4f}, max={t1_arr.max():.4f}, "
      f"frac<0={np.mean(t1_arr<0):.3f}")
print(f"  term_D: min={tD_arr.min():.4f}, max={tD_arr.max():.4f}, frac<0={np.mean(tD_arr<0):.3f}")
print(f"  term_RDR: min={tRDR_arr.min():.4f}, max={tRDR_arr.max():.4f}, frac<0={np.mean(tRDR_arr<0):.3f}")

# ============================================================
# TEST 7: Can the D-terms be bounded by f_same?
# ============================================================
print("\n" + "=" * 70)
print("TEST 7: Bound for cross_D + cross_RDR relative to f_same")
print("  Q: Is f_same + cross_D + cross_RDR >= 0 always?")
print("  (This would give gap = term1 + f_same + cross_D + cross_RDR >= 0)")
print("=" * 70)

N_tests = 20000
min_combined = float('inf')
violations = 0
for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    f_same = 0
    for mu, nu in PLANES:
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        f_same += 2*f_vec(U, T[mu]) + 2*f_vec(W, T[nu])

    cross_D = sum(-2 * float(T[mu] @ (np.eye(3) - D_mat[(mu,nu)].T) @ T[nu]) for mu, nu in PLANES)
    cross_RDR = sum(-2 * float(T[mu] @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ T[nu]) for mu, nu in PLANES)

    combined = f_same + cross_D + cross_RDR
    if combined < min_combined:
        min_combined = combined
    if combined < -1e-10:
        violations += 1

print(f"  N tests: {N_tests}")
print(f"  Min f_same + cross_D + cross_RDR: {min_combined:.6f}")
print(f"  Violations (< 0): {violations}")
print(f"  Bound holds: {violations == 0}")

# ============================================================
# TEST 8: Apply CBL to D-terms using the budget identity
# ============================================================
print("\n" + "=" * 70)
print("TEST 8: Apply vector CBL to D-related terms")
print("  Try: cross_D + cross_RDR + f_same >= 0?")
print("  by vector CBL applied to D_{mu,nu} terms individually")
print("=" * 70)

# For each plaquette (mu,nu), the D-related contribution to the gap is:
# f_same_part = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu)
# cross_D_part = -2 T_mu^T (I-D^T) T_nu
# cross_RDR_part = -2 T_mu^T (I-R_mu D R_nu^T) T_nu
#
# Together: 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu
# = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(2I - D^T - R_mu D R_nu^T)T_nu

# Try vector CBL with A=R_mu D, B=D R_nu^T (= W), D_middle = I:
# VCB_2 = p^T(I-U)I(I-W^T)q + f(U,p) + f(W,q)
# = p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)
# = f(U,p) + f(W,q) + p^T(I-U)(I-W^T)q

# And the D contribution: 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(I-D^T)T_nu - 2T_mu^T(I-R_mu D R_nu^T)T_nu
# Let's compute and compare.

N_tests = 30000
min_vcb2 = float('inf')
vcb2_violations = 0
min_correction2 = float('inf')
correction2_violations = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T

        # D-related contribution per plaquette
        cross_D_p = -2 * float(p @ (np.eye(3) - D_mat[(mu,nu)].T) @ q)
        cross_RDR_p = -2 * float(p @ (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T) @ q)
        D_contrib = 2*f_vec(U, p) + 2*f_vec(W, q) + cross_D_p + cross_RDR_p

        # Vector CBL with A=U, B=W, D_inner=I (i.e., p^T(I-U)(I-W^T)q + f(U,p) + f(W,q))
        VCB_2 = float(p @ (np.eye(3) - U) @ (np.eye(3) - W.T) @ q) + f_vec(U, p) + f_vec(W, q)

        correction2 = D_contrib - VCB_2

        min_vcb2 = min(min_vcb2, VCB_2)
        min_correction2 = min(min_correction2, correction2)
        if VCB_2 < -1e-10:
            vcb2_violations += 1
        if correction2 < -1e-10:
            correction2_violations += 1

print(f"  VCB_2 = p^T(I-U)(I-W^T)q + f(U,p) + f(W,q):")
print(f"    Min: {min_vcb2:.8f}, violations: {vcb2_violations}")
print(f"  correction2 = D_contrib - VCB_2:")
print(f"    Min: {min_correction2:.6f}, violations: {correction2_violations}")

# If correction2 can be negative, try another decomposition
print(f"\n  Is D_contrib >= VCB_2 always: {correction2_violations == 0}")

# ============================================================
# TEST 9: Direct factorization test
# ============================================================
print("\n" + "=" * 70)
print("TEST 9: Test if G_{mu,nu} = VCB_{mu,nu} + VCB'_{mu,nu} for some other VCB'")
print("  VCB' = p^T(I-A')D'(I-B'^T)q + f(A',p) + f(B',q)")
print("  Try A' = U, B' = W, D' = I (i.e., A'D' = U, D'B'^T = W)")
print("=" * 70)

# The per-plaquette gap G = 2f(U,p) + 2f(W,q) - 2p^T C q
# where C = (I-R_mu) + (I-R_nu^T) + (I-D^T) + (I-R_mu D R_nu^T)
#
# Claim: G = VCB_1 + VCB_2 + correction
# where VCB_1 = p^T(I-R_mu)D(I-R_nu)q + f(R_mu,p) + f(R_nu,q)  (tested in TEST 3)
#       VCB_2 = p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)  (tested in TEST 8)
# and correction might be >= 0

# Actually: VCB_1 + VCB_2
# = [p^T(I-R_mu)D(I-R_nu)q + f(R_mu,p) + f(R_nu,q)] + [p^T(I-U)(I-W^T)q + f(U,p) + f(W,q)]

N_tests = 20000
min_G2 = float('inf')
min_VCB12 = float('inf')
min_correction12 = float('inf')
G2_violations = 0
VCB12_violations = 0
correction12_violations = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D_mat[(mu,nu)].T) + (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T)

        G = 2*f_vec(U, p) + 2*f_vec(W, q) - 2 * float(p @ C @ q)

        VCB1 = float(p @ (np.eye(3)-R[mu]) @ D_mat[(mu,nu)] @ (np.eye(3)-R[nu]) @ q) + f_vec(R[mu], p) + f_vec(R[nu], q)
        VCB2 = float(p @ (np.eye(3)-U) @ (np.eye(3)-W.T) @ q) + f_vec(U, p) + f_vec(W, q)
        VCB12 = VCB1 + VCB2
        correction12 = G - VCB12

        min_G2 = min(min_G2, G)
        min_VCB12 = min(min_VCB12, VCB12)
        min_correction12 = min(min_correction12, correction12)
        if G < -1e-10:
            G2_violations += 1
        if VCB12 < -1e-10:
            VCB12_violations += 1
        if correction12 < -1e-10:
            correction12_violations += 1

print(f"  G per-plaquette violations: {G2_violations}")
print(f"  VCB1+VCB2 violations: {VCB12_violations}")
print(f"  correction12 = G - VCB1 - VCB2 violations: {correction12_violations}")
print(f"  Min correction12: {min_correction12:.4f}")
print(f"\n  G >= VCB1+VCB2 always: {correction12_violations == 0}")

# ============================================================
# TEST 10: Try the total sum CBL approach
# ============================================================
print("\n" + "=" * 70)
print("TEST 10: Total sum of VCBs vs total gap")
print("  sum_total_VCB = sum_plaq [VCB1 + VCB2]")
print("  Q: Is total_gap >= sum_total_VCB always?")
print("=" * 70)

N_tests = 20000
min_total_gap = float('inf')
min_sum_VCB12 = float('inf')
min_diff = float('inf')
total_gap_violations = 0
sum_VCB12_violations = 0
diff_violations = 0

for _ in range(N_tests):
    R = [random_so3() for _ in range(d)]
    D_mat = {p: random_so3() for p in PLANES}
    T = random_constrained_T()

    total_gap = 0
    sum_VCB12 = 0
    for mu, nu in PLANES:
        p = T[mu]
        q = T[nu]
        U = R[mu] @ D_mat[(mu, nu)]
        W = D_mat[(mu, nu)] @ R[nu].T
        C = (np.eye(3) - R[mu]) + (np.eye(3) - R[nu].T) + (np.eye(3) - D_mat[(mu,nu)].T) + (np.eye(3) - R[mu] @ D_mat[(mu,nu)] @ R[nu].T)

        G = 2*f_vec(U, p) + 2*f_vec(W, q) - 2 * float(p @ C @ q)
        VCB1 = float(p @ (np.eye(3)-R[mu]) @ D_mat[(mu,nu)] @ (np.eye(3)-R[nu]) @ q) + f_vec(R[mu], p) + f_vec(R[nu], q)
        VCB2 = float(p @ (np.eye(3)-U) @ (np.eye(3)-W.T) @ q) + f_vec(U, p) + f_vec(W, q)

        total_gap += G
        sum_VCB12 += VCB1 + VCB2

    min_total_gap = min(min_total_gap, total_gap)
    min_sum_VCB12 = min(min_sum_VCB12, sum_VCB12)
    min_diff = min(min_diff, total_gap - sum_VCB12)
    if total_gap < -1e-10:
        total_gap_violations += 1
    if sum_VCB12 < -1e-10:
        sum_VCB12_violations += 1
    if total_gap - sum_VCB12 < -1e-10:
        diff_violations += 1

print(f"  total_gap violations: {total_gap_violations}")
print(f"  sum_VCB12 violations: {sum_VCB12_violations}")
print(f"  (total_gap - sum_VCB12) violations: {diff_violations}")
print(f"  Min total_gap: {min_total_gap:.6f}")
print(f"  Min sum_VCB12: {min_sum_VCB12:.6f}")
print(f"  Min diff: {min_diff:.4f}")
print(f"\n  Bound proof via sum_VCB12 >= 0: {sum_VCB12_violations == 0}")

print("\n=== STAGE 4 COMPLETE ===")
