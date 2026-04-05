# Strategizer Reasoning

The strategizer will append its execution reasoning here.

## Iteration 1 - Startup and receptionist query design

- Read `GOAL.md`, `state.json`, `HISTORY-OF-REPORT-SUMMARIES.md`,
  `../../CHAIN.md`, and `../../CHAIN-HISTORY.md`.
- Read `../step-005/RESULTS.md` to inherit the frozen architecture:
  `local-energy flux/localization`, the bad term
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`, the solution package, and the
  candidate family
  (`divergence/stress`, `Lamb-vector / Helmholtz-projected`,
  `vorticity transport / Biot-Savart`).
- Immediate step requirement:
  before any estimate ledger, identify for each frozen candidate the exact
  Navier-Stokes-specific feature it claims to use, how Tao-style averaging
  destroys or preserves that feature, and whether that distinction can enter
  the already-fixed localized cutoff-flux balance.
- Repository baseline from direct reads:
  the local record already warns that these rewrites are likely to be
  identity-level or architecture-drifting unless they alter the estimate on
  the localized LEI flux bundle itself.
- Because the step requires fresh explorations, query the receptionist first
  for the strongest local source set on:
  - Tao-style averaged-model constraints relevant to this branch;
  - prior local judgments on Lamb-vector/projected/vorticity rewrites;
  - exact places where localization, projection, Calderon-Zygmund, or
    Biot-Savart debt is expected to erase any purely algebraic advantage;
  - prior-art boundaries relative to the De Giorgi sharpness record, the
    pressure-route negatives, and the killed geometry branch.
- Provisional exploration plan after the receptionist returns:
  - Exploration 001:
    Tao-screen `divergence/stress` and
    `Lamb-vector / Helmholtz-projected`
  - Exploration 002:
    Tao-screen `vorticity transport / Biot-Savart`
  - Exploration 003:
    write the unified admission/rejection verdict and Step-3 recommendation

## Iteration 2 - Receptionist result and exploration design

- Read receptionist result
  `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`.
- Strongest repository lesson from the receptionist:
  the Tao screen is not about whether the algebraic identity itself survives.
  It is about whether any candidate changes the effective coefficient on the
  already-fixed localized LEI cutoff-flux balance after localization debt is
  restored.
- Key source anchors confirmed:
  - `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
  - `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
  - `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
  - `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
  - `steps/step-005/explorations/exploration-003/REPORT.md`
- Strategizer decision:
  run exactly three explorations.
  - Exploration 001:
    screen `divergence/stress` and `Lamb-vector / Helmholtz-projected` under
    one common standard, because both are the most obviously identity-level
    rewrites unless a precise insertion point appears.
  - Exploration 002:
    screen `vorticity transport / Biot-Savart` separately, because the main
    risk is architecture drift plus nonlocal reinsertion debt rather than a
    purely local algebraic cosmetic gain.
  - Exploration 003:
    synthesize the admission/rejection table, branch verdict, and prior-art
    calibration note after the first two reports land.

## Iteration 3 - Exploration completion and Step-2 kill decision

- Created `exploration-001`, `exploration-002`, and `exploration-003` goals and
  launched all three explorer sessions through `bin/launch-role.sh`.
- Operational issue:
  the launched sessions for Explorations 001 and 003 stalled after creating
  early scaffolds, and Exploration 002 only partially completed. This matches
  the earlier wrapper-instability pattern already seen in `step-005`.
- Strategy adjustment:
  complete the exploration reports directly from the anchored local source set
  once the wrapper sessions stopped advancing.
- Exploration conclusions now fixed:
  - Exploration 001:
    `divergence / stress form` and
    `Lamb-vector / Helmholtz-projected form`
    are both rejected as `Tao-insufficient`
  - Exploration 002:
    `vorticity transport / Biot-Savart form`
    is rejected as `Tao-insufficient` inside the frozen LEI audit, with the
    added note that any apparent rescue would drift into a different
    stretching/geometry architecture
  - Exploration 003:
    no candidate survives; the correct branch verdict is immediate
    invalidation rather than Step-3 continuation
- Kill condition status:
  triggered for the full candidate family.
  Exact reason:
  no frozen candidate has a concrete NS-versus-averaged discriminator tied to
  a smaller effective coefficient on the fixed bad term `I_flux[φ]`.

## Iteration 4 - Curation handoff

- Copied the three completed exploration reports into `../../library-inbox/`
  with descriptive names.
- Wrote three step-level meta notes into `../../meta-inbox/`.
- Appended all three report summaries to
  `HISTORY-OF-REPORT-SUMMARIES.md`.
- Created three curator task files for the new inbox/meta artifacts.
- Planned curator launches with receipt files in `../../meta-inbox/`.
