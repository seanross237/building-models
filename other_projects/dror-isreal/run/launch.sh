#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DROR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PREFIX="dror"
LOG_DIR="$DROR_ROOT/run/logs"

list_prefix_sessions() {
  tmux list-sessions -F '#{session_name}' 2>/dev/null | grep "^${PREFIX}-" || true
}

kill_prefix_sessions() {
  local sessions=()
  local session
  while IFS= read -r session; do
    [[ -n "$session" ]] || continue
    sessions+=("$session")
  done < <(list_prefix_sessions)
  if ((${#sessions[@]} == 0)); then
    return 0
  fi

  for session in "${sessions[@]}"; do
    tmux kill-session -t "$session" 2>/dev/null || true
  done
}

remove_stale_sentinels() {
  local name="$1"
  local matches=()
  local match
  while IFS= read -r match; do
    [[ -n "$match" ]] || continue
    matches+=("$match")
  done < <(find "$DROR_ROOT/tree" -type f -name "$name" | sort)
  if ((${#matches[@]} == 0)); then
    printf '0'
    return 0
  fi

  for match in "${matches[@]}"; do
    rm -f "$match"
  done

  printf '%s' "${#matches[@]}"
}

mkdir -p "$LOG_DIR"

existing_sessions=()
while IFS= read -r session; do
  [[ -n "$session" ]] || continue
  existing_sessions+=("$session")
done < <(list_prefix_sessions)
fresh_scope_count="$(find "$DROR_ROOT/tree" -type f -name SCOPE.md | wc -l | tr -d ' ')"
root_branch_count="$(find "$DROR_ROOT/tree" -mindepth 2 -maxdepth 2 -type f -name SCOPE.md | wc -l | tr -d ' ')"

printf 'DROR root: %s\n' "$DROR_ROOT"
printf 'Prefix: %s\n' "$PREFIX"
printf 'Tree nodes with SCOPE.md: %s\n' "$fresh_scope_count"
printf 'Direct root-domain nodes already seeded: %s\n' "$root_branch_count"
printf 'Existing %s-* tmux sessions to kill: %s\n' "$PREFIX" "${#existing_sessions[@]}"

kill_prefix_sessions

launched_removed="$(remove_stale_sentinels LAUNCHED)"
waiting_removed="$(remove_stale_sentinels WAITING-FOR-CHILDREN)"
failed_removed="$(remove_stale_sentinels FAILED)"

printf 'Removed stale sentinels: LAUNCHED=%s WAITING-FOR-CHILDREN=%s FAILED=%s\n' \
  "$launched_removed" "$waiting_removed" "$failed_removed"

tmux new-session -d -s "${PREFIX}-operator" -c "$DROR_ROOT" \
  "bash run/operator.sh '$DROR_ROOT' '$PREFIX' 2>&1 | tee -a run/logs/operator.log"

tmux new-session -d -s "${PREFIX}-babysitter" -c "$DROR_ROOT" \
  "bash run/babysitter.sh '$DROR_ROOT' '$PREFIX' 2>&1 | tee -a run/logs/babysitter.log"

printf '\n'
printf 'Launched tmux sessions:\n'
printf '  - %s-operator\n' "$PREFIX"
printf '  - %s-babysitter\n' "$PREFIX"
printf '\n'
printf 'Useful commands:\n'
printf '  tmux attach -t %s-operator\n' "$PREFIX"
printf '  find tree -name DONE | wc -l\n'
printf '  bash run/teardown.sh\n'
