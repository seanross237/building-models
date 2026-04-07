# Bessla Motors

Write `main.py`.

There are `N` points of interest connected by `M` weighted undirected roads.
Nodes `1..C` are charging stations and the rest are destinations.

A destination is well-connected if it can be reached from at least `K` distinct charging stations within distance `R`.
Report all well-connected destinations in ascending order.

## Input

- Line 1: `N M C R K`
- Next `M` lines: `u v l` for each road

## Output

- First line: the number of well-connected destinations
- Then each well-connected destination on its own line in ascending order

## Constraints

- `2 <= N <= 5 * 10^4`
- `1 <= M <= 10^5`
- `1 <= K <= 10`
- `1 <= l <= 10^9`

## Notes

- This v1 packet grades only on bundled public samples.
- Source problem: USACO 2024 February Gold, Problem 1.
