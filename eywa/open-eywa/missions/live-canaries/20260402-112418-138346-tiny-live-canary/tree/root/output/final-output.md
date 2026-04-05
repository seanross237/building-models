# Operator Note on Open-Eywa

Open-Eywa is a distributed, hierarchical task execution system designed to break down complex missions into manageable units of work called nodes. Each node represents a discrete step or task within the overall mission, enabling clear tracking, modular execution, and robust fault tolerance.

## Why the Node is the Durable Unit of Work

The node is the durable unit of work because it encapsulates all necessary information, state, and progress for a specific task. This durability ensures that work can be paused, resumed, retried, or audited without loss of context. Nodes provide a stable checkpoint that supports reliable execution and recovery in a distributed environment.

## Key Mission Files for Human Inspection

To understand and interact with the mission effectively, human operators should first inspect the following files:

- `input/context.md`: Provides the overall mission context and parent task details.
- `input/parent-instructions.md`: Contains the original task instructions and goals.
- `output/final-output.md`: Where the node writes its final results or deliverables.
- `output/state.md`: Tracks the node's current state and progress.

These files offer a clear view of the mission's purpose, the node's role, and the current execution status, enabling efficient monitoring and intervention if needed.

---

This note aims to give a concise overview for operators to quickly grasp the Open-Eywa system and the significance of nodes within it.