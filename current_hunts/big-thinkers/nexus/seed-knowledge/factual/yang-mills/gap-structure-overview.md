---
topic: Gap structure toward Yang-Mills Millennium Prize Problem
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-001 exploration-001, exploration-004, exploration-006; Jaffe-Witten 2000 (Clay problem description), Douglas 2004"
---

## Classification: Numerical vs. Rigorous Status

| Result | Numerical | Rigorous | Gap |
|:---|:---|:---|:---|
| Confinement (area law at physical coupling) | ✓ Established | ✗ Not proved for SU(N) weak coupling | Fundamental |
| Mass gap Δ > 0 | ✓ m(0++) ≈ 1.7 GeV (SU(3)) | ✗ Not proved for continuous groups | **THE** Millennium problem |
| Asymptotic scaling | ✓ Verified β = 5.7–7.5 | ✗ Non-perturbative statement unproved | UV done (Balaban), IR open |
| Continuum limit existence | ✓ Consistent extrapolations | Partially (subsequential limits) | Uniqueness unproved |
| Universality | ✓ Multiple actions agree | ✗ Not proved | Requires uniqueness |
| Glueball spectrum | ✓ Full spectrum below 4 GeV | ✗ Not proved | Requires mass gap + construction |
| String tension | ✓ √σ ≈ 420 MeV | ✗ Not at weak coupling | Requires area law |
| Deconfinement transition | ✓ T_c ≈ 270 MeV (SU(3)) | Partially (strong coupling, finite groups) | Requires full construction |

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

## 7-Step Lattice-to-Continuum Chain (Logical Dependencies)

| Step | Status | Notes |
|:---|:---|:---|
| 1. UV stability | **PROVED** (Balaban 1982-89) | Partition function bounded uniformly as ε → 0 on T⁴ |
| 2. Tightness of measures | **FOLLOWS** from Step 1 | Subsequential limits exist by Prokhorov's theorem |
| 3. Control of observables | **NOT PROVED** | Need ⟨W_C⟩_ε → limit. Requires extending Balaban's RG to track gauge-invariant insertions. Believed tractable. |
| 4. Uniqueness of limit | **NOT PROVED** | Need RG map is a contraction. Logarithmic running at d=4 makes this much harder than d<4. Key conceptual gap. |
| 5. Reflection positivity | **NOT PROVED** | Holds on lattice for Wilson action; preservation under ε → 0 requires Step 3. |
| 6. Mass gap | **COMPLETELY OPEN** | No known technique can establish Δ > 0 from constructive framework. THE Millennium Problem core. |
| 7. Infinite volume T⁴ → R⁴ | **CONDITIONAL** on Step 6 | With mass gap, exponential decay makes this tractable via cluster expansion. |

**Summary:** Steps 1–2 done. Steps 3–5 believed tractable (Tier 1). Step 6 needs conceptual breakthrough (Tier 2). Step 7 conditional on Step 6.

### OS Axioms (What the Continuum Limit Must Satisfy)

The Jaffe-Witten formulation requires Euclidean Schwinger functions satisfying:
- **(E0)** Temperedness/growth condition
- **(E1)** Euclidean covariance (SO(4) rotations + translations)
- **(E2)** Reflection positivity: ⟨θf · f⟩ ≥ 0
- **(E3)** Symmetry under permutations
- **(E4)** Cluster property: correlations → product at large separation
- **(E0')** Linear growth condition (for Wightman reconstruction)

Plus mass gap: connected correlator of gauge-invariant operators decays as exp(−Δ|x−y|) with Δ > 0.

## Key Quotes

Jaffe-Witten: "While the construction is not complete, there is ample indication that known methods could be extended to construct Yang-Mills theory on T⁴."

But: "Even if this were accomplished, no present ideas point the direction to establish the existence of a mass gap that is uniform in the volume."

## Explicit Negative Status (as of March 2026)

What remains **NOT proved** despite recent progress:
- Mass gap for ANY continuous gauge group at weak coupling in 4D
- Mass gap for SU(2) or SU(3) at ANY coupling in 4D
- Mass gap for pure Yang-Mills (no Higgs) in ANY dimension > 2 at weak coupling
- Non-Gaussian scaling limit of any non-abelian gauge theory in d > 2
- Confinement (area law) for SU(N) at finite N at weak coupling in 4D
- Area law (linear confinement) in 3D at weak coupling — Chatterjee (2026) proves only logarithmic confinement

## Note on Claimed Solutions

A preprint (arXiv:2506.00284, May 2025) claimed constructive proof of existence and mass gap for SU(3) YM in 4D. Withdrawn by arXiv administration June 2025. As of March 2026, no verified solution exists.
