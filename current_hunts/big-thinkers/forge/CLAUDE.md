# Forge

Forge is a general-purpose autonomous agent system for tackling complex goals through structured planning, delegation, and iterative refinement. Unlike Atlas (which is specialized for research exploration), Forge is domain-agnostic — it works on engineering tasks, analysis, code generation, or any goal that benefits from decomposition into tasks.

## Architecture

- **System design:** `system/orchestration/LOOP-STOP-HOOK-GUIDE.md` (how loops work), `system/orchestration/SETUP-GUIDE.md` (how to launch)
- **Agent prompts:** `system/agents/` — Conductor, Planner, Workers, Library
- **Missions:** `missions/` — each mission gets its own directory with strategies, tasks, and logs
- **Library:** `system/agents/library/` — accumulated knowledge (factual findings + meta-learnings about methodology)
- **Improvement:** `improvement/` — modifications log, analysis reports, prompt versions

## How to Launch a Mission

Give the Architect (you, reading this) a goal. The workflow:

1. Write a `MISSION.md` describing the goal, constraints, and success criteria
2. Follow `system/orchestration/SETUP-GUIDE.md` to create the mission directory, install templates, and register the stop hook
3. Launch a Planner in a tmux session pointed at the strategy directory
4. The stop hook keeps the Planner alive across context resets
5. The Planner decomposes the goal into tasks and delegates to Workers
6. Workers execute tasks and write RESULT-SUMMARY.md files
7. The Planner reviews results, updates state, and plans next steps
8. When the strategy is complete, the Planner writes FINAL-REPORT.md

## Key Paths

| Path | Purpose |
|---|---|
| `system/orchestration/SETUP-GUIDE.md` | Step-by-step mission setup |
| `system/orchestration/LOOP-STOP-HOOK-GUIDE.md` | Stop hook mechanics reference |
| `system/agents/planner/` | Planner prompt and templates |
| `system/agents/conductor/` | Conductor prompt and templates |
| `system/agents/worker/` | Worker prompt |
| `system/measurement/log-schema.md` | JSONL log format definitions |
| `missions/` | Active and completed missions |
| `improvement/modifications-log.md` | Record of system changes |

## Model Assignment

- **Opus:** All important planning, difficult computations, and complex reasoning tasks.
- **Sonnet:** Straightforward operations (file writes, simple searches, routine edits).

## Spotting Ideas

When any agent encounters a finding worth investigating outside the current mission's scope, hand it off to a background sub-agent. Don't do the validation work yourself.

The sub-agent's job:
1. Read the idea validator guide at `../idea-exploration/agents/idea-validator/system-prompt.md`
2. Score the idea using the validator's rubric
3. Create a detailed idea file at `../idea-exploration/ideas/atlas-idea-NNN.md` (next available number)
4. Add a row to the index at `../idea-exploration/ATLAS-IDEAS.md`

## After a Mission Completes

When a mission finishes (Planner writes FINAL-REPORT.md, or Conductor declares MISSION-COMPLETE.md):

1. **Run the Analyzer** — review logs in `missions/<id>/logs/`, read the FINAL-REPORT, and write an analysis report to `improvement/analysis-reports/`
2. **Run the Evolver** — based on the analysis, propose and apply improvements to agent prompts, templates, or orchestration. Log changes in `improvement/modifications-log.md`
3. **Extract findings** — any significant results should be added to `findings.md` in the forge root
