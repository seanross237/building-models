# Exploration 003 Summary

- Goal:
  build the pro-circuit Step-4 dossier on
  `F_SS(mu)`
  and
  `F_SL(rho)`,
  then decide whether Chain Step 5 is well posed as one honest repair pass.
- What I tried:
  read the frozen Step-4 sheet from `exploration-001`,
  compared against the anti-circuit dossier from `exploration-002`,
  recovered the only concrete pro-family ledgers from the stalled local runtime
  draft,
  and rechecked the arithmetic with
  `code/pro_circuit_dossier_check.py`.
- Outcome:
  `succeeded`.
  `Template-Defect Near-Closure` survives,
  `Windowed Spectator-Leakage Budget` survives,
  and
  `Delayed-Threshold Itinerary` remains ambiguous.
- One key takeaway:
  the exact-packet audit is now genuinely balanced on one frozen ledger:
  friendly exact packets exist for the template and leakage screens, but the
  itinerary still stalls on the scale-separated exact `t_next` trace.
- Leads worth pursuing:
  Step 5 may tighten the template-defect and leakage budgets using only the
  recorded anti/pro margins, and may split the itinerary into
  `pre-trigger delay`
  versus
  `next-stage transfer-start`
  filters before deciding whether to discard it.
- Unexpected findings:
  the stalled local draft's family-wide
  `F_SL(rho)`
  template spectator load
  `3 rho + rho^2`
  sits slightly above the frozen `1/4` threshold at the endpoint
  `rho = 1/12`,
  so the positive scale-separated read had to be stated on the explicit witness
  `rho = 1/16`
  rather than claimed uniformly on the full interval.
- Computations worth doing later:
  derive a closed exact amplitude system for the scale-separated family that
  pins `t_next` on the full frozen family,
  and compute the sharp largest
  `rho`
  compatible with the current template sheet
  (`rho_* = (-3 + sqrt(10)) / 2` in the present draft arithmetic).
