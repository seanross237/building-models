# Forge — Mission Setup Guide

This guide is for the Architect agent. Follow these steps exactly when setting up a new Forge mission.

## Prerequisites

- The mission has a **mission ID** (short slug, e.g., `optimize-retrieval`)
- The mission has a **prefix** for namespacing (e.g., `forge-optret`)
- The Architect has written MISSION.md with the goal and constraints

## Step 1: Create Mission Directory Structure

```bash
MISSION_ID="your-mission-id"
MISSION_DIR="/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/forge/missions/$MISSION_ID"

mkdir -p "$MISSION_DIR/strategies/strategy-001/tasks"
mkdir -p "$MISSION_DIR/logs"
mkdir -p "$MISSION_DIR/inbox"
```

The resulting structure:

```
missions/<mission-id>/
├── MISSION.md              # Goal, constraints, success criteria
├── MISSION-COMPLETE.md     # Created when mission finishes
├── state.json              # Conductor state
├── LOOP-STATE.md           # Conductor loop state (if using conductor hook)
├── conductor-stop-hook.sh  # Conductor hook (if needed)
├── logs/
│   ├── restarts.jsonl
│   ├── token-usage.jsonl
│   ├── timing.jsonl
│   ├── efficacy.jsonl
│   └── retrieval-quality.jsonl
├── inbox/                  # Cross-agent communication
├── strategies/
│   └── strategy-001/
│       ├── STRATEGY.md     # Methodology for this strategy
│       ├── HISTORY.md      # Summaries of completed tasks
│       ├── REASONING.md    # Decision log
│       ├── FINAL-REPORT.md # Created when strategy finishes
│       ├── state.json      # Planner state
│       ├── LOOP-STATE.md   # Planner loop state
│       ├── planner-stop-hook.sh
│       └── tasks/
│           ├── task-001/
│           │   ├── GOAL.md
│           │   ├── RESULT-SUMMARY.md
│           │   └── work/
│           └── ...
```

## Step 2: Copy Templates

```bash
FORGE_ROOT="/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/forge"
STRATEGY_DIR="$MISSION_DIR/strategies/strategy-001"

# Planner templates
cp "$FORGE_ROOT/system/agents/planner/templates/state.json" "$STRATEGY_DIR/state.json"
cp "$FORGE_ROOT/system/agents/planner/templates/LOOP-STATE.md" "$STRATEGY_DIR/LOOP-STATE.md"

# Conductor templates
cp "$FORGE_ROOT/system/agents/conductor/templates/state.json" "$MISSION_DIR/state.json"
```

## Step 3: Configure the Planner Stop Hook

```bash
PREFIX="forge-yourmission"   # Short, unique prefix for this mission
MISSION_ID="your-mission-id"

# Copy the hook template
cp "$FORGE_ROOT/system/agents/planner/planner-stop-hook.sh" "$STRATEGY_DIR/planner-stop-hook.sh"

# Replace placeholders
sed -i '' "s/__PREFIX__/$PREFIX/g" "$STRATEGY_DIR/planner-stop-hook.sh"
sed -i '' "s/__MISSION_ID__/$MISSION_ID/g" "$STRATEGY_DIR/planner-stop-hook.sh"

# Make executable
chmod +x "$STRATEGY_DIR/planner-stop-hook.sh"
```

## Step 4: Initialize LOOP-STATE.md

```bash
SLUG="planner"
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

sed -i '' "s/__SLUG__/$SLUG/g" "$STRATEGY_DIR/LOOP-STATE.md"
sed -i '' "s/__TIMESTAMP__/$TIMESTAMP/g" "$STRATEGY_DIR/LOOP-STATE.md"
```

## Step 5: Initialize state.json

Replace the mission ID placeholder in the conductor state:

```bash
sed -i '' "s/__MISSION_ID__/$MISSION_ID/g" "$MISSION_DIR/state.json"
```

The planner state.json needs no placeholder replacement — it's ready to use.

## Step 6: Create Empty Log Files

```bash
touch "$MISSION_DIR/logs/restarts.jsonl"
touch "$MISSION_DIR/logs/token-usage.jsonl"
touch "$MISSION_DIR/logs/timing.jsonl"
touch "$MISSION_DIR/logs/efficacy.jsonl"
touch "$MISSION_DIR/logs/retrieval-quality.jsonl"
```

## Step 7: Create Empty Supporting Files

```bash
touch "$STRATEGY_DIR/HISTORY.md"
touch "$STRATEGY_DIR/REASONING.md"
```

## Step 8: Register the Stop Hook in settings.json

Edit `~/.claude/settings.json` to add the hook. The file uses an array of matcher groups. Add a new entry to the top-level `hooks` object:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/missions/<mission-id>/strategies/strategy-001/planner-stop-hook.sh"
          }
        ]
      }
    ]
  }
}
```

If `hooks.Stop` already has entries (e.g., from other missions or Atlas), **append** to the existing array — do not overwrite:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/existing-hook.sh"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/missions/<mission-id>/strategies/strategy-001/planner-stop-hook.sh"
          }
        ]
      }
    ]
  }
}
```

**Important:** After editing settings.json, Claude Code will prompt the user to approve the new hook on next session start. The hook will not fire until approved.

## Step 9: Verify Setup

Before launching the Planner, verify:

```bash
# Hook script exists and is executable
ls -la "$STRATEGY_DIR/planner-stop-hook.sh"

# Templates were properly initialized (no __PLACEHOLDER__ strings remain)
grep -r '__' "$STRATEGY_DIR/LOOP-STATE.md" "$STRATEGY_DIR/planner-stop-hook.sh" && echo "WARNING: unresolved placeholders" || echo "OK: no placeholders"

# state.json is valid JSON
jq . "$STRATEGY_DIR/state.json" > /dev/null && echo "OK: valid JSON"

# settings.json references the hook
grep "planner-stop-hook" ~/.claude/settings.json && echo "OK: hook registered"
```

## Conductor Stop Hook (Optional)

If the Conductor needs to run as a persistent loop (for multi-strategy missions), repeat steps 3-4 using the conductor hook:

```bash
cp "$FORGE_ROOT/system/agents/conductor/conductor-stop-hook.sh" "$MISSION_DIR/conductor-stop-hook.sh"
sed -i '' "s/__PREFIX__/$PREFIX/g" "$MISSION_DIR/conductor-stop-hook.sh"
sed -i '' "s/__MISSION_ID__/$MISSION_ID/g" "$MISSION_DIR/conductor-stop-hook.sh"
chmod +x "$MISSION_DIR/conductor-stop-hook.sh"
```

And register it in settings.json alongside the planner hook.
