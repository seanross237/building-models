"""
Task 6b: Investigate sign structure variations across vertices on different L.

CRITICAL QUESTION: On L=2, all vertices have the same staggered sign structure.
On L>=3, vertices where some coordinate x_mu = L-1 have DIFFERENT sign structures.
Does the proof's bound still hold?
"""

import numpy as np

np.random.seed(88888)

d = 4

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
    return 1.0 - n @ R @ n

PLANES = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]

# ============================================================
# Part A: Classify all sign structures
# ============================================================

print("=" * 70)
print("SIGN STRUCTURE ANALYSIS FOR DIFFERENT L")
print("=" * 70)

def get_sign_structure(x, L):
    """
    Compute (a, b) signs for each plaquette at vertex x on L-torus.
    a = (-1)^{|x|+mu}
    b = (-1)^{|x+e_mu|+nu}
    Returns dict: (mu,nu) -> (a, b, ab)
    """
    result = {}
    for mu, nu in PLANES:
        a = (-1) ** (sum(x) + mu)
        # x + e_mu
        x_mu = list(x)
        x_mu[mu] = (x_mu[mu] + 1) % L
        b = (-1) ** (sum(x_mu) + nu)
        result[(mu,nu)] = (a, b, a*b)
    return result

# L=2: Check all 16 vertices
print("\n--- L=2 ---")
L = 2
from itertools import product
sign_types_L2 = {}
for x in product(range(L), repeat=d):
    ss = get_sign_structure(x, L)
    ab_tuple = tuple(ss[(mu,nu)][2] for mu,nu in PLANES)
    if ab_tuple not in sign_types_L2:
        sign_types_L2[ab_tuple] = []
    sign_types_L2[ab_tuple].append(x)

print(f"  Number of distinct sign structures: {len(sign_types_L2)}")
for ab_tuple, verts in sign_types_L2.items():
    pos = sum(1 for s in ab_tuple if s > 0)
    neg = sum(1 for s in ab_tuple if s < 0)
    net = pos - neg
    c_tr = 24 + 2*net
    # Which planes are "inactive" (ab=-1)?
    inactive = [(mu,nu) for (mu,nu), ab_val in zip(PLANES, ab_tuple) if ab_val < 0]
    print(f"  ab={ab_tuple}: {len(verts)} vertices, {pos} pos {neg} neg, net={net}, c+Tr(P)={c_tr}, inactive={inactive}")

# L=3: Check all 81 vertices
print("\n--- L=3 ---")
L = 3
sign_types_L3 = {}
for x in product(range(L), repeat=d):
    ss = get_sign_structure(x, L)
    ab_tuple = tuple(ss[(mu,nu)][2] for mu,nu in PLANES)
    if ab_tuple not in sign_types_L3:
        sign_types_L3[ab_tuple] = []
    sign_types_L3[ab_tuple].append(x)

print(f"  Number of distinct sign structures: {len(sign_types_L3)}")
for ab_tuple, verts in sign_types_L3.items():
    pos = sum(1 for s in ab_tuple if s > 0)
    neg = sum(1 for s in ab_tuple if s < 0)
    net = pos - neg
    c_tr = 24 + 2*net
    inactive = [(mu,nu) for (mu,nu), ab_val in zip(PLANES, ab_tuple) if ab_val < 0]
    print(f"  ab={ab_tuple}: {len(verts)} vertices, {pos} pos {neg} neg, net={net}, c+Tr(P)={c_tr}, inactive={inactive}")
    if len(verts) <= 5:
        print(f"    Examples: {verts[:3]}")

# L=4: Check
print("\n--- L=4 ---")
L = 4
sign_types_L4 = {}
for x in product(range(L), repeat=d):
    ss = get_sign_structure(x, L)
    ab_tuple = tuple(ss[(mu,nu)][2] for mu,nu in PLANES)
    if ab_tuple not in sign_types_L4:
        sign_types_L4[ab_tuple] = []
    sign_types_L4[ab_tuple].append(x)

print(f"  Number of distinct sign structures: {len(sign_types_L4)}")
for ab_tuple, verts in sign_types_L4.items():
    pos = sum(1 for s in ab_tuple if s > 0)
    neg = sum(1 for s in ab_tuple if s < 0)
    net = pos - neg
    c_tr = 24 + 2*net
    inactive = [(mu,nu) for (mu,nu), ab_val in zip(PLANES, ab_tuple) if ab_val < 0]
    print(f"  ab={ab_tuple}: {len(verts)} vertices, {pos} pos {neg} neg, net={net}, c+Tr(P)={c_tr}, inactive={inactive}")

# ============================================================
# Part B: For each sign structure, compute M_total and check bound
# ============================================================

print("\n" + "=" * 70)
print("PER-SIGN-STRUCTURE BOUND CHECK (L=3)")
print("=" * 70)

def compute_M_total_with_signs(R, D, n, sign_struct):
    """Compute n^T M_total n for a given sign structure."""
    total = 0.0
    for mu, nu in PLANES:
        a, b, _ = sign_struct[(mu,nu)]
        Dmn = D[(mu,nu)]
        An = a * (n + R[mu] @ Dmn @ n) + b * (R[mu] @ n + R[mu] @ Dmn @ R[nu].T @ n)
        total += np.dot(An, An)
    return total

# Standard sign structure (L=2 type)
standard_ss = {}
for mu, nu in PLANES:
    a = (-1)**mu
    b = (-1)**(nu+1)
    standard_ss[(mu,nu)] = (a, b, a*b)

# All sign structures from L=3
all_structures = {}
L = 3
for x in product(range(L), repeat=d):
    ss = get_sign_structure(x, L)
    ab_key = tuple(ss[(mu,nu)][2] for mu,nu in PLANES)
    if ab_key not in all_structures:
        all_structures[ab_key] = ss

print(f"\nTesting {len(all_structures)} distinct sign structures on L=3...")

for ab_key, ss in all_structures.items():
    pos = sum(1 for s in ab_key if s > 0)
    neg = sum(1 for s in ab_key if s < 0)
    c_tr = 24 + 2*(pos - neg)

    max_F = 0
    for trial in range(10000):
        R = [random_so3() for _ in range(4)]
        D = {p: random_so3() for p in PLANES}
        n = np.random.randn(3); n /= np.linalg.norm(n)

        F = compute_M_total_with_signs(R, D, n, ss)
        max_F = max(max_F, F)

    # The bound should be c+Tr(P) for this sign structure
    inactive = [p for p, ab in zip(PLANES, ab_key) if ab < 0]
    print(f"  Signs: {pos}+/{neg}-, c+Tr(P)={c_tr}, max F = {max_F:.4f}, "
          f"ratio = {max_F/c_tr:.6f}, <=64? {'YES' if max_F <= 64+1e-10 else 'NO'}, "
          f"inactive={inactive}")

# ============================================================
# Part C: Can the proof be extended to all sign structures?
# ============================================================

print("\n" + "=" * 70)
print("PROOF EXTENSION ANALYSIS")
print("=" * 70)

# For the standard structure: 2 inactive planes, grouped into 2 Combined Bounds
# The proof needs each inactive group to be non-negative.
# For structures with 3+ inactive planes, we need more Combined Bound groups.
# But the base-link budget may be insufficient.

# Check: for each sign structure, verify 64-F expansion and group non-negativity

for ab_key, ss in all_structures.items():
    pos = sum(1 for s in ab_key if s > 0)
    neg = sum(1 for s in ab_key if s < 0)
    c_tr = 24 + 2*(pos - neg)
    inactive = [(mu,nu) for (mu,nu), ab in zip(PLANES, ab_key) if ab < 0]
    active = [(mu,nu) for (mu,nu), ab in zip(PLANES, ab_key) if ab > 0]

    # For each inactive plane, the Combined Bound Lemma needs f(R_mu) + f(R_nu).
    # These come from the active planes' base-link terms.
    # Count how many times each R_mu appears in active planes' base-link terms:
    base_link_budget = {mu: 0 for mu in range(4)}
    for mu, nu in active:
        base_link_budget[mu] += 1
        base_link_budget[nu] += 1

    # Count how many times each R_mu is needed by inactive planes:
    base_link_need = {mu: 0 for mu in range(4)}
    for mu, nu in inactive:
        base_link_need[mu] += 1
        base_link_need[nu] += 1

    deficit = {mu: base_link_need[mu] - base_link_budget[mu] for mu in range(4)}
    has_deficit = any(d > 0 for d in deficit.values())

    print(f"\n  Sign structure: {pos}+/{neg}-, inactive={inactive}")
    print(f"    Base link budget from active: {dict(base_link_budget)}")
    print(f"    Base link need for inactive:  {dict(base_link_need)}")
    print(f"    Deficit: {dict(deficit)}")
    print(f"    Proof grouping works: {'NO (deficit)' if has_deficit else 'YES'}")

    if has_deficit:
        # Check if a different grouping could work
        # Maybe pair inactive planes differently?
        print(f"    *** The proof's grouping strategy FAILS for this sign structure ***")
        print(f"    *** But c+Tr(P) = {c_tr} < 64, so the bound might still hold ***")

# ============================================================
# Part D: Verify F_x at identity for all vertices on L=3
# ============================================================

print("\n" + "=" * 70)
print("F_x AT IDENTITY FOR ALL VERTICES ON L=3")
print("=" * 70)

L = 3
n_test = np.array([1.0, 0.0, 0.0])

# At identity, B_sq = (s1 + s2 - s3 - s4) * n
# where s_i are the staggered signs
F_by_type = {}
for x in product(range(L), repeat=d):
    ss = get_sign_structure(x, L)
    ab_key = tuple(ss[(mu,nu)][2] for mu,nu in PLANES)

    F_x = 0.0
    for mu, nu in PLANES:
        a, b, _ = ss[(mu,nu)]
        # At identity: B = 2(a + b) * n
        B_coeff = 2 * (a + b)
        F_x += B_coeff**2

    if ab_key not in F_by_type:
        F_by_type[ab_key] = (F_x, [])
    F_by_type[ab_key][1].append(x)

total_F = 0
for ab_key, (F_val, verts) in F_by_type.items():
    total_F += F_val * len(verts)
    pos = sum(1 for s in ab_key if s > 0)
    neg = sum(1 for s in ab_key if s < 0)
    print(f"  Sign {pos}+/{neg}-: F_x(I) = {F_val:.0f}, count = {len(verts)}")

print(f"\n  Sum_x F_x(I) = {total_F:.0f}")
print(f"  |v|^2 = NE = {L**d * d}")
print(f"  Rayleigh quotient = {total_F / (L**d * d):.4f}")
print(f"  (Should be = lambda_max of full M at identity)")

print("\nDone.")
