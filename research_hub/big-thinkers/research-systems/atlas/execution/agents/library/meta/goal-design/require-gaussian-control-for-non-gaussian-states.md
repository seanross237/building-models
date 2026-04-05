---
topic: For non-Gaussian states, always request a Gaussian control state
category: goal-design
date: 2026-03-28
source: "thermal-time strategy-002 meta-exploration-001, thermal-time strategy-003 meta-exploration-001"
---

## Lesson

When a computation involves a **non-Gaussian quantum state** and uses a **Gaussian approximation** (e.g., quadratic modular Hamiltonian from covariance matrices), always request a parallel computation with a **Gaussian control state** (coherent state excitation, squeezed vacuum, etc.) to isolate the approximation artifact from the physical effect.

The Gaussian approximation captures two-point functions exactly but misses connected higher-order correlators. For a non-Gaussian state, the true modular Hamiltonian has non-quadratic terms. Without a Gaussian control, it is impossible to determine how much of the observed discrepancy comes from the physics and how much from the approximation.

## Evidence

- **thermal-time strategy-002 exploration-003** — The one-particle excitation |1_m> is non-Gaussian. The Gaussian approximation produced a modular Hamiltonian that oscillates at the wrong frequencies (entanglement spectrum, not physical). The meta note identified: "The goal should have specified: 'If using Gaussian approximation, also test with a coherent state (which IS Gaussian) to isolate the approximation artifact.'" This was not done, leaving a proof gap — the structural frequency mismatch could be partially a Gaussian approximation artifact, though the magnitude makes this unlikely.

- **thermal-time strategy-003 exploration-001 [CONFIRMATION]** — The Gaussian control pattern was executed as designed: coherent state (easy validation, confirms pipeline) + squeezed vacuum (hard test, exact modular Hamiltonian). Result: the squeezed vacuum reproduced the identical structural mismatch — modular flow at modular frequencies, physical frequency absent, discrepancy growing as N^{0.44}. The coherent state confirmed the pipeline at machine precision. **The proof gap from s002-E003 is now closed.** Pre-loading analytical predictions for the coherent state let the explorer verify it quickly and move on to the more important squeezed test.

## Design Pattern

**In GOAL.md, when the target state is non-Gaussian:**

"Compute [observable] for two states:
1. Target state: [non-Gaussian state, e.g., one-particle excitation]
2. Control state: [Gaussian state with comparable parameters, e.g., coherent state with same mean occupation]

If the Gaussian control shows the same discrepancy pattern as the target, the effect is robust to the Gaussian approximation. If it differs, quantify the Gaussian approximation error as |result_target - result_control| and report it as a systematic uncertainty."

**Two-tier variant (CONFIRMED by s003-E001):** Structure as easy-then-hard:
1. **Easy Gaussian control** (e.g., coherent state): validates computational pipeline, expected to show no effect (matches vacuum). Pre-load the analytical prediction so the explorer can verify quickly and move on.
2. **Hard Gaussian test** (e.g., squeezed vacuum): the real test — same observable, exact modular Hamiltonian, no approximation. If the hard test reproduces the same structural pattern as the non-Gaussian target, the caveat is resolved.

This two-tier design ensures the explorer doesn't waste time debugging the hard case when the pipeline itself might be wrong.

## Gaussian States for Common Non-Gaussian States

| Non-Gaussian state | Gaussian control | Rationale |
|--------------------|-----------------|-----------|
| One-particle excitation | Coherent state (same amplitude) | Same energy, Gaussian |
| Fock state |n> | Squeezed vacuum (same variance) | Same second moments |
| Cat state | Squeezed thermal state | Similar covariance |
| Post-measurement state | Pre-measurement state (if Gaussian) | Same correlators without projection |

## When to Apply

- Any computation using Williamson decomposition or Gaussian state formalism for a state that is NOT Gaussian
- When the modular Hamiltonian is approximated as quadratic
- When the result shows a structural discrepancy that could be attributed to the approximation
- NOT needed for: thermal states, vacuum states, squeezed states, coherent states — these are already Gaussian

## Relationship to Other Entries

- `include-trivial-control-checks.md` — A Gaussian control is NOT trivial (it requires a separate full computation), but serves the same validation function.
- `specify-computation-parameters.md` — The Gaussian control is a parameter choice that should be specified explicitly.
