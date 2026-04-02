#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATLAS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SESSION_PREFIX="codex-patlas"

fail() {
  echo "Error: $*" >&2
  exit 1
}

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

compact_timestamp() {
  date -u +"%Y%m%dT%H%M%SZ"
}

sanitize_token() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-'
}

ensure_runtime_dirs() {
  mkdir -p \
    "$PATLAS_ROOT/runtime/status" \
    "$PATLAS_ROOT/runtime/logs" \
    "$PATLAS_ROOT/runtime/results" \
    "$PATLAS_ROOT/runtime/tasks" \
    "$PATLAS_ROOT/runtime/tmp" \
    "$PATLAS_ROOT/runtime/requests/pending" \
    "$PATLAS_ROOT/runtime/requests/running" \
    "$PATLAS_ROOT/runtime/requests/completed" \
    "$PATLAS_ROOT/runtime/requests/failed"
}

nested_role_execution() {
  [[ -n "${CODEX_PATLAS_SESSION_NAME:-}" && -z "${CODEX_PATLAS_FORCE_DIRECT:-}" ]]
}

abspath() {
  python3 - "$1" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
}

ensure_inside_repo() {
  local target="$1"
  case "$target" in
    "$PATLAS_ROOT"/*|"$PATLAS_ROOT") ;;
    *)
      fail "Path must stay inside $PATLAS_ROOT: $target"
      ;;
  esac
}

role_prompt_path() {
  local role="$1"
  case "$role" in
    philosopher|planner|selector|attacker|judge|final-decider|strategizer|explorer|math-explorer|step-evaluator)
      printf '%s/agents/%s/system-prompt.md\n' "$PATLAS_ROOT" "$role"
      ;;
    receptionist)
      printf '%s/library/receptionist/system-prompt.md\n' "$PATLAS_ROOT"
      ;;
    curator)
      printf '%s/library/curator/system-prompt.md\n' "$PATLAS_ROOT"
      ;;
    babysitter)
      printf '%s/babysitter/system-prompt.md\n' "$PATLAS_ROOT"
      ;;
    idea-validator)
      printf '%s/idea-exploration/agents/idea-validator/system-prompt.md\n' "$PATLAS_ROOT"
      ;;
    idea-creator)
      printf '%s/idea-exploration/agents/idea-creator/system-prompt.md\n' "$PATLAS_ROOT"
      ;;
    *)
      fail "Unknown role: $role"
      ;;
  esac
}

default_model_for_role() {
  local role="$1"
  case "$role" in
    receptionist|babysitter)
      printf 'gpt-5.4-mini\n'
      ;;
    *)
      printf 'gpt-5.4\n'
      ;;
  esac
}

role_uses_search() {
  local role="$1"
  case "$role" in
    receptionist|curator|babysitter|step-evaluator)
      return 1
      ;;
    *)
      return 0
      ;;
  esac
}

status_field() {
  local file="$1"
  local field="$2"
  python3 - "$file" "$field" <<'PY'
import json
import sys
path, field = sys.argv[1:3]
with open(path) as fh:
    data = json.load(fh)
value = data.get(field, "")
if isinstance(value, bool):
    print("true" if value else "false")
else:
    print(value)
PY
}

write_status_json() {
  local file="$1"
  python3 - "$file" <<'PY'
import json
import os
import sys

path = sys.argv[1]
fields = {
    "session_name": os.environ.get("STATUS_SESSION_NAME", ""),
    "role": os.environ.get("STATUS_ROLE", ""),
    "model": os.environ.get("STATUS_MODEL", ""),
    "state": os.environ.get("STATUS_STATE", ""),
    "workspace_root": os.environ.get("STATUS_WORKSPACE_ROOT", ""),
    "operational_workdir": os.environ.get("STATUS_OPERATIONAL_WORKDIR", ""),
    "prompt_file": os.environ.get("STATUS_PROMPT_FILE", ""),
    "task_file": os.environ.get("STATUS_TASK_FILE", ""),
    "result_file": os.environ.get("STATUS_RESULT_FILE", ""),
    "log_file": os.environ.get("STATUS_LOG_FILE", ""),
    "sentinel_file": os.environ.get("STATUS_SENTINEL_FILE", ""),
    "session_prefix": os.environ.get("STATUS_SESSION_PREFIX", ""),
    "started_at": os.environ.get("STATUS_STARTED_AT", ""),
    "finished_at": os.environ.get("STATUS_FINISHED_AT", ""),
    "last_updated": os.environ.get("STATUS_LAST_UPDATED", ""),
    "search_enabled": os.environ.get("STATUS_SEARCH_ENABLED", ""),
    "error_message": os.environ.get("STATUS_ERROR_MESSAGE", ""),
}
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fields, fh, indent=2, sort_keys=True)
    fh.write("\n")
PY
}

wait_for_status_terminal_state() {
  local status_file="$1"
  local timeout_seconds="${2:-7200}"
  local start_epoch
  start_epoch="$(date +%s)"

  while true; do
    if [[ ! -f "$status_file" ]]; then
      sleep 2
      continue
    fi

    local state
    state="$(status_field "$status_file" state)"
    case "$state" in
      done)
        return 0
        ;;
      error)
        return 1
        ;;
    esac

    if (( "$(date +%s)" - start_epoch > timeout_seconds )); then
      return 2
    fi

    sleep 5
  done
}
