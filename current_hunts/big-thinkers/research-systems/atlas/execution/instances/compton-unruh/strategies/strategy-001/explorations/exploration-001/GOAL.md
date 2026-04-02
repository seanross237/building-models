# Exploration 001 — Dimensional Analysis and Scale Identification for the Compton-Unruh Resonance

## Mission Context

We are investigating the hypothesis that a resonance between a particle's Compton frequency and the Unruh radiation seen by an accelerating observer modifies inertia at very low accelerations (a ~ cH₀), potentially explaining galaxy rotation curves without dark matter.

Every massive particle oscillates at its Compton frequency: f_C = mc²/h. The Unruh effect predicts that an accelerating observer sees thermal radiation at temperature T_U = ℏa/(2πck_B). At very low accelerations, the characteristic Unruh wavelength becomes very large. The hypothesis claims a resonance occurs when this Unruh scale matches the Compton scale, at an acceleration a₀ ~ cH₀ ≈ 7×10⁻¹⁰ m/s².

Additionally, in de Sitter spacetime (our universe with positive cosmological constant Λ), there is a Gibbons-Hawking temperature T_GH = ℏH/(2πk_B) associated with the cosmological horizon. This introduces another thermal scale.

## Your Task

This is a **computation and derivation task**, not a survey. Use Python (numpy, scipy, sympy) for all calculations.

### Part 1: Enumerate and compute all relevant scales

Using Python, compute explicit numerical values for a particle of mass m (use the proton as the reference case, m_p = 1.67×10⁻²⁷ kg):

1. **Compton wavelength**: λ_C = h/(mc)
2. **Compton frequency**: f_C = mc²/h
3. **Compton energy**: E_C = mc²
4. **Unruh temperature as a function of acceleration**: T_U(a) = ℏa/(2πck_B)
5. **Unruh energy**: E_U(a) = k_B T_U = ℏa/(2πc)
6. **Characteristic Unruh wavelength**: λ_U(a) = c/f_U where f_U comes from E_U = hf_U
7. **De Sitter (Hubble) radius**: R_H = c/H₀ (use H₀ = 2.2×10⁻¹⁸ s⁻¹)
8. **Gibbons-Hawking temperature**: T_GH = ℏH₀/(2πk_B)
9. **MOND critical acceleration**: a₀ ≈ 1.2×10⁻¹⁰ m/s²
10. **cH₀**: compute this and compare to a₀

### Part 2: Dimensional analysis of the "resonance"

Answer these questions with explicit calculations:

1. **What exactly is being equated?** When people say "Compton frequency resonates with Unruh radiation," what physical quantities are being set equal? Is it:
   - E_C = E_U (energies)?
   - λ_C = λ_U (wavelengths)?
   - f_C = f_U (frequencies)?
   - Some other matching condition?

2. **At what acceleration does each matching occur?** For a proton, solve for the acceleration a* where each matching condition holds. Is a* close to cH₀?

3. **Does the mass drop out?** If we set E_C = E_U, we get mc² = ℏa/(2πc), so a* = 2πmc³/ℏ. Is this mass-dependent or mass-independent? For a proton, what is a*? Is it anywhere near 10⁻¹⁰ m/s²?

4. **Where does the cosmological scale enter?** The observed critical acceleration a₀ ~ cH₀ is a cosmological quantity. In the Compton-Unruh matching, where does H₀ or the Hubble radius enter? If the matching is purely local (Compton vs. Unruh), why should it care about cosmology?

5. **The role of the de Sitter horizon.** In de Sitter spacetime, the Unruh effect is modified. A uniformly accelerating detector in de Sitter sees a temperature that depends on BOTH the acceleration and the Hubble parameter. The exact formula is T = (ℏ/(2πk_B c))√(a² + (cH₀)²) (or similar — derive/verify this). How does this modify the resonance condition?

### Part 3: The Unruh-DeWitt detector response integral

Write down (from the standard QFT-in-curved-spacetime literature) the response function of an Unruh-DeWitt detector:

1. The detector is a two-level system coupled to a massive scalar field φ with mass m (so the field has Compton frequency f_C = mc²/h).
2. The detector moves on a uniformly accelerating worldline in de Sitter spacetime.
3. The transition rate of the detector is given by the Fourier transform of the Wightman function along the detector's worldline.
4. **Write down this integral explicitly.** Identify the Wightman function G⁺(x(τ), x(τ')) for a massive scalar field in de Sitter spacetime. Identify the detector gap energy E. The transition rate is R(E) = ∫ dΔτ e^{-iEΔτ} G⁺(Δτ).
5. **Identify what "resonance" would mean** in terms of this integral. Would it be a pole? A peak in R(E) as a function of a at fixed E = mc²? A divergence?

### Part 4: Numerical exploration

Using Python, make plots:
1. Plot T_U(a) and T_GH on the same axes, over a range a = 10⁻¹⁵ to 10⁰ m/s². Mark where they intersect or become comparable.
2. Plot the Unruh energy E_U(a) and the Compton energy E_C(proton) on the same axes. Where do they match?
3. If you can write down the de Sitter modified temperature T_dS(a, H₀), plot it and compare to the flat-space Unruh temperature.

## Success Criteria

- All scales in Part 1 are computed numerically
- The dimensional analysis in Part 2 is answered with explicit equations and numbers
- The key integral in Part 3 is written down explicitly (even if it can't be evaluated yet)
- At least 2 of the 3 plots in Part 4 are produced
- A clear verdict: "The Compton-Unruh resonance at a ~ cH₀ is dimensionally [consistent/inconsistent] because [specific reason]"

## Failure Criteria

- If the resonance turns out to be dimensionally impossible (e.g., the matching acceleration is mass-dependent and for a proton gives a* ~ 10⁴³ m/s² rather than 10⁻¹⁰), that is a valid and valuable result. Report it clearly with the specific numbers.
- If the Compton frequency plays no special role in the Unruh-DeWitt response (i.e., the field mass enters smoothly without any resonance structure), explain why.

## Deliverables

Write your findings to:
- `explorations/exploration-001/REPORT.md` — full detailed report with all derivations, code, and results (target 300-500 lines)
- `explorations/exploration-001/REPORT-SUMMARY.md` — concise summary (30-50 lines)
- Save any Python scripts to `explorations/exploration-001/code/`

## Important Notes

- **Derive, don't quote.** Show the algebra. If you cite a formula, derive it from first principles or explain where it comes from.
- **Distinguish standard results from novel claims.** Mark clearly which expressions are from established literature vs. your own derivation.
- **If something doesn't work out, say so.** A clear negative result is more valuable than a vague positive one.
