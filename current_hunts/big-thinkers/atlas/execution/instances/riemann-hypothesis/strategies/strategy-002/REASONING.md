# Strategizer Reasoning Log — Strategy 002

## Startup

**Date:** 2026-03-27
**State:** Iteration 0, fresh start. No explorations completed yet.

### What I read:
- state.json: empty, iteration 0
- STRATEGY.md: Operator Construction Tournament methodology
- HISTORY-OF-REPORT-SUMMARIES.md: empty (fresh start)
- strategy-001 FINAL-REPORT.md: Full context on what S001 established

### Key takeaways from S001:
- 10-point constraint catalog built, all computationally verified on 2000 zeros
- All tested operators scored 0/10 (Sierra-Townsend, BBM, trace formula, Toeplitz/Hankel)
- Critical insight: real symmetric matrices are capped at β≤1 (GOE), can never reach β=2 (GUE)
- Strategy-002 mandate: BUILD operators, don't just test them
- Open question: two-point formula (exploration-005 crashed before computing)

---

## Iteration 1 — Phase 1 Planning

**Date:** 2026-03-27

### Options considered:

The strategy is clear: Phase 1 runs three parallel tournament entries. Each attacks the construction problem from a different angle. These are independent and can run simultaneously, saving 2/3 of the wall-clock time.

**Entry A (Complex Arithmetic Matrices):** Math Explorer task. Construct Hermitian matrices with von Mangoldt amplitudes × Dirichlet character phases. Key test: can we push β from 0.44 (Hankel) toward 2.0 (GUE) with complex entries? This is the most direct extension of S001's arithmetic matrix finding.

**Entry B (Optimization-Based Construction):** Math Explorer task. Reverse-engineer the operator from constraints. Use scipy.optimize to find a Hermitian matrix whose eigenvalue spacing distribution matches GUE. Then examine what the optimized matrix looks like — does it have interpretable structure? This approach is novel: nobody has tried "what matrix produces these statistics?" as an optimization problem.

**Entry C (Two-Point Formula + Kernel):** Math Explorer task. Retry S001's crashed exploration-005. Compute Montgomery's pair correlation formula explicitly from prime pairs, compare to numerical pair correlation from actual zeros, and if they agree, use the two-point function as a kernel to construct an operator. This resolves the critical open question and potentially gives us a construction principle.

### Decision:
Run all three in parallel. All are Math Explorer tasks (computation-heavy, code-driven). I'll launch three tmux sessions simultaneously:
- rh-explorer-001a: Entry A (Complex Arithmetic Matrices) → exploration-001
- rh-explorer-001b: Entry B (Optimization-Based Construction) → exploration-002
- rh-explorer-001c: Entry C (Two-Point Formula + Kernel) → exploration-003

### What I expect:
- Entry A will show whether complex entries shift β toward 2.0 — direct test of the "matrix structure matters" insight
- Entry B is the longest shot but most novel — optimized matrix might reveal interpretable structure
- Entry C resolves the critical open question: does two-point formula succeed where one-point failed?

### Library query:
Will query the library for context on Dirichlet characters and GUE, Montgomery pair correlation implementation, and optimization methods for RMT.

---

## Library Query — Iteration 1

**Query sent:** Context on (a) complex Hermitian arithmetic matrices for GUE spectrum, (b) Montgomery pair correlation implementation, (c) optimization for RMT matching.

**Library returned:**

**For Entry A (Complex Arithmetic Matrices):**
- Confirmed: real symmetric matrices are mathematically capped at β≤1, never GUE. Complex Hermitian entries are required.
- Baseline: von Mangoldt Hankel β=0.44 (partial GOE). Extension to complex entries is the natural next step.
- No prior library results on Dirichlet character phases — this is unexplored territory.
- Meta lesson: multi-ansatz sweep pattern applies — test uniform random phase, Dirichlet character, and Gauss sum phases in one exploration.

**For Entry B (Optimization-Based Construction):**
- No prior library results on optimization-based construction — genuinely new approach.
- Key decomposition insight: short-range constraints (pair correlation, spacing) vs. long-range constraints (number variance, rigidity) test fundamentally different aspects. Optimization loss function must balance both.
- β (level repulsion exponent) must be a primary output metric.

**For Entry C (Two-Point Formula + Kernel):**
- Montgomery's formula: R₂(r) = 1 - (sin(πr)/(πr))²
- Strategy-001 exploration-005 crashed but partial code exists at `strategies/strategy-001/explorations/exploration-005/`
- The raw prime form factor sum DIVERGES at x=0; proper Berry normalization required
- One-point trace formula fails for individual zeros due to Gibbs phenomenon
- Two-point formula is theoretically different — if it succeeds, it means prime pairs encode correlations (not just density)
- No prior library results on kernel operator construction from R₂ — new territory

**Computational notes for all explorations:**
- mpmath practical cap: ~2000 zeros
- Strategy-001 saved eigenvalue data exists in exploration-006 directory (reusable)
- Always include GUE simulation as finite-size control
- Pre-load formulas and baseline numbers into goal

**Usefulness: HIGH.** The library gave me the exact β=0.44 baseline numbers, the Montgomery formula implementation details, and the key insight that the two-point approach is theoretically distinct from the failed one-point approach. Also confirmed that optimization construction is genuinely novel — no prior work.

**Key library finding for Entry C:** The exploration-005 GOAL.md and partial code already exist. I should check what code was written before the crash and use it as a starting point for Entry C.

---

## Reflection — Iteration 1

**Exploration-001 (Complex Arithmetic Matrices): DONE — Primary success criterion met (β=1.675)**
- C1 (Random complex phases): β = 1.675, GUE best fit, 4 PASS / 2 PARTIAL on constraint catalog
- C3b (Gauss p=997): β = 1.092, GOE best fit — meaningful arithmetic result
- Key structural principle discovered: phase φ(j,k) must be non-factorizable to break time-reversal symmetry
- Code bugs identified: R₂ normalization and Δ₃ formula need fixing for constraints 2 and 7

**Exploration-002 (Optimization): PARTIAL — Usage limit hit after Stage 1**
- Stage 1 critical finding: histogram loss is non-differentiable → gradient-based optimization fails
- Stage 2 (KDE loss + Nelder-Mead) was running when limit hit
- Useful negative result: this approach has a fundamental technical barrier

**Exploration-003 (Two-Point Formula): PARTIAL — Computations done, report not written (usage limit)**
- Pair correlation MAD = 6.9% (slightly better than S001's 9%)
- Form factor ramp MAD = 19.3% from zeros vs GUE
- K_primes identical across P_max = 100/1000/10000 → normalization bug
- Kernel matrix eigenvalues ~0 → rank-deficient

**What I'd do differently:**
- Specify exact R₂ normalization formula and Δ₃ integral formula in the goal
- Add design-validity check step for matrix constructions
- For exploration-003, the prime form factor normalization should have been spelled out explicitly (Berry's formula is tricky)

---

## Iteration 4 — Phase 1 Synthesis and Phase 2 Planning

**Date:** 2026-03-27

### Phase 1 Synthesis

The tournament produced one clear winner: **C1 (random complex phases on Von Mangoldt Hankel)** at β=1.675. This satisfies the Phase 1 success criterion (any entry ≥ 4/10).

Key insights from Phase 1:
1. **Complex phases work.** Breaking real symmetry pushes β from 0.44 to 1.65+.
2. **Arithmetic structure constrains β.** C3b (Gauss sums, genuinely arithmetic) only reaches β=1.09. C1 (random phases, not arithmetic) reaches β=1.65. The gap between arithmetic and random suggests arithmetic structure imposes a penalty on GUE statistics.
3. **Phase non-factorizability is necessary.** Only phases φ(j,k) depending on j and k jointly can break time-reversal symmetry.
4. **Optimization approach has a fundamental technical barrier** — eigenvalue statistics are non-differentiable loss functions.
5. **Two-point formula question still open** — 003's prime form factor normalization failed; the data is there but the key comparison wasn't properly completed.

### Phase 2 Options

The strategy says: if an entry scored ≥ 4/10, run 2-3 deeper explorations. Also: mandatory Berry saturation comparison.

**Option A (MANDATORY per strategy): Berry saturation quantitative comparison**
- Compute Berry's explicit prediction for Δ₃ saturation level from prime sums
- Compare to measured 0.156 for zeta zeros
- This is "a clean, high-value computation" per strategy
- Does NOT depend on Phase 1 results; should be done regardless

**Option B: Fix code bugs and recompute full 10-constraint score for C1**
- Fix R₂ normalization (exact formula: kernel smoothed pair correlation density)
- Fix Δ₃ (Dyson-Mehta integral, not mean-squared-residual/L)
- Recompute constraints 2, 7, 9, 10 for C1
- Would give the true score (currently 4 PASS + 2 NOT COMPUTED)
- Expected result: C1 will likely score 5-6/10 after bug fixes

**Option C: Deeper Gauss sum investigation**
- C3b (Gauss p=997) reaches β=1.09 with arithmetic phases. What's the math?
- Try larger primes: p=9973, 99991 — does β→2 as p→∞?
- Try superposition of Gauss sums from multiple primes
- If p→∞ limit achieves GUE with arithmetic phases, that's a genuinely novel construction

**Option D: Redo two-point formula properly**
- Fix Berry's prime form factor normalization bug
- Answer definitively: do prime pairs reproduce the pair correlation?
- The REPORT data (mae_R2_norm=6.9%) is good for zeros vs Montgomery; the prime side wasn't properly computed

**Option E: New Dirichlet character construction**
- C2 failed because odd characters cancel. Use χ mod 5 (complex values {1,i,-1,-i})
- Genuinely complex arithmetic phases with number-theoretic structure
- Different from C1 (random) and C3 (Gauss sums): character phases have modular arithmetic structure

### Phase 2 Decision

**Running 3 explorations in Phase 2:**

- **Exploration 004 (MANDATORY):** Berry saturation formula quantitative comparison. Math Explorer. Solo task — clean, high-value.
- **Exploration 005:** Full constraint rescoring for C1 + Gauss prime sweep (fix bugs + extend C3b to larger primes). Math Explorer. Combines the must-do bug fixes with the most promising arithmetic direction.
- **Exploration 006:** Two-point formula redo + Dirichlet character construction. Math Explorer. Resolves the open two-point question and tests the complex character approach.

This leaves 4 explorations for Phase 3 (adversarial + synthesis, mandatory) plus 1 extra buffer.

Actually, wait — I have 10 total explorations. Used 3 (001-003, with 002 and 003 partial). Remaining: 7.
Phase 2: 3 explorations → explorations 004-006
Phase 3 (mandatory): 2 explorations → explorations 007-008
That leaves 009-010 as buffer / follow-up

I'll run Phase 2 in sequence (not parallel) since they build on each other.

Start with exploration 004 (Berry saturation — independent), then 005 (code fixes + Gauss sweep), then 006 (two-point formula redo).

---

## Reflection — Exploration 004 (Berry Saturation)

Berry's formula confirmed quantitatively: Δ₃_sat = (1/π²)×log(log(T/2π)), 7.6% overall error. Height-resolved analysis confirms strict monotone increase. The mandatory computation is done and gives a clean positive result. Key disambiguation: integral formula (correct) vs sum formula (wrong by 2×).

## Reflection — Exploration 005 (C1 Rescoring + Gauss Sweep)

**C1 pair correlation (7.9% MRD):** This is the most important result. C1 satisfies Montgomery's formula, which means random complex phases on Von Mangoldt Hankel produce not just GUE-like short-range statistics (spacing distribution) but also GUE-like pair correlations. This is unexpected — the Mangoldt structure alone (not the phases) seems to be doing some of the work.

**Gauss sweep:** DEFINITIVE NEGATIVE. β peaks at p=809, then collapses for large p. The N²/p≈250 optimal ratio explains the behavior. Gauss sums are permanently GOE.

**The key finding for Phase 3:** C1 (random phases + Von Mangoldt Hankel) has:
- β = 1.18-1.68 (variable, in GUE range)
- Pair correlation MRD = 7.9% (passes constraint 2)
- Δ₃ saturation = 0.285 (not 0.156 like zeta, not 0.565 like GUE)
- This intermediate Δ₃ is interesting: the Hankel structure creates rigidity beyond what GUE gives, but not the same as actual prime orbit structure.

## Iteration 7 — Phase 3 Planning

**Date:** 2026-03-27

### Phase 2 overall assessment:

Phase 2 has produced clear findings:
1. Berry formula confirmed (E004)
2. C1 pair correlation passes Montgomery (E005)
3. Gauss sums permanently GOE (E005)
4. C1 intermediate rigidity (Δ₃=0.285 between GUE=0.565 and zeta=0.156)
5. Two-point formula still open (E006 in progress)

### Budget:
- 5 explorations used (001-005)
- Exploration 006 in progress
- Remaining after 006: 4 explorations
- Phase 3 mandatory: 2 explorations (adversarial + synthesis)
- Available buffer: 2 explorations (007-008 for Phase 3, 009-010 buffer if needed)

### Phase 3 Plan (explorations 007-008):

**Exploration 007 (MANDATORY — Adversarial Review):**
The strongest claim to adversarially test is: **"C1 random phase Von Mangoldt Hankel satisfies Montgomery's pair correlation formula at the 10% level (7.9% MRD)."**

Adversarial questions:
1. Is this 7.9% result specific to this construction, or does ANY random Hermitian matrix satisfy pair correlation?
2. Is the Von Mangoldt structure necessary, or would uniform amplitude give the same result?
3. Is 7.9% within statistical noise for N=500 matrices?
4. Does this already appear in the random matrix theory literature?

**Exploration 008 (MANDATORY — Synthesis):**
Survey all findings. Key question: what's the single most defensible novel claim of the entire mission?

Candidates:
1. Berry saturation confirmed quantitatively with height-resolved trend (solid, but Berry (1985) predicted this)
2. C1 pair correlation passes Montgomery (interesting but may be trivially true for any GUE-class matrix)
3. Gauss sums are permanently GOE — β peaks at N²/p≈250-310 (may be novel as explicit result)
4. Phase non-factorizability principle for GUE construction (structural insight, may be new as explicit theorem)
5. Two-point formula status (TBD after E006)

### Decision: Launch E007 (adversarial) immediately after E006, then E008 (synthesis).


## Reflection — Exploration 006 (Two-Point Formula + Dirichlet Characters)

**Part A (Two-point form factor): SUCCESS**
- K_primes matches K_GUE ramp with 14.5% MAD — Berry's conjecture confirmed computationally
- Resolves the persistent open question from E003 and E005
- Critical insight found: the cosine sum formula is wrong (it's Re[Z(τ)], not |Z|²/N). Correct formula bins prime orbit periods and divides by (2πρ̄)².
- Explorer got stuck at 58-62% context on scipy debugging after Part B computation. Required manual intervention to extract results and complete report.

**Part B (Dirichlet characters): NEGATIVE + PROVED IMPOSSIBLE**
- Best β = 0.281 (χ_13). All GOE class.
- The structural proof is the key result: multiplicative Hermitianizing → real matrix. Factorizable → unitarily equivalent to real. Both routes → GOE.
- This is stronger than a numerical test — it proves no Dirichlet character construction can give GUE.

**What I'd do differently:**
- Specify scipy fallback in goal: "If scipy.optimize fails, implement chi-squared fit manually (formula provided)"
- The explorer spent 30+ minutes trying to debug scipy after already computing results
- Separate multi-part goals that have independent tool dependencies

---

## Iteration 7 — Phase 3 Planning

**Date:** 2026-03-27

### Phase 2 complete — what we know:

**Definitive negatives:**
1. Real symmetric matrices: β ≤ 1 (mathematically proved) 
2. Gauss sum phases: permanently GOE (β peaks at p=809, then collapses; max β=1.15)
3. Dirichlet character phases: algebraically impossible to give GUE (both routes → real matrix or unitarily equivalent to real)
4. Optimization with gradient-based methods: non-differentiable loss function

**Positive findings:**
1. C1 (random complex phases + Von Mangoldt Hankel): β=1.18 ± 0.22, pair correlation PASS (7.9%), Δ₃=0.285 (intermediate)
2. Berry saturation formula confirmed quantitatively (7.6% error)
3. Two-point spectral correlations: primes determine the ramp (14.5% MAD)
4. Phase non-factorizability principle: need φ(j,k) ≠ g(j) ± g(k)

### Phase 3 Plan

**Exploration 007 (MANDATORY — Adversarial Review):**

Primary target: **"C1 random phases on Von Mangoldt Hankel satisfies Montgomery's pair correlation at the 7.9% MRD level."**

Four adversarial questions:
1. Is 7.9% from C1 better than random? → Compare to 100 random Hermitian matrices (no Von Mangoldt structure). If they also give 7.9%, the Von Mangoldt structure adds nothing.
2. Is the Von Mangoldt structure necessary, or would any Hermitian Toeplitz/Hankel with random phases work? → Test with flat amplitude (all Λ=1) + random phases.
3. Is 7.9% statistically significant for N=500? → What's the scatter in MRD for 100 GUE matrices?
4. Is C1's intermediate Δ₃=0.285 actually a feature, or a failure? → The zeta zeros have Δ₃=0.156, much smaller. Is C1 just "barely GUE-class" rather than "Riemann-like"?

**Exploration 008 (MANDATORY — Synthesis + Novel Claims):**

Task: Survey ALL findings from both strategies. Identify the single most defensible novel claim. Write it as it would appear in a short paper (one paragraph with explicit citations and evidence).

Candidates:
1. **"Dirichlet characters algebraically cannot give GUE"** — new as explicit proof (algebraic argument showing both routes → real matrix)
2. **"Gauss sum GOE confinement with N²/p scaling"** — β peaks at N²/p≈250-310, then collapses — may be novel explicit result
3. **"Berry saturation confirmed height-resolved with 7.6% accuracy"** — cleaner than Berry's original prediction; matches integral formula (not sum formula)
4. **"Von Mangoldt Hankel enhanced rigidity: Δ₃≈50% of GUE"** — intermediate rigidity not previously characterized
5. **"Prime form factor ramp: 14.5% MAD"** — quantitative confirmation of Berry's diagonal approximation

### Budget check:
- 6 explorations used (E001-E006)
- 4 remaining: E007, E008, E009, E010
- Phase 3 mandatory: E007 (adversarial), E008 (synthesis) = 2 explorations
- Buffer: E009, E010 for follow-up on whatever adversarial review reveals

Start E007 immediately.

## Library Query — Exploration 007

**Query:** Adversarial methodology, pair correlation baselines, Von Mangoldt necessity, null hypothesis design.

**Library returned (HIGH USEFULNESS):**

Key findings:
1. **Adversarial needs null hypothesis** (meta/methodology) — compute MRD for null matrices, don't just argue
2. **Flat amplitudes may work equally well** (factual) — library says "arithmetic content doesn't matter, only phase structure" for universality class
3. **GUE control baseline** (factual) — need to compute MRD for proper GUE vs Montgomery to know if 7.9% is meaningful
4. **Severity scheme** (meta/goal-design) — FATAL/SERIOUS/MODERATE/COSMETIC with claim evaluation table
5. **Multi-realization stability** (meta/methodology) — 5 realizations may not be enough for stable MRD estimate
6. **Scipy fallback** (meta from E006) — include manual Brody fit formula to prevent blocking on scipy ImportError

Particularly valuable: the library confirmed the Von Mangoldt amplitude issue — it actually makes Δ₃ WORSE (too rigid), so it may be doing nothing positive for pair correlation. The key test is flat-amplitude comparison.

**Action:** Used all of these directly in the E007 GOAL.md.

## Reflection — Exploration 007 (Adversarial Review)

**Outcome: THREE SERIOUS ATTACKS ESTABLISHED — valuable adversarial result**

Key findings:
1. **Von Mangoldt amplitude unnecessary:** Flat-amplitude (6.8%) ≤ C1 (7.9%). GUE control (7.8%) ≈ C1.
2. **Individual realization instability:** Mean MRD = 15.5% ± 1.9%; 0/20 pass ≤10%. The E005 "7.9% PASS" was a 5-realization averaging artifact.
3. **GOE-class also passes:** Toeplitz (β=0.45) achieves 9.0% — pair correlation test is insufficiently discriminating.

The adversarial test did its job — it significantly weakened the pair correlation claim. The surviving strong results are: C1's intermediate Δ₃ rigidity, Berry formula confirmation, and Dirichlet impossibility.

Same pattern as E006/007: explorer computed results, got stuck in deep thinking, couldn't write report. Killed and manually completed.

**What I'd do differently:** Instruct incremental writing in the goal: "After each test runs, fill in that section of REPORT.md immediately." This is now documented in meta-inbox.

---

## Iteration 8 — Synthesis Planning

**Date:** 2026-03-27

### E008 (MANDATORY — Final Synthesis)

With 7 explorations complete, I have a clear picture. E008 is the synthesis exploration — identify the most defensible novel claims and write them up with full citation chains.

After E007's adversarial review, the claim landscape is:

**Claims that survived adversarial review:**
1. **C1 intermediate Δ₃ rigidity** (Δ₃=0.285, between GUE=0.565 and zeta=0.156): Specific to Von Mangoldt Hankel. NOT reproduced by flat amplitudes (which would give Δ₃≈0.565, GUE-like). This is the one thing the Von Mangoldt structure uniquely contributes. Strength: MODERATE.
2. **Dirichlet character impossibility theorem**: Both construction routes (multiplicative + Hermitianize → real matrix; factorizable → unitarily equivalent) give GOE. Algebraically proved. Strength: HIGH (proved, not just empirical).
3. **Gauss sum GOE confinement with N²/p≈250 optimal ratio**: β peaks at N²/p≈250-310, collapses for larger p. May be novel as explicit numerical result with mechanistic explanation. Strength: MODERATE.
4. **Berry saturation formula confirmed height-resolved with 7.6% accuracy**: Cleaner than Berry (1985) original. Disambiguates integral formula (correct) from sum formula (2× off). Strength: MODERATE (incremental confirmation).
5. **Prime form factor ramp confirmation**: K_primes matches K_GUE ramp with 14.5% MAD. Also resolves why prior normalizations failed (cosine formula vs |Z|²/N). Strength: MODERATE (confirmation + normalization clarification).

**The most novel claim:** #2 (Dirichlet impossibility) and #1 (Von Mangoldt Δ₃ intermediate rigidity) are the strongest candidates for novelty. #2 has a clean algebraic proof. #1 is a quantitative observation not previously documented.

### E008 design:

E008 should be a standard Explorer (not math — this is synthesis/literature work) that:
1. Searches for prior work on each claim candidate to assess novelty
2. Writes up the top 2-3 claims in paper format
3. Recommends what the next strategy should focus on

Actually wait — given the pattern of explorers getting stuck in deep thinking loops, and the fact that E008 is a synthesis task (not computation), I should use a STANDARD Explorer (not Math Explorer) which typically writes more efficiently.

Budget check: 7 explorations used. 3 remaining (E008, E009, E010).
- E008: Final synthesis (1 exploration)
- E009, E010: Buffer (can use for follow-up if E008 reveals new directions, or skip)

Plan: Launch E008 now, use E009 if the synthesis identifies a key follow-up computation.

Actually, given the pattern issues, let me think about whether to use a standard vs math explorer. The synthesis task involves:
- Literature search (standard explorer)
- Writing up claims in paper format (standard explorer)
- NOT new computation

→ Use standard Explorer for E008.

## Library Query — Exploration 008

**Query:** Novelty assessment for four candidate claims from S002.

**Library returned (HIGH USEFULNESS):**

Key findings:
1. **Strategy-001 found zero novel claims** — all four S002 candidates are stronger than S001's three candidates
2. **Dirichlet impossibility (Claim 2)** — strongest novelty candidate; clean algebraic proof, no prior citation found in library, internally originated
3. **N²/p scaling (Claim 3)** — specific quantitative result, no prior citation in library; may appear in signal processing (chirp/DFT) literature — needs external search
4. **C1 intermediate rigidity (Claim 1)** — weak novelty; likely known to Hankel spectral theorists; no external citation
5. **Cosine sum normalization (Claim 4)** — weak-to-moderate; Berry (1985) is prior source for diagonal approx; normalization subtlety may not be explicitly documented

The library explicitly can't do the external novelty search (it only knows what we've put in). E008 should do targeted web searches for the Dirichlet impossibility and N²/p claims.

**Decision for E008:** Use STANDARD Explorer (not Math) — this is synthesis/literature work, not computation. The Explorer should search arXiv/literature for prior work on the two strongest claims (Dirichlet impossibility and N²/p scaling).

---

## Exploration 009 — Flat-Amplitude Δ₃ Spectral Rigidity Test

### Pre-exploration reasoning

**Date:** 2026-03-27
**Iteration:** 9 (budget: 10)
**Explorer type:** Math Explorer
**Budget remaining:** 2 explorations (E009 + E010)

### What I considered

After E008's synthesis, the options for E009 are:
1. **Write FINAL-REPORT now** — E008 gave us two SUPPORTED novel claims and a complete synthesis. Could stop here.
2. **Flat-amplitude Δ₃ test** — E008's #1 recommendation. One Math Explorer computation. Tests whether C1's anomalous Δ₃=0.285 is caused by Von Mangoldt arithmetic or is generic to any GUE-class matrix.
3. **N-scaling of N²/p** — Also recommended by E008. Tests whether N²/p≈275 is a universal constant.

### Critical context from librarian

The librarian revealed an important nuance: **GUE finite-size simulation at N=500 gives Δ₃_sat ≈ 0.250**, NOT 0.565 (which is the infinite-N theory value). C1 gives 0.285. These are nearly identical.

This means the "anomalous intermediate Δ₃" claim may be much weaker than presented in E008 — C1's Δ₃=0.285 could simply be finite-size GUE behavior, with the intermediate value (between 0.250 and the infinite-N 0.565) being expected rather than anomalous.

The flat-amplitude test will resolve this: if H_flat (GUE class, no Von Mangoldt) also gives Δ₃≈0.250-0.285, then C1's value is generic GUE-class behavior. If H_flat gives significantly lower Δ₃ (closer to zeta zeros at 0.155), something would be odd (but this seems unlikely).

### Decision: Run E009 for flat-amplitude Δ₃ test

**Why**: 
- This is a short, clean computation (1-2 hours for Math Explorer)
- It directly resolves the key ambiguity in the C1 Δ₃ claim
- Even if the result confirms C1's Δ₃ is generic GUE behavior (not arithmetic), that's a CLEAN definitive negative — important for the final report
- Budget justification: spending 1 exploration to definitively resolve the strongest positive finding is worth it

**What I rejected and why:**
- N-scaling test (E009b option): Would take longer (multiple N values), less directly relevant to the novel claims assessment
- Writing FINAL-REPORT now: The Δ₃ claim is the main remaining ambiguity; spending 1 more exploration to resolve it strengthens the report

### Library query results

**Most useful findings:**
1. GUE finite-size at N=500 gives Δ₃_sat≈0.250 — implies C1's 0.285 may be generic
2. Exact Δ₃ formula confirmed: integral/staircase method, NOT sum formula
3. scipy not available (numpy.Inf removed) but Δ₃ doesn't need scipy
4. Stalling pattern documented: kill after 30 min stagnation, extract from npz
5. Must include "WRITE INCREMENTALLY + [SECTION COMPLETE] markers" instruction

**Librarian exchange usefulness: HIGH** — the GUE finite-size value is critical context that changes interpretation of C1's Δ₃.

---

## Exploration 009 — Reflection

**Explorer died:** Hit Claude usage limit before writing report. Session was gone when I checked.

**Recovery:** I had already run the computation directly (python3 heredoc) and gotten clean results before the session died. Wrote REPORT.md and REPORT-SUMMARY.md manually from those results.

**Key finding:** H_flat (0.256±0.010) ≈ C1 (0.243±0.017) ≈ GUE (0.227±0.010) — all within noise. **Von Mangoldt amplitude does NOT cause intermediate Δ₃.** The C1 intermediate rigidity claim is retracted.

**Was scope right?** Yes — single computation with 3 ensembles × 3 realizations was exactly right. Clean decisive negative.

**What I'd change:** The Δ₃ formula in the GOAL.md was wrong (sampling at eigenvalue positions instead of integrating staircase). The explorer caught this via sanity check, which is good. Future goals should include: "verify GUE control gives Δ₃_sat ≈ 0.22-0.26 at N=500; if not, formula has a bug."

**Budget:** 9 explorations used (10 planned, E010 skipped — N²/p scaling verification is a lower priority than finishing cleanly with the decisive negative on C1 Δ₃). Budget exhausted. Writing FINAL-REPORT now.
