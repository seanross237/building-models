**Open-Eywa Operator Note**

Open-Eywa is a system designed for managing and executing complex computational tasks. Each node within Open-Eywa represents a durable unit of work, encapsulating all necessary context, code, and state to perform a specific part of a larger mission. This ensures reproducibility and allows for granular control over task execution.

For a human operator, the primary files to inspect when examining a mission are typically found within the `tree/root` directory of a node. Specifically, `input/goal.md` outlines the overall objective, while `output/final-output.md` contains the results of the node's execution. Examining these two files will provide a clear understanding of the task assigned to this node and its outcome.
