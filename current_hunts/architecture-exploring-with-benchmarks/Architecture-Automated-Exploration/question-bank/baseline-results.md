# Baseline Results — Round 1

**Status:** Complete
**Date:** 2026-03-29
**Protocol:** Sonnet single-shot (no planning) on all 60 questions. Opus single-shot on Sonnet failures.

## Token Costs

| Agent | Tokens | Duration | Questions |
|-------|--------|----------|-----------|
| Sonnet Science | 19,988 | 184s | 14 |
| Sonnet Logic | 131,116 | 1,333s | 22 |
| Sonnet Math B1 | 18,409 | 81s | 7 |
| Sonnet Math B2 | 89,699 | 998s | 7 |
| Sonnet Coding | 18,885 | 48s | 10 |
| Opus Science | 20,113 | 243s | 12 |
| Opus Logic | 44,492 | 484s | 5 |
| Opus Math | 40,744 | 475s | 5 |
| **Total** | **~383K** | **~65 min** | |

## Science — HLE (14 questions)

| ID | Sonnet | Opus | Correct | Difficulty |
|----|--------|------|---------|------------|
| SCI-01 | I ❌ | I ❌ | C | Hard |
| SCI-02 | 50 ❌ | 20 ❌ | 10 | Hard |
| SCI-03 | 0.04 ❌ | 0.08 ❌ | -0.08 | Hard |
| SCI-04 | 2E(0)x/(3nl²) ❌ | 2E(0)x/(n²l²) ❌ | 3E(0)x/(nl)² | Hard |
| SCI-05 | 7 ❌ | 1,2,2 ✅ | 1, 2, 2 | Medium |
| SCI-06 | B ❌ | C ✅ | C | Medium |
| SCI-07 | 0.56 ❌ | ~1 ❌ | Z=4.61, k=1.66 | Hard |
| SCI-08 | 0.358 ❌ | 0.847 ❌ | 0.424 | Hard |
| SCI-09 | B ✅ | — | B | Easy |
| SCI-10 | F ❌ | A ❌ | C | Hard |
| SCI-11 | D ❌ | B ✅ | B | Medium |
| SCI-12 | K ❌ | G ✅ | G | Medium |
| SCI-13 | ~correct ✅ | — | symbolic match | Easy |
| SCI-14 | Re-centered ❌ | Re-centered ❌ | Al-centered | Hard |

**Science: Sonnet 2/14, Opus adds 4 → Combined 6/14. Hard set: 8 questions.**

## Logic — BBEH (22 questions)

| ID | Sonnet | Opus | Correct | Difficulty |
|----|--------|------|---------|------------|
| LOGIC-01 | 10828 ✅ | — | 10828 | Easy |
| LOGIC-02 | proved | — | unknown | Unverified |
| LOGIC-03 | No ✅ | — | No | Easy |
| LOGIC-04 | 9.9 ✅ | — | 9.9 | Easy |
| LOGIC-05 | B ❌ | B ❌ | (E) | Hard |
| LOGIC-06 | 17 ❌ | 19 ✅ | 19 | Medium |
| LOGIC-07 | 14 ✅ | — | 14 | Easy |
| LOGIC-08 | H ✅ | — | (H) | Easy |
| LOGIC-09 | CDH ❌ | CDH ❌ | H | Hard |
| LOGIC-10 | 181 ✅ | — | 181 | Easy |
| LOGIC-11 | 22 ✅ | — | 22 | Easy |
| LOGIC-12 | correct ✅ | — | correct | Easy |
| LOGIC-13 | 3 ✅ | — | 3 | Easy |
| LOGIC-14 | 1,0,1 ❌ | 1,0,1 ❌ | 0,0,1 | Hard |
| LOGIC-15 | E ✅ | — | (E) | Easy |
| LOGIC-16 | yellow ✅ | — | yellow | Easy |
| LOGIC-17 | 65,1 ✅ | — | 65,1 | Easy |
| LOGIC-18 | [] ✅ | — | [] | Easy |
| LOGIC-19 | B ✅ | — | B | Easy |
| LOGIC-20 | yes,unk,no ✅ | — | yes,unk,no | Easy |
| LOGIC-21 | 9 ❌ | 5 ✅ | 5 | Medium |
| LOGIC-22 | 6 ✅ | — | 6 | Easy |

**Logic: Sonnet 16/21, Opus adds 2 → Combined 18/21. Hard set: 3 questions.**

## Math — Competition (14 questions)

| ID | Sonnet | Opus | Correct | Difficulty | Notes |
|----|--------|------|---------|------------|-------|
| MATH-01 | 104 ✅ | — | 104 | Easy | Derived |
| MATH-02 | 721 ✅ | — | 721 | Easy | Derived |
| MATH-03 | 155 ❌ | 110 ✅ | 110 | Medium | |
| MATH-04 | 371 ✅ | — | 371 | Easy⚠️ | Recalled from training |
| MATH-05 | 385 ✅ | — | 385 | Easy⚠️ | Recalled from training |
| MATH-06 | 211 ❌ | 211 ❌ | 150 | Hard? | **DISPUTED** — both models get 211 |
| MATH-07 | 315 ✅ | — | 315 | Easy⚠️ | Recalled from training |
| MATH-08 | 104 ❌ | 204 ✅ | 204 | Medium | |
| MATH-09 | 60 ✅ | — | 060 | Easy | |
| MATH-10 | 889 ❌ | 889 ❌ | 735 | Hard? | **DISPUTED** — both models get 889 |
| MATH-11 | 608 ✅ | — | 608 | Easy⚠️ | Possibly recalled |
| MATH-12 | 349 ✅ | — | 349 | Easy⚠️ | Possibly recalled |
| MATH-13 | 4 ❌ | 3 ✅ | 3 | Medium | |
| MATH-14 | correct ✅ | — | correct | Easy | |

**Math: Sonnet 9/14, Opus adds 3 → Combined 12/14. Hard set: 2 (both disputed). Contamination: 5 questions likely recalled from training data.**

## Coding — Code Reasoning (10 questions)

| ID | Sonnet | Correct | Difficulty |
|----|--------|---------|------------|
| CODE-01 | ✅ | [1,0,1,3,3,0] | Easy |
| CODE-02 | ✅ | [14,24,14,10] | Easy |
| CODE-03 | ✅ | [3,1,2,0,4] | Easy |
| CODE-04 | ✅ | O(n), 97 | Easy |
| CODE-05 | ✅ | [4,5,0,2,3,1] | Easy |
| CODE-06 | ✅ | 0,10,30,35,StopIteration | Easy |
| CODE-07 | ✅ | 4 | Easy |
| CODE-08 | ✅ | 265 | Easy |
| CODE-09 | ✅ | 13 | Easy |
| CODE-10 | ✅ | (4,5,False,5) | Easy |

**Coding: Sonnet 10/10. All easy — need harder problems.**

## Summary

| Domain | Total | Sonnet | +Opus | Combined | Easy | Medium | Hard |
|--------|-------|--------|-------|----------|------|--------|------|
| Science | 14 | 2 (14%) | +4 | 6 (43%) | 2 | 4 | 8 |
| Logic | 21* | 16 (76%) | +2 | 18 (86%) | 16 | 2 | 3 |
| Math | 14 | 9 (64%) | +3 | 12 (86%) | 9⚠️ | 3 | 2? |
| Coding | 10 | 10 (100%)| — | 10 (100%)| 10 | 0 | 0 |
| **Total** | **59*** | **37 (63%)** | **+9** | **46 (78%)** | **37** | **9** | **13** |

*Excluding LOGIC-02 (unverified answer)

## Exploration Set (22 questions that resist baseline)

**Hard (both models fail) — 13 questions:**
- SCI-01, 02, 03, 04, 07, 08, 10, 14 (science domain knowledge gaps)
- LOGIC-05, 09, 14 (subtle discrimination/reasoning)
- MATH-06, 10 (disputed answers — may actually be correct)

**Medium (Opus fixes what Sonnet misses) — 9 questions:**
- SCI-05, 06, 11, 12 (Opus has better domain knowledge)
- LOGIC-06, 21 (Opus better at careful trace/verification)
- MATH-03, 08, 13 (Opus better at multi-step math reasoning)

## Key Findings

**F16: Coding problems with known traps are too easy.** Sonnet 10/10 on Python gotcha and algorithm trace problems. These don't differentiate architectures. Need genuinely hard algorithmic reasoning problems.

**F17: Published competition math is contaminated.** Sonnet explicitly said "the answer to this AIME problem is known" for at least 3 problems (MATH-04, 05, 07), recalling answers from training data rather than solving them. This makes published competition problems unreliable for measuring reasoning ability.

**F18: Answer key reliability.** Two math problems (MATH-06, MATH-10) have both models agreeing on an answer that disagrees with our key. The models' math checks out (clean derivations). Answer keys sourced from web searches may have errors.

**F19: Science is the hardest domain.** Only 14% baseline accuracy (Sonnet), 43% with Opus. Most failures are genuine domain knowledge gaps (not solvable by better reasoning architecture alone). These need retrieval augmentation.

**F20: Opus primarily helps with domain knowledge, not reasoning.** Of the 9 questions Opus fixes, 4 are science domain knowledge and 3 are multi-step computation. Only 2 (LOGIC-06, LOGIC-21) are reasoning improvements. This suggests model capability > architecture for most of our question set.
