---
question: Q3-exciton
meta_plan: M1-classify
run: 2
model: opus-4.6
correct: true
answer_given: 0.08 eV
answer_expected: -0.08
plan_tokens: 16022
execution_tokens: 16512
total_tokens: 32534
plan_time_s: 19
execution_time_s: 17
total_time_s: 36
---

## Instance Plan
Classification: Computation problem requiring 2D hydrogen-like model for Wannier excitons.

Steps:
1. Recall 2D exciton formula: E_binding(n) = R_y/(n-1/2)^2
2. Relationship: E_resonance(n) = E_gap - E_binding(n)
3. Extract 1s binding energy: E_gap - E_resonance(1s)
4. Solve for R_y = E_binding(1s)/4
5. Compute E_binding(3) = R_y/6.25
6. Compute E_resonance(3) = E_gap - E_binding(3)
7. Clarify: "Rydberg energy for n=3" most likely means binding energy at n=3.

## Execution Trace
Followed plan. R_y = 0.5 eV, E_binding(3) = 0.08 eV. Applied exclusion principle: "Rydberg energy for n=3" must mean state-specific energy since R_y itself doesn't depend on n. Concluded binding energy is the answer.

## Final Answer
0.08 eV
