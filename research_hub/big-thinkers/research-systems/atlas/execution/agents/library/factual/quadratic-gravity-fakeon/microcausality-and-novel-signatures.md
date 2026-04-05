---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-003-quadratic-gravity-fakeon-validation
---

# Microcausality Violation and Novel Scattering Signatures

## Microcausality Violation

The fakeon prescription violates microcausality — the commutator [φ(x), φ(y)] ≠ 0 for spacelike separations at distances |x-y| < 1/M₂.

**Key properties:**
- Violation timescale: Δt ~ 1/M₂ (for M₂ ~ M_P: Δt ~ 10⁻⁴³ s, i.e. the Planck time)
- Range extends up to ~6 orders of magnitude above the Planck length (up to ~10⁻²⁹ m), since M₂ could be as low as ~10¹² GeV (consistency bound from inflation: M₂ > M₀/4)
- **Survives the classical limit** — not a purely quantum effect (Anselmi, CQG 2019)
- The "classicized" equations of motion (obtained by integrating out the fakeon) contain **nonlocal terms** that differ from the standard higher-derivative equations

**The violation does NOT propagate to observable scales** (Anselmi & Marino, CQG 2020):
- Does NOT propagate along light cones
- Does NOT propagate via gravitational waves
- The Hubble expansion (positive H₀) actively suppresses propagation of acausal effects
- "The universe even conspires to make the effect disappear"
- The violation is "short range for all practical purposes"

This is perhaps the most distinctive and dramatic prediction of the fakeon theory — it is a qualitative departure from standard QFT where microcausality is an axiom — but it is fundamentally unobservable at any foreseeable experimental scale.

The microcausality violation also has implications for the black hole information paradox — it provides a potential channel for information leakage during Hawking evaporation at rate ~(l_P/r_H)² per emission event. No quantitative calculation of cumulative leakage exists. See `black-hole-predictions.md` for details.

Source: Anselmi & Piva (2018), JHEP 11, 021 (18A3, 18A4); Anselmi & Piva (2019), CQG 37, 095003

## Scattering Cross Sections

**Tree level:** All scattering cross sections involving only gravitons are identical to GR. The fakeon cannot appear as an external state, so graviton-graviton scattering at tree level is mediated by massless graviton exchange only.

**The differences appear at:**

1. **Loop level:** The fakeon contributes to loop diagrams, modifying the running of couplings and loop corrections to cross sections.

2. **High-energy resummation:** Tree-level graviton cross sections grow at high energies (a known problem in GR). In fakeon theory, resummation shows cross sections may **decrease** at high energies — consistent with asymptotic freedom. This predicts **gravity becomes weaker at trans-Planckian energies**.

3. **Near the fakeon mass (E ~ M₂):** The cross section shows the **"missing resonance"** — a smooth cross section with at most a gentle shoulder or dip where a physical particle would produce a Breit-Wigner bump. The fakeon's dressed propagator has no peak (the peak region is "outside the convergence domain" — Anselmi, JHEP 2022). In four-derivative QG+F this manifests as a smooth absence; in the six-derivative Lee-Wick extension, complex-mass poles produce a **"pair of bumps"** from constructive/destructive interference. Both are smoking gun signatures distinguishing fakeon from alternative ghost treatments (e.g., unstable particle interpretation of Donoghue & Menezes).

## Peak Uncertainty (Anselmi 2022, JHEP 06, 058)

The dressed propagator of a fakeon near its mass shell exhibits "peak uncertainty": ΔE ≳ Γ_f/2, where Γ_f is the fakeon width. The Breit-Wigner peak is smeared by an irreducible uncertainty — a fundamental prediction, not an experimental limitation. This means fakeon resonances are intrinsically broader and harder to distinguish from background than normal particle resonances.

## Collider Phenomenology

The "fake doublet" model (Anselmi 21A3, 21A4; JHEP 10 (2021) 132) applies the fakeon concept to the Standard Model. A second scalar doublet (like the Inert Doublet Model) is treated as a fakeon. Observable effects:
- Modified h→γγ decay width (loop contributions from fake doublet)
- Shifted Higgs trilinear coupling
- EW vacuum stabilization
- NO missing energy signature (unlike standard inert doublet)
- Can have mass **below the EW scale** without violating Z-pole constraints

Separately, a fake scalar doublet coupling to the muon can explain the muon g-2 anomaly (arXiv:2104.03249), with sub-EW masses allowed because fakeons evade direct production bounds.

See `standard-model-and-agravity.md` for the full SM connection and agravity program.

## Experimental Accessibility

| Signature | Accessibility | Notes |
|-----------|-------------|-------|
| Direct microcausality violation | Inaccessible | Confined to ~10⁻²⁹ to 10⁻³⁵ m, does NOT propagate |
| Missing resonance / pair of bumps | Inaccessible | Requires ~10¹⁹ GeV (10¹⁵ beyond LHC) |
| Indirect effects on CMB spectra | Possible | Via inflationary perturbation spectra |
| Scalar GW polarization (breathing mode) | Inaccessible | M₀ ~ 10¹³ GeV, not sourced astrophysically |
| GQuEST spacetime fluctuations | Not relevant | Tests holographic physics, not QG+F |
| BMV entanglement | Not discriminating | All QG theories predict entanglement |
| GW ringdown QNMs | Inaccessible | LVK bounds 40 orders too weak |
| Fake doublet at LHC | Possible | Depends on unknown fake doublet mass |

**Priority ranking of experimental tests:**
1. CMB B-mode detection (tensor-to-scalar ratio r) — see inflationary-predictions.md
2. Fake doublet phenomenology at LHC (model-dependent)
3. Everything else is inaccessible — see `experimental-signatures-beyond-cmb.md` for the comprehensive catalog

Sources: Anselmi & Piva (2018), JHEP 11, 021; Anselmi & Marino (2020), CQG; Anselmi (2021), 21A3, 21A4; Anselmi (2022), JHEP 06, 058; arXiv:2506.14695 (June 2025, first LVK ringdown constraints)
