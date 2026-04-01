#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

MODE="${1:---once}"
SLEEP_SECONDS="${DISPATCHER_POLL_SECONDS:-2}"

ensure_runtime_dirs

process_request() {
  local pending_file="$1"
  local base_name
  base_name="$(basename "$pending_file")"
  local running_file="$PATLAS_ROOT/runtime/requests/running/$base_name"
  local completed_file="$PATLAS_ROOT/runtime/requests/completed/$base_name"
  local failed_file="$PATLAS_ROOT/runtime/requests/failed/$base_name"

  if ! mv "$pending_file" "$running_file" 2>/dev/null; then
    return 0
  fi

  local kind role workdir model task_file session_name sentinel_file
  kind="$(status_field "$running_file" kind)"
  role="$(status_field "$running_file" role)"
  workdir="$(status_field "$running_file" workdir)"
  model="$(status_field "$running_file" model)"
  task_file="$(status_field "$running_file" task_file)"
  session_name="$(status_field "$running_file" session_name)"
  sentinel_file="$(status_field "$running_file" sentinel_file)"

  local cmd=()
  local exit_code=0

  if [[ "$kind" == "run" ]]; then
    cmd=(
      "$PATLAS_ROOT/bin/run-role.sh"
      --role "$role"
      --workdir "$workdir"
      --model "$model"
      --session-name "$session_name"
      --status-file "$PATLAS_ROOT/runtime/status/${session_name}.json"
      --result-file "$PATLAS_ROOT/runtime/results/${session_name}.md"
      --log-file "$PATLAS_ROOT/runtime/logs/${session_name}.log"
    )
  elif [[ "$kind" == "launch" ]]; then
    cmd=(
      "$PATLAS_ROOT/bin/launch-role.sh"
      --role "$role"
      --workdir "$workdir"
      --model "$model"
      --session-name "$session_name"
    )
  else
    mv "$running_file" "$failed_file"
    return 1
  fi

  if [[ -n "$task_file" ]]; then
    cmd+=(--task-file "$task_file")
  fi
  if [[ -n "$sentinel_file" ]]; then
    cmd+=(--sentinel-file "$sentinel_file")
  fi

  CODEX_PATLAS_FORCE_DIRECT=1 "${cmd[@]}" || exit_code=$?

  if [[ $exit_code -eq 0 ]]; then
    mv "$running_file" "$completed_file"
  else
    mv "$running_file" "$failed_file"
  fi
}

process_pending_once() {
  local request found=0
  for request in "$PATLAS_ROOT"/runtime/requests/pending/*.json; do
    [[ -f "$request" ]] || continue
    found=1
    process_request "$request"
  done
  return "$found"
}

case "$MODE" in
  --once)
    process_pending_once || true
    ;;
  --loop)
    while true; do
      process_pending_once || true
      sleep "$SLEEP_SECONDS"
    done
    ;;
  *)
    fail "Usage: bin/dispatch-requests.sh [--once|--loop]"
    ;;
esac
