# Goal Analysis — m001-vasseur-pressure

## Classification

| Dimension | Value | Rationale |
|---|---|---|
| **Type** | Research + Computation | Mixed: DNS simulation (computation), mathematical analysis (research), potential proof construction (formal) |
| **Complexity** | Complex | 4-step chain with branching, multiple IC types, resolution convergence, analytical proof attempts |
| **Uncertainty** | High | Outcome depends entirely on Step 1 measurement — three possible branches with different survivability |
| **Measurability** | Quantitative | Primary metric is beta_effective (a number). Kill conditions are numeric thresholds. Clear. |
| **Decomposability** | Serial (with parallel sub-tasks) | Steps are sequential with branching. Within Step 1, multiple ICs can run in parallel. |
| **Domain** | PDE analysis + computational fluid dynamics + harmonic analysis |

## Hierarchy Depth Recommendation

**Depth 2 (Planner + Workers)**

Rationale: Despite the complexity, this mission has a single workstream with well-specified branching logic and clear kill conditions at every step. The mission document itself IS the strategy — it lays out exactly what to do at each branch point with quantitative thresholds. A Conductor on top would be redundant — there's no strategic ambiguity to resolve.

The Planner can handle the branching: evaluate Step 1 results against the kill conditions, then design Step 2A/2B/2C tasks accordingly. This is task-level adaptation, not strategic pivoting.

Cross-reference: Complex + High uncertainty normally suggests depth 3-4. But decomposability is serial (one workstream) and measurability is quantitative (clear success criteria). The tie-breaking rule says: serial decomposability → prefer shallower.

Task budget: 10-15 tasks across all steps.

## Worker Types Needed

- **Math Worker** — Vasseur framework analysis, De Giorgi iteration theory, Tran-Yu verification, proof attempts (Step 2A, 3)
- **Code Worker** — DNS solver setup/validation, simulation runs, data extraction (Step 1)
- **Analysis Worker** — CZ decomposition, beta_effective measurement, result synthesis
- **Research Worker** — Literature survey (Brandolini-Chiacchio-Trombetti, Vasseur-Yu, etc.)
- **Adversarial Worker** — Review claims, check for circular reasoning, stress-test beta measurements

## Library

Include Librarian + Curator. This mission builds on prior Atlas NS work and will accumulate findings across multiple steps. Knowledge retrieval before each task is valuable.
