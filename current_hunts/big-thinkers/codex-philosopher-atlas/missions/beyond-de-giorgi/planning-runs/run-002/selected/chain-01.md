# Chain 01 - Estimate-First NS Reformulation Cancellations

## Central Premise

Do not ask whether NS has "the SQG commutator." Ask the narrower question:

Can any natural reformulation of the exact NS nonlinearity produce an estimate-level improvement on a named localized or truncated interaction, in a way that depends on algebraic structure destroyed by Tao's averaged model?

If not, this branch should end with a sharp obstruction memo rather than a survey of attractive identities.

## Verifiable Result Target

Either:

- a concrete reformulation that improves the operative localized interaction and survives an early Tao screen; or
- a bounded negative result showing that the standard Lamb-vector, projected, vorticity, and closely related rewrites do not create a real estimate-level gain except in geometry-dominated regimes better handled by Chain 02.

## Why This Chain Is Meaningfully Different

This is the only chain whose core question is whether the exact NS nonlinearity can be reorganized into a better mechanism at the estimate level. It is not a vortex-geometry branch, not a compactness branch, and not a tensor-eigenframe branch.

## Ordered Steps

### Step 1 - Fix the target interaction and front-load the Tao screen

- Depends on: none.
- Action: name the exact localized or truncated NS interaction that must improve, and define in advance what counts as a genuine gain:
  - derivative reduction,
  - integrability improvement at the bottleneck term,
  - or a closure improvement strong enough to change the local-energy or truncation balance.
- Action: shortlist at most 2-3 reformulations whose usefulness would rely on an exact algebraic feature of NS not obviously preserved by Tao's averaged model.
- Expected output: a screening memo naming the bad term, the admissible notion of gain, and the candidate formulations worth testing.
- Kill condition: if no candidate is both estimate-relevant and plausibly nontrivial under the Tao filter, stop immediately and write the negative memo.

### Step 2 - Test the shortlisted reformulations at the estimate level

- Depends on: Step 1.
- Action: derive the actual localized or truncated estimate produced by each surviving candidate. Reject identity-level simplification as progress.
- Action: test the standard forms first:
  - Lamb-vector or projected form,
  - vorticity transport form,
  - one additional tensor or trilinear rewrite only if it targets the same bottleneck interaction.
- Expected output: an estimate table stating, for each candidate, the rewritten bad term, whether any derivative or integrability gain survives localization or projection, and whether the effect is real or cosmetic.
- Kill condition: if every candidate collapses back to the same quadratic or Calderon-Zygmund structure at the estimate level, terminate with an obstruction memo and do not proceed further.

### Step 3 - Run a robustness screen and branch-handoff test

- Depends on: Step 2.
- Action: if one candidate appears to improve the estimate, test whether the gain is genuinely algebraic and generic or merely a near-Beltrami or alignment effect.
- Action: use Beltrami only as a fragility screen, not as positive evidence. Fix the perturbation metric before running the test.
- Expected output: a robustness memo concluding either that the gain persists outside special alignment classes or that it belongs to the geometry branch only.
- Kill condition: if the only surviving signal is a geometry-only near-Beltrami effect, record "hand off to Chain 02" and close this chain as an algebraic dead end.

### Step 4 - Convert any surviving gain into a concrete attack path

- Depends on: Step 3.
- Action: translate the surviving estimate into a non-De-Giorgi proposition, local-energy improvement, or truncation-level criterion with a clearly named next theorem target.
- Expected output: a draft proposition with explicit hypotheses, the improved estimate, and the first missing lemma.
- Kill condition: if the gain does not materially change the operative closure mechanism, narrow the claim to a negative result and stop.

### Step 5 - Close with the strongest calibrated claim

- Depends on: Step 4, or directly on Step 2 or Step 3 if the chain dies earlier.
- Action: state the narrowest conclusion that the tested rewrites support.
- Expected output: one of two endpoints:
  - a concrete follow-on target defined by a specific improved estimate and why Tao does not immediately erase it; or
  - a bounded negative claim that the tested natural reformulations do not produce an SQG-analogous gain on the operative NS bottleneck except possibly through geometry-dominated effects outside this chain.
- Kill condition: if the final claim is broader than the family of formulations actually tested, narrow it until it is fully earned.
