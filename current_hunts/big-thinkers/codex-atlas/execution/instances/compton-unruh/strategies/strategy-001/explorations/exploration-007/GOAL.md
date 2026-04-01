# Exploration 007 — Free-Fall Objection: De Sitter-Relative Acceleration and the Factor of 1/6

## Mission Context

We are investigating modified dynamics at low accelerations from de Sitter vacuum effects.

**ACCUMULATED FINDINGS (explorations 001-006):**
1. The identity T_U(a)/T_dS(a) = a/√(a²+c²H₀²) equals the MOND interpolation function μ(a/cH₀). This appears novel (Milgrom 1999 used a different formula).
2. If inertial mass m_i = m × T_U/T_dS, the model gives exact standard MOND, BTFR, and solar system consistency.
3. BUT: a₀ = cH₀ is 5.5× too large. Verlinde's factor gives cH₀/6 ≈ 1.1×10⁻¹⁰ which matches observations.
4. No first-principles derivation of m_i = m × T_U/T_dS exists. FDT route is closed.
5. **THE DOMINANT OBSTACLE**: Stars in galaxies are in free fall (zero proper acceleration). The Unruh effect requires proper acceleration. How can T_U(a) apply to freely-falling stars? This has been an unresolved objection for 25 years (Milgrom 1999 flagged it).

## Your Task

This is a **computation and derivation** task. Use Python (sympy, numpy, scipy) for all calculations. Working directory: compton-unruh/strategies/strategy-001/. Write ALL output to explorations/exploration-007/.

### Part 1: De Sitter-Relative Acceleration

A star orbiting in a galaxy is in free fall (zero proper acceleration in GR). But it is NOT in free fall relative to the de Sitter background (the Hubble flow). The key question: what is the COVARIANT acceleration of an orbital star relative to the de Sitter background?

1. **Setup**: Consider Schwarzschild-de Sitter spacetime (a central mass M with cosmological constant Λ). A star on a circular orbit at radius r has a 4-velocity u^μ. Compute:
   - The 4-acceleration a^μ = u^ν ∇_ν u^μ (should be zero for geodesic motion)
   - The "de Sitter-relative acceleration": the deviation of the star's worldline from the nearest Hubble flow worldline. This is NOT the proper acceleration — it's the acceleration relative to the cosmological rest frame.

2. **Explicit computation**: For a circular geodesic in Schwarzschild-de Sitter:
   - The Newtonian gravitational acceleration is g_N = GM/r²
   - The de Sitter expansion acceleration at radius r is H₀²r/2 (from Λ)
   - What is the net "de Sitter-relative acceleration" experienced by the star?
   - In the limit Λ → 0, this should reduce to g_N = GM/r²
   - In the limit M → 0, this should reduce to zero (a Hubble-flow observer is at rest in de Sitter)

3. **The key question**: Is the de Sitter-relative acceleration equal to g_N (the Newtonian gravitational acceleration) for a star in a galaxy? If yes, this resolves the free-fall objection: you can replace "proper acceleration a" in the T_U/T_dS formula with "Newtonian acceleration g_N", and the formula becomes:

   m_i = m × g_N/√(g_N² + c²H₀²) = m × μ(g_N/cH₀)

   This is exactly the MOND formula with g_N playing the role of a.

4. **Rigorous test**: Compute this for:
   - A star at r = 8 kpc from a galaxy center with M = 10¹¹ M_sun
   - The Sun at r = 1 AU from the Sun (to check solar system limit)
   - A star at r = 50 kpc (deep MOND regime)

### Part 2: The Factor of 1/6

The T_U/T_dS identity gives a₀ = cH₀ ≈ 6.6×10⁻¹⁰ m/s², but observations require a₀ ≈ 1.2×10⁻¹⁰ m/s² (ratio ≈ 5.5). Verlinde gets a₀ = cH₀/6 from his entropic argument. Investigate where the factor of 1/6 (or 1/2π) comes from:

1. **Dimensional origin**: In de Sitter space, the Hubble radius is R_H = c/H₀. The de Sitter radius is L = √(3/Λ) = c√(3)/H₀√(3) = c/H₀ (for Ω_Λ = 1). The horizon area is A = 4πR_H². The horizon entropy is S = A/(4l_P²). How do these factors propagate into a₀?

2. **3D vs. 1D formulation**: The temperature ratio T_U/T_dS uses 1D quantities (acceleration along one direction). In 3D, the Unruh radiation is isotropic in the transverse plane but directional along the acceleration axis. Does accounting for spatial dimensions introduce a factor of 1/(2π) or 1/6?

3. **Verlinde's specific factor**: In Verlinde (2016), a₀ = cH₀/(2π) comes from comparing area entropy (proportional to surface area 4πr²) to volume entropy (proportional to volume 4πr³/3). The transition occurs when ΔS_area = ΔS_volume, giving r* = 3L/(2π)... trace through how this gives the 1/6 factor and whether the T_U/T_dS approach can incorporate it.

4. **Modified formula**: If the corrected formula is:

   m_i = m × g_N/√(g_N² + (cH₀/6)²)

   compute rotation curves for NGC 3198 (M_disk = 3.2×10¹⁰ M_sun, R_d = 3.5 kpc) and compare to MOND with a₀ = 1.2×10⁻¹⁰. What is the χ² residual?

### Part 3: Jacobson Local Rindler Interpretation

An alternative resolution to the free-fall objection:

1. **Jacobson (1995)**: Derived Einstein's equations from local Rindler horizons. In his framework, each spacetime point has an associated family of accelerating observers (local Rindler observers) with Unruh temperature T = ℏa/(2πck_B).

2. **For a freely-falling star in a galaxy**: The local Rindler acceleration associated with the gravitational field at radius r is a_Rindler ~ g_N = GM/r². Even though the star is in free fall, the local curvature defines a natural acceleration scale.

3. **Is a_Rindler = g_N?**: Verify this explicitly. In Jacobson's framework, the relevant acceleration is that of the accelerating observers who define the local Rindler horizon, not the proper acceleration of the test particle. This may resolve the free-fall objection.

### Part 4: Synthesis

1. **Does the de Sitter-relative acceleration equal g_N?** Clear answer with explicit computation.
2. **Can the factor of 1/6 be derived from the T_U/T_dS framework?** Or must it be imported from Verlinde?
3. **Which resolution of the free-fall objection is more rigorous** — de Sitter-relative acceleration or Jacobson local Rindler?
4. **If both work, are they equivalent?**

## Success Criteria
- De Sitter-relative acceleration computed for at least 2 of the 3 test cases
- Factor of 1/6 origin analyzed (even if not fully derived)
- At least one resolution of the free-fall objection proposed with explicit equations
- Clear assessment of whether the free-fall objection is resolved

## Failure Criteria
- If the de Sitter-relative acceleration is NOT equal to g_N, that's a valuable negative result.
- If the factor of 1/6 can't be derived from T_U/T_dS, document exactly why — this would mean the identity needs an external input.

## Deliverables
Write to:
- `explorations/exploration-007/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-007/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
- `explorations/exploration-007/code/` — all Python scripts
