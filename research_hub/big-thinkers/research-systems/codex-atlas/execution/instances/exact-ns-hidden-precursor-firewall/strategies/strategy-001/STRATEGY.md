# Strategy 001: Define One Hidden-Precursor Test, Then Force or Kill It

## Objective

Turn the mission question

```text
if exact Navier-Stokes were to realize a Tao-like delayed abrupt transfer,
must there be an earlier physically observable precursor?
```

into one theorem-facing physical-space test object and drive it to one of the mission's terminal outcomes:

1. positive hidden-precursor firewall,
2. counterexample: delayed transfer without precursor,
3. definition-level failure,
4. model-level negative: no faithful physical-space test object.

This strategy is not allowed to slide back into packet-engineering, generic epsilon-regularity language, or vague claims that "something should get large earlier."

## Methodology

### Phase 0: Delayed-Transfer Definition Gate

Start from the existing Tao mechanism reconstruction and define one preferred delayed-transfer event in physical-space terms, with at most one backup.

The preferred event definition must specify explicitly:

- the setting in which it is measured: exact NS, or a reduced model with a stated exact-NS derivation,
- the output or witness channel that undergoes the delayed abrupt increase,
- the spacetime localization of the event,
- the baseline regime before threshold,
- the threshold-crossing or short-window growth condition,
- what "hidden until threshold" means measurably.

Required deliverables:

- one preferred delayed-transfer event and at most one backup,
- a short notation table,
- a clear positive-firewall target and a clear counterexample target,
- a statement of which parts come from Tao's reconstructed mechanism and which parts are user-chosen observability conventions.

Phase 0 kill conditions:

- If the delayed-transfer event cannot be made falsifiable without smuggling in packet/circuit objects, stop with a definition-level failure.
- If the event only exists as a menu of loosely related formulations, stop. The mission needs one preferred event, not a catalog.

### Phase 1: Precursor-and-Fidelity Gate

Choose exactly one precursor observable for the preferred delayed-transfer event, and lock one faithful test object on which both can be evaluated.

The precursor observable must specify:

- its exact formula,
- the spacetime region where it is measured,
- the smallness condition representing "no earlier warning,"
- why it is dynamically tied to the delayed-transfer event,
- why it is not merely a renamed closed epsilon-regularity or pressure-route quantity.

The faithful test object must specify:

- whether it is exact NS or a reduced model,
- which exact-NS structures it preserves,
- which structures it discards,
- why those discards do not trivialize the hidden-precursor question.

Required deliverables:

- one preferred event-observable pair and at most one backup pair,
- an exact-NS fidelity ledger for the chosen test object,
- a precise formulation of what would count as a lower bound, observability statement, no-hidden-transfer statement, or counterexample.

Phase 1 kill conditions:

- If the only viable object collapses back to non-canonical packet choices, stop with a model-level negative.
- If the observable is just a disguised closed route, stop and report that sharply rather than widening the search.

### Phase 2: Quantitative Hidden-Precursor Test

Attack the single preferred event-observable pair directly.

Each exploration in this phase must begin with one concrete target:

- one observability inequality candidate,
- one precursor lower-bound theorem candidate,
- one no-hidden-transfer statement,
- or one explicit counterexample candidate.

Acceptable outputs are:

- a quantitative lower bound on the precursor on an earlier region,
- a statement that precursor smallness rules out the delayed-transfer event,
- a faithful reduced-model counterexample with the precursor genuinely small,
- or a structural argument that the pair cannot be tested faithfully at all.

Unacceptable outputs are:

- "there should be a warning signal,"
- a rotating menu of observables,
- packet/circuit bookkeeping that no longer lives in physical space,
- a reduced model whose exact-NS relation is rhetorical rather than explicit.

### Phase 3: Mandatory Adversarial Screen

Any apparent firewall or counterexample must be stress-tested adversarially.

If the main result is a firewall, the adversarial pass must try to show:

- the observable is epsilon-regularity or pressure language in disguise,
- the forced precursor is a coordinate or localization artifact,
- the same effect is already present in Tao's averaged model and so is not exact-NS-specific,
- or the claimed earlier region was chosen after the fact.

If the main result is a counterexample, the adversarial pass must try to show:

- the precursor was not actually small in the declared quantity,
- the example depends on hidden packet freedom or non-canonical reconstruction,
- omitted exact-NS structures would reintroduce a precursor,
- or the delayed-transfer event changed meaning between setup and conclusion.

This phase must also answer the Tao filter explicitly:

- is the proposed firewall genuinely exact-NS-specific,
- and is it genuinely tied to delayed transfer rather than generic pre-blowup activity?

### Phase 4: Final Verdict

Finish with exactly one named mission outcome:

1. positive hidden-precursor firewall,
2. counterexample: delayed transfer without precursor,
3. definition-level failure,
4. model-level negative: no faithful physical-space test object.

The final report must make the implication unambiguous:

- pursue,
- kill,
- or reformulate.

## Cross-Phase Rules

1. By the end of Phase 1 there must be one preferred event-observable pair and at most one backup pair.
2. One theorem target or one counterexample target per exploration. State it before derivations or computations.
3. Exact-NS fidelity is non-negotiable. Any reduced model must list preserved and discarded NS structure explicitly.
4. Quantitative content is mandatory. Every accepted claim must point to a named measurable quantity.
5. Do not re-open De Giorgi, epsilon-regularity, pressure-improvement, host-space, or generic BKM/enstrophy routes under new language.
6. Use Tao's existing mechanism reconstruction as input; do not spend budget re-deriving the averaged-NS mechanism from scratch.
7. Every substantial claim in the final report must be tagged `[VERIFIED]`, `[COMPUTED]`, `[CHECKED]`, or `[CONJECTURED]`.
8. Maintain a Direction Status Tracker in `REASONING.md` using `OPEN / PROMISING / CLOSED / EXHAUSTED`.
9. Early stopping is correct if the definition gate fails cleanly, the only faithful object is non-canonical, or a quantitative firewall/counterexample survives adversarial review.

## Validation Criteria

This strategy succeeds if it delivers all of the following:

- a concrete delayed-transfer event definition,
- one explicit precursor observable,
- a measurable hidden-until-threshold criterion,
- one faithful test object with a stated exact-NS relation,
- either a quantitative firewall statement or an explicit counterexample,
- a mandatory adversarial screen against closed routes and fidelity failures,
- an unambiguous terminal verdict in one of the mission's named categories.

This strategy is exhausted if:

- the delayed-transfer event cannot be defined sharply enough,
- the precursor observable or test object collapses into a non-faithful or non-canonical construction,
- the quantitative firewall/counterexample question is answered and survives adversarial review,
- or the only remaining uncertainty is clearly a sharper next-strategy problem rather than more of the same search.

## Context

### Predecessor results to preload

- `execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION-COMPLETE.md`
  - Tao's averaged-NS blowup is mechanistically a five-mode delayed-threshold circuit.
  - The strongest earlier exact-NS discrepancy was circuit non-isolability, but it did not sharpen into a firewall object.
- `execution/instances/exact-ns-no-near-closed-tao-circuit/MISSION-COMPLETE.md`
  - The singleton exact-circuit object is structurally impossible.
  - Packetized backups failed canonization and therefore were not one theorem-facing object.
- `execution/instances/exact-ns-tiny-trigger-firewall/MISSION-COMPLETE.md`
  - Narrowing to the trigger alone did not create a new canonical exact object.
  - The faithful exact object still collapses back to the dead singleton five-role structure, while packet backups remain non-canonical.
- `execution/agents/library/meta/missionary/strategy-001-exact-ns-no-near-closed-tao-circuit-learnings.md`
  - Require one preferred object, test the smallest faithful support first, and treat non-canonical fallbacks as terminal.
- `execution/agents/library/meta/missionary/strategy-002-navier-stokes-learnings.md`
  - Use phase gates and one-theorem-target explorations rather than broad qualitative probing.

### What is already closed

- packet/circuit object-definition missions that do not canonize the object,
- estimate-level epsilon-regularity or De Giorgi rewrites,
- pressure-route reopenings,
- generic host-space reformulations,
- vague claims that exact NS has "too much coupling" without a named measurable witness.

### Strategic aim

The live question is no longer whether exact NS admits Tao's exact interaction graph. That line already died.

The live question is:

```text
even without a canonical exact circuit object,
does exact NS force an earlier physical-space witness whenever Tao-like delayed transfer is approximated faithfully enough to matter?
```

This strategy should answer that question for one precise physical-space test, not for a family of analogies.

## Budget Guidance

Target 4-6 explorations.

Expected efficient path:

- 1 exploration for the delayed-transfer definition gate,
- 1 exploration for the precursor-and-fidelity gate,
- 1-2 explorations for the quantitative firewall/counterexample test,
- 1 exploration for adversarial screening and synthesis.

Do not spend the budget widening the object. If the preferred pair dies cleanly, stop.
