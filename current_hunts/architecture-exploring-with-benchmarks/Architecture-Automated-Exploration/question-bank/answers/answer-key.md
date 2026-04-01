# Answer Key

**WARNING: This file contains answers. Do NOT include this file in any agent context.**

---

## Science — HLE

| ID | Answer | Type |
|----|--------|------|
| SCI-01 | C | multipleChoice |
| SCI-02 | 10 | exactMatch |
| SCI-03 | -0.08 | exactMatch |
| SCI-04 | F(x) = 3E(0) x / (nl)^2 | exactMatch (symbolic) |
| SCI-05 | 1, 2, 2 | exactMatch |
| SCI-06 | C | multipleChoice |
| SCI-07 | Z = 4.61, <k> = 1.66 | exactMatch |
| SCI-08 | 0.424 | exactMatch |
| SCI-09 | B | multipleChoice |
| SCI-10 | C | multipleChoice |
| SCI-11 | B | multipleChoice |
| SCI-12 | G | multipleChoice |
| SCI-13 | C = (Vm*Cm + Vf*Cf*A) * (Vm*I + Vf*<A>)^{-1} | exactMatch (symbolic) |
| SCI-14 | Al, Re2Al13; Al, ReAl12; Al, Re2Al9 | exactMatch |

## Logic/Reasoning — BBEH

| ID | Source File | Answer | Type | Notes |
|----|------------|--------|------|-------|
| LOGIC-01 | arithmetic | 10828 | exactMatch | |
| LOGIC-02 | boardgame | unknown | exactMatch | Answer not verified — may need manual check |
| LOGIC-03 | causal_understanding | No | exactMatch | |
| LOGIC-04 | decimal_comparison | 9.9 | exactMatch | |
| LOGIC-05 | disambiguation_qa | (E) | multipleChoice | |
| LOGIC-06 | dyck | 19 | exactMatch | |
| LOGIC-07 | filtered_list | 14 | exactMatch | |
| LOGIC-08 | geometric_shapes | (H) | multipleChoice | |
| LOGIC-09 | hyperbaton | H | multipleChoice | |
| LOGIC-10 | object_counting | 181 | exactMatch | |
| LOGIC-11 | object_properties | 22 | exactMatch | |
| LOGIC-12 | ordering | Charlie, Diana, Bob, Alice, Eve | exactMatch | |
| LOGIC-13 | river_crossing | 3 | exactMatch | |
| LOGIC-14 | sarcasm | 0,0,1 | exactMatch | Multi-part answer |
| LOGIC-15 | shuffled_objects | (E) | multipleChoice | |
| LOGIC-16 | spatial_rotation | yellow | exactMatch | |
| LOGIC-17 | temporal_sequence | 65, 1 | exactMatch | Multi-part answer |
| LOGIC-18 | time_arithmetic | [] | exactMatch | Empty list — verify this is correct |
| LOGIC-19 | truth_teller | B | multipleChoice | |
| LOGIC-20 | web_of_lies | yes, unknown, no | exactMatch | Multi-part answer |
| LOGIC-21 | word_sorting | 5 | exactMatch | |
| LOGIC-22 | zebra | 6 | exactMatch | |

## Math — Competition Problems

| ID | Source | Answer | Type |
|----|--------|--------|------|
| MATH-01 | 2024 AIME I #14 | 104 | exactMatch (integer) |
| MATH-02 | 2024 AIME I #15 | 721 | exactMatch (integer) |
| MATH-03 | 2024 AIME I #13 | 110 | exactMatch (integer) |
| MATH-04 | 2024 AIME I #11 | 371 | exactMatch (integer) |
| MATH-05 | 2024 AIME I #12 | 385 | exactMatch (integer) |
| MATH-06 | 2024 AIME II #14 | 211 | exactMatch (integer) |
| MATH-07 | 2024 AIME II #15 | 315 | exactMatch (integer) |
| MATH-08 | 2025 AIME I #13 | 204 | exactMatch (integer) |
| MATH-09 | 2025 AIME I #14 | 060 | exactMatch (integer) |
| MATH-10 | 2025 AIME I #15 | 735 | exactMatch (integer) |
| MATH-11 | 2023 AIME I #14 | 608 | exactMatch (integer) |
| MATH-12 | 2023 AIME I #15 | 349 | exactMatch (integer) |
| MATH-13 | 2023 Putnam B2 | 3 | exactMatch (integer) |
| MATH-14 | IMO 2022 #5 | (2,2,2) and (3,4,3) | exactMatch (pairs) |

## Coding — Code Reasoning

| ID | Answer | Type | Common Wrong Answer |
|----|--------|------|---------------------|
| CODE-01 | [1, 0, 1, 3, 3, 0] | exactMatch | [1, 0, 5, 3, 4, 2] (traces on original array) |
| CODE-02 | [14, 24, 14, 10] | exactMatch | [11, 21, 12, 8] (assumes i varies per closure) |
| CODE-03 | [3, 1, 2, 0, 4] | exactMatch | [3, 1, 2, 3, 4] (wrong assignment order) |
| CODE-04 | O(n), exact=97 | exactMatch | O(n log n) (doesn't amortize inner loop) |
| CODE-05 | [4, 5, 0, 2, 3, 1] | exactMatch | [4, 5, 2, 0, 3, 1] (wrong heap ordering) |
| CODE-06 | 0, 10, 30, 35, StopIteration | exactMatch | Thinks send(None) returns 35 |
| CODE-07 | 4 | exactMatch (integer) | 3 (greedy matching error) |
| CODE-08 | 265 | exactMatch (integer) | 264 (off-by-one in inclusion-exclusion) |
| CODE-09 | 13 | exactMatch (integer) | 7 (confuses compositions with partitions) |
| CODE-10 | (4, 5, False, 5) | exactMatch | (4, 5, False, 6) (thinks `in` creates keys) |

## Coding — Hard Algorithmic Reasoning

See `coding-hard-answers.md` for detailed explanations, execution traces, and common wrong answers.

| ID | Answer | Type | Common Wrong Answer |
|----|--------|------|---------------------|
| CODEHARD-01 | 7 | exactMatch | 6 (computes true shortest path, not Dijkstra's output) |
| CODEHARD-02 | evictions: [(1,A),(2,B),(4,D),(3,C)] | exactMatch | Missing (4,D) eviction (thinks key 2 still cached) |
| CODEHARD-03 | 17 | exactMatch | 14 (greedy by value/weight ratio) |
| CODEHARD-04 | meeting=37, mu=2, lambda=6 | exactMatch | Arithmetic errors on modular squaring |
| CODEHARD-05 | find(4)=7 | exactMatch | find(4)=1 (ignores path compression during union) |
| CODEHARD-06 | 27 | exactMatch | 24 (assumes mystery(n)=n) or 26 (mystery(12)=12) |
| CODEHARD-07 | [0,2,5,4,6,1,3] | exactMatch | [0,1,3,4,2,5,6] (recursive DFS order) |
| CODEHARD-08 | [[1,2,3,2,4,5],[1,2,3,2,4,5],[1,3,4,5,6],[1,3,4,5,6],[1,3,5,6]] | exactMatch | [[1,2,3],[1,2,3,2,4,5],...] (no aliasing awareness) |
| CODEHARD-09 | count[5]=4, count[7]=1 | exactMatch | count[7]>1 (thinks 5->7 edge contributes) |
| CODEHARD-10 | 3 | exactMatch | 2 (uses // instead of int(a/b)) |
