# Plan-Debate-Refinement

This folder is for improving a plan before execution.

When the user says `plan-debate-refinement`, switch into this operating mode.

## Purpose

Generate one initial plan, have five subagents critique it from different perspectives, then synthesize one stronger final plan.

This is a plan-quality workflow, not a long-running execution workflow.

## When To Use This

Use `plan-debate-refinement` when:

- the user wants a plan sharpened before execution
- the main uncertainty is plan quality rather than run supervision
- the stakes are high enough that weak sequencing or hidden assumptions matter
- the user wants deliberate multi-angle critique instead of a single fast draft

Do not use this when the user needs persistent execution, phase-by-phase tracking, or replanning over time. Use `big-plan-babysit` for that.

## Core Workflow

1. Write a planning brief.
2. Produce one draft plan.
3. Spawn five critic subagents, each with a distinct perspective.
4. Collect all critiques.
5. Spawn one refiner agent to produce the final plan.
6. Save the draft plan, critiques, and final plan in one folder.

## The Five Critic Perspectives

Use these five perspectives unless the user asks for different ones:

1. `feasibility`: can this actually be executed with the stated tools, time, and constraints?
2. `risks`: what is most likely to fail, break, or create downstream problems?
3. `dependencies`: what prerequisites, sequencing constraints, or hidden assumptions are missing?
4. `scope-and-simplicity`: where is the plan overbuilt, bloated, or doing too much?
5. `goal-fit`: does the plan actually maximize the user's intended outcome?

Each critic should attack the plan hard from its assigned angle instead of giving generic polish.

## Minimum Output From Each Critic

Each critic should return:

- strongest objections
- missing assumptions or prerequisites
- concrete revisions
- whether the plan is salvageable without a full rewrite

## Refiner Responsibilities

The refiner sees:

- the original brief
- the original plan
- all five critiques

The refiner must produce:

- the final plan
- the main revisions it made
- which critiques caused which revisions
- any residual risks

The refiner may keep parts of the original plan, but it must say why.

## Folder Layout

When you run this workflow, create a folder like:

```text
plan-debate-refinement/runs/YYYY-MM-DD--goal-slug--NNN/
```

Recommended contents:

```text
runs/
  YYYY-MM-DD--goal-slug--NNN/
    BRIEF.md
    DRAFT-PLAN.md
    critiques/
      feasibility.md
      risks.md
      dependencies.md
      scope-and-simplicity.md
      goal-fit.md
    FINAL-PLAN.md
    SUMMARY.md
```

## Standard Prompt Shape

### Planner

Tell the planner to produce:

- a concise top-level plan
- assumptions
- risks
- why the sequencing makes sense

### Critics

Tell each critic:

- which single perspective it owns
- to look for real failure modes, not generic polish
- to recommend concrete changes

### Refiner

Tell the refiner:

- keep what still works
- fix what the critiques exposed
- simplify whenever two options are equally good
- explain which critiques changed the plan

## Quality Bar

A good `plan-debate-refinement` output should make it obvious:

- what the original plan was
- what each critic objected to
- what changed in the final plan
- why the final plan is stronger

If that traceability is missing, the refinement was too opaque.

## Trigger Phrase

If the user says `plan-debate-refinement`, interpret it as:

"Generate a plan, run five distinct critiques against it, then synthesize one improved final plan and save the full debate trail."
