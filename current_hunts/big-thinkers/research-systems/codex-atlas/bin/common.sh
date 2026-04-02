#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ATLAS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SESSION_PREFIX="codex-atlas"

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
    "$ATLAS_ROOT/runtime/status" \
    "$ATLAS_ROOT/runtime/logs" \
    "$ATLAS_ROOT/runtime/results" \
    "$ATLAS_ROOT/runtime/tasks" \
    "$ATLAS_ROOT/runtime/tmp" \
    "$ATLAS_ROOT/runtime/requests/pending" \
    "$ATLAS_ROOT/runtime/requests/running" \
    "$ATLAS_ROOT/runtime/requests/completed" \
    "$ATLAS_ROOT/runtime/requests/failed"
}

nested_role_execution() {
  [[ -n "${CODEX_ATLAS_SESSION_NAME:-}" && -z "${CODEX_ATLAS_FORCE_DIRECT:-}" ]]
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
    "$ATLAS_ROOT"/*|"$ATLAS_ROOT") ;;
    *)
      fail "Path must stay inside $ATLAS_ROOT: $target"
      ;;
  esac
}

role_prompt_path() {
  local role="$1"
  case "$role" in
    missionary|strategizer|explorer|math-explorer|scribe)
      printf '%s/execution/agents/%s/system-prompt.md\n' "$ATLAS_ROOT" "$role"
      ;;
    receptionist)
      printf '%s/execution/agents/library/receptionist/system-prompt.md\n' "$ATLAS_ROOT"
      ;;
    curator)
      printf '%s/execution/agents/library/curator/system-prompt.md\n' "$ATLAS_ROOT"
      ;;
    babysitter)
      printf '%s/execution/babysitter/system-prompt.md\n' "$ATLAS_ROOT"
      ;;
    idea-validator)
      printf '%s/idea-exploration/agents/idea-validator/system-prompt.md\n' "$ATLAS_ROOT"
      ;;
    idea-creator)
      printf '%s/idea-exploration/agents/idea-creator/system-prompt.md\n' "$ATLAS_ROOT"
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
    receptionist|curator|babysitter|scribe)
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
