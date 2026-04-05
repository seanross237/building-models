# Gravity & Dark Matter Exploration — April 2-3, 2026

## What we set out to do

Starting from the question "why can't light escape a black hole if it has no mass," we 
explored alternative theories of gravity, tested them against known anomalies and existing 
data, and followed the evidence wherever it led. The session evolved into a systematic 
empirical investigation of what produces the "extra gravity" in galaxies attributed to 
dark matter.

---

## Part 1: Alternative Gravity Theories

We generated 7 alternative theories of what gravity fundamentally is, then had agents 
explore the implications of each as if it were 100% true:

| # | Theory | Core idea |
|---|---|---|
| 1 | Dimensional shadow | Mass punctures higher-dimensional membranes; gravity is the lower-D shadow |
| 2 | Superfluid drain | Space is a superfluid flowing into matter; objects are carried by the inflow |
| 3 | Computational error correction | Gravity is the universe's garbage collection, compressing redundant state |
| 4 | Expansion shadow | Empty space expands; matter blocks expansion locally; gravity is the net push |
| 5 | Entanglement residue | Gravity is the macroscopic residue of the universe's entanglement graph |
| 6 | Pure time gradient | Gravity is entirely time dilation; spatial curvature is an illusion |
| 7 | Spin-2 flat spacetime | Spacetime is flat; gravity is a spin-2 field (gravitons) on Minkowski background |

### Critical assessment against existing data

| Theory | Status | Why |
|---|---|---|
| 6. Time gradient | **Likely killed** | Light bending / Shapiro delay require spatial curvature. Conformally flat metric gives half the observed deflection. |
| 3. Computational | **Severely constrained** | MICROSCOPE satellite tested equivalence principle to 10⁻¹⁵. Different "complexity" materials show no gravitational difference. |
| 1. Dimensional shadow | **Constrained** | LIGO waveforms show no frequency-dependent dispersion. GW170817 constrains speed to 10⁻¹⁵. |
| 2. Superfluid drain | **Squeezed** | LIGO waveforms match GR precisely. No nonlinear GW effects detected. |
| 4. Expansion shadow | **Alive** — most testable | Provides physical mechanism for MOND. RAR tightness is suggestive. |
| 5. Entanglement | **Alive** — but unfalsifiable | Elegant framework, dissolves conceptual problems, but no distinguishing predictions with current technology. |
| 7. Spin-2 flat | **Trivially alive** | Mathematically equivalent to GR classically. Only diverges at quantum gravity scales. |

---

## Part 2: Direct Tests of Theory #4 (Expansion Shadow)

### Expansion shielding vs. DESI dark energy data
- **Result: FAILED.** The simplest model (ρ_DE_eff = Λ_bare - α·ρ_m) produces wa > 0 
  for w0 > -1. DESI measures wa < 0. Wrong sign — structural failure.
- The model's w(z) is monotonic; DESI requires a phantom crossing (w going from < -1 to > -1).
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/desi_shielding_analysis.py`
- Key plot: `home-base/research_hub/big-thinkers/research-systems/science-data/w0_wa_parameter_space.png`

### a₀ evolution with redshift
- **Result: Weakly disfavored.** Milgrom (2017) already tested this with 6 galaxies at 
  z ~ 0.9-2.4. Data consistent with constant a₀, does not favor a₀ ∝ H(z).
- Sample too small for definitive conclusion, but the MOND community has looked and not found it.

### Wide binary stars (Gaia)
- **Result: Unresolvable with current data.** Chae claims MOND signal; Banik claims null. 
  Disagreement driven by unresolved triple-star contamination. Needs RV follow-up or Gaia DR4.

---

## Part 3: Additional Theories Explored

### Superfluid dark matter (Berezhiani-Khoury)
- DM particles form superfluid in galaxies → phonon forces reproduce MOND. Normal CDM in clusters.
- **Status: Alive but stressed.** a₀ is tuned not derived. No CMB success. Tensions from 
  Milky Way vertical dynamics, SPARC fitting, Cherenkov constraints, weak lensing.
- Unique prediction: MOND behavior should cut off at a finite superfluid-core boundary.

### Directional Hubble tension
- **Result: Not supported.** Several groups find SN dipoles, but directions don't converge on 
  the CMB anomaly axis (off by ~60-80 degrees). Likely explained by local bulk flows.

### Vacuum lag hypothesis (original theory)
- Proposed vacuum has finite relaxation time τ_vac; lag between expansion and vacuum response 
  produces both dark energy evolution and MOND.
- **Result: FAILED.** Simple relaxation ODE cannot produce phantom crossing. DESI prefers 
  τ → ∞ (= LCDM). a₀ prediction off by factor 55. Dimensional check fatal.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/vacuum-lag/analyze_vacuum_lag.py`

### Step dark energy model
- Tested whether a low-redshift "step" in dark energy beats LCDM.
- **Result: Inconclusive.** Step, wCDM, and CPL all beat LCDM by Δχ² ~ -9 to -19 but can't 
  be distinguished from each other. Needs full Cobaya/CLASS run with Planck likelihoods.

---

## Part 4: Koide Formula Search (Constraint Web Theory)

Tested whether SM fundamental constants show more precise algebraic relations than random 
numbers (prediction of a "constraint web" theory of reality).

- **Result: No excess over chance.** 28 hits at ≤0.1% precision vs. null mean of 30.19. 
  At Koide precision (≤0.01%): 3 hits vs. null mean of 3.00. Koide is isolated, not part 
  of a wider pattern.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/koide-search/koide_search.py`
- Monte Carlo: `home-base/research_hub/big-thinkers/research-systems/science-data/koide-search/output/summary.md`

---

## Part 5: Empirical Characterization of the "Extra Gravity" Mechanism

This is the most substantive outcome of the session. Rather than testing theories, we 
used SPARC data to empirically constrain what the mechanism must look like.

### RAR residuals vs. galaxy properties
- **Result: NULL.** No correlation with morphology, mass, gas fraction, surface brightness, 
  distance, or disk scale length. The residuals are pure noise.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/analyze_sparc_rar.py`

### RAR residuals vs. environment
- **Result: NULL.** Spearman rho = -0.116, p = 0.154. No environmental dependence detected.
  Survives distance control.
- Used Chae et al. 2020 environment metric (e_env) for 153 SPARC galaxies.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/environment/analyze_sparc_environment.py`

### What variable controls the transition?
- **Result: Acceleration wins.** g_bar scatter = 0.1795 dex. Phi_bar = 0.2368 dex (worse). 
  |dg_bar/dr| = 0.2954 dex (much worse). Surface density ties with acceleration but is 
  algebraically identical for disks (correlation = 1.000).
- Potential-dependent and gradient-dependent theories ruled out.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/variable-test/`

### Lensing vs. dynamics
- **Result: They match.** The lensing RAR matches the dynamical RAR at galaxy scales 
  (Mistele et al. 2024). The extra gravity bends light — it's real metric modification, 
  not modified inertia.
- Cluster problem persists: MOND still needs extra mass in clusters.
- Key papers: Mistele et al. 2024 (2310.15248), Mistele et al. 2024 (2406.09685)
- Summary: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/lensing-vs-dynamics/`

### Transition shape
- **Result: Gradual, ~2.91 decades.** Best fit is generalized exponential with free sharpness.
  Sharp phase transition strongly disfavored (ΔBIC = 281.6 vs. standard MOND).
- Deep-MOND slope: 0.683 ± 0.073 (possibly steeper than MOND's predicted 0.5, ~2.5 sigma).
  Needs confirmation with BIG-SPARC.
- Script: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/interpolation-shape/`

### Cluster deficit
- **Result: NOT universal.** Ranges from 0.4 to 5.4 within a single analysis.
- Strongest correlation: **dynamical state**. Relaxed clusters ~0.6, merging clusters ~4.7.
- Neutrinos killed: required mass ~2 eV, KATRIN limit < 0.45 eV. Also wrong spatial profile.
- Report: `home-base/research_hub/big-thinkers/research-systems/science-data/sparc-rar-residuals/cluster-deficit/output/report.md`

---

## The Empirical Profile of the Mechanism

Whatever produces the extra gravity in galaxies has these properties:

| Property | Finding | Confidence |
|---|---|---|
| Controlled by | Local acceleration (not potential, not gradient) | Strong |
| Affects photons? | Yes — modifies spacetime metric | Strong (Mistele et al.) |
| Transition shape | Gradual (~3 decades), not sharp | Strong (ΔBIC = 281) |
| Hidden variables? | None detected (no property or environment correlations) | Strong (163 galaxies) |
| Deep-regime scaling | Possibly g ∝ g_bar^0.68 rather than g_bar^0.5 | Tentative (~2.5 sigma) |
| Works in clusters? | Partially — deficit varies 0.4-5.4x, correlates with dynamical state | Established |
| Dark matter particles? | No detections despite decades of searching | Strong |

---

## What's Ruled Out

- Expansion shielding (wrong sign on DESI wa)
- Vacuum lag (no phantom crossing, wrong a₀ scale)
- Standard neutrinos as cluster fix (KATRIN mass limit, wrong profile)
- Sharp gravitational phase transition (ΔBIC = 281)
- Modified inertia (lensing matches dynamics)
- Potential-dependent gravity (worse scatter than acceleration)
- SM constants showing hidden constraint web (Monte Carlo null)

## What's Still Open

1. **Why is the RAR so tight?** The mechanism is deterministic from baryons with no hidden 
   variables. No theory cleanly explains this.

2. **Why does the cluster deficit depend on dynamical state?** Merging clusters need ~5x more 
   extra gravity than relaxed ones. Is this a measurement artifact (baryons flung to large 
   radii during mergers) or genuine physics?

3. **Is the deep-MOND slope really 0.68?** If confirmed with BIG-SPARC (~4000 galaxies), 
   this would rule out standard MOND's Lagrangian and constrain the mechanism's functional form.

4. **What Lagrangian reproduces all these constraints?** A metric, local, continuous, 
   acceleration-dependent, deterministic modification of gravity that matches the observed 
   interpolating function, bends light correctly, and accounts for the cluster-scale behavior. 
   Writing this down is a theorist's job, but we've given them an unusually tight set of 
   requirements.

---

## File Index

| Path | Contents |
|---|---|
| `big-thinkers/desi_shielding_analysis.py` | Expansion-shielding vs. DESI test |
| `big-thinkers/w0_wa_parameter_space.png` | Key plot: shielding model vs. DESI ellipse |
| `big-thinkers/vacuum-lag/` | Vacuum lag hypothesis analysis |
| `big-thinkers/koide-search/` | SM constant relation search + Monte Carlo |
| `big-thinkers/sparc-rar-residuals/analyze_sparc_rar.py` | RAR residual vs. properties |
| `big-thinkers/sparc-rar-residuals/environment/` | RAR residual vs. environment |
| `big-thinkers/sparc-rar-residuals/variable-test/` | Acceleration vs. potential vs. gradient |
| `big-thinkers/sparc-rar-residuals/lensing-vs-dynamics/` | Lensing RAR vs. dynamical RAR |
| `big-thinkers/sparc-rar-residuals/interpolation-shape/` | Transition shape fitting |
| `big-thinkers/sparc-rar-residuals/cluster-deficit/` | Cluster deficit characterization |
