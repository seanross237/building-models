# BBEH Questions

Source: Big-Bench Extra Hard (BBEH) benchmark — last example from each `task.json`.
Full question text lives in `../experiment-questions/` (the original working directory).

## All Questions

| # | File | Answer | Answer type | Opus T5 | Sonnet T5 | Notes |
|---|------|--------|-------------|---------|-----------|-------|
| 1 | [word_sorting.txt](../../experiment-questions/word_sorting.txt) | `5` | exactMatch | ✓ | ✓ | First error in sorting chain |
| 2 | [dyck.txt](../../experiment-questions/dyck.txt) | `19` | exactMatch | ✓ | ✓ | Bracket matching depth |
| 3 | [arithmetic.txt](../../experiment-questions/arithmetic.txt) | `10828` | exactMatch | ✓ | ✓ | 250+ digit chain; slow (~2min) |
| 4 | [boardgame.txt](../../experiment-questions/boardgame.txt) | `unknown` | exactMatch | ✓ (R1) / ✗ (R2) | ✓ (R1) / ✗ (R2) | High variance; closed-world trap |
| 5 | [object_properties.txt](../../experiment-questions/object_properties.txt) | `22` | exactMatch | ✓ | ✓ | 45-item inventory tracking |
| 6 | [zebra.txt](../../experiment-questions/zebra.txt) | `6` | exactMatch | ✓ | ✓ | Constraint satisfaction |
| 7 | [sarcasm.txt](../../experiment-questions/sarcasm.txt) | `0,0,1` | exactMatch | ✓ | ✓ | Pragmatic tone detection |
| 8 | [hyperbaton.txt](../../experiment-questions/hyperbaton.txt) | `H` | exactMatch | ✓ (R1) / ✗ (R2) | varies | High variance; adjective ordering |
| 9 | [sportqa.txt](../../experiment-questions/sportqa.txt) | `AB, ABC, ABC` | exactMatch | ✗ | ✗ | Benchmark question likely bad; reclassified |
| 10 | [web_of_lies.txt](../../experiment-questions/web_of_lies.txt) | `yes, unknown, no` | exactMatch | ✓ | ✓ | 50+ person truth/liar chain |
| 11 | [shuffled_objects.txt](../../experiment-questions/shuffled_objects.txt) | `(E)` | multipleChoice | ✓ | ✓ | 200+ book swap operations; slow |
| 12 | [temporal_sequence.txt](../../experiment-questions/temporal_sequence.txt) | `65, 1` | exactMatch | ✓ | ✓ | Timezone-aware meeting scheduling |
| 13 | [causal_understanding.txt](../../experiment-questions/causal_understanding.txt) | `No` | exactMatch | ✓ | ✓ | Counterfactual necessary cause |
| 14 | [geometric_shapes.txt](../../experiment-questions/geometric_shapes.txt) | `(H)` | multipleChoice | ✓ | ✗ | SVG coordinate parsing; Sonnet fails |
| 15 | [disambiguation_qa.txt](../../experiment-questions/disambiguation_qa.txt) | `(E)` | multipleChoice | ✗ | ✗ | Pronoun ambiguity; both models fail |
| 16 | [object_counting.txt](../../experiment-questions/object_counting.txt) | `181` | exactMatch | ✓ | ✓ | Massive noisy inventory |
| 17 | [time_arithmetic.txt](../../experiment-questions/time_arithmetic.txt) | `[]` | exactMatch | ✓ | ✓ | Chained dates; trick empty answer |

## Stumper Questions (Online, from Experiment 8)

| # | File | Answer | Opus T5 | Sonnet T5 | Notes |
|---|------|--------|---------|-----------|-------|
| S1 | [river_crossing.txt](../../experiment-questions/river_crossing.txt) | `3` | ✓ | ✓ | Boat holds farmer + 2 items |
| S2 | [spatial_rotation.txt](../../experiment-questions/spatial_rotation.txt) | `yellow` | ✓ | ✓ | |
| S3 | [truth_teller.txt](../../experiment-questions/truth_teller.txt) | `B` | ✓ | ✓ | |
| S4 | [ordering.txt](../../experiment-questions/ordering.txt) | `Charlie, Diana, Bob, Alice, Eve` | ✓ | ✓ | |
| S5 | [filtered_list.txt](../../experiment-questions/filtered_list.txt) | `14` | ✓ | ✓ | |
| S6 | [decimal_comparison.txt](../../experiment-questions/decimal_comparison.txt) | `9.9` | ✓ | ✓ | |

## Key Findings

- **Consistent failures:** `disambiguation_qa` (both models), `sportqa` (all models — likely bad question)
- **Opus > Sonnet:** `geometric_shapes` is the only question that distinguishes the two models
- **High-variance questions:** `boardgame`, `hyperbaton` — correct sometimes, wrong others
- **Effective ceiling:** 16/17 well-formed questions (excluding sportqa)
