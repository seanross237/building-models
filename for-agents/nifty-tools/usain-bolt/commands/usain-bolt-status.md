---
description: "Check status of an active Usain Bolt sprint"
allowed-tools: ["Bash(test:*)", "Bash(cat:*)", "Bash(ls:*)"]
---

# Usain Bolt Status

1. Check if `.usain-bolt/USAIN-BOLT-STATE.md` exists: `test -f .usain-bolt/USAIN-BOLT-STATE.md && echo "EXISTS" || echo "NOT_FOUND"`

2. **If NOT_FOUND**: Say "No active sprint found." Then check if `.usain-bolt/` has any report files: `ls .usain-bolt/*-REPORT.md 2>/dev/null` — if so, mention the last sprint's report is available.

3. **If EXISTS**:
   - Read `.usain-bolt/USAIN-BOLT-STATE.md` to get slug, iteration, and max_iterations
   - Read `.usain-bolt/USAIN-BOLT-{slug}-PROGRESS.md` for the work items checklist
   - Give a concise summary:
     - **Sprint**: the slug name
     - **Iteration**: current / max
     - **Completed**: count of checked items
     - **Remaining**: count of unchecked items (list them briefly)
     - **Blocked**: any items marked BLOCKED
   - Keep it short — this is a quick status check
