# Strategy 001: Define the Circuit, Then Prove or Kill It

## Objective

Turn the predecessor mission's surviving mechanism-level discrepancy

```text
exact NS circuit non-isolability
```

into a concrete yes/no object. This strategy must produce one of:

- a quantitative no-circuit / leakage lower-bound statement for exact Navier-Stokes,
- an explicit near-closed Tao-like circuit construction in exact Fourier/helical NS,
- or a sharp definition-level failure showing that "near-closed Tao circuit" cannot be made precise enough to test.

This is a ground-clearing but already theorem-facing strategy. It is not allowed to drift back into broad Tao exegesis, generic NS estimate improvement, or qualitative talk about "entanglement."

## Methodology

### Phase 0: Definition Gate

Start from the predecessor mission's mechanism reconstruction and define a small family of candidate "near-closed Tao circuit" notions.

The definition must specify, explicitly:

- a finite active set of Fourier modes or helical packets `S`,
- a desired coupling graph `G_target`,
- which couplings are intended to realize Tao's pump / amplifier / rotor / handoff logic,
- a leakage functional `Leak(S)` or equivalent spectator-coupling budget,
- a dominance requirement separating desired couplings from unwanted ones,
- a threshold or timescale condition representing Tao's delayed-trigger logic.

Required outputs from this phase:

- one preferred definition and at most one backup definition,
- a short notation table,
- an explanation of which parts are exact-NS objects and which are user-chosen tolerance parameters,
- a clear statement of what would count as a positive obstruction and what would count as a counterexample.

Phase 0 gate:

- If no candidate definition is concrete enough to be true or false in exact Fourier/helical NS, stop and report a definition-level negative result. Do not proceed to symbolic coupling computations on vague language.

### Phase 1: Exact Interaction Audit

Work in the smallest exact representation that can honestly test the definition: Fourier triads, helical decomposition, and exact Leray-projected bilinear interactions.

For the preferred candidate definition, compute the exact interaction table for the smallest Tao-like subsystem that could plausibly implement the five-stage logic. Identify:

- desired couplings,
- forced spectator couplings,
- couplings eliminated by geometry or helicity,
- couplings tunable by mode choice,
- couplings rigid under any admissible choice.

Required deliverable:

- an exact interaction ledger with entries of the form
  - coupling,
  - coefficient or structural form,
  - desired / spectator / forbidden status,
  - tunable vs rigid,
  - relevance to the leakage budget.

This phase should end with a single minimal configuration to stress-test. Do not keep multiple sprawling candidate geometries alive unless they are genuinely inequivalent.

### Phase 2: Obstruction-or-Construction Test

Attack the minimal configuration directly.

The exploration goal here is not "understand the geometry better." It is one of:

- prove a leakage lower bound,
- prove a rigidity statement preventing the required dominance hierarchy,
- or exhibit a concrete choice of modes/helicities where unwanted couplings stay below the admissible threshold and the Tao-like hierarchy is realized.

Accept analytical, computational, or mixed work, but the output must be quantitative.

Preferred proof/test shape:

- state one candidate theorem or one candidate construction first,
- then derive or compute the exact coefficient ratios needed to accept or reject it.

Failure path:

- If the obstruction reduces to a restatement of "many couplings exist" without a lower bound or domination failure, it does not count.
- If a near-circuit construction works in the chosen exact model, the firewall idea is killed unless an exact-NS fidelity issue remains explicit and serious.

### Phase 3: Mandatory Adversarial Verification

Whatever Phase 2 finds, run an adversarial pass that specifically tries to break it.

If the main result is a no-circuit claim, adversarial tasks should try to:

- find a different helical/geometric arrangement that evades the claimed leakage bound,
- identify hidden freedom in the definition that makes the impossibility statement vacuous,
- check whether the claimed spectator couplings can cancel rather than add.

If the main result is a construction, adversarial tasks should try to:

- expose omitted exact couplings,
- show the construction only works in a simplified model not faithful to exact NS,
- or demonstrate that the required hierarchy collapses under the stated tolerances.

### Phase 4: Mission-Level Verdict

Finish with exactly one of:

1. concrete no-circuit theorem candidate,
2. concrete near-circuit counterexample,
3. definition-level failure: idea too vague or too unconstrained.

The final report must make the implication unambiguous:

- pursue this as a real obstruction,
- kill the firewall idea,
- or stop because the object itself is not well-posed.

## Cross-Phase Rules

1. One theorem target or one construction target per exploration. State it before doing derivations.
2. Exact-NS fidelity is non-negotiable. Any helical simplification must be written as an exact reformulation, not a toy model in disguise.
3. Distinguish rigorously between:
   - Tao's reconstructed five-stage mechanism,
   - the candidate circuit definition,
   - the exact NS interaction law used to test it.
4. Every substantial claim in the final report must be tagged `[VERIFIED]`, `[COMPUTED]`, `[CHECKED]`, or `[CONJECTURED]`.
5. Maintain a Direction Status Tracker in `REASONING.md` with `OPEN / PROMISING / CLOSED / EXHAUSTED`.
6. Do not re-open estimate-level dead routes. De Giorgi, pressure rewrite, host-space compactness, and BKM/enstrophy programs are background constraints only.
7. Quantitative content is mandatory. "Exact NS has too much coupling" is never a deliverable by itself.
8. Before accepting any obstruction claim, run a cheap counterexample screen: try at least one adversarial mode/helicity arrangement designed to suppress the alleged leakage.
9. Before accepting any construction claim, list the exact spectator terms that remain and compare them explicitly against the leakage threshold from Phase 0.

## Validation Criteria

This strategy succeeds if it delivers all of:

- a concrete definition of "near-closed Tao circuit" that is narrow enough to be testable,
- an exact interaction table for a minimal Tao-like subsystem in Fourier/helical NS,
- either a leakage lower bound / impossibility statement or an explicit near-circuit construction,
- a mandatory adversarial check on the main result,
- an unambiguous pursue/kill/reformulate verdict.

This strategy is exhausted if:

- the definition gate fails cleanly, or
- the obstruction/construction question is answered for the preferred minimal configuration and the adversarial pass does not reopen it, or
- the remaining uncertainty is clearly identified as a sharper next-strategy question rather than more of the same work.

## Context

### Predecessor results to preload

- `execution/instances/anatomy-of-averaged-ns-blowup-firewall/strategies/strategy-001/FINAL-REPORT.md`
  - Tao's averaged blowup is a five-mode delayed-threshold circuit, not just a forward cascade.
  - The only live exact-NS discrepancy is circuit non-isolability.
  - That discrepancy split into triadic coefficient rigidity, unavoidable spectator couplings, and exact Leray-projection rigidity.
- `execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION-COMPLETE.md`
  - This follow-up mission exists specifically to formalize and test the no-near-closed-circuit idea.
- `execution/agents/library/meta/missionary/strategy-001-navier-stokes-learnings.md`
  - Ground-clearing strategies should produce cross-phase computable deliverables and not rely on qualitative synthesis alone.
- `execution/agents/library/meta/missionary/strategy-002-navier-stokes-learnings.md`
  - Use a clear phase gate and theorem-first exploration structure.

### What is already closed

- estimate-level improvement missions,
- generic pressure or frame rewrites,
- host-space reformulations without a concrete mechanism object,
- mechanism descriptions that never sharpen into a quantitative exact-NS statement.

### Strategic aim

The only live question is whether Tao's engineered near-isolated gate logic is genuinely incompatible with exact NS triadic/helical geometry, or whether that incompatibility disappears once the object is stated precisely.

## Budget Guidance

Target 4-6 explorations.

Expected efficient path:

- 1 exploration for the definition gate,
- 1 exploration for the exact interaction audit,
- 1-2 explorations for obstruction or construction testing,
- 1 exploration for adversarial verification and synthesis.

Early stopping is correct if the definition fails cleanly or if a quantitative obstruction/counterexample appears early and survives adversarial review.
