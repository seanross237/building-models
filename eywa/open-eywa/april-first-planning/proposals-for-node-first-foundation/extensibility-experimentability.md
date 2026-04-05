# Node-First Core For Open-Eywa

## Summary

Open-Eywa should be stable at the node level, flexible at the agent level, and hard at the protocol level. The simplest strong core is a node-centric system where the node stays the durable unit of truth, while agents remain replaceable contributors that can be swapped, split, added, or tested without changing what the node means.

If we expect frequent changes, many new agent types, and lots of future experiments, then the foundation has to be both durable and modular. The node should stay simple and inspectable, while the behavior around it should be configurable enough to support future A/B tests and new execution patterns.

## What A Node Is

A node is the stable unit of work, state, and measurement.

It is the thing that persists on disk and gives us a single readable place to understand one piece of work. A node should not mean “one agent” or “one fixed process.” It should mean “one bounded unit of truth,” even if multiple agent runs eventually touch it.

That makes the node the right place to anchor extensibility. New agent types can come and go, but the node remains the constant.

## What A Node Owns

A node should own:

- its goal or task
- its current status
- its readable input and output files
- its orchestrator control files
- its logs, usage data, and artifacts
- its child nodes, when it has them
- its complete history on disk

The key idea is that the node owns truth, not the agent. An agent can create or modify node artifacts, but it should never be the source of truth itself.

## What An Agent Run Is

An agent run is a temporary execution inside a node.

It is a replaceable contributor that reads the node’s prepared context, uses the allowed tools, writes back to the node, and exits. If we later want multiple agents inside one node, the node should still remain the same durable container while the mix of contributors changes.

That makes agent behavior something we can vary experimentally without changing the meaning of the node.

## Minimal Node State Model

The minimal state model should be intentionally small:

- a current status
- a role or mode for the next contributor
- a goal or parent instruction
- an output area
- a control area for the orchestrator

That is enough to make the system legible and measurable without turning the node into a workflow engine.

If a node-only design and a node-plus-workflow design would differ here, the first choice should still be the node-first version unless the workflow layer clearly improves experimentability without adding too much conceptual weight.

## Core Files That Define Truth

The core truth files should stay stable and easy to compare across experiments:

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

These files should be the primary experiment boundary. If we change agent behavior, the node should still mean the same thing and these files should still tell the same story.

## Completion, Failure, Escalation

Completion should mean the node satisfied its artifact contract and the orchestrator can prove it from disk.

Failure should mean the node could not satisfy that contract safely or recoverably.

Escalation should mean the node cannot continue under its current rules and needs a higher-level decision.

The important thing is that success and failure are determined by explicit file and status rules, not by whether an agent sounds confident or the model stops cleanly.

## What Must Be Hard In Code

The hard part of the system should be the protocol, not the prose.

Code should enforce:

- state transitions
- output requirements
- path boundaries
- tool permissions
- duplicate spawn prevention
- stale-file cleanup
- deterministic completion checks
- logging and usage capture

If we want future A/B tests to be meaningful, the protocol must stay stable while the agent behavior varies.

## What Can Stay Soft In Model Behavior

The model can stay soft on:

- how it writes
- how it explains
- how it sequences its internal reasoning
- which valid approach it chooses inside a node

Those are the parts we want to experiment with.

## Extensibility For New Agent Types

This is where the node-first design shines.

New agent types should be able to appear as new contributors to the same node without changing the node’s meaning. That means future additions like specialist reviewers, repair agents, math checkers, or alternative synthesizers should fit into the same durable node contract.

The node should stay the stable anchor while the agent set evolves around it.

## Future A/B Testability

This design should make experiments cheap and comparable.

We should be able to vary:

- agent type
- prompt text
- tool set
- retry policy
- context assembly
- recovery behavior
- node-level decision thresholds

without rewriting the meaning of the node or the way results are interpreted.

That means the node contract and logging format should be stable enough that we can compare runs across time and across variants.

## Biggest Risks

The biggest risks are:

- making the node too abstract and turning it into a hidden workflow engine
- letting process logic drift into prompts instead of code
- making experiment variants change the meaning of the node
- overloading the node with too many special cases
- losing clean measurement because logs or artifacts are inconsistent

The answer is to keep the node narrow, explicit, and stable, while making the surrounding agent behavior and experiment knobs modular.

## Conclusion

The strongest node-first foundation is one where the node stays the durable unit of truth and measurement, and agents remain swappable contributors that can be experimented on freely. That gives Open-Eywa a stable core for future extensibility, future A/B tests, and ongoing iteration without letting the system lose its shape.
