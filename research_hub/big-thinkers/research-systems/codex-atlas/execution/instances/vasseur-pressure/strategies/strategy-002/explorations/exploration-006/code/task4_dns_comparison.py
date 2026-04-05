"""
Task 4: Numerical DNS Comparison — CZ route vs Direct route

Compare the effective bounds from:
  (A) Standard CZ route: ||P^{21}||_{L^r} · ||d_k||_{L^2} · |A_k|^{1/s}
  (B) Direct route: ||v_{k-1}||_{L^b} · ||v_k||_{L^c} (no P^{21} norm)
  (C) Actual integral: compute I_k = ∫∫ P^{21} · d_k · 1_{A_k} dx dt numerically

If (C) << (A) and (C) ~ (B), the direct route captures reality better.
If (C) ~ (A) << (B), CZ is genuinely helping.
"""

import sys
sys.path.insert(0, '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-002/code')

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
from ns_solver import NavierStokesSolver
from degiorgi_measure import (
    compute_velocity_magnitude_and_gradients,
    compute_normalization_factor,
)

def taylor_green_ic(solver):
    """Taylor-Green vortex initial condition."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    return solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz)

def kida_pelz_ic(solver):
    """Kida-Pelz initial condition (stronger nonlinear interaction)."""
    X, Y, Z = solver.X, solver.Y, solver.Z
    ux = np.sin(X) * (np.cos(3*Y) * np.cos(Z) - np.cos(Y) * np.cos(3*Z))
    uy = np.sin(Y) * (np.cos(3*Z) * np.cos(X) - np.cos(Z) * np.cos(3*X))
    uz = np.sin(Z) * (np.cos(3*X) * np.cos(Y) - np.cos(X) * np.cos(3*Y))
    ux_hat, uy_hat, uz_hat = solver.to_spectral(ux), solver.to_spectral(uy), solver.to_spectral(uz)
    return solver.project(ux_hat, uy_hat, uz_hat)

def compute_P21_and_decompose(solver, ux_hat, uy_hat, uz_hat, norm_factor, k):
    """
    Compute P^{21}, the truncated fields, and all quantities needed for
    comparing CZ route vs Direct route.

    Returns dict with all relevant integrals and norms.
    """
    N = solver.N
    vol = (2*np.pi)**3
    dV = vol / N**3

    # Physical fields
    u_mag, grad_umag_sq, grad_u_sq, ux, uy, uz = \
        compute_velocity_magnitude_and_gradients(solver, ux_hat, uy_hat, uz_hat)

    # Normalize
    u_mag_norm = u_mag / norm_factor
    ux_norm, uy_norm, uz_norm = ux/norm_factor, uy/norm_factor, uz/norm_factor
    grad_umag_sq_norm = grad_umag_sq / norm_factor**2
    grad_u_sq_norm = grad_u_sq / norm_factor**2

    # Level k threshold
    lam_k = 1.0 - 2.0**(-k)
    # Level k-1 threshold
    lam_km1 = 1.0 - 2.0**(-(k-1)) if k >= 1 else 0.0

    # v_k = [|u_norm| - λ_k]+
    v_k = np.maximum(u_mag_norm - lam_k, 0.0)
    v_km1 = np.maximum(u_mag_norm - lam_km1, 0.0)

    active_k = v_k > 0
    active_km1 = v_km1 > 0

    # u^{below} at level k-1
    u_mag_norm_safe = np.where(u_mag_norm > 1e-14, u_mag_norm, 1.0)
    ratio_below = np.where(active_km1, lam_km1 / u_mag_norm_safe, 1.0)
    ratio_below[u_mag_norm < 1e-14] = 0.0

    wx = ux_norm * ratio_below  # u^{below}_x
    wy = uy_norm * ratio_below
    wz = uz_norm * ratio_below

    # u^{above} at level k-1
    ax = ux_norm - wx  # u^{above}_x
    ay = uy_norm - wy
    az = uz_norm - wz

    # --- Compute P^{21} spectrally ---
    # P^{21} = (-Δ)^{-1} ∂_i∂_j (u_i^{below} · u_j^{above})
    # P_hat = Σ_{i,j} (-k_i k_j / K^2) * FFT(w_i * a_j)

    w_fields = [wx, wy, wz]
    a_fields = [ax, ay, az]
    K = [solver.KX, solver.KY, solver.KZ]

    P21_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            prod_hat = fftn(w_fields[i] * a_fields[j])
            P21_hat += (-K[i] * K[j]) * prod_hat / solver.K2_safe
    P21_hat[0, 0, 0] = 0
    P21 = ifftn(P21_hat).real

    # --- Compute d_k (gradient of v_k, weighted) ---
    term1 = np.where(u_mag_norm > 1e-14, (v_k / u_mag_norm_safe) * grad_umag_sq_norm, 0.0)
    term2 = np.zeros_like(v_k)
    term2[active_k] = (lam_k / u_mag_norm_safe[active_k]) * grad_u_sq_norm[active_k]
    dk_sq = term1 + term2
    dk_abs = np.sqrt(np.maximum(dk_sq, 0.0))

    # --- Compute R_iR_j(v_k · 1_{v_k>0}) spectrally ---
    # R_iR_j(f) has Fourier symbol -k_i*k_j/|k|^2
    g = v_k.copy()  # v_k is already 0 where 1_{v_k>0} = 0
    g_hat = fftn(g)

    # Sum over i,j of R_iR_j(g):
    # Σ_{i,j} (-k_i k_j / K^2) * g_hat
    # But actually P^{21} involves specific (i,j) components, and the sum is:
    # Σ_{i,j} (u_i^{below} · u_j^{above}) · R_iR_j(g)
    # We need: for each (i,j), compute R_iR_j(g) separately

    # The "direct route" integral:
    # I_direct = Σ_{i,j} ∫ w_i · a_j · R_iR_j(g) dx
    # where g = v_k

    I_direct_integrand = np.zeros((N, N, N))
    for i in range(3):
        for j in range(3):
            RiRj_g_hat = (-K[i] * K[j]) * g_hat / solver.K2_safe
            RiRj_g_hat[0, 0, 0] = 0
            RiRj_g = ifftn(RiRj_g_hat).real
            I_direct_integrand += w_fields[i] * a_fields[j] * RiRj_g

    # ==============================
    # COMPUTE ALL INTEGRALS AND NORMS
    # ==============================

    # (1) Actual integral: I_actual = ∫ |P^{21}| · |d_k| · 1_{A_k} dx
    I_actual = np.sum(np.abs(P21) * dk_abs * active_k.astype(float)) * dV

    # Also compute the signed version: ∫ P^{21} · d_k-like · 1_{A_k} dx
    # The actual energy inequality has ∫ P^{21} · div(u/|u| · v_k) dx
    # For comparison, use ∫ P^{21} · v_k · 1_{A_k} dx (simplified)
    I_actual_Pv = np.sum(P21 * v_k * active_k.astype(float)) * dV
    I_actual_Pv_abs = np.sum(np.abs(P21) * v_k * active_k.astype(float)) * dV

    # (2) Direct route integral: ∫ (u^{below}·u^{above}) · R_iR_j(v_k) dx
    I_direct = np.sum(I_direct_integrand) * dV
    I_direct_abs = np.sum(np.abs(I_direct_integrand)) * dV

    # (3) CZ route bound: ||P^{21}||_{L^{3/2}} · ||v_k||_{L^3}
    P21_L32 = (np.sum(np.abs(P21)**(3/2)) * dV) ** (2/3)
    vk_L3 = (np.sum(np.abs(v_k)**3) * dV) ** (1/3)
    CZ_bound = P21_L32 * vk_L3

    # (4) Direct route bound: ||v_{k-1}||_{L^b} · ||v_k||_{L^c} for optimal b
    # Optimal at b = c = 10/3 (or anywhere in [10/7, 10/3])
    vkm1_L103 = (np.sum(np.abs(v_km1)**(10/3)) * dV) ** (3/10)
    vk_L107 = (np.sum(np.abs(v_k)**(10/7)) * dV) ** (7/10)
    direct_bound_optimal = vkm1_L103 * vk_L107  # b=10/3, c=10/7

    # Also try b=2, c=2
    vkm1_L2 = (np.sum(v_km1**2) * dV) ** 0.5
    vk_L2 = (np.sum(v_k**2) * dV) ** 0.5
    direct_bound_L2 = vkm1_L2 * vk_L2

    # (5) CZ route with the actual Hölder triple from Vasseur
    # ||P^{21}||_{L^{10/7}} · ||d_k||_{L^2} · |A_k|^{1/10}
    P21_L107 = (np.sum(np.abs(P21)**(10/7)) * dV) ** (7/10)
    dk_L2 = (np.sum(dk_sq) * dV) ** 0.5
    Ak_measure = np.sum(active_k.astype(float)) * dV
    CZ_vasseur_bound = P21_L107 * dk_L2 * Ak_measure**(1/10)

    # (6) Additional norms for analysis
    P21_L2 = (np.sum(P21**2) * dV) ** 0.5
    vkm1_Linf = np.max(v_km1)
    vk_Linf = np.max(v_k)

    # (7) U_k and U_{k-1} estimates
    Uk = np.sum(v_k**2) * dV  # spatial integral only (snapshot)
    Ukm1 = np.sum(v_km1**2) * dV

    return {
        'I_actual_Pd1A': I_actual,
        'I_actual_Pv': abs(I_actual_Pv),
        'I_actual_Pv_abs': I_actual_Pv_abs,
        'I_direct': abs(I_direct),
        'I_direct_abs': I_direct_abs,
        'CZ_bound_L32_L3': CZ_bound,
        'CZ_vasseur_bound': CZ_vasseur_bound,
        'direct_bound_L103': direct_bound_optimal,
        'direct_bound_L2': direct_bound_L2,
        'P21_L32': P21_L32,
        'P21_L107': P21_L107,
        'P21_L2': P21_L2,
        'vk_L3': vk_L3,
        'vk_L2': vk_L2,
        'vkm1_L2': vkm1_L2,
        'dk_L2': dk_L2,
        'Ak_measure': Ak_measure,
        'Uk_snapshot': Uk,
        'Ukm1_snapshot': Ukm1,
    }


def run_comparison(name, solver, ux_hat0, uy_hat0, uz_hat0, T_final, nu, K_max=7):
    """Run DNS and compare CZ vs Direct bounds at each De Giorgi level."""

    print(f"\n{'='*70}")
    print(f"CONFIGURATION: {name} (N={solver.N}, ν={nu}, T={T_final})")
    print(f"{'='*70}")

    # Run DNS with snapshots
    ux_hat, uy_hat, uz_hat, snapshots = solver.run(
        ux_hat0, uy_hat0, uz_hat0, T_final, snapshot_interval=T_final/10)

    print(f"DNS complete: {len(snapshots)} snapshots")

    # Normalization
    norm_factor, Linf = compute_normalization_factor(solver, snapshots)
    print(f"L^inf norm: {Linf:.4f}, normalization factor: {norm_factor:.4f}")

    # Use a middle snapshot (most developed turbulence)
    snap_idx = len(snapshots) // 2
    t_snap, sx, sy, sz = snapshots[snap_idx]
    print(f"Using snapshot at t = {t_snap:.4f}")

    # Compare at each De Giorgi level
    print(f"\n{'k':>3} | {'I_actual(P·v)':>14} | {'CZ bound':>14} | {'Direct bound':>14} | {'CZ/actual':>10} | {'Direct/actual':>14} | {'CZ/Direct':>10}")
    print("-" * 95)

    results_by_k = {}

    for k in range(1, K_max + 1):
        try:
            res = compute_P21_and_decompose(solver, sx, sy, sz, norm_factor, k)

            # The actual integral (P·v version, since we're comparing routes for ∫P·v)
            actual = max(res['I_actual_Pv_abs'], 1e-30)
            cz = max(res['CZ_bound_L32_L3'], 1e-30)
            direct = max(res['direct_bound_L103'], 1e-30)

            ratio_cz = cz / actual if actual > 1e-25 else float('nan')
            ratio_direct = direct / actual if actual > 1e-25 else float('nan')
            ratio_cz_direct = cz / direct if direct > 1e-25 else float('nan')

            print(f"{k:>3} | {actual:>14.6e} | {cz:>14.6e} | {direct:>14.6e} | {ratio_cz:>10.2f} | {ratio_direct:>14.2f} | {ratio_cz_direct:>10.4f}")

            results_by_k[k] = res

        except Exception as e:
            print(f"{k:>3} | ERROR: {e}")

    # Now compute effective β from actual integrals
    print(f"\n--- Effective β from U_k ratios ---")
    print(f"{'k':>3} | {'U_k (snap)':>14} | {'U_{k-1} (snap)':>14} | {'β_eff':>10}")
    print("-" * 50)

    for k in range(2, K_max + 1):
        if k in results_by_k and k-1 in results_by_k:
            Uk = max(results_by_k[k]['Uk_snapshot'], 1e-30)
            Ukm1 = max(results_by_k[k-1]['Uk_snapshot'], 1e-30)
            if Ukm1 < 1 and Ukm1 > 1e-25:
                beta_eff = np.log(Uk) / np.log(Ukm1)
                print(f"{k:>3} | {Uk:>14.6e} | {Ukm1:>14.6e} | {beta_eff:>10.4f}")
            else:
                print(f"{k:>3} | {Uk:>14.6e} | {Ukm1:>14.6e} | {'N/A':>10}")

    # Detailed analysis: how much does CZ consolidation help?
    print(f"\n--- CZ consolidation gain analysis ---")
    print(f"{'k':>3} | {'||P21||_{L3/2}':>14} | {'||v_{k-1}||_{L3}²':>16} | {'ratio':>10}")
    print("-" * 55)

    for k in range(1, K_max + 1):
        if k in results_by_k:
            res = results_by_k[k]
            # CZ consolidation: ||P^{21}||_{L^{3/2}} vs ||u^{below}·u^{above}||_{L^{3/2}}
            # The latter is bounded by ||u^{below}||_{L^∞} · ||u^{above}||_{L^{3/2}} = ||v_{k-1}||_{L^{3/2}}
            # But we want ||v_{k-1}||_{L^3}^2 (from Hölder ||u^{below}||_{L^3}·||u^{above}||_{L^3})
            P21_norm = res['P21_L32']
            vkm1_L3_sq = res.get('vkm1_L2', 0)**2  # Approximate
            if vkm1_L3_sq > 1e-25:
                ratio = P21_norm / vkm1_L3_sq
                print(f"{k:>3} | {P21_norm:>14.6e} | {vkm1_L3_sq:>16.6e} | {ratio:>10.4f}")
            else:
                print(f"{k:>3} | {P21_norm:>14.6e} | {vkm1_L3_sq:>16.6e} | {'N/A':>10}")

    return results_by_k


# ===================================================================
# RUN COMPARISONS
# ===================================================================
print("=" * 70)
print("TASK 4: NUMERICAL DNS COMPARISON — CZ vs DIRECT ROUTE")
print("=" * 70)

# Configuration 1: Taylor-Green, N=64, Re=500
N = 64
nu = 0.002  # Re ~ 500
solver1 = NavierStokesSolver(N, nu)
ux0, uy0, uz0 = taylor_green_ic(solver1)
results_tg = run_comparison("Taylor-Green Re≈500", solver1, ux0, uy0, uz0, T_final=2.0, nu=nu)

# Configuration 2: Kida-Pelz, N=64, Re=1000
nu2 = 0.001
solver2 = NavierStokesSolver(N, nu2)
ux0_kp, uy0_kp, uz0_kp = kida_pelz_ic(solver2)
results_kp = run_comparison("Kida-Pelz Re≈1000", solver2, ux0_kp, uy0_kp, uz0_kp, T_final=1.5, nu=nu2)

# Summary comparison
print("\n" + "=" * 70)
print("SUMMARY: CZ vs DIRECT BOUND RATIOS")
print("=" * 70)
print()
print("Ratio > 1 means the bound OVERESTIMATES the actual integral.")
print("Smaller ratio = tighter bound.")
print()
print("CZ bound = ||P^{21}||_{L^{3/2}} · ||v_k||_{L^3}")
print("Direct bound = ||v_{k-1}||_{L^{10/3}} · ||v_k||_{L^{10/7}}")
print()

for name, results in [("Taylor-Green", results_tg), ("Kida-Pelz", results_kp)]:
    print(f"\n{name}:")
    print(f"{'k':>3} | {'CZ/actual':>10} | {'Direct/actual':>14} | {'CZ wins?':>10}")
    print("-" * 45)
    for k in sorted(results.keys()):
        res = results[k]
        actual = max(res['I_actual_Pv_abs'], 1e-30)
        cz = max(res['CZ_bound_L32_L3'], 1e-30)
        direct = max(res['direct_bound_L103'], 1e-30)

        r_cz = cz / actual if actual > 1e-25 else float('nan')
        r_dir = direct / actual if actual > 1e-25 else float('nan')
        winner = "CZ" if r_cz < r_dir else "Direct" if r_dir < r_cz else "Tie"

        if not (np.isnan(r_cz) or np.isnan(r_dir)):
            print(f"{k:>3} | {r_cz:>10.2f} | {r_dir:>14.2f} | {winner:>10}")

print()
print("INTERPRETATION:")
print("If CZ wins at ALL levels → CZ consolidation genuinely improves the bound.")
print("If Direct wins at some levels → there might be room for hybrid approaches.")
