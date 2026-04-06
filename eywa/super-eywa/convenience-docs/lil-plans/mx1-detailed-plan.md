# Mission Exploration 1 Detailed Plan

## Purpose

Mission Exploration 1 is the prompt-optimization sweep that builds the evidence base for later prompt selection.

We are not building Buddy yet.

But MX1 should be built so that later Buddy can read the same data and use it to choose prompt family + prompt at node time.

## Core Shape

The basic unit of MX1 is:

- one question
- one prompt family
- ten runs

After ten runs on one `(question, family)` pair:

- keep the same question
- switch to the next family
- run ten more iterations

After all families have been tried on that question:

- move to the next question

So MX1 is a collection of independent prompt-improvement loops over fixed `(question, family)` pairs.

## Families In Scope

Initial families:

- `transmute`
- `delegate`
- `execute`

Possible later family:

- `review`

But `review` is out of scope for the first implementation because it adds more orchestration complexity.

## Immediate Pilot

Before full MX1, we will prove the loop on:

- one question
- one family

The first pilot should use:

- one auto-graded benchmark question
- family = `transmute`

This is just the first slice of MX1, not a separate architecture.

## Runtime Shape For The First Pilot

For the `transmute` family pilot:

- root node prompt family is hardcoded to `transmute`
- child node prompt family is hardcoded to `execute`
- root prompt text is the thing being optimized
- child prompt text stays minimal and stable

So the experiment isolates the effect of the transmutation prompt.

This should be done with generic variables, not with special-case runtime code.

The existing child-node variable pattern is the right foundation:

- `child_prompt_family`
- `child_selected_prompt_text`
- `child_base_header_prompt`

## Optimization Objective

The ordering is:

1. improve score / correctness first
2. reduce tokens second
3. reduce wall-clock time third

The tutor should not trade away correctness for a small efficiency gain.

## Exploration Policy

MX1 is not greedy from the start.

Rules:

- iterations `01-03` should lean heavily toward exploring meaningfully different prompt directions
- later iterations may refine promising directions
- if progress plateaus, the tutor should push exploration again

Plateau rule:

- if two tries in a row fail to improve tokens or time by at least `10%`
- and do so without sacrificing score
- then the tutor should lean toward a new prompt direction

## What The Tutor Sees

The tutor is separate from grading.

The tutor should see:

- the question
- the family being optimized
- the current prompt
- the current run's score
- total tokens
- total wall-clock time
- total cost
- relevant run outputs
- orchestration summary
- all prior attempts for the same `(question, family)`
- prior prompts and their outcomes

The tutor does not need every raw artifact by default.

It should get the useful summary plus enough run output to understand what happened.

## What The Tutor Produces

The tutor should emit structured JSON focused on prompt optimization.

At minimum:

- current prompt
- current outcome summary
- what likely helped
- what likely hurt
- whether this looks like exploration or refinement territory
- recommendation action:
  - `keep`
  - `adjust`
  - `pivot`
- next prompt text
- confidence

The tutor is not a grader.

It should not decide correctness itself.

## Prompt Strategy Labels

We do not want a rigid taxonomy.

But the tutor should still be able to describe prompt direction at a high level when useful, such as:

- simplifying
- formalizing
- reframing into subgoals
- emphasizing answer format
- encouraging verification

These are examples, not a fixed ontology.

## Starting Prompts

We are not treating family starter prompts as deeply meaningful defaults.

For MX1, each family can begin from a chosen starter prompt.

The point of MX1 is to improve from there.

So each `(question, family)` loop should record:

- the starter prompt
- why it was chosen if known

## Holdout Policy

For full MX1:

- choose 5 holdout questions
- make them diverse
- freeze them before the full sweep

The holdout is not part of the one-question pilot, but the plan should preserve this boundary.

## Data Model Principles

### 1. Local files are canonical

All loop truth must be reconstructable from local files.

Supabase is a mirror and query surface, not the canonical source of truth.

### 2. One loop manifest per `(question, family)` loop

Each loop should have a simple manifest tracking:

- loop id
- question id
- family
- model
- iteration count
- starter prompt
- all attempted prompts
- run ids
- grading record paths
- tutor record paths
- score/tokens/time/cost per iteration
- best iteration so far

This manifest should be the cleanest way to understand the full loop.

### 3. One main run row in Supabase should contain the important truth

We want one primary row per run that includes:

- run metadata
- score / grading result
- metrics
- tutor output or tutor summary

So the existing `graded_runs` row should remain the main row and be expanded as needed rather than splitting the system into many small tables.

## Generic Foundation We Need

### Prompt registry

Prompt text should become first-class data.

Each prompt should have at least:

- `prompt_id`
- `prompt_family`
- `prompt_text`
- `created_by`
- `parent_prompt_id` if applicable
- notes

This will make prompt history much easier to inspect and later easier for Buddy to consume.

### Loop manifest

MX1 needs a stable manifest shape that can work first for:

- one question
- one family

and later for:

- all questions
- all families

### Tutor schema

The tutor schema should be prompt-optimization-specific, not a generic review schema.

## Implementation Order

### Phase 1

Write this MX1 plan and lock the experiment rules.

### Phase 2

Build the first pilot:

- one question
- family `transmute`
- ten iterations
- root `transmute`
- child `execute`

### Phase 3

Run the pilot once end to end.

### Phase 4

Verify and fix:

- tutor schema
- manifest shape
- metric propagation
- Supabase sync
- run reconstruction

### Phase 5

Scale from the single pilot to broader MX1:

- same question, more families
- then more questions
- then holdout-aware full sweep

### Phase 6

After MX1 produces enough useful evidence, build Buddy on top of that dataset.

## What Success Looks Like

The pilot is successful when:

- one `(question, family)` loop can run for ten iterations
- grading is automatic
- tutor is separate
- tutor can see full same-loop history
- prompt changes are easy to inspect
- score/tokens/time trends are easy to compare
- the loop can be reconstructed from local files alone
- Supabase mirrors the important run and tutor data cleanly

MX1 as a whole is successful when:

- all non-holdout questions can be run through this same loop structure
- each family has comparable progression data
- the results are easy to interpret later when Buddy is introduced

