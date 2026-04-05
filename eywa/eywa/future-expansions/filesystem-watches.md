# Filesystem Watches

## Problem
The orchestrator polls every 10 seconds. This means up to 10 seconds of latency between an agent completing its work (writing result.md or plan.md) and the orchestrator noticing and triggering the next transition. Over a deep tree with many transitions, this polling delay accumulates.

## Design
Replace or supplement the polling loop with filesystem watches (e.g., `fswatch` on macOS, `inotifywait` on Linux) that trigger immediately when key files are created or modified.

### Watched files per node
- `output/plan.md` -- triggers review/approval flow
- `output/final-output.md` -- triggers completion
- `output/escalation.md` -- triggers escalation handling
- `for-orchestrator/eval-decision` -- triggers post-evaluation routing

### Hybrid approach
Keep the 10-second poll loop as a safety net (catches anything the watch misses, handles edge cases like node directories created between watch setup), but let filesystem events trigger immediate processing for the common paths.

## Key Considerations
- Platform dependency: `fswatch` (macOS) vs. `inotifywait` (Linux) have different APIs. Need a wrapper or conditional logic.
- Race conditions: a file watch might fire before the file is fully written. Need to ensure atomic writes (write to temp file, then mv) or add a brief delay after the watch triggers.
- Recursive watching: as new child directories are created, new watches must be registered dynamically.
