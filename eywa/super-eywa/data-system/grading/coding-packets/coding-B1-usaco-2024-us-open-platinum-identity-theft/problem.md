# Identity Theft

Write `main.py`.

Farmer John has `N` cows, each with a bitstring ID.
Each cow may report any prefix of its final ID, including the full string.
If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened.

You may append bits to the end of each original ID.
Appending one bit costs one second.
Find the minimum total number of appended bits needed so that no cow can ever be mistaken for another.

## Input

- Line 1: `N`
- Next `N` lines: the original bitstring IDs

## Output

- One integer: the minimum total appended-bit cost

## Constraints

- `1 <= N <= 10^5`
- Every ID is non-empty
- The total length of all IDs is at most `10^6`

## Notes

- This v1 packet grades only on bundled public samples.
- Source problem: USACO 2024 US Open Platinum, Problem 1.
