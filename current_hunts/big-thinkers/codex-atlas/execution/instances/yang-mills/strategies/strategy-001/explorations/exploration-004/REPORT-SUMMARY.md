# Exploration 004 Summary: Lattice-to-Continuum Limit — Bridging Numerical Evidence and Rigorous Proof

## Goal
Map what lattice simulations have established numerically about Yang-Mills, what has been proved rigorously, the precise gap between them, and the most promising proof strategies for the Millennium Prize Problem.

## Outcome: SUCCEEDED

## What Was Done
Systematic research cataloging: (1) specific numerical lattice results (glueball masses, string tension, asymptotic scaling, universality, deconfinement), (2) all rigorous mathematical results about lattice gauge theories, (3) the precise gap between numerical and rigorous for each major result, (4) assessment of 5 proof strategies with specific bottlenecks.

## Key Findings

**Numerical lattice results are extraordinary in quality:** SU(3) glueball spectrum fully mapped below 4 GeV (0++ at 1730±80 MeV, 2++ at 2400±120 MeV — Morningstar-Peardon 1999), string tension √σ ≈ 420 MeV, asymptotic scaling verified over β = 5.7–7.5, universality confirmed across multiple discretizations, large-N scaling checked for N = 2,...,12 (Athenodorou-Teper 2021). All NUMERICAL ONLY — none rigorously proved for continuous gauge groups at physical coupling.

**The rigorous frontier has advanced significantly (2020–2025):** Adhikari-Cao (2025) proved mass gap for *finite* gauge groups at weak coupling. Chatterjee (2024) constructed the first non-abelian scaling limit in d > 2, but it's Gaussian/trivial. Area law proved in the 't Hooft limit (2025). Stochastic quantization achieves YM-Higgs in 3D (Chandra-Chevyrev-Hairer-Shen 2024) but is fundamentally limited to d < 4.

**The gap is cleanly structured in 7 steps:** Steps 1-2 (UV stability, tightness) are done by Balaban. Steps 3-5 (observables, uniqueness, OS axioms) are Tier 1 — hard but believed tractable. Step 6 (mass gap) is THE Millennium Problem — no known technique works. Step 7 (infinite volume) is conditional on Step 6.

## Key Takeaway
The lattice-to-continuum gap is NOT a single missing lemma — it's a structured chain of 7 steps, of which 2 are complete, 3 are believed achievable, and 2 require fundamentally new ideas. The most promising near-term path is completing Balaban's program to construct YM on T⁴ (without mass gap) — Jaffe-Witten call this alone "a major breakthrough." For the mass gap itself, the Chatterjee probabilistic school is producing the steadiest stream of rigorous results (finite groups → continuous groups is the key barrier), while the stochastic quantization school is blocked at d = 4 by criticality. The finite-to-continuous gauge group transition is the single most important bottleneck in the field right now.

## Leads Worth Pursuing
- Adhikari-Cao's techniques for finite gauge group mass gap — what specifically fails for SU(2)?
- Whether Chatterjee's conditional theorem (strong mass gap ⟹ confinement) can be inverted or strengthened
- The 't Hooft limit area law result (2025) — can finite-N corrections be controlled?
- Spectral gap methods for the lattice transfer matrix as an alternative route to mass gap

## Unexpected Findings
- The 2020–2025 period has seen more rigorous progress on lattice gauge theory than any comparable period since Balaban's work in the 1980s. The Chatterjee school (Stanford) has essentially created a new subfield of "probabilistic lattice gauge theory" that didn't exist before 2018.
- Chatterjee's Gaussian scaling limit for SU(2) YMH (2024) — while trivial — is technically the first time anyone has rigorously constructed ANY scaling limit of a non-abelian lattice gauge theory in d > 2. This deserves more attention as a proof-of-concept.
- The UV problem is completely solved (Balaban 1989, Magnen-Rivasseau-Sénéor 1993). The entire Millennium Problem is an IR problem — confinement and mass gap are infrared phenomena. This is not always clearly stated in popular accounts.

## Computations Identified
1. **Transfer matrix spectral gap analysis for SU(2) on small lattices:** Numerically compute the eigenvalues of the transfer matrix T for pure SU(2) lattice gauge theory on small spatial volumes (e.g., 4³) at various β. Track the ratio of the second-largest eigenvalue to the largest as β increases. If the spectral gap persists, this provides numerical evidence for a rigorous spectral gap argument. Requires: standard lattice gauge theory Monte Carlo code + Lanczos eigenvalue solver. Difficulty: moderate (50–100 lines + existing lattice code). Result: would map the spectral gap as a function of coupling and volume.

2. **Finite group approximation convergence:** Approximate SU(2) by its finite subgroups (binary icosahedral group of order 120, etc.) and numerically check whether Adhikari-Cao mass gap bounds converge to something meaningful as the subgroup → SU(2). Difficulty: moderate (100–150 lines). Result: would test whether the finite→continuous barrier is a technicality or fundamental.
