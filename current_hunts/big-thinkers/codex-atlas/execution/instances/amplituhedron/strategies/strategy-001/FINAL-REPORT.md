# Strategy 001 Final Report: Compute First, Then Break It

## Executive Summary

Through 7 explorations (2 computational, 5 research), this strategy investigated whether the amplituhedron and related positive geometry frameworks are merely better calculators for quantum field theory, or reveal deeper physical structure. The answer is nuanced and well-supported:

**Within N=4 SYM: The amplituhedron is a mathematically rigorous reformulation.** All predictions are identical to Feynman diagrams. No experiment can distinguish "locality is fundamental" from "locality emerges from positivity." This was established by our computational verification (exploration 001: three methods agree to 10⁻¹⁵) and confirmed by the literature (exploration 004: multiple experts agree no observable predictions differ).

**Beyond N=4 SYM: Positive geometry produces genuine new physics.** Three concrete contributions have been identified and characterized:

1. **UV finiteness as a geometric selection principle** — The amplituhedron REQUIRES UV finiteness, selecting only N=4 SYM and ABJM from the space of gauge theories. This is physical content: the geometry encodes which theories have consistent UV behavior.

2. **EFT-hedron real-world constraints** — Positivity bounds on Wilson coefficients constrain which effective field theories can be UV-completed. We computationally verified these bounds (exploration 006): forward-limit positivity, Hankel matrix inequalities, and QED Euler-Heisenberg constraints all confirmed. The EFT-hedron is the most concrete real-world output of the program.

3. **Hidden zeros and the unification of theories** — The 2024-2025 discovery that phi³, pion, and gluon amplitudes share kinematic zeros revealed by geometry. A unique one-parameter deformation connects three seemingly different theories. At 1-loop (March 2025), hidden zeros fix the integrand from a generic non-local, non-unitary ansatz — locality and unitarity EMERGE.

**The broader framework: Surfaceology** — The field is converging toward a unified picture where all amplitude calculations in colored theories equal integrals over moduli spaces of surfaces. This framework handles all loops, all multiplicities, and non-planar amplitudes. The amplituhedron (N=4 SYM) and surfaceology (colored non-SUSY theories) are **parallel programs** with a mysterious relationship — unifying them is the most important open problem.

---

## What Was Tried

### Phase 1: Ground Truth (Explorations 001-002)

**Exploration 001 (Math Explorer — SUCCESS):** Implemented spinor-helicity formalism and computed the 4-point tree-level MHV amplitude via Parke-Taylor, BCFW recursion, and Grassmannian/positive geometry. All three methods agree to machine precision (< 10⁻¹⁵) across 10 kinematic configurations. Built reusable computational infrastructure (628 lines of Python).

Key insight: The Grassmannian computation reveals an "angle-square duality" — the amplitude expressed in square-bracket variables equals the Parke-Taylor formula in angle-bracket variables. This structural identity is invisible from either Parke-Taylor or BCFW alone.

**Exploration 002 (Math Explorer — PARTIAL):** Attempted 6-point NMHV tree amplitude via BCFW. Established 6-point kinematics and MHV baseline. Found a structural zero (Channel 3: λ_K ∝ −λ_{1̂} at the pole). BCFW not verified: two independent shifts disagreed due to cyclic color ordering ambiguity in sub-amplitudes. Grassmannian not attempted.

Lesson: BCFW for higher-multiplicity NMHV requires explicit diagram-based orderings. Should provide R-invariant formula as non-recursive ground truth first.

### Phase 2: Extension Map (Explorations 003-004)

**Exploration 003 (Standard Explorer — SUCCESS):** Mapped where positive geometry extends beyond N=4 SYM. Discovered a **two-tier structure**:
- **Tier 1 (Full amplituhedron, all-loop):** Only N=4 SYM and ABJM. Requires Yangian symmetry + planarity + UV finiteness.
- **Tier 2 (Partial geometry, tree-level):** Broad — bi-adjoint scalars (associahedron), phi⁴ (Stokes polytopes), YM tree-level (corolla polynomial), cosmological polytopes, strings.

The essential wall is **UV finiteness**: UV divergences produce poles that are not logarithmic singularities on geometric boundaries, breaking the canonical form interpretation. Five cases where geometry exceeds standard methods were identified.

**Exploration 004 (Standard Explorer — SUCCESS):** Investigated emergent locality and unitarity. Characterized the precise mechanism: locality = canonical form has log poles only on amplituhedron boundaries (positivity screens non-physical poles); unitarity = boundaries factorize as products of smaller amplituhedra. Both proved rigorously (unitarity: JHEP 2020; BCFW triangulation: Inventiones 2025).

Brutal assessment: within N=4 SYM, this is reformulation. But three genuine physical contributions identified (UV selection, EFT-hedron, hidden zeros). The March 2025 paper (arXiv:2503.03805) extends emergence to non-SUSY 1-loop.

### Phase 3: Deep Dives (Explorations 005-007)

**Exploration 005 (Standard Explorer — SUCCESS):** Deep dive into hidden zeros. Hidden zeros = kinematic configurations where amplitudes vanish, revealed by associahedron geometry. Key results: (1) zeros uniquely determine amplitudes (equivalent to enhanced UV scaling), (2) three theories form a unique one-parameter family via δ-deformation, (3) at 1-loop, zeros fix the integrand from a 6,500-parameter non-local ansatz (conjectured + verified at 4-point), (4) extends to cosmological wavefunctions. Critical limitation: loop results live in "surface kinematics," not standard momentum space.

**Exploration 006 (Math Explorer — SUCCESS):** Computationally verified EFT-hedron positivity bounds. Forward-limit bounds (g_{n,0} ≥ 0) confirmed for 3 UV-complete models, correctly violated by ghost. Hankel matrix bounds verified (single resonance saturates, two resonances give strict inequality). QED Euler-Heisenberg satisfies all photon bounds with c₂/c₁ = 7/4 exactly. Unexpected: non-monotonic saturation ratio suggests UV spectroscopy tool.

**Exploration 007 (Standard Explorer — SUCCESS):** Deep dive into surfaceology. Amplitudes = integrals over fatgraph surface parameter spaces with curve-counting integrands. Handles all loops, all multiplicities, non-planar. Key 2024-2026 results: canonical YM loop integrand (PRL 2025), cut equation recursion, cosmohedra for cosmological wavefunctions. Monte Carlo sampling makes 10-loop feasible. Critical distinction: surfaceology and amplituhedron are parallel programs, not nested.

---

## Most Promising Findings

### Finding 1: The Two-Tier Structure of Positive Geometry

Positive geometry is NOT a monolithic framework. It has two tiers:
- An inner tier (amplituhedron proper) that works only for UV-finite theories (N=4 SYM, ABJM) at all loops
- An outer tier (scattering forms, associahedra, surfaceology) that works for all colored theories at tree level and increasingly at loops

The essential distinction is UV finiteness. This is physical content, not just mathematical convenience.

### Finding 2: The EFT-Hedron as UV Spectroscopy

The EFT-hedron bounds are not just existence constraints — the Hankel matrix eigenstructure encodes information about the UV spectrum. Our computation shows that the saturation ratio is non-monotonic in M₂/M₁, suggesting measurable fingerprints of the UV spectrum from low-energy data alone.

### Finding 3: The Hidden Zeros Unity of Theories

The unique δ-deformation connecting phi³, NLSM (pions), and Yang-Mills (gluons) is a structural theorem: these three theories form a one-dimensional family in "theory space." This is a genuinely new result not visible from any single Lagrangian.

### Finding 4: Surfaceology as the Emerging Paradigm

The surfaceology framework is solving problems that have been open for 30+ years (canonical YM integrand), handling non-planar amplitudes that the amplituhedron cannot reach, and extending to cosmological observables. The field is converging on this framework as the master structure for colored amplitude theory.

---

## What I'd Recommend the Next Strategy Focus On

1. **The amplituhedron-surfaceology bridge.** The relationship between these parallel programs is the most important open question. A computational exploration comparing 6-point MHV amplitudes from both frameworks would make this concrete.

2. **SMEFT bounds from the EFT-hedron.** Apply the EFT-hedron to Standard Model EFT operators. This would connect the positive geometry program directly to LHC physics — the highest-impact application.

3. **Surface kinematics → momentum space.** The central technical challenge. If hidden zeros can be translated to standard momentum-space variables, the emergence program becomes directly relevant to practical amplitude calculations.

4. **Graviton EFT-hedron bounds.** Computing positivity bounds for graviton-graviton scattering would constrain quantum gravity UV completions — a direct connection to the quantum gravity problem.

5. **Computational verification of hidden zeros.** Verify the 5-point Tr(phi³) hidden zero explicitly (trivial computation) and attempt the surface-kinematics 1-loop integrand for 4-point (moderate difficulty).

---

## Novel Claims

### Claim 1: EFT-Hedron Saturation Ratio as UV Mass Spectroscopy

**Claim:** The Hankel determinant saturation ratio det(H₂)/g₂₀² exhibits non-monotonic behavior as a function of the UV mass ratio M₂/M₁, reaching maximum deviation from saturation at M₂/M₁ ≈ 1.25-1.50 and returning to near-saturation for both degenerate and hierarchical limits. This non-monotonic structure could serve as a "spectroscopic tool" to determine the mass ratio of UV resonances from low-energy EFT measurements alone.

**Evidence:** Computed numerically in exploration 006 across a range of M₂/M₁ ratios. Confirmed analytically via the closed-form expression det(H₂) = (16π)² A B (M₁²-M₂²)² / (M₁M₂)^{10} for two delta-function resonances (verified to 0.000000% error vs numerical).

**Novelty search:** The basic EFT-hedron bounds are published (arXiv:2012.15849). The interpretation of the saturation ratio as a spectroscopic tool with non-monotonic behavior appears to be a novel observation — the original paper discusses saturation but not its non-monotonic dependence on mass ratios. However, this may be implicit in the general analysis.

**Strongest counterargument:** The non-monotonic behavior is trivially implied by the analytic formula — anyone who computed det(H₂) for two resonances would see it. It may be considered an obvious consequence rather than a novel result. Also, the practical applicability is limited by the assumption of narrow resonances and the restriction to t=0 (forward limit).

**Status:** Partially verified / likely implicit in published work. The observation is correct but its novelty is uncertain.

### Claim 2: Amplituhedron and Surfaceology as Parallel (Not Nested) Programs

**Claim:** The amplituhedron (N=4 SYM, momentum-twistor space) and surfaceology (colored non-SUSY theories, kinematic space) are structurally parallel programs that share a philosophy but address different theories. They are NOT related by specialization or generalization. The relationship between them is the most important open question in the positive geometry program.

**Evidence:** Extensive literature survey across explorations 003, 005, 007. The amplituhedron uses momentum-twistor variables specific to N=4 SYM's dual conformal symmetry; surfaceology uses kinematic variables (Mandelstam-like) that work for any colored theory. No published paper establishes a map between them. The founding surfaceology paper (arXiv:2309.15913) explicitly states the framework applies to "Tr(phi³) and related theories" — N=4 SYM is not mentioned.

**Novelty search:** This structural observation appears in various conference talks and private communications but is not explicitly stated as a central conclusion in any published paper we found. Most presentations assume a vague "positive geometry" umbrella without distinguishing the two programs.

**Strongest counterargument:** Experts in the field likely understand this implicitly. Arkani-Hamed works on both programs simultaneously, and the distinction may be well-known without being explicitly published. This may be synthesis, not discovery.

**Status:** Established observation / likely well-known to experts but not clearly stated in the literature. Useful as a framing for non-specialists.

### Claim 3: UV Finiteness as the Essential Wall for Loop-Level Positive Geometry

**Claim:** The reason the full amplituhedron (all-loop positive geometry) is restricted to N=4 SYM and ABJM is specifically UV finiteness: UV divergences produce poles at "infinity" (loop momentum → ∞) that violate the bounded-region requirement of positive geometry. This is not merely a technical limitation but a physical selection principle — positive geometry selects UV-finite theories.

**Evidence:** Established across explorations 003 and 004 from multiple sources. The amplituhedron is a bounded region in projective momentum-twistor space; UV divergences would require unbounded boundaries. The EFT-hedron (exploration 006) shows the related principle: UV-completability imposes positivity constraints on Wilson coefficients.

**Novelty search:** This is discussed in the original amplituhedron papers and in review articles (arXiv:2203.13018). The framing as a "selection principle" rather than a "limitation" appears in talks by Arkani-Hamed but may not be explicitly stated as a central result in published papers.

**Strongest counterargument:** This is well-known in the community. The restriction of the amplituhedron to UV-finite theories has been understood since the original 2013 paper. Our contribution is synthesizing and clearly stating it, not discovering it.

**Status:** Established / well-known. Our contribution is clear articulation and evidence synthesis, not novelty.

---

## Methodology Assessment

**What worked well in the "Compute First, Then Break It" strategy:**
- Starting with computation (4-point tree-level) built confidence in the framework before making claims
- The computational infrastructure enabled verification of EFT-hedron bounds (exploration 006)
- The three-phase structure (ground truth → stress test → probe) was natural and productive

**What didn't work well:**
- Phase 1 took 2 explorations but only one was fully successful (4-point). The 6-point NMHV BCFW bug consumed an exploration without resolution. Should have used R-invariants as ground truth from the start.
- The "compute first" emphasis was less valuable than expected — the most productive explorations (003-005, 007) were literature surveys, not computations. The math explorations (001, 002, 006) had more overhead (long thinking phases, debugging cycles).
- The strategy suggested "half the budget on Phase 1" — I correctly deviated (spending only 2/10 on Phase 1, 5/10 on Phases 2-3).

**Standard explorers dominated:** 5 of 7 explorations were standard (literature survey) explorers. These consistently completed in ~15 min with 400-500 lines of well-cited reports. Math explorers took 30-50 min with more overhead. For a topic like the amplituhedron where the key findings are structural rather than computational, literature surveys are more productive than computation.

---

## Appendix: Exploration Summary Table

| # | Type | Goal | Outcome | Key Finding |
|---|------|------|---------|-------------|
| 001 | Math | 4-pt MHV 3 methods | ✅ Success | All agree to 10⁻¹⁵. Angle-square duality. |
| 002 | Math | 6-pt NMHV BCFW+Grassmannian | ⚠️ Partial | MHV baseline verified. BCFW buggy. |
| 003 | Standard | Extension map beyond N=4 | ✅ Success | Two-tier structure. UV finiteness wall. |
| 004 | Standard | Emergent locality/unitarity | ✅ Success | Reformulation in N=4. 3 contributions beyond. |
| 005 | Standard | Hidden zeros deep dive | ✅ Success | Zeros determine amplitudes. 3 theories unified. |
| 006 | Math | EFT-hedron computation | ✅ Success | All bounds verified. Saturation ratio insight. |
| 007 | Standard | Surfaceology framework | ✅ Success | Parallel to amplituhedron. All-loop, non-planar. |
