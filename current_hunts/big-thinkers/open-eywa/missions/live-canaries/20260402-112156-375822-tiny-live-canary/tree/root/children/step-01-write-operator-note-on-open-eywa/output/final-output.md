# Operator Note on Open-Eywa

Open-Eywa is a distributed, hierarchical system designed to manage complex tasks by breaking them down into smaller, manageable units called nodes. Each node represents a durable unit of work that encapsulates a specific task or subtask, along with its context, state, and results. This structure ensures robustness, traceability, and modularity in task execution.

The node is the durable unit of work because it maintains all necessary information to resume, verify, or audit the task independently. Nodes persist their state and outputs, allowing the system to recover from interruptions and enabling human operators to inspect and intervene at precise points in the workflow.

For human operators inspecting a mission, the priority should be:

1. **Context Files**: These provide the background and rationale for the mission and its tasks.
2. **Plan Files**: These outline the intended steps and goals, helping to understand the workflow.
3. **State Files**: These show the current progress and any intermediate results.
4. **Final Output Files**: These contain the completed work products or conclusions.

By focusing on these files in this order, operators can efficiently understand the mission's purpose, monitor its progress, and verify its outcomes.

---

This note aims to give a clear and concise overview of Open-Eywa's core concepts and guide human operators on where to focus their inspection efforts within mission files.
