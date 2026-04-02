# Step 6 Goal: Chain Step 2 State The Tao Discriminator Before Any Algebraic Optimism

## Mission Context

**Mission:** Beyond De Giorgi — What Structural Property Could Break the NS
Regularity Barrier?

**Active chain:** `Fixed-Protocol Obstruction Audit for Exact NS Reformulations`

**Why this step exists now:** `step-005` survived the chain's setup stage and
made the branch concrete. The audit is now frozen at:

- inherited architecture:
  `local-energy flux/localization`
- bad term:
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`
- solution class:
  suitable weak solutions in the Leray-Hopf energy class with LEI
- localization protocol:
  one CKN-style parabolic cutoff, with all projection, CZ, commutator, and
  Biot-Savart debt charged explicitly
- gain currency:
  `coefficient shrinkage in the fixed localized LEI balance`
- candidate family:
  `divergence/stress form`,
  `Lamb-vector / Helmholtz-projected form`,
  `vorticity transport / Biot-Savart form`
- paired hybrid route:
  `none at this stage`

The chain's next credibility gate is not an estimate derivation. It is the
Tao discriminator. Before any candidate is allowed into a loss ledger, this
step must say exactly what NS-specific feature the candidate is using, how
Tao-style averaging destroys or washes that feature out, and where that
difference could matter inside the already-fixed localized balance.

## This Step Covers

This strategizer execution covers **Chain Step 2 only**:

- for each frozen candidate, state the exact NS feature that is supposed to
  matter;
- state how Tao-style averaging destroys, washes out, or preserves that
  feature;
- state where, if anywhere, that distinction could alter the estimate on the
  already-fixed bad term `I_flux[φ]`;
- reject candidates whose specialness is only identity-level, only verbal, or
  only available after silently changing architecture or hypotheses;
- and decide whether the branch still deserves Step 3's estimate ledger.

Do **not** derive the actual candidate estimates yet. Do **not** run the full
localization-loss ledger yet. Do **not** reopen geometry or pressure branches
except as bounded negative background. This step is a gate, not a proof.

## Required Deliverables

Produce all of the following inside `RESULTS.md`:

1. **Candidate-by-candidate Tao-screen memo**
   - cover each frozen candidate separately:
     - `divergence/stress form`
     - `Lamb-vector / Helmholtz-projected form`
     - `vorticity transport / Biot-Savart form`
   - identify the exact NS feature each candidate claims to exploit;
   - state whether Tao-style averaging destroys, weakens, or preserves that
     feature;
   - label each claim `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.

2. **Localized insertion-point note**
   - for each candidate, name the exact place in the fixed local-energy
     cutoff-flux balance where the claimed NS-versus-averaged distinction could
     matter;
   - if there is no credible insertion point before Step 3, say so explicitly;
   - reject candidates whose discrimination lives only at the static rewrite
     level.

3. **Admission/rejection table**
   - for each candidate, classify it as one of:
     - `admit to Step 3`
     - `reject as Tao-insufficient`
     - `reject as architecture-changing`
   - give one short reason tied to the frozen architecture and bad term, not a
     general opinion about the reformulation.

4. **Branch verdict memo**
   - say whether the branch remains alive after the Tao screen;
   - if at least one candidate survives, name the exact survivors and the
     narrow question Step 3 should test;
   - if no candidate survives, recommend branch invalidation immediately rather
     than a cosmetic continuation.

5. **Prior-art calibration note**
   - distinguish this Tao screen from:
     - the established De Giorgi sharpness record,
     - the pressure-route negatives,
     - and the killed geometry branch;
   - state what this step newly tests that those earlier negatives did not
     already settle.

## Exploration Tasks

Use **2-4 explorations total** unless a kill condition fires early.

### Exploration A: Fix the Tao screen for the first two rewrites

Tasks:
- test `divergence/stress form` and `Lamb-vector / Helmholtz-projected form`
  against Tao's averaged-model filter;
- identify whether their purported NS-specific content survives only as exact
  identities or has a credible estimate-level insertion point in `I_flux[φ]`.

Success standard:
- both candidates receive explicit, nonverbal Tao-screen outcomes tied to the
  frozen LEI setup.

### Exploration B: Fix the Tao screen for the vorticity rewrite

Tasks:
- test `vorticity transport / Biot-Savart form` against the same Tao filter;
- decide whether any claimed NS-specific structure is genuine inside the fixed
  local-energy architecture or whether it already leaves the branch by changing
  architecture.

Success standard:
- the vorticity-side candidate is either admitted with a clear localized
  insertion point or rejected honestly for this branch.

### Exploration C: Write the admission verdict

Only run this after A and B are fixed.

Tasks:
- compare the three candidate outcomes under one standard;
- decide whether Step 3 should exist and, if so, for which exact survivors;
- write the narrowest branch verdict actually earned.

Success standard:
- mission control receives a clear continue-or-kill recommendation for the
  exact-reformulation audit.

## Kill Conditions

Trigger an early negative conclusion for this step if any of the following
happens:

- no candidate has a concrete NS-versus-averaged discriminator tied to the
  fixed bad term `I_flux[φ]`;
- a candidate's alleged specialness exists only before localization and has no
  credible place to alter the LEI cutoff-flux estimate;
- the only way to keep a candidate alive is to change architecture, smuggle in
  stronger hypotheses, or reopen the excluded hybrid geometry route;
- the claimed Tao discriminator is equally available in Tao's averaged setting
  once the statement is made precise.

If a kill condition fires for all candidates, count that as a successful
bounded negative result for this step and recommend branch invalidation rather
than continuation to Step 3.

## Constraints

- Do **not** derive the full estimate ledger yet. That belongs to Chain Step 3.
- Do **not** broaden the candidate family beyond the three items fixed in
  `step-005`.
- Do **not** admit a hybrid route in this step unless the fixed branch record
  is explicitly revised later by controller action.
- Do **not** convert a Tao-insufficient candidate into a live lead by switching
  to a different bottleneck or localization protocol.
- Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and
  `[PROPOSED]`.

## Validation Requirements

- Name the exact source files used for every Tao-discriminator claim.
- Make the NS-versus-averaged distinction explicit enough that a later step can
  test it without redefining it.
- State clearly whether each candidate is admitted or rejected and why.
- If any candidate survives, define the exact Step-3 estimate question in one
  sentence per survivor.
- If none survive, say plainly that the branch should stop rather than drift.
