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
4. [node_root_helper_01] Node started: Perform the following multi-stage verification task to solve the Exciton Rydberg Energy problem:

**Task Overview:**
Calculate the Rydberg energy for the n=3 state of an exciton given a band gap of 3 eV and a 1s exciton peak at 1 eV.

**Stage 1: Formal Sign Convention Establishment**
Define a rigorous sign convention for all energy levels. You must explicitly state whether you are working relative to the vacuum level, the conduction band edge ($E_c$), or the valence band edge ($E_v$). Clearly define the sign of the exciton binding energy ($E_b$) relative to the band gap ($E_g$).

**Stage 2: Symbolic Derivation & Sign-Consistency Check**
Derive the symbolic expression for the Rydberg energy ($R_y$) and the energy of the $n=3$ state. During this derivation, you must perform an explicit 'sign-consistency check': verify that the binding energy correctly reduces the total energy required for excitation (i.e., ensure the exciton peak energy $E_{exc} = E_g - E_b$ is consistent with your chosen convention). Confirm that the Rydberg formula $E_n = -R_y/n^2$ aligns with your established sign convention.

**Stage 3: Numerical Calculation**
Only after the symbolic sign-logic has been validated, substitute the given values (Band gap = 3 eV, 1s peak = 1 eV) into your validated expression to find the Rydberg energy and the specific energy for $n=3$.

**Required Output Format:**
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification including the sign convention used>
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__transmute__mx1_non_holdout_full_agent_v1_2026_04_06__transmute__10__run_2026_04_07_023229
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
