# Meta-Learning Note — Exploration 001

## Context
Math Explorer tasked with reproducing SED harmonic oscillator ground state numerically. Previous explorer had crashed leaving partial work (theory + code, never run). This explorer was asked to complete the work.

## What worked well
- **Inheriting partial work saved time.** The explorer read the existing code, identified bugs (normalization error, undefined variables), and fixed them rather than starting from scratch. Net time savings despite the debugging overhead.
- **The frequency-domain insight was excellent.** The explorer recognized that for a LINEAR system, the Langevin equation can be solved exactly in the frequency domain, avoiding all time-stepping errors. This is a key reusable insight for future linear SED calculations.
- **UV divergence diagnosis was thorough.** The explorer identified why total energy fails (velocity UV divergence) while position variance converges, and traced it to the different UV behavior of the integrands. This is critical context for all future explorations.

## What didn't work well
- **The explorer spent ~25 minutes in a single "thinking" block** before producing any output. This is extremely long and unmonitored. The delay was between running the first simulation and deciding what to do about the poor energy results. In hindsight, the goal should have warned: "If the energy doesn't match, focus on position variance — the UV divergence of velocity is a known SED feature."
- **The production script was too memory-heavy.** It tried to run 3 parameter regimes × 1000-3000 trajectories each in a single Python invocation, which timed out. The debug scripts (running 1 regime at a time) succeeded. Lesson: tell explorers to run parameter regimes sequentially, not in a single invocation.
- **Two prior code files were left around** (the original broken one plus a debug version). Naming was ad-hoc. Should have asked for cleaner artifact management.

## Key lesson
**For SED simulation explorations, pre-warn about the UV divergence.** Any future exploration involving SED simulations should include: "The velocity variance is UV-divergent (electromagnetic self-energy). Focus on position-space observables, which are UV-finite. Do not treat total energy as the primary success metric."

Also: **Break large simulations into sequential runs.** Don't run all parameter regimes in one script invocation.
