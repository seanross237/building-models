# Exploration 001 Summary: Balaban's RG Program for Lattice Yang-Mills

## Goal
Produce a theorem-level technical map of Balaban's renormalization group (RG) program for 4D lattice Yang-Mills theory: paper-by-paper inventory, precise stopping point, technical obstacles, and modern developments.

## Outcome: SUCCEEDED

## What Was Done
Conducted extensive web research across 20+ sources including the official Clay problem description (Jaffe-Witten), Douglas's status report, Chatterjee's authoritative bibliography, Dimock's expository papers, and multiple Springer/arXiv pages to reconstruct the full architecture of Balaban's program.

## Key Findings

### Paper Inventory
Identified and classified all 14 papers in Balaban's series (1983-1989), organized into four phases:
1. **Foundational tools** (papers 1-8, 1983-85): Propagators, averaging operations, gauge fixing, background fields
2. **3D UV stability** (paper 9, 1985): Complete proof for superrenormalizable case
3. **Small-field 4D RG** (papers 10-12, 1985-88): Effective actions, β-functions, cluster expansions in 4D
4. **Large-field 4D** (papers 13-14, 1989): R operation, completing UV stability proof

### The Precise Stopping Point
Balaban's program **achieves ultraviolet stability of 4D lattice Yang-Mills in finite volume** — uniform bounds on the partition function as lattice spacing ε → 0 on a 4-torus. This gives compactness (tightness), hence subsequential convergence to a continuum limit.

**It does NOT achieve:**
- Control of any observable (Wilson loops, correlation functions)
- Uniqueness of the continuum limit
- Infinite volume limit (T⁴ → R⁴)
- Mass gap
- Verification of Osterwalder-Schrader or Wightman axioms

### Gap Structure (Two Tiers)
**Tier 1 — Potentially tractable with known methods:**
- Gap 1: Extend UV stability to control gauge-invariant observables (Wilson loops)
- Gap 2: Prove uniqueness of the continuum limit (RG contraction)
- Gap 3: Verify OS axioms for the limiting theory on T⁴

**Tier 2 — Requires fundamentally new ideas:**
- Gap 4: Prove mass gap Δ > 0 (this IS the Millennium Problem core)
- Gap 5: Take infinite volume limit T⁴ → R⁴ (conditional on mass gap)

### Modern Developments
- **Dimock (2011-2022):** Three-part expository series making Balaban's method accessible via φ⁴₃; extended to QED in d=3
- **Chatterjee (2018-2024):** Probabilistic reformulation; scaling limit of SU(2) YMH (but Gaussian/trivial)
- **Chandra-Hairer-Shen-Chevyrev (2024):** Stochastic quantization of 3D YMH via regularity structures
- **No claimed solutions verified:** A preprint (arXiv:2506.00284) was withdrawn by arXiv admin

## Key Takeaway
Balaban's program represents a **complete ultraviolet analysis** of 4D Yang-Mills. It controls the short-distance structure of the theory and establishes that renormalization "works" rigorously. But it leaves a **two-tier gap**: (1) extending to observables and completing the T⁴ construction (hard but believed feasible), and (2) proving the mass gap (requires new ideas — the heart of the Millennium Problem). The Jaffe-Witten problem description explicitly states that "no present ideas point the direction to establish the existence of a mass gap."

## Unexpected Findings
- The closest active continuation of Balaban's specific methods is Dimock's work on 3D QED (not Yang-Mills), suggesting the community finds extending even to simpler gauge theories in 3D to be a major undertaking.
- The stochastic quantization approach (Chandra-Hairer et al.) is a fundamentally different route that doesn't build on Balaban at all — this may be the most active frontier for d=3.
- Jaffe-Witten note that even a complete construction on T⁴ (without mass gap) "would represent a major breakthrough" — suggesting the community would value completion of Tier 1 gaps alone as a significant result.

## Computations Identified
1. **Contraction analysis of 4D YM RG map:** Numerically study whether Balaban's RG transformation is contractive (in appropriate norms) for the marginally renormalizable 4D case. This would inform Gap 2 (uniqueness). Requires: extracting the explicit RG map from Balaban's papers [11]-[12], implementing it numerically for SU(2) on small lattices. Difficulty: ~100-line numpy/scipy script once the map is formalized, but formalizing from the papers is the hard part.

2. **Wilson loop RG tracking:** Formalize how a Wilson loop observable transforms under one Balaban RG step, and estimate the error bounds. This would inform Gap 1. Requires: detailed reading of papers [6], [10], [11]. Difficulty: conceptual — defining the right framework; the computation itself would be moderate.
