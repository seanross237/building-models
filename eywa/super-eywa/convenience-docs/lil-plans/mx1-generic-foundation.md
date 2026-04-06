# MX1 Generic Foundation

## Goal

Build the next phase around **Mission Exploration 1**, not Buddy yet.

But build it in a way where Buddy can later plug into the same primitives instead of forcing a rewrite.

## Core Idea

Keep the runtime generic.

The runtime should only care about:

- resolved variables for a node
- the prompt family chosen for that node
- the prompt text chosen for that node
- the JSON the node returns
- how that JSON drives orchestration

Everything else should sit outside the runtime as data, loop drivers, and analysis layers.

## What We Are Building Now

We are building the **prompt-optimization and evaluation layer**.

That means:

- prompt families stay generic
- prompt text becomes a first-class thing we track
- runs get graded automatically
- tutor stays separate from grading
- tutor recommends better prompts
- loop manifests track the history of each optimization run

For now, we stay narrow:

- one question at a time
- one family at a time when needed
- one optimized prompt variable at a time

## What We Are Not Building Yet

- Buddy
- per-node prompt selection from database history
- automatic live prompt choice before every node
- broad multi-family optimization all at once

Those come later.

## Design Principles

### 1. Runtime stays generic

Do not hardcode MX1 logic into the Eywa runtime.

The runtime should not know about:

- experiments
- tutors
- holdouts
- prompt-search loops
- Buddy

It should only execute with the variables it is given.

### 2. Prompts should be first-class data

Prompt text should not live only as anonymous strings inside old run rows.

We should be able to point to:

- which prompt was used
- what family it belonged to
- what prompt came before it
- what results it got

### 3. Loop history should be explicit

Each optimization loop should have one simple manifest that lets us reconstruct:

- what question was being worked on
- what family was being optimized
- which prompt was tried at each iteration
- what score, tokens, and time it got
- what the tutor recommended next

This makes the system legible without needing to query everything ad hoc.

### 4. Disk stays canonical

Local files remain source of truth.

Supabase is for:

- query
- views
- comparisons
- convenience

not canonical storage.

### 5. Tutor is separate from grading

The grader decides whether a run was right.

The tutor decides how to improve the prompt next.

Those should remain different roles.

## Generic Building Blocks We Need

### Prompt Registry

A clean place to store prompt candidates and metadata.

At minimum each prompt should carry:

- `prompt_id`
- `prompt_family`
- `prompt_text`
- `created_by`
- `parent_prompt_id` if applicable
- notes

### Loop Manifest

A simple file per optimization loop.

At minimum it should track:

- loop id
- question id
- family
- model
- iteration rows
- best iteration so far

### Tutor Output Schema

The tutor should emit structured data that is specifically about prompt improvement.

At minimum:

- what improved
- what got worse
- what likely helped
- what likely hurt
- recommended next prompt

### Clean Metrics

Each graded run should expose:

- score / correctness
- total tokens
- total wall time
- total cost

Those are the optimization targets.

## Immediate Build Order

1. Finish the single-question transmute tutor loop.
2. Add a simple prompt registry.
3. Add a reusable loop manifest format.
4. Make the tutor prompt-optimization-specific.
5. Run the first real 10-iteration loop.
6. After that, scale outward into MX1.

## How This Sets Up Buddy Later

Later, Buddy should not need a separate architecture.

Buddy should simply read the same kinds of data MX1 produced:

- past problem
- past family
- past prompt
- past score
- past token/time behavior

Then Buddy chooses:

- prompt family
- prompt

for a live node.

So the rule is:

- **MX1 produces the evidence**
- **Buddy consumes the evidence later**

## Success Condition

We are on the right track if:

- experiments are easy to run
- prompt history is easy to inspect
- results are easy to compare
- tutor recommendations are easy to trace
- none of this requires special-case runtime code

