# Sprint 1: Oppenheim Prediction — Where Does FDCG Sit?

**Date:** 2026-03-21
**Phase:** SPRINT (iteration 1)
**Verdict:** PARTIAL PASS

---

## The Question

Where does FDCG's Oppenheim prediction (σ_a = √(Gℏ/R³)) sit relative to (a) other quantum gravity theories' predictions, and (b) current and near-future experimental sensitivity?

## Method

1. Computed σ_a for FDCG at 5 test mass scales (fullerene → LISA PF)
2. Computed the same for Diósi-Penrose (unsaturated) and Kafri-Taylor-Milburn (unsaturated)
3. Compared to published and proposed experimental sensitivities
4. Skeptic challenged uniqueness, experimental realism, and frequency spectrum

## Key Results

### Master Comparison Table

All σ_a in m/s²/√Hz:

| Object | R (m) | m (kg) | FDCG | DP (unsaturated) | KTM (unsaturated) | FDCG/DP |
|--------|-------|--------|------|-------------------|--------------------|---------|
| C₆₀ fullerene | 3.5e-10 | 1.2e-24 | 1.28e-08 | 4.48e-06 | 3.66e-06 | 0.003 |
| OTIMA molecule | 1.0e-09 | 3.3e-23 | 2.65e-09 | 5.06e-07 | 4.13e-07 | 0.005 |
| Silica nanoparticle | 5.0e-08 | 1.1e-18 | 7.50e-12 | 3.92e-10 | 3.20e-10 | 0.019 |
| Diamond microsphere | 1.0e-06 | 1.47e-14 | 8.39e-14 | 7.58e-13 | 6.19e-13 | 0.111 |
| LISA PF test mass | 2.3e-02 | 1.928 | 2.41e-20 | 4.36e-22 | 3.56e-22 | 55.1 |

All arithmetic independently verified by Skeptic agent. Unit check: [Gℏ/R³] = m² s⁻³; √ → m/s²/√Hz. ✓

### Scaling Laws (the key distinguishing feature)

| Model | σ_a scaling (uniform sphere) | Depends on mass? | Free parameters |
|-------|------------------------------|------------------|-----------------|
| FDCG (= saturated DP) | R⁻³/² | NO | None |
| DP (unsaturated, parameter-free) | ρ⁻¹/² R⁻² | YES | None (RULED OUT) |
| KTM (unsaturated) | ρ⁻¹/² R⁻² | YES | None |
| Oppenheim continuous | varies with kernel width σ | depends on σ | σ (kernel width) |
| Any saturated-DP-like model | R⁻³/² | NO | None |

### Crossover Radius (FDCG = DP)

R_cross = 9/(10πρ): silica → 0.13 mm, diamond → 0.08 mm.
Below R_cross, FDCG predicts LESS noise than unsaturated DP. This is why FDCG evades the constraints that killed parameter-free DP (Donadi et al. 2021).

### Experimental Comparison

| Object | σ_a(FDCG) | Best achieved sensitivity | Gap | Proposed sensitivity | Projected SNR |
|--------|-----------|---------------------------|-----|---------------------|---------------|
| Silica NP (50 nm) | 7.50e-12 | ~1e-9 (current) | 133× below | ~1e-15 (MAQRO) | ~7500 |
| Diamond sphere (1 μm) | 8.39e-14 | ~1e-9 (current) | ~10⁵× below | ~1e-15 (Bouwmeester) | ~84 |
| LISA PF (2.3 cm) | 2.41e-20 | 5.2e-15 (achieved) | ~2×10⁵× below | — | — |

**CAVEAT (Skeptic):** All projected SNR values use *proposed*, not achieved, sensitivities. Current experiments are 5-6 orders of magnitude away. These SNR estimates are contingent on future experimental breakthroughs.

---

## Skeptic Challenges and Resolution

### 1. Is mass-independence unique to FDCG? → NO (SERIOUS)

The formula S_a = Gℏ/R³ arises from saturating the Oppenheim trade-off with DP-like decoherence. The mass cancels algebraically: D₂ ∝ M² and S_a = 2D₂/M². **Any model** with D₀ ∝ M² at saturation gives the identical prediction. KTM at saturation is indistinguishable.

**FDCG's actual unique contribution:** A physical mechanism (fracton dipole condensate vacuum fluctuations) that motivates WHY saturation occurs and WHY the kernel width equals R. This is an explanatory contribution, not a predictive one. An experiment measuring S_a = Gℏ/R³ would confirm "saturated DP-like decoherence" — it would not uniquely confirm FDCG over all alternatives.

### 2. DP comparison is against a dead model → MODERATE

Parameter-free DP is already ruled out by Donadi et al. (2021). The comparison shows FDCG differs from a dead model, which establishes viability but not novelty. The more relevant comparison — FDCG vs. Oppenheim continuous at various kernel widths — was not fully computed.

FDCG corresponds to the Oppenheim continuous model at σ_kernel = R, sitting on the saturation boundary. This is a specific, well-defined point in the Oppenheim parameter space.

### 3. Saturation assumption not derived → MODERATE

Saturation (D₂ = D₁²/(2D₀)) is assumed, not derived from the fracton condensate. However, mass-independence survives even without exact saturation: if D₂ = α · D₁²/(2D₀) with α ≥ 1, the M² still cancels, giving S_a = α · Gℏ/R³. The concern is that α could itself be mass-dependent without a rigorous derivation ruling it out.

**Mitigating:** Ground-state condensate = minimum fluctuation is a physically natural argument for saturation.

### 4. Frequency spectrum unspecified → MODERATE

White noise is assumed. The DP decoherence rate for a 1 μm diamond microsphere is Γ ≈ 137 s⁻¹ (f_DP ≈ 22 Hz). Optomechanical experiments typically operate at 10 kHz – 1 MHz. If the noise rolls off above f_DP, the SNR at measurement frequencies could be orders of magnitude worse than the white-noise estimate.

**This is an open question that needs future work.**

---

## Pass/Fail Assessment

| Criterion | Result | Notes |
|-----------|--------|-------|
| FDCG predicts distinguishable region vs. unsaturated DP | **PASS** | Different scaling: R⁻³/² vs R⁻² |
| FDCG predicts distinguishable region vs. ALL other models | **FAIL** | Same prediction as any saturated-DP-like model |
| FDCG has distinguishing experimental signature | **PASS** | Mass-independence (same noise for different densities at fixed R) |
| Experiments are close to testing FDCG | **PARTIAL** | 5-6 OOM gap in current sensitivity; proposals exist but unachieved |
| FDCG is within allowed experimental window | **PASS** | Consistent with LISA PF, evades Donadi et al. constraint |

**Overall: PARTIAL PASS.** FDCG's prediction is viable, distinguishable from unsaturated models, and has a clear experimental signature (mass-independence at fixed R). But it is NOT uniquely FDCG — any saturated-DP model gives the same numbers. The experimental timeline is 5-10+ years away at best.

---

## What We Learned

1. **The formula S_a = Gℏ/R³ is a prediction of the "saturated Oppenheim bound" class of models, not uniquely of FDCG.** FDCG provides a mechanism for saturation, but the prediction is shared.

2. **The smoking-gun experimental test is density variation at fixed radius.** Measure acceleration noise for silica vs. diamond nanoparticles of the same size. FDCG/saturated models predict identical noise; unsaturated models predict a density-dependent difference.

3. **The frequency spectrum of the noise is an unresolved open question** that could dramatically affect detectability. The DP decoherence rate sets a natural frequency scale; below it, noise may be enhanced; above it, suppressed.

4. **FDCG evades the constraint that killed parameter-free DP** because it predicts less noise at small scales (below the crossover radius ~0.1 mm).

5. **The most promising experimental path is diamond microspheres (R ~ 1-10 μm)** with next-generation optomechanical oscillators, BUT this requires 5-6 OOM improvement in sensitivity.

---

## Open Questions for Future Sprints

1. Can saturation be DERIVED from the fracton condensate, rather than assumed?
2. What is the frequency spectrum of the FDCG acceleration noise? Is it white, 1/f², or something else?
3. Does the Oppenheim continuous model at σ = R (i.e., FDCG's position) have any additional testable consequences beyond S_a?
4. Could the decoherence rate measurement (τ_dec for diamond microspheres) be easier to detect than the diffusion?

## Files

- Detailed calculations: `sprint-01-oppenheim-predictions.md`
- Skeptic review: `sprint-01-skeptic-review.md`
