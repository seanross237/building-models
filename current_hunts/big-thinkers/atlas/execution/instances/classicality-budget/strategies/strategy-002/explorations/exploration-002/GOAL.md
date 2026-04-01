# Exploration 002: BH Universal Constants — Systematic Literature Verification

## Mission Context

We are studying the "classicality budget" — an upper bound on quantum Darwinism redundancy. Strategy-001 derived three "universal constants" that describe Hawking radiation near any black hole horizon:

1. **S_Hawking(r_s sphere) = 1/(540 ln2) ≈ 0.002672 bits** — the Hawking radiation entropy inside the Schwarzschild radius sphere, for ANY black hole mass
2. **⟨N_photons⟩(r_s sphere) = ζ(3)/(24π⁴) ≈ 5.14 × 10⁻⁴** — mean photon count in the same sphere
3. **Classicality horizon: R_1bit = (540 ln2)^{1/3} × r_s ≈ 7.21 r_s** — the radius where accumulated Hawking radiation first provides 1 bit of entropy

These follow trivially (5-line calculation) from the universal identity **T_H × r_s = ℏc/(4πk_B) = constant** (M cancels). The derivation:
- T_H = ℏc³/(8πGMk_B), r_s = 2GM/c²
- Therefore T_H × r_s = ℏc/(4πk_B) [M cancels]
- λ_Hawking = ħc/(k_BT_H) = 4π r_s ≈ 12.57 r_s [always]
- S_Hawking = (16σ/3c) × T_H³ × (4π/3) r_s³ = const × (T_H × r_s)³ × (geometric factor) = 1/(540 ln2)

The 540 = 9 × 60 where: 60 comes from Stefan-Boltzmann constant (σ = π²k_B⁴/(60ħ³c²)), and 9 from the geometric factor (4π/3) × (4π)³ / (units combining).

**Your job:** Determine definitively whether these three constants, or equivalent results, have been published in the black hole thermodynamics literature.

## What You Must Check

### Specific Papers to Examine

**Black hole radiation and photon emission:**
1. **Page, D. N. (1976)** "Particle emission rates from a black hole: Massless particles from an uncharged, nonrotating hole" Phys. Rev. D 13, 198 — Search for any computation of photon number density or entropy in the near-horizon region
2. **Page, D. N. (1977)** "Particle emission rates from a black hole. II. Massless particles from a rotating hole" Phys. Rev. D 14, 3260 — same
3. **Wald, R. M.** "Quantum Field Theory in Curved Spacetime and Black Hole Thermodynamics" (1994 book) — Check Chapter 7-9 for near-horizon photon density calculations
4. **Hawking, S. W. (1975)** "Particle creation by black holes" — original paper — check if any near-horizon photon count appears
5. **Parker, L. (1975)** and other early papers on Hawking radiation particle production

**Sparsity of Hawking radiation:**
6. **Gray, F., Visser, M. et al. (2016)** "The Hawking cascade from a black hole is extremely sparse" — check for any entropy-per-horizon-radius computation
7. **Hod, S. (2015)** "Gravitation and Cosmology" on Hawking radiation sparsity — same
8. **Visser, M.** any papers on Hawking radiation greybody factors or sparseness — check for near-horizon entropy numbers
9. **Kim, S. W., Kim, W. T. et al.** — any papers computing photon density near the horizon

**Black hole photon gas / thermodynamics:**
10. **Mukhanov, V. and Winitzki, S.** "Introduction to Quantum Effects in Gravity" (2007) — check for near-horizon photon count
11. **Birrell, N. D. and Davies, P. C. W.** "Quantum Fields in Curved Space" (1982) — check for any near-horizon entropy density computation
12. **Frolov, V. and Novikov, I.** "Black Hole Physics" (1998) — check for photon number calculations
13. **Preskill, J.** "Do Black Holes Destroy Information?" (1992) — check for any photon number estimates
14. **Unruh, W. G. (1976)** "Notes on black hole evaporation" — check for any photon number density near horizon

**Universal constants and T_H × r_s:**
15. **Search specifically for the identity T_H × r_s = ℏc/(4πk_B)** — has this been stated as a named result anywhere? Any review paper on BH thermodynamics that discusses this?
16. **Search for "Hawking photon wavelength 4π Schwarzschild"** or "λ = 4π r_s" — has the universal scaling λ_Hawking = 4π r_s been named?

**BH classicality and quantum information:**
17. **Bekenstein, J. D.** papers on information in black holes — any photon count near the horizon?
18. **Susskind, L. and Lindesay, J.** "An Introduction to Black Holes, Information and the String Theory Revolution" (2005) — check for near-horizon photon thermodynamics

## Required Search Queries

Run web searches (Google Scholar, arXiv, Semantic Scholar) for ALL of these:
- "Hawking radiation entropy per Schwarzschild radius"
- "Hawking photon entropy near horizon"
- "1/(540 ln 2) black hole"
- "zeta(3) Hawking radiation photon count"
- "universal Hawking radiation constant"
- "Hawking radiation sparsity entropy density"
- "T_H r_s constant black hole"
- "Hawking temperature Schwarzschild radius product"
- "photon number Hawking radiation near horizon volume"
- "classicality horizon black hole"
- "7.21 Schwarzschild radius"

## What You're Looking For

**For each constant, answer:**
1. Does S = 1/(540 ln2) bits appear EXPLICITLY anywhere, under any name?
2. Does ⟨N⟩ = ζ(3)/(24π⁴) appear EXPLICITLY anywhere?
3. Does the identity T_H × r_s = const appear as a NAMED result?
4. Does λ_Hawking = 4π r_s appear as a named result?
5. Does R_1bit = 7.21 r_s appear in any discussion of classical limits near BH horizons?

**Be precise:** "Not found" means you searched and didn't find it. "Likely not published" means it's too trivial to bother. "Found implicitly" means the ingredients are there but the result isn't stated.

**What does NOT count as "found":**
- Papers that discuss T_H or r_s separately but don't compute their product explicitly
- Papers about BH entropy (Bekenstein-Hawking entropy S_BH = 4GM²/ħ) — that's different from Hawking photon entropy in the near-horizon sphere
- Papers that discuss Hawking radiation sparsity qualitatively without computing S/V

## Deliverables

For each constant: a verdict of PUBLISHED / IMPLICITLY KNOWN / NOT PUBLISHED, with the specific citations and quotes that support the verdict.

For each paper checked: a one-line summary of what it computed and whether it touches the relevant constants.

A final summary verdict: do these three constants represent a novel computation or just an overlooked 5-line calculation from existing results?

## Output

Write your report to: `explorations/exploration-002/REPORT.md` (relative to the strategy directory)

Then write a concise summary (max 300 words) to: `explorations/exploration-002/REPORT-SUMMARY.md`

Write the report incrementally — complete each section and write it to the file before moving on to the next. Do NOT compose the entire report in memory and write it all at once.

Check at least 15 specific papers/sources, not just search queries. For each paper, note: title, what you checked, and what you found.

## Strategy Directory

`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/classicality-budget/strategies/strategy-002/`
