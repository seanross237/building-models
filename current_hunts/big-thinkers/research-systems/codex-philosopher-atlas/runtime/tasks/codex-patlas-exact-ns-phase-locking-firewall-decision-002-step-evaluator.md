Evaluate the mission state and decide whether the mission should proceed with the current chain, replan, or terminate.

Mode: post-step
Mission: exact-ns-phase-locking-firewall
Active chain run: run-001
Mission file: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/MISSION.md
Current chain: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/CHAIN.md
Chain history: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/CHAIN-HISTORY.md
Latest planning run directory: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/planning-runs/run-001
Decision JSON output: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.json
Decision memo output: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.md
If decision is proceed, write GOAL.md here: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-002/GOAL.md
If decision is terminate, write mission completion note here: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/MISSION-COMPLETE.md
Chronological next step id: step-002

Latest completed step:
- Step id: step-001
- Step goal: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md
- Step results: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md
- Step state: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/state.json
- Step reasoning: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/REASONING.md
- Step summaries: /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/HISTORY-OF-REPORT-SUMMARIES.md

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
