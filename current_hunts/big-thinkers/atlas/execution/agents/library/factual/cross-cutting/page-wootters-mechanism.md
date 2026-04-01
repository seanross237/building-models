---
topic: cross-cutting
confidence: verified
date: 2026-03-25
source: exploration-001-time-from-entanglement (nature-of-time strategy-001)
---

# The Page-Wootters Mechanism: Time from Static Entanglement

## Summary

Page and Wootters (1983) showed that a completely static entangled quantum state — satisfying the Wheeler-DeWitt constraint Ĥ|Ψ⟩ = 0 — produces standard Schrödinger time evolution for subsystems when conditioned on a clock. Time evolution is not fundamental but emerges from entanglement between clock and system within a timeless universe. Experimentally confirmed by Moreva et al. (2014).

## The Mechanism

**Setup:** Divide the total Hilbert space into a clock system C and the rest S:

    H_total = H_C ⊗ H_S

The total state |Ψ⟩ satisfies Ĥ_total|Ψ⟩ = 0 with Ĥ_total = Ĥ_C + Ĥ_S (non-interacting case). The state is static but entangled — it is NOT a product state.

**Conditional state:** When the clock is measured to read t, the conditional state of S is:

    |ψ_S(t)⟩ = ⟨t|_C |Ψ⟩

where |t⟩_C are eigenstates of the clock observable.

**Key result:** Page and Wootters showed this conditional state satisfies:

    iℏ ∂|ψ_S(t)⟩/∂t = Ĥ_S |ψ_S(t)⟩

This is exactly the ordinary Schrödinger equation for S, with t playing the role of time. Standard quantum dynamics — Schrödinger equation, Born rule, unitarity — all emerge from static entanglement.

**Physical interpretation:**
- The universe as a whole does not evolve; the Wheeler-DeWitt equation is satisfied
- From any subsystem's perspective (conditioned on a clock), there IS evolution
- "At time t" means nothing more than "conditioned on the clock reading t"
- Time is a label for clock-system correlations, not a background parameter

## Three Critical Assumptions

1. **No clock-system interaction** — relaxed by Smith & Ahmadi (2019); see below
2. **Clock and system are entangled** — a product state produces no dynamics
3. **Total state is a zero-energy eigenstate** — the Hamiltonian constraint Ĥ|Ψ⟩ = 0

## Experimental Illustration: Moreva et al. (2014)

The first experimental test was performed at INRIM (Turin) using entangled photon polarizations (Phys. Rev. A 89, 052122; arXiv:1310.4691):

- One photon served as the clock, the other as the system
- An "internal" observer who correlates with the clock photon sees the other photon evolve
- An "external" observer measuring only global properties confirms the two-photon state is static
- Both perspectives are simultaneously correct — time is real from the inside, absent from the outside

**Important caveat:** The result was predicted in advance by standard QM without reference to Page-Wootters. The experiment confirms basic entanglement physics (any entangled state looks correlated when both subsystems are measured), not the Page-Wootters ontological claim specifically. The paper itself uses the word "illustration" in its title. The extrapolation from two photons to the universe is unsupported. The experiment is consistent with PW but does not uniquely test it — any interpretation of QM predicts the same outcome.

## Extensions and Refinements

### Smith & Ahmadi (2019): Interacting Clock-System

When gravity couples the clock to the system (unavoidable since "gravity couples to everything"), the Schrödinger equation acquires **time-nonlocal corrections**. The modified dynamics are no longer purely Markovian. These corrections should, in the appropriate limit, reproduce gravitational time dilation, though the full derivation connecting Page-Wootters clocks (internal quantum reference frames) to GR clocks (proper time along worldlines) remains an open problem.

### Giovannetti, Lloyd, Maccone (2015): Resolving Kuchar's Objections

Kuchar objected that different clock choices lead to different dynamics — whose "time" is real? Giovannetti et al. showed that different clocks give **consistent results for physical observables**. The apparent ambiguity is analogous to gauge freedom: different clocks are different descriptions of the same physics.

### Hoehn et al. (2019-2021): Quantum Reference Frame Program

Developed a complete framework for transformations between different clock choices, combining Page-Wootters with Dirac observables. Establishes that the Page-Wootters mechanism and the "evolving constants of motion" approach (Rovelli) are mathematically equivalent perspectives.

## Open Problems

### Unruh-Wald Objections (1989)

Unruh and Wald raised fundamental objections that caused the PW formalism to "lie dormant for some time." They argued that: (1) the conditional probability interpretation requires picking out a "preferred time variable" from the dynamical variables, with no principled selection criterion; (2) constructing proper time operators for semi-bounded Hamiltonians (the physically relevant ones — energies bounded below) faces severe difficulties. While Giovannetti et al. (2015) and Hoehn et al. (2019-2021) address aspects of these objections, the deeper issues persist in quantum gravity contexts.

### Ideal Clock Assumption

The basic mechanism assumes an ideal clock with continuous, unbounded spectrum. Real clocks are finite, bounded, and imperfect. With realistic clocks, the resulting "time evolution" is approximate — fine for phenomenology but undermines the ontological claim that time *is* entanglement.

### The Conditional Probability Problem

The mechanism defines "the state of S at time t" as |ψ_S(t)⟩ = ⟨t|_C |Ψ⟩ — a projection onto clock eigenstate |t⟩. But projection is measurement, importing the measurement problem: what gives us the right to project onto |t⟩? Who or what "measures" the clock? The mechanism thus depends on an unresolved foundational issue in quantum mechanics.

### The Interaction Problem

The basic mechanism assumes no clock-system interaction (Ĥ = Ĥ_C + Ĥ_S). Smith & Ahmadi (2019) showed interactions produce time-nonlocal corrections. But in quantum gravity, everything interacts gravitationally (universal coupling). The "clean" Schrödinger equation derivation works only in the idealized non-interacting case. With interactions, corrections depend on interaction details not derivable from PW itself — the mechanism becomes a perturbation theory starting point, not a fundamental derivation.

### Clock Ambiguity

Different choices of clock subsystem can lead to different dynamics for the rest of the universe. While Giovannetti et al. showed consistency for physical observables, and Hoehn handles transformations between clocks, the multiplicity of possible times remains conceptually uncomfortable.

### Factorization Problem

The mechanism presupposes a tensor product decomposition H = H_C ⊗ H_S. But in quantum gravity, the correct factorization of Hilbert space is itself a dynamical question. In diffeomorphism-invariant theories, localized subsystems are not well-defined in the usual sense. The division into clock and system may be **emergent rather than fundamental**, threatening the logical priority of the argument.

### Recovering Lorentzian Structure

The mechanism produces a *generic* notion of conditioned evolution but does not explain:
- Why the resulting time has Lorentzian character (−,+,+,+)
- Why time combines with space in the specific way described by special and general relativity
- Why there is exactly one time dimension

These properties must come from additional structure beyond the basic Page-Wootters setup.

## Key References

- Page & Wootters (1983), "Evolution without evolution," Phys. Rev. D 27, 2885
- Moreva et al. (2014), arXiv:1310.4691
- Smith & Ahmadi (2019), extension to interacting systems
- Giovannetti, Lloyd, Maccone (2015), resolution of Kuchar's objections
- Hoehn et al. (2019-2021), quantum reference frame program
- Connes & Rovelli (1994), thermal time hypothesis (complementary approach: time from KMS condition)

## Cross-References

- [problem-of-time.md](problem-of-time.md) — Page-Wootters is a Type III (timeless) resolution
- [time-from-entanglement-synthesis.md](time-from-entanglement-synthesis.md) — Page-Wootters as central piece of the unified thesis
- [entanglement-thesis-adversarial-assessment.md](entanglement-thesis-adversarial-assessment.md) — Systematic adversarial review; attacks on PW include circularity (clock is temporal in disguise), factorization vicious circle, and kinematic/dynamic entanglement incoherence
