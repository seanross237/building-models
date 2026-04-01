# Strategy 001 — Computational Ground-Truth and First Extension

## Objective

Establish a rigorous computational foundation for SED, then push exactly one calculation beyond the known literature to produce a novel, quantitative result. This strategy should produce at minimum a Tier 2 finding (extension with numerical comparison to QED), with a stretch goal of Tier 3 (boundary identification).

The emphasis is on **depth over breadth**. One fully-computed, stress-tested result that compares SED against QED quantitatively is worth more than five sketched arguments about where SED might fail. By the end of this strategy, we should have at least one number we can point to and say: "SED predicts X, QED predicts Y, the discrepancy is Z, and here's why."

## Methodology

### Phase 1: Reproduce (1-2 explorations)

Pick the SED result that provides the best computational on-ramp to novel territory. The harmonic oscillator ground state is the canonical choice — it's the foundation of nearly every SED derivation, and its computational infrastructure (Langevin equation + spectral density of the ZPF) is reused in every extension.

Each reproduction exploration must:
1. **Start from the SED axioms explicitly.** State them. Classical electrodynamics + a real, Lorentz-invariant zero-point radiation field with spectral density ρ(ω) = ℏω³/(2π²c³).
2. **Write and run code.** Solve the stochastic differential equation numerically. Don't just quote the textbook result — compute it independently and verify it matches.
3. **Deliver a reusable computational artifact.** The code from Phase 1 should be structured so Phase 2 explorations can import and extend it.
4. **Identify the assumptions.** What is this derivation assuming that might break for more complex systems? (Dipole approximation? Single particle? Equilibrium?)

The Strategizer should choose which known result to reproduce based on which one provides the best launching pad for the extension directions in Phase 2.

### Phase 2: Extend (2-3 explorations)

Push SED into territory where the literature is thin or contested. The Strategizer chooses which direction, but should prioritize based on:
- **Tractability** — Can it actually be computed in the exploration time budget?
- **Discriminating power** — Will the result clearly distinguish SED from QED? (A quantity where SED and QED agree to 10 decimal places is not interesting. A quantity where they diverge at leading order is very interesting.)
- **Novelty potential** — Is this calculation already in Boyer/de la Peña/Cetto, or is it genuinely new?

Candidate directions (Strategizer picks):
- **Hydrogen atom energy levels in SED.** The SED treatment of hydrogen is notoriously difficult — the 1/r potential doesn't have the stability properties of the harmonic oscillator. The literature has partial results (de la Peña & Cetto's treatment, Boyer's attempts). Compute what SED actually predicts for at least the ground state energy and compare to -13.6 eV.
- **Anharmonic oscillator.** The simplest extension beyond the harmonic case. Add a quartic term (x⁴) and compute the SED ground state energy. Compare against QM perturbation theory for the same potential. This tests whether SED's success is specific to the harmonic case.
- **Two coupled oscillators.** The minimal multi-particle system. Do SED correlations between two oscillators coupled through the shared ZPF reproduce quantum entanglement signatures? Compute the correlation function and compare against the QM prediction.
- **Anomalous magnetic moment (g-2).** Extremely ambitious for a single exploration, but even a partial result (computing the SED vertex correction setup) would be valuable.

Each extension exploration must:
1. **Set up the SED calculation from first principles.** No hand-waving.
2. **Compute the result numerically and/or analytically.**
3. **Compare against the QED/QM prediction for the same quantity.** State the discrepancy with numerical precision.
4. **Identify what assumptions are doing the work.** If SED fails, diagnose *why* — which specific feature of the SED framework breaks?

### Phase 3: Stress-Test (1 exploration)

Take the best result from Phase 2 and attack it:
- Try to break it. Find parameter regimes where the result fails. Check limiting cases.
- Search the literature for prior work. Has anyone already computed this? If yes, does our result agree?
- Identify the strongest counterargument a QFT physicist would raise. Address it.
- If the result is a divergence between SED and QED, verify it's not an artifact of approximation.

This phase turns a computation into a *claim*.

### Cross-Phase Rules

- **Computation is mandatory.** Every exploration must write and execute code. An exploration that only reasons about what SED "should" predict without computing has failed.
- **Numerical precision matters.** Don't say "SED agrees with QM." Say "SED predicts E₀ = -13.58 eV, QM predicts -13.61 eV, discrepancy = 0.2%."
- **Reuse computational artifacts.** Phase 2 explorations should build on Phase 1 code where possible. Include explicit instructions to check for and use prior exploration code.
- **Prior art in every exploration.** Every exploration must include a section on what the existing SED literature says about the quantity being computed. Use web search.

## Validation Criteria

**Minimum success (Tier 1-2):**
- At least one known SED result reproduced with working code
- At least one extension calculation completed with quantitative comparison to QED/QM
- The extension result has numerical precision (not just qualitative agreement/disagreement)

**Good success (Tier 3):**
- A specific observable is identified where SED and QED diverge
- The divergence is quantified and the physical mechanism is identified
- Multiple explorations confirm the boundary from different angles

**Excellent success (Tier 4):**
- A finding that is genuinely new — not already in Boyer, de la Peña, Cetto, or Cole
- Prior art search confirms novelty
- The strongest counterargument has been identified and addressed

## Context

This is the first strategy for this mission. No prior strategies exist.

**Known SED successes (from the literature):**
- Casimir effect: SED derives it from radiation pressure of the ZPF
- van der Waals forces: SED derives the correct 1/r⁶ and 1/r⁷ (retarded) dependence
- Blackbody spectrum: SED + the assumption of thermal equilibrium recovers Planck's law
- Harmonic oscillator: SED predicts the correct ground state energy ½ℏω and probability distribution

**Known SED difficulties:**
- Hydrogen atom: The 1/r Coulomb potential creates instabilities in the SED equations. Partial treatments exist but no definitive resolution.
- Nonlinear systems: SED's success with the harmonic oscillator may depend on linearity. The anharmonic case is not well-studied.
- Multi-particle entanglement: Whether SED can reproduce Bell-inequality-violating correlations is contested. Most physicists believe it cannot, but this has not been conclusively demonstrated computationally.
- Spin: SED does not naturally incorporate spin. The electron's magnetic moment is unclear in the SED framework.

**Key SED literature:**
- T.H. Boyer: Founder of modern SED, extensive work on Casimir effect, blackbody radiation
- L. de la Peña & A.M. Cetto: "The Quantum Dice" — most comprehensive SED monograph
- D.C. Cole: Numerical SED simulations, especially for hydrogen
- T.W. Marshall & E. Santos: SED and Bell inequalities

**Exploration budget:** The Strategizer should plan for 4-6 explorations total across all phases.
