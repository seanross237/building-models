"""
Step 2: Verify the SU(2) cross-product formula for commutator terms.

The claim:
    Σ_{i<j} Re Tr([wᵢ,wⱼ] U□) = -(1/2) L⃗ · b⃗

where L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ and b⃗ is the su(2) part of U□.
"""

import numpy as np
from scipy.linalg import expm

np.random.seed(42)

# ============================================================
# SU(2) utilities (same as step1)
# ============================================================

sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
T = [1j * s / 2 for s in sigma]
I2 = np.eye(2, dtype=complex)

def random_su2():
    alpha = np.random.randn(3)
    return sum(a * t for a, t in zip(alpha, T))

def random_SU2():
    return expm(random_su2())

def Ad(Q, v):
    return Q @ v @ Q.conj().T

def to_vec(X):
    """Extract 3-vector from su(2) element X = Σ αₐ Tₐ.
    Using Tₐ = iσₐ/2, so αₐ = -2 Tr(Tₐ X) = -2 Tr(Tₐ X)."""
    return np.array([-2.0 * np.trace(t @ X).real for t in T])

def from_vec(v):
    """Construct su(2) element from 3-vector."""
    return sum(vi * ti for vi, ti in zip(v, T))

def re_tr(M):
    return np.trace(M).real

def plaquette(Q1, Q2, Q3, Q4):
    return Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T

def compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4):
    Q3inv = Q3.conj().T
    Q4inv = Q4.conj().T
    U = Q1 @ Q2 @ Q3inv @ Q4inv
    P3 = Q1 @ Q2 @ Q3inv
    w1 = v1
    w2 = Ad(Q1, v2)
    w3 = -Ad(P3, v3)
    w4 = -Ad(U, v4)
    return w1, w2, w3, w4

# ============================================================
# Verify cross-product formula
# ============================================================

print("=" * 70)
print("STEP 2: Verify SU(2) Cross-Product Formula for Commutator Terms")
print("=" * 70)

for config_id in range(10):
    Q1, Q2, Q3, Q4 = [random_SU2() for _ in range(4)]
    v1, v2, v3, v4 = [random_su2() for _ in range(4)]

    U = plaquette(Q1, Q2, Q3, Q4)
    w1, w2, w3, w4 = compute_w_vectors(Q1, Q2, Q3, Q4, v1, v2, v3, v4)
    ws = [w1, w2, w3, w4]

    # Method 1: Direct matrix computation
    comm_direct = 0.0
    for i in range(4):
        for j in range(i+1, 4):
            comm = ws[i] @ ws[j] - ws[j] @ ws[i]
            comm_direct += re_tr(comm @ U)

    # Method 2: Cross-product formula
    # Extract su(2) part of U
    a = re_tr(U) / 2  # scalar part: cos(θ/2)
    b_mat = U - a * I2  # su(2) part
    b_vec = to_vec(b_mat)

    # Compute L = Σ_{i<j} w⃗ᵢ × w⃗ⱼ
    w_vecs = [to_vec(w) for w in ws]
    L = np.zeros(3)
    for i in range(4):
        for j in range(i+1, 4):
            L += np.cross(w_vecs[i], w_vecs[j])

    comm_crossproduct = -0.5 * np.dot(L, b_vec)

    # Method 3: Full formula d²/dt² = -(|w|²/2)cos(θ/2) - (1/2)L·b
    w = w1 + w2 + w3 + w4
    w_norm_sq = -2.0 * np.trace(w @ w).real
    theta_half = np.arccos(np.clip(a, -1, 1))
    full_formula = -(w_norm_sq / 2) * a + comm_crossproduct

    # Method 4: Direct matrix computation of full second derivative
    full_direct = re_tr(w @ w @ U) + comm_direct

    print(f"\nConfig {config_id+1}:")
    print(f"  Re Tr(U) = {2*a:.6f},  θ/2 = {theta_half:.4f}")
    print(f"  |w|² = {w_norm_sq:.6f},  |b⃗| = {np.linalg.norm(b_vec):.6f}")
    print(f"  Comm (direct):       {comm_direct:+.10f}")
    print(f"  Comm (cross-prod):   {comm_crossproduct:+.10f}")
    print(f"  Error:               {abs(comm_direct - comm_crossproduct):.2e}")
    print(f"  Full d²/dt² (matrix): {full_direct:+.10f}")
    print(f"  Full d²/dt² (formula):{full_formula:+.10f}")
    print(f"  Error:               {abs(full_direct - full_formula):.2e}")

# ============================================================
# Verify to_vec / from_vec roundtrip and Tr(TaTb) = -δ/2
# ============================================================
print("\n\n" + "=" * 70)
print("SANITY CHECKS")
print("=" * 70)

# Check Tr(TₐTᵦ) = -δ_{ab}/2
print("\nTr(TₐTᵦ):")
for a in range(3):
    row = []
    for b in range(3):
        row.append(f"{np.trace(T[a] @ T[b]).real:+.4f}")
    print(f"  [{', '.join(row)}]")

# Check to_vec/from_vec roundtrip
v = np.random.randn(3)
X = from_vec(v)
v_back = to_vec(X)
print(f"\nRoundtrip test: |v - to_vec(from_vec(v))| = {np.linalg.norm(v - v_back):.2e}")

# Check |b⃗|² = 4 sin²(θ/2)
for _ in range(5):
    Q = random_SU2()
    a_val = re_tr(Q) / 2
    b_mat_val = Q - a_val * I2
    b_vec_val = to_vec(b_mat_val)
    b_norm_sq = np.dot(b_vec_val, b_vec_val)
    expected = 4 * (1 - a_val**2)  # sin²(θ/2) = 1 - cos²(θ/2)
    print(f"  |b⃗|² = {b_norm_sq:.8f}, 4sin²(θ/2) = {expected:.8f}, "
          f"error = {abs(b_norm_sq - expected):.2e}")

print("\nDone.")
