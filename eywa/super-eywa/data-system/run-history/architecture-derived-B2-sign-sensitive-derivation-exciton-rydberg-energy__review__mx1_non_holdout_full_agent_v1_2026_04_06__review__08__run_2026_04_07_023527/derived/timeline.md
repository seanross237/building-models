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
Please perform a semantic and mathematical audit of this response. 1) Identify any ambiguities in terminology: Does 'Rydberg energy for n=3' refer to the binding energy magnitude (Eb/n^2), the energy level relative to the conduction band (En), or the effective Rydberg constant (Ry*)? 2) Verify the mathematical model: Using the hydrogenic approximation En = -Ry*/n^2, check if the mapping from the 1s peak to the Rydberg constant is correct. 3) Verify the sign: Ensure the resulting sign is physically consistent with the definition of an exciton state being a bound state below the band gap.

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
JUSTIFICATION: The exciton binding energy Eb is the difference between the band gap Eg and the 1s exciton peak energy E1s. Given Eg = 3 eV and E1s = 1 eV, Eb = 3 - 1 = 2 eV. In the hydrogenic model, the binding energy for a state n is given by Eb(n) = Eb(1s) / n^2. For n=3, Eb(3) = 2 / 3^2 = 2/9 approx 0.222 eV. However, the Rydberg energy (the energy level relative to the continuum) is typically expressed as a negative value: En = -Eb(n). Thus, E3 = -2/9 approx -0.222 eV. 

Wait, re-evaluating the prompt's specific constraints: If the 'Rydberg energy' refers to the scale Ry*, then Ry* = 2 eV. If it refers to the energy level E3, it is -2/9 eV. Given the 'sign-sensitive' instruction, I will provide the energy level value.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__08__run_2026_04_07_023527
8. [node_root] Run completed with 2 node(s)
