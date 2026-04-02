# Step 5 Results - Revised Shortlist After One Honest Repair Pass

## Completion Status

- Step complete: **yes**
- Kill condition fired: **no**
- Branch status: **Chain Step 6 is now well posed**
- `[INFERRED]` Honest summary:
  after one repair pass on the frozen Step-4 dossier,
  repaired `Template-Defect Near-Closure`
  and repaired `Windowed Spectator-Leakage Budget`
  survive as the final shortlist,
  while the behavior route is closed:
  `pre-trigger delay filter`
  is discarded as
  `not useful for the target theorem or counterexample question`,
  and
  `next-stage transfer-start filter`
  is discarded as
  `not well-defined`.
- `[VERIFIED]` Operational note:
  the required receptionist, explorer, and curator launches were all attempted
  through the repository-local wrappers;
  the receptionist and all three explorer runs failed to land usable sentinels
  within bounded waits, so the exploration reports were completed directly from
  the anchored local record;
  all three curator handoffs were launched, but no receipt files had landed by
  the time this step result was written.

## Repair Ledger

### 1. `Template-Defect Near-Closure`

- `[VERIFIED]` Inherited Step-4 status:
  `survives`.
- `[VERIFIED]` Only allowed repair:
  tighten
  `lambda_tmpl`
  and
  `lambda_spec`
  using only the already-recorded Step-4 anti/pro margins.
- `[VERIFIED]` Exact Step-4 evidence used:
  - `F_SS(1/12)` has
    `Delta_tmpl = 1/6`,
    `Delta_spec = 1/6`.
  - `F_SL(1/16)` has
    `Delta_tmpl = 1/4`,
    `Delta_spec = 49/256`.
  - `F_DT(delta, eta)` already fails on the same frozen ledger by
    late rotor / next-shell collapse.
- `[INFERRED]` Threshold update:

  ```text
  lambda_tmpl: 1/3 -> 1/4
  lambda_spec: 1/4 -> 49/256
  ```

- `[INFERRED]` Justification:
  the old sheet left unused friendly-side slack

  ```text
  1/3 - 1/4    = 1/12
  1/4 - 49/256 = 15/256
  ```

  and no recorded friendly witness needs more than the repaired values.

### 2. `Windowed Spectator-Leakage Budget`

- `[VERIFIED]` Inherited Step-4 status:
  `survives`.
- `[VERIFIED]` Only allowed repair:
  tighten
  `Lambda_tot`
  and the class budgets using only the already-recorded Step-4 gap.
- `[VERIFIED]` Exact Step-4 evidence used:
  - `F_SS(1/12)` has

    ```text
    L_tot       = 1/4
    L_mirror    = 1/12
    L_companion = 1/12
    L_feedback  = 1/24
    L_cross     = 1/24
    ```

  - `F_SL(1/16)` has

    ```text
    L_tot       = 49/256
    L_mirror    = 1/16
    L_companion = 1/16
    L_feedback  = 1/16
    L_cross     = 1/256
    ```

  - `F_DT(delta, eta)` carries the hostile class ledger recorded in the final
    Step-4 dossier:

    ```text
    int_I D_mirror     = 1/8
    int_I D_companion  = 1/6
    int_I D_feedback   = 1/6
    int_I D_cross      = delta
    ```

    and is already marked there as failing by classwise leakage overload.
- `[INFERRED]` Threshold update:

  ```text
  Lambda_tot:       3/8  -> 1/4
  Lambda_mirror:    1/8  -> 1/12
  Lambda_companion: 1/12 -> 1/12
  Lambda_feedback:  1/12 -> 1/16
  Lambda_cross:     1/12 -> 1/24
  ```

- `[INFERRED]` Justification:
  the old sheet left unused friendly-side slack in every budget except
  `Lambda_companion`.
  `Lambda_companion` cannot tighten further without ejecting `F_SS(1/12)`,
  which already saturates it.

### 3. `Delayed-Threshold Itinerary`

- `[VERIFIED]` Inherited Step-4 status:
  `remains ambiguous`.
- `[VERIFIED]` Only allowed repair:
  split into
  `pre-trigger delay filter`
  and
  `next-stage transfer-start filter`,
  or discard if the split cannot remove the `F_SL(rho)` ambiguity without
  changing the window or threshold language.
- `[PROPOSED]` Resulting notion 1:
  `pre-trigger delay filter`.
  It isolates the early ambiguity question:
  can the frozen packet keep the trigger below `theta_C` until a delayed
  activation time `t_trig` after the clock event, while the spectator ratio
  stays below `Lambda_itin` on `[0, t_trig]`?
- `[PROPOSED]` Resulting notion 2:
  `next-stage transfer-start filter`.
  It would isolate the late ambiguity question:
  can the frozen packet carry the rotor-to-next-stage transfer logic on the
  same event language after `t_rot`?
- `[INFERRED]` Split verdict:
  `pre-trigger delay filter`
  is exact but too weak to justify a separate Step-6 object freeze, so it is
  discarded as
  `not useful for the target theorem or counterexample question`;
  `next-stage transfer-start filter`
  is discarded as
  `not well-defined`
  because the `F_SL(rho)` ambiguity cannot be removed without changing the
  late-stage event language after outcomes are known.

## Revised Candidate Dossier

| Candidate | Exact criterion and downstream gate on the frozen sheet | Step-4 dossier under the repaired criterion | Status |
| --- | --- | --- | --- |
| Repaired `Template-Defect Near-Closure` | `[VERIFIED]` `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)` with repaired sheet `Delta_tmpl <= 1/4`, `Delta_spec <= 49/256` | `[VERIFIED]` `F_SS(1/12)` passes; `[VERIFIED]` `F_SL(1/16)` passes at the new boundary; `[VERIFIED]` `F_DT(delta, eta)` remains a hostile failure by late rotor / next-shell collapse | `survives` |
| Repaired `Windowed Spectator-Leakage Budget` | `[VERIFIED]` `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)` with repaired budgets `(1/4, 1/12, 1/12, 1/16, 1/24)` | `[VERIFIED]` `F_SS(1/12)` and `F_SL(1/16)` still pass on the fixed ledger; `[VERIFIED]` `F_DT(delta, eta)` remains the hostile overload family | `survives` |
| `Pre-trigger delay filter` | `[PROPOSED]` early itinerary gate `G_pre(P_n; I) = (t_clk, t_trig, max_{[0, t_trig]} D_off / D_on; sign sheet)` using the same `theta_B`, `theta_C`, and `Lambda_itin` | `[VERIFIED]` `F_DT(delta, eta)` fails by `t_trig > 1`; `[VERIFIED]` `F_SS(1/12)` and `F_SL(1/16)` pass the early-stage screen | `discarded` |
| `Next-stage transfer-start filter` | `[PROPOSED]` no honest exact gate survives on the frozen late-stage language | `[VERIFIED]` `F_SL(rho)` still lacks a uniformly fixed exact `t_next` trace; `[VERIFIED]` any weaker late-stage notion would change the event language after outcomes are seen | `discarded` |

## Three-Axis Classification Table

| Candidate | Precision | Why | Robustness | Why | Usefulness | Why | Earned negative bucket |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Repaired `Template-Defect Near-Closure` | `high` | one exact two-coordinate observable with repaired cutoffs and no free retuning left | `high` | the Step-3 `stable after canonicalization` verdict survives because the repair changes only unused slack | `medium` | the gate is concrete and exact, but its theorem-facing action is weaker than the leakage screen | none |
| Repaired `Windowed Spectator-Leakage Budget` | `high` | one exact classwise sheet on one fixed interaction currency | `high` | the Step-3 `stable after canonicalization` verdict survives because the class partition and window are unchanged | `high` | it remains the clearest same-currency obstruction/admissibility gate | none |
| `Pre-trigger delay filter` | `high` | the early-stage event language is exact and fully frozen | `medium` | it stays tied to the same finite-window sheet, but only as an admission filter | `low` | it does not cash out in a stronger theorem/counterexample gate than the two surviving candidates already provide | `not useful for the target theorem or counterexample question` |
| `Next-stage transfer-start filter` | `low` | no frozen exact definition removes the `F_SL` ambiguity | `low` | the notion would require a substantive late-stage rewrite to survive | `low` | without a stable exact definition there is no downstream gate to freeze | `not well-defined` |

## Downstream-Gate Check

### Repaired `Template-Defect Near-Closure`

- `[PROPOSED]` Concrete downstream gate:
  freeze the repaired invariant defect observable

  ```text
  G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)
  ```

  on the admissibility sheet
  `(1/4, 49/256)`.
- `[PROPOSED]` Smallest meaningful carried-forward family:
  `F_SL(1/16)`,
  because it is the worst recorded friendly witness for both repaired defect
  coordinates.
- `[INFERRED]` This gate is honest enough for Step 6 because it names one exact
  observable on one fixed packet family and still separates that friendly
  witness from the hostile `F_DT(delta, eta)` failure mode.

### Repaired `Windowed Spectator-Leakage Budget`

- `[PROPOSED]` Concrete downstream gate:
  freeze the repaired classwise sheet

  ```text
  G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)
  ```

  on the repaired budget vector
  `(1/4, 1/12, 1/12, 1/16, 1/24)`.
- `[PROPOSED]` Smallest meaningful carried-forward stress set:
  the friendly pair
  `F_SS(1/12)`
  and
  `F_SL(1/16)`,
  because together they saturate the repaired classwise sheet more sharply than
  any single recorded friendly family.
- `[INFERRED]` This gate is honest enough for Step 6 because it names the exact
  same burden currency that the hostile `F_DT(delta, eta)` already fails by a
  named classwise overload.

### Rejected Gates

- `[VERIFIED]` `Pre-trigger delay filter` is rejected because its downstream
  gate remains too weak:
  it is only a narrow admission filter with no stronger same-currency cash-out.
- `[VERIFIED]` `Next-stage transfer-start filter` is rejected because its
  supposed gate is not frozen exactly enough to carry forward.

## Step Verdict

- `[VERIFIED]` Chain Step 6 is now well posed.
- `[VERIFIED]` Surviving candidate set:
  repaired `Template-Defect Near-Closure`
  and repaired `Windowed Spectator-Leakage Budget`.
- `[PROPOSED]` Exact object-freeze tasks for Step 6:
  1. Freeze the repaired template-defect object on the canonical packet sheet
     with
     `lambda_tmpl = 1/4`
     and
     `lambda_spec = 49/256`.
  2. Freeze the repaired leakage object on the same canonical packet sheet with
     `Lambda_tot = 1/4`,
     `Lambda_mirror = 1/12`,
     `Lambda_companion = 1/12`,
     `Lambda_feedback = 1/16`,
     `Lambda_cross = 1/24`.
  3. Freeze `F_SL(1/16)` as the carried-forward friendly stress witness for the
     template-defect object.
  4. Freeze the friendly stress set
     `F_SS(1/12)` and `F_SL(1/16)`
     for the leakage object.
  5. Keep `F_DT(delta, eta)` as the hostile comparator on the same frozen
     ledger for both survivors.
- `[VERIFIED]` The branch does **not** stop here.
  No Step-5 kill condition fires:
  two candidates survive,
  neither depends on Tao's averaged construction,
  the repairs are justified directly from the Step-4 record,
  the itinerary discard is candidate-local rather than branch-fatal,
  and the remaining downstream gates are concrete rather than cosmetic.
