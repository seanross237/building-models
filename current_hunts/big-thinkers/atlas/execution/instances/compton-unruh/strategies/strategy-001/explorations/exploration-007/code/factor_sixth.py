"""
Part 2: The Factor of 1/6 (or 1/(2π)) Origin Analysis
======================================================
Why does T_U/T_dS give a₀ = cH₀ (too large by 5.7×),
while Verlinde gets a₀ = cH₀/(2π) ≈ cH₀/6.28?

This script traces:
1. Dimensional analysis of where factors come from
2. Verlinde's area-vs-volume entropy derivation
3. Whether T_U/T_dS can naturally produce 1/(2π)
4. The 3D solid angle / geometric factor analysis
"""

import numpy as np
import sympy as sp
from sympy import symbols, sqrt, simplify, pi, log, Rational, exp, latex

print("="*70)
print("PART 2: The Factor of 1/6 (1/(2π)) — Origin Analysis")
print("="*70)

# Physical constants
c = 2.998e8    # m/s
hbar = 1.055e-34  # J·s
kB = 1.381e-23    # J/K
G = 6.674e-11    # m³/(kg·s²)
lP = np.sqrt(G * hbar / c**3)  # Planck length ~1.616e-35 m
H0 = 2.268e-18   # s⁻¹
Msun = 1.989e30   # kg

a0_cH0 = c * H0
a0_Verlinde = c * H0 / (2 * np.pi)
a0_MOND = 1.2e-10

print(f"\nFundamental scales:")
print(f"  lP = {lP:.3e} m (Planck length)")
print(f"  RH = c/H₀ = {c/H0:.3e} m (Hubble radius)")
print(f"  cH₀ = {a0_cH0:.3e} m/s²")
print(f"  cH₀/(2π) = {a0_Verlinde:.3e} m/s²")
print(f"  a₀(MOND obs) = {a0_MOND:.3e} m/s²")
print(f"  Ratio cH₀/a₀_obs = {a0_cH0/a0_MOND:.2f}")
print(f"  Ratio cH₀/a₀_Verlinde = {a0_cH0/a0_Verlinde:.4f} = 2π = {2*np.pi:.4f}")

# ============================================================
# SECTION 2.1: Unruh and Gibbons-Hawking Temperature Formulas
# ============================================================
print("\n--- 2.1 Temperature Formulas ---\n")

print("""
Unruh temperature for proper acceleration a:
    T_U = ℏa / (2πk_B c)

Gibbons-Hawking (de Sitter) temperature for Hubble constant H₀:
    T_dS = ℏH₀ / (2πk_B)

The ratio:
    T_U/T_dS = a / (c H₀)    [the 2π factors cancel]

So T_U/T_dS = a/(cH₀), and the crossover a₀ where T_U = T_dS is:
    T_U = T_dS  ⟹  a/(cH₀) = 1  ⟹  a = cH₀

KEY: The factor of 2π appears in BOTH T_U and T_dS with the SAME sign,
so it cancels in the ratio. There is NO 1/(2π) suppression from the
temperature formulas alone.
""")

# ============================================================
# SECTION 2.2: Verlinde's Area vs. Volume Entropy Argument
# ============================================================
print("\n--- 2.2 Verlinde's Area-Volume Entropy Competition ---\n")

print("""
Verlinde (2016) derives apparent dark matter from the elasticity of
de Sitter entanglement entropy. Key steps:

1. De Sitter horizon area:  A_H = 4π R_H²  where R_H = c/H₀
   Horizon entropy: S_H = A_H/(4G/ℏc) = πR_H²c³/(Gℏ) = πc⁵/(GH₀²ℏ)

2. For a sphere of radius r around baryonic mass M_B:
   Surface entropy (area):    S_area = πr²c³/(Gℏ)   [general formula]
   Volume entropy displacement: ΔS_vol = (4/3)πr³ × s_vol

   where s_vol = S_H / V_H = [πR_H²c³/(Gℏ)] / [4πR_H³/3]
               = 3c³/(4GℏR_H)  = 3H₀c²/(4Gℏ)

   So ΔS_vol = (4/3)πr³ × 3H₀c²/(4Gℏ) = πr³H₀c²/(Gℏ)

3. Crossover radius r* where S_area = ΔS_vol:
   πr*²c³/(Gℏ) = πr*³H₀c²/(Gℏ)
   r*c = r*²H₀
   r* = c/H₀ = R_H

   Hmm — this gives r* = R_H, not a small scale. Let me be more careful.

4. The baryonic matter DISPLACES entropy from the volume.
   The displacement per unit mass: ΔS_B/M_B = ?

   The key Verlinde formula involves the strain in the entropy medium:
   Σ_D(r)² = c H₀ Σ_B(r) / (8πG)

   where Σ_D is the "dark matter" surface density and Σ_B is the
   baryonic surface density. This gives the apparent MOND force.

   From this: g_D ≈ √(g_B × cH₀/(2π))

   Comparing with MOND: g_D = √(g_B × a₀)
   We get: a₀ = cH₀/(2π)
""")

# Compute Verlinde's formula explicitly
print("Verlinde's surface density formula:")
print("  Σ_D² = (cH₀/8πG) × Σ_B")
print("\nFor a point mass M at radius r:")
M_test = 1e11 * Msun   # 10^11 solar masses
r_test = 8e3 * 3.086e19  # 8 kpc in meters

Sigma_B = M_test / (4 * np.pi * r_test**2)  # surface density
Sigma_D_sq = (c * H0 / (8 * np.pi * G)) * Sigma_B
Sigma_D = np.sqrt(Sigma_D_sq)
M_D = 4 * np.pi * r_test**2 * Sigma_D  # apparent dark mass
g_D = G * M_D / r_test**2   # dark matter acceleration

g_B = G * M_test / r_test**2
g_MOND = np.sqrt(g_B * a0_MOND)
g_Verlinde_calc = np.sqrt(g_B * a0_Verlinde)

print(f"\nTest: M = 10¹¹ M☉, r = 8 kpc")
print(f"  g_B = {g_B:.3e} m/s²")
print(f"  Verlinde g_D = {g_D:.3e} m/s²")
print(f"  MOND g_D = √(g_B × a₀) = {g_MOND:.3e} m/s²")
print(f"  With a₀=cH₀/(2π): g_D = {g_Verlinde_calc:.3e} m/s²")
print(f"  Verlinde/MOND = {g_D/g_MOND:.3f}")
print(f"  Note: Verlinde formula uses Σ, not point mass → not exact here")

# ============================================================
# SECTION 2.3: Can T_U/T_dS Produce 1/(2π)?
# ============================================================
print("\n--- 2.3 Can T_U/T_dS Produce the 1/(2π) Factor? ---\n")

print("""
Approach A: Modified Unruh formula with angular averaging
-----------------------------------------------------------
In 3+1D, if we average the Unruh effect over all solid angles (not just
along the acceleration axis), the effective thermal bath has:
    T_U^(effective) = T_U / (2π)  ?

NO — this doesn't work. The Unruh temperature T_U = ℏa/(2πk_B c) is
already the KMS temperature of the Rindler vacuum in 3+1D. There is no
additional angular averaging to perform.

Approach B: Rindler horizon area vs. de Sitter horizon area
------------------------------------------------------------
The Rindler horizon area for an accelerating observer with acceleration a:
  The local Rindler horizon is at a distance l_R = c²/a from the observer.
  Area of Rindler horizon (at distance l_R): A_R = π l_R² = πc⁴/a²
  (using only the relevant transverse area at the horizon)

  Actually, the Rindler horizon is an infinite plane — its area is
  infinite. We need to regularize using the de Sitter cutoff.

  Finite area using de Sitter cutoff: A_R(regulated) = π R_H² = πc²/H₀²

  De Sitter horizon area: A_H = 4πR_H² = 4πc²/H₀²

  Ratio: A_R/A_H = 1/4  (not 1/(2π))

Approach C: Entropy rate ratio
-------------------------------
The Unruh entropy production rate:
  dS_U/dτ = (k_B/ℏ) × (a/c) × (A_cross / (2π))

The de Sitter entropy:
  S_dS = A_H / (4G/ℏc) = πc⁵/(GH₀²ℏ)

Taking ratio of entropy scales:
  ΔS_U/ΔS_dS ~ ?

This doesn't naturally give 1/(2π) either.

Approach D: Quantum information — Rindler reduced density matrix
----------------------------------------------------------------
For the Minkowski vacuum, the Rindler reduced density matrix is thermal
with temperature T_U = ℏa/(2πk_B c).
The von Neumann entropy is: S_R = (π²/3) × (k_B T_U) × A_R / (ℏc)

For the de Sitter vacuum:
  S_dS = (π²/3) × (k_B T_dS) × A_dS / (ℏc)

The ratio of effective "thermal bath capacities" involves
A_R/A_dS = (c²/a²)/(c²/H₀²) = H₀²/a²

This gives: S_R/S_dS ~ (a/cH₀) × (H₀/a)² = H₀/(ac)  → growing at small a.
Not the MOND formula.

CONCLUSION on 1/(2π):
The ratio T_U/T_dS = a/(cH₀) has NO 1/(2π) suppression from the
temperature formulas alone.

The 1/(2π) (Verlinde's factor) comes from:
  - The competition between surface entropy (∝ r²) and volume entropy (∝ r³)
  - The boundary sphere contributes 4π from the solid angle in 3D
  - The "elastic medium" interpretation of the de Sitter entanglement

This factor CANNOT be derived from the T_U/T_dS ratio alone. It must
be imported from Verlinde's geometric argument or an equivalent.
""")

# ============================================================
# SECTION 2.4: What Factor CAN T_U/T_dS Framework Produce?
# ============================================================
print("\n--- 2.4 Modified T_U/T_dS: Finding the Right Factor ---\n")

print("""
The T_U formula uses the 1D (axial) acceleration temperature.
In 3D, the actual Unruh thermal bath is isotropic in the transverse
plane but directional along the acceleration axis.

However, there IS a natural geometric factor from the 4π solid angle:

If we use the Unruh formula for a DETECTOR sensitive to radiation from
all directions (not just the forward hemisphere):
  T_U^(isotropic) = ℏa/(2πk_B c)   [standard Unruh, already 4D]

And the de Sitter temperature:
  T_dS = ℏH₀/(2πk_B)   [Gibbons-Hawking]

Both include the 2π in the denominator (from the standard derivations).
Their ratio: T_U/T_dS = a/(cH₀)   [no extra factor]

What if we use the de Sitter temperature formula FROM THE HUBBLE HORIZON ENTROPY?

  S_H = A_H/(4G/ℏc) = 4πR_H²/(4G/ℏc) = πR_H²ℏc/G

  The "de Sitter acceleration" at the horizon:
  a_dS = c²/R_H = cH₀

  This gives T_dS = ℏa_dS/(2πk_Bc) = ℏcH₀/(2πk_Bc) = ℏH₀/(2πk_B) ✓

  Alternative: if we treat the Hubble horizon as a 2-sphere and use
  the holographic entropy with a normalization factor (4π vs π):

  S_H^(alternative) = A_H/G = 4πR_H²/G  (factor of 4 difference)

  This would give T_dS^(alt) = ℏH₀/(8πk_B)

  Then T_U/T_dS^(alt) = 4a/(cH₀)   → wrong direction (makes a₀ even smaller)

What about the Bekenstein-Mukhanov factor?
The de Sitter temperature can alternatively be written using
the first law of de Sitter thermodynamics:
  dE = T_dS dS - p dV = 0

For the de Sitter space: p = ρΛ c² = (Λc⁴)/(8πG) (equation of state p = -ρ)
This is a different approach that gives the same Gibbons-Hawking T.

BOTTOM LINE: No geometric manipulation of T_U/T_dS gives a factor of 1/(2π).
The formula T_U/T_dS = a/(cH₀) is robust. The 1/(2π) is external.
""")

# ============================================================
# SECTION 2.5: Possibility — Modified inertia formula
# ============================================================
print("\n--- 2.5 Can the formula m_i = m × f(T_U/T_dS) give the right a₀? ---\n")

print("""
Suppose instead of m_i = m × T_U/T_dS, we use:
    m_i = m × (T_U/T_dS) / (1 + T_U/T_dS)

This gives:
    m_i/m = (a/cH₀) / (1 + a/cH₀) = a / (a + cH₀)

The force equation:
    m_i × a = m × (a²/(a + cH₀)) = g_N m

Solving: a² = g_N (a + cH₀)
         a² - g_N a - g_N cH₀ = 0
         a = (g_N + √(g_N² + 4g_N cH₀)) / 2

For g_N << cH₀: a ≈ √(g_N × cH₀) → still a₀ = cH₀

The functional form doesn't help — a₀ is set by the scale where T_U = T_dS,
and the only way to shift it is to modify the temperature normalization.
""")

# Compute a₀ for various possible modifications
print("Comparing a₀ for different T_U/T_dS normalizations:")
print(f"\nStandard: T_U/T_dS = a/(cH₀)")
print(f"  → a₀ = cH₀ = {a0_cH0:.3e} m/s²  (5.7× too large)")

print(f"\nWith 1/(2π) correction: T_U/T_dS = a/(2π cH₀)")
a0_2pi = a0_cH0 / (2 * np.pi)
print(f"  → a₀ = cH₀/(2π) = {a0_2pi:.3e} m/s²  (ratio to obs: {a0_2pi/a0_MOND:.2f})")

print(f"\nWith 1/6 correction: T_U/T_dS = a/(6 cH₀)")
a0_6 = a0_cH0 / 6
print(f"  → a₀ = cH₀/6 = {a0_6:.3e} m/s²  (ratio to obs: {a0_6/a0_MOND:.2f})")

print(f"\nWith 1/(2π)² correction: T_U/T_dS = a/((2π)² cH₀)")
a0_4pi2 = a0_cH0 / (4 * np.pi**2)
print(f"  → a₀ = cH₀/(4π²) = {a0_4pi2:.3e} m/s²  (ratio to obs: {a0_4pi2/a0_MOND:.2f})")

print(f"\nObservational: a₀ = {a0_MOND:.3e} m/s²")
print(f"Best match: cH₀/(2π) with ratio {a0_2pi/a0_MOND:.3f} (Verlinde)")

# ============================================================
# SECTION 2.6: Geometric Factor from de Sitter vs. Rindler Mode Counting
# ============================================================
print("\n--- 2.6 Mode Counting: Where 1/(2π) Could Enter ---\n")

print("""
The Unruh effect temperature T_U = ℏa/(2πk_B c) comes from:
  - KMS condition for the Rindler vacuum
  - The factor 2π comes from the Fourier transform: τ → ω
  - For a periodic (KMS) state: β = 2π/a (in c=ℏ=kB=1 units)

The de Sitter temperature T_dS = ℏH₀/(2πk_B) comes from:
  - Gibbons-Hawking temperature of the de Sitter horizon
  - Same 2π factor from the same mathematical origin
  - They cancel in the ratio.

BUT: In Verlinde's approach, the relevant thermal length is not 1/T
but rather the thermal wavelength λ_T = ℏc/(k_B T).

For Unruh:    λ_T^U = 2πc²/a   [Rindler "horizon distance"]
For de Sitter: λ_T^dS = 2πc/H₀ = 2πR_H

If the MOND-like modification comes from comparing the number of modes
that fit in the thermal volume:

N_modes^U = V / λ_T^U³ ~ (r³) / (c²/a)³
N_modes^dS = V / λ_T^dS³ ~ (R_H³) / (2πR_H)³ = 1/(2π)³

This doesn't cleanly give 1/(2π) for the crossover acceleration.

CONCLUSION: The factor 1/(2π) in Verlinde's formula comes from the
geometry of the de Sitter entropy (area vs. volume competition), which
is NOT encoded in the temperature ratio T_U/T_dS.

The T_U/T_dS framework NEEDS an external input (from Verlinde or equivalent)
to get the correct a₀. This is a genuine gap in the framework.
""")

# ============================================================
# SECTION 2.7: Starkman-Vachaspati "dark mass" computation
# ============================================================
print("\n--- 2.7 Numerical check: What factor is needed for exact a₀? ---\n")

a0_needed = a0_MOND
factor_needed = a0_cH0 / a0_needed
print(f"Factor needed to reduce cH₀ to a₀_obs:")
print(f"  cH₀ / a₀_obs = {factor_needed:.3f}")
print(f"  2π = {2*np.pi:.3f}")
print(f"  4π/√3 = {4*np.pi/np.sqrt(3):.3f}")
print(f"  2π × 0.9 = {2*np.pi*0.9:.3f}")
print(f"  6 = 6.000")
print(f"  √(4π) = {np.sqrt(4*np.pi):.3f}")
print(f"  2π (Verlinde) = {2*np.pi:.3f} → a₀ = {a0_cH0/(2*np.pi):.3e}")
print(f"\nBest fit: 2π (Verlinde) gives ratio {a0_cH0/(2*np.pi)/a0_MOND:.3f} × a₀_obs")
print(f"  (9.8% below observed — within galaxy-to-galaxy variation)")

print("\n" + "="*70)
print("SUMMARY: Factor of 1/6 = 1/(2π) Analysis")
print("="*70)
print("""
1. The T_U/T_dS ratio = a/(cH₀) has NO suppression factor.
   Both T_U and T_dS have the same 2π in denominator; they cancel.

2. Verlinde's 1/(2π) comes from comparing:
   - Area entropy: S ∝ r²   (holographic, Bekenstein-like)
   - Volume entropy: S ∝ r³  (de Sitter bulk, Hubble volume)
   The crossover involves 4π (solid angle) divided by the 3D volume factor,
   giving a net 1/(2π) when expressed as an acceleration scale.

3. The T_U/T_dS framework CANNOT derive this factor internally.
   It needs Verlinde's geometric argument as an external input.
   This is a genuine gap: the model predicts a₀ = cH₀ without help.

4. With the Verlinde correction (treated as external):
   a₀ = cH₀/(2π) = 1.08×10⁻¹⁰ m/s² — within 10% of observations.

5. The formula m_i = m × g_N/√(g_N² + (cH₀/(2π))²) fits galaxy data
   (from exploration-006: χ²/dof ~ 0.5-1.2 for NGC 3198, NGC 2403).
""")
