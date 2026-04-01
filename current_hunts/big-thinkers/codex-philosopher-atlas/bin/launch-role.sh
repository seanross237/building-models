#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

ROLE=""
WORKDIR=""
TASK_FILE=""
MODEL=""
SESSION_NAME=""
SENTINEL_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role)
      ROLE="$2"
      shift 2
      ;;
    --workdir)
      WORKDIR="$2"
      shift 2
      ;;
    --task-file)
      TASK_FILE="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --session-name)
      SESSION_NAME="$2"
      shift 2
      ;;
    --sentinel-file)
      SENTINEL_FILE="$2"
      shift 2
      ;;
    *)
      fail "Unknown argument: $1"
      ;;
  esac
done

[[ -n "$ROLE" ]] || fail "--role is required"
[[ -n "$WORKDIR" ]] || fail "--workdir is required"

ensure_runtime_dirs

WORKDIR_ABS="$(abspath "$WORKDIR")"
ensure_inside_repo "$WORKDIR_ABS"

if [[ -n "$TASK_FILE" ]]; then
  TASK_FILE_ABS="$(abspath "$TASK_FILE")"
  ensure_inside_repo "$TASK_FILE_ABS"
else
  TASK_FILE_ABS=""
fi

if [[ -n "$SENTINEL_FILE" ]]; then
  SENTINEL_FILE_ABS="$(abspath "$SENTINEL_FILE")"
  ensure_inside_repo "$SENTINEL_FILE_ABS"
else
  SENTINEL_FILE_ABS=""
fi

MODEL="${MODEL:-$(default_model_for_role "$ROLE")}"
if [[ -z "$SESSION_NAME" ]]; then
  SESSION_NAME="${SESSION_PREFIX}-$(sanitize_token "$ROLE")-$(compact_timestamp)"
fi

STATUS_FILE="$PATLAS_ROOT/runtime/status/${SESSION_NAME}.json"
RESULT_FILE="$PATLAS_ROOT/runtime/results/${SESSION_NAME}.md"
LOG_FILE="$PATLAS_ROOT/runtime/logs/${SESSION_NAME}.log"
RUNNER_FILE="$PATLAS_ROOT/runtime/tmp/${SESSION_NAME}.sh"

if nested_role_execution; then
  export STATUS_SESSION_NAME="$SESSION_NAME"
  export STATUS_ROLE="$ROLE"
  export STATUS_MODEL="$MODEL"
  export STATUS_STATE="queued"
  export STATUS_WORKSPACE_ROOT="$PATLAS_ROOT"
  export STATUS_OPERATIONAL_WORKDIR="$WORKDIR_ABS"
  export STATUS_PROMPT_FILE="$(role_prompt_path "$ROLE")"
  export STATUS_TASK_FILE="$TASK_FILE_ABS"
  export STATUS_RESULT_FILE="$RESULT_FILE"
  export STATUS_LOG_FILE="$LOG_FILE"
  export STATUS_SENTINEL_FILE="$SENTINEL_FILE_ABS"
  export STATUS_SESSION_PREFIX="$SESSION_PREFIX"
  export STATUS_STARTED_AT="$(timestamp_utc)"
  export STATUS_FINISHED_AT=""
  export STATUS_LAST_UPDATED="$STATUS_STARTED_AT"
  if role_uses_search "$ROLE"; then
    export STATUS_SEARCH_ENABLED="true"
  else
    export STATUS_SEARCH_ENABLED="false"
  fi
  export STATUS_ERROR_MESSAGE=""
  write_status_json "$STATUS_FILE"

  REQUEST_FILE="$PATLAS_ROOT/runtime/requests/pending/${SESSION_NAME}.json"
  python3 - "$REQUEST_FILE" <<'PY'
import json
import os
import sys

path = sys.argv[1]
payload = {
    "kind": "launch",
    "requested_at": os.environ["STATUS_STARTED_AT"],
    "role": os.environ["STATUS_ROLE"],
    "workdir": os.environ["STATUS_OPERATIONAL_WORKDIR"],
    "model": os.environ["STATUS_MODEL"],
    "task_file": os.environ["STATUS_TASK_FILE"],
    "session_name": os.environ["STATUS_SESSION_NAME"],
    "sentinel_file": os.environ["STATUS_SENTINEL_FILE"],
}
with open(path, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, sort_keys=True)
    fh.write("\n")
PY

  echo "session_name=$SESSION_NAME"
  echo "status_file=$STATUS_FILE"
  echo "result_file=$RESULT_FILE"
  echo "log_file=$LOG_FILE"
  exit 0
fi

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  fail "tmux session already exists: $SESSION_NAME"
fi

export STATUS_SESSION_NAME="$SESSION_NAME"
export STATUS_ROLE="$ROLE"
export STATUS_MODEL="$MODEL"
export STATUS_STATE="active"
export STATUS_WORKSPACE_ROOT="$PATLAS_ROOT"
export STATUS_OPERATIONAL_WORKDIR="$WORKDIR_ABS"
export STATUS_PROMPT_FILE="$(role_prompt_path "$ROLE")"
export STATUS_TASK_FILE="$TASK_FILE_ABS"
export STATUS_RESULT_FILE="$RESULT_FILE"
export STATUS_LOG_FILE="$LOG_FILE"
export STATUS_SENTINEL_FILE="$SENTINEL_FILE_ABS"
export STATUS_SESSION_PREFIX="$SESSION_PREFIX"
export STATUS_STARTED_AT="$(timestamp_utc)"
export STATUS_FINISHED_AT=""
export STATUS_LAST_UPDATED="$STATUS_STARTED_AT"
if role_uses_search "$ROLE"; then
  export STATUS_SEARCH_ENABLED="true"
else
  export STATUS_SEARCH_ENABLED="false"
fi
export STATUS_ERROR_MESSAGE=""
write_status_json "$STATUS_FILE"

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf 'exec %q --role %q --workdir %q --model %q --session-name %q --status-file %q --result-file %q --log-file %q' \
    "$PATLAS_ROOT/bin/run-role.sh" \
    "$ROLE" \
    "$WORKDIR_ABS" \
    "$MODEL" \
    "$SESSION_NAME" \
    "$STATUS_FILE" \
    "$RESULT_FILE" \
    "$LOG_FILE"
  if [[ -n "$TASK_FILE_ABS" ]]; then
    printf ' --task-file %q' "$TASK_FILE_ABS"
  fi
  if [[ -n "$SENTINEL_FILE_ABS" ]]; then
    printf ' --sentinel-file %q' "$SENTINEL_FILE_ABS"
  fi
  printf ' >%q 2>&1\n' "$LOG_FILE"
} > "$RUNNER_FILE"

chmod +x "$RUNNER_FILE"
tmux new-session -d -s "$SESSION_NAME" -c "$PATLAS_ROOT" "$RUNNER_FILE"

echo "session_name=$SESSION_NAME"
echo "status_file=$STATUS_FILE"
echo "result_file=$RESULT_FILE"
echo "log_file=$LOG_FILE"
