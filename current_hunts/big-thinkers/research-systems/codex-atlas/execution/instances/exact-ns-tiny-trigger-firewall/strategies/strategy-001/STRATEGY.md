# Strategy 001: Define One Trigger, Then Force Its Visibility or Build It

## Objective

Turn the mission question

```text
can exact Navier-Stokes support a Tao-style tiny hidden trigger at all?
```

into one theorem-facing exact object and drive it to one of the mission's terminal outcomes:

1. a quantitative tiny-trigger firewall in exact NS,
2. an explicit hidden-trigger counterexample in an exact or faithfully reduced model,
3. a definition-level failure because "tiny delayed trigger" cannot be made precise enough,
4. a model-level negative because no canonical faithful test object survives.

This strategy is not allowed to retreat into generic NS estimates, qualitative language about "too much coupling," or an open-ended packet-engineering project.

## Methodology

### Phase 0: Definition Gate for a Tiny Delayed Trigger

Start from the predecessor reconstruction of Tao's five-mode delayed-threshold mechanism and define one preferred trigger object, with at most one backup.

The preferred definition must specify all of the following explicitly:

- the representation being used: exact Fourier/helical NS, or a reduced model with a stated exact-NS derivation,
- the trigger variable or trigger packet,
- the quantity in which the trigger is "tiny" before threshold,
- the quantity in which the trigger becomes causally visible after threshold,
- the threshold event or delayed timescale separation,
- the exact bookkeeping for desired transfer, spectator leakage, and back-reaction,
- which parts are exact-NS structure and which parts are user-chosen tolerances.

Required deliverables:

- one preferred exact object and at most one backup,
- a short notation table,
- a clear positive-firewall target and a clear counterexample target,
- a statement of what would count as a precursor, leakage witness, or back-reaction witness.

Phase 0 kill conditions:

- If "tiny delayed trigger" cannot be made falsifiable without unconstrained packet choices, stop and report a definition-level failure.
- If a packetized backup is used, it must also pass a canonization gate immediately:
  - fixed support convention,
  - fixed projection/coordinatization,
  - fixed visibility/leakage bookkeeping,
  - fixed restoration rule from the packet model back to exact NS language.
  If those are not pinned down, the backup is inadmissible.

### Phase 1: Smallest Faithful Exact-NS Test Object

Before any coefficient campaign, test static realizability on the smallest honest exact object that could host the preferred trigger definition.

Possible settings include:

- exact Fourier triads,
- exact helical triads,
- a reduced dynamical subsystem whose relation to the exact NS bilinear form is written explicitly.

The task in this phase is:

- identify the minimal active support needed for the trigger logic,
- determine which precursor, leakage, or back-reaction quantities are structurally forced,
- separate rigid features from tunable features,
- choose one minimal configuration for quantitative testing.

Required deliverable:

- an exact interaction/visibility ledger listing, for each relevant coupling or observable channel:
  - its structural form,
  - whether it is desired, precursor, leakage, or back-reaction,
  - whether it is rigid or tunable,
  - why it matters for hidden-trigger viability.

Cross-phase rule:

- Static realizability comes before dominance estimates. If the preferred trigger object cannot even exist on the smallest faithful exact support, treat that as a terminal structural result.

### Phase 2: Quantitative Firewall-or-Counterexample Test

Attack the single minimal configuration directly. Each exploration in this phase must begin with one concrete target:

- one lower-bound theorem candidate,
- one impossibility statement,
- or one explicit hidden-trigger construction.

Acceptable outputs are:

- a lower bound on precursor visibility,
- a lower bound on spectator leakage,
- a forced back-reaction estimate,
- an observability inequality,
- or an explicit exact/faithfully reduced hidden-trigger example that survives the bookkeeping from Phase 0.

Unacceptable outputs are:

- "there are many couplings,"
- "the geometry seems entangled,"
- a reduced model whose relation to exact NS is only rhetorical,
- a construction that works only by changing definitions midstream.

### Phase 3: Mandatory Adversarial Tao Filter

Any apparent positive firewall or counterexample must be stress-tested adversarially.

If the main result is a firewall, the adversarial pass must try to:

- find an alternate helical or geometric arrangement that evades the claimed precursor bound,
- show the witness quantity is a coordinate artifact,
- or show the same effect already appears in Tao's averaged model.

If the main result is a counterexample, the adversarial pass must try to:

- expose omitted spectator or back-reaction channels,
- show the trigger is not actually tiny in the declared quantity,
- or show the example depends on non-canonical packet freedom.

This phase must also answer the Tao filter:

- is the claimed firewall genuinely absent from Tao's averaged model,
- and is it genuinely exact-NS-specific rather than a bookkeeping artifact?

### Phase 4: Final Verdict

Finish with exactly one named mission outcome:

1. positive tiny-trigger firewall,
2. counterexample: hidden trigger survives,
3. definition-level failure,
4. model-level negative: no canonical faithful test object.

The final report must make the next-step implication explicit:

- pursue,
- kill,
- or reformulate.

## Cross-Phase Rules

1. One preferred exact object and at most one backup. No menus of partially compatible trigger notions.
2. One theorem target or one construction target per exploration. State it before derivations or computations.
3. Exact-NS fidelity is non-negotiable. Any reduced model must state exactly which NS couplings it preserves and which it discards.
4. Quantitative content is mandatory. Every accepted positive or negative claim must point to a named measurable quantity.
5. If packetization enters, canonization is the first test, not the fallback after several explorations.
6. Do not re-open pressure, De Giorgi, epsilon-regularity, host-space, or generic estimate-improvement routes.
7. Every substantial claim in the final report must be tagged `[VERIFIED]`, `[COMPUTED]`, `[CHECKED]`, or `[CONJECTURED]`.
8. Maintain a Direction Status Tracker in `REASONING.md` using `OPEN / PROMISING / CLOSED / EXHAUSTED`.
9. Early stopping is correct if the preferred object dies structurally, the canonization gate fails, or a quantitative firewall/counterexample survives adversarial review.

## Validation Criteria

This strategy succeeds if it delivers all of the following:

- a concrete definition of "tiny delayed trigger" with measurable smallness, delay, and causal effect,
- one preferred faithful test object,
- an exact interaction/visibility ledger for the minimal configuration,
- either a quantitative firewall witness or an explicit counterexample,
- a mandatory adversarial Tao filter,
- an unambiguous terminal verdict in one of the mission's named categories.

This strategy is exhausted if:

- the definition gate fails cleanly,
- the preferred object fails structural realizability on the smallest faithful support,
- the only surviving packetized versions are non-canonical,
- or the quantitative firewall/counterexample question is answered and survives adversarial review.

## Context

### Predecessor results to preload

- `execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION-COMPLETE.md`
  - Tao's averaged blowup is driven by a five-mode delayed-threshold circuit with a tiny but dynamically decisive trigger variable.
  - The earlier firewall mission ended with a mechanism-level negative and recommended formalizing a sharper exact object.
- `execution/instances/exact-ns-no-near-closed-tao-circuit/MISSION-COMPLETE.md`
  - The clean singleton exact-circuit embedding died structurally under exact triad geometry.
  - Packetized backups failed canonically: they became a family of choices rather than one theorem-facing object.
- `execution/agents/library/meta/missionary/strategy-001-exact-ns-no-near-closed-tao-circuit-learnings.md`
  - Require one preferred exact object, test the smallest faithful support first, and treat non-canonical backups as terminal failures.

### What is already closed

- broad Tao exegesis without a theorem-facing object,
- generic estimate improvements,
- vague "NS has too much coupling" narratives,
- packet models that are not canonized,
- any route that quietly changes the trigger definition during the argument.

### Strategic aim

The live question is now narrower than "can exact NS host a Tao-like circuit?":

```text
can exact NS hide an energetically tiny delayed trigger long enough for it to become dynamically decisive,
or does exact NS force an observable precursor before threshold?
```

This strategy should answer that question for one precise object, not for a broad family.

## Budget Guidance

Target 4-6 explorations.

Expected efficient path:

- 1 exploration for the definition gate,
- 1 exploration for the smallest faithful exact-object audit,
- 1-2 explorations for the quantitative firewall/counterexample test,
- 1 exploration for adversarial Tao filtering and synthesis.

Do not spend the budget widening the object. If the preferred object dies or the backup is non-canonical, stop.
