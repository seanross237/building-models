#!/usr/bin/env bash

set -euo pipefail

DROR_ROOT="${1:?Usage: babysitter.sh <dror-root> <session-prefix>}"
PREFIX="${2:?Usage: babysitter.sh <dror-root> <session-prefix>}"

CHECK_INTERVAL=180
TREE_LOG="$DROR_ROOT/_index/tree.jsonl"

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  printf '[%s] %s\n' "$(timestamp_utc)" "$*"
}

session_names() {
  tmux list-sessions -F '#{session_name}' 2>/dev/null | grep "^${PREFIX}-" | grep -v "^${PREFIX}-operator$" | grep -v "^${PREFIX}-babysitter$" || true
}

node_path_for_session() {
  local session="$1"
  grep -F "\"session\":\"$session\"" "$TREE_LOG" 2>/dev/null | tail -n 1 | sed -n 's/.*"path":"\([^"]*\)".*/\1/p'
}

mark_failed() {
  local node_dir="$1"
  local session="$2"
  local pane_command="$3"

  if [[ -f "$node_dir/DONE" || -f "$node_dir/WAITING-FOR-CHILDREN" || -f "$node_dir/FAILED" ]]; then
    return 0
  fi

  {
    printf 'timestamp: %s\n' "$(timestamp_utc)"
    printf 'session: %s\n' "$session"
    printf 'reason: codex process appears to have exited without DONE or WAITING-FOR-CHILDREN\n'
    printf 'pane_current_command: %s\n' "$pane_command"
    printf 'last_50_lines_of_run_log:\n'
    tail -n 50 "$node_dir/run.log" 2>/dev/null || true
  } > "$node_dir/FAILED"

  log "Marked FAILED: ${node_dir#"$DROR_ROOT"/} ($session)"
}

log "Babysitter started"
log "DROR_ROOT=$DROR_ROOT PREFIX=$PREFIX CHECK_INTERVAL=${CHECK_INTERVAL}s"

while true; do
  sessions=()
  while IFS= read -r session; do
    [[ -n "$session" ]] || continue
    sessions+=("$session")
  done < <(session_names)

  for session in "${sessions[@]}"; do
    rel_path="$(node_path_for_session "$session")"
    if [[ -z "$rel_path" ]]; then
      continue
    fi

    node_dir="$DROR_ROOT/$rel_path"
    if [[ ! -d "$node_dir" ]]; then
      continue
    fi

    pane_command="$(tmux list-panes -t "$session" -F '#{pane_current_command}' 2>/dev/null | head -n 1 || true)"
    if [[ "$pane_command" != "sleep" ]]; then
      continue
    fi

    mark_failed "$node_dir" "$session" "$pane_command"
  done

  sleep "$CHECK_INTERVAL"
done
