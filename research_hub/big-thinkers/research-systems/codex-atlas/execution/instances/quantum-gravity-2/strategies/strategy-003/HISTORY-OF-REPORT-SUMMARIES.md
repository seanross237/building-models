# Exploration History

## Exploration 001 — Precise Conjecture Statement (TIMED OUT)
**Goal:** State the QG+F–AS unification conjecture with mathematical precision, enumerate testable/falsifying implications, survey literature.
**Outcome:** TIMED OUT. Explorer wrote a skeleton (24 lines) but spent 25+ minutes researching without writing substantive content. Scope was too broad (5 parts requiring extensive literature search).
**Key lesson:** "Precise conjecture statement" requires breaking into sub-tasks. Explorer got lost in open-ended web research.

## Exploration 002 — Fixed Point Compatibility: AF → NGFP Connection (INCONCLUSIVE)
**Goal:** What does the published literature say about whether the AF fixed point of quadratic gravity connects to the Reuter NGFP via RG flow?
**Outcome:** INCONCLUSIVE. No paper has explicitly computed an RG trajectory from AF to NGFP. Two competing interpretations:
1. **Same FP, different approximations** (Codello-Percacci 2006): Non-perturbative RG turns the perturbative AF Gaussian FP into an NGFP. If true, the "connection" question is moot — they're the same point.
2. **Distinct FPs, possible connection** (SWY 2022): Two separate FPs with different critical exponents. A "critical trajectory" between them "may exist" but isn't proven.
**Key finding:** The tension is truncation-dependent: coarser truncations see one FP; finer (SWY) resolve two. Falls et al. (2023) find a 4D UV critical surface at the NGFP matching quadratic gravity's coupling count. QQG is described as "a concrete realization of asymptotic safety" (Salvio et al.). But no paper has proven the connection.
**Key papers:** SWY 2022 (arXiv:2111.04696), SWY 2023 (arXiv:2211.05508), Codello-Percacci 2006 (PRL 97, 221301), Falls et al. 2023 (PRD 108, 026005).
**Verdict for conjecture:** The most favorable reading is that AF is a perturbative approximation to the NGFP — plausible but NOT established.

## Exploration 003 — Ghost Fate at Strong Coupling (INCONCLUSIVE, leaning SUPPORTS)
**Goal:** What does the non-perturbative/AS literature say about the fate of the massive spin-2 ghost at strong coupling?
**Outcome:** INCONCLUSIVE, leaning SUPPORTS. The spin-2 ghost occupies a **blind spot** in the AS literature — multiple frameworks could address it, but no paper has done the definitive calculation. Four candidate mechanisms:
1. Ghost mass → ∞ at NGFP (Becker et al. 2017) — proven for scalars, not spin-2
2. Fictitious ghost / truncation artifact (Platania & Wetterich 2020) — framework proposed, not demonstrated for Stelle ghost
3. Complex pole tower (Draper, Knorr et al. 2020) — ghost-like poles migrate to complex momenta, unitarity preserved. **Most concrete mechanism.**
4. Ghost confinement / QCD analogy (Holdom & Ren 2016) — heuristic only, zero evidence in gravity
**Key finding:** The bridge between QG+F and AS at the ghost level is UNBUILT. AS has multiple consistent mechanisms for ghost removal and no result requiring the ghost to persist, but no one has shown AS dynamics *forces* the ghost out. Computing the full spin-2 propagator pole structure in the C²-extended AS truncation is the single most important open calculation.

## Exploration 004 — Inflationary Prediction Reconciliation (SUPPORTS)
**Goal:** Can the inflationary predictions (r, n_s) of QG+F and AS be reconciled?
**Outcome:** **SUPPORTS** (moderate confidence). The pre-loaded framing was misleading. The "AS predicts r up to ~0.01" comes from one specific model (Bonanno-Platania with maximal b). The majority of AS inflation papers — Codello et al. (2014), Gubitosi et al. (2018) — show AS naturally **produces Starobinsky inflation** with r ≈ 0.003, squarely within QG+F's window of r ∈ [0.0004, 0.0035]. Both theories predict the same inflationary mechanism.
**Key finding:** r is NOT the clean discriminator the library suggested. Both theories overlap at r ≈ 0.003. The missing calculation: AS inflation in the full R² + C² truncation. No paper has done this.
**Key papers:** Codello et al. PRD 91 103530 (2014), Gubitosi et al. JCAP 1812 004 (2018), Bonanno & Platania arXiv:1507.03375, Anselmi & Piva JHEP 07 (2020) 211, Bianchi & Gamonal arXiv:2506.10081 (June 2025).

## Exploration 005 — Black Hole Prediction Compatibility (SUPPORTS)
**Goal:** Can QG+F's Schwarzschild BH be reconciled with AS's modified BH (running G, singularity resolution, Planck remnants)?
**Outcome:** **SUPPORTS.** The predictions are compatible — they describe perturbative vs non-perturbative regimes. Five arguments:
1. Anselmi admits non-perturbative blindness (JHEP 2026) — "Schwarzschild" means "to all perturbative orders"
2. Both agree at large r — AS's Bonanno-Reuter metric reduces to Schwarzschild + O(l_P²/r²)
3. Perturbative expansion breaks down exactly where AS takes over (M ~ M_P)
4. Planck remnants fill a gap in QG+F (no evaporation endpoint prediction), not a contradiction
5. QCD analogy: Schwarzschild = "partonic" (perturbative), modified BH = "hadronic" (non-perturbative)
**Key caveat:** Compatibility depends on ghost being removed non-perturbatively. If ghost survives at strong coupling, spontaneous ghostification (Bonanno 2025) predicts naked singularity, which WOULD break compatibility.
**Scorecard:** 0 FALSIFIED, 2 SUPPORTS (inflation + BH), 2 INCONCLUSIVE (fixed points + ghost fate).

## Exploration 006 — Analyticity Reconciliation (SUPPORTS)
**Goal:** Can QG+F's sacrifice of S-matrix analyticity be reconciled with AS's Euclidean functional RG framework?
**Outcome:** **SUPPORTS** — with confidence. The tension dissolves completely. Three independent lines:
1. **AS already has Wick rotation obstructions** — ghost pole in upper right quadrant obstructs standard Wick rotation (Donoghue 2020); infinite towers of poles at imaginary p² (Draper et al. 2020). AS itself cannot rely on standard analyticity.
2. **AS doesn't require analyticity** — the Wetterich equation is a computational tool; physical prediction extraction is separate. Lorentzian AS (D'Angelo et al. 2024) demonstrated the NGFP directly in Lorentzian signature without any Wick rotation.
3. **Fakeon may solve AS's own problem** — QG+F's average continuation provides a systematic nonanalytic method for Euclidean→Lorentzian extraction despite complex poles — exactly the tool AS needs.
**Key finding:** The analyticity sacrifice is NOT a barrier. It may be a *feature* — QG+F acknowledges and handles a non-analyticity that AS already implicitly contains.
**Updated scorecard:** 0 FALSIFIED, 3 SUPPORTS (inflation + BH + analyticity), 2 INCONCLUSIVE (fixed points + ghost fate).

## Exploration 007 — Unified Framework Construction (SUCCEEDED)
**Goal:** Construct the unified QG+F–AS framework as a coherent theory statement.
**Outcome:** **SUCCEEDED.** 415-line framework document with 5 major components:
1. **Theory statement:** QG+F and AS describe the same four-derivative gravity action in complementary regimes (perturbative/non-perturbative), joined at M_P — the gravitational analog of Λ_QCD.
2. **Regime structure:** Six-regime phase diagram with Planck-scale transition identified via three independent mechanisms (coupling strength, ghost mass threshold, BH branch crossing).
3. **Five bridge mechanisms:** Ghost (fakeon ↔ confinement), Fixed Point (AF ↔ NGFP), Inflation (Starobinsky ↔ NGFP), Black Hole (Schwarzschild ↔ Bonanno-Reuter), Analyticity (average continuation ↔ obstructed Wick rotation).
4. **Seven novel predictions:** (a) Fakeon average continuation resolves AS's Wick rotation problem, (b) ghost confinement scale = M_P dynamically, (c) BH evaporation phase transition at M ~ M_P, (d) sharpened r with NGFP-determined b parameter, (e) full d_s(E) profile as consistency check, (f) six-derivative couplings from NGFP hierarchy, (g) Higgs mass as UV boundary check.
5. **Open problems:** AF→NGFP trajectory (uncomputed) and spin-2 ghost confinement (unproven for gravitational ghost). Both are well-defined FRG calculations.
**Key finding:** The framework is constructible, internally coherent, and falsifiable. The central conjecture: "fakeon prescription is the perturbative avatar of ghost confinement."

## Exploration 008 — Devil's Advocate Attack (FRAMEWORK SURVIVES BARELY)
**Goal:** Ruthlessly attack the unified framework. 7 attack vectors, 5-tier validation.
**Outcome:** No FATAL attacks but 3 SERIOUS, 4 MODERATE. Framework viable but unsubstantiated.
**SERIOUS attacks:**
1. QCD analogy broken at most critical point (confinement mechanism — no compact gauge group, no color charge)
2. INCONCLUSIVE results may be failures (central conjectures unresolved ~10 years)
3. Predictions unfalsifiable (no prediction simultaneously novel, testable, AND specific)
**5-Tier validation:** Novel=MARGINAL, Consistent=PASS, Explanatory=MARGINAL, Predictive=**FAIL**, Testable=MARGINAL.
**Key finding:** The framework is a "well-constructed conjecture that currently lacks both theoretical proof and experimental discriminability." Its fate depends on two FRG calculations: (1) AF→NGFP trajectory, (2) spin-2 ghost propagator in C²-extended FRG. The "compatible-but-separate" interpretation is a simpler alternative.
**Three calculations that would change the assessment:** (1) AF→NGFP trajectory computation, (2) spin-2 ghost propagator showing pole dissolution, (3) NGFP b parameter giving specific r prediction.

## Exploration 009 — Discriminating Predictions (PARTIALLY SUCCEEDED)
**Goal:** Find predictions that discriminate the unified framework from standalone theories and from the compatible-but-separate null hypothesis.
**Outcome:** Found **1 strong discriminator** and **1 moderate**, but **0 near-term experimental discriminators.**
**Strong discriminator:** The spin-2 ghost propagator in (R+R²+C²) FRG truncation. Unified framework predicts ghost pole dissolves (into complex towers or via mass divergence). Compatible-but-separate has no mechanism for this. Computation is well-defined, ~1-2 years for expert group, methodology exists.
**Moderate discriminator:** Fakeon average continuation applied to Wetterich equation. Predicted by unified framework, unnecessary if separate. May be rendered moot by Lorentzian AS.
**Not discriminating:** b parameter (consistency check), near-term CMB, LIGO QNMs, n_s tension (all resolvable by standalone frameworks).
**Key finding:** The framework has exactly ONE genuinely discriminating prediction: ghost dissolution in the C²-extended FRG. Everything else is a consistency check. The compatible-but-separate interpretation is simpler (Occam) and remains the default until the ghost propagator computation is performed.

