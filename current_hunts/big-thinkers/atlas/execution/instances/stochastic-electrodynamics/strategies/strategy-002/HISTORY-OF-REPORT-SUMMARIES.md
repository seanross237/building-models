# Exploration History

---

## Exploration 001 — SED Double-Well Barrier Crossing vs WKB (2026-03-27)

**Goal:** First numerical simulation of SED barrier crossing in double-well potential using ALD equation. Compare SED barrier-crossing rate to QM tunneling rate.

**Key Quantitative Results:**
- λ=0.25 (S_WKB=1.41): Γ_SED = 0.0663±0.0035 ω₀ vs Γ_QM = 0.0578 ω₀ → **ratio 1.15 (15% agreement)**
- λ=0.10 (S_WKB=6.29): Γ_SED = 0.00790±0.00137 ω₀ vs Γ_QM = 0.000428 ω₀ → **ratio 18.5 (18× overestimate)**
- λ=1.0: Over-barrier regime (E₀ > V_barrier), no WKB comparison

**Key Finding:** New formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf). At λ=0.25 the two exponents coincide (both ≈1.41), explaining 15% agreement. For deep barriers (λ=0.10), S_WKB >> V_barrier/E_zpf, explaining 18× overestimate.

**Nature of SED crossings:** ZPF-driven over-barrier crossings (not quantum tunneling). Particles never escape both wells. Moderate barriers: coherent tunneling-like oscillation (~15 ω₀⁻¹ period). Deep barriers: metastable trapping with rare burst events.

**Novelty:** First numerical SED simulation of double-well barrier crossing with ALD+ZPF noise vs exact QM. Faria & Franca (2005) was analytical only. Drummond (1989) confirmed truncated Wigner fails for large barriers — consistent with our 18× result. [CONJECTURED — based on search, not exhaustive]

**Status:** Succeeded. Explorer Type: Math.

---

## Exploration 002 — Two SED Oscillators: ZPF Correlations and Bell S (2026-03-27)

**Goal:** Simulate two harmonic oscillators sharing same ZPF realization (phase-shifted for separation d). Compute C_xx(d), C_pp(d), Bell-CHSH S.

**Key Quantitative Results:**

| d | C_xx (sim) | C_xx = cos(ω₀d/c) | S_max | S > 2? |
|---|------------|---------------------|-------|--------|
| 0.0 | 1.0000 | 1.0000 | 2.000 | NO |
| 0.1 | 0.9948 | 0.9950 | 1.949 | NO |
| 1.0 | 0.5384 | 0.5400 | 1.092 | NO |
| 10.0 | -0.8328 | -0.8391 | 1.613 | NO |

Individual var_x ≈ 0.49–0.51 (QM: 0.500). Agreement within 2%.

**Key Finding:** Shared ZPF creates C_xx(d) = cos(ω₀d/c) — oscillating with separation (not decaying), and completely absent in QM for uncoupled oscillators. These are classical common-cause correlations. Bell S ≤ 2 always — SED never violates Bell bound. Unexpected: at d=10, C_xx = -0.83 (anti-correlation due to half-wavelength phase flip).

**Novelty:** First direct computation of Bell-CHSH from two SED oscillators sharing ZPF realization. de la Peña (2010) claims structural entanglement in LSED but never computed Bell S. [CONJECTURED — not exhaustive]

**Key gap identified:** In 1D, C_xx oscillates. In 3D with all k-vectors, would it average to zero (recovering QM C_xx=0) or give van der Waals r⁻⁶ term? This is the discriminating question.

**Status:** Succeeded. Explorer Type: Math.


---

## Exploration 003 — SED Hydrogen: Time to Self-Ionization (2026-03-27)

**Goal:** Simulate SED hydrogen (electron in Coulomb potential + ZPF noise). Measure T_ion as function of initial angular momentum L.

**Key Quantitative Results:**

| L/ħ | Ionized in 200 periods | Median T_ion | ⟨r⟩/a₀ |
|------|------------------------|--------------|---------|
| 1.0 | 10% (2/20) | ~57 periods | **1.47 ≈ QM 1.50** |
| 0.9 | 35% (7/20) | ~108 periods | 1.24 |
| 0.7 | 75% (15/20) | ~83 periods | 1.05 |
| 0.5 | 95% (19/20) | ~17 periods | 1.15 |

**Key Finding:** NO stability window — all L values show eventual self-ionization. L=1.0 (circular orbit) appears stable short-term but extrapolates to ~100% ionization within ~9,000 periods. Reconciles Cole & Zou (2003) short-run optimism with Nieuwenhuizen (2015) long-run pessimism.

**Novel finding:** First quantitative T_ion(L) measurements. At L=0.5, minimum T_ion = 0.24 periods (ionizes before first orbit completes).

**Caveat:** τ used was ~60× too large (1.57×10⁻⁵ vs physical 2.6×10⁻⁷ atomic units), so T_ion values are ~60× too short.

**Status:** Succeeded. Explorer Type: Math.

---

## Exploration 004 — Phase 2 Root Cause Synthesis (2026-03-27)

**Goal:** Literature survey of SED modifications (Boyer, de la Peña-Cetto, Pesquera-Claverie, Santos, Nieuwenhuizen). Assess ω³ feedback hypothesis. Evaluate three proposed fixes. Identify which E001-E003 claims are novel.

**Key Findings:**

- **Root cause confirmed:** The ω³ feedback mechanism correctly unifies all SED failures. Boyer (1976) showed nonlinear oscillators push ZPF toward Rayleigh-Jeans; Claverie-Diner (1977) identified Fokker-Planck failure; Santos (2022) gave ħ-order framing. No paper explicitly unified all three failures — that unified narrative is NEW.

- **Fix space is bleak:** Fix A (Local FDT/position-dependent noise) — genuinely new idea but worsens failures. Fix B (spectral index n<3) — new idea but breaks Lorentz invariance. Fix C (dressed particle/renormalization) — exhaustively tested by Nieuwenhuizen (2020), all fail.

- **Claim survival:**
  - Claim A (Γ formula): Novel vs. Faria & França. Needs 4-5 more λ values to verify.
  - Claim B (C_xx = cos(ω₀d/c)): May be derivable from Boyer correlators; Bell-CHSH ≤ 2 demo is new.
  - Claim C (T_ion data): Genuinely new; physical τ correction (×60) needed.
  - Claim D (ω³ unification): Genuinely new synthesis with good evidential support.

- **Unexpected:** ω_local = √2 is UNIVERSAL for double-well V = -½x² + ¼λx⁴ (regardless of λ). The 15% crossover at λ=0.25 is NOT a coincidence — it's the specific λ where S_WKB(0.25) ≈ V_barrier/E_zpf = 1.41.

- **LSED ≠ fix:** de la Peña's LSED handles only resonant modes in linear systems; doesn't fix nonlinear failures.

**Status:** Succeeded. Explorer Type: Standard.

---

## Exploration 005 — SED Tunneling Formula Verification (2026-03-27)

**Goal:** Verify Γ_SED/Γ_exact ≈ A × exp(S_WKB − V_barrier/E_zpf) at 5 new λ values (0.30, 0.20, 0.15, 0.075, 0.05).

**Key Quantitative Results:**

Linear fit across all 7 data points (E001 + E005), spanning 4 decades in ratio:
```
ln(Γ_SED/Γ_exact) = 0.072 + 1.049 × (S_WKB − √2/(4λ))
```
- **slope = 1.049 ± 0.007** (expected 1.0; 5% deviation from unit slope) ✓
- **A = exp(0.072) = 1.075** ✓
- **R² = 0.99977** — near-perfect linear fit ✓
- Maximum prediction error: 7%
- Formula holds for λ=0.05 (ratio=6263): no breakdown detected

**Key bugs found and fixed:**
1. ω_max cutoff not applied in goal code — changes A by ~50% but not slope
2. S_WKB outer-wall contamination — naive integral overestimates S_WKB by 3–15×

**Unexpected:** Slope = 1.049 is significantly > 1.0 (p < 0.002). May indicate sub-leading correction to WKB or Boltzmann factor.

**Verdict:** EXCELLENT SUCCESS. The formula `ln(Γ_SED/Γ_exact) ≈ ln(A) + (S_WKB − V_b/E_zpf)` is now verified across 4 decades with R²=0.9998. This is a publishable quantitative result.

**Status:** Succeeded. Explorer Type: Math.

---

## Exploration 006 — Adversarial Review of All Four Claims (2026-03-27)

**Goal:** Aggressively challenge four SED novel claims as a PRL referee would. Find prior art and weaknesses.

**Key Findings:**

Critical prior art found:
- **Faria, França & Sponchiado (2004)** arXiv:quant-ph/0409119 / Found. Phys. 35 (2005): derived κ ∝ exp(−ΔU/(ħωa/2)) analytically using Kramers-Chandrasekhar theory. This IS the exponential structure of Claim A (tunneling formula).

| Claim | Verdict |
|-------|---------|
| A (tunneling formula) | **Marginally Novel** — core exponential known (Faria-França 2004), but ratio-to-QM formulation, S_WKB connection, R²=0.9998 numerical verification, and ω_local=√2 universality are new |
| B (Bell S ≤ 2) | **Not Novel** — tautologically true (SED is local-realistic by construction); C_xx=cos(ω₀d/c) is one-line derivation from Boyer 1975. Real finding: ZPF oscillating correlations absent in QM |
| C (T_ion data) | **Partially Novel** — qualitative picture known, quantitative T_ion(L) new but τ is 60× wrong |
| D (ω³ unification) | **Partially Novel** — mechanism in Boyer 1976 + Pesquera-Claverie 1982, but explicit unification across three failure modes is new |

**Unexpected:** Ibison-Haisch (1996) Phys. Rev. A 54, 2737 explicitly shows ω³ integral in ZPF variance (their Eq. 58) — useful citation for Claim D.

**Status:** Succeeded. Explorer Type: Standard.
