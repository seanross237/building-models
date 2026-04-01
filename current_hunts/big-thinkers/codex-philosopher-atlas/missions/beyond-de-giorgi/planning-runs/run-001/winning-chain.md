# Chain 01 - Harmonic Tail Obstruction Test with Early Tao Gate

## Central Premise

Do not ask whether harmonicity makes the far-field pressure tail smoother. That is already known. Ask the narrower and decisive question:

Can any NS-specific structure make the surviving far-field pressure pairing small enough to reduce the bad coefficient

`C_far ~ ||u||_{L^2}^2 / r_k^3`

from admissible NS data, in a way that Tao's averaged model would not preserve?

If not, the branch should end quickly with a sharp obstruction memo.

## Verifiable Result Target

Either:

- a concrete NS-specific mechanism that turns local information about the harmonic pressure tail into quantitative shrinkage of the actual bad coefficient, or into summable decay strictly stronger than fixed `O(E_0)` control; or
- a rigorous negative result showing that, after quotienting out pressure modes already killed by the test structure, local harmonic-tail information cannot improve the coefficient in a Tao-relevant way.

## Why This Is the Right Next Branch

The prior pressure mission left the harmonic-tail loophole explicitly open. This chain treats that loophole as a falsifiable cleanup target with a strong presentable downside, not as an open-ended search for nicer elliptic estimates.

## Non-Negotiable Gatekeeping Standard

No candidate quantity is allowed to survive unless all of the following hold:

- it acts on the actual surviving pressure pairing after removing constant, affine, or other modes already annihilated by the test structure;
- it targets the coefficient itself, not just a smoother restatement of fixed `O(E_0)` control;
- it uses an NS-specific ingredient beyond generic harmonic interior regularity;
- it survives an estimate-level test rather than only an identity-level or representation-level rewrite;
- it addresses the decisive nonlocal or exterior contribution rather than only a local-looking piece.

If these conditions fail, the chain immediately downgrades to the negative-result track.

## Ordered Steps

### Step 1 - Reconstruct the exact obstruction and front-load the Tao gate

- Depends on: none.
- Action: rebuild the precise far-field pressure pairing from `vasseur-pressure`, identify which harmonic modes survive the test structure, isolate the exact quantity whose smallness would matter, and state in advance what would count as a genuine gain on the bad term.
- Action: name the candidate NS-specific ingredient if one exists, and separate it from generic harmonic facts that Tao's averaged model should preserve.
- Expected output: a formula sheet containing `I_p^far`, the role of `C_far`, the surviving modes, the exact gain target, and a one-page Tao-gate memo.
- Kill condition: if no plausible NS-specific ingredient can be named, or if the claimed gain is not a gain on the actual coefficient, move directly to the negative-result track.

### Step 2 - Run an explicit remote-shell falsification model

- Depends on: Step 1.
- Action: choose a remote shell source with admissible energy, compute the induced harmonic field or harmonic polynomial on the inner cylinder, and test the exact surviving quantity isolated in Step 1.
- Action: treat the exterior contribution as the main adversary. Do not count control of a local subpiece as progress if the shell model keeps the full pairing at `O(E_0)`.
- Expected output: a countermodel memo showing whether the relevant local quantity remains comparable to shell energy and whether any supposed gain survives against the nonlocal source.
- Kill condition: if the shell model forces the relevant quantity to stay at fixed-size control, close the positive route unless a clearly NS-specific cancellation defeats that model.

### Step 3 - Test only a short, pressure-relevant candidate list at the estimate level

- Depends on: Step 2 surviving.
- Action: examine only tightly justified candidates such as oscillation after quotienting out killed modes, derivative decay, harmonic polynomial remainder, or another explicitly motivated quantity acting on the same pairing.
- Action: do not run a broad norm survey. Do not use positivity/Harnack heuristics for a sign-changing object. Do not accept nicer representation formulas as progress unless they improve the operative estimate.
- Expected output: an estimate table recording exactly where annular or local data enters, whether any candidate reduces the bad coefficient, and whether any effect is real or cosmetic.
- Kill condition: if every candidate simply propagates boundary or shell size into another fixed `O(E_0)` bound, stop and write the obstruction memo.

### Step 4 - Convert any surviving gain into a non-recursive quantitative criterion

- Depends on: Step 3.
- Action: if one candidate survives, translate it into a criterion that directly shrinks `C_far` or yields summable decay from admissible NS data, without rebuilding the exhausted De Giorgi recursion under new names.
- Action: require the gain to survive localization and to act on the full far-field contribution, not merely on a partial or mode-restricted surrogate.
- Expected output: a conditional proposition with explicit quantitative gain, assumptions, and proof skeleton.
- Kill condition: if the gain does not reduce the bad coefficient, or only feeds back into the same missing `W^{1,3}`-type input, threshold recursion, or other already-failed architecture, record structural failure.

### Step 5 - Close with the strongest calibrated claim

- Depends on: Step 4, or directly on an earlier kill.
- Action: test whether any surviving mechanism truly uses the NS-specific ingredient named in Step 1 rather than generic elliptic harmonicity.
- Action: make the final claim no broader than the tested family of quantities and models.
- Expected output: one of two endpoints:
  - a narrowly specified NS-specific attack path on the far-field coefficient; or
  - a polished negative result stating that the harmonic-tail loophole is Tao-compatible and does not provide a beyond-De-Giorgi escape.
- Kill condition: if the mechanism survives unchanged in Tao's averaged setting, or if the final claim exceeds what the shell model and estimate-level tests support, close the chain negatively and narrow the statement until it is fully earned.

## Outcome Standard

A sharp obstruction memo counts as a successful result. This branch should not be prolonged in search of prettier harmonic estimates once the coefficient-shrinkage route has failed.
