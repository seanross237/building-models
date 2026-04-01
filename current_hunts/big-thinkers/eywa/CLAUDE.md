# Eywa

## Rules

- Keep responses relatively short. I'll ask to expand when necessary.
- If you change how orchestration works (statuses, transitions, spawning, polling, etc.), update `eywa-overview.md` to match.
- If you change agent prompts or guidance docs, update `eywa-overview.md` if the change affects the documented architecture.
- `&&` in design notes marks an open question to A/B test later.

## Key Paths

```
eywa-overview.md             — architecture doc (source of truth)
agent-prompts-and-guides/architect/system-prompt.md — core architect agent
agent-prompts-and-guides/architect/execute-vs-plan.md — guidance: when to split vs do
agent-prompts-and-guides/architect/plan-design.md  — guidance: plan format + patterns
agent-prompts-and-guides/architect/escalation.md   — guidance: continue/replan/escalate
agent-prompts-and-guides/plan-reviewer/system-prompt.md — plan reviewer
agent-prompts-and-guides/plan-decider/system-prompt.md  — plan decider
agent-prompts-and-guides/library-retriever/system-prompt.md — knowledge retrieval
orchestrator/orchestrator.sh — the bash state machine
library/                     — persistent knowledge (factual + meta)
missions/                    — mission runs
```

## Model Assignment

- **Opus:** Evaluation, synthesis, reviewer, decider (critical decisions)
- **Sonnet:** Planner agents, retrieval agents
- **Haiku:** Executor agents (leaf-level work)

## Mission Structure

```
missions/my-mission/
├── mission-goal.md                          ← the goal (you create this)
├── orchestrator.jsonl                       ← event log (orchestrator creates)
└── tree/
    └── root/                                ← root node (orchestrator creates)
        ├── input/
        │   ├── goal.md                      ← copied from mission-goal.md (root only)
        │   ├── parent-instructions-and-relevant-information.md       ← goal + context from parent (child nodes)
        │   ├── instructions-{mode}.md        ← orchestrator-generated (executor/planner/evaluation/synthesis)
        │   └── retrieved_relevant_knowledge_from_library.md
        ├── output/
        │   ├── plan.md                      ← if node planned
        │   ├── final-output.md              ← completion signal
        │   └── state.md                     ← brain dump
        ├── for-orchestrator/
        │   ├── this-nodes-current-status    ← single word status
        │   ├── agent-mode                   ← "executor" or "planner"
        │   └── eval-decision                ← single word signal
        └── children/
            └── step-01-name/                ← same structure recursively
```

## How to Launch

```bash
bash orchestrator/orchestrator.sh missions/my-mission
```

## How to Monitor

```bash
tail -f missions/my-mission/orchestrator.jsonl
```

## How to Stop

Kill the orchestrator process (Ctrl-C or kill PID). Tmux sessions for active agents will persist but are harmless — they can be cleaned up with `tmux kill-server` or individually.

## Open && Questions

1. **Node context scope:** How much tree context does a node get? (its goal only vs. overall goal + position in tree)
2. **C × I threshold calibration:** Is 25 the right threshold? Should it vary by depth? &&
3. **Persistent vs. ephemeral agents:** Persistent agents that hold context vs. ephemeral spawn-per-job with file-based state (starting with ephemeral)
4. **Knowledge retrieval:** Who decides what knowledge a node gets — parent curates, node pulls, or a retrieval layer in between?
5. **Plan review tier thresholds:** Where to draw the lines between low (no review), medium (single reviewer), and high (5 plans + critics + judges)
6. **Synthesis: parent vs. separate node?** Should the planner that created the steps also synthesize the results (in synthesis mode), or should plans include a dedicated consolidation step that receives prior outputs? Parent synthesis is simpler and has full context of why it decomposed. Separate node allows the synthesis task itself to be scored/decomposed. &&
