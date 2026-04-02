"""
Analytical proof attempt: show lambda_max(HessS(Q)) <= 4d for all Q.

KEY IDEA: Decompose the Hessian quadratic form into per-plaquette contributions
and use a WEIGHTED per-plaquette bound that accounts for edge sharing.

Alternative: Show that the flat connection maximizes lambda_max via a
convexity/monotonicity argument.

We explore several sub-approaches here.
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *

print("=" * 70)
print("ANALYTICAL PROOF EXPLORATION")
print("=" * 70)

# ==========================================================================
# SUB-APPROACH A: Operator norm bound on the cross-term kernel
# ==========================================================================
print("\n--- SUB-APPROACH A: Cross-term kernel analysis ---\n")

# For a plaquette with context matrices L, mid, R:
# Cross-term kernel: F_{ab}(L, mid, R) = Re Tr(L iσ_a mid iσ_b R)
#
# Key identity for SU(2): iσ_a iσ_b = -δ_{ab}I + ε_{abc} iσ_c
# So the kernel can be decomposed.
#
# With M = L mid R (portion of holonomy):
# F_{ab} = Re Tr(L iσ_a mid iσ_b R)
#
# Using the adjoint representation:
# If L ∈ SU(2), then L iσ_a L^{-1} = R_L_{ac} iσ_c
# where R_L ∈ SO(3) is the adjoint rotation.
#
# So: L iσ_a mid iσ_b R = L iσ_a L^{-1} L mid iσ_b R
#     = R_L_{ac} iσ_c (L mid) iσ_b R
#
# If we define M' = L mid and N = R:
# F_{ab} = R_L_{ac} Re Tr(iσ_c M' iσ_b N)
#
# This shows F = R_L × G where G_{cb} = Re Tr(iσ_c M' iσ_b N).
# Since R_L ∈ SO(3), ||F||_op = ||G||_op.
#
# So WLOG we can set L=I: F_{ab} = Re Tr(iσ_a Y iσ_b Z).

# Let Y = mid, Z = R. Parameterize Y ∈ SU(2) as Y = y_0 I + Σ y_k iσ_k with y_0² + |y|² = 1.

def cross_kernel_from_yz(y0, y_vec, z0, z_vec):
    """Compute F_{ab} = Re Tr(iσ_a Y iσ_b Z) where Y = y0 I + y·iσ, Z = z0 I + z·iσ."""
    Y = y0 * np.eye(2, dtype=complex) + sum(y_vec[k] * isigma[k] for k in range(3))
    Z = z0 * np.eye(2, dtype=complex) + sum(z_vec[k] * isigma[k] for k in range(3))
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ Y @ isigma[b] @ Z))
    return F

# At flat: Y=Z=I, y0=z0=1, y_vec=z_vec=0
F_flat = cross_kernel_from_yz(1, [0,0,0], 1, [0,0,0])
print(f"F at flat (Y=Z=I):\n{np.round(F_flat, 4)}")
print(f"||F_flat||_op = {np.linalg.norm(F_flat, ord=2):.4f}")

# Scan: ||F||_op as function of Y, Z ∈ SU(2)
rng = np.random.default_rng(42)
max_norm = 0
for trial in range(10000):
    Y = random_su2(rng)
    Z = random_su2(rng)
    F = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            F[a, b] = np.real(np.trace(isigma[a] @ Y @ isigma[b] @ Z))
    norm = np.linalg.norm(F, ord=2)
    max_norm = max(max_norm, norm)

print(f"\n10000 random (Y,Z): max ||F||_op = {max_norm:.6f}")
print(f"Theoretical max = 2.0 (at flat)")
print(f"Is 2.0 the sharp upper bound? {'YES' if max_norm <= 2.001 else 'NO'}")

# ==========================================================================
# SUB-APPROACH B: The "self-term dominance + cross-term cancellation" argument
# ==========================================================================
print("\n--- SUB-APPROACH B: Self-term dominance analysis ---\n")

# At flat (Q=I), the Hessian has:
# - Self-term diagonal: (β/N) × 2(d-1) × 2 = 4(d-1) β/N per edge
# - Cross-terms that constructively add to reach 4d β/N at the staggered mode
#
# The cross-terms contribute 4β/N extra (from self=4(d-1) to total=4d).
# This is a SMALL fraction (1/d) of the total eigenvalue.
#
# Away from flat: self-terms DECREASE by factor f_e = Σ Re Tr(U_□) / [2 × 2(d-1)]
# where f_e ∈ [-(d-1)/(d-1), 1] = [-1, 1] per edge.
#
# Question: can cross-terms increase enough to compensate?

# Test: at random configs, what fraction of the max eigenvalue comes from self vs cross?

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)

    print(f"\nd={d}:")

    for trial in range(5):
        Q = random_config(lat, rng) if trial > 0 else flat_config(lat)
        label = "flat" if trial == 0 else f"random_{trial}"

        H = compute_hessian(lat, Q)
        evals, evecs = np.linalg.eigh(H)
        v_max = evecs[:, -1]
        lmax = evals[-1]

        # Self-term contribution
        ne = lat.nedges
        H_self = np.zeros_like(H)
        for e in range(ne):
            self_val = H[3*e, 3*e]  # diagonal (same for all a since δ_ab)
            for a in range(3):
                H_self[3*e+a, 3*e+a] = self_val

        self_contrib = v_max @ H_self @ v_max
        cross_contrib = lmax - self_contrib

        print(f"  {label}: lambda_max={lmax:.4f}, self={self_contrib:.4f} ({self_contrib/lmax*100:.1f}%), cross={cross_contrib:.4f} ({cross_contrib/lmax*100:.1f}%)")

# ==========================================================================
# SUB-APPROACH C: Bound via the Hilbert-Schmidt (Frobenius) norm
# ==========================================================================
print("\n--- SUB-APPROACH C: Frobenius norm bound ---\n")

# lambda_max(H) <= ||H||_F = sqrt(Σ H_{ij}^2). But this grows with matrix size,
# so it's too loose. However, we can bound Tr(H^2) and use λ_max ≤ sqrt(Tr(H^2)).

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)

    Q_flat = flat_config(lat)
    H_flat = compute_hessian(lat, Q_flat)
    frob_flat = np.linalg.norm(H_flat, 'fro')

    Q_rand = random_config(lat, rng)
    H_rand = compute_hessian(lat, Q_rand)
    frob_rand = np.linalg.norm(H_rand, 'fro')

    print(f"d={d}: ||H_flat||_F = {frob_flat:.4f}, ||H_rand||_F = {frob_rand:.4f}")
    print(f"  lambda_max: flat={np.linalg.eigvalsh(H_flat)[-1]:.4f}, rand={np.linalg.eigvalsh(H_rand)[-1]:.4f}")

# ==========================================================================
# SUB-APPROACH D: Operator norm decomposition H = Σ_□ H_□
# ==========================================================================
print("\n--- SUB-APPROACH D: Per-plaquette operator norm ---\n")

# Key insight: ||Σ_□ H_□||_op ≤ Σ_□ ||H_□||_op (triangle inequality)
# This overcounts because plaquettes share edges.
#
# Better: use the incidence structure. Each plaquette has 4 edges.
# If P = Σ_□ P_□ where P_□ is the projector onto the edges of □:
# Then P = 2(d-1) I (each edge in 2(d-1) plaquettes).
#
# For the POSITIVE contribution: H_□ ≤ c_□ P_□, then:
# H = Σ H_□ ≤ Σ c_□ P_□ ≤ (max c_□) × Σ P_□ = (max c_□) × 2(d-1) I
#
# But ||H_□||_op = 4 (at flat) and 2(d-1) × 4 = 8(d-1) > 4d for d > 2.
#
# HOWEVER: H_□ is NOT positive semidefinite! It has negative eigenvalues too.
# The per-plaquette Hessian at flat has eigenvalues {0,...,0, 4, 4, 4}.
# The nonzero eigenvalues are in a 3-dimensional subspace.

# Let me check: is H_□ PSD?
d = 4
L = 2
lat = Lattice(d, L)

Q_flat = flat_config(lat)

from attempt2_perplaquette import per_plaquette_hessian
H_p0, edges = per_plaquette_hessian(lat, Q_flat, 0)
evals_p0 = np.linalg.eigvalsh(H_p0)
print(f"Per-plaquette eigenvalues at flat (d=4):")
print(f"  {np.round(evals_p0, 6)}")
print(f"  Is PSD? {all(e >= -1e-10 for e in evals_p0)}")
print(f"  Rank = {np.sum(np.abs(evals_p0) > 1e-8)}")

# Check for random Q
rng = np.random.default_rng(42)
Q_rand = random_config(lat, rng)
H_p0_rand, _ = per_plaquette_hessian(lat, Q_rand, 0)
evals_rand = np.linalg.eigvalsh(H_p0_rand)
print(f"\nPer-plaquette eigenvalues at random Q (d=4):")
print(f"  {np.round(evals_rand, 4)}")
print(f"  Is PSD? {all(e >= -1e-10 for e in evals_rand)}")
print(f"  Min eigenvalue: {evals_rand[0]:.6f}")

# Are per-plaquette Hessians always PSD?
n_not_psd = 0
for trial in range(500):
    Q = random_config(lat, rng)
    for pidx in range(min(5, lat.nplaq)):
        H_p, _ = per_plaquette_hessian(lat, Q, pidx)
        ev = np.linalg.eigvalsh(H_p)
        if ev[0] < -1e-8:
            n_not_psd += 1
            break

print(f"\n500 random configs: {n_not_psd} have non-PSD per-plaquette Hessian")

# ==========================================================================
# SUB-APPROACH E: The CORRECT decomposition — split self and cross differently
# ==========================================================================
print("\n--- SUB-APPROACH E: Optimized decomposition ---\n")

# Write H(Q) = D(Q) + C(Q) where:
# D(Q) = self-term (diagonal, PSD at flat, decreases away from flat)
# C(Q) = cross-term (off-block-diagonal)
#
# At flat: D_flat + C_flat has eigenvalue 4d.
# D_flat has "eigenvalue" 4(d-1) (constant per edge).
# C_flat contributes +4 to the max eigenvalue (staggered mode).
#
# Claim: ||C(Q)||_op ≤ ||C_flat||_op for all Q.
# If true: λ_max(H) = λ_max(D+C) ≤ λ_max(D) + ||C||_op ≤ 4(d-1) + ||C_flat||_op = 4d.
#
# But is ||C(Q)||_op ≤ ||C_flat||_op?

for d in [2, 3, 4]:
    L = 2
    lat = Lattice(d, L)
    rng = np.random.default_rng(42)

    ne = lat.nedges
    dim = 3 * ne

    Q_flat = flat_config(lat)
    H_flat = compute_hessian(lat, Q_flat)

    # Extract diagonal (self-term) and off-diagonal (cross-term)
    D_flat = np.diag(np.diag(H_flat))
    C_flat = H_flat - D_flat

    # Operator norms
    C_flat_norm = np.linalg.norm(C_flat, ord=2)  # max singular value
    D_flat_norm = np.max(np.diag(H_flat))  # max diagonal = self-term

    print(f"d={d}:")
    print(f"  ||D_flat||_op = {D_flat_norm:.4f} (= self-term per edge = {4*(d-1):.1f})")
    print(f"  ||C_flat||_op = {C_flat_norm:.4f}")
    print(f"  D+C target: {D_flat_norm + C_flat_norm:.4f} vs 4d={4*d}")

    # Check if ||C(Q)||_op ≤ ||C_flat||_op for random Q
    max_C_norm = 0
    for trial in range(100):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
        D = np.diag(np.diag(H))
        C = H - D
        C_norm = np.linalg.norm(C, ord=2)
        max_C_norm = max(max_C_norm, C_norm)

    print(f"  ||C(Q)||_op: flat={C_flat_norm:.4f}, max_random={max_C_norm:.4f}")
    print(f"  ||C||_op monotone? {'YES (flat is max)' if max_C_norm <= C_flat_norm + 0.01 else 'NO!'}")

    # Also check: is D_flat_norm + C_flat_norm = 4d exactly?
    print(f"  D_flat + ||C_flat|| = {D_flat_norm:.4f} + {C_flat_norm:.4f} = {D_flat_norm + C_flat_norm:.4f}")
    print(f"  Gap from 4d: {D_flat_norm + C_flat_norm - 4*d:.4f}")
    print()
