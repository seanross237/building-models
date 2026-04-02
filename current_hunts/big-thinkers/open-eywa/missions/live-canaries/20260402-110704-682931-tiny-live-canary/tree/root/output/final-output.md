# Operator Note on Open-Eywa

Open-Eywa is a distributed system designed to manage complex tasks by breaking them down into smaller, manageable units called nodes. Each node represents a durable unit of work that can operate independently, maintain state, and communicate with other nodes. This architecture ensures robustness, fault tolerance, and scalability in task execution.

The node is the durable unit of work because it encapsulates all necessary context, progress, and results related to a specific part of the overall task. This encapsulation allows nodes to persist their state, recover from interruptions, and coordinate with other nodes without losing information or duplicating effort.

For human operators inspecting a mission, the most important files to review first are:

1. `input/goal.md` — This file contains the mission's primary objective and task description.
2. `output/final-output.md` — This file holds the final results or deliverables produced by the node.
3. `output/state.md` — This file provides the current state and progress of the node's work.
4. `output/escalation.md` (if present) — This file indicates any issues or blockers that require human intervention.

Reviewing these files gives a clear understanding of the mission's purpose, current status, and any problems that need attention.
