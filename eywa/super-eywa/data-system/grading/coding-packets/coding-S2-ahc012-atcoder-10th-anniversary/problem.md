# AHC012 / AtCoder 10th Anniversary

Write `main.py`.

You are given many strawberry positions inside a circle and a target distribution `a_1..a_10`.
You may cut the cake with at most `K = 100` straight lines.

## Objective

- After all cuts, the cake is split into pieces.
- Let `b_d` be the number of pieces containing exactly `d` strawberries for `d = 1..10`.
- The score is `round(10^6 * sum(min(a_d, b_d)) / sum(a_d))`.
- Higher is better.

## Input

- The instance gives the target counts and the strawberry coordinates.

## Output

- Output one candidate solution.
- First print `k`, the number of cuts, with `0 <= k <= 100`.
- Then print `k` lines of `px py qx qy`.
- Each line describes one straight cut through points `(px, py)` and `(qx, qy)`, which must be different.

## Notes

- The official parser also accepts multiple candidate outputs concatenated together, but the simplest valid submission is one solution.
- This v1 packet uses the official AtCoder visualizer on three bundled public instances.
