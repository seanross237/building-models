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
4. [node_root_helper_01] Node started: Perform a rigorous physical parameter mapping and derivation for the following problem:

**Problem Statement:**
A semiconductor system has a band gap ($E_g$) of 3 eV. Under a screened Coulomb potential, the observed 1s exciton peak ($E_{exc, 1s}$) is located at 1 eV. Calculate the Rydberg energy ($E_{R, n}$) for the $n = 3$ state.

**Instructions for Execution:**

1. **Formal Parameter Mapping:** Begin by mapping all provided numerical values to their specific physical definitions. You must explicitly distinguish between:
    - The electronic band gap ($E_g$).
    - The observed optical transition energy of the 1s exciton ($E_{exc, 1s}$).
    - The 1s exciton binding energy ($E_b$).
    - The effective Rydberg constant of the exciton system ($R_{ex}$).

2. **Symbolic Derivation:** Construct a step-by-step symbolic chain to connect the input parameters to the target. 
    - First, define the relationship between $E_g$, $E_{exc, 1s}$, and $E_b$.
    - Second, relate $E_b$ to the effective Rydberg constant $R_{ex}$ using the hydrogenic model for the $n=1$ state.
    - Third, derive the expression for the energy level of the $n=3$ state ($E_{R, n}$) based on the system's Rydberg constant.

3. **Target Definition:** Before performing any numerical substitution, explicitly state the physical meaning and the mathematical formula of the final target variable ($E_{R, n=3}$).

4. **Numerical Calculation:** Perform the final substitution to find the exact numerical value. Ensure the sign convention is consistent with the physical definition of the energy level relative to the band edge or the vacuum level as implied by the context of 'Rydberg energy'.

**Required Output Format:**
FINAL_ANSWER: <numerical value>
JUSTIFICATION: <brief symbolic derivation summary>
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__transmute__mx1_non_holdout_full_agent_v1_2026_04_06__transmute__12__run_2026_04_07_023412
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
