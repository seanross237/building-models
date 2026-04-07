# AHC032 / Mod Stamp

Write `main.py`.

You are given a `9 x 9` board of integers and `M = 20` different `3 x 3` stamps.
You may place at most `K = 81` stamps.

## Objective

- Each placement chooses a stamp index `m` and a top-left board position `(i, j)`.
- The chosen `3 x 3` stamp is added to the board modulo `998244353`.
- The score is the sum of all final board entries.
- Higher is better.

## Input

- Line 1: `N M K`
- Next `N` lines: the initial board
- Then for each stamp: `3` lines describing the stamp entries

## Output

- First line: `L`, the number of placements, with `0 <= L <= K`
- Then `L` lines of `m i j`
- `m` is the stamp index
- `(i, j)` is the top-left placement position, with the full `3 x 3` stamp inside the board

## Notes

- This v1 packet uses the official AtCoder visualizer on three bundled public instances.
