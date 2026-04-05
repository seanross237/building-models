---
topic: Numerical classicality budget across physical scales
confidence: verified
date: 2026-03-27
source: "classicality-budget strategy-001 exploration-002"
---

## Result

Numerical computation of R_delta <= (S_max / S_T) - 1 across 7 physical systems spanning Planck to cosmological scales. Budget spans ~122 orders of magnitude. All 7 sanity checks passed.

## Summary Table (S_T = 1 bit)

| System | S_max (bits) | Tighter Bound | R_delta | log10(S_max) |
|--------|-------------|---------------|---------|-------------|
| Lab (1m, 1 kg) | 1.29 x 10^43 | Bekenstein | 1.29 x 10^43 | 43.1 |
| Human brain (1.4 kg) | 2.50 x 10^42 | Bekenstein | 2.50 x 10^42 | 42.4 |
| Near BH (1 kg at 2r_s) | 7.61 x 10^46 | Bekenstein | 7.61 x 10^46 | 46.9 |
| Solar-mass BH | 1.51 x 10^77 | Both (equal) | 1.51 x 10^77 | 77.2 |
| Observable universe | 1.13 x 10^123 | Bekenstein | 1.13 x 10^123 | 123.1 |
| Planck-scale region | 4.53 | Holographic | 3.53 | 0.66 |
| QC (1000 qubits) | 2.58 x 10^19 | Bekenstein | 2.58 x 10^19 | 19.4 |

## Key Physical Insights

### Bekenstein always tighter for non-gravitational systems
For every system except the Planck-scale region, the Bekenstein bound determines S_max. The holographic bound is typically 25-50 orders of magnitude larger. The two bounds coincide ONLY for black holes (analytically: both equal 4*pi*G*M^2/(hbar*c) when R = r_s). The classicality budget for ordinary matter is determined by energy content, not surface area.

### Budget only constraining at Planck scale
For all macroscopic systems, R_delta ~ 10^42 to 10^123 — trivially satisfied. The classicality budget provides no useful constraint for everyday physics. It only becomes physically tight at the Planck scale (see planck-scale-classicality-breakdown.md).

### Empty space has zero budget
If E = 0, then S_Bek = 0, so R_delta = -1 for any S_T > 0. No classical reality is possible in truly empty space. Even a single photon (E ~ 1 eV) in 1 m^3 gives S_Bek ~ 2.3 x 10^7 bits. Classical facts require matter/energy to encode and transmit them.

### Observable universe entropy bounds nearly coincide
S_Bek/S_holo ~ 0.34 — within a factor of 3. Reflects the cosmic coincidence that the Schwarzschild radius of the universe's mass (~10^26 m) is comparable to the Hubble radius (~10^26 m). Cosmological application of Bekenstein bound is contested; Bousso covariant bound is more appropriate but gives same order of magnitude (~10^123).

### Holographic bound gives pi nats per Planck area, not "1 bit"
The exact value at R = l_P is pi/ln(2) ~ 4.53 bits. The informal "1 bit per Planck area" is approximate by a factor of ~4.5.

### Brain budget dwarfs neural complexity
Bekenstein bound (~10^42 bits) exceeds neural complexity (~10^11 neurons, ~10^14 synapses) by ~28 orders of magnitude. Even with 10^11 distinct neural facts, R_delta ~ 10^31 per fact. Caveat: thermally accessible entropy (~10^25 bits) is more operationally relevant and still vastly exceeds neural information capacity.

## Operational Bekenstein vs. Actual Bekenstein

The Bekenstein bound counts ALL physical degrees of freedom. Quantum Darwinism requires encoding in accessible environment (photons, air molecules, etc.). A more operationally relevant S_max might be thermal/environmental entropy, which is typically 17+ orders of magnitude below Bekenstein. The qualitative picture doesn't change for macroscopic systems but may matter near the boundary.

## Reproducibility

All computations in Python with numpy/scipy. Scripts, results.json, and plots saved to exploration code/ directory.
