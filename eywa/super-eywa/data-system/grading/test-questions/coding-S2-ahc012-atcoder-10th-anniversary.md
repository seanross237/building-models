# S2. AHC012 / AtCoder 10th Anniversary

- Type: Coding
- Subtype: Score-gradient task
- Source: https://atcoder.jp/contests/ahc012/tasks/ahc012_a

## Task

Cut a circular cake with at most K = 100 straight lines so the strawberry-count distribution of pieces matches the attendee-demand distribution as well as possible.

## Grading

round(10^6 * matched_pieces / total_requested_pieces) on each case.
Higher is better.

## Why It Discriminates

Hard constrained optimization with global interactions between cuts.
Good for planning, search, and refinement loops.

## Notes

- 
