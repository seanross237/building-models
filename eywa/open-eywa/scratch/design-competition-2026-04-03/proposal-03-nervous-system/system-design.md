# Open-Eywa Nervous System Proposal

## Target state

One system with three layers:

- `Eywa` executes tasks as a node tree.
- `Bonsai` learns which variables make Eywa better on which task shapes.
- `Potter` improves the code while a dry-run oracle prevents behavior drift.

The important constraint is that all three layers share the same trace language. If a run cannot be described as a task, a node, a variable set, and a result packet, it is not yet in the system.

## Proposed structure

```
task
  -> Eywa node tree
  -> trace packets + run history
  -> Bonsai selector and benchmark bank
  -> variable policy updates

code change
  -> Potter worktree
  -> dry-run machine
  -> exact-output check
  -> accept or reject
```

## Eywa

Eywa is the runtime. It takes a task, decides whether to solve it directly or split it, and records everything that happens.

### Node contract

Every node should share the same DNA. The only allowed differences are:

- the instruction bundle the node receives
- the parameter variables passed into the node

Proposed node inputs:

- `task_id`
- `task_text`
- `parent_state`
- `instruction_bundle`
- `tree_vars`
- `node_vars`
- `context_slice`

Proposed node outputs:

- `action_taken`
- `child_nodes`
- `final_answer` if the node resolves the task
- `trace_packet`

Allowed node actions:

- solve directly
- make a plan and solve
- make a plan and delegate to another agent
- make a plan and split into multiple agents

### Trace packet

Each node should emit a canonical packet with at least:

- node id and parent id
- task id
- instruction hash
- variable values
- inputs used
- outputs produced
- tools called
- token count
- elapsed time
- cost
- score or downstream reward when available

This packet is the nerve impulse. Bonsai learns from it. Potter uses it for replay and dry-run checks.

## Bonsai

Bonsai is the control plane around Eywa. It does not execute the task tree itself. It learns which variable settings improve performance for which kinds of tasks.

### Inputs

- runs history
- benchmark database
- task tags or embeddings
- node-level and tree-level variable settings
- scores, cost, time, and agent usage

### Proposed learning loop

1. Normalize the task into a compact representation.
2. Retrieve similar tasks from the benchmark bank and run history.
3. Start with heuristics for variable choice.
4. Learn a variable policy model once the dataset is clean enough.
5. Promote strong verifiable runs into the benchmark bank.

### Starter variable families

These are the first variables that should be versioned and compared across runs:

- tree depth limit
- fan-out limit
- budget cap
- delegation threshold
- verification strictness
- context compression style
- tool access policy
- reflection count

### Bonsai outputs

- recommended tree vars
- recommended node vars
- benchmark promotion candidates
- performance summaries by task family

## Potter

Potter is the code optimizer. Its job is to make Eywa and Bonsai simpler, more modular, more flexible, and more robust without changing the behavior of validated runs.

### Safety rule

A Potter change is only acceptable if the dry-run machine produces identical outputs for all validated cases. Execution time may differ slightly. The behavior must not.

### Potter workflow

1. Create a candidate worktree.
2. Run the dry-run machine against the benchmark corpus.
3. Compare candidate output to the reference output.
4. Reject any semantic drift.
5. If the outputs match, evaluate code quality dimensions such as modularity, simplicity, and intuitiveness.

### Potter outputs

- accepted code change or rejection
- dry-run diff report
- implementation quality notes
- follow-up refactor candidates

## Shared data model

The system should keep the following records distinct and versioned:

- `task`
- `task_tags`
- `node`
- `tree_vars`
- `node_vars`
- `trace_packet`
- `run_record`
- `benchmark_case`
- `dry_run_signature`
- `code_revision`

## Main data flow

### Runtime flow

Task enters the root node. The node picks an action. That action may split into children. Every child writes a trace packet. Those packets become run history. Verifiable runs may graduate into the benchmark bank.

### Learning flow

Benchmark cases and run history feed Bonsai. Bonsai looks for patterns in task shape and variable performance. It returns better variable defaults for new tasks.

### Change-control flow

Potter edits the code in a worktree, replays the benchmark corpus, and only passes changes that preserve the validated outputs.

## Open questions

- Which variables belong at the tree level and which belong at the node level?
- What is the minimum benchmark taxonomy that still predicts variable choice well?
- What must the dry-run machine fully simulate before Potter can be trusted?
- What is the promotion rule for moving a run from history into the benchmark bank?

## Decision to carry forward

Freeze the trace packet and variable schema first. After that, Eywa can run, Bonsai can learn, and Potter can improve the implementation without breaking the contract.
