# Where We Are At

## Purpose

This is a quick pickup doc for the next agent.

It summarizes:

- where Super-Eywa currently is
- what has been built
- what was tested
- what important files to read first
- what the most obvious next steps are

## Current State

Super-Eywa now has a real v1 runtime skeleton with both:

- a deterministic local execution mode
- a live OpenRouter execution mode

The system can now:

- create a `run_packet`
- create `node_packet`s
- execute a root node
- branch into helper nodes
- store node records and replay artifacts on disk
- validate stored runs structurally
- run a first grading-bank flow against selected test questions

This means the system bones are now real.

The runtime is still early.

The biggest thing that is working is the structure:

- packets
- run storage
- replay storage
- timeline/story view
- baseline vs main grading runs
- live model seam

The biggest thing that is still weak is answer quality.

Delegation is now working structurally, but it is not yet reliably improving answers.

## What Was Built

### Eywa Runtime

Main runtime entrypoint:

- `eywa-system/runtime/run_v1.py`

Core runtime package:

- `eywa-system/runtime/eywa_runtime/`

Important runtime files:

- `engine.py`
- `executor.py`
- `openrouter_client.py`
- `secrets.py`
- `contracts.py`
- `validation.py`
- `prompting.py`

### Data / Grading

Run storage root:

- `data-system/run-history/`

Stored-run validator:

- `data-system/correctness-suite/validate_run_v1.py`

Single-question grading runner:

- `data-system/grading/run_test_question_v1.py`

Live batch runner:

- `data-system/grading/run_live_batch_v1.py`

Simple first grader:

- `data-system/grading/grading_methods/simple_grade_v1.py`

### Tests

Runtime tests:

- `eywa-system/runtime/tests/`

Grading tests:

- `data-system/grading/tests/`

## What Was Successfully Tested

The following are real, not just planned:

- runtime syntax checks
- runtime unit tests
- grading parser/grader tests
- deterministic smoke run
- live OpenRouter smoke run
- 5 baseline live grading runs
- 5 main live grading runs
- structural validation of stored runs

## Live Batch Summary

Main live batch summary:

- `data-system/grading/runs/live-batch-v1-summary.json`

Quick outcomes:

- `B6` Binary Representation Minimization
  - clean single-node success
  - baseline correct
  - main correct

- `B11` Board Game Rule Chaining
  - clean delegated success
  - baseline correct
  - main correct

- `B4` Hensel Lifting Verification
  - delegated successfully
  - still wrong

- `B10` Mean-Field Lattice Gas Occupancy
  - delegated successfully
  - still wrong

- `B5` Random Chords
  - stayed single-node
  - wrong in both baseline and main

So the current read is:

- the runtime seam works
- the storage model works
- the grading runner works
- the model integration works
- the quality layer needs work

## Important Review Docs

If you are picking this up, read these first:

- `high-level-north-star.md`
- `detailed-target-state.md`
- `current-state.md`
- `eywa-system/detailed-target-state.md`
- `data-system/detailed-target-state.md`
- `sticky-notes/daily-journals/2026-04-04/v1-handoff.md`
- `sticky-notes/daily-journals/2026-04-04/live-run-results-summary.md`
- `sticky-notes/daily-journals/2026-04-04/implementation-questions-and-judgment-calls.md`
- `sticky-notes/daily-journals/2026-04-04/file-hierarchies-for-review.md`

## Important Judgment Calls Already Made

These are already documented in more detail in the judgment-calls doc, but the big ones are:

- file-first storage before any DB dependency
- deterministic executor first, then live provider
- OpenRouter as first live provider
- OpenRouter key loading supports:
  - env
  - local `.env`
  - sibling `../open-eywa/.env`
  - keychain
- hard recursion cap of `3`
- first grading pass uses a narrow explicit grader subset, not fake universal grading
- question files are currently treated as summary-style question packets, not fully rich runnable packets
- decomposition is still mostly code-driven heuristic behavior, not yet a mature model/variable-controlled policy

## What Still Feels Incomplete

- many grading-bank question files are not truly runnable packets yet
- decomposition is still too heuristic
- verification is too weak for exact-answer tasks
- delegation improves structure more than it improves correctness
- the current correctness suite validates structure, not semantic correctness

## Presentation

A presentation already exists here:

- `/Users/seanross/kingdom_of_god/home-base/presentations/super-eywa-first-live-pass-2026-04-04/`

Main file:

- `/Users/seanross/kingdom_of_god/home-base/presentations/super-eywa-first-live-pass-2026-04-04/presentation.html`

## What I Said We Should Probably Do Next

This is my last message, included here so the next agent sees the current recommendation directly:

1. `Make the grading bank truly runnable`
   Right now many question files are summaries, not full runnable packets.
   I’d add a richer question format with:
   `full_prompt`, `expected_answer`, `grader_type`, `recommended_baseline_mode`, `recommended_main_mode`.

2. `Add a real verification layer inside Eywa`
   The runtime bones worked.
   The main weakness from the live runs was answer quality.
   I’d add exact-answer verification for numeric/string tasks before a node reports success.

3. `Replace the brittle decomposition heuristic`
   Right now branching is structurally working, but it is still basically splitter-driven.
   I’d make decomposition more explicit and variable-controlled, so we can tune when to stay local vs recruit help.

4. `Create a small canonical mini-benchmark set`
   Take maybe `5-10` good runnable questions and make them the first official comparison set.
   Then every change can be judged against the same baseline/main table.

If you want the best immediate move, it’s `1 + 2` together:
make the question packets real, then make Eywa verify exact-answer tasks before finishing.
