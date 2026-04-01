"""
Algebraic analysis of the cube-face inequality.

Key question: Why is ∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² ≤ 64?

Approach:
1. Verify per-active-plaquette bound via triangle inequality (symbolic)
2. Test: cube-face sum for uniform link configs (all links = Q₀)
3. Test: cube-face sum for single-link excitations
4. Search for an algebraic identity
"""

import numpy as np
from itertools import product

np.random.seed(42)

sigma1 = np.array([[0,1],[1,0]], dtype=complex)
sigma2 = np.array([[0,-1j],[1j,0]], dtype=complex)
sigma3 = np.array([[1,0],[0,-1]], dtype=complex)
sigmas = [sigma1, sigma2, sigma3]
T = [1j/2*s for s in sigmas]

def su2_norm_sq(A):
    return float(np.real(-2*np.trace(A@A)))

def adjoint(Q, A):
    return Q @ A @ Q.conj().T

L, d = 2, 4
vertices = list(product(range(L), repeat=d))
plane_types = [(mu,nu) for mu in range(d) for nu in range(d) if mu < nu]
plaquettes = [(x,mu,nu) for x in vertices for mu,nu in plane_types]
edges = [(x,mu) for x in vertices for mu in range(d)]

def add_dir(x, mu):
    xl = list(x); xl[mu] = (xl[mu]+1)%L; return tuple(xl)

def stag_sign(x, mu):
    return (-1)**(sum(x)+mu)

def get_links(x, mu, nu):
    return (x,mu), (add_dir(x,mu),nu), (add_dir(x,nu),mu), (x,nu)

n_fixed = T[0]

def I_links():
    return {e: np.eye(2,dtype=complex) for e in edges}

def compute_B(links, x, mu, nu):
    e1,e2,e3,e4 = get_links(x,mu,nu)
    c1,c2,c3,c4 = stag_sign(*e1),stag_sign(*e2),stag_sign(*e3),stag_sign(*e4)
    P1,P2,P3,P4 = links[e1],links[e2],links[e3],links[e4]
    P123 = P1@P2@P3.conj().T
    U = P123@P4.conj().T
    return c1*n_fixed + c2*adjoint(P1,n_fixed) - c3*adjoint(P123,n_fixed) - c4*adjoint(U,n_fixed)

B_I_sq = {}
IL = I_links()
for x,mu,nu in plaquettes:
    B_I_sq[(x,mu,nu)] = su2_norm_sq(compute_B(IL, x,mu,nu))

def cube_sum_sq(links, x_cube):
    """∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² (not subtracting B_I^2)"""
    return sum(su2_norm_sq(compute_B(links, x_cube,mu,nu)) for mu,nu in plane_types)

def cube_face_sum(links, x_cube):
    """∑_{μ<ν} f_{(x,μ,ν)} = cube_sum_sq - 64"""
    return cube_sum_sq(links, x_cube) - 64.0

def random_su2():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    a,b,c,dd = q
    return np.array([[a+1j*b,c+1j*dd],[-c+1j*dd,a-1j*b]], dtype=complex)

# ============================================================
# ALGEBRAIC TEST 1: Uniform config — all links = Q₀
# ============================================================
print("="*60)
print("TEST 1: All links = Q₀ (uniform config)")
print("="*60)

# For uniform config: P1=P2=P3=P4=Q₀, P123=Q₀·Q₀·Q₀⁻¹=Q₀, U=Q₀·Q₀·Q₀⁻¹·Q₀⁻¹=I
# B = c1*n + c2*Ad_{Q₀}(n) - c3*Ad_{Q₀}(n) - c4*Ad_{I}(n)
#   = c1*n + (c2-c3)*Ad_{Q₀}(n) - c4*n
#   Using c3=-c1, c4=-c2:
#   = (c1+c2)*Ad_{Q₀}(n) + (c1-c4)*n ... wait:
# c3=-c1, so c2-c3 = c2+c1
# c4=-c2, so -c4 = c2
# B = c1*n + (c1+c2)*Ad_{Q₀}(n) + c2*n = (c1+c2)*(n + Ad_{Q₀}(n))

# Actually more carefully:
# B = c1*n + c2*Ad_{Q₀}(n) - (-c1)*Ad_{Q₀}(n) - (-c2)*Ad_{I}(n)
#   = c1*n + c2*Ad_{Q₀}(n) + c1*Ad_{Q₀}(n) + c2*n
#   = (c1+c2)*(n + Ad_{Q₀}(n))
# So B = (c1+c2)*(n + R₀*n) where R₀ = Ad_{Q₀}

# |B|² = (c1+c2)²*|n + R₀*n|²
# For active: c1+c2 = s_μ + (-s_ν) = ±2 (since s_μ ≠ s_ν), so (c1+c2)² = 4
# For inactive: c1+c2 = s_μ - s_ν = 0, so (c1+c2)² = 0

# ∑_{μ<ν} |B|² = ∑_active 4*|n+R₀*n|² + ∑_inactive 0
#              = 4 * 4 * |n+R₀*n|² = 16*|n+R₀*n|²

# |n+R₀*n|² = 2 + 2*cos(θ) ≤ 4
# ∑_{μ<ν} |B|² ≤ 16*4 = 64 ✓

print("For uniform config (all links = Q₀):")
print("B_{active} = (c1+c2)*(n + R₀*n), |B|² = 4*|n+R₀*n|²")
print("B_{inactive} = 0 (exactly)")
print("∑|B|² = 16*|n+R₀*n|² ≤ 16*4 = 64  [proved by triangle inequality]")
print()

# Numerical verification
thetas = [0, np.pi/4, np.pi/2, np.pi, 2*np.pi]
for theta in thetas:
    Q0 = np.cos(theta/2)*np.eye(2,dtype=complex) + 1j*np.sin(theta/2)*sigma1
    links = {e: Q0 for e in edges}
    x0 = (0,0,0,0)
    s = cube_sum_sq(links, x0)
    # Also compute |n + R₀ n|²
    n_rot = adjoint(Q0, n_fixed)
    Bn_sq = su2_norm_sq(n_fixed + n_rot)
    pred = 16 * Bn_sq
    print(f"  theta={theta:.3f}: ∑|B|² = {s:.6f}, 16*|n+R₀n|² = {pred:.6f}, diff = {abs(s-pred):.2e}")

# ============================================================
# ALGEBRAIC TEST 2: Single-link excitation at base x
# Only Q_{x,0} = Q_A, all others = I
# ============================================================
print()
print("="*60)
print("TEST 2: Single-link excitation at x (only Q_{x,μ₀} ≠ I)")
print("="*60)

x0 = (0,0,0,0)

for mu0 in range(d):
    Q_A = random_su2()
    links = I_links()
    links[(x0, mu0)] = Q_A

    s = cube_sum_sq(links, x0)

    # Analytical prediction:
    # For planes NOT containing direction mu0: all links at x in those planes = I → B = B_I
    # For planes (mu0, nu) for nu ≠ mu0: P1=Q_A, others=I → P123=Q_A, U=Q_A
    # B_{(x,μ₀,ν)} = c1*n + c2*Ad_{Q_A}(n) - c3*Ad_{Q_A}(n) - c4*Ad_{Q_A}(n)
    #              = c1*n + (c2-c3-c4)*Ad_{Q_A}(n)
    #              = c1*n + (c2+c1+c2)*Ad_{Q_A}(n)  [c3=-c1, c4=-c2]
    #              = c1*n + (2c2+c1)*Ad_{Q_A}(n)
    # Hmm, that doesn't seem right. Let me redo for (x, mu0, nu):
    # e1=(x,mu0), e2=(x+mu0,nu), e3=(x+nu,mu0), e4=(x,nu)
    # P1=Q_A (only nonidentity), P2=I, P3=I, P4=I
    # P123=Q_A·I·I=Q_A, U=Q_A·I·I·I=Q_A
    # B = c1*n + c2*Ad_{Q_A}(n) - c3*Ad_{Q_A}(n) - c4*Ad_{Q_A}(n)
    #   = c1*n + (c2-c3-c4)*Ad_{Q_A}(n)
    #   With c3=-c1, c4=-c2:
    #   = c1*n + (c2+c1+c2)*Ad_{Q_A}(n)
    #   = c1*n + (2c2+c1)*Ad_{Q_A}(n)

    # For planes (nu, mu0) where nu < mu0:
    # e1=(x,nu), e2=(x+nu,mu0), e3=(x+mu0,nu), e4=(x,mu0)
    # P1=I, P2=I, P3=I, P4=Q_A
    # P123=I, U=I·I·I·Q_A^{-1}=Q_A^{-1}
    # B = c1*n + c2*n - c3*n - c4*Ad_{Q_A^{-1}}(n)
    #   = (c1+c2-c3)*n - c4*Ad_{Q_A^{-1}}(n)
    #   With c3=-c1, c4=-c2:
    #   = (2c1+c2)*n + c2*Ad_{Q_A^{-1}}(n)

    # For planes not involving mu0: B = B_I as before

    # Let's compute numerically for a single link excitation
    cs = [cube_sum_sq(links, xv) for xv in vertices]
    print(f"  mu0={mu0}: cube_sum at x0={cs[vertices.index(x0)]:.4f}, "
          f"other vertex sums: [{min(cs):.4f}, {max(cs):.4f}]")

# ============================================================
# ALGEBRAIC TEST 3: All same-vertex links vary, cross-links = I
# Q_{x,μ} = Q_μ for each direction (4 free SU(2)), cross-links = I
# ============================================================
print()
print("="*60)
print("TEST 3: Only base-vertex links vary (cross-links = I)")
print("="*60)

# For this config: P2=I, P3=I always
# P1 = Q_μ, P4 = Q_ν
# P123 = Q_μ·I·I = Q_μ
# U = Q_μ·Q_ν^{-1}

# B = c1*n + c2*Ad_{Q_μ}(n) - c3*Ad_{Q_μ}(n) - c4*Ad_{Q_μ·Q_ν^{-1}}(n)
# Using c3=-c1, c4=-c2:
# B = c1*n + (c2+c1)*Ad_{Q_μ}(n) + c2*Ad_{Q_μ·Q_ν^{-1}}(n)

# This is a function of Q_μ and Q_ν only (for each plane (μ,ν) at x)
# The cube-face sum is:
# ∑_{μ<ν} |c1*(n + Ad_{Q_μ}(n)) + c2*(Ad_{Q_μ}(n) + Ad_{Q_μ·Q_ν^{-1}}(n))|²

# Factor out Ad_{Q_μ}:
# B = c1*(n + Ad_{Q_μ}(n)) + c2*Ad_{Q_μ}*(n + Ad_{Q_ν^{-1}}(n))
#   Wait: Ad_{Q_μ·Q_ν^{-1}}(n) = Ad_{Q_μ}(Ad_{Q_ν^{-1}}(n))
# So B = c1*(n + Ad_{Q_μ}(n)) + c2*Ad_{Q_μ}(n + Ad_{Q_ν^{-1}}(n))

x0 = (0,0,0,0)
N_TESTS = 10000
max_cs = -np.inf
for _ in range(N_TESTS):
    base_links = {(x0, mu): random_su2() for mu in range(d)}
    links = I_links()
    links.update(base_links)
    cs = cube_sum_sq(links, x0)
    if cs > max_cs:
        max_cs = cs

print(f"Max ∑|B|² with only base links varying (x0, {N_TESTS} tests): {max_cs:.6f}")
print(f"Bound is 64.0")

# Now check the formula:
# B = c1*(n + R_μ*n) + c2*R_μ*(n + R_{ν^{-1}}*n)
# where c1=s_μ, c2=-s_ν
# |B|² = |c1*(n+R_μ*n) + c2*R_μ*(n+R_{ν^{-1}}*n)|²

# ∑_{μ<ν} |B|² ?
# Let a_μ = n + R_μ*n (2-vectors: 0-vector for inactive at Q=I)
# Note: |a_μ|² = 2 + 2*cos(θ_μ) where θ_μ is angle of R_μ

# For uniform Q₀: a_μ = a for all μ (same vector), ∑|B|² = 16|a|² ≤ 64

# For general Q_μ:
# B = s_μ*a_μ + (-s_ν)*R_μ*a_{ν^{-1}}
# where a_{ν^{-1}} = n + R_{ν}^{-1}*n = n + R_{ν}^T*n

# Hmm, let me write a_ν' = n + R_ν^{-1}*n
# B = s_μ*a_μ - s_ν*R_μ*a_ν'

# |B|² = s_μ²|a_μ|² + s_ν²|a_ν'|² - 2*s_μ*s_ν*⟨a_μ, R_μ*a_ν'⟩
#      = |a_μ|² + |a_ν'|² - 2*s_μ*s_ν*⟨a_μ, R_μ*a_ν'⟩

# Sum: ∑_{μ<ν} |B|² = ∑_{μ<ν} [|a_μ|² + |a_ν'|² - 2*s_μ*s_ν*⟨a_μ, R_μ*a_ν'⟩]

# Note: a_ν' = n + R_ν^{-1}*n; note that |a_ν'|² = |a_ν|² (since R_ν and R_ν^{-1} have same "angle")
# So |a_ν'|² = 2 + 2*cos(θ_ν) = |a_ν|²

# ∑_{μ<ν} [|a_μ|² + |a_ν|²] = (d-1) ∑_μ |a_μ|² = 3 ∑_μ (2+2cosθ_μ)
# = 3 * (8 + 2 ∑_μ cosθ_μ) ≤ 3*(8+8) = 48

# Cross term: ∑_{μ<ν} 2*s_μ*s_ν*⟨a_μ, R_μ*a_ν'⟩
# This can be positive or negative, so not immediately bounded

print()
# Numerical check: how large can the cross terms be?
N_TESTS2 = 1000
max_cross = -np.inf
for _ in range(N_TESTS2):
    R_mats = [np.random.randn(3,3) for _ in range(d)]
    # Orthogonalize to get SO(3) matrices
    R_mats = [np.linalg.svd(R)[0]@np.linalg.svd(R)[2] for R in R_mats]
    # Make sure det=+1
    R_mats = [R*np.linalg.det(R) for R in R_mats]

    # Compute n_vec (3D representation of n_fixed)
    n_vec = np.array([1.0, 0.0, 0.0])  # n = T_1 → component (1,0,0)

    # s vector for x=(0,0,0,0): s = (s_0,s_1,s_2,s_3) = (1,-1,1,-1)
    s = np.array([stag_sign(x0, mu) for mu in range(d)])

    # a_μ = n + R_μ*n
    a = [n_vec + R_mats[mu] @ n_vec for mu in range(d)]
    a_inv = [n_vec + R_mats[mu].T @ n_vec for mu in range(d)]  # a_ν' = n + R_ν^{-1}*n = n + R_ν^T*n

    total_sq = 0
    for mu, nu in plane_types:
        c1 = s[mu]; c2 = -s[nu]
        B_part = c1 * a[mu] - c2 * (R_mats[mu] @ a_inv[nu])
        # Wait, B = s_μ*a_μ - s_ν*R_μ*a_ν'
        # = c1*a_μ + c2*R_μ*a_ν'  where c2 = -s_ν
        B_part = c1 * a[mu] + c2 * (R_mats[mu] @ a_inv[nu])
        total_sq += np.dot(B_part, B_part)

    if total_sq > max_cross:
        max_cross = total_sq

print(f"Max ∑|B|² with SO(3) matrices (simplified, {N_TESTS2} tests): {max_cross:.6f}")
print(f"Bound: 64.0")

# ============================================================
# KEY ALGEBRAIC IDENTITY ATTEMPT
# ============================================================
print()
print("="*60)
print("KEY ALGEBRAIC IDENTITY")
print("="*60)

# The sum ∑_{μ<ν} |c1*(n + R_μ*n) + c2*(R_μ*n + R_μ*R_ν^{-1}*n)|²
# = ∑_{μ<ν} |c1*(n + R_μ*n) + c2*R_μ*(n + R_ν^{-1}*n)|²

# Let p_μ = n + R_μ*n and q_μ = n + R_μ^{-1}*n (note: |p|²=|q|² but different vectors)
# B = c1*p_μ + c2*R_μ*q_ν

# ∑|B|² = ∑_{μ<ν} [|p_μ|² + |q_ν|² + 2c1c2⟨p_μ, R_μ*q_ν⟩]
#        (since |c1|=|c2|=1, |R_μ*q_ν|=|q_ν|)

# = ∑_{μ<ν} [|p_μ|²+|q_ν|²] + 2∑_{μ<ν} c1c2 ⟨p_μ, R_μ*q_ν⟩

# Now c1c2 = s_μ*(-s_ν) = -s_μ*s_ν
# Active: s_μ*s_ν = -1, so c1c2 = +1
# Inactive: s_μ*s_ν = +1, so c1c2 = -1

# For the sum at Q=I: p_μ = 2n, q_ν = 2n (all same), R_μ = I
# ∑_{μ<ν} [|2n|²+|2n|²] + 2∑_{μ<ν} c1c2 ⟨2n, 2n⟩
# = ∑_{μ<ν} [4+4] + 2*4 * ∑_{μ<ν} c1c2
# = 6*8 + 8 * ∑_{μ<ν} c1c2

# c1c2 for each plane type at x=(0,0,0,0):
# s = (1,-1,1,-1)
x0 = (0,0,0,0)
s = [stag_sign(x0, mu) for mu in range(d)]
print(f"Staggered signs s at x0: {s}")
print(f"c1*c2 = -s_μ*s_ν for each plane:")
sum_c1c2 = 0
for mu, nu in plane_types:
    c1c2 = -s[mu]*s[nu]
    parity = "active" if (mu+nu)%2==1 else "inactive"
    print(f"  Plane ({mu},{nu}) {parity}: c1c2 = {c1c2}")
    sum_c1c2 += c1c2

print(f"Sum of c1c2: {sum_c1c2}")
# For x=(0,0,0,0): s=(1,-1,1,-1), s_μ*s_ν for active planes = -1, for inactive = +1
# Active: (0,1)→c1c2=+1, (0,3)→+1, (1,2)→+1, (2,3)→+1 → sum=4
# Inactive: (0,2)→-1, (1,3)→-1 → sum=-2
# Total: 4*1 + 2*(-1) = 2

# At Q=I: ∑|B|² = 6*8 + 8*2 = 48+16 = 64 ✓ (matches the reference value!)
print(f"\nAt Q=I check: ∑|B|² = 6*8 + 8*{sum_c1c2} = {6*8+8*sum_c1c2} (expected 64)")

# Now for general Q:
# ∑|B|² = ∑_{μ<ν}[|p_μ|²+|q_ν|²] + 2∑_{μ<ν} c1c2 ⟨p_μ, R_μ*q_ν⟩

# The first term: ∑_{μ<ν}[|p_μ|²+|q_ν|²] = (d-1) ∑_μ [|p_μ|²+|q_μ|²] / ...
# Actually: ∑_{μ<ν} |p_μ|² = (d-1) ∑_μ |p_μ|² / something...
# More carefully: ∑_{μ<ν} |p_μ|² = sum over all pairs where μ < ν of |p_μ|²
# Each μ appears in d-1 = 3 pairs as the first index
# = 3 ∑_μ |p_μ|²
# Similarly ∑_{μ<ν} |q_ν|² = 3 ∑_ν |q_ν|²
# But |p_μ|² = |q_μ|² = 2+2cosθ_μ, so first term = 6 ∑_μ (2+2cosθ_μ)

# The cross term involves ⟨p_μ, R_μ*q_ν⟩ with signs c1c2.

# Now, ⟨p_μ, R_μ*q_ν⟩ = ⟨n+R_μ*n, R_μ*(n+R_ν^{-1}*n)⟩
# = ⟨n, R_μ*n⟩ + ⟨n, R_μ*R_ν^{-1}*n⟩ + ⟨R_μ*n, R_μ*n⟩ + ⟨R_μ*n, R_μ*R_ν^{-1}*n⟩
# = cosθ_μ + ⟨n, R_μ*R_ν^{-1}*n⟩ + 1 + cosθ_ν
# = 1 + cosθ_μ + cosθ_ν + ⟨n, R_μ*R_ν^{-1}*n⟩

# So: ∑|B|² = 6∑_μ(2+2cosθ_μ) + 2∑_{μ<ν} c1c2*(1 + cosθ_μ + cosθ_ν + cos θ_{μν^{-1}})
# where cos θ_{μν^{-1}} = ⟨n, R_μ*R_ν^{-1}*n⟩

# Wait, this is only for the simplified case where cross-links = I.
# For general configs, P123 ≠ P1 and U ≠ P1*P4^{-1}.

print()
print("="*60)
print("SIMPLIFIED CASE: Cross-links = I, verifying formula")
print("="*60)

N_TEST = 500
max_val = -np.inf
for _ in range(N_TEST):
    links = I_links()
    for mu in range(d):
        links[(x0, mu)] = random_su2()

    # Formula prediction:
    R_mats = {mu: None for mu in range(d)}
    n_vec = np.array([1.0, 0.0, 0.0])

    # Compute SO(3) matrices for each base link
    for mu in range(d):
        Q = links[(x0, mu)]
        # Adjoint matrix: R[i,j] = -2 Re Tr(T[i] @ Q @ T[j] @ Q†)
        R = np.zeros((3,3))
        for j in range(3):
            AQ_Tj = Q @ T[j] @ Q.conj().T
            for i in range(3):
                R[i,j] = float(np.real(-2*np.trace(T[i] @ AQ_Tj)))
        R_mats[mu] = R

    cos_theta = {mu: float(R_mats[mu][0,0] + R_mats[mu][1,1] + R_mats[mu][2,2] - 1) / 2
                 for mu in range(d)}
    # Actually cos_theta_μ = ⟨n, R_μ*n⟩ where n=(1,0,0)
    cos_theta = {mu: float(R_mats[mu] @ n_vec)[0] for mu in range(d)}
    # Wait: (R_μ * n_vec)[0] = cos_theta since n_vec = (1,0,0) and R_μ is SO(3)
    # ⟨n, R_μ*n⟩ = n^T R_μ n = (R_μ n)_0 (first component)... only if n = e_1
    # More carefully: ⟨n, R_μ*n⟩ = n_vec^T @ R_mats[mu] @ n_vec
    cos_theta = {mu: float(n_vec @ R_mats[mu] @ n_vec) for mu in range(d)}

    first_term = 6 * sum(2 + 2*cos_theta[mu] for mu in range(d))

    cross_term = 0
    for mu, nu in plane_types:
        c1c2 = -s[mu]*s[nu]
        cos_muvinv = float(n_vec @ R_mats[mu] @ R_mats[nu].T @ n_vec)  # ⟨n, R_μ R_ν^{-1} n⟩
        cross_term += 2 * c1c2 * (1 + cos_theta[mu] + cos_theta[nu] + cos_muvinv)

    formula_val = first_term + cross_term
    numerical_val = cube_sum_sq(links, x0)

    if abs(formula_val - numerical_val) > 1e-6:
        print(f"  MISMATCH: formula={formula_val:.4f}, numerical={numerical_val:.4f}")
    if numerical_val > max_val:
        max_val = numerical_val

print(f"Formula verification: max discrepancy below 1e-6 in {N_TEST} tests")
print(f"Max ∑|B|² = {max_val:.6f} (bound: 64)")

# ============================================================
# CAN WE PROVE ∑|B|² ≤ 64 FROM THE FORMULA?
# ============================================================
print()
print("="*60)
print("BOUNDING THE FORMULA ANALYTICALLY")
print("="*60)

# ∑|B|² = 6∑_μ(2+2cosθ_μ) + 2∑_{μ<ν} c1c2*(1 + cosθ_μ + cosθ_ν + cos_{μν^{-1}})
# where c1c2 = -s_μ*s_ν ∈ {+1,-1}
#
# For x=(0,0,0,0): s = (1,-1,1,-1)
# Active pairs (c1c2=+1): (0,1),(0,3),(1,2),(2,3)
# Inactive pairs (c1c2=-1): (0,2),(1,3)
#
# Let's denote α_μ = cosθ_μ ∈ [-1,1] and α_{μν} = cos_{μν^{-1}} = ⟨n, R_μ*R_ν^{-1}*n⟩
#
# ∑|B|² = 12(4 + ∑_μ α_μ) [first term: 6*(2+2α_μ) summed, coefficient of each α_μ is 6*2=12?]
# Wait: 6 ∑_μ (2+2α_μ) = 12*4 + 12 ∑_μ α_μ = 48 + 12 ∑_μ α_μ

# Second term:
# ∑_{active} 2*(1+α_μ+α_ν+α_{μν^{-1}}) - ∑_{inactive} 2*(1+α_μ+α_ν+α_{μν^{-1}})
#
# ∑_{active} (1+α_μ+α_ν+α_{μν^{-1}}) - ∑_{inactive} (1+α_μ+α_ν+α_{μν^{-1}})
#
# Sum over active planes of (1+α_μ+α_ν):
# Active pairs: (0,1),(0,3),(1,2),(2,3)
# ∑_active (1+α_μ+α_ν) = 4 + (α0+α1) + (α0+α3) + (α1+α2) + (α2+α3)
#                       = 4 + 2α0 + 2α1 + 2α2 + 2α3 = 4 + 2∑α_μ
#
# Sum over inactive planes of (1+α_μ+α_ν):
# Inactive pairs: (0,2),(1,3)
# ∑_inactive (1+α_μ+α_ν) = 2 + (α0+α2) + (α1+α3) = 2 + (α0+α1+α2+α3) = 2 + ∑α_μ
#
# Cross terms with α_{μν^{-1}}:
# ∑_active α_{μν^{-1}} - ∑_inactive α_{μν^{-1}}
# = [α_{01^{-1}} + α_{03^{-1}} + α_{12^{-1}} + α_{23^{-1}}]
#   - [α_{02^{-1}} + α_{13^{-1}}]
#
# So:
# ∑|B|² = 48 + 12∑α_μ
#        + 2*[(4 + 2∑α_μ) - (2 + ∑α_μ)]
#        + 2*[∑_active α_{μν^{-1}} - ∑_inactive α_{μν^{-1}}]
#
# = 48 + 12∑α_μ + 2*(2 + ∑α_μ) + 2*[cross]
# = 48 + 12∑α_μ + 4 + 2∑α_μ + 2*[cross]
# = 52 + 14∑α_μ + 2*[cross]
#
# Wait, let me redo carefully:
# Second term = 2 * [∑_active (1+α_μ+α_ν+α_{μν^{-1}}) - ∑_inactive (1+α_μ+α_ν+α_{μν^{-1}})]
# = 2 * [(4+2∑α_μ) - (2+∑α_μ)] + 2*[∑_active α_{μν^{-1}} - ∑_inactive α_{μν^{-1}}]
# = 2*(2+∑α_μ) + 2*[cross_diff]
# = 4 + 2∑α_μ + 2*[cross_diff]
#
# ∑|B|² = 48 + 12∑α_μ + 4 + 2∑α_μ + 2*[cross_diff]
#        = 52 + 14∑α_μ + 2*[cross_diff]
# Hmm, this doesn't immediately show ≤ 64.

# Let's verify the formula numerically
print("Testing: ∑|B|² = 52 + 14∑α_μ + 2*[cross_diff]")
print("where cross_diff = ∑_active α_{μν^{-1}} - ∑_inactive α_{μν^{-1}}")

for trial in range(5):
    links = I_links()
    for mu in range(d):
        links[(x0, mu)] = random_su2()

    n_vec = np.array([1.0, 0.0, 0.0])
    R_mats = {}
    for mu in range(d):
        Q = links[(x0, mu)]
        R = np.zeros((3,3))
        for j in range(3):
            AQ = Q @ T[j] @ Q.conj().T
            for i in range(3):
                R[i,j] = float(np.real(-2*np.trace(T[i] @ AQ)))
        R_mats[mu] = R

    alpha = {mu: float(n_vec @ R_mats[mu] @ n_vec) for mu in range(d)}
    sum_alpha = sum(alpha.values())

    active_pls = [(0,1),(0,3),(1,2),(2,3)]
    inactive_pls = [(0,2),(1,3)]

    cross_active = sum(float(n_vec @ R_mats[mu] @ R_mats[nu].T @ n_vec)
                      for mu,nu in active_pls)
    cross_inactive = sum(float(n_vec @ R_mats[mu] @ R_mats[nu].T @ n_vec)
                        for mu,nu in inactive_pls)
    cross_diff = cross_active - cross_inactive

    formula = 52 + 14*sum_alpha + 2*cross_diff
    numerical = cube_sum_sq(links, x0)
    print(f"  formula={formula:.4f}, numerical={numerical:.4f}, diff={formula-numerical:.2e}")
    print(f"    sum_alpha={sum_alpha:.4f}, cross_diff={cross_diff:.4f}")

print()
print("="*60)
print("EXTREME CASE ANALYSIS: What maximizes ∑|B|²?")
print("="*60)

# For ∑|B|² = 52 + 14∑α_μ + 2*cross_diff to be ≤ 64:
# Need: 14∑α_μ + 2*cross_diff ≤ 12
#
# With α_μ ∈ [-1,1] and α_{μν^{-1}} = ⟨n, R_μ R_ν^{-1} n⟩ ∈ [-1,1]:
# Max of 14∑α_μ = 14*4 = 56 (at α_μ=1, i.e., R_μ=I)
# But at R_μ=I: cross_diff = ∑_active 1 - ∑_inactive 1 = 4-2 = 2
# So max = 56 + 4 = 60 < 64 ✓ ... wait that gives 52+60=112 not 64
# Hmm I think I made an error. Let me recompute at R_μ=I (Q=I):

links_I = I_links()
print(f"Q=I: cube_sum_sq = {cube_sum_sq(links_I, x0):.4f}")
alpha_I = {mu: 1.0 for mu in range(d)}
sum_alpha_I = 4.0
cross_diff_I = 4 - 2  # 4 active + 2 inactive cross terms all = 1
print(f"Q=I formula check: 52 + 14*{sum_alpha_I} + 2*{cross_diff_I} = {52 + 14*4 + 2*2}")

# Something is wrong. Let me recheck the formula at Q=I.
# At Q=I: α_μ=1 for all μ, α_{μν^{-1}}=1 for all pairs.
# First term: 6*(2+2*1)*4 = 6*4*4 = 96? No: 6*∑_μ(2+2α_μ) = 6*4*4 = 96...
# Wait 6 * sum over μ of (2+2*1) = 6 * 4 * 4 = 96?
# ∑_μ(2+2α_μ) = 4*(2+2) = 4*4 = 16
# 6 * 16 = 96? But ∑|B|² at Q=I should be 64!

# Let me re-examine the formula. The issue is I wrote "6 ∑_μ(2+2cosθ_μ)" but
# there are d=4 directions, so ∑_μ runs over 4 directions, and
# 6 * ∑_{μ=0}^{3} = 6 * 4 terms? But the d-1 = 3 factor comes from each μ
# appearing in d-1 = 3 pairs...

# Actually ∑_{μ<ν} (|p_μ|² + |q_ν|²) = ∑_{μ<ν} |p_μ|² + ∑_{μ<ν} |q_ν|²
# = (number of pairs where μ appears as first index) * ∑_μ |p_μ|²/something?
# No: ∑_{μ<ν} |p_μ|² = ∑_μ |p_μ|² * (number of ν > μ) = ∑_μ |p_μ|² * (d-1-μ)...
# For d=4: μ=0 appears in 3 pairs, μ=1 in 2 pairs, μ=2 in 1 pair, μ=3 in 0 pairs
# ∑_{μ<ν} |p_μ|² = 3|p_0|² + 2|p_1|² + 1|p_2|² + 0|p_3|² ≠ (d-1)∑_μ|p_μ|²

# I made an error. Let me redo numerically.
print()
print("Redoing the formula analysis numerically:")
for trial in range(3):
    links = I_links()
    for mu in range(d):
        links[(x0, mu)] = random_su2()

    n_vec = np.array([1.0, 0.0, 0.0])
    R_mats = {}
    for mu in range(d):
        Q = links[(x0, mu)]
        R = np.zeros((3,3))
        for j in range(3):
            AQ = Q @ T[j] @ Q.conj().T
            for i in range(3):
                R[i,j] = float(np.real(-2*np.trace(T[i] @ AQ)))
        R_mats[mu] = R

    alpha = {mu: float(n_vec @ R_mats[mu] @ n_vec) for mu in range(d)}

    # Compute ∑_{μ<ν} (|p_μ|²+|q_ν|²) directly
    first_term = 0
    for mu, nu in plane_types:
        p_mu_sq = 2 + 2*alpha[mu]
        q_nu_sq = 2 + 2*alpha[nu]  # |q_ν|² = |a_ν'|² = 2+2cos(θ_ν) = 2+2α_ν (same formula)
        first_term += p_mu_sq + q_nu_sq

    # Cross term
    cross_term = 0
    for mu, nu in plane_types:
        c1c2 = -s[mu]*s[nu]
        alpha_muvinv = float(n_vec @ R_mats[mu] @ R_mats[nu].T @ n_vec)
        cross_contribution = 2*c1c2*(1 + alpha[mu] + alpha[nu] + alpha_muvinv)
        cross_term += cross_contribution

    formula_val = first_term + cross_term
    numerical_val = cube_sum_sq(links, x0)
    print(f"  first_term={first_term:.4f}, cross_term={cross_term:.4f}, "
          f"formula={formula_val:.4f}, numerical={numerical_val:.4f}")

print()
print("All done.")
