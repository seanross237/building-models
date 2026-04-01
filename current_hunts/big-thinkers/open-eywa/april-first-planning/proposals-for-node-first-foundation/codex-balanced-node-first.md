# Balanced Node-First Core For Open-Eywa

## Summary

Open-Eywa should be node-first at the foundation, agent-flexible above that, and hard at the protocol layer. The node should be the durable unit of truth, inspection, measurement, and recovery, while agent runs remain temporary contributors that can be swapped, split, added, or removed without changing what a node fundamentally means.

The goal is not to make nodes do everything. The goal is to make the node the stable place where correctness lives. That gives us a simpler foundation for reliability, future extensibility, and future A/B testability.

## What A Node Is

A node is a bounded unit of work with a durable on-disk contract.

It is the smallest unit that should be:

- inspectable by a human
- validated by code
- measured across runs
- replayable after failure
- stable even as agents and models change

A node should not mean "one agent" or "one fixed recipe." It should mean "one persistent work container whose truth can be checked on disk."

## What A Node Owns

A node should own:

- its task or goal
- its current status
- its artifact contract
- its readable inputs
- its readable outputs
- its orchestrator control files
- its logs and usage records
- its child relationships
- its execution history on disk

The key principle is that a node owns truth, not the agent. Agents help produce truth, but the node is where truth is stored, checked, and compared.

## What An Agent Run Is

An agent run is a temporary attempt to advance a node.

It should:

- read prepared node context
- use only allowed tools
- write only allowed artifacts
- leave behind logs and outputs
- exit cleanly or fail explicitly

An agent run should never be treated as the durable carrier of meaning. It is disposable. The node is not.

## Minimal Node State Model

The node state model should stay as small as possible while still making control explicit.

At minimum, a node needs:

- a current status
- a next mode or next role hint
- a task or goal
- a contract for required artifacts
- a control area for orchestrator decisions

The specific status list can evolve, but the model should remain simple enough that a human can inspect the node and understand where it is in the lifecycle.

If node-only and node-plus-workflow would differ here, the node-only version should win unless adding another abstraction clearly removes ambiguity rather than just moving it around.

## Core Truth Files

The truth of a node should be defined by stable, inspectable files.

Core truth files should include:

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

If a file matters for correctness, completion, or orchestration, code should treat it as part of the contract and tests should cover it.

## Completion, Failure, And Escalation

Completion should mean:

- the node satisfied its artifact contract
- the required files exist
- the orchestrator can validate them

Failure should mean:

- the node could not satisfy the contract safely
- retry or recovery rules were exhausted
- the node remains inspectable after the failure

Escalation should mean:

- the node cannot safely continue under its current assumptions
- a higher-level decision is required

The system should never confuse process exit with success. A node is done because its contract is satisfied on disk.

## Hard In Code, Soft In Model Behavior

The hard layer in code should own:

- valid state transitions
- required artifacts
- completion checks
- escalation semantics
- path and tool boundaries
- duplicate-run prevention
- retry limits
- logging and metrics schemas
- measurement hooks for future experiments

The soft layer can remain in model behavior:

- how a plan is phrased
- how a synthesis is worded
- how reasoning is expressed
- how a bounded task is carried out within the allowed contract

This preserves flexibility without outsourcing correctness.

## Extensibility

This design stays extensible because new agent types do not change what a node is.

New things can be added as:

- new roles
- new tool profiles
- new verification passes
- new repair passes
- new review patterns
- new experiment variants

But the node remains the same stable comparison boundary.

That is important because we expect:

- future agent growth
- future architectural tweaks
- many A/B tests
- many instrumentation changes

If the node contract stays fixed, those changes can happen around the edges without forcing structural rewrites.

## A/B Testability

Node-first is a good foundation for experiments because the node gives us a stable unit to compare across variants.

For a future A/B test, we should be able to ask:

- did the same kind of node complete more often
- with what cost
- in what time
- with what outputs
- with what failure modes

That becomes much easier if the node remains the invariant and the variable parts are things like:

- which agent type ran
- which prompt variant was used
- which tool policy was used
- which routing rule was used

The experiment boundary should be the node, not the raw agent run.

## Main Risks

The main risks in a node-first design are:

- burying too much process logic in scattered conventions
- letting the status model grow into a messy pseudo-workflow
- making node contracts too role-specific
- letting measurement hooks become inconsistent across node types

So the discipline we need is:

- keep the node contract small and explicit
- keep protocol hard
- let variation happen in agent behavior and configuration, not in the meaning of the node itself

## Conclusion

The strongest simple foundation for Open-Eywa is a balanced node-first core: the node is the stable unit of truth, while agents are replaceable contributors acting inside that boundary. That gives us the best base for reliability, inspectability, future extensibility, and future experimentation without prematurely adding a heavier abstraction layer.
