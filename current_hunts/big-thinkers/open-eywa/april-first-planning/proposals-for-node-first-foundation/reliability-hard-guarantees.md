# Node-First Core For Open-Eywa

## Summary

Open-Eywa should be stable at the node level, flexible at the agent level, and hard at the protocol level. The simplest strong core is a system where each node is a durable unit of work, state, artifacts, and inspection, while agents are ephemeral contributors that can change over time without changing the meaning of the node itself.

The foundation should be simple enough to reason about, strict enough to survive messy model behavior, and explicit enough to support future A/B testing without breaking downstream assumptions.

## What A Node Is

A node is the stable container for a single unit of work.

It is the thing that persists on disk, carries state forward, and gives humans a readable place to inspect what happened. A node is not “one agent”; it is the durable record of work that may be touched by multiple agents over time.

If a later design wants multiple agents, retries, repair passes, or specialized contributors, the node still remains the same unit of truth.

## What A Node Owns

A node owns:

- its current status
- its goal or task description
- its input files
- its output files
- its orchestrator-facing control files
- its logs, usage, and artifacts
- its child nodes, if any
- its history of what happened

The most important thing is that the node owns the truth of the work. Agents may help create that truth, but the node is where it lives.

## What An Agent Run Is

An agent run is a temporary contributor acting inside a node.

It reads the node’s instructions, uses only the tools allowed to it, writes files into the node, and exits. The agent run is not the durable entity. It is only a bounded execution of judgment or action inside the node’s contract.

That distinction matters because the system should remain correct even if an individual agent is inconsistent, incomplete, or strange.

## Minimal Node State Model

The minimal node model should be as small as possible while still being explicit.

At minimum, a node needs:

- a current status
- a role or mode for the next agent run
- a goal or parent instruction
- an output space
- a control space for orchestrator decisions

The state model should not depend on agent memory. Any important state should be serializable on disk so it can be replayed, inspected, and recovered.

If a node-only design and a node-plus-workflow design differ here, the node-first version should prefer simple explicit state over a larger workflow abstraction unless the extra abstraction clearly reduces ambiguity.

## Core Files That Define Truth

The files that should define truth are the ones a human or orchestrator can inspect directly.

Core truth files:

- `input/goal.md`
- `input/parent-instructions.md`
- `input/retrieved_relevant_knowledge_from_library.md`
- `output/plan.md`
- `output/review.md`
- `output/final-output.md`
- `output/state.md`
- `output/escalation.md`
- `for-orchestrator/agent-mode`
- `for-orchestrator/this-nodes-current-status`
- `for-orchestrator/eval-decision`

The key principle is that a node is complete because the right files exist with the right meaning, not because a process ended or a model said it was done.

## Completion, Failure, Escalation

Completion should mean:

- the required artifact exists
- the required status transition is valid
- no stale decision file is misleading the orchestrator
- the node has satisfied its contract

Failure should mean:

- the required artifact never appeared
- the agent behavior was malformed or unusable
- the orchestrator could not recover safely

Escalation should mean:

- the current node cannot safely continue under its own contract
- the issue should be handed upward explicitly
- the node should not pretend success

This is one of the strongest places to keep hard logic in code. Completion should never be inferred from model confidence or finish reason alone.

## What Must Be Hard In Code

The hardest guarantees should be owned by code, not prompts.

That includes:

- legal node state transitions
- required output validation
- spawn and respawn rules
- stale-file cleanup
- tool boundaries
- path restrictions
- completion checks
- failure detection
- usage and cost tracking
- duplicate-run prevention

If a model misbehaves, the system should remain safe and inspectable.

## What Can Stay Soft In Model Behavior

Models can stay soft on:

- wording
- synthesis style
- planning style
- explanatory detail
- local reasoning strategy

Those are important for quality, but they should not control protocol correctness.

## Extensibility For New Agent Types

The node-first core should make it easy to add new agent types later without changing the meaning of a node.

That means:

- new agents should be able to run inside the same node contract
- agent types should be swappable
- agent capabilities should be explicit and narrow
- node truth should stay stable even if the agent mix changes

This is where node-first helps the most. If new agents arrive later, the node still remains the same durable work container.

## Future A/B Testability

This design should support future A/B testing by keeping the node contract stable and making agent behavior modular.

That means we should be able to vary:

- agent type
- prompt variant
- tool profile
- context shape
- retry policy
- recovery behavior

without changing the meaning of the node itself.

To support that, the system should log enough detail that runs can be compared cleanly across experiments.

## Biggest Risks

The biggest risks in a node-first design are:

- smearing process logic across too many ad hoc status checks
- letting prompts define protocol instead of code
- making the node too large and overloaded
- relying on agent consistency for correctness
- allowing stale files to drive fresh transitions
- hiding too much behavior inside runtime magic

The answer to those risks is not to abandon node-first. It is to keep the node contract narrow, explicit, and hard.

## Conclusion

The simplest strong node-first core is a durable node that owns truth, a small number of explicit statuses and files, and ephemeral agent runs that operate inside strict contracts. That gives Open-Eywa a stable base for reliability, human inspection, future agent growth, and clean A/B testing without letting the architecture drift into fragile workflow magic.
