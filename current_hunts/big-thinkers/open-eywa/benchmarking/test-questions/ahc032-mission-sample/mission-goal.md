# Validation Mission: AHC032 Sample

Use the archived Open-Eywa worker to attempt one hard coding task from `validation-suite/notes/coding-test-candidates.md`.

Task: AtCoder Heuristic Contest 032, `Mod Stamp`.

You have:

- a sample input at `system/artifacts/sample_input.txt`
- a local scorer at `system/artifacts/score_sample.py`

Your job:

1. Write a Python 3 solver at `system/artifacts/solver.py`.
2. The solver must read the task input from stdin and print a valid sequence of stamp operations.
3. Run the scorer on the sample input.
4. If you have time, iterate to improve the sample score.
5. Write `output/final-output.md` with:
   - the final sample score
   - whether the output was valid
   - the exact scoring command
   - the solver path
   - a short note about the approach

Task summary:

- There is a `9 x 9` board with initial integers.
- There are `20` different `3 x 3` stamps.
- You may apply at most `81` stamp operations.
- Each operation chooses a stamp `m` and a top-left board position `(p, q)` with `0 <= p, q <= 6`.
- Applying the stamp adds its `3 x 3` values to the board cells it covers.
- The score is the sum of all final board cell values modulo `998244353`.
- Higher is better.

Use only files inside this node.
