---
topic: Chatterjee's probabilistic approach to Yang-Mills
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-001 exploration-001, exploration-004, exploration-006; Chatterjee arXiv:1803.01950 (2018), arXiv:2401.10507 (2024), arXiv:2602.00436 (2026); Adhikari-Cao Ann. Prob. 53(1) 2025; Adhikari et al. arXiv:2509.04688 (2025); Cao arXiv:2510.22788 (2025); Rajasekaran-Yakir-Zhou arXiv:2603.24555 (2026)"
---

## Overview

Sourav Chatterjee (Stanford) has pursued a probabilistic reformulation of the constructive Yang-Mills problem, distinct from Balaban's RG approach.

## Key Results

1. **"Yang-Mills for probabilists"** (arXiv:1803.01950, 2018) — Survey reformulating the constructive YM problem in probabilistic language. Authoritative bibliography of Balaban's papers.

2. **Wilson loop expectations for finite gauge groups** — Exact leading-order behavior:
   - Z₂ gauge group (Chatterjee, CMP 377, 2020)
   - Finite abelian groups (Forsström-Lenells-Viklund, Ann. Inst. H. Poincaré 58(4), 2022)
   - All finite groups including non-abelian (Cao, CMP 380, 2020)

3. **Strong mass gap ⟹ quark confinement** — Proved that if a strong form of the mass gap holds (exponential decay under arbitrary boundary conditions), then Wilson's area law follows for gauge groups with nontrivial center. For SU(3) (center Z₃): strong mass gap at all couplings ⟹ confinement at all couplings. Key insight: minimum steps to shrink a loop = minimum enclosed surface area. Conditional on unproven mass gap.

4. **Scaling limit of SU(2) lattice Yang-Mills-Higgs** (arXiv:2401.10507, 2024) — First construction of a scaling limit of a non-abelian lattice Yang-Mills theory in dimension > 2, with Higgs field. Triple scaling: ε → 0, g → 0 with g = O(ε^{50d}), α → ∞ with αg = cε. **The limit is Gaussian (trivial)** — extreme scaling suppresses all non-linear dynamics. Explicitly states: "The question of constructing a non-Gaussian scaling limit remains open."

5. **Mass gap for finite gauge groups** (Adhikari-Cao, Ann. Prob. 53(1), 140–174, 2025) — Proved exponential decay of correlations for gauge-invariant functions (including Wilson loops) in lattice gauge theories with **finite** gauge groups at weak coupling. This establishes a mass gap for finite (non-abelian) gauge groups. **Critical limitation:** Does not extend to continuous groups (SU(2), SU(3)). Techniques rely on finiteness of the gauge group.

6. **Area law at β < 1/24** (**Cao-Nissim-Sheffield**, arXiv:2509.04688, Sept 2025) — Proves Wilson's area law for U(N), SU(N), SO(2(N-1)) at coupling β < 1/(8(d-1)) = **1/24 in d=4** — doubling the SZZ mass gap threshold. Uses Bakry-Émery on σ-model at vertices (Hessian bound 4(d-1)Nβ, half of SZZ's 8(d-1)Nβ for edges) + Durhuus-Fröhlich slab argument. **Limitation:** string tension constant decays with N; see CNS May 2025 for N-independent result. *[Note: previously misattributed to Adhikari-Suzuki-Zhou-Zhuang — corrected by exploration-001, March 2026. See also `cao-nissim-sheffield-area-law-extension.md`.]*

7. **U(N) mass gap in 't Hooft regime** (Cao, arXiv:2510.22788, October 2025) — Establishes mass gap, unique infinite volume limit, and large-N limit for U(N) by recasting as a random-environment SU(N) model. Overcomes the obstacle that U(N) has non-uniformly-positive Ricci curvature (unlike SU(N)).

8. **Logarithmic confinement in 3D** (Chatterjee, arXiv:2602.00436, January 2026) — Proves |⟨W_ℓ⟩| ≤ n · exp{-c(1+nβ)^{-1} · T · log(R+1)} for 3D Wilson lattice gauge theory with gauge group G ⊆ U(n) containing the full circle of scalar matrices (the "central U(1)" condition). Establishes **logarithmic quark-antiquark potential** (not area law) in 3D for continuous groups. Applies to SU(n). Short, self-contained proof combining Fröhlich's comparison inequality with earlier techniques.

9. **Gaussian limits for all compact groups** (Rajasekaran-Yakir-Zhou, arXiv:2603.24555, March 2026) — Extends Chatterjee's SU(2) Gaussian scaling limit to **ALL compact connected matrix Lie groups** in any d ≥ 2, in the "complete breakdown of symmetry" regime. Shows the Gaussian limit phenomenon is universal, not SU(2)-specific. **Limit is still Gaussian/trivial.**

## Complete Timeline

| Year | Result | Authors | Citation |
|------|--------|---------|----------|
| 2018 | "Yang-Mills for probabilists" — probabilistic reformulation | Chatterjee | arXiv:1803.01950 |
| 2020 | Wilson loops for Z₂ gauge theory | Chatterjee | CMP 377 |
| 2020 | Wilson loops for ALL finite gauge groups | Cao | CMP 380 |
| 2021 | Strong mass gap ⟹ confinement | Chatterjee | CMP 385 |
| 2022 | Wilson loops for finite abelian groups | Forsström-Lenells-Viklund | Ann. IHP 58(4) |
| 2023 | Mass gap at strong coupling (SU(N), Langevin) | Shen-Zhu-Zhu | CMP 400 |
| 2024 | Gaussian scaling limit SU(2) YMH | Chatterjee | arXiv:2401.10507 |
| 2025 | Mass gap for finite gauge groups | Adhikari-Cao | Ann. Prob. 53(1) |
| 2025 | Area law at β < 1/24 (σ-model on vertices) | Cao-Nissim-Sheffield | arXiv:2509.04688 |
| 2025 | Area law (U(N), N-independent constant) | Cao-Nissim-Sheffield | arXiv:2505.16585 |
| 2025 | U(N) mass gap in 't Hooft regime | Cao | arXiv:2510.22788 |
| 2026 | 3D confinement with central U(1) | Chatterjee | arXiv:2602.00436 |
| 2026 | Gaussian limits for all compact groups | Rajasekaran-Yakir-Zhou | arXiv:2603.24555 |

12 papers in 8 years, all building on each other. Pace is accelerating.

## Chatterjee's Own Assessment (October 2025)

Harvard Millennium Prize Problems lecture: characterized the constructive field theory program as having achieved "many successes" but "not reached its original goal." Emphasized "exciting recent progress" but notably did **not** claim the field is close to a proof.

## Assessment

The most active constructive YM research front. 12 papers over 8 years: finite-group Wilson loops (2020) → finite-group mass gap (2025) → 't Hooft area law (2025) → 3D confinement (2026). The critical open gap is extending from finite to continuous gauge groups — the four-layer structural obstruction (see `adhikari-cao-technique-and-obstruction.md`) means the swapping map framework has no natural extension to SU(N). The trivial scaling limits (SU(2) and now all compact groups) show continuum limits CAN be constructed but are fundamentally non-interacting. Proving exponential correlation decay for SU(2) or SU(3) at even a single coupling β₀ > 0 would be transformative.
