"""
Part 1: Enumerate and compute all relevant scales for the Compton-Unruh resonance.
Reference particle: proton (m_p = 1.67e-27 kg).
"""
import numpy as np

# ============================================================
# Fundamental constants (CODATA 2018)
# ============================================================
h    = 6.62607015e-34   # Planck constant [J·s]
hbar = h / (2 * np.pi)  # Reduced Planck constant [J·s]
c    = 2.99792458e8      # Speed of light [m/s]
k_B  = 1.380649e-23      # Boltzmann constant [J/K]
m_p  = 1.67262192e-27    # Proton mass [kg]
H0   = 2.2e-18           # Hubble parameter [s⁻¹]  (≈ 67.4 km/s/Mpc)
a0_MOND = 1.2e-10        # MOND critical acceleration [m/s²]

print("=" * 70)
print("PART 1: ALL RELEVANT SCALES")
print("=" * 70)

# 1. Compton wavelength: λ_C = h / (mc)
lambda_C = h / (m_p * c)
print(f"\n1. Compton wavelength (proton):  λ_C = h/(m_p c) = {lambda_C:.6e} m")

# 2. Compton frequency: f_C = mc² / h
f_C = m_p * c**2 / h
print(f"2. Compton frequency (proton):   f_C = m_p c²/h = {f_C:.6e} Hz")

# 3. Compton energy: E_C = mc²
E_C = m_p * c**2
E_C_eV = E_C / 1.602176634e-19
print(f"3. Compton energy (proton):      E_C = m_p c² = {E_C:.6e} J = {E_C_eV:.6e} eV")

# 4. Unruh temperature as a function of acceleration: T_U(a) = ℏa / (2π c k_B)
def T_U(a):
    return hbar * a / (2 * np.pi * c * k_B)

# Evaluate at several accelerations
print(f"\n4. Unruh temperature T_U(a) = ℏa/(2πc k_B):")
for a_val in [1e-10, 1e-5, 1.0, 9.81, 1e10, 1e20]:
    print(f"   T_U({a_val:.1e} m/s²) = {T_U(a_val):.6e} K")

# 5. Unruh energy: E_U(a) = k_B T_U = ℏa / (2πc)
def E_U(a):
    return hbar * a / (2 * np.pi * c)

print(f"\n5. Unruh energy E_U(a) = ℏa/(2πc):")
for a_val in [1e-10, a0_MOND, 1.0, 9.81]:
    print(f"   E_U({a_val:.1e} m/s²) = {E_U(a_val):.6e} J = {E_U(a_val)/1.602176634e-19:.6e} eV")

# 6. Characteristic Unruh wavelength: λ_U(a) = c/f_U where E_U = h f_U
# So f_U = E_U / h = ℏa/(2πch) = a/(2πc · 2π) = a/(4π²c)
# Wait, let me be more careful:
# E_U = ℏa/(2πc), f_U = E_U/h = ℏa/(2πch) = a/(2πc · 2π) = a/(4π²c)
# λ_U = c/f_U = c · h / E_U = c · h · 2πc / (ℏa) = c · 2π · 2πc / a = 4π²c² / a
# Or more simply: λ_U = h/p_U? No, let's just do λ_U = c/f_U.
# f_U = E_U / h, λ_U = c / f_U = ch / E_U = ch · 2πc / (ℏa) = 2πc² · 2π / a  ...
# Let me just compute: λ_U = c / f_U, f_U = E_U/h
def f_U(a):
    return E_U(a) / h

def lambda_U(a):
    return c / f_U(a)

print(f"\n6. Characteristic Unruh wavelength λ_U(a) = ch/E_U(a):")
for a_val in [1e-10, a0_MOND, 1.0, 9.81]:
    print(f"   λ_U({a_val:.1e} m/s²) = {lambda_U(a_val):.6e} m")

# Let me also express this more simply:
# λ_U = ch/E_U = ch · 2πc / (ℏa) = 2πc² · (2π) / a  ... no
# λ_U = c / f_U = c / (E_U/h) = ch/E_U = ch/(ℏa/(2πc)) = ch·2πc/(ℏa) = 2π c h/(ℏa)
# But h = 2πℏ, so λ_U = 2π c · 2πℏ / (ℏa) = 4π²c/a
# So λ_U = 4π²c²/a  ... wait:
# λ_U = ch/(ℏa/(2πc)) = c · h · 2πc / (ℏ · a) = 2πc²h/(ℏa)
# h/ℏ = 2π, so λ_U = 2πc² · 2π / a = 4π²c²/a
# Hmm wait. Let me just check numerically at a=1:
# E_U(1) = hbar * 1 / (2*pi*c)
# f_U(1) = E_U(1)/h = hbar/(2*pi*c*h) = 1/(2*pi*c*2*pi) = 1/(4*pi^2*c)
# lambda_U(1) = c / f_U(1) = c * 4*pi^2*c = 4*pi^2*c^2
print(f"\n   Analytic check: λ_U = 4π²c²/a")
print(f"   At a=1: 4π²c² = {4*np.pi**2*c**2:.6e} m")
print(f"   lambda_U(1)    = {lambda_U(1.0):.6e} m")
# Hmm that gives ~3.56e17 m. Let me check: 4*pi^2 ~ 39.48, c^2 ~ 8.99e16
# 39.48 * 8.99e16 = 3.55e18. Yes.

# Actually wait. Let me recheck.
# f_U = E_U/h. But the "thermal" frequency might be better defined as f_U = k_B T_U / h.
# That's the same thing since E_U = k_B T_U by definition.
#
# But perhaps a more physical definition uses the PEAK wavelength of the thermal spectrum.
# Wien's law: λ_peak = b/T where b = 2.898e-3 m·K.
# Or perhaps we should use ω = k_B T / ℏ as the characteristic angular frequency.
# That gives ω_U = a/(2πc), f_U = ω_U/(2π) = a/(4π²c), same as above.
#
# The Unruh spectrum peak (for a massless scalar) is at ω_peak ≈ k_B T / ℏ times some O(1) factor.
# For our purposes the exact O(1) factor doesn't matter for the dimensional analysis.

# 7. De Sitter (Hubble) radius: R_H = c/H₀
R_H = c / H0
print(f"\n7. Hubble radius:   R_H = c/H₀ = {R_H:.6e} m")
print(f"                         = {R_H / (3.086e22):.2f} Gpc")
print(f"                         = {R_H / 9.461e15:.2e} light-years")

# 8. Gibbons-Hawking temperature: T_GH = ℏH₀/(2πk_B)
T_GH = hbar * H0 / (2 * np.pi * k_B)
print(f"\n8. Gibbons-Hawking temperature: T_GH = ℏH₀/(2πk_B) = {T_GH:.6e} K")

# 9. MOND critical acceleration
print(f"\n9. MOND critical acceleration: a₀ = {a0_MOND:.1e} m/s²")

# 10. cH₀ and comparison to a₀
cH0 = c * H0
print(f"\n10. cH₀ = {cH0:.6e} m/s²")
print(f"    a₀/cH₀ = {a0_MOND/cH0:.4f}")
print(f"    cH₀/a₀ = {cH0/a0_MOND:.4f}")
print(f"    Ratio: a₀ ≈ {a0_MOND/cH0:.2f} × cH₀")

# Additional derived quantities
print(f"\n{'=' * 70}")
print(f"ADDITIONAL DERIVED QUANTITIES")
print(f"{'=' * 70}")

# Unruh temperature at a = cH₀
T_U_cH0 = T_U(cH0)
print(f"\nUnruh temperature at a = cH₀: T_U(cH₀) = {T_U_cH0:.6e} K")
print(f"Gibbons-Hawking temperature:   T_GH     = {T_GH:.6e} K")
print(f"Ratio T_U(cH₀)/T_GH = {T_U_cH0/T_GH:.6f}")
print(f"(These are equal by construction: T_U(a) = ℏa/(2πck_B), T_GH = ℏH₀/(2πk_B), so T_U(cH₀) = ℏcH₀/(2πck_B) = ℏH₀/(2πk_B) = T_GH)")

# Compton temperature equivalent: T_C = mc²/k_B
T_C = m_p * c**2 / k_B
print(f"\nCompton 'temperature' (proton): T_C = m_p c²/k_B = {T_C:.6e} K")
print(f"Ratio T_C / T_GH = {T_C/T_GH:.6e}")
print(f"Ratio T_C / T_U(cH₀) = {T_C/T_U_cH0:.6e}")

print(f"\n{'=' * 70}")
print("SUMMARY TABLE")
print(f"{'=' * 70}")
print(f"{'Quantity':<40} {'Value':<25} {'Units'}")
print(f"{'-'*40} {'-'*25} {'-'*10}")
print(f"{'Proton Compton wavelength λ_C':<40} {lambda_C:<25.6e} {'m'}")
print(f"{'Proton Compton frequency f_C':<40} {f_C:<25.6e} {'Hz'}")
print(f"{'Proton Compton energy E_C':<40} {E_C:<25.6e} {'J'}")
print(f"{'Proton Compton energy E_C':<40} {E_C_eV:<25.6e} {'eV'}")
print(f"{'T_U at a = a₀(MOND)':<40} {T_U(a0_MOND):<25.6e} {'K'}")
print(f"{'T_U at a = cH₀':<40} {T_U_cH0:<25.6e} {'K'}")
print(f"{'Gibbons-Hawking temperature T_GH':<40} {T_GH:<25.6e} {'K'}")
print(f"{'Hubble radius R_H':<40} {R_H:<25.6e} {'m'}")
print(f"{'MOND a₀':<40} {a0_MOND:<25.6e} {'m/s²'}")
print(f"{'cH₀':<40} {cH0:<25.6e} {'m/s²'}")
print(f"{'a₀ / cH₀':<40} {a0_MOND/cH0:<25.6f} {''}")
print(f"{'Unruh wavelength at a₀':<40} {lambda_U(a0_MOND):<25.6e} {'m'}")
print(f"{'Hubble radius R_H':<40} {R_H:<25.6e} {'m'}")
print(f"{'λ_U(a₀) / R_H':<40} {lambda_U(a0_MOND)/R_H:<25.6f} {''}")
