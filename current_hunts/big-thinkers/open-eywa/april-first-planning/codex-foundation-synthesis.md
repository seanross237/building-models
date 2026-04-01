# Codex Foundation Synthesis

## Purpose

This document records my read of the node-first foundation proposals and gives a final recommended direction for Open-Eywa.

## Which Proposal Is Strongest

The strongest single proposal is:

- `proposals-for-node-first-foundation/codex-balanced-node-first.md`

Why it is strongest:

- it keeps the node clearly central without making the node vague
- it defines the node as a durable on-disk contract, not just a folder
- it balances reliability, inspectability, extensibility, and A/B testability well
- it explicitly treats the node as the comparison boundary for future experiments
- it acknowledges the workflow question without prematurely introducing more abstraction

If I had to pick one draft to build from directly, that would be the one.

## What The Other Proposals Add

### From `reliability-hard-guarantees.md`

This proposal is the strongest on hard guarantees.

What I want to carry forward from it:

- strong language around code owning protocol
- explicit rejection of process exit as success
- emphasis on stale-file cleanup and duplicate-run prevention
- the idea that the node contract must stay narrow and hard

### From `operator-trust-node-first.md`

This proposal is the strongest on human trust.

What I want to carry forward from it:

- the idea that a human should be able to open the node and understand what happened
- the idea that nodes outlast any one model, agent, or prompt
- the focus on visible state and readable truth

### From `extensibility-experimentability.md`

This proposal is the strongest on long-term change and experimentation.

What I want to carry forward from it:

- the node as a stable experiment boundary
- strong emphasis on modularity around a fixed node meaning
- clarity that agent behavior is the thing we should vary, not the node contract

## Final Recommendation

Open-Eywa should use a **balanced node-first foundation**.

That means:

- the node is the stable unit of work, truth, measurement, inspection, and recovery
- the node owns the durable on-disk contract
- agent runs are ephemeral contributors inside that contract
- code owns protocol correctness
- models contribute bounded judgment and content
- future changes should happen around the node, not by changing what a node fundamentally means

In short:

the node should be the place where truth lives, where correctness is checked, and where experiments are compared.

## Final Proposal

### What A Node Is

A node is a bounded unit of work with a durable on-disk contract.

It is the smallest unit that should be:

- inspectable by a human
- validated by code
- measured across runs
- replayable after failure
- stable even as agents, prompts, and models change

A node should not mean "one agent" or "one fixed process." It should mean "one persistent work container whose truth can be checked on disk."

### What A Node Owns

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

The key principle is that the node owns truth, not the agent.

### What An Agent Run Is

An agent run is a temporary attempt to advance a node.

It should:

- read prepared node context
- use only allowed tools
- write only allowed artifacts
- leave behind logs and outputs
- exit cleanly or fail explicitly

An agent run should never be treated as the durable carrier of meaning. It is disposable. The node is not.

### Minimal Node State Model

The node state model should stay as small as possible while still making control explicit.

At minimum, a node needs:

- a current status
- a next mode or next role hint
- a task or goal
- a contract for required artifacts
- a control area for orchestrator decisions

The specific status list can evolve, but the model should remain simple enough that a human can inspect the node and understand where it is in the lifecycle.

### Core Truth Files

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

### Completion, Failure, And Escalation

Completion should mean:

- the node satisfied its artifact contract
- the required files exist
- the orchestrator can validate them

Failure should mean:

- the node could not satisfy the contract safely
- retry or recovery rules were exhausted
- the node remains inspectable after failure

Escalation should mean:

- the node cannot safely continue under its current assumptions
- a higher-level decision is required

The system should never confuse process exit with success. A node is done because its contract is satisfied on disk.

### Hard In Code, Soft In Model Behavior

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
- stale-file cleanup

The soft layer can remain in model behavior:

- how a plan is phrased
- how a synthesis is worded
- how reasoning is expressed
- how a bounded task is carried out within the allowed contract

This preserves flexibility without outsourcing correctness.

### Extensibility

This design stays extensible because new agent types do not change what a node is.

New things can be added as:

- new roles
- new tool profiles
- new verification passes
- new repair passes
- new review patterns
- new experiment variants

But the node remains the same stable comparison boundary.

### A/B Testability

The node should be the main experiment boundary.

That means we should be able to vary:

- which agent type ran
- which prompt variant was used
- which tool policy was used
- which routing rule was used
- which retry or recovery policy was used

while keeping the meaning of the node fixed.

For future A/B tests, we should be able to ask:

- did the same kind of node complete more often
- with what cost
- in what time
- with what outputs
- with what failure modes

That becomes much easier if the node stays invariant and the variable parts are around it.

## Main Risks

The main risks in this node-first design are:

- burying too much process logic in scattered conventions
- letting the status model grow into a messy pseudo-workflow
- making node contracts too role-specific
- letting measurement hooks become inconsistent across node types

So the discipline we need is:

- keep the node contract small and explicit
- keep protocol hard
- keep the node meaning stable
- let variation happen in agent behavior and configuration, not in the meaning of the node itself

## Final Conclusion

The strongest foundation for Open-Eywa is a node-first core where the node is the stable unit of truth, correctness, measurement, and inspection, while agents are replaceable contributors acting inside that boundary. Among the current drafts, the balanced proposal is the best base, strengthened by the reliability proposal's hard-protocol language and the operator-trust proposal's emphasis on readable truth.
