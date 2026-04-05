---
topic: quadratic-gravity-fakeon
confidence: provisional
date: 2026-03-25
source: exploration-010-IHO-CMB-predictions (strategy-002)
---

# The IHO Ghost Interpretation (arXiv:2603.07150, March 2026)

## Paper Identity

**Title:** "Quantum (quadratic) gravity: replacing the massive tensor ghost with an inverted harmonic oscillator-like instability"
**Authors:** K. Sravan Kumar, Joao Marto
**Date:** March 7, 2026
**Framework:** Direct-Sum Quantum Field Theory (DQFT)

## The IHO Mechanism

The central claim: the massive spin-2 ghost in quadratic gravity (from the C² term) can be reinterpreted not as a ghost but as an **inverted harmonic oscillator (IHO)-like instability.**

| Mode Type | Hamiltonian | Behavior | Particle? |
|-----------|------------|----------|-----------|
| Ghost | H = -ω/2(p² + q²) | Negative definite, unbounded below | Yes (negative norm) |
| IHO | H = ω/2(p² - q²) | Indefinite but Hermitian | No — hyperbolic evolution |
| Dual IHO | H = ω/2(-p² + q²) | Indefinite but Hermitian | No — the actual spin-2 mode |

By flipping the sign of the C² coefficient, the ghost mode becomes:
- **Hyperbolic (exponential) evolution** instead of oscillatory
- **Spacelike momentum support** (k² > 0) — cannot go on-shell as a particle
- **No asymptotic particle interpretation** — contributes only virtually

Quantized within DQFT using **geometric superselection sectors**: phase space splits into four regions related by discrete PT symmetries. Hilbert space decomposes as H = H_(+E) ⊕ H_(-E). Sectors related by time-reversal have opposite commutation relations.

## Comparison to the Fakeon Prescription

| Feature | Fakeon (Anselmi) | IHO/DQFT (Sravan Kumar) |
|---------|-----------------|------------------------|
| Ghost treatment | Modified Feynman prescription (no -iε) | Structural reinterpretation of the mode |
| Mechanism | Kinematic: ghost projected out of spectrum | Dynamic: mode has no particle interpretation |
| Unitarity | Proven perturbatively to all loop orders | Argued via geometric superselection |
| Ghost appears as | "Purely virtual particle" | "IHO-like instability" |
| Hamiltonian | Not modified | Modified sign structure |
| Particle content | Ghost removed by prescription | No ghost to begin with |
| Status | Well-established (>150 citations/yr) | New proposal (March 2026) |

**Key difference:** The fakeon keeps the standard action but modifies the quantization prescription. The IHO/DQFT modifies the interpretation of the mode itself — not a ghost at all, but a healthy IHO instability. These are **competing interpretations**, not compatible frameworks.

## CMB Anomaly Connection

The paper builds on "Direct-Sum Inflation" (DSI), claiming to explain three longstanding CMB anomalies:

1. **Parity asymmetry** — Unequal power in even vs. odd multipoles at large angular scales
2. **Low quadrupole moment** — Suppressed ℓ=2 power relative to ΛCDM
3. **Hemispherical power asymmetry** — Power dipole favoring one sky hemisphere

### The 650× Statistical Claim

Bayesian evidence ratio comparing DSI to standard inflation:

    B = P(data|DSI) / P(data|ΛCDM) ≈ 50-650

depending on which statistics are combined. Uses Planck 2018 temperature and polarization data.

**Critical assessment of the 650× claim:**
- Computed using P(M|D) rather than the standard P(D|M)
- Range 50-650× depends heavily on which anomaly statistics are combined
- No independent group has reproduced this analysis
- Underlying anomalies are individually at ~2-3σ (not overwhelming)
- Bayesian framework choice (prior-dependent) introduces model-selection ambiguity

### Predictions

- Modified tensor-to-scalar ratio relative to pure Starobinsky
- Parity-odd oscillations in tensor power spectrum at large scales
- No extra propagating degrees of freedom in CMB or primordial GWs
- Large-scale correlations in primordial gravitational waves
- **No explicit numerical predictions** for n_s, r, or other standard observables provided

## Unitarity Assessment

The unitarity argument:
1. IHO mode has spacelike momentum support → cannot go on-shell
2. Optical theorem excludes spacelike momentum contributions
3. Geometric superselection ensures pure states → pure states
4. Asymptotic spectrum: only massless graviton and scalaron

**Assessment:** Argued constructively, not proven via theorem. Physically plausible but not subjected to the same scrutiny as the fakeon unitarity proofs (perturbatively rigorous to all loop orders).

## Riemann Zeta Connection

The IHO quantization connects to the Riemann zeta function via Berry-Keating:

    N(E) = (|E|/2πℏ)[ln(|E|/2πℏ) - 1] + 7/8

which matches the Riemann zero density. Mathematically interesting but physically speculative.

## Critical Assessment

**Strengths:**
- Addresses a genuine problem with a novel approach
- Mathematically coherent (Hermitian Hamiltonian, unitary evolution within sectors)
- CMB parity asymmetry connection is observationally motivated
- DQFT framework developed over several papers

**Weaknesses:**
- **The sign flip is ad hoc** — changing the C² sign changes the theory
- **Competing with well-established fakeon approach** with all-orders unitarity proof
- **650× Bayes factor is not robust** — depends on methodology choices
- **No independent verification** — only the authors' group has developed DQFT
- **Geometric superselection sectors are exotic** — "two arrows of time" is radical without strong motivation
- **No quantitative predictions** for standard observables (n_s, r)

**Verdict: INTERESTING BUT NOT YET CREDIBLE AS A BREAKTHROUGH.** The fakeon approach remains more robust and better established. Would need: independent verification, explicit numerical predictions, all-orders unitarity proof, and justification for the C² sign flip.

## Relationship to Other QG+F Ghost Treatments

- **Fakeon (Anselmi):** Most established — perturbative unitarity proven, yields QG+F
- **Ghost confinement (Holdom-Ren):** Non-perturbative analogy with QCD — fakeon as perturbative shadow
- **IHO/DQFT (Sravan Kumar):** Alternative interpretation — no ghost at all, just IHO instability
- **Mass gap (arXiv:2501.16445):** Dyson-Schwinger approach — ghost suppressed dynamically

See `qcd-analogy-ghost-confinement.md` for the full ghost treatment landscape.

Sources: arXiv:2603.07150 (Sravan Kumar & Marto, March 2026); Kubo-Kugo (2023); Anselmi-Modesto (2025)
