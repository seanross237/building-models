"""
Classicality Budget with Operationally Relevant (Thermal) Entropy
=================================================================

Computes the classicality budget R_delta <= S_eff / S_T - 1 for 6 physical systems
using actual thermodynamic entropy (S_eff) instead of the Bekenstein bound.

Exploration 005 of the classicality-budget mission.
"""

import numpy as np
from scipy.special import zeta as riemann_zeta

# ===========================================================================
# Physical Constants (SI units)
# ===========================================================================
k_B     = 1.380649e-23    # Boltzmann constant [J/K]
hbar    = 1.054571817e-34 # Reduced Planck constant [J·s]
h       = 2 * np.pi * hbar # Planck constant [J·s]
c       = 2.99792458e8    # Speed of light [m/s]
G       = 6.67430e-11     # Gravitational constant [m³ kg⁻¹ s⁻²]
sigma   = 5.670374419e-8  # Stefan-Boltzmann constant [W m⁻² K⁻⁴]
m_sun   = 1.989e30        # Solar mass [kg]
m_N2    = 4.652e-26       # Mass of N₂ molecule [kg]
m_air   = 4.811e-26       # Average mass of air molecule (~29 g/mol)
N_A     = 6.02214076e23   # Avogadro's number [mol⁻¹]
eV      = 1.602176634e-19 # Electron volt [J]

# Conversion factor: from J/K to bits
# S [bits] = S [J/K] / (k_B * ln 2)
LN2     = np.log(2)

def JK_to_bits(S_JK):
    """Convert entropy in J/K to bits."""
    return S_JK / (k_B * LN2)

def nats_to_bits(S_nats):
    """Convert entropy in nats (dimensionless, k_B=1) to bits."""
    return S_nats / LN2

def bekenstein_bound_bits(M_kg, R_m):
    """
    Bekenstein bound: S_max = 2πkRE / (ħc)
    Returns S_max in bits.
    E = Mc² for rest-mass energy.
    """
    E = M_kg * c**2
    S_bek_nats = 2 * np.pi * R_m * E / (hbar * c)
    return nats_to_bits(S_bek_nats)

def photon_entropy_bits(T_K, V_m3):
    """
    Thermal photon (blackbody) entropy in a volume V at temperature T.

    From the Planck distribution, the entropy density of a photon gas is:
      s = (16 σ T³) / (3 c)    [J / K / m³]

    This follows from:
      u = (4σ/c) T⁴  (energy density)
      s = (4/3) u / T = (16σ T³) / (3c)

    This can also be derived from the Planck distribution directly:
      s = (4π²/45) k_B⁴ T³ / (ħ³ c³) × k_B
    which gives the same result (verified numerically below).

    Returns S in bits.
    """
    s_density = (16 * sigma * T_K**3) / (3 * c)  # J/(K·m³)
    S_JK = s_density * V_m3
    return JK_to_bits(S_JK)

def photon_entropy_planck_bits(T_K, V_m3):
    """
    Alternative derivation: use Planck distribution directly.

    Entropy density from Bose-Einstein statistics for massless photons:
      s = (4π²/45) k_B⁴ T³ / (ħ³ c³) [in J/(K·m³)]

    This equals 16σT³/(3c) — two derivations should agree.
    """
    s_density = (4 * np.pi**2 / 45) * k_B**4 * T_K**3 / (hbar**3 * c**3)
    S_JK = s_density * V_m3
    return JK_to_bits(S_JK)

def photon_number_density(T_K):
    """
    Number of photons per unit volume at temperature T (thermal photons).
    n = 2 ζ(3) / π² × (k_B T / ħc)³
    where ζ(3) = Apéry's constant ≈ 1.20206
    """
    zeta3 = 1.2020569031595942  # Apéry's constant
    n = 2 * zeta3 / np.pi**2 * (k_B * T_K / (hbar * c))**3
    return n

def sackur_tetrode_bits(N, V_m3, T_K, m_kg):
    """
    Sackur-Tetrode formula for ideal monatomic gas entropy.

    S = N k_B [5/2 + ln(V/N × (2π m k_B T / h²)^(3/2))]

    For diatomic molecules (like N₂ or air), additional rotational degrees of freedom
    contribute: S_rot = N k_B × ln(T/θ_rot) + N k_B
    where θ_rot(N₂) ≈ 2.9 K (so at 300K, this adds ~ln(300/2.9) ≈ 4.6 per molecule)
    And vibrational contribution at 300K is small (θ_vib(N₂) ≈ 3374 K >> 300K).

    This function returns the translational contribution only (Sackur-Tetrode).
    Use diatomic_entropy_bits for the full result.
    """
    thermal_dB_wavelength = h / np.sqrt(2 * np.pi * m_kg * k_B * T_K)
    quantum_concentration = 1 / thermal_dB_wavelength**3  # 1/m³
    specific_volume = V_m3 / N  # m³ per particle

    log_term = np.log(specific_volume * quantum_concentration)
    S_per_particle_nats = 5/2 + log_term  # dimensionless (in nats)
    S_total_nats = N * S_per_particle_nats
    return nats_to_bits(S_total_nats)

def diatomic_gas_entropy_bits(N, V_m3, T_K, m_kg, theta_rot_K):
    """
    Full entropy of a diatomic ideal gas (translational + rotational + vibrational).

    S_trans = N k_B [5/2 + ln(V/N × (2π m k_B T / h²)^(3/2))]  (Sackur-Tetrode)
    S_rot   = N k_B [1 + ln(T / θ_rot)]  (high-T limit, valid when T >> θ_rot)
    S_vib   = negligible at 300K for N₂ (θ_vib ≈ 3374K >> 300K)

    Total: S = S_trans + S_rot
    """
    S_trans = sackur_tetrode_bits(N, V_m3, T_K, m_kg)

    # Rotational entropy (high-T limit)
    S_rot_nats = N * (1 + np.log(T_K / theta_rot_K))
    S_rot = nats_to_bits(S_rot_nats)

    return S_trans + S_rot

def hawking_temperature(M_kg):
    """Hawking temperature in Kelvin for a black hole of mass M."""
    return hbar * c**3 / (8 * np.pi * G * M_kg * k_B)

def schwarzschild_radius(M_kg):
    """Schwarzschild radius in meters."""
    return 2 * G * M_kg / c**2

def classicality_budget(S_eff_bits, S_T_bits):
    """
    R_delta <= S_eff / S_T - 1
    Returns R_delta (maximum redundancy supported by environment).
    If R_delta < 0, the environment cannot support even one copy.
    If 0 <= R_delta < 1, the environment can support up to 1 copy (barely).
    """
    return S_eff_bits / S_T_bits - 1.0

# ===========================================================================
# SYSTEM 1: Photon field in a room
# ===========================================================================
print("=" * 80)
print("SYSTEM 1: Photon field in a 1m³ room at T = 300K")
print("=" * 80)

T_room = 300.0     # K
V_room = 1.0       # m³
M_room = 1.0       # kg (rough mass for Bekenstein bound — a 1kg object)
R_room = 0.62      # m (radius of sphere with V=1m³)

S_photon_room = photon_entropy_bits(T_room, V_room)
S_photon_room_check = photon_entropy_planck_bits(T_room, V_room)
S_bek_room = bekenstein_bound_bits(M_room, R_room)
n_photons_room = photon_number_density(T_room) * V_room

print(f"  Temperature: {T_room} K")
print(f"  Volume: {V_room} m³")
print(f"  Number of thermal photons: {n_photons_room:.3e}")
print(f"  S_photon (Stefan-Boltzmann formula): {S_photon_room:.3e} bits")
print(f"  S_photon (Planck distribution formula): {S_photon_room_check:.3e} bits")
print(f"  Agreement between methods: {abs(S_photon_room - S_photon_room_check)/S_photon_room:.2e} relative error")
print(f"  S_Bekenstein (1kg, 0.62m): {S_bek_room:.3e} bits")
print(f"  Ratio S_photon / S_Bek: {S_photon_room / S_bek_room:.3e}")
print(f"  Entropy per photon: {S_photon_room / n_photons_room:.2f} bits/photon")

print(f"\n  Classicality budgets (using S_eff = S_photon):")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_photon_room, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")
print(f"\n  For comparison, Bekenstein-based budget:")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_bek_room, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# SYSTEM 2: Air molecules at STP
# ===========================================================================
print("\n" + "=" * 80)
print("SYSTEM 2: Air molecules in 1m³ at STP (T=293K, P=101.325 kPa)")
print("=" * 80)

T_air = 293.15     # K
V_air = 1.0        # m³
P_air = 101325.0   # Pa
N_air = P_air * V_air / (k_B * T_air)  # Loschmidt's number
M_air_total = N_air * m_air  # total mass of air

# Rotational constant for N₂: theta_rot ≈ 2.88 K
# For air (~80% N₂, ~20% O₂), weighted average:
# theta_rot(N₂) = 2.88 K, theta_rot(O₂) = 2.08 K
theta_rot_air = 0.8 * 2.88 + 0.2 * 2.08  # ≈ 2.72 K

S_air_trans = sackur_tetrode_bits(N_air, V_air, T_air, m_air)
S_air_full = diatomic_gas_entropy_bits(N_air, V_air, T_air, m_air, theta_rot_air)

# Bekenstein bound for 1m³ of air: use actual mass and radius
R_air = 0.62  # m (sphere of V=1m³)
S_bek_air = bekenstein_bound_bits(M_air_total, R_air)

print(f"  Temperature: {T_air} K, Pressure: {P_air} Pa")
print(f"  Number of molecules: {N_air:.3e}")
print(f"  Total mass: {M_air_total:.3f} kg")
print(f"  S_air (translational only, Sackur-Tetrode): {S_air_trans:.3e} bits")
print(f"  S_air (translational + rotational): {S_air_full:.3e} bits")
print(f"  Entropy per molecule: {S_air_full / N_air:.2f} bits/molecule")
print(f"  S_Bekenstein (air mass, 0.62m radius): {S_bek_air:.3e} bits")
print(f"  Ratio S_air_full / S_Bek: {S_air_full / S_bek_air:.3e}")

print(f"\n  Classicality budgets (using S_eff = S_air_full):")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_air_full, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")
print(f"\n  For comparison, Bekenstein-based budget:")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_bek_air, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# SYSTEM 3: CMB in the observable universe
# ===========================================================================
print("\n" + "=" * 80)
print("SYSTEM 3: CMB photons in the observable universe")
print("=" * 80)

T_CMB = 2.725       # K (CMB temperature)
R_Hubble = 4.4e26   # m (radius of observable universe ≈ 14 Gpc = 4.4×10²⁶ m)
V_univ = (4/3) * np.pi * R_Hubble**3  # m³

# Observable universe mass (total baryonic + dark matter energy):
# M_univ ≈ 3×10^54 kg (often quoted; includes dark matter ~27% + baryonic ~5%)
M_univ = 3.0e54     # kg

S_CMB = photon_entropy_bits(T_CMB, V_univ)
S_bek_univ = bekenstein_bound_bits(M_univ, R_Hubble)
n_CMB_per_m3 = photon_number_density(T_CMB)
N_CMB_total = n_CMB_per_m3 * V_univ

# Literature cross-check: S_CMB should be ~10^88 k_B = ~10^88 / ln(2) bits
print(f"  T_CMB = {T_CMB} K")
print(f"  Observable universe radius: {R_Hubble:.2e} m")
print(f"  Observable universe volume: {V_univ:.2e} m³")
print(f"  CMB photon number density: {n_CMB_per_m3:.1f} per cm³ = {n_CMB_per_m3*1e-6:.1f}/cm³")
print(f"  Total CMB photons: {N_CMB_total:.3e}")
print(f"  S_CMB: {S_CMB:.3e} bits")
print(f"  S_CMB in k_B: {S_CMB * LN2:.3e} (literature: ~3.6×10^88)")
print(f"  Entropy per CMB photon: {S_CMB / N_CMB_total:.2f} bits/photon")
print(f"  S_Bekenstein (universe): {S_bek_univ:.3e} bits")
print(f"  Ratio S_CMB / S_Bek: {S_CMB / S_bek_univ:.3e}")

# S_T for a cosmological fact: "galaxy cluster exists at a certain location"
# Position resolution: ~Mpc ≈ 3×10²² m. Number of Mpc³ in universe ~ 10^5
# So 1 bit per cluster position ~ 10 bits
S_T_cosmo = 10.0   # bits

print(f"\n  Classicality budgets (using S_eff = S_CMB):")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_CMB, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")
print(f"\n  For comparison, Bekenstein-based budget:")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_bek_univ, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# SYSTEM 4: Brain thermal environment
# ===========================================================================
print("\n" + "=" * 80)
print("SYSTEM 4: Brain thermal environment (37°C, 1.4 kg, 80% water)")
print("=" * 80)

T_brain = 310.15    # K (37°C)
M_brain = 1.4       # kg
water_fraction = 0.80
M_water_brain = M_brain * water_fraction  # kg

# Standard molar entropy of liquid water at 298K: 69.91 J/mol/K
# Temperature correction from 298K to 310K (slight increase):
# Cp(water) ≈ 75.3 J/mol/K (at constant pressure)
# ΔS = Cp × ln(T2/T1) per mole
S_molar_water_298K = 69.91  # J/mol/K
Cp_water = 75.3             # J/mol/K
S_molar_water_310K = S_molar_water_298K + Cp_water * np.log(T_brain / 298.15)

n_moles_water = (M_water_brain * 1000) / 18.015  # mol
S_brain_thermal_JK = n_moles_water * S_molar_water_310K
S_brain_thermal = JK_to_bits(S_brain_thermal_JK)

# Also compute photon entropy at brain temperature (EM decoherence)
V_brain = M_brain / 1040.0  # m³ (brain density ≈ 1040 kg/m³)
S_brain_photon = photon_entropy_bits(T_brain, V_brain)

# Bekenstein bound for brain
R_brain = (3*V_brain/(4*np.pi))**(1/3)
S_bek_brain = bekenstein_bound_bits(M_brain, R_brain)

# Neural S_T values:
# 1 bit per neuron firing: ~10^11 neurons → S_T ≈ 10^11 bits (full brain state)
# 1 bit per percept: ~10^6 bits (single conscious experience)
S_T_neuron = 1e11    # bits (full brain state)
S_T_percept = 1e6    # bits (single percept)

print(f"  T_brain = {T_brain} K ({T_brain-273.15:.1f}°C)")
print(f"  Volume: {V_brain*1e3:.2f} L")
print(f"  Water mass: {M_water_brain:.2f} kg = {n_moles_water:.1f} mol")
print(f"  S_molar(water, 298K) = {S_molar_water_298K:.2f} J/mol/K")
print(f"  S_molar(water, 310K) = {S_molar_water_310K:.2f} J/mol/K")
print(f"  S_brain_thermal (liquid water): {S_brain_thermal_JK:.2f} J/K = {S_brain_thermal:.3e} bits")
print(f"  S_brain_photon (thermal EM field): {S_brain_photon:.3e} bits")
print(f"  S_Bekenstein (1.4kg, {R_brain:.3f}m): {S_bek_brain:.3e} bits")
print(f"  Ratio S_brain_thermal / S_Bek: {S_brain_thermal / S_bek_brain:.3e}")
print(f"  Ratio S_brain_photon / S_Bek: {S_brain_photon / S_bek_brain:.3e}")

print(f"\n  Classicality budget for brain (using S_eff = S_brain_thermal):")
for S_T_bits in [1, S_T_percept, S_T_neuron]:
    label = f"{S_T_bits:.0e}"
    R = classicality_budget(S_brain_thermal, S_T_bits)
    print(f"    S_T = {label} bits → R_delta_max = {R:.3e}")
print(f"\n  Classicality budget (photon EM environment only):")
for S_T_bits in [1, S_T_percept, S_T_neuron]:
    label = f"{S_T_bits:.0e}"
    R = classicality_budget(S_brain_photon, S_T_bits)
    print(f"    S_T = {label} bits → R_delta_max = {R:.3e}")
print(f"\n  For comparison, Bekenstein-based budget:")
for S_T_bits in [1, S_T_percept, S_T_neuron]:
    label = f"{S_T_bits:.0e}"
    R = classicality_budget(S_bek_brain, S_T_bits)
    print(f"    S_T = {label} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# SYSTEM 5: Near a black hole horizon (solar-mass BH)
# ===========================================================================
print("\n" + "=" * 80)
print("SYSTEM 5: Near a solar-mass black hole horizon (Hawking radiation)")
print("=" * 80)

M_BH = m_sun           # kg
T_H = hawking_temperature(M_BH)
r_s = schwarzschild_radius(M_BH)
r_obs = 2 * r_s        # observer at 2× Schwarzschild radius

# Volume for encoding: choose a shell from r_s to 2r_s
# (the region where Hawking photons are relevant)
# For a sphere of radius r_s:
V_BH_shell = (4/3) * np.pi * r_s**3  # volume of sphere of radius r_s
V_BH_shell2 = (4/3) * np.pi * (2*r_s)**3 - (4/3)*np.pi*r_s**3  # shell r_s to 2r_s

# Entropy of Hawking photons in the shell
S_Hawking_V1 = photon_entropy_bits(T_H, V_BH_shell)
S_Hawking_V2 = photon_entropy_bits(T_H, V_BH_shell2)

# Black hole Bekenstein entropy (= Bekenstein = holographic, exactly at horizon)
# S_BH = A / (4 l_Planck²) in units of k_B
# = 4π r_s² / (4 × Gℏ/c³) = π r_s² c³ / (Gℏ)
l_Planck = np.sqrt(hbar * G / c**3)
A_BH = 4 * np.pi * r_s**2
S_BH_nats = A_BH / (4 * l_Planck**2)
S_BH_bits = nats_to_bits(S_BH_nats)

# Also compute Bekenstein bound for the shell region
# Energy in Hawking photons: use radiation energy density × volume
u_Hawking = (4 * sigma / c) * T_H**4
E_Hawking_shell = u_Hawking * V_BH_shell
S_bek_Hawking = bekenstein_bound_bits(E_Hawking_shell / c**2, r_s)  # use E/c² as effective mass

print(f"  Solar-mass BH: M = {M_BH:.2e} kg")
print(f"  Hawking temperature: T_H = {T_H:.3e} K")
print(f"  Schwarzschild radius: r_s = {r_s:.3e} m = {r_s/1000:.2f} km")
print(f"  BH entropy: S_BH = {S_BH_bits:.3e} bits (Bekenstein-Hawking)")
print(f"")
print(f"  Hawking photon entropy in sphere V = (4/3)π r_s³:")
print(f"    V_shell = {V_BH_shell:.3e} m³")
print(f"    S_Hawking = {S_Hawking_V1:.3e} bits")
print(f"  Hawking photon entropy in shell V = (4/3)π(2r_s)³ - (4/3)πr_s³:")
print(f"    V_shell2 = {V_BH_shell2:.3e} m³")
print(f"    S_Hawking = {S_Hawking_V2:.3e} bits")
print(f"  Ratio S_Hawking(V1) / S_BH = {S_Hawking_V1 / S_BH_bits:.3e}")
print(f"  Hawking photon number in V1: {photon_number_density(T_H) * V_BH_shell:.3e}")
print(f"")
print(f"  Classicality budget (using S_eff = S_Hawking in r_s sphere):")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_Hawking_V1, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")
print(f"\n  For comparison, Bekenstein-based budget (BH entropy):")
for S_T_bits in [1, 10, 100, 1e6]:
    R = classicality_budget(S_BH_bits, S_T_bits)
    print(f"    S_T = {S_T_bits:.0e} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# SYSTEM 6: Quantum computer register (1000 qubits at 10 mK)
# ===========================================================================
print("\n" + "=" * 80)
print("SYSTEM 6: Quantum computer register (1000 qubits, T = 10 mK)")
print("=" * 80)

T_QC = 0.010       # K (10 mK for dilution refrigerator base temperature)
n_qubits = 1000
V_QC = 1e-6        # m³ (roughly 1 cm × 1 cm × 1 cm chip area + packaging ≈ 1 cm³)

# Qubit frequency (superconducting transmon qubits): ω_q / (2π) ≈ 5 GHz
omega_q = 2 * np.pi * 5e9  # rad/s
E_q = hbar * omega_q       # energy spacing [J]
k_BT_QC = k_B * T_QC

print(f"  T = {T_QC*1000:.0f} mK")
print(f"  Qubit frequency: {omega_q/(2*np.pi)/1e9:.1f} GHz")
print(f"  Qubit energy gap: {E_q:.3e} J = {E_q/k_B:.4f} K (in temperature units)")
print(f"  k_B T / E_q = {k_BT_QC / E_q:.4f}  (→ 0 means well in ground state)")

# Environment 1: thermal photons at 10mK
S_QC_photon = photon_entropy_bits(T_QC, V_QC)

# Environment 2: phonons in the substrate (Si or Al)
# For silicon: Debye temperature θ_D ≈ 645 K
# At T << θ_D, phonon entropy goes as T³:
# S_Debye = (4π⁴/5) N k_B (T/θ_D)³
# where N = number of unit cells
# For Si: lattice constant a = 5.43 Å, so N/V ≈ 1/a³ * 2 (2 atoms per unit cell)
theta_D_Si = 645.0   # K (Debye temperature of Si)
a_Si = 5.43e-10      # m (Si lattice constant)
N_cells_per_m3 = 2 / a_Si**3  # 2 atoms per FCC primitive cell
N_phonon = N_cells_per_m3 * V_QC  # effective number of phonon modes

S_phonon_nats = (4 * np.pi**4 / 5) * N_phonon * (T_QC / theta_D_Si)**3
S_QC_phonon = nats_to_bits(S_phonon_nats)

# Total environment entropy
S_QC_total = S_QC_photon + S_QC_phonon

# Bekenstein bound for QC (using energy of the qubit states)
# Energy scale: qubits at 5 GHz, 1000 of them
# Use k_B × T × n_qubits as characteristic energy, plus RF electronics
E_QC = k_B * T_QC * n_qubits  # rough order of magnitude
R_QC = (V_QC)**(1/3)           # 1 cm = 0.01 m
M_QC = 0.001                    # 1 gram chip
S_bek_QC = bekenstein_bound_bits(M_QC, R_QC)

# S_T for qubit register: we want to record the state of N qubits
# The state of 1000 qubits in a classically verifiable way = 1000 bits
S_T_QC_1bit = 1.0
S_T_QC_full = n_qubits * 1.0  # 1000 bits for the full register

print(f"\n  Thermal photon entropy at {T_QC*1000:.0f}mK in {V_QC*1e6:.0f} cm³:")
print(f"    S_photon = {S_QC_photon:.3e} bits")
print(f"\n  Phonon entropy (Si substrate, Debye model, T << θ_D):")
print(f"    θ_D(Si) = {theta_D_Si} K")
print(f"    N_phonon modes = {N_phonon:.3e}")
print(f"    S_phonon = {S_QC_phonon:.3e} bits")
print(f"\n  Total environment entropy: {S_QC_total:.3e} bits")
print(f"  S_Bekenstein (1g chip, 1cm): {S_bek_QC:.3e} bits")
print(f"  Ratio S_QC_total / S_Bek: {S_QC_total / S_bek_QC:.3e}")

print(f"\n  Classicality budget (using S_eff = total environment entropy):")
for S_T_bits in [1, 10, 100, S_T_QC_full]:
    R = classicality_budget(S_QC_total, S_T_bits)
    label = f"{S_T_bits:.0e}"
    print(f"    S_T = {label} bits → R_delta_max = {R:.3e}")

# Can the thermal environment support even FULL redundancy of 1 qubit?
print(f"\n  CRITICAL: Can the environment support even 1 redundant copy of 1 qubit?")
print(f"    S_eff = {S_QC_total:.3e} bits")
print(f"    S_T (1 qubit) = 1 bit")
print(f"    R_max = {classicality_budget(S_QC_total, 1):.3e}")
if S_QC_total < 1.0:
    print(f"    >>> S_eff < 1 bit: environment CANNOT classicalize even 1 qubit!")
elif S_QC_total < n_qubits:
    print(f"    >>> S_eff < 1000 bits: environment cannot classicalize full register")
    print(f"    >>> Maximum classicalizable subset: ~{S_QC_total:.0e} qubits")

print(f"\n  For comparison, Bekenstein-based budget:")
for S_T_bits in [1, 10, 100, S_T_QC_full]:
    R = classicality_budget(S_bek_QC, S_T_bits)
    label = f"{S_T_bits:.0e}"
    print(f"    S_T = {label} bits → R_delta_max = {R:.3e}")

# ===========================================================================
# MASTER SUMMARY TABLE
# ===========================================================================
print("\n" + "=" * 80)
print("MASTER COMPARISON TABLE")
print("=" * 80)

systems = [
    ("Photon field (room, 300K, 1m³)",   S_photon_room,    S_bek_room,   "thermal photons"),
    ("Air molecules (STP, 1m³)",          S_air_full,       S_bek_air,    "Sackur-Tetrode gas"),
    ("CMB (observable universe)",         S_CMB,            S_bek_univ,   "thermal photons"),
    ("Brain thermal (310K, 1.4kg)",       S_brain_thermal,  S_bek_brain,  "liquid water entropy"),
    ("BH horizon (solar-mass, Hawking)",  S_Hawking_V1,     S_BH_bits,    "Hawking photons"),
    ("Quantum computer (10mK, 1000q)",    S_QC_total,       S_bek_QC,     "phonons + photons"),
]

S_T_ref = 1.0  # 1 bit reference fact

print(f"\n{'System':<40} {'S_eff (bits)':<14} {'S_Bek (bits)':<14} {'S_eff/S_Bek':<12} {'R_δ (S_T=1)':<14} {'R_δ (S_T=1e6)':<14}")
print("-" * 115)
for name, S_eff, S_bek, method in systems:
    ratio = S_eff / S_bek
    R_1 = classicality_budget(S_eff, 1.0)
    R_1e6 = classicality_budget(S_eff, 1e6)
    print(f"{name:<40} {S_eff:<14.3e} {S_bek:<14.3e} {ratio:<12.3e} {R_1:<14.3e} {R_1e6:<14.3e}")

print(f"\n{'System':<40} {'Is budget constraining?':<25} {'Notes'}")
print("-" * 90)
for name, S_eff, S_bek, method in systems:
    R_1 = classicality_budget(S_eff, 1.0)
    R_1e6 = classicality_budget(S_eff, 1e6)
    if R_1 < 0:
        status = "YES — no classicality!"
        note = f"S_eff = {S_eff:.2e} < 1 bit"
    elif R_1e6 < 10:
        status = "YES — budget tight"
        note = f"R_δ = {R_1e6:.2e} for 10^6 bit facts"
    elif R_1e6 < 1e6:
        status = "SOMEWHAT constraining"
        note = f"R_δ = {R_1e6:.2e} for 10^6 bit facts"
    else:
        status = "NO — generous"
        note = f"R_δ = {R_1e6:.2e} for 10^6 bit facts"
    print(f"{name:<40} {status:<25} {note}")

# ===========================================================================
# EXTRA: Sensitivity analysis — what temperature makes QC budget exactly 1?
# ===========================================================================
print("\n" + "=" * 80)
print("EXTRA: At what temperature does S_env = n_qubits (budget crosses classicality)?")
print("=" * 80)

# We want S_photon(T, V_QC) = n_qubits (1000 bits)
# S_photon = (16σT³V)/(3c) / (k_B ln2)
# → T³ = 1000 × k_B × ln2 × 3c / (16σV)
T_cross_photon = (n_qubits * k_B * LN2 * 3 * c / (16 * sigma * V_QC))**(1/3)
print(f"  For thermal photons in V = {V_QC*1e6:.0f} cm³:")
print(f"  T at which S_photon = 1000 bits: {T_cross_photon:.4f} K = {T_cross_photon*1000:.1f} mK")
print(f"  (Actual operating temperature: {T_QC*1000:.0f} mK)")
print(f"  Temperature ratio: {T_cross_photon / T_QC:.1f}×")
print(f"\n  This means: at {T_cross_photon*1000:.0f} mK, the environment BARELY has enough")
print(f"  entropy to store one copy of the full qubit register state.")
print(f"  Below this temperature, the environment cannot classicalize the register.")

# For phonons: solve S_phonon(T) = n_qubits
# S_phonon = (4π⁴/5) N_phonon (T/θ_D)³ / ln(2)
T_cross_phonon = theta_D_Si * (n_qubits * LN2 * 5 / (4 * np.pi**4 * N_phonon))**(1/3)
print(f"\n  For Si phonons in V = {V_QC*1e6:.0f} cm³ (Debye model):")
print(f"  T at which S_phonon = 1000 bits: {T_cross_phonon:.6e} K")
print(f"  (Actual operating temperature: {T_QC} K = {T_QC*1000:.0f} mK)")
print(f"  Temperature ratio: {T_cross_phonon / T_QC:.3e}×")

print("\n" + "=" * 80)
print("Done.")
print("=" * 80)
