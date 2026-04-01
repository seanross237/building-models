# Exploration 005: Hidden Zeros — The Frontier of Positive Geometry Beyond N=4 SYM

**Goal:** Deep dive into the hidden zeros program. Understand what hidden zeros are, the March 2025 paper (arXiv:2503.03805), how far the program extends beyond N=4 SYM, and whether this represents a new principle of QFT or a reformulation.

**Papers surveyed:**
- arXiv:2312.16282 — "Hidden zeros for particle/string amplitudes and the unity of colored scalars, pions and gluons" (Arkani-Hamed, Cao, Dong, Figueiredo, He; 2023/updated 2024) — **THE original hidden zeros paper**
- arXiv:2503.03805 — "Emergence of Unitarity and Locality from Hidden Zeros at One-Loop Order" (Backus, Rodina; March 2025; published in Physical Review Letters)
- arXiv:2406.04234 — "Hidden zeros are equivalent to enhanced ultraviolet scaling and lead to unique amplitudes in Tr(φ³) theory" (Rodina; published PRL 2025)
- arXiv:2403.10594 — "Hidden Amplitude Zeros From Double Copy" (Bartsch, Brown, Kampf, Oktem, Paranjape, Trnka; 2024)
- arXiv:2309.15913 — "All Loop Scattering As A Counting Problem" (Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas; 2023) — the surfaceology paper
- arXiv:2408.11891 — "Surface Kinematics and 'The' Yang-Mills Integrand" (Arkani-Hamed, Cao, Dong, Figueiredo, He; 2024, PRL 2025)
- arXiv:2412.21027 — "The Cut Equation" (Arkani-Hamed, Frost, Salvatori; 2024)
- arXiv:2503.23579 — "Hidden Zeros of the Cosmological Wavefunction" (De, Paranjape, Pokraka, Spradlin, Volovich; 2025)
- Plus 10+ additional follow-up papers from 2024-2026

---

## Section 1: What Are Hidden Zeros?

### Background: The ABHY Kinematic Setup

The ABHY (Arkani-Hamed–Bai–He–Yan) paper (arXiv:1711.09102) established that tree-level bi-adjoint scalar amplitudes (Tr(φ³) theory) equal the canonical form of an associahedron living naturally in kinematic space. This set up the framework of "positive geometry of kinematics."

The key variables in the ABHY framework:
- **Planar variables** X_{i,j} = (p_i + p_{i+1} + ... + p_{j-1})² — these correspond to chords of an n-gon / diagonals of the polygon
- **Non-planar variables** c_{i,j} = −2p_i · p_j — the actual Mandelstam invariants for non-adjacent particles, related to planar variables by:
  - c_{i,j} = X_{i,j} + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j} (a "lattice Laplacian" on the mesh)
- **Kinematic mesh**: The n-point mesh is an (n−1)×(n−1) grid of kinematic variables X_{i,j} (upper triangular portion), where the c_{i,j} appear as differences in the lattice

The associahedron lives in the space where all X_{i,j} > 0 and all c_{i,j} ≥ 0. Physical amplitudes are the canonical form — the unique differential form with simple poles on all faces.

### Definition of Hidden Zeros (Tree Level)

The hidden zeros theorem (discovered in arXiv:2312.16282, proved there for tree-level Tr(φ³)):

> **Consider an n-point tree-level amplitude in Tr(φ³). Choose any "causal diamond" in the kinematic mesh: pick a point X_B and follow the two lightlike rays up from X_B, bouncing off the boundaries of the mesh, until they meet at X_T. Set all c_{i,j} variables INSIDE this causal diamond to zero. The amplitude vanishes.**

This is "hidden" because it is not manifest from Feynman diagrams — each individual diagram contributes nonzero at this locus, but all contributions cancel. It IS made obvious by the associahedron connection: these c_{i,j} are exactly the non-planar variables that control whether the kinematic point is inside the associahedron, and the zero locus corresponds to a specific boundary structure.

### Explicit 5-Point Example

The 5-point amplitude is:
```
A_5 = 1/(X_{1,3}X_{1,4}) + 1/(X_{2,4}X_{2,5}) + 1/(X_{1,3}X_{3,5})
    + 1/(X_{1,4}X_{2,4}) + 1/(X_{2,5}X_{3,5})
```
(These are the 5 planar cubic diagrams.)

**Hidden zero:** Set c_{1,3} = 0 AND c_{1,4} = 0 simultaneously. These two variables form a causal diamond in the 5-point mesh. Result: A_5 = 0.

**Factorization near the zero:** When only c_{1,4} → 0 (approach the zero with one c nonzero), the amplitude factorizes:
```
A_5 → (1/X_{1,3} + 1/X_{2,5}) × (1/X_{1,4} + 1/X_{3,5})
```
This is NOT the usual factorization on a pole (which would be 1/X_{i,j} × A_L × A_R). It is a new kind of "soft" or "kinematic" factorization that has no classical-field-theory counterpart.

**General factorization formula (eq. 3.8 of arXiv:2312.16282):**
```
A_n(c_* ≠ 0) = (1/X_B + 1/X_T) × A^{down} × A^{up}
```
where A^{down} and A^{up} are lower-point amplitudes with momenta determined by the mesh geometry.

### Geometric Origin

The causal diamond construction is directly motivated by the geometry of the ABHY associahedron. In the kinematic mesh:
- The diamonds correspond to specific 2D sublattices
- Setting all c_{i,j} in a diamond to zero forces the amplitude to live on a specific boundary of the associahedron
- This boundary structure corresponds to a "collapse" in which the associahedron degenerates
- The factorization near zeros corresponds to a "telescope" decomposition of the canonical form

The authors note: "a clear interpretation of our zeros in familiar physical terms is still lacking" — these zeros are NOT related to momentum going on-shell (like factorization poles) or to soft limits in the usual sense. They are a genuinely new structure, visible only from the geometric perspective.

### Relationship to Adler Zero

For the Non-Linear Sigma Model (pions), the hidden zeros include but extend the Adler zero. The standard Adler zero says A → 0 when any single external momentum p_i → 0 ("soft pion theorem"). The NLSM hidden zeros say the amplitude vanishes when a full set of c_{i,j} in a causal diamond vanish — which is a different and more constraining condition. The Adler zero follows as a special case (the soft limit corresponds to a specific sub-case of the zero conditions), but the general zero is a stronger constraint.

---

## Section 2: The 2024 Discovery — Unity of Colored Theories (arXiv:2312.16282)

### Main Claim: Three Theories in One Function

The central discovery is:

> **The "stringy" Tr(φ³) amplitude secretly contains the scattering amplitudes for pions (NLSM) and non-supersymmetric gluons (Yang-Mills), related by a simple kinematic shift.**

This is encoded in the one-parameter family:
```
I^δ_{2n} = I^{Tr(φ³)}_{2n}[α'X_{e,e} → α'(X_{e,e}+δ), α'X_{o,o} → α'(X_{o,o}−δ)]
```
where X_{e,e} means even-indexed planar variables and X_{o,o} means odd-indexed ones.

The three theories correspond to:
- **α'δ = 0**: Tr(φ³) theory (scalar bi-adjoint)
- **α'δ ∈ (0,1)**: Non-Linear Sigma Model (pion amplitudes)
- **α'δ = 1**: Yang-Mills / scaffolded gluons

The shift is unique: it is proved that this is the **unique** kinematic shift that preserves the hidden zeros.

### How Gluons Emerge from Scalars

The "scaffolded gluons" construction: take 2n scalars labeled (1,2,...,2n) in a ring. Define:
```
q^μ_i = (p_{2i} + p_{2i-1})^μ   (the gluon momentum)
ε^μ_i ∝ (p_{2i} − p_{2i-1})^μ  (the gluon polarization)
```
At δ=1, the I^{δ=1}_{2n} amplitude, viewed in terms of the composite momenta q_i and polarizations ε_i, exactly reproduces the n-gluon Yang-Mills amplitude. The gluon polarization vectors EMERGE from the differences of pairs of scalar momenta.

This is structurally similar to how strings give rise to both gauge fields and gravitons — but here it works directly at the level of tree amplitudes in field theory.

### The Universal Zero Property

A crucial observation: **All three theories have hidden zeros at exactly the same kinematic locus.**

Specifically:
- Tr(φ³): zeros when causal diamond c_{i,j} = 0
- NLSM (pions): zeros when the same c_{i,j} = 0 (AND, for Yang-Mills, additionally ε_i·p_j = ε_j·p_i = ε_i·ε_j = 0)
- Yang-Mills: zeros when c_{i,j} = 0 AND all polarization contractions with the diamond vanish

This universality — the same kinematic locus kills all three theories — is what the authors call the "unity of colored scalars, pions and gluons."

### Evidence That Zeros Determine Amplitudes

A key (experimentally verified) observation in arXiv:2312.16282 Section 3: for n=5,6,7, the hidden zeros completely fix the Tr(φ³) amplitude (up to normalization) from a general ansatz. Similarly for NLSM at n=6,8. The paper does NOT prove this; it observes it numerically and notes it as a conjecture.

This conjecture was subsequently proved by Rodina (arXiv:2406.04234): hidden zeros are equivalent to enhanced UV scaling under BCFW shifts, and this combined with the structure of ordered propagators uniquely determines Tr(φ³) amplitudes.

---

## Section 3: The March 2025 Paper (arXiv:2503.03805) — Emergence at One-Loop

### Context and Motivation

The paper by Backus and Rodina (Princeton/BIMSA) extends the hidden zeros program from tree-level to one-loop, using the "surface integrand" technology. This is the strongest evidence to date that the emergence program extends beyond N=4 SYM and beyond tree level.

**Key technical obstacle at loop level:** Loop integrands are ambiguous in a way tree amplitudes are not — you can always add terms that vanish on all unitarity cuts (contact terms, "scheme" ambiguities). Also, tadpoles and external bubbles create 1/0 ambiguities. The surface integrand technology (from arXiv:2408.11891) resolves this by working on a "punctured momentum disk" where loop momenta live on the boundary.

### One-Loop Kinematic Variables

The one-loop setup extends the kinematic mesh. New variables:
- **Y^±_i**: loop momentum variables attached to external leg i, with two parities ±
- The loop mesh is a "punctured n-gon" where the puncture represents the loop momentum

The one-loop versions of the c_{i,j} at the diagonal are:
```
c_{i,i} = X_{i,i} − Y^−_i − Y^+_i
c_{i+1,i} = X_{i+1,i} − X_{i,i} − X_{i+1,i+1} + Y^−_{i+1} + Y^+_i
```

### Definition of One-Loop Hidden Zeros ("Big Mountains")

The one-loop hidden zeros correspond to **maximal triangles** ("big mountains") on the one-loop mesh, rather than causal diamonds. Specifically, the (i,±)-zero imposes:
```
c_{m,k} = 0, for m ∈ {k, k+1, ..., i-1}, for each k = 1, 2, ..., n
```

At n-points there are **2n big mountain zeros** (n for each parity). The existence of these zeros in the actual loop integrand is proved.

### Main Theorem: Unitarity ↔ Hidden Zeros

**Theorem (proved, assuming locality):** A local one-loop Tr(φ³) surface integrand is **unitary if and only if it satisfies the big mountain zeros**.

This is remarkable:
- Direction 1 (unitarity ⟹ zeros): The actual physical integrand satisfies the zeros. Proved in Appendix E.
- Direction 2 (zeros ⟹ unitarity): Assuming locality, any integrand satisfying the zeros must be unitary. Proved in Section 4.

The biconditional makes hidden zeros a perfect characterization of unitarity (given locality) at one-loop.

### The Starting Ansatz

The most ambitious version (Section 4, "Without Assuming Locality"):
- Start with a **generic, non-local, non-unitary ansatz** for the n-point one-loop integrand
- At 4-points, this ansatz has ~6,500 free parameters
- Impose the 2n = 8 big mountain zeros

**Result (numerically verified at 4-points):** The zeros reduce the ansatz to the **unique physical integrand**. Both locality AND unitarity emerge simultaneously from the zeros.

This is the strongest result — it says hidden zeros contain ALL the information needed to fix the amplitude, without pre-assuming any physical principle.

### The Reduced Ansatz (Assuming Locality)

When locality IS assumed (local ansatz), the ansatz collapses to:
```
M_n = a^+ I^+_n + a^− I^−_n
```
just 2 free parameters (the two parity-weighted versions of the known integrand). The zeros force a^+ = a^−, fixing the integrand uniquely.

### Factorization Near One-Loop Zeros

Near an (i,∓)-zero with only c_* ≠ 0:
```
I_n(c_* ≠ 0) = (1/Y^∓_i + 1/Y^±_{i-1}) × A_{n+2}
```
where A_{n+2} is a TREE-LEVEL (n+2)-point amplitude with kinematic variables from the mesh. This loop-to-tree factorization is remarkable: the loop integrand near its zeros factorizes onto tree-level objects.

### NLSM at One-Loop

For the Non-Linear Sigma Model: zeros alone are **not sufficient** to fix the integrand. Instead, imposing **factorization near zeros** (the formula above, but for NLSM) uniquely fixes the NLSM one-loop integrand, assuming neither locality nor unitarity. Verified at 4-points. This is stated as a conjecture.

### Explicit Loop Integrands

The 2-point and 3-point Tr(φ³) surface integrands are given explicitly (Appendix F):

**2-point:**
```
I^{Tr(φ³)}_2 = 1/(Y^+_1 Y^+_2) + 1/(Y^+_1 X_{1,1}) + 1/(Y^+_2 X_{2,2}) + (Y^+ ↔ Y^−)
```

**3-point:**
```
I^{Tr(φ³)}_3 = [1/(Y^+_1 X_{1,1}) × (1/X_{2,1} + 1/X_{1,3}) + (cyclic)]
             + [1/(Y^+_2 Y^+_3 X_{3,2}) + (cyclic) + 1/(Y^+_1 Y^+_2 Y^+_3)] + (Y^+ ↔ Y^−)
```

### Limitations Stated by Authors

1. The non-local uniqueness theorem (no locality assumption) is **proved only at 4-points numerically**; the general case is conjectured.
2. **NLSM uniqueness** from factorization is also a conjecture (verified at 4-points).
3. The one-loop zeros are defined in **surface kinematics** — these do NOT directly translate to standard momentum-space kinematics. Whether any structure survives is noted as "likely non-trivial."
4. **Yang-Mills at one-loop** is not treated; it's identified as future work.
5. Only **one-loop order** is treated; two-loop and beyond are open.
6. Ansatz size grows **factorially** with n, making higher-multiplicity verification extremely computationally intensive (~6,500 parameters at 4-points for non-local ansatz; ~25,000 for NLSM).

---

## Section 4: Scope of Extension

### What Is Established (Proven or Strongly Verified)

| Claim | Status | Evidence |
|-------|--------|---------|
| Hidden zeros at tree level in Tr(φ³) | **Proved** (arXiv:2312.16282) | General theorem with explicit formulas |
| Hidden zeros at tree level in NLSM | **Proved** (arXiv:2312.16282) | Checked for 4,6,8-point |
| Hidden zeros at tree level in Yang-Mills | **Observed** (arXiv:2312.16282) | Checked, proof deferred |
| Zeros uniquely determine Tr(φ³) tree amplitudes | **Proved** (arXiv:2406.04234) | Equivalence to UV scaling |
| Zeros uniquely determine NLSM tree amplitudes (experimental) | **Observed** (arXiv:2312.16282) | n=6,8 |
| One-loop zeros exist in Tr(φ³) and NLSM | **Proved** (arXiv:2503.03805) | General construction |
| Unitarity ↔ zeros in Tr(φ³) at 1-loop (local ansatz) | **Proved** (arXiv:2503.03805) | Full proof |
| Zeros uniquely fix Tr(φ³) at 1-loop (non-local ansatz) | **Conjectured** | 4-point numerical |
| NLSM uniquely fixed by factorization at 1-loop | **Conjectured** | 4-point numerical |

### What Is Open

1. **Two-loop and beyond**: The surface integrand framework (arXiv:2309.15913, arXiv:2412.21027) extends to all loops as a formal framework, but whether hidden zeros work there is not established.

2. **Yang-Mills at 1-loop**: Explicitly identified as future work in arXiv:2503.03805. The surface kinematics paper (arXiv:2408.11891) constructs the canonical YM integrand but doesn't address hidden zeros there.

3. **Standard momentum-space formulation**: The loop zeros are defined in surface kinematics. Whether analogous structures exist in standard (momentum-space) loop integrands is unknown and noted as "likely non-trivial."

4. **QCD and realistic theories**: No evidence yet that hidden zeros extend to theories with fermions or non-cubic interactions beyond what surfaceology covers.

5. **Higher multiplicity proof of non-local uniqueness**: Only 4-point numerically verified.

### The Key Physical Question: Does This Work for Gravity?

The hidden zeros program applies to colored theories (theories with adjoint color). The double-copy results (arXiv:2403.10594) show that hidden zeros in Yang-Mills/NLSM transfer to Galileon amplitudes and special gravity amplitudes through KLT relations. But full graviton scattering in general relativity is not covered.

The cosmological wavefunction paper (arXiv:2503.23579) shows hidden zeros extend to scalar field theory in de Sitter space — the first cosmological context.

---

## Section 5: Relationship to the Amplituhedron and Surfaceology

### The Amplituhedron Program (N=4 SYM)

The amplituhedron lives in auxiliary twistor space and applies only to N=4 SYM (and ABJM). As established in exploration-004, for N=4 SYM it is a reformulation. The positive geometry there enforces locality (poles only on boundaries) and unitarity (boundaries factorize) geometrically — but it doesn't generalize to other theories because those theories are not UV-finite enough to have a clean positive geometry without reference to spacetime.

### The Hidden Zeros / Surfaceology Program

Hidden zeros operate in **kinematic space directly** (not auxiliary twistor space). The ABHY associahedron lives in the space of Mandelstam invariants. This makes it applicable to:
- Any theory whose amplitudes can be expressed via the CHY formalism / as functions of planar and non-planar Mandelstam invariants
- Non-supersymmetric theories (gluons, pions, bi-adjoint scalars)
- Loop integrands in the surface kinematics framework

The surfaceology program (arXiv:2309.15913, arXiv:2412.21027) is a more general formulation:
- **Amplitudes = integrals of canonical forms over moduli spaces of surfaces** (with punctures and decorations)
- For tree level: surfaces with genus 0 and punctures = worldsheets
- For loop level: surfaces with higher genus = loop topologies
- The Tr(φ³) amplitude at all loops is reproduced by counting certain curves on surfaces (a "counting problem" — the title of arXiv:2309.15913)
- The "Cut Equation" (arXiv:2412.21027) gives a universal recursion relation for these surface functions, generating planar integrands at all loop orders for colored theories

**The relationship:**
- Amplituhedron: special geometry for N=4 SYM, lives in twistor space, limited to UV-finite theories
- Surfaceology/Hidden zeros: more general framework living in kinematic space, applies to non-SUSY theories, extends to loop level via surface integrands
- They are NOT competitors — they address different regimes. Surfaceology generalizes the ABHY approach, which was the precursor to the amplituhedron program.

### Are Hidden Zeros a Competitor to the Amplituhedron?

No. They are:
1. **In different theories**: Hidden zeros apply to Tr(φ³), NLSM, Yang-Mills; the amplituhedron applies to N=4 SYM.
2. **At different levels of precision**: The amplituhedron is fully developed (all n, all k, all L in principle); hidden zeros at loop level are conjectural beyond 4-points.
3. **Philosophically different**: The amplituhedron replaces all QFT principles; hidden zeros impose specific kinematic conditions that force locality/unitarity to emerge.

The hidden zeros program is the **natural generalization** of the amplituhedron spirit to non-SUSY theories and realistic quantum field theories. Whether this generalization can eventually match the amplituhedron's completeness for its respective theories is an open question.

---

## Section 6: Novel Predictions and Physical Consequences

### Prediction 1: New Amplitude Zeros

Hidden zeros predict specific kinematic configurations where NLSM and Yang-Mills amplitudes must vanish. These are NOT predicted by standard Feynman rules or known symmetries. They have been verified numerically but not explained physically. They represent a genuinely new constraint on physical scattering amplitudes.

**Observable consequence**: In principle, these zeros could be tested in physical scattering experiments, but the kinematic configurations required (setting multiple non-planar invariants to zero simultaneously) are highly non-generic and may be hard to probe experimentally. The more immediate application is theoretical: as universal constraints on EFT amplitudes.

### Prediction 2: Unity of Colored Theories

The δ-deformation predicts a **one-parameter family of interpolating amplitudes** between scalars, pions, and gluons. At integer values α'δ = 0, 1 the endpoints are field theory. At intermediate values, the amplitude has no field-theoretic interpretation — it's something new (string-theoretic). The existence of this interpolating family is a prediction not visible from individual Lagrangians.

More concretely: **NLSM amplitudes can be obtained from Tr(φ³) amplitudes by a universal kinematic shift**. This means any technique that works for Tr(φ³) (including new bootstrap techniques from hidden zeros) automatically applies to pions.

### Prediction 3: Loop Integrands Fixed by Zeros

The most ambitious claim (conjectured): one-loop Tr(φ³) integrands are uniquely determined by hidden zeros without assuming locality or unitarity. If proved, this would show that the standard properties of quantum field theory (locality, unitarity) at one-loop are not independent axioms but consequences of a more primitive geometric structure. This is a paradigm shift.

### Prediction 4: Cosmological Hidden Zeros

The extension to cosmological wavefunctions (arXiv:2503.23579) predicts that certain cosmological correlators have hidden vanishing properties not visible in standard in-in perturbation theory. This extends the hidden structure to a completely different physical context.

### Prediction 5: Yang-Mills Factorization at Loop Level

The paper arXiv:2408.11891 defines "the" canonical loop integrand for non-SUSY Yang-Mills theory using surface kinematics — the first such integrand with well-defined single-loop cuts at all multiplicities. This is a concrete prediction for the 1-loop n-gluon integrand in non-SUSY YM, something that was not previously uniquely defined.

### Double-Copy Extension

The paper arXiv:2403.10594 shows that hidden zeros in YM/NLSM **transfer to Galileon amplitudes** via the KLT double copy. This extends the zeros to a gravitational scalar theory, with potential implications for gravity amplitude constraints.

---

## Section 7: Assessment — New Principle or Reformulation?

### The Central Question

Is the hidden zeros program:
(a) A new physical principle that reveals structure invisible from standard QFT?
(b) A reformulation / repackaging of known constraints (unitarity, locality, soft theorems)?

### The Evidence

**In favor of (a) — genuinely new:**

1. The zeros are NOT visible from Feynman diagrams individually. They require cancellation between diagrams. Their existence required geometric insight.

2. The unity of colored theories (Tr(φ³) ↔ NLSM ↔ Yang-Mills via a single δ-deformation) is a new result not derivable from Lagrangians. It reveals a structural relationship between three apparently different theories.

3. The 1-loop result (arXiv:2503.03805) shows that hidden zeros are **equivalent** to unitarity (not just implied by it, but a biconditional). This means zeros are a new characterization of a standard physical property, and this characterization is more fundamental in the sense that it allows relaxing locality.

4. The zeros extend to cosmological wavefunctions, double copy theories, and loop integrands — a surprising generality suggesting they are a fundamental feature of amplitude mathematics, not an accident of a specific theory.

**In favor of (b) — reformulation:**

1. At tree level, the hidden zeros in Tr(φ³) follow from the geometry of the associahedron, which already encodes all of locality and unitarity. So the zeros ARE a consequence of known QFT.

2. The Adler zero (soft pion theorem) follows from chiral symmetry / the nonlinear sigma model structure. The NLSM hidden zeros generalize the Adler zero but may ultimately be traceable to the same symmetry.

3. Rodina's paper (arXiv:2406.04234) shows hidden zeros are equivalent to **UV scaling conditions** — which can be derived from BCFW recursion and known properties of amplitudes. So one could argue the zeros are "derived" from standard QFT tools, not independent.

4. The 1-loop result is currently verified only at 4-points for the non-local ansatz. The proof hasn't extended the claim beyond what unitarity and locality already guarantee at verified multiplicity.

### Verdict: Both, But the Non-Local Conjecture Is the Key

The honest assessment is:

**Already proven:** Hidden zeros are a new, elegant CHARACTERIZATION of physical amplitude properties (locality, unitarity) that makes them visible in a different way. The "unity of colored theories" via the δ-deformation is a genuine structural result — it goes beyond reformulation by unifying what looked like three separate theories.

**The potentially revolutionary claim (still conjectural):** That zeros from a NON-LOCAL ansatz uniquely fix the amplitude, deriving locality and unitarity from a more primitive geometric principle. If this is proved at all multiplicities and all loop orders, it would represent a genuine new principle: scattering amplitudes are determined by geometric vanishing conditions on kinematic space, and standard QFT principles (locality, unitarity) are consequences rather than axioms. This would parallel how the amplituhedron eliminates locality and unitarity as inputs for N=4 SYM — but would do so for the full class of colored theories including non-SUSY gauge theories.

**Current status:** We are in an intermediate phase. The program has produced clear results (unity of colored theories, tree-level uniqueness theorems, 1-loop equivalences) but the deepest claims (non-local uniqueness at loop level, extension to YM) remain conjectural. The extensive follow-up literature (20+ papers in 2024-2026) and the rapid pace of progress suggest the community considers this a genuine breakthrough direction.

---

## Section 8: Surfaceology — The Broader Framework

The "surfaceology" program (arXiv:2309.15913 "All Loop Scattering As A Counting Problem") is the overarching framework in which both the hidden zeros and the amplituhedron program live.

### What Is It?

**Surfaceology = scattering amplitudes from integrals over moduli spaces of surfaces decorated with kinematic data.**

Key elements:
- **Curves on surfaces**: Physical amplitudes correspond to specific curves drawn on oriented surfaces
- **Counting problem**: For Tr(φ³) at all loops, the integrated amplitude equals a sum over ways to fill a polygon with curves satisfying certain combinatorial rules — a literal counting problem with no Feynman diagrams
- **All-loop**: The framework handles all genera simultaneously via generating functions
- **Surface functions**: The fundamental objects are "surface functions" F(surface) that generate amplitudes when integrated; they satisfy a "Cut Equation" recursion relation (arXiv:2412.21027)

### Surface Kinematics

For loop integrands (as opposed to integrated amplitudes), the surface kinematics framework (arXiv:2408.11891) introduces:
- Kinematics on a punctured disk (the surface with a boundary representing loop momentum)
- Y^± variables as loop-momentum analogs
- Surface integrands that are canonical forms on these generalized kinematic spaces
- For Yang-Mills: a canonical integrand with well-defined cuts at all multiplicities (solving the gauge ambiguity problem that plagued previous approaches)

### Relationship to Hidden Zeros

Hidden zeros are a feature OF the surface integral approach: they emerge naturally because the canonical form on the surface has specific vanishing properties at boundaries. The loop-level hidden zeros (big mountains) correspond geometrically to specific degeneration limits of the punctured disk. The surfaceology framework is thus the geometric HOME of hidden zeros, and the zeros encode what happens when the surface reaches its boundary.

---

## Section 9: Synthesis and Limitations

### What Has Been Established (Confident)

1. **Hidden zeros exist** at tree level in Tr(φ³), NLSM, Yang-Mills — proved or well-verified.
2. **Zeros uniquely determine tree-level Tr(φ³) amplitudes** — proved (Rodina 2025).
3. **Zeros (via δ-deformation) unify Tr(φ³), pions, gluons** — proved (arXiv:2312.16282).
4. **One-loop hidden zeros exist** and are equivalent to unitarity (assuming locality) for Tr(φ³) — proved (arXiv:2503.03805).
5. **A canonical 1-loop Yang-Mills integrand** exists via surface kinematics (arXiv:2408.11891).

### What Remains Conjectural

1. **Non-local uniqueness at 1-loop**: Verified at 4-points, not proved.
2. **NLSM at 1-loop**: Factorization fixes integrand, verified at 4-points, not proved.
3. **Two-loop and beyond**: Framework exists, zeros not established.
4. **Standard momentum-space formulation of loop zeros**: Unknown if any structure survives in ordinary Feynman integral language.
5. **Extension to QCD, gravity**: Not established.

### Key Limitation: Surface Kinematics vs. Momentum Space

A critical limitation: the one-loop zeros are defined in "surface kinematics" (Y^± variables) which are NOT standard loop momenta. The result that zeros fix the integrand is thus technically a statement about the surface integrand, not about any standard Feynman integrand written in ℓ^μ loop momentum. Whether there is an analog in momentum space is explicitly left open by the authors as "likely non-trivial."

This means the loop-level results, while internally consistent and impressive, are formulated in a framework (surface integrands) that is itself not yet widely adopted. The hidden zeros program and surfaceology are deeply intertwined — you almost cannot separate them at loop level.

---

## References and Key Paper Details

| arXiv ID | Year | Title (abbreviated) | Key contribution |
|----------|------|---------------------|-----------------|
| 1711.09102 | 2017 | Scattering Forms and Positive Geometry of Kinematics (ABHY) | ABHY associahedron, basis for hidden zeros |
| 2312.16282 | 2023 | Hidden zeros: unity of colored scalars, pions, gluons | Original hidden zeros paper, δ-deformation |
| 2406.04234 | 2024 | Hidden zeros = enhanced UV scaling | Proved zeros uniquely determine Tr(φ³) tree amplitudes |
| 2403.10594 | 2024 | Hidden zeros from double copy | Zeros in Galileon via KLT; verified double-copy transfer |
| 2309.15913 | 2023 | All loop scattering as counting problem | Surfaceology — curves on surfaces, all-loop framework |
| 2408.11891 | 2024 | Surface kinematics and "the" YM integrand | Canonical YM 1-loop integrand via surface kinematics |
| 2412.21027 | 2024 | The cut equation | All-loop recursion for surface functions |
| 2503.03805 | 2025 | Emergence of unitarity/locality from zeros at 1-loop | Loop-level zeros; unitarity ↔ zeros theorem |
| 2503.23579 | 2025 | Hidden zeros of cosmological wavefunction | Extension to cosmology |
| 2406.04411 | 2024 | Surfaceology for colored Yukawa theory | Extension to fermionic theories |

**Follow-up papers (2025-2026 explosion):**
- arXiv:2504.14215 — Hidden zeros via BCFW recursion
- arXiv:2505.02520 — Smooth splitting and zeros from on-shell recursion
- arXiv:2506.22538 — Splitting regions and shrinking islands
- arXiv:2510.11070 — Hidden zeros for higher-derivative YM and GR at tree level (Zhou 2025): shows zeros extend to F³ operators, R², R³ insertions in gluon/graviton amplitudes; proves systematic cancellation of propagator singularities
- arXiv:2512.15882 — Differential operators for scalar-scaffolded gluons
- arXiv:2601.16860 — Hidden zeros in massive theories (Carrillo González & Ward, Jan 2026): zeros survive ONLY when mass generation is controlled by symmetry (SSB for NLSM/YM, uniform mass for Tr(φ³)); explicit mass terms destroy zeros → **zeros are a symmetry-sensitive probe, not universal**
- arXiv:2601.15088 — Five-point partial waves and hidden zeros (Jan 2026)

The explosion of follow-up papers (20+ in ~2 years) confirms this is a highly active frontier.

### Critical Constraint from Massive Theories (arXiv:2601.16860)

The massive theories paper reveals an important limitation: hidden zeros are NOT universal. They depend critically on how mass enters:
- **Tr(φ³) with uniform mass**: zeros survive (after "massive shift" of planar variables)
- **NLSM with pion mass from SSB**: zeros survive
- **NLSM with explicit mass term** (no symmetry protection): zeros DESTROYED
- **Yang-Mills with spontaneous breaking**: zeros survive
- **Yang-Mills with explicit mass** (Proca-type): zeros DESTROYED

This means hidden zeros are a feature of **symmetry-protected theories** — they probe the underlying symmetry structure. This is both a limitation (not universal) and an insight (they discriminate between symmetry-related and non-symmetry-related mass generation).
