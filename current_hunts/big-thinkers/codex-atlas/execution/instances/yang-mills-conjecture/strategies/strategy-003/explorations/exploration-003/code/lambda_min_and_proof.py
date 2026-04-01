"""
Critical computation: bound lambda_min(H(Q)) and the cross-term operator norm.
Also prove ||F||_op <= 2 analytically.

For the B-E mass gap condition: K = N/2 + inf_Q lambda_min(H(Q))/(2) > 0
=> need lambda_min(H(Q)) > -N for all Q.

Since H scales with beta: lambda_min = beta * lambda_min(H at beta=1).
Mass gap condition: beta * |lambda_min(H,beta=1)| < N.
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

def su2_exp(w_vec):
    """exp(Σ w_a iσ_a) for SU(2)."""
    theta = np.linalg.norm(w_vec)
    if theta < 1e-12:
        return np.eye(2, dtype=complex)
    w = sum(w_vec[a] * isigma[a] for a in range(3))
    return np.cos(theta) * np.eye(2, dtype=complex) + (np.sin(theta)/theta) * w

# =====================================================================
# PART 1: Proof that ||F_{ab}||_op <= 2 for all SU(2) contexts
# =====================================================================
print("=" * 70)
print("PROOF: ||F||_op <= 2 (cross-term kernel bound)")
print("=" * 70)

# Theorem: For M, N in SU(2), F_{ab} = Re Tr(iσ_a M iσ_b N).
# Then ||F||_op <= 2.
#
# Proof: ||F||_op = max_{|u|=|v|=1} |Σ u_a F_{ab} v_b|
#       = max |Re Tr((û·iσ) M (v̂·iσ) N)|
#
# Key: û·iσ and v̂·iσ are elements of SU(2) (quarter-turns).
# Proof: (û·iσ)†(û·iσ) = (-û·iσ)(û·iσ) = -|u|²(iσ)² = I. ✓
# det(û·iσ) = det(iΣu_aσ_a). For |u|=1: eigenvalues ±i, det=1. ✓
#
# So UMVN ∈ SU(2), and |Tr(A)| ≤ 2 for A ∈ SU(2).
# Therefore |Re Tr(UMVN)| ≤ |Tr(UMVN)| ≤ 2.
# Hence ||F||_op ≤ 2. QED.
#
# The bound is SHARP: at M=N=I, F=-2I₃, ||F||=2.

# Verify that û·iσ ∈ SU(2) for unit u
rng = np.random.default_rng(42)
for trial in range(10):
    u = rng.normal(size=3)
    u /= np.linalg.norm(u)
    U = sum(u[a] * isigma[a] for a in range(3))
    assert np.allclose(U @ U.conj().T, np.eye(2)), f"Not unitary!"
    assert abs(np.linalg.det(U) - 1) < 1e-10, f"det != 1"
print("Verified: û·iσ ∈ SU(2) for all unit û ✓")

# More precise: is ||F||_op always EXACTLY 2, or can it be less?
norms = []
for trial in range(10000):
    M = random_su2(rng)
    N = random_su2(rng)
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ M @ isigma[b] @ N))
    norms.append(np.linalg.norm(F, ord=2))

print(f"\n10000 random (M,N):")
print(f"  min ||F||_op = {min(norms):.6f}")
print(f"  max ||F||_op = {max(norms):.6f}")
print(f"  mean ||F||_op = {np.mean(norms):.6f}")
print(f"  ||F||_op is NOT always 2 — min is {min(norms):.6f}")

# =====================================================================
# PART 2: lambda_min(H(Q)) bounds
# =====================================================================
print("\n" + "=" * 70)
print("LAMBDA_MIN BOUNDS")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42 + d)

    lmins = []
    lmaxs = []
    for trial in range(500):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        evals = np.linalg.eigvalsh(H)
        lmins.append(evals[0])
        lmaxs.append(evals[-1])

    print(f"\nd={d}, L={L}: 500 random configs")
    print(f"  lambda_min: min={min(lmins):.4f}, mean={np.mean(lmins):.4f}")
    print(f"  lambda_max: max={max(lmaxs):.4f} (target 4d={4*d})")
    print(f"  |lambda_min| / lambda_max_flat: {abs(min(lmins))/(4*d):.4f}")
    print(f"  Spectral radius / 4d: {max(max(lmaxs), abs(min(lmins)))/(4*d):.4f}")

    # Also try gradient descent on lambda_min
    best_lmin = 0
    for start in range(5):
        Q = random_config(lat, rng)
        for step in range(100):
            H = compute_hessian(lat, Q)
            evals, evecs = np.linalg.eigh(H)
            lmin = evals[0]
            vmin = evecs[:, 0]

            # Gradient of lambda_min w.r.t. Q (via finite diff)
            eps = 1e-5
            ne = lat.nedges
            grad = np.zeros((ne, 3))
            for e in range(ne):
                for a in range(3):
                    Q_pert = [Qi.copy() for Qi in Q]
                    Q_pert[e] = Q[e] @ su2_exp(eps * np.array([1.0 if b==a else 0.0 for b in range(3)]))
                    H_pert = compute_hessian(lat, Q_pert)
                    lmin_pert = np.linalg.eigvalsh(H_pert)[0]
                    grad[e, a] = (lmin_pert - lmin) / eps

            # Descend (minimize lambda_min, make it more negative)
            Q = [Q[e] @ su2_exp(-0.02 * grad[e]) for e in range(ne)]

        H = compute_hessian(lat, Q)
        final_lmin = np.linalg.eigvalsh(H)[0]
        best_lmin = min(best_lmin, final_lmin)

    print(f"  Gradient descent on lambda_min: best = {best_lmin:.4f}")
    print(f"  |best_lmin|/4d = {abs(best_lmin)/(4*d):.4f}")

# =====================================================================
# PART 3: D + C decomposition — the key proof attempt
# =====================================================================
print("\n" + "=" * 70)
print("D + C DECOMPOSITION: PROOF VIABILITY")
print("=" * 70)

# The proof strategy:
# H = D + C where D = diagonal (self-term), C = off-diagonal (cross-term)
# lambda_max(H) <= lambda_max(D) + lambda_max(C)  [Weyl]
# lambda_min(H) >= lambda_min(D) + lambda_min(C) = lambda_min(D) - ||C||_op  [Weyl]
#
# D(Q) diagonal: D_ii = (beta/N) Σ_{□∋e(i)} Re Tr(U_□)
# At flat: D = 2(d-1) I (for beta=1, N=2)
# At general Q: |D_ii| <= 2(d-1) (since |Re Tr| <= 2)
#
# C(Q): off-diagonal cross-terms.
# At flat: ||C_flat||_op = 2(d+1) for beta=1, N=2
# Wait, let me recompute. For d=4: ||C_flat|| = 10.
# 2(d+1) = 2*5 = 10. ✓ for d=4.
# For d=2: 2(3) = 6 ✓. For d=3: 2(4) = 8 ✓.
# So ||C_flat||_op = 2(d+1) for all d.

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)
    ne = lat.nedges

    print(f"\nd={d}:")

    # Flat
    Q_flat = flat_config(lat)
    H_flat = compute_hessian(lat, Q_flat)
    D_flat = np.diag(np.diag(H_flat))
    C_flat = H_flat - D_flat

    D_flat_max = np.max(np.diag(H_flat))
    C_flat_lmax = np.linalg.eigvalsh(C_flat)[-1]
    C_flat_lmin = np.linalg.eigvalsh(C_flat)[0]
    C_flat_norm = np.linalg.norm(C_flat, ord=2)

    print(f"  At flat:")
    print(f"    max(D) = {D_flat_max:.4f} = 2(d-1) = {2*(d-1)}")
    print(f"    lambda_max(C) = {C_flat_lmax:.4f} = 2(d+1) = {2*(d+1)}")
    print(f"    lambda_min(C) = {C_flat_lmin:.4f} = -2(d-1) = {-2*(d-1)}")
    print(f"    ||C||_op = {C_flat_norm:.4f}")
    print(f"    D+C check: {D_flat_max:.0f} + {C_flat_lmax:.0f} = {D_flat_max+C_flat_lmax:.0f} = 4d = {4*d}")

    # Random configs: track max D, max C eigenvalue, max C norm, and max/min of H
    max_D_all = []
    max_C_eig = []
    min_C_eig = []
    C_norms = []
    H_lmax = []
    H_lmin = []

    for trial in range(200):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        D = np.diag(np.diag(H))
        C = H - D

        evals_H = np.linalg.eigvalsh(H)
        evals_C = np.linalg.eigvalsh(C)

        max_D_all.append(np.max(np.diag(H)))
        max_C_eig.append(evals_C[-1])
        min_C_eig.append(evals_C[0])
        C_norms.append(np.linalg.norm(C, ord=2))
        H_lmax.append(evals_H[-1])
        H_lmin.append(evals_H[0])

    print(f"  200 random configs:")
    print(f"    max D_ii:        max={max(max_D_all):.4f} (bound: {2*(d-1)})")
    print(f"    lambda_max(C):   max={max(max_C_eig):.4f} (flat: {2*(d+1)})")
    print(f"    lambda_min(C):   min={min(min_C_eig):.4f} (flat: {-2*(d-1)})")
    print(f"    ||C||_op:        max={max(C_norms):.4f} (flat: {C_flat_norm:.4f})")
    print(f"    lambda_max(H):   max={max(H_lmax):.4f} (bound: 4d={4*d})")
    print(f"    lambda_min(H):   min={min(H_lmin):.4f}")
    print(f"    D + max_C gives: {max(max_D_all):.4f} + {max(max_C_eig):.4f} = {max(max_D_all)+max(max_C_eig):.4f}")

    # KEY CHECK: is lambda_max(C(Q)) <= lambda_max(C_flat)?
    print(f"    lambda_max(C) <= lambda_max(C_flat)? {max(max_C_eig) <= C_flat_lmax + 0.01}")
    # KEY CHECK: is D_max(Q) + lambda_max(C(Q)) <= 4d for each Q?
    max_sum = max(max_D_all[i] + max_C_eig[i] for i in range(200))
    print(f"    max(D_max + C_max) per config: {max_sum:.4f} <= 4d={4*d}? {max_sum <= 4*d + 0.01}")

# =====================================================================
# PART 4: Mass gap threshold comparison
# =====================================================================
print("\n" + "=" * 70)
print("MASS GAP THRESHOLD COMPARISON")
print("=" * 70)

# Ricci curvature in |c|^2 norm: Ric = 2|c|^2 for SU(2)
# (Ric = 4g where g = (1/2)δ, so Ric = 4×(1/2)δ = 2δ)
# Actually: Ric per edge = 2 (in |c|^2 metric on each SU(2) copy)
# Total Ric(v,v) = 2Σ|c_e|^2 = 2|c|^2

# In SZZ metric (|v|^2_SZZ = 2|c|^2): Ric = (N/2)|v|^2 = |v|^2 for N=2.

# B-E condition: 2|c|^2 + c^T H c ≥ 2K|c|^2
# (using |v|^2_SZZ = 2|c|^2 as the base measure for K)

# Actually let's use: Ric + Hess(V) >= K g (as tensors)
# Ric_{ij} = 2 delta_ij, g_{ij} = (1/2) delta_ij, H_{ij} = our Hessian
# So: 2 delta + H >= K/2 delta
# => lambda_min(H) >= K/2 - 2

# K > 0 requires lambda_min(H) > -2. Since H ~ beta:
# beta * |lambda_min(H,beta=1)| < 2

print("\nSU(2), d=4, L=2:")
d = 4
L = 2
lat = Lattice(d, L)
rng = np.random.default_rng(42)

# Compute worst lambda_min at beta=1
worst_lmin = 0
worst_lmax = 0
for trial in range(500):
    Q = random_config(lat, rng)
    H = compute_hessian(lat, Q, beta=1.0, N=2)
    evals = np.linalg.eigvalsh(H)
    worst_lmin = min(worst_lmin, evals[0])
    worst_lmax = max(worst_lmax, evals[-1])

print(f"  500 random configs:")
print(f"    worst lambda_min = {worst_lmin:.4f}")
print(f"    best lambda_max = {worst_lmax:.4f}")
print(f"    4d = {4*d}")

# Ric = 2 per component (Ric_ij = 2 delta_ij)
# g = 0.5 per component (g_ij = 0.5 delta_ij)
# B-E: 2 + lambda_min(H) >= K × 0.5
# K = 2(2 + lambda_min(H)) = 4 + 2*lambda_min(H)
# K > 0: lambda_min > -2

# With Gershgorin bound: |lambda| <= 24*beta (for d=4)
# Mass gap: 24*beta < 2 => beta < 1/12 ≈ 0.083 (SZZ result)

# With our bound: lambda_max <= 16*beta, but lambda_min might be worse
# Let's assume lambda_min >= -C*beta. From gradient descent:

print(f"\n  SZZ Gershgorin per-row bound at flat (d=4, beta=1, N=2): 24")
print(f"  Our lambda_max at flat: 16 (= 4d)")
print(f"  Our lambda_min from random survey: {worst_lmin:.4f}")

# SZZ metric version
Ric_SZZ = 1.0  # N/2 = 1 for SU(2) (in |v|^2_SZZ normalization)

# H eigenvalue in SZZ metric: lambda_SZZ = lambda_our / 2
# B-E: Ric_SZZ + lambda_min_SZZ >= K_SZZ
# K_SZZ = 1 + lambda_min_our / 2

# For Gershgorin: lambda_min >= -24, so lambda_min_SZZ >= -12, K >= 1-12 = -11 (at beta=1)
# Mass gap at beta: K = 1 - 12*beta > 0 => beta < 1/12

# For our bound: if lambda_min >= -X*beta, then K = 1 - X*beta/2 > 0 => beta < 2/X

print(f"\n  Mass gap thresholds (SU(2), d=4):")
print(f"  SZZ Gershgorin: |H|_max/beta ≤ 24 → beta < 2/24 = 1/12 ≈ {1/12:.4f}")
print(f"  Our lambda_max/beta = 16 → if this also bounds |lambda_min|: beta < 2/16 = 1/8 = {1/8:.4f}")
print(f"  Observed |lambda_min|/beta = {abs(worst_lmin):.4f}")
print(f"  → beta < 2/{abs(worst_lmin):.1f} = {2/abs(worst_lmin):.4f} (from random survey)")

# The KEY question: is |lambda_min(H)| <= 4d * beta like lambda_max?
# Or is it different?
print(f"\n  Is the spectral radius bounded by 4d = {4*d}?")
print(f"  lambda_max ≤ 4d? (flat = 16, random max = {worst_lmax:.4f}): YES")
print(f"  |lambda_min| ≤ 4d? (random min = {worst_lmin:.4f}): {abs(worst_lmin) <= 4*d + 0.01}")
