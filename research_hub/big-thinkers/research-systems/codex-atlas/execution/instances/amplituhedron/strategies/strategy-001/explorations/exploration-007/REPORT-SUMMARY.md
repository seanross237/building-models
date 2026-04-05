# Exploration 007 Summary: Surfaceology — The Unifying Framework

## Goal
Deep dive into the surfaceology program (curves on surfaces for scattering amplitudes): understand the mathematical framework, how it unifies prior approaches, what new results it has produced (2023-2026), its connection to string theory, and whether it extends to non-planar amplitudes.

## What Was Done
Systematic survey of ~15 papers from 2023-2026: the founding paper (arXiv:2309.15913), the all-multiplicity extension (arXiv:2311.09284), the NLSM connection (arXiv:2403.04826), fermionic extension (arXiv:2406.04411), Yang-Mills integrand (arXiv:2408.11891, PRL 2025), the cut equation (arXiv:2412.21027), superstring connection (arXiv:2504.21676, SciPost 2025), surface soft theorem (arXiv:2505.17179), leading singularities (arXiv:2512.17019), and the newest papers (arXiv:2602.15102, arXiv:2603.03425). Full extraction of mathematical content including explicit formulas.

## Outcome: SUCCESS

Clear, detailed understanding of the framework with specific mathematical content. Unification map covering 7+ prior approaches. Current status as of early 2026.

## Key Takeaway

**Surfaceology is the all-loop, all-multiplicity generalization of positive geometry in kinematic space, covering colored theories (φ³, NLSM, Yang-Mills, Yukawa, strings) but NOT N=4 SYM (which belongs to the amplituhedron program).**

The core structure: scattering amplitudes = integrals over parameter space of fatgraph surfaces, where the integrand is determined by counting curves on the surface via 2×2 matrix products. The key formula:

```
A = ∫ [d^E t / MCG]  exp(−∑_C α_C(t) · (P_C² + m²))
```

where E = n + 3(L−1) is the number of internal edges, the α_C are "headlight functions" (tropicalized u-variables), and the integration automatically recovers all Feynman diagrams from cones in the g-vector fan.

**Three key properties distinguish this from all prior frameworks:**
1. Works at ALL loop orders and ALL multiplicities simultaneously (not just tree or 1-loop)
2. Handles non-planar amplitudes (higher-genus surfaces) naturally — unlike the amplituhedron
3. Provides a canonical formulation that makes hidden zeros, soft theorems, and string limits all manifest

## Unification Map (Brief)

| Framework | Connection |
|---|---|
| ABHY associahedron | Disk (g=0, L=0) special case; triangulations = Feynman diagrams |
| String theory | u-variables define string amplitude; QFT = α'→0 limit |
| NLSM | Tr(φ³) with δ-shift X_{e,e}→X+δ, X_{o,o}→X−δ |
| Yang-Mills | Scalar scaffolding: residue of 2n-scalar amplitude |
| Hidden zeros | Pairwise cancellations of triangulations = manifest in surface integrand |
| Colored Yukawa | Fermionic numerators = combinatorial determinants |
| **Amplituhedron** | **NOT a special case** — distinct framework, different theories |
| Cosmology | New: cosmohedra extend positive geometry to wavefunctions |

## Amplituhedron vs. Surfaceology — Critical Distinction

The amplituhedron (N=4 SYM, twistor space) and surfaceology (colored non-SUSY theories, kinematic space) are PARALLEL programs, not nested ones. They share a philosophy and key authors (Arkani-Hamed) but address different theories. The relationship between them — whether there is a deeper unification — is explicitly open and probably the most important question in the field.

## New Results (2024-2026)

1. **Canonical Yang-Mills loop integrand** (PRL 2025): solved a 30-year-old open problem using "surface kinematics" — which assigns distinct variables to homologous curves, eliminating the 1/0 ambiguities that plagued all prior approaches
2. **Cut equation** (Dec 2024): a single universal recursion ∂_{x_C} G_S = G_{S\C} generates all-order NLSM planar integrands without spurious poles
3. **Superstring amplitudes meet surfaceology** (SciPost 2025): superstring amplitudes = gauge-invariant combinations of bosonic string amplitudes, all expressible in the curve-integral framework
4. **Leading singularities from curve covers** (Dec 2025): gluon 1-loop leading singularities = sum over ways to cover the graph with non-overlapping curves
5. **Cosmohedra** (Dec 2024) and **Combinatorics of the Cosmohedron** (Mar 2026): extension of positive geometry to cosmological wavefunctions

## Connection to String Theory

String theory is precisely surfaceology at finite α': replace the step-function cones with smooth u-variable functions on moduli space. The field theory limit α'→0 sharpens the smooth u-variables into step functions (triangulation cones). Surfaceology provides a CFT-free, purely combinatorial formulation of string amplitudes via hyperbolic geometry of Teichmüller space.

## Non-Planar Status

YES — surfaceology handles non-planar amplitudes through higher-genus surfaces. Explicit all-multiplicity formulas through 2-loop (planar and non-planar) are proved in arXiv:2311.09284. This is a major advantage over the amplituhedron.

## Open Problems

1. **The momentum-space bridge**: loop results live in "surface kinematics" (extra variables X_{i,p} for punctures); getting back to conventional loop momenta for observable predictions is the central open problem
2. **Yang-Mills at higher loops**: 2-loop YM exists, 3-loop and beyond are open
3. **N=4 SYM connection**: the relationship between surfaceology and the amplituhedron is mysterious
4. **Gravity**: double copy provides a route, but direct "gravity surfaceology" doesn't exist yet

## Assessment

Surfaceology is clearly NOT the "final form" — the momentum-space bridge is missing. But it IS the leading framework for colored amplitude theory (2023-2026), solving the canonical YM integrand problem, handling non-planar amplitudes, and now extending to cosmological observables. The rate of progress (~15 papers in 2.5 years) is exceptional. The field is converging toward a unified picture: all amplitude calculations in colored theories = integrals over moduli spaces of surfaces.

## Unexpected Findings

1. **The cosmohedra extension** (arXiv:2412.19881, arXiv:2603.03425): the surfaceology framework is extending beyond scattering amplitudes to *cosmological wavefunctions*. This is much broader than expected — the "universe's amplitude" can apparently also be computed geometrically. The Mar 2026 paper connects cosmohedra to UV divergences in loop amplitudes.

2. **All Loop Scattering As A Sampling Problem** (arXiv:2503.07707): the curve integral can be computed via Monte Carlo tropical importance sampling. This makes the framework not just conceptually elegant but *computationally practical* — 10-loop amplitudes are feasible. This practical advantage was not previously apparent.

3. **Gluon leading singularities = curve covers** (arXiv:2512.17019, Dec 2025): a completely direct connection between on-shell methods (leading singularities) and the surface-geometric objects. This closes an open question about loop-order exponents in the surface formulation and suggests the surface description of YM may be more complete than previously thought.

## Computations Identified

1. **Verify NLSM δ-shift at 5-point**: substitute the shift X_{e,e}→X+δ, X_{o,o}→X-δ into the 5-point Tr(φ³) amplitude (6 terms) and verify it reproduces the 5-point NLSM amplitude (3 terms). A 30-line Python script. Would confirm the basic connection concretely.

2. **Surface integrand vs amplituhedron comparison at 6-point tree**: compute the 6-point MHV gluon amplitude from (a) the BCFW amplituhedron recursion and (b) the surface scaffolding construction. Compare numerically. Would make the relationship between the two frameworks concrete. Moderate difficulty (50-100 lines Python).

3. **1-loop φ³ amplitude in Schwinger representation**: explicitly perform the loop integration in the surface formalism for the simplest 4-point 1-loop case and compare to the standard result. Would demonstrate that the surface formulation produces correctly integrated amplitudes. Requires careful regularization. Moderate difficulty.
