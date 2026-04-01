# Codex Atlas — Agent Loop Architecture

## Goal

Codex Atlas keeps the original Atlas hierarchy:

- Missionary
- Strategizer
- Explorer / Math Explorer
- Receptionist / Curator / Babysitter support

The change is operational rather than conceptual. The old Claude-specific
operator flow is replaced by local Codex launcher scripts, structured runtime
status files, and sentinel-file completion.

## Runtime Rules

- Repository root: this folder
- Codex workspace root for launched runs: this folder
- Operational workdir: passed into each role via prompt and status metadata
- All writes must stay inside this repository
- Use the local launcher scripts instead of raw `codex exec` inside role prompts:
  - `bin/run-role.sh`
  - `bin/launch-role.sh`
  - `bin/monitor-sessions.sh`

## Launching

Mission-level pass:

```bash
bin/start-mission.sh <mission-name>
```

This launches the Missionary against
`execution/instances/<mission-name>/`. The Missionary is responsible for taking
the next mission-level action: evaluate a completed strategy, write the next
`STRATEGY.md`, set up the scaffold if needed, and launch the Strategizer.

Strategy-level execution:

```bash
bin/start-strategy.sh <mission-name> <strategy-001>
```

This launches the Strategizer against an existing strategy directory and waits
for `FINAL-REPORT.md` as the completion sentinel.

Direct roles:

```bash
bin/launch-role.sh --role explorer --workdir execution/instances/foo/strategies/strategy-001/explorations/exploration-001 --task-file runtime/tasks/example.md
bin/run-role.sh --role receptionist --workdir execution/agents/library --task-file runtime/tasks/library-query.md
```

## Mission Flow

1. The Missionary reads `MISSION.md`, `MISSION-VALIDATION-GUIDE.md`, prior
   strategy outputs, and the missionary meta library.
2. It writes or updates the next strategy, ensures the scaffold exists, and
   launches a Strategizer.
3. The Strategizer runs the exploration loop:
   - query the Receptionist
   - write `GOAL.md`
   - launch Explorers / Math Explorers
   - process `REPORT.md` and `REPORT-SUMMARY.md`
   - hand findings to the Curator
   - continue until it writes `FINAL-REPORT.md`
4. The Missionary evaluates the completed strategy and either:
   - writes `MISSION-COMPLETE.md`, or
   - writes the next `STRATEGY.md` and launches the next Strategizer

## Runtime Layout

- `runtime/status/<session>.json` — session metadata and state
- `runtime/logs/<session>.log` — launcher stdout/stderr
- `runtime/results/<session>.md` — final assistant message
- `runtime/tasks/` — orchestration task files
- `runtime/requests/` — nested launch queue used when one role launches another

## Key Directories

- `execution/instances/` — mission instances and strategy histories
- `execution/agents/` — active role prompts
- `execution/agents/library/` — factual and meta libraries
- `execution/babysitter/` — monitor prompt and historical babysitter data
- `idea-exploration/` — local copy of shared mission ideas

## Monitoring

Use:

```bash
bin/monitor-sessions.sh
```

Status is derived from `runtime/status/*.json`, log recency, tmux session
presence, and sentinel outputs such as `REPORT-SUMMARY.md`, `FINAL-REPORT.md`,
and `MISSION-COMPLETE.md`.

## Legacy Material

The copied `execution/operator/`, older tmux notes, and historical Atlas docs
remain in this fork as reference data. The active runtime path for Codex Atlas
is the local `bin/` launcher layer plus the rewritten role prompts.
