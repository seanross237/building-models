# Big-Plan-Babysit

This folder is for goals that are too large, uncertain, or long-running for a single `plan -> execute` cycle.

When the user says `big-plan-babysit`, switch into this operating mode.

## Core Idea

Do not try to solve the whole mission in one giant uninterrupted run.

Instead:

1. Create a persistent run folder on disk.
2. Produce a top-level plan.
3. If requested, run a multi-agent plan-sharpening round before committing to that plan.
4. Expand only the next phase into a detailed execution plan.
5. Hand that phase to a worker subagent.
6. Evaluate the result.
7. Decide whether to continue, pause, or replan.
8. Repeat until the goal is complete or a stop condition fires.

The run folder is the source of truth. Chat history is not.

## When To Use This

Use `big-plan-babysit` when:

- the task will likely take several distinct phases
- future phases depend on what is learned in earlier phases
- replanning is likely
- the user wants the system to keep going without constant supervision
- the user wants a record of plans, decisions, and outputs in one place

Do not use this when a normal single-pass plan and execution is enough.

## Required Run Inputs

Before starting a run, define these inputs as clearly as possible:

- `goal`: the outcome to reach
- `done_when`: explicit completion criteria
- `constraints`: time, scope, tools, permissions, or style limits
- `human_review_policy`: when the user must explicitly approve before continuing
- `stop_policy`: when the run should pause and ask for user input
- `replan_policy`: whether to patch the current plan locally or rebuild it more broadly
- `planning_ensemble`: whether to use multiple planning agents to sharpen the plan
- `budget_limits`: limits on time, spend, retries, or number of subagent calls

If something is missing, make a reasonable assumption and record it in the run folder.

## Standard Policies

### Human Review Policies

- `none`: do not ask for approval before continuing
- `initial_plan`: ask only after the first top-level plan is created
- `major_replans`: ask whenever the top-level plan materially changes
- `every_phase`: ask before each new phase starts

### Stop Policies

- `never`: continue until done or blocked
- `major_decisions`: pause only at major decision points
- `external_input`: pause whenever outside information or human judgment is required
- `destructive_actions`: pause before irreversible or risky actions
- `budget_risk`: pause if a budget threshold is crossed

### Replan Policies

- `local_first`: repair the current plan locally before attempting a full rewrite
- `phase_only`: only replan the current and downstream phases
- `full_plan`: rebuild the full top-level plan when material assumptions change

## Major Decision Triggers

Treat a moment as a major decision point if any of the following is true:

- the top-level phase structure changes
- a new dependency, tool, or permission is required
- the next step is destructive, irreversible, or expensive
- two or more materially different strategies remain plausible
- confidence in the current plan falls below roughly `0.65`
- expected cost or scope grows by more than roughly `25%`
- the current plan can no longer satisfy `done_when`

If `stop_policy` includes major decisions, pause at these points and write down the reason.

## Planning Ensemble

The planning ensemble is optional and should normally run only for:

- the initial plan
- major replans

Do not run the full ensemble before every phase.

If `planning_ensemble.enabled: true`, run this sequence:

1. Create one planning brief.
2. Spawn `candidate_count` planner agents and require materially distinct plans.
3. Spawn one critic for each candidate plan.
4. Spawn one judge for each candidate plan and give each judge the original plan plus its critique.
5. Spawn one selector agent to compare the judged plans and choose the final plan.
6. Allow the selector to synthesize a hybrid only if it cites which candidate each adopted idea came from.

When possible, assign explicit strategy labels to planner agents so they do not converge on nearly identical plans. Good labels include:

- `audience-first`
- `structure-first`
- `content-first`
- `constraints-first`
- `risk-first`

If the runtime has a live agent limit, close completed planner threads before the critic wave, close completed critics before the judge wave, and close completed judges before the selector.

Default ensemble shape:

```yaml
planning_ensemble:
  enabled: true
  run_on:
    - initial_plan
    - major_replan
  candidate_count: 3
  strategy_labels:
    - audience-first
    - structure-first
    - constraints-first
  critic_per_candidate: 1
  judge_per_candidate: 1
  selector_mode: synthesize_best
  require_distinct_strategies: true
  max_rounds: 1
```

Each role should produce the following:

- `planner`: plan, assumptions, risks, sequencing rationale
- `critic`: strongest objections, missing prerequisites, failure modes
- `judge`: revised plan, scorecard, recommendation
- `selector`: selected plan or hybrid, why it won, why others lost

Use the ensemble to sharpen the plan, not to create endless recursive debate.

## Run Folder Layout

Create each run under:

```text
big-plan-babysit/runs/YYYY-MM-DD--goal-slug--NNN/
```

Required contents:

```text
runs/
  YYYY-MM-DD--goal-slug--NNN/
    RUN.md
    STATE.yaml
    JOURNAL.md
    planning/
      round-001/
        BRIEF.md
        candidate-01-plan.md
        candidate-01-critique.md
        candidate-01-judgment.md
        candidate-02-plan.md
        candidate-02-critique.md
        candidate-02-judgment.md
        candidate-03-plan.md
        candidate-03-critique.md
        candidate-03-judgment.md
        selection.md
        adopted-plan-v001.md
    plans/
      plan-v001.md
    phases/
      phase-001/
        PHASE.md
        EXECUTION-PLAN.md
        RESULT.md
        EVALUATION.md
    decisions/
      decision-001.md
    final/
      FINAL-SUMMARY.md
```

You do not need every planning-round file if the planning ensemble is disabled. In that case, write the adopted plan directly into `plans/plan-v001.md`.

## File Responsibilities

Use the files consistently:

- `RUN.md`: human-readable run setup, policies, and current mission summary
- `STATE.yaml`: current status snapshot, next phase, plan version, outstanding risks
- `JOURNAL.md`: running timeline of major events
- `planning/...`: all ensemble artifacts from a planning round
- `plans/plan-vNNN.md`: the authoritative current top-level plan
- `phases/phase-XXX/PHASE.md`: phase objective, acceptance criteria, dependencies
- `phases/phase-XXX/EXECUTION-PLAN.md`: detailed plan for that single phase
- `phases/phase-XXX/RESULT.md`: what the worker actually did and produced
- `phases/phase-XXX/EVALUATION.md`: whether the phase succeeded and whether the broader plan still holds
- `decisions/decision-XXX.md`: key choices, tradeoffs, and why they were made
- `final/FINAL-SUMMARY.md`: final outcome, what remains, and whether `done_when` was met

## Required Contents Of `STATE.yaml`

At minimum, keep these fields current:

```yaml
run_id: 2026-04-01--goal-slug--001
status: planning
goal: ""
done_when: []
current_plan_version: 1
current_phase: null
next_action: ""
human_review_policy: none
stop_policy: major_decisions
replan_policy: local_first
planning_ensemble:
  enabled: false
  last_run: null
budgets:
  max_subagent_runs: null
  max_replans: null
  max_timebox_minutes: null
progress:
  completed_phases: []
  pending_phases: []
assumptions: []
risks: []
open_questions: []
decision_log: []
```

`STATE.yaml` does not need to be perfect YAML for machines. It does need to be structured and current.

## Standard Operating Procedure

### 1. Initialize The Run

Create the run folder and write:

- `RUN.md`
- `STATE.yaml`
- `JOURNAL.md`

Record:

- the user goal
- the completion criteria
- the policies
- any assumptions you had to make

### 2. Create The Top-Level Plan

Break the mission into phases that are:

- outcome-oriented
- independently evaluable
- ordered by dependency

Do not over-decompose at the top level. Usually `3-7` phases is enough.

### 3. Optionally Run The Planning Ensemble

If enabled:

- write the brief
- run planners
- close completed planner agents if needed before the next wave
- run critics
- close completed critic agents if needed before the next wave
- run judges
- close completed judge agents if needed before the next wave
- run the selector
- adopt the winning or synthesized plan

Record the selection rationale.

### 4. Execute One Phase At A Time

For the next unresolved phase:

1. Write `PHASE.md`
2. Write `EXECUTION-PLAN.md`
3. Spawn a worker subagent for that phase only
4. Save the worker output into `RESULT.md`
5. Evaluate the result in `EVALUATION.md`
6. Update `STATE.yaml` immediately after the evaluation

The worker should receive only the context needed for that phase plus the current plan and relevant decisions.

### 5. Evaluate After Every Phase

Ask:

- did the phase meet its acceptance criteria?
- what assumptions were confirmed or broken?
- does the current top-level plan still make sense?
- should the next phase remain the same?
- did a major decision trigger fire?
- is a replan needed?

Write the answers down. Do not keep them only in chat.

### 6. Continue, Pause, Or Replan

After evaluation:

- continue if the plan still holds
- pause if a stop policy fires
- replan if the current structure no longer makes sense

If replanning changes the top-level structure, create a new `plans/plan-vNNN.md` and update `STATE.yaml`.

### 7. Close The Run

A run ends only when one of these is true:

- `done_when` is satisfied
- the run is blocked and cannot continue without the user
- budget limits are exhausted
- the user stops the run

Write `final/FINAL-SUMMARY.md` before closing.

## Worker Guidance

When spawning a worker for a phase:

- give it one phase only
- give it explicit acceptance criteria
- give it relevant constraints and file paths
- tell it not to silently redefine the mission
- tell it to surface blockers and deviations clearly

If the worker discovers that the phase goal is wrong, that is an evaluation signal for the supervisor, not permission for the worker to silently rewrite the whole project.

## Selector Guidance

When using the planning ensemble, the selector must do one of two things:

- `pick_best`: select one judged plan with minimal changes
- `synthesize_best`: produce a hybrid plan and cite which candidate each major element came from

The selector must also explain:

- why the winning plan is best for the goal
- why the losing plans were not selected
- what risks remain even in the winning plan

## Minimum Quality Bar

A clean `big-plan-babysit` run should leave behind enough artifacts that another agent can resume it without guessing.

At minimum, another agent should be able to answer all of these from the run folder alone:

- what is the goal?
- what counts as done?
- what is the current plan?
- what phase was last executed?
- what happened in that phase?
- what decisions were made and why?
- what happens next?

If the run folder does not answer those questions, the run is not clean.

## Default Recommendation

Unless the user says otherwise, use these defaults:

```yaml
human_review_policy: none
stop_policy: major_decisions
replan_policy: local_first
planning_ensemble:
  enabled: true
  run_on:
    - initial_plan
    - major_replan
  candidate_count: 3
  critic_per_candidate: 1
  judge_per_candidate: 1
  selector_mode: synthesize_best
```

## Trigger Phrase

If the user says `big-plan-babysit`, interpret it as:

"Create a persistent run folder, produce a top-level plan, optionally sharpen it with the planning ensemble, then execute phase by phase with evaluation and replanning until the goal is complete or a stop condition fires."
