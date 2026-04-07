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
Please perform a variable-mapping and derivation audit on this response. 

1. **Variable Mapping**: Create a list mapping every numerical value in the problem to its specific physical variable (e.g., '3 eV = Band Gap E_g', '1 eV = 1s Exciton Peak Energy E_peak', '1 eV = 1s Binding Energy E_b').

2. **Derivation Audit**: Perform the final calculation by explicitly substituting these mapped variables into the Rydberg scaling formula (E_n = E_b / n^2). 

3. **Verification**: Pay specific attention to the mathematical sign (is the Rydberg energy expressed as a magnitude or a binding energy?) and the units. Ensure the final result matches the 1/n^2 scaling requirement for n=3.

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
FINAL_ANSWER: 0.1111 eV
JUSTIFICATION: The 1s exciton peak is at 1 eV below the band gap, meaning the 1s binding energy (E_b) is 1 eV. For a hydrogenic exciton model, the energy levels scale as E_n = E_b / n^2. For n = 3, E_3 = 1 eV / 3^2 = 1/9 eV ≈ 0.1111 eV.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__12__run_2026_04_07_024217
8. [node_root] Run completed with 2 node(s)
