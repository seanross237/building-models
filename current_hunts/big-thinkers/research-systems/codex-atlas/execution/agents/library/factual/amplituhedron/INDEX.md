# Amplituhedron — Factual Library

Knowledge about scattering amplitudes, the amplituhedron geometric program, spinor-helicity formalism, BCFW recursion, the Grassmannian/positive geometry approach, the full landscape of positive geometry extensions beyond N=4 SYM, and the physical status/consequences of the program. Covers 4-point tree-level MHV (three-method verification), 6-point NMHV (partial), a comprehensive extension map (exploration-003), locality/unitarity emergence + physical assessment (exploration-004), EFT-hedron computational verification (exploration-006), and the full surfaceology program survey (exploration-007). **24 findings (19 here + 5 in surfaceology/ subfolder).**

## Computational Findings (Explorations 001–002)

- **spinor-helicity-conventions-and-validation.md** — Spinor-helicity conventions (metric, brackets, Mandelstam), extraction algorithm, and numerical validation to machine precision across 8 kinematic configurations.

- **grassmannian-g24-square-bracket-identity.md** — G(2,4) Grassmannian integral localizes to a single residue; the resulting minors yield −[34]³/([12][14][23]) = ⟨12⟩³/(⟨23⟩⟨34⟩⟨41⟩) for any massless 4-particle kinematics. Momentum twistors in general position (⟨1234⟩ = 48.0). Verified across 10 kinematic points.

- **bcfw-recursion-sign-detail.md** — [1,2⟩ BCFW shift at 4-point; single pole from ⟨41̂⟩ = 0; critical sign A₄ = −(A_L × A_R / s₁₄) arising from bracket antisymmetry ⟨41⟩ = −⟨14⟩. Verified analytically and numerically.

- **4pt-mhv-method-comparison.md** — All three methods agree to < 10⁻¹⁵ relative error across 10 kinematics. Timing: PT 5.6 μs (baseline), Grassmannian 11× slower, BCFW 41× slower. Conceptual comparison and n-point scaling table.

- **6pt-nmhv-bcfw-structural-zeros.md** — For A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺): under [1,2⟩ shift, channel 3 ({1̂,6,5,4}|{2̂,3}) is structurally zero because λ_K ∝ −λ_{1̂} at the pole (verified numerically). Under [3,4⟩ shift, all three channels vanish for independent structural reasons (SWI, Parke-Taylor numerators). Reduces [1,2⟩ computation to 2 non-trivial channels.

- **6pt-nmhv-bcfw-cyclic-ordering-hazard.md** — Two BCFW implementations ([1,2⟩ and [2,4⟩ shifts) disagree by 93% for A₆^NMHV. Diagnosed cause: cyclic color ordering of sub-amplitudes and helicity assignment of internal particle K. Complexity comparison table (4pt MHV vs 6pt NMHV). Path to resolution: implement R-invariant / 5-bracket formula as independent ground truth before attempting Grassmannian G(3,6).

## Extension Map Findings (Exploration 003)

- **positive-geometry-prerequisites.md** — Essential features of N=4 SYM that make the amplituhedron possible: Yangian symmetry Y(psu(2,2|4)), planarity (large-N, amplitude/Wilson loop duality), maximal SUSY (UV finiteness, no poles at infinity). Essential vs. convenient distinction. Yangian unique to planar N=4 among 4D gauge theories.

- **n-less-than-4-sym-failure.md** — No positive geometry for N=1/N=2 SYM. Benincasa-Gordo (arXiv:1609.01923) obstacle: UV poles at infinity, deformed Grassmannian measure, helicity loops in on-shell diagrams, bubble ambiguities. Not technical — structural. Dian-Heslop "amplituhedron-like geometries" produce A×Ā (amplitude squares), not amplitudes for N=2.

- **yang-mills-scattering-forms.md** — YM tree-level partial positive geometry via scattering forms (arXiv:1711.09102): color=kinematics in wedge products explains BCJ duality. Corolla polynomial extends to 1-loop planar YM (arXiv:2405.10601). Fundamental loop-level obstruction for the **amplituhedron approach** (UV divergences, no Yangian, no dual conformal). **⚠️ Updated 2025:** Surface kinematics (arXiv:2408.11891, PRL 2025) RESOLVED the canonical loop integrand for non-SUSY YM via a different geometric approach — see surfaceology/ subfolder.

- **scalar-theory-positive-geometries.md** — Most successful extension: bi-adjoint ϕ³ (ABHY associahedron — clean, no SUSY needed), ϕ⁴ (Stokes polytopes), multi-scalar (accordiohedra). Associahedron as universal scaffold. Stringy canonical forms (arXiv:1912.08707) connect ϕ³ geometry to open string Koba-Nielsen integral. Associahedral grid (arXiv:2508.20161, 2025) geometrizes inverse KLT kernel.

- **gravity-amplituhedron-status.md** — No amplituhedron for gravity. Fundamental obstacles: no Yangian, harder BCFW singularities, KLT "squaring" lacks geometric meaning. Trnka's gravituhedron (arXiv:2012.15780): G-invariants defined, NMHV formulas up to 8-pt, but no geometric object after 5+ years. CHY pushforward (arXiv:2206.14196): partial (moduli space, requires scattering equations). N=8 SUGRA: UV-finite but no amplituhedron — UV finiteness necessary but not sufficient.

- **cosmological-polytopes.md** — Genuine working extension to cosmological correlators of scalar FRW wavefunctions. S-matrix appears as higher-codimension face (total energy pole) — geometrically explains flat-space limit. Cosmohedra (JHEP 2025) for Tr(ϕ³). De Sitter / inflation with gravitons: open problem.

- **positive-geometry-tier-structure.md** — Three-tier synthesis: Tier 1 (full amplituhedron: N=4 SYM + ABJM), Tier 2 (scattering forms: scalar/YM/gravity tree, cosmological), Tier 3 (structural insights: corolla, zero conditions, deformed measures). Complete failures: color-full QCD, non-planar loop-level. **UV finiteness wall**: loop-level positive geometry requires UV finiteness; UV finiteness is necessary but not sufficient (also need Yangian). Open problems: gravituhedron, non-planar amplituhedron, de Sitter, ϕ³ loops, non-perturbative.

## Locality/Unitarity Emergence and Physical Assessment (Exploration 004)

- **locality-unitarity-emergence-mechanism.md** — Precise mechanism: canonical form has log singularities only on boundaries (locality = boundaries are exactly physical poles); unitarity = boundary factorization proved all n,L,k (JHEP 2020) + ABJM (2023); binary code / sign-flip perspective (Arkani-Hamed, Thomas, Trnka 2018); concrete 4-pt example showing both; planarity derived not assumed; deformed amplituhedron (relaxed positivity) gains non-local poles; UV finiteness geometrically enforced via bounded region in projective space.

- **bcfw-triangulation-proof-2025.md** — Even-Zohar, Lakrec, Tessler, Inventiones Math. 239(2025)1009-1138; BCFW cells tile amplituhedron exactly (injectivity from chord diagrams/domino matrices; surjectivity via topological argument); amplituhedron homeomorphic to open ball; spurious poles cancel via opposite orientation on internal boundaries; 12-year gap between conjecture (2013) and proof (2025).

- **eft-hedron-positivity-constraints.md** — Arkani-Hamed, T.-C. Huang, Y.-T. Huang, JHEP 2021; positive geometry for real-world EFT Wilson coefficients; amplitude growth > E^6 → not UV-completable; bounds on photon-photon and graviton EFT operators; upper bound on new physics mass; most practically relevant output of the amplituhedron program; applies to real theories (QED, gravitational EFT).

- **hidden-zeros-inter-theory-structure.md** — arXiv:2312.16282, JHEP 2024: ϕ³/pions/gluons share hidden zeros (vanishing at specific kinematics) + kinematic-shift structure; ABHY associahedron collapses at zero kinematics; **2025 extension** (arXiv:2503.03805): one-loop Tr(φ³) integrand uniquely fixed by hidden zeros, locality/unitarity emerge in non-SUSY theory; most promising direction for genuinely new physics.

- **amplituhedron-physical-assessment.md** — Honest status: identical predictions to Feynman diagrams for N=4 SYM (reformulation); 3 genuine contributions (UV finiteness selection, EFT-hedron, hidden zeros); full assessment table (12 claims × Evidence For / Evidence Against / ESTABLISHED/SUPPORTED/SPECULATIVE/REFUTED); comparison table of emergent locality programs (amplituhedron vs. EFT-hedron vs. hidden zeros vs. string theory vs. NCG vs. causal sets).

## Surfaceology Program (Exploration 007)

- **[surfaceology/](surfaceology/INDEX.md)** — The surfaceology program: curves on surfaces as the unifying framework for colored amplitude theory (φ³, NLSM, YM, Yukawa, strings). 5 findings covering the foundational framework, amplituhedron vs. surfaceology distinction (parallel, not nested), the canonical YM loop integrand (PRL 2025, scalar scaffolding), a survey of all new results 2023–2026 (cut equation, Yukawa, string connection, cosmohedra, Monte Carlo 10-loop, inverse KLT), and open problems (central: momentum-space bridge).

## EFT-Hedron Computational Verification (Exploration 006)

- **eft-hedron-computational-verification.md** — Numerical verification of all EFT-hedron positivity bounds: forward limit g_{n,0} ≥ 0 for n=2..8 (3 UV-complete models pass, ghost model fails); Hankel PSD bounds (single resonance saturates det(H_2)≈4.76e-07, two resonances strict det=9.42e-03, analytic formula verified to machine precision 0%); Euler-Heisenberg c₂/c₁ = 1.7500 = 7/4 exactly reproduced; violation correctly triggered for c₁<0. **Novel physical insight**: saturation ratio non-monotonic in M2/M1, minimum ~0.988 at M2/M1≈1.25–1.5 — fingerprint for discriminating single-resonance vs. multi-resonance UV completions.

## Cross-References

- [analyticity-sacrifice.md](../quadratic-gravity-fakeon/analyticity-sacrifice.md) — QG+F sacrifices S-matrix analyticity (no dispersion relations), which is the foundation the EFT-hedron positivity bounds rely on; direct tension between these programs
- [yang-mills-scattering-forms.md → surfaceology/](surfaceology/INDEX.md) already covers YM scattering; for the constructive YM existence problem see [gap-structure-overview.md](../yang-mills/gap-structure-overview.md)
- [gravity-amplituhedron-status.md](gravity-amplituhedron-status.md) discusses the gravituhedron obstacle; for gravity UV completion via quadratic action see [core-idea.md](../quadratic-gravity-fakeon/core-idea.md)
- [scalar-theory-positive-geometries.md](scalar-theory-positive-geometries.md) covers stringy canonical forms connecting to open string integrals; for the full string theory context see [graviton-mechanism.md](../string-theory/graviton-mechanism.md)
