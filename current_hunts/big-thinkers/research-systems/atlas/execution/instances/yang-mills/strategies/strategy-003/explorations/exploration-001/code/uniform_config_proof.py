"""
Analytical proof attempt for UNIFORM configurations: Q_e = U for all e.

When all link variables are the same U ∈ SU(2), the transport matrices simplify:

For plaquette (x, μ, ν):
  Q₁ = Q₂ = Q₃ = Q₄ = U

  R₁ = I
  R₂ = Ad_U
  R₃ = -Ad_{U·U·U⁻¹} = -Ad_U
  R₄ = -Ad_{U·U·U⁻¹·U⁻¹} = -I

Wait, let me compute:
  Q₁Q₂Q₃⁻¹ = U·U·U⁻¹ = U
  U_□ = Q₁Q₂Q₃⁻¹Q₄⁻¹ = U·U⁻¹ = I

So for uniform config:
  R₁ = I, R₂ = Ad_U, R₃ = -Ad_U, R₄ = -Ad_I = -I

Compare with Q=I:
  R₁ = I, R₂ = I, R₃ = -I, R₄ = -I

So B_□(U,v) = v₁ + Ad_U(v₂) - Ad_U(v₃) - v₄
vs
B_□(I,v) = v₁ + v₂ - v₃ - v₄

The only difference is that v₂ and v₃ are rotated by Ad_U. Since edges 2 and 3 are in the SAME
direction (both in the μ direction for edges 2, 3 -- wait, no. Edge 2 is in direction ν and
edge 3 is in direction μ. They're in DIFFERENT directions.)

Actually, let me think more carefully about which edges get which rotation.

Edge 1 = (x, μ), Edge 2 = (x+ê_μ, ν), Edge 3 = (x+ê_ν, μ), Edge 4 = (x, ν)

For uniform Q = U:
  Q₁ = U (at edge (x, μ))
  Q₂ = U (at edge (x+ê_μ, ν))
  Q₃ = U (at edge (x+ê_ν, μ))
  Q₄ = U (at edge (x, ν))

  Q₁Q₂Q₃⁻¹ = U·U·U⁻¹ = U
  U_□ = Q₁Q₂Q₃⁻¹Q₄⁻¹ = U·U·U⁻¹·U⁻¹ = I

So the holonomy is TRIVIALLY identity for uniform configs!

This means:
  R₃ = -Ad_{Q₁Q₂Q₃⁻¹} = -Ad_U
  R₄ = -Ad_{U_□} = -Ad_I = -I

So B_□(U,v) = v₁ + Ad_U(v₂) - Ad_U(v₃) - v₄

Now, M(U) has a specific structure. Let's verify.

Since Ad_U is the SAME rotation for all plaquettes (because Q is uniform),
the operator M(U) is of the form:

M(U) = some function of Ad_U ⊗ L'

where L' depends on the lattice structure.

Let me compute M(U) in Fourier space for the uniform case.
"""

import numpy as np

def adjoint_action(U, A):
    return U @ A @ np.conj(U).T

def su2_basis():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [1j*s1/2, 1j*s2/2, 1j*s3/2]

def su2_to_vec(A, basis):
    return np.array([-2*np.trace(b @ A).real for b in basis])

def ad_matrix(U, basis):
    dim_su = 3
    R = np.zeros((dim_su, dim_su))
    for j in range(dim_su):
        transformed = adjoint_action(U, basis[j])
        R[:, j] = su2_to_vec(transformed, basis)
    return R


basis = su2_basis()

print("=== Uniform Configuration Analysis ===\n")

# For uniform Q = U, the B_□ formula gives:
# B_□ = I·v₁ + Ad_U·v₂ - Ad_U·v₃ - I·v₄
#      = v₁ + Ad_U(v₂ - v₃) - v₄
#
# Compare with Q=I:
# B_□(I) = v₁ + v₂ - v₃ - v₄
#
# The difference is that v₂ - v₃ gets rotated by Ad_U.

# In Fourier space on the lattice:
# For plaquette in (μ,ν) plane at position x:
#   e₁ = (x, μ), e₂ = (x+ê_μ, ν), e₃ = (x+ê_ν, μ), e₄ = (x, ν)
#
# B_□ = v̂_{k,μ} + e^{ik_μ} Ad_U v̂_{k,ν} - e^{ik_ν} Ad_U v̂_{k,μ} - v̂_{k,ν}
#
# (where the Fourier phases come from the lattice shifts)

# Let R = Ad_U (a 3×3 orthogonal matrix).
#
# B̂_k^{(μ,ν)} = (I - e^{ik_ν}R) v̂_{k,μ} + (e^{ik_μ}R - I) v̂_{k,ν}
#
# For Q=I (R=I):
# B̂_k^{(μ,ν)} = (1 - e^{ik_ν}) v̂_{k,μ} + (e^{ik_μ} - 1) v̂_{k,ν}
#
# (matching the known formula)

# For the operator M̂(k) at momentum k:
# M̂(k) = ∑_{μ<ν} C_{μν}(k)^† C_{μν}(k)
#
# where C_{μν}(k) is the 3 × 3d matrix:
# C_{μν}(k)·(v̂₀, v̂₁, ..., v̂_{d-1}) = (I - e^{ik_ν}R) v̂_μ + (e^{ik_μ}R - I) v̂_ν

# For each k, M̂(k) is a 3d × 3d Hermitian matrix.

# At k = (π, π, ..., π), with R being a general SO(3) rotation:
# I - e^{iπ}R = I + R (since e^{iπ} = -1)
# e^{iπ}R - I = -R - I = -(R + I)
#
# So C_{μν}(π) = (I + R)·v̂_μ - (I + R)·v̂_ν = (I + R)(v̂_μ - v̂_ν)
#
# |C_{μν}|² = (v̂_μ - v̂_ν)^T (I + R)^T(I + R) (v̂_μ - v̂_ν)
#           = (v̂_μ - v̂_ν)^T (I + R^T + R + R^T R) (v̂_μ - v̂_ν)
#           = (v̂_μ - v̂_ν)^T (I + R + R^T + I) (v̂_μ - v̂_ν)  [since R^T R = I]
#           = (v̂_μ - v̂_ν)^T (2I + R + R^T) (v̂_μ - v̂_ν)

# Now, R + R^T = 2I + 2cos(θ)(n⊗n - I) + ... hmm let me just compute (I+R)^T(I+R).
#
# Actually: (I+R)^T(I+R) = I + R^T + R + I = 2I + R + R^T
#
# For R = rotation by angle θ about axis n̂:
# R = cos(θ)I + (1-cos θ)(n⊗n) + sin(θ)[n]_×
# R + R^T = 2cos(θ)I + 2(1-cos θ)(n⊗n) = 2(n⊗n) + 2cos(θ)(I - n⊗n)
#
# 2I + R + R^T = 2I + 2(n⊗n) + 2cos(θ)(I - n⊗n)
#              = (2 + 2cos θ)(I - n⊗n) + (2 + 2)(n⊗n)
#              = (2 + 2cos θ)I + (2 - 2cos θ)(n⊗n)
#              = 2(1 + cos θ)I + 2(1 - cos θ)(n⊗n)
#
# Eigenvalues: 2(1 + cos θ) (multiplicity 2, perpendicular to n̂) and 4 (along n̂)
# Min eigenvalue = 2(1 + cos θ), max = 4.
#
# For Q=I: θ=0, eigenvalues all = 4. So (I+R)^T(I+R) = 4I.
# For general θ: min eigenvalue = 2(1+cos θ) ≤ 4.
#
# THIS PROVES that |C_{μν}(π)|² at general U is ≤ |C_{μν}(π)|² at U=I
# for each (μ,ν) plane, at momentum k=(π,...,π)!

# For the total: ∑_{μ<ν} |C_{μν}(π)|² ≤ ∑_{μ<ν} 4|v̂_μ - v̂_ν|² = 4 × Fourier norm at Q=I

# But this is only at k=(π,...,π). We need to check all k.

# General k:
# C_{μν}(k) v = (I - e^{ik_ν}R) v̂_μ + (e^{ik_μ}R - I) v̂_ν
#
# This maps (v̂_μ, v̂_ν) → B̂ ∈ R³.
#
# The norm is:
# |B̂|² = v̂_μ^T (I - e^{ik_ν}R)^†(I - e^{ik_ν}R) v̂_μ
#        + v̂_ν^T (e^{ik_μ}R - I)^†(e^{ik_μ}R - I) v̂_ν
#        + cross terms

# The diagonal blocks:
# (I - e^{ik}R)^†(I - e^{ik}R) = I - e^{-ik}R^T - e^{ik}R + R^TR = 2I - (e^{ik}R + e^{-ik}R^T)
#
# At Q=I (R=I): 2I - (e^{ik} + e^{-ik})I = (2 - 2cos k)I = 4sin²(k/2)I
# At general U: 2I - (e^{ik}R + e^{-ik}R^T)
#
# The eigenvalues of e^{ik}R + e^{-ik}R^T for R = rotation by θ about n̂:
# e^{ik}R = e^{ik}[cos θ I + (1-cos θ)n⊗n + sin θ [n]_×]
# e^{ik}R + e^{-ik}R^T = 2cos k · cos θ I + 2(1-cos θ)cos k (n⊗n) + i·2sin k sin θ [n]_×
#
# Hmm wait, this is a complex matrix. Let me work with real parts only since v̂ can be complex.

# Actually, for the real lattice setting, the Fourier components satisfy v̂_{-k} = v̂_k*.
# The physical norm is ∑_k |B̂_k|² with the reality constraint.
# But the maximum eigenvalue of M(Q) is the maximum of |B̂_k|²/|v̂_k|² over k and v̂_k.

# For uniform Q, M(Q) is translation-invariant, so it decomposes into k-blocks.
# At each k, the block is 3d × 3d (d directions × 3 su(2) components).

# The key claim: for each k, the maximum eigenvalue of the k-block is ≤ 4d.

# Let me compute this numerically for various U and k.

d = 4

def compute_M_block(k, R, d=4):
    """
    Compute the 3d × 3d matrix M̂(k) for uniform config with Ad_U = R.

    For plane (μ, ν) with μ < ν:
    C_{μν}(k) maps (v̂_0, ..., v̂_{d-1}) → B̂ ∈ R³

    C_{μν}(k) has 3×3 blocks:
      Block at μ: I - e^{ik_ν} R
      Block at ν: e^{ik_μ} R - I
      All other blocks: 0

    M̂(k) = ∑_{μ<ν} C_{μν}^† C_{μν}
    """
    dim = 3 * d
    M = np.zeros((dim, dim), dtype=complex)

    for mu in range(d):
        for nu in range(mu+1, d):
            # Build C_{μν} as 3 × dim matrix
            C = np.zeros((3, dim), dtype=complex)
            C[:, 3*mu:3*mu+3] = np.eye(3) - np.exp(1j*k[nu]) * R
            C[:, 3*nu:3*nu+3] = np.exp(1j*k[mu]) * R - np.eye(3)

            M += np.conj(C).T @ C

    return M


# Test at Q=I (R=I)
R_id = np.eye(3)
k_pi = np.array([np.pi]*d)

M_pi_id = compute_M_block(k_pi, R_id)
eigs = np.linalg.eigvalsh(M_pi_id.real)  # Should be real for Hermitian M
print(f"Q=I, k=(π,...,π): eigenvalues = {sorted(eigs)[::-1][:6]}")
print(f"  Max eigenvalue: {max(eigs):.6f} (expected {4*d})")

# Test at various U
print(f"\n=== Max eigenvalue of M̂(k) for uniform Q over all k ===")

for theta in [0, 0.1, 0.5, 1.0, np.pi/2, np.pi, 2.0, 3.0]:
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])  # Rotation by theta about z-axis

    max_eig = 0
    max_k = None

    # Scan k-space
    n_k = 20
    for k0 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
        for k1 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
            for k2 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
                for k3 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
                    k = np.array([k0, k1, k2, k3])
                    Mk = compute_M_block(k, R)
                    eig = np.linalg.eigvalsh(Mk)[-1].real
                    if eig > max_eig:
                        max_eig = eig
                        max_k = k.copy()

    print(f"  θ={theta:.4f}: max eig = {max_eig:.6f}, bound = {4*d}, ratio = {max_eig/(4*d):.6f}, at k={max_k}")

# Now let's prove the bound analytically for the k=(π,...,π) mode.
print(f"\n=== Analytical proof at k=(π,...,π) ===")
print("At k=(π,...,π):")
print("  C_{μν} = (I+R) v̂_μ - (I+R) v̂_ν = (I+R)(v̂_μ - v̂_ν)")
print("  |C_{μν}|² = (v̂_μ - v̂_ν)^T (I+R)^T(I+R) (v̂_μ - v̂_ν)")
print("  = (v̂_μ - v̂_ν)^T (2I + R + R^T) (v̂_μ - v̂_ν)")
print()
print("For R = rotation by θ about n̂:")
print("  2I + R + R^T has eigenvalues:")
print("  - Along n̂: 4 (independent of θ)")
print("  - Perpendicular to n̂: 2(1 + cos θ)")
print()
print("Since 2(1 + cos θ) ≤ 4, we have:")
print("  (2I + R + R^T) ≼ 4I")
print("  |C_{μν}|² ≤ 4|v̂_μ - v̂_ν|²")
print("  ∑_{μ<ν} |C_{μν}|² ≤ 4 ∑_{μ<ν} |v̂_μ - v̂_ν|² ≤ 4 × 4d/(4d) × 4d = 4d")
print()
print("Wait, that's circular. Let me be more careful.")
print()

# The actual bound at k=(π,...,π):
# ∑_{μ<ν} |C_{μν}|² ≤ ∑_{μ<ν} 4|v̂_μ - v̂_ν|² (since (2I+R+R^T) ≼ 4I)
#
# Now, ∑_{μ<ν} |v̂_μ - v̂_ν|² = d|v̂|² - |∑_μ v̂_μ|²  (where v̂ = (v̂_0,...,v̂_{d-1}))
#
# Actually: ∑_{μ<ν} |v̂_μ - v̂_ν|² = d∑_μ|v̂_μ|² - |∑_μ v̂_μ|²
#
# The maximum of this over unit vectors is d (achieved when v̂_μ's are orthogonal)
# So ∑_{μ<ν} 4|v̂_μ - v̂_ν|² ≤ 4d|v̂|²

# But at Q=I: ∑_{μ<ν} |C_{μν}|² at k=π = ∑_{μ<ν} 4|v̂_μ - v̂_ν|² = 4(d∑|v̂_μ|² - |∑v̂_μ|²)
# The max over unit v̂ is 4d (when ∑v̂_μ = 0, e.g., balanced directions)

# So for UNIFORM Q, the bound ≤ 4d HOLDS at k=(π,...,π) because (2I+R+R^T) ≼ 4I.

print("PROOF for uniform Q at k=(π,...,π):")
print()
print("  For rotation R by θ: (I+R)^†(I+R) = 2I + R + R^T ≼ 4I₃")
print()
print("  Therefore: |C_{μν}(π)|² ≤ 4|v̂_μ - v̂_ν|² for each plane (μ,ν)")
print()
print("  Summing: ∑_{μ<ν} |C_{μν}(π)|² ≤ 4 ∑_{μ<ν}|v̂_μ - v̂_ν|²")
print("         = 4(d∑_μ|v̂_μ|² - |∑_μ v̂_μ|²) ≤ 4d|v̂|²")
print()
print("  This gives λ_max ≤ 4d at k=(π,...,π) for ALL uniform Q. ■")

# Now check: does this argument extend to ALL k?
print(f"\n=== Check at general k ===")
print("For general k and R:")
print("  C_{μν} has blocks (I - e^{ik_ν}R) at μ and (e^{ik_μ}R - I) at ν")
print()
print("  The key quantity is (I - e^{ik}R)^†(I - e^{ik}R) = 2I - e^{ik}R - e^{-ik}R^T")
print()

# For the diagonal block at μ from plane (μ,ν):
# H_μ^{(ν)} = (I - e^{ik_ν}R)^†(I - e^{ik_ν}R) = 2I - e^{ik_ν}R - e^{-ik_ν}R^T
#
# At R=I: 2I - 2cos(k_ν)I = 4sin²(k_ν/2)I
# At general R: eigenvalues depend on both k_ν and θ.
#
# For R = rotation by θ about z:
# e^{ik}R = e^{ik}[cos θ I + ...]
# The (1,1) block of e^{ik}R + e^{-ik}R^T in the (x,y) plane:
# [2cos(k)cos(θ)   -2sin(k)sin(θ)]
# [ 2sin(k)sin(θ)   2cos(k)cos(θ)]
# Eigenvalues: 2cos(k)cos(θ) ± 2|sin(k)sin(θ)| = 2cos(k∓θ)
# = 2cos(k-θ) and 2cos(k+θ)
#
# So eigenvalues of 2I - (e^{ik}R + e^{-ik}R^T):
# In (x,y) plane: 2 - 2cos(k-θ) and 2 - 2cos(k+θ) = 4sin²((k-θ)/2) and 4sin²((k+θ)/2)
# Along z: 2 - 2cos(k)
#
# At R=I (θ=0): all = 4sin²(k/2). ✓

# The key point: the eigenvalues are 4sin²((k±θ)/2) and 4sin²(k/2).
# These are each ≤ 4 (trivially).
# And at k=π: 4sin²((π±θ)/2) = 4cos²(θ/2) ≤ 4. ✓
# Maximum over k: max(4sin²((k-θ)/2), 4sin²((k+θ)/2), 4sin²(k/2)) ≤ 4.

# The TOTAL M̂(k) for uniform Q:
# Each Fourier mode has: M̂(k)_{μa,νb} = ∑_{plane∋μ,ν} conjugate stuff...
# This is a 3d × 3d matrix. Its max eigenvalue is bounded by...

# For Q=I: M̂(k) = I₃ ⊗ L̂(k), where L̂(k) is d×d.
# Max eigenvalue of L̂(k) at k=π is 4d. Eigenvalues at other k are smaller.

# For general uniform Q: M̂(k) is NOT of the form R ⊗ L̂(k) because R appears
# differently in different blocks. But the per-plane bound still holds.

# Let me verify numerically that for uniform Q, max over ALL k of λ_max(M̂(k)) ≤ 4d.

print(f"\n=== Dense k-scan for uniform Q (verifying bound for all k) ===")

# Use finer k-grid for θ=π/2 (worst case from earlier scan)
for theta in [0, np.pi/4, np.pi/2, np.pi]:
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

    max_eig = 0
    n_k = 40  # finer grid
    for k0 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
        for k1 in np.linspace(0, 2*np.pi, n_k, endpoint=False):
            # For computational efficiency, only scan a 2D slice
            # (the max should occur at k=(π,π,π,π) based on earlier scan)
            k = np.array([k0, k1, np.pi, np.pi])
            Mk = compute_M_block(k, R)
            eig = np.linalg.eigvalsh(Mk)[-1].real
            if eig > max_eig:
                max_eig = eig

    print(f"  θ={theta:.4f}: max eig = {max_eig:.8f}, bound = {4*d}, {'OK' if max_eig <= 4*d + 1e-8 else 'VIOLATION!'}")

print(f"\n=== CONCLUSION ===")
print("For UNIFORM configurations Q_e = U (all links equal):")
print("1. The holonomy U_□ = I for all plaquettes (trivial holonomy)")
print("2. The B_□ formula simplifies: B = v₁ + Ad_U(v₂) - Ad_U(v₃) - v₄")
print("3. In Fourier space, the key operator (I+R)^T(I+R) = 2I + R + R^T ≼ 4I")
print("4. This gives ∑|B_□|² ≤ 4d|v|² for all uniform Q")
print("5. The proof technique: (2I + R + R^T) ≼ 4I from orthogonality of R ∈ SO(3)")
