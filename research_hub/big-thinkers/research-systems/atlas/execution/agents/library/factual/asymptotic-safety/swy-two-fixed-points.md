---
topic: asymptotic-safety
confidence: verified
date: 2026-03-24
source: exploration-001-escape-routes-survey (strategy-002)
---

# Sen-Wetterich-Yamada Result: Two Distinct Fixed Points in Quadratic Gravity

## The Discovery

Sen, Wetterich, and Yamada (SWY, 2022) computed non-perturbative flow equations for fourth-order derivative gravity (the full quadratic truncation: R^2 + C^2 + E + R + Lambda, where E is the Euler density). They found **two distinct fixed points**:

1. **Asymptotically free (AF) fixed point** — corresponding to perturbative higher-derivative gravity (Stelle theory / QG+F)
2. **Asymptotically safe (NGFP) fixed point** — the non-Gaussian fixed point extending the Einstein-Hilbert NGFP to the full quadratic truncation

These are distinct fixed points with different critical exponents, different numbers of relevant directions, and different physical predictions along the RG trajectories flowing from them.

## SWY Follow-up: Scaling Solutions (2023)

Sen, Wetterich, and Yamada (JHEP 02 (2023) 054) computed **scaling solutions** connecting the AF UV fixed point to the non-perturbative IR region. These show that the AF fixed point can produce viable low-energy physics (Einstein gravity in the IR) via its own trajectory, independent of the NGFP. "If the proposed scaling solution is confirmed beyond our approximations, asymptotic freedom is a viable alternative to asymptotic safety for quantum gravity."

For the broader question of whether AF and NGFP are the same or distinct fixed points, including evidence from Codello-Percacci (2006), Niedermaier (2009), Ohta-Percacci (2014), and Falls et al. (2023), see `af-ngfp-fixed-point-connection.md`.

## Implications for the AS-QG+F Relationship

The SWY result creates genuine ambiguity about which fixed point Nature selects. In the IR, both flow toward Einstein gravity plus small corrections. But they differ in:
- UV behavior and predictions
- Number of free parameters (relevant directions)
- Physical predictions along the RG trajectory

**The SINGLETON risk:** There is a real danger that both fixed points — and indeed all AS and QG+F analyses — ultimately describe the same physical theory viewed from different computational perspectives. Supporting evidence:
- QQG (quantum quadratic gravity) has been shown to "feature a UV fixed point even in the presence of realistic matter sectors, and can therefore be regarded as a concrete realization of asymptotic safety"
- The IR limit "entails only unobservably small modifications of Einstein gravity" for both
- But this convergence is NOT proven — the two fixed points have genuinely different physics

**What could differentiate them:**
- Different predictions for scattering amplitudes at E ~ M_2
- Different matter content effects on the fixed point structure
- Different cosmological predictions (early universe physics)

## d_s = 2 Robustness

A critical finding across all truncations: d_s = 2 is **robust** because it depends only on eta_N = -2, which is a universal property of the NGFP. The specific action varies with truncation, but the spectral dimension prediction does not. Evidence:

- Einstein-Hilbert truncation (R + Lambda): NGFP with eta_N ~ -2, d_s = 2
- R^2 truncation: NGFP persists, d_s = 2
- f(R) truncations (polynomial approximations): NGFP persists
- Weyl-squared truncation (C^2): Opens connection to Stelle theory
- Full fourth-order truncation: SWY two fixed points, both consistent with d_s = 2

However, the physical predictions at accessible energies DO depend on which trajectory and which fixed point — this is where truncations yield different physics.

## Swampland Tension (2025)

A conceptual assessment (Bonanno et al., SciPost Physics, 2025) examined the tension between AS and Swampland conjectures:
- AS graviton scattering amplitudes may violate positivity bounds assumed in the Swampland program
- If AS is realized, some Swampland conjectures (particularly regarding de Sitter vacua) may need modification
- This could *differentiate* AS from string theory: if de Sitter vacua are allowed in AS but forbidden by string Swampland conjectures, this is potentially testable

## QG+F as Perturbative Sector of AS?

Exploration 007 provides a detailed analysis of the QG+F-AS relationship. The most likely answer:

**QG+F is the perturbative sector of a larger theory whose non-perturbative sector includes AS.** The perturbative sector (QG+F) gives the correct S-matrix at energies well above M_P. The non-perturbative sector (AS) gives additional predictions for:
- Strong-field regimes (black hole interiors, very early universe)
- Cosmological scales (vacuum condensate effects)
- The full spectrum (remnants, bound states if they exist)
- UV boundary conditions for matter couplings (Higgs mass)

This interpretation is supported by the QCD analogy (see `quadratic-gravity-fakeon/qcd-analogy-ghost-confinement.md`): just as perturbative QCD gives the correct S-matrix at high energies while confinement is a non-perturbative effect, QG+F gives the perturbative predictions while ghost confinement/singularity resolution are non-perturbative effects captured by AS.

However, **this remains unproven**. The two fixed points (AF and NGFP) may describe genuinely distinct theories with different physical predictions.

## Most Promising Sub-Directions

- AS with specific matter content producing predictions distinct from QG+F
- Lorentzian AS (formulated directly in Lorentzian signature, avoiding Wick rotation issues)
- Bimetric AS with genuinely new operators having no single-metric counterpart (see `bmeg/`)
- AS theories in a different universality class than QQG (if they exist)
- Using the Swampland tension as a discriminator between AS and string-based approaches
