# Belief State

## Initial State

task:
  goal: "Find the most promising apparently underexplored NS route from the current status memo"
  success_criteria:
    - "Produce one theorem-facing route"
    - "Respect closed-route findings"
    - "Use a novelty caveat rather than overclaiming"
  non_goals:
    - "Do not solve Navier-Stokes"
    - "Do not certify absolute novelty"

context:
  known_facts:
    - "The memo closes enstrophy, De Giorgi/Vasseur, epsilon-regularity, H^1 pressure, and harmonic far-field routes."
    - "The memo treats the Tao line as blocked at object definition, not fully dead."
    - "The memo says a canonical packet model is the one live-looking frontier."
  active_hypotheses:
    - "The next useful path must solve the packet non-canonicity problem."
    - "A theorem object anchored to a hypothetical minimal blowup element may reduce modeling freedom."
    - "Microlocal directional functionals may supply canonical packet coordinates or leakage observables."
  rejected_hypotheses: []
  prior_attempts:
    - "Exact singleton Tao-circuit embedding failed."
    - "Trigger-only reframing failed."

search:
  frontier_routes:
    - "pure canonical packet model"
    - "critical-element packet leakage rigidity"
    - "direct microlocal regularity route"
    - "reopened partial-regularity bootstrap with new language"
  pruned_routes: []
  chosen_route: null
  route_history: []

uncertainty:
  key_unknowns:
    - "Can a critical element make packet coordinates canonical enough?"
    - "Can leakage be turned into a quantitative lower bound?"
    - "Is the microlocal literature already too close to this route for it to count as new?"
  confidence_notes:
    - "Local memo is strong about closures."
    - "Novelty judgment is low-to-medium confidence because the literature scan is selective."
  calibration_flags:
    - "Do not confuse a synthesis of known tools with a fully new theorem."
    - "Favor routes that eliminate non-canonicity."

budget:
  remaining_steps: 3
  remaining_time: "short conceptual scan"
  remaining_tokens: "moderate"
  remaining_tool_calls: "limited"

outputs:
  decision_log: []
  evidence_log: []
  artifacts: []

## Cycle Updates

### Cycle 1

context:
  active_hypotheses:
    - "A plain packet-model mission is necessary but not sufficient because it still lacks a canonical anchor."
    - "Critical-element methods may provide the missing anchor by selecting a minimal bad object."
search:
  chosen_route: "critical-element packet leakage rigidity"
uncertainty:
  calibration_flags:
    - "Be careful not to reopen epsilon-regularity by relabeling it."

### Cycle 2

context:
  active_hypotheses:
    - "The winning route should synthesize three ingredients: Tao mechanism, critical element, and packet/microlocal observables."
    - "A direct microlocal regularity route looks more speculative than a microlocal support role inside a packet theorem."
search:
  chosen_route: "critical-element packet leakage rigidity"
uncertainty:
  calibration_flags:
    - "Novelty remains uncertain, but the exact synthesis still looks absent in checked sources."

### Cycle 3

context:
  active_hypotheses:
    - "The sharpest theorem target is a lower bound on unavoidable packet leakage or angular dispersion for any minimal blowup profile."
    - "If proved, this would convert the Tao comparison from a story into an exclusion mechanism."
search:
  chosen_route: "critical-element packet leakage rigidity"
  pruned_routes:
    - "reopened partial-regularity bootstrap with new language"
    - "pure canonical packet model"
uncertainty:
  calibration_flags:
    - "The route is promising because it fixes object definition, not because it already solves the hard estimate."
