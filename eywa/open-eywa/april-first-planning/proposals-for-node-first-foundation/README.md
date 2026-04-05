# Proposals For Node-First Foundation

This folder contains the first round of proposal docs for the simplest strong node-first foundation for Open-Eywa.

## Primary Comparison Set

These are the four main proposals to compare side by side:

- `reliability-hard-guarantees.md`
- `operator-trust-node-first.md`
- `extensibility-experimentability.md`
- `codex-balanced-node-first.md`

## Supplemental Variants

These are extra drafts that came out of the same round and may still be useful:

- `operator-legibility.md`
- `measurement-and-ablation.md`

## Shared Prompt Direction

All proposals were generated under the same high-level constraint:

- stable at the node level
- flexible at the agent level
- hard at the protocol level
- inspectable by humans
- reliable under messy model behavior
- easy to measure
- easy to evolve
- easy to A/B test in the future

## Opus Concrete Proposal

- `opus-node-first-core.md` — Full implementable spec: 5-status state machine, contract/ directory with JSON schemas, pure-function orchestrator, agent I/O protocol, decision table, risks, and migration path

## Comparison Goal

The goal of this folder is not to pick wording. It is to compare different ideas about:

- what a node fundamentally is
- what a node should own
- what an agent run is relative to a node
- what the minimal node state model should be
- what files define truth
- what completion, failure, and escalation should mean
- what must be hard in code vs soft in model behavior
- how the system should stay extensible and testable over time
