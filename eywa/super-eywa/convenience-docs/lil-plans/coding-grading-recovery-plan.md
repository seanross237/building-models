# Coding Grading Recovery Plan

## Goal

Make coding benchmarks fairer by separating:
- actual task performance
- submission-contract compliance

So a model can still earn a real task score if it produced usable code, even if it failed the exact JSON/artifact contract.

## Core Principle

For coding tasks:
- score correctness from the best recoverable runnable submission
- track compliance separately
- only hard-fail when no single safe runnable submission can be recovered

## V1 Output Model

Each coding grading row should carry:
- `task_score`
- `task_correct` when binary
- `submission_compliance`
- `recovery_used`
- `submission_source`
- `recovery_notes`

The main `grading.score` should represent task score, not contract purity.

## Recovery Layer

Before coding grading:
1. look for the normal attached `main.py` artifact
2. if missing, try to recover one submission from:
   - `artifacts`-like JSON in raw text
   - fenced code block
   - plain code-looking body
3. if exactly one confident runnable submission is found, use it
4. if multiple plausible submissions or unclear code are found, hard-fail

## Compliance Levels

Suggested values:
- `clean`
- `recovered_from_response`
- `recovered_from_fenced_code`
- `recovered_from_plain_text`
- `missing_submission`
- `ambiguous_submission`

## Hard-Fail Conditions

Hard-fail only when:
- no runnable code can be recovered
- multiple candidate submissions are present
- required files are missing and cannot be inferred safely
- interactive protocol is too malformed to run

## Scorer Behavior

Official tools should distinguish:
- invalid candidate output
- tool failure

A bad candidate output should usually score `0`, not become a harness error.

## Build Order

1. Add submission recovery helper for coding runs
2. Split coding grading into task score vs compliance score
3. Thread recovery/compliance fields into grading rows and traces
4. Soften official-tool parse failures into normal wrong-output cases where appropriate
5. Add tests for:
   - clean artifact submission
   - fenced-code recovery
   - plain-text recovery
   - ambiguous submission hard-fail
6. Rerun `coding-S1` and `coding-S5` baseline comparisons

## First Validation Target

Use:
- `coding-S1` to test soft handling of malformed candidate output
- `coding-S5` to test a cleaner continuous-score baseline comparison
