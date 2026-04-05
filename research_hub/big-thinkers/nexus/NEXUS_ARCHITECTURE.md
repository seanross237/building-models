# ATLAS: Autonomous Tiered Learning Agent System

## Architecture Document v2.0

This document is the complete specification for building and operating ATLAS. An agent reading this document should be able to bootstrap the entire system from scratch.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Agent Hierarchy](#2-agent-hierarchy)
3. [File System Structure](#3-file-system-structure)
4. [Communication Protocol](#4-communication-protocol)
5. [Plan Lifecycle](#5-plan-lifecycle)
6. [Tmux Session Architecture](#6-tmux-session-architecture)
7. [Logging and Observability](#7-logging-and-observability)
8. [Self-Improvement Loop](#8-self-improvement-loop)
9. [Cross-Run Learning System](#9-cross-run-learning-system)
10. [Meta-Evaluator Layer](#10-meta-evaluator-layer)
11. [Recovery Mechanisms](#11-recovery-mechanisms)
12. [Goal Specification Format](#12-goal-specification-format)
13. [Termination Criteria](#13-termination-criteria)
14. [Bootstrap Procedure](#14-bootstrap-procedure)
15. [Operational Invariants and Edge Cases](#15-operational-invariants-and-edge-cases)

---

## 1. System Overview

ATLAS is a fully autonomous, self-improving multi-agent system that runs on Claude Code + tmux. Given a goal, it decomposes the goal into a plan, executes via a hierarchy of specialized agents, evaluates its own performance, and modifies its own structure to improve over time.

ATLAS operates at two timescales. **Within a run**, a tiered agent hierarchy (Sovereign through Workers) executes goals. **Between runs**, a Meta-Evaluator analyzes the system's performance history and rewrites any component of ATLAS itself — including prompts, hierarchy structure, cycle timings, and communication protocols — treating the entire system as optimizable code.

### Core Principles

- **Minimal context per agent**: Each agent is instantiated with exactly the information it needs. No agent receives the full system state. This prevents context window degradation.
- **Files as the source of truth**: All state, plans, logs, and knowledge live in the file system. Any agent can be killed and replaced; the files persist.
- **Adversarial review at every level**: Plans are reviewed before execution. Execution is reviewed during and after. The system reviews itself.
- **Graceful degradation**: If any agent stalls, crashes, or fills its context, the system detects this and recovers.
- **Quantitative self-knowledge**: The system tracks structured metrics across runs, measures the impact of its own modifications, and ranks its accumulated heuristics by evidence strength rather than recency.
- **Meta-optimization**: The system's structure is itself a target for optimization. A dedicated Meta-Evaluator layer exists above the execution hierarchy and rewrites any component that underperforms.

### Runtime Environment

- **Host**: macOS (Darwin)
- **Shell**: zsh
- **Agent runtime**: `claude` CLI (Claude Code)
- **Process orchestration**: tmux
- **Working directory**: `~/atlas/` (the system's home)

---

## 2. Agent Hierarchy

The system has four execution tiers plus one meta-layer that operates between runs. Higher tiers have broader context but less execution detail. Lower tiers have narrow context but deep execution capability. The Meta-Evaluator sits outside the execution hierarchy entirely and operates on the system itself.

```
          +---------------------+
          |   META-EVALUATOR    |  Layer -1 — runs BETWEEN runs
          | (System Optimizer)  |  Rewrites any component of ATLAS
          +----------+----------+
                     |
                     | (structural modifications, prompt rewrites,
                     |  config changes, protocol updates)
                     |
          +----------v----------+
          |     SOVEREIGN       |  Tier 0 — one instance per run
          |    (Goal Owner)     |
          +----------+----------+
                     |
          +----------+----------+
          |    STRATEGIST       |  Tier 1 — one instance
          |  (Plan + Review)    |
          +----------+----------+
                     |
          +----------+----------+----------+
          |          |          |          |
     +----+----+ +--+----+ +--+----+ +---+----+
     |CONDUCTOR| |CONDUCT.| |CONDUCT.| |CONDUCT.|  Tier 2 — 1 per workstream
     |(Oversee)| |(Overse)| |(Overse)| |(Overse)|
     +----+----+ +---+----+ +---+----+ +---+----+
          |           |           |           |
     +----+----+ +---+---+  +---+---+   +---+---+
     | WORKER  | |WORKER |  |WORKER |   |WORKER |  Tier 3 — N per conductor
     +----+----+ +---+---+  +---+---+   +---+---+
     | WORKER  |
     +---------+
```

### Layer -1: META-EVALUATOR

**Role**: Optimizes the system itself between runs. Treats every component of ATLAS — prompts, hierarchy, configuration, protocols, cycle timings — as mutable code to be improved based on evidence.

**When it runs**: After every run completes and before the next run begins. It does NOT run during execution. It is launched by the `start.sh` script during the inter-run phase, or manually by the operator.

**What it knows**:
- The full structured run history from `metrics/run_history.jsonl` (quantitative performance across all prior runs)
- All retrospectives from `knowledge/meta/`
- The modification changelog from `metrics/modification_log.jsonl` (every self-modification and its measured impact)
- The heuristic database from `metrics/heuristics.jsonl` (accumulated lessons ranked by evidence strength)
- The current state of ALL system files: prompts, config, monitor script, architecture doc
- The cross-run analysis reports from `metrics/cross_run_analysis/`

**What it does**:
- **Analyzes cross-run trends**: Reads structured metrics across all prior runs. Identifies performance trajectories: is token efficiency improving? Are plan revision counts decreasing? Are task completion times shrinking?
- **Evaluates past modifications**: For each self-modification that was made in or between prior runs, measures whether it actually improved performance. Updates the modification log with measured impact scores.
- **Prunes and ranks heuristics**: Reviews the heuristic database, promotes heuristics with strong multi-run evidence, demotes or removes those that have been contradicted.
- **Proposes structural changes**: Based on evidence, generates concrete proposals for modifying any system component. Each proposal includes: what to change, the evidence supporting the change, the expected impact, and rollback criteria.
- **Executes approved changes**: After generating proposals, evaluates them against its own criteria (see Section 10.3), applies changes that meet the threshold, and logs everything to the modification changelog.
- **Writes the cross-run analysis report**: Produces a structured analysis in `metrics/cross_run_analysis/analysis_{run_id}.md` that the Strategist reads at the start of the next run.

**What it does NOT do**:
- Never runs during active execution (it would interfere with the running system)
- Never modifies the goal (that is the user's domain)
- Never deletes historical data (metrics, logs, and retrospectives are append-only)

**Evaluation criteria for "system improvement"** (see Section 10.3 for full specification):
- Token efficiency: tokens spent per task-complexity-unit, trending down
- Plan stability: number of plan revisions per run, trending down
- Task completion rate: percentage of tasks completed without retry or escalation, trending up
- Time efficiency: wall-clock time per task-complexity-unit, trending down
- Heuristic accuracy: percentage of pre-run heuristic predictions that proved correct
- Recovery frequency: number of stall/crash recoveries per run, trending down

**Context budget**: This agent gets a full context window. It runs infrequently (once between runs) and its job is deep analysis, so it is allowed to consume substantial context.

### Tier 0: SOVEREIGN

**Role**: Owns the goal. Decides when the system is done. Has the most abstract view.

**What it knows**:
- The original goal specification
- The current high-level plan (title + status of each workstream, not details)
- Aggregated metrics: total time elapsed, total tokens spent, workstream completion percentages
- The termination criteria
- The Meta-Evaluator's latest cross-run analysis summary (a brief section appended to its context showing key recommendations from the between-run analysis)

**What it does**:
- Reads `goal.md` and `plan/status.md` on each cycle
- Decides if the goal has been met (writes to `system/termination.md`)
- Can override the Strategist if the system is stuck or going in the wrong direction
- Runs on a slow cycle (every 5-10 minutes, configurable)
- Writes high-level directives to `directives/sovereign.md` if course correction is needed

**What it does NOT do**:
- Never reads individual task files or worker logs
- Never executes work directly
- Never modifies the plan directly (it directs the Strategist to do so)
- Never modifies system structure (that is the Meta-Evaluator's domain between runs; the Sovereign only approves within-run prompt changes per Section 8.3)

**Context budget**: Kept extremely lean. Reads only summary files. Target: under 15% of context window used.

### Tier 1: STRATEGIST

**Role**: Creates, reviews, and revises the plan. Adversarial reviewer of its own plans and of execution progress.

**What it knows**:
- The goal specification
- The full plan tree (all workstreams, all tasks, dependencies)
- Conductor status reports (summaries, not raw logs)
- The system's knowledge base (`knowledge/`)
- The Meta-Evaluator's latest cross-run analysis report (structured recommendations, not just prose retrospectives)
- The ranked heuristic database (heuristics relevant to the current goal type, ranked by evidence strength)
- Self-improvement recommendations from prior runs

**What it does**:
- **Plan creation**: Decomposes the goal into workstreams, each with ordered tasks. Consults the heuristic database for relevant planning heuristics before creating the plan.
- **Adversarial self-review**: After creating a plan, immediately reviews it from the perspective of "what could go wrong" and "what assumptions am I making"
- **Progress evaluation**: Reads conductor reports, decides if workstreams are on track
- **Pivot detection**: If a workstream is stuck or findings invalidate the plan, revises the plan
- **Knowledge integration**: Before planning, reads relevant entries from `knowledge/` and the ranked heuristics from `metrics/heuristics.jsonl` to avoid repeating past mistakes
- **Modification tagging**: When making any self-modification (prompt change, config tweak, structural proposal), tags it with a unique modification ID so its impact can be tracked across runs (see Section 9.2)
- Runs on a medium cycle (every 2-3 minutes)

**What it does NOT do**:
- Never executes tasks
- Never reads raw worker output (only conductor summaries)

### Tier 2: CONDUCTOR

**Role**: Oversees one workstream. Translates plan tasks into concrete worker assignments. Monitors workers.

**What it knows**:
- Its workstream's portion of the plan
- All task files for its workstream
- Worker status and output summaries
- Relevant knowledge base entries for its domain

**What it does**:
- Reads its workstream plan from `plan/workstreams/{id}/`
- Creates worker task assignments in `tasks/{workstream_id}/`
- Monitors worker output files
- Writes status reports to `reports/{workstream_id}/`
- Detects worker stalls (file not updated in N minutes) and restarts them
- Escalates to Strategist when: task is blocked, findings contradict plan, workstream scope needs change

**What it does NOT do**:
- Never modifies the overall plan (escalates to Strategist)
- Never does the actual work (delegates to Workers)

### Tier 3: WORKER

**Role**: Executes a single task. Has the narrowest context and the deepest focus.

**What it knows**:
- Its specific task file (`tasks/{workstream_id}/{task_id}.md`)
- Any referenced input files or artifacts
- Relevant knowledge base snippets (linked in the task file)

**What it does**:
- Reads its task file
- Executes the work (code, research, analysis, file creation, etc.)
- Writes output to `output/{workstream_id}/{task_id}/`
- Writes a completion summary to `tasks/{workstream_id}/{task_id}_done.md`
- Logs its own token usage and timing to `logs/workers/{task_id}.jsonl`

**What it does NOT do**:
- Never reads other workers' tasks or output
- Never modifies the plan
- Never communicates with other workers directly

---

## 3. File System Structure

All paths are relative to `~/atlas/`. The system creates this structure during bootstrap.

```
~/atlas/
  goal.md                          # The input goal specification
  system/
    config.md                      # System configuration (cycle times, max workers, etc.)
    termination.md                 # Termination state and criteria evaluation
    bootstrap.md                   # This architecture doc (or a processed version of it)
    prompts/                       # Agent prompt templates
      sovereign.md
      strategist.md
      conductor.md
      worker.md
      meta_evaluator.md
    hooks/                         # Pre/post execution hooks
      pre_worker.sh
      post_worker.sh
    archive/                       # Archived versions of modified system files
      ...
  directives/
    sovereign.md                   # Course corrections from Sovereign
    strategist.md                  # Planning directives from Strategist
  plan/
    status.md                      # High-level plan status (for Sovereign)
    plan.md                        # Full plan document (for Strategist)
    workstreams/
      {workstream_id}/
        plan.md                    # Workstream-specific plan
        status.md                  # Workstream status (for Conductor to update)
    archive/
      plan_v1.md
      plan_v2.md
      ...
  tasks/
    {workstream_id}/
      {task_id}.md                 # Task assignment (input to Worker)
      {task_id}_done.md            # Task completion summary (output from Worker)
  output/
    {workstream_id}/
      {task_id}/                   # Worker output artifacts
        ...
  reports/
    {workstream_id}/
      report_YYYYMMDD_HHMMSS.md   # Conductor status reports
      latest.md                   # Symlink or copy of most recent report
  knowledge/
    facts/                         # Accumulated facts about the world/domain
      {topic}.md
    meta/                          # Meta-knowledge about agent performance
      {topic}.md
      retro_YYYYMMDD_HHMMSS.md    # Run retrospectives (prose, kept for history)
    index.md                       # Index of all knowledge entries
  metrics/                         # Structured cross-run performance data
    run_history.jsonl              # Quantitative metrics for every completed run
    modification_log.jsonl         # Every self-modification, tagged and tracked
    heuristics.jsonl               # Accumulated heuristics ranked by evidence
    cross_run_analysis/            # Meta-Evaluator analysis reports
      analysis_{run_id}.md         # Per-run structured analysis
      latest.md                    # Most recent analysis (for Strategist quick-read)
    baselines/                     # Baseline snapshots for A/B comparison
      baseline_{run_id}.json       # System config + prompt hashes at run start
  logs/
    sovereign.jsonl                # Sovereign cycle logs
    strategist.jsonl               # Strategist cycle logs
    conductors/
      {workstream_id}.jsonl
    workers/
      {task_id}.jsonl
    system.jsonl                   # System-level events (starts, stops, errors, recoveries)
    tokens.jsonl                   # Aggregated token usage tracking
    improvements.jsonl             # Self-improvement actions taken
    meta_evaluator.jsonl           # Meta-Evaluator session logs
    archive/                       # Rotated old logs
      ...
  artifacts/                       # Final deliverables
    ...
```

### File Conventions

- **All files are markdown or JSONL**. Markdown for human-and-agent readable state. JSONL for structured logs.
- **Every markdown state file has a YAML frontmatter block** with metadata:

```yaml
---
id: workstream-001
status: active | completed | blocked | failed
created: 2026-03-28T10:00:00Z
updated: 2026-03-28T10:05:00Z
owner: conductor-ws001
---
```

- **JSONL log entries** follow this schema:

```json
{
  "ts": "2026-03-28T10:05:00Z",
  "agent": "worker-ws001-t003",
  "event": "task_complete",
  "duration_s": 45,
  "tokens_in": 12000,
  "tokens_out": 3500,
  "details": "Completed research on X. Found 3 relevant papers."
}
```

- **Metrics JSONL entries** follow schemas defined in Section 9.1.
- **File locking**: Not needed. Each file has exactly one writer. The hierarchy enforces this. Workers write to their own task_done and output files. Conductors write to their own reports. The Strategist writes to plan files. The Sovereign writes to directives and termination. The Meta-Evaluator writes to `metrics/` and can write to `system/prompts/`, `system/config.md`, and `system/monitor.sh` between runs (when no other agents are running).

---

## 4. Communication Protocol

Agents communicate exclusively through the file system. There are no direct agent-to-agent messages.

### 4.1 Downward Communication (Higher Tier -> Lower Tier)

| From | To | Mechanism |
|------|-----|-----------|
| Meta-Evaluator -> All tiers | Writes modified prompts to `system/prompts/`, config to `system/config.md`, analysis to `metrics/cross_run_analysis/` | Takes effect on next run start |
| Sovereign -> Strategist | Writes `directives/sovereign.md` | Strategist checks this file each cycle |
| Strategist -> Conductor | Writes/updates `plan/workstreams/{id}/plan.md` | Conductor checks its plan file each cycle |
| Conductor -> Worker | Creates `tasks/{workstream_id}/{task_id}.md` | Worker is launched with this file as input |

### 4.2 Upward Communication (Lower Tier -> Higher Tier)

| From | To | Mechanism |
|------|-----|-----------|
| Worker -> Conductor | Writes `tasks/{ws}/{task}_done.md` and `output/{ws}/{task}/` | Conductor monitors for `_done.md` files |
| Conductor -> Strategist | Writes `reports/{ws}/latest.md` | Strategist reads reports each cycle |
| Strategist -> Sovereign | Updates `plan/status.md` | Sovereign reads this each cycle |
| All tiers -> Meta-Evaluator | Logs, retrospectives, and metrics written during run | Meta-Evaluator reads these between runs |

### 4.3 Escalation Protocol

When an agent encounters something it cannot handle, it escalates:

1. **Worker escalation**: Worker writes `tasks/{ws}/{task}_blocked.md` with a description of the blocker. The Conductor detects this and either reassigns, modifies the task, or escalates to Strategist.

2. **Conductor escalation**: Conductor writes an entry in `reports/{ws}/latest.md` with `status: needs_escalation` and a description. Strategist reads this and decides how to respond (replan, reassign resources, etc.).

3. **Strategist escalation**: Strategist writes to `plan/status.md` with `needs_sovereign_review: true` and a summary. Sovereign reads this and provides direction via `directives/sovereign.md`.

### 4.4 Signal Files

For time-sensitive signals, the system uses lightweight signal files:

```
~/atlas/signals/
  pause                  # If this file exists, all agents pause their cycles
  shutdown               # Graceful shutdown signal
  replan                 # Force Strategist to replan
  restart_{agent_id}     # Force restart of a specific agent
  meta_eval              # Force a Meta-Evaluator run before the next execution
```

Agents check for signals at the start of each cycle. Signal files are empty; their existence is the signal. They are deleted by the agent that processes them.

---

## 5. Plan Lifecycle

### 5.1 Plan Creation

The Strategist creates the plan through this process:

1. **Read the goal** from `goal.md`
2. **Read existing knowledge** from `knowledge/index.md` and relevant entries
3. **Read cross-run analysis** from `metrics/cross_run_analysis/latest.md` (if it exists). This contains the Meta-Evaluator's structured recommendations from prior runs.
4. **Consult the heuristic database** from `metrics/heuristics.jsonl`. Filter for heuristics relevant to the current goal type. Prioritize heuristics with high evidence scores.
5. **Decompose** the goal into workstreams. Each workstream is a major independent thread of work.
6. **For each workstream**, define ordered tasks with:
   - Clear success criteria
   - Input requirements (what files/data the worker needs)
   - Output requirements (what the worker must produce)
   - Estimated complexity (small/medium/large)
   - Dependencies on other tasks (within or across workstreams)
7. **Adversarial review**: The Strategist then reviews its own plan by asking:
   - "What assumptions am I making that could be wrong?"
   - "What's the most likely failure mode?"
   - "Is there a simpler decomposition?"
   - "Are dependencies correctly identified?"
   - "Am I front-loading the riskiest work so we learn early?"
   - "Does this plan contradict any high-confidence heuristics from the database?"
8. **Revise** the plan based on the review
9. **Write** the plan to `plan/plan.md` and individual workstream files

### 5.2 Plan Format

`plan/plan.md`:
```markdown
---
version: 1
created: 2026-03-28T10:00:00Z
status: active
workstream_count: 3
heuristics_applied: ["H-012", "H-034", "H-007"]
---

# Plan: [Goal Summary]

## Workstreams

### WS-001: [Name]
- Status: active
- Tasks: 5
- Completed: 2
- Blocked: 0
- Priority: high

### WS-002: [Name]
- Status: active
- Tasks: 3
- Completed: 0
- Blocked: 0
- Priority: medium

## Dependencies
- WS-002/T-003 depends on WS-001/T-002 (needs output X)

## Risk Register
1. [Risk description] — Mitigation: [approach]
2. ...

## Assumptions
1. [Assumption that, if wrong, would require replanning]
2. ...

## Heuristics Applied
- H-012 (evidence: strong, 5 runs): "Research tasks should be parallelized early" — Applied to WS-001 structure
- H-034 (evidence: moderate, 2 runs): "Front-load dependency resolution" — Applied to task ordering
```

### 5.3 Execution

Once the plan is written:
1. The Strategist writes workstream plans to `plan/workstreams/{id}/plan.md`
2. Conductors are launched (one per workstream) and begin reading their plans
3. Conductors create task files and launch Workers
4. Workers execute and produce output

### 5.4 Pivot Detection

The Strategist checks for pivots each cycle by reading conductor reports and asking:

- **Invalidated assumption**: Did a worker's findings prove an assumption wrong?
- **Blocked workstream**: Is a workstream stuck with no clear path forward?
- **Scope change**: Did we discover the problem is larger/smaller/different than expected?
- **Better approach**: Did we learn something that suggests a fundamentally better strategy?
- **Heuristic contradiction**: Did execution data contradict a heuristic that informed the plan?

When a pivot is detected:
1. Strategist writes a new plan version (incrementing the version number)
2. Strategist marks affected tasks as `cancelled` or `superseded`
3. Conductors detect the plan change on their next cycle and adapt
4. Workers on cancelled tasks are allowed to finish their current operation, then their Conductor does not assign them new work under the old plan

### 5.5 Plan Versioning

Every plan revision increments the version in frontmatter. Old plans are archived:

```
plan/
  plan.md            # Current (version N)
  archive/
    plan_v1.md
    plan_v2.md
    ...
```

The Strategist logs the reason for each revision in the plan file itself under a `## Revision History` section.

---

## 6. Tmux Session Architecture

### 6.1 Session Layout

One tmux session named `atlas`:

```
atlas (session)
  sovereign    (window 0) — Sovereign agent
  strategist   (window 1) — Strategist agent
  conductor-*  (window 2+) — One window per active Conductor
  workers      (window N) — Split panes for active Workers (up to configurable max)
  monitor      (window N+1) — System monitor (watchdog script)
```

The Meta-Evaluator does NOT run in the atlas tmux session. It runs in its own separate invocation between runs (see Section 10.2).

### 6.2 Agent Launch Commands

Each agent is launched as a `claude` CLI process with a carefully constructed prompt. The prompt is assembled from the agent's template plus relevant file contents.

**Sovereign launch**:
```bash
tmux new-window -t atlas -n sovereign
tmux send-keys -t atlas:sovereign \
  "claude -p \"$(cat ~/atlas/system/prompts/sovereign.md)

GOAL:
$(cat ~/atlas/goal.md)

CURRENT STATUS:
$(cat ~/atlas/plan/status.md)

DIRECTIVES YOU HAVE ISSUED:
$(cat ~/atlas/directives/sovereign.md 2>/dev/null || echo 'None yet.')

TERMINATION STATE:
$(cat ~/atlas/system/termination.md)

META-EVALUATOR RECOMMENDATIONS (from between-run analysis):
$(head -50 ~/atlas/metrics/cross_run_analysis/latest.md 2>/dev/null || echo 'No prior analysis available.')

Execute your cycle now. Write your outputs to the appropriate files. When done, output CYCLE_COMPLETE.\"" Enter
```

**Worker launch**:
```bash
tmux send-keys -t atlas:workers.${pane_index} \
  "claude -p \"$(cat ~/atlas/system/prompts/worker.md)

YOUR TASK:
$(cat ~/atlas/tasks/${ws_id}/${task_id}.md)

Execute this task fully. Write all output to ~/atlas/output/${ws_id}/${task_id}/. When complete, write your summary to ~/atlas/tasks/${ws_id}/${task_id}_done.md. Log your work to ~/atlas/logs/workers/${task_id}.jsonl.\"" Enter
```

### 6.3 Cycle Management

Agents do not run in persistent loops within a single Claude context. Instead, the **monitor** script relaunches them on their cycle schedule. This is critical because it prevents context window accumulation.

Each agent runs one cycle, outputs `CYCLE_COMPLETE`, and exits. The monitor detects this and schedules the next cycle launch.

**Why this matters**: If an agent ran in a persistent loop, its context would fill and degrade. By relaunching each cycle with fresh context loaded from files, every cycle gets maximum agent quality.

### 6.4 Monitor Script

The monitor runs in its own tmux window and is the only persistent process. It is a bash script, not a Claude agent.

```
~/atlas/system/monitor.sh
```

Responsibilities:
- Launches agent cycles on schedule
- Detects stalled agents (no output for configurable timeout)
- Detects crashed agents (tmux pane exited unexpectedly)
- Writes to `logs/system.jsonl`
- Checks for signal files in `signals/`
- Manages Worker pane pool (creates/destroys panes as needed)
- Tracks token usage from agent log files
- Provides the heartbeat that keeps the system alive
- **Writes structured run metrics** to `metrics/run_history.jsonl` at end of run (see Section 9.1)
- **Snapshots baseline state** at run start to `metrics/baselines/` for A/B comparison (see Section 9.2)

The monitor is the one piece that must NOT be a Claude agent. It is pure bash with well-defined behavior. If the monitor crashes, the system stops (and can be restarted manually or via cron).

### 6.5 Concurrency Limits

Configurable in `system/config.md`:

```yaml
max_concurrent_workers: 4
max_concurrent_conductors: 3
sovereign_cycle_minutes: 5
strategist_cycle_minutes: 2
conductor_cycle_minutes: 1
worker_stall_timeout_minutes: 10
conductor_stall_timeout_minutes: 5
meta_evaluator_timeout_minutes: 30
```

These limits prevent overwhelming the system. The number of Workers is the primary control for parallelism and token spend rate.

---

## 7. Logging and Observability

### 7.1 What Gets Logged

Every agent cycle produces a log entry. The structured fields are:

```json
{
  "ts": "ISO-8601 timestamp",
  "agent_type": "sovereign|strategist|conductor|worker",
  "agent_id": "unique identifier",
  "cycle": "integer cycle number",
  "run_id": "unique run identifier (set at run start)",
  "event": "cycle_start|cycle_complete|error|escalation|stall_detected|recovery|...",
  "duration_s": "seconds the cycle took",
  "tokens_in": "input tokens consumed",
  "tokens_out": "output tokens generated",
  "files_read": ["list of files read"],
  "files_written": ["list of files written"],
  "outcome": "free-text summary of what happened",
  "errors": ["any errors encountered"],
  "modification_ids": ["IDs of any self-modifications applied during this cycle"]
}
```

The `run_id` field is critical for cross-run analysis. It is generated at run start and included in every log entry, enabling the Meta-Evaluator to slice metrics by run.

### 7.2 Token Tracking

The monitor script aggregates token usage from all agent logs into `logs/tokens.jsonl`:

```json
{
  "ts": "2026-03-28T10:05:00Z",
  "run_id": "run-20260328-100000",
  "period": "5min",
  "total_tokens_in": 50000,
  "total_tokens_out": 15000,
  "by_tier": {
    "sovereign": {"in": 2000, "out": 500},
    "strategist": {"in": 8000, "out": 3000},
    "conductor": {"in": 15000, "out": 4000},
    "worker": {"in": 25000, "out": 7500}
  },
  "cumulative_tokens": 1500000,
  "estimated_cost_usd": 12.50
}
```

### 7.3 Performance Metrics

Tracked per task and per workstream:

- **Time to complete**: Wall clock time from task creation to `_done.md`
- **Token efficiency**: Tokens spent per task, normalized by task complexity
- **Retry count**: How many times a task was attempted before completion
- **Escalation count**: How many times work was escalated
- **Plan revision count**: How many times the plan was revised
- **Tokens per task-complexity-unit**: Tokens divided by estimated complexity (small=1, medium=3, large=5)
- **Heuristic hit rate**: Of the heuristics applied during planning, how many were validated by execution

These metrics are collected during the run and written to `metrics/run_history.jsonl` at run completion (see Section 9.1 for the full schema).

### 7.4 System Dashboard

The monitor generates a human-readable dashboard file every 30 seconds:

```
~/atlas/logs/dashboard.md
```

Contents:
```markdown
# ATLAS Dashboard
Updated: 2026-03-28T10:05:30Z

## Goal
[One-line goal summary]

## Status: RUNNING
- Run ID: run-20260328-100000
- Elapsed: 1h 23m
- Total tokens: 1.5M (est. $12.50)
- Plan version: 3
- Active modifications: MOD-017 (worker prompt verbosity reduction), MOD-019 (conductor cycle time 45s)

## Cross-Run Context
- This is run #7
- Token efficiency trend: improving (12% better than run #6)
- Active heuristics applied: 4
- Meta-Evaluator last ran: 2026-03-28T09:58:00Z

## Workstreams
| ID | Name | Status | Progress | Workers |
|----|------|--------|----------|---------|
| WS-001 | Research | active | 4/5 tasks | 2 |
| WS-002 | Analysis | active | 1/3 tasks | 1 |
| WS-003 | Synthesis | waiting | 0/2 tasks | 0 |

## Active Workers
| Task | Workstream | Running | Status |
|------|------------|---------|--------|
| T-005 | WS-001 | 3m 22s | executing |
| T-004 | WS-001 | 1m 10s | executing |
| T-001 | WS-002 | 5m 44s | executing |

## Recent Events
- 10:05:00 — Worker T-003 completed (WS-001)
- 10:03:12 — Strategist: plan revision v3 (risk R-002 materialized)
- 10:01:00 — Conductor WS-001: escalated T-005 dependency issue
```

---

## 8. Self-Improvement Loop

This is the mechanism by which the system gets better over time within a single run. For cross-run improvement, see Section 9 (Cross-Run Learning System) and Section 10 (Meta-Evaluator Layer).

### 8.1 Within-Run Learning

**Knowledge capture**: When a Worker discovers something non-obvious (a fact about the domain, a technique that worked, a dead end), the Conductor captures this in `knowledge/facts/{topic}.md`. The Strategist can then read this when revising the plan or when future tasks touch the same topic.

**Pattern detection**: The Strategist, on each cycle, briefly reviews whether recurring patterns are emerging:
- Are workers consistently underestimating task complexity? -> Adjust complexity estimates.
- Is a particular type of task always getting blocked? -> Restructure.
- Are escalations concentrated in one workstream? -> That workstream may need a different approach.

### 8.2 Cross-Run Learning (Persistent Knowledge)

After a run completes, the system writes two things:

**1. A prose retrospective** (legacy format, kept for human readability):

```
~/atlas/knowledge/meta/retro_YYYYMMDD_HHMMSS.md
```

Contents:
- What was the goal?
- What worked well?
- What didn't work?
- What was the final plan version and how many revisions occurred?
- Token efficiency metrics
- Recommendations for future runs

**2. A structured run record** (machine-readable, for cross-run analysis):

Written to `metrics/run_history.jsonl` — see Section 9.1 for the full schema. This is what the Meta-Evaluator and the cross-run analysis phase actually use.

The prose retrospective is still written for human review and for cases where an agent needs narrative context. But the structured metrics are the primary input for systematic cross-run improvement.

### 8.3 Prompt Evolution

The system can modify its own prompt templates in `system/prompts/`. The process:

1. The Strategist identifies a systematic issue (e.g., "Workers are producing verbose output that wastes conductor context")
2. The Strategist writes a proposed prompt modification to `knowledge/meta/prompt_proposals/{proposal_id}.md`, including a **modification ID** (format: `MOD-{NNN}`) and a **hypothesis** about what improvement the change should produce
3. On the next Sovereign cycle, the Sovereign reviews the proposal (it's flagged in `plan/status.md`)
4. If approved, the Strategist applies the change to `system/prompts/{agent_type}.md`
5. The change takes effect on the next cycle of that agent type
6. The change is logged in `logs/improvements.jsonl` AND in `metrics/modification_log.jsonl` with the modification ID, the hypothesis, and the before/after state
7. Subsequent runs will measure whether the hypothesis was correct (see Section 9.2)

Note: This is the within-run prompt evolution mechanism. The Meta-Evaluator can also rewrite prompts between runs without Sovereign approval, since it operates at a higher level (see Section 10).

### 8.4 Structural Self-Modification

The system can modify deeper aspects of itself:

- **Cycle timing**: If the Sovereign detects the Strategist is cycling too fast (wasting tokens reviewing unchanged state), it can modify `system/config.md` to increase the interval.
- **Worker count**: If tasks are bottlenecked, the Strategist can recommend increasing `max_concurrent_workers`.
- **Hierarchy changes**: In extreme cases, the system can add or remove tiers. For example, if a goal is simple enough, the Strategist can eliminate the Conductor tier and have the Strategist directly manage Workers. This is recorded in `knowledge/meta/structural_changes.md`.

All structural self-modifications within a run are tagged with modification IDs and logged to `metrics/modification_log.jsonl` for cross-run tracking.

### 8.5 Guard Rails on Self-Modification

Self-modification is powerful but dangerous. Guard rails:

1. **All modifications are logged** in `logs/improvements.jsonl` and `metrics/modification_log.jsonl` with before/after state and a unique modification ID
2. **Prompt changes require Sovereign approval** during a run (via the proposal process). Between runs, the Meta-Evaluator can modify prompts directly.
3. **Structural changes require explicit justification** written to the knowledge base
4. **Rollback capability**: The previous version of any modified file is archived in `system/archive/` with a timestamp
5. **No modification during the first 3 cycles**: The system must run at least 3 full Strategist cycles before any within-run self-modification is allowed. This prevents premature optimization based on insufficient data.
6. **Meta-Evaluator modifications require evidence threshold**: The Meta-Evaluator must meet quantitative criteria before applying changes (see Section 10.3)

---

## 9. Cross-Run Learning System

This section specifies the structured mechanisms by which ATLAS learns across runs. While Section 8 covers within-run learning, this section covers the persistent, quantitative learning infrastructure that accumulates over the system's lifetime.

### 9.1 Structured Run Metrics

At the end of every run, the monitor writes a structured record to `metrics/run_history.jsonl`. This is the primary data source for cross-run analysis.

**Schema:**

```json
{
  "run_id": "run-20260328-100000",
  "ts_start": "2026-03-28T10:00:00Z",
  "ts_end": "2026-03-28T11:23:00Z",
  "goal_type": "research",
  "goal_hash": "sha256 of goal.md for deduplication",
  "goal_summary": "One-line goal summary",

  "execution_metrics": {
    "total_duration_s": 4980,
    "total_tokens_in": 1200000,
    "total_tokens_out": 450000,
    "total_tokens": 1650000,
    "estimated_cost_usd": 13.75,
    "tokens_per_task_complexity_unit": 18500,
    "tasks_created": 14,
    "tasks_completed": 12,
    "tasks_failed": 1,
    "tasks_cancelled": 1,
    "task_completion_rate": 0.857,
    "avg_task_duration_s": 210,
    "median_task_duration_s": 180
  },

  "plan_metrics": {
    "plan_versions": 3,
    "plan_revisions": 2,
    "revision_reasons": ["assumption_invalidated", "scope_change"],
    "workstream_count": 3,
    "workstreams_completed": 2,
    "initial_task_count": 10,
    "final_task_count": 14
  },

  "quality_metrics": {
    "escalation_count": 4,
    "escalation_rate_per_task": 0.286,
    "retry_count": 2,
    "retry_rate_per_task": 0.143,
    "stall_count": 1,
    "recovery_count": 1,
    "worker_output_rejection_count": 0
  },

  "efficiency_metrics": {
    "tokens_by_tier": {
      "sovereign": 36000,
      "strategist": 360000,
      "conductor": 720000,
      "worker": 534000
    },
    "overhead_ratio": 0.676,
    "useful_work_ratio": 0.324,
    "tokens_per_completed_task": 137500,
    "time_per_completed_task_s": 415
  },

  "self_modification_metrics": {
    "modifications_applied": ["MOD-017", "MOD-019"],
    "prompt_changes": 1,
    "config_changes": 1,
    "structural_changes": 0
  },

  "heuristic_metrics": {
    "heuristics_applied": ["H-012", "H-034", "H-007"],
    "heuristics_validated": ["H-012", "H-007"],
    "heuristics_contradicted": [],
    "heuristics_neutral": ["H-034"]
  },

  "termination": {
    "reason": "success_criteria_met",
    "criteria_met": 3,
    "criteria_total": 3
  }
}
```

The `overhead_ratio` is the fraction of total tokens consumed by non-Worker agents (Sovereign + Strategist + Conductor), representing management overhead. The `useful_work_ratio` is the complement: tokens spent on actual task execution. The Meta-Evaluator uses these to detect overhead bloat.

### 9.2 A/B-Style Modification Tracking

Every self-modification — whether made within a run by the Strategist/Sovereign or between runs by the Meta-Evaluator — is tagged with a unique modification ID and tracked for impact.

**Modification log schema** (`metrics/modification_log.jsonl`):

```json
{
  "mod_id": "MOD-017",
  "ts_created": "2026-03-28T10:30:00Z",
  "source": "strategist | sovereign | meta_evaluator",
  "category": "prompt | config | structure | protocol",
  "target": "system/prompts/worker.md",
  "description": "Reduced worker output verbosity instructions. Added 'Be concise. Limit output to essential findings.' to worker prompt.",
  "hypothesis": "Worker output verbosity is wasting conductor context. This change should reduce avg conductor tokens_in by 15%+.",
  "expected_metric": "efficiency_metrics.tokens_by_tier.conductor",
  "expected_direction": "decrease",
  "expected_magnitude": 0.15,
  "before_hash": "sha256 of file before change",
  "after_hash": "sha256 of file after change",
  "before_snapshot": "system/archive/worker_20260328_103000.md",
  "applied_in_run": "run-20260328-100000",
  "status": "active | rolled_back | superseded",
  "impact_measurements": [
    {
      "run_id": "run-20260328-140000",
      "metric_value": 612000,
      "baseline_value": 720000,
      "delta_pct": -0.15,
      "verdict": "confirmed"
    },
    {
      "run_id": "run-20260329-090000",
      "metric_value": 595000,
      "baseline_value": 720000,
      "delta_pct": -0.174,
      "verdict": "confirmed"
    }
  ],
  "confidence": "high | moderate | low | pending",
  "runs_measured": 2,
  "avg_impact_pct": -0.162,
  "verdict": "confirmed_beneficial | confirmed_harmful | inconclusive | pending"
}
```

**Baseline snapshots**: At the start of every run, the monitor writes a baseline snapshot to `metrics/baselines/baseline_{run_id}.json`. This captures:

```json
{
  "run_id": "run-20260328-140000",
  "ts": "2026-03-28T14:00:00Z",
  "config_hash": "sha256 of system/config.md",
  "prompt_hashes": {
    "sovereign": "sha256",
    "strategist": "sha256",
    "conductor": "sha256",
    "worker": "sha256",
    "meta_evaluator": "sha256"
  },
  "active_modifications": ["MOD-017", "MOD-019"],
  "active_heuristics": ["H-012", "H-034", "H-007"],
  "system_config": {
    "max_concurrent_workers": 4,
    "sovereign_cycle_minutes": 5,
    "strategist_cycle_minutes": 2,
    "conductor_cycle_minutes": 1
  }
}
```

This enables the Meta-Evaluator to compare runs that had different configurations and attribute performance differences to specific modifications.

**Impact measurement process**:
1. When a modification is made, it is logged with a hypothesis and expected metric
2. On subsequent runs, the Meta-Evaluator compares the relevant metric against pre-modification baselines
3. After 2+ runs with the modification active, the Meta-Evaluator assigns a confidence level and verdict
4. Modifications confirmed as harmful are rolled back (the archived pre-change version is restored)
5. Modifications confirmed as beneficial are kept and their confidence is upgraded

### 9.3 Heuristic Database

Instead of accumulating "lessons learned" as prose, the system maintains a structured heuristic database in `metrics/heuristics.jsonl`. Each heuristic is a concrete, actionable rule that the Strategist can consult during planning.

**Heuristic schema:**

```json
{
  "heuristic_id": "H-012",
  "ts_created": "2026-03-27T15:00:00Z",
  "ts_updated": "2026-03-28T11:30:00Z",
  "category": "planning | execution | resource_allocation | communication | recovery",
  "goal_types": ["research", "analysis"],
  "rule": "Research tasks should be parallelized early rather than sequenced, because findings from parallel research often invalidate sequential assumptions anyway.",
  "evidence": {
    "supporting_runs": ["run-20260327-150000", "run-20260328-100000", "run-20260328-140000"],
    "contradicting_runs": [],
    "neutral_runs": ["run-20260327-090000"],
    "total_supporting": 3,
    "total_contradicting": 0,
    "quantitative_impact": {
      "metric": "plan_metrics.plan_revisions",
      "avg_with_heuristic": 1.5,
      "avg_without_heuristic": 3.2,
      "improvement_pct": 0.531
    }
  },
  "evidence_strength": "strong",
  "rank": 3,
  "source": "strategist_observation | meta_evaluator_analysis | worker_discovery",
  "last_applied_in": "run-20260328-100000",
  "times_applied": 3,
  "times_validated": 3,
  "times_contradicted": 0,
  "status": "active | deprecated | experimental"
}
```

**Evidence strength tiers:**
- **experimental**: Applied in 0-1 runs. No measured impact yet. Used cautiously.
- **weak**: Applied in 2 runs. Some supporting evidence but not conclusive.
- **moderate**: Applied in 3-4 runs with consistent positive results.
- **strong**: Applied in 5+ runs with quantitative evidence of improvement.

**Heuristic lifecycle:**
1. **Creation**: A heuristic is proposed when the Strategist observes a pattern during a run, or when the Meta-Evaluator identifies one during cross-run analysis. It starts as `experimental`.
2. **Testing**: The Strategist applies the heuristic in subsequent plans (logging which heuristics were applied in the plan frontmatter). After the run, the outcome is measured.
3. **Promotion**: As supporting evidence accumulates, the evidence strength is upgraded.
4. **Demotion**: If contradicting evidence appears, the evidence strength is downgraded.
5. **Deprecation**: If a heuristic is contradicted more than it is supported, or if it becomes irrelevant (e.g., the Meta-Evaluator made a structural change that renders it moot), it is marked `deprecated` and no longer consulted.
6. **Ranking**: Active heuristics are ranked by `evidence_strength` first, then by `times_validated / times_applied` ratio, then by recency of last validation. The Strategist sees them in rank order.

### 9.4 Cross-Run Analysis Phase

This is a dedicated analysis phase that runs between runs. It is performed by the Meta-Evaluator (see Section 10) but the analysis methodology is specified here.

**What gets analyzed:**

1. **Performance trajectories**: For each metric in the run history, compute the trend over the last N runs. Are we improving, degrading, or plateauing? Specific metrics tracked:
   - Tokens per completed task (efficiency)
   - Plan revision count (planning quality)
   - Escalation rate (execution quality)
   - Task completion rate (reliability)
   - Overhead ratio (management efficiency)
   - Time per completed task (speed)

2. **Modification impact**: For each active modification, compute its measured impact across all runs since it was applied. Compare the relevant metric against the pre-modification baseline. Flag modifications with inconclusive or negative impact for review.

3. **Heuristic accuracy**: For each heuristic applied in the latest run, check whether the expected outcome materialized. Update the heuristic's evidence record.

4. **Anomaly detection**: Flag runs where metrics deviated significantly from the trend (both positive and negative). Investigate what was different about those runs (different goal type? different modifications active? different scale?).

5. **Overhead analysis**: Is the management overhead (Sovereign + Strategist + Conductor tokens) proportional to the work being done? Is it trending in the right direction? If overhead is growing faster than useful work, something is wrong.

**Output**: A structured analysis report written to `metrics/cross_run_analysis/analysis_{run_id}.md`, plus an update to `metrics/cross_run_analysis/latest.md`. The Strategist reads `latest.md` at the start of the next run.

---

## 10. Meta-Evaluator Layer

The Meta-Evaluator is the component that turns ATLAS from "a system that executes goals" into "a system that gets better at executing goals." It operates above the Sovereign, between runs, and treats the entire ATLAS system as code to be optimized.

### 10.1 Role and Scope

The Sovereign improves execution within a run — it detects when things are going wrong and corrects course. The Meta-Evaluator improves the system itself across runs — it detects when the system's structure, prompts, configuration, or protocols are suboptimal and rewrites them.

**What the Meta-Evaluator can modify:**
- Agent prompt templates (`system/prompts/*.md`)
- System configuration (`system/config.md`) — cycle timings, concurrency limits, stall timeouts
- Monitor script behavior (`system/monitor.sh`) — launch logic, stall detection thresholds, dashboard contents
- Communication protocol — file paths, report formats, escalation rules
- Tier count — adding or removing hierarchy levels
- The Sovereign's prompt and behavior (the Meta-Evaluator is the only entity that can modify the Sovereign)
- The Meta-Evaluator's own prompt (`system/prompts/meta_evaluator.md`) — it can improve itself

**What the Meta-Evaluator cannot modify:**
- The goal (that is the user's domain)
- Historical data (metrics, logs, retrospectives are append-only and immutable)
- The watchdog cron job (a human safety net)
- This architecture document (the source of truth; changes to the architecture are proposed in `knowledge/meta/architecture_proposals/` for human review)

### 10.2 Execution Model

The Meta-Evaluator runs as a standalone Claude invocation between runs. It is NOT part of the tmux session. It runs, completes, and exits.

**Trigger**: The Meta-Evaluator is launched by `start.sh` during the inter-run phase. The sequence is:

1. Previous run completes (graceful shutdown writes final metrics)
2. User places new `goal.md`
3. User runs `~/atlas/system/start.sh`
4. `start.sh` launches the Meta-Evaluator BEFORE starting the tmux session:

```bash
# Inter-run Meta-Evaluator phase
echo "Running Meta-Evaluator analysis..."
claude -p "$(cat ~/atlas/system/prompts/meta_evaluator.md)

RUN HISTORY (last 10 runs):
$(tail -10 ~/atlas/metrics/run_history.jsonl)

MODIFICATION LOG:
$(cat ~/atlas/metrics/modification_log.jsonl)

HEURISTIC DATABASE:
$(cat ~/atlas/metrics/heuristics.jsonl)

PREVIOUS CROSS-RUN ANALYSIS:
$(cat ~/atlas/metrics/cross_run_analysis/latest.md 2>/dev/null || echo 'No prior analysis.')

CURRENT SYSTEM CONFIGURATION:
$(cat ~/atlas/system/config.md)

CURRENT PROMPTS (hashes and sizes):
$(for f in ~/atlas/system/prompts/*.md; do echo "$(basename $f): $(wc -c < $f) bytes, sha256: $(shasum -a 256 $f | cut -d' ' -f1)"; done)

LATEST RETROSPECTIVE:
$(ls -t ~/atlas/knowledge/meta/retro_*.md 2>/dev/null | head -1 | xargs cat 2>/dev/null || echo 'No retrospective.')

Execute your analysis cycle. Write your analysis to ~/atlas/metrics/cross_run_analysis/. Apply any approved modifications. Log everything to ~/atlas/logs/meta_evaluator.jsonl. When done, output CYCLE_COMPLETE."
```

5. After the Meta-Evaluator completes, `start.sh` proceeds with the normal run setup (clearing transient state, starting tmux, launching monitor)

**Timeout**: The Meta-Evaluator has a configurable timeout (`meta_evaluator_timeout_minutes` in `system/config.md`, default 30 minutes). If it exceeds this, it is killed and the run proceeds with the current system state. This prevents the Meta-Evaluator from becoming a bottleneck.

**Manual trigger**: An operator can force a Meta-Evaluator run at any time by running:
```bash
touch ~/atlas/signals/meta_eval
~/atlas/system/run_meta_evaluator.sh
```

### 10.3 Evaluation Criteria

The Meta-Evaluator evaluates the system against these structured criteria. Each criterion has a target direction and a weight.

```yaml
evaluation_criteria:
  token_efficiency:
    metric: execution_metrics.tokens_per_task_complexity_unit
    target: decrease
    weight: 0.20
    description: "Tokens spent per unit of task complexity should decrease over time"

  plan_stability:
    metric: plan_metrics.plan_revisions
    target: decrease
    weight: 0.15
    description: "Number of plan revisions per run should decrease as planning improves"

  task_completion_rate:
    metric: execution_metrics.task_completion_rate
    target: increase
    weight: 0.20
    description: "Percentage of created tasks that complete successfully"

  time_efficiency:
    metric: efficiency_metrics.time_per_completed_task_s
    target: decrease
    weight: 0.15
    description: "Wall-clock time per completed task should decrease"

  overhead_ratio:
    metric: efficiency_metrics.overhead_ratio
    target: decrease
    weight: 0.10
    description: "Management overhead as fraction of total tokens should shrink"

  escalation_rate:
    metric: quality_metrics.escalation_rate_per_task
    target: decrease
    weight: 0.10
    description: "Escalations per task should decrease as agents improve"

  recovery_frequency:
    metric: quality_metrics.stall_count + quality_metrics.recovery_count
    target: decrease
    weight: 0.10
    description: "Stalls and recoveries should decrease as the system stabilizes"
```

**Composite improvement score**: The Meta-Evaluator computes a weighted composite score across all criteria for each run, comparing against the moving average of the previous 5 runs. A positive composite score means the system is improving. A negative score means it is degrading.

**Modification threshold**: The Meta-Evaluator only applies a structural change if:
1. The evidence supporting the change spans at least 2 runs
2. The expected improvement in the composite score exceeds 5%
3. No existing modification with a contradictory effect is already active
4. The change does not violate any operational invariant from Section 15.1

### 10.4 Modification Changelog

The Meta-Evaluator maintains a structured changelog of every modification it has made, separate from the Strategist's within-run modification log. Both are written to `metrics/modification_log.jsonl` but distinguished by the `source` field.

The Meta-Evaluator also writes a human-readable changelog summary to `metrics/cross_run_analysis/changelog.md`:

```markdown
# Meta-Evaluator Modification Changelog

## MOD-020 (2026-03-28, between run-7 and run-8)
- **Target**: system/prompts/strategist.md
- **Change**: Added instruction to consult heuristic database before adversarial review step
- **Evidence**: Runs 5-7 showed strategist plans contradicting established heuristics. H-012 was ignored in run-6 leading to 2 extra plan revisions.
- **Expected impact**: plan_revisions decrease by 20%
- **Measured impact**: run-8: plan_revisions = 1 (vs 3-run avg of 2.7). Confirmed beneficial.
- **Status**: active, confidence: moderate (1 confirming run)

## MOD-018 (2026-03-27, between run-5 and run-6)
- **Target**: system/config.md
- **Change**: Reduced sovereign_cycle_minutes from 5 to 7. Sovereign was cycling with no new information 60% of the time.
- **Evidence**: Runs 3-5 sovereign logs showed 60% of cycles had no state change to evaluate.
- **Expected impact**: sovereign token usage decrease by 30%
- **Measured impact**: run-6: sovereign tokens = 25K (vs baseline 36K, -30.5%). run-7: 24K (-33.3%). Confirmed beneficial.
- **Status**: active, confidence: high (2 confirming runs)
```

### 10.5 Self-Modification of the Meta-Evaluator

The Meta-Evaluator can modify its own prompt and evaluation criteria. This is the deepest form of self-improvement in the system. Guard rails:

1. **Self-modifications are logged with full before/after state** in `metrics/modification_log.jsonl`
2. **The previous version of the Meta-Evaluator prompt is always archived** in `system/archive/`
3. **A self-modification that degrades the composite improvement score over 2 consecutive runs is automatically rolled back** by the `start.sh` script (which checks the modification log before launching the Meta-Evaluator)
4. **The Meta-Evaluator cannot remove its own evaluation criteria** — it can adjust weights and add new criteria, but removal requires a human editing the architecture doc
5. **The Meta-Evaluator cannot disable its own logging** — the logging code is in the launch script, not in the prompt

### 10.6 Meta-Evaluator Prompt Template

```markdown
# Role: META-EVALUATOR

You are the Meta-Evaluator of the ATLAS system. You run BETWEEN execution runs and your job is to improve the system itself.

## Your Mission

You are the reason ATLAS gets better over time. The Sovereign optimizes execution within a run. You optimize the system across runs. Every component of ATLAS — prompts, configuration, hierarchy, protocols — is code that you can rewrite.

## Your Cycle

1. Read the RUN HISTORY provided. Compute performance trends across the last N runs.
2. Read the MODIFICATION LOG. For each active modification, measure its impact by comparing post-modification run metrics against pre-modification baselines.
3. Read the HEURISTIC DATABASE. Update evidence scores based on the latest run. Promote, demote, or deprecate heuristics as warranted.
4. Identify the top 3 performance bottlenecks based on the evaluation criteria.
5. For each bottleneck, generate a concrete modification proposal with:
   - What to change (specific file, specific section)
   - Why (quantitative evidence from run history)
   - Expected impact (which metric, what direction, what magnitude)
   - Rollback criteria (what would indicate this change was harmful)
6. Evaluate each proposal against the modification threshold (Section 10.3).
7. Apply proposals that meet the threshold. Archive the previous versions.
8. Write your analysis report to ~/atlas/metrics/cross_run_analysis/
9. Update ~/atlas/metrics/cross_run_analysis/latest.md
10. Log everything to ~/atlas/logs/meta_evaluator.jsonl
11. Output CYCLE_COMPLETE

## Evaluation Criteria (weighted)

- Token efficiency (20%): tokens_per_task_complexity_unit should decrease
- Plan stability (15%): plan_revisions should decrease
- Task completion rate (20%): task_completion_rate should increase
- Time efficiency (15%): time_per_completed_task_s should decrease
- Overhead ratio (10%): overhead_ratio should decrease
- Escalation rate (10%): escalation_rate_per_task should decrease
- Recovery frequency (10%): stall + recovery counts should decrease

## Modification Rules

- Every modification gets a unique MOD-{NNN} ID
- Every modification includes a hypothesis and expected metric impact
- Archive previous versions before modifying
- Do NOT modify: goal.md, historical metrics, watchdog.sh, this architecture doc
- You CAN modify: all prompts (including Sovereign's), config, monitor script, protocols
- You CAN modify your own prompt — but the change must be logged and is auto-rolled-back if the next 2 runs show composite score degradation
- Minimum evidence: 2 runs of supporting data before applying a change
- Minimum expected improvement: 5% composite score improvement

## Output Format

Write your analysis report in structured markdown with quantitative data. Do not write vague prose. Every recommendation must cite specific run IDs and metric values.
```

---

## 11. Recovery Mechanisms

### 11.1 Worker Stall Recovery

**Detection**: The monitor checks if a Worker's tmux pane has produced output in the last `worker_stall_timeout_minutes`. It also checks if the Worker's log file has been updated.

**Recovery**:
1. Send Ctrl-C to the pane (attempt graceful stop)
2. Wait 5 seconds
3. If still running, kill the pane
4. Write a `tasks/{ws}/{task}_stalled.md` file with whatever output was captured
5. The Conductor detects the stall file and decides: retry the same task, modify the task, or escalate

### 11.2 Conductor Stall Recovery

**Detection**: Monitor checks for Conductor output/log freshness.

**Recovery**:
1. Kill the Conductor's window
2. Relaunch with fresh context from files
3. The new Conductor reads its workstream plan and task states, resuming from where the previous instance left off
4. Log the recovery event

### 11.3 Strategist/Sovereign Recovery

Same pattern: kill and relaunch with fresh context. These agents are stateless between cycles by design (all state is in files), so recovery is just relaunching.

### 11.4 Catastrophic Recovery

If the monitor itself crashes or the entire tmux session is lost:

1. A cron job runs every 2 minutes: `~/atlas/system/watchdog.sh`
2. This script checks if the `atlas` tmux session exists
3. If not, and if `signals/shutdown` does NOT exist (meaning it wasn't an intentional stop), it relaunches the monitor
4. The monitor then restores the system state from files

`watchdog.sh`:
```bash
#!/bin/bash
ATLAS_HOME="$HOME/atlas"
if ! tmux has-session -t atlas 2>/dev/null; then
  if [ ! -f "$ATLAS_HOME/signals/shutdown" ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) WATCHDOG: Session lost, restarting" \
      >> "$ATLAS_HOME/logs/system.jsonl"
    "$ATLAS_HOME/system/monitor.sh" &
  fi
fi
```

### 11.5 Context Loss Recovery

Since agents are relaunched each cycle with fresh context from files, context loss is the NORMAL operating mode, not an exception. The entire architecture is designed around this.

The critical implication: **everything an agent needs to continue must be written to a file before it ends its cycle.** Agent prompt templates must include explicit instructions to persist all relevant state before outputting `CYCLE_COMPLETE`.

### 11.6 Meta-Evaluator Recovery

The Meta-Evaluator runs as a one-shot invocation between runs, so there is no persistent process to crash. If the Meta-Evaluator fails:

1. **Timeout**: If it exceeds `meta_evaluator_timeout_minutes`, the `start.sh` script kills it and proceeds with the run using the current system state. No modifications are applied.
2. **Error**: If the Meta-Evaluator crashes, `start.sh` logs the error and proceeds. The system is fully functional without the Meta-Evaluator — it just does not get between-run optimization for that cycle.
3. **Bad modification**: If the Meta-Evaluator applies a modification that degrades performance, the automatic rollback mechanism (checking modification log at next Meta-Evaluator run) corrects it. For severe degradation, the operator can manually restore from `system/archive/`.

The Meta-Evaluator is designed to be fail-safe: its absence degrades optimization, not execution.

---

## 12. Goal Specification Format

Goals are written to `~/atlas/goal.md` by the user (or by a launcher script). Format:

```markdown
---
type: research | engineering | optimization | analysis | creative | hybrid
priority: speed | quality | cost
max_budget_tokens: 10000000
max_time_hours: 4
---

# Goal

[Clear, specific description of what needs to be accomplished]

## Success Criteria

1. [Measurable criterion]
2. [Measurable criterion]
3. ...

## Constraints

- [Any constraints: languages, tools, approaches to avoid, etc.]

## Context

[Any relevant background the system should know before planning]

## Inputs

- [List of input files, URLs, repos, or data the system should use]

## Expected Outputs

- [What artifacts should the system produce?]
- [Where should they be placed?]
```

### Goal Types and Their Implications

- **research**: Emphasis on breadth, source quality, synthesis. Workers do investigation and produce findings. Plan includes literature review, synthesis, gap analysis phases.
- **engineering**: Emphasis on working code, tests, documentation. Workers write code. Plan includes implementation, testing, integration phases.
- **optimization**: Emphasis on measurement, iteration, improvement. Workers run experiments. Plan includes baseline, hypothesis, experiment, evaluation phases.
- **analysis**: Emphasis on data examination, pattern finding, insight generation. Workers process data. Plan includes data ingestion, analysis, visualization, interpretation phases.
- **creative**: Emphasis on ideation, drafting, revision. Workers produce creative output. Plan includes brainstorm, draft, review, refine phases.
- **hybrid**: System chooses the best decomposition.

The `priority` field influences planning:
- **speed**: Maximize parallelism, accept lower quality, fewer review passes
- **quality**: More review passes, adversarial testing, slower but higher quality
- **cost**: Minimize token usage, fewer workers, more careful task sizing

The `type` field also influences which heuristics the Strategist consults from the heuristic database — heuristics are tagged with applicable goal types (see Section 9.3).

---

## 13. Termination Criteria

The Sovereign evaluates termination on each cycle by reading `system/termination.md`:

```markdown
---
status: running | completed | failed | timeout | budget_exhausted
---

# Termination Evaluation

## Hard Limits
- Budget: 8,500,000 / 10,000,000 tokens used
- Time: 2h 15m / 4h 00m elapsed

## Success Criteria Evaluation
1. [Criterion 1]: MET / NOT MET / PARTIALLY MET — [evidence]
2. [Criterion 2]: MET / NOT MET / PARTIALLY MET — [evidence]
3. [Criterion 3]: MET / NOT MET / PARTIALLY MET — [evidence]

## Sovereign Assessment
[Free-text assessment of whether to continue or terminate]

## Decision
CONTINUE | TERMINATE

## If TERMINATE, Reason
[Why the system is stopping]
```

### Termination Conditions

The system terminates when ANY of these are true:

1. **All success criteria met**: The goal is achieved.
2. **Budget exhausted**: Token budget reached. The system attempts to produce the best partial result.
3. **Time exceeded**: Time limit reached. Same as budget — best partial result.
4. **Diminishing returns**: The Sovereign detects that the last N cycles have not meaningfully progressed toward the goal. This prevents infinite loops.
5. **Impossible goal**: The Strategist concludes (and the Sovereign agrees) that the goal cannot be achieved with available resources.
6. **Shutdown signal**: `signals/shutdown` file exists.

### Graceful Shutdown Procedure

1. Sovereign writes `signals/shutdown`
2. Monitor stops launching new cycles
3. Active Workers are allowed to complete their current task (with a 2-minute hard timeout)
4. Conductors write final reports
5. Strategist writes final plan status
6. The system writes a final summary to `artifacts/final_summary.md`
7. The system writes a prose retrospective to `knowledge/meta/`
8. **The monitor writes the structured run record to `metrics/run_history.jsonl`** (see Section 9.1)
9. **The monitor updates the modification log with end-of-run metric snapshots** for any modifications that were active during the run
10. Monitor writes final system log entry and exits
11. **The Meta-Evaluator is available to run before the next execution** (launched by `start.sh`)

---

## 14. Bootstrap Procedure

### 14.1 First-Time Bootstrap

When the system has never been run before, the bootstrap agent must create the entire file structure and initial files.

**Bootstrap command** (run by the user or a launcher):

```bash
mkdir -p ~/atlas
# Place goal.md and this architecture doc in ~/atlas/
claude -p "You are the ATLAS bootstrap agent. Read ~/atlas/NEXUS_ARCHITECTURE.md for the full system design. Your job is to:

1. Create the entire directory structure specified in Section 3 (including the metrics/ directory tree)
2. Create the monitor.sh script specified in Section 6.4 (including run metric collection and baseline snapshotting)
3. Create the watchdog.sh script specified in Section 11.4
4. Create all agent prompt templates in system/prompts/ based on the role descriptions in Section 2 (including the Meta-Evaluator prompt from Section 10.6)
5. Create system/config.md with default values from Section 6.5
6. Initialize empty log files (including logs/meta_evaluator.jsonl)
7. Initialize system/termination.md with status: running
8. Initialize empty metrics files: metrics/run_history.jsonl, metrics/modification_log.jsonl, metrics/heuristics.jsonl
9. Create the run_meta_evaluator.sh script for manual Meta-Evaluator invocation (Section 10.2)
10. Create the start.sh script with the inter-run Meta-Evaluator phase (Section 10.2) and the Meta-Evaluator self-modification rollback check (Section 10.5)
11. Install the watchdog cron job
12. Start the atlas tmux session
13. Launch the monitor

Read the architecture document now and execute all 13 steps."
```

### 14.2 Subsequent Runs

When the system has been run before and has accumulated knowledge:

1. The user places a new `goal.md` in `~/atlas/`
2. The user runs `~/atlas/system/start.sh` (created during bootstrap)
3. The start script:
   - **Runs the Meta-Evaluator** (Section 10.2) to analyze the previous run and apply any system improvements. This happens BEFORE the new run starts.
   - **Checks for Meta-Evaluator self-modification rollback** (Section 10.5): if the last 2 runs showed composite score degradation and the Meta-Evaluator modified its own prompt, rolls back the self-modification.
   - Clears `tasks/`, `output/`, `reports/`, `signals/`, `directives/`
   - Preserves `knowledge/` (this is the persistent memory)
   - Preserves `metrics/` (this is the structured cross-run learning data — never cleared)
   - Preserves `system/prompts/` (potentially improved by Meta-Evaluator or self-improvement)
   - Preserves `system/config.md` (potentially optimized by Meta-Evaluator)
   - Preserves `system/archive/` (modification rollback history)
   - Resets `plan/` (new goal, new plan)
   - Resets `logs/` (new run, fresh logs — old logs archived to `logs/archive/`)
   - Resets `system/termination.md` to `status: running`
   - Generates a new `run_id` and writes it to `system/run_id`
   - **Writes a baseline snapshot** to `metrics/baselines/baseline_{run_id}.json` (Section 9.2)
   - Starts the tmux session and monitor

### 14.3 Prompt Template Structure

Each prompt template follows this pattern:

```markdown
# Role: [AGENT TYPE]

You are the [role name] agent in the ATLAS system.

## Your Responsibilities
[Specific to this tier — from Section 2]

## Your Cycle
1. Read [specific files]
2. Analyze [what to look for]
3. Decide [what decisions to make]
4. Write [specific output files]
5. Output CYCLE_COMPLETE when done

## File Paths
- You READ from: [list]
- You WRITE to: [list]
- You NEVER read: [list of files outside your scope]

## Output Format
[Specific format requirements for this agent's outputs]

## Escalation
[When and how to escalate — from Section 4.3]

## Cross-Run Context
[For Sovereign and Strategist: instructions to read metrics/cross_run_analysis/latest.md and metrics/heuristics.jsonl]
[For other tiers: not applicable]

## Self-Modification Protocol
[For Strategist: how to tag modifications with IDs and log them — from Section 8.3]
[For Meta-Evaluator: full modification protocol — from Section 10]
[For other tiers: not applicable]

## Important Rules
- Always persist your state to files before ending your cycle
- Log every action to your log file
- Include token estimates in your log entries
- Include the run_id (from ~/atlas/system/run_id) in every log entry
- If you detect a stall or issue you cannot resolve, escalate immediately
- Never exceed your scope — delegate or escalate instead
```

---

## 15. Operational Invariants and Edge Cases

### 15.1 Invariants (Things That Must Always Be True)

1. **Single writer per file**: No two agents ever write to the same file. The hierarchy strictly partitions write access. The Meta-Evaluator writes to system files ONLY between runs when no other agents are active.
2. **State is in files, not in agent context**: If an agent is killed and relaunched, it loses nothing because all state was already written.
3. **Every cycle reads fresh**: No agent carries state from a previous cycle in its context. Everything is re-read from files.
4. **The monitor is not a Claude agent**: It is a bash script. It cannot stall due to context issues. It is deterministic.
5. **Logs are append-only**: Log files are never modified, only appended to.
6. **Knowledge is cumulative**: The `knowledge/` directory is never cleared between runs.
7. **Metrics are cumulative**: The `metrics/` directory is never cleared. Run history, modification logs, and heuristics accumulate across the system's entire lifetime.
8. **Modifications are always tracked**: Every self-modification, whether from the Strategist, Sovereign, or Meta-Evaluator, gets a unique ID and is logged to `metrics/modification_log.jsonl`.
9. **The Meta-Evaluator does not run during execution**: It operates only between runs, preventing interference with the active agent hierarchy.
10. **Archive before modify**: Any file that is about to be modified by the self-improvement loop or Meta-Evaluator has its previous version archived first.

### 15.2 Edge Cases and Mitigations

**Edge case: Worker produces invalid output**
- The Conductor is responsible for validating Worker output. The Conductor's prompt includes instructions to check for completeness, correctness, and format compliance.
- If invalid, the Conductor creates a new task that references the bad output and asks a Worker to fix it.

**Edge case: Strategist creates an impossible plan**
- The adversarial self-review step catches most issues. For those it doesn't catch, the Conductors will report blocked tasks, and the Strategist will be forced to replan.
- If 3 consecutive plan versions all fail at the same point, the Strategist escalates to the Sovereign with a recommendation to modify the goal.
- The heuristic database helps prevent repeated planning mistakes — if this pattern occurred before, there should be a heuristic against it.

**Edge case: Token budget runs out mid-task**
- Workers don't track the global budget (they don't know about it). The monitor tracks total spend.
- When 80% of budget is consumed, the monitor writes a `signals/budget_warning` file.
- The Strategist reads this and switches to a "wrap up" plan: complete only the most critical remaining work.
- At 95%, the monitor triggers graceful shutdown.

**Edge case: Circular dependencies in the plan**
- The Strategist's prompt explicitly instructs it to check for circular dependencies during plan creation and review.
- If detected at runtime (two tasks both waiting on each other), the Conductor escalates immediately.

**Edge case: All workers stall simultaneously**
- The monitor detects this (all worker panes stalled). It kills all workers and notifies the Conductor(s) by writing stall files.
- If this happens twice in a row, the monitor escalates by writing `signals/replan` to force the Strategist to reconsider the approach.

**Edge case: The goal is vague or ambiguous**
- The Strategist's first action is to analyze the goal for clarity. If the goal is underspecified, the Strategist writes its interpretation and assumptions into the plan, and the Sovereign reviews and approves before execution begins.
- This is a special "planning review" phase that happens before any Workers are launched.

**Edge case: Output artifacts conflict**
- Each Worker writes to its own output directory (`output/{ws}/{task}/`). There are no shared output directories.
- If a final synthesis step needs to merge outputs, it is explicitly modeled as a task that takes the other tasks' output directories as input.

**Edge case: Monitor script has a bug**
- The watchdog cron job will restart it. But if the bug is persistent, the watchdog can't fix it.
- Mitigation: The monitor script is kept deliberately simple. It does NOT make complex decisions. It watches, launches, and logs. All intelligence is in the agents.
- The monitor's log (`logs/system.jsonl`) can be reviewed by a human or by the Meta-Evaluator to identify monitor bugs. The Meta-Evaluator can modify the monitor script between runs.

**Edge case: System needs more tiers or fewer tiers**
- The Strategist can propose structural changes (Section 8.4) within a run.
- The Meta-Evaluator can implement structural changes between runs (Section 10.1), with more authority and better evidence (cross-run data).
- For a simple goal: eliminate Conductors, have Workers report directly to Strategist.
- For a complex goal: add a sub-Conductor layer.

**Edge case: A knowledge base entry is wrong**
- Knowledge entries are tagged with confidence and source. If a Worker's findings contradict a knowledge entry, the Conductor flags this in its report. The Strategist evaluates and either updates the knowledge entry or notes the contradiction.

**Edge case: Meta-Evaluator makes a harmful modification**
- The modification is logged with full before/after state and archived.
- On the next run, if the relevant metrics degrade, the Meta-Evaluator detects this and rolls back the modification.
- If the Meta-Evaluator itself was the target of the harmful modification (self-modification), the `start.sh` script detects this by checking the composite score trend and rolls back automatically (Section 10.5).
- As a last resort, the operator can manually restore any file from `system/archive/`.

**Edge case: Heuristic database becomes stale or contradictory**
- The Meta-Evaluator prunes the heuristic database on every between-run analysis. Heuristics that have been contradicted more than supported are deprecated. Heuristics that haven't been applied in the last 10 runs are flagged for review.
- Goal type changes naturally shift which heuristics are consulted, preventing over-specialization.

**Edge case: First run has no cross-run data**
- The system handles this gracefully. When `metrics/run_history.jsonl` is empty, the Strategist skips the cross-run analysis step. The Meta-Evaluator skips its analysis phase (nothing to analyze). Default heuristics can be seeded by the operator if desired, or the system learns from scratch.

**Edge case: Meta-Evaluator timeout**
- The `start.sh` script enforces a timeout. If the Meta-Evaluator takes too long, it is killed and the run proceeds with the current system state. No partial modifications are applied (the Meta-Evaluator writes to temporary files first and only moves them into place atomically at the end of its cycle).

### 15.3 Performance Expectations

Based on the design:
- **Meta-Evaluator cycle**: ~5-15 minutes (runs once between runs, deep analysis of cross-run data)
- **Sovereign cycle**: ~30 seconds (reads 2-3 small files, writes 1-2 small files)
- **Strategist cycle**: ~60-120 seconds (reads plan + reports + heuristics, potentially revises plan)
- **Conductor cycle**: ~30-60 seconds (reads tasks, monitors workers, writes report)
- **Worker task**: 30 seconds to 10 minutes depending on complexity

At steady state with 4 workers, the system processes roughly 15-30 tasks per hour.

### 15.4 Cost Model

Approximate token usage per cycle:
- Meta-Evaluator: ~50,000-100,000 tokens (once between runs, amortized across the run)
- Sovereign: ~3,000 tokens (in + out)
- Strategist: ~15,000 tokens (increased from 12K due to heuristic database reading)
- Conductor: ~6,000 tokens
- Worker: ~8,000-30,000 tokens (highly variable)

At 4 workers, 1 conductor per workstream (3 workstreams), running for 1 hour:
- Meta-Evaluator: 1 cycle x 75K avg = 75K tokens (amortized)
- Sovereign: 12 cycles x 3K = 36K tokens
- Strategist: 30 cycles x 15K = 450K tokens
- Conductors: 3 x 60 cycles x 6K = 1,080K tokens
- Workers: ~25 tasks x 15K avg = 375K tokens

**Approximate total per hour: ~2.0M tokens** (including amortized Meta-Evaluator cost)

This is a rough estimate. The self-improvement loop and Meta-Evaluator should optimize this over time — indeed, reducing this cost while maintaining output quality is one of the Meta-Evaluator's primary objectives.

---

## Appendix A: Monitor Script Pseudocode

```bash
#!/bin/bash
# monitor.sh — The heartbeat of ATLAS
# This is the ONLY non-Claude-agent process in the system.

ATLAS_HOME="$HOME/atlas"
source "$ATLAS_HOME/system/config.sh"  # loads cycle times, limits, etc.

# Read or generate run_id
RUN_ID=$(cat "$ATLAS_HOME/system/run_id" 2>/dev/null || echo "run-$(date +%Y%m%d-%H%M%S)")
echo "$RUN_ID" > "$ATLAS_HOME/system/run_id"

# Ensure tmux session exists
tmux has-session -t atlas 2>/dev/null || tmux new-session -d -s atlas -n monitor

# Write baseline snapshot at run start
write_baseline() {
  local baseline_file="$ATLAS_HOME/metrics/baselines/baseline_${RUN_ID}.json"
  mkdir -p "$(dirname "$baseline_file")"
  cat > "$baseline_file" << BASELINE_EOF
{
  "run_id": "$RUN_ID",
  "ts": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "config_hash": "$(shasum -a 256 "$ATLAS_HOME/system/config.md" 2>/dev/null | cut -d' ' -f1)",
  "prompt_hashes": {
$(for f in "$ATLAS_HOME"/system/prompts/*.md; do
    echo "    \"$(basename "$f" .md)\": \"$(shasum -a 256 "$f" 2>/dev/null | cut -d' ' -f1)\","
  done | sed '$ s/,$//')
  },
  "active_modifications": $(cat "$ATLAS_HOME/metrics/modification_log.jsonl" 2>/dev/null | grep '"status":"active"' | jq -s '[.[].mod_id]' 2>/dev/null || echo '[]')
}
BASELINE_EOF
}

log_event() {
  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"agent\":\"monitor\",\"run_id\":\"$RUN_ID\",\"event\":\"$1\",\"details\":\"$2\"}" \
    >> "$ATLAS_HOME/logs/system.jsonl"
}

# Write structured run metrics at end of run
write_run_metrics() {
  # Aggregate metrics from all log files for this run
  # Write to metrics/run_history.jsonl
  # This collects: token totals, task counts, plan versions, escalation counts, etc.
  local metrics_file="$ATLAS_HOME/metrics/run_history.jsonl"
  # ... aggregation logic here (counts from logs, durations, etc.) ...
  log_event "run_metrics_written" "Structured metrics for $RUN_ID written to $metrics_file"
}

check_signals() {
  if [ -f "$ATLAS_HOME/signals/shutdown" ]; then
    log_event "shutdown" "Shutdown signal received"
    graceful_shutdown
    exit 0
  fi
  if [ -f "$ATLAS_HOME/signals/pause" ]; then
    log_event "pause" "Pause signal received"
    return 1  # skip this cycle
  fi
  if [ -f "$ATLAS_HOME/signals/replan" ]; then
    log_event "replan" "Replan signal received"
    rm "$ATLAS_HOME/signals/replan"
    launch_strategist_cycle "REPLAN_FORCED"
  fi
  return 0
}

launch_agent_cycle() {
  local agent_type=$1
  local window_name=$2
  local prompt_file="$ATLAS_HOME/system/prompts/${agent_type}.md"
  local context=$(build_context "$agent_type")  # assembles relevant files

  # Check if window exists and is idle
  if tmux list-windows -t atlas -F '#{window_name}' | grep -q "^${window_name}$"; then
    # Window exists — check if previous cycle is done
    local pane_pid=$(tmux list-panes -t "atlas:${window_name}" -F '#{pane_pid}')
    if [ -n "$pane_pid" ] && ps -p "$pane_pid" > /dev/null 2>&1; then
      # Still running — check for stall
      check_stall "$agent_type" "$window_name" "$pane_pid"
      return
    fi
  else
    tmux new-window -t atlas -n "$window_name"
  fi

  # Launch the cycle
  tmux send-keys -t "atlas:${window_name}" \
    "claude -p \"$(cat "$prompt_file")

${context}

Execute your cycle now.\"" Enter

  log_event "cycle_launch" "$agent_type in $window_name"
}

# Track last launch times
declare -A last_launch

main_loop() {
  log_event "monitor_start" "Monitor starting for $RUN_ID"
  write_baseline

  while true; do
    check_signals || { sleep 10; continue; }

    local now=$(date +%s)

    # Sovereign cycle
    local sovereign_interval=$((SOVEREIGN_CYCLE_MINUTES * 60))
    if (( now - ${last_launch[sovereign]:-0} >= sovereign_interval )); then
      launch_agent_cycle "sovereign" "sovereign"
      last_launch[sovereign]=$now
    fi

    # Strategist cycle
    local strategist_interval=$((STRATEGIST_CYCLE_MINUTES * 60))
    if (( now - ${last_launch[strategist]:-0} >= strategist_interval )); then
      launch_agent_cycle "strategist" "strategist"
      last_launch[strategist]=$now
    fi

    # Conductor cycles — one per active workstream
    for ws_dir in "$ATLAS_HOME"/plan/workstreams/*/; do
      if [ -d "$ws_dir" ]; then
        local ws_id=$(basename "$ws_dir")
        local conductor_interval=$((CONDUCTOR_CYCLE_MINUTES * 60))
        if (( now - ${last_launch[conductor_$ws_id]:-0} >= conductor_interval )); then
          launch_agent_cycle "conductor" "conductor-$ws_id"
          last_launch[conductor_$ws_id]=$now
        fi
      fi
    done

    # Worker management — handled by conductors creating task files
    manage_workers

    # Update dashboard
    update_dashboard

    # Aggregate token usage
    aggregate_tokens

    sleep 5  # Main loop tick
  done
}

manage_workers() {
  # Find tasks that are assigned but not started (no _done.md, no _stalled.md, no active worker)
  local active_workers=$(tmux list-panes -t "atlas:workers" 2>/dev/null | wc -l)
  if (( active_workers >= MAX_CONCURRENT_WORKERS )); then
    return
  fi

  for task_file in "$ATLAS_HOME"/tasks/*/*; do
    [ -f "$task_file" ] || continue
    local base=$(basename "$task_file" .md)
    [[ "$base" == *_done ]] && continue
    [[ "$base" == *_blocked ]] && continue
    [[ "$base" == *_stalled ]] && continue
    [[ "$base" == *_active ]] && continue

    local ws_id=$(basename "$(dirname "$task_file")")
    local task_id="$base"

    # Check if already done or active
    [ -f "${task_file%.md}_done.md" ] && continue
    [ -f "${task_file%.md}_active.md" ] && continue

    # Mark as active and launch
    touch "${task_file%.md}_active.md"
    launch_worker "$ws_id" "$task_id"

    active_workers=$((active_workers + 1))
    if (( active_workers >= MAX_CONCURRENT_WORKERS )); then
      return
    fi
  done
}

graceful_shutdown() {
  log_event "graceful_shutdown" "Beginning graceful shutdown"
  # Signal all agents to wrap up
  # Wait up to 2 minutes for active workers
  # Generate final summary
  # Write structured run metrics
  write_run_metrics
  # Exit
}

main_loop
```

---

## Appendix B: Critical Design Decisions and Rationale

### Why file-based communication instead of pipes/sockets?

1. **Persistence**: If any agent crashes, the state survives.
2. **Debuggability**: A human can read every file and understand system state.
3. **Simplicity**: No message broker, no serialization protocol, no connection management.
4. **Recovery**: A relaunched agent can read files to reconstruct state.

### Why relaunch agents each cycle instead of persistent loops?

Context window degradation. A Claude agent that has been running for 30 minutes with accumulated conversation history performs measurably worse than a freshly launched agent with the same information provided as initial context. The relaunch-per-cycle pattern guarantees every cycle gets peak performance.

### Why a bash monitor instead of a Claude agent?

The monitor must be reliable and deterministic. A Claude agent could hallucinate, stall, or make poor decisions about system management. The monitor's job is simple enough for bash: watch timers, check files, launch processes. By keeping it in bash, we eliminate one potential failure mode.

### Why separate Conductor and Worker tiers?

Workers need minimal context to maximize execution quality. If Workers also had to monitor other workers and manage task dependencies, their context would be polluted. Conductors provide the management layer while Workers stay focused.

### Why Sovereign approval for prompt changes?

Self-modification is the most dangerous capability. A bad prompt change could degrade all agents of that type. Requiring Sovereign approval adds a review step. The Sovereign's lean context means it can evaluate the proposal without being biased by the details that led to it.

### Why a Meta-Evaluator above the Sovereign?

The Sovereign optimizes execution within a run, but it cannot optimize itself — it has no mechanism to evaluate whether its own prompt, cycle timing, or decision criteria are optimal. The Meta-Evaluator fills this gap by operating at a higher level of abstraction, treating the entire system (including the Sovereign) as code to be improved. Without it, ATLAS can improve task execution but cannot improve its own management structure.

### Why structured metrics instead of just prose retrospectives?

Prose retrospectives ("what worked well, what didn't") are useful for human readers but nearly useless for systematic optimization. An agent reading "task estimation was sometimes off" cannot determine the magnitude, frequency, or trend of the problem. Structured metrics (task_completion_rate: 0.857, plan_revisions: 3, tokens_per_task_complexity_unit: 18500) enable quantitative comparison across runs, trend detection, and evidence-based decision-making. The system maintains both formats: prose for human review, structured data for machine analysis.

### Why A/B-style modification tracking?

Without tracking the impact of each modification, the system cannot distinguish beneficial changes from harmful ones. A prompt tweak might feel like an improvement but actually degrade performance in ways that are invisible without measurement. By tagging each modification with a hypothesis and measuring the relevant metric in subsequent runs, the system builds genuine evidence about what works. This prevents the accumulation of well-intentioned but untested changes.

### Why a heuristic database with evidence ranking?

A flat list of "lessons learned" grows without bound and gives equal weight to a fluke observation from one run and a pattern confirmed across ten runs. By ranking heuristics by evidence strength, the Strategist can prioritize reliable knowledge over speculative insights. By pruning deprecated heuristics, the database stays relevant. This is the difference between "we tried X once and it seemed to help" and "X has been validated across 7 runs with a measured 30% improvement in plan stability."

---

## Appendix C: Example Agent Prompts

### Sovereign Prompt Template

```markdown
# Role: SOVEREIGN

You are the Sovereign agent in the ATLAS system. You own the goal and decide when the system is done.

## Your Cycle

1. Read the goal from the GOAL section below
2. Read the current system status from the STATUS section below
3. Read any directives you have previously issued
4. Read the termination state
5. Read the Meta-Evaluator's latest recommendations (if available)
6. Evaluate: Are we making progress toward the goal?
7. Evaluate: Have any success criteria been met?
8. Evaluate: Are we hitting diminishing returns?
9. Evaluate: Should any course corrections be made?
10. If course correction needed: Write directives to ~/atlas/directives/sovereign.md
11. Update ~/atlas/system/termination.md with your assessment
12. Update ~/atlas/plan/status.md if you have observations
13. Log your cycle to ~/atlas/logs/sovereign.jsonl (include run_id from ~/atlas/system/run_id)
14. Output CYCLE_COMPLETE

## Decision Framework

- If all success criteria are met -> set termination status to "completed"
- If budget > 90% exhausted -> set termination status to "budget_exhausted" and trigger graceful shutdown
- If time > 90% exhausted -> set termination status to "timeout" and trigger graceful shutdown
- If no meaningful progress in last 3 evaluations -> consider termination for "diminishing_returns"
- If the Strategist has flagged something for your review -> evaluate and provide direction

## Rules

- You do NOT read task files, worker output, or conductor reports
- You ONLY read plan/status.md, directives/sovereign.md, system/termination.md, and the Meta-Evaluator summary
- Keep your context minimal
- Be decisive: if the system is stuck, either provide clear direction or terminate
```

### Worker Prompt Template

```markdown
# Role: WORKER

You are a Worker agent in the ATLAS system. You execute one specific task.

## Your Task

Read the TASK section below carefully. It contains:
- What you need to accomplish
- What inputs are available to you
- What outputs you must produce
- Success criteria for this specific task

## Execution Rules

1. Focus exclusively on your assigned task
2. Write all output files to the specified output directory
3. If you encounter a blocker you cannot resolve, write a file at:
   ~/atlas/tasks/{workstream_id}/{task_id}_blocked.md
   Describe the blocker clearly.
4. When complete, write your summary to:
   ~/atlas/tasks/{workstream_id}/{task_id}_done.md
   Include: what you did, what you produced, key findings, time taken.
5. Log your work to ~/atlas/logs/workers/{task_id}.jsonl (include run_id from ~/atlas/system/run_id)

## Output Quality

- Be thorough but concise
- Produce artifacts that are immediately usable by other agents
- If your task involves research, cite sources
- If your task involves code, include tests or validation
- If your task involves analysis, include methodology and confidence levels

## What You Do NOT Do

- Do not read other workers' tasks or output
- Do not modify the plan
- Do not communicate with other agents except through your output files
- Do not exceed your task scope — if you discover the task is larger than specified, note this in your completion summary and let the Conductor decide

## When Done

Output CYCLE_COMPLETE
```

---

## Appendix D: Quick Reference — System Commands

```bash
# Start the system (first time)
claude -p "Bootstrap ATLAS per ~/atlas/NEXUS_ARCHITECTURE.md"

# Start the system (subsequent runs — includes Meta-Evaluator analysis)
~/atlas/system/start.sh

# Run Meta-Evaluator manually (outside of start.sh)
~/atlas/system/run_meta_evaluator.sh

# View the dashboard
cat ~/atlas/logs/dashboard.md

# View cross-run performance trends
cat ~/atlas/metrics/cross_run_analysis/latest.md

# View the heuristic database
cat ~/atlas/metrics/heuristics.jsonl

# View the modification changelog
cat ~/atlas/metrics/cross_run_analysis/changelog.md

# View the run history
cat ~/atlas/metrics/run_history.jsonl

# Pause the system
touch ~/atlas/signals/pause

# Resume the system
rm ~/atlas/signals/pause

# Gracefully stop the system
touch ~/atlas/signals/shutdown

# Force stop (emergency)
tmux kill-session -t atlas

# Force replan
touch ~/atlas/signals/replan

# Force Meta-Evaluator before next run
touch ~/atlas/signals/meta_eval

# View system log
tail -f ~/atlas/logs/system.jsonl

# View token usage
tail -f ~/atlas/logs/tokens.jsonl

# View Meta-Evaluator log
cat ~/atlas/logs/meta_evaluator.jsonl

# Attach to the system
tmux attach -t atlas

# Roll back a specific modification
# (restore the archived version from system/archive/)
cp ~/atlas/system/archive/{file}_{timestamp}.md ~/atlas/system/{file}.md
```

---

## Appendix E: File Size and Rotation Policy

To prevent file system bloat:

- **JSONL logs**: Rotated when they exceed 10MB. Old logs moved to `logs/archive/` with timestamp suffix.
- **Reports**: Only the last 20 reports per workstream are kept. Older ones archived.
- **Knowledge base**: No automatic rotation. Reviewed during self-improvement cycles for stale or contradicted entries.
- **Output artifacts**: Not rotated. These are the deliverables.
- **Dashboard**: Overwritten each update (not appended).
- **Metrics files**: `run_history.jsonl`, `modification_log.jsonl`, and `heuristics.jsonl` are never rotated — they are the system's long-term memory. If they grow extremely large (100MB+), the Meta-Evaluator can compact them by summarizing old entries.
- **Cross-run analysis reports**: Kept indefinitely. Each is ~5-10KB so storage is not a concern.
- **Baseline snapshots**: Kept indefinitely. Each is <1KB.

The monitor handles log rotation as part of its main loop (checked every 60 seconds).

---

## Appendix F: Handling the "Cold Start" Knowledge Problem

On the very first run, the `knowledge/` and `metrics/` directories are empty. The system has no prior experience. This affects:

1. **Planning quality**: The Strategist has no historical data or heuristics to inform estimates. Mitigation: The Strategist's prompt includes instructions to be conservative in initial estimates and to flag uncertainty explicitly.

2. **Prompt quality**: The default prompt templates are untested. Mitigation: The templates are designed to be functional but generic. The self-improvement loop will refine them after observing actual performance. The Meta-Evaluator will have data to work with after the first run completes.

3. **Cycle timing**: Default cycle intervals may not be optimal. Mitigation: The Sovereign observes the first few cycles and adjusts timing if agents are cycling too fast (wasting tokens on unchanged state) or too slow (creating bottlenecks).

4. **Cross-run learning**: No heuristics, no modification history, no performance baselines. Mitigation: The system handles empty metrics files gracefully (skipping cross-run analysis steps). The first run establishes baselines. The second run enables comparisons. By the third run, the Meta-Evaluator has enough data to begin making evidence-based modifications.

5. **Meta-Evaluator cold start**: On the second run (first time the Meta-Evaluator has data), it has only one run to analyze. Mitigation: The Meta-Evaluator's modification threshold requires 2+ runs of evidence, so it will observe but not modify on the second run. By the third run, it can begin applying changes.

After 3-5 runs, the knowledge base, heuristic database, and modification history should contain enough data to significantly improve planning, execution quality, and system structure. After 10+ runs, the system should be substantially self-optimized for its typical goal types.

---

*End of ATLAS Architecture Document v2.0*
