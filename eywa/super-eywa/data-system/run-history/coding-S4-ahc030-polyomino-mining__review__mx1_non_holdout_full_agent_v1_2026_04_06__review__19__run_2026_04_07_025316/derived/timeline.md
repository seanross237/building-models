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
Act as an Implementation Specialist. Your task is to transform the high-level Bayesian Active Learning strategy provided in the draft into a rigorous, step-by-step technical specification. For every conceptual component mentioned (e.g., 'Prior Modeling', 'Observation Model', 'Expected Information Gain', 'Posterior Update'), you must provide: 1. The exact mathematical formula (e.g., the specific Bayesian update equation and the Mutual Information formula). 2. The specific data structures to be used (e.g., how to represent the state space, the probability distributions, and the grid). 3. The precise algorithmic logic in pseudocode (e.g., the loop for query selection, the update step, and the final MAP estimation). The goal is to produce a document so detailed that a programmer could implement the solution without further clarification.

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
To minimize probing cost, we will employ an Active Learning framework based on Bayesian Inference. 1. Prior Modeling: We represent the grid as a set of possible configurations. Since we know the polyomino shapes but not their locations, our prior P(S) is a uniform distribution over all valid placements of the known polyominoes that do not overlap and fit within the grid boundaries. 2. Observation Model: We use 'noisy aggregate queries'. Let Q be a query on a subset of cells C. The result Y is a noisy signal representing the number of oil cells in C. We model this using a Gaussian or Poisson noise model: Y = (sum of x_i for i in C) + epsilon, where x_i is in {0, 1} is the state of cell i. 3. Iterative Probing (Acquisition Function): In each step, we select a query region C that maximizes the Expected Information Gain (EIG). We calculate the Mutual Information between the query result Y and the true state X, selecting C* = argmax_C I(X; Y | C). This prioritizes queries that most significantly reduce the entropy of our posterior distribution. 4. Posterior Update: After each query, we update our belief using Bayes' Rule: P(S | Y) proportional to P(Y | S) P(S). 5. Final Guess: Once the marginal entropy of the cells falls below a threshold, we select the configuration S that maximizes the posterior probability P(S | all observations) and output the coordinates of the oil cells. FINAL_ANSWER: [The set of coordinates identified by the MAP estimate] JUSTIFICATION: The Bayesian approach minimizes cost by selecting queries that maximize information gain, reducing the total number of probes needed to reach a high-confidence state estimate.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root] Node completed with action report_success
7. [node_root] Node wrote final output for run coding-S4-ahc030-polyomino-mining__review__mx1_non_holdout_full_agent_v1_2026_04_06__review__19__run_2026_04_07_025316
8. [node_root] Run completed with 2 node(s)
