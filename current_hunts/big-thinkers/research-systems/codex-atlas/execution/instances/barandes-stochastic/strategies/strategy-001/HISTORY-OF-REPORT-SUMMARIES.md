# Exploration History

## Exploration 001 — Mathematical Framework Extraction (Standard Explorer)

**Goal:** Extract the precise mathematical framework from Barandes' papers (arXiv:2302.10778, 2309.03085) and Doukas (arXiv:2602.22095).

**Outcome:** Successful extraction. 4 papers reviewed (including newly found Barandes arXiv:2507.21192).

**Key Findings:**
- The Stochastic-Quantum Theorem: "Every ISP can be regarded as a subsystem of a unistochastic process." Essentially Stinespring dilation for stochastic matrices. Finite N only.
- ISP defined as tuple (C, T, T₀, Gamma, p, A) where divisibility holds only for t' in T₀. Finite config space only.
- Forward direction (ISP → quantum) proved. Reverse direction claimed but proved elsewhere (Barandes 2025).
- Phase degrees of freedom NOT determined by stochastic data — 3 independent sources of non-uniqueness. Barandes calls it "gauge invariance."
- Born rule is definitional — density matrix defined so that Born rule holds algebraically. Barandes uses "express" and "coincide with," not "derive."
- Measurement "derivation" = standard decoherence repackaged in stochastic language. Assumes quantum interaction dynamics (Footnote 21).
- CTMCs excluded from theta-process framework (Doukas Appendix A) — "unitary QM is a particular corner of stochasticity, not the generic outcome."

**Adversarial Objections Assessment:**
1. "Isomorphism not derivation" — PARTIALLY CORRECT (forward proved, reverse claimed)
2. "Born rule definitional" — CORRECT
3. "Phase non-uniqueness" — CORRECT AND ACKNOWLEDGED by Barandes
4. "Indivisibility smuggles QM" — PARTIALLY CORRECT but overstated
5. "Nelson multi-time problem" — VALID AND CONFIRMED by Doukas

**Gaps Identified:** (1) Infinite-dimensional case unproven, (2) Born rule circularity, (3) Multi-time correlations require phases not in ISP, (4) Measurement derivation assumes quantum dynamics, (5) CTMCs excluded, (6) Entanglement/locality deferred.

**Unexpected:** Doukas (2026) is significantly sharper than Barandes and more candid about limitations. Barandes has a cluster of Feb 2026 papers building a comprehensive program. "Schur-Hadamard gauge invariance" is essentially known phase freedom in Kraus decompositions.

---

## Exploration 002 — Stochastic Programs Comparison (Standard Explorer)

**Goal:** Compare Barandes' ISP framework to SED, Nelson stochastic mechanics, and consistent/decoherent histories along structured dimensions. Produce definitive verdicts.

**Outcome:** Successful. All three comparisons resolved with definitive verdicts.

**Verdicts:**
1. **Barandes vs. SED: CATEGORY ERROR** — SED is a physical theory (classical EM + ω³ ZPF → QM). Barandes is a mathematical reformulation (QM re-expressed in stochastic language). Incompatible problem statements. SED fails as a physical theory (wrong predictions). Barandes cannot fail the same way because it makes no predictions beyond QM. The comparison reveals Barandes' essential character: gains freedom from failure by sacrificing physical specificity.

2. **Barandes vs. Nelson: DISTINCT** — Neither subsumes the other. Different mathematical structures (Markovian diffusion on ℝⁿ vs. non-Markovian kernels on finite N). Different ontological commitments (real trajectories vs. agnosticism). Multi-time problem has OPPOSITE character: Nelson over-specifies (unique paths → wrong correlations); Barandes under-specifies (multiple towers → no unique prediction).

3. **Barandes vs. Consistent Histories: COMPLEMENTARY** — CH addresses "when can probabilities be assigned to histories?" (interpretational). Barandes addresses "what is the stochastic structure of QM dynamics?" (representational). Both use decoherence for measurement. Both adopt ontological agnosticism. CH handles multi-time correctly; Barandes treats multi-time as underdetermined.

**Three-Level Classification:**
- Level 1 (Physical/reductionist): SED, Nelson — try to derive QM from stochastic mechanisms; both fail
- Level 2 (Formal/representational): Barandes — re-expresses QM in stochastic language; makes no new predictions
- Level 3 (Interpretational/extensional): CH — adds consistency rules within QM formalism; handles multi-time

**Unexpected Findings:**
1. Barandes' phase freedom and CH's realm selection problem are structurally analogous — both express non-uniqueness of classical embedding of quantum density matrix. Connection not in literature.
2. Multi-time problem has opposite character in Nelson vs. Barandes — suggests fundamental difficulty for any single-time stochastic representation.
3. Barandes never mentions consistent histories in any paper despite strong structural parallels.
4. SED failure reread through Barandes = negative existence theorem: no physical stochastic mechanism with ω³ density reproduces quantum phase structure for nonlinear systems.

---

## Exploration 003a — Phase Freedom vs. Realm Selection: Computation (Math Explorer)

**Goal:** For N=2 qubit, construct and compare the Barandes phase freedom space and the CH consistent history family space.

**Outcome:** Successful computation. Hypothesis PARTIALLY REFUTED.

**Key Results [VERIFIED/COMPUTED]:**
- Phase freedom space: dim = 2, topology T² (2-torus), parameterized by (α, β) ∈ [0, 2π)²
- Consistent history space (3-time): dim = 2, topology S² (2-sphere, from free t₂ choice)
- Dimensions match at N=2 (both = 2), but **topologies differ** (T² ≠ S²)
- **Match does NOT generalize to N > 2**: at N=3, phase freedom = 4, realm selection = 6; diverges further for larger N
- Phase freedom grows sub-quadratically; realm selection grows as N(N-1) (quadratic)
- No natural map between the spaces was found

**Assessment:** The dimensional coincidence at N=2 is coincidental. The spaces represent different mathematical objects (gauge freedom vs. measurement choice). However, both represent "hidden choices" that classical reformulations must make but standard QM fixes automatically. This is a shared structural feature even though the specific spaces differ.

**Unexpected:** For the specific system (H ∝ σ_x, ρ₀ = |+⟩), the evolved state is an energy eigenstate at all times, making t₁ completely determined. Asymmetric consistency structure: t₁ forced, t₂ free.

---

## Exploration 003b — Novelty Search: Phase Freedom = Realm Selection (Standard Explorer)

**Goal:** Systematic literature search to determine if the phase freedom ≈ realm selection connection has been published.

**Outcome:** Connection is LARGELY NOVEL with one partial prior.

**Key Findings:**
- Brun (2000, arXiv:quant-ph/0006046) connected quantum trajectory unravelings to consistent histories. Unravelings = different Kraus decompositions of a quantum channel. This is a partial prior — it shows non-uniqueness in stochastic representations relates to non-uniqueness in consistent histories, for open systems via unitary Kraus mixing.
- Our claim concerns CLOSED systems with Schur-Hadamard phase freedom (|Θ_ij|² = Γ_ij), mathematically different from Kraus mixing.
- No one has connected Barandes' specific phase freedom to realm selection. Barandes never cites consistent histories.
- The broader "non-uniqueness of classical embedding" theme appears in quantum Darwinism, frame-dependent decoherence, and quantum reference frames, but none make the specific connection.

**Novelty Verdict:** The specific formulation is novel. Brun (2000) is a partial prior at the conceptual level but uses different mathematical objects.

---

## Exploration 004 — Physical Content Probe (Standard Explorer)

**Goal:** Assess Feb 2026 paper cluster, test three value propositions (selection principle, computational advantage, structural insight), answer "what does it buy me?"

**Outcome:** Completed. MIXED VERDICT.

**Feb 2026 Papers (7 assessed):**
- **CHSH/Tsirelson (2512.18105):** STRONGEST claim. Causal local ISP → exactly Tsirelson bound. Identifies which postulate (causal locality of dynamics, not just statistics) does the work. No-signaling permits PR boxes; causal local ISP does not.
- **Deflationary Account (2602.01043):** Complex numbers needed for N>2 because unistochastic matrices require complex amplitudes. "Pseudo-quaternion" structural observation. Novel derivation path, known result.
- **Pilot-Wave/HMM (2602.10569):** Resolves ontological-nomological fork via latent variables. Real contribution to Bohmian foundations, not to physics predictions.
- **Critique papers (2602.09380, 2602.07402):** Consistent deflationary program. No positive content.

**Value Proposition Results:**
- **Test A (Selection Principle):** NEGATIVE within QM. ISP covers all finite-dim QM. Characterizes which stochastic theories are quantum (indivisible), but this is known as non-Markovianity in QI.
- **Test B (Computational Advantage):** NEGATIVE. ISP is coarser (erases phases). Every quantum calculation harder or equivalent.
- **Test C (Structural Insight):** POSITIVE in 3 ways: (1) complex numbers from indivisibility, (2) Tsirelson from causal local ISP, (3) phase freedom = realm selection.

**"What does it buy me?" (one paragraph):**
"One scientifically useful thing: a principled explanation for why Tsirelson's bound is 2√2 — because causal local indivisible stochastic evolution is precisely the class achieving this bound. Also structural derivation of why QM needs complex numbers. Beyond these: no new predictions, no easier calculations, no QFT coverage. Value is foundational/philosophical, not operational."

**Gap Analysis (4 fundamental limitations):**
1. Entanglement structure completely obscured (phases erased → can't distinguish entangled from mixed)
2. No dynamics generator (no analog of Hamiltonian H)
3. QFT/Standard Model out of reach (finite N only, no particle creation, no Lorentz symmetry)
4. Superposition invisible (interference = non-Markovianity, mechanism opaque)

**Amplituhedron Comparison:** Amplituhedron adds OPERATIONAL value (new inequalities, calculations). Barandes adds CONCEPTUAL value only (new explanations for known results). Significantly weaker.

---

## Exploration 005 — Adversarial Review: Tsirelson Claim + Steelman (Standard Explorer)

**Goal:** Try to destroy the CHSH/Tsirelson claim (arXiv:2512.18105). Construct steelman of overall program.

**Outcome:** PARTIALLY SURVIVES.

**Part 1 — Tsirelson Circularity:**
- Proof structure: ASSUME unistochastic (= Born rule QM) → APPLY causal locality → DERIVE Tsirelson via standard quantum inequality
- Amplitude matrix Θ introduced with arbitrary phases, NOT derived from ISP axioms. Unistochastic = Born rule QM.
- The proof IS the standard Tsirelson argument in stochastic language. Paper itself admits this: "we believe...may provide a route toward a novel proof...bypassing the need for explicit use of the quantum side"
- **Circularity: CONFIRMED, PARTIAL** — math is standard, framing is new

**Prior Art:**
- Tsirelson 1980: Direct prior art (QM + tensor product → 2√2)
- Buhrman-Massar 2005: Same in causality language. Direct prior art.
- Information Causality (Pawłowski 2009): Different approach, doesn't assume QM

**Causal Locality vs. No-Signaling:** Genuinely stronger. Stochastic causal locality constrains underlying dynamics, not just observable statistics. PR boxes satisfy no-signaling but not causal locality. This distinction IS real and novel.

**Survival Classification:**
- Mathematical result: NOT NOVEL (Tsirelson 1980)
- Explanatory framing: NOVEL (stochastic causal locality condition)
- Future aspiration: Unproven (proof without quantum assumption)

**Part 2 — Steelman:**
- "Level 2+" confirmed — more than reformulation at foundational level, zero operational value
- Strongest steelman arguments: (1) ISP dissolves measurement problem substantively, (2) Lagrangian analogy honest about what's missing, (3) open systems = most credible path to operational value, (4) causal locality as new foundational principle
- Path to Level 3 requires: non-unistochastic Tsirelson proof, stochastic variational principle, or operational quantum channel result

**Key Open Question:** Can causally local non-unistochastic ISPs violate Tsirelson? If "no," the proof generalizes beyond QM and the program escapes quantum assumptions. This is the single most important open question.

---

