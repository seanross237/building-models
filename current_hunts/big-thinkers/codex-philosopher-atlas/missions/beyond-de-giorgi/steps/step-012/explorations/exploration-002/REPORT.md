# Exploration 002 Report

## Goal

Fix the prior-art comparator and anti-repackaging burden for the stochastic branch, or say plainly that the repository never built a concrete enough comparator packet to keep the branch alive.

## Method

- Inspect the required local repository sources named in the task.
- Extract every explicit stochastic comparator candidate and any theorem-facing claims attached to it.
- Separate already-standard content from any beyond-baseline gain the branch would need.
- Formulate a concrete anti-repackaging rule in the branch's own burden language.

## Source Log

- Started report skeleton.
- Read `missions/beyond-de-giorgi/steps/step-012/GOAL.md`.
- Read `missions/beyond-de-giorgi/CHAIN.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-007/planner-chains/chain-04.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-008/refined/chain-03.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-008/attacks/chain-03.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-008/judgments/chain-03.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-008/final-decider.md`.
- Read `missions/beyond-de-giorgi/planning-runs/run-007/attacks/chain-01.md`.
- Searched the broader `missions/beyond-de-giorgi` tree for `Constantin`,
  `Iyer`, `stochastic circulation`, `back-to-label`, `backward-flow`,
  `filtration`, `expectation`, `localization`, and `comparator`.

## Findings In Progress

### Comparator Candidates

[VERIFIED] The only explicitly person-named stochastic comparator on disk is
`Constantin-Iyer`, and it appears only as one menu item inside the old
run-007 chain setup: "a Constantin-Iyer representation term" sits alongside "a
stochastic circulation identity" and "a stochastic back-to-label observable"
in `planning-runs/run-007/planner-chains/chain-04.md:23-34`. The current step
reasoning separately records that "`Constantin-Iyer` appears as the only
explicitly named stochastic comparator neighborhood on disk" in
`steps/step-012/REASONING.md:24-31`.

[VERIFIED] The active chain and the refined chain require a concrete prior-art
baseline, but they do not themselves supply one beyond this neighborhood-level
naming. Both `CHAIN.md:27-57` and
`planning-runs/run-008/refined/chain-03.md:34-55` demand "the closest known
stochastic Navier-Stokes representation and the exact gain claimed beyond it,"
but neither file names a theorem, paper, or theorem-facing comparator packet.

#### Comparator Table

| candidate comparator | status | already standard | required new gain | overlap verdict |
| --- | --- | --- | --- | --- |
| `Constantin-Iyer representation term` | [VERIFIED] only explicitly named stochastic comparator neighborhood on disk; appears as a menu item, not a built comparator memo | [VERIFIED] exact stochastic transport / viscous-Lagrangian reformulation is treated as known terrain; [VERIFIED] the record repeatedly treats exactness alone as common and strategically insufficient | [VERIFIED] one sign, exclusion principle, monotonicity surrogate, or local/pathwise control that constrains a named concentration or stretching burden and survives localization/stopping/filtration debt | [INFERRED] closest comparator, but the local record never builds the exact theorem-facing gap packet needed to clear overlap |
| `stochastic circulation identity` | [VERIFIED] generic family label only; no theorem or exact comparator statement attached | [INFERRED] exact circulation-style stochastic packaging and possible expectation-level / martingale bookkeeping are part of the same known exact-but-nonclosing neighborhood | [VERIFIED] a localizable concentration-exclusion or stretching-control consequence, not just an expectation estimate | [INFERRED] too generic to clear prior-art burden; high repackaging risk |
| `backward-flow / back-to-label observable` | [VERIFIED] generic family label only; appears in menus but not as a frozen prior-art theorem | [INFERRED] exact back-to-label / Cauchy-type stochastic reformulation is part of the same known representation neighborhood | [VERIFIED] endpoint-facing control that remains usable near singularity without smooth-flow or strong-filtration collapse | [INFERRED] comparator naming remains menu-level; overlap unresolved |
| generic `exact martingale transport statement` / `viscous-Lagrangian neighborhood` | [VERIFIED] literature neighborhood only | [VERIFIED] exact stochastic representation distinct from Eulerian estimates is acknowledged as real, but theorem leverage is not standardly earned from that fact alone | [VERIFIED] mechanism-facing leverage stronger than deterministic rewrite and not destroyed by localization or parasitic imports | [INFERRED] anti-repackaging obstruction already active if no sharper comparator is built |

### Standard Baseline on Repository Record

[VERIFIED] The repository's standard baseline is not a theorem-facing gain but
the availability of exact stochastic reformulation itself. The old chain asks
whether the object yields "pathwise control, conditional-expectation control,
cancellation, or only a reformulation" and explicitly rejects routes that stay
at "representation-level exactness" in
`planning-runs/run-007/planner-chains/chain-04.md:51-62`.

[VERIFIED] The refined judgment makes the baseline even sharper:
"Exact stochastic identities are common; theorem-facing leverage is rare," and
the real discriminator is whether the formula yields "a sign, exclusion
principle, monotonicity surrogate, or local/pathwise control" beyond the
deterministic rewrite
(`planning-runs/run-008/judgments/chain-03.md:21-25`).

[VERIFIED] The local record also treats the failure pattern itself as already
known: "exact stochastic reformulation followed by nonclosure is a known
failure pattern" (`planning-runs/run-008/judgments/chain-03.md:61-64`), and
the attack spells out the familiar shape as "exact stochastic Lagrangian
reformulation, elegant martingale identity, some localized expectation
estimate, then no closure at critical regularity"
(`planning-runs/run-008/attacks/chain-03.md:71-73`).

[INFERRED] So the exact gain already standard on the repository record is:
exact stochastic transport / circulation / backward-flow representation, with
at most expectation-level or localized-martingale bookkeeping. The record does
not freeze any stronger comparator-side gain than that.

### Required Beyond-Baseline Gain

[VERIFIED] The active chain requires something strictly stronger than
expectation-level packaging: one-sided or exclusionary content, local or
pathwise consequence, stability under localization/stopping near singular
behavior, or a plausible gain over known deterministic or stochastic
reformulations (`CHAIN.md:5-12`).

[VERIFIED] The refined chain and judgment make the needed gain concrete. The
branch would need one observable that yields a sign, exclusion principle,
monotonicity surrogate, or conditional reduction of the named bad term before
generic inequalities erase the structure
(`CHAIN.md:61-66`; `planning-runs/run-008/judgments/chain-03.md:24-25`).

[VERIFIED] The same sources also specify where that gain must land: local
concentration exclusion is the default first endpoint, while continuation
criteria are allowed only if the observable already behaves like near-coercive
norm control (`CHAIN.md:40-42`;
`planning-runs/run-008/judgments/chain-03.md:73-79`).

[INFERRED] Relative to the named `Constantin-Iyer` neighborhood, the branch
would need at least one theorem-facing gain of the following form:

- a local/pathwise estimate, not only expectation or conditional expectation;
- tied to one named concentration or stretching bottleneck;
- surviving stopping-time, filtration, localization, and reconstruction debt;
- and not obtained by importing a stronger framework whose real content is just
  the original deterministic burden in another language.

[INFERRED] Without that, the branch is only replaying a known exact-but-
nonclosing stochastic reformulation.

### Anti-Repackaging Rule

[VERIFIED] The branch's own burden language already contains the core rule:
"stochastic reformulation does not count if its usable content is only the
deterministic burden restated through expectation, filtration, or imported
machinery" (`CHAIN.md:43-44`).

[VERIFIED] The attack and judgment sharpen how to enforce that mechanically:

- expectation-only gain with no pathwise or local coercive consequence is a
  distinct failure bucket (`planning-runs/run-008/attacks/chain-03.md:49-50`;
  `planning-runs/run-008/judgments/chain-03.md:39-40`);
- stronger frameworks are parasitic if they merely smuggle back the
  deterministic hard part (`planning-runs/run-008/attacks/chain-03.md:43`;
  `planning-runs/run-008/judgments/chain-03.md:34`);
- filtration, stopping-time, and smooth-flow dependence must be charged early,
  because the representation may collapse near the singular regime precisely
  there (`CHAIN.md:71-84`;
  `planning-runs/run-008/judgments/chain-03.md:64-69`);
- the final decider preserves this as an explicit anti-repackaging standard so
  "stochastic elegance is not allowed to function as mere representational
  theater" (`planning-runs/run-008/final-decider.md:54-57`).

#### Mechanical Anti-Repackaging Rule

[INFERRED] Kill the branch as `anti-repackaging collapse` if, after fixing the
comparator and writing the candidate identity, every usable consequence falls
into any of these buckets:

1. only expectation or conditional-expectation control, with no stated local or
   pathwise consequence on the named concentration/stretching burden;
2. only filtration/stopping/localization bookkeeping, with the apparent gain
   disappearing once singular-regime debt is charged;
3. only a claim available after importing smoother stochastic flows, stronger
   filtrations, or regularity machinery whose substantive content is the
   original deterministic hard part.

[INFERRED] This is concrete enough for Step 2 enforcement because each bucket
maps directly onto the chain's failure labels:
`expectation-only gain`, `localization collapse`, `solution-class mismatch`, or
`parasitic import`.

### Dead Ends / Failed Attempts

- [VERIFIED] Repository-wide search found no local file that upgrades
  `Constantin-Iyer` from a menu item into a comparator theorem, exact theorem
  statement, or explicit "already standard vs. new gain" packet.
- [VERIFIED] The required source set repeatedly demands a prior-art baseline and
  exact gap, but the archive never supplies that gap concretely; it keeps the
  burden at the level of a planning requirement (`GOAL.md:38-41, 80-86`;
  `CHAIN.md:36-57`; `refined/chain-03.md:36-55`).
- [INFERRED] Because the local record never gets beyond comparator naming plus a
  known nonclosure warning, there is no source-backed way to keep the branch
  alive by pretending the comparator burden has already been discharged.

## Provisional Status

[VERIFIED] `GOAL.md` says Step 12 should stop before Chain Step 2 if it cannot
freeze one closest comparator and one concrete beyond-prior-art claim
(`steps/step-012/GOAL.md:16-27, 80-86, 95-104`).

[INFERRED] That failure has already happened on the local record for the
stochastic comparator burden. The archive supports the stochastic neighborhood,
and it supports the known failure pattern
`exact reformulation -> expectation/localization nonclosure`, but it does not
build a concrete enough comparator packet to say what theorem-facing gain would
actually surpass the named baseline.

## Conclusion

[INFERRED] Final conclusion for this exploration:
`prior-art / anti-repackaging obstruction already active`.

[INFERRED] The closest comparator that is actually named on disk is the
`Constantin-Iyer` representation neighborhood, but the repository never turns
that name into a usable theorem-facing comparator memo. What is already
standard on the record is exact stochastic reformulation, possibly with
expectation-level or localized martingale bookkeeping, plus the known failure
pattern that such reformulations often do not close. To keep the branch alive,
the repository would need a sharper local/pathwise, mechanism-facing gain that
survives filtration, stopping, localization, and import debt. No such gain is
frozen locally. On the present record, the honest output is obstruction rather
than baseline-and-gap closure.
