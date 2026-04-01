"""
Derive and verify the Hessian of the Wilson action for SU(2) lattice gauge theory.

Wilson action for one plaquette:
  s_□ = -(β/N) Re Tr(U_□)
  U_□ = Q1 Q2 Q3^{-1} Q4^{-1}

Perturbation: Q_i -> Q_i exp(ε v_i), v_i ∈ su(2)

We compute d²/dε² s_□(Q exp(εv))|_{ε=0} both analytically and by finite differences.
"""

import numpy as np
np.set_printoptions(precision=10, linewidth=120)

# Pauli matrices
sigma = np.array([
    [[0, 1], [1, 0]],       # sigma_1
    [[0, -1j], [1j, 0]],    # sigma_2
    [[1, 0], [0, -1]],      # sigma_3
], dtype=complex)

I2 = np.eye(2, dtype=complex)

def expm_su2(v):
    """Matrix exponential for v ∈ su(2) (2x2 anti-hermitian traceless).
    v = i(a1 σ1 + a2 σ2 + a3 σ3) => exp(v) = cos(θ)I + sin(θ)/θ · v
    where θ = |a| = sqrt(a1² + a2² + a3²), and |v| as matrix has eigenvalues ±iθ.
    """
    # v should be anti-hermitian traceless
    # eigenvalues of v are ±iθ where θ = sqrt(-det(v)) for traceless 2x2
    # det(v) = -θ² for anti-hermitian traceless
    det_v = v[0,0]*v[1,1] - v[0,1]*v[1,0]
    theta_sq = -det_v  # should be real and positive
    theta = np.sqrt(np.abs(theta_sq.real))
    if theta < 1e-15:
        return I2 + v + 0.5 * v @ v
    return np.cos(theta) * I2 + (np.sin(theta) / theta) * v

def random_su2():
    """Random SU(2) matrix via quaternion parametrization."""
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    return v[0]*I2 + 1j*(v[1]*sigma[0] + v[2]*sigma[1] + v[3]*sigma[2])

def su2_basis():
    """Basis for su(2): i*sigma_a."""
    return [1j * sigma[a] for a in range(3)]

def adjoint_rep(Q):
    """3x3 SO(3) adjoint representation: Ad_Q(i σ_a) = Q (i σ_a) Q^† = Σ_b R_{ba} (i σ_b)"""
    basis = su2_basis()
    Qdag = Q.conj().T
    R = np.zeros((3, 3))
    for a in range(3):
        rotated = Q @ basis[a] @ Qdag
        for b in range(3):
            R[b, a] = (np.trace(basis[b].conj().T @ rotated) / 2.0).real
    return R

# ============================================================
# ANALYTICAL HESSIAN FOR SINGLE PLAQUETTE
# ============================================================
#
# U_□(ε) = Q1 e^{εv1} Q2 e^{εv2} e^{-εv3} Q3^{-1} e^{-εv4} Q4^{-1}
#
# Define signed perturbations: w1=v1, w2=v2, w3=-v3, w4=-v4
#
# The product has 4 insertion points:
#   pos1: between Q1 and Q2 (where e^{εw1} goes)
#   pos2: between Q2 and Q3^{-1} (where e^{εw2} e^{εw3} goes)
#   pos3: between Q3^{-1} and Q4^{-1} (where e^{εw4} goes)
#
# Note pos2 gets both w2 and w3!
#
# Expanding e^{εw} = I + εw + ε²w²/2:
#
# O(ε²) terms in Tr(U_□(ε)):
#
# Self terms (coefficient 1 after d²/dε²):
#   Tr(Q1 w1² Q2 Q3⁻¹ Q4⁻¹)
#   Tr(Q1Q2 w2² Q3⁻¹ Q4⁻¹)
#   Tr(Q1Q2 w3² Q3⁻¹ Q4⁻¹)
#   Tr(Q1Q2Q3⁻¹ w4² Q4⁻¹)
#
# Cross terms (coefficient 2 after d²/dε²):
#   Tr(Q1 w1 Q2 w2 Q3⁻¹ Q4⁻¹)       -- (1,2)
#   Tr(Q1 w1 Q2 w3 Q3⁻¹ Q4⁻¹)       -- (1,3)
#   Tr(Q1 w1 Q2Q3⁻¹ w4 Q4⁻¹)        -- (1,4)
#   Tr(Q1Q2 w2 w3 Q3⁻¹ Q4⁻¹)        -- (2,3) same insertion point
#   Tr(Q1Q2 w2 Q3⁻¹ w4 Q4⁻¹)        -- (2,4)
#   Tr(Q1Q2 w3 Q3⁻¹ w4 Q4⁻¹)        -- (3,4)
#
# d²/dε² Re Tr(U_□(ε))|_0 = Re[self_sum + 2*cross_sum]
# HessS_□ = -(β/N) * d²/dε² Re Tr(U_□(ε))|_0

def plaquette_hessian_analytical(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, N=2):
    """Analytical Hessian of single plaquette action."""
    w1, w2, w3, w4 = v1, v2, -v3, -v4

    Q3inv = Q3.conj().T  # SU(2): inverse = conjugate transpose
    Q4inv = Q4.conj().T

    # Left partial products
    L1 = Q1.copy()
    L12 = Q1 @ Q2
    L123 = L12 @ Q3inv

    # Right partial products
    R1 = Q2 @ Q3inv @ Q4inv
    R2 = Q3inv @ Q4inv
    R3 = Q4inv

    # Self terms
    self1 = np.trace(L1 @ w1 @ w1 @ R1)
    self2 = np.trace(L12 @ w2 @ w2 @ R2)
    self3 = np.trace(L12 @ w3 @ w3 @ R2)
    self4 = np.trace(L123 @ w4 @ w4 @ R3)
    self_sum = self1 + self2 + self3 + self4

    # Cross terms
    c12 = np.trace(L1 @ w1 @ Q2 @ w2 @ R2)
    c13 = np.trace(L1 @ w1 @ Q2 @ w3 @ R2)
    c14 = np.trace(L1 @ w1 @ Q2 @ Q3inv @ w4 @ R3)
    c23 = np.trace(L12 @ w2 @ w3 @ R2)
    c24 = np.trace(L12 @ w2 @ Q3inv @ w4 @ R3)
    c34 = np.trace(L12 @ w3 @ Q3inv @ w4 @ R3)
    cross_sum = c12 + c13 + c14 + c23 + c24 + c34

    d2_trace = (self_sum + 2 * cross_sum).real
    return -(beta / N) * d2_trace

def plaquette_hessian_fd(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, N=2, eps=1e-5):
    """Finite-difference Hessian of single plaquette action."""
    def action(e):
        U = (Q1 @ expm_su2(e*v1)) @ (Q2 @ expm_su2(e*v2)) @ \
            (expm_su2(-e*v3) @ Q3.conj().T) @ (expm_su2(-e*v4) @ Q4.conj().T)
        return -(beta/N) * np.trace(U).real
    fp = action(eps)
    fm = action(-eps)
    f0 = action(0)
    return (fp + fm - 2*f0) / eps**2

# ============================================================
# TEST 1: Q = I
# ============================================================
print("="*70)
print("TEST 1: All links = I")
print("="*70)

basis = su2_basis()
v_test = [0.3*basis[0] + 0.5*basis[1] - 0.2*basis[2] for _ in range(4)]

h_fd = plaquette_hessian_fd(I2, I2, I2, I2, v_test[0], v_test[1], v_test[2], v_test[3])
h_an = plaquette_hessian_analytical(I2, I2, I2, I2, v_test[0], v_test[1], v_test[2], v_test[3])

print(f"Finite diff:  {h_fd:.10f}")
print(f"Analytical:   {h_an:.10f}")
print(f"Difference:   {abs(h_fd - h_an):.2e}")

# ============================================================
# TEST 2: Q = i*sigma_3
# ============================================================
print("\n" + "="*70)
print("TEST 2: All links = i*sigma_3")
print("="*70)

Q_is3 = 1j * sigma[2]  # i*sigma_3

h_fd2 = plaquette_hessian_fd(Q_is3, Q_is3, Q_is3, Q_is3, v_test[0], v_test[1], v_test[2], v_test[3])
h_an2 = plaquette_hessian_analytical(Q_is3, Q_is3, Q_is3, Q_is3, v_test[0], v_test[1], v_test[2], v_test[3])

print(f"Finite diff:  {h_fd2:.10f}")
print(f"Analytical:   {h_an2:.10f}")
print(f"Difference:   {abs(h_fd2 - h_an2):.2e}")

# ============================================================
# TEST 3: 10 random configs
# ============================================================
print("\n" + "="*70)
print("TEST 3: 10 random SU(2) configurations")
print("="*70)

np.random.seed(42)
max_err = 0
for trial in range(10):
    Q1, Q2, Q3, Q4 = [random_su2() for _ in range(4)]
    coeffs = np.random.randn(4, 3)
    vs = [sum(c * b for c, b in zip(coeffs[i], basis)) for i in range(4)]

    h_fd_r = plaquette_hessian_fd(Q1, Q2, Q3, Q4, vs[0], vs[1], vs[2], vs[3])
    h_an_r = plaquette_hessian_analytical(Q1, Q2, Q3, Q4, vs[0], vs[1], vs[2], vs[3])

    err = abs(h_fd_r - h_an_r)
    denom = max(abs(h_fd_r), abs(h_an_r), 1e-15)
    rel_err = err / denom
    max_err = max(max_err, rel_err)
    print(f"Trial {trial:2d}: FD={h_fd_r:+.10f}  AN={h_an_r:+.10f}  rel_err={rel_err:.2e}")

print(f"\nMax relative error across 10 trials: {max_err:.2e}")
print("PASS" if max_err < 1e-4 else "FAIL")
