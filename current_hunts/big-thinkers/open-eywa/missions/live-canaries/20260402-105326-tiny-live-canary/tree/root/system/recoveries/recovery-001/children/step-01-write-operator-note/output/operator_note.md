# Open-Eywa Operator Note

Open-Eywa is a system designed to manage and execute complex, multi-step tasks by breaking them down into smaller, independent units called "nodes."

Each node represents a durable unit of work. This means that the state, inputs, and outputs of a node are preserved, allowing for tasks to be resumed, parallelized, and audited. This durability ensures that progress is not lost and provides a clear, traceable history of operations.

When inspecting a mission, a human operator should first read this `output/operator_note.md` file. This note provides a high-level overview of the mission's purpose and how to interpret the results. Following this, depending on the mission's outcome, `output/final-output.md` or `output/state.md` would be the next logical files to inspect for detailed results or status.
