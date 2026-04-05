# Exploration 010 Summary: Adversarial Review of Novel Claims

## Goal
Stress-test the three most promising novel claims from prior explorations, trying to break each one.

## What Was Tried
Systematic adversarial analysis of each claim: searched for prior art, tested statistical validity, checked definitions against source papers, ran numerical verifications. Computed the correct Adhikari-Cao Δ_G values from first principles to cross-check Exploration 008.

## Outcomes by Claim

---

### Claim 1: Power-Law Convergence Rate α ≈ 0.7–2.5
**Verdict: SERIOUS — needs major qualification**

**Strongest counterargument:** The power law is fit to exactly 3 data points with 2 free parameters, giving zero degrees of freedom. Any monotone decreasing function through 3 points can be called a "power law" — it proves nothing about functional form. Competing fits (exponential, log-log) are nearly as good.

**Statistical problem found:** At β=1.0 (where α≈2.4 was claimed), all three deviations (0.0019, 0.0008, 0.00004) are **below the Monte Carlo noise floor of ±0.002–0.003**. The α≈2.4 value is a fit to statistical noise. At β=2.0 (where α≈0.7 was claimed), the 2O and 2I deviations are only 1.2–1.7σ above zero.

**Additional issue:** The range "α ≈ 0.7–2.5 depending on observable" is misleading — both values come from the SAME observable (plaquette) at different β values. The variation is β-dependent, not observable-dependent.

**What survives:** The qualitative monotone ordering (2T → 2O → 2I → SU(2)) and the fact that 2I agrees with SU(2) to <0.5% are robust. The specific α claim is not statistically established.

**Novelty status:** Still appears novel that no prior paper extracted power-law rates for Euclidean LGT observables vs. group order, but must be stated with appropriate caveats about statistical significance.

---

### Claim 2: Adhikari-Cao Bounds Are 10–23x Vacuous
**Verdict: SERIOUS — quantitative error found, but conclusion stands stronger than claimed**

**Critical error found:** Exploration 008 used the **Cayley graph Laplacian** as Δ_G, but the Adhikari-Cao paper defines Δ_G = min_{g≠1} Re(χ(1)−χ(g)) — the character minimum. For the fundamental representation this is 2(1 − max Re(g₀)). These are different by factors of 3–6x.

**Computed correct values:**
| Group | Δ_G (correct) | β_min (correct) | β_c | Ratio |
|-------|--------------|-----------------|-----|-------|
| 2T    | 1.0000       | 126.7           | 2.2 | 57.6x |
| 2O    | 0.5858       | 221.0           | 3.2 | 69.1x |
| 2I    | 0.3820       | 348.6           | 5.8 | 60.1x |

The correct ratios are **57–69x** (not 10–23x). The exploration's wrong definition **understated** the vacuousness by ~4x. The core claim ("bounds are vacuous") is correct and actually stronger than reported.

**Additional issue:** The "divergence as |G| → ∞" claim is technically an extrapolation since SU(2) has only THREE binary polyhedral subgroups — there is no infinite sequence to take |G| → ∞ within this class. The divergence is real for the formula β_min(|G|) but applies to the analytic expression, not a literal sequence of SU(2) subgroups.

**Cayley gap non-monotonicity is telling:** The Cayley graph values (4.0, 1.757, 2.292) are NON-MONOTONE (2I > 2O), which is physically wrong. The correct character-minimum values (1.0, 0.586, 0.382) ARE monotonically decreasing, consistent with groups approaching SU(2).

---

### Claim 3: Four-Layer Structural Barrier
**Verdict: MODERATE — overstated in two ways**

**Counterargument 1 (interpretive framing):** The four layers are our own analytical construction, not a theorem. The layers are also not independent — they all stem from the same root cause: G must be discrete for the proof to work. One could equally describe this as "one fundamental obstruction (continuity of G) appearing in four aspects of the proof."

**Counterargument 2 (not provably permanent):** Calling barriers "structural, not technical" is a prediction about future mathematics. History shows many "structural" barriers eventually yield to new techniques (Adhikari-Cao's swapping map itself was this — Borgs' counterexample was thought to make cluster expansion impossible for non-abelian groups, and Adhikari-Cao routed around it). Layers 3 (swapping map → optimal transport?) and 1 (discrete defect support → continuous defect measure?) may be addressable.

**Counterargument 3 (other approaches circumvent all four):** Shen-Zhu-Zhu's Langevin/Bakry-Émery approach already works for continuous groups. This shows the four layers are barriers to **this specific proof strategy**, not to the mass gap problem. The Adhikari-Cao barriers don't prevent new techniques from succeeding.

**What survives:** The four-layer description correctly identifies where the Adhikari-Cao proof fails when extended to SU(2). It remains useful as a roadmap for why any attempt to extend this strategy must overcome these specific obstacles.

---

## Key Takeaway

**One explicit error was found:** Exploration 008 used the wrong definition of Δ_G (Cayley graph Laplacian instead of Adhikari-Cao's character minimum). The corrected β_min ratios are 57–69x (not 10–23x). The bounds are MORE vacuous than claimed. This is the main quantitative correction from this adversarial review.

The other two claims survive with qualifications: the convergence rate claim needs to be downgraded from a precise power law to a qualitative monotone ordering (the α values are not statistically established), and the four-layer barrier claim needs to be moderated from "structural/permanent" to "current obstructions to this specific approach."

---

## Unexpected Findings

- The Cayley graph Laplacian values in Exploration 008 are non-monotone across groups (2I > 2O), which was a red flag pointing to the definitional error. The correct character-minimum values are monotonically decreasing, as expected.
- At β=1.0, ALL deviations are below the Monte Carlo noise floor — the α≈2.4 claim is entirely based on noise. This was not explicitly checked in the original explorations.
- The correct β_min values (127, 221, 349) show an increasing trend within the binary polyhedral sequence itself — meaning even within the existing three subgroups, the bounds become MORE vacuous as the group gets larger. This is the right pattern.

## Computations Identified

1. **Recompute β_min with correct Δ_G** (5-line calculation): Already done here. Result: 57–69x ratios. This should be incorporated into the final strategy report.

2. **Higher-statistics convergence study** (medium difficulty, ~100-line script): Rerun Exploration 005 with 10x more Monte Carlo samples to get reliable estimates of |⟨P⟩_G − ⟨P⟩_SU(2)| above the noise floor for all three groups at the same β. This would either confirm or refute the power-law claim with statistical significance.

3. **Representation-theoretic prediction of α** (medium difficulty, analytical): Compute which SU(2) irreps are absent from each binary polyhedral group's representation ring, which determines the leading convergence correction analytically. Compare to empirical α. If they match, the power law is "predicted" from theory.
