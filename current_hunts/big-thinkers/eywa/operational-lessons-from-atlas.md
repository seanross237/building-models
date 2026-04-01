# Operational Lessons from Atlas for Eywa Agent Orchestration

Eywa's architecture (ephemeral agents, file-based state, recursive task tree) avoids several of Atlas's early mistakes by design. But the execution details — how you actually spawn agents, detect problems, and keep things moving — have sharp edges that only show up in practice. These are lessons from running 30+ Atlas missions across multiple architectures.

---

## 1. Spawning Agents via tmux

**The 800-character paste limit.** Claude Code silently drops prompts >= 800 characters sent via `tmux send-keys "long prompt" Enter`. It treats rapid large input as a paste, absorbs the Enter, and the session sits at 0% forever — no error, no indication anything is wrong.

**Workaround:** Always separate the text from the Enter keystroke:
```bash
tmux send-keys -t "$SESSION" -l "$PROMPT"
sleep 0.3
tmux send-keys -t "$SESSION" Enter
```

**Better pattern for Eywa:** Don't put task content in the tmux prompt at all. Write the task to a file (e.g., `TASK.md`), then send a short prompt: `"Read TASK.md and execute it."` This is immune to length limits and makes the task inspectable on disk.

## 2. Zombie Detection

Agents can accept a prompt but never start processing — stuck at 0% with no thinking indicator. This happens silently. You cannot rely on the agent to report its own failure.

**What works:**
- Poll the tmux pane every 30-60s. Look for a thinking indicator (spinner + verb + timer) or token counter movement.
- If an agent is at 0% with no indicator for > 3 minutes, it's a zombie.
- First intervention: send a nudge message ("Continue where you left off.")
- Second intervention: Ctrl-C, wait 3s, re-send the task.
- Third intervention: kill the session and re-spawn fresh.

**For Eywa's ephemeral model:** This is actually easier — if a node doesn't produce output within a timeout, kill it and re-spawn. Since state is on disk, re-spawning is free. Don't try to recover a stuck agent; just replace it.

## 3. Completion Detection

Agents need a clear completion signal that external orchestration can detect without parsing output.

**What works in Atlas:** The explorer writes `REPORT-SUMMARY.md` as its last action. A pure-bash operator polls for this file every 30 seconds. When it appears, the operator kills the explorer session and nudges the next agent. Zero tokens spent on polling.

**For Eywa:** Each node should write a `RESULT.md` (or equivalent) as its final action. The parent's orchestration layer watches for this file. Don't have the parent agent poll — use a bash loop or filesystem watch that costs zero tokens.

## 4. The Operator Pattern (Separate Orchestration from Reasoning)

Atlas's biggest cost reduction came from separating tmux plumbing (launching agents, detecting completion, nudging) into a pure-bash script that runs alongside the reasoning agent. The reasoning agent (strategizer) just writes files and waits. The bash script does all the coordination.

**Why this matters:** Every bash command a Claude agent runs re-sends its full context. If the strategizer ran `tmux send-keys` and `sleep` loops itself, each poll would cost thousands of tokens. The operator does the same work for zero tokens.

**For Eywa:** The parent node should NOT be the one spawning and monitoring children. A lightweight bash orchestrator should handle: spawning the child, watching for completion, and waking the parent when results are ready. The parent is re-spawned (ephemeral) only when there's actual work to do — never for polling.

## 5. Ephemeral Agents and State Quality

Eywa is already designed around ephemeral agents — good. Atlas learned this the hard way. Persistent agents accumulate context, grow expensive, and develop framing bias from early work coloring later decisions.

**The critical thing Eywa needs to get right:** State file quality. A re-spawned parent must reconstruct its full decision context from files alone. In Atlas, `REASONING.md` + `HISTORY.md` + `state.json` capture ~90% of what matters, but the missing 10% (half-formed hypotheses, rejected options, vibes about which direction feels right) causes subtle quality loss.

**Recommendation:** Have each node write a `STATE.md` brain dump at the end of every action — not just what it decided, but what it considered and rejected, what its hunches are, and what it would do next and why. This is the "dark knowledge" that structured state files miss.

## 6. Long-Running Computations

If child nodes can run code, some computations will take hours (DNS simulations, parameter sweeps, heavy numerical work). The agent will appear stuck but is actually waiting on a background process.

**What to watch for:**
- Check for running processes (`ps aux | grep python`) before declaring an agent stuck
- Agents should write to a `progress.txt` file periodically so the orchestrator can distinguish "computing" from "stuck"
- Bash command timeout in Claude Code is 10 minutes. Long computations must be broken into stages or run via `run_in_background`.

**For Eywa:** If a node identifies a computation that will exceed ~5 minutes, it should write the code to disk, launch it as a background process, and write a `WAITING_FOR_COMPUTATION` marker file. The orchestrator watches for both the marker (computation started) and the result file (computation finished), then re-spawns the node to continue with the results.

## 7. Cross-Node Knowledge Sharing

Atlas runs multiple systems (Atlas, Philosopher Atlas, Forge) on the same problem. They produce complementary findings but run blind to each other. Knowledge that one system discovered gets re-derived by another, wasting explorations.

**For Eywa:** The tree structure naturally handles this for parent-child knowledge flow. But sibling nodes (parallel children of the same parent) can discover things relevant to each other. The parent should check if completed siblings produced findings that change the remaining siblings' tasks. This is the "continue / replan" decision — don't just continue mechanically, actually read what came back.

## 8. Babysitter Pattern

Even with good orchestration, things go wrong — agents zombie, sessions crash, computations hang. A lightweight periodic check catches these before they block the whole tree.

**What works:** A cron job (every 5-7 minutes) that runs a bash health check. If everything is healthy, it does nothing (zero tokens). If something looks wrong, it spawns a small agent to diagnose and intervene.

**For Eywa:** Build health checking into the orchestration layer, not as a separate system. Each time the orchestrator polls for completion, also check: is the child session alive? Is it making progress (file timestamps moving)? Has it exceeded its time budget? If unhealthy, kill and re-spawn — ephemeral agents make this cheap.
