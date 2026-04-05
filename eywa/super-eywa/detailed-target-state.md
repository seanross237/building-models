# Super Eywa — Detailed Target State

## Target Design

This doc describes the target shape of Super-Eywa at the highest level.

It is the shared target doc for the whole system.

The subsystem docs in:

- `eywa-system/`
- `data-system/`

should be more specific than this doc, but they should not contradict it.

## What Super-Eywa Is

Super-Eywa is a system being built to improve itself in two different ways:

1. by getting better at choosing variables for a task
2. by later improving the bones of the system without changing validated behavior

At the highest level, the system is made of three conceptual layers:

- `Eywa`
  - the task-solving runtime
- `Bonsai`
  - the storage, learning, grading, and variable-optimization layer around Eywa
- `Potter`
  - the later behavior-preserving code-improvement layer

For now, the practical build focus is:

- `eywa-system/`
- `data-system/`

## North Star

The north star is a machine where, as much as possible, a run can be understood as:

- the task
- the chosen variables

The important run-to-run adaptation should live in explicit variables.

The bones should stay strong and stable.

The broader system should get better over time at:

- choosing better variables
- preserving and learning from what happened
- later improving the bones without changing intended behavior

## The Three Systems

### Eywa

Eywa is the task-solving runtime.

It takes a task, instantiates a root node, and works through a graph of same-DNA nodes to try to solve that task.

Eywa owns:

- node creation and execution
- prompt preparation
- tool use under policy
- validated graph expansion
- node-level recording

Eywa does not own:

- long-term variable learning
- grading strategy as a whole
- behavior-preserving code improvement

### Bonsai

Bonsai is the learning and optimization layer around Eywa.

Its job is to:

- preserve run truth
- organize grading and comparison
- study which variables worked well in which situations
- improve future variable choice

An expected future subcomponent of Bonsai is `Gardener`, which proposes short-term variable ideas and experiments by inspecting real runs before a more mature ML-based selector exists.

### Potter

Potter is the later code-improvement layer.

Its job is not to improve task performance by silently changing intended behavior.

Its job is to improve the bones:

- simplicity
- modularity
- flexibility
- intuitiveness
- robustness

while preserving validated behavior through correctness and equivalence checks.

## Core Design Commitments

The following are core commitments of the target state.

### 1. Node-First Design

The stable unit of the system is the node.

Every node should be fundamentally the same kind of thing.

Different node roles should come mainly from:

- the input it was given
- the variables it was given

not from separate special-purpose node species.

### 2. Bones Vs Variables

The system should be built so that:

- the bones define what the machine is
- the variables define how the machine behaves on this run

Anything that shapes behavior and can be decided before a node starts should strongly tend to live in variables.

The bones should stay stable so the system remains:

- legible
- comparable
- reconstructable

### 3. Graph-Capable Execution

The runtime should be graph-capable by design.

It should not hard-code the assumption that outputs always flow back only to the node that created a child.

The system may look tree-like often, but the underlying structure should support more flexible routing.

### 4. Preserved Truth

The system should preserve enough truth from every run that it can later be:

- reconstructed
- reorganized
- graded
- compared
- learned from

This is more important in v1 than sophisticated optimization logic.

### 5. Correctness And Effectiveness Stay Separate

The system must keep two different kinds of evaluation separate:

- `correctness-suite`
  - protects whether the machine is behaving correctly
- `grading`
  - measures how well the machine performs on test questions and later benchmarks

These two areas may inform each other, but they should not be mentally or structurally collapsed together.

## The Bones

At the overall system level, the current target bones are:

- the stable execution unit is the node
- every node begins from:
  - `input`
  - `variables`
  - identity and bookkeeping facts
- variables are fully resolved before a node starts
- nodes do not directly mutate the graph
- nodes emit work results and structured follow-up outputs
- code validates and applies legal graph consequences
- graph relationships are explicit recorded facts
- every node preserves the same core record categories:
  - `input`
  - `variables`
  - `state`
  - `results`
  - `prompt`
  - `logging`
- replay-heavy material is stored separately
- the system must remain human-readable

These bones exist so that later learning and later Potter work have a stable foundation.

## Eywa In The Target State

Eywa should be a graph-capable runtime of same-DNA nodes.

At a high level:

1. a task enters the system
2. Eywa creates a root node
3. nodes work, emit results, and request follow-up consequences
4. the run may expand into a graph of related nodes
5. the system records what happened in a reconstructable form

The human-facing story of the run should stay simple even if the backend is flexible.

## Data-System In The Target State

The data-system should preserve and organize the truth of Eywa runs.

Its main jobs are:

- preserve run-level and node-level packets
- preserve core node records and replay records
- organize grading questions and grading runs
- keep correctness separate from grading
- create derived views and summaries that later Bonsai work can use

For v1, the data-system should prioritize truth preservation and reorganizability over mature optimization logic.

## V1 Priority

The immediate version should optimize for:

- strong bones
- explicit variables
- graph-capable execution
- clean recording contracts
- human readability
- enough preserved truth for later learning

The immediate version should not over-focus on:

- mature ML variable selection
- Potter implementation
- a heavy database-first architecture
- premature complexity in benchmarking logic

The first version should be sturdy enough that those later layers can be added honestly.

## What Success Looks Like

At this level, success means:

- a future agent can read the target docs and understand what Super-Eywa is trying to become
- Eywa is clearly node-first, graph-capable, and variable-driven
- the data-system is clearly the truth-preserving and grading layer around Eywa
- the distinction between bones and variables is clear
- the distinction between correctness and effectiveness is clear
- the system is being built so that Bonsai and later Potter can be added without replacing the foundation

## Still To Decide

- the exact serialization format of the preserved run truth
- the exact database or derived-table strategy for v1 and shortly after
- the exact task-tagging and normalization pipeline for early Bonsai work
- the exact promotion rules for moving grading material into official benchmarks
- the exact dry-run and equivalence machinery Potter will eventually depend on
