# Refined Chain 02 - Estimate-First Obstruction Hunt for NS Reformulation Cancellations

## Central Premise

Do not ask whether NS has "the SQG commutator." Ask the narrower question:

Can any natural reformulation of the exact NS nonlinearity produce an estimate-level improvement on the actual localized or truncated bottleneck term, in a way that depends on algebraic structure destroyed by Tao's averaged model?

If not, the branch should end with a sharp obstruction memo rather than a vague rewrite survey.

## Verifiable Result Target

Either:

- a concrete candidate reformulation that improves a named localized/truncated NS interaction and survives an early Tao screen, or
- a narrow negative memo showing that the standard Lamb-vector, projected, vorticity, or closely related tensor rewrites do not improve the operative estimate except in geometry-only regimes better assigned to Chain 03.

## Why This Refined Chain Is Meaningfully Different

This branch is still about whether the exact NS algebra can be operationalized into a better nonlinear mechanism, but it is no longer a general search over pretty identities. It is an estimate-first screen tied directly to the mission bottleneck and separated from geometry-first Beltrami analysis.

## Ordered Steps

### Step 1 - Fix the target estimate and apply the Tao pre-screen

- Depends on: none.
- Action: name the exact localized or truncated interaction that must improve, and define in advance what counts as a genuine gain:
  - derivative reduction,
  - integrability improvement at the bottleneck term,
  - or a closure improvement strong enough to change the local-energy/level-set balance.
- Action: shortlist only reformulations whose usefulness would rely on an exact algebraic feature of NS not obviously preserved by Tao's averaged model.
- Expected output: a one-page screening memo with:
  - the named bad term,
  - the admissible notion of "gain,"
  - and at most 2-3 candidate formulations worth testing.
- Kill condition: if no candidate is both estimate-relevant and plausibly nontrivial under the Tao filter, stop and write the negative memo immediately.

### Step 2 - Test shortlisted candidates at the estimate level, not the identity level

- Depends on: Step 1.
- Action: for each surviving candidate, derive the actual localized/truncated estimate that would replace or improve the bad NS term. Do not accept identity-level simplification as progress.
- Action: test standard formulations first:
  - Lamb-vector / projected form,
  - vorticity transport form,
  - one additional tensor or trilinear formulation only if it targets the same bottleneck term.
- Expected output: an estimate memo stating, for each candidate:
  - the exact rewritten bad term,
  - whether any derivative or integrability gain survives localization/projection,
  - and whether the effect is real or cosmetic.
- Kill condition: if every candidate collapses back to the same second-order CZ/quadratic structure at the estimate level, terminate with an obstruction memo and do not proceed further.

### Step 3 - Run a robustness screen and branch handoff test

- Depends on: Step 2.
- Action: if one candidate appears to improve the estimate, test whether the gain is genuinely algebraic and generic or merely a near-Beltrami / alignment effect.
- Action: use Beltrami only as a fragility screen, not as positive evidence. Specify the perturbation metric before testing.
- Expected output: a robustness memo with one of two conclusions:
  - the gain persists outside special alignment classes and remains a live algebraic lead, or
  - the gain is confined to geometry-only regimes and should be handed off to Chain 03.
- Kill condition: if the candidate only survives in exact or near-exact Beltrami-style alignment, record "geometry branch only" and close this chain as an algebraic dead end.

### Step 4 - Close with a calibrated final claim

- Depends on: Step 3, or directly on Step 2 if the branch dies there.
- Action: write the strongest justified conclusion and no stronger.
- Expected output: one of:
  - a concrete follow-on target defined by a specific improved estimate and why Tao does not immediately erase it, or
  - a bounded negative claim: the tested natural reformulations do not produce an SQG-analogous estimate-level gain on the operative NS bottleneck, except possibly through geometry-dominated effects outside this branch.
- Kill condition: if the final claim requires language broader than the tested family of formulations, narrow the statement until it is fully earned.
