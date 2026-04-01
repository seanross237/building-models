# D2 — Adversarial Elimination Results

**Prompt used:** "For each answer option, ASSUME it is correct. Then search the problem statement for ANY evidence that CONTRADICTS that assumption — even subtle contradictions count. A single contradiction eliminates an option. List contradictions for every option. The correct answer is the option with ZERO contradictions."

**Guidance:** "Default to EXCLUSION. Ground claims in evidence. Consider the OPPOSITE."

---

## Q6: Largest hyperfine field in 57Fe Mossbauer spectroscopy

**Contradictions per option:**

| Option | Description | Contradictions |
|--------|-------------|----------------|
| A | Square pyramidal S=0 Fe(II) | S=0 → zero unpaired electrons → zero Fermi contact and zero orbital contribution → cannot produce largest field. ELIMINATED. |
| B | Planar S=5/2 Fe(III) | d5 high-spin has half-filled shell (L=0) → orbital angular momentum fully quenched → only Fermi contact contributes (~55T for ionic Fe3+), but no orbital enhancement to push higher. ELIMINATED. |
| **C** | **Linear S=2 Fe(II)** | **No contradiction.** d6 with S=2 gives 4 unpaired electrons (large Fermi contact). Linear geometry is the lowest coordination number → minimal crystal field quenching → large unquenched first-order orbital angular momentum. Both Fermi contact AND orbital terms are maximized simultaneously. |
| D | Tetrahedral S=2 Fe(II) | Same d6 S=2 as C, but tetrahedral (Td) symmetry provides more orbital quenching than linear geometry → smaller orbital contribution. Linear beats tetrahedral. ELIMINATED. |
| E | Trigonal bipyramidal S=2 Fe(IV) | d4, Fe(IV) has more contracted d-orbitals → smaller Fermi contact per unpaired electron. TBP (5-coordinate) provides more crystal field quenching than linear (2-coordinate). ELIMINATED. |

**Answer: C — Linear S=2 Fe(II)**

**Reasoning:** Hyperfine field = Fermi contact + orbital + dipolar terms. Linear geometry uniquely maximizes the orbital contribution (unquenched L) while S=2 Fe(II) provides 4 unpaired electrons for large Fermi contact. No other combination maximizes both terms simultaneously.

---

## Q9: Broadband CARS microscopy with a broadband pump beam

**Contradictions per option:**

| Option | Description | Contradictions |
|--------|-------------|----------------|
| A | Only generate Stokes | CARS is by definition anti-Stokes Raman — the four-wave mixing process generates signal at omega_aS = 2*omega_pump - omega_Stokes. Changing pump bandwidth doesn't convert the process to Stokes-only. ELIMINATED. |
| **B** | **Anti-Stokes but no separate vibrational info** | **No contradiction.** With broadband pump (serving as both pump and probe), the anti-Stokes signal at each output frequency is a convolution over all pump frequency pairs. The vibrational spectrum is convolved with the broad pump spectral profile, smearing out individual vibrational mode information. Anti-Stokes signal IS generated (four-wave mixing still occurs) but vibrational modes are not spectrally distinguishable. |
| C | Anti-Stokes with distinguishable info | Broadband pump means many pump frequency combinations contribute to each output frequency. The vibrational response is convolved with the pump autocorrelation, destroying spectral resolution of individual modes. ELIMINATED. |
| D | None of above | B is self-consistent with no contradictions, so "none of above" is itself contradicted. ELIMINATED. |
| E | Cannot generate anti-Stokes | Four-wave mixing (chi-3 process) occurs regardless of pump bandwidth. Broadband light can still drive CARS. ELIMINATED. |

**Answer: B — Anti-Stokes signal generated but without separately distinguishable vibrational information**

**Reasoning:** Broadband pump acts as both pump and probe. The CARS signal at each spectral point integrates over all frequency-pair combinations, convolving the vibrational response with the pump spectral profile. Signal exists but vibrational specificity is destroyed.

---

## Q10: Effect UNLIKELY from coarsening gas (chloride impurity) in ceramic sintering

**Contradictions per option (remember: we want the option where "this IS caused by coarsening gas" is CONTRADICTED):**

| Option | Description | Is this a known effect of coarsening gas? | Contradiction with "UNLIKELY" claim |
|--------|-------------|-------------------------------------------|--------------------------------------|
| A | Higher heating rates → lower densities | YES — fast heating closes pore channels before gas escapes, trapping gas | If A is the "unlikely" answer, that contradicts literature. ELIMINATED as answer. |
| B | De-densification under some atmospheres | YES — trapped insoluble gas causes pore growth/bloating at high T | If B is the "unlikely" answer, that contradicts literature. ELIMINATED as answer. |
| C | Large, randomly distributed voids | YES — trapped gas causes large pores distributed through the body | If C is the "unlikely" answer, that contradicts literature. ELIMINATED as answer. |
| **D** | **Larger grain sizes in interior than surface** | **NOT a standard effect of coarsening gas.** While coarsening gas enhances vapor transport, the grain size gradient is primarily controlled by thermal gradients and sintering kinetics, not gas trapping. The trapped gas in the interior primarily inhibits DENSIFICATION (pore removal) rather than enhancing grain GROWTH in the interior relative to the surface. Surface grains can coarsen via multiple mechanisms (surface diffusion, atmosphere exposure). | **No contradiction with "unlikely" — this is the answer.** |
| E | Cracking | YES — trapped gas pressure buildup causes cracking | If E is the "unlikely" answer, that contradicts literature. ELIMINATED as answer. |
| F | Higher green densities → lower sintered densities | YES — the classic green-density paradox: higher green density closes pores earlier, trapping more gas | If F is the "unlikely" answer, that contradicts literature. ELIMINATED as answer. |

**Answer: D — Larger grain sizes in interior than surface**

**Reasoning:** All other effects (A, B, C, E, F) are well-documented consequences of coarsening gas in ceramic sintering literature. The "interior-larger-than-surface" grain size gradient is not a characteristic signature of coarsening gas — coarsening gas primarily affects DENSIFICATION (pore behavior) rather than creating systematic grain size gradients. Grain size gradients are more typically attributed to thermal gradients and atmosphere exposure differences.

---

## Q11: Comprehensive list of organic A-site cations forming 3D lead halide perovskites (A-Pb-Br3)

**Contradictions per option:**

| Option | Description | Contradictions |
|--------|-------------|----------------|
| A | Cs, MA, FA only | Incomplete — aziridinium has been experimentally confirmed to form 3D APbBr3 perovskite (reported ~2020). List is missing a known 3D perovskite-forming cation. ELIMINATED. |
| **B** | **Cs, MA, FA, Aziridinium** | **No contradiction.** Aziridinium (Az, protonated aziridine, cyclic C2H5NH+) has a compact 3-membered ring structure giving effective ionic radius ~250 pm, fitting within the Goldschmidt tolerance factor window (0.8-1.0) for 3D perovskite. AzPbBr3 confirmed as 3D perovskite structure. The list Cs/MA/FA/Az accounts for all known A-site cations forming 3D lead bromide perovskites. |
| C | Cs, MA, FA, Ethylammonium | Ethylammonium (EA, CH3CH2NH3+) has effective radius ~274 pm — too large for 3D perovskite cavity. Tolerance factor > 1.0 for PbBr3. EAPbBr3 forms 1D/2D structure, not 3D. ELIMINATED. |
| D | Cs, MA, FA, Methylhydrazinium | Methylhydrazinium (MHy) does form 3D PbBr3 perovskite (Mączka et al., 2020), BUT if D is the comprehensive list, it excludes aziridinium which also forms 3D PbBr3. POTENTIALLY CONTRADICTED if Az also confirmed. However, if MHy forms 3D but Az does not specifically with PbBr3, D could be valid. Borderline — MHy confirmed but completeness uncertain. |
| E | Cs, MA, FA, Dimethylammonium | Dimethylammonium (DMA, (CH3)2NH2+) is too large — forms hexagonal or 1D perovskite structures with PbBr3, not standard 3D corner-sharing octahedral perovskite. ELIMINATED. |

**Answer: B — Cs, MA, FA, Aziridinium**

**Reasoning:** Aziridinium's compact cyclic structure gives it a uniquely small effective radius among organic cations, allowing it to fit in the cuboctahedral A-site cavity. This was a notable discovery precisely because ring compounds were not previously expected to form 3D perovskites. EA and DMA are too large (tolerance factor violations). The comprehensive list of cations forming true 3D corner-sharing PbBr3 perovskites is Cs, MA, FA, and aziridinium.

---

## Summary Table

| Q | Contradictions found per option | Answer |
|---|--------------------------------|--------|
| Q6 | A: S=0 gives zero field; B: L=0 quenches orbital term; C: **none**; D: Td quenches more than linear; E: Fe(IV) contracted orbitals + TBP quenching | **C** (Linear S=2 Fe(II)) |
| Q9 | A: CARS is inherently anti-Stokes; B: **none**; C: convolution destroys distinguishability; D: B is valid so "none" fails; E: chi-3 process still occurs | **B** (Anti-Stokes, no vibrational info) |
| Q10 | A: documented effect; B: documented effect; C: documented effect; D: **none** (not a coarsening-gas effect); E: documented effect; F: documented effect | **D** (Interior > surface grain size) |
| Q11 | A: incomplete (misses Az); B: **none**; C: EA too large; D: may miss Az; E: DMA too large | **B** (Cs, MA, FA, Aziridinium) |
