# Organizing All Thoughts on Building Models

To research and build towards more capable systems of AI by exploring novel methods of orchestration, recursive loops, feedback mechanisms etc.

## Avenues We Are Pursuing

1. Atlas (orchestration and exploration)
2. Rhyme Evaluator (feedback looper)
3. BBEH Model (architecture exploring)
4. Best Argument Creator (logic testing)

## Steps to Training a Great Model

1. **Get a source of validation** — ground truth you trust
2. **Set up a run/execute/validate feedback loop** against that validation

## Model Learnings

### Certainty calibration is real and usable
*Source: BBEH Benchmark (03-09)*

When Claude reports its own confidence, it's actually meaningful:
- **52% certainty → 0% accuracy** (causal_understanding, zebra_puzzles — both wrong when uncertain)
- **82-92% certainty → 62.5% accuracy** (decent but not reliable)
- **95-97% certainty → 90.9% accuracy** (trustworthy)

Takeaway: When the model says it's unsure, believe it. Low-confidence answers should be flagged for human review or retry.

### Claude overestimates its rightness on rule-following tasks
*Source: BBEH Benchmark (03-09)*

The most dangerous failures are high-confidence wrong answers. These cluster on specific problem types:

**Consistent failures (wrong both runs, identical wrong answers):**
- **Board game rule chains** (90% certainty, wrong) — multi-step rule application where Claude inverts the conclusion
- **Adjective ordering / hyperbaton** (92% certainty, wrong) — asked for 1 answer, gave 5. Systematic format misunderstanding
- **Sarcasm detection** (82% certainty, wrong) — misreads social/pragmatic tone in 1 of 3 examples
- **Multi-select sports knowledge** (72% certainty, wrong) — over-selects answers, adds wrong options
- **Counting/enumeration** (95% certainty, wrong) — word_sorting said 11 instead of 9. Off-by-small-amount in systematic counting

**Variance zone (different results across runs):**
- **250+ digit arithmetic** — Run 1 produced an astronomically wrong number, Run 2 got it right. Path-dependent computation.
- **Object property counting** — off by 1 (33 vs 34). Precision error.
- **Causal understanding** (52% certainty) — genuinely uncertain, got it right once and wrong once
- **Zebra puzzles** (52% certainty) — same, genuinely uncertain

**Pattern:** The model's blind spot isn't missing knowledge — it's rule misapplication. It KNOWS the rules but applies them wrong, especially on multi-step chains and counting. And it's confidently wrong on exactly these tasks, which makes them the most dangerous.

## Ways to Use Validation Source to Improve Models

1. **Evolution (A/B/C mutation):** Breed several alternatives, test them against validation, take winner and breed alternatives.

## Getting Back on the Horse

1. **Review Atlas prez** (can do now)
2. **Review Rhyme Looper prez** (can do now)
3. **Review YouTube** (can do March 26th or later)

## Review

When reviewing each attempt, update this doc with any new learnings.

1. **Rhyme Looper**
   - Full summary & learnings: `attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/summary_learnings_and_review.md`
   - Live dashboard: run `python3 attempts/SIMPLE-FEEDBACK-LOOPER-rhyme-eval-03-24/dashboard.py` then open http://localhost:8877

2. **Atlas**
   - Review Atlas work. Have a presentation made? Look at the visual page.

## Things to Expand Into

1. **Review Structure (Nightly?)**
2. **Logic loop with adversarial**
