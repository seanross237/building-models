---
topic: quadratic-gravity-fakeon
confidence: provisional
date: 2026-03-26
source: exploration-004-indivisibility-fakeon (quantum-gravity-2 strategy-002)
---

# The Fakeon as Gravitational Indivisibility

## Summary

Novel concept: the fakeon prescription is the gravitational manifestation of stochastic indivisibility (Barandes-Doukas). The massive spin-2 ghost cannot become a real particle because the gravitational process involving it is fundamentally indivisible — it cannot be factored through intermediate states involving the ghost. The concept is **genuinely novel** (no existing literature connects these programs) but **primarily interpretive** — it restates the unitarity argument in stochastic language with three genuine conceptual gains.

**Self-assessment:** Novelty 7/10, Consistency 8/10, Clarity 8/10, Viability 4/10. **Verdict:** Clear physical picture, internally consistent, but no new predictions or calculations. Value is interpretive.

## The Mechanism

Five-step argument:

1. **Barandes-Doukas dictionary:** An indivisible stochastic process has transition kernel Γ(t₀→t₂) ≠ Γ(t₁→t₂) · Γ(t₀→t₁). Factorizability through intermediate times requires all transition probabilities to be non-negative and normalized. Doukas (arXiv:2602.22095, Feb 2026) isolates Chapman-Kolmogorov divisibility as the decisive constraint: CK-consistent CPTP → Lindblad (Markovian); indivisible → non-Lindblad (unitary).

2. **QFT translation:** "Factorizing through an intermediate state" = placing a mode on-shell. Via the optical theorem, Im(M) = Σ_cuts |M_cut|². A real particle with positive residue contributes positively — legitimate intermediate probability.

3. **Negative residue obstruction:** The spin-2 ghost has residue -1 in the propagator decomposition. Feynman prescription cutting yields negative contribution to Im(M). In stochastic language: negative intermediate "transition probability." The process cannot be factored through this state.

4. **Indivisibility selects the fakeon:** Demanding the gravitational process be a consistent indivisible stochastic evolution means the negative-residue pole must never contribute a real intermediate state. This IS the fakeon prescription: project the ghost away from physical cuts.

5. **Positive-residue modes are divisible:** Graviton and scalar have positive residues → positive cut contributions → divisible → Feynman prescription.

**Summary rule:** Negative residue → negative intermediate probability → indivisible → fakeon. Positive residue → positive intermediate probability → divisible → Feynman.

## Three Distinguishing Consequences

### 1. Explains the Analyticity Sacrifice

Indivisible processes encode information in multi-time correlations irreducible to two-time (pairwise) data. Analyticity in QFT allows reconstructing amplitudes from their singularity structure — essentially two-point information (dispersion relations). The fakeon destroys analyticity because the gravitational process carries multi-time information not capturable by analytic continuation. **The analyticity sacrifice is the signature of indivisibility.**

This is the concept's strongest added value — no other interpretation of the fakeon addresses why analyticity must be sacrificed.

### 2. Connects the Fakeon to the Measurement Problem

In the Barandes framework, "divisibility" = classical measurement compatibility (divisible process can be measured at intermediate times). An indivisible process cannot. The fakeon mode is "unmeasurable at intermediate times" — exactly Anselmi's statement that fakeons cannot appear as asymptotic states. The impossibility of detecting the fakeon reflects fundamental indivisibility at the ghost mass scale.

### 3. Suggests a Non-Perturbative Criterion

If the fakeon arises from indivisibility, the non-perturbative completion of QG+F should be characterizable as the most general indivisible stochastic process on the gravitational configuration space. This could provide a handle on the non-perturbative regime where perturbative Feynman diagrams break down.

## Devil's Advocate: Key Objections

1. **Mostly restates unitarity (STRONGEST):** Core logic: negative residue → negative cut → must remove from spectrum. This IS the unitarity argument. Indivisibility adds physical picture but the mathematical content is identical. The concept is genuinely new only if indivisibility imposes STRONGER constraints than unitarity alone.

2. **Isomorphism problem:** Barandes-Doukas lifting is an isomorphism, not a derivation. "Fakeon arises from indivisibility" may just mean "fakeon arises from QM" — true but vacuous.

3. **No QFT extension exists:** Barandes-Doukas works in non-relativistic QM with finite configuration spaces. Extension to QFT requires infinite-dimensional config spaces, Lorentz invariance, renormalization, path integrals. None developed.

4. **Different mathematical objects:** Indivisibility is about time evolution of stochastic processes; fakeon is about momentum-space pole handling. The analogy uses "intermediate state" in two different senses.

5. **Aaronson test:** No new predictions, no new calculations, no new mathematical tools. Main gains: physical picture, analyticity explanation, non-perturbative criterion. **Barely passes.**

## Cross-References

- [`../gravitize-the-quantum/scg-viable-moves-for-qgf.md`](../gravitize-the-quantum/scg-viable-moves-for-qgf.md) — Move 2 (1-paragraph precursor)
- [`../gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md`](../gravitize-the-quantum/barandes-verlinde-stochastic-emergence.md) — Source: Barandes-Doukas framework
- [`analyticity-sacrifice.md`](analyticity-sacrifice.md) — The analyticity cost this concept explains
- [`core-idea.md`](core-idea.md) — Fakeon prescription definition
- [`explanatory-debts-catalog.md`](explanatory-debts-catalog.md) — Gap #1 (fakeon interpretation)
- [`causal-order-fakeon-interpretation.md`](causal-order-fakeon-interpretation.md) — Alternative interpretation (higher viability, lower novelty)

Sources: Barandes (arXiv:2302.10778, 2023); Doukas (arXiv:2602.22095, Feb 2026); Anselmi (JHEP 11(2018)021); Jatkar & Narayan (Nucl. Phys. B 922, 2017)
