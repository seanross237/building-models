# Q11 — Organic A-Site Cations in 3D Lead Halide Perovskites Plan Review

## VERDICT: CORRECTED

## ISSUES:
1. **Cs is inorganic — the question says "organic" but every answer option includes Cs.** The plan flags this as a concern but does not resolve it. Resolution: This is a flaw in the question itself (or a deliberate trap). Since ALL five answer choices include Cs, the Cs issue is non-discriminating. Every option treats Cs as part of the baseline set. The plan should note this explicitly and move on — it cannot change the answer.
2. **Methylhydrazinium (MHy) DOES form 3D perovskites — the plan's dismissal is too casual.** MHyPbBr3 and MHyPbCl3 were reported with 3D perovskite structures (Maczka et al., 2019-2020, multiple publications in Chemistry of Materials and J. Phys. Chem. Lett.). The ionic radius of MHy+ (~264 pm) gives a borderline tolerance factor, but the experimentally determined crystal structures are genuinely 3D (corner-sharing PbX6 octahedra). This is the critical vulnerability in the plan: Option D (MHy) is a real competitor to Option B (Az).
3. **The plan relies heavily on a single reference (Becker et al. 2018) for aziridinium.** Becker et al. reported the synthesis of AzPbBr3 with a 3D perovskite structure and t ~ 0.98. This is a legitimate, peer-reviewed result. However, leaning on one paper is fragile.
4. **The tolerance factor dismissals need more care.** The plan states EA is "too large (1D)" and DMA is "too large (1D)" — these are correct for the dominant polymorphs. Ethylammonium (EA+, ~274 pm) forms 1D structures. Dimethylammonium (DMA+, ~272 pm) predominantly forms 1D chain perovskites with lead halides. These dismissals hold up.

### Detailed Review

**Step 1 — Focus on the 4th cation: CORRECT strategy**
Cs, MA, and FA are in every option. The discriminating question is which 4th cation forms a genuine 3D ABX3 perovskite with lead halides.

**Step 2 — Tolerance factor analysis: MOSTLY CORRECT but incomplete on MHy**

| Cation | Effective radius (pm) | t (with Pb²+, Br⁻) | Known structure | 3D? |
|--------|----------------------|---------------------|-----------------|-----|
| MA+ | ~217 | ~0.91 | 3D | Yes |
| FA+ | ~253 | ~1.00 | 3D | Yes |
| Az (Aziridinium) | ~250 | ~0.98 | 3D (Becker 2018) | Yes |
| MHy+ | ~264 | ~1.03 | 3D (Maczka 2019-2020) | Yes, but distorted |
| EA+ | ~274 | ~1.06 | 1D | No |
| DMA+ | ~272 | ~1.05 | 1D/hexagonal | No |

The plan correctly eliminates EA (C) and DMA (E). The real contest is between Az (B) and MHy (D).

**Step 3 — Adjudicating Az vs. MHy: Plan's conclusion is LIKELY CORRECT but reasoning needs strengthening**

The critical distinction:
- **Aziridinium (Az+):** The three-membered ring structure gives it a compact, nearly spherical shape despite having a molecular weight similar to larger cations. AzPbBr3 forms an undistorted cubic 3D perovskite (Becker et al. 2018, Kieslich et al. classification). Az is widely cited as the "fourth" organic A-site cation for 3D lead halide perovskites.
- **Methylhydrazinium (MHy+):** MHyPbBr3 and MHyPbCl3 are reported as 3D structures, BUT they adopt highly polar, distorted variants (orthorhombic/monoclinic) and the Pb-X framework shows significant octahedral tilting. Some authors classify these as "3D but non-perovskite" or "perovskite-related" rather than true ABX3 perovskite topology. The MHyPbI3 phase does NOT form a 3D perovskite — it adopts a 2D layered structure, showing that MHy is on the edge of the tolerance window and fails for the iodide.

This distinction matters: the question asks about "3D lead halide perovskites" generically. Az forms 3D perovskites across multiple halides; MHy only does so for some halides and with significant distortion that places its classification in dispute.

**Step 4 — Literature consensus**
The "four A-site cations" framing (Cs, MA, FA, Az) appears in multiple review articles post-2018. MHy is discussed as an interesting borderline case but is NOT included in the canonical set in most reviews. The plan's conclusion selecting B (Az) aligns with the dominant literature consensus.

### The Cs Paradox — Resolved

The question asks for "organic A-site cations" but includes Cs (an inorganic ion) in every option. Two interpretations:
1. The question is poorly worded and means "A-site cations" generally.
2. The question is testing whether you know which cations (including the inorganic Cs) form 3D perovskites, with "organic" being imprecise.

Either way, since Cs appears in all options, it is non-discriminating. The plan should acknowledge the imprecision but not let it derail the analysis. The answer hinges entirely on the 4th cation.

## FINAL_PLAN

(1) All options share Cs/MA/FA — discriminate on the 4th cation. (2) Eliminate EA (Option C): effective radius ~274 pm, t > 1.05, forms only 1D structures with lead halides. Eliminate DMA (Option E): effective radius ~272 pm, t > 1.05, forms 1D/hexagonal phases, not 3D corner-sharing perovskite. (3) Adjudicate Az vs. MHy: Both have reported 3D structures, but MHy is borderline — MHyPbI3 fails to form 3D, MHyPbBr3/Cl3 are highly distorted and classification as "perovskite" is contested. Aziridinium forms undistorted 3D perovskite (AzPbBr3, t ~ 0.98, Becker et al. 2018) and is included in the canonical set in review literature. (4) Note the Cs paradox (inorganic, but non-discriminating since all options include it). (5) Answer: **B. Cs, MA, FA, Aziridinium**.

**Key correction from original plan:** The original plan was too dismissive of MHy, calling it merely "borderline" without engaging with the published 3D structures. The corrected plan acknowledges MHy's 3D structures but explains why Az is the stronger answer: Az forms undistorted 3D perovskites across halides and is part of the consensus canonical set, while MHy is a contested edge case that fails for iodides.
