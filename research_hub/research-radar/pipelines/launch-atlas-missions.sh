#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# launch-atlas-missions.sh
#
# Scans the atlas-missions queue for pending breakthrough
# manifests and launches a codex-atlas mission for each.
#
# Usage:
#   pipelines/launch-atlas-missions.sh [--dry-run] [--limit N]
# ─────────────────────────────────────────────────────────

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE_DIR="$ROOT/data/queues/atlas-missions"
ATLAS_LAUNCHER="$(cd "$ROOT/../../research_hub/big-thinkers/research-systems/codex-atlas/bin" && pwd)/auto-mission-from-radar.sh"

DRY_RUN=false
LIMIT=0   # 0 = no limit

log() { echo "[launch-atlas] $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"; }

# ── Parse flags ───────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --limit)
      LIMIT="${2:-}"
      [[ -n "$LIMIT" && "$LIMIT" =~ ^[0-9]+$ ]] || { log "ERROR: --limit requires a positive integer"; exit 1; }
      shift 2
      ;;
    *)
      log "ERROR: Unknown flag: $1"
      echo "Usage: launch-atlas-missions.sh [--dry-run] [--limit N]" >&2
      exit 1
      ;;
  esac
done

# ── Pre-flight checks ────────────────────────────────────

if [[ ! -x "$ATLAS_LAUNCHER" ]]; then
  log "ERROR: Auto-launcher not found or not executable: $ATLAS_LAUNCHER"
  exit 1
fi

if [[ ! -d "$QUEUE_DIR" ]]; then
  log "No queue directory found at $QUEUE_DIR — nothing to launch"
  exit 0
fi

# ── Scan for pending manifests ────────────────────────────

PENDING_FILES=()
for manifest in "$QUEUE_DIR"/*.json; do
  [[ -f "$manifest" ]] || continue
  status="$(jq -r '.mission_status // empty' "$manifest" 2>/dev/null)" || continue
  if [[ "$status" == "pending" ]]; then
    PENDING_FILES+=("$manifest")
  fi
done

TOTAL="${#PENDING_FILES[@]}"
log "Found $TOTAL pending manifest(s) in $QUEUE_DIR"

if [[ "$TOTAL" -eq 0 ]]; then
  log "Nothing to do"
  exit 0
fi

# ── Launch each ───────────────────────────────────────────

launched=0
failed=0
skipped=0

for manifest in "${PENDING_FILES[@]}"; do
  # Check limit
  if [[ "$LIMIT" -gt 0 && "$launched" -ge "$LIMIT" ]]; then
    log "Reached limit of $LIMIT — stopping"
    break
  fi

  filename="$(basename "$manifest")"
  title="$(jq -r '.title // "unknown"' "$manifest" 2>/dev/null)"
  log "Processing: $filename ($title)"

  if $DRY_RUN; then
    log "  [dry-run] Would launch mission for: $title"
    skipped=$((skipped + 1))
    continue
  fi

  if "$ATLAS_LAUNCHER" "$manifest"; then
    launched=$((launched + 1))
    log "  Launched successfully"
  else
    failed=$((failed + 1))
    log "  Launch failed (continuing with next)"
  fi
done

log "Summary: total=$TOTAL launched=$launched failed=$failed skipped=$skipped"

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
