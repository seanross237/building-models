"""
Debug the sign in the cross-product formula.

Key question: What is [Tₐ,Tᵦ] for Tₐ = iσₐ/2?

[Tₐ,Tᵦ] = (i/2)²[σₐ,σᵦ] = -(1/4)[σₐ,σᵦ] = -(1/4)(2iεₐᵦ꜀σ꜀) = -(i/2)εₐᵦ꜀σ꜀ = -εₐᵦ꜀ T꜀

So [T₁,T₂] = -T₃ (NOT +T₃).

This means [wᵢ,wⱼ] = -(w⃗ᵢ × w⃗ⱼ)·T⃗

And Tr([wᵢ,wⱼ] b) = Tr(-(w⃗ᵢ×w⃗ⱼ)꜀ T꜀ · b⃗_d T_d)
                    = -(w⃗ᵢ×w⃗ⱼ)꜀ b⃗_d Tr(T꜀T_d)
                    = -(w⃗ᵢ×w⃗ⱼ)꜀ b⃗_d (-δ_{cd}/2)
                    = +(1/2)(w⃗ᵢ×w⃗ⱼ)·b⃗

CORRECT FORMULA: Σ_{i<j} Re Tr([wᵢ,wⱼ] U□) = +(1/2) L⃗ · b⃗
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def random_su2():
    return sum(a * t for a, t in zip(np.random.randn(3), T))

def random_SU2():
    return expm(random_su2())

def Ad(Q, v):
    return Q @ v @ Q.conj().T

def to_vec(X):
    return np.array([-2.0 * np.trace(t @ X).real for t in T])

def from_vec(v):
    return sum(vi * ti for vi, ti in zip(v, T))

def re_tr(M):
    return np.trace(M).real

def plaquette(Q1, Q2, Q3, Q4):
    return Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T

def compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    Q3inv = Q3.conj().T
    U = Q1 @ Q2 @ Q3inv @ Q4.conj().T
    P3 = Q1 @ Q2 @ Q3inv
    return v1, Ad(Q1, v2), -Ad(P3, v3), -Ad(U, v4)

# ============================================================
# Verify structure constants
# ============================================================
print("Structure constants check: [Tₐ,Tᵦ] = ?")
for a in range(3):
    for b in range(3):
        comm = T[a] @ T[b] - T[b] @ T[a]
        # Express in T basis
        coeffs = to_vec(comm)
        if np.linalg.norm(coeffs) > 1e-10:
            print(f"  [T{a+1},T{b+1}] = {coeffs[0]:+.1f}T₁ {coeffs[1]:+.1f}T₂ {coeffs[2]:+.1f}T₃")

# Expected: [T₁,T₂] = -T₃, [T₂,T₃] = -T₁, [T₃,T₁] = -T₂
# i.e. [Tₐ,Tᵦ] = -εₐᵦ꜀T꜀

# ============================================================
# Test corrected formula: comm = +(1/2) L·b
# ============================================================
print("\n" + "=" * 70)
print("CORRECTED FORMULA: Σ Re Tr([wᵢ,wⱼ] U) = +(1/2) L⃗·b⃗")
print("=" * 70)

max_err = 0.0
for config_id in range(20):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]

    U = plaquette(Q1, Q2, Q3, Q4)
    ws = list(compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4))

    # Direct
    comm_direct = 0.0
    for i in range(4):
        for j in range(i+1, 4):
            comm = ws[i] @ ws[j] - ws[j] @ ws[i]
            comm_direct += re_tr(comm @ U)

    # Cross-product with CORRECTED sign: +(1/2) L·b
    a = re_tr(U) / 2
    b_mat = U - a * I2
    b_vec = to_vec(b_mat)
    w_vecs = [to_vec(w) for w in ws]
    L = np.zeros(3)
    for i in range(4):
        for j in range(i+1, 4):
            L += np.cross(w_vecs[i], w_vecs[j])
    comm_formula = +0.5 * np.dot(L, b_vec)  # CORRECTED: plus sign

    err = abs(comm_direct - comm_formula)
    max_err = max(max_err, err)

    if config_id < 5:
        print(f"  Config {config_id+1}: direct = {comm_direct:+.10f}, "
              f"formula = {comm_formula:+.10f}, error = {err:.2e}")

print(f"\n  Max error over 20 configs: {max_err:.2e}")

# ============================================================
# Full second derivative with corrected formula
# ============================================================
print("\n" + "=" * 70)
print("FULL FORMULA: d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗")
print("=" * 70)

max_err = 0.0
for config_id in range(20):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]

    U = plaquette(Q1, Q2, Q3, Q4)
    ws = list(compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4))
    w = ws[0] + ws[1] + ws[2] + ws[3]

    # Direct matrix
    full_direct = re_tr(w @ w @ U)
    for i in range(4):
        for j in range(i+1, 4):
            full_direct += re_tr((ws[i] @ ws[j] - ws[j] @ ws[i]) @ U)

    # Corrected SU(2) formula
    w_norm_sq = -2.0 * np.trace(w @ w).real
    a = re_tr(U) / 2
    b_mat = U - a * I2
    b_vec = to_vec(b_mat)
    w_vecs = [to_vec(wi) for wi in ws]
    L = np.zeros(3)
    for i in range(4):
        for j in range(i+1, 4):
            L += np.cross(w_vecs[i], w_vecs[j])

    full_formula = -(w_norm_sq / 2) * a + 0.5 * np.dot(L, b_vec)

    err = abs(full_direct - full_formula)
    max_err = max(max_err, err)

    if config_id < 5:
        print(f"  Config {config_id+1}: direct = {full_direct:+.10f}, "
              f"formula = {full_formula:+.10f}, error = {err:.2e}")

print(f"\n  Max error over 20 configs: {max_err:.2e}")

# ============================================================
# Also verify against finite differences
# ============================================================
print("\n" + "=" * 70)
print("VS FINITE DIFFERENCES")
print("=" * 70)

def perturbed_plaquette(Q1, Q2, Q3, Q4, v1, v2, v3, v4, t):
    return plaquette(expm(t*v1)@Q1, expm(t*v2)@Q2, expm(t*v3)@Q3, expm(t*v4)@Q4)

max_err = 0.0
for config_id in range(10):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]

    h = 1e-4
    fd = (re_tr(perturbed_plaquette(Q1,Q2,Q3,Q4,v1,v2,v3,v4,h))
          - 2*re_tr(perturbed_plaquette(Q1,Q2,Q3,Q4,v1,v2,v3,v4,0))
          + re_tr(perturbed_plaquette(Q1,Q2,Q3,Q4,v1,v2,v3,v4,-h))) / h**2

    # Full formula
    U = plaquette(Q1,Q2,Q3,Q4)
    ws = list(compute_w_vectors(Q1,Q2,Q3,Q4,v1,v2,v3,v4))
    w = sum(ws)
    w_norm_sq = -2.0 * np.trace(w @ w).real
    a = re_tr(U) / 2
    b_vec = to_vec(U - a * I2)
    w_vecs = [to_vec(wi) for wi in ws]
    L = np.zeros(3)
    for i in range(4):
        for j in range(i+1, 4):
            L += np.cross(w_vecs[i], w_vecs[j])
    formula = -(w_norm_sq/2)*a + 0.5*np.dot(L, b_vec)

    err = abs(fd - formula)
    max_err = max(max_err, err)
    print(f"  Config {config_id+1}: FD = {fd:+.8f}, Formula = {formula:+.8f}, error = {err:.2e}")

print(f"\n  Max error (vs FD): {max_err:.2e}")
print("\nDone.")
