# Eywa System — North Star

For Sean's original vision and thinking, see: `../../open-eywa/seans_sarangkot_eywa_vision.md`

## What Eywa Is

Eywa is the execution engine. Given a task and a set of variables, it produces a result. That's it.

It is a node-based system. Every node has identical DNA. The only things that differ between nodes are the instructions given and the parameter variables passed in. This uniformity is the core bet of the entire system — it's what makes Eywa optimizable.

## The Core Bet

With the right variables, any node performs optimally on its task.

The entire optimization story — benchmarking, heuristics, ML — depends on this being true. If nodes are uniform and parameterized, then improving Eywa becomes a variable selection problem. If nodes are snowflakes with hidden behavior, optimization is impossible.

## What a Node Does

A node receives a task and variables. It then decides what to do:

- Solve the task directly
- Make a plan and solve it
- Make a plan and pass it to another node
- Make a plan, decompose it, and distribute to multiple child nodes

Every node makes this decision the same way, governed by its variables. A root node and a leaf node deep in a tree are fundamentally the same thing — one just got different instructions and possibly different variable values.

## The Variable Model

Variables are the knobs of the system. They control things like:

- How the node approaches planning (method, depth, decomposition strategy)
- How it evaluates progress (evaluation strictness, continue/replan/escalate thresholds)
- What model to use
- What tools are available
- How much context to assemble and from where
- Retry and recovery behavior
- Synthesis strategy

Variables can be set at the tree level (inherited by all nodes) or at the node level (overriding the tree default). The variable schema must be explicit, closed, and versioned — no hidden knobs.

Every run must record exactly which variables were active. This is non-negotiable. Without clean variable records, the data system has nothing to learn from.

## The Node Lifecycle

Every node moves through a lifecycle:

1. Receives instructions and variables
2. Decides its approach (solve, plan, decompose)
3. Executes — possibly creating child nodes that go through this same lifecycle
4. Produces a result
5. Gets evaluated (by parent or evaluator)
6. Terminates (completed, escalated, or failed)

The orchestrator owns this lifecycle. Models contribute judgment within it — planning, reasoning, evaluating — but code owns the protocol, state transitions, and correctness.

## The Runtime Seam

Eywa doesn't care what model runs inside a node. The runtime seam is the boundary:

- Orchestrator prepares a structured request (instructions + variables + context)
- Runtime executes it (could be OpenRouter, could be simulated, could be anything)
- Runtime returns a structured result
- Orchestrator validates and progresses

This makes Eywa provider-agnostic and testable offline.

## What Eywa Records

Every node run produces:

- The exact instructions and variables used
- The prepared context sent to the model
- The raw model response
- Tool calls and results
- Usage and cost data
- Events (raw facts) and summaries (derived views)
- The terminal outcome and any artifacts

This is what the data system consumes. Eywa's job is to produce clean, complete records. The data system's job is to learn from them.

## What Eywa Is Not

- Eywa does not decide which variables to use. That's Bonsai / the selection layer.
- Eywa does not optimize itself. That's the optimization loop around it.
- Eywa does not improve its own code. That's the Potter.

Eywa executes. Cleanly, observably, and parameterically.

## The Dream State

When Eywa is fully realized:

- The structure of any run is simply: the task + the variables chosen
- Each node is an independent unit — the rest of the tree is almost irrelevant in the moment of execution
- The system is a simple chaining of uniform nodes
- All flexibility lives in the variables, all structure lives in the bones
- Every run produces data clean enough to train on
