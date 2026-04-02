#!/usr/bin/env python3
"""Quick test: run one case (TaylorGreen, Re=100, N=32) to verify the pipeline."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from ns_solver import NavierStokesSolver
from degiorgi_measure import (
    compute_velocity_magnitude_and_gradients,
    compute_Uk_single_snapshot,
    compute_Uk_from_snapshots_fast,
    compute_normalization_factor,
    measure_degiorgi_sequence,
    compute_bottleneck_integral,
)

N = 32
Re = 100
nu = 1.0 / Re

print("=== Quick Test: TaylorGreen, Re=100, N=32 ===")
solver = NavierStokesSolver(N, nu, cfl=0.4)

# Taylor-Green IC
X, Y, Z = solver.X, solver.Y, solver.Z
ux = np.sin(X) * np.cos(Y) * np.cos(Z)
uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
uz = np.zeros_like(X)
ux_hat, uy_hat, uz_hat = solver.project(
    solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz))
ux_hat = solver.dealias(ux_hat)
uy_hat = solver.dealias(uy_hat)
uz_hat = solver.dealias(uz_hat)

# Check IC
ux_p = solver.to_physical(ux_hat)
uy_p = solver.to_physical(uy_hat)
uz_p = solver.to_physical(uz_hat)
E0 = 0.5 * np.mean(ux_p**2 + uy_p**2 + uz_p**2)
print(f"Initial energy: {E0:.6f}")

# Run short DNS
T_final = 1.0
n_snaps = 10
snap_interval = T_final / n_snaps
_, _, _, snapshots = solver.run(ux_hat, uy_hat, uz_hat, T_final, snapshot_interval=snap_interval)
print(f"DNS done, {len(snapshots)} snapshots collected")

# Check energies
for i, (t, sx, sy, sz) in enumerate(snapshots):
    ux_s = solver.to_physical(sx)
    uy_s = solver.to_physical(sy)
    uz_s = solver.to_physical(sz)
    E = 0.5 * np.mean(ux_s**2 + uy_s**2 + uz_s**2)
    if i == 0 or i == len(snapshots) - 1:
        print(f"  t={t:.4f}: E={E:.6f}")

# Test normalization
norm_factor, U_0_unnorm = compute_normalization_factor(solver, snapshots)
print(f"\nNormalization: factor={norm_factor:.6f}, U_0_unnorm={U_0_unnorm:.6f}")

# Test U_k computation
print("\nU_k sequence:")
K_max = 8
for k in range(K_max + 1):
    U_k, vk_sq, dk_sq = compute_Uk_from_snapshots_fast(solver, snapshots, k, norm_factor)
    print(f"  k={k}: U_k={U_k:.6e}, sup(vk_sq)={np.max(vk_sq):.6e}, int(dk_sq)={np.sum(dk_sq):.6e}")

# Full measurement
print("\n=== Full De Giorgi Measurement ===")
result = measure_degiorgi_sequence(solver, snapshots, K_max=K_max)
print(f"U_0 (normalized): {result['U_0_normalized']:.6f}")
print(f"Monotone: {result['monotone']}")
print(f"K_max used: {result['K_max_used']}")
print(f"beta_eff: {result['beta_eff']:.4f} +/- {result['beta_stderr']:.4f}")
print(f"a_coeff: {result['a_coeff']:.4f}")
print(f"fit R^2: {result['fit_r2']:.4f}")
print(f"U_k values: {[f'{x:.4e}' for x in result['U_k_values']]}")

# Bottleneck test
print("\n=== Bottleneck Integral Test ===")
for k in [2, 3, 4]:
    if k < len(result['U_k_values']) and result['U_k_values'][k] > 1e-30:
        I_k = compute_bottleneck_integral(solver, snapshots, k, norm_factor)
        print(f"  k={k}: I_k={I_k:.6e}, U_{k-1}={result['U_k_values'][k-1]:.6e}")

print("\n=== QUICK TEST PASSED ===")
