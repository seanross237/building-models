# Real Data Sources for Physics Validation

Publicly available datasets that research agents can download and analyze. These are the same datasets professional physicists use. Start small, validate your pipeline against published results, then look for new physics.

---

## Gravitational Waves (LIGO/Virgo/KAGRA)

| | |
|---|---|
| **Source** | Gravitational Wave Open Science Center |
| **URL** | https://gwosc.org/data/ |
| **Format** | HDF5 files, 4096 Hz or 16384 Hz sampling rate |
| **Python packages** | `gwosc`, `gwpy`, `pycbc`, `bilby` |
| **Install** | `pip install gwosc gwpy pycbc` |

### What's Available

- Raw strain data from LIGO Hanford (H1), LIGO Livingston (L1), Virgo (V1)
- 32-second segments around confirmed events (quick analysis)
- 4096-second segments for rigorous noise characterization
- Full observing run data (O1, O2, O3)
- Event catalogs: GWTC-1, GWTC-2, GWTC-3 (~90 confirmed events)

### Key Events for Analysis

| Event | Type | Why It Matters | Year |
|-------|------|----------------|------|
| GW150914 | Binary black hole | First detection. High SNR. Best for pipeline validation. | 2015 |
| GW151226 | Binary black hole | Lower mass, longer signal. Tests waveform models. | 2015 |
| GW170817 | Binary neutron star | EM counterpart (GRB 170817A). Constrains c_gw = c. | 2017 |
| GW190521 | Intermediate-mass BH | Heaviest merger. Tests strong-field gravity. | 2019 |
| GW190814 | Asymmetric merger | Contains object in mass gap (2.6 M_sun). | 2019 |

### What an Agent Can Do

**In one session (~1 hour):**
- Download 32-second segment around GW150914
- Apply band-pass filtering (35-350 Hz) and whitening
- Compute the spectrogram, see the chirp signal
- Match-filter against a GR waveform template
- Extract basic parameters (chirp mass, SNR)

**In a longer session (~4 hours):**
- Run full parameter estimation using `bilby` or `pycbc`
- Compare a modified-gravity waveform prediction against data
- Compute Bayes factors for GR vs. modified gravity
- Analyze multiple events for consistency

**For our theories:**
- Compare predicted gravitational waveforms against observed data
- Test if modified dispersion relations are consistent with observed chirps
- Check graviton mass bounds using the phase evolution
- Verify gravitational wave speed using GW170817 + GRB 170817A timing

### Quick Start Code

```python
from gwosc.datasets import event_gps
from gwpy.timeseries import TimeSeries

# Download GW150914 data (32 seconds around the event)
gps = event_gps('GW150914')
h1_data = TimeSeries.fetch_open_data('H1', gps - 16, gps + 16)
l1_data = TimeSeries.fetch_open_data('L1', gps - 16, gps + 16)

# Band-pass filter and whiten
h1_bp = h1_data.bandpass(35, 350).whiten()
l1_bp = l1_data.bandpass(35, 350).whiten()

# Plot the spectrogram
h1_bp.q_transform().plot()
```

---

## Cosmic Microwave Background (Planck)

| | |
|---|---|
| **Source** | Planck Legacy Archive |
| **URL** | https://pla.esac.esa.int/ |
| **Format** | FITS files (HEALPix maps), ASCII tables (power spectra) |
| **Python packages** | `healpy`, `astropy`, `camb`, `cobaya` |
| **Install** | `pip install healpy astropy camb` |

### What's Available

- Full-sky temperature and polarization maps (multiple frequencies)
- Angular power spectra: TT, EE, TE, BB, and lensing
- Best-fit cosmological parameters
- Likelihood code for parameter estimation
- Component-separated maps (CMB, dust, synchrotron, etc.)

### Key Data Products

| Product | What It Is | Use For |
|---------|------------|---------|
| COM_PowerSpect_CMB-TT-full_R3.01.txt | Temperature power spectrum | Testing inflationary predictions |
| COM_PowerSpect_CMB-EE-full_R3.01.txt | E-mode polarization spectrum | Testing polarization predictions |
| COM_CMB_IQU-commander_2048_R3.00_full.fits | CMB map (Commander) | Full-sky analysis |
| COM_Lensing_4096_R3.00 | Lensing potential map | Testing gravity at large scales |

### What an Agent Can Do

**In one session:**
- Download the TT power spectrum data
- Compare against a theoretical prediction from CAMB
- Fit basic cosmological parameters (H_0, Omega_m, n_s)
- Plot residuals to look for anomalies

**For our theories:**
- If the theory predicts modified primordial power spectrum, compare against TT data
- Check if tensor-to-scalar ratio prediction is consistent with r < 0.036
- Look for spectral dimension signatures in CMB at high multipoles
- Test modified gravity effects on the lensing spectrum

### Quick Start Code

```python
import healpy as hp
import camb
import numpy as np

# Generate theoretical CMB spectrum for comparison
pars = camb.set_params(H0=67.4, ombh2=0.0224, omch2=0.120,
                        ns=0.965, As=2.1e-9, tau=0.054)
results = camb.get_results(pars)
powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
totCL = powers['total']  # TT, EE, BB, TE columns

# Load Planck data for comparison
# Download from: https://pla.esac.esa.int/
# planck_tt = np.loadtxt('COM_PowerSpect_CMB-TT-full_R3.01.txt')
```

---

## Causal Dynamical Triangulations (CDT)

| | |
|---|---|
| **Source** | Published papers (Ambjorn, Jurkiewicz, Loll groups) |
| **URL** | arXiv papers (no public raw data repository) |
| **Format** | Published tables and figures |
| **Relevant for** | Spectral dimension running, Hausdorff dimension |

### Key Published Results

| Result | Value | Reference |
|--------|-------|-----------|
| Spectral dimension (UV) | d_s = 1.80 +/- 0.25 | Ambjorn, Jurkiewicz, Loll (2005), hep-th/0505113 |
| Spectral dimension (IR) | d_s = 4.02 +/- 0.1 | Same |
| Hausdorff dimension (IR) | d_H ~ 4 | Same |
| de Sitter-like behavior | Volume profile matches S^4 | Ambjorn et al. (2004), hep-th/0404156 |
| Phase diagram | Phases A, B, C_b, C_dS | Ambjorn et al. (2012), arXiv:1205.3791 |

### What an Agent Can Do

- Extract the spectral dimension curve from published figures/data
- Compare your theory's spectral dimension prediction against CDT results
- The key curve to match: d_s as a function of diffusion time sigma, going from ~2 (small sigma) to ~4 (large sigma)
- This is a benchmark, not experimental data — but it's a strong consistency check across multiple QG approaches

### Writing Your Own CDT Code

CDT simulations are computationally intensive but conceptually straightforward:
- Triangulate spacetime with simplices
- Weight configurations by the Regge action
- Use Markov chain Monte Carlo to sample
- Measure observables (spectral dimension, volume profiles)
- Typical simulation: 10^5-10^6 simplices, O(10^6) MC sweeps
- Reference implementation ideas: Ambjorn et al. review, arXiv:1203.3591

---

## Particle Physics (PDG)

| | |
|---|---|
| **Source** | Particle Data Group |
| **URL** | https://pdg.lbl.gov/ |
| **API** | https://pdgapi.lbl.gov/ |
| **Format** | Web tables, PDF, machine-readable files |
| **Python packages** | `particle` (PyPI), or direct API access |
| **Install** | `pip install particle` |

### What's Available

- Every measured particle property: masses, widths, lifetimes, branching ratios
- Coupling constants at various scales
- Review articles on major physics topics
- Updated annually

### Quick Start Code

```python
from particle import Particle

# Look up particle properties
higgs = Particle.from_name('H(125)')
print(f"Higgs mass: {higgs.mass} MeV")

top = Particle.from_name('t')
print(f"Top quark mass: {top.mass} MeV")

# All known particles
for p in Particle.findall():
    if p.mass and p.mass > 1e5:  # > 100 GeV
        print(f"{p.name}: {p.mass} MeV")
```

---

## Cosmological Surveys

### DESI (Dark Energy Spectroscopic Instrument)

| | |
|---|---|
| **URL** | https://data.desi.lbl.gov/ |
| **What** | Baryon acoustic oscillation measurements, galaxy redshift surveys |
| **Format** | FITS catalogs, power spectra |
| **Key result** | First evidence for evolving dark energy (w != -1), 2024 |
| **Relevance** | If your theory predicts w(z) != -1, compare against DESI BAO data |

### DES (Dark Energy Survey)

| | |
|---|---|
| **URL** | https://des.ncsa.illinois.edu/releases |
| **What** | Weak lensing, galaxy clustering, supernovae |
| **Format** | FITS catalogs |
| **Relevance** | Tests gravity at cosmological scales through lensing/clustering comparison |

### Sloan Digital Sky Survey (SDSS)

| | |
|---|---|
| **URL** | https://www.sdss.org/dr18/ |
| **What** | Galaxy spectra, redshifts, BAO measurements |
| **Format** | FITS files, CSV catalogs |
| **Relevance** | Large-scale structure power spectrum, BAO scale |

---

## Gravitational Tests

### Lunar Laser Ranging

| | |
|---|---|
| **URL** | https://www.lpi.usra.edu/lunar/missions/apollo/apollo_11/experiments/lrr/ (background) |
| **Data** | ILRS (International Laser Ranging Service): https://ilrs.gsfc.nasa.gov/ |
| **What** | Earth-Moon distance measured to ~mm precision |
| **Tests** | Equivalence principle (Nordtvedt effect), PPN parameters, time variation of G |
| **Key result** | |gamma - 1| < 10^-5, |dG/dt|/G < 10^-13 /yr |

### MICROSCOPE Satellite

| | |
|---|---|
| **URL** | https://microscope.onera.fr/ |
| **Data** | Published final results (2022): arXiv:2209.15487 |
| **What** | Test of weak equivalence principle in space |
| **Key result** | Eotvos parameter eta(Ti, Pt) = [-1.5 +/- 2.3 (stat) +/- 1.5 (syst)] x 10^-15 |
| **Relevance** | Tightest bound on EP violation. Any theory with composition-dependent gravity must satisfy this. |

### Cassini Spacecraft

| | |
|---|---|
| **Data** | Published results: Bertotti, Iess, Tortora (2003) |
| **What** | Shapiro time delay measurement |
| **Key result** | gamma_PPN = 1 + (2.1 +/- 2.3) x 10^-5 |
| **Relevance** | Tightest bound on PPN gamma parameter. Tests the spatial curvature produced by mass. |

### Event Horizon Telescope (EHT)

| | |
|---|---|
| **URL** | https://eventhorizontelescope.org/for-astronomers/data |
| **What** | Black hole shadow images (M87*, Sgr A*) |
| **Format** | FITS visibility data, reconstructed images |
| **Python packages** | `ehtim` |
| **Relevance** | Shadow size and shape test strong-field gravity. Deviations from Kerr metric would show up here. |

---

## Lorentz Violation Data Tables

| | |
|---|---|
| **Source** | Kostelecky & Russell |
| **URL** | https://lorentz.sitehost.iu.edu/kostelecky/datatables/ |
| **arXiv** | 0801.0287 (updated annually) |
| **What** | Comprehensive tables of all experimental bounds on Lorentz and CPT violation |
| **Format** | PDF tables organized by particle sector (photon, electron, proton, neutron, gravity, etc.) |
| **Relevance** | If your theory breaks Lorentz invariance in any sector, these tables tell you the bound |

---

## How to Use Real Data

### General Principles

1. **Start with the smallest dataset.** Use 32-second LIGO segments, not full observing runs. Use the Planck power spectrum table, not the full-sky maps. Get your pipeline working on small data first.

2. **Validate against published results first.** Before looking for new physics, reproduce the standard result. If you can't match the published analysis of GW150914, your pipeline has a bug — don't conclude you've found new physics.

3. **Use established packages.** Don't write your own FFT or matched filter from scratch. Use `gwpy`, `pycbc`, `healpy`, `camb`, etc. These have been tested by hundreds of physicists.

4. **Document your pipeline.** Write down every step: data download, preprocessing, filtering, analysis, result extraction. Another agent (or your future self) needs to reproduce this.

5. **Be honest about uncertainties.** Noise is real. Systematics are real. If your result is 1-sigma away from GR, that's consistent with GR, not evidence for new physics. You generally need 3-sigma (or better, 5-sigma) to claim a detection.

### Practical Workflow

```
Step 1: Define the question
  "Does our theory's predicted waveform match GW150914 data?"

Step 2: Download the data
  Use gwosc to get 32-second segment around event

Step 3: Preprocess
  Band-pass filter, whiten, remove glitches

Step 4: Validate pipeline
  Match-filter with a standard GR waveform template
  → Should recover published SNR (~24 for GW150914 in H1)

Step 5: Compare your theory
  Generate waveform from your theory's equations
  Match-filter against same data
  Compute Bayes factor: B = P(data|your theory) / P(data|GR)

Step 6: Interpret
  B > 1: Your theory fits better (but check for overfitting)
  B ~ 1: Can't distinguish
  B < 1: GR fits better
  B << 1: Your theory is disfavored by data
```

### Common Pitfalls

| Pitfall | How to Avoid |
|---------|--------------|
| Using unfiltered data | Always band-pass to the detector's sensitive band (~20-2000 Hz for LIGO) |
| Ignoring the noise curve | Weight by the power spectral density (PSD). LIGO is most sensitive at ~100 Hz. |
| Not windowing | Apply a Tukey window before FFTs to avoid spectral leakage |
| Overfitting | Your theory has more free parameters than GR? Penalize with BIC or use Bayesian evidence. |
| Confusing strain and displacement | LIGO measures strain h = Delta L / L, not displacement. Keep units straight. |
| Comparing apples to oranges | Make sure your predicted waveform uses the same conventions (polarizations, reference frame, tapering) |

---

## Data Analysis for Specific Physics Questions

### "Does our modified dispersion relation match LIGO data?"

1. Start from your theory's dispersion relation: omega^2 = k^2 c^2 + f(k, M_Pl, ...)
2. Compute the modified GW phase evolution during inspiral
3. Use `pycbc` to generate a template with the modified phase
4. Match-filter against GW150914 data
5. Compare SNR to the standard GR template's SNR

### "Does our theory predict the right CMB spectrum?"

1. Modify CAMB (or write a Boltzmann solver) with your theory's modifications
2. Generate C_l(TT), C_l(EE), C_l(TE) power spectra
3. Compare against Planck data
4. Compute chi-squared

### "Is our predicted graviton mass consistent with data?"

1. A massive graviton modifies the GW dispersion: v_g/c = sqrt(1 - (m_g c^2 / E)^2)
2. This causes frequency-dependent arrival times
3. Use LIGO data to bound the dispersion
4. Published bound: m_g < 1.2 x 10^-22 eV (O3 catalog)
5. If your theory predicts a specific mass, check it against this

### "Does our spectral dimension prediction match CDT?"

1. Extract the CDT spectral dimension curve from published papers
2. Compute d_s(sigma) from your theory
3. Plot both on the same axes
4. Key features to match: d_s(UV) ~ 2, d_s(IR) ~ 4, smooth transition

---

## Summary: Which Data Source for Which Question

| Question | Primary Data Source | Secondary |
|----------|-------------------|-----------|
| Graviton mass bounds | LIGO (GWOSC) | Solar system dynamics |
| GW speed = c? | LIGO + Fermi (GW170817) | — |
| Newton's law | Eot-Wash torsion balance (published) | Lunar laser ranging |
| Equivalence principle | MICROSCOPE (published) | Lunar laser ranging |
| Lorentz violation | Kostelecky data tables | LIGO, Fermi-LAT |
| CMB predictions | Planck Legacy Archive | CAMB theory code |
| Dark energy | DESI, DES, SDSS | Planck (ISW effect) |
| Black hole shadows | EHT data | — |
| Spectral dimension | CDT papers (benchmark) | — |
| Particle properties | PDG | — |
| Strong-field gravity | LIGO (binary mergers) | EHT (shadow) |
