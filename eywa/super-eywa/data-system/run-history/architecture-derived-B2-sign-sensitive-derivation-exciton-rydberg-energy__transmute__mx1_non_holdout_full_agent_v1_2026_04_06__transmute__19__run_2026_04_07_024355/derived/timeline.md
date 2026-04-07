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
4. [node_root_helper_01] Node started: Perform a strict algebraic isolation task to determine the Rydberg energy for the n=3 state. 

1. **Identify Parameters**: 
   - $E_g$ (Band gap)
   - $E_{peak}$ (Observed 1s exciton peak energy)
   - $n$ (Principal quantum number)

2. **Symbolic Isolation Task**: 
   First, express the system's fundamental scaling constant, the Rydberg energy ($R_y$), as a single, isolated algebraic expression involving only $E_g$ and $E_{peak}$. Note that the exciton binding energy $E_b$ is the difference between the band gap and the peak energy, and for a hydrogenic model, $E_b = R_y / n^2$ (where $n=1$ for the 1s state). 
   
   **You must explicitly state the symbolic equation for $R_y$ before performing any numerical substitution.**

3. **Numerical Substitution**: 
   Once the symbolic equation for $R_y$ is established, substitute the provided values ($E_g = 3$ eV, $E_{peak} = 1$ eV) to find the value of $R_y$. 

4. **Final Calculation**: 
   Using the isolated $R_y$, calculate the specific energy for the $n=3$ state. Ensure you account for the sign convention requested in the problem (the energy of the state relative to the band edge or the absolute binding energy as implied by the context).

**Constraints**: 
- Do not calculate state-specific energies until $R_y$ is isolated.
- Provide the final answer in the format: 
  FINAL_ANSWER: <value>
  JUSTIFICATION: <brief justification>
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run architecture-derived-B2-sign-sensitive-derivation-exciton-rydberg-energy__transmute__mx1_non_holdout_full_agent_v1_2026_04_06__transmute__19__run_2026_04_07_024355
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
