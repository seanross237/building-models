# Strategy Setup Guide

This guide is for setting up a new strategy directory so a Strategizer can run. You will be given a mission name and strategy number.

## Steps

### 1. Create the strategy directory

```bash
STRATEGY_DIR="instances/<mission>/strategies/strategy-<NNN>"
mkdir -p "$STRATEGY_DIR/explorations"
```

### 2. Copy templates

```bash
cp agents/strategizer/templates/state.json "$STRATEGY_DIR/"
cp agents/strategizer/templates/LOOP-STATE.md "$STRATEGY_DIR/"
cp agents/strategizer/templates/HISTORY-OF-REPORT-SUMMARIES.md "$STRATEGY_DIR/"
cp agents/strategizer/templates/REASONING.md "$STRATEGY_DIR/"
cp agents/strategizer/strategizer-stop-hook.sh "$STRATEGY_DIR/"
chmod +x "$STRATEGY_DIR/strategizer-stop-hook.sh"
```

### 3. Create instance-level files (if they don't exist)

```bash
INSTANCE_DIR="instances/<mission>"
# Computation registry — accumulates across strategies
if [ ! -f "$INSTANCE_DIR/COMPUTATIONS-FOR-LATER.md" ]; then
  echo "# Computation Registry" > "$INSTANCE_DIR/COMPUTATIONS-FOR-LATER.md"
  echo "" >> "$INSTANCE_DIR/COMPUTATIONS-FOR-LATER.md"
  echo "Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers." >> "$INSTANCE_DIR/COMPUTATIONS-FOR-LATER.md"
  echo "" >> "$INSTANCE_DIR/COMPUTATIONS-FOR-LATER.md"
fi
```

### 4. Verify STRATEGY.md exists

The Missionary should have already written `STRATEGY.md` in the strategy directory before this setup runs. Verify it exists:

```bash
ls "$STRATEGY_DIR/STRATEGY.md"
```

If it doesn't exist, stop and report back — something went wrong.

### 5. Register the stop hook

Add the hook to `~/.claude/settings.json` under `hooks.Stop`.

Read the current file. If `hooks.Stop` exists, append a new entry to the array. If it doesn't exist, create it. Do not overwrite existing hooks.

The entry to add:

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "<absolute-path-to-strategy-dir>/strategizer-stop-hook.sh"
    }
  ]
}
```

The command path **must be absolute** (e.g., `/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/quantum-gravity/strategies/strategy-001/strategizer-stop-hook.sh`). Relative paths will not work.

### 6. Verify

Confirm the setup by listing the strategy directory contents. It should contain:

```
STRATEGY.md
state.json
LOOP-STATE.md
HISTORY-OF-REPORT-SUMMARIES.md
REASONING.md
strategizer-stop-hook.sh
explorations/
```

Report back with the absolute path to the strategy directory and confirmation that the hook is registered.
