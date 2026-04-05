#!/bin/bash
set -euo pipefail

# backfill-transcripts.sh — run from a local Mac (residential IP) to fetch
# YouTube transcripts that the Hetzner dev box cannot grab.
#
# Usage:
#   bash backfill-transcripts.sh          # default: 100 transcripts
#   bash backfill-transcripts.sh 50       # custom limit
#   bash backfill-transcripts.sh --dry-run

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

# If the first arg looks like a flag, pass everything as flags.
# Otherwise treat $1 as the limit.
if [[ "${1:-}" == --* ]]; then
  EXTRA_ARGS=("$@")
  LIMIT=""
else
  LIMIT="${1:-100}"
  shift || true
  EXTRA_ARGS=("$@")
fi

echo "[backfill] pulling latest..."
cd "$REPO_ROOT"
git pull origin main --rebase

echo "[backfill] fetching transcripts${LIMIT:+ (limit $LIMIT)}..."
cd "$ROOT"
ARGS=()
if [ -n "$LIMIT" ]; then
  ARGS+=(--limit "$LIMIT")
fi
ARGS+=("${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}")

python3 scripts/fetch-transcripts-local.py "${ARGS[@]}"

cd "$REPO_ROOT"
if [ -n "$(git status --porcelain research-radar/ research_hub/research-radar/)" ]; then
  git add research-radar/ research_hub/research-radar/
  git commit -m "chore(research-radar): backfill transcripts $(date +%Y-%m-%d)"
  git push origin main
  echo "[backfill] committed and pushed"
else
  echo "[backfill] no new transcripts to commit"
fi
