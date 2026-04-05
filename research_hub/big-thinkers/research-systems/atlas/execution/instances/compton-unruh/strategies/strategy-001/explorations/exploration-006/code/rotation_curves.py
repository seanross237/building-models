"""
Galaxy Rotation Curve Fits: NGC 3198 and NGC 2403

Compare Newton, MOND, and ratio model (T_U/T_dS) for exponential disk galaxies.

Interpolation function: mu(x) = x/sqrt(1+x^2)  [the "nu" or "ν" function]
This is the same as T_U/T_dS with x = a/a0, a0 = cH0

Models compared:
1. Newton (no dark matter)
2. MOND: mu(g_N/a0_MOND) * g = g_N, a0_MOND = 1.2e-10 m/s^2
3. Ratio model (a0 = cH0 = 6.8e-10 m/s^2, factor 5.7x too large)
4. Ratio model (a0 = cH0/6 = 1.13e-10 m/s^2, Verlinde factor)
5. Best-fit a0 from chi-squared minimization
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import iv as BesselI, kv as BesselK
from scipy.optimize import brentq, minimize_scalar
from scipy.interpolate import interp1d

# ============================================================
# CONSTANTS
# ============================================================
G = 4.302e-3       # pc * (km/s)^2 / M_sun — useful for rotation curves
hbar = 1.0546e-34  # J*s
k_B = 1.3806e-23   # J/K
c_ms = 2.998e8     # m/s
H0 = 2.268e-18     # s^-1 (70 km/s/Mpc)

# Convert to kpc units
kpc_to_m = 3.086e19   # m/kpc
M_sun = 1.989e30      # kg

# a0 values in m/s^2
a0_MOND = 1.2e-10            # observed MOND parameter
a0_cH0 = c_ms * H0           # = 6.8e-10 m/s^2 (ratio model, no correction)
a0_Verlinde = a0_cH0 / 6.0   # = 1.13e-10 m/s^2 (Verlinde factor)

print("=" * 60)
print("GALAXY ROTATION CURVE FITS")
print("=" * 60)
print(f"G = {G:.4e} pc*(km/s)^2/M_sun")
print(f"a0_MOND = {a0_MOND:.3e} m/s^2")
print(f"a0_cH0 = {a0_cH0:.3e} m/s^2")
print(f"a0_Verlinde = {a0_Verlinde:.3e} m/s^2")
print()

# ============================================================
# EXPONENTIAL DISK ROTATION VELOCITY (Freeman 1970)
# ============================================================
def v_disk_newtonian(R_kpc, M_disk_Msun, R_d_kpc):
    """
    Circular velocity for an infinitely thin exponential disk.

    v^2(R) = 4*pi*G*Sigma_0*R_d * y^2 * [I_0(y)*K_0(y) - I_1(y)*K_1(y)]
    where y = R/(2*R_d), Sigma_0 = M_disk/(2*pi*R_d^2)

    Parameters:
        R_kpc: array, radii in kpc
        M_disk_Msun: total disk mass in solar masses
        R_d_kpc: disk scale length in kpc

    Returns:
        v_N: Newtonian circular velocity in km/s
    """
    y = R_kpc / (2.0 * R_d_kpc)
    # Avoid y=0
    y = np.maximum(y, 1e-6)

    # Sigma_0 in M_sun/kpc^2
    Sigma_0 = M_disk_Msun / (2 * np.pi * R_d_kpc**2)

    # Freeman's formula: v^2 = 4*pi*G*Sigma_0*R_d * y^2 * [I0*K0 - I1*K1]
    # In units where G is in pc*(km/s)^2/M_sun:
    # Convert to kpc: G [kpc*(km/s)^2/M_sun] = G_pc * 1000
    G_kpc = G * 1e-3  # kpc*(km/s)^2/M_sun

    # Bessel functions
    I0 = BesselI(0, y)
    K0 = BesselK(0, y)
    I1 = BesselI(1, y)
    K1 = BesselK(1, y)

    v2 = 4 * np.pi * G_kpc * Sigma_0 * R_d_kpc * y**2 * (I0*K0 - I1*K1)
    v2 = np.maximum(v2, 0)
    return np.sqrt(v2)

def g_N_disk(R_kpc, M_disk_Msun, R_d_kpc):
    """
    Newtonian gravitational acceleration from exponential disk (pointing inward).
    g_N = v_N^2 / R
    Returns g_N in m/s^2
    """
    v_N = v_disk_newtonian(R_kpc, M_disk_Msun, R_d_kpc)  # km/s
    R_m = R_kpc * kpc_to_m  # m
    v_ms = v_N * 1e3  # m/s
    return v_ms**2 / R_m  # m/s^2

def solve_mond(g_N_arr, a0):
    """
    Solve mu(g/a0)*g = g_N for g, where mu(x) = x/sqrt(1+x^2)

    This gives: g^2 / sqrt(g^2 + a0^2) = g_N
    => g^4 = g_N^2 * (g^2 + a0^2)
    => g^4 - g_N^2 * g^2 - g_N^2 * a0^2 = 0

    Quadratic in g^2:
    g^2 = (g_N^2/2) + sqrt(g_N^4/4 + g_N^2*a0^2)
        = (g_N^2/2) * (1 + sqrt(1 + 4*a0^2/g_N^2))
    """
    g2 = (g_N_arr**2 / 2) * (1 + np.sqrt(1 + 4*a0**2 / g_N_arr**2))
    return np.sqrt(g2)

def v_mond(R_kpc, M_disk_Msun, R_d_kpc, a0):
    """
    MOND circular velocity with mu(x) = x/sqrt(1+x^2)
    Returns v in km/s
    """
    g_N = g_N_disk(R_kpc, M_disk_Msun, R_d_kpc)  # m/s^2
    g = solve_mond(g_N, a0)
    R_m = R_kpc * kpc_to_m
    v2_ms = g * R_m  # m^2/s^2
    return np.sqrt(v2_ms) * 1e-3  # km/s

def v_ratio_model(R_kpc, M_disk_Msun, R_d_kpc, a0):
    """
    Ratio model: SAME as MOND with mu = x/sqrt(1+x^2)
    The ratio T_U/T_dS IS this mu function.
    So v_ratio = v_mond (same mu function, possibly different a0).
    """
    return v_mond(R_kpc, M_disk_Msun, R_d_kpc, a0)

# ============================================================
# NGC 3198 ROTATION CURVE
# ============================================================
print("=" * 60)
print("NGC 3198")
print("=" * 60)

# Galaxy parameters
M_3198 = 2.0e10   # M_sun (disk mass)
Rd_3198 = 3.5     # kpc (disk scale length)

# Observed rotation curve data (tabulated from van Albada+1985, Begeman 1989)
# Approximate values at key radii
R_obs_3198 = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32])  # kpc
v_obs_3198 = np.array([100, 130, 145, 148, 150, 150, 150, 150, 150, 150, 150, 148, 150])  # km/s
v_err_3198 = np.array([10, 8, 7, 7, 6, 6, 6, 6, 6, 6, 7, 8, 10])  # km/s (approximate)

R_model = np.linspace(0.5, 35, 200)

v_N_3198 = v_disk_newtonian(R_model, M_3198, Rd_3198)
v_MOND_3198 = v_mond(R_model, M_3198, Rd_3198, a0_MOND)
v_ratio_cH0_3198 = v_ratio_model(R_model, M_3198, Rd_3198, a0_cH0)
v_ratio_Verl_3198 = v_ratio_model(R_model, M_3198, Rd_3198, a0_Verlinde)

# Asymptotic flat velocity prediction (deep MOND: v^4 = G*M*a0)
def v_flat_MOND(M, a0):
    """Deep MOND asymptotic: v^4 = G*M*a0 (BTFR)"""
    G_SI = 6.674e-11  # m^3/kg/s^2
    M_kg = M * M_sun
    v4 = G_SI * M_kg * a0
    return v4**0.25 * 1e-3  # km/s

v_flat_pred_MOND = v_flat_MOND(M_3198, a0_MOND)
v_flat_pred_cH0 = v_flat_MOND(M_3198, a0_cH0)
v_flat_pred_Verl = v_flat_MOND(M_3198, a0_Verlinde)

print(f"Disk mass: {M_3198:.1e} M_sun, R_d = {Rd_3198} kpc")
print(f"Observed flat velocity: ~150 km/s at 30 kpc")
print()
print(f"Deep MOND asymptotic v_flat predictions:")
print(f"  MOND (a0 = 1.2e-10):   v_flat = {v_flat_pred_MOND:.1f} km/s")
print(f"  cH0 (a0 = 6.8e-10):    v_flat = {v_flat_pred_cH0:.1f} km/s")
print(f"  Verlinde (a0=cH0/6):   v_flat = {v_flat_pred_Verl:.1f} km/s")
print()
print("Model velocities at R = 30 kpc:")
print(f"  Newton:   {np.interp(30, R_model, v_N_3198):.1f} km/s")
print(f"  MOND:     {np.interp(30, R_model, v_MOND_3198):.1f} km/s")
print(f"  cH0:      {np.interp(30, R_model, v_ratio_cH0_3198):.1f} km/s")
print(f"  Verlinde: {np.interp(30, R_model, v_ratio_Verl_3198):.1f} km/s")
print(f"  Observed: ~150 km/s")
print()

# Compute chi-squared for each model
def chi2_model(R_obs, v_obs, v_err, M, Rd, a0):
    """Chi-squared for a given a0"""
    v_pred = v_mond(R_obs, M, Rd, a0)
    return np.sum(((v_obs - v_pred) / v_err)**2)

chi2_MOND_3198 = chi2_model(R_obs_3198, v_obs_3198, v_err_3198, M_3198, Rd_3198, a0_MOND)
chi2_cH0_3198 = chi2_model(R_obs_3198, v_obs_3198, v_err_3198, M_3198, Rd_3198, a0_cH0)
chi2_Verl_3198 = chi2_model(R_obs_3198, v_obs_3198, v_err_3198, M_3198, Rd_3198, a0_Verlinde)

print(f"Chi-squared / dof (dof = {len(R_obs_3198)}):")
print(f"  MOND (a0=1.2e-10): chi2 = {chi2_MOND_3198:.1f}  (chi2/dof = {chi2_MOND_3198/len(R_obs_3198):.2f})")
print(f"  cH0 (a0=6.8e-10):  chi2 = {chi2_cH0_3198:.1f}  (chi2/dof = {chi2_cH0_3198/len(R_obs_3198):.2f})")
print(f"  Verlinde (cH0/6):  chi2 = {chi2_Verl_3198:.1f}  (chi2/dof = {chi2_Verl_3198/len(R_obs_3198):.2f})")
print()

# Best-fit a0
def neg_chi2_3198(log_a0):
    a0 = 10**log_a0
    return chi2_model(R_obs_3198, v_obs_3198, v_err_3198, M_3198, Rd_3198, a0)

result_3198 = minimize_scalar(neg_chi2_3198, bounds=(-11, -8), method='bounded')
a0_best_3198 = 10**result_3198.x
chi2_best_3198 = result_3198.fun

print(f"Best-fit a0 for NGC 3198: {a0_best_3198:.3e} m/s^2")
print(f"Best-fit chi2: {chi2_best_3198:.1f}  (chi2/dof = {chi2_best_3198/len(R_obs_3198):.2f})")
print(f"Best-fit a0 / a0_MOND = {a0_best_3198/a0_MOND:.2f}")
print(f"Best-fit a0 / a0_Verlinde = {a0_best_3198/a0_Verlinde:.2f}")
print()

v_best_3198 = v_mond(R_model, M_3198, Rd_3198, a0_best_3198)

# Acceleration profile
g_N_arr_3198 = g_N_disk(R_model, M_3198, Rd_3198)
mond_regime_mask_3198 = g_N_arr_3198 < a0_MOND
MOND_regime_frac_3198 = np.mean(mond_regime_mask_3198)
print(f"Fraction of model range (0.5-35 kpc) in MOND regime (g_N < a0_MOND): {100*MOND_regime_frac_3198:.0f}%")

# Find crossover radius
try:
    def g_minus_a0_3198(R):
        return g_N_disk(np.array([R]), M_3198, Rd_3198)[0] - a0_MOND
    R_cross_3198 = brentq(g_minus_a0_3198, 0.1, 35)
    print(f"Crossover radius (g_N = a0_MOND): R_cross = {R_cross_3198:.1f} kpc")
except Exception as e:
    R_cross_3198 = None
    print(f"Could not find crossover radius: {e}")
print()

# ============================================================
# NGC 2403 ROTATION CURVE
# ============================================================
print("=" * 60)
print("NGC 2403")
print("=" * 60)

# Galaxy parameters
M_2403 = 2.5e9    # M_sun (disk mass)
Rd_2403 = 2.0     # kpc

# Observed rotation curve (de Blok & Bosma 2002, approximate)
R_obs_2403 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15])  # kpc
v_obs_2403 = np.array([55, 90, 110, 120, 125, 128, 130, 131, 132, 132, 133, 133])  # km/s
v_err_2403 = np.array([8, 7, 6, 6, 5, 5, 5, 5, 5, 5, 6, 7])  # km/s

R_model_2403 = np.linspace(0.3, 18, 200)

v_N_2403 = v_disk_newtonian(R_model_2403, M_2403, Rd_2403)
v_MOND_2403 = v_mond(R_model_2403, M_2403, Rd_2403, a0_MOND)
v_ratio_cH0_2403 = v_ratio_model(R_model_2403, M_2403, Rd_2403, a0_cH0)
v_ratio_Verl_2403 = v_ratio_model(R_model_2403, M_2403, Rd_2403, a0_Verlinde)

v_flat_pred_MOND_2403 = v_flat_MOND(M_2403, a0_MOND)
v_flat_pred_cH0_2403 = v_flat_MOND(M_2403, a0_cH0)
v_flat_pred_Verl_2403 = v_flat_MOND(M_2403, a0_Verlinde)

print(f"Disk mass: {M_2403:.1e} M_sun, R_d = {Rd_2403} kpc")
print(f"Observed flat velocity: ~130 km/s at 15 kpc")
print()
print(f"Deep MOND asymptotic v_flat predictions:")
print(f"  MOND (a0 = 1.2e-10):   v_flat = {v_flat_pred_MOND_2403:.1f} km/s")
print(f"  cH0 (a0 = 6.8e-10):    v_flat = {v_flat_pred_cH0_2403:.1f} km/s")
print(f"  Verlinde (a0=cH0/6):   v_flat = {v_flat_pred_Verl_2403:.1f} km/s")
print()
print("Model velocities at R = 15 kpc:")
print(f"  Newton:   {np.interp(15, R_model_2403, v_N_2403):.1f} km/s")
print(f"  MOND:     {np.interp(15, R_model_2403, v_MOND_2403):.1f} km/s")
print(f"  cH0:      {np.interp(15, R_model_2403, v_ratio_cH0_2403):.1f} km/s")
print(f"  Verlinde: {np.interp(15, R_model_2403, v_ratio_Verl_2403):.1f} km/s")
print(f"  Observed: ~130 km/s")
print()

chi2_MOND_2403 = chi2_model(R_obs_2403, v_obs_2403, v_err_2403, M_2403, Rd_2403, a0_MOND)
chi2_cH0_2403 = chi2_model(R_obs_2403, v_obs_2403, v_err_2403, M_2403, Rd_2403, a0_cH0)
chi2_Verl_2403 = chi2_model(R_obs_2403, v_obs_2403, v_err_2403, M_2403, Rd_2403, a0_Verlinde)

print(f"Chi-squared / dof (dof = {len(R_obs_2403)}):")
print(f"  MOND (a0=1.2e-10): chi2 = {chi2_MOND_2403:.1f}  (chi2/dof = {chi2_MOND_2403/len(R_obs_2403):.2f})")
print(f"  cH0 (a0=6.8e-10):  chi2 = {chi2_cH0_2403:.1f}  (chi2/dof = {chi2_cH0_2403/len(R_obs_2403):.2f})")
print(f"  Verlinde (cH0/6):  chi2 = {chi2_Verl_2403:.1f}  (chi2/dof = {chi2_Verl_2403/len(R_obs_2403):.2f})")
print()

def neg_chi2_2403(log_a0):
    a0 = 10**log_a0
    return chi2_model(R_obs_2403, v_obs_2403, v_err_2403, M_2403, Rd_2403, a0)

result_2403 = minimize_scalar(neg_chi2_2403, bounds=(-11, -8), method='bounded')
a0_best_2403 = 10**result_2403.x
chi2_best_2403 = result_2403.fun

print(f"Best-fit a0 for NGC 2403: {a0_best_2403:.3e} m/s^2")
print(f"Best-fit chi2: {chi2_best_2403:.1f}  (chi2/dof = {chi2_best_2403/len(R_obs_2403):.2f})")
print(f"Best-fit a0 / a0_MOND = {a0_best_2403/a0_MOND:.2f}")
print(f"Best-fit a0 / a0_Verlinde = {a0_best_2403/a0_Verlinde:.2f}")
print()

v_best_2403 = v_mond(R_model_2403, M_2403, Rd_2403, a0_best_2403)

g_N_arr_2403 = g_N_disk(R_model_2403, M_2403, Rd_2403)
mond_regime_mask_2403 = g_N_arr_2403 < a0_MOND
MOND_regime_frac_2403 = np.mean(mond_regime_mask_2403)
print(f"Fraction of model range (0.3-18 kpc) in MOND regime (g_N < a0_MOND): {100*MOND_regime_frac_2403:.0f}%")

try:
    def g_minus_a0_2403(R):
        return g_N_disk(np.array([R]), M_2403, Rd_2403)[0] - a0_MOND
    R_cross_2403 = brentq(g_minus_a0_2403, 0.1, 18)
    print(f"Crossover radius (g_N = a0_MOND): R_cross = {R_cross_2403:.1f} kpc")
except Exception as e:
    R_cross_2403 = None
    print(f"Could not find crossover: {e}")
print()

# ============================================================
# BEST-FIT a0 vs. MOND/VERLINDE
# ============================================================
print("=" * 60)
print("BEST-FIT a0 COMPARISON")
print("=" * 60)
print(f"  NGC 3198 best-fit a0 = {a0_best_3198:.3e} m/s^2")
print(f"  NGC 2403 best-fit a0 = {a0_best_2403:.3e} m/s^2")
print(f"  MOND a0 = {a0_MOND:.3e} m/s^2")
print(f"  Verlinde (cH0/6) = {a0_Verlinde:.3e} m/s^2")
print(f"  cH0 = {a0_cH0:.3e} m/s^2")
print()
print(f"  NGC 3198: best_a0/a0_MOND = {a0_best_3198/a0_MOND:.3f}")
print(f"  NGC 2403: best_a0/a0_MOND = {a0_best_2403/a0_MOND:.3f}")
print()

# Scan chi2 vs a0 for both galaxies
log_a0_arr = np.linspace(-11, -8, 200)
chi2_scan_3198 = np.array([chi2_model(R_obs_3198, v_obs_3198, v_err_3198, M_3198, Rd_3198, 10**la) for la in log_a0_arr])
chi2_scan_2403 = np.array([chi2_model(R_obs_2403, v_obs_2403, v_err_2403, M_2403, Rd_2403, 10**la) for la in log_a0_arr])

# ============================================================
# PLOTS
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Galaxy Rotation Curves: Newton / MOND / Ratio Model', fontsize=14, fontweight='bold')

# ---- NGC 3198 rotation curve ----
ax = axes[0, 0]
ax.errorbar(R_obs_3198, v_obs_3198, yerr=v_err_3198, fmt='ko', markersize=5,
            capsize=3, label='Observed (NGC 3198)', zorder=10)
ax.plot(R_model, v_N_3198, 'gray', lw=1.5, ls='--', label='Newton (baryons only)')
ax.plot(R_model, v_MOND_3198, 'b-', lw=2, label=f'MOND (a₀=1.2×10⁻¹⁰)')
ax.plot(R_model, v_ratio_Verl_3198, 'g-', lw=2, label=f'Ratio (cH₀/6=1.1×10⁻¹⁰)')
ax.plot(R_model, v_ratio_cH0_3198, 'r-', lw=1.5, ls=':', label=f'Ratio (cH₀=6.8×10⁻¹⁰)')
ax.plot(R_model, v_best_3198, 'm-', lw=2, ls='-.', label=f'Best fit (a₀={a0_best_3198:.1e})')
ax.axhline(150, color='k', ls=':', alpha=0.3)
if R_cross_3198:
    ax.axvline(R_cross_3198, color='orange', ls='--', alpha=0.7, label=f'R_cross={R_cross_3198:.1f} kpc')
ax.set_xlabel('R [kpc]')
ax.set_ylabel('v [km/s]')
ax.set_title('NGC 3198: Rotation Curves')
ax.legend(fontsize=7)
ax.set_xlim([0, 35])
ax.set_ylim([0, 220])
ax.grid(True, alpha=0.3)
ax.text(0.05, 0.9, f'χ²/dof (MOND)={chi2_MOND_3198/len(R_obs_3198):.1f}',
        transform=ax.transAxes, fontsize=8, color='blue')
ax.text(0.05, 0.83, f'χ²/dof (Verl)={chi2_Verl_3198/len(R_obs_3198):.1f}',
        transform=ax.transAxes, fontsize=8, color='green')
ax.text(0.05, 0.76, f'χ²/dof (cH₀)={chi2_cH0_3198/len(R_obs_3198):.1f}',
        transform=ax.transAxes, fontsize=8, color='red')

# ---- NGC 3198 acceleration profile ----
ax = axes[0, 1]
ax.semilogy(R_model, g_N_arr_3198, 'k-', lw=2, label='g_N (Newton)')
ax.axhline(a0_MOND, color='b', ls='--', lw=1.5, label=f'a₀_MOND={a0_MOND:.1e}')
ax.axhline(a0_Verlinde, color='g', ls=':', lw=1.5, label=f'a₀_Verl={a0_Verlinde:.1e}')
ax.axhline(a0_cH0, color='r', ls=':', lw=1.5, label=f'cH₀={a0_cH0:.1e}')
if R_cross_3198:
    ax.axvline(R_cross_3198, color='orange', ls='--', alpha=0.7)
ax.set_xlabel('R [kpc]')
ax.set_ylabel('g_N [m/s²]')
ax.set_title('NGC 3198: Acceleration Profile')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 35])

# ---- chi2 scan for NGC 3198 ----
ax = axes[0, 2]
a0_scan = 10**log_a0_arr
ax.loglog(a0_scan / a0_MOND, chi2_scan_3198 / len(R_obs_3198), 'k-', lw=2)
ax.axvline(1.0, color='b', ls='--', label='MOND a₀')
ax.axvline(a0_Verlinde/a0_MOND, color='g', ls=':', label='Verlinde (cH₀/6)')
ax.axvline(a0_cH0/a0_MOND, color='r', ls=':', label='cH₀')
ax.axvline(a0_best_3198/a0_MOND, color='m', ls='-.', label=f'Best fit')
ax.set_xlabel('a₀ / a₀_MOND')
ax.set_ylabel('χ²/dof')
ax.set_title('NGC 3198: χ² vs a₀')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim([0.01, 10])

# ---- NGC 2403 rotation curve ----
ax = axes[1, 0]
ax.errorbar(R_obs_2403, v_obs_2403, yerr=v_err_2403, fmt='ko', markersize=5,
            capsize=3, label='Observed (NGC 2403)', zorder=10)
ax.plot(R_model_2403, v_N_2403, 'gray', lw=1.5, ls='--', label='Newton (baryons only)')
ax.plot(R_model_2403, v_MOND_2403, 'b-', lw=2, label=f'MOND (a₀=1.2×10⁻¹⁰)')
ax.plot(R_model_2403, v_ratio_Verl_2403, 'g-', lw=2, label=f'Ratio (cH₀/6=1.1×10⁻¹⁰)')
ax.plot(R_model_2403, v_ratio_cH0_2403, 'r-', lw=1.5, ls=':', label=f'Ratio (cH₀=6.8×10⁻¹⁰)')
ax.plot(R_model_2403, v_best_2403, 'm-', lw=2, ls='-.', label=f'Best fit (a₀={a0_best_2403:.1e})')
ax.axhline(130, color='k', ls=':', alpha=0.3)
if R_cross_2403:
    ax.axvline(R_cross_2403, color='orange', ls='--', alpha=0.7, label=f'R_cross={R_cross_2403:.1f} kpc')
ax.set_xlabel('R [kpc]')
ax.set_ylabel('v [km/s]')
ax.set_title('NGC 2403: Rotation Curves')
ax.legend(fontsize=7)
ax.set_xlim([0, 18])
ax.set_ylim([0, 200])
ax.grid(True, alpha=0.3)
ax.text(0.05, 0.9, f'χ²/dof (MOND)={chi2_MOND_2403/len(R_obs_2403):.1f}',
        transform=ax.transAxes, fontsize=8, color='blue')
ax.text(0.05, 0.83, f'χ²/dof (Verl)={chi2_Verl_2403/len(R_obs_2403):.1f}',
        transform=ax.transAxes, fontsize=8, color='green')
ax.text(0.05, 0.76, f'χ²/dof (cH₀)={chi2_cH0_2403/len(R_obs_2403):.1f}',
        transform=ax.transAxes, fontsize=8, color='red')

# ---- NGC 2403 acceleration profile ----
ax = axes[1, 1]
ax.semilogy(R_model_2403, g_N_arr_2403, 'k-', lw=2, label='g_N (Newton)')
ax.axhline(a0_MOND, color='b', ls='--', lw=1.5, label=f'a₀_MOND={a0_MOND:.1e}')
ax.axhline(a0_Verlinde, color='g', ls=':', lw=1.5, label=f'a₀_Verl={a0_Verlinde:.1e}')
ax.axhline(a0_cH0, color='r', ls=':', lw=1.5, label=f'cH₀={a0_cH0:.1e}')
if R_cross_2403:
    ax.axvline(R_cross_2403, color='orange', ls='--', alpha=0.7)
ax.set_xlabel('R [kpc]')
ax.set_ylabel('g_N [m/s²]')
ax.set_title('NGC 2403: Acceleration Profile')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 18])

# ---- chi2 scan for NGC 2403 ----
ax = axes[1, 2]
ax.loglog(a0_scan / a0_MOND, chi2_scan_2403 / len(R_obs_2403), 'k-', lw=2)
ax.axvline(1.0, color='b', ls='--', label='MOND a₀')
ax.axvline(a0_Verlinde/a0_MOND, color='g', ls=':', label='Verlinde (cH₀/6)')
ax.axvline(a0_cH0/a0_MOND, color='r', ls=':', label='cH₀')
ax.axvline(a0_best_2403/a0_MOND, color='m', ls='-.', label=f'Best fit')
ax.set_xlabel('a₀ / a₀_MOND')
ax.set_ylabel('χ²/dof')
ax.set_title('NGC 2403: χ² vs a₀')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim([0.01, 10])

plt.tight_layout()
outfile = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/compton-unruh/strategies/strategy-001/explorations/exploration-006/rotation_curves.png'
plt.savefig(outfile, dpi=150, bbox_inches='tight')
print(f"\nSaved: rotation_curves.png")

# ============================================================
# BTFR: Baryonic Tully-Fisher Relation
# ============================================================
print()
print("=" * 60)
print("BARYONIC TULLY-FISHER RELATION CHECK")
print("=" * 60)

# v_flat^4 = G*M*a0
# Log-log slope should be 4

masses = np.logspace(8, 12, 100)  # M_sun
log_v_MOND = 0.25 * np.log10(G * masses * M_sun * a0_MOND / (kpc_to_m**3 / (kpc_to_m * 1e3**2)))

# In consistent SI:
def v_BTFR_SI(M, a0):
    G_SI = 6.674e-11  # m^3/(kg*s^2)
    return (G_SI * M * M_sun * a0)**0.25 * 1e-3  # km/s

v_3198_BTFR_MOND = v_BTFR_SI(M_3198, a0_MOND)
v_3198_BTFR_Verl = v_BTFR_SI(M_3198, a0_Verlinde)
v_3198_BTFR_cH0  = v_BTFR_SI(M_3198, a0_cH0)
v_2403_BTFR_MOND = v_BTFR_SI(M_2403, a0_MOND)
v_2403_BTFR_Verl = v_BTFR_SI(M_2403, a0_Verlinde)
v_2403_BTFR_cH0  = v_BTFR_SI(M_2403, a0_cH0)

print("BTFR asymptotic velocity predictions v_flat = (G*M*a0)^(1/4):")
print()
print(f"NGC 3198 (M = {M_3198:.1e} M_sun, observed v_flat ~ 150 km/s):")
print(f"  MOND (a0=1.2e-10): v_flat = {v_3198_BTFR_MOND:.1f} km/s")
print(f"  Verlinde (cH0/6):  v_flat = {v_3198_BTFR_Verl:.1f} km/s")
print(f"  cH0 model:         v_flat = {v_3198_BTFR_cH0:.1f} km/s")
print()
print(f"NGC 2403 (M = {M_2403:.1e} M_sun, observed v_flat ~ 130 km/s):")
print(f"  MOND (a0=1.2e-10): v_flat = {v_2403_BTFR_MOND:.1f} km/s")
print(f"  Verlinde (cH0/6):  v_flat = {v_2403_BTFR_Verl:.1f} km/s")
print(f"  cH0 model:         v_flat = {v_2403_BTFR_cH0:.1f} km/s")
print()

print("=" * 60)
print("SUMMARY OF GALAXY FITS")
print("=" * 60)
print()
print(f"{'Model':<25} {'NGC 3198 chi2/dof':>18} {'NGC 2403 chi2/dof':>18}")
print("-" * 62)
print(f"{'MOND (a0=1.2e-10)':<25} {chi2_MOND_3198/len(R_obs_3198):>18.2f} {chi2_MOND_2403/len(R_obs_2403):>18.2f}")
print(f"{'Verlinde (cH0/6)':<25} {chi2_Verl_3198/len(R_obs_3198):>18.2f} {chi2_Verl_2403/len(R_obs_2403):>18.2f}")
print(f"{'cH0 ratio model':<25} {chi2_cH0_3198/len(R_obs_3198):>18.2f} {chi2_cH0_2403/len(R_obs_2403):>18.2f}")
print(f"{'Best-fit a0':<25} {chi2_best_3198/len(R_obs_3198):>18.2f} {chi2_best_2403/len(R_obs_2403):>18.2f}")
print()
print(f"Best-fit a0:")
print(f"  NGC 3198: {a0_best_3198:.3e} m/s^2 = {a0_best_3198/a0_MOND:.2f} * a0_MOND = {a0_best_3198/a0_Verlinde:.2f} * a0_Verlinde")
print(f"  NGC 2403: {a0_best_2403:.3e} m/s^2 = {a0_best_2403/a0_MOND:.2f} * a0_MOND = {a0_best_2403/a0_Verlinde:.2f} * a0_Verlinde")
print()
print("Conclusion on cH0 model: 5.7x too large a0 => FAILS to fit rotation curves")
print("Conclusion on Verlinde (cH0/6): comparable to MOND, fits within factor ~2")
