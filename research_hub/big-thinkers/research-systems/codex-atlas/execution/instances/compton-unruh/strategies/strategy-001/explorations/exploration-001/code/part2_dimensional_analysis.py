"""
Part 2: Dimensional analysis of the Compton-Unruh "resonance".
Answers the five key questions about what is being equated and whether it works.
"""
import numpy as np

# ============================================================
# Constants
# ============================================================
h    = 6.62607015e-34
hbar = h / (2 * np.pi)
c    = 2.99792458e8
k_B  = 1.380649e-23
m_p  = 1.67262192e-27    # proton mass
m_e  = 9.1093837015e-31  # electron mass
H0   = 2.2e-18
a0_MOND = 1.2e-10

print("=" * 70)
print("PART 2: DIMENSIONAL ANALYSIS OF THE 'RESONANCE'")
print("=" * 70)

# ============================================================
# Q1: What exactly is being equated?
# ============================================================
print("\n--- Q1: What is being equated? ---")
print("""
Three possible matching conditions:

(a) Energy matching: E_C = E_U
    mc² = ℏa/(2πc)
    => a* = 2πmc³/ℏ

(b) Wavelength matching: λ_C = λ_U
    h/(mc) = 4π²c²/a     [using λ_U = c/f_U = ch/E_U = 4π²c²/a]
    => a* = 4π²c²·mc/h = 4π²mc³/h = 4π² · mc³/(2πℏ) = 2πmc³/ℏ
    Same as (a)! This is expected: if E_C = hf_C and E_U = hf_U,
    then E_C = E_U ⟺ f_C = f_U ⟺ λ_C = λ_U.

(c) Frequency matching: f_C = f_U
    mc²/h = a/(4π²c)
    => a* = 4π²c·mc²/h = 4π²mc³/h = 2πmc³/ℏ
    Same again.

All three matching conditions give the same result:
    a* = 2πmc³/ℏ
""")

# ============================================================
# Q2: At what acceleration does matching occur?
# ============================================================
print("\n--- Q2: Matching acceleration for proton ---")

a_star_proton = 2 * np.pi * m_p * c**3 / hbar
print(f"a*(proton) = 2πm_p c³/ℏ = {a_star_proton:.6e} m/s²")
print(f"Compare to cH₀ = {c*H0:.6e} m/s²")
print(f"Compare to a₀  = {a0_MOND:.1e} m/s²")
print(f"Ratio a*(proton) / cH₀ = {a_star_proton / (c*H0):.6e}")
print(f"Ratio a*(proton) / a₀  = {a_star_proton / a0_MOND:.6e}")

# For electron
a_star_electron = 2 * np.pi * m_e * c**3 / hbar
print(f"\na*(electron) = 2πm_e c³/ℏ = {a_star_electron:.6e} m/s²")
print(f"Ratio a*(electron) / cH₀ = {a_star_electron / (c*H0):.6e}")

print(f"""
CONCLUSION: The naive Compton-Unruh matching acceleration is:
  a*(proton)   ≈ {a_star_proton:.2e} m/s²
  a₀ (MOND)    ≈ {a0_MOND:.1e} m/s²
  cH₀          ≈ {c*H0:.2e} m/s²

  a*(proton) is {a_star_proton/a0_MOND:.1e} times LARGER than a₀.
  This is a factor of ~10^{int(np.log10(a_star_proton/a0_MOND))}, an enormous discrepancy.

  The direct Compton-Unruh matching does NOT occur at a ~ cH₀.
  It occurs at an absurdly large acceleration.
""")

# ============================================================
# Q3: Does the mass drop out?
# ============================================================
print("\n--- Q3: Does the mass drop out? ---")
print("""
The matching acceleration a* = 2πmc³/ℏ is MASS-DEPENDENT.
It scales linearly with particle mass m.

For a* to equal cH₀, we would need:
  2πmc³/ℏ = cH₀
  m = ℏH₀/(2πc²)
""")

m_critical = hbar * H0 / (2 * np.pi * c**2)
print(f"Critical mass for a* = cH₀:  m_crit = ℏH₀/(2πc²) = {m_critical:.6e} kg")
print(f"                                     = {m_critical * c**2 / 1.602176634e-19:.6e} eV/c²")
print(f"Proton mass:                  m_p    = {m_p:.6e} kg")
print(f"                                     = {m_p * c**2 / 1.602176634e-19:.6e} eV/c²")
print(f"Ratio m_p / m_crit = {m_p / m_critical:.6e}")
print(f"""
The critical mass is m_crit ≈ {m_critical:.1e} kg ≈ {m_critical * c**2 / 1.602176634e-19:.1e} eV/c².
This is an extraordinarily tiny mass — about {m_p/m_critical:.0e} times smaller than the proton.
It corresponds to an energy of ~{m_critical * c**2 / 1.602176634e-19:.1e} eV.

No known particle has this mass. The mass does NOT drop out.
The resonance condition is mass-dependent and occurs at wildly different
accelerations for different particles.
""")

# ============================================================
# Q4: Where does the cosmological scale enter?
# ============================================================
print("\n--- Q4: Where does the cosmological scale enter? ---")
print("""
In the DIRECT Compton-Unruh matching (E_C = E_U), the cosmological
scale H₀ does NOT appear at all. The matching acceleration
a* = 2πmc³/ℏ involves only:
  - m (particle mass)
  - c (speed of light)
  - ℏ (Planck's constant)

These are all LOCAL, non-cosmological quantities.

The observation that a₀ ≈ cH₀ is a SEPARATE empirical fact.
The Compton-Unruh matching doesn't explain it.

For the cosmological scale to enter, one needs an ADDITIONAL ingredient.
Possible ingredients in the literature:

(1) McCulloch/QI approach: postulates that Unruh radiation wavelengths
    longer than 2R_H = 2c/H₀ are suppressed. This introduces H₀ by
    cutting off the Unruh spectrum at long wavelengths. This is a
    BOUNDARY CONDITION, not a resonance.

(2) De Sitter modification: In de Sitter spacetime, the Unruh temperature
    is modified. The detector sees a combined temperature from both
    acceleration and the cosmological horizon. This naturally mixes
    the acceleration a with H₀.

(3) Infrared cutoff: If one imposes an IR cutoff on the field modes at
    the Hubble scale, this modifies low-frequency contributions to the
    Wightman function, which could affect the detector response at
    energies E ~ ℏH₀/c (the Gibbons-Hawking energy).

None of these involve a Compton-Unruh RESONANCE in the direct sense.
""")

# ============================================================
# Q5: The role of the de Sitter horizon
# ============================================================
print("\n--- Q5: De Sitter modified temperature ---")
print("""
DERIVATION of the de Sitter modified temperature:

In de Sitter spacetime with Hubble parameter H, a uniformly accelerating
observer with proper acceleration a sees a thermal spectrum at temperature:

  T_dS(a, H) = (ℏ/(2π k_B c)) √(a² + c²H²)

This is a standard result. Here is the logic:

In de Sitter spacetime, the static metric for an observer at the origin is:
  ds² = -(1 - H²r²/c²)c²dt² + dr²/(1 - H²r²/c²) + r²dΩ²

An observer at fixed r experiences a proper acceleration (surface gravity)
  a_eff = Hr²c²/... Actually, let's derive this more carefully.

The key result comes from the Euclidean approach: the Wightman function
for a uniformly accelerating observer (proper acceleration a) in de Sitter
spacetime (Hubble parameter H) has poles in the complex τ plane at:

  τ_n = -i · 2πn / √(a²/c² + H²)     (n = 1, 2, 3, ...)

This gives a KMS (thermal) periodicity with period:
  β = 2π / √(a²/c² + H²)

and therefore a temperature:
  T = ℏ/(k_B β c) = ℏ √(a² + c²H²) / (2π k_B c)

Wait, let me be more precise about factors of c. The standard result
(Deser & Levin 1997, Narnhofer et al. 1996) states:

For an observer with proper acceleration a in de Sitter space with
Hubble constant H:
  T = (ℏ/(2π c k_B)) √(a² + c²H²)
    = (1/(2π c k_B)) √((ℏa)² + (ℏcH)²)
""")

# De Sitter temperature
def T_dS(a, H):
    """De Sitter modified Unruh temperature."""
    return hbar * np.sqrt(a**2 + (c*H)**2) / (2 * np.pi * c * k_B)

def T_U(a):
    """Flat-space Unruh temperature."""
    return hbar * a / (2 * np.pi * c * k_B)

# Check limits
print(f"Checks:")
print(f"  T_dS(a=0, H=H₀) = {T_dS(0, H0):.6e} K (should equal T_GH = {hbar*H0/(2*np.pi*k_B):.6e} K)")
print(f"  T_dS(a=1e10, H=H₀) = {T_dS(1e10, H0):.6e} K (should ≈ T_U(1e10) = {T_U(1e10):.6e} K)")
print(f"  T_dS(a=cH₀, H=H₀) = {T_dS(c*H0, H0):.6e} K")
print(f"  T_U(cH₀) = {T_U(c*H0):.6e} K")
print(f"  Ratio T_dS(cH₀)/T_U(cH₀) = {T_dS(c*H0, H0)/T_U(c*H0):.6f} (should be √2 = {np.sqrt(2):.6f})")

print(f"""
MODIFIED RESONANCE CONDITION with de Sitter temperature:

Setting T_dS = T_C (Compton temperature):
  (ℏ/(2πck_B)) √(a² + c²H₀²) = mc²/k_B
  √(a² + c²H₀²) = 2πmc³/ℏ
  a² + c²H₀² = (2πmc³/ℏ)²
  a² = (2πmc³/ℏ)² - c²H₀²

Since (2πmc³/ℏ) ≈ {2*np.pi*m_p*c**3/hbar:.2e} >> cH₀ ≈ {c*H0:.2e},
the correction from H₀ is completely negligible:
  a* = √((2πmc³/ℏ)² - c²H₀²) ≈ 2πmc³/ℏ

The de Sitter modification does NOT bring the matching acceleration
down to a ~ cH₀. The cosmological term c²H₀² is {(c*H0)**2 / (2*np.pi*m_p*c**3/hbar)**2:.2e}
times smaller than the dominant term.
""")

# What about the RATIO of de Sitter to flat Unruh temperatures?
print("The de Sitter modification is interesting at LOW accelerations:")
print(f"  When a << cH₀:")
print(f"    T_dS ≈ ℏcH₀/(2πck_B) = T_GH = {T_dS(0, H0):.2e} K")
print(f"    T_U → 0")
print(f"    T_dS/T_U → ∞ (the Gibbons-Hawking floor)")
print(f"  When a = cH₀:")
print(f"    T_dS = √2 · T_U = {T_dS(c*H0, H0):.2e} K")
print(f"  When a >> cH₀:")
print(f"    T_dS ≈ T_U (de Sitter correction negligible)")

print(f"""
KEY INSIGHT about where cosmology enters:

The de Sitter modification T_dS = (ℏ/2πck_B)√(a² + c²H²) creates a
FLOOR on the effective temperature at T_GH = ℏH/(2πk_B) ≈ {T_dS(0,H0):.1e} K.

This means: as acceleration decreases below a ~ cH₀, the thermal
environment stops getting colder. The observer is always immersed in
at least the Gibbons-Hawking thermal bath.

But this is NOT a resonance. It's a smooth transition from
acceleration-dominated thermal effects (a >> cH₀) to
cosmological-horizon-dominated thermal effects (a << cH₀).
The crossover happens at a ~ cH₀, which is suggestively close to a₀.

This crossover does NOT involve the Compton frequency at all.
""")
