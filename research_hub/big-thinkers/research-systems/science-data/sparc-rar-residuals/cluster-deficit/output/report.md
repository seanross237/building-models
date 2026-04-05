# MOND Cluster Deficit: Universal or Variable?

## Short Answer

Not as a single global number. The literature points to a **split picture**:

- **Clusters do not lie on the same universal RAR as galaxies.** Direct cluster-RAR papers find either a different acceleration scale or large scatter: Tian et al. 2020 found a tight CLASH cluster RAR, but with \(g_\ddagger = (2.02 \pm 0.11)\times 10^{-9}\,\mathrm{m\,s^{-2}}\), about 17 times the galaxy scale \(g_\dagger\), so it is **not** the same RAR as galaxies. Chan & Del Popolo 2020 and Chan & Law 2022 found **large scatter** and concluded the cluster relation is not universal. Mistele et al. 2025 found that cluster offsets from the galaxy RAR depend strongly on **outer gas-mass extrapolation**.
- **Inside the inner \(\sim\)Mpc, some lensing analyses do show an approximately universal residual MOND component.** Famaey et al. 2025 found a “remarkable uniformity” in 16 CLASH clusters: the missing-to-hot-gas density ratio is of order 10 with a cutoff radius of order 400 kpc.

So the best current answer is: **no universal cluster deficit factor overall; partial inner-profile universality in gas-rich inner regions.**

## What the Literature Shows

### 1. Cluster RAR papers

- **Tian et al. 2020** constructed a direct CLASH cluster RAR for 20 high-mass clusters and found a power law with intrinsic scatter \(14.7^{+2.9}_{-2.8}\%\), but with a much higher acceleration scale than galaxies. That means **clusters are offset from the galaxy RAR**, not simply extensions of it.  
  Source: https://arxiv.org/abs/2001.08340
- **Chan & Del Popolo 2020** used 52 non-cool-core X-ray clusters and found the cluster RAR scatters over a large parameter space, arguing the RAR is unlikely to be universal across galaxies and clusters.  
  Source: https://arxiv.org/abs/2001.06141
- **Chan & Law 2022** similarly found large scatter in the central cluster relation and concluded its functional form differs from the galaxy RAR.  
  Source: https://arxiv.org/abs/2203.15217
- **Mistele et al. 2025** found that CLASH clusters systematically deviate from the galaxy BTFR/RAR, but the offset depends strongly on the assumed gas profile at large radii; with a suitable extra positive baryonic component, clusters may move closer to the galaxy relations.  
  Source: https://arxiv.org/abs/2506.13716

### 2. Best current evidence on variability

- **Kelleher & Lelli 2024** is the cleanest direct cluster-by-cluster MOND-deficit paper I found. For five X-COP clusters, the inferred missing-to-baryon mass ratio at the outer measured radius is:
  - Relaxed clusters: A1795 1.10, A2029 0.61, A2142 0.38
  - Merger-signature clusters: A644 5.43, A2319 3.99
  These are their preferred “with EFE” values. The relaxed-cluster median is **0.61**; the merging-cluster median is **4.71**. In this tiny sample, dynamical state is the strongest trend.  
  Source: https://arxiv.org/abs/2405.08557
- **Famaey, Pizzuti & Saltas 2025** studied 16 CLASH clusters with lensing. Using their inner-profile proxy, I get:
  - \(\delta M/M_{\rm gas}\): median **1.40**, scatter **0.167 dex**
  - \(\eta = \rho_{\rm missing}/\rho_{\rm hot\,gas}\): median **10.97**, scatter **0.178 dex**
  This is fairly tight, but **not** at the galaxy-RAR level of 0.1 dex. In the transcribed table, \(\eta\) shows a mild anti-correlation with total cluster mass (\(\rho=-0.59\), \(p=0.016\)); Famaey et al. themselves describe a slight increase in the ratio toward lower gas-mass clusters.  
  Source: https://arxiv.org/abs/2410.02612

## Assessment

### Is the deficit universal?

**Globally no.** The direct scalar-deficit evidence varies from about **0.4 to 5.4** even within a single modern X-COP analysis, and the cluster RAR offset itself depends on baryon-model choices at large radii. A single universal factor of 2 is too simple.

### What does it correlate with most strongly?

The strongest current evidence is for **dynamical state** in the X-COP sample: relaxed clusters need much less extra MOND mass than disturbed ones. In the lensing-based CLASH sample, the inner density-ratio proxy is fairly uniform and shows at most a **mild mass or gas-mass dependence**, not a strong temperature trend.

### Can ordinary neutrinos close the gap?

For a universal factor of only \(\sim 2\), the attractive idea would be standard active neutrinos with \(\Sigma m_\nu \sim 0.15\) to \(0.3\) eV. But the cluster literature does **not** support that as a full solution:

- **Pointecouteau & Silk 2005** found MOND still needs \(M_m/M_b = 4.94 \pm 0.50\) around \(0.5R_{\rm vir}\), implying a minimum neutrino mass \(m_\nu > 1.74 \pm 0.34\) eV per species to fill the gap.  
  Source: https://arxiv.org/abs/astro-ph/0505017
- **Sanders 2003** argued for active neutrinos of order **2 eV**.  
  DOI trail via arXiv reference in later MOND reviews: https://doi.org/10.1046/j.1365-8711.2003.06227.x
- **KATRIN 2024/2025** now gives \(m_\nu < 0.45\) eV at 90% CL, excluding that active-neutrino fix.  
  Source: https://arxiv.org/abs/2406.13516

So **standard active neutrinos at 0.15-0.3 eV are too light**, and the older \(\sim 2\) eV active-neutrino MOND fix is now ruled out by direct lab data.

### What about sterile neutrinos or cosmology-dependent limits?

- In \(\Lambda\)CDM-like cosmology, current neutrino-mass bounds are even tighter than 0.12 eV; a recent review notes bounds as strong as **\(\Sigma m_\nu < 0.072\) eV** from Planck+ACT+DESI, though it also emphasizes these are sensitive to data choices and model assumptions.  
  Source: https://cds.cern.ch/record/2906506/files/2407.13831.pdf
- Those cosmological bounds are **not directly transferable to MOND cosmology**, but they certainly do not help a 1-2 eV active-neutrino solution.
- Sterile-neutrino MOND models have been explored, but **Angus et al. 2013** found MOND plus light sterile neutrinos overproduces massive clusters.  
  Source: https://arxiv.org/abs/1309.6094

### Does the required profile look neutrino-like?

Not obviously. Both **Kelleher & Lelli 2024** and **Famaey et al. 2025** argue the residual component must be **more centrally concentrated than the ICM**, with Famaey et al. favoring a cored inner profile and a sharp outer decline. That is not the most natural profile for a hot, diffuse neutrino halo.

## What Would Settle It?

A decisive test would be a **single homogeneous sample** of clusters with:

- weak-lensing total masses,
- deep X-ray + SZ gas profiles to large radius,
- stellar + ICL baryon estimates,
- a common analysis radius such as \(r_{2500}\) or \(0.5R_{200}\),
- and a consistent dynamical-state classification.

Then one could measure one scalar deficit per cluster and ask cleanly whether the residual is a constant, mass-dependent, merger-dependent, or radius-dependent quantity.
