# Exploration 007: Surfaceology — The Unifying Framework

## Goal Summary

Deep dive into the surfaceology program (curves on surfaces for scattering amplitudes). Understand the framework, how it unifies prior approaches (amplituhedron, ABHY associahedron, hidden zeros, momentum amplituhedron), what new predictions it makes, and where the field is heading as of early 2026.

Key papers analyzed:
- arXiv:2309.15913 — "All Loop Scattering As A Counting Problem" (Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas, Sep 2023)
- arXiv:2311.09284 — "All Loop Scattering For All Multiplicity" (same authors, Nov 2023)
- arXiv:2403.04826 — "Circles and Triangles, the NLSM and Tr(Φ³)" (Arkani-Hamed, Figueiredo, Mar 2024)
- arXiv:2406.04411 — "Surfaceology for Colored Yukawa Theory" (De, Pokraka, Skowronek, Spradlin, Volovich, Jun 2024)
- arXiv:2408.11891 — "Surface Kinematics and 'The' Yang-Mills Integrand" (Arkani-Hamed, Cao, Dong, Figueiredo, He, Aug 2024; PRL 2025)
- arXiv:2412.21027 — "The Cut Equation" (Arkani-Hamed, Frost, Salvatori, Dec 2024)
- arXiv:2504.21676 — "Superstring amplitudes meet surfaceology" (Cao, Dong, He, Zhu, Apr 2025; SciPost 2025)
- arXiv:2505.17179 — "Surface Gauge Invariance, Soft Limits and the Transmutation of Gluons into Scalars" (Backus, Figueiredo, May 2025)
- arXiv:2506.05456 — "Cuts and Contours" (Figueiredo, Skowronek, Jun 2025)
- arXiv:2512.17019 — "How gluon leading singularities discover curves on surfaces" (Carrôlo, Figueiredo, Dec 2025)
- arXiv:2602.15102 — "A Surface Integrand for the Inverse KLT Kernel" (Bartsch, Kampf, Novotný, Trnka, Feb 2026)
- arXiv:2503.07707 — "All Loop Scattering As A Sampling Problem" (Salvatori, Mar 2025)

---

## 1. Framework Definition

### 1.1 What Is Surfaceology?

"Surfaceology" is the collective name for a program that reformulates quantum field theory scattering amplitudes as integrals over (or counting problems on) **combinatorial surfaces** — specifically, fatgraphs (ribbon graphs) that encode the topological data of Feynman diagrams. The foundational paper is arXiv:2309.15913, "All Loop Scattering As A Counting Problem," by Nima Arkani-Hamed, Hadleigh Frost, Giulio Salvatori, Pierre-Guy Plamondon, and Hugh Thomas (Sep 2023). The program has since expanded into a large cluster of connected papers (see above).

The central claim is that scattering amplitudes — for colored scalar theories at all loop orders and all multiplicities, and increasingly for Yang-Mills, NLSM, string theory, and fermionic theories — can be expressed as integrals over a natural parameter space associated with surfaces, where the integrand is determined by a remarkably simple counting problem.

### 1.2 The Fundamental Objects

**Fatgraphs (ribbon graphs):** The basic combinatorial object is a *fatgraph* — a graph with a cyclic ordering on the edges at each vertex. A fatgraph with n external lines, E internal edges, and L loops satisfies the relation:

```
E = n + 3(L - 1)
```

A fatgraph itself defines a surface (through its Euler characteristic), with genus g. The amplitude formula integrates over all fatgraphs at a given (n, L, g) order.

**Curves on surfaces:** Each fatgraph has a collection of *curves* — paths on the surface that can be encoded via a 2×2 matrix product over the edges:

```
M(C) = ∏_{turns along C}  M_turn(y_i)
```

where the turn matrices are:
```
M_L(y) = [[1, 0], [y, y]]   (left turn, "peak")
M_R(y) = [[1, 1], [0, y]]   (right turn, "valley")
```

The curve carries momentum:
```
P_C^μ = p_start^μ + ∑_{right turns} p_{from left}^μ
```

**Headlight functions (u-variables):** For each curve C, define:
```
u_C = M(C)₁₂ · M(C)₂₁ / (M(C)₁₁ · M(C)₂₂)    ∈ [0, 1]
```

These satisfy a remarkable constraint: for any curve C and the set of curves D that intersect it:
```
u_C + ∏_D u_D^{n(C,D)} = 1
```
where n(C,D) is the intersection number. This is the equation defining a natural compactification of Teichmüller space (analogous to Fock-Goncharov coordinates).

**The headlight/Schwinger parameter:** The headlight function also defines the Schwinger parameter:
```
α_C = −Trop(u_C) = Trop(M₁₁) + Trop(M₂₂) − Trop(M₁₂) − Trop(M₂₁)
```
where Trop replaces products with sums and sums with min (tropicalization).

### 1.3 The Amplitude Formula

The full amplitude (pre-loop-integration) is:

```
A = ∫ d^D ℓ_1 ··· d^D ℓ_L  ∫ [d^E t / MCG]  exp(−∑_C α_C(t) · (P_C² + m²))
```

After loop integration, using the Schwinger parametrization:
```
A = ∫ [d^E t / MCG]  (π^L / U(α))^{D/2}  exp(F(α)/U(α))
```

where U and F are the standard Symanzik polynomials, but now the Schwinger parameters α_C come directly from the curve structure of the surface.

**The counting/F-polynomial:** The key simplification is that within a given *cone* of the g-vector fan, the Schwinger parameter becomes a linear function of the integration variables:

```
S(t) = ∑_C α_C(t) · X_C = ∑_C t_C · X_C    (linear within a cone)
```

Integrating exp(−S) over the cone gives exactly the standard Feynman propagator formula:
```
∫_{cone} d^E t  e^{−S} = ∏_{i=1}^E  1/(P_{C_i}² + m²)
```

**The First Miracle:** Each cone in the g-vector fan corresponds to exactly one Feynman diagram. So integrating over all cones (= all fatgraphs) gives exactly the sum over all Feynman diagrams — but organized by a single geometric construction.

**The counting problem:** Within a fatgraph, computing the partition function (the sum over all triangulations weighted by variables y_i associated with edges) is equivalent to evaluating a product of 2×2 matrices — a simple counting problem. The F-polynomial:
```
F(C) = ∑_{valid subsets} ∏_i y_i
```
where "valid subsets" follow a "downhill closure" rule (if you pick an edge, include all edges downhill in the mountainscape). This is literally computing the number of ways to cover the graph satisfying certain constraints.

### 1.4 The Non-Planar Extension

The non-planar case is handled in arXiv:2311.09284 ("All Loop Scattering For All Multiplicity"). For genus-g contributions, the edge count becomes:
```
E = n + 3L + 2g
```

Non-planar amplitudes arise from fatgraphs that live on higher-genus surfaces. The main technical issue is that the mapping class group (MCG) of the surface acts on the curve space, creating infinite redundancy. This is handled via the **Mirzakhani kernel** K(t): instead of finding a fundamental domain for the MCG action, one replaces the quotient measure with this kernel, which encodes the symmetry directly in the integrand.

For double-trace 1-loop amplitudes, infinitely many curves that differ only in winding number all contribute, but the Mirzakhani trick sums them to a finite result. The all-multiplicity, all-loop, non-planar formula is explicit through 2-loop order.

### 1.5 Key Mathematical Structures

- **Tropical geometry:** The u-variables, when tropicalized, give the Schwinger parameters. This connects to tropical Grassmannians and tropical amplitudes (Tourkine 2013, arXiv:1309.3551).
- **Cluster algebras:** The u-variable equations u_C + ∏u_D^{n(C,D)} = 1 are the exchange relations of a cluster algebra associated with the surface. The surface itself is the data of a cluster variety.
- **Teichmüller space:** The positive region (all u_C ∈ (0,1)) is a compactification of the decorated Teichmüller space of the surface. This is the Fock-Goncharov construction.
- **Triangulations:** A triangulation of the surface (maximal collection of non-crossing curves) corresponds to a cone in the g-vector fan, and thus to a Feynman diagram.

---

## 2. Unification Map

### 2.1 How Surfaceology Unifies Existing Approaches

| Framework | Theory | Connection to Surfaceology |
|---|---|---|
| **ABHY associahedron** | Bi-adjoint Tr(φ³), tree | Associahedron = surfaceology on disk (g=0, L=0). Triangulations of disk = Feynman diagrams. Amplitude = canonical form of associahedron = sum over triangulations. Surfaceology extends to all loops and genera. |
| **String amplitude (open string)** | All theories (bosonic/super) | u-variables define the string amplitude via exp(−∑ α' X_C u_C). The field theory limit α'→0 gives the QFT amplitude. Surfaceology is "string theory written combinatorially." |
| **Hidden zeros** | Tr(φ³), NLSM, gluons | Big-mountain zeros = special collections of curves whose contributions cancel. The pairwise cancellation structure is manifest in the surface integrand (arXiv:2503.03805). |
| **NLSM amplitudes** | Pions (Goldstone bosons) | NLSM = Tr(φ³) with a δ-shift: X_{e,e} → X_{e,e}+δ, X_{o,o} → X_{o,o}−δ. The "circles and triangles" connection (arXiv:2403.04826) shows this shift emerges from the Catalan generating function. |
| **Yang-Mills (non-SUSY)** | Gluons, all loops | Scalar scaffolding: take 2n-point scalar amplitude, set scaffolding curve variables to zero (residue), to get n-point gluon amplitude. Surface kinematics resolves 1/0 ambiguities. (arXiv:2408.11891) |
| **Amplituhedron** | N=4 SYM | Distinct framework — amplituhedron lives in auxiliary twistor space, not kinematic space. NOT a special case of surfaceology. Instead, surfaceology and amplituhedron are parallel geometric programs covering different theories. |
| **Colored fermions (Yukawa)** | Colored Yukawa | Extended in arXiv:2406.04411: fermionic numerators repackaged as combinatorial determinants. All-loop, all-genus, all-multiplicity formula established. |
| **Superstrings** | Type-I, Heterotic, Type-II | arXiv:2504.21676 shows superstring amplitudes = gauge-invariant combinations of bosonic string amplitudes on surfaces. The curve-integral formalism accommodates them directly. |

### 2.2 ABHY Associahedron in Detail

The ABHY associahedron (arXiv:1711.09102, Arkani-Hamed, Bai, He, Yan) showed that tree-level bi-adjoint scalar amplitudes are the canonical form of the associahedron in kinematic space. The kinematic variables X_{i,j} = (p_i + p_{i+1} + … + p_{j-1})² form the vertices of the associahedron.

In surfaceology, this is exactly the disk (g=0, L=0) case: a triangulation of the n-gon corresponds to a Feynman diagram, and the sum over all triangulations (with Schwinger parametrization) gives the amplitude. The associahedron is the *dual polytope* of the triangulation fan. Surfaceology makes this explicit and extends it to loops.

### 2.3 The Amplituhedron — Not a Special Case

**Critical clarification:** The amplituhedron is NOT embedded as a special case of surfaceology. They are parallel, distinct frameworks:

- **Amplituhedron:** Lives in auxiliary twistor space (momentum twistors). Applies to N=4 SYM with full supersymmetry. The geometry encodes all the non-trivial supersymmetric numerator structure. Proved in Inventiones 2025 (Arkani-Hamed and Trnka).

- **Surfaceology:** Lives in kinematic space (Mandelstam variables X_{i,j}). Applies to non-supersymmetric colored theories (φ³, NLSM, YM, Yukawa, strings). The amplituhedron's supersymmetric numerators are replaced by simpler scalar structure.

The two programs share a philosophy (geometry encodes physics) and key figures (Arkani-Hamed), but address different theories and different kinematic spaces. Surfaceology could be described as the "poor man's amplituhedron" — it gives amplitude integrands for a broader class of theories, but without the full power of the amplituhedron for N=4 SYM.

### 2.4 Hidden Zeros from Surfaces

The connection is established in arXiv:2503.03805 (Backus, Rodina, "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop Order"). A "big mountain zero" — setting all variables X in a causal diamond to zero — forces a large collection of curves to have zero propagator. In the surface integrand, this causes pairwise cancellations between triangulations, making the zero manifest geometrically. The biconditional "unitarity ↔ big mountain zeros" is proved in the surface kinematics language.

### 2.5 NLSM from δ-Shift

arXiv:2403.04826 establishes:
```
A_NLSM = A_{Tr(φ³)} |_{X_{e,e} → X_{e,e}+δ, X_{o,o} → X_{o,o}-δ}
```

This δ-shift has a beautiful geometric explanation: the NLSM field U = Φ + i√(1−Φ²) is the unit circle parametrized by the same function that generates Catalan numbers (counting triangulations). So NLSM amplitudes automatically decompose as sums over triangulations with Catalan-number-weighted numerators.

The "surface-soft limit" is a new construction: rather than rescaling momenta, one geometrically identifies boundary points of the surface polygon. This makes the Adler zero (vanishing of pion amplitudes in the soft limit) manifest at the integrand level — not just the amplitude level.

---

## 3. New Results from Surfaceology (2023-2026)

### 3.1 The "First Miracle": Counting Reproduces All Feynman Diagrams

The key result of arXiv:2309.15913 is that the entire perturbative expansion of colored φ³ theory — at all loop orders and all multiplicities — is encoded in a single combinatorial counting problem on a surface. All Feynman diagrams arise from cones in the g-vector fan. There is no need to enumerate diagrams; one integrates over the full surface space and the diagram structure emerges automatically.

This is the first time a completely non-perturbative-in-topology formula has been given for an entire QFT's perturbative expansion.

### 3.2 The Yang-Mills Integrand (arXiv:2408.11891, PRL 2025)

The long-standing problem of defining a canonical loop integrand for non-supersymmetric Yang-Mills was solved using surface kinematics. The key ideas:

**Scalar scaffolding:** A 2n-point scalar surface amplitude has n-point gluon amplitudes embedded in it via:
```
ℐ_n = Res_{X_Scaff=0} ∫ ∏_P dy_P/y_P²  ∏_C u_C^{α'X_C}
```
Taking residues at scaffolding curve locations (where adjacent scalar pairs fuse into gluons) extracts the gluon integrand.

**Surface gauge invariance:** The gluon integrand satisfies a surface-generalized gauge invariance condition: shifts ε^μ → ε^μ + αp^μ leave the amplitude unchanged through combinations of X-variables.

**Perfect factorization:** Single cuts give well-defined tree amplitudes without 1/0 singularities, because surface kinematics assigns distinct variables X_{i,j} ≠ X_{j,i} even when the curves are homologous.

**Recursion:** The integrand satisfies:
```
ℐ_n^S = ∑_i  Res_{X_{i,p}=0}[ℐ_n^S(X_{j,p}→X_{j,p}-X_{i,p})] / X_{i,p}
```
This recursively constructs all-multiplicity, multi-loop integrands from tree-level data.

**Results:** Explicit integrands at 1-loop (all multiplicity) and 2-loop (4-point), reproducing known results in D dimensions near D=4.

### 3.3 The Cut Equation (arXiv:2412.21027)

Defines *surface functions* G_S as generating functions for all MCG-inequivalent triangulations:
```
G_S = ∑_Γ  (∏_{C∈Γ} x_C)  N_Γ(Y_C)
```
where the sum is over all triangulations Γ of surface S.

The **cut equation** is a universal recursion relation:
```
∂_{x_C} G_S = G_{S\C}
```
where S\C is the surface obtained by cutting S along curve C. This single equation generates all-loop planar integrands for colored theories and all-genus planar integrands for NLSM.

Key achievement: computed explicit all-order planar integrands for NLSM through 4 loops (with Mathematica notebook included), without spurious poles.

### 3.4 Decoupling of n and L (arXiv:2311.09284)

A "surprising fact" about the curve integral: the dependence on particle number n and loop order L is effectively decoupled. Higher-loop contributions reduce to studying tadpole-like amplitudes (single-particle-per-trace contributions), which combine with tree results to generate all-n amplitudes at L loops. This is a structural property invisible in Feynman diagrams.

### 3.5 Extension to Fermions (arXiv:2406.04411)

The curve integral formalism was extended to colored Yukawa theory (scalar-Yukawa interactions with colored fermions). The fermionic numerators are repackaged as combinatorial determinants:
```
A^{L-loop} = ∑_{subsets S, |S|=2^L}  det(M_S)  × (scalar amplitude)
```
This gives an all-loop, all-genus, all-multiplicity formula for colored Yukawa theory.

### 3.6 Surface Soft Theorem at 1-Loop (arXiv:2505.17179)

A differential operator ("surface gauge invariance operator") acting on individual gluons in the surface integrand transmutes them into scalars:
```
D^μ ℐ_n^gluon = ℐ_{n-1}^scalar
```
This is the surface-kinematics analog of the transmutation operator. Applying it near the soft limit recovers the Weinberg soft theorem, extended to the loop-integrand level.

### 3.7 Leading Singularities Discover Curves (arXiv:2512.17019, Dec 2025)

One-loop leading singularities of gluon amplitudes are determined by:
```
LS = ∑_T  (polarization structure of T)
```
where T ranges over all ways of covering the graph with non-overlapping curves such that each edge is covered exactly once. This resolves an open question about the exponents of closed curves in the surface formulation, establishing a direct bridge between on-shell methods and surface geometry at loop level.

### 3.8 All Loop Scattering As A Sampling Problem (arXiv:2503.07707)

Reformulated the curve integral as a Monte Carlo sampling problem using tropical importance sampling. The algorithm computed Tr(φ³) amplitudes up to 10-loop order in 2D. The number of sample points required grows far slower than the number of Feynman diagrams — demonstrating computational advantages of the surface formulation.

### 3.9 Inverse KLT Kernel from Surfaces (arXiv:2602.15102, Feb 2026)

The inverse KLT kernel (connecting open and closed string amplitudes) has a natural surface integrand formulation via a Berends-Giele-type recursion. This unifies cubic scalars and pions (NLSM) to all loop orders via kinematic α'-shifts, extending KLT duality to the loop-integrated level.

### 3.10 Extension to Cosmological Observables (arXiv:2412.19881, arXiv:2603.03425)

The positive geometry / surfaceology program has recently extended beyond scattering amplitudes to **cosmological wavefunctions**. The "Cosmohedra" (Figueiredo et al., arXiv:2412.19881, Dec 2024) are new polytopes whose canonical forms compute the cosmological wavefunction in Tr(φ³) theory. They are constructed by "blowing up" associahedron faces, generalizing the associahedron → amplitude connection to wavefunction → cosmohedron.

The companion paper "Combinatorics of the Cosmohedron" (Ardila-Mantilla, Arkani-Hamed, arXiv:2603.03425, Mar 2026) proves that the cosmohedron's faces are in bijection with "Matryoshkas" (nested polygon structures), and introduces a broader class of "X in Y polytopes." A surprising application: these chiseled polytopes connect to the structure of UV divergences in loop-integrated Feynman amplitudes.

This cosmological extension shows that surfaceology is not limited to scattering amplitudes — the underlying combinatorial geometry appears to govern a wider class of physical observables.

---

## 4. Connection to String Theory

### 4.1 The Original Connection: u-Variables and the String Worldsheet

The surfaceology framework has a deep and explicit connection to string theory. The key observation from arXiv:2309.15913:

**String amplitudes can be written as:**
```
A_string = ∫ [d^E t / MCG]  exp(−α' ∑_C X_C · u_C(t))
```

In the limit α'→0, u_C → step function (equals 0 or 1 on the triangulation cones), recovering the QFT amplitude. For finite α', the u_C regularize all the poles — this is exactly the string theory "smoothing" of UV singularities.

**The worldsheet = the surface:** The Riemann surface on which strings propagate is exactly the fatgraph surface. String moduli space (Mg,n) is the parameter space being integrated over. The surfaceology construction provides a combinatorial, algebraic parametrization of this moduli space without ever writing a worldsheet CFT.

### 4.2 "String Theory Written Combinatorially"

The paper explicitly shows: "string amplitudes can be written in a combinatorial formulation that makes no reference to worldsheet CFTs and vertex operators." Instead, the construction uses:
1. Hyperbolic geometry of Teichmüller space (not complex structure)
2. The u-variable equations (cluster-algebra relations)
3. The Mirzakhani kernel for the moduli space measure

This is a fundamentally different way to define string theory — from combinatorics of curves on surfaces, not from 2D CFT.

**Key implication:** String theory with finite α' is a "deformation" of the field theory amplitude, obtained by replacing the step functions (cone indicator functions) with the smooth u-variables. The QFT is the α'→0 limit.

### 4.3 Superstrings Meet Surfaceology (arXiv:2504.21676, SciPost 2025)

Tree-level open superstring (Type I) amplitudes can be written as gauge-invariant combinations of bosonic string amplitudes:
```
A_superstring = ∑_k  c_k  A_bosonic(kinematics shifted by α'/k terms)
```

This expresses superstring amplitudes in terms of bosonic string amplitudes, which are themselves given by the surfaceology formula. The framework naturally accommodates reduced Pfaffians (the NSR sector superstring vertex operators) as combinations of u-variables.

Extended to heterotic and Type II theories, with new formulas for Yang-Mills amplitudes with F³ and R² insertions.

### 4.4 Cuts and Contours (arXiv:2506.05456)

The traditional worldsheet parametrization "fails to expose the complete singularity structure." Surface kinematics resolves this by providing a global contour prescription that remains finite across all kinematics. The Feynman iε prescription, when implemented in surface kinematics, connects Euclidean and Lorentzian worldsheets naturally.

### 4.5 Surfaceology vs. String Theory: Key Distinction

Surfaceology is **not** "string theory without strings." Rather:
- **String theory with α':** All u_C → smooth functions on moduli space; massive resonances present
- **Surfaceology (QFT limit α'→0):** u_C → step functions (cones); massless poles only
- **Intermediate:** "Deformed amplitudes" obtained by keeping some α' dependence; interpolate between QFT and string

The surface provides the unifying geometric structure, but the distinction is whether we keep finite-α' smoothing or take the sharp field-theory limit.

---

## 5. The Non-Planar Question

### 5.1 Non-Planar Amplitudes Are Handled

From arXiv:2311.09284: the surfaceology framework explicitly handles non-planar amplitudes at all loop orders through higher-genus surfaces. This is one of the program's most important advantages over the amplituhedron (which is inherently planar/large-N).

**Mathematical structure:** Non-planar diagrams arise from fatgraphs on genus-g surfaces. The amplitude at loop order L, genus g, multiplicity n integrates over the moduli space:
```
M_{g,n,L} = surface with E = n + 3L + 2g internal edges
```

The mapping class group (MCG) acts on the curve space, and the Mirzakhani kernel handles this modding-out.

**Status:** Explicit all-multiplicity formulas through 2-loop, both planar (g=0) and non-planar (g=1), are given in arXiv:2311.09284.

### 5.2 The 't Hooft Expansion

The topological expansion organizes contributions by genus g:
```
A = ∑_{g≥0}  N^{2-2g}  A_g
```
where N is the number of colors. The leading term (g=0) is the planar amplitude; subleading terms are non-planar.

Surfaceology handles all g simultaneously. This is natural because the surface itself has genus g — there is no need for separate treatments.

### 5.3 Comparison to Amplituhedron

The amplituhedron is restricted to g=0 (planar, large-N limit) by construction — it was designed for N=4 SYM in the planar limit. Surfaceology naturally extends to all genera, making it more general for the topology expansion, though it applies to different theories.

---

## 6. Open Problems and Future Directions

### 6.1 The Central Open Problem: Momentum Space

The loop-level results (1-loop YM integrand, hidden zeros at loop level) are expressed in "surface kinematics" — variables X_{i,j} that are distinct from standard loop momenta ℓ. The missing link is:

**How do we go from surface kinematics back to conventional loop momentum space?**

The surface kinematic variables include both standard Mandelstam invariants AND additional loop-sector variables (X_{i,p} where p labels the puncture) that don't have direct momentum-space counterparts. Computing actual S-matrix elements requires integrating over the loop momenta, which requires returning to conventional kinematics.

This is explicitly acknowledged as the central technical challenge in arXiv:2408.11891 and arXiv:2503.03805.

### 6.2 Yang-Mills at Higher Loops

The 2-loop YM integrand is known (2-loop 4-point in arXiv:2408.11891), but the full all-loop YM recursion in surface kinematics is not yet resolved. The recursion relation exists (the "cut equation"), but explicit all-multiplicity formulas at 3-loop and beyond remain open.

### 6.3 N=4 SYM Connection

The amplituhedron applies to N=4 SYM. Does surfaceology have an N=4 SYM sector? The answer is not yet clear — the massive spin-2 ghost of Yang-Mills (present in non-SUSY YM) doesn't appear, so the supersymmetric completion might require new structure. This is open.

### 6.4 Standard Model Applications

All surfaceology results so far are for colored theories (where large-N / planar limit makes sense). Extending to electroweak theory (without color) or to full Standard Model requires:
- Handling uncolored particles differently (tree-level surface functions work; loops require color)
- Incorporating masses properly (massive deformations exist in principle)
- Including fermions with fractional statistics (started in arXiv:2406.04411 for Yukawa)

### 6.5 Gravity

All surfaceology papers address gauge theories. The double copy (BCJ/KLT relations) connects gauge and gravity amplitudes, but a direct "gravity surfaceology" has not been constructed. The inverse KLT kernel (arXiv:2602.15102) is a step in this direction.

### 6.6 Integrated Amplitudes

The surfaceology formula gives *integrands*, not integrated amplitudes. Performing the loop integrals (even for φ³ at 1-loop) in the surface formulation has not been fully worked out — the Schwinger representation is standard, but the surface kinematic variables introduce additional complications for regularization.

---

## 7. Assessment: Is This the "Final Form"?

### 7.1 What Surfaceology Achieves

Surfaceology is a genuinely new, powerful framework that:
1. **Unifies** colored scalar, NLSM, Yang-Mills, Yukawa, and string amplitudes under a single mathematical framework
2. **Solves old problems** (canonical YM loop integrand, 1/0 ambiguities, non-planar extension)
3. **Makes new structure manifest** (hidden zeros, surface soft theorem, decoupling of n and L)
4. **Connects QFT to string theory** without worldsheet CFT
5. **Works at all loop orders and all multiplicities** (for colored scalar theories)

The rate of progress is remarkable: from the founding paper in September 2023 to ~15+ papers through early 2026, covering extensions to YM, fermions, NLSM, strings, leading singularities, soft theorems, and computational methods.

### 7.2 What Surfaceology Does NOT Achieve

1. **It does not cover N=4 SYM** — the amplituhedron is still the framework of choice for that theory
2. **The loop-momentum-space bridge is missing** — the practical connection to observable amplitudes (for non-scalar theories) requires work
3. **Gravity is not included** — double copy gives a route, but direct gravity surfaceology is absent
4. **Non-colored theories** (QED, electroweak) are not yet handled at loop level
5. **It is an integrand formula, not an integrated formula** — computing actual cross-sections requires additional steps

### 7.3 Relation to the "Positive Geometry" Program

Surfaceology is the **kinematic-space incarnation** of positive geometry. The canonical form of a positive geometry = the amplitude = the sum over triangulations of a surface. The innovation is:

- ABHY: canonical form of an associahedron in kinematic space (tree-level)
- Surfaceology: canonical form of the moduli space of surfaces (all loops)

So surfaceology is the all-loop extension of positive geometry to kinematic space.

### 7.4 Verdict

Surfaceology is almost certainly not the "final form" — the missing bridge to conventional momentum space (especially for non-scalar theories) means we are still in the middle of the program. But it is clearly the **current leading framework** for colored amplitude theory, and the rate of progress suggests the remaining gaps may be filled in the next few years.

The relationship between surfaceology (kinematic space) and the amplituhedron (auxiliary twistor space) remains mysterious and may point to a deeper unification. This is the most important open conceptual question in the positive geometry / surfaceology program.

---

## 8. Summary of Key Mathematical Results

| Result | Paper | Status |
|---|---|---|
| All-loop colored φ³ amplitudes = counting problem | arXiv:2309.15913 | Proved |
| Non-planar φ³ amplitudes at all loops | arXiv:2311.09284 | Proved (explicit through 2-loop) |
| NLSM = Tr(φ³) with δ-shift | arXiv:2403.04826 | Proved |
| Colored Yukawa all-loop formula | arXiv:2406.04411 | Proved |
| Canonical YM loop integrand (1-loop) | arXiv:2408.11891 | Proved (PRL 2025) |
| Cut equation for NLSM (all-order recursion) | arXiv:2412.21027 | Proved |
| Cosmohedra for cosmological wavefunctions | arXiv:2412.19881 | Proved (tree-level) |
| Hidden zeros ↔ unitarity (biconditional) | arXiv:2503.03805 | Proved (1-loop, with locality assumption) |
| Superstring amplitudes = bosonic string combinations | arXiv:2504.21676 | Proved (tree level, SciPost 2025) |
| Surface soft theorem at 1-loop | arXiv:2505.17179 | Proved |
| Gluon leading singularities from curve covers | arXiv:2512.17019 | Proved |
| Monte Carlo sampling for loop amplitudes | arXiv:2503.07707 | Demonstrated (10-loop φ³) |
| Inverse KLT kernel as surface integrand | arXiv:2602.15102 | Proved (Feb 2026) |
| Combinatorics of cosmohedron; UV divergences | arXiv:2603.03425 | Proved (Mar 2026) |

---

## 9. References

1. Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas. "All Loop Scattering As A Counting Problem." arXiv:2309.15913 (Sep 2023).
2. Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas. "All Loop Scattering For All Multiplicity." arXiv:2311.09284 (Nov 2023).
3. Arkani-Hamed, Figueiredo. "Circles and Triangles, the NLSM and Tr(Φ³)." arXiv:2403.04826 (Mar 2024).
4. De, Pokraka, Skowronek, Spradlin, Volovich. "Surfaceology for Colored Yukawa Theory." arXiv:2406.04411 (Jun 2024).
5. Arkani-Hamed, Cao, Dong, Figueiredo, He. "Surface Kinematics and 'The' Yang-Mills Integrand." arXiv:2408.11891 (Aug 2024). Published in PRL 2025.
6. Arkani-Hamed, Frost, Salvatori. "The Cut Equation." arXiv:2412.21027 (Dec 2024).
7. Backus, Rodina. "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop Order." arXiv:2503.03805 (Mar 2025). Published in PRL.
8. Salvatori. "All Loop Scattering As A Sampling Problem." arXiv:2503.07707 (Mar 2025).
9. Cao, Dong, He, Zhu. "Superstring amplitudes meet surfaceology." arXiv:2504.21676 (Apr 2025). Published in SciPost Physics 19, 114 (2025).
10. Backus, Figueiredo. "Surface Gauge Invariance, Soft Limits and the Transmutation of Gluons into Scalars." arXiv:2505.17179 (May 2025). Published in JHEP.
11. Figueiredo, Skowronek. "Cuts and Contours." arXiv:2506.05456 (Jun 2025).
12. Carrôlo, Figueiredo. "How gluon leading singularities discover curves on surfaces." arXiv:2512.17019 (Dec 2025).
13. Bartsch, Kampf, Novotný, Trnka. "A Surface Integrand for the Inverse KLT Kernel." arXiv:2602.15102 (Feb 2026).
14. Arkani-Hamed, Bai, He, Yan. "Scattering Forms and the Positive Geometry of Kinematics, Color and the Worldsheet" (ABHY). arXiv:1711.09102 (2017).
15. Figueiredo et al. "Cosmohedra." arXiv:2412.19881 (Dec 2024).
16. Ardila-Mantilla, Arkani-Hamed. "Combinatorics of the Cosmohedron." arXiv:2603.03425 (Mar 2026).
17. Salvatori, Backus, Figueiredo, Skowronek. "All Loop Scattering As A Sampling Problem." arXiv:2503.07707 (Mar 2025).
