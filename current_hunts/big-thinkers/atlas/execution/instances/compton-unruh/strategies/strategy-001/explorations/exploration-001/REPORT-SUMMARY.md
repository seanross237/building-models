# Exploration 001 — Summary

## Goal
Compute all physical scales for the Compton-Unruh resonance hypothesis, perform dimensional analysis, write down the Unruh-DeWitt detector response integral, and determine if a resonance at a ~ cH_0 is dimensionally consistent.

## What Was Done
- Computed 12+ physical quantities (Compton scales, Unruh scales, Gibbons-Hawking temperature, MOND acceleration, cH_0) numerically in Python
- Derived the matching acceleration a* = 2*pi*mc^3/hbar for all three matching conditions (energy, frequency, wavelength)
- Analyzed the de Sitter modified Unruh temperature T_dS = (hbar/2*pi*c*k_B)*sqrt(a^2 + c^2*H^2)
- Wrote down the Unruh-DeWitt detector transition rate integral and evaluated it for massless and massive fields
- Produced 5 plots illustrating temperature scales, energy matching, de Sitter modification, and detector response

## Outcome: DECISIVE NEGATIVE RESULT

**The Compton-Unruh resonance at a ~ cH_0 is dimensionally inconsistent by 43 orders of magnitude.**

The matching acceleration for a proton is a* = 2.69 x 10^33 m/s^2, while the target is cH_0 = 6.6 x 10^-10 m/s^2. The matching is mass-dependent (no universal a_0), the cosmological scale H_0 doesn't appear in the matching, and the Boltzmann suppression at a ~ cH_0 is exp(-10^42) — effectively zero. The Unruh-DeWitt detector response has no resonance structure; the Compton frequency enters only as a mass threshold.

## Verification Scorecard
- **VERIFIED**: 0 (no Lean proofs — not applicable)
- **COMPUTED**: 11 (all scales, matching accelerations, suppressions, 5 plots)
- **CHECKED**: 2 (standard QFT formulas cross-checked against literature)
- **CONJECTURED**: 4 (massive field details, resonance characterization)

## Key Takeaway
The "Compton-Unruh resonance" cannot work as literally described. The Compton and Unruh energy scales differ by 42 orders of magnitude at a ~ cH_0. However, there IS an interesting crossover at a ~ cH_0 where de Sitter horizon effects begin dominating over acceleration effects — this crossover does not involve the Compton frequency but may deserve separate investigation as a distinct mechanism.

## Leads Worth Pursuing
1. The de Sitter thermal crossover at a ~ cH_0 as a potential mechanism (without Compton frequency)
2. McCulloch's IR cutoff approach — does truncating Unruh modes at the Hubble scale produce any non-trivial modification? This is not a "resonance" but could still affect the Wightman function
3. Whether the proton mass enters through a completely different channel than direct Compton-Unruh matching

## Proof Gaps Identified
- The massive-field Wightman function in de Sitter along an accelerating worldline is stated but not derived or computed — this is the key integral that would need evaluation for a rigorous treatment
- The claim that the massive density of states has no resonance structure (only a threshold) needs verification for non-trivially curved backgrounds

## Unexpected Findings
- The Unruh wavelength at a = a_0 is ~200x the Hubble radius (lambda_U(a_0)/R_H ~ 217). This means the "Unruh radiation" at MOND-scale accelerations has wavelengths far exceeding the observable universe — raising questions about whether such modes are physical at all.
