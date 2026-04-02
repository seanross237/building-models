# Chain 01 - Dynamic Phase-Decoherence Tax On Delayed Transfer

## Central premise

If exact Navier-Stokes really blocks Tao-like delayed transfer, the obstruction
should appear as a quantitative dynamical tax: any interaction family that
keeps the desired transfer direction alive for a full delayed-transfer window
must pay a positive amount of phase slippage or coherence loss. The object to
hunt is therefore a time-integrated intrinsic phase-defect functional, not
another static packet score.

## Verifiable result target

Either:

- an exact lower bound of the form
  "strong delayed one-way transfer plus low spectator burden implies
  integrated phase defect at least c > 0";
- an explicit exact family showing that the candidate defect can stay small long
  enough that this obstruction route dies; or
- a bounded negative memo explaining why the object cannot be made intrinsic.

## Prior context to carry forward

- Tao's delayed-threshold stage order and tiny-trigger role are load-bearing.
- Exact NS helical packets need mandatory conjugate completion, a frozen sign
  sheet, one amplitude normalization, and one phase anchor.
- The Step-6 packet gates from the predecessor mission may be reused only as
  stress-test fixtures, not as the theorem object itself.

## Ordered steps

### Step 1 - Define the smallest intrinsic phase-defect object

- Depends on: none.
- Actions:
  - choose one minimal exact support class, likely a role-labeled helical packet
    family with forced conjugate completion;
  - define one candidate intrinsic defect, such as a transfer-weighted
    triad-phase slippage functional or a delayed-window coherence budget;
  - state the gauge fixing explicitly: phase anchor, sign sheet, and what is
    quotient-ed out as symmetry rather than baked into the object.
- Expected output:
  - one definition sheet with an explicit formula,
  - one symmetry/canonicalization note,
  - one sentence stating why the object is not just a relabeled desired graph.
- Kill condition:
  - if the object only makes sense after hand-picking a Tao-style desired
    channel set or packet trace, stop and report a definition-level failure.

### Step 2 - Derive the exact phase-amplitude evolution ledger

- Depends on: Step 1.
- Actions:
  - write the exact Fourier/helical amplitude and phase equations for the
    minimal carried interaction family;
  - separate desired-transfer terms, forced mirror/conjugate terms, spectator
    terms, and viscous drift;
  - identify which exact phase combinations control transfer sign.
- Expected output:
  - an exact evolution ledger for amplitudes and phase combinations,
  - a short list of terms that can change the sign or size of the desired
    transfer.
- Kill condition:
  - if the phase ledger does not close even on the minimal honest family, or if
    the needed variables proliferate into an uncontrolled packet forest, stop.

### Step 3 - Convert Tao-like delayed transfer into phase-window requirements

- Depends on: Step 2.
- Actions:
  - formalize the minimum delayed-transfer hypotheses worth testing:
    weak clock, tiny trigger, rapid carrier-to-conduit transfer, and low
    spectator burden over one activation window;
  - prove which phase windows are required for those transfer signs to persist;
  - isolate the narrowest phase relations that are genuinely exact-NS-specific.
- Expected output:
  - a lemma translating transfer-direction assumptions into phase-window
    constraints,
  - one explicit list of required windows or inequalities.
- Kill condition:
  - if delayed transfer does not force any nontrivial phase localization, then
    the candidate defect is too weak to matter and the chain should close.

### Step 4 - Prove or refute a positive decoherence tax

- Depends on: Step 3.
- Actions:
  - use the exact ledger to bound the rate of change of the required phase
    combinations;
  - show that forced couplings, mirror modes, or projection geometry inject a
    positive lower bound on cumulative slippage, or else identify an honest
    cancellation family;
  - state the obstruction as an integrated inequality, not a slogan.
- Expected output:
  - either a theorem-grade obstruction proposition,
  - or a precise counter-ledger showing why the tax can vanish.
- Kill condition:
  - if the lower bound reduces to already-known packet leakage bookkeeping, or
    if an exact family cancels the proposed tax on honest support, stop.

### Step 5 - Stress test on explicit exact families

- Depends on: Step 4.
- Actions:
  - test the proposition against the smallest explicit family carried by the new
    run and against inherited packet fixtures such as `F_SL`, `F_SS`, and
    `F_DT` only as sanity checks;
  - verify whether the obstruction distinguishes friendly, hostile, and
    potentially phase-locked examples.
- Expected output:
  - a pass/fail stress-test table,
  - a final verdict:
    obstruction survives,
    counterexample found,
    or object fails.
- Kill condition:
  - if the proposition cannot separate any honest exact examples, it is not a
    useful theorem-facing object.

## Why this chain is meaningfully different

This is the only chain whose success depends on a dynamical lower bound over a
time window. It does not ask first for a compatible phase assignment or a
special subsystem. It asks whether exact NS imposes an unavoidable cumulative
decoherence tax once delayed transfer is demanded.
