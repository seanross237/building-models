# FINAL REPORT — Strategy 001: Barandes' Indivisible Stochastic Dynamics

**Mission:** Determine whether Barandes' reformulation of quantum mechanics as "indivisible stochastic dynamics" reveals structure, predictions, or constraints beyond standard QM — or whether it is purely notational.

**Explorations:** 6 completed (E001-E005, with E003 split into 003a/003b)
- 4 standard explorations, 1 math exploration, 1 novelty search
- 11 Barandes papers reviewed (4 core + 7 Feb 2026 cluster)
- 3 comparative frameworks analyzed (SED, Nelson, consistent histories)
- 1 adversarial review with steelman

---

## Executive Summary

Barandes' indivisible stochastic dynamics is a **Level 2+ reformulation** of finite-dimensional quantum mechanics. It re-expresses QM in stochastic process language using a mathematical correspondence (essentially Stinespring dilation for stochastic matrices). It makes **no new predictions**, provides **no computational advantages**, and has **fundamental limitations** (no entanglement visibility, no dynamics generator, no QFT extension). However, it adds **genuine conceptual value** at the foundational level: it identifies stochastic causal locality as a physical principle characterizing the Tsirelson bound, provides a structural derivation of why QM needs complex numbers, and dissolves the measurement problem via configuration-space realism without new postulates.

**Verdict:** More than trivial notation change, less than new physics. A coherent foundational program that reframes known results from stochastic starting points. The single most important open question — whether causally local non-unistochastic ISPs are also constrained to the Tsirelson bound — would, if answered positively, elevate the program from reformulation to genuine new constraint.

---

## What We Accomplished

### Phase 1: Foundation & Disambiguation (E001, E002)

**E001** extracted the precise mathematical framework from 4 papers (Barandes arXiv:2302.10778, 2309.03085, 2507.21192; Doukas arXiv:2602.22095). Key findings:
- The Stochastic-Quantum Theorem is essentially Stinespring dilation for stochastic matrices (finite N only)
- Born rule is definitional (density matrix constructed to satisfy it, not derived from it)
- Phase degrees of freedom (3 independent sources of non-uniqueness) are NOT determined by stochastic data
- Measurement "derivation" = standard decoherence repackaged in stochastic language
- 4 of 5 adversarial objections from the QG mission were confirmed or partially confirmed

**E002** established the three-level classification:
- Level 1 (Physical/reductionist): SED, Nelson — try to derive QM from stochastic mechanisms; both fail
- Level 2 (Formal/representational): Barandes — re-expresses QM in stochastic language; no new predictions
- Level 3 (Interpretational/extensional): Consistent histories — adds consistency rules within QM; handles multi-time

The SED comparison is a **category error**: SED is a physical theory that fails; Barandes is a reformulation that can't fail in the SED way because it never leaves the quantum framework.

### Phase 2: Computation & Novel Content (E003a/b, E004)

**E003a** (math explorer) constructed the phase freedom and realm selection spaces for a qubit:
- Phase freedom: dim = 2, topology T² (2-torus)
- Realm selection: dim = 2, topology S² (2-sphere)
- Dimensions match at N=2 (coincidental); **match breaks at N>2** (phase freedom grows sub-quadratically, realm selection grows quadratically)
- No natural map between the spaces

**E003b** (novelty search) confirmed the observation is novel: Brun (2000) is a partial prior using different mathematical objects. No one has connected Barandes' specific phase freedom to consistent histories realm selection.

**E004** assessed 7 Feb 2026 papers and tested three value propositions:
- Selection principle: NEGATIVE (ISP covers all finite-dim QM; "indivisibility = quantum" is known as non-Markovianity in QI)
- Computational advantage: NEGATIVE (ISP erases phases; every quantum calculation is harder or equivalent)
- Structural insight: POSITIVE (complex numbers from indivisibility; Tsirelson from causal local ISP; phase-realm connection)

### Phase 3: Adversarial Review & Verdict (E005)

**E005** adversarially reviewed the strongest claim (CHSH/Tsirelson):
- The proof IS partially circular: assumes unistochastic (= Born rule QM), derives Tsirelson via standard quantum inequality
- Mathematical result is prior art (Tsirelson 1980)
- The conceptual framing IS novel: stochastic causal locality condition is genuinely stronger than no-signaling
- The paper itself acknowledges the limitation and calls for a future proof bypassing quantum assumptions

Steelman assessment: "Level 2+" — more than a reformulation at the foundational level, zero operational value.

---

## Directions Tried

| Direction | Status | Key Outcome |
|-----------|--------|-------------|
| Framework extraction | Succeeded | Stinespring dilation for stochastic matrices |
| Three-level classification | Succeeded | SED = Level 1, Barandes = Level 2, CH = Level 3 |
| Phase freedom ≈ realm selection | Exhausted | Coincidental match at N=2; breaks at N>2 |
| Physical content probe | Succeeded | Structural insight only; no computational/predictive value |
| Adversarial review of Tsirelson | Succeeded | Partially circular; conceptual framing novel |

---

## What We'd Recommend Next

1. **The open ISP Tsirelson question** (highest priority): Can causally local non-unistochastic ISPs violate the Tsirelson bound? This is a well-defined computational problem (enumerate ISPs on a 4×4 stochastic matrix, apply causal locality, optimize CHSH). A positive answer ("no, they can't violate it") would be a genuine new result — the Tsirelson bound would follow from causal locality alone, without quantum assumptions. This is the single most promising path to new physics from the ISP program.

2. **Stochastic variational principle**: Does a variational principle S[p(q_t|q_0)] exist whose extremization recovers quantum dynamics? This is the "missing Lagrangian" — the enabling step that could transform ISP from reformulation to foundation, analogous to how the Lagrangian formulation enabled gauge theories and path integrals.

3. **Open quantum systems connection**: The ISP framework naturally handles CPTP maps. There may be operational value in connecting ISP to the Milz et al. non-Markovian quantum process framework. This is the most credible path to computational relevance.

4. **No further strategy needed for the core assessment.** The verdict is clear and stable: Barandes is a Level 2+ reformulation. Further investigation would only be worthwhile if the Tsirelson open question is answered positively.

---

## Novel Claims

### Claim 1: Three-Level Classification of Stochastic QM Programs

**Claim:** Stochastic approaches to quantum mechanics fall into three distinct levels: Level 1 (physical/reductionist — SED, Nelson), Level 2 (formal/representational — Barandes), Level 3 (interpretational/extensional — consistent histories). The SED-Barandes comparison is a category error because they operate at different levels.

**Evidence:** E002 systematic comparison along 6 structured dimensions per program. Direct quotes from papers. SED failure mechanism (Santos O(ℏ) proof) vs. Barandes' structural immunity.

**Novelty search:** No published taxonomy of stochastic QM programs at this granularity found. Individual programs are well-characterized but the three-level classification is our synthesis.

**Strongest counterargument:** The levels may not be cleanly separable — Barandes aspires to Level 1 (deriving QM from stochastic principles) and the ISP axioms could be seen as physical assumptions, not just formal ones.

**Status:** Partially verified — the classification is useful but the boundaries are contested.

### Claim 2: Phase Freedom and Realm Selection Are Structurally Analogous

**Claim:** Barandes' Schur-Hadamard phase freedom (multiple Θ for same Γ) and consistent histories' realm selection problem (multiple consistent families for same quantum system) both represent the non-uniqueness of projecting a quantum density matrix onto classical probability distributions.

**Evidence:** E003a computation (verified for N=2), E003b novelty search (confirmed novel, Brun 2000 partial prior). Both spaces represent "hidden choices" that classical reformulations must make.

**Novelty search:** Brun (2000, arXiv:quant-ph/0006046) is a partial prior using Kraus mixing for open systems. Our formulation concerns Schur-Hadamard freedom for closed systems — different mathematical objects.

**Strongest counterargument:** The mathematical equivalence fails: different topologies (T² vs S²), different scaling with N. The analogy is conceptual, not structural. The N=2 dimension match is coincidental.

**Status:** Partially verified — the conceptual analogy holds but the mathematical isomorphism is refuted.

### Claim 3: Tsirelson Bound from Stochastic Causal Locality

**Claim:** The Tsirelson bound (2√2) follows from causal local indivisible stochastic dynamics, providing a physical interpretation of which postulate explains the bound.

**Evidence:** arXiv:2512.18105 (Barandes, Hasan, Kagan 2025). E004 assessment, E005 adversarial review.

**Novelty search:** Mathematical result is prior art (Tsirelson 1980). Conceptual framing (stochastic causal locality vs. no-signaling) is novel. Causal locality condition is genuinely stronger than no-signaling (excludes PR boxes).

**Strongest counterargument:** The proof is partially circular — assumes unistochastic (= QM). The paper itself acknowledges this and calls for a future proof bypassing quantum assumptions. Without that future proof, this is a restatement, not a derivation.

**Status:** Partially verified — novel framing of known result, not yet a genuinely independent derivation.

### Claim 4: SED Failure as Negative Existence Theorem

**Claim:** SED's irreparable failure, viewed through the Barandes Level 1/Level 2 distinction, functions as a negative existence theorem: no physical stochastic mechanism with ω³ spectral density reproduces quantum phase structure for nonlinear systems.

**Evidence:** SED mission (16 explorations), Santos O(ℏ) proof, fix-space exhaustion. E002 reinterpretation through Barandes framework.

**Novelty search:** The SED failure is well-known. The reinterpretation as a negative existence theorem via the Level 1/Level 2 distinction is our synthesis.

**Strongest counterargument:** This may be a trivial restatement — "SED fails" and "no classical EM + ω³ mechanism reproduces QM" may be the same claim in different language.

**Status:** Speculative — the reinterpretation adds framing but may not add substance.

---

## Assessment of the Strategy

The Disambiguate-Compute-Adjudicate methodology worked well:
- **Phase 1 (Disambiguate):** 2 explorations instead of the planned 3. The framework extraction (E001) was so thorough that the adversarial disambiguation (originally E003) was largely completed within it.
- **Phase 2 (Compute):** 2 explorations. The phase freedom = realm selection hypothesis was worth testing computationally (E003a) even though it was partially refuted — the refutation IS the finding.
- **Phase 3 (Adjudicate):** 2 explorations. The adversarial review (E005) was essential and produced the nuanced "Level 2+" classification that is more accurate than a simple "reformulation" verdict.

**What worked:** Pre-loading adversarial findings, requiring definitive verdicts, the amplituhedron comparison frame, parallel exploration (003a/003b), the steelman requirement.

**What I'd change:** Would have run the Tsirelson non-unistochastic computation (flagged in E005) instead of the concrete worked example. This is the highest-value computation remaining.

**Total: 6 explorations used, 4 remaining in budget.** The verdict is clear; additional explorations would have diminishing returns unless targeting the Tsirelson open question specifically.
