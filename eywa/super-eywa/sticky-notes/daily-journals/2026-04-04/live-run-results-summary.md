# 2026-04-04 Live Run Results Summary

## Purpose

This doc summarizes the first full live grading batch for Super-Eywa v1.

It is the quickest catch-up doc for:

- which questions were run
- baseline vs main behavior
- where delegation actually happened
- which questions graded correct
- what the first recommendations are

## Batch Shape

- model: `openai/gpt-4.1-mini`
- runtime provider: `openrouter`
- baseline mode: `max_depth = 0`
- main mode: `max_depth = 3`
- main run count: `5`
- baseline run count: `5`

## Results

| Question | Baseline | Main | Node Counts | Notes |
| --- | --- | --- | --- | --- |
| `B4` Hensel lifting | incorrect | incorrect | `1 -> 3` | first successful delegated math run; branching worked but answer quality stayed wrong |
| `B5` random chords | incorrect | incorrect | `1 -> 1` | no branching triggered; same wrong answer both times |
| `B6` binary minimization | correct | correct | `1 -> 1` | best clean single-node success |
| `B10` mean-field occupancy | incorrect | incorrect | `1 -> 4` | delegated, but decomposition did not improve answer quality |
| `B11` board-game chaining | correct | correct | `1 -> 5` | delegated cleanly and stayed correct, though the question itself is underspecified |

## Structural Successes

- live OpenRouter execution worked end to end
- stored run validation stayed green on live runs
- baseline and main runs were both stored cleanly
- at least one clean single-node live success exists:
  - `B6`
- at least one clean delegated live success exists:
  - `B11`
- delegated live failures were also informative:
  - `B4`
  - `B10`

## Main Observations

- The live provider seam is now real.
- The current question bank is only partly runnable.
- Delegation currently works structurally better than it works intellectually.
- On this first pass, delegation increased node count and trace richness more than it increased accuracy.
- The best current win surface is still:
  - short exact-answer questions
  - strong explicit answer formatting
  - single-node direct work

## First Recommendations

### System Design

- make runnable question packets richer
- make decomposition decisions more explicit and less heuristic
- add stronger verification for exact-answer questions
- separate synthesis prompts from local-solve prompts more sharply

### Near-Term Practical

- prefer exact-answer numeric/string cases when testing runtime behavior
- keep using the same cheap reliable model for short integration loops
- add a question-level metadata field for:
  - `recommended_baseline_mode`
  - `recommended_main_mode`
  - `recommended_grader`

## Key Paths

- batch summary:
  - `data-system/grading/runs/live-batch-v1-summary.json`
- one clean single-node success:
  - `data-system/grading/runs/architecture-derived-B6-binary-representation-minimization/`
- one clean delegated success:
  - `data-system/grading/runs/architecture-derived-B11-board-game-rule-chaining/`
- first delegated failure worth reviewing:
  - `data-system/grading/runs/architecture-derived-B4-hensel-lifting-verification/`
