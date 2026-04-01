"""
Analysis of the extremal configuration for lambda_min(HessS).
Verifies the anti-instanton structure and D+C decomposition.
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from hessian_core import *
from itertools import product as iprod

d = 4; L = 2; beta = 1.0; N = 2
lat = Lattice(d, L)
ne = lat.nedges

print("="*60)
print("ANTI-INSTANTON EXTREMIZER ANALYSIS")
print("="*60)

# Enumerate all axis assignments, find the best
print("\nAll 5/6 non-commuting axis assignments:")
results = []
for axes in iprod(range(3), repeat=d):
    comm = sum(1 for mu in range(d) for nu in range(mu+1,d) if axes[mu]==axes[nu])
    if comm > 1: continue  # Only 5/6 or 6/6
    Q = [isigma[axes[mu]].copy() for mu in range(d) for _ in range(lat.nsites)]
    H = compute_hessian(lat, Q, beta, N)
    D, C = compute_hessian_decomposed(lat, Q, beta, N)
    ev_H = np.linalg.eigvalsh(H)
    ev_C = np.linalg.eigvalsh(C)
    results.append((ev_H[0], axes, min(D), np.linalg.norm(C,ord=2), ev_C[0]))

results.sort()
for lmin, axes, dmin, cnorm, clmin in results[:10]:
    print(f"  axes={axes}: λ_min={lmin:.4f}, D_min={dmin:.1f}, ||C||={cnorm:.4f}")

# Cross-term norm survey
print("\n" + "="*60)
print("DECOHERENCE: ||C(Q)||_op vs ||C_flat||")
print("="*60)

rng = np.random.default_rng(42)
c_norms = []
for _ in range(2000):
    Q = random_config(lat, rng)
    _, C = compute_hessian_decomposed(lat, Q, beta, N)
    c_norms.append(np.linalg.norm(C, ord=2))

Q_flat = flat_config(lat)
_, C_flat = compute_hessian_decomposed(lat, Q_flat, beta, N)
flat_norm = np.linalg.norm(C_flat, ord=2)

print(f"Flat ||C||: {flat_norm:.4f} = 2(d+1) = {2*(d+1)}")
print(f"Random max ||C||: {max(c_norms):.4f}")
print(f"Random mean ||C||: {np.mean(c_norms):.4f}")
print(f"Decoherence holds: {max(c_norms) < flat_norm + 0.001}")
print(f"Violations: {sum(1 for x in c_norms if x > flat_norm + 0.001)}/2000")
