# Exploration 004 — Phase 2: Root Cause Diagnosis and Minimal Modification Survey

## Mission Context

You are exploring Stochastic Electrodynamics (SED) — classical electrodynamics augmented by a real, Lorentz-invariant zero-point field (ZPF). This is a synthesis/literature exploration, not a simulation.

## What Has Been Done (Results to Synthesize)

**Strategy-001 (6 explorations):**
- SED harmonic oscillator: var_x = 0.507 ± 0.05 vs QM 0.500 (1.4%) ✓
- SED anharmonic oscillator (ALD): ~15-18% residual at β=1.0, scales as τ^0.23 × ω_max^(-0.18)
- Key formula: ALD equation ẍ = -V'(x)/m - τV''(x)ẋ + F_zpf + τḞ_zpf

**Strategy-002 Phase 1 (3 explorations just completed):**

**E001 — SED Double-Well Barrier Crossing:**
- First numerical simulation of SED tunneling in V(x) = -½ω₀²x² + ¼λx⁴
- KEY RESULT: Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) [NEW FORMULA, verified at 2 λ values]
- At λ=0.25 (S_WKB=1.41≈V_barrier/E_zpf=1.41): Γ_SED/Γ_QM = 1.15 (15% agreement)
- At λ=0.10 (S_WKB=6.29, V_barrier/E_zpf=3.52): Γ_SED/Γ_QM = 18.5 (18× overestimate)
- SED crossings are ZPF-driven over-barrier events, NOT quantum tunneling
- ALD is well-behaved even with anti-damping at barrier top (V'' < 0)
- Prior art: Faria & Franca (2005) — analytical only, no WKB comparison

**E002 — Two Coupled SED Oscillators:**
- In 1D: C_xx(d) = cos(ω₀d/c) [VERIFIED analytically and numerically]
- Bell-CHSH S ≤ 2 always — SED never violates Bell bound
- First direct Bell-CHSH computation from SED
- Key gap: 3D multi-mode ZPF would average C_xx over all k-directions (unknown result)
- Boyer (2018) explicitly states SED is globally non-local (global ZPF phases)

**E003 — SED Hydrogen Circular Orbits:**
- T_ion measurements: at L=1.0, 10% ionize in 200 periods, ⟨r⟩=1.47a₀≈QM (1.50)
- At L=0.5, 95% ionize, median T_ion=17 periods
- NO stability window for any L value
- Reconciles Cole & Zou (2003) short-run optimism with Nieuwenhuizen (2015) pessimism

## The Root Cause Hypothesis

The Strategizer (me) proposes the following unifying root cause:

**The ω³ positive feedback mechanism:**
SED fails whenever the system's LOCAL oscillation frequency ω_local(x) deviates significantly from the equilibrium frequency ω₀. The ω³ ZPF spectral density delivers power proportional to ω_local³, while the ALD damping calibrated to ω₀ cannot fully compensate. This creates energy imbalance:

- **Anharmonic oscillator:** Anharmonic term shifts ω_local upward → ZPF delivers more power → ALD partially compensates (15-18% residual)
- **Double-well:** At barrier top, V'' < 0 → ω_local → imaginary → ALD becomes anti-damper → ZPF kicks particle over barrier faster than QM tunneling
- **Hydrogen:** Near nucleus, ω_local → ∞ → ω³ ZPF → ∞ → runaway

This mechanism DOESN'T apply to:
- **Harmonic oscillator:** ω_local = ω₀ everywhere → exact balance
- **Coupled linear oscillators:** Linear, so ω_local = ω₀ for each oscillator → exact balance (van der Waals)
- **Casimir, blackbody, van der Waals:** All linear systems

## Your Specific Goals

### 1. Literature Survey: SED Modifications (Priority 1)

Search the literature for proposed modifications to SED that address nonlinear failures. Specifically look for:

**Authors to search:**
- Boyer, T.H. (all papers 1975-2024 on SED nonlinear systems)
- de la Peña, L. & Cetto, A.M. (books: "The Quantum Dice" 1996, "The Emerging Quantum" 2015; papers on LSED)
- Pesquera & Claverie (1982) — their O(β²) result and any follow-up
- Santos, E. (all papers on SED modifications and stochastic optics)
- Nieuwenhuizen (2020) renormalization schemes
- Claverie & Diner (1977)
- Marshall, T.W. (stochastic optics)

**Questions to answer:**
- Has anyone proposed replacing the ω³ spectral density with a system-dependent spectrum?
- Has anyone proposed "position-dependent noise" (noise power proportional to V''(x)) as a fix?
- Has anyone proposed the Local FDT (Fluctuation-Dissipation Theorem) approach — using the local oscillation frequency for both damping AND noise?
- What does de la Peña's LSED impose that standard SED doesn't? Is it a "position-dependent noise"?

### 2. Assess the Root Cause Hypothesis

Does the "ω³ feedback mechanism" unify the failures in E001, E002 (partially), E003, and Strategy-001?

Specifically, evaluate:
(a) Is the crossover condition S_WKB = V_barrier/E_zpf physically equivalent to ω_local = ω₀? (The crossover occurs when the barrier height equals the ZPF energy, which happens when the local potential curvature matches the equilibrium curvature.) If so, this would strengthen the unified story.

(b) For hydrogen: is the failure mechanism "ω_local → ∞ near nucleus" or something more specific to the Coulomb 1/r potential? (Nieuwenhuizen's 2015 finding: failure occurs when orbital angular momentum falls below 0.588ħ, which corresponds to the orbit becoming sufficiently eccentric that near-nucleus passes dominate.)

(c) For coupled oscillators: Why does C_xx(d) = cos(ω₀d/c) in 1D? Is this a consequence of the single-mode 1D ZPF being phase-coherent across both oscillators, while 3D averaging destroys the coherence? Is this a "failure" of SED or just a 1D artifact?

### 3. Minimal Modification — What Would Fix SED?

Evaluate three proposed fixes:

**Fix A: Local FDT (position-dependent noise)**
Replace S_F(ω) = 2τω³/m with S_F(ω, x) = 2τ|V''(x)|^(3/2)/m × δ(ω - ω_local(x)).
This would make noise power match the LOCAL oscillation frequency at each position.
- Would this fix the anharmonic oscillator? (The ALD already does position-dependent damping; this would also do position-dependent noise.)
- Would this fix hydrogen? (Near nucleus, V'' from Coulomb: V''(r) = -2/r³, ω_local² = |V''| = 2/r³ → noise still diverges near nucleus)
- Would this preserve harmonic oscillator success? (At x where V'' = ω₀², would recover standard noise)
- Is this known in the literature?

**Fix B: Spectral index modification**
Replace ω³ with ω^n for n < 3 (Strategy-001 suggested this might matter).
- Strategy-001 found that reducing n below 3 reduces the ALD residual (n=2 undershoots, n=3 overshoots, crossover at n*≈2.61).
- Would n=n* < 3 fix ALL SED failures simultaneously?
- What's the physical meaning of n < 3 for the ZPF spectral density?

**Fix C: Effective mass / dressed particle**
Some proposals (e.g., extended electron model of Cavalleri et al.) use a dressed particle with modified mass. Does any version of this fix the nonlinear failures?

### 4. Novel Claim Identification

Based on your survey, identify which of these claims from Strategy-002 are genuinely new:

**Claim A (from E001):** The formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) — is this in Faria & Franca (2005) or elsewhere?

**Claim B (from E002):** C_xx(d) = cos(ω₀d/c) for two SED oscillators sharing a 1D ZPF — is this the van der Waals result from Boyer (1973) in disguise, or genuinely different?

**Claim C (from E003):** The first quantitative T_ion(L) measurements for SED hydrogen — is there any prior paper with explicit T_ion data?

**Claim D (root cause):** "The ω³ feedback mechanism unifies all SED failures" — is this stated anywhere explicitly in the SED literature?

## Success Criteria

**Good success:**
- Identify whether any of the three minimal modifications have been proposed before
- Confirm or refute the root cause hypothesis based on literature
- Identify which novel claims survive scrutiny

**Excellent success:**
- Find that the "Local FDT" modification is genuinely new AND assess whether it would fix the failures
- Establish that the crossover condition S_WKB = V_barrier/E_zpf is equivalent to a known energy balance condition

**Acceptable negative result:**
- "All three minimal modifications are already in the literature" — then catalog what was tried and why it failed

## Your Exploration Directory

`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-004/`

Write REPORT.md as you go (write each section when you complete it). Write REPORT-SUMMARY.md (max 400 words) when done.

## Output Format

REPORT.md should contain:
1. Literature survey results: what SED modifications have been proposed
2. Assessment of root cause hypothesis: does ω³ feedback unify the failures?
3. Evaluation of three fixes (Local FDT, spectral index, dressed particle)
4. Novel claim assessment: which E001-E003 claims are genuinely new
5. Overall recommendation for Phase 3 (adversarial synthesis) and remaining explorations
