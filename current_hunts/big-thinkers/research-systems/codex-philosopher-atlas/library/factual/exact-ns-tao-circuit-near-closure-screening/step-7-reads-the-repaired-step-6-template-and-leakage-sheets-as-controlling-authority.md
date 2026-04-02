# Step-7 Reads The Repaired Step-6 Template And Leakage Sheets As Controlling Authority

Status: `VERIFIED` repaired-sheet values with `INFERRED` branch-precedence rule

The completed Step-7 exploration treats the repaired Step-6 sheets as the
controlling branch authority:
`G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)` with
`Delta_tmpl <= 1/4` and `Delta_spec <= 49/256`,
and
`G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)` with
`(L_tot, L_mirror, L_companion, L_feedback, L_cross) <= (1/4, 1/12, 1/12, 1/16, 1/24)`.

Those repaired sheets are the only hard pass/fail gates the branch carries
into Step 2.
`t_clk`, `t_trig`, `t_rot`, `t_next`, and stage-order narrative may still be
recorded as diagnostics, but they are not promoted branch gates and cannot
override a failure of repaired `G_tmpl` or repaired `G_leak`.

The primary controlling path on disk is
`missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`.
The Step-6 exploration report and Step-5 result stay supporting freeze paths,
not peer sources that reopen the repaired sheet once the shortlist has
already been frozen.

The main historical variance is the earlier Step-5 exploration draft that
still wrote `Lambda_cross = 1/12`.
Step 7 preserves that value only as part of the drift record.
The controlling authority is the later step-level repair sheet, repeated in
the Step-5 and Step-6 results, where the branch freezes
`Lambda_cross: 1/12 -> 1/24` and therefore carries `L_cross <= 1/24`.

The honest Step-7 precedence rule for this branch is:
step-level result files first, supporting exploration reports second, and
earlier conflicting drafts only as historical variance.
That keeps the branch from turning record mismatch into a fake live threshold
choice.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-007-exploration-001-frozen-witness-and-authority-sheet.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-007-exploration-002-scorecard-guardrails-and-step-2-readiness.md`
