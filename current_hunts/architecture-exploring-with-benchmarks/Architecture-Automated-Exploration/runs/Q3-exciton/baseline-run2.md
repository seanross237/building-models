---
question: Q3-exciton
meta_plan: baseline
run: 2
model: opus-4.6
correct: true
answer_given: 0.08 eV
answer_expected: -0.08
plan_tokens: 0
execution_tokens: 16013
total_tokens: 16013
plan_time_s: 0
execution_time_s: 26
total_time_s: 26
---

## Instance Plan
N/A — baseline (direct solve with T5 prompt)

## Execution Trace
Parsed givens: E_g = 3 eV, 1s resonance = 1 eV. Computed binding energy = 2 eV. Considered screened vs unscreened Coulomb — concluded "simple screened" still uses 2D hydrogen formula. Applied E_n = R_y/(n-1/2)^2. R_y = 0.5 eV. E_3 = 0.08 eV. Checked opposite: could "Rydberg energy" mean R_y itself (0.5 eV)? No — R_y doesn't depend on n. Could it mean resonance energy (2.92 eV)? No — "Rydberg energy" more naturally means binding energy.

## Final Answer
0.08 eV
