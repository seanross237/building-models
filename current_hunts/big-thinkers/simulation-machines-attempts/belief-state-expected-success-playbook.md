# Belief-State Expected-Success Search

## Purpose

This document is a complete execution manual for an agent facing a hard, uncertain task where the solution is not a single obvious path but a landscape of possible routes.

Use this strategy when:

- the task is high uncertainty
- there are multiple plausible approaches
- progress depends on discovering intermediate facts, lemmas, constraints, or structures
- the best next move depends on what might be learned from that move

The core idea is:

- represent the task as a belief state
- generate candidate routes from the belief state
- estimate what each route is likely to reveal
- score routes by expected chance of eventual success
- choose the best branch, execute one step, update beliefs, and repeat

This is a search-and-replan loop, not a one-shot plan.

---

## Operating Rules

1. Keep every important assumption explicit.
2. Never commit to a long route without a checkpoint.
3. Prefer routes that both advance the task and improve future decision quality.
4. Track uncertainty at every step.
5. Recompute the best route whenever new evidence arrives.
6. Prune aggressively when branches become dominated, contradictory, or too costly.
7. Preserve a complete written trail so another agent can resume from the record alone.
8. Create a dedicated run folder before doing substantive work.
9. Write all run artifacts inside that run folder only.
10. Do not edit, create, delete, or reorganize anything outside the run folder.

---

## Execution Boundary

This strategy must run inside a self-contained output folder.

### Folder rule

Before analysis begins, create a new run folder inside the strategy's working directory. Use a name that is unique and reviewable, such as:

```text
run-001-task-slug
run-2026-04-01-task-slug
```

All documents, notes, logs, and artifacts created during execution must live inside that folder.

### Isolation rule

- Do not modify files outside the run folder.
- Do not use external files as mutable scratch space.
- If you must read outside context, copy only the necessary summary into the run folder.
- If the task cannot be executed without editing outside the run folder, stop and report that the strategy is blocked by boundary constraints.

### Minimum required run structure

Create this structure at the start of the run:

```text
run-<id>-<task-slug>/
  README.md
  manifest.md
  task.md
  belief-state.md
  route-map.md
  decision-log.md
  evidence-log.md
  calibration.md
  final-summary.md
  artifacts/
```

You may add extra files if useful, but these files are required.

### File responsibilities

- `README.md`: one-screen index explaining the run, file layout, and current status
- `manifest.md`: file inventory, cycle count, and boundary statement for auditability
- `task.md`: task framing, constraints, success criteria, and inferred assumptions
- `belief-state.md`: current structured belief state and updates over time
- `route-map.md`: active route families, scored branches, and pruned branches
- `decision-log.md`: per-cycle decision record with chosen and rejected actions
- `evidence-log.md`: observations, implications, and contradictions
- `calibration.md`: forecast quality, misses, and corrections
- `final-summary.md`: result, what was learned, unresolved questions, and best next route
- `artifacts/`: any supplementary tables, sketches, or supporting materials

---

## Inputs To Gather First

Before choosing any action, collect these inputs and write them down:

1. `Task statement`
   - the exact goal
   - what counts as success
   - what counts as partial progress

2. `Constraints`
   - time budget
   - token/compute budget
   - tool limits
   - forbidden actions
   - required deliverables

3. `Known context`
   - relevant prior work
   - already-tested ideas
   - known dead ends
   - available artifacts

4. `Available action space`
   - what kinds of moves are allowed
   - what kinds of evidence can be gathered
   - what kinds of transformations can be made on the task state

5. `Risk profile`
   - low-risk incremental moves
   - high-upside exploratory moves
   - irreversible or expensive moves

6. `Stopping criteria`
   - success condition
   - best-effort condition
   - exhaustion condition

If any of these are missing, infer them conservatively and mark the inference.

---

## State Representation

Represent the current situation as a structured belief state.

### Required fields

```yaml
task:
  goal: ""
  success_criteria: []
  non_goals: []

context:
  known_facts: []
  active_hypotheses: []
  rejected_hypotheses: []
  prior_attempts: []

search:
  frontier_routes: []
  pruned_routes: []
  chosen_route: null
  route_history: []

uncertainty:
  key_unknowns: []
  confidence_notes: []
  calibration_flags: []

budget:
  remaining_steps: 0
  remaining_time: ""
  remaining_tokens: ""
  remaining_tool_calls: ""

outputs:
  decision_log: []
  evidence_log: []
  artifacts: []
```

### State rules

- Keep hypotheses short and testable.
- Keep evidence separate from interpretation.
- Track confidence for each hypothesis and each branch.
- Update the state after every meaningful observation.
- Treat the state as the system of record.

---

## Route Types

When generating candidate routes, consider these families:

1. `Direct attack`
   - try to solve the goal head-on.

2. `Decomposition route`
   - break the goal into subgoals, lemmas, or milestones.

3. `Evidence-finding route`
   - gather information that clarifies which paths are viable.

4. `Constraint route`
   - derive hard bounds, impossibility results, or necessary conditions.

5. `Analogy route`
   - map the task to a known solved problem or known framework.

6. `Counterexample route`
   - test whether a candidate approach fails in a sharp way.

7. `Bridge route`
   - search for an intermediate result that connects two known regions.

8. `Verification route`
   - check whether an apparently promising claim is actually valid.

Prefer routes that reduce uncertainty while keeping future options open.

---

## Candidate Action Generation

At each cycle, generate a small set of concrete candidate actions.

### Action generation procedure

1. Read the current belief state.
2. List the most important unknowns.
3. For each unknown, ask:
   - what action could reveal it?
   - what action could bypass it?
   - what action could prove it irrelevant?
4. Produce 3 to 7 concrete actions.
5. For each action, write:
   - intended purpose
   - expected observation types
   - likely failure modes
   - cost estimate
   - estimated success impact
   - route family
   - whether the action is exploratory, verifying, pruning, or advancing

### Action quality constraints

- Actions must be specific enough to execute immediately.
- Each action must change the state if it succeeds.
- Avoid vague actions like "think more."
- Prefer actions that can be falsified or clarified quickly.
- Broad route families are not a substitute for candidate actions.
- Every cycle must include an explicit action table with 3 to 7 actions, even if several actions belong to the same route family.

---

## Outcome Estimation

For each action, estimate the distribution of possible outcomes.

### Required outcome fields

```yaml
action: ""
outcomes:
  - label: ""
    probability: 0.0
    observation: ""
    state_update: ""
    downstream_value: 0.0
    confidence: ""
    notes: ""
```

### Estimation rules

- Use approximate probabilities, not fake precision.
- If uncertain, give coarse estimates such as 10%, 30%, 60%.
- Probabilities for outcomes of one action should sum to 1.
- Estimate downstream value as the action's effect on future success, not just immediate usefulness.
- If two outcomes are similar, merge them.

### Calibration rules

- Penalize overconfidence.
- If you have little basis for a number, lower the confidence level even if the number is useful.
- Record whether the estimate is:
  - grounded in evidence
  - analogy-based
  - heuristic
  - speculative

### Suggested confidence scale

- `high`: supported by direct evidence or strong structural analogy
- `medium`: plausible but not well-anchored
- `low`: speculative or weakly grounded

---

## Branch Scoring

Score each action by expected contribution to eventual success.

### Default scoring model

Use this mental model:

```text
branch_score =
  expected_success_probability
  + information_gain_bonus
  + option_value_bonus
  - expected_cost
  - risk_penalty
  - redundancy_penalty
```

### Practical interpretation

- `expected_success_probability`: how likely this branch is to eventually solve the task
- `information_gain_bonus`: how much this branch clarifies the problem space
- `option_value_bonus`: how much this branch opens future routes
- `expected_cost`: time, tokens, computation, complexity
- `risk_penalty`: chance of dead end, irrecoverable choice, or misleading evidence
- `redundancy_penalty`: how much this repeats already-tested ideas

### Scoring rules

- Prefer branches with high downstream leverage, not just high immediate payoff.
- Do not reward a branch for sounding elegant.
- Down-rank branches that merely restate the current state.
- Down-rank branches whose main benefit is novelty without testability.

---

## Selection Policy

After scoring all candidate actions, choose the next action using this policy:

1. Filter out dominated actions.
2. Remove actions that exceed budget.
3. Remove actions that are too vague to execute.
4. Keep the top 1 to 3 actions by branch score.
5. If uncertainty is high, prefer the best action plus one backup route.
6. Execute the action with the highest expected value unless a slightly lower-scoring action has much better information gain.

If two actions are close, prefer the one that:

- is cheaper
- is more reversible
- gives clearer evidence
- improves calibration

---

## Pruning Policy

Prune a branch when any of the following becomes true:

- it is contradicted by new evidence
- it is strictly dominated by another branch
- its expected value drops below a practical threshold
- its remaining cost exceeds budget
- it repeats already-discarded logic
- it no longer changes the search frontier meaningfully

When pruning, record:

- why it was pruned
- what evidence caused the pruning
- what residual uncertainty remains
- whether the branch should be revisited later

Do not delete pruned branches from memory. Archive them in the log.

---

## Replanning Loop

Use this loop after every step.

### Loop

1. Execute the chosen action.
2. Record the actual observation.
3. Update the belief state.
4. Compare actual outcome vs predicted outcome.
5. Adjust calibration if the prediction was poor.
6. Regenerate candidate actions.
7. Rescore branches.
8. Re-select the next action.

### Replan triggers

Replan immediately if:

- the action revealed a surprising result
- the central hypothesis changed
- the top branch collapsed
- a new higher-value route became visible
- the budget moved materially
- the task definition became clearer

---

## Budget Management

Budget is a first-class constraint.

### Budget policy

- Keep a running estimate of remaining capacity.
- Reserve a portion of the budget for recovery and verification.
- Never spend the entire budget on one speculative branch.
- If the task is highly uncertain, keep multiple route families alive for as long as possible.

### Recommended allocation

- `60%` on the strongest current route
- `25%` on the second-best route or a clarifying branch
- `15%` reserved for surprise pivots, checks, or recovery

If budget is very tight, compress to:

- one main route
- one cheap verification route

---

## Failure Handling

Treat failure as information, not as noise.

### Failure categories

1. `Model failure`
   - the route model was wrong

2. `Search failure`
   - the system failed to consider a viable route

3. `Estimation failure`
   - probabilities or scores were badly calibrated

4. `Execution failure`
   - the action was not carried out correctly

5. `Budget failure`
   - too much was spent on unproductive branches

### Recovery procedure

1. Name the failure type.
2. Identify the earliest point where the route diverged.
3. Decide whether the failure invalidates only one branch or the entire route family.
4. Add a corrective action.
5. Lower confidence in the failed assumptions.
6. Resume search from the strongest remaining branch.

Do not treat one failed branch as proof that the whole strategy is bad.

---

## Execution Loop

Use this exact operating loop until stop conditions are met.

```text
initialize belief state
gather missing inputs
create run folder and required files
generate route families
for each cycle:
  generate candidate actions
  estimate outcomes for each action
  score branches
  prune dominated branches
  choose best next action
  execute one action
  observe result
  update belief state
  log prediction error
  replan
  check stop conditions
end
```

### One-cycle rule

Do not execute a long sequence of uncommitted actions.

After each meaningful move, stop, update, and rescore.

### Documentation rule

After each cycle, update the run folder documents before starting the next cycle.

- update `belief-state.md`
- update `route-map.md`
- append to `decision-log.md`
- append to `evidence-log.md`
- append to `calibration.md` if forecast quality changed
- update `manifest.md` with cycle count and current status

For each cycle, the written record must include:

- a candidate action table with 3 to 7 actions
- an outcome distribution table for each considered action
- the chosen action and rejected actions
- the actual observation or explicit note that the cycle used simulated planning evidence only
- the resulting state delta

The run is not complete unless the written record is sufficient for a different agent to resume without hidden context.

---

## Stop Conditions

Stop when one of these is true:

- the goal is solved
- the best available route is clearly exhausted
- the remaining budget is too small for meaningful progress
- the search frontier has converged on a stable conclusion
- further work would be redundant relative to the current evidence

When stopping, produce a final decision record, even if the answer is partial.

---

## Required Output Artifacts

Every run of this strategy must produce these artifacts:

1. `Run Folder`
   - a self-contained folder containing the full execution record
   - no edits outside that folder

2. `Route Map`
   - the active route families
   - the pruned routes
   - the chosen route and why it was chosen

3. `Belief State`
   - the current facts
   - hypotheses
   - confidence levels
   - open unknowns

4. `Decision Log`
   - every action considered
   - the score assigned
   - the reason for acceptance or rejection

5. `Evidence Log`
   - observations
   - what they changed
   - what they ruled out

6. `Calibration Notes`
   - where the agent was overconfident
   - where the estimates were well calibrated
   - what to adjust next time

7. `Final Summary`
   - result
   - what was learned
   - what remains open
   - next best route if continuing later

8. `Run Index`
   - a short README that tells a reviewer where to start and which file reflects the latest state

9. `Manifest`
   - a file inventory for the run
   - cycle count
   - explicit boundary statement
   - brief note on whether the run used external evidence, internal reasoning only, or a mix

---

## Concrete Output Template

Use this template for the final writeup.

```markdown
# Strategy Execution Report

## Task
- Goal:
- Success criteria:
- Constraints:

## Belief State
- Known facts:
- Active hypotheses:
- Key unknowns:
- Confidence notes:

## Route Map
- Route family 1:
  - Action:
  - Expected outcomes:
  - Score:
- Route family 2:
  - Action:
  - Expected outcomes:
  - Score:
- Pruned routes:

## Chosen Action
- Selected action:
- Why this one:
- Expected observation:
- Expected value:
- Cost:

## Observation
- What happened:
- Surprise level:
- Prediction error:

## Update
- State changes:
- Hypotheses strengthened:
- Hypotheses weakened:
- New unknowns:

## Calibration
- Well-calibrated estimates:
- Miscalibrated estimates:
- Adjustments for next cycle:

## Decision Log
- [timestamp or cycle] action / score / decision / reason

## Evidence Log
- [timestamp or cycle] observation / implication

## Final Summary
- Outcome:
- What was learned:
- What remains unresolved:
- Best next route:
```

---

## Minimal Agent Prompt

If another agent needs a short prompt to execute this strategy, give it this:

> You are running belief-state expected-success search. First create a new self-contained run folder and keep every artifact inside it. Do not modify anything outside that folder. Build a structured belief state, generate 3 to 7 concrete candidate actions per cycle, estimate outcome distributions for each action, score branches by expected success plus information gain plus option value minus cost and risk, choose the best action, execute one step, update the belief state, log the result, replan, and repeat. Distinguish route families from concrete actions, tag evidence as external observation, derived inference, or planning assumption, and maintain a full manifest, decision, evidence, calibration, and final-summary record that another agent could resume from without hidden context.

---

## Completion Standard

This strategy is complete when:

- the agent can explain why the final branch was chosen
- the agent can show how alternative branches were scored and pruned
- the agent can show how each observation changed the belief state
- the agent can state whether calibration improved or worsened
- the agent can resume later from the written record alone
