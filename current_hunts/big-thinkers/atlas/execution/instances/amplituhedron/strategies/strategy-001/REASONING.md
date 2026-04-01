# Reasoning Log

## Exploration 001: 4-Point Tree-Level MHV Amplitude — Three-Way Computation

### What I Considered

**Options for first exploration:**

1. **Broad landscape survey** — Have a standard explorer survey the state of the amplituhedron program, map what's been computed, what's open. Pro: builds a map for later explorations. Con: meta-lessons say this is exactly what standard explorers are good at, but the strategy explicitly says "compute, not philosophize." Also, I can learn the landscape from literature myself.

2. **4-point tree-level MHV computation via three methods** — Use a math explorer to implement spinor-helicity formalism in Python, compute the 4-point tree-level MHV amplitude via (a) Parke-Taylor / color-ordered Feynman diagrams, (b) BCFW recursion, (c) Grassmannian residues / positive geometry. Verify agreement numerically. Pro: builds computational infrastructure, exactly what Phase 1 calls for, one clear task with unambiguous success criteria. Con: might be "too easy" — 4-point tree-level is textbook.

3. **Jump straight to 6-point or 1-loop** — More ambitious, more interesting. Con: risk of scope explosion, and without the 4-point infrastructure, we'd have to build everything from scratch anyway.

4. **Survey + computation hybrid** — Survey the landscape of what's been computed, then compute the simplest case. Con: violates one-task-per-exploration meta-lesson.

### What I Chose and Why

**Option 2: 4-point tree-level three-way computation using a Math Explorer.**

Rationale:
- The strategy says "compute first." The simplest nontrivial case is the right starting point.
- All three methods (Parke-Taylor, BCFW, Grassmannian) are well-published with explicit formulas — so the math explorer can implement them, not derive them.
- The spinor-helicity code built here will be reusable infrastructure for all subsequent explorations.
- 4-point is "easy" but the three-way comparison + cost characterization is genuinely useful ground truth.
- If this works cleanly, exploration 002 can immediately push to 6-point or 1-loop.

### What I Rejected and Why

- Option 1 (survey): Too passive for a "compute first" strategy. The explorer would produce prose, not code.
- Option 3 (jump to 6-point/1-loop): Risk of the explorer getting bogged down without working infrastructure. Build the ladder one rung at a time.
- Option 4 (hybrid): Violates one-task-per-exploration. Split into two explorations if needed.

### Library Query

**Query:** Searched for amplituhedron, N=4 SYM, scattering amplitudes, positive geometry, Arkani-Hamed/Trnka work, and meta-lessons on computational explorations.

**Result:** The factual library has ZERO entries on amplituhedron or scattering amplitudes — completely unmapped territory. The meta library provided 16 relevant lessons, the most critical being: (1) one-task-per-exploration, (2) explorers can evaluate formulas but cannot perform novel computations — must provide specific formulas to evaluate, (3) request explicit equations, (4) specify rigor level, (5) tell the explorer "this is a computation task, not a research task."

**Usefulness:** Very useful. The meta-lessons directly shaped how I designed the goal — providing explicit formulas/references rather than asking for open-ended computation, and using the math explorer instead of standard explorer.

### Reflection (post-exploration)

The explorer delivered exactly what I asked: three working implementations, 10 verified kinematic points, all agreeing to machine precision. The scope was right — one amplitude, three methods.

**What I'd change:**
- Tell the explorer to break computation into modular scripts from the start. It wrote a 900-line monolith that timed out.
- Shorter goal prompt — 80 lines was probably too detailed. The explorer has good physics knowledge and can fill in details.
- The explorer got stuck in a 10-minute thinking loop after the timeout. Nudging was necessary and effective.

**What surprised me:**
- The angle-square duality observation (Grassmannian gives square-bracket result that equals Parke-Taylor's angle-bracket formula) is genuinely interesting structural insight. This wasn't in my goal — the explorer noticed it.
- The timing data is useful: for 4-point, Parke-Taylor is 41x faster than BCFW and 11x faster than Grassmannian. But at 4-point everything is trivial. Need higher multiplicity to see real divergence.

**Assessment:** Phase 1 ground truth partially established. We have working infrastructure and verified 4-point agreement. Need at least one more exploration for higher multiplicity or loop level before moving to Phase 2.

## Exploration 002: 6-Point MHV and NMHV — Where Methods Diverge

### What I Considered

1. **6-point MHV tree-level** — For MHV (k=2), the Grassmannian always has 1 residue regardless of n. So the amplituhedron computation stays O(n) while Feynman diagrams explode. Good scaling test. BCFW gives O(n) terms for MHV. This would show the Parke-Taylor formula generalizing cleanly.

2. **6-point NMHV tree-level** — This is k=3, n=6. The Grassmannian has E(3,2) = multiple residues. BCFW has multiple terms. This is where the amplituhedron really starts to differentiate itself — the canonical form of the NMHV amplituhedron is a sum over "cells" (BCFW tiles), and the geometry reveals hidden relationships between terms.

3. **4-point 1-loop** — New geometric structure but might be too technically complex for one exploration. The loop amplituhedron involves an additional "loop variable" in momentum-twistor space.

4. **Combine 6-point MHV + NMHV** — Violates one-task-per-exploration lesson.

### What I Chose and Why

**6-point NMHV tree-level via BCFW and Grassmannian.** This is the sweet spot:
- It's the simplest case where the Grassmannian has MULTIPLE residues (not just one as in MHV)
- The BCFW recursion produces multiple terms — so we can compare the structure of terms from both methods
- The Parke-Taylor formula doesn't directly apply to NMHV, so we need genuinely different methods
- Known analytic results exist (e.g., the R-invariants / 5-brackets from Drummond, Henn, Korchemsky, Sokatchev) as baselines
- This will establish whether the amplituhedron decomposition matches the BCFW decomposition or reveals finer structure

I'll skip the Feynman diagram approach entirely — it's intractable for 6-point NMHV (hundreds of diagrams) and the whole point is that modern methods bypass it.

### What I Rejected

- 6-point MHV: Too similar to 4-point in Grassmannian difficulty (still 1 residue). Doesn't push far enough.
- 4-point 1-loop: Better saved for Phase 2 after we've established tree-level patterns.
- Combined MHV+NMHV: One task per exploration.

### Reflection (post-exploration)

Partial success. The explorer established 6-point kinematics and MHV baselines, and found a genuine structural zero (Channel 3), but couldn't verify the BCFW computation — two independent shifts gave different answers.

**Root cause:** The cyclic color ordering of sub-amplitudes in BCFW factorization is ambiguous in set notation. This is a known subtlety but harder to get right in code than I anticipated.

**What I'd change:**
- Provide the R-invariant / momentum twistor 5-bracket formula as ground truth. Don't ask the explorer to verify BCFW against another BCFW implementation — they share the same bug class.
- The 6-point NMHV was too ambitious to both compute AND compare in one exploration. Should have split: (a) get the answer via R-invariants, (b) compare BCFW and Grassmannian against it.
- The explorer's thinking phases were extremely long (35+ minutes). Need a strategy for this — maybe shorter goals, or explicit time bounds in the goal.

**Assessment:** Phase 1 is only partially complete. I have verified 4-point agreement and 6-point MHV baseline, but 6-point NMHV is unresolved. I should pivot: instead of continuing to debug BCFW, use the R-invariant formula to get the correct answer, then move to Phase 2 (stress testing beyond N=4).

**Strategic decision:** I'm going to spend exploration 003 getting the 6-point NMHV answer via momentum twistor R-invariants and using it to fix/verify the BCFW. This completes Phase 1 ground truth. Then I can move to Phase 2 with confidence.

**Revised strategic decision (after further thought):** Actually, the strategy warns not to spend more than half the budget on Phase 1. I've spent 2 already. The 4-point ground truth is solid. The 6-point NMHV BCFW bug is a software debugging problem, not a physics insight. I should pivot to Phase 2 questions that could produce NOVEL findings, rather than continuing to debug. The 6-point fix can happen if/when needed.

## Exploration 003: Beyond N=4 SYM — Where Does Positive Geometry Break?

### What I Considered

1. **Fix 6-point NMHV with R-invariants** — Would complete Phase 1, but it's debugging, not physics. Low novelty potential.

2. **Beyond N=4 SYM** — The strategy says to "attempt to apply positive geometry to N<4 theories, pure Yang-Mills, or QCD-like amplitudes." This is where the mission gets interesting — characterizing where the geometric framework breaks. High novelty potential.

3. **1-loop amplituhedron** — New geometric structure at loop level. Interesting but technically demanding, and still within N=4 SYM.

4. **Cosmological polytopes** — Geometric approach to cosmological correlators. Fascinating but may be too disconnected from what we've built so far.

5. **Non-planar sector** — Where the amplituhedron is least understood. Could reveal fundamental limitations.

### What I Chose and Why

**A survey + computation exploration on extending positive geometry beyond N=4 SYM.** This is Phase 2 territory and directly addresses the mission's core question. I'll use a STANDARD explorer (not math) for this one — the goal is to map what exists and characterize what breaks, not to compute a specific amplitude.

Specifically:
- What is known about positive geometry for pure Yang-Mills (no supersymmetry)?
- What about N=1 or N=2 SYM?
- The associahedron (Bai & He) applies to bi-adjoint scalar theory — how does it relate to gluon amplitudes?
- Can the BCFW-based amplituhedron construction work without SUSY?
- What SPECIFICALLY breaks when you try to extend?

This should produce a clear "extension map" — where positive geometry works, where it doesn't, and WHY.

### What I Rejected

- Fix 6-point: debugging, not discovery. Can come back to it.
- 1-loop: still within N=4. The extension question is more fundamental.
- Cosmological polytopes: too disconnected from current progress.

### Reflection (post-exploration)

Excellent result. The standard explorer completed in ~20 min with a 563-line report — far more efficient than the math explorations. The two-tier structure (full amplituhedron only for N=4/ABJM, partial geometry much broader) is a sharp insight that directly answers the mission question.

**Key takeaway for remaining explorations:** The UV finiteness wall means the amplituhedron is NOT just a calculator — it encodes a specific physical property (UV finiteness). This is a Tier 3 finding: the geometric framework has physical content beyond just "efficient computation." The geometric framework REQUIRES UV finiteness, which is a physical property of the theory. This is deeper than "better calculator."

**Strategic implications:**
- Phase 2 is mostly done: we now know where the framework extends (tree-level broadly, all-loop only N=4) and where it breaks (UV divergences).
- Phase 3 should probe: (a) does locality/unitarity truly emerge from the geometry? (b) what happens in the non-planar sector? (c) can the UV finiteness requirement be made into a CONSTRUCTIVE principle (use positive geometry to constrain which theories are physically consistent)?

## Exploration 004: Emergent Locality and Unitarity — Physical Consequences

### What I Considered

Now in Phase 3 territory. Options for highest novelty potential:

1. **Emergent locality/unitarity** — The amplituhedron DERIVES locality and unitarity from geometry. This is the deepest claim. Are there specific computational examples where this emergence is visible? Are there "amplituhedron-allowed" objects that violate standard QFT axioms?

2. **UV finiteness as constructive principle** — Turn the finding from exploration 003 around: instead of asking "does positive geometry extend beyond UV-finite theories?", ask "can positive geometry PREDICT UV finiteness?" This would be a genuinely novel application.

3. **Non-planar amplituhedron** — Open problem, could produce insights but likely too technically hard.

4. **Fix 6-point NMHV** — Still needed for completeness but low novelty.

### What I Chose and Why

**Exploration 004: Emergent locality and unitarity.** This is where the amplituhedron makes its most radical claim: locality and unitarity are not inputs but outputs. I want to understand this precisely:

- HOW does locality emerge from the amplituhedron? What geometric property corresponds to locality?
- Are there deformations of the amplituhedron that produce "almost-local" or "almost-unitary" amplitudes?
- Does this give physical predictions? (E.g., does it constrain which UV completions of gravity are possible?)
- Is there any known computation where an "amplituhedron-allowed" object differs from standard QFT?

This should be a standard explorer (research + analysis), not math.

### What I Rejected

- UV finiteness as constructive principle: will pursue in exploration 005 if 004 goes well.
- Non-planar: too technically hard, low chance of success.
- Fix 6-point: debugging, not discovery. Low priority.

### Reflection (post-exploration)

Outstanding result. The explorer produced a 362-line report with 16 cited papers, a rigorous assessment table, and — most importantly — a brutally honest distinction between REFORMULATION and GENUINE CONTRIBUTION.

**Key strategic insight gained:** The answer to the mission question is now clearer than expected:
- Within N=4 SYM: reformulation (no new predictions)
- Beyond N=4 SYM: three genuine contributions (EFT-hedron, hidden zeros, UV selection principle)
- The March 2025 paper (arXiv:2503.03805) is the most exciting lead — emergence extending to non-SUSY at 1-loop

**What the remaining explorations should focus on:**
1. The March 2025 paper on hidden zeros at 1-loop (deep dive)
2. EFT-hedron bounds (computational verification)
3. The "surfaceology" program and where positive geometry is headed
4. Final synthesis and novel claims assessment

I'm at 4/10 explorations. The landscape is well-mapped. Now I should go deep on the most promising leads to see if there's anything genuinely novel to claim.

## Explorations 005 & 006: Parallel Deep Dives — Hidden Zeros + EFT-Hedron

### Strategic Decision: Running Two Explorations in Parallel

With 6 explorations remaining and the landscape well-mapped, I should maximize throughput. Two independent directions deserve deep investigation:

**Exploration 005: Hidden Zeros and the March 2025 Paper (Standard Explorer)**
- The discovery that phi³, pions, and gluons share hidden zeros is genuinely novel (2024)
- The March 2025 paper (arXiv:2503.03805) extends emergence to non-SUSY 1-loop — this is the frontier
- Need to understand: what exactly are hidden zeros, why do they imply locality/unitarity, and can this extend to higher loops or more theories?
- This is the highest-novelty direction

**Exploration 006: EFT-Hedron Computational Verification (Math Explorer)**
- The EFT-hedron gives specific bounds on Wilson coefficients — the most concrete physical consequence
- Want to COMPUTE specific bounds and verify them independently
- This would make the "physical consequences" claim concrete and verifiable

These are completely independent and should run in parallel.

### What I Rejected
- Surfaceology deep dive: interesting but potentially too disconnected from our main thread. Will do in 007 if budget allows.
- Fix 6-point NMHV: still low priority vs discovery potential.
- Non-planar amplituhedron: too technically hard.

### Reflection on Exploration 005 (Hidden Zeros)

Excellent result. The explorer found 15+ papers, extracted specific formulas and theorems, and produced a clear 461-line report in ~15 minutes. The hidden zeros program is indeed the most exciting frontier.

**Key strategic insights gained:**
1. The surfaceology framework is the common parent — amplituhedron and hidden zeros are branches of the same tree
2. Loop-level results live in "surface kinematics," not momentum space — this is a critical limitation
3. The program extends to cosmological wavefunctions — broader applicability than expected
4. 20+ papers in 2 years — this is a genuinely active frontier with rapid progress
5. The unique δ-deformation connecting scalar/pion/gluon is a deep structural result

**What this means for the remaining explorations:**
- The mission's answer is becoming clear: the amplituhedron IS more than a calculator — it's the N=4 branch of a broader principle (positive geometry → physical properties)
- The hidden zeros / surfaceology program shows this principle extends beyond N=4 SYM
- The most interesting open question: can surface kinematics be connected to standard momentum-space QFT?
- Worth exploring: the connection between hidden zeros and cosmological correlators

### Reflection on Exploration 006 (EFT-Hedron)

Excellent computational result. All 4 stages (partial waves, forward bounds, Hankel, photon) completed successfully. The unexpected insight about the non-monotonic saturation ratio is genuinely interesting — suggests the Hankel determinant could serve as a "spectroscopic tool" for UV physics from low-energy data.

Running 005 and 006 in parallel was the right decision — both completed in ~20 min, saving significant time vs serial execution.

**Strategic status:** 6 explorations done, 4 remaining. I have:
- Computational ground truth (exp 001: 4-point verified)
- Extension map (exp 003: two-tier structure, UV finiteness wall)
- Physical consequences (exp 004: reformulation + 3 genuine contributions)
- Frontier mapped (exp 005: hidden zeros, surfaceology)
- Computational verification (exp 006: EFT-hedron bounds work)

**What's missing for the final report:**
1. A synthesis exploration — bringing all findings together, assessing novel claims
2. Possibly one more deep dive on a specific technical point (surfaceology? cosmological polytopes?)
3. The COMPUTATIONS-FOR-LATER file needs updating

**Decision for remaining 4 explorations:**
- Exploration 007: Surfaceology deep dive (the common parent framework) — standard explorer
- Exploration 008: Adversarial review — challenge our strongest findings
- Keep 2 in reserve for follow-ups, then write FINAL-REPORT.md

## Exploration 007: Surfaceology — The Common Parent Framework

### What I Chose and Why

Exploration 005 revealed that "surfaceology" (curves on surfaces) is the COMMON PARENT framework that unifies the amplituhedron (N=4 SYM), hidden zeros, and potentially all positive geometry approaches. This is the missing piece: understanding the unifying structure.

Specifically, I want to know:
- What is surfaceology? (Curves on punctured disks/Riemann surfaces)
- How does it unify the amplituhedron with hidden zeros?
- What new predictions does it make?
- How does it connect to string theory (worldsheet → surface)?
- Is this the "final form" of the positive geometry program or still evolving?

Standard explorer — this is a literature survey.

### Reflection on Exploration 007 (Surfaceology)

Excellent result — 466 lines, 15+ papers, clear framework description. The critical insight: amplituhedron and surfaceology are PARALLEL programs (different theories, same philosophy), not nested. This was the missing structural understanding.

**Final strategic decision:** I'm at 7/10 explorations with comprehensive coverage:
- Phase 1 (Ground Truth): Completed (4-point verified, 6-point partial)
- Phase 2 (Extension/Stress Test): Completed (extension map, emergent L/U, EFT-hedron, hidden zeros)
- Phase 3 (Probe for Divergence/Novel): Completed (surfaceology, hidden zeros frontier)

The picture is clear. Rather than running 3 more explorations on increasingly narrow topics, I should synthesize now and write the FINAL-REPORT.md. The 7 explorations produced a coherent narrative that directly answers the mission question. Using the remaining budget on synthesis quality rather than exploration breadth is the right call.

