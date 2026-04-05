"""
Stage 1: Verify sum_S(R, D=I, T) = 0 for all R, T in V.
Then prove it algebraically.
"""
import numpy as np

np.random.seed(42)

def random_SO3():
    """Random SO(3) via QR decomposition of random matrix."""
    A = np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.sign(np.diag(R)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q

def f(M, p):
    """f(M, p) = p^T (I - M) p"""
    return p @ (np.eye(3) - M) @ p

def random_T_in_V():
    """Random T = (T_0,...,T_3) with sum T_mu = 0"""
    T = {mu: np.random.randn(3) for mu in range(3)}
    T[3] = -T[0] - T[1] - T[2]
    return T

def compute_S_munu(R, D, T, mu, nu):
    """S_{mu,nu} per GOAL.md definition."""
    R_mu, R_nu = R[mu], R[nu]
    D_mn = D[(mu, nu)]
    T_mu, T_nu = T[mu], T[nu]

    term1 = 2 * f(R_mu @ D_mn, T_mu)
    term2 = 2 * f(D_mn @ R_nu.T, T_nu)
    C = 2*np.eye(3) - D_mn.T - R_mu @ D_mn @ R_nu.T
    term3 = -2 * T_mu @ C @ T_nu
    return term1 + term2 + term3

PAIRS = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def compute_sum_S(R, D, T):
    return sum(compute_S_munu(R, D, T, mu, nu) for mu, nu in PAIRS)

D_I = {p: np.eye(3) for p in PAIRS}

# ========================
# TEST 1: sum_S(D=I) for 500 random (R, T)
# ========================
print("=" * 60)
print("TEST 1: sum_S(R, D=I, T) for 500 random configs")
print("=" * 60)

vals = []
for _ in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    T = random_T_in_V()
    vals.append(compute_sum_S(R, D_I, T))

vals = np.array(vals)
print(f"  max |sum_S|: {np.max(np.abs(vals)):.2e}")
print(f"  mean:        {np.mean(vals):.2e}")

# ========================
# TEST 2: f(R^T, p) = f(R, p)
# ========================
print("\n" + "=" * 60)
print("TEST 2: f(R^T, p) = f(R, p)")
print("=" * 60)
max_diff = 0
for _ in range(1000):
    R_t = random_SO3()
    p = np.random.randn(3)
    max_diff = max(max_diff, abs(f(R_t.T, p) - f(R_t, p)))
print(f"  max diff: {max_diff:.2e}  [CONFIRMED]")

# ========================
# TEST 3: Decompose into diagonal + cross for one config
# ========================
print("\n" + "=" * 60)
print("TEST 3: Decompose sum_S(D=I)")
print("=" * 60)
R = {mu: random_SO3() for mu in range(4)}
T = random_T_in_V()

direct = compute_sum_S(R, D_I, T)
diag = sum(2*f(R[mu], T[mu]) + 2*f(R[nu], T[nu]) for mu, nu in PAIRS)
cross = sum(-2*T[mu] @ (np.eye(3) - R[mu] @ R[nu].T) @ T[nu] for mu, nu in PAIRS)
print(f"  Direct sum_S: {direct:.6e}")
print(f"  diag:         {diag:.10f}")
print(f"  cross:        {cross:.10f}")
print(f"  diag+cross:   {diag+cross:.6e}")

# So sum_S(D=I) = diag + cross. If direct ≈ 0, then cross ≈ -diag.
# Let me verify the algebra of cross more carefully.
normT = sum(np.dot(T[mu], T[mu]) for mu in range(4))
# cross = -2 sum_{mu<nu} T_mu·T_nu + 2 sum_{mu<nu} T_mu^T R_mu R_nu^T T_nu
cp1 = -2*sum(np.dot(T[mu], T[nu]) for mu, nu in PAIRS)
cp2 = 2*sum(T[mu] @ R[mu] @ R[nu].T @ T[nu] for mu, nu in PAIRS)
print(f"\n  cross_part1 (-2 sum T·T):        {cp1:.10f}")
print(f"  ||T||^2 (should equal cp1):      {normT:.10f}")
print(f"  Match: {abs(cp1 - normT):.2e}")

# Check cp2 = 2 sum (R_mu^T T_mu)·(R_nu^T T_nu)?
cp2_inner = 2*sum(np.dot(R[mu].T @ T[mu], R[nu].T @ T[nu]) for mu, nu in PAIRS)
print(f"\n  cp2 direct:        {cp2:.10f}")
print(f"  cp2 inner product: {cp2_inner:.10f}")
print(f"  Match: {abs(cp2 - cp2_inner):.2e}")

# And 2 sum_{mu<nu} S_mu·S_nu = |sum S|^2 - sum|S|^2 where S_mu = R_mu^T T_mu
S_vecs = [R[mu].T @ T[mu] for mu in range(4)]
sum_S_vec = sum(S_vecs)
sum_Ssq = np.dot(sum_S_vec, sum_S_vec)
sum_norms = sum(np.dot(s,s) for s in S_vecs)
print(f"\n  |sum R^T T|^2 - ||T||^2:  {sum_Ssq - normT:.10f}")
print(f"  cp2:                       {cp2:.10f}")
print(f"  Match: {abs(cp2 - (sum_Ssq - normT)):.2e}")

# So cross = normT + (sum_Ssq - normT) = sum_Ssq
# And diag = 6 sum f(R_mu, T_mu)
print(f"\n  cross = |sum R^T T|^2 = {sum_Ssq:.10f}")
print(f"  diag  = 6 sum f       = {diag:.10f}")
print(f"  Total = {diag + sum_Ssq:.10f}")
print(f"  Direct =               {direct:.10e}")

# DISCREPANCY: formula gives diag + |sum R^T T|^2 but direct gives ~0.
# Let me check if my formula for diag is wrong.
diag_check = 6 * sum(f(R[mu], T[mu]) for mu in range(4))
print(f"\n  diag from pairs:  {diag:.10f}")
print(f"  6*sum_f:          {diag_check:.10f}")
print(f"  Match: {abs(diag - diag_check):.2e}")

# ========================
# TEST 4: The problem must be in compute_S_munu. Let me check the definition against
# the per-plaquette identity differently.
# ========================
print("\n" + "=" * 60)
print("TEST 4: Check per-plaquette at D=I for pair (0,1)")
print("=" * 60)

mu, nu = 0, 1
T_mu, T_nu = T[mu], T[nu]
R_mu, R_nu = R[mu], R[nu]
D_mn = np.eye(3)

# By definition:
# S_{mu,nu} = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2 T_mu^T [2I - D^T - R_mu D R_nu^T] T_nu

# At D=I:
t1 = 2*f(R_mu, T_mu)  # = 2 T_mu^T(I-R_mu)T_mu
t2 = 2*f(R_nu.T, T_nu)  # = 2 T_nu^T(I-R_nu^T)T_nu
C = 2*np.eye(3) - np.eye(3) - R_mu @ R_nu.T  # = I - R_mu R_nu^T
t3 = -2*T_mu @ C @ T_nu

print(f"  t1 = 2f(R_mu, T_mu) = {t1:.10f}")
print(f"  t2 = 2f(R_nu^T, T_nu) = {t2:.10f}")
print(f"  t3 = -2 T_mu^T(I - R_mu R_nu^T)T_nu = {t3:.10f}")
print(f"  S_01 = {t1+t2+t3:.10f}")

# Now let me check: is this the correct definition?
# From the proof chain: "4|T_mu-T_nu|^2 - |B|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2T^T C T"
# And: "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S"

# The per-plaquette identity gives us:
# 4|T_mu-T_nu|^2 - |B_mn|^2 = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2T_mu^T C T_nu
# where C = 2I - D^T - R_mu D R_nu^T

# Summing over all pairs:
# 16||T||^2 - F = sum_{mu<nu} [2f(R_mu D_mn, T_mu) + 2f(D_mn R_nu^T, T_nu) - 2T_mu^T C_mn T_nu]

# Now the claim is this equals 2*sum_mu f(R_mu, T_mu) + sum_S.
# So sum_S = sum_{mu<nu} [2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2T^T C T] - 2 sum_mu f(R_mu, T_mu)

# WAIT. This means sum_S is NOT equal to sum_{mu<nu} S_{mu,nu} where S_{mu,nu} is the
# per-plaquette expression. Instead, 2*sum_mu f(R_mu, T_mu) has been EXTRACTED.

# But the GOAL says:
# "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S [VERIFIED]"
# "sum_S = sum_{mu<nu} S_{mu,nu} where S_{mu,nu} = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2T^T C T"
# So the GOAL defines S_{mu,nu} as the FULL per-plaquette expression, and claims
# sum of those = 2 sum f(R_mu, T_mu) + sum_S.
# That makes sum_S = sum S_{mu,nu} - 2 sum f.

# NO WAIT. Re-reading: it says sum_S = sum_{mu<nu} S_{mu,nu}, AND SEPARATELY,
# 16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S.
# So sum S_{mu,nu} (with the cross term) PLUS 2 sum f = 16||T||^2 - F_x.
# But 16||T||^2 - F_x also = sum per-plaquette = sum [2f(U,T_mu) + 2f(W,T_nu) - 2T^TC T].

# This means: sum [2f(U,T_mu) + 2f(W,T_nu) - 2T^TC T] = 2 sum f(R_mu, T_mu) + sum_S
# where sum_S = sum S_{mu,nu} = sum [2f(U,T_mu) + 2f(W,T_nu) - 2T^T C T].
# That's circular! Unless S_{mu,nu} is defined differently from the per-plaquette expression.

# Let me re-read the GOAL very carefully.
# "sum_S = sum_{mu<nu} S_{mu,nu} where:
#  S_{mu,nu} = 2f(R_mu D_{mu,nu}, T_mu) + 2f(D_{mu,nu} R_nu^T, T_nu)
#              - 2 T_mu^T [2I - D_{mu,nu}^T - R_mu D_{mu,nu} R_nu^T] T_nu"

# And "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S"

# So this says that: sum_{mu<nu} [full per-plaquette] = 2 sum f + sum_S
# Which means sum_S = sum_{mu<nu} S_{mu,nu} where S_{mu,nu} is defined DIFFERENTLY
# from the per-plaquette expression, and the 2 sum f is extracted.

# But the GOAL literally defines S_{mu,nu} = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2T^T C T.
# This IS the per-plaquette expression. So:
# sum S_{mu,nu} = 2 sum f(R_mu, T_mu) + sum_S  with sum_S = sum S_{mu,nu}
# means 2 sum f = 0? No, that can't be right.

# THERE IS A SUBTLE POINT. Let me recheck.
# The per-plaquette identity is:
# 4|T_mu - T_nu|^2 - |B_mn|^2 = 2f(U, T_mu) + 2f(W, T_nu) - 2T_mu^T C T_nu
# where U and W involve D.

# To extract 2 sum f(R_mu, T_mu):
# Note f(R_mu D, T_mu) = f(R_mu, T_mu) + [f(R_mu D, T_mu) - f(R_mu, T_mu)]
# = f(R_mu, T_mu) + T_mu^T [R_mu - R_mu D] T_mu  = f(R_mu, T_mu) + T_mu^T R_mu(I-D) T_mu

# Similarly f(D R_nu^T, T_nu) = f(R_nu^T, T_nu) + T_nu^T [R_nu^T - D R_nu^T] T_nu
# = f(R_nu, T_nu) + T_nu^T (I-D) R_nu^T T_nu

# So per-plaquette = 2[f(R_mu) + T_mu^T R_mu(I-D) T_mu] + 2[f(R_nu) + T_nu^T(I-D)R_nu^T T_nu] - 2T^T C T
# = 2f(R_mu) + 2f(R_nu) + [2 T_mu^T R_mu(I-D) T_mu + 2 T_nu^T(I-D)R_nu^T T_nu - 2T^T C T]

# Summing: sum [2f(R_mu) + 2f(R_nu)] = 6 sum f(R_mu, T_mu) as before.
# Wait, but the GOAL says "2*sum_mu f(R_mu, T_mu)" is extracted, not 6!

# Hmm. Let me re-read one more time.
# "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S [VERIFIED to 5.7e-14]"
# So the claim is: sum of per-plaquette = 2 sum_mu f + sum_S,
# where sum_S = sum S_{mu,nu} as defined.

# If sum of per-plaquette = sum S_{mu,nu} by definition, then 2 sum f = 0, contradiction.
# So S_{mu,nu} must NOT be the full per-plaquette expression!

# Maybe the definition has a SUBTRACTION already built in:
# S_{mu,nu} = [full per-plaquette] - [some diagonal contribution]
# such that sum of those diagonal contributions = 2 sum f.

# But the GOAL literally gives:
# S_{mu,nu} = 2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu) - 2T^T [2I-D^T-R_mu D R_nu^T] T_nu
# which IS the full per-plaquette (2f(U) + 2f(W) - 2T^T C T).

# I think the resolution is:
# "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S" is an identity where
# the LHS has been REWRITTEN. The "2*sum_mu f" is the R-only contribution and
# "sum_S" is everything else. So sum_S ≠ sum S_{mu,nu}, rather:
# sum_S = 16||T||^2 - F_x - 2*sum_mu f(R_mu, T_mu)
# = sum_{mu<nu} [per-plaquette] - 2 sum_mu f(R_mu, T_mu)

# So: my compute_S_munu is computing the FULL per-plaquette, but sum_S as defined
# in the extraction identity is sum_{mu<nu} S_{mu,nu} - 2 sum f.
# Or equivalently, the "S_{mu,nu}" in the extraction is NOT the per-plaquette but
# has the diagonal subtracted.

# BOTTOM LINE: I need to check what the actual definition is. Let me look at E003.

# For now, let me test the hypothesis that sum_S = sum[per-plaquette] - 6 sum f
# (not 2 sum f, since my counting gives 6).

sum_perplaq = sum(compute_S_munu(R, D_I, T, mu, nu) for mu, nu in PAIRS)
sum_f = sum(f(R[mu], T[mu]) for mu in range(4))

print(f"\n  sum per-plaquette: {sum_perplaq:.10f}")
print(f"  2 sum f:           {2*sum_f:.10f}")
print(f"  6 sum f:           {6*sum_f:.10f}")
print(f"  perplaq - 2*sum_f: {sum_perplaq - 2*sum_f:.10f}")
print(f"  perplaq - 6*sum_f: {sum_perplaq - 6*sum_f:.10f}")

# ========================
# TEST 5: Check budget identity: 16||T||^2 = 4 sum |T_mu - T_nu|^2
# ========================
print("\n" + "=" * 60)
print("TEST 5: Budget identity check")
print("=" * 60)
lhs = 16 * normT
rhs = 4 * sum(np.dot(T[mu]-T[nu], T[mu]-T[nu]) for mu, nu in PAIRS)
print(f"  16||T||^2:           {lhs:.10f}")
print(f"  4 sum |T_mu-T_nu|^2: {rhs:.10f}")
print(f"  Match: {abs(lhs - rhs):.2e}")

# At D=I, all B_{mu,nu} involve trivial plaquettes:
# B_{mu,nu} = (I + R_mu) T_mu - (R_mu + R_mu R_nu^T) T_nu = (I+R_mu)(T_mu - R_nu^T... hmm)
# Let me just compute F_x at D=I.
def compute_B_munu(R, D, T, mu, nu):
    R_mu = R[mu]; R_nu = R[nu]; D_mn = D[(mu, nu)]
    T_mu = T[mu]; T_nu = T[nu]
    U = R_mu @ D_mn
    return (np.eye(3) + U) @ T_mu - R_mu @ (np.eye(3) + D_mn @ R_nu.T) @ T_nu

F_x = sum(np.dot(compute_B_munu(R, D_I, T, mu, nu),
                  compute_B_munu(R, D_I, T, mu, nu)) for mu, nu in PAIRS)

actual_sum_S = 16*normT - F_x - 2*sum_f
print(f"\n  16||T||^2 - F - 2*sum_f: {actual_sum_S:.10f}")
perplaq_check = 16*normT - F_x
print(f"  16||T||^2 - F (=sum perplaq): {perplaq_check:.10f}")
print(f"  sum perplaquette computed:     {sum_perplaq:.10f}")
print(f"  Match: {abs(perplaq_check - sum_perplaq):.2e}")

# So the ACTUAL sum_S in the proof chain = 16||T||^2 - F - 2*sum_f(R, T).
# And my compute_S_munu computes the per-plaquette expression (= 16||T||^2 - F when summed).
# These differ by 2*sum_f.

# At D=I: sum_perplaq = 6*sum_f + |sum R^T T|^2 (from my algebra).
# actual sum_S = sum_perplaq - 2*sum_f = 4*sum_f + |sum R^T T|^2.
# But E003 says sum_S(D=I) = 0... so either my algebra or E003 is wrong.

# WAIT. Let me re-read the proof chain more carefully.
# Step 3: "16||T||^2 - F_x = 2*sum_mu f(R_mu, T_mu) + sum_S [VERIFIED to 5.7e-14]"
# This means: sum_S = 16||T||^2 - F_x - 2*sum_mu f(R_mu, T_mu)
# And my algebra says at D=I:
# 16||T||^2 - F_x = sum perplaq = diag + cross = 6*sum_f + cross
# So sum_S = 6*sum_f + cross - 2*sum_f = 4*sum_f + cross

# Unless the extraction is "2*sum_mu f(R_mu, T_mu)" with the factor 2 inside:
# "2*sum_mu f" = 2 * (sum_mu f(R_mu, T_mu)) = 2 * 4-terms = 2 * sum_f.
# This is what I computed. So sum_S at D=I = sum_perplaq - 2*sum_f.

# Let me just check numerically what 16||T||^2 - F - 2*sum_f gives at D=I.
print(f"\n  ACTUAL sum_S(D=I) = 16||T||^2 - F - 2*sum_f = {actual_sum_S:.10e}")

# If this is NOT zero, then E003's claim is wrong.
# If it IS zero, then my per-plaquette formula is wrong.

# Check with many samples:
print("\n" + "=" * 60)
print("TEST 6: actual sum_S(D=I) for 500 random configs")
print("=" * 60)
max_val = 0
vals2 = []
for _ in range(500):
    R = {mu: random_SO3() for mu in range(4)}
    T = random_T_in_V()
    nT = sum(np.dot(T[mu], T[mu]) for mu in range(4))
    Fx = sum(np.dot(compute_B_munu(R, D_I, T, mu, nu),
                    compute_B_munu(R, D_I, T, mu, nu)) for mu, nu in PAIRS)
    sf = sum(f(R[mu], T[mu]) for mu in range(4))
    v = 16*nT - Fx - 2*sf
    vals2.append(v)
    if abs(v) > max_val:
        max_val = abs(v)

vals2 = np.array(vals2)
print(f"  max |actual_sum_S|: {max_val:.2e}")
print(f"  min:  {np.min(vals2):.6f}")
print(f"  max:  {np.max(vals2):.6f}")
print(f"  mean: {np.mean(vals2):.6f}")

# CONCLUSION: Report whether actual_sum_S(D=I) is 0 or positive.
