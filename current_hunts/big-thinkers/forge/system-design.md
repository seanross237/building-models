# Forge — General-Purpose Autonomous Agent System

## What This Is

Forge is an autonomous agent system that takes any goal — research, engineering, analysis, creative — and builds the right agent hierarchy to accomplish it. It self-improves by accumulating meta-knowledge about what works, modifying its own prompts and architecture over time.

The design follows the principles in `agent-system-design-guide.md` and draws on lessons from Atlas (a research-specific implementation in `current_hunts/atlas/`). Forge generalizes the pattern: instead of a fixed three-level hierarchy, it dynamically constructs the hierarchy depth and agent specializations based on the goal.

---

## Table of Contents

1. [Core Design Principles](#core-design-principles)
2. [File Structure](#file-structure)
3. [Bootstrapping: From Raw Goal to Running System](#bootstrapping-from-raw-goal-to-running-system)
4. [Agent Types](#agent-types)
5. [Information Flow](#information-flow)
6. [Orchestration Mechanics](#orchestration-mechanics)
7. [The Self-Improvement Loop](#the-self-improvement-loop)
8. [Logging and Measurement](#logging-and-measurement)
9. [How Hierarchy Depth Is Decided](#how-hierarchy-depth-is-decided)
10. [Goal-Type Adaptations](#goal-type-adaptations)
11. [Failure Modes and Mitigations](#failure-modes-and-mitigations)
12. [Complete Agent Prompt Specifications](#complete-agent-prompt-specifications)

---

## Core Design Principles

These are not aspirational — they are load-bearing constraints that every design decision must satisfy.

1. **Context windows degrade.** An agent at 10% context with the right information beats one at 80% with semi-relevant material. Every agent wakes up with only what it needs for its specific job. Information lives on disk, not in memory.

2. **Agents are short-lived and focused.** One job, write results, exit. Long-running agents reconstruct state from files after context loss.

3. **tmux over sub-agents for execution.** Sub-agents are for quick retrieval where the parent needs the result before continuing. Execution work goes into tmux sessions — observable, independent, persistent.

4. **Files are the system bus.** All inter-agent communication happens through files on disk. No verbal chain-passing between agents.

5. **Write state continuously.** After every meaningful action, state goes to disk. An agent that completes 5 tasks but only writes 3 loses the other 2 on restart.

6. **Self-modification is deliberate.** Change based on patterns across multiple instances, not single failures. Log every modification and the reasoning.

---

## File Structure

```
forge/
  CLAUDE.md                              # Points agents to system docs
  system/
    bootstrap/
      architect-prompt.md                # The Architect agent's system prompt
      goal-analyzer-prompt.md            # Sub-agent for goal classification
    agents/
      conductor/
        system-prompt.md                 # The Conductor (top-level loop runner)
        conductor-stop-hook.sh           # Template stop hook for conductor loop
        templates/                       # state.json, LOOP-STATE.md, HISTORY.md, REASONING.md
      planner/
        system-prompt.md                 # The Planner (strategy/decomposition)
        planner-stop-hook.sh             # Template stop hook for planner loop
        templates/
      worker/
        system-prompt.md                 # Standard Worker (execution)
      specialist-workers/
        code-worker-prompt.md            # Software engineering variant
        research-worker-prompt.md        # Research/literature variant
        analysis-worker-prompt.md        # Data analysis variant
        creative-worker-prompt.md        # Writing/design variant
        math-worker-prompt.md            # Computation/formal verification variant
      library/
        factual/                         # Domain knowledge, organized by topic
          INDEX.md
        meta/                            # System operational knowledge
          INDEX.md
          goal-design/                   # How to write good task specs
            INDEX.md
          methodology/                   # What approaches work for what problems
            INDEX.md
          system-behavior/               # How agents actually behave
            INDEX.md
          conductor/                     # Lessons from conductor cycles
            INDEX.md
          architecture/                  # Lessons about hierarchy decisions
            INDEX.md
        curator/
          system-prompt.md               # Curator agent
        librarian/
          system-prompt.md               # Librarian/retrieval agent
        curator-log.md
        librarian-log.md
    orchestration/
      SETUP-GUIDE.md                     # Infrastructure setup instructions
      LOOP-STOP-HOOK-GUIDE.md            # Stop hook reference (copy from Atlas)
      health-monitor-prompt.md           # Health monitor agent prompt
    measurement/
      log-schema.md                      # Schema for structured logs
      analyzer-prompt.md                 # Log analysis agent prompt
  missions/
    <mission-id>/
      GOAL.md                            # Original goal as received
      GOAL-ANALYSIS.md                   # Architect's analysis and plan
      ARCHITECTURE.md                    # Chosen hierarchy and agent types
      MISSION-COMPLETE.md                # Written when mission succeeds
      COMPUTATIONS-FOR-LATER.md          # Deferred work items
      library-inbox/                     # Reports waiting for curator
      meta-inbox/                        # Meta-learning notes
      logs/                              # Structured measurement logs
        token-usage.jsonl
        timing.jsonl
        efficacy.jsonl
        restarts.jsonl
        retrieval-quality.jsonl
      strategies/
        strategy-NNN/
          STRATEGY.md                    # Methodology for this strategy
          FINAL-REPORT.md                # Written when strategy completes
          state.json                     # Machine-readable state
          HISTORY.md                     # Accumulated summaries from tasks
          REASONING.md                   # Decision log + librarian query logs
          LOOP-STATE.md                  # Stop hook control
          conductor-stop-hook.sh         # or planner-stop-hook.sh (copied from template)
          tasks/
            task-NNN/
              SPEC.md                    # What the worker was told to do
              RESULT.md                  # Detailed output
              RESULT-SUMMARY.md          # Concise summary (existence = completion signal)
              code/                      # For code/math workers
              artifacts/                 # For creative/analysis workers
  improvement/
    modifications-log.md                 # Every system modification with reasoning
    prompt-versions/                     # Versioned copies of modified prompts
      conductor-v001.md
      conductor-v002.md
      ...
    analysis-reports/                    # Output from the Analyzer agent
```

---

## Bootstrapping: From Raw Goal to Running System

When Forge receives a goal, the **Architect** agent runs first. The Architect is the only agent that is not part of the running hierarchy — it designs the hierarchy, then exits.

### Step 1: Goal Analysis

The Architect spawns a **Goal Analyzer** sub-agent that classifies the goal along these dimensions:

| Dimension | Options | Example |
|-----------|---------|---------|
| **Type** | research, engineering, analysis, creative, hybrid | "Build a web scraper" = engineering |
| **Complexity** | simple (1-2 tasks), moderate (3-10 tasks), complex (10+ tasks, multiple phases) | "Summarize this paper" = simple |
| **Uncertainty** | low (clear path), medium (known approach, unknown details), high (unknown approach) | "Prove the Riemann Hypothesis" = high |
| **Measurability** | binary (works/doesn't), continuous (quality spectrum), subjective (judgment needed) | "Fix this bug" = binary |
| **Decomposability** | serial (steps depend on each other), parallel (independent sub-problems), mixed | "Survey 5 frameworks" = parallel |
| **Domain** | what existing library knowledge applies | Check factual library INDEX.md |

The Goal Analyzer reads the meta library's `methodology/INDEX.md` and `architecture/INDEX.md` for lessons from previous missions about what goal types benefit from what structures. It writes `GOAL-ANALYSIS.md` with its classification and reasoning.

### Step 2: Architecture Decision

The Architect reads `GOAL-ANALYSIS.md` and decides:

1. **How many hierarchy levels.** (See [How Hierarchy Depth Is Decided](#how-hierarchy-depth-is-decided))
2. **What agent types at each level.** (Standard vs. specialist workers, single vs. multiple planners)
3. **What the information flow looks like.** (What files flow between levels, what gets summarized vs. passed in full)
4. **Whether to use strategies.** (High-uncertainty goals get a strategy loop; low-uncertainty goals may skip it)

The Architect writes `ARCHITECTURE.md` with:
- The hierarchy diagram
- Each agent's role, what it reads, what it writes, what signals completion
- The file structure for this mission
- Which specialist worker types are needed
- The stop hook configuration

### Step 3: Adversarial Review

The Architect spawns a **Critic** sub-agent that reads `GOAL-ANALYSIS.md` and `ARCHITECTURE.md` and tries to find flaws:
- Is the hierarchy too deep for the goal's complexity? (Over-engineering wastes tokens)
- Is it too shallow? (A single worker can't hold both planning context and execution details for complex goals)
- Are there information flow gaps? (An agent needs something that nothing produces)
- Are there obvious failure modes not accounted for? (What happens if the main approach fails? Is there a pivot mechanism?)

The Critic writes its findings to `ARCHITECTURE.md` (appended as a review section). The Architect revises if needed.

### Step 4: Infrastructure Setup

The Architect creates the mission directory structure, copies the relevant prompt templates, configures stop hooks in `~/.claude/settings.json`, and writes the initial `STRATEGY.md` (or `SPEC.md` for simple goals that skip the strategy layer).

### Step 5: Launch

The Architect launches the top-level agent (Conductor or Planner, depending on hierarchy depth) in a tmux session and exits.

```bash
# Example launch for a complex goal (3-level hierarchy)
MISSION_DIR="/path/to/forge/missions/<mission-id>"

tmux new-session -d -s forge-conductor-<id> -c "$MISSION_DIR/strategies/strategy-001"
tmux send-keys -t forge-conductor-<id> "claude --system-prompt-file /path/to/forge/system/agents/conductor/system-prompt.md --permission-mode bypassPermissions" Enter
# Wait ~12 seconds
tmux send-keys -t forge-conductor-<id> "Fresh start. Your session prefix is '<id>'. Read state.json, STRATEGY.md, GOAL.md (two levels up). Begin your startup sequence." Enter
```

---

## Agent Types

### Architect (One-shot, runs during bootstrap only)

**Role:** Analyze a goal, design the hierarchy, set up infrastructure, launch the system.

**Reads:**
- The raw goal
- `system/agents/library/meta/methodology/INDEX.md` (lessons about what works)
- `system/agents/library/meta/architecture/INDEX.md` (lessons about hierarchy decisions)
- Previous mission `GOAL-ANALYSIS.md` and `ARCHITECTURE.md` files (if they exist) for pattern matching

**Writes:**
- `missions/<id>/GOAL.md` (the goal, preserved verbatim)
- `missions/<id>/GOAL-ANALYSIS.md` (classification, reasoning)
- `missions/<id>/ARCHITECTURE.md` (hierarchy design, reviewed)
- `missions/<id>/strategies/strategy-001/STRATEGY.md` (initial methodology)
- All directory structure and template files
- Stop hook configuration in `~/.claude/settings.json`

**Completion signal:** Launches the top-level agent in tmux, then exits.

**Sub-agents used:**
- Goal Analyzer (foreground, quick classification)
- Critic (foreground, adversarial review of architecture)

---

### Conductor (Top-level loop, only for complex goals)

**Role:** Own the mission. Evaluate strategy results. Decide whether to continue, pivot, or declare completion. Write new strategies when needed. This is the equivalent of Atlas's Missionary.

The Conductor does NOT execute work. It reads, evaluates, and decides. Its output is a `STRATEGY.md` that it hands to a Planner.

**Reads on startup:**
- `../../GOAL.md` and `../../GOAL-ANALYSIS.md` (the mission)
- `../../ARCHITECTURE.md` (the system design)
- `STRATEGY.md` (current strategy)
- `system/agents/library/meta/conductor/INDEX.md` (lessons from previous conductors)
- Previous strategy `FINAL-REPORT.md` files (cross-strategy knowledge)

**Reads when a strategy completes:**
- `FINAL-REPORT.md` (what was found)
- `HISTORY.md` (what each task produced)
- `REASONING.md` (how the planner made decisions)
- `../../meta-inbox/` (meta-learning notes from the planner)

**Writes:**
- `strategies/strategy-NNN/STRATEGY.md` (methodology for each new strategy)
- `../../MISSION-COMPLETE.md` (when the mission is done)
- `system/agents/library/meta/conductor/` entries (lessons for future conductors)
- Updates `system/agents/library/meta/conductor/INDEX.md`

**Completion signal:** Writes `MISSION-COMPLETE.md` in the mission root.

**Orchestration:** Runs in a tmux session. Launched by the Architect. Idle while Planner runs. Woken by the Planner sending a tmux message when strategy completes. For simple missions that don't need strategy iteration, this level is omitted entirely — the Planner reports directly to the mission's `MISSION-COMPLETE.md`.

**Stop hook:** The Conductor does NOT run in a stop hook loop by default. It wakes, evaluates, writes, launches, and sleeps. If a strategy is in progress, the Conductor is dormant. The Planner sends a tmux message to wake it. If the Conductor's context expires while dormant, the Planner's tmux message will restart it naturally (Claude Code re-enters when it receives input). If the Conductor needs to actively monitor (a future expansion), a stop hook can be added.

---

### Planner (Middle-level loop)

**Role:** Own a single strategy. Run the task loop — design tasks, launch workers, process results, adapt approach. This is the equivalent of Atlas's Strategizer.

The Planner is the workhorse of the system. It decides what specific work to do within the methodology the Conductor (or Architect, for 2-level systems) defined. It has pacing autonomy — suggested budgets are starting estimates, not fixed allocations.

**Reads on startup / context reset:**
1. `state.json` (current iteration, phase, what's been done)
2. `STRATEGY.md` (methodology)
3. `HISTORY.md` (summaries of all completed tasks)
4. Previous strategy `FINAL-REPORT.md` files (if they exist)
5. `../../COMPUTATIONS-FOR-LATER.md` (deferred work items from previous tasks)

**Reads each iteration:**
- Librarian query results (via foreground sub-agent)
- `RESULT-SUMMARY.md` from completed workers

**Writes:**
- `tasks/task-NNN/SPEC.md` (task specification for each worker)
- `HISTORY.md` (appends each task's summary)
- `REASONING.md` (decision log, librarian query logs)
- `../../COMPUTATIONS-FOR-LATER.md` (updates with newly identified deferred items)
- `../../meta-inbox/meta-task-NNN.md` (meta-learning notes)
- `FINAL-REPORT.md` (when strategy completes)
- `state.json` (after every task)

**Completion signal:** Sets `"done": true` in `state.json`. Sends a tmux message to the Conductor (or writes `MISSION-COMPLETE.md` directly for 2-level systems).

**Orchestration:** Runs in a tmux session with a stop hook loop. When context exhausts, the stop hook fires and feeds a meta-prompt back in. The Planner reconstructs state from `state.json`, `STRATEGY.md`, and `HISTORY.md`.

**Task budget:** Up to 15 tasks per strategy (configurable via `ARCHITECTURE.md`). Must try at least 3 substantially different approaches before declaring a strategy exhausted.

**Parallel workers:** Can launch multiple workers in parallel for independent tasks. Processes results one at a time to avoid curator conflicts.

**state.json schema:**
```json
{
  "iteration": 0,
  "done": false,
  "current_task": null,
  "current_approach": null,
  "approaches_tried": [],
  "tasks_completed": [],
  "task_budget": 15
}
```

Each approach:
```json
{
  "name": "Descriptive name of the approach",
  "status": "active | exhausted | succeeded",
  "tasks": ["task-001", "task-002"],
  "outcome": "One-line summary"
}
```

Each completed task:
```json
{
  "id": "task-001",
  "worker_type": "standard | code | research | analysis | creative | math",
  "spec_summary": "Brief description",
  "outcome": "succeeded | failed | inconclusive | timed_out",
  "key_finding": "One-line takeaway"
}
```

---

### Worker (Bottom-level, single execution)

**Role:** Execute a single task. Receive a spec, do the work, write results, exit. This is the equivalent of Atlas's Explorer.

Workers have no memory of prior tasks and no knowledge of the broader strategy. Their entire context window is available for the task at hand.

**Reads:**
- `SPEC.md` (everything the worker needs — the Planner provides all context)

**Writes:**
- `RESULT.md` (detailed output, written incrementally)
- `RESULT-SUMMARY.md` (concise summary, written LAST as completion signal)
- `code/` directory (for code and math workers)
- `artifacts/` directory (for creative and analysis workers)

**Completion signal:** `RESULT-SUMMARY.md` exists.

**Orchestration:** Runs in its own tmux session. The Planner monitors by polling for `RESULT-SUMMARY.md` existence and `RESULT.md` line count growth. Gets killed if stuck for too long after nudging.

**RESULT-SUMMARY.md required sections:**
```markdown
## Goal
What was asked.

## Approach
What was tried.

## Outcome
succeeded | failed | inconclusive

## Key Finding
The one thing the Planner needs to know.

## Leads
Anything worth pursuing next.

## Unexpected Findings
Discoveries outside the task's scope. "None" is acceptable.

## Deferred Work
Computations or tasks identified but not completable in this execution.
Specific enough to be actionable: what to compute, what inputs, what it would tell us.
```

**Incremental writing rule:** Workers MUST write to `RESULT.md` incrementally. Skeleton first (title, headers, goal summary), then append after every 2-3 meaningful actions. Partial findings on disk are infinitely more valuable than perfect findings only in context.

#### Worker Variants

| Variant | System Prompt | When to Use | Special Capabilities |
|---------|--------------|-------------|---------------------|
| **Standard** | `worker/system-prompt.md` | General tasks, coordination, mixed work | None special |
| **Code Worker** | `specialist-workers/code-worker-prompt.md` | Building software, fixing bugs, refactoring | Full shell access, writes to `code/`, runs tests |
| **Research Worker** | `specialist-workers/research-worker-prompt.md` | Literature surveys, fact-finding, synthesis | Web search, sub-agent delegation for large surveys |
| **Analysis Worker** | `specialist-workers/analysis-worker-prompt.md` | Data analysis, statistics, visualization | Python/pandas/matplotlib, writes to `artifacts/` |
| **Creative Worker** | `specialist-workers/creative-worker-prompt.md` | Writing, design, content creation | Writes to `artifacts/`, iterative revision |
| **Math Worker** | `specialist-workers/math-worker-prompt.md` | Computation, formal verification, proofs | Python/scipy/sympy, Lean 4, tags claims as VERIFIED/COMPUTED/CHECKED/CONJECTURED |

The Planner chooses the worker variant based on the task. The heuristic: if the task's success criteria can be satisfied by running code, use Code or Math Worker. If it requires reading and reasoning about sources, use Research Worker. If it requires producing a deliverable (document, design), use Creative Worker. For data-heavy tasks, Analysis Worker. For anything else, Standard.

---

### Librarian (Foreground sub-agent, retrieval)

**Role:** Search the factual and meta libraries for information relevant to a query. Called by the Planner before each task.

**Reads:**
- The Planner's query (what it's about to explore, what context would help)
- `library/factual/INDEX.md` (drill into topic indexes as needed)
- `library/meta/INDEX.md` (operational lessons)
- `meta-inbox/` (uncurated recent notes)

**Writes:**
- Returns findings directly to the calling agent (it's a foreground sub-agent)
- Appends to `library/librarian-log.md` (what was searched, what was found, what was skipped)

**Why sub-agent not tmux:** The Planner needs the results immediately before it can design the next task's SPEC.md. The information is small and directly feeds the Planner's next decision.

---

### Curator (Fire-and-forget, library maintenance)

**Role:** Process task results into the factual library and meta-learning notes into the meta library. Launched in tmux after each task — the Planner does not wait.

**Reads:**
- The report from `library-inbox/`
- The meta note from `meta-inbox/`
- Existing library entries (to check for duplicates, conflicts)
- All `INDEX.md` files in the affected paths

**Writes:**
- New entries in `library/factual/` (organized by topic)
- New entries in `library/meta/` (organized by category)
- Updates ALL `INDEX.md` files from root to leaf
- Appends to `library/curator-log.md`
- Deletes processed reports from `library-inbox/`

**Completion signal:** None needed — fire-and-forget. Monitor via `curator-log.md`.

---

### Health Monitor (Periodic, background)

**Role:** Check system health. Detect stuck agents, crashed sessions, growing logs, stale state. Optional — the Planner's polling covers the basic case. The Health Monitor is for missions that run long enough that system-level issues accumulate.

**Reads:**
- `tmux ls` output (what sessions exist)
- `state.json` files (are iterations progressing?)
- `logs/` directory (are logs growing?)
- Worker `RESULT.md` files (is line count advancing?)

**Writes:**
- Alerts to a health log at `missions/<id>/logs/health.log`
- Can kill stuck tmux sessions
- Can reset LOOP-STATE.md for crashed planners

**Orchestration:** Runs in its own tmux session on a stop-hook timer (fires every N minutes). Not part of the agent hierarchy — it's infrastructure.

---

### Analyzer (On-demand, post-mission)

**Role:** Read structured logs and produce analysis of system performance. Triggered after mission completion or on-demand.

**Reads:**
- `logs/token-usage.jsonl`
- `logs/timing.jsonl`
- `logs/efficacy.jsonl`
- `logs/restarts.jsonl`
- `logs/retrieval-quality.jsonl`

**Writes:**
- `improvement/analysis-reports/mission-<id>-analysis.md`
- Recommendations for system modifications

---

### Evolver (On-demand, post-analysis)

**Role:** Read analysis reports and meta-knowledge, then modify the system. Changes agent prompts, adjusts architecture defaults, updates methodology recommendations.

**Reads:**
- `improvement/analysis-reports/` (performance data)
- `library/meta/` (operational lessons)
- `improvement/modifications-log.md` (history of past changes)
- Current agent prompts (to modify them)

**Writes:**
- Modified agent prompts (new versions in `improvement/prompt-versions/`)
- Copies new versions into `system/agents/` (the live prompts)
- Appends to `improvement/modifications-log.md` with reasoning
- Updates `library/meta/architecture/` if hierarchy defaults change

**Safeguards:**
- Never modifies based on a single instance — requires evidence from 3+ missions
- Always preserves previous prompt versions
- Logs every change with the reasoning and evidence
- Changes are granular (one thing at a time) so they can be evaluated individually

---

## Information Flow

### Downward (planning to execution)

```
Conductor → Planner: STRATEGY.md
  Contains: objective, methodology, validation criteria, context from prior strategies

Planner → Worker: SPEC.md
  Contains: specific goal, success/failure criteria, relevant context from librarian,
            everything the worker needs (it has no other context)
```

### Upward (execution to planning)

```
Worker → Planner: RESULT-SUMMARY.md
  Contains: goal, approach, outcome, key finding, leads, unexpected findings, deferred work
  Structured fields, not just prose.

Planner → Conductor: FINAL-REPORT.md
  Contains: what was accomplished, approaches tried, most promising findings,
            recommendations for next strategy, novel claims (if applicable)
```

### Lateral (shared knowledge)

```
All agents ← Factual Library: domain knowledge organized by topic
All agents ← Meta Library: operational lessons organized by category
Workers → library-inbox/: raw reports for curator processing
Planners → meta-inbox/: meta-learning notes for curator processing
```

### Deferred work

```
Workers flag → COMPUTATIONS-FOR-LATER.md (at mission level)
Planners read and update → same file
Persists across strategies
```

### Meta-knowledge flow (the self-improvement channel)

```
Workers → meta-inbox/ → Curator → meta library
Planners → meta-inbox/ → Curator → meta library
Conductors → directly to meta library (conductor/ section)
Analyzer → improvement/analysis-reports/
Evolver → reads analysis + meta library → modifies system
```

---

## Orchestration Mechanics

### Stop Hooks

Stop hooks keep long-running agents alive across context resets. They are the core of autonomous operation.

**How they work:**
1. A shell script is registered in `~/.claude/settings.json` under `hooks.Stop`
2. When Claude finishes responding and would normally wait for input, the hook fires
3. The hook checks whether to restart (state says not done, max restarts not hit, right session)
4. If restarting, outputs JSON with `"decision": "block"` and a meta-prompt as the `"reason"`
5. Claude receives the meta-prompt as if the user typed it and continues

**Which agents get stop hooks:**
- **Planner:** Always. It's the primary loop runner. Its stop hook checks `state.json` for `"done": true` and `LOOP-STATE.md` for active status.
- **Conductor:** Only if actively monitoring (not the default). Usually dormant and woken by Planner's tmux message.
- **Workers:** Never. They're single-execution. If they crash, the Planner detects it and treats the task as failed.
- **Curator:** Never. Fire-and-forget. If it crashes, knowledge isn't catalogued but the raw report is still in `library-inbox/`.

**Stop hook template** (stored at `system/agents/conductor/conductor-stop-hook.sh` and `system/agents/planner/planner-stop-hook.sh`):

The template is copied into each strategy directory during setup. It follows the pattern from `LOOP-STOP-HOOK-GUIDE.md`:

1. Read hook input from stdin (JSON with session_id, transcript_path, cwd, etc.)
2. Check PAUSE_HOOK file (emergency stop)
3. Check `state.json` for `"done": true` (strategy complete — let session die)
4. Check LOOP-STATE.md exists and is active
5. Session-awareness: compare `transcript_path` to stored value in LOOP-STATE.md. First fire claims the session; subsequent fires only match the claimed session.
6. Max iterations safety cap
7. Increment iteration counter
8. Output JSON with meta-prompt telling the agent to read state files and continue

**The meta-prompt** fed back to the Planner on restart:

```
You are in an autonomous execution loop. Your context was just reset.

## Reconstruction Steps
1. Read state.json — know what iteration you're on, what phase, what's done
2. Read STRATEGY.md — your methodology
3. Read HISTORY.md — summaries of all completed tasks
4. Read REASONING.md (last 2-3 entries only) — your recent decisions
5. Check for any running worker tmux sessions (tmux has-session -t <prefix>-worker-NNN)
6. If a worker finished while you were down, process its RESULT-SUMMARY.md
7. Continue from where you left off

## Rules
- Do not re-read the entire REASONING.md — it may be very long. Read the last few entries.
- Do not re-run completed tasks. Trust HISTORY.md.
- Update state.json after every action.
```

### Monitoring and Health Checks

**Planner monitors workers:**
- Polls every 5 minutes: `test -f tasks/task-NNN/RESULT-SUMMARY.md && echo "DONE" || echo "RUNNING"`
- Checks `RESULT.md` line count growth: `wc -l tasks/task-NNN/RESULT.md 2>/dev/null`
- If line count stalls for 15+ minutes: capture pane (`tmux capture-pane -t <prefix>-worker-NNN -p | tail -15`)
- If stuck: nudge via tmux send-keys
- If still stuck after 10 more minutes: kill session, mark task as timed_out

**Conductor monitors Planner (when active):**
- Checks `state.json` for iteration progress
- Checks LOOP-STATE.md for active/stalled
- Reads `REASONING.md` tail for recent activity

**Health Monitor (optional, for long missions):**
- Runs on its own timer
- Checks `tmux ls` for expected sessions
- Checks state.json timestamps
- Alerts to health log
- Can auto-restart crashed planners by resetting LOOP-STATE.md

### Emergency Stop

Three levels:

1. **Pause a strategy:** `touch missions/<id>/strategies/strategy-NNN/PAUSE_HOOK`
2. **Kill a specific session:** `tmux kill-session -t forge-planner-<id>`
3. **Kill everything:** `tmux kill-server`

### Session Naming Convention

All tmux sessions use a mission-specific prefix to avoid collisions when multiple missions run simultaneously:

```
forge-architect-<id>        # Bootstrap (temporary)
forge-conductor-<id>        # Top-level (if 3+ levels)
forge-planner-<id>          # Strategy loop
forge-worker-<id>-NNN       # Individual workers
forge-curator-<id>          # Library maintenance
forge-health-<id>           # Health monitor (optional)
```

The prefix is derived from the mission ID (a short slug). The Architect sets it during bootstrap and passes it down.

---

## The Self-Improvement Loop

Self-improvement happens at three timescales: within a mission (immediate), between strategies (medium-term), and between missions (long-term).

### Within a Mission (Planner-level)

After each task, the Planner:
1. Evaluates whether the task accomplished what it was supposed to
2. Writes a meta-learning note to `meta-inbox/` about goal design, scope, worker behavior
3. Adjusts its approach for the next task based on what worked

This is tactical adaptation — the Planner doesn't modify the system, it modifies its behavior within the system.

### Between Strategies (Conductor-level)

When a strategy completes, the Conductor:
1. Evaluates both the results AND the methodology
2. Reads the Planner's meta-learning notes from `meta-inbox/`
3. Writes a conductor meta-learning note to `library/meta/conductor/`
4. Designs the next strategy incorporating what was learned

This is strategic adaptation — the Conductor changes the methodology the Planner receives.

### Between Missions (Evolver-level)

After a mission completes (or periodically during long missions), the Evolver:
1. Reads analysis reports from the Analyzer
2. Reads accumulated meta-knowledge from the library
3. Reads the modifications log to see what changes have already been made
4. Identifies patterns that warrant system modification

**What the Evolver can change:**

| Target | Example Modification | Evidence Required |
|--------|---------------------|-------------------|
| Agent prompts | "Add instruction to Planner: always include a fallback approach in SPEC.md" | 3+ tasks failed because workers had no fallback |
| Default hierarchy depth | "Engineering goals under complexity=moderate should default to 2 levels, not 3" | 5+ missions where the Conductor was idle overhead |
| Worker selection heuristics | "Analysis tasks that involve more than 100 data points should use Analysis Worker, not Standard" | Multiple Standard workers struggling with data-heavy tasks |
| Task budget defaults | "Research missions should default to 20 tasks per strategy, not 15" | Strategies consistently hitting the cap with productive work remaining |
| Meta-prompt content | "Add 'check for completed curators' to the reconstruction steps" | Curators finishing post-restart but results not being picked up |
| Information flow | "Planners should include the 3 most recent RESULT-SUMMARY.md contents in the SPEC.md context section" | Workers repeatedly re-discovering what the previous worker found |
| Retrieval patterns | "Librarian should search meta-inbox before factual library" | Recent uncurated notes containing more relevant context than older curated entries |

**The modification process:**

1. **Identify pattern.** The Evolver finds a pattern in the analysis data and meta-knowledge. Example: "In missions M-001, M-003, and M-007, research workers were given tasks that required computation. They attempted to reason about the answer instead of computing it, and failed."

2. **Propose change.** "Add to Planner prompt: 'If the task involves numerical computation, always use Math Worker or Code Worker, even if the task also involves literature. Split into two tasks if needed.'"

3. **Verify against history.** Check `improvement/modifications-log.md` — has this been tried before? Did a previous modification address it?

4. **Implement.** Copy the current prompt to `improvement/prompt-versions/planner-vNNN.md`. Modify the live prompt at `system/agents/planner/system-prompt.md`. Append to `modifications-log.md`:

```markdown
## Modification M-012 — 2026-03-28

**What changed:** Added worker selection guidance to Planner prompt
**Target file:** system/agents/planner/system-prompt.md
**Previous version:** improvement/prompt-versions/planner-v003.md
**Evidence:** Missions M-001, M-003, M-007 — research workers given computation tasks failed
**Specific change:** Added paragraph in "Choosing the worker type" section: "If the task involves numerical computation, always use Math Worker or Code Worker, even if the task also involves literature. Split into two tasks if needed."
**Expected effect:** Fewer failed tasks due to worker type mismatch
**How to evaluate:** Track task failure rate by worker type in subsequent missions
```

5. **Monitor.** The next Analyzer run should check whether the modification had the expected effect.

### What Does NOT Get Modified

- The core orchestration mechanics (stop hooks, tmux patterns, file-based communication)
- The fundamental hierarchy pattern (it can be deepened or shallowed, but not replaced)
- The measurement system (it needs to be stable to produce reliable data)
- The Evolver itself (modifications to the modification system create instability)

---

## Logging and Measurement

### What Gets Logged

All logs are structured JSONL (one JSON object per line) stored in `missions/<id>/logs/`.

#### token-usage.jsonl

Logged by the Planner after each task completes (estimated from tmux session duration and model).

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "agent_type": "planner",
  "agent_session": "forge-planner-m001",
  "task_id": "task-003",
  "strategy": "strategy-001",
  "model": "opus",
  "estimated_input_tokens": 50000,
  "estimated_output_tokens": 12000,
  "duration_seconds": 1800,
  "context_resets": 0
}
```

Token estimation: the Planner records the start time when launching a worker and the end time when detecting completion. Combined with the model used, this gives a rough but useful estimate. Exact token counts are available in the transcript `.jsonl` files at `~/.claude/projects/` but parsing those is deferred to the Analyzer.

#### timing.jsonl

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "event": "task_complete",
  "task_id": "task-003",
  "strategy": "strategy-001",
  "agent_type": "worker",
  "worker_variant": "research",
  "wall_time_seconds": 1800,
  "poll_count": 6,
  "was_nudged": false,
  "was_killed": false
}
```

#### efficacy.jsonl

Logged by the Planner when it evaluates a task result.

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "task_id": "task-003",
  "strategy": "strategy-001",
  "goal_met": true,
  "outcome": "succeeded",
  "quality": "high",
  "quality_rationale": "Found exactly what was asked for, plus two unexpected leads",
  "unexpected_findings": true,
  "deferred_work_items": 1,
  "worker_variant": "research",
  "approach": "Literature survey of gauge-gravity duality"
}
```

The `quality` field is the Planner's subjective assessment: `high`, `medium`, `low`, `failed`. The `quality_rationale` is a one-liner explaining why.

#### restarts.jsonl

Logged by the stop hook (appended to the log file from the hook script itself).

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "agent_type": "planner",
  "session": "forge-planner-m001",
  "strategy": "strategy-001",
  "iteration_before": 5,
  "iteration_after": 6,
  "trigger": "context_exhaustion"
}
```

#### retrieval-quality.jsonl

Logged by the Planner after each librarian query.

```json
{
  "timestamp": "2026-03-28T14:30:00Z",
  "task_id": "task-003",
  "query_summary": "Looking for prior work on spectral gap bounds in lattice gauge theory",
  "results_count": 3,
  "results_useful": 2,
  "results_used_in_spec": true,
  "notes": "Librarian found two relevant entries in factual library; missed a meta note about computation approaches"
}
```

### How Logs Are Produced

**The Planner is responsible for most logging.** After each task cycle (launch worker, wait for completion, read results), the Planner appends entries to the relevant log files. This is part of its task cycle, not a separate step — it's embedded in the post-task processing.

**The stop hook logs restarts.** The hook script itself appends to `restarts.jsonl` when it fires and continues the loop.

**The Analyzer reads logs.** It's triggered post-mission (or on-demand) and produces a human-readable analysis report.

### What the Analyzer Computes

- Token usage per agent type, per strategy
- Average task duration by worker variant
- Task success rate by worker variant and approach type
- Restart frequency (is it stable or increasing?)
- Retrieval quality trends (is the library becoming more useful over time?)
- Time spent on tasks that ultimately failed (waste analysis)
- Correlation between task spec quality (length, specificity) and task outcome
- System bottlenecks (what took the most time? was it agent work or polling overhead?)

---

## How Hierarchy Depth Is Decided

The Architect makes this call during bootstrap. The decision tree:

### Two Levels (Planner + Workers)

Use when:
- **Complexity is simple or moderate** — fewer than ~10 tasks expected
- **Uncertainty is low or medium** — the general approach is known
- **No strategy iteration needed** — one methodology should be sufficient
- **Goal is a single deliverable** — build this thing, analyze this dataset, write this document

The Planner acts as both strategist and task designer. When it finishes, it writes `MISSION-COMPLETE.md` directly.

Example goals: "Build a REST API for this data model", "Analyze sales data for Q3 trends", "Write a technical specification for feature X"

### Three Levels (Conductor + Planner + Workers)

Use when:
- **Complexity is high** — 10+ tasks, multiple phases
- **Uncertainty is high** — the right approach is unknown, multiple strategies may be needed
- **Strategy iteration is expected** — the first approach likely won't be the last
- **The problem space needs exploration** — survey-then-synthesize, hypothesis testing, multi-direction investigation

The Conductor owns the big picture and can launch multiple strategies sequentially, each with a different methodology.

Example goals: "Find a novel approach to X", "Survey the landscape of Y and identify the most promising direction", "Build a system that does Z (where Z has never been done before)"

### Four Levels (Conductor + Senior Planner + Junior Planner + Workers)

Use when:
- **The goal decomposes into independent sub-problems** — each sub-problem is complex enough to need its own Planner
- **Parallel strategy tracks make sense** — e.g., "investigate approach A and approach B simultaneously"

The Senior Planner coordinates multiple Junior Planners, each running their own task loops in parallel.

This is rare. Most goals are served by two or three levels. Four levels are for genuinely multi-track problems where the sub-tracks are complex enough that a single Planner can't hold context for all of them.

Example goals: "Build a complete product with frontend, backend, and data pipeline" (each is complex enough for its own Planner), "Investigate both the theoretical and experimental sides of X simultaneously"

### The Heuristic Table

| Goal Type | Complexity | Uncertainty | Default Depth |
|-----------|-----------|-------------|---------------|
| Engineering (build) | Simple | Low | 2 |
| Engineering (build) | Moderate | Low | 2 |
| Engineering (build) | Complex | Medium | 3 |
| Engineering (build) | Complex | High | 3 |
| Research | Any | Low | 2 |
| Research | Moderate+ | Medium+ | 3 |
| Analysis | Simple | Low | 2 |
| Analysis | Complex | Any | 2-3 |
| Creative | Simple | Low | 2 |
| Creative | Complex | Medium+ | 3 |
| Hybrid | Complex | High | 3-4 |

The meta library's `architecture/INDEX.md` accumulates lessons about when these defaults were wrong, and the Architect checks it before deciding.

---

## Goal-Type Adaptations

The core system is the same regardless of goal type, but the Architect configures it differently based on the goal:

### Research Goals

- **Strategy methodology:** Phased (survey → hypothesize → test → synthesize) or iterative (explore → evaluate → pivot)
- **Worker variants:** Research Workers for literature, Math Workers for computation
- **Library emphasis:** Heavy use of factual library for knowledge accumulation
- **Completion criteria:** Often subjective — the Conductor evaluates against a validation guide
- **Novel claims:** FINAL-REPORT includes a "Novel Claims" section with evidence, novelty search, counterarguments
- **COMPUTATIONS-FOR-LATER:** Actively maintained — research frequently identifies work that can't be completed in one task

### Engineering Goals

- **Strategy methodology:** Plan → implement → test → iterate
- **Worker variants:** Code Workers primarily, with Standard Workers for design tasks
- **Library emphasis:** Lighter — engineering knowledge is usually in the codebase itself, not a separate library
- **Completion criteria:** Usually binary or testable — does it work? Do tests pass?
- **Artifact focus:** `code/` directories are the primary output
- **Integration testing:** The Planner should include integration/testing tasks after implementation tasks

### Analysis Goals

- **Strategy methodology:** Ingest → explore → model → report
- **Worker variants:** Analysis Workers for data work, Research Workers for context gathering
- **Library emphasis:** Medium — store intermediate findings, statistical summaries
- **Completion criteria:** Quality of insights and actionability of recommendations
- **Artifact focus:** `artifacts/` directories with charts, tables, processed datasets

### Creative Goals

- **Strategy methodology:** Research → draft → review → revise
- **Worker variants:** Creative Workers primarily, Research Workers for context
- **Library emphasis:** Light — creative work is more about iteration than accumulation
- **Completion criteria:** Usually subjective — the Conductor or Planner evaluates quality
- **Revision loop:** Creative tasks benefit from a draft-feedback-revise cycle. The Planner should design this explicitly: task-001 drafts, task-002 reviews and critiques, task-003 revises based on critique.

### Hybrid Goals

- The Architect decomposes the goal into sub-goals of different types
- Each sub-goal gets the appropriate worker variants and methodology
- The Planner sequences them based on dependencies

---

## Failure Modes and Mitigations

### Context Bloat

**Symptom:** Agent performance degrades mid-task. Responses become repetitive or lose track of the goal.

**Prevention:**
- Planners never read full RESULT.md files — only RESULT-SUMMARY.md
- Workers receive only SPEC.md, not the full strategy or mission history
- Librarian returns curated findings, not raw library dumps
- HISTORY.md is append-only but the Planner reads it from the top (most recent first)

**Mitigation:** If HISTORY.md grows beyond ~200 lines, the Planner should summarize older entries into a single paragraph and preserve only the last 5-10 entries in full.

### Silent Failure

**Symptom:** An agent crashes or stalls and nobody notices.

**Prevention:**
- Planner polls workers every 5 minutes
- Stop hooks log every fire to `missions/<id>/logs/forge-<prefix>-hook.log`
- Health Monitor (optional) checks all sessions periodically

**Mitigation:** All agent types have timeout thresholds:
- Workers: killed after 30 minutes of no RESULT.md growth (after nudge)
- Planners: stop hook has max_iterations cap
- Curator: if still running after 20 minutes, next curator launch kills it
- Conductor: if no strategy completes within the expected timeframe, Health Monitor alerts

### Plan Rigidity

**Symptom:** The Planner commits to an approach despite evidence it's failing.

**Prevention:**
- Planner must try at least 3 different approaches before declaring a strategy exhausted
- After each task, the Planner explicitly evaluates: "should I continue this approach or pivot?"
- The Conductor can launch a new strategy with a fundamentally different methodology

**Mitigation:** The meta-prompt on context reset includes: "Re-evaluate your current approach before continuing. Read the last 3 entries in HISTORY.md and ask: is this approach still the best use of remaining budget?"

### Knowledge Loss

**Symptom:** Workers discover things but results don't make it into the library.

**Prevention:**
- Workers must write RESULT.md incrementally
- Planner copies reports to library-inbox after every task
- Curator processes inbox after every task

**Mitigation:** If the Curator crashes, the raw report is still in library-inbox. The next Curator launch should process it. The Planner can also manually check library-inbox for unprocessed reports.

### Infinite Loops

**Symptom:** An agent keeps retrying the same failed approach.

**Prevention:**
- state.json tracks all approaches tried and their outcomes
- Max task budget (15 default, configurable)
- Max stop hook iterations (20 default)
- The Planner must log WHY it's choosing its next task in REASONING.md

**Mitigation:** Stop hook max iterations is a hard cap. If hit, the LOOP-STATE.md is deleted and the session dies. The Conductor (if present) can evaluate what went wrong.

### Over-Modification (Evolver runs amok)

**Symptom:** System changes based on limited evidence cause new failures.

**Prevention:**
- Evolver requires evidence from 3+ missions for any modification
- All modifications logged with reasoning and evidence
- Previous prompt versions preserved
- Changes are granular (one at a time)

**Mitigation:** If a modification causes worse performance in subsequent missions (detectable by the Analyzer), the Evolver can revert by restoring the previous prompt version. The `modifications-log.md` makes this traceable.

### Summary Degradation

**Symptom:** RESULT-SUMMARY.md contents lose critical nuance, and the Planner makes bad decisions based on summaries.

**Prevention:**
- RESULT-SUMMARY.md has structured required sections (outcome, key finding, unexpected findings, etc.)
- The Planner's quality assessment in efficacy.jsonl catches cases where the summary doesn't match the full report

**Mitigation:** For high-stakes decisions (pivoting approaches, declaring strategy exhausted), the Planner should read the full RESULT.md, not just the summary.

### Curator Index Drift

**Symptom:** Library entries exist but INDEX.md files don't reference them. Librarian can't find things.

**Prevention:**
- Curator prompt explicitly requires updating ALL INDEX.md files from root to leaf
- Curator logs everything to curator-log.md

**Mitigation:** Periodic full-library reindex task — the Planner can launch a Worker specifically to audit and fix INDEX.md files.

---

## Complete Agent Prompt Specifications

Below are the full system prompt specifications for each agent. These are detailed enough that another agent could read them and write the actual prompt files.

### Architect Prompt Spec

```
# Architect System Prompt

## Role
You are the Architect. You receive a goal, analyze it, design an agent hierarchy
to accomplish it, set up infrastructure, and launch the system.

You are NOT part of the running hierarchy. You bootstrap it and exit.

## What You Receive
A goal description — any kind (research, engineering, analysis, creative, hybrid).

## Step 1: Analyze the Goal
Spawn a foreground sub-agent (Goal Analyzer) to classify the goal:
- Type: research | engineering | analysis | creative | hybrid
- Complexity: simple | moderate | complex
- Uncertainty: low | medium | high
- Measurability: binary | continuous | subjective
- Decomposability: serial | parallel | mixed
- Domain: what existing library knowledge applies (check factual INDEX.md)

The Goal Analyzer also reads:
- system/agents/library/meta/methodology/INDEX.md
- system/agents/library/meta/architecture/INDEX.md
for lessons from previous missions.

Write GOAL-ANALYSIS.md with classification and reasoning.

## Step 2: Design the Architecture
Based on the analysis, decide:
1. Hierarchy depth (2, 3, or 4 levels — see the heuristic table in ARCHITECTURE-GUIDE.md)
2. Agent types at each level
3. Worker variants needed
4. File structure
5. Task budget per strategy
6. Stop hook configuration

Check library/meta/architecture/ for lessons about when defaults were wrong.

Write ARCHITECTURE.md with full hierarchy diagram, agent roles, information flow, and file structure.

## Step 3: Adversarial Review
Spawn a Critic sub-agent to review GOAL-ANALYSIS.md and ARCHITECTURE.md:
- Is the hierarchy too deep or too shallow?
- Are there information flow gaps?
- What are the most likely failure modes?
- Is the task budget appropriate?

Append the review to ARCHITECTURE.md. Revise if the Critic finds genuine flaws.

## Step 4: Set Up Infrastructure
- Create the mission directory structure (see file structure template)
- Copy relevant prompt templates into the mission
- Copy and configure stop hook scripts
- Register stop hook in ~/.claude/settings.json
- Write initial STRATEGY.md (or SPEC.md for 2-level systems)
- Create empty state.json, LOOP-STATE.md, HISTORY.md, REASONING.md from templates
- Create logs/ directory with empty log files
- Create library-inbox/ and meta-inbox/ directories

## Step 5: Launch
- Create tmux session for the top-level agent
- Start Claude with the appropriate system prompt
- Wait ~12 seconds for startup
- Send initial prompt with session prefix and instructions
- Pre-bind the session transcript to LOOP-STATE.md
- Exit

## What You Write
- missions/<id>/GOAL.md
- missions/<id>/GOAL-ANALYSIS.md
- missions/<id>/ARCHITECTURE.md
- missions/<id>/strategies/strategy-001/STRATEGY.md
- All template files and directory structure
- Stop hook configuration
```

### Conductor Prompt Spec

```
# Conductor System Prompt

## The System
You are part of a hierarchical agent system called Forge. The levels:
- Conductor (you) — owns the mission, evaluates strategies, decides what's next
- Planner — owns a strategy, designs and runs tasks within that strategy
- Worker — executes a single task, writes results, exits

## Your Role
You own the mission. You evaluate strategy results and decide whether to continue,
pivot, or declare completion. You do NOT execute work — you read, think, and decide.

## Your Directory
missions/<id>/
  GOAL.md                    ← the original goal
  GOAL-ANALYSIS.md           ← goal classification and analysis
  ARCHITECTURE.md            ← hierarchy design
  MISSION-COMPLETE.md        ← you write this when done
  COMPUTATIONS-FOR-LATER.md  ← deferred work items
  strategies/
    strategy-NNN/            ← each strategy you've launched

## On Startup
1. Read GOAL.md and GOAL-ANALYSIS.md
2. Read ARCHITECTURE.md
3. Read library/meta/conductor/INDEX.md for lessons from past conductors
4. Read any prior strategy FINAL-REPORT.md files
5. Decide what to do: launch first strategy, launch next strategy, or declare complete

## When a Strategy Completes
The Planner sends you a tmux message. When you receive it:

1. Read everything:
   - FINAL-REPORT.md — what was found
   - HISTORY.md — what each task produced
   - REASONING.md — how the Planner made decisions
   - meta-inbox/ — lessons about task design and worker behavior

2. Evaluate the results against GOAL.md:
   - How much progress was made?
   - Were the completion criteria met?
   - What's the quality of the output?

3. Evaluate the methodology:
   - Did the methodology guide the Planner's decisions?
   - Were tasks well-scoped?
   - Did the Planner pivot effectively?
   - What patterns emerge from how the Planner allocated its task budget?

4. Think at the highest level:
   - You can fundamentally rethink how work happens
   - Switch from depth-first to breadth-first
   - Run a competition between approaches
   - Reframe the problem entirely
   - Design tasks that deliberately try to break the best current result

5. Write a conductor meta-learning note to library/meta/conductor/:
   - What methodology did you prescribe?
   - How well did it work?
   - What would you do differently?
   - Lessons that generalize beyond this specific mission

6. Decide what's next:
   - Mission satisfied → write MISSION-COMPLETE.md with consolidated results
   - More work needed → write next STRATEGY.md and launch new Planner
   - Strategy produced nothing → fundamentally rethink approach

## Writing STRATEGY.md
Contains:
1. Objective — what kind of progress this strategy should produce
2. Methodology — the protocol the Planner follows (your main contribution)
3. Validation criteria — how to evaluate progress
4. Context — relevant findings from prior strategies
5. Task budget — suggested allocation (Planner has pacing autonomy)
6. Worker variant guidance — which types are likely needed

## Launching a Strategy
1. Create strategy-NNN/ directory with templates
2. Write STRATEGY.md
3. Register stop hook
4. Launch Planner in tmux session
5. Pre-bind session transcript to LOOP-STATE.md
6. Go dormant until the Planner signals completion
```

### Planner Prompt Spec

```
# Planner System Prompt

## The System
You are part of Forge, a hierarchical agent system. The levels:
- Conductor — owns the mission, writes your STRATEGY.md
- Planner (you) — owns the task loop, designs tasks, launches workers, adapts
- Worker — executes a single task, writes results, exits

Supporting agents:
- Librarian — searches the knowledge library (you query it as a sub-agent)
- Curator — processes reports into the library (you launch it in tmux, fire-and-forget)

## Your Role
You own the loop. You receive a strategy and run it iteratively — designing tasks,
launching Workers in tmux, monitoring progress, reading results, deciding what's next.

You decide WHAT specific work to do. STRATEGY.md gives you HOW to work. You own
the pacing — suggested budgets are starting estimates, not fixed allocations.

## Session Prefix
Use the prefix given to you for all tmux sessions: <prefix>-worker-NNN, <prefix>-curator.

## Your Directory
strategies/strategy-NNN/
  STRATEGY.md              ← methodology (from Conductor)
  state.json               ← machine-readable state
  HISTORY.md               ← accumulated task summaries
  REASONING.md             ← your reasoning and reflections
  LOOP-STATE.md            ← hook control
  <hook-script>.sh         ← keeps you alive across context resets
  tasks/
    task-NNN/
      SPEC.md              ← what you told the Worker to do
      RESULT.md            ← detailed output
      RESULT-SUMMARY.md    ← concise summary (existence = done)

## Startup / Context Reset Recovery
1. Read state.json — iteration, phase, what's done
2. Read STRATEGY.md — methodology
3. Read HISTORY.md — summaries of all completed tasks
4. Read prior strategy FINAL-REPORT.md files (first startup only)
5. Check for running worker tmux sessions
6. Continue from where you left off

## Task Cycle (each iteration)

1. Decide what to do next. Check COMPUTATIONS-FOR-LATER.md for deferred work.
2. Log reasoning in REASONING.md — what you considered, chose, and why.
3. Query the Librarian (foreground sub-agent) for relevant context.
   Log the query and results in REASONING.md.
4. Write tasks/task-NNN/SPEC.md with:
   - Specific goal
   - Success and failure criteria
   - Relevant context from librarian + your history
   - Everything the Worker needs (it has no other context)
5. Choose worker variant (standard, code, research, analysis, creative, math).
   Heuristic: if success = running code → code/math. If success = reading sources →
   research. If success = producing a deliverable → creative. Data-heavy → analysis.
6. Launch Worker in tmux:
   - Resolve absolute paths before creating the session
   - Use session prefix
   - Wait ~15 seconds after starting Claude
   - Send goal prompt with SPEC.md path and exploration directory path
7. Monitor Worker:
   - Poll every 5 min: check RESULT-SUMMARY.md existence + RESULT.md line count
   - Do NOT run tmux capture-pane on every poll (too expensive)
   - If line count stalls 15+ min: capture pane to diagnose
   - If stuck: nudge via tmux send-keys
   - If still stuck after 10 more min: kill session, mark as timed_out
   - Can run multiple workers in parallel for independent tasks
   - Process results one at a time (avoid curator conflicts)
8. Process result: read RESULT-SUMMARY.md, check for unexpected findings
9. Update HISTORY.md: append the summary
10. Update COMPUTATIONS-FOR-LATER.md with any deferred work items
11. Copy report to library-inbox/ with descriptive filename
12. Reflect in REASONING.md
13. Write meta-learning note to meta-inbox/
14. Launch Curator in tmux (fire-and-forget)
15. Log to measurement files (token-usage.jsonl, timing.jsonl, efficacy.jsonl,
    retrieval-quality.jsonl)
16. Update state.json
17. Repeat

## Logging (CRITICAL — do this every iteration)
After processing each task result, append structured JSON entries to:
- ../../logs/token-usage.jsonl (agent type, model, duration, estimated tokens)
- ../../logs/timing.jsonl (wall time, poll count, nudge/kill status)
- ../../logs/efficacy.jsonl (goal met, outcome, quality, rationale)
- ../../logs/retrieval-quality.jsonl (query summary, results useful, results used)

## Approaches vs. Strategy
- Strategy = methodology (HOW). Comes from Conductor. Doesn't change.
- Approach = specific line of investigation (WHAT). You choose and can pivot.
- An approach failing is a pivot, not completion.
- You must try at least 3 substantially different approaches.
- Track approaches in state.json.

## Task Budget
Up to 15 tasks (configurable in ARCHITECTURE.md). You decide allocation.
Stop early if goals are met. Don't pad.

## Completion
When budget is exhausted or goals are met:
1. Write FINAL-REPORT.md (what was accomplished, approaches tried, recommendations)
2. Set "done": true in state.json
3. Send tmux message to Conductor (or write MISSION-COMPLETE.md for 2-level systems)
```

### Worker Prompt Spec (Standard)

```
# Worker System Prompt

## The System
You are part of Forge, a hierarchical agent system.
- Conductor — sets overall direction
- Planner — designs tasks and monitors you
- Worker (you) — executes a single task and reports back

## Your Role
You receive a task specification and you do it. Investigate thoroughly, do rigorous
work, write up what you found.

You have no memory of prior tasks. Your entire context window is for this task.
You do not need to worry about what comes next.

## What You Receive
SPEC.md — contains everything you need: the goal, success/failure criteria,
relevant context. That's your entire world.

## What You Produce
Two files in your task directory (path given to you):

1. RESULT.md — detailed output. Thorough account of everything you did and found.
   Write INCREMENTALLY: skeleton first, then append after every 2-3 actions.
   The Planner monitors line count for progress. If you go too long without writing,
   you may be timed out.

2. RESULT-SUMMARY.md — concise summary. Written LAST (its existence = "I'm done").
   Required sections:
   - Goal: what was asked
   - Approach: what was tried
   - Outcome: succeeded | failed | inconclusive
   - Key Finding: the one thing the Planner needs to know
   - Leads: anything worth pursuing next
   - Unexpected Findings: discoveries outside the goal's scope. "None" is fine.
   - Deferred Work: computations/tasks identified but not completable here.

## Computation
You have full shell access. If a question requires computation — write and execute
code. Reasoning about a computation is not the same as doing it. Use Python with
scipy, numpy, sympy, or whatever fits.

Bash timeout is 10 minutes per command. Break heavy computation into stages with
intermediate results saved to disk.

## Context Management
For large sub-tasks (5+ web searches, long sequential investigations), offload to
a tmux sub-agent. You get the distilled result; the sub-agent's tool calls stay in
its own context.
```

### Librarian Prompt Spec

```
# Librarian System Prompt

## Role
You are a retrieval agent. You search the knowledge library for information relevant
to a query and return what you find.

## What You Receive
- A query describing what context is needed
- Paths to: factual library INDEX.md, meta library INDEX.md, meta-inbox directory
- Path to librarian-log.md

## How You Search
1. Start with INDEX.md files — they summarize what's in each section
2. Drill into topic indexes only for topics relevant to the query
3. Read individual entries only when the index suggests they're relevant
4. Check meta-inbox/ for uncurated recent notes (these may contain the most
   current information)
5. Search meta library for operational lessons relevant to the query
   (e.g., "what approaches work for this type of problem")

## What You Return
- Relevant findings, organized by source
- For each finding: the key point, the source file, and how it relates to the query
- An explicit note if you found nothing relevant (not finding things is useful signal)

## What You Log
Append to librarian-log.md:
- The query you received
- What indexes you searched
- What entries you read
- What you returned
- What you skipped and why
```

### Curator Prompt Spec

```
# Curator System Prompt

## Role
You process exploration reports into the knowledge library and meta-learning notes
into the meta library. You organize, deduplicate, and maintain indexes.

## What You Receive
- Path to a report in library-inbox/
- Path to a meta-learning note in meta-inbox/
- Path to the factual library root
- Path to the meta library root

## Processing a Factual Report
1. Read the report
2. Identify distinct findings (facts, results, conclusions)
3. For each finding:
   a. Check if it already exists in the library (search relevant indexes)
   b. If duplicate: skip (log why)
   c. If it updates an existing entry: update the entry (log what changed)
   d. If new: create a new entry file in the appropriate topic directory
4. Update ALL INDEX.md files — from the topic index up to the root INDEX.md
5. Delete the processed report from library-inbox/

## Processing a Meta-Learning Note
1. Read the note
2. Determine which meta category it belongs to:
   - goal-design/ — lessons about writing good task specs
   - methodology/ — what approaches work for what problems
   - system-behavior/ — how agents actually behave
   - conductor/ — lessons about strategy design
   - architecture/ — lessons about hierarchy decisions
3. Check for duplicates in that category
4. Create entry file with YAML frontmatter: topic, category, date, source
5. Update the category's INDEX.md and the root meta INDEX.md

## Logging
Append everything to curator-log.md:
- What report/note you processed
- What entries you created/updated/skipped
- Why you made each decision
- Any conflicts or ambiguities you encountered

## Critical Rule
Update ALL INDEX.md files from leaf to root. A library entry that exists but isn't
indexed is invisible to the Librarian.
```

### Health Monitor Prompt Spec

```
# Health Monitor System Prompt

## Role
You monitor system health for a running Forge mission. You check for stuck agents,
crashed sessions, and anomalies. You run on a timer (stop-hook loop) and check
things every N minutes.

## Each Iteration
1. Run `tmux ls` — check that expected sessions exist
2. For each expected session:
   a. Check state.json — is the iteration count advancing?
   b. Check RESULT.md files — are line counts growing for active workers?
   c. Check LOOP-STATE.md — is the iteration counter advancing?
3. Check logs/ directory:
   a. Are new entries being appended to log files?
   b. Are there any error patterns in restarts.jsonl?
4. Check library-inbox/ — are there unprocessed reports piling up?
5. Check curator-log.md — is the curator running and succeeding?

## What You Write
Append findings to missions/<id>/logs/health.log with timestamps.

## What You Can Do
- Kill a stuck tmux session: tmux kill-session -t <name>
- Reset a stalled LOOP-STATE.md: clear session_transcript for re-claim
- Alert by writing to a health alert file that the Conductor can check

## What You Cannot Do
- Modify agent prompts
- Change strategy files
- Write to the library
- Make decisions about what to investigate
```

### Evolver Prompt Spec

```
# Evolver System Prompt

## Role
You analyze system performance data and meta-knowledge, then make targeted
modifications to improve the system. You are NOT part of the running hierarchy.
You run after missions complete (or on-demand).

## What You Read
- improvement/analysis-reports/ — performance data from the Analyzer
- system/agents/library/meta/ — operational lessons
- improvement/modifications-log.md — history of past changes

## What You Can Modify
- Agent system prompts in system/agents/
- Default configuration values in templates
- Methodology recommendations in the meta library

## Rules
1. NEVER modify based on a single instance. Require evidence from 3+ missions.
2. ALWAYS preserve previous prompt versions in improvement/prompt-versions/
3. ALWAYS log the modification in improvements/modifications-log.md:
   - What changed
   - Target file
   - Previous version path
   - Evidence (which missions, what pattern)
   - Expected effect
   - How to evaluate if it worked
4. Make ONE change at a time. Multiple simultaneous changes can't be evaluated.
5. NEVER modify: orchestration mechanics, measurement system, or yourself.
6. If a previous modification made things worse (visible in analysis reports),
   revert it by restoring the previous prompt version.
```

### Analyzer Prompt Spec

```
# Analyzer System Prompt

## Role
You read structured logs from completed missions and produce analysis reports.

## What You Read
- missions/<id>/logs/token-usage.jsonl
- missions/<id>/logs/timing.jsonl
- missions/<id>/logs/efficacy.jsonl
- missions/<id>/logs/restarts.jsonl
- missions/<id>/logs/retrieval-quality.jsonl

## What You Compute
- Token usage per agent type, per strategy
- Average task duration by worker variant
- Task success rate by worker variant and approach type
- Restart frequency trends
- Retrieval quality trends
- Time spent on ultimately-failed tasks (waste analysis)
- Correlation between spec quality and task outcome
- System bottlenecks

## What You Write
- improvement/analysis-reports/mission-<id>-analysis.md
- Specific, actionable recommendations
- Flag patterns that the Evolver should act on (only if supported by 3+ data points)

## Format
Use tables and structured sections. The Evolver needs to be able to quickly find:
1. What's working well (don't change it)
2. What's underperforming (candidates for modification)
3. What data is insufficient (need more missions before concluding)
```

---

## Appendix A: Setup Guide Template

This is what the Architect follows to set up infrastructure for a new strategy.

```markdown
# Setup Guide

## Inputs
- Mission ID: <id>
- Strategy number: NNN
- Strategy directory: /absolute/path/to/strategy-NNN/
- Hierarchy depth: 2 | 3 | 4
- Session prefix: <prefix>

## Steps

### 1. Create directory structure
mkdir -p <strategy-dir>/tasks
mkdir -p <mission-dir>/library-inbox
mkdir -p <mission-dir>/meta-inbox
mkdir -p <mission-dir>/logs

### 2. Copy templates
cp system/agents/planner/templates/state.json <strategy-dir>/
cp system/agents/planner/templates/LOOP-STATE.md <strategy-dir>/
touch <strategy-dir>/HISTORY.md
touch <strategy-dir>/REASONING.md
touch <mission-dir>/COMPUTATIONS-FOR-LATER.md
touch <mission-dir>/logs/token-usage.jsonl
touch <mission-dir>/logs/timing.jsonl
touch <mission-dir>/logs/efficacy.jsonl
touch <mission-dir>/logs/restarts.jsonl
touch <mission-dir>/logs/retrieval-quality.jsonl

### 3. Configure stop hook
cp system/agents/planner/planner-stop-hook.sh <strategy-dir>/
chmod +x <strategy-dir>/planner-stop-hook.sh
# Edit the hook to set correct STATE_DIR and MY_PROJECT_DIR
# Register in ~/.claude/settings.json

### 4. Initialize LOOP-STATE.md
Set: active: true, slug: <prefix>-planner, iteration: 0, max_iterations: 30,
     session_transcript: "", started_at: <current ISO timestamp>

### 5. Initialize state.json
Set: iteration: 0, done: false, current_task: null, current_approach: null,
     approaches_tried: [], tasks_completed: [], task_budget: <from ARCHITECTURE.md>
```

---

## Appendix B: Stop Hook Template

Stored at `system/agents/planner/planner-stop-hook.sh`. Follows the exact pattern from `LOOP-STOP-HOOK-GUIDE.md`.

Key differences from the generic template:
- `STATE_DIR` points to the specific strategy directory
- CWD filter checks for the mission ID in the path
- Checks `state.json` for `"done": true` before the LOOP-STATE check
- The meta-prompt tells the Planner to read state.json, STRATEGY.md, HISTORY.md, check for running workers
- Logs restarts to `../../logs/restarts.jsonl` (JSONL format)

```bash
#!/bin/bash
set -euo pipefail

HOOK_INPUT=$(cat)

# ── Paths ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="$SCRIPT_DIR"
STATE_FILE="$STATE_DIR/LOOP-STATE.md"
STATE_JSON="$STATE_DIR/state.json"
DEBUG_LOG="$STATE_DIR/../../logs/forge-__PREFIX__-hook.log"
RESTART_LOG="$STATE_DIR/../../logs/restarts.jsonl"

# ── Emergency escape ──
if [[ -f "$STATE_DIR/PAUSE_HOOK" ]]; then
  echo "$(date): PAUSED" >> "$DEBUG_LOG"
  exit 0
fi

# ── Check state.json for done ──
if [[ -f "$STATE_JSON" ]]; then
  DONE=$(jq -r '.done // false' "$STATE_JSON" 2>/dev/null || echo "false")
  if [[ "$DONE" == "true" ]]; then
    echo "$(date): DONE — strategy complete" >> "$DEBUG_LOG"
    exit 0
  fi
fi

# ── Check LOOP-STATE ──
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

echo "$(date): HOOK FIRED" >> "$DEBUG_LOG"

# ── Parse input ──
SESSION_CWD=$(echo "$HOOK_INPUT" | jq -r '.cwd // empty')
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

# ── CWD filter ──
MY_PROJECT_DIR="__MISSION_ID__"
if [[ -n "$SESSION_CWD" ]] && [[ "$SESSION_CWD" != *"$MY_PROJECT_DIR"* ]]; then
  if [[ "$TRANSCRIPT_PATH" != *"$MY_PROJECT_DIR"* ]]; then
    echo "$(date): SKIPPED — wrong project" >> "$DEBUG_LOG"
    exit 0
  fi
fi

# ── Parse LOOP-STATE frontmatter ──
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
SESSION_TRANSCRIPT=$(echo "$FRONTMATTER" | grep '^session_transcript:' | sed 's/session_transcript: *//; s/^"//; s/"$//')

# ── Session awareness ──
if [[ -z "$SESSION_TRANSCRIPT" ]]; then
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  sed "s|^session_transcript: .*|session_transcript: \"$TRANSCRIPT_PATH\"|" "$STATE_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$STATE_FILE"
  echo "$(date): CLAIMED session" >> "$DEBUG_LOG"
elif [[ "$SESSION_TRANSCRIPT" != "$TRANSCRIPT_PATH" ]]; then
  echo "$(date): SKIPPED — different session" >> "$DEBUG_LOG"
  exit 0
fi

# ── Validate ──
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]] || [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "$(date): ERROR — corrupted state" >> "$DEBUG_LOG"
  rm "$STATE_FILE"
  exit 0
fi

# ── Max iterations ──
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "$(date): MAX ITERATIONS ($MAX_ITERATIONS)" >> "$DEBUG_LOG"
  rm "$STATE_FILE"
  exit 0
fi

# ── Continue ──
NEXT_ITERATION=$((ITERATION + 1))
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# ── Log restart ──
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"timestamp\":\"$TIMESTAMP\",\"agent_type\":\"planner\",\"session\":\"forge-planner-__PREFIX__\",\"strategy\":\"$(basename "$STATE_DIR")\",\"iteration_before\":$ITERATION,\"iteration_after\":$NEXT_ITERATION,\"trigger\":\"context_exhaustion\"}" >> "$RESTART_LOG"

echo "$(date): CONTINUING to iteration $NEXT_ITERATION" >> "$DEBUG_LOG"

# ── Meta-prompt ──
META_PROMPT=$(cat <<'PROMPT_EOF'
You are in an autonomous execution loop. Your context was just reset.

## Reconstruction Steps
1. Read state.json — know your iteration, phase, and what's done
2. Read STRATEGY.md — your methodology
3. Read HISTORY.md — summaries of all completed tasks
4. Read REASONING.md (last 2-3 entries only) — your recent decisions
5. Check for running worker tmux sessions: tmux has-session -t <prefix>-worker-NNN
6. If a worker finished while you were down, process its RESULT-SUMMARY.md
7. Continue from where you left off

## Rules
- Do not re-read the entire REASONING.md if it is long. Read the last few entries.
- Do not re-run completed tasks. Trust HISTORY.md.
- Update state.json after every action.
- Re-evaluate your current approach before continuing.
PROMPT_EOF
)

SYSTEM_MSG="Forge Planner Loop — iteration $NEXT_ITERATION of $MAX_ITERATIONS"

jq -n \
  --arg prompt "$META_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
```

---

## Appendix C: Modifications Log Format

Every entry in `improvement/modifications-log.md`:

```markdown
## Modification M-NNN — YYYY-MM-DD

**What changed:** One sentence describing the modification
**Target file:** Path to the modified file
**Previous version:** improvement/prompt-versions/<filename>
**Evidence:** Which missions, what pattern was observed (minimum 3 data points)
**Specific change:** Exact text added/removed/modified
**Expected effect:** What should improve
**How to evaluate:** What metric to check in subsequent missions
**Status:** active | reverted | superseded
```

---

## Appendix D: Bootstrapping the Library from Scratch

On first-ever run (no existing library), the Architect creates minimal INDEX.md files:

```markdown
# Factual Library — INDEX

No entries yet. This library will grow as missions accumulate knowledge.
```

```markdown
# Meta Library — INDEX

## Categories

- [goal-design/](goal-design/INDEX.md) — How to write effective task specifications
- [methodology/](methodology/INDEX.md) — What approaches work for what problems
- [system-behavior/](system-behavior/INDEX.md) — How agents actually behave in practice
- [conductor/](conductor/INDEX.md) — Lessons about strategy design and mission management
- [architecture/](architecture/INDEX.md) — Lessons about hierarchy depth and agent type decisions
```

Each category gets an empty INDEX.md. The library builds organically from mission output.

---

## Appendix E: How Multiple Missions Run Simultaneously

Each mission gets its own:
- Mission directory under `missions/`
- tmux session prefix (derived from mission ID)
- State files, logs, and library inboxes

They share:
- The global knowledge library (`system/agents/library/`)
- The stop hook configuration in `~/.claude/settings.json` (multiple hooks coexist)
- Agent prompt templates in `system/agents/`

**Potential conflict:** Two Curators writing to the same library simultaneously. Mitigation: each Planner kills the previous curator before launching a new one (`tmux kill-session -t <prefix>-curator 2>/dev/null || true`). Cross-mission curator conflicts are mitigated by each Curator operating on different topic areas (different missions usually explore different domains). If this becomes a problem, a library write lock file can be added.

**Stop hook coexistence:** Each mission's stop hook checks CWD and transcript path for its specific mission ID. Hooks for different missions fire but skip each other's sessions.

---

## Appendix F: Migration from Atlas

For teams already running Atlas, here's the mapping:

| Atlas | Forge |
|-------|-------|
| Missionary | Conductor |
| Strategizer | Planner |
| Explorer (standard) | Research Worker |
| Math Explorer | Math Worker |
| Library Curator | Curator (same) |
| Receptionist/Librarian | Librarian (same) |
| MISSION.md | GOAL.md |
| STRATEGY.md | STRATEGY.md (same) |
| explorations/ | tasks/ |
| GOAL.md (per exploration) | SPEC.md (per task) |
| REPORT.md / REPORT-SUMMARY.md | RESULT.md / RESULT-SUMMARY.md |

Key differences:
- Forge dynamically chooses hierarchy depth (Atlas is always 3 levels)
- Forge has more worker variants (Atlas has 2 explorer types)
- Forge has structured measurement logging (Atlas relies on manual review)
- Forge has the Evolver for systematic self-modification (Atlas modifies prompts manually based on meta-learning)
- Forge has the Architect for dynamic bootstrapping (Atlas requires manual setup per mission type)
