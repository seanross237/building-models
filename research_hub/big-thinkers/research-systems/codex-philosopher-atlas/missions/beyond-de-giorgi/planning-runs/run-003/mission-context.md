# Mission Context Snapshot

Mission: beyond-de-giorgi
Planning run: run-003
Timestamp: 2026-03-31T11:56:08Z

## MISSION.md

# Mission: Beyond De Giorgi — What Structural Property Could Break the NS Regularity Barrier?

## Background

Two independent systems (Atlas and Philosopher Atlas) have conclusively established that the De Giorgi-Vasseur framework is exhausted for 3D Navier-Stokes regularity:

**Atlas findings (18 explorations, 2 strategies):**
- β = 4/3 is rigorously sharp. All four De Giorgi proof steps (energy definition → Sobolev H^1→L^6 → parabolic interpolation to L^{10/3} → Chebyshev level-set) are individually tight under NS constraints.
- Tool-independent: CZ, IBP, H^1/BMO duality, CRW commutators all give β ≤ 4/3.
- Universal formula: β = 1 + s/n. For 3D NS: s/n = 1/3, need s/n ≥ 1/2. The gap is 1/6.
- The Lamb vector L = ω × u generates the CZ-lossy pressure piece. For Beltrami flows (L = 0), CZ loss vanishes — but mechanism doesn't survive even 1% perturbation from Beltrami alignment.
- Vorticity formulation (Vasseur-Yang 2021) also gives 4/3 — the barrier is the quadratic nonlinearity, not the pressure formulation.
- Constant field u = (c,0,0) simultaneously extremizes 3 of 4 De Giorgi chain steps. One-line sharpness proof.

**Philosopher Atlas findings (4 explorations):**
- Three H^1 pressure routes tested (H^1-BMO duality, atomic decomposition, interpolation) — all failed.
- Universal obstruction: W^{1,3} wall. W^{1,2} (what Leray-Hopf gives) does not embed in BMO (needs W^{1,3}).
- Local pressure closes (σ = 3/5 > 0). Far-field pressure is the sole obstruction.
- Even with hypothetical W^{1,3} regularity, H^1-BMO is structurally WORSE than Hölder (loses U_k^{1/2} factor). Wrong tool entirely.
- Bogovskii corrector introduces 2^{2k} compound growth — eliminates all localization strategies.

**The Tao constraint (2016):**
Tao proved that any method based solely on energy identity + harmonic analysis CANNOT resolve NS regularity. He showed blowup exists for an averaged version of NS that preserves energy identity and all standard harmonic analysis structure. Therefore, the proof (if NS is regular) MUST use some specific property of the actual NS nonlinearity that the averaged version lacks.

Our β = 4/3 sharpness is a concrete quantitative instance of Tao's general obstruction.

## The Goal

**Primary question:** What specific structural property of the 3D Navier-Stokes equations — not captured by energy identity + harmonic analysis — could bypass the De Giorgi β = 4/3 barrier and provide a path toward regularity?

This is NOT "try random approaches and hope." The Tao constraint gives us a precise filter: the property must distinguish the actual NS nonlinearity from the averaged version. The SQG success gives us a concrete example of what "using the right structural property" looks like.

**What success looks like:**
- Identify 1-2 structural properties of NS that (a) are absent from Tao's averaged equations, (b) are present in SQG-like equations where regularity is proven, and (c) could plausibly feed into a non-De-Giorgi regularity proof.
- For each candidate property, assess whether it can be operationalized into a concrete mathematical attack.
- Produce an obstruction map of the non-De-Giorgi landscape: what approaches exist, which ones could exploit the identified properties, which ones have been tried and failed.

**What failure looks like:**
- All identified structural properties are either already exploited (and insufficient) or cannot be operationalized.
- Even failure is valuable: a comprehensive map of "what NS has that averaged NS doesn't, and why none of it helps" would be a publishable result.

## Key Context for the Planner

### The SQG Blueprint (most concrete lead)

SQG (surface quasi-geostrophic equation) is the closest structural analog to NS where De Giorgi regularity was proved (Caffarelli-Vasseur 2010). Atlas identified three specific structural gaps:

1. **Scalar vs vector.** SQG truncates a scalar θ. Div-free of the drift R⊥θ is preserved under scalar truncation. NS truncates a vector u — no amplitude truncation preserves div-free (topological obstruction).
2. **Linear vs quadratic coupling.** SQG drift is linear in θ. NS pressure is quadratic in u.
3. **First-order vs second-order cancellation.** SQG gains a power via commutator [(-Δ)^{1/2}, u·]θ. NS loses a power through CZ.

SQG in the Caffarelli-Silvestre extension has β = 4/3 (same as NS) at the Chebyshev level. The improvement is entirely in the drift coupling structure, not in beating Chebyshev. This means the question is NOT "how to get β > 4/3" but "how to reformulate the nonlinear interaction so that a different mechanism (commutator-type) handles it."

### Concrete Leads (untested)

1. **Harmonic structure of far-field pressure.** p_far is harmonic on Q_k with oscillation decaying exponentially (Harnack). A LOCAL H^1 norm of p_far could be much smaller than the global H^1 norm. This was identified by patlas but never tested — and it works OUTSIDE De Giorgi by exploiting harmonicity.

2. **Profile decomposition / concentration-compactness.** Kenig-Merle type approach: assume blowup, extract critical element, derive contradiction. Works for energy-critical NLS. For NS: supercriticality makes critical element extraction harder. Gallagher-Koch-Planchon (2016) have partial results.

3. **Geometric vorticity criteria.** Constantin-Fefferman (1993): regularity holds if vorticity direction is sufficiently regular. Doesn't require De Giorgi at all. Question: can NS dynamics be shown to produce the required vorticity regularity?

4. **Lorentz-space De Giorgi.** The L^{3/2,∞} weak-type estimate is available but unexploited. A De Giorgi framework using weak-type norms directly might sidestep the strong-type CZ ceiling. (This is technically still within De Giorgi, but using a qualitatively different norm structure.)

5. **Local Beltrami structure near vortex tubes.** Exact Beltrami kills CZ loss entirely (β_eff → 1.0). The mechanism requires >98% global alignment. But vortex tube cores are locally near-Beltrami. A conditional result using LOCAL Beltrami deficit (restricted to high-|ω| regions) might work — connecting to Constantin-Fefferman geometric criteria.

### What must be avoided

- Do NOT attempt further modifications to the De Giorgi iteration. β = 4/3 is sharp — this has been proven, not just observed.
- Do NOT approach this as "find a better bound for the pressure term." The barrier is universal — it's not about pressure specifically.
- Do NOT confuse H^1 structure with better L^p integrability (this error was caught by the wide funnel last mission).

### What the Tao filter requires

Any proposed approach must be checked against Tao's 2016 construction. His averaged NS preserves:
- Energy identity (||u(t)||_{L^2} ≤ ||u_0||_{L^2})
- Div-free condition
- All standard Calderón-Zygmund / Littlewood-Paley / Sobolev estimates
- The quadratic nonlinearity structure at the harmonic analysis level

But blowup CAN occur. So the proof must use something that the averaging destroys. The leading candidates for "what averaging destroys":
- The specific algebraic form of u · ∇u (not just "some quadratic term")
- Geometric properties of the vorticity field (stretching alignment, tube structure)
- The pointwise identity ω · ∇u = S · ω (strain-vorticity alignment)
- The specific structure of the pressure Hessian (∂_i∂_j p relates to u_i u_j, not just any quadratic)

## Budget

6-10 explorations total across all steps. This is a landscape + feasibility mission, not a proof construction.

## Connection to Prior Work

This is the natural successor to:
- patlas `vasseur-pressure` (H^1 pressure route → dead end)
- Atlas `vasseur-pressure` (full De Giorgi framework → exhausted)
- Atlas `navier-stokes` (proof architecture comparison: CKN/Lin/Vasseur)

All findings from those missions should be treated as established. Do not re-derive them.

## CHAIN.md

# Winning Chain - Calibrated Geometry Route with Explicit Tao Discriminator and Narrow Claim Discipline

## Central Premise

The next branch should pursue Navier-Stokes-specific vortex geometry, but only under a protocol that prevents both vague optimism and premature defeat.

The operative question is:

Can a sharply defined geometric or hybrid observable, tied to a fixed localization protocol, a fixed singular-scenario class, and a fixed kernel-level representation of `S omega . omega`, produce operational control of the full stretching mechanism in a way that

- is not already absorbed by prior geometric regularity frameworks,
- uses an NS-specific feature that is not plausibly preserved by Tao-style averaged models,
- and has at least a credible persistence story under the chosen scenario?

If not, the branch still succeeds by producing a calibrated obstruction map with tightly bounded claims.

## Verifiable Result Target

Produce one of the following:

- a mission-live geometric or hybrid route: one observable or hybrid observable that controls the full stretching mechanism in a fixed representation and comes with a plausible persistence path in a named scenario class;
- a calibrated obstruction result: a representation-fixed explanation of why a specific observable family fails, despite prior-art calibration and dynamic screening;
- or a ranked hybrid-observable shortlist that is concrete enough to justify follow-on work.

## Why This Is the Right Next Chain

This chain is the best balance of ambition and tractability.

- It is more genuinely beyond-De-Giorgi than the architecture-fixed reformulation test.
- It has a higher useful floor than the critical-element audit because it can still produce object-level deliverables even when it fails.
- It is concrete enough for this system to execute: the key objects are observables, localization rules, scenario classes, stretching representations, and propagation heuristics.

## Scope Discipline

Before substantive conclusions are allowed, the chain must fix all of the following:

- one or two concrete singular-scenario classes;
- one primary localization protocol;
- one primary kernel-level representation of `S omega . omega`;
- one bounded family of observables or hybrid observables;
- one explicit NS-versus-averaged discriminator for each promoted route;
- and one claim boundary specifying what counts as full control, partial control, or failure.

If these are not fixed, the branch downgrades to under-specified obstruction rather than drifting into suggestive prose.

## Ordered Steps

### Step 1 - Benchmark prior art and operationalize the Tao screen

- Depends on: none.
- Action: benchmark candidate mechanisms against the main existing geometry-based regularity ideas, including direction coherence, geometric depletion, and near-Beltrami-style routes.
- Action: separate candidate NS-specific ingredients into buckets:
  - transport or propagation structure,
  - exact algebraic structure,
  - multiscale coherence or concentration structure.
- Action: for each bucket, state explicitly what Tao-style averaged or toy models would preserve and what they would destroy.
- Action: forbid novelty claims that are only restatements of known static singular-integral geometry.
- Expected output: a benchmark memo listing prior-art overlap, genuinely live ingredients, and an explicit Tao discriminator for each surviving ingredient.
- Kill condition: terminate only if every candidate collapses to generic static Calderon-Zygmund geometry with no additional NS-specific dynamic content.

### Step 2 - Fix scenario class and localization before defining observables

- Depends on: Step 1.
- Action: choose one or two concrete singular-scenario classes, such as filament concentration or sheet/pancake concentration.
- Action: fix the localization protocol:
  - intensity threshold,
  - spatial scale,
  - time window,
  - and whether localization is Eulerian, Lagrangian, or tube-adapted.
- Action: define observables only after those choices are fixed.
- Action: allow both single observables and bounded hybrid observables, for example:
  - local Beltrami deficit,
  - vorticity-direction regularity,
  - tube-family coherence,
  - Beltrami deficit plus concentration,
  - Beltrami deficit plus anisotropy,
  - direction coherence plus tube persistence.
- Expected output: an observable table recording localization data, scaling, target scenario, intended leverage point, and Tao discriminator.
- Kill condition: eliminate a candidate only if it is unstable under reasonable localization choices or gains its strength only from hidden normalization choices.

### Step 3 - Run the dynamic plausibility screen early

- Depends on: Step 2.
- Action: for each candidate, ask immediately what is transported, approximately propagated, or rapidly lost under the chosen localization.
- Action: record the best available transport identity, diffusion loss, commutator burden, and localization-evolution cost.
- Action: classify candidates as:
  - dynamically plausible,
  - informative but dynamically weak,
  - or static-only.
- Action: do not require a final transport theorem at this stage, but do require a credible persistence story before major investment.
- Expected output: a ranked shortlist with explicit dynamic scores and first failure modes.
- Kill condition: terminate a route only if it has no credible propagation mechanism even heuristically and no scenario-based reason to expect persistence.

### Step 4 - Fix one kernel-level stretching representation and one control target

- Depends on: Step 3.
- Action: choose one explicit Biot-Savart-level representation for `S omega . omega`.
- Action: choose one primary localization-based split, for example near-field versus exterior relative to the intense region.
- Action: define every remainder term inside that fixed representation.
- Action: specify in advance what counts as success:
  - control of near-field, exterior, and interaction terms in the fixed representation,
  - or a clearly delimited conditional reduction that still bears on the full stretching mechanism.
- Action: where feasible, cross-check against one secondary reasonable decomposition to detect artifacts.
- Expected output: a representation memo with formula, split, glossary of controlled terms, and explicit success/failure criteria.
- Kill condition: do not declare failure from a remainder term unless the obstruction is stable across reasonable reformulations of the same fixed target.

### Step 5 - Test whether the observable controls the full stretching mechanism

- Depends on: Step 4.
- Action: evaluate each shortlisted observable or hybrid observable against:
  - the near-field contribution,
  - the exterior contribution,
  - and interaction terms introduced by localization.
- Action: distinguish three outcomes:
  - full operational control,
  - partial control of only a portion,
  - or descriptive value without control.
- Action: keep the representation fixed while making this judgment.
- Expected output: a lemma sheet or obstruction memo stating exactly what is controlled, what remains free, and whether the surviving leverage is genuinely NS-specific.
- Kill condition: terminate a positive route if it improves only a descriptive local fragment while leaving the scale-critical stretching mechanism uncontrolled in the fixed representation.

### Step 6 - Promote only routes that survive both stretching and persistence

- Depends on: Step 5.
- Action: promote a route to a serious final candidate only if it has:
  - a sharply defined observable or hybrid observable,
  - a scale-credible hypothesis,
  - control of the full stretching mechanism in the fixed representation,
  - an explicit NS-specific ingredient not plausibly preserved by Tao-style averaging,
  - and a plausible persistence story in the chosen scenario class.
- Action: otherwise classify the outcome into one of:
  - conditional proposition,
  - calibrated obstruction result,
  - hybrid-observable follow-up target.
- Expected output: a mission-ready note that says whether the geometry is operational, merely descriptive, or promising only in hybrid form.
- Kill condition: if the claim extends beyond the observable family, scenario class, or stretching representation actually tested, narrow it until fully earned.

### Step 7 - Close with an explicit obstruction taxonomy if no route survives

- Depends on: Step 6, or directly on Step 5 if every route dies there.
- Action: classify failure precisely rather than generically. Use categories such as:
  - prior-art collapse,
  - Tao-robust rather than NS-specific,
  - localization instability,
  - dynamic non-persistence,
  - kernel-level remainder obstruction,
  - only partial stretching control,
  - or dependence on special alignment with no robust remainder.
- Action: state which failures are representation-stable and which are only provisional.
- Expected output: a bounded obstruction map that can guide later chains rather than merely ending this one.
- Kill condition: if the final memo says more than the audited observable family supports, narrow it.

## Promotion Standard

This chain does not win by elegant geometric language alone. It wins only if it reaches a fixed-representation control statement with a credible persistence story and an explicit NS-specific discriminator.

Absent that, the correct success case is a trustworthy obstruction map.

## Probability Assessment

- Probability this chain yields a presentable result: **0.69**
- Most likely strong outcome: a calibrated obstruction result or a sharp hybrid-observable shortlist.
- Less likely but higher-upside outcome: one operational geometric or hybrid control route on the full stretching mechanism in a fixed scenario class.

## CHAIN-HISTORY.md


## run-001 — 2026-03-31T05:43:20Z

# Final Decision Memo - beyond-de-giorgi / run-001

## Decision

The winning chain is **Refined Chain 01 - Harmonic Tail Obstruction Test with Early Tao Gate**.

This is the best next execution choice because it has the strongest combination of:

- presentable-result probability
- useful failure payload
- short-path fit with the current system's validated pressure context
- ability to close a live loophole without pretending that loophole is the whole beyond-De-Giorgi strategy

I am not choosing it because it has the highest proof ceiling. It does not. I am choosing it because it is the most likely next branch to produce a clean, defensible result that improves the mission map rather than merely expanding it.

## Why Chain 01 Wins

### 1. Best chance of a genuinely presentable result

Chain 01 has the clearest near-term endpoint: either it finds an NS-specific way to shrink the far-field pressure coefficient, or it produces a sharp obstruction memo showing that local harmonic-tail structure cannot do that in a Tao-relevant way. That is a much cleaner finish line than the likely outcomes of Chains 02 or 03.

The judgment on Chain 01 is also the strongest numerically and structurally. Its likely negative endpoint is already well-shaped into something publishable inside the project: a falsification of the last pressure-side loophole left by the earlier pressure mission.

### 2. Strongest useful floor on failure

Failure in Chain 01 is highly informative. If the explicit remote-shell model shows that the surviving pressure quantity stays comparable to shell energy, then one more plausible exit from the De Giorgi bottleneck is closed with a precise reason. That immediately sharpens the research landscape.

By contrast:

- Chain 02 can fail in a more diffuse way, because "no useful gain from these rewrites" is informative but easier to under-specify or over-claim.
- Chain 03 can fail descriptively unless it cleanly isolates where local geometry loses control of the full stretching term.

### 3. Best execution fit for this system

This system already has concrete pressure-side context, including the named `vasseur-pressure` obstruction and the surviving harmonic-tail loophole. Chain 01 is therefore the branch with the smallest startup cost and the least speculative setup.

Its refined form is also operationally disciplined:

- early Tao gate
- explicit surviving mode analysis
- explicit remote-shell falsification
- narrow candidate list
- quantitative success criterion tied to coefficient shrinkage

That is the strongest execution design among the three finalists.

### 4. Adequate novelty ceiling, despite not being the highest-upside branch

Chain 02 has the highest novelty ceiling in the abstract, and Chain 03 has the most NS-specific geometric flavor. But both carry a larger risk of spending time proving that attractive language does not cash out at the estimate level.

Chain 01's novelty ceiling is lower, but not trivial. If an NS-specific harmonic-tail mechanism survives both the shell model and the Tao screen, that would still be a real structural find. More importantly, the floor is much stronger, and the decision criteria explicitly reward that.

## Why the Other Finalists Lose

### Chain 02 - Estimate-First Obstruction Hunt for NS Reformulation Cancellations

This is the best reserve branch, not the best next branch.

It deserves credit for the highest upside and for being tightly aligned with the mission's SQG blueprint. But even after refinement it still has a serious execution risk: algebraic reformulations are very good at looking nontrivial before they are tested against the actual localized estimate. The branch is improved by its estimate-first rewrite screen, yet it still has a materially weaker floor than Chain 01.

If Chain 01 closes negatively, Chain 02 should likely be next.

### Chain 03 - Obstruction-First Geometry Route

This remains the strongest geometry-first candidate, but it is not the right immediate winner.

Its core problem is that the missing bridge is also the main difficulty: local near-Beltrami or alignment observables do not obviously control the full stretching quantity, especially the nonlocal remainder. That makes the branch valuable, but comparatively fragile. Its best negative result is useful, though still harder to secure cleanly than Chain 01's shell-based obstruction.

## Elements Borrowed from the Losing Chains

The winning chain should absorb two useful refinements from the losing branches:

- From Chain 02: define the exact bad term and the acceptable notion of "gain" before testing any candidate quantity. Identity-level prettification does not count.
- From Chain 03: treat the nonlocal or exterior contribution as the main adversary. Any candidate that only improves a local-looking piece while leaving the decisive remote contribution untouched should be killed immediately.

These do not change the winner. They make the winner tighter.

## Final Execution Posture

The correct next move is not "search for a better pressure estimate." It is:

1. reconstruct the precise surviving far-field pressure pairing,
2. run the Tao gate immediately,
3. attack the loophole with an explicit remote-shell falsification model,
4. allow continuation only if a candidate quantity can reduce the actual coefficient rather than repackage `O(E_0)`,
5. write the strongest earned conclusion, with a sharp negative memo counted as success.

That is the chain with the best expected value for the next run.

### Winning Chain

# Chain 01 - Harmonic Tail Obstruction Test with Early Tao Gate

## Central Premise

Do not ask whether harmonicity makes the far-field pressure tail smoother. That is already known. Ask the narrower and decisive question:

Can any NS-specific structure make the surviving far-field pressure pairing small enough to reduce the bad coefficient

`C_far ~ ||u||_{L^2}^2 / r_k^3`

from admissible NS data, in a way that Tao's averaged model would not preserve?

If not, the branch should end quickly with a sharp obstruction memo.

## Verifiable Result Target

Either:

- a concrete NS-specific mechanism that turns local information about the harmonic pressure tail into quantitative shrinkage of the actual bad coefficient, or into summable decay strictly stronger than fixed `O(E_0)` control; or
- a rigorous negative result showing that, after quotienting out pressure modes already killed by the test structure, local harmonic-tail information cannot improve the coefficient in a Tao-relevant way.

## Why This Is the Right Next Branch

The prior pressure mission left the harmonic-tail loophole explicitly open. This chain treats that loophole as a falsifiable cleanup target with a strong presentable downside, not as an open-ended search for nicer elliptic estimates.

## Non-Negotiable Gatekeeping Standard

No candidate quantity is allowed to survive unless all of the following hold:

- it acts on the actual surviving pressure pairing after removing constant, affine, or other modes already annihilated by the test structure;
- it targets the coefficient itself, not just a smoother restatement of fixed `O(E_0)` control;
- it uses an NS-specific ingredient beyond generic harmonic interior regularity;
- it survives an estimate-level test rather than only an identity-level or representation-level rewrite;
- it addresses the decisive nonlocal or exterior contribution rather than only a local-looking piece.

If these conditions fail, the chain immediately downgrades to the negative-result track.

## Ordered Steps

### Step 1 - Reconstruct the exact obstruction and front-load the Tao gate

- Depends on: none.
- Action: rebuild the precise far-field pressure pairing from `vasseur-pressure`, identify which harmonic modes survive the test structure, isolate the exact quantity whose smallness would matter, and state in advance what would count as a genuine gain on the bad term.
- Action: name the candidate NS-specific ingredient if one exists, and separate it from generic harmonic facts that Tao's averaged model should preserve.
- Expected output: a formula sheet containing `I_p^far`, the role of `C_far`, the surviving modes, the exact gain target, and a one-page Tao-gate memo.
- Kill condition: if no plausible NS-specific ingredient can be named, or if the claimed gain is not a gain on the actual coefficient, move directly to the negative-result track.

### Step 2 - Run an explicit remote-shell falsification model

- Depends on: Step 1.
- Action: choose a remote shell source with admissible energy, compute the induced harmonic field or harmonic polynomial on the inner cylinder, and test the exact surviving quantity isolated in Step 1.
- Action: treat the exterior contribution as the main adversary. Do not count control of a local subpiece as progress if the shell model keeps the full pairing at `O(E_0)`.
- Expected output: a countermodel memo showing whether the relevant local quantity remains comparable to shell energy and whether any supposed gain survives against the nonlocal source.
- Kill condition: if the shell model forces the relevant quantity to stay at fixed-size control, close the positive route unless a clearly NS-specific cancellation defeats that model.

### Step 3 - Test only a short, pressure-relevant candidate list at the estimate level

- Depends on: Step 2 surviving.
- Action: examine only tightly justified candidates such as oscillation after quotienting out killed modes, derivative decay, harmonic polynomial remainder, or another explicitly motivated quantity acting on the same pairing.
- Action: do not run a broad norm survey. Do not use positivity/Harnack heuristics for a sign-changing object. Do not accept nicer representation formulas as progress unless they improve the operative estimate.
- Expected output: an estimate table recording exactly where annular or local data enters, whether any candidate reduces the bad coefficient, and whether any effect is real or cosmetic.
- Kill condition: if every candidate simply propagates boundary or shell size into another fixed `O(E_0)` bound, stop and write the obstruction memo.

### Step 4 - Convert any surviving gain into a non-recursive quantitative criterion

- Depends on: Step 3.
- Action: if one candidate survives, translate it into a criterion that directly shrinks `C_far` or yields summable decay from admissible NS data, without rebuilding the exhausted De Giorgi recursion under new names.
- Action: require the gain to survive localization and to act on the full far-field contribution, not merely on a partial or mode-restricted surrogate.
- Expected output: a conditional proposition with explicit quantitative gain, assumptions, and proof skeleton.
- Kill condition: if the gain does not reduce the bad coefficient, or only feeds back into the same missing `W^{1,3}`-type input, threshold recursion, or other already-failed architecture, record structural failure.

### Step 5 - Close with the strongest calibrated claim

- Depends on: Step 4, or directly on an earlier kill.
- Action: test whether any surviving mechanism truly uses the NS-specific ingredient named in Step 1 rather than generic elliptic harmonicity.
- Action: make the final claim no broader than the tested family of quantities and models.
- Expected output: one of two endpoints:
  - a narrowly specified NS-specific attack path on the far-field coefficient; or
  - a polished negative result stating that the harmonic-tail loophole is Tao-compatible and does not provide a beyond-De-Giorgi escape.
- Kill condition: if the mechanism survives unchanged in Tao's averaged setting, or if the final claim exceeds what the shell model and estimate-level tests support, close the chain negatively and narrow the statement until it is fully earned.

## Outcome Standard

A sharp obstruction memo counts as a successful result. This branch should not be prolonged in search of prettier harmonic estimates once the coefficient-shrinkage route has failed.


## run-002 — 2026-03-31T08:40:51Z

# Final Decision Memo - beyond-de-giorgi / run-002

## Decision

The winning chain is **Refined Chain 02**, promoted in merged form as:

**Calibrated Geometry Route with Explicit Tao Discriminator and Narrow Claim Discipline**

This is the best next chain to execute.

## Why Chain 02 Wins

Chain 02 has the best overall balance across the decision criteria.

- **Highest presentable-result quality:** its failure mode is strong without being trivially pre-written. If it does not produce a live mechanism, it can still produce a calibrated obstruction result, a trustworthy hybrid-observable shortlist, or a clean statement of where geometric leverage breaks.
- **Best novelty-to-floor ratio:** it stays genuinely beyond the estimate-first cleanup logic of Chain 01, but it is less speculative and less globally burdened than Chain 03.
- **Best execution fit for this system:** it can be driven by explicit objects, scenario classes, localization protocols, and kernel-level representations. That is a better match for disciplined stepwise analysis than the heavier global compactness-and-rigidity audit in Chain 03.
- **Strong useful floor on failure:** even a negative outcome can leave behind operational artifacts that matter for later work: an obstruction taxonomy, a representation-fixed failure analysis, and a hybrid observable ranking.

## Why Not Chain 01

Chain 01 is the safest bounded obstruction branch, but it is too narrow to be the best next move. Its most credible endpoint is a cleanup memo showing that exact reformulations do not beat a fixed inherited bottleneck. That is useful, but it is less aligned with the mission's "beyond De Giorgi" ambition and has a lower novelty ceiling than the geometry route.

Chain 01 is therefore better treated as a support discipline, not as the main winner.

## Why Not Chain 03

Chain 03 has a serious upside tail, but its likely positive path is still weakly credible relative to the system burden it imposes. The refined version improved the sequencing, yet the branch remains dominated by foundational compactness, coercive-backbone, and rigidity difficulties. It is more likely to produce an obstruction map than an actionable program, and its execution demands are less concrete than Chain 02's.

Chain 03 remains valuable as a later audit branch, not as the immediate next execution chain.

## Elements Merged Into the Winner

The winning chain should inherit three disciplines from the losing chains:

- **From Chain 01:** explicit Tao-vs-NS discrimination, early fixation of the exact stretching target and localization protocol, and narrow claim discipline for negative conclusions.
- **From Chain 03:** explicit obstruction taxonomy, so failure is classified precisely rather than collapsed into a generic "geometry did not work" memo.
- **From both:** terminal claims must not outrun the exact observable family, scenario class, and representation actually audited.

## Canonical Choice

Execute the merged Chain 02 as the canonical next chain.

Its role is:

1. benchmark geometric ingredients against prior art and Tao-style robustness,
2. define observables only after fixing scenario class and localization,
3. screen dynamic plausibility early,
4. test control of the full stretching mechanism in one fixed kernel-level representation,
5. and close with either a live hybrid/geometric route or a sharply bounded obstruction map.

## Expected Best Outcome

The most realistic strong outcome is not an immediate theorem. It is a mission-worthy intermediate product:

- either one sharply defined geometric or hybrid observable that genuinely controls the full stretching mechanism in a fixed scenario class with a plausible persistence story,
- or a trustworthy obstruction map showing exactly why the main geometry candidates fail.

That is the best combination of floor, ceiling, and execution realism in this run.

### Winning Chain

# Winning Chain - Calibrated Geometry Route with Explicit Tao Discriminator and Narrow Claim Discipline

## Central Premise

The next branch should pursue Navier-Stokes-specific vortex geometry, but only under a protocol that prevents both vague optimism and premature defeat.

The operative question is:

Can a sharply defined geometric or hybrid observable, tied to a fixed localization protocol, a fixed singular-scenario class, and a fixed kernel-level representation of `S omega . omega`, produce operational control of the full stretching mechanism in a way that

- is not already absorbed by prior geometric regularity frameworks,
- uses an NS-specific feature that is not plausibly preserved by Tao-style averaged models,
- and has at least a credible persistence story under the chosen scenario?

If not, the branch still succeeds by producing a calibrated obstruction map with tightly bounded claims.

## Verifiable Result Target

Produce one of the following:

- a mission-live geometric or hybrid route: one observable or hybrid observable that controls the full stretching mechanism in a fixed representation and comes with a plausible persistence path in a named scenario class;
- a calibrated obstruction result: a representation-fixed explanation of why a specific observable family fails, despite prior-art calibration and dynamic screening;
- or a ranked hybrid-observable shortlist that is concrete enough to justify follow-on work.

## Why This Is the Right Next Chain

This chain is the best balance of ambition and tractability.

- It is more genuinely beyond-De-Giorgi than the architecture-fixed reformulation test.
- It has a higher useful floor than the critical-element audit because it can still produce object-level deliverables even when it fails.
- It is concrete enough for this system to execute: the key objects are observables, localization rules, scenario classes, stretching representations, and propagation heuristics.

## Scope Discipline

Before substantive conclusions are allowed, the chain must fix all of the following:

- one or two concrete singular-scenario classes;
- one primary localization protocol;
- one primary kernel-level representation of `S omega . omega`;
- one bounded family of observables or hybrid observables;
- one explicit NS-versus-averaged discriminator for each promoted route;
- and one claim boundary specifying what counts as full control, partial control, or failure.

If these are not fixed, the branch downgrades to under-specified obstruction rather than drifting into suggestive prose.

## Ordered Steps

### Step 1 - Benchmark prior art and operationalize the Tao screen

- Depends on: none.
- Action: benchmark candidate mechanisms against the main existing geometry-based regularity ideas, including direction coherence, geometric depletion, and near-Beltrami-style routes.
- Action: separate candidate NS-specific ingredients into buckets:
  - transport or propagation structure,
  - exact algebraic structure,
  - multiscale coherence or concentration structure.
- Action: for each bucket, state explicitly what Tao-style averaged or toy models would preserve and what they would destroy.
- Action: forbid novelty claims that are only restatements of known static singular-integral geometry.
- Expected output: a benchmark memo listing prior-art overlap, genuinely live ingredients, and an explicit Tao discriminator for each surviving ingredient.
- Kill condition: terminate only if every candidate collapses to generic static Calderon-Zygmund geometry with no additional NS-specific dynamic content.

### Step 2 - Fix scenario class and localization before defining observables

- Depends on: Step 1.
- Action: choose one or two concrete singular-scenario classes, such as filament concentration or sheet/pancake concentration.
- Action: fix the localization protocol:
  - intensity threshold,
  - spatial scale,
  - time window,
  - and whether localization is Eulerian, Lagrangian, or tube-adapted.
- Action: define observables only after those choices are fixed.
- Action: allow both single observables and bounded hybrid observables, for example:
  - local Beltrami deficit,
  - vorticity-direction regularity,
  - tube-family coherence,
  - Beltrami deficit plus concentration,
  - Beltrami deficit plus anisotropy,
  - direction coherence plus tube persistence.
- Expected output: an observable table recording localization data, scaling, target scenario, intended leverage point, and Tao discriminator.
- Kill condition: eliminate a candidate only if it is unstable under reasonable localization choices or gains its strength only from hidden normalization choices.

### Step 3 - Run the dynamic plausibility screen early

- Depends on: Step 2.
- Action: for each candidate, ask immediately what is transported, approximately propagated, or rapidly lost under the chosen localization.
- Action: record the best available transport identity, diffusion loss, commutator burden, and localization-evolution cost.
- Action: classify candidates as:
  - dynamically plausible,
  - informative but dynamically weak,
  - or static-only.
- Action: do not require a final transport theorem at this stage, but do require a credible persistence story before major investment.
- Expected output: a ranked shortlist with explicit dynamic scores and first failure modes.
- Kill condition: terminate a route only if it has no credible propagation mechanism even heuristically and no scenario-based reason to expect persistence.

### Step 4 - Fix one kernel-level stretching representation and one control target

- Depends on: Step 3.
- Action: choose one explicit Biot-Savart-level representation for `S omega . omega`.
- Action: choose one primary localization-based split, for example near-field versus exterior relative to the intense region.
- Action: define every remainder term inside that fixed representation.
- Action: specify in advance what counts as success:
  - control of near-field, exterior, and interaction terms in the fixed representation,
  - or a clearly delimited conditional reduction that still bears on the full stretching mechanism.
- Action: where feasible, cross-check against one secondary reasonable decomposition to detect artifacts.
- Expected output: a representation memo with formula, split, glossary of controlled terms, and explicit success/failure criteria.
- Kill condition: do not declare failure from a remainder term unless the obstruction is stable across reasonable reformulations of the same fixed target.

### Step 5 - Test whether the observable controls the full stretching mechanism

- Depends on: Step 4.
- Action: evaluate each shortlisted observable or hybrid observable against:
  - the near-field contribution,
  - the exterior contribution,
  - and interaction terms introduced by localization.
- Action: distinguish three outcomes:
  - full operational control,
  - partial control of only a portion,
  - or descriptive value without control.
- Action: keep the representation fixed while making this judgment.
- Expected output: a lemma sheet or obstruction memo stating exactly what is controlled, what remains free, and whether the surviving leverage is genuinely NS-specific.
- Kill condition: terminate a positive route if it improves only a descriptive local fragment while leaving the scale-critical stretching mechanism uncontrolled in the fixed representation.

### Step 6 - Promote only routes that survive both stretching and persistence

- Depends on: Step 5.
- Action: promote a route to a serious final candidate only if it has:
  - a sharply defined observable or hybrid observable,
  - a scale-credible hypothesis,
  - control of the full stretching mechanism in the fixed representation,
  - an explicit NS-specific ingredient not plausibly preserved by Tao-style averaging,
  - and a plausible persistence story in the chosen scenario class.
- Action: otherwise classify the outcome into one of:
  - conditional proposition,
  - calibrated obstruction result,
  - hybrid-observable follow-up target.
- Expected output: a mission-ready note that says whether the geometry is operational, merely descriptive, or promising only in hybrid form.
- Kill condition: if the claim extends beyond the observable family, scenario class, or stretching representation actually tested, narrow it until fully earned.

### Step 7 - Close with an explicit obstruction taxonomy if no route survives

- Depends on: Step 6, or directly on Step 5 if every route dies there.
- Action: classify failure precisely rather than generically. Use categories such as:
  - prior-art collapse,
  - Tao-robust rather than NS-specific,
  - localization instability,
  - dynamic non-persistence,
  - kernel-level remainder obstruction,
  - only partial stretching control,
  - or dependence on special alignment with no robust remainder.
- Action: state which failures are representation-stable and which are only provisional.
- Expected output: a bounded obstruction map that can guide later chains rather than merely ending this one.
- Kill condition: if the final memo says more than the audited observable family supports, narrow it.

## Promotion Standard

This chain does not win by elegant geometric language alone. It wins only if it reaches a fixed-representation control statement with a credible persistence story and an explicit NS-specific discriminator.

Absent that, the correct success case is a trustworthy obstruction map.

## Probability Assessment

- Probability this chain yields a presentable result: **0.69**
- Most likely strong outcome: a calibrated obstruction result or a sharp hybrid-observable shortlist.
- Less likely but higher-upside outcome: one operational geometric or hybrid control route on the full stretching mechanism in a fixed scenario class.


## Latest Step Results

# Step 4 Results — Dynamic Plausibility Screen And Branch-Kill Memo

## Completion Status

Step 4 is complete.

- Kill condition fired: **yes**
- Branch status: **dynamic screen failed on the fixed Step-3 package**
- Honest summary:
  on the inherited Eulerian parabolic package, no candidate cleared the
  `dynamically plausible` bar. The primary hybrid
  `direction coherence + tube persistence` remains the best dynamic idea, but
  only as `informative but dynamically weak`. Every comparator or fragility
  screen is likewise dynamically weak or static-only. Advancing to kernel-level
  `S omega . omega` representation work on this package would be blind momentum
  rather than an earned next step.

## Source Basis

Primary step outputs:

- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-002/REPORT-SUMMARY.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-004/explorations/exploration-003/REPORT-SUMMARY.md`

Main underlying local sources:

- `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
- `missions/beyond-de-giorgi/steps/step-004/REASONING.md`
- `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-003/HISTORY-OF-REPORT-SUMMARIES.md`
- `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
- `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
- `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
- `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`

## Dynamic-Screen Memo

### Fixed inherited Step-3 package

- [VERIFIED] Primary scenario:
  `filament or tube concentration`
- [VERIFIED] Comparator scenario:
  `sheet or pancake concentration`
- [VERIFIED] Localization:
  Eulerian parabolic package on
  `B_r(x_*) x [t_* - r^2, t_*]`
- [VERIFIED] Threshold:
  `|omega| >= r^{-2}`
- [VERIFIED] Candidate set entering the dynamic screen:
  - primary:
    `direction coherence + tube persistence`
  - secondary comparators:
    `vorticity-direction coherence`,
    `tube coherence / persistence`
  - fragility screens only:
    `local Beltrami / alignment`,
    `Beltrami deficit + concentration`,
    `Beltrami deficit + anisotropy`

### Why dynamic plausibility is the right gate now

- [VERIFIED] The active chain requires the branch to ask what is transported,
  approximately propagated, or rapidly lost before fixing any kernel-level
  representation of `S omega . omega`. Source:
  `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] Step 3 already did the honest static narrowing:
  it fixed the scenario, localization, and bounded candidate list without
  reintroducing tube-adapted coordinates. Source:
  `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- [INFERRED] So the only remaining question before representation work is
  persistence credibility:
  does any candidate retain a believable dynamic mechanism once diffusion,
  moving superlevel sets, and Eulerian localization are named explicitly?
- [INFERRED] If not, then the chain should stop here. Otherwise Step 4 would
  merely choose a decomposition for a route that already failed its persistence
  screen.

## Candidate-By-Candidate Transport Table

| Candidate | Best transport identity or propagation heuristic | Main diffusion loss | Main commutator / localization-evolution burden | Depends most on | Tao discriminator dynamic status | First obvious dynamic failure mode | Final rating |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction coherence + tube persistence` | [INFERRED] vorticity transport-diffusion-stretching heuristic plus the idea that an intense filamentary region might be advected and stretched while its direction field stays coherent enough for later `xi . S xi` control. Sources: `MISSION.md`, `CHAIN.md`, `direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md` | [INFERRED] order-one diffusion on scale `r` over time `r^2`; thresholded tube boundary can smear/reconnect, and the direction part inherits derivative-heavy diffusion terms | [INFERRED] matching coherent intense components across a moving Eulerian superlevel set without tube refitting; any smooth localization also carries `1/r` and `1/r^2` cutoff costs. Sources: `step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`, `ckn-1982-proof-architecture.md`, `vasseur-2007-proof-architecture.md` | [INFERRED] a hidden matching principle for the evolving intense set and a stronger direction-propagation principle than the fixed package contains | [INFERRED] still live conceptually, but weak in practice: joint persistence of direction coherence on a coherent tube family is Tao-sensitive, yet no estimate-level propagation mechanism is supplied | [INFERRED] route becomes viable only after hidden tube adaptation, threshold/window retuning, or stronger `nabla xi`-type control | `informative but dynamically weak` |
| `vorticity-direction coherence` | [INFERRED] normalized-vorticity direction heuristic: if `xi = omega / |omega|` stays coherent on `E_r(t)`, then `xi . S xi` remains the relevant stretching-facing quantity. Sources: `MISSION.md`, `step-003/RESULTS.md` | [INFERRED] diffusion of `xi` introduces derivative losses and pushes the route toward stronger `nabla xi` control | [INFERRED] measuring the same coherence notion on the moving Eulerian intense set without quietly upgrading to a stronger prior-art direction criterion | [INFERRED] maintaining direction coherence on `E_r(t)` without importing the stronger regularity package already associated with known criteria | [VERIFIED/INFERRED] weak; as a standalone route it mostly collapses into prior-art direction regularity unless a new localized persistence bridge is supplied. Source: `direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md` | [INFERRED] hidden import of `nabla xi`-type control stronger than the Step-3 package | `informative but dynamically weak` |
| `tube coherence / persistence` | [INFERRED] vortex-structure heuristic: intense filamentary components might persist approximately because vorticity is advected and stretched | [INFERRED] tube-boundary erosion, splitting, or merging over the `r^2` window | [INFERRED] matching connected components of the thresholded Eulerian intense set across time without tube-adapted relocalization | [INFERRED] threshold and connectedness rules for the evolving intense set | [VERIFIED/INFERRED] live only if there is genuine time/scale persistence; one-time tube imagery is static. Sources: `tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`, `step-002/explorations/exploration-002/REPORT.md` | [INFERRED] descriptive slippage into tube language or hidden tube-adapted tracking | `informative but dynamically weak` |
| `local Beltrami / alignment` | [INFERRED] no credible full-stretching transport story; at best a vague hope that local alignment might persist on a core | [INFERRED] local alignment is quickly degraded without stronger derivative control on both `u` and `omega` | [INFERRED] thresholding can isolate a favorable aligned core while leaving exterior strain untouched | [VERIFIED/INFERRED] local alignment on the intense set, but without a bridge from `u x omega`-style depletion to full `S omega . omega`. Sources: `MISSION.md`, `standalone-beltrami-alignment-collapses-to-a-fragility-screen.md` | [VERIFIED] collapsed; static alignment language is Tao-robust and aimed at the wrong quantity | [INFERRED] only local/self-induced depletion improves while the decisive exterior strain remains free | `static-only` |
| `Beltrami deficit + concentration` | [INFERRED] concentrated aligned core might persist long enough to make the exterior field relatively less important | [INFERRED] diffusion weakens both alignment and concentration over the same `r^2` window | [VERIFIED/INFERRED] concentration strength is hostage to the thresholded intense set; threshold choice can manufacture the favorable core. Sources: `step-003/RESULTS.md`, `step-003/explorations/exploration-003/REPORT.md` | [INFERRED] isolating an unusually aligned intense core by the fixed threshold | [INFERRED] weak at best; concentrated aligned cores can survive as descriptive pictures unless they are linked dynamically to a smaller full-stretching term | [INFERRED] threshold tuning manufactures the signal while exterior/nonlocal strain remains scale-critical | `informative but dynamically weak` |
| `Beltrami deficit + anisotropy` | [INFERRED] anisotropic aligned core might persist and later improve a kernel angular factor or exterior remainder | [INFERRED] diffusion relaxes anisotropy and blurs the shape information needed to distinguish a filamentary core | [VERIFIED/INFERRED] anisotropy can be silently imported by geometry fitting, especially via a preferred tube axis. Sources: `step-003/RESULTS.md`, `step-003/explorations/exploration-003/REPORT.md` | [INFERRED] reading anisotropy from the neutral Eulerian package without later tube fitting | [INFERRED] weak; static anisotropy is descriptive unless paired with a real propagation law | [INFERRED] route becomes plausible only after preferred-axis fitting or stronger geometric adaptation than the Step-3 package allows | `informative but dynamically weak` |

## Dynamic Ranking And Kill Memo

### Ranking

- [INFERRED] `direction coherence + tube persistence`:
  `informative but dynamically weak`
- [INFERRED] `vorticity-direction coherence`:
  `informative but dynamically weak`
- [INFERRED] `tube coherence / persistence`:
  `informative but dynamically weak`
- [INFERRED] `local Beltrami / alignment`:
  `static-only`
- [INFERRED] `Beltrami deficit + concentration`:
  `informative but dynamically weak`
- [INFERRED] `Beltrami deficit + anisotropy`:
  `informative but dynamically weak`

### Kill memo

- [INFERRED] No candidate is `dynamically plausible` on the audited package.
- [INFERRED] The primary hybrid remains the best route descriptively and
  conceptually, but not strongly enough to justify Step 4 representation work.
- [INFERRED] The step's early kill condition is met in two convergent ways:
  - every surviving candidate is dynamically weak or static-only, so further
    work would be blind momentum;
  - the only visible rescues for the primary hybrid are the forbidden ones:
    tube-adapted relocalization, tuned threshold/window choices, or stronger
    derivative control than the bounded Step-3 package contains.
- [INFERRED] Therefore the current geometry branch should be invalidated or
  replanned rather than allowed to drift into kernel-level analysis anyway.

## Step-4 Readiness Recommendation

- [INFERRED] No route survives honestly enough to justify fixing a primary
  kernel-level representation of `S omega . omega` on the present package.
- [INFERRED] The current chain should stop here and hand the controller a
  calibrated obstruction result:
  the geometry branch fails at the dynamic screen because neutral Eulerian
  localization plus a diffusion-scale time window makes every candidate either
  too weak dynamically, too dependent on hidden normalization, or too close to
  static prior-art geometry.
- [INFERRED] If later work wants to revisit geometry, it should do so only by
  openly changing the package and admitting that the current Step-3 audit did
  not earn continuation.

