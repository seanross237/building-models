"""
Stage 3: Identify eigenvalues algebraically and understand the structure.

The perp block M_perp has 128×128 eigenvalues, all strictly negative.
Try to relate them to lattice Fourier modes.
"""

import numpy as np
from itertools import product

# Known eigenvalues and multiplicities:
# -40.000000 (×2)     = -8*5
# -31.034578 (×8)
# -24.000000 (×4)     = -8*3
# -22.472136 (×8)
# -21.571683 (×8)
# -20.000000 (×8)     = -4*5
# -15.768967 (×8)
# -13.656854 (×8)     = -(8+4√2) = -4*(2+√2)
# -13.527864 (×8)
# -12.000000 (×16)    = -4*3
#  -8.000000 (×2)     = -8*1
#  -5.768501 (×8)
#  -4.000000 (×16)    = -4*1
#  -3.393739 (×8)
#  -2.462531 (×8)
#  -2.343146 (×8)     = -(8-4√2) = -4*(2-√2)

# Let me check exact values:
import math
sqrt2 = math.sqrt(2)
sqrt5 = math.sqrt(5)

print("Eigenvalue identification attempts:")
known = [-40, -31.034578, -24, -22.472136, -21.571683, -20, -15.768967,
         -13.656854, -13.527864, -12, -8, -5.768501, -4, -3.393739,
         -2.462531, -2.343146]

# Check against simple algebraic numbers
candidates = {}
for a in range(-15, 1):
    for b in range(-15, 16):
        for radical in [1, sqrt2, sqrt5, math.sqrt(3)]:
            val = a + b * radical
            if -45 < val < 0:
                candidates[f"{a}+{b}*{radical:.4f}"] = val
            val2 = a * radical + b
            if -45 < val2 < 0:
                candidates[f"{a}*{radical:.4f}+{b}"] = val2

for ev in known:
    matches = []
    for name, val in candidates.items():
        if abs(val - ev) < 0.001:
            matches.append((name, val))
    if matches:
        print(f"  {ev:+12.6f}: matches {matches[:3]}")
    else:
        print(f"  {ev:+12.6f}: no simple match found")

# More systematic: check -4*(a + b*sqrt(c)) for small integers
print("\n\nSystematic check: -4*(a + b*sqrt(c))")
for ev in known:
    target = -ev / 4
    for c in [2, 3, 5, 6, 7]:
        sc = math.sqrt(c)
        # target = a + b*sc => b = (target - a)/sc
        for a in range(-5, 20):
            b_frac = (target - a) / sc
            if abs(b_frac - round(b_frac)) < 0.001:
                b = round(b_frac)
                print(f"  {ev:+12.6f} = -4*({a} + {b}*√{c}) = -4*{a+b*sc:.6f}")

# Also check: eigenvalues of lattice Laplacian on (Z/2Z)^4
# The Laplacian eigenvalues on Z/LZ are: 2*(1-cos(2πk/L)) for k=0,...,L-1
# For L=2: k=0 gives 0, k=1 gives 2*(1-cos(π)) = 4.
# So Laplacian eigenvalues on (Z/2Z)^d: Sum_{mu} 4*k_mu where k_mu ∈ {0,1}
# = 4*|k| where |k| = number of nonzero components.
# Values: 0, 4, 8, 12, 16 with multiplicities C(4,j) = 1, 4, 6, 4, 1.

d = 4
print("\n\nLattice Laplacian eigenvalues on (Z/2Z)^4:")
for j in range(d+1):
    print(f"  |k| = {j}: eigenvalue = {4*j}, multiplicity = {math.comb(d,j)}")

# The staggered mode has k = (1,1,1,1) → |k| = 4 → eigenvalue = 16.

# Now, M_perp acts on the "perpendicular to n" components.
# It should be related to some combination of lattice Laplacians.

# Let's try to understand M_perp using Fourier analysis.
# On (Z/2Z)^4, the Fourier modes are e^{i*pi*k·x} = (-1)^{k·x} for k ∈ {0,1}^4.
# The edges have an additional direction index mu.

# Let me compute: for each Fourier mode k and direction mu,
# the contribution of that mode to M_perp.

# Actually, let me just diagonalize M_perp by Fourier transform.

L = 2
d = 4
coords = list(product(range(L), repeat=d))

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def staggered_sign(x, mu):
    return (-1) ** (sum(x) + mu)

def edge_index(x, mu):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx * d + mu

# Build M_perp more carefully.
# The "perp to n" part: for n=(0,0,1), perp components are x,y.
# Each edge has 2 perp components. Total: 64*2 = 128.
# Index: 2*edge_index + {0=x, 1=y}.

def build_M_perp():
    n = np.array([0., 0., 1.])
    P_perp_3d = np.eye(3) - np.outer(n, n)  # 3x3
    P_neg_3d = np.outer(n, n) - np.eye(3)   # 3x3
    # For perp components only:
    P_perp = np.eye(2)  # 2x2 identity (x,y block of P_perp_3d)
    P_neg = -np.eye(2)  # x,y block of P_neg_3d

    M = np.zeros((128, 128))

    plaq_data = []
    for x in coords:
        for mu in range(d):
            for nu in range(mu+1, d):
                e1 = (x, mu)
                e2 = (add_mod(x, mu), nu)
                e3 = (add_mod(x, nu), mu)
                e4 = (x, nu)
                ei = [edge_index(*e) for e in [e1, e2, e3, e4]]
                active = (mu + nu) % 2 == 1
                plaq_data.append({'ei': ei, 'active': active})

    for p in plaq_data:
        ei = p['ei']
        if p['active']:
            coeffs_D = {0: 3, 1: 2, 2: -2, 3: -1}
            for j in range(4):
                for k in range(4):
                    block = coeffs_D[j] * coeffs_D[k] * P_perp
                    M[ei[j]*2:ei[j]*2+2, ei[k]*2:ei[k]*2+2] += block

            d_coeffs = [
                {0: 1},
                {0: 1, 1: 1, 2: -1},
                {0: 1, 1: 1, 2: -1, 3: -1}
            ]
            for di_c in d_coeffs:
                for j_local, cj in di_c.items():
                    for k_local, ck in di_c.items():
                        block = 4 * cj * ck * P_neg
                        M[ei[j_local]*2:ei[j_local]*2+2, ei[k_local]*2:ei[k_local]*2+2] += block
        else:
            coeffs_Dp = {0: -1, 3: 1}
            for j in coeffs_Dp:
                for k in coeffs_Dp:
                    block = coeffs_Dp[j] * coeffs_Dp[k] * P_perp
                    M[ei[j]*2:ei[j]*2+2, ei[k]*2:ei[k]*2+2] += block

    return M

M_perp = build_M_perp()
eigs = np.linalg.eigvalsh(M_perp)
print(f"\nM_perp eigenvalues (rebuilt): min={eigs[0]:.6f}, max={eigs[-1]:.10f}")

# Since M_perp acts on 2D perp-to-n space at each edge, and the lattice has
# translational symmetry, M_perp should be block-diagonal in Fourier space.
# Let me do the Fourier transform.

# Fourier basis: for k ∈ {0,1}^4, mu ∈ {0,...,3}:
# f_{k,mu}(x, nu) = delta_{mu,nu} * (-1)^{k·x} / sqrt(16)

# So the 128-dim space decomposes into 16 Fourier modes, each with a 4*2=8 dimensional block
# (4 direction components × 2 perp-to-n components).

# Build Fourier transform matrix
modes = list(product(range(L), repeat=d))  # k-vectors
n_modes = len(modes)
print(f"\nFourier modes: {n_modes}")

# For each (k, mu), the Fourier basis vector is:
# v_{k,mu,alpha}(x, nu, beta) = delta_{mu,nu} * delta_{alpha,beta} * (-1)^{k·x} / sqrt(16)
# where alpha, beta ∈ {0,1} (perp components)

# Build unitary Fourier transform F: 128x128
F = np.zeros((128, 128))
for k_idx, k in enumerate(modes):
    for mu in range(d):
        for alpha in range(2):
            # Column index: k_idx * 8 + mu * 2 + alpha
            col = k_idx * 8 + mu * 2 + alpha
            for x_idx, x in enumerate(coords):
                sign = (-1) ** sum(k[i]*x[i] for i in range(d))
                # Row index: edge_index(x, mu) * 2 + alpha
                row = edge_index(x, mu) * 2 + alpha
                F[row, col] = sign / 4.0  # 1/sqrt(16) = 1/4

# Check unitarity
print(f"F^T F ≈ I: {np.allclose(F.T @ F, np.eye(128))}")

# Transform M_perp to Fourier space
M_fourier = F.T @ M_perp @ F

# Check block structure
print(f"\nM in Fourier space:")
for k_idx, k in enumerate(modes):
    block = M_fourier[k_idx*8:(k_idx+1)*8, k_idx*8:(k_idx+1)*8]
    off_diag_max = 0
    for k2_idx in range(n_modes):
        if k2_idx != k_idx:
            off = M_fourier[k_idx*8:(k_idx+1)*8, k2_idx*8:(k2_idx+1)*8]
            off_diag_max = max(off_diag_max, np.max(np.abs(off)))
    eigs_block = np.linalg.eigvalsh(block)
    print(f"  k={k}: block eigs = {np.sort(eigs_block)}, off-diag max = {off_diag_max:.2e}")

# The staggered mode has k = (1,1,1,1). What's the block there?
k_stag = (1,1,1,1)
k_stag_idx = modes.index(k_stag)
block_stag = M_fourier[k_stag_idx*8:(k_stag_idx+1)*8, k_stag_idx*8:(k_stag_idx+1)*8]
print(f"\nStaggered mode block (k=(1,1,1,1)):")
print(block_stag)
eigs_stag = np.linalg.eigvalsh(block_stag)
print(f"Eigenvalues: {eigs_stag}")

# Check: sum of all Fourier block eigenvalues should match total
all_block_eigs = []
for k_idx in range(n_modes):
    block = M_fourier[k_idx*8:(k_idx+1)*8, k_idx*8:(k_idx+1)*8]
    all_block_eigs.extend(np.linalg.eigvalsh(block))
all_block_eigs.sort()
print(f"\nAll block eigenvalues match M_perp eigenvalues: {np.allclose(sorted(all_block_eigs), sorted(eigs))}")

# =====================================================
# FURTHER: Understanding the block at each k
# =====================================================
print("\n" + "=" * 70)
print("BLOCK STRUCTURE AT EACH FOURIER MODE")
print("=" * 70)

for k_idx, k in enumerate(modes):
    block = M_fourier[k_idx*8:(k_idx+1)*8, k_idx*8:(k_idx+1)*8]
    eig_k = np.sort(np.linalg.eigvalsh(block))
    k_sum = sum(k)
    k_type = "staggered" if k == (1,1,1,1) else ("uniform" if k == (0,0,0,0) else f"|k|={k_sum}")
    print(f"k={k} ({k_type}): eigenvalues = [{', '.join(f'{e:.4f}' for e in eig_k)}]")
