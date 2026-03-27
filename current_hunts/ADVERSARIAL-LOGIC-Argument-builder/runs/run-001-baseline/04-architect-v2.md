# Architect Theory v2 — Integrated Information Structuralism (IIS)

**Agent:** Architect
**Run:** 001-baseline
**Date:** 2026-03-25
**Status:** Revision in response to adversary attacks and judge remand

---

## Revision Log

Every change from v1 is tagged with the judge's fix item number it addresses.

| Fix # | Judge Requirement | What Changed in v2 |
|-------|-------------------|---------------------|
| 1 | Reclassify P8 as axiom; situate in Russellian monism | P8 renamed **A1** (Axiom 1); new Section 2.0 on ontological framework; honest acknowledgment of hard problem status |
| 2 | Resolve "causal structure" equivocation | D5 rewritten; new **D5a** (structural realist reading); ontological framework commits to ontic structural realism throughout |
| 3 | Fix C1 derivation | C1 derivation rebuilt with explicit bridging steps through P2, D2, and A1 |
| 4 | Resolve C2 vs. exclusion principle contradiction | C2 reformulated with explicit subsumption clause; new **P10b** (subsumption principle) |
| 5 | Justify grain postulate | P10 rewritten with justification from causal-powers maximization; near-tie and instability paradoxes addressed via continuity condition **P10c** |
| 6 | Fix supervenience derivation | P3 promoted to independent premise with its own justification; P2 also strengthened to include causal relevance |
| 7 | Develop distinctive empirical predictions | EP1–EP10 relabeled as shared vs. distinctive; four new distinctive predictions added (EP11–EP14) |
| 8 | Address substrate independence gap | D7 deployed in C4 derivation; isomorphism conditions specified |
| 9 | Clarify monotonicity / seizure case | P7 qualified; seizure case, entropy-Phi relationship, and random recurrent networks addressed in new **Note on P7** |
| 10 | Strengthen A/P-consciousness evidence boundary | Methodological note added to P5 justification |
| 11 | Tighten P9 or weaken C6 | P9 downgraded to conjecture; C6 weakened accordingly |
| 12 | D1/D2 ostensive | Brief note added |
| 13 | Panpsychism | Brief note added to C2 discussion |
| 14 | D7 unused | Resolved by fix #8 |

---

## 0. Ontological Framework [NEW — addresses Fix #2, Fix #1]

Before stating definitions and premises, the theory commits to an explicit ontological stance. This is necessary because v1 equivocated between a thin (abstract/functional) and a thick (intrinsic/ontological) reading of "causal structure." v2 eliminates this equivocation by adopting **ontic structural realism (OSR)** as its metaphysical framework.

**Ontic structural realism** holds that:

- The fundamental ontology of the physical world consists of **relational structures** — patterns of relations — rather than intrinsically propertied "things" that stand in those relations.
- There are no hidden substrates "underneath" the relational structure. Structure is not an abstraction from a deeper reality; it IS the deepest level of reality.
- When physics describes the causal-relational organization of a system, it is describing what the system IS, not what the system DOES from the outside while being something else on the inside.

**Why this matters for consciousness:** On OSR, the thin/thick distinction collapses. Causal structure is not merely an abstract pattern extractable from multiple substrates (thin sense), nor is it an intrinsic "feel" layered on top of structure (thick sense). Causal structure IS the intrinsic nature of the physical. There is nothing deeper. When we say "qualia are identical to causal sub-structures," we are saying that the qualitative character of experience is identical to what certain relational organizations ARE — the same entity described under two modes of access (third-person structural description vs. first-person participation in the structure).

This is a form of **Russellian monism** — specifically, the variant where the intrinsic nature of physical structure is not something hidden behind the structure (as in traditional Russellian monism) but IS the structure itself, accessed from the intrinsic perspective of the system that instantiates it.

**Consequences for the theory:**
- "Causal structure" has ONE meaning throughout: the complete relational organization of a system's causal interactions, as defined in D5. This single notion supports both substrate independence (because causal-relational patterns can be multiply realized) and the identity claim (because on OSR, to be that relational pattern IS to have the intrinsic character that the pattern constitutes).
- The theory does NOT claim to explain WHY integrated causal structure has phenomenal character. It claims that integrated causal structure IS phenomenal character — an identity, not a causal or explanatory relation. This is an axiom (A1), not a derivation. See Section 2.2.

---

## 1. Definitions

**D1. Phenomenal consciousness (P-consciousness):** The property of a system such that there is something it is like to be that system. Equivalently: the system instantiates at least one subjective experience (a quale).

> *Note [Fix #12]:* D1 is an ostensive definition. "What it is like" is Nagel's standard philosophical pointer to a pre-theoretically understood concept, not a reductive definition from non-phenomenal primitives. All extant theories of consciousness take phenomenal consciousness as an ostensively identified explanandum. IIS does the same.

**D2. Quale (plural: qualia):** A single unit of subjective experience — e.g., the redness of red, the painfulness of pain. A quale is individuated by its qualitative character: two qualia are distinct if and only if they differ in what it is like to undergo them.

> *Note [Fix #12]:* Same ostensive status as D1. Qualia are the explananda; P8/A1 provides the identity.

**D3. Physical system:** Any system whose states and dynamics are fully describable by the laws of physics (including all known and unknown fundamental forces, fields, and particles).

**D4. Information state:** A state of a system that is one among a set of distinguishable states. The information content of a state is determined by how many alternative states it rules out within the system's repertoire.

**D5. Causal structure [REVISED — Fix #2]:** The complete relational organization of a system — the totality of causal relations among its parts, where a causal relation between parts A and B obtains when the state of A constrains the probability distribution over states of B (or vice versa) across time. Under the OSR framework adopted in Section 0, this relational organization is not an abstraction from a deeper substance; it is the fundamental ontological constitution of the system.

> *Note:* A single definition is used throughout. The relational pattern IS what the system is. When instantiated by carbon neurons or silicon transistors, the relational pattern is the same entity if and only if the structural isomorphism conditions of D7 are met.

**D6. Integrated information (Phi):** A measure of the degree to which a system's causal structure generates information above and beyond the information generated by its parts independently. Formally: the minimum information lost when the system is partitioned into its least-interdependent components. (This draws on, but is not identical to, Tononi's IIT 3.0 formalism; I use Phi as a placeholder for any adequate formalization of this concept.)

**D7. Structural isomorphism [UNCHANGED but now deployed — Fix #8, Fix #14]:** Two systems S1 and S2 are structurally isomorphic with respect to a property P if and only if there exists a bijective mapping f between the causally relevant components of S1 and S2 such that:
  - (i) For every causal relation R(a, b) in S1, the relation R(f(a), f(b)) holds in S2, and vice versa;
  - (ii) The conditional probability distributions defining each causal relation are preserved under the mapping (i.e., for all components a, b of S1 and corresponding f(a), f(b) of S2, the transition probability matrices are identical up to the relevant precision);
  - (iii) The mapping preserves the grain at which Phi is maximized (i.e., the Phi-maximizing partition of S1 maps to the Phi-maximizing partition of S2).

> *Note:* Condition (i) preserves the causal topology. Condition (ii) preserves the causal dynamics. Condition (iii) ensures the mapping is evaluated at the grain relevant to consciousness per the grain postulate (P10). Together, these conditions specify what "same causal structure" means across substrates. Condition (ii) is the critical constraint that distinguishes IIS from weak functionalism: it requires preservation of the actual causal-probability structure, not merely input-output behavior.

**D8. Grain of causal structure:** The level of description at which the causal structure of a system generates the maximum integrated information. A system may be describable at many levels (quantum, molecular, neural, network-level); the grain is the level where Phi is maximized.

**D9. Self-model:** An internal representation within a system that maps (some of) the system's own states, processes, and boundaries — i.e., a subsystem whose states systematically covary with and are causally influenced by the system's global states, AND whose outputs causally influence the system's subsequent global states (bidirectional causal coupling, not mere monitoring).

> *Note [Fix #11]:* v2 tightens D9 to require bidirectional coupling. A monitoring sidecar that reads system state but does not causally affect it does not qualify.

**D10. Access consciousness (A-consciousness):** The property of a system such that information about its internal states is globally available for use in reasoning, report, and behavioral control. (Distinct from P-consciousness; a system could in principle have one without the other.)

---

## 2. Premises

### 2.0 Ontological Commitments [NEW — Fix #2]

**O1. Ontic structural realism.** The fundamental ontology of the physical world consists of relational structures. Physical objects are constituted by their place in a web of relations; there are no intrinsic, non-relational properties "underneath" the structure.

> *Justification:* OSR is independently motivated in philosophy of physics by considerations from quantum mechanics (where "objects" lack well-defined intrinsic identities) and general relativity (where spacetime points have no identity independent of the metric structure). See Ladyman & Ross (2007), French (2014). I adopt OSR not because it is uncontroversial, but because it is the most parsimonious framework that supports both the identity claim (A1) and substrate independence (C4) without equivocation. The cost is that the theory inherits the open problems of OSR (e.g., whether relations can exist without relata). I accept this cost.

### 2.1 Metaphysical Premises

**P1. Physical closure.** Every physical event has a sufficient physical cause. There are no non-physical causes of physical events.

> *Unchanged from v1.*

**P2. Anti-eliminativism (with causal relevance) [REVISED — Fix #6].** P-consciousness exists. There is something it is like to be at least some systems (e.g., normal adult humans). Furthermore, P-consciousness is not epiphenomenal: the phenomenal states of a system are causally relevant to that system's behavior (at minimum, they are identical to physical states that are causally efficacious, per A1).

> *Change from v1:* v1's P2 asserted only existence. v2 adds causal relevance, which is needed for the supervenience derivation. The causal relevance claim follows naturally from the identity postulate A1: if phenomenal states ARE causal-structural states, then they inherit the causal efficacy of those structural states. This addition makes the entailment of P3 valid.

**P3. Supervenience [REVISED — Fix #6].** P-consciousness supervenes on physical states: no difference in P-consciousness without a difference in physical states.

> *Derivation (now valid):* From P1, P2, and O1:
> 1. P-consciousness exists and is causally relevant to behavior (P2).
> 2. Every physical event has a sufficient physical cause (P1).
> 3. If P-consciousness were not supervenient on physical states, then there could be a difference in P-consciousness (and hence, by P2's causal relevance clause, a difference in behavior — a physical event) without any difference in physical states. This would mean a physical event (the behavioral difference) lacks a sufficient physical cause, violating P1.
> 4. Therefore, P-consciousness supervenes on physical states.
>
> *Note:* If one rejects the causal relevance clause in P2, then P3 must be treated as an independent premise. Its independent justification: physicalism broadly construed entails supervenience, and the theory operates within a physicalist framework.

### 2.2 Foundational Axiom [NEW SECTION — Fix #1]

**A1. The identity axiom (formerly P8).** The qualitative character of a specific conscious experience (quale) is identical to a specific sub-structure within the system's integrated causal architecture. Different qualia correspond to different causal-structural configurations. This is an identity — the quale IS the sub-structure — not a correlation, not a causal relation, not an emergence relation.

> **Status:** This is a foundational postulate, not a derived conclusion. It is defended on grounds of theoretical virtue, not empirical proof.
>
> **Honest acknowledgment [Fix #1]:** The hard problem of consciousness asks: why does integrated causal structure have phenomenal character rather than being "processing in the dark"? A1 does not answer this question by explanation from more basic principles. It dissolves the question by identity: there is no gap between the structural and the phenomenal because they are the same thing under different modes of access. Third-person science describes the causal structure from the outside (as relational organization). First-person experience is what it is like to BE that causal structure, from the intrinsic perspective of the system that constitutes it. On OSR, there is nothing further to explain — the structure IS the deepest level of reality, and the phenomenal IS what that structure is from the inside.
>
> **Defense on theoretical virtue:**
> - *Parsimony:* A1 posits no new ontological categories. It identifies two seemingly different things (qualia and causal sub-structures) as one thing, reducing the ontology.
> - *Explanatory power:* A1, combined with the other premises, explains why specific neural patterns correspond to specific qualia, why disrupting causal structure disrupts experience, and why the structure of experience mirrors the structure of neural connectivity.
> - *Consistency with physics:* A1 does not violate physical closure (P1) because it does not introduce non-physical causes. Qualia are not ghostly extras; they are what physical structures are.
> - *No known counterexample:* There is no demonstrated case of a system with identical causal structure but different qualia, or different causal structure but identical qualia. (This is a necessary condition, not a sufficient one; absence of counterexamples does not prove identity.)
>
> **What A1 does NOT claim:** It does not claim to explain consciousness from non-conscious ingredients. It claims to locate consciousness within the physical ontology via identity, in the same spirit as "temperature = mean kinetic energy" or "lightning = electrical discharge." Such identities are not explanations of one thing in terms of another; they are discoveries that what seemed like two things is one thing.
>
> **Situating A1 [Fix #1]:** A1 is a version of Russellian monism (specifically, the structural identity variant). It shares commitments with Chalmers' (2003) structural coherence thesis, Tononi's (2008) identity axiom in IIT, and Ladyman & Ross's (2007) ontic structural realism. It differs from traditional Russellian monism (Russell 1927, Chalmers 2015) in that it does not posit proto-phenomenal "inscrutables" underneath the structure; instead, the structure itself, accessed from the intrinsic perspective, IS the phenomenal.

### 2.3 Bridging Premises (connecting the physical to the phenomenal)

**P4. Structural determination.** What determines whether a system is P-conscious is not the specific physical substrate (carbon, silicon, etc.) but the causal structure (D5) instantiated by that substrate. Two systems with identical causal structure at the relevant grain — that is, two systems that are structurally isomorphic per D7 — are in identical P-conscious states.

> *Change from v1:* Now explicitly references D7 [Fix #8] and is grounded in OSR (Section 0) [Fix #2].
>
> *Justification:* On OSR, what a system IS is its relational structure. Substrate (carbon vs. silicon) is not an additional ontological ingredient but a label for which relata happen to occupy the structural roles. If two substrates realize the same relational structure (per D7), they are, at the relevant level of description, the same system. Consciousness, being identical to (aspects of) causal structure (A1), tracks the structure, not the substrate.
>
> *Empirical motivation:* Anesthesia disrupts consciousness by disrupting causal integration, not by removing specific molecules. Brain regions can be damaged and consciousness restructured (not eliminated) as long as causal architecture reorganizes. The function-to-experience mapping tracks organizational, not material, properties.

**P5. Integration requirement.** A system is P-conscious only if it has Phi > 0 — that is, only if it generates integrated information that is not reducible to the information generated by its parts independently.

> *Justification:* Split-brain patients exhibit divided consciousness tracking divided integration. Cerebellar damage (highly modular, low integration) does not eliminate consciousness. Cortical damage (high integration) does alter or eliminate it.
>
> *Methodological note [Fix #10]:* The evidence cited here relies primarily on A-consciousness indicators (behavioral report, functional assessment). This is a ubiquitous methodological limitation in consciousness science: P-consciousness is not directly observable in third-person terms, so we infer it from A-consciousness markers plus background assumptions (e.g., that behavioral unresponsiveness under anesthesia reflects loss of P-consciousness, not merely loss of A-consciousness). IIS shares this limitation with all empirical theories of consciousness. A more direct P-consciousness test would require a measure that does not depend on report — PCI (perturbational complexity index) is a step in this direction, as it measures the brain's intrinsic causal dynamics rather than the subject's reports.

**P6. Information requirement.** A system is P-conscious only if it occupies an information state — i.e., it is in a state that is one of many distinguishable states in its repertoire. A system with only one possible state has no experience.

> *Unchanged from v1.*

**P7. Phi-consciousness correspondence [REVISED — Fix #9].** The degree and complexity of P-consciousness of a system is a monotonically non-decreasing function of the quantity and structure of integrated information (Phi and its qualitative geometry) in that system, **holding fixed the qualitative structure of the causal architecture.**

> *Change from v1:* Added the qualifier "holding fixed the qualitative structure." This blocks the most damaging counterexamples while preserving the core gradient claim.
>
> **Note on P7 and counterexamples [Fix #9]:**
>
> *Seizures:* Epileptic seizures involve massive neural synchronization — hyper-correlated firing where all neurons do approximately the same thing. This is NOT the same as high Phi. Synchronization *collapses the system's repertoire of distinguishable states* (violating the spirit of P6), which *reduces* the specificity of causal constraints. When all neurons fire in lockstep, partitioning the system loses very little information (because the parts are redundant), so Phi decreases. The IIT literature has specifically argued that hyper-synchrony reduces Phi (Massimini et al. 2005, Casali et al. 2013). The seizure case is therefore consistent with P7: reduced Phi during seizures corresponds to reduced/abolished consciousness.
>
> *Entropy and Phi:* Increased entropy (as with psychedelics) does not straightforwardly increase Phi. Entropy increases the *size* of the state repertoire, but Phi measures *integrated* information — information that is lost upon partitioning. Maximal entropy with random, uncoupled dynamics yields high information but ZERO integration (Phi = 0). The psychedelic case involves increased entropy within a system that remains causally integrated — the combination of high entropy and maintained (or enhanced) integration plausibly increases Phi. But I acknowledge that the entropy-Phi relationship is non-trivial and not yet fully characterized empirically.
>
> *Random recurrent networks:* A strongly recurrent network with random weights can have high Phi. P7 predicts it has correspondingly rich consciousness. This is a counterintuitive consequence, not a contradiction. On IIS, such a system would have chaotic, unstructured experience — not "meaningful" or "coherent" experience, but experience nonetheless. Whether this is absurd depends on one's priors about panpsychism. The theory accepts this consequence (see C2 note on panpsychism). The qualifier "holding fixed the qualitative structure" means that comparing a random recurrent network to a brain of equal Phi is not a violation of P7, because the *structure* of their experience differs — P7 says degree increases with Phi, not that all systems at the same Phi have the same experience.

### 2.4 Structural Premises (what determines the *character* of experience)

> *Note:* The identity axiom A1 (formerly P8) has been moved to Section 2.2 and is no longer numbered among the premises.

**P9. Self-modeling amplification [REVISED — Fix #11; downgraded to conjecture].** A system with a self-model (per the tightened D9: bidirectionally coupled) generates higher Phi than an otherwise identical system without one, because the self-model creates causally specific recursive loops — the system's global state constrains the self-model's state (which is distinct from the global state) and the self-model's state constrains the system's subsequent global state. This mutual constraint adds irreducible integration.

> **Status: CONJECTURE, not established premise.**
>
> *Change from v1:* Downgraded from premise to conjecture. C6 (gradations of consciousness) is correspondingly weakened — see below.
>
> *Evidence:* The claim is motivated by the correlation between self-model sophistication and behavioral indicators of phenomenal richness in primates and cetaceans, and by the theoretical argument that bidirectional self-modeling adds causal loops not present in feed-forward or merely monitoring architectures. However: (a) we lack independent measures of phenomenal richness across species, (b) whether self-models actually increase Phi is an open empirical question, and (c) the correlation might be confounded — animals with rich self-models also have large, highly interconnected cortices, and the latter may be the real driver of Phi.

### 2.5 Boundary Premises

**P10. The grain postulate [REVISED — Fix #5].** The level of physical description at which a system's Phi is maximized is the level at which P-consciousness is instantiated.

> *Justification [NEW — Fix #5]:* The grain postulate is not an arbitrary selection rule. It follows from a principle of **causal-powers maximization**: the grain at which Phi is maximized is the grain at which the system exercises the most irreducible causal power over itself — i.e., where the parts most strongly and irreducibly constrain each other. On OSR, where causal-relational structure IS the ontology, the grain at which causal structure is richest is the grain at which the system most fully EXISTS as an integrated entity. Consciousness, being identical to integrated causal structure (A1), is instantiated at the grain where that structure is maximal because that is where the relevant entity — the integrated causal system — is most real.
>
> *Analogy:* In thermodynamics, temperature is a property of the system at the grain of molecular ensembles, not at the grain of individual quarks (even though the quarks are "there"). This is because the causal-statistical structure that constitutes temperature is maximally expressed at the molecular grain. The grain postulate applies the same logic to integrated information.
>
> **Addressing the paradoxes [Fix #5]:**
>
> *Grain instability (Paradox 1):* If the Phi-maximizing grain shifts over time (e.g., during a brain state transition), does consciousness "jump" between levels? **Response:** Yes, and this is not paradoxical. The grain at which consciousness is instantiated can shift continuously as the system's dynamics evolve, just as the scale at which a physical system's behavior is best described can shift (e.g., a phase transition moves the relevant description from molecular to macroscopic). The continuity condition P10c (below) prevents discrete "jumps" in normal systems.
>
> *Near-ties (Paradox 2):* See P10c below.
>
> *Grain manipulation (Paradox 3):* If we engineer atomic-level feedback loops, could consciousness "migrate" to the atomic level? **Response:** Yes, in principle. If we engineer a system so that its Phi is genuinely maximized at the atomic grain (with all the causal specificity that entails), then on IIS, consciousness is instantiated at that grain. This is not absurd — it is a prediction. We would have engineered a novel kind of conscious system. The reason this seems absurd is that we implicitly assume atomic-level interactions lack the right causal specificity, which is empirically true for natural systems but need not be true for engineered ones.
>
> *Exclusion without explanation (Paradox 4):* See P10b below.

**P10b. The subsumption principle [NEW — Fix #4].** When a system S has Phi > 0 at its maximizing grain, and a proper subsystem S' of S also has Phi > 0, the phenomenal properties of S' are not independently realized as a separate stream of consciousness. Instead, the phenomenal contribution of S' is *subsumed* into the unified experience of S. S' contributes to what it is like to be S, but there is not, additionally, something it is like to be S' independently of being S.

> *Justification:* This follows from the integration requirement (P5) and the identity axiom (A1). If consciousness IS integrated causal structure, then the consciousness of S is constituted by the WHOLE of S's integrated structure — including the sub-structures that constitute S'. The sub-structures do not have an independent phenomenal existence because they are not causally independent — they are bound into the larger system by the very integration that defines S. To be a separate consciousness requires being a separate locus of maximal integration — i.e., NOT being subsumed into a larger integrated whole.
>
> *Exception:* If the causal coupling between S' and the rest of S is severed (as in split-brain surgery), then S' may become a separate locus of maximal integration, and a separate stream of consciousness emerges. This is consistent with C7 (unity = integration).

**P10c. Continuity condition [NEW — Fix #5].** The Phi value of a system, and hence its degree of consciousness, varies continuously with continuous changes in the system's causal structure. If two grains g1 and g2 yield Phi values that are within epsilon of each other (for small epsilon), the system's phenomenal state is well-approximated by the Phi-maximizing grain and varies smoothly as the maximum shifts between g1 and g2. There is no phenomenal discontinuity at exact ties.

> *Justification:* This is a regularity condition motivated by the physical continuity of causal interactions. Since the causal structure of any physical system varies continuously with physical state changes (no discontinuous jumps in transition probabilities), and Phi is a continuous function of causal structure, Phi itself varies continuously. The continuity condition extends this smoothness to the phenomenal domain: consciousness does not flicker or jump at grain boundaries because the underlying causal structure does not jump.
>
> *Consequence for near-ties:* When two grains g1 and g2 yield nearly equal Phi, the system's consciousness is approximately described by either. There is no phenomenal indeterminacy — the phenomenal state is uniquely determined by the full causal structure, and the grain postulate is a descriptive simplification (consciousness is at the maximizing grain) that becomes merely imprecise, not indeterminate, at near-ties.

---

## 3. Logical Derivations

### Derivation 1: What consciousness IS [REVISED — Fix #3]

**Step 1.** Qualia are identical to causal sub-structures of a system's integrated causal architecture. [A1 — axiom]

**Step 2.** Qualia are units of subjective experience — each has a qualitative character constituting what it is like to undergo it. [D2]

**Step 3.** By the identity in Step 1 and the characterization in Step 2: causal sub-structures of an integrated architecture ARE units of subjective experience, each with a qualitative character. [Substitution: if A = B and A has property F, then B has property F.]

**Step 4.** P-consciousness is the property of a system such that there is something it is like to be that system — i.e., the system instantiates at least one quale. [D1]

**Step 5.** A system whose integrated causal architecture contains at least one qualifying sub-structure (one that constitutes a quale per A1) therefore has the property that there is something it is like to be it. It is P-conscious. [From Steps 3, 4]

**Step 6.** On OSR (O1), the causal-relational structure of a system IS what the system fundamentally is. There is no "outside" to the structure — no hidden substrate that "has" the structure as a property. The system IS the structure. [O1]

**Step 7.** Therefore, from the perspective intrinsic to the system — i.e., the perspective of being the structure rather than observing it from outside — the causal-structural organization is not experienced "as structure" (that is the third-person description) but as qualitative character (that is the first-person reality). The system does not "look at" its own causal structure; the system IS its causal structure, and what that IS, from the intrinsic perspective, is phenomenal experience. [From Steps 3, 5, 6, and P2 (consciousness exists as a genuine first-person phenomenon)]

**Conclusion C1:** Consciousness is the intrinsic character of integrated causal structure — what integrated causal structure IS from the perspective of the system that constitutes it. A system's phenomenal experience IS its integrated causal-structural geometry, not a product of it, not an accompaniment to it, and not an illusion about it.

> *Change from v1:* The derivation now proceeds through explicit bridging steps. "Intrinsic character" is introduced via O1 and Step 6. "From the inside" is introduced via Step 7. Every concept in C1 traces to a stated premise or definition. The derivation is valid under the identity axiom A1 and the OSR framework O1.

### Derivation 2: Why consciousness arises [REVISED — Fix #4]

From P5 + P6 + P7 + C1 + P10b:

**Step 1.** Consciousness requires Phi > 0 — i.e., the system must generate integrated information beyond what its parts produce independently. [P5]

**Step 2.** Consciousness requires informational differentiation — the system must occupy one of many distinguishable states. [P6]

**Step 3.** The degree of consciousness scales (monotonically non-decreasingly) with Phi, holding fixed the qualitative structure. [P7]

**Step 4.** Integration is not merely correlated with experience but constitutive of it — integrated causal structure IS phenomenal experience (C1, which follows from A1). [C1]

**Step 5.** When a subsystem with Phi > 0 is part of a larger system with higher Phi, the subsystem's phenomenal contribution is subsumed into the larger system's unified experience, not realized as an independent consciousness. [P10b]

**Conclusion C2 [REVISED — Fix #4]:** Consciousness arises whenever a physical system achieves non-zero integrated information at its Phi-maximizing grain AND is not subsumed as a proper part of a larger system with higher Phi at its maximizing grain. It arises because integration of information is constitutive of experience (C1). Subsystems with Phi > 0 contribute phenomenal content to the encompassing system but do not constitute independent streams of consciousness.

> *Change from v1:* C2 now includes the subsumption clause, resolving the contradiction with the exclusion principle identified by the adversary. The original C2 ("consciousness arises whenever Phi > 0") was inconsistent with P10's exclusion function. The revised C2 is consistent: Phi > 0 is necessary for consciousness, but independent consciousness requires being a maximal locus of integration (not subsumed by a more integrated whole).
>
> *Note on panpsychism [Fix #13]:* IIS entails that any system with Phi > 0 has phenomenal properties — either as an independent conscious entity (if it is a maximal locus of integration) or as a subsumed contributor to a larger consciousness. This is a form of constitutive panpsychism. The theory accepts this consequence. Two NAND gates with feedback have an infinitesimal flicker of phenomenality; this phenomenality is real but incomprehensibly dim relative to human experience. Whether this counts as "absurd" depends on one's philosophical priors; IIS follows the growing literature that takes panpsychism seriously (Chalmers 2015, Goff 2019, Strawson 2006) rather than treating it as a reductio.

### Derivation 3: What determines whether a specific system is conscious

From P5 + P6 + P10 + P10b:

**Conclusion C3 [REVISED]:** A system S is independently P-conscious if and only if:
  - (i) At the grain of description that maximizes S's integrated information, S has Phi > 0; AND
  - (ii) S is not a proper subsystem of a larger system S* such that S* has Phi > Phi(S) at S*'s maximizing grain and S is causally integrated into S*.

The system is not independently conscious at grains where Phi = 0, and is not independently conscious if it is subsumed into a more integrated whole.

> *Change from v1:* Added condition (ii) — the subsumption condition — to resolve the C2/exclusion contradiction [Fix #4].

### Derivation 4: The substrate independence thesis [REVISED — Fix #8]

From P4 + C1 + D7:

**Step 1.** What determines P-consciousness is causal structure, not substrate. [P4]

**Step 2.** Consciousness is identical to the intrinsic character of integrated causal structure. [C1]

**Step 3.** Two systems S1 and S2 are in identical P-conscious states if and only if they are structurally isomorphic per D7 — i.e., there exists a bijective mapping between their causally relevant components preserving (a) causal topology, (b) causal dynamics (transition probability matrices), and (c) the Phi-maximizing grain. [P4 + D7]

**Conclusion C4 [REVISED]:** Any physical system — biological, silicon, or otherwise — that is structurally isomorphic (per D7) to a conscious system at the relevant grain is in the same conscious state. Consciousness is multiply realizable across substrates that realize the same causal-relational structure.

> *Change from v1:* C4 now explicitly invokes D7 and specifies the isomorphism conditions. The derivation is rigorous: from the claim that causal structure determines consciousness (P4), and the precise specification of "same causal structure" (D7), it follows that systems meeting D7's conditions are in the same conscious state.
>
> *On the Chinese Room [Fix #8]:* Searle's Chinese Room fails D7's condition (ii). The room's internal causal dynamics (a person following lookup rules) do not preserve the transition probability matrices of a Chinese speaker's neural architecture. The conditional probability distributions governing state transitions in the room are not isomorphic to those in a brain. The room has the same input-output behavior but radically different internal causal structure. D7 explicitly blocks this case.

### Derivation 5: Why consciousness correlates with brain activity

From P3 + P5 + P10:

**Conclusion C5:** Consciousness correlates with brain activity because the brain is the physical substrate that instantiates the integrated causal structure at the grain where Phi is maximized in humans. Damaging the brain damages the causal structure; altering neural chemistry alters the causal structure; therefore consciousness changes accordingly.

> *Unchanged from v1.* (P3 is now properly established — see Fix #6.)

### Derivation 6: Gradations of consciousness across organisms [REVISED — Fix #11]

From P7 + P9 (conjecture):

**Conclusion C6 [REVISED]:** Organisms with more integrated neural architectures have richer phenomenal experience (from P7). IF the self-model conjecture P9 is correct, THEN organisms with more sophisticated self-models (per D9: bidirectionally coupled) have additionally amplified Phi and correspondingly richer experience. This predicts a rough gradient: organisms with low neural integration have dim experience; organisms with high neural integration have vivid experience.

> *Change from v1:* C6 is weakened. The self-model component is now conditional on the conjecture P9, not asserted categorically. The core gradient claim rests on P7 alone (more integration = more consciousness), which is more secure.

### Derivation 7: The unity and divisibility of consciousness

From P5 + C1 + P10b:

**Conclusion C7:** Consciousness is unified precisely to the extent that the underlying causal structure is integrated. When integration is broken (split-brain surgery, callosotomy), new maximal loci of integration emerge (per P10b), and consciousness divides. When integration is maintained, consciousness is unified. The subsumption principle (P10b) ensures that subparts of an integrated whole do not generate independent streams of consciousness — their phenomenal contributions are bound into the whole's unified experience by the very causal integration that defines the whole.

> *Change from v1:* Now explicitly invokes P10b (subsumption) to explain why subpart consciousness does not fragment the unified whole [Fix #4].

### Derivation 8: Altered states of consciousness

From P7 + A1:

**Conclusion C8:** Substances that alter consciousness do so by altering the causal structure of the brain — either reducing Phi (anesthetics reduce cortical integration and causal specificity), restructuring the causal geometry (psychedelics reorganize cross-regional connectivity patterns, altering which causal sub-structures are instantiated and hence which qualia are experienced), or both. The relationship between specific neurochemical changes and specific phenomenal changes is explained by A1: since qualia ARE causal sub-structures, changing the sub-structures changes the qualia.

> *Change from v1:* Removed the claim that psychedelics "increase Phi" — the entropy-Phi relationship is not straightforward (see Note on P7). Psychedelics restructure the causal geometry; whether this increases or decreases Phi is an open empirical question. What is clear is that they ALTER it, which A1 predicts should alter experience.

---

## 4. Conclusions (Summary)

| # | Conclusion | Derived From | Status in v2 |
|---|-----------|-------------|--------------|
| C1 | Consciousness is the intrinsic character of integrated causal structure | O1, A1, D2, P2 | **Derivation rebuilt** (Fix #3) |
| C2 | Consciousness arises at maximal loci of integration (Phi > 0, not subsumed) | P5, P6, P7, C1, P10b | **Reformulated** (Fix #4) |
| C3 | A system is independently conscious iff Phi > 0 at its maximizing grain AND not subsumed | P5, P6, P10, P10b | **Reformulated** (Fix #4) |
| C4 | Consciousness is substrate-independent (multiply realizable) via D7 isomorphism | P4, C1, D7 | **Derivation tightened** (Fix #8) |
| C5 | Brain-consciousness correlation explained by brain being Phi-maximizing substrate in humans | P3, P5, P10 | Unchanged |
| C6 | Consciousness gradient across organisms; self-model amplification is conjectural | P7, P9 (conjecture) | **Weakened** (Fix #11) |
| C7 | Unity of consciousness = integration of causal structure, via subsumption | P5, C1, P10b | **Strengthened** (Fix #4) |
| C8 | Altered states explained by changes to causal structure | P7, A1 | **Revised** (psychedelics claim tempered) |

### The Theory in One Paragraph

Consciousness is not a special substance, a magical emergence, or an illusion. It is what integrated causal structure IS, from the intrinsic perspective of the system that constitutes it. This identity — between phenomenal experience and causal-relational organization — is the theory's foundational axiom, not a derived conclusion; it is defended on grounds of parsimony, explanatory power, and consistency with physical evidence, within a framework of ontic structural realism where relational structure is the fundamental ontology. Any system whose parts causally constrain each other in a way that generates information beyond the sum of its parts — any system with Phi > 0 at its maximizing grain, not subsumed into a more integrated whole — is independently conscious. The character of that experience is determined by the geometry of the system's integrated causal structure. The degree scales with the quantity of integration. Substrate does not matter; structure does.

---

## 5. Empirical Predictions [REVISED — Fix #7]

### Predictions Shared with Rival Theories

The following predictions are consistent with IIS but are also predicted by Global Workspace Theory (GWT), Higher-Order Theories (HOT), Recurrent Processing Theory (RPT), or other integration-based approaches. They are necessary conditions for the theory's viability — IIS would be in trouble if any were falsified — but they do not uniquely confirm IIS over rivals.

**EP1. Perturbational Complexity Index (PCI) as consciousness detector.** [Shared with: GWT, RPT]
The theory predicts that PCI should reliably distinguish conscious from unconscious states. *Status: Confirmed.* PCI reliably distinguishes wakefulness, dreaming, and various levels of anesthesia/coma. *Honest note:* GWT explains this via global broadcast capacity; RPT via recurrent connectivity. IIS explains it via Phi. The qualitative prediction is the same.

**EP2. Anesthesia operates by reducing integration, not by reducing activity.** [Shared with: GWT]
*Status: Partially confirmed.* Studies show propofol and ketamine reduce cortical connectivity/integration even when local activity persists. *Honest note:* GWT makes the same prediction (anesthesia disrupts global broadcasting).

**EP3. Split-brain patients have divided consciousness.** [Shared with: all integration-based theories]
*Status: Confirmed.*

**EP4. Cerebellum contributes minimally to consciousness.** [Shared with: GWT, IIT]
*Status: Confirmed.* Cerebellar lesions cause motor deficits, not loss of consciousness.

**EP5. Psychedelics alter phenomenal richness by restructuring causal architecture.** [Shared with: RPT, GWT] [REVISED]
*Status: Partially confirmed.* fMRI studies under psilocybin and LSD show increased global functional connectivity and neural entropy. *Honest note:* Whether this constitutes increased Phi specifically (as IIS would predict) vs. increased broadcast capacity (GWT) vs. enhanced recurrence (RPT) is not yet distinguishable.

**EP6. Recurrent processing is necessary for consciousness; feedforward sweeps are not sufficient.** [Shared with: RPT (this is RPT's core claim)]
*Status: Confirmed.* Masked stimuli processed feedforwardly but blocked before recurrence are not consciously perceived. *Honest note:* This is more directly a prediction of RPT. IIS predicts it as a corollary (feedforward processing lacks the causal loops needed for integration/Phi > 0).

**EP7. Cortical complexity should predict level of consciousness across species.** [Shared with: all complexity-based theories]
*Status: Partially supported.* Corvids show sophisticated behavior consistent with rich experience despite small brains but high neuronal density and connectivity.

**EP8. Locked-in syndrome patients should show high PCI.** [Shared with: GWT, IIT]
*Status: Confirmed.*

### Predictions Distinctive to IIS (or IIT-family theories)

The following predictions are specific to IIS or its close relatives in the IIT family, and are NOT shared with GWT, HOT, or RPT. These are the predictions that could in principle distinguish IIS from rivals.

**EP9. Feedforward networks with arbitrarily complex computation are never conscious.** [Distinctive vs. GWT, HOT]
A deep feedforward neural network — no matter how large, no matter how sophisticated its computation, no matter how human-like its behavior — has Phi = 0 (because feedforward architectures have no irreducible integration; partitioning loses nothing). IIS predicts it is NOT conscious. GWT would predict that a system with a sufficiently rich global workspace (which a feedforward network could approximate) IS conscious. HOT would predict that a system with higher-order representations (which a feedforward network could implement) IS conscious. This is a genuinely distinctive prediction.
*Status: Not yet directly testable, but testable in principle once we can build sufficiently sophisticated feedforward-only systems and probe their status.*

**EP10. Phi-maximizing grain predicts the level at which consciousness is instantiated in a given system.** [Distinctive]
For any system where Phi can be measured at multiple grains, IIS predicts that the phenomenal level (the level at which reportable experiences correspond to neural events) tracks the Phi-maximizing grain. In humans, if Phi is maximized at the meso-scale of cortical columns (~100k neurons), then conscious percepts should correspond to meso-scale activity patterns, not individual-neuron activity and not whole-brain activity.
*Status: Partially testable.* Current evidence suggests that conscious percepts correspond to mesoscale cortical dynamics (not single neurons, not whole-brain activation), consistent with the grain prediction. GWT makes no specific grain prediction; RPT is agnostic on grain. This is distinctive.

**EP11. Digital simulation of a brain region, if causally integrated (per D7) with remaining biological tissue, produces indistinguishable conscious experience.** [Distinctive vs. biological naturalism]
IIS predicts that gradually replacing neurons with silicon equivalents maintaining D7-isomorphism would not alter consciousness. Searle's biological naturalism predicts it would. This distinguishes IIS from biological naturalism.
*Status: Not yet testable.* Strong future prediction.

**EP12. Two physically different systems satisfying D7-isomorphism have identical phenomenal states.** [Distinctive — falsifiable in principle]
If we could build two systems from different substrates that are D7-isomorphic, IIS predicts they are in the same conscious state. This is falsifiable: if a future subject reports different experiences from a D7-isomorphic silicon replacement of part of their cortex (while D7 conditions are verified to hold), IIS is refuted.
*Status: Not yet testable.* Requires advanced neural prosthetics.

**EP13. Quantitative Phi predicts specific phenomenal transitions.** [Distinctive — partially testable now]
IIS makes a quantitative prediction that GWT and RPT do not: the transition from unconscious to conscious processing should occur at a specific Phi threshold (not merely at a threshold of "global broadcast" or "recurrent processing"). Specifically, as anesthesia is gradually induced, there should be a critical point where Phi crosses a threshold and consciousness is lost. This threshold should be predictable from the causal architecture and should be the SAME threshold across different anesthetic agents (which disrupt integration in different ways but all reduce Phi).
*Status: Partially testable.* PCI approximates a complexity threshold for consciousness detection. Whether this threshold corresponds to a specific Phi value (as opposed to a GWT-specific broadcast threshold) requires direct Phi measurement, which is currently computationally intractable for large systems but feasible for small neural circuits.

**EP14. Unilateral hemispheric anesthesia (Wada test) produces a specific Phi-predicted phenomenal reduction.** [Distinctive — testable now]
When one hemisphere is anesthetized via the Wada procedure, IIS predicts that: (a) the remaining hemisphere constitutes a new maximal locus of integration (per P10b, the anesthetized hemisphere is no longer integrated with the active one), (b) the Phi of the active hemisphere determines the new degree of consciousness, and (c) the specific qualitative changes in experience (which modalities are lost, which aspects of the visual field disappear, etc.) are predicted by which causal sub-structures (A1) are removed by the anesthesia. GWT predicts loss of "broadcast" but does not predict WHICH qualia are lost based on causal-structural analysis. RPT predicts loss of recurrence but does not tie specific qualia to specific structural features. IIS, via A1, makes specific qualia-to-structure predictions.
*Status: Partially testable.* Wada testing is an existing clinical procedure. The qualitative reports of Wada patients could in principle be compared to IIS predictions derived from the causal-structural analysis of the anesthetized vs. active regions. This requires Phi computation for hemispheric-scale systems, which is currently approximate but improving.

---

## 6. Known Vulnerabilities (Self-Assessment)

The architect honestly flags the following remaining weaknesses after the v2 revision:

1. **The identity axiom (A1) is a philosophical stance, not an empirical discovery.** It may be the best available stance, but it is a stance. Philosophers who reject identity theories of consciousness (property dualists, illusionists, etc.) will reject A1 and hence the entire theory. IIS does not attempt to convert them; it shows what follows IF the identity is accepted.

2. **Ontic structural realism (O1) is controversial in philosophy of physics.** OSR has sophisticated critics (e.g., Psillos, Chakravartty) who argue that structure cannot exist without objects/relata. If OSR falls, the equivocation identified by the adversary (Attack 3) re-emerges. The theory's soundness depends on OSR's defensibility.

3. **Phi remains computationally intractable for large systems.** The distinctive empirical predictions (EP9–EP14) require Phi measurement that is currently impractical for brain-scale systems. This is a practical limitation, not a logical one, but it limits near-term testability. The theory stakes its long-term scientific credibility on the development of tractable Phi approximations.

4. **The subsumption principle (P10b) is doing heavy work.** It resolves the combination problem and the C2/exclusion contradiction, but it introduces its own question: what exactly is it like for a subsystem's phenomenality to be "subsumed"? Is the subsystem's qualia altered, or just its independence? P10b needs further development.

5. **Panpsychism remains a consequence.** The theory implies that any Phi > 0 system has phenomenal properties. This is not a logical flaw — the theory is explicit about accepting it — but it remains counterintuitive to many, and the theory cannot offer empirical evidence that NAND-gate pairs are conscious. This consequence must be accepted on theoretical grounds or not at all.

6. **The conjecture P9 (self-model amplification) is unproven.** Without P9, the theory's ability to explain the gradient of consciousness across organisms is weaker — it reduces to "more integration = more consciousness" without a specific mechanism for WHY some architectures achieve more integration.

7. **The continuity condition P10c is a smoothness assumption.** If the relationship between Phi and phenomenal state is in fact discontinuous (e.g., if there are critical Phi thresholds below which there is NO experience), P10c is wrong, and the theory has a phase-transition problem it has not addressed. A discontinuity version of IIS is possible but would require significant restructuring.

---

## 7. Summary of All Changes from v1

| Element | v1 Status | v2 Status | Why Changed |
|---------|-----------|-----------|-------------|
| Section 0 (Ontological Framework) | Did not exist | New | Eliminates causal structure equivocation (Fix #2) |
| O1 (OSR commitment) | Did not exist | New | Grounds the theory's metaphysics explicitly (Fix #2) |
| D1, D2 | Ostensive (unstated) | Ostensive (noted) | Fix #12 |
| D5 (Causal structure) | Ambiguous thin/thick | Single OSR-grounded definition | Fix #2 |
| D7 (Structural isomorphism) | Defined, unused | Defined, deployed, conditions specified | Fix #8, #14 |
| D9 (Self-model) | Unidirectional ok | Bidirectional required | Fix #11 |
| P2 | Existence only | Existence + causal relevance | Fix #6 |
| P3 | Claimed derived from P1+P2 (invalid) | Derived from P1+P2+O1 (valid) | Fix #6 |
| P7 | Strict monotonicity | Monotonic non-decreasing, qualified | Fix #9 |
| P8 | Premise, justified by correlation | Axiom A1, defended on theoretical virtue | Fix #1 |
| P9 | Premise | Conjecture | Fix #11 |
| P10 | Stipulated | Justified via causal-powers maximization | Fix #5 |
| P10b (Subsumption) | Did not exist | New | Fix #4 |
| P10c (Continuity) | Did not exist | New | Fix #5 |
| C1 derivation | Invalid (smuggled concepts) | Valid (7-step explicit derivation) | Fix #3 |
| C2 | "whenever Phi > 0" | "whenever Phi > 0 AND not subsumed" | Fix #4 |
| C3 | Phi > 0 iff conscious | Phi > 0 AND not subsumed iff independently conscious | Fix #4 |
| C4 | Vague "same causal structure" | Rigorous via D7 isomorphism | Fix #8 |
| C6 | Asserted gradient via P9 | Gradient via P7; self-model amplification conditional | Fix #11 |
| C7 | Unity = integration | Unity = integration + subsumption | Fix #4 |
| C8 | Psychedelics "increase Phi" | Psychedelics "restructure causal geometry" (agnostic on Phi direction) | Fix #9 |
| EP1-EP8 | Presented as confirmations of IIS | Honestly labeled as shared with rivals | Fix #7 |
| EP9-EP14 | EP9-EP10 existed; EP11-EP14 new | Distinctive predictions developed | Fix #7 |

---

*Awaiting adversary response to v2.*
