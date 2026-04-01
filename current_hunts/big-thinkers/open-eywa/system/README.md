# System Rebuild

This is the fresh implementation area for the contract-first rebuild.

Subdirectories:

- `orchestrator/`
  The node-state engine and routing logic.
- `runtime/`
  The agent-run execution layer.
- `tools/`
  The controlled local capability layer.
- `configs/`
  Models, tool profiles, and runtime configuration.
- `scripts/`
  Entry points and developer utilities.

Rebuild rule:

- build outward from the canonical node contract
- keep protocol hard in code
- keep models out of correctness decisions
- design for offline simulation before live inference
