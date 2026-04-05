#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common.sh"

ROLE=""
WORKDIR=""
MODEL=""
TASK_FILE=""
RESULT_FILE=""
STATUS_FILE=""
SESSION_NAME=""
SENTINEL_FILE=""
LOG_FILE=""

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
    --model)
      MODEL="$2"
      shift 2
      ;;
    --task-file)
      TASK_FILE="$2"
      shift 2
      ;;
    --result-file)
      RESULT_FILE="$2"
      shift 2
      ;;
    --status-file)
      STATUS_FILE="$2"
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
    --log-file)
      LOG_FILE="$2"
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

PROMPT_FILE="$(role_prompt_path "$ROLE")"
PROMPT_FILE="$(abspath "$PROMPT_FILE")"
WORKDIR_ABS="$(abspath "$WORKDIR")"
ensure_inside_repo "$WORKDIR_ABS"
ensure_inside_repo "$PROMPT_FILE"

if [[ -n "$TASK_FILE" ]]; then
  TASK_FILE_ABS="$(abspath "$TASK_FILE")"
  ensure_inside_repo "$TASK_FILE_ABS"
  TASK_CONTENT="$(cat "$TASK_FILE_ABS")"
else
  TASK_FILE_ABS=""
  TASK_CONTENT="$(cat)"
fi

MODEL="${MODEL:-$(default_model_for_role "$ROLE")}"
RUN_ID="$(compact_timestamp)-$(sanitize_token "$ROLE")-$$"
SESSION_NAME="${SESSION_NAME:-${SESSION_PREFIX}-standalone-${RUN_ID}}"

RESULT_FILE="${RESULT_FILE:-$PATLAS_ROOT/runtime/results/${SESSION_NAME}.md}"
STATUS_FILE="${STATUS_FILE:-$PATLAS_ROOT/runtime/status/${SESSION_NAME}.json}"
LOG_FILE="${LOG_FILE:-$PATLAS_ROOT/runtime/logs/${SESSION_NAME}.log}"

RESULT_FILE_ABS="$(abspath "$RESULT_FILE")"
STATUS_FILE_ABS="$(abspath "$STATUS_FILE")"
LOG_FILE_ABS="$(abspath "$LOG_FILE")"
ensure_inside_repo "$RESULT_FILE_ABS"
ensure_inside_repo "$STATUS_FILE_ABS"
ensure_inside_repo "$LOG_FILE_ABS"
mkdir -p "$(dirname "$RESULT_FILE_ABS")" "$(dirname "$STATUS_FILE_ABS")"

if [[ -n "$SENTINEL_FILE" ]]; then
  SENTINEL_FILE_ABS="$(abspath "$SENTINEL_FILE")"
  ensure_inside_repo "$SENTINEL_FILE_ABS"
  mkdir -p "$(dirname "$SENTINEL_FILE_ABS")"
else
  SENTINEL_FILE_ABS=""
fi

SEARCH_ENABLED="false"
SEARCH_FLAG=()
if role_uses_search "$ROLE"; then
  SEARCH_ENABLED="true"
  SEARCH_FLAG+=(--search)
fi

STARTED_AT="$(timestamp_utc)"
TMP_PROMPT="$PATLAS_ROOT/runtime/tmp/${RUN_ID}.prompt.md"

if nested_role_execution; then
  export STATUS_SESSION_NAME="$SESSION_NAME"
  export STATUS_ROLE="$ROLE"
  export STATUS_MODEL="$MODEL"
  export STATUS_STATE="queued"
  export STATUS_WORKSPACE_ROOT="$PATLAS_ROOT"
  export STATUS_OPERATIONAL_WORKDIR="$WORKDIR_ABS"
  export STATUS_PROMPT_FILE="$PROMPT_FILE"
  export STATUS_TASK_FILE="$TASK_FILE_ABS"
  export STATUS_RESULT_FILE="$RESULT_FILE_ABS"
  export STATUS_LOG_FILE="$LOG_FILE_ABS"
  export STATUS_SENTINEL_FILE="$SENTINEL_FILE_ABS"
  export STATUS_SESSION_PREFIX="$SESSION_PREFIX"
  export STATUS_STARTED_AT="$STARTED_AT"
  export STATUS_FINISHED_AT=""
  export STATUS_LAST_UPDATED="$STARTED_AT"
  export STATUS_SEARCH_ENABLED="$SEARCH_ENABLED"
  export STATUS_ERROR_MESSAGE=""
  write_status_json "$STATUS_FILE_ABS"

  REQUEST_FILE="$PATLAS_ROOT/runtime/requests/pending/${SESSION_NAME}.json"
  python3 - "$REQUEST_FILE" <<'PY'
import json
import os
import sys

path = sys.argv[1]
payload = {
    "kind": "run",
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

  if wait_for_status_terminal_state "$STATUS_FILE_ABS"; then
    echo "role=$ROLE"
    echo "session_name=$SESSION_NAME"
    echo "result_file=$RESULT_FILE_ABS"
    echo "status_file=$STATUS_FILE_ABS"
    exit 0
  fi

  exit 1
fi

{
  echo "You are running inside codex-philosopher-atlas."
  echo
  echo "Follow the role prompt first, then satisfy the task exactly."
  echo
  echo "## Runtime Context"
  echo
  echo "- Repository root: $PATLAS_ROOT"
  echo "- Codex workspace root: $PATLAS_ROOT"
  echo "- Operational workdir: $WORKDIR_ABS"
  echo "- Session name: $SESSION_NAME"
  echo "- Session prefix: $SESSION_PREFIX"
  echo "- Use only files inside the repository root."
  echo "- Use the local launcher scripts instead of invoking Codex directly:"
  echo "  - $PATLAS_ROOT/bin/run-role.sh"
  echo "  - $PATLAS_ROOT/bin/launch-role.sh"
  echo "  - $PATLAS_ROOT/bin/monitor-sessions.sh"
  echo "- Shared local resources live inside this repository:"
  echo "  - $PATLAS_ROOT/available-tools.md"
  echo "  - $PATLAS_ROOT/promising-findings.md"
  echo "  - $PATLAS_ROOT/idea-exploration/"
  if [[ -n "$SENTINEL_FILE_ABS" ]]; then
    echo "- Required sentinel output: $SENTINEL_FILE_ABS"
  fi
  echo
  echo "## Role Prompt"
  echo
  cat "$PROMPT_FILE"
  echo
  echo "## Task"
  echo
  printf '%s\n' "$TASK_CONTENT"
} > "$TMP_PROMPT"

export CODEX_PATLAS_ROOT="$PATLAS_ROOT"
export CODEX_PATLAS_ROLE="$ROLE"
export CODEX_PATLAS_OPERATIONAL_WORKDIR="$WORKDIR_ABS"
export CODEX_PATLAS_SESSION_PREFIX="$SESSION_PREFIX"
export CODEX_PATLAS_SESSION_NAME="$SESSION_NAME"
ORIGINAL_HOME="${HOME:-}"
SANDBOX_HOME="$PATLAS_ROOT/runtime/tmp/home"
mkdir -p "$SANDBOX_HOME"
if [[ -n "$ORIGINAL_HOME" && -d "$ORIGINAL_HOME/.codex" && ! -e "$SANDBOX_HOME/.codex" ]]; then
  ln -s "$ORIGINAL_HOME/.codex" "$SANDBOX_HOME/.codex"
fi
export HOME="$SANDBOX_HOME"
export ZDOTDIR="$SANDBOX_HOME"
export BASH_ENV="/dev/null"
export ENV=""

export STATUS_SESSION_NAME="$SESSION_NAME"
export STATUS_ROLE="$ROLE"
export STATUS_MODEL="$MODEL"
export STATUS_STATE="active"
export STATUS_WORKSPACE_ROOT="$PATLAS_ROOT"
export STATUS_OPERATIONAL_WORKDIR="$WORKDIR_ABS"
export STATUS_PROMPT_FILE="$PROMPT_FILE"
export STATUS_TASK_FILE="$TASK_FILE_ABS"
export STATUS_RESULT_FILE="$RESULT_FILE_ABS"
export STATUS_LOG_FILE="$LOG_FILE_ABS"
export STATUS_SENTINEL_FILE="$SENTINEL_FILE_ABS"
export STATUS_SESSION_PREFIX="$SESSION_PREFIX"
export STATUS_STARTED_AT="$STARTED_AT"
export STATUS_FINISHED_AT=""
export STATUS_LAST_UPDATED="$STARTED_AT"
export STATUS_SEARCH_ENABLED="$SEARCH_ENABLED"
export STATUS_ERROR_MESSAGE=""
write_status_json "$STATUS_FILE_ABS"

CMD=(
  codex
)
if [[ ${#SEARCH_FLAG[@]} -gt 0 ]]; then
  CMD+=("${SEARCH_FLAG[@]}")
fi
CMD+=(
  exec
  --skip-git-repo-check
  --full-auto
  -C "$PATLAS_ROOT"
  -m "$MODEL"
  -o "$RESULT_FILE_ABS"
  -
)

set +e
"${CMD[@]}" < "$TMP_PROMPT"
EXIT_CODE=$?
set -e

FINISHED_AT="$(timestamp_utc)"
STATUS_FINISHED_AT="$FINISHED_AT"
STATUS_LAST_UPDATED="$FINISHED_AT"

if [[ $EXIT_CODE -eq 0 ]]; then
  if [[ -n "$SENTINEL_FILE_ABS" && ! -f "$SENTINEL_FILE_ABS" ]]; then
    STATUS_STATE="error"
    STATUS_ERROR_MESSAGE="Codex exited successfully but did not produce sentinel file $SENTINEL_FILE_ABS"
  else
    STATUS_STATE="done"
    STATUS_ERROR_MESSAGE=""
  fi
else
  STATUS_STATE="error"
  STATUS_ERROR_MESSAGE="codex exec exited with status $EXIT_CODE"
fi

export STATUS_STATE STATUS_ERROR_MESSAGE STATUS_FINISHED_AT STATUS_LAST_UPDATED
write_status_json "$STATUS_FILE_ABS"
rm -f "$TMP_PROMPT"

echo "role=$ROLE"
echo "session_name=$SESSION_NAME"
echo "result_file=$RESULT_FILE_ABS"
echo "status_file=$STATUS_FILE_ABS"

if [[ "$STATUS_STATE" == "error" ]]; then
  exit 1
fi
