# Exploration 005 — Summary

## Goal
Literature survey: Has T_U/T_dS = μ_MOND been published? How does it compare to Verlinde 2016? Is the free-fall objection resolved?

## What Was Tried
- Searched for all papers connecting Unruh temperature, de Sitter temperature, and MOND interpolation function
- Fetched arXiv abstracts and secondary sources for: Milgrom 1999, Deser-Levin 1997, Pikhitsa 2010, Verlinde 2016, Smolin 2017, McCulloch 2007, Luo 2026
- Searched directly for "T_U/T_dS" ratio combined with MOND in indexed literature
- Investigated the free-fall objection via Sciama-Candelas 1981 and Jacobson 1995

## Outcome: MOSTLY SUCCEEDED

**Part 1 (novelty): The specific identity T_U/T_dS = μ_standard_MOND appears genuinely novel.** Direct search returned zero papers with this identity. The closest prior work is Milgrom 1999 (astro-ph/9805346), who used the EXCESS temperature T_dS − T_GH — a different formula giving a different interpolation function and a₀ = 2cH₀. Milgrom explicitly noted the argument doesn't obviously apply to circular orbits.

**Part 2 (Verlinde comparison): T_U/T_dS and Verlinde 2016 are genuinely distinct.** Verlinde uses elastic entropy displacement (modified gravity); T_U/T_dS uses a temperature ratio (modified inertia). Verlinde gets only the deep-MOND limit (not a full interpolation function), with a₀_eff = cH₀/6 ≈ 1.1 × 10⁻¹⁰ m/s² (8% from observed). The T_U/T_dS approach gives the exact standard MOND interpolation function μ = x/√(1+x²) but with a₀ = cH₀ (5.5× too large). Importantly: T_U/T_dS predicts the RAR exactly; Verlinde fails the RAR observationally.

**Part 3 (free-fall): The objection is unresolved for T_U/T_dS modified-inertia approach.** Sciama-Candelas 1981 confirms that freely-falling observers see cold vacuum, not T_GH. Milgrom himself (1999) explicitly flagged that his de Sitter temperature argument doesn't obviously apply to circular orbits — this concern has stood for 25 years. Verlinde bypasses it cleanly by using g_N = |∇Φ| instead of proper acceleration. A potential resolution exists (replace proper acceleration with de Sitter-relative acceleration = g_B for orbital stars) but has not been rigorously developed.

## Key Takeaway
The T_U/T_dS identity appears novel. The spirit of connecting de Sitter temperature crossover to MOND dates to Milgrom 1999, but the specific identity with the STANDARD MOND interpolation function (exact, not just asymptotic) has not been made. The approach gives better phenomenology than Verlinde (exact standard MOND, consistent with RAR) but worse a₀ (5.5× off vs. 8% off) and an unresolved free-fall problem. The free-fall objection is the dominant obstacle.

## Leads Worth Pursuing
1. **De Sitter-relative acceleration (Approach C):** Formally compute the proper acceleration of an orbital star relative to the de Sitter background (Hubble flow), not Minkowski. This may equal g_B, which would resolve the free-fall problem and connect T_U to g_N rigorously.
2. **Jacobson 1995 connection:** Investigate whether local Rindler horizon structure in galaxies gives T_U ~ T_U(g_B), not T_U(a_proper). This could be the missing link.
3. **Factor of 5.5:** The a₀ discrepancy between cH₀ and observed MOND scale is a factor of 5.5. Verlinde gets a factor of 1/6 from spatial volume of de Sitter space. Investigate whether the T_U/T_dS approach, reformulated in 3D, picks up a factor of 1/6 as well.

## Unexpected Findings
- Verlinde 2016 (despite its fame) actually FAILS the RAR and solar system tests badly. The T_U/T_dS approach, despite its fundamental problems, gives BETTER observational predictions than Verlinde in terms of the interpolation function shape.
- Milgrom himself (1999) was aware of and concerned about the free-fall objection for Unruh-based MOND — this has been an unresolved issue for 25 years.
- A new 2026 paper (Luo, arXiv:2602.14515) proposes yet another mechanism (spectral broadening) connecting de Sitter + MOND but also doesn't use T_U/T_dS.

## Computations Identified
- **De Sitter relative acceleration calculation:** Compute the covariant proper acceleration of a circular geodesic in Schwarzschild-de Sitter spacetime relative to the de Sitter Hubble observer. Is this equal to g_B = GM/r²? This is a ~50-line GR calculation using sympy/sage. If the answer is yes, the free-fall objection is resolved for orbital stars.
- **Jacobson local Rindler temperature in galaxy field:** For a freely-falling star in a Schwarzschild geometry, compute the temperature of local Rindler horizons associated with the local tidal field. If this equals T_U(g_B), it provides a QFT-grounded mechanism for T_U/T_dS inertia modification without invoking proper acceleration.
