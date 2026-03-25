# Sprint 1: FDCG Oppenheim Prediction — Calculation Results

## Constants Used
- G = 6.67430 x 10^-11 m^3 kg^-1 s^-2
- hbar = 1.054571817 x 10^-34 J s
- G*hbar = 7.0385 x 10^-45 m^5 s^-3

Note: the prompt stated Ghbar = 7.0406e-45, but direct multiplication gives 7.0385e-45. The difference (~0.03%) likely comes from rounding in the prompt. All calculations below use the exact product.

---

## Model Formulas

| Model | Formula for sigma_a | Scaling (uniform sphere) | Free parameters |
|-------|---------------------|--------------------------|-----------------|
| FDCG  | sqrt(G*hbar / R^3)  | R^(-3/2), independent of mass and density | None |
| Diosi-Penrose (DP) | sqrt(6*G*hbar / (5*m*R)) | rho^(-1/2) R^(-2) | None |
| KTM   | sqrt(4*G*hbar / (5*m*R)) | rho^(-1/2) R^(-2) | None |
| Oppenheim continuous | Parameterized by kernel width sigma | Varies | sigma (kernel width) |

Units: sigma_a is acceleration noise spectral density in m/s^2/sqrt(Hz).

FDCG unit verification: [G*hbar/R^3] = m^5 s^-3 / m^3 = m^2 s^-3. sqrt gives m s^(-3/2) = m/s^2/sqrt(Hz). Correct.

---

## Test Masses

| # | Object | R (m) | m (kg) | rho (kg/m^3) |
|---|--------|-------|--------|--------------|
| 1 | C60 fullerene | 3.5e-10 | 1.2e-24 | ~1700 |
| 2 | OTIMA-scale molecule (~20 kDa) | 1.0e-9 | 3.3e-23 | — |
| 3 | Silica nanoparticle | 5.0e-8 | 1.1e-18 | 2200 |
| 4 | Diamond microsphere | 1.0e-6 | 1.47e-14 | 3510 |
| 5 | LISA Pathfinder test mass | 2.3e-2 | 1.928 | — |

---

## Computation: FDCG (sigma_a = sqrt(G*hbar / R^3))

### C60 fullerene (R = 3.5e-10 m)
- R^3 = (3.5e-10)^3 = 4.2875e-29 m^3
- G*hbar/R^3 = 7.0385e-45 / 4.2875e-29 = 1.6416e-16
- sigma_a = sqrt(1.6416e-16) = **1.281e-08 m/s^2/sqrt(Hz)**

### OTIMA-scale molecule (R = 1.0e-9 m)
- R^3 = 1.000e-27 m^3
- G*hbar/R^3 = 7.0385e-45 / 1.000e-27 = 7.0385e-18
- sigma_a = sqrt(7.0385e-18) = **2.653e-09 m/s^2/sqrt(Hz)**

### Silica nanoparticle (R = 5.0e-8 m)
- R^3 = 1.250e-22 m^3
- G*hbar/R^3 = 7.0385e-45 / 1.250e-22 = 5.6308e-23
- sigma_a = sqrt(5.6308e-23) = **7.504e-12 m/s^2/sqrt(Hz)**

### Diamond microsphere (R = 1.0e-6 m)
- R^3 = 1.000e-18 m^3
- G*hbar/R^3 = 7.0385e-45 / 1.000e-18 = 7.0385e-27
- sigma_a = sqrt(7.0385e-27) = **8.390e-14 m/s^2/sqrt(Hz)**

### LISA Pathfinder (R = 2.3e-2 m)
- R^3 = 1.2167e-5 m^3
- G*hbar/R^3 = 7.0385e-45 / 1.2167e-5 = 5.7849e-40
- sigma_a = sqrt(5.7849e-40) = **2.405e-20 m/s^2/sqrt(Hz)**

---

## Computation: Diosi-Penrose (sigma_a = sqrt(6*G*hbar / (5*m*R)))

### C60 fullerene
- m*R = 1.2e-24 * 3.5e-10 = 4.200e-34 kg m
- (6/5) * G*hbar/(m*R) = 1.2 * 7.0385e-45 / 4.200e-34 = 2.011e-11
- sigma_a = **4.484e-06 m/s^2/sqrt(Hz)**

### OTIMA-scale molecule
- m*R = 3.3e-23 * 1.0e-9 = 3.300e-32
- (6/5) * G*hbar/(m*R) = 1.2 * 7.0385e-45 / 3.300e-32 = 2.560e-13
- sigma_a = **5.059e-07 m/s^2/sqrt(Hz)**

### Silica nanoparticle
- m*R = 1.1e-18 * 5.0e-8 = 5.500e-26
- (6/5) * G*hbar/(m*R) = 1.2 * 7.0385e-45 / 5.500e-26 = 1.536e-19
- sigma_a = **3.919e-10 m/s^2/sqrt(Hz)**

### Diamond microsphere
- m*R = 1.47e-14 * 1.0e-6 = 1.470e-20
- (6/5) * G*hbar/(m*R) = 1.2 * 7.0385e-45 / 1.470e-20 = 5.746e-25
- sigma_a = **7.580e-13 m/s^2/sqrt(Hz)**

### LISA Pathfinder
- m*R = 1.928 * 2.3e-2 = 4.434e-2
- (6/5) * G*hbar/(m*R) = 1.2 * 7.0385e-45 / 4.434e-2 = 1.905e-43
- sigma_a = **4.364e-22 m/s^2/sqrt(Hz)**

---

## Computation: KTM (sigma_a = sqrt(4*G*hbar / (5*m*R)))

| Object | sigma_a (KTM) |
|--------|---------------|
| C60 fullerene | 3.662e-06 |
| OTIMA-scale molecule | 4.131e-07 |
| Silica nanoparticle | 3.200e-10 |
| Diamond microsphere | 6.189e-13 |
| LISA Pathfinder | 3.563e-22 |

Note: KTM differs from DP only by a numerical prefactor: sqrt(4/6) = sqrt(2/3) = 0.816.

---

## Master Comparison Table

All sigma_a values in m/s^2/sqrt(Hz).

| Object | R (m) | m (kg) | sigma_a FDCG | sigma_a DP | sigma_a KTM | FDCG/DP ratio |
|--------|-------|--------|-------------|-----------|------------|---------------|
| C60 fullerene | 3.5e-10 | 1.2e-24 | 1.281e-08 | 4.484e-06 | 3.662e-06 | 0.003 |
| OTIMA molecule | 1.0e-09 | 3.3e-23 | 2.653e-09 | 5.059e-07 | 4.131e-07 | 0.005 |
| Silica NP | 5.0e-08 | 1.1e-18 | 7.504e-12 | 3.919e-10 | 3.200e-10 | 0.019 |
| Diamond sphere | 1.0e-06 | 1.47e-14 | 8.390e-14 | 7.580e-13 | 6.189e-13 | 0.111 |
| LISA PF | 2.3e-02 | 1.928 | 2.405e-20 | 4.364e-22 | 3.563e-22 | 55.1 |

---

## Experimental Sensitivity Comparison

| Object | sigma_a FDCG | Best sigma_exp | FDCG/sigma_exp | Detectable? | Source |
|--------|-------------|----------------|----------------|-------------|--------|
| C60 fullerene | 1.281e-08 | N/A (interferometry) | — | Decoherence only | Matter-wave experiments |
| OTIMA molecule | 2.653e-09 | N/A (interferometry) | — | Decoherence only | OTIMA |
| Silica NP (current) | 7.504e-12 | ~1e-09 | 0.0075 | NO (133x below) | Levitated optomechanics |
| Silica NP (MAQRO) | 7.504e-12 | ~1e-15 | 7500 | YES (7500x above) | MAQRO space mission |
| Diamond sphere | 8.390e-14 | ~1e-15 (proposed) | 84 | YES (84x above) | Bouwmeester proposal |
| LISA PF | 2.405e-20 | 5.2e-15 (achieved) | 4.6e-06 | NO (5 OOM below) | LISA Pathfinder (2016) |

---

## Analysis

### A. Is FDCG distinguishable from DP?

**YES, decisively.** The models have fundamentally different scaling laws:

- **FDCG: sigma_a proportional to R^(-3/2)** — depends ONLY on radius R, completely independent of mass m and density rho.
- **DP: sigma_a proportional to (m*R)^(-1/2)** — depends on both mass and radius. For uniform spheres of fixed density, this becomes R^(-2).
- **KTM:** Same scaling as DP (differs only by prefactor sqrt(2/3) = 0.816).

The FDCG/DP ratio varies from 0.003 (at fullerene scale) to 55 (at LISA PF scale). This is not a constant — the two models are structurally different, not just rescaled versions of each other.

**Key physical difference:** FDCG predicts that gravitational fluctuations depend only on the geometry of the region of space being probed (the radius R), not on the mass probing it. This is because in FDCG, the noise arises from vacuum fluctuations of the fracton dipole condensate, which are a property of spacetime itself, not of matter.

### B. Crossover Point

Setting sigma_a(FDCG) = sigma_a(DP) for a uniform sphere (m = 4pi*rho*R^3/3):

    R_cross = 9 / (10*pi*rho)

| Material | rho (kg/m^3) | R_cross |
|----------|-------------|---------|
| Silica | 2200 | 0.130 mm |
| Diamond | 3510 | 0.082 mm |

- For R < R_cross: FDCG predicts LESS noise than DP (harder to detect, but also means DP is ruled out first).
- For R > R_cross: FDCG predicts MORE noise than DP.

### C. Where Are Experiments Closest to FDCG?

**The diamond microsphere (R ~ 1 um) with Bouwmeester-type experiments is the sweet spot.**

- FDCG prediction: 8.39e-14 m/s^2/sqrt(Hz)
- Proposed experimental sensitivity: ~1e-15 m/s^2/sqrt(Hz)
- SNR = 84: the FDCG signal would be 84 times above the noise floor.

The proposed MAQRO space mission for nanoparticles (R ~ 50 nm) would also be excellent:
- FDCG prediction: 7.50e-12 m/s^2/sqrt(Hz)
- MAQRO target sensitivity: ~1e-15 m/s^2/sqrt(Hz)
- SNR = 7500: overwhelmingly detectable.

For current levitated nanoparticle experiments, FDCG is about 133x below sensitivity — not yet detectable but within reach of near-term improvements.

### D. Definitive Test for FDCG

The critical diagnostic: **measure sigma_a for objects of the same radius R but different masses m.**

- Example: silica (rho=2200) vs diamond (rho=3510) nanoparticles, both R = 50 nm
- FDCG predicts: sigma_a(silica) = sigma_a(diamond) = 7.504e-12 m/s^2/sqrt(Hz) (identical)
- DP predicts: sigma_a(silica) = 3.829e-10, sigma_a(diamond) = 3.032e-10 (ratio 1.263)

If the noise is the same for both materials at the same size, that is uniquely FDCG.

Alternative diagnostic: **measure sigma_a at two radii of the same material.**
- FDCG predicts sigma_a(R1)/sigma_a(R2) = (R2/R1)^(3/2)
- DP predicts sigma_a(R1)/sigma_a(R2) = (R2/R1)^2
- For a factor-of-10 size change: FDCG predicts 31.6x change, DP predicts 100x change.

### E. What Radius Is Detectable at a Given Sensitivity?

Solving sigma_a(FDCG) = sigma_exp for R:

    R = (G*hbar / sigma_exp^2)^(1/3)

| Sensitivity level | sigma_exp | R_detect |
|-------------------|-----------|----------|
| Current levitated NP | 1e-09 | 1.9 nm |
| 10x improved | 1e-10 | 8.9 nm |
| Bouwmeester/MAQRO | 1e-15 | 19 um |
| LISA PF achieved | 5.2e-15 | 6.4 um |

This means any experiment reaching 1e-15 m/s^2/sqrt(Hz) sensitivity on an object smaller than ~19 um would see the FDCG signal.

---

## Summary Verdict

**PASS.** FDCG occupies a unique, distinguishable region of prediction space:

1. **Different scaling law** (R^(-3/2) vs R^(-2) for DP/KTM) — structurally different, not just a rescaling.
2. **Mass-independent** — FDCG's noise depends only on R, providing a clean experimental signature (vary mass at fixed R).
3. **Experimentally accessible** — Bouwmeester-type microsphere experiments at R~1um with sensitivity ~1e-15 m/s^2/sqrt(Hz) would see the signal with SNR~84. The proposed MAQRO space mission would see it with SNR~7500.
4. **Already constrainable** — Current levitated nanoparticle experiments are only ~133x away from the FDCG prediction at R=50nm.
5. **Importantly, FDCG predicts less noise than DP for small objects.** Since parameter-free DP is already experimentally ruled out (Donadi et al. 2021), FDCG remains viable. FDCG's smaller prediction at small R means it evades the constraints that killed DP.

The fact that FDCG is mass-independent is its most distinctive feature. No other gravitational decoherence model predicts this. It is a direct consequence of the noise being a property of spacetime geometry (the condensate vacuum), not of the matter coupling to gravity.
