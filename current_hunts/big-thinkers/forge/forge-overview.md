# Forge — System Overview

Forge is a general-purpose autonomous agent system. Given any goal, it designs and executes an agent hierarchy to accomplish it. It runs on Claude Code + tmux, communicates through files on disk, and survives context window resets via stop hooks.

## How It Works

### The Core Loop

```
Human provides a goal
        ↓
  ┌─────────────┐
  │  Architect   │  One-shot bootstrap agent. Analyzes the goal, designs
  │  (exits)     │  the hierarchy, sets up infrastructure, launches the
  └──────┬───────┘  top-level agent, then exits.
         ↓
  ┌─────────────┐
  │  Planner     │  Persistent loop agent. Decomposes the goal into tasks,
  │  (looping)   │  spawns Workers, reads their results, adapts, repeats.
  └──────┬───────┘  Survives context resets via stop hook.
         ↓
  ┌─────────────┐
  │  Workers     │  Short-lived execution agents. Each gets one task,
  │  (one-shot)  │  does the work, writes a report, exits.
  └─────────────┘
```

For complex goals, a **Conductor** sits above the Planner to manage multi-phase strategy.

### What Makes It Work

1. **Files are the system bus.** Agents don't pass information verbally — they write to disk and read from disk. STRATEGY.md, state.json, HISTORY.md, task reports. Everything persists.

2. **Stop hooks keep the loop alive.** When the Planner's context window fills up, Claude Code fires a Stop event. The stop hook intercepts it, injects a meta-prompt ("you just lost context — read state.json and HISTORY.md to recover"), and the Planner resumes from where it left off.

3. **Workers are disposable.** A Worker gets a task spec, runs in its own tmux session with a clean context window, writes results, and exits. The Planner never shares context with Workers — it reads their reports.

4. **The Architect decides the shape.** It classifies the goal (complexity, uncertainty, decomposability) and picks depth 2, 3, or 4. Too shallow wastes the goal's potential; too deep wastes tokens on coordination. The Critic sub-agent reviews the architecture before anything launches.

## Hierarchy Depths

| Depth | Shape | When |
|---|---|---|
| **2** | Planner → Workers | Single workstream, clear path, well-defined branching |
| **3** | Conductor → Planner → Workers | Multi-phase, needs strategic pivoting between phases |
| **4** | Conductor → multiple Planners → Workers | Parallel independent workstreams |

## Agent Types

| Agent | Lifetime | Job |
|---|---|---|
| **Architect** | One-shot (bootstrap) | Analyze goal, design hierarchy, create infrastructure, launch |
| **Conductor** | Looping (depth 3-4 only) | Evaluate strategy results, decide continue/pivot/done, write new strategies |
| **Planner** | Looping | Decompose strategy into tasks, spawn workers, synthesize results, adapt |
| **Worker** | One-shot | Execute a single task, write report |
| **Librarian** | Sub-agent (foreground) | Retrieve relevant knowledge from library before each task |
| **Curator** | Sub-agent (fire-and-forget) | Organize new findings into the library |

### Worker Variants

Workers come in specialist flavors. The Planner picks the right one for each task:

- **Standard** — research, writing, analysis, synthesis
- **Code** — software engineering, DNS solvers, simulations
- **Math** — computation, formal verification, proof attempts
- **Research** — literature surveys, paper analysis
- **Analysis** — data analysis, measurement, comparison
- **Adversarial** — stress-test claims, find circular reasoning, break proofs
- **Creative** — writing, design, content generation

## File Layout

```
forge/
  system/                     # The system itself (prompts, templates, orchestration)
    bootstrap/                #   Architect + Goal Analyzer prompts
    agents/                   #   All agent system prompts
      conductor/              #     + stop hook template
      planner/                #     + stop hook template + state templates
      worker/                 #     Standard worker
      specialist-workers/     #     Code, research, analysis, creative, math, adversarial
      library/                #     Librarian, Curator, factual + meta knowledge
    orchestration/            #   Setup guides, stop hook reference
    measurement/              #   Log schemas, analyzer, evolver prompts
  missions/                   # One directory per mission
    m001-vasseur-pressure/    #   Currently running
      GOAL.md                 #     Verbatim goal
      GOAL-ANALYSIS.md        #     Goal classification
      ARCHITECTURE.md         #     Hierarchy design
      STRATEGY.md             #     Top-level strategy
      plan/                   #     Planner's working directory
        state.json            #       Machine-readable state (iteration, tasks, done)
        LOOP-STATE.md         #       Stop hook control (active, iteration, transcript)
        HISTORY.md            #       Accumulated task summaries
        REASONING.md          #       Decision log
        planner-stop-hook.sh  #       The stop hook script
        tasks/                #       One subdirectory per task
          task-001/           #         SPEC.md, RESULT.md, code/, etc.
        reports/              #       Task report summaries
      logs/                   #     Restart logs, debug logs
      token-usage.sh          #     Token counting script
  improvement/                # Post-mission analysis and self-modification
  system-design.md            # The full detailed system design document
```

## How a Mission Runs

### 1. Setup (Architect or manual)
- Classify the goal → GOAL-ANALYSIS.md
- Design hierarchy → ARCHITECTURE.md
- Write strategy → STRATEGY.md
- Create directory structure, state files, stop hook
- Register stop hook in `~/.claude/settings.json`

### 2. Execution (Planner loop)
The Planner runs in a tmux session. Each iteration:

1. Read state.json, STRATEGY.md, HISTORY.md
2. Consult Librarian for relevant prior knowledge
3. Design the next task (write SPEC.md)
4. Spawn a Worker in a new tmux session
5. Wait for the Worker to finish (poll for RESULT-SUMMARY.md)
6. Read the result, update HISTORY.md and state.json
7. Evaluate: continue, pivot, or done?
8. If done → write FINAL-REPORT.md

When context fills up, the stop hook fires and restarts the loop at step 1.

### 3. Monitoring (human or this session)
- `tmux capture-pane -t <session> -p | tail -10` — see what any agent is doing
- `./token-usage.sh` — cumulative token counts from JSONL transcripts
- `cat plan/state.json` — machine-readable mission state
- `touch plan/PAUSE_HOOK` — emergency stop (stop hook lets session die)

### 4. Post-mission (Analyzer + Evolver)
- **Analyzer** reads logs and FINAL-REPORT, writes analysis to `improvement/`
- **Evolver** proposes and applies system improvements based on the analysis
- Findings go to `findings.md`

## The Stop Hook

The stop hook is what makes the loop autonomous. It's a bash script registered in `~/.claude/settings.json` that runs whenever Claude Code's Stop event fires.

```
Claude context fills up → Stop event fires → stop hook runs
                                                    ↓
                                              Check PAUSE_HOOK? → let die
                                              Check state.json done? → let die
                                              Check session ownership? → not mine, ignore
                                              Check max iterations? → let die
                                                    ↓
                                              Increment iteration counter
                                              Output: {"decision": "block", "reason": "<meta-prompt>"}
                                                    ↓
                                              Claude restarts with meta-prompt
                                              → reads state files → resumes work
```

Session ownership: the hook binds to a specific JSONL transcript path on first fire, so it only catches its own session — not other Claude instances running on the machine.

## The Library

Knowledge accumulates across missions in two categories:

- **Factual** (`library/factual/`) — domain knowledge, findings, verified results
- **Meta** (`library/meta/`) — operational lessons about the system itself
  - `goal-design/` — how to write effective task specs
  - `methodology/` — what approaches work for what problems
  - `system-behavior/` — how agents actually behave at runtime
  - `conductor/` — lessons about strategy management
  - `architecture/` — lessons about hierarchy depth decisions

The Librarian retrieves relevant entries before each task. The Curator processes new findings after tasks complete. The Architect reads meta lessons before designing new missions.

## Self-Improvement

After a mission completes:
1. **Analyzer** reviews logs (token usage, timing, restarts, task efficacy) and writes an analysis report
2. **Evolver** reads the analysis and proposes modifications to agent prompts, templates, or orchestration
3. All modifications are logged in `improvement/modifications-log.md` with reasoning
4. Prompt versions are saved in `improvement/prompt-versions/`

This is deliberate — changes are based on patterns across instances, not single failures.

## Key Design Constraints

- **Everything isolated to forge/.** No writing outside the forge directory except `~/.claude/settings.json` (unavoidable for stop hooks, protected by session filtering).
- **Agents wake up with minimal context.** System prompts are loaded via `--system-prompt-file`. Mission context comes from reading files on disk, not from conversation history.
- **Workers never see the Planner's context.** They get a SPEC.md and that's it. This keeps their context windows clean.
- **The Planner never sees raw Worker output.** It reads RESULT-SUMMARY.md — a condensed version. This prevents context bloat.
