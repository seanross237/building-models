# Exploration 001 Report

## Goal

Decide whether this mission admits one preferred exact-NS helical packet/sign object that is canonical enough to support later quantitative work, or whether the exploration ends in a clean canonicity failure.

## Executive Verdict

[CHECKED] Verdict: `canonicity failure`.

[CHECKED] The new `SD_part` / `SD_target` split sharpens the sign language, but it does **not** repair the predecessor packet-object failure. The packet/sign object still moves under:

- packet support and refinement choices,
- conjugate-pair representative choice for global sign bookkeeping,
- desired-triad witness bookkeeping,
- and the induced exact-ledger leakage split.

[CHECKED] Strategy implication: stop at Phase 0. Later quantitative work would still be testing a moving target rather than one theorem-facing exact-NS object.

## Sources Loaded

- [CHECKED] mission and strategy files for `exact-ns-helical-sign-bottleneck`
- [CHECKED] `exact-helical-near-closed-tao-circuit-definition.md`
- [CHECKED] `packetized-tao-circuit-noncanonical.md`
- [CHECKED] `exact-ns-triadic-coefficient-rigidity.md`
- [CHECKED] `exact-ns-unavoidable-spectator-couplings.md`
- [CHECKED] `strategy-001-exact-ns-no-near-closed-tao-circuit-learnings.md`
- [CHECKED] `definition-extraction-gates-computation.md`
- [CHECKED] `coefficient-weighted-amplitude-level-leakage.md`
- [CHECKED] `check-faithful-support-shrinkage-before-narrowing.md`
- [CHECKED] `build-adversarial-suppression-into-first-audit.md`
- [CHECKED] the helical sign prototype `summary.md` and `packet-functional-sketch.md`
- [CHECKED] predecessor exact-NS packet reports, especially exploration 003 on packet non-canonicity

## Decision Logic

### 1. What is genuinely new in this mission

[CHECKED] The predecessor line had already reached a sharp negative on the packet backup: after singleton failure, packetization remained an underconstrained family of support, projection, leakage, and restoration choices rather than one exact object.

[CHECKED] The new mission adds one real ingredient:

```text
replace one vague sign-defect scalar by two visible quantities
(SD_part, SD_target).
```

[CHECKED] That is a meaningful refinement of the *obstruction language*, but it only helps if those new functionals are themselves canonical on one frozen packet object.

### 1a. What the reduced packet summary preserves and discards

[CHECKED] The candidate packet/sign summary preserves:

- exact helical triad coefficients and exact triad constraints,
- coefficient-weighted absolute-magnitude ledger terms,
- finite sign-closed exact support,
- the five Tao-like role labels,
- separate bookkeeping for global sign coherence and desired-edge heterochirality.

[CHECKED] It discards or leaves unresolved:

- one unique exact support table,
- one unique packet refinement convention,
- one unique desired-triad witness set inside each role edge,
- one intrinsic sign label on each conjugate-pair quotient family.

### 2. Packet support is still not canonically fixed

[CHECKED] The inherited singleton obstruction only says that some packet enlargement is necessary. It does **not** identify one preferred repair.

[CHECKED] Many inequivalent packet enlargements remain alive:

- split the carrier packet to realize distinct pump and seed outputs,
- enlarge one or both target packets,
- enlarge several roles simultaneously to recover amplifier and handoff structure,
- or choose different minimal-cardinality exact supports with the same role graph.

[CHECKED] The sign prototype does not collapse that freedom. It says something about helicity organization *once a support has been chosen*; it does not canonically choose the packet support or refinement convention itself.

### 3. `SD_part` is not representative-invariant

[CHECKED] The prototype definition of `SD_part` explicitly says it should be computed on a fixed representative of each conjugate-pair family. That is exactly the problem.

[CHECKED] For a real-valued exact helical ledger, the quotient family

```text
{(k, sigma), (-k, -sigma)}
```

is canonical, but the sign label of the family is not. Switching the representative from `(k, sigma)` to `(-k, -sigma)` leaves the exact solution and all exact triad magnitudes unchanged while flipping the sign attached to that family.

[CHECKED] There are only two possible bookkeeping responses, and both fail:

1. Count both members of every sign-closed pair. Then conjugation pairs each ledger contribution with an equal-weight opposite-sign contribution, so the global sign balance trivializes and `SD_part` becomes a constant rather than a meaningful defect.
2. Quotient by conjugate pairs. Then the pair is canonical but its sign is not, because the representative choice flips the assigned sign with no change in exact NS data.

[CHECKED] Under the quotient definition, write

```text
SD_part^R(I) = min(W_+^R, W_-^R) / (W_+^R + W_-^R),
```

for a representative rule `R`, where

```text
w_m := ∫_I Part_m(t) dt > 0,
W_±^R := Σ_{m : sign_R(m) = ±} w_m.
```

[CHECKED] Perform the required harmless representative-relabeling test on one family `m0`:

- choose representatives so every family is labeled `+`; then `W_- = 0` and `SD_part = 0`;
- flip only the representative of `m0`; then the same exact family now contributes to `W_-`, so

```text
W_- = w_{m0},
SD_part = min(w_{m0}, W - w_{m0}) / W,
W := Σ_m w_m.
```

[CHECKED] For any nontrivial packet object with `0 < w_{m0} < W`, `SD_part` changes strictly while the exact support, exact solution segment, and exact triad magnitudes do not change at all.

[CHECKED] Therefore `SD_part` is not invariant unless an extra orientation or chirality convention is imposed from outside the exact packet ledger. No such convention was supplied, and imposing one would add new arbitrary structure rather than remove it.

### 4. `SD_part` also moves under harmless packet refinement

[CHECKED] The participation weight

```text
Part_m(t) = sum_{tau touches m} W_tau(t)
```

depends on the chosen active mode families `m`. If a packet is harmlessly refined into subfamilies with the same union support and the same Tao-role label, then the list of families `m` changes and the participation mass is redistributed across them.

[CHECKED] Without a canonically fixed refinement rule, the global minority-helicity participation defect can move even when the underlying exact support union and exact solution segment are unchanged.

### 5. `SD_target` and `Leak` still depend on non-canonical desired-edge bookkeeping

[CHECKED] To define `SD_target`, one must first define the exact target-triad set `T_target` realizing the Tao-role graph on packets.

[CHECKED] That choice is not canonical:

- if *all* role-compatible exact triads inside the packets count as desired, then harmless support refinement changes the desired set and can reclassify what used to be internal packet interaction as desired drive;
- if only a selected witness subset counts as desired, then the witness choice is arbitrary and representative-dependent.

[CHECKED] The same instability propagates to `Leak(I)` because the exact desired / internal-leakage / external-leakage split is defined relative to that target set.

[CHECKED] This is precisely where the predecessor negative survives. The new split keeps `SD_target` separate from `SD_part`, which is correct, but it does not fix the target-triad ledger on which both `SD_target` and `Leak` depend.

[CHECKED] So the leakage functional remains canonical only as a template, not as one concrete exact object.

### 6. Required adversarial harmless-change check

[CHECKED] Representative relabeling test:

- start with any candidate quotient family `m = {(k,sigma), (-k,-sigma)}`;
- compute `Part_m` from exact triad magnitudes;
- switch the chosen representative from `(k,sigma)` to `(-k,-sigma)`.

[CHECKED] Result:

- exact NS data unchanged,
- exact triad magnitudes unchanged,
- `SD_target` unchanged if `T_target` is held fixed,
- but the sign attached to `m` flips, so `SD_part` changes unless an extra convention is added.

[CHECKED] Packet-refinement test:

- split one role packet into two subpackets with the same union support and same role label;
- keep the Tao role graph at the packet level unchanged.

[CHECKED] Result:

- either the desired exact-triad set changes, which changes both `SD_target` and `Leak`,
- or one selects a witness subset by hand, which makes the object depend on that non-canonical selection.

[CHECKED] So the object fails the required harmless-change screen.

## Outcome

[CHECKED] No preferred packet/sign object survived.

[CHECKED] No genuinely inequivalent backup survived either. Every backup was the same moving family of:

- packet support choices,
- representative/quotient choices,
- desired-edge witness choices,
- leakage-instantiation choices.

[CHECKED] Minimal list of load-bearing non-canonical freedoms:

1. conjugate-pair sign bookkeeping for `SD_part`;
2. packet support and refinement convention for the five Tao-like roles;
3. desired-edge witness bookkeeping inside refined packet roles;
4. the restored exact spectator ledger induced by those support and witness choices.

[CHECKED] The correct terminal label at this phase is:

```text
canonicity failure
```

[CHECKED] This is not yet a model-level failure. The singleton sign clue remains an interesting clue, but it never reaches a faithful frozen packet object on which Phase 1 could honestly be run.

[CHECKED] Why later quantitative work would otherwise be testing a moving target:

- `SD_part` would depend on representative choice rather than on exact NS data alone;
- `SD_target` and `Leak` would depend on support/refinement and desired-witness bookkeeping;
- different quantitative conclusions could therefore reflect object selection rather than a real packet-level theorem or counterexample.
