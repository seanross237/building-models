---
question: Q3-exciton
meta_plan: M5-vanilla
run: 1
model: opus-4.6
correct: true
answer_given: 0.08 eV
answer_expected: -0.08
plan_tokens: 15958
execution_tokens: 16434
total_tokens: 32392
plan_time_s: 16
execution_time_s: 14
total_time_s: 30
---

## Instance Plan
Steps:
1. Identify 2D exciton formula: E_n = E_Ry/(n-1/2)^2
2. Extract 1s binding energy: E_gap - E_resonance
3. Compute E_Ry from 1s binding: E_Ry = E_binding(1s)/4
4. Compute E_binding(n=3) = E_Ry/6.25
5. Compute E_resonance(n=3) = E_gap - E_binding(3)
6. Clarify: "Rydberg energy for n=3" likely means binding energy at n=3

## Execution Trace
Followed plan. R_y = 0.5 eV, E_binding(3) = 0.08 eV, E_resonance(3) = 2.92 eV. Applied exclusion principle: R_y doesn't depend on n, so "for n=3" must mean binding energy. Cross-checked physically: higher states closer to band edge with smaller binding.

## Final Answer
0.08 eV
