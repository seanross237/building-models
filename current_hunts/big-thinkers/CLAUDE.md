# Big Thinkers

Autonomous agent orchestration systems for tackling complex research problems. Each system has a different architecture, but they share infrastructure.

## Shared Resources

- **Idea pipeline:** `idea-exploration/` — ideas spotted during any mission go here, regardless of which system found them
- **Promising findings:** `promising-findings.md` — validated novel claims from completed missions across all systems
- **Available tools:** `available-tools.md` — shared tooling reference

## The Systems

| System | Architecture | Status |
|---|---|---|
| **Atlas** | Missionary → Strategizer → Explorer | Most mature, 15+ missions run |
| **Philosopher Atlas** | Wide-funnel planning loop (planner → selector picks 3 → 3× attacker → 3× judge → final decider) | Independent library, own agents |
| **Forge** | Conductor → Planner → Workers (domain-agnostic) | Engineering + analysis focus |
| **Colossus** | Self-building controller → Workers | Autonomous self-improvement |
| **Nexus** | Autonomous orchestration | Architecture doc + NS goal |

## Spotting Ideas (All Systems)

When any agent encounters a finding worth investigating outside the current mission's scope, hand it off to a background sub-agent. Don't do the validation work yourself.

The sub-agent's job:
1. Read the idea validator guide at `idea-exploration/agents/idea-validator/system-prompt.md`
2. Score the idea using the validator's rubric
3. Create a detailed idea file at `idea-exploration/ideas/atlas-idea-NNN.md` (next available number)
4. Add a row to the index at `idea-exploration/ATLAS-IDEAS.md`

## Model Assignment

- **Opus:** All important planning, difficult computations, and complex reasoning tasks.
- **Sonnet:** Straightforward operations (file writes, simple searches, routine edits).

## After Any Mission Completes

Review novel claims from final reports. Any claims that survived adversarial review and passed validation should be added to `promising-findings.md`, following the format already in that file.
