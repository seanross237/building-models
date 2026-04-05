# Eywa System — Detailed Target State

## Target Design

This doc describes the target shape of the `eywa-system/`.

It is the build-guiding target doc for Eywa specifically.

It should stay aligned with the root Super-Eywa target docs, but it zooms in on:

- the node runtime
- the graph execution model
- the recording contract
- the main behavior-shaping surfaces that should remain variable-driven

## What Eywa Is

Eywa is the task-solving runtime.

Its job is to take a task and work on it through a graph of same-DNA nodes.

The system may often look like a tree, but the runtime should be graph-capable from the beginning.

Eywa owns:

- node creation and execution
- prompt preparation
- tool usage inside policy
- action/output emission
- graph expansion through validated requests
- recording what happened at the run and node level

Eywa does not own:

- long-term optimization of variable selection
- grading strategy as a whole
- Potter-style implementation improvement

## Eywa North Star

The north star for Eywa is a runtime where:

- the stable unit is the node
- every node is fundamentally the same kind of thing
- most important run-to-run adaptation lives in explicit variables
- the runtime stays inspectable and reconstructable
- graph flexibility is supported without sacrificing human readability

The design goal is that the bones stay sturdy while the important behavioral flexibility is captured in explicit pre-start variables.

## The Stable Unit: The Node

The node is the core unit of execution in Eywa.

Every node should have the same fundamental structure and runtime contract.

A root node is not a different species from a middle node or a late-stage synthesis-like node.

Different roles should emerge mainly from:

- the node input
- the resolved variables

not from separate core machinery.

## The Bones Of Eywa

The following are part of the Eywa bones and should not be treated as run-to-run optimization knobs:

- the node is the stable execution unit
- every node begins from:
  - `input`
  - `variables`
  - identity and bookkeeping facts
- variables are fully resolved before a node starts
- a node does not directly mutate the run graph
- a node produces work results and structured outgoing packets
- code validates and applies legal follow-up consequences
- graph relationships are explicit recorded facts
- each node preserves the same core record categories:
  - `input`
  - `variables`
  - `state`
  - `results`
  - `prompt`
  - `logging`
- replay-heavy material is stored separately from the core node record
- the system must be able to produce a human-readable story of what happened

These bones exist so that Eywa remains legible, comparable, and sturdy while the behavior within those bones can later be optimized through variables.

## Node Starting Contract

For v1, a node starts from three categories:

- `input`
- `variables`
- identity and bookkeeping facts

### Input

The node `input` is the starting assignment package for that node.

For v1, this includes:

- the instructions or task for this node
- the provided context for this node
- any explicitly attached or prepared artifacts for this node

The `input` describes the situation the node is being placed into.

### Variables

The node `variables` are the pre-resolved behavior-shaping controls for that node.

These should be fully resolved before the node starts.

A node should not begin with a vague or partially inherited behavioral configuration that needs to be inferred later.

### Identity And Bookkeeping

These are factual metadata fields around the node rather than behavior knobs.

Examples include:

- node identity
- run identity
- creation metadata
- timestamps

These are part of the node record, but they are not part of the run-to-run optimization surface.

## Run Packet And Node Packet

Eywa should preserve a frozen packet at both the run level and the node level.

### Run Packet

Each overall run should have a `run_packet`.

Its purpose is to preserve the top-level assignment and run setup thoroughly enough that the run can later be understood and, as much as possible, reconstructed.

At a high level, the run packet should preserve:

- the original top-level task exactly as given
- run-level variables
- top-level context, constraints, and attachments
- root setup facts

### Node Packet

Each node run should have a `node_packet`.

Its purpose is to preserve exactly what that node was given when it started.

At a high level, the node packet should preserve:

- the node input
- the fully resolved variable set for that node
- node-specific setup facts

Even if the system also tracks run-level defaults and node-level overrides separately, the node packet should preserve the full resolved variable set so the node can be understood and reconstructed in isolation.

## Node Runtime Shape

At the highest level, a node runtime does this:

1. receives its node packet
2. prepares the prompt and working context
3. optionally uses tools under policy
4. does work locally
5. emits structured results and outgoing packets
6. the system validates and applies legal consequences

The runtime should stay generic.

Planning, delegation, execution, and synthesis-like behavior should not require separate fundamental node types.

They should emerge from the same-DNA node behavior operating on different inputs and variables.

## Human-Facing Action Layer

Although the backend should stay flexible, the front layer should remain simple and human-readable.

For v1, the intended human-facing `action_type` vocabulary is:

- `local_attempt`
- `local_replan`
- `recruit_help`
- `report_success`
- `report_problem`

These are the simple action labels a human should be able to read in a run story.

Synthesis should not be treated as a special front-layer action for v1.

A synthesis-like step should simply be a normal node performing a local attempt on provided upstream outputs.

## Node Output Shape

For v1, a node should emit:

- `action_type`
- `results`
- `outgoing_packets`

This keeps the human-readable action layer simple while keeping the backend packet structure explicit.

### Outgoing Packet Fields

Each outgoing packet should preserve:

- `message_type`
- `target`
- `message`
- `attachment_refs`

### V1 Message Types

For v1, the intended `message_type` set is:

- `helper_assignment`
- `work_result`
- `replan_message`
- `success_report`
- `problem_report`

The runtime should validate these packets and then apply legal graph consequences.

## Work Results And Outgoing Packets

A node should not directly author system facts like metrics or edge records.

Those should be created by the system from what the node did and from the validated outgoing packets.

The node's meaningful authored output should be thought of in two parts:

- work results
- outgoing packets

### Work Results

Work results are the actual artifacts of the node's work.

Examples include:

- an answer
- a plan
- helper instructions
- a summary
- a code patch
- an explanation of why the goal is unachievable

### Outgoing Packets

Outgoing packets are structured messages to intended targets.

These are how the node asks for follow-up work, returns results, replans, or reports status upward or elsewhere in the graph.

## Graph Model

Eywa should be graph-capable by design.

It should not hard-code the assumption that a node's output always flows back to the node that created it.

That may be the default often, but it should not be the only legal shape.

For v1, the intended first-class edge types are:

- `created_by`
- `sends_output_to`
- `depends_on`

These should be enough to express the initial runtime shape without introducing too much complexity.

This means Eywa should be able to distinguish between:

- who created a node
- where a node's output goes
- what a node is waiting on

## Routing And Sequencing

Routing should be part of the behavior-shaping layer, not buried in hard-coded orchestration assumptions.

For example:

- output destination should be configurable
- follow-up work may be launched sequentially or simultaneously

For v1, some of these may be held constant in practice, such as always using sequential helper launching at first.

But they should still be treated as part of the variable-driven behavior surface rather than as permanent bones.

## Recording Model

The Eywa core node record should stay clean and readable.

For v1, the intended core node record categories are:

- `input`
- `variables`
- `state`
- `results`
- `prompt`
- `logging`

### Logging

For v1, `logging` should be the umbrella category that contains:

- metrics
- events
- edges

This keeps the node record readable without losing the important factual record.

### Replay

Replay-heavy material should be stored separately from the core node record.

This replay layer exists so that later the system can:

- reconstruct what happened more deeply
- compare runs
- support dry-run or replay-oriented work
- support later Potter-style behavior-preserving checks

The replay layer should exist from v1, even if its exact contents evolve later.

## Prompt Preservation

Eywa should preserve the actual prepared prompt a node was given.

This should remain separate in concept from the primitive node input.

The input is the assignment and provided context.

The prompt is the prepared rendered execution packet produced from:

- input
- variables
- system scaffolding

Keeping prompt preservation explicit is important for reconstruction and later analysis.

## Variable Families For V1

The exact variable schema is not yet frozen, but the first broad variable families for Eywa should be:

- `injected prompts`
- `workflow structure`
- `model selection`
- `context policy`
- `tool policy`
- `budget policy`
- `verification policy`
- `recovery policy`
- `routing policy`

These are not yet the full final field list.

They are the broad behavioral regions that Eywa should treat as variable-driven rather than baking into the bones.

## Core Variables To Focus On First

The first small core variable list that should get the most attention is:

- `model`
- `injected_prompt_profile`
- `context_policy`
- `workflow_structure`
- `verification_policy`

These are the highest-leverage starting knobs for early iteration.

## Human-Readable Run View

The required human-readable run view for v1 should be a timeline or story view.

When a human inspects a run, the system should be able to present a simple sequence such as:

- root node made a local attempt
- root node recruited three helpers
- helper one returned a result
- parent chose to launch the next helper
- a node replanned
- the run finished

Other views such as graph views or node tables may be added later if they can be derived cheaply, but the required v1 readable layer should be the story of what happened over time.

## V1 Build Priority

The purpose of Eywa v1 is not to complete the whole self-optimization loop.

The purpose of Eywa v1 is to provide:

- strong same-DNA node execution
- explicit pre-start variables
- graph-capable control flow
- clean recording
- prompt preservation
- enough truth preservation that later learning and replay are possible

Eywa v1 should be judged mainly by whether it creates a sturdy, inspectable, variable-driven runtime foundation.

## Still To Decide

- the exact state machine for nodes
- the exact representation of work results
- the exact replay record contents
- the exact initial prompt scaffolding strategy
- which v1 variables are fixed constants in practice even though they conceptually belong to the variable surface
