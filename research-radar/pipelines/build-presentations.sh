#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
QUEUE_DIR="$ROOT/data/queues/presentation-candidates"
OUTPUT_ROOT="$REPO_ROOT/presentations"

mkdir -p "$QUEUE_DIR"
count=$(find "$QUEUE_DIR" -maxdepth 1 -name "*.json" | wc -l | tr -d " ")

if [ "$count" = "0" ]; then
  echo "[build-presentations] no presentation candidates queued"
  exit 0
fi

echo "[build-presentations] queued candidates: $count"
echo "[build-presentations] output root: $OUTPUT_ROOT"
find "$QUEUE_DIR" -maxdepth 1 -name "*.json" | sort
echo "[build-presentations] TODO: generate guide-compliant decks from queued candidates"
