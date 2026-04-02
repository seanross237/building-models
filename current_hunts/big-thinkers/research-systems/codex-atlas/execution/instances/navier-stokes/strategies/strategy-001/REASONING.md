# Reasoning Log

## Exploration 001: Catalog of Load-Bearing Inequalities in 3D NS Regularity Theory

### Pre-Exploration Reasoning (2026-03-29)

**Phase:** Phase 1 — Catalog the Estimates (exploration 1 of 2-3)

**Options considered:**
1. **Standard explorer: comprehensive literature survey of all load-bearing inequalities** — This is the natural starting point. The strategy explicitly calls for it as the first Phase 1 exploration. Everything downstream depends on having a precise catalog.
2. **Math explorer: simultaneously write computable forms** — The strategy suggests a parallel math explorer. But without the literature survey output, the math explorer would have to do its own survey + code, which wastes its computation-focused capabilities.
3. **Split into multiple surveys (one per inequality family)** — Meta-learning says a single well-scoped survey with 6 named families should work as one exploration. Splitting wastes budget.

**Chosen:** Option 1 — standard explorer for comprehensive literature survey.

**Why:** Foundation-first. Every Phase 2 computation depends on having the exact mathematical statements. The meta-library confirms: standard explorers are 2.5× faster than math explorers for surveys with equivalent depth. The single-survey approach is fine for 6 named families.

**Rejected:**
- Option 2: The math explorer should follow, working from the survey results. Running it blind wastes its strength.
- Option 3: Over-splitting. Meta-learning says a single well-scoped survey with explicit categories covers all sub-categories.

**Meta-learning applied:**
- Divergent survey pattern (5-part structure with honest assessment + next computation recommendation)
- Theorem-level precision ("What EXACTLY do they prove?")
- Named specific authors/papers as starting points + "any others you find"
- Classification scheme with table format
- Incremental writing deadline nudge to prevent research-buffering stall
- Failure path: note ambiguities in conventions
- Allow explorer synthesis for structural patterns

**Librarian query summary:** No factual library entries on NS (expected — first mission). Rich meta-learning returns: 12 applicable lessons about survey design, incremental writing, classification schemes, rigor levels, and failure paths. All incorporated into the goal design.

### Post-Exploration Reflection

**Did the explorer deliver?** Yes — exceeded expectations. 17 entries (vs. minimum 8), all 7 fields filled, structural chain analysis, ranked slack list, and the Tao classification. The catalog is comprehensive enough to proceed directly to computation.

**Was the scope right?** Perfect. The single-exploration approach for the full survey worked. The 7 named families + "find more" instruction gave structure without over-constraining.

**What I'd change:**
- Should have asked for more precise Re-scaling analysis (the explorer gave some hand-wavy dimensional arguments). The math explorer will need to redo this computationally.
- Should have asked explicitly about Strichartz estimates — the explorer flagged them as "potentially missing" but didn't resolve whether they're truly load-bearing.

**Key strategic insight from this exploration:** The Tao classification splits the catalog into two worlds: (1) generic inequalities that are sharp in ℝ³ but whose extremals aren't NS solutions, and (2) NS-specific inequalities where the real slack lives. This means Phase 2 should focus primarily on NS-specific estimates (vortex stretching, CKN, Prodi-Serrin) rather than generic Sobolev/GNS bounds.

**Decision for next exploration:** Launch exploration 002 as a math explorer to build the computational measurement infrastructure. It should write Python functions for bound(u)/actual(u) for each cataloged inequality and run the first measurements on Taylor-Green vortex at multiple Re. This bridges Phase 1 → Phase 2.

---

## Exploration 002: Computational Slack Measurement Infrastructure + First Measurements

### Pre-Exploration Reasoning (2026-03-29)

**Phase:** Phase 1→2 bridge (exploration 2 of the catalog phase, first of measurement phase)

**Options considered:**
1. **Math explorer: Write computable forms (bound/actual pairs) for all inequalities + run first measurements on Taylor-Green vortex** — This is the natural next step. Uses the existing ns_solver.py scaffolding. Bridges Phase 1 → Phase 2 efficiently.
2. **Standard explorer: Deeper literature dive into vortex stretching bounds** — Tempting given the #1 slack ranking, but premature. Need computational data first.
3. **Math explorer: Only write the computable forms, no simulation** — Too narrow. The strategy requires simulation results, and the math explorer is the right tool for both code AND computation.
4. **Math explorer: Full Phase 2 measurements across all initial conditions** — Too broad. Save the full measurement campaign for dedicated Phase 2 explorations.

**Chosen:** Option 1 — Math explorer writes bound/actual functions and runs first measurements on Taylor-Green vortex.

**Why:** The strategy's "cross-phase rule" requires every inequality to be written as computable Python functions. The math explorer is the right tool (code + verification). Including first measurements on Taylor-Green gives immediate slack data, providing direction for the rest of Phase 2. The existing ns_solver.py provides scaffolding.

**Key design decisions:**
- Focus on the top 5 inequalities by expected slack (not all 17 — many are just GNS special cases)
- Use N=64³ for first pass (speed), with N=128³ convergence check on the highest-slack estimate
- Re = 100, 500, 1000, 5000 (4 values as specified in strategy)
- Taylor-Green vortex initial condition (standard benchmark)
- Require the math explorer to tag all results with [VERIFIED]/[COMPUTED]/[CHECKED]/[CONJECTURED]

**Librarian query:** Not needed for this exploration — we have everything from exploration 001. The catalog provides all the mathematical statements needed for coding.

### Post-Exploration Reflection

**Did the explorer deliver?** Yes — exceeded expectations. All 8 inequalities implemented and validated, full slack atlas with convergence checks, plus an insightful decomposition of the vortex stretching slack into three sources.

**Was the scope right?** Good scope. The bridge between Phase 1 and Phase 2 worked well — having the catalog's exact formulas let the math explorer focus on computation rather than re-derivation. The only gap was the resolution/time limits: T=5 doesn't capture fully developed turbulence at high Re.

**Key strategic insights from this exploration:**
1. **Vortex stretching is THE target** — 237× min slack, 55× more than the next inequality. This isn't close.
2. **Slack grows with Re** (Re^0.28) for vortex stretching — meaning the bound gets WORSE at higher Re, exactly where regularity breaks down.
3. **Three sources of the 237×**: Hölder alignment loss (~9×), constant looseness (~18.6×), ||S||≤||ω|| factor (~1.4×). The ~9× from Hölder is the most interesting — it represents actual geometric information being discarded.
4. **Functional inequalities (F1, F3) are surprisingly tight** at 4.3-4.5×. The NS-specific Ladyzhenskaya constant is still worth computing but won't give orders of magnitude.
5. **Min slack is determined by initial condition geometry** for all stable inequalities. This means adversarial IC search is critical.

**Decision for next explorations:** The data overwhelmingly points to vortex stretching as the target. I'll run two parallel explorations:
- **Exploration 003 (math):** Adversarial initial conditions — search for flows that minimize the vortex stretching slack ratio. Also test ABC flow and random-phase ICs. Uses the existing measurement infrastructure.
- **Exploration 004 (math):** Vortex stretching Hölder decomposition — isolate the three sources of slack computationally. Compute the intermediate quantities ||S||_{L²}, ||ω||²_{L⁴}, and the alignment tensor ∫ξ_i S_{ij} ξ_j |ω|² dx to understand exactly where the 9× geometric loss comes from.

### Post-Exploration 004 Reflection

**Did the explorer deliver?** Exceeded expectations. Complete decomposition at 30+ timesteps across two Re values, full alignment statistics with eigendecompositions at every grid point, and a preliminary sharp constant survey.

**Was the scope right?** Almost perfect. Part C (sharp constant) was too limited — only surveyed known fields rather than attempting systematic optimization. But Parts A and B were excellent.

**Critical finding that changes strategy:** The corrected decomposition shows Ladyzhenskaya dominates (63% of log-slack), not geometric alignment (31%). This is the opposite of what exploration 002's rough estimates suggested. The effective Ladyzhenskaya constant (C_{L,eff} = 0.147) being only 18% of the sharp constant means NS solutions are structurally far from the Ladyzhenskaya optimizer. **This points toward constrained interpolation inequalities as the highest-leverage tightening direction.**

**Strategic pivot:** Instead of focusing on Constantin-Fefferman-style geometric bounds (which addresses only 31% of log-slack), the most impactful direction is:
1. **Constrained interpolation inequalities** for NS-like fields (div-free, spectrally decaying, etc.)
2. **BKM-type bounds** that bypass Ladyzhenskaya entirely
3. **Spectral Ladyzhenskaya bounds** that exploit the spectral localization of NS solutions

This doesn't mean the geometric factor is unimportant — 5.3× is still real slack — but the biggest win is in better interpolation.

### Post-Exploration 003 Reflection

**Did the explorer deliver?** Yes — all 5 ICs tested, adversarial search found 158× (34% below TGV), convergence validated at N=128.

**Was the scope right?** Good but had one blind spot — the z-invariant vortex tube symmetry degeneracy (VS ≡ 0) wasn't anticipated. The explorer handled it well by adding z-perturbation, but wasted some time.

**Key strategic insight:** The ~158× minimum across all tested ICs strongly suggests this is a **structural limitation of the Hölder + Ladyzhenskaya proof chain**, not a property of any specific flow. Combined with exploration 004's decomposition (Ladyzhenskaya dominates at 63%), the path forward is clear: better interpolation inequalities.

## Phase 2 Conclusion & Phase 3 Plan

**Phase 2 summary (explorations 002-004):**
- Vortex stretching has 158-237× slack depending on IC (158× adversarial minimum)
- Slack decomposes: 63% Ladyzhenskaya constant + 31% geometric alignment + 6% symmetric factor
- Slack grows with Re (∝ Re^0.28) — gets worse exactly where regularity is hardest
- The effective Ladyzhenskaya constant for NS flows (C_{L,eff} = 0.147) is 18% of the sharp constant (0.827)
- NS solutions are structurally far from Ladyzhenskaya optimizers
- All functional inequalities are Re-independent and relatively tight (4-8×)

**Phase 3 plan: Tighten the loosest estimate**

I'll pursue two parallel directions:

1. **Direction A — Constrained interpolation:** Can we prove a tighter Ladyzhenskaya inequality for NS-like fields? The 63% log-slack contribution suggests this is the highest-leverage target. Need literature survey + computational attempt.

2. **Direction B — Alternative enstrophy closures:** What if we bypass Ladyzhenskaya entirely? The enstrophy equation closure doesn't HAVE to go through ||ω||_{L⁴}. Alternative approaches (BKM, spectral truncation, Biot-Savart-aware bounds) may have structurally less slack.

**Exploration plan:**
- **Exploration 005 (standard):** Literature survey on existing tightening attempts — what has been tried for improved vortex stretching bounds, spectral NS estimates, and alternative enstrophy closures?
- **Exploration 006 (math):** Compute the spectral Ladyzhenskaya inequality: for fields with energy spectrum E(k) ~ k^{-5/3}, what is the effective C_L? Systematic computation over spectral classes.
- These run in parallel — independent goals.

---

## Explorations 005+006: Literature Survey + Spectral Ladyzhenskaya

### Pre-Exploration Reasoning (2026-03-30)

**Phase:** Phase 3 — Tighten the Loosest Estimate (first 2 of 3-4 explorations)

**Options considered:**
1. **Parallel: Standard explorer literature survey + Math explorer spectral Ladyzhenskaya** — Efficient. Literature survey informs later explorations; spectral computation is independent.
2. **Sequential: Literature first, then computation** — Safer but slower. Risk: we might already know enough to compute.
3. **Skip literature, go straight to proving a tighter bound** — Risky. We might waste time proving something that's already known.
4. **Different direction: CKN ε* computation** — Interesting but the vortex stretching direction is more promising given the data.

**Chosen:** Option 1 — parallel literature + computation.

**Why:** We have 12-16 remaining explorations. Running these in parallel saves time. The literature survey (005) ensures we don't rediscover known results. The spectral computation (006) directly tests whether spectral localization reduces C_L.

**What would change my approach:** If the literature survey finds that constrained Ladyzhenskaya has already been thoroughly studied with negative results, I'll pivot to Direction B (alternative closures). If the spectral computation shows negligible improvement, I'll pivot to the geometric factor instead.

### Post-Exploration 005 Reflection

**Did the explorer deliver?** Excellent — 28 papers with exact theorem statements, clear assessment of each against our bottleneck.

**Key strategic updates from the literature:**
1. **No spectral Ladyzhenskaya exists** — this is genuinely an open problem, which is good for novelty
2. **Tao (2014) obstruction** means spectral improvements alone can't close regularity — reframes exploration 006 from "path to proof" to "quantification tool"
3. **BKM vs Ladyzhenskaya comparison (12× vs 158×)** is under-remarked in literature — potentially novel observation
4. **Bradshaw-Farhat-Grujić intermittency** is the most actionable existing framework for explaining our C_{L,eff}/C_L ratio
5. **Protas group confirms the bound IS functionally tight** for adversarial ICs — our 158× is for non-adversarial flows

**Revised Phase 3 plan (after exploration 006 returns):**
- Direction A: Spectral Ladyzhenskaya — exploration 006 will quantify this
- Direction B: Intermittency calibration — measure μ for our flows, check Bradshaw-Farhat-Grujić prediction
- Direction C: BKM advantage quantification — compute ‖ω‖_{BMO}/‖ω‖_{L^∞} for our flows
- Direction D: Adversarial review of our best claimed results

### Post-Exploration 006 Reflection

**Did the explorer deliver?** Yes — the critical negative result (spectral support doesn't help for worst-case bounds) is the most valuable finding. The (5/9)^{1/4} div-free factor is a clean positive result.

**Key strategic update:** Direction A (spectral Ladyzhenskaya) is CLOSED as a tightening path. The observed C_{L,eff} ~ Re^{-3/8} is statistical, not provable. This is consistent with Tao's 2014 obstruction — harmonic analysis alone can't improve things.

**Remaining tightening paths:**
- Direction B: Intermittency/flatness bounds — if F₄ ≤ C Re^ε can be proven, the spectral improvement follows
- Direction C: BKM advantage — the 12× vs 158× comparison is concrete, computable, and potentially novel

**Revised plan for remaining explorations (budget: 6-14 explorations left):**
- **Exploration 007 (math):** Compute BMO norms and intermittency measures for DNS flows. Quantify BKM vs Ladyzhenskaya advantage. Test BFG prediction. This is the key remaining computational task.
- **Exploration 008 (standard):** Adversarial review of all claimed novel results — novelty search, strongest counterarguments
- **Exploration 009:** Optional — depends on 007-008 results. Formalize the tightest claimable result.

I'm cutting the budget from 15-20 to ~9 total. The science results are clear: we have a quantified slack atlas, a corrected decomposition, a dead-end spectral direction, and remaining live paths. The adversarial review is the critical remaining exploration.

---

## Exploration 007: BMO Norms + Intermittency Calibration + BKM Advantage

### Pre-Exploration Reasoning (2026-03-30)

**Phase:** Phase 3 — final computational exploration before adversarial review

**Options considered:**
1. **Math explorer: BMO + intermittency + BKM quantification on DNS data** — combines three related measurements on existing simulation data. Uses existing infrastructure.
2. **Math explorer: Attempt formal proof of conditional bound** — premature without knowing if intermittency actually explains C_{L,eff}
3. **Standard explorer: Literature on flatness bounds for NS** — could be useful but delays computation
4. **Skip straight to adversarial review** — premature, BMO comparison is the most promising remaining novelty

**Chosen:** Option 1 — combined BMO + intermittency + BKM computation.

**Why:** Three measurements that share the same DNS data and infrastructure. The BKM vs Ladyzhenskaya comparison (12× vs 158×) is the most promising novel observation from this strategy. Quantifying it precisely, including via BMO norms and intermittency measures, could be the strategy's main novel contribution.

**Librarian query:** Not needed — existing library has our prior NS exploration results, which is all we need.
