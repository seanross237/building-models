# BBEH Benchmark Analysis

**Models tested:** Claude Opus 4.6, Claude Sonnet 4.6
**Dates:** 2026-03-08 (Opus runs 1-2), 2026-03-26 (Sonnet run 3)

## Run Comparison

| | Opus Run 1 | Opus Run 2 | Sonnet Run 3 |
|---|---|---|---|
| **Accuracy** | 16/23 (69.57%) | 16/23 (69.57%) | 15/23 (65.22%) |
| **Unique misses** | multistep_arithmetic, object_properties | causal_understanding, zebra_puzzles | disambiguation_qa, dyck_languages, geometric_shapes |
| **Shared misses (all 3)** | hyperbaton, sarc_triples, sportqa, word_sorting | *(same 4)* | *(same 4)* |

## Sonnet vs Opus — Cross-Model Comparison (Run 3 vs Runs 1-2)

| Task | Opus R1 | Opus R2 | Sonnet | Correct | Time |
|------|---------|---------|--------|---------|------|
| boardgame_qa | WRONG | WRONG | **RIGHT** | proved | 17s |
| boolean_expressions | RIGHT | RIGHT | RIGHT | (A) | 36s |
| buggy_tables | RIGHT | RIGHT | RIGHT | 23.5 | 56s |
| causal_understanding | RIGHT | WRONG | RIGHT | Yes | 2s |
| disambiguation_qa | RIGHT | RIGHT | **WRONG** | (A) | 12s |
| dyck_languages | RIGHT | RIGHT | **WRONG** | 18 | 18s |
| geometric_shapes | RIGHT | RIGHT | **WRONG** | (C) | 37s |
| hyperbaton | WRONG | WRONG | WRONG | B | 2m41s |
| linguini | RIGHT | RIGHT | RIGHT | les pelvis | 14s |
| movie_recommendation | RIGHT | RIGHT | RIGHT | (J) | 17s |
| multistep_arithmetic | WRONG | RIGHT | **WRONG** | -45678 | 10m+ |
| nycc | RIGHT | RIGHT | RIGHT | (C) | 13s |
| object_counting | RIGHT | RIGHT | RIGHT | 293 | 13s |
| object_properties | WRONG | RIGHT | **RIGHT** | 34 | 2m16s |
| sarc_triples | WRONG | WRONG | WRONG | 1,1,1 | 10s |
| shuffled_objects | RIGHT | RIGHT | RIGHT | (F) | 2m10s |
| spatial_reasoning | RIGHT | RIGHT | RIGHT | correct | 8s |
| sportqa | WRONG | WRONG | WRONG | ABD,ABD,B | 9s |
| temporal_sequence | RIGHT | RIGHT | RIGHT | 120,1 | 3m2s |
| time_arithmetic | RIGHT | RIGHT | RIGHT | [] | 10s |
| web_of_lies | RIGHT | RIGHT | RIGHT | correct | 59s |
| word_sorting | WRONG | WRONG | WRONG | 9 | 10s |
| zebra_puzzles | RIGHT | WRONG | **RIGHT** | 6 | 7m34s |

### Key Sonnet vs Opus differences

**Sonnet wins (solved what Opus couldn't):**
- **boardgame_qa** — Opus's persistent failure. Sonnet correctly traced the preference chain where Rule2 overrides Rule8, then Rule5 fires because no animal refuses to help the goat. This was Opus's #1 "unknown unknown."
- **zebra_puzzles** — Opus got this wrong on run 2 (52% certainty). Sonnet solved 137 clues in 7m34s and got it right.
- **object_properties** — Opus missed on run 1 (off-by-one). Sonnet got 34 correctly.
- **causal_understanding** — Opus run 2 miss (52% certainty). Sonnet answered correctly.

**Opus wins (Sonnet regressed):**
- **disambiguation_qa** — Sonnet answered (E) Ambiguous, but the correct answer is (A). Opus got this right both times. Sonnet overthought the pronoun ambiguity when the sentence structure makes it clear.
- **dyck_languages** — Sonnet answered 19, correct is 18. Off-by-one error in stack tracking. Opus consistent.
- **geometric_shapes** — Sonnet couldn't identify the parallelogram, answered (B) "none of the above" instead of (C) "only 5". Opus consistent.
- **multistep_arithmetic** — Numbers exploded to millions of digits. Sonnet used Python but still couldn't converge. Same failure mode as Opus run 1.

**Both models consistently fail (4 tasks):**
- **hyperbaton** — Both over-select adjective orderings (Opus: ABDEF, Sonnet: BDE). Neither can learn the full custom ordering from examples alone.
- **sarc_triples** — Both miss sarcasm on at least one reply. Different error patterns (Opus: 1,0,1; Sonnet: 0,1,0).
- **sportqa** — Both over-select answers on sub-question 2. Neither gets the restrictive "B only" answer.
- **word_sorting** — Both find *a* mistake but not the *first* mistake (Opus: Thought 11, Sonnet: Thought 15, correct: Thought 9).

### Sonnet timing profile

| Duration | Tasks |
|----------|-------|
| < 15s | causal_understanding, spatial_reasoning, sportqa, sarc_triples, time_arithmetic, word_sorting, nycc, object_counting, linguini, disambiguation_qa |
| 15-60s | boardgame_qa, movie_recommendation, dyck_languages, boolean_expressions, geometric_shapes, buggy_tables, web_of_lies |
| 1-3m | shuffled_objects, object_properties, hyperbaton, temporal_sequence |
| 3-10m | zebra_puzzles (7m34s) |
| 10m+ | multistep_arithmetic (still running, using Python) |

Total wall-clock time for all 23 tasks run in parallel: ~10 minutes (dominated by multistep_arithmetic and zebra_puzzles).

## Run 2 Results (with Certainty)

| Task | Result | Certainty | Run 1 |
|------|--------|-----------|-------|
| bbeh_boardgame_qa | WRONG | 90% | WRONG |
| bbeh_boolean_expressions | RIGHT | 90% | RIGHT |
| bbeh_buggy_tables | RIGHT | 90% | RIGHT |
| bbeh_causal_understanding | **WRONG** | **52%** | RIGHT |
| bbeh_disambiguation_qa | RIGHT | 95% | RIGHT |
| bbeh_dyck_languages | RIGHT | 97% | RIGHT |
| bbeh_geometric_shapes | RIGHT | 95% | RIGHT |
| bbeh_hyperbaton | WRONG | 92% | WRONG |
| bbeh_linguini | RIGHT | 97% | RIGHT |
| bbeh_movie_recommendation | RIGHT | 72% | RIGHT |
| bbeh_multistep_arithmetic | **RIGHT** | 95% | WRONG |
| bbeh_nycc | RIGHT | 92% | RIGHT |
| bbeh_object_counting | RIGHT | 95% | RIGHT |
| bbeh_object_properties | **RIGHT** | 90% | WRONG |
| bbeh_sarc_triples | WRONG | 82% | WRONG |
| bbeh_shuffled_objects | RIGHT | 95% | RIGHT |
| bbeh_spatial_reasoning | RIGHT | 97% | RIGHT |
| bbeh_sportqa | WRONG | 72% | WRONG |
| bbeh_temporal_sequence | RIGHT | 95% | RIGHT |
| bbeh_time_arithmetic | RIGHT | 97% | RIGHT |
| bbeh_web_of_lies | RIGHT | 92% | RIGHT |
| bbeh_word_sorting | WRONG | 95% | WRONG |
| bbeh_zebra_puzzles | **WRONG** | **52%** | RIGHT |

## Certainty Calibration Analysis

### The model's certainty is meaningfully calibrated:

| Certainty Tier | Count | Accuracy | Assessment |
|----------------|-------|----------|------------|
| 52% (low) | 2 | 0/2 (0%) | **Perfectly calibrated** — genuinely uncertain, genuinely wrong |
| 72% (medium) | 2 | 1/2 (50%) | Reasonable — coin-flip territory |
| 82-92% (high) | 8 | 5/8 (62.5%) | Overconfident — should be ~85% |
| 95-97% (very high) | 11 | 10/11 (90.9%) | Well calibrated |

**Average certainty on correct answers: 91.9%**
**Average certainty on incorrect answers: 77.9%**
**Gap: 14 percentage points** — meaningful but not large enough to be a reliable filter.

### Key finding: Low certainty is a strong negative signal
Both 52% answers were wrong. If you filtered out answers below 70%, you'd remove 2 wrong answers and 0 right ones — a free accuracy boost.

### Key finding: High certainty doesn't prevent errors
boardgame_qa (90%), hyperbaton (92%), and word_sorting (95%) were all confidently wrong. These represent "unknown unknowns" — the model doesn't know what it doesn't know in these domains.

## Variance Between Runs

Two tasks flipped from wrong→right (multistep_arithmetic, object_properties) and two flipped from right→wrong (causal_understanding, zebra_puzzles). This suggests:

1. **~5 tasks are rock-solid wrong** (boardgame_qa, hyperbaton, sarc_triples, sportqa, word_sorting) — failed both times
2. **~14 tasks are rock-solid right** — passed both times
3. **~4 tasks are in the "variance zone"** — outcome depends on the specific reasoning path taken

The "true" accuracy is likely around **14-18/23 (61-78%)** depending on luck with the variance-zone tasks.

## Failure Analysis

### Persistently Wrong (5 tasks — failed both runs)

**1. bbeh_boardgame_qa** (90% certainty — overconfident)
Complex rule-based reasoning with preference chains. Incorrectly applied Rule 6 preemptively. The preference system only applies when both rules fire with contradictory conclusions.

**2. bbeh_hyperbaton** (92% certainty — overconfident)
Custom adjective ordering from examples. Accepted 5 options as correct when only 1 was. Difficulty with inductive rule learning when rules are non-standard.

**3. bbeh_sarc_triples** (82% certainty — appropriately less confident)
Sarcasm detection. Missed sarcasm in Reply 2 — a politically-charged ironic agreement. Lower certainty here suggests some awareness of ambiguity.

**4. bbeh_sportqa** (72% certainty — good self-awareness)
Sports knowledge multiple-select. Over-selected answers. The model's lower confidence correctly reflects its uncertainty in sports domain knowledge.

**5. bbeh_word_sorting** (95% certainty — overconfident)
Error localization. Found *an* error but not the *first* error. Flagged Thought 11 instead of Thought 9 both times.

### Variance Zone (4 tasks — different results across runs)

**6. bbeh_multistep_arithmetic** — WRONG in run 1 (250+ digit blowup), RIGHT in run 2 (95% certainty). Non-deterministic computation path; sometimes the chain of 60+ custom operators works, sometimes it compounds errors catastrophically.

**7. bbeh_object_properties** — WRONG in run 1 (off by one: 33→34), RIGHT in run 2 (90% certainty). State tracking with 46+ items through transformations. The off-by-one nature suggests this is right at the edge of capability.

**8. bbeh_causal_understanding** — RIGHT in run 1, WRONG in run 2 (52% certainty). Flipped from "Yes" to "No". The very low certainty shows the model genuinely doesn't know — it's essentially guessing.

**9. bbeh_zebra_puzzles** — RIGHT in run 1, WRONG in run 2 (52% certainty). Answered 2 instead of 6. Again, lowest possible certainty, correctly reflecting genuine uncertainty when the constraint propagation didn't converge.

## Patterns

1. **Overconfidence on rule-based reasoning** (boardgame_qa 90%, hyperbaton 92%, word_sorting 95%): The model confidently applies incorrect rules without knowing it's wrong.
2. **Good calibration on uncertain tasks** (causal_understanding 52%, zebra_puzzles 52%): When the model is genuinely unsure, it knows it.
3. **Domain knowledge gaps correlate with lower certainty** (sportqa 72%, movie_recommendation 72%): Knowledge-dependent tasks get appropriate hedging.
4. **Computation variance** (multistep_arithmetic, object_properties): Same question can get different answers across runs — the reasoning path is non-deterministic.

## Strengths (consistent across both runs)

- **Formal logic** (web_of_lies 92%, disambiguation_qa 95%)
- **Pattern matching** (dyck_languages 97%, geometric_shapes 95%, linguini 97%)
- **State tracking** (shuffled_objects 95% — 100+ ball swaps tracked correctly)
- **Data parsing** (buggy_tables 90%, object_counting 95%)
- **Constraint satisfaction** (temporal_sequence 95%)
- **Creative judgment** (nycc 92%, movie_recommendation 72%)
- **Graph/spatial reasoning** (spatial_reasoning 97%)
- **Date arithmetic** (time_arithmetic 97%)
