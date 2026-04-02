# Operator Note on Open-Eywa

Open-Eywa is a distributed system designed to coordinate complex tasks by breaking them down into smaller units of work called nodes. Each node operates independently and can execute its assigned task reliably and durably, ensuring progress is saved and recoverable even in case of interruptions.

The node is the durable unit of work because it encapsulates all necessary context, state, and results for a specific portion of the overall task. This design allows for robust fault tolerance, easy parallelization, and clear tracking of progress across the system.

For human operators inspecting a mission, the most important files to review first are:

- `input/goal.md`: Defines the overall objective or task for the node.
- `output/final-output.md`: Contains the final results or deliverables produced by the node.
- `output/state.md`: Records the current state or progress of the node’s work, useful for understanding intermediate steps or resuming work.

These files provide a clear overview of what the node is trying to achieve, what it has accomplished, and how it is progressing.

---

This note should help operators quickly understand the purpose and workflow of Open-Eywa nodes and efficiently navigate mission files.
