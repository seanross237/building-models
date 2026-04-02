# Exploration 002 Goal — Tao Gate for the Pressure-Side Branch

## Objective

Test the short list of pressure-relevant candidate NS-specific ingredients against the Tao 2016 averaged-Navier-Stokes filter and determine whether any nontrivial version of the harmonic-tail branch survives.

The candidates to screen are only:

- the exact algebraic form of `u · ∇u`
- pressure-Hessian / tensor structure tied to `∂_i∂_j p = R_i R_j(u_i u_j)`
- vorticity or strain geometry only if it directly affects the surviving far-field pairing

## Success Criteria

- For each candidate, return one verdict:
  - `survives Tao gate`
  - `fails Tao gate`
  - `unclear but testable`
- Distinguish generic harmonic/elliptic facts from genuinely NS-specific structure.
- Tie the verdict to the actual far-field coefficient problem, not to unrelated NS structure.
- State whether Step 1 should green-light Step 2 or trigger the negative-result track.

## Failure Criteria

- Treats generic harmonic regularity as NS-specific.
- Keeps a candidate alive without explaining how it could shrink the actual bad coefficient.
- Drifts into broad vorticity or geometry discussion detached from the pressure pairing.

## Required Source Anchors

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/MISSION.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-001/mission-context.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-philosopher-atlas/missions/vasseur-pressure/steps/step-002/RESULTS.md`

## Constraints

- Use local repository materials only.
- Do not broaden the candidate list.
- Do not count identities or representation formulas as progress unless they plausibly act on `C_far` itself.
- Be explicit about what Tao's averaged model preserves and therefore what it does not kill.

## Deliverables

Write:

1. `REPORT.md` with the candidate-by-candidate Tao screening.
2. `REPORT-SUMMARY.md` with:
   - goal
   - what was tested
   - outcome
   - one key takeaway
   - whether Step 2 should proceed or be downgraded
