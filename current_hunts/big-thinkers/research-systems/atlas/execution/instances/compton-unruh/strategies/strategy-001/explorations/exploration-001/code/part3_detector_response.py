# -*- coding: utf-8 -*-
"""
Part 3: Unruh-DeWitt detector response -- numerical exploration.

We compute the transition rate R(E) for a detector coupled to a MASSLESS
scalar field on a Rindler trajectory, then explore how a MASSIVE field
modifies the Wightman function.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Constants
h    = 6.62607015e-34
hbar = h / (2 * np.pi)
c    = 2.99792458e8
k_B  = 1.380649e-23
m_p  = 1.67262192e-27
H0   = 2.2e-18
eV   = 1.602176634e-19

# Derived
cH0 = c * H0
T_GH = hbar * H0 / (2 * np.pi * k_B)
a0_MOND = 1.2e-10

print("=" * 70)
print("PART 3: UNRUH-DEWITT DETECTOR RESPONSE")
print("=" * 70)

print("""
MASSLESS SCALAR FIELD IN FLAT SPACETIME (Rindler)
=================================================

The Wightman function for a massless scalar field evaluated along
a uniformly accelerating trajectory with proper acceleration a is:

  G+(Delta_tau) = -(a/(4*pi*c))^2 / sinh^2(a*(Delta_tau - i*eps)/(2c))   ...(1)

where Delta_tau = tau - tau' and eps -> 0+.

The transition rate of a two-level detector with energy gap E is:

  R(E) = integral d(Delta_tau) exp(-i*E*Delta_tau/hbar) * G+(Delta_tau)   ...(2)

Evaluating via contour integration (poles at Delta_tau = 2*pi*i*n*c/a):

  R(E) = (E/hbar) / (2*pi * (exp(2*pi*c*E/(hbar*a)) - 1))   [E > 0]     ...(3)

This is a Bose-Einstein distribution with temperature T_U = hbar*a/(2*pi*c*k_B).
The factor E/hbar out front is the density of states factor.

KEY POINT: This result has NO resonance structure. The rate R(E) is a
smooth, monotonically decreasing function of E at fixed a.
""")

# Compute the suppression at a = cH0, E = m_p c^2
a_val = cH0
E_val = m_p * c**2
exponent = 2 * np.pi * c * E_val / (hbar * a_val)
print(f"At a = cH0 = {a_val:.2e} m/s^2, E = m_p c^2 = {E_val:.2e} J:")
print(f"  Exponent: 2*pi*c*E/(hbar*a) = {exponent:.6e}")
print(f"  This is ~10^{np.log10(exponent):.0f}")
print(f"  Boltzmann factor exp(-exponent) = 10^(-{exponent/np.log(10):.0e})")
print(f"  The detector response at Compton energy is suppressed by ~10^(-{exponent/np.log(10):.0e})")
print(f"  This is fantastically, absurdly, unmeasurably small.")

print("""
=================================================
MASSIVE SCALAR FIELD IN FLAT SPACETIME (Rindler)
=================================================

For a MASSIVE scalar field (mass m, Compton frequency w_C = mc/hbar),
the field modes have a minimum frequency w >= w_C (mass gap).

The key changes from the massless case:

1. The response is still THERMAL at T = hbar*a/(2*pi*c*k_B).
   This is guaranteed by the KMS condition (depends on periodicity
   in imaginary time, not on field mass).

2. The SPECTRAL DISTRIBUTION (density of states) is modified.
   For a massive field, the 3+1D density of states near threshold is:
     rho(w) ~ w * sqrt(w^2 - w_C^2)    for w > w_C
     rho(w) = 0                         for w < w_C

   Near threshold: rho(w) -> 0 as w -> w_C+ (square-root onset).
   There is NO resonance peak; there is a threshold with a square-root
   rise (a Van Hove singularity -- but it's a zero, not a pole).

3. The detector response for gap E in the massive field:
     R_m(E) ~ (1/(exp(beta*E) - 1)) * rho_m(E)

When E = mc^2 (detector gap = Compton energy):
  - Boltzmann: exp(-mc^2/(k_B*T_U)) = exp(-2*pi*mc^3/(hbar*a))
    At a ~ cH0: exp(-10^43) (unmeasurably small!)
  - Density of states at threshold: rho = 0

Both factors conspire to make R(mc^2) essentially zero at a ~ cH0.

VERDICT: No resonance. The Compton frequency marks a THRESHOLD,
not a resonance, in the detector response.
""")

# ============================================================
# De Sitter spacetime
# ============================================================
print("""
=================================================
MASSIVE SCALAR IN DE SITTER SPACETIME
=================================================

In de Sitter spacetime, the Wightman function for a massive scalar
field along a geodesic observer's worldline (Bunch-Davies vacuum) is:

  G+_dS(Delta_tau) = (H^2/(16*pi^2)) * Gamma(h+)*Gamma(h-) / Gamma(3/2)^2
                     * 2F1(h+, h-; 3/2; (1 + cos(H*Delta_tau - i*eps))/2)

where:
  h+ = 3/2 + sqrt(9/4 - m^2*c^4/(hbar^2*H^2))   [or i*nu for large mass]
  h- = 3/2 - sqrt(9/4 - m^2*c^4/(hbar^2*H^2))

The dimensionless mass parameter is:
  nu^2 = m^2*c^4/(hbar^2*H^2) - 9/4
""")

nu_sq = (m_p * c**2)**2 / (hbar * H0)**2 - 9.0/4
print(f"For the proton with H = H0:")
print(f"  nu^2 = m^2*c^4/(hbar^2*H0^2) - 9/4 = {nu_sq:.6e}")
print(f"  nu = {np.sqrt(nu_sq):.6e}")
print(f"  mc^2/(hbar*H0) = {m_p*c**2/(hbar*H0):.6e}")

T_dS_cH0 = hbar * np.sqrt(cH0**2 + cH0**2) / (2 * np.pi * c * k_B)
mc2_over_kT = m_p * c**2 / (k_B * T_dS_cH0)

print(f"""
Since mc^2/(hbar*H0) ~ {m_p*c**2/(hbar*H0):.1e} >> 1, the proton is deeply
in the 'heavy field' regime in de Sitter space.

For the accelerating observer in de Sitter:
  - T_dS(cH0) = sqrt(2) * T_GH ~ {T_dS_cH0:.2e} K
  - mc^2/(k_B * T_dS) ~ {mc2_over_kT:.2e}
  - Boltzmann factor ~ exp(-{mc2_over_kT:.2e})

This is again absurdly suppressed. The massive field in de Sitter
does NOT produce a resonance at a ~ cH0 for detector gap E = mc^2.
""")

# ============================================================
# Plot: Detector response R(E) vs E for different accelerations
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

# For MASSLESS field, R(E) = (E/hbar) / (2*pi*(exp(2*pi*c*E/(hbar*a)) - 1))
# Plot log R vs E for several accelerations
E_range = np.logspace(-40, -5, 1000) * eV  # in Joules

for a_val, label, color in [
    (1e20, r'$a = 10^{20}$ m/s$^2$', 'red'),
    (1e10, r'$a = 10^{10}$ m/s$^2$', 'orange'),
    (1.0, r'$a = 1$ m/s$^2$ (Earth gravity)', 'blue'),
    (c*H0, r'$a = cH_0$', 'green'),
]:
    # Use log to avoid overflow: log R = log(E/hbar) - log(2*pi) - x/ln(10)
    x = 2 * np.pi * c * E_range / (hbar * a_val)
    log_R = np.log10(E_range/hbar) - np.log10(2*np.pi) - x / np.log(10)
    # Only plot where R > 10^-300
    mask = log_R > -300
    if np.any(mask):
        ax.plot(E_range[mask]/eV, log_R[mask], color=color, linewidth=2, label=label)

# Mark proton Compton energy
ax.axvline(x=m_p*c**2/eV, color='black', linestyle='--', linewidth=1.5,
           label=r'$m_p c^2$ = %.0e eV' % (m_p*c**2/eV))

ax.set_xlabel('Detector gap energy $E$ (eV)', fontsize=14)
ax.set_ylabel(r'$\log_{10}$ R(E) (arb. units)', fontsize=14)
ax.set_title('Detector Response Rate vs. Energy Gap\n(massless field, various accelerations)', fontsize=14)
ax.set_xscale('log')
ax.legend(fontsize=10)
ax.set_xlim(1e-40, 1e-5)
ax.set_ylim(-300, 100)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('code/plot4_detector_response.png', dpi=150)
print("\nPlot 4 saved to code/plot4_detector_response.png")
plt.close()

# ============================================================
# Plot 5: R(E=m_p*c^2) vs acceleration -- is there a peak?
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

a_range = np.logspace(-12, 40, 10000)
E_proton = m_p * c**2

# log10 R = log10(E/hbar) - log10(2*pi) - 2*pi*c*E/(hbar*a*ln10)
log_R_vs_a = np.log10(E_proton/hbar) - np.log10(2*np.pi) - 2*np.pi*c*E_proton/(hbar*a_range*np.log(10))

# Also compute dR/da to check for peaks
# d(log R)/d(log a) = 2*pi*c*E/(hbar*a * ln10) (always positive -> R always increases with a)
# There is no peak.

mask = log_R_vs_a > -300
if np.any(mask):
    ax.plot(a_range[mask], log_R_vs_a[mask], 'b-', linewidth=2,
            label=r'$\log_{10} R(E = m_p c^2, a)$ (massless field)')

ax.axvline(x=cH0, color='orange', linestyle=':', linewidth=1.5, label=r'$cH_0$')
ax.axvline(x=a0_MOND, color='purple', linestyle='-.', linewidth=1.5, label=r'$a_0$ (MOND)')

# Mark the matching acceleration
a_star = 2 * np.pi * m_p * c**3 / hbar
ax.axvline(x=a_star, color='red', linestyle='--', linewidth=1.5,
           label=r'$a^* = 2\pi m_p c^3/\hbar$')

ax.set_xlabel('Acceleration $a$ (m/s$^2$)', fontsize=14)
ax.set_ylabel(r'$\log_{10}$ R($m_p c^2$, $a$)', fontsize=14)
ax.set_title(r'Detector Response at $E = m_p c^2$ vs. Acceleration', fontsize=14)
ax.set_xscale('log')
ax.legend(fontsize=10)
ax.set_xlim(1e-12, 1e40)
ax.set_ylim(-300, 50)
ax.grid(True, alpha=0.3)

# Annotate
ax.annotate('No peak or resonance!\nR increases monotonically with a',
            xy=(1e25, -50), fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('code/plot5_response_vs_acceleration.png', dpi=150)
print("Plot 5 saved to code/plot5_response_vs_acceleration.png")
plt.close()

print("\nDone.")
