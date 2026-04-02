# Exploration 004 — Summary

## Goal
Investigate whether cost function constraints in the Pedraza et al. (2023) complexity-geometry framework can select ghost-free higher-derivative gravity — specifically QG+F (quadratic gravity with fakeon quantization).

## What Was Tried
Deep technical analysis of three interacting frameworks:
1. **Pedraza et al.'s "spacetime complexity" principle** (arXiv: 2306.08503): Einstein equations emerge from optimizing CV complexity; modified cost functions yield higher-derivative gravity.
2. **QG+F (Anselmi-Piva)**: The quadratic gravity Lagrangian L = R + αC² + βR² with the ghost pole quantized as a fakeon (purely virtual particle) — the unique perturbatively UV-complete QG.
3. **Nielsen complexity geometry**: Cost function constraints (penalty factor positive-definiteness) create a "landscape/swampland" of viable complexity measures.

Attempted to construct a logical chain: cost function constraints → ghost-freedom → QG+F selection.

## Outcome: FAILURE (with instructive reasons)

**Cost function constraints cannot select QG+F.** Four fundamental obstacles:

1. **Too much freedom**: The "complexity = anything" framework (Pedraza et al. 2025) shows infinitely many valid complexity functionals. Known constraints (linear growth, switchback, positivity) are necessary but vastly insufficient.

2. **Wrong inference direction**: The framework maps FROM bulk gravity TO complexity. The reverse is degenerate — many cost functions are compatible with many theories.

3. **Classical vs. quantum gap**: The cost function is a classical geometric object. The fakeon prescription is a quantum choice about propagator contours. Stelle gravity and QG+F have identical Lagrangians — no classical cost function can distinguish them.

4. **IR vs. UV mismatch**: Known complexity constraints are infrared (growth rates, asymptotics). Ghost-freedom is ultraviolet (propagator pole structure). No mapping connects the two.

## Key Takeaway

**The deepest obstacle is #3: the fakeon prescription operates at the quantization level, not the Lagrangian level.** Since the cost function encodes the classical geometry (which is the same for Stelle and QG+F), it is structurally incapable of distinguishing the two theories. To select QG+F from a computational framework, one would need a "quantum cost function" that constrains how fluctuations around the optimal geometry are quantized — a significant extension beyond the current framework.

## Leads Worth Pursuing

- **The penalty factor landscape/swampland** (Flory et al. 2026): positive-definiteness of the complexity metric IS structurally analogous to ghost-freedom. If a holographic dictionary mapping penalty factor positive-definiteness → bulk positive spectral weight could be established, this would bridge the gap.
- **CFT unitarity constraints** provide sign/magnitude bounds on higher-derivative couplings via conformal collider bounds and bootstrap, but give ranges, not unique values.
- **The core insight for SCG**: the computational cost framework can derive the Einstein equations and parameterize higher-derivative extensions, but it needs additional quantum-level input to select the quantization scheme. The fakeon prescription must be imposed as an independent principle — it doesn't emerge from classical cost function optimization.
