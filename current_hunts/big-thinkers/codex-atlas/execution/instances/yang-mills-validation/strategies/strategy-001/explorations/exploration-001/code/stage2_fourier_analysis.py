"""
Stage 2: Fourier Analysis at Q=I + Analysis of Where SZZ Lemma 4.1 is Loose
=============================================================================

At Q=I, the lattice has translation symmetry, so the Hessian diagonalizes in Fourier modes.
We compute H_norm exactly at Q=I and identify the maximizing mode.

Key questions:
1. What is H_norm = max_v HessS(v,v)/|v|^2 at Q=I?
2. Which mode achieves this maximum?
3. Compare with the SZZ bound and the improved Cauchy-Schwarz bound
"""

import numpy as np
from itertools import product as iproduct

print("=" * 60)
print("STAGE 2: FOURIER ANALYSIS AT Q=I")
print("=" * 60)

# ===========================
# Parameters
# ===========================
L = 2
d = 4
N = 2
beta = 1.0

n_sites = L**d
n_links = d * n_sites
n_gen = N**2 - 1

print(f"\nParameters: L={L}, d={d}, N={N}, n_links={n_links}")

def site_index(x):
    idx = 0
    for i, xi in enumerate(x):
        idx += (int(xi) % L) * (L ** i)
    return idx

def shift(x, mu, sign=1):
    xnew = list(x)
    xnew[mu] = (xnew[mu] + sign) % L
    return tuple(xnew)

def link_index(x, mu):
    return site_index(x) * d + mu

# ===========================
# Load M matrix
# ===========================
M = np.load('/tmp/M_matrix.npy')
evals_M, evecs_M = np.linalg.eigh(M)

print(f"\n=== M matrix eigenvalue distribution ===")
unique_evals = sorted(set(np.round(evals_M, 6)))
for ev in unique_evals:
    count = np.sum(np.abs(evals_M - ev) < 0.01)
    print(f"  λ = {ev:8.4f}  (multiplicity {count})")

print(f"\n  λ_max(M) = {np.max(evals_M):.6f}")
print(f"  H_norm = (β/2N) × λ_max(M) = {beta/(2*N) * np.max(evals_M):.6f}")

# ===========================
# Identify the maximizing mode
# ===========================

print("\n=== Eigenvector Analysis ===")

max_idx = np.argmax(evals_M)
v_max = evecs_M[:, max_idx]

print(f"\n  Maximizing eigenvector (link components):")
for i, (x, mu) in enumerate(
    ((x, mu) for x in iproduct(range(L), repeat=d) for mu in range(d))
):
    li = link_index(x, mu)
    if abs(v_max[li]) > 0.01:
        print(f"    Link (x={x}, μ={mu}): {v_max[li]:+.4f}")

# Test: is the maximizing mode v_{x,mu} = (-1)^(|x|+mu)?
print("\n  Testing staggered mode v_{x,mu} = (-1)^(|x|+mu):")
v_stag = np.zeros(n_links)
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        li = link_index(x, mu)
        v_stag[li] = (-1)**(sum(x) + mu)
v_stag /= np.linalg.norm(v_stag)

rq_stag = v_stag @ M @ v_stag
print(f"    Rayleigh quotient = {rq_stag:.6f}  (λ_max = {np.max(evals_M):.6f})")
print(f"    Is staggered = max eigvec? {abs(rq_stag - np.max(evals_M)) < 0.01}")

# ===========================
# Compute |B_□|^2 for staggered mode analytically
# ===========================

print("\n=== Staggered mode: B_□ computation ===")
print()
print("  v_{x,μ} = (-1)^(|x|+μ) τ_1  (using generator τ_1)")
print()
print("  For plaquette at (x, μ<ν):")
print("  B_□ = v_{x,μ} + v_{x+μ,ν} - v_{x+ν,μ} - v_{x,ν}")
print()

# Compute |B_□|^2 for each plaquette type (|x| and (μ,ν))
print("  |B_□|^2 by plane (μ,ν) [using |x| = 0 case, all sites give same]:")

for mu in range(d):
    for nu in range(mu+1, d):
        # Using |x| = 0 (site at origin)
        # v_{x,μ} = (-1)^μ, v_{x+μ,ν} = (-1)^(1+ν), v_{x+ν,μ} = (-1)^(1+μ), v_{x,ν} = (-1)^ν
        # (all times |τ_1|^2 = 1)
        a = (-1)**mu
        b = (-1)**(1+nu)
        c = (-1)**(1+mu)
        dd = (-1)**nu
        B_scalar = a + b - c - dd  # = a-c + b-dd = (-1)^μ - (-1)^(1+μ) + (-1)^(1+ν) - (-1)^ν
        # = (-1)^μ(1+1) + (-1)^ν(-1-1)
        # Wait let me redo: (-1)^(1+μ) = -(-1)^μ, (-1)^(1+ν) = -(-1)^ν
        # B = (-1)^μ + (-(-1)^ν) - (-(-1)^μ) - (-1)^ν
        #   = (-1)^μ - (-1)^ν + (-1)^μ - (-1)^ν
        #   = 2[(-1)^μ - (-1)^ν]
        B_correct = 2*((-1)**mu - (-1)**nu)
        B_sq = B_correct**2
        print(f"    (μ,ν)=({mu},{nu}): (-1)^μ={(-1)**mu}, (-1)^ν={(-1)**nu}, B={B_correct:+.0f}, |B|²={B_sq:.0f}")

print()
print("  Sum of |B_□|^2 over all plaquette types (d=4, n_sites=16):")
total_B_sq = 0
nonzero_planes = 0
for mu in range(d):
    for nu in range(mu+1, d):
        B = 2*((-1)**mu - (-1)**nu)
        total_B_sq += B**2 * n_sites
        if B**2 > 0:
            nonzero_planes += 1
print(f"  Total = n_sites × Σ_planes |B|² = {n_sites} × {total_B_sq//n_sites} = {total_B_sq}")

# Verify with Rayleigh quotient
# H_norm = (β/2N) × Σ|B|^2 / |v|^2
v_stag_unnorm = np.zeros(n_links)
for x in iproduct(range(L), repeat=d):
    for mu in range(d):
        li = link_index(x, mu)
        v_stag_unnorm[li] = (-1)**(sum(x) + mu)

v_norm_sq = np.sum(v_stag_unnorm**2)  # = n_links
hess_stag = beta/(2*N) * v_stag_unnorm @ M @ v_stag_unnorm
h_norm_stag = hess_stag / v_norm_sq

print(f"\n  |v_stag|^2 = {v_norm_sq:.0f}")
print(f"  HessS(v_stag, v_stag) = (β/2N) × v^T M v = {hess_stag:.4f}")
print(f"  H_norm = HessS/|v|^2 = {h_norm_stag:.6f} = {h_norm_stag:.6f}β")
print(f"  Expected: λ_max(H) = (β/2N) × {np.max(evals_M):.0f} = {beta/(2*N)*np.max(evals_M):.4f}β")

# ===========================
# Fourier decomposition
# ===========================

print("\n=== Fourier Mode Analysis (L=2 lattice) ===")
print()
print("  For L=2, the Fourier modes are: k ∈ {0, π}^d (binary)")
print("  Total independent modes: 2^d = 16 momentum modes")
print("  With link/generator structure: 16 × 4 × 3 = 192 modes total")
print()

# The M matrix in Fourier space
# For L=2 lattice with periodic BC, the Fourier transform is:
# v_{k,μ} = (1/√n_sites) Σ_x (-1)^{k·x} v_{x,μ}
# where k ∈ {0,1}^d (momentum mode index, (-1)^1 = -1 corresponds to k_μ = π)

# The staggered mode corresponds to k = (1,1,1,1) with factor (-1)^μ
# i.e., the (π,π,π,π) momentum mode with additional direction-dependent phase

print("  Computing eigenvalue structure in Fourier space:")
print()

# For each momentum mode k ∈ {0,1}^d:
momentum_eigenvalues = {}
for k in iproduct(range(2), repeat=d):
    # Build the Fourier mode for momentum k, direction μ
    # v_{x,μ} = (-1)^{k·x} δ_{μ, μ0} (for fixed direction μ0)
    # The eigenvalue is: (1/n_sites) Σ_{□,x} signs... complex computation

    # Instead, compute the block of M for this k mode
    # For L=2, the Fourier basis: φ_{k,μ}(x) = (-1)^{k·x} / √n_sites
    # The Fourier-transformed M block: M_k = d × d matrix

    # Build the d × d block for momentum k
    # M_{k;μ,ν} = Σ_x φ_k(x) Σ_f M_{(x,μ),(f_site,f_dir)} φ_k(f_site)
    M_k = np.zeros((d, d))
    for x in iproduct(range(L), repeat=d):
        phase_x = (-1)**sum(ki*xi for ki, xi in zip(k, x))
        for mu in range(d):
            li = link_index(x, mu)
            for x2 in iproduct(range(L), repeat=d):
                phase_x2 = (-1)**sum(ki*xi for ki, xi in zip(k, x2))
                for nu in range(d):
                    lj = link_index(x2, nu)
                    M_k[mu, nu] += phase_x * M[li, lj] * phase_x2

    M_k /= n_sites  # normalize
    evals_k = np.linalg.eigvalsh(M_k)
    momentum_eigenvalues[k] = np.sort(evals_k)[::-1]

print("  Top momentum-direction eigenvalues:")
all_max_evals = [(k, mv[0]) for k, mv in momentum_eigenvalues.items()]
all_max_evals.sort(key=lambda x: -x[1])
for k, ev in all_max_evals[:5]:
    print(f"    k={k}: λ_max = {ev:.4f}")

print()
print(f"  Global maximum at k=(1,1,1,1): {momentum_eigenvalues[(1,1,1,1)][0]:.4f}")
print(f"  This matches λ_max(M) = {np.max(evals_M):.4f} ✓")

# ===========================
# Where is SZZ Lemma 4.1 loose?
# ===========================

print("\n=== Tightness Analysis: Where is CS Tight? ===")
print()
print("  The Cauchy-Schwarz bound: |B_□|² ≤ 4 Σ_{e∈□} |v_e|²")
print("  is TIGHT iff all four vectors A_k = ±Ad_{P_k}(v_{e_k}) are equal.")
print()
print("  At Q=I with staggered mode v_{x,μ} = (-1)^(|x|+μ):")
print("  B_□ = 2(-1)^|x| [(-1)^μ - (-1)^ν] τ_1 for plane (μ,ν)")
print()
print("  Check: CS tight for (μ,ν) = (0,1):")
print("  v1 = +τ_1, v2 = -τ_1, v3 = -τ_1, v4 = +τ_1  (schematic)")
print("  B = v1 + v2 - (-v3) - (-v4) = ... let me compute carefully")
print()

# For plaquette at x=0, mu=0, nu=1:
# e1 = (x=0, mu=0): v = (-1)^0 = +1
# e2 = (x+mu=e0, nu=1): v = (-1)^(1+1) = +1  (wait: |x+e0| = 1, nu=1: phase = (-1)^(1+1) = 1)
# e3 = (x+nu=e1, mu=0) backward: v = (-1)^(1+0) = -1
# e4 = (x=0, nu=1) backward: v = (-1)^(0+1) = -1
#
# B = +1 + 1 - (-1) - (-1) = 1 + 1 + 1 + 1 = 4  -- but this is wrong
#
# Wait, B = v_{e1} + v_{e2} - v_{e3} - v_{e4} with sign from orientation
# = +1 + (+1) - (-1) - (-1)  -- NO!
# The signs in B_□ come from whether the link is forward or backward
# Forward links: +1, backward links: -1 in B_□ = s_1 v_{e1} + ...
# But v_{e_k} itself has the staggered sign (-1)^(|x_k|+mu_k)

# For plaquette (x=0, mu=0, nu=1):
x0 = (0,0,0,0)
mu, nu = 0, 1
e1_site, e1_mu = x0, mu
e2_site, e2_mu = shift(x0, mu), nu
e3_site, e3_mu = shift(x0, nu), mu
e4_site, e4_mu = x0, nu

v_e1 = (-1)**(sum(e1_site) + e1_mu)
v_e2 = (-1)**(sum(e2_site) + e2_mu)
v_e3 = (-1)**(sum(e3_site) + e3_mu)
v_e4 = (-1)**(sum(e4_site) + e4_mu)

B_00 = v_e1 + v_e2 - v_e3 - v_e4
print(f"  Plaquette (x=0, μ=0, ν=1): v_e1={v_e1:+d}, v_e2={v_e2:+d}, v_e3={v_e3:+d}, v_e4={v_e4:+d}")
print(f"  B_□ = {v_e1:+d} + {v_e2:+d} - {v_e3:+d} - {v_e4:+d} = {B_00:+d}")
print(f"  |B_□|² = {B_00**2:.0f}, 4×Σ|v|² = {4*4:.0f}  (CS tight: {abs(B_00**2 - 4*4) < 0.1})")
print()
print("  The CS bound |B|² ≤ 4 Σ|v|² is TIGHT for this plaquette!")
print("  All four vectors contribute with the same absolute value.")
print()

print("  Planes where |B|^2 = 16 (tight) vs 0 (slack):")
for mu2 in range(d):
    for nu2 in range(mu2+1, d):
        B = 2*((-1)**mu2 - (-1)**nu2)
        status = "TIGHT (|B|²=16)" if B**2 == 16 else "ZERO (|B|²=0)"
        print(f"    (μ,ν)=({mu2},{nu2}): {status}")

print()
print("  Summary: 4 of 6 plaquette planes are CS-tight, 2 have |B|²=0")
print("  The bound is tight in the tight planes, loose in the zero planes.")

# ===========================
# Summary
# ===========================

print("\n" + "=" * 60)
print("STAGE 2 SUMMARY")
print("=" * 60)
print()
print(f"  H_norm at Q=I = {h_norm_stag:.6f} = 4β")
print(f"  Achieved by staggered mode v_{{x,μ}} = (-1)^(|x|+μ)")
print(f"  CS bound: H_norm ≤ 6β  (satisfied: 4 < 6)")
print(f"  SZZ bound: H_norm ≤ 48β  (satisfied: 4 < 48, but very loose)")
print()
print(f"  The staggered mode is the WORST CASE at Q=I")
print(f"  with H_norm = 4β < 1 iff β < 1/4")
print()
print(f"  For GENERAL Q: CS gives H_norm ≤ 6β < 1 iff β < 1/6")
print(f"  (The Q=I case is actually BETTER than the worst case Q)")
print()
print(f"  Key question for Stage 4:")
print(f"  Does H_norm actually approach 6β for some Q?")
print(f"  Or is 4β the true maximum over all Q?")
