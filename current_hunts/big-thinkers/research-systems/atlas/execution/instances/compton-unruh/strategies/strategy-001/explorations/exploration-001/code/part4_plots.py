"""
Part 4: Numerical exploration — produce plots of thermal scales vs. acceleration.
Generates three plots as PNG files.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# Constants
# ============================================================
h    = 6.62607015e-34
hbar = h / (2 * np.pi)
c    = 2.99792458e8
k_B  = 1.380649e-23
m_p  = 1.67262192e-27
H0   = 2.2e-18
a0_MOND = 1.2e-10
eV   = 1.602176634e-19

# Derived
cH0 = c * H0
T_GH = hbar * H0 / (2 * np.pi * k_B)
E_C_proton = m_p * c**2
a_star_proton = 2 * np.pi * m_p * c**3 / hbar

# Functions
def T_U(a):
    return hbar * a / (2 * np.pi * c * k_B)

def T_dS(a, H):
    return hbar * np.sqrt(a**2 + (c*H)**2) / (2 * np.pi * c * k_B)

def E_U(a):
    return hbar * a / (2 * np.pi * c)

# ============================================================
# Plot 1: T_U(a) and T_GH vs. acceleration
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

a_range = np.logspace(-15, 0, 1000)

ax.loglog(a_range, T_U(a_range), 'b-', linewidth=2, label=r'$T_U(a) = \frac{\hbar a}{2\pi c k_B}$ (flat Unruh)')
ax.loglog(a_range, T_dS(a_range, H0), 'r--', linewidth=2, label=r'$T_{dS}(a) = \frac{\hbar}{2\pi c k_B}\sqrt{a^2 + c^2 H_0^2}$ (de Sitter)')
ax.axhline(y=T_GH, color='green', linestyle=':', linewidth=1.5, label=f'$T_{{GH}} = {T_GH:.2e}$ K')
ax.axvline(x=cH0, color='orange', linestyle=':', linewidth=1.5, label=f'$cH_0 = {cH0:.2e}$ m/s²')
ax.axvline(x=a0_MOND, color='purple', linestyle='-.', linewidth=1.5, label=f'$a_0$ (MOND) = {a0_MOND:.1e} m/s²')

ax.set_xlabel('Acceleration $a$ (m/s²)', fontsize=14)
ax.set_ylabel('Temperature (K)', fontsize=14)
ax.set_title('Plot 1: Unruh Temperature vs. Acceleration\n(with Gibbons-Hawking floor)', fontsize=14)
ax.legend(fontsize=10, loc='upper left')
ax.set_xlim(1e-15, 1e0)
ax.set_ylim(1e-36, 1e-20)
ax.grid(True, alpha=0.3)

# Annotate the crossover region
ax.annotate(f'Crossover at $a \\sim cH_0$\n$T_U \\approx T_{{GH}}$',
            xy=(cH0, T_GH), xytext=(1e-7, 1e-27),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=11, ha='center')

plt.tight_layout()
plt.savefig('code/plot1_temperatures.png', dpi=150)
print("Plot 1 saved to code/plot1_temperatures.png")
plt.close()

# ============================================================
# Plot 2: E_U(a) and E_C(proton) vs. acceleration
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

# Need much wider range to show intersection
a_range2 = np.logspace(-15, 40, 2000)

ax.loglog(a_range2, E_U(a_range2) / eV, 'b-', linewidth=2, label=r'$E_U(a) = \frac{\hbar a}{2\pi c}$ (Unruh energy)')
ax.axhline(y=E_C_proton / eV, color='red', linestyle='-', linewidth=2, label=f'$E_C$ (proton) = {E_C_proton/eV:.2e} eV')
ax.axvline(x=a_star_proton, color='darkred', linestyle=':', linewidth=1.5, label=f'$a^* = 2\\pi m_p c^3/\\hbar = {a_star_proton:.2e}$ m/s²')
ax.axvline(x=cH0, color='orange', linestyle=':', linewidth=1.5, label=f'$cH_0 = {cH0:.2e}$ m/s²')
ax.axvline(x=a0_MOND, color='purple', linestyle='-.', linewidth=1.5, label=f'$a_0$ (MOND) = {a0_MOND:.1e} m/s²')

# Shade the gap
ax.axvspan(a0_MOND, a_star_proton, alpha=0.05, color='red')
ax.annotate(f'$a^*/a_0 \\approx 10^{{43}}$\n(enormous gap!)',
            xy=(1e16, E_C_proton/eV), xytext=(1e16, 1e-5),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=12, ha='center')

ax.set_xlabel('Acceleration $a$ (m/s²)', fontsize=14)
ax.set_ylabel('Energy (eV)', fontsize=14)
ax.set_title('Plot 2: Unruh Energy vs. Proton Compton Energy\n(matching acceleration $a^*$ vs. MOND $a_0$)', fontsize=14)
ax.legend(fontsize=9, loc='upper left')
ax.set_xlim(1e-15, 1e40)
ax.set_ylim(1e-40, 1e15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('code/plot2_energies.png', dpi=150)
print("Plot 2 saved to code/plot2_energies.png")
plt.close()

# ============================================================
# Plot 3: De Sitter modified temperature vs. flat Unruh
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

a_range3 = np.logspace(-14, -6, 1000)

# Top panel: temperatures
ax1.loglog(a_range3, T_U(a_range3), 'b-', linewidth=2, label='Flat Unruh $T_U(a)$')
ax1.loglog(a_range3, T_dS(a_range3, H0), 'r--', linewidth=2, label='De Sitter $T_{dS}(a, H_0)$')
ax1.axhline(y=T_GH, color='green', linestyle=':', linewidth=1.5, label=f'$T_{{GH}}$ = {T_GH:.2e} K')
ax1.axvline(x=cH0, color='orange', linestyle=':', linewidth=1.5, label=f'$cH_0$ = {cH0:.2e} m/s²')
ax1.axvline(x=a0_MOND, color='purple', linestyle='-.', linewidth=1.5, label=f'$a_0$ (MOND)')

ax1.set_xlabel('Acceleration $a$ (m/s²)', fontsize=12)
ax1.set_ylabel('Temperature (K)', fontsize=12)
ax1.set_title('De Sitter vs. Flat Unruh Temperature (zoomed to low-$a$ regime)', fontsize=13)
ax1.legend(fontsize=9, loc='upper left')
ax1.set_xlim(1e-14, 1e-6)
ax1.grid(True, alpha=0.3)

# Bottom panel: ratio T_dS / T_U
ratio = T_dS(a_range3, H0) / T_U(a_range3)
ax2.semilogx(a_range3, ratio, 'k-', linewidth=2)
ax2.axvline(x=cH0, color='orange', linestyle=':', linewidth=1.5, label=f'$cH_0$')
ax2.axvline(x=a0_MOND, color='purple', linestyle='-.', linewidth=1.5, label=f'$a_0$ (MOND)')
ax2.axhline(y=np.sqrt(2), color='gray', linestyle='--', alpha=0.5, label=f'$\\sqrt{{2}}$ (at $a = cH_0$)')
ax2.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='1 (flat limit)')

ax2.set_xlabel('Acceleration $a$ (m/s²)', fontsize=12)
ax2.set_ylabel('$T_{dS} / T_U$', fontsize=12)
ax2.set_title('Ratio: De Sitter to Flat Unruh Temperature', fontsize=13)
ax2.legend(fontsize=10)
ax2.set_xlim(1e-14, 1e-6)
ax2.set_ylim(0.9, 20)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('code/plot3_deSitter_comparison.png', dpi=150)
print("Plot 3 saved to code/plot3_deSitter_comparison.png")
plt.close()

print("\nAll plots generated successfully.")
