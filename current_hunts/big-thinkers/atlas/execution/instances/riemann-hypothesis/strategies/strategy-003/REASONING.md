# Strategy-003 Reasoning Log

## Startup — 2026-03-27

### State on Entry
- Iteration 0, no explorations in this strategy
- strategy-001: 6 explorations, built 10-constraint catalog, confirmed GUE + super-rigidity
- strategy-002: 9 explorations, systematic construction tournament — no matrix achieves Δ₃<0.2
- Central gap confirmed: Δ₃_sat(zeta) = 0.155 vs. best GUE-class matrix = 0.243 (~40% gap)

### Reading Prior Strategy Final Reports
Both S001 and S002 final reports read. Key takeaways:
- The super-rigidity gap is the mission's central unsolved problem
- Berry's formula PREDICTS Δ₃=0.155 from prime sums — the information is there, but no matrix captures it
- The diagonal approximation explains the ramp but not the plateau/saturation
- Off-diagonal orbit pairs (Berry/Bogomolny-Keating) are the theoretically correct explanation
- S002 recommended this as Priority 1 for S003

### Library Query Summary
Queried library for: off-diagonal form factor context, Li's criterion context, meta-lessons.

**Useful factual findings returned:**
- Confirmed Δ₃ formulas (integral form, NOT sum) — preload into explorer goals
- K(τ) normalization conventions — prior explorations burned on this; K_primes = K_density/(2πρ̄)²
- Berry formula (1/π²)log(log(T/2π)) confirmed 7.6% accuracy
- Prime sums confirm ramp (MAD=14.5%) but fail plateau — off-diagonal corrections are the missing piece
- No prior library content on Li's criterion — fresh territory

**Meta-lessons returned:**
- Research-buffering stall is the #1 danger — include [SECTION COMPLETE] markers
- Staged computation + incremental writing is the prevention
- Save .npz after EACH computation block (against usage-limit death)
- scipy.optimize is BROKEN — include manual Brody fit as fallback
- Both: N=500 GUE gives Δ₃=0.23–0.26, NOT 0.566 (infinite-N theory)

---

## Explorations 001 & 002: Phase 1 Parallel Launch — 2026-03-27

### Options Considered

**Option A:** Run Phase 1 explorations (off-diagonal + Li) in parallel as STRATEGY.md specifies
**Option B:** Start with just off-diagonal (the most important), then Li sequentially
**Option C:** Start with the low-cost N²/p scaling verification (COMPUTATIONS-FOR-LATER item 12)

**Decision: Option A — run Phase 1 parallel as specified**

Rationale:
- STRATEGY.md is explicit: Phase 1 can and should run in parallel
- The off-diagonal computation (E001) is the single highest-value computation of the mission
- Li's criterion (E002) is independent and takes similar compute time
- Running them in parallel saves ~45-60 minutes of wall time
- N²/p scaling (Exploration E) is Phase 2 and should wait for Phase 1 results

**Explorer type: Math Explorer for both**
- E001: success criteria = "produces a number" — Math Explorer
- E002: pure mpmath computation — Math Explorer

### Session Prefix: `rh3`

---

## POST-LAUNCH NOTES (to be filled after explorations complete)

## E001 Post-Completion Reflection

**Result: PARTIAL SUCCESS**

**What was asked:** Extract off-diagonal form factor from Berry-Keating, compute K_total, predict Δ₃_sat.

**What was delivered:**
- Off-diagonal formula extracted: R²_c(x) = (1/(2(πρ̄)²)) × [-cos(2πx)/ξ² + |ζ(1+iξ)|² × Re{exp(2πix) × b(ξ)}]
- Critical finding: perturbative expansion requires ⟨d⟩ >> 1 (T >> 10^{10}); INVALID at T=1682
- R²_c gives only 1.6% gap closure (0.211 → 0.210 vs target 0.155)
- R¹_c blows up numerically at T=1682 (⟨d⟩=0.89, far from ⟨d⟩>>1)
- Correct Δ₃ route: Σ₂ → Δ₃ via (L³-2L²r+r³) kernel, verified to 3% against GUE matrices
- GUE Δ₃(N=500, L=20) = 0.217 (ground truth)

**Was scope right?** Yes, but the computation was slow. The formula extraction took a while, and the formula debug (wrong kernel) consumed ~20 minutes.

**Key insight:** The Berry-Keating off-diagonal corrections are NOT a valid explanation for the super-rigidity gap at T=1682. They're asymptotic formulas valid only for T >> 10^{10}. This is a fundamental limitation that was NOT obvious from the theory.

**What I'd do differently:**
- Provide the correct Σ₂ → Δ₃ formula explicitly in the goal (it was rediscovered after the wrong formula failed)
- Warn about the perturbative regime requirement
- Use 20-minute timeout instead of 10-minute

**Library inbox:** ✓ Dropped. Curator to be launched.

**Phase 2 implication:** Since perturbative corrections fail, Phase 2 should pursue:
1. Non-perturbative K(τ) directly from prime pair sums (no 1/⟨d⟩² expansion)
2. N²/p scaling verification (low-cost Claim A confirmation)
3. High-T verification using Odlyzko data (Phase 2 buffer option)

## E002 Post-Completion Reflection

**Result: SUCCEEDED**

**What was asked:** Compute Li coefficients λ_n for n=1..500, verify positivity, analyze patterns.

**What was delivered:**
- All 500 λ_n > 0 ✓ (confirms RH for truncated 2000-zero sum)
- λ_n grows as expected: 0.023 → 881 from n=1 to 500
- Key structural insight: |1-1/ρ|=1 for Re(ρ)=1/2 → convergence by phase cancellation
- λ_n^zeta/λ_n^GUE < 1 for n>300 → super-rigidity appears in Li coefficient space!
- Truncation convergence ratio r≈0.646, uniform across all n
- No prime correlation in residuals

**Was scope right?** Yes — exactly right. The goal specified 5 tasks and all were completed. The 10-minute timeout was tight for zero computation (needed ~9 min).

**Novel finding:** λ_n^zeta < λ_n^GUE for large n is interesting — it means the zeta zeros' Li coefficients grow slightly MORE SLOWLY than GUE's. Whether this encodes super-rigidity or is a truncation artifact needs investigation with larger zero sets.

**What I'd do differently:** Specify 15-minute timeout for the zeros computation. Also: ask the explorer to write to REPORT.md after EACH task rather than bulk at the end (REPORT was stuck at 33 lines for 20+ minutes).

**Library inbox:** ✓ Dropped. Curator launched.

---

## Phase 2 Launch: E003 + E004 — 2026-03-27

### Context
Both Phase 1 explorations are complete and processed. Library was queried. Key Phase 2 findings from the library:
- E001 confirmed: perturbative BK corrections invalid at T=1682 (⟨d⟩=0.89). Route: non-perturbative K(τ) from prime pair sums.
- E002 confirmed: all 500 λ_n > 0, super-rigidity signature in λ_n/λ_n^GUE ratio.
- N=500 Gauss sum baseline: β_peak=1.154 at p=809, N²/p_opt=309. Universality claim flagged as PREMATURE (single N).

### Decision: Launch E003 and E004 in parallel

**E003: Non-Perturbative K(τ) from Prime Pair Sums**
- Addresses the central mystery: can prime orbit correlations explain Δ₃_sat=0.155?
- Bypasses the perturbative expansion that failed in E001
- Route: empirical R₂(r) from zero pairs → K(τ) via FT → Σ₂ → Δ₃
- Secondary: Hardy-Littlewood b(ξ) Euler product (non-perturbative off-diagonal)

**E004: N²/p Scaling Universality**
- Tests whether N²/p ≈ 275 is universal or just an N=500 artifact
- Low-cost verification: mostly eigenvalue computations
- Would either strengthen Claim A (universal scaling law) or refute it

**Rejected alternatives:**
- E003-only (sequential): would waste ~90 min while E003 runs (parallel is clearly better)
- Li coefficients at large n (COMPUTATIONS #13): interesting but secondary; would confirm/refute a truncation artifact, not the main gap problem
- Flat-amplitude Δ₃ test (COMPUTATIONS #11): interesting for characterizing C1 matrix, but not the central gap

**Explorer type: Math Explorer for both** — pure computation, both have clear numerical success criteria.

**Session prefix: rh3**

---

## E003 Post-Completion Reflection

**Result: SUCCESS**

**What was asked:** Compute K(τ) non-perturbatively from zeta zero pair correlations, propagate via Σ₂ → Δ₃, determine if prime structure explains the 0.155 gap.

**What was delivered:**
- Tasks 0 & 1: Zero loading, unfolding, empirical R₂(r) — complete, high quality
- Task 2: K(τ) via Fourier transform of R₂ — qualitative, noisy, Gibbs spike at τ=1
- Task 4: Δ₃ via TWO methods — direct (0.1545, correct) and R₂ chain (0.220, 43% overestimate)
- Tasks 3, 5 skipped

**Key results:**
- Δ₃_sat = 0.1545 confirmed (direct sliding-window) [COMPUTED]
- GUE analytic = 0.294; ratio = 0.527 (47% more rigid)
- Saturation plateau is extremely flat (L=15 to L=30, <1% variation)
- R₂(1) = 0.921 for zeta vs ~1.0 for GUE (pair-level super-rigidity signature)

**Was scope right?** The goal was slightly too broad. The prime orbit K(τ) (Task 3) and Hardy-Littlewood enhancement (Task 5) got skipped because the explorer correctly prioritized Δ₃ confirmation. These are the most scientifically interesting parts and deserve their own exploration.

**Key lesson:** The integral chain R₂ → Σ₂ → Δ₃ requires 10,000+ zeros to be quantitatively reliable. For N=2000, use direct sliding-window only. This rules out the integral chain as a verification tool in this strategy.

**Implication for Phase 2:** The gap is confirmed. What's MISSING is the explanation — why does K(τ) for zeta zeros saturate at a lower level than GUE? Prime orbit sums (Task 3 skipped) are the theoretically predicted explanation. This should be E005 or E006.

---

## E004 Post-Completion Reflection

**Result: SUCCEEDED (negative)**

**What was asked:** Test N²/p universality for Gauss sum matrices with N=250 and N=1000.

**What was delivered:**
- Task 1: Baseline replication — Wigner histogram method reproduces S002 β=1.154 at p=809 [CHECKED]
- Task 2: N=250 sweep (26 primes) — peak β_W=1.318 at p=277, N²/p=225.6
- Task 3: N=1000 sweep (19 primes) — peak β_W=1.019 at p=4999, N²/p=200.0
- Task 4: Universality rejected — β_max decreasing with N (1.32→1.15→1.02), 1.5× spread in N²/p

**Key results:**
- N²/p universality REJECTED (decisive) [COMPUTED]
- Peak β_max decreases with N — finite-size effect
- S002 used Wigner (not Brody) — methodological discovery
- p≈N resonance identified (β→0 at p=N)

**Was scope right?** Yes — exactly the right tests. The nudge ("test these specific primes") was key to getting the explorer unstuck.

**Key lesson:** Same 3.5-hour stall pattern as E003. The cure is explicit row-by-row writing instructions: "after testing each prime p, write one result row to REPORT.md immediately."

**Phase 3 implications:**
- Gauss sum approach eliminated as a serious candidate
- 6 explorations remain: E005-E010
- Highest priority: K(τ) from prime orbit sums (the E003 Task 3 that was skipped) — this directly tests whether the diagonal approximation explains the gap
- Also valuable: adversarial review of novel claims (Li coefficient ratio, flat saturation plateau)

---

## E005: Prime Orbit K(τ) → Δ₃ Prediction — Phase 3 Launch

### Decision
E005 is the highest-priority exploration: compute K(τ) from prime orbit sums (Berry diagonal approximation) and check if it predicts Δ₃_sat ≈ 0.155.

This directly answers the central question of the mission: does the prime periodic orbit structure explain the spectral rigidity gap?

Options considered:
- **Option A: Prime orbit K(τ) (E005)** — directly tests Berry's mechanism, uses existing code framework
- **Option B: Novelty literature search (E005)** — valuable but lower impact; can do later
- **Option C: Large-n Li coefficients (E005)** — interesting but secondary to gap explanation

**Decision: Option A — prime orbit K(τ) is the most important remaining computation.**

Explorer type: Math Explorer (pure computation). Goal is focused: 5 tasks, each with explicit REPORT.md write instruction after completion.

Key design improvements from E003/E004 lessons:
- "Write to REPORT.md after EACH task" repeated prominently
- Two σ values tested in single computation run (avoid re-running)
- Data reuse from E003 (zeros already computed)
- Explicit timeout warning for prime sum loop


---

## E005 Reflection + E006 Decision

**E005 result:** Explorer navigated to wrong directory (strategy-002/exploration-005) and computed Gauss Δ₃ hierarchy instead of prime orbit K(τ). Results valid and valuable:
- Rigidity hierarchy: Zeta(0.155) < C1(0.285) < Gauss-best(0.415) < GUE(0.581)
- Δ₃/β decoupling: matrices with similar β can have 1.46× different Δ₃
- β→2 hypothesis definitively refuted (47 primes, all β<1.2)

**Key lesson:** Add explicit CWD confirmation as Task 0 of every Math Explorer goal.

**E006 decision:** Prime orbit K(τ) from Berry's diagonal approximation — this is the original E005 goal that was never attempted. It remains the highest-priority computation: does the prime orbit structure predict Δ₃_sat=0.155?

Budget: 4 explorations remaining (E006, E007, E008, E009, E010 = 5 total remaining).
Plan:
- E006: Prime orbit K(τ) → Δ₃ prediction (Math Explorer)
- E007: Adversarial/novelty review of key findings (Standard Explorer)
- E008: Final synthesis or focused follow-up on strongest novel claim
- E009-E010: Final report buffer

---

## E006 Post-Completion Reflection

**Result: PARTIAL SUCCESS**

**What was asked:** Compute K_primes(τ) from Berry diagonal approximation, predict Δ₃ via Wiener-Khinchin route, compare to 0.155 vs 0.294.

**What was delivered:**
- K_primes computed correctly (after discovering the 1/p^m normalization issue) — K_primes ≈ 0.94·τ for τ<1, decays to ~0 past τ=1 (max ~1.32 near τ≈1.1)
- Berry formula cross-check: 0.154 at T=600 (0.6% error), 0.167 at T=1127 (8% error) [COMPUTED]
- K→Σ₂ integral route produced ~2x too large values for GUE control (Δ₃(L=10) = 0.491 vs known 0.226)
- Relative comparison: K_primes_cap is only 3.3% above GUE through this route (not 47% different as the gap requires)

**Key insights:**
1. Berry's formula predicts 0.155 analytically (log(log(T)) growth is fundamentally slower than GUE log(L) growth)
2. K_primes is close to K_GUE for τ<1 — the super-rigidity is NOT visible in K at short times; it lives in the saturation behavior
3. The diagonal approximation cannot explain the gap via K→Σ₂ because K_primes≈0.94τ ≈ K_GUE=τ for τ<1
4. The GOAL.md had wrong weight: (log p)² should be (log p)²/p^m — important normalization bug identified

**Was scope right?** Yes, but I should have verified the formula against GUE analytic result BEFORE running the prime orbit computation. A 2-line sanity check (compute GUE Σ₂ from K_GUE, confirm Δ₃≈0.226 at L=10) would have caught the normalization issue immediately.

**What I'd do differently:** Always include a GUE control check step BEFORE running the main computation in goals that use the K→Σ₂→Δ₃ chain.

---

## E007 Planning

### Options Considered

**Option A: Standard Explorer — Adversarial/novelty review of key claims**
- Questions to address: Is the flat plateau known? Is Berry formula overestimate at high T explained? Is λ_n^zeta/λ_n^GUE documented?
- Does NOT fix the K→Σ₂ normalization issue
- Highest value for final report (validates novel claims)

**Option B: Math Explorer — Fix normalization, get definitive K_primes → Δ₃**
- Uses the E006 code, fixes the 2x normalization issue (factor in Fourier convention)
- Would answer "does the integral route give 0.155?" definitively
- But Berry's formula already gives a clear answer at 0.6-8% accuracy

**Option C: Standard Explorer — Literature deep-dive on Berry (1985) derivation mechanism**
- Understanding WHY Berry's formula gives log(log(T)) not log(L)
- This is conceptual/theoretical; no new computation

**Decision: Option A — adversarial/novelty review (Standard Explorer)**

Rationale:
- Berry's formula already gives a clear answer (0.154 at T=600, 0.167 at T=1127)
- The integral route has known issues but doesn't change the conclusion
- The most valuable thing now is assessing novelty of our key claims before writing the final report
- 3 explorations remain after E007 (E008, E009, E010)
- If novelty review reveals something unexpected, E008 can follow up

**Key claims to review:**
1. **Flat saturation plateau**: Δ₃(L) varies <1% from L=15 to L=30 for zeta zeros (E003). Is this in Berry/BK/Odlyzko?
2. **λ_n ratio**: λ_n^zeta/λ_n^GUE < 1 for n>300, falling to 0.95 at n=500 (E002). Is this documented?
3. **Berry formula accuracy**: 0.6% at T=600, 8% at T=1127 — is the growing discrepancy noted in literature?
4. **K_primes normalization**: (log p)²/p^m is the correct weight — is this in Berry (1985) explicitly?
5. **C1 matrix Δ₃**: 0.285 (intermediate between GUE and zeta) — any prior construction this close?

### Library Query Summary for E007

Queried library for: novelty assessment context for the 5 key claims from this strategy. Highly useful return.

**Pre-assessment from library:**
1. Flat plateau: NOT NOVEL — Berry (1985) predicted saturation at this level, Odlyzko confirmed numerically. Library has Δ₃_zeta=0.156 at L=50,100 confirming plateau extends. Not worth searching further.
2. λ_n ratio (crossover n≈300, ratio 0.95 at n=500): UNKNOWN — library has E002 results but NO prior literature search was done against Li/Coffey/BL/Keiper. This is the LIVE novel claim.
3. Berry formula accuracy (0.2%→12.5% with T): POSSIBLY WEAK — mechanism not in library. Berry (1985) may have discussion of correction terms at high T. Library has the quantitative table (our data) but no comparison to Berry's own analysis.
4. K_primes normalization (log p)²/p^m: WEAK — Berry (1985) is prior source. Not checking.
5. C1 Δ₃=0.285: RETRACTED — S002 flat-amplitude test showed Von Mangoldt amplitude plays no role; C1 within GUE-class range. Formally record retraction.

**Meta-lessons returned:**
- Use adversarial 4-part structure: (evidence, prior art, objection, verdict) per claim
- Name specific papers: Berry 1985, Li 1997, Coffey 2004, Keiper 1992, Bombieri-Lagarias 1999
- Include [SECTION COMPLETE] markers to prevent research-buffering stall
- "Find the closest prior work" framing for Claim 2 (Li literature)
- Rigor: paper-by-paper verdict table format

**Revised E007 scope**: Focus on Claims 2 and 3 (live unknowns). Claims 1, 4, 5 are pre-settled. This allows a tighter, more actionable exploration.

---

## E007 Post-Completion Reflection

**Result: PARTIAL SUCCESS** (Synthesis section not written, but key verdicts obtained)

**What was asked:** Adversarial literature search on 2 live claims.

**What was delivered:**
- Pre-settled claims section: complete
- Live Claim 1 (λ_n ratio): NOVEL (4/5) — zero prior papers found comparing λ_n^zeta to λ_n^GUE [FOUND]
- Live Claim 2 (Berry accuracy): ARTIFACT/WEAK (1-2/5) — sparse-sampling explains discrepancy [FOUND]
- Synthesis section: NOT written (explorer timed out in extended thinking)

**Key stall pattern:** Explorer researched for ~45 min (multiple context resets) before writing, despite nudges. Research-buffering on standard Explorer is worse than Math Explorer — the web search+fetch cycle encourages longer thinking chains.

**What I'd do differently:** Add explicit "write partial sections after 20 minutes regardless" instruction. The "[SECTION COMPLETE]" markers weren't followed; add "stop after 5 web searches for any one claim and write what you know."

**Most valuable output:** λ_n^zeta/λ_n^GUE crossover is NOVEL. No prior literature. This is the strongest surviving claim from the entire mission and justifies E008 validation.

---

## E008 Planning

### Decision: Validate λ_n ratio with more zeros + larger GUE ensemble

**The strongest claim from this strategy:** λ_n^zeta/λ_n^GUE < 1 for n>300, crossover at n≈300, ratio 0.95 at n=500. NOVEL per E007.

**Why validate?** E002 used 2000 zeros and GUE matrices N=100 (1000 realizations). The 0.95 ratio at n=500 could be:
- A genuine signal of super-rigidity encoding in Li space
- A finite-N artifact (N=100 GUE matrices are too small)
- A truncation artifact (2000 zeros not enough for n=500)

**E008 goal:** Math Explorer — compute λ_n ratio with:
- 5,000 zeta zeros (requires ~25 min mpmath computation)
- GUE N=300 matrices × 2,000 realizations (larger ensemble, larger N)
- Compare: does ratio at n=500 change? At n=1000?
- Statistical test: is ratio significantly < 1 or within noise?

**Rejected alternatives:**
- Literature synthesis only: Already done by E007
- Fix K→Σ₂ normalization: Would validate integral route but the Berry formula already gives 0.154 at T=600 with <1% error — the central question is answered
- Final report writing: Can do that directly after E008 without a separate exploration

**Budget plan:**
- E008: Math Explorer — λ_n ratio validation
- E009-E010: Write FINAL-REPORT.md directly (no new explorations needed)

Actually given budget constraints, I'll use E009 only if E008 raises something that needs follow-up. Otherwise E009 and E010 will be the final report.




---

## E008 Post-Completion Reflection

**Result: PARTIAL SUCCESS** — truncation analysis complete, K=N=5000 matched test incomplete

**What was asked:** Validate λ_n^zeta/λ_n^GUE crossover with 5000 zeros and N=300 GUE.

**What was delivered:**
- E002 exact replication with 100 GUE realizations (vs E002's 5) — crossover confirmed at K=N=2000 (7.3σ)
- Truncation analysis showing λ_500^zeta grows by +6.1% from K=2000 to K=5000 — CRITICAL FINDING
- N-dependence test: GUE λ_n scales linearly with N — only K=N comparison is valid
- At K=4500 zeros vs N=2000 GUE (unfair): ratio = 1.005 > 1, crossover DISAPPEARS
- K=N=5000 matched test: not completed due to context pressure at 52+ minutes

**Critical error in GOAL.md**: I stated λ_100^zeta = 59.72 and N=100 GUE. E008 found: λ_100^zeta = 114.18 and E002 actually used N=2000 GUE. My understanding of E002 was wrong. The explorer fixed this independently — important.

**Key insight gained:** The Li coefficient comparison is NOT simply "zeta vs GUE at same truncation level." Both series depend on the cutoff K=N in a non-trivial way. The question is whether the ratio λ_n^zeta(K)/λ_n^GUE(N=K) converges as K=N→∞, and if so to what value.

**What I'd do differently:** Scope to ONE computation: "compute ratio at K=N=500, 1000, 2000, 3000, 5000 and plot." Don't replicate E002 separately (waste of 20 min of computation), just load cached data and do the convergence analysis directly.

**Result for E009 planning:** Need to decide: do K=N=5000 matched test (definitive verdict) or write FINAL-REPORT now?

---

## E009 Planning

### Decision: Convergence Rate Analysis — Definitive Verdict on Novel Claim

**Context:** We have 2 explorations remaining (E009, E010). The main novel claim is "the λ_n ratio is genuine." E008 weakened it by showing truncation sensitivity. The decisive test is the convergence rate.

**The question:** What is lim_{K=N→∞} λ_500^zeta(K) / λ_500^GUE(N=K)?
- If → constant < 1: genuine structural difference between zeta zeros and GUE eigenvalues in Li space
- If → 1: truncation artifact — the claim is refuted

**We already have:**
- All 5000 zeros cached in E008's directory (exploration-008/code/)
- GUE λ_n for N=2000 (926, 100 realizations)
- GUE λ_n for N=3000 (1385, 50 realizations from N-dependence test)
- Formula and code already working

**What E009 needs to compute:**
- GUE λ_n(N=K) for K=500, 1000, 2000 (use cached), 3000 (use cached), 5000 (~10-20 realizations)
- All scaled to the same range as the K zeros
- Compute ratio at each K=N
- Plot: does ratio converge to constant < 1 or → 1?

**This is a focused 1-hour Math Explorer computation.** The key deliverable: a table of ratio vs K=N. Even 3 points (K=N=500, 1000, 2000) would show if the ratio is increasing toward 1 or stabilizing.

**E010 plan:** If E009 shows ratio converging to constant < 1 → adversarial check (30 min standard Explorer). If ratio → 1 → write FINAL-REPORT directly (skip E010 as exploration). Either way, FINAL-REPORT written after E009 or after E010.

**Library query plan:** Ask for any prior work on convergence of truncated Li sums, or comparison of growth rates of Li coefficients for different zero distributions.

### Librarian Query Summary for E009

**Query:** Prior work on convergence of Li criterion truncated sums; Li coefficient growth rate; comparison of λ_n growth for different zero distributions; RMT Li coefficient convergence.

**Returned:** (query to be sent below)

**Librarian query result for E009:** Returned highly useful context:
- Confirmed all 5000 zeros and GUE data cached in E008 directory
- Bombieri-Lagarias asymptotics (λ_n ~ n/2 log n) gives zeta growth rate; no literature on GUE Li coefficients
- Key meta-lesson: scope to MINIMUM computation (convergence rate sweep, not full replication)
- Recommended trial counts: K=500 (50), K=1000 (50), K=2000 (cached), K=3000 (30), K=5000 (10-20)
- GOAL.md designed to: load cached files, compute 4 new GUE levels, produce trend table

**E009 launched**: Math Explorer (rh3-explorer-009), 2026-03-28.

---

## E009 Post-Completion Reflection

**Result: SUCCEEDED** (negative result, definitively concluded)

**What was asked:** Compute matched ratio at K=N=500, 1000, 2000, 3000, 5000.

**What was delivered:**
- Complete convergence table: ratio 0.888 → 0.898 → 0.952 → 1.004 → 1.090 as K=N increases
- Root cause identification: linear GUE scaling creates density mismatch — GUE eigenvalues get diluted at high t as K grows
- Complete refutation of the novel claim

**Key surprise**: The ratio doesn't just approach 1.0 — it EXCEEDS 1.0 significantly (ratio 1.090, 9.7σ above 1 at K=N=5000). This means the GUE Li coefficient DECREASES as K=N grows (from 926 at K=2000 to 858 at K=5000), while zeta increases (881 → 935). Non-monotone GUE behavior is a real mathematical finding, even if the underlying comparison method is flawed.

**Methodological finding**: The correct comparison should use unfolded spectra (both zeta zeros and GUE eigenvalues normalized to unit mean spacing). The current linear-scaling comparison is not self-consistent for varying K=N.

**Decision for final report**: No novel claims survive from strategy-003. The mission's central findings are confirmations of known results (Δ₃=0.155, Berry formula). The methodology (comparing Li coefficients across ensembles) is novel but the specific comparison used is flawed. Recommend next strategy focus on fixing the comparison method or exploring other approaches to the super-rigidity gap.

---

## Final Report Planning

All 9 explorations complete. Writing FINAL-REPORT.md now.

**Key findings to report:**
1. Δ₃_sat=0.1545 confirmed (E003) — prior art, Berry 1985
2. Berry formula 0.154 at T=600, 0.6% accuracy (E006) — prior art
3. N²/p universality for Gauss matrices rejected (E004) — internal (S002 claim)
4. Rigidity hierarchy Zeta<C1<Gauss<GUE (E005) — computational, possibly novel but not well-motivated
5. Li coefficient crossover: REFUTED (E007-E009) — truncation artifact

**Novel claims section**: NONE survive full validation. Candidates considered but refuted or not novel:
- Flat plateau: NOT NOVEL (Berry 1985)
- Li crossover: ARTIFACT (E009)
- Berry accuracy: ARTIFACT (sparse sampling, E007)

**Recommendations for next strategy:**
- Fix K→Σ₂ normalization (2x bug in E006) — would validate the integral route
- Use properly unfolded Li comparison (unit mean spacing) instead of linear scaling
- Off-diagonal orbit pairs (Sieber-Richter) — the theoretically correct explanation for the super-rigidity, not yet explored computationally

**Budget**: 9/10 explorations used. Will write FINAL-REPORT.md as final action (counts as iteration 10).
