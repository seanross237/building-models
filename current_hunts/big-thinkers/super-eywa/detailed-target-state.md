# Super Eywa — Detailed Target State

## Target Design

This doc describes the target shape of Super-Eywa at the highest level.

It is not the detailed build spec for `eywa-system/` or `data-system/`. Those docs should later zoom in and make the subsystem contracts more exact. This doc is the shared target state they should both be consistent with.

## What Super-Eywa Is

Super-Eywa is the larger system around an autonomous task-solving machine.

At the highest level, it is made of three conceptual layers:

- `Eywa`
  - the task-solving runtime
- `Bonsai`
  - the learning, storage, evaluation, and optimization layer around Eywa
- `Potter`
  - the later code-improvement layer that is allowed to improve implementation quality without changing validated behavior

For now, the practical system split is:

- `eywa-system/`
- `data-system/`

Potter is part of the long-term target state, but it is not the present build focus.

## North Star

The north star is a system where, as much as possible, a run can be understood as:

- a task
- a chosen set of variables

The core machine should stay strong and stable. The main thing that changes from run to run should be the variables, and the broader system should get better over time at choosing those variables.

The system should be built so that:

- it can solve tasks through a network of same-DNA nodes
- it records what happened in a clean, reusable way
- it can later learn from that history
- it can later support behavior-preserving implementation improvement

## Core Shape

The stable unit of the system is the node.

Every node should be the same kind of thing at its core. A node may appear in different roles inside a run, but the underlying machine should stay the same.

At a high level:

1. a task enters the system
2. Eywa instantiates a root node
3. nodes execute work, produce results, and request follow-up consequences
4. the overall run may expand into a graph of related nodes
5. the system records all of this in a form that can later be analyzed, replayed, reorganized, and learned from

The machine should be graph-capable by design, even if early runs often behave like a simple tree.

## The Bones

The bones are the parts of the system that should stay stable and should not be treated as run-to-run optimization knobs.

These are the current target bones:

- the stable unit is the node
- every node starts with exactly two behavior-shaping payloads:
  - `input`
  - `variables`
- variables are fully resolved before a node starts running
- node behavior should be shaped by variables, not by hidden undocumented behavior
- a node does not directly mutate the graph
- a node produces results and control/request outputs, and code validates and applies legal consequences
- the system is graph-capable by default
- graph relationships are explicit recorded facts, not just implied by directory nesting
- every node records the same factual core:
  - `state`
  - `results`
  - `metrics`
  - `events`
  - `edges`
- the original input and the fully resolved variables are always preserved
- replay-heavy artifacts are stored separately from the core node record
- core schemas are stable and code-validated
- the system must remain human-readable

The point of the bones is to keep the machine sturdy, legible, and comparable over time.

## What Belongs In Variables

Anything that changes how a node behaves, and can be decided before that node starts, should strongly tend to live in variables.

This includes things like:

- routing behavior
- decomposition behavior
- context policy
- tool policy
- budgets and limits
- verification strictness
- synthesis style
- retry and recovery behavior
- model or prompt style choices, if those are part of the system

The exact variable taxonomy is still to be nailed down, but the overall principle is already part of the target state:

- the bones define what the machine is
- the variables define how it behaves on this run

## Eywa In The Target State

Eywa is the task-solving runtime.

Its job is to take a task and execute a graph of same-DNA nodes that work toward solving it.

Eywa should be built so that:

- the root node is not a fundamentally different kind of thing from any other node
- nodes can create follow-up work through validated control outputs
- node outputs do not need to return only to the creating parent
- routing can be more general than parent-child return flow
- graph flexibility is allowed without giving up readability

At the highest level, a node:

1. receives input and variables
2. does work
3. may use tools under policy
4. produces results
5. may request follow-up consequences in the run graph

The human-facing story of what happened should still be easy to understand, even if the underlying system is flexible.

## Data-System In The Target State

The data-system is the layer that stores, organizes, scores, and later learns from what Eywa does.

Its job is not just to archive raw runs. Its job is to make later learning and later analysis possible.

At a high level, the data-system should eventually contain:

- run history
- benchmark tasks
- scored benchmark results
- replay and reconstruction artifacts
- promoted tasks that become benchmark material
- summaries, comparisons, and later variable-selection knowledge

For v1, the priority is not to build full optimization yet.

For v1, the priority is:

- preserve the important raw truth
- preserve the resolved variables
- preserve the outputs and graph facts
- preserve enough replay material that future reconstruction is possible
- keep the data easy to reorganize later

The system should be built so that later scoring, comparison, heuristics, and machine-learning layers can be added on top of the preserved run data rather than requiring a redesign.

## Bonsai In The Target State

Bonsai is the learning and optimization intelligence around Eywa.

It is not a separate executor replacing Eywa. It is the layer that studies:

- what kinds of tasks came in
- what variables were chosen
- how the run performed
- which patterns worked better than others

Its long-term job is to improve variable selection.

The intended progression is:

1. record and preserve clean data
2. compare results with simple heuristics and summaries
3. identify stronger variable choices for broad task categories
4. later move toward more learned or model-based variable selection

V1 does not need to complete this loop. V1 needs to keep the data good enough that this loop can be built honestly later.

## Potter In The Target State

Potter is a later system.

Its role is not to make Eywa more effective by changing the intended behavior of the machine. Its role is to improve code quality while preserving validated behavior.

Potter should eventually be allowed to improve things like:

- simplicity
- modularity
- flexibility
- intuitiveness
- robustness

But it should be gated by correctness-preserving checks, including dry-run equivalence machinery and later comparison machinery that protects the intended behavior of Eywa and Bonsai.

Potter is part of the target state, but not part of the immediate build sequence.

## V1 Priority

The immediate version should optimize for:

- strong bones
- clear node and recording contracts
- graph-capable execution
- explicit variables
- human readability
- preservation of enough truth that the system can be reconstructed and reorganized later

The immediate version should not over-focus on:

- sophisticated optimization logic
- mature ML selection
- overcomplicated storage systems
- premature Potter implementation

The first job is to build a system that is structurally clean enough to support those later layers.

## What Success Looks Like

At this overall level, success means:

- a future agent can read the target docs and understand what Super-Eywa is trying to become
- Eywa and the data-system can be designed as separate docs without contradicting each other
- the system is clearly graph-capable, node-first, and variable-driven
- the distinction between bones and variables is clear
- the system is being built so that later learning and later code-improvement are possible without changing the foundation

## Still To Decide

- the exact variable taxonomy
- the exact legal control/request schema a node may emit
- the exact legal edge types in the run graph
- the exact boundary between core node record and replay record
- the exact task-tagging and normalization pipeline for early Bonsai work
- the exact promotion rules for moving real tasks into benchmark material
- the exact shape of the first human-readable run summary layer
- the exact dry-run and equivalence requirements Potter will eventually depend on
