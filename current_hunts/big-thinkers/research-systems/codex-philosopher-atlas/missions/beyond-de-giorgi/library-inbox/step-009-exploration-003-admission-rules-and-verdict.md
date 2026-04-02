# Exploration 003 Report

## Goal

Freeze the endpoint-tied admission rules and the final Step-009 verdict for the
frozen `I_p^far` ledger, without reopening the endpoint, cash-out line,
currency, or threshold established by Explorations 001 and 002.

## Status

- Started: 2026-03-31
- Outcome: succeeded

## Sources To Check

- `missions/beyond-de-giorgi/steps/step-009/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-014.md`
- `missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`
- `missions/beyond-de-giorgi/planning-runs/run-006/judgments/chain-01.md`
- `runtime/results/codex-patlas-standalone-20260331T152036Z-receptionist-42212.md`
- `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-002/REPORT.md`
- `library/factual/far-field-pressure-obstruction/exact-surviving-far-field-pairing.md`
- `library/factual/far-field-pressure-obstruction/bad-coefficient-stays-at-fixed-energy-scale.md`
- `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/meta/obstruction-screening/when-one-bad-term-and-one-gain-currency-are-frozen-a-tao-screen-may-end-the-branch.md`

## Working Notes

### Initial hypotheses under test

1. The endpoint setup survives Step 1 because one theorem ledger, one cash-out
   line, one currency, and one threshold are already frozen.
2. Same-scale unconstrained exterior or harmonic freedom in the full
   `I_p^far` pairing should count as immediate failure because the frozen
   coefficient-shrinkage endpoint would not be met.
3. Tao sensitivity should be mandatory but insufficient by itself unless it
   yields the frozen coefficient reduction on the full pairing.

### Findings log

- Report skeleton created before source review.
- Read the Step-009 goal, active chain, controller decision, run-006 judgment,
  prior explorations 001 and 002, and the far-field obstruction packet.
- Confirmed that Explorations 001 and 002 already froze the theorem ledger,
  cash-out line, currency, and threshold shape on the inherited full
  `I_p^far` pairing.
- Confirmed that the only remaining work for this exploration is to state the
  two admission rules in endpoint-specific form and classify the branch
  narrowly as proceed-or-stop.

## Evidence Read

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/controller/decisions/decision-014.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/judgments/chain-01.md`
- [VERIFIED] `runtime/results/codex-patlas-standalone-20260331T152036Z-receptionist-42212.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-001/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-002/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/exact-surviving-far-field-pairing.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/bad-coefficient-stays-at-fixed-energy-scale.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/affine-and-higher-harmonic-modes-survive-as-moments.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/constant-harmonic-mode-is-automatically-killed.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/real-progress-requires-a-smaller-effective-coefficient.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- [VERIFIED] `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] `library/meta/obstruction-screening/when-one-bad-term-and-one-gain-currency-are-frozen-a-tao-screen-may-end-the-branch.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`

## Findings

### 1. Frozen ledger inherited from Explorations 001 and 002

- [VERIFIED] The only exact theorem ledger locally frozen on disk is the
  inherited suitable-weak / Leray-Hopf plus local-energy inequality,
  CKN/Lin epsilon-regularity contradiction package, with live bad term
  `I_p^far = -∬ p_far div(v_k phi_k^2 e_hat)`.
- [VERIFIED] The full pairing, not a surrogate piece, is the live endpoint
  object for this branch. Its operative inherited estimate is
  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}` with
  `C_far ~ ||u||_{L^2}^2 / r_k^3`.
- [VERIFIED] The progress currency is already frozen as quantified reduction of
  the specified nonlocal remainder, namely shrinkage of the effective
  coefficient on the same full pairing.
- [INFERRED] The Step-1 threshold shape already frozen by Exploration 002 is:
  after later reconstruction and any required localization debt, the branch
  must still yield
  `|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}`
  with `C_far,eff(k) <= (1-delta) ||u||_{L^2}^2 / r_k^3`
  for some uniform `delta > 0`, or an equivalent same-ledger full-pairing
  estimate with positive-margin net coefficient shrinkage.

### 2. Exact same-scale unconstrained exterior / harmonic failure rule

- [VERIFIED] `CHAIN.md`, `winning-chain.md`, `decision-014.md`, and
  `judgments/chain-01.md` require that same-scale unconstrained exterior or
  harmonic freedom count as immediate failure, not as a tolerable residual.
- [VERIFIED] `step-001/RESULTS.md` and the far-field packet show why that rule
  must be stated against `I_p^far` itself: constants are already killed by the
  pairing, but affine-and-higher harmonic modes remain live in the full
  far-field term.
- [INFERRED] Exact branch rule to freeze:
  later tensor work is admitted only if, after full harmonic accounting and any
  required localization debt, it yields positive-margin shrinkage of the
  coefficient on the complete frozen pairing `I_p^far`.
- [INFERRED] Therefore if the reconstructed full pairing still contains any
  same-scale unconstrained exterior or harmonic remainder coming from the live
  affine-and-higher harmonic moments, so that the branch cannot prove a smaller
  effective coefficient on that full pairing, the branch fails immediately.
- [PROPOSED] Operational wording for later steps:
  "For the frozen endpoint
  `I_p^far = -∬ p_far div(v_k phi_k^2 e_hat)`,
  any candidate that closes only on a local piece, a self-induced piece, a
  reduced model, or a representation-level defect while leaving a same-scale
  unconstrained exterior/harmonic remainder in the full pairing is an immediate
  branch failure, because the frozen coefficient-shrinkage threshold on
  `I_p^far` has not been met."

### 3. Exact Tao rule for this branch

- [VERIFIED] The step goal, active chain, and run-006 judgment all require the
  Tao rule in the same form:
  averaged-model sensitivity is mandatory, but it does not by itself establish
  theorem relevance.
- [VERIFIED] The obstruction packet sharpens this branch-specifically:
  generic harmonic regularity, exact algebraic rewrites of `u . grad u`, and
  local vorticity/strain geometry all fail unless they shrink the actual bad
  coefficient in the full far-field pairing.
- [VERIFIED] The meta screening note fixes the mechanical standard:
  each candidate must say what exact estimate changes and what exact term or
  coefficient becomes smaller on the frozen ledger.
- [INFERRED] Exact Tao rule to freeze:
  every later mechanism must be tested against an explicit averaged-model
  comparator, and if the relevant feature survives averaging then the candidate
  is dead for the branch; but even averaged-model sensitivity does not count
  unless the candidate also produces estimate-level shrinkage of the live
  coefficient on the full `I_p^far` pairing.
- [PROPOSED] Operational wording for later steps:
  "A candidate mechanism must be destroyed by the relevant averaged-model
  comparison, but Tao sensitivity is only an admission screen. It counts for
  this branch only if the same candidate also lowers the effective coefficient
  in the frozen full-pairing estimate for `I_p^far`; otherwise it is
  NS-specific branding without endpoint-level leverage."

### 4. Final Step-009 verdict

- [VERIFIED] Step-009 asked for one exact endpoint, one contradiction line, one
  literal cash-out, one currency, one threshold, and the two admission rules
  before any tensor packaging or observable screening could proceed.
- [VERIFIED] Explorations 001 and 002 already fixed the endpoint ledger,
  contradiction line, cash-out inequality, currency, and threshold on the
  inherited `I_p^far` pairing.
- [INFERRED] This exploration has now fixed the two required admission rules in
  endpoint-specific form without reopening that ledger.
- [VERIFIED] No Step-009 kill condition remains unaddressed at the endpoint
  gate: the setup is concrete enough to front-load prior-art overlap and
  equivalent-packaging screening next.
- [VERDICT] `endpoint frozen, proceed to prior-art and packaging screening`

### 5. What is frozen now, and what later steps may still vary

- [VERIFIED] Already frozen:
  the theorem ledger
  (inherited suitable-weak / Leray-Hopf plus LEI, CKN/Lin contradiction line),
  the live endpoint object
  (`I_p^far = -∬ p_far div(v_k phi_k^2 e_hat)`),
  the cash-out shape
  (`|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}` on the full pairing),
  the progress currency
  (coefficient shrinkage on that same pairing),
  the minimum threshold
  (uniform positive-margin shrinkage after later debt),
  the same-scale immediate-failure rule,
  and the Tao rule.
- [VERIFIED] Later steps may still vary:
  which mechanism family survives prior-art and equivalent-packaging screening,
  which exact tensor package is chosen,
  which observable is promoted,
  which averaged-model comparator is used,
  and the exact reconstruction/localization bookkeeping.
- [INFERRED] None of those later choices may renegotiate the frozen endpoint,
  replace the full `I_p^far` pairing with a surrogate, weaken the coefficient
  shrinkage currency, or treat Tao sensitivity as a substitute for the frozen
  endpoint gain.

### 6. Where the kill condition fires if the setup fails

- [VERIFIED] If Step-009 had failed to freeze one exact endpoint-complete
  ledger, the branch was required to die at the Step-1 endpoint gate before any
  tensor packaging or observable screening.
- [INFERRED] That Step-009 endpoint-gate kill does not fire on the present
  record, because the ledger and both admission rules can now be stated
  concretely.
- [VERIFIED] The next live kill locations are later in the frozen chain:
  Step 2 may stop the branch if no prior-art-screened candidate shrinks the
  same bad term on the same ledger;
  Step 4 may stop it if a candidate lacks meaningful Tao sensitivity or is only
  packaging-dependent;
  and Step 5 must stop it immediately if full reconstruction leaves an
  uncontrolled same-scale exterior or harmonic remainder in the complete
  `I_p^far` pairing.
- [INFERRED] So the exact kill condition tied to the same-scale rule is:
  failure fires the moment the branch cannot convert the full reconstructed
  `I_p^far` ledger into a positive-margin smaller coefficient. At that point
  the branch stops before tensor packaging can be presented as success.

## Dead Ends / Failed Attempts

- [VERIFIED] I searched the local record for a different theorem endpoint that
  would let the same-scale rule be stated more abstractly than on `I_p^far`.
  None exists on disk with equal support; the only stable ledger is the
  inherited far-field pairing.
- [VERIFIED] I searched for a sharper numeric Step-1 lower bound on `delta`
  beyond "materially smaller" / "positive margin." The repository does not
  freeze one; only the threshold shape is source-backed at Step 1.
- [VERIFIED] I found no source support for letting Tao sensitivity do
  stand-alone analytical work. Every relevant note returns to the same demand:
  name the exact estimate and coefficient that become smaller.

## Conclusion

- [VERIFIED] The same-scale admission rule can and should now be frozen in
  exact endpoint language: any later candidate that leaves an uncontrolled
  same-scale exterior/harmonic remainder in the full `I_p^far` pairing fails
  immediately because it has not earned coefficient shrinkage on the frozen
  ledger.
- [VERIFIED] The Tao rule can and should now be frozen in exact endpoint
  language: averaged-model sensitivity is mandatory as a screen, but it does
  not count unless the same candidate also reduces the live coefficient in the
  full `I_p^far` estimate.
- [VERIFIED] The Step-009 outcome is
  `endpoint frozen, proceed to prior-art and packaging screening`.
- [INFERRED] The branch survives Step 1 narrowly. It does not survive by
  admitting any tensor package yet; it survives only because the endpoint,
  gain currency, threshold, and failure rules are now concrete enough to police
  later steps.

## Source Map

### Endpoint, cash-out, currency, and threshold

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-001/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-002/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/exact-surviving-far-field-pairing.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/bad-coefficient-stays-at-fixed-energy-scale.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/real-progress-requires-a-smaller-effective-coefficient.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`

### Same-scale failure rule

- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`
- [VERIFIED] `missions/beyond-de-giorgi/controller/decisions/decision-014.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/judgments/chain-01.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/affine-and-higher-harmonic-modes-survive-as-moments.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/constant-harmonic-mode-is-automatically-killed.md`

### Tao rule

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/judgments/chain-01.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- [VERIFIED] `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] `library/meta/obstruction-screening/when-one-bad-term-and-one-gain-currency-are-frozen-a-tao-screen-may-end-the-branch.md`

### Step verdict and later-step scope

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/controller/decisions/decision-014.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`
