# Known Anomalies and Open Tensions in Physics

Reference catalog for research agents. Consolidated from cosmology, particle physics, and foundational physics sources. Last updated 2026-03-26.

---

## Summary Table

| # | Anomaly | Domain | Status |
|---|---------|--------|--------|
| 1 | Hubble Tension | Cosmology | Established |
| 2 | S8 Tension | Cosmology | Strong Evidence |
| 3 | Cosmological Constant Problem | Cosmology | Established |
| 4 | DESI Dark Energy Evolution | Cosmology | Tentative |
| 5 | Dark Matter (Nature Unknown) | Cosmology | Established |
| 6 | CMB Anomalies | Cosmology | Tentative |
| 7 | Cosmic Dipole Tension | Cosmology | Strong Evidence |
| 8 | Baryon Asymmetry | Cosmology | Established |
| 9 | Cosmological Lithium Problem | Cosmology | Strong Evidence |
| 10 | El Gordo Cluster | Cosmology | Strong Evidence |
| 11 | JWST Early Galaxies | Cosmology | Tentative |
| 12 | Impossible Early Quasars | Cosmology | Strong Evidence |
| 13 | Dark Flow | Cosmology | Controversial |
| 14 | CMB Lensing Anomaly (A_lens) | Cosmology | Tentative |
| 15 | Dwarf Galaxy Problems | Cosmology | Controversial |
| 16 | Muon g-2 | Particle Physics | Controversial |
| 17 | W Boson Mass (CDF) | Particle Physics | Controversial |
| 18 | Neutrino Masses | Particle Physics | Established |
| 19 | Strong CP Problem | Particle Physics | Established |
| 20 | Hierarchy Problem | Particle Physics | Established |
| 21 | Flavor Puzzle | Particle Physics | Established |
| 22 | B-Meson Anomalies (R(D)/R(D*)) | Particle Physics | Strong Evidence |
| 23 | Proton Radius Puzzle | Particle Physics | Resolved |
| 24 | CKM Unitarity Deficit | Particle Physics | Tentative |
| 25 | Koide Formula | Particle Physics | Controversial |
| 26 | Electroweak Vacuum Stability | Particle Physics | Established |
| 27 | Quantum Measurement Problem | Foundational | Established |
| 28 | Black Hole Information Paradox | Gravity & Spacetime | Established |
| 29 | Black Hole Singularities | Gravity & Spacetime | Established |
| 30 | Arrow of Time | Foundational | Established |
| 31 | Problem of Time in QG | Gravity & Spacetime | Established |
| 32 | Galaxy Rotation Curves / MOND | Gravity & Spacetime | Controversial |
| 33 | Flyby Anomaly | Gravity & Spacetime | Tentative |
| 34 | GW Echoes | Gravity & Spacetime | Controversial |
| 35 | QG Phenomenology Gap | Gravity & Spacetime | Established |
| 36 | GW170817 vs Modified Gravity | Gravity & Spacetime | Established |
| 37 | Unruh Effect | Gravity & Spacetime | Established |
| 38 | Hawking Radiation | Gravity & Spacetime | Established |
| 39 | Pioneer Anomaly | Gravity & Spacetime | Resolved |

---

## Cosmology & Astrophysics

### 1. Hubble Tension

**What it is.** The expansion rate measured locally (Cepheids + SNe Ia) gives H0 ~ 73 km/s/Mpc. The early-universe value inferred from Planck CMB + LCDM gives H0 ~ 67.4. The gap exceeds 5 sigma and has been confirmed by multiple independent methods on both sides. JWST confirmed Cepheid measurements are not contaminated.

**Status:** Established

**Key numbers**

| Measurement | Value |
|---|---|
| Planck CMB (LCDM) | 67.4 +/- 0.5 km/s/Mpc |
| SH0ES (Cepheids + SNe Ia) | 73.04 +/- 1.04 km/s/Mpc |
| TDCOSMO (strong lensing) | ~74 km/s/Mpc |
| Freedman TRGB + JWST | 69.85 +/- 1.75 km/s/Mpc |
| ACT DR6 | ~67.6 km/s/Mpc |
| Discrepancy | ~5 km/s/Mpc, >5 sigma |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck Legacy Archive | https://pla.esac.esa.int/ | Sky maps, power spectra, likelihoods |
| ACT DR6 | https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/ | Ground-based CMB |
| Pantheon+ SNe Ia | https://github.com/PantheonPlusSH0ES/DataRelease | 1701 light curves, includes SH0ES Cepheid data |
| TDCOSMO | https://shsuyu.github.io/H0LiCOW/site/ | Strong lensing time delays |
| Python: `camb` | https://camb.readthedocs.io/ | Boltzmann code for CMB spectra |
| Python: `cobaya` | https://cobaya.readthedocs.io/ | Bayesian parameter estimation with Planck likelihoods |

**What would solving it mean.** A theory must produce H0 ~ 73 from early-universe physics (or show local measurements are biased) while preserving the CMB power spectrum, BAO, and BBN. The mechanism must be physically motivated with predictions beyond H0.

---

### 2. S8 Tension (Matter Clumpiness)

**What it is.** The CMB predicts how clumpy matter should be today. Weak lensing surveys consistently find 5-8% less clustering than predicted. The tension sits at 2-3 sigma across KiDS, DES, and HSC surveys and has persisted through multiple data releases.

**Status:** Strong Evidence

**Key numbers**

| Measurement | S8 value |
|---|---|
| Planck 2018 (CMB) | 0.834 +/- 0.016 |
| KiDS-1000 | 0.759 +0.024/-0.021 |
| DES Y3 | 0.776 +/- 0.017 |
| HSC Y3 | ~0.77 |
| Discrepancy | ~2-3 sigma lower |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| KiDS-1000 | https://kids.strw.leidenuniv.nl/DR4/lensing.php | 21M sources, shear catalogs |
| DES Y3 | https://www.darkenergysurvey.org/des-year-3-cosmology-results-papers/ | 100M sources, 4143 deg^2 |
| Planck Legacy Archive | https://pla.esac.esa.int/ | CMB-derived S8 |
| Python: `pyccl` | pip install pyccl | Lensing power spectra predictions |
| Python: `pymaster` | pip install pymaster | Pseudo-Cl estimation |

**What would solving it mean.** Explain why late-universe probes see less clustering than CMB predicts, while preserving the CMB fit, BAO, and H0 constraints. Candidates: massive neutrinos, dark energy evolution, modified gravity, dark matter self-interactions.

---

### 3. Cosmological Constant Problem

**What it is.** QFT predicts vacuum energy density ~10^71 GeV^4 (Planck cutoff). The observed value is ~2.5 x 10^-47 GeV^4 -- a mismatch of 55-120 orders of magnitude depending on cutoff. Additionally, dark energy and matter densities are comparable *now* despite scaling differently (the coincidence problem).

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Observed vacuum energy density | ~2.5 x 10^-47 GeV^4 |
| QFT prediction (Planck cutoff) | ~10^71 GeV^4 |
| QFT prediction (SM cutoff) | ~10^-1 to 10^13 GeV^4 |
| Dark energy fraction | Omega_Lambda ~ 0.685 |
| Equation of state | w = -1.03 +/- 0.03 |
| Cosmological constant | Lambda ~ 1.1 x 10^-52 m^-2 |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck Legacy Archive | https://pla.esac.esa.int/ | Omega_Lambda, w constraints |
| Pantheon+ SNe Ia | https://github.com/PantheonPlusSH0ES/DataRelease | Distance-redshift relation |
| DESI BAO | https://data.desi.lbl.gov/doc/releases/dr1/ | Most precise BAO |
| CosmoVerse Tensions DB | https://cosmoversetensions.eu/ | Community tension tracker |
| Python: `astropy.cosmology` | Part of astropy | Distance calculations for arbitrary w(z) |
| Python: `CLASS` | pip install classy | Boltzmann solver |

**What would solving it mean.** A mechanism (not fine-tuning) explaining why vacuum energy does not gravitate as naively expected, or dynamically drives the cosmological constant to its observed value. Must accommodate w ~ -1 and the Planck CMB fit.

---

### 4. DESI Dark Energy Evolution

**What it is.** DESI DR2 (March 2025, 14M spectra) finds evidence that dark energy's equation of state varies with time. A cosmological constant (w = -1) is rejected at 2.8-4.2 sigma depending on supernova dataset. The signal strengthened from DR1 to DR2.

**Status:** Tentative

**Key numbers**

| Quantity | Value |
|---|---|
| w0 (DESI DR2 + Planck + Pantheon+) | ~-0.7 to -0.8 |
| wa | ~-0.6 to -1.0 |
| Rejection of w = -1 | 2.8 sigma (Pantheon+), 3.8 sigma (Union3), 4.2 sigma (DES-SN5YR) |
| BAO precision at z > 2 | 0.65% |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| DESI DR1 public data | https://data.desi.lbl.gov/doc/releases/dr1/ | 18.7M objects |
| DESI on AWS | S3 bucket `desidata` | Cloud querying |
| NOIRLab Astro Data Lab | https://datalab.noirlab.edu/data/desi | Database queries + SPARCL |
| DESI tutorials | https://github.com/desihub/tutorials | Jupyter notebooks |
| DESI DR2 papers | https://data.desi.lbl.gov/doc/papers/dr2/ | Analysis papers |

**What would solving it mean.** Predict the specific form of w(z) from a Lagrangian -- quintessence, modified gravity, or vacuum phase transition. Must fit CMB, BAO at all redshifts, and supernova distances simultaneously. If w crosses -1, must avoid ghost instabilities.

---

### 5. Dark Matter

**What it is.** ~27% of the universe's energy budget is something that gravitates but does not interact with light. Evidence is overwhelming and multi-scale (rotation curves, Bullet Cluster, CMB acoustic peaks, large-scale structure). No dark matter particle has been directly detected despite decades of searching. WIMPs are increasingly constrained; axions and sterile neutrinos remain viable.

**Status:** Established (existence). Nature unknown.

**Key numbers**

| Quantity | Value |
|---|---|
| Dark matter density | Omega_DM h^2 = 0.120 +/- 0.001 |
| DM-to-baryon ratio | ~5.4:1 |
| Local DM density | ~0.3 GeV/cm^3 |
| WIMP cross-section limit (LZ 2025) | sigma_SI < 2.2 x 10^-48 cm^2 at 40 GeV |
| ADMX axion limit | KSVZ excluded for m_a ~ 4.5-5.4 micro-eV |
| Neutrino fog floor | ~10^-49 cm^2 |
| Bullet Cluster mass offset | ~150 kpc lensing-gas offset |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| SPARC rotation curves | http://astroweb.case.edu/SPARC/ | 175 galaxies |
| BIG-SPARC | https://arxiv.org/abs/2411.13329 | ~4000 galaxies |
| LZ results | https://lz.lbl.gov/ | Best WIMP limits |
| ADMX | https://depts.washington.edu/admx/ | Axion search |
| Axion limits compilation | https://github.com/cajohare/AxionLimits | Python-accessible plots + data |
| Neutrino fog compilation | https://github.com/cajohare/NeutrinoFog | Direct detection floor |
| Bullet Cluster (Chandra) | https://cda.harvard.edu/chaser/ | Search for 1E 0657-56 |
| PDG dark matter review | https://pdg.lbl.gov/2025/reviews/rpp2024-rev-dark-matter.pdf | Authoritative review |
| Planck CMB | https://pla.esac.esa.int/ | DM density from CMB |
| Python: `galpy` | pip install galpy | Rotation curve modeling |
| Python: `colossus` | pip install colossus | Halo mass functions |
| Python: `darkhistory` | pip install darkhistory | DM energy injection cosmology |

**What would solving it mean.** Identify a particle (or gravitational modification) that explains all scales -- rotation curves, cluster lensing, CMB peaks, Bullet Cluster -- with correct relic abundance and consistency with null direct detection. Must predict something new and testable.

---

### 6. CMB Anomalies

**What it is.** Several features in the CMB are statistically unusual under LCDM: the Cold Spot (~70 uK cold, ~5 deg), hemispherical power asymmetry (~3 sigma), quadrupole-octupole alignment (99% unusual), near-zero large-angle correlations (>99.9% unusual), and odd-even parity asymmetry. Planck confirmed all relative to WMAP.

**Status:** Tentative

**Key numbers**

| Anomaly | Significance |
|---|---|
| Cold Spot | ~2-3 sigma, ~70 uK, ~5 deg toward Eridanus |
| Hemispherical asymmetry | ~3 sigma, dipole modulation A ~ 0.07 |
| Quadrupole-octupole alignment | 99% unusual |
| Missing large-angle correlations | >99.9% unusual |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck Legacy Archive | https://pla.esac.esa.int/ | Full-sky CMB maps |
| WMAP 9-year | https://lambda.gsfc.nasa.gov/product/wmap/ | Independent CMB satellite |
| NASA LAMBDA | https://lambda.gsfc.nasa.gov/ | Central CMB data repository |
| Python: `healpy` | pip install healpy | Spherical harmonic analysis |
| Python: `camb` | pip install camb | Theoretical CMB realizations |

**What would solving it mean.** Explain multiple anomalies simultaneously, predict CMB polarization anomalies, and survive look-elsewhere correction. Could point to pre-inflationary physics, non-trivial topology, or anisotropic cosmologies.

---

### 7. Cosmic Dipole Tension

**What it is.** The CMB dipole implies we move at ~370 km/s through the CMB rest frame. Distant radio sources and quasars should show a corresponding dipole of predictable amplitude. Multiple surveys find the right direction but 2-5x larger amplitude than expected.

**Status:** Strong Evidence

**Key numbers**

| Quantity | Value |
|---|---|
| CMB dipole velocity | 369.82 +/- 0.11 km/s |
| NVSS+RACS radio dipole | ~3x kinematic expectation, 4.8 sigma |
| CatWISE quasar dipole | ~4-5x expectation, >5 sigma vs Planck |
| Direction agreement | Within ~20 deg of CMB dipole |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| NVSS catalog | https://www.cv.nrao.edu/nvss/ | 1.77M radio sources |
| RACS (ASKAP) | https://research.csiro.au/racs/ | 2.1M radio sources |
| CatWISE 2020 | https://catwise.github.io/ | IR-selected quasars |
| VizieR | https://vizier.cds.unistra.fr/ | Cross-catalog access |
| Python: `astroquery` | pip install astroquery | Query VizieR, IRSA |
| Python: `healpy` | pip install healpy | Dipole fitting |

**What would solving it mean.** Either identify a systematic in radio/IR surveys that inflates amplitude without changing direction, or provide a physical mechanism for a cosmological dipole that is consistent with the CMB power spectrum at l >= 2.

---

### 8. Baryon Asymmetry (Matter-Antimatter Imbalance)

**What it is.** The Big Bang should have produced equal matter and antimatter. Instead, ~1 extra baryon survived per 1.6 billion baryon-antibaryon pairs. The SM has some CP violation (Jarlskog invariant J ~ 3 x 10^-5) but it is quantitatively insufficient by many orders of magnitude.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Baryon-to-photon ratio (eta) | (6.10-6.14 +/- 0.04) x 10^-10 |
| Baryon asymmetry | ~1 part in 1.6 x 10^9 |
| Baryon density | Omega_b h^2 = 0.02237 +/- 0.00015 |
| SM CP violation (Jarlskog) | J ~ 3 x 10^-5 (far too small) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck cosmological parameters | https://pla.esac.esa.int/ | Omega_b h^2 |
| PDG reviews (BBN, Baryogenesis) | https://pdg.lbl.gov/ | Authoritative |
| LHCb CP violation | https://lhcb-public.web.cern.ch/ | Experimental CP data |
| EDM experiments (nEDM, ACME, JILA) | Various | Testing CP violation sources |
| Electron EDM (JILA 2023) | https://www.science.org/doi/10.1126/science.adg4084 | Best electron EDM limit |
| T2K / NOvA / DUNE | Various experiment sites | Leptonic CP violation |

**What would solving it mean.** Produce eta ~ 6 x 10^-10 from a specific baryogenesis mechanism with correlated testable signals (EDM, collider particles, neutrino CP phase, gravitational waves from first-order phase transition).

---

### 9. Cosmological Lithium Problem

**What it is.** BBN predicts Li-7/H ~ (4.7-5.6) x 10^-10. The observed Spite plateau in metal-poor stars gives ~1.6 x 10^-10 -- a factor ~3-3.5x discrepancy at 4-5 sigma. Deuterium and He-4 predictions match beautifully. Astrophysical depletion explanations struggle to reproduce the plateau's uniformity. A 2025 A&A paper claims resolution via Pop III chemical evolution, not yet consensus.

**Status:** Strong Evidence

**Key numbers**

| Quantity | Value |
|---|---|
| BBN predicted Li-7/H | (4.7-5.6) x 10^-10 |
| Observed Li-7/H (Spite plateau) | ~1.6 x 10^-10 |
| Discrepancy factor | ~3-3.5x |
| Significance | ~4-5 sigma |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG BBN review | https://pdg.lbl.gov/ | Predicted and observed abundances |
| PArthENoPE BBN code | http://parthenope.na.infn.it/ | Public BBN calculator |
| PRIMAT BBN code | https://www2.iap.fr/users/pitrou/primat.htm | Alternative BBN code |
| AlterBBN | https://alterbbn.hepforge.org/ | Another BBN code |
| NACRE II | http://www.astro.ulb.ac.be/nacreii/ | Nuclear reaction rates |
| Spite plateau data | Literature: Sbordone+ 2010, Spite & Spite 1982 | Stellar Li-7 measurements |

**What would solving it mean.** Reduce predicted Li-7 by ~3x without disrupting D and He-4 agreement. If astrophysical: explain the universal Spite plateau. If new physics: specify the mechanism (late-decaying particles, modified reaction rates) with other testable predictions.

---

### 10. El Gordo Cluster

**What it is.** ACT-CL J0102-4915 ("El Gordo") is a massive merging cluster (~3 x 10^15 M_sun) at z = 0.87. Its mass and infall velocity (~2500 km/s) give it a probability of ~10^-10 in LCDM -- a 6.2 sigma tension.

**Status:** Strong Evidence

**Key numbers**

| Quantity | Value |
|---|---|
| Mass (M200) | ~3.2 x 10^15 M_sun |
| Redshift | z = 0.87 |
| Infall velocity | >= 2500 km/s |
| LCDM probability | ~7.5 x 10^-10 (6.2 sigma) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| ACT cluster catalog | https://lambda.gsfc.nasa.gov/product/act/ | SZ-detected clusters |
| Chandra X-ray archive | https://cda.harvard.edu/chaser/ | X-ray morphology |
| Python: `hmf` | pip install hmf | Halo mass function calculator |
| Python: `colossus` | pip install colossus | Cluster abundance predictions |

**What would solving it mean.** Either produce such clusters at reasonable rates in a modified cosmology, or demonstrate mass/velocity estimates are biased to move tail probability to >= ~10^-3.

---

### 11. JWST "Impossible Early Galaxies"

**What it is.** JWST detected numerous luminous, massive galaxies at z > 7-10 (<700 Myr after Big Bang). Initial mass estimates required >80% baryon-to-star efficiency. A 2025 NASA study found some contain AGN inflating mass estimates. After correction, tension reduced but ~2x excess remains at z > 10.

**Status:** Tentative

**Key numbers**

| Quantity | Value |
|---|---|
| Redshifts of concern | z ~ 7-16 |
| Initial mass estimates | ~10^10-10^11 M_sun at z > 10 |
| Post-AGN correction | Factor ~2-5 lower |
| Remaining excess | ~2x more than LCDM at z > 10 |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| JWST data (MAST) | https://mast.stsci.edu/ | All JWST imaging/spectroscopy |
| CEERS survey | https://ceers.github.io/ | Major early galaxy survey |
| JADES survey | Via MAST | JWST Advanced Deep Extragalactic Survey |

**What would solving it mean.** Produce the UV luminosity function at z > 10 within LCDM (via modified star formation physics, AGN contribution) or require new cosmological physics.

---

### 12. Impossible Early Quasars

**What it is.** JWST and ground-based surveys find supermassive black holes (10^8-10^9 M_sun) at z > 7, too massive to explain by standard Eddington-limited accretion in <700 Myr.

**Status:** Strong Evidence

**Key numbers**

| Quantity | Value |
|---|---|
| BH masses at z > 7 | 10^8-10^9 M_sun |
| Time available | <700 Myr |
| Standard accretion | Cannot reach observed masses from stellar seeds |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| JWST data (MAST) | https://mast.stsci.edu/ | Quasar spectra |
| SDSS quasar catalog | https://www.sdss.org/dr18/ | Ground-based complement |

**What would solving it mean.** Identify the seeding mechanism: direct collapse BHs, super-Eddington accretion, primordial BHs, or modified early-universe growth rates.

---

### 13. Dark Flow

**What it is.** Kashlinsky et al. (2008-2010) claimed ~1000+ galaxy clusters share a coherent bulk flow of 600-1000 km/s toward Centaurus/Vela, beyond LCDM expectations. Planck (2014) found no evidence for this signal.

**Status:** Controversial (likely not real)

**Key numbers**

| Quantity | Value |
|---|---|
| Claimed velocity | 600-1000 km/s |
| Expected from LCDM | ~200-300 km/s at 100 Mpc |
| Planck 2014 | No significant signal at >300 Mpc |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck SZ cluster catalog | https://pla.esac.esa.int/ | SZ clusters |
| CosmicFlows-4 | https://www.ipnl.in2p3.fr/projet/cosmicflows/ | Peculiar velocities |
| Kashlinsky et al. | https://arxiv.org/abs/0809.3734 | Original claim |

**What would solving it mean.** Either definitive confirmation with independent data at >5 sigma (pointing to pre-inflationary physics), or demonstration that the signal is systematics.

---

### 14. CMB Lensing Anomaly (A_lens)

**What it is.** Planck CMB shows more lensing smoothing than expected. The phenomenological parameter A_lens (should be 1) is preferred at ~1.1 at ~2.5 sigma. ACT and SPT show less of this anomaly.

**Status:** Tentative

---

### 15. Dwarf Galaxy Problems

**What it is.** Missing satellites (fewer than predicted), too-big-to-fail (massive subhalos without visible galaxies), and planes of satellites (thin planar orbits extremely unlikely in LCDM). Baryonic feedback partially resolves the first two; the planes problem persists.

**Status:** Controversial

---

## Particle Physics

### 16. Muon g-2 Anomaly

**What it is.** The muon's anomalous magnetic moment is measured to extraordinary precision. Fermilab's final result (2025) confirmed the experimental value. However, lattice QCD now gives a SM prediction that agrees with experiment, while older data-driven predictions show ~5 sigma tension. The theoretical community has not reached consensus.

**Status:** Controversial

**Key numbers**

| Quantity | Value |
|---|---|
| Experimental (Fermilab final 2025) | a_mu = 116592070.5(14.6) x 10^-11 |
| SM (lattice-based, 2025) | a_mu = 116592033(62) x 10^-11 |
| SM (data-driven e+e-) | a_mu = 116591810(43) x 10^-11 |
| Discrepancy vs data-driven | ~5 sigma |
| Discrepancy vs lattice | ~0.6 sigma (not significant) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Fermilab final paper | https://muon-g-2.fnal.gov/result2025.pdf | Experiment |
| Muon g-2 Theory Initiative | https://muon-gm2-theory.illinois.edu/ | Theory consensus effort |
| BMW lattice data | https://arxiv.org/abs/2002.12347 | Key lattice calculation |
| PDG | https://pdg.lbl.gov/ | Muon magnetic anomaly review |
| HEPData | https://www.hepdata.net/ | e+e- cross-section data |
| Python: `pdg` | pip install pdg | Programmatic PDG access |

**What would solving it mean.** First, resolve the lattice vs data-driven discrepancy. If data-driven is correct, a new particle must contribute ~250 x 10^-11 to a_mu without violating other constraints.

---

### 17. W Boson Mass (CDF Anomaly)

**What it is.** CDF II (2022) measured M_W = 80,433.5 +/- 9.4 MeV, 7 sigma above the SM prediction. However, ATLAS and CMS both agree with the SM. CDF is an outlier; most of the community considers it a systematic error.

**Status:** Controversial (likely systematic)

**Key numbers**

| Measurement | M_W (MeV) |
|---|---|
| CDF II (2022) | 80,433.5 +/- 9.4 |
| CMS (2024) | 80,360.2 +/- 9.9 |
| ATLAS (2024) | 80,366.5 +/- 15.9 |
| SM prediction (EW fit) | 80,357 +/- 6 |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| CDF paper | https://www.science.org/doi/10.1126/science.abk1781 | Original measurement |
| PDG W mass review | https://pdg.lbl.gov/2025/reviews/rpp2024-rev-w-mass.pdf | World average |
| Gfitter EW fit | http://project-gfitter.web.cern.ch/project-gfitter/ | SM prediction |

**What would solving it mean.** Most likely: detailed identification of the CDF systematic. If real: a new particle contributing to W self-energy by ~76 MeV without disturbing other EW observables (extremely difficult).

---

### 18. Neutrino Masses

**What it is.** Neutrinos oscillate between flavors, proving they have nonzero mass -- the only confirmed departure from the minimal SM. We know mass-squared differences but not absolute scale, mass ordering (normal vs inverted), or whether neutrinos are Dirac or Majorana.

**Status:** Established (oscillations). Mechanism unknown.

**Key numbers**

| Quantity | Value |
|---|---|
| Delta m^2_21 (solar) | 7.53 +/- 0.18 x 10^-5 eV^2 |
| |Delta m^2_32| (atmospheric) | 2.453 +/- 0.033 x 10^-3 eV^2 |
| Direct mass limit (KATRIN 2025) | m_nu_e < 0.45 eV (90% CL) |
| Cosmological bound (Planck+BAO) | Sum of masses < ~0.12 eV (95% CL) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| NuFIT global fit | http://www.nu-fit.org/ | Best-fit oscillation parameters, chi-squared tables |
| KATRIN 2025 | https://www.science.org/doi/10.1126/science.adq9592 | Direct mass measurement |
| T2K + NOvA joint analysis | https://www.nature.com/articles/s41586-025-09599-3 | Mass ordering analysis |
| PDG neutrino review | https://pdg.lbl.gov/ | Comprehensive review |
| Planck Legacy Archive | https://pla.esac.esa.int/ | Cosmological mass bounds |
| Python: `nuoscprobexact` | pip install nuoscprobexact | Oscillation probability calculations |

**What would solving it mean.** Explain why neutrinos are massive, why masses are 6+ orders of magnitude below the electron, the large mixing pattern, and whether they are Majorana. Predict the mass ordering and CP phase delta_CP.

---

### 19. Strong CP Problem

**What it is.** The QCD Lagrangian allows a CP-violating parameter theta. No reason theta should be small, yet the neutron EDM constrains theta < 10^-10. The leading solution -- the axion -- is also a dark matter candidate.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| theta_QCD | < 10^-10 |
| Best nEDM limit | |d_n| < 1.8 x 10^-26 e-cm (PSI 2020) |
| n2EDM target sensitivity | ~10^-27 e-cm |
| QCD axion mass window (if all DM) | ~1-1000 micro-eV |
| ADMX exclusion | KSVZ axions at 1.10-1.31 GHz (~4.5-5.4 micro-eV) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| nEDM measurement | https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.124.081803 | Best limit |
| PDG axion review | https://pdg.lbl.gov/ | "Axions and Other Similar Particles" |
| ADMX | https://depts.washington.edu/admx/ | Axion search results |
| Axion limits compilation | https://github.com/cajohare/AxionLimits | Python-accessible data files |
| IAXO | https://iaxo.desy.de/ | Future solar axion search |

**What would solving it mean.** Discover the axion (mass + coupling), confirm an alternative symmetry mechanism, or find a nonzero nEDM with a dynamical explanation for small theta.

---

### 20. Hierarchy Problem

**What it is.** The Higgs mass is 125 GeV. Quantum corrections should push it to the Planck scale (~10^19 GeV) unless they cancel to 1 part in 10^34. The LHC has excluded the simplest SUSY, composite Higgs, and extra dimension models up to several TeV.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Higgs mass | 125.25 +/- 0.17 GeV |
| Planck mass | 1.22 x 10^19 GeV |
| Fine-tuning required | ~1 part in 10^34 |
| LHC exclusions | Gluinos > ~2.3 TeV, stops > ~1.3 TeV |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| ATLAS Higgs | https://atlas.cern/result/higgs-boson | Combined Higgs results |
| CMS Higgs | https://cms.cern/physics/higgs-boson | Combined Higgs results |
| ATLAS SUSY summary | https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CombinedSummaryPlots/SUSY/ | Exclusion plots |
| CMS SUSY summary | https://cms-results.web.cern.ch/cms-results/public-results/publications/SUS/ | Exclusion plots |
| CERN Open Data | https://opendata.cern.ch/ | LHC collision data |

**What would solving it mean.** A symmetry protecting the Higgs mass with testable partner particles, a dynamical selection mechanism, or a principled explanation of why naturalness fails. Must preserve measured Higgs properties.

---

### 21. Flavor Puzzle

**What it is.** The SM has three generations with masses spanning a factor of ~10^12 (top quark to lightest neutrino), mixing angles that differ wildly between quarks (small) and leptons (large), and ~20 free parameters with no known pattern. Why three generations? Why these masses?

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Mass range | m_t / m_u ~ 75,000; m_t / m_nu ~ 10^12 |
| CKM mixing (quark) | V_us ~ 0.22, V_cb ~ 0.04, V_ub ~ 0.004 |
| PMNS mixing (lepton) | theta_12 ~ 34 deg, theta_23 ~ 49 deg, theta_13 ~ 8.6 deg |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG reviews | https://pdg.lbl.gov/ | Quark masses, CKM, neutrino mixing |
| NuFIT | http://www.nu-fit.org/ | Lepton mixing fits |
| CKMfitter | http://ckmfitter.in2p3.fr/ | Quark mixing fits |
| FLAG lattice review | https://flag.unibe.ch/ | Lattice QCD quark masses |
| Python: `flavio` | pip install flavio | Flavor physics toolkit |

**What would solving it mean.** Predict (not accommodate) the mass/mixing pattern from fewer parameters. Explain why three generations, why the hierarchy, and why quark vs lepton mixing differs.

---

### 22. B-Meson Anomalies

**What it is.** R(K)/R(K*) anomalies (neutral current) disappeared in LHCb's 2022 update. However, R(D)/R(D*) (charged current, involving tau) persist at ~3.3 sigma combined excess. Angular observable P5' shows 2-3 sigma tensions. Belle II is actively collecting data.

**Status:** Strong Evidence (R(D)/R(D*) only)

**Key numbers**

| Observable | Value | SM prediction |
|---|---|---|
| R(D) world average | 0.342 +/- 0.026 | 0.298 +/- 0.004 |
| R(D*) world average | 0.287 +/- 0.012 | 0.254 +/- 0.005 |
| Combined tension | ~3.3 sigma | |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| HFLAV averages | https://hflav.web.cern.ch/ | Authoritative world averages |
| Belle II | https://www.belle2.jp/ | Active experiment |
| LHCb public results | https://lhcbproject.web.cern.ch/lhcbproject/Publications/LHCbProjectPublic/Summary_RXMu.html | R(K), angular analyses |
| Python: `flavio` | pip install flavio | SM predictions, BSM fits |
| Python: `wilson` | pip install wilson | Wilson coefficient running |

**What would solving it mean.** A new particle (charged Higgs, leptoquark, W') enhancing b -> c tau nu by ~20-30% while respecting B_c lifetime, LHC high-pT tails, and tau polarization measurements.

---

### 23. Proton Radius Puzzle (Resolved)

**What it is.** Muonic hydrogen (2010) gave r_p = 0.8409 fm, 4% smaller than older electronic hydrogen measurements (~0.88 fm). Newer measurements have converged to the smaller value. PDG 2025 consensus: r_p = 0.8409(4) fm. Some e-p scattering tension remains (PRad vs Mainz); PRad-II is clarifying.

**Status:** Resolved (largely)

**Key numbers**

| Measurement | r_p (fm) |
|---|---|
| Muonic hydrogen | 0.84087(39) |
| PDG 2025 consensus | 0.8409(4) |
| PRad (JLab) | 0.831(14) |
| Older e-p scattering (Mainz) | 0.879(8) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG proton listing | https://pdg.lbl.gov/ | Consensus value |
| CODATA proton radius | https://physics.nist.gov/cgi-bin/cuu/Value?rp | Official NIST value |
| NIST Atomic Spectra DB | https://www.nist.gov/pml/atomic-spectra-database | Hydrogen spectroscopy |

---

### 24. CKM Unitarity Deficit (Cabibbo Angle Anomaly)

**What it is.** The CKM first-row unitarity sum |V_ud|^2 + |V_us|^2 + |V_ub|^2 falls ~3 sigma below 1. Depends critically on inner radiative corrections to nuclear beta decay and lattice QCD for V_us. Situation is in flux.

**Status:** Tentative

**Key numbers**

| Quantity | Value |
|---|---|
| |V_ud| | 0.97367(32) |
| |V_us| | 0.2243(5) |
| First-row sum | 0.9985(5) (~3 sigma below 1) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG CKM review | https://pdg.lbl.gov/ | "The CKM Quark-Mixing Matrix" |
| CKMfitter | http://ckmfitter.in2p3.fr/ | Global CKM fits |
| Hardy & Towner compilation | https://journals.aps.org/prc/abstract/10.1103/PhysRevC.102.045501 | Superallowed decays |
| FLAG lattice review | https://flag.unibe.ch/ | V_us inputs |

**What would solving it mean.** Either improved theory restores unitarity, or new physics (fourth generation, heavy vector boson, right-handed currents) predicts the deficit with additional testable consequences.

---

### 25. Koide Formula

**What it is.** The charged lepton masses satisfy Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3 to 0.001% accuracy. No known theoretical reason. Extensions to quarks do not work as cleanly.

**Status:** Controversial (unexplained curiosity)

**Key numbers**

| Quantity | Value |
|---|---|
| Predicted Q | 2/3 exactly |
| Measured Q | 0.666661(7) |
| Accuracy | ~0.001% |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG lepton masses | https://pdg.lbl.gov/ | Electron, muon, tau |
| Python: `particle` | pip install particle | Pythonic mass access |
| Original Koide paper | https://link.springer.com/article/10.1007/BF02817096 | Lett. Nuovo Cim. 34, 201 (1982) |

**What would solving it mean.** Derive Q = 2/3 from a symmetry with fewer assumptions than three input masses, predict extensions, and make at least one additional testable prediction.

---

### 26. Electroweak Vacuum Stability

**What it is.** With measured Higgs (~125 GeV) and top (~173 GeV) masses, the SM Higgs potential develops a deeper minimum at ~10^11 GeV, making our vacuum metastable. Vacuum lifetime ~10^600 years. The near-criticality (sitting right at the stability boundary) may itself be a clue.

**Status:** Established (within SM)

**Key numbers**

| Quantity | Value |
|---|---|
| Higgs mass | 125.25 +/- 0.17 GeV |
| Top quark pole mass | 172.57 +/- 0.29 GeV |
| Instability scale | ~10^11 GeV |
| Vacuum lifetime | ~10^600 years |
| Stability boundary | m_top < ~171 GeV (approximate) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| PDG Higgs, top mass | https://pdg.lbl.gov/ | Input measurements |
| Degrassi et al. | https://arxiv.org/abs/1205.6497 | Key theoretical paper |
| Python: `mr` | https://github.com/apik/mr | SM parameter running |
| PyR@TE | https://pyrate.hepforge.org/ | RG evolution of SM couplings |

**What would solving it mean.** Explain why the vacuum is metastable and why we ended up here, or introduce stabilizing new physics near 10^11 GeV, or explain near-criticality from a deeper principle.

---

## Gravity & Spacetime

### 27. Quantum Measurement Problem

**What it is.** Quantum mechanics does not explain how or why definite measurement outcomes occur. The Schrodinger equation is deterministic and linear; measurement appears to be neither. Objective collapse models (GRW, CSL, Diosi-Penrose) predict testable deviations from standard QM. Macro-superposition experiments are tightening constraints.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Largest superposition | ~2000-atom molecules (Vienna group) |
| CSL collapse rate excluded | Above ~10^-8 s^-1 at ~10^-15 kg |
| GRW collapse rate (original) | lambda ~ 10^-16 s^-1, partially constrained |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| CSL bounds compilation | https://arxiv.org/abs/2203.11028 | Comprehensive |
| Molecule interferometry | https://www.nature.com/articles/s41567-019-0663-9 | Largest superpositions |
| LIGO collapse constraints | https://arxiv.org/abs/1606.06266 | GW detector as collapse tester |
| Spontaneous radiation tests | https://www.nature.com/articles/s41567-020-1008-4 | X-ray emission searches |
| Python: `qutip` | pip install qutip | Quantum dynamics simulations |

**What would solving it mean.** Confirm objective collapse via deviations from unitarity in macroscopic experiments, or establish a framework that resolves the problem while reproducing all QM predictions with a novel testable prediction.

---

### 28. Black Hole Information Paradox

**What it is.** Hawking radiation is thermal and carries no information about what fell in. If a black hole evaporates completely, unitarity is violated. The island formula and Page curve developments (2019-2020) reproduce the expected entropy curve but leave the physical mechanism unspecified.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Hawking temperature (solar mass) | ~6 x 10^-8 K |
| Evaporation time (solar mass) | ~2 x 10^67 years |
| Bekenstein-Hawking entropy (solar mass) | ~10^77 k_B |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| LIGO/Virgo/KAGRA catalog | https://gwosc.org/eventapi/ | BH mass/spin data |
| GW strain data | https://gwosc.org/data/ | Raw data |
| EHT shadow images | https://eventhorizontelescope.org/ | Near-horizon geometry |
| BEC analog (Steinhauer) | https://www.nature.com/articles/nphys3863 | Analog Hawking pairs |
| Circuit analog (2023) | https://www.nature.com/articles/s41467-023-39064-6 | Superconducting analog |
| Python: `gwpy`, `pycbc` | pip install gwpy pycbc | GW analysis |

**What would solving it mean.** A concrete mechanism showing how information is preserved, reproducing the Page curve quantitatively, specifying the evaporation endpoint, and making a prediction distinguishable from "information is lost."

---

### 29. Black Hole Singularities

**What it is.** GR predicts infinite density at r = 0 where the theory breaks down. The Penrose-Hawking theorems prove singularities are generic. Every QG program claims to resolve them differently (LQG bounce, AS running G, string fuzzballs). No observation distinguishes these scenarios.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Planck density | ~5.16 x 10^93 kg/m^3 |
| Planck length | ~1.6 x 10^-35 m |
| LQG bounce density | ~0.41 rho_Planck |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| GWOSC (GW ringdown) | https://gwosc.org/eventapi/ | Mass/spin from ringdown |
| EHT | https://eventhorizontelescope.org/ | Shadow images |
| Python: `ehtim` | https://github.com/achael/eht-imaging | EHT imaging pipeline |

**What would solving it mean.** A QG calculation showing what replaces the singularity, with observable consequences: GW echoes, quasinormal mode deviations, or bouncing cosmology CMB imprints.

---

### 30. Arrow of Time

**What it is.** All fundamental laws are time-symmetric (or CPT-symmetric), yet the universe exhibits a stark entropy asymmetry. The "Past Hypothesis" -- the early universe had very low entropy -- is accepted as description but not explanation. Penrose estimates the specialness of the initial state at 1 in 10^(10^123).

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Entropy of observable universe today | ~10^103 k_B (SMBH-dominated) |
| Entropy of CMB | ~10^89 k_B |
| Penrose specialness estimate | 1 in 10^(10^123) |
| Boltzmann brain timescale | ~10^(10^69) years |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Planck Legacy Archive | https://pla.esac.esa.int/ | Early-universe entropy from CMB |
| SDSS | https://www.sdss.org/ | SMBH mass function for entropy budget |
| IllustrisTNG | https://www.tng-project.org/data/ | Cosmological simulations |

**What would solving it mean.** A dynamical mechanism producing low-entropy initial conditions without fine-tuning, a reformulation where time-asymmetry is fundamental, or demonstration that entropy increase is observer selection. Must be compatible with CMB isotropy at 1 part in 10^5.

---

### 31. Problem of Time in Quantum Gravity

**What it is.** In canonical QG, the Hamiltonian is a constraint (H|psi> = 0, the Wheeler-DeWitt equation), meaning physical states do not evolve. Time is dynamical in GR but external in QM. Multiple resolution strategies exist (Page-Wootters, relational, emergent semiclassical) but no consensus.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Wheeler-DeWitt equation | H|psi> = 0 |
| Planck time | ~5.4 x 10^-44 s |
| Resolution strategies cataloged (Isham 1993) | ~3 major types, ~12 subtypes |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Isham canonical review | https://arxiv.org/abs/gr-qc/9210011 | Definitive classification |
| Page-Wootters experiment | https://arxiv.org/abs/1310.4691 | Moreva et al. photon analog |
| BICEP/Keck | https://bicepkeck.org/ | Primordial GW bounds |

**What would solving it mean.** Derive time evolution from a timeless constraint with clear physical interpretation of "time," reproducing semiclassical GR in the appropriate limit and handling the multiple-choice problem.

---

### 32. Galaxy Rotation Curves / MOND

**What it is.** Galaxies rotate faster in outer regions than Newtonian gravity predicts from visible matter. The standard explanation is dark matter. MOND (Milgrom 1983) offers an alternative: below a_0 = 1.2 x 10^-10 m/s^2, gravity transitions to a modified form. MOND predicts individual rotation curves and the Radial Acceleration Relation with remarkable accuracy but fails for clusters and lacks a satisfactory relativistic completion.

**Status:** Controversial

**Key numbers**

| Quantity | Value |
|---|---|
| MOND critical acceleration a_0 | 1.2 x 10^-10 m/s^2 |
| Coincidence: a_0 ~ cH_0/(2pi) | Within order unity |
| RAR scatter | ~0.13 dex |
| Cluster deficit in MOND | Still needs ~2x observed baryons |
| Wide binary test (Chae 2023) | Claimed deviation, disputed |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| SPARC database | https://astroweb.case.edu/SPARC/ | 175 galaxy rotation curves |
| BIG-SPARC | https://arxiv.org/abs/2411.13329 | ~4000 galaxies |
| Python: `pygrc` | https://github.com/amanmdesai/pygrc | SPARC analysis |
| Gaia DR3 (wide binaries) | https://gea.esac.esa.int/archive/ | Low-acceleration test |
| MOND review (Jan 2025) | https://arxiv.org/abs/2501.17006 | Comprehensive |

**What would solving it mean.** Either a relativistic MOND that passes GW170817, reproduces CMB, and explains clusters -- or a DM model that naturally produces the RAR and Baryonic Tully-Fisher Relation without galaxy-by-galaxy halo tuning.

---

### 33. Flyby Anomaly

**What it is.** Several spacecraft show unexplained velocity changes (mm/s scale) during Earth gravity assists, correlating with geocentric latitude. Some flybys show clear anomalies, others show none. Anderson's empirical formula fits some cases but not all. Upcoming: Europa Clipper (Dec 2026) and JUICE (Sep 2026) Earth flybys.

**Status:** Tentative

**Key numbers**

| Flyby | Anomaly |
|---|---|
| Galileo I (1990) | +3.92 mm/s |
| NEAR (1998) | +13.46 mm/s |
| Cassini (1999) | -2 mm/s |
| Rosetta I (2005) | +1.82 mm/s |
| MESSENGER (2005) | +0.02 mm/s (equatorial) |
| Juno (2013) | No anomaly |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Anderson et al. | https://arxiv.org/abs/0809.4351 | Original compilation |
| JPL Horizons | https://ssd.jpl.nasa.gov/horizons/ | Ephemeris comparison |

**What would solving it mean.** A model predicting the anomalous velocity for all flybys (including null results) from first principles, handling the latitude dependence.

---

### 34. Gravitational Wave Echoes

**What it is.** If post-merger objects have reflective surfaces near the horizon (exotic compact objects), GW echoes should appear in post-merger ringdown. Abedi et al. (2017) claimed marginal evidence (~2.5 sigma) in LIGO O1. The LVK O3 search (2023) found no echoes. GW250114 (SNR ~77-80) confirmed standard GR ringdown.

**Status:** Controversial (no detection)

**Key numbers**

| Quantity | Value |
|---|---|
| Abedi et al. (2017) claimed p-value | ~0.004, reduced on reanalysis |
| LVK O3 search (2023) | Consistent with noise |
| GW250114 (Jan 2025) | Clean ringdown, first overtone at 4.1 sigma, no echoes |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| GWOSC | https://gwosc.org/ | Open GW data |
| O3 echo search | https://arxiv.org/abs/2309.01894 | LVK systematic search |
| Original claim | https://arxiv.org/abs/1612.00266 | Abedi et al. |
| Python: `gwpy`, `pycbc`, `bilby` | pip install gwpy pycbc bilby | GW analysis |

**What would solving it mean.** Either a >5 sigma detection of periodic post-merger echoes, or demonstrated null at sufficient sensitivity to rule out all reasonable ECO models.

---

### 35. Quantum Gravity Phenomenology Gap

**What it is.** The Planck scale (~10^19 GeV) is 15 orders of magnitude above the LHC (~10^4 GeV). Several indirect probes exist: CMB B-modes (r < 0.036), Lorentz invariance violation (Fermi-LAT constrains E_LIV > 10^19 GeV for linear dispersion), GQuEST (targeting holographic fluctuations at ~10^-18 m), and gravity-induced entanglement experiments.

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Planck energy | ~1.22 x 10^19 GeV |
| LHC energy | ~1.4 x 10^4 GeV |
| LIV bound (Fermi-LAT, linear) | E_LIV,1 > 9.3 x 10^19 GeV |
| Tensor-to-scalar ratio bound | r < 0.036 (95% CL) |
| GQuEST target sensitivity | ~10^-18 m |
| LiteBIRD launch | JFY 2032 |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Fermi-LAT data | https://fermi.gsfc.nasa.gov/ssc/data/access/ | GRB timing for LIV |
| BICEP/Keck | https://bicepkeck.org/ | CMB B-mode data |
| Simons Observatory | https://simonsobservatory.org/ | Next-gen CMB |
| GWOSC | https://gwosc.org/ | GW ringdown QG tests |
| GQuEST | https://gquest.fnal.gov/ | Holographic noise search |
| Python: `gammapy` | pip install gammapy | Fermi-LAT analysis |

**What would solving it mean.** Detection of primordial B-modes, holographic spacetime noise, gravity-induced entanglement, or Planck-scale Lorentz violation. Any one would be transformative.

---

### 36. GW170817 vs Modified Gravity

**What it is.** GW170817 (binary neutron star merger) arrived 1.7 seconds before GRB170817A from 40 Mpc away, constraining |c_gw/c - 1| < 5 x 10^-16. This eliminated entire classes of modified gravity dark energy models (most Horndeski, beyond-Horndeski, massive gravity variants).

**Status:** Established

**Key numbers**

| Quantity | Value |
|---|---|
| Speed constraint | |c_gw/c - 1| < 5 x 10^-16 |
| Graviton mass bound | m_g < 9.52 x 10^-22 eV/c^2 |
| Time delay | 1.74 +/- 0.05 seconds |
| Source distance | ~40 Mpc |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| GW170817 strain data | https://gwosc.org/events/GW170817/ | Open data |
| Multi-messenger paper | https://arxiv.org/abs/1710.05834 | Abbott et al. 2017 |
| Speed of gravity paper | https://arxiv.org/abs/1710.05835 | Abbott et al. 2017 |
| GRB170817A (Fermi GBM) | https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/ | Gamma-ray data |

**What would solving it mean.** For modified gravity theorists: construct a theory explaining cosmic acceleration without Lambda that maintains c_gw = c exactly and passes all other gravitational tests.

---

### 37. Unruh Effect

**What it is.** An accelerating observer should detect thermal radiation at T = hbar a / (2 pi c k_B). Theoretically established from standard QFT. Never directly detected due to extreme accelerations needed. New proposals (2025): Josephson junctions, accelerated atoms between mirrors, trapped ion analogs, CERN-NA63 channeling.

**Status:** Established (theoretically). Undetected experimentally.

**Key numbers**

| Quantity | Value |
|---|---|
| Unruh temperature | ~4 x 10^-23 K per m/s^2 |
| To reach 1 K | Need a ~ 2.5 x 10^22 m/s^2 |
| Josephson junction proposal | Effective T of ~few K achievable |
| CERN-NA63 channeling | Electron accelerations ~10^25 m/s^2 |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Unruh (1976) | Phys. Rev. D 14, 870 | Original prediction |
| Trapped ion simulation | https://arxiv.org/abs/2510.23050 | Analog approach |
| Review: Crispino et al. | Rev. Mod. Phys. 80, 787 (2008) | Comprehensive |

**What would solving it mean.** Direct detection of thermal radiation at the predicted temperature from an accelerating detector (or rigorous analog confirmation), ruling out systematic effects.

---

### 38. Hawking Radiation

**What it is.** Black holes emit thermal radiation at T_H = hbar c^3 / (8 pi G M k_B). For solar-mass BHs, T_H ~ 6 x 10^-8 K -- utterly undetectable. Confirmed in BEC and superconducting circuit analogs. Primordial BHs of mass ~10^14-10^15 g would be evaporating now with detectable gamma rays. No confirmed detection.

**Status:** Established (theoretically). Analog-confirmed. Not detected from astrophysical BHs.

**Key numbers**

| Quantity | Value |
|---|---|
| T_H (solar mass) | ~6 x 10^-8 K |
| T_H (10^12 kg primordial BH) | ~10^11 K |
| Power (solar mass) | ~10^-29 W |
| PBH evaporation threshold | M ~ 5 x 10^14 g |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| BEC analog (Steinhauer) | https://www.nature.com/articles/nphys3863 | Correlated phonon pairs |
| Circuit analog (2023) | https://www.nature.com/articles/s41467-023-39064-6 | Superconducting circuit |
| PBH gamma-ray searches | https://fermi.gsfc.nasa.gov/ssc/data/access/ | Fermi-LAT |
| PBH constraints review | https://arxiv.org/abs/2002.12778 | Carr et al. 2021 |

**What would solving it mean.** Detect PBH gamma rays matching Hawking spectrum, or increasingly precise analog experiments testing beyond the thermal spectrum (entanglement structure, greybody factors).

---

### 39. Pioneer Anomaly (Resolved)

**What it is.** Pioneer 10/11 showed anomalous sunward acceleration of ~8.74 x 10^-10 m/s^2 from 1980-2002. Resolved by Turyshev et al. (2012): anisotropic thermal radiation from RTGs accounts for 100% of the anomaly. Time dependence matches Pu-238 decay.

**Status:** Resolved

**Key numbers**

| Quantity | Value |
|---|---|
| Anomalous acceleration | (8.74 +/- 1.33) x 10^-10 m/s^2 |
| Explanation | Thermal recoil (100% accounted) |

**Data sources**

| Resource | URL | Notes |
|---|---|---|
| Resolution paper | https://arxiv.org/abs/1204.2507 | Turyshev et al. 2012 |
| JPL Horizons | https://ssd.jpl.nasa.gov/horizons/ | Ephemeris data |

**Agents: do not spend time on this. It is solved.**

---

## Foundational / Theoretical

The Quantum Measurement Problem (#27) and Arrow of Time (#30) are listed above in their respective sections but are fundamentally theoretical/foundational problems. Similarly, the Problem of Time (#31), Black Hole Information Paradox (#28), and Black Hole Singularities (#29) sit at the intersection of gravity and foundational physics. They are grouped with Gravity & Spacetime for organizational purposes.

---

## Cross-Cutting Data Resources

| Resource | URL | Python Package | Coverage |
|---|---|---|---|
| Planck Legacy Archive | https://pla.esac.esa.int/ | `healpy`, `camb`, `cobaya` | CMB maps, spectra, likelihoods |
| NASA LAMBDA | https://lambda.gsfc.nasa.gov/ | -- | All CMB mission data |
| GWOSC | https://gwosc.org/ | `gwpy`, `pycbc` | GW strain, event catalogs |
| PDG | https://pdg.lbl.gov/ | `pdg`, `particle` | Particle properties, reviews |
| HEPData | https://www.hepdata.net/ | -- | Published HEP data tables |
| CERN Open Data | https://opendata.cern.ch/ | `pyhf` | LHC collision data |
| MAST (STScI) | https://mast.stsci.edu/ | -- | JWST, HST data |
| DESI | https://data.desi.lbl.gov/ | -- | BAO, galaxy spectra |
| SDSS | https://www.sdss.org/ | `astroquery.sdss` | Galaxy spectra, photometry |
| Fermi-LAT | https://fermi.gsfc.nasa.gov/ssc/data/access/ | `gammapy` | Gamma-ray data |
| SPARC | https://astroweb.case.edu/SPARC/ | `pygrc` | Rotation curves |
| EHT | https://eventhorizontelescope.org/ | `ehtim` | BH shadow images |
| CosmoVerse Tensions | https://cosmoversetensions.eu/ | -- | Tensions database |
| VizieR | https://vizier.cds.unistra.fr/ | `astroquery` | Cross-catalog access |

---

*Note on sigma levels: 3 sigma (~99.7%) is "evidence," 5 sigma (~99.99994%) is "discovery." Many tensions above are 2-4 sigma, where history shows a substantial fraction are statistical fluctuations or systematic errors.*
