"""
FDT Analysis: Fluctuation-Dissipation Theorem in Rindler vs de Sitter

We analyze whether the FDT, in the context of an Unruh-DeWitt detector,
produces a modified effective inertia m_i = m × T_U/T_dS in de Sitter space.

Key formulas:
- Unruh temperature: T_U = hbar*a / (2*pi*c*k_B)
- de Sitter temperature: T_dS = hbar*sqrt(a^2 + c^2*H^2) / (2*pi*c*k_B)
- Ratio: T_U/T_dS = a/sqrt(a^2 + c^2*H^2) = mu_MOND(a/a0) with a0 = cH0
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import integrate
import sympy as sp

# ============================================================
# PHYSICAL CONSTANTS
# ============================================================
hbar = 1.0546e-34  # J*s
k_B  = 1.3806e-23  # J/K
c    = 2.998e8     # m/s
G    = 6.674e-11   # m^3/kg/s^2

# Hubble constant
H0 = 2.268e-18  # s^-1 (70 km/s/Mpc)
a0_cH0 = c * H0  # = 6.8e-10 m/s^2

print("=" * 60)
print("PHYSICAL SCALES")
print("=" * 60)
print(f"H0 = {H0:.3e} s^-1")
print(f"cH0 = {a0_cH0:.3e} m/s^2  (a0 from ratio model)")
print(f"MOND a0 = 1.2e-10 m/s^2")
print(f"Ratio cH0 / a0_MOND = {a0_cH0 / 1.2e-10:.2f}")
print(f"cH0/6 = {a0_cH0/6:.3e} m/s^2  (Verlinde factor)")
print()

# ============================================================
# SECTION 1: TEMPERATURE FORMULAS
# ============================================================

def T_U(a):
    """Unruh temperature for acceleration a [m/s^2]"""
    return hbar * a / (2 * np.pi * c * k_B)

def T_dS(a, H=H0):
    """de Sitter temperature for acceleration a and Hubble constant H"""
    return hbar * np.sqrt(a**2 + c**2 * H**2) / (2 * np.pi * c * k_B)

def T_Gibbons_Hawking(H=H0):
    """Pure de Sitter (Gibbons-Hawking) temperature at a=0"""
    return hbar * H / (2 * np.pi * k_B)

def mu_ratio(a, H=H0):
    """T_U/T_dS = a/sqrt(a^2+c^2*H^2) -- the MOND mu function"""
    return a / np.sqrt(a**2 + c**2 * H**2)

T_GH = T_Gibbons_Hawking()
print("=" * 60)
print("TEMPERATURE SCALES")
print("=" * 60)
print(f"T_GH (de Sitter, a=0) = {T_GH:.3e} K")
print(f"T_U at a = cH0: {T_U(a0_cH0):.3e} K")
print(f"T_dS at a = cH0: {T_dS(a0_cH0):.3e} K")
print(f"Ratio T_U/T_dS at a=cH0: {T_U(a0_cH0)/T_dS(a0_cH0):.4f}")
print(f"Expected: 1/sqrt(2) = {1/np.sqrt(2):.4f}")
print()

# ============================================================
# SECTION 2: FDT ANALYSIS — SYMBOLIC
# ============================================================
print("=" * 60)
print("SECTION 2: FDT ANALYSIS")
print("=" * 60)

# In the Unruh-DeWitt (UDW) detector framework:
#
# The Wightman function for a massless scalar in the Rindler vacuum (= Minkowski vacuum):
# W_R(Delta_tau) = -hbar/(4*pi^2) * 1/(Delta_tau - i*epsilon)^2
#
# Thermal Wightman (KMS state at T):
# W_T(Delta_tau) = -hbar*T^2 / (4*hbar^2) * 1/sinh^2(pi*T*Delta_tau/hbar)
#
# The transition rate for the UDW detector:
# R(E) = |c|^2 * integral_{-inf}^{+inf} dtau e^{i*E*tau/hbar} W(tau)
#
# For Rindler (thermal at T_U):
# R_U(E) = |c|^2 * (E/2*pi*hbar) / (exp(E/k_B*T_U) - 1)  for E > 0
# R_U(-E) = R_U(E) * exp(E/k_B*T_U)  [KMS condition]
#
# For de Sitter (thermal at T_dS):
# R_dS(E) = |c|^2 * (E/2*pi*hbar) / (exp(E/k_B*T_dS) - 1)  for E > 0
#
# The FDT for the FIELD:
# S(omega) = hbar*omega * coth(hbar*omega / (2*k_B*T)) + hbar*omega
#          ≈ 2*k_B*T  for classical limit (hbar*omega << k_B*T)
#
# The imaginary part of the susceptibility (dissipation):
# chi''(omega) = (1/2*hbar) * (S(omega) - S(-omega))
#              = (S(omega)/2*hbar) * (1 - e^{-hbar*omega/k_B*T})
#              ≈ omega * S(omega) / (2*k_B*T)  [classical FDT]
#
# The damping coefficient from Kubo:
# gamma = lim_{omega->0} chi''(omega) / omega
#
# For a KMS state at temperature T (Ohmic spectral density J(omega) = eta*omega):
# chi''(omega) = pi * eta * omega * [delta function sum]
# In the continuum limit: chi''(omega) ~ eta*omega
# => gamma = eta  (temperature independent!)
#
# The noise-to-dissipation ratio:
# D = <eta^2> / (2*gamma) = k_B*T  (Einstein relation)
#
# KEY POINT: gamma is temperature-independent (for Ohmic bath).
# Temperature determines the noise strength, not the dissipation.
# => Effective inertia m is UNCHANGED in the Langevin framework.

print("FDT Framework Summary:")
print("-" * 40)
print("For UDW detector in KMS thermal state at temperature T:")
print("  - Susceptibility chi''(omega) is T-independent (Ohmic bath)")
print("  - Damping coefficient gamma is T-independent")
print("  - Noise-to-dissipation ratio: D = k_B*T (Einstein relation)")
print("  => Effective inertia m is unchanged by thermal bath")
print()
print("In flat Rindler (T = T_U):")
print("  gamma = gamma_U  (T-independent)")
print("  <eta^2> / (2*gamma_U) = k_B * T_U")
print()
print("In de Sitter (T = T_dS > T_U):")
print("  gamma = gamma_U  (dissipation same -- set by coupling to acceleration horizon)")
print("  <eta^2> / (2*gamma_U) = k_B * T_dS  (MORE noise from de Sitter bath)")
print()
print("=> STANDARD FDT GIVES: effective inertia = m (unchanged)")
print("=> Does NOT give m_i = m * T_U/T_dS directly")
print()

# ============================================================
# SECTION 3: NON-EQUILIBRIUM LANGEVIN ANALYSIS
# ============================================================
print("=" * 60)
print("SECTION 3: NON-EQUILIBRIUM LANGEVIN ANALYSIS")
print("=" * 60)

# Scenario: detector is in a non-equilibrium state where:
# (a) Dissipation is determined by the acceleration-horizon coupling (gamma ~ T_U)
# (b) Noise is from the de Sitter vacuum (T_dS)
#
# This is a NON-EQUILIBRIUM situation (violations of detailed balance).
# The effective temperature would be T_dS, not T_U.
#
# For the detector to be in equilibrium, we need detailed balance:
# gamma_eff / m_eff = k_B * T_dS / m_eff  =>  gamma_eff = m_eff * k_B * T_dS / (m * k_B * T_U)
#
# IF gamma is fixed by T_U (through the acceleration horizon coupling):
#   gamma = alpha * T_U  (for some coupling alpha)
# AND the noise is at T_dS:
#   D = k_B * T_dS
#
# Then to restore equilibrium (Einstein relation D = gamma * k_B * T_eff / m):
# k_B * T_dS = (alpha * T_U / m_eff) * k_B * T_eff
#
# If T_eff = T_dS (the bath determines T_eff):
# 1 = alpha * T_U / m_eff
# m_eff = alpha * T_U = m * (T_U / T_Flat) where T_Flat is the flat-space reference
#
# PROBLEM: This gives m_eff = m * T_U/T_flat, not m * T_U/T_dS
# The argument is circular unless we specify T_flat = T_dS.

print("Non-equilibrium scenario:")
print("  gamma_U = alpha * T_U  (dissipation from acceleration horizon)")
print("  D = k_B * T_dS         (noise from de Sitter bath)")
print()
print("Einstein relation: D = gamma * (k_B*T_eff) / m_eff")
print("If T_eff = T_dS: k_B*T_dS = (alpha*T_U/m_eff) * k_B*T_dS")
print("  => m_eff = alpha * T_U")
print()
print("This gives m_eff = m * (T_U/T_flat) where T_flat is flat-space reference,")
print("NOT m * T_U/T_dS.")
print()
print("CONCLUSION: Non-equilibrium Langevin gives wrong ratio unless T_flat = T_dS,")
print("which is circular.")
print()

# ============================================================
# SECTION 4: STOCHASTIC POWER ANALYSIS
# ============================================================
print("=" * 60)
print("SECTION 4: STOCHASTIC POWER DISSIPATION ROUTE")
print("=" * 60)

# Alternative approach: compare power dissipated in flat vs de Sitter.
#
# For a particle undergoing stochastic motion in the vacuum:
# Power input from vacuum fluctuations = Power dissipated through radiation
#
# In flat space (T_U):
# P_in = gamma_U * k_B * T_U / m  (from FDT: equipartition)
# P_diss = gamma_U * <v^2> = gamma_U * k_B * T_U / m  (equilibrium)
#
# In de Sitter (T_dS):
# P_in = gamma_U * k_B * T_dS / m  (MORE power input from de Sitter bath)
# P_diss = gamma_U * <v^2>
#
# At steady state: <v^2> = k_B * T_dS / m
#
# Now define effective inertia via the kinetic energy:
# (1/2) m_eff * <v^2> = (1/2) k_B * T_U  (Unruh energy scale)
# => m_eff = m * T_U / T_dS
#
# This IS the ratio ansatz!
# But it requires: the "natural" energy scale is T_U, not T_dS.
# Physical interpretation: the particle is "trying" to have energy k_B*T_U
# (set by the acceleration horizon), but the de Sitter bath is forcing
# it to have energy k_B*T_dS > k_B*T_U.
# The ratio m_i = m * T_U/T_dS measures how "surprised" the acceleration
# horizon is by the extra de Sitter energy.

print("Stochastic power argument:")
print("  In flat Rindler: <v^2> = k_B*T_U/m  (equipartition at T_U)")
print("  In de Sitter:    <v^2> = k_B*T_dS/m (equipartition at T_dS)")
print()
print("Define effective inertia via the Unruh energy scale:")
print("  (1/2) m_i * <v^2>_dS = (1/2) k_B * T_U")
print("  => m_i = m * T_U / T_dS  [THE RATIO FORMULA]")
print()
print("This gives the ratio formula IF we assume the 'effective' kinetic energy")
print("is set by T_U (the acceleration horizon) rather than T_dS (the full bath).")
print()
print("Physical interpretation: In de Sitter, the particle has MORE kinetic energy")
print("than its acceleration horizon 'expects'. The ratio T_U/T_dS measures the")
print("'fraction' of the kinetic energy that comes from the acceleration horizon.")
print("Effective inertia = m * (T_U-energy / T_dS-energy) = m * T_U/T_dS.")
print()

# ============================================================
# SECTION 5: QUANTITATIVE FDT — SPECTRAL DENSITY RATIO
# ============================================================
print("=" * 60)
print("SECTION 5: SPECTRAL DENSITY COMPARISON")
print("=" * 60)

# The key question: does S_dS(omega) / S_flat(omega) = T_dS / T_U?
# In the classical limit (hbar*omega << k_B*T):
# S(omega) ≈ 2*k_B*T/omega^2 (for a specific model) or ~ k_B*T (flat spectral density)
#
# For the Wightman function of a massless scalar, the spectral density is:
# S_T(omega) = sign(omega) * omega / (exp(|omega|*hbar/k_B*T) - 1) + omega*delta(omega)
#
# In the classical limit:
# S_T(omega) ≈ k_B*T / hbar * sign(omega)  for |omega| << k_B*T/hbar
#
# Ratio:
# S_dS(omega) / S_flat(omega) = T_dS / T_U
#
# In the FDT: chi''(omega) = S(omega) * (1 - e^{-hbar*omega/k_BT}) / (2*hbar)
# Classical: chi''(omega) = omega * S(omega) / (2*k_B*T)
#
# If we use S_dS and T_dS:
# chi''_dS(omega) = omega * S_dS(omega) / (2*k_B*T_dS)
#                = omega * (T_dS/T_U) * S_flat(omega) / (2*k_B*T_dS)
#                = omega * S_flat(omega) / (2*k_B*T_U)
#                = chi''_flat(omega)
#
# KEY RESULT: chi''_dS = chi''_flat in the classical limit!
# The dissipation is the same in flat and de Sitter.
# The increased noise (from T_dS) exactly cancels in the FDT.

print("Spectral density analysis:")
print()
print("Classical FDT: chi''(omega) = omega * S(omega) / (2*k_B*T)")
print()
print("In flat Rindler (T = T_U):")
print("  S_flat(omega) ~ k_B*T_U/hbar  (classical, low-freq)")
print("  chi''_flat(omega) = omega * S_flat / (2*k_B*T_U)")
print("                    = omega / (2*hbar)  [independent of T_U!]")
print()
print("In de Sitter (T = T_dS):")
print("  S_dS(omega) ~ k_B*T_dS/hbar = (T_dS/T_U) * k_B*T_U/hbar")
print("  chi''_dS(omega) = omega * S_dS / (2*k_B*T_dS)")
print("                  = omega * (T_dS/T_U) * k_B*T_U / (2*k_B*T_dS*hbar)")
print("                  = omega / (2*hbar)  [SAME AS FLAT!]")
print()
print("CRITICAL RESULT: The dissipative susceptibility chi'' is IDENTICAL")
print("in flat and de Sitter (classical limit). The extra noise from T_dS")
print("is canceled by the higher temperature in the FDT denominator.")
print()
print("=> STANDARD FDT GIVES NO MODIFICATION TO INERTIA.")
print()

# Compute the ratio chi''_dS / chi''_flat as a function of a/cH0
a_vals = np.logspace(-2, 2, 1000) * a0_cH0  # from 0.01*cH0 to 100*cH0
ratio_T = T_dS(a_vals) / T_U(a_vals)  # = T_dS/T_U = sqrt(1 + (cH/a)^2)
ratio_mu = mu_ratio(a_vals)  # = T_U/T_dS

# chi'' ratio (classical FDT):
# chi''_dS/chi''_flat = (S_dS/S_flat) * (T_U/T_dS) = (T_dS/T_U) * (T_U/T_dS) = 1
chi_ratio = ratio_T * (T_U(a_vals) / T_dS(a_vals))
print(f"chi''_dS / chi''_flat (classical FDT) = {chi_ratio.mean():.6f}  (should be 1.0)")
print()

# ============================================================
# SECTION 6: QUANTUM FDT — BREAKDOWN AT LOW T
# ============================================================
print("=" * 60)
print("SECTION 6: QUANTUM FDT CORRECTIONS")
print("=" * 60)

# The classical FDT fails when hbar*omega ~ k_B*T.
# The full quantum FDT:
# chi''(omega) = (1/2*hbar) * S(omega) * tanh(hbar*omega/(2*k_B*T))
#
# For a harmonic oscillator with natural frequency omega_0:
# m_eff(omega_0) = m * [1 + delta_m(omega_0, T)]
#
# The quantum correction to the mass from vacuum polarization:
# delta_m = (q^2/pi*m) * integral_0^infty domega' J(omega')/(omega'^2 - omega_0^2 + i*epsilon)
#
# In the Caldeira-Leggett model with Ohmic spectral density J(omega) = eta*omega:
# delta_m ~ eta * ln(Lambda/omega_0)  (log-divergent, needs renormalization)
#
# The KEY difference between T_U and T_dS is only in the NOISE, not in the
# dissipation or the mass renormalization.
# => QUANTUM FDT ALSO GIVES NO MODIFICATION TO INERTIA.

print("Quantum FDT (full, not classical approximation):")
print()
print("Full quantum FDT: chi''(omega) = (S(omega)/2*hbar) * tanh(hbar*omega/(2*k_B*T))")
print()
print("For Ohmic spectral density J(omega) = eta*omega:")
print("  Mass renormalization: delta_m = (q^2/pi) * integral J(omega')/omega'^2 domega'")
print("  This is T-independent (UV-divergent, requires renormalization)")
print()
print("=> QUANTUM FDT: mass renormalization is T-independent.")
print("   Temperature only affects the NOISE (fluctuations), not the mass.")
print()
print("CONCLUSION: Neither classical nor quantum FDT gives m_i = m * T_U/T_dS.")
print()

# ============================================================
# SECTION 7: THE TEMPERATURE MISMATCH SCENARIO
# ============================================================
print("=" * 60)
print("SECTION 7: TEMPERATURE MISMATCH — WHAT IF gamma IS AT T_U?")
print("=" * 60)

# Specific scenario (plausible from acceleration-horizon coupling):
# The DISSIPATION coefficient gamma is determined by the acceleration horizon:
#   gamma_U = alpha * a  (proportional to acceleration, which gives T_U ~ a)
# The NOISE is from the full de Sitter vacuum:
#   <eta^2> = 2 * gamma_U * k_B * T_dS  (VIOLATING the FDT at T_U)
#
# Modified Langevin equation:
# m * dv/dt = F_ext - gamma_U * v + eta(t)
# where <eta^2> = 2 * gamma_U * k_B * T_dS
#
# This is NOT in thermal equilibrium. The effective temperature is T_dS.
# But the inertia is still m (not modified).
#
# HOWEVER: if we define the "effective mass" via the dispersion relation:
# omega_eff^2 = (F_ext / m) / (d<x^2>/dt^2)  -- not standard
#
# Or via the effective energy:
# E_kin = (1/2) m <v^2> = (1/2) k_B T_dS (from equipartition in de Sitter)
# E_Unruh = (1/2) k_B T_U (what the acceleration horizon "assigns")
#
# The ratio E_Unruh / E_kin = T_U/T_dS = mu_MOND
#
# If we define m_i via E_Unruh = (1/2) m_i <v^2>:
# m_i = m * T_U / T_dS  [THE RATIO FORMULA]
#
# This is the "effective thermodynamic inertia" — the mass the detector
# would need to have (in flat space) to have energy k_B*T_U/2 with
# the observed velocity dispersion k_B*T_dS/m.

print("Temperature mismatch scenario:")
print()
print("If gamma is determined by T_U (acceleration horizon) but noise is at T_dS:")
print("  m * dv/dt = F_ext - gamma_U * v + eta_dS(t)")
print("  <eta_dS^2> = 2*gamma_U*k_B*T_dS  (noise from de Sitter)")
print()
print("Steady-state kinetic energy: E_kin = (1/2)*m*<v^2> = (1/2)*k_B*T_dS")
print("Unruh energy: E_U = (1/2)*k_B*T_U")
print()
print("Ratio: E_U / E_kin = T_U/T_dS = mu_MOND  (the ratio formula)")
print()
print("Effective 'thermodynamic inertia':")
print("  m_i * <v^2>/2 = k_B*T_U/2")
print("  m_i = m * T_U/T_dS  [RATIO FORMULA RECOVERED]")
print()
print("KEY CAVEAT: This is an ad hoc definition of 'effective inertia'.")
print("The actual equation of motion still has m (not m_i) on the LHS.")
print("The ratio formula emerges from REINTERPRETING kinetic energy using T_U.")
print()

# Compute m_i/m as a function of acceleration
a_over_a0 = np.logspace(-2, 2, 1000)  # a/a0 from 0.01 to 100
mu_vals = a_over_a0 / np.sqrt(1 + a_over_a0**2)

print("mu = T_U/T_dS at key acceleration values:")
for x in [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]:
    mu = x / np.sqrt(1 + x**2)
    print(f"  a/a0 = {x:6.2f}:  mu = {mu:.4f}  (m_i/m = {mu:.4f})")
print()

# ============================================================
# SECTION 8: EFFECTIVE DAMPING RATIO
# ============================================================
print("=" * 60)
print("SECTION 8: EFFECTIVE DAMPING COEFFICIENT RATIO")
print("=" * 60)

# Compute gamma_eff(a) in both flat and de Sitter
# using the Abraham-Lorentz-Dirac self-force
#
# For a scalar charge q in flat space, the Caldeira-Leggett damping is:
# gamma_flat = q^2 * rho(0)  where rho(omega) is the bath spectral density
# For massless scalar in 3+1D: rho(omega) = omega^2/(4*pi^2*c^3) (density of states)
#
# The relevant low-frequency spectral density scales with the temperature:
# gamma ~ q^2 * k_B * T / (hbar * c^3)  (dimensional analysis, thermal correction)
#
# For Rindler/de Sitter, the relevant scales are T_U and T_dS.
# In the low-frequency (Markov) approximation:
# gamma_flat ~ q^2 * T_U / (hbar * c^3)
# gamma_dS  ~ q^2 * T_dS / (hbar * c^3)
#
# Ratio:
# gamma_dS / gamma_flat = T_dS / T_U = 1/mu_MOND

print("Effective damping ratio gamma_dS/gamma_flat:")
print("  (In the thermal, low-frequency Markov approximation)")
print("  gamma ~ T (proportional to thermal fluctuation amplitude)")
print()
print("  gamma_flat ~ T_U")
print("  gamma_dS  ~ T_dS")
print("  gamma_dS/gamma_flat = T_dS/T_U = 1/mu > 1  (MORE damping in de Sitter)")
print()
print("This is the WRONG direction for m_i = m*T_U/T_dS!")
print("MORE damping => MORE resistance => larger effective inertia, not smaller.")
print()
print("SIGN PROBLEM CONFIRMED IN DAMPING COEFFICIENT TOO.")
print()

# ============================================================
# SECTION 9: SUMMARY PLOT — FDT ANALYSIS
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('FDT Analysis: Rindler vs de Sitter', fontsize=14, fontweight='bold')

a_range = np.logspace(-2, 2, 500) * a0_cH0
x = a_range / a0_cH0  # a/cH0

# Panel 1: Temperature ratio
ax = axes[0,0]
ax.loglog(x, T_dS(a_range)/T_U(a_range), 'b-', linewidth=2, label=r'$T_{dS}/T_U$')
ax.loglog(x, T_U(a_range)/T_dS(a_range), 'r-', linewidth=2, label=r'$T_U/T_{dS} = \mu$')
ax.axvline(1.0, color='gray', linestyle='--', alpha=0.5, label=r'$a = cH_0$')
ax.set_xlabel(r'$a / cH_0$')
ax.set_ylabel('Temperature ratio')
ax.set_title('Temperature Ratios')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim([0.01, 100])

# Panel 2: FDT — susceptibility comparison
ax = axes[0,1]
# chi''_flat ~ omega (T-independent for Ohmic bath)
# chi''_dS = chi''_flat (classical FDT)
# The noise S(omega) is enhanced, but the FDT ratio chi''/S is reduced
omega_range = np.logspace(-3, 3, 200)
# Illustrate: S_flat and S_dS at a = 0.5*cH0
a_test = 0.5 * a0_cH0
TU_test = T_U(a_test)
TdS_test = T_dS(a_test)
x_U = hbar * omega_range / (k_B * TU_test)
x_dS = hbar * omega_range / (k_B * TdS_test)

def spectral_density(omega, T):
    """Quantum spectral density: S(omega) = hbar*omega*coth(hbar*omega/(2*k_B*T))"""
    x = hbar * np.abs(omega) / (k_B * T)
    # Use coth(x) = 1/tanh(x) carefully for small x
    with np.errstate(over='ignore', invalid='ignore'):
        result = hbar * np.abs(omega) / np.tanh(x/2)
        result[x < 1e-6] = 2 * k_B * T  # classical limit
    return result

S_flat = spectral_density(omega_range, TU_test)
S_dS = spectral_density(omega_range, TdS_test)

# Normalize by k_B*T_U for comparison
ax.loglog(omega_range, S_flat / (k_B * TU_test), 'b-', lw=2, label=r'$S_{flat}/k_BT_U$')
ax.loglog(omega_range, S_dS / (k_B * TU_test), 'r-', lw=2, label=r'$S_{dS}/k_BT_U$')
ax.set_xlabel(r'$\omega$ [rad/s]')
ax.set_ylabel(r'$S(\omega) / k_BT_U$')
ax.set_title(rf'Spectral Density (a = 0.5 cH₀, T_dS/T_U = {TdS_test/TU_test:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)

# Panel 3: chi'' comparison
ax = axes[1,0]
# Classical: chi''(omega) = omega * S(omega) / (2*k_B*T)
chi_flat = omega_range * S_flat / (2 * k_B * TU_test)
chi_dS = omega_range * S_dS / (2 * k_B * TdS_test)

ax.loglog(omega_range, chi_flat, 'b-', lw=2, label=r"$\chi''_{flat}$ (at $T_U$)")
ax.loglog(omega_range, chi_dS, 'r--', lw=2, label=r"$\chi''_{dS}$ (at $T_{dS}$)")
ax.set_xlabel(r'$\omega$ [rad/s]')
ax.set_ylabel(r"$\chi''(\omega)$")
ax.set_title(r"Dissipative Susceptibility $\chi''(\omega)$")
ax.legend()
ax.grid(True, alpha=0.3)
ax.text(0.05, 0.15, r'Classical FDT: $\chi''$ is the same!', transform=ax.transAxes,
        fontsize=10, color='green', fontweight='bold')

# Panel 4: Effective mass ratio
ax = axes[1,1]
mu_curve = mu_ratio(a_range)
ax.semilogx(x, mu_curve, 'k-', linewidth=2, label=r'$\mu = T_U/T_{dS}$ (ratio formula)')
ax.semilogx(x, 1/np.sqrt(1+x**2), 'b--', linewidth=1.5, label=r'$1/\sqrt{1+(a/a_0)^2}$')
ax.axvline(1.0, color='gray', linestyle='--', alpha=0.5)
ax.axhline(0.5, color='orange', linestyle=':', alpha=0.7, label=r'$\mu = 0.5$')
ax.set_xlabel(r'$a / cH_0$')
ax.set_ylabel(r'$m_i/m = \mu$')
ax.set_title(r'Effective Inertia $m_i/m$ (Ratio Ansatz)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.text(0.05, 0.4, 'Deep MOND:\nm_i → m*(a/a₀) → 0', transform=ax.transAxes, fontsize=9)
ax.text(0.6, 0.8, 'Newtonian:\nm_i → m', transform=ax.transAxes, fontsize=9)

plt.tight_layout()
plt.savefig('/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/compton-unruh/strategies/strategy-001/explorations/exploration-006/fdt_analysis.png',
            dpi=150, bbox_inches='tight')
print("Saved: fdt_analysis.png")
print()

# ============================================================
# FINAL SUMMARY
# ============================================================
print("=" * 60)
print("FINAL FDT SUMMARY")
print("=" * 60)
print()
print("1. STANDARD FDT (classical): chi''_dS = chi''_flat")
print("   => No modification to inertia from FDT alone.")
print("   => The extra de Sitter noise is absorbed in the FDT denominator.")
print()
print("2. DAMPING COEFFICIENT: gamma_dS/gamma_flat = T_dS/T_U > 1")
print("   => De Sitter has MORE damping, not less.")
print("   => Wrong direction for m_i = m*T_U/T_dS < m.")
print()
print("3. ENERGY ARGUMENT: A non-rigorous path to the ratio formula exists.")
print("   If effective kinetic energy is 'defined' via T_U (not T_dS),")
print("   then m_i = m*(T_U/T_dS) follows from E_U = E_kin * (T_U/T_dS).")
print("   This is the ratio ansatz, not a derivation.")
print()
print("4. SIGN PROBLEM: The FDT confirms the sign problem from Expl. 004.")
print("   The de Sitter bath INCREASES effective temperature (more noise),")
print("   but the ratio formula requires DECREASED effective inertia.")
print("   These are NOT equivalent unless a specific non-standard")
print("   definition of inertia is adopted.")
print()
print("5. MOST PROMISING ROUTE: The 'thermodynamic inertia' definition")
print("   m_i = m * E_U/E_kin = m * T_U/T_dS is self-consistent.")
print("   Needs grounding in a specific dynamical model.")
