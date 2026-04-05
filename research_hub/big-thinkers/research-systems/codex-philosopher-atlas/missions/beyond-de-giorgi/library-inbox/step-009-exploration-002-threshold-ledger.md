# Exploration 002 Report

## Goal

Stress-test the cash-out, progress currency, and minimum threshold for the best endpoint candidate in step-009, staying estimate-level and endpoint-bound.

## Evidence Read

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/GOAL.md`
- [VERIFIED] `runtime/results/codex-patlas-standalone-20260331T152036Z-receptionist-42212.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-001-exploration-001-far-field-obstruction-reconstruction.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-001-exploration-002-tao-gate-pressure-branch.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/exact-surviving-far-field-pairing.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/bad-coefficient-stays-at-fixed-energy-scale.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/affine-and-higher-harmonic-modes-survive-as-moments.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/constant-harmonic-mode-is-automatically-killed.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/real-progress-requires-a-smaller-effective-coefficient.md`
- [VERIFIED] `library/factual/far-field-pressure-obstruction/pressure-tensor-identity-remains-only-a-narrow-testable-possibility.md`
- [VERIFIED] `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] `library/meta/obstruction-screening/when-one-bad-term-and-one-gain-currency-are-frozen-a-tao-screen-may-end-the-branch.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/selected/chain-01.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-006/judgments/chain-01.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/REASONING.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-009-exploration-001-endpoint-menu-freeze.md`

## Findings

### 1. Frozen endpoint context

- [VERIFIED] Exploration 001 already narrowed Step 1 to one actual theorem ledger: the inherited suitable-weak / Leray-Hopf plus local-energy inequality, CKN/Lin epsilon-regularity contradiction package, with the live bad term fixed as the far-field pressure pairing `I_p^far`.
- [VERIFIED] The exact live object is the full pairing
  `I_p^far = -∬ p_far div(v_k phi_k^2 e_hat)`,
  with operative inherited estimate
  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`
  and bad coefficient
  `C_far ~ ||u||_{L^2}^2 / r_k^3`.
- [VERIFIED] The branch standard from `CHAIN.md`, `winning-chain.md`, and the obstruction-screening notes is estimate-level: fix one bad term, one gain currency, and one minimum threshold that still matters after later reconstruction and localization debt.

### 2. Required answers

#### Q1. Exact positive deliverable

- [VERIFIED] The exact endpoint-attached positive deliverable is a full-pairing inequality on the inherited bad term, not a free-floating tensor identity:
  `|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}`.
- [INFERRED] The important content inside that deliverable is that `C_far,eff(k)` is genuinely smaller than the inherited fixed-energy-scale size `||u||_{L^2}^2 / r_k^3`.
- [INFERRED] Cancellation of a named harmonic-moment family is admissible only as the mechanism for obtaining that same improved full-pairing inequality. It is not a standalone cash-out.
- [VERIFIED] A representation identity such as `partial_i partial_j p = R_i R_j(u_i u_j)` stays below threshold unless it yields estimate-level shrinkage of the live coefficient.

#### Q2. Best-supported progress currency

- [VERIFIED] The best-supported currency is `quantified reduction of a specified nonlocal remainder`, namely reduction of the effective coefficient on the live far-field pairing.
- [INFERRED] Among the Step-009 menu options, this is stronger and more source-backed than `monotonicity`, which has no locally frozen monotone quantity tied to the endpoint, and more precise than `one-sided inequality`, which is the cash-out object rather than the discriminating currency inside it.
- [INFERRED] `cancellation of a named harmonic-moment family` survives only as a secondary mechanism language, and only if it cashes out as quantified shrinkage of `C_far,eff(k)` for the full pairing.

#### Q3. Minimum quantitative threshold to freeze now

- [VERIFIED] The threshold cannot be "better modulo constants" or any generic harmonic upgrade, because constants are already annihilated by the pairing and affine-and-higher harmonic modes remain live.
- [INFERRED] The minimum non-cosmetic threshold supported by the record is not merely "some improvement in spirit," but a positive-margin reduction of the live coefficient for the same full pairing.
- [PROPOSED] Freeze the threshold as:
  there exists `delta > 0` such that, after later reconstruction and any required localization debt are paid, the surviving endpoint inequality still has
  `|I_p^far| <= (1 - delta) (||u||_{L^2}^2 / r_k^3) 2^{12k/5} U_k^{6/5}`
  for the same full pairing and all relevant scales `k`, or an equivalent full-pairing estimate with net coefficient improvement by a uniform positive margin.
- [INFERRED] This is the sharpest faithful formalization of the repository's repeated requirements that the gain be "materially smaller," "same-protocol," and survive later debt "with positive margin."

#### Q4. Why that threshold is meaningful after later reconstruction and localization debt

- [VERIFIED] `CHAIN.md` and `winning-chain.md` require the Step-1 threshold to survive full reconstruction and any required localization losses; otherwise the branch is supposed to die at Step 5.
- [VERIFIED] The exact-rewrite screening note fixes the right standard: only a smaller effective coefficient in the same localized protocol counts once projection, Calderon-Zygmund, commutator, and related restoration costs are charged.
- [INFERRED] Therefore the proposed threshold is meaningful because it is not a gain on a surrogate object, a prettier identity before localization, or a different architecture. It is a net improvement on the same live bad term in the same theorem ledger after the bill is repaid.
- [INFERRED] That is precisely what separates real progress from coefficient-size rebranding: the coefficient being reduced is the already-frozen obstruction coefficient itself.

#### Q5. Source-backed negative tests against weaker thresholds

- [VERIFIED] `constant-mode quotienting` is too weak:
  the localization/test structure already kills constants, so quotienting by constants does not shrink the live obstruction.
- [VERIFIED] `generic harmonic regularity` is too weak:
  Harnack, Campanato, local `H^1`, derivative decay, and harmonic polynomial approximation remain inside Tao-preserved harmonic-analysis structure and do not count unless they shrink the actual bad coefficient.
- [VERIFIED] `algebraic rewrites or local geometry` are too weak:
  exact rewrites of `u . grad u` and local vorticity/strain geometry do not act directly on the surviving affine-and-higher harmonic moments of `p_far`; absent a new coefficient estimate they fail the branch gate.
- [VERIFIED] `partial or surrogate improvements` are too weak:
  a gain only on a local piece, a reduced model, or a representation-level defect that leaves the full pairing coefficient unchanged is explicitly screened out by both the far-field obstruction packet and the same-protocol rewrite audit.

### 3. Ledger

| candidate cash-out | currency | minimum threshold | why meaningful | failure mode of weaker version |
| --- | --- | --- | --- | --- |
| `[VERIFIED]` Full-pairing estimate `|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}` | `[VERIFIED]` Quantified reduction of the specified nonlocal remainder, i.e. the effective coefficient on `I_p^far` | `[PROPOSED]` Uniform positive-margin net shrinkage after later reconstruction/localization: `C_far,eff(k) <= (1-delta) ||u||_{L^2}^2 / r_k^3` for some `delta > 0` | `[INFERRED]` It improves the same frozen bad term in the same inherited LEI / epsilon-regularity ledger, after the later debt is restored | `[VERIFIED]` Anything weaker can leave the live coefficient unchanged and so is cosmetic |
| `[INFERRED]` Exact cancellation or quantified reduction of the affine-and-higher harmonic moment family behind `I_p^far` | `[INFERRED]` Named cancellation is admissible only as mechanism language for the same coefficient shrinkage | `[INFERRED]` Strong enough to imply the same net reduction of `C_far,eff(k)` for the full pairing | `[INFERRED]` These moments are the surviving source of the live coefficient, so reducing them matters only if the full pairing estimate improves | `[VERIFIED]` Moment language without coefficient shrinkage can be a representation identity or partial cancellation with no theorem-level gain |
| `[VERIFIED]` Quotient by constants / oscillation modulo constants | `[VERIFIED]` None; not a live currency | `[VERIFIED]` Rejected | `[VERIFIED]` Constants are already annihilated by the pairing before any tensor work begins | `[VERIFIED]` Affine and higher harmonic modes still survive as moments, so the bad coefficient can stay fixed |
| `[VERIFIED]` Generic harmonic smoothing, algebraic rewrite, or local geometry improvement with no coefficient shrinkage on the full pairing | `[VERIFIED]` None; branch-standard screen rejects it | `[VERIFIED]` Rejected | `[VERIFIED]` Tao-preserved harmonic analysis or representation cleanup is not theorem leverage on the frozen obstruction | `[VERIFIED]` The actual far-field coefficient and full pairing remain unchanged |

### 4. Recommended freeze

- [VERIFIED] Recommended cash-out:
  a one-sided full-pairing inequality on `I_p^far` in the inherited LEI / CKN-Lin contradiction ledger.
- [VERIFIED] Recommended currency:
  quantified reduction of the specified nonlocal remainder, namely the effective coefficient on `I_p^far`.
- [PROPOSED] Recommended minimum threshold:
  a uniform positive-margin net shrinkage of that coefficient on the same full pairing after later reconstruction and localization debt, not merely better modulo constants or nicer harmonic regularity.

### 5. Outcome

- [VERIFIED] The working hypotheses are mostly confirmed.
- [VERIFIED] The only clearly live cash-out line is the full-pairing inequality with a smaller effective coefficient.
- [VERIFIED] Harmonic-moment cancellation is admissible only as the mechanism for that reduction.
- [INFERRED] The minimum threshold should be frozen as positive-margin coefficient shrinkage that survives later debt.
- [VERIFIED] Weaker thresholds are ruled out by the constant-mode cancellation fact, the survival of affine-and-higher moments, the Tao gate against generic harmonic regularity, and the same-protocol rule against representation-only or surrogate gains.

## Dead Ends / Rejected Lines

- [VERIFIED] I searched for a stronger on-disk quantitative threshold than "materially smaller" / "positive margin" and did not find one tied specifically to this branch.
- [INFERRED] The repository supports the threshold shape, but not a sharper numeric lower bound for `delta` at Step 1.
- [VERIFIED] I found no locally frozen monotonicity formula tied to the inherited far-field pressure ledger, so monotonicity is not supportable as the primary progress currency here.
