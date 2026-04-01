# Stop Hook Guide — Definitive Reference

> Last updated: 2026-03-21
> Based on: Claude Code official documentation + empirical testing on this project

This guide is the single source of truth for how to set up autonomous research loop stop hooks in Claude Code. It covers how hooks work, exactly what format they need, every failure mode we have encountered, and a complete working template.

---

## Table of Contents

1. [How Claude Code Stop Hooks Work](#1-how-claude-code-stop-hooks-work)
2. [The Exact JSON Format](#2-the-exact-json-format)
3. [Settings Configuration](#3-settings-configuration)
4. [Where Claude Code Looks for Settings](#4-where-claude-code-looks-for-settings-critical)
5. [Common Failure Modes](#5-common-failure-modes)
6. [Working Template](#6-working-template)
7. [Session Awareness](#7-session-awareness)
8. [CWD Filtering](#8-cwd-filtering)
9. [Debugging Checklist](#9-debugging-checklist)
10. [Known Gotchas](#10-known-gotchas)
11. [History of Failures in This Project](#11-history-of-failures-in-this-project)

---

## 1. How Claude Code Stop Hooks Work

### The Stop Event

The `Stop` hook fires **when the main Claude agent finishes responding**. This is NOT on user interrupt and NOT on API errors (those use `StopFailure`).

When Claude finishes its turn and would normally wait for user input, all registered Stop hooks run. If any hook outputs `"decision": "block"`, Claude does NOT stop — instead it continues with the `reason` field injected as the next user message.

### Hook Execution Flow

```
Claude finishes responding
    → Stop event fires
    → All registered Stop hooks execute
    → Each hook receives JSON on STDIN
    → Each hook outputs JSON on STDOUT (or nothing)
    → If any hook outputs {"decision": "block", "reason": "..."}, Claude continues
    → If no hook blocks, Claude stops and waits for user input
```

### Available Hook Events (Complete List)

| Event | Can Block? | When It Fires |
|-------|-----------|---------------|
| `SessionStart` | No | Session begins or resumes |
| `SessionEnd` | No | Session terminates (1.5s timeout) |
| `UserPromptSubmit` | Yes | Before Claude processes user prompt |
| `PreToolUse` | Yes | Before tool executes |
| `PermissionRequest` | Yes | Permission dialog about to show |
| `PostToolUse` | Yes | After tool succeeds |
| `PostToolUseFailure` | Yes | After tool fails |
| `SubagentStart` | No | Subagent spawned |
| `SubagentStop` | Yes | Subagent finished |
| `TeammateIdle` | Yes | Teammate about to go idle |
| `TaskCompleted` | Yes | Task marked complete |
| `Notification` | No | Notification sent |
| `ConfigChange` | Yes | Config file changed |
| `InstructionsLoaded` | No | CLAUDE.md loaded |
| `PreCompact` | No | Before context compaction |
| `PostCompact` | No | After compaction |
| **Stop** | **Yes** | **Main agent finishes responding** |
| `StopFailure` | No | Turn ends due to API error |
| `WorktreeCreate` | Yes | Creating worktree |
| `WorktreeRemove` | No | Removing worktree |
| `Elicitation` | Yes | MCP requests user input |
| `ElicitationResult` | No | User responded to MCP |

---

## 2. The Exact JSON Format

### What the Hook RECEIVES on STDIN

```json
{
  "session_id": "e8b88880-14fb-4103-83e1-e0bfa68949de",
  "transcript_path": "/Users/seanross/.claude/projects/-Users-seanross-kingdom-of-god-science/e8b88880-14fb-4103-83e1-e0bfa68949de.jsonl",
  "cwd": "/Users/seanross/kingdom_of_god/science",
  "permission_mode": "bypassPermissions",
  "hook_event_name": "Stop",
  "stop_hook_active": false,
  "last_assistant_message": "I've completed the refactoring..."
}
```

**Fields:**
- `session_id` — UUID of the current session
- `transcript_path` — Full path to the .jsonl transcript file. This path encodes the **project key** (derived from CWD at session start — see Section 4)
- `cwd` — Current working directory of the Claude session. **NOTE:** This can change mid-session if the agent `cd`s
- `permission_mode` — One of: `default`, `plan`, `acceptEdits`, `dontAsk`, `bypassPermissions`
- `hook_event_name` — Always `"Stop"` for stop hooks
- `stop_hook_active` — **CRITICAL:** `true` when Claude is already continuing due to a previous stop hook block. Use this to prevent infinite loops
- `last_assistant_message` — The text of Claude's last response

### What the Hook Must OUTPUT on STDOUT

**To block the stop (keep Claude going):**
```json
{
  "decision": "block",
  "reason": "Your meta-prompt text here. Claude will see this as the next user message."
}
```

**Optional additional fields:**
```json
{
  "decision": "block",
  "reason": "Continue working on the task...",
  "systemMessage": "Iteration 5 of 20",
  "continue": true
}
```

**To allow the stop (let Claude stop normally):**
- Output nothing (empty stdout), OR
- Output `{}`, OR
- Exit with code 0 and no JSON

**To force Claude to stop entirely:**
```json
{
  "continue": false,
  "stopReason": "Session complete."
}
```
**NOTE:** `"continue": false` overrides everything, including `"decision": "block"`.

### Exit Codes

| Code | Meaning | Effect |
|------|---------|--------|
| **0** | Success | STDOUT is parsed as JSON |
| **2** | Blocking error | Action is blocked; STDERR shown to Claude |
| **Other** | Non-blocking error | Shown in verbose mode; Claude continues normally |

---

## 3. Settings Configuration

### The Correct Format

Stop hooks are registered in `settings.json` or `settings.local.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/your-stop-hook.sh"
          }
        ]
      }
    ]
  }
}
```

**Key points:**
- The outer array under `"Stop"` contains **matcher groups**
- Each matcher group has a `"hooks"` array of handlers
- Stop hooks do NOT support matchers (they always fire)
- The command path should be **absolute** — relative paths are unreliable
- Do NOT use `"async": true` on stop hooks you want to block with — async hooks cannot block

### Multiple Hooks

You can register multiple stop hooks. They all fire. If ANY of them outputs `"decision": "block"`, Claude continues:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook-1.sh"
          }
        ]
      },
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook-2.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 4. Where Claude Code Looks for Settings (CRITICAL)

This is the **#1 source of hook failures** in this project.

### Settings File Locations

Claude Code reads settings from these locations, in this priority order:

1. **Managed** (highest) — Server/MDM managed settings
2. **Command line args** — Temporary session overrides
3. **Local** — `<git-root>/.claude/settings.local.json`
4. **Project** — `<git-root>/.claude/settings.json`
5. **User** (lowest) — `~/.claude/settings.json`

### How the Git Root Is Determined

Claude Code walks UP from the CWD to find a `.git` directory. That directory becomes the **git root**, and that is where it looks for `.claude/settings.json` and `.claude/settings.local.json`.

### CRITICAL: Subdirectory .claude/ Directories Are IGNORED

If you have a directory structure like:

```
/science/              <-- git root (.git is here)
/science/.claude/settings.local.json    <-- THIS IS READ
/science/grand-unified-theory/.claude/settings.local.json  <-- IGNORED!
```

The `.claude/` directory in `grand-unified-theory/` is **NOT** a git root, so Claude Code does **NOT** read it. Only the `.claude/` at the git root matters.

### CRITICAL: ~/.claude/projects/<key>/settings.local.json Is NOT Used for Hooks

We have empirically confirmed that settings files placed in the per-project-key directory at `~/.claude/projects/<key>/` are **NOT** read for hook configuration. Claude Code uses that directory for:
- Transcript storage (`.jsonl` files)
- Session data

But NOT for settings or hooks.

### CRITICAL UPDATE (2026-03-21): Only Global Settings Reliably Load Hooks

After extensive testing, we discovered that **only `~/.claude/settings.json` (global user settings) reliably loads hooks for ALL sessions**. Git-root and project-level settings files were NOT picked up by sessions started from subdirectories, even when the git root resolved correctly.

**The reliable approach:**
1. Register hooks in `~/.claude/settings.json` (global)
2. Use CWD checks INSIDE the hook script to filter by session (so the hook only activates for the right project)
3. Do NOT rely on `<git-root>/.claude/settings.local.json` for hooks — it may work in some cases but has been unreliable in practice

This was the root cause of all stop hook failures in this project. The hooks were correctly written and the settings files existed at the git root, but Claude Code sessions started from subdirectories never loaded them.

### How the Project Key Is Determined

The project key (used for transcript path) is derived from the **CWD at session start**, NOT the git root:

```
Session started from: /Users/sean/kingdom_of_god/science/grand-unified-theory
Project key:          -Users-sean-kingdom-of-god-science-grand-unified-theory
Transcript at:        ~/.claude/projects/-Users-sean-kingdom-of-god-science-grand-unified-theory/<session-id>.jsonl
```

But hooks are loaded from the GIT ROOT:
```
Git root:             /Users/sean/kingdom_of_god/science
Hooks read from:      /Users/sean/kingdom_of_god/science/.claude/settings.local.json
```

This disconnect between project key (CWD-based) and settings resolution (git-root-based) is a major source of confusion.

---

## 5. Common Failure Modes

### Failure Mode 1: Hooks Registered in Wrong Location

**Symptom:** Hook never fires at all (no debug log entries).

**Cause:** The hook is registered in a `.claude/settings.local.json` that is NOT at the git root of the repo where the session is running.

**Examples from this project:**
- Hook registered at `/science/grand-unified-theory/.claude/settings.local.json` — IGNORED because `/science/` is the git root, not `/science/grand-unified-theory/`
- Hook registered at `~/.claude/projects/<key>/settings.local.json` — NEVER read for hooks

**Fix:** Always register hooks at `<git-root>/.claude/settings.local.json`.

### Failure Mode 2: Session Running from Different Git Repo

**Symptom:** Hook fires for other sessions but not the target session.

**Cause:** The tmux session was started from a directory that belongs to a DIFFERENT git repo than expected.

**Example from this project:** The theory-builder tmux session was started from `/Users/seanross/kingdom_of_god/grand-unified-theory/` (a separate git repo) instead of `/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/` (under the correct git repo). The hook at the git root's `.claude/settings.local.json` fires for sessions in that repo but not for the separately-rooted session.

**Fix:** Always start tmux sessions from the correct directory. Verify with:
```bash
# Check CWD of tmux session
tmux display-message -t <session-name> -p '#{pane_current_path}'

# Check its git root
cd <that-path> && git rev-parse --show-toplevel
```

### Failure Mode 3: Session Transcript Mismatch

**Symptom:** Hook fires but exits silently without blocking.

**Cause:** The session-awareness check in the hook compares the session's `transcript_path` against a stored value in LOOP-STATE.md. If they don't match, the hook lets the session exit.

This happens when:
- The LOOP-STATE.md was claimed by a DIFFERENT session
- The session was restarted with a new session ID
- The project key changed (e.g., directory was moved)

**Fix:** Reset the session_transcript in LOOP-STATE.md:
```bash
# Clear the stored session transcript so the next session can claim it
sed -i '' 's|^session_transcript: .*|session_transcript: ""|' /path/to/LOOP-STATE.md
```

### Failure Mode 4: CWD Filter Too Strict

**Symptom:** Hook fires but immediately skips because CWD doesn't match.

**Cause:** The hook checks `$SESSION_CWD` for a substring match, but the agent `cd`'d to a parent or sibling directory.

**Example:** Hook checks for `*"grand-unified-theory"*` but the CWD is `/Users/seanross/kingdom_of_god/science` (the git root).

**Fix:** Use a broader CWD check, or check the transcript_path as a fallback:
```bash
# Check CWD first, then fall back to transcript path
if [[ "$SESSION_CWD" != *"your-project"* ]] && [[ "$TRANSCRIPT_PATH" != *"your-project"* ]]; then
  exit 0
fi
```

### Failure Mode 5: PAUSE_HOOK File Left Behind

**Symptom:** Hook fires but does nothing.

**Cause:** A `PAUSE_HOOK` file exists in the state directory from a previous debugging session.

**Fix:**
```bash
rm /path/to/state-dir/PAUSE_HOOK
```

### Failure Mode 6: LOOP-STATE.md Does Not Exist

**Symptom:** Hook fires but exits at the first check.

**Cause:** The loop was never started, or the state file was cleaned up.

**Fix:** Create the LOOP-STATE.md file:
```bash
cat > /path/to/LOOP-STATE.md << 'EOF'
---
active: true
slug: my-loop
iteration: 0
max_iterations: 20
session_transcript: ""
started_at: "2026-03-21T00:00:00Z"
---
EOF
```

### Failure Mode 7: Hook Script Not Executable

**Symptom:** Hook doesn't fire or errors silently.

**Fix:**
```bash
chmod +x /path/to/hook.sh
```

### Failure Mode 8: stdout Pollution

**Symptom:** Hook fires but Claude doesn't continue. No error visible.

**Cause:** Debug output, echo statements, or shell profile messages written to stdout corrupt the JSON output. Claude Code expects ONLY valid JSON on stdout.

**Fix:** All debug output must go to a file or stderr:
```bash
# GOOD: debug to file
echo "debug info" >> /tmp/my-hook.log

# GOOD: debug to stderr
echo "debug info" >&2

# BAD: debug to stdout (corrupts JSON)
echo "debug info"
```

### Failure Mode 9: Hook Runs with async: true

**Symptom:** Hook fires but never blocks.

**Cause:** If the hook is registered with `"async": true`, it runs in the background and its output is NOT checked for blocking decisions.

**Fix:** Remove `"async": true` from the hook configuration. Only use async for hooks that don't need to block (like sound notifications).

---

## 6. Working Template

### Hook Script: `/path/to/my-loop-stop-hook.sh`

```bash
#!/bin/bash

# My Research Loop — Stop Hook
# Keeps the autonomous loop going by feeding a meta-prompt each iteration.
# Only activates when LOOP-STATE.md exists.
# SESSION-AWARE: Only traps the session that started the loop.

set -euo pipefail

# ── Read hook input from stdin ──
HOOK_INPUT=$(cat)

# ── Paths ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
STATE_FILE="$STATE_DIR/LOOP-STATE.md"
DEBUG_LOG="/tmp/my-loop-hook.log"

# ── Emergency escape hatch ──
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  echo "$(date): PAUSED by PAUSE_HOOK file" >> "$DEBUG_LOG"
  exit 0
fi

# ── Check if loop is active ──
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# ── Debug logging (to FILE, never stdout) ──
echo "$(date): HOOK FIRED" >> "$DEBUG_LOG"
echo "$HOOK_INPUT" >> "$DEBUG_LOG"

# ── Parse hook input ──
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')
STOP_HOOK_ACTIVE=$(echo "$HOOK_INPUT" | jq -r '.stop_hook_active // false')

# ── Prevent infinite loops ──
# If stop_hook_active is true, Claude is already continuing from a previous hook.
# You can choose to block again (for multi-iteration loops) or let it stop.
# For research loops, we DO want to block again, so we skip this check.
# Uncomment the next 3 lines if you want single-iteration hooks:
# if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
#   exit 0
# fi

# ── CWD filter: only activate for the right project ──
# Replace "my-project" with your project directory name
MY_PROJECT_DIR="my-project"
if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" != *"$MY_PROJECT_DIR"* ]]; then
  # Fallback: check transcript path
  if [[ "$TRANSCRIPT_PATH" != *"$MY_PROJECT_DIR"* ]]; then
    echo "$(date): SKIPPED — cwd=$SESSION_CWD, transcript=$TRANSCRIPT_PATH" >> "$DEBUG_LOG"
    exit 0
  fi
fi

# ── Parse YAML frontmatter from LOOP-STATE.md ──
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
SESSION_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *//; s/^"//; s/"$//')

# ── Session-aware check ──
if [[ -z "$SESSION_TRANSCRIPT" ]]; then
  # First trigger — claim this session
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  sed "s|^session_transcript: .*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$STATE_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$STATE_FILE"
  echo "$(date): CLAIMED session $TRANSCRIPT_PATH" >> "$DEBUG_LOG"
elif [[ "$SESSION_TRANSCRIPT" != "$TRANSCRIPT_PATH" ]]; then
  # Different session — let it exit normally
  echo "$(date): SKIPPED — different session (stored=$SESSION_TRANSCRIPT)" >> "$DEBUG_LOG"
  exit 0
fi

# ── Validate numeric fields ──
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "$(date): ERROR — corrupted state (iteration=$ITERATION, max=$MAX_ITERATIONS)" >> "$DEBUG_LOG"
  rm "$STATE_FILE"
  exit 0
fi

# ── Check if max iterations reached ──
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "$(date): MAX ITERATIONS reached ($MAX_ITERATIONS)" >> "$DEBUG_LOG"
  rm "$STATE_FILE"
  exit 0
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

      if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" == "MY LOOP COMPLETE" ]]; then
        echo "$(date): LOOP COMPLETE by promise" >> "$DEBUG_LOG"
        rm "$STATE_FILE"
        exit 0
      fi
    fi
  fi
fi

# ── Not complete — continue loop ──
NEXT_ITERATION=$((ITERATION + 1))

# Update iteration counter
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

echo "$(date): CONTINUING to iteration $NEXT_ITERATION" >> "$DEBUG_LOG"

# ── Build the meta-prompt ──
# IMPORTANT: Use single-quoted heredoc to avoid variable expansion issues
META_PROMPT=$(cat <<'PROMPT_EOF'
You are in autonomous research loop mode. Continue your work.

## Every Iteration Checklist
1. Read your knowledge document
2. Read your handoff notes
3. Determine what to do next
4. Execute the work
5. Update all state files

## Completion
When done, output: `<promise>MY LOOP COMPLETE</promise>`
PROMPT_EOF
)

SYSTEM_MSG="Research Loop, iteration $NEXT_ITERATION of $MAX_ITERATIONS"

# ── Output JSON to block the stop ──
# This MUST be the ONLY thing on stdout
jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
```

### LOOP-STATE.md Template

```markdown
---
active: true
slug: my-loop
iteration: 0
max_iterations: 20
session_transcript: ""
started_at: "2026-03-21T00:00:00Z"
---
```

### Settings Configuration

Place this at `<git-root>/.claude/settings.local.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/my-loop-stop-hook.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 7. Session Awareness

### Why It Matters

When you have a stop hook registered at the git root, it fires for EVERY session in that repo. If you have two terminal tabs open in the same repo, the hook fires for BOTH. Without session awareness, the hook would trap random sessions into your research loop.

### How It Works

1. LOOP-STATE.md starts with an empty `session_transcript: ""`
2. When the hook first fires, it checks `session_transcript`
3. If empty, it "claims" the session by writing the current `transcript_path` into LOOP-STATE.md
4. On subsequent fires, it compares the incoming `transcript_path` to the stored one
5. If they match — this is our loop session, continue blocking
6. If they don't match — this is a different session, let it exit

### Resetting Session Binding

When restarting a loop (new tmux session, new session ID), you MUST clear the stored transcript:

```bash
sed -i '' 's|^session_transcript: .*|session_transcript: ""|' /path/to/LOOP-STATE.md
```

Or just delete and recreate LOOP-STATE.md.

---

## 8. CWD Filtering

### The Problem

If your git repo contains multiple projects (like `/science/` containing both `grand-unified-theory/` and `research-sprints/`), hooks from `settings.local.json` fire for ALL sessions in the repo.

### The Solution

Filter by CWD in the hook script:

```bash
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

# Primary check: CWD
if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" != *"my-project"* ]]; then
  # Fallback: transcript path (catches cd'd sessions)
  if [[ "$TRANSCRIPT_PATH" != *"my-project"* ]]; then
    exit 0
  fi
fi
```

### Why Both Checks?

- The `cwd` field can change if the agent runs `cd`
- The `transcript_path` contains the original CWD from session start (encoded in the project key)
- Checking both catches more cases

---

## 9. Debugging Checklist

When a stop hook is not working, go through these steps in order:

### Step 1: Is the hook registered?

```bash
# Check the git root of your project
cd /path/to/your/project && git rev-parse --show-toplevel
# => Should show the git root

# Check if settings.local.json exists at the git root
cat "$(git rev-parse --show-toplevel)/.claude/settings.local.json"
# => Should show your hook config
```

### Step 2: Is the hook script executable?

```bash
ls -la /path/to/your-hook.sh
# => Should show -rwxr-xr-x (x permission)

# Fix if needed:
chmod +x /path/to/your-hook.sh
```

### Step 3: Is the hook firing at all?

Check the debug log:
```bash
cat /tmp/your-hook.log
# If empty: hook is not firing at all (wrong settings location)
# If has entries: hook fires but something else is wrong
```

### Step 4: Is the LOOP-STATE.md present?

```bash
cat /path/to/LOOP-STATE.md
# Should exist and have active: true
```

### Step 5: Is the session transcript matching?

```bash
# Check what's stored in LOOP-STATE.md
grep session_transcript /path/to/LOOP-STATE.md

# Check what transcript the tmux session would use
tmux display-message -t <session-name> -p '#{pane_current_path}'
# => The project key in the transcript path is derived from this CWD
```

### Step 6: Is the CWD filter passing?

Check the debug log for "SKIPPED" entries:
```bash
grep "SKIPPED" /tmp/your-hook.log
```

### Step 7: Does the hook produce valid JSON?

Test manually:
```bash
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","cwd":"/your/project/path","permission_mode":"bypassPermissions","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"test"}' | /path/to/your-hook.sh
```

The output should be valid JSON with `"decision": "block"`.

### Step 8: Is there a PAUSE_HOOK file?

```bash
ls /path/to/state-dir/PAUSE_HOOK
# If exists, remove it:
rm /path/to/state-dir/PAUSE_HOOK
```

### Step 9: Is the hook async?

Check your settings — if the hook has `"async": true`, it CANNOT block:
```json
// WRONG - async hooks cannot block
{"type": "command", "command": "/path/to/hook.sh", "async": true}

// RIGHT - synchronous (default)
{"type": "command", "command": "/path/to/hook.sh"}
```

### Step 10: Use Claude Code debug mode

```bash
claude --debug hooks
# This shows detailed hook execution info
```

---

## 10. Known Gotchas

### 1. Apostrophes in heredocs

Using `<<PROMPT_EOF` (without single quotes) causes variable expansion in the heredoc. If your meta-prompt contains `$VARIABLES` or backticks, they get expanded.

**Fix:** Always use single-quoted heredoc delimiters:
```bash
META_PROMPT=$(cat <<'PROMPT_EOF'
Your prompt here with $VARIABLES that should NOT expand
PROMPT_EOF
)
```

### 2. Relative paths in hook commands

The `command` field in settings.json does NOT resolve relative to the settings file.

**Fix:** Always use absolute paths:
```json
// WRONG
{"command": "./scripts/hook.sh"}

// RIGHT
{"command": "/Users/sean/project/scripts/hook.sh"}
```

### 3. Git root vs subdirectory

If your project is a subdirectory of a larger git repo, your `.claude/settings.local.json` must be at the git root, NOT in the subdirectory.

### 4. Multiple git repos with similar names

If you have `/kingdom/grand-unified-theory/` (own git repo) AND `/kingdom/science/grand-unified-theory/` (subdir of science repo), sessions started from each will have DIFFERENT project keys and read DIFFERENT settings files.

### 5. The stop_hook_active field

When `stop_hook_active` is `true`, Claude is already continuing from a previous stop hook. For research loops that run multiple iterations, you want to block AGAIN even when this is true. For single-shot hooks, you should check this field and exit to prevent infinite loops.

### 6. set -e and pipe failures

With `set -euo pipefail`, a failed `grep` (no matches) exits the script. This is a problem when checking transcript files:

```bash
# This will EXIT if no match found (exit code 1 from grep):
LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)

# Fix: guard with a conditional
if grep -q '"role":"assistant"' "$TRANSCRIPT_PATH"; then
  LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1)
fi
```

### 7. jq must be installed

The hook scripts depend on `jq` for JSON parsing. If jq is not in PATH, the hook silently fails.

```bash
# Verify jq is available
which jq
```

### 8. Settings are re-read on change

Claude Code watches settings files for changes. If you edit `settings.local.json` while a session is running, the new hooks WILL take effect on the next Stop event. You do NOT need to restart the session.

### 9. Hook deduplication

If the same command appears in multiple matcher groups, it only runs once. This prevents duplicate blocking.

### 10. The transcript_path encodes the CWD at session start

The project key in `transcript_path` is set when the session starts and NEVER changes, even if the agent `cd`s to a different directory. This is different from `cwd`, which reflects the current directory.

---

## 11. History of Failures in This Project

### Failure 1: Theory-builder hook never fires for tmux session (March 20-21)

**Root cause:** The tmux session was started from `/Users/seanross/kingdom_of_god/grand-unified-theory/`, which is a separate git repo with NO `.claude/` directory. The hooks were configured at the science repo's `.claude/settings.local.json` (atlas has since moved to `/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/`), which only applied to sessions in that git repo.

**Additional complication:** Someone placed a `settings.local.json` in `~/.claude/projects/-Users-seanross-kingdom-of-god-grand-unified-theory/` thinking it would be picked up. It was NOT — that directory is only for transcript storage.

**Fix needed:** Either:
1. Start the tmux session from the correct directory under the atlas git root, OR
2. Add `.claude/settings.local.json` to `/Users/seanross/kingdom_of_god/grand-unified-theory/` (the separate git root)

### Failure 2: Hook traps wrong session (March 21)

**Root cause:** Two sessions running in the same git repo (`/science/`). The hook fired for both. The first time the session_transcript was empty, so it claimed the WRONG session (Sean's interactive session instead of the tmux loop session).

**Fix:** Session-awareness check was already in place but the stored transcript was empty, causing it to claim the first session that triggered it. After manually setting the correct transcript, it worked.

### Failure 3: Research-sprints hook fires but skips

**Root cause:** The hook correctly filters by CWD containing "research-sprints", but sessions running from `/science/` (the git root) also trigger the hook. Since their CWD is `/science/` (not containing "research-sprints"), the hook correctly skips them. This is working as designed.

---

## Quick Setup Checklist

For any new autonomous research loop:

- [ ] Hook script exists and is executable (`chmod +x`)
- [ ] Hook script uses absolute paths for everything
- [ ] Hook script writes debug info to `/tmp/<name>-hook.log` (not stdout)
- [ ] Hook script only writes JSON to stdout
- [ ] LOOP-STATE.md exists with `active: true` and `session_transcript: ""`
- [ ] Settings registered at `<git-root>/.claude/settings.local.json` (verify git root with `git rev-parse --show-toplevel`)
- [ ] Settings do NOT use `"async": true` for blocking hooks
- [ ] `jq` is installed and in PATH
- [ ] tmux session starts from the correct directory (under the right git root)
- [ ] No `PAUSE_HOOK` file exists in the state directory
- [ ] CWD filter uses both `cwd` and `transcript_path` as fallback
