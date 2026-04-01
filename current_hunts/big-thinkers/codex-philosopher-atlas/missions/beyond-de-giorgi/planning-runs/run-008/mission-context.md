# Mission Context Snapshot

Mission: beyond-de-giorgi
Planning run: run-008
Timestamp: 2026-03-31T18:46:52Z

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

# Canonical Chain - Coupled Energy-Helicity Route With Early Coercivity Gate

## Central Premise

This branch is live only if full 3D energy-helicity transport yields more than exact cascade bookkeeping.

The default hypothesis is negative: exact energy-helicity coupling is **non-coercive** for theorem-facing purposes unless the chain can exhibit one coupled quantity or forbidden transfer pattern that:

- is one-sided or coercive enough to matter;
- survives mixed-helicity restoration and low-helicity regions;
- survives the localization needed by the target endpoint;
- beats or genuinely sharpens one frozen baseline criterion;
- depends on an NS-specific feature that Tao-style averaging destroys; and
- reaches a named bad term or bad transfer pattern inside an actual endpoint-facing argument.

If those conditions fail, the correct output is a calibrated obstruction memo, not a positive invariant narrative.

## Verifiable Result Target

Either:

- one proposition-scale conditional statement tying a specific coupled energy-helicity quantity or forbidden transfer pattern to one named continuation, concentration-exclusion, or stretching/enstrophy bottleneck, together with one benchmarked gain and one genuinely narrower missing lemma; or
- one calibrated obstruction memo showing that the route fails by non-coercivity, mixed-helicity restoration, low-helicity escape, localization collapse, prior-art collapse, baseline non-improvement, or a stacked combination of these.

## Scope Lock

Before substantive execution begins, fix all of the following:

- one provisional endpoint family at the level of burden type:
  continuation criterion,
  concentration exclusion,
  or stretching/enstrophy bottleneck;
- one invariant package to audit first:
  coarse-grained local balances,
  dyadic coupled fluxes,
  or one other sharply defined ledger;
- one exact Tao-sensitive feature to test in advance;
- one frozen baseline criterion that the route must beat or genuinely sharpen;
- one minimum quantitative gain threshold that still matters after localization, pressure, viscosity, and mixed-helicity debt are paid;
- one admission rule:
  no candidate is promoted unless it names one one-sided gain on one named bad term or bad transfer pattern;
- one novelty rule:
  favorable same-helicity or polarized sectors do not count unless they carry a quantitatively relevant portion of the full burden near the chosen endpoint family; and
- one passing and one failing Tao-calibration example.

If these cannot be fixed concretely, stop and write a setup obstruction.

## Ordered Steps

### Step 1 - Calibrate the invariant package and Tao discriminator

- Depends on: none.
- Action: write the exact energy and helicity transfer identities in the chosen package, separating exact structure from bookkeeping choices.
- Action: define the Tao-sensitive feature in advance and state exactly what it means for averaging to destroy it.
- Action: give one worked example that clearly passes the Tao screen and one that clearly fails.
- Action: screen immediately for prior-art overlap with Waleffe-type triad analysis, helical decimation, shell-model intuition, and same-helicity favorable-sector lore.
- Expected output: an audit memo listing exact structure, Tao calibration, and prior-art risk.
- Kill condition: if the Tao test cannot distinguish a real pass case from a real fail case, or if the package already collapses to known folklore or generic cascade language, stop and write an overlap or calibration obstruction.

### Step 2 - Run the coercivity gate before endpoint packaging

- Depends on: Step 1.
- Action: ask whether the chosen coupled quantity yields any one-sided, endpoint-relevant gain before absolute values, generic inequalities, or sign averaging erase it.
- Action: require that gain to point to one named bad term or bad transfer pattern:
  stretching production,
  enstrophy growth,
  concentration of active scales,
  or another precisely stated bottleneck.
- Action: keep at most two candidate gains, each stated in the same burden language as the frozen baseline criterion.
- Expected output: at most two candidate gains, each tied to one named bottleneck and one candidate quantitative benchmark.
- Kill condition: if no one-sided or exclusionary gain survives this gate, stop and write a non-coercivity obstruction.

### Step 3 - Pay the full-equation debt early

- Depends on: Step 2.
- Action: test each surviving candidate against mixed-helicity interactions, low-helicity regions, viscosity, and pressure as first-order constraints rather than late corrections.
- Action: state explicitly whether the candidate controls a non-negligible share of the full nonlinear burden or only a thin favorable sector.
- Action: reject any mechanism that works only in decimated, filtered, or strongly polarized regimes without a theorem-relevant burden estimate.
- Expected output: a full-equation viability ledger.
- Kill condition: if mixed-helicity restoration, low-helicity escape, viscosity, or pressure destroys the gain, stop and write the obstruction.

### Step 4 - Test localization and endpoint insertion with a benchmarked gain

- Depends on: Step 3.
- Action: insert the localization machinery required by the endpoint:
  cutoffs,
  local flux commutators,
  pressure terms,
  and coarse-graining losses.
- Action: write one explicit endpoint-facing inequality, exclusion statement, or contradiction line.
- Action: state the benchmark clearly:
  what burden is reduced,
  in what norm or scale,
  and by how much relative to the frozen baseline criterion.
- Action: require the Tao-sensitive feature from Step 1 to appear inside this endpoint-facing mechanism, not just in surrounding exposition.
- Expected output: a localization-and-insertion memo containing one explicit mechanism and one quantitative benchmark.
- Kill condition: if localization erases the gain, if the gain collapses to energy-only control, or if no benchmarked improvement over the baseline criterion can be written, stop and write a localization or no-bridge obstruction.

### Step 5 - Audit the remaining gap for genuine narrowness

- Depends on: Step 4.
- Action: if a positive route remains, isolate the first missing lemma.
- Action: test whether that lemma is strictly narrower than the full regularity problem in scale, norm strength, geometric scope, or burden share.
- Action: reject any missing lemma that merely restates full control of the original hard case in renamed language.
- Expected output: either one proposition-scale target with a genuinely narrower missing lemma or a calibrated obstruction stating the first honest failure.
- Kill condition: if the remaining gap is equivalent to the original problem, downgrade the branch to obstruction immediately.

### Step 6 - State the narrowest earned claim

- Depends on: Step 5.
- Action: if positive, write one proposition-scale conditional statement with:
  the endpoint,
  the coupled quantity,
  the exact gain,
  the localization assumptions,
  the benchmarked improvement over the baseline criterion,
  and the first genuinely narrower missing lemma.
- Action: if negative, write one obstruction memo with the narrowest honest labels:
  non-coercivity,
  mixed-helicity restoration,
  low-helicity escape,
  localization collapse,
  prior-art collapse,
  baseline non-improvement,
  or a stacked combination.
- Action: reject any final claim that merely says helicity is interesting, or that assumes a persistently polarized regime strong enough to encode the hard case away.
- Expected output: a final-comparison-ready positive route or a sharp no-go.
- Kill condition: if the final claim hides the main difficulty inside the hypothesis or conclusion language, narrow it until the debt is explicit.

## Success Standard

This chain succeeds only if it does one of two things:

- isolates one coupled energy-helicity mechanism that is one-sided enough, localizable enough, Tao-sensitive enough, and endpoint-relevant enough to earn a serious conditional proposition; or
- shows cleanly that the exact coupled invariant geometry is too non-coercive or too fragile under full-equation restoration and localization to improve on the frozen baseline criterion.

## Presentable-Result Assessment

Estimated probability of a presentable result: **high**, with the most likely output being a strong obstruction memo rather than a positive theorem route.

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


## run-003 — 2026-03-31T12:35:40Z

# Final Decision Memo - beyond-de-giorgi / run-003

## Decision

The winning chain is **Refined Chain 01: Fixed-Protocol Obstruction Audit for Exact NS Reformulations**.

This is the best next execution target because it has the strongest combined score on:

- presentable-result probability,
- useful failure floor,
- execution fit for this system,
- and still-nontrivial upside if a real hybrid mechanism survives.

Chain 03 has a slightly higher novelty ceiling in the abstract, but its own judgment makes clear that its positive route is much less executable here: the branch is likely to succeed only as an obstruction map, and its actionable contradiction-program probability is explicitly low. Chain 02 is genuinely different and worth preserving conceptually, but it has a lower floor and a higher risk of spending budget on descriptive Fourier structure that fails under localization or dynamics.

## Why Chain 01 Wins

Chain 01 is the cleanest next move because it forces the one loophole most likely to waste future effort into a bounded yes-or-no audit: can an exact NS reformulation change one named localized closure cost inside one frozen architecture after full bookkeeping is paid?

That question is narrow enough to execute rigorously and strong enough to matter. If the answer is no, the result is still mission-useful: we get a sharp obstruction memo that closes a live reformulation hope instead of leaving it half-alive. If the answer is yes, the branch already demands the right standard of proof: the gain must survive localization, projection, commutators, and Tao-style averaging, and must improve the fixed closure mechanism rather than merely restating the nonlinearity attractively.

This also best matches the current system. The chain is estimate-first, protocol-first, and designed to terminate cleanly. It does not require building an entire critical-element package before learning whether the route is even alive.

## Why The Others Lose

### Chain 02

Chain 02 preserves important diversity, but as the judgments note, it remains structurally vulnerable to producing coefficient-level or folklore-level distinctions that do not survive summation, localization, or persistence. Its best use here is as a source of calibration constraints, not as the next primary execution.

### Chain 03

Chain 03 is the strongest high-upside alternative, but it is still more credible as a compactness-and-rigidity obstruction audit than as a live positive attack. The setup burden is much larger, the theorem-compatibility risks are heavier, and the branch can absorb significant effort before identifying whether the route is circular.

## Elements Imported Into The Winner

The canonical winning chain keeps Chain 01 as the spine, but absorbs two useful upgrades from the losing branches:

1. From Chain 02:
   require earlier prior-art calibration and insist that any surviving gain be operational inside the audited localized scenario, not merely a static algebraic difference.

2. From Chain 03:
   require explicit solution-class and theorem-hypothesis compatibility in the fixed architecture, and refuse to promote any survivor whose first missing lemma is effectively equivalent to the original regularity problem.

## Canonical Execution Claim

Execute the refined Chain 01 audit as the next branch.

The branch should be judged a success only if it produces one of these:

- a quantified estimate-level gain on one fixed localized bottleneck inside one frozen architecture, with an explicit Tao discriminator and full loss ledger; or
- a bounded obstruction memo showing that the tested exact-reformulation family does not improve the chosen closure mechanism except possibly through hybrid effects that should be handed off elsewhere.

That is the best balance of floor, ceiling, and execution realism available in this run.

### Winning Chain

# CHAIN - Fixed-Protocol Obstruction Audit for Exact NS Reformulations

## Central Premise

Treat this branch as a bounded falsification test, not as the main search for the mission's beyond-De-Giorgi mechanism.

Question: within one explicitly fixed inherited estimate architecture, can a tightly defined family of exact Navier-Stokes reformulations, or one predeclared paired hybrid route, produce a localized estimate-level gain on one named bottleneck term that

- survives the full localization/projection/commutator bookkeeping,
- is operational in the audited localized scenario rather than merely an attractive static rewrite,
- is not merely a geometry-only or tensor-only artifact,
- and depends on a feature that Tao-style averaging destroys?

If not, the correct output is a sharp obstruction memo closing this loophole.

## Verifiable Result Target

Either:

- one concrete candidate that improves a single named localized bottleneck estimate in the fixed architecture and comes with an explicit Tao discriminator; or
- a bounded negative result showing that, for the specified architecture and candidate family, exact reformulations do not yield a presentable gain except possibly through hybrid mechanisms that leave this branch.

## Why This Chain Is Worth Running

This branch is worth running because "maybe an exact rewrite helps" is still a live enough loophole to deserve one disciplined closure attempt. What it should not claim to be is a broad discovery program. Its value is precision: either isolate one real estimate-level gain, or kill a narrow family of false hopes cleanly.

## Scope Lock

Before candidate testing begins, the chain must fix all of the following:

- one inherited estimate architecture:
  - De Giorgi truncation,
  - local-energy flux/localization,
  - vorticity stretching localization,
  - or one other specifically named architecture;
- one exact bad term inside that architecture;
- one named solution class and any theorem-hypothesis compatibility constraints needed for the architecture to make sense;
- one frozen localization protocol, including cutoff placement and where projection/commutators are paid;
- one bookkeeping currency of gain:
  - derivative count,
  - integrability/exponent improvement,
  - coefficient shrinkage,
  - or a strictly weaker hypothesis in the same closure scheme;
- one explicit NS-versus-averaged discriminator;
- one perturbation metric for geometry/alignment dependence;
- one note stating what is genuinely new relative to already-known negatives and nearby prior art.

If any of these remain vague, the branch defaults to an under-specified negative memo.

## Ordered Steps

### Step 1 - Fix the architecture, bottleneck, protocol, compatibility, and novelty claim

- Depends on: none.
- Action: choose exactly one inherited architecture and one mission-central bad term.
- Action: name the solution class in which the localized estimate is supposed to operate and record any theorem-hypothesis compatibility constraints.
- Action: freeze the localization protocol before comparing candidates.
- Action: define one gain currency that every candidate will be judged in.
- Action: state what new localized estimate or bookkeeping issue is being tested that prior project negatives and nearby prior art did not already settle.
- Expected output: a screening memo containing the architecture, bad term, solution class, compatibility note, localization protocol, gain metric, novelty claim, and a bounded candidate family.
- Kill condition: if the chain cannot make the architecture or comparison protocol concrete, stop and write the under-specification memo.

### Step 2 - State the Tao discriminator before any algebraic optimism

- Depends on: Step 1.
- Action: for each candidate family member, say exactly what exact NS feature is supposed to matter and how Tao-style averaging destroys or washes it out.
- Action: reject any candidate whose purported specialness only exists at the identity level and has no clear place to alter the localized estimate.
- Expected output: a Tao-screen memo mapping each candidate to a precise NS-versus-averaged distinction.
- Kill condition: if no candidate has a concrete Tao discriminator, close the branch negatively rather than pretending the family is still live.

### Step 3 - Derive candidate estimates with full loss ledgers

- Depends on: Step 2.
- Action: test a predeclared family of at most 2-3 exact reformulations of the same nonlinearity.
- Action: allow at most one paired hybrid route, such as a coupled identity or auxiliary propagated quantity, only if it still targets the same bad term in the same architecture.
- Action: for each candidate, record explicitly:
  - localization losses,
  - projection or Calderon-Zygmund losses,
  - commutator costs,
  - shell/frequency bookkeeping,
  - and any cost transfer that merely relocates rather than reduces the obstruction.
- Expected output: an estimate ledger showing for each candidate whether the gain is real, cosmetic, hybrid, or architecture-changing.
- Kill condition: if every candidate reproduces the same effective closure cost once all losses are paid, and the paired route does not change that, stop and write the bounded obstruction memo.

### Step 4 - Run the geometry/tensor split early and classify, not purify

- Depends on: Step 3.
- Action: test any apparent gain against the predeclared perturbation metric immediately.
- Action: classify each surviving signal as:
  - generic,
  - hybrid algebraic-geometric or algebraic-tensorial,
  - or geometry-only/tensor-only.
- Action: do not count near-Beltrami or special alignment as success by itself, but also do not discard a hybrid mechanism just because it is not purely algebraic.
- Expected output: a robustness memo stating whether the candidate survives outside special regimes and whether any remainder stays inside the fixed architecture.
- Kill condition: if the only surviving effect is regime-specific and leaves no estimate-level remainder in the fixed setup, hand it off and close this branch negatively.

### Step 5 - Convert the survivor into either a usable proposition or a sharp handoff

- Depends on: Step 4, or directly on Step 3 if the branch dies there.
- Action: if a candidate survives, translate it into a proposition that feeds the same architecture and quantify the gain in the predeclared bookkeeping currency.
- Action: verify that the gain improves the actual localized closure mechanism in the audited scenario rather than only producing a static rewritten identity.
- Action: if the candidate only works by changing architecture, say so explicitly and convert the result into a handoff note rather than a false positive.
- Action: if no candidate survives, write the strongest obstruction statement actually earned.
- Expected output: either a draft proposition with explicit quantitative gain and first missing lemma, or a bounded obstruction/handoff memo.
- Kill condition: if the apparent survivor does not improve the fixed closure mechanism in quantified form, or if its first missing lemma is effectively equivalent to the original regularity problem, do not promote it.

### Step 6 - Close with the narrowest earned claim

- Depends on: Step 5.
- Action: state exactly which architecture, bad term, solution class, protocol, and candidate family were tested.
- Action: state exactly what the Tao discriminator showed and whether the surviving effect was generic, hybrid, or purely regime-dependent.
- Action: include an explicit prior-art comparison so the output distinguishes a new obstruction diagnosis from a rediscovered known failure mode.
- Expected output: one of three endpoints:
  - a live estimate-level lead within the fixed architecture,
  - a bounded obstruction result on the specified reformulation family,
  - or a handoff note showing that any live signal is hybrid and belongs to another branch.
- Kill condition: if the final statement reaches beyond the tested family or fixed architecture, narrow it until it is fully earned.

## Probability Assessment

**Probability that this chain yields a presentable result: 0.76**

The most likely presentable result is a disciplined obstruction memo, not a breakthrough.


## run-004 — 2026-03-31T13:45:20Z

# Final Decision Memo - beyond-de-giorgi / run-004

## Decision

The winning chain is **Refined Chain 02 - Critical Element Program With Extraction Audit Before Rigidity**.

It should be executed in a slightly hardened form: keep Chain 02 as the canonical spine, then import two constraints from the losing chains:

- from Chain 01: earlier anti-cosmetic admissibility and overlap accounting, so the branch cannot drift into polished but non-operative mechanism shopping;
- from Chain 03: an explicit prior-art and Tao-sensitivity screen for any promoted rigidity quantity, treated as a secondary discriminator rather than the main gate.

## Why Chain 02 Wins

Chain 02 has the best total profile across the decision criteria.

First, it has the strongest novelty ceiling. If it works positively at all, it does not merely rank obstructions or repackage tensor structure; it produces a theorem-like compactness-rigidity program with one host space, one critical object, one contradiction mechanism, and one sharply identified missing lemma. That is the highest-upside presentable output in the field.

Second, its floor is still strong after refinement. The branch now forces an extraction-package audit before any rigidity rhetoric, defines the critical element before choosing a rigidity mechanism, and allows a precise obstruction result if the route dies at extraction, formulation, definability, coercivity, or contradiction. That makes failure informative rather than aesthetic.

Third, it fits this system better than the alternatives. The workflow is sequential, auditable, and theorem-shaped. Each step has a hard dependency and a clean kill condition. That is better suited to disciplined execution than Chain 01's broader cross-family screening or Chain 03's heavier exposure to nonlocal tensor ambiguity.

## Why Not Chain 01

Chain 01 has the safest floor in the portfolio and the best negative-information yield. But even after refinement it remains primarily a triage court. Its most likely success mode is a bounded obstruction or bucketed handoff, not a single executable proof architecture. That makes it an excellent discipline layer and an excellent reserve branch, but not the best final winner once the funnel has already narrowed.

The right move is therefore to keep Chain 01's strongest procedural gains inside the winner:

- force overlap accounting early;
- reject cosmetic gains before ranking;
- allow zero-promotion outcomes without narrative pressure.

## Why Not Chain 03

Chain 03 is honest and useful, but it is still more likely to produce a calibrated obstruction memo than a live route. Its positive path remains narrow because every candidate has to survive nonlocal pressure-Hessian debt, representation stability, eigenvalue degeneracy, and prior-art adjacency all at once. That makes it a good negative-discovery branch, but a weaker final choice than Chain 02.

The main import from Chain 03 is methodological:

- any promoted rigidity quantity in Chain 02 should face an explicit prior-art check;
- Tao-sensitivity should be recorded early, but only as secondary evidence once definability and contradiction power are established.

## Execution Directive

Execute **Chain 02** as the mission's canonical next chain, with the imported refinements listed above and no further broadening. The output standard remains theorem-like: either a conditional compactness-rigidity program in one audited host space, or a precise obstruction map locating the first fatal break.

### Winning Chain

# Chain 02 - Critical Element Program With Extraction Audit, Early Overlap Control, and Secondary Tao Screen

## Central Premise

A compactness-rigidity route is live only if one specific critical or near-critical host space supports an explicit extraction package, one theorem-like minimal blowup object, and one rigidity quantity that is actually defined on that class and can drive a contradiction.

This branch therefore fixes one host space first, audits the extraction package theorem by theorem, defines the hypothetical critical element before overcommitting to rigidity, and treats Tao-sensitivity only as a secondary discriminator after definability and contradiction power are established.

## Verifiable Result Target

Either:

- a theorem-like conditional program naming one host space, the exact extraction and stability inputs, the critical-element class, one admissible rigidity quantity, and the first missing lemma whose scope is strictly narrower than full regularity; or
- an obstruction map identifying the first fatal break as one of:
  - extraction,
  - critical stability,
  - normalization or solution class,
  - overlap or cosmeticity,
  - definability of the rigidity quantity,
  - failure of coercivity,
  - or failure of contradiction even under almost periodicity.

## Why This Is The Winning Chain

This is the highest-upside branch that still has a disciplined failure mode. It is more concrete than an open-ended mechanism-ranking audit and more theorem-oriented than the tensor branch. If it succeeds positively, it yields a genuine execution-ready proof architecture. If it fails, it should still produce a sharply localized obstruction rather than a vague research memo.

## Scope Lock

Before substantive execution begins, fix all of the following:

- the intended solution framework and localization regime;
- the admissibility standard for a promoted rigidity quantity:
  - it must be defined on the actual critical-element class,
  - stable under the compactness limit,
  - tied to one explicit contradiction mechanism,
  - and non-cosmetic in the chosen architecture;
- the overlap-audit sources:
  - prior mission findings,
  - internal run history,
  - and the nearest literature family;
- the policy that Tao-sensitivity is supportive evidence only, not the main gate.

If these items cannot be fixed concretely, stop and write a setup obstruction.

## Ordered Steps

### Step 1 - Audit one host space against a full extraction package

- Depends on: none.
- Action: compare `L^3`, `\dot H^{1/2}`, and only if justified `BMO^{-1}` against an explicit checklist:
  - local theory in the intended solution framework,
  - large-data perturbation or stability,
  - profile decomposition or equivalent extraction input,
  - symmetry normalization,
  - pressure or local-energy compatibility,
  - and a compactness notion usable by the later rigidity step.
- Action: for each candidate host space, record the known inputs, solution-class commitments, prior-art overlap, and at most one sharply identified missing theorem on the critical path.
- Action: reject host spaces whose apparent viability depends on diffuse missing ingredients or on merely verbal compatibility.
- Expected output: a package-audit table with requirement, known input, overlap note, and missing piece, plus one chosen host space or an explicit no-host verdict.
- Kill condition: if no single host space clears the checklist except for at most one sharply stated missing theorem, stop and record a package obstruction.

### Step 2 - Define the hypothetical minimal blowup object in the chosen framework

- Depends on: Step 1.
- Action: state the minimizing quantity, solution class, symmetry group, normalization conventions, and the exact compactness or almost-periodicity statement the extraction package would deliver.
- Action: specify how scaling, spatial translation, pressure normalization, and any Galilean issue are handled in the chosen framework.
- Action: require theorem-like formulation: under inputs A, B, and C, a minimal counterexample with properties P, Q, and R exists.
- Expected output: a theorem-like critical-object dossier with one dependency graph and no hidden auxiliary assumptions.
- Kill condition: if the critical object cannot be stated without importing additional unproved ingredients beyond the Step 1 audit, stop and record a formulation obstruction.

### Step 3 - Screen rigidity quantities only on the actual critical-element class

- Depends on: Step 2.
- Action: list candidate rigidity quantities or identities that are well-defined on the Step 2 class.
- Action: for each candidate, record:
  - the exact contradiction mechanism it is supposed to support,
  - whether it gives sign, monotonicity, coercivity, unique-continuation leverage, or another named mechanism,
  - the nearest prior-art overlap,
  - and whether Tao's averaged model appears to destroy the relevant feature.
- Action: reject any candidate that is undefined on the class, unstable under the compactness limit, already absorbed by a known non-operative template, or cosmetic in the chosen architecture.
- Action: treat Tao-failure only as a secondary discriminator after the previous screens are passed.
- Expected output: one promoted rigidity quantity and at most one backup, each with a short mechanism statement and an overlap note.
- Kill condition: if no candidate survives definability, non-cosmeticity, and mechanism screening, stop and record a rigidity obstruction.

### Step 4 - Force a genuine complexity drop in the contradiction step

- Depends on: Step 3.
- Action: run the promoted rigidity quantity through the critical element and state the contradiction pathway line by line, including where compactness, almost periodicity, pressure structure, and solution-class regularity enter.
- Action: identify the first missing lemma and require that it be strictly narrower than arbitrary finite-energy regularity, using the compactness-normalized class in an essential way.
- Action: classify failure precisely as one of:
  - non-closure under limits,
  - lack of coercivity,
  - insufficient regularity to state or pass the quantity,
  - prior-art collapse,
  - or failure of contradiction even under almost periodicity.
- Expected output: either a conditional contradiction theorem schema or a sharply typed failure memo.
- Kill condition: if the first missing lemma is effectively the full regularity problem, or if the failure mode cannot be localized, downgrade to obstruction.

### Step 5 - State the narrowest earned claim in theorem form

- Depends on: Step 4.
- Action: write the final result as either:
  - a conditional theorem blueprint with exact assumptions, exact known inputs, exact missing lemma, and conditional consequence; or
  - an obstruction statement naming the first fatal break and why later steps cannot start.
- Action: keep the final claim tied to the single audited host space and the single promoted rigidity quantity. Remove all unevaluated alternatives.
- Action: state explicitly what Tao-sensitivity did and did not add to the case.
- Expected output: a final-comparison-ready chain that is either an executable conditional compactness-rigidity program or a precise obstruction map.
- Kill condition: if the final claim cannot be written in theorem-like form, the chain has not earned a presentable result.

## Success Standard

Do not count the branch as successful because it sounds like a Kenig-Merle program. It succeeds only if it isolates one audited host space, one critical-element class, one admissible rigidity quantity, and one missing lemma that is genuinely narrower than the whole problem. Otherwise the correct output is a precise obstruction.


## run-005 — 2026-03-31T14:23:42Z

# Final Decision Memo - beyond-de-giorgi / run-005

## Decision

The winning chain is **Chain 01**, in refined form:

**Frozen-Framework Compactness-Rigidity Falsification With Early No-Host Gate**

This should be the next chain executed, with two incorporated upgrades:

- from Chain 02: lock the theorem endpoint and the progress currency early, so the branch cannot drift into symbolic or template-level optimism;
- from Chain 03: keep overlap and packaging-robustness checks explicit, so any surviving rigidity route is not an artifact of one cosmetic formulation.

## Why Chain 01 Wins

Chain 01 has the best overall score on the actual decision criteria.

First, it has the highest chance of producing a genuinely presentable result. The refined version is already calibrated to the run-005 evidence on disk, especially the possibility that the honest outcome is an audited no-host or no-rigidity verdict rather than a live positive program. That makes it less dependent on discovering a new effect from scratch.

Second, it still has the strongest useful floor on failure. Even if the positive Kenig-Merle-style route dies, Chain 01 can return a decision-grade obstruction map with a clean taxonomy: no coherent host space, no operational critical object, no admissible rigidity quantity, or no genuine complexity drop. That is stronger than a vague negative result from the other branches.

Third, it retains the best ceiling compatible with this system. Chain 02 has the sharper Tao-sensitive novelty ceiling, but its positive branch depends on finding an explicit helical inequality that survives full reconstruction, which is a narrow and fragile event. Chain 03 is more likely to collapse into informative-but-noncoercive tensor language. Chain 01 is the only branch that can still end in a theorem-shaped compactness-rigidity package if one coherent starting package actually exists.

Fourth, it is the best execution fit for this repository. The branch can directly absorb the selector and judgment evidence already produced in run-005, rather than reopening the search from a fresh symbol-level or tensor-level program. That makes it more likely to converge quickly to an honest result.

## Why The Others Lose

### Chain 02

Chain 02 is the best adversarial test of exact Navier-Stokes interaction geometry and the most Tao-sensitive branch in the portfolio. Its novelty ceiling is real. But the positive route is still too contingent on a very specific outcome: one explicit helical feature must survive shell summation, mixed-helicity restoration, and localization with enough margin to matter at theorem scale. That makes its presentable-result odds slightly worse, and its execution risk higher, than Chain 01.

### Chain 03

Chain 03 is serious and well-disciplined after refinement, but it has the weakest combined profile of the finalists. Its overlap risk is high, its positive route is less clearly differentiated from existing tensor/alignment families, and its likely success mode is an obstruction memo with a lower novelty ceiling than the helical route and a lower theorem-shaped ceiling than Chain 01.

## What Gets Merged Into The Winner

The winner should not be Chain 01 in its narrower original form. It should absorb the strongest discipline from the losing chains:

- lock one theorem-level endpoint or contradiction line before host-space comparison begins;
- declare the progress currency explicitly, so any claimed complexity drop is measured rather than narrated;
- keep prior-art overlap accounting early and active, not deferred to the end;
- require any promoted rigidity quantity to survive equivalent packaging checks rather than relying on one convenient formulation;
- keep Tao-sensitivity as a mandatory secondary screen once mathematical operability is established.

## Final Call

Execute **Chain 01** next, in the canonical form written in `winning-chain.md`.

### Winning Chain

# Frozen-Framework Compactness-Rigidity Falsification With Early Endpoint Lock

## Central Premise

Treat the compactness-rigidity route as an audited falsification program first and a positive blueprint only second.

A live forward branch exists only if one host-space / solution-framework pair supports, in one coherent package:

- a real extraction statement rather than an aspirational one;
- a theorem-like minimal blowup object with explicit temporal architecture;
- one rigidity quantity defined on that actual class and robust to equivalent packaging;
- and a contradiction step on one fixed theorem-level endpoint whose first missing input is genuinely narrower than full regularity.

If no such package exists, the correct output is an obstruction memo stating whether the branch fails at no-host, no-frozen-object, no-rigidity, or no-complexity-drop stage.

## Verifiable Result Target

Either:

- an audited no-host verdict under one frozen framework and one fixed endpoint;
- a theorem-like conditional program naming one host space, one solution framework, one critical-element class, one admissible rigidity quantity, one contradiction line, and one genuinely narrower missing lemma; or
- a stacked obstruction memo showing that the compactness-rigidity route lacks a coherent audited starting point before the final contradiction.

## Scope Lock

Before host spaces are compared, fix all of the following:

- one primary solution framework;
- one theorem-level endpoint or contradiction line where the branch would have to cash out;
- the temporal architecture for any minimal object: forward maximal-lifespan, ancient, normalized near blowup time, or another explicitly named option;
- burden categories that must stay separated:
  extraction and stability,
  symmetry and temporal normalization,
  pressure or local-energy compatibility,
  overlap with prior art,
  and packaging robustness of any later rigidity quantity;
- the rule that stacked multi-theorem debt counts as decisive failure, not as "close except for one theorem";
- the policy that Tao-sensitivity is mandatory but secondary:
  it cannot rescue a mathematically non-operative route, and it cannot be ignored once a route becomes operational;
- the progress currency for the contradiction step:
  coercivity, localization burden, compactness debt, regularity demand, or another explicitly named currency.

If these items cannot be fixed concretely, stop and write a setup obstruction.

## Ordered Steps

### Step 1 - Freeze one framework and one endpoint before ranking host spaces

- Depends on: none.
- Action: choose one primary framework in which the whole branch will be judged.
- Action: state the theorem-level endpoint or contradiction line the branch is trying to reach.
- Action: state what bridge, if any, is required to connect that framework to the inherited suitable-weak / local-energy floor.
- Action: reject any setup that compares host spaces across incompatible frameworks or shifts endpoints midstream.
- Expected output: a framework-and-endpoint memo naming one solution class, one temporal architecture, and one contradiction target.
- Kill condition: if no single framework can host the extraction, critical-object, and rigidity burdens on one ledger, stop and record a framework obstruction.

### Step 2 - Re-audit host spaces with separated burden columns

- Depends on: Step 1.
- Action: compare `L^3`, `\dot H^{1/2}`, and only if still justified `BMO^{-1}` inside the frozen framework.
- Action: for each space, record separately:
  local theory,
  large-data stability or perturbation,
  extraction or profile input,
  symmetry and temporal normalization,
  pressure or local-energy compatibility,
  and prior-art overlap.
- Action: use the existing run-005 host-space audit as evidence to be confirmed or narrowed, not ignored.
- Action: treat a diffuse multi-theorem architecture gap as decisive failure rather than a near miss.
- Expected output: a package-audit table plus either one surviving host-space / framework pair or an explicit no-host verdict.
- Kill condition: if every candidate fails by stacked debts rather than one narrow missing ingredient, stop and write the no-host obstruction.

### Step 3 - Define the minimal blowup object only if a single pair survives

- Depends on: Step 2.
- Action: state the minimizing quantity, solution class, lifespan type, time normalization, symmetry group, and pressure conventions.
- Action: name the exact compactness or almost-periodicity statement the chosen extraction package delivers.
- Action: reject any formulation that imports new unproved structure beyond what Step 2 admitted.
- Expected output: a theorem-like critical-object dossier with explicit temporal architecture and no hidden bridges.
- Kill condition: if the critical object is only formal because the compactness statement is missing or mismatched to the chosen class, stop and record a formulation obstruction.

### Step 4 - Screen rigidity quantities with a dual gate and a robustness check

- Depends on: Step 3.
- Action: list only rigidity quantities that are defined on the actual critical-element class.
- Action: first apply the mathematical-operability gate:
  definability,
  stability under the compactness limit,
  non-cosmetic role in the contradiction,
  and one explicit mechanism such as coercivity, monotonicity, unique continuation, or exclusion of a named scenario.
- Action: require each candidate to survive an equivalent-packaging check, so the mechanism is not an artifact of one convenient formulation.
- Action: only after that, apply the mission gate:
  record what exact Navier-Stokes-specific feature the quantity uses and whether Tao-style averaging appears to destroy that feature.
- Action: reject candidates that merely restate familiar templates without a new operational lever.
- Expected output: one promoted rigidity quantity and at most one backup, each with an operability note, a robustness note, and a Tao-relevance note.
- Kill condition: if no quantity survives the operability gate, or if the only survivors are packaging artifacts or Tao-compatible in the relevant sense, stop and write a rigidity obstruction.

### Step 5 - Demand a genuine complexity drop on the fixed contradiction line

- Depends on: Step 4.
- Action: run the promoted quantity through the chosen contradiction line step by step.
- Action: state where compactness, temporal architecture, pressure structure, localization, and regularity demands enter.
- Action: identify the first missing input and measure the claimed reduction in the declared progress currency.
- Action: if the missing input really requires simultaneous gains in compactness, compatibility, and coercivity, classify that honestly as a stacked architectural obstruction rather than a fake single lemma.
- Expected output: either a conditional contradiction schema with a real complexity drop or a typed obstruction memo.
- Kill condition: if the alleged missing lemma is effectively the whole problem, or if the route only works by hiding multiple debts inside one label, stop and downgrade to obstruction.

### Step 6 - Close with the narrowest earned claim

- Depends on: Step 5.
- Action: write the final result in theorem-like form.
- Action: if positive, name exactly one host space, one framework, one critical-element class, one rigidity quantity, one contradiction line, one missing lemma, and one conditional consequence.
- Action: if negative, state whether the first honest break is:
  no coherent host space,
  no operational critical object,
  no admissible rigidity quantity,
  or no genuine complexity drop.
- Action: allow the final obstruction to be stacked if that is what the audited record supports.
- Expected output: a final-comparison-ready chain that is either a narrow conditional program or a precise obstruction map.
- Kill condition: if the final claim cannot be written without overstating the coherence of the package, narrow it further until it is fully earned.

## Success Standard

Do not count the branch as successful because it resembles a Kenig-Merle program. It succeeds only if it either:

- isolates one audited host-space / framework pair and one real rigidity route with a genuinely narrower missing lemma; or
- proves, in a disciplined and localized way, that no such coherent package is presently available.


## run-006 — 2026-03-31T15:04:45Z

# Final Decision Memo - beyond-de-giorgi / run-006

## Decision

The winner is **Refined Chain 01**:
`Endpoint-First Pressure-Hessian Obstruction Test With Early Packaging and Harmonic-Freedom Gates`.

The canonical execution chain is written in:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-006/winning-chain.md`

## Why Chain 01 Wins

Chain 01 is the best fit across all decision criteria.

- **Highest chance of a genuinely presentable result.**
  Its negative branch is already clean, typed, and mission-useful: it can certify whether the tensor route dies from repackaging, lack of an endpoint-attached observable, surviving same-scale harmonic freedom, or NS-specific but non-coercive structure. That is a better presentable floor than the others.
- **Strongest novelty ceiling.**
  If anything positive survives in this mission, the pressure-Hessian and harmonic-moment route is the most likely place to find a genuinely nontrivial Navier-Stokes-specific mechanism rather than a repackaged endpoint architecture or an exact-but-fragile symbol effect.
- **Strongest useful floor on failure.**
  Even failure gives a sharp obstruction map at the real tensor/nonlocal bottleneck. It does not merely say "weak-type tools are generic" or "triad effects collapse after summation"; it can identify whether the live obstruction is nonlocal freedom itself.
- **Best execution fit for this system.**
  The chain is already organized around early kill conditions, honest obstruction outputs, and a small number of decisive gates. That matches the system well: it can produce a concrete memo without needing a large speculative buildout.

## Why The Others Lose

- **Chain 02** has real value and the cleanest exact-symbol discriminator, but its positive branch is too exposed to shell-summation, bad-class, and localization collapse. Its best likely output is a good obstruction memo, but the floor is slightly narrower and the ceiling is lower than Chain 01 because exact triad structure has a long history of dying during reconstruction.
- **Chain 03** is disciplined and useful as an audit, but it is the weakest positive route. The mission risk is that it proves only that weak-type or Lorentz packaging is generic or nonlocalization-compatible, which is informative but less novel and less central than a decisive tensor obstruction.

## Elements Merged Into The Winner

The winning chain is Chain 01 with two upgrades borrowed from the losing chains.

- From **Chain 02**: require an explicit minimum quantitative gain threshold and a full reconstruction ledger before any positive promotion survives.
- From **Chain 03**: require explicit localization compatibility whenever the chosen endpoint is local or cutoff-based, so the route cannot survive as endpoint packaging alone.

These strengthen Chain 01 without changing its core identity.

## Final Judgment

Execute the pressure-Hessian branch, but execute it as an obstruction-first route under a hard quantitative standard. The branch only earns a positive continuation if one tensor observable produces an explicit endpoint-level gain that survives prior-art screening, equivalent-packaging screening, full harmonic accounting, and any required localization debt with positive margin. Otherwise, the intended success is a sharply typed obstruction memo.

### Winning Chain

# Canonical Winning Chain - Endpoint-First Pressure-Hessian Obstruction Test With Quantitative Reconstruction and Localization Gates

## Central Premise

Treat the pressure-Hessian tensor branch primarily as an audited obstruction
test, not as a default positive regularity blueprint.

A live positive route exists only if one exact theorem endpoint and one
contradiction line can be tied to one tensor mechanism that:

- acts on the full stretching term `S omega . omega` or on the actual
  affine-and-higher harmonic moments;
- survives prior-art and equivalent-packaging screening;
- remains meaningful near eigenvalue degeneracy;
- yields one explicit analytic gain in a named estimate or contradiction step;
- clears a stated minimum success threshold after full reconstruction; and
- remains viable after any localization debt required by the chosen endpoint is
  honestly charged.

If no such mechanism survives, the correct output is a calibrated obstruction
memo stating that pressure-Hessian structure is informative but non-coercive, or
that the branch fails earlier by repackaging, endpoint mismatch, same-scale
harmonic freedom, or localization collapse.

## Verifiable Result Target

Either:

- a proposition-scale conditional statement naming one theorem endpoint, one
  tensor package, one admissible observable, one explicit inequality or defect
  identity, one minimum gain threshold, one reconstruction regime, and one
  genuinely narrower missing lemma; or
- a calibrated obstruction memo identifying the first honest failure:
  prior-art-only repackaging,
  no endpoint-attached observable,
  same-scale harmonic freedom survives,
  localization collapses the route,
  or NS-specific algebra without coercive gain.

## Why This Chain Is Worth Running

This is the highest-upside branch that still fails usefully. It stays closest to
a genuinely pressure-adjacent Navier-Stokes mechanism, but it is now built so
that positive progress must be earned early and quantitatively.

## Scope Lock

Before any observable shortlist is built, freeze all of the following:

- one exact theorem endpoint:
  a continuation criterion,
  a contradiction inequality,
  or another explicitly named cash-out line;
- one progress currency:
  one-sided inequality,
  monotonicity,
  cancellation of a named harmonic-moment family,
  or a quantified reduction of a specified nonlocal remainder;
- one minimum quantitative success threshold that would still matter after full
  reconstruction and any required localization losses;
- one rule that same-scale unconstrained exterior or harmonic freedom counts as
  immediate failure;
- one rule that Tao sensitivity is mandatory but not sufficient:
  averaged-model failure does not by itself produce theorem relevance.

If these items cannot be fixed concretely, stop and write a setup obstruction.

## Ordered Steps

### Step 1 - Freeze the theorem endpoint before freezing tensor language

- Depends on: none.
- Action: choose one exact theorem endpoint and one contradiction line.
- Action: state what a positive deliverable would literally look like:
  an inequality,
  a continuation criterion,
  or a defect identity with an explicit role in the endpoint.
- Action: define the admissible gain currency and the minimum quantitative
  threshold needed for the route to matter after reconstruction.
- Action: reject branches that can only name a bottleneck theme but not the
  exact mathematical cash-out.
- Expected output: an endpoint memo naming one target statement, one progress
  currency, and one minimum success threshold.
- Kill condition: if the branch cannot say how a tensor mechanism would cash out
  mathematically, stop and record an endpoint obstruction.

### Step 2 - Front-load prior-art overlap and equivalent-packaging screening

- Depends on: Step 1.
- Action: map the closest prior families:
  strain-vorticity alignment,
  eigenframe geometry,
  restricted-Euler defects,
  pressure-Hessian modeling,
  and conditional regularity criteria.
- Action: list the main equivalent tensor packagings of the proposed mechanism.
- Action: reject any candidate whose apparent novelty is only a reformulation,
  or whose known equivalent packaging is already non-coercive against the chosen
  endpoint.
- Expected output: an overlap-and-packaging memo with one admitted mechanism
  family and an explicit non-novelty risk note.
- Kill condition: if the branch survives only by renaming a familiar mechanism
  or by hiding in one favored packaging, stop and write a repackaging
  obstruction.

### Step 3 - Freeze one tensor package only after the endpoint and overlap gates survive

- Depends on: Step 2.
- Action: choose one exact package for the branch:
  the stretching equation,
  the exact `S` / `nabla^2 p` relation,
  and the local-plus-harmonic pressure split.
- Action: state the admissible observable class in a way that is frame-invariant
  or explicitly robust near repeated eigenvalues.
- Action: require each candidate observable to be tied to the endpoint by one
  explicit analytic role, not just by narrative appeal.
- Expected output: a representation memo and a shortlist of at most one primary
  observable plus one backup.
- Kill condition: if every candidate is descriptive, packaging-dependent, or
  unattached to the endpoint, stop and record an observable obstruction.

### Step 4 - Promote an observable only through an operational gate, then a Tao gate

- Depends on: Step 3.
- Action: apply the operational gate first:
  definability on the chosen package,
  robustness near degeneracy,
  an explicit inequality or defect identity,
  and a non-cosmetic role in the chosen endpoint.
- Action: only after that, apply the Tao gate:
  state the exact averaged comparison being used and which feature the averaging
  destroys.
- Action: reject any candidate for which Tao sensitivity is only branding, or
  for which NS-specific algebra does not translate into endpoint-level leverage.
- Expected output: one promoted observable with an operability note and a
  Tao-sensitivity note.
- Kill condition: if no candidate survives the operational gate, or if Tao
  relevance cannot be stated concretely, stop and record a mechanism
  obstruction.

### Step 5 - Charge the full nonlocal and reconstruction debt as a decisive test

- Depends on: Step 4.
- Action: test whether the promoted observable acts on the full
  `S omega . omega` term or on the actual affine-and-higher harmonic moments,
  not only on a local or self-induced piece.
- Action: split the local and harmonic pressure contributions explicitly and
  record exactly what exterior freedom remains.
- Action: if the remaining harmonic or exterior freedom is same-scale and
  unconstrained relative to the endpoint, classify that as immediate failure.
- Action: distinguish:
  total independence,
  weak but endpoint-irrelevant correlation,
  or genuine cancellation/control.
- Action: if the chosen endpoint is local or cutoff-based, charge the full
  localization bill as part of the same reconstruction test:
  cutoff losses,
  pressure-splitting debt,
  commutator terms,
  and any local-energy bookkeeping needed to return to the actual setting.
- Action: measure whether the claimed gain still clears the Step-1 threshold
  after this full restoration.
- Expected output: a reconstruction verdict specifying whether the observable
  survives full harmonic accounting and any required localization with positive
  margin.
- Kill condition: if the route closes only on a reduced model, on a renormalized
  local term, on an uncontrolled same-scale remainder, or only before
  localization debt is paid, stop and write the obstruction.

### Step 6 - Close only on an earned survivor

- Depends on: Step 5.
- Action: if a survivor remains, write a proposition-scale target naming:
  the endpoint,
  the tensor package,
  the observable,
  the explicit gain,
  the reconstruction regime,
  and the first missing lemma.
- Action: measure whether the missing lemma is a genuine complexity drop in the
  declared progress currency.
- Action: if not, state the narrowest honest obstruction:
  repackaging only,
  no endpoint-attached observable,
  same-scale harmonic freedom survives,
  localization collapse,
  or NS-specific but non-coercive structure.
- Expected output: either a conditional positive route or a precise obstruction
  memo ready for execution.
- Kill condition: if the positive statement hides the whole regularity problem
  inside one unlabeled tensor estimate, downgrade it to obstruction.

## Success Standard

Do not count the branch as successful because it produces a polished invariant
table or an NS-specific identity. It succeeds only if it either:

- isolates one endpoint-attached tensor mechanism that survives packaging, full
  harmonic accounting, and any required localization with a genuinely narrower
  missing lemma; or
- proves, cleanly and early, that the pressure-Hessian route remains
  non-coercive once the same-scale nonlocal and reconstruction debt is fully
  charged.

## Presentable-Result Assessment

Estimated probability of a presentable result: **0.80**.

The most credible endpoint is still a presentable obstruction memo rather than a
live positive regularity route. That is the intended design standard, not a
fallback embarrassment.


## run-007 — 2026-03-31T18:16:42Z

# Final Decision Memo - beyond-de-giorgi / run-007

## Decision

The winning chain is **Refined Chain 03**, upgraded with two imported constraints:

- from Chain 01: an explicit Tao-discriminator calibration with one passing and one failing example, plus stricter typed failure labels;
- from Chain 02: a frozen baseline criterion and minimum quantitative gain threshold, plus a hard test that any surviving missing lemma is genuinely narrower than the full regularity problem.

The canonical execution text appears in `winning-chain.md`.

## Why Chain 03 Wins

Chain 03 is the best single chain to execute next because it gives the strongest overall blend of:

- **presentable-result probability:** it had the highest judged probability of yielding a presentable outcome, and its likely negative output is still sharp rather than vague;
- **specificity:** unlike Chain 01, it is already a thesis-specific mathematical route rather than a meta-audit over multiple candidate families;
- **useful failure mode:** if it fails, it fails in a way that should produce a clean statement about non-coercivity, mixed-helicity restoration, low-helicity escape, localization collapse, or prior-art collapse;
- **novelty ceiling:** it still preserves a real upside if one coupled energy-helicity quantity survives all gates and reaches a theorem-facing bottleneck;
- **execution fit:** its refined form naturally enforces early kill conditions, which is a good fit for this system's strength at building honest obstruction dossiers rather than narratively inflating weak mechanisms.

## Why Chain 01 Does Not Win

Chain 01 remains the best **portfolio governor**. It is the strongest cross-family audit protocol and the safest broad filter. But that is no longer the right job. The wide-funnel process has already done the portfolio selection and refinement work. As the next executable chain, Chain 01 is still too meta: it spends effort arbitrating among candidate classes instead of committing to one mathematically distinct route.

Its best features were therefore imported rather than chosen outright:

- operational Tao calibration;
- typed failure severity;
- refusal to promote rhetoric without a hard artifact.

## Why Chain 02 Does Not Win

Chain 02 keeps the most concrete transport-side upside, but it remains more vulnerable than Chain 03 at the first-contact level:

- definability may already require too much flow-map regularity;
- the route sits closer to known BKM-type or cumulative-strain repackaging risk;
- viscous and nonlocal strain debt are especially likely to erase leverage before a real endpoint gain appears.

Its strongest repair ideas were still valuable and have been imported:

- freeze one named baseline criterion before claiming novelty;
- require one minimum quantitative gain threshold;
- reject any surviving lemma that is just the original regularity problem in compressed form.

## Merge Policy Applied To The Winner

The winning chain is not plain Chain 03. It is Chain 03 with the following hardenings:

- Tao sensitivity must be calibrated up front with one pass and one fail case.
- A candidate must beat or genuinely sharpen one frozen baseline criterion.
- The endpoint bridge must contain a benchmarked quantitative gain, not just descriptive cascade language.
- Any final positive route must isolate a first missing lemma that is strictly narrower than the full problem.

## Final Rationale

If the task is to pick the single chain most worth executing now, the right choice is the **energy-helicity route with an early coercivity gate**, not the broader triage protocol and not the more fragile material-variable route.

This choice maximizes the chance of getting a genuinely presentable result while still preserving enough novelty to justify the run. It also fails well: even a negative outcome should yield a precise theorem-facing obstruction rather than another attractive but weak reformulation memo.

### Winning Chain

# Canonical Chain - Coupled Energy-Helicity Route With Early Coercivity Gate

## Central Premise

This branch is live only if full 3D energy-helicity transport yields more than exact cascade bookkeeping.

The default hypothesis is negative: exact energy-helicity coupling is **non-coercive** for theorem-facing purposes unless the chain can exhibit one coupled quantity or forbidden transfer pattern that:

- is one-sided or coercive enough to matter;
- survives mixed-helicity restoration and low-helicity regions;
- survives the localization needed by the target endpoint;
- beats or genuinely sharpens one frozen baseline criterion;
- depends on an NS-specific feature that Tao-style averaging destroys; and
- reaches a named bad term or bad transfer pattern inside an actual endpoint-facing argument.

If those conditions fail, the correct output is a calibrated obstruction memo, not a positive invariant narrative.

## Verifiable Result Target

Either:

- one proposition-scale conditional statement tying a specific coupled energy-helicity quantity or forbidden transfer pattern to one named continuation, concentration-exclusion, or stretching/enstrophy bottleneck, together with one benchmarked gain and one genuinely narrower missing lemma; or
- one calibrated obstruction memo showing that the route fails by non-coercivity, mixed-helicity restoration, low-helicity escape, localization collapse, prior-art collapse, baseline non-improvement, or a stacked combination of these.

## Scope Lock

Before substantive execution begins, fix all of the following:

- one provisional endpoint family at the level of burden type:
  continuation criterion,
  concentration exclusion,
  or stretching/enstrophy bottleneck;
- one invariant package to audit first:
  coarse-grained local balances,
  dyadic coupled fluxes,
  or one other sharply defined ledger;
- one exact Tao-sensitive feature to test in advance;
- one frozen baseline criterion that the route must beat or genuinely sharpen;
- one minimum quantitative gain threshold that still matters after localization, pressure, viscosity, and mixed-helicity debt are paid;
- one admission rule:
  no candidate is promoted unless it names one one-sided gain on one named bad term or bad transfer pattern;
- one novelty rule:
  favorable same-helicity or polarized sectors do not count unless they carry a quantitatively relevant portion of the full burden near the chosen endpoint family; and
- one passing and one failing Tao-calibration example.

If these cannot be fixed concretely, stop and write a setup obstruction.

## Ordered Steps

### Step 1 - Calibrate the invariant package and Tao discriminator

- Depends on: none.
- Action: write the exact energy and helicity transfer identities in the chosen package, separating exact structure from bookkeeping choices.
- Action: define the Tao-sensitive feature in advance and state exactly what it means for averaging to destroy it.
- Action: give one worked example that clearly passes the Tao screen and one that clearly fails.
- Action: screen immediately for prior-art overlap with Waleffe-type triad analysis, helical decimation, shell-model intuition, and same-helicity favorable-sector lore.
- Expected output: an audit memo listing exact structure, Tao calibration, and prior-art risk.
- Kill condition: if the Tao test cannot distinguish a real pass case from a real fail case, or if the package already collapses to known folklore or generic cascade language, stop and write an overlap or calibration obstruction.

### Step 2 - Run the coercivity gate before endpoint packaging

- Depends on: Step 1.
- Action: ask whether the chosen coupled quantity yields any one-sided, endpoint-relevant gain before absolute values, generic inequalities, or sign averaging erase it.
- Action: require that gain to point to one named bad term or bad transfer pattern:
  stretching production,
  enstrophy growth,
  concentration of active scales,
  or another precisely stated bottleneck.
- Action: keep at most two candidate gains, each stated in the same burden language as the frozen baseline criterion.
- Expected output: at most two candidate gains, each tied to one named bottleneck and one candidate quantitative benchmark.
- Kill condition: if no one-sided or exclusionary gain survives this gate, stop and write a non-coercivity obstruction.

### Step 3 - Pay the full-equation debt early

- Depends on: Step 2.
- Action: test each surviving candidate against mixed-helicity interactions, low-helicity regions, viscosity, and pressure as first-order constraints rather than late corrections.
- Action: state explicitly whether the candidate controls a non-negligible share of the full nonlinear burden or only a thin favorable sector.
- Action: reject any mechanism that works only in decimated, filtered, or strongly polarized regimes without a theorem-relevant burden estimate.
- Expected output: a full-equation viability ledger.
- Kill condition: if mixed-helicity restoration, low-helicity escape, viscosity, or pressure destroys the gain, stop and write the obstruction.

### Step 4 - Test localization and endpoint insertion with a benchmarked gain

- Depends on: Step 3.
- Action: insert the localization machinery required by the endpoint:
  cutoffs,
  local flux commutators,
  pressure terms,
  and coarse-graining losses.
- Action: write one explicit endpoint-facing inequality, exclusion statement, or contradiction line.
- Action: state the benchmark clearly:
  what burden is reduced,
  in what norm or scale,
  and by how much relative to the frozen baseline criterion.
- Action: require the Tao-sensitive feature from Step 1 to appear inside this endpoint-facing mechanism, not just in surrounding exposition.
- Expected output: a localization-and-insertion memo containing one explicit mechanism and one quantitative benchmark.
- Kill condition: if localization erases the gain, if the gain collapses to energy-only control, or if no benchmarked improvement over the baseline criterion can be written, stop and write a localization or no-bridge obstruction.

### Step 5 - Audit the remaining gap for genuine narrowness

- Depends on: Step 4.
- Action: if a positive route remains, isolate the first missing lemma.
- Action: test whether that lemma is strictly narrower than the full regularity problem in scale, norm strength, geometric scope, or burden share.
- Action: reject any missing lemma that merely restates full control of the original hard case in renamed language.
- Expected output: either one proposition-scale target with a genuinely narrower missing lemma or a calibrated obstruction stating the first honest failure.
- Kill condition: if the remaining gap is equivalent to the original problem, downgrade the branch to obstruction immediately.

### Step 6 - State the narrowest earned claim

- Depends on: Step 5.
- Action: if positive, write one proposition-scale conditional statement with:
  the endpoint,
  the coupled quantity,
  the exact gain,
  the localization assumptions,
  the benchmarked improvement over the baseline criterion,
  and the first genuinely narrower missing lemma.
- Action: if negative, write one obstruction memo with the narrowest honest labels:
  non-coercivity,
  mixed-helicity restoration,
  low-helicity escape,
  localization collapse,
  prior-art collapse,
  baseline non-improvement,
  or a stacked combination.
- Action: reject any final claim that merely says helicity is interesting, or that assumes a persistently polarized regime strong enough to encode the hard case away.
- Expected output: a final-comparison-ready positive route or a sharp no-go.
- Kill condition: if the final claim hides the main difficulty inside the hypothesis or conclusion language, narrow it until the debt is explicit.

## Success Standard

This chain succeeds only if it does one of two things:

- isolates one coupled energy-helicity mechanism that is one-sided enough, localizable enough, Tao-sensitive enough, and endpoint-relevant enough to earn a serious conditional proposition; or
- shows cleanly that the exact coupled invariant geometry is too non-coercive or too fragile under full-equation restoration and localization to improve on the frozen baseline criterion.

## Presentable-Result Assessment

Estimated probability of a presentable result: **high**, with the most likely output being a strong obstruction memo rather than a positive theorem route.


## Latest Step Results

# Step 011 Results

## Step Verdict

- **Classification:** `setup obstruction, branch should stop before coercivity gate`
- `[VERIFIED]` Kill condition fired.
- `[VERIFIED]` The branch cannot freeze the scope lock concretely enough for
  Step 2 because the record never supplies:
  - one exact baseline cash-out in theorem-facing burden language;
  - one minimum quantitative gain threshold in that same currency;
  - one named bad term / bad transfer pattern tied to an explicit
    stretching/enstrophy inequality or exclusion line.
- `[VERIFIED]` Secondary failure labels also apply:
  `calibration obstruction` and prior-art-adjacent `exact-but-noncoercive`
  structure.
- `[VERIFIED]` The branch should **not** continue into coercivity testing.

## Scope-Lock Sheet

| Item | Result |
| --- | --- |
| Endpoint family | `[INFERRED]` Freezeable only provisionally as `stretching/enstrophy bottleneck`. |
| Invariant package | `[INFERRED]` Freezeable only provisionally as `dyadic coupled fluxes`, with the warning that the exact ledger actually lives at the helical-triad core. |
| Tao-sensitive feature | `[INFERRED]` Exact packet-level rigidity: role-labeled helical packets with mandatory conjugate completion, frozen sign/phase sheet, and unavoidable spectator leakage. |
| Baseline criterion | `[VERIFIED]` **Not frozen concretely enough.** Only burden-language survives: “beat the default exact-but-noncoercive stretching/enstrophy bottleneck by one one-sided gain on a named bad term.” |
| Minimum gain threshold | `[VERIFIED]` **Not frozen concretely enough.** Only “strict positive margin after localization, pressure, viscosity, and mixed-helicity debt” is supported. |
| Admission rule | `[PROPOSED]` No candidate survives unless it names one dyadic/packet transfer object, one named stretching/enstrophy burden, one one-sided gain, and one declared burden share that survives Tao, localization, pressure, viscosity, and mixed-helicity restoration. |
| Novelty rule | `[PROPOSED]` Same-helicity or polarized sectors do not count unless packet-complete and burden-relevant after mixed-helicity restoration. |

- `[VERIFIED]` Scope lock is therefore narrowed but not actually frozen.

## Invariant Identity Memo

- `[VERIFIED]` The strongest exact on-disk law is the Fourier/Leray evolution:

  ```text
  ∂t û(k) + |k|^2 û(k)
    = -i ∑_{p+q=k} (q·û(p)) P_k û(q),
  P_k = I - (k⊗k)/|k|^2,
  û(-k) = overline{û(k)}.
  ```

- `[VERIFIED]` Exact structure supported on disk:
  - full triad sum `p + q = k`;
  - exact Leray projection;
  - forced conjugate completion from real-valuedness;
  - helical-triad coefficient rigidity and energy/helicity conservation
    constraints.
- `[INFERRED]` Exact dyadic energy/helicity fluxes are therefore available only
  as an aggregation of this exact helical-triad core.
- `[VERIFIED]` The repository does **not** contain a standalone exact dyadic
  energy/helicity identity sheet for this branch.
- `[VERIFIED]` Bookkeeping choices rather than exact structure:
  dyadic shell grouping, packet role labels, helical basis convention, sign
  sheet, amplitude normalization, phase anchor, leakage window.
- `[INFERRED]` Nearest honest bad transfer pattern:
  a packet-complete delayed-threshold shell-bridging transfer pattern that
  would need to suppress a quantitatively relevant share of
  stretching production or enstrophy growth.
- `[VERIFIED]` That pattern is still only burden-language. No exact
  stretching/enstrophy cash-out is frozen.

## Tao Calibration Memo

- `[VERIFIED]` “Destroyed by averaging” is operational on this record:
  a feature counts only if it survives one fixed canonical packet sheet in
  exact NS but disappears when Tao-style averaged freedom restores independent
  role tuning and suppresses the exact spectator/conjugate constraints.
- `[VERIFIED]` Passing example:
  exact-NS helical packet rigidity with unavoidable same-scale, cross-scale,
  and conjugate spectator couplings.
- `[INFERRED]` Why it passes:
  Tao’s delayed-threshold circuit needs independently tunable weak pump, tiny
  seed, strong amplifier/rotor, and delayed next-shell pump, while exact NS
  supplies one rigid quadratic law plus forced extra couplings.
- `[VERIFIED]` Failing example:
  generic same-helicity / shell-model favorable-transfer folklore.
- `[INFERRED]` Why it fails:
  it remains sparse or polarized packaging without the full five-part Tao role
  hierarchy and without a uniquely NS-specific destroyed feature.
- `[VERIFIED]` The Tao screen is now operational as an admission filter.
- `[VERIFIED]` It does **not** produce a coercive gain or rescue the branch
  from non-coercivity.

## Prior-Art Overlap Memo

| Family | Verdict |
| --- | --- |
| Waleffe-type triad analysis | `[VERIFIED]` Strong overlap at the exact-ledger level. The branch’s sharpest exact content is still helical-triad coefficient rigidity and conservation. |
| Helical decimation | `[VERIFIED]` Strong overlap risk. The branch avoids total collapse only because it insists on packet completion and mixed-helicity restoration. |
| Shell-model intuition | `[VERIFIED]` Comparator only. It does not yield a theorem-facing NS gain here. |
| Same-helicity favorable-sector lore | `[VERIFIED]` Still a novelty trap unless it carries a quantitatively relevant full-burden share, which the record does not show. |

- `[INFERRED]` The package is not pure repackaging because one narrow
  packet-level Tao discriminator survives.
- `[VERIFIED]` It is still too prior-art-adjacent and too non-coercive to
  justify Step 2.

## Recommendation

- `[VERIFIED]` Do not run the coercivity gate.
- `[VERIFIED]` No Step-2 package is frozen.
- `[VERIFIED]` The narrowest honest mission output from this step is:
  `the coupled energy-helicity route narrows to a packet-complete helical-triad Tao discriminator, but fails the setup gate because its baseline cash-out, gain threshold, and theorem-facing bad term never freeze in the same burden currency.`

## Source Map

### Planning-run evidence

- `missions/beyond-de-giorgi/steps/step-011/GOAL.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/selected/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/attacks/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/judgments/chain-03.md`
- `missions/beyond-de-giorgi/planning-runs/run-007/final-decider.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-017.md`

### Prior mission / library evidence

- `runtime/results/codex-patlas-standalone-20260331T182129Z-receptionist-83682.md`
- `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`

### New synthesis created in this step

- `missions/beyond-de-giorgi/steps/step-011/explorations/exploration-001/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-011/explorations/exploration-002/REPORT.md`
- `missions/beyond-de-giorgi/steps/step-011/explorations/exploration-003/REPORT.md`

## Kill-Condition Note

- `[VERIFIED]` The step counts as a successful bounded negative result.
- `[VERIFIED]` Kill conditions triggered:
  - the scope lock could not be fixed concretely;
  - the branch would stay alive only by delaying the baseline criterion and
    gain threshold to later steps;
  - the package remained exact-but-noncoercive and prior-art-adjacent at the
    theorem-facing level.

