# Operator Note on Open-Eywa

Open-Eywa is a distributed system designed to manage complex workflows by breaking them down into discrete, manageable units called nodes. Each node represents a durable unit of work that can be independently executed, tracked, and resumed if necessary. This design ensures robustness, fault tolerance, and clear progress tracking within the system.

The node is the durable unit of work because it encapsulates all the necessary context, state, and outputs related to a specific task or subtask. This encapsulation allows the system to recover from interruptions, maintain consistency, and coordinate work across multiple nodes efficiently.

For human operators inspecting a mission, the key files to review first are:

1. `input/goal.md` — This file contains the mission's primary objective and task description.
2. `output/final-output.md` — This file will contain the final results or deliverables produced by the node.
3. `output/state.md` — This file tracks the current state and progress of the node's work.
4. `output/escalation.md` — If present, this file indicates issues or blockers requiring human intervention.

Reviewing these files provides a clear understanding of the mission's purpose, current progress, and any problems that need attention.
