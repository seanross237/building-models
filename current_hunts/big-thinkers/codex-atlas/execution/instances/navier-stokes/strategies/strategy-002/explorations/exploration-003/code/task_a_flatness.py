#!/usr/bin/env python3
"""
Task A: Derive and test C(F4) bound.

Generate random div-free fields on T^3 with controlled flatness F4,
measure effective Ladyzhenskaya constant, and attempt a proof.

F4 = ||omega||^4_{L^4} / (||omega||^2_{L^2})^2  (vorticity flatness)
C_{L,eff} = ||omega||_{L^4} / (||omega||_{L^2}^{1/4} * ||grad omega||_{L^2}^{3/4})
"""
import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import json, os, sys

S001_CODE = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'strategy-001', 'explorations', 'exploration-002', 'code')
E001_CODE = os.path.join(os.path.dirname(__file__), '..', '..', 'exploration-001', 'code')
sys.path.insert(0, S001_CODE)
sys.path.insert(0, E001_CODE)

from ns_solver import NavierStokesSolver, taylor_green_ic, random_gaussian_ic, antiparallel_tubes_ic

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)


def generate_random_divfree(solver, k0=4, seed=None):
    """Generate a random div-free vector field on T^3."""
    rng = np.random.RandomState(seed)
    N = solver.N
    ux_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)
    uy_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)
    uz_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)
    envelope = solver.K_mag**2 * np.exp(-solver.K_mag**2/(2*k0**2))
    envelope[0,0,0] = 0
    ux_hat *= envelope; uy_hat *= envelope; uz_hat *= envelope
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat)
    uy_hat = solver.dealias(uy_hat)
    uz_hat = solver.dealias(uz_hat)
    # Normalize energy
    ux_p = solver.to_physical(ux_hat); uy_p = solver.to_physical(uy_hat); uz_p = solver.to_physical(uz_hat)
    E = 0.5*np.mean(ux_p**2+uy_p**2+uz_p**2)
    if E > 0:
        s = np.sqrt(0.5/E)
        ux_hat *= s; uy_hat *= s; uz_hat *= s
    return ux_hat, uy_hat, uz_hat


def generate_concentrated_divfree(solver, sigma=0.5, seed=None):
    """Generate a concentrated (high-flatness) div-free field via narrow Gaussian vortex."""
    rng = np.random.RandomState(seed)
    X, Y, Z = solver.X, solver.Y, solver.Z
    cx, cy = np.pi + rng.randn()*0.5, np.pi + rng.randn()*0.5
    r2 = (X-cx)**2 + (Y-cy)**2
    omega_z = np.exp(-r2/(2*sigma**2))
    omega_x = np.zeros_like(X); omega_y = np.zeros_like(X)
    # Biot-Savart
    ox_hat = solver.to_spectral(omega_x)
    oy_hat = solver.to_spectral(omega_y)
    oz_hat = solver.to_spectral(omega_z)
    K2s = solver.K2_safe
    px_hat = ox_hat/K2s; py_hat = oy_hat/K2s; pz_hat = oz_hat/K2s
    px_hat[0,0,0]=0; py_hat[0,0,0]=0; pz_hat[0,0,0]=0
    ux_hat = 1j*solver.KY*pz_hat - 1j*solver.KZ*py_hat
    uy_hat = 1j*solver.KZ*px_hat - 1j*solver.KX*pz_hat
    uz_hat = 1j*solver.KX*py_hat - 1j*solver.KY*px_hat
    ux_hat, uy_hat, uz_hat = solver.project(ux_hat, uy_hat, uz_hat)
    ux_hat = solver.dealias(ux_hat); uy_hat = solver.dealias(uy_hat); uz_hat = solver.dealias(uz_hat)
    ux_p = solver.to_physical(ux_hat); uy_p = solver.to_physical(uy_hat); uz_p = solver.to_physical(uz_hat)
    E = 0.5*np.mean(ux_p**2+uy_p**2+uz_p**2)
    if E > 0:
        s = np.sqrt(0.5/E)
        ux_hat *= s; uy_hat *= s; uz_hat *= s
    return ux_hat, uy_hat, uz_hat


def measure_field(solver, ux_hat, uy_hat, uz_hat):
    """Measure F4, C_{L,eff}, and related quantities for a field."""
    vol = (2*np.pi)**3
    # Vorticity
    ox_hat = 1j*(solver.KY*uz_hat - solver.KZ*uy_hat)
    oy_hat = 1j*(solver.KZ*ux_hat - solver.KX*uz_hat)
    oz_hat = 1j*(solver.KX*uy_hat - solver.KY*ux_hat)
    ox = solver.to_physical(ox_hat); oy = solver.to_physical(oy_hat); oz = solver.to_physical(oz_hat)
    osq = ox**2 + oy**2 + oz**2

    omega_L2_sq = np.mean(osq)*vol
    omega_L2 = np.sqrt(omega_L2_sq)
    omega_L4_4 = np.mean(osq**2)*vol
    omega_L4 = omega_L4_4**0.25
    omega_Linf = np.sqrt(np.max(osq))

    # Gradient of omega (spectral)
    go_sq = 0.0
    for w_hat in [ox_hat, oy_hat, oz_hat]:
        for K in [solver.KX, solver.KY, solver.KZ]:
            dw = solver.to_physical(1j*K*w_hat)
            go_sq += np.mean(dw**2)*vol
    grad_omega_L2 = np.sqrt(go_sq)

    F4 = omega_L4_4 / omega_L2_sq**2 if omega_L2_sq > 1e-30 else 1.0
    C_Leff = omega_L4 / (omega_L2**0.25 * grad_omega_L2**0.75) if grad_omega_L2 > 1e-30 else 0.0

    return {
        'F4': F4,
        'C_Leff': C_Leff,
        'omega_L2': omega_L2,
        'omega_L4': omega_L4,
        'omega_Linf': omega_Linf,
        'grad_omega_L2': grad_omega_L2,
    }


def run_task_a():
    """Generate random fields and measure C_Leff vs F4."""
    N = 64
    solver = NavierStokesSolver(N, nu=0.01)
    print("=" * 80)
    print("TASK A: C(F4) BOUND — MEASURING C_Leff vs F4")
    print("=" * 80)

    results = []

    # Broad-spectrum fields with different k0 (low flatness)
    print("\n  Generating broad-spectrum fields (low F4)...")
    for k0 in [2, 3, 4, 6, 8, 10]:
        for seed in range(80):
            ux_hat, uy_hat, uz_hat = generate_random_divfree(solver, k0=k0, seed=seed*100+k0)
            m = measure_field(solver, ux_hat, uy_hat, uz_hat)
            m['type'] = 'broad'; m['k0'] = k0; m['seed'] = seed
            results.append(m)
    print(f"    Generated {len(results)} broad-spectrum fields")

    # Concentrated fields (high flatness)
    print("  Generating concentrated fields (high F4)...")
    n_before = len(results)
    for sigma in [0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0]:
        for seed in range(40):
            ux_hat, uy_hat, uz_hat = generate_concentrated_divfree(solver, sigma=sigma, seed=seed*100+int(sigma*10))
            m = measure_field(solver, ux_hat, uy_hat, uz_hat)
            m['type'] = 'concentrated'; m['sigma'] = sigma; m['seed'] = seed
            results.append(m)
    print(f"    Generated {len(results)-n_before} concentrated fields")

    # DNS snapshots (evolved fields — realistic turbulence)
    print("  Computing DNS snapshot fields...")
    n_before = len(results)
    for ic_name, ic_func in [("TGV", taylor_green_ic), ("Gaussian", random_gaussian_ic)]:
        for Re in [100, 500, 1000]:
            nu = 1.0/Re
            s = NavierStokesSolver(N, nu)
            ux_hat, uy_hat, uz_hat = ic_func(s)
            T_final = min(3.0, 500*nu)
            t = 0
            step = 0
            while t < T_final:
                dt = s.compute_dt(ux_hat, uy_hat, uz_hat)
                dt = min(dt, T_final-t)
                ux_hat, uy_hat, uz_hat = s.rk4_step(ux_hat, uy_hat, uz_hat, dt)
                t += dt; step += 1
                if step % max(1, int(T_final/(dt*20))) == 0:
                    m = measure_field(s, ux_hat, uy_hat, uz_hat)
                    m['type'] = 'DNS'; m['ic'] = ic_name; m['Re'] = Re; m['t'] = t
                    results.append(m)
    print(f"    Generated {len(results)-n_before} DNS snapshots")

    # Analysis
    print(f"\n  TOTAL: {len(results)} fields measured")

    F4_vals = np.array([r['F4'] for r in results])
    CL_vals = np.array([r['C_Leff'] for r in results])

    # Filter valid
    valid = (F4_vals > 0) & (CL_vals > 0) & np.isfinite(F4_vals) & np.isfinite(CL_vals)
    F4_v = F4_vals[valid]
    CL_v = CL_vals[valid]

    print(f"  Valid measurements: {np.sum(valid)}")
    print(f"  F4 range: [{np.min(F4_v):.4f}, {np.max(F4_v):.4f}]")
    print(f"  C_Leff range: [{np.min(CL_v):.4f}, {np.max(CL_v):.4f}]")

    # Power-law fit: C_Leff = A * F4^beta
    logF4 = np.log(F4_v)
    logCL = np.log(CL_v)
    # Linear regression on log-log
    A_fit = np.vstack([logF4, np.ones(len(logF4))]).T
    beta, logA = np.linalg.lstsq(A_fit, logCL, rcond=None)[0]
    A = np.exp(logA)
    # Correlation
    corr = np.corrcoef(logF4, logCL)[0,1]

    print(f"\n  POWER-LAW FIT: C_Leff = {A:.4f} * F4^({beta:.4f})")
    print(f"  Correlation (log-log): r = {corr:.4f}")
    print(f"  Strategy-001 found: exponent = -0.30, r = -0.93")

    # Check bound: is C_Leff <= A * F4^beta for ALL fields?
    predicted = A * F4_v**beta
    ratio = CL_v / predicted
    print(f"\n  C_Leff / predicted: max = {np.max(ratio):.4f}, mean = {np.mean(ratio):.4f}")
    if np.max(ratio) <= 1.01:
        print("  => Power-law IS an upper bound (within 1%)")
    else:
        safety = np.max(CL_v / (A * F4_v**beta))
        print(f"  => Need safety factor {safety:.2f}x to make it a bound")

    # Theoretical analysis
    print("\n  THEORETICAL ANALYSIS:")
    print("  F4 = ||omega||^4_{L^4} / ||omega||^4_{L^2}")
    print("  C_Leff = ||omega||_{L^4} / (||omega||_{L^2}^{1/4} * ||grad omega||^{3/4})")
    print("  So: C_Leff^4 = ||omega||^4_{L^4} / (||omega||_{L^2} * ||grad omega||^3)")
    print("       = F4 * ||omega||^4_{L^2} / (||omega||_{L^2} * ||grad omega||^3)")
    print("       = F4 * ||omega||^3_{L^2} / ||grad omega||^3")
    print("       = F4 * (||omega||_{L^2}/||grad omega||_{L^2})^3")
    print("  Define R = ||omega||_{L^2}/||grad omega||_{L^2} (inverse Poincare ratio)")
    print("  Then: C_Leff^4 = F4 * R^3")
    print("  Since R <= 1/lambda_1 (Poincare): C_Leff^4 <= F4 / lambda_1^3")
    print("  This gives C_Leff ~ F4^{1/4}, NOT F4^{-0.30}!")
    print("  The POSITIVE exponent 1/4 means higher flatness -> HIGHER C_Leff.")
    print("  This contradicts the Strategy-001 finding of a NEGATIVE exponent.")

    R_vals = np.array([r['omega_L2']/r['grad_omega_L2'] for r in results if r['grad_omega_L2']>1e-30])
    print(f"\n  R = ||omega||/||grad omega|| range: [{np.min(R_vals):.4f}, {np.max(R_vals):.4f}]")
    print(f"  Check: C_Leff^4 vs F4*R^3...")
    check_lhs = CL_v**4
    check_rhs = F4_v * np.array([r['omega_L2']/r['grad_omega_L2'] for r in np.array(results)[valid]])**3
    ratio_check = check_lhs / check_rhs
    print(f"  C_Leff^4 / (F4*R^3): mean={np.mean(ratio_check):.6f}, std={np.std(ratio_check):.6f}")
    print(f"  This should be ~1.0 (exact identity). Mean = {np.mean(ratio_check):.6f}")

    # Save results
    save_results = [{k:float(v) if isinstance(v, (np.floating, float)) else v
                     for k,v in r.items()} for r in results]
    with open(os.path.join(RESULTS_DIR, 'task_a_results.json'), 'w') as f:
        json.dump({
            'n_fields': len(results),
            'fit': {'A': float(A), 'beta': float(beta), 'corr': float(corr)},
            'F4_range': [float(np.min(F4_v)), float(np.max(F4_v))],
            'CL_range': [float(np.min(CL_v)), float(np.max(CL_v))],
            'fields': save_results,
        }, f, indent=2, default=str)

    return results, {'A': A, 'beta': beta, 'corr': corr}


if __name__ == '__main__':
    run_task_a()
