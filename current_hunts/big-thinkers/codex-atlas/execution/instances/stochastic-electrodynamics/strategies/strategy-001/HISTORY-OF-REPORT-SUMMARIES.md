# Exploration History

## Exploration 001 — SED Harmonic Oscillator Ground State: Numerical Reproduction

**Goal:** Numerically reproduce the QM ground state of a harmonic oscillator from SED.

**Outcome: PARTIAL SUCCESS**

**Position variance: PASS.** var_x = 0.507 ± 0.05 vs target 0.5 (1.4% error for best run). Confirmed across all parameter regimes. Insensitive to UV cutoff. Gaussian distribution confirmed (KS p > 0.5).

**Total energy: FAIL (but explained).** The total energy is UV-divergent because the velocity variance grows logarithmically with the frequency cutoff. This is a real physics effect (electromagnetic self-energy divergence), not a simulation bug. The potential energy PE = 0.25 matches QM correctly.

**Key findings:**
- Found and fixed a critical normalization error (factor of π) in the ZPF spectral density
- Replaced time-domain Velocity Verlet with exact frequency-domain solution (linear system)
- Full Abraham-Lorentz transfer function is REQUIRED for UV convergence of var_x (effective damping gives divergent var_x)
- Frequency-domain approach BREAKS for nonlinear systems — anharmonic oscillator will need true time-domain simulation
- Code artifacts saved: `code/sed_harmonic_oscillator.py`, `code/debug_normalization.py`, `code/sed_corrected_run.py`

**Tags:** [VERIFIED]: spectral density, FFT normalization. [COMPUTED]: var_x, var_v, energy, Gaussianity, UV divergence scaling.

---

## Exploration 002 — SED Extension Landscape: What's Been Computed, What's Open

**Goal:** Survey the SED computation landscape across five domains (hydrogen, anharmonic oscillators, entanglement/Bell, g-2, other) to identify the best extension direction for a novel SED vs. QM numerical comparison.

**Outcome: SUCCEEDED**

### Key Findings

**SED has a sharp "linearity boundary."** Every SED success involves linear systems or free fields (harmonic oscillator, Casimir, van der Waals, blackbody). Every extension to nonlinear potentials, excited states, or interference phenomena has failed:

1. **Hydrogen atom:** Self-ionizes in long simulations (Nieuwenhuizen & Liska 2015). Renormalization doesn't help (Nieuwenhuizen 2020). Effectively closed as a research direction.

2. **Anharmonic oscillator:** Pesquera & Claverie (1982) proved analytically that SED disagrees with QM at order β² in the quartic perturbation. Three distinct signatures: wrong energy, wrong absorption frequencies, broken radiation balance. **This has never been verified numerically.**

3. **Entanglement/Bell:** Deeply contested. Marshall & Santos argue SED is compatible with Bell violations via contextuality. Mainstream physics rejects this. The computational question has not been done and would be intractable.

4. **g-2:** Pure SED has no spin, so g-2 can't be formulated. SEDS extension claims are non-standard and unverified.

5. **Quantum coherence:** Huang & Batelaan (2019) showed SED fails to produce interference fringes for squeezed cat states — a clean falsification.

### Recommendation

**Primary: Anharmonic oscillator ground state energy.** Numerically simulate V(x) = ½mω₀²x² + βx⁴ in SED and compare to QM perturbation theory. First numerical verification of a 40-year-old analytic result. Extends beyond perturbation theory to large β where SED vs. QM divergence is maximal.

**Secondary: SED tunneling rate** — compute barrier-crossing rates in a double-well potential, compare to WKB. Higher novelty but higher risk.

### Key References
- Pesquera & Claverie (1982), J. Math. Phys. 23(7), 1315–1322
- Nieuwenhuizen & Liska (2015), Physica Scripta T165, 014006
- Huang & Batelaan (2019), Atoms 7(2), 42
- Cole & Zou (2003), Phys. Lett. A 317, 14–20

---

## Exploration 003 — Anharmonic SED Oscillator: First Numerical Test of the Linearity Boundary

**Goal:** First numerical simulation of the anharmonic SED oscillator V(x) = ½x² + βx⁴. Compare SED vs QM position statistics for β = 0 to 1.0.

**Outcome: SUCCESS — major result found**

**SED fails QUALITATIVELY for the anharmonic oscillator.** QM var_x DECREASES with β (quartic confinement). SED var_x INCREASES with β (positive feedback from ω³ noise). Opposite trends!

| β    | var_x_QM | var_x_SED     | SED/QM | Significance |
|------|----------|---------------|--------|--------------|
| 0.00 | 0.500    | 0.515±0.007   | 1.03   | baseline     |
| 0.01 | 0.486    | 0.529±0.008   | 1.09   | 5.4σ         |
| 0.10 | 0.413    | 0.735±0.014   | 1.78   | 23.6σ        |
| 1.00 | 0.257    | 2.411±0.043   | 9.38   | 50.5σ        |

**Key findings:**
- The failure is at O(β), not O(β²) — but this is because the simulation uses the Langevin approximation (constant Γ = τω₀²), not the full Abraham-Lorentz dynamics (ALD)
- Physical mechanism: ω³ ZPF spectrum + constant damping → positive feedback loop pumps oscillator to larger amplitude. QM doesn't have this feedback (energy quantization controls level populations)
- P(x) shape: SED is super-Gaussian, QM is sub-Gaussian (KS p = 0.000 at β=0.1)
- Linearity boundary: β ≈ 0.005 (SED-QM excess exceeds 2σ)
- Pesquera & Claverie (1982) used the FULL ALD where damping is position-dependent → would expect agreement at O(β) but failure at O(β²)

**Critical next step:** Implement full ALD (Landau-Lifshitz order reduction) to test whether position-dependent damping fixes the O(β) failure, leaving only the O(β²) failure that P&C predicted.

---

## Exploration 004 — Full Abraham-Lorentz Dynamics: Direct Test of Pesquera-Claverie

**Goal:** Implement Landau-Lifshitz order-reduced ALD with position-dependent damping Γ_eff = τ(ω₀² + 12βx²). Test whether this fixes the O(β) failure from E003.

**Outcome: YES — O(β) failure is eliminated.**

3-way comparison:

| β    | var_x QM | var_x ALD (E004) | ALD err | var_x Langevin (E003) | Lang err |
|------|----------|------------------|---------|----------------------|----------|
| 0.00 | 0.500    | 0.516 ± 0.007    | +3.1%   | 0.515 ± 0.007        | +3.0%    |
| 0.10 | 0.413    | 0.426 ± 0.006    | +3.2%   | 0.735 ± 0.014        | +78.2%   |
| 1.00 | 0.257    | 0.303 ± 0.004    | +17.8%  | 2.411 ± 0.043        | +837.8%  |

**Key findings:**
- ALD improvement: 11× at β=0.1, 47× at β=1.0 vs Langevin
- For β ≤ 0.1: ALD error is statistically indistinguishable from β=0 baseline (no O(β) failure)
- For β > 0.2: Residual error grows as β^0.40 — slower than both O(β) and O(β²)
- ALD gets direction correct: var_x decreases with β (88% of QM slope)
- Physical mechanism: Γ_eff increases by 4.6× at β=1, counteracting ω³ noise pumping
- β^0.40 scaling (instead of P&C's O(β²)) is likely a UV-cutoff artifact (ω_max = 10)
- P&C prediction approximately supported but full verification needs larger ω_max and smaller τ

---

## Exploration 006 — Adversarial Review and Novelty Search

**Goal:** Attack our SED anharmonic oscillator findings (E001-E004). Literature novelty search, methodology critique, robustness/novelty/significance ratings.

**Outcome: MIXED — two findings survive attack, two are weaker than claimed**

**Rating table:**

| Finding | Robustness | Novelty | Significance | Verdict |
|---------|-----------|---------|--------------|---------|
| F1 (HO numerical) | 5/5 | 2/5 | 2/5 | Confirmatory |
| F2 (Langevin O(β)) | 4/5 | 3/5 | 3/5 | Real but needs reframing — it's an approximation failure, not SED failure |
| F3 (ALD + β^0.40) | 4/5 | 4/5 | 4/5 | **Main result** |
| F4 (linearity boundary) | 5/5 | 1/5 | 2/5 | Known concept (Boyer 1975, 2019) |

**Novelty search:** No prior time-domain numerical simulations of anharmonic SED oscillator found. Pesquera & Claverie (1982) is purely analytical. Moore & Ramirez (1981) studied the τ→0 limit analytically (different regime). Landau-Lifshitz order reduction applied to SED appears genuinely new.

**Methodology concerns:**
- 5.4σ claim at β=0.01 is overstated (should be ~2.5σ after baseline correction)
- UV cutoff explains β^0.40: 5th harmonic at β=1 exceeds ω_max=10
- Equilibration, LL errors, Euler-Cromer accuracy all cleared

**Key recommendation:** ω_max scan (E005) is THE critical remaining check. Determines whether β^0.40 is UV artifact (supports P&C) or intrinsic (contradicts P&C).

---

## Exploration 005 — UV-Cutoff Scan: β^0.40 Error is Real

**Goal:** Determine whether the β^0.40 residual error in ALD-SED is a UV-cutoff artifact or genuine. ω_max scan (10, 20, 30) and τ scan (0.01, 0.005, 0.002).

**Outcome: β^0.40 error is REAL — not a UV artifact**

ω_max scan (β=1.0, τ=0.01):
| ω_max | Δe     | Change vs ω_max=10 |
|-------|--------|-------------------|
| 10    | 0.0300 | reference         |
| 20    | 0.0279 | −7%               |
| 30    | 0.0245 | −18%              |

τ scan (β=1.0, ω_max=10):
| τ     | Δe     | Change vs τ=0.01 |
|-------|--------|-----------------|
| 0.010 | 0.0300 | reference        |
| 0.005 | 0.0257 | −14%             |
| 0.002 | 0.0208 | −31%             |

**Key finding:** Convergence is extremely slow: Δe ~ ω_max^(-0.18) × τ^0.23. P&C's O(β²) result requires τ < 10⁻⁶ and ω_max > 10⁷ — physically inaccessible. In the accessible regime (τ ~ 0.002-0.01, ω_max ~ 10-30), ALD-SED overpredicts var_x by 15-18% at β=1.

---

## Exploration 007 — β^0.40 Mechanism: ω³ ZPF Spectrum Is the Cause

**Goal:** Determine whether the ω³ ZPF spectral shape drives the β^0.40 power-law scaling (Hypothesis H1), by running ALD-SED with four noise spectra: n=0 (white), n=1 (ω¹), n=2 (ω²), n=3 (ω³ standard ZPF). Each spectrum was normalized to give var_x(β=0) ≈ 0.500.

**Outcome: H1 STRONGLY CONFIRMED**

**Key result: Only n=3 produces POSITIVE Δe; n=0,1,2 all produce NEGATIVE Δe.**

| n | Spectrum | sign(Δe) | α     | Δe at β=1.0 |
|---|----------|----------|-------|-------------|
| 3 | ω³ ZPF   | **+**    | 0.25  | +0.043      |
| 2 | ω²       | **−**    | 0.11  | −0.066      |
| 1 | ω¹       | **−**    | 0.06  | −0.113      |
| 0 | white    | **−**    | 0.02  | −0.138      |

The sign reversal between n=2 and n=3 is **qualitative** — the ω³ ZPF spectrum causes ALD-SED to overshoot QM variance with increasing β, while all softer spectra cause undershoot. All four spectra correctly reproduce the ↓ direction (var_x decreasing with β matches QM).

**Physical mechanism:** The ω³ spectrum is "tuned" for the harmonic ALD equilibrium (where Γ_eff ∝ ω²). For the anharmonic oscillator, the anharmonic harmonics at 3ω₀, 5ω₀ receive excess ZPF power ∝ ω³ that the ALD damping (∝ ω²) cannot fully compensate. This creates a net positive feedback that persists even with full ALD. Lower-n spectra lack this enhanced high-frequency content and the ALD overcompensates → undershoot.

**Crossover exponent n*:** Linear interpolation between n=2 (Δe=-0.066) and n=3 (Δe=+0.043) gives n* ≈ 2.61. The physical ZPF (n=3) lies above the stability threshold.

**Note on α discrepancy:** E004 found α≈0.40; E007 finds α≈0.25 for n=3. Difference is due to different normalization (calibrated 0.492 vs physical 0.516). α at physical normalization needs separate check.

**Tags:** [COMPUTED]: all 4 β-scan tables, normalization constants, QM references. [CONJECTURED]: n* ≈ 2.61, ω³ threshold mechanism, α discrepancy origin.

