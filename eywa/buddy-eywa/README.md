# Buddy-Eywa

A proposed evolution of Super-Eywa where strategic decisions and tactical execution are cleanly separated, and workflows are expressed as composable, reusable subgraph types picked at runtime by a meta-agent called **Buddy**.

This folder is a design snapshot, not working code. It captures the direction agreed on in the 2026-04-07 design conversation with Sean and is intended as the starting point for a worktree-based implementation.

## Table of contents

- `01-vision.md` — north star, the core reframe, key concept definitions
- `02-subgraph-types.md` — what a subgraph type is, the library, what to seed
- `03-buddy-loop.md` — multi-turn buddy, checkpoints, pivots, nesting, fail-fast
- `04-workers-slots.md` — the single-turn rule and clean division of labor
- `05-artifacts.md` — the artifact store and two views of every artifact
- `06-learning-surfaces.md` — what the Scientist sees and how learning trajectories work
- `07-relation-to-current.md` — how buddy-eywa relates to the current super-eywa codebase
- `08-implementation-plan.md` — build chunks in order, eval-informed modifications
- `09-evaluation-and-open-questions.md` — subagent eval summary and unresolved questions
- `examples/` — three worked examples of buddy + subgraph in action

## The one-sentence version

A run is a tree of **buddy loops**, where each loop is a sequence of **subgraph executions** (bursts of bounded autonomy), and each subgraph is a **pure DAG of single-turn worker slots**, with a **Scientist** growing the subgraph-type library over time from observed run data.

## Where this lives relative to super-eywa

Buddy-Eywa is a sibling folder to `super-eywa/`, not a replacement. Implementation will happen in a worktree branched off `main`, with eventual merge once the new bones have been validated against the grading bench. The current super-eywa runtime, contracts, and grading infrastructure remain the reference implementation until buddy-eywa is ready to replace them.
