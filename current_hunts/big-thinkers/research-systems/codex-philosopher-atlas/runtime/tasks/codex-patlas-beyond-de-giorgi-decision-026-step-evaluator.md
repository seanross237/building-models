Evaluate the mission state and decide whether the mission should proceed with the current chain, replan, or terminate.

Mode: bootstrap
Mission: beyond-de-giorgi
Active chain run: run-011
Mission file: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/MISSION.md
Current chain: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md
Chain history: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN-HISTORY.md
Latest planning run directory: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-011
Decision JSON output: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/controller/decisions/decision-026.json
Decision memo output: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/controller/decisions/decision-026.md
If decision is proceed, write GOAL.md here: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-016/GOAL.md
If decision is terminate, write mission completion note here: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/MISSION-COMPLETE.md
Chronological next step id: step-016

Write the decision JSON with exactly this schema:
{
  "decision": "proceed" | "replan" | "terminate",
  "reason": "short paragraph",
  "chain_assessment": "active" | "invalidated" | "completed",
  "step_id_evaluated": "step-XYZ or empty string",
  "next_step_id": "step-XYZ or empty string",
  "next_logical_chain_step": "short label or empty string",
  "termination_status": "empty string, negative_complete, positive_complete, or blocked",
  "mission_complete": true | false
}

Rules:
- Choose `proceed` only if the current chain still looks like the right next path.
- Choose `replan` if the latest step weakens, closes, or invalidates the branch enough that the mission should compare paths again.
- Choose `terminate` only if the mission should now stop with a terminal result.
- If `proceed`, write a full step GOAL.md for the provided next step path.
- The step directory number is mission chronology, not proof that the logical chain-step number is the same.
- If `terminate`, write the mission completion note.
- Keep the strategizer step-scoped. You are deciding mission control, not executing the next step.
