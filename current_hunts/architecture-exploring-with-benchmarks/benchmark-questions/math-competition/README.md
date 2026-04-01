# Math Competition Benchmark

14 hard math competition problems with verified exact answers.

## Sources
- **AIME 2023-2025** (problems #11-15 — the hardest tier)
- **Putnam 2023** (Session B)
- **IMO 2022** (Problem 5)

## Category Distribution
| Category | Count | Problem IDs |
|----------|-------|-------------|
| Number Theory | 4 | MATH-03, MATH-06, MATH-10, MATH-13 |
| Combinatorics / Probability | 4 | MATH-04, MATH-07, MATH-08, MATH-11 |
| Geometry | 3 | MATH-01, MATH-05, MATH-09 |
| Algebra / Optimization | 1 | MATH-02 |
| Multi-domain (algebra + number theory + geometry) | 1 | MATH-12 |
| Diophantine (proof-style) | 1 | MATH-14 |

## Difficulty Distribution
- AIME #11-12 range: 2 problems (MATH-04, MATH-05)
- AIME #13-14 range: 6 problems (MATH-01, MATH-03, MATH-06, MATH-08, MATH-09, MATH-11)
- AIME #15 range: 4 problems (MATH-02, MATH-07, MATH-10, MATH-12)
- Putnam B: 1 problem (MATH-13)
- IMO: 1 problem (MATH-14 — hardest, requires proof)

## Validation
All AIME answers are integers 000-999, verifiable by exact match.
Putnam B2 answer is a single integer (3).
IMO Problem 5 answer is two specific triples — requires enumeration check.

## Why These Problems
These problems were selected because:
1. They come from the hardest tiers of major competitions (AIME #11-15, Putnam B, IMO)
2. Frontier models (GPT-4o, Claude Opus, Gemini) do NOT reliably solve AIME #13+ problems
3. Each requires multi-step reasoning — naive approaches fail
4. Structured architecture (planning, decomposition, critic, multi-agent) should outperform single-shot
5. All have publicly available answers for automated validation
