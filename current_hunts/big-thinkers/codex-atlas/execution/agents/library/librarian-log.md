# Librarian Log

## 2026-03-29: Query for Navier-Stokes Strategy-001 Exploration-001 (literature survey of load-bearing inequalities in 3D NS regularity proofs)

**Requester:** Library Receptionist on behalf of Strategizer (navier-stokes, strategy-001, pre-exploration-001)

**Query:** First exploration launch for Navier-Stokes regularity theory mission. Literature survey to catalog all load-bearing inequalities in 3D NS regularity proofs (CKN, Prodi-Serrin-Ladyzhenskaya, ESS, Ladyzhenskaya inequality, Sobolev embeddings, Gronwall estimates). Need: (1) factual library content on Navier-Stokes, (2) meta-library lessons on literature survey design, first exploration scoping, providing context to explorers.

### Search path:
- Searched factual/INDEX.md for "navier", "stokes", "fluid", "regularity", "PDE" — no dedicated Navier-Stokes entries. Only tangential mentions (Padmanabhan Einstein-Navier-Stokes connection in emergent gravity; Hairer regularity structures in yang-mills stochastic quantization).
- Read meta/INDEX.md — goal-design (33 entries), methodology (38 entries)
- Checked navier-stokes/meta-inbox/ — empty (no prior meta-notes)
- Read 12 meta entries in full

### Factual entries returned: NONE
No factual library content on Navier-Stokes regularity theory. This is a new domain for Atlas.

### Meta entries returned (12):
- **methodology/divergent-survey-pattern.md** — Five-part survey pattern (survey + deep dive + synthesis + novelty assessment + next-computation recommendation). Apply to Phase 1 landscape mapping.
- **methodology/standard-explorer-for-literature-surveys.md** — Use standard explorer (~20 min) not math explorer (50+ min) for literature surveys. Handles multi-part analysis tasks.
- **goal-design/specify-rigor-level.md** — Request "theorem-level precision" for technical maps. "What EXACTLY do they prove?" pattern. Paper-by-paper verdict format for literature searches.
- **goal-design/name-specific-authors-and-papers.md** — Name target authors/papers + "and any others you find" for directed but thorough searches.
- **goal-design/one-task-per-exploration.md** — One cognitive task per exploration. Survey + deep dive + synthesis counts as one. Trust a well-scoped comprehensive survey.
- **goal-design/preload-context-from-prior-work.md** — Paste relevant findings into goals. First exploration has no prior context to load, but note for future explorations.
- **goal-design/specify-failure-paths.md** — Include "if this fails, explain why." Pre-specify known domain constraints.
- **goal-design/allow-explorer-synthesis.md** — Don't over-specify conclusions. Leave synthesis open for emergent insights.
- **goal-design/use-classification-schemes.md** — Provide explicit classification schemes. Extension map tables (Feature | Status | Key Reference | What Breaks). Require claim attribution.
- **goal-design/instruct-incremental-writing.md** — "Write section by section" instruction. For literature surveys, add deadline nudge and [INCOMPLETE] permission.
- **goal-design/scope-computations-to-minimum-diagnostic.md** — Not directly applicable (this is a survey, not computation), but relevant for later explorations.
- **methodology/split-search-from-synthesis.md** — If the survey requires 3+ distinct literature searches, consider splitting search and synthesis into two explorations. Proposed but not yet confirmed.
- **methodology/gap-finding-in-existing-programs.md** — "What's already been computed" comparison tables make gaps visible. Relevant for identifying where constants are explicit vs. existential.
- **goal-design/require-claim-attribution.md** — Ask explorer to distinguish paper-sourced claims from own reasoning.

---

## 2026-03-29: Query for Yang-Mills-Validation Strategy-002 Math Explorer (H_actual vs H_formula Hessian stress-test)

**Requester:** Library Receptionist on behalf of Strategizer (yang-mills-validation, strategy-002, pre-exploration)

**Query:** Pre-launch briefing for numerical stress-test of inequality lambda_max(H_actual(Q)) <= lambda_max(H_formula(Q)). H_actual = true Hessian by finite differences, H_formula = B-squared formula Hessian. Need: (1) B-squared formula relationship to actual Hessian (exact/upper-bound/neither), (2) correct LEFT B_box formula convention, (3) lessons on finite-difference Hessians for lattice gauge, (4) meta-lessons for designing Math Explorer stress-test goals.

### Search path:
- Read factual/yang-mills/INDEX.md — 22 entries, identified 8 directly relevant
- Read meta/INDEX.md -> goal-design (33 entries), methodology (37 entries) — identified 8 relevant
- Read yang-mills-validation/meta-inbox/ (6 files) — identified 4 directly relevant (E001, E003, E004, E005)
- Read all identified entries in full

### Factual entries returned (8):
- **b-square-inequality-proof-progress.md** — CRITICAL (M(Q) != Hessian: H(Q)=M(Q)-C(Q), C not PSD; B_box formula correction for backward edges; UNRESOLVED potential counterexample with wrong formula)
- **per-plaquette-inequality-false.md** — CRITICAL (per-plaquette H_P <= (beta/2N)|B_P|^2 is FALSE for Q!=I; global sum ratio up to 1.936; Q=I equality is flat-vacuum coincidence)
- **weitzenbock-exact-formula.md** — RELEVANT (M(Q) definition, R(Q)=M(Q)-M(I) structure)
- **szz-lemma-4-1-hessian-slack.md** — RELEVANT (finite-difference Hessian verification methodology; adversarial search gave >=176x slack)
- **hnorm-conjecture-numerical-resolution.md** — CRITICAL (FD verification max error 9.26e-8 at h=1e-4; convention audit SZZ S=-(beta/N)Sigma ReTr)
- **eigenvalue-verification-d5-departure.md** — RELEVANT (FD verification max error 2.38e-6; convention table S1 raw vs S2 SZZ)
- **fourier-hessian-proof-q-identity.md** — RELEVANT (Lemma 5.1: -1/N Re Tr(B^2 U) <= 1/(2N)|B|^2, equality iff U=I; triangle bound H_norm <= 1/8)
- **per-plaquette-inequality-false.md** — CONTEXT (dead proof chain)

### Meta entries returned (8):
- **meta-inbox/meta-exploration-001.md** — CRITICAL (LEFT perturbation convention = SZZ; FD-verify OFF-DIAGONAL elements; derive independently can reproduce known errors)
- **meta-inbox/meta-exploration-003.md** — CRITICAL (test at NON-IDENTITY config first; both LEFT and RIGHT formula variants; off-diagonal FD checks essential)
- **meta-inbox/meta-exploration-004.md** — RELEVANT (ARPACK artifact detection; large lattice background computation stalls)
- **meta-inbox/meta-exploration-005.md** — RELEVANT (derive analytical prediction BEFORE running numerics)
- **include-trivial-control-checks.md** — CRITICAL (Q=I sanity check variant for Hessian computations)
- **require-quantification-in-stress-tests.md** — CRITICAL (quantify each finding, not just argue)
- **budget-adversarial-for-high-dim.md** — CRITICAL (>=20 adversarial starts for high-dim parameter spaces)
- **gradient-ascent-on-projected-quantity.md** — RELEVANT (test projected quantity for subspace bounds)

---

## 2026-03-29: Query for Yang-Mills-Conjecture Strategy-003 Math Explorer (counterexample verification + SZZ clarification)

**Requester:** Library Receptionist on behalf of Strategizer (yang-mills-conjecture, strategy-003, pre-exploration)

**Query:** Pre-launch briefing for Math Explorer to verify E007 counterexample (lambda_max ~ 16.08 from gradient ascent) and clarify SZZ framework (M(Q) vs full Hessian H(Q), Bakry-Emery condition target). Need: (1) E007 counterexample details, B-field formula, adjoint vs fundamental issue; (2) SZZ framework / Lemma 4.1 / Hessian distinction; (3) meta-learning for math explorer verification goals; (4) non-staggered eigenvalue data.

### Search path:
- Read factual/yang-mills/INDEX.md (22 entries) — identified 12 directly relevant
- Read meta/INDEX.md -> goal-design (33 entries), methodology (36 entries) — identified 10+ relevant
- Read yang-mills-conjecture/meta-inbox/ (9 files) — identified 2 directly relevant (E007, E005)
- Read all identified entries in full

### Factual entries returned (12):
- **b-square-inequality-proof-progress.md** — CRITICAL (B_field formula correction for backward edges, SZZ normalization convention note SU(2) N=2 vs SO(3) N=3, partial proofs status, remaining gap structure)
- **cube-face-reduction-adversarial-review.md** — CRITICAL (Gap 1 CLOSED by S002-E005, momentum decomposition eigenvalue = 4*(# pi-components), non-stag eigenvalue max 14.6 vs stag max 9.5 for random Q, L=3 eigenvalue formula 4d*sin^2(pi/L))
- **szz-lemma-4-1-hessian-slack.md** — CRITICAL (Hessian bound 12-170x loose, adversarial search gives >=176x slack, 4D tighter than 3D)
- **shen-zhu-zhu-stochastic-analysis.md** — CRITICAL (K_S = N/2 - 8N(d-1)|beta|, Bakry-Emery uses full Hessian HessS not M(Q), Lemma 4.1 bounds |HessS(v,v)| <= 8(d-1)N|beta||v|^2)
- **eigenvalue-verification-d5-departure.md** — CRITICAL (lambda_max = 4beta at Q=I confirmed, convention table S1 raw vs S2 SZZ, d=5 departure)
- **fourier-hessian-proof-q-identity.md** — CRITICAL (Fourier proof H_norm = 1/12 at Q=I, improved threshold table, H_norm <= 1/8 for ALL Q via triangle)
- **full-eigenspace-gap1-investigation.md** — CRITICAL (per-vertex 12x12 reduction, constraint ESSENTIAL, 110K+ tests 0 violations, best adversarial 15.997)
- **hnorm-conjecture-numerical-resolution.md** — CRITICAL (100-config scan zero violations, Q=I is unique global max, convention audit)
- **weitzenbock-exact-formula.md** — RELEVANT (R(Q)|_P exact formula, -1/12 coefficient, gradient ascent stays at -8 to -11)
- **lemma-d-rdr-false-sum-s-nonneg.md** — RELEVANT (sum_S >= 0 PROVED, closes Gap 1 in cube-face reduction)
- **per-plaquette-inequality-false.md** — RELEVANT (per-plaquette bound false for Q!=I, proof must use direct spectral argument)
- **per-plaquette-inequality-false.md** — CONTEXT (B_P proof chain dead, both steps fail)

### Meta entries returned (10):
- **meta-inbox/s002-meta-exploration-007.md** — CRITICAL (E007 counterexample: B-field formula may use fundamental not adjoint; 16.08 not cross-checked; M(Q) vs Hessian distinction should be clarified)
- **meta-inbox/meta-exploration-006.md** — RELEVANT (proof attempt workflow: Stage 1 numerical -> Stage 2 algebraic -> Stage 3 proof)
- **verify-goal-claims-before-delegating.md** — CRITICAL (verify cited claims before GOAL.md; anti-pattern: confusing scalar bound with operator ordering)
- **require-matrix-sanity-checks.md** — CRITICAL (Q=I sanity check, finite-difference verification, numerical check before proof attempts)
- **include-trivial-control-checks.md** — CRITICAL (Q=I baseline check for Hessian/eigenvalue computations, numerical sanity before proof)
- **staged-computation-goals.md** — CRITICAL (4-stage sequential pipeline for math explorer goals)
- **budget-adversarial-for-high-dim.md** — CRITICAL (adversarial optimization essential for >=20D parameter spaces)
- **verify-unexpected-findings-immediately.md** — CRITICAL (immediate stress-test for unexpected findings)
- **gradient-ascent-on-projected-quantity.md** — RELEVANT (test correct target: lambda_max(P^T R P) not full matrix)
- **characterize-maximizers-not-just-bounds.md** — RELEVANT (ask "characterize the maximizers" to reveal geometry)

---

## 2026-03-28: Query for Yang-Mills Validation Strategy-001 (3 parallel explorations)

**Requester:** Library Receptionist on behalf of Strategizer (yang-mills-validation, strategy-001, pre-launch)

**Query:** Pre-launch briefing for 3 parallel explorations: (1) Independent rederivation of beta < 1/6 proof from SZZ Bakry-Emery Hessian, (2) CNS papers overlap/novelty analysis, (3) B-square formula and conventions verification. Need all library entries about SZZ Hessian bound, B-square formula, convention issues, CNS papers, eigenvalue verification, staggered modes, and meta-lessons for proof verification goals.

### Search path:
- Read factual/INDEX.md -> yang-mills section
- Read factual/yang-mills/INDEX.md — 19 entries, identified 10 relevant
- Read meta/INDEX.md -> goal-design (31 entries), methodology (31 entries)
- Read meta/goal-design/INDEX.md, meta/methodology/INDEX.md — identified 12+ relevant entries

## 2026-03-31: Query for Far-Field Pressure Harmonic Loophole Pre-Exploration Briefing (strategy-001, mission far-field-pressure-harmonic-loophole)

**Requester:** Library Receptionist on behalf of Strategizer (navier-stokes / vasseur-pressure context, pre-exploration-003)

**Query:** Minimal falsification-model material for a harmonic pressure piece generated by exterior/far-field data; need Wolf-style local pressure decomposition notes, harmonicity-vs-scaling guidance, and counterexample-style methodology.

### Search path:
- Read factual/INDEX.md and factual/navier-stokes/INDEX.md
- Read factual/navier-stokes/vasseur-de-giorgi/INDEX.md
- Read meta/INDEX.md, meta/methodology/INDEX.md, meta/missionary/INDEX.md
- Read `execution/instances/far-field-pressure-harmonic-loophole/meta-inbox/meta-exploration-001.md`
- Searched for `Wolf`, `harmonic`, `p_far`, `local pressure decomposition`, `oscillation`, `Harnack`, `constant-scale`, `energy-scale`

### Key files returned:
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md` — exact near/far split obstruction; `P_{k1}` already favorable; surviving loophole is a decomposition mismatch, and harmonic control must change the bad pairing itself from fixed energy-scale to `U_k`-dependent
- `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — clarifies `P_{k1}` vs `P_{k21}`; harmonic term is not the bottleneck; surviving lead is an alternative harmonic far-field piece that might absorb the bad local interaction
- `factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md` — H^1 routes fail at the `W^{1,3}` wall; far-field harmonic reformulation remains only as a non-literal Vasseur split; harmonicity alone is not enough
- `factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md` — Wolf local pressure decomposition is explicitly listed as untested; harmonic+particular split is CZ-free but not yet applied to De Giorgi
- `factual/navier-stokes/beltrami-pressure-analytical.md` — exact harmonic/pressure-simplification reference point: on `T^3`, pressure reduces to Bernoulli form and CZ loss vanishes, but this is exact-symmetry-only
- `meta/methodology/check-bypass-not-just-improve-bottleneck.md` — strategy rule: ask whether the bottleneck tool can be bypassed entirely before trying to improve it
- `meta/methodology/distinguish-constant-from-scaling-slack.md` — constant harmonic/oscillation gains do not change beta; only `U_{k-1}`-scaling slack can
- `meta/methodology/test-generalization-before-concluding.md` — exact-case mechanisms must be perturbed before treating them as strategy conclusions
- `meta/methodology/verify-counterexample-before-investigating.md` — verify the exact mathematical object first; do not chase consequences of a possibly mis-specified counterexample

### Bottom line:
- The local library does **not** contain a worked Wolf-style De Giorgi counterexample.
- It does contain a precise formulation of the remaining live test: can a harmonic far-field split make the dangerous pressure pairing genuinely `U_k`-dependent, rather than merely smoothing constants/oscillation?
- The library’s repeated answer is: harmonicity alone changes only constants/oscillation unless the decomposition itself changes which term carries the level-set scaling.
- Checked yang-mills-validation/meta-inbox/ — empty (new mission)

### Factual entries returned (10):
- **szz-lemma-4-1-hessian-slack.md** — CRITICAL (Hessian bound 12-170x loose, plaquette cancellation mechanism)
- **b-square-inequality-proof-progress.md** — CRITICAL (B_square formula correction, partial proofs, failed approaches, remaining gap)
- **shen-zhu-zhu-stochastic-analysis.md** — CRITICAL (K_S = N/2 - 8N(d-1)beta formula, 8(d-1) factor derivation)
- **cao-nissim-sheffield-area-law-extension.md** — CRITICAL (CNS Sept 2025 + May 2025 papers, threshold doubled to 1/24)
- **weitzenbock-exact-formula.md** — CRITICAL (R(Q)|_P exact formula, -1/12 coefficient)
- **eigenvalue-verification-d5-departure.md** — CRITICAL (lambda_max = 4beta at Q=I confirmed; d=5 staggered departure; convention table)
- **fourier-hessian-proof-q-identity.md** — CRITICAL (Fourier proof H_norm = 1/12 at Q=I; improved threshold table)
- **master-loop-optimized-ceiling.md** — RELEVANT (beta_0(4) = 1/87 ceiling; curvature structurally absent)
- **per-plaquette-inequality-false.md** — RELEVANT (per-plaquette bound definitively false for Q!=I)
- **hnorm-conjecture-numerical-resolution.md** — CRITICAL (100-config scan, zero violations, convention audit)

### Meta entries returned (12):
- **verify-goal-claims-before-delegating.md** — CRITICAL (verify cited claims match actual findings)
- **characterize-maximizers-not-just-bounds.md** — RELEVANT (frame goals as "characterize maximizers")
- **verify-unexpected-findings-immediately.md** — RELEVANT (stress-test unexpected findings)
- **include-trivial-control-checks.md** — CRITICAL (Q=I sanity check variant; numerical check before proof)
- **specify-rigor-level.md** — RELEVANT (request theorem-level precision)
- **preload-context-from-prior-work.md** — CRITICAL (paste findings directly; verify formulas before preloading)
- **specify-computation-parameters.md** — RELEVANT (exact parameters for simulations)
- **one-task-per-exploration.md** — RELEVANT (separate convention questions from computation)
- **specify-failure-paths.md** — RELEVANT (failure paths for proof verification)
- **staged-computation-goals.md** — RELEVANT (sequential verification pipeline)
- **gradient-ascent-on-projected-quantity.md** — RELEVANT (test projected quantity P^T R P)
- **sequence-computation-approaches.md** — RELEVANT (verify Method 1 before comparing Method 2)

---

## 2026-03-28: Query for RH Strategy-003 Exploration 007 (adversarial + novelty review)

**Requester:** Library Receptionist on behalf of Strategizer (riemann-hypothesis, strategy-003, E007 design)

**Query:** Pre-launch briefing for E007 — a standard (literature/synthesis) Explorer doing adversarial and novelty review of five key claims: (1) Δ₃ flat saturation plateau L=15–30, (2) λ_n^zeta/λ_n^GUE < 1 for n>300 (Li coefficients), (3) Berry formula accuracy growing discrepancy at high T (0.6% to 12%), (4) K_primes normalization (log p)²/p^m, (5) C1 matrix intermediate Δ₃=0.285. What's documented in the library? What meta-lessons apply?

### Search path:
- Read factual/INDEX.md → RH section; meta/INDEX.md → goal-design, methodology
- Read riemann-hypothesis/INDEX.md — full entry list
- Read berry-saturation-confirmed.md — CRITICAL (Δ₃_sat=0.1550, onset L≈10–12, flat L=15–100)
- Read berry-formula-quantitative-test.md — CRITICAL (height-resolved bins, 0.2%→12.5% growing error table)
- Read li-gue-comparison-super-rigidity.md — CRITICAL (crossover n≈300, ratio 0.95 at n=500)
- Read novelty-verdicts-synthesis.md — CRITICAL (Berry saturation NOT NOVEL, C1 rigidity RETRACTED, N²/p and Dirichlet SUPPORTED)
- Read prime-sum-form-factor-ramp.md — CRITICAL (correct normalization K_primes = K_density/(2πρ̄)², E006 resolution)
- Read c1-constraint-scorecard.md — CRITICAL (E009 retraction of anomalous rigidity)
- Read goal-design/adversarial-synthesis-goal-structure.md — critical meta
- Read goal-design/prioritize-novelty-assessment.md — critical meta
- Read goal-design/name-specific-authors-and-papers.md — relevant meta
- Read goal-design/specify-rigor-level.md — relevant meta
- Read methodology/adversarial-explorations-need-null-hypothesis.md — critical meta
- Read methodology/split-search-from-synthesis.md — critical meta
- Read meta-inbox/s002-meta-006, s002-meta-007, s002-meta-008 — operational patterns for adversarial/lit explorations
- Read meta-inbox/s003-meta-001, s003-meta-002, s003-meta-003, s003-meta-006 — S003 operational lessons

### Returned:
- Full factual content for all five claims with exact numbers
- Berry saturation: NOT NOVEL (Berry 1985 predicted; Odlyzko confirmed); our 7.6% accuracy and height-resolved table add precision but not novelty
- Li λ_n ratio: NOT IN LIBRARY (li-gue-comparison-super-rigidity.md documents it but no literature search conducted yet — prime target for E007)
- Berry formula discrepancy at high T: 0.2%→12.5% table documented; mechanism identified (short prime orbit corrections) but not checked against literature
- K_primes normalization: WEAK — Berry (1985) is prior source; normalization subtlety not explicitly stated
- C1 Δ₃=0.285: RETRACTED as NOT NOVEL — E009 proved it is generic finite-size GUE
- Meta: use adversarial-synthesis-goal-structure (4-part); use split-search-from-synthesis; name Berry, Bogomolny-Keating, Odlyzko, Li, Coffey as specific targets; use [SECTION COMPLETE] markers; include null hypothesis test

### Skipped:
- All non-RH factual subtrees — not relevant
- trace-formula-*, prime-corrections-*, individual-zero-*, arithmetic-matrix-*, gauss-*, pair-correlation-discriminating-power — not directly relevant to E007 five claims
- Most methodology entries — covered by the above targeted reads

## 2026-03-27: Query for RH Strategy-003 (Exploration A: Off-Diagonal Form Factor; Exploration B: Li's Criterion)

**Requester:** Strategizer (stochastic-electrodynamics, strategy-003)
**Query:** Three parallel explorations: (1) E-Santos — Santos (2022) O(ħ) framework and whether O(ħ²) corrections explain the 15-18% anharmonic residual at β=1 and tunneling slope=1.049; (2) E-Hydrogen — re-run SED hydrogen with physical τ=2.6×10⁻⁷ a.u.; (3) E-3D — compute 3D two-point ZPF correlator using Boyer's formula and check if orientational average gives C_xx→0 or C_xx→r⁻⁶.

### Search path:
- Read factual/INDEX.md → SED section highly relevant, followed stochastic-electrodynamics/INDEX.md
- Read meta/INDEX.md → followed goal-design/, methodology/
- Meta-inbox: read all 12 files (meta-exploration-001 through 011, meta-s001-exploration-007); meta-003 (s002-E003), meta-007 (s002-E002), meta-010 (s002-E005) most relevant
- Read sed-omega3-feedback-mechanism.md — highly relevant (E-Santos: Santos 2022 framework, fix assessment)
- Read sed-double-well-tunneling.md — highly relevant (E-Santos: slope=1.049, Faria-França prior art)
- Read anharmonic-ald-landau-lifshitz.md — highly relevant (E-Santos: 15-18% residual data, β^0.40)
- Read sed-coupled-oscillator-zpf-correlations.md — highly relevant (E-3D: 1D formula, 3D open question)
- Read hydrogen-self-ionization.md — highly relevant (E-Hydrogen: τ correction, T_ion data)
- Read sed-s002-adversarial-review.md — relevant to all three (novelty verdicts, must-fix list)
- Read anharmonic-oscillator-failure.md — relevant (E-Santos: QM reference values)
- Read established-successes.md — relevant (E-3D: Boyer references)
- Read COMPUTATIONS-FOR-LATER.md — relevant (registered computations #6 and #7)
- Read goal-design/INDEX.md, preload-context-from-prior-work.md, specify-computation-parameters.md — relevant meta
- Read methodology/INDEX.md — relevant meta

### Returned:
- Santos (2022) O(ħ) framework from sed-omega3-feedback-mechanism.md — SED=O(ħ¹) QED, quadratic Hamiltonian exact, nonlinear failures = missing O(ħ²)

---

## 2026-03-31: Query for Strategizer briefing on exact-ns-no-near-closed-tao-circuit (strategy-001, pre-exploration-003)

**Requester:** Library Receptionist on behalf of Strategizer (Navier-Stokes / Tao firewall context)

**Query:** Determine whether the packetized backup definition remains precise enough to pursue, or whether it is too non-canonical / underconstrained to remain a good mission object. Requested: exact finite packet / projection / basis-dependence notes, methodology for backup-definition failure, toy-subsystem isolation guidance, and follow-up exploration framing.

### Search path:
- Read `execution/agents/library/factual/INDEX.md`
- Read `execution/agents/library/meta/INDEX.md`
- Read `execution/instances/exact-ns-no-near-closed-tao-circuit/meta-inbox/meta-exploration-001.md`
- Read `execution/agents/library/factual/navier-stokes/INDEX.md`
- Read `execution/agents/library/factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md`
- Read `execution/agents/library/factual/navier-stokes/exact-ns-triadic-coefficient-rigidity.md`
- Read `execution/agents/library/factual/navier-stokes/exact-ns-unavoidable-spectator-couplings.md`
- Read `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md`
- Read `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`
- Read `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/strategy-001-adversarial-synthesis.md`
- Read `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md`
- Read `execution/agents/library/factual/navier-stokes/near-beltrami-negative-result.md`
- Read `execution/agents/library/meta/methodology/toy-subsystem-isolation-inside-exact-network.md`
- Read `execution/agents/library/meta/methodology/reconcile-notation-before-falsification.md`
- Read `execution/agents/library/meta/methodology/definition-extraction-gates-computation.md`
- Read `execution/agents/library/meta/methodology/decomposition-audit-before-attacking-barrier.md`
- Read `execution/agents/library/meta/methodology/verification-catches-library-errors.md`
- Read `execution/agents/library/meta/goal-design/require-mechanism-layer-maps.md`
- Read `execution/agents/library/meta/goal-design/preload-context-from-prior-work.md`
- Read `execution/agents/library/meta/goal-design/specify-failure-paths.md`

### Bottom line:
- The library has **no separate packet-model branch** for this mission beyond the Tao/firewall notes and the exact-network isolation methodology.
- The exact-NS material says the live object must be treated as a **channel graph** under rigid coefficients and forced spectators, not as a loosely defined packet family.
- The meta guidance says to decide this via a **failure-path / null-hypothesis** test: if the packetized backup cannot be tied to a literal exact-channel table and a full-network isolation check, it should be treated as a definition-level failure rather than a candidate.

### Most relevant factual files:
- `factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md` — Tao’s reduced mechanism is a deliberately engineered five-mode delayed-abrupt-transfer circuit; packet models are only useful if they can realize that literal gate chain.
- `factual/navier-stokes/exact-ns-triadic-coefficient-rigidity.md` — exact Fourier/helical coefficients are rigid; the main risk is loss of the engineered hierarchy.
- `factual/navier-stokes/exact-ns-unavoidable-spectator-couplings.md` — exact NS activates spectator couplings automatically; isolation is the decisive stress test.
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md` — the surviving issue is decomposition mismatch, not a hidden harmonic loophole.
- `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — the pressure-side loophole must change the pairing itself, not just improve constants.
- `factual/navier-stokes/near-beltrami-negative-result.md` — exact-symmetry mechanisms do not generally survive perturbation; genericity is a real failure mode.

### Most relevant meta files:
- `meta/methodology/toy-subsystem-isolation-inside-exact-network.md` — test whether the reduced subsystem survives the restored exact interaction network.
- `meta/goal-design/require-mechanism-layer-maps.md` — require exact PDE / reduced circuit / theorem layers plus a literal channel table.
- `meta/methodology/reconcile-notation-before-falsification.md` — reconcile decompositions before falsifying a surviving lead.
- `meta/methodology/definition-extraction-gates-computation.md` — extract the exact target definition first; if the object is only architecture-level, that is enough for Phase 0.
- `meta/goal-design/specify-failure-paths.md` — if it fails, explain the structural reason and what would work instead.
- `meta/methodology/decomposition-audit-before-attacking-barrier.md` — audit the proof structure before spending effort on a barrier.
- β^0.40 residual data + ALD 3-way table from anharmonic-ald-landau-lifshitz.md — 15-18% at β=1 confirmed
- Slope=1.049 unexplained systematic from sed-double-well-tunneling.md — Faria-França predict 1.0 exactly
- τ correction (60× too large) + physical value from hydrogen-self-ionization.md — τ_phys = 2.6×10⁻⁷ a.u.
- 1D C_xx(d)=cos(ω₀d/c) verified, 3D open from sed-coupled-oscillator-zpf-correlations.md
- Must-cite Faria-França (2004) from sed-s002-adversarial-review.md
- Meta lessons: verify physical constants before writing goal; preload exact code; sequential runs; normalization matching

### Skipped:
- constraints/, asymptotic-safety/, string-theory/ etc. — not relevant to SED
- riemann-hypothesis/, yang-mills/, amplituhedron/ — not relevant
- sed-novelty-assessment.md — covered by sed-s002-adversarial-review.md
- sed-ho-zpf-spectral-density.md, sed-ho-uv-divergence-structure.md, sed-ho-numerical-verification.md — HO details not needed for these three explorations
- quantum-coherence-failure.md, entanglement-bell-contested.md — not relevant to E-Santos/E-Hydrogen/E-3D
- spin-anomalous-moment-status.md — not relevant
- linearity-boundary-pattern.md — context already covered in other files
- meta-inbox 001, 002, 004, 005, 006 (s001 strategy) — general SED lessons, not new info for these specific explorations

## 2026-03-27: Query for RH Strategy-003 (Exploration A: Off-Diagonal Form Factor; Exploration B: Li's Criterion)

**Requester:** Strategizer (riemann-hypothesis, strategy-003, pre-launch briefing for Phase 1 parallel explorations)

## 2026-03-31: Query for Anatomy-of-Averaged-NS-Blowup-Firewall Strategy-001 Exploration 001 (Phase 0 mechanism reconstruction of Tao 2016)

**Requester:** Library Receptionist on behalf of Strategizer (anatomy-of-averaged-ns-blowup-firewall, strategy-001, pre-exploration-001)

**Query:** Pre-exploration briefing for a mechanism-level reconstruction of Tao's 2016 averaged Navier-Stokes blowup. Need the most relevant local library material for: explicit averaged operator / averaging ingredients, modal packets or transfer architecture, exact role of averaging in isolating transfer, load-bearing identities/cancellations/symmetries, Atlas notes connecting Tao to limits of generic energy + harmonic-analysis methods, and GOAL.md writing guidance that stays equation-first and avoids vague cancellation language.

### Search path:
- Read `execution/agents/library/factual/INDEX.md`
- Read `execution/agents/library/factual/navier-stokes/INDEX.md`
- Read `execution/agents/library/meta/INDEX.md`
- Read `execution/agents/library/meta/goal-design/INDEX.md`
- Read `execution/agents/library/meta/methodology/INDEX.md`
- Read `execution/agents/library/librarian-log.md`
- Read mission / strategy files under `execution/instances/anatomy-of-averaged-ns-blowup-firewall/`
- Read Tao-related local notes in `execution/instances/navier-stokes/library-inbox/` and `execution/instances/far-field-pressure-harmonic-loophole/`

### Key findings returned:
- The local factual library is strong on the barrier side but sparse on Tao's actual finite-dimensional cascade internals.
- Best local explicit Tao formulas are in `execution/instances/navier-stokes/library-inbox/exploration-005-literature-vortex-stretching.md` and `execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md`.
- Best cross-cutting Atlas notes on the Tao barrier are `navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md`, `post-2007-beta-landscape.md`, and `MISSION-VALIDATION-GUIDE.md`.
- Best goal-writing/meta notes are `meta/methodology/reconcile-notation-before-falsification.md`, `meta/methodology/decomposition-audit-before-attacking-barrier.md`, `meta/goal-design/request-equations-for-construction.md`, `meta/goal-design/specify-rigor-level.md`, `meta/goal-design/specify-failure-paths.md`, `meta/goal-design/one-task-per-exploration.md`, `meta/goal-design/distinguish-identity-from-mechanism.md`, and `meta/goal-design/allow-explorer-synthesis.md`.

### Bottom line:
- Phase 0 should be written as a decomposition audit that forces the explorer to recover the averaged operator, the transfer architecture, and the blowup trigger separately.
- If the cascade cannot be stated equation-level from the paper plus local context, the exploration should terminate with a reconstruction-level negative result rather than a firewall claim.
**Query:** (1) Exploration A — Berry's spectral rigidity formula, off-diagonal periodic orbit corrections, Bogomolny-Keating framework, K(τ) → Δ₃ relationship, prior normalization failures, confirmed formulas. (2) Exploration B — Li's criterion (λ_n coefficients), asymptotic growth, mpmath approach, prior patterns. (3) Both — meta-lessons for Math Explorer goal design, stalling/failure modes, scope/context level.

### Search path:
- Read factual/INDEX.md → RH section highly relevant, followed riemann-hypothesis/INDEX.md
- Read meta/INDEX.md → followed goal-design/INDEX.md, methodology/INDEX.md, system-behavior/INDEX.md
- Read meta-inbox: all 8 files (meta-001, meta-002, meta-003, s002-meta-001, s002-meta-006, s002-meta-007, s002-meta-008, s002-meta-009)
- Read strategy-003/STRATEGY.md — read full plan to understand exact context of the two explorations
- Read factual/riemann-hypothesis/prime-sum-form-factor-ramp.md — CRITICAL for Exploration A (confirmed normalization, ramp vs. plateau)
- Read factual/riemann-hypothesis/berry-saturation-confirmed.md — CRITICAL (Δ₃_sat=0.155 target, Dyson-Mehta integral formula required)
- Read factual/riemann-hypothesis/berry-formula-quantitative-test.md — CRITICAL (formula (a) confirmed 7.6%, integral formula derivation, height-resolved table)
- Read factual/riemann-hypothesis/spectral-form-factor-gue.md — relevant (K(τ) ramp slope 1.010, plateau 1.043)
- Read factual/riemann-hypothesis/riemann-operator-constraints.md — relevant (operator constraints, off-diagonal nuance added from E006)
- Read factual/riemann-hypothesis/novelty-verdicts-synthesis.md — relevant (central open problem, S003 questions)
- Read goal-design/instruct-incremental-writing.md — CRITICAL meta (8 confirmations, [SECTION COMPLETE] variant, research-buffering stall)
- Read goal-design/INDEX.md — relevant (specify-computation-parameters, require-matrix-sanity-checks, allow-explorer-synthesis, preload-context)
- Read methodology/split-search-from-synthesis.md — relevant meta pattern
- Searched factual/riemann-hypothesis/ and full library for "Li's criterion", "lambda_n", "Bombieri", "Keiper" — NO MATCHES (library has no prior Li's criterion content)

### Returned:
- See full response below

### Skipped:
- All non-RH factual subtrees (QG, SED, classicality, amplituhedron, TTH, YM, etc.) — not relevant
- RH arithmetic matrix files (gauss-sum-phases, c1-constraint-scorecard, complex-phase-matrices, arithmetic-matrix-operators, pair-correlation-discriminating-power, trace-formula-*, individual-zero-*, prime-corrections-*) — not relevant to off-diagonal form factor or Li's criterion
- gue-pair-correlation.md, gue-nearest-neighbor-spacing.md — not relevant to these computations
- meta/goal-design/ entries not relevant to Math Explorer computation tasks (require-baryonic-completeness, specify-modified-inertia, scale-spread-in-numerical-surveys, etc.)
- meta/methodology/ entries not relevant to these specific tasks (comparison-exploration-pattern, decisive-negative-pivot, adversarial-check-between-phases, etc.)

## 2026-03-28: Query for RH Strategy-003 Exploration 009 (convergence rate of λ_n^zeta(K)/λ_n^GUE(N=K))

**Requester:** Library Receptionist on behalf of Strategizer (riemann-hypothesis, strategy-003, E009 design)

**Query:** Pre-launch briefing for E009 — convergence rate analysis of λ_n^zeta(K)/λ_n^GUE(N=K) as K=N→∞. Does the ratio converge to <1 (genuine structural difference) or →1 (truncation artifact)? Context needed on: Li coefficient asymptotics (Bombieri-Lagarias, Coffey), GUE Li coefficients, prior convergence behavior from E002/E008, meta-lessons on scoping Math Explorer computation goals efficiently.

### Search path:
- Read factual/riemann-hypothesis/INDEX.md — full RH factual summary
- Read li-gue-comparison-super-rigidity.md — CRITICAL (E007 confirmed novelty 4/5; crossover n≈300, ratio 0.95 at n=500; GUE ensemble was N=2000 with 5 trials; convergence requirements documented)
- Read li-coefficients-verified-n500.md — CRITICAL (truncation ratio r≈0.646 uniform; Coffey vs BL asymptotics; runtime data; saved files: zeros_cache.pkl, li_coefficients.npz, gue_results.npz)
- Read integral-chain-unreliable-n2000.md — relevant (computation reliability lessons)
- Read HISTORY-OF-REPORT-SUMMARIES.md — read E008 summary (confirmed r=0.949 at K=N=2000, 7.3σ; K=4500≠N=2000 gives ratio>1; GUE scales linearly with N; matched K=N=5000 was cut off)
- Read exploration-008/REPORT-SUMMARY.md — CRITICAL (full E008 findings; saved data files documented; K_values=[1000,2000,3000,4500] tested at N_TRIALS=30; code in exploration-008/code/)
- Read exploration-008/code/matched_comparison.py — code template to reuse
- Read meta-inbox/s003-meta-exploration-008.md — CRITICAL (E008 meta lessons: scope too wide; K=N test was the needed test; polling interval for long sessions; explorer discovered E002 GUE was N=2000 not N=100)
- Read meta-inbox/s003-meta-exploration-006.md — relevant (CWD check as Task 0; multiple K versions; GOAL.md normalization errors)
- Read meta-inbox/s003-meta-exploration-003.md — relevant (stall patterns; direct computation as fallback; 3.5hr stall; nudge pattern)
- Read meta-inbox/s003-meta-exploration-002.md — relevant (efficiency instruction; pre-compute zeros first; incremental saving; computation timeout)
- Read meta-inbox/s003-meta-exploration-001.md — relevant (formula bugs; computation timeout too short for prime sums)
- Read meta/methodology/staged-computation-goals.md — relevant (pipeline staging)
- Read meta/methodology/sequence-computation-approaches.md — relevant (sequencing methods)
- Read meta/methodology/parallel-math-explorer-explorations.md — relevant (when to parallelize)
- Read meta/methodology/require-trend-tabulation-for-negative-results.md — CRITICAL (trend table format for convergence tests)
- Read meta/goal-design/instruct-incremental-writing.md — CRITICAL (write after each K, row-level writing)
- Read meta/goal-design/specify-computation-parameters.md (partial) — relevant (exact parameters, fast-to-slow sequencing)

### Returned:
- Full E008 data and code available for reuse (gue_li_N2000_100trials.npz, li_zeta_2k.npz, li_zeta_5k.npz, matched_comparison.py)
- Key finding from E008: ratio at K=N=2000 is 0.949 (7.3σ); K=4500 vs N=2000 gives ratio>1; K=N=5000 was cut off
- GUE λ_n scales linearly with N: need matched K=N at each level
- Convergence r≈0.646 from E002 — zeta Li sums converge slowly; expect +6.1% increase n=500 from K=2000→5000
- Bombieri-Lagarias asymptotic: λ_n ~ (n/2)log(n); Coffey correction 2.44× better but NOT the ratio λ_n^zeta/λ_n^GUE
- No literature on GUE Li coefficients (novelty 4/5 confirmed by E007)
- Meta: scope to minimum computation (K=N=500,1000,2000,3000,5000 only); require trend table as primary output; write row-by-row during sweep; use existing code as template; CWD check as Task 0; set 20-30 min timeouts for large K; poll at 5 min for sessions >45 min

### Skipped:
- All non-RH factual subtrees — not relevant
- RH arithmetic matrix files (Gauss, Dirichlet, C1, pair correlation discriminating power) — not relevant
- Berry saturation, trace formula, prime corrections, individual zero files — not relevant to Li convergence
- meta/system-behavior files — not needed given E008's clean execution
- meta/methodology/adversarial-check*, decisive-negative-pivot*, gap-finding* — not relevant to convergence computation

## 2026-03-27: Query for Thermal-Time Mission (strategy-001, exploration-001 design)

**Requester:** Strategizer (thermal-time, strategy-001)
**Query:** What does the library contain about modular theory, KMS states, thermal time hypothesis (TTH), Bisognano-Wichmann theorem, or related topics that should be given to an explorer for a TTH survey / modular Hamiltonian extraction exploration? Also, what meta-lessons exist about scoping surveys of this type?

### Search path:
- Read factual/INDEX.md → followed emergent-gravity, compton-unruh, cross-cutting
- Read emergent-gravity/INDEX.md → followed thermodynamic-derivations, entanglement-and-holography
- Read thermodynamic-derivations/INDEX.md — identified Jacobson 1995 (Rindler + Unruh temperature) as relevant
- Read thermodynamic-derivations/jacobson-thermodynamic.md — relevant (Rindler-horizon Unruh temperature background)
- Read entanglement-and-holography/INDEX.md — not relevant directly (RT formula, ER=EPR)
- Read compton-unruh/INDEX.md — relevant (Unruh thermal structure, Planckian spectrum, de Sitter crossover)
- Read cross-cutting/INDEX.md → followed information-theoretic-constructive-axioms, entanglement-gravity-bootstrap, page-wootters-mechanism, problem-of-time
- Read cross-cutting/entanglement-gravity-bootstrap.md — HIGHLY RELEVANT (explicit modular Hamiltonian K, modular flow unitarity, Bueno et al. MVEH)
- Read cross-cutting/information-theoretic-constructive-axioms.md — RELEVANT (modular flow unitarity as Axiom 5)
- Read cross-cutting/page-wootters-mechanism.md — RELEVANT (explicit Connes-Rovelli 1994 cross-reference)
- Read cross-cutting/problem-of-time.md — RELEVANT (frozen formalism context for TTH motivation)
- Meta-inbox: thermal-time/meta-inbox/ — empty, 0 files

Meta library:
- Read meta/INDEX.md → followed goal-design, methodology
- Read meta/goal-design/INDEX.md — identified 8 relevant entries
- Read meta/methodology/INDEX.md — identified standard-explorer-for-literature-surveys, divergent-survey-pattern as most relevant
- Read divergent-survey-pattern.md — relevant
- Read one-task-per-exploration.md — relevant
- Read preload-context-from-prior-work.md — relevant
- Read specify-rigor-level.md — relevant
- Read name-specific-authors-and-papers.md — relevant
- Read specify-failure-paths.md — relevant
- Read allow-explorer-synthesis.md — relevant
- Read standard-explorer-for-literature-surveys.md — relevant

### Returned:
- jacobson-thermodynamic.md — Rindler-horizon thermodynamics + Unruh temperature as TTH background
- compton-unruh INDEX — Unruh/Gibbons-Hawking thermal structure, Planckian spectrum
- entanglement-gravity-bootstrap.md — explicit modular Hamiltonian K definition; modular flow unitarity; Bueno et al. MVEH
- information-theoretic-constructive-axioms.md — modular flow unitarity Axiom 5; KMS connection stated
- page-wootters-mechanism.md — explicit Connes-Rovelli (1994) cross-reference; PW vs. KMS time comparison
- problem-of-time.md — frozen formalism motivation for why TTH was proposed
- 8 meta entries: divergent-survey-pattern, one-task-per-exploration, preload-context, specify-rigor-level, name-specific-authors, specify-failure-paths, allow-explorer-synthesis, standard-explorer-for-literature-surveys

### Skipped:
- emergent-gravity/entanglement-and-holography/ contents — RT formula not directly relevant to modular Hamiltonians for Rindler/HO/CFT interval
- All LQG, string, AS, causal sets, Riemann, Yang-Mills, classicality-budget, amplituhedron, SED factual subtrees — not relevant to TTH/KMS
- cross-cutting time-interpretation synthesis entries (CI vs CP, meta-interpretation, etc.) — philosophical synthesis downstream of PW, not technical TTH content
- meta/system-behavior/ — not relevant to survey scoping

---

## 2026-03-27: Query for Riemann Hypothesis Mission (strategy-002, operator construction planning)

**Requester:** Strategizer (riemann-hypothesis, strategy-002)
**Query:** Planning three parallel operator construction explorations: (1) complex Hermitian arithmetic matrices with phases/Dirichlet characters targeting β=2; (2) optimization-based operator construction to match GUE/Montgomery statistics; (3) two-point formula + kernel operator from Montgomery pair correlation R₂. Asked about phases/Dirichlet characters for GUE, GUE vs GOE structure, optimization approaches for spectrum matching, published work, and strategy-001 findings on pair correlation.

### Search path:
- Read factual/INDEX.md — identified riemann-hypothesis/ as primary target
- Read factual/riemann-hypothesis/INDEX.md — all 6 entries directly relevant
- Read factual/riemann-hypothesis/arithmetic-matrix-operators-poisson-failure.md — DIRECTLY RELEVANT (Exploration 1)
- Read factual/riemann-hypothesis/riemann-operator-constraints.md — DIRECTLY RELEVANT (all three explorations)
- Read factual/riemann-hypothesis/gue-pair-correlation.md — DIRECTLY RELEVANT (Exploration 3)
- Read factual/riemann-hypothesis/berry-saturation-confirmed.md — RELEVANT (constraint context)
- Read factual/riemann-hypothesis/individual-zero-reconstruction-impossible.md — RELEVANT (Exploration 3, negative result)
- Read factual/riemann-hypothesis/trace-formula-gibbs-phenomenon.md — RELEVANT (Exploration 3)
- Read factual/riemann-hypothesis/prime-corrections-statistical-partial-success.md — RELEVANT (Exploration 3)
- Read meta/INDEX.md — identified goal-design/ and methodology/ as relevant
- Read meta/goal-design/INDEX.md — identified specify-computation-parameters, preload-context, one-task-per-exploration as most relevant
- Read meta/methodology/INDEX.md — identified multi-ansatz-sweep-pattern as relevant
- Read meta/goal-design/specify-computation-parameters.md — RELEVANT (code templates, parameter specification)
- Read meta/goal-design/preload-context-from-prior-work.md — RELEVANT (preload formulas)
- Read meta/goal-design/one-task-per-exploration.md — RELEVANT (scope guidance)
- Read meta/methodology/multi-ansatz-sweep-pattern.md — RELEVANT (Exploration 1 has multiple phase variants)
- Meta-inbox: read 4 files, all relevant
  - meta-exploration-001.md — mpmath timing, 2000-zero budget
  - meta-exploration-002.md — GUE simulation as control, saving data
  - meta-exploration-003.md — basis specification, scorecard format, key insight on spectral correlations
  - meta-exploration-004.md — negative results valuable, single deep > multi-approach, GUE stats need more than trace formula
- Read strategy-001/FINAL-REPORT.md — DIRECTLY RELEVANT (Explorations 1 and 3)
- Read strategy-001/explorations/exploration-005/GOAL.md — DIRECTLY RELEVANT (Exploration 3 — Montgomery computation design)
- Read strategy-001/explorations/exploration-005/REPORT.md — incomplete (explorer crashed)
- Read strategy-001/explorations/exploration-005/code/part1_form_factor_primes.py — RELEVANT (working prime sum code)

### Returned:
- arithmetic-matrix-operators-poisson-failure.md — full content: β=0.44 Hankel baseline, complex phase as most promising direction
- riemann-operator-constraints.md — full content: GUE/GOE/complex requirements, trace formula limitation
- gue-pair-correlation.md — full content: Montgomery formula, computation methodology, quantitative results
- berry-saturation-confirmed.md — full content: quantitative saturation tables
- individual-zero-reconstruction-impossible.md — full content: Gibbs obstruction for Exploration 3
- prime-corrections-statistical-partial-success.md — full content: density vs. correlation distinction
- trace-formula-gibbs-phenomenon.md — relevant excerpt
- All 4 meta-inbox files — computational lessons for goal design
- strategy-001 FINAL-REPORT — strategy context + recommendations for strategy-002
- exploration-005 code (part1) — working pair correlation code

### Skipped:
- gue-nearest-neighbor-spacing.md — spacing statistics not needed for operator construction planning
- spectral-form-factor-gue.md — already captured in FINAL-REPORT summary
- All other factual domains (QG, SED, Yang-Mills, etc.) — not relevant to Riemann operator construction

## 2026-03-27: Query for SED Mission (strategy-002, exploration-007)

**Requester:** Strategizer (stochastic-electrodynamics, strategy-002)
**Query:** Context for exploration-007 investigating the cause of β^0.40 power-law scaling in ALD-SED anharmonic oscillator residual error. Specifically: does the ω³ spectral shape of the ZPF drive the β^0.40 scaling? Plans to compare ALD-SED with ω³ ZPF (standard), white noise (n=0), ω¹ and ω² colored noise.

**Files searched (15 files read):**

Factual library:
- INDEX.md (root)
- stochastic-electrodynamics/INDEX.md
- stochastic-electrodynamics/anharmonic-ald-landau-lifshitz.md ← DIRECTLY RELEVANT
- stochastic-electrodynamics/uv-cutoff-parameter-scan.md ← DIRECTLY RELEVANT
- stochastic-electrodynamics/anharmonic-langevin-o-beta-failure.md ← DIRECTLY RELEVANT
- stochastic-electrodynamics/sed-novelty-assessment.md ← DIRECTLY RELEVANT
- stochastic-electrodynamics/sed-ho-zpf-spectral-density.md ← RELEVANT (ZPF PSD formula)

Meta library:
- INDEX.md (root)
- methodology/comparison-exploration-pattern.md ← DIRECTLY RELEVANT
- methodology/multi-ansatz-sweep-pattern.md ← DIRECTLY RELEVANT
- methodology/scale-spread-in-numerical-surveys.md ← RELEVANT
- methodology/sequence-computation-approaches.md ← RELEVANT
- goal-design/specify-computation-parameters.md ← DIRECTLY RELEVANT

SED meta-inbox:
- meta-exploration-003.md ← RELEVANT (noise normalization + parameter scan lessons)
- meta-exploration-004.md ← RELEVANT (pre-loading formulas lesson)
- meta-exploration-005.md ← DIRECTLY RELEVANT (parameter scan lessons, dt stability)
- meta-exploration-006.md ← RELEVANT (adversarial review timing)

**Findings returned:** All 7 factual files and 6 meta files above (full content). Judgment: high signal-to-noise — all findings returned are load-bearing for exploration-007 goal design.



## 2026-03-27: Query for Compton-Unruh Resonance Hypothesis (strategy-001, compton-unruh)

**Requester:** Strategizer (compton-unruh, strategy-001)
**Query:** Context for first exploration into QFT-in-curved-spacetime framework with scalar field in de Sitter background, Unruh-DeWitt detector response function, dimensional analysis of resonance at a ~ cH_0 between Compton frequency and Unruh temperature, and key integral identification. Six sub-queries:
1. Unruh effect
2. QFT in curved spacetime
3. de Sitter spacetime
4. Modified inertia proposals
5. MOND
6. McCulloch's quantized inertia
Plus meta-lessons about scoping explorations effectively.

**Files searched (32 files read):**

Factual library:
- INDEX.md (root)
- emergent-gravity/INDEX.md
- emergent-gravity/verlinde-entropic-gravity/INDEX.md, entropic-gravity-2010.md, dark-universe-2016.md, dark-gravity-mechanism.md, wide-binary-test-2024.md
- emergent-gravity/thermodynamic-derivations/INDEX.md, jacobson-thermodynamic.md
- emergent-gravity/analogue-gravity/INDEX.md, condensed-matter-analogues.md
- emergent-gravity/criticisms-and-limitations/INDEX.md, limitations-overview.md
- cross-cutting/INDEX.md, cosmological-constant-problem.md
- constraints/INDEX.md

Meta library:
- meta/INDEX.md
- meta/goal-design/INDEX.md, one-task-per-exploration.md, specify-failure-paths.md, preload-context-from-prior-work.md, use-line-count-targets.md, request-equations-for-construction.md, specify-rigor-level.md, require-claim-attribution.md
- meta/methodology/INDEX.md, divergent-survey-pattern.md, benchmark-comparison-early.md, devils-advocate-after-construction.md, comparison-exploration-pattern.md
- meta/system-behavior/INDEX.md, computation-vs-reasoning-limits.md, synthesis-vs-research-mode.md

Meta-inbox:
- compton-unruh/meta-inbox/ (empty)

**Grep searches:**
- "Unruh|MOND|McCulloch|quantized inertia|modified inertia|Compton|de Sitter" across full library
- "Unruh|MOND|McCulloch|quantized inertia|modified inertia|Compton|scalar field" across factual library

**Findings delivered:** Partial coverage. Library has strong content on Verlinde entropic gravity (MOND recovery, a_0 = cH_0 scale), Jacobson thermodynamic derivation (Unruh temperature in derivation), analogue Hawking radiation, and cosmological constant. No dedicated content on: Unruh effect proper, QFT in curved spacetime formalism, Unruh-DeWitt detectors, McCulloch's quantized inertia, de Sitter QFT, or modified inertia proposals. See detailed response.

**Gaps identified:**
- No dedicated file on the Unruh effect (only mentioned in Jacobson derivation and LQG black hole entropy)
- No file on QFT in curved spacetime as a formalism (scalar fields, mode functions, Bogoliubov transformations)
- No file on Unruh-DeWitt detectors
- No file on de Sitter QFT (Bunch-Davies vacuum, Gibbons-Hawking temperature)
- No file on McCulloch's quantized inertia / MiHsC
- No file on modified inertia proposals generally
- No file on MOND as a standalone topic (only Verlinde's recovery of MOND)
- No file on Milgrom's original MOND or its relativistic extensions (TeVeS, etc.)

## 2026-03-27: Follow-up Query for Compton-Unruh Exploration-001 (strategy-001, compton-unruh)

**Requester:** Strategizer (compton-unruh/stochastic-electrodynamics, strategy-001)
**Query:** Pre-exploration library search for first exploration: QFT-in-curved-spacetime framework, dimensional analysis of resonance at a ~ cH_0, no-go theorems against Unruh-based inertia modification. Also meta-lessons for first-exploration design.

**Additional files read beyond prior search (18 files):**

Factual library:
- emergent-gravity/verlinde-entropic-gravity/observational-tests.md, dark-matter-quanta.md
- emergent-gravity/criticisms-and-limitations/carlip-challenges.md, kobakhidze-criticisms.md, observational-scorecard.md
- emergent-gravity/thermodynamic-derivations/jacobson-entanglement-2015.md
- emergent-gravity/analogue-gravity/next-gen-experiments.md, condensed-matter-analogues.md
- cross-cutting/experimental-constraints.md
- constraints/INDEX.md

Meta library:
- meta/goal-design/name-specific-authors-and-papers.md, specify-temporal-recency.md, require-claim-attribution.md, request-equations-for-construction.md
- meta/methodology/adversarial-explorations-need-null-hypothesis.md, comparison-exploration-pattern.md

Meta-inbox:
- compton-unruh/meta-inbox/ (confirmed empty)

**Grep searches:**
- "Unruh|Compton|McCulloch|modified inertia|MiHsC|quantized inertia" across factual library (11 files)
- "Unruh|dark matter alternative|MOND|Milgrom|inertia modification" across factual library (22 files)

**Findings delivered:** Comprehensive results covering all relevant Verlinde/entropic gravity entries, Jacobson thermodynamic + entanglement derivations, criticisms/limitations, observational scorecard, analogue gravity (Unruh 1981 sonic BH), wide binary anomaly, plus 11 meta-lessons for goal design and methodology. Library gaps from prior search confirmed — no dedicated entries on Unruh effect, QFT in curved spacetime, Unruh-DeWitt detectors, de Sitter QFT, McCulloch/QI, or MOND proper.

## 2026-03-24: Query for Strategy-002 Escape Route Explorations

**Requester:** Strategizer (strategy-002)
**Query:** Context on 5 escape routes from the no-go theorem {d_s=2, Lorentz invariance, diffeomorphism invariance, renormalizability} -> quadratic gravity + fakeon. Also meta-lessons from meta-inbox.

**Files searched (28 files read):**

Factual library:
- INDEX.md (root)
- constraints/INDEX.md, constraint-rankings-and-dependencies.md, theory-construction-implications.md
- constraints/structural/ghost-spectral-dimension-no-go.md, unitarity-and-ghost-freedom.md, diffeomorphism-invariance.md, causality-preservation.md, uv-completion.md
- constraints/recovery/lorentz-invariance-bounds.md
- asymptotic-safety/INDEX.md, core-idea.md, spectral-dimension.md, critical-assessment.md, limitations.md, graviton-propagator.md, reuter-fixed-point.md
- cross-cutting/spectral-dimension-running.md, spectral-dimension-propagator-constraint.md, bekenstein-hawking-entropy.md, cosmological-constant-problem.md, holographic-principle.md, entanglement-area-law.md, experimental-constraints.md
- quadratic-gravity-fakeon/INDEX.md, core-idea.md, research-program-status.md, microcausality-and-novel-signatures.md
- bmeg/INDEX.md, eta-h-self-consistency.md, sign-robustness-arguments.md, uv-convergence-on-ds2.md, prediction-sensitivity.md
- emergent-gravity/thermodynamic-derivations/jacobson-thermodynamic.md, jacobson-entanglement-2015.md
- causal-set-theory/lorentz-invariance.md
- loop-quantum-gravity/limitations.md

Meta-inbox:
- meta-exploration-001.md through meta-exploration-005.md

**Grep searches:**
- "Horava|Lifshitz|anisotropic scaling|foliation" across factual library
- "nonlocal|infinite.derivative|IDG|entire function|partially nonlocal" across factual library

**Findings delivered:** Comprehensive results organized by escape route, plus meta-lessons. See response to strategizer.

**Gaps identified:**
- No dedicated Horava-Lifshitz file in the library (only scattered mentions)
- No dedicated IDG/nonlocal gravity file (only mentions in no-go theorem and constraints)
- No file on Lee-Wick theories
- No file on emergent Lorentz invariance mechanisms
- No file on "partially nonlocal" theories (this concept may not exist in the literature)

## 2026-03-24: Query for Bianconi 2025 Entropic Action Scrutiny

**Requester:** Explorer (strategy-002, exploration-002)
**Query:** Context for scrutinizing Bianconi's 2025 "entropic action" quantum gravity proposal (gravity from quantum relative entropy S(rho_metric || rho_matter)). Five sub-queries:
1. Entropic/thermodynamic derivations of gravity (Jacobson, Verlinde, Padmanabhan, Sakharov)
2. Cosmological constant problem and theories predicting Lambda
3. Tier 1-2 validation criteria for QG theories
4. Information-theoretic approaches to gravity
5. Meta-lessons about evaluating theory proposals

**Files searched (38 files read):**

Factual library:
- INDEX.md (root)
- emergent-gravity/thermodynamic-derivations/jacobson-thermodynamic.md, jacobson-entanglement-2015.md, padmanabhan-program.md, sakharov-induced-gravity.md
- emergent-gravity/verlinde-entropic-gravity/entropic-gravity-2010.md, dark-universe-2016.md, dark-gravity-mechanism.md, dark-matter-quanta.md, observational-tests.md, wide-binary-test-2024.md
- emergent-gravity/entanglement-and-holography/holographic-entanglement-spacetime.md, ryu-takayanagi.md
- emergent-gravity/criticisms-and-limitations/limitations-overview.md, kobakhidze-criticisms.md, carlip-challenges.md, observational-scorecard.md
- cross-cutting/cosmological-constant-problem.md, bekenstein-hawking-entropy.md, holographic-principle.md, information-paradox.md, entanglement-area-law.md, spectral-dimension-propagator-constraint.md
- causal-set-theory/cosmological-constant.md
- constraints/constraint-rankings-and-dependencies.md, theory-construction-implications.md
- constraints/structural/INDEX.md, unitarity-and-ghost-freedom.md, diffeomorphism-invariance.md, uv-completion.md, ghost-spectral-dimension-no-go.md, weinberg-witten-theorem.md, causality-preservation.md
- constraints/recovery/INDEX.md, graviton-propagator-ir-matching.md, equivalence-principle.md
- constraints/precision-bounds/INDEX.md

Meta-inbox:
- meta-exploration-001.md through meta-exploration-006.md

**Findings delivered:** Comprehensive dossier organized by 5 sub-queries. See response to explorer.

**Gaps identified:**
- No dedicated file on quantum relative entropy in the gravity context
- No file on Bianconi's work specifically (this is what the exploration will produce)
- No file on information-geometric approaches to gravity (Fisher information metric, etc.)
- No dedicated "theory evaluation rubric" document (the constraint rankings serve this purpose partially)

## 2026-03-25: Query for "Gravitizing the Quantum" Exploration (strategy-001, quantum-gravity-2)

**Requester:** Strategy-001 (quantum-gravity-2 instance)
**Query:** Four sub-queries about "gravitizing the quantum" — deriving quantum mechanics from gravitational/spacetime structure rather than quantizing gravity:
1. Approaches where gravity is more fundamental than QM
2. 't Hooft's deterministic QM, Penrose's gravitational collapse, stochastic gravity, emergent quantum mechanics
3. Constraints from the library applicable to such an approach
4. Information-theoretic findings connecting gravity to QM foundations

**Files searched (30+ files read):**

Factual library:
- INDEX.md (root)
- emergent-gravity/INDEX.md, thermodynamic-derivations/INDEX.md, jacobson-thermodynamic.md, jacobson-entanglement-2015.md, padmanabhan-program.md, sakharov-induced-gravity.md
- emergent-gravity/entanglement-and-holography/INDEX.md, ryu-takayanagi.md, holographic-entanglement-spacetime.md
- emergent-gravity/verlinde-entropic-gravity/INDEX.md
- emergent-gravity/criticisms-and-limitations/INDEX.md, limitations-overview.md
- cross-cutting/INDEX.md, information-theoretic-constructive-axioms.md, entanglement-gravity-bootstrap.md, problem-of-time.md, holographic-principle.md, information-paradox.md, entanglement-area-law.md, spectral-dimension-running.md, spectral-dimension-propagator-constraint.md
- constraints/INDEX.md, constraint-rankings-and-dependencies.md, theory-construction-implications.md, escape-routes-from-no-go.md
- constraints/structural/INDEX.md, ghost-spectral-dimension-no-go.md
- string-theory/ads-cft.md (for 't Hooft limit reference)

Meta-inbox (quantum-gravity-2):
- Empty (no files)

Also checked:
- nature-of-time instance meta-inbox (meta-exploration-001.md — methodology notes only)

**Grep searches:**
- "'t Hooft|tHooft|deterministic|Penrose|gravitational collapse|stochastic gravity|gravitizing|emergent quantum" across factual library

**Findings delivered:** Comprehensive results organized by 4 sub-queries. Key finding: the library has extensive material on "gravity from entanglement/information" (the reverse direction — QM as more fundamental) but virtually NO material on 't Hooft deterministic QM, Penrose gravitational collapse of the wavefunction, stochastic gravity, or the emergent quantum mechanics program. These are major gaps.

**Gaps identified:**
- NO file on 't Hooft's deterministic quantum mechanics / cellular automaton interpretation
- NO file on Penrose's gravitational OR (objective reduction) / Diosi-Penrose model
- NO file on stochastic gravity / stochastic semiclassical gravity
- NO file on emergent quantum mechanics programs (e.g., Adler's trace dynamics, Nelson's stochastic mechanics, 't Hooft's cellular automaton)
- NO file on "gravitizing the quantum" as a research direction (the library is entirely oriented toward "quantizing gravity")
- The 't Hooft references in the library are limited to the 't Hooft limit in AdS/CFT and 't Hooft as co-originator of the holographic principle — nothing about his deterministic QM program
- Penrose references are limited to spin networks in LQG — nothing about gravitational collapse of the wavefunction
- No file on the measurement problem and its relationship to gravity

## 2026-03-25: Query for Computational Spacetime Exploration (strategy-001, quantum-gravity-2)

**Requester:** Strategy-001 (quantum-gravity-2 instance)
**Query:** Five sub-queries about "computational spacetime" — spacetime geometry IS quantum circuit complexity:
1. Complexity = volume, complexity = action, complexity-geometry correspondence
2. De Sitter space and complexity, connections to cosmological constant
3. Holographic entanglement and spacetime emergence (Van Raamsdonk, ER=EPR, Ryu-Takayanagi)
4. Constraints/findings applicable to building a theory from computational principles
5. Tensor networks and spacetime structure

**Files searched (35+ files read):**

Factual library:
- INDEX.md (root)
- emergent-gravity/INDEX.md, entanglement-and-holography/INDEX.md, ryu-takayanagi.md, holographic-entanglement-spacetime.md
- emergent-gravity/thermodynamic-derivations/INDEX.md, jacobson-entanglement-2015.md
- emergent-gravity/criticisms-and-limitations/ (INDEX only)
- cross-cutting/INDEX.md, holographic-principle.md, entanglement-area-law.md, bekenstein-hawking-entropy.md, cosmological-constant-problem.md, information-paradox.md, spectral-dimension-running.md, spectral-dimension-propagator-constraint.md, information-theoretic-constructive-axioms.md, entanglement-gravity-bootstrap.md, time-from-entanglement-synthesis.md
- string-theory/INDEX.md, ads-cft.md, limitations.md
- causal-set-theory/INDEX.md, cosmological-constant.md, de-sitter-cosmology.md
- constraints/INDEX.md, theory-construction-implications.md, escape-routes-from-no-go.md
- constraints/structural/INDEX.md, ghost-spectral-dimension-no-go.md

Meta-inbox (quantum-gravity-2):
- meta-exploration-001.md (methodology notes only)

**Grep searches:**
- "complexity.*volume|complexity.*action|computational complexity|tensor network|circuit complexity" across factual library — NO MATCHES
- "Susskind|Brown.*Susskind|MERA|tensor network|complexity geometry" across factual library — only Susskind matches in existing ER=EPR and holographic contexts
- "de Sitter.*complexity|dS.*complexity|cosmological.*complexity|computational.*spacetime" across factual library — one match in holographic-principle.md (Universal Holographic Principle incorporating complexity into Einstein equations)

**Findings delivered:** Comprehensive results organized by 5 sub-queries. Key finding: the library has ZERO dedicated content on complexity=volume, complexity=action, tensor networks (MERA, HaPPY code), or circuit complexity in the gravity context. These are MAJOR gaps. The library does have extensive material on adjacent topics: Ryu-Takayanagi, Van Raamsdonk, ER=EPR, Jacobson entanglement equilibrium, entanglement-gravity bootstrap, holographic principle extensions, and information-theoretic axioms. The one mention of "complexity" in the holographic context is a passing reference in the Universal Holographic Principle paper.

**Gaps identified:**
- NO file on complexity = volume (Susskind 2014) or complexity = action (Brown, Roberts, Swingle, Susskind et al. 2015)
- NO file on quantum circuit complexity in the gravity/holography context
- NO file on tensor networks and spacetime (MERA, Swingle 2012, HaPPY code, Pastawski et al. 2015)
- NO file on switchback effect, complexity growth rate, or Lloyd's bound
- NO file on de Sitter complexity or the connection between complexity growth and cosmological constant
- NO file on holographic complexity in general
- NO file on quantum error correction and holography (Almheiri, Dong, Harlow 2015)
- NO file on subregion complexity or purification complexity
- NO file on Nielsen's geometric approach to circuit complexity
- The library's coverage of Susskind's contributions is limited to ER=EPR and the holographic principle — nothing on his extensive complexity program
- These gaps are especially significant because complexity-geometry is one of the most active research areas in quantum gravity (2014-present)

## 2026-03-27: Query for Riemann Hypothesis Strategy-002, E008 Design — Novel Claims Assessment

**Requester:** Strategizer (riemann-hypothesis, strategy-002, planning E008 synthesis)
**Query:** Assess four candidate novel claims for the final synthesis exploration — Von Mangoldt Hankel intermediate spectral rigidity (C1 Δ₃_sat=0.285), Dirichlet characters algebraically impossible for GUE, Gauss sum optimal N²/p≈250–310, and prime form factor normalization resolution (cosine sum ≠ spectral form factor). Also: what did strategy-001 previously conclude about novelty?

### Search path:
- Read factual/riemann-hypothesis/INDEX.md — directly relevant, all 14 findings scanned
- Read factual/riemann-hypothesis/c1-constraint-scorecard.md — relevant (Claim 1: Δ₃_sat=0.285)
- Read factual/riemann-hypothesis/complex-phase-matrices-gue-approach.md — relevant (Claims 1, 2)
- Read factual/riemann-hypothesis/gauss-sum-phases-permanently-goe.md — relevant (Claim 3)
- Read factual/riemann-hypothesis/prime-sum-form-factor-ramp.md — relevant (Claim 4)
- Read factual/riemann-hypothesis/riemann-operator-constraints.md — relevant (background)
- Read strategies/strategy-001/FINAL-REPORT.md — relevant (prior novelty conclusions)
- Read strategies/strategy-001/REASONING.md — supplementary context
- Meta-inbox (riemann-hypothesis): read 6 files (meta-001, meta-002, meta-003, s002-meta-001, s002-meta-006, s002-meta-007) — all operational/methodology; none bear on novelty of the four claims
- Meta library INDEX.md — no entries specifically about novelty assessment of these claims

### Returned:
- Claim 1 (C1 intermediate rigidity, Δ₃_sat=0.285): documented in c1-constraint-scorecard.md + complex-phase-matrices-gue-approach.md — anomalous rigidity attributed to Hankel structure; novelty not externally assessed
- Claim 2 (Dirichlet characters → GOE, algebraic proof): documented in complex-phase-matrices-gue-approach.md (Routes 1 & 2 with full proof) — library treats this as a genuine structural result; strategy-001 didn't address it (predates E006)
- Claim 3 (Gauss sum N²/p≈250–310 optimal): documented in gauss-sum-phases-permanently-goe.md — chirp interpretation identified; strategy-001 didn't address this
- Claim 4 (cosine sum ≠ form factor; MAD=14.5%): documented in prime-sum-form-factor-ramp.md — normalization resolution fully documented with derivation; strategy-001 didn't address this
- Strategy-001 novelty conclusions: FINAL-REPORT.md declares "No genuinely novel claims emerged" for its three claims (Gibbs obstruction, Toeplitz-Hankel dichotomy, super-rigidity quantification)

### Skipped:
- Other factual library topics (QG, Yang-Mills, SED, etc.) — not relevant to RH operator claims
- Meta library goal-design/, methodology/, system-behavior/ — relevant to exploration design, not to novelty of claims

## 2026-03-26: Query for Strategy-002 Exploration 001 — "Map QG+F's Explanatory Debts"

**Requester:** Strategizer (strategy-002, quantum-gravity-2)
**Query:** Four sub-queries for launching Exploration 001 ("Map QG+F's Explanatory Debts"):
1. QG+F's known limitations and gaps — what QG+F cannot explain, predict, or address
2. Emergent gravity and "gravitize the quantum" approaches — alternative explanatory frameworks
3. SCG v2.0's key findings — valuable conceptual ideas from previous strategy
4. Meta-lessons about designing exploration goals for gap-mapping or survey tasks

**Files searched (40+ files read):**

Factual library:
- INDEX.md (root)
- quadratic-gravity-fakeon/INDEX.md, core-idea.md, black-hole-predictions.md, microcausality-and-novel-signatures.md, standard-model-and-agravity.md, experimental-signatures-beyond-cmb.md
- gravitize-the-quantum/INDEX.md, landscape-overview.md, scg-theory-construction.md, scg-adversarial-assessment.md, scg-v2-causal-order-rewrite.md
- emergent-gravity/INDEX.md, entanglement-and-holography/INDEX.md, holographic-entanglement-spacetime.md, criticisms-and-limitations/INDEX.md, limitations-overview.md
- cross-cutting/INDEX.md, cosmological-constant-problem.md, information-paradox.md, entanglement-gravity-bootstrap.md, information-theoretic-constructive-axioms.md, cost-function-ghost-selection-negative.md
- constraints/INDEX.md

Strategy-001 final report:
- strategy-001/FINAL-REPORT.md

Meta-inbox (quantum-gravity-2):
- Empty (no files)

**Findings delivered:** Comprehensive results organized by 4 sub-queries. Detailed content returned for: (1) 12 specific QG+F explanatory debts, (2) 3 alternative framework categories, (3) 7 key SCG findings, (4) 5 meta-lessons from strategy-001.

**Gaps identified:**
- Meta-inbox for quantum-gravity-2 is empty — no accumulated meta-lessons from previous explorations to draw on
- No dedicated "QG+F open problems" synthesis document exists (information is distributed across multiple files)

## 2026-03-26: Query for Strategy-002 Exploration 002 — "Extract Viable Conceptual Moves from SCG v2.0"

**Requester:** Strategizer (strategy-002, quantum-gravity-2)
**Query:** Six sub-queries for launching Exploration 002:
1. All library entries about SCG — theory construction, adversarial assessment, v2.0 causal order rewrite (full content)
2. Cost function ghost-selection negative result (full content)
3. Pedraza complexity-geometry result — what was found about complexity → Einstein equations
4. Oppenheim postquantum gravity — current status
5. Barandes stochastic-quantum correspondence (full content)
6. Meta-lessons from meta-inbox about what worked/failed in strategy-001

**Files searched (30+ files read):**

Factual library:
- INDEX.md (root)
- gravitize-the-quantum/INDEX.md, landscape-overview.md, scg-theory-construction.md, scg-adversarial-assessment.md, scg-v2-causal-order-rewrite.md, stochastic-spacetime-qm-synthesis.md, barandes-verlinde-stochastic-emergence.md, oppenheim-postquantum-classical-gravity.md
- cross-cutting/INDEX.md, cost-function-ghost-selection-negative.md
- emergent-gravity/entanglement-and-holography/holographic-entanglement-spacetime.md

Strategy-001:
- strategy-001/FINAL-REPORT.md

Meta-inbox (quantum-gravity-2 instance level):
- meta-exploration-003.md through meta-exploration-009.md (all strategy-001 construction/repair/comparison phases)

Meta-inbox (quantum-gravity-2 strategies level):
- meta-exploration-001.md (exploration methodology)

**Findings delivered:** Full content of all 9 requested documents plus 7 meta-learning entries. Organized response covering: SCG full trilogy (construction + adversarial + v2.0), cost function negative result, Pedraza findings, Oppenheim status, Barandes full content, strategy-001 FINAL-REPORT synthesis, and 8 meta-lessons from meta-inbox.

**Gaps identified:**
- No dedicated Pedraza complexity-geometry file exists (findings distributed across scg-theory-construction.md and cost-function-ghost-selection-negative.md)
- No dedicated file on complexity=volume or complexity=action (flagged in prior librarian log entry)

## 2026-03-26: Query for Strategy-003 Exploration 001 — "QG+F–AS Unification Conjecture Statement"

**Requester:** Strategizer (strategy-003, quantum-gravity-2)
**Query:** Five sub-queries for launching Exploration 001 (precise conjecture statement + testable/falsifying implications):
1. Relationship between QG+F's AF fixed point and AS's Reuter fixed point (SWY two-fixed-point result)
2. Ghost fate at strong coupling / non-perturbative scales (ghost confinement conjecture, QCD analogy)
3. Predictions where QG+F and AS differ (inflation r, black holes, spectral dimension profile)
4. Existing analysis of whether QG+F = AS has been explored or published
5. Fixed point compatibility — AF fixed point connecting to NGFP via RG flow

**Files searched (45+ files read):**

Factual library:
- INDEX.md (root)
- asymptotic-safety/INDEX.md, swy-two-fixed-points.md, cosmology.md, black-holes-and-singularity-resolution.md, graviton-propagator.md, limitations.md, reuter-fixed-point.md, spectral-dimension.md, core-idea.md, functional-rg.md, critical-assessment.md, standard-model.md
- quadratic-gravity-fakeon/INDEX.md, core-idea.md, qcd-analogy-ghost-confinement.md, black-hole-predictions.md, analyticity-sacrifice.md, research-program-status.md, physical-beta-functions.md, inflationary-predictions.md, explanatory-debts-catalog.md
- cross-cutting/INDEX.md, qgf-vs-as-cmb-discrimination.md, spectral-dimension-running.md, spectral-dimension-propagator-constraint.md, entanglement-gravity-bootstrap.md
- bmeg/INDEX.md, uv-convergence-on-ds2.md, prediction-sensitivity.md, eta-h-self-consistency.md

Meta-inbox (quantum-gravity-2):
- meta-exploration-001.md through meta-exploration-009.md (all 9 files)

**Findings delivered:** Comprehensive dossier organized by 5 sub-queries, with full content from all relevant library entries. See response below.

**Gaps identified:**
- No dedicated file on the QG+F = AS conjecture itself (this is what Exploration 001 will produce)
- No file cataloging RG trajectories connecting AF and NGFP fixed points
- No file on Platania's work connecting AS and QG+F specifically (mentioned in research-program-status.md but no dedicated entry)
- The SWY result (swy-two-fixed-points.md) is the closest existing analysis; it was produced by strategy-002 exploration-001
- No lattice QG+F results exist to compare with CDT/Hamber lattice AS results

## 2026-03-26: Query for Strategy-004 Exploration — "Ghost Propagator Specification"

**Requester:** Strategizer (strategy-004, quantum-gravity-2)
**Query:** Five sub-queries for launching a Ghost Propagator Specification exploration:
1. Ghost confinement mechanisms (Becker mass divergence, Draper complex pole tower, Platania fictitious ghosts)
2. QCD-gravity analogy details — mapping between quark confinement and ghost confinement
3. Existing propagator reconstruction results from AS/FRG
4. Ghost fate at strong coupling assessment
5. Meta-learning about goal design scope for technical physics explorations

**Files searched (20+ files read):**

Factual library:
- INDEX.md (root)
- quadratic-gravity-fakeon/INDEX.md, qcd-analogy-ghost-confinement.md
- asymptotic-safety/INDEX.md, ghost-fate-strong-coupling.md, graviton-propagator.md, swy-two-fixed-points.md, limitations.md, af-ngfp-fixed-point-connection.md
- cross-cutting/INDEX.md, unified-qgf-as-framework/INDEX.md, unified-qgf-as-framework/discriminating-predictions.md, unified-qgf-as-framework/open-problems.md

Meta-inbox (quantum-gravity-2):
- meta-exploration-001.md, meta-exploration-004.md, meta-exploration-006.md
- meta-exploration-s3-001.md through meta-exploration-s3-009.md

**Findings delivered:** Full content from 7 factual library files and 8 meta-inbox files. Key material: ghost-fate-strong-coupling.md (4 mechanisms, zero confirmations), qcd-analogy-ghost-confinement.md (structural mapping + 7 breakdown points), graviton-propagator.md (Knorr-Saueressig 2022 methodology, Wick rotation obstruction), discriminating-predictions.md (ghost dissolution as single strongest discriminator), open-problems.md (#2 spin-2 confinement), af-ngfp-fixed-point-connection.md (INCONCLUSIVE verdict). Meta-lessons: single-question pattern, pre-loaded context, one task per exploration, failure path instruction, null hypothesis development.

**Gaps identified:**
- No file exists for the specific C²-extended FRG propagator computation (this is what the exploration targets)
- The Knorr-Saueressig 2022 methodology is the closest template but excludes C² term
- No Lorentzian spectral reconstruction methodology file exists (Bonanno et al. 2022 methodology only mentioned, not detailed)

## 2026-03-26: Query for Strategy-002 Challenger Interpretation Design (nature-of-time)

**Requester:** Strategizer (strategy-002, nature-of-time)
**Query:** Context for designing a challenger interpretation of time to compete against the computational interpretation (time = computationally irreducible processing of quantum correlations). Four sub-queries:
1. Causal fundamentalism / causal set theory approaches to time
2. Thermodynamic realism / Prigogine's fundamental irreversibility
3. Experience-first / consciousness-based approaches
4. Process philosophy connections to physics

**Files searched (20+ files read):**

Factual library:
- INDEX.md (root)
- cross-cutting/INDEX.md, temporal-realism-irreducible-becoming.md, computational-irreducibility-thesis.md, three-layer-time-synthesis.md, problem-of-time.md, page-wootters-mechanism.md, arrow-of-time-from-entanglement.md, time-from-entanglement-synthesis.md, entanglement-thesis-adversarial-assessment.md
- causal-set-theory/INDEX.md, core-idea.md, dynamics.md, cosmological-constant.md, limitations.md
- gravitize-the-quantum/INDEX.md

Grep searches:
- "consciousness|panpsychism|experience.*time|Chalmers|IIT|integrated information" across factual library
- "Smolin|temporal naturalism|causal fundamentalism|process.*philosophy|Whitehead.*physics" across factual library
- "Prigogine|dissipative|irreversibility.*fundamental|far.from.equilibrium" across factual library

Meta-inbox (nature-of-time):
- meta-exploration-001.md, meta-exploration-005.md through meta-exploration-010.md

**Findings delivered:** Comprehensive results organized by 4 sub-queries plus the existing computational thesis (as the target to beat). Library has STRONG coverage of causal set theory (15 files), STRONG coverage of temporal realism / becoming / Prigogine (temporal-realism-irreducible-becoming.md is a dedicated 190-line treatment), MODERATE coverage of process philosophy (Whitehead covered within temporal-realism), and ZERO dedicated coverage of consciousness-based / experience-first approaches to time (panpsychism, IIT, Chalmers hard problem of temporal experience). The library also contains the full three-thesis investigation from nature-of-time strategy-001 (entanglement thesis, computational thesis, becoming thesis, adversarial assessment, three-layer synthesis) which provides the competitive landscape.

**Gaps identified:**
- NO file on consciousness-based approaches to time (panpsychism, IIT, Chalmers, Tononi)
- NO file on Penrose-Hameroff Orch-OR as a time/consciousness theory
- NO file on retrocausation / two-state vector formalism and its implications for time
- NO dedicated file on Smolin's temporal naturalism (covered only within temporal-realism-irreducible-becoming.md)
- NO file on Unger-Smolin "The Singular Universe and the Reality of Time" argument
- NO file on energetic causal sets (Cortês-Smolin program)
- NO file on the relationship between CST sequential growth and process philosophy formally
- Prigogine coverage is a sub-section within temporal-realism, not a standalone treatment

## 2026-03-26: Query for Strategy-004 Exploration — "BH Evaporation Phase Transition"

**Requester:** Strategy-004 (quantum-gravity-2)
**Query:** Five sub-queries for launching a BH Evaporation Phase Transition exploration in the unified QG+F--AS framework:
1. Bonanno-Reuter BH thermodynamics (RG-improved metric, singularity resolution, two horizons, Planck remnant, g* value, remnant mass)
2. Bonanno et al. 2025 spontaneous ghostification instability (threshold r_H ~ 0.876/m_2)
3. QG+F BH predictions (fakeon selects Schwarzschild, Wald entropy, LPPS results)
4. QCD deconfinement phase transition features (gravitational deconfinement analogy)
5. PBH/dark matter remnant observational constraints

**Files searched (20+ files read):**

Factual library:
- INDEX.md (root)
- asymptotic-safety/INDEX.md, black-holes-and-singularity-resolution.md, reuter-fixed-point.md, cosmology.md, ghost-fate-strong-coupling.md, limitations.md
- quadratic-gravity-fakeon/INDEX.md, black-hole-predictions.md, qcd-analogy-ghost-confinement.md, research-program-status.md
- cross-cutting/INDEX.md, qgf-vs-as-bh-compatibility.md, unified-qgf-as-framework/INDEX.md, unified-qgf-as-framework/framework-conjecture.md, unified-qgf-as-framework/novel-predictions.md, cdt-phase-diagram.md, gravitational-bound-states.md, information-paradox.md

Meta-inbox (quantum-gravity-2):
- meta-exploration-s4-001.md (ghost propagator specification meta-learning)

**Findings delivered:** Full content from all 18+ files covering: (1) Bonanno-Reuter metric with lapse function formula, g* values across truncations (0.1-1.2), remnant mass ~10^{-5} g, alpha > 1 requirement; (2) Bonanno et al. 2025 spontaneous ghostification at r_H ~ 0.876/m_2, three-possibility analysis under QG+F = AS; (3) LPPS three solution families, fakeon selects Schwarzschild (S_2^- = 0), Wald entropy S = A/(4G) + O(l_P^2/r_H^2); (4) CDT phase diagram (A/B/C/C_b phases), QCD deconfinement analogy (Phase C = confined = 4D spacetime, Phase A = deconfined), Holdom-Ren structural mapping with 7 breakdown points; (5) PBH remnant DM candidates (~10^{-5} g), GW signal at ~100 Hz, LISA-era observability (2030s), no quantitative PBH mass-spectrum constraints in library.

**Gaps identified:**
- No dedicated file on BH evaporation phase transition dynamics (this is what the exploration targets)
- No quantitative PBH mass spectrum or abundance constraints from Planck remnants
- No file on QCD deconfinement transition temperature / order / features in detail (only CDT analogy)
- No file mapping QCD lattice thermodynamics results to gravitational phase transition
- The g* value used in the BR metric formula is not precisely specified beyond "g* = g_N" (the NGFP value of dimensionless Newton's coupling, ranging 0.1-1.2 across truncations); the cosmology file gives g* = 540pi/833 in one running-G model
- No computation exists for remnant mass as a function of g* and m_2 jointly

## 2026-03-26: Query for Strategy-004 Exploration — "Inflation Predictions in the Unified QG+F--AS Framework"

**Requester:** Strategy-004 (quantum-gravity-2)
**Query:** Five sub-queries covering: (1) QG+F inflationary predictions (r, n_s, Bianchi-Gamonal precision formula, six-derivative extension, n_s tension), (2) AS inflation findings (Codello 2014, Bonanno-Platania, b parameter, NGFP-driven inflation), (3) n_s tension observational status (0.974 vs 0.967, resolution paths), (4) six-derivative extension details (n_s prediction, R^3 coefficients), (5) NGFP critical exponents and numerical values across truncations.

**Files searched (20+ files read):**

Factual library:
- INDEX.md (root)
- quadratic-gravity-fakeon/INDEX.md, inflationary-predictions.md, ns-tension-resolution-paths.md, six-derivative-extension.md
- asymptotic-safety/INDEX.md, cosmology.md, reuter-fixed-point.md, swy-two-fixed-points.md, ghost-fate-strong-coupling.md, af-ngfp-fixed-point-connection.md, limitations.md
- cross-cutting/INDEX.md, cmb-spectral-index-tension.md, qgf-vs-as-cmb-discrimination.md, inflationary-model-selection-post-act.md, unified-qgf-as-framework/INDEX.md, unified-qgf-as-framework/novel-predictions.md

Meta-inbox (quantum-gravity-2):
- meta-exploration-s4-001.md, meta-exploration-s4-002.md

**Findings delivered:** Full content from all relevant library entries covering: QG+F inflation mechanism and predictions (r in [0.0004, 0.0035], n_s ~ 0.967, Bianchi-Gamonal formula r ~ 3(1-beta/6alpha)(n_s-1)^2, Anselmi 2023 causality bound, full CMB catalog), AS inflation taxonomy (4 classes, 6 models, most predict Starobinsky r ~ 0.003), n_s tension observational status (CMB+DESI: 0.974 +/- 0.003, CMB alone: 0.969 +/- 0.003, 2.3-sigma tension), resolution paths (RG running RULED OUT at 10^{-14}, R^3 correction WORKS at delta_3 ~ -10^{-4}), six-derivative extension (super-renormalizable, d_s = 4/3, 14 DOF, R^3 shifts n_s to 0.974 and r to 0.0045), NGFP critical exponents across truncations (Einstein-Hilbert: theta = 1.55 +/- 3.83i; R^2 truncation: theta_1 = 2.38, theta_2,3 = 1.26 +/- 2.74i; Benedetti et al. 4-param: theta_0 = 2.51, theta_1 = 1.69, theta_2 = 8.40, theta_3 = -2.11), unified r formula, Bonanno-Platania b parameter and its relation to critical exponents.

**Gaps identified:**
- No library entry computes the precise mapping from NGFP critical exponents to the Bonanno-Platania b parameter (b ~ theta/(16pi^2) is stated but not derived)
- No paper has done AS inflation with full R^2 + C^2 truncation simultaneously (the "missing calculation" flagged in qgf-vs-as-cmb-discrimination.md)
- No library entry on the R^3 coefficient in the NGFP effective action specifically (whether AS determines delta_3 from first principles)
- No file on Lorentzian critical exponents (D'Angelo et al. 2024 Lorentzian NGFP exists at g*=1.15, lambda*=0.42, but critical exponents in Lorentzian signature not cataloged)

## 2026-03-27: Query for Strategy-001 Exploration 001 — GUE Statistics for Riemann Zeta Zeros (riemann-hypothesis)

**Requester:** Strategizer (strategy-001, riemann-hypothesis instance)
**Query:** Two sub-queries:
1. Any factual content related to Riemann Hypothesis, zeta function, random matrix theory, or spectral approaches to number theory
2. Meta-learning lessons about designing effective first explorations, scoping computational tasks, and what makes explorations succeed or fail

**Files searched (22 files read):**

Factual library:
- INDEX.md (root) — scanned all 12 top-level categories

Meta library (all 18 entries):
- goal-design/INDEX.md, one-task-per-exploration.md, specify-failure-paths.md, preload-context-from-prior-work.md, use-line-count-targets.md, name-specific-authors-and-papers.md, use-classification-schemes.md, use-absolute-file-paths.md
- methodology/INDEX.md, divergent-survey-pattern.md, devils-advocate-after-construction.md, predict-attack-synthesize-sequence.md, adversarial-explorations-need-null-hypothesis.md, repair-pattern.md, benchmark-comparison-early.md, verification-catches-library-errors.md
- system-behavior/INDEX.md, computation-vs-reasoning-limits.md, explorer-crashes-and-path-confusion.md, explorer-stalling-and-nudge-pattern.md, synthesis-vs-research-mode.md

Meta-inbox (riemann-hypothesis):
- Empty (no files)

**Findings delivered:**
- Factual library: ZERO relevant content. The entire factual library is quantum-gravity-focused. No entries on Riemann Hypothesis, zeta functions, random matrix theory, GUE statistics, Montgomery-Odlyzko, spectral approaches to number theory, or any analytic number theory topic.
- Meta library: ALL 18 entries returned as relevant to designing the first exploration. Most critical for a computational GUE-statistics exploration: computation-vs-reasoning-limits.md (explorers can evaluate formulas but not perform novel computations — critical for scoping a computational task), one-task-per-exploration.md (keep the GUE computation as ONE task, don't combine with analysis), use-line-count-targets.md (150-300 for verification, 300-500 for construction), specify-failure-paths.md (include "if computation fails, explain why"), use-absolute-file-paths.md, divergent-survey-pattern.md (good model for first exploration), synthesis-vs-research-mode.md (distinguish computation mode from research mode explicitly).

**Gaps identified:**
- ZERO factual library coverage of analytic number theory, Riemann Hypothesis, random matrix theory, or spectral methods — this is an entirely new domain for the library
- Meta-inbox is empty — no accumulated meta-lessons from previous RH explorations

## 2026-03-27: Query for Strategy-001 Explorations 001-002 — Yang-Mills Existence and Mass Gap

**Requester:** Strategizer (strategy-001, yang-mills instance)
**Query:** Nine topic searches: Yang-Mills, lattice gauge theory, renormalization group, constructive QFT, mass gap, Wightman axioms, Osterwalder-Schrader axioms, continuum limits, non-perturbative QFT. Also meta-learning about designing literature survey / technical mapping explorations.

**Files searched (30+ files read/grepped):**

Factual library:
- INDEX.md (root) — scanned all 12 top-level categories
- Grep search across entire factual library for: Yang-Mills, mass gap, Wightman, Osterwalder-Schrader, constructive QFT, lattice gauge, Balaban, Glimm-Jaffe, continuum limit, non-perturbative QFT, renormalization group
- cross-cutting/qgf-vs-as-analyticity-compatibility.md (Osterwalder-Schrader mention)
- quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md (mass gap in R^2 gravity, QCD analogy)
- asymptotic-safety/core-idea.md (Yang-Mills antiscreening analogy)
- asymptotic-safety/functional-rg.md (functional renormalization group)
- string-theory/ads-cft.md (N=4 super Yang-Mills)
- causal-set-theory/entanglement-entropy.md (Wightman function)
- causal-set-theory/qft-sorkin-johnston.md (Wightman two-point function)

Meta library (all 18 entries read):
- goal-design/ (7 entries)
- methodology/ (7 entries)
- system-behavior/ (4 entries)

Meta-inbox (yang-mills):
- Empty (no files)

**Findings delivered:**
- Factual library: ZERO dedicated content on Yang-Mills existence and mass gap, Balaban's renormalization group program, constructive QFT (Glimm-Jaffe), Wightman axioms, or lattice gauge theory as a mathematical subject. Only tangential mentions: (1) Yang-Mills appears in AS antiscreening analogy, AdS/CFT boundary theory, and Horava-Lifshitz tropological extension; (2) mass gap appears in QCD-gravity ghost confinement analogy and Frasca R^2 gravity result; (3) Osterwalder-Schrader appears once in analyticity compatibility analysis; (4) Wightman function appears in CST entanglement entropy; (5) renormalization group is covered extensively but only in the gravitational AS context; (6) continuum limits discussed in many QG contexts but not in the Yang-Mills/constructive QFT sense.
- Meta library: ALL 18 entries returned. Most critical for literature survey / technical mapping: divergent-survey-pattern.md (4-part survey pattern), one-task-per-exploration.md, name-specific-authors-and-papers.md, use-line-count-targets.md, specify-failure-paths.md, use-classification-schemes.md, preload-context-from-prior-work.md, verification-catches-library-errors.md, computation-vs-reasoning-limits.md.

**Gaps identified:**
- ZERO factual library coverage of: Yang-Mills existence and mass gap problem, Balaban's RG program for lattice YM, constructive QFT (Glimm-Jaffe phi^4 in 2D/3D), Wightman axioms, Osterwalder-Schrader reconstruction theorem, lattice gauge theory as mathematical framework, non-perturbative QFT in the constructive sense
- This is an entirely new domain for the library — similar situation to the Riemann Hypothesis instance

## 2026-03-27: Query for Amplituhedron Strategy-001 First Exploration

**Requester:** Strategizer (amplituhedron strategy-001)
**Query:** Library content on: (1) scattering amplitudes, (2) N=4 super Yang-Mills, (3) amplituhedron / positive geometry, (4) Arkani-Hamed/Trnka work, (5) computational approaches to amplitude calculations. Also meta-library lessons about designing first explorations, computational explorations, scope management.

**Files searched:**

Factual library:
- factual/INDEX.md — top-level index, 178 findings across 14 categories
- factual/yang-mills/INDEX.md — 9 findings on Yang-Mills Millennium Problem (constructive QFT, not scattering amplitudes)
- factual/string-theory/INDEX.md — 8 findings; checked graviton-mechanism.md for amplitude content
- factual/string-theory/graviton-mechanism.md — mentions string scattering amplitudes / UV finiteness but nothing on amplituhedron/positive geometry
- factual/cross-cutting/INDEX.md — 42 findings; no amplituhedron content
- Grep across entire library for: amplituhedron, positive geometry, Arkani-Hamed, Trnka, BCFW, on-shell, twistor, grassmannian — no dedicated entries found; only incidental mentions of "scattering amplitudes" in unrelated QG contexts

Meta library:
- meta/INDEX.md — 4 categories (goal-design 11, methodology 8, system-behavior 4, missionary 0)
- meta/goal-design/INDEX.md — all 11 entries read
- meta/methodology/INDEX.md — all 8 entries read
- meta/system-behavior/INDEX.md — all 4 entries read

Amplituhedron meta-inbox:
- /instances/amplituhedron/meta-inbox/ — directory is empty (no recent meta-notes)

**Findings:**

FACTUAL: **Nothing directly relevant.** The library has zero entries on:
- Amplituhedron or positive geometry
- N=4 super Yang-Mills scattering amplitudes
- Arkani-Hamed/Trnka work
- BCFW recursion or on-shell methods
- Grassmannian geometry for amplitudes
- Momentum twistor space
- Computational amplitude methods

The closest content is incidental: string theory graviton-mechanism.md discusses string scattering amplitudes (worldsheet CFT, UV finiteness) — conceptually adjacent but not operationally relevant. Yang-Mills library is entirely about the Millennium Prize (constructive QFT / mass gap), not scattering amplitude computation.

META: **11 highly relevant entries returned** covering first-exploration design and computational exploration patterns.


## 2026-03-27: Query for Strategy-002, Stochastic-Electrodynamics Mission

**Requester:** Strategizer (stochastic-electrodynamics, strategy-002)
**Query:** Pre-launch context for three parallel computational explorations. Four sub-topics:
1. SED tunneling / double-well potential — any prior computation of barrier crossing rates?
2. Two coupled oscillators / correlations from shared ZPF — de la Peña, Stochastic Optics, Bell S?
3. Hydrogen self-ionization — what exactly did Nieuwenhuizen 2015/2020 and Cole & Zou 2003 show?
4. Goal design lessons for Math Explorers doing SED computations specifically.

### Search path:
- Read factual/INDEX.md → followed stochastic-electrodynamics/ (primary) — highly relevant
- Read factual/stochastic-electrodynamics/INDEX.md — all 14 entries reviewed for relevance
- Read hydrogen-self-ionization.md — directly relevant (topic 3)
- Read entanglement-bell-contested.md — directly relevant (topic 2)
- Read linearity-boundary-pattern.md — directly relevant (topics 1, 2, 3: tunneling listed as open)
- Read established-successes.md — relevant background; van der Waals (Boyer 1973) confirms linear success
- Read anharmonic-oscillator-failure.md — relevant: has exact QM reference table; documents simulation context
- Read sed-ho-zpf-spectral-density.md — relevant: verified formula needed for any new simulation
- Skipped: quantum-coherence-failure.md, spin-anomalous-moment-status.md, sed-ho-numerical-verification.md, sed-ho-uv-divergence-structure.md, anharmonic-langevin-o-beta-failure.md, anharmonic-ald-landau-lifshitz.md, uv-cutoff-parameter-scan.md, sed-novelty-assessment.md — not directly relevant to these 3 new exploration topics (already well-documented in strategy-001)
- Read meta/INDEX.md → followed goal-design/, methodology/
- Read meta/goal-design/INDEX.md — 22 entries; selected 6 most relevant for SED computation context
- Read preload-context-from-prior-work.md — directly relevant (topic 4)
- Read specify-computation-parameters.md — directly relevant (topic 4)
- Read specify-failure-paths.md — directly relevant (topic 4)
- Read separate-numerical-from-physics-parameters.md — directly relevant (topic 4; SED-specific)
- Read require-baseline-adjusted-significance.md — directly relevant (topic 4; SED-specific)
- Read prioritize-novelty-assessment.md — relevant for framing any positive SED computation result
- Read instruct-incremental-writing.md — relevant for SED report stall prevention
- Read meta/methodology/INDEX.md — scanned; adversarial-check-between-phases and investigate-why-on-discrepancies most relevant but already captured in meta-inbox
- Meta-inbox: read all 6 files; all 6 relevant to topic 4

### Returned:
- hydrogen-self-ionization.md — full three-phase history: Cole & Zou 2003, Nieuwenhuizen 2015, Nieuwenhuizen 2020
- entanglement-bell-contested.md — de la Peña 2010, Marshall & Santos SO, Santos 2020, loophole-free Bell tests
- linearity-boundary-pattern.md — full scorecard; tunneling explicitly listed as "never computed"
- anharmonic-oscillator-failure.md — QM reference table (7 beta values); simulation comparison table
- sed-ho-zpf-spectral-density.md — verified ZPF force PSD formula and documented factor-of-pi bug
- preload-context-from-prior-work.md — lesson + E004 evidence (14 min vs 36 min)
- specify-computation-parameters.md — lesson + code template variant + threshold-finding variant
- specify-failure-paths.md — lesson + SED-specific variants
- separate-numerical-from-physics-parameters.md — SED-origin lesson; template specification
- require-baseline-adjusted-significance.md — SED-origin lesson; template language
- meta-inbox files E001–E006 — all 6 read; key lessons: UV divergence warning, sequential scans, noise normalization formula pre-provision, ALD vs Langevin distinction, dt confounding, adversarial framing

### Skipped:
- All other factual library topics (QG approaches, Yang-Mills, Riemann, etc.) — not relevant to SED computations
- meta/methodology/math-explorer-dimensional-analysis.md, decisive-negative-pivot.md — not applicable to SED simulation explorations
- meta/goal-design/use-classification-schemes.md, require-gap-analysis-in-formal-mappings.md, allow-explorer-synthesis.md — less critical given specific computational nature of the three explorations

---

## 2026-03-27: Query for Yang-Mills Mission (strategy-002, explorations 001+002)

**Requester:** Strategizer (yang-mills, strategy-002)
**Query:** Pre-search for two parallel explorations: (1) deep extraction of Shen-Zhu-Zhu (arXiv:2204.12737, CMP 400, 2023) — Bakry-Émery technique, β < 1/48 bound origin, failure at larger β, relation to Chatterjee's "strong mass gap" condition; (2) computational measurement of spectral gap / Poincaré constant for SU(2) lattice YM across β = 0.02 to β = 3.0, including prior measurements and available methods.

**Files searched (18 files read):**

Factual library:
- factual/INDEX.md — top-level scan
- factual/yang-mills/INDEX.md — all 12 findings scanned
- factual/yang-mills/shen-zhu-zhu-stochastic-analysis.md ← PRIMARY for Exploration 001
- factual/yang-mills/chatterjee-probabilistic-program.md ← RELEVANT (strong mass gap condition)
- factual/yang-mills/gap-structure-overview.md ← RELEVANT (Chatterjee conditional theorem context)
- factual/yang-mills/lattice-numerical-evidence.md ← PRIMARY for Exploration 002 (Atlas SU(2) baseline, β range, known observables)
- factual/yang-mills/adhikari-cao-technique-and-obstruction.md — scanned; spectral gap Δ_G → 0 obstruction directly relevant to Exploration 001

Meta library:
- meta/INDEX.md — top-level scan
- meta/goal-design/INDEX.md — scanned all 24 entries
- meta/goal-design/specify-rigor-level.md ← DIRECTLY RELEVANT (E001 and E006 evidence for "what EXACTLY do they prove" pattern)
- meta/goal-design/preload-context-from-prior-work.md ← DIRECTLY RELEVANT
- meta/goal-design/specify-computation-parameters.md ← DIRECTLY RELEVANT for Exploration 002
- meta/methodology/INDEX.md — scanned all 19 entries
- meta/methodology/standard-explorer-for-literature-surveys.md ← RELEVANT (Exploration 001 is literature/paper extraction, not computation)
- meta/system-behavior/INDEX.md — scanned

Meta-inbox (yang-mills):
- meta-exploration-001.md ← RELEVANT (naming papers, theorem-level precision)
- meta-exploration-002.md ← RELEVANT (yang-mills context injection lesson)
- meta-exploration-003.md ← DIRECTLY RELEVANT (SU(2) lattice simulation: β values, lattice sizes, failure modes)
- meta-exploration-004.md ← RELEVANT (numerical vs. rigorous gap framing)
- meta-exploration-006.md ← DIRECTLY RELEVANT ("what EXACTLY do they prove" produced the best precision)
- meta-exploration-007.md ← RELEVANT (novelty assessment format)
- meta-exploration-008.md ← DIRECTLY RELEVANT (spectral gap computation stalled — timeout warning for Exploration 002)
- meta-exploration-009.md ← RELEVANT (synthesis with full context)
- meta-exploration-010.md ← RELEVANT (adversarial review found definitional error in spectral gap)

### Returned:
- shen-zhu-zhu-stochastic-analysis.md — full content (Bakry-Émery technique, β < 1/48 derivation, weak coupling failure, complementarity table)
- chatterjee-probabilistic-program.md — full content including strong mass gap ⟹ area law theorem, Gaussian limit results
- gap-structure-overview.md — full content (two-tier structure, 12-step chain, Chatterjee conditional theorem context)
- lattice-numerical-evidence.md — full content (Atlas SU(2) simulation results, β range 2.0-3.0, practical size requirements, glueball mass discussion)
- specify-rigor-level.md — "what EXACTLY do they prove" pattern + variants
- preload-context-from-prior-work.md — paste formulas directly, pointing-to-library variant
- specify-computation-parameters.md — exact parameters + code templates + threshold-finding scan variants
- standard-explorer-for-literature-surveys.md — use standard (not math) explorer for paper extraction
- meta-exploration-006 lesson — "what specifically fails" pattern for structural vs. technical obstructions
- meta-exploration-008 lesson — spectral gap computation timeout warning; save code to files; single focused script preferred
- meta-exploration-010 lesson — adversarial review essential before claiming novelty; cross-check definitions

### Skipped:
- All non-Yang-Mills factual library topics
- meta/goal-design/require-baryonic-completeness.md, specify-modified-inertia-vs-gravity.md, require-baseline-adjusted-significance.md — MOND/galaxy-specific, not relevant
- meta/methodology/decisive-negative-pivot.md, math-explorer-dimensional-analysis.md — not directly relevant to these task types

---

## 2026-03-27: Query for Riemann Hypothesis E007 Adversarial Design

**Requester:** Strategizer (riemann-hypothesis, strategy-002, E007 planning)
**Query:** Library context for designing an adversarial review of the C1 random-phase Von Mangoldt Hankel matrix pair correlation claim (MRD=7.9%). Needed: (1) adversarial null-hypothesis methodology lessons; (2) pair correlation baselines for GUE/random Hermitian matrices; (3) whether Von Mangoldt amplitude structure is necessary vs. flat amplitudes achieving same stats; (4) adversarial design lessons (null hypothesis structure, trial counts, statistical power).

### Search path:
- Read factual/riemann-hypothesis/INDEX.md → read c1-constraint-scorecard.md, complex-phase-matrices-gue-approach.md, gue-pair-correlation.md, arithmetic-matrix-operators-poisson-failure.md — all directly relevant
- Read meta/INDEX.md → followed goal-design/ and methodology/
- Read meta/goal-design/INDEX.md → read require-quantification-in-stress-tests.md, use-classification-schemes.md — directly relevant
- Read meta/methodology/INDEX.md → read adversarial-explorations-need-null-hypothesis.md, adversarial-check-between-phases.md, devils-advocate-after-construction.md — directly relevant
- Meta-inbox: read all 5 files (meta-001, meta-002, meta-003, s002-meta-001, s002-meta-006); s002-meta-001 and meta-003 relevant (scorecard format, scipy fallback warning); meta-001/002 marginally relevant (computation budget patterns)

### Returned:
- c1-constraint-scorecard.md — full corrected scorecard: pair correlation MRD=7.9% PASS, β=1.18 PARTIAL, Δ₃_sat=0.285 PARTIAL (vs GUE 0.495, actual zeros 0.156)
- complex-phase-matrices-gue-approach.md — GUE control baseline β=2.187; random phases β=1.655 (S002-E001) / 1.182 (S002-E005); non-factorizability principle
- gue-pair-correlation.md — zeta zeros MRD=9.1% (2000 zeros); high-height MRD=17.2% (500 zeros)
- arithmetic-matrix-operators-poisson-failure.md — flat real Hankel β=0.44; Toeplitz β=-0.31; amplitude structure alone insufficient
- adversarial-explorations-need-null-hypothesis.md — null hypothesis test mandatory: "Can observations be explained without this framework?"
- adversarial-check-between-phases.md — run standard canonical tests before Phase 3; lightweight vs. full adversarial formats
- require-quantification-in-stress-tests.md — compute quantitative bounds on each objection, not just argue; argued catch-22 = concern, computed = finding
- use-classification-schemes.md — FATAL/SERIOUS/MODERATE classification + "brutally honest" language for adversarial explorations
- s002-meta-001 — specify exact formulas for R₂ and Δ₃ in goal; sanity-check step for Hermitian non-degeneracy
- s002-meta-006 — scipy.optimize fallback protocol; specify fallback formula if scipy fails

### Skipped:
- gue-nearest-neighbor-spacing.md, spectral-form-factor-gue.md, berry-saturation-confirmed.md, berry-formula-quantitative-test.md, riemann-operator-constraints.md, trace formula entries — not directly relevant to adversarial design of pair correlation test
- meta/goal-design/: most entries not relevant to adversarial review design specifically
- meta/methodology/: repair-pattern, benchmark-comparison-early, multi-ansatz-sweep, staged-computation-goals, etc. — not relevant to adversarial phase
- meta-inbox meta-001, meta-002 — computation budget patterns, marginally relevant, not returned

---

## 2026-03-27: Query for Riemann Hypothesis Mission (strategy-002, Exploration 009 — Flat-Amplitude Δ₃ Test)

**Requester:** Strategizer (riemann-hypothesis, strategy-002)
**Query:** Context for Math Explorer computing Δ₃_sat for H_flat (N=500 Hermitian, flat amplitude 1, random complex phases), comparing to C1 (Δ₃_sat=0.285), GUE (Δ₃_sat≈0.565), and zeta zeros (Δ₃_sat≈0.156). Key question: Is C1's anomalous intermediate Δ₃=0.285 caused by von Mangoldt arithmetic structure, or is it generic to any GUE-class matrix? Known issues: scipy.optimize broken (numpy.Inf removed), incremental writing stall pattern.

### Search path:
- Read factual/INDEX.md — identified riemann-hypothesis/ as primary; noted E007 adversarial review finding that flat-amplitude achieves MRD=6.8% (better than C1)
- Read factual/riemann-hypothesis/INDEX.md — all entries relevant; berry-saturation-confirmed, c1-constraint-scorecard, complex-phase-matrices-gue-approach, pair-correlation-discriminating-power most critical
- Read factual/riemann-hypothesis/c1-constraint-scorecard.md — DIRECTLY RELEVANT: full corrected scorecard, Δ₃_sat=0.285 (L=25–50 avg), exact computation method (Dyson-Mehta integral, 200 windows per L), GUE Δ₃_sat≈0.495 at L=30, zeta zeros 0.156
- Read factual/riemann-hypothesis/berry-saturation-confirmed.md — RELEVANT: Dyson-Mehta formula note; GUE sim table at L=10/50/100; integral formula required (not sum formula)
- Read factual/riemann-hypothesis/complex-phase-matrices-gue-approach.md — RELEVANT: GUE control β=2.187, random phases β=1.18–1.67; flat-amplitude has no prior Δ₃ measurement
- Read factual/riemann-hypothesis/pair-correlation-discriminating-power.md — CRITICAL: E007 null comparison table shows flat-amplitude random phase MRD=6.8%, β=1.45 — better than C1; Δ₃ not yet measured for flat amplitude
- Read meta/INDEX.md — identified system-behavior/, goal-design/, methodology/ as relevant
- Read meta/system-behavior/explorer-stalling-and-nudge-pattern.md — CRITICAL: scipy ImportError stall pattern (computation-done-but-debugging variant); post-computation thinking stall (30 min for RH E007); pre-computation coding stall (5-6 min)
- Read meta/system-behavior/computation-vs-reasoning-limits.md — RELEVANT: Math Explorers fast on pure formula tasks (~2 min); self-debugging with expected-value context
- Read meta/goal-design/instruct-incremental-writing.md — CRITICAL: section-specific checkpoint instruction required; tie each write to its computation stage; confirmed for E006/E007/E008
- Read meta/goal-design/specify-computation-parameters.md — RELEVANT: provide exact implementation formula + known numerical anchor; startup diagnostics for fragile imports; expected output file keys
- Read meta/methodology/verify-unexpected-findings-immediately.md — RELEVANT: if result is unexpected, design immediate stress-test
- Read meta-inbox/s002-meta-exploration-006.md — CRITICAL: scipy.optimize ImportError (numpy.Inf); specify fallback manually; name expected npz keys; "computation-done-but-debugging" stall
- Read meta-inbox/s002-meta-exploration-007.md — CRITICAL: 30-min post-computation thinking stall; REPORT.md all-placeholder despite data saved; "write incrementally" must be section-specific
- Read meta-inbox/s002-meta-exploration-008.md — RELEVANT: same buffering pattern third time; kill after 30 min + manually complete is fastest route; section-completion marker [SECTION COMPLETE] pattern
- Read meta-inbox/s002-meta-exploration-001.md — RELEVANT: specify exact R₂ and Δ₃ formulas; sanity-check for Hermitian non-degeneracy

### Returned:

**Factual — Δ₃ computation methods and confirmed values:**
- C1 Δ₃_sat = 0.285 (L=25–50 average, Dyson-Mehta integral, 200 windows per L, N=500, 5 matrices) — from c1-constraint-scorecard.md
- GUE Δ₃_sat ≈ 0.495 at L=30, ≈0.566 at L=30–50 (theory) — from c1-constraint-scorecard.md table
- Zeta zeros Δ₃_sat = 0.1550 ± 0.0008 (onset L≈10–12, constant L=15–100) — from berry-saturation-confirmed.md
- GUE finite-size sim: Δ₃(L=50) = 0.250 — zeta still 38% more rigid than GUE sim — from berry-saturation-confirmed.md
- E007 adversarial null comparison: flat-amplitude random phase achieved MRD=6.8%, β=1.45 — but Δ₃ NOT YET MEASURED for flat-amplitude — this is the key gap E009 fills
- Δ₃ formula: Dyson-Mehta integral, NOT the sum formula (sum gives ~half correct value) — from berry-saturation-confirmed.md

**Factual — C1 construction and what's established:**
- C1: H_{jk} = Λ(|j-k|+1) × exp(iφ_{jk}), φ i.i.d. Uniform[0,2π], N=500, 5 matrices, β=1.18±0.22
- C1 is GUE-class by spacing KS criterion but shows anomalous rigidity (Δ₃=0.285 ≈ 50% of GUE, 1.8× stiffer than GUE sim)
- Adversarial review (E007): pair correlation PASS is 5-realization averaging artifact; Von Mangoldt amplitude unnecessary for pair correlation; Δ₃ difference between flat and C1 NOT YET TESTED
- E009 directly tests: "Does von Mangoldt amplitude explain C1's anomalous Δ₃=0.285?"
- If H_flat Δ₃_sat ≈ 0.285 → anomaly is generic to GUE-class, not arithmetic. If H_flat Δ₃_sat ≈ 0.495 (GUE) → anomaly is caused by von Mangoldt structure.

**Known issues — scipy, stalling, incremental writing:**
- scipy.optimize BROKEN in this environment (numpy.Inf removed in NumPy 1.25+). Use startup diagnostic: `python3 -c "import scipy.optimize; print(scipy.__version__)"`. Fallback: manual Brody fit grid search over β ∈ [0, 2.5] using manual chi-squared on spacing histogram.
- Δ₃ itself does not require scipy — it only requires numpy (minimize linear fit analytically over A, B for each window). scipy.optimize is only needed for Brody β fitting.
- Post-computation thinking stall: RH E007 entered 30-min loop after saving results.npz. Intervention needed after 15 min of no writing.
- Write-incrementally pattern: MUST tie each write to its computation stage. Example: "After computing Δ₃(L) for H_flat, write the H_flat section to REPORT.md before moving to comparison table."
- Section completion markers: "At end of each section, write [SECTION COMPLETE] before proceeding."
- If stall persists >30 min post-computation: kill + manually complete from conversation history.

**Meta lessons — Math Explorer code tasks:**
- Math Explorers complete pure formula optimization in ~2 min. N=500 matrix eigendecomposition is fast (seconds). Δ₃ scan (L=1 to 50, 200 windows each) takes ~1-3 min. Full E009 should complete computation in <10 min.
- Provide expected values in goal as debugging scaffolding: "GUE control should give Δ₃_sat ≈ 0.49–0.57; if Δ₃_sat < 0.3 for GUE control, something is wrong."
- Provide exact Δ₃ implementation in goal to prevent formula bugs (see s002-meta-001: mean-squared-residual/L was wrong).

### Skipped:
- gue-nearest-neighbor-spacing.md, spectral-form-factor-gue.md, berry-formula-quantitative-test.md — not needed for Δ₃ computation per se
- riemann-operator-constraints.md, trace formula files, gauss-sum-phases-permanently-goe.md — not relevant to flat-amplitude test
- All other factual domains (QG, SED, Yang-Mills, etc.) — not relevant
- meta/methodology/ most entries — verify-unexpected-findings-immediately returned as potentially relevant (if result is surprising)
- meta-inbox meta-002, meta-003 — general computation lessons already covered by later entries

## 2026-03-27: Query for RH strategy-003 (E003 + E004 parallel launch)

**Requester:** Strategizer (riemann-hypothesis, strategy-003)
**Query:** Two parallel explorations: (1) E003 — non-perturbative K(τ) from prime pair sums WITHOUT perturbative 1/⟨d⟩² expansion, then compute Σ₂(L) and Δ₃(L) via verified formula route; (2) E004 — Gauss sum matrix N²/p scaling verification at N=250 and N=1000 in addition to known N=500 result to test universality of N²/p ≈ 275.

### Search path:
- Read factual/INDEX.md → riemann-hypothesis section dense and relevant
- Read meta/INDEX.md → goal-design/, methodology/, system-behavior/ relevant
- Read meta-inbox: s003-meta-exploration-001.md, s003-meta-exploration-002.md, s002-meta-exploration-007.md, s002-meta-exploration-008.md
- Read factual/riemann-hypothesis/INDEX.md — 20 findings cataloged
- Read factual/riemann-hypothesis/prime-sum-form-factor-ramp.md — directly relevant to E003
- Read factual/riemann-hypothesis/gauss-sum-phases-permanently-goe.md — directly relevant to E004
- Read factual/riemann-hypothesis/spectral-form-factor-gue.md — K(τ) ground truth
- Read factual/riemann-hypothesis/berry-saturation-confirmed.md — Δ₃=0.1550 ground truth
- Read factual/riemann-hypothesis/berry-formula-quantitative-test.md — integral formula + bug warning
- Read meta/goal-design/specify-computation-parameters.md — timeout variant, normalization warnings
- Read meta/goal-design/instruct-incremental-writing.md — 7th confirmation context
- Read instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-001/REPORT-SUMMARY.md — E001 key result: perturbative approach failed, non-perturbative K(τ) identified as lead
- Read instances/riemann-hypothesis/strategies/strategy-003/REASONING.md — Strategizer's Phase 2 plan context

### Key findings returned to requester:
- Berry-Keating 1999 eq 4.18: correct K_primes normalization is K_density/(2πρ̄)² (NOT /2πρ̄)
- S002-E006 confirmed prime sums reproduce ramp with MAD=14.5%; fails plateau (needs off-diagonal)
- Correct Σ₂→Δ₃ formula verified: integral kernel (L³-2L²r+r³), NOT the wrong (L-r)³ kernel
- Gauss sum N=500: peak β=1.154 at p=809, N²/p≈309; optimal range N²/p≈250-310
- Universality claim was flagged as premature in literature (only N=500 tested)
- Critical meta-lessons: 20-30min timeout for prime sum computations; scipy.optimize broken; incremental write-then-proceed; save .npz after each block

## 2026-03-28: Query for thermal-time strategy-003 (coherent state test for Rindler wedge)

**Requester:** Strategizer (thermal-time, strategy-003)
**Query:** Context for a Math Explorer computing the coherent state test for the Rindler wedge — testing whether the structural mismatch between modular flow and physical dynamics (found for one-particle excitations under Gaussian approximation) persists for coherent state excitations, where the Gaussian modular Hamiltonian is exact. Need: (1) thermal-time factual library on excited-state result (Claim 3), Gaussian caveat, Rindler lattice setup; (2) meta-learning on running Math Explorers for lattice QFT; (3) meta-learning on goal design for computational explorations.

### Search path:
- Read factual/INDEX.md → thermal-time section highly relevant
- Read factual/thermal-time/INDEX.md → all 7 findings reviewed
- Read excited-state-modular-flow.md — PRIMARY (Claim 3: modular clock ticks at entanglement frequencies; Gaussian caveat; coherent state control explicitly recommended)
- Read rindler-bw-lattice-verification.md — PRIMARY (lattice setup: N=50/100/200, Williamson decomposition, BW profile, KMS exact, Calabrese-Cardy 1.5%)
- Read nonequilibrium-tth-post-quench.md — RELEVANT (parallel structural mismatch finding; product-state identity; squeezed state contrast)
- Read modular-hamiltonian-catalog.md — RELEVANT (Rindler BW theorem: K = 2pi K_boost; modular flow = boost not time translation)
- Read meta/INDEX.md → followed goal-design/ and methodology/
- Read meta-inbox: all 4 thermal-time files (meta-exploration-001, 002, 003, s002-meta-exploration-001) — all relevant
- Read goal-design/specify-computation-parameters.md — highly relevant (exact baseline comparison, code templates, physics sanity checks)
- Read goal-design/specify-failure-paths.md — relevant (Gaussian caveat = interpretation ambiguity variant)
- Read goal-design/one-task-per-exploration.md — relevant (single task; mark optional tasks skippable)
- Read goal-design/specify-rigor-level.md — relevant (request analytic coefficient)
- Read goal-design/preload-context-from-prior-work.md — relevant (paste exact formulas and code)
- Read methodology/include-trivial-control-checks.md — highly relevant (vacuum control = trivial check)
- Read methodology/structural-vs-quantitative-discrepancy.md — highly relevant (diagnose before investing)
- Read methodology/parallel-math-explorer-explorations.md — relevant (scheduling)
- Read methodology/staged-computation-goals.md — relevant (pipeline structure)
- Read methodology/math-explorer-dimensional-analysis.md — relevant (Math Explorer design notes)
- Read methodology/verify-unexpected-findings-immediately.md — relevant (if coherent state shows different pattern)

### Returned:
- Excited-state finding (Claim 3): modular flow oscillates at eps_k/(2pi) NOT omega_m; delta_disc ~ N^{+0.33}; Gaussian caveat explicitly flagged; coherent state control recommended but NOT done
- Rindler lattice setup: N=50/100/200, Williamson decomposition, BW profile within 0.1% at d<=1.5, KMS exact, entanglement spectrum sparse (2 modes = 91% entropy)
- Non-equilibrium finding: modular time = pre-quench time; structural spectral mismatch (wrong frequencies entirely); product-state identity C_global = C_local
- Modular Hamiltonian catalog: BW theorem K = 2pi K_boost for Rindler vacuum; modular flow = Lorentz boost not time translation
- s002-meta-001: Gaussian control explicitly called for; Williamson (not Peschel) for bosonic fields; fixed-frequency convergence is correct metric; specify which Poincare transformation
- meta-001: convention questions separate from computation; comparison table as deliverable
- meta-002: specify exact baseline (C_full vs C_free); analytic coefficient requested
- meta-003: trivial control checks; structural vs quantitative diagnosis
- Meta lessons: staged computation goals; preload exact formulas + code; include physics sanity checks; one task per exploration; specify exact comparison baseline

### Skipped:
- All non-thermal-time factual sections (RH, YM, SED, etc.)
- tth-normalization-and-discriminating-observable.md — normalization already resolved (tau = beta * t_modular)
- tth-deltaK-and-period-shift.md — coupled oscillator setup, not directly relevant to lattice Rindler
- tth-full-qm-vs-local-tth.md — coupled oscillator comparison, context already captured in meta notes
- meta/system-behavior/ — explorer crash/stall patterns not specifically needed
- meta/missionary/ — strategy-level lessons not needed for this query

## 2026-03-28: Query for TTH Strategy-003 Adversarial Review Design

**Requester:** Library Receptionist on behalf of Strategizer (thermal-time, strategy-003, adversarial exploration design)

**Query:** Context for adversarial review of TTH claims. Need: (1) all factual library entries about TTH, (2) meta-learning about adversarial exploration design and pitfalls, (3) cross-mission adversarial review lessons.

### Search path:
- factual/thermal-time/INDEX.md + all 7 entries (modular-hamiltonian-catalog, tth-normalization, tth-deltaK, tth-full-qm-vs-local-tth, rindler-bw-lattice-verification, nonequilibrium-tth-post-quench, excited-state-modular-flow)
- meta/methodology/adversarial-explorations-need-null-hypothesis.md
- meta/methodology/adversarial-check-between-phases.md
- meta/goal-design/adversarial-synthesis-goal-structure.md
- meta/methodology/include-trivial-control-checks.md
- meta/methodology/structural-vs-quantitative-discrepancy.md
- meta/methodology/decisive-negative-pivot.md
- meta/methodology/verify-unexpected-findings-immediately.md
- meta/methodology/investigate-why-on-discrepancies.md
- meta/methodology/split-search-from-synthesis.md
- meta/goal-design/prioritize-novelty-assessment.md
- meta/missionary/strategy-001-thermal-time-learnings.md
- meta/missionary/strategy-002-thermal-time-learnings.md
- meta/missionary/strategy-001-yang-mills-learnings.md
- meta/missionary/strategy-003-sed-learnings.md
- meta/missionary/strategy-001-compton-unruh-learnings.md
- thermal-time/meta-inbox/ (all 5 files)

### Findings delivered:
- All 7 TTH factual entries (full content)
- 6 adversarial-specific meta entries (full content)
- 5 cross-mission missionary learnings with adversarial lessons
- 5 thermal-time meta-inbox notes
- Key adversarial pitfalls identified: (1) missing null hypothesis, (2) late adversarial timing, (3) unstructured adversarial goals, (4) missing Gaussian control caveat, (5) conclusion-level vs technique-level prior art confusion

## 2026-03-28: Query for Yang-Mills Strategy-003 (B_□ inequality / staggered mode proof)

**Requester:** Library Receptionist on behalf of Yang-Mills research project

**Query:** Looking for results relevant to proving v^T [M(Q) - M(I)] v ≤ 0 for staggered modes v. Specifically: (1) adjoint rotations of fixed vectors destructively interfering in sums; (2) Schur-Weyl / Peter-Weyl bounds on sums of adjoint actions; (3) bounding ∑_□ |Ad_{G_□}(n)|² for SU(2) holonomies; (4) Jiang (2022) arXiv:2211.17195 discrete Weitzenböck; (5) lattice gauge theory Hessian / curvature bounds.

### Search path:
- Read factual/INDEX.md (too large, used offset) → yang-mills/ section highly relevant
- Read factual/yang-mills/INDEX.md — fully relevant; navigated to all B_□-related entries
- Read factual/yang-mills/weitzenbock-exact-formula.md — directly relevant (central finding)
- Read factual/yang-mills/b-square-inequality-proof-progress.md — directly relevant (proof status)
- Read factual/yang-mills/szz-lemma-4-1-hessian-slack.md — directly relevant (Hessian bound looseness)
- Read factual/yang-mills/shen-zhu-zhu-stochastic-analysis.md — relevant (Bakry-Émery / Hessian context)
- Read factual/yang-mills/adhikari-cao-technique-and-obstruction.md — relevant (proof technique landscape)
- Read factual/yang-mills/per-plaquette-inequality-false.md — relevant (dead proof route)
- Read meta/INDEX.md — navigated to methodology/INDEX.md and goal-design/INDEX.md
- Read meta/methodology/INDEX.md — relevant entries noted
- Read meta/goal-design/INDEX.md — relevant entries noted
- Meta-inbox: read 22 files, focused on s003-006, s003-007, s002-007, s002-009, s002-010 — all relevant

### Returned:
- weitzenbock-exact-formula.md — exact formula max λ[R(Q)|_P] = −W(Q)/12 ≤ 0; parallel transport decoherence mechanism; Jiang (2022) confirmed but does NOT prove sign
- b-square-inequality-proof-progress.md — comprehensive proof status: what's proved (uniform Q, flat, single-link, Q=I local max), what failed (M(Q) ≼ M(I) FALSE, geodesic concavity fails globally), remaining gap (R(Q)|_P ≼ 0 globally), proof routes
- szz-lemma-4-1-hessian-slack.md — SZZ Hessian bound 12-170× loose; plaquette destructive interference mechanism; adversarial slack ≥176×
- shen-zhu-zhu-stochastic-analysis.md — Bakry-Émery context; derivation of the 8(d-1) factor; K_S formula
- adhikari-cao-technique-and-obstruction.md — finite-group proof technique context
- per-plaquette-inequality-false.md — dead proof chain; direct spectral argument required
- meta-inbox s003-006 — Tr(M(Q)) = Tr(M(I)) for all Q (R trace-free); gradient ascent on P^T R P target; 42-config verification
- meta-inbox s003-007 — B_□ B_□^T = 4I₃; Haar average E[M(Q)] = 6I; correct target λ_max ≤ 4d (not M(Q) ≼ M(I))
- meta-inbox s002-007 — staggered mode gives H_norm = 1/12 exactly (adversarial analysis found it)
- meta/methodology/verify-unexpected-findings-immediately.md — stress-test design lesson

### Skipped:
- factual/yang-mills/balaban-uv-stability.md — RG methods, not relevant to B_□ inequality
- factual/yang-mills/lattice-numerical-evidence.md — numerical benchmarks, not directly relevant
- factual/yang-mills/proof-strategies-comparison.md — strategic overview, not proof-technique-level
- factual/yang-mills/cao-nissim-sheffield-area-law-extension.md — vertex σ-model variant; background only
- factual/yang-mills/finite-subgroup-convergence.md — convergence numerics, not relevant
- factual/yang-mills/master-loop-optimized-ceiling.md — CNS optimization, not relevant
- factual/yang-mills/szz-spectral-gap-numerical-evidence.md — MCMC gap proxy, not relevant
- All non-yang-mills factual topics — not relevant to this query
- meta-inbox files s002-001 through s002-006, s002-008 — unrelated tasks (Hessian scan setup, E006 adversarial)
- meta-inbox files s003-001 through s003-005 (not present); meta files 001-010 — task design, not proof technique

## 2026-03-28: Query for Yang-Mills-Conjecture Strategy-001 (Three Parallel Math Explorations)

**Requester:** Library Receptionist on behalf of Strategizer (yang-mills-conjecture, strategy-001, pre-launch briefing)

**Query:** Three parallel math explorations for proving Conjecture 1 (lambda_max(M(Q)) <= 4d = 16 for SU(2), d=4): (1) Maximal Tree Gauge Decomposition — fixing spanning tree to identity, studying P^T R(Q) P in reduced variables; (2) Per-Plaquette Contribution Structure — how individual plaquettes contribute to v^T R(Q) v for staggered modes, cancellation patterns; (3) SU(2)/SO(3) Representation Theory Bound — max |sum c_k R_k n|^2 for R_k in SO(3). Need: prior findings on these decompositions, corrected B_square formula, Weitzenbock exact formula, meta-learning for math explorations, per-plaquette bound status.

### Search path:
- Read factual/INDEX.md, factual/yang-mills/INDEX.md — full entry list (19 findings)
- Read meta/INDEX.md — goal-design (31 entries), methodology (31 entries), system-behavior (4 entries)
- Read b-square-inequality-proof-progress.md — CRITICAL (corrected B_square formula, all proved/failed approaches, saturation characterization, P^T R P target, Jiang reference)
- Read weitzenbock-exact-formula.md — CRITICAL (exact -1/12 coefficient, W(Q) bound, decoherence mechanism, 42/42 verification, gradient ascent stays -8 to -11)
- Read per-plaquette-inequality-false.md — CRITICAL (per-plaquette bound FALSE, global sum also FALSE at v_max, Q=I coincidence, dead proof chain)
- Read fourier-hessian-proof-q-identity.md — CRITICAL (Q=I proof via Fourier, tight bound in d=4, staggered mode structure, Lemma 5.1)
- Read hnorm-conjecture-numerical-resolution.md — CRITICAL (100+95 configs zero violations, gradient ascent plateaus at 14.1-14.4, staggered mode characterization)
- Read eigenvalue-verification-d5-departure.md — RELEVANT (d=5 departure, traceless direction vectors, eigenvalue spectrum)
- Read meta/methodology/parallel-math-explorer-explorations.md — CRITICAL (independence criteria, when to parallelize)
- Read meta/methodology/sequence-computation-approaches.md — RELEVANT (don't try two methods simultaneously)
- Read meta/methodology/check-algebra-before-multi-approach.md — RELEVANT (pre-screen algebraic inevitability)
- Read meta/methodology/staged-computation-goals.md — CRITICAL (sequential stages with verification)
- Read meta/methodology/math-explorer-dimensional-analysis.md — RELEVANT (math explorer strengths)
- Read meta/methodology/gradient-ascent-on-projected-quantity.md — CRITICAL (project onto P, not full matrix)
- Read meta/methodology/work-backward-from-constraint.md — RELEVANT (constructive framing)
- Read meta/methodology/sign-flip-diagnostic-for-critical-thresholds.md — RELEVANT
- Read meta/methodology/verify-unexpected-findings-immediately.md — RELEVANT (stress-test protocol)
- Read meta/goal-design/specify-computation-parameters.md — CRITICAL (exact params, code templates, formula disambiguation)
- Read meta/goal-design/scope-computations-to-minimum-diagnostic.md — CRITICAL (minimum diagnostic test)
- Read meta/goal-design/one-task-per-exploration.md — CRITICAL (one cognitive task, depth over breadth)
- Read meta/goal-design/verify-goal-claims-before-delegating.md — CRITICAL (lambda_max vs M(Q) <= M(I) confusion)
- Read meta/goal-design/characterize-maximizers-not-just-bounds.md — RELEVANT (ask "characterize the set of maximizers")
- Read meta/goal-design/preload-context-from-prior-work.md — CRITICAL (paste findings into goals, verify formulas first)
- Read yang-mills/meta-inbox/meta-exploration-s003-006.md — CRITICAL (trace constraint, gradient ascent on P^T R P)
- Read yang-mills/meta-inbox/meta-exploration-s003-007.md — CRITICAL (B_square B_square^T = 4I_3, Haar average, correct target)
- Checked yang-mills-conjecture/meta-inbox/ — EMPTY (new instance)

### Returned:
- Corrected B_square formula: B_square = v1 + Ad_{Q1}(v2) - Ad_{Q1 Q2 Q3^{-1}}(v3) - Ad_{U_square}(v4)
- Weitzenbock exact formula: max lambda[R(Q)|_P] = -W(Q)/12 (single-link exact, general bound), 42/42 verified, gradient ascent stays -8 to -11
- Per-plaquette bound: FALSE for Q != I (ratios up to 8383x per-plaquette, global sum 1.936x), Q=I coincidence
- SO(3) triangle inequality gives lambda_max <= 24 (too weak by 50%); Haar average E[M(Q)] = 6I (37.5% of max)
- Maximal tree gauge: mentioned as proof route #4 in b-square entry ("gauge-covariant Fourier + perturbation: work in maximal tree gauge, most links = I, corrections bounded by holonomy norms") but NOT attempted yet
- Per-plaquette contribution structure for staggered modes: staggered single-link bound PROVED (Delta = 14(cos epsilon - 1) <= 0); active/inactive plane decomposition (4 of 6 planes active for d=4); B_square B_square^T = 4I_3 per plaquette
- Saturation characterization: lambda_max = 4d iff fixed color direction n invariant under all Ad_P (pure gauge and abelian satisfy this)
- Trace conservation: Tr(M(Q)) = 12 * n_plaq for ALL Q (PROVED), implies R trace-free
- Meta lessons: (1) one task per exploration; (2) staged computation goals; (3) parallel launch OK since all three are independent; (4) specify exact computation parameters; (5) preload corrected B_square formula and Weitzenbock formula into each goal; (6) verify goal claims numerically before delegating; (7) gradient ascent on P^T R P not full matrix; (8) scope to minimum diagnostic; (9) characterize maximizers not just bounds; (10) pre-screen for algebraic inevitability

### Skipped:
- factual/yang-mills/balaban-uv-stability.md — RG program, not B_square proof
- factual/yang-mills/lattice-numerical-evidence.md — numerical benchmarks, not relevant to proof
- factual/yang-mills/proof-strategies-comparison.md — strategic overview level
- factual/yang-mills/dimock-expository-program.md — Balaban exposition, not relevant
- factual/yang-mills/stochastic-quantization-chandra-hairer.md — different approach
- factual/yang-mills/other-modern-approaches.md — alternative UV proofs
- factual/yang-mills/completed-gauge-constructions.md — completed models, not relevant
- factual/yang-mills/cao-nissim-sheffield-area-law-extension.md — CNS area law, background only
- factual/yang-mills/master-loop-optimized-ceiling.md — CNS ceiling, not relevant
- factual/yang-mills/szz-spectral-gap-numerical-evidence.md — MCMC proxy, not relevant
- factual/yang-mills/finite-subgroup-convergence.md — convergence numerics, not relevant
- factual/yang-mills/adhikari-cao-technique-and-obstruction.md — finite-group obstruction, not relevant to B_square
- factual/yang-mills/szz-lemma-4-1-hessian-slack.md — documents the slack but not proof techniques
- factual/yang-mills/chatterjee-probabilistic-program.md — program overview, not proof technique
- All non-yang-mills factual entries — not relevant
- meta-inbox files not from s003-006/s003-007 — earlier explorations, less relevant to proof techniques
- meta/methodology entries not listed above — not specifically relevant to math proof explorations
- meta/system-behavior — operational stalling patterns, not proof design
- meta/missionary — strategy-level lessons, not exploration-level

## 2026-03-31: Query for Anatomy-of-Averaged-NS-Blowup Firewall Strategy-001 Exploration 002 (Phase 1 intervention-map briefing)

**Requester:** Library Receptionist on behalf of Strategizer (anatomy-of-averaged-ns-blowup-firewall, strategy-001, pre-exploration-002)

**Query:** Pre-exploration briefing for Tao-style mechanism tracing. Need only the local-library material that helps assess firewall types for exact NS structure missing after averaging: triadic coefficient rigidity/sign constraints, same-scale/cross-scale couplings, pressure/Leray/incompressibility couplings, dynamically decisive but energetically negligible modes, and prior closures to preload so the next exploration does not drift back into estimate-level routes. Also requested meta-guidance on engineered toy mechanisms vs exact PDE structure and adversarial comparison tables.

### Search path:
- Read `factual/navier-stokes/INDEX.md`, `meta/INDEX.md`, and `meta-inbox/meta-exploration-001.md`
- Read the following factual entries in full: `exact-far-field-pressure-obstruction.md`, `beta-current-value-four-thirds.md`, `pressure-galilean-invariance.md`, `pressure-bernoulli-dominance-truncated.md`, `near-beltrami-negative-result.md`, `beltrami-pressure-analytical.md`, `near-beltrami-pressure-perturbation.md`, `beltrami-zero-vortex-stretching.md`, `vorticity-intermittency-measures.md`, `vortex-stretching-structural-slack.md`, `adversarial-minimum-vs-slack.md`, `compensated-compactness-commutator-obstruction.md`, `frequency-localized-degiorgi-lp-obstruction.md`, `chebyshev-sharpness-constant-field-extremizer.md`, `non-cz-pressure-routes-tool-independence.md`, `chebyshev-universality-and-model-pde-comparison.md`, `proposition-3-sharpness-audit.md`
- Read the following meta entries in full: `model-pde-comparison-for-mechanism-identification.md`, `distinguish-identity-from-mechanism.md`, `comparison-exploration-pattern.md`, `structural-vs-quantitative-discrepancy.md`, `distinguish-constant-from-scaling-slack.md`, `preload-context-from-prior-work.md`, `adversarial-synthesis-goal-structure.md`, `check-bypass-not-just-improve-bottleneck.md`, `quantitative-comparison-reveals-why-standard-is-standard.md`, and the `reconcile-notation-before-falsification` / `allow-analytic-extremizer-over-computation` updates in `meta/INDEX.md`

### Key source material surfaced:
- `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md` — the live far-field lead is a decomposition mismatch, not Vasseur's literal bottleneck; harmonic `P_{k1}` is already favorable, while the load-bearing obstruction is `P_{k21}`
- `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md` — exact exponent table shows the bad local non-divergence pressure term is the only term stuck at `4/3 - 5/(3q) -> 4/3`
- `factual/navier-stokes/vasseur-de-giorgi/pressure-galilean-invariance.md` — Galilean boosts cannot improve the pressure CZ bound; cross-terms vanish only because `div u = 0`
- `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` and `factual/navier-stokes/near-beltrami-negative-result.md` — exact Beltrami gives Bernoulli dominance, but the mechanism collapses for perturbed ABC flows; Leray projection is only a minor correction
- `factual/navier-stokes/vorticity-intermittency-measures.md` and `factual/navier-stokes/vortex-stretching-structural-slack.md` — dynamically decisive modes can be spatially tiny; the main obstruction can be geometric/structural rather than energetic
- `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md`, `frequency-localized-degiorgi-lp-obstruction.md`, `non-cz-pressure-routes-tool-independence.md`, `chebyshev-sharpness-constant-field-extremizer.md` — the classical estimate-level routes are already closed; constant-factor slack does not move `beta`
- `meta/methodology/model-pde-comparison-for-mechanism-identification.md` + `distinguish-identity-from-mechanism.md` — compare exact NS to model PDEs and label algebraic identities separately from physical mechanisms
- `meta/methodology/structural-vs-quantitative-discrepancy.md` + `distinguish-constant-from-scaling-slack.md` — the next exploration should test for structural missing couplings, not just tighter constants
- `meta/methodology/check-bypass-not-just-improve-bottleneck.md` — ask whether the bottleneck tool can be bypassed entirely before trying to sharpen it
- `meta/goal-design/adversarial-synthesis-goal-structure.md` + `preload-context-from-prior-work.md` — pre-load the closed routes and the surviving live loophole so the next exploration does not silently re-enter already closed estimate-level territory

### Practical preload set for the next phase:
- closed: Chebyshev improvement, compensated compactness/commutator, frequency-localized LP, non-CZ pressure variants, near-Beltrami generalization
- live: exact far-field decomposition mismatch, any genuinely `U_k`-dependent harmonic split, any exact-NS structural asymmetry not already absorbed into the closed route stack

## 2026-03-31: Query for Anatomy-of-Averaged-NS-Blowup Firewall Strategy-001 Exploration 003 (Phase 2 stress-test briefing)

**Requester:** Library Receptionist on behalf of Strategizer (anatomy-of-averaged-ns-blowup-firewall, strategy-001, pre-exploration-003)

**Query:** Need only the local-library material that helps a Phase 2 stress test of the exact-NS firewall candidate narrowed by exploration 002: exact NS may fail to admit Tao-style five-mode isolation because exact triad coefficients and spectator couplings are rigid. Requested specifics: exact Fourier/helical NS nonlinearity form for a minimal triad amplitude system, any helical-triad/Waleffe notes, Leray-projection / target-mode / conjugate-mode constraints, and meta guidance for a minimal feasibility test that tries to close the candidate sharply.

### Search path:
- Read `factual/INDEX.md`, `meta/INDEX.md`, and `factual/navier-stokes/INDEX.md`
- Read `factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/strategy-001-adversarial-synthesis.md`
- Read `factual/navier-stokes/vasseur-de-giorgi/compensated-compactness-commutator-obstruction.md`
- Read `meta/goal-design/require-mechanism-layer-maps.md`
- Read `meta/methodology/definition-extraction-gates-computation.md`
- Read `meta/goal-design/specify-failure-paths.md`
- Read `meta/methodology/verify-unexpected-findings-immediately.md`
- Read `meta/methodology/test-improvability-before-pursuing-variations.md`
- Read `meta/methodology/model-pde-comparison-for-mechanism-identification.md`
- Read `meta/methodology/structural-vs-quantitative-discrepancy.md`
- Read `meta/methodology/adversarial-check-between-phases.md`

### Key takeaways:
- No local helical-triad / Waleffe-style corpus was found
- Local exact-NS structure is documented through Leray-projected pressure splitting and Tao-style triadic geometry language
- The sharp next exploration should be a structural feasibility test, not an estimate-refinement loop
