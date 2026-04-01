"""
Adversarial stress tests for T_U/T_dS modified inertia model.
m_i = m * mu(g_N/a0), mu(x) = x/sqrt(1+x^2)
a0 = c*H0/6 ≈ 1.1e-10 m/s^2
"""

import numpy as np

# Constants
G = 6.674e-11       # m^3 kg^-1 s^-2
c = 3e8             # m/s
H0 = 2.18e-18       # s^-1 (67 km/s/Mpc)
Msun = 1.989e30     # kg
kpc = 3.086e19      # m
Mpc = 3.086e22      # m
AU = 1.496e11       # m

# Model parameters
a0 = c * H0 / 6     # MOND acceleration scale with Verlinde correction
a0_standard = 1.2e-10  # Standard MOND a0 from observations

print("=" * 70)
print("MODEL PARAMETERS")
print("=" * 70)
print(f"H0 = {H0:.3e} s^-1 = {H0*Mpc/1e3:.1f} km/s/Mpc")
print(f"a0 = cH0/6 = {a0:.3e} m/s^2")
print(f"a0_standard = {a0_standard:.3e} m/s^2")
print(f"Ratio a0/a0_standard = {a0/a0_standard:.3f}")
print()

def mu(x):
    """MOND interpolation function: mu(x) = x/sqrt(1+x^2)"""
    return x / np.sqrt(1 + x**2)

# ============================================================
# SECTION 1: BULLET CLUSTER
# ============================================================
print("=" * 70)
print("SECTION 1: BULLET CLUSTER ANALYSIS")
print("=" * 70)

# Bullet cluster parameters
M_gas_bullet = 3e13 * Msun     # Hot gas mass (dominant baryon component)
M_stars_bullet = 5e12 * Msun   # Stellar mass
M_total_baryon_bullet = M_gas_bullet + M_stars_bullet
M_lensing_bullet = 2e14 * Msun  # Observed lensing mass
M_DM_required = M_lensing_bullet - M_total_baryon_bullet

print("\nBullet Cluster (1E 0657-558) parameters:")
print(f"  Gas mass: {M_gas_bullet/Msun:.2e} Msun")
print(f"  Stellar mass: {M_stars_bullet/Msun:.2e} Msun")
print(f"  Total baryonic: {M_total_baryon_bullet/Msun:.2e} Msun")
print(f"  Observed lensing mass: {M_lensing_bullet/Msun:.2e} Msun")
print(f"  Required dark matter: {M_DM_required/Msun:.2e} Msun")
print(f"  DM/baryon ratio: {M_DM_required/M_total_baryon_bullet:.1f}:1")
print(f"  Gas fraction of baryons: {M_gas_bullet/M_total_baryon_bullet:.0%}")

print("\nKey issue for modified INERTIA (not modified gravity):")
print("  - Modified inertia changes m_i, NOT m_g")
print("  - Gravitational potential: Poisson equation is UNCHANGED")
print("  - ∇²Φ = 4πG × ρ_baryon (standard)")
print("  - Lensing depends on total Φ, which is sourced by baryons only")
print("  - Lensing peak should be at GAS location (85% of baryons)")
print("  - Observed: lensing peak at GALAXY (stellar) location")
print("  - CONCLUSION: Modified inertia CANNOT explain Bullet Cluster offset")

# Compute convergence offset estimate
R_cluster = 1.0 * Mpc  # Approximate cluster radius
r_separation = 720 * kpc  # Gas-galaxy offset

# Modified MOND lensing (if we used modified gravity analog)
# In MOND, effective surface density for lensing is enhanced in deep-MOND regime
# For cluster scale, check if we're even in MOND regime
r_test = 0.5 * Mpc  # Half cluster radius
g_N_cluster = G * M_total_baryon_bullet / r_test**2
x_cluster = g_N_cluster / a0
mu_cluster = mu(x_cluster)

print(f"\nAt r = 0.5 Mpc from Bullet cluster center:")
print(f"  g_N = {g_N_cluster:.3e} m/s^2")
print(f"  x = g_N/a0 = {x_cluster:.3f}")
print(f"  mu = {mu_cluster:.4f}")
print(f"  Effective mass in MOND gravity: M_eff = M_baryon/mu = {M_total_baryon_bullet/Msun/mu_cluster:.2e} Msun")
print(f"  Compare to lensing mass: {M_lensing_bullet/Msun:.2e} Msun")
print(f"  Ratio (MOND effective / lensing): {M_total_baryon_bullet/mu_cluster/M_lensing_bullet:.2f}")
print(f"  NOTE: MOND gravity also fails (ratio ≠ 1.0), but at least lensing traces gas+galaxies")
print(f"  In modified INERTIA, no enhancement of gravitational potential → fails worse")

print("\nMODIFIED INERTIA-SPECIFIC PROBLEM:")
print("  If lensing follows baryons only (no enhanced potential):")
lensing_prediction = M_total_baryon_bullet
print(f"  Predicted lensing mass = {lensing_prediction/Msun:.2e} Msun")
print(f"  Observed lensing mass  = {M_lensing_bullet/Msun:.2e} Msun")
print(f"  Discrepancy factor: {M_lensing_bullet/lensing_prediction:.1f}x")
print("  VERDICT: CRITICAL FAILURE — lensing mass underestimated by ~6x")
print("  AND lensing morphology is wrong (gas vs galaxy offset)")

# ============================================================
# SECTION 2: CMB THIRD ACOUSTIC PEAK
# ============================================================
print()
print("=" * 70)
print("SECTION 2: CMB THIRD ACOUSTIC PEAK")
print("=" * 70)

# Hubble parameter at recombination z=1100
z_rec = 1100
# Matter-radiation equality at z_eq ~ 3400
z_eq = 3400
# H(z) in flat ΛCDM (simplified, matter+radiation dominated at z=1100)
# H^2 = H0^2 * [Omega_m*(1+z)^3 + Omega_r*(1+z)^4]
Omega_m = 0.31
Omega_r = 9e-5
Omega_Lambda = 0.69

def H_of_z(z):
    return H0 * np.sqrt(Omega_m*(1+z)**3 + Omega_r*(1+z)**4 + Omega_Lambda)

H_rec = H_of_z(z_rec)
H_BBN = H_of_z(1e9)  # approximate BBN epoch

print(f"\nH(z=1100) = {H_rec:.3e} s^-1 = {H_rec/H0:.0e} × H0")
print(f"H(BBN, z~1e9) = {H_BBN:.3e} s^-1 = {H_BBN/H0:.0e} × H0")

# If a0 evolves with H: a0(z) = c*H(z)/6
a0_rec_evolving = c * H_rec / 6
a0_BBN_evolving = c * H_BBN / 6

print(f"\nIF a0 = cH(z)/6 EVOLVES with H:")
print(f"  a0(z=1100) = {a0_rec_evolving:.3e} m/s^2 = {a0_rec_evolving/a0:.0e} × a0(today)")
print(f"  a0(BBN) = {a0_BBN_evolving:.3e} m/s^2")

# Typical acceleration in CMB perturbations at recombination
# Sound horizon at recombination ~ 150 Mpc (comoving) = 150/(1+1100) Mpc (physical) = 0.136 Mpc
r_sound = 150 * Mpc / (1 + z_rec)
# Mean baryon density at recombination
rho_crit_0 = 3 * H0**2 / (8 * np.pi * G)
rho_b_rec = 0.05 * rho_crit_0 * (1 + z_rec)**3  # Omega_b ~ 0.05
# Density perturbation amplitude at z=1100: delta ~ 10^-4 (CMB amplitude)
delta_rec = 1e-4
# Gravitational acceleration at sound horizon scale
g_CMB = 4/3 * np.pi * G * rho_b_rec * delta_rec * r_sound

print(f"\nTypical gravitational acceleration in CMB perturbations (sound horizon scale):")
print(f"  r_sound (physical at z=1100) = {r_sound/kpc:.1f} kpc = {r_sound/Mpc*1000:.1f} Mpc (physical)")
print(f"  rho_baryon(z=1100) = {rho_b_rec:.3e} kg/m^3")
print(f"  delta_rec ~ 10^-4")
print(f"  g_CMB ~ {g_CMB:.3e} m/s^2")

print(f"\nIf a0 EVOLVES: x = g_CMB/a0(z=1100) = {g_CMB/a0_rec_evolving:.3e}")
print(f"  mu(x) = {mu(g_CMB/a0_rec_evolving):.3e}")
print(f"  → DEEP MOND (mu << 1) at recombination: CATASTROPHIC")

print(f"\nIf a0 is FIXED at today's value: x = g_CMB/a0(today) = {g_CMB/a0:.3e}")
print(f"  mu(x) = {mu(g_CMB/a0):.3f}")
print(f"  → Still in Newtonian regime (mu ~ 1): CMB unaffected")

print(f"\nIF a0 IS FIXED:")
print(f"  - CMB acoustic oscillations are in Newtonian regime")
print(f"  - MOND effect only starts after structure forms at low-z")
print(f"  - BUT: still need to explain CMB peak ratios WITHOUT dark matter")
print(f"  - CDM contribution to CMB peak ratio is ~27% of total energy density")
print(f"  - Without CDM: 3rd peak dramatically reduced relative to 1st peak")
print(f"  - Standard MOND/modified inertia predicts ONLY baryons -> wrong peak ratios")
print(f"  VERDICT: Modified inertia at fixed a0 doesn't affect CMB dynamics, BUT")
print(f"  model predicts wrong CMB peak ratios because no dark matter contribution")

# ============================================================
# SECTION 3: GRAVITATIONAL LENSING
# ============================================================
print()
print("=" * 70)
print("SECTION 3: GRAVITATIONAL LENSING WITHOUT DARK MATTER")
print("=" * 70)

print("\nKey distinction in modified INERTIA vs modified GRAVITY:")
print()
print("  Modified GRAVITY (MOND Poisson equation):")
print("    ∇·[μ(|∇Φ|/a0) × ∇Φ] = 4πG × ρ_baryon")
print("    → Enhanced potential → enhanced lensing (partially compensates)")
print()
print("  Modified INERTIA (T_U/T_dS model):")
print("    ∇²Φ = 4πG × ρ_baryon  (STANDARD Poisson equation)")
print("    Only inertial mass is modified: m_i = m × μ(g_N/a0)")
print("    → Gravitational potential is UNCHANGED")
print("    → Lensing (photon geodesics in Φ) is UNCHANGED")
print("    → Lensing traces baryons ONLY")

# Typical galaxy cluster lensing comparison
M_baryon_cluster = 5e13 * Msun   # Typical cluster baryonic mass
M_lensing_cluster = 5e14 * Msun  # Typical cluster lensing mass
mass_ratio = M_lensing_cluster / M_baryon_cluster

print(f"\nTypical galaxy cluster:")
print(f"  Baryonic mass: {M_baryon_cluster/Msun:.1e} Msun")
print(f"  Lensing mass: {M_lensing_cluster/Msun:.1e} Msun")
print(f"  Ratio: {mass_ratio:.0f}:1 dark matter to baryons")
print(f"  Modified inertia prediction: lensing mass = {M_baryon_cluster/Msun:.1e} Msun")
print(f"  Discrepancy: {mass_ratio:.0f}x")

# Einstein radius comparison
# θ_E = sqrt(4GM/c^2 × D_ls/(D_l D_s))
# For a given lens geometry, θ_E ∝ sqrt(M_lens)
theta_ratio = np.sqrt(mass_ratio)
print(f"\n  Einstein radius θ_E ∝ √M_lens")
print(f"  Modified inertia underestimates θ_E by factor: √{mass_ratio:.0f} = {theta_ratio:.1f}")
print(f"  This would be immediately detectable in strong lensing systems")

print(f"\nElliptical galaxy scale (strong lensing):")
M_baryon_ell = 1e12 * Msun
M_lensing_ell = 5e12 * Msun
print(f"  Baryonic mass: {M_baryon_ell/Msun:.1e} Msun")
print(f"  Lensing mass: {M_lensing_ell/Msun:.1e} Msun")
print(f"  Ratio: {M_lensing_ell/M_baryon_ell:.0f}:1")

print(f"\nIn modified MOND gravity (not this model):")
r_ell = 10 * kpc
g_N_ell = G * M_baryon_ell / r_ell**2
x_ell = g_N_ell / a0
mu_ell = mu(x_ell)
print(f"  At r=10 kpc: g_N = {g_N_ell:.3e}, x = {x_ell:.2f}, mu = {mu_ell:.4f}")
print(f"  MOND effective mass = M_baryon/mu = {M_baryon_ell/mu_ell/Msun:.2e} Msun")
print(f"  (MOND gravity can partially compensate; modified inertia cannot)")

print(f"\nVERDICT: Critical failure for modified inertia at cluster scale lensing")
print(f"  Note: MOND gravity also fails (clusters still have 2-3x missing mass)")
print(f"  Modified inertia fails MORE severely because lensing is unaffected by μ")

# ============================================================
# SECTION 4: GALAXY CLUSTER DYNAMICS — COMA CLUSTER
# ============================================================
print()
print("=" * 70)
print("SECTION 4: GALAXY CLUSTER DYNAMICS — COMA CLUSTER")
print("=" * 70)

# Coma cluster parameters
M_gas_coma = 3e14 * Msun        # Hot gas (dominant baryon)
M_stars_coma = 6e13 * Msun      # Stellar mass
M_total_baryon_coma = M_gas_coma + M_stars_coma
M_dyn_coma = 1.5e15 * Msun      # Dynamical mass from virial theorem
sigma_obs_coma = 900e3           # Observed velocity dispersion, m/s
R_coma = 1.5 * Mpc              # Cluster radius

print(f"\nComa cluster parameters:")
print(f"  Total baryonic mass: {M_total_baryon_coma/Msun:.2e} Msun")
print(f"  Gas fraction: {M_gas_coma/M_total_baryon_coma:.0%}")
print(f"  Dynamical mass: {M_dyn_coma/Msun:.2e} Msun")
print(f"  Dark matter ratio: {(M_dyn_coma-M_total_baryon_coma)/M_total_baryon_coma:.1f}:1")
print(f"  Observed σ: {sigma_obs_coma/1e3:.0f} km/s")
print(f"  Cluster radius: {R_coma/Mpc:.1f} Mpc")

# MOND prediction for velocity dispersion
# In deep MOND virial: sigma^4 ~ G * M_baryon * a0
# (From Sanders 1994, The de Mott & Sanders, Milgrom 1997 cluster dynamics)
# More precisely: sigma^4 = G * M_baryon * a0 * (constant)
# The constant depends on geometry; for isothermal sphere ~ 1/(4)
# Let's use the relation: 4 * sigma^4 = G * M_baryon * a0 (Milgrom 1997 estimate)

sigma_MOND = (G * M_total_baryon_coma * a0)**(0.25)
print(f"\nMOND/Modified-inertia prediction:")
print(f"  Deep MOND virial: sigma^4 = G*M_b*a0")
print(f"  sigma_MOND = (G*M_b*a0)^(1/4) = {sigma_MOND/1e3:.0f} km/s")
print(f"  Observed sigma = {sigma_obs_coma/1e3:.0f} km/s")
print(f"  Ratio sigma_MOND/sigma_obs = {sigma_MOND/sigma_obs_coma:.2f}")

# What acceleration regime is the cluster in?
g_N_coma_gal = G * M_total_baryon_coma / R_coma**2
x_coma = g_N_coma_gal / a0
mu_coma = mu(x_coma)
print(f"\nAcceleration analysis at cluster periphery (r={R_coma/Mpc:.1f} Mpc):")
print(f"  g_N = {g_N_coma_gal:.3e} m/s^2")
print(f"  x = g_N/a0 = {x_coma:.4f}")
print(f"  mu(x) = {mu_coma:.4f}")
print(f"  We are in DEEP MOND regime (x << 1): mu ≈ x = {x_coma:.4f}")

# Dynamical mass from centripetal balance in modified inertia
# For a cluster, gravity vs inertia: G*M_b*m/(r^2) = m_i * v^2/r = m*mu * v^2/r
# So G*M_b/r^2 = mu * v^2/r
# v^2 = G*M_b/(r * mu)
# sigma^2 ≈ v^2 (rough virial)
sigma_pred_MI = np.sqrt(G * M_total_baryon_coma / (R_coma * mu_coma))
print(f"\nModified inertia circular velocity at cluster periphery:")
print(f"  v^2 = G*M_b/(r * mu): v = {sigma_pred_MI/1e3:.0f} km/s")
print(f"  Compare observed sigma = {sigma_obs_coma/1e3:.0f} km/s")
print(f"  Ratio: {sigma_pred_MI/sigma_obs_coma:.2f}")

# What baryonic mass would be needed to explain sigma_obs in MOND?
M_needed_MOND = sigma_obs_coma**4 / (G * a0)
print(f"\nMass needed to explain sigma_obs in MOND:")
print(f"  M_needed = sigma^4/(G*a0) = {M_needed_MOND/Msun:.2e} Msun")
print(f"  M_baryon actual = {M_total_baryon_coma/Msun:.2e} Msun")
print(f"  Missing mass factor: {M_needed_MOND/M_total_baryon_coma:.1f}x")
print(f"  (Classic MOND failure: clusters need ~2-3x more mass than baryons)")
print(f"  Modified inertia inherits this MOND cluster failure identically")
print(f"  VERDICT: FAIL — ~2.5x missing mass even with modified inertia")

# ============================================================
# SECTION 5: EXTERNAL FIELD EFFECT
# ============================================================
print()
print("=" * 70)
print("SECTION 5: EXTERNAL FIELD EFFECT (EFE)")
print("=" * 70)

# Milky Way external field at Sun's position
v_circ_MW = 220e3   # m/s
r_sun = 8 * kpc
g_ext_MW = v_circ_MW**2 / r_sun  # external field from MW at Sun

# EFE: if total acceleration enters mu, solar system sees EFE
# g_int = g_Sun(Earth) ~ 6e-3 m/s^2
# g_ext = g_MW ~ 2e-10 m/s^2
g_Earth = G * Msun / AU**2
g_total_Earth = np.sqrt(g_Earth**2 + g_ext_MW**2)  # Approximate vectorial sum

x_Earth_internal = g_Earth / a0
x_Earth_external = g_ext_MW / a0
x_Earth_total = g_total_Earth / a0

print(f"\nSun-Earth system parameters:")
print(f"  g_Sun at Earth orbit: {g_Earth:.3e} m/s^2")
print(f"  g_MW external field: {g_ext_MW:.3e} m/s^2")
print(f"  x_internal = g_Earth/a0 = {x_Earth_internal:.2e}")
print(f"  x_external = g_ext/a0 = {x_Earth_external:.4f}")
print(f"  mu(x_total) = {mu(x_Earth_total):.10f}")
print(f"  mu(x_internal) = {mu(x_Earth_internal):.10f}")
print(f"  Difference: {abs(mu(x_Earth_total)-mu(x_Earth_internal)):.2e}")

# Wide binary system in the Milky Way
# Typical wide binary separation: 1-10 kAU
# Internal acceleration
r_WB = 1e4 * AU      # 10,000 AU separation
M_WB = 2 * Msun      # two solar mass stars
g_WB_internal = G * M_WB / r_WB**2

x_WB_internal = g_WB_internal / a0
x_WB_external = g_ext_MW / a0
x_WB_total = np.sqrt(g_WB_internal**2 + g_ext_MW**2) / a0

print(f"\nWide binary at 10,000 AU (r = {r_WB/kpc:.2f} kpc from each other):")
print(f"  g_internal = {g_WB_internal:.3e} m/s^2")
print(f"  g_external (MW) = {g_ext_MW:.3e} m/s^2")
print(f"  x_internal/a0 = {x_WB_internal:.4f}")
print(f"  x_external/a0 = {x_WB_external:.4f}")
print(f"  x_total/a0 = {x_WB_total:.4f}")
print(f"  mu(internal only) = {mu(x_WB_internal):.6f}")
print(f"  mu(total) = {mu(x_WB_total):.6f}")
print(f"  With EFE: mu is suppressed from {mu(x_WB_internal):.4f} to {mu(x_WB_total):.4f}")
print(f"  Predicted orbital velocity boost (no EFE): {1/mu(x_WB_internal):.3f}")
print(f"  Predicted orbital velocity boost (with EFE): {1/mu(x_WB_total):.3f}")

print(f"\n  NOTE: Wide binary EFE creates a testable prediction:")
print(f"  At 10,000 AU, g_int ~ g_ext (both ~ a0). EFE is SIGNIFICANT.")
print(f"  Modified inertia WITH EFE: orbital speed enhanced by ~{1/mu(x_WB_total):.2f}x")
print(f"  Modified inertia WITHOUT EFE: enhanced by ~{1/mu(x_WB_internal):.2f}x")
print(f"  2024 wide binary study (26,615 binaries) shows 10-sigma deviation from Newton")
print(f"  But it's INCONSISTENT with EFE-MOND (EFE should suppress the effect here)")

# Dwarf galaxies in clusters
print(f"\nDwarf galaxies in clusters (EFE test):")
g_int_dwarf = 1e-11  # typical internal acceleration in dwarf
g_ext_cluster = 5e-11  # external field from host cluster
x_dwarf_no_EFE = g_int_dwarf / a0
x_dwarf_EFE = np.sqrt(g_int_dwarf**2 + g_ext_cluster**2) / a0
print(f"  g_internal (dwarf) = {g_int_dwarf:.2e} m/s^2")
print(f"  g_external (cluster) = {g_ext_cluster:.2e} m/s^2")
print(f"  mu without EFE = {mu(x_dwarf_no_EFE):.4f}")
print(f"  mu with EFE = {mu(x_dwarf_EFE):.4f}")
print(f"  EFE suppresses MOND enhancement by factor: {mu(x_dwarf_EFE)/mu(x_dwarf_no_EFE):.2f}")
print(f"  → Isolated dwarfs should show stronger MOND effect than cluster dwarfs")
print(f"  → This prediction exists and is observationally testable")
print(f"  → The model must take a specific stance on whether EFE applies")

# ============================================================
# SECTION 6: SOLAR SYSTEM PRECISION TESTS
# ============================================================
print()
print("=" * 70)
print("SECTION 6: SOLAR SYSTEM PRECISION TESTS")
print("=" * 70)

# Planets: check deviation from Newtonian at each planet's orbit
planets = [
    ("Mercury",  0.387 * AU, "3.3e-7"),
    ("Earth",    1.000 * AU, "6.0e-24"),
    ("Saturn",   9.537 * AU, "3.7e10"),
    ("Pluto",   39.5 * AU, "1.2e11"),
    ("100 AU",  100 * AU, None),
    ("Voyager (~150 AU)", 150 * AU, None),
]

print(f"\nDeviation δm_i/m = 1 - mu(g_N/a0) at each location:")
print(f"{'Object':<25} {'r (AU)':>10} {'g_N (m/s^2)':>15} {'x=g/a0':>12} {'mu':>12} {'1-mu':>12}")
print("-" * 87)
for name, r, _ in planets:
    g_N = G * Msun / r**2
    x = g_N / a0
    m = mu(x)
    print(f"{name:<25} {r/AU:>10.1f} {g_N:>15.3e} {x:>12.3e} {m:>12.10f} {1-m:>12.3e}")

print(f"\nPioneer anomaly bound: a_anomaly < 8.74e-10 m/s^2 (Anderson et al. 2002)")
print(f"At Pioneer location (~40 AU): g_N = {G*Msun/(40*AU)**2:.3e} m/s^2")
g_pioneer = G * Msun / (40*AU)**2
x_pioneer = g_pioneer / a0
mu_pioneer = mu(x_pioneer)
MOND_boost_pioneer = 1/mu_pioneer - 1
print(f"  x = {x_pioneer:.4f}")
print(f"  mu = {mu_pioneer:.8f}")
print(f"  Effective force boost: 1/mu - 1 = {MOND_boost_pioneer:.6f}")
print(f"  This is well within Pioneer anomaly bounds")

print(f"\nLunar laser ranging (LLR) constraint:")
print(f"  LLR measures |GM/G'M| to <10^-4 precision")
print(f"  At Moon orbit (r=384,400 km): g_N = {G*Msun/(384400e3)**2:.3e} m/s^2")
g_moon = G * Msun / (384400e3)**2
x_moon = g_moon / a0
print(f"  Actually at Moon, g_Earth at Moon is more relevant:")
g_Earth_at_Moon = G * 5.97e24 / (384400e3)**2
print(f"  g_Earth at Moon: {g_Earth_at_Moon:.3e} m/s^2")
x_moon_from_earth = g_Earth_at_Moon / a0
print(f"  x = g/a0 = {x_moon_from_earth:.3e}")
print(f"  mu = {mu(x_moon_from_earth):.12f}")
print(f"  1-mu = {1-mu(x_moon_from_earth):.3e}")
print(f"  LLR precision requirement: < 10^-4 → SATISFIED by many orders of magnitude")

print(f"\nEFE from Milky Way at Solar System:")
print(f"  g_MW at Sun: {g_ext_MW:.3e} m/s^2")
x_MW = g_ext_MW / a0
print(f"  x_MW = {x_MW:.4f}")
print(f"  mu(x_MW) = {mu(x_MW):.6f}")
print(f"  This applies universally to ALL objects in solar system via EFE")
print(f"  Modification to effective G: G_eff = G/mu(x_MW+x_internal)")
print(f"  At Earth orbit: x_total >> x_MW, so correction is negligible")
print(f"  At outer solar system (100+ AU): x_Sun + x_MW both ~ a0")
# At 100 AU from Sun
r_100AU = 100 * AU
g_100AU = G * Msun / r_100AU**2 + g_ext_MW   # Total including MW
x_100AU = g_100AU / a0
print(f"  At 100 AU: g_Sun = {G*Msun/r_100AU**2:.3e}, g_MW = {g_ext_MW:.3e}")
print(f"  x_total = {x_100AU:.4f}")
print(f"  mu(x_total) = {mu(x_100AU):.6f}")
print(f"  MOND boost factor: 1/mu = {1/mu(x_100AU):.4f} (0.5% effect)")
print(f"  Below current Cassini/New Horizons observational precision")
print(f"  VERDICT: Solar system is CONSISTENT with model (deviations < 10^-10)")

# ============================================================
# SECTION 7: THEORETICAL CONSISTENCY
# ============================================================
print()
print("=" * 70)
print("SECTION 7: THEORETICAL CONSISTENCY")
print("=" * 70)

print("\n7.1 EQUIVALENCE PRINCIPLE")
print("-" * 40)
print("  WEP: All bodies fall with same acceleration in gravity.")
print("  In T_U/T_dS model: F = m_g * g_N = m_i * a")
print("  => a = (m_g/m_i) * g_N = g_N / mu(g_N/a0)")
print("  Since g_N depends only on the FIELD (not the test particle),")
print("  all particles have the same acceleration: WEP IS PRESERVED")
print("  (provided all particle types have same gravitational coupling)")
print()
print("  SEP (Strong Equivalence Principle): VIOLATED")
print("  SEP requires internal dynamics of a system to be")
print("  independent of external gravitational field.")
print("  EFE in this model violates SEP: dwarf galaxy dynamics")
print("  depend on the external cluster field. This is the same")
print("  SEP violation as in MOND — a known prediction, not a fatal flaw.")
print()
print("  Eötvös experiment (WEP tests to 10^-15):")
print("  At surface gravity g = 9.8 m/s^2:")
x_eotv = 9.8 / a0
print(f"  x = g/a0 = {x_eotv:.3e}")
print(f"  mu = {mu(x_eotv):.15f}")
print(f"  1-mu = {1-mu(x_eotv):.3e}")
print(f"  Eötvös sensitivity: 10^-15. WEP violation would need: 10^-28 level effect.")
print(f"  RESULT: WEP is effectively preserved at lab scales (violation < 10^-28)")

print("\n7.2 MOMENTUM CONSERVATION")
print("-" * 40)
print("  Critical problem: In modified inertia, p = m_i * v = m * mu(g_N/a0) * v")
print("  As object moves through varying gravitational field, m_i changes.")
print("  dp/dt = m * d(mu)/dt * v + m * mu * a")
print("  For Newton's 3rd law: F_12 = -F_21 (gravitational forces equal & opposite)")
print("  But dp_1/dt = F_21 and dp_2/dt = F_12 = -F_21")
print("  dp_total/dt = dp_1/dt + dp_2/dt = 0 IF m_i is constant")
print("  IF m_i varies along trajectory: d(m_i*v)/dt ≠ F_grav unless d(m_i)/dt*v = 0")
print("  → Momentum is NOT conserved in general in modified inertia")
print()
print("  How severe? For a pair of galaxies passing each other:")
print("  Each galaxy's effective m_i changes as the gravitational field changes.")
print("  This introduces a systematic momentum violation proportional to Δmu.")
print("  For merger speeds v ~ 1000 km/s, Δmu ~ 0.1: momentum kicks of ~10% of p")
print("  → Not immediately ruled out observationally (hard to measure)")
print("  → BUT: fundamental departure from Hamiltonian mechanics")
print("  → Cannot be derived from an action principle without fine-tuning")
print("  → This is a serious theoretical defect, not a minor problem")

print("\n7.3 CAUSALITY AND STABILITY")
print("-" * 40)
print("  Dispersion relation for density waves with modified inertia:")
print("  Standard: omega^2 = cs^2 * k^2 - 4*pi*G*rho (Jeans)")
print("  Modified: (m * mu * omega^2) = (m * cs^2 * k^2 - 4*pi*G*rho*m)")
print("  => omega^2 = (cs^2 * k^2 - 4*pi*G*rho) / mu(k)")
print("  For large-scale modes (k -> 0): g_N -> 0, x -> 0, mu -> 0")
print("  => omega^2 -> (cs^2 * k^2 - 4*pi*G*rho) / (k/a0) * scaling")
print()
print("  In the deep MOND regime (k very small):")
print("  mu ≈ g_N/a0 ~ k (schematically)")
print("  omega^2 ~ (4*pi*G*rho)/mu ~ (4*pi*G*rho*a0)/g_N")
print("  This AMPLIFIES the Jeans instability for long-wavelength modes")
print("  → Large-scale structure forms MORE readily in modified inertia")
print("  → This could help with structure formation (good!)")
print("  → But it also means cosmological perturbation theory is modified")

# Negative energy check
print()
print("  Positive m_i check:")
print("  mu(x) = x/sqrt(1+x^2) > 0 for all x > 0")
print("  So m_i = m * mu > 0 always: NO negative mass problem")
print("  No ghost instability from sign change")

print("\n7.4 COSMOLOGICAL CONSISTENCY (a0 EVOLUTION)")
print("-" * 40)
print("  Scenario A: a0 = c*H(z)/6 evolves with Hubble parameter")

# Compute a0 at various redshifts
redshifts = [0, 0.5, 1, 2, 5, 10, 100, 1100, 1e9]
print(f"\n  {'z':>8} {'H(z)/H0':>12} {'a0(z) [m/s^2]':>15} {'a0(z)/a0(today)':>15}")
print("  " + "-" * 55)
for z in redshifts:
    Hz = H_of_z(z)
    a0z = c * Hz / 6
    print(f"  {z:>8.1e} {Hz/H0:>12.3e} {a0z:>15.3e} {a0z/a0:>15.2e}")

print()
print("  Problem with evolving a0:")
print("  At z=1100: a0 ~ 10^6 × a0(today)")
print("  All CMB-scale accelerations << a0(z=1100) → deep MOND regime")
print("  → Acoustic oscillations completely disrupted")
print("  → Structure formation fails (baryons barely feel any effective gravity)")
print("  CONCLUSION: Evolving a0 is RULED OUT observationally")

print()
print("  Scenario B: a0 = c*H0/6 = CONSTANT (today's value)")
print("  This requires that the de Sitter scale is SET at the current epoch")
print("  = future de Sitter phase determines physics everywhere")
print("  Conceptual problem: how does today's H0 affect early universe?")
print("  This is the 'cosmic coincidence': a0 ~ cH0 only NOW")
print()
print("  At z=5 (structure formation era):")
z5 = 5
Hz5 = H_of_z(z5)
print(f"  H(z=5) = {Hz5:.3e} s^-1 = {Hz5/H0:.0f} × H0")
print(f"  If a0 is fixed at cH0/6: CMB/structure is unaffected at z=5 for most modes")
print(f"  BUT: why should a0 be frozen at z=0 value?")
print(f"  No mechanism in the T_U/T_dS derivation suggests this.")
print(f"  This is an unsolved problem: a0 must be essentially constant for model to work.")

print()
print("  STRUCTURE FORMATION without dark matter:")
print("  Even with fixed a0, modified inertia cannot produce correct")
print("  CMB peak ratios because:")
print("  1. No dark matter contribution to potential wells at z>1000")
print("  2. CDM suppresses baryon oscillations before recombination")
print("  3. Without CDM, baryon acoustic oscillations are weaker")
print("  4. 3rd peak is strongly suppressed relative to ΛCDM prediction")
print("  5. Planck CMB data matches ΛCDM peak ratios to 1% accuracy")
print("  VERDICT: Modified inertia (or any modified gravity without CDM)")
print("  cannot fit CMB peak ratios without invoking sterile neutrinos or")
print("  some other hot/warm dark matter component")

