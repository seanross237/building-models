# Exploration 002 — Summary

## Goal
Survey the SED computation landscape across five domains (hydrogen, anharmonic oscillators, entanglement/Bell, g-2, other) to identify the best extension direction for a novel SED vs. QM numerical comparison.

## What Was Done
Comprehensive literature survey using web searches and paper analysis. Researched all five target systems, identified key papers with specific results, and assessed tractability, discriminating power, and novelty for each.

## Outcome: SUCCEEDED

### Key Findings

**SED has a sharp "linearity boundary."** Every SED success involves linear systems or free fields (harmonic oscillator, Casimir, van der Waals, blackbody). Every extension to nonlinear potentials, excited states, or interference phenomena has failed:

1. **Hydrogen atom:** Self-ionizes in long simulations (Nieuwenhuizen & Liska 2015). Renormalization doesn't help (Nieuwenhuizen 2020). Effectively closed as a research direction.

2. **Anharmonic oscillator:** Pesquera & Claverie (1982) proved analytically that SED disagrees with QM at order β² in the quartic perturbation. Three distinct signatures: wrong energy, wrong absorption frequencies, broken radiation balance. **This has never been verified numerically.**

3. **Entanglement/Bell:** Deeply contested. Marshall & Santos argue SED is compatible with Bell violations via contextuality. Mainstream physics rejects this. The computational question (simulating Bell correlations from SED dynamics) has not been done and would be intractable.

4. **g-2:** Pure SED has no spin, so g-2 can't be formulated. The SEDS (SED + spin) extension by Cavalleri et al. claims 9th-decimal-place accuracy, but this is non-standard, from a small group, and unverified. Not productive.

5. **Quantum coherence:** Huang & Batelaan (2019) showed SED fails to produce interference fringes for squeezed Schrödinger cat states — a clean falsification.

## Recommendation

**Primary: Anharmonic oscillator ground state energy.** Numerically simulate V(x) = ½mω₀²x² + βx⁴ in SED and compare to QM perturbation theory. This is:
- Maximally tractable (extends harmonic oscillator code with one force term)
- Has a known analytic prediction to verify (Pesquera & Claverie 1982)
- Has well-known QM comparison values (E₀ = 0.5 + 0.75β − 2.625β² + ...)
- Would be the first numerical verification of a 40-year-old analytic result
- Extends beyond perturbation theory to large β where SED vs. QM divergence is maximal
- Directly tests the "linearity boundary" hypothesis

**Secondary: SED tunneling rate** — compute barrier-crossing rates in a double-well potential, compare to WKB. Higher novelty but higher risk.

## Unexpected Findings

The SED anharmonic oscillator paper (Pesquera & Claverie 1982) showing SED ≠ QM at O(β²) has been known for over 40 years but apparently never numerically verified. This is a remarkable gap — it's arguably the cleanest, most important negative result about SED, and it's sitting there waiting for computational confirmation.

Also notable: the quantum coherence failure (Huang & Batelaan 2019) predicts SED will fail for electron double-slit diffraction, but no one has computed this. The paper is very recent.

## Computations Identified

1. **Anharmonic SED oscillator simulation** (recommended next): Solve ẍ = -ω₀²x - 4βx³/m - Γẋ + F_zpf(t), collect ⟨E⟩ vs β, compare to QM. Difficulty: ~100-line Python/scipy script extending exploration-001 code. Would produce a Tier 2-3 result.

2. **SED tunneling rate**: Double-well Langevin simulation, measure first-passage times, compare to WKB rate. Difficulty: ~200-line script, longer simulation times needed. Would be genuinely novel.

3. **Full anharmonic probability distribution**: Beyond just the energy, compute P(x) for the anharmonic SED oscillator and compare to QM |ψ₀(x)|². Would show whether the distribution shape (not just the energy) disagrees. Moderate difficulty, could be combined with computation #1.
