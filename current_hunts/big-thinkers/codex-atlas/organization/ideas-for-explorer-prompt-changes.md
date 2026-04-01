# Ideas for Explorer Prompt Changes to Try

## Motivation

Atlas explorers have produced both correct and incorrect results. By examining specific cases where we now know the right answer, we can test whether different prompting strategies, architectures, or guidance would have led to better outcomes. The goal is to learn what actually helps — and bake the winners into the system.

## Clean-Room Test Cases

Three cases chosen for different failure patterns:

### Case 1: Yang-Mills H_norm = 1/12 (S2-E007/E008) — "Find the right answer"

- **Task:** Find the tight Hessian bound for SU(2) Yang-Mills at Q=I
- **Ground truth:** H_norm = 1/12, achieved by staggered mode v_{x,μ} = (-1)^{|x|+μ}
- **Verified by:** Full eigenvalue computation (E009), zero residual
- **Original explorer got it:** RIGHT (E007 found it), but only after E006 got it WRONG (claimed 29-138× loose from Gibbs sampling, missed worst-case)
- **Failure pattern:** Sampling bias — tested typical configurations, not adversarial. The staggered mode is a structured analytical construction that gradient ascent / random sampling won't find.
- **GOAL.md location:** `execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-006/GOAL.md` (the one that failed) and `exploration-007/GOAL.md` (the one that caught it)

### Case 2: Riemann Li Coefficient Crossover (S3-E002 → E009) — "Avoid a methodological trap"

- **Task:** Test whether λ_n^zeta / λ_n^GUE < 1 at n=500
- **Initial wrong answer:** Ratio = 0.95, claimed as "super-rigidity"
- **Correct answer:** Ratio = 1.09 at matched K=N=5000. The 0.95 was a density mismatch / truncation artifact.
- **Failure pattern:** Insufficient convergence testing. The result looked real at one scale but reversed at larger scale. Explorer didn't check robustness across scales.
- **GOAL.md location:** `execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/` (E002 original, E009 correction)

### Case 3: Riemann C1 Intermediate Rigidity (S2-E005 → E009) — "Run the right control"

- **Task:** Determine if Von Mangoldt amplitudes create anomalous Δ₃ = 0.285
- **Initial wrong answer:** "Yes, arithmetic structure creates unique intermediate rigidity"
- **Correct answer:** No — flat random amplitudes give the same value. Generic finite-size GUE behavior, not Von Mangoldt-specific.
- **Failure pattern:** False positive. Explorer was excited by a result and didn't run the obvious null experiment (same matrix structure, flat amplitudes instead of Von Mangoldt).
- **GOAL.md location:** `execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/` (E005 original, E009 correction)

## Test Conditions

### A: Bare goal (baseline)
Same goal text as the original exploration, no modifications. Measures what the current system does.

### B: "Plan first"
Prepend "Write a detailed plan before any computation" to the goal. Tests whether generic planning helps on research tasks. (Prior finding F27 from architecture benchmarks: planning is a no-op within single agents on standard benchmarks. Does this hold for research?)

### C1: Task-specific guard-rails
Minimal hints that address the *type* of error, crafted by someone who knows what went wrong:
- **H_norm:** "After finding a candidate maximum, verify it's the global max by also checking non-obvious modes (alternating signs, staggered patterns). Don't stop at the first plausible-looking eigenvector."
- **Li coefficient:** "When comparing two sequences, verify your comparison is apples-to-apples — matching density, matching normalization, matching N. Run the comparison at 2+ different scales to check if the result is robust."
- **C1 rigidity:** "Before claiming any result is caused by a specific structural feature, run a null experiment with that feature removed. If the null gives the same result, your feature isn't the cause."

Note: These are "cheating" slightly — they're written by someone who knows the answer. Useful for measuring the ceiling, not for production deployment.

### C2: Generic methodology guard-rails (from Atlas library)
Give the explorer the actual meta-learnings from the Atlas library that already exist, written from past failures but NOT from knowing these specific tasks. Pull from:
- `include-trivial-control-checks.md`
- `verify-unexpected-findings-immediately.md`
- `adversarial-check-between-phases.md`
- `require-baseline-adjusted-significance.md`
- `verify-counterexample-before-investigating.md`

This is the realistic test — these are the guard-rails we'd actually deploy in production.

### D: Opus plan → Sonnet execution
Opus reads the goal, writes a detailed plan. A fresh Sonnet instance gets the plan + goal and executes. Tests plan transfer across model tiers.

**Caveat:** This tests two things at once (model capability AND plan transfer). To isolate plan transfer, also consider Opus→Opus (same model, fresh instance).

### E: Self-review
Same agent, second pass after completing work: "Now review your work — what could be wrong? What assumptions did you make? What checks did you skip?" Tests whether self-critique catches errors.

### F: Fresh adversarial reviewer
Agent 1 does the work. Fresh Agent 2 gets the report + "Find what's wrong with this analysis. Be adversarial." Tests whether fresh eyes catch what self-review misses.

### G: Stripped/open-ended goal
Remove the step-by-step recipe from the goal. Just give the question:
- **H_norm:** "What is the tightest Hessian bound for SU(2) Yang-Mills? Find it and prove it."
- **Li coefficient:** "Compute λ_n^zeta / λ_n^GUE and determine if the ratio has structural significance."
- **C1 rigidity:** "Is the spectral rigidity of Von Mangoldt matrices anomalous? Determine the cause."

Tests whether current goals are *too prescriptive* — does the explorer discover better approaches when not constrained to a recipe?

## Predictions

| Task | Expected pattern |
|------|-----------------|
| H_norm (find answer) | G (open-ended) and C2 (library guard-rails) most likely to help. B (generic plan) probably a no-op. Self-review (E) won't help — can't find what you didn't look for. |
| Li coefficient (methodology trap) | C1/C2 guard-rails should prevent it. F (fresh reviewer) might catch it. B (generic plan) probably won't — the trap is subtle. |
| C1 rigidity (false positive) | C1/C2 guard-rails should prevent it (literally says "run a null"). Self-review (E) might catch it if prompted. Bare/plan-first probably falls in the same trap. |

**Punchline prediction:** C2 (library guard-rails) will dominate, B (generic plan) will be a no-op, and the interesting question is whether F (fresh reviewer) catches things E (self-review) doesn't.

## Cheap Diagnostic First

Before running 18+ expensive explorer sessions, do a pre-test:

Take the 3 GOAL.md files and the known right answers. Give each to a fresh Claude with just: "Here's a research task. Before doing it, list the top 3 ways you could get this wrong."

If the model CAN identify the failure modes when explicitly asked, the problem is **application** (knows the trap but doesn't check during execution). Fix: guard-rails, checklists, forced verification steps.

If the model CANNOT identify the failure modes, the problem is **knowledge**. Fix: better training data, domain-specific context, or accept the limitation and rely on fresh adversarial reviewers (F).

## Practical Execution Notes

- **Sample size:** 1 run per cell is noise with LLM variance. Need at least 3 runs per cell for any confidence. Prioritize: pick 2-3 most informative conditions and run those 3× each against baseline.
- **Suggested priority:** G (open-ended) and C2 (library guard-rails) vs A (baseline), on all 3 tasks. That's 27 runs and tests the most important hypotheses.
- **Cost:** Each explorer run is significant tokens. Budget accordingly.
- **Measurement per run:**
  - Correctness (binary: right answer or not)
  - Did it run the right checks? (convergence test for Li, null experiment for C1, adversarial modes for H_norm)
  - Tokens consumed
  - Wall-clock time
  - Confidence calibration (how confident was it in its conclusion, especially when wrong)

## What We're Trying to Learn

1. **Are current goals too prescriptive?** Does the strategizer's step-by-step recipe help or constrain?
2. **Do library meta-learnings transfer?** Can generic methodology lessons prevent specific errors?
3. **Is self-review useful or does it need fresh eyes?** E vs F comparison.
4. **Is the failure mode knowledge or application?** The cheap diagnostic answers this.
5. **What should we bake into the explorer system prompt?** Winners from the test matrix become permanent additions.
