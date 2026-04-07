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
4. [node_root_helper_01] Node started: TASK: Constant-Isolation (Exciton Rydberg Scaling Parameter)

SYSTEM CONTEXT:
You are analyzing a semiconductor system characterized by a screened Coulomb interaction. The energy levels of the exciton states are governed by a fundamental system constant (the Rydberg energy, $R_y^*$) which acts as the universal scaling parameter for all bound states in this system.

PROVIDED STATE DATA:
- Band gap ($E_g$): 3 eV
- Observed energy of the $n=1$ (1s) exciton peak: 1 eV

OBJECTIVE:
1. Define the mathematical relationship between the observed energy of a specific state ($E_{obs}$) and the fundamental scaling constant ($R_y^*$), accounting for the band gap.
2. Using the provided $n=1$ state data, isolate and solve for the value of the fundamental scaling constant ($R_y^*$).
3. Once the constant is determined, use it to calculate the energy level for the $n=3$ state.

CRITICAL CONSTRAINTS:
- DO NOT provide the energy of the $n=3$ state as your final answer. 
- The final answer MUST be the fundamental scaling constant ($R_y^*$) that governs the entire system.
- Ensure the sign and magnitude are derived strictly from the relationship between the band gap and the observed exciton peak.

FINAL_ANSWER format: <numerical value of the scaling constant>
JUSTIFICATION: <brief derivation showing the isolation of the constant>
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__transmute__mx1_non_holdout_full_agent_v1_2026_04_06__transmute__14__run_2026_04_07_023718
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
