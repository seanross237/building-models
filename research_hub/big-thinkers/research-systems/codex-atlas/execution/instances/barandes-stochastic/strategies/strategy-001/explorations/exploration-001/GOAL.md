# Exploration 001 — Mathematical Framework Extraction: Barandes' Indivisible Stochastic Dynamics

## Mission Context

We are investigating whether Jacob Barandes' reformulation of quantum mechanics as "indivisible stochastic dynamics" reveals structure, predictions, or constraints beyond standard QM — or whether it is purely a notational reformulation. This first exploration establishes the mathematical ground truth: what does Barandes actually claim, prove, and assume?

## Your Task

Read and extract the precise mathematical framework from these papers:
- **Barandes arXiv:2302.10778** (2023) — "The stochastic-quantum correspondence"
- **Barandes arXiv:2309.03085** (2023) — Follow-up paper
- **Doukas arXiv:2602.22095** (2026) — Rigorous lifting procedure
- **Any other Barandes papers you find** on this topic (check his arXiv profile)

Your task is EXTRACTION, not evaluation. Produce a precise mathematical summary at theorem-level rigor, not a paraphrase of claims. If the papers contain hand-waving where a proof should be, note exactly where.

## What to Extract (in this order)

### Stage 1: Precise Definitions
- What EXACTLY is an "indivisible stochastic process"? Give the formal definition. How does it relate to non-Markovianity? Is it stronger, weaker, or different?
- What is a "divisible" stochastic process? What is the "divisibility condition" mathematically?
- What is the configuration space? Is it finite, countable, or continuous? Does the framework work for all three?
- What are the stochastic transition kernels? Are they doubly stochastic? What properties are assumed?

### Stage 2: Precise Theorems
- What EXACTLY does the lifting theorem prove? State it as a formal theorem with all assumptions and conclusions.
- In what direction does the correspondence run? Stochastic → quantum? Quantum → stochastic? Both? Is it an isomorphism?
- What is the relationship between transition kernels and quantum channels (CPTP maps)? Is it one-to-one, many-to-one, or one-to-many?
- What role do the off-diagonal "phase" degrees of freedom play? Are they determined by the stochastic data or are they free parameters?
- What does Doukas (2026) prove beyond what Barandes (2023) claimed?

### Stage 3: Scope Conditions
- Finite-dimensional vs. infinite-dimensional: where does the framework work? What breaks in infinite dimensions?
- Single-particle vs. multi-particle: what happens with entanglement?
- Non-relativistic vs. relativistic: is there a QFT extension?
- Open vs. closed systems: how do dissipation and decoherence fit?
- Which observables are covered? Only position-basis measurements, or arbitrary observables?

### Stage 4: The Measurement Claim
- Barandes claims the measurement postulate is derived, not assumed. What EXACTLY is claimed?
- What assumptions go into this derivation? Write them down explicitly.
- How does "collapse" appear in the stochastic formulation?
- Is this the same as decoherence, or genuinely different?

### Stage 5: Known Failure Points and Open Questions
Identify at least 3 places where the framework's claims exceed its proofs. For each, explain exactly what gap exists.

## Adversarial Context (Pre-loaded — Address These)

A prior adversarial assessment raised these objections. For each one, determine whether it is a correct characterization of what Barandes claims:

1. **Isomorphism, not derivation:** The lifting theorem runs both ways — it equally well "derives" stochastic processes from QM. Is this true? Does Barandes acknowledge it?

2. **Born rule is definitional:** The density matrix rho is constructed so that <x_i|rho|x_i> = p(x_i, tau). Is the Born rule an input or output? Be precise about what is assumed vs. derived.

3. **Phase non-uniqueness:** Multiple Hilbert space representations exist for the same stochastic process. Does Barandes address this? How?

4. **Indivisibility smuggles in QM:** Defining processes as "indivisible" (violating Leggett-Garg) is tantamount to defining them as non-classical. Is this a fair characterization?

5. **Nelson's multi-time problem (Blanchard et al. 1986):** Single-time probabilities match by construction, but multi-time correlations require the phases the stochastic process alone doesn't determine. Does Barandes' framework address this?

For each claim, classify it as:
- **(a) Algebraic identity** — true by construction, part of the mathematical framework
- **(b) Standard physics consequence** — follows from known QM/stochastic process theory
- **(c) Novel physical claim** — requires new assumptions specific to Barandes

## Success Criteria
- All definitions in Stage 1 are stated formally (not paraphrased)
- The lifting theorem is stated with all assumptions explicit
- The direction and structure of the correspondence is clear (isomorphism vs. one-way)
- Phase degrees of freedom are characterized: determined vs. free
- All 5 adversarial objections are addressed with reference to the actual papers (page/section numbers)
- At least 3 gaps between claims and proofs are identified

## Failure Criteria
- Paraphrasing Barandes' claims without checking the mathematical details
- Conflating Barandes' framework with SCG (Stochastic Computational Gravity) — they are different programs
- Missing the Doukas (2026) paper if it exists
- Not finding or reading the actual papers (this exploration requires web access to arXiv)

## Output
Write your findings to REPORT.md and a concise summary to REPORT-SUMMARY.md in your exploration directory. Use exact quotes from the papers where possible, with arXiv page/section references.

Your exploration directory is: the current directory (where this GOAL.md is located).
