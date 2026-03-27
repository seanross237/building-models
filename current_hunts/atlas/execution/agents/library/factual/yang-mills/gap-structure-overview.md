---
topic: Gap structure toward Yang-Mills Millennium Prize Problem
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-001 exploration-001; Jaffe-Witten 2000 (Clay problem description), Douglas 2004"
---

## Two-Tier Gap Structure

**Tier 1 — Potentially tractable with known methods:**
- Gap 1: Control of gauge-invariant observables on T⁴
- Gap 2: Uniqueness of the continuum limit on T⁴

**Tier 2 — Fundamental obstruction, needs new ideas:**
- Gap 3: Mass gap (Δ > 0)
- Gap 4: Infinite volume limit T⁴ → R⁴

### 12-Step Reconstruction Chain

| Step | Status |
|------|--------|
| 1. Lattice formulation (Wilson action) | COMPLETED (Wilson 1974, Osterwalder-Seiler 1978) |
| 2. Propagator estimates on lattice | COMPLETED (Balaban [1]-[4], [8]) |
| 3. Block-averaging / RG transformation | COMPLETED (Balaban [6], [7], [10]) |
| 4. Small-field effective action in 4D | COMPLETED (Balaban [11]) |
| 5. Large-field control in 4D | COMPLETED (Balaban [13], [14]) |
| 6. UV stability in 3D (full) | COMPLETED (Balaban [9]) |
| 7. UV stability in 4D (finite volume) | COMPLETED (Balaban [11]-[14]) |
| 8. Continuum limit on T⁴ | PARTIALLY — subsequential limits exist, uniqueness not shown |
| 9. Verification of OS axioms | NOT ATTEMPTED |
| 10. Infinite volume limit T⁴ → R⁴ | NOT ATTEMPTED |
| 11. Mass gap | NOT ATTEMPTED |
| 12. Wightman axioms via OS reconstruction | Automatic IF OS axioms and mass gap established |

## Gap 1: Control of Correlation Functions on T⁴

**Mathematical formulation:** Prove ∃ lim_{ε→0} ⟨W_C⟩_ε for Wilson loops W_C.

**Nature:** Technical — extending Balaban's RG to act on "insertions" (observable generates extra terms at each RG step). Main challenge is combinatorics of tracking insertions through multi-scale decomposition.

**Tractability:** Believed tractable. Jaffe-Witten: "ample indication that known methods could be extended." Dimock's φ⁴₃ work suggests framework understood well enough.

**Difficulty:** Substantial but potentially well-defined extension.

## Gap 2: Uniqueness of Continuum Limit

**Mathematical formulation:** Prove the RG map is a contraction on the space of effective actions at large k.

**Nature:** Technical/conceptual. In superrenormalizable theories, uniqueness follows from contraction near Gaussian fixed point. For 4D YM (marginally renormalizable), logarithmic running complicates the analysis.

**Difficulty:** Moderate to hard. May require new analytical ideas about RG contraction in the marginally renormalizable regime.

## Gap 3: Mass Gap (THE Millennium Problem)

**Mathematical formulation:** Prove ⟨Tr F²(x) · Tr F²(y)⟩_conn ≤ C e^{-Δ|x-y|} with Δ > 0 independent of volume.

**Nature:** Conceptual — no known CQFT method establishes a dynamically generated mass gap.

**Possible approaches:** Duality transformations (Debye screening analogy), large-N expansion (Maldacena), supersymmetric methods (Seiberg-Witten), stochastic analysis (Chatterjee).

**Difficulty:** Fundamental obstruction. Widely regarded as requiring a conceptual breakthrough.

## Gap 4: Infinite Volume Limit

**Mathematical formulation:** Prove correlation functions on T⁴_L converge as L → ∞ and satisfy full OS axioms on R⁴.

**Nature:** Technical IF mass gap established — with exponential decay, standard cluster expansion methods apply.

**Difficulty:** Moderate, conditional on Gap 3. Without mass gap, inaccessible.

## Key Quotes

Jaffe-Witten: "While the construction is not complete, there is ample indication that known methods could be extended to construct Yang-Mills theory on T⁴."

But: "Even if this were accomplished, no present ideas point the direction to establish the existence of a mass gap that is uniform in the volume."

## Note on Claimed Solutions

A preprint (arXiv:2506.00284, May 2025) claimed constructive proof of existence and mass gap for SU(3) YM in 4D. Withdrawn by arXiv administration June 2025. As of March 2026, no verified solution exists.
