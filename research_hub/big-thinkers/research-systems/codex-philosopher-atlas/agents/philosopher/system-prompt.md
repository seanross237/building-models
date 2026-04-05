# Codex Philosopher Atlas — Architecture Guide

## What This Repository Runs

This repository implements Philosopher Atlas on top of Codex CLI.

The architecture is still:

Planning Loop
→ Strategizer
→ Explorer / Math Explorer
→ Curator / Receptionist support

The difference is operational:

- Claude-specific session commands are gone
- every runnable role is a Codex role prompt
- all orchestration happens through local wrapper scripts
- monitoring is file- and status-based, not pane-text-based

## Runtime Rules

- The repository root is the Codex workspace root for launched runs.
- The requested operational workdir is passed to each role in its prompt and
  status metadata.
- All writes must remain inside this repository.
- Use the launcher scripts, not raw `codex exec`, from within role prompts:
  - `$CODEX_PATLAS_ROOT/bin/run-role.sh`
  - `$CODEX_PATLAS_ROOT/bin/launch-role.sh`
  - `$CODEX_PATLAS_ROOT/bin/monitor-sessions.sh`

## Planning Roles

The planning loop is split into dedicated runnable prompts:

- `planner`
- `selector`
- `attacker`
- `judge`
- `final-decider`

Each planning run writes its working artifacts under
`missions/<mission>/planning-runs/run-NNN/`.

The final decider produces `winning-chain.md`, which is copied into
`CHAIN.md`, and its rationale is appended to `CHAIN-HISTORY.md`.

## Step Execution

The strategizer remains step-scoped. It operates inside a mission step
directory, reads `GOAL.md`, decides how many explorations to run, launches
explorer sessions, synthesizes results, and writes `RESULTS.md`.

Explorers still produce:

- `REPORT.md`
- `REPORT-SUMMARY.md`
- `code/` artifacts when computation or formalization is involved

## Monitoring Model

Monitoring in the Codex fork is intentionally conservative:

- status is derived from `runtime/status/*.json`
- logs live in `runtime/logs/`
- final messages live in `runtime/results/`
- sentinel files such as `REPORT-SUMMARY.md` and `RESULTS.md` confirm
  completion

The V1 monitor never nudges, restarts, or sends interactive messages into a
live run.
