# Mission Complete: Amplituhedron vs QFT

## One-Sentence Answer

The amplituhedron is not just a better calculator — it encodes physical principles (UV finiteness selection, theory unification through hidden zeros, EFT positivity bounds) — but within N=4 SYM alone, it produces identical predictions to Feynman diagrams and is a mathematically rigorous reformulation, not new physics.

## Summary

Through 7 explorations across 1 strategy, this mission investigated whether the amplituhedron and related positive geometry frameworks reveal deeper physics than standard quantum field theory. The answer has three layers:

**Layer 1 — Within N=4 SYM: Exact reformulation.** All predictions are identical to Feynman diagrams. Locality and unitarity emerge exactly from the geometry (unitarity proved for all n,L,k in JHEP 2020; BCFW triangulation proved in Inventiones 2025). No experiment can distinguish "locality is fundamental" from "locality emerges from positivity." Verified computationally: 4-point MHV amplitude agrees across three methods (Parke-Taylor, BCFW, Grassmannian) to 10⁻¹⁵.

**Layer 2 — Beyond N=4 SYM: Three genuine physical contributions.**

1. **UV finiteness as selection principle.** The full amplituhedron (all-loop positive geometry) REQUIRES UV finiteness. UV divergences produce poles at infinity that break the bounded-region geometry. This selects only N=4 SYM and ABJM from all gauge theories — a physical constraint, not computational convenience.

2. **EFT-hedron: real-world positivity bounds.** Positive geometry constrains which effective field theories can be UV-completed. Wilson coefficients must satisfy positivity and Hankel matrix inequalities. Verified computationally for QED (Euler-Heisenberg satisfies all photon bounds with c₂/c₁ = 7/4 exactly). This is the most concrete real-world output of the positive geometry program.

3. **Hidden zeros and theory unification.** The 2024-2025 discovery that phi³, pion, and gluon amplitudes share kinematic zeros revealed by geometry. A unique one-parameter deformation connects these three seemingly different theories. At 1-loop (March 2025), hidden zeros fix the integrand from a generic non-local, non-unitary ansatz — locality and unitarity EMERGE. This extends beyond N=4 SYM for the first time.

**Layer 3 — The emerging paradigm: Surfaceology.** The field is converging toward a unified picture where all amplitude calculations in colored theories equal integrals over moduli spaces of surfaces. This handles all loops, all multiplicities, non-planar amplitudes. The amplituhedron (N=4 SYM) and surfaceology (colored non-SUSY theories) are parallel programs with a mysterious, unresolved relationship — the most important open question in the field.

## Validation Tier Achievement

| Tier | Status | Evidence |
|------|--------|----------|
| 1: Computation | ✅ Solid | 4-point 3-method agreement to 10⁻¹⁵. EFT-hedron bounds verified. |
| 2: Extension | ✅ Solid | Two-tier structure mapped. 5 cases where geometry exceeds standard methods. |
| 3: Physical Content | ✅ Reached | "Better calculator?" answered with evidence for both N=4 (reformulation) and beyond (physical content). |
| 4: Novelty | Partial | Claims are synthesis, not discovery. Individual components likely known to experts. |
| 5: Implications | Partial | Spacetime emergence identified. Connections to cosmology. Not deeply explored. |

## Consolidated Novel Claims

### Claim 1: EFT-Hedron Saturation Ratio as UV Mass Spectroscopy

**Claim:** The Hankel determinant saturation ratio det(H₂)/g₂₀² exhibits non-monotonic behavior as a function of the UV mass ratio M₂/M₁, reaching maximum deviation from saturation at M₂/M₁ ≈ 1.25–1.50. This could serve as a spectroscopic tool to determine the mass ratio of UV resonances from low-energy EFT measurements alone.

**Evidence:** Computed numerically across a range of M₂/M₁ ratios. Confirmed analytically via closed-form expression (verified to machine precision). The non-monotonic structure arises because degenerate limits (M₂→M₁) and hierarchical limits (M₂≫M₁) both approach single-resonance saturation.

**Novelty:** The basic EFT-hedron bounds are published (arXiv:2012.15849). The spectroscopic interpretation of the saturation ratio's non-monotonic dependence appears to be a novel observation, but it may be implicit in the general analysis — anyone computing det(H₂) for two resonances would see the behavior.

**Strongest counterargument:** The behavior is a trivial consequence of the analytic formula. Practical applicability is limited by narrow-resonance and forward-limit assumptions.

**Status:** Correct observation, uncertain novelty. Moderate strength.

### Claim 2: Two-Tier Structure of Positive Geometry

**Claim:** Positive geometry is not a monolithic framework but has a sharp two-tier structure: (i) the full amplituhedron (all-loop) applies ONLY to N=4 SYM and ABJM (UV-finite theories), while (ii) partial geometric tools (associahedra, Stokes polytopes, scattering forms, surfaceology) apply broadly at tree level and increasingly at loops for non-SUSY theories. The tier boundary is UV finiteness.

**Evidence:** Synthesized from 7+ theory classes across explorations 003, 004, 005, 007. The UV finiteness wall has a precise mechanism: UV divergences produce poles at "infinity" that violate the bounded-region requirement of positive geometry.

**Novelty:** The individual facts are known. The clean two-tier articulation with UV finiteness as the sharp dividing criterion, synthesized across the full landscape of positive geometry applications, appears to be a useful organizational contribution that doesn't exist as a single clear statement in the literature. But experts likely understand this implicitly.

**Strongest counterargument:** This is well-known in the community, just not explicitly stated as a two-tier structure because the community doesn't need the label.

**Status:** Useful synthesis. Novel as articulation, not as discovery.

### Claim 3: Amplituhedron and Surfaceology as Structurally Parallel Programs

**Claim:** The amplituhedron (N=4 SYM, momentum-twistor space) and surfaceology (colored non-SUSY theories, kinematic space) are structurally parallel programs that share a philosophy but address different theories via different mathematical objects. They are NOT related by specialization or generalization. Their unification is the most important open problem in the positive geometry program.

**Evidence:** Extensive literature survey (15+ papers). The amplituhedron uses momentum-twistor variables specific to N=4 SYM's dual conformal symmetry; surfaceology uses kinematic variables that work for any colored theory. No published map exists between them.

**Novelty:** Conference talks and private communications discuss this, but no published paper states it as a central structural conclusion. This is synthesis — organizing what experts know into a clear framework.

**Strongest counterargument:** Arkani-Hamed works on both programs; the distinction is understood by the community without needing to be published.

**Status:** Useful framing for non-specialists. Not novel to experts.

## What Remains Open

The computation registry (COMPUTATIONS-FOR-LATER.md) identifies 11 follow-up computations, the most impactful being:

1. **SMEFT bounds from EFT-hedron** — Apply positivity bounds to Standard Model EFT operators. Would connect positive geometry to LHC physics. (Moderate difficulty, high impact)
2. **Graviton EFT-hedron bounds** — Constrain quantum gravity UV completions from graviton scattering. (Moderate-high difficulty, very high impact)
3. **Surface kinematics → momentum space** — The central open technical problem. Bridge surfaceology results back to standard QFT variables. (Very high difficulty, field-defining)
4. **Amplituhedron-surfaceology bridge** — Compute the same amplitude from both frameworks to characterize the relationship. (High difficulty, high impact)

## Strategy History

| Strategy | Approach | Explorations | Key Finding |
|----------|----------|--------------|-------------|
| 001 | Compute First, Then Break It | 7 (6 success, 1 partial) | Three-layer answer: reformulation in N=4 SYM, physical content beyond, surfaceology as emerging paradigm |
