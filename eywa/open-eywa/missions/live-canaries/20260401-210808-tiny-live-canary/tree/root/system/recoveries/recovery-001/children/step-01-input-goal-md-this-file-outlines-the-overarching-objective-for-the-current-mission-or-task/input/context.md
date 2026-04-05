## Parent Task
Write a short operator note explaining what Open-Eywa is, why the node is the durable unit of work, and which mission files a human should inspect first.

## Parent Plan
## Operator Note

Open-Eywa is a framework designed to orchestrate complex, multi-agent tasks. It achieves this by decomposing large goals into smaller, manageable steps, each executed by specialized agents.

The **node** serves as the durable unit of work within Open-Eywa. Each node encapsulates a specific part of the task tree, maintaining its own state, files, and execution history. This design ensures durability, allowing for resilience, reproducibility, and the potential for parallel execution. If a node encounters an issue, its work is preserved, and it can be restarted or retried without losing progress.

For a human inspecting a mission, the primary files to review are:

1.  `input/goal.md`: This file outlines the overarching objective for the current mission or task.
2.  `output/plan.md`: If the current node is a `planner`, this file details the breakdown of the task into child steps. If it's a `worker`, this would typically be `output/result.md` detailing the outcome.
3.  `output/state.md`: This file provides crucial context, including reasoning behind decisions, status updates, and any uncertainties encountered during the node's execution.

## Parent State
The task is to write a short operator note explaining what Open-Eywa is, why the node is the durable unit of work, and which mission files a human should inspect first. This task is straightforward and can be executed directly by a single agent. The output will be a markdown file.
