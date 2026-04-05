Open-Eywa is a system designed to manage and execute complex computational tasks by dividing them into smaller, self-contained units called nodes. Each node represents a durable unit of work, encapsulating its execution environment, code, and data to ensure reproducibility and track progress.

For a human operator inspecting a mission, the following files are crucial for understanding and verifying the work:

1.  **`input/goal.md`**: This file outlines the primary objective or task assigned to the mission.
2.  **`output/final-output.md`**: This contains the final results or summary produced by the node's execution.
3.  **`output/state.md`**: This file provides insights into the node's current status, progress, and any intermediate states.
4.  **`output/escalation.md`**: If this file exists, it indicates that the node encountered an unresolvable issue and requires human intervention or re-evaluation.

Starting with `input/goal.md` provides context, while examining the `output/` files allows for verification of the work performed.