# Plan Testing Dataset

**Date:** 2026-03-28
**Goal:** Build a labeled dataset of agent plans and their outcomes to discover what makes a good plan.
**Design doc:** [creating-agent-plan-dataset-discussion.md](../creating-agent-plan-dataset-discussion.md)

## What We're Testing

Does separating planning from execution improve reasoning accuracy? And if so, what kind of planning instructions (meta-plans) produce the best plans?

## Three Independent Variables

1. **Meta-plan** — generic instructions for how to decompose a problem (M1, M3, M5)
2. **Instance-plan** — the actual plan produced for a specific problem (observable artifact)
3. **Execution architecture** — held constant for this experiment: single agent executes all steps

## Conditions

### Baseline (no planning)
T5 Triple Fusion system prompt, direct solve:
> "Default to EXCLUSION -- better to select too few. Ground every claim in specific cited evidence. Before committing, consider the OPPOSITE of your initial reading. Check if surface patterns are misleading you. Only include what survives all three checks."

### M1: Classify-then-Decompose
> "Before planning how to solve this problem, classify it: What type of reasoning does it require? (constraint satisfaction, state tracking, logical deduction, computation, pattern recognition, or something else?) Then, based on that classification, decompose it into steps that are natural for that problem type. For each step, state what it takes as input and what it produces as output. Do not solve — only produce the plan."

### M3: Failure-Mode Planning
> "Before planning how to solve, identify how you could get this wrong. What are the traps? What assumptions might be wrong? What surface patterns could be misleading? List at least 3 failure modes. Then design your solving steps so that each failure mode is explicitly guarded against — each step should either avoid a failure mode or include a check for one. Do not solve — only produce the plan."

### M5: Vanilla Decomposition
> "Break this problem into logical steps to arrive at the answer. Do not solve — only produce the plan."

## Questions (4 from HLE)

| ID | Short Name | Subject | Answer | Type |
|----|------------|---------|--------|------|
| Q3 | exciton | Condensed matter — 2D semiconductor Rydberg energy | -0.08 | exactMatch |
| Q7 | partition | Thermodynamics — grand partition function | Z = 4.61, <k> = 1.66 | exactMatch |
| Q8 | mean-field | Thermodynamics — mean-field occupancy | 0.424 | exactMatch |
| Q10 | sintering | Materials science — coarsening gas effects | C | multipleChoice |

Full question text: [../benchmark-questions/hle/questions.md](../benchmark-questions/hle/questions.md)

## Run Matrix

4 questions x (1 baseline + 3 meta-plans) x 2 runs = **32 total runs**

| Condition | Runs per question | Total runs |
|-----------|-------------------|------------|
| Baseline (T5 direct) | 2 | 8 |
| M1 Classify | 2 | 8 |
| M3 Failure-Mode | 2 | 8 |
| M5 Vanilla | 2 | 8 |

## Execution Protocol

### Baseline runs
1. Give agent: T5 system prompt + question text
2. Agent solves directly
3. Record full trace + answer

### Plan runs (M1, M3, M5)
1. **Planning phase:** Give agent: meta-plan (as system prompt) + question text. Agent produces instance-plan only, does NOT solve.
2. **Execution phase:** Give fresh agent: T5 system prompt + question text + instance-plan. Agent executes the plan and produces answer.
3. Record: instance-plan + execution trace + answer

## Run Log Format

Each run is a markdown file in `runs/[question]/` with this structure:

```markdown
---
question: Q1-ftir
meta_plan: M1-classify | M3-failure | M5-vanilla | baseline
run: 1
model: opus-4.6
correct: true | false
answer_given: [answer]
answer_expected: [answer]
plan_tokens: [number or 0 for baseline]
execution_tokens: [number]
total_tokens: [number]
plan_time_s: [number or 0]
execution_time_s: [number]
total_time_s: [number]
---

## Instance Plan
[full plan text — null for baseline]

## Execution Trace
[full reasoning produced during execution]

## Final Answer
[the answer]
```

## Variance Follow-Up Protocol

If any condition goes 1/2 (correct once, wrong once) on a question, re-run that same (question, condition) pair with Sonnet 4.6 (2 additional runs). This tests whether the variance is model-inherent or plan-dependent:
- If Sonnet also goes 1/2 → the question is inherently high-variance, plan didn't stabilize it
- If Sonnet goes 0/2 or 2/2 → the model is the variable, not the plan
- Compare across conditions: if M3 is 2/2 but M5 is 1/2 on the same question, the meta-plan matters

## Results

See [summary.md](summary.md) for the aggregated results table.

## Directory Structure

```
testing-plans/
  README.md              (this file)
  summary.md             (aggregated results table)
  runs/
    Q3-exciton/          (8 run logs: 2 baseline + 2 M1 + 2 M3 + 2 M5)
    Q7-partition/
    Q8-mean-field/
    Q10-sintering/
```
