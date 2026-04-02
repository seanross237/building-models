#!/bin/bash
# Token usage for Forge mission m001-vasseur-pressure
# Parses JSONL transcripts for real input/output/cache counts.
# Usage: ./token-usage.sh

set -euo pipefail

python3 << 'PYEOF'
import json, os, glob

project_base = os.path.expanduser("~/.claude/projects")
mission_pattern = "vasseur-pressure"

# Find all project dirs matching this mission
all_dirs = []
for d in os.listdir(project_base):
    full = os.path.join(project_base, d)
    if os.path.isdir(full) and mission_pattern in d:
        all_dirs.append(full)

def agent_role(dirname):
    d = dirname.lower()
    if "task" in d:
        parts = d.split("-")
        for i, p in enumerate(parts):
            if p == "task" and i+1 < len(parts):
                return f"worker (task-{parts[i+1]})"
        return "worker"
    elif "plan" in d and "task" not in d:
        return "planner"
    else:
        return "other"

grand = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0}
rows = []

for d in sorted(all_dirs):
    for jf in sorted(glob.glob(os.path.join(d, "*.jsonl"))):
        totals = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0}
        # Only count the final snapshot per message.id to avoid duplicates
        messages = {}
        for line in open(jf):
            try:
                rec = json.loads(line)
                msg = rec.get("message", {})
                if not isinstance(msg, dict):
                    continue
                usage = msg.get("usage")
                mid = msg.get("id", "") or rec.get("messageId", "")
                if usage and mid:
                    messages[mid] = usage
            except:
                pass

        for usage in messages.values():
            totals["input"] += usage.get("input_tokens", 0)
            totals["output"] += usage.get("output_tokens", 0)
            totals["cache_create"] += usage.get("cache_creation_input_tokens", 0)
            totals["cache_read"] += usage.get("cache_read_input_tokens", 0)

        if totals["input"] + totals["output"] > 0:
            role = agent_role(os.path.basename(d))
            rows.append((role, totals))
            for k in grand:
                grand[k] += totals[k]

print("=== m001-vasseur-pressure — Token Usage ===")
print()
if rows:
    for role, t in rows:
        print(f"  {role:<25s}  in: {t['input']:>8,}  out: {t['output']:>8,}  cache_w: {t['cache_create']:>8,}  cache_r: {t['cache_read']:>8,}")
    print(f"  {'─'*80}")
    print(f"  {'TOTAL':<25s}  in: {grand['input']:>8,}  out: {grand['output']:>8,}  cache_w: {grand['cache_create']:>8,}  cache_r: {grand['cache_read']:>8,}")
    print(f"\n  All tokens: {sum(grand.values()):,}")
else:
    print("  No transcript data found yet.")
PYEOF
