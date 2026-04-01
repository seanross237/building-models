# Belief State

## Initial State

task:
  goal: "Rank plausible research routes toward Navier-Stokes existence and smoothness"
  success_criteria:
    - "A ranked route map"
    - "Three or more cycles completed"
    - "A self-contained run record"
  non_goals:
    - "Do not solve the millennium problem"
    - "Do not produce a formal proof"

context:
  known_facts:
    - "The problem is a global regularity question for 3D incompressible Navier-Stokes."
    - "A good route likely needs a tractable blow-up or regularity criterion."
    - "Purely elegant but untestable routes are low value under budget."
  active_hypotheses:
    - "Criticality-based routes have high option value."
    - "Epsilon-regularity routes are more immediately testable."
    - "Cascade-based routes may be useful but harder to bound quickly."
  rejected_hypotheses: []
  prior_attempts: []

search:
  frontier_routes:
    - "criticality-and-concentration"
    - "partial-regularity-and-epsilon-bootstrapping"
    - "frequency-cascade-and-structure-rules"
    - "barrier-and-morrey-control"
  pruned_routes: []
  chosen_route: null
  route_history: []

uncertainty:
  key_unknowns:
    - "Which route family is most likely to yield sharp intermediate lemmas?"
    - "Which route family best balances reach and testability?"
    - "Which route family is most budget-efficient?"
  confidence_notes:
    - "Confidence is moderate and heuristic, not evidence-tight."
    - "Scores should be treated as planning estimates only."
  calibration_flags:
    - "Avoid overvaluing conceptual breadth."
    - "Prefer routes that generate concrete checkpoints."

budget:
  remaining_steps: 3
  remaining_time: "tight"
  remaining_tokens: "tight"
  remaining_tool_calls: "tight"

outputs:
  decision_log: []
  evidence_log: []
  artifacts: []

## Cycle Updates

### Cycle 1

context:
  active_hypotheses:
    - "Criticality and concentration compactness offer the strongest route family."
    - "Partial regularity is the best backup because it is concrete and verifiable."
  search:
    chosen_route: "criticality-and-concentration"
  uncertainty:
    calibration_flags:
      - "The initial ranking should privilege leverage over elegance."

### Cycle 2

context:
  active_hypotheses:
    - "Criticality route remains strongest, but it needs a backup checkpoint."
    - "Partial regularity has improved because it decomposes well into testable subproblems."
  search:
    chosen_route: "partial-regularity-and-epsilon-bootstrapping"
  uncertainty:
    calibration_flags:
      - "Some broad criticality routes are too diffuse for a tight budget."

### Cycle 3

context:
  active_hypotheses:
    - "Partial regularity is the best execution route for a short run."
    - "Criticality remains the best long-horizon route."
  search:
    chosen_route: "partial-regularity-and-epsilon-bootstrapping"
  uncertainty:
    calibration_flags:
      - "The best route is the one with the clearest next-step falsifiers."
