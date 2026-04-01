# Strategy-002 Final Report — Stochastic Electrodynamics: New Systems and Root Cause

**Date:** 2026-03-27
**Explorations completed:** 6 of 10 (E001–E006)
**Status:** Complete

---

## What Was Accomplished

Strategy-002 extended SED analysis to three new systems (double-well tunneling, coupled oscillators, hydrogen), identified the root cause of all SED failures, verified a new quantitative formula, and conducted adversarial review of all novel claims.

### Explorations Summary

| ID | Type | Topic | Outcome |
|----|------|--------|---------|
| E001 | Math | SED double-well barrier crossing vs WKB | Formula discovered, 15% at crossover, 18× at deep barriers |
| E002 | Math | Two coupled SED oscillators: ZPF correlations + Bell-CHSH | C_xx=cos(ω₀d/c), Bell S ≤ 2 always |
| E003 | Math | SED hydrogen: T_ion(L) measurements | First quantitative ionization timescales |
| E004 | Standard | Phase 2: Root cause synthesis + literature survey | ω³ unification confirmed novel |
| E005 | Math | Γ formula verification at 7 λ values | R²=0.9998 across 4 decades, formula confirmed |
| E006 | Standard | Adversarial review of all four claims | Faria-França (2004) prior art found, novelty status clarified |

---

## Most Promising Findings

### Finding 1: SED Barrier-Crossing Formula (PARTIALLY NOVEL — after adversarial review)

**The result:** For the double-well V(x) = −½ω₀²x² + ¼λx⁴ with ω₀ = m = ħ = 1:

```
ln(Γ_SED/Γ_exact) = 0.072 + 1.049 × (S_WKB − V_barrier/E_zpf)
```

where:
- Γ_SED = SED barrier-crossing rate (ALD equation with ZPF noise)
- Γ_exact = exact QM tunneling rate (Schrödinger equation)
- S_WKB = WKB action integral for the quantum problem
- V_barrier/E_zpf = (1/(4λ)) / (√2/2) = √2/(4λ) [UNIVERSAL for this potential family]
- E_zpf = ħω_local/2 = √2/2 (universal: ω_local at potential minimum is always √2 regardless of λ)
- A = exp(0.072) ≈ 1.075, slope = 1.049 ± 0.007, R² = 0.99977

**Fit quality:** Verified across 7 data points, 4 decades in ratio (Γ_SED/Γ_exact from 0.84 to 6263), λ ∈ [0.05, 0.30].

**Physical interpretation:** SED uses classical Boltzmann barrier crossing exp(−V_barrier/E_zpf), while QM uses WKB tunneling exp(−S_WKB). Their ratio is controlled by (S_WKB − V_barrier/E_zpf). They agree when S_WKB ≈ V_barrier/E_zpf (at λ=0.25, both ≈ 1.41).

**Prior art situation (from E006):**
- Faria, França & Sponchiado (2004), Found. Phys. 35 (2005), Eq. 40: derived Γ_SED ∝ exp(−ΔU/[ħωa/2]) analytically via Kramers-Chandrasekhar theory. This IS the exponential structure.
- What is NEW: (a) the ratio Γ_SED/Γ_exact formulation, (b) the connection to S_WKB (crossover condition), (c) R²=0.9998 numerical verification across 4 decades, (d) ω_local=√2 universality for the double-well family, (e) identification of the systematic slope=1.049 ≠ 1.0 deviation.
- **Status: PARTIALLY VERIFIED (computational). Marginally novel vs. Faria-França (2004).**

**Open questions:** Slope=1.049 is 7σ from 1.0 — physical origin unknown. A ≈ 1.075 is UV-sensitive (changes ~50% with ω_max).

---

### Finding 2: ω_local = √2 Universality (NOVEL — analytic result)

For V(x) = −½ω₀²x² + ¼λx⁴ with ω₀ = 1 and any λ:
- Potential minimum at x_min = 1/√λ
- V''(x_min) = −1 + 3λ × (1/λ) = 2
- ω_local = √(V''(x_min)) = **√2 regardless of λ**

Therefore E_zpf = √2/2 is a universal constant for this potential family, and V_barrier/E_zpf = √2/(4λ) is determined analytically.

**This explains why λ=0.25 is the crossover:** S_WKB(0.25) ≈ 1.41 ≈ V_barrier/E_zpf(0.25) = 1.414.

**Status: VERIFIED (analytic). This is a clean mathematical fact.**

---

### Finding 3: ω³ Positive Feedback as Unified Root Cause (PARTIALLY NOVEL — synthesis)

All SED failures share one mechanism:

> *When the system's local oscillation frequency ω_local(x) deviates from the equilibrium frequency ω₀, the ω³ ZPF spectral density delivers power proportional to ω_local³, while ALD damping calibrated to ω₀ cannot compensate. This creates net energy injection.*

Evidence:
- **Anharmonic oscillator (Strategy-001):** ω_local shifts up with anharmonicity → ALD leaves 15-18% residual at β=1.0
- **Double-well (E001/E005):** V''(x) < 0 at barrier top → ALD becomes anti-damper → classical barrier crossings at rate exp(−V_b/E_zpf) exceed WKB rate
- **Hydrogen (E003):** Near nucleus, ω_local → ∞ → ω³ ZPF → ∞ → runaway; T_ion monotonically decreasing with L, rapid ionization below L_crit ≈ 0.588ħ
- **Linear systems (E002):** ω_local = ω₀ everywhere → exact balance → SED succeeds for van der Waals, harmonic oscillator, Casimir

**Prior art (from E004/E006):**
- Boyer (1976) showed nonlinear oscillators push ZPF toward non-equilibrium
- Pesquera-Claverie (1982) showed radiation balance fails at O(β) for anharmonic oscillator
- Ibison-Haisch (1996) showed ω³ factor in ZPF variance explicitly

**What is new:** Explicit unification of three failure modes (anharmonic oscillator, double-well, hydrogen) under one named mechanism, with quantitative support from new simulations.
**Status: PARTIALLY VERIFIED. The synthesis is new; the individual components are in the literature.**

---

### Finding 4: SED Hydrogen Ionization Timescales (PARTIALLY NOVEL — first quantitative T_ion(L) data)

First measurements of T_ion as function of initial angular momentum:

| L/ħ | Ionized in 200 periods | Median T_ion | ⟨r⟩/a₀ |
|------|------------------------|--------------|---------|
| 1.0 | 10% (2/20) | ~57 periods | **1.47 ≈ QM 1.50** |
| 0.9 | 35% (7/20) | ~108 periods | 1.24 |
| 0.7 | 75% (15/20) | ~83 periods | 1.05 |
| 0.5 | 95% (19/20) | ~17 periods | 1.15 |

Key finding: No stability window. L=1.0 (circular orbit) appears stable short-term (⟨r⟩≈QM, 90% survive 200 periods) but extrapolates to 100% ionization within ~9,000 periods. This reconciles Cole & Zou (2003) short-run optimism with Nieuwenhuizen (2015) long-run pessimism.

**Caveat:** τ used was 60× physical value. T_ion values are 60× too short. With physical τ, T_ion(L=1.0) ≈ 3,400 periods → consistent with Nieuwenhuizen's observation that ionization takes "tens of thousands of orbits."

**Status: PARTIALLY VERIFIED (computational, with τ caveat). Quantitative T_ion(L) data is new; no prior paper has this table with explicit numbers.**

---

### Finding 5: ZPF Correlations and Bell S (REFRAMED after adversarial review)

The true finding from E002 is NOT "Bell S ≤ 2" (trivially true for SED) but:

**SED produces C_xx(d) = cos(ω₀d/c) — oscillating correlations that are absent in QM for uncoupled oscillators.**

For two harmonic oscillators at separation d sharing the same 1D ZPF realization (with phase delay d/c):
- SED: C_xx(d) = cos(ω₀d/c) → oscillates, can anti-correlate (C_xx = -0.83 at d=10)
- QM (vacuum, uncoupled): C_xx = 0 everywhere

This SED-QM discrepancy is a non-trivial prediction. In 1D, it's a one-line derivation from Boyer (1975) correlators. Whether it survives the 3D multi-mode ZPF average (which might give C_xx → 0 or → van der Waals r⁻⁶) is UNKNOWN.

**Status: CONJECTURED for 3D case. The 1D formula is known (Boyer); the QM discrepancy in 3D is an open question.**

---

## What I'd Recommend the Next Strategy Focus On

### Priority 1 (HIGH): Sharpen Claim A against Faria-França (2004)

The E006 finding that Faria-França (2004) has the core exponential structure requires a specific comparison. A clean paper would need to show explicitly:
- What Faria-França derive vs. what we compute
- Why the ratio Γ_SED/Γ_exact ∝ exp(S_WKB − V_b/E_zpf) is a non-trivial extension
- Whether the slope = 1.049 deviation indicates a physical correction beyond the Kramers-Chandrasekhar approximation

**Exploration type:** Standard Explorer — read Faria-França (2004) in detail, identify where their Eq. 40 differs from our formulation, and propose a precise statement of novelty.

### Priority 2 (HIGH): Fix Claim C with Physical τ

The τ correction (×60) would make E003 publishable. T_ion(L) with physical τ is needed.

**Exploration type:** Math Explorer — re-run E003 with τ = 2.6×10⁻⁷ atomic units, extend L=1.0 to 5,000 periods, scan L more finely near L_crit.

### Priority 3 (MEDIUM): 3D ZPF Correlations

Whether C_xx → 0 or → r⁻⁶ in 3D is the key question for E002's finding.

**Exploration type:** Math Explorer — compute ⟨x₁x₂⟩ in 3D using Boyer's two-point correlator formula, check if orientational average gives zero or van der Waals term.

### Priority 4 (MEDIUM): Santos ħ-Order Analysis

Santos (2022) showed SED = first-order-in-ħ QED approximation. The 15-18% anharmonic residual and slope=1.049 tunneling deviation might both be computable from the missing ħ-order corrections.

**Exploration type:** Standard Explorer — read Santos (2022), compute the O(ħ²) correction to the anharmonic oscillator partition function, check if it predicts A ≈ 1.075 and slope=1.049.

---

## Novel Claims (Final Status After Adversarial Review)

### Claim 1: SED Barrier-Crossing Rate Formula

**Claim:** For V(x) = −½ω₀²x² + ¼λx⁴, the ratio of SED barrier-crossing rate to exact QM tunneling rate satisfies:
`ln(Γ_SED/Γ_exact) = 0.072 + 1.049(S_WKB − √2/(4λ))`
with slope = 1.049 ± 0.007, R² = 0.99977, verified at 7 λ values over 4 decades.

**Evidence:** E001 + E005 simulations [COMPUTED]. E006 adversarial review. Slope=1.049 from scipy linear regression on 7 data points.

**Novelty search:** Faria-França-Sponchiado (2004) Found. Phys. 35 derives Γ_SED ∝ exp(−ΔU/[ħωa/2]) analytically. Their exponential structure = ours. New contributions: ratio-to-QM formulation, S_WKB crossover condition, R²=0.9998 numerical verification across 4 decades, ω_local=√2 universality.

**Strongest counterargument:** The formula is essentially Kramers / Faria-França (2004) repackaged. The "novel" ratio formulation is a trivial algebraic step from dividing two known results.

**Status: PARTIALLY VERIFIED. Genuinely extends Faria-França (2004) with numerical precision but not conceptually distinct from their result.**

---

### Claim 2: ω_local = √2 Universality for V = −½x² + ¼λx⁴

**Claim:** For all λ, the oscillation frequency at the potential minimum of V(x) = −½x² + ¼λx⁴ is exactly ω_local = √2, making E_zpf = √2/2 a universal constant for this potential family.

**Evidence:** Analytic: V''(x_min) = −1 + 3λ(1/λ) = 2 → ω_local = √2. [VERIFIED analytic]

**Novelty search:** Not found in any paper searched. This is a simple but useful observation.

**Strongest counterargument:** This is a trivial algebraic calculation that any reader can do in 3 lines. Not a publishable result on its own — only useful as context for the tunneling formula.

**Status: VERIFIED. Trivially correct. Modestly novel as an observation that makes V_barrier/E_zpf = √2/(4λ) exact.**

---

### Claim 3: ω³ Feedback Mechanism as Root Cause of ALL SED Failures

**Claim:** All SED failures (anharmonic oscillator, double-well, hydrogen) arise from a single mechanism: when ω_local(x) ≠ ω₀, the ω³ ZPF spectral density creates net energy injection that ALD damping cannot balance.

**Evidence:** Strategy-001 anharmonic oscillator [COMPUTED]; E001/E005 double-well [COMPUTED]; E003 hydrogen [COMPUTED]; E004 literature survey [CONJECTURED with literature support from Boyer 1976, Pesquera-Claverie 1982, Santos 2022, Ibison-Haisch 1996].

**Novelty search (E006):** Boyer (1976) showed non-equilibrium in nonlinear SED; Pesquera-Claverie (1982) showed O(β) failure; Santos (2022) showed SED = O(ħ) QED. None unify all three failures under one named mechanism. No paper contains the phrase "ω³ positive feedback" or "ω_local-ω₀ mismatch" as the explicit explanation.

**Strongest counterargument:** Boyer, Pesquera-Claverie, and Santos already identified the mechanism in different guises. Our "unification" is a narrative repackaging of known results, not a new insight. A referee could say: "This is already in the literature if you read Boyer and Pesquera-Claverie together."

**Status: PARTIALLY VERIFIED. The synthesis is new and useful, but the underlying mechanism isn't.**

---

### Claim 4: First Quantitative T_ion(L) Table for SED Hydrogen

**Claim:** The monotonically decreasing T_ion(L) table (L=1.0: 10% ionized/200 periods; L=0.5: 95% ionized, median 17 periods) is the first published quantitative data for SED hydrogen ionization timescales as a function of angular momentum.

**Evidence:** E003 [COMPUTED], 20 trajectories per L value.

**Novelty search (E006):** Nieuwenhuizen-Liska (2015) has no explicit T_ion(L) table. Cole & Zou (2003) reports timescales only implicitly (runs were "short"). No prior paper found with quantitative T_ion vs. L.

**Critical caveat:** τ used was 60× physical value. Physical τ would give T_ion ≈ 60× longer. The qualitative pattern (T_ion decreasing with L) should survive, but all absolute values are wrong.

**Strongest counterargument:** Nieuwenhuizen (2015) certainly measured T_ion — they just didn't report it numerically. The tabular presentation may just reflect what they chose to publish, not what they computed. Without their raw data, we cannot claim priority for the measurement.

**Status: PARTIALLY VERIFIED (with τ caveat). Quantitative T_ion(L) data is not published in any paper found. But τ correction is needed before claiming publishability.**

---

## What the Next Strategizer Should Know

1. **Faria-França (2004) is the critical reference for tunneling.** Before claiming novelty for the Γ formula, read their full paper (arXiv:quant-ph/0409119) and map their Eq. 40 to our formula explicitly.

2. **The τ bug in E003 must be fixed** (use τ = 2.6×10⁻⁷ in atomic units). The corrected E003 code is in E005's `code/sed_sim_corrected.py`.

3. **Bell S ≤ 2 should not be presented as a finding.** The real finding is C_xx(d) = cos(ω₀d/c) as a SED-QM discrepancy. The 3D version of this (whether it averages to zero or r⁻⁶) is the open question worth pursuing.

4. **The strongest single publishable result** is the tunneling formula with R²=0.9998 across 4 decades. Even after Faria-França prior art, the S_WKB crossover condition, the numerical verification, and the ω_local=√2 universality make this worth publishing as a "Computational Verification and Extension" paper.

5. **Santos (2022)** "SED = O(ħ) QED" may be the key to explaining slope=1.049 and the 15-18% anharmonic residual. This is the highest-value unexplored direction.

---

## Pacing Notes (Deviations from Strategy)

- Phase 1: 3 explorations (as planned) — launched in parallel
- Phase 2: 1 exploration (plan said 1-2) — E004 was sufficient
- Phase 3A: 2 explorations (E005 was addendum to E001 not in original plan) — correct decision
- Phase 3B: 1 exploration (as planned) — E006 adversarial review
- Total: 6 of 10 budget used. Stopped early because adversarial review completed all required stress-testing. Remaining 4 slots left for next strategy's higher-priority work.
