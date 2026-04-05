# 🌳 Open Eywa Factory Proposal

## Decision

Build one shared runtime with three layers:

- Eywa runs tasks as node trees and records every run.
- Bonsai learns which variables work best for which tasks.
- Potter changes the code only when dry-run behavior stays identical.

The core rule is simple: every node has the same DNA. A node may differ only in its instructions and the parameter variables passed into it.

## System Shape

```text
Task -> fingerprint -> Eywa root node -> child nodes -> run record
                              \-> Bonsai selector -> better variables
                              \-> Potter worktree -> dry-run gate -> merge
```

## Eywa

Eywa is the execution machine.

- Input: a task, plus any root-level constraints and goal framing.
- Behavior: decide whether to solve, plan, delegate, or split.
- Output: a tree of node runs, plus a complete record of what happened.
- Invariant: any node taken from the middle of a tree should still look and behave like the same machine.

### Candidate node variables

These are the knobs Eywa should expose and log cleanly:

- `decomposition_mode`
- `branch_factor`
- `tool_budget`
- `reflection_budget`
- `context_compression`
- `handoff_policy`
- `retry_timeout`

The point is to keep the bones stable and move the adaptation into named variables.

## Bonsai

Bonsai is the optimizer around Eywa.

- Input: runs_history, benchmark cases, task fingerprints, node variables, scores.
- Behavior: find similar tasks, compare outcomes, and recommend better variable sets.
- Output: a chosen variable set for the next task or node.

### Task fingerprint

Use a small set of stable task tags so similar tasks can be matched quickly. A good starting set is:

1. `domain`
2. `task_shape`
3. `verification_mode`
4. `ambiguity_level`
5. `decomposition_need`

These tags should be recorded for every task and used for retrieval before the system gets fancy.

## Potter

Potter is the refactor system.

- Input: source code, a worktree, the dry-run suite, and benchmark replay.
- Behavior: propose implementation changes that improve clarity, modularity, flexibility, or robustness.
- Output: a candidate refactor, plus proof that behavior did not change.
- Gate: if the dry run changes the observable result, the refactor is rejected.

Potter is not trying to make Eywa score better. Potter is trying to make the code easier to evolve without changing what the machine does.

## Contracts

| Artifact | Must contain | Why it matters |
| --- | --- | --- |
| `TaskSpec` | raw task, normalized task, task tags, constraints, provenance | Makes tasks searchable and comparable |
| `NodeSpec` | node id, parent id, depth, instruction pack, variable set, handoff mode | Defines the exact shape of one node |
| `RunRecord` | run id, task id, node id, prompt ref, model, tools, output ref, score, token use, cost, time | Makes every run learnable |
| `BenchmarkCase` | benchmark id, gold output, scoring rule, validation mode, stability flag | Keeps the benchmark yard clean |
| `DryRunCase` | input snapshot, expected control flow, expected artifact hash, expected score | Gives Potter a hard equivalence test |

### Variable set boundary

Only two things should vary between nodes:

- the instructions passed into the node
- the parameter variables attached to the node

Everything else should be part of the shared chassis.

## Data Flow

1. A task enters and gets normalized into `TaskSpec`.
2. Bonsai fingerprints the task and retrieves similar runs and benchmarks.
3. Eywa starts at the root node and emits child nodes when the task needs decomposition.
4. Each node writes a `RunRecord`, including the variables that shaped the run.
5. Verifiable runs can be promoted into `BenchmarkCase`.
6. Bonsai learns from the scored history and updates its variable recommendations.
7. Potter proposes code changes in a separate worktree and runs dry checks.
8. If dry-run output stays identical, Potter can promote the refactor.

## Promotion Rules

Only promote a run into the benchmark yard if all of these are true:

- the task is verifiable
- the scoring rule is clear
- the task tags are complete
- the result is stable enough to reuse later

That keeps the benchmark database from becoming noisy.

## Open Questions

- What is the canonical list of task tags?
- Where exactly is the line between tree-level variables and node-level variables?
- Should dry-run equivalence be structural, byte-level, or both?
- Which metrics decide whether Potter made the code better after equivalence passes?
- What is the fastest path from a new run to a useful benchmark case?

## Short Version

Eywa executes. Bonsai learns. Potter refactors. The whole system works only if the data contract stays tight and the dry-run machine can prove that implementation changes did not change behavior.
