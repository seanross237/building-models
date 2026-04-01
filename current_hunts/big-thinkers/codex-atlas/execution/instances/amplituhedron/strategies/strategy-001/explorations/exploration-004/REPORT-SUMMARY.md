# Exploration 004 Summary: Emergent Locality and Unitarity

## Goal
Map precisely how locality and unitarity emerge from the amplituhedron geometry, and assess whether this emergence has physical consequences beyond reformulation.

## What Was Done
Systematic literature survey: the two original Arkani-Hamed & Trnka papers (1312.2007, 1312.7878), the "Anatomy" paper (1408.3410), "Positive Amplitudes" (1412.8478), the binary-code paper (1704.05069), the "Emergent Unitarity" proof (1906.10700), the EFT-hedron (2012.15849), the momentum amplituhedron (1905.04216), the Landau singularities paper (1612.02708), the 2025 Inventiones proof (2112.02703), the hidden-zeros paper (2312.16282), and a March 2025 preprint (2503.03805). Also: PhysicsOverflow expert discussion, Quanta Magazine 2024 article on surfaceology.

## Outcome: SUCCESS

Clear characterization of both mechanisms, with concrete 4-point example. Honest assessment of new physics vs. reformulation with specific evidence.

## Key Takeaway

**The mechanism is precise**: Locality = canonical form has logarithmic poles only on boundaries of the amplituhedron, enforced by positivity conditions that screen out non-physical ("illegal") singularities via a codimension-1 surface in momentum-twistor space. Unitarity = these boundaries factorize as products of left/right amplituhedra (proved for all n, L, k, JHEP 2020). Spurious-pole cancellation was formally proved via BCFW triangulation of the amplituhedron (Inventiones 2025 — 12 years after the conjecture).

**Brutal assessment**: For N=4 SYM itself, this is reformulation. All predictions are identical to Feynman diagrams. Multiple experts confirm no observable prediction distinguishes the approaches.

**But the program yields three genuine physical contributions**:
1. **EFT-hedron** (2021): Real-world positivity bounds on Wilson coefficients for QED, graviton EFTs — specific inequalities, mass bounds on new physics. This is the most concrete real-world consequence.
2. **Hidden zeros** (2024): Phi³, pions, and gluon amplitudes share a common structure and identical hidden zeros — a genuine new result not visible from Lagrangian methods, with geometric origin in the ABHY associahedron.
3. **March 2025 paper** (arXiv:2503.03805): Locality and unitarity at 1-loop emerge from hidden zeros in non-supersymmetric Tr(φ³) theory — strongest evidence to date that the emergence program extends beyond N=4 SYM.

UV finiteness as a selection principle (positive geometry selects UV-finite theories) is a fourth physical insight, though not a prediction.

## Leads Worth Pursuing

1. **arXiv:2503.03805** (March 2025): "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop" — applies to non-SUSY theories. Worth reading in full; could be the beginning of generalizing the emergent-locality program beyond N=4 SYM.

2. **EFT-hedron bounds for gravity** (arXiv:2012.15849, Section on graviton scattering): Specific constraints on graviton-graviton scattering coefficients. Worth checking whether these constraints are testable or have been tested.

3. **ABJM emergent unitarity at all loops** (arXiv:2303.03035): Proves odd-point vanishing from "bipartite" geometry — this is a non-trivial prediction (odd-point ABJM amplitudes must vanish) derived purely from the geometric structure.

## Unexpected Findings

1. **March 2025 preprint extends emergence to non-SUSY 1-loop** (arXiv:2503.03805): The claim "locality and unitarity emerge from geometry" now applies beyond N=4 SYM at 1-loop. This was outside the scope of my search but directly relevant — the program is more general than the amplituhedron itself.

2. **The 2025 Inventiones proof** (Even-Zohar, Lakrec, Tessler): A full 130-page mathematics proof that the BCFW triangulation conjecture is true. This took 12 years from the original paper. The difficulty of the proof reveals that the "obvious from topology" argument about spurious poles requires serious work — suggesting the geometric picture, while conceptually clean, has non-trivial mathematical content.

3. **Relaxing positivity → non-local singularities**: The "deformed amplituhedron" (1408.3410 Section 10) explicitly shows what happens if you violate positivity: you get poles at non-physical locations. This is the amplituhedron's direct answer to "what if locality were violated" — you'd need to leave the positive region. This is concrete.

## Computations Identified

None required — this was a literature survey. No missing calculations block progress on the core question.

However: the EFT-hedron bounds (arXiv:2012.15849) contain specific quantitative constraints on photon-graviton EFT coefficients that could be computed/reproduced from the geometric formula. A 50-100 line Python script implementing the EFT-hedron positivity matrix and verifying the bounds for specific Wilson coefficients would make the "physical consequences" claim concrete and verifiable. Input: the EFT-hedron paper's explicit positivity matrices. Output: specific allowed regions in EFT coefficient space.
