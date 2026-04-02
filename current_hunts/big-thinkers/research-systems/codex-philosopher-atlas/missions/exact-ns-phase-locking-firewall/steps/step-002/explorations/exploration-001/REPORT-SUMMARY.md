# Exploration 001 Summary

- Goal:
  classify the canonical first-budget seed families for Step 2:
  one exact triad orbit on the frozen canonical helical support sheet, modulo
  the Step-1 equivalence and admissibility rules.
- What I tried:
  read the Step-2 brief, controller memo, Step-1 result, and the Step-1
  intrinsic-object / exact-search-class reports; re-derived the seed-admission
  test from the exact interaction scalar; and wrote
  `code/helical_seed_probe.py`
  with output saved in
  `code/helical_seed_probe.txt`
  to check raw sign-sector activity on sample triads.
- Outcome:
  `succeeded`.
- One key takeaway:
  the honest first-budget seed catalog is
  **all noncollinear exact one-triad lattice orbits on the frozen canonical
  helical sheet, each in exactly two orbit-level sign families:
  `homochiral` and `heterochiral`**.
- Leads worth pursuing:
  run the closure audit from symmetric orbit representatives
  `Delta = {a,b,c}`,
  `a + b + c = 0`,
  and keep the target-ordered three-class sign split only as later
  coefficient-table bookkeeping, not as a seed-count distinction.
- Unexpected findings:
  ordered bookkeeping `k = p + q` leaves three sign classes after global sign
  flip plus `p <-> q`, but the true orbit-level seed object collapses those to
  two families after full triad relabeling; also, near-collinear triads remain
  live at seed admission as long as the exact projected coefficient is
  nonzero.
- Computations worth doing later if outside scope:
  the next pass should compute recursive closure from the canonical orbit-level
  seeds and, if needed, write an explicit coefficient-transport table showing
  how the ordered sign subclasses map under full triad-orbit relabeling.
