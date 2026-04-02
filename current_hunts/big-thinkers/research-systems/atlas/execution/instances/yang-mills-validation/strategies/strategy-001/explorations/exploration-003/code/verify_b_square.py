"""
verify_b_square.py
==================
Numerical verification of the B_□ (B-square) formula for the Wilson action Hessian.

Convention (SZZ arXiv:2204.12737):
  - Action: S(Q) = -(β/N) Σ_□ Re Tr(U_□), N=2 for SU(2)
  - Inner product: <A,B> = -2 Re Tr(AB), |A|² = -2 Tr(A²)
  - Generators: τ_a = i σ_a / 2, so |τ_a|² = 1
  - Plaquette: U_{x,μν} = Q_{e1} Q_{e2} Q_{e3}⁻¹ Q_{e4}⁻¹

The corrected B_□ formula:
  B_□(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}⁻¹}(v_{e3}) - Ad_{U_□}(v_{e4})

NOTE: For backward edges, the adjoint transport INCLUDES the edge's own Q⁻¹.
"""

import numpy as np
from scipy.linalg import expm, logm
import itertools

# ============================================================
# SU(2) setup
# ============================================================

# Pauli matrices
sigma1 = np.array([[0,1],[1,0]], dtype=complex)
sigma2 = np.array([[0,-1j],[1j,0]], dtype=complex)
sigma3 = np.array([[1,0],[0,-1]], dtype=complex)

# SZZ generators: τ_a = i σ_a / 2
tau = [1j*sigma1/2, 1j*sigma2/2, 1j*sigma3/2]

# Inner product: <A,B> = -2 Re Tr(AB)
# |τ_a|² = -2 Tr(τ_a²) = -2 Tr(-σ_a²/4) = -2 Tr(-I/4) = 1 ✓
def inner(A, B):
    return -2.0 * np.real(np.trace(A @ B))

def norm_sq(A):
    return inner(A, A)

def random_su2():
    """Generate a random SU(2) matrix via Haar measure."""
    # Parametrize as a + i(b σ1 + c σ2 + d σ3), a²+b²+c²+d²=1
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    a, b, c, d = v
    return np.array([[a + 1j*d, b + 1j*c],
                     [-b + 1j*c, a - 1j*d]], dtype=complex)

def random_su2_lie():
    """Generate a random element of su(2) = span{τ_a}."""
    coeffs = np.random.randn(3)
    return sum(c * t for c, t in zip(coeffs, tau))

def adjoint_action(U, A):
    """Ad_U(A) = U A U⁻¹."""
    return U @ A @ np.linalg.inv(U)

# ============================================================
# B_□ formula (corrected version)
# ============================================================

def compute_plaquette(Q1, Q2, Q3, Q4):
    """U_□ = Q1 Q2 Q3⁻¹ Q4⁻¹"""
    return Q1 @ Q2 @ np.linalg.inv(Q3) @ np.linalg.inv(Q4)

def B_square_corrected(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    Corrected B_□ formula (from GOAL.md):
    B = v1 + Ad_{Q1}(v2) - Ad_{Q1 Q2 Q3⁻¹}(v3) - Ad_{U_□}(v4)

    For backward edges (e3, e4), transport includes the edge's own Q⁻¹.
    """
    U = compute_plaquette(Q1, Q2, Q3, Q4)
    transport_e1 = np.eye(2, dtype=complex)  # identity
    transport_e2 = Q1
    transport_e3 = Q1 @ Q2 @ np.linalg.inv(Q3)  # includes Q3⁻¹
    transport_e4 = U                              # = Q1 Q2 Q3⁻¹ Q4⁻¹, includes Q4⁻¹

    B = (adjoint_action(transport_e1, v1)
         + adjoint_action(transport_e2, v2)
         - adjoint_action(transport_e3, v3)
         - adjoint_action(transport_e4, v4))
    return B

def B_square_wrong(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    WRONG B_□ formula (original error — does NOT include edge's own Q⁻¹ for backward edges):
    B = v1 + Ad_{Q1}(v2) - Ad_{Q1 Q2}(v3) - Ad_{Q1 Q2 Q3⁻¹}(v4)
    """
    U = compute_plaquette(Q1, Q2, Q3, Q4)
    transport_e3_wrong = Q1 @ Q2              # missing Q3⁻¹
    transport_e4_wrong = Q1 @ Q2 @ np.linalg.inv(Q3)  # missing Q4⁻¹

    B = (v1
         + adjoint_action(Q1, v2)
         - adjoint_action(transport_e3_wrong, v3)
         - adjoint_action(transport_e4_wrong, v4))
    return B

# ============================================================
# Stage 1: Numerical verification via finite differences
# ============================================================

def hessian_finite_diff(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, N=2, h=1e-5):
    """
    Numerical d²/dt² [-(β/N) Re Tr(U_□(t))] |_{t=0}
    where Q_e(t) = exp(t·v_e) Q_e.
    Uses central difference: [f(h) - 2f(0) + f(-h)] / h²
    """
    def action_at_t(t):
        Q1t = expm(t * v1) @ Q1
        Q2t = expm(t * v2) @ Q2
        Q3t = expm(t * v3) @ Q3
        Q4t = expm(t * v4) @ Q4
        U = compute_plaquette(Q1t, Q2t, Q3t, Q4t)
        return -(beta/N) * np.real(np.trace(U))

    f0 = action_at_t(0)
    fp = action_at_t(h)
    fm = action_at_t(-h)
    return (fp - 2*f0 + fm) / h**2

def hessian_analytic(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, N=2):
    """
    Analytic Hessian via B_□ formula:
    d²/dt² [-(β/N) Re Tr(U_□(t))] |_{t=0} = (β/(2N)) |B_□(Q,v)|²
    """
    B = B_square_corrected(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
    return (beta / (2*N)) * norm_sq(B)

print("=" * 60)
print("STAGE 1: Numerical Verification of B_□ Formula")
print("=" * 60)

np.random.seed(42)
beta = 1.0
N = 2
h = 1e-5

errors_corrected = []
errors_wrong = []

n_configs = 5
n_plaquettes = 5
n_tangents = 5  # multiple tangent vectors per (Q, □)

trial = 0
max_error_corrected = 0.0
max_error_wrong = 0.0

print(f"\nTesting {n_configs} × {n_plaquettes} × {n_tangents} = "
      f"{n_configs*n_plaquettes*n_tangents} (Q, □, v) triples\n")

for ic in range(n_configs):
    for ip in range(n_plaquettes):
        Q1 = random_su2()
        Q2 = random_su2()
        Q3 = random_su2()
        Q4 = random_su2()

        for iv in range(n_tangents):
            v1 = random_su2_lie()
            v2 = random_su2_lie()
            v3 = random_su2_lie()
            v4 = random_su2_lie()

            hess_num = hessian_finite_diff(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=beta, N=N, h=h)
            hess_analytic = hessian_analytic(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=beta, N=N)

            err_corrected = abs(hess_num - hess_analytic)
            errors_corrected.append(err_corrected)

            # Also test the wrong formula
            B_w = B_square_wrong(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
            hess_wrong = (beta / (2*N)) * norm_sq(B_w)
            err_wrong = abs(hess_num - hess_wrong)
            errors_wrong.append(err_wrong)

            trial += 1

max_error_corrected = max(errors_corrected)
max_error_wrong = max(errors_wrong)
mean_error_corrected = np.mean(errors_corrected)
mean_error_wrong = np.mean(errors_wrong)

print(f"CORRECTED formula:")
print(f"  Max  |hess_num - hess_analytic| = {max_error_corrected:.2e}")
print(f"  Mean |hess_num - hess_analytic| = {mean_error_corrected:.2e}")
print(f"  PASS: {max_error_corrected < 1e-8}")

print(f"\nWRONG formula (original error):")
print(f"  Max  |hess_num - hess_wrong|    = {max_error_wrong:.2e}")
print(f"  Mean |hess_num - hess_wrong|    = {mean_error_wrong:.2e}")
print(f"  Would fail: {max_error_wrong > 1e-6}")

# Special test: Q=I
print("\n--- Special test: Q = I (identity) ---")
I2 = np.eye(2, dtype=complex)
v1 = tau[0] + 0.3*tau[1]
v2 = 0.5*tau[1] - 0.2*tau[2]
v3 = 0.7*tau[0] + 0.1*tau[2]
v4 = -0.3*tau[1] + 0.4*tau[2]

# At Q=I: B_□(I,v) = v1 + v2 - v3 - v4 (discrete curl)
B_identity = B_square_corrected(I2, I2, I2, I2, v1, v2, v3, v4)
B_expected = v1 + v2 - v3 - v4

err_identity = np.max(np.abs(B_identity - B_expected))
print(f"B_□(I,v) vs v1+v2-v3-v4: max element error = {err_identity:.2e}")
print(f"PASS: {err_identity < 1e-12}")

hess_num_I = hessian_finite_diff(I2, I2, I2, I2, v1, v2, v3, v4, beta=beta, N=N)
hess_ana_I = hessian_analytic(I2, I2, I2, I2, v1, v2, v3, v4, beta=beta, N=N)
print(f"At Q=I: finite diff = {hess_num_I:.8f}, analytic = {hess_ana_I:.8f}")
print(f"Error at Q=I: {abs(hess_num_I - hess_ana_I):.2e}")

# ============================================================
# Stage 2: Structural properties of B_□
# ============================================================

print("\n" + "=" * 60)
print("STAGE 2: Structural Properties of B_□")
print("=" * 60)

def compute_B_matrix(Q1, Q2, Q3, Q4, beta=1.0, N=2):
    """
    Compute the 3×12 matrix B_□ as a linear map from (v1,v2,v3,v4) in su(2)^4
    to su(2) ≅ R^3.

    Columns: generators τ_a acting on each of the 4 edges.
    Row: component in the τ_b basis.

    B_□ is a 3×12 matrix (3 generators, 4 edges × 3 generators = 12 columns).
    """
    def to_vec(A):
        """Project A onto the {τ_a} basis using the inner product."""
        return np.array([inner(tau_a, A) for tau_a in tau])

    # B acts on (v1, v2, v3, v4) ∈ (su(2))^4 ≅ R^12
    # Each edge e contributes v_e in position (3*e_idx : 3*e_idx+3)
    B_mat = np.zeros((3, 12))

    for a in range(3):
        for e_idx, basis_vec in enumerate(tau):
            # Unit vector e_a in edge e_idx
            unit = [np.zeros((2,2), dtype=complex)] * 4
            unit = list(unit)
            unit[e_idx] = basis_vec

            B_val = B_square_corrected(Q1, Q2, Q3, Q4, *unit)
            col = e_idx * 3  # This is wrong; need to properly index
            # Actually: column = e_idx*3 + a corresponds to v_{e_idx, a}
            # Row b = output component in τ_b direction

    # Redo: columns are indexed by (edge, generator) pairs
    # B_mat[b, e*3+a] = <τ_b, B_□(e_{e,a})> where e_{e,a} has v_{e,a}=τ_a, rest 0
    B_mat = np.zeros((3, 12))
    for e_idx in range(4):
        for a in range(3):
            unit = [np.zeros((2,2), dtype=complex)] * 4
            unit = list(unit)
            unit[e_idx] = tau[a]
            B_val = B_square_corrected(Q1, Q2, Q3, Q4, *unit)
            col = e_idx * 3 + a
            for b in range(3):
                B_mat[b, col] = inner(tau[b], B_val)

    return B_mat

print("\nTest: B_□ B_□^T = 4I_{3} for random (Q, □) pairs")
print("Expected: B_mat @ B_mat.T = 4 * I_3")

np.random.seed(123)
for trial_idx in range(5):
    Q1 = random_su2()
    Q2 = random_su2()
    Q3 = random_su2()
    Q4 = random_su2()

    B_mat = compute_B_matrix(Q1, Q2, Q3, Q4)
    BBT = B_mat @ B_mat.T
    expected = 4.0 * np.eye(3)
    err = np.max(np.abs(BBT - expected))
    print(f"  Trial {trial_idx+1}: max |B·B^T - 4I| = {err:.2e}  PASS={err < 1e-8}")

# Per-plaquette M_□ = B^T B should have eigenvalues {4,4,4,0,...,0}
print("\nTest: Per-plaquette M_□ = B_□^T B_□ eigenvalues = {4,4,4,0,...,0}")

np.random.seed(456)
for trial_idx in range(5):
    Q1 = random_su2()
    Q2 = random_su2()
    Q3 = random_su2()
    Q4 = random_su2()

    B_mat = compute_B_matrix(Q1, Q2, Q3, Q4)
    M_sq = B_mat.T @ B_mat  # 12×12
    eigs = np.sort(np.real(np.linalg.eigvalsh(M_sq)))[::-1]

    nonzero_eigs = eigs[eigs > 1e-6]
    zero_count = np.sum(eigs < 1e-6)
    print(f"  Trial {trial_idx+1}: nonzero eigs = {nonzero_eigs[:5].round(4)}, "
          f"zeros = {zero_count}  PASS={np.allclose(nonzero_eigs[:3], [4,4,4], atol=1e-6)}")

print("\nTest: Tr(M(Q)) = 4 × n_plaquettes × (N²-1) independent of Q")
# For a single plaquette: Tr(B^T B) = Tr(B B^T) = Tr(4I_3) = 12 = 4 × 1 × 3
np.random.seed(789)
for trial_idx in range(6):
    if trial_idx == 0:
        Q1, Q2, Q3, Q4 = np.eye(2,dtype=complex), np.eye(2,dtype=complex), np.eye(2,dtype=complex), np.eye(2,dtype=complex)
        label = "Q=I"
    else:
        Q1 = random_su2(); Q2 = random_su2(); Q3 = random_su2(); Q4 = random_su2()
        label = f"random {trial_idx}"

    B_mat = compute_B_matrix(Q1, Q2, Q3, Q4)
    tr_M = np.trace(B_mat.T @ B_mat)
    expected_tr = 4 * 1 * 3  # 4 × n_plaq × (N²-1)
    print(f"  {label}: Tr(M) = {tr_M:.4f}, expected = {expected_tr}  "
          f"PASS={abs(tr_M - expected_tr) < 1e-6}")

print("\nStage 2 complete.")
