# Exploration 003 — Survey of Unruh-Inertia Proposals and No-Go Theorem Search

## Mission Context

We are investigating whether Unruh-effect physics can explain the anomalous dynamics observed at low accelerations (a ~ cH₀ ≈ 7×10⁻¹⁰ m/s²) in galaxies, potentially explaining rotation curves without dark matter.

**CRITICAL PRIOR RESULT**: Exploration 001 has already shown that the direct "Compton-Unruh resonance" — where the Compton frequency of a proton matches the Unruh temperature — is ruled out by 43 orders of magnitude. The matching acceleration is a* = 2πmc³/ℏ ~ 10³³ m/s² for a proton, not 10⁻¹⁰ m/s². The cosmological scale H₀ does not appear in the direct matching. Boltzmann suppression is exp(-10⁴²).

However, there IS an interesting de Sitter crossover at a ~ cH₀ where the thermal environment transitions from acceleration-dominated (Unruh) to horizon-dominated (Gibbons-Hawking). The question is whether EXISTING proposals in the literature exploit this or a related mechanism.

## Your Task

This is a **literature survey and critical analysis** task. You are investigating the Compton-Unruh resonance / modified inertia topic. Your working directory is the compton-unruh mission. Write ALL output files to the explorations/exploration-003/ directory.

### Part 1: Survey of existing Unruh-inertia proposals

Search for and summarize the major proposals connecting the Unruh effect to inertia or low-acceleration dynamics:

1. **McCulloch's Quantized Inertia (QI / MiHsC)**
   - Core mechanism: modified inertia from Hubble-scale Casimir effect on Unruh radiation
   - Key equations — write them down explicitly
   - Predictions for galaxy rotation curves
   - Reception and published critiques
   - Key papers: McCulloch (2007, 2013, 2017)

2. **Haisch-Rueda-Puthoff stochastic electrodynamics (SED) inertia**
   - Proposed that inertia arises from interaction with quantum vacuum (ZPF)
   - Current status — was it refuted?
   - Key papers: Haisch, Rueda & Puthoff (1994), Haisch & Rueda (2001)

3. **Milgrom's MOND** (for comparison)
   - The interpolation function μ(a/a₀)
   - Which observations support it, which challenge it
   - The external field effect

4. **Verlinde's emergent gravity** (for comparison)
   - Key result: derives a₀ = cH₀/6 from entropy displacement in de Sitter
   - Relation to Unruh-based proposals

5. **Any other proposals** connecting Unruh radiation to dark matter phenomenology

### Part 2: No-go theorems and fundamental objections

Evaluate the strongest arguments against Unruh-based inertia modification:

1. **Temperature argument**: T_U at a ~ 10⁻¹⁰ m/s² is ~10⁻³⁰ K, drowned by CMB at 2.7 K
2. **Bound system problem**: Unruh effect applies to uniform acceleration in vacuum, not orbiting stars
3. **Detector coupling**: How would real particles "detect" Unruh radiation?
4. **Backreaction**: Is Unruh radiation energy density sufficient to modify dynamics?
5. **Equivalence principle**: Does modified inertia violate the equivalence principle?
6. **Solar system constraints**: Bounds from Earth-Moon laser ranging, planetary ephemerides
7. **Published critiques**: Strongest peer-reviewed objections

### Part 3: Assessment

1. Is there a **fatal no-go** ruling out ALL Unruh-based inertia modification?
2. What are the **strongest surviving objections** any new proposal must address?
3. Is there a meaningful mechanism that operates at a ~ cH₀ that doesn't suffer from the 43-order-of-magnitude problem?
4. How do McCulloch's QI, Verlinde, and the de Sitter crossover relate to each other?

## Success Criteria
- At least 3 proposals summarized with key equations
- At least 5 no-go arguments evaluated with specific references
- Clear assessment of whether a fatal no-go exists
- Relationship between proposals clarified

## Deliverables
Write to:
- `explorations/exploration-003/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-003/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
