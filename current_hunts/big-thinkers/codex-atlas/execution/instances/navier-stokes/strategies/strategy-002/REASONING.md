# Reasoning Log

## Exploration 001: BKM Enstrophy Bypass Validation

### What I considered

Three options for the first exploration:

1. **Phase 0 — BKM enstrophy bypass validation** (the strategy's prescribed first step). Computationally verify that replacing the Ladyzhenskaya chain with BKM/CZ in the enstrophy ODE gives a tighter effective inequality. The key risk: if ||omega||_{L^infty}/||omega||_{L^2} grows too fast, the BKM approach could actually be WORSE.

2. **Direction C — Multi-IC validation of the Strategy-001 slack atlas**. Independent of Phase 0 and useful context for later proofs. Could run in parallel.

3. **Jump to Direction B — Conditional C(F_4) bound derivation**. The strongest empirical finding from Strategy-001. But this is analytical/proof work that benefits from having the Phase 0 data first.

### What I chose and why

**Phase 0 — BKM enstrophy bypass validation.** This is the gate for the entire strategy. If the BKM-based enstrophy ODE doesn't improve things, Direction A dies and we pivot entirely to Direction B (conditional flatness bound). Doing this first maximizes the strategic value per exploration — it tells us which of the two main proof targets to pursue.

I'm designing this as a single comprehensive math exploration that covers:
- Both bound computations (Ladyzhenskaya vs BKM) at every timestep
- Three ICs (TGV, random Gaussian, adversarial tubes) at Re=100, 500, 1000, 5000
- The critical ||omega||_{L^infty}/||omega||_{L^2} ratio check
- Effective blow-up time comparison for both ODE closures
- Young's inequality absorption analysis (can the BKM bound absorb the viscous term better?)

This is a math explorer task — it's all computation.

### What I rejected and why

- Multi-IC validation (Direction C): Useful but not gating. Can run as a parallel exploration later.
- C(F_4) proof attempt: Premature — Phase 0 results may reshape how we approach it.
- Protas-type adversarial search (Computation #8 from COMPUTATIONS-FOR-LATER): Too expensive for the first exploration and doesn't inform the core question.

### Library query (abbreviated)

Queried the NS factual library.
- bkm-near-tightness-226x-advantage.md: BKM min slack 1.05x with empirical C, ~3x with theoretical. WEAKENED by adversarial review — comparison is apples-to-oranges (different quantities). This is exactly what Phase 0 needs to resolve: do the tighter bounds on ||nabla u||_{L^infty} actually translate to tighter enstrophy control?
- vortex-stretching-structural-slack.md: 158x lower bound, 63% Ladyzhenskaya dominance
- conditional-vortex-stretching-bound.md: C(F_4) ~ 0.003/F_4, purely empirical

The library confirms the "apples-to-oranges" concern is the #1 risk for this exploration. I'm designing the goal to address this directly — compute both bounds on the SAME quantity (the vortex stretching integral) and compare.

### Reflection (post-exploration)

**Did the explorer answer what I asked?** Yes, comprehensively. All 6 computational steps were executed. 13 DNS runs completed with full diagnostics. The verdict is unambiguous — BKM enstrophy bypass is massively validated.

**Was the scope right?** Perfect. The 3 ICs × 4 Re design with convergence check was exactly right for a gating decision. The explorer also added valuable analysis beyond what I asked (empirical CZ constants, Young's inequality optimization).

**Key surprise:** The magnitude of the advantage (10⁷ to 10¹⁶) was far beyond what I expected. I thought we'd see 10-100× improvement, not billions. The reason: the ν⁻³ factor in the Ladyzhenskaya ODE coefficient is devastating, and BKM avoids it entirely by putting ||∇ω|| inside a logarithm.

**What I learned:** The BKM advantage is NOT about tighter constants (though C_CZ < C_L). It's structural — the power of ||∇ω|| in the vortex stretching bound. BKM uses power 0 (inside log), Ladyzhenskaya uses power 3/2. When you trade against dissipation (power 2), the Ladyzhenskaya approach introduces ν⁻³ while BKM does not. This is a clean, provable structural advantage.

**Next steps:** Phase 0 is complete and validated. Move to Phase 1 — construct the proof. Direction A (BKM enstrophy criterion) is now the primary target. The data shows exactly what the theorem should look like.

---

## Exploration 002: BKM Enstrophy Criterion — Proof Attempt

### What I considered

With Phase 0 massively validated, Phase 1 has two parallel directions:
- **Direction A**: BKM enstrophy criterion (the primary target from STRATEGY.md)
- **Direction B**: Conditional Ladyzhenskaya with flatness C(F₄)

I'll start with Direction A since the validation data is overwhelming. The question: can we prove that the BKM-based enstrophy closure gives a strictly weaker blow-up criterion than the Ladyzhenskaya chain?

The data shows the key structural insight: BKM replaces ||∇ω||^{3/2} with log(||∇ω||), which means the dissipation term ν||∇ω||² always dominates the stretching term's dependence on ||∇ω||. This eliminates the need for the Young's inequality step that introduces ν⁻³.

### Explorer type decision

This is fundamentally an analytical proof task, but it benefits from computational verification of individual proof steps. The math explorer will:
1. Write the proof step by step with each step verified computationally
2. Check the resulting ODE on our DNS data
3. Compare the new criterion against Prodi-Serrin

I'm choosing the **math explorer** because the proof involves specific calculations (Young's inequality parameters, ODE comparison) that benefit from computational checks at each step.

### Reflection (post-exploration-002)

**Did the explorer answer what I asked?** Yes — proved the theorem in 4 steps with clear identification of the one proof gap (BGW on T³). Comparison with Prodi-Serrin was addressed. Computational verification thorough.

**Was the scope right?** Slightly too ambitious. The explorer spent 30+ minutes before producing output. The proof itself is clean; the Prodi-Serrin comparison is conjectural. The novel content is the explicit quantitative comparison T_BKM/T_Lad ~ Re³.

**Key insight:** The result is "modest but genuine" — which is exactly what the strategy predicted.

**Next:** Proceed with Direction B (conditional C(F₄) bound) and then adversarial review.

## Exploration 003: C(F4) + Multi-IC Validation

### What I chose and why
Combined Direction B (C(F4) bound) and Direction C (multi-IC validation) into one exploration since they share DNS infrastructure.

### Reflection (post-exploration-003)
**C(F4) is a dead end** — exact identity C_Leff^4 = F4 * R^3 kills it. The Strategy-001 correlation was a confounding variable artifact. Major lesson: always look for algebraic identities behind empirical correlations.

**Multi-IC validation is the MVP of this exploration.** The IC-robustness classification clearly shows that F5/F1/F3 are universally tight while E2E3/E4 are IC-specific. This validates the BKM approach further and points to CZ pressure as potentially the "true" regularity bottleneck.

**Next:** Phase 2 adversarial review. With 3 explorations done, I have enough material for a comprehensive adversarial review of the strategy's claims.

---

### What I chose

**Exploration 002**: Prove that the BKM-based enstrophy closure gives a regularity criterion. Specifically, prove:

"If u is a Leray-Hopf weak solution of 3D NS on T³ and ∫₀ᵀ ||ω(t)||_{L^∞} dt < ∞, then the enstrophy stays bounded on [0,T]."

This is actually known (it's essentially the BKM criterion restated at the enstrophy level). The novel contribution would be:
1. **Quantifying the advantage**: Showing the effective ODE from BKM closure has no ν⁻³ factor
2. **Comparing to Prodi-Serrin**: Is the BKM enstrophy criterion strictly weaker?
3. **The conditional result**: Under what conditions on ||ω||_{L^∞}/||ω||_{L²} does BKM give finite-time regularity?

---

