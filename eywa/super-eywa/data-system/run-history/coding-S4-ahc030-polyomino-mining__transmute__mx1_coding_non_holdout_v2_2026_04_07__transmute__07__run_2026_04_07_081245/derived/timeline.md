# Run Timeline

1. [node_root] Run started for task: Solve this Super-Eywa coding benchmark.
Question ID: coding-S4-ahc030-polyomino-mining
Title: S4. AHC030 / Polyomino Mining

Problem:
# AHC030 / Polyomino Mining

Write `main.py`.

This is an interactive-style optimization task.
You know the oil-field polyomino shapes but not their placements on the grid.
Your program must gather information and then report the oil cells.

## Objective

- Minimize probing cost while recovering the true oil configuration.
- Lower cost is better, and the official local tester converts that cost into the contest score.

## Input

- The initial input describes the grid size, the number of hidden oil fields, the noise parameter, and the set of polyomino shapes.

## Interaction Protocol

- Your program reads the initial problem instance from stdin.
- Then it writes commands to stdout and reads tester responses from stdin.
- Supported commands are:
  - `q 1 x y` for a single-cell drill query
  - `q k x1 y1 ... xk yk` for a multi-cell noisy aggregate query
  - `a k x1 y1 ... xk yk` to submit the final set of oil cells
- Flush after every command.

## Output Contract

- Because this packet uses the official local tester, your program should behave like a normal interactive solution.
- The tester captures the full command transcript and scores it.

## Notes

- This v1 packet uses the official AtCoder tester and visualizer on three bundled public instances.

Submission contract:
- Return a single Python submission file named main.py.
- Read from stdin and write to stdout.
- Put the full file content in the artifacts list of your execute_locally JSON response.
- Use the response field only for a brief submission summary.
- Do not wrap the code in markdown fences inside artifacts.

Critical validity rules:
- Your program is judged by the stdout it prints when run, not by the summary in your JSON response.
- Print exactly the contestant output described in the Output section, and nothing else.
- Do not print the objective score, estimated score, labels, explanations, or debug text unless the Output section explicitly requires them.
- If the Output section requires a count/header on the first line, print that first line exactly.
- Every printed index, count, and coordinate must stay within the allowed ranges.
- Prefer a simple valid baseline solution over an ambitious but invalid one.
- If the problem permits an empty or minimal valid plan, that is better than malformed output.

Grading target:
Lower probing cost is better.
Contest score is derived from absolute and relative cost.
2. [node_root] Node started: Solve this Super-Eywa coding benchmark.
Question ID: coding-S4-ahc030-polyomino-mining
Title: S4. AHC030 / Polyomino Mining

Problem:
# AHC030 / Polyomino Mining

Write `main.py`.

This is an interactive-style optimization task.
You know the oil-field polyomino shapes but not their placements on the grid.
Your program must gather information and then report the oil cells.

## Objective

- Minimize probing cost while recovering the true oil configuration.
- Lower cost is better, and the official local tester converts that cost into the contest score.

## Input

- The initial input describes the grid size, the number of hidden oil fields, the noise parameter, and the set of polyomino shapes.

## Interaction Protocol

- Your program reads the initial problem instance from stdin.
- Then it writes commands to stdout and reads tester responses from stdin.
- Supported commands are:
  - `q 1 x y` for a single-cell drill query
  - `q k x1 y1 ... xk yk` for a multi-cell noisy aggregate query
  - `a k x1 y1 ... xk yk` to submit the final set of oil cells
- Flush after every command.

## Output Contract

- Because this packet uses the official local tester, your program should behave like a normal interactive solution.
- The tester captures the full command transcript and scores it.

## Notes

- This v1 packet uses the official AtCoder tester and visualizer on three bundled public instances.

Submission contract:
- Return a single Python submission file named main.py.
- Read from stdin and write to stdout.
- Put the full file content in the artifacts list of your execute_locally JSON response.
- Use the response field only for a brief submission summary.
- Do not wrap the code in markdown fences inside artifacts.

Critical validity rules:
- Your program is judged by the stdout it prints when run, not by the summary in your JSON response.
- Print exactly the contestant output described in the Output section, and nothing else.
- Do not print the objective score, estimated score, labels, explanations, or debug text unless the Output section explicitly requires them.
- If the Output section requires a count/header on the first line, print that first line exactly.
- Every printed index, count, and coordinate must stay within the allowed ranges.
- Prefer a simple valid baseline solution over an ambitious but invalid one.
- If the problem permits an empty or minimal valid plan, that is better than malformed output.

Grading target:
Lower probing cost is better.
Contest score is derived from absolute and relative cost.
3. [node_root] Node recruited 1 helper(s)
4. [node_root_helper_01] Node started: TECHNICAL REQUIREMENTS DOCUMENT: POLYOMINO MINING

1. INTERACTION PROTOCOL

Input Parsing:
- Read initial configuration from stdin: Grid dimensions (W, H), number of hidden oil fields (N), noise parameter (P), and a list of polyomino shapes (sets of relative coordinates).

Command Syntax (stdout):
- Single-cell drill: q 1 x y
- Multi-cell aggregate query: q k x1 y1 x2 y2 ... xk yk
- Final submission: a k x1 y1 x2 y2 ... xk yk

Response Format (stdin):
- For 'q' commands: Read a response indicating the presence or absence of oil (subject to noise parameter P).
- For 'a' command: The interaction terminates.

Note: Flush stdout after every command.

2. OPTIMIZATION LOGIC

Objective Function:
- Minimize Total Probing Cost.
- Cost is the sum of costs associated with each 'q' command. Single-cell queries and multi-cell aggregate queries have different cost weights (implied by the problem structure).

Goal:
- Identify the exact set of coordinates belonging to the N hidden polyominoes while minimizing the cumulative cost of queries used to resolve uncertainty.

3. ALGORITHMIC CORE

Search Space and Constraints:
- The search space consists of all possible valid placements of the provided polyomino shapes on the W x H grid.
- The presence of noise (P) means query results are probabilistic rather than deterministic.

Logic Requirements:
- Implement a probabilistic model (e.g., Bayesian update) to maintain a belief map of oil cell probabilities across the grid.
- Develop a query selection strategy: Choose query coordinates (single or aggregate) that maximize Information Gain regarding the placement of the N polyominoes relative to the cost of the query.
- Handle shape recognition: Use the known polyomino templates to constrain the possible configurations of oil cells.
- Termination: Once the confidence in the identified oil configuration meets a threshold or the cost-benefit of further querying becomes negative, execute the 'a' command.

4. STRICT EXECUTION RULES

- File Naming: The solution must be contained in a file named main.py.
- I/O: Use only stdin for input and stdout for output. Do not use file I/O.
- Output Purity: Do not print debug information, scores, labels, or explanations. The only output allowed is the command syntax defined in the Interaction Protocol.
- Error Handling: Ensure all coordinates are within [0, W-1] and [0, H-1]. Ensure the final submission 'a' contains the correct number of cells 'k'.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run coding-S4-ahc030-polyomino-mining__transmute__mx1_coding_non_holdout_v2_2026_04_07__transmute__07__run_2026_04_07_081245
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
