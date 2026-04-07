#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DROR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PREFIX="dror"

list_prefix_sessions() {
  tmux list-sessions -F '#{session_name}' 2>/dev/null | grep "^${PREFIX}-" || true
}

sessions=()
while IFS= read -r session; do
  [[ -n "$session" ]] || continue
  sessions+=("$session")
done < <(list_prefix_sessions)

if ((${#sessions[@]} == 0)); then
  printf 'No %s-* tmux sessions found.\n' "$PREFIX"
else
  printf 'Killing %s tmux sessions:\n' "$PREFIX"
  session_count=0
  for session in "${sessions[@]}"; do
    printf '  - %s\n' "$session"
    tmux kill-session -t "$session" 2>/dev/null || true
    session_count=$((session_count + 1))
  done
  printf 'Killed %s session(s).\n' "$session_count"
fi

orphan_codex="$(pgrep -lf 'codex exec' | grep -i dror || true)"
if [[ -n "$orphan_codex" ]]; then
  printf '\nWarning: possible orphan Codex processes remain for %s:\n' "$DROR_ROOT"
  printf '%s\n' "$orphan_codex"
  printf 'Kill specific PIDs manually if needed.\n'
fi

exit 0
