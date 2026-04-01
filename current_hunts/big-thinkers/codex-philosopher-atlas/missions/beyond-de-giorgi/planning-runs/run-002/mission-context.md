# Mission Context Snapshot

Mission: beyond-de-giorgi
Planning run: run-002
Timestamp: 2026-03-31T08:22:43Z

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


## Latest Step Results

# Step 1 Results — Exact Far-Field Obstruction Reconstruction And Tao Gate

## Completion Status

Step 1 is complete.

- Kill condition fired: **yes**
- Kill condition reason: no screened NS-specific ingredient currently shrinks the actual bad coefficient for the surviving far-field pairing, and the generic harmonic gains act only on already-killed modes or leave the coefficient at fixed energy scale.

## Source Basis

Primary copied sources used in this step:

- `missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/mission-context.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`

## Formula Sheet

- [VERIFIED] The exact far-field pressure pairing carried forward from the copied pressure dissection is

  `I_p^far = -∬ p_far div(v_k φ_k^2 ê)`.

- [VERIFIED] Expanding the divergence gives

  `I_p^far = -∬ p_far (ê·∇v_k) φ_k^2`
  `          - 2∬ p_far v_k φ_k (ê·∇φ_k)`
  `          - ∬ p_far v_k φ_k^2 div(ê)`.

- [VERIFIED] The dominant live term is

  `I_p^far,main = -2∬ p_far v_k φ_k (ê·∇φ_k)`.

- [VERIFIED] The operative inherited estimate is

  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`.

- [VERIFIED] The bad coefficient is

  `C_far ~ ||p_far||_{L^∞(Q_k)} ~ ||u||_{L^2}^2 / r_k^3`.

- [VERIFIED] Local pressure is not the obstruction; the copied prior mission already isolates it as closing superlinearly.

- [INFERRED] The localization/test structure already annihilates the constant pressure mode:
  if `p_far = c`, then `I_p^far = -c ∬ div(v_k φ_k^2 ê) = 0`.

- [INFERRED] Affine harmonic modes generally survive:
  if `p_far = a·x + c`, then `I_p^far = ∬ a·(v_k φ_k^2 ê)`, which has no general reason to vanish.

- [INFERRED] Higher harmonic modes also survive generically, because the pairing reduces to moments of `F_k = v_k φ_k^2 ê` against gradients of harmonic polynomials.

- [INFERRED] Therefore the only automatic quotient is by constants. Any claimed improvement that only controls oscillation modulo constants does **not** touch the live obstruction.

- [INFERRED] The quantity that would actually need to become smaller for progress is an effective coefficient for the **full** far-field pairing, for example

  `|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}`

  with `C_far,eff(k)` materially smaller than `||u||_{L^2}^2 / r_k^3` from admissible NS data.

## Tao-Gate Memo

What Tao's averaged model preserves for present purposes:

- [VERIFIED] energy identity / energy-class control
- [VERIFIED] divergence-free structure
- [VERIFIED] standard Calderon-Zygmund, Littlewood-Paley, Sobolev, and generic harmonic-analysis estimates

Candidate list and verdicts:

- [INFERRED] Exact algebraic form of `u · ∇u`: **fails Tao gate** for this branch.
  Reason: after localization the live issue is the harmonic-tail pressure pairing, and no estimate was found showing that the raw algebraic form shrinks the surviving affine-or-higher pressure moments behind `C_far`.

- [INFERRED] Pressure-Hessian / tensor structure tied to `∂_i∂_j p = R_i R_j(u_i u_j)`: **unclear but testable**.
  Reason: this is the only candidate naturally attached to the pressure-side object itself, but in the current record it remains a representation-level possibility, not an estimate-level mechanism on the bad coefficient.

- [INFERRED] Vorticity / strain geometry, restricted to this pressure pairing: **fails Tao gate** for this branch.
  Reason: geometry may matter elsewhere, but no direct route was found from local geometry to shrinkage of the nonlocal far-field coefficient generated by remote shells.

Verdict:

- [VERIFIED] Generic harmonic-tail regularity fails the Tao gate.
- [INFERRED] No candidate earned `survives Tao gate`.
- [INFERRED] The harmonic-tail pressure loophole is therefore Tao-compatible in every nontrivial form currently supported by the copied mission evidence.

## Execution Recommendation For Step 2

- [VERIFIED] Do **not** green-light a broad remote-shell falsification program as the next step in this harmonic-tail branch.
- [INFERRED] Immediate recommendation: downgrade to the negative-result track.
- [PROPOSED] Preserve only one narrow follow-up question, and only if it is treated as a different tensor-focused branch rather than a continuation of harmonic-tail norm-shopping:
  can the exact pressure-tensor structure force cancellation in the remote-shell moments that generate the affine-or-higher harmonic tail on the inner cylinder?

## Honest Bottom Line

- [VERIFIED] The far-field pairing is now pinned down explicitly.
- [VERIFIED] The live obstruction is coefficient-side.
- [INFERRED] The surviving far-field issue is already a moment problem for affine-or-higher harmonic content, not a problem of constants or generic harmonic smoothness.
- [INFERRED] This step succeeded by closing the branch negatively and sharply, which is an allowed success state under the mission chain.

