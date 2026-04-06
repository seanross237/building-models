# Mission Exploration 1

## Overview

A constrained prompt-optimization sweep over the grading-bank questions.

For each non-holdout question, we run a 10-iteration prompt-improvement loop per prompt family. The reviewer proposes a new prompt each iteration, trying to push score up, tokens down, and time down — while also exploring multiple directions rather than greedy single-path optimization.

The output is a dataset of:

- `10 × num_prompt_families × num_non_holdout_questions` rows
- per-question progression curves
- reviewer notes and suggested system improvements

## Step 0 — Carve Out a Holdout

Before the mission starts:

- Pick **5 questions** from the benchmark grading test set and mark them as a **holdout**.
- They should be **diverse** (different domains / difficulty / answer shapes).
- The holdout is not touched by Mission Exploration 1.
- It exists so we can later measure whether optimizations generalize.

## Step 1 — Define the Constraint Families

Each run in Mission Exploration 1 is pinned to one **prompt family** (the "constraint family").

Examples:

- `transmute`
- `delegate`
- (and whatever other families exist — `execute`, `agent_chooses`, etc.)

For a given question + family pair, only the prompt **inside that family** is optimized. The orchestration pattern stays fixed for that run group.

## Step 2 — The Per-Question, Per-Family 10-Iteration Loop

For every `(question, family)` pair where `question ∉ holdout`:

1. Start with the **default prompt** for that family.
2. Run the question through Eywa using that prompt.
3. Grade the run automatically. Scoring signal includes:
   - question correctness / score
   - total tokens used
   - total wall-clock time
4. Hand the run to the **reviewer**. Reviewer sees:
   - the question
   - the score + metrics
   - the run's relevant outputs
   - (on iterations ≥ 2) the **history** of prior prompts + their scores/metrics for this same `(question, family)`
5. Reviewer proposes a **new prompt** to try next.
6. Repeat for **10 iterations total** per `(question, family)`.

### Reviewer Behavior Guidance

The reviewer is not a pure greedy optimizer. Its mandate:

- If a new direction is improving scores → **keep exploring that direction**.
- If a direction is plateauing → **try a different direction**.
- The goal is a strong score **and** a diverse set of explored directions. Diversity is an explicit objective, not a side effect.

### Open Question — Reviewer Context Depth

We want to later run an experiment on **how much context the reviewer should see**.

Candidate extra signals to feed the reviewer:

- the **reasoning** the model used during the run (add reasoning as an output)
- **tool calls** made during the run
- other run artifacts

Hypothesis: richer reviewer context → faster convergence on good prompts.

This is not in scope for Mission Exploration 1 itself, but MX1 should preserve enough truth per run that this follow-up experiment is possible without re-running anything.

## Step 3 — Family Rotation on the Same Question

After 10 iterations on `(question, family_A)`:

- Move to `(question, family_B)` and start over from that family's default prompt.
- Repeat until all families have been explored for that question.

Then move to the next question.

Total runs after MX1:

```
runs = 10 × num_prompt_families × num_non_holdout_questions
```

## Step 4 — Per-Run Notes

Each run (and/or each review session) should compile notes covering:

- what the reviewer thinks went well / badly
- the **new suggested prompt**
- any observations about how the **system itself** could be improved (runtime, variables, contracts, data shape, etc.)
- anything else the reviewer surfaces

These notes should live somewhere consolidated so they are easy to read back later.

## Step 5 — Analysis Of Progression Curves

After the sweep, generate an analysis that shows:

- first-iteration score vs. **baseline** (pre-MX1 score of that question)
- average score at iteration 2, 3, 4, … 10
- same curves for tokens and wall time
- per-family curves and cross-family comparisons

The point is to see **how fast** the loop improves things, on average, and **how consistent** that improvement is.

## Step 6 — Database Analysis

The database will hold ~`10 × num_families × num_questions` rows from MX1.

From that, run:

- **best-performing family per question type**
- within each winning family, **best-performing prompts**
- (question types are a tagging system we still need to flesh out — see "Still To Decide" below)

## Step 7 — Consolidation Phase

After MX1 finishes, many of the prompts we discovered will be **similar to each other**.

We want a consolidation pass that:

- groups similar prompts
- merges them into representative prompts
- tries to keep those representatives **not overfit** to a single question
- produces:
  - **the best family to use per question type**
  - **the best prompts per family**, generalizing across questions of that type

Consolidation is about extracting durable lessons, not picking trophies.

## Future Work (Not In Scope Here, But Connected)

- **Optimize the reviewer itself.** This will require measuring things like **score-increase rate per review session** so we can compare reviewer variants.
- **Reviewer context depth experiment** (reasoning traces, tool calls, etc.) — see Step 2.
- **Holdout evaluation** to check whether MX1's winners generalize outside the questions they were tuned on.

## Still To Decide

- exact definition of "question type" / tagging system used in the per-type analysis
- which prompt families are included in MX1 vs. deferred
- how the consolidation pass decides "too overfit"
- where the compiled reviewer notes live (probably `sticky-notes/daily-journals/` during the run, then a consolidated doc after)
- exactly how diversity is measured/encouraged in the reviewer's proposals

## Success Criteria

MX1 is successful when:

- the holdout has been carved out and is untouched
- every non-holdout question has been run through every chosen family for 10 iterations
- progression curves (score / tokens / time) exist per family and per question
- database analysis surfaces best family per question type and best prompts per family
- a consolidation pass has produced a small set of durable, non-overfit recommended prompts per family
- we have a body of reviewer notes pointing at possible system improvements for later missions
