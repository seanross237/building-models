# Live Model Runs And Presentation Plan

## Purpose

This doc captures the next requested build scope so it does not get lost during context compaction.

It is the build plan for:

- live-model execution
- real test-question runs
- baselines
- run review
- presentation creation

## What Sean Requested

The requested next scope is:

1. build the live-model path out until the system can run real test questions
2. get to a first successful real test-question run
3. specifically ensure:
   - one successful single-node execution run
   - one successful delegated run
4. keep going until there are `5` successful live runs total
5. cap recursion depth at `3`
6. use a cheap model
7. also get baselines for the questions we run
8. then make a presentation covering:
   - what we built
   - how it works
   - how to run it
   - what happens step by step when we start a run
   - how the test runs went
   - all major judgment calls made while building
   - questions we should answer
   - recommendations based on the test runs
   - how the data ended up getting stored
   - file hierarchies
   - background images

## Current Starting Point

Already built:

- deterministic v1 runtime
- file-first run storage
- contract validation
- run-history layout
- correctness validator for stored runs
- unit tests
- one deterministic smoke run

Not built yet:

- live model executor
- real test-question runner
- baseline comparison runner
- 5 successful live test-question runs
- presentation about the built system and test results

## Main Constraints

### Runtime Constraints

- recursion depth must be capped at `3`
- keep the current file-first storage shape
- preserve the current runtime seam
- keep deterministic mode working

### Testing Constraints

- must include at least one successful single-node run
- must include at least one successful delegated run
- need `5` successful live runs total
- each run should be reviewable from stored artifacts

### Model Constraint

Use a cheap live model.

Current planned default:

- `google/gemini-2.5-flash-lite`

Reason:

- it is already used in Open-Eywa live canaries
- it is cheap enough for iteration
- it should be good enough for v1 integration testing

## Main Deliverables

### 1. Live Executor

Add a real live-model executor behind the same runtime seam as the deterministic one.

Initial planned provider:

- OpenRouter

Requirements:

- load API key from the same environment/keychain pattern already used elsewhere
- preserve raw request and raw response into replay
- record token/cost usage into node metrics
- preserve deterministic mode as the fallback/default-safe path

### 2. Test Question Runner

Add a runner that can execute from the grading bank directly.

It should be able to:

- point at a question file
- extract the question/task text
- launch a run using the current runtime
- write the resulting run under `data-system/run-history/`

This should reduce ad hoc prompt typing and keep test runs tied to the grading bank.

### 3. Baseline Protocol

For each selected live test question, also run a baseline.

Current planned baseline definition:

- same cheap live model
- single-node direct local attempt
- no decomposition

Current planned comparison run:

- same cheap live model
- normal v1 runtime behavior with decomposition allowed

Reason:

- this isolates the effect of delegation / orchestration better than comparing against deterministic mode
- it gives a practical first comparison without inventing a large benchmark framework first

### 4. Five Live Runs

Get to `5` successful live runs total.

Target mix:

- at least `2` single-node successful runs
- at least `2` delegated successful runs
- at least `1` additional run chosen for variety or failure-surface learning

Each successful run should be:

- stored cleanly
- validated by the correctness validator
- easy to compare against its baseline

### 5. Presentation

Create a dark-themed deck in `presentations/` that explains:

- what Super-Eywa v1 now is
- what was built
- the runtime seam
- the contract layer
- the run-history storage layout
- the file hierarchies
- how a run proceeds step by step
- how single-node vs delegated runs behave
- what happened in the live test runs
- what the baselines were
- what judgment calls were made
- what questions remain
- what recommendations came out of the live runs

The deck should use:

- background images
- dark theme
- sparse visual slides
- clear file-hierarchy visuals

## Planned Execution Order

### Phase 1. Wire The Live Provider

1. finish the executor selection seam
2. add an OpenRouter-backed executor
3. preserve request/response/usage in replay
4. keep deterministic mode working
5. test with one simple non-benchmark prompt first

### Phase 2. Add Depth Cap

Make sure the live path respects:

- max recursion depth `3`

This should be enforced through run-level variables and verified in code.

### Phase 3. Add Test-Question Runner

Build a small runner that can:

- read one grading question file
- extract the runnable question or task text
- launch a live run
- optionally force a baseline configuration

### Phase 4. Choose The 5 Questions

Pick a small set of questions that can realistically succeed with the cheap model and current runtime.

Planned selection strategy:

- avoid giant coding optimization tasks first
- prefer architecture-derived and logic/NLU questions first
- choose a mix that gives:
  - easy single-node wins
  - at least one question that naturally invites decomposition

Tentative pool to choose from:

- `architecture-derived-B7-sarcasm-classification.md`
- `architecture-derived-B11-board-game-rule-chaining.md`
- other short architecture-derived questions with clear binary/exact outcomes

### Phase 5. Run Baselines And Main Runs

For each chosen question:

1. run baseline
2. run normal system mode
3. validate both stored runs
4. record outcome, cost, tokens, and notable behavior

Keep going until:

- `5` main runs succeed
- at least one success is single-node
- at least one success is delegated

### Phase 6. Analyze What Happened

Review the stored runs for:

- which questions stayed single-node
- which questions delegated
- how useful delegation was
- whether outputs were coherent
- whether data storage stayed readable
- whether the timeline/story view remained understandable

### Phase 7. Build The Presentation

Once the live runs are complete:

1. assemble the run results and hierarchies
2. summarize the main architecture
3. summarize the live runs and baselines
4. summarize judgment calls and open questions
5. summarize recommendations
6. build the deck in `presentations/`

## Planned Success Criteria

This next phase is considered successful if:

- the live OpenRouter path works
- deterministic mode still works
- depth cap `3` is enforced
- there are `5` successful live runs
- at least one successful run is single-node
- at least one successful run is delegated
- those runs have baselines
- all stored runs validate
- the results are documented
- the presentation exists and explains both the system and the test outcomes

## Likely Judgment Calls I Expect To Need

These are likely places where implementation judgment will matter:

- what exactly counts as a successful delegated run
- which grading questions are realistic first candidates
- whether decomposition should stay heuristic or be partly model-driven in this phase
- how to choose baselines that are fair without creating a second whole runtime
- how much of multi-step node behavior should stay in replay vs move into core records
- how much grading detail should be reflected in the deck vs the journal docs

## Questions To Revisit After The Runs

These are likely post-run questions to answer once evidence exists:

- when does delegation actually help?
- what kinds of questions should stay single-node?
- is the current action/output model expressive enough?
- is the current run-history layout calm enough at scale?
- should baseline mode become an official runtime option?
- should the grading system store run-to-question links more explicitly?
- should the core node record surface more of the multi-step history?

## Immediate Next Action

The next implementation action after this doc is:

- finish the live OpenRouter executor integration

After that:

- add the test-question runner
- define the baseline mode
- start running the real questions
