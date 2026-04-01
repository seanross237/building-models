# Exploration 006 — Adversarial Review Summary

## Goal
Aggressively challenge four SED novel claims (tunneling formula, Bell S ≤ 2, T_ion measurements, ω³ unification) as a harsh PRL referee would.

## What Was Tried
Web searches for each claim (3-5 searches per claim), PDF downloads and full reading of key papers: Faria-França-Sponchiado (2004), Ibison-Haisch (1996). Searched for Boyer correlator precedent, Marshall-Santos Bell work, Pesquera-Claverie (1982), Nieuwenhuizen (2015), Cole & Zou (2003).

## Outcome: Excellent Success

All four claims assessed with specific papers found. One critical prior art found that undermines the flagship claim.

## Key Takeaway

**The most important finding: Faria, França & Sponchiado (2004), arXiv:quant-ph/0409119 / Foundations of Physics 35 (2005) analytically derived Γ_SED ∝ exp(−ΔU/E_zpf) using Kramers-Chandrasekhar theory.** Their Eq. 40 at T=0 is:
```
κ = (ωa/2π) × exp(−ΔU / [ħωa/2])
```
This is EXACTLY the exponential structure of the E001+E005 "novel" formula. The ratio formulation Γ_SED/Γ_QM = A×exp(S_WKB − V_b/E_zpf) follows trivially by dividing this by the WKB rate. The numerical verification (R²=0.9998 across 7 points) is real but secondary. The core formula was published in 2004.

## Claim Rankings

| Claim | Verdict | Most Damaging Finding |
|-------|---------|----------------------|
| **A** (tunneling formula) | **Marginally Novel** | Faria-França (2004) = exact same exponential structure. Slope=1.049 unexplained. A is UV-sensitive (~50% change with ω_max). |
| **B** (Bell S ≤ 2) | **Not Novel** | (a) SED is classical by construction — S ≤ 2 is a tautology. (b) C_xx(d)=cos(ω₀d/c) is a one-line derivation from Boyer (1975) Eq. 41. (c) Uncoupled QM oscillators ALSO give S ≤ 2, making the QM comparison invalid. |
| **C** (T_ion measurements) | **Partially Novel** | τ is 60× wrong (all timescales unphysical). Only 4 L values. Nieuwenhuizen knew qualitative picture. No fine scan near L_crit. |
| **D** (ω³ unification) | **Partially Novel** | Boyer (1976) and Pesquera-Claverie (1982) have the mechanism in disguise. The NAME and UNIFICATION are new but the mechanism isn't. |

## Leads Worth Pursuing

1. **Immediately fix Claim A citation:** Explicitly differentiate from Faria-França (2004). The S_WKB connection and the numerical verification are the true novelty — not the exponential factor.

2. **Claim B needs complete reframing.** Remove Bell S ≤ 2 — it's trivially true and the QM comparison is wrong. Replace with: "SED produces oscillating ZPF-induced correlations C_xx(d) = cos(ω₀d/c) that are absent in QM for uncoupled oscillators."

3. **Claim C: Rerun with physical τ = 2.6×10⁻⁷.** Without this, no absolute timescale is credible.

4. **Claim D: Connect to Pesquera-Claverie (1982) explicitly and show what is genuinely new** (the unification across three failure modes, not the mechanism itself).

## Unexpected Findings

The Ibison-Haisch (1996) paper (Phys. Rev. A 54, 2737) shows explicitly that the ω³ factor ∫ dω ω³|h(ω)|² appears in computing ZPF-driven oscillator variance (their Eq. 58). This directly connects to Claim D: the ω³ spectrum is the enabling mechanism for SED's success in linear systems and its failure in nonlinear systems. This reference should be cited in support of Claim D.

The Marshall-Santos Springer chapter "Stochastic Electrodynamics and the Bell Inequalities" exists but was not fully accessible. It may contain prior Bell-SED analysis that would further undermine Claim B.

## Computations Identified

None — this was a literature research exploration.

DONE
