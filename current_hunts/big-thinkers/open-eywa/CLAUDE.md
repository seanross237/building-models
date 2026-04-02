# Open-Eywa

## Rules

- Keep responses relatively short unless asked to expand.
- For Open-Eywa architectural values, trust boundary, and change discipline, follow `BUILDING-PRINCIPLES.md`.
- Strongly prefer lower complexity over cleverness.
- Strongly prefer small compartmentalized modules over growing large files.
- Strongly prefer changes that keep future iteration, testing, and A/B comparison easy.
- `OPEN-EYWA-GOAL-AND-OVERVIEW.md` should stay high-level and should be updated when high-level behavior changes.
- `OPEN-EYWA-IMPLEMENTATION-DETAILS.md` should be updated when the current implementation shape changes.
- `BUILDING-PRINCIPLES.md` should be updated when the architectural philosophy or design principles change.
- If you create an Open-Eywa presentation, follow `/Users/seanross/kingdom_of_god/home-base/presentations/guide_presentations.md` and put it under `/Users/seanross/kingdom_of_god/home-base/presentations/`.
- If you change guidance in `CLAUDE.md` and that same guidance should also apply to agent-facing instructions, update `AGENTS.md` too.
- Keep the top level human-readable. Hide implementation detail under `system/`.
- Do not edit the existing `eywa` folder from inside Open-Eywa work.

## Key Paths

```text
OPEN-EYWA-GOAL-AND-OVERVIEW.md                - goal + high-level architecture doc
OPEN-EYWA-IMPLEMENTATION-DETAILS.md           - current implementation details
BUILDING-PRINCIPLES.md                        - architectural values and builder philosophy
april-first-planning/canonical-node-contract-spec.md
stuff-for-agents/planning/planner/system-prompt.md
stuff-for-agents/planning/planner/plan-design.md
stuff-for-agents/planning/planner/execute-vs-plan.md
stuff-for-agents/planning/plan-reviewer/system-prompt.md
stuff-for-agents/planning/plan-decider/system-prompt.md
stuff-for-agents/planning/mid-plan-evaluator/system-prompt.md
stuff-for-agents/worker/system-prompt.md
stuff-for-agents/synthesizer/system-prompt.md
stuff-for-agents/librarian/system-prompt.md
stuff-for-agents/library/
missions/
validation-suite/
viz/
system/
```

## Runtime Assumptions

- Open-Eywa uses OpenRouter Chat Completions.
- Open-Eywa owns the tool loop and local execution.
- Agents are ephemeral and reconstruct from files.
- Worker nodes may use heavy local math tooling.

## Launch

```bash
python3 system/scripts/run_mission.py missions/my-mission
```

## Monitor

```bash
tail -f missions/my-mission/orchestrator.jsonl
tail -f missions/my-mission/usage.jsonl
```
