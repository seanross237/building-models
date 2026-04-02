#!/bin/bash
set -euo pipefail

ROOT="/Users/seanross/kingdom_of_god/home-base/research-radar"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y-%m-%dT%H-%M-%S)"
LOG_FILE="$LOG_DIR/nightly-radar-$STAMP.log"

exec > >(tee -a "$LOG_FILE") 2>&1

failures=0
successes=0

run_step() {
  local step_name="$1"
  shift

  echo "[research-radar] step:start $step_name"
  if "$@"; then
    successes=$((successes + 1))
    echo "[research-radar] step:ok $step_name"
  else
    local exit_code=$?
    failures=$((failures + 1))
    echo "[research-radar] step:failed $step_name exit=$exit_code"
  fi
}

echo "[research-radar] starting nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
run_step collect-youtube bash "$ROOT/pipelines/collect-youtube.sh"
run_step collect-transcripts bash "$ROOT/pipelines/collect-transcripts.sh"
run_step collect-papers bash "$ROOT/pipelines/collect-papers.sh"
run_step analyze-items bash "$ROOT/pipelines/analyze-items.sh"
run_step build-presentations bash "$ROOT/pipelines/build-presentations.sh"

echo "[research-radar] finished nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ') failures=$failures successes=$successes"
if [ "$successes" -eq 0 ]; then
  exit 1
fi
