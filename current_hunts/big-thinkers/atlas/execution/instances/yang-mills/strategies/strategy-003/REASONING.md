# Reasoning Log — Strategy 003

## Startup

Strategy-003 is a finishing strategy with one specific goal: prove or disprove ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for all Q ∈ SU(N)^E.

Prior state:
- Strategy 002 proved H_norm ≤ 1/12 at Q=I (Fourier) and H_norm ≤ 1/8 for all Q (triangle).
- Strategy 002 numerically confirmed H_norm ≤ 1/12 for 100 diverse L=2 configs with zero counterexamples.
- The one remaining gap: ∑_□ |B_□(Q,v)|² ≤ 4d|v|² for general Q.

## Iteration 1: Phase 1 — Parallel Proof Tournament

### Decision
Per STRATEGY.md, Phase 1 launches 4 independent explorations in parallel:
1. E001: Representation theory approach (Standard Explorer)
2. E002: Geodesic convexity approach (Standard Explorer)
3. E003: Gauge-covariant Fourier approach (Standard Explorer)
4. E004: Large-lattice (L=4) verification (Math Explorer)

Each proof attempt is completely independent — no cross-contamination of approaches.
The Math Explorer gets the verification task since it requires code.

Session prefix: ym3

---

## Phase 1 Complete → Phase 2 Launch (Iterations 1-4)

### Phase 1 Synthesis

All 4 Phase 1 explorations produced useful results. Key convergence:

**Convergent findings (all 4 agree):**
- H_norm ≤ 1/12 = 0.08333 holds for all tested configurations (L=2 and L=4, 500+ total)
- Zero counterexamples even under analytical gradient adversarial search
- Q=I is the unique maximizer of F(Q) = λ_max(M(Q))

**Critical structural discovery (E002):**
- F(Q) = 4d = 16 IFF Q is a pure gauge configuration (all plaquette holonomies = I)
- Non-pure-gauge Q gives F(Q) < 4d strictly
- For pure gauge Q, M(Q) is isospectral with M(I) (via gauge transformation isometry)

**B_P proof chain broken (E004):**
- Per-plaquette: H_P ≤ (β/2N)|B_P|² is FALSE for Q≠I (ratio up to 8383×)
- Global sum: Σ H_P ≤ (β/2N)Σ|B_P|² is ALSO FALSE at v_max (ratio 1.94×)
- BUT: Σ|B_P|² ≤ 4d|v|² is TRUE (E004 Step 2, max ratio 7.4/16)
- Must use direct spectral approach

**Formula corrections (E001/E002):**
- GOAL.MD B_□ formula had errors in transport for backward edges
- Corrected formula verified by finite differences

**Key proof targets identified:**
- R(Q) ≼ 0 (Weitzenböck curvature correction, identified by E001/E003)
- M(Q) ≼ M(I) directly via pure gauge characterization (E002)
- Jiang (2022) discrete Weitzenböck formula is the key tool

### Phase 2 Decision

Phase 2 launches 3 parallel explorations targeting the one remaining gap:

**E005 (Standard Explorer):** Extract Jiang (2022) Weitzenböck R(Q) formula + SZZ literature. Determine if R(Q) ≼ 0 is provable from the explicit formula.

**E006 (Math Explorer):** Full operator M(Q) - M(I) eigenvalue scan (ALL eigenvalues, not just max). Verify pure gauge isometry analytically + numerically. Gradient ascent on λ_max(M(Q)-M(I)).

**E007 (Standard Explorer):** Attempt analytical proof via pure gauge orbit + SU(2)-specific identities. Focus on staggered mode per-plaquette bound.

### Pacing note

Phase 1 used 4 explorations (as planned). Phase 2 uses 3 (E005-E007). That leaves 3 for Phase 3 (E008-E010). Phase 3 will be:
- E008: final synthesis/adversarial review of novel claims
- E009: formal theorem statement + proof assembly
- E010: (if needed) final gap-filling or larger-scale verification

If Phase 2 produces a complete proof, Phase 3 can compress to 2 explorations (adversarial review + final report synthesis).

### Meta-reflection on E002/E003 compaction issues

Both E002 and E003 spent 70%+ context in deep thinking before writing anything, then compacted, required killing/relaunching. Pattern: standard explorers on long math derivations should be nudged at 40-50% context, not 80%. The "queued messages" state (where multiple nudge messages pile up) requires killing the session to resolve — additional nudges make it worse. Going forward: one nudge at 40%, one strong nudge at 60%, kill at 70%.

---

## Phase 2 Reflections: E005 and E007 Completed

### E005 Reflection

E005 delivered a CRITICAL CORRECTION: the full operator inequality M(Q) ≼ M(I) is FALSE. Prior explorations conflated "λ_max(M(Q)) ≤ 4d" with the full PSD ordering — these are fundamentally different. E005 clarified the correct target: R(Q)|_{top eigenspace} ≼ 0, which is equivalent to λ_max ≤ 4d.

Did the explorer answer what was asked? Partially. It was asked to extract the Jiang (2022) formula and determine R(Q) ≼ 0 sign. It did find Jiang (2022) (arXiv:2211.17195) but found the paper doesn't prove what we need. More importantly, it independently computed R(Q) and discovered the full operator inequality is false. This was MORE valuable than the literature extraction.

Scope was right. The computation + literature dual approach was good. The nudge at 37% worked — it unlocked 180 more lines of output.

The key finding (full operator ordering FALSE) should inform E008-E010 goals: they must target λ_max ≤ 4d, not M(Q) ≼ M(I).

### E007 Reflection

E007 attempted to prove M(Q) ≼ M(I) — which is false. So the main proof target failed. However, E007 produced two valuable outputs:
1. Confirmed E005's finding (full operator inequality FALSE, even for pure gauge)
2. Proved a new analytical result: Δ = 14(cosε − 1) ≤ 0 for single-link excitations (rigorous)
3. Identified B_□ B_□^T = 4I₃ as a per-plaquette algebraic invariant
4. Computed E[M(Q)] = 2(d-1)I = 6I (Haar average)

The scope was wrong (targeting false statement), but the useful failure gave us structural insights. In Phase 3, goals must be rewritten to target λ_max ≤ 4d, not the full operator inequality.

### Phase 2 Strategic Assessment

Phase 2 has produced two critical clarifications:
1. The correct target is λ_max(M(Q)) ≤ 4d (NOT M(Q) ≼ M(I))
2. Three families are proved: pure gauge, single-link, uniform Q
3. The Haar average E[M(Q)] = 6I << 16 — the inequality has enormous slack on average
4. R(Q)|_P ≼ 0 is the Weitzenböck reformulation; Jiang (2022) exists but doesn't prove it

Still waiting for E006 results.

### Phase 3 Direction

For E008-E010, the focus should shift to:
- **E008**: Formal proof attempt of λ_max(M(Q)) ≤ 4d using the new algebraic invariants (B_□ B_□^T = 4I₃) and the SU(2) = SO(3) structure. Target: Schur-style bound or Jiang F specialization.
- **E009**: Adversarial review of novel claims from this entire strategy (12× improvement, β < 1/4 under the unproved conjecture).
- **E010**: Assembly of all proved results into a final theorem statement.

---

## Phase 2 Complete — E006 Reflection and Phase 3 Plan

### E006 Reflection

E006 was the math explorer for Phase 2 — the most computationally thorough. Key results:
1. Confirmed M(Q) ≼ M(I) FALSE — AND gave a structural reason: Tr(M(Q)) = Tr(M(I)) for all Q forces Tr(R(Q)) = 0, meaning R(Q) CANNOT be NSD. This is a clean mathematical fact, not just numerical.
2. Proved pure gauge isometry analytically (M(Q_pure) = Ad_G^T M(I) Ad_G) — now verifiable to 1e-14.
3. Confirmed P^T R(Q) P ≼ 0 for 42 configs, gradient ascent plateaus at -8 to -11 (never near 0).
4. New: Tr(M²) is NOT conserved — non-trivial Q "flattens" the spectrum.

Was scope right? Yes. The math explorer correctly prioritized computation over literature.

What would I change? The gradient ascent on P^T R P is crucial — I should have asked for more aggressive adversarial search here specifically (more starting points, longer runs).

### Phase 2 Complete — All Three Converge

All three Phase 2 explorations confirm:
1. **M(Q) ≼ M(I) is FALSE** (structural, not just numerical)
2. **P^T R(Q) P ≼ 0 is TRUE** (42+ configs, gradient ascent, huge margin)
3. **Tr(M(Q)) = Tr(M(I))** explains why full operator ordering fails
4. **Pure gauge isometry**: M(Q_pure) = Ad_G^T M(I) Ad_G (analytical proof + verified)
5. **New algebraic invariants**: B_□ B_□^T = 4I₃, E[M(Q)] = 6I

The central remaining gap: prove P^T R(Q) P ≼ 0 analytically.

### Phase 3 Revised Plan

**E008 (Math Explorer): Analytical proof of P^T R(Q) P ≼ 0**
- Target: for staggered modes v = f_{stag}(x,μ) ⊗ n (fixed color n), show v^T R(Q) v ≤ 0
- Tools: SU(2) = SO(3) in adjoint rep, B_□ B_□^T = 4I₃ invariant, per-plaquette decomposition
- Key computation: for each plaquette □, compute the contribution of Ad_P(n) terms to v^T R(Q) v
- Also try: Jiang F formula specialized to hypercubic lattice with SU(2)

**E009 (Standard Explorer): Adversarial review of novel claims**
- Review all claims from strategy-003 for novelty and rigor
- Check: is P^T R(Q) P ≼ 0 in any prior literature? Is Tr(M(Q)) = Tr(M(I)) known?
- Construct strongest possible counterargument to β < 1/4 improvement
- Verify: what is rigorously proved vs conjectured?

**E010 (Standard Explorer): Final synthesis + theorem assembly**
- Compile all proved results into a clean theorem statement
- Identify exactly what conjecture is needed for β < 1/4 vs β < 1/6
- Write the key theorem: "If P^T R(Q) P ≼ 0 for all Q [CONJECTURED], then H_norm ≤ 1/12 → mass gap β < 1/4 for SU(2), d=4"
