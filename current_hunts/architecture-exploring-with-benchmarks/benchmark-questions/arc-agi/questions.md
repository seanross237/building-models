# ARC-AGI-2 Questions

Source: `arcprize/ARC-AGI-2` on GitHub (public training set).
All tasks represented as plain JSON arrays — no image needed, fully text-parseable.

## How to prompt
```
Here are training examples showing an input→output transformation.
Figure out the rule, then produce the output for the test input.
Reply with ONLY the output grid as a JSON array of arrays.

[paste training examples + test input]
```

---

## Q1: Alternating Tile (task 00576224)
**Source:** arcprize/ARC-AGI-2, data/training/00576224.json
**Rule:** 2×2 input → 6×6 output. Tile 3 times; odd rows use original, even rows use row-reversed copy.
**Answer:** `[[3,2,3,2,3,2],[7,8,7,8,7,8],[2,3,2,3,2,3],[8,7,8,7,8,7],[3,2,3,2,3,2],[7,8,7,8,7,8]]`
**Validation:** auto (exact grid match)
**Model results:** untested

```
Training Example 1:
Input:  [[7,9],[4,3]]
Output: [[7,9,7,9,7,9],[4,3,4,3,4,3],[9,7,9,7,9,7],[3,4,3,4,3,4],[7,9,7,9,7,9],[4,3,4,3,4,3]]

Training Example 2:
Input:  [[8,6],[6,4]]
Output: [[8,6,8,6,8,6],[6,4,6,4,6,4],[6,8,6,8,6,8],[4,6,4,6,4,6],[8,6,8,6,8,6],[6,4,6,4,6,4]]

Test Input: [[3,2],[7,8]]
Output:
```

---

## Q2: Key-Color Mapping (task 009d5c81)
**Source:** arcprize/ARC-AGI-2, data/training/009d5c81.json
**Rule:** Each 14×14 grid has a pattern of 8s (light-blue) and a small shape made of 1s (blue). The 1s shape encodes a replacement color via its form. Output: recolor all 8s to that color; remove the 1s.
**Answer:** (requires determining which key shape → which color from training examples; model must learn the mapping)
**Validation:** auto (exact grid match)
**Model results:** untested

```
Training Example 1:
Input:
Row 0:  [0,0,0,0,0,0,0,8,8,0,0,0,0,0]
Row 1:  [0,0,0,0,0,0,0,0,8,8,8,0,0,0]
Row 2:  [0,0,0,0,0,0,0,0,0,0,8,0,8,0]
Row 3:  [0,0,0,0,0,8,8,8,8,0,8,8,8,0]
Row 4:  [0,0,0,0,8,8,0,0,8,8,8,0,8,8]
Row 5:  [0,0,0,0,0,0,0,8,8,0,0,0,8,0]
Row 6:  [0,0,0,0,0,0,8,8,0,0,0,8,8,0]
Row 7:  [0,0,0,0,0,0,0,0,0,8,8,8,0,0]
Row 8:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 9:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 10: [0,0,0,0,1,1,1,0,0,0,0,0,0,0]
Row 11: [0,0,0,0,1,0,1,0,0,0,0,0,0,0]
Row 12: [0,0,0,0,0,1,0,0,0,0,0,0,0,0]
Row 13: [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: (same grid but all 8s → 7 (orange), all 1s → 0)

[Additional training examples with different key shapes mapping to colors 3 (green), 2 (red)]

Test Input:
Row 0:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 1:  [0,0,0,0,0,8,8,8,8,8,8,8,8,8]
Row 2:  [0,0,0,0,0,8,0,0,0,8,0,8,0,8]
Row 3:  [0,0,0,0,0,8,0,8,0,8,0,0,0,8]
Row 4:  [0,0,0,0,0,8,8,8,8,8,8,8,8,8]
Row 5:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 6:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 7:  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 8:  [0,0,0,0,0,0,1,1,1,0,0,0,0,0]
Row 9:  [0,0,0,0,0,0,1,0,1,0,0,0,0,0]
Row 10: [0,0,0,0,0,0,0,1,0,0,0,0,0,0]
Row 11: [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 12: [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Row 13: [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output:
```

---

## Q3: Flood Fill Enclosed Regions (task 00d62c1b)
**Source:** arcprize/ARC-AGI-2, data/training/00d62c1b.json
**Rule:** Find all closed loops/regions formed by 3s (green) and fill their interior with 4s (yellow). Open shapes and isolated 3s are left unchanged.
**Answer:** (model must identify closed regions and flood-fill correctly)
**Validation:** auto (exact grid match)
**Model results:** untested

```
Training Example 1:
Input (10x10):
Row 0: [0,0,0,0,0,0,0,0,0,0]
Row 1: [0,0,3,3,3,3,0,0,0,0]
Row 2: [0,0,3,0,0,3,0,0,0,0]
Row 3: [0,0,3,0,0,3,0,3,0,0]
Row 4: [0,0,3,3,3,3,3,3,3,0]
Row 5: [0,0,0,3,0,0,0,0,3,0]
Row 6: [0,0,0,3,0,0,0,3,3,0]
Row 7: [0,0,0,3,3,0,0,3,0,3]
Row 8: [0,0,0,3,0,3,0,0,3,0]
Row 9: [0,0,0,0,3,0,0,0,0,0]

Output (10x10):
Row 0: [0,0,0,0,0,0,0,0,0,0]
Row 1: [0,0,3,3,3,3,0,0,0,0]
Row 2: [0,0,3,4,4,3,0,0,0,0]
Row 3: [0,0,3,4,4,3,0,3,0,0]
Row 4: [0,0,3,3,3,3,3,3,3,0]
Row 5: [0,0,0,3,0,0,0,0,3,0]
Row 6: [0,0,0,3,0,0,0,3,3,0]
Row 7: [0,0,0,3,3,0,0,3,4,3]
Row 8: [0,0,0,3,4,3,0,0,3,0]
Row 9: [0,0,0,0,3,0,0,0,0,0]

[Additional training examples with different closed/open region configurations]

Test Input (20x20): [full grid with multiple 3-patterns — fetch from GitHub for exact values]
Output:
```

---

## Q4: Fractal Self-Similar Tiling (task 007bbfb7)
**Source:** arcprize/ARC-AGI-2, data/training/007bbfb7.json
**Rule:** 3×3 input → 9×9 output. Each non-zero cell in the input is replaced by a full copy of the input; each zero cell is replaced by a 3×3 block of zeros.
**Answer:** `[[7,0,7,0,0,0,7,0,7],[7,0,7,0,0,0,7,0,7],[7,7,0,0,0,0,7,7,0],[7,0,7,7,0,7,0,0,0],[7,0,7,7,0,7,0,0,0],[7,7,0,7,7,0,0,0,0],[7,0,7,0,0,0,0,0,0],[7,0,7,0,0,0,0,0,0],[7,7,0,0,0,0,0,0,0]]`
**Validation:** auto (exact grid match)
**Model results:** untested

```
Training Example 1:
Input (3x3):  [[6,6,0],[6,0,0],[0,6,6]]
Output (9x9): [[6,6,0,6,6,0,0,0,0],[6,0,0,6,0,0,0,0,0],[0,6,6,0,6,6,0,0,0],[6,6,0,0,0,0,0,0,0],[6,0,0,0,0,0,0,0,0],[0,6,6,0,0,0,0,0,0],[0,0,0,6,6,0,6,6,0],[0,0,0,6,0,0,6,0,0],[0,0,0,0,6,6,0,6,6]]

Training Example 2:
Input (3x3):  [[4,0,4],[0,0,0],[0,4,0]]
Output (9x9): [[4,0,4,0,0,0,4,0,4],[0,0,0,0,0,0,0,0,0],[0,4,0,0,0,0,0,4,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,4,0,4,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,4,0,0,0,0]]

Training Example 3:
Input (3x3):  [[0,0,7],[7,7,7],[0,7,0]]
Output (9x9): [[0,0,0,0,0,0,0,0,7],[0,0,0,0,0,0,7,7,7],[0,0,0,0,0,0,0,7,0],[0,0,7,0,0,7,0,0,7],[7,7,7,7,7,7,7,7,7],[0,7,0,0,7,0,0,7,0],[0,0,0,0,0,7,0,0,0],[0,0,0,7,7,7,0,0,0],[0,0,0,0,7,0,0,0,0]]

Test Input (3x3): [[7,0,7],[7,0,7],[7,7,0]]
Output:
```
