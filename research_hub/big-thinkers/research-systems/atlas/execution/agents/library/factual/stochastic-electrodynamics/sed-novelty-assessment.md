---
topic: SED anharmonic oscillator — novelty and robustness assessment (adversarial review)
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-006"
---

## Summary

Finding-by-finding novelty and robustness assessment from adversarial review (E006). Conclusion: **Finding 3 (ALD + β^0.40) is the main novel result** — first numerical test of Pesquera-Claverie 1982. Finding 4 (linearity boundary) is NOT novel — known since Boyer 1975/2019.

## Finding-by-Finding Verdicts

| Finding | Robustness | Novelty | Priority |
|---------|-----------|---------|----------|
| F1: HO numerical confirmation (E001) | 5/5 | 2/5 | Present as verification, not novel finding |
| F2: Langevin O(β) failure mechanism (E003) | 4/5 | 3/5 | Include as methodological finding; careful framing needed |
| F3: ALD LL fix + residual β^0.40 (E004/E005) | 4/5 | 4/5 | LEAD FINDING — most novel and significant |
| F4: "Linearity boundary" pattern (E002) | 5/5 | 1/5 | Present as framing/context, NOT as new discovery |

## Key Framing Corrections from E006

### F2 (Langevin failure): Label as approximation artifact
The O(β) Langevin failure is NOT a fundamental SED failure — it is a failure of the constant-Γ approximation. The full ALD (E004) restores agreement for β ≤ 0.1. Label as: "Langevin approximation of SED fails at O(β); full ALD works to O(β²)." Reporting it as "SED fails at O(β)" is misleading.

### F4 (linearity boundary): Known concept, not novel
The concept that SED succeeds for linear systems only is WELL KNOWN since Boyer (1975) and explicitly articulated in Boyer (2019): "SED gives predictions agreeing with QM for linear systems (Hamiltonians quadratic in positions and momenta), but not for nonlinear systems." Claverie, Diner, and others noted this in the 1970s-1980s.

**What IS new:** The label "linearity boundary," the systematic enumeration (4+3 successes + 6 failure categories), and the specific numerical quantification (threshold β > 0.005). Present as "confirming and quantifying a known pattern," not a new discovery.

## Significance Correction: β=0.01

The 5.4σ reported in E003 for β=0.01 is a comparison of absolute var_x_SED vs. var_x_QM. The correct significance for the O(β) *trend* (slope of excess vs. β):

- Adjusted excess = [SED-QM at β=0.01] − [SED-QM at β=0] = 0.0275
- Combined std: √(0.0079² + 0.0074²) = 0.0108
- True O(β) trend significance: **~2.5σ** (not 5.4σ)

The 5.4σ is not wrong — it accurately reflects the absolute deviation from QM. But for demonstrating O(β) failure as a *trend* (slope), ~2.5σ is the correct figure. At β ≥ 0.1, both metrics agree: failure is >20σ regardless of correction.

## Methodology Robustness Summary

| Attack | Verdict | Severity |
|--------|---------|----------|
| Langevin validity (β=0.01-0.1) | O(β) failure REAL — Langevin IS valid there | Medium (framing issue) |
| LL O(τ²) errors | 10⁻⁴ vs 0.030 signal — negligible | None |
| UV cutoff (5th harmonic) | TESTED by E005 — error only drops 18% at 3× ω_max | Low (artifact explanation REFUTED by E005) |
| Equilibration | 100-464 relaxation times | None |
| Ensemble size / autocorrelation | Oscillatory C(t) → near-independent samples; reported std_var correct | None |
| Euler-Cromer integration | O(dt²) ≈ 0.25% << signal; symplectic for HO | None |

## Key References Found (Novel Search, E006)

No prior time-domain numerical simulation of anharmonic SED oscillator found in any search. Specific searches confirmed absence of:
- var_x vs. β for SED anharmonic oscillator
- LL order reduction applied to SED anharmonic oscillator
- Time-domain Langevin simulation for any anharmonic SED system

### Confirmed Prior Literature

- **Pesquera & Claverie (1982)**, J. Math. Phys. 23(7): O(β²) failure for full ALD (analytical, no numerics). THE foundational result. DOI: 10.1063/1.525501
- **Moore & Ramirez (1981)**, Il Nuovo Cimento B 64:275: Analytic study; "qualitative agreement" in zero-charge (τ→0) limit. DIFFERENT regime — no radiation reaction, no noise pumping. Does NOT contradict E003/E004.
- **Boyer (2019)**, Atoms 7(1):29, arXiv:1903.00996: Explicitly states linearity boundary; CONFIRMS F4 is not novel.
- **Boyer (1975)**, multiple papers: Original identification of SED-QM agreement for linear systems.
- **Huang & Batelaan (2013)**, J. Comput. Methods Phys. 2013:308538 (Hindawi): Numerical SED harmonic oscillator confirmation. Comparable to our F1.
- **Cole (2005)**, Bu.edu preprint: Numerical SED work on HO and hydrogen; no anharmonic simulations.
- SED review arXiv:1205.0916: Theory review, no numerical anharmonic simulations.

### Papers Searched and Not Found
- No paper applying Landau-Lifshitz order reduction to SED anharmonic oscillator.
- No paper computing position variance vs. β for SED in time domain.
- No paper with explicit "linearity boundary" as a named concept.

## Conclusions for Publication Strategy

1. **Lead with F3** (ALD + β^0.40): first numerical verification of P&C 1982, 44 years later
2. **Present F2** as methodological finding: what goes wrong with Langevin approximation for nonlinear SED
3. **Use F1** as methodology/validation section, not a contribution
4. **Use F4** as framing/introduction, explicitly citing Boyer (2019) to acknowledge prior art

Whether the β^0.40 residual is a UV artifact or intrinsic SED behavior — both outcomes are significant and neither has been previously identified.
