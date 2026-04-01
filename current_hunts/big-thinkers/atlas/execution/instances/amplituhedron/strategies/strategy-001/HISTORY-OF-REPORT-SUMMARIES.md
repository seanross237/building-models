# Exploration History

## Exploration 001: 4-Point Tree-Level MHV Amplitude — Three-Way Computation

**Goal:** Implement spinor-helicity formalism and compute the 4-point tree-level MHV amplitude A₄(1⁻,2⁻,3⁺,4⁺) in N=4 SYM via three independent methods (Parke-Taylor, BCFW recursion, Grassmannian), verify numerical agreement, and characterize computational cost.

**Outcome: SUCCESS**

All three methods implemented in working Python code (628 lines), tested, and verified to agree to machine precision (< 10⁻¹⁵ relative error) across 10 independent kinematic configurations.

**Verification Scorecard:** 8 [COMPUTED], 2 [VERIFIED], 0 [CONJECTURED]

**Key Takeaway:** The Grassmannian computation reveals a non-trivial algebraic identity: the amplitude expressed as 1/(M₁M₂M₃M₄) in square-bracket variables equals the Parke-Taylor formula in angle-bracket variables. This "angle-square duality" is invisible from either the Parke-Taylor or BCFW perspective alone — it emerges from the Grassmannian geometry. Already suggestive that the amplituhedron encodes structural information beyond conventional methods.

**Timing benchmark (5000 evals):** Parke-Taylor 5.6 μs, BCFW 231 μs (41x slower), Grassmannian 62 μs (11x slower). At 4-point all reduce to single term — real divergence appears at higher multiplicity.

**Unexpected findings:** (1) Grassmannian "raw" result matches Parke-Taylor EXACTLY without Jacobian factor — the contour integral formulation absorbs it. (2) BCFW for color-ordered amplitudes has only 1 diagram (not 2) for n=4 because non-adjacent channel doesn't respect cyclic ordering.

**Computations identified:** (1) 6-point NMHV via k=3 Grassmannian, (2) 1-loop amplituhedron, (3) Positivity check on C-matrix, (4) Symbolic computation for formal angle-square identity verification.

## Exploration 002: 6-Point NMHV Tree Amplitude — BCFW vs Grassmannian

**Goal:** Compute A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) via BCFW recursion and Grassmannian G(3,6) residues, compare term-by-term structure.

**Outcome: PARTIAL SUCCESS / INCONCLUSIVE**

What worked:
- Kinematics verified to 10⁻¹⁶ [VERIFIED]
- MHV baseline: all 15 Parke-Taylor amplitudes at 6 points computed [COMPUTED]
- Channel 3 structural zero for [1,2⟩ shift: λ_K ∝ −λ_{1̂} at the pole → A₅^MHV numerator vanishes [VERIFIED]
- [3,4⟩ shift gives ALL channels zero — surprising, possibly boundary term issue [VERIFIED]

What failed:
- BCFW not verified: [1,2⟩ shift gives −8030−3626i but [2,4⟩ shift gives −543−259i (~93% disagreement). Root cause: cyclic color ordering of sub-amplitudes is ambiguous in set notation.
- Grassmannian not attempted (no verified target to validate against)

**Verification Scorecard:** 2 [VERIFIED], 1 [COMPUTED], 1 [CONJECTURED]

**Key Takeaway:** The cyclic color ordering in sub-amplitudes is the critical unsolved problem. Solution: use the R-invariant (momentum twistor 5-bracket) formula as non-recursive ground truth before attempting BCFW or Grassmannian.

**Computations identified:** (1) Implement momentum twistor R-invariant formula for A₆^NMHV, (2) Fix BCFW with explicit diagram-based cyclic orderings, (3) Grassmannian G(3,6) once BCFW is verified.

## Exploration 003: Positive Geometry Beyond N=4 SYM — Extension Map

**Goal:** Map where positive geometry / amplituhedron extends beyond N=4 SYM and where it breaks. Cover 7+ theory classes.

**Outcome: SUCCESS — Clear two-tier structure identified.**

**Key Finding:** Positive geometry has a TWO-TIER structure:
- **Tier 1 (Full amplituhedron, all-loop):** ONLY N=4 SYM and ABJM. Requires Yangian symmetry + planarity + UV finiteness.
- **Tier 2 (Partial — scattering forms, tree-level):** Broad — bi-adjoint scalars (associahedron), ϕ⁴ (Stokes polytopes), YM tree-level (corolla polynomial), cosmological polytopes, strings (associahedral grid).
- **Complete failures:** N<4 SYM at loops (UV poles deform measure), color-full QCD, non-planar loops, de Sitter gravity.

**The essential wall is UV finiteness:** UV divergences produce poles that are NOT logarithmic singularities on geometric boundaries, breaking the canonical form interpretation.

**Cases where geometry exceeds standard methods:**
1. Color-kinematics duality EXPLAINED geometrically (wedge products satisfy Jacobi)
2. ϕ⁴ diagram weights determined by geometry (Stokes polytopes)
3. ABJM all-loop integrands from single geometric object (unachievable from perturbation theory)
4. S-matrix as boundary of cosmological wavefunction (codimension-1 fact)
5. Inverse KLT kernel gets geometric home (associahedral grid, 2025)

**Key open problems:** Gravituhedron stalled for 5 years (no actual geometric object). Non-planar amplituhedron unknown. Extension to de Sitter unknown.

**Unexpected finding:** ABJM amplituhedron must be IMPORTED from N=4 SYM via reduction, not constructed natively. This suggests the geometry is more specific to N=4 than to maximal SUSY.

## Exploration 004: Emergent Locality and Unitarity from the Amplituhedron

**Goal:** Investigate how locality and unitarity emerge from amplituhedron geometry. Assess whether this is genuinely new physics or just reformulation.

**Outcome: SUCCESS — Brutally honest assessment with concrete mechanism and three genuine physical contributions identified.**

**Mechanism:** Locality = canonical form has log poles only on amplituhedron boundaries (positivity screens out non-physical poles via codimension-1 legal/illegal surface). Unitarity = boundaries factorize as products of smaller amplituhedra. Both PROVED: unitarity for all n,L,k (JHEP 2020), BCFW triangulation (Inventiones 2025).

**Brutal assessment:** For N=4 SYM, this is REFORMULATION — identical predictions to Feynman diagrams. No experiment can distinguish "locality is fundamental" from "locality emerges from positivity."

**Three genuine physical contributions:**
1. **EFT-hedron** (2021): Real-world positivity bounds on Wilson coefficients — constrains UV completions of actual EFTs (QED, gravity). Most concrete physical consequence.
2. **Hidden zeros** (2024): phi³, pions, gluons share unexpected structure revealed geometrically — genuine new result not visible from Lagrangian methods.
3. **March 2025 paper** (arXiv:2503.03805): Locality + unitarity at 1-loop from hidden zeros in non-SUSY Tr(phi³). Strongest evidence emergence extends beyond N=4 SYM.

**Key finding for mission:** UV finiteness is not accidental — positive geometry REQUIRES it. This is a genuine physical insight (selection principle), not just computational efficiency. The geometry selects UV-finite theories.

**Leads identified:** (1) arXiv:2503.03805 deserves deep dive — may be beginning of generalizing emergence beyond N=4 SYM; (2) EFT-hedron bounds could be computationally verified; (3) ABJM odd-point vanishing from geometry is non-trivial prediction.

## Exploration 005: Hidden Zeros — The Frontier of Positive Geometry Beyond N=4 SYM

**Goal:** Deep dive into hidden zeros program: what they are, March 2025 paper, scope and limitations.

**Outcome: SUCCESS — Clear technical account with 15+ papers surveyed.**

**What are hidden zeros?** In Tr(phi³), pick any "causal diamond" in the kinematic mesh and set all non-planar Mandelstam invariants inside to zero — the amplitude vanishes. This is invisible from Feynman diagrams but obvious from ABHY associahedron geometry.

**Key results by strength:**
1. PROVED (tree): Zeros exist and uniquely determine Tr(phi³) amplitudes (equiv. to enhanced UV scaling). Three theories (phi³, pions, gluons) unified by unique kinematic shift δ.
2. PROVED (1-loop, assuming locality): Unitarity ↔ big mountain zeros (biconditional).
3. CONJECTURED + VERIFIED (4pt): From non-local non-unitary ansatz (~6,500 parameters), zeros uniquely fix the integrand; locality + unitarity emerge.
4. OPEN: 2-loop+, Yang-Mills at 1-loop, standard momentum-space formulation.

**Critical boundary:** Loop results live in "surface kinematics" (Y± variables on punctured disk), NOT standard Feynman loop momenta. Momentum-space translation is explicitly open.

**Unexpected findings:**
1. δ-deformation is UNIQUE — one-parameter family connecting three theories is a structural theorem
2. Factorization near zeros is NOT standard pole factorization — new algebraic structure
3. Loop zeros decompose to tree-level objects (loop integrand near zero → tree amplitude)
4. Extends to cosmological wavefunctions (arXiv:2503.23579)
5. 20+ follow-up papers in 2 years — genuinely active frontier
6. Jan 2026: zeros survive massive deformations ONLY with symmetry-protected mass (not universal)

**Hidden zeros vs amplituhedron:** NOT competitors — different theories. Surfaceology is the common parent framework. Amplituhedron = N=4 SYM branch; hidden zeros = non-SUSY branch.

## Exploration 006: EFT-Hedron — Computational Verification of Positivity Bounds

**Goal:** Implement EFT-hedron positivity constraints computationally. Verify forward bounds, Hankel matrix bounds, and photon-photon bounds.

**Outcome: SUCCESS — All computations verified, 4 modular scripts, QED bounds confirmed.**

**Verification Scorecard:** 1 [VERIFIED], 11 [COMPUTED], 2 [CHECKED], 3 [CONJECTURED]

**Key results:**
- Forward limit: g_{n,0} ≥ 0 (n=2..8) confirmed for 3 UV-complete models, correctly violated by ghost resonance
- Hankel matrix: det(H₂) ≈ 0 for single resonance (saturation), det(H₂) > 0 for two resonances (strict inequality). Analytic formula confirmed to machine precision.
- Photon-photon: Euler-Heisenberg QED coefficients satisfy all 4 EFT-hedron conditions. c₂/c₁ = 7/4 exactly reproduced.

**Physical insight (unexpected):** Saturation ratio is non-monotonic vs mass ratio M₂/M₁ — measuring Hankel determinant can locate UV resonance mass ratio from low-energy EFT data alone. This is a potential "spectroscopic tool" — reconstruct UV spectrum from low-energy measurements.

**Proof gaps:** Crossing symmetry not imposed; non-forward bounds not computed; graviton sector conceptual only.

## Exploration 007: Surfaceology — The Unifying Framework

**Goal:** Deep dive into surfaceology (curves on surfaces for scattering amplitudes) — understand framework, unification, new results, string theory connection.

**Outcome: SUCCESS — Clear framework description with 15+ papers, unification map covering 7+ approaches.**

**What is surfaceology?** Amplitudes = integrals over fatgraph surface parameter spaces, with integrands from counting curves via 2×2 matrix products. Formula: A = ∫ [d^E t / MCG] exp(−Σ_C α_C(t)·(P_C²+m²)).

**Three key properties:**
1. ALL loops, ALL multiplicities simultaneously
2. Handles non-planar amplitudes (higher-genus surfaces) — unlike amplituhedron
3. Makes hidden zeros, soft theorems, string limits all manifest

**Critical distinction:** Amplituhedron (N=4 SYM, twistor space) and surfaceology (colored non-SUSY theories, kinematic space) are PARALLEL programs. NOT nested. Relationship is the most important open question in the field.

**New results 2024-2026:** Canonical YM loop integrand (PRL 2025, 30-year problem solved), cut equation recursion, superstring connection, gluon leading singularities from curve covers, cosmohedra for cosmological wavefunctions.

**Unexpected:** (1) Monte Carlo sampling makes 10-loop amplitudes feasible computationally, (2) extends to cosmological wavefunctions, (3) gluon leading singularities = curve covers.

**Central open problem:** Loop results live in "surface kinematics" — bridge back to standard momentum-space is missing.

