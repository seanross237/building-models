# Exploration 001 Summary - Canonical Second-Budget Seed Classification

- Goal:
  classify the canonical two-triad shared-mode seed families for the second
  budget under the frozen Step-1 equivalence rules and the Step-2 first-budget
  exclusions.
- What I tried:
  re-read the frozen Step-1 and Step-2 records,
  normalized every connected two-triad shared-mode candidate to a common-input
  form,
  and added reproducible artifact
  `code/shared_mode_seed_catalog.py`
  to classify abstract two-triad overlap types up to relabeling.
- Outcome:
  `succeeded`.
- One key takeaway:
  after quotienting by conjugation and triad-orbit relabeling, the honest
  connected second budget has exactly two genuinely new wavevector families:
  the four-orbit shared parallelogram
  `((p+q), p, q)` with `((p-q), p, -q)`,
  and the five-orbit generic fan
  `((p+q), p, q)` with `((p+s), p, s)` sharing only `[p]`.
- Leads worth pursuing:
  Exploration 002 should run recursive closure on exactly those two canonical
  wavevector families,
  using the existing representative names
  `mirror_parallelogram`
  and
  `generic_fan`
  from the local closure-audit scaffold.
- Unexpected findings:
  several apparently different four-orbit pictures
  (`s=-q`,
  `s=k`,
  `r=q`,
  `r=-k`)
  are not separate families at all;
  they collapse to one abstract intersection-size-2 class once hidden
  representative choices are removed.
- Computations worth doing later:
  the next exploration should compute the first forced new wavevectors and
  sign-sector spill for the two canonical families, rather than redoing seed
  classification or splitting by cosmetic sign-sheet variants.
