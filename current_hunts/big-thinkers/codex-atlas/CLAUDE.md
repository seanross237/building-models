# Codex Atlas — Quick Reference

The active operator guide for this fork is [README.md](README.md), with
additional detail in [atlas-overview.md](atlas-overview.md).

## Runtime

- Repository root: this folder only
- Session prefix: `codex-atlas-`
- Launcher scripts:
  - `bin/start-mission.sh`
  - `bin/start-strategy.sh`
  - `bin/run-role.sh`
  - `bin/launch-role.sh`
  - `bin/monitor-sessions.sh`

## Key Locations

- Overview: `atlas-overview.md`
- Missions: `execution/instances/`
- Role prompts: `execution/agents/`
- Shared library: `execution/agents/library/`
- Shared local resources: `available-tools.md`, `promising-findings.md`,
  `idea-exploration/`

## Model Defaults

- `gpt-5.4`: missionary, strategizer, explorer, math-explorer, curator
- `gpt-5.4-mini`: receptionist, babysitter

## Briefing

When Sean asks to "open the briefing", "run the briefing", "briefing", or
similar:

1. Start the dev server in the background: `cd organization/briefing && npm run dev`
2. Wait a couple seconds for it to start
3. Open the browser: `open http://localhost:5173`

If port `5173` is taken, check the dev server output for the actual port and
open that instead.
