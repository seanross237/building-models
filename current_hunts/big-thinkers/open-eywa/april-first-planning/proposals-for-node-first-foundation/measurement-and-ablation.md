# Node-First Core For Open-Eywa

## Summary

Open-Eywa should be built so that every meaningful run can be measured, compared, and experimented on without changing the meaning of the node. The simplest strong core is a node-first system where the node is the stable contract, and everything around it is designed to be swappable, observable, and easy to ablate.

If we want to do many future experiments, the core must be easy to instrument. A node-first design works well because it gives us one stable place to compare outputs, costs, timings, failures, and behavior changes across variants.

## What A Node Is

A node is the unit we measure.

It is the durable work container that survives agent churn, prompt churn, and policy churn. If we cannot tell whether two runs produced different results for the same node, the system is not yet a good experiment platform.

## What A Node Owns

A node should own:

- its goal and context
- its status and transitions
- its outputs and state files
- its logs and usage records
- its child nodes
- its run history

That makes the node the natural place to attach metrics and compare experiments.

## What An Agent Run Is

An agent run is a variable part inside a stable node.

That separation matters because the whole point of experimentation is to vary something while keeping the comparison boundary stable. The node gives us that boundary.

## Minimal Node State Model

The minimal state should stay narrow:

- a status
- a role or mode
- a goal
- outputs
- control files

The more extra state we add, the harder it becomes to run clean tests and A/B comparisons.

## Core Files That Define Truth

The core truth files should remain fixed so experiments are comparable:

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

If those files stop meaning the same things across variants, then comparison breaks.

## Completion, Failure, Escalation

Completion should mean the node satisfied the artifact contract and the run can be scored.

Failure should mean the node could not satisfy the contract within the allowed recovery rules.

Escalation should mean the node needs a higher-level decision and should be excluded from “clean success” statistics unless the experiment explicitly measures escalations.

## What Must Be Hard In Code

The hard layer should define:

- artifact checks
- status transitions
- output validation
- path boundaries
- logging schemas
- usage accounting
- experiment labels or variant identifiers

If those are soft, then A/B tests become impossible to trust.

## What Can Stay Soft In Model Behavior

The model can stay soft in:

- phrasing
- strategy
- reasoning path
- selection among valid options
- style of explanation

Those are the variables we may actually want to measure.

## Extensibility For New Agent Types

New agent types should fit into the same node measurement model.

That means future agents should be able to plug into the node without changing how we score, inspect, or compare results. If a new agent is introduced, we should still know how its outputs map back to node-level metrics.

## Future A/B Testability

This is the strongest argument for a node-first foundation.

We should be able to A/B test:

- agent type
- prompt version
- tool set
- retry policy
- context layout
- recovery behavior

while keeping the node contract stable enough that the measurement remains clean.

## Biggest Risks

The biggest risks are:

- letting variants change the meaning of a node
- creating too many special cases for metrics
- making the node contract depend on hidden workflow logic
- losing comparability because logs or outputs are inconsistent

The remedy is stable node semantics, stable artifacts, and stable metrics.

## Conclusion

The simplest strong node-first core is one where the node is the stable unit of truth and measurement, and agents are variable components we can swap, compare, and improve over time. That gives Open-Eywa a clean foundation for experimentation without sacrificing reliability or inspectability.
