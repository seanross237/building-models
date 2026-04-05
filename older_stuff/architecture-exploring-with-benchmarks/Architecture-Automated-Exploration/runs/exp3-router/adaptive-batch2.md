# Adaptive Batch 2 — Difficulty-Adaptive Pipeline Results

**Model:** Claude Opus 4.6 (1M context)
**Date:** 2026-03-28
**Questions:** Q7-Q11 (3 computation, 2 discrimination... correction: 2 computation, 3 discrimination)

---

## Summary Table

| Q | Type | Difficulty | Initial Answer | Verified? | Final Answer |
|---|------|-----------|----------------|-----------|-------------|
| Q7 | COMPUTATION (C1) | HARD | Z diverges (condensation) | 3 approaches, all diverge | **Series diverges; system above BET condensation threshold. With k_max=5 truncation: Z~9.87, <k>~2.96** |
| Q8 | COMPUTATION (C1) | HARD | <n>=0.848 | 3 approaches; sign-convention resolved; particle-hole symmetry confirmed | **<n> = 0.848** |
| Q9 | DISCRIMINATION (D2) | MEDIUM | C | All options tested; A,E contradicted; B contradicted by multiplex CARS physics | **C** |
| Q10 | DISCRIMINATION (D2) | MEDIUM | D | All options tested; A,B,C,E,F are known coarsening-gas effects; D is anomalous | **D** |
| Q11 | DISCRIMINATION (D2) | HARD | D | 3 approaches (tolerance factor, literature, experimental confirmation) | **D** |

---

## Detailed Solutions

### Q7 [COMPUTATION] — Multilayer Adsorption, Grand Canonical Mean-Field

**Difficulty: HARD** — Ambiguous notation, multiple possible interpretations, divergence issues.

**C1 Plan — Sign Conventions:**
- eps_1 = 0.1 k_BT: first-layer binding energy (positive = attractive = lowers energy)
- eps_l = (0.02)^l k_BT for l >= 2: upper-layer binding energies (exponentially decaying)
- mu = 0.15 k_BT: chemical potential (positive = favors adsorption)
- z_l = 4 (lateral), z_inter = 4 (interlayer): coordination numbers
- T = 318 K

**Approach 1: Direct partition function (exponential eps_l)**

Single-site grand partition function:
Z = sum_{n=0}^{k_max} w(n)

where w(n) = exp(n*mu + eps_1 + sum_{l=2}^{n} (0.02)^l) for n >= 1, w(0) = 1.

Problem: The incremental Boltzmann factor for each additional layer is ~exp(0.15) = 1.162 > 1 for all l >= 3 (since eps_l = 0.02^l ~ 0 for large l, and mu = 0.15 dominates). The series DIVERGES.

**Approach 2: Cost interpretation**

Treating eps as energy costs (unfavorable): w(n) = exp(n*mu - eps_1 - sum eps_l). Still diverges because n*mu grows linearly while sum eps_l is bounded.

**Approach 3: BET-like constant upper-layer energy**

If eps_l = 0.02 k_BT (constant, not exponential): incremental factor = exp(mu + eps_l) = exp(0.17) > 1. Still diverges.

**Diagnosis:** With mu = 0.15 k_BT > 0, the chemical potential always dominates the (vanishingly small) upper-layer energies. The system is above the BET condensation point, meaning infinite multilayer growth. This is physically meaningful: it represents supersaturation conditions.

The mean-field lateral/interlayer interactions (z_l=4, z_inter=4) should provide self-consistent corrections, but without a specified lateral interaction energy separate from the layer binding energies, this cannot be resolved.

**Truncated result (k_max = 5):**
- Z = 9.866
- <k> = 2.963

Individual weights: w(0)=1.000, w(1)=1.284, w(2)=1.492, w(3)=1.734, w(4)=2.015, w(5)=2.341

**NOTE:** This problem appears underspecified. The divergence is physical (condensation), and a rigorous answer requires either (a) a finite k_max, (b) separate lateral interaction energies for mean-field self-consistency, or (c) a different interpretation of the energy parameters.

---

### Q8 [COMPUTATION] — 2D Lattice Gas, Mean-Field

**Difficulty: HARD** — Subtle double-counting issue explicitly flagged; sign conventions critical.

**C1 Plan — Sign Conventions:**
- eps = -(k_BT)/(2pi): NEGATIVE pair interaction energy (attractive)
- |eps| = k_BT/(2pi) = 0.15915 k_BT: magnitude of coupling
- mu = 0.1 k_BT: chemical potential
- z_horizontal = 4, z_vertical = 8: z_total = 12
- T = 300 K
- Single occupancy per site (n_i = 0 or 1)

**Hamiltonian:** H = sum_{<ij>} eps * n_i * n_j - mu * sum_i n_i
(sum over bonds counts each bond once; eps < 0 makes occupied neighbors energetically favorable)

**Approach 1: Weiss mean-field (no 1/2 in self-consistency)**

For site i with z neighbors, replace n_j -> <n>:
- Effective energy of occupied site: z * eps * <n> = z * (-|eps|) * <n>
- Grand canonical weight: exp(-beta * [z*eps*<n> - mu]) = exp(beta * [z*|eps|*<n> + mu])
- Self-consistency: <n> = 1/(1 + exp(-(z*|eps|*<n>/k_BT + mu/k_BT)))

Iterating from <n>=0.5: converges to **<n> = 0.848**

**Approach 2: With 1/2 in self-consistency**

<n> = 1/(1 + exp(-((z/2)*|eps|*<n>/k_BT + mu/k_BT)))

Converges to <n> = 0.679

**Approach 3: Sign verification via particle-hole symmetry**

At the particle-hole symmetric point, <n> must equal 0.5. For the no-1/2 formula:
mu_half = -z*|eps|/2 = -0.9549 k_BT gives <n> = 0.500000 exactly. Confirmed.

**Which is correct — 1/2 or no 1/2?**

The self-consistency equation computes the conditional distribution of a single site given the mean field from its z neighbors. Each of the z neighbors contributes a field of |eps|*<n> to site i. There is NO double-counting at the single-site level because we are computing the probability of ONE site being occupied, not the total system energy.

The 1/2 factor is only needed when computing the TOTAL mean-field free energy F = -(k_BT/2) * z * |eps| * <n>^2 * N + ..., to avoid counting each bond twice.

This is the standard Bragg-Williams / Weiss result, and is confirmed by the particle-hole symmetry check.

**Verification:**
- Dimensions: all energies in units of k_BT. Consistent.
- Sign: attractive interactions + positive mu -> <n> > 0.5. Confirmed (0.848).
- Limiting case: at mu=0, <n> > 0.5 due to attractive interactions. Confirmed (0.830).
- No phase transition: z*|eps|/k_BT = 1.91 < 4 (mean-field critical coupling). Unique solution confirmed (all initial conditions converge to same fixed point).

**Final answer: <n> = 0.848**

---

### Q9 [DISCRIMINATION] — Broadband CARS Microscopy

**Difficulty: MEDIUM** — Requires CARS spectroscopy knowledge, but D2 elimination is clean.

**D2 Analysis — Assume each option true, find contradictions:**

**Option A: "You can only generate a Stokes beam"**
- CONTRADICTION: CARS (Coherent Anti-Stokes Raman Scattering) by definition generates an anti-Stokes signal at omega_AS = 2*omega_p - omega_S. A broadband pump changes the spectral properties but does not prevent anti-Stokes generation. Eliminated.

**Option B: "You can generate an anti-Stokes beam, but it doesn't contain separate vibrational information"**
- CONTRADICTION: In broadband CARS / multiplex CARS, a broadband source can simultaneously serve as pump and Stokes (the red edge acts as Stokes, blue edge as pump). The anti-Stokes signal at different frequencies maps to different vibrational resonances (omega_vib = omega_p - omega_S). Spectral dispersion of the anti-Stokes band recovers the vibrational spectrum. This is the basis of multiplex CARS microscopy. Eliminated.

**Option C: "You can generate an anti-Stokes beam that contains distinguishable information"**
- No contradiction found. Consistent with the physics of multiplex/broadband CARS where different vibrational modes produce spectrally separated anti-Stokes signals.

**Option D: "None of the above"**
- Would require A, B, and C all false. But C has no contradiction, so D is eliminated.

**Option E: "You cannot generate an anti-Stokes beam"**
- CONTRADICTION: Same as Option A reasoning. CARS always generates anti-Stokes photons via four-wave mixing. Eliminated.

**Verification:** The physics is clear: broadband pump CARS (also called multiplex CARS) is a well-established technique. The broadband pump provides multiple frequency pairs that drive different vibrational coherences simultaneously. The resulting anti-Stokes spectrum is spectrally resolved and contains distinct vibrational information. This confirms C.

**Final answer: C**

---

### Q10 [DISCRIMINATION] — Coarsening Gas During Ceramic Sintering

**Difficulty: MEDIUM** — Requires ceramic processing knowledge; systematic D2 elimination works well.

Background: During sintering of ceramic oxides, volatile impurities (e.g., chloride) generate gas species (HCl, Cl2). These gases can become trapped in closed pores, creating internal pressure that opposes sintering forces and drives pore coarsening (Ostwald ripening of gas-filled pores).

**D2 Analysis:**

**Option A: "Higher heating rates -> lower sintered densities"**
- Known coarsening gas effect: faster heating = less time for gas to escape through open porosity before pore closure = more trapped gas = lower final density. NO contradiction.

**Option B: "De-densification under some atmospheres"**
- Known effect: gas pressure in closed pores can exceed sintering driving force at high T, causing pore GROWTH and density decrease. Well-documented in He and other low-solubility atmospheres. NO contradiction.

**Option C: "Large, randomly distributed voids"**
- Known effect: gas-driven coarsening creates large pores from coalescence/growth of gas-filled pores. These appear as large, randomly distributed voids in the microstructure. NO contradiction.

**Option D: "Larger grain sizes in interior than surface"**
- CONTRADICTION: With coarsening gas, the INTERIOR retains more trapped gas (gas cannot escape as easily as from the surface). More retained porosity in the interior = more grain boundary pinning = SMALLER grains in the interior. The surface loses gas more easily, densifies faster, and undergoes more grain growth. The expected gradient is LARGER grains at the surface, SMALLER in the interior — the opposite of what D claims.

**Option E: "Cracking"**
- Known effect: gas pressure buildup can exceed mechanical strength, causing cracking. NO contradiction.

**Option F: "Higher green densities -> lower sintered densities"**
- Known effect: higher green density = smaller initial pores that close earlier = more gas trapped at lower temperatures = potentially lower sintered densities. This is the "green density paradox" in powder processing. NO contradiction.

**Verification:** A, B, C, E, F are all well-documented effects of coarsening gas during sintering. D describes a grain size gradient (interior > surface) that is the OPPOSITE of what coarsening gas produces.

**Final answer: D**

---

### Q11 [DISCRIMINATION] — Organic A-Site Cations for 3D Lead Halide Perovskites (A-Pb-Br3)

**Difficulty: HARD** — Requires specific materials science knowledge; tolerance factors and experimental literature both needed.

**D2 Analysis + 3 Independent Approaches:**

**Approach 1: Goldschmidt tolerance factor screening**

t = (r_A + r_X) / [sqrt(2) * (r_B + r_X)]

For Pb-Br: r_B = 119 pm (Pb2+), r_X = 196 pm (Br-)
Denominator = sqrt(2) * 315 = 445.5 pm
Valid range: t = 0.8-1.0 => r_A = 160-250 pm

Cation effective radii and tolerance factors:
| Cation | r_eff (pm) | t | Viable? |
|--------|-----------|---|---------|
| Cs+ | 167 | 0.815 | Yes (borderline) |
| MA (CH3NH3+) | 217 | 0.927 | Yes |
| FA (CH(NH2)2+) | 253 | 1.008 | Borderline, confirmed |
| Aziridinium (C2H5NH2+) | ~217 | ~0.93 | Possible |
| Ethylammonium (CH3CH2NH3+) | ~274 | ~1.055 | Too large |
| Methylhydrazinium (CH3NHNH3+) | ~264 | ~1.03 | Borderline |
| Dimethylammonium ((CH3)2NH2+) | ~272 | ~1.05 | Too large |

Ethylammonium (C) and Dimethylammonium (E) are clearly too large. Aziridinium (B) and Methylhydrazinium (D) are both in the viable range.

**Approach 2: Experimental literature**

- MHyPbBr3 (methylhydrazinium lead bromide): Definitively synthesized and characterized as a 3D perovskite by Maczka et al. (Chemistry of Materials, 2020). Confirmed polar 3D perovskite structure with space group Pnm21. This was a high-profile result that expanded the known set of A-site cations.

- AzPbBr3 (aziridinium lead bromide): Predicted to be viable by Kieslich, Sun & Cheetham (2014-2015) based on tolerance factor arguments. Experimental synthesis reports exist but are less widely cited.

**Approach 3: Discrimination between B and D**

Both B (Aziridinium) and D (Methylhydrazinium) appear in the viable tolerance factor range, and both have some experimental support. However:

1. The Maczka group's work on MHyPbBr3 is one of the most cited and definitive demonstrations of a "new" A-site cation beyond MA/FA for 3D perovskites.
2. Methylhydrazinium's success was notable precisely because it pushed past the traditional tolerance factor limit, driven by favorable hydrogen bonding patterns.
3. The question asks for cations that "can independently form 3D lead halide perovskite structures" — MHyPbBr3 is unambiguously confirmed to do this.

If both Az and MHy truly form 3D perovskites, no single answer option is "comprehensive." However, MHyPbBr3 has stronger experimental confirmation as a standalone 3D perovskite.

**Final answer: D (Cs, MA, FA, Methylhydrazinium)**

---

## Difficulty Assessment Notes

- Q7 (HARD): The problem notation is genuinely ambiguous (eps_l = (0.02)^k could mean several things), and the series diverges under most reasonable interpretations. Mean-field self-consistency cannot be completed without additional information (separate lateral interaction energy). Problem appears underspecified.
- Q8 (HARD): The sign convention and 1/2-factor issue required very careful derivation. Three different formulations gave three different answers until signs were fully resolved. Particle-hole symmetry provided a definitive check. Confidence: HIGH.
- Q9 (MEDIUM): Clean D2 elimination. The physics of broadband/multiplex CARS is well-established. Confidence: HIGH.
- Q10 (MEDIUM): All effects are textbook except D. Grain size gradient from coarsening gas is clearly surface > interior, not the reverse. Confidence: HIGH.
- Q11 (HARD): Tolerance factor screening narrows to B or D. Literature strongly supports D (MHyPbBr3 is definitively confirmed). Confidence: MODERATE-HIGH.
