#!/usr/bin/env python3
"""
BKM vs Ladyzhenskaya enstrophy bound comparison for 3D Navier-Stokes.

Computes both closures at every timestep and compares:
1. Actual vortex stretching vs both bounds
2. Enstrophy ODE RHS under each closure
3. Effective blow-up times
4. ||omega||_{L^inf} / ||omega||_{L^2} dynamics
5. Young's inequality optimization

Usage: python bkm_comparison.py
Output: results saved to ../results/ as JSON + tables written to stdout
"""

import numpy as np
import json
import os
import sys
import time as time_module
from ns_solver import (NavierStokesSolver, taylor_green_ic,
                       random_gaussian_ic, antiparallel_tubes_ic)

# Constants
C_L = 0.827       # Ladyzhenskaya constant (sharp on R^3, vector field)
C_CZ = 0.24       # Calderon-Zygmund constant (theoretical, from Strategy-001)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'progress.txt')


def write_progress(msg):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"[{time_module.strftime('%H:%M:%S')}] {msg}\n")
    print(msg)


def compute_bkm_diagnostics(solver, ux_hat, uy_hat, uz_hat):
    """Compute all quantities needed for BKM vs Ladyzhenskaya comparison.

    Returns dict with:
    - omega_L2, omega_Linf, grad_omega_L2
    - vortex_stretching (actual, signed)
    - S_Linf (strain L^infinity norm)
    - Ladyzhenskaya bound, BKM bound
    - ODE RHS quantities
    """
    N = solver.N
    vol = (2 * np.pi)**3
    norm_factor = vol / N**6

    # Physical velocities
    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)

    # All velocity gradients
    dux_dx = solver.to_physical(1j * solver.KX * ux_hat)
    dux_dy = solver.to_physical(1j * solver.KY * ux_hat)
    dux_dz = solver.to_physical(1j * solver.KZ * ux_hat)
    duy_dx = solver.to_physical(1j * solver.KX * uy_hat)
    duy_dy = solver.to_physical(1j * solver.KY * uy_hat)
    duy_dz = solver.to_physical(1j * solver.KZ * uy_hat)
    duz_dx = solver.to_physical(1j * solver.KX * uz_hat)
    duz_dy = solver.to_physical(1j * solver.KY * uz_hat)
    duz_dz = solver.to_physical(1j * solver.KZ * uz_hat)

    # Vorticity: omega = curl(u)
    omega_x = duz_dy - duy_dz
    omega_y = dux_dz - duz_dx
    omega_z = duy_dx - dux_dy

    # Strain rate tensor S_{ij} = 0.5 * (du_i/dx_j + du_j/dx_i)
    S11 = dux_dx
    S22 = duy_dy
    S33 = duz_dz
    S12 = 0.5 * (dux_dy + duy_dx)
    S13 = 0.5 * (dux_dz + duz_dx)
    S23 = 0.5 * (duy_dz + duz_dy)

    # Vortex stretching: integral(omega_i S_{ij} omega_j) dx
    vs_integrand = (S11 * omega_x**2 + S22 * omega_y**2 + S33 * omega_z**2 +
                    2*S12 * omega_x * omega_y + 2*S13 * omega_x * omega_z +
                    2*S23 * omega_y * omega_z)
    vortex_stretching = np.mean(vs_integrand) * vol

    # ||omega||_{L^2}
    omega_sq = omega_x**2 + omega_y**2 + omega_z**2
    omega_L2_sq = np.mean(omega_sq) * vol
    omega_L2 = np.sqrt(omega_L2_sq)

    # ||omega||_{L^inf}
    omega_Linf = np.sqrt(np.max(omega_sq))

    # ||nabla omega||_{L^2} via spectral
    omega_x_hat = 1j * (solver.KY * uz_hat - solver.KZ * uy_hat)
    omega_y_hat = 1j * (solver.KZ * ux_hat - solver.KX * uz_hat)
    omega_z_hat = 1j * (solver.KX * uy_hat - solver.KY * ux_hat)

    grad_omega_L2_sq = norm_factor * (
        np.sum(solver.K2 * np.abs(omega_x_hat)**2) +
        np.sum(solver.K2 * np.abs(omega_y_hat)**2) +
        np.sum(solver.K2 * np.abs(omega_z_hat)**2)
    ).real
    grad_omega_L2 = np.sqrt(max(grad_omega_L2_sq, 0.0))

    # ||S||_{L^inf} = max eigenvalue of S at each point, take max over space
    # For symmetric 3x3: compute Frobenius norm as upper bound, or compute eigenvalues
    # Frobenius norm is a safe upper bound: ||S||_{op} <= ||S||_F
    S_Frob_sq = (S11**2 + S22**2 + S33**2 + 2*S12**2 + 2*S13**2 + 2*S23**2)
    S_Linf_frob = np.sqrt(np.max(S_Frob_sq))

    # For a tighter S_Linf, compute actual spectral norm at the max point
    # (find where Frobenius is max, compute eigenvalues there)
    idx_max = np.unravel_index(np.argmax(S_Frob_sq), S_Frob_sq.shape)
    S_local = np.array([
        [S11[idx_max], S12[idx_max], S13[idx_max]],
        [S12[idx_max], S22[idx_max], S23[idx_max]],
        [S13[idx_max], S23[idx_max], S33[idx_max]]
    ])
    S_Linf = np.max(np.abs(np.linalg.eigvalsh(S_local)))

    # Energy and enstrophy
    u_sq = ux**2 + uy**2 + uz**2
    energy = 0.5 * np.mean(u_sq) * vol
    enstrophy = 0.5 * omega_L2_sq

    # Dissipation: nu * ||nabla omega||^2
    dissipation = solver.nu * grad_omega_L2_sq

    # === Ladyzhenskaya bound ===
    # |VS| <= C_L^2 * ||omega||^{3/2} * ||nabla omega||^{3/2}
    # (Using the chain: |VS| <= ||S||_{L^2} * ||omega||_{L^4}^2
    #  with ||S||_{L^2} <= ||omega||_{L^2} and Ladyzhenskaya on ||omega||_{L^4})
    VS_Lad = C_L**2 * omega_L2**1.5 * grad_omega_L2**1.5

    # === BKM bound ===
    # |VS| = |integral(omega_i S_{ij} omega_j)| <= ||omega||^2_{L^2} * ||S||_{L^inf}
    # Then ||S||_{L^inf} <= C_CZ * ||omega||_{L^inf} * (1 + log^+(||nabla omega||/||omega||))
    log_ratio = 0.0
    if omega_L2 > 1e-14 and grad_omega_L2 > omega_L2:
        log_ratio = np.log(grad_omega_L2 / omega_L2)
    log_factor = 1.0 + log_ratio

    VS_BKM = C_CZ * omega_L2_sq * omega_Linf * log_factor

    # Direct BKM bound (without CZ on strain, just using ||S||_{L^inf} directly)
    VS_BKM_direct = omega_L2_sq * S_Linf

    # Empirical C_CZ: what constant makes BKM tight?
    if omega_L2 > 1e-14 and omega_Linf > 1e-14 and log_factor > 1e-14:
        C_CZ_empirical = abs(vortex_stretching) / (omega_L2_sq * omega_Linf * log_factor)
    else:
        C_CZ_empirical = np.nan

    # === Slacks ===
    abs_vs = abs(vortex_stretching)
    if abs_vs > 1e-20:
        slack_Lad = VS_Lad / abs_vs
        slack_BKM = VS_BKM / abs_vs
        slack_BKM_direct = VS_BKM_direct / abs_vs
        advantage = VS_Lad / VS_BKM if VS_BKM > 1e-20 else np.inf
    else:
        slack_Lad = np.inf
        slack_BKM = np.inf
        slack_BKM_direct = np.inf
        advantage = np.nan

    # === ODE RHS ===
    # Ladyzhenskaya ODE RHS (before Young's): C_L^2 * ||omega||^{3/2} * ||nabla omega||^{3/2} - nu * ||nabla omega||^2
    RHS_Lad = VS_Lad - dissipation

    # BKM ODE RHS (before Young's): C_CZ * ||omega||^2 * ||omega||_{Linf} * log_factor - nu * ||nabla omega||^2
    RHS_BKM = VS_BKM - dissipation

    # Actual RHS of enstrophy equation: VS - dissipation
    RHS_actual = vortex_stretching - dissipation

    # === Ladyzhenskaya after Young's inequality ===
    # VS_Lad = C * ||omega||^{3/2} * ||nabla omega||^{3/2}
    # By Young: a*b <= (a^p/p + b^q/q) with 1/p + 1/q = 1
    # We want: C * X^{3/2} * Y^{3/2} <= nu * Y^2 + f(X)
    # Let a = C * X^{3/2}, b = Y^{3/2}
    # Young with p=4, q=4/3: a*b <= eps * b^{4/3} + C(eps) * a^4
    # Wait — let's be systematic:
    # C_L^2 ||omega||^{3/2} ||nabla omega||^{3/2}
    # Use Young: ab <= eps * a^{4/3} / (4/3) + b^4 / (4 * eps^{1/3})
    # With a = ||nabla omega||^{3/2}, b = C_L^2 ||omega||^{3/2}
    # => eps * ||nabla omega||^2 * 3/4 + (C_L^2)^4 * ||omega||^6 / (4 * eps^{1/3})
    # Set eps = 4*nu/3 to absorb dissipation:
    # => nu * ||nabla omega||^2 + (C_L^2)^4 * ||omega||^6 / (4 * (4*nu/3)^{1/3})
    # After absorbing: d/dt(||omega||^2) <= (C_L^8 / (4*(4*nu/3)^{1/3})) * ||omega||^6
    #
    # Actually the standard result is:
    # d/dt ||omega||^2 <= C * ||omega||^6 / nu^3
    # where C = (27/4) * C_L^8  (or similar — let me derive carefully)
    #
    # From: C_L^2 * A^{3/2} * B^{3/2} - nu * B^2
    # where A = ||omega||_{L^2}, B = ||nabla omega||_{L^2}
    # Young: C_L^2 * A^{3/2} * B^{3/2} <= eps * B^2 + C_eps * A^6
    # with eps = nu: C_L^2 * A^{3/2} * B^{3/2} <= nu * B^2 + (27/256) * C_L^8 * A^6 / nu^3
    # (from Young p=4/3, q=4: X^{3/2} Y^{3/2} <= (3/4)*eps*Y^2 + (1/4)*X^6/eps^3
    #  set (3/4)*eps = nu => eps = 4*nu/3
    #  => (1/4) * X^6 / (4*nu/3)^3 = (1/4) * 27/(64*nu^3) * X^6 = 27/(256*nu^3) * X^6
    #  coefficient = 27/(256) * C_L^8)
    #
    # So: d/dt ||omega||^2 <= (27 * C_L^8) / (256 * nu^3) * ||omega||^6
    #
    # Actually, let me just do it more carefully with epsilon optimization.
    # VS <= C_L^2 * X^{3/2} * Y^{3/2}  (X = omega_L2, Y = grad_omega_L2)
    # We need: C_L^2 * X^{3/2} * Y^{3/2} - nu * Y^2 <= f(X)
    # Maximize LHS over Y:
    # d/dY[C_L^2 * X^{3/2} * (3/2) * Y^{1/2} - 2*nu*Y] = 0
    # => Y^{1/2} = (3*C_L^2 * X^{3/2}) / (4*nu)
    # => Y_* = (3*C_L^2 * X^{3/2} / (4*nu))^2 = 9*C_L^4 * X^3 / (16*nu^2)
    # f(X) = C_L^2 * X^{3/2} * Y_*^{3/2} - nu * Y_*^2
    # Y_*^{3/2} = (9*C_L^4/(16*nu^2))^{3/2} * X^{9/2}
    #           = 27*C_L^6/(64*nu^3) * X^{9/2}  (since (9/16)^{3/2} = 27/64)
    # Y_*^2 = 81*C_L^8 * X^6 / (256*nu^4)
    # f(X) = C_L^2 * X^{3/2} * 27*C_L^6/(64*nu^3) * X^{9/2} - nu * 81*C_L^8*X^6/(256*nu^4)
    #       = 27*C_L^8 * X^6 / (64*nu^3) - 81*C_L^8 * X^6 / (256*nu^3)
    #       = C_L^8 * X^6 / nu^3 * (27/64 - 81/256)
    #       = C_L^8 * X^6 / nu^3 * (108/256 - 81/256)
    #       = C_L^8 * X^6 / nu^3 * 27/256
    #
    # So: d/dt ||omega||^2 <= (27/256) * C_L^8 * ||omega||^6 / nu^3
    # But wait, enstrophy = (1/2)||omega||^2, so d/dt(enstrophy) = (1/2) d/dt ||omega||^2
    # The enstrophy equation: (1/2) d/dt ||omega||^2 = VS - nu ||nabla omega||^2
    # So d/dt ||omega||^2 = 2 * VS - 2*nu * ||nabla omega||^2
    # <= 2 * C_L^2 * ||omega||^{3/2} * ||nabla omega||^{3/2} - 2*nu * ||nabla omega||^2
    # Optimization with factor of 2: same structure, multiply result by 2
    #
    # Let me just use the standard result and compute blow-up time numerically.

    # For Ladyzhenskaya Young's optimized bound:
    # d/dt(y) <= alpha_Lad * y^3  where y = ||omega||^2_{L^2}
    # alpha_Lad = 27 * C_L^8 / (128 * nu^3)  (the factor from optimization above, times 2 for the enstrophy eq factor)
    # Wait, let me just be consistent. The enstrophy equation is:
    # (1/2) d/dt E_omega = VS - nu ||nabla omega||^2  where E_omega = ||omega||^2
    # So d/dt E_omega = 2*VS - 2*nu*||nabla omega||^2
    # <= 2*C_L^2 * E_omega^{3/4} * ||nabla omega||^{3/2} - 2*nu*||nabla omega||^2
    # Optimize over ||nabla omega||: maximum of 2*C_L^2 * E_omega^{3/4} * Y^{3/2} - 2*nu*Y^2
    # d/dY = 3*C_L^2 * E_omega^{3/4} * Y^{1/2} - 4*nu*Y = 0
    # Y = (3*C_L^2 * E_omega^{3/4} / (4*nu))^2 = 9*C_L^4 * E_omega^{3/2} / (16*nu^2)
    # => d/dt E_omega <= 2*C_L^2*E_omega^{3/4} * (9*C_L^4*E_omega^{3/2}/(16*nu^2))^{3/2}
    #                    - 2*nu*(9*C_L^4*E_omega^{3/2}/(16*nu^2))^2
    # This gives: d/dt E_omega <= alpha_Lad * E_omega^3
    # I'll compute alpha_Lad numerically to avoid algebra errors.

    # Just compute alpha directly:
    # d/dt y <= max_{Y>=0} [2*C_L^2 * y^{3/4} * Y^{3/2} - 2*nu*Y^2]
    # = 2 * y^{3/4} * max_{Y>=0}[C_L^2 * Y^{3/2} - nu * Y^2]
    # hmm, max of f(Y) = C_L^2 * Y^{3/2} - nu * Y^2
    # f'(Y) = 1.5*C_L^2*Y^{1/2} - 2*nu*Y = 0 => Y^{1/2} = 3*C_L^2/(4*nu)
    # Y* = 9*C_L^4/(16*nu^2)
    # f(Y*) = C_L^2 * (9*C_L^4/(16*nu^2))^{3/2} - nu * (9*C_L^4/(16*nu^2))^2
    # = C_L^2 * 27*C_L^6/(64*nu^3) - nu * 81*C_L^8/(256*nu^4)
    # = 27*C_L^8/(64*nu^3) - 81*C_L^8/(256*nu^3)
    # = C_L^8/nu^3 * (108 - 81)/256 = 27*C_L^8/(256*nu^3)
    # So d/dt y <= 2 * y^{3/4} * 27*C_L^8/(256*nu^3) * ... wait I lost a y^{3/4}
    # No: d/dt y <= max_{Y>=0} [2*C_L^2 * y^{3/4} * Y^{3/2} - 2*nu*Y^2]
    # The optimization is over Y with y fixed.
    # Let g(Y) = 2*C_L^2 * y^{3/4} * Y^{3/2} - 2*nu*Y^2
    # g'(Y) = 3*C_L^2 * y^{3/4} * Y^{1/2} - 4*nu*Y = 0
    # Y^{1/2} = 3*C_L^2*y^{3/4} / (4*nu)
    # Y* = 9*C_L^4*y^{3/2}/(16*nu^2)
    # g(Y*) = 2*C_L^2*y^{3/4}*(9*C_L^4*y^{3/2}/(16*nu^2))^{3/2} - 2*nu*(9*C_L^4*y^{3/2}/(16*nu^2))^2
    # = 2*C_L^2*y^{3/4} * 27*C_L^6*y^{9/4}/(64*nu^3) - 2*nu * 81*C_L^8*y^3/(256*nu^4)
    # = 54*C_L^8*y^3/(64*nu^3) - 162*C_L^8*y^3/(256*nu^3)
    # = C_L^8*y^3/nu^3 * (54/64 - 162/256)
    # = C_L^8*y^3/nu^3 * (216/256 - 162/256)
    # = 54*C_L^8*y^3/(256*nu^3)
    # = 27*C_L^8*y^3/(128*nu^3)
    #
    # So: d/dt y <= (27*C_L^8/(128*nu^3)) * y^3
    # where y = ||omega||^2_{L^2}
    alpha_Lad = 27 * C_L**8 / (128 * solver.nu**3)

    RHS_Lad_Young = alpha_Lad * omega_L2_sq**3

    # For BKM: d/dt y = 2*VS - 2*nu*||nabla omega||^2
    # <= 2*C_CZ*y*omega_Linf*log_factor - 2*nu*||nabla omega||^2
    # The BKM bound doesn't involve ||nabla omega|| in the stretching term!
    # So: d/dt y <= 2*C_CZ*y*omega_Linf*log_factor
    # (the dissipation helps, we just drop it for an upper bound)
    # But log_factor involves ||nabla omega||/||omega||...
    # If we keep the log: d/dt y <= 2*C_CZ*y*omega_Linf*(1 + log(||nabla omega||/||omega||))
    # The ||nabla omega|| appears in the log, which makes Young's optimization different.
    #
    # Simple upper bound (drop dissipation and bound log):
    # Since ||nabla omega|| >= lambda_1 * ||omega|| (Poincare), log >= log(lambda_1)
    # But we can also use: ||nabla omega|| <= ||omega||^{1/3} * ||Delta omega||^{2/3} (interpolation)
    # For the simplest bound: assume log_factor is O(1) (bounded) during the flow
    # Then d/dt y <= 2*C_CZ*omega_Linf*log_factor * y
    # This is LINEAR in y when omega_Linf and log_factor are external.
    # If omega_Linf ~ y^{1/2} (which would happen if ||omega||_Linf ~ ||omega||_L2),
    # then d/dt y <= C * y^{3/2} which gives y ~ 1/(T-t)^2 (finite time blowup)
    # If omega_Linf ~ y^alpha with alpha < 1/2, we get better than Ladyzhenskaya.

    # For now, just record the raw BKM bound after dropping dissipation:
    RHS_BKM_Young = 2 * C_CZ * omega_L2_sq * omega_Linf * log_factor

    # === ||omega||_Linf / ||omega||_L2 ratio ===
    if omega_L2 > 1e-14:
        omega_ratio = omega_Linf / omega_L2
    else:
        omega_ratio = np.nan

    return {
        # Basic quantities
        'energy': energy,
        'enstrophy': enstrophy,
        'omega_L2': omega_L2,
        'omega_L2_sq': omega_L2_sq,
        'omega_Linf': omega_Linf,
        'grad_omega_L2': grad_omega_L2,
        'grad_omega_L2_sq': grad_omega_L2_sq,
        'S_Linf': S_Linf,
        'S_Linf_frob': S_Linf_frob,

        # Vortex stretching
        'vortex_stretching': float(vortex_stretching),
        'abs_vortex_stretching': float(abs(vortex_stretching)),

        # Bounds
        'VS_Lad': float(VS_Lad),
        'VS_BKM': float(VS_BKM),
        'VS_BKM_direct': float(VS_BKM_direct),

        # Slacks
        'slack_Lad': float(slack_Lad),
        'slack_BKM': float(slack_BKM),
        'slack_BKM_direct': float(slack_BKM_direct),
        'advantage': float(advantage),
        'C_CZ_empirical': float(C_CZ_empirical) if not np.isnan(C_CZ_empirical) else None,

        # ODE RHS
        'RHS_actual': float(RHS_actual),
        'RHS_Lad': float(RHS_Lad),
        'RHS_BKM': float(RHS_BKM),
        'RHS_Lad_Young': float(RHS_Lad_Young),
        'RHS_BKM_Young': float(RHS_BKM_Young),

        # Dissipation
        'dissipation': float(dissipation),

        # Critical ratio
        'omega_ratio': float(omega_ratio) if not np.isnan(omega_ratio) else None,
        'log_factor': float(log_factor),

        # For blow-up computation
        'alpha_Lad': float(alpha_Lad),
    }


def compute_blowup_times(diagnostics_list, times, nu):
    """Compute effective blow-up times from both ODE closures.

    Ladyzhenskaya: d/dt y <= alpha_Lad * y^3
    Solution: y(t) = y0 / sqrt(1 - 2*alpha_Lad*y0^2*t)
    Blow-up at: T = 1 / (2*alpha_Lad*y0^2)

    BKM: d/dt y <= 2*C_CZ*y*omega_Linf*log_factor
    If omega_Linf grows with y, we need to integrate numerically.
    """
    if not diagnostics_list:
        return {}

    d0 = diagnostics_list[0]
    y0 = d0['omega_L2_sq']  # ||omega||^2_{L^2} at t=0
    alpha_Lad = d0['alpha_Lad']

    # Ladyzhenskaya blow-up time
    if alpha_Lad > 0 and y0 > 0:
        T_Lad = 1.0 / (2 * alpha_Lad * y0**2)
    else:
        T_Lad = np.inf

    # BKM blow-up time: integrate numerically
    # d/dt y = 2*C_CZ * y * omega_Linf(y) * log_factor(y)
    # We need a model for how omega_Linf depends on y.
    # Fit: omega_Linf ~ C * y^alpha from the data
    omegas_L2_sq = np.array([d['omega_L2_sq'] for d in diagnostics_list])
    omegas_Linf = np.array([d['omega_Linf'] for d in diagnostics_list])
    log_factors = np.array([d['log_factor'] for d in diagnostics_list])

    # Filter out near-zero values
    mask = (omegas_L2_sq > 1e-14) & (omegas_Linf > 1e-14)
    if np.sum(mask) > 2:
        log_y = np.log(omegas_L2_sq[mask])
        log_oLinf = np.log(omegas_Linf[mask])

        # Linear fit: log(omega_Linf) = alpha * log(y) + log(C_fit)
        coeffs = np.polyfit(log_y, log_oLinf, 1)
        alpha_fit = coeffs[0]
        C_fit = np.exp(coeffs[1])

        # Mean log factor
        mean_log_factor = np.mean(log_factors[mask])
        max_log_factor = np.max(log_factors[mask])
    else:
        alpha_fit = 0.5  # default assumption
        C_fit = 1.0
        mean_log_factor = 1.0
        max_log_factor = 1.0

    # With omega_Linf ~ C_fit * y^alpha_fit:
    # d/dt y <= 2*C_CZ*C_fit*mean_log_factor * y^{1+alpha_fit}
    # If 1+alpha_fit > 1 (i.e., alpha_fit > 0):
    # Blow-up time: T = 1 / (2*C_CZ*C_fit*mean_log_factor*alpha_fit*y0^alpha_fit)
    beta = 2 * C_CZ * C_fit * mean_log_factor
    if alpha_fit > 0.01 and y0 > 0:
        T_BKM = 1.0 / (beta * alpha_fit * y0**alpha_fit)
    elif alpha_fit <= 0.01:
        # Nearly linear ODE: y(t) = y0 * exp(beta*t) — no finite-time blow-up!
        T_BKM = np.inf
    else:
        T_BKM = np.inf

    # Also integrate the BKM ODE numerically using actual data-fitted model
    T_BKM_numerical = integrate_bkm_ode(y0, alpha_fit, C_fit, mean_log_factor, nu)

    return {
        'T_Lad': float(T_Lad),
        'T_BKM': float(T_BKM),
        'T_BKM_numerical': float(T_BKM_numerical),
        'T_ratio': float(T_BKM / T_Lad) if T_Lad > 0 and T_Lad < np.inf else float('inf'),
        'alpha_fit': float(alpha_fit),
        'C_fit': float(C_fit),
        'mean_log_factor': float(mean_log_factor),
        'max_log_factor': float(max_log_factor),
        'alpha_Lad': float(alpha_Lad),
        'y0': float(y0),
    }


def integrate_bkm_ode(y0, alpha_fit, C_fit, mean_log_factor, nu):
    """Numerically integrate the BKM-based enstrophy ODE.

    d/dt y = 2*C_CZ*C_fit*log_factor * y^{1+alpha_fit}

    Returns blow-up time (or 1e10 if no blow-up within integration window).
    """
    dt = 1e-4
    t = 0.0
    y = y0
    T_max = 1e6  # max integration time

    beta = 2 * C_CZ * C_fit * mean_log_factor

    while t < T_max and y < 1e20:
        dy = beta * y**(1 + alpha_fit)
        if dy * dt > 0.1 * y:
            dt = 0.1 * y / max(dy, 1e-20)
        y += dy * dt
        t += dt
        if y > 1e20:
            return t
        if dt < 1e-15:
            return t  # effectively blown up

    return min(t, T_max)


def run_single_case(N, Re, ic_name, T_final=5.0, save_interval=0.05):
    """Run a single simulation and compute all BKM diagnostics."""
    nu = 1.0 / Re
    solver = NavierStokesSolver(N, nu, cfl=0.5)

    write_progress(f"Starting: N={N}, Re={Re}, IC={ic_name}")

    # Initialize
    if ic_name == 'TGV':
        ux_hat, uy_hat, uz_hat = taylor_green_ic(solver)
    elif ic_name == 'Gaussian':
        ux_hat, uy_hat, uz_hat = random_gaussian_ic(solver)
    elif ic_name == 'AntiParallel':
        ux_hat, uy_hat, uz_hat = antiparallel_tubes_ic(solver)
    else:
        raise ValueError(f"Unknown IC: {ic_name}")

    times = [0.0]
    diag_list = [compute_bkm_diagnostics(solver, ux_hat, uy_hat, uz_hat)]

    t = 0.0
    next_save = save_interval
    step = 0
    enstrophy_peaked = False
    peak_enstrophy = diag_list[0]['enstrophy']
    t_start = time_module.time()

    while t < T_final:
        dt = solver.compute_dt(ux_hat, uy_hat, uz_hat)
        dt = min(dt, T_final - t)

        if dt < 1e-12:
            write_progress(f"  dt too small at t={t:.4f}, stopping")
            break

        ux_hat, uy_hat, uz_hat = solver.rk4_step(ux_hat, uy_hat, uz_hat, dt)
        t += dt
        step += 1

        # Save at intervals
        if t >= next_save or t >= T_final - 1e-10:
            diag = compute_bkm_diagnostics(solver, ux_hat, uy_hat, uz_hat)
            times.append(t)
            diag_list.append(diag)
            next_save += save_interval

            # Check enstrophy dynamics
            if diag['enstrophy'] > peak_enstrophy:
                peak_enstrophy = diag['enstrophy']
                enstrophy_peaked = False
            elif diag['enstrophy'] < 0.5 * peak_enstrophy and not enstrophy_peaked:
                enstrophy_peaked = True
                # Continue a bit past peak to capture decay

            if step % 500 == 0:
                elapsed = time_module.time() - t_start
                write_progress(f"  t={t:.3f}/{T_final}, step={step}, "
                             f"enstrophy={diag['enstrophy']:.4e}, "
                             f"dt={dt:.2e}, wall={elapsed:.1f}s")

    elapsed = time_module.time() - t_start
    write_progress(f"Done: N={N}, Re={Re}, IC={ic_name}, "
                 f"steps={step}, t_final={t:.3f}, wall={elapsed:.1f}s")

    # Compute blow-up times
    blowup = compute_blowup_times(diag_list, times, nu)

    return {
        'N': N,
        'Re': Re,
        'ic_name': ic_name,
        'nu': nu,
        'times': times,
        'diagnostics': diag_list,
        'blowup': blowup,
        'n_steps': step,
        'wall_time': elapsed,
    }


def format_summary_table(all_results):
    """Format a summary table of all results."""
    header = (f"{'IC':<15} {'Re':<6} {'N':<4} {'Min Slack_Lad':<14} {'Min Slack_BKM':<14} "
              f"{'Advantage':<12} {'T_Lad':<12} {'T_BKM':<12} {'T_ratio':<10} "
              f"{'alpha_fit':<10} {'omega_ratio_max':<16}")
    lines = [header, '=' * len(header)]

    for r in all_results:
        diags = r['diagnostics']
        # Skip t=0 where stretching might be zero
        valid_diags = [d for d in diags[1:] if d['abs_vortex_stretching'] > 1e-20]
        if not valid_diags:
            valid_diags = diags

        min_slack_Lad = min(d['slack_Lad'] for d in valid_diags if d['slack_Lad'] < 1e10)
        min_slack_BKM = min(d['slack_BKM'] for d in valid_diags if d['slack_BKM'] < 1e10)
        max_advantage = max(d['advantage'] for d in valid_diags
                           if not np.isinf(d['advantage']) and not np.isnan(d['advantage']))
        min_advantage = min(d['advantage'] for d in valid_diags
                           if not np.isinf(d['advantage']) and not np.isnan(d['advantage']))

        ratios = [d['omega_ratio'] for d in valid_diags if d['omega_ratio'] is not None]
        max_omega_ratio = max(ratios) if ratios else float('nan')

        bl = r['blowup']
        T_Lad = bl['T_Lad']
        T_BKM = bl['T_BKM']
        T_ratio = bl['T_ratio']
        alpha = bl['alpha_fit']

        lines.append(
            f"{r['ic_name']:<15} {r['Re']:<6} {r['N']:<4} "
            f"{min_slack_Lad:<14.2f} {min_slack_BKM:<14.2f} "
            f"{min_advantage:<12.2f} {T_Lad:<12.4e} {T_BKM:<12.4e} {T_ratio:<10.2f} "
            f"{alpha:<10.4f} {max_omega_ratio:<16.4f}"
        )

    return '\n'.join(lines)


def format_time_series(result):
    """Format time series for one run."""
    lines = []
    lines.append(f"\n=== Time Series: {result['ic_name']} Re={result['Re']} N={result['N']} ===")
    header = (f"{'t':<8} {'enstrophy':<12} {'|VS_actual|':<12} {'VS_Lad':<12} {'VS_BKM':<12} "
              f"{'slack_Lad':<10} {'slack_BKM':<10} {'advantage':<10} "
              f"{'omega_ratio':<12} {'log_factor':<10}")
    lines.append(header)
    lines.append('-' * len(header))

    for i, (t, d) in enumerate(zip(result['times'], result['diagnostics'])):
        if i % max(1, len(result['times']) // 20) != 0 and i != len(result['times'])-1:
            continue  # Show ~20 rows

        sl = min(d['slack_Lad'], 99999)
        sb = min(d['slack_BKM'], 99999)
        adv = min(d['advantage'], 99999) if not np.isnan(d['advantage']) else float('nan')
        orat = d['omega_ratio'] if d['omega_ratio'] is not None else float('nan')

        lines.append(
            f"{t:<8.3f} {d['enstrophy']:<12.4e} {d['abs_vortex_stretching']:<12.4e} "
            f"{d['VS_Lad']:<12.4e} {d['VS_BKM']:<12.4e} "
            f"{sl:<10.1f} {sb:<10.1f} {adv:<10.1f} "
            f"{orat:<12.4f} {d['log_factor']:<10.4f}"
        )

    return '\n'.join(lines)


def youngs_optimization(result):
    """Young's inequality optimization for BKM closure.

    For the BKM-based bound:
    |VS| <= C_CZ * ||omega||^2 * ||omega||_Linf * (1 + log^+(||nabla omega||/||omega||))

    The log term involves ||nabla omega||. When applying Young's to separate
    the stretching from dissipation, we can use:

    Strategy A: Drop dissipation entirely (simplest)
      d/dt y <= 2*C_CZ*y*omega_Linf*log_factor

    Strategy B: Use the fact that log(||nabla omega||/||omega||) is bounded by
      ||nabla omega||^epsilon for any epsilon > 0, then absorb via Young's.

    Strategy C: Optimize epsilon at each timestep.
    """
    lines = []
    lines.append(f"\n=== Young's Optimization: {result['ic_name']} Re={result['Re']} ===")

    nu = result['nu']
    for i, (t, d) in enumerate(zip(result['times'], result['diagnostics'])):
        if i % max(1, len(result['times']) // 10) != 0:
            continue

        omega_L2 = d['omega_L2']
        omega_Linf = d['omega_Linf']
        grad_omega_L2 = d['grad_omega_L2']
        omega_L2_sq = d['omega_L2_sq']

        # Strategy A: drop dissipation
        RHS_A = 2 * C_CZ * omega_L2_sq * omega_Linf * d['log_factor']

        # Strategy B: for each epsilon in (0, 2), bound
        # log(Y/X) <= Y^eps / (eps * X^eps)  (for Y >= X >= 0)
        # Then VS <= C_CZ * X^2 * omega_Linf * (1 + Y^eps/(eps*X^eps))
        # = C_CZ * omega_Linf * X^2 + C_CZ * omega_Linf * X^{2-eps} * Y^eps / eps
        # Apply Young to the second term to absorb Y^2 (dissipation):
        # C_CZ*omega_Linf*X^{2-eps}*Y^eps/eps <= nu*Y^2 + f(X, omega_Linf)
        # Young: a*b <= nu*b^{2/eps} + C(nu)*a^{2/(2-eps)} when 1/(2/eps) + 1/(2/(2-eps)) = 1
        # i.e., eps/2 + (2-eps)/2 = 1 ✓
        # So: C_CZ*omega_Linf*X^{2-eps}*Y^eps/eps <= nu*Y^2 + C(nu,eps)*[C_CZ*omega_Linf*X^{2-eps}/eps]^{2/(2-eps)}

        best_eps = 0.5
        best_RHS = np.inf

        if omega_L2 > 1e-14 and grad_omega_L2 > 1e-14 and omega_Linf > 1e-14:
            for eps_try in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2, 1.5]:
                if eps_try >= 2.0:
                    continue
                # The log-bounded term after Young's:
                # Coefficient A = C_CZ * omega_Linf / eps_try
                # RHS bound = C_CZ*omega_Linf*X^2 + C(nu,eps)*A^{2/(2-eps)} * X^2
                # where C(nu,eps) = (1 - eps/2) * (eps/(2*nu))^{eps/(2-eps)}
                p = 2.0 / (2.0 - eps_try)  # conjugate exponent for Young
                q = 2.0 / eps_try

                # Young: a*b <= a^p/p + b^q/q with a = (C_CZ*oLinf/eps*X^{2-eps}), b = Y^eps
                # and we want nu*Y^2 on the b side, so b = Y^eps, b^q = Y^2, q = 2/eps ✓
                # a^p/p = (C_CZ*oLinf/eps)^p * X^{(2-eps)*p} / p
                # = (C_CZ*oLinf/eps)^{2/(2-eps)} * X^2 / (2/(2-eps))
                a_val = C_CZ * omega_Linf * omega_L2**(2-eps_try) / eps_try
                rhs_young = a_val**p / p  # this absorbs Y, leaving function of X

                # Total: C_CZ*omega_Linf*X^2 (from the "1" in 1+log) + rhs_young
                # But rhs_young already accounts for the dissipation absorption
                total_rhs = 2 * (C_CZ * omega_Linf * omega_L2_sq + rhs_young)

                if total_rhs < best_RHS:
                    best_RHS = total_rhs
                    best_eps = eps_try

        RHS_B = best_RHS if best_RHS < np.inf else RHS_A

        lines.append(f"  t={t:.3f}: RHS_A={RHS_A:.4e}, RHS_B(eps={best_eps})={RHS_B:.4e}, "
                    f"RHS_Lad_Young={d['RHS_Lad_Young']:.4e}")

    return '\n'.join(lines)


def main():
    """Run the full BKM comparison study."""
    write_progress("=" * 60)
    write_progress("BKM Enstrophy Bypass — Computational Validation")
    write_progress("=" * 60)

    # Configuration
    reynolds_numbers = [100, 500, 1000, 5000]
    ics = ['TGV', 'Gaussian', 'AntiParallel']
    N_primary = 64
    T_final = 5.0

    all_results = []

    # Run all cases at primary resolution
    for ic_name in ics:
        for Re in reynolds_numbers:
            # For high Re on N=64, may need shorter runs or reduced Re
            # N=64 can resolve Re up to ~1000 cleanly
            T_run = T_final
            if Re >= 5000 and N_primary == 64:
                T_run = 2.0  # shorter run for underresolved case
                write_progress(f"WARNING: Re={Re} on N={N_primary} likely underresolved, running to T={T_run}")

            try:
                result = run_single_case(N_primary, Re, ic_name, T_final=T_run)
                all_results.append(result)
            except Exception as e:
                write_progress(f"FAILED: N={N_primary}, Re={Re}, IC={ic_name}: {e}")
                import traceback
                traceback.print_exc()

    # Convergence check: TGV Re=1000 at N=128
    write_progress("\n=== Convergence Check: TGV Re=1000 N=128 ===")
    try:
        result_128 = run_single_case(128, 1000, 'TGV', T_final=3.0)
        all_results.append(result_128)
    except Exception as e:
        write_progress(f"FAILED: N=128 convergence check: {e}")
        import traceback
        traceback.print_exc()

    # === Output ===
    write_progress("\n" + "=" * 60)
    write_progress("RESULTS SUMMARY")
    write_progress("=" * 60)

    # Summary table
    summary = format_summary_table(all_results)
    print(summary)
    write_progress(summary)

    # Time series for key cases
    for r in all_results:
        ts = format_time_series(r)
        print(ts)

    # Young's optimization
    for r in all_results:
        if r['ic_name'] == 'TGV' and r['Re'] in [100, 1000]:
            yo = youngs_optimization(r)
            print(yo)

    # Save all results as JSON
    def sanitize(obj):
        """Make numpy types JSON-serializable."""
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize(v) for v in obj]
        elif isinstance(obj, (np.floating, np.float64)):
            v = float(obj)
            if np.isnan(v) or np.isinf(v):
                return str(v)
            return v
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return sanitize(obj.tolist())
        elif isinstance(obj, float):
            if np.isnan(obj) or np.isinf(obj):
                return str(obj)
            return obj
        return obj

    results_file = os.path.join(RESULTS_DIR, 'bkm_comparison.json')
    with open(results_file, 'w') as f:
        json.dump(sanitize(all_results), f, indent=2)
    write_progress(f"\nResults saved to {results_file}")

    # Generate focused output for report
    report_file = os.path.join(RESULTS_DIR, 'report_data.txt')
    with open(report_file, 'w') as f:
        f.write("BKM vs Ladyzhenskaya Enstrophy Bound Comparison\n")
        f.write("=" * 60 + "\n\n")
        f.write(summary + "\n\n")

        for r in all_results:
            f.write(format_time_series(r) + "\n\n")
            if r['ic_name'] == 'TGV':
                f.write(youngs_optimization(r) + "\n\n")

            # Blow-up analysis
            bl = r['blowup']
            f.write(f"\nBlow-up Analysis: {r['ic_name']} Re={r['Re']}:\n")
            f.write(f"  T_Lad = {bl['T_Lad']:.6e}\n")
            f.write(f"  T_BKM (analytical) = {bl['T_BKM']:.6e}\n")
            f.write(f"  T_BKM (numerical) = {bl['T_BKM_numerical']:.6e}\n")
            f.write(f"  T_BKM / T_Lad = {bl['T_ratio']:.2f}\n")
            f.write(f"  alpha_fit (omega_Linf ~ y^alpha) = {bl['alpha_fit']:.4f}\n")
            f.write(f"  C_fit = {bl['C_fit']:.4f}\n")
            f.write(f"  mean log_factor = {bl['mean_log_factor']:.4f}\n\n")

    write_progress(f"Report data saved to {report_file}")
    write_progress("DONE")

    return all_results


if __name__ == '__main__':
    main()
