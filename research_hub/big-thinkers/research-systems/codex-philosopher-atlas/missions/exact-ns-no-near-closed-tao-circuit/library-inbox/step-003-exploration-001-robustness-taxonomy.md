# Exploration 001 Report - Freeze The Step-3 Robustness Taxonomy

## Goal

Freeze one source-grounded transformation taxonomy for the Step-3 robustness
audit of the three promoted Step-2 candidates:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`
- `Delayed-Threshold Itinerary`

The taxonomy must distinguish:

1. true exact symmetries
2. fixed canonicalization choices
3. substantive model changes

It must also state, candidate by candidate, which parts of the frozen packet /
candidate / gate sheets must be invariant under exact symmetries, which
dependencies are acceptable only because they were frozen earlier, and which
changes should count as a different model rather than a harmless rewrite.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-001-candidate-family.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`
- `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`
- `library/factual/tao-circuit-feature-ledger/admissible-leakage-must-be-declared-but-is-a-branch-level-policy-choice.md`
- `library/meta/obstruction-screening/separate-true-symmetries-canonicalization-and-substantive-object-changes-before-claiming-support-stability.md`

## Findings Log

### Initial Setup

- Started from the exploration directory and verified the required mission files
  are present in the repository.
- The prompt referenced repository instructions through `AGENTS.md`, but that
  file is not present at the repository root on disk. I followed the
  instructions embedded in the task message instead. [VERIFIED]

### Symmetry-Ledger Search

- The local Step-1 / Step-2 / library packet-policy record is much more
  explicit about what is **not** cosmetic than about a large menu of nontrivial
  exact symmetries. [VERIFIED]
- The local record therefore supports freezing a **narrow** exact-symmetry
  class and pushing everything else either into up-front canonicalization or
  into substantive model changes. [INFERRED]
- The only locally explicit transformation formulas I found were:
  Tao's averaged use of transformed copies of the ordinary bilinear form via
  `Rot_R`, `Dil_λ`, and order-zero multipliers `m(D)`,
  plus the exact bilinear scaling law
  `<B(Dil_λ u, Dil_λ v), Dil_λ w> = λ^(5/2) <B(u,v), w>`. [VERIFIED]
- The same search reinforced the negative lesson that bare rescaling is not a
  harmless rewrite unless the **full** NS scaling data is transported, and that
  conjugate completion, helical-basis changes, and packet regrouping should not
  be presumed cosmetic. [VERIFIED]

## Frozen Transformation Taxonomy

### A. True Exact Symmetries

- `[VERIFIED]` A separate exact-symmetry tier is required. Later candidate
  judgments must distinguish it from canonicalization and from substantive model
  drift. Support:
  `steps/step-001/RESULTS.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`,
  `library/meta/obstruction-screening/separate-true-symmetries-canonicalization-and-substantive-object-changes-before-claiming-support-stability.md`,
  `planning-runs/run-001/judgments/chain-01.md`.
- `[INFERRED]` For the **canonical one-bridge role-labeled helical packet
  family with mandatory conjugate completion**, the exact-symmetry class should
  be frozen narrowly:
  only transformations already justified as exact NS symmetries **and** still
  preserving the whole role-labeled packet family should count here. Support:
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `planning-runs/run-001/judgments/chain-01.md`.
- `[INFERRED]` **Role-preserving rigid rotation of the whole packet geometry**
  counts as a true exact symmetry:
  rotate the entire wavevector packet, transport the vector amplitudes and the
  mandatory conjugate completion with it, and keep the same role ledger.
  The local support is indirect but real:
  Tao's averaged operator is written as an average over transformed copies of
  the ordinary bilinear form using `Rot_R`, and the packet policy says the
  exact-symmetry list should be restricted to transformations already justified
  for the chosen packet presentation. Support:
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`.
- `[INFERRED]` **Full coupled dilation / NS scaling of the whole packet sheet**
  counts as a true exact symmetry only if the whole sheet is transported
  together:
  packet geometry,
  amplitudes / normalization,
  and time scaling.
  The local record supports the scaling law itself, and separately warns that
  bare rescaling without the full NS scaling data is not a harmless rewrite.
  Support:
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `planning-runs/run-001/attacks/chain-01.md`.
- `[PROPOSED]` No broader symmetry class should be admitted at Step 3 without
  extra local justification.
  In particular, this exploration does **not** quotient by:
  phase rotations,
  helical-basis changes,
  conjugate-representative changes,
  packet regroupings,
  sign-sheet swaps,
  or Tao's averaged freedoms such as order-zero multipliers.
  Those belong elsewhere in the taxonomy below. Support:
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `planning-runs/run-001/attacks/chain-01.md`,
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`.

### A.1 What The Symmetry Tier Must Preserve

- `[INFERRED]` The symmetry tier must preserve the **packet identity**:
  a finite role-labeled helical packet, with mandatory conjugate completion only
  as canonical real-valued bookkeeping. Support:
  `steps/step-001/RESULTS.md`,
  `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`.
- `[VERIFIED]` It must preserve the **shared five-channel interaction core**
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`,
  together with the forced extras
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
  Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.
- `[INFERRED]` It must preserve the **truth value** of each candidate and its
  downstream gate after transporting the entire packet / candidate / gate sheet
  through the symmetry, not merely preserve a slogan-level resemblance.
  Support:
  `planning-runs/run-001/judgments/chain-01.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.

### B. Fixed Canonicalization Choices

- `[VERIFIED]` Conjugate completion is mandatory in the canonical
  representation, but it is not the packet's primary identity. Support:
  `steps/step-001/RESULTS.md`,
  `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`.
- `[INFERRED]` The frozen Step-1 / Step-2 canonicalization sheet consists of:
  one conjugate-representative convention,
  one helical basis convention,
  one role-label ordering,
  one amplitude normalization anchor,
  one phase anchor or equivalent canonical gauge,
  and one declared sign sheet carried consistently through the bookkeeping.
  Support:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`.
- `[INFERRED]` Under that frozen policy, the following are merely
  canonicalization:
  reordering role labels after the order is fixed,
  displaying the mandatory conjugate packet explicitly versus implicitly,
  and changing the chosen conjugate representative without changing the
  completed real-valued packet.
  Support:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`.
- `[INFERRED]` **Sign-sheet bookkeeping** is canonicalization only in the weak
  sense of carrying along the already declared sign sheet consistently.
  It does **not** mean the sign sheet may be replaced later.
  Support:
  `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`.
- `[VERIFIED]` Dependence on these choices is acceptable only because the
  choices were frozen up front in Step 1 and inherited uniformly by Step 2.
  Dependence on them is not automatically fatal; hidden drift in them is.
  Support:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `planning-runs/run-001/judgments/chain-01.md`.

### B.1 What Must Survive Canonicalization

- `[VERIFIED]` Tao-likeness is judged only after canonicalization, and five
  things must survive:
  identifiable roles,
  ordered delayed-threshold sequence,
  dominant-channel hierarchy,
  phase / helical-sign bookkeeping tight enough to prevent representation
  drift,
  and a declared admissible-leakage rule on a declared finite window.
  Support:
  `steps/step-001/RESULTS.md`,
  `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`.

### C. Substantive Model Changes

- `[VERIFIED]` The following moves count as substantive model changes rather
  than harmless rewrites:
  packet regrouping,
  support-semantics changes,
  treating conjugate completion as optional,
  threshold retuning,
  time-window changes,
  changing the helical sign sheet,
  and changing the relative phase sheet.
  Support:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`,
  `planning-runs/run-001/attacks/chain-01.md`.
- `[INFERRED]` Changing the **spectator partition** is also substantive for this
  branch.
  In Step 2, `Windowed Spectator-Leakage Budget` froze
  `mirror`,
  `companion`,
  `feedback`,
  `cross`
  as the classes themselves, not as a later reporting convenience. Changing
  that partition changes the modeled leakage object. Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`,
  `steps/step-003/GOAL.md`.
- `[INFERRED]` Importing Tao's averaged freedoms by hand is substantive, not
  canonical.
  The exact-NS / Tao comparison is only meaningful after quotienting true exact
  symmetries and one fixed canonical packet sheet.
  If a candidate only survives after adding averaged-circuit freedoms such as
  retunable gate strengths or multiplier freedom, that is a different model.
  Support:
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`,
  `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`.
- `[VERIFIED]` Threshold retuning after outcomes are seen is especially fatal:
  the attack packet names tuned thresholds and cherry-picked time windows as
  genuine circularity routes, not benign repair moves. Support:
  `planning-runs/run-001/attacks/chain-01.md`,
  `steps/step-001/RESULTS.md`.

## Candidate-Facing Invariance Sheet

### Shared Across All Three Promoted Candidates

- `[VERIFIED]` All three candidates share the same packet object:
  one canonical one-bridge role-labeled helical packet family with mandatory
  conjugate completion.
  They also share the same exact five-channel core and the same forced
  spectator classes.
  Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.
- `[INFERRED]` Therefore, for **every** promoted candidate:
  the packet object and candidate truth value must be invariant under the
  narrow true-symmetry tier above;
  may depend on the frozen canonicalization sheet only because that sheet was
  fixed up front;
  and must count as a different model if packet semantics, packet grouping,
  spectator partition, thresholds, windows, sign sheets, or Tao-like freedoms
  are altered.
  Support:
  `steps/step-001/RESULTS.md`,
  `steps/step-002/RESULTS.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`.

### 1. `Template-Defect Near-Closure`

- `[VERIFIED]` The invariant content is:
  one role-labeled packet object,
  one five-channel core,
  one finite activation window,
  and one downstream defect gate
  `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`.
  Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-001-candidate-family.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.
- `[INFERRED]` Under true exact symmetries, what must remain invariant is the
  **candidate truth value**:
  whether the transformed exact packet stays within the same template-defect and
  spectator-defect tolerances when the whole packet / criterion / gate sheet is
  transported coherently.
  Support:
  `planning-runs/run-001/judgments/chain-01.md`,
  `steps/step-002/RESULTS.md`.
- `[INFERRED]` Acceptable frozen canonicalization dependence:
  one helical sign sheet,
  one amplitude anchor,
  one phase anchor,
  one conjugate-representative convention,
  one helical basis,
  one role order.
  This candidate is allowed to be only "stable after canonicalization" because
  Step 2 explicitly built it on one canonical packet family and one
  role-normalized template.
  Support:
  `steps/step-002/RESULTS.md`,
  `steps/step-001/RESULTS.md`,
  `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`.
- `[VERIFIED]` The following count as **different models**, not rewrites:
  changing the role hierarchy sheet
  `(h_seed, h_clk, h_amp, h_rot, h_next)`,
  changing `lambda_tmpl` or `lambda_spec`,
  changing `T_act`,
  regrouping packets,
  changing support semantics,
  swapping sign sheets,
  or importing Tao's averaged gate freedoms to improve the fit.
  Support:
  `steps/step-002/RESULTS.md`,
  `steps/step-001/RESULTS.md`,
  `planning-runs/run-001/attacks/chain-01.md`,
  `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`.

### 2. `Windowed Spectator-Leakage Budget`

- `[VERIFIED]` The invariant content is:
  the same packet object,
  the same on-template five-channel denominator ledger,
  the same four spectator classes,
  one fixed window,
  and one downstream admissibility sheet
  `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`.
  Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.
- `[INFERRED]` Under true exact symmetries, what must remain invariant is again
  the candidate truth value:
  whether the same transformed packet passes the same leakage sheet when judged
  in the same interaction currency.
  Support:
  `steps/step-002/RESULTS.md`,
  `planning-runs/run-001/judgments/chain-01.md`.
- `[INFERRED]` Acceptable frozen canonicalization dependence:
  one sign / amplitude / phase sheet,
  one conjugate-completion convention,
  and whatever representative choices are fixed by the common packet policy.
  Support:
  `steps/step-002/RESULTS.md`,
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`.
- `[VERIFIED]` The following count as **different models**, not rewrites:
  changing the spectator partition,
  changing the definition of `D_on` or `D_off`,
  changing `Lambda_tot` or the class budgets,
  changing `T_act`,
  changing support semantics,
  regrouping the packet,
  or recoding the same packet under a different sign sheet.
  Support:
  `steps/step-002/RESULTS.md`,
  `steps/step-003/GOAL.md`,
  `planning-runs/run-001/attacks/chain-01.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`.

### 3. `Delayed-Threshold Itinerary`

- `[VERIFIED]` The invariant content is:
  the same packet object,
  the same ordered five-channel mechanism,
  one fixed activation window,
  the same ordered event logic
  `clock -> trigger -> rotor -> next-stage transfer`,
  and one downstream gate
  `G_itin(P_n; I) = (t_clk, t_trig, t_rot, t_next; sign sheet; spectator pass/fail)`.
  Support:
  `steps/step-002/RESULTS.md`,
  `library-inbox/step-002-exploration-001-candidate-family.md`,
  `library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`.
- `[INFERRED]` Under true exact symmetries, what must remain invariant is the
  existence of the ordered itinerary with the same gate logic.
  For any symmetry that rescales the whole sheet, the honest invariant is the
  existence of the correspondingly transported ordered event tuple, not the
  literal unchanged numeric timestamps inside the unscaled sheet.
  Support:
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `steps/step-002/RESULTS.md`.
- `[INFERRED]` Acceptable frozen canonicalization dependence:
  one sign sheet,
  one amplitude anchor,
  one phase anchor,
  one role order,
  one conjugate-completion rule.
  This candidate is the most visibly phase- and sign-sensitive, but that is not
  disqualifying by itself because Step 1 explicitly froze those bookkeeping
  needs rather than pretending they vanish.
  Support:
  `steps/step-001/RESULTS.md`,
  `steps/step-002/RESULTS.md`,
  `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`.
- `[VERIFIED]` The following count as **different models**, not rewrites:
  retuning
  `theta_B, theta_C, theta_D, theta_E, Lambda_itin, kappa_rot`,
  changing `T_act`,
  redefining the spectator screen,
  changing the sign sheet,
  regrouping the packet,
  or importing Tao's delayed-threshold freedoms by hand.
  Support:
  `steps/step-002/RESULTS.md`,
  `steps/step-003/GOAL.md`,
  `planning-runs/run-001/attacks/chain-01.md`,
  `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`.

## Consolidated Takeaway

- `[VERIFIED]` The frozen packet object is:
  the canonical one-bridge role-labeled helical packet family with mandatory
  conjugate completion, one shared five-channel core, and one fixed
  candidate-by-candidate gate sheet. Support:
  `steps/step-001/RESULTS.md`,
  `steps/step-002/RESULTS.md`.
- `[INFERRED]` The sharpest Step-3 discipline is:
  require invariance under a **narrow** exact-symmetry tier,
  tolerate dependence on the frozen canonicalization sheet only because it was
  declared up front,
  and count packet regrouping, support changes, spectator re-partitioning,
  threshold / window retuning, sign-sheet swaps, and Tao-style averaged
  freedoms as different models.
  Support:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`,
  `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`.

## Failed Attempts And Dead Ends

- Repository-level `AGENTS.md` was not found on disk at the stated root path, so
  no additional on-disk instructions could be read from that file. This did not
  block the task because the user message already included the relevant
  instructions. [VERIFIED]
- The local record did **not** contain one precompiled positive list of exact
  symmetries for the frozen packet presentation. Most sources instead focused on
  separating canonicalization and substantive drift. This forced a narrow,
  conservative symmetry freeze rather than an expansive one. [VERIFIED]
- I did not find local support for treating phase rotations, helical-basis
  changes, conjugate-representative changes, or packet regrouping as true exact
  symmetries of the frozen candidate sheets. Those were therefore classified
  outside the exact-symmetry tier. [INFERRED]

## Status

Source extraction complete. Taxonomy frozen for later Step-3 candidate audit.
