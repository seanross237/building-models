#!/usr/bin/env python3
"""
Verify ||S||_{L2} = ||ω||_{L2}/√2 for div-free fields on T³
and decompose the vortex stretching slack into its three components:
1. Hölder alignment loss: |∫Sωω| vs ||S||·||ω||²_L4
2. √2 factor: ||S|| vs ||ω|| (replacing S norm with vorticity norm)
3. Ladyzhenskaya constant: ||ω||_L4 vs C_L·||ω||^{1/4}·||∇ω||^{3/4}

Results:
- ||S||/||ω|| = 1/√2 exactly (machine precision) at all times [VERIFIED]
- At the minimum total slack (t ≈ 1.4, Re=100):
  - Hölder alignment: ~5.4×
  - √2 factor: 1.414× (exact)
  - Ladyzhenskaya on ω: ~31× (much larger than 4.3× for u, because ω is broader in Fourier space)
  - Total: ~237×
"""
import numpy as np
from ns_solver import NavierStokesSolver, taylor_green_ic
from slack_measurements import compute_constants_on_torus

def run_decomposition(Re=100, N=64, target_times=None):
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu)
    constants = compute_constants_on_torus(N_sum=30)
    vol = (2 * np.pi)**3
    C_L = constants['C_L']

    ux_hat, uy_hat, uz_hat = taylor_green_ic(solver, Re)

    if target_times is None:
        target_times = [0.5, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 2.0, 3.0, 5.0]

    t = 0.0
    target_idx = 0
    results = []

    while t < max(target_times) + 0.1 and target_idx < len(target_times):
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)

        if t + dt >= target_times[target_idx] - 0.05:
            ux = solver.to_physical(ux_hat)
            uy = solver.to_physical(uy_hat)
            uz = solver.to_physical(uz_hat)

            dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
            dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
            dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
            duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
            duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
            duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
            duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
            duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
            duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

            omega_x = duz_dy - duy_dz
            omega_y = dux_dz - duz_dx
            omega_z = duy_dx - dux_dy
            omega_sq = omega_x**2 + omega_y**2 + omega_z**2
            omega_L2 = np.sqrt(np.mean(omega_sq) * vol)

            S11 = dux_dx; S22 = duy_dy; S33 = duz_dz
            S12 = 0.5*(dux_dy+duy_dx); S13 = 0.5*(dux_dz+duz_dx); S23 = 0.5*(duy_dz+duz_dy)
            S_L2 = np.sqrt(np.mean(S11**2 + S22**2 + S33**2 + 2*S12**2 + 2*S13**2 + 2*S23**2) * vol)

            vs_int = (S11*omega_x**2 + S22*omega_y**2 + S33*omega_z**2 +
                      2*S12*omega_x*omega_y + 2*S13*omega_x*omega_z + 2*S23*omega_y*omega_z)
            actual_vs = abs(np.mean(vs_int) * vol)

            omega_L4 = (np.mean(omega_sq**2) * vol)**0.25

            holder_bound = S_L2 * omega_L4**2
            level2_bound = omega_L2 * omega_L4**2

            omega_x_hat = 1j*(solver.KY*uz_hat - solver.KZ*uy_hat)
            omega_y_hat = 1j*(solver.KZ*ux_hat - solver.KX*uz_hat)
            omega_z_hat = 1j*(solver.KX*uy_hat - solver.KY*ux_hat)
            norm_fac = vol/N**6
            grad_omega_L2 = np.sqrt(norm_fac * (np.sum(solver.K2*np.abs(omega_x_hat)**2) +
                                                  np.sum(solver.K2*np.abs(omega_y_hat)**2) +
                                                  np.sum(solver.K2*np.abs(omega_z_hat)**2)).real)
            full_bound = C_L**2 * omega_L2**1.5 * grad_omega_L2**1.5

            results.append({
                't': t,
                'actual': actual_vs,
                'holder_bound': holder_bound,
                'level2_bound': level2_bound,
                'full_bound': full_bound,
                'S_over_omega': S_L2 / omega_L2,
                'holder_loss': holder_bound / actual_vs if actual_vs > 1e-30 else float('inf'),
                'sqrt2_loss': level2_bound / holder_bound if holder_bound > 0 else 0,
                'lady_loss': full_bound / level2_bound if level2_bound > 0 else 0,
                'total_slack': full_bound / actual_vs if actual_vs > 1e-30 else float('inf'),
            })

            target_idx += 1

        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt

    return results


if __name__ == '__main__':
    print("=== Re=100 ===")
    results = run_decomposition(Re=100)
    print(f"{'t':>5} | {'Actual':>10} | {'Hölder':>7} | {'√2':>5} | {'Lady':>7} | {'Total':>7}")
    print("-" * 55)
    for r in results:
        print(f"{r['t']:>5.2f} | {r['actual']:>10.4e} | {r['holder_loss']:>7.2f} | {r['sqrt2_loss']:>5.3f} | {r['lady_loss']:>7.2f} | {r['total_slack']:>7.1f}")

    print("\n=== Re=1000 ===")
    results = run_decomposition(Re=1000)
    print(f"{'t':>5} | {'Actual':>10} | {'Hölder':>7} | {'√2':>5} | {'Lady':>7} | {'Total':>7}")
    print("-" * 55)
    for r in results:
        print(f"{r['t']:>5.2f} | {r['actual']:>10.4e} | {r['holder_loss']:>7.2f} | {r['sqrt2_loss']:>5.3f} | {r['lady_loss']:>7.2f} | {r['total_slack']:>7.1f}")
