"""
Part 1: Wightman function in the de Sitter crossover regime.

We analyze the Wightman function G+(Delta_tau) for a massless scalar field
experienced by a uniformly accelerating observer in de Sitter spacetime.

Key references:
- Deser & Levin (1997): Accelerated detectors in de Sitter
- Narnhofer, Peter, Thirring (1996): KMS condition in de Sitter
- Birrell & Davies: QFT in curved spacetime (textbook)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.special import gamma as Gamma
import os

# Output directory
OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================================
# PHYSICAL CONSTANTS
# ======================================================================
hbar = 1.054571817e-34   # J*s
c = 2.99792458e8         # m/s
kB = 1.380649e-23        # J/K
G_N = 6.67430e-11        # m^3/(kg*s^2)
H0 = 2.2e-18             # 1/s  (H0 ~ 67.4 km/s/Mpc)
a0_MOND = 1.2e-10        # m/s^2  (MOND acceleration)
cH0 = c * H0             # ~ 6.6e-10 m/s^2
T_GH = hbar * H0 / (2 * np.pi * kB)  # Gibbons-Hawking temperature
M_sun = 1.989e30         # kg

print("=" * 70)
print("Part 1: Wightman Function Analysis in de Sitter Crossover Regime")
print("=" * 70)
print(f"\nFundamental scales:")
print(f"  H_0 = {H0:.3e} s^-1")
print(f"  cH_0 = {cH0:.3e} m/s^2")
print(f"  a_0(MOND) = {a0_MOND:.3e} m/s^2")
print(f"  T_GH = {T_GH:.3e} K")
print(f"  a_0/cH_0 = {a0_MOND/cH0:.4f}")

# ======================================================================
# SECTION 1.1: The Wightman function forms
# ======================================================================
print("\n" + "=" * 70)
print("Section 1.1: Wightman Function Forms")
print("=" * 70)

# --- Flat-space Rindler (pure Unruh) ---
# For a massless scalar in (3+1)D, along a Rindler worldline with acceleration a:
#
#   G+_Rindler(s) = -(1/(4*pi^2)) * (a/(2c))^2 / sinh^2(a*s/(2c) - i*eps)
#
# where s = Delta_tau (proper time difference)
#
# This is periodic in imaginary time with period beta_U = 2*pi*c/a,
# corresponding to the Unruh temperature T_U = hbar*a/(2*pi*c*k_B).

# --- De Sitter (static patch, accelerating observer) ---
# For a uniformly accelerating observer in de Sitter with acceleration a,
# the effective temperature is:
#
#   T_dS(a) = (hbar/(2*pi*c*k_B)) * sqrt(a^2 + c^2*H^2)
#
# The Wightman function for a MASSLESS scalar field experienced by
# a uniformly accelerating observer in de Sitter spacetime is:
#
#   G+_dS(s) = -(H^2/(16*pi^2)) / [sinh^2(alpha*s/(2) - i*eps)]
#
# where alpha = sqrt(a^2/c^2 + H^2) is the "effective surface gravity"
# of the observer's horizon, and the KMS periodicity is
# beta_dS = 2*pi/alpha in proper time, corresponding to T_dS.
#
# In the limit H -> 0: alpha -> a/c, and we recover the Rindler result
# (up to normalization factors related to the embedding).
#
# In the limit a -> 0: alpha -> H, and we get the Bunch-Davies vacuum
# Wightman function for a static observer in de Sitter.

alpha_eff = lambda a_acc: np.sqrt(a_acc**2 / c**2 + H0**2)

# The effective temperature
# T_dS(a) = (hbar/(2*pi*c*kB)) * sqrt(a^2 + c^2*H^2)
#         = (hbar/(2*pi*kB)) * sqrt(a^2/c^2 + H^2)
#         = (hbar/(2*pi*kB)) * alpha_eff
T_dS = lambda a_acc: hbar * alpha_eff(a_acc) / (2 * np.pi * kB)
T_U = lambda a_acc: hbar * a_acc / (2 * np.pi * c * kB)

print("\nVerification of temperature formulas:")
print(f"  T_U(cH0) = {T_U(cH0):.4e} K")
print(f"  T_GH = {T_GH:.4e} K")
print(f"  T_dS(cH0) = {T_dS(cH0):.4e} K")
print(f"  sqrt(2)*T_GH = {np.sqrt(2)*T_GH:.4e} K")
print(f"  T_dS(cH0) / (sqrt(2)*T_GH) = {T_dS(cH0) / (np.sqrt(2)*T_GH):.6f}")
# Should be exactly 1

# ======================================================================
# SECTION 1.2: Power Spectral Density (Fourier transform of G+)
# ======================================================================
print("\n" + "=" * 70)
print("Section 1.2: Power Spectral Density")
print("=" * 70)

# The spectral density (response function for a detector with gap omega) is:
#
#   rho(omega; a) = integral_{-inf}^{inf} ds exp(-i*omega*s) G+(s)
#
# For a THERMAL state at temperature T, this gives the Planckian distribution:
#
#   rho(omega; T) = omega / (2*pi) * 1/(exp(hbar*omega/(kB*T)) - 1)    for omega > 0
#
# The KMS condition guarantees that the state along an accelerating
# worldline in de Sitter is thermal at temperature T_dS(a).
#
# Therefore:
#   - For a >> cH0: T_eff ~ T_U(a) = hbar*a/(2*pi*c*kB), Planckian at T_U
#   - For a ~ cH0: T_eff = T_dS(a) = (hbar/2*pi*c*kB)*sqrt(a^2 + c^2*H^2)
#   - For a << cH0: T_eff ~ T_GH = hbar*H0/(2*pi*kB), Planckian at T_GH
#
# CRITICAL POINT: In all three regimes, the spectrum is EXACTLY thermal
# (for a massless scalar field). The KMS condition holds. The ONLY
# difference is the temperature.

# Planckian spectral density (number of quanta per unit frequency per unit time)
def planckian(omega, T):
    """Bose-Einstein spectral density at temperature T, frequency omega (rad/s)."""
    if T <= 0:
        return np.zeros_like(omega) if hasattr(omega, '__len__') else 0.0
    x = hbar * omega / (kB * T)
    # Avoid overflow
    x = np.clip(x, 0, 700)
    return omega / (2 * np.pi) * 1.0 / (np.exp(x) - 1)

# ======================================================================
# SECTION 1.3: Numerical comparison of spectral densities
# ======================================================================
print("\n" + "=" * 70)
print("Section 1.3: Numerical Comparison of Power Spectra")
print("=" * 70)

# Choose several accelerations spanning the crossover
accelerations = {
    '100 cH0': 100 * cH0,
    '10 cH0': 10 * cH0,
    'cH0': cH0,
    '0.1 cH0': 0.1 * cH0,
    '0.01 cH0': 0.01 * cH0,
    'a0_MOND': a0_MOND,
}

print("\nEffective temperatures across the crossover:")
print(f"{'Acceleration':>15s}  {'a (m/s^2)':>12s}  {'T_U (K)':>12s}  {'T_dS (K)':>12s}  {'T_dS/T_U':>10s}")
for label, a_val in accelerations.items():
    t_u = T_U(a_val)
    t_ds = T_dS(a_val)
    ratio = t_ds / t_u if t_u > 0 else float('inf')
    print(f"{label:>15s}  {a_val:12.4e}  {t_u:12.4e}  {t_ds:12.4e}  {ratio:10.4f}")

# Key insight: At a >> cH0, T_dS/T_U -> 1 (flat space limit)
# At a = cH0, T_dS/T_U = sqrt(2)
# At a << cH0, T_dS/T_U -> cH0/a -> infinity

# ======================================================================
# PLOT 1: Power spectral density at several accelerations
# ======================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: Unruh (flat space) spectral density
# Right panel: de Sitter spectral density
# Show both for several accelerations

# Frequency range appropriate for the thermal scale
# Peak of Planckian at omega ~ 2.82 * kB*T/hbar
omega_min = 1e-5  # rad/s (normalized)
omega_max = 1e3   # rad/s

# Use dimensionless frequency: x = hbar*omega/(kB*T_GH)
x_range = np.logspace(-2, 4, 1000)

colors = plt.cm.viridis(np.linspace(0, 0.9, len(accelerations)))

for ax_idx, (title, T_func) in enumerate([
    ('Flat-Space Unruh', T_U),
    ('De Sitter Modified', T_dS)
]):
    ax = axes[ax_idx]
    for (label, a_val), col in zip(accelerations.items(), colors):
        T = T_func(a_val)
        # Dimensionless spectral density
        # rho(x * kB*T_GH/hbar) * (hbar/kB*T_GH)
        omega_vals = x_range * kB * T_GH / hbar
        spec = np.array([planckian(om, T) for om in omega_vals])
        # Normalize by T_GH scale
        spec_norm = spec * hbar / (kB * T_GH)
        ax.loglog(x_range, spec_norm + 1e-300, color=col, label=label, linewidth=1.5)
    ax.set_xlabel(r'$\hbar\omega / k_B T_{GH}$', fontsize=12)
    ax.set_ylabel(r'Spectral density (normalized)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=9)
    ax.set_xlim(1e-2, 1e4)
    ax.set_ylim(1e-10, 1e6)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot1_spectral_density_comparison.png'), dpi=150)
plt.close()
print("\nPlot 1 saved: plot1_spectral_density_comparison.png")

# ======================================================================
# PLOT 2: Temperature ratio T_dS/T_U across the crossover
# ======================================================================
a_range = np.logspace(-15, 0, 1000)  # m/s^2
t_ratio = np.array([T_dS(a) / T_U(a) for a in a_range])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Top: absolute temperatures
ax1.loglog(a_range, [T_U(a) for a in a_range], 'b-', label=r'$T_U(a) = \frac{\hbar a}{2\pi c k_B}$', linewidth=2)
ax1.loglog(a_range, [T_dS(a) for a in a_range], 'r--', label=r'$T_{dS}(a) = \frac{\hbar}{2\pi c k_B}\sqrt{a^2 + c^2H_0^2}$', linewidth=2)
ax1.axhline(T_GH, color='green', linestyle=':', linewidth=1.5, label=r'$T_{GH}$')
ax1.axvline(cH0, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
ax1.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5, linewidth=1.5)
ax1.text(cH0*1.5, 1e-27, r'$cH_0$', fontsize=11, color='gray')
ax1.text(a0_MOND*0.1, 1e-27, r'$a_0$', fontsize=11, color='orange')
ax1.set_ylabel('Temperature (K)', fontsize=12)
ax1.set_title('Effective Temperature: Flat Unruh vs De Sitter', fontsize=14)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1e-15, 1e0)

# Bottom: ratio T_dS/T_U
ax2.loglog(a_range, t_ratio, 'k-', linewidth=2)
ax2.axhline(np.sqrt(2), color='red', linestyle=':', linewidth=1.5, label=r'$\sqrt{2}$ (at $a = cH_0$)')
ax2.axvline(cH0, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
ax2.axvline(a0_MOND, color='orange', linestyle=':', alpha=0.5, linewidth=1.5)
ax2.set_xlabel(r'Acceleration $a$ (m/s$^2$)', fontsize=12)
ax2.set_ylabel(r'$T_{dS}(a) / T_U(a)$', fontsize=12)
ax2.set_title(r'Temperature ratio across the crossover', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1e-15, 1e0)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot2_temperature_crossover.png'), dpi=150)
plt.close()
print("Plot 2 saved: plot2_temperature_crossover.png")

# ======================================================================
# SECTION 1.4: The TOTAL power (integrated spectral density)
# ======================================================================
print("\n" + "=" * 70)
print("Section 1.4: Total Vacuum Fluctuation Power")
print("=" * 70)

# The total power in a Planckian spectrum at temperature T is:
#   P = sigma * T^4   (Stefan-Boltzmann for a scalar field)
# where sigma_scalar = pi^2 * kB^4 / (120 * hbar^3 * c^2) for ONE scalar
#
# So the total power goes as T^4.
# For the de Sitter case: P_dS(a) ~ T_dS(a)^4 = [(hbar/(2*pi*c*kB))]^4 * (a^2 + c^2*H^2)^2
# For flat Unruh: P_U(a) ~ T_U(a)^4 ~ a^4

# The RATIO of powers:
#   P_dS(a) / P_U(a) = T_dS(a)^4 / T_U(a)^4 = [(a^2 + c^2*H^2)/a^2]^2 = [1 + (cH/a)^2]^2

print("\nTotal power ratio P_dS/P_U (proportional to T^4 ratio):")
for label, a_val in accelerations.items():
    ratio = (1 + (cH0/a_val)**2)**2
    print(f"  a = {label:>15s}: P_dS/P_U = {ratio:.6e}")

# At a = cH0: ratio = (1+1)^2 = 4
# At a = 0.1*cH0: ratio = (1+100)^2 ~ 10^4
# This is a POLYNOMIAL enhancement, not exponential. Still physical.

print("\nKey insight: At low accelerations (a << cH0), the de Sitter vacuum")
print("provides a 'bath' with power ~ T_GH^4, independent of acceleration.")
print("This means the ACCELERATION DEPENDENCE of vacuum effects changes.")
print("In flat space: P ~ a^4. In de Sitter at low a: P ~ const (= T_GH^4).")

# ======================================================================
# SECTION 1.5: The Wightman function itself
# ======================================================================
print("\n" + "=" * 70)
print("Section 1.5: Explicit Wightman Functions")
print("=" * 70)

print("""
For a MASSLESS scalar field in (3+1)D:

FLAT SPACE (Rindler):
  G+_R(s) = -(1/(4*pi^2)) * (a/(2c))^2 / sinh^2(a*s/(2c) - i*eps)

  KMS periodicity: beta_U = 2*pi*c/a  in proper time
  Temperature: T_U = hbar*a/(2*pi*c*kB)

DE SITTER (accelerating observer):
  G+_dS(s) = -(H^2/(16*pi^2)) / sinh^2(alpha_eff*s/2 - i*eps)

  where alpha_eff = sqrt(a^2/c^2 + H^2)
  KMS periodicity: beta_dS = 2*pi/alpha_eff
  Temperature: T_dS = hbar*c*alpha_eff/(2*pi*kB)

The functional FORM is the same — both are sinh^-2 — but the
characteristic frequency is different:
  Rindler: omega_char = a/(2c)
  de Sitter: omega_char = alpha_eff/2 = sqrt(a^2/c^2 + H^2)/2

In the crossover regime (a ~ cH0):
  alpha_eff ~ sqrt(2)*H0
  T_dS ~ sqrt(2)*T_GH
  The Wightman function has a longer correlation time compared to
  flat-space Unruh at the same acceleration.
""")

# ======================================================================
# PLOT 3: Wightman function comparison
# ======================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot G+(s) for Rindler and de Sitter at several accelerations
# Use dimensionless time: s_dimless = H0 * s

s_dimless = np.linspace(0.01, 10, 1000)
eps_reg = 0.01  # regularization

for idx, (label, a_val) in enumerate(list(accelerations.items())[:4]):
    row, col = idx // 2, idx % 2
    ax = axes[row][col]

    # Rindler G+
    omega_R = a_val / (2 * c)
    s_phys = s_dimless / H0  # convert to physical time
    arg_R = omega_R * s_phys
    G_R = -1/(4*np.pi**2) * omega_R**2 / (np.sinh(arg_R)**2 + eps_reg**2)

    # de Sitter G+
    alpha = alpha_eff(a_val)
    arg_dS = alpha * s_phys / 2
    G_dS = -H0**2 / (16*np.pi**2) / (np.sinh(arg_dS)**2 + eps_reg**2)

    ax.plot(s_dimless, np.abs(G_R) / max(np.abs(G_R)), 'b-', label='Rindler', linewidth=2)
    ax.plot(s_dimless, np.abs(G_dS) / max(np.abs(G_dS)), 'r--', label='de Sitter', linewidth=2)
    ax.set_title(f'a = {label}', fontsize=12)
    ax.set_xlabel(r'$H_0 \Delta\tau$', fontsize=11)
    ax.set_ylabel(r'$|G^+|$ (normalized)', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.suptitle('Wightman Function: Rindler vs De Sitter', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'plot3_wightman_comparison.png'), dpi=150)
plt.close()
print("\nPlot 3 saved: plot3_wightman_comparison.png")

# ======================================================================
# SUMMARY OF PART 1
# ======================================================================
print("\n" + "=" * 70)
print("PART 1 SUMMARY")
print("=" * 70)
print("""
KEY RESULTS:

1. The Wightman function in de Sitter has the SAME functional form (sinh^-2)
   as in flat Rindler space, but with alpha_eff = sqrt(a^2/c^2 + H^2)
   replacing a/c.

2. The spectral density is EXACTLY THERMAL (Planckian) at temperature
   T_dS(a) = (hbar*c*alpha_eff)/(2*pi*kB) for a massless scalar field.
   This is guaranteed by the KMS condition.

3. The crossover at a ~ cH0 changes the TEMPERATURE of the bath from
   T ~ a (proportional to acceleration) to T ~ T_GH (constant).

4. The total power in the vacuum fluctuation spectrum scales as T^4:
   - For a >> cH0: P ~ a^4 (acceleration-dominated)
   - For a << cH0: P ~ T_GH^4 ~ H0^4 (cosmological-horizon-dominated)
   - Crossover at a ~ cH0: P ~ (a^2 + c^2*H^2)^2

5. CRITICAL: The spectral form is still Planckian in all regimes.
   The de Sitter modification changes ONLY the temperature parameter.
   This means the force modification (if any) must come from the
   temperature dependence of the radiation reaction force, NOT from
   a change in spectral shape.
""")
