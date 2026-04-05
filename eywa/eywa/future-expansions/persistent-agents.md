# Persistent Agents

## Problem
Ephemeral agents reconstruct their state entirely from files on each re-spawn. For nodes that go through many evaluation cycles (receiving child results, deciding continue/replan/escalate, receiving the next child's results, etc.), critical nuance can be lost in serialization. The "dark knowledge" -- hunches, rejected alternatives, evolving intuitions -- degrades with each serialize/deserialize cycle.

## Design
For nodes where context reconstruction from files is too lossy, keep the agent alive across multiple phases rather than killing and re-spawning it. The agent would block (or sleep) while waiting for child results, then resume with its full context intact when the orchestrator signals new input.

## Key Considerations
- Resource cost: persistent agents hold a tmux session and (depending on implementation) a model context window open for the duration. This limits how many can run simultaneously.
- Crash recovery: if a persistent agent's session dies, the system must fall back to ephemeral reconstruction from state files. State files must still be written at every phase boundary.
- Which nodes benefit most: likely high-depth planners that evaluate many children sequentially. Leaf executors don't need persistence (they run once and complete).
- Could be opt-in per node based on expected evaluation cycles, rather than a global switch.
