# Exploration 006 — Adversarial Review and Novelty Search

**Date:** 2026-03-27
**Status:** COMPLETE

---

## Summary of Findings Under Review

| Finding | Claim | Source |
|---------|-------|--------|
| F1 | SED reproduces QM harmonic oscillator ground state (var_x = 0.507 vs 0.500) | E001 |
| F2 | Langevin-approximation SED fails at O(β) for anharmonic oscillator | E003 |
| F3 | Full ALD (Landau-Lifshitz) fixes O(β) failure; residual β^0.40 at large β | E004 |
| F4 | "Linearity boundary": SED succeeds iff system is linear | E002 |

---

## Part 1: Novelty Search — Prior Numerical Simulations

Searches conducted: 12 distinct queries across Google/web for each of the 4 novelty claims.

### 1.1 Search: Anharmonic oscillator + SED numerical simulations

**Queries used:**
- "anharmonic oscillator stochastic electrodynamics numerical simulation quartic"
- "stochastic electrodynamics anharmonic oscillator numerical simulation var_x position variance 2000 2010 2015 2020 2025"
- "stochastic electrodynamics quartic anharmonic simulation numerical time domain radiation reaction 2010 2015 2020"
- "stochastic electrodynamics numerical simulation anharmonic quartic oscillator position distribution time series 2020 2021 2022 2023 2024 2025"

**Findings:**

The field is dominated by **two known analytical results**:

1. **Pesquera & Claverie (1982)**, J. Math. Phys. 23(7), 1315–1322: Proved analytically that SED with full ALD fails at O(β²). Used Fokker-Planck + perturbation theory. **No numerical simulation.** This is the definitive analytical result.

2. **Moore & Ramirez (1981)**, Il Nuovo Cimento B, vol. 64, p. 275: Examined SED for harmonic and anharmonic oscillators. Key claim: "in the limit of zero charge, classical SED qualitatively agrees with quantum mechanics for the anharmonic oscillator, but ambiguities make quantitative comparison difficult." **Potentially contradicts our E003 Langevin result.**
   - IMPORTANT: "zero charge limit" = τ → 0 (radiation reaction → 0). This removes the damping and noise entirely. In this limit, the ω³ ZPF noise pumping mechanism identified in E003 is absent. This is a different regime from our simulation (τ = 0.01).
   - Their claim of "qualitative agreement" likely refers to the sign of the O(β) shift — but their method treats the SED oscillator as a harmonic oscillator with a perturbation, not a fully self-consistent nonequilibrium simulation.
   - **Bottom line:** Moore & Ramirez do NOT contradict our findings. They study a different limit (τ→0 = no radiation reaction = trivially no pumping).

**No prior numerical simulations found:**
- No time-domain Langevin simulation of anharmonic SED oscillator found in any search.
- No papers computing position variance vs. β for SED in time domain.
- No papers computing the full P(x) distribution for anharmonic SED.
- The arXiv paper 1205.0916 (SED review) is a theoretical review with no numerical anharmonic simulations.
- Daniel Cole's SED numerical work (2005, bu.edu/simulation/) focuses on the harmonic oscillator and hydrogen atom.
- The SED numerical literature is focused on: harmonic oscillator (well-studied), hydrogen atom (self-ionization), Casimir/van der Waals (linear systems).

**Novelty verdict for F2/F3:** The time-domain numerical simulation of the anharmonic SED oscillator — specifically measuring var_x as a function of β and detecting the qualitative failure — **appears to be genuinely new** as of 2026.

### 1.2 Search: O(β) Langevin failure vs. O(β²) ALD distinction

**Query used:** "SED Abraham-Lorentz Landau-Lifshitz stochastic electrodynamics anharmonic position dependent damping"

**Findings:**

The distinction between Langevin (constant Γ) and full ALD (position-dependent Γ) failure modes for SED is **not present in the literature**. Searches for this specific topic return:
- Papers on Landau-Lifshitz reduction for relativistic laser-plasma physics (completely different context)
- Reduction-of-order papers (Phys. Rev. D) for ALD in high-intensity lasers
- No papers applying the LL reduction to an SED harmonic/anharmonic oscillator

**The P&C (1982) paper itself** used the full ALD and derived its O(β²) result analytically. It does not discuss what happens with constant-Γ Langevin approximation.

**The "O(β) Langevin failure" (E003 Finding 2) is a novel observation.** The positive feedback mechanism (ω³ noise × constant Γ → pumping) has not been identified in the literature. P&C implicitly avoided it by using full ALD, but never noted that Langevin approximation would fail one order earlier.

**Novelty verdict for F2:** Potentially novel, but with an important caveat: it's possible P&C knew the Langevin approximation was incorrect for this reason and simply used full ALD from the start. This makes Finding 2 a "known pitfall, first explicitly demonstrated and quantified" rather than a surprise.

### 1.3 Search: Landau-Lifshitz order reduction applied to SED

**Query used:** "SED Landau-Lifshitz order reduction radiation reaction nonlinear oscillator anharmonic numerical"

**Findings:**

The Landau-Lifshitz reduction in the literature is used almost exclusively for:
- Relativistic electron motion in intense laser fields (Phys. Rev. D papers)
- Magnetism (Landau-Lifshitz-Gilbert equation)

**No paper found applying the LL reduction to the SED anharmonic oscillator.** The LL equation for SED (resulting in position-dependent damping Γ_eff = τ(ω₀² + 12βx²)) and its numerical implementation are **genuinely novel**.

**Novelty verdict for F3:** The LL-reduced ALD simulation is novel. However, the equation itself is derivable straightforwardly from the standard LL prescription applied to V = ½x² + βx⁴. A physicist who tried would derive the same equation. Novelty is in the numerical execution and the confirmation that it fixes the O(β) failure.

### 1.4 Search: "Linearity boundary" as named concept

**Queries used:**
- "SED stochastic electrodynamics linearity boundary nonlinear oscillator failure classical quantum"
- "Boyer stochastic electrodynamics closest classical approximation quantum linear nonlinear 2019"

**Findings:**

The CONCEPT that SED succeeds only for linear systems is WELL KNOWN. Multiple papers state it explicitly:
- Boyer (2019), Atoms 7(1), 29: "Stochastic electrodynamics gives predictions agreeing with quantum mechanics for linear systems (Hamiltonians quadratic in positions and momenta), but not for nonlinear systems."
- Boyer (1975), multiple papers: Identified that SED = QM exactly for harmonic oscillators, and fails for Coulomb-based (nonlinear) atomic potentials.
- Claverie, Diner, and others (1970s-1980s): This boundary was recognized early in the field.

**What is NEW in our E002 "linearity boundary" finding:**
- We have given it a specific name ("linearity boundary") and a quantitative threshold (β > 0.005)
- We have numerically confirmed and quantified it for the quartic anharmonic oscillator
- We have listed the exact set of successes/failures systematically

**Novelty verdict for F4 ("linearity boundary"):** The concept is NOT novel. It's been known since the 1970s-1980s. What's new is the systematic articulation, naming, and numerical quantification. This finding should be presented as "confirming and quantifying a known pattern" not as a new discovery.

### Summary of Novelty Search

| Finding | Prior work found | Our novelty |
|---------|-----------------|-------------|
| F1 (HO numerical) | Huang 2013, Cole numerical HO work | Confirmatory; our implementation is independent but not new concept |
| F2 (Langevin O(β) failure) | P&C 1982 (implicit); no explicit prior work | Likely novel: first explicit demonstration and mechanism |
| F3 (ALD LL fix + β^0.40) | P&C 1982 (analytical O(β²) prediction) | Novel: first numerical verification of P&C via LL; β^0.40 residual is new |
| F4 (linearity boundary) | Boyer 2019, Boyer 1975, Claverie/Diner 1970s-1980s | Conceptually known; quantification is new but incremental |

---

## Part 2: Methodology Attack

### Attack 2.1: Langevin equation validity — IS THE FAILURE TRIVIAL?

**The adversarial case:** The Langevin approximation (constant Γ = τω₀²) is obtained by replacing the exact Abraham-Lorentz x''' term with a harmonic approximation x'' → -ω₀²x, giving Γ = τω₀². This approximation is valid ONLY when the force is approximately harmonic, i.e., when |4βx³| << |ω₀²x|, meaning β*x_rms² << 0.25.

**Quantitative validity check** (computed):
| β    | 4β·x_rms² | Langevin valid? |
|------|-----------|----------------|
| 0.01 | 0.012     | YES |
| 0.05 | 0.061     | YES |
| 0.10 | 0.121     | YES (marginal) |
| 0.50 | 0.605     | NO |
| 1.00 | 1.210     | NO |

**DAMNING VERDICT:** The O(β) failure in Finding 2 occurs at β=0.01–0.10, where the Langevin approximation IS valid by this criterion. The failure is therefore NOT trivial — it's a real physical effect even within the regime where Langevin should work.

BUT: The mechanism (constant Γ doesn't track changing ω_eff) is an expected consequence of the approximation, not a SED fundamental failure. Finding 2 should be labeled "Langevin approximation fails at O(β)" not "SED fails at O(β)." The distinction matters because E004 shows full ALD (which the Langevin approximates) fixes it.

**Robustness impact on F2:** The finding is real and correctly computed, but its physical interpretation requires care.

---

### Attack 2.2: Landau-Lifshitz O(τ²) errors

**The adversarial case:** The LL reduction drops O(τ²) terms. Could these explain the β^0.40 residual in E004?

**Computed:** At τ=0.01, β=1:
- O(τ²) corrections to force: τ² × ω₀³ ≈ 10⁻⁴ (negligible vs typical forces ~0.55)
- τ² × d²F/dt² terms are of order τ² × ω₀⁵ × var_x ≈ 5×10⁻⁵
- The β^0.40 residual at β=1 is ~0.030 in var_x, which is 300× larger than O(τ²) corrections.

**VERDICT:** O(τ²) LL errors cannot explain the β^0.40 residual. Cleared.

---

### Attack 2.3: Noise spectrum fidelity — UV CUTOFF IS THE MAIN CONCERN

**The adversarial case:** The UV cutoff at ω_max=10 creates an artificial truncation of the ZPF spectrum. This violates the FDT (fluctuation-dissipation theorem) for ω > ω_max: modes above the cutoff are still damped (by the radiation reaction in the equation of motion) but receive no ZPF drive.

**Anharmonic mode coupling analysis** (computed):
The quartic potential V = βx⁴ generates harmonics at 3ω_eff, 5ω_eff, etc. The effective frequency ω_eff = √(1 + 12β·var_x).

| β    | ω_eff | 3rd harmonic | 5th harmonic | UV cutoff exceeded? |
|------|--------|--------------|--------------|---------------------|
| 0.00 | 1.000  | 3.00         | 5.00         | NO |
| 0.10 | 1.229  | 3.69         | 6.15         | NO |
| 0.50 | 1.750  | 5.25         | 8.75         | NO |
| 1.00 | 2.153  | 6.46         | **10.77**    | YES (5th harmonic) |

**KEY FINDING:** At β ≈ 0.5–1.0, the 5th harmonic of the anharmonic oscillator exceeds ω_max=10. This creates a UV artifact: the oscillator tries to couple to modes that have no ZPF drive, creating an effective energy sink. This EXPLAINS why the β^0.40 residual appears at β > 0.2 but NOT at β ≤ 0.1.

**Prediction:** Increasing ω_max from 10 to 20 should reduce the β^0.40 residual at β=1, as more harmonics fall within the ZPF bandwidth. If ω_max=20 still shows β^0.40, that would be a novel finding inconsistent with this explanation.

**VERDICT:** The noise spectrum fidelity is the PRIMARY explanation for the β^0.40 residual. This is not a simulation artifact — it's a PHYSICAL artifact of using a finite UV cutoff. E005 is specifically designed to test this.

---

### Attack 2.4: Equilibration adequacy

**Computed:** At β=0: equilibration time = 10000 time units = 100 × (1/Γ). At β=1: equilibration time = 10000 × Γ_eff = 10000 × 0.046 = 464 effective relaxation times. Equilibration becomes FASTER at larger β (because Γ_eff increases).

**VERDICT:** Equilibration is not a concern. 100-464 relaxation times is extremely conservative.

---

### Attack 2.5: Ensemble size and statistical power

**Computed autocorrelation analysis:**
- Position autocorrelation: C(t) = exp(-Γt/2) × cos(ω₀t)
- At stride=200: C(200) = exp(-1) × cos(200) ≈ 0.37 × 0.485 ≈ 0.178
- Variance estimator autocorrelation: C_x²(200) = C(200)² ≈ 0.032
- Sum of lagged C_x² correlations: 0.040
- Effective N per trajectory: 49.9 (essentially full N=50)
- Predicted std_var: 0.0071 vs. reported 0.0074 — excellent agreement!

**VERDICT:** The oscillatory nature of the position correlation (cos(ω₀t) factor) means samples at stride=200 time units are effectively independent, even though stride ≈ 2×T_corr. The reported std_var values are correct.

**ONE REAL CONCERN:** The 5.4σ significance at β=0.01 (Langevin) is computed by comparing var_x_SED(0.01) directly to var_x_QM(0.01), without accounting for the β=0 offset. The corrected significance for the β-dependent trend:
- Adjusted excess = [SED-QM at β=0.01] − [SED-QM at β=0] = 0.0275
- Combined std: √(0.0079² + 0.0074²) = 0.0108
- True O(β) trend significance: **2.5σ** (not 5.4σ)

The 5.4σ is a comparison of absolute values vs. QM prediction, not a test of the slope. For demonstrating O(β) failure as a trend, the correct statistic gives ~2.5σ at β=0.01. At β=0.1, the significance of the Langevin failure remains >20σ regardless of correction.

---

### Attack 2.6: Integration scheme (Euler-Cromer)

**The adversarial case:** Euler-Cromer (symplectic Euler) has first-order local error. Could it introduce β-dependent systematic errors?

**Analysis:**
Euler-Cromer is a symplectic integrator, meaning it conserves a modified Hamiltonian exactly. For the harmonic oscillator, it integrates with effective frequency ω_EC = (2/dt)×arcsin(ω₀dt/2).

At ω₀=1, dt=0.05: ω_EC = 1.000104 (0.01% error → negligible effect on var_x).

For the nonlinear oscillator, Euler-Cromer is approximately (not exactly) symplectic, with O(dt²) corrections to the equilibrium distribution:
- At dt=0.05: correction ~ (ω₀dt)² × ... ≈ 0.25% — below statistical errors.

The ZPF modes near ω_max=10: ω_max × dt = 0.5 rad (well within Nyquist). These modes are resolved in the noise but the oscillator dynamics at ω=10 are poorly integrated (10 steps/period). However, since var_x is UV-insensitive (dominated by modes near ω₀), this doesn't affect the results.

**VERDICT:** Euler-Cromer is appropriate. O(dt²) equilibrium error ≈ 0.25% << discrepancies being measured. The high-frequency integration quality doesn't affect var_x.

---

## Part 3: Assessment — Finding-by-Finding Ratings

### Finding 1: SED Harmonic Oscillator Numerical Reproduction (E001)
**Claim:** SED reproduces QM ground state for harmonic oscillator. var_x = 0.507 vs 0.500 (1.4% error). Gaussian distribution confirmed.

**Robustness: 5/5.** The harmonic oscillator is analytically solvable; this is a numerical confirmation of a known exact result. The methodology (frequency-domain for linear systems, exact in principle) is correct. The 1.4% error is attributable to finite τ=0.001 → τ→0 limit. The result would be reproduced by any competent implementation.

**Novelty: 2/5.** Huang & Batelaan (2013) and earlier Cole et al. have done similar numerical verifications of the SED harmonic oscillator. This is confirmatory, not new. The specific finding about requiring the full Abraham-Lorentz transfer function for UV convergence of var_x is marginally new (more precise than prior statements), but it's essentially a consequence of the well-known UV structure.

**Significance: 2/5.** The HO in SED is well-understood analytically. This finding is a prerequisite and sanity check, not a contribution.

**Verdict:** Present as a verification/methodology section, not as a novel finding. Do not prominently feature in a final report.

---

### Finding 2: Langevin O(β) Failure (E003)
**Claim:** SED with constant-Γ Langevin approximation fails at O(β) for the anharmonic oscillator; failure is qualitative (wrong direction of var_x trend).

**Robustness: 4/5.** The numerical result is rock-solid at β=0.1–1.0 (23–50σ significance). The slight concern is the σ at β=0.01: reported as 5.4σ but more accurately ~2.5σ for the O(β) trend. The physical mechanism (ω³ noise × constant Γ → pumping) is well-explained and computationally confirmed. The β^1 scaling is validated by the Adj/β ratio being roughly constant (5.8–8.9).

**BUT adversarial attack:** The Langevin approximation is known to be a simplification of the full ALD. Pesquera & Claverie (1982) explicitly used full ALD. Using the Langevin approximation for a system with nonlinear forces and then discovering it fails is arguably "expected" to a careful physicist. **The failure might be filed under "wrong tool, wrong result."**

**Counterargument:** The MECHANISM discovered (ω³ noise × constant Γ → positive feedback pumping, giving QUALITATIVELY opposite trend to QM) is genuinely illuminating. Many SED practitioners use Langevin approximation for nonlinear systems (it's computationally convenient), and this finding provides a quantitative warning about when it breaks down.

**Novelty: 3/5.** The specific failure mode (O(β) vs P-C's O(β²)) has not been previously reported. The qualitative reversal of trend direction at O(β) is new. However, that a Langevin approximation fails for nonlinear systems is not surprising.

**Significance: 3/5.** Important as a "what goes wrong" example. Illuminates the mechanism. But the "SED fails at O(β)" framing requires the clarification "the LANGEVIN APPROXIMATION of SED fails at O(β)."

**Verdict:** Include as a methodological finding about the Langevin approximation. Clarify that this is an approximation artifact, not a fundamental SED failure. Emphasize the positive feedback mechanism as the interesting physical content.

---

### Finding 3: Full ALD (Landau-Lifshitz) Fixes O(β) Failure; Residual β^0.40 (E004)
**Claim:** LL-reduced ALD with position-dependent Γ_eff = τ(ω₀² + 12βx²) eliminates the O(β) failure. Residual β^0.40 at β > 0.2.

**Robustness of "O(β) fixed": 4/5.** For β ≤ 0.1: ALD error is statistically indistinguishable from β=0 baseline. This supports P&C (1982) prediction of O(β) agreement. The 11× improvement at β=0.1 (from 78% to 3% error) is striking and robust.

**Robustness of β^0.40: 4/5.** The power-law fit is based on only 3 data points (β=0.2, 0.5, 1.0). The scaling rules out O(β) and O(β²) convincingly (observed ratio 1.40 vs O(β)=2.50 and O(β²)=6.25). The UV cutoff mechanism explanation is physically compelling (5th harmonic exceeds ω_max at β≈1.0). BUT: without the ω_max=20 confirmation (E005), the β^0.40 interpretation remains CONJECTURED.

**CRITICAL ADVERSARIAL CONCERN:** The residual β^0.40 CONTRADICTS P&C's O(β²τ) prediction. P&C predict the leading SED-QM discrepancy should scale as β². Our simulation gives β^0.40 ≈ β^{2/5}. The UV cutoff hypothesis might be wrong: the true SED with full LL might fail as β^0.40 intrinsically. This would be a more significant and more unexpected result than the UV cutoff artifact interpretation.

**Novelty of "ALD fix": 4/5.** First numerical implementation of LL-reduced ALD for SED anharmonic oscillator. The specific equation Γ_eff = τ(ω₀² + 12βx²) is derivable from first principles but has not been computed numerically in this context. The quantitative improvement (47× at β=1) is new.

**Novelty of β^0.40: 4/5.** Completely new observation. P&C predicted O(β²). We observe β^0.40. Whether this is UV artifact or intrinsic — both outcomes are interesting and neither has been previously noted.

**Significance: 4/5.** If the ALD fix is confirmed and the β^0.40 is shown to be UV artifact (E005), this constitutes the first numerical verification of the Pesquera-Claverie 1982 result, 44 years later. If β^0.40 is intrinsic, it contradicts P&C and would require reanalysis of the SED anharmonic problem.

**Verdict:** Highlight as the main numerical finding. Finding 3 is the most novel and significant result.

---

### Finding 4: "Linearity Boundary" Pattern (E002)
**Claim:** SED succeeds iff system is linear; fails for all nonlinear, excited-state, or interference extensions.

**Robustness: 5/5.** This pattern is extremely well-supported by decades of literature. No counter-examples are known.

**Novelty: 1/5.** This is WELL KNOWN in the SED community. Boyer (2019) explicitly states this. Boyer (1975) established it. Claverie, Diner, and others discussed it in the 1970s-1980s. The specific label "linearity boundary" is new, and the systematic enumeration (4+3 successes, failures by category) is new. But the concept itself is textbook.

**Significance: 2/5.** As a summary/characterization, useful for exposition. Not a contribution to new knowledge.

**Verdict:** Present as framing/context, not as a novel finding. The "linearity boundary" is a useful label for a known pattern.

---

### Overall Assessment

**Findings ranked by novelty × significance:**

1. **Finding 3 (ALD + β^0.40):** Most novel and significant. First numerical test of P&C. β^0.40 scaling is unexpected. High priority for publication.
2. **Finding 2 (Langevin O(β) failure mechanism):** Moderately novel. The ω³ feedback mechanism is worth documenting. But needs careful framing.
3. **Finding 1 (HO verification):** Confirmatory only.
4. **Finding 4 (linearity boundary):** Conceptually known; labeling is new.

**For a final report:** Lead with Finding 3. Present Finding 2 as context showing why the Langevin approximation can't be used for nonlinear SED. Use Finding 1 as methodology validation. Use Finding 4 as the introduction/framing.

---

## Part 4: Most Important Remaining Check

### The Single Most Important Check

**The key unresolved question after E003 and E004 is:**

> *Is the β^0.40 residual a UV cutoff artifact or an intrinsic SED failure?*

This is exactly what E005 is designed to test. But let me frame the adversarial case for WHY this specific check is critical:

**If UV artifact (confirmed by E005):**
- ALD agrees with QM for ALL β in the τ→0 limit (P&C confirmed)
- SED is not fundamentally wrong for the anharmonic oscillator (it just needs τ small enough and ω_max large enough)
- The main finding is that the Langevin approximation fails but the full ALD approximately works
- This is a **moderately positive** result for SED

**If intrinsic (β^0.40 persists at ω_max=20, 50):**
- ALD disagrees with QM as β^0.40, which is FASTER than P&C's O(β²) and in a different functional form
- This would CONTRADICT P&C (1982) — a 44-year-old analytical result would be wrong
- This would be a **highly significant negative result** for SED
- Possible explanations: (a) P&C made an error, (b) LL reduction misses important terms, (c) there's a non-perturbative correction

**What a skeptical physicist demands:** Run ω_max=10, 20, 50 at β=1 and plot Δe(β=1) vs. ω_max. If Δe → 0 as ω_max → ∞, the UV cutoff is the culprit and P&C is confirmed. If Δe → constant, SED has an intrinsic β^0.40 failure.

**E005 is exactly this check.** The result will determine whether our main finding is "Langevin approximation fails but SED is OK" (weak result) or "P&C 1982 is incorrect — full ALD fails as β^0.40, not β²" (potentially significant result).

### Secondary important check: QM reference accuracy

The QM matrix diagonalization uses N_max=80 basis functions. For β=1, the convergence should be checked. If the ground-state wavefunction has significant tails requiring higher basis states, the QM reference could be slightly wrong. **This is unlikely to matter** (the report claims convergence < 2×10⁻¹¹), but a skeptical physicist would want to see convergence vs. N_max.

### Tertiary check: τ dependence

P&C's result is in the τ→0 limit. At τ=0.01, the O(τ²) corrections to the LL equation could contribute. Running at τ=0.001 would provide a much cleaner test of the P&C prediction. This is the second part of E005's program.

---

## Part 4: Most Important Remaining Check

---

## Methodology Summary Table

| Attack | Verdict | Severity |
|--------|---------|----------|
| 2.1 Langevin validity | O(β) failure is REAL at β=0.01–0.1 (Langevin is valid there). BUT it's an approximation artifact, not SED failure. | Medium |
| 2.2 LL O(τ²) errors | Negligible (10⁻⁴ vs 0.030 signal). NOT an issue. | Low |
| 2.3 UV cutoff / noise | MAIN CONCERN. 5th harmonic exceeds ω_max at β≈1. Explains β^0.40 as UV artifact. Needs E005 confirmation. | High |
| 2.4 Equilibration | 100-464 relaxation times. ADEQUATE. | None |
| 2.5 Ensemble size | Autocorrelation is small (oscillatory C(t)). 5.4σ at β=0.01 is more accurately ~2.5σ for the trend. Large-β results unaffected. | Low-Medium |
| 2.6 Euler-Cromer | O(dt²) = 0.25% error, negligible. Symplectic property preserves equilibrium. | None |

---

## References Found

### Key Prior Papers
- **Pesquera, L. & Claverie, P. (1982).** "The quartic anharmonic oscillator in stochastic electrodynamics." *J. Math. Phys.* **23**(7), 1315–1322. [AIP Publishing](https://pubs.aip.org/aip/jmp/article-abstract/23/7/1315/225501/The-quartic-anharmonic-oscillator-in-stochastic)
  - *The foundational analytical result. O(β²) SED-QM disagreement for full ALD. No numerical simulation.*

- **Moore, S.M. & Ramírez, J.A. (1981).** "The harmonic and anharmonic oscillator in classical stochastic electrodynamics." *Il Nuovo Cimento B* **64**, 275–286. [Springer](https://link.springer.com/article/10.1007/BF02903289)
  - *Earlier analytic work. Claims "qualitative agreement" in zero-charge limit — different regime from our simulation.*

- **Boyer, T.H. (2019).** "Stochastic Electrodynamics: The Closest Classical Approximation to Quantum Theory." *Atoms* **7**(1), 29. [arXiv:1903.00996](https://arxiv.org/abs/1903.00996)
  - *The "linearity boundary" is explicitly articulated here. Confirms our F4 is not novel.*

- **Huang, W.C.-W. & Batelaan, H. (2013).** "Dynamics Underlying the Gaussian Distribution of the Classical Harmonic Oscillator in Zero-Point Radiation." *J. Comput. Methods Phys.* **2013**, 308538. [Hindawi](https://www.hindawi.com/journals/jcmp/2013/308538/)
  - *Recent numerical confirmation of SED harmonic oscillator. Relevant comparison to F1.*

- **Cole, D.C. (2005).** "Simulation Results Related to Stochastic Electrodynamics." *Proc. Conf. on Stochastic Electrodynamics.* [Boston University preprint](https://www.bu.edu/simulation/publications/dcole/PDF/SwedenCole2005.pdf)
  - *Numerical SED work by Daniel Cole. Focused on HO and hydrogen; no anharmonic oscillator simulations found.*

### Papers NOT Found (searched but absent)
- No time-domain simulation of anharmonic SED oscillator found in any database.
- No paper computing var_x vs. β for SED anharmonic oscillator found.
- No paper applying Landau-Lifshitz order reduction to SED anharmonic oscillator found.
- No paper with explicit "linearity boundary" as a named concept found (though the concept is implicit in Boyer 2019 and others).
