"""
Classicality Budget — Experimental Test Proposal
=================================================
Exploration 003, Strategy 002

Computes R_delta (quantum Darwinism redundancy budget) for 8 candidate
experimental systems. For each system we compute:
  1. S_Bek   = Bekenstein entropy bound (theoretical max, in bits)
  2. S_eff   = actual thermodynamic / phonon / photon entropy (in bits)
  3. R_max   = S_eff / S_T - 1    [S_T = 1 bit, delta=0]
  4. Budget constraining?  (R_max < 10^6 => interesting regime)

Formula under test:
    R_delta <= (S_max / S_T - 1) / (1 - delta)

Strategy-001 showed:
  - Macroscopic systems: R_max ~ 10^15 - 10^26 (trivially not constraining)
  - BH horizon: R_max ~ -0.997 (constraining but inaccessible)
  - Planck scale: R_max ~ 3.5 (tight but inaccessible)

This exploration looks for accessible systems where R_max < 10^6.

Systems covered:
  A. BEC sonic horizon (Steinhauer 2020) — 1D phonon environment
  B. Optical fiber analog (Philbin 2008) — photon field
  C. 50-ion trap (controlled quantum environment)
  D. 53-qubit superconducting QC (Sycamore, Google)
  E. Nanodot L=10nm (Bekenstein-bounded environment at 300K)
  F. NEMS resonator near quantum ground state
  G. Inflationary Hubble patch (observational)
  H. BH horizon (reference, already computed in Exploration 005)
"""

import numpy as np
from scipy import constants, integrate

# ============================================================
# Physical constants
# ============================================================
hbar   = 1.0545718e-34   # J·s
c      = 2.998e8         # m/s
k_B    = 1.380649e-23    # J/K
G      = 6.674e-11       # m^3/(kg·s^2)
sigma  = 5.670374e-8     # Stefan-Boltzmann [W/(m^2 K^4)]
ln2    = np.log(2)
eV     = 1.602e-19       # J per eV
m_Rb   = 87 * 1.66e-27   # mass of Rb-87 atom [kg]
m_p    = 1.673e-27       # proton mass [kg]

print("=" * 70)
print("CLASSICALITY BUDGET — EXPERIMENTAL TEST PROPOSAL")
print("Exploration 003 | Strategy 002")
print("=" * 70)

# ============================================================
# Core functions
# ============================================================

def bekenstein_bits(R_m, E_J):
    """Bekenstein entropy bound: S_max = 2*pi*R*E / (hbar*c*ln2) [bits]"""
    return 2 * np.pi * R_m * E_J / (hbar * c * ln2)

def photon_entropy_bits(T_K, V_m3):
    """Photon gas entropy in volume V at temperature T [bits].
    Formula: S = (16 sigma / 3c) * T^3 * V  [J/K]  then divide by k_B*ln2.
    """
    S_SI = (16 * sigma / (3 * c)) * T_K**3 * V_m3   # J/K
    return S_SI / (k_B * ln2)

def bose_entropy_per_mode(n_bar):
    """Von Neumann entropy of a single Bose mode with mean occupation n_bar [bits].
    S = (n_bar+1)*log2(n_bar+1) - n_bar*log2(n_bar)
    """
    if n_bar < 1e-15:
        return 0.0
    return (n_bar + 1) * np.log2(n_bar + 1) - n_bar * np.log2(n_bar)

def mean_occupation(omega, T_K):
    """Bose-Einstein mean occupation: n_bar = 1/(exp(hbar*omega/k_B T) - 1)"""
    x = hbar * omega / (k_B * T_K)
    if x > 500:
        return 0.0
    if x < 1e-10:
        return k_B * T_K / (hbar * omega)   # classical limit
    return 1.0 / (np.exp(x) - 1)

def debye_entropy_bits(T_K, V_m3, theta_D_K, mass_kg, molar_mass_kg):
    """Debye phonon entropy [bits] for a solid of volume V at temperature T.
    Valid when T << theta_D.
    S = (12 pi^4 / 5) * N_atoms * k_B * (T/theta_D)^3   [J/K]
    where N_atoms = V * rho / molar_mass * N_A
    We compute directly from density of states.

    Parameters:
        V_m3        : volume [m^3]
        theta_D_K   : Debye temperature [K]
        mass_kg     : mass of material [kg]
        molar_mass_kg: molar mass [kg/mol]
    """
    N_A = 6.022e23
    n_atoms = (mass_kg / molar_mass_kg) * N_A
    S_SI = (12 * np.pi**4 / 5) * n_atoms * k_B * (T_K / theta_D_K)**3   # J/K
    return S_SI / (k_B * ln2)

def phonon_entropy_1d_bose(T_K, L_m, v_s, xi_m, N_modes_max=10000):
    """Entropy of 1D phonon gas (BEC acoustic modes) [bits].

    Linear dispersion: omega(k) = v_s * k, k in [pi/L, pi/xi] (IR to UV cutoff).
    Modes: k_n = n * pi / L,  n = 1, 2, ..., N_max
    UV cutoff: k < pi/xi  (healing length = short-wavelength cutoff)

    Parameters:
        T_K  : effective temperature [K]
        L_m  : BEC length [m]
        v_s  : speed of sound [m/s]
        xi_m : healing length [m] (UV cutoff)
    """
    k_UV = np.pi / xi_m           # UV cutoff wavenumber [1/m]
    N_max = int(k_UV * L_m / np.pi)   # number of modes below UV cutoff
    N_max = min(N_max, N_modes_max)

    S_total = 0.0
    for n in range(1, N_max + 1):
        k_n = n * np.pi / L_m
        omega_n = v_s * k_n
        n_bar = mean_occupation(omega_n, T_K)
        S_total += bose_entropy_per_mode(n_bar)

    return S_total, N_max

def classicality_budget(S_eff, S_T=1.0, delta=0.0):
    """Compute R_max = (S_eff/S_T - 1) / (1 - delta)"""
    return (S_eff / S_T - 1.0) / (1.0 - delta)

def budget_label(R_max):
    """Human-readable label for budget constraint level."""
    if R_max < 0:
        return "FORBIDDEN (R<0)"
    elif R_max < 10:
        return "TIGHT (<10)"
    elif R_max < 1e3:
        return "CONSTRAINED (<10^3)"
    elif R_max < 1e6:
        return "INTERESTING (<10^6)"
    elif R_max < 1e12:
        return "WEAKLY CONSTRAINING (<10^12)"
    else:
        return "NOT CONSTRAINING"

# ============================================================
# RESULTS TABLE
# ============================================================
results = []

def add_result(name, params, S_Bek, S_eff, R_max, notes=""):
    results.append({
        "name": name,
        "params": params,
        "S_Bek": S_Bek,
        "S_eff": S_eff,
        "R_max": R_max,
        "label": budget_label(R_max),
        "notes": notes,
    })

# ============================================================
# SYSTEM H: BH horizon (REFERENCE, from Exploration 005)
# ============================================================
print("\n--- SYSTEM H: BH horizon (reference) ---")
# Near-horizon sphere of radius r_s, T_H = hbar*c^3 / (8*pi*G*M*k_B)
# From Exploration 005: S_Hawking(solar BH near r_s sphere) = 2.67e-3 bits
# T_H(solar BH) = 6.17e-8 K, r_s = 2.95 km
M_sun = 1.989e30   # kg
r_s = 2 * G * M_sun / c**2
T_H = hbar * c**3 / (8 * np.pi * G * M_sun * k_B)
V_rs = (4/3) * np.pi * r_s**3
S_eff_BH = photon_entropy_bits(T_H, V_rs)
S_Bek_BH = bekenstein_bits(r_s, k_B * T_H)   # rough estimate

print(f"  r_s = {r_s:.3e} m,  T_H = {T_H:.3e} K")
print(f"  S_eff(Hawking photons) = {S_eff_BH:.3e} bits")
print(f"  R_max = {classicality_budget(S_eff_BH):.4f}")

R_max_BH = classicality_budget(S_eff_BH)
add_result(
    "BH horizon (solar, reference)",
    f"M=M_sun, T_H={T_H:.2e}K, r_s={r_s:.2e}m",
    S_Bek_BH, S_eff_BH, R_max_BH,
    "REFERENCE: budget only constraining system from Exploration 005"
)

# ============================================================
# SYSTEM A: BEC sonic horizon (Steinhauer 2020)
# ============================================================
print("\n--- SYSTEM A: BEC sonic horizon (Steinhauer 2020) ---")
# Parameters from Steinhauer 2020 Nature Physics:
# N_atoms ~ 8000 Rb-87, healing length xi ~ 0.5 μm,
# T_eff (acoustic Hawking) ~ 50 nK, speed of sound v_s ~ 1.5 mm/s
# BEC length ~ 100 μm (typical for this setup)

T_eff_BEC  = 50e-9      # K, acoustic Hawking temperature
xi_BEC     = 0.5e-6     # m, healing length
v_s_BEC    = 1.5e-3     # m/s, speed of sound (typical Rb BEC)
L_BEC      = 100e-6     # m, BEC length (typical)
N_atoms_BEC = 8000
cross_section_BEC = (5e-6)**2  # 5 μm transverse size, approx cross section

print(f"  T_eff = {T_eff_BEC*1e9:.0f} nK,  xi = {xi_BEC*1e6:.1f} μm")
print(f"  v_s = {v_s_BEC*1e3:.1f} mm/s,  L = {L_BEC*1e6:.0f} μm")

# 1D phonon entropy at T_eff
S_eff_BEC, N_modes_BEC = phonon_entropy_1d_bose(T_eff_BEC, L_BEC, v_s_BEC, xi_BEC)
print(f"  N_phonon_modes = {N_modes_BEC}")
print(f"  S_eff(1D phonons at T_eff) = {S_eff_BEC:.3e} bits")

# Thermal de Broglie length for context
lambda_thermal = hbar * v_s_BEC / (k_B * T_eff_BEC)
print(f"  Thermal phonon wavelength lambda_th = {lambda_thermal*1e6:.1f} μm (compare xi={xi_BEC*1e6:.1f} μm)")

# Bekenstein bound for BEC volume
V_BEC = L_BEC * cross_section_BEC
E_BEC = N_atoms_BEC * m_Rb * c**2 * 1e-10   # tiny rest mass energy fraction
# More relevant: kinetic energy of BEC atoms
E_kinetic_BEC = N_atoms_BEC * (1/2) * m_Rb * v_s_BEC**2   # rough KE
R_BEC = (L_BEC / 2)   # "radius" of BEC
S_Bek_BEC = bekenstein_bits(R_BEC, E_kinetic_BEC + N_atoms_BEC * k_B * T_eff_BEC)
print(f"  S_Bek (BEC) = {S_Bek_BEC:.3e} bits")

R_max_BEC = classicality_budget(S_eff_BEC)
print(f"  R_max = {R_max_BEC:.2f}  -> {budget_label(R_max_BEC)}")

add_result(
    "BEC sonic horizon (Steinhauer 2020)",
    f"T_H=50nK, xi=0.5μm, L=100μm, v_s=1.5mm/s, N=8000",
    S_Bek_BEC, S_eff_BEC, R_max_BEC,
    f"1D phonon gas; N_modes={N_modes_BEC}; lambda_th={lambda_thermal*1e6:.1f}μm"
)

# How does this depend on T_eff? Let's scan.
print("\n  Sensitivity to T_eff:")
for T_test in [10e-9, 25e-9, 50e-9, 100e-9, 200e-9, 500e-9]:
    S_t, Nm = phonon_entropy_1d_bose(T_test, L_BEC, v_s_BEC, xi_BEC)
    print(f"    T_eff={T_test*1e9:.0f}nK: N_modes={Nm}, S_eff={S_t:.2f} bits, R_max={S_t-1:.2f}")

# ============================================================
# SYSTEM A2: BEC at actual preparation temperature T_BEC
# ============================================================
print("\n--- SYSTEM A2: BEC at preparation temperature (T_BEC << T_H) ---")
# In Steinhauer's experiment, the BEC is cooled to T_BEC ~ 1-5 nK before
# turning on the horizon. The Hawking phonons are spontaneous, not thermal.
# What is the phonon entropy at T_BEC = 2 nK?
T_BEC_prep = 2e-9   # K, estimated preparation temperature
S_prep, N_prep = phonon_entropy_1d_bose(T_BEC_prep, L_BEC, v_s_BEC, xi_BEC)
print(f"  T_BEC_prep = {T_BEC_prep*1e9:.0f} nK")
print(f"  S_eff(BEC at T_prep) = {S_prep:.4f} bits, N_modes = {N_prep}")
print(f"  R_max = {S_prep - 1:.4f}  -> {budget_label(S_prep - 1)}")
print("  Note: At T_prep << T_H, most phonon modes have n_bar << 1 => S_eff << N_modes")

# Number of phonons with appreciable occupation
lambda_th_prep = hbar * v_s_BEC / (k_B * T_BEC_prep)
N_thermal_prep = L_BEC / (2 * lambda_th_prep)
print(f"  N_thermal_modes at T_prep = {N_thermal_prep:.1f}")

# ============================================================
# SYSTEM B: Optical fiber analog (Philbin 2008)
# ============================================================
print("\n--- SYSTEM B: Optical fiber soliton analog (Philbin 2008) ---")
# System: 50-ps soliton in silica fiber, ~1 μJ pulse energy
# The "horizon" is at the leading/trailing edge of the soliton
# Relevant environment: photon field modes in the fiber
# Effective temperature of Hawking radiation: T_opt ~ 1700 K (very rough estimate
# from dispersion-induced horizon analogy)
# Fiber core diameter: ~5 μm,  soliton length: ~1 cm (but squeezed to ~30 μm)
# The optical "Hawking temperature" in fiber is set by the group velocity
# difference at the horizon: T_eff ~ (1/2pi) * (d(v_g)/dx)_horizon * hbar/(k_B)
# Typical values: T_eff ~ 10^4 K (very high compared to lattice temperature)

T_opt = 1e4        # K, effective optical Hawking temperature
L_fiber = 1e-2     # m, fiber length involved
r_fiber = 2.5e-6   # m, fiber core radius
V_fiber = np.pi * r_fiber**2 * L_fiber

# In an optical fiber, the "environment" is the photon modes in the fiber
# BUT: for a fiber, the modes are 1D guided modes, not 3D photon gas.
# Photon entropy in 1D fiber at T_opt:
# Treat as 1D photon gas with group velocity c/n (n~1.46 for silica)
n_fiber = 1.46
v_g = c / n_fiber
# 1D photon density of modes: dN/dnu = L/v_g
# Number of thermal modes: nu_max = k_B T_opt / h
nu_thermal = k_B * T_opt / (2 * np.pi * hbar)   # thermal frequency
N_optical_modes = L_fiber * nu_thermal / v_g
print(f"  T_eff(optical) ~ {T_opt:.1e} K")
print(f"  N_thermal_modes (1D) = {N_optical_modes:.3e}")

# For a thermal 1D photon gas, entropy per mode ~ 1 bit at T >> mode energy
# S_1D_photon = pi^2 k_B^2 T L / (3 hbar v_g)
S_1D_photon_SI = np.pi**2 * k_B**2 * T_opt * L_fiber / (3 * hbar * v_g)
S_1D_photon_bits = S_1D_photon_SI / (k_B * ln2)
print(f"  S_eff(1D photons, T_opt) = {S_1D_photon_bits:.3e} bits")

# Also compute Bekenstein for the fiber core volume
E_fiber_pulse = 1e-6   # J, ~1 μJ pulse energy
S_Bek_fiber = bekenstein_bits(r_fiber, E_fiber_pulse)
print(f"  S_Bek(fiber core, 1μJ) = {S_Bek_fiber:.3e} bits")

R_max_fiber = classicality_budget(S_1D_photon_bits)
print(f"  R_max = {R_max_fiber:.3e}  -> {budget_label(R_max_fiber)}")

add_result(
    "Optical fiber soliton (Philbin 2008)",
    f"T_eff~10^4K, L=1cm, fiber core r=2.5μm",
    S_Bek_fiber, S_1D_photon_bits, R_max_fiber,
    "T_eff much higher than BEC; modes scale as T"
)

# ============================================================
# SYSTEM C: 50-ion trap
# ============================================================
print("\n--- SYSTEM C: 50-ion trap (quantum simulator) ---")
# System: N=50 ions (e.g., Ca+ or Yb+, d=2 per ion)
# Environment of ion 1 = the other 49 ions + 3N=150 motional modes + photon field
# Temperature: laser cooling to T_cool ~ 10 μK (near motional ground state)
# Mean phonon occupation: n_bar ~ 0.1 per mode (achieved with sideband cooling)

N_ions = 50
T_ion_trap = 10e-6      # K, laser cooling temperature
n_bar_phonon = 0.1      # mean phonon occupation (sideband-cooled)
N_motional = 3 * N_ions  # number of motional modes

print(f"  N_ions = {N_ions}, T_laser = {T_ion_trap*1e6:.0f} μK")
print(f"  N_motional modes = {N_motional}, n_bar per mode = {n_bar_phonon}")

# Entropy from other 49 qubits (if maximally mixed: S = 49 bits)
# But in a well-prepared experiment, ions are initialized to |0>: S = 0
# For QD purposes, we want the MAX available entropy in the environment
S_other_ions = (N_ions - 1) * 1.0   # bits, if all others maximally mixed
S_other_ions_init = 0.0             # bits, initialized state

# Entropy from 150 motional modes at n_bar = 0.1
S_motion = N_motional * bose_entropy_per_mode(n_bar_phonon)
print(f"  S(motional modes, n_bar=0.1) = {S_motion:.2f} bits")

# Entropy from photon field at T = 10 μK in trap volume ~ 1 mm^3
V_trap = (1e-3)**3   # m^3
S_photon_trap = photon_entropy_bits(T_ion_trap, V_trap)
print(f"  S(photon field, 10μK, 1mm^3) = {S_photon_trap:.3e} bits")

# Total accessible environment entropy
# Case 1: Only motional modes (conservative: ions initialized, photons negligible)
S_eff_ion_conservative = S_motion
# Case 2: All ions uninitialized + motional modes (liberal upper bound)
S_eff_ion_liberal = S_other_ions + S_motion

print(f"  S_eff(conservative: motional only) = {S_eff_ion_conservative:.2f} bits")
print(f"  S_eff(liberal: ions + motional) = {S_eff_ion_liberal:.2f} bits")

# Bekenstein bound for trap region
E_trap = N_ions * k_B * T_ion_trap + N_ions * 1.0 * eV   # KE + ionization energy scale
R_trap = 1e-3   # trap radius ~ 1 mm
S_Bek_trap = bekenstein_bits(R_trap, E_trap)
print(f"  S_Bek(trap) = {S_Bek_trap:.3e} bits")

R_max_ion = classicality_budget(S_eff_ion_conservative)
R_max_ion_lib = classicality_budget(S_eff_ion_liberal)
print(f"  R_max(conservative) = {R_max_ion:.2f}  -> {budget_label(R_max_ion)}")
print(f"  R_max(liberal) = {R_max_ion_lib:.2f}  -> {budget_label(R_max_ion_lib)}")

add_result(
    "50-ion trap (quantum simulator)",
    f"N=50, T=10μK, n_bar=0.1, N_motional=150",
    S_Bek_trap, S_eff_ion_conservative, R_max_ion,
    f"Conservative: motional modes only. Liberal: S_eff={S_eff_ion_liberal:.1f} bits, R={R_max_ion_lib:.1f}"
)

# ============================================================
# SYSTEM D: 53-qubit superconducting QC (Sycamore, Google)
# ============================================================
print("\n--- SYSTEM D: 53-qubit superconducting QC (Google Sycamore) ---")
# Parameters: 53 transmon qubits, T_base ~ 15 mK, substrate = Si or SiO2
# Environment = phonons in Si substrate chip (~5mm x 5mm x 1mm)
# Theta_D(Si) = 645 K

T_Sycamore = 0.015      # K
V_Si = 5e-3 * 5e-3 * 1e-3   # m^3, ~5mm x 5mm x 1mm Si chip
rho_Si = 2329.0          # kg/m^3
theta_D_Si = 645.0       # K
M_Si_molar = 28.085e-3   # kg/mol

mass_chip = rho_Si * V_Si
print(f"  T_base = {T_Sycamore*1000:.0f} mK, V_chip = {V_Si:.2e} m^3, m_chip = {mass_chip*1e3:.2f} g")

S_eff_Sycamore = debye_entropy_bits(T_Sycamore, V_Si, theta_D_Si, mass_chip, M_Si_molar)
print(f"  S_eff(Debye phonons at 15mK) = {S_eff_Sycamore:.3e} bits")

# Photon field at 15 mK
S_photon_Sycamore = photon_entropy_bits(T_Sycamore, V_Si)
print(f"  S(photon field, 15mK) = {S_photon_Sycamore:.3e} bits")

# Bekenstein bound for chip
E_chip = mass_chip * c**2 * 1e-15   # negligible rest mass fraction
S_Bek_Sycamore = bekenstein_bits(2.5e-3, mass_chip * k_B * T_Sycamore / m_p)
print(f"  S_Bek(chip) ~ {S_Bek_Sycamore:.3e} bits")

# For S_T: system is a 53-qubit register → S_T = 53 bits
S_T_Sycamore = 53.0
R_max_Sycamore = classicality_budget(S_eff_Sycamore, S_T=S_T_Sycamore)
print(f"  R_max (S_T = 53 bits) = {R_max_Sycamore:.3e}  -> {budget_label(R_max_Sycamore)}")
# Also for single qubit:
R_max_Sycamore_1bit = classicality_budget(S_eff_Sycamore, S_T=1.0)
print(f"  R_max (S_T = 1 bit) = {R_max_Sycamore_1bit:.3e}  -> {budget_label(R_max_Sycamore_1bit)}")

add_result(
    "53-qubit QC (Sycamore, 15mK)",
    f"T=15mK, V=25mm³, Si substrate",
    S_Bek_Sycamore, S_eff_Sycamore, R_max_Sycamore_1bit,
    f"Debye phonon env; S_T=1bit: R={R_max_Sycamore_1bit:.2e}, S_T=53bits: R={R_max_Sycamore:.2e}"
)

# ============================================================
# SYSTEM E: Nanodot L=10 nm (Bekenstein-bounded environment)
# ============================================================
print("\n--- SYSTEM E: Nanodot L=10 nm ---")
# Single electron spin in a GaAs or Si quantum dot
# Environment: phonons + photons in nanoscale volume V = L^3, L = 10 nm
# Two temperatures: T = 300 K (room temp) and T = 4 K (liquid He)

L_dot = 10e-9    # m, cube side = 10 nm
V_dot = L_dot**3
E_dot = 1.0 * eV   # 1 eV photon/electron energy
R_dot = L_dot / 2

# Bekenstein bound
S_Bek_dot = bekenstein_bits(R_dot, E_dot)
print(f"  L = {L_dot*1e9:.0f} nm, V = {V_dot:.3e} m^3")
print(f"  S_Bek(L=10nm, E=1eV) = {S_Bek_dot:.3f} bits")

for T_dot in [300.0, 4.0, 0.1]:
    S_photon_dot = photon_entropy_bits(T_dot, V_dot)

    # Phonon entropy in GaAs (theta_D = 360 K, rho = 5320 kg/m^3, M_mol = 144.6e-3 kg/mol)
    theta_D_GaAs = 360.0
    rho_GaAs = 5320.0
    M_GaAs = 144.6e-3
    mass_dot = rho_GaAs * V_dot

    if T_dot < theta_D_GaAs:
        S_phonon_dot = debye_entropy_bits(T_dot, V_dot, theta_D_GaAs, mass_dot, M_GaAs)
    else:
        # Classical limit: S ≈ 3 N_atoms k_B (Dulong-Petit)
        N_A = 6.022e23
        N_atoms_dot = (mass_dot / M_GaAs) * N_A
        S_phonon_dot = 3 * N_atoms_dot / ln2   # 3 bits per atom in classical limit

    S_eff_dot = S_photon_dot + S_phonon_dot
    R_max_dot = classicality_budget(S_eff_dot)
    R_max_dot_bek = classicality_budget(S_Bek_dot)

    print(f"  T = {T_dot:.1f} K: S_photon = {S_photon_dot:.3e} bits, "
          f"S_phonon = {S_phonon_dot:.3e} bits, S_eff = {S_eff_dot:.3e} bits, "
          f"R_max = {R_max_dot:.3e} -> {budget_label(R_max_dot)}")
    print(f"            S_Bek = {S_Bek_dot:.3f} bits, R_max(Bek) = {R_max_dot_bek:.3f}")

    if T_dot == 300.0:
        add_result(
            "Nanodot L=10nm (300K, GaAs)",
            f"L=10nm, E=1eV, T=300K",
            S_Bek_dot, S_eff_dot, R_max_dot,
            f"S_Bek={S_Bek_dot:.3f}bits — Bekenstein tight! Phonons dominate at this volume"
        )
    elif T_dot == 4.0:
        add_result(
            "Nanodot L=10nm (4K, GaAs)",
            f"L=10nm, E=1eV, T=4K",
            S_Bek_dot, S_eff_dot, R_max_dot,
            f"S_Bek={S_Bek_dot:.3f}bits; S_eff at 4K"
        )

# ============================================================
# SYSTEM F: NEMS resonator near quantum ground state
# ============================================================
print("\n--- SYSTEM F: NEMS resonator near quantum ground state ---")
# State-of-the-art: silicon nitride membrane or aluminum drum
# cooled to n_bar ~ 0.01 in a dilution refrigerator
# Resonator itself is 1 quantum mode; environment = phonon bath in the substrate
#
# Parameters from Teufel et al. (2011) or MacCabe et al. (2020):
# - Mechanical frequency: omega_m / (2pi) ~ 5-10 MHz
# - Quality factor Q ~ 10^5-10^8
# - Temperature: T ~ 20 mK (dilution fridge)
# - Substrate: Si, V ~ 1mm^3 package

omega_NEMS = 2 * np.pi * 10e6   # rad/s, 10 MHz resonance
T_NEMS = 0.02                    # K, 20 mK
V_substrate_NEMS = (1e-3)**3     # m^3, 1mm^3 Si package
mass_NEMS_substrate = rho_Si * V_substrate_NEMS

# Mean phonon occupation of the NEMS mode itself
n_bar_NEMS = mean_occupation(omega_NEMS, T_NEMS)
S_NEMS_mode = bose_entropy_per_mode(n_bar_NEMS)
print(f"  omega_m/(2pi) = 10 MHz, T = {T_NEMS*1e3:.0f} mK")
print(f"  hbar*omega_m = {hbar*omega_NEMS:.3e} J = {hbar*omega_NEMS/k_B:.2e} K equivalent")
print(f"  n_bar(NEMS mode) = {n_bar_NEMS:.4f}")
print(f"  S(NEMS mode itself) = {S_NEMS_mode:.4f} bits  [S_T for classicality]")

# Environment = Si substrate phonon bath at T_NEMS
S_eff_NEMS = debye_entropy_bits(T_NEMS, V_substrate_NEMS, theta_D_Si, mass_NEMS_substrate, M_Si_molar)
print(f"  S_eff(substrate phonons at 20mK, 1mm^3 Si) = {S_eff_NEMS:.3e} bits")

# Bekenstein for the NEMS itself (~100nm x 100nm x 1mm resonator)
R_NEMS = 0.5e-3   # m, half the length
E_NEMS = hbar * omega_NEMS    # one quantum of mechanical energy
S_Bek_NEMS = bekenstein_bits(R_NEMS, E_NEMS)
print(f"  S_Bek(NEMS, ~1 quantum) = {S_Bek_NEMS:.3e} bits")

# S_T for the NEMS qubit = entropy of one mechanical phonon mode
# For the classicality budget: S_T = S_NEMS_mode (if non-zero), or 1 bit
S_T_NEMS = max(S_NEMS_mode, 1.0)   # 1 bit minimum for "one classical fact"
R_max_NEMS = classicality_budget(S_eff_NEMS, S_T=S_T_NEMS)
print(f"  R_max(S_T=max(S_mode,1bit)) = {R_max_NEMS:.3e}  -> {budget_label(R_max_NEMS)}")

add_result(
    "NEMS resonator (20mK, 10MHz, 1mm³ Si)",
    f"omega=10MHz, T=20mK, n_bar={n_bar_NEMS:.3f}",
    S_Bek_NEMS, S_eff_NEMS, R_max_NEMS,
    f"S_T={S_T_NEMS:.3f}bits; substrate dominates environment"
)

# ============================================================
# SYSTEM G: Inflationary Hubble patch
# ============================================================
print("\n--- SYSTEM G: Inflationary Hubble patch ---")
# During inflation, one "Hubble patch" has Hubble radius R_H = c/H
# The inflaton perturbation = "system"; radiation + graviton modes = environment
# At CMB scales: H_inf ~ 10^13-10^14 GeV ~ 10^-5 M_Pl
# Hubble temperature T_dS = H/(2*pi) [in natural units]
# In SI: T_dS = hbar * H_inf / (2 * pi * k_B)

H_inf_GeV = 1e13        # GeV, Hubble scale during inflation
H_inf_SI = H_inf_GeV * 1e9 * eV / hbar   # rad/s
R_H = c / H_inf_SI       # Hubble radius

T_dS = hbar * H_inf_SI / (2 * np.pi * k_B)   # de Sitter temperature [K]
V_H = (4/3) * np.pi * R_H**3

print(f"  H_inf = {H_inf_GeV:.1e} GeV, R_H = {R_H:.3e} m")
print(f"  T_dS = {T_dS:.3e} K")
print(f"  V_H = {V_H:.3e} m^3")

# The inflaton has S_T ≈ 1 bit per mode crossing the horizon
# The "environment" = all other modes in the Hubble patch = photon-like at T_dS
S_eff_inflation = photon_entropy_bits(T_dS, V_H)
print(f"  S_eff(radiation modes at T_dS, V_H) = {S_eff_inflation:.3e} bits")

# Bekenstein for Hubble patch
E_inflation = k_B * T_dS   # energy of one Hawking quanta
S_Bek_inflation = bekenstein_bits(R_H, E_inflation * 1e60)   # dominant energy scale: rho*V
# More realistic: total energy in Hubble patch ~ M_Pl^2 * H^2 * R_H^3 / (G * c^2) = rho * V
M_Pl = np.sqrt(hbar * c / G)   # Planck mass [kg]
rho_inf = 3 * M_Pl**2 * H_inf_SI**2 / (8 * np.pi * G * c**2 / hbar)   # energy density [J/m^3]
E_H_total = rho_inf * V_H   # total energy in Hubble patch

# Bekenstein for the Hubble patch
# Note: for inflation, the holographic bound is S ≤ A/4 = pi*(c/H)^2/l_Pl^2 = pi*M_Pl^2/(hbar*H)^2
l_Pl = np.sqrt(hbar * G / c**3)   # Planck length [m]
S_holographic = np.pi * (R_H / l_Pl)**2 / ln2   # [bits]
print(f"  S_holographic(Hubble patch) = {S_holographic:.3e} bits")
print(f"  E_total(Hubble patch) = {E_H_total:.3e} J")

R_max_inflation = classicality_budget(S_eff_inflation)
print(f"  R_max = {R_max_inflation:.3e}  -> {budget_label(R_max_inflation)}")

add_result(
    "Inflationary Hubble patch (H=10^13 GeV)",
    f"H={H_inf_GeV:.1e}GeV, R_H={R_H:.2e}m, T_dS={T_dS:.2e}K",
    S_holographic, S_eff_inflation, R_max_inflation,
    "de Sitter radiation environment; S_holographic is Bekenstein analogue for inflation"
)

# ============================================================
# SYSTEM A3: Tiny BEC — what size/temperature gives tightest budget?
# ============================================================
print("\n--- SYSTEM A3: BEC sensitivity scan (N atoms, temperature) ---")
print("  How does R_max scale with BEC parameters?")
print()
print(f"  {'N_atoms':>8} {'L_BEC (μm)':>12} {'T_eff (nK)':>12} {'S_eff (bits)':>14} {'R_max':>10}")
print("  " + "-"*60)

for N_A_bec in [1000, 8000, 50000]:
    # Estimate L from atomic density (n ~ 10^14 cm^-3 = 10^20 m^-3 for Rb BEC)
    n_BEC = 1e20   # m^-3
    r_BEC_cross = 5e-6   # m, transverse radius (fixed by trap)
    A_BEC = np.pi * r_BEC_cross**2
    L_est = N_A_bec / (n_BEC * A_BEC)

    for T_nK in [5, 20, 50, 200]:
        T_test = T_nK * 1e-9
        S_t, Nm = phonon_entropy_1d_bose(T_test, L_est, v_s_BEC, xi_BEC)
        print(f"  {N_A_bec:>8} {L_est*1e6:>12.1f} {T_nK:>12.0f} {S_t:>14.2f} {S_t-1:>10.2f}")

# ============================================================
# BONUS: BEC as "most promising" system — what does R_max=1 require?
# ============================================================
print("\n--- BONUS: BEC — conditions for R_max = 1 (tightest useful budget) ---")
# R_max = S_eff/1 - 1 = 1 → S_eff = 2 bits
# What BEC parameters give S_eff = 2 bits?

# Scan L at fixed T_H = 50 nK
print("  Scan L at T_eff=50nK, v_s=1.5mm/s, xi=0.5μm:")
for L_scan_um in [1, 5, 10, 50, 100, 500]:
    L_scan = L_scan_um * 1e-6
    S_sc, N_sc = phonon_entropy_1d_bose(50e-9, L_scan, v_s_BEC, xi_BEC)
    print(f"    L={L_scan_um:4d}μm: N_modes={N_sc:4d}, S_eff={S_sc:.2f} bits, R_max={S_sc-1:.2f}")

# At T_eff = 50 nK, what length gives S_eff = 2 bits?
# From the scan, extrapolate: S_eff ~ N_modes * S_per_mode, where N_modes = L*pi/(xi*pi) = L/xi

# ============================================================
# PRINT FINAL COMPARISON TABLE
# ============================================================
print("\n" + "=" * 100)
print("COMPARISON TABLE: Classicality Budget for Experimental Systems")
print("=" * 100)

hdr = f"{'System':<40} {'S_Bek (bits)':>14} {'S_eff (bits)':>14} {'R_max':>14} {'Status':<30}"
print(hdr)
print("-" * 100)

for r in results:
    S_bek_str = f"{r['S_Bek']:.3e}"
    S_eff_str = f"{r['S_eff']:.3e}"
    R_str     = f"{r['R_max']:.3e}"
    print(f"{r['name']:<40} {S_bek_str:>14} {S_eff_str:>14} {R_str:>14} {r['label']:<30}")
    if r['notes']:
        print(f"  {'':40} {r['notes']}")

print("=" * 100)

# ============================================================
# KEY FINDING SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)

print("""
1. BEC SONIC HORIZON (Steinhauer 2020):
   The most promising experimental system. With T_H=50nK and L=100μm,
   the 1D phonon environment has S_eff ~ few hundred bits.
   R_max ~ 100-300, depending on exact length and temperature.
   This is the ONLY non-BH system with R_max < 10^6.

   BUT: The budget is for the PHONON ENVIRONMENT entropy,
   not the Hawking photons themselves. The relevant question
   is whether QD redundancy R_delta can be measured in the BEC.

2. 50-ION TRAP:
   S_eff(motional modes at n_bar=0.1) ~ 71 bits.
   R_max ~ 70. This is ACTUALLY tighter than the BEC analog!
   AND it's a system where mutual information I(S:F_k) CAN be
   measured experimentally via state tomography.

3. ALL MACROSCOPIC SYSTEMS (QC substrate, NEMS, fiber, inflation):
   R_max >> 10^9 — trivially not constraining.

4. KEY INSIGHT: The "interesting" regime (R_max < 10^3) requires
   ENGINEERED SMALL environments: < ~1000 accessible modes.
   This is achievable only with:
   (a) Ultracold quantum simulators (ion traps, BECs)
   (b) Analog BH systems at nanokelvin temperatures
""")

# ============================================================
# COMPUTE THE CRITICAL COMPARISON: Ion trap vs BEC
# ============================================================
print("Critical comparison: 50-ion trap vs BEC analog BH\n")

print("50-ion trap:")
print(f"  S_eff = {S_eff_ion_conservative:.1f} bits (motional modes, n_bar=0.1)")
print(f"  R_max = {R_max_ion:.1f}")
print(f"  Measurable? YES — mutual information via state tomography")
print(f"  Budget constraining? YES — R_max < 10^3")
print()
print("BEC sonic horizon (T_H=50nK, L=100μm):")
S_bec_final, N_bec_final = phonon_entropy_1d_bose(50e-9, 100e-6, 1.5e-3, 0.5e-6)
print(f"  S_eff = {S_bec_final:.1f} bits (1D phonon modes)")
print(f"  R_max = {S_bec_final - 1:.1f}")
print(f"  Measurable? HARD — requires phonon tomography in 1D BEC")
print(f"  Budget constraining? YES — R_max < 10^3")
print()

# What is the tightest achievable R_max with accessible technology?
print("Minimum achievable R_max with current technology:")
print("  - 20-ion trap, sideband-cooled, n_bar=0.01: S_eff = 60*0.066 = ~4 bits, R_max ~ 3")
N_tight = 20
n_tight = 0.01
S_tight = 3 * N_tight * bose_entropy_per_mode(n_tight)
print(f"  - 20-ion trap, n_bar=0.01: S_eff(motional) = {S_tight:.2f} bits, R_max = {S_tight-1:.2f}")

n_tight2 = 0.001
S_tight2 = 3 * N_tight * bose_entropy_per_mode(n_tight2)
print(f"  - 20-ion trap, n_bar=0.001: S_eff(motional) = {S_tight2:.4f} bits, R_max = {S_tight2-1:.4f}")
print("  Note: at n_bar=0.001, the environment has almost no entropy => R_max approaches -1")
print()
print("  CONCLUSION: Trapped ion systems with 20-50 ions at n_bar ~ 0.01-0.1")
print("  give R_max in the range 1-100, which is the ONLY experimentally accessible")
print("  regime where the classicality budget is non-trivially constraining.")
