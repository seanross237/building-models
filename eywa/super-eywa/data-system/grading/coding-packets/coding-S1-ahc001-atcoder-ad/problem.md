# AHC001 / AtCoder Ad

Write `main.py`.

You are given `N` advertisers.
Advertiser `i` requests a point `(x_i, y_i)` and a target area `r_i` inside a `10000 x 10000` square.
Output one axis-aligned rectangle for each advertiser.

## Objective

- Every rectangle must stay inside the board.
- Rectangle `i` must contain its requested point `(x_i, y_i)`.
- Rectangles must not overlap.
- The score rewards making each rectangle area close to `r_i`.

## Input

- Line 1: `N`
- Next `N` lines: `x_i y_i r_i`

## Output

- Print exactly `N` lines.
- Line `i` must be `x1 y1 x2 y2` for advertiser `i`.
- The rectangle is `[x1, x2) x [y1, y2)`.

## Notes

- A rectangle with invalid bounds or one that misses its required point receives no benefit.
- Overlapping rectangles make the score collapse to zero.
- This v1 packet uses the official AtCoder visualizer on three bundled public instances.
