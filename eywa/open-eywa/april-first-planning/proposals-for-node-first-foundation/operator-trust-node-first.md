# Node-First Foundation for Open-Eywa

## What A Node Is

A node is the stable unit of work, state, and inspection in Open-Eywa. It is the place where a human should be able to open a folder and understand what happened, what is happening, and what happened next. Nodes outlast any one agent, model, or prompt.

## What A Node Owns

A node owns its goal, its state, its outputs, its history, and the artifacts that explain how it got there. In practice, that means the node is the durable record of truth for a single piece of work, with human-readable files standing in for hidden memory.

## What An Agent Run Is

An agent run is a temporary contributor to a node. It reads the node’s files, does one bounded piece of reasoning or execution, writes back the required artifacts, and exits. If more work is needed later, the node can spawn a fresh run without losing its own continuity.

## Minimal State Model

The smallest useful node state model should be simple enough to inspect by eye:

- `pending`
- `retrieving`
- `running`
- `executing`
- `evaluating`
- `complete`
- `escalated`
- `failed`
- `cancelled`

The important thing is not the exact vocabulary, but that every transition is explicit and visible on disk.

## Core Truth Files

The core files that define truth should be:

- `input/goal.md`
- `input/parent-instructions.md`
- `input/retrieved_relevant_knowledge_from_library.md`
- `output/plan.md`
- `output/review.md`
- `output/final-output.md`
- `output/state.md`
- `output/escalation.md`
- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/eval-decision`

If a file matters for correctness, the code should treat it as part of the contract and not as optional prose.

## Completion, Failure, And Escalation

Completion should mean the node has produced the required artifacts for its current role and those artifacts are internally consistent. Failure should mean the node could not complete safely or correctly within the allowed rules. Escalation should mean the node needs a higher-level decision or a different path, not that it vaguely ran out of steam.

The key operator-trust rule is that process exit is never enough by itself. A node is done because the right files exist and the state machine says it is done.

## Hard In Code, Soft In Model Behavior

The hard parts should be in code:

- valid state transitions
- file boundaries
- required outputs
- completion checks
- timeouts and retries
- logging and metrics
- duplicate-run prevention

The soft parts can stay in the model:

- how a plan is phrased
- how a review is worded
- how a final note is written
- how a reasoning step is explained

That keeps the system trustworthy without making it rigid or ugly.

## Extensibility

This node-first model stays extensible because new agent types do not change what a node is. They just become new ways to act on a node. A future agent can be a verifier, a math checker, a repair agent, a specialist reviewer, or a multi-pass collaborator, and the node still remains the stable place where the truth lives.

This is where I would briefly flag the workflow question: if later we need reusable process recipes, those can be added as a layer above nodes without changing the basic node contract.

## Future A/B Testability

The node-first design should make A/B tests easy because each node can capture comparable inputs, outputs, timings, costs, and transitions. That means we can swap agent models, prompts, or tool profiles while keeping the node contract fixed and measuring differences cleanly.

To support this well, the node should record enough structured data that runs can be compared without manual reconstruction.

## Biggest Risks

The main risk in a node-first system is hiding too much process logic inside ad hoc status changes and per-role conventions. If that happens, the node stays visible but the behavior becomes hard to reason about. Another risk is overloading the node with too many responsibilities, which can make it feel simple at first and messy later.

The antidote is to keep the node contract narrow, the files explicit, and the hard rules enforced in code.
