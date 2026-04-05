# Meta-Learnings About Atlas

Lessons learned from running Atlas, observed firsthand. Updated as we learn more.

---

## Token Cost

### The strategizer polling problem

**The problem:** Strategizers ignore the "use background file-watches" instruction and poll explorer status in a loop. Each bash call re-sends the entire conversation history. One strategizer made 1,019 bash calls at ~250K tokens average = 255M tokens wasted. That was **82% of the entire strategy's budget** spent on "is it done yet?" instead of science.

**The fix (deployed):** Rewrote the strategizer system prompt with:
- A concrete horror story ("1,019 bash calls, 255M tokens wasted, 82% of budget")
- A hard rule ("your very next tool call MUST be a background file-watch, then STOP")
- An explicit ban list of every specific polling action observed
- Removed the "one quick status check" escape hatch they were exploiting

**Result:** After the rewrite, the restarted strategizer dropped from 125+ shells to 1-3. The fix works when the strategizer loads the updated prompt. Strategy-002 got a fresh strategizer that reverted to polling — the prompt needs to be loaded at strategy creation time, not just updated on disk.

**Lesson:** Abstract instructions ("don't poll") get ignored. Concrete consequences + hard rules + explicit ban lists work. Remove escape hatches.

### The babysitter problem

**The problem:** Running the babysitter as a cron prompt inside a long-lived Claude session. Every check re-sends the full conversation. After 8 hours: 292 checks × 127K avg = 37M tokens, when the actual new work per check was ~584K.

**The fix (deployed):** Replaced with a bash script (`execution/babysitter/check.sh`) that pattern-matches known states (zero tokens). Only spawns a fresh, short-lived Claude instance for unknown scenarios (~5K tokens). The Claude instance can update the bash script to handle the unknown pattern next time — self-improving.

**Result:** ~99.7% token reduction. See `docs_and_guides/babysitter-guide.md` for full details.

**Lesson:** Don't use an LLM for tasks that are 95%+ pattern matching. Use bash for the common case, LLM for the exceptions.

### Context growth is the hidden cost

Every API call in a Claude session re-sends the full conversation history. This means:
- A babysitter check that takes 2K of new tokens costs 130K because of the 128K of prior conversation
- A strategizer status check that takes 500 tokens of new work costs 250K because of accumulated context
- The longer a session runs, the more expensive each action becomes

**Lesson:** For repetitive monitoring tasks, use fresh short-lived sessions or bash scripts. Reserve long-lived sessions for work that genuinely needs conversational context.

---

## Agent Behavior

### Explorers don't write files to disk

**Observed twice in the NS mission.** Explorers complete their analysis, show deliverables in their terminal output ("REPORT.md — 328 lines, REPORT-SUMMARY.md — 42 lines"), but never actually write the files. The strategizer's file-watch waits forever.

**Worse:** One explorer wrote files to the wrong directory (exploration-002/ instead of exploration-003/) because it got confused about its working directory after a context reset.

**Current fix:** The babysitter catches this (session idle but no REPORT-SUMMARY.md) and nudges. But this is reactive — we should prevent it.

**Potential fix:** Add to explorer system prompt: "After writing REPORT-SUMMARY.md, verify it exists on disk with `ls -la REPORT-SUMMARY.md`. If it doesn't exist, you didn't write it — write it now." Could also add a check to the strategizer: if the explorer session exits but REPORT-SUMMARY.md doesn't exist, treat as failed.

### Explorers hit the 10-minute bash timeout

**The problem:** Claude Code has a hard 10-minute timeout on foreground bash commands. NS simulations at N=64/128 often exceed this. Explorer-006 ran the same script three times, hitting the wall each time, before pivoting.

**Workarounds explorers discovered:**
1. **Reduced resolution** for broad searches (N=32 for 120-point parameter sweep), higher resolution only for convergence checks
2. **Background mode** (`run_in_background=true`) + sleep polling (`sleep 300 && cat results.txt`)

**Fix (deployed):** Updated both explorer system prompts to explicitly teach background mode, progress files, and intermediate result saving. Future explorers know from the start.

**Lesson:** If you know agents will hit a constraint, teach them the workaround in the system prompt. Don't rely on them discovering it themselves — it wastes explorations.

### Strategizers can't "do nothing"

Even with explicit instructions to wait, strategizers struggle to be idle. They look for productive things to do, which means running bash commands, which means burning tokens. The anti-polling fix helps but the underlying tendency remains.

**Lesson:** "Do nothing and wait" is one of the hardest instructions for an LLM agent to follow. The best fix is mechanical — background file-watches that make "doing nothing" the default by not returning until there's something to do.

### Stop hooks cause permission prompts on every launch

**The problem:** The missionary system prompt instructed setting up a stop hook in `~/.claude/settings.json` on every launch. This triggered a permission prompt that blocked the agent until the babysitter approved it.

**Fix (deployed):** Removed stop hook setup from the missionary system prompt and SETUP-GUIDE. The babysitter covers the same crash-detection functionality (with a ~7 minute delay instead of immediate).

**Lesson:** Avoid agent actions that require interactive approval. If something needs to be in settings.json, put it there before launch, not during.


---

## Operational

### Rate limits pause everything

When agents hit rate limits, all progress stops until the limit resets. This is especially painful with parallel explorers — all of them hit the limit simultaneously because they share an account.

**Current mitigation:** The babysitter nudges with "continue" on each check. Agents sometimes figure out to wait and retry.

**No good fix exists** beyond having higher rate limits or staggering agent launches.

### Orphaned processes accumulate

Killing tmux sessions doesn't kill the Claude processes they spawned. These orphan processes sit idle using RAM. They don't burn tokens (idle processes make no API calls) but they clutter the process list and can confuse monitoring.

**Fix:** After killing sessions, also kill orphaned claude processes. Or accept the clutter — they're harmless.

### Clean launches need a checklist

To start a mission cleanly:
1. Kill all prior sessions (`tmux kill-server` or targeted kills)
2. Remove stale stop hooks from `~/.claude/settings.json`
3. Clean instance directory (remove strategies/*, library-inbox/*, meta-inbox/*)
4. Verify system prompts are up to date
5. Launch missionary, note timestamp
6. Start babysitter (`check.sh` on a cron or timer)

We've done this three times for the NS mission. Should be scripted.
