---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-009-discriminating-predictions (quantum-gravity-2 strategy-003)
---

# Discriminating Predictions: Unified QG+F–AS vs. "Compatible-but-Separate"

Systematic identification and ranking of predictions that discriminate the unified QG+F–AS framework from the null hypothesis that both theories are correct but not unified. **Bottom line: one genuinely discriminating computational prediction (ghost dissolution), one moderate (average continuation), zero near-term experimental discriminators.**

## The Null Hypothesis H₀: "Compatible-but-Separate"

**H₀:** QG+F and AS are both valid descriptions of quantum gravity in their respective regimes — QG+F perturbatively above the Planck scale, AS non-perturbatively around it — but they are NOT manifestations of a single theory. Their compatibility reflects very general consistency constraints, not a shared underlying structure.

Under H₀:
- **Ghost fate:** The spin-2 ghost is QG+F's problem; AS has its own separate mechanism for unitarity. No reason for AS's FRG dynamics to affect the ghost's pole structure.
- **b parameter:** Free, or determined by AS's own internal logic, with no connection to QG+F's C² coupling.
- **Average continuation:** Irrelevant to AS; AS solves its own Wick rotation problem independently (e.g., via Lorentzian AS).
- **Fixed points:** AF and NGFP are separate UV completions. No connecting trajectory needed or expected.

Note: H₀ is simpler (Occam's razor) and makes no prediction that the unified framework contradicts. The unified framework's advantage is explanatory — it explains the compatibility rather than treating it as coincidental — but this only becomes scientific if discriminating predictions are confirmed.

## Discriminator A: Ghost Pole Dissolution in C²-Extended FRG (STRONG)

**The single most discriminating test of the unified framework.**

If QG+F and AS are the same theory, the full non-perturbative graviton propagator (computed via C²-extended FRG) should show the spin-2 ghost pole **dissolving** — either into complex pole towers (Draper et al. 2020) or via mass divergence (Becker et al. 2017). A persistent real ghost pole at negative residue would **kill** the framework.

| Outcome | Unified framework | Compatible-but-separate | Standalone QG+F |
|---------|-------------------|------------------------|-----------------|
| Ghost dissolves into complex towers | **PREDICTED** | Not predicted | Contradicts perturbative ghost |
| Ghost mass → ∞ at NGFP | **PREDICTED** | Not predicted | Contradicts finite ghost mass |
| Ghost persists as real pole | **FALSIFIED** | Compatible | Standard prediction |

**Why this genuinely discriminates:** The "compatible-but-separate" view has no mechanism for the ghost to dissolve — it would require AS dynamics reaching into QG+F's perturbative structure. Only the unified theory predicts this because it identifies the ghost as a *perturbative artifact* of a single underlying theory.

### Current Computational Status

Nobody has done this calculation. The specific computation — reconstructing the transverse-traceless spin-2 sector of the graviton propagator within an (R + R² + C²) FRG truncation — has not been performed. Closest existing work:

- **Knorr & Saueressig (2022, SciPost Phys. 12, 001):** Reconstructed the graviton propagator from Euclidean FRG data. Found the spectral function of the *background* graviton necessarily has negative parts (ghost-like contributions), while the *dynamical* graviton spectral function is positive. But Einstein-Hilbert truncation only — no C² term.
- **Draper, Knorr, Ripken & Saueressig (2020, PRL 125, 181301):** Complex pole towers from form-factor ansatz. Not Stelle's ghost specifically.
- **Antoniou, Gualtieri & Pani (2024, arXiv:2412.15037):** Perturbative QNMs of Schwarzschild in quadratic gravity — new classes from massive spin-2 modes. Does not address non-perturbative fate.
- **Platania & Wetterich (2020, PLB 811, 135911):** Conceptual "fictitious ghost" argument. Not carried out for spin-2 case.

### Feasibility

Requires: (1) FRG flow equations for (R + R² + C²) truncation (partially available: Falls et al. 2023, SWY 2022), (2) momentum-dependent form factors in spin-2 sector (methodology from Knorr-Saueressig 2022), (3) spectral reconstruction Euclidean → Lorentzian (methodology from Bonanno et al. 2022).

**Estimated difficulty:** PhD-thesis-level computation. 1–2 years for an expert group (Knorr, Saueressig, or Platania groups). No fundamental obstruction.

**Amplitude equivalence test (sharpest criterion):** The true discriminating question is NOT "does the ghost dissolve?" but "does the ghost dissolve IN A WAY CONSISTENT WITH THE FAKEON PRESCRIPTION?" Specifically: do scattering amplitudes from the complex pole tower equal amplitudes from ghost-pole averaging (fakeon) at tree level? If yes → unification supported. If no → unification refuted. Complex poles alone could emerge for non-unified reasons (any non-perturbative completion generates form factors). See `./ghost-propagator-prediction.md` for the full quantitative specification.

**Honest assessment:** This is a well-specified consistency check, not a sharp discriminating prediction. It can **refute** unification but cannot **uniquely confirm** it.

**Verdict: STRONGLY DISCRIMINATING. Computationally testable. Not yet performed.**

## Discriminator B: Fakeon Average Continuation Applied to FRG (MODERATE)

If unified, Anselmi's average continuation is the correct Euclidean→Lorentzian extraction method for AS calculations. No one has tried this.

| Outcome | Unified framework | Compatible-but-separate |
|---------|-------------------|------------------------|
| Average continuation produces well-defined Lorentzian physics from Euclidean FRG | **PREDICTED** — framework's raison d'être | Not predicted — no reason to use QG+F's prescription in AS |
| Standard Wick rotation works (via Lorentzian AS) | Prediction unnecessary | Default expectation |
| No consistent continuation exists | Both in trouble | Both in trouble |

**Key new reference:** Baldazzi, D'Angelo, Knorr (2025, PRD 111, 106007; arXiv:2501.03752) — "Foliated Asymptotically Safe Gravity" shows Euclidean and Lorentzian FRG flows agree when using analytic continuation of the lapse function. The Lorentzian two-point function has the causal structure of the **Feynman propagator** (NOT the fakeon/average continuation). This is a positive development for Lorentzian AS but does NOT use the fakeon prescription.

**Risk of being rendered moot:** If Lorentzian AS (D'Angelo et al. 2024; Baldazzi et al. 2025) works perfectly without the average continuation, then the unified framework's prediction becomes unnecessary. This is a live research question.

**Estimated difficulty:** 6–12 months for an expert. Conceptually straightforward, technically novel.

**Verdict: MODERATELY DISCRIMINATING. May be rendered moot by Lorentzian AS progress.**

## Discriminator C: Coupling Unification at Planck Scale (WEAK)

If unified, QG+F's couplings (α_R², α_C²) at the Planck scale must match AS's NGFP fixed-point values. Under H₀, the couplings are independent.

**Assessment:** This is a consistency check, not a prediction. A match could be explained by H₀ — both theories correct, so of course they agree where applicable. A mismatch would tension (but not necessarily falsify) the unified framework. **Not genuinely discriminating.**

## Near-Term Experimental Prospects (Before 2030)

**Verdict: NO discriminating experimental prediction before 2030.** The physics lives at the Planck scale; all near-term observations probe 15+ orders of magnitude too low.

| Observable | Status | Discrimination value |
|-----------|--------|---------------------|
| Massive spin-2 QNMs (LIGO/Virgo) | QNM frequencies ~ M_P ~ 10⁴³ Hz; corrections suppressed by (M_P/M_BH)² ~ 10⁻⁷⁶ | **None** |
| CMB tensor-to-scalar ratio (BICEP 2027-28) | σ(r) ~ 0.003; unified predicts r ~ 0.003 at detection threshold | **Not clean** |
| n_s tension (CMB+DESI) | Unified offers resolution (NGFP b or R³) but so does standalone AS | **Not unique** |
| GW waveforms (LIGO O4/O5) | Higher-derivative corrections suppressed by 10⁻⁷⁶ | **None** |

**QNM suppression prediction (specific to unification):** If ghost is confined (unified theory), massive spin-2 QNMs should be **absent or suppressed** for astrophysical BHs. But both unified and standalone QG+F agree these modes are unobservable (mass ~ M_P, too heavy). Only Planck-mass BHs would show the difference.

## Overall Falsifiability Verdict

**The unified QG+F–AS framework is falsifiable in principle but not in practice within 5 years.** Its falsifiability rests entirely on computational tests — specifically the ghost propagator computation — not on near-term experiments.

### What Would Make the Framework More Falsifiable

1. **Compute the AF→NGFP trajectory.** If it exists, extract b and predict specific r. If measured by LiteBIRD (~2037), gains an experimental test.
2. **Compute the ghost confinement scale.** If Λ_ghost = M_P from dynamics (not by hand), non-trivial consistency check.
3. **Find a matter-sector prediction.** Shaposhnikov-Wetterich Higgs mass (m_H ~ 126 GeV) could discriminate if it requires fakeon prescription — not yet investigated.

### Honest Bottom Line

The framework is a well-formed scientific conjecture with one genuinely discriminating computational prediction (ghost dissolution) and several weaker consistency checks. It is not currently experimentally falsifiable. Its scientific status depends entirely on whether the ghost propagator computation is performed. Until then: a conjecture — not wrong, not right, not testable in practice.

Cross-references: `../../asymptotic-safety/ghost-fate-strong-coupling.md` (ghost fate survey), `../qgf-vs-as-analyticity-compatibility.md` (analyticity compatibility), `./open-problems.md` (prioritized open problems), `./novel-predictions.md` (7 novel predictions)

Sources: Knorr & Saueressig (2022, SciPost Phys. 12, 001); Draper et al. (2020, PRL 125, 181301); Antoniou, Gualtieri & Pani (2024, arXiv:2412.15037); Platania & Wetterich (2020, PLB 811, 135911); Baldazzi, D'Angelo, Knorr (2025, PRD 111, 106007); D'Angelo et al. (2024, PRD 109, 066012); Bonanno & Platania (2015, 2018); exploration-009-discriminating-predictions
