# Current Status of Navier-Stokes

Canonical top-level status file for the Navier-Stokes regularity effort in `big-thinkers/research-systems/`.
If other NS summary docs disagree with this file, treat this one as authoritative.

This is the top-level aggregated status memo for the 3D Navier-Stokes regularity effort across:

- `research-systems/atlas`
- `research-systems/codex-atlas`
- `research-systems/philosopher-atlas`
- `research-systems/codex-philosopher-atlas`
- `research-systems/codex-nexus`

It is meant to answer one practical question:

```text
after all completed missions so far, what do we actually know, what is closed,
and what is still even faintly worth trying?
```

It supersedes older summary/planning docs, especially:

- `docs_and_guides/NS-REGULARITY-WHAT-WE-KNOW.md`
- `docs_and_guides/current-NS-status-and-plan.md`

## Executive Bottom Line

The project has produced several strong negative results and a few durable structural findings, but it has **not** yet identified a credible proof path to the Millennium Prize.

The current picture is:

- Enstrophy-based regularity routes are obstructed by a logical circle around the BKM criterion.
- De Giorgi / Vasseur pressure improvement is closed within that framework: `beta = 4/3` is sharp.
- The epsilon-regularity family appears structurally capped in the same way.
- The `H^1` pressure route is dead at the `W^{1,3}` wall.
- The harmonic far-field pressure loophole is closed.
- Tao's averaged-NS blowup has been reconstructed mechanistically, but no concrete exact-NS firewall theorem has emerged.
- The clean exact Tao-circuit object is structurally impossible, trigger-focused narrowing does not rescue it, the first concrete clustered exact-mode packet model fails canonicity, and a follow-up anti-circuit expansion restatement also fails to reach an intrinsic theorem object.
- A newer exact near-circuit screening branch did better than the older packet lines: it froze one canonical one-bridge helical screening ledger and promoted repaired `Template-Defect Near-Closure` and repaired `Windowed Spectator-Leakage Budget`, but the carried constructive follow-through then stopped at Step 8 with `exact non-isolability / arbitrary-truncation requirement` and at Step 9 with a `source-basis / no-canonical-finite-reduction` memo because no same-currency explicit realization or finite-closure convention is frozen.
- The first intrinsic phase-locking / coherence firewall branch also sharpened the frontier: it froze a genuinely intrinsic triad-phase object, but its first three finite recursively closed support budgets all failed by forced spill, so no tiny finite-support phase-locked exact subsystem survived.
- A second intrinsic phase/coherence attempt in `codex-atlas` also closed negatively: a definable interface transfer-coherence ratio survived the object gate, but it was too tautological on one triad and too weak on the first nontrivial two-input exact cluster.
- A physical-space hidden-precursor branch also closed negatively: it found a real event object, but the strongest precursor pair failed because the exact balance law has no backward-memory term.
- A small exact-helical sign-defect prototype gave a real mechanistic clue, and the latest follow-up sharpened that into an exact functional package on a fixed sign-sensitive ledger with `SD_target` as the primary load-bearing sign quantity, but the line still failed at theorem-object stage because the ledger extraction remains non-canonical.
- A broad April 2, 2026 angle search outside the Tao-adjacent family selected the strain-vorticity `e_2`-alignment GMT approach as the most promising novel direction, confirmed the alignment mechanism in exact solutions (Burgers vortex, Lamb-Oseen), proved a new conditional regularity theorem (Theorem C3), but reached a terminal structural obstruction: `s_2 > 0` universally in high-vorticity regions, and `e_2`-alignment removes the feedback that could reverse it. The GMT dimensional-reduction component was separately killed (superlevel sets have full Hausdorff dimension).

So the overall status is:

```text
many natural routes are now closed;
the Tao-adjacent frontier has narrowed further:
a canonical packet model is still the missing object in principle,
the first concrete clustered exact-mode packetization has already failed,
and even an exact-hypergraph anti-circuit restatement still needs non-intrinsic
role and desired-channel annotation. The newer exact near-circuit branch did
freeze two honest downstream packet screens on one canonical one-bridge
helical ledger, and the carried witness `F_SS(1/12)` can now be frozen on the
repaired authority sheet in the same comparison currency. But the constructive
follow-through has now also stopped honestly: Step 8 reaches only classwise
exact non-isolability / arbitrary-truncation requirement, Step 9 stops again
at source-basis / no-canonical-finite-reduction because there is still no
promoted same-currency explicit realization, exact coefficient ledger, or
finite-closure convention, and the latest explicit one-bridge bridge attempt
only narrows that realization gap partially without rescuing the branch. The
first intrinsic phase-locking branch then improved the object-definition side
but still failed to find a tiny finite exact subsystem: one-triad, two-triad
shared-mode, and three-triad single-repeated-orbit budgets all spill under
honest recursive closure. So any remaining packet route now has a sharper
split: either upgrade the frozen template-defect or leakage screens into real
packet-family theorems, or freeze a same-currency explicit realization
protocol that can survive exact closure bookkeeping without ad hoc repair. The
helical sign clue remains informative at the level of fixed-ledger mechanism
and suggests `SD_target` is the sharper sign quantity, but it is still not a
theorem-facing packet program until a substantially more intrinsic object class
or extraction rule is found.
```

## Durable Findings

### 1. Inequality-slack atlas: the loosest classical bound is known

From `atlas` / `codex-atlas` Navier-Stokes slack missions:

- The vortex stretching bound is the loosest major estimate in the standard regularity chain, with measured slack on the order of `237x`.
- The dominant source of that slack is the Ladyzhenskaya interpolation chain, not geometric alignment alone.
- A BKM-style enstrophy bypass sharply improves the numerical bound, but it does **not** break the deeper obstruction.

Durable interpretation:

- Better constants in classical enstrophy estimates are interesting and sometimes novel.
- They do not, by themselves, produce a path to full regularity.

### 2. The enstrophy route hits a logical circle

From `atlas` / `codex-atlas` Navier-Stokes missions:

- Any attempt to close regularity through enstrophy growth eventually reduces to controlling `||omega||_{L^infty}`.
- But that is exactly the Beale-Kato-Majda criterion, which is essentially equivalent to regularity.

Durable interpretation:

- Enstrophy-based regularity is not just hard; it is structurally self-referential.
- This makes the route a bad primary candidate for a proof unless some new ingredient bypasses the `L^infty` bottleneck entirely.

### 3. The Vasseur / De Giorgi pressure gap is closed negatively

From `atlas` / `codex-atlas` Vasseur-pressure missions:

- The target gap was `beta = 4/3` versus the `beta > 3/2` threshold needed for full regularity inside Vasseur's framework.
- The completed missions show that `beta = 4/3` is sharp within the De Giorgi–Vasseur architecture.
- This is not just a Calderon-Zygmund artifact: multiple analytical tools collapse to the same ceiling or worse.
- The one-line constant-field extremizer confirms the final Chebyshev step is tight.

Durable interpretation:

- The De Giorgi pressure-improvement program is exhausted as a proof route.
- Any future progress would have to leave that framework or introduce a genuinely different structural object.

### 4. The universal De Giorgi scaling picture is now explicit

From `atlas` / `codex-atlas` Vasseur-pressure synthesis:

- The recurrence exponent is best understood through the formula `beta = 1 + s/n` for De Giorgi iteration on dissipative PDEs with `H^s` diffusion in dimension `n`.
- For 3D Navier-Stokes this gives `1 + 1/3 = 4/3`, exactly the observed ceiling.
- The full-regularity threshold inside the Vasseur program is `beta > 3/2`, so the gap is the same as the gap between `s/n = 1/3` and `s/n = 1/2`.

Durable interpretation:

- This makes the obstruction feel dimensional/structural rather than accidental.
- It is one of the clearest reasons the De Giorgi route now looks fundamentally mismatched to 3D NS.

### 5. The epsilon-regularity family shares the same structural ceiling

From `codex-philosopher-atlas` and later carry-forward summaries:

- CKN, Lin, and Vasseur-style epsilon-regularity arguments reduce to the same covering architecture.
- The usual `dim <= 1` singular-set outcome is structural in that family, not just a feature of one proof presentation.

Durable interpretation:

- "Partial regularity plus epsilon-bootstrapping" should be treated as closed by default.
- It only reopens if the bootstrap uses a genuinely new mechanism outside the familiar epsilon-regularity family.

### 6. The `H^1` pressure route is dead

From `philosopher-atlas` and `codex-philosopher-atlas` Vasseur-pressure missions:

- The pressure does have `H^1` structure from compensated compactness.
- But every tested route runs into the same structural barrier: `W^{1,2}` is what Leray-Hopf gives, while the hoped-for improvements require `W^{1,3}`-level control.
- `H^1`-BMO duality does not rescue the argument.
- Atomic decomposition and interpolation do not rescue it either.
- The local/far-field split is sharp in this lane: local pressure closes, far-field pressure is the only obstruction.

Durable interpretation:

- The `H^1` pressure idea is not just unfinished; it is structurally blocked.
- The most important surviving lesson from that branch was the identification of the far-field pressure as the sole remaining pressure-side obstruction.

### 7. The harmonic far-field pressure loophole is closed

From `codex-atlas` far-field-pressure-harmonic-loophole mission:

- The literal Vasseur bottleneck is the local term `P_{k21}`, not the already-favorable harmonic term `P_{k1}`.
- So the only remaining loophole was whether some alternative near/far split could move the dangerous interaction into a harmonic far-field piece.
- That route failed.
- Harmonicity alone does not create the needed `U_k`-dependence; constant and affine harmonic modes still let the pairing be controlled by exterior data instead of local De Giorgi mass.

Durable interpretation:

- Harmonic far-field structure improves oscillation and smoothness, but not the coefficient mechanism needed to beat `beta = 4/3`.

### 8. Tao's averaged blowup is now understood mechanistically

From `codex-atlas` anatomy-of-averaged-ns-blowup-firewall mission, plus `codex-philosopher-atlas` Tao-circuit feature ledgers:

- Tao's averaged-NS blowup is not just a generic high-frequency cascade.
- It is best understood as a five-mode delayed-threshold circuit embedded in a shell cascade.
- The tiny trigger variable is dynamically central.
- The load-bearing issue is isolated gate logic, not just forward transfer of energy.

Durable interpretation:

- This was real progress in understanding the obstruction landscape.
- It turned Tao from a black-box barrier theorem into a specific mechanism target.

### 9. Exact rewrites and standard host-space escapes were audited and closed

From `codex-philosopher-atlas` beyond-De-Giorgi audits:

- The main exact rewrites were tested directly:
  - divergence/stress form
  - Lamb-vector / Helmholtz-projected form
  - vorticity / Biot-Savart form
- None of them produced a smaller coefficient on the fixed localized bad term after localization debt was restored.
- Standard compactness-rigidity host spaces such as `L^3`, `\dot H^{1/2}`, and `BMO^{-1}` also failed to supply a viable NS-specific extraction package.

Durable interpretation:

- Merely rewriting the equation in an exact but equivalent form is not enough.
- The still-missing object is not "another formulation" but a formulation that creates a theorem-facing one-sided gain, and no standard host space has yet supplied that either.

### 10. No exact-NS firewall has yet survived Tao comparison

From `codex-atlas` Tao follow-up missions:

- The strongest candidate firewall was exact-NS circuit non-isolability.
- But that never sharpened into a theorem-facing inequality, invariant, or dynamical constraint.
- The crisp singleton-support exact Tao-circuit object then failed immediately under triad-closure geometry.
- A trigger-focused narrowing failed too: once made faithful, it collapsed back to the same five-role object.
- Packetized replacements remain too non-canonical.

Durable interpretation:

- The Tao branch has been informative, but not yet constructive.
- The branch is not dead in principle, but it is blocked at the level of object definition rather than at the level of one more estimate.

### 11. The first concrete clustered exact-mode packet model failed canonicity

From the `codex-nexus` packet-model bootstrap:

- The theorem-object bottleneck was sharpened into an explicit ledger:
  - singleton exact circuit failure
  - trigger-focused failure
  - mechanism-level non-isolability intuition with no theorem object
- A first concrete candidate packet family was then tested:
  - deterministic dyadic-helical triad packets on `T^3`
- That candidate failed the first canonicity gates:
  - partition robustness fails because refinement runs back into the already-impossible singleton exact circuit
  - tie-breaker robustness fails because symmetry-related seeds require arbitrary coordinatization choices
  - support stability fails because packet boundaries are not canonically fixed
  - desired-channel bookkeeping and leakage scalarization are not invariant under admissible packet changes

Durable interpretation:

- It is no longer enough to say only "define a canonical packet model."
- The first concrete clustered exact-mode packetization has already failed, so any remaining packet route would need a fundamentally different object class than "cluster exact modes and then annotate desired channels."
- A secondary live option is to turn this negative result into a broader no-go statement for that whole packetization family.

### 12. The anti-circuit expansion restatement is blocked at theorem-object stage

From the `codex-nexus` anti-circuit scope mission:

- The repository now supports naming a sharper exact substrate for Tao-adjacent discussion:
  - the ordered helical triad interaction tensor, or equivalently its weighted oriented `3`-uniform hypergraph shadow
- That is a real exact object and is cleaner than clustered packets at the substrate level.
- But the hoped-for Tao-specific anti-circuit quantity still cannot be stated intrinsically on that object.
- A generic escape-rate / conductance ratio can be written for arbitrary mode sets.
- The moment one asks for the Tao-like five-role community and its desired-versus-spectator internal motifs, one reintroduces non-intrinsic role and desired-channel annotation.

Durable interpretation:

- This blocks a whole style of "just phrase non-isolability as hypergraph expansion" move unless the role-community can be extracted intrinsically from the exact transfer tensor.
- The result is genuinely sharper than the packet failure alone, because it shows that even an exact hypergraph substrate does not by itself solve the theorem-object problem.

### 13. Physical-space hidden-precursor observability also failed

From `codex-atlas` hidden-precursor firewall mission:

- A faithful exact-NS physical-space delayed-transfer event was successfully defined using a localized coarse-grained forward-flux burst plus a narrow subscale witness channel.
- The strongest surviving precursor pair was earlier cumulative positive forward flux on the predecessor cylinder for the same scale interface.
- That branch still failed, for a structural reason: the exact filtered-energy balance is too time-local and provides no backward-memory term linking the earlier precursor slab to the later burst window.

Durable interpretation:

- This is stronger than a mere definition failure. A genuine physical-space event object exists.
- But the first plausible precursor theorem candidate already dies on the exact identity structure, so hidden-precursor observability is not currently a live firewall route without extra temporal-memory structure.

### 14. A first exact-helical sign-defect prototype supports a sharpened packet route

From `simulation-machines-attempts` helical sign-defect prototype follow-up:

- On the existing exact five-role singleton helical support audit, the lowest-leakage nontrivial sign patterns are the most globally near-homochiral ones.
- But the only surviving desired activation triad on that audit support, `a1 + a3 -> a4`, is nonzero only in heterochiral sign configurations.
- The fully homochiral sign assignments kill the desired drive entirely on that support.
- A first packet-stage stress test then split into two contrasting non-singleton lifts:
  - a shell-sign nearest-anchor lift was too crude and drove leakage sharply upward,
  - but a source-incidence lift activated several desired packet edges, reduced leakage substantially relative to the singleton baseline, and still kept the desired-edge heterochirality defect `SD_target` large.
- A broader adversarial search across all 32 core sign patterns inside the same one-step external-closure class then materially weakened the first stronger slogan:
  - the globally lowest-leak families in that searched class came from fully homochiral cores, with `Leak ≈ 7.19` and still substantial but no longer extreme `SD_target ≈ 0.762`,
  - minority-count-2 cores could push `SD_target` much lower than the single-pattern search suggested, reaching `SD_target ≈ 0.509` at `Leak ≈ 14.83`,
  - but in the stricter near-isolated regime the searched class still kept a meaningful heterochiral dependence: the best global values found were about `SD_target ≈ 0.699` under `Leak <= 8`, `0.613` under `Leak <= 10`, and `0.571` under `Leak <= 12`.
- This does **not** rescue the singleton route; that route remains closed negatively for earlier structural reasons.

Durable interpretation:

- The value here is mechanistic, not theorem-level.
- It is concrete exact-ledger evidence that a sign-sensitive packet route may still say something sharper than pure leakage minimization alone, but the effect is weaker and more threshold-sensitive than the first single-pattern search implied.
- The plausible next object is therefore not a single vague `SignDefect`, but a packet-level pair:
  - global minority-helicity participation on the active packet ledger
  - heterochiral dependence of the load-bearing Tao-like target edges
- The global minority-helicity quantity should be defined on a conjugate-pair representative quotient, not by counting both members of the raw sign-closed support, or else the sign balance trivializes.
- The current exploratory emphasis shifts again after the global scan:
  - `SD_part` still carries some signal, but `SD_target` remains the more decision-relevant quantity.
  - the broad claim "no low-leak / low-`SD_target` family appears" is too strong on the searched class.
  - the only empirically honest theorem-shaped remnant is a stricter-threshold envelope inside that restricted family class, closer to "for genuinely low leakage, `SD_target` stays bounded away from `0`."
  - because the packet object is still non-canonical, this branch remains a mechanism probe, not the main theorem object; the cleaner prize-facing next work still sits with the two frozen exact packet screens or with a more intrinsic non-packet object class.

### 15. The sign-sensitive packet-functional route sharpened, but still failed at theorem-object stage

From the helical sign-defect prototypes and the `codex-nexus` sign-sensitive packet-functional mission:

- The sign-sensitive follow-up split the hoped-for obstruction into
  - global minority-helicity participation `SD_part`,
  - desired-edge heterochirality defect `SD_target`.
- The best honest local object was sharpened from "some packet model" to a fixed sign-sensitive packet ledger on the exact helical triad substrate.
- On that fixed ledger, the route now supports a coherent exact functional package:
  - `Drive_target`
  - `Leak`
  - `SD_part`
  - `SD_target`
- The direct follow-up result is that `SD_target`, not `SD_part`, is the primary load-bearing sign quantity:
  - the singleton audit already forced the desired activation edge to be heterochiral,
  - and the first better non-singleton source-incidence lift kept `SD_target` large while lowering leakage.
- This does **not** solve the theorem-object problem.
- The functionals are exact only after a role-labeled packet ledger has been fixed, while the repository still lacks a canonical extraction rule producing that ledger from exact NS data.
- The current best exploratory lift remains heuristic, so the route still inherits non-intrinsic packet/object debt.

Durable interpretation:

- This is a real sharpening of the sign-sensitive line, not just repetition.
- It upgrades the helical sign clue from slogan to a conditional exact functional package on a fixed ledger.
- But it also clarifies the failure mode: the route is blocked not because the sign package is empty, but because the packet ledger still is not intrinsic.
- The best current theorem-shaped target in this language is only conditional, something like
  `Drive_target >= d0` and `canonical ledger` implying `Leak + lambda * SD_target >= c0`.
- So the helical sign clue should still be treated as mechanistic evidence, not as a live theorem program in packet language unless a substantially more intrinsic extraction rule or object class is found first.

### 16. The exact near-circuit screening branch now freezes a real authority sheet, then stops honestly on exact closure / source-basis grounds

From `codex-philosopher-atlas` exact-ns-no-near-closed-tao-circuit:

- Steps 1 through 6 did something genuinely new for this repo family:
  they froze one canonical one-bridge role-labeled helical packet ledger,
  killed the behavior-side alternatives,
  and promoted two exact downstream packet screens with repaired thresholds,
  packet semantics, canonicalization policy, invariant gates, and named exact
  follow-on questions:
  - repaired `Template-Defect Near-Closure`
  - repaired `Windowed Spectator-Leakage Budget`
- Step 7 then sharpened the branch further instead of merely summarizing it:
  it froze the carried witness to the single point `F_SS(1/12)` on that same
  ledger, fixed the repaired authority sheet for `G_tmpl` and `G_leak`, and
  made the later `L_cross <= 1/24` repair controlling rather than treating the
  older `1/12` helper entries as live alternatives.
- Step 8 is where the constructive follow-through first stops honestly:
  on the frozen ledger, exact closure can be stabilized only at the
  interaction-class level, not as one finite exact closed subsystem, so the
  sharpest earned verdict is
  `exact non-isolability / arbitrary-truncation requirement`.
- Step 9 then tries to reopen the same chain through provenance discipline and
  stops again:
  there is still no promoted same-currency explicit wavevector family,
  no fixed helicity tuple,
  no exact desired/forced coefficient ledger,
  no theorem-facing exceptional-set sheet,
  and no finite-closure convention.
  The sharpest honest verdict there is
  `source-basis / no-canonical-finite-reduction memo`.
- A local April 2, 2026 bridge attempt did partially narrow that gap:
  it exhibited one explicit singleton helical realization candidate on the
  same role currency and recovered part of the desired witness pattern.
  More specifically, it realizes `A_n + C_n -> D_n` exactly and recovers the
  return leg only after a conjugate adjustment, but it still misses
  `A_n + A_n -> B_n`,
  `A_n + A_n -> C_n`,
  `B_n + C_n -> C_n`,
  and `D_n + D_n -> E_n`
  on the same exact support and immediately emits large external terms, so it
  does not rescue the constructive branch.
- A second April 2, 2026 continuation then removed the obvious
  "maybe another sign sheet fixes it" escape hatch on that same explicit
  singleton family:
  an exhaustive scan over all `5! * 2^5 = 3840` role permutations and helicity
  assignments on the old five-vector support never realizes more than `1 / 6`
  desired Step-7 pairs exactly, never realizes more than `2 / 6` even after
  allowing conjugate-adjusted hits, and only the
  `C_n + D_n -> A_n`
  and
  `A_n + C_n -> D_n`
  pairs appear anywhere in the full search.
  The same continuation also makes the singleton arithmetic obstruction
  explicit:
  `A_n + A_n -> B_n` and `A_n + A_n -> C_n` force `k_B = k_C = 2 k_A`,
  `B_n + C_n -> C_n` forces `k_B = 0`,
  and exact activation together with exact return forces `2 k_C = 0`.

Durable interpretation:

- This is still the first Tao-adjacent exact-NS branch in the repo family that
  froze promoted exact packet-level objects instead of dying immediately at
  object definition, and Step 7 made that branch much cleaner by freezing one
  witness-local authority sheet on one canonical ledger.
- But it is now equally important that the later carried chain has already
  stopped twice on the same record.
  The obstruction is no longer vague "packet ambiguity"; it is the absence of
  one promotable same-currency explicit realization/closure protocol.
- So the exact Tao-adjacent frontier now has a sharper split than before:
  one line tries to prove honest packet-family theorems from the frozen
  template-defect and leakage screens,
  while another line would have to earn a same-currency explicit realization
  protocol before any exact reduced dynamics or recursive closure claim can be
  treated seriously.

### 17. The first intrinsic phase-locking firewall froze a real object but failed on the first three finite-support budgets

From `codex-philosopher-atlas` exact-ns-phase-locking-firewall:

- The mission did **not** die at definition level.
- Step 1 froze a genuinely intrinsic candidate object:
  the coefficient-corrected exact triad-phase orbit measure on a closed
  helical support ledger, while scalar aggregate coherence scores were demoted
  to diagnostic-only status.
- The mission then ran the smallest-first exact support search with recursive
  closure and admissible-enlargement audits.
- The first three budgets all closed negatively:
  - one-triad seeds all spilled once mandatory conjugate completion and full
    active-ledger closure were enforced;
  - two-triad shared-mode families also spilled under cross-triad closure;
  - three-triad single-repeated-orbit families reduced to the canonical
    three-arm star and still spilled under honest closure.
- So the branch did earn a durable local negative:
  no tiny finite-support exact helical subsystem survived as a recursively
  closed carrier for the intrinsic phase object through those first three
  budgets.

Durable interpretation:

- This is stronger than "phase language was too vague." The intrinsic object
  itself survived the definition screen.
- What failed was the first concrete realization strategy:
  very small finite recursively closed supports do not appear capable of
  carrying the hoped-for phase-locking firewall.
- That shifts the burden of the phase route away from tiny closed mode packets
  and toward more distributed shell-interface or shell-crossing structures, if
  the route remains alive at all.

### 18. A second intrinsic phase/coherence branch died because the observable was too weak

From `codex-atlas` exact-ns-phase-locking-firewall:

- This mission also found a real intrinsic object after a narrow Phase 0 pass:

```text
C_ℓ(t) = (∑_{τ∈𝒯_ℓ} T_{τ,ℓ}(t)) / (∑_{τ∈𝒯_ℓ} |T_{τ,ℓ}(t)|),
D_ℓ(t) = 1 - C_ℓ(t),
```

  the exact transfer-coherence ratio on a sign-closed helical triad population
  across one smooth scale interface, with backup raw phase concentration
  observable `A_ℓ`.
- It paired that object with a clean delayed-transfer companion event
  `E_ℓ^transfer`.
- The route then died at the smallest honest exact-support audit:
  - on one active transfer term, `C_ℓ = ±1`, so the observable is tautological,
  - on the first nontrivial exact-helical two-input cluster, exact phase tuning
    keeps positive receiver gain while driving `C_ℓ` arbitrarily close to `0`.

Durable interpretation:

- This is a stronger negative than mere definition failure.
- It shows that even a genuinely intrinsic phase observable can still be too
  weak to function as a firewall.
- In particular, cancellation-ratio phase observables are a bad family for this
  pursuit unless they can survive the same one-triad / first-two-input-cluster
  adversarial screen.

### 19. Strain-vorticity e_2-alignment: confirmed mechanism, conditional regularity theorem, but structurally blocked for unconditional regularity

From the April 2, 2026 pursuit plan (10-angle exploration → Angle 10 selected → 5 subproblems pursued):

- **Ground truth confirmed (Subproblem A):** The DNS observation that vorticity
  aligns with the intermediate eigenvector `e_2` of the strain tensor is
  confirmed by exact Burgers vortex and Lamb-Oseen computations. A
  self-organization mechanism was identified: strong azimuthal vorticity
  rearranges the strain eigenvalue ordering, placing `omega` at `e_2`. The
  misaligned high-vorticity fraction vanishes as `Re^{-1}`.
- **Eigenvector regularity solved (Subproblem B):** Eigenvalue coalescence has
  codimension 2 (curves in `R^3`). The smooth Rayleigh quotient
  `Q = omega . S omega / |omega|^2` captures all stretching information with
  no eigendecomposition needed. `Q` is `C^infty` wherever `omega != 0` and
  satisfies a parabolic PDE derived from NS.
- **Conditional regularity proved (Subproblem C, Theorem C3):** If `omega`
  aligns with `e_2` at rate `delta(M) = O(M^{-1}(log M)^{-1})` AND
  `s_2 <= 0` on `{|omega| > M}`, then the solution remains regular. This is
  incomparable with Constantin-Fefferman (local alignment condition vs. spatial
  Lipschitz condition on vorticity direction).
- **GMT dimensional reduction killed (Subproblem D):** The dangerous set
  `{|omega| > M, Q > epsilon}` has full Hausdorff dimension 3 even for passive
  vorticity with smooth drift. Seven independent GMT approaches all fail.
  Superlevel sets are not amenable to GMT dimension estimates.
- **s_2 dynamics killed (Subproblem E):** `s_2 > 0` in high-vorticity regions
  is confirmed by restricted Euler (with `s_2/s_1 -> 1` at blowup), DNS
  (`s_2/s_1 ~ 0.2-0.4` at all Re), pressure Hessian (moderates but does not
  reverse sign), and viscous analysis. The anti-alignment feedback: `e_2`-alignment
  suppresses the vorticity term `-(1/4)(omega_1^2 + omega_3^2)` in the `s_2`
  evolution to `O(delta^2 |omega|^2)`, removing the mechanism that could push
  `s_2` negative.

Durable interpretation:

- Alignment and positive `s_2` are inseparable consequences of vortex tube
  geometry: the eigenvalue reordering that creates `e_2`-alignment simultaneously
  makes `s_2` positive.
- `e_2`-alignment controls the direction of vortex stretching but not its
  magnitude. Regularity requires magnitude control, and `s_2 > 0` defeats it.
- The approach is structurally blocked, not just technically incomplete.
- Theorem C3 and the `Q` reformulation are the durable survivors and should be
  used in future strain-vorticity analysis.

A follow-up exploration of three surviving non-Tao directions then produced:

- **Direction 2 (pressure Hessian Q-self-damping) is dead.** The claimed
  `-|omega|^2/6` autonomous self-damping in the `Q`-evolution does not exist.
  The vorticity tensor contributes exactly zero (`Omega^2 omega = 0`). The
  `-|omega|^2/6` is actually the isotropic part of the pressure Hessian, which
  is anti-damping when `|S|^2 > |omega|^2/2` (the physically relevant regime).
- **Direction 1 (combined alignment + direction regularity) survives weakly**
  but the naive eigenframe-regularity route is circular: the CF Lipschitz
  constant diverges under Type I blowup scaling despite the growing spectral
  gap.
- **Direction 3 (vorticity-direction Lipschitz / DHY condition) survives weakly**
  and produced a concrete positive result: the Deng-Hou-Yu condition
  `|D_xi xi| bounded` was verified for the bent Burgers vortex tube, with
  `|D_xi xi| = kappa + O(kappa^2 r_c)` bounded uniformly in `Re`. The bound
  improves on higher-vorticity subsets. No `Re`-dependent amplification exists.
  This identifies **curvature of vortex lines** as the controlling quantity for
  the DHY condition.

The remaining gap for the vorticity-direction route is exactly: proving that
vortex-line curvature remains bounded on `{|omega| > M}` for general NS
solutions. This requires showing high-vorticity regions are approximately
tube-like, that tube-axis curvature stays bounded, and handling multi-tube
interactions — each of which is open and hard.

**Current sharpest frontier (April 2, 2026):** The curvature evolution equation
for `kappa = |D_xi xi|` has now been fully derived and analyzed. The result is
**Outcome 2 (ambiguous / strong structural evidence, no proof):**

- The evolution is: `D_t eta = P_perp(S eta) - 2Q eta + P_perp((D_xi S) xi) + V_nu`
- **Restricted Euler damps curvature.** At the Vieillefosse blowup attractor
  (`s_2/s_1 -> 1`), both eigenvalues of the linear operator are negative.
  Restricted Euler blowup straightens vortex lines — the opposite of DHY failure.
- **Hasimoto/NLS connection.** Curvature under LIA maps to 1D cubic NLS (globally
  well-posed), giving structural kappa boundedness for thin vortex filaments.
- **Curvature-viscosity feedback.** Large kappa directly enhances viscous damping
  of `|omega|` at vorticity maxima: damping rate `>= nu kappa^2 |omega|`.
- **Supercritical source term kills closure.** The source `D_xi S` involves
  `nabla^2 u`, which is supercritical and prevents any maximum-principle or
  energy-method closure.
- **No kappa blowup mechanism found.** Multiple independent mechanisms resist it.
- **Type I self-similar scaling:** `kappa ~ (T-t)^{-1/2}` while `|omega| ~
  (T-t)^{-1}`, so `kappa/|omega| -> 0` (vortex lines straighten relatively).

The most promising remaining sub-approach is a **coupled bootstrap argument**:
large `|omega|` damps kappa (restricted Euler), large kappa damps `|omega|`
(viscous feedback). Whether the coupled damping beats the supercritical source
growth is the quantitative question at the honest frontier. Estimated probability
of success: 10-20%.

## What Is Closed

These should currently be treated as closed, or at least as very poor default bets:

- generic enstrophy regularity programs
- De Giorgi pressure-improvement attempts aimed at `beta > 3/2`
- standard epsilon-regularity bootstrapping
- `H^1` pressure / compensated compactness pressure repair
- harmonic far-field pressure refinements by themselves
- exact reformulation-only escapes without a new one-sided gain
- standard compactness-rigidity host-space retries
- hidden-precursor physical-space observability without extra memory structure
- broad "maybe Tao misses some NS structure" surveys without a concrete theorem object
- exact singleton Tao-circuit embedding
- trigger-only reframings that do not first define a canonical packet model
- clustered exact-mode packetizations with post hoc desired-channel bookkeeping, as exemplified by the tested dyadic-helical triad-packet model
- anti-circuit expansion / hypergraph-conductance restatements that still require post hoc role-community or desired-channel annotation
- helical-sign packet missions whose `SD_part` / `SD_target` functionals still depend on non-canonical packet support, representative choice, or desired-triad classification
- cancellation-ratio phase-coherence observables that are forced on one exact triad and arbitrarily weakened on the first nontrivial two-input exact-helical cluster
- intrinsic phase-locking firewall attempts built on tiny finite recursively closed helical supports of the first three searched budgets:
  one-triad seeds,
  two-triad shared-mode seeds,
  and three-triad single-repeated-orbit seeds
- strain-vorticity alignment GMT approaches that try to prove regularity from `e_2`-alignment of vorticity alone: the intermediate eigenvalue `s_2` is universally positive in high-vorticity regions (confirmed by restricted Euler, DNS at all Reynolds numbers, pressure Hessian analysis, and all known blowup mechanisms), and the anti-alignment feedback structure means `e_2`-alignment suppresses the vorticity-induced modification of `s_2`, making the `s_2 > 0` obstruction structural rather than technical
- GMT dimensional-reduction arguments on the "dangerous set" `{|omega| > M, Q > epsilon}` where `Q = omega . S omega / |omega|^2`: superlevel sets of smooth functions have full Hausdorff dimension even for passive vorticity with smooth drift; this is a category error (GMT dimension estimates apply to zero sets and singular sets, not superlevel sets)
- direct pressure Hessian self-damping arguments through the `Q`-evolution equation: the claimed `-|omega|^2/6` vorticity self-damping term does not exist (`Omega^2 omega = 0`); the isotropic pressure Hessian is anti-damping when `|S|^2 > |omega|^2/2`, which is the case in high-vorticity regions (DNS: `|S|^2/|omega|^2 ~ 2-4`)

## What Still Looks Even Slightly Live

Only a narrow set of directions still seems worth real effort.

An additional five-route synthesis completed on **April 1, 2026** sharpened the
frontier further. The picture is now:

- two packet-level branches already have concrete next theorem tests on one
  frozen canonical ledger;
- the cleanest intrinsic moonshot is still a phase/coherence object on exact
  shell-crossing triads rather than another packet object, but the first
  three smallest finite-support budgets have now failed by recursive spill, so
  the burden has shifted away from immediate local phase frustration on tiny
  closed supports and toward larger shell-interface structure versus locking;
- the critical-element route only stays alive conditionally, and only after a
  new canonical-ledger extraction lemma is proved;
- the helical-sign route remains mechanistically informative, but has been
  demoted behind the phase route as a primary theorem candidate.

Plain status of the five live pursuits after the follow-up checks:

- `Route 1` and `Route 2` are now the best concrete theorem moves.
- `Route 3` is still the best intrinsic moonshot, but it is weaker than before:
  the first three finite-support budgets all spill before any local
  phase-frustration theorem appears.
- `Route 4` should currently be treated as parked unless a canonical
  critical-element ledger extraction lemma appears.
- `Route 5` should currently be treated as auxiliary evidence feeding the
  leakage and phase routes, not as the lead theorem object.

### 1. Template-defect family theorem on the frozen near-circuit ledger

The repaired `Template-Defect Near-Closure` object is no longer just a vague
screen. On the frozen one-bridge canonical ledger, the clearest next move is a
sharp family theorem on the carried `F_SL(rho)` line:

- prove exactly that `Delta_tmpl(F_SL(rho)) = 1/4`;
- prove exactly that `Delta_spec(F_SL(rho)) = 3 rho + rho^2`;
- and prove sharpness at `rho = 1/16`, which is the carried friendly witness.

If that ledger closes cleanly, the route earns a real packet-family theorem:
the repaired admissibility sheet is sharp on one explicit friendly family.

The main near-term kill condition is also sharp:

- if the inferred `F_SL(rho)` defect ledger fails to close as an exact
  role-projected coefficient/sign computation on the frozen sheet, then this
  branch is still depending on hidden bookkeeping and should be downgraded.

Even in the positive case, this remains only a packet-family theorem on the
frozen ledger, not yet an intrinsic control law on actual Navier-Stokes
solutions.

### 2. Leakage firewall lemma on the same frozen ledger

The repaired `Windowed Spectator-Leakage Budget` route is now sharper than a
generic "maybe leakage is unavoidable" slogan.

On the frozen ledger, the repaired admissibility sheet

`b* = (1/4, 1/12, 1/12, 1/16, 1/24)`

is the coordinatewise smallest sheet admitting the carried friendly stress set,
and the hostile tiny-trigger family `F_DT(delta, eta)` already sits uniformly
outside that sheet in four coordinates, not just one.

A small exact witness-freeze follow-up now makes that branch more concrete:

- `F_SS(1/12)` can be frozen on the repaired branch authority sheet without reopening the
  packet semantics, witness choice, or comparison currency;
- on that same ledger it passes repaired `G_tmpl` and repaired `G_leak`, and
  it saturates the obstruction-facing entries `L_tot`, `L_mirror`,
  `L_companion`, and `L_cross`;
- `F_SL(1/16)` still remains the boundary-friendly witness for
  `Delta_tmpl`, `Delta_spec`, and `L_feedback`;
- the one surviving threshold-variance note is historical only:
  some older helper artifacts still show `L_cross = 1/12`, but the later
  controlling repaired branch sheet freezes `L_cross <= 1/24`.

So the best next theorem-shaped target is a local frozen-ledger firewall lemma:

- any packet on the same frozen class with the hostile near-degenerate
  tiny-trigger shape must violate the repaired leakage sheet in at least the
  recorded `L_tot`, `L_mirror`, `L_companion`, and `L_feedback` coordinates.

The key missing step is no longer the friendly arithmetic. It is a transfer
lemma:

- prove that the hostile desired-channel shape really forces those leakage lower
  bounds in the same exact interaction currency.

One exact packet on the same frozen ledger with hostile tiny-trigger behavior
but repaired leakage would kill this route immediately.

### 3. Intrinsic phase / coherence firewall on shell-crossing exact triads

The cleanest intrinsic moonshot is now a phase/coherence route that avoids
packet annotation altogether.

The best current object is a transfer-weighted constructive-phase defect on an
intrinsic dyadic shell interface:

- work directly with exact shell-crossing helical triads;
- weight them by exact transfer magnitude;
- and measure how closely their phases align with the forward-transfer phase.

This route is now more promising than the direct sign-packet route because it
keeps the only robust sign clue, namely target-edge constructive versus
frustrated transfer, while avoiding post hoc desired-edge packet bookkeeping.

The sharp next theorem question used to be very small-scale:

- on the first exact branching layer above the surviving core triad
  `a1 + a3 -> a4`, with first emissions to `(1,2,0)` and `(2,1,0)`,
  does sustained positive forward transfer force incompatible constructive
  phase windows across the branching triads?

That test has now been run in the smallest honest five-mode branching module,
and the answer is negative at that level:

- the reduced internal phase system admits an exact quadrature-locked sector
  with simultaneous constructive core transfer and constructive first-branch
  emissions;
- so the hoped-for first-branch finite phase-frustration obstruction does not
  appear immediately.

The route therefore survives only in a narrower form:

- the real question is now whether recursive exact closure and spectator burden
  destroy that would-be locking sector once the next forced families are added.

One more step has now also been checked, and it points the same way:

- on the quadrature-locked five-mode sector, the first recursive emission layer
  organizes into coherent `+pi/2` and `-pi/2` phase bands rather than a local
  incompatibility;
- in particular the strongest doubled target `(2,2,0), sigma = +1` receives
  aligned contributions from both `a1 b` and `a3 c`, so the most obvious
  recursive clash actually reinforces instead of frustrating.

So the best next Route 3 theorem target is no longer "incompatible
constructive windows on the first branch." It is closer to:

- any would-be quadrature-locked shell-crossing transfer sector must trigger
  recursive companion/spectator growth too quickly to support a Tao-like delayed
  window.

This is still the best candidate for a genuinely different intrinsic object
class, but it is now noticeably weaker than it looked even one iteration ago.

### 4. Conditional critical-element packet-leakage rigidity

Ordinary compactness-rigidity restarts remain poor default bets and should still
be treated as closed in the sense stated above.

The only conditional hybrid that still looks worth naming is much narrower:

- assume a symmetry-normalized minimal blowup element in a defensible critical
  host space, most likely `L^3`;
- canonically extract one exact Tao-style one-bridge ledger on concentration
  windows;
- then prove a `no-double-admissibility` theorem saying that the extracted
  object cannot satisfy the repaired template-defect and repaired leakage gates
  simultaneously.

The contradiction blueprint is attractive:

`blowup => minimal element => canonical ledger => repeated near-closure windows
=> exact NS contradiction`

But this branch is still substantially more speculative than the first three,
because its main missing piece is not an estimate. It is a new object-definition
lemma:

- a canonical critical-element ledger extraction rule that is stable under
  compactness limits, harmless refinement, and representative relabeling.

Without that lemma, this route is still only a disciplined placeholder.

### 5. Restricted variational helical-sign route, now demoted behind the phase route

The helical-sign line is not dead, but it has changed status.

The robust mechanistic clue now seems to be:

- low leakage pushes toward globally near-homochiral organization;
- but the load-bearing Tao-like target edge remains stubbornly heterochiral.

So the best surviving theorem-shaped form is no longer a vague global sign
coherence statement. It is closer to:

- define `J_lambda = Leak + lambda SD_target` on one restricted faithful class;
- ask whether `Leak <= eps` forces `SD_target >= c(eps)`;
- or whether minimizers for `J_lambda` compactify up to symmetries.

This route is still blocked by one concentrated canonicity problem:

- there is no intrinsic exact desired-triad set `T_target`, so both `SD_target`
  and `Leak` still move under harmless support/refinement and desired-witness
  changes.

So this line should currently be treated as a support route for the leakage or
phase programs, not as the primary theorem object.

### Sidecar obstruction work

The earlier meta-no-go theorem for clustered packetizations is still worth doing
as durable obstruction work:

- prove that clustered exact-mode packet models with post hoc desired-channel
  bookkeeping must fail canonicity for essentially the same reasons as the first
  tested packet family.

But after the April 1, 2026 synthesis, that line no longer looks like one of
the top five prize-facing routes.

Likewise, the old "no-near-closed packet theorem" should now be viewed as an
endpoint theorem that reopens only after one of the routes above produces a
genuinely canonical object.

## Practical Status Relative to the Million-Dollar Problem

Two prize-winning outcomes exist:

1. prove global regularity
2. produce a genuine finite-time blowup

Current practical read:

- A constructive exact-NS blowup path looks less plausible than it did before Tao was mechanized; Tao's example clarified how much engineering exact NS may not permit.
- A regularity proof path also does **not** currently exist.
- The research program is therefore still in a mapping-and-elimination phase rather than a proof phase.

More sharply after the April 1, 2026 route synthesis:

- the best near-term deliverables are now two exact packet-family theorems on
  the frozen one-bridge ledger:
  - a sharp template-defect theorem on the carried `F_SL(rho)` family,
  - and a sharp leakage firewall lemma against the hostile tiny-trigger family
    if the transfer step can be proved;
- the carried constructive `F_SS(1/12)` chain is now cleaner but not more
  open-ended:
  Step 7 freezes one honest same-ledger authority sheet,
  while Step 8 and Step 9 stop the branch at
  `exact non-isolability / arbitrary-truncation requirement`
  and then
  `source-basis / no-canonical-finite-reduction memo`;
  the April 2, 2026 explicit one-bridge bridge only narrows that realization
  gap partially and does not yet reopen reduced dynamics;
  the fixed-wavevector follow-up then sharpens the negative further, because
  the whole explicit singleton family already on disk only supports two of the
  six desired Step-7 pairs anywhere in the searched sigma / representative
  space and never more than one at once;
- the best intrinsic moonshot is now a recursive closure-versus-locking theorem
  on exact shell-crossing triads: the first branching module itself admits a
  compatible quadrature-locked sector, so the burden has shifted to whether
  recursive spill destroys any such sector before a real delayed window forms;
  the first recursive emission layer also propagates coherent quadrature phases,
  so any Route 3 obstruction now has to come from later support growth or
  spectator burden rather than a small local phase clash;
- the critical-element route remains conceptually attractive but is still blocked
  earlier than before, at the canonical-ledger extraction stage;
- the helical-sign route remains informative as mechanism shape, but not yet as
  the main theorem object.

In plain project-management terms, that now means:

- `Routes 1 and 2`: active and best for real near-term theorem progress;
- `Route 3`: active, but now clearly more speculative than `1` and `2`;
- `Route 4`: parked;
- `Route 5`: helper route only.

An **April 2, 2026** broad-angle pursuit (10 novel angles generated, all 10
adversarially explored, best one pursued through 5 subproblems) then added:

- The strain-vorticity `e_2`-alignment GMT approach (Angle 10) was selected as
  the most promising novel direction outside the existing Tao-adjacent family.
  It reached a terminal structural obstruction: `s_2 > 0` universally in
  high-vorticity regions, and `e_2`-alignment itself removes the feedback
  mechanism that could reverse the sign. The GMT dimensional-reduction component
  was killed at the passive model level (category error: superlevel sets have
  full dimension).
- Theorem C3 (conditional regularity under `e_2`-alignment + `s_2 <= 0`) is a
  genuine new result, incomparable with Constantin-Fefferman.
- The smooth Rayleigh quotient `Q = omega . S omega / |omega|^2` was identified
  as the correct object for strain-vorticity analysis, resolving the eigenvector
  regularity issue (coalescence is codimension 2, not 1).
- Nine other novel angles were also explored and ranked. The two next most
  promising (Lagrangian stretch-dissipation, convex integration rigidity) both
  face serious but not definitively fatal obstacles.
- Three new live directions were identified that are not blocked by the `s_2`
  obstruction:
  - combined alignment + vorticity-direction regularity (verify
    Constantin-Fefferman geometrically via eigenframe spatial coherence)
  - direct pressure Hessian analysis of the enstrophy balance
  - vorticity-direction regularity (proving Lipschitz regularity of
    `omega/|omega|` in high-vorticity regions)

That sounds discouraging, but the progress is still real:

- several major false doors have now been closed rigorously or near-rigorously
- Tao's obstruction has been converted into a concrete mechanism picture
- the open frontier has been narrowed to a much more specific object-definition problem
- the strain-vorticity alignment picture is now fully characterized: alignment
  is real and self-organizing, but it controls direction not magnitude, and
  the precise obstruction (`s_2 > 0`) is identified

## Best Current One-Paragraph Status

If someone asked, "Where do we stand on Navier-Stokes after all this work?", the honest answer would be:

```text
The classical estimate routes now look largely exhausted. Enstrophy runs into
the BKM circle, De Giorgi pressure improvement is sharply capped at beta = 4/3,
epsilon-regularity seems structurally capped too, and the H^1 / harmonic-pressure
repair ideas are dead. Tao's averaged blowup has been understood much more
concretely, but every exact-NS firewall candidate tested so far has either failed,
dissolved into a non-canonical packet model, collapsed back into non-intrinsic
hypergraph annotation, or run into a physical-space backward-memory failure.
The first concrete clustered exact-mode packet model has now also failed
canonicity, and even the anti-circuit expansion restatement is blocked at the
same theorem-object level. A newer exact near-circuit screen has done better:
it froze two honest packet-level objects, template-defect and leakage budget,
on one canonical one-bridge helical ledger, and the carried witness
`F_SS(1/12)` can now be frozen on the repaired authority sheet in the same
currency. But the constructive continuation then stops honestly:
Step 8 reaches only classwise exact non-isolability / arbitrary-truncation
requirement, Step 9 stops again at source-basis / no-canonical-finite-
reduction, and the latest explicit singleton bridge only narrows that gap
partially without rescuing exact closure. So the remaining Tao-adjacent hope,
if any, is now split more sharply: either upgrade the frozen template-defect
and leakage objects into real exact packet-family theorems, or earn one
same-currency explicit realization protocol before claiming any reduced
dynamics. The sharpest new local ranking is now: first try to promote the
frozen template-defect and leakage objects into exact packet-family theorems;
in parallel, pursue an intrinsic phase/coherence object on exact shell-
crossing triads, but now in the stricter recursive-spill form rather than the
earlier first-branch phase-frustration form, since even the first recursive
emission layer propagates coherent quadrature phases; keep the critical-element
bridge alive only conditionally, pending a canonical-ledger extraction lemma;
and treat the helical-sign route mainly as a mechanism clue centered on
persistent target-edge heterochirality, not as the leading theorem object until
the desired-triad set is made intrinsic.

A separate broad-angle search on April 2, 2026 generated and explored 10 novel
angles outside the Tao-adjacent family. The best candidate — strain-vorticity
e_2-alignment GMT — was pursued to a structural dead end: the intermediate
strain eigenvalue s_2 is universally positive in high-vorticity regions, and
e_2-alignment itself removes the feedback that could reverse it. A new
conditional regularity theorem (Theorem C3: alignment + s_2 <= 0 implies
regularity) survives as a genuine contribution, incomparable with
Constantin-Fefferman. Three remaining live non-Tao directions were identified:
combined alignment + direction regularity, direct pressure Hessian analysis,
and vorticity-direction Lipschitz regularity.
```

## High-Signal Source Map

### atlas

- `research-systems/atlas/execution/instances/navier-stokes/MISSION-COMPLETE.md`
- `research-systems/atlas/execution/instances/vasseur-pressure/MISSION-COMPLETE.md`

### codex-atlas

- `research-systems/codex-atlas/execution/instances/navier-stokes/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/vasseur-pressure/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/FINAL-REPORT.md`
- `research-systems/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/exact-ns-tiny-trigger-firewall/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/MISSION-COMPLETE.md`
- `research-systems/codex-atlas/execution/instances/exact-ns-phase-locking-firewall/MISSION.md`
- `research-systems/codex-atlas/docs_and_guides/vasseur-pressure-mission.md`
- `research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/INDEX.md`

### philosopher-atlas

- `research-systems/philosopher-atlas/missions/vasseur-pressure/MISSION-COMPLETE.md`

### codex-philosopher-atlas

- `research-systems/codex-philosopher-atlas/missions/vasseur-pressure/MISSION-COMPLETE.md`
- `research-systems/codex-philosopher-atlas/library/factual/far-field-pressure-obstruction/INDEX.md`
- `research-systems/codex-philosopher-atlas/library/factual/navier-stokes/INDEX.md`
- `research-systems/codex-philosopher-atlas/library/factual/tao-circuit-feature-ledger/INDEX.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-no-near-closed-tao-circuit/steps/step-008/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-no-near-closed-tao-circuit/steps/step-009/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-003/RESULTS.md`
- `research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-004/RESULTS.md`

### codex-nexus

- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/theorem-object-ledger.md`
- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/packet-model-spec-v0.md`
- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/canonicity-stress-test.md`
- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/clustered-packet-no-go-scope.md`
- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/anti-circuit-expansion-scope.md`
- `/Users/seanross/kingdom_of_god/home-base_worktrees/codex-nexus/current_hunts/big-thinkers/research-systems/codex-nexus/artifacts/sign-sensitive-packet-functionals-v0.md`

### local follow-up synthesis

- `simulation-machines-attempts/run-2026-04-01-ns-new-path-from-status-doc/final-summary.md`
- `simulation-machines-attempts/run-2026-04-01-ns-underexplored-route-search/final-summary.md`
- `simulation-machines-attempts/run-2026-04-01-ns-underexplored-route-search/artifacts/favored-route-sketch.md`
- `simulation-machines-attempts/run-2026-04-01-ns-phase-branching-module-check/final-summary.md`
- `simulation-machines-attempts/run-2026-04-01-ns-phase-recursive-generation-check/final-summary.md`
- `simulation-machines-attempts/run-2026-04-01-helical-sign-defect-prototype/summary.md`
- `simulation-machines-attempts/run-2026-04-01-helical-sign-defect-prototype/packet-functional-sketch.md`
- `simulation-machines-attempts/run-2026-04-01-packet-ledger-functional-prototype/summary.md`
- `simulation-machines-attempts/run-2026-04-01-packet-ledger-functional-prototype/adversarial-search-summary.md`
- `simulation-machines-attempts/run-2026-04-01-packet-ledger-functional-prototype/global-adversarial-search-summary.md`
- `simulation-machines-attempts/run-2026-04-01-packet-functional-prototype/summary.md`
- `simulation-machines-attempts/run-2026-04-01-fss-authority-sheet-freeze/summary.md`
- `simulation-machines-attempts/run-2026-04-02-one-bridge-realization-bridge/summary.md`
- `simulation-machines-attempts/run-2026-04-02-fixed-wavevector-sheet-search/summary.md`
- `simulation-machines-attempts/run-2026-04-02-singleton-step7-obstruction-scan/summary.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/final-synthesis.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/phase-1-2-angles.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/phase-4-selection.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/subproblem-A-ground-truth.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/subproblem-B-eigenvector-regularity.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/subproblem-C-conditional-regularity.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/subproblem-D-gmt-model.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/subproblem-E-s2-dynamics.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/direction-1-alignment-direction.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/direction-2-pressure-hessian.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/direction-3-vorticity-direction.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/dhy-burgers-test.md`
- `simulation-machines-attempts/run-2026-04-02-ns-pursuit-plan/curvature-evolution-analysis.md`
