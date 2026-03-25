#!/bin/bash

# Strategizer — Stop Hook
# Keeps the strategizer loop alive between context resets.
# Adapts the template from LOOP-STOP-HOOK-GUIDE.md.
#
# USAGE: Place this script in the strategy directory, or symlink it there.
#        The script assumes LOOP-STATE.md and state.json are in SCRIPT_DIR.
#        Register in ~/.claude/settings.json (global) for reliability.
#
# EXPECTS in SCRIPT_DIR:
#   LOOP-STATE.md  — hook control (iteration, session binding)
#   state.json     — strategizer state (done flag, explorations)
#   STRATEGY.md    — the strategic direction from the missionary
#   HISTORY.md     — accumulated exploration summaries

set -euo pipefail

# ── Read hook input from stdin ──
HOOK_INPUT=$(cat)

# ── Paths ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
LOOP_STATE="$STATE_DIR/LOOP-STATE.md"
STRATEGY_STATE="$STATE_DIR/state.json"
DEBUG_LOG="/tmp/strategizer-hook.log"

# ── Emergency escape hatch ──
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  echo "$(date): PAUSED by PAUSE_HOOK file" >> "$DEBUG_LOG"
  exit 0
fi

# ── Check if loop is active ──
if [[ ! -f "$LOOP_STATE" ]]; then
  exit 0
fi

# ── Debug logging (to FILE, never stdout) ──
echo "$(date): HOOK FIRED" >> "$DEBUG_LOG"

# ── Parse hook input ──
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

# ── CWD filter: only activate for sessions in this project ──
# Must match on EITHER cwd or transcript_path. If neither contains the project dir, skip.
PROJECT_DIR="atlas"
CWD_MATCH=false
TRANSCRIPT_MATCH=false
if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" == *"$PROJECT_DIR"* ]]; then
  CWD_MATCH=true
fi
if [[ -n "$TRANSCRIPT_PATH" ]] && [[ "$TRANSCRIPT_PATH" == *"$PROJECT_DIR"* ]]; then
  TRANSCRIPT_MATCH=true
fi
if [[ "$CWD_MATCH" == "false" ]] && [[ "$TRANSCRIPT_MATCH" == "false" ]]; then
  echo "$(date): SKIPPED — cwd=$SESSION_CWD, transcript=$TRANSCRIPT_PATH" >> "$DEBUG_LOG"
  exit 0
fi

# ── Parse YAML frontmatter from LOOP-STATE.md ──
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_STATE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
SESSION_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *//; s/^"//; s/"$//')

# ── Session-aware check ──
if [[ -z "$SESSION_TRANSCRIPT" ]]; then
  # First trigger — claim this session
  TEMP_FILE="${LOOP_STATE}.tmp.$$"
  sed "s|^session_transcript: .*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$LOOP_STATE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$LOOP_STATE"
  echo "$(date): CLAIMED session $TRANSCRIPT_PATH" >> "$DEBUG_LOG"
elif [[ "$SESSION_TRANSCRIPT" != "$TRANSCRIPT_PATH" ]]; then
  echo "$(date): SKIPPED — different session" >> "$DEBUG_LOG"
  exit 0
fi

# ── Validate numeric fields ──
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "$(date): ERROR — corrupted state (iteration=$ITERATION, max=$MAX_ITERATIONS)" >> "$DEBUG_LOG"
  rm "$LOOP_STATE"
  exit 0
fi

# ── Check if max iterations reached ──
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "$(date): MAX ITERATIONS reached ($MAX_ITERATIONS)" >> "$DEBUG_LOG"
  rm "$LOOP_STATE"
  # Hand off to missionary (same logic as done=true)
  INSTANCE_DIR="$(cd "$STATE_DIR/../.." && pwd)"
  PROJECT_ROOT="$(cd "$STATE_DIR/../../../.." && pwd)"
  STRATEGY_NAME="$(basename "$STATE_DIR")"
  MISSIONARY_PROMPT="$PROJECT_ROOT/agents/missionary/system-prompt.md"
  if [[ -f "$MISSIONARY_PROMPT" ]]; then
    echo "$(date): LAUNCHING MISSIONARY — max iterations on $STRATEGY_NAME" >> "$DEBUG_LOG"
    tmux new-session -d -s missionary -c "$INSTANCE_DIR" \
      "claude --system-prompt-file '$MISSIONARY_PROMPT' --permission-mode bypassPermissions" 2>> "$DEBUG_LOG" || true
    sleep 5
    tmux send-keys -t missionary "Strategy $STRATEGY_NAME hit its iteration limit. Read the strategy state in strategies/$STRATEGY_NAME/state.json and history in strategies/$STRATEGY_NAME/HISTORY.md. Decide whether to continue (launch a new strategy with the same or modified approach), pivot, or declare the mission needs rethinking. Use SETUP-GUIDE.md at $PROJECT_ROOT/SETUP-GUIDE.md if launching a new strategy." Enter 2>> "$DEBUG_LOG" || true
  fi
  exit 0
fi

# ── Check if strategizer marked itself done via state.json ──
if [[ -f "$STRATEGY_STATE" ]]; then
  DONE=$(jq -r '.done // false' "$STRATEGY_STATE" 2>/dev/null || echo "false")
  if [[ "$DONE" == "true" ]]; then
    echo "$(date): STRATEGIZER DONE (state.json done=true)" >> "$DEBUG_LOG"
    rm "$LOOP_STATE"

    # ── Hand off to the Missionary ──
    # Find the instance directory (two levels up from strategy dir)
    INSTANCE_DIR="$(cd "$STATE_DIR/../.." && pwd)"
    PROJECT_ROOT="$(cd "$STATE_DIR/../../../.." && pwd)"
    STRATEGY_NAME="$(basename "$STATE_DIR")"
    MISSIONARY_PROMPT="$PROJECT_ROOT/agents/missionary/system-prompt.md"

    if [[ -f "$MISSIONARY_PROMPT" ]]; then
      echo "$(date): LAUNCHING MISSIONARY for $STRATEGY_NAME completion" >> "$DEBUG_LOG"
      # Launch missionary in a new tmux session
      tmux new-session -d -s missionary -c "$INSTANCE_DIR" \
        "claude --system-prompt-file '$MISSIONARY_PROMPT' --permission-mode bypassPermissions" 2>> "$DEBUG_LOG" || true
      # Wait for it to start, then send the prompt
      sleep 5
      tmux send-keys -t missionary "Strategy $STRATEGY_NAME has completed. Read the strategy outcome in strategies/$STRATEGY_NAME/state.json and the exploration history in strategies/$STRATEGY_NAME/HISTORY.md. Decide whether to launch a new strategy or declare the mission complete. If launching a new strategy, use the SETUP-GUIDE.md at $PROJECT_ROOT/SETUP-GUIDE.md." Enter 2>> "$DEBUG_LOG" || true
    else
      echo "$(date): WARNING — missionary prompt not found at $MISSIONARY_PROMPT" >> "$DEBUG_LOG"
    fi

    exit 0
  fi
fi

# ── Check for completion signal in last assistant message ──
if [[ -f "$TRANSCRIPT_PATH" ]] && grep -q '"role":"assistant"' "$TRANSCRIPT_PATH"; then
  LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)
  if [[ -n "$LAST_LINE" ]]; then
    LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
      .message.content |
      map(select(.type == "text")) |
      map(.text) |
      join("\n")
    ' 2>/dev/null || echo "")

    if [[ -n "$LAST_OUTPUT" ]]; then
      PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' 2>/dev/null || echo "")

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" == "STRATEGY COMPLETE" ]]; then
        echo "$(date): STRATEGY COMPLETE by promise" >> "$DEBUG_LOG"
        rm "$LOOP_STATE"
        # Hand off to missionary (same logic as done=true)
        INSTANCE_DIR="$(cd "$STATE_DIR/../.." && pwd)"
        PROJECT_ROOT="$(cd "$STATE_DIR/../../../.." && pwd)"
        STRATEGY_NAME="$(basename "$STATE_DIR")"
        MISSIONARY_PROMPT="$PROJECT_ROOT/agents/missionary/system-prompt.md"
        if [[ -f "$MISSIONARY_PROMPT" ]]; then
          echo "$(date): LAUNCHING MISSIONARY — strategy $STRATEGY_NAME complete by promise" >> "$DEBUG_LOG"
          tmux new-session -d -s missionary -c "$INSTANCE_DIR" \
            "claude --system-prompt-file '$MISSIONARY_PROMPT' --permission-mode bypassPermissions" 2>> "$DEBUG_LOG" || true
          sleep 5
          tmux send-keys -t missionary "Strategy $STRATEGY_NAME has completed. Read the strategy outcome in strategies/$STRATEGY_NAME/state.json and the exploration history in strategies/$STRATEGY_NAME/HISTORY.md. Decide whether to launch a new strategy or declare the mission complete. Use SETUP-GUIDE.md at $PROJECT_ROOT/SETUP-GUIDE.md if launching a new strategy." Enter 2>> "$DEBUG_LOG" || true
        fi
        exit 0
      fi
    fi
  fi
fi

# ── Not complete — continue loop ──
NEXT_ITERATION=$((ITERATION + 1))

# Update iteration counter
TEMP_FILE="${LOOP_STATE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$LOOP_STATE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$LOOP_STATE"

echo "$(date): CONTINUING to iteration $NEXT_ITERATION" >> "$DEBUG_LOG"

# ── Build the meta-prompt ──
# Paths relative to strategy directory for the strategizer to read
META_PROMPT=$(cat <<'PROMPT_EOF'
You are the Strategizer in autonomous loop mode. A context reset occurred. Resume your work.

## Startup Sequence

1. **Read `state.json`** — Know your iteration, current phase, and what explorations have been completed.
2. **Read `STRATEGY.md`** — Your strategic direction from the Missionary.
3. **Read `HISTORY.md`** — Summaries of all completed explorations.
4. **If planning a new exploration**, check the library INDEX at `../../../../agents/library/factual/INDEX.md` — browse topic indexes only as needed.
5. **Determine your phase** from state.json and act:
   - If an exploration was in progress when context reset: treat it as failed, note in state.json, plan next.
   - If between explorations: decide what to explore next based on history and strategy.

## Exploration Cycle

1. Design the exploration — write `explorations/exploration-NNN/GOAL.md`
2. Spawn an Explorer sub-agent with the goal and any relevant library context
3. Explorer writes `REPORT.md` (detailed) and `REPORT-SUMMARY.md` (concise) in its exploration directory
4. Explorer returns a short summary to you
5. Append the summary to `HISTORY.md`
6. Drop `REPORT.md` into `../../../../library-inbox/` for the curator
7. Update `state.json` with the outcome
8. Decide next exploration and repeat

## State Updates

After EVERY exploration, update state.json:
- Increment iteration
- Update current_exploration status
- Add to explorations_completed array
- Set phase

## Completion

When the strategy is complete or exhausted, update state.json with `"done": true`, then output:
`<promise>STRATEGY COMPLETE</promise>`
PROMPT_EOF
)

SYSTEM_MSG="Strategizer Loop — iteration $NEXT_ITERATION of $MAX_ITERATIONS"

# ── Output JSON to block the stop ──
jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
