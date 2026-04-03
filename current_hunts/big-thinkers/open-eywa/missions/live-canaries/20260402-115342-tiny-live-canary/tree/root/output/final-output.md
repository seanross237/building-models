# Operator Note: Open-Eywa

## What Open-Eywa Is

Open-Eywa is a node-first agent orchestration system built to be visible, testable, and improvable over time. It is not a hidden agent cloud or a fragile prompt bundle. It is an offline-first system where code owns protocol and correctness, and models contribute bounded intelligence inside that hard structure.

The system drives multi-agent work through a tree of nodes. Each node holds a task, runs one or more agent roles (planner, worker, evaluator, synthesizer), records every event and artifact, and can recover from failure without losing prior work. Three runtime backends are currently supported — OpenRouter chat completions, Claude CLI, and Codex CLI — and the orchestrator treats them identically: it always validates outcomes by checking for required output artifacts, not by trusting the runtime's self-report.

## Why the Node Is the Durable Unit of Work

The node is the durable unit because everything the system needs to continue, recover, audit, or compare lives on disk inside the node directory — not in memory, not in an agent session, not in a provider's cloud.

Specifically:

- **Input** is written once and does not move. An agent that crashes can be retried against the same input.
- **Output** is validated by contract after every run. A run is not considered successful unless the required artifact exists.
- **Status and progression state** are explicit files. The orchestrator reads them on startup, so resuming after an interruption requires no coordination.
- **Run records** (`system/runs/run-XXX/`) capture the exact request, context packet, result, and usage for every attempt — before and after failure.
- **Recovery archives** (`system/recoveries/recovery-XXX/`) let the system make a fresh attempt without discarding prior evidence.

Agents are ephemeral: they are invoked, they write files, and they exit. The node outlives every agent that touches it. This means the system can swap runtimes, compare providers, or restart a failed agent without losing any ground.

## Mission Files to Inspect First

For any mission tree under `missions/`, start here:

| File | What It Tells You |
|---|---|
| `input/goal.md` (root node) | The original task the mission was given |
| `output/final-output.md` (root node) | The worker's answer or the synthesizer's summary |
| `system/mission-summary.json` | Aggregated outcome: status, terminal outcome, total cost, node count |
| `system/mission-events.jsonl` | Raw chronological event trail for the full mission |
| `for-orchestrator/` (any node) | Escalation reasons, next-action decisions, cancellation notes |
| `system/runs/run-XXX/summary.json` | Per-run breakdown: role, result, usage, duration |

If a node failed or escalated, check:

1. `output/escalation.md` — the agent's explanation of why it could not complete the task
2. `system/recoveries/` — prior attempt archives if the node was retried
3. `system/events.jsonl` — node-level event trail showing each status transition

The fastest way to confirm a mission succeeded is: `system/mission-summary.json` shows `terminal_outcome: completed` and the root node's `output/final-output.md` exists and is non-empty.
