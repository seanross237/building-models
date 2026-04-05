# Exploration 002 Report

## Goal

Write the exact invariant ledger for the frozen package as far as the local
repository supports it, separate exact NS structure from bookkeeping, identify
the theorem-facing bad transfer pattern, and make the Tao screen operational
with one passing and one failing example.

## Method

- Read the Step 11 goal and chain packet to inherit the current freeze.
- Read the Tao canonicalization screen and the exact-NS packet-policy files to
  distinguish exact structure from canonicalization and from substantive model
  changes.
- Read the earlier exact-NS Tao-comparison reports to extract the sharpest
  source-backed energy/helicity transfer claims available locally.
- Search the repository for a standalone dyadic energy/helicity identity sheet.

## Source Log

- `missions/beyond-de-giorgi/steps/step-011/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/selected/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/refined/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/attacks/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/judgments/chain-03.md`
- `runtime/results/codex-patlas-standalone-20260331T182129Z-receptionist-83682.md`
- `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `missions/beyond-de-giorgi/steps/step-011/explorations/exploration-001/REPORT.md`

## Findings

### 1. Frozen setup inherited from the local Step-11 record

- `[VERIFIED]` The current Step-11 record does not support a fully earned
  scope lock, but it does support one narrowed provisional setup:
  `stretching/enstrophy bottleneck` +
  `dyadic coupled fluxes` +
  `role-labeled helical packet Tao screen`.
- `[VERIFIED]` The dyadic package freeze is still indirect: the repository does
  not already contain a standalone dyadic energy/helicity identity memo.
- `[INFERRED]` Because of that gap, the sharpest exact ledger available locally
  is not a pre-tabulated shell formula. It is the exact Fourier/Leray law plus
  the helical-triad conservation constraints, with any dyadic shell ledger
  obtained by aggregating those exact packet-complete triad transfers.

### 2. Exact ledger

#### 2.1 Exact NS starting law

- `[VERIFIED]` The exact on-disk nonlinear law is

```text
∂t û(k) + |k|^2 û(k)
  = -i ∑_{p+q=k} (q · û(p)) P_k û(q),
P_k = I - (k ⊗ k)/|k|^2,
û(-k) = overline{û(k)}.
```

- `[VERIFIED]` This already fixes three structural facts that matter for the
  invariant ledger:
  1. all transfer occurs through exact triads `p + q = k`;
  2. target-mode coupling is filtered by the exact Leray projector `P_k`;
  3. real-valuedness forces conjugate completion.

#### 2.2 Sharpest exact energy/helicity transfer identities supported locally

- `[VERIFIED]` The exact-NS comparison packet states that in a helical triad
  the three modal equations share one cyclic geometric coefficient pattern and
  that those coefficients are constrained by energy and helicity conservation.
- `[INFERRED]` The most honest exact ledger therefore lives at packet-complete
  helical-triad level. For each canonically fixed helical triad packet `τ`,
  there are exact modal energy-transfer entries and exact modal
  helicity-transfer entries whose triad sums vanish:

```text
Σ_{κ in τ} T^E_τ(κ) = 0,
Σ_{κ in τ} T^H_τ(κ) = 0.
```

- `[INFERRED]` This is the sharpest formula-level statement the local packet
  licenses without importing an external helical-amplitude sheet. The record
  supports the conservation constraints and coefficient rigidity, but not a
  standalone on-disk table of the exact helical amplitude formulas.

#### 2.3 What the provisional dyadic package adds

- `[INFERRED]` The provisional `dyadic coupled fluxes` package is an
  aggregation of the exact triad ledger by shell labels, not a new invariant.
- `[INFERRED]` Concretely: once one fixes a dyadic shell assignment and a
  canonically represented packet, each dyadic energy or helicity flux entry is
  obtained by summing the exact triad-level transfer entries over all packets
  whose roles land in the chosen shell pattern.
- `[VERIFIED]` The repository repeatedly warns that a dyadic or helical
  presentation can make the joint energy/helicity picture look richer than it
  is. So the dyadic presentation counts as honest only if it is treated as a
  reindexing of the exact triad ledger rather than as a new structural gain.

#### 2.4 Exactness verdict for the ledger

- `[VERIFIED]` Exact NS structure on disk:
  the Fourier/Leray law, triad-by-triad transfer geometry, cyclic
  energy/helicity conservation constraints, exact projection, and real-valued
  conjugate completion.
- `[INFERRED]` Exactness claim that is justified for this exploration:
  the frozen package has an exact underlying helical-triad ledger, and the
  provisional dyadic coupled-flux package is exact only as an aggregation of
  that ledger.
- `[VERIFIED]` The local record does not support any stronger claim such as a
  pre-frozen coercive dyadic identity or a theorem-facing one-sided flux law.

### 3. Bookkeeping choices

#### 3.1 Exact structure versus bookkeeping

- `[VERIFIED]` Exact structure:
  the triad relation `p + q = k`,
  the exact Leray projector,
  the reality constraint,
  and the energy/helicity conservation constraints on the helical-triad
  coefficients.
- `[VERIFIED]` Canonicalization choices that must be frozen but are not new
  invariants:
  conjugate representatives,
  helical basis convention,
  role-label order,
  amplitude normalization anchor,
  phase anchor,
  and one explicit helical sign sheet.
- `[VERIFIED]` Substantive model changes, not harmless bookkeeping:
  regrouping modes into different packets,
  changing support semantics,
  treating conjugate completion as optional,
  retuning thresholds,
  changing time windows,
  or changing the helical sign sheet after the fact.

#### 3.2 Honest bookkeeping verdict for this branch

- `[INFERRED]` Choosing `dyadic coupled fluxes` instead of a coarse-grained
  balance law is a package choice, not a new invariant identity.
- `[INFERRED]` Restricting attention to favorable same-helicity sectors is also
  bookkeeping unless one proves that the packet-complete sector carries a
  quantitatively relevant share of the full stretching/enstrophy burden.
- `[VERIFIED]` The branch's strongest Tao-sensitive content therefore does not
  live in generic energy/helicity flux language. It lives in packet-complete
  role bookkeeping with mandatory conjugate completion, explicit sign/phase
  sheets, and spectator-coupling discipline.

### 4. Named bad transfer pattern

- `[VERIFIED]` The frozen burden family is
  `stretching/enstrophy bottleneck`, and the chain requires one named bad term
  or bad transfer pattern in that burden language.
- `[INFERRED]` The most honest named target supported by the local packet is
  not a direct one-sided inequality on stretching production. It is the
  Tao-style shell-bridging transfer pattern that would have to feed that
  bottleneck:
  an isolated delayed-threshold packet transfer with
  weak pump,
  tiny trigger,
  strong amplifier/rotor response,
  and delayed next-stage shell pump,
  while spectator channels remain lower order.
- `[INFERRED]` This is the right target because the repository's strongest
  exact-NS evidence is about transfer-pattern non-isolability:
  geometry-fixed coefficient rigidity,
  mandatory conjugate completion,
  and unavoidable spectator couplings,
  not about a direct coercive inequality on `ω · ∇u · ω`.
- `[VERIFIED]` The record still does not justify a stronger theorem-facing
  claim such as “the exact ledger directly controls stretching production.”
  On current evidence the ledger is exact, but not coercive.

### 5. Tao screen

#### 5.1 Operational comparison statement

- `[VERIFIED]` The local canonicalization screen says a family counts as
  Tao-like only if, after canonicalization, it retains:
  identifiable five roles,
  the ordered delayed-threshold sequence,
  a real dominant-channel hierarchy,
  tight sign/phase bookkeeping,
  and bounded spectator leakage on a declared time window.

- `[INFERRED]` For this chain, a candidate feature `F` counts as
  `destroyed by averaging` exactly when all of the following hold:
  1. `F` survives true exact symmetries and one fixed canonical packet sheet;
  2. `F` depends on exact-NS constraints that come from the real triad law,
     namely geometry-fixed coefficients, exact projection, mandatory conjugate
     completion, or unavoidable spectator couplings;
  3. once those exact constraints are replaced by Tao-style averaged circuit
     freedoms, `F` disappears because the delayed-threshold circuit can be
     retuned independently.

- `[INFERRED]` A candidate does **not** count as destroyed by averaging if the
  difference from Tao can be produced merely by:
  shell regrouping,
  helical sign-sheet drift,
  packet re-labeling,
  same-helicity filtering,
  or any other change already classified as bookkeeping or substantive
  re-modeling rather than exact NS structure.

#### 5.2 Why this comparison is concrete enough

- `[VERIFIED]` The canonicalization packet explicitly separates:
  true symmetries,
  fixed canonicalization choices,
  and substantive model changes.
- `[INFERRED]` That separation makes the phrase `destroyed by averaging`
  concrete:
  it means loss under a substantive change from exact NS packet constraints to
  Tao-style averaged circuit freedoms, not loss under a mere rewrite.

### 6. Passing Tao-calibration example

- `[INFERRED]` Passing example:
  the exact role-labeled helical packet with mandatory conjugate completion,
  fixed sign/amplitude/phase sheet, and the exact-NS triadic rigidity /
  spectator-coupling mismatch identified in
  `atlas-anatomy-exploration-002-REPORT.md`.

- `[VERIFIED]` Why it passes:
  the exact-NS packet comparison says Tao needs independently tunable weak
  pump, tiny seed, strong amplifier, stronger rotor, and next-stage pump,
  together with unusually suppressed spectator channels.
  Exact NS instead gives one rigid quadratic law with geometry-fixed helical
  coefficients, exact projection, and forced extra couplings.

- `[INFERRED]` Screen result:
  this is a real NS-sensitive feature destroyed by averaging.
  Tao-style averaging removes the exact coupling rigidity and near-forces the
  desired role hierarchy by construction.
  The difference is therefore structural, not decomposition shopping.

### 7. Failing Tao-calibration example

- `[INFERRED]` Failing example:
  generic same-helicity or shell-model folklore that talks about favorable
  forward energy/helicity transfer in a sparse or polarized sector without
  packet-complete role labels, fixed sign/phase sheet, or an admissible
  spectator-leakage rule.

- `[VERIFIED]` Why it fails:
  the Tao screen itself says that a family that is only sparse, multiscale, or
  triad-engineered but lacks the delayed-threshold role package should not
  count as Tao-like.
  The Chain-03 attack and judgment packet also warn that same-helicity or
  polarized sectors are prior-art-adjacent and do not count unless they carry a
  theorem-relevant burden share.

- `[INFERRED]` Screen result:
  this candidate does not exhibit an NS-sensitive feature that Tao averaging
  destroys.
  It survives only as packaging or favorable-sector folklore, so it fails the
  branch-local Tao screen.

### 8. Is the Tao screen operational now?

- `[INFERRED]` Yes, at the calibration level required for this chain's Step 1.
  The two examples separate:
  1. exact packet-complete NS structure that Tao averaging genuinely removes;
  2. prior-art-adjacent packaging that only sounds special until canonicalized.

- `[VERIFIED]` No stronger conclusion follows.
  The screen is operational as an admission/rejection filter.
  It is **not** itself a coercive gain, a baseline improvement, or an endpoint
  bridge.

### 9. Exploration verdict

- `[VERIFIED]` The strongest exact ledger available locally is
  dyadic/helical only through an exact helical-triad core.
- `[VERIFIED]` The Tao-sensitive feature supported on disk is packet-level
  role-labeled helical coupling with mandatory conjugate completion and frozen
  packet-sheet data, not generic energy/helicity flux language.
- `[VERIFIED]` The ledger remains exact-but-noncoercive on the present record.
- `[INFERRED]` This exploration therefore improves the branch as a calibrated
  obstruction setup, not as a positive mechanism dossier.

## Dead Ends / Failed Attempts

- `[VERIFIED]` Repository search did not find a standalone exact dyadic
  energy/helicity identity sheet for this branch.
- `[VERIFIED]` Repository search did not find a source-backed one-sided
  stretching/enstrophy inequality attached to the coupled ledger.
- `[INFERRED]` Because of those gaps, the dyadic package can be written
  honestly only as an aggregation of the exact helical-triad ledger, and the
  bad transfer pattern can be named honestly only at the Tao-comparison level,
  not yet as a direct theorem inequality.

## Provisional Conclusion

- `[VERIFIED]` The exploration succeeds in making the Tao screen operational:
  one packet-complete exact-NS example passes the discriminator and one
  same-helicity / shell-folklore example fails it.
- `[VERIFIED]` The exploration does **not** upgrade the branch past the
  non-coercivity warning.
- `[INFERRED]` Best current label:
  `exact ledger recovered only at helical-triad core; Tao screen operational; branch still exact-but-noncoercive on local evidence`.
