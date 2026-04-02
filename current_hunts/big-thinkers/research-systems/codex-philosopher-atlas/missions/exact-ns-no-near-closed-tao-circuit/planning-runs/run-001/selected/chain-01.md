# Chain 04 - Definition-Stability Audit for "Near-Closed Tao Circuit"

## Central Premise

The prior mission already identified that "exact-NS circuit non-isolability" failed because it was not yet a concrete object. The cleanest early kill is to test whether any precise definition of a near-closed Tao circuit remains stable under the unavoidable exact symmetries and bookkeeping choices of Fourier/helical NS.

## Verifiable Result Target

Either:

- one stable definition family of "near-closed Tao circuit" that later chains can use without hidden normalization tricks; or
- a definition-level obstruction memo proving that every plausible definition is too unstable, too representation-dependent, or too unconstrained to support a theorem test.

## Why This Chain Is Meaningfully Different

This chain does not try to prove obstruction or build a counterexample directly. It asks whether the mission's core theorem object can even be stated in a robust way.

## Ordered Steps

### Step 1 - Propose a short list of candidate definitions

Depends on: none.

Action: write two or three concrete notions of near-closure, for example:
interaction-graph closure,
leakage-ratio closure,
or delayed-threshold behavioral closure.

Action: make each definition explicit about support, normalization, time window, and admissible spectator size.

Expected output: a definition shortlist with formulas, invariances, and intended use.

Kill condition: if the only available definitions are verbal paraphrases of "not too entangled," stop the mission with a sharp vagueness verdict.

### Step 2 - Audit invariance and normalization stability

Depends on: Step 1.

Action: test each definition against exact symmetries and bookkeeping changes that should not change the mathematical content: rescaling, phase rotation, helical basis choice, conjugate completion, and packet regrouping.

Action: reject definitions whose truth value changes under cosmetic representation moves.

Expected output: an invariance audit table marking which definitions are stable, unstable, or only conditionally stable.

Kill condition: if no candidate survives basic invariance checks, produce a definition-level kill report and stop the mission before theorem work.

### Step 3 - Audit dynamical testability on small exact packets

Depends on: Step 2.

Action: for each surviving definition, check whether it can actually be evaluated on a small exact helical/Fourier packet without hidden asymptotic limits or an entire regularity theory.

Action: require each candidate to yield a finite interaction table, a finite leakage metric, or a finite-time behavioral test.

Expected output: a testability memo saying exactly what data one would need to certify or refute the definition.

Kill condition: if every surviving definition requires unbounded packet growth or inaccessible global dynamics, mark the idea untestable at mission scope.

### Step 4 - Attack the survivors with adversarial edge cases

Depends on: Step 3.

Action: test the definitions on edge cases already visible in the inherited context: exact Beltrami cancellation, mirror-mode completion, nearly degenerate triads, and packets with tiny but dynamically decisive trigger modes.

Action: reject any notion that labels obviously irrelevant configurations as Tao-like or obviously relevant ones as non-comparable.

Expected output: an adversarial examples memo with pass/fail outcomes for each candidate definition.

Kill condition: if the classification boundary remains arbitrary after the edge-case audit, do not proceed to theorem planning.

### Step 5 - Freeze the mission object or kill it cleanly

Depends on: Step 4.

Action: if one definition survives, promote it as the fixed object for Chains 01-03 and state its first measurable theorem question.

Action: if none survive, write the cleanest earned conclusion: the mission fails at the object-definition stage, not at the level of proof technique.

Expected output: a canonical definition memo or a definition-level failure memo.

Kill condition: if the final survivor only works by hard-coding Tao's own averaged construction features back into exact NS language, count that as circular and reject it.
