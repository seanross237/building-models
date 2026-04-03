# Eywa System North Star

For Sean's original vision and thinking, see: `../../open-eywa/seans_sarangkot_eywa_vision.md`

## The Point

Eywa is the execution engine of Super Eywa.

Its job is simple: given a task and a set of parameter variables, produce a result.

That is the whole game. Eywa is not a personality. It is not a chat interface. It is not a bag of bespoke agent types. It is not a loose collection of prompt experiments. It is a node-based agent orchestration system built around one hard idea:

**every node is the same machine.**

The only things that change are:

- the instructions the node receives
- the variables the node is given
- the context assembled for that run

Everything else is shared DNA.

If this remains true, Eywa stays legible, optimizable, and composable. If this stops being true, the system collapses into special cases and folklore.

## What Eywa Is

Eywa is a uniform graph of nodes that execute work.

A node receives:

- a task
- a set of variables
- context

It then decides how to proceed. A node may:

- solve the task directly
- make a plan and solve it itself
- make a plan and pass that plan to another node
- decompose the task into multiple child nodes

This is not four different systems. This is one system expressing four possible moves.

A root node and a deep leaf node are fundamentally the same thing. The root is not a manager species. The leaf is not a worker species. They are the same node under different local conditions.

That symmetry matters. It means orchestration is not built from castes. It is built from recursion.

## What Eywa Refuses To Be

Eywa refuses to become a zoo of handcrafted agent identities.

It refuses:

- specialized node classes for every new workflow
- invisible heuristics that cannot be inspected or replayed
- prompt piles that only work because someone remembers the ritual
- runtime behavior that depends on hidden state
- vendor lock-in disguised as architecture
- optimization by anecdote

If a capability cannot be expressed through the common node shape plus explicit variables, it does not belong in Eywa.

The system must be boring in its bones and powerful in its configuration.

## The Core Bet

Eywa is built on a strong bet:

**with the right variables, any node can perform optimally for its task.**

Not "well enough." Optimally within the system’s operating limits.

This is what makes Eywa worth building. If every node is the same machine, then improvement stops being a problem of inventing new species of agents and becomes a problem of choosing the right variables for the situation.

That is the leverage.

The system becomes optimizable because performance can be traced back to explicit, comparable choices:

- which planning method was used
- which model was selected
- how strict evaluation was
- how tools were allowed or constrained
- how context was assembled
- how retries were handled
- how synthesis was performed

If these choices are explicit, recorded, and replayable, improvement becomes a real discipline. Eywa gets better by learning which variable settings produce the best outcomes for which classes of tasks.

## Nodes Are Uniform By Design

The deepest architectural principle in Eywa is uniformity.

Every node has identical DNA. There is no distinction in kind between:

- the first node in a run
- a planning node
- an evaluator node
- a synthesizer node
- a child node at depth seven

These are not different beings. They are the same execution primitive with different instructions and variables.

This matters because uniform systems can be studied, tuned, and trusted. Non-uniform systems sprawl. Once different node types carry hidden rules, the system becomes harder to reason about and nearly impossible to optimize globally.

Eywa does not want more kinds of nodes. It wants better variable assignment.

## Variables Are The Knobs

Variables are the control surface of Eywa.

They are not incidental metadata. They are the operative knobs that shape how the node behaves. They determine the style, rigor, cost profile, decomposition strategy, and risk posture of a run.

Variables include things like:

- planning method
- evaluation strictness
- model choice
- tool policy
- context assembly strategy
- retry behavior
- synthesis strategy
- escalation policy
- budget posture
- stopping conditions

Some variables live at the tree level and are inherited downward. Some variables are overridden at the node level when local conditions demand it. Both matter. What matters more is that every effective variable must be explicit.

There is no acceptable hidden configuration in Eywa.

Every run must record the variables that actually governed behavior. If a variable affected the outcome, it must be visible in the record. If it cannot be recorded, it is not a real part of the system.

## The Runtime Seam

Eywa is provider-agnostic by design.

The orchestrator does not care whether execution happens through OpenRouter, a direct model provider, a simulator, a local runtime, or something that does not exist yet. Its responsibility is to prepare a structured request for a node run.

The runtime’s responsibility is different:

- accept the structured request
- execute it
- return a structured result

This seam is sacred.

Eywa owns orchestration. The runtime owns execution. Crossing those responsibilities creates coupling, muddies the logs, and weakens portability.

Provider choice is a variable. Provider dependence is a failure mode.

## Recording Is Not Optional

Eywa must produce clean records for every run.

Not vague summaries. Not selective traces. Full, structured, replayable records.

Each run should capture:

- instructions
- variables
- assembled context
- model responses
- tool calls
- usage
- cost
- events
- outcomes

This is not observability theater. This is the raw material for learning.

The data system can only improve the system if the system tells the truth about what happened. If records are incomplete, the optimization layer is blind. If records are messy, the optimization layer learns noise. If records are inconsistent, the optimization layer becomes superstition.

Eywa must be honest enough to be optimized.

## The Trust Boundary

Eywa draws a hard line between what code must own and what models may contribute.

Code owns:

- protocol
- state transitions
- execution rules
- correctness boundaries
- data integrity
- recording
- enforcement of allowed behavior

Models contribute bounded judgment:

- planning
- reasoning
- evaluation
- synthesis

This boundary is not philosophical. It is operational.

Models are powerful but unreliable in the ways that matter most for system integrity. They should shape decisions within a controlled frame. They should not own the frame itself.

Eywa does not ask models to define truth. It asks them to work inside a truth-preserving machine.

## The Three Sibling Systems

Super Eywa is not one blob. It is three sibling systems with distinct responsibilities.

### Eywa

Eywa is the execution engine.

Its question is: **execute this task with these variables.**

Eywa does not search for the globally best settings during execution. It runs the work.

### Bonsai

Bonsai is the optimization layer.

Its question is: **based on past runs, which variables should Eywa choose here?**

Bonsai learns from records. It improves selection, not execution protocol. It does not replace Eywa. It makes Eywa sharper.

### Potter

Potter is the code-level optimizer.

Its question is: **how can the code improve without changing behavior?**

Potter comes later. Its role is not to redesign the system’s logic on instinct. Its role is to improve the machinery while preserving externally validated behavior through dry runs and comparable execution records.

These systems are siblings, not substitutes.

- Eywa executes.
- Bonsai selects.
- Potter hardens and improves the code.

Confusing these layers will destroy clarity.

## The Dream

The dream is radical simplicity.

Any run in Eywa should be understandable as:

- the task
- the variables chosen
- the resulting chain of uniform nodes

That is it.

All flexibility lives in the variables. All structure lives in the bones.

Each node is independent. Each node can be inspected on its own terms. Each subtree can be replayed, compared, and learned from. The system scales not by inventing new metaphors but by repeating one strong primitive with discipline.

Eywa should feel like a simple machine that can express complex behavior, not a complex machine barely held together by taste.

## Non-Negotiables

These principles are not preferences. They are constraints.

- One node shape.
- Explicit variables.
- Provider-agnostic runtime seam.
- Full structured recording.
- Hard trust boundary.
- No hidden agent castes.
- No magic behavior that cannot be explained from task plus variables plus code.

If future work violates these constraints, it is not extending Eywa. It is drifting away from it.

## Final Definition

Eywa is a node-based execution engine where every node shares identical DNA, every run is governed by explicit variables, and every outcome is recorded cleanly enough to optimize the whole system over time.

It is not a tangle of special-purpose agents.

It is a uniform orchestration substrate for turning tasks and variables into results.
