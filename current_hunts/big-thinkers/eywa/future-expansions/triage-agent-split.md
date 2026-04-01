# Triage Agent Split

## Problem
The mechanical C x I threshold (> 25 -> planner, <= 25 -> executor) is a blunt instrument. A numeric product can't capture nuances like "this task is complex but well-defined enough for a single agent" or "this task is simple but politically sensitive and needs decomposition for review purposes."

## Design
Replace the mechanical threshold with a dedicated triage agent that reads the child's goal and decides executor vs. planner with richer reasoning. The triage agent sees:

- The child's goal.md
- The parent's full plan (for context on where this step fits)
- The C and I scores from the parent (as advisory input, not deterministic)
- Guidance on when decomposition helps vs. when it adds overhead

The triage agent writes its decision to `for-orchestrator/agent-mode` with a brief rationale logged for post-run review.

## Key Considerations
- Adds latency to every child spawn (one extra agent call per node). Worth profiling whether the better routing decisions justify the overhead.
- The triage agent becomes a new decision point in the Decision Point Catalog (needs its own logging and review criteria).
- Could start as a hybrid: use the mechanical threshold by default, but invoke the triage agent when C x I is in a "gray zone" (e.g., 20-30).
