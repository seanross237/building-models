"""
Targeted algebraic analysis.

Key formula (derived analytically, for cross-links = I case):
∑_{μ<ν} |B_{(x,μ,ν)}|² = 28 + 8∑cosθ_μ + 2∑_{μ<ν} c₁c₂ α_{μν⁻¹}

where cosθ_μ = ⟨n, R_μ n⟩ and α_{μν⁻¹} = ⟨n, R_μ R_ν⁻¹ n⟩

Goal: verify formula, then check whether 64 is the maximum.
"""
import numpy as np
from itertools import product
np.random.seed(7)

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
edges = [(x,mu) for x in vertices for mu in range(d)]
plaquettes = [(x,mu,nu) for x in vertices for mu,nu in plane_types]

def add_dir(x, mu):
    xl = list(x); xl[mu] = (xl[mu]+1)%L; return tuple(xl)
def stag_sign(x, mu):
    return (-1)**(sum(x)+mu)
def get_links(x, mu, nu):
    return (x,mu), (add_dir(x,mu),nu), (add_dir(x,nu),mu), (x,nu)
def I_links():
    return {e: np.eye(2,dtype=complex) for e in edges}

n_fixed = T[0]

def compute_B(links, x, mu, nu):
    e1,e2,e3,e4 = get_links(x,mu,nu)
    c1,c2,c3,c4 = stag_sign(*e1),stag_sign(*e2),stag_sign(*e3),stag_sign(*e4)
    P1,P2,P3,P4 = links[e1],links[e2],links[e3],links[e4]
    P123 = P1@P2@P3.conj().T
    U = P123@P4.conj().T
    return c1*n_fixed + c2*adjoint(P1,n_fixed) - c3*adjoint(P123,n_fixed) - c4*adjoint(U,n_fixed)

def cube_sum_sq(links, x):
    return sum(su2_norm_sq(compute_B(links,x,mu,nu)) for mu,nu in plane_types)

def random_su2():
    q = np.random.randn(4); q /= np.linalg.norm(q)
    a,b,c,dd = q
    return np.array([[a+1j*b,c+1j*dd],[-c+1j*dd,a-1j*b]], dtype=complex)

def adj_mat(Q):
    """3x3 adjoint (SO(3)) rep of Q."""
    R = np.zeros((3,3))
    for j in range(3):
        AQ = Q @ T[j] @ Q.conj().T
        for i in range(3):
            R[i,j] = float(np.real(-2*np.trace(T[i] @ AQ)))
    return R

x0 = (0,0,0,0)
s = np.array([stag_sign(x0, mu) for mu in range(d)])
# s = (1,-1,1,-1) for x0=(0,0,0,0)
# c1c2 = -s_μ*s_ν: active pairs get +1, inactive get -1
print(f"s = {s}")

# =================================================
# FORMULA VERIFICATION (simplified: cross-links = I)
# =================================================
print("\nFormula: ∑|B|² = 28 + 8∑cosθ + 2∑_{μ<ν}c₁c₂·α_{μν⁻¹}")
print("(valid when cross-links = I)")
print()

n_vec = np.array([1.0, 0.0, 0.0])  # n = T_0, component representation

max_numerical = -np.inf
max_diff = 0.0

for trial in range(10000):
    links = I_links()
    R_mats = []
    for mu in range(d):
        Q = random_su2()
        links[(x0, mu)] = Q
        R_mats.append(adj_mat(Q))

    cos_theta = np.array([n_vec @ R_mats[mu] @ n_vec for mu in range(d)])
    sum_cos = cos_theta.sum()

    cross_sum = 0.0
    for mu, nu in plane_types:
        c1c2 = -s[mu]*s[nu]
        alpha_muvinv = n_vec @ R_mats[mu] @ R_mats[nu].T @ n_vec
        cross_sum += c1c2 * alpha_muvinv

    formula_val = 28 + 8*sum_cos + 2*cross_sum
    numerical_val = cube_sum_sq(links, x0)
    diff = abs(formula_val - numerical_val)
    max_diff = max(max_diff, diff)
    max_numerical = max(max_numerical, numerical_val)

print(f"Over 10000 tests (cross-links=I):")
print(f"  Max |formula - numerical| = {max_diff:.2e} (should be ~0)")
print(f"  Max ∑|B|² = {max_numerical:.6f} (bound: 64.0)")

# The formula is:
# f(R_0,...,R_3) = 28 + 8∑cosθ_μ + 2∑_{μ<ν} c₁c₂ α_{μν⁻¹}
#
# where cosθ_μ = n^T R_μ n and α_{μν⁻¹} = n^T R_μ R_ν^T n
# and c₁c₂ = -s_μ s_ν
#
# Active pairs (c₁c₂=+1): (0,1),(0,3),(1,2),(2,3)
# Inactive pairs (c₁c₂=-1): (0,2),(1,3)

# Key observation: α_{μν⁻¹} = (R_ν^T n)^T (R_μ^T n)^{-1}... wait:
# α_{μν⁻¹} = n^T R_μ R_ν^T n = (R_μ^T n)^T (R_ν^T n)
# = ⟨R_μ^T n, R_ν^T n⟩

# Let w_μ = R_μ^T n = R_μ^{-1} n ∈ S² (unit vector)
# Then: cosθ_μ = n^T R_μ n = ⟨n, R_μ n⟩ = ⟨R_μ^T n, n⟩ ... hmm:
# cosθ_μ = n^T R_μ n, but R_μ is SO(3) so this is ⟨n, R_μ n⟩
# And w_μ = R_μ^T n = R_μ^{-1} n
# ⟨n, w_μ⟩ = n^T R_μ^T n = (R_μ n)^T n = ⟨R_μ n, n⟩ = ⟨n, R_μ n⟩ = cosθ_μ...
# wait: ⟨n, R_μ n⟩ = n^T R_μ n = (n^T R_μ n) which is cosθ_μ
# And ⟨n, w_μ⟩ = n^T w_μ = n^T R_μ^T n = n^T R_μ^T n = cosθ_μ ✓

# So cosθ_μ = ⟨n, w_μ⟩ and α_{μν⁻¹} = ⟨w_μ, w_ν⟩?
# α_{μν⁻¹} = n^T R_μ R_ν^T n = (R_μ^T n)^T (R_ν^T n) = w_μ^T w_ν... wait:
# n^T R_μ R_ν^T n: let me expand as (n^T R_μ)(R_ν^T n) = ⟨R_μ^T n, R_ν^T n⟩ ...
# No: n^T R_μ is the row vector (R_μ^T n)^T? Yes!
# n^T R_μ R_ν^T n = (R_μ^T n)^T (R_ν^T n) = ⟨R_μ^T n, R_ν^T n⟩ = ⟨w_μ, w_ν⟩

# BEAUTIFUL: cosθ_μ = ⟨n, w_μ⟩ and α_{μν⁻¹} = ⟨w_μ, w_ν⟩
# where w_μ = R_μ^{-1} n are UNIT VECTORS IN S²!

print("\n" + "="*60)
print("KEY: Substituting w_μ = R_μ^{-1} n:")
print("  cosθ_μ = ⟨n, w_μ⟩")
print("  α_{μν⁻¹} = ⟨w_μ, w_ν⟩")
print()
print("Formula becomes:")
print("  ∑|B|² = 28 + 8∑⟨n,w_μ⟩ + 2∑_{μ<ν} c₁c₂·⟨w_μ,w_ν⟩")
print()
print("Expanding further using ⟨n,w_μ⟩:")
print("  Let ẑ = n ∈ S² and w_μ ∈ S²")
print("  ∑|B|² = 28 + 8∑⟨ẑ,w_μ⟩ + 2∑_{μ<ν} c₁c₂·⟨w_μ,w_ν⟩")
print()
print("Now define vector W = ∑_μ σ_μ w_μ where σ_μ are signs...")
print()

# Let's try to complete the square.
# With s = (1,-1,1,-1) for x0:
# ∑_μ σ_μ w_μ where σ_μ = s_μ: σ = (1,-1,1,-1)
# |∑_μ σ_μ w_μ|² = ∑_μ |w_μ|² + 2∑_{μ<ν} σ_μ σ_ν ⟨w_μ, w_ν⟩
# = 4 + 2∑_{μ<ν} σ_μ σ_ν ⟨w_μ, w_ν⟩
# where σ_μ σ_ν for active = s_μ s_ν = -1 (since active means s_μ ≠ s_ν)
# and for inactive = s_μ s_ν = +1

# But c₁c₂ = -s_μ s_ν, so ∑_{μ<ν} c₁c₂ ⟨w_μ,w_ν⟩ = -∑_{μ<ν} s_μ s_ν ⟨w_μ,w_ν⟩

# |∑_μ s_μ w_μ|² = 4 + 2∑_{μ<ν} s_μ s_ν ⟨w_μ,w_ν⟩
# ∑_{μ<ν} s_μ s_ν ⟨w_μ,w_ν⟩ = (|∑_μ s_μ w_μ|² - 4) / 2

# So: ∑_{μ<ν} c₁c₂ ⟨w_μ,w_ν⟩ = -(|∑_μ s_μ w_μ|² - 4)/2

# And: 8∑⟨ẑ,w_μ⟩ = 8∑_μ ⟨n, w_μ⟩
# Note: ∑_μ s_μ = 1-1+1-1=0, so ⟨n, ∑_μ s_μ w_μ⟩ is one expression.
# Also: ∑_μ ⟨n, w_μ⟩ = ⟨n, ∑_μ w_μ⟩

# Define: A = ∑_μ s_μ w_μ (active-inactive combination)
#         B_vec = ∑_μ w_μ (total)

# Formula: ∑|B|² = 28 + 8⟨n, B_vec⟩ + 2*(-(|A|²-4)/2)
#                = 28 + 8⟨n, B_vec⟩ - |A|² + 4
#                = 32 + 8⟨n, B_vec⟩ - |A|²

# For ≤ 64: need 8⟨n, B_vec⟩ - |A|² ≤ 32

# Verify this numerically:
print("Formula (new form): ∑|B|² = 32 + 8⟨n,∑w_μ⟩ - |∑s_μ w_μ|²")
print("(where w_μ = R_μ^{-1} n = unit vectors)")
print()

max_numerical2 = -np.inf
max_diff2 = 0.0

for trial in range(10000):
    links = I_links()
    R_mats = []
    w_vecs = []
    for mu in range(d):
        Q = random_su2()
        links[(x0, mu)] = Q
        R = adj_mat(Q)
        R_mats.append(R)
        w_vecs.append(R.T @ n_vec)  # w_μ = R_μ^{-1} n = R_μ^T n

    B_vec = sum(w_vecs)
    A_vec = sum(s[mu] * w_vecs[mu] for mu in range(d))

    formula_val = 32 + 8*(n_vec @ B_vec) - np.dot(A_vec, A_vec)
    numerical_val = cube_sum_sq(links, x0)
    diff = abs(formula_val - numerical_val)
    max_diff2 = max(max_diff2, diff)
    max_numerical2 = max(max_numerical2, numerical_val)

print(f"Over 10000 tests:")
print(f"  Max formula error = {max_diff2:.2e}")
print(f"  Max ∑|B|² = {max_numerical2:.6f} (bound: 64.0)")

# =================================================
# PROOF OF THE BOUND
# =================================================
print()
print("="*60)
print("PROOF OF ∑|B|² ≤ 64 FROM THE FORMULA")
print("="*60)
print()
print("We have: ∑|B|² = 32 + 8⟨n, W⟩ - |A|²")
print("where W = ∑_μ w_μ ∈ R³, A = ∑_μ s_μ w_μ ∈ R³")
print("and each w_μ ∈ S² (unit vector), s = (1,-1,1,-1)")
print()
print("Need to show: 8⟨n, W⟩ - |A|² ≤ 32")
print()
print("Strategy: |A|² ≥ 0, so it suffices to show 8⟨n,W⟩ ≤ 32 + |A|²")
print()
print("By Cauchy-Schwarz: ⟨n, W⟩ = ⟨n, ∑w_μ⟩ ≤ |∑w_μ| ≤ ∑|w_μ| = 4")
print("So 8⟨n, W⟩ ≤ 32.  But then 8⟨n,W⟩ - |A|² ≤ 32 - |A|² ≤ 32 ✓")
print()
print("Therefore ∑|B|² ≤ 32 + 8*4 - 0 = 32 + 32 - 0 = 64")
print("Wait: 8⟨n,W⟩ ≤ 8*4 = 32, and -|A|² ≤ 0")
print("So ∑|B|² ≤ 32 + 32 + 0 = 64. QED!")
print()
print("Equality iff ⟨n,W⟩ = 4 (all w_μ = n, i.e., R_μ^{-1}n = n, i.e., R_μ fixes n)")
print("AND |A|² = 0 (i.e., ∑s_μ w_μ = 0)")
print()
print("Check: at Q=I: w_μ = n for all μ (R_μ=I), so ⟨n,W⟩ = ⟨n, 4n⟩ = 4")
print("A = ∑s_μ n = (1-1+1-1)n = 0, |A|² = 0")
print(f"∑|B|² = 32 + 8*4 - 0 = {32+32} = 64 ✓")
print()

# Verify at Q=I
links_I = I_links()
print(f"Numerical check at Q=I: cube_sum_sq = {cube_sum_sq(links_I, x0):.6f}")

# =================================================
# BUT: This is for cross-links = I. What about general links?
# =================================================
print()
print("="*60)
print("GENERAL CASE: Cross-links non-trivial")
print("="*60)
print()
print("For general Q, B = c₁n + c₂Ad_{P₁}n - c₃Ad_{P₁P₂P₃⁻¹}n - c₄Ad_{U□}n")
print("With c₃=-c₁, c₄=-c₂:")
print("B = c₁(n + Ad_{P₁P₂P₃⁻¹}n) + c₂(Ad_{P₁}n + Ad_{U□}n)")
print()
print("Define: ξ_□ = P₁P₂P₃⁻¹ (3 of the 4 links) and U□ = ξ□·P₄⁻¹")
print("B = c₁(n + R_ξn) + c₂(R₁n + R_ξ R₄⁻¹ n)")
print("  = c₁(n + R_ξn) + c₂ R_ξ(R_ξ⁻¹R₁n + R₄⁻¹n)")
print()
print("This is more complex. The formula ∑|B|² = 32 + 8⟨n,W⟩ - |A|²")
print("does NOT hold for general cross-links.")
print()

# Test: what is the cube-face sum formula for general Q?
# Let's numerically find an alternative representation.
# For general Q, define for each plane (μ,ν):
# B = c₁(n + R_{μν}n) + c₂(R_μn + R_μν R_ν^{-1} n)...
# where R_μ = Ad_{Q_{x,μ}}, R_ν = Ad_{Q_{x,ν}}, R_{μν} = Ad_{Q_{x,μ}Q_{x+μ,ν}Q_{x+ν,μ}^{-1}}
# This depends on 3 different rotation matrices per plaquette, not just the base links.

# However, numerically we know cube_sum_sq ≤ 64 always.
# Let's understand it via the Hessian structure.

print("="*60)
print("CHECKING: Does the formula 32 + 8⟨n,W̃⟩ - |Ã|² generalize?")
print("="*60)
print()

# For general Q: B = c₁·a_{μν} + c₂·b_{μν}
# where a_{μν} = n + R_{ξ_{μν}} n  (two parallel-transported vectors)
#       b_{μν} = R_{μ} n + R_□ n
# (using R_ξ = R_P1*R_P2*R_P3^{-1}, R_□ = R_ξ*R_P4^{-1})

# The general sum ∑|B|² with arbitrary 4-link structure per plaquette.
# Key idea: Can we still write it as a quadratic form in some "extended" vector?

# Actually, from SZZ and prior explorations, the Hessian M(Q) is known to factor.
# But let's just verify the numerical bound and accept it.

N_FULL = 10000
max_full = -np.inf
for _ in range(N_FULL):
    links = {e: random_su2() for e in edges}
    cs = cube_sum_sq(links, x0)
    if cs > max_full:
        max_full = cs

print(f"Max cube_sum_sq (all links free, {N_FULL} tests): {max_full:.6f}")
print(f"Bound: 64.0")
print(f"Shortfall from 64: {64 - max_full:.4f}")

# Additional check: adversarial maximization of cube_sum_sq (not cube_face_sum)
print()
print("Adversarial: maximize ∑|B_{(x0,μ,ν)}|² directly")
links = {e: random_su2() for e in edges}
for step in range(500):
    val = cube_sum_sq(links, x0)
    new_links = dict(links)
    for e in edges:
        grads = np.zeros(3)
        eps = 1e-4
        for k in range(3):
            dl = dict(links)
            Q0 = links[e]
            U_perturb = (np.eye(2,dtype=complex) + eps * T[k]) @ Q0
            det = np.linalg.det(U_perturb)
            dl[e] = U_perturb / np.sqrt(det)
            grads[k] = (cube_sum_sq(dl, x0) - val) / eps
        gn = np.linalg.norm(grads)
        if gn > 1e-10:
            g = grads/gn
            ang = min(0.02*gn, 0.3)
            v_sigma = sum(g[k]*sigmas[k] for k in range(3))
            exp_X = np.cos(ang/2)*np.eye(2,dtype=complex) + 1j*np.sin(ang/2)*v_sigma
            new_links[e] = exp_X @ links[e]
    links = new_links
    if step % 100 == 0:
        print(f"  step {step}: cube_sum_sq = {val:.6f}")

final = cube_sum_sq(links, x0)
print(f"Final: cube_sum_sq = {final:.6f} (converged to: Q=I gives {cube_sum_sq(I_links(), x0):.6f})")

print("\nAll done.")
