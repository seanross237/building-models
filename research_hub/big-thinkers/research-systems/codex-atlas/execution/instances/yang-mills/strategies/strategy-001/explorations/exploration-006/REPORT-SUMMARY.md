# Exploration 006 Summary: The Modern Rigorous Frontier

## Goal
Deep technical analysis of the three most important recent rigorous results in constructive Yang-Mills theory (Adhikari-Cao mass gap for finite groups, Chatterjee's probabilistic program, connections between approaches) and an honest assessment of proximity to solving the Millennium Prize Problem.

## What Was Tried
Systematic research into 17 papers from 2018-2026, focusing on extracting precise theorem statements, identifying the mathematical obstruction preventing extension from finite to continuous gauge groups, and mapping the complementarity between different approaches.

## Outcome: SUCCEEDED

### Key Findings

**1. Adhikari-Cao (2025) — Theorem 1.1 fully extracted.** Proves exponential correlation decay for ALL finite gauge groups at weak coupling β ≥ (114 + 4log|G|)/Δ_G, using a novel "swapping map" technique (NOT cluster expansion). The technique reformulates gauge theory via homomorphisms into finite groups and uses topological defect decomposition.

**2. The finite→continuous obstruction has FOUR layers** (not one):
- Discrete homomorphism space becomes continuous/uncountable for Lie groups
- Counting bounds (|G|^{|P|}) become meaningless for continuous G
- Swapping map requires discrete bijections with no continuous analog
- Spectral gap Δ_G → 0 as finite subgroups approach SU(2), making quantitative estimates degenerate

These are **structural, not technical** — the entire framework has no natural extension to SU(2).

**3. Chatterjee's conditional theorem** (CMP 385, 2021): Strong mass gap (exponential decay under arbitrary boundary conditions) ⟹ unbroken center symmetry ⟹ confinement (area law), for compact connected groups with nontrivial center. The implication is strictly one-directional and conditional on unproven mass gap.

**4. Every existing result has a critical limitation:** wrong groups (finite), wrong coupling (strong, β < 1/48), wrong dimension (3D), wrong limit ('t Hooft/large-N), or trivial dynamics (Gaussian scaling limits). No result touches SU(2) or SU(3) at weak coupling in 4D.

**5. The field is accelerating** — 12+ papers from Chatterjee's school alone in 2018-2026, with the pace increasing. Most recent: 3D confinement with logarithmic potential (Chatterjee, Jan 2026) and universal Gaussian scaling limits for all compact groups (Rajasekaran-Yakir-Zhou, Mar 2026).

## Key Takeaway
The Millennium Prize mass gap problem remains a **20-50+ year problem**. The 2020-2026 period represents the most productive era of rigorous progress since Balaban's 1980s work, but every result so far operates in a regime that carefully avoids the core difficulty: SU(N) at weak coupling in 4D. The finite→continuous obstruction is fundamental, not a gap that incremental improvement can close. A conceptual breakthrough — a genuinely new technique for proving spectral gaps in continuous gauge theories — is required.

## Unexpected Findings
- **The swapping map is the innovation, not cluster expansion.** Adhikari-Cao explicitly state that non-abelian theories "do not (as of yet) admit a cluster expansion." Their technique is topological/combinatorial, not analytical, which explains why it's inherently finite-group.
- **Chatterjee's 2026 3D result gives logarithmic confinement, not area law.** This is weaker than expected — even in 3D with continuous groups, only logarithmic quark-antiquark potential is proved, not linear confinement.
- **Three completely independent research fronts** are active: (a) Chatterjee school (probabilistic), (b) Chandra-Hairer school (regularity structures), (c) Shen-Zhu-Zhu (stochastic analysis/Langevin). They don't currently interact but could potentially be combined.

## Leads Worth Pursuing
- The Shen-Zhu-Zhu Bakry-Émery approach works for continuous groups but only at strong coupling. Extending the coupling range is the most promising concrete direction.
- Computing how mass gap bounds for binary icosahedral group (|G|=120) and other finite SU(2) subgroups behave as |G| → ∞ would quantify exactly how the Adhikari-Cao bounds degenerate.

## Computations Identified
1. **Finite subgroup mass gap convergence study** (medium difficulty, ~100-line Python script): For G_n = finite subgroups of SU(2) with increasing |G_n|, compute Δ_{G_n} and the resulting mass gap bound from Adhikari-Cao. Plot how the correlation length diverges as G_n → SU(2). This would quantify obstruction #4.
2. **Bakry-Émery curvature bound as function of β** (medium difficulty, symbolic computation): For SU(2) on a small lattice, compute the Bakry-Émery criterion value as a function of β to see where it fails. This would map the boundary of the strong-coupling regime precisely.
