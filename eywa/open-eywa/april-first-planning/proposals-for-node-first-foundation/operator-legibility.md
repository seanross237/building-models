# Node-First Core For Open-Eywa

## Summary

Open-Eywa should be stable at the node level, flexible at the agent level, and hard at the protocol level. The best node-first core is one where a human can open a node directory and understand, with minimal guesswork, what happened, what is happening, and what would count as success.

If the system is going to change often and support many future agent types, then the foundation must stay readable, local, and explicit. The node should remain the visible unit of truth, while agents remain temporary helpers that do not own correctness.

## What A Node Is

A node is a readable unit of work.

It is the folder where the story of one piece of work lives. It should be easy to inspect, easy to replay, and easy to compare against another node in a later experiment.

That means the node is not just a place for files. It is the human-facing record of a run.

## What A Node Owns

A node should own:

- its task goal
- its inputs
- its outputs
- its status
- its logs
- its history
- its child nodes

If a person needs to know what the node did, the answer should already be present on disk inside the node.

## What An Agent Run Is

An agent run is a transient attempt to produce or change node artifacts.

The agent can come and go. The node stays. That is important because operator trust depends on the node being the lasting evidence of what happened, not on any one run being perfect.

## Minimal Node State Model

The node state model should be simple:

- a current status
- a role or mode
- a goal or instruction
- a way to inspect outputs
- a way to inspect control state

If a later design wants to introduce more process structure, it should do so without making the node less readable.

## Core Files That Define Truth

The core truth files should be obvious and stable:

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

These files should tell the complete story of the node without requiring hidden runtime state.

## Completion, Failure, Escalation

Completion should mean the node has a valid terminal artifact and the orchestrator can prove it.

Failure should mean the node could not safely produce the required artifact.

Escalation should mean the node is telling the parent that it cannot continue under the current assumptions.

The system should never guess here. The files and statuses should make the answer unambiguous.

## What Must Be Hard In Code

Code should enforce:

- valid state transitions
- output presence
- file boundaries
- spawn rules
- cleanup rules
- duplicate prevention
- logging and accounting

If a model behaves oddly, the node should still be readable and the orchestrator should still know what to do.

## What Can Stay Soft In Model Behavior

The model can vary in:

- phrasing
- explanation style
- synthesis style
- planning style
- local reasoning path

That variability is acceptable as long as the node contract remains intact.

## Extensibility For New Agent Types

The node-first core should make it easy to add new agents without changing what the node means.

That is the key to long-term operator legibility. If later we add more specialists, the node should still be the same readable folder of truth.

## Future A/B Testability

This design supports future A/B testing if the node contract stays stable and the agent behavior is modular.

That makes it possible to compare:

- different prompts
- different tools
- different agent types
- different recovery strategies
- different thresholds or policies

without turning the node into a moving target.

## Biggest Risks

The main risks are:

- burying too much process inside the node
- letting prompts become the real protocol
- making the node too large and hard to scan
- allowing stale artifacts to mislead the orchestrator

The answer is to keep the node small, hard, and readable.

## Conclusion

The simplest strong node-first core is a durable, inspectable node that owns truth on disk while agents stay temporary and swappable. That gives Open-Eywa a foundation that humans can trust and future changes can build on cleanly.
