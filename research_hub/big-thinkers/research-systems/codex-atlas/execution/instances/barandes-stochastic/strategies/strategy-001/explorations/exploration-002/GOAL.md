# Exploration 002 — Stochastic Programs Comparison: Barandes vs. SED, Nelson, and Decoherent Histories

## Mission Context

We are investigating whether Barandes' indivisible stochastic dynamics reformulation of QM has physical content beyond standard QM. Exploration 001 established the mathematical framework precisely. Now we need to understand how Barandes relates to other stochastic approaches to QM — especially SED, which we have extensive data on.

## What Exploration 001 Established (Pre-loaded Context)

- Barandes' framework is a **reformulation** of finite-dimensional QM, not a derivation from more fundamental principles
- The Stochastic-Quantum Theorem: "Every ISP can be regarded as a subsystem of a unistochastic process" — essentially Stinespring dilation for stochastic matrices
- Born rule is definitional (density matrix constructed to satisfy it)
- Phase degrees of freedom are NOT determined by stochastic data (3 independent sources of non-uniqueness)
- Measurement "derivation" = standard decoherence repackaged in stochastic language
- CTMCs are excluded from the theta-process framework — "unitary QM is a particular corner of stochasticity" (Doukas 2026)
- Framework is finite-dimensional only; no extension to continuous spaces
- Nelson's multi-time correlation problem is inherited

## Your Task

Compare Barandes' indivisible stochastic dynamics to three other programs that connect stochastic processes to quantum mechanics. For each, determine the precise relationship using a structured comparison along multiple dimensions. Produce a definitive verdict: same, complementary, distinct, or subsumes.

### Comparison 1: Barandes vs. SED (Stochastic Electrodynamics) — MOST CRITICAL

**What SED is:** Classical electrodynamics + a real, Lorentz-invariant electromagnetic zero-point field (ZPF). SED tries to DERIVE quantum behavior from classical physics + stochastic noise. It succeeds exactly for linear systems (harmonic oscillator ground state, Casimir effect, van der Waals forces, blackbody). It fails catastrophically for all nonlinear systems.

**Root cause of SED failure (established by our SED mission, 16 explorations):**
- Santos (2022) proved: SED is formally identical to O(hbar) QED in the Wigner-Weyl representation
- The Moyal bracket expansion: {W,H}_M = {W,H}_P + (hbar^2/24) V'''(x) d^3W/dp^3 + O(hbar^4)
- SED captures only the O(hbar) term. For linear systems, all higher-order terms vanish (exact). For nonlinear systems, the O(hbar^2) corrections are non-zero and SED misses them.
- The physical mechanism: omega^3 spectral density creates positive feedback in nonlinear systems (frequency shifts → more ZPF power → excess energy)
- Quantitative: SED overshoots QM variance by 17.8% for quartic oscillator at beta=1. SED hydrogen self-ionizes (T_ion ~ 19,000 orbital periods at L=1.0).
- Three proposed fixes all fail. The failure is structurally irreparable.

**The critical question:** Why doesn't Barandes hit the same wall? The strategy identifies the expected answer: SED is a **physical theory** (classical EM + ZPF) trying to derive QM from specific dynamics. Barandes is a **reformulation** of the QM formalism itself — it doesn't model the electromagnetic field, doesn't specify a noise source, doesn't derive QM from classical physics. If this is correct, the SED comparison is a **category error** — like asking why Lagrangian mechanics doesn't fail where Newtonian mechanics fails in non-inertial frames (they're the same theory in different language).

**Compare along these dimensions:**
1. **Level of description:** Physical theory vs. mathematical reformulation?
2. **What plays the role of stochasticity:** ZPF noise (SED) vs. indivisibility condition (Barandes)?
3. **Born rule:** Derived approximation (SED, O(hbar)) vs. definitional input (Barandes)?
4. **Where does quantum structure come from:** Emerges from classical physics + noise (SED claim, fails) vs. imported via indivisibility axiom (Barandes)?
5. **Predictions:** SED makes predictions that differ from QM (and are wrong). Does Barandes?
6. **Failure mode:** omega^3 feedback (SED). What is Barandes' failure mode, if any?

**Verdict required:** Is the SED comparison a category error (different levels of description), or does it reveal something about Barandes?

### Comparison 2: Barandes vs. Nelson Stochastic Mechanics (1966)

**What Nelson is:** QM = conservative diffusion in configuration space with diffusion coefficient hbar/2m. The Schrodinger equation IS the Kolmogorov equation for this diffusion.

**Known problems:** Born rule is input. Multi-time correlations wrong (Blanchard et al. 1986). Entanglement requires non-local noise correlations. No relativistic extension.

**Compare along these dimensions:**
1. What stochastic structure is used (diffusion vs. transition kernels)?
2. Is the Born rule input or output?
3. How is the multi-time correlation problem handled?
4. Does one subsume the other?
5. Does Barandes have anything that Nelson doesn't?
6. Does Nelson have anything Barandes doesn't (e.g., a specific dynamical law, trajectories)?

### Comparison 3: Barandes vs. Consistent/Decoherent Histories (Griffiths/Omnes/Gell-Mann/Hartle)

**What consistent histories is:** Standard QM + a set of consistency conditions that determine which histories (sequences of events) can be assigned probabilities. No collapse postulate. Probabilities are fundamental. The decoherence functional determines consistency.

**Compare along these dimensions:**
1. Both claim to handle measurement without collapse — how do their approaches differ?
2. Both involve conditions on when classical-like descriptions apply — how do their conditions relate (consistency vs. indivisibility)?
3. Does Barandes' "division events" concept relate to the decoherence functional?
4. Is Barandes a refinement, restatement, or genuinely different approach to the same problem that consistent histories addresses?

## Success Criteria

- The SED comparison produces a clear structural answer to "why doesn't Barandes fail where SED fails?"
- Each of the 3 comparisons includes a definitive verdict (same / complementary / distinct / subsumes)
- The level-of-description distinction is made precise — not just "they're at different levels" but exactly what this means mathematically
- Unexpected connections or contrasts are identified

## Failure Criteria

- Conflating SED (physical theory) with Barandes (reformulation) without noting the category difference
- Superficial comparison that doesn't engage with the specific technical features of each program
- Missing the multi-time correlation problem as a shared difficulty across stochastic approaches
- Not producing definitive verdicts

## Output

Write REPORT.md and REPORT-SUMMARY.md in your exploration directory (current directory).
