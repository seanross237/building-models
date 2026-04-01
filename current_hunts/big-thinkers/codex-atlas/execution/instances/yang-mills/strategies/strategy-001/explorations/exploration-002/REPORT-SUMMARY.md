# Exploration 002 Summary: Constructive QFT — What Works in 2D/3D and What Breaks in 4D

## Goal
Map constructive QFT successes in lower dimensions and identify exactly which mathematical techniques fail when extended to 4D, relevant to the Yang-Mills Millennium Prize Problem.

## What Was Tried
Systematic web research cataloging all major rigorous QFT constructions in 2D and 3D, analyzing the technical methods used in each, and tracing exactly what fails when each technique is applied to 4D.

## Outcome: SUCCEEDED

### Key Findings

**Catalog of constructions (8 major results):**
1. **φ⁴₂** (Glimm-Jaffe-Spencer 1974) — Full Wightman axioms + mass gap via cluster expansion
2. **φ⁴₃** (Feldman-Osterwalder 1976) — Full Wightman axioms + mass gap via phase space expansion
3. **Yukawa₂** — Full construction via Euclidean functional integrals
4. **Gross-Neveu₂** (Feldman-Magnen-Rivasseau-Sénéor 1985-86) — First rigorous construction of an asymptotically free QFT; uses Pauli principle
5. **YM₂** (Driver 1989, Sengupta 1997) — Exactly solvable; topological (no local degrees of freedom)
6. **Lattice gauge theories** (Brydges-Fröhlich-Seiler 1979-81) — Strong coupling results in any dimension
7. **Balaban's program** (1982-89) — UV stability for YM in 3D (full) and 4D (small field only); incomplete
8. **YM-Higgs₃** (Chandra-Chevyrev-Hairer-Shen 2024) — Stochastic quantization via regularity structures; state of the art

**The single most important technical distinction is super-renormalizability vs. just-renormalizability:**
- In d=2,3: coupling constant has positive mass dimension → finitely many divergent diagrams → cluster expansions converge
- In d=4: coupling is dimensionless → infinitely many divergent diagrams at every order → cluster expansions fail to converge

**Three specific 4D failure modes identified:**
1. **Cluster expansion divergence** — loses convergence because dimensionless coupling provides no automatic small factors at each scale
2. **Large field problem** — field fluctuations at critical dimension d=4 are insufficiently suppressed by the action
3. **Infinite renormalization convergence** — must prove an infinite iterative RG procedure converges non-perturbatively; no one has done this

**φ⁴₄ triviality (Aizenman-Duminil-Copin 2021):** The continuum limit of φ⁴ in 4D is provably trivial (Gaussian/free). This shows the 4D obstruction is real and structural, not just technical. Yang-Mills is expected to escape triviality due to asymptotic freedom, but this is unproven.

**Closest approach to 4D YM:** Magnen-Rivasseau-Sénéor (1993) constructed YM₄ with infrared cutoff but no UV cutoff. UV renormalization is solved; the IR problem (infinite volume, confinement, mass gap) is what remains.

## Key Takeaway
The constructive QFT toolbox was built for super-renormalizable theories. Every successful construction in 2D/3D exploits super-renormalizability in an essential way. The 4D barrier is not a single missing lemma — it's the fact that the entire constructive framework loses its convergence mechanism when the coupling becomes dimensionless. New mathematical ideas are required, not refinements of existing techniques.

## Leads Worth Pursuing
- Balaban's program was never completed and is poorly understood by the current generation; the Brydges-Dimock-Hurd exposition (2014) attempted to make it accessible
- Stochastic quantization (Hairer school) succeeded in 3D but is fundamentally limited to subcritical/super-renormalizable regime; extending to critical would be revolutionary
- The Gross-Neveu construction shows asymptotically free theories CAN be rigorously constructed, but only with the Pauli principle (fermions); finding an analog for bosonic gauge fields is an open problem

## Unexpected Findings
- The 2D Yang-Mills construction is essentially irrelevant to the 4D problem because 2D YM is topological with no local degrees of freedom — it's an entirely different kind of theory
- The Magnen-Rivasseau-Sénéor result (1993) is underappreciated: it shows the UV problem for 4D YM is solved. The entire difficulty is in the infrared (confinement and mass gap). This reframes the Millennium Prize Problem as primarily an IR problem, not a UV one.
- There may be fundamental incompatibility between the OS axioms, mass gap, and asymptotic freedom when imposed simultaneously — a recent preprint raises this concern, though it's not yet peer-reviewed

## Computations Identified
1. **Numerical verification of Balaban's bounds in small lattice volumes** — Could check whether the UV stability bounds from Balaban's program are tight or have room for improvement. Would require implementing the block-spin RG for SU(2) lattice gauge theory on small lattices (e.g., 8⁴). Difficulty: moderate (100-200 lines of code for the RG step, but conceptual understanding of Balaban's setup needed). Result would tell us if there's unexploited room in the bounds.
2. **Beta function coefficients for non-perturbative RG schemes** — Compare perturbative beta function with Balaban-style block-spin beta function on the lattice. Could illuminate how perturbative AF connects to non-perturbative UV stability. Difficulty: moderate; would require lattice gauge theory simulation code.
