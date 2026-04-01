# Codex Philosopher Atlas — Overview

## What It Is

`codex-philosopher-atlas` is a self-contained Codex-native fork of
Philosopher Atlas. It keeps the wide-funnel adversarial planning loop and the
step-scoped strategizer/explorer workflow, but replaces Claude-specific
session handling with local `codex exec` launchers, runtime status files, and
`tmux` sessions under a distinct namespace.

## How It Works

Wide Funnel Planning Loop:

Planner
→ Selector
→ 3x Attacker (parallel)
→ 3x Judge (parallel)
→ Final Decider
→ Strategizer executes Step 1
→ Results back to Planning Loop
→ Evaluate: replan / proceed / kill
→ Repeat until chain complete or killed

## Codex Runtime Model

- Every runnable role is launched through `bin/run-role.sh` or
  `bin/launch-role.sh`.
- All sessions use the prefix `codex-patlas-`.
- Runtime metadata is written to:
  - `runtime/status/`
  - `runtime/logs/`
  - `runtime/results/`
- Planning loop runs write intermediate outputs to
  `missions/<mission>/planning-runs/run-NNN/`.
- The launcher uses this repository root as the Codex workspace root so roles
  can write across mission, library, and inbox directories while still staying
  inside this fork.

## Planning Loop

The planning loop is now directly runnable. Each mission planning round writes:

- `mission-context.md`
- `planner.md`
- `planner-chains/chain-*.md`
- `selector.md`
- `selected/chain-*.md`
- `attacks/chain-*.md`
- `judgments/chain-*.md`
- `refined/chain-*.md`
- `final-decider.md`
- `winning-chain.md`

`CHAIN.md` remains the canonical active chain for a mission, and
`CHAIN-HISTORY.md` remains the append-only history.

## Strategizer and Explorers

The strategizer still owns one scoped step at a time. It can:

- query the local receptionist synchronously through `bin/run-role.sh`
- launch explorers and curator sessions through `bin/launch-role.sh`
- monitor explorer completion through sentinel files such as
  `REPORT-SUMMARY.md`

Explorers still write:

- `REPORT.md`
- `REPORT-SUMMARY.md`
- optional `code/` artifacts for reproducible computation

## Monitoring

The Codex fork drops Claude-pane heuristics entirely. Monitoring is based on:

- launcher-written status files
- log freshness
- tmux session existence
- sentinel outputs such as `REPORT-SUMMARY.md` and `RESULTS.md`

V1 monitoring is observe-only. It classifies sessions as active, done, stale,
or error, but does not nudge or restart them.

## Local Resources

This fork vendors the small shared resources it used to reference externally:

- `idea-exploration/`
- `available-tools.md`
- `promising-findings.md`

The fork is intended to run entirely from this folder without touching the
original `philosopher-atlas` or any sibling project.
