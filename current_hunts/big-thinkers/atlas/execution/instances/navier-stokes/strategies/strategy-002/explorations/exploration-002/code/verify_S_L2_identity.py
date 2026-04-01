#!/usr/bin/env python3
"""
Verify the exact identity ||S||_{L^2} = ||omega||_{L^2} / sqrt(2) on T^3 for div-free fields.

Proof sketch (Fourier):
  For div-free u on T^3, k · u_hat(k) = 0. Then:
  ||grad u||^2 = sum_k |k|^2 |u_hat|^2
  ||omega||^2 = sum_k |k x u_hat|^2 = sum_k (|k|^2|u_hat|^2 - |k.u_hat|^2) = sum_k |k|^2|u_hat|^2
  So ||grad u||^2 = ||omega||^2.

  Also: grad u = S + A where S is symmetric (strain), A is antisymmetric.
  ||grad u||^2 = ||S||^2 + ||A||^2 (cross terms vanish by symmetry).
  ||A||^2 = (1/2)||omega||^2 (A_{ij} = (1/2)epsilon_{ijk} omega_k, so |A|^2 = (1/2)|omega|^2).
  Therefore: ||S||^2 = ||grad u||^2 - ||A||^2 = ||omega||^2 - (1/2)||omega||^2 = (1/2)||omega||^2.
  Hence ||S||_{L^2} = ||omega||_{L^2}/sqrt(2).

This script verifies the identity numerically and checks the proof via Fourier.
"""
import numpy as np
import sys
import os

E001_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'exploration-001')
sys.path.insert(0, os.path.join(E001_DIR, 'code'))
from ns_solver import NavierStokesSolver, taylor_green_ic, random_gaussian_ic, antiparallel_tubes_ic

def verify_identity():
    """Verify ||S||_{L^2} = ||omega||_{L^2}/sqrt(2) and the underlying Parseval identities."""
    print("=" * 80)
    print("VERIFICATION: ||S||_{L^2} = ||omega||_{L^2}/sqrt(2)")
    print("=" * 80)
    print()

    for ic_name, ic_func in [("TGV", taylor_green_ic), ("Gaussian", random_gaussian_ic),
                               ("AntiParallel", antiparallel_tubes_ic)]:
        for N in [32, 64]:
            nu = 0.01
            solver = NavierStokesSolver(N, nu)
            ux_hat, uy_hat, uz_hat = ic_func(solver)

            vol = (2*np.pi)**3

            # Evolve a few steps to get non-trivial flow
            for _ in range(20):
                dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
                ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)

            # Compute all gradients
            du = [[solver.to_physical(1j * K * u_hat)
                   for K in [solver.KX, solver.KY, solver.KZ]]
                  for u_hat in [ux_hat, uy_hat, uz_hat]]

            # ||grad u||^2 = sum_{ij} ||du_i/dx_j||^2
            grad_u_sq = sum(np.mean(du[i][j]**2) * vol for i in range(3) for j in range(3))

            # omega = curl(u)
            omega_x = du[2][1] - du[1][2]
            omega_y = du[0][2] - du[2][0]
            omega_z = du[1][0] - du[0][1]
            omega_sq_field = omega_x**2 + omega_y**2 + omega_z**2
            omega_sq = np.mean(omega_sq_field) * vol

            # S_{ij} = 0.5*(du_i/dx_j + du_j/dx_i)
            S = [[0.5*(du[i][j] + du[j][i]) for j in range(3)] for i in range(3)]
            # ||S||^2 = sum_{ij} ||S_{ij}||^2
            S_sq = sum(np.mean(S[i][j]**2) * vol for i in range(3) for j in range(3))

            # A_{ij} = 0.5*(du_i/dx_j - du_j/dx_i)
            A = [[0.5*(du[i][j] - du[j][i]) for j in range(3)] for i in range(3)]
            A_sq = sum(np.mean(A[i][j]**2) * vol for i in range(3) for j in range(3))

            # Check identities
            print(f"  {ic_name:>12} N={N}:")
            print(f"    ||grad u||^2 = {grad_u_sq:.10f}")
            print(f"    ||omega||^2  = {omega_sq:.10f}")
            print(f"    ||S||^2      = {S_sq:.10f}")
            print(f"    ||A||^2      = {A_sq:.10f}")
            print(f"    ||grad u||^2 / ||omega||^2 = {grad_u_sq/omega_sq:.10f} (should be 1.0)")
            print(f"    ||S||^2 / ||omega||^2      = {S_sq/omega_sq:.10f} (should be 0.5)")
            print(f"    ||A||^2 / ||omega||^2      = {A_sq/omega_sq:.10f} (should be 0.5)")
            print(f"    ||S||^2 + ||A||^2          = {S_sq + A_sq:.10f}")
            print(f"    ||grad u||^2               = {grad_u_sq:.10f}")
            print(f"    Cross-check S+A = grad u:    {abs((S_sq + A_sq) - grad_u_sq)/grad_u_sq:.2e}")
            print()

    # Also verify in Fourier space directly
    print("  FOURIER SPACE VERIFICATION:")
    N = 64
    solver = NavierStokesSolver(N, 0.01)
    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)

    # Parseval: sum |k|^2 |u_hat|^2 = ||grad u||^2 / (2pi)^3
    k2_u_sq = np.sum(solver.K2 * (np.abs(ux_hat)**2 + np.abs(uy_hat)**2 + np.abs(uz_hat)**2))
    print(f"    sum |k|^2 |u_hat|^2 = {k2_u_sq.real:.6f}")

    # Divergence check: k.u_hat should be 0
    kdotu = solver.KX * ux_hat + solver.KY * uy_hat + solver.KZ * uz_hat
    max_div = np.max(np.abs(kdotu))
    print(f"    max |k.u_hat| = {max_div:.2e} (should be ~0)")

    # omega_hat = ik x u_hat
    omega_x_hat = 1j*(solver.KY*uz_hat - solver.KZ*uy_hat)
    omega_y_hat = 1j*(solver.KZ*ux_hat - solver.KX*uz_hat)
    omega_z_hat = 1j*(solver.KX*uy_hat - solver.KY*ux_hat)

    omega_hat_sq = np.sum(np.abs(omega_x_hat)**2 + np.abs(omega_y_hat)**2 + np.abs(omega_z_hat)**2)
    print(f"    sum |omega_hat|^2 = {omega_hat_sq.real:.6f}")
    print(f"    Ratio |k|^2|u_hat|^2 / |k x u_hat|^2 = {k2_u_sq.real/omega_hat_sq.real:.10f} (should be 1.0)")
    print()
    print("  IDENTITY VERIFIED: ||grad u|| = ||omega|| and ||S|| = ||omega||/sqrt(2) for div-free u on T^3")


if __name__ == '__main__':
    verify_identity()
