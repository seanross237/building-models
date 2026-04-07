# Run Timeline

1. [node_root] Run started for task: Solve this Super-Eywa coding benchmark.
Question ID: coding-S3-ahc024-topological-map
Title: S3. AHC024 / Topological Map

Problem:
# AHC024 / Topological Map

Write `main.py`.

You are given a `50 x 50` colored map.
Colors `1..M` must preserve their connectivity and all color-adjacency relations.
Color `0` represents empty cells.

## Objective

- Output a `50 x 50` grid using colors `0..M`.
- Every nonzero color must remain connected.
- Two colors must be adjacent in the output if and only if they were adjacent in the input.
- The score is `E + 1`, where `E` is the number of `0` cells in the final grid.
- Higher is better.

## Input

- The instance provides `N = 50`, `M`, and the original `50 x 50` color grid.

## Output

- Print `50` lines.
- Each line must contain `50` integers in `0..M`.
- The official tool accepts multiple candidate grids and scores the last one, but the simplest valid submission is one final `50 x 50` grid.

## Notes

- This v1 packet uses the official AtCoder visualizer on three bundled public instances.

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
E + 1, where E is the number of empty cells.
Higher is better.
2. [node_root] Node started: Solve this Super-Eywa coding benchmark.
Question ID: coding-S3-ahc024-topological-map
Title: S3. AHC024 / Topological Map

Problem:
# AHC024 / Topological Map

Write `main.py`.

You are given a `50 x 50` colored map.
Colors `1..M` must preserve their connectivity and all color-adjacency relations.
Color `0` represents empty cells.

## Objective

- Output a `50 x 50` grid using colors `0..M`.
- Every nonzero color must remain connected.
- Two colors must be adjacent in the output if and only if they were adjacent in the input.
- The score is `E + 1`, where `E` is the number of `0` cells in the final grid.
- Higher is better.

## Input

- The instance provides `N = 50`, `M`, and the original `50 x 50` color grid.

## Output

- Print `50` lines.
- Each line must contain `50` integers in `0..M`.
- The official tool accepts multiple candidate grids and scores the last one, but the simplest valid submission is one final `50 x 50` grid.

## Notes

- This v1 packet uses the official AtCoder visualizer on three bundled public instances.

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
E + 1, where E is the number of empty cells.
Higher is better.
3. [node_root] Node recruited 1 helper(s)
4. [node_root_helper_01] Node started: TASK: Topological Map Optimization

INPUT SPECIFICATION:
- Read from stdin.
- N: Integer (Grid dimension, N=50).
- M: Integer (Maximum color index).
- Input Grid: An N x N matrix of integers where each element is in the range [0, M].
- Color 0 represents empty cells.
- Colors 1 to M represent distinct topological entities.

OUTPUT SPECIFICATION:
- Write to stdout.
- Output an N x N matrix of integers where each element is in the range [0, M].
- Format: Exactly N lines, each containing N space-separated integers.
- No additional text, headers, or debug information.

FORMAL CONSTRAINTS AND INVARIANTS:
Let G_in be the input grid and G_out be the output grid.
Let C = {1, 2, ..., M} be the set of non-zero colors.

1. Connectivity Invariant: For every color c in C, the set of cells {(r, c) | G_out[r][c] = c} must form a single connected component under 4-connectivity (up, down, left, right).
2. Adjacency Invariant (Bi-directional): For any two distinct colors c1, c2 in C, c1 and c2 are adjacent in G_out if and only if they are adjacent in G_in. 
   - Adjacency is defined as the existence of at least one pair of cells (r1, c1) and (r2, c2) such that G_out[r1][c1] = color_a, G_out[r2][c2] = color_b, and the cells are 4-neighbors.
   - Note: The adjacency relation must be preserved exactly. If color A and B are adjacent in the input, they must be adjacent in the output. If they are NOT adjacent in the input, they MUST NOT be adjacent in the output.
3. Domain Constraint: All elements in G_out must be in the set {0, 1, ..., M}.

OPTIMIZATION OBJECTIVE:
- Maximize Score = E + 1, where E is the count of cells in G_out such that G_out[r][c] = 0.
- This is equivalent to minimizing the total number of non-zero color cells used to satisfy the connectivity and adjacency invariants.

IMPLEMENTATION REQUIREMENTS:
- Language: Python (main.py).
- Complexity: Must execute within standard competitive programming time limits (typically 2.0s).
- Robustness: Ensure the adjacency relation is strictly maintained; accidental adjacency of non-adjacent colors in the input is a violation.
5. [node_root_helper_01] Node completed with action report_success
6. [node_root_helper_01] Node wrote final output for run coding-S3-ahc024-topological-map__transmute__mx1_coding_non_holdout_v2_2026_04_07__transmute__15__run_2026_04_07_081453
7. [node_root] Node completed with action recruit_help
8. [node_root] Run completed with 2 node(s)
