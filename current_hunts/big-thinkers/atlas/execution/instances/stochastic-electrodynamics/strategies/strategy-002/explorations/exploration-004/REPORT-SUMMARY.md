# Exploration 004 — Summary: Phase 2 Root Cause Synthesis

## Goal
Synthesize E001-E003 results and evaluate the "ω³ feedback mechanism" as a unifying root cause. Survey SED literature for prior modifications (Boyer, de la Peña-Cetto, Pesquera-Claverie, Santos, Nieuwenhuizen, Claverie-Diner). Assess three proposed fixes (Local FDT, spectral index n<3, dressed particle). Identify which novel claims survive scrutiny.

## What Was Tried
Web literature searches across arXiv, Springer, Frontiers, Semantic Scholar, SciELO. Fetched full content of key papers: Nieuwenhuizen 2020, Faria & Franca 2006, Santos 2022, de la Peña LSED 2005. Ran independent numerical verification of E001's Γ_SED/Γ_WKB formula using WKB integrals for double-well (confirming V_barrier/E_zpf interpretation with local ω_local = √2).

## Outcome: Good Success

**Literature Survey:** All four major proposed modifications found and characterized:
- **Boyer:** No modifications proposed. Maintains standard ω³ and ALD. 1976 paper showed nonlinear oscillators push ZPF toward Rayleigh-Jeans (non-equilibrium) — foundational to the ω³ feedback story.
- **de la Peña-Cetto LSED:** Mode-selection (only resonant modes matter) — NOT position-dependent noise. Explicitly linear response; doesn't fix hydrogen or anharmonic oscillator.
- **Pesquera-Claverie 1982:** Showed radiation balance fails at O(β) — first-order in anharmonicity. The failure is qualitative (not perturbative), not just a small correction. No fix proposed.
- **Santos 2022:** SED = first-order-in-ħ QED approximation; exact only for quadratic Hamiltonians. Elegant diagnostic, no fix.
- **Nieuwenhuizen 2020:** Exhaustively tested 5 renormalization schemes for hydrogen — ALL fail. Self-ionization is fundamental.

**Three Fixes:** None exists in literature for any of them. Fix A (Local FDT) and Fix B (spectral index n<3) are genuinely new concepts, but both are wrong: Fix A worsens anharmonic/hydrogen, Fix B breaks Lorentz invariance. Fix C (dressed particle) is partially in the literature (Cavalleri, Santos SEDS) and exhaustively tested by Nieuwenhuizen — all fail.

## Key Takeaway

**The ω³ feedback mechanism is a correct but previously unnamed unification.** Boyer (1976) established the non-equilibrium; Claverie-Diner (1977) identified the Fokker-Planck failure; Santos (2022) gave the quantum-mechanical framing. But no paper explicitly unified all three failures (anharmonic, double-well, hydrogen) under a single ω³ mechanism. That unified narrative is new.

**The fix space is genuinely bleak.** Nieuwenhuizen's exhaustive 5-scheme result for hydrogen, combined with the Fix A/B analysis, makes a strong case that no simple modification of the ZPF spectrum or coupling can rescue SED for nonlinear systems. Santos' result gives the mathematical reason: the missing ħ-order corrections cannot be recovered by patching the noise term.

## Claim Survival

- **Claim A (Γ formula):** Novel vs. Faria & França (ratio-to-WKB formulation). ~15% systematic underestimate at both λ values. Computation confirms the E_zpf = ħω_local/2 = √2/2 interpretation. Should be tested at 4-5 more λ values before being promoted as a strong result.
- **Claim B (C_xx = cos):** Likely derivable from Boyer's ZPF two-point correlators. The correlation formula may not be novel, but the Bell-CHSH ≤ 2 demonstration is new and publishable.
- **Claim C (T_ion data):** Genuinely new quantitative T_ion(L) measurements. Important caveat: E003's τ is ~60× the physical value; the real T_ion values are ~60× longer. After this rescaling, the results remain consistent with Nieuwenhuizen's long-run pessimism.
- **Claim D (ω³ unification):** Genuinely new synthesis. Not stated anywhere explicitly in the literature. Has good support from Boyer, Claverie-Diner, and Santos as independent pillars.

## Leads Worth Pursuing

1. **Phase 3A (Priority 1):** Test Γ formula at 5 λ values. Can the ~15% prefactor be understood? At what λ does Γ_SED < Γ_QM (formula predicts undershoot)?
2. **Phase 3B:** 3D ZPF correlation computation. The cos(ω₀d/c) result may wash out to zero in 3D multi-mode ZPF, making E002's result a 1D artifact.
3. **Phase 3C:** Santos' ħ-order analysis: do the missing second-order corrections quantitatively predict the 15-18% residual and 18× tunneling overestimate?

## Unexpected Findings

- **ω_local = √2 universality:** In the double-well V(x) = -½x² + ¼λx⁴, the local oscillation frequency at the potential minimum is ALWAYS √2 regardless of λ (when ω₀=1). This means E_zpf_local is a universal constant for this potential family, and the crossover S_WKB = V_barrier/E_zpf for λ=0.25 is a specific tuning (not a general identity).
- **LSED is not a fix — it's a subset:** De la Peña's LSED is explicitly about resonant modes in linear systems. It's been oversold as a route to quantum mechanics for general systems. The LSED-hydrogen "stabilization" claimed by de la Peña (2022) relies on the short-run Cole & Zou (2003) result, which E003 has now falsified.
- **Nelson's SM ≠ SED:** Recent paper (arXiv:2512.16168) on double-well tunneling uses Nelson's stochastic mechanics — a completely different theory that enforces quantum distributions by construction. It is sometimes confused with SED but is not.

## Computations Identified

1. **WKB action as function of λ (simple, 50 lines Python):** Test the Γ_SED/Γ_WKB formula at 5 values of λ. Inputs: Schrödinger equation finite-difference (already done in E001 code). What it tells us: whether the formula has a universal prefactor or breaks down.
2. **3D ZPF correlation integral (medium, 100 lines):** Compute ⟨x₁x₂⟩ for two oscillators in full 3D multi-mode ZPF. Inputs: Boyer's ZPF correlation tensor formula. What it tells us: whether E002's cos(ω₀d/c) survives in 3D or averages to zero.
