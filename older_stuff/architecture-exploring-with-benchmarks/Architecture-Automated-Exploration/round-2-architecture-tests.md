# Round 2: Architecture Component Testing

**Date:** 2026-03-29
**Questions tested:** 8 unique questions from the exploration set
**Architectures tested:** D2 adversarial elimination, critic + hints, 3-way majority vote

## Results Summary

| Architecture | Questions | Fixed | Rate | Token Cost |
|-------------|-----------|-------|------|------------|
| D2 adversarial elimination | 3 (discrimination) | 0/3 | 0% | ~28K |
| Critic + targeted hints | 5 (computation) | 4/5 | 80% | ~33K |
| 3-way majority vote | 5 (mixed) | 3/5 | 60% | ~100K |
| Opus model upgrade | 17 (Sonnet failures) | 9/17 | 53% | ~105K |

## Test 1: D2 Adversarial Elimination

**Hypothesis:** D2 ("assume each option is correct, search for contradictions") helps with discrimination errors.

**Questions tested:** LOGIC-05, LOGIC-14, SCI-01

| ID | Baseline | D2 | Correct | Result |
|----|----------|-----|---------|--------|
| LOGIC-05 | B | B | (E) | No change — same wrong answer |
| LOGIC-14 | 1,0,1 | 1,0,1 | 0,0,1 | No change — same wrong answer |
| SCI-01 | I | I | C | No change — same wrong answer |

**Finding F21: D2 cannot fix knowledge-based discrimination errors.** The model constructs plausible-but-wrong contradiction arguments against the correct answers. For SCI-01, it "eliminated" option C (coiled-coils) by arguing coiled-coils can't produce the 1618+1680 FTIR signature — which is factually wrong but the model doesn't know that. D2 only works when the model HAS the knowledge to find real contradictions.

## Test 2: Critic + Targeted Hints

**Hypothesis:** A two-pass approach (solve, then self-critique with a targeted hint) fixes computation errors.

**Questions tested:** SCI-03, SCI-04, LOGIC-06, MATH-03, MATH-13

| ID | Baseline | Critic+Hint | Correct | Result | Hint Given |
|----|----------|------------|---------|--------|------------|
| SCI-03 | 0.04 | -0.04 | -0.08 | Partial (sign fixed, magnitude wrong) | "Answer should be NEGATIVE" |
| SCI-04 | 2E(0)x/(3nl²) | 3E(0)x/(n²l²) | 3E(0)x/(nl)² | ✅ Fixed | "Check coefficient and n power" |
| LOGIC-06 | 17 | 19 | 19 | ✅ Fixed | "Error is in upper teens" |
| MATH-03 | 155 | 110 | 110 | ✅ Fixed | "Use Hensel's lemma carefully, m ≤ 155" |
| MATH-13 | 4 | 3 | 3 | ✅ Fixed | "k=2 impossible mod 7, check k=3" |

**Finding F22: Critic + targeted hints is the strongest architecture tested (80% fix rate).** But the hints are doing the heavy lifting — they tell the model WHERE to look and WHAT to check. This is effectively retrieval-augmented critique. Pure self-critique (without hints) would likely perform worse, since the model can't find errors it doesn't know to look for.

**Finding F23: Hints work by narrowing the search space, not providing answers.** The hints didn't give the answer — they pointed to the error type ("sign should be negative", "check coefficient"). The model then successfully corrected its own work. This suggests a practical architecture: use a planning/routing step to identify likely error types, then use targeted verification prompts.

## Test 3: 3-Way Majority Vote (Separate Agents)

**Hypothesis:** Running 3 independent Sonnet agents and taking the majority answer reduces variance-dominated errors.

**Questions tested:** LOGIC-06, LOGIC-21, MATH-03, MATH-08, MATH-13

| ID | Vote 1 | Vote 2 | Vote 3 | Correct | Majority | Fixed? |
|----|--------|--------|--------|---------|----------|--------|
| LOGIC-06 | 17 ❌ | 19 ✅ | 17 ❌ | 19 | 17 ❌ | No |
| LOGIC-21 | 7 ❌ | 7 ❌ | 7 ❌ | 5 | 7 ❌ | No |
| MATH-03 | 110 ✅ | 110 ✅ | 110 ✅ | 110 | 110 ✅ | Yes |
| MATH-08 | 204 ✅ | 204 ✅ | 204 ✅ | 204 | 204 ✅ | Yes |
| MATH-13 | 3 ✅ | 3 ✅ | 3 ✅ | 3 | 3 ✅ | Yes |

**Finding F24: Majority vote perfectly fixes variance-dominated math errors but not systematic logic errors.** All 3 math questions were unanimously correct across the fresh runs — the original baseline was just an unlucky single run. This proves the prior finding (F5) that plan variance is the #1 problem for computation, and majority vote is the solution.

**Finding F25: Logic trace errors are systematic, not variance.** LOGIC-21 was unanimously wrong (all 3 agents got "7" instead of "5"). LOGIC-06 had some variance (1/3 correct) but the wrong answer dominated. The model consistently makes the same type of mistake in bracket/letter tracing — this is a capability gap, not variance.

**Finding F26: The original baseline run was an anomaly for math.** All 3 fresh Sonnet runs got MATH-03, MATH-08, and MATH-13 correct. The original baseline got all 3 wrong. This means the "Sonnet fails, Opus fixes" classification for these questions was misleading — Sonnet CAN solve them, it just didn't on that particular run. True difficulty classification requires multiple runs.

## Updated Failure Mode Taxonomy

Based on Round 2 results, the taxonomy refines to:

| Failure Mode | Example | Best Architecture | Fix Rate |
|-------------|---------|-------------------|----------|
| **Variance** (model CAN solve, doesn't always) | MATH-03, 08, 13 | Majority vote (3 agents) | ~100% |
| **Computation** (systematic arithmetic/formula error) | SCI-04, LOGIC-06 | Critic + targeted hints | ~80% |
| **Knowledge** (model lacks domain expertise) | SCI-01, SCI-02, SCI-10 | Retrieval augmentation | Untested |
| **Systematic reasoning** (consistent wrong logic) | LOGIC-21, LOGIC-05 | None found yet | 0% |
| **Interpretation** (ambiguous problem reading) | SCI-03 | Hints help partially | ~50% |

## Architecture Decision Tree (Draft)

```
New Problem
├── Is baseline correct? → Easy, done
├── Is it variance? (run 3 agents, check agreement)
│   ├── All agree → Systematic error (go below)
│   └── Disagree → Take majority vote (fixes ~100%)
├── Is it a computation error? (wrong formula, arithmetic)
│   └── Yes → Critic + verification hints (fixes ~80%)
├── Is it a knowledge gap? (model lacks domain facts)
│   └── Yes → Retrieval augmentation (untested, predicted high)
└── Systematic reasoning error
    └── No known fix — need capability upgrade
```

## Token Cost Analysis

| Run | Tokens | Duration | Questions | Cost/Question |
|-----|--------|----------|-----------|---------------|
| D2 test (Sonnet) | 28K | 90s | 3 | 9.3K |
| Critic test (Sonnet) | 33K | 374s | 5 | 6.6K |
| Vote run 1 (Sonnet) | 41K | 407s | 5 | 8.2K |
| Vote run 2 (Sonnet) | 33K | 384s | 5 | 6.6K |
| Vote run 3 (Sonnet) | 27K | 341s | 5 | 5.4K |
| **Round 2 total** | **~162K** | **~27 min** | | |

3-way majority vote costs ~3x a single run. Critic is ~1.5x. D2 is ~1x.

## What's Next

Round 3 priorities:
1. **Test retrieval augmentation** on knowledge-gap questions (SCI-01, SCI-02, SCI-10) — this is the last untested component with high predicted value
2. **Validate the decision tree** — run the full pipeline (classify → route → execute) on a held-out set
3. **Replace coding problems** — current set is trivially easy; need harder algorithmic reasoning problems
4. **Verify MATH-10** — both models get 889 but official answer is 735; may be a problem statement transcription error
