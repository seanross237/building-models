# Exploration 002 Report — Stochastic Programs Comparison: Barandes vs. SED, Nelson, and Decoherent Histories

## Goal

Compare Barandes' indivisible stochastic dynamics to three other stochastic-QM programs along precise structural dimensions. Produce definitive verdicts (same / complementary / distinct / subsumes) for each comparison.

## Pre-loaded Context from Exploration 001

Key facts established:
- Barandes' framework is a **reformulation** of finite-dimensional QM (not a derivation from classical physics)
- The core theorem (Stochastic-Quantum Theorem) = Stinespring dilation for stochastic matrices
- Born rule is **definitional** (ρ defined so Born rule holds algebraically)
- Phase degrees of freedom are NOT determined by stochastic data (3 sources of non-uniqueness)
- Measurement "derivation" = standard decoherence repackaged
- CTMCs excluded from θ-process framework (Doukas shows only Markovian θ-process is trivial)
- Framework is finite-dimensional only; no extension to continuous spaces
- Multi-time structure is underdetermined: choosing a Kolmogorov tower consistent with Γ is "potentially unknowable" per Barandes himself

Key SED mission facts (from completed 16-exploration SED mission):
- Santos (2022): SED = O(ℏ) term of QED in Wigner-Weyl representation
- Moyal bracket: {W,H}_M = {W,H}_P + (ℏ²/24)V'''(x)∂³W/∂p³ + O(ℏ⁴)
- SED captures only O(ℏ⁰) Poisson term. Fails at O(ℏ²) for nonlinear systems.
- Root cause: ω³ spectral density creates positive feedback in nonlinear systems
- Quartic oscillator: SED overshoots QM variance by 17.8% (var_x = 0.303 vs. QM 0.257 at β=1)
- Hydrogen: self-ionizes in T_ion ≈ 19,223 orbital periods at L=1.0
- Three proposed fixes all fail; failure is structurally irreparable

---

## Section 1: Barandes vs. SED

### 1.1 Overview of SED

SED is a **physical theory** that claims quantum behavior emerges from classical electrodynamics plus a real, Lorentz-invariant electromagnetic zero-point field (ZPF). Key features:
- The ZPF is a specific physical entity: a random electromagnetic field with spectral energy density ρ(ω) = ℏω³/(2π²c³) — the Lorentz-invariant zero-point density
- Particles are classical point charges driven by the Abraham-Lorentz-Dirac radiation reaction force + ZPF
- QM is claimed to EMERGE from these classical dynamics through statistical averaging over ZPF realizations
- Success cases: exact agreement for linear (quadratic Hamiltonian) systems (harmonic oscillator, Casimir, van der Waals)
- Failure cases: catastrophic disagreement for all nonlinear systems

### 1.2 Six-Dimensional Comparison

**Dimension 1: Level of description**

- **SED:** A *physical theory*. Makes claims about the actual dynamics of matter and fields in spacetime. The ZPF is proposed as a real physical field that exists in vacuum. SED particles have trajectories. The theory predicts specific observables (energy, spectra, cross-sections) that differ from QM.

- **Barandes:** A *mathematical reformulation*. Makes no claims about the physical substrate of quantum randomness. There is no physical field, no particle trajectory, no specific dynamical law proposed. The reformulation recasts the QM formalism in stochastic language — it is to QM as matrix mechanics is to wave mechanics. It does not propose a deeper physical mechanism.

**This is the fundamental category distinction. SED and Barandes are not in the same category of program.**

The analogy in the GOAL.md is precisely correct: asking "why doesn't Barandes fail where SED fails?" is like asking "why doesn't the Lagrangian formulation of mechanics fail where the Newtonian formulation works in non-inertial frames?" They're reformulations of the same theory — the question contains a category error.

An even sharper analogy: SED is like trying to DERIVE electromagnetism from a model of elastic ether. Barandes is like switching from Cartesian to spherical coordinates in Maxwell's equations. The ether model can be tested and falsified (and was). The coordinate change cannot — it is exact and says nothing new.

**Dimension 2: What plays the role of stochasticity**

- **SED:** The ZPF is the physical noise source. It is a specific stochastic field with:
  - Lorentz-invariant spectral density ρ(ω) = ℏω³/(2π²c³)
  - Real, classical electromagnetic field (E and B fields)
  - Specific correlation functions (Boyer 1975 propagator)
  - Dynamics governed by Maxwell's equations with random boundary conditions

- **Barandes:** The "indivisibility" is a *structural property* of the mathematical transition kernel — not a physical noise source. Specifically: the composition property Γ(t←s) = Γ(t←r)Γ(r←s) fails for generic intermediate times r. This is a mathematical statement about the kernel structure, not a claim about any physical mechanism. The word "stochastic" in Barandes refers to the mathematical form of the equations (probabilities summing to 1), not to a physical noise source.

**Dimension 3: Born rule**

- **SED:** An *approximate derivation* from classical averaging. For linear systems: averaging over ZPF realizations exactly yields ρ(x) = |ψ(x)|² at equilibrium. This is exact for linear systems because all O(ℏ²) corrections to the Moyal bracket vanish. For nonlinear systems: the O(ℏ²) Moyal corrections are absent from SED, and the Born rule probabilities break down (systematic deviation from |ψ|²). Santos (2022) makes this formal: SED ≡ O(ℏ⁰) + O(ℏ¹) terms in Wigner-Weyl QED; the Born rule holds iff these terms are exact.

- **Barandes:** *Definitional.* The density matrix ρ(t) is defined as ρ(t) = Θρ₀Θ† where Θ is the time-evolution operator satisfying Γᵢⱼ = |Θᵢⱼ|². The Born rule pᵢ(t) = tr(Pᵢρ(t)) follows algebraically from this definition. Barandes uses the word "express" not "derive" — the Born rule cannot be violated within this framework because it is a mathematical identity, not a tested prediction. There is no regime where it breaks down.

This asymmetry is decisive: SED's Born rule is a testable approximation; Barandes' Born rule is an unfalsifiable algebraic identity.

**Dimension 4: Where does quantum structure come from?**

- **SED:** Claims to emerge from classical physics + stochastic ZPF noise. The quantum structure (discrete energy levels, interference, entanglement) is supposed to be an emergent collective phenomenon arising from the ZPF dynamics. The ω³ spectral density is the proposed mechanism for "quantum behavior." This claim fails: the ω³ density creates feedback that exceeds QM predictions for nonlinear systems. Santos: SED = O(ℏ) QED, not O(ℏ∞) QED.

- **Barandes:** Imported via two definitional choices: (1) the indivisibility condition on Γ (which excludes classical Markovian processes), and (2) the definition ρ(t) = Θρ₀Θ† (which imports unitarity through the choice of Θ). The quantum structure is not *derived* — it is *re-encoded* in stochastic language. Barandes' indivisibility condition is essentially the condition that the process is NOT classical (CTMCs are excluded, as Doukas (2026) proves: "the only Markovian θ-process is the trivial process"). So the framework excludes classical physics by construction and re-encodes quantum structure through the non-Markovian indivisibility condition.

**Dimension 5: Predictions**

- **SED:** Makes predictions that DIFFER from QM and are experimentally WRONG:
  - Quartic anharmonic oscillator ground state variance: SED = 0.303, QM = 0.257 (17.8% excess)
  - Hydrogen atom: SED predicts self-ionization in ~19,223 orbital periods; QM predicts stable 1s state
  - Bell inequalities: SED satisfies S ≤ 2 (Bell); QM violates Bell. SED is wrong.

- **Barandes:** Makes NO distinct predictions from standard QM (within the finite-dimensional scope). The Stochastic-Quantum Theorem guarantees mathematical equivalence: every ISP maps to a quantum system and vice versa. There is by construction nothing to falsify independently.

**Dimension 6: Failure mode**

- **SED:** The ω³ spectral density creates positive feedback in nonlinear systems:
  - Nonlinearity → frequency shifts → ω³ delivers more ZPF power at higher frequency → excess energy injection → more nonlinearity → ...
  - Santos (2022) identifies the exact mathematical form: the O(ℏ²) Moyal corrections are structurally absent from SED and cannot be recovered without importing the QM structure itself.
  - The failure is not a technical problem but a structural impossibility.

- **Barandes:** No analogous failure mode within the finite-dimensional scope. The framework is:
  - Free of any dynamical law → no ω³ problem (no spectral density; no physical field)
  - Free of any approximation → no systematic deviation from QM (Born rule is exact by definition)
  - Free of any propagation → no feedback mechanism (kernel Γ is read from QM, not propagated forward)
  - The limitations of Barandes are of a different character: phase non-uniqueness, finite-dimensional restriction, circular structure.

### 1.3 The Category Error, Made Precise

SED and Barandes belong to fundamentally different categories:

| Feature | SED | Barandes |
|---------|-----|---------|
| Program type | Physical theory (reductionist) | Mathematical reformulation |
| Goal | Derive QM from classical physics | Reformulate QM in stochastic language |
| Noise source | Real EM field (ZPF, ω³ density) | Mathematical property (indivisibility) |
| Born rule | Approximate derivation (fails for nonlinear) | Definitional algebraic identity |
| Testability | Makes falsifiable predictions ≠ QM | Equivalent to QM by construction |
| Failure mode | ω³ feedback loop in nonlinear systems | No physical failure; only structural limitations |
| Relationship to QM | Competitor (claims to do more) | Reformulation (claims equivalence) |

**Why doesn't Barandes hit the SED wall?** Because the wall is: "when you try to derive quantum mechanics from a specific classical model (EM + noise), the specific noise (ω³) creates unphysical feedback for nonlinear systems." Barandes doesn't try to derive QM from anything. It has no spectral density, no ω³, no ALD equation, no particle trajectory. The SED wall is not a wall Barandes would ever encounter.

### 1.4 Verdict

**CATEGORY ERROR: not directly comparable.**

More precisely: **Distinct programs addressing incompatible problem statements.** SED addresses: "Can QM be derived from classical mechanics + specific physical noise?" (Answer: no.) Barandes addresses: "Can QM be reformulated in stochastic mathematical language?" (Answer: yes, formally, for finite-dimensional systems.)

They share the vocabulary of "stochasticity" but use it to mean entirely different things (physical noise source vs. mathematical structure). Comparing their failure modes reveals the category structure: SED fails as a *physical theory*, while Barandes cannot fail in the same sense because it is not a physical theory. The comparison is informative precisely through its failure to apply.

---

## Section 2: Barandes vs. Nelson Stochastic Mechanics

### 2.1 Overview of Nelson Stochastic Mechanics

Nelson (1966) showed that Schrödinger's equation is equivalent to a system of stochastic differential equations for a diffusing particle. Key features:
- Particles undergo Brownian motion in configuration space (ℝ³)
- Diffusion coefficient: ν = ℏ/2m (specific physical value, not a free parameter)
- Two velocity fields: osmotic velocity u = ν ∇ ln R (where ψ = R exp(iS/ℏ)) and current velocity v = (1/m)∇S
- The forward SDE: dX = (v + u)dt + dW⁺, and backward SDE: dX = (v - u)dt + dW⁻, where dW are Wiener processes with covariance 2ν dt
- The Newton-Nelson equation: m(Du + D*u)/2 = -∇V (where D, D* are mean forward/backward stochastic derivatives)
- This equation is exactly equivalent to the real and imaginary parts of the Schrödinger equation iℏ ∂ψ/∂t = -ℏ²/(2m) ∇²ψ + Vψ

### 2.2 Barandes' Own Characterization of the Difference

From Barandes (arXiv:2507.21192): "The most well-known stochastic-process formulation was due to Nelson's work in the 1960s through the 1980s, and is known today as Nelsonian stochastic mechanics." The key limitation of all prior stochastic approaches (including Nelson): "they were all based on adaptations of methods like Brownian motion, and so they all assumed **Markovian** dynamical laws. This constraint limited the ability of these approaches to capture the full behavior of quantum systems without becoming very complicated, and also made it difficult to generalize them beyond systems of fixed numbers of finitely many non-relativistic particles."

This is the core technical distinction Barandes himself identifies: **divisible (Markovian) vs. indivisible (non-Markovian).**

### 2.3 Five-Dimensional Comparison

**Dimension 1: Stochastic structure**

- **Nelson:** Continuous diffusion on configuration space ℝⁿ. The mathematical framework is Itô SDEs with Wiener process noise. The diffusion coefficient ℏ/2m is a specific physical constant — not a free parameter. Particles have continuous (though nowhere differentiable) trajectories. The stochastic process is a Markov diffusion in position space (when conditioned on the wavefunction), making it effectively Markovian relative to the quantum state.

- **Barandes:** Discrete-time transition kernels on finite configuration spaces (N states). The mathematical framework is stochastic matrices. No diffusion coefficient. No SDE. No Wiener process. The key structural feature is **indivisibility** — the composition law Γ(t←s) ≠ Γ(t←r)Γ(r←s) for generic intermediate times r. This is the non-Markovian property that Barandes says Nelson's approach lacked.

These are technically incompatible mathematical structures: continuous Markovian diffusion vs. discrete-space non-Markovian transition kernels.

**Dimension 2: Born rule**

- **Nelson:** The Born rule ρ = |ψ|² is an input assumption — the "quantum equilibrium" condition. Nelson showed that if the initial distribution equals |ψ₀|², it remains |ψ(t)|² at all later times. But why the initial distribution should be |ψ₀|² is not derived from more fundamental principles — it must be imposed. (This is parallel to how Bohmian mechanics requires quantum equilibrium as an initial condition.)

- **Barandes:** Born rule is definitional via ρ(t) = Θρ₀Θ†. Not an initial condition — an algebraic consequence of the construction. Also not derived from something more fundamental.

Both treat Born rule as an input, but via different formal mechanisms (initial condition vs. algebraic definition).

**Dimension 3: Multi-time correlations**

This is a critical shared failure mode, but with an important difference:

- **Nelson (original formulation):** The multi-time problem was identified by Nelson himself and analyzed by Blanchard, Golin, and Serva (1986). The canonical failure case: two uncoupled but entangled harmonic oscillators. Quantum mechanics predicts persistent correlations ⟨X₁(2πn) X₂(0)⟩_QM = const ≠ 0 for all n (periodic, non-decaying). The Nelson Markov diffusion predicts ⟨X₁(2πn) X₂(0)⟩_stoch → 0 as n → ∞ — ergodicity of the Markov diffusion erases memory of the initial entanglement. The fundamental reason: in QM, multi-time correlations are computed via ⟨A(t₁)B(t₂)⟩ = Tr[ρ A(t₁) B(t₂)] using Heisenberg picture operators — this is NOT the same as classical conditional expectations over a Markov process. A 2022 paper (arXiv:2208.14189) showed that adding "effective collapse" — wave function collapse to a delta function after position measurement, which changes the subsequent stochastic drift — restores agreement with QM for sequential position measurements. The fix requires importing wave function collapse, which is precisely what one is trying to avoid, and it introduces instantaneous nonlocal influences between particles. **Nelson himself ultimately concluded (around 2005–2012) that stochastic mechanics fails as a complete interpretation of quantum mechanics**, citing the multi-time correlations problem and the nonlocality required by entanglement. His Princeton lecture notes "Mystery of Stochastic Mechanics" document this disillusionment.

- **Barandes:** Multi-time structure is **underdetermined**. The one-step kernel Γ(t←s) does not specify the process. As Doukas (2026) showed quantitatively: "For N configurations and 3 time points, fixing two-time conditionals leaves at least N(N-1)² degrees of freedom in three-time conditionals." Barandes himself acknowledges this: "there will generically exist a large or infinite number of ways of choosing a complete Kolmogorov tower consistent with those ingredients" and the specific choice is "potentially unknowable, and perhaps meaningless" empirically. Off-diagonal density matrix elements are "a compressed memory register" encoding multi-time history dependence.

**Key asymmetry:** Nelson's multi-time problem is that the process gives WRONG predictions (too determinate — one unique path measure). Barandes' multi-time problem is the opposite — the process gives NO unique predictions (too indeterminate — any phase choice works). Both frameworks fail to independently derive QM multi-time predictions, but for opposite reasons: Nelson over-specifies the process; Barandes under-specifies it.

**Dimension 4: Does one subsume the other?**

No — they are orthogonal in mathematical domain:
- Nelson: continuous configuration spaces ℝⁿ, Markovian diffusion
- Barandes: finite N-state systems, non-Markovian transition kernels

One could ask whether Nelson's process satisfies Barandes' indivisibility condition. In Nelson's framework, the position-space propagator P(x₂,t₂|x₁,t₁) is Markovian given the drift (conditioned on the wavefunction), which means it IS divisible in the sense relevant to Barandes — making Nelson's process a classical stochastic process in Barandes' classification! But since Barandes requires finite N and Nelson operates on ℝ³, the formal inclusion question cannot be posed directly.

This is a significant structural point: Nelson's Markovian diffusion would be classified by Barandes as "not quantum" (since only non-Markovian/indivisible processes are quantum in Barandes' framework). The quantum behavior emerges from the non-Markovian drift in Nelson's case — which Barandes would call "importing quantum structure through the wavefunction-dependent drift."

**Dimension 5: What does each have that the other lacks?**

Nelson has but Barandes lacks:
- Specific dynamical law: the Newton-Nelson equation with ℏ/2m diffusion coefficient
- Particle trajectories (continuous paths in configuration space)
- Extension to ℝ³ and continuous quantum mechanics (wave mechanics)
- A candidate ontology: "particles actually undergo random walks in configuration space"
- A natural connection to Bohmian mechanics (same ontology: real trajectories)
- Relativistic attempts (though they failed)
- Clear failure mode (over-specified path measure → wrong multi-time correlations)

Barandes has but Nelson lacks:
- General finite-dimensional coverage (qubits, spin systems, quantum gates, open systems)
- The Stochastic-Quantum Theorem (formal proof that any ISP maps to a quantum system)
- No specific dynamics required — works for any quantum Hamiltonian
- A formal statement distinguishing quantum from classical: indivisibility vs. divisibility
- Natural treatment of open quantum systems (Lindblad dynamics fit naturally)
- Doukas (2026) extension to CPTP (Kraus) maps, which CAN accommodate CTMCs

### 2.4 The Deeper Structural Distinction

Both Nelson and Barandes use stochastic language but make fundamentally different metaphysical commitments:

- **Nelson:** Particles are real, follow definite trajectories (with noise), and quantum mechanics is the emergent statistics. The stochasticity is physical — it represents actual random forces on particles. This is an ONTOLOGICAL claim about what exists.

- **Barandes:** The stochastic transition kernel is a mathematical description. No claim is made about whether the stochasticity is physical or what causes it. The framework is explicitly ONTOLOGICALLY AGNOSTIC. Barandes says the realizer choice (the complete Kolmogorov tower) is "potentially unknowable, and perhaps meaningless."

This distinction matters for the multi-time problem. Nelson WANTS to give an ontological account of multi-time correlations (particles following real trajectories) — and fails because the ontology gives the wrong predictions without adding collapse. Barandes AVOIDS giving an ontological account — and "succeeds" by treating the multi-time structure as empirically meaningless, essentially saying "we don't know which trajectory, so we don't predict multi-time correlations beyond what QM says."

### 2.5 Verdict

**DISTINCT — neither subsumes the other.**

More precisely: they are non-overlapping in mathematical domain (continuous Markovian diffusion vs. finite-discrete non-Markovian transitions) and differ in ontological commitment (physical particle trajectories vs. mathematical agnosticism). The core technical distinction is Markovian vs. non-Markovian — Barandes explicitly identifies this as why his approach supersedes Nelson's. Both share the multi-time correlation problem but for opposite reasons: Nelson over-specifies (unique path measure, wrong predictions); Barandes under-specifies (multiple Kolmogorov towers, no unique prediction). Nelson is richer in physical content and continuous-space coverage; Barandes is more general in scope (any quantum system) and more honest about multi-time indeterminacy.

---

## Section 3: Barandes vs. Consistent/Decoherent Histories

### 3.1 Overview of Consistent/Decoherent Histories

The consistent histories (CH) / decoherent histories framework (Griffiths 1984, Omnes 1988, Gell-Mann & Hartle 1990/1993) reformulates QM to address interpretation without invoking collapse:

- A **history** is a sequence of projection operators {P_{α₁}(t₁), P_{α₂}(t₂), ..., P_{αₙ}(tₙ)}
- The **chain/class operator** for history α is: K(Y^α) = P_{αₙ}(tₙ)...P_{α₂}(t₂)P_{α₁}(t₁) (time-ordered)
- The **decoherence functional** is: D(α, α') = Tr(K(Y^α) ρ₀ K(Y^{α'})†) [Gell-Mann-Hartle form]
- **Consistency condition (Griffiths):** Re[D(α, α')] = 0 for α ≠ α' — quantum interference vanishes
- **Medium decoherence (Gell-Mann-Hartle):** D(α, α') ≈ 0 for α ≠ α' — approximate vanishing
- For a consistent set, probabilities p(α) = D(α, α) = Tr(K(Y^α) ρ₀ K(Y^α)†) satisfy classical probability axioms
- **Single framework rule:** Cannot mix incompatible frameworks (projectors that don't commute)
- **Realm selection problem (key unresolved issue):** Many different consistent sets exist; no preferred one

### 3.2 Barandes Does Not Discuss Consistent Histories

A notable finding: in all three of Barandes' main papers (arXiv:2302.10778, 2309.03085, 2507.21192), consistent histories and decoherent histories are **not mentioned**. Barandes' papers compare extensively to Nelson, Bopp, and Fényes, but not to CH. This is a significant omission given that CH is arguably the most systematic framework for addressing the measurement problem in QM — the same problem Barandes claims to address.

### 3.3 Four-Dimensional Comparison

**Dimension 1: Handling measurement without collapse**

- **Consistent Histories:** The CH approach uses three-time sequences: t₀ (initial), t₁ (quantum system state), t₂ (pointer position). The pointer family and measurement family are consistent sets. For the measurement family: Pr([s^j_1], R^k) = |c_j|² δ_{jk} — the probability of finding particle in state s^j before measurement and pointer at R^k is |c_j|² if j=k and 0 otherwise. No collapse needed — different frameworks answer different questions consistently. The decoherence functional D(α, α') ≈ 0 when the measuring apparatus entangles the outcome with environmental modes, making different branches consistent.

- **Barandes:** Measurement is "a prosaic example of conditioning." Given a composite SDE system (quantum system + measurement device) with assumed unistochastic evolution of a specific form (Eq. 73 in 2309.03085, Footnote 21), conditioning on the device showing outcome i gives Born-rule probability p_i = ρ_{ii}. The "derivation" assumes appropriate quantum interaction dynamics as input (Footnote 21 explicitly).

**Key similarity:** Both approaches use decoherence as the physical mechanism. CH: decoherence makes D(α, α') ≈ 0 for different outcomes. Barandes: decoherence ensures the composite system evolves in the required unistochastic form. Both ASSUME appropriate dynamics as input and both show that, given decoherence, Born-rule probabilities follow. Neither derives measurement from first principles.

**Key difference:** CH asks "WHEN can probabilities be assigned to histories?" — a question about which questions are well-posed. Barandes asks "WHAT is the stochastic mathematical structure of quantum dynamics?" — a question about the formal representation. CH is interpretational; Barandes is representational.

**Dimension 2: Conditions for when classical-like descriptions apply**

- **Consistent Histories:** The consistency condition Re[D(α, α')] = 0 (or approximately 0). This says: quantum amplitudes for different histories must not interfere. When this holds, the histories can be treated as classical alternatives with additive probabilities. The condition depends on the Hamiltonian, the initial state, and the choice of projectors — it is not an intrinsic property of the system but of the chosen description.

- **Barandes:** The indivisibility condition (violation of Chapman-Kolmogorov: Γ(t←s) ≠ Γ(t←r)Γ(r←s) for generic r). When a process IS divisible (Markovian), it is classical (Doukas proves: the only Markovian θ-process is trivial). Indivisibility is the criterion distinguishing quantum from classical stochastic processes.

**The relationship:** These are complementary, not equivalent. CH's consistency condition is a condition on which SETS OF HISTORIES can receive classical probability assignments (a selection criterion applied to histories). Barandes' indivisibility is a structural property of the transition kernel (a classification criterion for stochastic processes). They're measuring different things: CH asks "for this quantum system, which coarse-grained description is internally consistent?" while Barandes asks "which stochastic processes correspond to quantum systems?"

A key asymmetry: CH is defined within the Hilbert space formalism (it takes ρ₀, H, and projectors as given). Barandes claims to operate below the Hilbert space formalism (deriving it from the ISP). However, as Exploration 001 showed, Barandes effectively imports the Hilbert space structure through the definition ρ = Θρ₀Θ†.

**Dimension 3: Division events vs. decoherence functional**

- In Barandes, "conditioning times" T₀ are the special times t' at which divisibility holds: Γ(t←t₀) = Γ(t←t')Γ(t'←t₀). These mark moments when the process can be factored — "division events."

- In CH, measurement times are when projection operators are inserted, and the decoherence functional D(α, α') determines if these define a consistent set. The times t₁, t₂, ... in a history are the analogs of conditioning times.

**Conceptual parallel:** Both frameworks identify special times at which the quantum evolution can be "cut" for classical description. Barandes' conditioning times T₀ and CH's projection times serve the same conceptual function: marking moments of potential classical description. However:
- CH: the cut is validated by checking D ≈ 0 (requires computing quantum amplitudes)
- Barandes: the cut is built into the framework's construction (T₀ are defined as the conditioning times, not derived)

In Barandes, T₀ is part of the model specification; in CH, consistency is a testable condition on any proposed set of times.

**Dimension 4: Is Barandes a refinement, restatement, or different approach to the same problem?**

CH and Barandes address adjacent but genuinely different problems:

- **CH's central problem:** The measurement problem in its interpretational form — "how do we assign definite probabilities to measurement outcomes without collapse?" CH answer: identify consistent families where D ≈ 0, assign classical probabilities within each family.

- **Barandes' central problem:** The formalism problem — "can QM be re-expressed in stochastic mathematical language?" Barandes answer: yes, any ISP maps to a quantum system (Stochastic-Quantum Theorem).

These are different questions. However, they connect at the measurement problem: both claim to dissolve the collapse postulate using decoherence-type arguments. The connection is: if we translate CH's decoherence functional into stochastic kernel language, we would express CH's consistency condition as a condition on Γ. This has not been done, and it would require extending Barandes' finite-dimensional framework.

**The realm selection problem vs. phase freedom:** A structural parallel:
- CH's realm selection problem: Given a quantum system, many different consistent families exist. Which do we pick? The framework gives no preferred answer — it adopts "pluricity" (multiple valid descriptions depending on questions asked).
- Barandes' phase freedom: Given an ISP, many different phase choices for Θ give different valid ISP representations of the same QM. Which is "real"? Barandes says the choice is "potentially unknowable, and perhaps meaningless."

**Both frameworks hit the same philosophical wall**: QM does not uniquely specify a classical description. CH calls this the realm selection problem; Barandes avoids naming it but acknowledges it (via phase freedom). The parallel is substantive: both are expressing the fact that quantum mechanics admits many inequivalent classical coarse-grainings, none of which is preferred.

### 3.4 The Decoherence Condition Hierarchy

The research agent identified a precise hierarchy of decoherence conditions in CH:
- **Exact:** D(α, β) = 0 exactly — too stringent, never holds in realistic systems
- **Weak (Griffiths):** Re[D(α, β)] = 0 — sufficient for probability sum rules
- **Medium (Gell-Mann–Hartle):** D(α, β) ≈ 0 — physically relevant, holds when environment decoheres branches
- **Strong:** Medium + existence of records — required for quasiclassical realm selection

The key contrast with Barandes: in CH, the decoherence condition must be *checked* as a precondition before assigning probabilities. In Barandes' framework, probabilities are assigned via the stochastic transition matrix directly, and decoherence (vanishing of off-diagonal Γ elements) emerges as a feature of dynamics (when a system couples to a large environment) rather than as a precondition. This is a genuine structural difference: CH is epistemically conservative (only assign probabilities to consistent histories) while Barandes is structurally pre-committed (probabilities are always assigned, with decoherence emerging dynamically).

Also: **Kent's (1997) "contrary inferences" objection** to CH deserves noting. Kent showed that two different consistent sets can assign probability 1 to mutually contradictory propositions about the same system. This shows that the single-framework rule, while preventing *within-framework* inconsistency, does not prevent the framework *selection* from being physically underdetermined. This is the technical form of the realm selection problem.

### 3.5 Verdict

**COMPLEMENTARY — different aspects of the same foundational problem.**

CH addresses: "When can we assign consistent probabilities to sequences of events?" (interpretational, about observability and classical descriptions). Barandes addresses: "What is the mathematical structure that maps quantum dynamics to stochastic language?" (representational, about the formal structure). Both use decoherence as measurement physics, both adopt ontological agnosticism (no preferred description), both hit the same philosophical wall (non-unique classical description). Neither subsumes the other. CH is structurally better for multi-time correlations (built around multi-time histories). Barandes is structurally broader (any quantum system, any dynamics). A synthesis connecting CH's decoherence functional to Barandes' stochastic kernels would be technically interesting.

---

## Section 4: Cross-Cutting Analysis

### 4.1 The Multi-Time Problem as Universal Obstacle

All three comparison programs (SED, Nelson, Barandes) struggle with multi-time correlations, but for structurally different reasons:

- **SED:** Wrong multi-time correlations for nonlinear systems — the ω³ feedback creates incorrect statistics at multiple times. The failure is quantitative and experimentally wrong.
- **Nelson:** Wrong multi-time correlations by construction for entangled systems — the canonical example is two uncoupled entangled oscillators: QM predicts persistent ⟨X₁(2πn) X₂(0)⟩ = const ≠ 0; Nelson's Markov diffusion predicts decay to 0 (ergodicity). The fix (effective collapse) imports the QM measurement postulate, making the framework circular. Nelson himself abandoned the program after recognizing this.
- **Barandes:** Underdetermined multi-time correlations — phase freedom means any Kolmogorov tower is consistent. Barandes treats this as a feature, not a bug ("potentially unknowable"). The research agent's table claims "multi-time correlations: correct" for Barandes, but this is Barandes' claim, not the established result; Doukas (2026) shows N(N-1)² degrees of freedom remain unspecified for three-time correlations.
- **Only Consistent Histories** handles multi-time correlations correctly *by construction* — it is built around multi-time histories from the start, and decoherence condition directly encodes whether the multi-time structure is admissible.

**Structural conclusion:** Any stochastic program that represents quantum dynamics via single-time transition kernels (or single-time diffusion equations) will generically fail to uniquely specify QM multi-time correlations. This is a structural gap between the single-time stochastic description and QM's richer multi-time structure. The multi-time problem is effectively a theorem about stochastic representations of QM, not a coincidence.

### 4.2 The Ontological Commitment Spectrum Maps to Failure Modes

| Program | Ontological commitment | Physical substrate | Failure mode |
|---------|----------------------|-------------------|-------------|
| SED | Very high | Real ZPF field (ω³) | Physically wrong predictions for nonlinear systems |
| Nelson | High | Real particle trajectories (Brownian) | Wrong multi-time correlations (without collapse) |
| Barandes | Very low | None specified | Phase non-uniqueness; not a physical failure |
| Consistent Histories | Very low | None specified | Realm selection: no preferred classical description |

Programs with high ontological commitment make wrong predictions. Programs with low ontological commitment make no wrong predictions but also no new predictions. This is not coincidence — the more physically specific the stochastic mechanism, the more likely it conflicts with QM for nonlinear/multi-time behavior.

### 4.3 The Reformulation Hierarchy

Four programs organized by type:

1. **SED:** NOT a reformulation of QM — a *competitor* claiming QM derives from classical physics + ω³ noise. Falsified.
2. **Nelson:** *Partial reformulation* — the Schrödinger equation is equivalent to specific Brownian motion, but requires additional input (quantum equilibrium, multi-time structure via collapse). Markovian.
3. **Barandes:** *Full reformulation* (for finite-dim QM) — any ISP maps to QM (Stochastic-Quantum Theorem). Non-Markovian/indivisible. Phase freedom means the reformulation is many-to-one.
4. **CH:** *Interpretational extension within QM* — adds rules (consistency condition) for when to assign classical probabilities to histories. Does not reformulate the formalism.

Nelson is properly a failed predecessor to Barandes: it used Markovian dynamics (divisible) and therefore couldn't capture quantum non-Markovianity without complications. Barandes fixes this by using indivisible dynamics explicitly. SED is a different enterprise entirely. CH operates at a different level (interpretational).

### 4.3b Cross-Program Comparison Table

| Feature | Nelson (1966) | Consistent Histories (1984–) | Barandes (2023–) |
|---------|--------------|------------------------------|------------------|
| Fundamental object | Markov diffusion on config. space | Consistent history families (projection operators + decoherence functional) | Indivisible stochastic matrix on config. space |
| Wave function | Derived (ψ = √ρ e^{iS/ℏ}), needed for drift | Primary (defines class operators and D(α,β)) | Secondary (derived from Γ) |
| Born rule | Input (quantum equilibrium assumption) | Input (Pr(α) = D(α,α)) | Input (definitional via ρ = Θρ₀Θ†) |
| Trajectories | Continuous, Brownian paths | No trajectories — history propositions only | Stochastic jumps between configurations |
| Multi-time correlations | Wrong without effective collapse | Correct when decoherence condition holds | Underdetermined (phase freedom) |
| Nonlocality | Explicit (correlated noise for entangled particles) | Present but repackaged (entangled histories) | Encoded in indivisibility of joint matrices |
| Set/process selection | Unique (given ψ) | Highly non-unique (set selection problem) | Non-unique (phase freedom — multiple Θ choices) |
| Measurement problem | Requires effective collapse (circular) | Dissolved via framework choice | Dissolved via stochastic conditioning |
| Relativistic extension | Failed | Natural (timeless formulation possible) | Under development |
| Original developer's assessment | Abandoned by Nelson himself (~2005) | Still active research program | Active development |

*Note on Born rule row: all three entries are "input" in some form — the table entry for Barandes in some sources says "output" (reflecting Barandes' own framing), but Exploration 001's analysis established it is definitional, not derived.*

### 4.4 A Novel Structural Observation: Phase Freedom = Realm Selection Problem

Both Barandes and CH hit a structural wall that may be the same wall in different languages:

- **Barandes:** Multiple phase choices for Θ give multiple valid ISP representations of the same quantum system. No physical criterion selects one.
- **CH:** Multiple consistent families give multiple valid classical descriptions of the same quantum system. No physical criterion selects one (the "realm selection problem").

Mathematically, these may be the same freedom. The off-diagonal elements of ρ (which encode phases in Barandes' framework) are precisely what determines which consistent families exist (via the decoherence functional D(α, α') = Tr(K_α ρ₀ K_{α'}†)). The freedom to choose different phase matrices in Barandes and the freedom to choose different consistent sets in CH may be two perspectives on the same mathematical structure: the non-uniqueness of projecting a quantum density matrix onto classical probability distributions.

This connection has not been made explicit in the literature and may be worth formalizing.

---

## Section 5: Definitive Verdicts

### Verdict 1: Barandes vs. SED

**CATEGORY ERROR — programs in fundamentally different categories.**

More precisely: **Distinct programs with incompatible problem statements.**
- SED = physical theory (reductionist; tries to derive QM from classical physics + ω³ ZPF noise)
- Barandes = mathematical reformulation (re-expresses QM in stochastic language, no physical mechanism)

The comparison is a category error: SED fails *as a physical theory* (wrong predictions for nonlinear systems). Barandes cannot fail in the same way *because it makes no physical predictions beyond QM*. The SED comparison reveals Barandes' essential character: a reformulation that gains freedom from failure by sacrificing physical specificity.

### Verdict 2: Barandes vs. Nelson

**DISTINCT — neither subsumes the other.**

- Different mathematical structures (Markovian diffusion on ℝⁿ vs. non-Markovian kernels on finite N)
- Different ontological commitments (real trajectories vs. mathematical agnosticism)
- Barandes explicitly identifies Nelson as limited by its Markovian assumption
- Nelson is richer in physical content (dynamics, trajectories, ℝ³ extension) but narrower in scope
- Barandes is more general but physically empty and treats multi-time structure as unknowable
- Shared failure: both cannot independently predict QM multi-time correlations (but for opposite reasons)

### Verdict 3: Barandes vs. Consistent Histories

**COMPLEMENTARY — different aspects of the same foundational domain.**

- CH: interpretational (when can probabilities be assigned to sequences of events?)
- Barandes: representational (what is the stochastic mathematical structure of quantum dynamics?)
- Both use decoherence for measurement; neither makes novel predictions beyond QM
- CH naturally handles multi-time correlations; Barandes treats multi-time structure as underdetermined
- Both adopt ontological agnosticism (multiple valid descriptions, no preferred one)
- A potential synthesis: expressing CH's decoherence functional in stochastic kernel language would connect them formally

---

## Section 6: Unexpected Findings

### Finding 1: Barandes Explicitly Never Addresses Consistent Histories

All three of Barandes' main papers (2302.10778, 2309.03085, 2507.21192) discuss Nelson, Bopp, and Fényes as predecessors but never mention consistent/decoherent histories (Griffiths, Omnes, Gell-Mann, Hartle). This is a significant omission. CH is the standard framework for addressing the measurement problem without collapse — the same problem Barandes claims to address. The absence of this comparison in Barandes' work suggests either he is unaware of the structural parallels (unlikely given his depth) or he considers them in different enough categories that no comparison is needed.

### Finding 2: The Multi-Time Problem Has Opposite Character in Nelson vs. Barandes

Nelson's multi-time problem: the process is TOO DETERMINATE (specifies unique paths → wrong conditional probabilities). Barandes' multi-time problem: the process is TOO INDETERMINATE (multiple towers consistent with Γ → no unique multi-time prediction). These are opposite failures, suggesting a fundamental difficulty: to correctly specify QM multi-time correlations from a stochastic description, one needs a description that is neither over-specified (Nelson) nor under-specified (Barandes). Consistent Histories achieves this by directly encoding multi-time structure via the decoherence functional.

### Finding 3: Barandes' Phase Freedom and CH's Realm Selection Problem Are Structurally Analogous

The non-uniqueness of classical description in CH (realm selection: many consistent families, no preferred one) and the non-uniqueness of stochastic representation in Barandes (phase freedom: many Θ matrices, no preferred one) may be two sides of the same mathematical structure — the non-uniqueness of embedding a quantum density matrix into a classical probability space. This connection has not been formalized in the literature. If correct, it would mean: Barandes' "gauge invariance" of the stochastic representation IS CH's realm selection problem, expressed in stochastic kernel language.

### Finding 4: The Doukas (2026) Generalization Partly Dissolves the Nelson-Barandes Distinction

Doukas (2026, arXiv:2602.22095) extended Barandes' framework from θ-processes to general CPTP (Kraus) maps, which CAN accommodate CTMCs. This means the classical stochastic processes that Barandes' original framework excluded are recovered in the Doukas generalization. This generalization moves closer to Nelson's framework (by including Markovian processes) while maintaining the richer structure. Whether the Doukas extension can formally incorporate Nelson-style diffusion processes (for continuous configuration spaces) is an open question.

### Finding 5: SED as a Negative Existence Theorem

The SED failure, reread through Barandes' framework, becomes a negative existence theorem: there is no physical stochastic mechanism (specifically, no ZPF-like field with ω³ spectral density) that is equivalent to Barandes' ISP framework for nonlinear systems. The Barandes framework requires the phase structure (encoded in the complex-valued Θ) to be specified in addition to the real-valued kernel Γ. SED's ZPF fixes a specific phase structure (via the ALD radiation reaction), and this specific choice produces wrong predictions. This sharpen the question: does ANY physical stochastic mechanism successfully specify the phases? Answer: only if it is equivalent to quantum mechanics itself — which is circular.

---

## Summary

The three comparisons produce a clean three-level classification:

**Level 1 (Physical theories — reductionist programs):** SED and Nelson both claim QM behavior emerges from specific physical stochastic mechanisms. Both fail to fully reproduce QM multi-time correlations. SED fails quantitatively (wrong predictions for nonlinear systems). Nelson fails conceptually (wrong multi-time correlations without adding QM collapse back in). These programs are falsifiable and have been shown to be incorrect or incomplete.

**Level 2 (Mathematical reformulation — formal programs):** Barandes systematically recasts QM in stochastic language without specifying a physical mechanism. Succeeds formally (Stochastic-Quantum Theorem) but at the cost of physical specificity. Multi-time structure is explicitly treated as underdetermined. Makes no novel predictions. Cannot fail in the way Level 1 programs fail.

**Level 3 (Interpretational extension — meta-programs):** Consistent Histories works within standard QM formalism and adds rules for when classical probabilities can be assigned to histories. Not a reformulation but an interpretational framework. Correctly handles multi-time correlations. Has its own unresolved problem (realm selection).

Barandes is correctly classified at Level 2. It is distinct from all three comparison programs: SED (Level 1, falsified reductionism), Nelson (Level 1, incomplete reductionism), and CH (Level 3, interpretational extension). The most interesting structural finding is that Barandes (Level 2) and CH (Level 3) share a deep structural parallel — both face the non-uniqueness of classical description — suggesting they may be two different formal languages for the same mathematical problem.

