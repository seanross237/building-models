# Chain 01 - Local Harmonic Pressure Localization

## Central Premise

The prior mission killed every global H^1-based pressure route because the bad far-field term stayed `O(E_0)`. But `p_far` is harmonic on the local cylinder. This chain tests whether a truly local harmonic norm, annular-energy quantity, or Harnack-decay estimate gives a usable gain outside the De Giorgi framework.

## Verifiable Result Target

Either:

- a local estimate for `p_far` that depends on annular or local data in a way that is stronger than the old `O(E_0)` bound, or
- a sharp obstruction note proving that harmonicity does not generate any Tao-relevant gain.

## Why This Chain Is Meaningfully Different

This is the only chain centered on the local/global mismatch of the far-field pressure term. It does not search for a better De Giorgi exponent and does not revisit the failed global H^1 program.

## Ordered Steps

### Step 1 - Reconstruct the exact obstruction

- Depends on: none.
- Action: rebuild the near/far pressure split from `vasseur-pressure`, isolate the exact place where the far-field term enters with a fixed constant, and record which quantities are already `U_k`-dependent.
- Expected output: a short formula sheet with the bad term, its scaling, and the precise statement of what must improve for this chain to matter.
- Kill condition: if the prior mission already implies that every local harmonic candidate collapses to the same fixed constant before any new argument begins, stop and write a one-page obstruction memo.

### Step 2 - Test truly local harmonic norms

- Depends on: Step 1.
- Action: evaluate local `H^1`, local `BMO`, Campanato, Carleson-type, and annular-energy formulations for `p_far` on the cylinder, using Harnack, mean-value, and interior-gradient estimates.
- Expected output: an estimate table showing, for each candidate norm, whether support distance or annular energy enters and whether the bound is still only `C E_0`.
- Kill condition: if every natural local norm reduces to `C E_0` at the working scale, terminate the chain and record that harmonicity gives smoothness but no useful locality.

### Step 3 - Convert the best surviving estimate into a non-De-Giorgi criterion

- Depends on: Step 2.
- Action: if a candidate norm survives, translate it into either a conditional epsilon-regularity statement, a local energy improvement, or an annular-flux control statement that does not reopen the exhausted De Giorgi recursion.
- Expected output: a draft lemma or conditional proposition with a proof skeleton and a precise statement of what data it controls.
- Kill condition: if the gain is too weak to affect a critical step, or if it still requires the same missing `W^{1,3}`-type input, stop and write the failure as a structural obstruction.

### Step 4 - Apply the Tao filter and close the chain

- Depends on: Step 3, or directly on Step 2 if the chain dies there.
- Action: compare the surviving mechanism with Tao's averaged NS model and decide whether the argument uses exact NS pressure structure or only generic elliptic harmonicity.
- Expected output: a final route memo with one of two outcomes: a concrete local-harmonic attack path, or a negative result stating that harmonicity is not a distinguishing NS property here.
- Kill condition: if the same mechanism survives averaging unchanged, record that failure explicitly and close the chain.
