# Exploration 001 Summary

## Goal

- `[VERIFIED]` Lock the Step-5 repair sheet for
  `Template-Defect Near-Closure`
  and
  `Windowed Spectator-Leakage Budget`
  using the fixed Step-4 dossier only.

## What Was Tried

- `[VERIFIED]` Read the controlling Step-4 `RESULTS.md` plus the landed anti-
  and pro-dossier artifacts.
- `[CHECKED]` Ran `code/repair_sheet_lock.py` and saved the checked output in
  `code/repair_sheet_lock.txt` to compute friendly maxima, removed slack, and
  exact hostile-side gaps where the record supports them.

## Outcome

- `[CHECKED][INFERRED]` `Template-Defect Near-Closure` repairs to
  `lambda_tmpl = 1/4`
  and
  `lambda_spec = 49/256`.
- `[CHECKED][INFERRED]` `Windowed Spectator-Leakage Budget` repairs to
  `Lambda_tot = 1/4`,
  `Lambda_mirror = 1/12`,
  `Lambda_companion = 1/12`,
  `Lambda_feedback = 1/16`,
  while
  `Lambda_cross = 1/12`
  remains unchanged.

## Verification Scorecard

- `[VERIFIED]` Inherited Step-4 statuses were confirmed:
  both candidates enter Step 5 as `survives`.
- `[COMPUTED]` Friendly maxima were extracted exactly from the recorded
  witnesses:
  `Delta_tmpl = 1/4`,
  `Delta_spec = 49/256`,
  `L_tot = 1/4`,
  `L_mirror = 1/12`,
  `L_companion = 1/12`,
  `L_feedback = 1/16`,
  `L_cross = 1/24`.
- `[CHECKED]` Exact hostile-side gaps are on record for
  `lambda_spec`,
  `Lambda_tot`,
  `Lambda_mirror`,
  `Lambda_companion`,
  and
  `Lambda_feedback`.
- `[CHECKED]` The hostile-side `Delta_tmpl` margin is only symbolic
  (`1/2 - O(delta)`), and the hostile-side `L_cross` entry is only `delta`,
  so those two entries cannot be overclaimed.

## Key Takeaway

- `[CHECKED]` The only honest Step-5 repair is to remove threshold slack that
  the Step-4 dossier actually measured, while leaving untouched any entry for
  which the hostile-side gap was not landed on the frozen packet sheet.

## Proof Gaps Or Computation Gaps

- `[CHECKED]` Step 4 does not land one exact hostile numerical margin for
  `Delta_tmpl`.
- `[CHECKED]` Step 4 does not land one uniform hostile cross-class overload gap
  above the friendly `L_cross = 1/24` ceiling.

## Unexpected Findings

- `[VERIFIED]` One narrower landed anti-dossier note underspecifies the hostile
  template/leakage arithmetic, so Step 5 must treat final Step-4 `RESULTS.md`
  as the controlling branch record.
