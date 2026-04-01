---
topic: 4-point tree-level MHV amplitude — three-method numerical comparison and timing
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-001
---

## Finding

All three methods for computing the 4-point tree-level MHV amplitude in N=4 SYM (Parke-Taylor, BCFW recursion, Grassmannian/positive geometry) agree to machine precision across 10 kinematic configurations. Timing benchmarks show Parke-Taylor is fastest (5.6 μs), Grassmannian is intermediate (11× slower), and BCFW is slowest (41× slower).

## Numerical Agreement [COMPUTED]

All results compared to Parke-Taylor as baseline. Maximum relative error across all methods and kinematics: **< 10⁻¹⁵** (machine epsilon for float64).

| Kinematics | A_PT | |BCFW/PT − 1| | |Grass/PT − 1| | Pass? |
|---|---|---|---|---|
| COM E=1 θ=π/3 | 2.37037037 | 4.4×10⁻¹⁶ | 0 | ✓ |
| COM E=1 θ=π/4 | 1.60808101 | 1.1×10⁻¹⁶ | 1.1×10⁻¹⁶ | ✓ |
| COM E=1 θ=π/6 | 1.23122473 | 4.4×10⁻¹⁶ | 0 | ✓ |
| COM E=1 θ=1.0 | 2.18913271 | 0 | 0 | ✓ |
| COM E=2 θ=2.1 | 7.13453397 | 1.1×10⁻¹⁶ | 7.8×10⁻¹⁶ | ✓ |
| COM E=5 θ=0.5 | 1.20862857 | 1.1×10⁻¹⁶ | 2.2×10⁻¹⁶ | ✓ |
| Random seed=42 | 7.71498985 | 4.4×10⁻¹⁶ | 0 | ✓ |
| Random seed=137 | 1.18809805 | 2.2×10⁻¹⁶ | 4.4×10⁻¹⁶ | ✓ |
| Random seed=999 | 4.47039754 | 3.3×10⁻¹⁶ | 3.3×10⁻¹⁶ | ✓ |
| Random seed=7 | 6.77603128 | 0 | 2.2×10⁻¹⁶ | ✓ |

## Timing Benchmarks [COMPUTED]

5000 evaluations each at COM E=1, θ=π/3:

| Method | Time per eval | Ratio to PT |
|---|---|---|
| Parke-Taylor | 5.6 μs | 1.0× |
| Grassmannian | 62 μs | 11× |
| BCFW | 231 μs | 41× |

BCFW is slowest because it requires spinor extraction for the internal on-shell momentum (building a 4-vector sum and factoring a 2×2 matrix). Grassmannian requires a 2×2 linear solve. Parke-Taylor only evaluates angle brackets.

## Operation Counts (n=4)

| Method | Operations | Terms | Conceptual level |
|---|---|---|---|
| Parke-Taylor | ~20 | 1 | Lowest — closed-form formula |
| Grassmannian | ~30 | 1 | Highest — linear algebra + geometry |
| BCFW | ~40 | 1 | Medium — recursive factorization |

## General Scaling

| Method | n-point scaling |
|---|---|
| Parke-Taylor | O(n) — but only for MHV; doesn't generalize beyond MHV without extra structure |
| BCFW | O(n²) terms — grows quadratically; works for all tree amplitudes |
| Grassmannian (MHV) | O(n) — single residue for all MHV; most general via Eulerian number for NMHV+ |

## Conceptual Comparison

**Parke-Taylor**: Simplest computation. A RESULT (conjectured from patterns, proven by BCFW), not a method. O(n) but restricted to MHV.

**BCFW**: A genuine recursive METHOD for any tree amplitude. Never introduces off-shell or gauge-dependent quantities. The "killer app" that launched the modern amplitudes program.

**Grassmannian**: Deepest geometrically. Encodes the amplitude as a canonical form on the positive Grassmannian. For n=4, k=2, the amplitude is the "volume" of a quadrilateral in 2D. Locality and unitarity are emergent, not manifest.

At 4-point the Grassmannian reveals structure invisible in the other representations: the amplitude lives naturally in momentum-twistor space (CP³), and the square-bracket vs. angle-bracket representations are dual coordinate descriptions of the same geometric invariant. See `grassmannian-g24-square-bracket-identity.md` for the explicit algebraic identity.
