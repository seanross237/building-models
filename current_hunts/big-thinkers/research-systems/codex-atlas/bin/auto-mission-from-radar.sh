#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# auto-mission-from-radar.sh
#
# Creates and launches a codex-atlas mission from a
# Research Radar breakthrough manifest JSON file.
# ─────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ATLAS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTANCES_DIR="$ATLAS_ROOT/execution/instances"

log() { echo "[auto-mission] $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"; }
fail() { log "ERROR: $*" >&2; exit 1; }

# ── Pre-flight checks ────────────────────────────────────

command -v jq >/dev/null 2>&1 || fail "jq is required but not installed"

MANIFEST="${1:-}"
[[ -n "$MANIFEST" ]] || fail "Usage: auto-mission-from-radar.sh <manifest.json>"
[[ -f "$MANIFEST" ]] || fail "Manifest file not found: $MANIFEST"

# Resolve to absolute path
MANIFEST="$(cd "$(dirname "$MANIFEST")" && pwd)/$(basename "$MANIFEST")"

# ── Parse manifest ────────────────────────────────────────

read_field() { jq -r ".$1 // empty" "$MANIFEST"; }

TITLE="$(read_field title)"
SOURCE_URL="$(read_field source_url)"
SUMMARY_PATH="$(read_field summary_path)"
ITEM_TYPE="$(read_field item_type)"
TOPIC_SLUG="$(read_field topic_slug)"
BREAKTHROUGH_SCORE="$(read_field breakthrough_score)"
DETECTED_AT="$(read_field detected_at)"
MISSION_STATUS="$(read_field mission_status)"

BREAKTHROUGH_REASONS="$(jq -r '.breakthrough_reasons // [] | join(", ")' "$MANIFEST")"

[[ -n "$TITLE" ]]      || fail "Manifest missing required field: title"
[[ -n "$SOURCE_URL" ]]  || fail "Manifest missing required field: source_url"
[[ -n "$ITEM_TYPE" ]]   || fail "Manifest missing required field: item_type"

# ── Check status ──────────────────────────────────────────

if [[ "$MISSION_STATUS" != "pending" ]]; then
  log "Skipping — mission_status is '$MISSION_STATUS' (expected 'pending')"
  exit 0
fi

# ── Generate mission name ─────────────────────────────────

TODAY="$(date -u +%Y%m%d)"

# Sanitize the title: lowercase, replace non-alphanum with hyphens, collapse,
# trim leading/trailing hyphens, then truncate to keep total name <= 60 chars.
SANITIZED_TITLE="$(printf '%s' "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs 'a-z0-9' '-' \
  | sed 's/^-*//;s/-*$//' \
  | cut -c1-30)"

# radar-<item_type>-<short-title>-<date>
MISSION_NAME="radar-${ITEM_TYPE}-${SANITIZED_TITLE}-${TODAY}"
# Final safety truncation to 60 chars and strip trailing hyphen
MISSION_NAME="$(printf '%s' "$MISSION_NAME" | cut -c1-60 | sed 's/-$//')"

MISSION_DIR="$INSTANCES_DIR/$MISSION_NAME"

log "Mission name: $MISSION_NAME"

# ── Idempotency guard ─────────────────────────────────────

if [[ -d "$MISSION_DIR" ]]; then
  log "Mission directory already exists — skipping: $MISSION_DIR"
  exit 0
fi

# ── Resolve summary content ──────────────────────────────

SUMMARY_CONTENT=""
if [[ -n "$SUMMARY_PATH" ]]; then
  # Summary path is relative to the research-radar root
  RADAR_ROOT="$(cd "$ATLAS_ROOT/../../../../research-radar" 2>/dev/null && pwd)" || true
  SUMMARY_FILE=""

  # Try several resolution strategies
  if [[ -f "$SUMMARY_PATH" ]]; then
    SUMMARY_FILE="$SUMMARY_PATH"
  elif [[ -n "$RADAR_ROOT" && -f "$RADAR_ROOT/$SUMMARY_PATH" ]]; then
    SUMMARY_FILE="$RADAR_ROOT/$SUMMARY_PATH"
  fi

  if [[ -n "$SUMMARY_FILE" && -f "$SUMMARY_FILE" ]]; then
    SUMMARY_CONTENT="$(cat "$SUMMARY_FILE")"
    log "Loaded summary from: $SUMMARY_FILE"
  else
    SUMMARY_CONTENT="_Summary file not found at \`$SUMMARY_PATH\`. The missionary agent should fetch and review the source directly._"
    log "WARNING: Summary file not found: $SUMMARY_PATH"
  fi
else
  SUMMARY_CONTENT="_No summary path provided in the manifest. The missionary agent should fetch and review the source directly._"
fi

# ── Create mission scaffold ──────────────────────────────

log "Creating mission directory: $MISSION_DIR"
mkdir -p "$MISSION_DIR/strategies" "$MISSION_DIR/meta-library"

# ── Write MISSION.md ──────────────────────────────────────

VALIDATION_NOTE=""
VALIDATION_TEMPLATE="$MISSION_DIR/MISSION-VALIDATION-GUIDE.md"
if [[ -f "$VALIDATION_TEMPLATE" ]]; then
  VALIDATION_NOTE="
## Validation

See [MISSION-VALIDATION-GUIDE.md](MISSION-VALIDATION-GUIDE.md) for the validation tiers and success criteria for this mission."
fi

cat > "$MISSION_DIR/MISSION.md" <<MISSION_EOF
# Radar Mission: ${TITLE}

## Origin

This mission was automatically triggered by Research Radar's breakthrough detector.

- Source: ${SOURCE_URL}
- Type: ${ITEM_TYPE}
- Topic: ${TOPIC_SLUG}
- Breakthrough score: ${BREAKTHROUGH_SCORE}
- Reasons flagged: ${BREAKTHROUGH_REASONS}
- Detected: ${DETECTED_AT}

## Goal

Deeply investigate this finding:

> ${TITLE}

Specific objectives:
1. Verify the central claims — are they reproducible, well-supported, and novel?
2. Find supporting evidence from related literature
3. Find contradicting evidence or limitations
4. Assess the true novelty — is this genuinely new or incremental?
5. Evaluate relevance to Eywa's self-evolving agent architecture
6. Write a comprehensive final analysis with confidence levels

## Source Summary

${SUMMARY_CONTENT}

## Constraints

- Stay focused on verification and analysis — don't pursue tangential directions
- Prefer depth over breadth
- Cite specific papers, results, or evidence
- Be honest about uncertainty — flag what you couldn't verify
${VALIDATION_NOTE}
MISSION_EOF

log "Wrote MISSION.md"

# ── Helper: update manifest fields ────────────────────────

update_manifest() {
  local tmp
  tmp="$(mktemp)"
  jq "$1" "$MANIFEST" > "$tmp" && mv "$tmp" "$MANIFEST"
}

# ── Launch mission ────────────────────────────────────────

LAUNCHED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
log "Launching mission via start-mission.sh ..."

if "$ATLAS_ROOT/bin/start-mission.sh" "$MISSION_NAME"; then
  log "Mission launched successfully"
  update_manifest \
    --arg name "$MISSION_NAME" \
    --arg ts "$LAUNCHED_AT" \
    '.mission_status = "launched" | .mission_name = $name | .launched_at = $ts'
  log "Updated manifest: status=launched"
else
  EXIT_CODE=$?
  log "start-mission.sh failed with exit code $EXIT_CODE"
  update_manifest \
    --arg name "$MISSION_NAME" \
    --arg ts "$LAUNCHED_AT" \
    '.mission_status = "failed" | .mission_name = $name | .launched_at = $ts'
  log "Updated manifest: status=failed"
  exit $EXIT_CODE
fi

log "Done — mission $MISSION_NAME is running"
