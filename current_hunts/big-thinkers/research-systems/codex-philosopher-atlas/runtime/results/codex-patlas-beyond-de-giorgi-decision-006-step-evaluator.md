Wrote the controller outputs for `decision-006` and set the mission state to `replan`.

The active geometry chain is treated as invalidated after `step-004`: the dynamic plausibility screen fired its kill condition, no candidate was ranked `dynamically plausible`, and advancing to the fixed stretching-representation step would have been unjustified. I therefore did not write `step-005/GOAL.md`.

Files:
[decision-006.json](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/controller/decisions/decision-006.json)
[decision-006.md](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/controller/decisions/decision-006.md)

Verification: the JSON matches the requested schema and marks `chain_assessment` as `invalidated`, `termination_status` as empty, and `mission_complete` as `false`.