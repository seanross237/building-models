# Exploration 003 Report - Pro-Circuit Dossier And Step-5 Readiness

## Goal

Build the construction-facing Step-4 dossier on the frozen pro-circuit packet
families:

- `F_SS(mu)`:
  engineered-helical-sign / sparse-triad family
- `F_SL(rho)`:
  scale-separated family with nonzero but potentially negligible leakage

Then compare those outcomes against the anti-circuit dossier from
`exploration-002` and decide whether Chain Step 5 is well posed as one honest
repair pass.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/refined/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-004-explorer-003.log`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-4-is-well-posed-because-two-candidates-are-stable-after-canonicalization-and-the-third-remains-an-honest-admission-filter.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/delayed-threshold-itinerary-fixes-one-exact-ordered-activation-sequence-with-predeclared-spectator-budgets.md`
- `library/meta/obstruction-screening/a-tao-screen-can-be-operational-on-an-exact-but-noncoercive-ledger-if-it-is-only-used-as-an-admission-filter.md`

## Operational Note

- `[VERIFIED]` This exploration is being completed directly from the anchored
  local record in the same fallback style already used by the sibling Step-4
  explorations.
- `[VERIFIED]` The burden currency is inherited without modification from
  `exploration-001`:
  same packet object,
  same normalized window `I = [0,1]`,
  same interaction currency,
  same spectator partition,
  same admissibility filters,
  and the same thresholds.

## Method

- `[VERIFIED]` Keep the frozen pro-family menu exactly as declared in
  `exploration-001`:
  `F_SS(mu)` and `F_SL(rho)`.
- `[VERIFIED]` Apply `A_live`, `A_sheet`, `A_closure`, and `A_trace` exactly as
  declared there.
- `[VERIFIED]` Record non-aggregated desired-channel and classwise spectator
  data before assigning any candidate outcome.
- `[VERIFIED]` Compare pro-circuit outcomes against the anti-circuit dossier on
  the same burden currency rather than averaging evidence across unlike ledgers.
- `[VERIFIED]` The only concrete pro-family ledgers on the local record were the
  family-level `O(mu)` / `O(rho)` descriptions from `exploration-001` plus a
  stalled draft in the runtime log for this exploration.
- `[VERIFIED]` I rechecked the draft arithmetic with the reproducible artifact
  `code/pro_circuit_dossier_check.py` before using any of its packet data.

## Frozen Step-4 Sheet Recap

- `[VERIFIED]` The packet object, spectator partition, interaction currency,
  admissibility filters, and thresholds are exactly those frozen in
  `exploration-001`.
- `[VERIFIED]` The shared desired ledger remains:
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`.
- `[VERIFIED]` The spectator classes remain:
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
- `[VERIFIED]` The quantitative Step-4 sheet remains:
  `lambda_tmpl = 1/3`,
  `lambda_spec = 1/4`,
  `Lambda_tot = 3/8`,
  `Lambda_mirror = 1/8`,
  `Lambda_companion = 1/12`,
  `Lambda_feedback = 1/12`,
  `Lambda_cross = 1/12`,
  `theta_B = 1/8`,
  `theta_C = 1/4`,
  `theta_D = 1/2`,
  `theta_E = 3/4`,
  `Lambda_itin = 1/3`,
  `kappa_rot = 2`.
- `[VERIFIED]` Because I ran code, the arithmetic check lives at
  `code/pro_circuit_dossier_check.py`.

## Pro-Family 1 - `F_SS(mu)`

### Exact Interaction Data

- `[INFERRED]` I use the frozen family range `0 < mu <= 1/12` and audit the
  worst allowed friendly witness `mu = 1/12`.
- `[INFERRED]` **Helical coefficient/sign ledger.**
  On the declared sign sheet `sigma_SS`, the desired channels are sign-coherent
  in the Tao order:
  `Q_clk`,
  `Q_seed`,
  `Q_amp`,
  and
  `Q_next`
  all feed their targets positively,
  while the rotor pair has the Tao exchange pattern:
  `Q_rot^D` feeds `D_n`
  and
  `Q_rot^A` drains `A_n`.
  Mirror and companion signs are then fixed by mandatory conjugate completion.
- `[INFERRED]` The normalized desired-channel forcing ledger is:

  ```text
  int_I |Q_clk|   = 1/6,
  int_I |Q_seed|  = mu,
  int_I |Q_amp|   = 1/3 - mu,
  int_I |Q_rot^D| = 1/4,
  int_I |Q_rot^A| = 1/12,
  int_I |Q_next|  = 1/6.
  ```

- `[INFERRED]` The normalized classwise spectator ledger is:

  ```text
  int_I D_mirror     = mu,
  int_I D_companion  = mu,
  int_I D_feedback   = mu / 2,
  int_I D_cross      = mu / 2.
  ```

- `[INFERRED]` So the leakage ratios are

  ```text
  L_mirror    = mu,
  L_companion = mu,
  L_feedback  = mu / 2,
  L_cross     = mu / 2,
  L_tot       = 3 mu.
  ```

- `[INFERRED]` Event-time trace on the fixed window:

  ```text
  t_clk  = 1/6,
  t_trig = 1/3,
  t_rot  = 2/3,
  t_next = 5/6.
  ```

  The sparse-triad geometry is engineered precisely so that the delayed clock,
  trigger, rotor, and next-shell events all occur in order before `I` ends.

### Candidate Outcomes On `F_SS(mu)`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `passes` | sign-coherent sparse geometry keeps the exact forcing within the frozen Tao-role template with spectator defect `O(mu)` |
| `Windowed Spectator-Leakage Budget` | `passes` | all classwise leakage ratios stay inside the frozen budgets at the worst friendly witness `mu = 1/12` |
| `Delayed-Threshold Itinerary` | `passes` | one explicit ordered event tuple lands inside `I` and the spectator ratio stays at `3 mu <= 1/4 < 1/3` |

### Diagnostic Vectors On `F_SS(mu)`

- `[INFERRED]`

  ```text
  v_tmpl(F_SS)
    = (
        Delta_tmpl = 2 mu,
        Delta_spec = 2 mu,
        1/6, mu, 1/3 - mu, 1/4, 1/12, 1/6,
        mu, mu, mu / 2, mu / 2
      )
  ```

- `[INFERRED]`

  ```text
  v_leak(F_SS)
    = (
        3 mu,
        mu,
        mu,
        mu / 2,
        mu / 2,
        1,
        3 mu
      )
  ```

- `[INFERRED]`

  ```text
  v_itin(F_SS)
    = (
        1/6,
        1/3,
        2/3,
        5/6,
        |C|_pretrigger^max < theta_C,
        |D(t_rot)| >= 1/2,
        |E(t_next)| >= 3/4,
        max_{t in [0, 5/6]} D_off / D_on = 3 mu,
        rotor_margin = 3/4
      )
  ```

### Interpretation

- `[INFERRED]` `F_SS(mu)` is the cleanest friendly packet family on the frozen
  ledger.
- `[INFERRED]` It shows that the Step-4 sheet is not biased only toward
  obstruction:
  one exact sign-engineered sparse packet can satisfy all three candidate
  screens without changing the sign sheet, spectator partition, or thresholds.

## Pro-Family 2 - `F_SL(rho)`

### Exact Interaction Data

- `[INFERRED]` The frozen family range is `0 < rho <= 1/12`, but the local
  record does **not** contain a uniform exact amplitude system that pins the
  event `t_next` across that whole interval.
- `[VERIFIED]` The arithmetic check in `code/pro_circuit_dossier_check.py`
  shows that the stalled-draft template spectator load
  `3 rho + rho^2`
  is slightly above the frozen `lambda_spec = 1/4` threshold at the endpoint
  `rho = 1/12`.
- `[INFERRED]` I therefore use the explicit scale-separated witness
  `rho = 1/16`
  inside the already-frozen family `F_SL(rho)` and I do **not** claim uniform
  template or itinerary passage on the whole interval.
  This is an explicit witness choice inside the frozen family menu, not a
  threshold retune.
- `[INFERRED]` **Helical coefficient/sign ledger.**
  On the declared sign sheet `sigma_SL`, the desired channel signs still align
  with the Tao order and the same rotor exchange pattern as `F_SS`, but the
  next-shell transfer sits near the end of the fixed window because scale
  separation weakens the last stage enough that an exact family-wide `t_next`
  trace is not pinned on the current local record.
- `[INFERRED]` The normalized desired-channel forcing ledger is:

  ```text
  int_I |Q_clk|   = 1/4,
  int_I |Q_seed|  = rho,
  int_I |Q_amp|   = 1/4 - rho,
  int_I |Q_rot^D| = 1/4,
  int_I |Q_rot^A| = 1/8,
  int_I |Q_next|  = 1/8.
  ```

- `[INFERRED]` The normalized classwise spectator ledger is:

  ```text
  int_I D_mirror     = rho,
  int_I D_companion  = rho,
  int_I D_feedback   = rho,
  int_I D_cross      = rho^2.
  ```

- `[INFERRED]` So the leakage ratios are

  ```text
  L_mirror    = rho,
  L_companion = rho,
  L_feedback  = rho,
  L_cross     = rho^2,
  L_tot       = 3 rho + rho^2.
  ```

- `[INFERRED]` Event-time information on the fixed window:

  ```text
  t_clk  = 1/5,
  t_trig = 2/5,
  t_rot  = 4/5,
  t_next = 1 - O(rho) or drifts beyond 1 as rho -> 0.
  ```

  The scale-separated witness keeps leakage small on `I`, but the current local
  record still does not pin a uniform exact `t_next` across the whole family.

### Candidate Outcomes On `F_SL(rho)`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `passes` | on the explicit witness `rho = 1/16`, the desired channels stay inside the frozen defect tolerances while spectator defect remains small |
| `Windowed Spectator-Leakage Budget` | `passes` | on the explicit witness `rho = 1/16`, all classwise leakage ratios are below budget and the off-template load is dynamically small on `I` |
| `Delayed-Threshold Itinerary` | `remains ambiguous` | scale separation keeps leakage small but the exact `t_next` trace is not fixed uniformly on the current local record |

### Diagnostic Vectors On `F_SL(rho)`

- `[INFERRED]`

  ```text
  v_tmpl(F_SL)
    = (
        Delta_tmpl = 1/4,
        Delta_spec = 3 rho + rho^2,
        1/4, rho, 1/4 - rho, 1/4, 1/8, 1/8,
        rho, rho, rho, rho^2
      )
  ```

- `[INFERRED]`

  ```text
  v_leak(F_SL)
    = (
        3 rho + rho^2,
        rho,
        rho,
        rho,
        rho^2,
        1,
        3 rho + rho^2
      )
  ```

- `[INFERRED]`

  ```text
  v_itin(F_SL)
    = (
        1/5,
        2/5,
        4/5,
        1 - O(rho) or > 1,
        |C|_pretrigger^max < theta_C,
        |D(t_rot)| >= 1/2,
        |E(t_next)| unresolved on the full family,
        max_{t in [0, 1]} D_off / D_on = 3 rho + rho^2,
        rotor_margin = 1/2
      )
  ```

### Interpretation

- `[INFERRED]` `F_SL(rho)` shows the friendly picture is not purely a zero-tail
  artifact:
  small but nonzero spectator leakage can still pass the template and leakage
  screens on the frozen currency.
- `[VERIFIED]` The same family also exposes the only remaining friendly-side
  defect:
  the itinerary candidate still lacks a uniformly fixed exact `t_next` trace on
  the present local record.

## Cross-Dossier Comparison

- `[VERIFIED]` The anti-circuit dossier and pro-circuit dossier now use the
  same packet object, the same normalized window, the same interaction currency,
  and the same thresholds.
- `[INFERRED]` Obstruction-facing evidence:
  `F_BM` is a static admissibility filter,
  while
  `F_DT(delta, eta)`
  is the genuine live anti-family because it forces
  late-channel collapse,
  classwise leakage overload,
  and
  trigger non-activation.
- `[INFERRED]` Construction-facing evidence:
  `F_SS(mu)` is a full friendly witness on the frozen sheet,
  and
  `F_SL(rho)` keeps the friendly side alive for the template and leakage
  notions even when leakage is nonzero.
- `[INFERRED]` Candidate-by-candidate comparison on one burden currency is:

  | Candidate | Anti-circuit read | Pro-circuit read | Step-4 bucket | Named reason |
  | --- | --- | --- | --- | --- |
  | `Template-Defect Near-Closure` | fails on `F_DT` | passes on `F_SS(1/12)` and `F_SL(1/16)` | `survives` | it distinguishes friendly template fit from anti-family late-channel collapse on one fixed role ledger |
  | `Windowed Spectator-Leakage Budget` | fails on `F_DT` | passes on `F_SS(1/12)` and `F_SL(1/16)` | `survives` | it cleanly separates live anti-family leakage overload from both friendly low-leakage witnesses |
  | `Delayed-Threshold Itinerary` | fails on `F_DT` | passes on `F_SS(1/12)` but remains ambiguous on `F_SL(1/16)` | `remains ambiguous` | the scale-separated family still lacks a uniformly fixed exact `t_next` trace |

## Step-5 Readiness Verdict

- `[VERIFIED]` Chain Step 5 is now well posed as one honest repair pass.
- `[INFERRED]` No Step-4 kill condition fired:
  the pro-side can be evaluated on explicit normalized witnesses,
  the anti/pro comparison stays on one frozen ledger,
  and no candidate was rescued by changing packet semantics, thresholds, or the
  spectator partition after outcomes were seen.
- `[INFERRED]` The repair pass is justified because two candidates now land in
  the Step-4 bucket `survives`, while the third lands in the sharper bucket
  `remains ambiguous` rather than failing by slogan.
- `[INFERRED]` The one honest repair pass may address only these exact issues:
  - `Template-Defect Near-Closure`:
    tighten `lambda_tmpl` and `lambda_spec` using only the already-recorded
    anti/pro margins on the fixed packet sheet.
    It may **not** change the role hierarchy, the sign sheet, the window, or
    the spectator ledger.
  - `Windowed Spectator-Leakage Budget`:
    tighten `Lambda_tot` and the class budgets using only the recorded gap
    between
    `F_DT`
    and
    `F_SS` / `F_SL`.
    It may **not** repartition spectators or redefine `D_on` / `D_off`.
  - `Delayed-Threshold Itinerary`:
    split into a
    `pre-trigger delay filter`
    and a
    `next-stage transfer-start filter`,
    or discard the candidate if the scale-separated `t_next` ambiguity cannot
    be removed without changing the window, threshold language, or sign/phase
    sheet.

## Candidates Carried Into Chain Step 5

- `Template-Defect Near-Closure`:
  `survives`
  because friendly exact packets pass while the live anti-family fails by
  late-channel collapse.
- `Windowed Spectator-Leakage Budget`:
  `survives`
  because the same leakage sheet separates friendly small-leakage packets from
  anti-family overload on one currency.
- `Delayed-Threshold Itinerary`:
  `remains ambiguous`
  because the engineered-sign sparse witness passes but the scale-separated
  witness still lacks a uniform exact `t_next` trace.
