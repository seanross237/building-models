# Sprint 1 Skeptic Review: FDCG Oppenheim Prediction Analysis

**Reviewer role:** Adversarial skeptic (fair but aggressive)
**Date:** 2026-03-21
**File under review:** sprint-01-oppenheim-predictions.md

---

## Challenge 1: Is mass-independence REALLY unique to FDCG?

**Severity: SERIOUS**

The Calculator's claim (line 223): "No other gravitational decoherence model predicts this [mass-independence]." This is **false**.

The mass-independence of S_a = Ghbar/R^3 is NOT a unique property of FDCG. It is a generic algebraic consequence of three ingredients:

1. Decoherence coupling D_0 proportional to M^2
2. Gravitational coupling D_1 proportional to M^2
3. Saturation of the Oppenheim bound (D_2 = D_1^2 / (2 D_0))

Given these three, D_2 ~ M^4/M^2 = M^2, and S_a = 2 D_2/M^2 cancels to M^0 automatically. Both DP and KTM have D_0 ~ M^2 and D_1 ~ M^2. Therefore **KTM at saturation gives the identical prediction S_a = Ghbar/R^3**. The sprint file itself notes KTM differs from DP "only by a prefactor" in the unsaturated case -- but fails to note that at saturation, even this prefactor difference vanishes and the two models converge to the same formula.

Any theory with D_0 ~ M^2/R^3 at saturation yields the same number. FDCG is one such theory; it is not the only one.

**What IS unique to FDCG:** The physical mechanism claiming to explain WHY saturation occurs (condensate vacuum fluctuations) and WHY the kernel width equals R (geometric extent of the test mass in the condensate). These are explanatory contributions, not predictive ones. An experimentalist cannot distinguish "FDCG at saturation" from "KTM at saturation" or "generic-DP at saturation" by measuring S_a alone.

**Verdict: VALID.** The uniqueness claim is overstated. The sprint file should say: "FDCG predicts S_a = Ghbar/R^3. This prediction is shared by any gravitational decoherence model with DP-like scaling at saturation. FDCG's unique contribution is providing a physical mechanism for saturation, not a unique numerical prediction."

---

## Challenge 2: The DP comparison is misleading

**Severity: MODERATE**

The Calculator compares FDCG against unsaturated DP throughout the table. But:

- Unsaturated parameter-free DP is **already ruled out** by Donadi et al. (2021) using underground germanium experiments.
- Comparing FDCG to a dead model and showing they differ does not establish that FDCG is novel or interesting. It establishes only that FDCG is not dead yet.

The more relevant comparison is FDCG vs. **Oppenheim's continuous model at various kernel widths sigma**. Analysis shows:

- Oppenheim continuous with Gaussian kernel width sigma at saturation gives S_a = Ghbar/sigma^3
- FDCG sets sigma = R (the object radius), making it a **specific point** on the Oppenheim parameter space
- The real question is whether the Oppenheim framework at sigma = R is already experimentally constrained or not

The sprint file does list Oppenheim continuous in the model table (line 19) but never actually computes its predictions for comparison. This is a gap.

**Verdict: VALID but not fatal.** The comparison against unsaturated DP is still informative for showing scaling-law differences. But the file should explicitly acknowledge that DP is ruled out and that the real competition is Oppenheim continuous models, where FDCG occupies one specific parameter point.

---

## Challenge 3: Is the saturation assumption justified?

**Severity: MODERATE**

The THEORIES.md derivation (line 376) states assumption 3: "The Oppenheim trade-off is SATURATED (minimum diffusion for given decoherence)." This is presented as an assumption, not derived from the fracton condensate.

If the bound is not saturated, D_2 = alpha * D_1^2/(2 D_0) with alpha >= 1, then S_a = alpha * Ghbar/R^3. Importantly, **mass-independence is preserved** regardless of alpha, because the M^2 cancellation occurs in D_1^2/D_0 before the alpha factor enters. So the scaling law survives non-saturation.

However, there is a subtlety: alpha could itself be mass-dependent if the mechanism producing excess diffusion (above the saturation floor) depends on properties of the test mass. Without a derivation from the condensate showing that the condensate's vacuum fluctuations produce exactly the saturation-level diffusion, alpha is effectively a hidden free parameter.

The sprint file does not discuss this at all. This is a gap in the analysis.

**Mitigating factor:** Saturation is the most natural assumption in many physical contexts (ground state = minimum energy = minimum fluctuation). FDCG's claim that the metric is a condensate order parameter does provide a qualitative argument for saturation: the condensate is in its ground state, which should minimize diffusion for a given decoherence rate. But this argument is qualitative, not quantitative.

**Verdict: VALID but answerable in principle.** The saturation assumption is physically motivated but not derived. The sprint file should flag this as an assumption that needs future derivation. The saving grace is that mass-independence survives even without exact saturation.

---

## Challenge 4: Experimental SNR claims are too optimistic

**Severity: SERIOUS**

The sprint file claims SNR = 84 for diamond microsphere experiments based on a proposed sensitivity of 1e-15 m/s^2/sqrt(Hz). This number requires scrutiny:

**The 1e-15 figure is aspirational, not achieved.** Current state of the art for levitated optomechanical force sensing is approximately:
- Achieved (2023-2024): ~1e-9 to 1e-10 m/s^2/sqrt(Hz) for levitated nanoparticles
- Best clamped mechanical oscillators: ~1e-12 m/s^2/sqrt(Hz)
- The 1e-15 target requires **5-6 orders of magnitude improvement** over current levitated systems

**The MAQRO SNR = 7500 is even more speculative.** MAQRO is a proposed ESA space mission that has not been approved for flight. Its target sensitivity of 1e-15 m/s^2/sqrt(Hz) for nanoparticles in space assumes zero-vibration, zero-gas-collision environment that has never been demonstrated at that scale.

**Systematic effects not discussed:**
- Radiation pressure noise from trapping laser
- Residual gas collisions (dominant in current experiments)
- Laser phase noise coupling to displacement readout
- Blackbody radiation recoil
- Electrical patch potentials (dominant for LISA Pathfinder at low frequencies)
- All of these produce acceleration noise that could mask or mimic the FDCG signal

The sprint file presents the SNR figures without any discussion of systematics, timelines, or the gap between proposed and achieved sensitivity. This makes the "detectable" claims misleadingly confident.

**Verdict: VALID and SERIOUS.** The SNR numbers are technically correct given the assumed sensitivity, but presenting them without caveats about the 5-6 OOM gap between current achievement and proposal is misleading. The file should clearly state: "These SNR figures assume proposed, not achieved, experimental sensitivities. Current experiments are 5-6 orders of magnitude away from the required sensitivity."

---

## Challenge 5: Frequency dependence

**Severity: MODERATE**

The sprint file assumes white (frequency-independent) noise throughout. The THEORIES.md file itself flags this as an open issue (line 451): "We assumed white noise. The actual spectrum may have 1/f^2 behavior or a cutoff frequency related to the DP rate."

For the diamond microsphere (R = 1 um, m = 1.47e-14 kg), the DP decoherence rate is:
- Gamma = G M^2 / (hbar R) = 137 s^-1
- f_DP = 22 Hz

This is a **low frequency**. Optomechanical experiments typically operate at mechanical frequencies of 10 kHz to 1 MHz. If the noise spectrum is NOT white but has a rolloff or 1/f^2 behavior above f_DP, then at the actual measurement frequencies (>> 22 Hz), the noise could be dramatically lower than the white-noise prediction.

Conversely, if the noise is concentrated below f_DP, it would be EASIER to detect at low frequencies but HARDER at the high frequencies where optomechanical sensitivity is best.

The sprint file does not discuss this frequency mismatch at all. This could change the SNR estimates by orders of magnitude in either direction.

**Verdict: VALID.** This is a genuine gap in the analysis. The frequency spectrum of the predicted noise must be specified before any SNR claim is meaningful. The sprint file should add a caveat: "All SNR estimates assume white noise. If the noise spectrum has frequency dependence, these estimates could change by orders of magnitude."

---

## Challenge 6: Unit check and numerical verification

**Severity: NONE (all correct)**

I independently recomputed all entries from scratch:

**FDCG values (all match exactly):**
- C60: 1.281e-08 -- CORRECT
- OTIMA: 2.653e-09 -- CORRECT
- Silica NP: 7.504e-12 -- CORRECT
- Diamond: 8.390e-14 -- CORRECT
- LISA PF: 2.405e-20 -- CORRECT

**DP values (all match exactly):**
- C60: 4.484e-06 -- CORRECT
- OTIMA: 5.059e-07 -- CORRECT
- Silica NP: 3.919e-10 -- CORRECT
- Diamond: 7.580e-13 -- CORRECT
- LISA PF: 4.364e-22 -- CORRECT

**KTM values (all match):** Verified sqrt(2/3) prefactor relative to DP.

**FDCG/DP ratios (all match):** 0.003, 0.005, 0.019, 0.111, 55.1

**Crossover radii (match):** Silica 0.130 mm, Diamond 0.082 mm

**R_detect values (match):** 1.9 nm, 8.9 nm, 19 um, 6.4 um

**G*hbar product:** Calculator correctly identified the 0.03% discrepancy in the prompt's value and used the exact product 7.0385e-45. Good practice.

**Unit check:** [G*hbar/R^3] = [m^3 kg^-1 s^-2 * J s / m^3] = [m^3 kg^-1 s^-2 * kg m^2 s^-1 / m^3] = [m^2 s^-3]. sqrt gives m s^(-3/2) = m/s^2/sqrt(Hz). CORRECT.

**Cross-check against THEORIES.md table:** The THEORIES.md predictions for different radii also match independent computation. Note that the THEORIES.md table uses different test objects (e.g., C720 at R=5e-10 vs. sprint's C60 at R=3.5e-10), so the numbers differ appropriately.

**Verdict: NO ISSUES FOUND.** All arithmetic is correct. The Calculator did careful, reproducible work.

---

## Overall Assessment

### Does FDCG genuinely occupy a distinguishable region of prediction space?

**YES, but with important caveats that the sprint file fails to state.**

**What holds up under scrutiny:**
1. The arithmetic is flawless. Every number checks out.
2. FDCG (= saturated DP) IS distinguishable from unsaturated DP. The scaling laws are structurally different (R^(-3/2) vs R^(-2) for uniform density).
3. The mass-independence signature IS a real, testable prediction. Measuring the same noise for different-mass objects at the same R would be strong evidence.
4. The crossover analysis is correct and informative.
5. FDCG IS inside the experimentally allowed window (consistent with LISA Pathfinder).

**What does NOT hold up:**
1. **The uniqueness claim is wrong.** S_a = Ghbar/R^3 is not unique to FDCG. Any DP-like model at saturation gives the same formula. KTM at saturation is identical. The sprint file should not claim this formula distinguishes FDCG from all competitors.
2. **The experimental detectability claims are misleadingly optimistic.** The SNR = 84 and SNR = 7500 figures use proposed, not achieved, sensitivities. Current experiments are 5-6 OOM away. No systematic effects are discussed.
3. **The frequency spectrum is unspecified.** White noise is assumed but not justified. The DP decoherence rate for the diamond microsphere is only 22 Hz, which is well below typical optomechanical measurement frequencies. If the noise rolls off above this frequency, the SNR estimates are invalid.
4. **The saturation assumption is not derived.** It is physically motivated but remains an assumption. The sprint file should flag this explicitly.

### Summary Scorecard

| Challenge | Severity | Status |
|-----------|----------|--------|
| 1. Mass-independence uniqueness | SERIOUS | Claim overstated. Formula shared by any saturated-DP model. |
| 2. DP comparison misleading | MODERATE | Should compare to Oppenheim continuous, not dead model. |
| 3. Saturation assumption | MODERATE | Assumed, not derived. Mass-independence survives regardless. |
| 4. Experimental SNR optimism | SERIOUS | 5-6 OOM gap between current and proposed sensitivity unmentioned. |
| 5. Frequency dependence | MODERATE | White noise assumed without justification. Could shift SNR by OOM. |
| 6. Numerical accuracy | NONE | All calculations verified correct. |

### Bottom Line

**The calculation is correct but the interpretation oversells.** FDCG does not make a unique prediction -- it makes the same prediction as any DP-like gravitational decoherence model at saturation. What FDCG uniquely provides is a physical mechanism (fracton condensate) that motivates saturation, but this mechanism has not been shown to rigorously produce saturation. The experimental claims are contingent on 5-6 orders of magnitude improvement in sensitivity and on the noise being white at measurement frequencies, neither of which is established.

The sprint file should be revised to:
1. Replace "no other model predicts this" with "this prediction is shared by any saturated-DP-like model; FDCG provides a mechanism for why saturation occurs"
2. Add a clear caveat about the gap between proposed and achieved experimental sensitivity
3. Flag the white-noise assumption as unverified
4. Add Oppenheim continuous model predictions at sigma = R for direct comparison
5. Note the frequency-spectrum open question from THEORIES.md line 451

**Overall grade: B.** Solid computation, overstated interpretation.
