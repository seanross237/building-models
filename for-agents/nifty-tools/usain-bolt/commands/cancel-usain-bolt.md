---
description: "Cancel an active Usain Bolt sprint"
allowed-tools: ["Bash(test -f .usain-bolt/USAIN-BOLT-STATE.md:*)", "Bash(rm .usain-bolt/USAIN-BOLT-STATE.md)", "Read(.usain-bolt/USAIN-BOLT-STATE.md)", "Bash(jq:*)"]
---

# Cancel Usain Bolt Sprint

1. Check if `.usain-bolt/USAIN-BOLT-STATE.md` exists using Bash: `test -f .usain-bolt/USAIN-BOLT-STATE.md && echo "EXISTS" || echo "NOT_FOUND"`

2. **If NOT_FOUND**: Say "No active sprint found."

3. **If EXISTS**:
   - Read `.usain-bolt/USAIN-BOLT-STATE.md` to get the current iteration from the `iteration:` field
   - Remove the state file using Bash: `rm .usain-bolt/USAIN-BOLT-STATE.md`
   - Remove the stop hook from settings using Bash:
     ```
     jq '.hooks.Stop = [.hooks.Stop[] | select(.hooks | map(.command) | contains(["./scripts/usain-bolt/usain-bolt-stop-hook.sh"]) | not)]' .claude/settings.local.json > .claude/settings.local.json.tmp && mv .claude/settings.local.json.tmp .claude/settings.local.json
     ```
   - Report: "Cancelled sprint at iteration N. Stop hook removed. Plan files are still in `.usain-bolt/` if you need them."
