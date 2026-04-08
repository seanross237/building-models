#!/usr/bin/env bash
# Cron-ready radar wrapper.
#
# Activates the project venv, runs the radar pipeline, and writes a
# dated log file under logs/. Exits non-zero if anything fails so cron
# (or the Telegram notify-failure hook) can pick it up.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f .venv/bin/activate ]]; then
  echo "ERROR: .venv not found at $(pwd)/.venv. Run 'python -m venv .venv && pip install -r requirements.txt' first." >&2
  exit 2
fi

# shellcheck source=/dev/null
source .venv/bin/activate

mkdir -p logs
LOGFILE="logs/radar-$(date +%Y-%m-%d).log"

{
  echo "=== Radar run at $(date -Iseconds 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  python -m pipelines.run_skeleton
  echo "=== OK at $(date -Iseconds 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOGFILE" 2>&1
