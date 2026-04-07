# dror-isreal runtime

These scripts run the tmux-hosted Codex orchestrator for the `dror-isreal`
knowledge tree. They do not launch themselves automatically; use them from
the repo root or via `bash run/<script>.sh`.

## Files

- `launch.sh` — clean start. Kills existing `dror-*` tmux sessions, removes
  stale non-terminal sentinels, creates `run/logs/`, and starts the operator
  plus babysitter sessions.
- `operator.sh` — the pure-bash state machine. It walks `tree/`, decides
  which nodes are fresh, waiting, blocked, failed, or ready to synthesize,
  and spawns Codex in detached tmux sessions.
- `babysitter.sh` — zero-LLM safety net. It checks agent sessions and marks a
  node `FAILED` if the Codex process has exited into the tail `sleep 120`
  without producing `DONE` or `WAITING-FOR-CHILDREN`.
- `teardown.sh` — kills only `dror-*` tmux sessions and prints any matching
  orphan `codex exec` processes so you can decide whether to kill them.

## Codex invocation

The operator uses `codex --search exec ...` instead of `codex exec --search`
because this local CLI accepts `--search` only as a top-level option before
the `exec` subcommand. Prompts are piped on stdin, so the Atlas
`tmux send-keys` 800-character workaround is not needed here.

## Usage

From the repo root:

```bash
bash run/launch.sh
tmux attach -t dror-operator
find tree -name DONE | wc -l
bash run/teardown.sh
```

## Logs

- `run/logs/operator.log`
- `run/logs/babysitter.log`
- `<node>/run.log` for each spawned branch or leaf agent
