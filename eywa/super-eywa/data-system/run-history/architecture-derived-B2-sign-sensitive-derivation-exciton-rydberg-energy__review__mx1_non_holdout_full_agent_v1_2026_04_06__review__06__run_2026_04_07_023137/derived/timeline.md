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
Please perform a step-by-step verification of this derivation. 

1. Independently re-derive the solution starting from the problem statement: Band gap = 3 eV, 1s peak = 1 eV, find Rydberg energy for n=3.
2. Verify the calculation of the 1s binding energy.
3. Verify the application of the $1/n^2$ scaling law.
4. Compare your intermediate steps and final result with the draft provided above.
5. Check if the 'sign-sensitive' requirement implies the answer should be expressed as a negative energy level (e.g., -2/9 eV) or if the magnitude is expected. If you believe the sign should be negative, please flag this clearly.

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
To find the Rydberg energy for the n = 3 state, we first determine the binding energy of the 1s exciton state.

1. **Identify the 1s binding energy ($E_{b,1s}$):**
   The band gap ($E_g$) is 3 eV. The 1s exciton peak is observed at 1 eV. 
   The binding energy is the difference between the band gap and the exciton peak energy:
   $E_{b,1s} = E_g - E_{peak,1s} = 3\text{ eV} - 1\text{ eV} = 2\text{ eV}$.

2. **Apply the Rydberg scaling law:**
   In a hydrogenic model (screened Coulomb potential), the binding energy of an exciton state with principal quantum number $n$ scales as:
   $E_{b,n} = \frac{E_{b,1s}}{n^2}$

3. **Calculate for n = 3:**
   $E_{b,3} = \frac{2\text{ eV}}{3^2} = \frac{2\text{ eV}}{9}$
   $E_{b,3} \approx 0.2222...\text{ eV}$

Note: In physics, the Rydberg energy (binding energy) is typically expressed as a positive value representing the energy required to ionize the exciton, though the energy level itself is negative relative to the conduction band edge. Given the prompt's emphasis on sign-sensitivity, we provide the magnitude of the binding energy.

FINAL_ANSWER: 2/9 eV
JUSTIFICATION: The 1s binding energy is 2 eV (3 eV gap - 1 eV peak). Using the hydrogenic scaling $E_n = E_1/n^2$, for $n=3$, $E_3 = 2/9$ eV.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__06__run_2026_04_07_023137
8. [node_root] Run completed with 2 node(s)
