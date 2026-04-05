# 🌳 Eywa, Bonsai, and Potter

## Decision

Open-Eywa should be a three-layer tree system:

- **Eywa** runs the task tree.
- **Bonsai** learns how to tune the tree.
- **Potter** changes the code around the tree, but only if dry runs stay identical.

The point of the split is discipline. Eywa stays a stable execution engine, Bonsai learns from the history of runs, and Potter improves the implementation without changing behavior.

## Core Rules

- The node is the durable unit of work.
- Code owns protocol and correctness.
- Models contribute bounded reasoning inside the protocol.
- Simulation comes before live spend.
- Events are raw facts; metrics are views.
- The system must stay inspectable from files on disk.

## Proposed Shape

```text
task
  -> root node
  -> node tree
  -> run history
  -> benchmark registry
  -> Bonsai policy
  -> next task variables

code change
  -> Potter worktree
  -> dry run machine
  -> equivalence check
  -> accepted or rejected refactor
```

## Eywa

Eywa is the execution tree.

It receives a task, chooses a first action, and may solve directly, plan first, split work, or hand off to child nodes. Every node should have the same DNA. The only allowed differences are:

- the instruction packet
- the variable bundle

Everything else should be stable enough that any middle node still looks like the same machine.

### Eywa node contract

Each node should record:

- task text or task reference
- task tags
- parent and child links
- instruction packet
- tree-scoped variables
- node-scoped variables
- raw events
- artifact paths
- usage and cost
- terminal outcome

### Variable families

The variable bundle should be explicit and closed, not ad hoc. A first version can use a small set of families:

- decomposition
- context shaping
- handoff style
- verification strictness
- resource budget
- recovery policy

Tree-scoped variables set the default envelope. Node-scoped variables override only where needed.

## Bonsai

Bonsai is the learning layer around Eywa.

It does not replace the tree. It watches the runs, scores them, and learns which variable bundles work best for which task shapes.

### Bonsai inputs

- run history
- benchmark registry
- task tags
- chosen variables
- scores
- time
- tokens
- cost

### Bonsai outputs

- variable recommendations for a task family
- promoted benchmark tasks
- heuristic rules for first-pass selection
- later, a model that predicts variable bundles from task form

### Bonsai loop

1. Canonicalize the task.
2. Map the task to tags and a compact form.
3. Look up similar past runs and benchmarks.
4. Choose a variable bundle.
5. Run Eywa.
6. Score the result.
7. Feed the new example back into the policy store.

### Benchmark registry

The benchmark registry should be separate from ordinary runs.

It is the set of tasks that are at least partly verifiable and can be used to compare variable bundles over time. This registry should grow from:

- hand-collected tasks
- good real tasks promoted from run history
- tasks with clear scoring rules

Each benchmark row should keep:

- raw task text
- canonical task form
- task tags
- scoring rule
- provenance
- best known variable bundle
- latest scores

## Potter

Potter is the code-shaping layer.

It may refactor, simplify, modularize, or harden the code, but it must not change observable behavior.

### Potter gate

Candidate code changes should be tested against a dry run machine that can reproduce the proper outputs for known situations without depending on live model randomness.

Potter passes only if:

- dry run outputs stay identical
- live run outputs stay equivalent in the expected places
- timing differences stay within tolerance

Anything else is advisory, not a release gate.

### Potter inputs

- a candidate worktree
- the canonical dry run suite
- a set of benchmark scenarios
- code quality checks

### Potter outputs

- accepted refactor
- rejected refactor
- equivalence report
- maintainability notes

## Dry Run Machine

The dry run machine is the truth source that keeps Potter honest.

It should be able to replay important scenarios and generate the expected outputs without calling a live model. That makes it useful for:

- equivalence checks for code changes
- regression detection
- scenario comparison
- future replay-based validation

It does not need to simulate everything perfectly. It does need to be strict about the parts of the system that define correctness.

## Data Flows

### Execution flow

```text
task
  -> canonical task form
  -> variable bundle selection
  -> Eywa node tree
  -> raw run artifacts
  -> scored result
  -> run history
  -> Bonsai policy update
```

### Improvement flow

```text
new run data
  -> benchmark promotion
  -> variable comparison
  -> heuristic update
  -> later model training
```

### Code improvement flow

```text
code change
  -> Potter worktree
  -> dry run suite
  -> equivalence check
  -> keep or reject
```

## Minimum First Implementation Shape

The first stable version should keep the system split into small modules:

- node contract and lifecycle
- run recorder
- benchmark registry
- variable policy store
- canonicalization step
- dry run machine
- Potter evaluator

This keeps future changes local and makes A/B testing easier.

## Open Questions

The proposal is still missing a few decisions:

- Which variable families are truly canonical and closed
- How much task canonicalization should happen before embeddings
- What counts as identical enough for Potter
- When a real task should be promoted into benchmarks
- When Bonsai should use heuristics versus a learned model

## Recommendation

Start with heuristics, data capture, and strict contracts.

That gives Sean a system that can solve tasks now, learn from every run, and improve the implementation later without losing behavioral stability.
