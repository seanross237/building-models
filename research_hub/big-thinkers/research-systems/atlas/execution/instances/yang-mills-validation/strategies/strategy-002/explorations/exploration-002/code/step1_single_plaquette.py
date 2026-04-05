"""
Step 1: Compute d²/dt² Re Tr(U□(t))|_{t=0} for a single plaquette.

Analytical derivation:
    U□ = Q₁ Q₂ Q₃⁻¹ Q₄⁻¹
    Under left perturbation Qₖ → exp(t·vₖ) Qₖ:

    U□(t) = exp(tv₁) Q₁ · exp(tv₂) Q₂ · Q₃⁻¹ exp(-tv₃) · Q₄⁻¹ exp(-tv₄)

    Push all exponentials to the left by conjugation:
    U□(t) = exp(tw₁) exp(tw₂) exp(tw₃) exp(tw₄) · U□

    where:
        w₁ = v₁
        w₂ = Ad_{Q₁}(v₂)       = Q₁ v₂ Q₁⁻¹
        w₃ = -Ad_{Q₁Q₂Q₃⁻¹}(v₃) = -(Q₁Q₂Q₃⁻¹) v₃ (Q₁Q₂Q₃⁻¹)⁻¹
        w₄ = -Ad_{U□}(v₄)       = -U□ v₄ U□⁻¹

    Expand product of exponentials to O(t²):

    ∏ exp(twₖ) = I + t·w + t²·[w²/2 + (1/2)Σ_{i<j}[wᵢ,wⱼ]] + O(t³)

    where w = Σwₖ.

    Therefore:
    d²/dt² Re Tr(U□(t))|_{t=0} = Re Tr(w² U□) + Σ_{i<j} Re Tr([wᵢ,wⱼ] U□)

    The CROSS TERM is: Σ_{i<j} Re Tr([wᵢ,wⱼ] U□)
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

# ============================================================
# SU(2) utilities
# ============================================================

# Generators: Tₐ = i σₐ / 2
sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),    # σ₁
    np.array([[0, -1j], [1j, 0]], dtype=complex),  # σ₂
    np.array([[1, 0], [0, -1]], dtype=complex),    # σ₃
]

T = [1j * s / 2 for s in sigma]  # T₁, T₂, T₃

def random_su2():
    """Random element of su(2): v = Σ αₐ Tₐ with random αₐ."""
    alpha = np.random.randn(3)
    return sum(a * t for a, t in zip(alpha, T))

def random_SU2():
    """Random element of SU(2) via exp of random su(2)."""
    return expm(random_su2())

def Ad(Q, v):
    """Adjoint action: Ad_Q(v) = Q v Q⁻¹ = Q v Q†."""
    return Q @ v @ Q.conj().T

def inner_product(X, Y):
    """⟨X,Y⟩ = -2 Tr(XY) for X,Y ∈ su(2)."""
    return -2.0 * np.trace(X @ Y).real

def norm_sq(X):
    """|X|² = -2 Tr(X²)."""
    return inner_product(X, X)

# ============================================================
# Single plaquette computation
# ============================================================

def plaquette(Q1, Q2, Q3, Q4):
    """U□ = Q₁ Q₂ Q₃⁻¹ Q₄⁻¹"""
    Q3inv = Q3.conj().T
    Q4inv = Q4.conj().T
    return Q1 @ Q2 @ Q3inv @ Q4inv

def re_tr(M):
    """Re Tr(M)"""
    return np.trace(M).real

def perturbed_plaquette(Q1, Q2, Q3, Q4, v1, v2, v3, v4, t):
    """U□(t) with left perturbation Qₖ → exp(t·vₖ) Qₖ"""
    eQ1 = expm(t * v1) @ Q1
    eQ2 = expm(t * v2) @ Q2
    eQ3 = expm(t * v3) @ Q3
    eQ4 = expm(t * v4) @ Q4
    return plaquette(eQ1, eQ2, eQ3, eQ4)

def finite_diff_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4, h=1e-4):
    """d²/dt² Re Tr(U□(t))|_{t=0} by central finite differences."""
    f_plus = re_tr(perturbed_plaquette(Q1, Q2, Q3, Q4, v1, v2, v3, v4, h))
    f_zero = re_tr(perturbed_plaquette(Q1, Q2, Q3, Q4, v1, v2, v3, v4, 0.0))
    f_minus = re_tr(perturbed_plaquette(Q1, Q2, Q3, Q4, v1, v2, v3, v4, -h))
    return (f_plus - 2 * f_zero + f_minus) / h**2

def compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    Compute the wₖ vectors:
        w₁ = v₁
        w₂ = Ad_{Q₁}(v₂)
        w₃ = -Ad_{Q₁Q₂Q₃⁻¹}(v₃)
        w₄ = -Ad_{U□}(v₄)
    """
    Q3inv = Q3.conj().T
    Q4inv = Q4.conj().T
    U = Q1 @ Q2 @ Q3inv @ Q4inv
    P3 = Q1 @ Q2 @ Q3inv  # = U @ Q4

    w1 = v1
    w2 = Ad(Q1, v2)
    w3 = -Ad(P3, v3)
    w4 = -Ad(U, v4)

    return w1, w2, w3, w4

def analytical_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    """
    d²/dt² Re Tr(U□(t))|_{t=0} = Re Tr(w² U□) + Σ_{i<j} Re Tr([wᵢ,wⱼ] U□)

    Returns: (total, w_squared_term, commutator_term, w_vectors)
    """
    U = plaquette(Q1, Q2, Q3, Q4)
    w1, w2, w3, w4 = compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
    w = w1 + w2 + w3 + w4

    # w² term
    w_sq_term = re_tr(w @ w @ U)

    # Commutator terms: Σ_{i<j} Re Tr([wᵢ,wⱼ] U)
    ws = [w1, w2, w3, w4]
    comm_term = 0.0
    for i in range(4):
        for j in range(i+1, 4):
            comm = ws[i] @ ws[j] - ws[j] @ ws[i]
            comm_term += re_tr(comm @ U)

    total = w_sq_term + comm_term
    return total, w_sq_term, comm_term, (w1, w2, w3, w4)

# ============================================================
# Run tests
# ============================================================

print("=" * 70)
print("STEP 1: Single Plaquette Second Derivative Verification")
print("=" * 70)

# Test 1: Flat configuration (Q = I)
print("\n--- Test 1: Flat configuration (all Qₖ = I) ---")
I2 = np.eye(2, dtype=complex)
for trial in range(3):
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]
    fd = finite_diff_second_derivative(I2, I2, I2, I2, v1, v2, v3, v4)
    ana, wsq, comm, _ = analytical_second_derivative(I2, I2, I2, I2, v1, v2, v3, v4)
    print(f"  Trial {trial+1}: FD = {fd:.10f}, Analytical = {ana:.10f}, "
          f"w²·U = {wsq:.10f}, [w,w]·U = {comm:.10f}, "
          f"Error = {abs(fd - ana):.2e}")

# Test 2: Random configurations
print("\n--- Test 2: Random configurations ---")
for config in range(5):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    U = plaquette(Q1, Q2, Q3, Q4)
    theta = np.arccos(np.clip(re_tr(U) / 2, -1, 1))

    print(f"\n  Config {config+1}: Re Tr(U□) = {re_tr(U):.6f}, θ = {theta:.4f}")

    for trial in range(3):
        v1, v2, v3, v4 = [random_su2() for _ in range(4)]

        fd = finite_diff_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
        ana, wsq, comm, _ = analytical_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4)

        print(f"    Trial {trial+1}: FD = {fd:+.8f}, Ana = {ana:+.8f}, "
              f"w²U = {wsq:+.8f}, [w,w]U = {comm:+.8f}, "
              f"|FD-Ana| = {abs(fd-ana):.2e}")

# Test 3: Large deformation — single link far from identity
print("\n--- Test 3: Large deformation (Q₁ = exp(π·T₁), rest = I) ---")
Q1_large = expm(np.pi * T[0])
for trial in range(3):
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]
    fd = finite_diff_second_derivative(Q1_large, I2, I2, I2, v1, v2, v3, v4)
    ana, wsq, comm, _ = analytical_second_derivative(Q1_large, I2, I2, I2, v1, v2, v3, v4)
    U = plaquette(Q1_large, I2, I2, I2)
    print(f"  Trial {trial+1}: FD = {fd:+.8f}, Ana = {ana:+.8f}, "
          f"w²U = {wsq:+.8f}, [w,w]U = {comm:+.8f}, "
          f"|FD-Ana| = {abs(fd-ana):.2e}")

# Test 4: Are cross terms ever significant?
print("\n\n" + "=" * 70)
print("CROSS TERM ANALYSIS")
print("=" * 70)

print("\n--- Ratio |comm_term / w²_term| over 100 random configs ---")
ratios = []
for _ in range(100):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]
    _, wsq, comm, _ = analytical_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
    if abs(wsq) > 1e-10:
        ratios.append(abs(comm / wsq))

ratios = np.array(ratios)
print(f"  Mean ratio:   {ratios.mean():.6f}")
print(f"  Max ratio:    {ratios.max():.6f}")
print(f"  Min ratio:    {ratios.min():.6f}")
print(f"  Median ratio: {np.median(ratios):.6f}")
print(f"  Fraction where |comm| > |w²U|: {(ratios > 1.0).mean():.3f}")

# Test 5: Sign of commutator term
print("\n--- Sign distribution of commutator term (100 random) ---")
signs = []
for _ in range(100):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]
    _, _, comm, _ = analytical_second_derivative(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
    signs.append(np.sign(comm) if abs(comm) > 1e-12 else 0)

signs = np.array(signs)
print(f"  Positive: {(signs > 0).sum()}")
print(f"  Negative: {(signs < 0).sum()}")
print(f"  Zero:     {(signs == 0).sum()}")

print("\n\nDone.")
