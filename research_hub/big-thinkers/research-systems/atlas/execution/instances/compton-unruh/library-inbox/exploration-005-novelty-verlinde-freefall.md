# Exploration 005 — Literature Survey: T_U/T_dS = μ_MOND Identity, Verlinde Comparison, and Free-Fall Objection

## Goal

Literature survey and critical comparison addressing:
1. Whether T_U(a)/T_dS(a) = μ_MOND(a/cH₀) has been published
2. Detailed comparison with Verlinde (2016)
3. The free-fall objection and proposed resolutions
4. Assessment of novelty and distinctness

**Key result from Exploration 004:** The ratio T_U/T_dS = a/√(a²+c²H₀²) is algebraically identical to the standard MOND interpolation function μ(x) = x/√(1+x²) with a₀ = cH₀.

**Temperature definitions:**
- T_U(a) = ℏa/(2πck_B) — standard Unruh temperature
- T_dS(a) = (ℏ/2πck_B)√(a²+c²H₀²) — de Sitter-modified Unruh temperature (Deser & Levin 1997)
- T_GH = (ℏH₀/2πk_B) = T_dS(0) — Gibbons-Hawking temperature

---

## Part 1: Has T_U/T_dS = μ_MOND Been Published?

### 1.1 Milgrom 1999 — The Closest Prior Work

**Paper:** "The modified dynamics as a vacuum effect," Milgrom, M. (1999). *Physics Letters A* 253, 273–279. arXiv:astro-ph/9805346.

**What Milgrom actually said:**
Milgrom was the first (1999) to connect the de Sitter-modified Unruh temperature to MOND. He stated:
> "A constant-acceleration observer in de Sitter universe sees Unruh radiation of temperature T ∝ [a² + a₀²]^(1/2), with a₀ = (Λ/3)^(1/2). The temperature excess over what an inertial observer sees, T(a) − T(0), depends on a in the same way that MOND inertia does."

And crucially (from the Milgrom review):
> "Inertia, which is related to the departure of the trajectory from that of an inertial observer, might be proportional to the temperature difference."

And cautiously:
> "this would reflect on a 'linear', constant-acceleration motion, while circular trajectories will probably behave differently. But the emergence of an expression à la MOND in this connection with the vacuum is very interesting."

**Critical distinction from T_U/T_dS:**

Milgrom uses the temperature DIFFERENCE (excess), not the RATIO:

    Modified inertia ∝ T_dS(a) - T_GH = T_GH × [√(1 + (a/cH₀)²) - 1]

This is NOT the same as T_U/T_dS = a/√(a²+c²H₀²).

For the excess temperature approach:
- For a >> cH₀: excess ~ a (correct Newtonian limit: m_i ∝ a)
- For a << cH₀: excess ~ a²/(2cH₀) (deep-MOND: m_i ∝ a², same qualitative behavior)
- Predicted a₀ = 2cH₀ (factor of 2 discrepancy from our result cH₀, and far from observed a₀ = 1.2×10⁻¹⁰ m/s²)

The interpolation function from the excess temperature is:
    μ_excess(x) = √(1+x²) - 1  (normalized to linear at large x)

This is NOT the standard MOND interpolation function μ_standard(x) = x/√(1+x²).

**Milgrom himself explicitly acknowledged:** "An actual inertia-from-vacuum mechanism is still a far cry off."

**Key limitation:** Milgrom only analyzed the asymptotic limits (a ≫ a₀ and a ≪ a₀) and did not write the full interpolation function, and explicitly worried that the argument doesn't apply to circular orbits.

**Verdict:** Milgrom 1999 did NOT write T_U/T_dS = μ_MOND. Uses excess temperature (different formula, different interpolation function), and explicitly disclaimed the mechanism for circular/orbital trajectories.

---

### 1.2 Deser & Levin 1997 — Derived T_dS But No MOND Connection

**Paper:** "Accelerated Detectors and Temperature in (Anti) de Sitter Spaces," Deser & Levin (1997). *Class. Quantum Grav.* 14, L163. arXiv:gr-qc/9706018.

**Key result:** Derived 2πT = √(Λ/3 + a²) for uniformly accelerated detector in de Sitter space. This is T_dS(a) = (ℏ/2πck_B)√(a²+c²H₀²) in conventional notation.

**MOND connection:** The abstract and paper contain NO mention of MOND. The result was purely kinematic (the 5-acceleration in the embedding flat 5-space).

**Verdict:** Deser & Levin did not note any ratio or MOND connection.

---

### 1.3 Pikhitsa 2010 — Different Approach, Different Result

**Paper:** "MOND reveals the thermodynamics of gravity," Pikhitsa, P.V. (2010). arXiv:1010.0318.

**Key result:** Derives MOND equations from thermodynamics of gravity incorporating Hubble expansion. Predicts a₀ = 2cH₀ — same as the excess-temperature prediction of Milgrom 1999, but derived differently.

**Does not use:** Ratio T_U/T_dS. Different mechanism (thermodynamics of gravity, not Unruh/de Sitter ratio).

**Verdict:** Did not write T_U/T_dS = μ_MOND.

---

### 1.4 Verlinde 2016 — Different Mechanism, Closest Result Phenomenologically

See Part 2 for detailed comparison. Summary: Verlinde derives MOND from de Sitter elastic entropy, gets a different interpolation function, and achieves better agreement with observations (a₀_eff ≈ cH₀/6). Never mentions T_U/T_dS ratio.

---

### 1.5 McCulloch 2007–2017 — Different Approach

As documented in Exploration 003, McCulloch uses a Hubble-scale Casimir cutoff. The formula m_i = m(1 − 2c²/aΘ) is a completely different function. Never mentions T_U/T_dS.

---

### 1.6 Smolin 2017 — Quantum Gravity Perspective

**Paper:** "MOND as a regime of quantum gravity," Smolin, L. (2017). *Phys. Rev. D* 96, 083523. arXiv:1704.00780.

**Key result:** Proposes that MOND arises in the regime of quantum gravity phenomena at temperatures BELOW the de Sitter temperature T_dS. When a < a₀ (where a₀ ~ cH₀), the Unruh temperature T_U is below T_GH, and "standard quantum gravity" breaks down in a way that leads to MOND.

**Structural connection to T_U/T_dS:** Smolin's regime condition T_U < T_GH is equivalent to a < cH₀, which is precisely the condition where the T_U/T_dS ratio is significantly below 1. However, Smolin does NOT compute T_U/T_dS or identify it as the MOND interpolation function.

**Verdict:** Smolin 2017 shares the insight that de Sitter temperature sets the MOND scale, but uses a quantum gravity framework, not the temperature ratio.

---

### 1.7 Luo 2026 — Most Recent, Different Mechanism

**Paper:** "Local Short-Time Acceleration and deSitter Spacetime induced Extra Spectral Broadening," Luo, M.J. (2026). arXiv:2602.14515. [Very recent — February 2026]

**Key result:** Derives a_eff^r = √[(a_N + a_bg)² − a_bg²] ≈ √(2a_N a_bg) (deep-MOND limit) using *spectral broadening of quantum states* during non-equilibrium, short-time acceleration.

**Physical mechanism:** Completely different from T_U/T_dS:
- Does NOT assume thermal equilibrium
- Uses second-order moment quantum fluctuations (not temperature ratios)
- Invokes a "quantum equivalence principle" for second-order moments
- The de Sitter contribution comes from background spectral broadening, not equilibrium T_GH

**Explicit check:** Paper does NOT write T_U/T_dS = μ_MOND.

**Interpolation function:** a_eff^r = √[(a_N + a_bg)² − a_bg²], which is yet another functional form, different from both μ_standard = x/√(1+x²) and Milgrom's excess temperature.

---

### 1.8 Search Result: Direct Search for T_U/T_dS = μ_MOND

Direct web search for "T_U/T_dS" and "ratio of Unruh temperature" combined with "MOND interpolation function" returned **zero results**. This is strong confirmation that this specific ratio and its identification with the standard MOND interpolation function has not appeared in any indexed paper.

---

### 1.9 Summary: Novelty Assessment for T_U/T_dS = μ_MOND

**Finding:** The algebraic identity T_U(a)/T_dS(a) = a/√(a²+c²H₀²) = μ_standard_MOND(a/cH₀) appears to be **genuinely novel as an explicit identification**.

**Context:** The individual ingredients (T_dS formula since Deser & Levin 1997; μ_standard since Milgrom 1983) are well known. The connection between de Sitter temperature and MOND scale is known since Milgrom 1999. But the SPECIFIC claim that the RATIO T_U/T_dS equals the STANDARD MOND interpolation function exactly has not appeared in any paper found by this search.

**How the known prior work differs:**

| Paper | Formula Used | Why Different from T_U/T_dS |
|-------|-------------|------------------------------|
| Milgrom 1999 | T_dS − T_GH (excess temp) | Excess, not ratio; different μ; a₀ = 2cH₀ |
| Verlinde 2016 | Elastic entropy displacement | Different mechanism; no T_U/T_dS; different μ |
| Pikhitsa 2010 | Gravity thermodynamics | Different mechanism; a₀ = 2cH₀ |
| McCulloch 2007 | Hubble Casimir cutoff | Linear formula; completely different |
| Smolin 2017 | Quantum gravity regime below T_GH | Regime, not ratio; no explicit μ |
| Luo 2026 | Spectral broadening | Different mechanism; different μ |

**Caveat:** The identity is simple algebra — it might have been noticed in passing in unpublished notes or in papers not indexed by common search engines. Given its simplicity, the chance that someone has observed it informally is nonzero. However, no systematic derivation or physical motivation for m_i ∝ T_U/T_dS appears in the literature.

---

## Part 2: Detailed Comparison with Verlinde (2016)

### 2.1 Verlinde's Physical Mechanism

Verlinde's 2016 paper "Emergent Gravity and the Dark Universe" (arXiv:1611.02269) derives MOND-like behavior from:

1. **Entanglement entropy of spacetime**: Gravity emerges from entanglement entropy of an underlying quantum system
2. **Area law vs. volume law**: In de Sitter space, matter displaces entropy from area law (surface, responsible for gravity as in Bekenstein-Hawking) to volume law (bulk, the "dark energy" contribution)
3. **Elastic response**: The displaced entropy creates a restoring force — de Sitter space acts like an elastic medium
4. **Apparent dark matter**: This extra force, when interpreted as matter, mimics dark matter

**The key equation (for a spherically symmetric, static, point-mass exterior):**

Verlinde derives (his equation 7.40 for apparent dark matter):

    M_D²(r) = (a₀/6G) × r² × d/dr[r × M_B(r)]

where M_D is the apparent dark matter mass, M_B is baryonic mass, G is Newton's constant, and a₀ = cH₀.

For a POINT MASS M_B = M (constant), d/dr(rM) = M, so:

    M_D² = (a₀/6G) × r² × M_B = (cH₀/6G) × r² × M_B

The gravitational acceleration from apparent dark matter:

    g_D = G × M_D / r² = √(G × M_D² / r⁴) = √((cH₀/6) × G × M_B / r²) = √((cH₀/6) × g_B)

**In deep-MOND limit:**

    g_total ≈ g_D = √((cH₀/6) × g_B) = √(a₀_eff × g_B)

where a₀_eff = cH₀/6 ≈ 1.10 × 10⁻¹⁰ m/s² (within 8% of observed MOND a₀ = 1.2 × 10⁻¹⁰ m/s²).

This is only valid in the DEEP-MOND limit (g_B ≪ a₀_eff). Verlinde does NOT derive a full interpolation function connecting Newtonian and deep-MOND regimes.

---

### 2.2 Side-by-Side Equation Comparison

| Property | T_U/T_dS approach | Verlinde 2016 |
|----------|-------------------|---------------|
| **Physical mechanism** | Ratio of Unruh to de Sitter temperature modifies inertial mass | Elastic entropy displacement of de Sitter vacuum creates extra gravity force |
| **Key equation** | m_i = m × T_U/T_dS = m × a/√(a²+c²H₀²) | M_D² = (cH₀/6G) × r² × d(rM_B)/dr |
| **Modified inertia or gravity?** | Modified INERTIA | Modified GRAVITY (extra force) |
| **Full interpolation function** | μ(x) = x/√(1+x²) [standard MOND, exact] | None — only deep-MOND limit derived |
| **Deep-MOND limit** | g ≈ √(a₀ × g_B) with a₀ = cH₀ | g ≈ √(a₀ × g_B/6) with a₀ = cH₀ |
| **a₀ effective** | cH₀ = 6.60 × 10⁻¹⁰ m/s² (5.5× too large) | cH₀/6 ≈ 1.10 × 10⁻¹⁰ m/s² (8% low) |
| **Acceleration concept** | Proper acceleration of particle | Newtonian gravitational acceleration g_B = GM/r² |
| **Free-fall problem** | Fatal: free-fall → a_proper = 0 → T_U = 0 | Bypassed: uses g_B (Newtonian), not a_proper |
| **Observational performance** | Exact MOND interpolation function (well-validated if a₀ were corrected) | Fails: 100% deviation inside dwarfs, 7 orders off in solar system |
| **Connection to de Sitter** | Via Unruh effect temperature crossover | Via holographic entropy displacement |
| **T_U/T_dS ratio** | The central formula | Never computed or mentioned |

---

### 2.3 The Factor of 6 (or 2π) Difference in a₀

**T_U/T_dS approach:** a₀ = cH₀ = 6.60 × 10⁻¹⁰ m/s² (5.5× too large)

**Verlinde 2016:** a₀_eff = cH₀/6 ≈ 1.10 × 10⁻¹⁰ m/s² (8% low)

**Verlinde 2010:** a₀ = cH₀/(2π) ≈ 1.05 × 10⁻¹⁰ m/s² (13% low)

The factor of 6 in Verlinde 2016 comes from:
- The spatial volume of de Sitter space contributing to entropy displacement
- The area-to-volume ratio in the holographic calculation
- Geometric factors in the 3D treatment (4π factor from spherical averaging → factor of ~6)

The factor of 2π in Verlinde 2010 came from the standard Unruh formula 2πT = a, also appearing in the KMS periodicity.

**For T_U/T_dS:** There is no factor. The ratio is T_U/T_dS = a/√(a²+c²H₀²) directly, with no further numerical suppression. To get the correct a₀, one would need to divide by a factor of √(cH₀/(a₀_obs)) = √5.5 ≈ 2.3 somewhere in the derivation.

---

### 2.4 Different MOND Interpolation Functions — Observational Consequences

**Standard MOND interpolation (T_U/T_dS):** μ(x) = x/√(1+x²)

The equation of motion is: μ(a/a₀) × a = g_B → a²/√(a²+a₀²) = g_B

This gives the rotation curve:
- Newtonian: v² = GM/r (large r, dense mass)
- Deep MOND: v⁴ = GM × a₀ (flat rotation: v = const at large r)
- Transition: smooth, parameterized by μ

**Verlinde 2016:** g = g_B + √(g_B × a₀/6)

No simple interpolation function. In the interior of a galaxy (where g_B is changing), the derivative d(rM_B)/dr enters, making predictions depend on mass DISTRIBUTION, not just local acceleration. This is why Verlinde fails inside dwarf spheroidals: the formula gives different predictions than MOND in the interior region.

**Key observational difference:** For intermediate accelerations a ~ a₀:
- Standard MOND (T_U/T_dS formula) predicts smooth, specific transition shape
- Verlinde predicts different transition shape (determined by mass distribution gradient, not just g_B)

The radial acceleration relation (RAR) — the tight correlation between total and baryonic acceleration across thousands of galaxies — is naturally explained by MOND (both standard and simple interpolation functions). Verlinde's theory is INCONSISTENT with the RAR (Lelli et al. 2017, various subsequent papers).

The T_U/T_dS approach, if the a₀ problem could be fixed, would predict exactly the standard MOND interpolation function and thus reproduce the RAR. This is actually an observational ADVANTAGE over Verlinde.

---

### 2.5 Physical Content: How Related Are They?

**Shared elements:**
1. Both connect the MOND acceleration scale to cH₀
2. Both involve de Sitter spacetime physics
3. Both are motivated by the observation a₀ ~ cH₀ ~ c√Λ

**Fundamental differences:**
1. T_U/T_dS modifies inertia; Verlinde modifies gravity
2. T_U/T_dS uses equilibrium Unruh temperatures; Verlinde uses non-equilibrium entropy displacement
3. T_U/T_dS gives exact standard MOND; Verlinde gives approximate MOND (only for point-mass exterior, deep-MOND limit)
4. T_U/T_dS has a₀ = cH₀ (5.5× too large); Verlinde gets a₀_eff = cH₀/6 (8% low)

**Verdict:** T_U/T_dS approach and Verlinde 2016 are **genuinely different theories** that share only the observation that de Sitter physics sets the MOND scale. They are not equivalent, not simplifications of each other, and not in a derivation relation.

---

## Part 3: The Free-Fall Objection

### 3.1 The Objection Stated

Stars in galaxy rotation curves are in FREE FALL: they follow spacetime geodesics with zero proper acceleration. The standard Unruh effect produces temperature T_U = ℏa/(2πck_B) for observers with PROPER acceleration a. A freely-falling star has a_proper = 0, so T_U = 0.

**Explicit statement:** If m_i = m × T_U/T_dS, then for a freely-falling particle (a_proper = 0):
    m_i = m × 0/T_dS = 0

This is unphysical: the particle would have zero inertial mass. The free-fall objection is DEVASTATING for the T_U/T_dS approach as a modified-inertia mechanism.

---

### 3.2 Sciama-Candelas-Deutsch (1981)

**Paper:** "Quantum field theory, horizons and thermodynamics," Sciama, Candelas, Deutsch. *Advances in Physics* 30, 327–366 (1981).

**Relevant results:**
- A uniformly ACCELERATED observer (proper acceleration a ≠ 0) sees a thermal bath at T_U = ℏa/(2πck_B)
- A FREELY-FALLING observer sees approximately cold vacuum (in locally inertial frame)
- Near a Schwarzschild black hole: static observer (a = GM/r²) sees Hawking radiation; freely-falling observer sees cold vacuum

**Implication:** Orbital stars in free fall see approximately cold vacuum. They do NOT see T_GH or T_dS. Therefore, the thermal modification of inertia does NOT operate for orbital stars.

**Status:** This firmly establishes that the free-fall objection is NOT a misunderstanding — it is physically well-founded.

---

### 3.3 Jacobson 1995 — Local Rindler Horizons

**Paper:** "Thermodynamics of Spacetime: The Einstein Equation of State," Jacobson, T. (1995). *Phys. Rev. Lett.* 75, 1260. arXiv:gr-qc/9504004.

**Key insight:** Jacobson derives the Einstein equation by demanding that δQ = TdS hold for LOCAL RINDLER HORIZONS through every spacetime point, where T is the Unruh temperature of virtual accelerated observers (taking a → ∞).

**Relevance to free-fall problem:** Jacobson's derivation uses the thermodynamic properties of local Rindler horizons to derive spacetime dynamics. The Unruh temperature that enters is not the temperature of the actual particle, but of local virtual observers.

**Potential resolution route:** If the modification of dynamics arises from local Rindler horizon structure (as in Jacobson's framework), it could potentially apply to freely-falling particles — because the relevant temperature is determined by the CURVATURE of spacetime (related to local tidal forces/g_N), not the proper acceleration of the particle.

**However:** This would require the MOND interpolation function to arise from tidal forces or local curvature, not from T_U directly. This is closer to a modified-gravity interpretation (like Verlinde) than a modified-inertia interpretation. The connection to T_U/T_dS ratio specifically would be lost.

**Status:** Suggestive but does not constitute a resolution for the T_U/T_dS modified-inertia approach.

---

### 3.4 Verlinde's Resolution

In Verlinde's emergent gravity framework:
- The "acceleration" that enters the formula is the NEWTONIAN gravitational acceleration g_B = GM_B/r² (or equivalently, the gradient of the gravitational potential ∇Φ)
- This is NOT the proper acceleration of the freely-falling star
- Freely-falling stars DO experience g_B ≠ 0 even though a_proper = 0

**Why this works in Verlinde's framework:** The extra gravitational force arises from entropy displacement in the de Sitter vacuum. This is a property of the GRAVITATIONAL FIELD (i.e., the spacetime geometry around the mass distribution), not of the kinematics of individual particles. Any particle in the field — accelerating, free-falling, or stationary — experiences this extra force.

**Verdict:** Verlinde's modified-gravity formulation RESOLVES the free-fall objection by construction. The force depends on g_B = |∇Φ|, not on a_proper of the test particle.

**Key lesson:** The free-fall objection applies to MODIFIED INERTIA (T_U/T_dS approach) but NOT to MODIFIED GRAVITY (Verlinde approach).

---

### 3.5 Milgrom's Awareness of the Problem

Milgrom himself noted in 1999 (from the review):
> "this would reflect on a 'linear', constant-acceleration motion, while circular trajectories will probably behave differently."

This is a direct acknowledgment that his de Sitter temperature argument applies to linearly accelerating (Rindler) trajectories but NOT obviously to circular orbits (free fall in gravitational field). Milgrom treats this as a limitation of the argument, not a resolution.

**Significance:** The discoverer of MOND explicitly recognized in 1999 that the de Sitter temperature argument has unclear applicability to orbital dynamics. This has not been resolved in 25 years.

---

### 3.6 Approaches That Attempt Resolution

**Approach A: Reformulate as modified gravity**
Convert T_U/T_dS modified inertia into an equivalent modified gravity by replacing proper acceleration with g_N = GM/r². This resolves the free-fall objection but abandons the Unruh-effect motivation (since proper acceleration ≠ g_N in GR).

**Approach B: Phase-space/stochastic approach (Luo 2026)**
Luo argues that the relevant quantity is the local spectral broadening of quantum states, which depends on the LOCAL ACCELERATION (not proper) including gravitational contributions. In the non-equilibrium, short-time limit, the distinction between gravitational and inertial acceleration is blurred. This partially addresses the free-fall problem but requires the "quantum equivalence principle" conjecture.

**Approach C: de Sitter geodesic deviation**
In de Sitter space, even freely-falling geodesics experience tidal acceleration relative to the de Sitter background (due to cosmological expansion). For a particle in a galaxy orbit, the acceleration relative to pure Hubble flow is a_orbit ~ v²/r ~ g_B. This is NOT zero even in free fall. Some authors (implicitly) use this to justify replacing proper acceleration with g_B.

**Status of Approach C:** This is a potentially valid reformulation. In de Sitter spacetime, the "inertial frame" is the Hubble-flow frame, not the flat-space Minkowski frame. The proper acceleration RELATIVE TO THE DE SITTER BACKGROUND is g_B, not zero. This would give T_U → T_U(g_B) for orbital stars, resolving the free-fall objection. But this requires a careful derivation of the de Sitter-relative acceleration and has not been done rigorously.

---

### 3.7 Free-Fall Objection: Overall Assessment

| Approach | Status of Free-Fall Objection |
|----------|-------------------------------|
| T_U/T_dS modified inertia (proper acceleration) | **FATAL**: a_proper = 0 for free fall |
| Verlinde 2016 modified gravity | **Bypassed**: uses g_N = |∇Φ| not a_proper |
| Jacobson 1995 local Rindler | **Partial**: different application, not directly resolved |
| Milgrom 1999 excess temperature | **Acknowledged by Milgrom**: circular orbits unclear |
| Luo 2026 spectral broadening | **Partial**: non-equilibrium approach may bypass it |
| de Sitter geodesic deviation (Approach C) | **Potentially valid but unproven** |

**Bottom line:** The free-fall objection is the **strongest remaining obstacle** to the T_U/T_dS approach as a modified-inertia mechanism. Verlinde's modified-gravity formulation cleanly avoids it, which may explain why Verlinde's approach (despite its observational failures) has been more seriously pursued in the literature.

---

## Part 4: Assessment

### 4.1 Novelty Verdict

**T_U/T_dS = μ_standard_MOND:**

After extensive search, this specific algebraic identity has NOT been explicitly published. The closest prior work:
- Milgrom 1999: excess temperature T_dS − T_GH (different formula)
- Verlinde 2016: elastic entropy (different mechanism, no T_U/T_dS)
- Smolin 2017: quantum gravity regime (qualitative, no formula)
- Luo 2026: spectral broadening (different mechanism, different μ)

**Novelty status:** LIKELY NOVEL as an explicit statement. The connection between de Sitter temperature and MOND scale is known (Milgrom 1999), but the specific identity T_U/T_dS = μ_standard_MOND has not appeared.

**Value of the identity:** The identity is:
1. Algebraically trivial (ratio of two known formulas)
2. Potentially significant (identifies exact standard MOND interpolation function)
3. Physically unjustified (no derivation that m_i ∝ T_U/T_dS)
4. Historically novel (appears to have been missed in 25 years of related work)

**Intellectual comparison:** Milgrom 1999 noted that T_dS − T_GH has the right asymptotic behavior for MOND. Our result (Exploration 004) notes that T_U/T_dS has EXACTLY the right functional form (not just asymptotics) for the standard MOND interpolation function. This is a sharper, more specific observation — but still without a physical mechanism.

---

### 4.2 Distinctness from Verlinde

**Verdict: Genuinely distinct.**

| Dimension | T_U/T_dS | Verlinde 2016 | Verdict |
|-----------|-----------|---------------|---------|
| Mechanism | Modified inertia | Modified gravity | Different |
| Connection to de Sitter | Equilibrium temperature ratio | Entropy displacement | Different |
| Interpolation function | Exact standard MOND | Approximate, only deep-MOND | Different |
| a₀ from formula | cH₀ (5.5× too large) | cH₀/6 (8% low) | Different |
| Free-fall problem | Yes (problem) | No (bypassed) | Different |
| Observational predictions | Matches RAR | Fails RAR | Different |

**Summary:** The T_U/T_dS approach gives better PHENOMENOLOGY (exact MOND interpolation function, consistent with RAR) but worse NUMEROLOGY (a₀ off by 5.5×) and worse FOUNDATIONS (free-fall problem, no derivation). Verlinde gives better NUMEROLOGY (a₀ within 8%) but worse PHENOMENOLOGY (fails inside galaxies, fails solar system).

---

### 4.3 Free-Fall Status

**Status: Unresolved for T_U/T_dS modified-inertia approach.**

Best available resolutions:
1. **Reframe as modified gravity using g_B** (conceptually sound, but loses connection to Unruh T_U)
2. **de Sitter relative acceleration** (Approach C: a_proper relative to de Sitter Hubble flow = g_B for orbital stars; potentially valid but unproven)
3. **Verlinde's approach** (sidesteps the problem but is a different theory)

**Recommended resolution path:** The most defensible approach is to reformulate m_i = m × T_U(g_B)/T_dS(g_B), replacing proper acceleration with Newtonian tidal acceleration g_B. This gives the same formula (since the formula only involves the acceleration scale), avoids the free-fall problem, and corresponds to saying "the relevant Unruh temperature for MOND is the one associated with the Newtonian gravitational field, not the proper acceleration of the test particle." This is an ad hoc but physically motivated substitution, similar to how Verlinde uses g_N in his formula.

---

## Summary of Key Findings

### Literature Status of T_U/T_dS = μ_MOND

| Paper | What they found | Why different |
|-------|-----------------|---------------|
| Milgrom 1999 | T_dS − T_GH ~ MOND behavior (asymptotic only) | Excess, not ratio; different μ |
| Deser-Levin 1997 | T_dS formula derivation | No MOND connection |
| Verlinde 2016 | MOND from elastic entropy of de Sitter | Different mechanism; no T_U/T_dS |
| Pikhitsa 2010 | a₀ = 2cH₀ from gravity thermodynamics | Different; no T_U/T_dS |
| Smolin 2017 | MOND below de Sitter temperature | Qualitative regime argument only |
| Luo 2026 | Spectral broadening → MOND | Different mechanism; different μ |
| **T_U/T_dS (Exploration 004)** | **T_U/T_dS = μ_standard_MOND exactly** | **Appears novel** |

### Verlinde 2016 Comparison

- **Different mechanism**: Elastic entropy vs. temperature ratio
- **Different interpolation function**: Approximate (deep-MOND only) vs. exact standard MOND
- **Different a₀**: cH₀/6 (8% from observed) vs. cH₀ (5.5× off)
- **Different approach to free fall**: Bypassed (modified gravity) vs. fatal (modified inertia)
- **Not equivalent**, not simplifications of each other

### Free-Fall Objection

- **Unresolved** for T_U/T_dS modified-inertia approach
- **Resolved** by Verlinde's modified-gravity reformulation
- **Potential resolution** via de Sitter-relative acceleration (Approach C) — needs rigorous development
- The free-fall issue was recognized by Milgrom (1999) himself and has stood for 25 years

---

## References

1. Milgrom, M. (1999). "The modified dynamics as a vacuum effect." *Phys. Lett. A* 253, 273–279. arXiv:astro-ph/9805346.
2. Deser, S. & Levin, O. (1997). "Accelerated Detectors and Temperature in (Anti) de Sitter Spaces." *Class. Quantum Grav.* 14, L163. arXiv:gr-qc/9706018.
3. Verlinde, E. (2016). "Emergent Gravity and the Dark Universe." arXiv:1611.02269. Published in SciPost Physics.
4. Verlinde, E. (2010). "On the Origin of Gravity and the Laws of Newton." arXiv:1001.0785.
5. Pikhitsa, P.V. (2010). "MOND reveals the thermodynamics of gravity." arXiv:1010.0318.
6. McCulloch, M.E. (2007). "Modelling the Pioneer anomaly as modified inertia." *MNRAS* 376, 338.
7. Smolin, L. (2017). "MOND as a regime of quantum gravity." *Phys. Rev. D* 96, 083523. arXiv:1704.00780.
8. Luo, M.J. (2026). "Local Short-Time Acceleration and deSitter Spacetime induced Extra Spectral Broadening." arXiv:2602.14515.
9. Jacobson, T. (1995). "Thermodynamics of Spacetime: The Einstein Equation of State." *Phys. Rev. Lett.* 75, 1260. arXiv:gr-qc/9504004.
10. Sciama, D., Candelas, P., Deutsch, D. (1981). "Quantum field theory, horizons and thermodynamics." *Advances in Physics* 30, 327–366.
11. Milgrom, M. (1983). "A modification of the Newtonian dynamics." *ApJ* 270, 365.
12. Milgrom, M. (2020). "The a₀–cosmology connection in MOND." arXiv:2001.09729.
13. Famaey, B. & McGaugh, S. (2012). "Modified Newtonian Dynamics (MOND)." *Living Rev. Rel.* 15, 10.
14. Lelli, F. et al. (2017). "Testing Verlinde's emergent gravity with the Radial Acceleration Relation." *MNRAS Lett.* 468, L68. arXiv:1702.04355.
15. Brouwer, M. et al. (2017). "First test of Verlinde's theory of emergent gravity using weak gravitational lensing measurements." *MNRAS* 466, 2547.
