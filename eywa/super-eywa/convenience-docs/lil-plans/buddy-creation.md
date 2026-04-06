# Buddy Creation

## Overview

Project 2.

Introduce a concept called **Buddy**. Buddy runs **before every node** in Eywa. His job is to decide, for the node that is about to run, which **prompt family** and which **prompt** to give it.

Buddy uses:

- the problem / input the node is about to handle
- the database of past runs (problems, families, prompts, scores)

to make that choice.

The end goal of this project: **one single best Buddy prompt** that we trust as the default Buddy behavior.

## Prerequisite

Buddy depends on having the database in shape — specifically the result of Mission Exploration 1 (or at least partial MX1 data).

Buddy leans on:

- past problems
- what family / prompt was used on them
- the scores they got (correctness, tokens, time)
- (ideally) tags / question-type info

Buddy can still work on data that has **no recorded Buddy prompt** (because it was produced before Buddy existed). That historical data is still useful — Buddy just treats "Buddy prompt" as optional on prior rows.

## How Buddy Runs

For each node run in Eywa:

1. Buddy runs **first**.
2. Buddy sees:
   - the problem / input heading into the node
   - relevant past runs pulled from the database
   - past scores on similar problems under different families and prompts
3. Buddy outputs:
   - the chosen **family type** for the node
   - the chosen **prompt** (within that family) for the node
4. The node runs with that family + prompt.
5. The run is scored as usual.

Buddy is a node-level decision-maker — it sits in front of every node, not just the root.

## The Buddy Prompt Optimization Loop

Buddy itself has a prompt — the "Buddy prompt" — that governs how Buddy makes decisions.

We optimize the Buddy prompt via a reviewer loop analogous to MX1's, but one level up:

1. Start with an initial **Buddy prompt**.
2. Buddy receives a question, does its job, assigns family + prompt to the node.
3. The node runs. We get scores back.
4. A **reviewer** looks at:
   - the Buddy prompt that was used
   - what Buddy decided
   - the resulting scores
   - a **history** of prior Buddy prompts and their resulting scores
5. Reviewer proposes a **new Buddy prompt**.
6. Next run uses that new Buddy prompt.
7. Repeat.

The reviewer is not scoring the node's answer in isolation — it is scoring **Buddy's decision quality** as reflected in the final outcome.

## Per-Question vs. Per-Batch Review

We want to try two review modes:

- **Per-question review**
  - reviewer looks at a single question outcome and updates the Buddy prompt
  - fast feedback, noisier signal
- **Per-batch review**
  - reviewer looks at a batch of question outcomes and updates the Buddy prompt
  - slower feedback, cleaner aggregate signal

Both are in scope. We want to see which produces better Buddy prompts, and whether a mix works best (e.g. per-question early, per-batch later).

## Dealing With Pre-Buddy Data

Some rows in the database will not have a `buddy_prompt` field because they were produced before Buddy existed.

That's fine:

- treat `buddy_prompt` as optional on historical rows
- Buddy can still learn from the `(problem, family, prompt, score)` signal on those rows
- Buddy's own reviewer only needs Buddy-era rows to evaluate **Buddy prompt quality**, not to evaluate the underlying family/prompt quality

## End State

Buddy Creation is done when:

- Buddy exists and runs before every node
- Buddy reads the database and chooses family + prompt per node
- a Buddy-prompt optimization loop has been run (per-question and per-batch variants tried)
- we have converged on **one single best Buddy prompt** that is adopted as the default

## Open Questions

- how much of the database Buddy should see per decision (top-k similar problems? tag-matched subset? whole table?)
- whether Buddy's decision and the reviewer's updates should factor in tokens/time cost of Buddy itself
- whether Buddy should output a confidence or fallback when it has no relevant history
- how to define "similar problem" for the past-runs lookup (depends on the tagging system from MX1)
- whether the Buddy reviewer should also see the reasoning/tool-calls context (same open question as MX1's reviewer)
- whether Buddy needs different prompts for root nodes vs. deeper nodes, or if truly one prompt is enough

## Relationship To Mission Exploration 1

- **MX1** tells us which families/prompts tend to work on which kinds of problems.
- **Buddy** operationalizes that knowledge live, at node time, per node.
- MX1 populates the database Buddy reads from.
- Buddy's success is partially a validation that MX1's findings were learnable from the data.
