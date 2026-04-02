# Exploration 001 Report - Canonical First-Budget Seed Classification

## Goal

Classify the canonical first-budget seed families for Step 2:
one exact triad orbit as the seed object on the frozen canonical helical
support sheet, modulo the Step-1 equivalence and admissibility rules.

Required questions:

- what counts as an honest one-triad seed once conjugation,
  triad relabeling,
  helical-sign relabeling,
  gauge conventions,
  and canonicalization choices are quotiented;
- which degenerate geometries are excluded because they are not exact active
  triads with nonzero projected interaction coefficient;
- how much sign-family collapse is actually earned from the local record; and
- what canonical catalog Step 2 should enumerate without hidden
  representation choices.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/HISTORY-OF-REPORT-SUMMARIES.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.md`
- `missions/exact-ns-phase-locking-firewall/MISSION.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `library/factual/navier-stokes/exact-support-search-object-is-a-finite-canonical-helical-support-sheet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/recursive-exact-closure-must-use-the-full-active-ledger-and-exact-projected-helical-coefficients.md`
- `library/factual/exact-ns-phase-locking-firewall/coefficient-corrected-triad-phase-orbit-ledger-is-the-best-current-intrinsic-object.md`

## Working Notes

### Initial setup

- Created the report skeleton first, as required.
- Read the Step-2 brief and controller memo to confirm that the current task is
  **seed classification only**, at the first budget only.

### Step-1 freeze extraction

- Re-read the Step-1 result and both relevant exploration reports.
- Confirmed that Step 1 already froze:
  the intrinsic object `Mu_S`,
  the exact search object as finite canonical helical support sheets,
  mandatory conjugate completion,
  recursive exact closure driven by nonzero projected helical coefficients,
  immediate spectator inclusion,
  and the admissible-enlargement policy.

### Coefficient probe

- Added reproducible artifact `code/helical_seed_probe.py`.
- Initial attempt failed because `numpy` is unavailable in this runtime.
- Rewrote the probe in pure stdlib Python and saved latest output to
  `code/helical_seed_probe.txt`.
- The probe records two combinatorial sign partitions:
  ordered sign classes under global sign flip plus `p <-> q`,
  and orbit-level sign classes under global sign flip plus full mode
  permutation.
- It also checks several sample triads:
  three noncollinear examples and one collinear example.

## Findings

### 1. Frozen object and quotient discipline

- `[VERIFIED]` Step 1 froze the Step-2 search object as a **finite canonical
  helical support sheet with mandatory conjugate completion**, not a packet
  family and not bare Fourier support.
  Source:
  `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`,
  `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`,
  `library/factual/navier-stokes/exact-support-search-object-is-a-finite-canonical-helical-support-sheet-with-mandatory-conjugate-completion.md`.
- `[VERIFIED]` Step 1 also froze the admissible quotient layers relevant here:
  triad-orbit relabeling,
  real-valued conjugate completion / mirror representative choice,
  helical-basis sign and phase relabeling,
  gauge / phase-anchor conventions,
  and canonicalization / normalization choices.
  Source:
  `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`,
  `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`.
- `[VERIFIED]` The same local record also says that **different helical sign
  sheets on the frozen basis are different exact objects**.
  So sign collapse is allowed only where the explicit equivalence sheet earns
  it.
  Source:
  `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`.
- `[INFERRED]` Because the current seed object is explicitly **one exact triad
  orbit**, the clean raw seed should be written in the symmetric orbit form

  ```text
  Delta = {a, b, c},
  a + b + c = 0,
  ```

  together with one helical sign assignment
  `(sigma_a, sigma_b, sigma_c)`
  on the frozen canonical sheet.
  This avoids importing a hidden distinguished-output choice too early.

### 2. Honest live geometry versus dead pseudo-triads

- `[VERIFIED]` Step 2 must use the **exact projected helical coefficient law**.
  Only exact active triads with nonzero projected coefficient count as live
  seeds.
  Source:
  `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`,
  `library/factual/navier-stokes/recursive-exact-closure-must-use-the-full-active-ledger-and-exact-projected-helical-coefficients.md`.
- `[INFERRED]` Start from the exact interaction scalar already frozen in the
  Step-1 record:

  ```text
  Gamma_{k,p,q}(u)
    = -i overline{u^(k)} · [ (q · u^(p)) P_k u^(q) ].
  ```

  Choose a triad-plane helical gauge
  `n = (p x q) / |p x q|`
  and

  ```text
  h_sigma(m) = (n x m_hat + i sigma n) / sqrt(2).
  ```

  Then the ordered helical coefficient factorizes as

  ```text
  C_(k,p,q; sigma_k,sigma_p,sigma_q)
    propto (q · h_(sigma_p)(p))
            (h_(sigma_k)(k)^* · h_(sigma_q)(q)),
  ```

  with

  ```text
  q · h_(sigma_p)(p) = |p x q| / (sqrt(2) |p|),
  h_(sigma_k)(k)^* · h_(sigma_q)(q)
    = (k_hat · q_hat + sigma_k sigma_q) / 2.
  ```

  For a noncollinear triad,
  `|p x q| > 0`
  and
  `|k_hat · q_hat| < 1`,
  so this coefficient is nonzero for every sign choice.
  By `p <-> q`, the same conclusion holds from the other ordered presentation.
- `[VERIFIED]` The direct probe in `code/helical_seed_probe.py` matches that
  conclusion:
  the three noncollinear sample triads give `8/8` nonzero raw sign triples,
  while the collinear sample gives `0/8`.
- `[INFERRED]` Therefore an **honest live one-triad seed geometry** is exactly:
  a nonzero exact lattice triad orbit
  `Delta = {a, b, c}`,
  `a + b + c = 0`,
  with
  `a x b != 0`
  (equivalently: three nonzero wavevectors, not all collinear).
- `[INFERRED]` The following pseudo-triads are excluded already at seed
  admission:
  1. any zero-mode case such as `p = -q`, `k = p`, or `k = q`;
  2. any repeated-wavevector case such as `p = q`, because then the exact
     triple is collinear (`k = 2p`);
  3. any other collinear exact triple.
- `[INFERRED]` Near-collinear families are **not** excluded at this stage.
  They may be badly conditioned later, but they are still exact active triads
  whenever the area is nonzero.

### 3. Sign-family collapse actually earned

- `[INFERRED]` The direct coefficient check shows that **nondegenerate geometry
  kills no helical sign sector** at the one-triad level:
  every raw sign triple is active once the geometry is noncollinear.
- `[INFERRED]` The local record earns only two sign collapses for seed
  classification:
  1. **global helical-sign relabeling / basis rename**:
     `(sigma_a, sigma_b, sigma_c) ~ (-sigma_a, -sigma_b, -sigma_c)`;
  2. **triad-orbit relabeling**:
     the three orbit positions may be permuted without changing the seed.
- `[INFERRED]` A useful intermediate check is the target-ordered bookkeeping
  view `k = p + q`.
  There, after only global sign flip and `p <-> q`, the raw `2^3` sign triples
  collapse to **three ordered classes**:
  1. `+++, ---`
  2. `+--, -++`
  3. `++-, +-+, -+-, --+`
  The probe writes this partition explicitly under
  `ordered-sign classes`.
- `[INFERRED]` But the Step-2 seed object is **not** one ordered interaction
  term.
  It is **one exact triad orbit**.
  Once full orbit relabeling is applied, the two ordered heterochiral classes
  above are the same orbit family.
  So the honest orbit-level sign catalog has exactly **two** and only two live
  families:
  1. **homochiral**:
     all three helical signs equal, modulo global sign relabeling;
  2. **heterochiral**:
     exactly one sign differs, modulo global sign relabeling and mode
     permutation.
- `[INFERRED]` This is the sharp collapse verdict:
  Step 2 has earned **more than zero collapse but less than total collapse**.
  It should enumerate **two orbit-level sign families**, not one and not
  three.
  One family would silently identify homochiral and heterochiral sheets;
  three families would smuggle in an ordered-target representation choice that
  the seed object itself does not keep.

### 4. Canonical first-budget seed catalog

- `[INFERRED]` An honest first-budget seed is therefore a pair

  ```text
  ([Delta], Sigma),
  ```

  where:
  1. `[Delta]` is a canonical representative of an **unordered noncollinear
     exact lattice triad orbit** on the frozen helical sheet,
     written symmetrically as `a + b + c = 0`,
     modulo conjugation and triad-orbit relabeling;
  2. `Sigma` is one of the two orbit-level helical sign families:
     `homochiral` or `heterochiral`.
- `[INFERRED]` Conjugate completion belongs in the support ledger immediately,
  but it is bookkeeping, not a separate seed family.
  Source:
  `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`,
  `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`.
- `[INFERRED]` The first-budget catalog Step 2 should enumerate is therefore:

  ```text
  all canonical noncollinear exact one-triad lattice orbits
  x
  {homochiral, heterochiral}.
  ```

  No further sign collapse is earned from the local record,
  and no live sign family may be dropped at seed-admission time.
- `[INFERRED]` If the Step-2 implementation prefers an ordered representative
  `k = p + q`, that is acceptable only as a **canonicalization layer**.
  The extra split between
  `+-- / -++`
  and
  `++- / +-+ / -+- / --+`
  is then bookkeeping for coefficient tables, not a distinct seed-family
  distinction.

### 5. Classification answer

- `[INFERRED]` **Honest one-triad seed:**
  one noncollinear exact lattice triad orbit on the frozen canonical helical
  sheet, with one orbit-level sign family
  (`homochiral` or `heterochiral`),
  modulo conjugation,
  triad-orbit relabeling,
  global sign relabeling,
  and the frozen gauge / canonicalization conventions.
- `[INFERRED]` **Excluded degeneracies:**
  zero-mode pseudo-triads,
  repeated-wavevector cases that force collinearity,
  and all collinear exact triples.
- `[INFERRED]` **Earned sign collapse:**
  raw `8` sign assignments
  -> `3` ordered classes under global sign flip plus `p <-> q`
  -> `2` honest orbit-level seed families after full triad-orbit relabeling.
- `[INFERRED]` **Canonical catalog Step 2 should enumerate:**
  canonical representatives of unordered noncollinear exact lattice triad
  orbits, each in exactly two sign families:
  `homochiral`,
  `heterochiral`.

## Failed Attempts / Dead Ends

- `[VERIFIED]` The first direct probe failed because `numpy` is not installed
  in this runtime.
  Replaced it with a pure-stdlib script.
- `[INFERRED]` An initial target-ordered reading suggested three live sign
  families.
  After re-reading the task's seed object as **one exact triad orbit**, not one
  ordered `k = p + q` term, that third-vs-second split was downgraded to a
  representation artifact rather than a true seed distinction.

## Provisional Conclusion

`[INFERRED]` Exploration objective succeeded.
The first-budget seed catalog is sharp:
Step 2 should enumerate **all noncollinear exact one-triad lattice orbits on
the frozen canonical helical sheet, each in exactly two orbit-level sign
families (`homochiral`, `heterochiral`)**.
Collinear / zero-mode / repeated-mode pseudo-triads are excluded at seed
admission because their exact projected coefficient vanishes or the support is
outside the frozen Step-1 class.
