#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

ensure_runtime_dirs

STALE_SECONDS="${STALE_SECONDS:-900}"
STATUS_GLOB=("$ATLAS_ROOT/runtime/status/"*.json)

printf "%-42s %-15s %-10s %s\n" "Session" "Role" "Status" "Notes"
printf "%-42s %-15s %-10s %s\n" "------------------------------------------" "---------------" "----------" "------------------------------"

if [[ ! -e "${STATUS_GLOB[0]}" ]]; then
  echo "No runtime status files found."
  exit 0
fi

for status_file in "${STATUS_GLOB[@]}"; do
  [[ -f "$status_file" ]] || continue

  session_name="$(status_field "$status_file" session_name)"
  role="$(status_field "$status_file" role)"
  state="$(status_field "$status_file" state)"
  workdir="$(status_field "$status_file" operational_workdir)"
  log_file="$(status_field "$status_file" log_file)"
  sentinel_file="$(status_field "$status_file" sentinel_file)"
  note=""
  derived_status="$state"

  tmux_running="no"
  if tmux has-session -t "$session_name" 2>/dev/null; then
    tmux_running="yes"
  fi

  if [[ "$state" == "error" ]]; then
    note="$(status_field "$status_file" error_message)"
  elif [[ "$state" == "queued" ]]; then
    derived_status="queued"
    note="waiting for dispatcher"
  elif [[ "$state" == "done" && -n "$sentinel_file" && -f "$sentinel_file" ]]; then
    derived_status="done"
    note="sentinel present"
  else
    if [[ -n "$log_file" && -f "$log_file" ]]; then
      now_epoch="$(date +%s)"
      log_epoch="$(stat -f %m "$log_file")"
      age="$(( now_epoch - log_epoch ))"
      if [[ "$tmux_running" == "yes" && "$age" -le "$STALE_SECONDS" ]]; then
        derived_status="active"
        note="tmux live, log age ${age}s"
      elif [[ "$tmux_running" == "yes" ]]; then
        derived_status="stale"
        note="tmux live, log age ${age}s"
      elif [[ "$state" == "done" ]]; then
        derived_status="done"
        note="completed, tmux exited"
      else
        derived_status="stale"
        note="tmux gone, no sentinel"
      fi
    else
      if [[ "$tmux_running" == "yes" ]]; then
        derived_status="active"
        note="tmux live, no log yet"
      else
        derived_status="$state"
        note="no log file"
      fi
    fi
  fi

  if [[ -z "$note" ]]; then
    note="$workdir"
  else
    note="$note | $workdir"
  fi

  printf "%-42s %-15s %-10s %s\n" "$session_name" "$role" "$derived_status" "$note"
done
