# Colossus

An autonomous AI system that builds itself into the most capable task-execution system possible, using existing foundation models without training new ones.

## How It Works

A **controller** agent runs every 5 minutes (via `bootstrap.sh`). It reads state files, decides what to do, spawns **worker** agents in tmux windows, and updates state. Workers build components, run experiments, compile knowledge, and write results back to files. Everything coordinates through the file system.

## Conventions

- All state lives in markdown files. No external databases until the system decides it needs one and builds it.
- The controller runs in the `colossus` tmux session. Workers are tmux windows in the same session.
- Workers write results to their file in `workers/`.
- Code the system builds goes in `infrastructure/`.
- Knowledge entries go in `knowledge/`.
- Experiment designs and results go in `experiments/`.
- Benchmark data and scores go in `benchmarks/`.

## Directory Layout

```
colossus/
  MISSION.md        — the plan (do not modify autonomously)
  CONTROLLER.md     — controller operating instructions
  STATE.md          — current system state (controller updates this)
  DECISIONS.md      — decision log (append-only)
  BUDGET.md         — spending limits and tracking
  bootstrap.sh      — starts the controller loop
  controller.log    — stdout/stderr from controller cycles
  infrastructure/   — code the system writes for itself
  knowledge/        — compiled domain knowledge and procedures
  experiments/      — experiment designs and results
  benchmarks/       — benchmark datasets and scores
  workers/          — worker state files
```

## Rules

1. Never modify MISSION.md — that's the human's document.
2. Always update STATE.md after significant actions.
3. Always log decisions in DECISIONS.md with timestamp and reasoning.
4. Respect BUDGET.md limits. Check before spawning expensive work.
5. Worker IDs are sequential integers: worker-001, worker-002, etc.
6. When a worker completes, it updates its own file with status and results.
7. When uncertain, write the uncertainty to STATE.md rather than guessing.
