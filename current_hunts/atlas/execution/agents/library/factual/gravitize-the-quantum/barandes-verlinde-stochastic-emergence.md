---
topic: gravitize-the-quantum
confidence: provisional
date: 2026-03-25
source: exploration-001-gravitize-the-quantum (quantum-gravity-2 strategy-001)
---

# Barandes-Verlinde Stochastic Emergence of QM and Gravity

## Core Idea

Reality is fundamentally a web of stochastic transitions between configurations. These transitions are "indivisible" — they don't decompose into sequences of intermediate steps (non-Markovian in a strong sense). The mathematical description of these indivisible stochastic processes IS quantum mechanics. Gravity is the macroscopic thermodynamic/entropic signature of the same stochastic causality.

## How QM Emerges (Barandes' Stochastic-Quantum Correspondence)

1. Start with configuration space and stochastic transition kernels Γ(x→y|t)
2. Transitions are "indivisible" — can't break t₁→t₃ into t₁→t₂ and t₂→t₃
3. Mathematical "lifting" procedure: embed stochastic kernels into operators on a Hilbert space
4. In the lifted description, off-diagonal "phase" DOF emerge naturally — they encode multi-time memory making the process indivisible
5. Lifted operators are automatically CPTP (completely positive, trace-preserving) = quantum channels
6. Standard QM emerges as the special case where lifted dynamics is unitary

## Doukas' Key Insight (2025)

Rigorous "lifting procedure" mapping stochastic transition kernels to CPTP quantum maps. Shows:
- One-step stochastic kernels can't distinguish unitaries U_X and U_Y with |U_X|² = |U_Y|² (same transition probabilities but different phases)
- Composition over multiple time steps DOES distinguish them
- **The quantum phase is the compressed encoding of multi-time stochastic memory**
- Derives: quantum operators, density matrices, superposition, interference, Lindblad equations
- Does NOT derive: why nature uses the quantum description, Hilbert space dimensionality, preference for unitary dynamics

## How Gravity Emerges (Verlinde Connection)

- Verlinde: gravity = entropic force from information about material body positions
- Barandes: "gravity is the aggregate signature of underlying stochastic causality, resisting division"
- Combined: the same indivisible stochastic processes that give QM at micro scales give gravity at macro scales via statistical averaging

## Known Problems

| Problem | Status |
|---------|--------|
| No testable predictions beyond standard QM | Acknowledged |
| Gravity connection is purely conceptual | No concrete equations yet |
| Time is assumed, not derived | Fundamental gap |
| Why indivisible stochastic dynamics? | Not derived from deeper principles |
| Conservation laws, gauge symmetries not derived | Major open question |
| No QFT extension | Work in progress |
| Born rule status | Emerges in some formulations but assumptions vary |

## Adversarial Findings (from SCG Devil's Advocate)

The [SCG adversarial assessment](scg-adversarial-assessment.md) identified deep problems with the Barandes-Doukas lifting as a "derivation" of QM:

- **Isomorphism, not derivation:** The theorem runs both ways — it equally well "derives" stochastic processes from QM. The correspondence is symmetric; no mathematical reason to privilege the stochastic direction.
- **Born rule is definitional:** ρ is *constructed* so that ⟨xᵢ|ρ|xᵢ⟩ = p(xᵢ,τ). The Born rule is the construction criterion, not a derived consequence.
- **Phase non-uniqueness dilemma:** Multiple valid Hilbert space representations exist. Either phases are physical (stochastic description incomplete) or not physical (can't account for interference).
- **Indivisibility may smuggle in QM:** Defining processes as "indivisible" (violating Leggett-Garg inequalities) is tantamount to defining them as exhibiting non-classical temporal correlations — quantum mechanics by another name.
- **Aaronson's critique:** After 2.5-hour discussion, Scott Aaronson asked "What does it buy me?" — Barandes wants classical trajectories reproducing QM perfectly but without commitment to any trajectory rule.
- **Nelson multi-time problem inherited:** Single-time probabilities match QM by construction, but multi-time correlations require the phases the stochastic process alone doesn't determine.
- **Publication status:** Key papers appear as preprints / philosophy-of-physics publications, not peer-reviewed physics journals as of 2025.

## Cross-References

- [`adler-singh-trace-dynamics.md`](adler-singh-trace-dynamics.md) — related "QM from deeper stochastic/matrix dynamics" program
- [`stochastic-spacetime-qm-synthesis.md`](stochastic-spacetime-qm-synthesis.md) — synthesis incorporating Barandes lifting as a key step
- [`scg-theory-construction.md`](scg-theory-construction.md) — most developed application: Barandes-Doukas lifting as QM emergence within the full SCG axiomatic framework (5 axioms, geometry from cost function, ℏ = 2mσ²)
