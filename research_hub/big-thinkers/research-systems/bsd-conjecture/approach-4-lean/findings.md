# LLM-Guided Lean 4 Proof Search for BSD Rank >= 2

**Date:** 2026-04-04
**Status:** Deep survey complete. Roadmap and feasibility assessment below.
**Verdict:** Technically possible but requires 5-8 years of infrastructure building. The FLT project is the critical enabler. A focused pilot on formalizing the Euler system axioms is achievable in 1-2 years and would be the right entry point.

---

## Table of Contents

1. [The Formalization Frontier](#1-the-formalization-frontier-what-exists-in-lean-mathlib)
2. [The Proof Dependency Chain](#2-the-proof-dependency-chain-rank-1-bsd)
3. [The Rank 2 Chokepoint](#3-the-rank-2-chokepoint-what-breaks)
4. [Candidate Constructions](#4-candidate-constructions-for-rank-2)
5. [The Attack Plan](#5-the-attack-plan-llm--lean-4-proof-search)
6. [Feasibility Assessment](#6-feasibility-assessment)
7. [Concrete Roadmap](#7-concrete-roadmap)

---

## 1. The Formalization Frontier: What Exists in Lean/Mathlib

### What IS formalized (as of early 2026)

| Component | Status | Details |
|-----------|--------|---------|
| **Elliptic curves (Weierstrass model)** | Definitions + group law | WeierstrassCurve structure with a1..a6 coefficients, b/c-invariants, discriminant, j-invariant. Group law on nonsingular points proven (Angdinata 2023). Handles all characteristics. |
| **p-adic numbers** | Mature | Q_p as Cauchy completion, Z_p as subtype with norm <= 1. Hensel's lemma proven. DVR structure. p-adic L-functions partially formalized (Narayanan). |
| **Algebraic number theory basics** | Solid foundation | Finiteness of class number, Dirichlet unit theorem, Dedekind domains, class groups of global fields. |
| **Group cohomology** | Defined + basic results | H^n(G,M) via derived functors (Livingston 2023). Hilbert 90 proven. Profinite group cohomology as limit. |
| **Galois theory** | Fundamental theorem | Galois correspondence between intermediate fields and subgroups. Abel-Ruffini (one direction). |
| **Adeles and ideles** | Recently formalized | Ring of adeles of number field K, locally compact topological ring structure. Idele group. Statement of global CFT (de Frutos-Fernandez). |
| **Modular forms** | Definitions only | Modular forms and cusp forms defined, complex vector space structure. NO q-expansions, NO Hecke operators in Mathlib proper (in progress). |
| **Schemes** | Basic definitions | Prime spectrum, Zariski topology, locally ringed spaces, schemes, Nullstellensatz. |
| **Derived categories** | Formalized (Riou 2025) | D(C) for abelian category C. Triangulated structure. Foundation for sheaf cohomology. |
| **Sheaves on sites** | Definitions available | Sheaf of types on arbitrary site (Mehta). Opens door to etale cohomology. |
| **Local fields** | Basic theory | Nonarchimedean local field definition, basic properties. Extensions (2025 CFT workshop). |
| **BSD conjecture statement** | Parameterized | LeanMillenniumPrizeProblems repo has the statement but uses ClayLSeriesData package to abstract over the missing Hasse-Weil L-function construction. |

### What is NOT formalized (critical gaps for BSD)

| Component | Gap Severity | Notes |
|-----------|-------------|-------|
| **Hasse-Weil L-function** | CRITICAL | Cannot even state BSD properly without it. Requires analytic continuation (modularity). |
| **Galois representations from elliptic curves** | CRITICAL | The Tate module, l-adic representations -- not in Mathlib. |
| **Selmer groups** | CRITICAL | Zero formalization. Need exact sequences, local conditions, Tate duality. |
| **Heegner points** | CRITICAL | Nothing. Requires modular parametrization + CM theory. |
| **Modular parametrization** | CRITICAL | Modularity theorem not formalized. FLT project will eventually produce this. |
| **Euler systems** | CRITICAL | No axiomatic framework. No norm-compatibility relations. |
| **Etale cohomology** | SEVERE | Definitions possible via sites, but no theorems. No proper/smooth base change. |
| **Heights (Neron-Tate)** | SEVERE | Not formalized. Needed for BSD formula and Gross-Zagier. |
| **Tate-Shafarevich group** | SEVERE | Not defined. Sha = ker(H^1(Q,E) -> prod H^1(Q_v,E)). |
| **Iwasawa theory** | SEVERE | Not in Mathlib. Cyclotomic/anticyclotomic Z_p-extensions, main conjectures. |
| **Riemann-Roch for curves** | SEVERE | Needed for proper definition of genus, divisors on curves. |
| **Class field theory (proofs)** | MODERATE | Statement exists (de Frutos-Fernandez). Proofs in progress (2025 Oxford workshop). |

### Key Observation

The gap between "what Mathlib has" and "what BSD rank 1 needs" is enormous. We are missing essentially every component of the proof chain. However, the FLT formalization project (Buzzard, funded through 2029) is building many of the same components: Galois representations, modularity, automorphic forms, Hecke operators. The BSD effort should be designed to draft behind FLT.

---

## 2. The Proof Dependency Chain: Rank 1 BSD

The proof that BSD holds for rank <= 1 chains through these major results:

```
BSD rank 0-1
    |
    +-- Burungale-Castella-Skinner (2024)
    |     "p-part of BSD formula when ord_{s=1} L(E,s) <= 1"
    |     Proves: Iwasawa main conjecture (cyclotomic + anticyclotomic)
    |     Uses: base change, two-variable zeta element, Wan's three-variable divisibility
    |
    +-- Kolyvagin (1990)
    |     "Finiteness of Sha when analytic rank <= 1"
    |     Constructs: Euler system from Heegner points
    |     Uses: Derivative operator, local Tate duality, Chebotarev
    |     REQUIRES: One non-torsion Heegner point (analytic rank 1 case)
    |
    +-- Gross-Zagier (1986)
    |     "L'(E,1) = (height of Heegner point) * (period stuff)"
    |     Connects: Analytic rank to algebraic data
    |     Uses: Rankin-Selberg method, Shimura curves, heights
    |     REQUIRES: Modularity, Heegner point construction, analytic continuation
    |
    +-- Modularity (Wiles 1995 / Breuil-Conrad-Diamond-Taylor 2001)
    |     "Every E/Q is modular"
    |     This IS the FLT proof machinery
    |
    +-- Foundations
          - Elliptic curves over Q (group law, reduction, conductors)
          - Modular forms (Hecke eigenforms, newforms, L-functions)
          - Galois representations (Tate modules, mod-l representations)
          - Selmer groups and Tate-Shafarevich groups
          - Heights (Neron-Tate canonical height)
          - Analytic number theory (functional equation, analytic continuation)
```

### Formalization difficulty by component

| Component | Lines of math (est.) | Lean difficulty | Prerequisites |
|-----------|---------------------|-----------------|---------------|
| Elliptic curve foundations | ~2000 pages | Medium | Alg. geom. basics |
| Modularity theorem | ~500 pages (FLT route) | Extreme | Everything in FLT |
| Gross-Zagier formula | ~300 pages | Extreme | Modularity, heights, Rankin-Selberg |
| Kolyvagin's Euler system | ~150 pages | Very Hard | Galois cohomology, Selmer groups, Chebotarev |
| Burungale-Castella-Skinner | ~100 pages | Very Hard | Iwasawa theory, p-adic L-functions |

### What FLT will deliver (by ~2029)

The Buzzard FLT project explicitly plans to formalize: automorphic forms and representations, Galois representations, potential automorphy, modularity lifting theorems, class field theory, arithmetic duality theorems. This overlaps heavily with BSD needs. However, FLT does NOT need: Heegner points, Euler systems, Selmer group bounds, L-function special values, heights. These are BSD-specific.

---

## 3. The Rank 2 Chokepoint: What Breaks

### Why rank 1 works

Kolyvagin's method for rank 1:
1. Start with a Heegner point y_K in E(K) for an imaginary quadratic field K
2. If y_K has infinite order (guaranteed by Gross-Zagier when L'(E,1) != 0), then:
3. Apply derivative operators to produce "Kolyvagin classes" c(n) in H^1(Q, E[p])
4. These classes satisfy: if y_K is non-torsion, the classes c(n) bound the Selmer group
5. Result: rank E(Q) = 1 and Sha is finite

The key structural feature: ONE non-torsion point generates an entire Euler system that controls the Selmer group.

### What breaks at rank 2

**The fundamental obstruction:** Kolyvagin's machine takes ONE special point and produces cohomology classes that kill everything in the Selmer group except the one-dimensional subspace generated by that point. For rank 2, you need:

1. **Two independent special points** (or an algebraic cycle of higher dimension that replaces them)
2. **An Euler system with rank >= 2** (a compatible family in exterior powers of cohomology)
3. **A descent argument** that bounds the Selmer group to be exactly 2-dimensional

Specifically, the obstructions are:

**(A) No known rank-2 Euler system with the right properties.** Perrin-Riou defined higher-rank Euler systems using exterior powers: elements in wedge^r H^1(F, T) satisfying norm-compatibility. For r=2, you need elements in wedge^2 H^1(F, T) -- pairs of cohomology classes that are "jointly compatible" across field extensions. The rank-1 Euler systems (Heegner, Kato, Beilinson-Flach) are all r=1. Nobody has constructed an r=2 Euler system that applies to E/Q.

**(B) The Gross-Zagier formula has no rank-2 analogue.** Gross-Zagier relates L'(E,1) to a height. For rank 2, you'd need a formula relating L''(E,1) to some arithmetic invariant (a "derived height" or "arithmetic intersection number"). The Gross-Kudla conjecture relates triple product L-functions to heights of diagonal cycles, which is close but not the same thing.

**(C) Kolyvagin's descent breaks.** The rank-lowering / level-raising technique (Wei Zhang's approach) works by: if Selmer rank is r, produce an Euler system class that cuts it to r-1, iterate until r=0 or 1. But each step requires a new special element, and the existence of these elements at each step is not known beyond rank 1. Sweeting's bipartite Euler system approach reformulates this but still needs the underlying special elements.

**(D) The Iwasawa-theoretic approach stalls.** Burungale-Castella-Skinner prove the Iwasawa main conjecture (relating p-adic L-functions to Selmer groups) only when ord_{s=1} L(E,s) <= 1. The main conjecture at higher vanishing order is wide open.

### The state of the art for rank 2 (2024-2026)

The closest results:

**Castella (2022):** For CM elliptic curves E/Q with ord_{s=1} L(E,s) >= 2, constructs a "generalised Kato class" kappa_p in Sel(Q, V_pE) using Darmon-Rotger diagonal cycles. Proves: if kappa_p != 0, then dim Sel(Q, V_pE) = 2. This is a rank-2 analogue of Kolyvagin's result, but:
- Only works for CM curves (a measure-zero subset)
- The nonvanishing of kappa_p is conditional on p-adic height conditions
- Does not give the full BSD formula, only the rank part
- Does not prove finiteness of Sha for rank 2

**Darmon-Rotger (2014-2017):** Construct two linearly independent classes in the Selmer group when ord_{s=1} L(E,rho,1) >= 2 for certain Artin twists. Uses Gross-Kudla-Schoen diagonal cycles on triple products of modular curves. Conditional on nonvanishing of Garrett-Hida p-adic L-function outside interpolation range.

**Loeffler-Zerbes (2024-2025):** Construct Euler systems for GSp(4) spin representations and prove Bloch-Kato in analytic rank 0 for Asai representations. Ultra-Kolyvagin systems for non-ordinary settings. These are rank-1 Euler systems for higher-dimensional Galois representations, not rank-2 Euler systems for GL(2).

---

## 4. Candidate Constructions for Rank 2

### 4.1 Diagonal Cycles (Gross-Kudla-Schoen / Darmon-Rotger)

**Idea:** The Gross-Kudla-Schoen cycle is a modified diagonal in the triple product X x X x X of a modular curve. Its Abel-Jacobi image lands in H^1 of a triple tensor product of Galois representations. When one factor specializes to the Galois representation of E, the cycle produces classes in the Selmer group.

**Current status:** Darmon-Rotger produced explicit classes. Castella proved the rank-2 implication for CM curves. The "diagonal cycle Euler system" satisfies Euler-system-like compatibility but lives in the wrong cohomology (triple product, not just E).

**What's needed for BSD rank 2:**
- Remove the CM hypothesis from Castella's result
- Prove unconditional nonvanishing of the generalised Kato class
- Develop a "derived height" pairing that computes L''(E,1)
- Prove the full three-variable Iwasawa main conjecture

**Lean formalization challenge:** HIGH. Requires: triple products of modular curves, p-adic Abel-Jacobi maps, Hida families, p-adic L-functions.

### 4.2 Beilinson-Flach Elements (Bertolini-Darmon-Rotger / Kings-Loeffler-Zerbes)

**Idea:** Motivic classes in K-theory of products of modular curves. Related to but different from diagonal cycles. Produce Euler systems for Rankin-Selberg convolutions.

**Current status:** Loeffler-Zerbes have a mature theory for GL(2) x GL(2). They proved Bloch-Kato in analytic rank 0 for Rankin-Selberg convolutions. Universal Euler systems for GSp(4).

**Rank 2 relevance:** The Beilinson-Flach Euler system is rank 1. To get rank 2, you'd need to take exterior squares or find a genuinely rank-2 variant. Not currently known.

**Lean formalization challenge:** VERY HIGH. Same issues as diagonal cycles plus K-theory.

### 4.3 Higher Rank Euler Systems (Perrin-Riou / Burns-Sano / Sakamoto)

**Idea:** Abstractly, a rank-r Euler system is a collection of elements in wedge^r H^1(F, T) satisfying norm-compatibility. Burns-Sano developed the theory for the multiplicative group Gm. Sakamoto constructed a higher rank Euler system for Gm over totally real fields.

**Current status:** The abstract machinery exists. Concrete examples for elliptic curves at rank 2 do not.

**Rank 2 relevance:** DIRECT. If someone could construct explicit elements in wedge^2 H^1(F, T_pE) satisfying the Euler system axioms, the descent machinery of Burns-Sano would (in principle) bound the Selmer group.

**Lean formalization challenge:** The ABSTRACT axiomatics are the most formalizable part of this entire enterprise. The axioms for a rank-r Euler system are purely algebraic.

### 4.4 Stark-Heegner Points (Darmon)

**Idea:** p-adic analytic construction of points on elliptic curves using p-adic integration on Hp x H (product of p-adic and complex upper half planes). Conjectural: these should be rational points, but this is unproven.

**Status:** The rationality conjecture for Stark-Heegner points is wide open. Even if proven, they only give one additional point, not a rank-2 Euler system.

**Lean relevance:** Low priority. The construction is analytic and conjectural.

### 4.5 Kudla-Rapoport Special Cycles

**Idea:** Arithmetic intersection theory on unitary Shimura varieties. The Kudla-Rapoport conjecture (proven by Chao Li, 2019) relates intersection numbers of special cycles to derivatives of Eisenstein series Fourier coefficients.

**Rank 2 relevance:** The arithmetic Siegel-Weil formula connects these to central derivatives of L-functions. In principle, higher-codimension cycles could encode higher-order vanishing.

**Lean formalization challenge:** EXTREME. Requires Shimura varieties, arithmetic intersection theory, and the full Kudla program.

---

## 5. The Attack Plan: LLM + Lean 4 Proof Search

### 5.1 What the LLM would actually search for

The core insight: the rank-2 obstruction is a CONSTRUCTION problem, not (primarily) a verification problem. We need to FIND an object satisfying known axioms. This is where LLM-guided search could help.

**Target object:** A rank-2 Euler system for the Tate module T = T_p(E) of an elliptic curve E/Q.

**Type signature in pseudo-Lean:**

```lean
/-- A rank-2 Euler system for a p-adic Galois representation T -/
structure EulerSystemRank2 (T : GaloisRepresentation Q_p) where
  /-- For each square-free integer m coprime to some conductor N,
      a class in the exterior square of cohomology -/
  classes : (m : SquareFreeNat) -> ExteriorPower 2 (H1_Gal (CyclotomicField m) T)

  /-- Norm compatibility: for primes l dividing m,
      the norm from Q(zeta_m) to Q(zeta_{m/l}) relates classes
      via the Euler factor at l -/
  norm_compat : forall (m : SquareFreeNat) (l : Prime) (h : l | m),
    norm_map (classes m) =
      euler_factor T l * classes (m / l)

  /-- Local conditions: at primes dividing m,
      the classes satisfy prescribed local behavior -/
  local_conditions : forall (m : SquareFreeNat) (v : Place),
    satisfies_local_condition (classes m) v

  /-- Non-triviality: the base class is nonzero -/
  nontrivial : classes 1 != 0
```

**Verification conditions Lean would check:**
1. The classes are well-defined elements of the right cohomology groups
2. Norm-compatibility relations hold (algebraic identities)
3. Local conditions are satisfied (controlled by representation theory data)
4. The Euler factors match the L-function data
5. The descent argument actually produces the right Selmer bound

### 5.2 Search strategy

**Phase 1: Axiom formalization (no search needed)**
Formalize the abstract definition of rank-r Euler systems in Lean 4. This is well-defined mathematics (Perrin-Riou, Burns-Sano). The type signatures create a well-typed search target.

**Phase 2: Known construction encoding**
Formalize the known rank-1 Euler systems as instances:
- Cyclotomic units (for Gm)
- Kato's Euler system (for modular forms)
- Heegner point Euler system (for E/Q over anticyclotomic towers)
- Beilinson-Flach elements (for GL2 x GL2)

This creates training data: the LLM sees what valid Euler systems look like.

**Phase 3: LLM-guided construction search**
Use LLM proof search to explore modifications of known constructions:
- "What if we take the exterior square of the Beilinson-Flach construction?"
- "What if we use diagonal cycles in a different configuration?"
- "What if we compose two rank-1 Euler systems?"

The LLM proposes constructions. Lean checks whether they satisfy the axioms. The search space is:
- Source geometry: products of modular curves, Shimura varieties, Hilbert modular surfaces
- Algebraic cycles: pushforwards, pullbacks, correspondences, modified diagonals
- Euler factors: determined by local representation theory
- Local conditions: Bloch-Kato, balanced, relaxed, strict

**Phase 4: Descent verification**
If a candidate rank-2 Euler system is found, the LLM + Lean system verifies the descent argument that bounds the Selmer group.

### 5.3 What LLM capabilities are needed

| Capability | Current state | Gap |
|-----------|--------------|-----|
| Lean tactic generation | 85% of Mathlib steps (Lean Copilot) | Adequate for verification |
| Novel construction proposal | Weak at research-level math | Main bottleneck |
| Algebraic identity verification | Strong (ring tactic, Grobner) | Adequate |
| Type-checking proposed objects | Lean handles this | No gap |
| Long-horizon planning | Improving (DeepSeek-Prover-V2 subgoal decomposition) | Needs further work |
| Domain knowledge (arithmetic geometry) | Trained on papers but not proofs | Significant gap |

### 5.4 Why this approach has a chance

1. **The search space is constrained.** Euler systems aren't arbitrary -- they come from algebraic geometry. The source objects (cycles on Shimura varieties) form a discrete, structured search space.

2. **Verification is (relatively) cheap.** Checking norm-compatibility is a computation. Lean can do it.

3. **The axioms are known.** We know WHAT we're looking for. We don't know WHERE to find it.

4. **Incremental value.** Even partial constructions (satisfying some but not all axioms) would be publishable and would narrow the search.

5. **The FLT project creates infrastructure.** By 2029, much of the heavy Lean infrastructure will exist.

---

## 6. Feasibility Assessment

### 6.1 Infrastructure timeline

| Milestone | Dependency | Estimated date | Confidence |
|-----------|-----------|----------------|------------|
| Group cohomology H^n in Mathlib | Done (Livingston 2023) | DONE | -- |
| Derived categories in Mathlib | Done (Riou 2025) | DONE | -- |
| Galois representations from E/Q | FLT project | 2027-2028 | Medium |
| Modular forms (Hecke operators, q-exp) | FLT project | 2027 | Medium |
| Selmer groups defined | Needs Tate duality + local conditions | 2028 | Low-Medium |
| Euler system axioms (abstract) | Group cohomology + algebra | 2026-2027 | HIGH |
| Rank-1 Euler system examples | Selmer groups + L-functions | 2029-2030 | Low |
| Class field theory (proofs) | 2025 Oxford workshop + ongoing | 2027-2028 | Medium |
| Etale cohomology | Derived categories + sites | 2028-2030 | Low |
| Heights (Neron-Tate) | Elliptic curves over number fields | 2028 | Medium |
| Heegner points | Modularity + CM theory + heights | 2030+ | Low |
| Gross-Zagier formula | Everything above | 2032+ | Very Low |
| Rank-2 Euler system construction | Everything + novel math | Unknown | Speculative |

### 6.2 Honest assessment

**Is this a 1-year or 10-year project?**

It depends on what "this" means:

- **Formalizing Euler system axioms in Lean 4:** 1-2 years. Achievable now. Pure algebra over group cohomology (which exists). This should be the FIRST milestone.

- **Formalizing known rank-1 Euler systems:** 5-7 years. Requires FLT infrastructure. Will happen as a natural byproduct of the broader formalization movement.

- **Using LLM search to find rank-2 Euler systems:** 8-15 years minimum before the search space is formally representable in Lean. But: informal/semi-formal search (LLM proposes, human checks, Lean verifies pieces) could start in 3-5 years.

- **A complete formal proof of BSD rank 2:** This is a "century problem" level aspiration. Even if the mathematics is discovered tomorrow, formalizing it would take a decade.

### 6.3 What could accelerate this

1. **FLT project succeeds on schedule (2029).** This is the single biggest accelerator. It delivers Galois representations, modularity, automorphic forms.

2. **LLM provers get dramatically better.** DeepSeek-Prover-V2 solves ~49/658 Putnam problems. If this reaches ~500/658 by 2028, the verification bottleneck drops.

3. **A mathematician discovers the rank-2 Euler system.** If someone constructs it on paper, the formalization becomes "merely" a formalization project (hard but tractable).

4. **Modular Lean infrastructure.** If the community builds Selmer groups, Euler system axioms, and descent machinery as reusable Lean libraries, many research groups could search in parallel.

### 6.4 Risks

- **The rank-2 Euler system might not exist in any "nice" form.** Maybe the rank-2 case requires fundamentally different techniques (derived categories, motivic cohomology, homotopy-theoretic methods) that are even further from formalization.

- **The FLT project could stall.** It's ambitious and depends on sustained funding and community effort.

- **LLM provers might plateau.** Current progress is impressive but is driven by competition-level problems. Research-level math is qualitatively different.

- **The search space might be too large.** Even with type-checking, the space of candidate constructions in algebraic geometry is enormous.

---

## 7. Concrete Roadmap

### Phase 0: Foundation (2026 -- Now)
**Goal:** Formalize the abstract axiomatics of Euler systems in Lean 4.

Tasks:
- [ ] Define `EulerSystem` structure parameterized by:
  - A p-adic Galois representation T
  - A set of "admissible" primes Sigma
  - A rank r (defaulting to 1)
- [ ] State the norm-compatibility axiom using existing Mathlib group cohomology
- [ ] State the local condition axioms
- [ ] Prove: "an Euler system of rank r bounds the Selmer group to have corank <= r" (the abstract descent theorem, following Rubin's formulation)
- [ ] Formalize Perrin-Riou's exterior power definition for higher rank

**Lean infrastructure needed:** Group cohomology (DONE), exterior powers of modules (DONE in Mathlib), basic Galois theory (DONE).

**Estimated effort:** 1 person-year. An expert Lean formalization researcher could do this.

### Phase 1: Examples (2027-2029)
**Goal:** Formalize at least one rank-1 Euler system as an instance.

Target: Cyclotomic units for Gm (simplest known Euler system).

Tasks:
- [ ] Define cyclotomic units in Lean
- [ ] Verify they satisfy the Euler system axioms
- [ ] State and prove Rubin's theorem: cyclotomic ES => Selmer bound for Gm (= class number formula direction)

**Lean infrastructure needed:** Cyclotomic fields (partially in Mathlib), units, class groups (DONE), Kummer theory.

**Estimated effort:** 2-3 person-years. Requires someone who knows both Iwasawa theory and Lean.

### Phase 2: Selmer Infrastructure (2028-2030)
**Goal:** Build the Selmer group machinery in Lean.

Tasks:
- [ ] Define Selmer groups as kernels of localization maps
- [ ] Formalize Tate local duality
- [ ] Formalize Poitou-Tate exact sequence
- [ ] Define Bloch-Kato Selmer groups
- [ ] Connect to Euler system descent machinery from Phase 0

**Lean infrastructure needed:** Galois cohomology of local fields (partially from FLT/CFT projects), completions, Tate module of E.

**Estimated effort:** 3-4 person-years. This is a major infrastructure project.

### Phase 3: LLM Search Setup (2029-2031)
**Goal:** Create a Lean environment where candidate rank-2 constructions can be type-checked.

Tasks:
- [ ] Axiomatize the "source" objects: algebraic cycles on products of Shimura varieties
- [ ] Define the "output" map: cycle -> cohomology class -> Euler system class
- [ ] Build a "construction template" that an LLM can fill in:
  - Choose a geometric setting (triple product, Hilbert modular surface, etc.)
  - Choose a cycle (diagonal, special cycle, correspondence)
  - Specify norm-compatibility proof strategy
- [ ] Train/fine-tune an LLM on the formalized examples from Phases 0-2
- [ ] Run search: LLM proposes, Lean checks

**Estimated effort:** 2-3 person-years + compute.

### Phase 4: Attack (2031+)
**Goal:** Search for rank-2 Euler system constructions.

This is the speculative part. By this point:
- Lean has the abstract framework
- At least one rank-1 example is formalized
- Selmer groups and descent are operational
- LLM provers are (hopefully) substantially better than today

The search targets, in order of plausibility:
1. Exterior square of Beilinson-Flach elements
2. Generalized Kato classes (Castella's construction, extended beyond CM)
3. Diagonal cycle Euler system (Darmon-Rotger, checked for rank-2 compatibility)
4. Novel construction from Kudla-Rapoport special cycles
5. Completely new construction suggested by LLM exploration

---

## Appendix A: Key References

### Rank 1 proof chain
- Gross-Zagier, "Heegner points and derivatives of L-series" (1986)
- Kolyvagin, "Euler systems" (1990)
- Burungale-Castella-Skinner, "Base change and Iwasawa main conjectures for GL2" (2024)

### Rank 2 candidates
- Darmon-Rotger, "Diagonal cycles and Euler systems I, II" (2014-2017)
- Castella, "Generalised Kato classes on CM elliptic curves of rank 2" (2022)
- Loeffler-Zerbes, "A universal Euler system for GSp(4)" (2024)
- Loeffler-Zerbes, "Ultra-Kolyvagin systems and non-ordinary Selmer groups" (2025)
- Sweeting, "Kolyvagin's conjecture, bipartite Euler systems, and higher congruences" (2023)

### Higher rank Euler system theory
- Perrin-Riou, "Systemes d'Euler p-adiques et theorie d'Iwasawa" (1998)
- Burns-Sano, "On the theory of higher rank Euler, Kolyvagin and Stark systems" (2020)
- Sakamoto, "A higher rank Euler system for Gm over a totally real field" (2020)

### Lean/formalization
- Angdinata, "An elementary formal proof of the group law on Weierstrass elliptic curves" (2023)
- Livingston, "Group cohomology in the Lean community library" (2023)
- Riou, "Formalization of derived categories in Lean/Mathlib" (2025)
- de Frutos-Fernandez, "Formalizing the ring of adeles" (2022, 2025)
- Narayanan, "Formalization of p-adic L-functions in Lean 3" (2023)
- Buzzard et al., "Towards a Lean proof of Fermat's Last Theorem" (2024-ongoing)
- LeanMillenniumPrizeProblems, "BSD conjecture statement (parameterized)" (2025)

### LLM theorem proving
- Lean Copilot (2024): 74.2% proof step automation
- DeepSeek-Prover-V2 (2025): 88.9% on MiniF2F-test
- APOLLO (2025): 84.9% on MiniF2F with sub-8B params
- AlphaProof (2024): IMO silver medal level

---

## Appendix B: The Mathematical Heart of the Problem

For the reader who wants the precise obstruction:

Let E/Q be an elliptic curve with ord_{s=1} L(E,s) = 2. BSD predicts rank E(Q) = 2.

**What we can currently prove:** Almost nothing unconditionally.

**What Castella proved (for CM curves):** If kappa_p != 0, then dim Sel(Q, V_pE) = 2, where kappa_p is a generalised Kato class constructed from p-adic families of diagonal cycles. The nonvanishing of kappa_p is equivalent to: (a) the Selmer group is 2-dimensional, AND (b) the restriction to E(Q_p) tensor Q_p is nonzero.

**What's missing for full BSD rank 2:**
1. An UNCONDITIONAL construction of two linearly independent elements of the Selmer group (or proof that E(Q) has rank >= 2)
2. An UPPER bound on the Selmer group (showing rank <= 2)
3. Finiteness of Sha
4. The exact leading coefficient formula: L''(E,1)/2 = |Sha| * Reg * Omega * prod(c_p) / |E(Q)_tors|^2

The rank-2 Euler system, if it exists, would give (2) and (3). A rank-2 Gross-Zagier formula would give (1) and connect to (4).

**The LLM's job:** Find the object that gives (2) and (3). The type signature is known. The construction is not.

---

## Appendix C: Comparison with Other AI-Math Approaches

| Approach | What it does | BSD relevance |
|----------|-------------|---------------|
| AlphaProof | RL + Lean for competition math | Infrastructure, not BSD-specific |
| DeepSeek-Prover | LLM + MCTS for Lean | Could generate tactic proofs once framework exists |
| Lean Copilot | Interactive proof assistance | Would help human formalizers |
| Autoformalization | Math text -> Lean | Could help encode papers into Lean |
| This proposal | Targeted construction search | Directly attacks the missing object |

The key difference: existing AI theorem provers solve KNOWN problems. This proposal would search for UNKNOWN mathematical objects. That requires the formalization framework to serve as a SPECIFICATION, not just a verification tool.
