"""
Tasks 3, 4, 5: Independent verification of the core proof steps.

Task 3: Check the sign structure (28 positive, 8 negative cross-terms)
Task 4: Check the expansion 64I - M = 2*[group_02 + group_13 + group_active]
Task 5: Check the Combined Bound Lemma

ALL CODE WRITTEN FROM SCRATCH.
"""

import numpy as np

np.random.seed(77777)

def random_so3():
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def f(R, n):
    """f(R, n) = 1 - n^T R n, non-negative for R in SO(3)."""
    return 1.0 - n @ R @ n

# Plaquette orientations
PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]
ACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu) % 2 == 1]
INACTIVE = [(mu, nu) for mu, nu in PLANES if (mu+nu) % 2 == 0]

print(f"Planes: {PLANES}")
print(f"Active (|a+b|=2): {ACTIVE}")
print(f"Inactive (a+b=0): {INACTIVE}")

# ============================================================
# TASK 3: Check the sign structure
# ============================================================

print("\n" + "=" * 70)
print("TASK 3: Sign structure verification")
print("=" * 70)

# For vertex x with |x| = sum of coords, and staggered sign (-1)^{|x|+mu}:
# At vertex x = (0,0,0,0), |x| = 0.
#
# For plaquette (mu, nu) at x:
#   e1 = (x, mu): sign s1 = (-1)^{|x|+mu} = (-1)^mu
#   e2 = (x+e_mu, nu): sign s2 = (-1)^{|x|+1+nu} = (-1)^{1+nu}
#   e3 = (x+e_nu, mu): sign s3 = (-1)^{|x|+1+mu} = (-1)^{1+mu}
#   e4 = (x, nu): sign s4 = (-1)^{|x|+nu} = (-1)^nu
#
# So s1 = (-1)^mu, s2 = (-1)^{nu+1}, s3 = (-1)^{mu+1} = -s1, s4 = (-1)^nu
#
# B_sq(Q,v) = s1*n + Q1*(s2*n) - (Q1*Q2*Q3^T)*(s3*n) - U_sq*(s4*n)
#           = s1*n + s2*Q1*n + s1*(Q1*Q2*Q3^T)*n - s4*U_sq*n
#   (since s3 = -s1)

# Let me define a = s1 = (-1)^mu, b_coeff = s2 = (-1)^{nu+1}
# Then s3 = -a, s4 = (-1)^nu = -b_coeff (since s4 = (-1)^nu = -(-1)^{nu+1} = -b_coeff)
# WAIT: s4 = (-1)^nu. And b_coeff = (-1)^{nu+1} = -(-1)^nu = -s4.
# So s4 = -b_coeff.

# B = a*n + b_coeff*Q1*n + a*(Q1*Q2*Q3^T)*n + b_coeff*U_sq*n
# Wait let me redo this:
# B = s1*n + s2*(Q1*n) - s3*(Q1*Q2*Q3^T*n) - s4*(U_sq*n)
# = a*n + b*(Q1*n) + a*(Q1*Q2*Q3^T*n) + b*(U_sq*n)
# where a = (-1)^mu and b = (-1)^{nu+1}
# because -s3 = s1 = a and -s4 = b_coeff = b

# Hmm wait, let me check more carefully:
# s3 = (-1)^{mu+1} = -(-1)^mu = -a
# So -s3 = a. ✓
# s4 = (-1)^nu
# -s4 = -(-1)^nu = (-1)^{nu+1} = b. ✓

# So B = a*n + b*(Q1*n) + a*(Q1*Q2*Q3^T)*n + b*(U_sq)*n

# For the proof, we need rotations acting on n:
# Term 1: a * I * n (rotation = I)
# Term 2: b * Q1 * n (rotation = Q1 = R_mu * ...)

# Actually, let me think about what Q1, Q2, Q3, Q4 are in terms of the proof's R_mu, D_{mu,nu}.
#
# On the L=2 torus, the edges are gauge variables in SU(2) ≅ SO(3).
# The proof parametrizes:
#   Q_{(x,mu)} for base edges at vertex x=0: these are R_0, R_1, R_2, R_3
#   Cross-links depend on D_{mu,nu}
#
# For plaquette (mu,nu) at x=0:
#   e1 = (0, mu) → Q1 = R_mu
#   e2 = (e_mu, nu) → this is a cross-edge. Q2 = ?
#   e3 = (e_nu, mu) → cross-edge. Q3 = ?
#   e4 = (0, nu) → Q4 = R_nu
#
# The proof defines D_{mu,nu} as the holonomy of the "cross" path.
# From E006: A_{mu,nu} = a(I + R_mu D_{mu,nu}) + b(R_mu + R_mu D_{mu,nu} R_nu^T)
#
# Let me derive what A_{mu,nu} should be from B_sq:
#
# B = a*n + b*R_mu*n + a*(R_mu*Q2*Q3^T)*n + b*(R_mu*Q2*Q3^T*R_nu^T)*n
#   = (aI + bR_mu + a*R_mu*Q2*Q3^T + b*R_mu*Q2*Q3^T*R_nu^T) * n
#
# If we define D_{mu,nu} = Q2 * Q3^T (the cross-link combination), then:
# B = (aI + bR_mu + a*R_mu*D + b*R_mu*D*R_nu^T) * n
#   = a*(I + R_mu*D) * n + b*(R_mu + R_mu*D*R_nu^T) * n
#
# So A_{mu,nu} = a(I + R_mu D) + b(R_mu + R_mu D R_nu^T). ✓ Matches E006!

# Now, |B|^2 = n^T A^T A n. Expanding A^T A:
# A = aI + bR_mu + aR_mu*D + bR_mu*D*R_nu^T
# 4 terms, so A^T A has 16 terms.

# Let's enumerate the 6 cross-product terms for each plaquette.
# The diagonal terms give: a^2 + b^2 + a^2 + b^2 = 2(a^2 + b^2) = 4 each (since a,b are ±1).
# Wait, A has 4 column-terms: [aI, bR_mu, aR_mu*D, bR_mu*D*R_nu^T]
# Actually, A * n = (aI + bR_mu + aR_mu D + bR_mu D R_nu^T) n
# So |An|^2 = sum of all pairs:
#   = a^2(n^T n) + b^2(n^T R_mu^T R_mu n) + a^2(n^T D^T R_mu^T R_mu D n) + b^2(n^T R_nu D^T R_mu^T R_mu D R_nu^T n)
#     + cross terms
#   = a^2 + b^2 + a^2 + b^2 + cross terms  (since R, D ∈ SO(3))
#   = 4 + cross terms

# Cross terms (there are C(4,2) = 6 pairs):
# Pair (1,2): 2ab * n^T R_mu n
# Pair (1,3): 2a^2 * n^T R_mu D n
# Pair (1,4): 2ab * n^T R_mu D R_nu^T n
# Pair (2,3): 2ab * n^T R_mu^T R_mu D n = 2ab * n^T D n  (since R_mu^T R_mu = I)

# Wait, that's wrong. Let me redo:
# A = aI + bR_mu + a(R_mu D) + b(R_mu D R_nu^T)
# |An|^2 = |a*n + b*R_mu*n + a*R_mu*D*n + b*R_mu*D*R_nu^T*n|^2
# Diagonal: a^2|n|^2 + b^2|R_mu n|^2 + a^2|R_mu D n|^2 + b^2|R_mu D R_nu^T n|^2 = a^2 + b^2 + a^2 + b^2 = 4
# Cross (i,j) terms: 2 * (coefficient_i * coefficient_j) * (term_i)^T (term_j)

# Let me label:
# u0 = n (coeff a), u1 = R_mu n (coeff b), u2 = R_mu D n (coeff a), u3 = R_mu D R_nu^T n (coeff b)
# coeffs = [a, b, a, b]

# Cross term (i,j): 2 * c_i * c_j * u_i^T u_j = 2 * c_i * c_j * n^T O_{ij} n
# where O_{ij} is the rotation taking n to u_j via the left factor and u_i via the right.

# O_01 = R_mu          (n^T R_mu n)        coeff: 2ab
# O_02 = R_mu D        (n^T R_mu D n)      coeff: 2a^2
# O_03 = R_mu D R_nu^T (n^T R_mu D R_nu^T n) coeff: 2ab
# O_12 = R_mu^T R_mu D = D                  (n^T D n)           coeff: 2ab  (WAIT: u1^T u2 = (R_mu n)^T (R_mu D n) = n^T R_mu^T R_mu D n = n^T D n)
# O_13 = R_mu^T R_mu D R_nu^T = D R_nu^T   (n^T D R_nu^T n)   coeff: 2b^2
# O_23 = D^T R_mu^T R_mu D R_nu^T = R_nu^T  (WAIT: u2^T u3 = (R_mu D n)^T (R_mu D R_nu^T n) = n^T D^T R_mu^T R_mu D R_nu^T n = n^T R_nu^T n)

# Wait, u2^T u3 = n^T D^T R_mu^T R_mu D R_nu^T n = n^T D^T D R_nu^T n? No!
# u2 = R_mu D n, u3 = R_mu D R_nu^T n
# u2^T u3 = n^T (R_mu D)^T (R_mu D R_nu^T) n = n^T D^T R_mu^T R_mu D R_nu^T n = n^T D^T D R_nu^T n = n^T R_nu^T n
# Hmm, D^T D = I since D ∈ SO(3). So n^T R_nu^T n = n^T R_nu n (well, n^T R_nu^T n != n^T R_nu n in general)
# Actually, n^T R_nu^T n IS equal to n^T R_nu n when R_nu is real, because n^T R n = (n^T R n)^T = n^T R^T n for a scalar.
# YES: n^T R n is a scalar, so (n^T R n)^T = n^T R^T n = n^T R n. WRONG!
# (n^T R n) is a scalar. Its transpose is itself: n^T R n.
# (n^T R n)^T = n^T R^T n. Since a scalar equals its transpose, n^T R n = n^T R^T n.
# So indeed n^T R_nu^T n = n^T R_nu n.

# So the cross terms are:
# (0,1): 2ab * n^T R_mu n, sign = 2ab
# (0,2): 2a^2 * n^T (R_mu D) n, sign = 2a^2 = 2
# (0,3): 2ab * n^T (R_mu D R_nu^T) n, sign = 2ab
# (1,2): 2ab * n^T D n, sign = 2ab (since u1^T u2 = n^T D n)
#    Wait, the coeff is 2 * b * a = 2ab.
# (1,3): 2b^2 * n^T (D R_nu^T) n, sign = 2b^2 = 2
# (2,3): 2ab * n^T R_nu^T n = 2ab * n^T R_nu n, sign = 2ab

# So total for plaquette (mu,nu):
# |B|^2 = 4 + 2[ab*n^T R_mu n + a^2*n^T(R_mu D)n + ab*n^T(R_mu D R_nu^T)n
#              + ab*n^T D n + b^2*n^T(D R_nu^T)n + ab*n^T R_nu n]
# = 4 + 2[ab(n^T R_mu n + n^T R_nu n + n^T D n + n^T(R_mu D R_nu^T)n)
#        + a^2*n^T(R_mu D)n + b^2*n^T(D R_nu^T)n]

# Now a = (-1)^mu, b = (-1)^{nu+1}
# ab = (-1)^{mu+nu+1}
# a^2 = 1, b^2 = 1

# So the sign of each cross-term rotation O:
# For each plaquette (mu,nu):
#   R_mu:           sign = ab = (-1)^{mu+nu+1}
#   R_mu D:         sign = 1  (always positive)
#   R_mu D R_nu^T:  sign = ab = (-1)^{mu+nu+1}
#   D:              sign = ab = (-1)^{mu+nu+1}
#   D R_nu^T:       sign = 1  (always positive)
#   R_nu:           sign = ab = (-1)^{mu+nu+1}

# For active plaquettes (mu+nu odd): ab = (-1)^{even} = +1 → all 6 terms have sign +1
# For inactive plaquettes (mu+nu even): ab = (-1)^{odd} = -1 → 4 terms have sign -1, 2 have sign +1

print("\n--- Cross-term sign analysis ---")
total_positive = 0
total_negative = 0
print(f"\n{'Plane':>8} {'a':>3} {'b':>3} {'ab':>3} | {'R_mu':>5} {'R_mu D':>6} {'R_mu D Rnu^T':>12} {'D':>5} {'D Rnu^T':>7} {'R_nu':>5} | pos neg")
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    ab = a * b

    signs = [ab, 1, ab, ab, 1, ab]  # R_mu, R_mu D, R_mu D R_nu^T, D, D R_nu^T, R_nu
    pos = sum(1 for s in signs if s > 0)
    neg = sum(1 for s in signs if s < 0)
    total_positive += pos
    total_negative += neg

    print(f"  ({mu},{nu}): a={a:+d} b={b:+d} ab={ab:+d} | "
          f"{signs[0]:+d}   {signs[1]:+d}      {signs[2]:+d}          {signs[3]:+d}   {signs[4]:+d}      {signs[5]:+d}   | {pos} {neg}")

print(f"\nTotal: {total_positive} positive, {total_negative} negative")
print(f"Net sum of signs: {total_positive - total_negative}")
print(f"Expected: 28 positive, 8 negative, net = 20")

# Verify: c + Tr(P) = 24 + 2*20 = 64
net_sum = total_positive - total_negative
expected_trace = 24 + 2 * net_sum  # 24 from diagonal (4 per plaquette × 6 plaquettes), plus cross terms
print(f"\nc + Tr(P) = 24 + 2*{net_sum} = {expected_trace}")

# ============================================================
# TASK 3b: Verify sign structure is the SAME for all vertices
# ============================================================

print("\n" + "=" * 70)
print("TASK 3b: Sign structure for different vertices")
print("=" * 70)

# The staggered signs depend on |x| = sum of coords.
# s1 = (-1)^{|x|+mu}, s2 = (-1)^{|x|+1+nu}, s3 = (-1)^{|x|+1+mu}, s4 = (-1)^{|x|+nu}
# -s3 = (-1)^{|x|+mu} = s1, -s4 = (-1)^{|x|+nu+1} = s2... wait:
# -s4 = -(-1)^{|x|+nu} = (-1)^{|x|+nu+1}

# B = s1*n + s2*Q1*n + (-s3)*Q1Q2Q3^T*n + (-s4)*U*n
#   = s1*n + s2*Q1*n + s1*Q1Q2Q3^T*n + (-s4)*U*n

# Wait, -s4 = (-1)^{|x|+nu+1}. And s2 = (-1)^{|x|+1+nu} = (-1)^{|x|+nu+1}. So -s4 = s2!

# So B = s1*(I + Q1Q2Q3^T)*n + s2*(Q1 + U)*n
# This means A_{mu,nu} = s1*(I + R_mu D) + s2*(R_mu + R_mu D R_nu^T)

# Now, s1 = (-1)^{|x|+mu} and s2 = (-1)^{|x|+nu+1}.
# For |x| even (same parity as x=0): s1 = (-1)^mu = a, s2 = (-1)^{nu+1} = b. Same as before.
# For |x| odd: s1 = (-1)^{mu+1} = -a, s2 = (-1)^{nu+2} = -b. So both signs flip!

# A_{mu,nu} = -a*(I + R_mu D) + (-b)*(R_mu + R_mu D R_nu^T) = -[a*(I + R_mu D) + b*(R_mu + R_mu D R_nu^T)]

# So A at odd |x| is just -A at even |x|. And |B|^2 = |-A*n|^2 = |A*n|^2. THE SAME!

# Therefore the sign structure is IDENTICAL for all vertices.

# But wait - the rotations R_mu, D_{mu,nu} are DIFFERENT for different vertices!
# At vertex x=0: R_mu = Q_{(0,mu)}, D depends on cross-links.
# At vertex x=1: R_mu = Q_{(1,mu)}, different gauge variables.

# The per-vertex bound says: for ANY SO(3) rotations R_0,...,R_3, D_{mu,nu},
# lambda_max(M_total) <= 64. Since this is universally quantified, it applies
# regardless of which specific gauge variables appear at each vertex.

# The sign structure (which determines the proof's grouping) is the same for all vertices
# (up to an overall sign that cancels in |B|^2).

for parity in [0, 1]:
    label = "even |x|" if parity == 0 else "odd |x|"
    pos_count = 0
    neg_count = 0
    for mu, nu in PLANES:
        s1 = (-1)**(parity + mu)
        s2 = (-1)**(parity + 1 + nu)
        # Coefficients in A: s1 for (I, R_mu D) and s2 for (R_mu, R_mu D R_nu^T)
        # Cross-term coefficient pairs:
        # (term_i, term_j) -> 2 * coeff_i * coeff_j
        # (0,1): 2*s1*s2, (0,2): 2*s1^2=2, (0,3): 2*s1*s2
        # (1,2): 2*s2*s1, (1,3): 2*s2^2=2, (2,3): 2*s1*s2
        ab = s1 * s2
        signs = [ab, 1, ab, ab, 1, ab]
        pos_count += sum(1 for s in signs if s > 0)
        neg_count += sum(1 for s in signs if s < 0)
    print(f"  {label}: {pos_count} positive, {neg_count} negative, net = {pos_count - neg_count}")

# ============================================================
# TASK 4: Check the expansion 64I - M = 2*[group_02 + group_13 + group_active]
# ============================================================

print("\n" + "=" * 70)
print("TASK 4: Verify the expansion of 64 - n^T M n")
print("=" * 70)

# The proof claims:
# 64 - n^T M_total n = 2 * [group_02 + group_13 + group_active]
# where (using f(R,n) = 1 - n^T R n):
#
# group_02 = f(R0) + f(R2) + f(R0*D02) + f(D02*R2^T) - f(D02) - f(R0*D02*R2^T)
# group_13 = f(R1) + f(R3) + f(R1*D13) + f(D13*R3^T) - f(D13) - f(R1*D13*R3^T)
# group_active = sum over active (mu,nu) of [f(R_mu D) + f(D) + f(R_mu D R_nu^T) + f(D R_nu^T)]

# I need to verify this by independently computing both sides.

def compute_M_total(R, D, n):
    """Compute n^T M_total n = sum_{mu<nu} |A_{mu,nu} n|^2."""
    total = 0.0
    for mu, nu in PLANES:
        a = (-1)**mu
        b = (-1)**(nu+1)
        An = a * (n + R[mu] @ D[(mu,nu)] @ n) + b * (R[mu] @ n + R[mu] @ D[(mu,nu)] @ R[nu].T @ n)
        total += np.dot(An, An)
    return total

def compute_expansion(R, D, n):
    """Compute the RHS: 2*(group_02 + group_13 + group_active)."""

    # group_02: inactive (0,2) with A=R0, B=R2, D=D02
    D02 = D[(0,2)]
    g02 = (f(R[0], n) + f(R[2], n)
         + f(R[0] @ D02, n) + f(D02 @ R[2].T, n)
         - f(D02, n) - f(R[0] @ D02 @ R[2].T, n))

    # group_13: inactive (1,3) with A=R1, B=R3, D=D13
    D13 = D[(1,3)]
    g13 = (f(R[1], n) + f(R[3], n)
         + f(R[1] @ D13, n) + f(D13 @ R[3].T, n)
         - f(D13, n) - f(R[1] @ D13 @ R[3].T, n))

    # group_active: 16 terms from active plaquettes
    g_active = 0.0
    for mu, nu in ACTIVE:
        Dmn = D[(mu,nu)]
        g_active += (f(R[mu] @ Dmn, n)
                   + f(Dmn, n)
                   + f(R[mu] @ Dmn @ R[nu].T, n)
                   + f(Dmn @ R[nu].T, n))

    return 2 * (g02 + g13 + g_active), g02, g13, g_active

# But WAIT - I need to verify the expansion is correct.
# The proof claims that 64 - n^T M n = 2*(g02 + g13 + g_active).
# Let me derive this independently.

# From the cross-term analysis above:
# n^T M_total n = Sum_{(mu,nu)} [4 + 2*(sum of 6 cross terms for that plaquette)]
#               = 24 + 2*Sum_{all 36 cross terms} sigma_k * n^T O_k n
#
# 64 - n^T M_total n = 64 - 24 - 2*Sum sigma_k * n^T O_k n
#                     = 40 - 2*Sum sigma_k * n^T O_k n
#                     = 40 + 2*Sum sigma_k * (1 - n^T O_k n) - 2*Sum sigma_k
#                     = 40 + 2*Sum sigma_k * f(O_k, n) - 2*20
#                     = 2*Sum sigma_k * f(O_k, n)
#
# So 64 - n^T M n = 2 * Sum_{k=1}^{36} sigma_k * f(O_k, n)
#
# Now I need to verify that this sum matches the grouping.

# Let me enumerate all 36 terms with their signs and rotations:
print("\n--- Enumerating all 36 cross-term rotations and signs ---")

all_terms = []
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    ab = a * b

    # The 6 rotations and their signs (from the analysis above):
    terms = [
        (ab, f"R{mu}", "base"),
        (1, f"R{mu}*D{mu}{nu}", "positive"),
        (ab, f"R{mu}*D{mu}{nu}*R{nu}^T", "composite"),
        (ab, f"D{mu}{nu}", "cross"),
        (1, f"D{mu}{nu}*R{nu}^T", "positive"),
        (ab, f"R{nu}", "base"),
    ]
    for sign, name, category in terms:
        all_terms.append((mu, nu, sign, name, category))

# Count
pos_terms = [(mu,nu,s,n,c) for mu,nu,s,n,c in all_terms if s > 0]
neg_terms = [(mu,nu,s,n,c) for mu,nu,s,n,c in all_terms if s < 0]
print(f"Total terms: {len(all_terms)}, Positive: {len(pos_terms)}, Negative: {len(neg_terms)}")

# Now group by the proof's decomposition:
# Negative terms (sign = -1) only occur when ab = -1, i.e., mu+nu even (inactive)
# For inactive (0,2): negative terms are ab*f(R0), ab*f(R0*D02*R2^T), ab*f(D02), ab*f(R2) → 4 negative
# For inactive (1,3): same → 4 negative
# Total negative: 8 ✓

# The positive terms:
# From active plaquettes: all 6*4 = 24 terms positive (since ab = +1)
# From inactive plaquettes: 2 terms each (the a^2 and b^2 ones) = 2*2 = 4
# Total positive: 24 + 4 = 28 ✓

# Now verify the grouping:
# For inactive (0,2), the 6 terms are:
# +f(R0*D02), -f(R0*D02*R2^T), -f(D02), +f(D02*R2^T), -f(R0), -f(R2)
# Wait: signs are ab=-1 for (R0, R0*D02*R2^T, D02, R2) and +1 for (R0*D02, D02*R2^T)
# So sigma_k * f(O_k) = -f(R0) + f(R0*D02) - f(R0*D02*R2^T) - f(D02) + f(D02*R2^T) - f(R2)
# = f(R0*D02) + f(D02*R2^T) - f(R0) - f(R2) - f(D02) - f(R0*D02*R2^T)
# Hmm, that's MINUS what the proof calls group_02!

# The proof says group_02 = f(R0) + f(R2) + f(R0*D02) + f(D02*R2^T) - f(D02) - f(R0*D02*R2^T)
# My derivation gives: sigma terms for (0,2) = -f(R0) - f(R2) + f(R0*D02) + f(D02*R2^T) - f(D02) - f(R0*D02*R2^T)
# = f(R0*D02) + f(D02*R2^T) - f(D02) - f(R0*D02*R2^T) - f(R0) - f(R2)

# The proof's group_02 - my (0,2) sigma sum = 2*f(R0) + 2*f(R2)

# And for active plaquettes, the sigma terms are ALL positive:
# sigma terms for active (mu,nu) = +f(R_mu) + f(R_mu D) + f(R_mu D R_nu^T) + f(D) + f(D R_nu^T) + f(R_nu)
# The proof's group_active only has 4 terms per active plaquette: f(R_mu D) + f(D) + f(R_mu D R_nu^T) + f(D R_nu^T)
# So the proof absorbs the f(R_mu) and f(R_nu) terms from active plaquettes into the inactive groups!

# Total sigma sum = sum over inactive + sum over active
# = [sigma terms for (0,2)] + [sigma terms for (1,3)] + [sigma terms for active]

# Now, from each active plaquette, f(R_mu) and f(R_nu) terms need to go somewhere.
# The active plaquettes are (0,1), (0,3), (1,2), (2,3).
# Base link terms from active plaquettes:
# (0,1): f(R0) + f(R1)
# (0,3): f(R0) + f(R3)
# (1,2): f(R1) + f(R2)
# (2,3): f(R2) + f(R3)
# Total: 2*f(R0) + 2*f(R1) + 2*f(R2) + 2*f(R3)

# From inactive (0,2): -f(R0) - f(R2). Plus proof's group_02 needs +f(R0) + f(R2) extra.
# From inactive (1,3): -f(R1) - f(R3). Plus proof's group_13 needs +f(R1) + f(R3) extra.

# So: sigma sum for inactive (0,2) = group_02 - 2*f(R0) - 2*f(R2)
# sigma sum for inactive (1,3) = group_13 - 2*f(R1) - 2*f(R3)
# sigma sum for active = group_active + 2*f(R0) + 2*f(R1) + 2*f(R2) + 2*f(R3)

# Total: (group_02 - 2f(R0) - 2f(R2)) + (group_13 - 2f(R1) - 2f(R3)) + (group_active + 2f(R0) + 2f(R1) + 2f(R2) + 2f(R3))
#       = group_02 + group_13 + group_active

# So the grouping IS correct! The base-link terms from active plaquettes provide the extra
# f(R_mu) needed in the inactive groups. Beautiful.

print("\nGrouping verification (algebraic):")
print("  Active plaquettes contribute f(R_mu) + f(R_nu) each")
print("  These get absorbed into the inactive groups to form the Combined Bound")
print("  Algebraically consistent ✓")

# Now numerically verify:

print("\n--- Numerical verification of expansion ---")
max_err = 0
min_g02 = float('inf')
min_g13 = float('inf')
min_g_active = float('inf')
N_trials = 100000

for trial in range(N_trials):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    n = np.random.randn(3); n /= np.linalg.norm(n)

    lhs = 64 - compute_M_total(R, D, n)
    rhs, g02, g13, g_active = compute_expansion(R, D, n)

    err = abs(lhs - rhs)
    max_err = max(max_err, err)
    min_g02 = min(min_g02, g02)
    min_g13 = min(min_g13, g13)
    min_g_active = min(min_g_active, g_active)

print(f"  Max |LHS - RHS| over {N_trials} tests: {max_err:.2e}")
print(f"  Expansion VERIFIED: {max_err < 1e-10}")
print(f"  Min group_02: {min_g02:.6f} (should be >= 0)")
print(f"  Min group_13: {min_g13:.6f} (should be >= 0)")
print(f"  Min group_active: {min_g_active:.6f} (should be >= 0)")

# ============================================================
# TASK 5: Check the Combined Bound Lemma
# ============================================================

print("\n" + "=" * 70)
print("TASK 5: Combined Bound Lemma verification")
print("=" * 70)

# LEMMA: For A, B, D in SO(3), unit n in R^3:
# f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) >= 0
#
# CLAIMED PROOF:
# (a) Algebraic identity: LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B)
# (b) Cauchy-Schwarz: |n^T(I-A)D(I-B^T)n| <= 2*sqrt(f(A)*f(B))
# (c) AM-GM: f(A)+f(B) - 2*sqrt(f(A)*f(B)) = (sqrt(f(A))-sqrt(f(B)))^2 >= 0

# Part (a): Verify algebraic identity
print("\n--- Part (a): Algebraic identity ---")
max_err_identity = 0
for _ in range(100000):
    A = random_so3()
    B = random_so3()
    D = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    lhs = (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n)
         - f(D,n) - f(A@D@B.T,n))

    cross = n @ (np.eye(3) - A) @ D @ (np.eye(3) - B.T) @ n
    rhs = cross + f(A,n) + f(B,n)

    err = abs(lhs - rhs)
    max_err_identity = max(max_err_identity, err)

print(f"  Max error: {max_err_identity:.2e}")
print(f"  Identity VERIFIED: {max_err_identity < 1e-12}")

# Let me also verify ANALYTICALLY:
# LHS = (1-n^T A n) + (1-n^T B n) + (1-n^T AD n) + (1-n^T DB^T n)
#      - (1-n^T D n) - (1-n^T ADB^T n)
# = 6 - n^T(A+B+AD+DB^T)n - 6 + n^T(I+I+D+ADB^T)n
# Wait let me be more careful:
# = (1-nAn) + (1-nBn) + (1-nADn) + (1-nDBn) - (1-nDn) - (1-nADBn)
# = 4 - nAn - nBn - nADn - nDBn - (-2 + nDn + nADBn)
# Hmm, let me just expand:
# = 1 - nAn + 1 - nBn + 1 - nADn + 1 - nDBn - 1 + nDn - 1 + nADBn
# = 2 - nAn - nBn - nADn - nDBn + nDn + nADBn

# cross + f(A) + f(B) = nDn - nDBn - nADn + nADBn + 1 - nAn + 1 - nBn
# = 2 - nAn - nBn + nDn - nDBn - nADn + nADBn
# Same! ✓ (The identity holds algebraically.)

print("  Algebraic expansion confirms identity ✓")

# Part (b): Cauchy-Schwarz bound
print("\n--- Part (b): Cauchy-Schwarz bound ---")
max_ratio = 0
cs_violations = 0
for _ in range(200000):
    A = random_so3()
    B = random_so3()
    D = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)

    cross = abs(n @ (np.eye(3) - A) @ D @ (np.eye(3) - B.T) @ n)
    fA = f(A, n)
    fB = f(B, n)
    bound = 2 * np.sqrt(max(fA, 0) * max(fB, 0))

    if bound > 1e-15:
        ratio = cross / bound
        max_ratio = max(max_ratio, ratio)
        if ratio > 1 + 1e-10:
            cs_violations += 1

print(f"  Max |cross|/bound: {max_ratio:.10f}")
print(f"  Violations: {cs_violations}")
print(f"  Cauchy-Schwarz VERIFIED: {max_ratio <= 1.0 + 1e-10}")

# Part (b) proof check: The claim is:
# |n^T(I-A)D(I-B^T)n| = |((I-A^T)n)^T D ((I-B^T)n)|
# By C-S: <= |(I-A^T)n| * |D(I-B^T)n| = |(I-A^T)n| * |(I-B^T)n| (D orthogonal)
# And |(I-R^T)n|^2 = n^T(I-R)(I-R^T)n = n^T(2I - R - R^T)n = 2(1 - n^T((R+R^T)/2)n)
# = 2(1 - n^T R n) = 2f(R,n)  [since n^T R n = n^T R^T n = n^T((R+R^T)/2)n]

# CRITICAL CHECK: Is n^T R n = n^T R^T n?
# Yes! For any real matrix M and real vector n: n^T M n is a scalar, and
# (n^T M n)^T = n^T M^T n. Since a scalar equals its transpose, n^T M n = n^T M^T n.
# Therefore n^T R n = n^T R^T n = n^T((R+R^T)/2)n.
print("  Key step: n^T R n = n^T R^T n (trivially true for real scalars) ✓")

# Verify |(I-R^T)n|^2 = 2*f(R,n)
print("\n--- Verifying |(I-R^T)n|^2 = 2*f(R,n) ---")
max_err_norm = 0
for _ in range(100000):
    R = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)
    lhs = np.linalg.norm((np.eye(3) - R.T) @ n)**2
    rhs = 2 * f(R, n)
    err = abs(lhs - rhs)
    max_err_norm = max(max_err_norm, err)
print(f"  Max error: {max_err_norm:.2e}")
print(f"  VERIFIED: {max_err_norm < 1e-12}")

# Part (c): AM-GM (trivially true)
print("\n--- Part (c): AM-GM ---")
print("  (sqrt(a) - sqrt(b))^2 >= 0 for a,b >= 0: TRIVIALLY TRUE")

# Verify that f(R,n) >= 0 for all R in SO(3), n unit
print("\n--- Verifying f(R,n) >= 0 ---")
min_f = float('inf')
for _ in range(500000):
    R = random_so3()
    n = np.random.randn(3); n /= np.linalg.norm(n)
    val = f(R, n)
    min_f = min(min_f, val)
print(f"  Min f(R,n): {min_f:.10f} (should be >= 0)")
print(f"  VERIFIED: {min_f >= -1e-15}")

# Analytic proof: n^T R n = n^T ((R+R^T)/2) n. For R in SO(3) with eigenvalues
# {1, e^{i*theta}, e^{-i*theta}}, we have (R+R^T)/2 has eigenvalues {1, cos(theta), cos(theta)}.
# So n^T R n = n_1^2 + cos(theta)*(n_2^2 + n_3^2) where n_i are projections onto eigenvectors.
# Since cos(theta) >= -1 and n_1^2 + n_2^2 + n_3^2 = 1:
# n^T R n >= min(1, cos(theta)) = cos(theta) >= -1.
# So f(R,n) = 1 - n^T R n <= 2 and f(R,n) = 1 - n^T R n >= 1 - 1 = 0. ✓

# ============================================================
# TASK 5b: Try to BREAK the Combined Bound Lemma
# ============================================================

print("\n" + "=" * 70)
print("TASK 5b: Adversarial search for Combined Bound Lemma violation")
print("=" * 70)

# Try to minimize f(A)+f(B)+f(AD)+f(DB^T)-f(D)-f(ADB^T)
# If we can find a negative value, the lemma is false.

# Strategy: gradient descent on the expression

from scipy.optimize import minimize

def combined_bound_objective(params):
    """Parametrize A, B, D via axis-angle, n via spherical coords."""
    # A: params[0:3], B: params[3:6], D: params[6:9], n: params[9:11]
    def axis_angle_to_R(omega):
        angle = np.linalg.norm(omega)
        if angle < 1e-14:
            return np.eye(3)
        axis = omega / angle
        K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
        return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K@K)

    A = axis_angle_to_R(params[0:3])
    B = axis_angle_to_R(params[3:6])
    D = axis_angle_to_R(params[6:9])
    theta, phi = params[9], params[10]
    n = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])

    val = (f(A,n) + f(B,n) + f(A@D,n) + f(D@B.T,n)
         - f(D,n) - f(A@D@B.T,n))
    return val

min_val = float('inf')
for trial in range(500):
    x0 = np.random.randn(11) * np.pi
    res = minimize(combined_bound_objective, x0, method='Nelder-Mead',
                  options={'maxiter': 5000, 'xatol': 1e-12, 'fatol': 1e-14})
    if res.fun < min_val:
        min_val = res.fun
        if res.fun < -1e-10:
            print(f"  VIOLATION at trial {trial}: min = {res.fun:.15f}")
            break

print(f"  Min combined bound over 500 adversarial trials: {min_val:.15e}")
print(f"  Lemma HOLDS: {min_val >= -1e-10}")

# ============================================================
# TASK 4b: Verify group_active terms are all non-negative
# ============================================================

print("\n" + "=" * 70)
print("TASK 4b: Verify all 16 active terms are non-negative")
print("=" * 70)

# group_active = sum over active (mu,nu) of [f(R_mu D) + f(D) + f(R_mu D R_nu^T) + f(D R_nu^T)]
# Each of these 16 terms is f(some SO(3) rotation, n) which we just proved is >= 0.
# So this is trivially non-negative.

min_active_term = float('inf')
for _ in range(100000):
    R = [random_so3() for _ in range(4)]
    D = {p: random_so3() for p in PLANES}
    n = np.random.randn(3); n /= np.linalg.norm(n)

    for mu, nu in ACTIVE:
        Dmn = D[(mu,nu)]
        terms = [
            f(R[mu] @ Dmn, n),
            f(Dmn, n),
            f(R[mu] @ Dmn @ R[nu].T, n),
            f(Dmn @ R[nu].T, n)
        ]
        for t in terms:
            min_active_term = min(min_active_term, t)

print(f"  Min individual active term: {min_active_term:.10f}")
print(f"  All non-negative: {min_active_term >= -1e-15} (trivially, since f(R,n) >= 0)")

print("\nAll core proof tasks complete.")
