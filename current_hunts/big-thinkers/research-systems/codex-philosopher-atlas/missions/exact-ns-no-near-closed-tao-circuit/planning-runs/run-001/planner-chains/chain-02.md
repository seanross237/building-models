# Chain 02 - Spectator-Leakage Lower-Bound Ledger

## Central Premise

The strongest surviving mismatch may not be that desired Tao channels are impossible, but that exact NS cannot keep them isolated. Once one activates the needed triads, exact closure under `p + q = k`, Leray projection, and mirror-mode completion forces extra channels. The route is to turn that into a quantitative leakage lower bound.

## Verifiable Result Target

Either:

- a lower bound showing that any exact packet realizing the desired Tao-like channels must leak at least a fixed fraction of interaction strength or energy flux into spectator modes; or
- a precise negative result showing that leakage can in fact be made arbitrarily small in some explicit family.

## Why This Chain Is Meaningfully Different

This chain accepts that some desired couplings may exist and focuses instead on unavoidable extra couplings. It is graph-closure and leakage-based, not coefficient-ratio based or adversarially constructive.

## Ordered Steps

### Step 1 - Freeze one leakage functional and one closure rule

Depends on: none.

Action: define a finite target circuit graph and one quantitative leakage measure, for example the ratio of forced off-graph interaction strength to on-graph interaction strength, or the minimum spectator amplitude production over one activation window.

Action: choose one closure convention in advance: exact Fourier support closure, helical triad closure, and conjugate completion under `u^(-k) = conjugate(u^k)`.

Expected output: a leakage-definition sheet with one formula for "near-closed" and one exact closure rule.

Kill condition: if no leakage functional is invariant enough to compare different packet realizations honestly, stop and redirect to Chain 04.

### Step 2 - Build the forced spectator ledger for the smallest candidate packets

Depends on: Step 1.

Action: start from a minimal packet that realizes the intended Tao roles and compute the full list of same-scale, conjugate, and cross-scale interactions forced by the closure rule.

Action: separate spectators into classes so later lower bounds can be attributed cleanly: mirror modes, companion triads, long-leg feedback, and next-shell feedback.

Expected output: a closure ledger listing desired channels, forced spectator channels, and the structural reason each spectator appears.

Kill condition: if the desired packet cannot even be closed finitely under the chosen rule, the chain should report finite-packet non-closure immediately as a stronger obstruction.

### Step 3 - Convert the closure ledger into a quantitative lower-bound problem

Depends on: Step 2.

Action: express each spectator class in the same normalization as the desired channels so the comparison is honest.

Action: derive candidate lower bounds from exact coefficient identities, reality symmetry, and projection geometry rather than heuristic "many couplings" language.

Expected output: a lower-bound worksheet reducing the problem to a finite set of inequalities or an optimization problem over geometry parameters.

Kill condition: if every spectator term can simultaneously cancel by phase choice or geometry without violating the desired channels, the lower-bound premise is broken and the chain should hand off to Chain 03.

### Step 4 - Stress-test the bound against adversarial geometry and helicity choices

Depends on: Step 3.

Action: search the allowed geometry families for worst-case leakage, including near-degenerate or specially aligned helical configurations.

Action: identify whether the infimum leakage is positive, merely bounded in a weaker norm, or tends to zero along an explicit family.

Expected output: a stress-test memo with the best surviving lower bound or an explicit vanishing-leakage family.

Kill condition: if the lower bound survives only for generic choices and collapses on the first special family, it is not the right theorem object.

### Step 5 - Package the result as obstruction or counterexample

Depends on: Step 4.

Action: if the infimum leakage stays positive, formulate the cleanest no-near-closure statement available, naming the packet class, leakage functional, and bound.

Action: if the infimum leakage tends to zero, record the exact family that beats the leakage route and pass it to the adversarial construction chain.

Expected output: a theorem candidate or an explicit anti-obstruction family.

Kill condition: if the final product is only a long list of extra couplings without a metric or bound, the chain failed.
