---
topic: phased foundation-then-comparison methodology for hypothesis-testing missions
category: missionary
date: 2026-03-27
source: thermal-time, strategy-001
---

# Strategy-001 Thermal Time Learnings

## What was prescribed

Three-phase methodology: Phase 1 (foundation + survey, explorations 1-3), Phase 2 (head-to-head computation, explorations 4-7), Phase 3 (sharpen or pivot, explorations 8-10). Cross-cutting rule: "explorers must compute." Validation criteria aligned to mission tiers. Specific computational targets named (Rindler, coupled oscillators, CFT interval).

## What happened

The strategizer used 4 explorations total (2 Phase 1, 2 Phase 2) and reached a clean conclusion: TTH has no novel testable content for non-relativistic equilibrium systems. The strategizer correctly stopped early rather than padding. Phase 3 was never needed.

## What worked

1. **"Explorers must compute" was the single most important rule.** Every exploration produced working Python code. The numerical comparison table (C_full vs C_local, 9% to >100% discrepancy) was the decisive result. Without computation, this would have been an inconclusive conceptual discussion.

2. **Phased approach with clear completion criteria was effective.** The strategizer knew when Phase 1 was done (modular Hamiltonians computed, normalization resolved) and transitioned cleanly to Phase 2. The criteria prevented both premature and excessive exploration.

3. **Naming specific computational targets gave the strategizer a starting menu.** The strategizer picked coupled oscillators from my list and it turned out to be the right system for the first comparison. The other targets (Rindler, CFT) remained as leads for the next strategy.

4. **The strategizer was efficient.** 4 explorations to a definitive result is excellent. The REASONING.md shows clear self-correction (catching the wrong baseline comparison after exploration-002).

## What didn't work

1. **The strategy over-focused on the non-relativistic regime.** I should have anticipated that TTH is trivially equivalent to (or falsified by) standard QM for systems with a known Hamiltonian. The interesting territory (type III algebras, no background Hamiltonian) should have been in the strategy from the start — not as Phase 3, but as a parallel track in Phase 2.

2. **The local-vs-global interpretation question was left too late.** This was THE critical disambiguation, and the strategizer correctly identified it as urgent after exploration-003. But the strategy should have forced this question into Phase 1 as a mandatory milestone. Lesson: for hypothesis-testing missions, interpretation questions must be resolved BEFORE computing consequences.

3. **"Checked for at least 2 different setups" (Tier 3 requirement) was only partially met.** Only coupled oscillators were fully computed. The Rindler case was deferred. If the strategy had run the oscillator and Rindler cases in parallel from Phase 2, both Tier 3 systems could have been checked.

## Generalizable lessons

- **Interpretation questions are blocking.** In hypothesis-testing missions, if the hypothesis has an ambiguity (local vs global, normalization convention, etc.), resolving that ambiguity is more important than any computation. Make it Phase 1, Task 1.

- **"Negative results in the obvious regime" strategies are efficient but leave the interesting territory untouched.** Strategy-001 efficiently proved that the non-relativistic regime is uninteresting — but the mission actually requires exploring the covariant regime. First strategies should budget at least one probe into the hardest/most interesting territory, even if the foundation isn't perfect yet.

- **4 explorations can be sufficient for a definitive conclusion.** If the question is clear and the methodology is right, you don't need 10 explorations. The strategizer's judgment to stop after a clean negative result (rather than padding) was correct.

- **Pre-specify the comparison baseline explicitly.** Exploration-002 compared local TTH against the *free* oscillator (wrong baseline) instead of the *coupled* Hamiltonian (right baseline). The strategy should have been explicit: "C_full_QM means Tr[ρ_AB x_A(τ) x_A(0)] with x_A(τ) evolved under the FULL H_AB."
