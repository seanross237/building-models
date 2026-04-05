# Codex Atlas

`codex-atlas` is a Codex-native fork of `atlas`.
It preserves Atlas's mission, strategy, exploration, and library structure, but
swaps the old Claude/operator flow for a local `codex exec` + `tmux` runtime
that lives entirely inside this folder.

## What Changed

- Runnable roles now launch through `bin/run-role.sh` and `bin/launch-role.sh`.
- Sessions use the `codex-atlas-*` prefix.
- The active runtime is file- and status-driven under `runtime/`.
- Shared local resources that Atlas used from the wider repo now have local
  copies:
  - `available-tools.md`
  - `promising-findings.md`
  - `idea-exploration/`
- The copied `execution/operator/` and older tmux/Claude docs remain as
  historical reference, not as the primary runtime.

## Launch Commands

Mission-level control:

```bash
bin/start-mission.sh <mission-name>
```

Run an existing strategy directly:

```bash
bin/start-strategy.sh <mission-name> <strategy-001>
```

Monitor runtime status:

```bash
bin/monitor-sessions.sh
```

Direct role launches:

```bash
bin/launch-role.sh --role explorer --workdir execution/instances/foo/strategies/strategy-001/explorations/exploration-001 --task-file runtime/tasks/example.md
bin/run-role.sh --role receptionist --workdir execution/agents/library --task-file runtime/tasks/library-query.md
```

## Runtime Layout

- `runtime/status/<session>.json` — structured session metadata
- `runtime/logs/<session>.log` — launcher stdout/stderr
- `runtime/results/<session>.md` — final assistant message from the Codex run
- `runtime/tasks/` — generated orchestration task files
- `runtime/tmp/` — helper scripts and prompt bundles

## Codex Workspace Note

Launched runs use this repository root as the Codex workspace root. The
requested operational workdir is passed into the role prompt and status
metadata, so roles can still work inside mission, strategy, and exploration
directories without losing access to the shared Atlas library.
