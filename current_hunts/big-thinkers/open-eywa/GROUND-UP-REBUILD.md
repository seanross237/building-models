# Ground-Up Rebuild

Open-Eywa is now being rebuilt from the ground up.

The earlier implementation has been preserved intact under:

- `saved-prototypes/2026-04-01-pre-ground-up-rebuild/`

That archived prototype is being treated as:

- a reference
- a source of ideas
- a source of failure cases

It is not the foundation we are building on directly anymore.

The new foundation is:

- node-first
- contract-first
- simulation-first before live-model testing

Current build order:

1. land the canonical node contract
2. audit the implementation against that contract
3. design the offline simulated test system
4. rebuild the engine from the contract upward
5. only then reintroduce live model runs

The planning and contract docs in `april-first-planning/` are now the main source of truth for the rebuild.
