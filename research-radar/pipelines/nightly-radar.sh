#!/bin/bash
set -euo pipefail

ROOT="/Users/seanross/kingdom_of_god/home-base/research-radar"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y-%m-%dT%H-%M-%S)"
LOG_FILE="$LOG_DIR/nightly-radar-$STAMP.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "[research-radar] starting nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
bash "$ROOT/pipelines/collect-youtube.sh"
bash "$ROOT/pipelines/collect-transcripts.sh"
bash "$ROOT/pipelines/collect-papers.sh"
bash "$ROOT/pipelines/analyze-items.sh"
bash "$ROOT/pipelines/build-presentations.sh"
echo "[research-radar] finished nightly radar run at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
