# 2026-04-04 Implementation Questions And Judgment Calls

## Purpose

This doc captures the big implementation questions that came up during the autonomous v1 build pass, including the judgment calls made to keep moving.

## Judgment Calls

### 1. V1 Executor Type

Question:

- Should v1 depend on a live model provider from day one?

Decision:

- No.
- Use a deterministic local executor first.

Reason:

- This makes v1 runnable and testable immediately.
- It preserves the provider seam without making the first build depend on secrets or network provider behavior.

### 2. Storage Strategy

Question:

- Should v1 depend on a database first?

Decision:

- No.
- Use file-first canonical truth under `data-system/run-history/`.

Reason:

- This matches the target docs.
- It keeps the first build simple and reconstructable.

### 3. Executor Scope

Question:

- Should v1 try to support live-model execution immediately?

Decision:

- No.
- Preserve the provider seam, but ship a deterministic executor first.

Reason:

- The main v1 goal is strong bones and clean recording.
- A deterministic executor makes testing and smoke-running reliable.

### 4. Multi-Step Root Nodes

Question:

- How should a node that first recruits helpers and later finishes be represented?

Decision:

- Allow the runtime to keep multiple authored steps in replay.
- Preserve only the final readable node record as the canonical calm view.
- Add `final_action_type` to the node record.

Reason:

- This keeps the main node record readable.
- It avoids needing a heavier multi-record node contract immediately.

### 5. Event And Edge Placement

Question:

- Should events and edges be stored centrally or next to each node?

Decision:

- Use both:
  - a central run event log
  - node-local `events.jsonl` and `edges.json`

Reason:

- The run timeline is easier to derive from a central log.
- Node-local logs keep each node self-explanatory.

### 6. First Correctness Step

Question:

- What is the smallest honest correctness-suite implementation for v1?

Decision:

- Start with stored-run validation, not dry-run execution.

Reason:

- The runtime already needed a way to prove that what it wrote matches the contracts and layout.
- This creates a real correctness foothold without pretending dry-run machinery already exists.

### 7. Secret Loading Source

Question:

- Where should Super-Eywa load the OpenRouter key from if Sean already has working live keys in `open-eywa`?

Decision:

- Prefer:
  - process environment
  - local `.env`
  - sibling `../open-eywa/.env`
  - keychain

Reason:

- Sean explicitly said the keys already live in `open-eywa`.
- Reusing the working credential source was lower risk than inventing a new secret setup first.

### 8. Usage Accounting Source

Question:

- How should usage from chat completions and generation stats be combined?

Decision:

- Do not sum them.
- Prefer non-zero generation stats fields when present, while preserving response metadata from both sources.

Reason:

- Both payloads can describe the same request.
- Summing them would inflate cost and token totals.

### 9. Depth Control

Question:

- How should the requested depth cap of `3` be enforced?

Decision:

- Enforce it in code with a hard runtime cap of `3`, not just by convention in variables.

Reason:

- Sean explicitly wanted a hard stop against runaway branching.
- This belongs on the code-owned side of correctness.

### 10. Runnable Question Gap

Question:

- Are the current grading-bank question files fully runnable as-is?

Decision:

- No.
- Treat them as summary-style question packets for now.
- Build a thin runner that composes a runnable prompt from:
  - title
  - question/task section
  - grading section

Reason:

- The grading bank already had enough information to support a first live pass.
- Waiting for a richer question schema would have blocked the requested testing phase.

### 11. First Grading Scope

Question:

- Should the first grader try to support the whole bank?

Decision:

- No.
- Support a small explicit subset first with simple exact/tolerance graders.

Reason:

- The immediate need was to run a real batch and compare baseline vs main.
- A narrow honest grader is better than a fake universal grader.

### 12. Decomposition Ownership

Question:

- Should live decomposition already be model-decided?

Decision:

- Not yet.
- Keep decomposition as code-owned heuristic behavior for this pass.

Reason:

- This keeps branching predictable while the live provider seam and storage are still settling.
- It also makes baseline vs main comparisons easier to interpret.

## Open Implementation Questions

- The current live executor only uses the model for local work and synthesis, not for decomposition decisions.
- The grading-bank question files should eventually become richer runnable packets rather than summary-style markdown cases.
- The exact long-term shape of multi-step node histories may eventually need a more formal contract.
- The current correctness validator still checks structure and contract validity, not semantic correctness.
- The first simple grader supports only a small subset of questions.
- We still need to decide whether delegation should be driven by:
  - prompting
  - explicit variables
  - model judgment
  - or a mix
