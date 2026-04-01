# Strategy-002: BKM Enstrophy Bypass — Prove a Tighter Blow-up Criterion

## Objective

Construct a tighter enstrophy-based regularity criterion for 3D Navier-Stokes by replacing the Ladyzhenskaya interpolation chain (237× slack) with the BKM/Kozono-Taniuchi approach (3× slack). The goal is a **stated theorem with a proof** — not further characterization of the slack. A secondary target is rigorous derivation of the conditional bound C(F₄) ≈ 0.003/F₄ relating effective Ladyzhenskaya constant to vorticity intermittency.

This is a constructive attack strategy. Every exploration should produce either a proved statement or a precisely identified obstruction.

## Methodology

Three-phase protocol: **Validate Premise → Construct Proof → Adversarial Verification**. All explorations mandatory.

### Phase 0: Validate the Premise (1-2 explorations)

**Goal:** Before attempting proofs, computationally verify that a BKM-based enstrophy closure actually produces a tighter inequality for the tested flows.

**Mandatory computation:** Starting from the enstrophy equation

  (1/2) d/dt ||ω||²_{L²} = ∫ ω_i S_{ij} ω_j dx - ν||∇ω||²_{L²}

write the vortex stretching term two ways:
1. **Ladyzhenskaya chain:** |∫ ω_i S_{ij} ω_j| ≤ C_L ||ω||^{3/2}_{L²} ||∇ω||^{3/2}_{L²} (the standard approach, 237× slack)
2. **BKM-based:** |∫ ω_i S_{ij} ω_j| ≤ ||ω||²_{L²} ||S||_{L^∞} ≤ ||ω||²_{L²} · C_{BKM} ||ω||_{L^∞} (1 + log(||∇ω||_{L²}/||ω||_{L²}))

For each Re=100,500,1000,5000 on Taylor-Green AND at least 2 other ICs (random Gaussian + adversarial tubes from Strategy-001):
- Compute both bounds at every timestep
- Compute the resulting enstrophy ODE right-hand side for each approach
- Determine: does the BKM-based ODE avoid blow-up for the tested flows? What is the effective blow-up time for each approach?
- **Critical check:** The BKM approach trades the Ladyzhenskaya constant for ||ω||_{L^∞}. Is ||ω||_{L^∞} controllable for these flows? Compute ||ω||_{L^∞}/||ω||_{L²} vs time — if this ratio grows fast enough, BKM might not be better.

**Success criterion:** BKM-based ODE gives at least 10× later effective blow-up time than Ladyzhenskaya-based ODE for all tested flows. If not, this direction is dead and Phase 1 should pivot to the conditional C(F₄) bound instead.

**Failure criterion:** If ||ω||_{L^∞}/||ω||_{L²} grows so fast that BKM-based enstrophy ODE is actually WORSE, stop this direction immediately and pivot.

### Phase 1: Construct the Proof (4-5 explorations)

The Strategizer chooses the specific proof targets based on Phase 0 results. The methodology is: **ONE theorem target per exploration. State the theorem first. Attempt the proof. If the proof breaks, identify exactly WHERE and WHY.**

**Direction A — BKM Enstrophy Criterion (if Phase 0 validates):**

Target theorem (to be refined by Phase 0 data): "If u is a Leray-Hopf weak solution of 3D NS on T³ and ∫₀ᵀ ||ω(t)||_{L^∞} · (1 + log(||∇ω||/||ω||))^α dt < ∞ for some α ≥ 1, then u is regular on [0,T]."

This should be compared against Prodi-Serrin and BKM. The key question: does the BKM-based enstrophy closure give a criterion that is STRICTLY weaker (harder to violate) than standard Prodi-Serrin?

Proof approach: Start from the enstrophy ODE, bound VS using BKM instead of Ladyzhenskaya, use Young's inequality to absorb the viscous term, get a Gronwall-type inequality. The log correction may give double-exponential growth instead of finite-time blow-up.

**Direction B — Conditional Ladyzhenskaya with Flatness (parallel or fallback):**

Target theorem: "For divergence-free vector fields on T³ with vorticity flatness F₄ = ||ω||⁴_{L⁴}/(||ω||²_{L²})², the effective Ladyzhenskaya constant satisfies C_{L,eff} ≤ C_L · F₄^{-β} for some β > 0."

Proof approach: Use the relation between L⁴ norm, L² norm, and flatness. The Ladyzhenskaya optimizer has F₄ = 1 (maximally concentrated). For fields with bounded flatness F₄ ≤ M, the optimizer is excluded, giving a tighter constant. The key step is making this rigorous via interpolation theory.

This direction is valuable independently because it explains the 63% Ladyzhenskaya slack component.

**Direction C — Multi-IC validation of the Strategy-001 slack atlas (1 exploration):**

Compute the full slack atlas (all 8 inequalities) for:
1. Random-phase Gaussian spectrum at Re=500, 1000, 5000
2. Kida vortex at Re=500, 1000
3. The adversarial anti-parallel tubes (σ=2.5) at Re=500, 1000

Also compute the decomposition (α_geom × α_Lad × α_sym) and BMO/L^∞ ratio for these ICs. Report which findings are IC-robust and which are TGV-specific.

### Phase 2: Adversarial Verification (2-3 explorations, all mandatory)

**Exploration A — Math explorer adversarial recomputation:**
- Independently reimplement the NS solver from scratch (different code, same physics)
- Recompute the 3 most important numerical claims from Strategy-001 and this strategy
- Report any discrepancies >5%

**Exploration B — Standard explorer adversarial review:**
- For every claimed theorem: check the proof step by step. Identify the weakest step.
- Novelty search: exact search terms for each claimed result on arXiv, MathSciNet, Google Scholar
- The (5/9)^{1/4} error from Strategy-001 shows we need this — check ALL analytical claims for misattribution
- Strongest counterargument for each claim

**Exploration C (if budget allows) — Protas-type adversarial IC search:**
- Use adjoint-based PDE optimization to find the IC that minimizes vortex stretching slack
- Compare against our 158× minimum from Strategy-001
- This addresses the strongest counterargument to Claim 1 (our adversarial search was local, not global)

## Validation Criteria

**Strategy succeeds if:**
- A proved theorem gives a strictly tighter enstrophy-based regularity criterion than the standard Ladyzhenskaya chain (Tier 4: Significance)
- OR a proved conditional bound C_{L,eff} ≤ f(F₄) formalizes the intermittency advantage (Tier 4)
- AND the slack atlas is validated on ≥3 ICs, establishing generality (strengthens Tier 3)
- AND the best result survives both math and standard adversarial review (Tier 5)

**Strategy is exhausted if:**
- Phase 0 shows the BKM-based ODE is no better (||ω||_{L^∞} growth kills the advantage)
- AND the conditional C(F₄) bound turns out to be algebraically trivial (just restating L⁴ norm control)
- AND multi-IC testing shows the Strategy-001 findings were TGV artifacts

## Context: What Strategy-001 Established

**Established facts (carry forward):**
- Vortex stretching has 237× slack on TGV (158× adversarial minimum), loosest by 8× vs next inequality
- Slack decomposes: 63% Ladyzhenskaya (α_Lad = 31×) + 31% geometric alignment (α_geom = 5.3×) + 6% symmetric (α_sym = √2)
- Effective Ladyzhenskaya constant C_{L,eff} = 0.147, only 18% of sharp C_L = 0.827
- BKM/CZ gives ~3× slack with theoretical constant vs 237× for Ladyzhenskaya chain
- BMO/L^∞ ≈ 0.27 across Re=100-5000
- Spectral Ladyzhenskaya is dead: phase alignment achieves near-sharp constant regardless of spectral support
- Conditional empirical fit: C(F₄) ≈ 0.003/F₄ with r = -0.93 correlation
- Code artifacts in strategy-001/explorations/exploration-002/code/

**Established dead ends (do not revisit):**
- Spectral/harmonic analysis improvement of Ladyzhenskaya constant (Tao obstruction + exploration 006)
- The (5/9)^{1/4} "div-free factor" — this is a vector vs scalar effect, NOT incompressibility

**Known weaknesses to address:**
- All key findings are TGV-specific (except vortex stretching slack from exploration 003)
- Adversarial review was standard-only — no independent recomputation
- BKM comparison is "apples-to-oranges" (different quantities) — needs reformulation
- 158× adversarial minimum used local search only (gradient descent on tube parameters)
- Conditional bound C(F₄) is purely empirical, single IC

**Existing code to reuse:**
- NS solver: strategy-001/explorations/exploration-002/code/ns_solver.py
- Slack measurements: strategy-001/explorations/exploration-002/code/slack_measurements.py
- These are validated at N=128 with <0.7% convergence and <0.15% energy conservation error
