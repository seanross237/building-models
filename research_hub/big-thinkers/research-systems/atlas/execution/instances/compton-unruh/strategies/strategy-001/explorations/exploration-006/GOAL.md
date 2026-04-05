# Exploration 006 — Fluctuation-Dissipation Mechanism and SPARC Galaxy Fits

## Mission Context

We are investigating modified dynamics from de Sitter vacuum effects at low accelerations.

**KEY PRIOR RESULTS:**
1. The ratio T_U(a)/T_dS(a) = a/√(a²+c²H₀²) equals the MOND interpolation function μ(a/cH₀) (Expl. 004)
2. The naive entropic approach F ~ T_dS gives the WRONG SIGN (anti-MOND) (Expl. 004)
3. No first-principles derivation exists for m_i = m × T_U/T_dS (Expl. 004)
4. The predicted a₀ = cH₀ is 5.5× too large; Verlinde's factor gives cH₀/6 within 8% (Expl. 004)

## Your Task

This is a **computation and derivation** task. Use Python (sympy, numpy, scipy, matplotlib). Working directory: compton-unruh/strategies/strategy-001/. Write ALL output to explorations/exploration-006/.

### Part 1: Fluctuation-Dissipation Theorem in de Sitter

The fluctuation-dissipation theorem (FDT) relates the response function to the power spectrum. In flat space:

    χ''(ω) = (1/(2k_BT)) * S(ω)    (classical FDT)

where χ'' is the dissipative part of the susceptibility and S(ω) is the spectral density.

In the Unruh context, the FDT connects the detector response to vacuum fluctuations. The question: does the de Sitter modification of the vacuum state change the FDT in a way that modifies the effective inertia?

1. **Write down the FDT for an Unruh-DeWitt detector** in flat space (Rindler). The detector response is thermal at T_U. The fluctuation-dissipation relation should give F = ma as a consistency check (Unruh 1976, DeWitt 1979).

2. **Modify for de Sitter.** The detector is now in de Sitter space with acceleration a. The temperature is T_dS. How does the FDT change? Specifically:
   - Does the response function change?
   - Does the dissipation kernel change?
   - Does the effective mass extracted from the FDT depend on T_U/T_dS?

3. **The key calculation**: In the FDT, the response function couples to the spectral density. If the spectral density is Planckian at T_dS but the dissipation channel is set by the acceleration (through T_U), does the effective damping coefficient go as T_U/T_dS?

4. **Compute explicitly**: If f = −γ_eff × v where γ_eff is the effective damping from vacuum fluctuations, compute γ_eff(a) in both flat and de Sitter. Take the ratio γ_dS/γ_flat.

### Part 2: Stochastic dynamics approach

An alternative route: treat the detector as undergoing Brownian motion in the vacuum thermal bath.

1. **Langevin equation**: ṗ = F_ext − γv + η(t), where η is noise from vacuum fluctuations.
2. **In flat Rindler**: γ and η are determined by T_U. The FDT gives ⟨η²⟩ ∝ γ × T_U.
3. **In de Sitter**: η is determined by T_dS but γ may still be set by T_U (since the dissipation is through the acceleration-dependent coupling to the field). This would give:
   - ⟨η²⟩ ∝ γ × T_dS (fluctuations from de Sitter bath)
   - Effective temperature = T_dS
   - But effective mass (from γ) scales with T_U
4. **Check**: Does the Langevin equation with T_dS fluctuations and T_U dissipation give an effective m_i = m × T_U/T_dS?

### Part 3: SPARC Galaxy Rotation Curve Fits

Independently of the mechanism question, test the ratio model against real data.

Using Python, compute rotation curves for 2-3 well-known galaxies and compare to MOND:

1. **NGC 3198** — one of the best-studied rotation curves
   - Baryonic mass distribution: exponential disk with R_d ≈ 3.5 kpc, M_disk ≈ 2×10¹⁰ M_sun
   - Compute v(r) for: Newton, MOND (a₀=1.2×10⁻¹⁰), this model (a₀=cH₀), this model (a₀=cH₀/6)
   - Compare to observed v(r) ~ 150 km/s at 30 kpc

2. **NGC 2403** — another benchmark galaxy
   - M_disk ≈ 2.5×10⁹ M_sun, R_d ≈ 2.0 kpc
   - Same comparisons as above

3. **For each galaxy**: Compute the acceleration profile g_N(r) and mark where it crosses a₀. How much of the galaxy is in the "MOND regime"?

4. **Compute residuals**: For the ratio model with a₀ as a free parameter, what is the best-fit a₀? Does fitting a₀ to the data give a value between cH₀ and cH₀/6?

### Part 4: Synthesis

1. **Does the FDT give T_U/T_dS?** Definitive answer, even if "no" or "inconclusive".
2. **Do the galaxy fits work?** χ² or equivalent metric.
3. **What is the most promising route to a first-principles derivation?** Based on what you tried.

## Success Criteria
- FDT written down for Rindler and de Sitter cases
- At least one approach to deriving the ratio formula attempted
- Rotation curves for at least 1 galaxy computed and compared to MOND
- Clear assessment of whether the FDT route works

## Failure Criteria
- If the FDT gives F ~ T_dS (wrong sign), that confirms the sign problem is robust. Document it.
- If rotation curves don't match, identify where the model fails.

## Deliverables
Write to:
- `explorations/exploration-006/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-006/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
- `explorations/exploration-006/code/` — all Python scripts
