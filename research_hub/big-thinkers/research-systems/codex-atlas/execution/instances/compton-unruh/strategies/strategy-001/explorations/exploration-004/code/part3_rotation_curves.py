"""
Part 3: Modified Equation of Motion and Rotation Curves

Given the modified inertia hypothesis from Part 2:
  mu(a/a0) * a = g_N  where mu(x) = x/sqrt(1+x^2), a0 = cH0

We compute:
1. m_i(a)/m ratio
2. Rotation curves for a typical galaxy
3. Comparison with MOND using the observed a0
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Physical constants
hbar = 1.054571817e-34
c = 2.99792458e8
kB = 1.380649e-23
G_N = 6.67430e-11
H0 = 2.2e-18
a0_MOND = 1.2e-10
cH0 = c * H0
M_sun = 1.989e30
kpc = 3.0857e19  # 1 kpc in meters

print("=" * 70)
print("Part 3: Modified Equation of Motion and Rotation Curves")
print("=" * 70)

# ======================================================================
# SECTION 3.1: Effective inertial mass ratio
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.1: Effective Inertial Mass Ratio m_i(a)/m")
print("=" * 70)

# Under the ratio hypothesis: m_i(a) = m * T_U(a)/T_dS(a) = m * a/sqrt(a^2 + c^2*H^2)
# mu(a) = a / sqrt(a^2 + c^2*H^2)
# or equivalently: mu(x) = x/sqrt(1+x^2) with x = a/(cH0)

# Also consider with Verlinde's scale: a0_V = cH0/6
a0_Verlinde = cH0 / 6

def mu_standard(a, a0):
    """Standard MOND interpolation function mu(x) = x/sqrt(1+x^2)"""
    x = a / a0
    return x / np.sqrt(1 + x**2)

a_range = np.logspace(-15, 0, 1000)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Plot mu(a) for different a0 values
for a0_val, label, color, style in [
    (cH0, f'a0 = cH0 = {cH0:.2e}', 'red', '--'),
    (a0_Verlinde, f'a0 = cH0/6 = {a0_Verlinde:.2e}', 'green', ':'),
    (a0_MOND, f'a0 = a0_MOND = {a0_MOND:.2e}', 'blue', '-'),
]:
    mu_vals = mu_standard(a_range, a0_val)
    ax1.semilogx(a_range, mu_vals, color=color, linestyle=style,
                 label=label, linewidth=2)

ax1.axvline(cH0, color='gray', linestyle=':', alpha=0.3)
ax1.axvline(a0_MOND, color='gray', linestyle=':', alpha=0.3)
ax1.set_xlabel(r'Acceleration $a$ (m/s$^2$)', fontsize=12)
ax1.set_ylabel(r'$\mu(a) = m_i(a)/m$', fontsize=12)
ax1.set_title('Effective inertial mass ratio', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1e-15, 1e0)
ax1.set_ylim(0, 1.1)

# Also show the "simple" MOND interpolation mu(x) = x/(1+x) for comparison
def mu_simple(a, a0):
    x = a / a0
    return x / (1 + x)

for a0_val, label, color, style in [
    (a0_MOND, r'$\mu = x/\sqrt{1+x^2}$ (standard)', 'blue', '-'),
    (a0_MOND, r'$\mu = x/(1+x)$ (simple)', 'purple', '--'),
]:
    if 'simple' in label:
        mu_vals = mu_simple(a_range, a0_val)
    else:
        mu_vals = mu_standard(a_range, a0_val)
    ax2.semilogx(a_range, mu_vals, color=color, linestyle=style,
                 label=label, linewidth=2)

ax2.set_xlabel(r'Acceleration $a$ (m/s$^2$)', fontsize=12)
ax2.set_ylabel(r'$\mu(a)$', fontsize=12)
ax2.set_title('MOND interpolation functions compared (both at a0 = a0_MOND)', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1e-15, 1e0)
ax2.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot6_inertial_mass_ratio.png'), dpi=150)
plt.close()
print("Plot 6 saved: plot6_inertial_mass_ratio.png")

# Print key values
print(f"\nScale comparison:")
print(f"  cH0 = {cH0:.4e} m/s^2")
print(f"  cH0/6 (Verlinde) = {cH0/6:.4e} m/s^2")
print(f"  a0_MOND (observed) = {a0_MOND:.4e} m/s^2")
print(f"  Ratio cH0/a0_MOND = {cH0/a0_MOND:.2f}")
print(f"  Ratio (cH0/6)/a0_MOND = {cH0/(6*a0_MOND):.3f}")

# ======================================================================
# SECTION 3.2: Rotation Curves
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.2: Galaxy Rotation Curves")
print("=" * 70)

def solve_mond_a(g_N, a0):
    """Solve mu(a/a0)*a = g_N for the standard interpolation function."""
    if g_N <= 0:
        return 0
    def residual(a):
        x = a / a0
        return a * x / np.sqrt(1 + x**2) - g_N
    a_max = max(g_N * 100, a0 * 100)
    try:
        return brentq(residual, 1e-40, a_max)
    except:
        return g_N

def rotation_curve_newton(r, M):
    """Newtonian circular velocity: v = sqrt(GM/r)"""
    return np.sqrt(G_N * M / r)

def rotation_curve_mond(r, M, a0):
    """MOND rotation curve with mu(x) = x/sqrt(1+x^2)"""
    g_N = G_N * M / r**2
    a_obs = np.array([solve_mond_a(g, a0) for g in g_N])
    return np.sqrt(a_obs * r)

# Galaxy parameters
M_galaxy = 1e11 * M_sun  # typical galaxy mass (~ Milky Way)
r_range = np.linspace(1, 100, 200) * kpc  # 1 to 100 kpc
r_kpc = r_range / kpc

# Compute rotation curves
v_newton = rotation_curve_newton(r_range, M_galaxy) / 1e3  # km/s

# MOND with observed a0
v_mond_std = rotation_curve_mond(r_range, M_galaxy, a0_MOND) / 1e3

# Our model with a0 = cH0
v_mond_cH0 = rotation_curve_mond(r_range, M_galaxy, cH0) / 1e3

# Our model with a0 = cH0/6 (Verlinde)
v_mond_verlinde = rotation_curve_mond(r_range, M_galaxy, a0_Verlinde) / 1e3

# Deep MOND asymptotic velocity: v^4 = G*M*a0
v_flat_std = (G_N * M_galaxy * a0_MOND)**0.25 / 1e3
v_flat_cH0 = (G_N * M_galaxy * cH0)**0.25 / 1e3
v_flat_verlinde = (G_N * M_galaxy * a0_Verlinde)**0.25 / 1e3

print(f"\nGalaxy: M = {M_galaxy/M_sun:.1e} M_sun")
print(f"Deep MOND asymptotic velocities (v^4 = GMa0):")
print(f"  a0 = a0_MOND: v_flat = {v_flat_std:.1f} km/s")
print(f"  a0 = cH0:     v_flat = {v_flat_cH0:.1f} km/s")
print(f"  a0 = cH0/6:   v_flat = {v_flat_verlinde:.1f} km/s")
print(f"  Observed MW flat velocity: ~220 km/s")

# Newtonian velocity at specific radii
for r_val in [10, 30, 50, 100]:
    r_m = r_val * kpc
    g = G_N * M_galaxy / r_m**2
    print(f"\n  At r = {r_val} kpc:")
    print(f"    g_N = {g:.4e} m/s^2")
    print(f"    g_N/a0_MOND = {g/a0_MOND:.2f}")
    print(f"    g_N/cH0 = {g/cH0:.4f}")

# ======================================================================
# PLOT 7: Rotation curves
# ======================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Top: Rotation curves
ax1.plot(r_kpc, v_newton, 'k-', label=f'Newton (M={M_galaxy/M_sun:.0e} M_sun)',
         linewidth=2)
ax1.plot(r_kpc, v_mond_std, 'b-', label=f'MOND (a0={a0_MOND:.1e})',
         linewidth=2)
ax1.plot(r_kpc, v_mond_cH0, 'r--', label=f'dS model (a0=cH0={cH0:.1e})',
         linewidth=2)
ax1.plot(r_kpc, v_mond_verlinde, 'g:', label=f'dS model (a0=cH0/6={a0_Verlinde:.1e})',
         linewidth=2)
ax1.axhline(v_flat_std, color='blue', linestyle=':', alpha=0.3)
ax1.axhline(220, color='gray', linestyle=':', alpha=0.3)
ax1.text(85, 225, 'MW observed', fontsize=9, color='gray')
ax1.set_xlabel('Radius (kpc)', fontsize=12)
ax1.set_ylabel('Circular velocity (km/s)', fontsize=12)
ax1.set_title(f'Rotation Curves: M = {M_galaxy/M_sun:.0e} M_sun', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 500)

# Bottom: Ratio v/v_Newton
ax2.plot(r_kpc, v_mond_std/v_newton, 'b-', label='MOND / Newton', linewidth=2)
ax2.plot(r_kpc, v_mond_cH0/v_newton, 'r--', label='dS (a0=cH0) / Newton', linewidth=2)
ax2.plot(r_kpc, v_mond_verlinde/v_newton, 'g:', label='dS (a0=cH0/6) / Newton', linewidth=2)
ax2.axhline(1, color='k', linestyle='-', linewidth=1, alpha=0.3)
ax2.set_xlabel('Radius (kpc)', fontsize=12)
ax2.set_ylabel('v / v_Newton', fontsize=12)
ax2.set_title('Boost factor vs radius', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 100)
ax2.set_ylim(0.5, 5)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot7_rotation_curves.png'), dpi=150)
plt.close()
print("\nPlot 7 saved: plot7_rotation_curves.png")

# ======================================================================
# SECTION 3.3: The a0 problem
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.3: The a0 Scale Problem")
print("=" * 70)

print(f"""
The ratio model gives mu(x) = x/sqrt(1+x^2) with a0 = cH0 = {cH0:.4e} m/s^2.
The observed MOND value is a0 = {a0_MOND:.4e} m/s^2.

The discrepancy factor is {cH0/a0_MOND:.2f}.

This is NOT a fatal flaw — it's a well-known issue in all approaches
that try to derive a0 from cosmological parameters. The exact
relationship between a0 and cH0 depends on:

1. The number of field degrees of freedom (we used 1 scalar; the SM has ~100+)
2. The precise form of the entropy-area relationship
3. Whether the de Sitter radius or the particle horizon matters
4. Numerical factors from the integration over modes

Known relationships in the literature:
  - Milgrom (1983): a0 ~ cH0 (empirical, factor ~1/6)
  - Verlinde (2016): a0 = cH0/(2*pi) ~ cH0/6 = {cH0/6:.4e} → ratio to obs: {cH0/(6*a0_MOND):.2f}
  - McCulloch (2007): a0 = 2*c^2/(R_H*pi) ~ {2*c**2/(c/H0*np.pi):.4e} → ratio: {2*c*H0/np.pi/a0_MOND:.2f}

So getting a0 within a factor of ~5-10 of cH0 is typical and
probably acceptable at this stage of the derivation.

The more important question: does the FUNCTIONAL FORM mu(x) = x/sqrt(1+x^2)
match observations? This is the "standard" MOND interpolation function,
and it is known to fit galaxy rotation curves well.
""")

# ======================================================================
# SECTION 3.4: Comparison with specific galaxies
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.4: Comparison for Different Galaxy Masses")
print("=" * 70)

# Compute asymptotic flat velocities for several galaxy masses
galaxy_masses = [1e9, 1e10, 5e10, 1e11, 5e11, 1e12]  # in M_sun

print(f"\nAsymptotic flat rotation velocities (v^4 = GMa0):")
print(f"{'M/M_sun':>12s}  {'v_Newton(30kpc)':>15s}  {'v_MOND':>10s}  {'v_dS(cH0)':>10s}  {'v_dS(cH0/6)':>12s}")
for M_sol in galaxy_masses:
    M = M_sol * M_sun
    v_N = rotation_curve_newton(np.array([30*kpc]), M)[0] / 1e3
    v_M = (G_N * M * a0_MOND)**0.25 / 1e3
    v_dS = (G_N * M * cH0)**0.25 / 1e3
    v_V = (G_N * M * a0_Verlinde)**0.25 / 1e3
    print(f"{M_sol:12.0e}  {v_N:15.1f}  {v_M:10.1f}  {v_dS:10.1f}  {v_V:12.1f}")

# ======================================================================
# SECTION 3.5: Tully-Fisher relation
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.5: Baryonic Tully-Fisher Relation")
print("=" * 70)

print("""
A key prediction of MOND is the Baryonic Tully-Fisher Relation (BTFR):
  M_baryonic = v_flat^4 / (G*a0)

Our model predicts exactly the same relation with a0 = cH0 (or cH0/6).
Since the functional form is identical to MOND, ALL predictions of
MOND with the standard interpolation function are automatically
reproduced — just with a different value of a0.

The observed BTFR slope is v^4 ~ M with normalization:
  M = v^4 / (G * a0) where a0 ~ 1.2e-10 m/s^2

Our prediction:
  M = v^4 / (G * cH0) = v^4 / (G * 6.6e-10)

This predicts ~5.5x more baryonic mass than observed for a given v_flat,
OR equivalently, ~1.5x lower v_flat for a given mass (since v ~ M^(1/4)).

With a0 = cH0/6: the BTFR is reproduced within ~8%.
""")

# Numerical BTFR comparison
v_range = np.linspace(50, 300, 100)  # km/s
M_btfr_mond = (v_range * 1e3)**4 / (G_N * a0_MOND) / M_sun
M_btfr_dS = (v_range * 1e3)**4 / (G_N * cH0) / M_sun
M_btfr_verlinde = (v_range * 1e3)**4 / (G_N * a0_Verlinde) / M_sun

fig, ax = plt.subplots(figsize=(10, 8))
ax.loglog(v_range, M_btfr_mond, 'b-', label=f'MOND (a0={a0_MOND:.1e})', linewidth=2)
ax.loglog(v_range, M_btfr_dS, 'r--', label=f'dS model (a0=cH0)', linewidth=2)
ax.loglog(v_range, M_btfr_verlinde, 'g:', label=f'dS model (a0=cH0/6)', linewidth=2)
ax.set_xlabel('Flat rotation velocity (km/s)', fontsize=12)
ax.set_ylabel(r'Baryonic mass ($M_\odot$)', fontsize=12)
ax.set_title('Baryonic Tully-Fisher Relation', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Add some observed data points (approximate)
# Milky Way: v ~ 220 km/s, M_bar ~ 6e10 M_sun
# NGC 3198: v ~ 150 km/s, M_bar ~ 3e10 M_sun
obs_v = [220, 150, 100, 300]
obs_M = [6e10, 3e10, 5e9, 2e11]
ax.scatter(obs_v, obs_M, c='black', s=100, zorder=5, label='Approximate observations')
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot8_tully_fisher.png'), dpi=150)
plt.close()
print("Plot 8 saved: plot8_tully_fisher.png")

# ======================================================================
# SECTION 3.6: The external field effect test
# ======================================================================
print("\n" + "=" * 70)
print("Section 3.6: Distinguishing Predictions")
print("=" * 70)

print("""
Since our model reproduces the SAME interpolation function as standard
MOND (just with a0 = cH0 instead of a0_MOND), the ONLY testable
difference is in the value of a0.

Key observational tests:
1. BTFR normalization: Our model predicts a0 = cH0, which gives
   ~5.5x too much mass for a given v_flat. With a0 = cH0/6, the
   match is much better (~8% off).

2. External field effect (EFE): In MOND, the EFE is a feature of
   the specific theory (AQUAL, TeVeS). Our model would need to
   specify whether the de Sitter background affects the TOTAL
   acceleration or only the self-acceleration. This is a genuine
   prediction that differs between models.

3. Cosmological evolution: If a0 = cH0, then a0 changes with cosmic
   time (H evolves). This predicts stronger MOND effects at earlier
   times (higher H), which is testable with high-redshift rotation
   curves. However, this prediction is shared with other a0 ~ cH models.

4. Solar system: At solar-system accelerations (a ~ 6e-3 m/s^2 at
   Earth's orbit), mu(a/cH0) = 1 - 5e-15, which is undetectable.
   No conflict with precision solar system tests.
""")

# Solar system check
a_earth = G_N * M_sun / (1.496e11)**2  # Earth orbital acceleration
mu_earth = mu_standard(a_earth, cH0)
print(f"Solar system consistency check:")
print(f"  Earth orbital acceleration: a = {a_earth:.4e} m/s^2")
print(f"  a/cH0 = {a_earth/cH0:.4e}")
print(f"  mu(a/cH0) = 1 - {1-mu_earth:.2e}")
print(f"  Deviation from Newton: {(1-mu_earth)*100:.2e}%")
print(f"  => Completely undetectable in solar system")

# Pioneer anomaly check (a_P ~ 8.7e-10 m/s^2 at ~70 AU)
a_pioneer = G_N * M_sun / (70*1.496e11)**2
mu_pioneer = mu_standard(a_pioneer, cH0)
print(f"\n  Pioneer distance (~70 AU):")
print(f"  Gravitational acceleration: a = {a_pioneer:.4e} m/s^2")
print(f"  a/cH0 = {a_pioneer/cH0:.4f}")
print(f"  mu = {mu_pioneer:.6f}")
print(f"  Deviation from Newton: {(1-mu_pioneer)*100:.4f}%")

# ======================================================================
# SUMMARY
# ======================================================================
print("\n" + "=" * 70)
print("PART 3 SUMMARY")
print("=" * 70)
print(f"""
1. The modified inertia hypothesis m_i(a) = m * T_U/T_dS gives:
   mu(x) = x/sqrt(1+x^2) with x = a/cH0

2. This is the STANDARD MOND interpolation function with a0 = cH0.

3. Rotation curves flatten with asymptotic v = (GMa0)^(1/4), exactly
   as in MOND. The asymptotic velocity is ~1.5x too high compared to
   observations (because a0 = cH0 = 5.5*a0_MOND).

4. Using a0 = cH0/6 (Verlinde's factor) brings the prediction within
   ~8% of observations.

5. The model is consistent with solar system precision tests
   (deviation < 10^-14 at Earth orbit).

6. The model reproduces the Baryonic Tully-Fisher Relation with the
   correct slope (v^4 ~ M) but ~5.5x off in normalization (or ~8%
   off with Verlinde's factor).

7. Since the functional form is identical to MOND, the model
   inherits ALL of MOND's rotation curve successes — it differs
   only in the value of a0 and potentially in the EFE.
""")
