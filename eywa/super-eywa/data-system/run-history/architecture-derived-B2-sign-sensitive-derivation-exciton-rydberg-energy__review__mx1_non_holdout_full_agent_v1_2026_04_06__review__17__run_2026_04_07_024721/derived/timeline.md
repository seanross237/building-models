# Run Timeline

1. [node_root] Run started for task: Solve this Super-Eywa grading-bank question.
Question ID: architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy
Title: B2. Sign-Sensitive Derivation (Exciton Rydberg Energy)

Problem:
Band gap 3 eV, screened Coulomb, 1s exciton peak at 1 eV.
What is the Rydberg energy for n = 3?

Grading target:
Exact numerical match.
The sign matters.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>
2. [node_root] Node started: Solve this Super-Eywa grading-bank question.
Question ID: architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy
Title: B2. Sign-Sensitive Derivation (Exciton Rydberg Energy)

Problem:
Band gap 3 eV, screened Coulomb, 1s exciton peak at 1 eV.
What is the Rydberg energy for n = 3?

Grading target:
Exact numerical match.
The sign matters.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>
3. [node_root] Node recruited 1 helper(s)
4. [node_root_helper_01] Node started: Review this draft answer carefully.
Find flaws, missing reasoning, or corrections, then produce the strongest corrected answer you can.

Review focus:
Please perform a variable-mapping audit before calculating. 

Step 1: Create a list mapping every numerical value in the problem to its specific physical variable (e.g., 'Value X = Binding Energy E_b') and explicitly define the target quantity's physical meaning (e.g., 'Target = Energy level relative to the band edge').

Step 2: Once the mapping is verified, perform the final calculation. You must pay specific attention to the mathematical sign of the result (whether the energy level is expressed as a positive binding energy or a negative energy level relative to the conduction band edge) to ensure it meets the 'sign-sensitive' requirement of the prompt.

Original question:
Solve this Super-Eywa grading-bank question.
Question ID: architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy
Title: B2. Sign-Sensitive Derivation (Exciton Rydberg Energy)

Problem:
Band gap 3 eV, screened Coulomb, 1s exciton peak at 1 eV.
What is the Rydberg energy for n = 3?

Grading target:
Exact numerical match.
The sign matters.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>

Draft answer:
FINAL_ANSWER: -0.111 eV
JUSTIFICATION: The 1s exciton binding energy is given as E_b(1s) = 1 eV. In a hydrogenic model, the binding energy scales as E_b(n) = E_b(1s) / n^2. For n = 3, E_b(3) = 1 eV / 3^2 = 1/9 eV ≈ 0.111 eV. Since Rydberg energy in this context refers to the energy level relative to the band edge (where the continuum is 0), the energy level is E_n = -E_b(n) = -0.111 eV.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__17__run_2026_04_07_024721
8. [node_root] Run completed with 2 node(s)
