# Exploration 002 — Survey of Unruh-Inertia Proposals and No-Go Theorem Search

## Mission Context

We are investigating the hypothesis that a resonance between a particle's Compton frequency and the Unruh radiation modifies inertia at very low accelerations (a ~ cH₀ ≈ 7×10⁻¹⁰ m/s²), potentially explaining galaxy rotation curves without dark matter.

Before we invest in detailed calculations, we need to understand: (1) what proposals already exist connecting the Unruh effect to inertia modification, and (2) whether there are known no-go theorems or fundamental objections that would rule out such a mechanism.

## Your Task

This is a **literature survey and critical analysis task.**

### Part 1: Survey of existing Unruh-inertia proposals

Search for and summarize the major proposals that connect the Unruh effect to inertia or modified gravity:

1. **McCulloch's Quantized Inertia (QI / MiHsC)**
   - What is the core mechanism? (Modified inertia from a Hubble-scale Casimir effect on Unruh radiation)
   - What are the key equations? Write them down explicitly.
   - What predictions does it make for galaxy rotation curves?
   - What is the reception in the physics community? Published critiques?
   - Key papers: McCulloch (2007, 2013, 2017)

2. **Haisch-Rueda-Puthoff stochastic electrodynamics (SED) inertia**
   - Proposed that inertia arises from interaction with the quantum vacuum (ZPF)
   - What happened to this program? Was it refuted?
   - Key papers: Haisch, Rueda & Puthoff (1994), Haisch & Rueda (2001)

3. **Milgrom's MOND** (for comparison)
   - The phenomenological framework: a₀ ≈ 1.2×10⁻¹⁰ m/s²
   - The interpolation function μ(a/a₀): what forms have been proposed?
   - Current status: which observations support MOND, which challenge it?
   - The "external field effect" — does it have analogues in Unruh-based proposals?

4. **Verlinde's emergent gravity** (for comparison)
   - Key result: derives a₀ = cH₀/6 from entropy displacement in de Sitter space
   - How does this relate to Unruh-based inertia modification?
   - Current status after observational tests

5. **Any other proposals** connecting Unruh radiation to dark matter phenomenology
   - Jacobson-Parentani? Liberati? Others?

### Part 2: No-go theorems and fundamental objections

Search for and evaluate the strongest arguments against Unruh-based inertia modification:

1. **Temperature argument**: At a ~ 10⁻¹⁰ m/s², the Unruh temperature is T_U ~ 10⁻³⁰ K. This is absurdly small — many orders of magnitude below the CMB temperature (2.7 K) and even the cosmic neutrino background (~1.9 K). Can a thermal effect at 10⁻³⁰ K have any physical consequences in a universe bathed in 2.7 K radiation?

2. **Bound system problem**: The Unruh effect applies to uniformly accelerating observers in vacuum. Stars in galaxies are not uniformly accelerating — they orbit. Does the Unruh effect apply to circular orbits? To bound gravitational systems? What about the equivalence principle — does a freely falling star "see" Unruh radiation?

3. **Detector coupling**: The Unruh-DeWitt detector is a theoretical construct — a pointlike two-level system coupled to a quantum field. Real particles are not Unruh-DeWitt detectors. How would a proton or neutron "detect" Unruh radiation? What is the actual coupling mechanism?

4. **Backreaction**: Even if Unruh radiation exists, modifying inertia requires it to exert a significant force on the particle. What is the energy density of Unruh radiation at a ~ 10⁻¹⁰ m/s²? Is it sufficient to modify dynamics?

5. **Equivalence principle**: If inertia is modified by the Unruh effect, does this violate the equivalence principle? How?

6. **Observational constraints from solar system**: MOND-like modifications are tightly constrained by solar system dynamics (Earth-Moon laser ranging, planetary ephemerides, Pioneer anomaly). What are the bounds?

7. **Published critiques**: Search for published critiques of McCulloch's QI, Haisch-Rueda SED inertia, and Unruh-based dark matter explanations generally. What are the strongest objections?

### Part 3: Assessment

Based on Parts 1 and 2, provide a verdict:

1. Is there a **fatal no-go theorem** that rules out ALL Unruh-based inertia modification? If so, identify it precisely.
2. If not fatal, what are the **strongest objections** that any new Compton-Unruh proposal would need to address?
3. Is the Compton-Unruh resonance hypothesis (as described in the mission context) **genuinely distinct** from McCulloch's QI? If so, what is the key difference? If not, it's a reinvention and we should acknowledge that.
4. What is the **most promising** mechanism for connecting Unruh physics to low-acceleration dynamics?

## Success Criteria

- At least 3 existing proposals are summarized with their key equations
- At least 5 of the 7 no-go arguments are evaluated with specific references
- A clear assessment is provided: whether a fatal no-go exists, and what the strongest surviving objections are
- The relationship to McCulloch's QI is clarified

## Failure Criteria

- If a genuinely fatal no-go theorem is found, that is a valuable result. Document it rigorously with references.
- If the Compton-Unruh idea turns out to be identical to McCulloch's QI, document the equivalence.

## Deliverables

Write your findings to:
- `explorations/exploration-002/REPORT.md` — full detailed report (target 300-500 lines)
- `explorations/exploration-002/REPORT-SUMMARY.md` — concise summary (30-50 lines)

## Important Notes

- **Cite specifically.** For every claim, give author, year, and ideally arXiv ID or journal reference.
- **Distinguish criticism quality.** A published peer-reviewed critique is stronger than a blog post or arxiv comment. Rank the objections by how rigorous the argument is.
- **Be honest about the landscape.** If these proposals are widely regarded as fringe, say so — but also note if any have mainstream support or positive observational evidence.
