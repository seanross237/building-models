# Codex Philosopher Atlas — Quick Reference

This file is retained only as a copied quick-reference entrypoint from the
original folder. In this fork, the active operator guide is [README.md](README.md).

## Runtime

- Repository root: this folder only
- Session prefix: `codex-patlas-`
- Launcher scripts:
  - `bin/run-role.sh`
  - `bin/launch-role.sh`
  - `bin/start-planning-run.sh`
  - `bin/start-step.sh`
  - `bin/monitor-sessions.sh`

## Key Locations

- Architecture guide: `agents/philosopher/system-prompt.md`
- Runnable planning prompts: `agents/planner/`, `agents/selector/`,
  `agents/attacker/`, `agents/judge/`, `agents/final-decider/`
- Execution prompts: `agents/strategizer/`, `agents/explorer/`,
  `agents/math-explorer/`
- Support prompts: `library/receptionist/`, `library/curator/`,
  `babysitter/`
- Missions: `missions/`
- Local shared resources: `idea-exploration/`, `available-tools.md`,
  `promising-findings.md`

## Model Defaults

- `gpt-5.4`: planner, selector, attacker, judge, final decider,
  strategizer, explorer, math explorer, curator
- `gpt-5.4-mini`: receptionist, babysitter
