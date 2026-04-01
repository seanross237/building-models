# Reasoning Log

---

## Iteration 1 — Exploration 001

### Context
Starting strategy-002 fresh. Strategy-001 completed 10 explorations and produced:
- Complete obstruction atlas (9 approaches, 5 bottleneck theorems)
- Quantitative demonstration that Adhikari-Cao bounds are 57-69x vacuous for SU(2) subgroups
- Binary icosahedral group reproduces SU(2) observables to <0.5%
- Identified SZZ (Shen-Zhu-Zhu) + RG as most promising unexplored combination

Strategy-002 mandate: Constructive attack on SZZ extension. No pure literature surveys — every exploration must compute, prove, or stress-test.

### Options Considered

**Option A:** Run exploration-001 and exploration-002 sequentially (SZZ extraction first, then Poincaré computation). Safer — computation benefits from knowing exact SZZ technique.

**Option B:** Run exploration-001 (SZZ extraction, Standard) and exploration-002 (Poincaré constant computation, Math) in parallel. The computation is well-defined regardless of SZZ's exact technique — we're measuring autocorrelation times of SU(2) Gibbs measure at various β, which doesn't need the SZZ proof details.

**Option C:** Start with the SZZ+Chatterjee combination check (exploration-003) since it's the highest-value potential finding (novel theorem from existing pieces).

### Decision
**Chose Option B: parallel explorers for 001 and 002.**

Rationale:
- Exploration-001 (SZZ extraction) and Exploration-002 (Poincaré constant measurement) are fully independent. The computation in exploration-002 is well-scoped: measure autocorrelation times for SU(2) Langevin/Metropolis at β = 0.02, 0.05, 0.1, 0.5, 1.0, 2.0 — this directly tests whether the spectral gap degrades as β increases past the SZZ threshold.
- Running in parallel saves real time and preserves the 10-exploration budget for more intensive work in Phase 2.
- Exploration-003 (SZZ+Chatterjee combination) is better run AFTER seeing exploration-001's results — the exact form of SZZ's mass gap matters for whether it satisfies Chatterjee's "strong mass gap" definition.

### What I Rejected
- Starting with the Lean formalization (Phase 3 task — too early without knowing what we're formalizing)
- Running exploration-003 first (need exploration-001's results to design it well)
- Running exploration-001 and exploration-002 sequentially (parallel saves ~30-40 minutes)

### Librarian Query Summary

**Queried about:** SZZ Bakry-Émery technique details, Poincaré/log-Sobolev inequalities, how β < 1/48 arises, whether SZZ satisfies Chatterjee's "strong mass gap" condition, prior spectral gap measurements, and meta lessons about goal design.

**Key findings returned:**

1. **SZZ technique (factual library):** The library has a high-level account of SZZ but NOT the step-by-step curvature calculation. Knows: (a) they verify Bakry-Émery condition (positive Ricci curvature of config space) → Poincaré + log-Sobolev inequality → exponential decay of correlations; (b) β < 1/48 comes from the threshold where SU(N)'s intrinsic Ricci curvature dominates the action's negative curvature contributions; (c) at weak coupling, gauge fluctuations dominate and the bound fails. Does NOT have: the explicit curvature formula, the exact Bakry-Émery tensor calculation, or the precise derivation of the 1/(16(d-1)) prefactor.

2. **SZZ + Chatterjee (factual library):** Chatterjee's "strong mass gap" requires exponential decay under ARBITRARY BOUNDARY CONDITIONS, uniformly in volume. SZZ proves exponential decay on torus T⁴ (finite volume). The library does NOT confirm whether SZZ satisfies the uniform-in-boundary-conditions requirement. SZZ is used in Adhikari-Suzuki-Zhou-Zhuang 2025 (area law in 't Hooft limit) via Chatterjee's theorem, which is suggestive but not definitive.

3. **Spectral gap measurements (factual library):** No prior measurements of Poincaré constant or autocorrelation time vs. β for SU(2) in the library. E003 code exists (SU(2) heat bath, at `../strategy-001/explorations/exploration-003/code/`). E008 code exists (autocorrelation code, at `../strategy-001/explorations/exploration-008/code/`) but was written for finite groups, not SU(2).

4. **Meta lesson (critical):** E008's spectral gap computation TIMED OUT because the explorer spent 25 minutes thinking instead of computing. Mitigation for E002: instruct "compute first, report second," print numbers immediately, save code to files before running.

5. **Meta lesson:** Use "EXACTLY" in questions to force theorem-level precision (worked well in E006). Name specific papers. Preload SZZ library content into goal. State "YANG-MILLS mission" explicitly.

**Assessment:** The librarian's most important find is the E008 autocorrelation code (available to reuse) and the warning about the E008 timeout pattern. For exploration-002, I will instruct the explorer to run computation immediately and print results, rather than planning an elaborate setup.

### Reflection After Explorations 001 and 002

**E001 (SZZ technique extraction):** Delivered exactly what was asked. The exact Bakry-Émery formula K_S = N/2 - 8N(d-1)β was extracted with the precise factor derivation. The unexpected finding — that Cao-Nissim-Sheffield (Sept 2025) already doubled the threshold to 1/24 using a vertex σ-model — is the most important result. This means the "SZZ + Chatterjee → novel area law" we were hoping to assemble is already in the literature (at a better threshold). Scope was right. The API error/long write time (~30 min) was the only problem — a reflection of the explorer composing a large (507-line) report in one pass. Future exploration goals should explicitly say "write incrementally, not in one large write."

**E002 (spectral gap scan):** The explorer self-diagnosed and fixed a parallelism bug in the heat bath algorithm — a sign of high competence. Results are 8 clean data points with verified plaquette values. The key finding (γ > 0 for all β) is physically meaningful and the critical slowing down near β_c is correctly identified. The slow computation (~8 minutes per β value on a 4⁴ lattice) means larger lattices are not feasible in one explorer run — need to plan Phase 2 computations with tighter scope.

**Strategic revision after Phase 1:** The discovery of CNS 2025 (doubling SZZ threshold from 1/48 to 1/24) changes the Phase 2 targets:
- ORIGINAL: Test RG+Bakry-Émery idea to push from 1/48 to ~1/12
- REVISED: Test RG+Bakry-Émery idea to push from 1/24 to ~1/12 (using CNS as starting point, not SZZ)
- The vertex σ-model formulation (CNS) is the better base, not the edge formulation (SZZ)

---

## Iteration 2 — Exploration 003

### Context
Phase 1 task 3 originally: "Check whether SZZ + Chatterjee gives an unpublished theorem."
Result from E001: This combination (SZZ + Chatterjee → area law) is already in the literature via CNS at a better threshold. So this specific goal is superseded.

**Pivot:** The remaining high-value Phase 1 task is to understand the CNS improvement (1/48 → 1/24) in detail, and determine what the BEST achievable threshold is under the Bakry-Émery framework. Specifically: what does the master loop equation approach (CNS May 2025, arXiv:2505.16585) give for β₀(d)? If β₀(d) > 1/24, that's the new state of the art.

### Options Considered

**Option A:** Extract CNS May 2025 master loop equation paper — what is β₀(d)? Can it be computed? (Standard Explorer, ~20 min)

**Option B:** Compute Hessian sharpness numerically for SU(2) — is the Lemma 4.1 bound 8(d-1)Nβ tight or loose? (Math Explorer, ~30 min)

**Option C:** Deep extract CNS Sept 2025 (arXiv:2509.04688) — exactly how does the vertex σ-model give Hessian = 4(d-1)Nβ? Can we find a yet-finer formulation? (Standard Explorer)

### Decision
**Option A: Extract CNS May 2025 master loop approach.**

Rationale: The master loop equation approach potentially gives area law for ALL β (without explicit threshold) via string duality. If β₀(d) is computable and turns out to be > 1/24, this gives the strongest current state of the art. Even if β₀(d) < 1/24, understanding the complementary approach helps decide where Phase 2 should focus (Bakry-Émery extension vs. master loop extension). This is Phase 1 work — extracting and synthesizing the literature.

### What I Rejected
- Option B (Hessian sharpness): This is clearly a Math Explorer Phase 2 task. Running it now would use a Phase 1 exploration on Phase 2 work.
- Option C (CNS Sept 2025): E001 already extracted enough context on this paper (how vertex formulation gives factor-2 improvement). Doing a full deep extraction of the same paper would be redundant.

### Reflection After Exploration 003

**E003:** Clean execution. The explorer found the answer directly in the paper's own Remark 1.1 ("CNS Sept 2025 achieves a larger β range"). β₀(4) < 1/24. Scope was right.

**Strategic implications:**
- Phase 1 is complete. The landscape is now clear:
  - Best explicit threshold: β < 1/24 (Bakry-Émery on vertices, CNS Sept 2025)
  - Master loop: β < 1/87 (worse range, better N-scaling)
  - Physical target: β ≈ 2.0 (48× gap from 1/24)
  - Novel combination: prove area law at β < 1/24 with N-independent string tension (Remark 1.4 of CNS May 2025)

- **Phase 2 revision:** The original Phase 2 plan (RG+Bakry-Émery) is still valid, but now I have a clearer picture of the landscape. Two targets emerge:
  1. **Extend the threshold beyond 1/24** (the hard goal) — via RG+Bakry-Émery or tighter Hessian bounds
  2. **Fix N-scaling of the β < 1/24 result** (the modest goal) — via combining master loop with Bakry-Émery at β < 1/24

I'll pursue both in Phase 2 with parallel explorations.

### Reflection After Explorations 004, 005, and 006

**E004 (master loop optimization):** Clean computation. Key: ambiguity about C_eff = 8de vs 8e unresolved. Could have been merged with E003.

**E005 (Hessian sharpness 3D): MAJOR UNEXPECTED FINDING.** The 12-45× slack was unexpected. Correctly flagged as needing 4D verification.

**E006 (Hessian sharpness 4D): CONFIRMED AND AMPLIFIED.** 4D slack is 29-138× (larger than 3D). Adversarial search found no configuration with H_norm > 0.01. This is the strongest result of the strategy. The bound is genuinely loose — not a dimensional artifact, not a sampling artifact.

**Physical implication:** At β = 0.5 (4D), the actual Bakry-Émery condition K_S = 1 - actual_max_Hess × 48 × 0.5 = 1 - 0.485 = 0.515 > 0. The condition NUMERICALLY HOLDS at β = 0.5, which is 24× the SZZ threshold.

**What's needed for a novel mathematical claim:**
- An analytic proof that H_norm ≤ c for some c < 1 in the appropriate regime
- The physical mechanism is: sign cancellations from 2(d-1) independent plaquette contributions (each edge in 4D is shared by 6 plaquettes, which have approximately independent contributions in the weakly coupled regime)
- If a CLT-type argument gives c ≈ 1/√(2(d-1)) ≈ 1/√6 ≈ 0.41, threshold improves from 1/48 to 0.41/48 ≈ 1/10. The observed c ≈ 0.007-0.034 is MUCH smaller than 1/√6, suggesting additional structure beyond CLT.

**BUDGET NOTE:** 6 explorations used, 4 remaining. Use E007 for adversarial review, E008 for analytic proof search, E009 for Lean formalization or additional computation, E010 for final report.

---

## Iteration 7 — Exploration 007 (Adversarial Review)

### Context
We have a potentially novel finding: SZZ Lemma 4.1 Hessian bound is 29-138× loose in 4D. Before investing E008 in proving a tighter bound, I need an adversarial review to check whether:
1. There's a theoretical reason the bound can't be improved (some configurations we haven't tested)
2. The bound actually IS tight for some class of configurations (e.g., at weak coupling β → ∞ where H_norm grows toward 1)
3. The physical mechanism (plaquette cancellations) is already well-known in the literature

### Decision: E007 = Adversarial Review (Standard Explorer)

The review should:
- Challenge the Hessian slack finding on multiple fronts
- Search for literature on plaquette cancellations / tighter Bakry-Émery bounds
- Assess whether the implied extension to β ≈ 0.5 is theoretically sound
- Identify the most likely source of error or overestimation

### Reflection After Exploration 007

**E007 (adversarial review): THE BEST EXPLORATION OF THE STRATEGY.** Found:
1. H_norm ≤ 1/12 analytically (staggered mode at identity)
2. E006 adversarial search was 14× weaker than E007's structured analysis
3. If provable, gives β < 1/4 (12× SZZ, 6× CNS)
4. The formula H_norm = 4/(3d) = 1/12 is NOT in the prior literature

**Corrected strategic assessment:**
- The "138× slack" claim was wrong — the actual worst case is 12× slack
- The implied threshold is β < 1/4 (not β < 0.5 as E006 suggested)
- This is STILL a significant improvement over the current best (1/24)
- The proof structure is clean and ~30-line

**Adversarial review lesson:** Should have run adversarial review MUCH EARLIER (after E005, not after E006). The adversarial reviewer immediately found the tight bound. Next time: run adversarial review after the first "unexpected finding" exploration.

---

## Iteration 8 — Explorations 008 and 009 (Parallel)

### Context
Budget: 7 done (001-007), 3 remaining (008-010). Phase 3 begins.

The key remaining task is to PROVE H_norm ≤ 1/12 rigorously. If this is proved:
- New Lemma replacing SZZ Lemma 4.1: max HessS / (|v|² × 8(d-1)Nβ) ≤ 4/(3d)
- New threshold: β < 3Nd/(32(d-1)) = 1/4 for SU(2) in d=4
- This is 12× better than SZZ (1/48) and 6× better than CNS (1/24)

Two things needed:
1. **E008:** Prove max H_norm ≤ 1/12 rigorously (Math Explorer — ~30-line formal calculation)
2. **E009:** Verify the staggered mode IS the global maximum (Math Explorer — full Hessian matrix eigenvalue computation for the 4D identity configuration)

These can run in parallel.

### Decision: E008 and E009 in parallel

**E008 (Math Explorer):**
- Goal: Prove analytically that for ANY Q ∈ SU(N)^E and any tangent v:
  |HessS(v,v)| / (|v|² × 8(d-1)Nβ) ≤ 4/(3d)
- The key steps: (1) At identity Q=I, the per-plaquette Hessian contribution for staggered mode = 4β; (2) For the staggered pattern, exactly 4 of 6 plane-pairs contribute (2 cancel to zero); (3) The same geometric cancellation holds for any Q (since |Hess_plaq| ≤ 4β always); (4) Sum over all plaquettes and normalize
- If this works: write a clean formal "Lemma X" with complete proof

**E009 (Math Explorer):**
- Goal: Compute the full Hessian matrix of the Wilson action at Q=I for SU(2) on a 4⁴ lattice, find its maximum eigenvalue, and verify it equals 4β
- This confirms the staggered mode is the TRUE global maximum, not just a local one
- Simultaneously: test the formula H_norm = ⌊d/2⌋⌈d/2⌉/(4d(d-1)) for d=5,6

After E008 and E009, I will write FINAL-REPORT.md (exploration 010 will be the final adversarial review + novel claims synthesis, or I'll skip it and use E010 for the final report).

### What I Rejected
- Lean 4 formalization: Would take too long (Lean 4 formalization is expert-level work requiring months). The ~30-line proof is better served by a clear mathematical writeup (E008) than a Lean formalization.
- Only 1 remaining exploration instead of 2: There are 2 essential tasks (proof + eigenvalue verification) that are both important and independent. Parallel is the right call.




**E004 (master loop optimization):** Clean computation, all results from closed-form formulas. The β₀(4)_max ≈ 1/87 result is solid. The critical ambiguity (C_eff = 8de vs 8e) is important — if 8e, master loops already beat Bakry-Émery! This must be resolved from the paper. Budget note: this exploration could have been merged with E003 (asking the same explorer to do the optimization after extracting β₀). Will optimize for future.

**E005 (Hessian sharpness): MAJOR UNEXPECTED FINDING.** The 12-45× slack in Lemma 4.1 was completely unexpected. This is potentially the most important numerical result in this strategy. Key caveat: the measurement used a 3D lattice, not 4D. The result must be verified on a 4D lattice before it can inform the proof strategy. Also, the worst-case configuration (non-Gibbs) might still saturate the bound.

**Phase 2 revision:** The Hessian slack finding changes Phase 2's priority. The RG blocking step is now SECONDARY to:
1. Verifying the Hessian slack on a 4D lattice (and searching for worst-case configs)
2. Finding the analytic explanation for the cancellations
3. Assessing whether the slack can be exploited in a rigorous proof

---

## Iteration 5 — Exploration 006

### Context
Budget: 4 explorations remaining (006-009, then 010 for final report and adversarial). Wait — let me recount: we've done 001-005 (5 explorations), 5 remaining (006-010).

Phase 2 remaining: 2 explorations (006, 007). Phase 3: 3 explorations (008-010).

### Decision for E006

**Goal: Verify Hessian slack on 4D lattice and search for worst-case configurations.**

This is the highest-priority Phase 2 task. The 3D result is suggestive but not directly applicable to the Yang-Mills (d=4) case. Must verify:
1. 4D lattice Hessian measurement: is max h_norm still << 1?
2. Worst-case search: gradient ascent to find config Q and tangent v that maximize h_norm

If h_norm stays << 1 in 4D too, this is a strong indication that the Lemma 4.1 bound has structural slack, not just dimensional artifact.

### What I Rejected
- RG blocking step: This is harder to implement correctly (needs gauge fixing) and less urgent given the Hessian slack finding. Save for E007 or Phase 3.
- Adversarial review: Too early — I should complete the key computations before the adversarial review. The adversarial review will be E007.



### Context
Phase 2 begins. Budget: 7 explorations remaining (004-010). Phase 2 target: 4 explorations.

**Two independent Phase 2 tasks that can run in parallel:**

**E004 (Math Explorer):** Optimize master loop contraction estimate. 20-line numpy optimization to pin down β₀(d) true maximum. ~15-20 min.

**E005 (Math Explorer):** Hessian sharpness check for SU(2). Monte Carlo measurement of actual |HessS(v,v)|/|v|² at β = 0.02, 0.1, 0.5 to quantify slack in Lemma 4.1 bound (8(d-1)Nβ = 48β for SU(2) in d=4). ~30-40 min.

### Why These Two In Parallel?

1. They are fully independent (different computations, different code)
2. E004 is small (20 lines) and can likely finish while E005 is still running
3. Together they answer: "Can the Bakry-Émery threshold be pushed beyond 1/24 without changing the proof architecture?"
   - E004 tells us whether master loop can help
   - E005 tells us whether the Hessian bound has room

### What I Considered

**Option: RG blocking step first (E004).** This is the harder computation but more strategically important. If RG blocking reduces the effective coupling β_eff below 1/24, we've potentially extended the result. However, implementing correct Balaban-style RG is complex (needs gauge fixing, ~200 lines). Better to save this for after the simpler computations confirm there's slack to exploit.

**Decision: Run E004 (master loop optimization) and E005 (Hessian sharpness) in parallel first.** These are fast (15-40 min), inform whether there's room in the existing methods, and the results will guide whether E006 should be RG blocking or something else.





---

## Iteration 9-10: Processing E008 and E009 Results + Planning E010

### E008 and E009 Outcomes

**E009 (Math Explorer, eigenvalue verification):**
- VERIFIED: λ_max = 4β at Q=I under SZZ convention S = -(β/N)Re Tr
- Staggered mode IS the maximum eigenvector (9-fold degenerate, zero residual)
- 5 random Q all give λ_max ≈ 2β < 4β — Q=I appears to be the worst case
- d=5 SURPRISE: staggered mode NOT the max eigenvector there (true λ_max = 5β, residual = 0.98)
- Formula correction: ⌈d/2⌉⌊d/2⌋/(N²d(d-1)) gives 1/12 for d=3,4 but staggered mode isn't tight for d≥5
- Convention warning: without 1/N, λ_max = 8β and H_norm = 1/6 (wrong)

**E008 (Standard Explorer, proof):**
- PROVED at Q=I: H_norm ≤ 1/12 via Fourier analysis of the discrete curl operator
- PROVED for all Q: H_norm ≤ 1/8 (triangle inequality, rigorous) → threshold β < 1/6 (8× SZZ, 4× CNS)
- GAP: ∑_□ |B_□(Q,v)|² ≤ 4d|v|² is the one missing step for full H_norm ≤ 1/12 for all Q
- Lemma A (proved at Q=I) + Corollary B (under conjecture): β < N²/(4d) = 1/4 for SU(2), d=4
- Literature check: Result appears novel — Fourier analysis of discrete curl, staggered mode maximizer, improved threshold not in SZZ/CNS/related papers
- Formula correction: GOAL.md had wrong formula (4/(3d)); correct is ⌈d/2⌉⌊d/2⌋/(N²d(d-1))

### What We Know Now

At iteration 10 (using 9 of 10 explorations), the picture is:

**Proved rigorously:**
1. H_norm ≤ 1/12 at Q=I (Fourier + discrete curl analysis)
2. H_norm ≤ 1/8 for all Q (triangle inequality) → β < 1/6 PROVED (8× SZZ, 4× CNS)
3. Staggered mode achieves H_norm = 1/12 exactly (E009 verified, zero residual)

**Strongly supported but not proved:**
4. H_norm ≤ 1/12 for all Q (needs ∑_□ |B_□|² ≤ 4d|v|²)
5. Q=I is the global worst-case (5 random Q all gave < 4β, E009)
6. β < 1/4 threshold (if conjecture 4 is proved)

**Unexpectedly found:**
7. d=5 doesn't fit the simple formula — staggered mode not the max eigenvector there

### E010 Planning

This is the last exploration. Options:

**Option A (Math Explorer): Prove/disprove ∑_□ |B_□(Q,v)|² ≤ 4d|v|²**
- Try temporal gauge fixing (Q_{x,0}=I) to reduce the problem
- Run numerical scan: 100+ diverse Q configs to test H_norm ≤ 1/12
- If proved: novel theorem complete (β < 1/4 rigorous)
- If disproved: find the true maximum H_norm bound

**Option B (Standard Explorer): Final adversarial synthesis + novelty search**
- Deep search for papers with Fourier analysis of Wilson action Hessian
- Adversarial review of the E008 Fourier proof (check each step)
- Prepare novel claims section for FINAL-REPORT

**Decision: Option A (Math Explorer)**

Rationale: We already have a strong novel claim (β < 1/6 proved rigorously). The open conjecture (β < 1/4) is the most valuable thing to resolve. A Math Explorer can:
1. Scan 100+ Q configs numerically (30-50 min of computation)
2. Attempt the temporal gauge proof strategy
3. Verify SZZ convention explicitly (read their paper Section 2)
4. Provide a definitive answer to: "Is H_norm ≤ 1/12 for all Q?"

If the scan finds no counterexample among 100+ diverse configs, that's strong numerical evidence. If the temporal gauge argument works, that's a proof. Either way, E010 produces the best possible evidence for the final report.

I am NOT pursuing: separate adversarial review (E008 already assessed novelty), separate convention audit (E009 already identified the key convention). These can be brief sub-tasks within E010.

**E010 goal:** Math Explorer — (1) Large H_norm numerical scan (100+ configs), (2) Temporal gauge proof attempt for ∑_□ |B_□|² ≤ 4d|v|², (3) SZZ convention verification.
