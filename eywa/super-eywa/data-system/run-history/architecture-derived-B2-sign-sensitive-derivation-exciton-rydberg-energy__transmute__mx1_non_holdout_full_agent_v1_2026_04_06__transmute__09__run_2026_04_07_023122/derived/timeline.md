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
4. [node_root_helper_01] Node started: Task: Perform a precise derivation of the Rydberg energy for the n=3 state of an exciton. 

Step 1: Glossary Creation. Define all physical terms mentioned in the problem with their exact mathematical meaning. You must explicitly distinguish between:
- $E_g$: The band gap energy.
- $E_{peak}$: The observed energy of the 1s exciton peak.
- $E_{b,1s}$: The binding energy of the 1s exciton state (the difference between $E_g$ and $E_{peak}$).
- $R_y$: The fundamental Rydberg energy constant for this specific screened Coulomb system (the energy scale such that $E_{b,n} = R_y / n^2$).
- $E_{n=3}$: The energy level/binding energy specifically requested for the n=3 state.

Step 2: Symbolic Mapping. Before any numerical substitution, state the exact symbolic formula for the target variable (the Rydberg energy for n=3) in terms of the glossary terms. Note: The question asks for 'the Rydberg energy for n=3'. Clarify if this refers to the binding energy of the n=3 state ($E_{b,3}$) or the fundamental system constant ($R_y$) applied to that state. Given the context of 'Sign-Sensitive Derivation', ensure the sign convention (binding energy vs. total energy relative to the band edge) is mathematically rigorous.

Step 3: Numerical Calculation. Substitute the values (Band gap = 3 eV, 1s peak = 1 eV) into your derived formula to find the final value.

Target Variable: The binding energy of the n=3 exciton state.
Required Format:
FINAL_ANSWER: <value>
JUSTIFICATION: <brief derivation steps>
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__transmute__mx1_non_holdout_full_agent_v1_2026_04_06__transmute__09__run_2026_04_07_023122
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
