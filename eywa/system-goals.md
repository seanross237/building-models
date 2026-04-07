# Agent Orchestration System — Goals

This document describes the goals of an agent orchestration system. It is intentionally agnostic about *how* to achieve these goals. It is meant to be shared with different agents and architects, each of whom should propose their own system design to meet these goals. Different proposals can then be compared and the best one chosen.

## The core purpose

Build a system that, given a task, orchestrates agents to solve it — and **learns over time to get extremely good at this orchestration** by studying its own past performance.

## The goals

### 1. Flexibility with simplicity

The system should be **flexible enough** to handle a wide variety of tasks and workflows without needing structural rewrites, but **simple enough** to remain easy to build upon over time. Additions should feel like extending a clean foundation, not patching a complicated one.

### 2. Learning over time

The system should **get better at agent orchestration over time**. Not just at executing one static approach — at the whole skill of deciding how to orchestrate agents for new tasks. Improvement should come from studying what has actually worked in past runs.

### 3. Every run saved to a database

**Every run is persisted** to a database. Nothing transient, nothing ephemeral. The full history of how the system has attempted tasks is available for study.

### 4. Learning from past runs

Past runs should be **usable as training material** for improving future runs. The way runs are recorded needs to support the kinds of analysis, comparison, and iteration an improving system requires.

### 5. Bounded but flexible

The system should have **well-defined limits** (cost, depth, runtime, attempts) to prevent runaway behavior, while still giving real room for flexibility inside those limits. The boundaries should be clear and enforceable, not accidental.

### 6. Faithful truth preservation

Runs must be recorded **richly enough** that past decisions can be meaningfully re-studied — full prompts, full outputs, full variables, full context. Summaries alone are not enough. Without faithful truth preservation, "learn from past runs" is a slogan without substance.

### 7. Human-readable runs

Any human should be able to **open a single run and follow what happened and why**. A system that learns but is opaque to its operators is unmaintainable. Human-readability is not optional — it is load-bearing for long-term development, debugging, and trust.

## What this document does NOT specify

This document deliberately does not prescribe:

- *How* tasks get broken down or represented
- *How* agents coordinate with each other
- *How* decisions get made during a run
- *How* the system represents workflows internally
- *How* learning from past runs actually works
- *What* kinds of agents exist, or how many kinds there are
- *What* the storage format looks like
- *What* the improvement loop looks like

Agents reading this document should propose their own architectural answers to all of the above. **The goals are the fixed point; the implementation is open.**

## What a good proposal should do

A good proposal for a system meeting these goals should:

- Explain how it meets each of the 7 goals above
- Be specific enough that a different reader could implement it without major reinterpretation
- Be honest about which goals it prioritizes most and which tradeoffs it accepts
- Identify the parts it is least sure about, not just the parts it is most sure about
