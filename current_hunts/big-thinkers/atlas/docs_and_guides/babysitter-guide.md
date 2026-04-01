# Atlas Babysitter Guide

## What It Does

The babysitter monitors Atlas tmux sessions (missionaries, strategizers, explorers) and handles common issues automatically. It runs as a bash script — zero tokens for known patterns, and only spawns a Claude instance for situations it hasn't seen before.

## Location

```
execution/babysitter/
├── check.sh          # The main script — run this on a timer
├── test_check.sh     # Test suite — 24 tests covering all patterns
├── logs/             # Daily log files (YYYYMMDD.log)
├── status.json       # Last known status (legacy, may be removed)
└── system-prompt.md  # Legacy prompt (superseded by check.sh)
```

## How to Run

### Manual check
```bash
bash execution/babysitter/check.sh
```

### On a timer (from a Claude session)
```
CronCreate: cron="*/10 * * * *", prompt="bash /path/to/check.sh"
```

### As a system cron (survives session exit)
```bash
crontab -e
# Add:
*/10 * * * * /path/to/atlas/execution/babysitter/check.sh
```

### Recommended interval
Every 10-15 minutes. The old 7-minute interval was overkill — stuck agents don't get MORE stuck, and the babysitter can't help with rate limits (it just nudges, and if the limit hasn't reset, nothing happens).

## How It Works

### Pattern matching (zero tokens)
The script captures the last 20 lines of each tmux pane and pattern-matches against known states:

| Pattern | Detection | Action |
|---|---|---|
| **Settings.json prompt** | "Do you want to make this edit to settings.json" | Auto-approve (option 2) |
| **Permission prompt** | "❯ 1. Yes" + known file type (REPORT, GOAL, etc.) | Auto-approve |
| **Rate limited** | "You've hit your limit" | Nudge with "continue" |
| **Completed work** | "Cooked/Crunched/Worked/Brewed for" | Log as idle |
| **Mission/strategy complete** | "strategy is complete", "MISSION-COMPLETE", etc. | Log as idle |
| **Actively working** | Spinner characters (✳✶✽✢✻·) | Log progress % and tokens |
| **Computing** | "Running…" with timeout | Log computation status |
| **Blank/starting** | < 3 non-empty lines | Log as starting |
| **Error loop** | 3+ lines with "Error/error/failed" | Escalate to Claude |

### Claude escalation (tokens only when needed)
When the script encounters a state it can't pattern-match, it spawns a **fresh, short-lived Claude instance** with:
- `--permission-mode bypassPermissions` (can take action)
- `--no-session-persistence` (no history saved)
- `-p` (print mode — runs and exits)
- Only the unknown pane content as context (~5K tokens instead of ~200K)

The Claude instance can:
1. Diagnose and fix the issue
2. **Update check.sh** to add a new pattern for this scenario

This makes the babysitter self-improving — each unknown scenario it encounters teaches it to handle similar situations without tokens next time.

## Why Not Use a Claude Cron?

The previous approach used a Claude cron (`CronCreate`) that ran the check as a prompt in the main conversation. This was expensive because:

- Every API call re-sends the **entire conversation history**
- After 8 hours, each check cost ~130-200K input tokens
- 292 checks × 127K avg = **37M tokens** for babysitting alone
- The actual new work per check was ~2K tokens

The bash script costs **zero tokens** for the 95%+ of checks where everything is healthy. When Claude IS needed, a fresh instance with minimal context costs ~5K tokens instead of 200K.

**Cost comparison for 8 hours of monitoring:**

| Approach | Checks | Tokens/check | Total |
|---|---|---|---|
| Claude cron (old) | ~68 | ~130K | ~9M |
| Bash + Claude escalation (new) | ~48 | ~0 (+ ~5K per escalation) | ~25K |
| Savings | | | **~99.7%** |

## Testing

Run the test suite:
```bash
bash execution/babysitter/test_check.sh
```

Tests cover:
- All 6 spinner variants (✳✶✽✢✻·)
- Permission prompts (settings, known files, unknown files)
- Rate limit detection and nudging
- Idle states (completed work, mission complete, strategy complete)
- Blank/starting sessions
- Error loop detection (3+ errors) vs single errors
- Unknown state escalation
- Integration test against live sessions

## Adding New Patterns

When Claude is spawned for an unknown scenario, it should add a new pattern to `check.sh` in the `KNOWN_PATTERNS` section. The format:

```bash
# Pattern: <description>
if echo "$PANE" | grep -q "<detection string>"; then
    # Optional: take action
    tmux send-keys -t "$SESSION" "<keys>" Enter 2>/dev/null
    ACTIONS_TAKEN="${ACTIONS_TAKEN}[$TIMESTAMP] $SESSION: <log message>\n"
    continue
fi
```

After adding a pattern, run `test_check.sh` to verify it doesn't break existing patterns. Add a new `test_pattern` call for the new scenario.

## Known Limitations

1. **Can't distinguish "idle because done" from "idle because crashed"** if the crash left no error output. The strategizer's file-watch handles this — if an explorer crashes, the watch times out after 3 hours.

2. **Rate limit nudging is blind** — it sends "continue" without knowing if the limit has actually reset. Harmless (the agent just shows the limit message again), but wastes a nudge.

3. **Pattern matching is literal** — if Claude Code changes its UI (different spinner characters, different prompt format), patterns will break. The self-improving mechanism handles this: the first occurrence escalates to Claude, which updates the patterns.

4. **Only monitors Atlas sessions** — the grep filter is `(explorer|strategizer|missionary)`. Other systems (forge, nexus) use different session naming and aren't monitored.
