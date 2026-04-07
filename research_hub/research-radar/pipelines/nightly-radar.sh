#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${RADAR_LOG_DIR:-/tmp/research-radar-logs}"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y-%m-%dT%H-%M-%S)"
LOG_FILE="$LOG_DIR/nightly-radar-$STAMP.log"

exec > >(tee -a "$LOG_FILE") 2>&1

failures=0
successes=0
RADAR_TRANSCRIPT_LIMIT="${RADAR_TRANSCRIPT_LIMIT:-10}"
RADAR_ANALYZE_LIMIT="${RADAR_ANALYZE_LIMIT:-10}"
RADAR_PAPER_LOOKBACK_HOURS="${RADAR_PAPER_LOOKBACK_HOURS:-24}"
TOPIC_ARGS=()

if [[ -n "${RADAR_TOPICS:-}" ]]; then
  IFS=',' read -r -a raw_topics <<< "$RADAR_TOPICS"
  for topic in "${raw_topics[@]}"; do
    topic="${topic//[[:space:]]/}"
    if [[ -n "$topic" ]]; then
      TOPIC_ARGS+=(--topic "$topic")
    fi
  done
fi

run_step() {
  local step_name="$1"
  shift
  local step_log="$LOG_DIR/${STAMP}-${step_name}.log"

  echo "[research-radar] step:start $step_name"
  if "$@" > "$step_log" 2>&1; then
    successes=$((successes + 1))
    echo "[research-radar] step:ok $step_name log=$(basename "$step_log")"
  else
    local exit_code=$?
    failures=$((failures + 1))
    echo "[research-radar] step:failed $step_name exit=$exit_code log=$(basename "$step_log")"
    tail -n 20 "$step_log" || true
  fi
}

echo "[research-radar] starting nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "[research-radar] topic_filter=${RADAR_TOPICS:-all} transcript_limit=$RADAR_TRANSCRIPT_LIMIT analyze_limit=$RADAR_ANALYZE_LIMIT paper_lookback_hours=$RADAR_PAPER_LOOKBACK_HOURS"

youtube_args=("${TOPIC_ARGS[@]}")
if [[ -n "${RADAR_YOUTUBE_MAX_RESULTS:-}" ]]; then
  youtube_args+=(--max-results "$RADAR_YOUTUBE_MAX_RESULTS")
fi
run_step collect-youtube bash "$ROOT/pipelines/collect-youtube.sh" "${youtube_args[@]}"

transcript_args=("${TOPIC_ARGS[@]}" --limit "$RADAR_TRANSCRIPT_LIMIT")
if [[ -n "${RADAR_TRANSCRIPT_FORCE:-}" ]]; then
  transcript_args+=(--force)
fi
run_step collect-transcripts bash "$ROOT/pipelines/collect-transcripts.sh" "${transcript_args[@]}"

paper_args=("${TOPIC_ARGS[@]}" --lookback-hours "$RADAR_PAPER_LOOKBACK_HOURS")
if [[ -n "${RADAR_PAPER_MAX_RESULTS:-}" ]]; then
  paper_args+=(--max-results "$RADAR_PAPER_MAX_RESULTS")
fi
run_step collect-papers bash "$ROOT/pipelines/collect-papers.sh" "${paper_args[@]}"

analyze_args=("${TOPIC_ARGS[@]}" --limit "$RADAR_ANALYZE_LIMIT")
if [[ -n "${RADAR_ANALYZE_FORCE:-}" ]]; then
  analyze_args+=(--force)
fi
run_step analyze-items bash "$ROOT/pipelines/analyze-items.sh" "${analyze_args[@]}"

run_step build-presentations bash "$ROOT/pipelines/build-presentations.sh"

# --- Daily aggregation and analysis ---
# NOTE: aggregate-daily.sh and analyze-daily.sh were referenced here by
# commit 1e57476ce ("add daily aggregate + analysis steps to nightly
# pipeline") but the scripts themselves were never committed. They
# silently failed with exit 127 every night until 2026-04-07. Disabled
# until the actual scripts exist. Re-enable by uncommenting both lines.
# run_step aggregate-daily bash "$ROOT/pipelines/aggregate-daily.sh"
# run_step analyze-daily bash "$ROOT/pipelines/analyze-daily.sh"

echo "[research-radar] finished nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ') failures=$failures successes=$successes"
# Exit non-zero on ANY step failure so ~/scripts/nightly-radar.sh fires
# notify-failure.sh. The previous "successes==0" check meant partial
# failures were silently swallowed.
if [ "$failures" -gt 0 ]; then
  exit 1
fi
