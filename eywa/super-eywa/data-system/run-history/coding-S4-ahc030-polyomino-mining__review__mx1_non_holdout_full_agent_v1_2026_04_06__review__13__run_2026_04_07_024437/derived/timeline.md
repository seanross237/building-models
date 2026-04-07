# Run Timeline

1. [node_root] Run started for task: Solve this Super-Eywa grading-bank question.
Question ID: coding-S4-ahc030-polyomino-mining
Title: S4. AHC030 / Polyomino Mining

Problem:
Given known polyomino oil-field shapes but unknown placements, recover all oil-containing cells with as little probing cost as possible using drilling, noisy aggregate queries, and final guesses.

Grading target:
Lower probing cost is better.
Contest score is derived from absolute and relative cost.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>
2. [node_root] Node started: Solve this Super-Eywa grading-bank question.
Question ID: coding-S4-ahc030-polyomino-mining
Title: S4. AHC030 / Polyomino Mining

Problem:
Given known polyomino oil-field shapes but unknown placements, recover all oil-containing cells with as little probing cost as possible using drilling, noisy aggregate queries, and final guesses.

Grading target:
Lower probing cost is better.
Contest score is derived from absolute and relative cost.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>
3. [node_root] Node recruited 1 helper(s)
4. [node_root_helper_01] Node started: Review this draft answer carefully.
Find flaws, missing reasoning, or corrections, then produce the strongest corrected answer you can.

Review focus:
I am appointing you as the technical co-author for this specification. The current draft is purely conceptual and insufficient for implementation. To transform this into a concrete technical blueprint, you must provide: 1. The explicit Bayesian update formula $P(S|Q)$ where $S$ is the set of polyomino placements and $Q$ is the noisy aggregate query result. 2. A formal definition of the data structures required to represent the grid, the polyomino templates, and the probability density map. 3. A detailed step-by-step algorithmic pseudocode for the 'Adaptive Sampling' loop, specifically detailing how the next probe location is selected based on the expected information gain (entropy reduction). Do not merely critique; provide the missing mathematical and algorithmic components.

Original question:
Solve this Super-Eywa grading-bank question.
Question ID: coding-S4-ahc030-polyomino-mining
Title: S4. AHC030 / Polyomino Mining

Problem:
Given known polyomino oil-field shapes but unknown placements, recover all oil-containing cells with as little probing cost as possible using drilling, noisy aggregate queries, and final guesses.

Grading target:
Lower probing cost is better.
Contest score is derived from absolute and relative cost.

Return format:
FINAL_ANSWER: <your answer>
JUSTIFICATION: <brief justification>

Draft answer:
FINAL_ANSWER: Implement a Bayesian-driven adaptive sampling strategy combined with a template-matching algorithm. 

JUSTIFICATION: To minimize probing cost, we must maximize the information gain per drill. The strategy involves: 1. Initial sparse sampling using a Sobol sequence to identify high-probability regions. 2. Using noisy aggregate queries to estimate the local density of polyominoes. 3. Applying a Bayesian update to the probability map of each cell based on the observed aggregate values and the known shapes of the polyominoes. 4. Once a threshold probability is met, use local drilling to confirm the exact orientation and placement of the polyominoes. This minimizes redundant drilling by leveraging the geometric constraints of the known shapes.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run coding-S4-ahc030-polyomino-mining__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__13__run_2026_04_07_024437
8. [node_root] Run completed with 2 node(s)
