# AHC032 Sample Standalone Run

Solve one concrete coding benchmark task in this directory only.

Task: AtCoder Heuristic Contest 032, `Mod Stamp`.

Available files:

- `sample_input.txt`
- `score_sample.py`

Required work:

1. Write a Python 3 solver at `solver.py`.
2. The solver must read the task input from stdin and print a valid sequence of stamp operations.
3. Run `score_sample.py` on your solver.
4. If possible, iterate to improve the score.
5. Write `final-output.md` containing:
   - final sample score
   - whether the output was valid
   - the exact scoring command
   - the solver path
   - a short note about the approach

Task summary:

- There is a `9 x 9` board with initial integers.
- There are `20` different `3 x 3` stamps.
- You may apply at most `81` operations.
- Each operation chooses a stamp `m` and a top-left position `(p, q)` with `0 <= p, q <= 6`.
- Applying a stamp adds its `3 x 3` values to the board cells it covers.
- The score is the sum of all final board cell values modulo `998244353`.
- Higher is better.

Constraints for this run:

- Work only in this directory.
- Produce a working solver and an actual measured score.
