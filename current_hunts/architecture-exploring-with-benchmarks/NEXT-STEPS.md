# Next Steps: Mapping the "Best Approach for a Given Task" Boundary

**Date:** 2026-03-30
**Context:** Two sessions of architecture exploration (F1-F29 in FINDINGS.md). Core question remains: given a task, what's the best approach? And how do we systematically learn that?

## The Core Question

We know WHAT works (specific reasoning instructions, vote, retrieval, critic). We don't yet know HOW TO PREDICT which approach to use for a new task without trial and error. The goal is a system that, given a novel task, selects the right architecture automatically.

## What We've Established So Far

The boundary isn't "planning vs no planning." It's "what is the model missing?"

| What's missing | Best fix | Fix rate | Cost |
|---|---|---|---|
| Nothing (variance) | 3-way majority vote (separate agents) | ~100% | 3x |
| Knowledge | Retrieval augmentation | 100% (4/4) | ~1.5x |
| Computation accuracy | Critic + targeted hints | 80% (4/5) | ~1.5x |
| Reasoning approach | Specific instruction (M2/M4/D2/C1) | ~2x accuracy | 1x |
| Systematic understanding | Nothing single-model | 0% | N/A |

Generic planning ("make a plan") is a no-op. Specific reasoning instructions that channel the model into a different path DO work.

## The Gap: We Can't Yet Predict the Failure Mode

Right now we classify failure modes AFTER seeing the wrong answer. We need to classify BEFORE — from the task description alone. That's the dispatcher problem.

## Proposed Next Experiment: Clean Room Atlas Reproductions

Use real Atlas explorer tasks as benchmarks. These are better than competition problems because:
- Not in training data (original research tasks)
- Multi-step reasoning + computation (not just answer a question)
- Known ground truth from completed explorations
- Include cases where explorers made wrong conclusions we can test against

### 3 Selected Tasks

**Task 1: Yang-Mills Hessian Bound (H_norm = 1/12)**
- Type: "Find the right answer" — compute tight eigenvalue bound
- Ground truth: H_norm = 1/12, achieved by staggered mode v_{x,μ} = (-1)^{|x|+μ}
- Source: Yang-Mills S2-E007/E008, verified by E009
- Tests: systematic search, mathematical insight + computation

**Task 2: Riemann Li Coefficient Crossover (WRONG then CORRECTED)**
- Type: "Avoid a methodology trap" — compare sequences correctly
- Ground truth: Initial answer 0.95 was WRONG (density mismatch). Correct: 1.09 at matched K=N=5000
- Source: Riemann S3-E002 → E009
- Tests: whether architecture avoids comparing mismatched ensembles

**Task 3: Riemann C1 Intermediate Rigidity (FALSE POSITIVE)**
- Type: "Run the right control experiment"
- Ground truth: Von Mangoldt amplitudes do NOT create anomalous Δ₃. Flat random amplitudes give the same value — it's generic finite-size GUE.
- Source: Riemann S2-E005 → E009
- Tests: whether architecture tests null hypothesis before claiming novelty

### 6 Conditions Per Task (18 runs total)

| # | Condition | What it tests |
|---|-----------|---------------|
| A | Bare goal (control) | Baseline — what happens with no guidance? |
| B | "Plan first" prepended | F27 replication — is generic planning still a no-op on research tasks? |
| C | Methodological guard-rails | Do targeted instructions prevent the known traps? (Like M2/D2 but for research methodology) |
| D | Opus plan → Sonnet exec | Does plan transfer work for research tasks? (extends F5) |
| E | Self-review (same agent) | Does self-critique catch research errors? (extends F9) |
| F | Fresh adversarial reviewer | Do fresh eyes catch what self-review misses? |

### Guard-Rails for Condition C (task-specific but generalizable methodology)

- **Task 1 (H_norm):** "After finding a candidate maximum, verify it's the global max by checking non-obvious modes (alternating signs, staggered patterns). Don't stop at the first plausible eigenvector."
- **Task 2 (Li coefficient):** "When comparing two sequences, verify your comparison is apples-to-apples — matching density, normalization, N. Run at 2+ scales to check robustness."
- **Task 3 (C1 rigidity):** "Before claiming any result is caused by a specific structural feature, run a null experiment with that feature removed. If the null gives the same result, your feature isn't the cause."

These are reusable methodology patterns, not task-specific hints.

### What We Measure

- **Correctness:** Did it reach the right answer / avoid the trap?
- **Tokens consumed** and **wall-clock time**
- **Did it run the right checks?** (verify matching for Task 2, run null for Task 3)
- **Confidence calibration:** How confident was it in a wrong conclusion?

### Expected Outcomes

If F27 holds for research tasks: Condition B ≈ Condition A (generic plan still no-op).
If guard-rails work: Condition C >> A and B (targeted methodology prevents traps).
New question: Does Condition F (fresh reviewer) >> Condition E (self-review)?

## Bigger Picture: Building the Reusable Pipeline

Once we validate the clean room approach on these 3 tasks, the pipeline generalizes:

### Phase 1: Task Bank (reusable, contamination-free)
- Source from completed Atlas explorations with known outcomes
- Generate original problems programmatically (vary step count, working memory load)
- Tag each with failure-mode ground truth

### Phase 2: Model Profiling (per new model)
- Run each task 5x to separate variance from systematic failure
- Classify: Easy (5/5), Reliable (3-4/5), Unreliable (1-2/5), Hard (0/5)

### Phase 3: Failure Mode Classification (per model)
- For non-Easy tasks: variance, computation, discrimination, systematic, knowledge gap
- This is the classification we need to automate

### Phase 4: Architecture Sweep (per failure mode)
- Test each condition (A-F) on each failure mode bucket
- Build the mapping: failure mode → best architecture

### Phase 5: Dispatcher Validation
- Build the classifier that predicts failure mode from task description alone
- Test end-to-end: task → predicted failure mode → selected architecture → result
- Compare to oracle dispatcher (uses ground-truth failure mode)

### The Key Deliverable
A function: `task_description → recommended_architecture` that works for new tasks without trial and error. The gap between the oracle dispatcher and the learned dispatcher tells us how much room there is to improve.

## Open Questions

1. **Can we classify failure modes from task descriptions alone?** This is the hard part. We can classify AFTER seeing the wrong answer. Can we do it BEFORE?

2. **Do the guard-rails generalize?** The 3 methodology patterns (check non-obvious modes, verify apples-to-apples, run null experiments) might cover a large fraction of research task failures. Or they might be too specific.

3. **Is fresh adversarial review worth the cost?** If Condition F >> Condition E, that's a strong signal for multi-agent architectures on research tasks. If F ≈ E, self-review is sufficient.

4. **How do these results change with new models?** The whole pipeline is designed to be re-run. When Claude 5 / GPT-5 / Gemini 3 drops, run Phase 2-4 and see what shifts.

## Files Reference

- `FINDINGS.md` — All 29 findings from benchmark experiments
- `round-2-architecture-tests.md` — Detailed Round 2 results
- `question-bank/` — 60 questions, answer key, baseline results, exploration set
- Atlas explorer tasks: `current_hunts/atlas/execution/instances/*/strategies/*/explorations/*/`
