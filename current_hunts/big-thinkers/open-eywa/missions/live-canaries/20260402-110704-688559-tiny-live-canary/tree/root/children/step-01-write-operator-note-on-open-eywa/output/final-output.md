# Operator Note on Open-Eywa

**What is Open-Eywa?**  
Open-Eywa is a distributed, hierarchical task execution system designed to break down complex missions into manageable units called nodes. Each node represents a discrete unit of work that can be executed, monitored, and verified independently, enabling scalable and reliable mission progress.

**Why is the node the durable unit of work?**  
The node is the durable unit of work because it encapsulates all necessary context, state, and results for a specific task segment. This durability ensures that work can be paused, resumed, retried, or audited without loss of information, providing robustness and traceability throughout the mission lifecycle.

**Which mission files should a human inspect first?**  
Humans should prioritize inspecting the following mission files:  
- `input/context.md` 
for overall mission context and instructions.  
- `output/final-output.md` 
to review the final results or deliverables of the node.  
- `output/state.md` 
to understand the current state and progress of the node.  
- `output/escalation.md` (if present) 
to identify any issues requiring human intervention.

Inspecting these files ensures a clear understanding of the mission goals, current progress, and any problems that need resolution.
