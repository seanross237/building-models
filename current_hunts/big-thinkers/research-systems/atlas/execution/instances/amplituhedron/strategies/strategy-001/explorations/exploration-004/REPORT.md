# Exploration 004: Emergent Locality and Unitarity from the Amplituhedron

## Goal
Investigate precisely how locality and unitarity emerge from the amplituhedron geometry. Assess whether this emergence has physical consequences — predictions, constraints, or observable signatures beyond assuming L/U as axioms.

**Status: COMPLETE**

---

## Executive Summary

Locality and unitarity emerge from the amplituhedron via a specific geometric mechanism: the canonical form has logarithmic singularities *only* on the boundaries of the amplituhedron, and the boundary structure is determined by positivity conditions that automatically select only physical poles. Unitarity follows from the factorization of boundaries into products of smaller amplituhedra. This has been proved rigorously for all n, L, k in 2020 (unitarity) and the BCFW triangulation was proved in Inventiones Mathematicae in 2025.

The brutal honest assessment: **For N=4 SYM, the amplituhedron is primarily a computational and conceptual reformulation. All observational predictions are identical to Feynman diagram calculations.** However, the *conceptual* framework has spawned three genuinely new physical insights: (1) UV finiteness as a selection principle for positive geometry, (2) EFT-hedron positivity bounds on real-world Wilson coefficients, and (3) hidden zeros revealing unexpected relations between non-supersymmetric theories (pions, gluons, phi³). A March 2025 paper further extends "emergence of locality and unitarity" to one-loop non-supersymmetric theories via hidden zeros.

---

## Part 1: The Mechanism of Emergence

### 1.1 How Locality Is Encoded Geometrically

**The short answer**: Physical poles ↔ codimension-1 boundaries of the amplituhedron.

The amplituhedron A_{n,k,L} is defined as the image of the positive Grassmannian G₊(k,n) under a map Z: G₊(k,n) → G(k, k+4) determined by the external data Z_i ∈ M_{+}(k+4, n). The canonical form Ω_{n,k,L} is the unique differential form with:
- Logarithmic singularities on *all* boundaries of the amplituhedron
- No poles elsewhere

The statement "locality" = "the integrand has poles only at physical propagator singularities" translates geometrically as:

> Physical poles = boundaries where the amplituhedron meets the space of on-shell momentum configurations.

**The key technical point** (from Arkani-Hamed & Trnka 1312.2007, and "Anatomy" 1408.3410): The "extended positivity" condition imposes that all maximal minors AND certain non-minimal minors of the extended matrix are positive. This automatically eliminates non-physical (spurious) boundaries. A codimension-1 surface in momentum-twistor space separates "legal" (physical, local) singularities from "illegal" (non-local, non-physical) ones. The amplituhedron sits entirely on the legal side of this surface. When you compute the canonical form, it can only have poles at boundaries — all of which are physical by construction.

**Concrete example**: In the momentum amplituhedron (Damgaard-Ferro-Lukowski-Parisi, arXiv:1905.04216, JHEP 2019), boundaries were classified explicitly:
- Collinear limits → boundaries where ⟨i i+1⟩ → 0 (adjacent pair going collinear)
- Soft limits → boundaries where particle momentum → 0
- Multiparticle factorization channels → boundaries where P²_{i,i+1,...,j} = 0 (sum of adjacent momenta on-shell)
- No boundaries corresponding to non-adjacent channels or other non-physical singularities

The planarity (cyclic color-ordering) constraint also emerges: non-adjacent channels like P²_{1,3} would require the external data to lie in a *different* positroid cell, incompatible with the cyclic positivity condition of the amplituhedron. This connects the restriction to adjacent channels to the planarity/large-N limit, which is itself an emergent property from the geometry (1312.2007, Section 7).

**Landau singularities** (Arkani-Hamed, Langer, Yelleshpur Srikant, Trnka, arXiv:1612.02708, JHEP 2017): The amplituhedron approach systematically identifies where Landau singularities (branch points from loop integrals) occur. For double-pentagon two-loop integrals, naive analysis gives O(n⁴) potential singularities; positivity constraints reduce this to O(n³). This is a concrete example where the geometric framework gives a structural understanding of the singularity content that standard Feynman methods make laborious.

### 1.2 How Unitarity Is Encoded Geometrically

**The main result** (Arkani-Hamed & Trnka, arXiv:1906.10700, JHEP 01(2020)069): *Proof of perturbative unitarity for planar N=4 SYM following from the geometry of the amplituhedron, valid for arbitrary n, L, k.*

The geometric encoding works as follows:

The optical theorem states: Im(A_{n,k,L}) = Σ_{cuts} ∫ A_L × A_R (product of lower amplitudes over phase space)

In the amplituhedron, this becomes:
- **Discontinuity across a branch cut** = residue of the canonical form on a specific codimension-1 boundary
- **The optical theorem** = factorization statement: this boundary decomposes as a product of "left amplituhedron" × "right amplituhedron"
- The "left" and "right" amplituhedra are precisely the geometric objects corresponding to the lower-loop amplitudes appearing on each side of the unitarity cut

For MHV amplitudes (k=0), the proof is explicit and complete. For higher-MHV sectors, left/right amplituhedra for NkMHV external data must be defined, which the authors do and prove the factorization.

**The geometric fact underlying unitarity**: When external data is restricted to a codimension-1 boundary of the amplituhedron (loop momentum put on-shell), the geometry factorizes into two independent positive regions — one for each side of the cut. This factorization is not assumed; it follows from the positivity conditions.

**ABJM extension** (arXiv:2303.03035, JHEP 2023): The same emergent unitarity was proved for ABJM theory's amplituhedron at all loops, four points. Additionally, vanishing of cuts involving odd-point amplitudes follows from the "bipartite" nature of the ABJM geometry — not assumed, but forced by geometry.

### 1.3 The Binary Code Perspective (Arkani-Hamed, Thomas, Trnka, arXiv:1704.05069, JHEP 2018)

A complementary and arguably the cleanest formulation: The amplituhedron is defined entirely combinatorially via **sign flips**.

For tree-level: the amplituhedron A_{n,k} is the region of momentum-twistor space where, for any reference direction, projections of the external data undergo exactly 2k sign flips as you traverse the cyclic order. The maximal winding / sign-flip count uniquely characterizes the physical region.

**Locality as consequence**: A non-physical (spurious) pole corresponds to a zero of the canonical form in a sign-flip direction that doesn't correspond to a face of this maximal-sign-flip region. These are automatically absent because they would reduce the sign-flip count below 2k.

**Unitarity as consequence**: The boundaries (faces of the sign-flip region) automatically have a product structure — one sign-flip region for the left part, another for the right — because sign flips add independently for independent sectors.

The authors state explicitly: "The locality and unitarity of scattering amplitudes are easily derived as elementary consequences of this binary code."

---

## Part 2: Beyond Locality and Unitarity

### 2.1 Deformations of the Amplituhedron: Non-Local Objects

**What happens when you relax positivity?**

If you replace G₊(k,n) with G(k,n) (dropping the positivity requirement on the C-matrix), the canonical form gains poles at locations that are not physical propagator singularities. These correspond to configurations where minors change sign — they are geometrically "inside" the original amplituhedron but become boundaries of the expanded region.

From "Anatomy of the Amplituhedron" (1408.3410): A configuration that violates positivity because "only negative terms survive" in the minor's expansion corresponds to a location that would be a boundary of the relaxed region but NOT of the physical amplituhedron. The canonical form of the relaxed region picks up these as poles — non-local singularities.

**Result**: Yes, you can mathematically define objects by relaxing positivity that have non-local singularities, are well-defined differentiable forms, but do NOT correspond to physical amplitudes. The positivity condition is precisely what screens out non-local singularities.

The "deformed amplituhedron" (Section 10 of 1408.3410) is a geometrically modified version with "outstandingly simple topological properties," used to study the geometry, but it does not compute physical amplitudes.

**The codimension-1 surface** (arXiv:1412.8478): The amplituhedron sits inside a larger space, and there is a codimension-1 surface separating "legal" local singularities (in the amplituhedron interior) from "illegal" non-local singularities (outside). The positivity condition = the requirement to be on the legal side of this surface.

### 2.2 Spurious Poles and Their Cancellation

**The problem**: The BCFW decomposition breaks the amplituhedron into cells (BCFW cells). Each cell has poles at ALL its boundaries — both the outer boundary of the amplituhedron (physical) and the shared boundaries between adjacent cells (spurious, non-physical).

**The geometric resolution**:
- Physical poles = boundaries of the FULL amplituhedron = outer boundaries of the triangulation
- Spurious poles = internal boundaries shared between adjacent BCFW cells
- When two adjacent BCFW cells share a boundary, their contributions to that boundary appear with opposite signs in the sum over cells (due to orientation)
- Therefore, spurious poles cancel identically in the sum

From the amplituhedron perspective, this is obvious from topology: if a boundary is internal to the triangulation, adjacent cells induce opposite orientations on it, so contributions cancel. If it's a boundary of the full amplituhedron, all cells agree on the orientation, so contributions add.

**The 2025 proof** (Even-Zohar, Lakrec, Tessler, arXiv:2112.02703, Inventiones Mathematicae 239 (2025) 1009-1138): The BCFW conjecture — that the BCFW recursion gives exactly a triangulation of the amplituhedron — was formally proved. This rigorously establishes:
1. BCFW cells map injectively into the amplituhedron
2. BCFW cells tile the amplituhedron without gaps (surjectivity proven via topological argument)
3. The interior of the amplituhedron is homeomorphic to an open ball

This proof formally completes the program of proving spurious pole cancellation from geometry. It took 12 years from the original 2013 paper to achieve this proof.

### 2.3 Non-Adjacent Channels and Planarity

**Why only adjacent factorization channels appear**:

In the amplituhedron, the cyclic structure is built into the positivity conditions: external data Z_i ∈ M_{+}(k+4, n) means all ordered minors are positive. This cyclically ordered data can only factorize on channels connecting adjacent particles (maintaining the cyclic order).

A non-adjacent channel like P²_{1,3} = (p₁ + p₃)² = 0 would require the momentum configuration to satisfy conditions incompatible with the cyclic positivity of the external data. Specifically, it would require certain minors involving particle 1, 2, 3 to have a zero while maintaining positivity of all cyclic minors — but inspection shows this forces a spurious configuration.

**Key statement from 1312.2007**: "Planarity" (the restriction to planar / color-ordered amplitudes) is itself a *derived* property from the amplituhedron, not an input assumption. It follows from the cyclic structure of positive external data.

**Is this consequence of planarity or something deeper?** Both. The cyclic positivity (amplituhedron's definition) implies planarity implies adjacent-only channels. The three are equivalent for the amplituhedron. The "deeper" level is positivity; planarity is a consequence.

---

## Part 3: Physical Consequences

### 3.1 UV Completions and the Selection Principle

**The key physical insight from Exploration 003**: The amplituhedron (loop-level positive geometry with canonical form) requires the theory to be UV-finite. UV divergences would appear as poles of the canonical form at "UV boundaries" (loop momentum → ∞), but the amplituhedron has no such boundaries — it is a bounded region in projective space (momentum-twistor space is projective).

This is a **genuine physical consequence**: any theory admitting a full amplituhedron formulation (all-loop positive geometry with no additional regularization) must be UV-finite. This selects exactly:
- Planar N=4 SYM (exactly finite at all loops)
- ABJM (3D, also exactly finite)

For N < 4 SYM, QCD, or gravity, UV divergences generate logarithmic poles that don't fit the boundary structure of a simple positive geometry. This explains WHY the amplituhedron is restricted to these theories — it's not an arbitrary limitation, it's a physical selection principle encoded in the geometry.

**Connection to UV completions**: Arkani-Hamed's long-running program (Adams, Arkani-Hamed, Dubovsky, Nicolis, Rattazzi, 2006 — "Causality, analyticity and an IR obstruction to UV completion") showed that requiring forward-scattering positivity (causality + unitarity) places constraints on which low-energy EFTs admit UV completions. The EFT-hedron (Arkani-Hamed, T.-C. Huang, Y.-T. Huang, JHEP 2021) formalized this as positive geometry: the space of UV-completable EFT Wilson coefficients forms a "totally positive" geometric object.

**EFT-hedron constraints** (2021):
- The EFT-hedron gives infinitely many linear and nonlinear inequalities on EFT operator coefficients
- These apply to real-world theories including Standard Model EFTs
- Specific result: amplitude growth faster than E^6 in some regime → CANNOT be UV-completed
- Constraints on photon-photon and graviton-graviton scattering amplitudes (specific bounds on derivative expansion coefficients)
- An upper bound on the mass of the next lightest state in any UV-completable EFT

This is the most concrete **real-world physical consequence** of the positive geometry / amplituhedron program. These bounds are:
- Derived from geometry (causality + unitarity = positive geometry)
- Apply to real theories (QED, gravity EFT)
- Constrain which UV completions are possible
- Cannot be derived from standard QFT without the positivity framework

### 3.2 Connection to Holography and Emergent Spacetime

**What's true**: The amplituhedron lives in momentum-twistor space, a 4-dimensional projective space PT* that is dual to the original twistor space PT. This is NOT the same as the AdS bulk space in AdS/CFT.

N=4 SYM is the boundary CFT in the AdS₅/CFT₄ correspondence. The amplituhedron computes scattering amplitudes of this boundary CFT. So the amplituhedron is, in a sense, entirely on the boundary side of AdS/CFT — it doesn't probe the AdS bulk.

Arkani-Hamed's suggestion: momentum-twistor space might represent "a different sort of holographic dual than the AdS/CFT one" (private communications and talks), but no concrete proposal has been published establishing an amplituhedron-as-holographic-dual relationship.

**The honest statement**: The amplituhedron is in 3+4k dimensional space (external data space × loop momenta), not AdS₅. Any holographic interpretation would require significantly more development.

**What IS interesting about emergent spacetime**: The amplituhedron makes no reference to:
- Position space (no x^μ)
- Local fields (no Lagrangian density L(x))
- Propagation through spacetime (no Green's functions)

The object lives entirely in momentum-twistor space, which is a non-local space (a single point in momentum-twistor space corresponds to a null line in position space). In this sense, the amplituhedron is "outside of spacetime" — it describes scattering without reference to spacetime propagation. Locality and spacetime then emerge when you extract the amplitude (it has poles at physical propagator locations, consistent with spacetime propagation) even though spacetime was never input.

This is a genuine conceptual result, but its physical import beyond N=4 SYM is unproven.

### 3.3 Predictions for Non-Locality / Planck Scale

**Direct predictions from the amplituhedron itself**: None. The amplituhedron computes N=4 SYM amplitudes in flat space; it makes no predictions about Planck-scale physics, modified dispersion relations, or noncommutative geometry.

**Negative geometry and strong coupling** (arXiv:2112.06956, JHEP 2022): The "nonperturbative negative geometries" paper attempts to extend the geometric approach beyond perturbation theory. It reproduces the known BDS/BDS-like ansatz for IR divergences of N=4 SYM amplitudes from a geometric calculation. This is an interesting consistency check showing the geometric framework is self-consistent at strong coupling, but it reproduces known results rather than predicting new ones.

**The 2025 extension to non-supersymmetric theories**: The "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop" paper (arXiv:2503.03805, March 2025) shows that in Tr(φ³) theory, NLSM, and Yang-Mills theory (none supersymmetric), locality and unitarity at one-loop follow from hidden zeros. Specifically: the one-loop integrand in Tr(φ³) can be fixed from a generic non-local, non-unitary ansatz by imposing hidden zeros. This is a new result — it shows the geometric principle extends beyond N=4 SYM.

### 3.4 Comparison to Other Emergent Locality Programs

| Program | Mechanism | Scale | New Predictions? | Testable? |
|---------|-----------|-------|-------------------|-----------|
| Amplituhedron (N=4 SYM) | Positivity → no non-physical poles | No scale (planar limit) | No (same as Feynman for N=4 SYM) | No |
| EFT-hedron | Causality+unitarity → positivity bounds | Below UV cutoff | Yes (Wilson coefficient bounds) | In principle |
| Hidden zeros (2024) | Geometric vanishing = UV scaling | Tree-level | Yes (inter-theory relations) | Formal |
| String theory UV softness | Regge trajectory, string oscillators | E ~ 1/√α' (string scale) | Yes (string tower) | At Planck-adjacent scales |
| Noncommutative geometry | [x^μ, x^ν] = iθ^μν | E ~ 1/√θ | Yes (modified cross sections) | If θ accessible |
| Causal sets | Discrete Planck-scale spacetime | Planck scale | Yes (stochastic fluctuations) | Very hard |

**Key distinctions**:

1. **String theory**: UV softness is dynamical — the string propagator goes as exp(-α's) at large s. This provides a concrete UV completion with specific new particles (string excitations). Unlike the amplituhedron, string theory's locality emergence is at a physical scale and is testable in principle at string-scale energies. String amplitudes also have "emergent locality" in a similar sense: the string worldsheet theory (a 2D CFT) doesn't assume target-space locality, which emerges from the massless sector.

2. **Noncommutative geometry**: A concrete deformation of spacetime structure that modifies cross-sections at E ~ 1/√θ. Unlike the amplituhedron, NCG makes specific, falsifiable predictions for scattering experiments if θ is accessible. NCG is a physical modification; the amplituhedron is a reformulation.

3. **Causal sets**: Spacetime is fundamentally discrete at the Planck scale, with Lorentz-invariant discreteness. Makes predictions for stochastic fluctuations in particle masses and modified propagation. These are in-principle testable but extremely small. The causal-set approach CHANGES the physical content (introduces discreteness); the amplituhedron does not change N=4 SYM physics.

**The critical difference**: String theory, NCG, and causal sets all modify physics at some scale. The amplituhedron (for N=4 SYM) does NOT modify any observable prediction — it reformulates the same physics in a different framework. The emergent locality is a conceptual/mathematical fact, not an empirical one.

---

## Part 4: Novel Insight Assessment

### 4.1 The Central Question: New Physics or Reformulation?

**BRUTALLY HONEST ASSESSMENT:**

For N=4 SYM specifically, the amplituhedron is a computational and conceptual reformulation that produces identical predictions to Feynman diagrams. There is no experiment that could distinguish "locality is fundamental" from "locality emerges from positivity" within N=4 SYM, because both approaches compute the same amplitudes. Luboš Motl states the direct expert position: "the observable results are finally the same." Multiple physics experts (PhysicsOverflow discussion) confirm: no experimental prediction distinguishes the approaches.

However, dismissing it as "just reformulation" misses three genuine physical contributions:

**Genuine Contribution 1: UV Finiteness as Selection Principle** [ESTABLISHED]
The amplituhedron works for N=4 SYM and ABJM, and only these theories among N≤4 SYM. This isn't accidental — positive geometry *requires* the loop integrals to have no UV poles (which would be unbounded boundaries of the geometric region). This is a physical insight: the class of theories admitting a positive geometry formulation is *smaller* than the class of unitary, local theories. The geometry reveals a deeper reason why certain theories are UV-finite.

**Genuine Contribution 2: EFT-Hedron Real-World Constraints** [ESTABLISHED, PRACTICAL]
The EFT-hedron (2021) translates the positive geometry philosophy into concrete inequalities on real-world Wilson coefficients. These constrain which EFTs can be UV-completed, give specific bounds on photon-photon and graviton scattering, and provide an upper bound on the mass scale of new physics. This is directly physically relevant. The bounds come from a causality+unitarity geometry that is a direct descendent of the amplituhedron program.

**Genuine Contribution 3: Hidden Zeros — Inter-Theory Predictions** [NEW, 2024-2025]
The discovery (2024) that phi³, pion, and gluon amplitudes share identical structure (related by a kinematic shift) and share "hidden zeros" (vanishing at specific kinematics) was genuinely new. These zeros:
- Were not predicted by Lagrangian methods
- Have a geometric origin (ABHY associahedron collapses to lower dimension)
- Reveal unexpected unity across theories
- At one-loop (2025), encode all of locality and unitarity for Tr(φ³) theory

This is the most promising direction for the program yielding genuinely new physics: the positive geometry framework reveals inter-theory relations and constraints not visible from any single Lagrangian perspective.

**What remains REFORMULATION:**
- The statement "locality and unitarity are not fundamental" for N=4 SYM: mathematically true, physically empty for observable predictions
- The specific amplituhedron form computation: same as BCFW/Feynman sum
- The unitarity proof: confirms existing knowledge, doesn't predict new physics

**What remains SPECULATIVE:**
- That the emergent locality of the amplituhedron implies locality is non-fundamental in the real world: no evidence
- That gravity will have an analogous "gravituhedron": stalled for 5 years (see Exploration 003)
- That Planck-scale physics will reveal non-locality related to the amplituhedron's structure: no mechanism

---

## Assessment Table

| Claim | Evidence For | Evidence Against | Status |
|-------|-------------|-----------------|--------|
| Physical poles in amplituhedron come only from boundaries | Proven: canonical form has log singularities only on boundaries; anatomy paper shows legal/illegal surface | — | **ESTABLISHED** |
| Unitarity (optical theorem) follows from boundary factorization | Proved for all n, L, k (JHEP 2020); ABJM all-loop (JHEP 2023) | Requires defining L/R amplituhedra for higher k | **ESTABLISHED** |
| Spurious poles cancel geometrically in BCFW | Proved in Inventiones 2025 (BCFW cells tile amplituhedron exactly) | Took 12 years to prove — suggests non-trivial | **ESTABLISHED** (since 2025) |
| Relaxing positivity gives non-local singularities | Anatomy paper (1408.3410); codimension-1 legal/illegal surface | No explicit construction of a physical non-local amplitude | **SUPPORTED** |
| UV finiteness is geometrically enforced | Only N=4 SYM / ABJM admit full loop amplituhedron | No proof that UV-finite always → positive geometry | **SUPPORTED** |
| Amplituhedron gives new physical predictions for N=4 SYM | — | All predictions identical to Feynman diagrams; multiple experts confirm | **REFUTED** |
| EFT-hedron gives new real-world constraints | Bounds on Wilson coefficients, photon/graviton EFT; derives upper bound on new physics mass | Not as sharp as claimed in some limits | **ESTABLISHED** |
| Hidden zeros predict new inter-theory relations | 2024 JHEP: phi³, pions, gluons share zeros + structure | Applies to colored scalars, pions, YM — not to full SM | **ESTABLISHED** (limited scope) |
| Emergence of L/U from geometry extends beyond N=4 SYM | arXiv:2503.03805 (March 2025): Tr(φ³) 1-loop integrands fixed by hidden zeros | Only one-loop, and Tr(φ³) is special (scalar) | **SUPPORTED** (early evidence) |
| Amplituhedron connects to holography / emergent spacetime | Lives in momentum-twistor space, outside spacetime | No concrete holographic dual established | **SPECULATIVE** |
| Planck-scale non-locality predicted by amplituhedron | — | No mechanism connecting amplituhedron to Planck scale | **REFUTED** |
| Gravity will have a gravituhedron | G-invariants for NMHV gravity (Trnka 2020) | No full geometric object in 5 years; obstacles seem fundamental | **SPECULATIVE** |
| Positive geometry selects UV-complete theories | EFT-hedron; Adams-Arkani-Hamed causality paper (2006) | Not a complete characterization; only scalar positivity | **SUPPORTED** |

---

## Part 5: Detailed Mechanism — How the Signs Work

To be concrete about the locality mechanism, consider the 4-point case (n=4, k=2, L=0):

The amplituhedron A_{4,2,0} is the set of points Y ∈ G(2,6) such that
- ⟨Y Z_1 Z_2⟩ > 0
- ⟨Y Z_2 Z_3⟩ > 0
- ⟨Y Z_3 Z_4⟩ > 0
- ⟨Y Z_4 Z_1⟩ > 0

(All 4 cyclic "bracket" conditions positive.)

The canonical form is Ω = ⟨Yd²Y⟩ / (⟨YZ₁Z₂⟩⟨YZ₂Z₃⟩⟨YZ₃Z₄⟩⟨YZ₄Z₁⟩)

Poles occur at:
- ⟨YZ₁Z₂⟩ = 0: momentum P₁₂ on-shell → physical s₁₂ channel (LOCALITY: adjacent)
- ⟨YZ₂Z₃⟩ = 0: momentum P₂₃ on-shell → physical s₂₃ channel (LOCALITY: adjacent)
- Similarly for ⟨YZ₃Z₄⟩, ⟨YZ₄Z₁⟩

Note: ⟨YZ₁Z₃⟩ = 0 would be a non-adjacent channel — but this never appears as a factor in the canonical form. It's not a boundary of A_{4,2,0} because the cyclic positivity conditions prevent it.

Residues at these poles:
- At ⟨YZ₁Z₂⟩ = 0: the residue factorizes as (3-point)× (3-point) → UNITARITY

This concrete calculation shows both locality and unitarity emerging from the positivity conditions, not assumed.

---

## Part 6: The 2025 Developments

Two key 2025 results are worth highlighting:

**1. BCFW Triangulation Proof** (Inventiones 2025):
The conjecture that BCFW recursion gives a triangulation of the amplituhedron was proved rigorously by Even-Zohar, Lakrec, Tessler. This uses:
- Chord diagrams and domino matrices to classify BCFW cells
- Topological argument for surjectivity (the amplituhedron is homeomorphic to an open ball)
- Injectivity proved from combinatorics

Physical implication: This formally proves that all spurious poles cancel exactly, completing a gap that had existed since 2013.

**2. Emergence of Locality and Unitarity from Hidden Zeros (1-loop, non-SUSY)** (arXiv:2503.03805, March 2025):
Shows that in non-supersymmetric Tr(φ³) theory:
- Hidden zeros (kinematic loci where amplitudes vanish) at tree-level extend to one-loop
- The one-loop integrand can be fixed from a non-local, non-unitary starting ansatz by imposing only the hidden-zero conditions
- Locality and unitarity emerge as consequences

This is the strongest evidence to date that the emergence program extends beyond N=4 SYM and may be a feature of any theory with a "positive geometry" structure.

---

## Synthesis and Conclusions

### What the Amplituhedron Actually Shows About Locality and Unitarity

1. **The mechanism is precise**: Locality = boundaries of the amplituhedron are exactly the physical singularities (no more, no less). Unitarity = these boundaries factorize as products of smaller amplituhedra. Both follow from positivity conditions on the external/loop data.

2. **The cancellation mechanism is clean**: Spurious poles cancel because they are internal to the BCFW triangulation. This has been rigorously proved (2025).

3. **Non-adjacent channels don't appear** because cyclic positivity = planarity = adjacent-only channels. These three are equivalent, all following from the definition.

### What This Means Physically

**Within N=4 SYM**: Reformulation only. Identical predictions to Feynman diagrams.

**Beyond N=4 SYM**:
- EFT-hedron: real constraints on real Wilson coefficients [PHYSICAL CONSEQUENCE]
- Hidden zeros: reveals unexpected inter-theory structure [PHYSICAL CONSEQUENCE]
- 2025 non-SUSY extension: suggests locality/unitarity emerge from positivity in broader class [EARLY EVIDENCE]
- UV selection principle: positive geometry selects UV-finite theories [PHYSICAL INSIGHT]

### The Most Honest Summary

The amplituhedron shows that if you assume positivity (a geometric property of the external kinematic data), you get locality and unitarity for free. This is mathematically beautiful and conceptually significant. But for any single theory, it doesn't change a single observable prediction.

The physical value lies in:
1. Understanding WHY locality and unitarity hold (they're consequences of positivity, not independent axioms)
2. Understanding WHAT restricts UV behavior (positive geometry + UV finiteness are connected)
3. Understanding HOW different theories are related (hidden zeros, inter-theory structure)
4. Constraining real-world EFTs through the EFT-hedron

Whether this rises to "new physics" depends on whether "understanding why" counts as physics. The discovery of hidden zeros and the EFT-hedron bounds suggest the program does produce genuinely new results — they were not known before and wouldn't have been found without the geometric perspective. But the core claim that "locality is not fundamental" is, in a strict sense, a statement about the logical structure of a specific theory, not about nature.

---

## Key References

1. Arkani-Hamed, Trnka, "The Amplituhedron," arXiv:1312.2007, JHEP 10(2014)030
2. Arkani-Hamed, Trnka, "Into the Amplituhedron," arXiv:1312.7878, JHEP 11(2014)182
3. Arkani-Hamed, Trnka, "Positive Amplitudes in the Amplituhedron," arXiv:1412.8478, JHEP 08(2015)030
4. Arkani-Hamed, Hodges, Trnka, "Anatomy of the Amplituhedron," arXiv:1408.3410, JHEP 03(2015)128
5. Arkani-Hamed, Thomas, Trnka, "Unwinding the Amplituhedron in Binary," arXiv:1704.05069, JHEP 01(2018)016
6. Arkani-Hamed, Trnka, "Emergent Unitarity from the Amplituhedron," arXiv:1906.10700, JHEP 01(2020)069
7. Arkani-Hamed, T.-C. Huang, Y.-T. Huang, "The EFT-Hedron," arXiv:2012.15849, JHEP 05(2021)259
8. Damgaard, Ferro, Lukowski, Parisi, "The Momentum Amplituhedron," arXiv:1905.04216, JHEP 08(2019)042
9. Ferro, Lukowski, et al., "From Momentum Amplituhedron Boundaries to Amplitude Singularities," JHEP 07(2020)201
10. Arkani-Hamed, Langer, Yelleshpur Srikant, Trnka, "Landau Singularities from the Amplituhedron," arXiv:1612.02708, JHEP 06(2017)152
11. Arkani-Hamed et al., "Deep Into the Amplituhedron," arXiv:1901.xxxxx, PRL 122(2019)051601
12. Even-Zohar, Lakrec, Tessler, "The Amplituhedron BCFW Triangulation," arXiv:2112.02703, Inventiones Math. 239(2025)1009–1138
13. Huang, Shi, Zhang, "Emergent Unitarity, All-Loop Cuts and Integrations from the ABJM Amplituhedron," arXiv:2303.03035, JHEP 07(2023)212
14. Arkani-Hamed et al., "Hidden Zeros for Particle/String Amplitudes and the Unity of Colored Scalars, Pions and Gluons," arXiv:2312.16282, JHEP 10(2024)231
15. [Authors], "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop Order," arXiv:2503.03805 (March 2025)
16. Adams, Arkani-Hamed, Dubovsky, Nicolis, Rattazzi, "Causality, analyticity and an IR obstruction to UV completion," JHEP 10(2006)014
