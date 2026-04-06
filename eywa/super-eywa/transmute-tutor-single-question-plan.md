# Transmute Tutor Single-Question Plan

## Goal

Build a controlled prompt-iteration loop for Super-Eywa where:

1. Gemma 4 runs one grading-bank question.
2. The run is graded automatically.
3. A separate manual "tutor" step reviews the graded run and recommends a better transmutation prompt.
4. We run the new prompt again on the same question.
5. We repeat this for 10 iterations.

The optimization target is:

- improve correctness / score first
- reduce total tokens
- reduce total wall-clock time

## Current State

These parts already exist:

- Gemma 4 is already the default model in `eywa-system/variables/default-run-level-variables.json`.
- Prompt families already exist: `none`, `execute`, `transmute`, `delegate`, `agent_chooses`.
- We can already force `root transmute -> child execute`.
- Grading already runs automatically after each benchmark run.
- Supabase sync already exists for `benchmark_questions`, `graded_runs`, `experiment_runs`, and `experiment_run_cases`.

These parts are wrong for the new workflow:

- `run_test_question_v1.py` still auto-runs the reviewer.
- grading records currently mix grading and review too early.
- the current reviewer is too general; the new tutor should focus on transmutation-prompt improvement.
- `graded_runs` currently does not carry all the optimization metrics we care about, especially total tokens and total wall time.

## Scope Decisions

For this phase, we will keep the system narrow and controlled.

- One question only.
- One model only: Gemma 4.
- One orchestration pattern only: `transmute` at root, then `execute_locally` in the child.
- The transmutation prompt is the only prompt we optimize.
- The execute node gets no behavioral coaching beyond minimal output-shape scaffolding.
- The fixed JSON protocol layer stays in place.
- The tutor stays outside the Eywa node graph.
- The tutor does not run automatically.
- We do not add a separate Supabase table for tutor outputs.

## Initial Question Choice

We do not need to discover a failure from scratch. We already have machine-scored Gemma failures on auto-graded questions:

- `architecture-derived-B4-hensel-lifting-verification`
- `architecture-derived-B5-combinatorial-probability-random-chords`
- `architecture-derived-B6-binary-representation-minimization`
- `architecture-derived-B10-mean-field-lattice-gas-occupancy`

Recommended starter question:

- `architecture-derived-B6-binary-representation-minimization`

Why:

- exact numeric grading
- already fails under Gemma baseline
- short enough to iterate quickly
- token and time savings will be easier to see than on a much larger task

Before the loop starts, we should run one fresh baseline execute-only confirmation on the chosen question and store it as iteration `00`.

## Desired Runtime Shape

For each experiment iteration after baseline:

1. Root node uses prompt family `transmute`.
2. Root selected prompt text is the current candidate transmutation prompt.
3. Root returns `orchestration_decision = "transmute"` with `message_for_next_agent`.
4. Child node uses prompt family `execute`.
5. Child execute prompt is minimal and only enforces the required JSON/answer shape.
6. Parent review turn uses `execute` behavior to finalize from the child result.
7. Automatic grader scores the run.
8. Manual tutor reads:
   - the grading record
   - the run artifacts
   - the exact transmutation prompt used
   - prior prompt attempts on this same question
   - metrics from earlier attempts
9. Tutor recommends the next transmutation prompt.
10. The next iteration runs with that new prompt.

## Prompt Setup

### Root transmutation prompt

Initial prompt text:

`Try to simplify this question down to its core parts, to help the next agent solve it. Your output should be sufficient for another agent to get, and then produce the final answer.`

This will still be wrapped in the existing transmute-family JSON return instructions.

### Execute prompt

The child execute prompt should be minimal.

It should only:

- preserve the question objective
- preserve any answer-format requirements already present
- require the expected JSON shape

No extra reasoning advice should be added for the child in this phase.

### Base header

Keep `base_header_prompt = ""`.

Note:

- the runtime still has the fixed JSON protocol header
- that is acceptable for this experiment
- "no extra prompt" here means no extra behavioral coaching beyond the protocol/output-shape rules

## Data Model Changes

### 1. Separate grading from tutor output

After this change:

- the grading step always writes a grading record
- tutor output is optional and manual

Target local files:

- grading record:
  - `data-system/grading/runs/<question_id>/<label>__<run_id>.json`
- tutor record:
  - `data-system/grading/tutoring/<question_id>/<label>__<run_id>.json`

The grading record should no longer require tutor data to exist.

### 2. Add run metrics needed for optimization

Each grading record should include metrics copied from `run_summary.json`:

- `total_tokens`
- `total_wall_time_ms`
- `total_cost_usd`

These are needed because the tutor is optimizing for:

- score / correctness
- token usage
- time

### 3. Keep tutor separate in storage, but linkable

The grading record may optionally include:

- `tutor_record_path`

But the main grading step should not create it automatically.

If a tutor run happens later, we can either:

- update the grading record with `tutor_record_path` and embedded tutor summary
- or leave the grading record untouched and keep the tutor linkage in a higher-level loop manifest

The cleaner v1 is:

- grading record remains primary truth for the run
- tutor sidecar exists separately
- loop summary links both

## Supabase Plan

We do not add a separate tutor table.

### Required Supabase changes

Add these columns to `graded_runs`:

- `total_tokens`
- `total_wall_time_ms`
- `total_cost_usd`
- optional `tutor_record_path`

Keep:

- `review` jsonb as the place where optional tutor output can be mirrored when we choose to sync it

That keeps the database shape compatible with the current no-extra-table rule.

### Sync behavior

Automatic grading sync:

- always sync the grading record to Supabase after the run

Manual tutor sync:

- only when the tutor command is run
- sync the tutor result by updating the matching `graded_runs` row
- do not create any new table

## Tutor Responsibilities

The tutor is not a grader.

The grader decides:

- correctness
- score
- expected answer comparison

The tutor decides:

- what likely went wrong
- what the current transmutation prompt did well
- how to change the transmutation prompt next

### Tutor input

For each tutoring step, the tutor should see:

- question id and question file
- current transmutation prompt
- grading result
- total tokens
- total wall time
- root variables
- root orchestration
- root and child outputs
- prior prompt attempts on this question
- prior metrics and outcomes on this question

### Tutor output

The tutor should return structured JSON like:

```json
{
  "question_id": "architecture-derived-B6-binary-representation-minimization",
  "run_id": "....",
  "iteration_index": 3,
  "current_transmutation_prompt": "....",
  "assessment": {
    "score_direction": "worse | same | better",
    "token_direction": "worse | same | better",
    "time_direction": "worse | same | better",
    "summary": "string"
  },
  "what_helped": [
    "string"
  ],
  "what_hurt": [
    "string"
  ],
  "recommendation": {
    "action": "keep | adjust | pivot",
    "reason": "string",
    "new_transmutation_prompt": "string"
  },
  "history_observations": [
    "string"
  ],
  "confidence": "low | medium | high"
}
```

This is intentionally narrower than the old reviewer schema. It is prompt-optimization specific.

## Loop Manifest

Create one experiment manifest for the 10-iteration run on one question.

Suggested path:

- `data-system/grading/tutor-loops/<question_id>/<loop_id>.json`

This manifest should track:

- question id
- chosen model
- baseline iteration
- iteration count
- all transmutation prompts tried
- grading outcome per iteration
- token/time metrics per iteration
- tutor record path per iteration
- which iteration produced the best score

This file becomes the single source of truth for the prompt-search loop.

## Commands To Build

### 1. Run and grade one question

Create or adapt a command that:

- runs one question
- grades it automatically
- does not tutor automatically
- can force the prompt-family configuration for this experiment

Example target behavior:

- baseline mode: execute only
- loop mode: root transmute, child execute

### 2. Manual tutor command

Create a separate tutor command that:

- takes one grading record path or one loop id + iteration
- loads prior attempts on the same question
- produces one tutor JSON
- optionally syncs that tutor output into Supabase by updating `graded_runs.review`

### 3. Ten-iteration loop driver

Create a loop runner that:

1. picks the chosen question
2. runs baseline execute-only confirmation as iteration `00`
3. runs transmute iteration `01` with the starter prompt
4. stops and waits for tutor output
5. uses tutor's recommended prompt for iteration `02`
6. repeats until iteration `10`

Because tutor is manual for now, this driver should support a stepwise mode rather than assuming full unattended automation.

## Build Sequence

### Phase 1. Decouple grader from tutor

- remove automatic tutor execution from `run_test_question_v1.py`
- keep grading automatic
- make tutor a separate command/module
- ensure Supabase sync for grading still works without tutor output

### Phase 2. Add missing metrics

- copy run summary metrics into grading records
- extend Supabase schema and sync code for those metrics

### Phase 3. Add single-question loop manifest

- create a persistent manifest for one-question iterative transmutation experiments
- store prompt text, metrics, and record paths per iteration

### Phase 4. Build manual tutor

- rename conceptually from reviewer to tutor
- narrow its prompt and JSON schema around transmutation-prompt optimization
- give it prior-attempt history on the same question

### Phase 5. Build the loop driver

- baseline confirm
- iteration `01` starter transmutation prompt
- 10 total transmute iterations
- manual tutor handoff between iterations

### Phase 6. Run the first real loop

- start with `B6`
- run baseline confirm
- run iteration `01`
- tutor it
- continue through iteration `10`

## Acceptance Criteria

The plan is complete when all of the following are true:

- a question can be run and graded without automatically producing tutor output
- tutor output can be generated later as a separate step
- the chosen question has one baseline failure record under Gemma 4
- each transmute iteration stores:
  - exact transmutation prompt
  - grading result
  - total tokens
  - total wall time
  - total cost
  - tutor recommendation
- tutor can see all prior attempts on the same question
- tutor recommends a next transmutation prompt focused only on improving the transmutation layer
- Supabase receives grading rows automatically
- Supabase can optionally receive tutor data by updating the same run row
- the 10-iteration loop can be reconstructed from local files alone

## Immediate First Implementation Step

The first code change should be:

- split `run_test_question_v1.py` so grading is automatic but tutor is not

That is the boundary change that makes the rest of the loop sane.
