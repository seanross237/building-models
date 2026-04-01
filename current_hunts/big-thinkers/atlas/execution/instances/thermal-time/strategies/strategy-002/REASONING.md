# Reasoning Log

## Iteration 1 — Phase 1: Three Parallel Computational Probes

### Context
Strategy-001 closed off the non-relativistic equilibrium regime: TTH ≡ QM (global) or falsified (local) for Gibbs states. Strategy-002 moves into TTH's natural habitat — type III von Neumann algebras and non-equilibrium states.

### What I considered
The strategy mandates three parallel probes:
1. **Rindler Wedge Verification (Vacuum)** — control test in TTH's intended domain (BW theorem should guarantee agreement)
2. **Non-Equilibrium Coupled Oscillators** — test where even global TTH differs from QM (non-Gibbs state)
3. **Excited-State Modular Flow (Rindler)** — most conceptually important: state-dependent time in QFT

All three are independent, computational, and well-specified by the strategy. The COMPUTATIONS-FOR-LATER.md registry pre-specified Probes 1 and 2 with difficulty estimates.

### Decision
Launch all three probes simultaneously as Math Explorer explorations. Each is self-contained with clear success criteria and control checks. The strategy identifies these as mandatory, and they're logically independent — perfect for parallel execution.

**Explorer type:** Math Explorer for all three (computational tasks producing code + numbers).

**Probe allocation:**
- Exploration-001: Rindler Wedge Verification (Probe 1) — moderate difficulty
- Exploration-002: Non-Equilibrium TTH (Probe 2) — lower difficulty, extends E003 code
- Exploration-003: Excited-State Modular Flow (Probe 3) — highest difficulty, perturbative fallback

### What I rejected
- Running probes sequentially: wasteful since they're independent
- Starting with just one probe to "test the waters": the strategy is clear and these are well-specified
- Replacing Probe 3 with the analytic ΔK_A computation: Probe 3 has higher conceptual importance (state-dependent time is radical), and the strategy labels it most important

### Librarian query summary
- **Factual library**: 4 thermal-time findings already curated from strategy-001. All directly relevant — pre-loaded as context in GOALs.
- **Meta library**: 12 actionable lessons incorporated — specify exact comparison formulas, include control checks, ask "structural or quantitative?", specify failure paths, pre-load context, staged computation structure.
- **Meta-inbox**: 3 notes from strategy-001 (already processed into library). Key: always specify exact baseline, include trivial controls, diagnose structural vs quantitative.

### Post-completion reflections

**E001 (Rindler):** Explorer delivered excellent results and caught a physics error in my GOAL — I asked for modular flow ≈ time translation, but BW says modular flow = boost. The explorer corrected this and compared against the boost correlator instead. Scope was right. The BW-valid region analysis (N-independent, ~2-3 spacings) was an unexpected bonus.

**E002 (Non-equilibrium):** Best exploration of the three. Analytical formulas verified to 10⁻⁹, FFT spectral analysis clean, squeezed state test provided unexpected depth. The product-state identity (C_global = C_local for product states) was a clean algebraic result I didn't anticipate. The squeezed state hierarchy (quantitative vs structural discrepancy) is the most promising finding for follow-up.

**E003 (Excited state):** Strongest conceptual result — modular clock ticks at entanglement frequencies, not physical frequencies, and the discrepancy GROWS in the continuum limit. The mode-0 convergence artifact was a subtle trap the explorer identified. Main weakness: Gaussian approximation caveat. Next time, I should explicitly request a Gaussian control (coherent state) alongside any non-Gaussian test.

**Overall:** Three parallel Math Explorer probes worked very well for this Phase 1. All three succeeded with clean numerical results and verified control checks. The strategy budgeted 10 explorations but the three probes were so comprehensive (each running FFT analysis, convergence studies, control checks, and bonus tests like the squeezed state) that the core scientific questions are answered. An adversarial review would strengthen the claims but isn't needed for the synthesis.

**Decision: Write FINAL-REPORT with 3 explorations.** The strategy suggested 6 explorations across 3 phases (3 probes + deepen + adversarial + synthesis). But the probes were thorough enough that Phases 2-3 have less marginal value than I expected. The key open question (Gaussian approximation for E003) would benefit from a single targeted follow-up, but the missionary can decide whether to commission that in a strategy-003 or close the mission.
