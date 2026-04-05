---
topic: T_U/T_dS model fails CMB 3rd acoustic peak and structure formation — a₀ evolution is catastrophic
confidence: verified
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-008"
---

## Finding

The T_U/T_dS modified inertia model fails CMB and large-scale structure observations through two
independent mechanisms: (1) if a₀ = cH(z)/6 evolves with the Hubble rate, early-universe processes
(CMB, BBN) are thrown into deep MOND — catastrophically disrupting nucleosynthesis and acoustic
oscillations; (2) even with a frozen a₀ = cH₀/6 (no mechanism provided), the model has no dark
matter and predicts the wrong CMB 3rd acoustic peak ratio by ~2×. Neither variant is compatible
with cosmological observations.

## Scenario A: Evolving a₀ = cH(z)/6 — CATASTROPHICALLY RULED OUT [COMPUTED]

The T_U/T_dS formula involves the de Sitter Hubble rate, which naturally evolves with cosmic time.
If a₀ tracks H(z):

| z | H(z)/H₀ | a₀(z) | a₀/a₀(today) |
|---|---------|-------|--------------|
| 0 | 1.0 | 1.09×10⁻¹⁰ m/s² | 1 |
| 1 | 1.78 | 1.94×10⁻¹⁰ | 1.78 |
| 100 | 573 | 6.25×10⁻⁸ | 573 |
| 1100 (recombination) | 2.3×10⁴ | 2.55×10⁻⁶ | 23,000 |
| 10⁹ (BBN) | 9.5×10¹⁵ | ~1 m/s² | 10¹⁵ |

At z = 1100, gravitational acceleration in CMB density perturbations:
- g_CMB ≈ 6.7×10⁻¹¹ m/s²
- a₀(z=1100) ≈ 2.5×10⁻⁶ m/s²
- x = g_CMB/a₀ ≈ 2.6×10⁻⁵ → μ ≈ 2.6×10⁻⁵

All acoustic modes have essentially zero inertial mass: **deep MOND at recombination**.
Acoustic oscillations and structure formation are completely disrupted. **Evolving a₀ is
observationally ruled out.**

## Scenario B: Frozen a₀ = cH₀/6 — FAILS CMB PEAK RATIOS [COMPUTED]

If a₀ is frozen at today's value (no mechanism provided for why H should stop evolving):

    x = g_CMB/a₀ ≈ 0.6   →   μ ≈ 0.52

Acoustic modes are at the Newtonian-MOND transition; not catastrophic, but:

**CMB 3rd acoustic peak suppression:**
- ΛCDM (Ω_DM = 0.27): 3rd/1st acoustic peak ratio ≈ 0.43 (matches Planck 2018 to ~1%)
- Modified inertia (no CDM): 3rd/1st acoustic peak ratio ≈ 0.20 (suppressed by ~2×)

Without dark matter, CDM cannot seed density fluctuations before recombination. CDM provides
the potential wells that enhance odd peaks relative to even peaks in the CMB acoustic spectrum.
The 2× suppression of the 3rd peak is a direct observational signature of missing CDM.

**Structure formation failure:**
1. Acoustic oscillations before z=1100 are purely baryonic (Silk damping scale unchanged)
2. After recombination: no CDM potential wells → baryonic structure formation only
3. Matter power spectrum amplitude and BAO features differ from ΛCDM predictions
4. Galaxy formation is delayed; too-low-amplitude perturbations at all scales

## The Cosmic Coincidence Problem (New Form)

The T_U/T_dS formula naturally gives a₀ = cH/6 where H is the instantaneous Hubble rate.
Fixing a₀ = cH₀/6 (a constant) is:
- Required to avoid Scenario A catastrophe
- But not derived from the formula — requires freezing H at its present value
- Equivalent to saying the de Sitter temperature "remembers" today's H₀ throughout cosmic history

No mechanism within the T_U/T_dS framework explains why H should be frozen. This is the
"coincidence problem" in a new form: why is a₀ tuned to the present-day Hubble rate?

## Verdict

**FAILS cosmological tests** on two independent grounds:
- Evolving a₀: catastrophically ruled out (nuclear BBN + CMB disrupted)
- Frozen a₀: wrong CMB 3rd peak by 2×, no CDM, broken structure formation

Neither variant can be made consistent with Planck CMB data without introducing CDM-like
dark matter, which defeats the purpose of the modified inertia model.

## Relationship to Other Entries

- `mond-phenomenology-coincidences.md` — background on MOND cosmological failures
- `tu-tds-viability-scorecard.md` — full model assessment (CMB scores 1/10)
- `modified-inertia-lensing-falsification.md` — cluster lensing failure (complementary fatal issue)
