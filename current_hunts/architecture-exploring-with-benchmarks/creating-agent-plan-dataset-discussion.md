# Experiment 9: Plan Evaluation — Discussion & Design

**Date:** 2026-03-28
**Status:** Design phase
**Predecessor:** Experiment 7 (system prompt gauntlet — found T5 Triple Fusion as best single prompt)

## Motivation

Experiment 7 showed that single-prompt approaches hit a variance ceiling. T5 Triple Fusion scores 8/9 one run, ~6/9 the next. The prompt is near-optimal; the architecture isn't. The next question is: **does separating planning from execution improve reliability?**

More broadly: how should agents decompose, organize, and execute multi-step reasoning? What makes a good plan? Can bad plans be identified before execution?

## Core Idea

Build a labeled dataset of plans and their outcomes. Analyze the dataset to discover what attributes of a plan predict success.

## Three Independent Variables

### 1. Meta-plan (strategy for decomposition)
Generic instructions for how to decompose *any* problem. Analogous to T1-T10 system prompts from Experiment 7, but one level up — these are system prompts for *planning how to solve* rather than for *solving directly*.

Example meta-plan: "When given a problem, first identify what type of reasoning it requires. Then list all constraints. Then identify which constraints interact. Then propose an order of operations that resolves dependencies first..."

**What we're testing:** Which meta-plans produce better instance-plans across a diverse question set?

### 2. Instance-plan (the actual decomposition)
The concrete plan an agent produces when given a meta-plan + a specific problem. This is the observable artifact — the decomposition, the steps, the identified challenges.

Example instance-plan: "Step 1: Parse the 12 constraints from the puzzle. Step 2: Assign houses to positions using the direct-placement constraints first. Step 3: Check remaining constraints..."

**What we're testing:** What structural features of instance-plans correlate with success, regardless of which meta-plan produced them?

### 3. Execution architecture
How agents are assigned to execute the steps in an instance-plan.

Options to test:
- **Single agent, all steps** — one context window, no handoffs. Simplest.
- **One agent per step** — each step gets clean context with problem + plan + prior step outputs. Prevents contamination, loses continuity.
- **Orchestrator + workers** — one agent manages flow, spawns fresh agents for steps, synthesizes results. Can checkpoint and pivot.

**What we're testing:** Does execution architecture matter independently of plan quality?

### 4. Plan critique (adversarial review before execution)
An additional agent reviews the instance-plan before execution begins and pokes holes — identifies logical gaps, wrong assumptions, missing cases, or flawed decomposition.

Options to test:
- **No critique** — plan goes straight to execution (control)
- **Single critic** — one agent reviews the plan, planner revises
- **Adversarial critic** — critic actively tries to find failure modes
- **Multiple independent critics** — diverse perspectives on the same plan

**What we're testing:** Does pre-execution critique improve outcomes? Does it improve them enough to justify the cost?

## Plan Schema (Draft)

```markdown
## Problem
[short title + source]

## Problem Type
[what kind of reasoning — constraint satisfaction, state tracking, logical deduction, pattern recognition, computation, etc.]

## Key Challenges
[what makes this hard / where a naive approach would fail]

## Steps
1. [step description] → [agent assignment: same agent / fresh agent]
2. [step description] → [agent assignment]
...

## Assumptions
[anything being taken for granted that could be wrong]

## Checkpoints
- After step N: [condition to check — if fails, pivot to...]

## Pivot Triggers
[what would indicate the plan is wrong and needs revision]

## Verification
[how to check the answer before committing]
```

## Execution Loop

1. **Planning agent** receives: meta-plan (system prompt) + problem → produces instance-plan. Explicitly told: do NOT solve yet.
2. **[Optional] Critique agent** receives: problem + instance-plan → produces critique / revision suggestions.
3. **[Optional] Planning agent revises** based on critique.
4. **Execution agent(s)** receive: problem + instance-plan → execute steps, produce answer.
5. **Record:** `(meta-plan, instance-plan, critique (if any), execution-architecture, problem, answer, correct?)`

### Adaptive execution (later iteration)
After each step completion, a supervisor agent receives the results and decides:
- Proceed to next step on current plan
- Pivot — create a new plan based on what was learned
- Escalate — flag that the problem needs re-decomposition

## Dataset Structure

Each row in the dataset:

| Field | Description |
|-------|-------------|
| `problem_id` | Which benchmark question |
| `problem_source` | BBEH, HLE, ARC-AGI, FrontierMath |
| `meta_plan_id` | Which meta-plan was used (M1, M2, ...) |
| `instance_plan` | The full plan text produced |
| `critique` | Critique text (if critique step was used, else null) |
| `revised_plan` | Revised plan after critique (if applicable, else null) |
| `execution_arch` | single-agent / per-step / orchestrator |
| `model` | Which model (Opus 4.6 / Sonnet 4.6) |
| `answer` | The answer produced |
| `correct` | Boolean |
| `plan_generation_tokens` | Token cost of planning phase |
| `execution_tokens` | Token cost of execution phase |
| `total_time` | Wall-clock time |

## Analysis Plan (What To Do With The Dataset)

### A. Which meta-plans win?
Score each meta-plan across problems. Equivalent to Experiment 7 scoring T1-T10. But now we also have instance-plans to inspect *why* one meta-plan beat another.

### B. What structural features of instance-plans predict success?
Compare winning vs. losing instance-plans for the same problem. Look for:
- Did the plan identify the actual hard part?
- Did it flag the right assumptions/traps?
- Number of steps — too few (underspecified) vs. too many (overfit)?
- Did it include verification steps?
- Did it correctly classify the problem type?
- Were steps actually independent or did it create false dependencies?

If identifiable, these features become a **rubric for plan quality**.

### C. Can you predict success from the instance-plan alone (without execution)?
Give a judge agent: problem + instance-plan (no answer, no execution trace). Ask: will this plan succeed? If the judge predicts outcomes above chance, instance-plans carry evaluable signal and bad plans can be filtered pre-execution.

### D. Does execution architecture matter independently?
Same instance-plan, different execution architectures. If multi-agent consistently rescues failing plans, execution is load-bearing. If outcomes match, plan quality is what matters.

### E. Does critique improve outcomes?
Same meta-plan, same problem, with and without the critique step. Does critique reliably catch the failure modes that lead to wrong answers? Or does it introduce over-analysis (like T4 Conservative+Evidence did in Experiment 7)?

### F. Feedback loop
The rubric from analysis B becomes instructions in next-generation meta-plans: "When decomposing a problem, make sure your plan explicitly identifies [features that predicted success]." Each round refines the meta-plans based on empirical findings, same as Experiment 6 findings fed into Experiment 7 prompt design.

## Experimental Staging

**Phase 1: Meta-plan tournament (hold execution constant)**
- Design M1-M10 candidate meta-plans
- Run all meta-plans against a fixed question set (BBEH characterized questions)
- Single-agent execution throughout (control)
- No critique step (control)
- Goal: find the best meta-plans, collect instance-plan dataset

**Phase 2: Critique evaluation (hold meta-plan and execution constant)**
- Take the winning meta-plan(s) from Phase 1
- Run with and without critique step
- Same questions, same execution architecture
- Goal: measure whether critique adds value

**Phase 3: Execution architecture (hold meta-plan constant)**
- Take the winning meta-plan (and critique config if it helped)
- Test single-agent vs. per-step vs. orchestrator execution
- Same questions
- Goal: measure whether execution architecture matters independently

**Phase 4: Full system on hard questions**
- Best meta-plan + best critique config + best execution architecture
- Run against HLE (untested, genuinely hard) and high-variance BBEH questions
- Goal: measure end-to-end improvement over T5 baseline

## Open Questions

- How many meta-plans to test in Phase 1? (Experiment 7 did 10 — probably similar)
- How many runs per (meta-plan, question) pair? (Need 3-5 to measure variance)
- Should the planning agent and execution agent be the same model?
- What's the right granularity for steps? (Too fine = overhead, too coarse = no benefit)
- Should the instance-plan specify agent assignments, or should that be decided separately?
- How to handle problems where decomposition doesn't obviously apply (e.g., single-insight problems)?

## Relationship to Prior Work

This is a direct extension of Experiments 1-7:
- Experiments 1-7: "What system prompt makes a single agent solve better?"
- Experiment 9: "What system prompt makes an agent *plan* better, and does executing a plan beat direct solving?"

The T5 Triple Fusion prompt remains the baseline for direct solving. Any plan-based architecture needs to beat T5's 8/9 (R1) or at least stabilize T5's variance on hard questions.
