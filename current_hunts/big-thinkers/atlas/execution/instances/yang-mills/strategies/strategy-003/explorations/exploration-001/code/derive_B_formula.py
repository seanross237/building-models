"""
Derive and verify the correct B_□ formula by computing dU_□/dt · U_□⁻¹ directly.

There are two candidate formulas for B_□:

GOAL.MD formula:
  B_□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂}(v₃) - Ad_{Q₁Q₂Q₃⁻¹}(v₄)

DERIVED formula (from dU/dt · U⁻¹):
  B_□ = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U₀}(v₄)
  where U₀ = Q₁Q₂Q₃⁻¹Q₄⁻¹

We test which is correct by comparing with finite-difference computation of dU/dt.
"""

import numpy as np

def random_su2():
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([
        [a + 1j*b, c + 1j*d],
        [-c + 1j*d, a - 1j*b]
    ])

def su2_exp(A_vec):
    theta = np.linalg.norm(A_vec)
    if theta < 1e-15:
        return np.eye(2, dtype=complex)
    n = A_vec / theta
    ct = np.cos(theta / 2)
    st = np.sin(theta / 2)
    return np.array([
        [ct + 1j*st*n[2], st*(1j*n[0] + n[1])],
        [st*(1j*n[0] - n[1]), ct - 1j*st*n[2]]
    ])

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sigma1 / 2, 1j * sigma2 / 2, 1j * sigma3 / 2]


np.random.seed(42)
basis = su2_basis()

# Generate random link variables
Q1 = random_su2()
Q2 = random_su2()
Q3 = random_su2()
Q4 = random_su2()

U0 = Q1 @ Q2 @ np.conj(Q3).T @ np.conj(Q4).T  # U_□ = Q₁Q₂Q₃⁻¹Q₄⁻¹

# Generate random tangent vectors
v1_coeffs = np.random.randn(3)
v2_coeffs = np.random.randn(3)
v3_coeffs = np.random.randn(3)
v4_coeffs = np.random.randn(3)

v1 = sum(c * T for c, T in zip(v1_coeffs, basis))
v2 = sum(c * T for c, T in zip(v2_coeffs, basis))
v3 = sum(c * T for c, T in zip(v3_coeffs, basis))
v4 = sum(c * T for c, T in zip(v4_coeffs, basis))

# --- Finite difference: compute dU/dt for varying each edge ---

h = 1e-7

def U_plaq(dQ1, dQ2, dQ3, dQ4):
    """Compute plaquette with perturbed links."""
    return dQ1 @ dQ2 @ np.conj(dQ3).T @ np.conj(dQ4).T

# Vary edge 1: Q₁ → exp(tv₁)Q₁
def U_vary_e1(t):
    return su2_exp(t * v1_coeffs) @ Q1 @ Q2 @ np.conj(Q3).T @ np.conj(Q4).T

dU_e1_fd = (U_vary_e1(h) - U_vary_e1(-h)) / (2*h)

# Vary edge 2: Q₂ → exp(tv₂)Q₂
def U_vary_e2(t):
    return Q1 @ su2_exp(t * v2_coeffs) @ Q2 @ np.conj(Q3).T @ np.conj(Q4).T

dU_e2_fd = (U_vary_e2(h) - U_vary_e2(-h)) / (2*h)

# Vary edge 3: Q₃ → exp(tv₃)Q₃, so Q₃⁻¹ → Q₃⁻¹exp(-tv₃)
def U_vary_e3(t):
    Q3_new = su2_exp(t * v3_coeffs) @ Q3
    return Q1 @ Q2 @ np.conj(Q3_new).T @ np.conj(Q4).T

dU_e3_fd = (U_vary_e3(h) - U_vary_e3(-h)) / (2*h)

# Vary edge 4: Q₄ → exp(tv₄)Q₄
def U_vary_e4(t):
    Q4_new = su2_exp(t * v4_coeffs) @ Q4
    return Q1 @ Q2 @ np.conj(Q3).T @ np.conj(Q4_new).T

dU_e4_fd = (U_vary_e4(h) - U_vary_e4(-h)) / (2*h)

# Total first variation
dU_total_fd = dU_e1_fd + dU_e2_fd + dU_e3_fd + dU_e4_fd

# Extract B_□ = dU · U⁻¹
U0_inv = np.conj(U0).T  # U₀⁻¹ for SU(2)
B_fd = dU_total_fd @ U0_inv

print("=== Finite Difference B_□ ===")
print(f"B_fd (should be anti-Hermitian):")
print(f"  B_fd = \n{B_fd}")
print(f"  B_fd + B_fd† = \n{B_fd + np.conj(B_fd).T}")
print(f"  |B_fd + B_fd†| = {np.max(np.abs(B_fd + np.conj(B_fd).T)):.2e}")

# --- GOAL.MD formula ---
# B' = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂}(v₃) - Ad_{Q₁Q₂Q₃⁻¹}(v₄)
Q12 = Q1 @ Q2
Q123inv = Q12 @ np.conj(Q3).T

A1_goalmd = v1
A2_goalmd = adjoint_action(Q1, v2)
A3_goalmd = -adjoint_action(Q12, v3)
A4_goalmd = -adjoint_action(Q123inv, v4)
B_goalmd = A1_goalmd + A2_goalmd + A3_goalmd + A4_goalmd

print(f"\n=== GOAL.MD Formula ===")
print(f"B_goalmd = \n{B_goalmd}")
print(f"|B_goalmd - B_fd| = {np.max(np.abs(B_goalmd - B_fd)):.2e}")

# --- DERIVED formula ---
# B = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U₀}(v₄)
A1_derived = v1
A2_derived = adjoint_action(Q1, v2)
A3_derived = -adjoint_action(Q123inv, v3)
A4_derived = -adjoint_action(U0, v4)
B_derived = A1_derived + A2_derived + A3_derived + A4_derived

print(f"\n=== DERIVED Formula (dU·U⁻¹) ===")
print(f"B_derived = \n{B_derived}")
print(f"|B_derived - B_fd| = {np.max(np.abs(B_derived - B_fd)):.2e}")

# Also check per-edge contributions
print(f"\n=== Per-edge verification ===")
for name, dU_fd, Atilde in [
    ("e1", dU_e1_fd, v1),
    ("e2", dU_e2_fd, adjoint_action(Q1, v2)),
    ("e3", dU_e3_fd, -adjoint_action(Q123inv, v3)),
    ("e4", dU_e4_fd, -adjoint_action(U0, v4)),
]:
    B_e = dU_fd @ U0_inv
    err = np.max(np.abs(B_e - Atilde))
    print(f"  {name}: |Ã_derived - (dU_e·U⁻¹)| = {err:.2e}")

print(f"\n=== Per-edge (GOAL.MD version) ===")
for name, dU_fd, Atilde in [
    ("e1", dU_e1_fd, v1),
    ("e2", dU_e2_fd, adjoint_action(Q1, v2)),
    ("e3", dU_e3_fd, -adjoint_action(Q12, v3)),
    ("e4", dU_e4_fd, -adjoint_action(Q123inv, v4)),
]:
    B_e = dU_fd @ U0_inv
    err = np.max(np.abs(B_e - Atilde))
    print(f"  {name}: |Ã_goalmd - (dU_e·U⁻¹)| = {err:.2e}")

# --- Compute |B|² for both formulas ---
print(f"\n=== |B|² comparison ===")
B_sq_fd = -2 * np.trace(B_fd @ B_fd).real
B_sq_goalmd = -2 * np.trace(B_goalmd @ B_goalmd).real
B_sq_derived = -2 * np.trace(B_derived @ B_derived).real
print(f"|B_fd|² = {B_sq_fd:.10f}")
print(f"|B_goalmd|² = {B_sq_goalmd:.10f}")
print(f"|B_derived|² = {B_sq_derived:.10f}")
