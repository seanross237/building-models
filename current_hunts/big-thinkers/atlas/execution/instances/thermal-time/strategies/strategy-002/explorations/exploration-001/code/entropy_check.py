#!/usr/bin/env python3
"""
Detailed entropy scaling verification and BW convergence analysis.
"""

import numpy as np
from scipy.linalg import eigh
from rindler_verification import build_lattice, compute_vacuum_correlators, restrict_to_right_half, mat_sqrt

def entanglement_entropy_from_correlators(N):
    """Compute entanglement entropy for half-chain of N-site lattice."""
    omega, U, K = build_lattice(N)
    X, P = compute_vacuum_correlators(omega, U)
    X_R = restrict_to_right_half(X, N)
    P_R = restrict_to_right_half(P, N)

    Xh = mat_sqrt(X_R)
    D = Xh @ P_R @ Xh
    D = (D + D.T) / 2.0
    nu_sq, _ = eigh(D)
    nu = np.sqrt(np.maximum(nu_sq, 0.25))

    S = 0.0
    for v in nu:
        vp = v + 0.5
        vm = v - 0.5
        if vm > 1e-15:
            S += vp * np.log(vp) - vm * np.log(vm)
        elif vp > 1e-15:
            S += vp * np.log(vp)
    return S, nu

print("="*70)
print("ENTANGLEMENT ENTROPY SCALING")
print("="*70)
print(f"{'N':>6} | {'S':>8} | {'(1/6)ln(2(N+1)/π)':>20} | {'S₀':>8} | {'ν_max':>8} | {'#(ν>0.501)':>11}")
print("-"*70)

Ns = [20, 30, 50, 75, 100, 150, 200, 300, 400]
S_vals = []
ln_vals = []

for N in Ns:
    S, nu = entanglement_entropy_from_correlators(N)
    cc = (1.0/6.0) * np.log(2*(N+1)/np.pi)
    s0 = S - cc
    n_entangled = int(np.sum(nu > 0.501))
    print(f"{N:>6} | {S:>8.4f} | {cc:>20.4f} | {s0:>8.4f} | {nu.max():>8.4f} | {n_entangled:>11}")
    S_vals.append(S)
    ln_vals.append(np.log(N))

# Fit slope
S_arr = np.array(S_vals)
ln_arr = np.array(ln_vals)
# Linear fit: S = a * ln(N) + b
A = np.vstack([ln_arr, np.ones(len(ln_arr))]).T
slope, intercept = np.linalg.lstsq(A, S_arr, rcond=None)[0]
print(f"\nLinear fit: S = {slope:.5f} × ln(N) + {intercept:.4f}")
print(f"Expected slope (c/6 = 1/6): {1/6:.5f}")
print(f"Ratio (computed/expected): {slope / (1/6):.4f}")

# Also check if the number of entangled modes changes
print(f"\n{'='*70}")
print(f"MODULAR SPECTRUM DETAILS FOR N=200")
print(f"{'='*70}")
_, nu200 = entanglement_entropy_from_correlators(200)
nu200_sorted = np.sort(nu200)[::-1]
print(f"Top 10 symplectic eigenvalues:")
for i in range(min(10, len(nu200_sorted))):
    v = nu200_sorted[i]
    eps = np.log((2*v+1)/(2*v-1)) if v > 0.5001 else float('inf')
    contrib = 0
    vm, vp = v-0.5, v+0.5
    if vm > 1e-15:
        contrib = vp*np.log(vp) - vm*np.log(vm)
    print(f"  ν_{i} = {v:.8f}, ε_{i} = {eps:>10.4f}, S_contrib = {contrib:.6f}")

# Count modes with ν > threshold
for thresh in [0.5001, 0.501, 0.51, 0.55, 0.6, 0.7]:
    count = np.sum(nu200_sorted > thresh)
    print(f"  modes with ν > {thresh}: {count}")
