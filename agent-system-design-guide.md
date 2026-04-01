# How to Build an Autonomous Agent System

This document is a guide for an agent that has been given a goal and needs to design and build a system of agents to accomplish it. Read this entire document before designing anything.

## Core Constraint: Context Windows

Everything in this system follows from one fact: **agents degrade as their context window fills up.** An agent with 10% of its context used on exactly the right information will outperform an agent at 80% context full of semi-relevant material. This is the single most important design constraint.

This means:
- Every agent should wake up with **only what it needs** to do its specific job
- Information should live in files on disk, not in agent memory
- Agents should be **short-lived and focused** — do one thing, write results to disk, exit
- When an agent needs context, it should retrieve it from files at the moment it needs it, not carry it from birth
- Long-running agents will inevitably lose context (the system will compress or truncate). They must be able to **reconstruct their state from files** at any point

## Execution Substrate: Claude Code + tmux

Agents are Claude Code instances running in tmux sessions. This is the foundation.

**Why tmux over sub-agents:**
- tmux sessions are observable — you can check what an agent is doing from outside (`tmux capture-pane`)
- tmux sessions are independent — one agent crashing doesn't kill another
- tmux sessions persist — if a parent agent dies, child sessions keep running
- Sub-agents live inside the parent's context window and consume its tokens. tmux agents don't.

**How to launch an agent in tmux:**
```bash
tmux new-session -d -s <session-name> -c <working-directory>
tmux send-keys -t <session-name> "claude --system-prompt-file <path-to-system-prompt> --permission-mode bypassPermissions" Enter
# Wait for Claude to start (~12 seconds)
tmux send-keys -t <session-name> "<initial instructions>" Enter
```

**How to monitor an agent:**
```bash
tmux capture-pane -t <session-name> -p | tail -20   # see recent output
tmux ls                                                # see all sessions
```

**How to send messages to a running agent:**
```bash
tmux send-keys -t <session-name> "<message>" Enter
```

**Sub-agents are appropriate when:**
- The task is quick (under a few minutes)
- The parent needs the result immediately before it can continue
- The information retrieved is small and directly feeds the parent's next decision

Use sub-agents for retrieval. Use tmux for execution.

## Architecture: Hierarchical Agents

An effective system has multiple levels. This isn't bureaucracy — it's a direct consequence of the context window constraint. No single agent can hold the full picture AND the execution details AND the accumulated results. So you split them.

### The Pattern

```
Goal
 └── Planner (holds the big picture, makes strategic decisions)
      └── Executor (holds one task, does the work, writes results)
           └── [optional deeper levels for complex sub-tasks]
```

**Each level has a fundamentally different job:**

| Level | Holds | Decides | Reads | Writes |
|-------|-------|---------|-------|--------|
| Top (Planner) | The goal, the strategy, progress summaries | What to do next, when to pivot, when to stop | Summaries and evaluations from below | Strategy docs, evaluation notes |
| Middle (Coordinator) | One phase of work, relevant context | How to execute, what information to retrieve, how to decompose | Detailed results from executors, retrieved context | Task specifications, progress logs |
| Bottom (Executor) | One specific task and its context | How to accomplish the task | Goal file, retrieved reference material | Detailed results, summaries |

**How many levels you need depends on the goal's complexity.** A simple goal might need two levels. A complex research mission might need three or four. Start with the minimum and add levels only when a single agent can't hold both the planning context and execution context for a given scope of work.

### Information Flow

Information flows through files on disk. Never rely on agents passing context verbally through a chain — it degrades at every hop.

**Downward (planning → execution):**
- Goal specifications
- Strategy documents
- Retrieved context relevant to the task

**Upward (execution → planning):**
- Result summaries (concise — the planner doesn't need every detail)
- Status signals (completion, failure, unexpected findings)
- Flagged items that need higher-level decisions

**Lateral (across agents at the same level):**
- Shared knowledge stores (libraries, indexes)
- Logs of what's been tried and what happened

### Completion Signals

Agents need unambiguous ways to signal they're done. Writing a specific file is the simplest and most reliable pattern — the parent polls for the file's existence. Examples:
- Write `REPORT-SUMMARY.md` as the last action (its existence means "done")
- Set `"done": true` in a `state.json` file
- The absence of a signal means "still running" or "crashed" — the parent should handle both

## Planning and Adversarial Review

Agents are good at making plans. Plans are often wrong. The system should account for this.

**The cycle:**
1. An agent creates a plan based on the goal and available information
2. The plan is reviewed adversarially — either by a separate agent or by the planning agent explicitly adopting a critic role
3. The plan is revised
4. Execution begins
5. As results come in, the plan is re-evaluated against reality
6. Pivots happen when evidence warrants them — not on every setback, but not never

**What makes a pivot necessary vs. noise:**
- A core assumption of the plan was wrong → pivot
- An approach failed but others within the plan remain → continue
- Unexpected findings open a better path → pivot
- An agent struggled with execution → fix the execution, don't change the plan

**The planner must have access to summarized results** from execution — not raw dumps, but concise assessments of what worked, what didn't, and what was surprising. This is how it decides whether to stay the course or change direction.

## Surviving Context Loss

Long-running agents will lose context. The system will compress old messages. An agent that was lucid at message 10 may be confused by message 200. This is not a bug — it's the operating environment.

**The stop hook pattern:** When a Claude Code session ends (context exhaustion, crash, timeout), a shell script can detect this and restart the agent with a meta-prompt that tells it how to reconstruct its state.

How stop hooks work:
1. Register a shell script in `~/.claude/settings.json` under `hooks.Stop`
2. When Claude stops, the hook fires
3. The hook checks whether to restart (state file says not done, max restarts not hit, right session)
4. If restarting, the hook outputs a JSON message that feeds back into Claude as if the user typed it
5. That message tells the agent: "You just lost context. Read these files to reconstruct your state. Continue from where you left off."

**What must be on disk for reconstruction:**
- Current state (what phase are we in, what has been done, what's next)
- History of results so far (summaries, not full reports)
- The original plan/strategy
- Any accumulated reasoning or decision log

The agent after a restart won't remember its previous reasoning. It will re-derive its understanding from files. **This only works if the files are kept up to date as work progresses.** An agent that does 5 tasks but only writes results for the first 3 will lose tasks 4 and 5 on restart.

**Rule: write state to disk after every meaningful action.** Not at the end — continuously.

## Knowledge Accumulation

A system that only holds knowledge in agent context loses everything when agents die. A system that writes knowledge to disk accumulates it across the entire run and across future runs.

### Factual Knowledge

Things learned about the domain — facts, findings, results, dead ends. Stored in a structured library on disk with an index hierarchy.

**Requirements:**
- Organized by topic, not by when it was discovered
- Indexed — a retrieval agent can quickly find relevant entries without reading everything
- Deduplicated — new findings are checked against existing entries before being added
- A dedicated agent (curator) should process raw results into the library, because the executing agent's job is execution, not librarian work

### Meta Knowledge

Things learned about how the system itself works — what approaches succeed, what goal structures produce good results, what failure modes agents exhibit, how to frame problems.

This is the most important category for self-improvement. It includes:
- What types of plans work well for what types of problems
- How agents behave in practice (stalling patterns, common failure modes)
- What information retrieval patterns produce good context vs. noise
- What level of specificity in goals leads to good execution

Meta knowledge should be stored separately from factual knowledge and surfaced to planning agents when they're designing approaches.

### Retrieval

Knowledge on disk is useless if agents can't find what they need. Build a retrieval mechanism:
- Index files that summarize what's in each section of the library
- A retrieval agent (librarian) that can search indexes, read relevant entries, and return a curated summary
- The retrieval agent is a sub-agent (not tmux) because the parent needs the result immediately

## Self-Improvement

The system should get better over time. This happens at multiple levels.

### Evaluate Components

After each major unit of work, evaluate how the components performed:
- Did the planner's strategy actually work? What would have been better in retrospect?
- Did executors get the context they needed? Were goals well-specified?
- Did retrieval return relevant information? Was important context missed?
- Did the system waste effort on dead ends that could have been caught earlier?

Write these evaluations to the meta knowledge store.

### Modify the System

The system can change its own:
- **Agent prompts** — if a pattern of failure traces back to how an agent was instructed, update the prompt
- **Architecture** — if two levels aren't enough, add a third. If a support agent isn't pulling its weight, remove it
- **Processes** — if the plan-execute-evaluate loop needs an extra step (like adversarial review), add it
- **Information flow** — if agents aren't getting the right context, change how retrieval works or what gets written to disk

**Caution:** Self-modification should be deliberate, not reactive. Change the system based on patterns across multiple instances, not based on a single failure. Log every modification and the reasoning behind it so the change can be evaluated later.

### Logging and Measurement

You can't improve what you don't measure. The system should track:
- **Token usage** per agent per task — are some agents burning context on low-value work?
- **Time** per task — where are the bottlenecks?
- **Efficacy** — did the task accomplish what it was supposed to? (Requires the evaluating agent to score outcomes)
- **Restart count** — how often do agents lose context? Is this increasing?
- **Retrieval quality** — when the librarian returns context, does the executor use it? (Check by comparing retrieval results against what appears in the final output)

Store logs in a dedicated directory. Make them machine-parseable (JSON or structured markdown) so that an analysis agent can process them.

## Putting It All Together: What to Do When Given a Goal

When you receive a goal, here is how to proceed:

1. **Analyze the goal.** What kind of problem is this? How complex? What does success look like? What are the failure modes?

2. **Design the hierarchy.** How many levels of agents are needed? What does each level hold and decide? What files flow between them? Start minimal — you can add complexity later.

3. **Design the information architecture.** What files will exist? What does each contain? How will agents find what they need? Where does knowledge accumulate?

4. **Write the agent prompts.** Each agent's system prompt should contain:
   - Its role and scope (what it's responsible for, what it's NOT responsible for)
   - What files it should read on startup
   - What files it should write and when
   - How to signal completion
   - What to do if it gets stuck or encounters something unexpected
   - How to reconstruct state after context loss

5. **Build the orchestration.** Stop hooks, monitoring, completion detection, restart logic.

6. **Build the evaluation layer.** How will you know if the system is working? What gets measured? When do evaluations trigger?

7. **Launch.** Start the top-level agent with the goal. Monitor the first cycle closely. Intervene only if the system is fundamentally broken, not if it's just slow or imperfect.

8. **After completion, improve.** Review logs, evaluations, and meta knowledge. Modify the system. Run again.

## Common Failure Modes

Anticipate these:

- **Context bloat** — an agent is given too much information and performs poorly. Fix: give it less, retrieve on demand.
- **Silent failure** — an agent crashes or stalls and nobody notices. Fix: polling, health checks, timeout logic in the parent.
- **Plan rigidity** — the planner commits to a strategy and won't pivot despite evidence. Fix: force periodic re-evaluation checkpoints.
- **Knowledge loss** — agents discover things but don't write them down. Fix: make writing to disk part of the task definition, not an afterthought.
- **Infinite loops** — an agent keeps retrying a failed approach. Fix: max retry caps, escalation to a higher-level agent.
- **Over-modification** — the system changes itself too aggressively based on limited data. Fix: require multiple instances of a pattern before modifying.
- **Summary degradation** — summaries passed upward lose critical nuance. Fix: include structured fields (outcome, confidence, surprises, blockers) not just prose.
