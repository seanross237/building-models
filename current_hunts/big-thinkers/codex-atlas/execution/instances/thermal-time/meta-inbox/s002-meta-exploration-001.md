# Meta-Learning: Strategy-002 Explorations 001-003

## What worked well

1. **Parallel launch of all three probes.** The three Phase 1 probes were independent and ran simultaneously. All three completed successfully. This is the ideal pattern for Phase 1 survey/verification explorations.

2. **Exact analytical formulas in E002.** The explorer derived exact closed-form expressions for both correlators, then verified numerics against them. This eliminates all doubt about the numerical results. Future goals should explicitly request "derive the analytical formula if possible, then verify numerics against it."

3. **Multiple convergence strategies in E003.** The explorer tested both mode-0 (ω → 0) and fixed-frequency convergence, discovering that mode-0 convergence was an artifact. This kind of multi-angle convergence analysis should be requested by default for lattice computations.

4. **Pre-loading strategy-001 context.** Including the normalization resolution, local interpretation confirmation, and code paths in every GOAL.md prevented re-derivation and kept explorers focused.

## What didn't work well

1. **E001 GOAL had a physics error.** The goal asked for C_local ≈ C_full (modular flow ≈ time evolution), but BW says modular flow = boost, not time translation. The explorer caught this and corrected course, but a better goal would have specified the boost comparison from the start. **Lesson: for QFT/relativity problems, be precise about which Poincaré transformation is involved.**

2. **E003 Gaussian approximation caveat.** The excited-state probe used a Gaussian approximation for a non-Gaussian state. This leaves a proof gap. The goal should have specified: "If using Gaussian approximation, also test with a coherent state (which IS Gaussian) to isolate the approximation artifact."

3. **No adversarial exploration.** Strategy-002 ran only 3 of the budgeted 10 explorations. The results are strong but unverified by adversarial review. Should have launched at least an adversarial probe.

## Lessons for future strategizers

- **Lattice QFT goals must specify which symmetry generator** (boost vs. time translation vs. rotation) the modular flow should be compared against. "Compare to full QM" is ambiguous in relativistic settings.
- **For non-Gaussian states, always request a Gaussian control** (coherent state) alongside the target state.
- **The Williamson decomposition** (not Peschel's fermionic formula) is the correct tool for bosonic lattice modular Hamiltonians. Goals should specify this for bosonic fields.
- **Fixed-frequency convergence** is the right metric for lattice QFT, not fixed-mode convergence (modes change frequency as N changes).
