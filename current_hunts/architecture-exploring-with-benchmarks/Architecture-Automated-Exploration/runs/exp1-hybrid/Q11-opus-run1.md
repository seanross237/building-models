# Q11 — Perovskite A-Site Cations | Opus Run 1 (Hybrid M2+M4)

## PLAN

**Constraints extracted:**
1. Must be **organic** A-site cations (Cs⁺ is inorganic but included in all options as baseline)
2. Must **independently** form **3D** lead halide perovskites (APbX₃)
3. Goldschmidt tolerance factor t = (r_A + r_X) / [sqrt(2) * (r_B + r_X)] must be ~0.8-1.0
4. For Pb-halide perovskites, effective ionic radius of A constrained to roughly 1.7-2.6 Angstroms
5. All options include Cs, MA, FA — the differentiator is the proposed 4th cation

**Shortest path (3 steps):**
1. Confirm Cs/MA/FA are universal (all options agree) — focus on the 4th cation
2. Evaluate each candidate 4th cation against the size/tolerance-factor constraint for 3D perovskite formation
3. Match survivor to answer choice

## REASONING

### Step 1: Universal cations (no discrimination needed)
- Cesium (Cs⁺, r ~ 1.67 A): CsPbBr₃, CsPbI₃ — well-known 3D perovskites. Present in all options.
- Methylammonium (MA⁺, CH₃NH₃⁺, r ~ 2.17 A): MAPbI₃, MAPbBr₃ — canonical 3D perovskites. Present in all options.
- Formamidinium (FA⁺, CH(NH₂)₂⁺, r ~ 2.53 A): FAPbI₃, FAPbBr₃ — established 3D perovskites. Present in all options.

If answer is A (only these three), then no 4th cation qualifies. Otherwise, exactly one of B/C/D/E adds the correct 4th.

### Step 2: Evaluate each candidate 4th cation

**Ethylammonium (EA⁺, C₂H₅NH₃⁺, r ~ 2.74 A)** — Option C
- Too large for 3D perovskite cavity. Tolerance factor exceeds 1.0 for lead halides.
- EAPbI₃ forms 1D chain structure, not 3D.
- EXCLUDED.

**Dimethylammonium (DMA⁺, (CH₃)₂NH₂⁺, r ~ 2.72 A)** — Option E
- Too large. Forms hexagonal 1D structures with lead halides (e.g., DMAPbI₃ is 1D).
- EXCLUDED.

**Methylhydrazinium (MHy⁺, CH₃NHNH₃⁺, r ~ 2.64 A)** — Option D
- Mączka et al. reported MHyPbBr₃ and MHyPbCl₃ as 3D perovskite structures (polar, space group P2₁).
- These are genuine 3D corner-sharing PbX₆ octahedral networks.
- However, the effective radius is at the upper boundary, and these are unusual polar distorted variants.
- Does qualify as 3D, but less widely recognized.

**Aziridinium (Az⁺, (CH₂)₂NH₂⁺, r ~ 2.50 A)** — Option B
- Becker et al. (2018, Chem. Sci.) confirmed AzPbBr₃ as a genuine 3D perovskite.
- Tolerance factor ~ 0.98, well within the 3D perovskite window.
- The compact 3-membered ring keeps the effective radius small despite being a larger molecule.
- Widely cited as the "4th organic A-site cation" for 3D lead halide perovskites.

### Step 3: Discrimination between B and D

Both aziridinium and methylhydrazinium have literature reports of 3D perovskite formation. However:

- Aziridinium was specifically highlighted as a discovery — being only the 4th organic cation known to form 3D lead halide perovskites (after MA, FA, and the inorganic Cs).
- The question asks for organic cations that are "capable of independently forming" 3D structures — aziridinium's 3D perovskite formation is well-established and unambiguous.
- Methylhydrazinium 3D perovskites were reported later and expand the list further, but the "comprehensive list" framing with exactly 4 options (Cs + 3 organic) matches the canonical set: Cs, MA, FA, Az.

**Opposite-reading check:** Could answer A (only three) be correct? No — aziridinium's 3D perovskite formation is experimentally verified. Could C or E be correct? No — EA and DMA are too large for 3D. Could D be correct instead of B? Methylhydrazinium does form 3D structures, but aziridinium was the breakthrough recognized as completing the set of A-site cations for 3D perovskites.

**Surface-pattern check:** The question says "comprehensive list of ALL possible" — this might suggest including both Az and MHy. But no answer option includes both. Between B and D, aziridinium is the more established and widely recognized 4th member.

## ANSWER

**B. Cesium, Methylammonium, Formamidinium and Aziridinium**
