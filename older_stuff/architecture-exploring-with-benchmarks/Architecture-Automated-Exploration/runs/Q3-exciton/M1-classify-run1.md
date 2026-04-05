---
question: Q3-exciton
meta_plan: M1-classify
run: 1
model: opus-4.6
correct: false
answer_given: 2.92 eV
answer_expected: -0.08
plan_tokens: 16022
execution_tokens: 16579
total_tokens: 32601
plan_time_s: 18
execution_time_s: 16
total_time_s: 34
---

## Instance Plan
Classification: Computation problem in semiconductor exciton physics, requiring 2D hydrogen model.

Steps:
1. Identify 2D exciton formula: E_b(n) = R_y/(n-1/2)^2
2. Relate 1s resonance peak to binding energy: E_peak = E_gap - E_b(n)
3. Extract R_y from 1s binding energy: E_b(1) = 4*R_y
4. Compute n=3 binding energy: E_b(3) = R_y/(5/2)^2
5. Compute resonance peak for n=3: E_peak(3) = E_gap - E_b(3)
   Note: Clarify whether question asks for binding energy or resonance peak.

## Execution Trace
Followed plan steps 1-5. Computed R_y = 0.5 eV, E_b(3) = 0.08 eV, E_peak(3) = 2.92 eV. At interpretation step, noted ambiguity. Reasoned that since problem gave resonance peak for 1s and asks for "Rydberg energy for n=3", the parallel construction suggests they want the resonance peak energy. Answered 2.92 eV.

## Final Answer
2.92 eV (WRONG — should be 0.08, the binding energy)
