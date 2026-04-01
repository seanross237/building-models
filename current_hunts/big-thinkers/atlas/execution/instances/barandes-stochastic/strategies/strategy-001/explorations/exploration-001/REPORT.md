# Exploration 001 — Mathematical Framework Extraction: Barandes' Indivisible Stochastic Dynamics

## Status: COMPLETE

## Papers Reviewed

1. **Barandes arXiv:2302.10778v3** (2023, updated June 2025) — "The Stochastic-Quantum Correspondence" — 38 pages. Full PDF obtained and extracted.
2. **Barandes arXiv:2309.03085v2** (2023, updated Feb 2026) — "The Stochastic-Quantum Theorem" — 32 pages. Full PDF obtained and extracted.
3. **Doukas arXiv:2602.22095v2** (2026, updated March 2026) — "On the emergence of quantum mechanics from stochastic processes" — 33 pages. Full PDF obtained and extracted.
4. **Barandes arXiv:2507.21192** (July 2025) — "Quantum Systems as Indivisible Stochastic Processes" — Abstract and HTML version reviewed.

Additional papers found but not fully reviewed:
- arXiv:2402.16935 — "New Prospects for a Causally Local Formulation of Quantum Theory" (Feb 2024)
- arXiv:2602.01043 — "A Deflationary Account of Quantum Theory and its Implications for the Complex Numbers" (Feb 2026)
- arXiv:2602.10569 — "Pilot-Wave Theories as Hidden Markov Models" (Feb 2026)

---

## Stage 1: Precise Definitions

### Indivisible Stochastic Process (ISP) — Formal Definition

From Barandes 2023b (2309.03085), Section 3.1 and Eq. 24, an indivisible stochastic process is a **tuple**:

**(C, T, T₀, Γ, p, A)**

where:

- **C**: A finite set (the **configuration space**), with N elements labeled {1, 2, ..., N}. Strictly finite in all rigorous proofs. Continuous extensions "left to future work." (Sec 3.1, footnote on measure theory)
- **T**: The set of **target times**, including an initial time 0.
- **T₀ ⊂ T**: The set of **conditioning times** (also called "division events"). Typically a "sparse" subset of T.
- **Γ**: A map **Γ: C² × T × T₀ → [0,1]**, the **transition map**, with entries:
  - Γᵢⱼ(t←t₀) ≡ p(i,t | j,t₀)  [conditional probability]
  - **Normalization** (Eq. 28): Σᵢ Γᵢⱼ(t←t₀) = 1 for all j ∈ C, t ∈ T, t₀ ∈ T₀
  - **Trivialization** (Eq. 29): Γᵢⱼ(t₀←t₀) = δᵢⱼ for all t₀ ∈ T₀
  - **Divisibility condition** (Eq. 35): Γᵢⱼ(t←t₀) = Σₖ Γᵢₖ(t←t') Γₖⱼ(t'←t₀) **ONLY for t' ∈ T₀** (not for all t')
- **p**: The **standalone probability distribution** p: C × T → [0,1], satisfying:
  - **Marginalization** (Eq. 33): pᵢ(t) ≡ Σⱼ Γᵢⱼ(t←0) pⱼ(0) for all i ∈ C, t ∈ T
  - Initial values p₁(0),...,pₙ(0) are free parameters (summing to 1)
- **A**: The **maximal algebra of random variables** A: C × T → ℝ.

**The critical constraint**: The divisibility condition holds **only when t' ∈ T₀**. For target times t' ∉ T₀, the values Γᵢₖ(t←t') are not well-defined, and the divisibility condition does not hold. This is the precise meaning of "indivisible."

### Divisible (Markovian) Stochastic Process

A Markovian process satisfies the divisibility condition **for all t'** (not just t' ∈ T₀). The set T₀ equals all of T, so every intermediate time is a conditioning time. (Barandes 2023b, Secs 2.2-2.3)

The divisibility condition for Markovian systems (Eq. 17 in 2023b):
> g_{t←t''} = g_{t←t'} ∘ g_{t'←t''} for ALL t, t', t'' ∈ T

**Relationship to standard non-Markovianity**: An ISP "represents a whole equivalence class of non-Markovian models, each of which is called a non-Markovian realizer... the specific non-Markovian realizer is potentially unknowable" (Barandes 2023b, Sec 3.1). The ISP is **weaker** than specifying a full non-Markovian Kolmogorov tower — it fixes only first-order conditional probabilities, not higher-order.

### Unistochastic Process

An indivisible stochastic process whose transition matrix Γ satisfies (Barandes 2023b, Eq. 68):

**Γᵢⱼ = |Uᵢⱼ|²** for some unitary matrix U.

Unistochastic matrices are doubly stochastic (rows and columns sum to 1), since Σᵢ|Uᵢⱼ|² = 1 = Σⱼ|Uᵢⱼ|². (2023b, Sec 5.7)

### Transition Kernels

- In general, NOT doubly stochastic: only normalized (columns sum to 1)
- The unistochastic *representation* (which is what the theorem gives) IS doubly stochastic
- Transition kernels are NOT assumed to be symmetric or to satisfy detailed balance

### Configuration Space

Explicitly finite in all rigorous work. The paper 2023a (Sec 2.1) mentions: "finite can be extremely large" and notes continuous spaces but says measure-theoretic complications "will be entirely set aside."

---

## Stage 2: Precise Theorems

### The Stochastic-Quantum Theorem (Barandes 2023b, Sec 4.1, Eq. 69)

**Formal Statement:**
> "Every indivisible stochastic process can be regarded as a subsystem of a unistochastic process." (Eq. 69)

This is the **complete formal statement** of the theorem. The paper (Sec 4.1) adds: "Focusing on the case of indivisible stochastic processes with finite configuration spaces (leaving the more general case to future work)."

**So the full conditions are:**
- Hypothesis: (C, T, T₀, Γ, p, A) is an indivisible stochastic process with **finite** C.
- Conclusion: There exists a dilated system (C̃, T, T̃₀, Γ̃, p̃, Ã) with C̃ ⊃ C, where Γ̃ is unistochastic, and the restriction to C recovers Γ.

### The Dictionary (Barandes 2023a, Eq. 15 / 2023b, Sec 5.1)

The fundamental identity (not a postulate):
**Γᵢⱼ(t←0) = tr(Θ†(t←0) Pᵢ Θ(t←0) Pⱼ)**

This is just the entry-by-entry statement Γᵢⱼ = |Θᵢⱼ|² rewritten in trace form using projectors Pᵢ = eᵢeᵢ†. "This formula is an identity, not a postulate. Any non-negative real number can be written non-uniquely as the modulus-square of a complex number." (Barandes 2023b, Sec 5.1, after Eq. 72)

### Construction (Proof Sketch)

The proof (Barandes 2023b, Secs 5.1-5.9) proceeds:

1. **Step 1** (Eq. 72): Write Γᵢⱼ(t←0) = |Θᵢⱼ(t←0)|² — defines the (non-unique) time-evolution operator.
2. **Step 2** (Eq. 76): Define Hilbert space H ≅ ℂᴺ with configuration basis e₁,...,eₙ.
3. **Step 3** (Sec 5.2): Define configuration projectors Pᵢ = eᵢeᵢ†.
4. **Step 4** (Eq. 83): Define density matrix ρ(t) ≡ Θ(t←0) ρ(0) Θ†(t←0), where ρ(0) = Σⱼ pⱼ(0) Pⱼ.
5. **Step 5** (Sec 5.3-5.4): Extract Kraus operators Kβ = Θ(t←0) Pβ, satisfying Σβ Kβ† Kβ = 1.
6. **Step 6** (Sec 5.5-5.9): Construct a dilated system with a larger Hilbert space where Θ embeds unitarily via Stinespring dilation.

### Direction of Correspondence

**Forward direction (proved in 2023b):** ISP → unistochastic (quantum). Explicit construction via the above steps.

**Reverse direction (claimed but proved elsewhere):** "As shown in other work (Barandes 2025), one can go in the other logical direction and show that any comprehensive quantum system that includes measuring devices and observers as part of the system can be modeled as an indivisible stochastic process." (Barandes 2023b, Sec 4.2)

The reverse direction is NOT proved in 2023b or 2023a. It requires the 2025 paper (likely 2507.21192). The 2025 paper HTML states this is "claimed bidirectional" but the construction is only explicit in one direction.

**Is it an isomorphism?** No. The correspondence is:
- Many-to-one stochastic → quantum: Multiple Θ matrices give the same Γ (phase freedom)
- Many-to-one quantum → stochastic: Multiple quantum systems can give the same Γ after restriction to diagonal

### Relationship Between Transition Kernels and Quantum Channels (CPTP Maps)

**Doukas (2026)** establishes this precisely (Sec 4.2):
- The compatibility condition: Π(ϕ_{t,s}(J(p(s)))) = J(Γ(t←s)p(s)), where Π projects to diagonal and J embeds probability vectors as diagonal operators.
- **One-to-many**: "Every stochastic kernel Γ(t←s) admits **at least one** completely positive operator lift." (Doukas 2026, after Eq. 34, emphasis original)
- **Why?** By Arveson's extension theorem: every positive map on a commutative C*-algebra (the diagonal) extends to a CP map on the full algebra. But the extension is NOT unique.

In Kraus form (Doukas Eq. 35): Given Kraus operators Kβ, the stochastic kernel is Γ(t←s) = Σβ Kβ ⊙ Kβ* (Hadamard product). Multiple Kraus decompositions give the same Γ.

### Phase Degrees of Freedom

**Three independent sources of non-uniqueness** (Barandes 2023a, footnote 6; 2023b, Sec 5.1; Doukas 2026, Sec 5):

1. **Entry-wise phase freedom (Schur-Hadamard gauge):** Θᵢⱼ(t←0) ↦ exp(iθᵢⱼ(t)) Θᵢⱼ(t←0) leaves Γ = |Θ|² invariant. "This nonuniqueness implies a previously unrecognized form of gauge invariance for all quantum systems." (Barandes 2023a, footnote 6)

2. **Kraus decomposition non-uniqueness:** Multiple Kraus decompositions for the same quantum channel.

3. **Non-Markovian realizer choice:** Different higher-order conditional probabilities (same Γ) correspond to different "non-Markovian realizers."

**Physical significance of phases:** Off-diagonal elements of ρ(t) = Θρ₀Θ† encode "compressed memory of history dependence not fixed by transition kernels alone" (Doukas 2026, Abstract). The phases are NOT determined by Γ alone; they require specification of multi-time conditional structure.

### What Doukas (2026) Proves Beyond Barandes

1. **Generalization**: Barandes' θ-process (unitary lift) is a special case. Doukas extends to arbitrary CPTP lifts, including open quantum system (Lindblad) dynamics.

2. **θ-process limitation**: "The only Markovian θ-process is the trivial process" (Doukas 2026, Appendix A). CTMCs are excluded from the original Barandes framework.

3. **Divisibility Criterion (Theorem 1)**: If a stochastic process is Q-divisible at time t₁ (t₀ < t₁ < t₂) AND the lifted state ρ(t₁) is diagonal for every initially diagonal ρ(t₀), THEN the process is C-divisible at t₁. (Full proof provided, Sec 6.3)

4. **Lindblad connection**: CK-divisible CPTP families ↔ Lindblad master equation form. The natural class is open-system quantum dynamics, not closed unitary.

5. **Phase clarification**: Resolves where phase information lives (in path-space multi-time conditional structure, not in one-step kernel Γ).

---

## Stage 3: Scope Conditions

### Finite vs. Infinite Dimensional

**Explicit limitation**: "Focusing on the case of indivisible stochastic processes with finite configuration spaces (leaving the more general case to future work)" (Barandes 2023b, Sec 4.1). All proofs are N×N matrix constructions with finite N.

**Continuous case**: "for reasons of brevity and simplicity, this paper will entirely set aside measure-theoretic considerations that arise for the case of uncountable sets" (Barandes 2023b, Sec 2.1). No rigorous extension to position/momentum (continuous configuration spaces).

**What breaks in infinite dimensions**: The Stinespring dilation requires bounded operators on finite-dimensional spaces. For infinite-dimensional Hilbert spaces, additional functional-analytic conditions are needed (domain considerations, unbounded operators, etc.). This covers spin, discrete systems, and finite-dimensional quantum mechanics, but NOT quantum field theory or continuous-spectrum observables directly.

### Single-Particle vs. Multi-Particle (Entanglement)

**Composite systems** (Barandes 2023a, Sec 3.9; Eq. 63-66):

Configuration space of composite system AB: C̃ = C × C'. Transition matrix: Γ̃_{ii',jj'}(t←0) = p((i,i'), t | (j,j'), 0).

**Entanglement** (Barandes 2023a, Sec 3.9):
> "Systems A and B start to exhibit what superficially appears to be a nonlocal kind of stochastic dynamics" when Γ̃(t←0) ≠ Γᴬ(t←0) ⊗ Γᴮ(t←0).

This captures entanglement phenomenologically. However: "the precise nature of this apparent dynamical nonlocality is an extremely subtle matter. Relevant questions concerning locality and causation will be treated in detail in future work." (Barandes 2023a, Sec 3.9)

**Critical limitation**: Subsystem A does NOT get a well-defined ISP structure of its own in the entangled case. Marginal probabilities exist but transition maps for individual subsystems are generally undefined. (Barandes 2023b, Sec 3.4, Eq. 55)

### Non-Relativistic vs. Relativistic

None of the three papers address QFT, special relativity, or relativistic quantum mechanics. All examples are non-relativistic. This is a complete open gap.

### Open vs. Closed Systems

- **Closed systems**: Unistochastic processes (unitary evolution). The theorem covers this case.
- **Open systems**: Kraus/CPTP maps. Handled via Stinespring dilation into a larger closed system, then tracing over the environment.
- **Lindblad dynamics**: Doukas (2026) shows that CK-divisible CPTP families admit Lindblad form. This covers open quantum systems with Markovian-like quantum dynamics.
- **Decoherence**: Modeled as environmental division events (Barandes 2023a, Sec 3.7).

### Observables Coverage

- **"Beables"** (random variables): Diagonal matrices A(t) = Σᵢ aᵢ(t) Pᵢ. These are the genuine configuration-space random variables.
- **"Emergeables"**: Non-diagonal self-adjoint matrices. Modeled as measurement outcomes of composite system interactions (Sec 4.1-4.3). "These sorts of emergent observables also play a key role in de Broglie-Bohm formulation." (Barandes 2023a, Sec 4.1)
- **POVMs**: Doukas (2026, Sec 5) shows arbitrary POVMs can be recovered by engineering system-apparatus couplings.

**Key point about emergeables**: Non-position-basis observables (spin, momentum) are not random variables in the fundamental stochastic description — they are emergent properties that only appear in measurement interactions. This is a significant ontological claim.

---

## Stage 4: The Measurement Claim

### What Exactly Is Claimed

Barandes 2023a, Sec 4.4: "According to the foregoing treatment of the measurement process, a measuring device is an ordinary physical system that can carry out a measurement of an observable and then ends up in a final configuration that reflects a definite measurement outcome. The probabilities for a measuring device's various possible measurement outcomes are given by the textbook Born rule (78), and conditioning on the specific measurement outcome leads to the textbook formula (94) for wave-function collapse. Hence, this picture **arguably has the resources to solve the measurement problem**."

The key word is **"arguably"** — Barandes acknowledges this as a claim, not a proof.

### Assumptions in the Derivation (Sec 4.2)

The derivation (Eqs. 72-89) assumes:

1. **Composite system SDE exists** with subject S, device D, environment E.
2. **Unistochastic evolution** (Eq. 72): Γ^SDE_{ide,i'₀d'₀e'₀}(t←0) = |U^SDE_{ide,i'₀d'₀e'₀}(t←0)|². This assumes the composite quantum dynamics.
3. **Specific interaction wave function** (Eq. 73): Ψ^SDE_{i'd'e'}(t') = Σ_{α'} Ψ̃^S_{α'}(t') ẽ^S_{α',i'} δ_{d',d(α')} δ_{e',e(α')}. This is the quantum measurement interaction — it encodes that the device ends up in state d(α') correlated with eigenstate α' of observable Ã^S. This is an **assumed form**, not derived.
4. **Post-interaction factorization** (Eq. 74): U^SDE(t←t') = U^S(t←t') ⊗ U^D(t←t') ⊗ U^E(t←t'). Assumes no further SDE interaction.
5. **Environment generates a division event** (Sec 4.4): "a good measuring device should be... in sufficiently strong contact with a noisy environment to generate a robust division event at the conclusion of the measurement interaction."

**Footnote 21** is crucial: "It is straightforward to write down idealized examples of suitable unitary time-evolution operators for the composite system." — The correct unitary dynamics is ASSUMED to exist, not derived.

### How Collapse Appears

**Barandes 2023a, Sec 4.3:** "The phenomenon of wave-function collapse therefore reduces to a prosaic example of conditioning."

The conditional density matrix (Eq. 91):
> ρ^{S|α',t'}(t) ≡ U^S(t←t') P̃^S_{α'} U^{S†}(t←t')

"corresponds to a collapsed state vector or wave function" (Eq. 94):
> Ψ^{S|α',t'}(t) ≡ U(t←t') ẽ^S_α

Collapse is the transition to using this conditional density matrix after obtaining measurement result d(α').

### Is This Genuinely Different from Decoherence?

**Largely the same mechanism.** The key ingredients are identical to standard decoherence accounts:
1. Coupling to environment E
2. Entanglement between S and D
3. Environment creates a "robust division event" = decoherence
4. Effective collapse when conditioned on device reading

The novelty is the **language**: Barandes translates the standard decoherence story into stochastic language and calls the division event a "conditioning" rather than collapse. Ontologically, the configuration-space trajectory continues — there is no actual discontinuity. But the mathematical mechanism is standard decoherence.

---

## Stage 5: Known Failure Points and Gaps

### Gap 1: Infinite-Dimensional Claim vs. Proof

**Claim:** "provides a first-principles explanation for why quantum systems are based on... the Born rule." (2023b abstract)

**Actual proof:** Only for finite N. No extension to continuous Hilbert spaces. Continuous quantum systems (particles in ℝ³, quantum fields) are not covered rigorously.

**Where exactly:** Barandes 2023b, Sec 4.1: "leaving the more general case to future work."

### Gap 2: Born Rule Is Definitional

**Claim:** "a first-principles explanation for why quantum systems are based on... the Born rule."

**Reality:** The density matrix is DEFINED as ρ(t) ≡ Θ(t←0) ρ(0) Θ†(t←0) (Eq. 83 in 2023b, Eq. 17 in 2023a). The Born rule pᵢ(t) = tr(Pᵢ ρ(t)) then follows **algebraically** from this definition and the marginalization condition. Barandes himself uses the word "express" (2023a, Sec 3.4): "One can **express** the law of total probability (19) as pᵢ(t) = tr(Pᵢ ρ(t))." This is a **reformulation**, not a derivation.

**Where exactly:** Barandes 2023a, Sec 3.2: "The probability formulas pᵢ(t) = tr(Pᵢ ρ(t)) and pᵢ(t) = |Ψᵢ(t)|² **coincide with** the Born rule" — "coincide with" acknowledges it's an identification, not a proof.

### Gap 3: Phase Non-Uniqueness and Multi-Time Correlations

**Claim:** Full quantum mechanics recoverable from the stochastic description.

**Reality (Doukas 2026, Sec 5):** A single one-step transition kernel Γ(t←s) is "one-step stochastically indistinguishable" between many different unitaries U_X, U_Y that have |U_X_{ij}|² = |U_Y_{ij}|² but differ in phases. These different unitaries yield different predictions for sequential measurements:

> "[V U_X]_⊙ ≠ [V U_Y]_⊙ despite [U_X]_⊙ = [U_Y]_⊙"

"The one-step kernel Γ(t←s) does not specify the process." (Doukas 2026, Sec 7)

**The resolution** is that multi-time correlations encode the phase structure. But this means: to recover full QM predictions, you need MORE than just Γ — you need the multi-time conditional structure. Barandes' ISP only fixes Γ and leaves higher-order conditionals unspecified.

**Where exactly:** This gap is most clearly stated in Doukas 2026, Sec 5 (Phases from phase-blind dynamics).

### Gap 4: The Measurement Derivation Assumes Quantum Dynamics

**Claim:** "the measurement problem is solved" — measuring devices are ordinary physical systems.

**Reality:** The derivation assumes the composite SDE evolves **unitarily** (Eq. 72 in 2023a). This is assumed, not derived from the stochastic framework itself. The measurement "derivation" uses quantum evolution as input.

**Where exactly:** Barandes 2023a, Sec 4.2, Eq. 72, and Footnote 21: the unitary evolution of SDE is assumed to take the specific form in Eq. 73.

### Gap 5: CTMCs and Standard Classical Stochasticity Excluded

**Doukas' finding** (Appendix A and Sec 3): In Barandes' θ-process framework, the only Markovian θ-process is the trivial (identity) process. Classical CTMCs (Brownian motion, chemical kinetics, etc.) have R ≠ 0 (nonzero generator) and are therefore NOT θ-processes.

> "the constraint R=0 excludes not only CTMCs, but also intrinsically non-Markovian processes with genuine first-order leakage" (Doukas 2026, after Eq. 19)

This means: if "indivisibility" is the key feature distinguishing quantum from classical stochasticity, the framework **artificially** excludes large classes of legitimate classical processes (CTMCs). The quantum sector is not "generic" — it's a special corner.

**Where exactly:** Doukas 2026, Sec 3 and Appendix A.

### Gap 6: Entanglement and Locality

The paper explicitly defers: "the precise nature of this apparent dynamical nonlocality is an extremely subtle matter. Relevant questions concerning locality and causation will be treated in detail in future work." (Barandes 2023a, Sec 3.9)

Bell inequalities, causal locality, and what makes quantum correlations non-classical within this framework are explicitly unaddressed in the three papers.

---

## Adversarial Objections Assessment

### Objection 1: "Isomorphism, not derivation"

**Claim:** The lifting theorem runs both ways — it equally well "derives" stochastic processes from QM.

**Assessment:** **PARTIALLY CORRECT**. The correspondence is claimed bidirectional:
- Forward (ISP → quantum): Proved in 2023b via explicit Stinespring dilation.
- Reverse (quantum → ISP): Claimed in 2023b Sec 4.2, attributed to "other work (Barandes 2025)," not proved here.

Barandes 2023b, Sec 4.2: "As shown in other work (Barandes 2025), one can go in the other logical direction."

However, the reverse direction requires that the quantum system include measuring devices as explicit subsystems — it's not automatic for isolated quantum systems. The forward direction is the content of the theorem.

**Classification: (a) Algebraic identity** for the forward direction (the proof is correct algebra). The reverse direction is closer to **(c) Novel physical claim** — it requires including observers as physical subsystems.

**Does Barandes acknowledge this?** Yes, implicitly. The 2023b abstract says "every indivisible stochastic process corresponds to a unitarily evolving quantum system" — this is the forward direction only.

### Objection 2: "Born rule is definitional"

**Claim:** The density matrix ρ is constructed so that ⟨xᵢ|ρ|xᵢ⟩ = p(xᵢ, τ). Is the Born rule an input or output?

**Assessment:** **CORRECT**. The Born rule is an **algebraic consequence of the definition** of ρ, not an independently derived fact. The sequence is:
1. Define ρ(t) ≡ Θ(t←0) ρ(0) Θ†(t←0) (Eq. 17 in 2023a)
2. Check that pᵢ(t) = tr(Pᵢ ρ(t)) — this follows immediately from ρ(0) = Σⱼ pⱼ(0) Pⱼ and the definition of ρ(t)
3. Call this the Born rule

Barandes uses the word "express" (not "derive") in 2023a Sec 3.2: "One can **express** the law of total probability as pᵢ(t) = tr(Pᵢρ(t))."

The Born rule for emergeables (non-diagonal observables) IS genuinely more interesting (Sec 4.2, Eq. 78), but it relies on assuming the measurement interaction in Eq. 73.

**Classification: (a) Algebraic identity** — the basic Born rule is definitional. The emergeable Born rule requires additional physical assumptions.

### Objection 3: "Phase non-uniqueness"

**Claim:** Multiple Hilbert space representations exist for the same stochastic process.

**Assessment:** **CORRECT and explicitly acknowledged by Barandes**. Barandes 2023a, footnote 6: "This nonuniqueness implies a previously unrecognized form of gauge invariance for all quantum systems." Barandes 2023a, Sec 3.2: "The mathematical objects Θ(t←0), ρ(t), Ψ(t), and A(t)... do not naturally have direct physical meanings, in part because they are **not uniquely defined** by C or by Γ(t←0)."

Doukas (2026, Sec 5) clarifies: The different representations encode different multi-time conditional probabilities. Within the ISP framework, different phase choices are empirically distinguishable — they give different predictions for sequential measurements.

**Classification: (a) Algebraic identity** — the non-uniqueness is inherent in the construction.

### Objection 4: "Indivisibility smuggles in QM"

**Claim:** Defining processes as "indivisible" (violating Leggett-Garg) is tantamount to defining them as non-classical.

**Assessment:** **PARTIALLY CORRECT but overstated**. The definition of indivisibility is:
- A stochastic process where divisibility holds ONLY for t' ∈ T₀ (not all t')

This is a real mathematical condition that excludes CTMCs (which require R ≠ 0, contradicting the θ-process constraint). Doukas confirms: "the stochastic-quantum correspondence identifies a distinguished subclass of kernels, the θ-processes, for which [first-order] leakage is excluded." (Doukas 2026, Sec 3)

However, calling it "tantamount to non-classical" is too strong — classical deterministic systems (permutation matrices) are trivially unistochastic and thus ISPs. The key issue is that the class of ISPs that are ALSO unistochastic (i.e., have a unitary lift) is precisely the class of quantum systems. This makes the framework a **restatement** of quantum mechanics in stochastic language, not an independent derivation.

**Classification: (b) Standard physics consequence** — the indivisibility condition does carve out non-classical behavior, but it is a genuine mathematical constraint, not a mere definitional trick.

**Leggett-Garg**: Neither Barandes nor Doukas discusses Leggett-Garg inequalities. This is an explicit gap.

### Objection 5: "Nelson's multi-time problem (Blanchard et al. 1986)"

**Claim:** Single-time probabilities match by construction, but multi-time correlations require the phases the stochastic process alone doesn't determine.

**Assessment:** **VALID and confirmed by Doukas**. This is the cleanest and most important objection.

Barandes' framework only specifies Γ(t←t₀) — first-order conditional probabilities. Higher-order conditionals are "unobservable in experiments and will be left unspecified" (Barandes 2023a, Sec 2.2).

But quantum mechanics DOES predict multi-time correlations (via the Heisenberg picture, successive measurements, quantum trajectory theory). These predictions depend on the specific quantum state (density matrix, off-diagonal elements), which is NOT determined by Γ alone.

Doukas 2026, Sec 5 (Eq. 46-48) shows explicitly: Two unitaries U_X, U_Y with |U_X_{ij}|² = |U_Y_{ij}|² give the same one-step kernel Γ but different predictions for sequential measurements. The phases "encode compressed path-space memory... invisible at the level of one-step transition probabilities."

Barandes' response (implicit): The sequential measurement context involves a larger composite system (S + devices), and the relevant predictions are captured by the emergeable structure. But this pushes the problem to multi-system stochastic dynamics, which requires even more unspecified phase structure.

**Classification:** The mismatch in single-time probabilities is **(a) algebraic identity** (by construction). The claim that full QM multi-time predictions are recovered is **(c) novel physical claim** that is NOT established in the papers reviewed — it requires specification of the measurement interactions (which depends on phases).

---

## Summary Assessment

### What the Framework Actually Proves

**Solid mathematical result (Barandes 2023b, Theorem):** Any finite-dimensional stochastic matrix Γ satisfying the ISP axioms can be embedded in a unistochastic system via Stinespring dilation. This is correct and non-trivial — it generalizes the fact that any CP map has a unitary dilation.

**Solid result (Doukas 2026, Theorem 1):** Q-divisibility + diagonality preservation ⟹ C-divisibility. This is a rigorous theorem with a complete proof.

### What the Framework Claims But Doesn't Prove

1. That the ISP framework provides a fundamentally new interpretation of QM rather than a restatement
2. That the Born rule is "derived from first principles" rather than built in by construction
3. That the measurement problem is solved (it's re-solved using the same ingredients as decoherence theory)
4. That multi-time correlations are captured (they require phases not determined by Γ)
5. That the framework extends to infinite dimensions (explicitly left to future work)
6. That the framework accommodates standard classical stochastic processes (CTMCs are excluded)

### Novelty Assessment

The **genuine mathematical novelty** is:
1. The systematic framework of ISPs as a generalization of Markov chains
2. The dictionary Γᵢⱼ = |Θᵢⱼ|² rewritten as tr(Θ†PᵢΘPⱼ) — a useful algebraic identity
3. The unistochastic embedding theorem — essentially a restatement of Stinespring dilation for stochastic matrices
4. The "Schur-Hadamard gauge invariance" — novel terminology for known phase freedom

The **conceptual novelty** (whether it constitutes a genuinely new formulation of QM or just a restatement) depends on whether one finds the stochastic language more illuminating than the Hilbert space language. Mathematically, the content is equivalent.

---

## Key Quotes (Direct)

1. **On the theorem**: "Every indivisible stochastic process can be regarded as a subsystem of a unistochastic process." (2309.03085, Eq. 69)

2. **On uniqueness**: "the mathematical objects Θ(t←0), ρ(t), Ψ(t), and A(t)... do not naturally have direct physical meanings, in part because they are **not uniquely defined** by C or by Γ(t←0)." (2302.10778, Sec 3.2)

3. **On the Born rule**: "The probability formulas pᵢ(t) = tr(Pᵢρ(t)) and pᵢ(t) = |Ψᵢ(t)|² **coincide with** the Born rule." (2302.10778, Sec 3.2) — "coincide with," not "prove."

4. **On collapse**: "The phenomenon of wave-function collapse therefore reduces to a prosaic example of conditioning." (2302.10778, Sec 4.3)

5. **On the measurement derivation assumption**: "It is straightforward to write down **idealized examples of** suitable unitary time-evolution operators for the composite system." (2302.10778, Footnote 21) — i.e., they are assumed to exist.

6. **On entanglement locality**: "the precise nature of this apparent dynamical nonlocality is an extremely subtle matter. Relevant questions concerning locality and causation will be **treated in detail in future work**." (2302.10778, Sec 3.9)

7. **On finite scope**: "Focusing on the case of indivisible stochastic processes with finite configuration spaces (**leaving the more general case to future work**)." (2309.03085, Sec 4.1)

8. **Doukas on unitary corner**: "unitary quantum mechanics is not the **generic** outcome of mere stochasticity, but rather a **particular corner** of it." (2602.22095, Sec 7)

9. **Doukas on phase information**: "The one-step kernel Γ(t←s) does not specify the process." (2602.22095, Sec 7)

10. **Doukas on the θ-process constraint**: "making the choice [Eq. 13] therefore imposes **substantive additional structure** on the space of stochastic processes; it is not a vacuous reparametrization." (2602.22095, Sec 3)
