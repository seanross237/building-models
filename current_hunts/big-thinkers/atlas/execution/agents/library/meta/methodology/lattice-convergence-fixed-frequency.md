---
topic: Use fixed physical frequency (not fixed mode index) for lattice QFT convergence tests
category: methodology
date: 2026-03-28
source: "thermal-time strategy-002 meta-exploration-001"
---

## Lesson

When testing convergence of a lattice QFT computation as N increases, use a **fixed physical frequency** (omega ~ constant) across all N values, not a fixed mode index. Mode indices have N-dependent frequencies (e.g., omega_m = m*pi/(N+1)), so fixing the mode number tests a DIFFERENT physical observable at each N. The correct approach: select the mode closest to a target frequency at each N value.

Additionally, when convergence results are ambiguous, use **multi-angle convergence analysis**: test at least two different convergence strategies (e.g., fixed-mode AND fixed-frequency) to distinguish genuine physical effects from IR/UV artifacts.

## Evidence

- **thermal-time strategy-002 exploration-003** — The explorer tested both mode-0 convergence (fixed mode, omega -> 0) and fixed-frequency convergence (omega ~ 0.3). Mode-0 showed APPARENT convergence: delta_disc ~ N^{-0.46}. Fixed-frequency showed the OPPOSITE: delta_disc ~ N^{+0.33} (growing!). The mode-0 "convergence" was an artifact — omega_0 = pi/(N+1) -> 0 as N grows, making the physical correction delta_C_full -> constant, so the L2 metric measured only the DC offset. The explorer caught this by testing both strategies, which was the exploration's most important methodological discovery.

## Design Pattern

**For lattice convergence studies, specify in the GOAL.md:**

1. "Select the mode with physical frequency closest to omega_target = [value] at each N."
2. "Report omega_actual for each N to confirm stability."
3. "Also run at fixed mode-0 as a control to identify IR artifacts."
4. "Compare the N-dependence of the two strategies."

The dual-strategy approach is cheap (same code, different mode selection) and can reveal artifacts that neither strategy alone would catch.

## When to Apply

- Any lattice QFT computation where the claim is "this quantity converges/diverges in the continuum limit"
- Especially when the lowest mode (mode 0) has omega -> 0 as N -> infinity
- When convergence exponents are reported as power laws — check that the exponent isn't an artifact of the mode-selection strategy

## Relationship to Other Entries

- `staged-computation-goals.md` — This is a specific instance of the staged pattern: run the convergence analysis as a stage after the main computation, with explicit comparison between strategies.
- `include-trivial-control-checks.md` — The fixed-mode run serves as a control that makes the fixed-frequency result more trustworthy.
