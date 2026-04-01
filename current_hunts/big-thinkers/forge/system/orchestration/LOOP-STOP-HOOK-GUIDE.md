# Forge — Loop Stop Hook Reference Guide

## How Claude Code Stop Hooks Work

Claude Code fires a **Stop** event every time the agent finishes responding — when it would normally return control to the user. A stop hook is a shell script registered in `~/.claude/settings.json` that runs on each Stop event. The hook receives context on stdin and can:

- **Allow the stop** (exit 0 with no JSON output, or output `{"decision":"allow"}`) — the session ends normally.
- **Block the stop** (output `{"decision":"block", "reason":"...", ...}`) — the agent receives the `reason` as its next user message and continues working.

This is the mechanism that makes autonomous loops possible: the agent finishes, the hook catches it, and injects a meta-prompt that tells the agent to resume.

## Hook Input Format (stdin)

The hook receives a JSON object on stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/you/.claude/projects/-Users-you-project/session-uuid.jsonl",
  "cwd": "/Users/you/project",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

| Field | Description |
|---|---|
| `session_id` | Unique identifier for the Claude Code session |
| `transcript_path` | Absolute path to the session's transcript JSONL file |
| `cwd` | Working directory of the Claude Code session |
| `permission_mode` | Permission mode the session is running in |
| `hook_event_name` | Always `"Stop"` for stop hooks |
| `stop_hook_active` | Whether the hook system is active |

## Hook Output Format (stdout)

To **block the stop** and continue the loop:

```json
{
  "decision": "block",
  "reason": "Your meta-prompt text here — this becomes the next user message",
  "systemMessage": "Optional system-level context (shown as system info, not user message)"
}
```

To **allow the stop** (or for non-matching sessions), either:
- Output nothing and exit 0
- Output `{"decision": "allow"}`

## settings.json Configuration

Stop hooks are registered in `~/.claude/settings.json` under `hooks.Stop`. The structure is an array of **matcher groups**, each containing a `hooks` array:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
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

Multiple hooks can coexist. Each matcher group fires independently. An empty `matcher` string matches all sessions — the hook script itself is responsible for filtering.

**Example with multiple hooks (Atlas + Forge):**

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/atlas/strategizer-stop-hook.sh"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/forge/planner-stop-hook.sh"
          }
        ]
      }
    ]
  }
}
```

**Important:** After modifying settings.json, Claude Code will prompt the user to approve new hooks on the next session start.

## Session Awareness Pattern

The critical problem: multiple hooks fire on **every** stop event across **all** sessions. Each hook must determine whether the event belongs to its loop.

### First Fire Claims, Subsequent Fires Match

```
1. Hook fires → reads LOOP-STATE.md → session_transcript is empty
   → First fire: write transcript_path into LOOP-STATE.md (claim the session)
   → Block the stop

2. Hook fires → reads LOOP-STATE.md → session_transcript has a value
   → Compare transcript_path from stdin against stored value
   → Match: this is our session → block the stop
   → Mismatch: not our session → exit 0 (allow the stop)
```

This pattern ensures that:
- A Planner hook only catches its own Planner session
- Worker sessions, other Planners, and unrelated Claude sessions pass through unaffected
- The binding is durable across restarts (stored in the file, not in memory)

### Why transcript_path, not cwd?

Multiple agents (Planner, Workers) may share the same `cwd`. The `transcript_path` is unique per session and stable across the session's lifetime, making it the only reliable discriminator.

## LOOP-STATE.md Format

```markdown
---
active: true
slug: planner
iteration: 0
max_iterations: 30
session_transcript: ""
started_at: 2026-03-28T12:00:00Z
---

Forge Planner loop state. Do not edit manually — managed by the stop hook.
```

| Field | Description |
|---|---|
| `active` | Set to `false` to gracefully stop the loop on next fire |
| `slug` | Agent identifier (for logging) |
| `iteration` | Current iteration count (incremented by the hook) |
| `max_iterations` | Safety cap — hook stops blocking after this many iterations |
| `session_transcript` | Empty initially; set to transcript_path on first fire |
| `started_at` | ISO timestamp of when the loop was initialized |

The hook reads and updates this file using `sed` — it parses the YAML frontmatter between `---` delimiters.

## CWD Filtering

For additional safety, the hook can check that the `transcript_path` or `cwd` from stdin contains the mission ID. This prevents a hook from accidentally claiming a session from a completely unrelated project. The session awareness pattern (above) is the primary filter; CWD checking is a secondary guard.

## Debugging Checklist

When a hook is not firing or behaving unexpectedly:

1. **Check the debug log:** `cat missions/<id>/logs/forge-<prefix>-hook.log`
   - If no log entries: the hook is not being executed at all
   - If log entries say "Session mismatch": another session is triggering it

2. **Verify settings.json registration:**
   ```bash
   jq '.hooks.Stop' ~/.claude/settings.json
   ```
   - Ensure the path is absolute and the file exists
   - Ensure the hook was approved (Claude prompts on first use)

3. **Verify the hook is executable:**
   ```bash
   ls -la /path/to/planner-stop-hook.sh
   ```

4. **Check LOOP-STATE.md:**
   - Is `active: true`?
   - Is `iteration` below `max_iterations`?
   - Is `session_transcript` set to the correct session, or empty?

5. **Check state.json:**
   - Is `done: false`?

6. **Check for PAUSE_HOOK file:**
   ```bash
   ls /path/to/strategy-dir/PAUSE_HOOK
   ```

7. **Test the hook manually:**
   ```bash
   echo '{"transcript_path":"/test/path","session_id":"test"}' | /path/to/planner-stop-hook.sh
   ```

8. **Check jq is available:**
   ```bash
   which jq
   ```

## Known Gotchas

### Hook fires but nothing happens
The hook exited 0 without outputting JSON. Check the debug log to see which check caused the early exit. Common causes: `active: false`, `done: true`, session mismatch.

### Hook catches the wrong session
The `session_transcript` field in LOOP-STATE.md was claimed by a different session. Fix: clear the `session_transcript` field (set it back to `""`) and restart the intended session.

### Relative paths don't work
Hook commands in settings.json must use **absolute paths**. Relative paths will fail silently because the hook's working directory is unpredictable.

### settings.json permission prompt
Every time you add a new hook command to settings.json, Claude Code prompts the user to approve it. This is a security feature. The hook will not fire until approved. Make sure to approve it before expecting the loop to work.

### Multiple hooks interfere
If two hooks both try to block the same session, the behavior is undefined. Each hook must correctly identify its own session and exit 0 for all others. The transcript_path matching pattern handles this.

### sed differences between macOS and Linux
The hook uses `sed -i ''` on macOS. If deploying on Linux, change to `sed -i` (without the empty string argument). The hook templates use in-place temp files (`${FILE}.tmp.$$` + `mv`) instead of `sed -i` to avoid this portability issue.

### Frontmatter parsing edge cases
The hook parses YAML frontmatter using `sed` and `grep`, not a real YAML parser. Avoid putting colons, quotes, or special characters in field values. The `session_transcript` field is the most sensitive — it contains a file path with special characters (dashes, dots), which is handled by the regex but could break if the path contains quotes or newlines.
